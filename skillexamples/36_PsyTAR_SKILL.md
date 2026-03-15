---
name: psytar-query
description: >
  Query or inspect the PsyTAR - Psychiatric Treatment Adverse Reaction Corpus resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# PsyTAR - Psychiatric Treatment Adverse Reaction Corpus

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `36_PsyTAR.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `load_psytar()` | See `36_PsyTAR.py` for exact input/output behavior. |
| `describe_psytar()` | See `36_PsyTAR.py` for exact input/output behavior. |

## Usage

Read `36_PsyTAR.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_36_psytar.py`
- Run: `python tools/test_skill_36_psytar.py`
- Runtime import: `from skills.drug_nlp.psytar import PsyTARSkill`

## Notes

- Review `if __name__ == "__main__"` in `36_PsyTAR.py` first when generating runnable query code.
- Primary link from the example: <https://huggingface.co/datasets/bigbio/psytar>
- Reference paper from the example: <https://dl.acm.org/doi/10.1016/j.jbi.2018.12.005>
- The validation script currently checks:
- import PsyTARSkill
- call is_available()
- standard query: drug=sertraline
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://huggingface.co/datasets/bigbio/psytar>
- <https://dl.acm.org/doi/10.1016/j.jbi.2018.12.005>
