---
name: promiscuous2-query
description: >
  Query or inspect the PROMISCUOUS 2.0 - Drug Polypharmacology Network resource for drug-centric tasks with emphasis on drug-target interaction (dti) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# PROMISCUOUS 2.0 - Drug Polypharmacology Network

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `46_PROMISCUOUS2.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug-Target Interaction (DTI)`

## API Surface

| Function | Purpose |
|---|---|
| `search_drug()` | See `46_PROMISCUOUS2.py` for exact input/output behavior. |
| `download_dataset()` | See `46_PROMISCUOUS2.py` for exact input/output behavior. |

## Usage

Read `46_PROMISCUOUS2.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skills_40_49.py`
- Run: `python tools/test_skills_40_49.py`

## Notes

- Review `if __name__ == "__main__"` in `46_PROMISCUOUS2.py` first when generating runnable query code.
- Primary link from the example: <https://bioinf-applied.charite.de/promiscuous2/index.php>
- Reference paper from the example: <https://academic.oup.com/nar/article/49/D1/D1373/5983618>
- The validation script currently checks:
- call is_available()

## Data Source

- <https://bioinf-applied.charite.de/promiscuous2/index.php>
- <https://academic.oup.com/nar/article/49/D1/D1373/5983618>
