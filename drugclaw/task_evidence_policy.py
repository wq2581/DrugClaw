from __future__ import annotations

from dataclasses import dataclass

from .evidence import EvidenceItem
from .query_plan import normalize_question_type


@dataclass(frozen=True)
class EvidenceClassification:
    tier: str
    slot: str
    rationale: str = ""


def classify_evidence_item(task_type: str, item: EvidenceItem) -> EvidenceClassification:
    normalized_task_type = normalize_question_type(task_type)
    if normalized_task_type == "drug_repurposing":
        return _classify_drug_repurposing_item(item)

    return EvidenceClassification(
        tier="generic_weak_support",
        slot="additional_context",
        rationale=f"no specialized policy for task type {normalized_task_type!r}",
    )


def _classify_drug_repurposing_item(item: EvidenceItem) -> EvidenceClassification:
    source_skill = str(getattr(item, "source_skill", "")).strip()
    relationship = str(item.metadata.get("relationship", "")).strip().lower()
    target_type = str(item.metadata.get("target_type", "")).strip().lower()

    if source_skill == "RepoDB" and relationship == "repurposing_evidence":
        return EvidenceClassification(
            tier="strong_structured",
            slot="repurposing_evidence",
            rationale="RepoDB repurposing rows are the Phase 2A primary source for repurposing evidence.",
        )

    if (
        source_skill in {"DrugBank", "DrugCentral"}
        and relationship == "indicated_for"
        and target_type == "disease"
    ):
        return EvidenceClassification(
            tier="strong_structured",
            slot="approved_indications",
            rationale="Structured disease-level indication rows from primary indication sources count as strong evidence.",
        )

    if source_skill in {"DailyMed", "openFDA Human Drug"} and relationship == "indicated_for":
        return EvidenceClassification(
            tier="secondary_official_support",
            slot="approved_indications",
            rationale="Official label-derived indication support is secondary official support in Phase 2A.",
        )

    if source_skill == "Open Targets Platform" and relationship in {"indicated_for", "investigated_for"}:
        return EvidenceClassification(
            tier="generic_weak_support",
            slot="approved_indications",
            rationale="Open Targets clinical-stage indication rows are useful support but not primary approved-indication evidence in Phase 2A.",
        )

    if source_skill in {"DailyMed", "openFDA Human Drug"}:
        return EvidenceClassification(
            tier="generic_weak_support",
            slot="additional_context",
            rationale="Official label sections outside direct indication support cannot be promoted to repurposing evidence.",
        )

    if source_skill == "DrugCentral" and relationship == "has_approved_entry":
        return EvidenceClassification(
            tier="generic_weak_support",
            slot="approved_indications",
            rationale="Approval roster rows without disease-level indication metadata are weaker than structured indication records.",
        )

    return EvidenceClassification(
        tier="generic_weak_support",
        slot="additional_context",
        rationale="Unmapped evidence defaults to weak contextual support.",
    )
