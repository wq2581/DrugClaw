from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def _normalize_name(text: str) -> str:
    normalized = re.sub(r"\s+", " ", str(text).strip().lower())
    return normalized


def normalize_chembl_identifier(value: str) -> str:
    match = re.search(r"chembl[:\s-]?(\d+)", str(value), flags=re.IGNORECASE)
    if match:
        return f"CHEMBL{match.group(1)}"
    text = str(value).strip().upper()
    return text if re.fullmatch(r"CHEMBL\d+", text) else ""


def normalize_pubchem_cid(value: str) -> str:
    match = re.search(r"(\d+)", str(value))
    return match.group(1) if match else ""


def normalize_inchikey(value: str) -> str:
    text = str(value).strip().upper()
    text = re.sub(r"^INCHIKEY\s*[:=]\s*", "", text)
    return text if re.fullmatch(r"[A-Z]{14}-[A-Z]{10}-[A-Z]", text) else ""


@dataclass(frozen=True)
class ResolvedIdentifierRecord:
    identifier_type: str
    identifier_value: str
    canonical_name: str = ""
    source: str = ""
    status: str = "unresolved"
    error: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "identifier_type": self.identifier_type,
            "identifier_value": self.identifier_value,
            "canonical_drug_name": self.canonical_name,
            "source": self.source,
            "status": self.status,
            "error": self.error,
        }


class _CachedIdentifierSource:
    def __init__(self, timeout: int = 5, cache_size: int = 256) -> None:
        self.timeout = timeout
        self.cache_size = cache_size
        self._cache: OrderedDict[tuple[str, str], ResolvedIdentifierRecord] = OrderedDict()

    def _get_cached(
        self,
        identifier_type: str,
        identifier_value: str,
    ) -> ResolvedIdentifierRecord | None:
        key = (identifier_type, identifier_value)
        record = self._cache.get(key)
        if record is not None:
            self._cache.move_to_end(key)
        return record

    def _set_cached(self, record: ResolvedIdentifierRecord) -> None:
        if not record.canonical_name:
            return
        key = (record.identifier_type, record.identifier_value)
        self._cache[key] = record
        self._cache.move_to_end(key)
        while len(self._cache) > self.cache_size:
            self._cache.popitem(last=False)

    def _fetch_json(self, url: str) -> dict[str, Any]:
        with urlopen(url, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _error_code(exc: Exception) -> str:
        if isinstance(exc, HTTPError):
            return f"http_{exc.code}"
        if isinstance(exc, TimeoutError):
            return "timeout"
        if isinstance(exc, URLError):
            reason = getattr(exc, "reason", None)
            if isinstance(reason, TimeoutError):
                return "timeout"
            return "network_error"
        return "unexpected_error"


class ChEMBLIdentifierSource(_CachedIdentifierSource):
    def resolve_chembl_id(self, value: str) -> ResolvedIdentifierRecord:
        normalized_value = normalize_chembl_identifier(value)
        if not normalized_value:
            return ResolvedIdentifierRecord(
                identifier_type="chembl_id",
                identifier_value=str(value).strip(),
                source="chembl_rest",
                status="unresolved",
                error="invalid_identifier",
            )

        cached = self._get_cached("chembl_id", normalized_value)
        if cached is not None:
            return cached

        try:
            payload = self._fetch_json(
                f"https://www.ebi.ac.uk/chembl/api/data/molecule/{normalized_value}.json"
            )
        except Exception as exc:
            return ResolvedIdentifierRecord(
                identifier_type="chembl_id",
                identifier_value=normalized_value,
                source="chembl_rest",
                status="error",
                error=self._error_code(exc),
            )

        candidate_names = [
            payload.get("pref_name"),
            payload.get("chembl_pref_name"),
        ]
        for synonym in payload.get("molecule_synonyms", []) or []:
            candidate_names.append(synonym.get("molecule_synonym"))
            candidate_names.append(synonym.get("synonyms"))

        canonical_name = ""
        for candidate in candidate_names:
            normalized_name = _normalize_name(candidate)
            if normalized_name:
                canonical_name = normalized_name
                break

        record = ResolvedIdentifierRecord(
            identifier_type="chembl_id",
            identifier_value=normalized_value,
            canonical_name=canonical_name,
            source="chembl_rest",
            status="resolved" if canonical_name else "unresolved",
            error="" if canonical_name else "not_found",
        )
        self._set_cached(record)
        return record


class PubChemIdentifierSource(_CachedIdentifierSource):
    def resolve_pubchem_cid(self, value: str) -> ResolvedIdentifierRecord:
        normalized_value = normalize_pubchem_cid(value)
        if not normalized_value:
            return ResolvedIdentifierRecord(
                identifier_type="pubchem_cid",
                identifier_value=str(value).strip(),
                source="pubchem_pug_rest",
                status="unresolved",
                error="invalid_identifier",
            )

        cached = self._get_cached("pubchem_cid", normalized_value)
        if cached is not None:
            return cached

        try:
            payload = self._fetch_json(
                "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
                f"cid/{normalized_value}/property/Title/JSON"
            )
        except Exception as exc:
            return ResolvedIdentifierRecord(
                identifier_type="pubchem_cid",
                identifier_value=normalized_value,
                source="pubchem_pug_rest",
                status="error",
                error=self._error_code(exc),
            )

        canonical_name = self._extract_pubchem_title(payload)
        record = ResolvedIdentifierRecord(
            identifier_type="pubchem_cid",
            identifier_value=normalized_value,
            canonical_name=canonical_name,
            source="pubchem_pug_rest",
            status="resolved" if canonical_name else "unresolved",
            error="" if canonical_name else "not_found",
        )
        self._set_cached(record)
        return record

    def resolve_inchikey(self, value: str) -> ResolvedIdentifierRecord:
        normalized_value = normalize_inchikey(value)
        if not normalized_value:
            return ResolvedIdentifierRecord(
                identifier_type="inchikey",
                identifier_value=str(value).strip(),
                source="pubchem_pug_rest",
                status="unresolved",
                error="invalid_identifier",
            )

        cached = self._get_cached("inchikey", normalized_value)
        if cached is not None:
            return cached

        try:
            payload = self._fetch_json(
                "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
                f"inchikey/{normalized_value}/property/Title/JSON"
            )
        except Exception as exc:
            return ResolvedIdentifierRecord(
                identifier_type="inchikey",
                identifier_value=normalized_value,
                source="pubchem_pug_rest",
                status="error",
                error=self._error_code(exc),
            )

        canonical_name = self._extract_pubchem_title(payload)
        record = ResolvedIdentifierRecord(
            identifier_type="inchikey",
            identifier_value=normalized_value,
            canonical_name=canonical_name,
            source="pubchem_pug_rest",
            status="resolved" if canonical_name else "unresolved",
            error="" if canonical_name else "not_found",
        )
        self._set_cached(record)
        return record

    @staticmethod
    def _extract_pubchem_title(payload: dict[str, Any]) -> str:
        properties = (
            payload.get("PropertyTable", {}).get("Properties", [])
            if isinstance(payload, dict)
            else []
        )
        if not properties:
            return ""
        return _normalize_name(properties[0].get("Title", ""))


class CompositeDrugIdentifierSource:
    def __init__(
        self,
        chembl_source: ChEMBLIdentifierSource | None = None,
        pubchem_source: PubChemIdentifierSource | None = None,
    ) -> None:
        self.chembl_source = chembl_source or ChEMBLIdentifierSource()
        self.pubchem_source = pubchem_source or PubChemIdentifierSource()

    @classmethod
    def default(cls, timeout: int = 5, cache_size: int = 256) -> "CompositeDrugIdentifierSource":
        return cls(
            chembl_source=ChEMBLIdentifierSource(timeout=timeout, cache_size=cache_size),
            pubchem_source=PubChemIdentifierSource(timeout=timeout, cache_size=cache_size),
        )

    def resolve_identifier(
        self,
        identifier_type: str,
        identifier_value: str,
    ) -> list[ResolvedIdentifierRecord]:
        if identifier_type == "chembl_id":
            return [self.chembl_source.resolve_chembl_id(identifier_value)]
        if identifier_type == "pubchem_cid":
            return [self.pubchem_source.resolve_pubchem_cid(identifier_value)]
        if identifier_type == "inchikey":
            return [self.pubchem_source.resolve_inchikey(identifier_value)]
        return []
