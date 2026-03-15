---
name: bindingdb-query
description: >
  Query or inspect the BindingDB – Drug-Target Binding Affinity Data resource for drug-centric tasks with emphasis on drug-target interaction (dti) Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# BindingDB – Drug-Target Binding Affinity Data

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `26_BindingDB.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug-Target Interaction (DTI)`

## API Surface

| Function | Purpose |
|---|---|
| `query_by_uniprot()` | See `26_BindingDB.py` for exact input/output behavior. |
| `query_by_pdb()` | See `26_BindingDB.py` for exact input/output behavior. |
| `query_by_smiles()` | See `26_BindingDB.py` for exact input/output behavior. |
| `search()` | See `26_BindingDB.py` for exact input/output behavior. |
| `search_batch()` | See `26_BindingDB.py` for exact input/output behavior. |
| `summarize()` | See `26_BindingDB.py` for exact input/output behavior. |
| `to_json()` | See `26_BindingDB.py` for exact input/output behavior. |

## Usage

Read `26_BindingDB.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_26_bindingdb.py`
- Run: `python tools/test_skill_26_bindingdb.py`
- Runtime import: `from skills.dti.bindingdb import BindingDBSkill`

## Notes

- Review `if __name__ == "__main__"` in `26_BindingDB.py` first when generating runnable query code.
- Primary link from the example: <https://www.bindingdb.org/>
- Reference paper from the example: <https://academic.oup.com/nar/article/53/D1/D1633/7906836>
- The validation script currently checks:
- import BindingDBSkill
- instantiate BindingDBSkill(timeout=20)
- call is_available()
- standard query: drug=imatinib
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://www.bindingdb.org/>
- <https://academic.oup.com/nar/article/53/D1/D1633/7906836>
- <https://www.bindingdb.org/rwd/bind/BindingDBRESTfulAPI.jsp>
