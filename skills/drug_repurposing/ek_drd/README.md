# EK-DRD

> **Subcategory**: `drug_repurposing` &nbsp;|&nbsp; **Access mode**: `Local File`

**Purpose**: Expert knowledge drug repurposing  

**Coverage**: Expert knowledge-based drug repurposing database  

## Setup

1. Prepare a maintained EK-DRD CSV or TSV export.
2. Prefer a locally mirrored file under `resources_metadata/drug_repurposing/EK_DRD/`.
3. Set `csv_path` in config (see below).

## Configuration

| Key | Type / Description |
|-----|--------------------|
| `csv_path` | path to EK-DRD CSV/TSV export |
| `delimiter` | column delimiter (default: auto-detect from extension) |

## Usage

```python
from drugclaw.skills.drug_repurposing.ek_drd import EKDRDSkill

skill = EKDRDSkill(config={
    "csv_path": "...",  # path to EK-DRD CSV/TSV export
    "delimiter": "...",  # column delimiter (default: auto-detect from extension)
})

if skill.is_available():
    results = skill.retrieve(
        entities={"drug": ["imatinib"]},
        query="mechanism",
        max_results=20,
    )
    for r in results:
        print(r.source_entity, r.relationship, r.target_entity)
```

## Output (`RetrievalResult`)

| Field | Description |
|-------|-------------|
| `source_entity` | Drug name |
| `target_entity` | Target / disease / ADE / partner |
| `relationship` | Relation type |
| `weight` | Confidence / score (0–1 or raw) |
| `evidence_text` | Human-readable summary |
| `sources` | Source IDs (PMID, DOI, etc.) |
| `metadata` | Extra fields specific to this skill |

## Data Source

- Legacy source references:
  - <https://github.com/luoyunan/EKDRGraph>
  - <http://www.idruglab.com/drd/index.php>
- Verified runtime note: the GitHub reference is currently dead, and the iDrugLab portal currently fails TLS verification in automated access. This skill should be treated as local-file-only unless a maintained mirror is available.
