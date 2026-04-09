"""
Clinical MCQ — MedQA drug-focused test set.

Task  : Multiple-choice medical question; select the single best answer letter.
Labels: A, B, C, D, E
Data  : new_bench_data/medqa/medqa_drug_test.json
        JSON array [{meta_info, question, answer_idx, answer, options}, ...]
        options: [{"key": "A", "value": "..."}, ...]
Metric: Accuracy (exact letter match)
"""

import json
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "new_bench_data/medqa/medqa_drug_test.json"
)

LABELS = ["A", "B", "C", "D", "E"]

SYSTEM_PROMPT = """\
You are a medical exam expert.

Task: Read the clinical question and all answer choices, then select the single
      best answer letter.

Respond with ONLY a JSON object: {"answer": "<letter>"}
where <letter> is one of: A, B, C, D, E
"""

USER_TEMPLATE = """\
Question: {question}

Options:
{options}

Select the best answer (A/B/C/D/E):
"""


def _format_options(options: list[dict]) -> str:
    return "\n".join(f"  {o['key']}. {o['value']}" for o in options)


def load_data(max_samples: int = 0) -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for r in raw:
        gold = str(r.get("answer_idx", "")).strip().upper()
        if gold not in LABELS:
            continue
        rows.append({
            "question": r["question"],
            "options": r["options"],
            "gold": gold,
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
    from new_bench.bench_utils import run_bench, extract_mcq_answer

    samples = load_data(max_samples)
    valid_keys = sorted({s["gold"] for s in samples} | set(LABELS))

    return run_bench(
        dataset_name="medqa",
        labels=LABELS,
        default_label="A",
        system_prompt=SYSTEM_PROMPT,
        samples=samples,
        format_prompt=lambda s: USER_TEMPLATE.format(
            question=s["question"],
            options=_format_options(s["options"]),
        ),
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
        answer_extractor=lambda text: extract_mcq_answer(text, valid_keys),
    )
