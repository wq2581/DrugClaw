---
name: n2c2-2018-track2-query
description: >
  Query or inspect the n2c2 2018 Track 2 - Drug and Adverse Event Extraction from Clinical Notes resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# n2c2 2018 Track 2 - Drug and Adverse Event Extraction from Clinical Notes

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `33_n2c2_2018_Track2.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `load_n2c2_from_huggingface()` | See `33_n2c2_2018_Track2.py` for exact input/output behavior. |
| `describe_dataset()` | See `33_n2c2_2018_Track2.py` for exact input/output behavior. |

## Usage

Read `33_n2c2_2018_Track2.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_33_n2c2_2018.py`
- Run: `python tools/test_skill_33_n2c2_2018.py`
- Runtime import: `from skills.drug_nlp.n2c2_2018 import N2C22018Skill`

## Notes

- Review `if __name__ == "__main__"` in `33_n2c2_2018_Track2.py` first when generating runnable query code.
- Primary link from the example: <https://huggingface.co/datasets/bigbio/n2c2_2018_track2>
- Reference paper from the example: <https://academic.oup.com/jamia/article-abstract/27/1/3/5581277>
- The validation script currently checks:
- import N2C22018Skill
- call is_available()
- standard query: drug=warfarin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://huggingface.co/datasets/bigbio/n2c2_2018_track2>
- <https://academic.oup.com/jamia/article-abstract/27/1/3/5581277>
