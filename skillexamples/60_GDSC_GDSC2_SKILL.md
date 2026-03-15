---
name: gdsc-gdsc2-query
description: >
  Query or inspect the GDSC/GDSC2 - Genomics of Drug Sensitivity in Cancer resource for drug-centric tasks with emphasis on drug molecular property Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# GDSC/GDSC2 - Genomics of Drug Sensitivity in Cancer

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `60_GDSC_GDSC2.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug Molecular Property`

## API Surface

| Function | Purpose |
|---|---|
| `download_gdsc_drug_list()` | See `60_GDSC_GDSC2.py` for exact input/output behavior. |
| `download_gdsc2_data()` | See `60_GDSC_GDSC2.py` for exact input/output behavior. |
| `preview_drug_list()` | See `60_GDSC_GDSC2.py` for exact input/output behavior. |

## Usage

Read `60_GDSC_GDSC2.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_60_gdsc.py`
- Run: `python tools/test_skill_60_gdsc.py`
- Runtime import: `from skills.drug_molecular_property.gdsc import GDSCSkill`

## Notes

- Review `if __name__ == "__main__"` in `60_GDSC_GDSC2.py` first when generating runnable query code.
- Primary link from the example: <https://www.cancerrxgene.org/>
- Reference paper from the example: <https://academic.oup.com/nar/article/41/D1/D955/1059448>
- The validation script currently checks:
- read gdsc_skill.py
- read README.md
- read skillexamples/60_GDSC_GDSC2.py
- import GDSCSkill
- download official screened_compounds_rel_8.4.csv
- instantiate GDSCSkill with real csv_path
- call is_available()
- standard query 1: drug=Erlotinib

## Data Source

- <https://www.cancerrxgene.org/>
- <https://academic.oup.com/nar/article/41/D1/D955/1059448>
