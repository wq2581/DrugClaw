"""
Self-benchmark: PHEE — Pharmacovigilance Event Type Classification

Task : Given a sentence describing a pharmacovigilance event, classify
       whether it is an adverse drug event or a potential therapeutic event.
Labels: adverse_event, therapeutic_outcome
Data  : resources_metadata/drug_nlp/PHEE/phee.json
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from self_bench.utils import (
    load_json, sample_data, call_llm, extract_answer, compute_metrics, save_results,
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "resources_metadata", "drug_nlp", "PHEE", "phee.json",
)

LABELS = ["adverse_event", "therapeutic_outcome"]

PROMPT_TEMPLATE = """\
You are a pharmacovigilance NLP expert. Your task is to classify the type of \
pharmacovigilance event described in the sentence below.

**Sentence:** {sentence}
**Drug:** {drug}
**Effect:** {effect}

**Possible labels:**
- adverse_event: the sentence describes an adverse drug event (harmful side effect)
- therapeutic_outcome: the sentence describes a beneficial therapeutic effect

Reply with ONLY the label on a single line.
Answer: """


def build_prompt(row: dict) -> str:
    return PROMPT_TEMPLATE.format(
        sentence=row.get("sentence", ""),
        drug=row.get("drug", ""),
        effect=row.get("effect", ""),
    )


def run(model: str = "gpt-4o-mini", n_samples: int = 50, seed: int = 42,
        output_dir: str | None = None) -> dict:
    """Run the PHEE event type classification benchmark."""
    rows = load_json(DATA_PATH)
    if not rows:
        print(f"[phee] No data found at {DATA_PATH}")
        return {}

    # Filter to rows that have event_type
    rows = [r for r in rows if r.get("event_type")]
    samples = sample_data(rows, n=n_samples, seed=seed)
    gold, pred, details = [], [], []

    for i, row in enumerate(samples):
        prompt = build_prompt(row)
        response = call_llm(prompt, model=model)
        label = extract_answer(response, LABELS)
        gold_label = row["event_type"].strip().lower()
        pred_label = (label or "UNKNOWN").lower()
        gold.append(gold_label)
        pred.append(pred_label)
        details.append({
            "id": i,
            "gold": gold_label,
            "pred": pred_label,
            "raw_response": response,
            "sentence": row.get("sentence", "")[:200],
        })
        print(f"  [{i+1}/{len(samples)}] gold={gold_label} pred={pred_label}")

    metrics = compute_metrics(gold, pred)
    result = {
        "dataset": "PHEE",
        "task": "event_type_classification",
        "model": model,
        "n_samples": len(samples),
        "metrics": {k: v for k, v in metrics.items() if k != "classification_report"},
        "classification_report": metrics["classification_report"],
        "details": details,
    }

    print(f"\n[phee] Accuracy: {metrics['accuracy']:.3f}  Macro-F1: {metrics['macro_f1']:.3f}")
    print(metrics["classification_report"])

    if output_dir:
        save_results(result, os.path.join(output_dir, "phee_results.json"))

    return result


if __name__ == "__main__":
    run(output_dir=os.path.join(os.path.dirname(__file__), "results"))
