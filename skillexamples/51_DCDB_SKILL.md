---
name: dcdb-query
description: >
  Query or inspect the DCDB - Drug Combination Database resource for drug-centric tasks with emphasis on drug combination/synergy Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DCDB - Drug Combination Database

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `51_DCDB.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Combination/Synergy`

## API Surface

| Function | Purpose |
|---|---|
| `download_dcdb_data()` | See `51_DCDB.py` for exact input/output behavior. |
| `describe_dcdb()` | See `51_DCDB.py` for exact input/output behavior. |

## Usage

Read `51_DCDB.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_51_dcdb.py`
- Run: `python tools/test_skill_51_dcdb.py`
- Runtime import: `from skills.drug_combination.dcdb.dcdb_skill import DCDBSkill`

## Notes

- Review `if __name__ == "__main__"` in `51_DCDB.py` first when generating runnable query code.
- Primary link from the example: <http://www.cls.zju.edu.cn/dcdb/>
- Reference paper from the example: <https://academic.oup.com/database/article/doi/10.1093/database/bau124/2635579>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <http://www.cls.zju.edu.cn/dcdb/>
- <https://academic.oup.com/database/article/doi/10.1093/database/bau124/2635579>
