---
name: unitox-query
description: >
  Query or inspect the UniTox - Unified Multi-Organ Drug Toxicity Annotation resource for drug-centric tasks with emphasis on drug toxicity Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# UniTox - Unified Multi-Organ Drug Toxicity Annotation

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `28_UniTox.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug Toxicity`

## API Surface

| Function | Purpose |
|---|---|
| `download_unitox()` | See `28_UniTox.py` for exact input/output behavior. |
| `preview_unitox()` | See `28_UniTox.py` for exact input/output behavior. |

## Usage

Read `28_UniTox.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_28_unitox.py`
- Run: `python tools/test_skill_28_unitox.py`
- Runtime import: `from skills.drug_toxicity.unitox import UniToxSkill`

## Notes

- Review `if __name__ == "__main__"` in `28_UniTox.py` first when generating runnable query code.
- Primary link from the example: <https://zenodo.org/records/11627822>
- Reference paper from the example: <https://doi.org/10.1101/2024.06.21.24309315>
- The validation script currently checks:
- import UniToxSkill
- call is_available()
- standard query: drug=acetaminophen
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://zenodo.org/records/11627822>
- <https://doi.org/10.1101/2024.06.21.24309315>
