"""
Self-benchmark: n2c2 2018 Track 2 — Adverse Drug Event Detection (Binary)

Task : Given a sentence mentioning a drug, classify whether an adverse drug
       event (ADE) is present.
Labels: positive, negative
Data  : resources_metadata/drug_nlp/n2c2_2018/n2c2_2018.tsv
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from self_bench.utils import (
    load_tsv, sample_data, call_llm, extract_answer, compute_metrics, save_results,
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "resources_metadata", "drug_nlp", "n2c2_2018", "n2c2_2018.tsv",
)

LABELS = ["positive", "negative"]

PROMPT_TEMPLATE = """\
You are a clinical NLP expert. Your task is to determine whether the following \
clinical sentence describes an adverse drug event (ADE) associated with the \
given drug.

**Sentence:** {sentence}
**Drug:** {drug}
**Adverse event mentioned:** {adverse_event}

Is this a true adverse drug event (the drug caused or is associated with the \
adverse event)?

Reply with ONLY one of: positive, negative
Answer: """


def build_prompt(row: dict) -> str:
    return PROMPT_TEMPLATE.format(
        sentence=row["sentence"],
        drug=row["drug"],
        adverse_event=row.get("adverse_event", row.get("ae", "")),
    )


def run(model: str = "gpt-4o-mini", n_samples: int = 50, seed: int = 42,
        output_dir: str | None = None) -> dict:
    """Run the n2c2 2018 ADE detection benchmark."""
    rows = load_tsv(DATA_PATH)
    if not rows:
        print(f"[n2c2_2018] No data found at {DATA_PATH}")
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
            "sentence": row["sentence"][:200],
        })
        print(f"  [{i+1}/{len(samples)}] gold={gold_label} pred={pred_label}")

    metrics = compute_metrics(gold, pred)
    result = {
        "dataset": "n2c2_2018",
        "task": "ade_binary_classification",
        "model": model,
        "n_samples": len(samples),
        "metrics": {k: v for k, v in metrics.items() if k != "classification_report"},
        "classification_report": metrics["classification_report"],
        "details": details,
    }

    print(f"\n[n2c2_2018] Accuracy: {metrics['accuracy']:.3f}  Macro-F1: {metrics['macro_f1']:.3f}")
    print(metrics["classification_report"])

    if output_dir:
        save_results(result, os.path.join(output_dir, "n2c2_2018_results.json"))

    return result


if __name__ == "__main__":
    run(output_dir=os.path.join(os.path.dirname(__file__), "results"))
