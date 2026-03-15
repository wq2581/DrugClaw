---
name: atc-ddd-query
description: >
  Query or inspect the ATC/DDD - WHO Anatomical Therapeutic Chemical Classification resource for drug-centric tasks with emphasis on drug ontology/terminology Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# ATC/DDD - WHO Anatomical Therapeutic Chemical Classification

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `27_ATC_DDD.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Ontology/Terminology`

## API Surface

| Function | Purpose |
|---|---|
| `get_atc_class_drugs()` | See `27_ATC_DDD.py` for exact input/output behavior. |
| `search_atc_by_drug()` | See `27_ATC_DDD.py` for exact input/output behavior. |
| `get_atc_hierarchy()` | See `27_ATC_DDD.py` for exact input/output behavior. |

## Usage

Read `27_ATC_DDD.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skills_20_29.py`
- Run: `python tools/test_skills_20_29.py`

## Notes

- Review `if __name__ == "__main__"` in `27_ATC_DDD.py` first when generating runnable query code.
- Primary link from the example: <https://atcddd.fhi.no/atc_ddd_index/>
- The validation script currently checks:
- call is_available()

## Data Source

- <https://atcddd.fhi.no/atc_ddd_index/>
