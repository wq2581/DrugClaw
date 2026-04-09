"""
Drug-Drug Interaction — DDInter.

Task A (binary)  : Is there a harmful interaction between Drug_A and Drug_B?
                   Labels: yes, no  (label > 0 = Major or Moderate = yes)
Task B (severity): What is the severity of interaction? Major / Moderate / Minor
                   Labels: Major, Moderate, Minor  (all 1500 samples)

Data  : new_bench_data/DDInter/ddinter_benchmark.json
        JSON array [{drug_1, drug_2, label (0/1/2), severity, query}, ...]
        label 0 = Minor, 1 = Moderate, 2 = Major
        Balanced: 500 each.

Metrics: AUROC, F1 (binary); Accuracy, macro-F1 (severity)
         Bonus: severity classification (Major/Moderate/Minor)

The run() function runs severity classification by default and also computes
the binary DDI metric using label > 0 as "yes".
"""

import json
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "new_bench_data/DDInter/ddinter_benchmark.json"
)

# Severity labels (3-class)
SEVERITY_LABELS = ["Major", "Moderate", "Minor"]

# Binary DDI labels
BINARY_LABELS = ["yes", "no"]

# Map raw severity string to binary
_BINARY_MAP = {
    "Major":    "yes",
    "Moderate": "yes",
    "Minor":    "no",
}

SYSTEM_PROMPT_SEVERITY = """\
You are a clinical pharmacology expert.

Task: Assess the severity of the drug-drug interaction between the two drugs.

Severity levels:
- Major    : Can be life-threatening or cause permanent damage.
- Moderate : May require dose adjustment or close monitoring.
- Minor    : Mild effect; usually does not require treatment modification.

Respond with ONLY a JSON object: {"answer": "<severity>"}
where <severity> is one of: Major, Moderate, Minor
"""

SYSTEM_PROMPT_BINARY = """\
You are a clinical pharmacology expert.

Task: Determine whether there is a clinically significant (harmful) drug-drug
      interaction between the two drugs.

Respond with ONLY a JSON object: {"answer": "<label>"}
where <label> is one of: yes, no
"""

USER_TEMPLATE_SEVERITY = """\
Drug A: {drug_1}
Drug B: {drug_2}

What is the severity of interaction between {drug_1} and {drug_2}?
Answer: Major, Moderate, or Minor.
Respond with JSON: {{"answer": "Major"}} / {{"answer": "Moderate"}} / {{"answer": "Minor"}}
"""

USER_TEMPLATE_BINARY = """\
Drug A: {drug_1}
Drug B: {drug_2}

Is there a harmful interaction between {drug_1} and {drug_2}?
Respond with JSON: {{"answer": "yes"}} or {{"answer": "no"}}
"""


def load_data(max_samples: int = 0) -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for r in raw:
        severity = r["severity"].strip()     # "Major" / "Moderate" / "Minor"
        binary   = _BINARY_MAP.get(severity, "no")
        rows.append({
            "drug_1":   r["drug_1"],
            "drug_2":   r["drug_2"],
            "severity": severity,
            "binary":   binary,
            "gold":     severity,            # default gold = severity
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
    task: str = "severity",
) -> dict:
    """
    task="severity" (default) — 3-class Major/Moderate/Minor classification.
    task="binary"             — binary yes/no harmful interaction + AUROC.
    task="both"               — run both and return combined result dict.
    """
    from new_bench.bench_utils import run_bench, run_binary_bench

    samples = load_data(max_samples)

    if task == "binary":
        binary_samples = [{**s, "gold": s["binary"]} for s in samples]
        return run_binary_bench(
            dataset_name="ddinter_binary",
            pos_label="yes",
            neg_label="no",
            default_label="no",
            system_prompt=SYSTEM_PROMPT_BINARY,
            samples=binary_samples,
            format_prompt=lambda s: USER_TEMPLATE_BINARY.format(
                drug_1=s["drug_1"], drug_2=s["drug_2"],
            ),
            mode=mode,
            maskself=maskself,
            key_file=key_file,
            log_dir=log_dir,
        )

    if task == "both":
        sev_result = run(
            key_file=key_file, max_samples=max_samples, mode=mode,
            maskself=maskself, log_dir=log_dir, task="severity",
        )
        bin_result = run(
            key_file=key_file, max_samples=max_samples, mode=mode,
            maskself=maskself, log_dir=log_dir, task="binary",
        )
        return {"severity": sev_result, "binary": bin_result}

    # Default: severity
    return run_bench(
        dataset_name="ddinter_severity",
        labels=SEVERITY_LABELS,
        default_label="Moderate",
        system_prompt=SYSTEM_PROMPT_SEVERITY,
        samples=samples,
        format_prompt=lambda s: USER_TEMPLATE_SEVERITY.format(
            drug_1=s["drug_1"], drug_2=s["drug_2"],
        ),
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
    )
