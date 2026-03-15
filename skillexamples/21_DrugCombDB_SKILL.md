---
name: drugcombdb-query
description: >
  Query or inspect the DrugCombDB - Drug Combination Synergy Data resource for drug-centric tasks with emphasis on drug combination/synergy Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DrugCombDB - Drug Combination Synergy Data

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `21_DrugCombDB.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Combination/Synergy`

## API Surface

| Function | Purpose |
|---|---|
| `download_drugcombdb()` | See `21_DrugCombDB.py` for exact input/output behavior. |
| `preview_data()` | See `21_DrugCombDB.py` for exact input/output behavior. |

## Usage

Read `21_DrugCombDB.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_21_drugcombdb.py`
- Run: `python tools/test_skill_21_drugcombdb.py`
- Runtime import: `from skills.drug_combination.drugcombdb import DrugCombDBSkill`

## Notes

- Review `if __name__ == "__main__"` in `21_DrugCombDB.py` first when generating runnable query code.
- Primary link from the example: <http://drugcombdb.denglab.org/>
- Reference paper from the example: <https://academic.oup.com/nar/article/48/D1/D871/5609522>
- The validation script currently checks:
- import DrugCombDBSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <http://drugcombdb.denglab.org/>
- <https://academic.oup.com/nar/article/48/D1/D871/5609522>
