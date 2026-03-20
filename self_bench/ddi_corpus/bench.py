"""
Self-benchmark: DDI Corpus 2013 — Drug-Drug Interaction Type Classification

Task : Given a sentence mentioning two drugs, classify the DDI type.
Labels: advise, effect, mechanism, int
Data  : resources_metadata/drug_nlp/DDI_Corpus_2013/ddi_corpus.tsv
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from self_bench.utils import (
    load_tsv, sample_data, call_llm, extract_answer, compute_metrics, save_results,
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "resources_metadata", "drug_nlp", "DDI_Corpus_2013", "ddi_corpus.tsv",
)

LABELS = ["advise", "effect", "mechanism", "int"]

PROMPT_TEMPLATE = """\
You are a biomedical NLP expert. Your task is to classify the type of \
drug-drug interaction (DDI) described in the sentence below.

**Sentence:** {sentence}
**Drug 1:** {drug1}
**Drug 2:** {drug2}

**Possible labels:**
- advise: a recommendation or advice regarding the concomitant use of two drugs
- effect: the effect of a DDI (e.g. increased toxicity, decreased efficacy)
- mechanism: the pharmacokinetic or pharmacodynamic mechanism behind the DDI
- int: a generic interaction statement without further detail

Reply with ONLY the label on a single line.
Answer: """


def build_prompt(row: dict) -> str:
    return PROMPT_TEMPLATE.format(
        sentence=row["sentence"],
        drug1=row["drug1"],
        drug2=row["drug2"],
    )


def run(model: str = "gpt-4o-mini", n_samples: int = 50, seed: int = 42,
        output_dir: str | None = None) -> dict:
    """Run the DDI Corpus classification benchmark."""
    rows = load_tsv(DATA_PATH)
    if not rows:
        print(f"[ddi_corpus] No data found at {DATA_PATH}")
        return {}

    samples = sample_data(rows, n=n_samples, seed=seed)
    gold, pred, details = [], [], []

    for i, row in enumerate(samples):
        prompt = build_prompt(row)
        response = call_llm(prompt, model=model)
        label = extract_answer(response, LABELS)
        gold_label = row["ddi_type"].strip().lower()
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
        "dataset": "DDI_Corpus_2013",
        "task": "ddi_type_classification",
        "model": model,
        "n_samples": len(samples),
        "metrics": {k: v for k, v in metrics.items() if k != "classification_report"},
        "classification_report": metrics["classification_report"],
        "details": details,
    }

    print(f"\n[ddi_corpus] Accuracy: {metrics['accuracy']:.3f}  Macro-F1: {metrics['macro_f1']:.3f}")
    print(metrics["classification_report"])

    if output_dir:
        save_results(result, os.path.join(output_dir, "ddi_corpus_results.json"))

    return result


if __name__ == "__main__":
    run(output_dir=os.path.join(os.path.dirname(__file__), "results"))
