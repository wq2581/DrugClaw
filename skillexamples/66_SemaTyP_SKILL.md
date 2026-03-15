---
name: sematyp-query
description: >
  Query or inspect the SemaTyP - Drug-Disease Association Knowledge Graph resource for drug-centric tasks with emphasis on drug–disease associations Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# SemaTyP - Drug-Disease Association Knowledge Graph

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `66_SemaTyP.py`
- Category: `Drug-centric`
- Type: `KG`
- Subcategory: `Drug–Disease Associations`

## API Surface

| Function | Purpose |
|---|---|
| `download_sematyp()` | See `66_SemaTyP.py` for exact input/output behavior. |
| `explore_dataset()` | See `66_SemaTyP.py` for exact input/output behavior. |
| `preview_triples()` | See `66_SemaTyP.py` for exact input/output behavior. |

## Usage

Read `66_SemaTyP.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skills_66_68.py`
- Run: `python tools/test_skills_66_68.py`

## Notes

- Review `if __name__ == "__main__"` in `66_SemaTyP.py` first when generating runnable query code.
- Primary link from the example: <https://github.com/ShengtianSang/SemaTyP>
- Reference paper from the example: <https://link.springer.com/article/10.1186/s12859-018-2167-5>
- The validation script currently checks:
- import SemaTyPSkill
- instantiate with real local file config if available
- call is_available()
- call retrieve(...) with README-style drug input
- validate evidence_text and metadata

## Data Source

- <https://github.com/ShengtianSang/SemaTyP>
- <https://link.springer.com/article/10.1186/s12859-018-2167-5>
