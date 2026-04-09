"""
Drug Repurposing — RepoDB.

Task  : Given a disease, rank candidate drugs by evidence for treatment.
Data  : new_bench_data/RepoDB/full.csv
        CSV: drug_name, drugbank_id, ind_name, ind_id, NCT, status, phase, DetailedStatus
        Gold = all "Approved" drugs for each disease (ind_name).
        Only diseases with ≥3 approved drugs are included (~200 diseases).
Prompt: "What drugs could treat {disease}? List as many as you can, one per line."
Metric: Recall@10, Recall@50, MRR, NDCG@20
        (parsed from ranked drug list in LLM output)
"""

import csv
import random
from collections import defaultdict
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "new_bench_data/RepoDB/full.csv"
)

MIN_APPROVED_DRUGS = 3    # minimum approved drugs per disease to include
MAX_DISEASES = 200        # cap on number of diseases (for manageable runtime)

SYSTEM_PROMPT = """\
You are a pharmacology expert specialising in drug repurposing.

Task: Given a disease name, list all drugs that could treat it.
Rank your suggestions from most to least evidence-based.
Include both approved and investigational agents you are aware of.

Output format — one drug per line, numbered:
  1. <drug name>
  2. <drug name>
  ...

List as many drugs as you can (aim for at least 20).
"""

USER_TEMPLATE = """\
Disease: {disease}

What drugs could treat this disease? Rank by strength of evidence.
"""


def load_data(max_samples: int = 0, seed: int = 42) -> list[dict]:
    """
    Load RepoDB, group by disease, keep diseases with ≥ MIN_APPROVED_DRUGS.
    Returns a list of query dicts: {disease, gold_drugs (set)}.
    max_samples: if > 0, limit to this many diseases.
    """
    disease_drugs: dict[str, set[str]] = defaultdict(set)

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status", "").strip() == "Approved":
                disease = row["ind_name"].strip()
                drug = row["drug_name"].strip()
                if disease and drug:
                    disease_drugs[disease].add(drug)

    # Filter diseases with enough approved drugs
    qualified = [
        {"disease": disease, "gold_drugs": drugs}
        for disease, drugs in disease_drugs.items()
        if len(drugs) >= MIN_APPROVED_DRUGS
    ]

    # Deterministic shuffle then cap
    rng = random.Random(seed)
    rng.shuffle(qualified)
    cap = MAX_DISEASES
    if max_samples > 0:
        cap = min(cap, max_samples)
    return qualified[:cap]


def run(
    key_file: str | None = None,
    max_samples: int = 0,
    mode: str = "direct",
    maskself: bool = False,
    log_dir: str | None = None,
) -> dict:
    from new_bench.bench_utils import run_ranking_bench

    return run_ranking_bench(
        dataset_name="repodb",
        system_prompt=SYSTEM_PROMPT,
        queries=load_data(max_samples),
        format_prompt=lambda q: USER_TEMPLATE.format(disease=q["disease"]),
        k_recall=[10, 50],
        k_ndcg=20,
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
    )
