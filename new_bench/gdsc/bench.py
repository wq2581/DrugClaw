"""
Drug Sensitivity — GDSC2.

Task  : Predict whether a cancer cell line is sensitive or resistant to a drug.
Labels: Sensitive, Resistant
Data  : new_bench_data/gdsc/gdsc2_benchmark.json
        JSON array [{drug, cell_line, cancer_type, target, pathway,
                     label (0=Resistant/1=Sensitive), label_name,
                     ln_ic50, threshold, query}, ...]
        Balanced: 500 Sensitive + 500 Resistant.
Prompt: "Is {cell_line} ({cancer_type}) sensitive or resistant to {drug}?"
Metric: Accuracy, F1 (macro), per-class precision/recall/F1
"""

import json
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "new_bench_data/gdsc/gdsc2_benchmark.json"
)

LABELS = ["Sensitive", "Resistant"]

SYSTEM_PROMPT = """\
You are an oncology pharmacogenomics expert.

Task: Based on known drug sensitivity profiles, predict whether the given
      cancer cell line is Sensitive or Resistant to the specified drug.

Consider:
- The drug's mechanism of action and known targets
- The cancer type and cell line characteristics
- Known genomic biomarkers of response

Respond with ONLY a JSON object: {"answer": "<label>"}
where <label> is one of: Sensitive, Resistant
"""

USER_TEMPLATE = """\
Drug: {drug}
  Target(s): {target}
  Pathway: {pathway}
Cell line: {cell_line}
  Cancer type: {cancer_type}

Is this cell line Sensitive or Resistant to {drug}?
Respond with JSON: {{"answer": "Sensitive"}} or {{"answer": "Resistant"}}
"""


def load_data(max_samples: int = 0) -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for r in raw:
        gold = r.get("label_name", "").strip()
        if gold not in LABELS:
            gold = "Sensitive" if int(r.get("label", 0)) == 1 else "Resistant"
        rows.append({
            "drug":        r["drug"],
            "cell_line":   r["cell_line"],
            "cancer_type": r.get("cancer_type", "Unknown"),
            "target":      r.get("target", "Unknown"),
            "pathway":     r.get("pathway", "Unknown"),
            "gold":        gold,
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
    from new_bench.bench_utils import run_bench

    return run_bench(
        dataset_name="gdsc",
        labels=LABELS,
        default_label="Resistant",
        system_prompt=SYSTEM_PROMPT,
        samples=load_data(max_samples),
        format_prompt=lambda s: USER_TEMPLATE.format(
            drug=s["drug"],
            target=s["target"],
            pathway=s["pathway"],
            cell_line=s["cell_line"],
            cancer_type=s["cancer_type"],
        ),
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
    )
