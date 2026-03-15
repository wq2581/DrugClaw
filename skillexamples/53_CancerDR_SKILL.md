---
name: cancerdr-query
description: >
  Query or inspect the CancerDR - Cancer Drug Resistance Data resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# CancerDR - Cancer Drug Resistance Data

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `53_CancerDR.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `download_cancerdr()` | See `53_CancerDR.py` for exact input/output behavior. |
| `describe_cancerdr()` | See `53_CancerDR.py` for exact input/output behavior. |

## Usage

Read `53_CancerDR.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_53_cancerdr.py`
- Run: `python tools/test_skill_53_cancerdr.py`
- Runtime import: `from skills.drug_repurposing.cancerdr.cancerdr_skill import CancerDRSkill`

## Notes

- Review `if __name__ == "__main__"` in `53_CancerDR.py` first when generating runnable query code.
- Primary link from the example: <http://crdd.osdd.net/raghava/cancerdr/>
- Reference paper from the example: <https://www.nature.com/articles/srep01445>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <http://crdd.osdd.net/raghava/cancerdr/>
- <https://www.nature.com/articles/srep01445>
