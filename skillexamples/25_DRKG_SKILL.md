---
name: drkg-query
description: >
  Query or inspect the DRKG - Drug Repurposing Knowledge Graph resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DRKG - Drug Repurposing Knowledge Graph

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `25_DRKG.py`
- Category: `Drug-centric`
- Type: `KG`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `download_drkg_repo()` | See `25_DRKG.py` for exact input/output behavior. |
| `download_drkg_data()` | See `25_DRKG.py` for exact input/output behavior. |
| `preview_drkg_edges()` | See `25_DRKG.py` for exact input/output behavior. |

## Usage

Read `25_DRKG.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_25_drkg.py`
- Run: `python tools/test_skill_25_drkg.py`
- Runtime import: `from skills.drug_repurposing.drkg import DRKGSkill`

## Notes

- Review `if __name__ == "__main__"` in `25_DRKG.py` first when generating runnable query code.
- Primary link from the example: <https://github.com/gnn4dr/DRKG>
- The validation script currently checks:
- import DRKGSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://github.com/gnn4dr/DRKG>
