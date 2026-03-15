---
name: ade-corpus-query
description: >
  Query or inspect the ADE Corpus - Adverse Drug Event Extraction Benchmark resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# ADE Corpus - Adverse Drug Event Extraction Benchmark

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `32_ADE_Corpus.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `download_ade_corpus()` | See `32_ADE_Corpus.py` for exact input/output behavior. |
| `load_ade_dataset()` | See `32_ADE_Corpus.py` for exact input/output behavior. |

## Usage

Read `32_ADE_Corpus.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_32_ade_corpus.py`
- Run: `python tools/test_skill_32_ade_corpus.py`
- Runtime import: `from skills.drug_nlp.ade_corpus import ADECorpusSkill`

## Notes

- Review `if __name__ == "__main__"` in `32_ADE_Corpus.py` first when generating runnable query code.
- Primary link from the example: <https://github.com/trunghlt/AdverseDrugReaction>
- Reference paper from the example: <https://aclanthology.org/C16-1084/>
- The validation script currently checks:
- import ADECorpusSkill
- call is_available()
- standard query: drug=aspirin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://github.com/trunghlt/AdverseDrugReaction>
- <https://aclanthology.org/C16-1084/>
