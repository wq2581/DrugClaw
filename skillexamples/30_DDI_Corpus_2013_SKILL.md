---
name: ddi-corpus-2013-query
description: >
  Query or inspect the DDI Corpus 2013 - Drug-Drug Interaction Extraction NLP Benchmark resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DDI Corpus 2013 - Drug-Drug Interaction Extraction NLP Benchmark

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `30_DDI_Corpus_2013.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `download_ddi_corpus()` | See `30_DDI_Corpus_2013.py` for exact input/output behavior. |
| `parse_ddi_xml()` | See `30_DDI_Corpus_2013.py` for exact input/output behavior. |

## Usage

Read `30_DDI_Corpus_2013.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_30_ddi_corpus.py`
- Run: `python tools/test_skill_30_ddi_corpus.py`
- Runtime import: `from skills.drug_nlp.ddi_corpus import DDICorpusSkill`

## Notes

- Review `if __name__ == "__main__"` in `30_DDI_Corpus_2013.py` first when generating runnable query code.
- Primary link from the example: <https://github.com/isegura/DDICorpus>
- Reference paper from the example: <https://www.sciencedirect.com/science/article/pii/S1532046413001123>
- The validation script currently checks:
- import DDICorpusSkill
- call is_available()
- standard query: drug=aspirin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://github.com/isegura/DDICorpus>
- <https://www.sciencedirect.com/science/article/pii/S1532046413001123>
