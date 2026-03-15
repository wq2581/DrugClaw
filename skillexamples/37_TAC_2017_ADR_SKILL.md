---
name: tac-2017-adr-query
description: >
  Query or inspect the TAC 2017 ADR - Adverse Drug Reaction Extraction from Drug Labels resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# TAC 2017 ADR - Adverse Drug Reaction Extraction from Drug Labels

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `37_TAC_2017_ADR.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `load_tac2017_from_huggingface()` | See `37_TAC_2017_ADR.py` for exact input/output behavior. |
| `describe_tac2017()` | See `37_TAC_2017_ADR.py` for exact input/output behavior. |

## Usage

Read `37_TAC_2017_ADR.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_37_tac2017.py`
- Run: `python tools/test_skill_37_tac2017.py`
- Runtime import: `from skills.drug_nlp.tac2017 import TAC2017ADRSkill`

## Notes

- Review `if __name__ == "__main__"` in `37_TAC_2017_ADR.py` first when generating runnable query code.
- Primary link from the example: <https://bionlp.nlm.nih.gov/tac2017adversereactions/>
- Reference paper from the example: <https://tac.nist.gov/publications/2017/additional.papers/TAC2017.ADR_overview.proceedings.pdf>
- The validation script currently checks:
- import TAC2017ADRSkill
- call is_available()
- standard query: drug=aspirin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://bionlp.nlm.nih.gov/tac2017adversereactions/>
- <https://tac.nist.gov/publications/2017/additional.papers/TAC2017.ADR_overview.proceedings.pdf>
- <https://huggingface.co/datasets/bigbio/tac2017_adr>
