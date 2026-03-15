---
name: cadec-query
description: >
  Query or inspect the CADEC - CSIRO Adverse Drug Event Corpus resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# CADEC - CSIRO Adverse Drug Event Corpus

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `34_CADEC.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `load_cadec_from_huggingface()` | See `34_CADEC.py` for exact input/output behavior. |
| `describe_cadec()` | See `34_CADEC.py` for exact input/output behavior. |

## Usage

Read `34_CADEC.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_34_cadec.py`
- Run: `python tools/test_skill_34_cadec.py`
- Runtime import: `from skills.drug_nlp.cadec import CADECSkill`

## Notes

- Review `if __name__ == "__main__"` in `34_CADEC.py` first when generating runnable query code.
- Primary link from the example: <https://data.csiro.au/collection/csiro:10948>
- Reference paper from the example: <https://www.sciencedirect.com/science/article/pii/S1532046415000532>
- The validation script currently checks:
- import CADECSkill
- call is_available()
- standard query: drug=lipitor
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://data.csiro.au/collection/csiro:10948>
- <https://www.sciencedirect.com/science/article/pii/S1532046415000532>
- <https://huggingface.co/datasets/bigbio/cadec>
