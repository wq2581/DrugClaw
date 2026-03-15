---
name: repurposedrugs-query
description: >
  Query or inspect the RepurposeDrugs - Drug Repurposing Opportunities Database resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# RepurposeDrugs - Drug Repurposing Opportunities Database

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `43_RepurposeDrugs.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `search_repurposed_drugs()` | See `43_RepurposeDrugs.py` for exact input/output behavior. |
| `download_dataset()` | See `43_RepurposeDrugs.py` for exact input/output behavior. |

## Usage

Read `43_RepurposeDrugs.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_43_repurposedrugs.py`
- Run: `python tools/test_skill_43_repurposedrugs.py`
- Runtime import: `from skills.drug_repurposing.repurposedrugs import RepurposeDrugsSkill`

## Notes

- Review `if __name__ == "__main__"` in `43_RepurposeDrugs.py` first when generating runnable query code.
- Primary link from the example: <https://repurposedrugs.org/>
- Reference paper from the example: <https://academic.oup.com/bib/article/25/4/bbae328/7709763>
- The validation script currently checks:
- import RepurposeDrugsSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://repurposedrugs.org/>
- <https://academic.oup.com/bib/article/25/4/bbae328/7709763>
