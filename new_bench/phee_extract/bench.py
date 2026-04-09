"""
Pharma Event Extraction — PHEE (pharmacovigilance).

Task  : Given a sentence, extract all (drug, adverse_event) pairs.
Data  : new_bench_data/phee/test.json  — JSONL, original PHEE annotation format
        Each line: {id, context, is_mult_event, annotations:[{events:[...]}]}
        Gold tuples come from Adverse_event entries:
          drug  ← Treatment.Drug.text[0][0]
          event ← Effect.text[0][0]
Prompt: "Extract all adverse events caused by {drug} from this text: {sentence}"
        (one prompt per sentence, listing all expected drug-event pairs)
Metric: Micro-F1, Precision, Recall on (drug, event) tuple sets
"""

import json
import re
from pathlib import Path

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "new_bench_data/phee/test.json"
)

SYSTEM_PROMPT = """\
You are a pharmacovigilance information extraction system.

Task: Extract all adverse drug events from the provided text.
For each adverse event, identify:
  - The drug (or treatment) that caused it
  - The adverse event / effect observed

Output each finding on a separate line in this exact format:
  Drug: <drug name>, Event: <adverse event description>

If no adverse events are described, output: NONE
"""

USER_TEMPLATE = """\
Text: {sentence}

Extract all adverse drug events (drug → effect) from the text above.
"""


def _load_jsonl(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def _extract_gold_tuples(record: dict) -> set[tuple[str, str]]:
    """
    Extract gold (drug, adverse_event) tuples from a PHEE annotation record.
    Only events with event_type == "Adverse_event" are included.
    """
    tuples: set[tuple[str, str]] = set()
    for ann in record.get("annotations", []):
        for ev in ann.get("events", []):
            event_type = ev.get("event_type", "").strip()
            if event_type.lower() != "adverse_event":
                continue

            # Drug
            drug_texts = (
                ev.get("Treatment", {})
                  .get("Drug", {})
                  .get("text", [[]])
            )
            drug = drug_texts[0][0] if drug_texts and drug_texts[0] else ""

            # Adverse effect
            effect_texts = ev.get("Effect", {}).get("text", [[]])
            effect = effect_texts[0][0] if effect_texts and effect_texts[0] else ""

            if drug and effect:
                tuples.add((drug.lower().strip(), effect.lower().strip()))
    return tuples


def load_data(max_samples: int = 0) -> list[dict]:
    raw = _load_jsonl(DATA_PATH)
    rows = []
    for r in raw:
        gold_tuples = _extract_gold_tuples(r)
        # Only include records with at least one adverse event
        if not gold_tuples:
            continue
        rows.append({
            "sentence": r.get("context", ""),
            "gold_tuples": gold_tuples,
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
    from new_bench.bench_utils import run_extraction_bench

    return run_extraction_bench(
        dataset_name="phee_extract",
        system_prompt=SYSTEM_PROMPT,
        samples=load_data(max_samples),
        format_prompt=lambda s: USER_TEMPLATE.format(sentence=s["sentence"]),
        mode=mode,
        maskself=maskself,
        key_file=key_file,
        log_dir=log_dir,
    )
