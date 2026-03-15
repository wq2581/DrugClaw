---
name: phee-query
description: >
  Query or inspect the PHEE - Pharmacovigilance Event Extraction Dataset resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# PHEE - Pharmacovigilance Event Extraction Dataset

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `38_PHEE.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `download_phee()` | See `38_PHEE.py` for exact input/output behavior. |
| `load_phee_json()` | See `38_PHEE.py` for exact input/output behavior. |

## Usage

Read `38_PHEE.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_38_phee.py`
- Run: `python tools/test_skill_38_phee.py`
- Runtime import: `from skills.drug_nlp.phee import PHEESkill`

## Notes

- Review `if __name__ == "__main__"` in `38_PHEE.py` first when generating runnable query code.
- Primary link from the example: <https://zenodo.org/records/7689970>
- Reference paper from the example: <https://arxiv.org/abs/2210.12560>
- The validation script currently checks:
- import PHEESkill
- call is_available()
- standard query: drug=aspirin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://zenodo.org/records/7689970>
- <https://arxiv.org/abs/2210.12560>
