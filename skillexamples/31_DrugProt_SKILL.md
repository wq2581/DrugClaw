---
name: drugprot-query
description: >
  Query or inspect the DrugProt - Drug-Protein Relation Extraction Benchmark resource for drug-centric tasks with emphasis on drug nlp/text mining Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# DrugProt - Drug-Protein Relation Extraction Benchmark

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `31_DrugProt.py`
- Category: `Drug-centric`
- Type: `Dataset`
- Subcategory: `Drug NLP/Text Mining`

## API Surface

| Function | Purpose |
|---|---|
| `download_drugprot()` | See `31_DrugProt.py` for exact input/output behavior. |
| `parse_drugprot_relations()` | See `31_DrugProt.py` for exact input/output behavior. |

## Usage

Read `31_DrugProt.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_31_drugprot.py`
- Run: `python tools/test_skill_31_drugprot.py`
- Runtime import: `from skills.drug_nlp.drugprot import DrugProtSkill`

## Notes

- Review `if __name__ == "__main__"` in `31_DrugProt.py` first when generating runnable query code.
- Primary link from the example: <https://zenodo.org/records/5119892>
- Reference paper from the example: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10683943/>
- The validation script currently checks:
- import DrugProtSkill
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://zenodo.org/records/5119892>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC10683943/>
