---
name: kegg-drug-query
description: >
  Query or inspect the KEGG Drug - Approved Drugs and Their Molecular Mechanisms resource for drug-centric tasks with emphasis on drug-drug interaction (ddi) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# KEGG Drug - Approved Drugs and Their Molecular Mechanisms

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `68_KEGG_Drug.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug-Drug Interaction (DDI)`

## API Surface

| Function | Purpose |
|---|---|
| `search()` | See `68_KEGG_Drug.py` for exact input/output behavior. |
| `get_entry()` | See `68_KEGG_Drug.py` for exact input/output behavior. |
| `get_interactions()` | See `68_KEGG_Drug.py` for exact input/output behavior. |
| `get_targets()` | See `68_KEGG_Drug.py` for exact input/output behavior. |
| `query()` | See `68_KEGG_Drug.py` for exact input/output behavior. |

## Usage

Read `68_KEGG_Drug.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skills_66_68.py`
- Run: `python tools/test_skills_66_68.py`

## Notes

- Review `if __name__ == "__main__"` in `68_KEGG_Drug.py` first when generating runnable query code.
- Primary link from the example: <https://www.genome.jp/kegg/>
- Reference paper from the example: <https://academic.oup.com/nar/article/38/suppl_1/D355/3112250>
- The validation script currently checks:
- import SemaTyPSkill
- instantiate with real local file config if available
- call is_available()
- call retrieve(...) with README-style drug input
- validate evidence_text and metadata

## Data Source

- <https://www.genome.jp/kegg/>
- <https://academic.oup.com/nar/article/38/suppl_1/D355/3112250>
- <https://www.kegg.jp/kegg/docs/keggapi.html>
