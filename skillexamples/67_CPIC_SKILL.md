---
name: cpic-query
description: >
  Query or inspect the CPIC - Clinical Pharmacogenomics Implementation Consortium resource for drug-centric tasks with emphasis on drug knowledgebase Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# CPIC - Clinical Pharmacogenomics Implementation Consortium

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `67_CPIC.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Knowledgebase`

## API Surface

| Function | Purpose |
|---|---|
| `get_drug_info()` | See `67_CPIC.py` for exact input/output behavior. |
| `get_guidelines()` | See `67_CPIC.py` for exact input/output behavior. |
| `get_gene_drug_pairs()` | See `67_CPIC.py` for exact input/output behavior. |
| `get_recommendations()` | See `67_CPIC.py` for exact input/output behavior. |
| `query()` | See `67_CPIC.py` for exact input/output behavior. |

## Usage

Read `67_CPIC.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_67_cpic.py`
- Run: `python tools/test_skill_67_cpic.py`
- Runtime import: `from skills.drug_knowledgebase.cpic import CPICSkill`

## Notes

- Review `if __name__ == "__main__"` in `67_CPIC.py` first when generating runnable query code.
- Primary link from the example: <https://cpicpgx.org/>
- Reference paper from the example: <https://pubmed.ncbi.nlm.nih.gov/33479744/>
- The validation script currently checks:
- read cpic_skill.py
- read README.md
- read SKILL.md if present
- read skills/.../example.py and skillexamples/67_CPIC.py
- import CPICSkill
- instantiate CPICSkill(timeout=20)
- call is_available()
- standard query 1: drug=clopidogrel

## Data Source

- <https://cpicpgx.org/>
- <https://pubmed.ncbi.nlm.nih.gov/33479744/>
- <https://cpicpgx.org/cpic-data/>
