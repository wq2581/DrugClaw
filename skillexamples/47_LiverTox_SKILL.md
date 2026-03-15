---
name: livertox-query
description: >
  Query or inspect the LiverTox - Drug-Induced Liver Injury Information resource for drug-centric tasks with emphasis on drug toxicity Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# LiverTox - Drug-Induced Liver Injury Information

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `47_LiverTox.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Toxicity`

## API Surface

| Function | Purpose |
|---|---|
| `search_livertox()` | See `47_LiverTox.py` for exact input/output behavior. |
| `fetch_livertox_summary()` | See `47_LiverTox.py` for exact input/output behavior. |
| `get_livertox_article_text()` | See `47_LiverTox.py` for exact input/output behavior. |

## Usage

Read `47_LiverTox.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_47_livertox.py`
- Run: `python tools/test_skill_47_livertox.py`
- Runtime import: `from skills.drug_toxicity.livertox import LiverToxSkill`

## Notes

- Review `if __name__ == "__main__"` in `47_LiverTox.py` first when generating runnable query code.
- Primary link from the example: <https://www.ncbi.nlm.nih.gov/books/NBK547852/>
- The validation script currently checks:
- import LiverToxSkill
- call is_available()
- standard query: drug=acetaminophen
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://www.ncbi.nlm.nih.gov/books/NBK547852/>
