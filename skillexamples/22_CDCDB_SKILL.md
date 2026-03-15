---
name: cdcdb-query
description: >
  Query or inspect the CDCDB - Cancer Drug Combination Database resource for drug-centric tasks with emphasis on drug combination/synergy Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# CDCDB - Cancer Drug Combination Database

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `22_CDCDB.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Combination/Synergy`

## API Surface

| Function | Purpose |
|---|---|
| `download_cdcdb()` | See `22_CDCDB.py` for exact input/output behavior. |
| `preview_cdcdb()` | See `22_CDCDB.py` for exact input/output behavior. |

## Usage

Read `22_CDCDB.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_22_cdcdb.py`
- Run: `python tools/test_skill_22_cdcdb.py`
- Runtime import: `from skills.drug_combination.cdcdb import CDCDBSkill`

## Notes

- Review `if __name__ == "__main__"` in `22_CDCDB.py` first when generating runnable query code.
- Primary link from the example: <https://icc.ise.bgu.ac.il/medical_ai/CDCDB/>
- Reference paper from the example: <https://www.nature.com/articles/s41597-022-01360-z>
- The validation script currently checks:
- import CDCDBSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://icc.ise.bgu.ac.il/medical_ai/CDCDB/>
- <https://www.nature.com/articles/s41597-022-01360-z>
