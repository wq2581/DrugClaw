---
name: dilirank-query
description: >
  Query or inspect the DILIrank - Drug-Induced Liver Injury Risk Ranking resource for drug-centric tasks with emphasis on drug toxicity Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DILIrank - Drug-Induced Liver Injury Risk Ranking

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `48_DILIrank.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug Toxicity`

## API Surface

| Function | Purpose |
|---|---|
| `download_dilirank()` | See `48_DILIrank.py` for exact input/output behavior. |
| `preview_dilirank()` | See `48_DILIrank.py` for exact input/output behavior. |

## Usage

Read `48_DILIrank.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_48_dilirank.py`
- Run: `python tools/test_skill_48_dilirank.py`
- Runtime import: `from skills.drug_toxicity.dilirank import DILIrankSkill`

## Notes

- Review `if __name__ == "__main__"` in `48_DILIrank.py` first when generating runnable query code.
- Primary link from the example: <https://www.fda.gov/science-research/liver-toxicity-knowledge-base-ltkb/drug-induced-liver-injury-rank-dilirank-dataset>
- Reference paper from the example: <https://www.sciencedirect.com/science/article/abs/pii/S1359644616300411>
- The validation script currently checks:
- import DILIrankSkill
- call is_available()
- standard query: drug=acetaminophen
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://www.fda.gov/science-research/liver-toxicity-knowledge-base-ltkb/drug-induced-liver-injury-rank-dilirank-dataset>
- <https://www.sciencedirect.com/science/article/abs/pii/S1359644616300411>
