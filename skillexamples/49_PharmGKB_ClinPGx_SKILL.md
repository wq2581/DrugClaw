---
name: pharmgkb-clinpgx-query
description: >
  Query or inspect the 49 · PharmGKB / ClinPGx – Pharmacogenomics Knowledge Curation resource for drug-related (indirect) tasks with emphasis on pharmacogenomics Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# 49 · PharmGKB / ClinPGx – Pharmacogenomics Knowledge Curation

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `49_PharmGKB_ClinPGx.py`
- Category: `Drug-related (indirect)`
- Type: `REST API`
- Subcategory: `Pharmacogenomics`

## API Surface

| Function | Purpose |
|---|---|
| `search_gene()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `get_gene_detail()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `search_drug()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `get_drug_detail()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `search_variant()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `lookup_by_id()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `get_cpic_pairs_by_gene()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |
| `get_cpic_pairs_by_drug()` | See `49_PharmGKB_ClinPGx.py` for exact input/output behavior. |

## Usage

Read `49_PharmGKB_ClinPGx.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_49_pharmgkb.py`
- Run: `python tools/test_skill_49_pharmgkb.py`
- Runtime import: `from skills.pharmacogenomics.pharmgkb import PharmGKBSkill`

## Notes

- Review `if __name__ == "__main__"` in `49_PharmGKB_ClinPGx.py` first when generating runnable query code.
- Primary link from the example: <https://www.clinpgx.org/>
- The validation script currently checks:
- import PharmGKBSkill
- instantiate PharmGKBSkill(timeout=20)
- call is_available()
- standard query: drug=clopidogrel and gene=CYP2C19
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://www.clinpgx.org/>
- <https://api.clinpgx.org/v1>
- <https://api.cpicpgx.org/v1>
