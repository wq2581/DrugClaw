---
name: chebi-query
description: >
  Query or inspect the 64_ChEBI.py – ChEBI (Chemical Entities of Biological Interest) query skill. resource for drug ontology/terminology tasks with emphasis on drug ontology/terminology Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# 64_ChEBI.py – ChEBI (Chemical Entities of Biological Interest) query skill.

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `64_ChEBI.py`
- Category: `Drug Ontology/Terminology`
- Type: `KG`
- Subcategory: `Drug Ontology/Terminology`

## API Surface

| Function | Purpose |
|---|---|
| `search_chebi()` | See `64_ChEBI.py` for exact input/output behavior. |
| `get_entity()` | See `64_ChEBI.py` for exact input/output behavior. |
| `get_entities_batch()` | See `64_ChEBI.py` for exact input/output behavior. |
| `search()` | See `64_ChEBI.py` for exact input/output behavior. |
| `search_batch()` | See `64_ChEBI.py` for exact input/output behavior. |
| `summarize()` | See `64_ChEBI.py` for exact input/output behavior. |
| `to_json()` | See `64_ChEBI.py` for exact input/output behavior. |

## Usage

Read `64_ChEBI.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_64_chebi.py`
- Run: `python tools/test_skill_64_chebi.py`
- Runtime import: `from skills.drug_ontology.chebi import ChEBISkill`

## Notes

- Review `if __name__ == "__main__"` in `64_ChEBI.py` first when generating runnable query code.
- The validation script currently checks:
- read chebi_skill.py
- read README.md
- read SKILL.md
- read example.py
- import ChEBISkill
- instantiate ChEBISkill(timeout=20)
- call is_available()
- standard query 1: drug=aspirin

## Data Source

- <https://www.ebi.ac.uk/chebi/>
- <https://academic.oup.com/nar/article/54/D1/D1768/8349173>
- <https://www.ebi.ac.uk/chebi/backend/api/docs/>
