---
name: dtc-query
description: >
  Query or inspect the DTC - Drug Target Commons 2.0 resource for drug-centric tasks with emphasis on drug-target interaction (dti) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DTC - Drug Target Commons 2.0

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `63_DTC.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug-Target Interaction (DTI)`

## API Surface

| Function | Purpose |
|---|---|
| `download_dtc()` | See `63_DTC.py` for exact input/output behavior. |
| `preview_dtc()` | See `63_DTC.py` for exact input/output behavior. |
| `filter_by_gene()` | See `63_DTC.py` for exact input/output behavior. |

## Usage

Read `63_DTC.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_63_dtc.py`
- Run: `python tools/test_skill_63_dtc.py`
- Runtime import: `from skills.dti.dtc import DTCSkill`

## Notes

- Review `if __name__ == "__main__"` in `63_DTC.py` first when generating runnable query code.
- Primary link from the example: <https://drugtargetcommons.fimm.fi/static/Excell_files/DTC_data.csv>
- Reference paper from the example: <https://academic.oup.com/database/article/doi/10.1093/database/bay083/5096727>
- The validation script currently checks:
- read dtc_skill.py
- read README.md
- read skillexamples/63_DTC.py
- import DTCSkill
- attempt real DTC download through example path
- instantiate DTCSkill with downloaded csv_path if available
- call is_available()
- standard query 1: drug=imatinib

## Data Source

- <https://drugtargetcommons.fimm.fi/static/Excell_files/DTC_data.csv>
- <https://academic.oup.com/database/article/doi/10.1093/database/bay083/5096727>
