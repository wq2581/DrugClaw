---
name: askapatient-query
description: >
  Query or inspect the AskaPatient - Patient Drug Experience Ratings resource for drug-centric tasks with emphasis on drug review/patient report Use whenever Codex needs the calling pattern, downloadable entrypoint, or example query flow from this skill example script.
---

# AskaPatient - Patient Drug Experience Ratings

Use this file as the compact operator guide for the paired `skillexamples` script.
Prefer reading the Python example itself for exact request parameters, field names,
and response handling.

## Paired Example

- Script: `35_askapatient.py`
- Category: `Drug-centric`
- Type: `DB`
- Subcategory: `Drug Review/Patient Report`

## API Surface

| Function | Purpose |
|---|---|
| `get_drug_reviews()` | See `35_askapatient.py` for exact input/output behavior. |
| `check_robots_txt()` | See `35_askapatient.py` for exact input/output behavior. |

## Usage

Read `35_askapatient.py` and copy its call pattern when writing Code Agent query code.
Keep network timeouts short and preserve the script's native access method
(REST, direct download, local file scan, or HTML scraping).

## Validation

- Validation script: `tools/test_skill_35_askapatient.py`
- Run: `python tools/test_skill_35_askapatient.py`
- Runtime import: `from skills.drug_review.askapatient import AskAPatientSkill`

## Notes

- Review `if __name__ == "__main__"` in `35_askapatient.py` first when generating runnable query code.
- Primary link from the example: <https://www.askapatient.com/>
- The validation script currently checks:
- import AskAPatientSkill
- call is_available()
- standard query: drug=metformin
- edge query: drug=zzz_not_a_real_drug_zzz
- validate evidence_text and metadata

## Data Source

- <https://www.askapatient.com/>
