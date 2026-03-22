from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Dict, List, Tuple

from .drug_alias_sources import InMemoryDrugAliasSource


@dataclass
class DrugNameNormalizer:
    alias_source: InMemoryDrugAliasSource

    @classmethod
    def default(cls) -> "DrugNameNormalizer":
        return cls(alias_source=InMemoryDrugAliasSource.default())

    def normalize_query(self, query: str) -> Dict[str, Any]:
        original_query = str(query)
        normalized_query = original_query
        resolution_trace: List[Dict[str, str]] = []
        detected_mentions: List[str] = []
        canonical_drug_names: List[str] = []
        alias_candidates: List[str] = []

        for alias, canonical in sorted(
            self.alias_source.alias_to_canonical.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            pattern = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
            matches = list(pattern.finditer(normalized_query))
            if not matches:
                continue

            normalized_query = pattern.sub(canonical, normalized_query)
            detected_mentions.extend(match.group(0) for match in matches)
            if canonical not in canonical_drug_names:
                canonical_drug_names.append(canonical)
            if alias != canonical and alias not in alias_candidates:
                alias_candidates.append(alias)
            resolution_trace.append(
                {
                    "matched_text": ", ".join(match.group(0) for match in matches),
                    "matched_alias": alias,
                    "canonical_name": canonical,
                }
            )

        if not canonical_drug_names:
            status = "unresolved"
        elif len(canonical_drug_names) == 1:
            status = "resolved"
        else:
            status = "ambiguous"

        return {
            "original_query": original_query,
            "normalized_query": normalized_query,
            "status": status,
            "detected_drug_mentions": detected_mentions,
            "canonical_drug_names": canonical_drug_names,
            "alias_candidates": alias_candidates,
            "resolution_trace": resolution_trace,
        }

    def normalize_entities(self, entities: Dict[str, List[str]]) -> Tuple[Dict[str, List[str]], Dict[str, Any]]:
        resolved_entities: Dict[str, List[str]] = {}
        traces: List[Dict[str, str]] = []

        for entity_type, values in entities.items():
            if entity_type != "drug":
                if values:
                    resolved_entities[entity_type] = list(values)
                continue

            canonical_values: List[str] = []
            for value in values:
                canonical = self.alias_source.resolve_name(value) or value
                if canonical not in canonical_values:
                    canonical_values.append(canonical)
                if canonical != value:
                    traces.append(
                        {
                            "matched_alias": value,
                            "canonical_name": canonical,
                        }
                    )
            if canonical_values:
                resolved_entities[entity_type] = canonical_values

        return resolved_entities, {"entity_resolution_trace": traces}
