---
name: drug-repurposing-hub-query
description: >
  Query or inspect the Drug Repurposing Hub - Curated Drug Repurposing Compound Collection resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# Drug Repurposing Hub - Curated Drug Repurposing Compound Collection

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `29_Drug_Repurposing_Hub.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `download_hub()` | See `29_Drug_Repurposing_Hub.py` for exact input/output behavior. |
| `preview_drugs()` | See `29_Drug_Repurposing_Hub.py` for exact input/output behavior. |

## Usage

Read `29_Drug_Repurposing_Hub.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_29_repurposing_hub.py`
- Run: `python tools/test_skill_29_repurposing_hub.py`
- Runtime import: `from skills.drug_repurposing.repurposing_hub import RepurposingHubSkill`

## Notes

- Review `if __name__ == "__main__"` in `29_Drug_Repurposing_Hub.py` first when generating runnable query code.
- Primary link from the example: <https://clue.io/repurposing>
- Reference paper from the example: <https://www.nature.com/articles/nm.4306>
- The validation script currently checks:
- import RepurposingHubSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://clue.io/repurposing>
- <https://www.nature.com/articles/nm.4306>
- <https://clue.io/repurposing-app>
