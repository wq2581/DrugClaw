---
name: pharmkg-query
description: >
  Query or inspect the PharmKG - Pharmacology Knowledge Graph Benchmark resource for drug-centric tasks with emphasis on drug knowledgebase Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# PharmKG - Pharmacology Knowledge Graph Benchmark

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `55_PharmKG.py`
- Category: `Drug-centric`
- Type: `KG`
- Subcategory: `Drug Knowledgebase`

## API Surface

| Function | Purpose |
|---|---|
| `download_pharmkg()` | See `55_PharmKG.py` for exact input/output behavior. |
| `preview_pharmkg_triples()` | See `55_PharmKG.py` for exact input/output behavior. |
| `describe_pharmkg()` | See `55_PharmKG.py` for exact input/output behavior. |

## Usage

Read `55_PharmKG.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_55_pharmkg.py`
- Run: `python tools/test_skill_55_pharmkg.py`
- Runtime import: `from skills.drug_knowledgebase.pharmkg.pharmkg_skill import PharmKGSkill`

## Notes

- Review `if __name__ == "__main__"` in `55_PharmKG.py` first when generating runnable query code.
- Primary link from the example: <https://github.com/MindRank-Biotech/PharmKG>
- Reference paper from the example: <https://academic.oup.com/bib/article/22/4/bbaa344/6042240>
- Inspect the validation script directly for its current assertions and sample entities.

## Data Source

- <https://github.com/MindRank-Biotech/PharmKG>
- <https://academic.oup.com/bib/article/22/4/bbaa344/6042240>
