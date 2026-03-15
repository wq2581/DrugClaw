---
name: stitch-query
description: >
  Query or inspect the 45_STITCH — Search Tool for Interactions of Chemicals resource for drug-centric tasks with emphasis on drug-target interaction (dti) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# 45_STITCH — Search Tool for Interactions of Chemicals

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `45_STITCH.py`
- Category: `Drug-centric`
- Type: `KG`
- Subcategory: `Drug-Target Interaction (DTI)`

## API Surface

| Function | Purpose |
|---|---|
| `resolve()` | See `45_STITCH.py` for exact input/output behavior. |
| `resolve_batch()` | See `45_STITCH.py` for exact input/output behavior. |
| `get_interactors()` | See `45_STITCH.py` for exact input/output behavior. |
| `get_actions()` | See `45_STITCH.py` for exact input/output behavior. |
| `get_interactions()` | See `45_STITCH.py` for exact input/output behavior. |
| `search()` | See `45_STITCH.py` for exact input/output behavior. |
| `search_batch()` | See `45_STITCH.py` for exact input/output behavior. |
| `summarize()` | See `45_STITCH.py` for exact input/output behavior. |

## Usage

Read `45_STITCH.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_45_stitch.py`
- Run: `python tools/test_skill_45_stitch.py`
- Runtime import: `from skills.dti.stitch import STITCHSkill`

## Notes

- Review `if __name__ == "__main__"` in `45_STITCH.py` first when generating runnable query code.
- Primary link from the example: <http://stitch.embl.de/>
- Reference paper from the example: <https://doi.org/10.1093/nar/gkv1277>
- The validation script currently checks:
- import STITCHSkill
- instantiate STITCHSkill(timeout=20)
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <http://stitch.embl.de/>
- <https://doi.org/10.1093/nar/gkv1277>
- <http://stitch.embl.de/api/>
- <http://stitch.embl.de/api>
- <https://string-db.org/api>
