---
name: rxlist-query
description: >
  Query or inspect the RxList Drug Descriptions - Detailed Drug Monographs for Clinicians resource for drug-centric tasks with emphasis on drug labeling/info Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# RxList Drug Descriptions - Detailed Drug Monographs for Clinicians

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `56_RxList.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Labeling/Info`

## API Surface

| Function | Purpose |
|---|---|
| `get_drug_page()` | See `56_RxList.py` for exact input/output behavior. |
| `extract_drug_description()` | See `56_RxList.py` for exact input/output behavior. |

## Usage

Read `56_RxList.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_56_rxlist.py`
- Run: `python tools/test_skill_56_rxlist.py`
- Runtime import: `from skills.drug_labeling.rxlist.rxlist_skill import RxListSkill`

## Notes

- Review `if __name__ == "__main__"` in `56_RxList.py` first when generating runnable query code.
- Primary link from the example: <https://www.rxlist.com/>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://www.rxlist.com/>
