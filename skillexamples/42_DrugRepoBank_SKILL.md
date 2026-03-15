---
name: drugrepobank-query
description: >
  Query or inspect the DrugRepoBank - Drug Repurposing Evidence Compilation resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DrugRepoBank - Drug Repurposing Evidence Compilation

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `42_DrugRepoBank.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `search_repurposing_candidates()` | See `42_DrugRepoBank.py` for exact input/output behavior. |
| `download_database()` | See `42_DrugRepoBank.py` for exact input/output behavior. |

## Usage

Read `42_DrugRepoBank.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_42_drugrepobank.py`
- Run: `python tools/test_skill_42_drugrepobank.py`
- Runtime import: `from skills.drug_repurposing.drugrepobank import DrugRepoBankSkill`

## Notes

- Review `if __name__ == "__main__"` in `42_DrugRepoBank.py` first when generating runnable query code.
- Primary link from the example: <https://awi.cuhk.edu.cn/DrugRepoBank/php/index.php>
- Reference paper from the example: <https://academic.oup.com/database/article/doi/10.1093/database/baae051/7712639>
- The validation script currently checks:
- import DrugRepoBankSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://awi.cuhk.edu.cn/DrugRepoBank/php/index.php>
- <https://academic.oup.com/database/article/doi/10.1093/database/baae051/7712639>
