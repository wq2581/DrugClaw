---
name: who-essential-medicines-list-query
description: >
  Query or inspect the WHO Essential Medicines List - Global Essential Drug List resource for drug-centric tasks with emphasis on drug knowledgebase Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# WHO Essential Medicines List - Global Essential Drug List

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `58_WHO_Essential_Medicines_List.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Knowledgebase`

## API Surface

| Function | Purpose |
|---|---|
| `download_eml_pdf()` | See `58_WHO_Essential_Medicines_List.py` for exact input/output behavior. |
| `download_community_csv()` | See `58_WHO_Essential_Medicines_List.py` for exact input/output behavior. |
| `preview_eml_csv()` | See `58_WHO_Essential_Medicines_List.py` for exact input/output behavior. |

## Usage

Read `58_WHO_Essential_Medicines_List.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_58_who_eml.py`
- Run: `python tools/test_skill_58_who_eml.py`
- Runtime import: `from skills.drug_knowledgebase.who_eml.who_eml_skill import WHOEssentialMedicinesSkill`

## Notes

- Review `if __name__ == "__main__"` in `58_WHO_Essential_Medicines_List.py` first when generating runnable query code.
- Primary link from the example: <https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.02>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.02>
