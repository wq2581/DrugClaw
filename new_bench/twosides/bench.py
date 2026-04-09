"""
Drug-pair ADR — TWOSIDES.

Task  : Given a drug pair and an adverse event, predict whether the combination
        causes that event (yes / no).
Data  : new_bench_data/2sides/twosides_benchmark.json
        JSON array [{drug_1, drug_2, condition, label (0/1), PRR, query}, ...]
        label 1 = positive (pair causes AE), 0 = negative.
        Dataset is balanced: 500 positives + 500 negatives.
Prompt: "Does the combination of {drug_A} and {drug_B} cause {adverse_event}?"
Metric: Precision, Recall, F1, AUROC
        (AUROC computed as balanced accuracy from binary hard predictions)
"""

import json
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "new_bench_data/2sides/twosides_benchmark.json"
)

LABELS = ["yes", "no"]

SYSTEM_PROMPT = """\
You are a pharmacovigilance expert.

Task: Determine whether the combination of two drugs causes the specified
      adverse event based on known pharmacological interactions and safety data.

Respond with ONLY a JSON object: {"answer": "<label>"}
where <label> is one of: yes, no
"""

USER_TEMPLATE = """\
Drug A: {drug_1}
Drug B: {drug_2}
Adverse Event: {condition}

Does the combination of {drug_1} and {drug_2} cause {condition}?
Respond with JSON: {{"answer": "yes"}} or {{"answer": "no"}}
"""


def load_data(max_samples: int = 0) -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for r in raw:
        label_int = int(r["label"])
        gold = "yes" if label_int == 1 else "no"
        rows.append({
            "drug_1":    r["drug_1"],
            "drug_2":    r["drug_2"],
            "condition": r["condition"],
            "gold":      gold,
            "_label":    label_int,
        })

    if max_samples > 0:
        rows = rows[:max_samples]
    return rows


def run(
    key_file: str | None = None,
    max_samples: int = 0,
    mode: str = "direct",
    maskself: bool = False,
    log_dir: str | None = None,
) -> dict:
    from new_bench.bench_utils import run_binary_bench

    return run_binary_bench(
        dataset_name="twosides",
        pos_label="yes",
        neg_label="no",
        default_label="no",
        system_prompt=SYSTEM_PROMPT,
        samples=load_data(max_samples),
        format_prompt=lambda s: USER_TEMPLATE.format(
            drug_1=s["drug_1"],
            drug_2=s["drug_2"],
            condition=s["condition"],
        ),
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
    )
