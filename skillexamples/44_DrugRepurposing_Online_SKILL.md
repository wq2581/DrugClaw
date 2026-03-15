---
name: drugrepurposing-online-query
description: >
  Query or inspect the DrugRepurposing Online - Drug Repurposing Resource Aggregation resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DrugRepurposing Online - Drug Repurposing Resource Aggregation

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `44_DrugRepurposing_Online.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `get_homepage()` | See `44_DrugRepurposing_Online.py` for exact input/output behavior. |
| `search_drug()` | See `44_DrugRepurposing_Online.py` for exact input/output behavior. |

## Usage

Read `44_DrugRepurposing_Online.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_44_drugrepurposing_online.py`
- Run: `python tools/test_skill_44_drugrepurposing_online.py`
- Runtime import: `from skills.drug_repurposing.drugrepurposing_online import DrugRepurposingOnlineSkill`

## Notes

- Review `if __name__ == "__main__"` in `44_DrugRepurposing_Online.py` first when generating runnable query code.
- Primary link from the example: <https://drugrepurposing.info/>
- The validation script currently checks:
- import DrugRepurposingOnlineSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://drugrepurposing.info/>
