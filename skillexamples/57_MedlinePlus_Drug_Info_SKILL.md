---
name: medlineplus-drug-info-query
description: >
  Query or inspect the MedlinePlus Drug Info – Consumer-Oriented Drug Information Skill resource for drug-centric tasks with emphasis on drug labeling/info Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# MedlinePlus Drug Info – Consumer-Oriented Drug Information Skill

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `57_MedlinePlus_Drug_Info.py`
- Category: `Drug-centric`
- Type: `Public REST API`
- Subcategory: `Drug Labeling/Info`

## API Surface

| Function | Purpose |
|---|---|
| `search()` | See `57_MedlinePlus_Drug_Info.py` for exact input/output behavior. |
| `search_batch()` | See `57_MedlinePlus_Drug_Info.py` for exact input/output behavior. |
| `summarize()` | See `57_MedlinePlus_Drug_Info.py` for exact input/output behavior. |
| `to_json()` | See `57_MedlinePlus_Drug_Info.py` for exact input/output behavior. |

## Usage

Read `57_MedlinePlus_Drug_Info.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_57_medlineplus.py`
- Run: `python tools/test_skill_57_medlineplus.py`
- Runtime import: `from skills.drug_labeling.medlineplus.medlineplus_skill import MedlinePlusSkill`

## Notes

- Review `if __name__ == "__main__"` in `57_MedlinePlus_Drug_Info.py` first when generating runnable query code.
- Primary link from the example: <https://medlineplus.gov/druginformation.html>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://medlineplus.gov/druginformation.html>
- <https://wsearch.nlm.nih.gov/ws/query>
- <https://connect.medlineplus.gov/service>
