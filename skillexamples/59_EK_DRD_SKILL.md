---
name: ek-drd-query
description: >
  Query or inspect the EK-DRD - Enhanced Knowledgebase of Drug Resistance Data resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# EK-DRD - Enhanced Knowledgebase of Drug Resistance Data

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `59_EK_DRD.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `check_website()` | See `59_EK_DRD.py` for exact input/output behavior. |
| `download_ekdrd()` | See `59_EK_DRD.py` for exact input/output behavior. |
| `describe_ekdrd()` | See `59_EK_DRD.py` for exact input/output behavior. |

## Usage

Read `59_EK_DRD.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_59_ek_drd.py`
- Run: `python tools/test_skill_59_ek_drd.py`
- Runtime import: `from skills.drug_repurposing.ek_drd.ek_drd_skill import EKDRDSkill`

## Notes

- Review `if __name__ == "__main__"` in `59_EK_DRD.py` first when generating runnable query code.
- Primary link from the example: <http://www.idruglab.com/drd/index.php>
- Reference paper from the example: <https://pubs.acs.org/doi/10.1021/acs.jcim.9b00365>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <http://www.idruglab.com/drd/index.php>
- <https://pubs.acs.org/doi/10.1021/acs.jcim.9b00365>
