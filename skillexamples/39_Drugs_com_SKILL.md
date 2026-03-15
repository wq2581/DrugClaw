---
name: drugs-com-query
description: >
  Query or inspect the Drugs.com - Consumer Drug Information and Interactions resource for drug-centric tasks with emphasis on drug knowledgebase Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# Drugs.com - Consumer Drug Information and Interactions

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `39_Drugs_com.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Knowledgebase`

## API Surface

| Function | Purpose |
|---|---|
| `get_drug_info_page()` | See `39_Drugs_com.py` for exact input/output behavior. |
| `extract_drug_details()` | See `39_Drugs_com.py` for exact input/output behavior. |
| `check_drug_interactions()` | See `39_Drugs_com.py` for exact input/output behavior. |

## Usage

Read `39_Drugs_com.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skills_30_39.py`
- Run: `python tools/test_skills_30_39.py`

## Notes

- Review `if __name__ == "__main__"` in `39_Drugs_com.py` first when generating runnable query code.
- Primary link from the example: <https://www.drugs.com/>
- The validation script currently checks:
- call is_available()

## Data Source

- <https://www.drugs.com/>
