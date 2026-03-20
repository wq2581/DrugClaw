"""
Self-benchmark: CADEC — Adverse Drug Reaction Detection (Binary)

Task : Given a patient-reported text about a drug, classify whether an
       adverse drug reaction (ADR) is present.
Labels: present, absent
Data  : resources_metadata/drug_nlp/CADEC/cadec.csv
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from self_bench.utils import (
    load_csv, sample_data, call_llm, extract_answer, compute_metrics, save_results,
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "resources_metadata", "drug_nlp", "CADEC", "cadec.csv",
)

LABELS = ["present", "absent"]

PROMPT_TEMPLATE = """\
You are a pharmacovigilance expert. Your task is to determine whether an \
adverse drug reaction (ADR) is described in the following patient report.

**Patient text:** {text}
**Drug mentioned:** {drug}
**Adverse event candidate:** {adverse_event}

Does this text indicate that the adverse drug reaction is present?

Reply with ONLY one of: present, absent
Answer: """


def build_prompt(row: dict) -> str:
    return PROMPT_TEMPLATE.format(
        text=row["text"],
        drug=row["drug"],
        adverse_event=row.get("adverse_event", ""),
    )


def run(model: str = "gpt-4o-mini", n_samples: int = 50, seed: int = 42,
        output_dir: str | None = None) -> dict:
    """Run the CADEC ADR detection benchmark."""
    rows = load_csv(DATA_PATH)
    if not rows:
        print(f"[cadec] No data found at {DATA_PATH}")
        return {}

    samples = sample_data(rows, n=n_samples, seed=seed)
    gold, pred, details = [], [], []

    for i, row in enumerate(samples):
        prompt = build_prompt(row)
        response = call_llm(prompt, model=model)
        label = extract_answer(response, LABELS)
        gold_label = row["label"].strip().lower()
        pred_label = (label or "UNKNOWN").lower()
        gold.append(gold_label)
        pred.append(pred_label)
        details.append({
            "id": i,
            "gold": gold_label,
            "pred": pred_label,
            "raw_response": response,
            "text": row["text"][:200],
        })
        print(f"  [{i+1}/{len(samples)}] gold={gold_label} pred={pred_label}")

    metrics = compute_metrics(gold, pred)
    result = {
        "dataset": "CADEC",
        "task": "adr_binary_classification",
        "model": model,
        "n_samples": len(samples),
        "metrics": {k: v for k, v in metrics.items() if k != "classification_report"},
        "classification_report": metrics["classification_report"],
        "details": details,
    }

    print(f"\n[cadec] Accuracy: {metrics['accuracy']:.3f}  Macro-F1: {metrics['macro_f1']:.3f}")
    print(metrics["classification_report"])

    if output_dir:
        save_results(result, os.path.join(output_dir, "cadec_results.json"))

    return result


if __name__ == "__main__":
    run(output_dir=os.path.join(os.path.dirname(__file__), "results"))
