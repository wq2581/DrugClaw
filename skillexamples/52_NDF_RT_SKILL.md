---
name: ndf-rt-query
description: >
  Query or inspect the NDF-RT - National Drug File Reference Terminology resource for drug-centric tasks with emphasis on drug ontology/terminology Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# NDF-RT - National Drug File Reference Terminology

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `52_NDF_RT.py`
- Category: `Drug-centric`
- Type: `KG`
- Subcategory: `Drug Ontology/Terminology`

## API Surface

| Function | Purpose |
|---|---|
| `search_ndfrt()` | See `52_NDF_RT.py` for exact input/output behavior. |
| `get_concept()` | See `52_NDF_RT.py` for exact input/output behavior. |
| `get_concept_children()` | See `52_NDF_RT.py` for exact input/output behavior. |
| `get_all_roots()` | See `52_NDF_RT.py` for exact input/output behavior. |

## Usage

Read `52_NDF_RT.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_52_ndfrt.py`
- Run: `python tools/test_skill_52_ndfrt.py`
- Runtime import: `from skills.drug_ontology.ndfrt.ndfrt_skill import NDFRTSkill`

## Notes

- Review `if __name__ == "__main__"` in `52_NDF_RT.py` first when generating runnable query code.
- Primary link from the example: <https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ndfrt>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ndfrt>
- <https://api-evsrest.nci.nih.gov/api/v1>
