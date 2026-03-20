"""
Shared utilities for self-bench: LLM calling, answer extraction, metrics.
"""

import json
import os
import re
import time
from collections import Counter
from typing import Optional


# ---------------------------------------------------------------------------
# LLM interface
# ---------------------------------------------------------------------------

def call_llm(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.0,
             max_tokens: int = 256) -> str:
    """Call an OpenAI-compatible LLM and return the text response.

    Supports the ``OPENAI_API_KEY`` env var.  Falls back to a placeholder
    when no key is set so the benchmark scaffolding can still be tested.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

    if not api_key:
        return "[NO_API_KEY]"

    try:
        import openai
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM_ERROR] {e}"


# ---------------------------------------------------------------------------
# Answer extraction
# ---------------------------------------------------------------------------

def extract_answer(text: str, valid_labels: list[str]) -> Optional[str]:
    """Extract a predicted label from free-form LLM output.

    Strategy:
      1. Look for ``Answer: <label>`` pattern.
      2. Look for a label appearing on its own line.
      3. Case-insensitive substring match against valid labels.
    """
    if not text:
        return None

    low = text.lower().strip()

    # 1. "Answer: <label>"
    m = re.search(r"answer\s*:\s*(.+)", low)
    if m:
        candidate = m.group(1).strip().strip("\"'`.").lower()
        for lab in valid_labels:
            if lab.lower() == candidate:
                return lab

    # 2. Check each line
    for line in low.splitlines():
        line = line.strip().strip("\"'`.")
        for lab in valid_labels:
            if line == lab.lower():
                return lab

    # 3. Substring match (prefer longer matches first)
    sorted_labels = sorted(valid_labels, key=len, reverse=True)
    for lab in sorted_labels:
        if lab.lower() in low:
            return lab

    return None


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_metrics(gold: list[str], pred: list[str]) -> dict:
    """Compute accuracy, per-class precision/recall/F1, and macro-F1.

    Returns a dict with ``accuracy``, ``macro_f1``, ``per_class``, and
    ``classification_report`` (formatted string).
    """
    assert len(gold) == len(pred), "gold and pred must have the same length"
    n = len(gold)
    if n == 0:
        return {"accuracy": 0.0, "macro_f1": 0.0, "per_class": {}, "classification_report": ""}

    correct = sum(g == p for g, p in zip(gold, pred))
    accuracy = correct / n

    labels = sorted(set(gold))
    per_class = {}
    for lab in labels:
        tp = sum(1 for g, p in zip(gold, pred) if g == lab and p == lab)
        fp = sum(1 for g, p in zip(gold, pred) if g != lab and p == lab)
        fn = sum(1 for g, p in zip(gold, pred) if g == lab and p != lab)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        per_class[lab] = {"precision": prec, "recall": rec, "f1": f1,
                          "support": sum(1 for g in gold if g == lab)}

    macro_f1 = sum(v["f1"] for v in per_class.values()) / len(per_class) if per_class else 0.0

    # Formatted report
    lines = [f"{'Label':<25} {'Prec':>6} {'Rec':>6} {'F1':>6} {'Support':>8}"]
    lines.append("-" * 55)
    for lab in labels:
        m = per_class[lab]
        lines.append(f"{lab:<25} {m['precision']:>6.3f} {m['recall']:>6.3f} "
                      f"{m['f1']:>6.3f} {m['support']:>8d}")
    lines.append("-" * 55)
    lines.append(f"{'Accuracy':<25} {'':<6} {'':<6} {accuracy:>6.3f} {n:>8d}")
    lines.append(f"{'Macro F1':<25} {'':<6} {'':<6} {macro_f1:>6.3f}")
    report = "\n".join(lines)

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "per_class": per_class,
        "classification_report": report,
        "total": n,
        "correct": correct,
    }


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_tsv(path: str) -> list[dict]:
    """Load a TSV file with header row into a list of dicts."""
    import csv
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows


def load_csv(path: str) -> list[dict]:
    """Load a CSV file with header row into a list of dicts."""
    import csv
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_json(path: str) -> list[dict]:
    """Load a JSON file (expects a list of objects)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get("data", [])


def sample_data(rows: list[dict], n: int = 50, seed: int = 42) -> list[dict]:
    """Deterministically sample up to *n* rows."""
    import random
    rng = random.Random(seed)
    if len(rows) <= n:
        return list(rows)
    return rng.sample(rows, n)


# ---------------------------------------------------------------------------
# Result I/O
# ---------------------------------------------------------------------------

def save_results(results: dict, path: str) -> None:
    """Save benchmark results to a JSON file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {path}")
