---
name: adrecs-query
description: >
  Query or inspect the ADReCS - Adverse Drug Reaction Classification System resource for drug-centric tasks with emphasis on adverse drug reaction (adr) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# ADReCS - Adverse Drug Reaction Classification System

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `62_ADReCS.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Adverse Drug Reaction (ADR)`

## API Surface

| Function | Purpose |
|---|---|
| `download_adrecs()` | See `62_ADReCS.py` for exact input/output behavior. |
| `describe_adrecs()` | See `62_ADReCS.py` for exact input/output behavior. |

## Usage

Read `62_ADReCS.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_62_adrecs.py`
- Run: `python tools/test_skill_62_adrecs.py`
- Runtime import: `from skills.adr.adrecs import ADReCSSkill`

## Notes

- Review `if __name__ == "__main__"` in `62_ADReCS.py` first when generating runnable query code.
- Primary link from the example: <http://bioinf.xmu.edu.cn/ADReCS>
- Reference paper from the example: <https://academic.oup.com/nar/article/43/D1/D907/2437234>
- The validation script currently checks:
- read adrecs_skill.py
- read README.md
- read skillexamples/62_ADReCS.py
- import ADReCSSkill
- instantiate ADReCSSkill(timeout=20)
- call is_available()
- standard query 1: drug=aspirin
- standard query 2: drug=imatinib

## Data Source

- <http://bioinf.xmu.edu.cn/ADReCS>
- <https://academic.oup.com/nar/article/43/D1/D907/2437234>
