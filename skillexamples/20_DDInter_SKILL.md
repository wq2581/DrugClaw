---
name: ddinter-query
description: >
  Query or inspect the DDInter - Drug-Drug Interaction Database (Local CSV) resource for drug-centric tasks with emphasis on drug-drug interaction (ddi) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DDInter - Drug-Drug Interaction Database (Local CSV)

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `20_DDInter.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug-Drug Interaction (DDI)`

## API Surface

| Function | Purpose |
|---|---|
| `search()` | See `20_DDInter.py` for exact input/output behavior. |
| `search_batch()` | See `20_DDInter.py` for exact input/output behavior. |
| `summarize()` | See `20_DDInter.py` for exact input/output behavior. |
| `to_json()` | See `20_DDInter.py` for exact input/output behavior. |
| `list_drugs()` | See `20_DDInter.py` for exact input/output behavior. |
| `get_interactions_between()` | See `20_DDInter.py` for exact input/output behavior. |

## Usage

Read `20_DDInter.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_20_ddinter.py`
- Run: `python tools/test_skill_20_ddinter.py`
- Runtime import: `from skills.ddi.ddinter import DDInterSkill`

## Notes

- Review `if __name__ == "__main__"` in `20_DDInter.py` first when generating runnable query code.
- Primary link from the example: <https://ddinter2.scbdd.com/server/search/>
- Reference paper from the example: <https://academic.oup.com/nar/article/53/D1/D1356/7740584>
- The validation script currently checks:
- import DDInterSkill
- instantiate DDInterSkill(timeout=20)
- call is_available()
- standard query: drug=aspirin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://ddinter2.scbdd.com/server/search/>
- <https://academic.oup.com/nar/article/53/D1/D1356/7740584>
