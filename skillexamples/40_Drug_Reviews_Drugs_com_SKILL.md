---
name: drug-reviews-drugs-com-query
description: >
  Query or inspect the Drug Reviews (Drugs.com) - Drug User Reviews for NLP resource for drug-centric tasks with emphasis on drug review/patient report Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# Drug Reviews (Drugs.com) - Drug User Reviews for NLP

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `40_Drug_Reviews_Drugs_com.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug Review/Patient Report`

## API Surface

| Function | Purpose |
|---|---|
| `download_drug_reviews()` | See `40_Drug_Reviews_Drugs_com.py` for exact input/output behavior. |
| `preview_reviews()` | See `40_Drug_Reviews_Drugs_com.py` for exact input/output behavior. |

## Usage

Read `40_Drug_Reviews_Drugs_com.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_40_drugs_com_reviews.py`
- Run: `python tools/test_skill_40_drugs_com_reviews.py`
- Runtime import: `from skills.drug_review.drugs_com_reviews import DrugsComReviewsSkill`

## Notes

- Review `if __name__ == "__main__"` in `40_Drug_Reviews_Drugs_com.py` first when generating runnable query code.
- Primary link from the example: <https://archive.ics.uci.edu/dataset/461/drug+review+dataset+druglib+com>
- Reference paper from the example: <N/A>
- The validation script currently checks:
- import DrugsComReviewsSkill
- call is_available()
- standard query: drug=aspirin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://archive.ics.uci.edu/dataset/461/drug+review+dataset+druglib+com>
- N/A
