"""
Self-benchmark: DrugProt — Drug-Protein Relation Type Classification

Task : Given a sentence with a drug and a protein/gene, classify the relation.
Labels: INHIBITOR, SUBSTRATE, AGONIST, ANTAGONIST, INDIRECT-DOWNREGULATOR,
        INDIRECT-UPREGULATOR, ACTIVATOR, PRODUCT-OF, PART-OF, DIRECT-REGULATOR
Data  : resources_metadata/drug_nlp/DrugProt/drugprot.tsv
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from self_bench.utils import (
    load_tsv, sample_data, call_llm, extract_answer, compute_metrics, save_results,
)

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "resources_metadata", "drug_nlp", "DrugProt", "drugprot.tsv",
)

LABELS = [
    "INHIBITOR", "SUBSTRATE", "AGONIST", "ANTAGONIST",
    "INDIRECT-DOWNREGULATOR", "INDIRECT-UPREGULATOR",
    "ACTIVATOR", "PRODUCT-OF", "PART-OF", "DIRECT-REGULATOR",
]

PROMPT_TEMPLATE = """\
You are a biomedical NLP expert. Your task is to classify the relation type \
between a drug/chemical and a gene/protein mentioned in the sentence below.

**Sentence:** {sentence}
**Drug/Chemical:** {entity1}
**Gene/Protein:** {entity2}

**Possible labels:**
- INHIBITOR: the drug inhibits the protein
- SUBSTRATE: the drug is a substrate of the protein (e.g. metabolized by)
- AGONIST: the drug is an agonist of the protein
- ANTAGONIST: the drug is an antagonist of the protein
- INDIRECT-DOWNREGULATOR: the drug indirectly downregulates the protein
- INDIRECT-UPREGULATOR: the drug indirectly upregulates the protein
- ACTIVATOR: the drug activates the protein
- PRODUCT-OF: the drug is a product of the protein
- PART-OF: part-of relationship
- DIRECT-REGULATOR: the drug directly regulates the protein

Reply with ONLY the label on a single line.
Answer: """


def build_prompt(row: dict) -> str:
    return PROMPT_TEMPLATE.format(
        sentence=row["sentence"],
        entity1=row["entity1"],
        entity2=row["entity2"],
    )


def run(model: str = "gpt-4o-mini", n_samples: int = 50, seed: int = 42,
        output_dir: str | None = None) -> dict:
    """Run the DrugProt relation classification benchmark."""
    rows = load_tsv(DATA_PATH)
    if not rows:
        print(f"[drugprot] No data found at {DATA_PATH}")
        return {}

    samples = sample_data(rows, n=n_samples, seed=seed)
    gold, pred, details = [], [], []

    for i, row in enumerate(samples):
        prompt = build_prompt(row)
        response = call_llm(prompt, model=model)
        label = extract_answer(response, LABELS)
        gold_label = row["relation_type"].strip()
        pred_label = label or "UNKNOWN"
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
        "dataset": "DrugProt",
        "task": "relation_type_classification",
        "model": model,
        "n_samples": len(samples),
        "metrics": {k: v for k, v in metrics.items() if k != "classification_report"},
        "classification_report": metrics["classification_report"],
        "details": details,
    }

    print(f"\n[drugprot] Accuracy: {metrics['accuracy']:.3f}  Macro-F1: {metrics['macro_f1']:.3f}")
    print(metrics["classification_report"])

    if output_dir:
        save_results(result, os.path.join(output_dir, "drugprot_results.json"))

    return result


if __name__ == "__main__":
    run(output_dir=os.path.join(os.path.dirname(__file__), "results"))
