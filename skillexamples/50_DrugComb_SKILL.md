---
name: drugcomb-query
description: >
  Query or inspect the DrugComb - Drug Combination Response Data for Cancer resource for drug-centric tasks with emphasis on drug combination/synergy Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DrugComb - Drug Combination Response Data for Cancer

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `50_DrugComb.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Combination/Synergy`

## API Surface

| Function | Purpose |
|---|---|
| `download_drugcomb()` | See `50_DrugComb.py` for exact input/output behavior. |
| `list_zenodo_files()` | See `50_DrugComb.py` for exact input/output behavior. |
| `preview_drugcomb()` | See `50_DrugComb.py` for exact input/output behavior. |

## Usage

Read `50_DrugComb.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_50_drugcomb.py`
- Run: `python tools/test_skill_50_drugcomb.py`
- Runtime import: `from skills.drug_combination.drugcomb.drugcomb_skill import DrugCombSkill`

## Notes

- Review `if __name__ == "__main__"` in `50_DrugComb.py` first when generating runnable query code.
- Primary link from the example: <https://zenodo.org/records/11102665>
- Reference paper from the example: <https://academic.oup.com/nar/article/47/W1/W43/5486743>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://zenodo.org/records/11102665>
- <https://academic.oup.com/nar/article/47/W1/W43/5486743>
