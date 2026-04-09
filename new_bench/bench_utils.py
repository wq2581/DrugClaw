"""
Extended benchmark utilities for new_bench.

Builds on self_bench.bench_utils and adds:
  - mode-based dispatch:  direct | simple | graph
      direct → pure LLM, no RAG
      simple → DrugClaw RAG with simple thinking mode
      graph  → DrugClaw RAG with full graph thinking mode
  - maskself option (for simple/graph modes)
  - BenchLogger: always-on, QueryLogger-style per-sample directory storage
      Each sample → its own subdir with:
          conversation.json    full messages array (system + user + assistant)
          raw_response.md      LLM output as Markdown
          metadata.json        prediction / gold / correct / timing
          reasoning_trace.md   RAG step-by-step reasoning (simple/graph only)
          evidence.json        retrieved content (simple/graph only)
      Run-level files:
          run_config.json      dataset / mode / maskself / timestamp
          run_results.json     final aggregated metrics (written at end)
      Global (one per log_dir):
          bench_index.json     index of every completed run
  - additional metric functions: AUROC, MRR, NDCG@k, Recall@k
  - run_ranking_bench()    — RepoDB-style ranking tasks
  - run_extraction_bench() — PHEE-style tuple extraction tasks

DEFAULT_LOG_DIR is used when no log_dir is supplied, so logs are always saved.
"""

import json
import math
import pickle
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

# Re-export shared helpers from self_bench so callers only need one import
from self_bench.bench_utils import (
    make_llm,
    llm_predict,
    make_system,
    extract_answer,
    compute_metrics,
    DATASET_SKILL_MAP,
)

# ── Defaults ─────────────────────────────────────────────────────────────
DEFAULT_LOG_DIR = "./new_bench_logs"

# ── Mode constants ───────────────────────────────────────────────────────
MODE_DIRECT = "direct"   # No RAG; pure single-turn LLM
MODE_SIMPLE = "simple"   # DrugClaw RAG, simple (one-shot) thinking mode
MODE_GRAPH  = "graph"    # DrugClaw RAG, full multi-agent graph thinking mode

ALL_MODES = (MODE_DIRECT, MODE_SIMPLE, MODE_GRAPH)


# ── DrugClaw system helper with explicit thinking mode ───────────────────

def system_predict_mode(
    system,
    query: str,
    dataset: str,
    thinking_mode: str,
    maskself: bool = False,
) -> tuple[str, dict]:
    """
    Query the DrugClaw RAG system with a given thinking_mode ("simple"/"graph").

    maskself=True  → exclude the dataset's own skill from retrieval
    maskself=False → allow all skills (including the dataset's own)
    """
    resource_filter = None
    if maskself:
        self_skill = DATASET_SKILL_MAP.get(dataset)
        if self_skill:
            resource_filter = [
                s.name
                for s in system.skill_registry.get_registered_skills()
                if s.name != self_skill
            ]

    result = system.query(
        query,
        thinking_mode=thinking_mode,
        resource_filter=resource_filter,
        verbose=False,
    )
    return result.get("answer", ""), result


# ── MCQ answer extraction ────────────────────────────────────────────────

def extract_mcq_answer(text: str, valid_keys: list[str] | None = None) -> str | None:
    """
    Extract a single letter choice (A-E) from LLM output for MCQ tasks.

    Strategy:
      1. JSON: {"answer": "A"}
      2. Pattern: "Answer: A" / "The answer is A" / "(A)"
      3. First standalone capital letter in valid_keys found in text
    """
    if valid_keys is None:
        valid_keys = ["A", "B", "C", "D", "E"]
    text_clean = text.strip()

    # 1) JSON
    try:
        obj = json.loads(text_clean)
        if isinstance(obj, dict):
            ans = obj.get("answer", obj.get("choice", obj.get("option")))
            if ans and str(ans).strip().upper() in valid_keys:
                return str(ans).strip().upper()
    except json.JSONDecodeError:
        pass

    # 2) Explicit pattern
    pattern = r"(?:answer|choice|option)\s*[:\s]+[\"']?\(?([A-Ea-e])\)?[\"']?"
    m = re.search(pattern, text_clean, re.I)
    if m:
        c = m.group(1).upper()
        if c in valid_keys:
            return c

    # 3) "The answer is (B)" / "correct answer is B."
    m2 = re.search(r"\b(?:is|:)\s*\(?([A-Ea-e])\)?[\s.,]", text_clean, re.I)
    if m2:
        c = m2.group(1).upper()
        if c in valid_keys:
            return c

    # 4) First standalone letter
    for m3 in re.finditer(r"\b([A-Ea-e])\b", text_clean):
        c = m3.group(1).upper()
        if c in valid_keys:
            return c

    return None


# ── Ranked-list extraction ────────────────────────────────────────────────

def parse_ranked_list(text: str, max_items: int = 100) -> list[str]:
    """
    Parse a ranked drug list from free-text LLM output.

    Handles:
      1. Numbered lists    (1. Aspirin / 1) Aspirin)
      2. Bullet lists      (- Aspirin / • Aspirin)
      3. Comma-separated   (Aspirin, Ibuprofen, ...)
      4. One drug per line
    """
    items: list[str] = []

    # Remove common header noise
    text = re.sub(
        r"(?i)^(here are|ranked list of|drugs that (treat|could treat)[^:]*:?\s*)", "",
        text.strip(),
    )

    lines = text.splitlines()
    for line in lines:
        line = re.sub(r"^\s*(\d+[\.\)]\s*|[-•*]\s*)", "", line).strip()
        line = re.sub(r"\s*[\(\[].*?[\)\]]", "", line).strip()
        line = re.sub(r"[,;].*$", "", line).strip()
        line = re.sub(r"^(?:drug|medication|agent|compound)\s*:\s*", "", line, flags=re.I).strip()
        if len(line) > 1:
            items.append(line)
        if len(items) >= max_items:
            break

    # Fall back to comma split if no line-based items found
    if not items:
        for part in re.split(r"[,;]", text):
            part = part.strip().strip(".")
            if len(part) > 1:
                items.append(part)
            if len(items) >= max_items:
                break

    return items


# ── Extraction tuple parser ───────────────────────────────────────────────

def parse_extraction_tuples(text: str) -> set[tuple[str, str]]:
    """
    Parse (drug, event) tuples from LLM output for event extraction tasks.

    Supports formats:
      Drug: <name>, Event: <description>
      <drug> → <event>   /   <drug> -> <event>
      - <drug>: <event>
    """
    tuples: set[tuple[str, str]] = set()

    for line in text.splitlines():
        line = line.strip().lstrip("-•*").strip()
        if not line:
            continue

        m = re.search(
            r"drug\s*:\s*([^,\n]+)[,\s]+(?:adverse\s+)?event\s*:\s*(.+)",
            line, re.I,
        )
        if m:
            tuples.add((m.group(1).strip().lower(), m.group(2).strip().lower()))
            continue

        m2 = re.search(r"(.+?)\s*[-–→]+\s*(.+)", line)
        if m2:
            tuples.add((m2.group(1).strip().lower(), m2.group(2).strip().lower()))
            continue

        m3 = re.search(r"\(([^)]+)\)\s*:\s*(.+)", line)
        if m3:
            tuples.add((m3.group(1).strip().lower(), m3.group(2).strip().lower()))

    return tuples


# ── Additional metrics ────────────────────────────────────────────────────

def compute_auroc(golds_binary: list[int], preds_binary: list[int]) -> float:
    """Compute AUROC from binary 0/1 gold and predicted labels."""
    try:
        from sklearn.metrics import roc_auc_score
        return round(float(roc_auc_score(golds_binary, preds_binary)), 4)
    except Exception:
        n_pos = sum(golds_binary)
        n_neg = len(golds_binary) - n_pos
        if n_pos == 0 or n_neg == 0:
            return 0.5
        tp_rate = sum(1 for g, p in zip(golds_binary, preds_binary) if g == 1 and p == 1) / n_pos
        tn_rate = sum(1 for g, p in zip(golds_binary, preds_binary) if g == 0 and p == 0) / n_neg
        return round((tp_rate + tn_rate) / 2.0, 4)


def compute_ranking_metrics(
    gold_sets: list[set[str]],
    ranked_lists: list[list[str]],
    k_recall: list[int] | None = None,
    k_ndcg: int = 20,
) -> dict[str, Any]:
    """Compute Recall@k, MRR, and NDCG@k_ndcg for a ranking task."""
    if k_recall is None:
        k_recall = [10, 50]

    recall_at: dict[int, list[float]] = {k: [] for k in k_recall}
    rrs: list[float] = []
    ndcgs: list[float] = []

    for gold, ranked in zip(gold_sets, ranked_lists):
        if not gold:
            continue
        gold_lower = {g.lower().strip() for g in gold}
        ranked_lower = [r.lower().strip() for r in ranked]

        for k in k_recall:
            top_k = set(ranked_lower[:k])
            recall_at[k].append(len(gold_lower & top_k) / len(gold_lower))

        rr = 0.0
        for idx, drug in enumerate(ranked_lower):
            if drug in gold_lower:
                rr = 1.0 / (idx + 1)
                break
        rrs.append(rr)

        dcg = sum(
            1.0 / math.log2(idx + 2)
            for idx, drug in enumerate(ranked_lower[:k_ndcg])
            if drug in gold_lower
        )
        ideal_len = min(len(gold_lower), k_ndcg)
        idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_len))
        ndcgs.append(dcg / idcg if idcg else 0.0)

    total = len(rrs)
    result: dict[str, Any] = {"total_queries": total}
    for k in k_recall:
        vals = recall_at[k]
        result[f"recall@{k}"] = round(sum(vals) / len(vals), 4) if vals else 0.0
    result["mrr"] = round(sum(rrs) / total, 4) if total else 0.0
    result[f"ndcg@{k_ndcg}"] = round(sum(ndcgs) / total, 4) if total else 0.0
    return result


def compute_extraction_f1(
    gold_sets: list[set[tuple[str, ...]]],
    pred_sets: list[set[tuple[str, ...]]],
) -> dict[str, Any]:
    """Compute micro Precision / Recall / F1 over extraction tuple sets."""
    tp = fp = fn = 0
    for gold, pred in zip(gold_sets, pred_sets):
        gold_norm = {tuple(x.lower() for x in t) for t in gold}
        pred_norm = {tuple(x.lower() for x in t) for t in pred}
        tp += len(gold_norm & pred_norm)
        fp += len(pred_norm - gold_norm)
        fn += len(gold_norm - pred_norm)

    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {
        "micro_f1":  round(f1, 4),
        "precision": round(prec, 4),
        "recall":    round(rec, 4),
        "tp": tp, "fp": fp, "fn": fn,
    }


# ── BenchLogger ───────────────────────────────────────────────────────────

class BenchLogger:
    """
    Always-on per-run logger modelled after QueryLogger.

    Directory layout (mirrors QueryLogger conventions):

        <log_dir>/
        ├── bench_index.json                  ← global index of all runs
        └── <dataset>_<mode>_<timestamp>/     ← one directory per run
            ├── run_config.json               ← dataset / mode / maskself / timestamp
            ├── run_results.json              ← final metrics (written at end)
            └── sample_<NNNN>/               ← one directory per sample
                ├── conversation.json         ← full messages [{role, content}]
                ├── raw_response.md           ← LLM output
                ├── metadata.json             ← prediction / gold / correct / timing
                ├── reasoning_trace.md        ← reasoning steps (RAG modes)
                └── evidence.json             ← retrieved content (RAG modes)
    """

    def __init__(self, log_dir: str, dataset: str, mode: str, maskself: bool = False):
        self.log_root = Path(log_dir).resolve()
        self.log_root.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.dataset  = dataset
        self.mode     = mode
        self.maskself = maskself
        self.ts       = ts
        self._count   = 0

        # Run directory
        run_name = f"{dataset}_{mode}_{ts}"
        self.run_dir = self.log_root / run_name
        self.run_dir.mkdir(parents=True, exist_ok=True)

        # run_config.json
        (self.run_dir / "run_config.json").write_text(
            json.dumps(
                {
                    "dataset":   dataset,
                    "mode":      mode,
                    "maskself":  maskself,
                    "timestamp": ts,
                    "log_dir":   str(self.log_root),
                },
                indent=2, ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        # Update / create global bench_index.json
        self._index_file = self.log_root / "bench_index.json"
        self._index = self._load_index()
        self._run_entry: dict = {
            "run_name":  run_name,
            "dataset":   dataset,
            "mode":      mode,
            "maskself":  maskself,
            "timestamp": ts,
            "run_dir":   str(self.run_dir),
            "total_samples": 0,
            "completed": False,
        }
        self._index["runs"].append(self._run_entry)
        self._save_index()

    # ── Index helpers ─────────────────────────────────────────────────

    def _load_index(self) -> dict:
        if self._index_file.exists():
            try:
                return json.loads(self._index_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return {"total_runs": 0, "runs": []}

    def _save_index(self):
        self._index_file.write_text(
            json.dumps(self._index, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ── Per-sample logging ────────────────────────────────────────────

    def log_sample(
        self,
        idx: int,
        system_prompt: str,
        user_prompt: str,
        raw_response: str,
        extracted: Any,
        gold: Any,
        elapsed_sec: float = 0.0,
        sys_result: dict | None = None,
    ):
        """
        Persist one sample's full dialogue and metadata.

        sys_result: the full DrugClaw result dict (for RAG modes); if provided,
                    reasoning_trace.md and evidence.json are also written.
        """
        sample_dir = self.run_dir / f"sample_{idx:04d}"
        sample_dir.mkdir(exist_ok=True)

        # 1. conversation.json — full message history
        messages = [
            {"role": "system",    "content": system_prompt},
            {"role": "user",      "content": user_prompt},
            {"role": "assistant", "content": raw_response},
        ]
        (sample_dir / "conversation.json").write_text(
            json.dumps(messages, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # 2. raw_response.md
        (sample_dir / "raw_response.md").write_text(
            f"# Sample {idx} — Raw LLM Response\n\n"
            f"**Mode**: {self.mode}  |  **Dataset**: {self.dataset}\n\n"
            f"---\n\n{raw_response}\n",
            encoding="utf-8",
        )

        # 3. metadata.json
        meta = {
            "sample_id":       idx,
            "dataset":         self.dataset,
            "mode":            self.mode,
            "extracted":       extracted if not isinstance(extracted, set) else list(extracted),
            "gold":            gold       if not isinstance(gold, set)      else list(gold),
            "correct":         extracted == gold,
            "elapsed_sec":     round(elapsed_sec, 3),
        }
        (sample_dir / "metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

        # 4. RAG-specific files (reasoning_trace.md + evidence.json)
        if sys_result:
            self._write_reasoning_trace(sample_dir, idx, sys_result)
            self._write_evidence(sample_dir, sys_result)

        # 5. Pickle for deep inspection
        with open(sample_dir / "full_record.pkl", "wb") as f:
            pickle.dump(
                {
                    "sample_id":    idx,
                    "system_prompt": system_prompt,
                    "user_prompt":  user_prompt,
                    "raw_response": raw_response,
                    "extracted":    extracted,
                    "gold":         gold,
                    "correct":      extracted == gold,
                    "sys_result":   sys_result,
                },
                f,
            )

        self._count += 1

    def _write_reasoning_trace(self, sample_dir: Path, idx: int, sys_result: dict):
        reasoning_history = sys_result.get("reasoning_history", [])
        reflection = sys_result.get("reflection_feedback", "")

        lines = [
            f"# Reasoning Trace — Sample {idx}\n",
            f"> **Mode**: {self.mode}\n",
            f"> **Dataset**: {self.dataset}\n",
            "",
        ]

        if reasoning_history:
            for step in reasoning_history:
                step_num = step.get("step", "?")
                reward   = step.get("reward", 0.0)
                suf      = step.get("evidence_sufficiency", 0.0)
                action   = step.get("action", "")
                thought  = step.get("thought", "")
                lines += [
                    f"## Step {step_num}  (reward={reward:.3f}, sufficiency={suf:.3f})",
                    "",
                    f"**Action**: {action}",
                    "",
                    f"**Thought**: {thought}",
                    "",
                ]
        else:
            lines.append("*No multi-step reasoning (single-shot / simple mode).*\n")

        if reflection:
            lines += ["", "## Reflection Feedback", "", reflection, ""]

        (sample_dir / "reasoning_trace.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )

    def _write_evidence(self, sample_dir: Path, sys_result: dict):
        evidence = {
            "retrieved_content":   sys_result.get("retrieved_content", []),
            "retrieved_text":      sys_result.get("retrieved_text", ""),
            "web_search_results":  sys_result.get("web_search_results", []),
            "evidence_graph_size": sys_result.get("evidence_graph_size", 0),
            "final_reward":        sys_result.get("final_reward", 0.0),
            "iterations":          sys_result.get("iterations", 0),
        }
        (sample_dir / "evidence.json").write_text(
            json.dumps(evidence, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

    # ── Finalise run ──────────────────────────────────────────────────

    def save_results(self, metrics: dict):
        """Write run_results.json and update the global bench_index."""
        (self.run_dir / "run_results.json").write_text(
            json.dumps(metrics, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # Update the run entry in the index
        self._run_entry["total_samples"] = self._count
        self._run_entry["completed"]     = True
        self._run_entry["metrics"]       = {
            k: v for k, v in metrics.items()
            if not isinstance(v, dict)      # skip per_class nesting
        }
        self._index["total_runs"] = len(self._index["runs"])
        self._save_index()

        print(
            f"[BenchLogger] {self._count} samples saved → {self.run_dir}\n"
            f"             bench_index → {self._index_file}"
        )


# ── Internal helpers ──────────────────────────────────────────────────────

def _init_inference(mode: str, key_file: str | None):
    """Initialise LLM or DrugClaw system based on mode."""
    if mode in (MODE_SIMPLE, MODE_GRAPH):
        return None, make_system(key_file)
    llm, _ = make_llm(key_file)
    return llm, None


def _get_response(
    system_prompt: str,
    user_prompt: str,
    mode: str,
    dataset_name: str,
    maskself: bool,
    llm=None,
    system=None,
) -> tuple[str, dict | None]:
    """
    Dispatch to direct LLM or RAG system.

    Returns (raw_response_text, sys_result_or_None).
    sys_result is the full DrugClaw result dict (only for RAG modes).
    """
    if mode in (MODE_SIMPLE, MODE_GRAPH):
        query = f"{system_prompt}\n\n{user_prompt}"
        resp, sys_result = system_predict_mode(
            system, query, dataset_name, thinking_mode=mode, maskself=maskself
        )
        return resp, sys_result
    else:
        resp = llm_predict(llm, system_prompt, user_prompt)
        return resp, None


# ── Generic classification bench runner ──────────────────────────────────

def run_bench(
    *,
    dataset_name: str,
    labels: list[str],
    default_label: str,
    system_prompt: str,
    samples: list[dict],
    format_prompt: Callable[[dict], str],
    mode: str = MODE_DIRECT,
    maskself: bool = False,
    key_file: str | None = None,
    log_dir: str | None = None,
    answer_extractor: Callable[[str], str | None] | None = None,
) -> dict:
    """
    Run a classification benchmark in any mode.

    Logs are always saved to log_dir (defaults to DEFAULT_LOG_DIR).
    answer_extractor: optional override for label extraction from raw text.
    """
    if not samples:
        return {"error": "No data loaded", "total": 0}

    log_dir = log_dir or DEFAULT_LOG_DIR
    llm, system = _init_inference(mode, key_file)
    logger = BenchLogger(log_dir, dataset_name, mode, maskself)

    golds: list[str] = []
    preds: list[str] = []

    for i, sample in enumerate(samples):
        user_prompt = format_prompt(sample)
        t0 = time.time()

        resp, sys_result = _get_response(
            system_prompt, user_prompt,
            mode, dataset_name, maskself, llm, system,
        )

        elapsed = time.time() - t0

        if answer_extractor:
            pred = answer_extractor(resp) or default_label
        else:
            pred = extract_answer(resp, labels) or default_label

        golds.append(sample["gold"])
        preds.append(pred)

        logger.log_sample(
            idx=i,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            raw_response=resp,
            extracted=pred,
            gold=sample["gold"],
            elapsed_sec=elapsed,
            sys_result=sys_result,
        )

    metrics = compute_metrics(golds, preds, labels)
    logger.save_results(metrics)
    return metrics


def run_binary_bench(
    *,
    dataset_name: str,
    pos_label: str,
    neg_label: str,
    default_label: str,
    system_prompt: str,
    samples: list[dict],
    format_prompt: Callable[[dict], str],
    mode: str = MODE_DIRECT,
    maskself: bool = False,
    key_file: str | None = None,
    log_dir: str | None = None,
) -> dict:
    """
    Binary classification bench that also computes AUROC.
    Internally delegates to run_bench then adds AUROC from per-class recalls.
    """
    labels = [pos_label, neg_label]
    metrics = run_bench(
        dataset_name=dataset_name,
        labels=labels,
        default_label=default_label,
        system_prompt=system_prompt,
        samples=samples,
        format_prompt=format_prompt,
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
    )

    pc = metrics.get("per_class", {})
    if pos_label in pc and neg_label in pc:
        tpr = pc[pos_label].get("recall", 0.0)
        tnr = pc[neg_label].get("recall", 0.0)
        metrics["auroc"] = round((tpr + tnr) / 2.0, 4)

    return metrics


# ── Extraction bench runner ───────────────────────────────────────────────

def run_extraction_bench(
    *,
    dataset_name: str,
    system_prompt: str,
    samples: list[dict],
    format_prompt: Callable[[dict], str],
    parse_response: Callable[[str], set[tuple]] | None = None,
    mode: str = MODE_DIRECT,
    maskself: bool = False,
    key_file: str | None = None,
    log_dir: str | None = None,
) -> dict:
    """
    Event-extraction benchmark. Each sample must have a "gold_tuples" field.
    Computes micro Precision / Recall / F1.
    """
    if not samples:
        return {"error": "No data loaded", "total": 0}

    if parse_response is None:
        parse_response = parse_extraction_tuples

    log_dir = log_dir or DEFAULT_LOG_DIR
    llm, system = _init_inference(mode, key_file)
    logger = BenchLogger(log_dir, dataset_name, mode, maskself)

    gold_sets: list[set[tuple]] = []
    pred_sets: list[set[tuple]] = []

    for i, sample in enumerate(samples):
        user_prompt = format_prompt(sample)
        t0 = time.time()

        resp, sys_result = _get_response(
            system_prompt, user_prompt,
            mode, dataset_name, maskself, llm, system,
        )

        elapsed   = time.time() - t0
        pred_tuples = parse_response(resp)
        gold_tuples = sample["gold_tuples"]

        gold_sets.append(gold_tuples)
        pred_sets.append(pred_tuples)

        logger.log_sample(
            idx=i,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            raw_response=resp,
            extracted=pred_tuples,
            gold=gold_tuples,
            elapsed_sec=elapsed,
            sys_result=sys_result,
        )

    metrics = compute_extraction_f1(gold_sets, pred_sets)
    metrics["total"] = len(samples)
    logger.save_results(metrics)
    return metrics


# ── Ranking bench runner ──────────────────────────────────────────────────

def run_ranking_bench(
    *,
    dataset_name: str,
    system_prompt: str,
    queries: list[dict],
    format_prompt: Callable[[dict], str],
    k_recall: list[int] | None = None,
    k_ndcg: int = 20,
    mode: str = MODE_DIRECT,
    maskself: bool = False,
    key_file: str | None = None,
    log_dir: str | None = None,
) -> dict:
    """
    Ranking benchmark. Each query must have a "gold_drugs" (set of strings) field.
    Computes Recall@k, MRR, NDCG@k_ndcg.
    """
    if not queries:
        return {"error": "No data loaded", "total_queries": 0}

    if k_recall is None:
        k_recall = [10, 50]

    log_dir = log_dir or DEFAULT_LOG_DIR
    llm, system = _init_inference(mode, key_file)
    logger = BenchLogger(log_dir, dataset_name, mode, maskself)

    gold_sets:    list[set[str]]   = []
    ranked_lists: list[list[str]]  = []

    for i, query in enumerate(queries):
        user_prompt = format_prompt(query)
        t0 = time.time()

        resp, sys_result = _get_response(
            system_prompt, user_prompt,
            mode, dataset_name, maskself, llm, system,
        )

        elapsed = time.time() - t0
        ranked  = parse_ranked_list(resp)
        gold_sets.append(query["gold_drugs"])
        ranked_lists.append(ranked)

        logger.log_sample(
            idx=i,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            raw_response=resp,
            extracted=ranked[:20],
            gold=list(query["gold_drugs"])[:20],
            elapsed_sec=elapsed,
            sys_result=sys_result,
        )

    metrics = compute_ranking_metrics(gold_sets, ranked_lists, k_recall=k_recall, k_ndcg=k_ndcg)
    logger.save_results(metrics)
    return metrics
