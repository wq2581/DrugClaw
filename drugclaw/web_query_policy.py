from __future__ import annotations

from typing import Dict, Iterable, List, Sequence
from urllib.parse import urlparse


HIGH_RISK_QUESTION_TYPES = {
    "adr",
    "ddi",
    "ddi_mechanism",
    "labeling",
    "pharmacogenomics",
}


_AUTHORITY_DOMAINS: Dict[str, set[str]] = {
    "target_lookup": {
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "opentargets.org",
        "platform.opentargets.org",
        "chembl.ebi.ac.uk",
        "drugbank.com",
    },
    "mechanism": {
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "opentargets.org",
        "platform.opentargets.org",
        "chembl.ebi.ac.uk",
        "drugbank.com",
        "nih.gov",
    },
    "drug_repurposing": {
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "clinicaltrials.gov",
        "fda.gov",
        "nih.gov",
    },
    "adr": {
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "fda.gov",
        "dailymed.nlm.nih.gov",
        "nih.gov",
    },
    "ddi": {
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "fda.gov",
        "dailymed.nlm.nih.gov",
        "nih.gov",
    },
    "ddi_mechanism": {
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "fda.gov",
        "dailymed.nlm.nih.gov",
        "nih.gov",
    },
    "labeling": {
        "dailymed.nlm.nih.gov",
        "fda.gov",
        "nih.gov",
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
    },
    "pharmacogenomics": {
        "cpicpgx.org",
        "pharmgkb.org",
        "pubmed.ncbi.nlm.nih.gov",
        "ncbi.nlm.nih.gov",
        "nih.gov",
    },
}


def build_simple_search_queries(
    *,
    query: str,
    question_type: str,
    candidate_entities: Sequence[str] | None = None,
) -> List[Dict[str, str]]:
    queries: List[Dict[str, str]] = []

    if question_type == "pharmacogenomics":
        queries.append(
            {
                "query": query.strip(),
                "purpose": "authority-first PGx guidance",
                "source": "pubmed",
            }
        )
    elif question_type in {"labeling", "adr", "ddi", "ddi_mechanism"}:
        queries.append(
            {
                "query": query.strip(),
                "purpose": "authority-first labeling and safety context",
                "source": "pubmed",
            }
        )
    else:
        queries.append(
            {
                "query": query.strip(),
                "purpose": "authority-first biomedical evidence",
                "source": "pubmed",
            }
        )

    queries.append(
        {
            "query": query,
            "purpose": "supplemental authority web evidence",
            "source": "duckduckgo",
        }
    )

    seen = set()
    unique_queries: List[Dict[str, str]] = []
    for query_info in queries:
        key = (query_info["query"], query_info["source"])
        if key in seen:
            continue
        seen.add(key)
        unique_queries.append(query_info)
    return unique_queries


def filter_results_for_question_type(
    question_type: str,
    results: Iterable[Dict[str, str]],
) -> List[Dict[str, str]]:
    normalized_type = str(question_type or "").strip().lower()
    results_list = list(results)
    if not results_list:
        return []

    authority_results = [
        result for result in results_list
        if is_authority_result(normalized_type, result)
    ]
    if normalized_type in HIGH_RISK_QUESTION_TYPES:
        return authority_results
    return authority_results or results_list[:5]


def is_authority_result(question_type: str, result: Dict[str, str]) -> bool:
    source = str(result.get("source", "")).strip().lower()
    if source == "pubmed":
        return True
    if source == "clinicaltrials.gov":
        return True

    domain = normalize_result_domain(result)
    if not domain:
        return False

    allowed = _AUTHORITY_DOMAINS.get(question_type) or _AUTHORITY_DOMAINS.get("mechanism", set())
    return any(domain == authority or domain.endswith(f".{authority}") for authority in allowed)


def normalize_result_domain(result: Dict[str, str]) -> str:
    url = str(result.get("url", "")).strip()
    if not url:
        metadata = result.get("metadata", {}) or {}
        url = str(metadata.get("url", "")).strip()
    if not url:
        return ""
    parsed = urlparse(url)
    return parsed.netloc.lower().removeprefix("www.")
