---
name: tarkg-query
description: >
  Query or inspect the TarKG - Drug Target Discovery Knowledge Graph resource for drug-centric tasks with emphasis on drug-target interaction (dti) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# TarKG - Drug Target Discovery Knowledge Graph

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `41_TarKG.py`
- Category: `Drug-centric`
- Type: `KG`
- Subcategory: `Drug-Target Interaction (DTI)`

## API Surface

| Function | Purpose |
|---|---|
| `download_tarkg()` | See `41_TarKG.py` for exact input/output behavior. |
| `describe_tarkg()` | See `41_TarKG.py` for exact input/output behavior. |

## Usage

Read `41_TarKG.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_41_tarkg.py`
- Run: `python tools/test_skill_41_tarkg.py`
- Runtime import: `from skills.dti.tarkg import TarKGSkill`

## Notes

- Review `if __name__ == "__main__"` in `41_TarKG.py` first when generating runnable query code.
- Primary link from the example: <https://tarkg.ddtmlab.org/index>
- Reference paper from the example: <https://academic.oup.com/bioinformatics/article/40/10/btae598/7818343>
- The validation script currently checks:
- import TarKGSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://tarkg.ddtmlab.org/index>
- <https://academic.oup.com/bioinformatics/article/40/10/btae598/7818343>
