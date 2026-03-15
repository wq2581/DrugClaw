---
name: oregano-query
description: >
  Query or inspect the OREGANO - Drug Repurposing Knowledge Graph resource for drug-centric tasks with emphasis on drug repurposing Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# OREGANO - Drug Repurposing Knowledge Graph

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `24_OREGANO.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Repurposing`

## API Surface

| Function | Purpose |
|---|---|
| `download_oregano()` | See `24_OREGANO.py` for exact input/output behavior. |
| `list_contents()` | See `24_OREGANO.py` for exact input/output behavior. |

## Usage

Read `24_OREGANO.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_24_oregano.py`
- Run: `python tools/test_skill_24_oregano.py`
- Runtime import: `from skills.drug_repurposing.oregano import OREGANOSkill`

## Notes

- Review `if __name__ == "__main__"` in `24_OREGANO.py` first when generating runnable query code.
- Primary link from the example: <https://gitub.u-bordeaux.fr/erias/oregano>
- Reference paper from the example: <https://www.nature.com/articles/s41597-023-02757-0>
- The validation script currently checks:
- import OREGANOSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://gitub.u-bordeaux.fr/erias/oregano>
- <https://www.nature.com/articles/s41597-023-02757-0>
