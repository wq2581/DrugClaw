---
name: nsides-query
description: >
  Query or inspect the nSIDES - EHR-Derived Drug Side Effects resource for drug-centric tasks with emphasis on adverse drug reaction (adr) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# nSIDES - EHR-Derived Drug Side Effects

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `15_nSIDES.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Adverse Drug Reaction (ADR)`

## API Surface

| Function | Purpose |
|---|---|
| `search_concept()` | See `15_nSIDES.py` for exact input/output behavior. |
| `get_drug_outcomes()` | See `15_nSIDES.py` for exact input/output behavior. |
| `get_outcome_drugs()` | See `15_nSIDES.py` for exact input/output behavior. |
| `query()` | See `15_nSIDES.py` for exact input/output behavior. |
| `query_batch()` | See `15_nSIDES.py` for exact input/output behavior. |
| `summarize()` | See `15_nSIDES.py` for exact input/output behavior. |

## Usage

Read `15_nSIDES.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Notes

- Review `if __name__ == "__main__"` in `15_nSIDES.py` first when generating runnable query code.
- Primary link from the example: <https://nsides.io/>
- Reference paper from the example: <https://www.science.org/doi/10.1126/scitranslmed.3003377>

## Data Source

- <https://nsides.io/>
- <https://www.science.org/doi/10.1126/scitranslmed.3003377>
- <https://nsides.io/api/v1>
