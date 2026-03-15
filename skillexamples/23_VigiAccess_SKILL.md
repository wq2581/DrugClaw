---
name: vigiaccess-query
description: >
  Query or inspect the VigiAccess - Global Pharmacovigilance Data resource for drug-centric tasks with emphasis on adverse drug reaction (adr) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# VigiAccess - Global Pharmacovigilance Data

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `23_VigiAccess.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Adverse Drug Reaction (ADR)`

## API Surface

| Function | Purpose |
|---|---|
| `get_vigiaccess_page()` | See `23_VigiAccess.py` for exact input/output behavior. |
| `demonstrate_access()` | See `23_VigiAccess.py` for exact input/output behavior. |

## Usage

Read `23_VigiAccess.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skills_20_29.py`
- Run: `python tools/test_skills_20_29.py`

## Notes

- Review `if __name__ == "__main__"` in `23_VigiAccess.py` first when generating runnable query code.
- Primary link from the example: <http://www.vigiaccess.org/>
- The validation script currently checks:
- call is_available()

## Data Source

- <http://www.vigiaccess.org/>
- <http://www.vigiaccess.org/.>
- <https://www.who-umc.org/>
