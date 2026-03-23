from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, Iterable, Mapping


DEFAULT_DRUG_ALIAS_SEED: Dict[str, list[str]] = {
    "imatinib": ["gleevec"],
    "metformin": ["glucophage"],
    "sildenafil": ["viagra"],
    "atorvastatin": ["lipitor"],
}


def normalize_drug_token(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", str(text).strip().lower())
    return " ".join(normalized.split())


@dataclass(frozen=True)
class InMemoryDrugAliasSource:
    alias_to_canonical: Mapping[str, str]

    @classmethod
    def default(cls) -> "InMemoryDrugAliasSource":
        return cls.from_seed(DEFAULT_DRUG_ALIAS_SEED)

    @classmethod
    def from_seed(
        cls,
        seed: Mapping[str, Iterable[str]],
    ) -> "InMemoryDrugAliasSource":
        alias_to_canonical: Dict[str, str] = {}
        for canonical_name, aliases in seed.items():
            normalized_canonical = normalize_drug_token(canonical_name)
            if not normalized_canonical:
                continue

            alias_to_canonical[normalized_canonical] = normalized_canonical
            for alias in aliases:
                normalized_alias = normalize_drug_token(alias)
                if normalized_alias:
                    alias_to_canonical[normalized_alias] = normalized_canonical

        return cls(alias_to_canonical=alias_to_canonical)

    def resolve_name(self, name: str) -> str | None:
        normalized_name = normalize_drug_token(name)
        if not normalized_name:
            return None
        return self.alias_to_canonical.get(normalized_name)
