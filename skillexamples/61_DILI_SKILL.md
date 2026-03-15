---
name: dili-query
description: >
  Query or inspect the DILI - Drug-Induced Liver Injury Dataset from ChEMBL resource for drug-centric tasks with emphasis on drug toxicity Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DILI - Drug-Induced Liver Injury Dataset from ChEMBL

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `61_DILI.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug Toxicity`

## API Surface

| Function | Purpose |
|---|---|
| `get_dili_compounds_from_chembl()` | See `61_DILI.py` for exact input/output behavior. |
| `get_hepatotoxicity_assays()` | See `61_DILI.py` for exact input/output behavior. |
| `download_supplement_data()` | See `61_DILI.py` for exact input/output behavior. |

## Usage

Read `61_DILI.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_61_dili.py`
- Run: `python tools/test_skill_61_dili.py`
- Runtime import: `from skills.drug_toxicity.dili import DILISkill`

## Notes

- Review `if __name__ == "__main__"` in `61_DILI.py` first when generating runnable query code.
- Primary link from the example: <https://doi.org/10.1021/acs.chemrestox.0c00296>
- Reference paper from the example: <https://doi.org/10.1021/acs.chemrestox.0c00296>
- The validation script currently checks:
- read dili_skill.py
- read README.md
- read skillexamples/61_DILI.py
- import DILISkill
- instantiate DILISkill(timeout=20)
- call is_available()
- standard query 1: drug=imatinib
- standard query 2: drug=acetaminophen

## Data Source

- <https://doi.org/10.1021/acs.chemrestox.0c00296>
