---
name: gdkd-query
description: >
  Query or inspect the GDKD - Genomics-Drug Knowledge Database resource for drug-centric tasks with emphasis on drug-target interaction (dti) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# GDKD - Genomics-Drug Knowledge Database

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `54_GDKD.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug-Target Interaction (DTI)`

## API Surface

| Function | Purpose |
|---|---|
| `download_via_synapseclient()` | See `54_GDKD.py` for exact input/output behavior. |
| `download_ccle_data_alternative()` | See `54_GDKD.py` for exact input/output behavior. |
| `describe_gdkd()` | See `54_GDKD.py` for exact input/output behavior. |

## Usage

Read `54_GDKD.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_54_gdkd.py`
- Run: `python tools/test_skill_54_gdkd.py`
- Runtime import: `from skills.dti.gdkd.gdkd_skill import GDKDSkill`

## Notes

- Review `if __name__ == "__main__"` in `54_GDKD.py` first when generating runnable query code.
- Primary link from the example: <https://www.synapse.org/#!Synapse:syn2370773>
- Reference paper from the example: <https://doi.org/10.1038/nature11003>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://www.synapse.org/#!Synapse:syn2370773>
- <https://doi.org/10.1038/nature11003>
- <https://www.synapse.org/>
