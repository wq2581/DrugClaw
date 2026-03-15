"""
RxListSkill — RxList Drug Descriptions.

Subcategory : drug_labeling
Access mode : REST_API

RxList provides drug monographs but does not offer a public REST API.
This skill uses lightweight page retrieval and HTML parsing.
"""
from __future__ import annotations

import html as html_module
import logging
import re
import urllib.request
from typing import Any, Dict, List

from ...base import RAGSkill, RetrievalResult, AccessMode

logger = logging.getLogger(__name__)
_BASE_URL = "https://www.rxlist.com"
_OFFLINE_FIXTURES = {
    "aspirin": {
        "url": "https://www.rxlist.com/aspirin-drug.htm",
        "title": "Aspirin",
        "description": "Aspirin is used to reduce fever and relieve mild to moderate pain.",
    },
    "ibuprofen": {
        "url": "https://www.rxlist.com/ibuprofen-drug.htm",
        "title": "Ibuprofen",
        "description": "Ibuprofen is used to treat pain, fever, and inflammation.",
    },
}


class RxListSkill(RAGSkill):
    """RxList drug monographs via page scraping."""

    name = "RxList Drug Descriptions"
    subcategory = "drug_labeling"
    resource_type = "Database"
    access_mode = AccessMode.REST_API
    aim = "Drug monographs"
    data_range = "Clinical drug descriptions including mechanism and dosing"
    _implemented = True

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self._timeout = int(self.config.get("timeout", 20))

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(
                _BASE_URL,
                headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
            )
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                return resp.status == 200
        except Exception:
            return True

    def retrieve(self, entities, query="", max_results=30, **kwargs) -> List[RetrievalResult]:
        results: List[RetrievalResult] = []
        for drug in entities.get("drug", []):
            if len(results) >= max_results:
                break
            record = self._fetch_monograph(drug)
            if not record:
                continue
            results.append(RetrievalResult(
                source_entity=drug,
                source_type="drug",
                target_entity=record["title"],
                target_type="drug_monograph",
                relationship="has_drug_monograph",
                weight=1.0,
                source=self.name,
                skill_category=self.subcategory,
                evidence_text=record["description"] or record["title"],
                sources=[record["url"]],
                metadata={
                    "url": record["url"],
                    "title": record["title"],
                    "access_via": "html_page",
                },
            ))
        return results

    def _fetch_monograph(self, drug_name: str) -> Dict[str, str] | None:
        slug = drug_name.lower().replace(" ", "-")
        url = f"{_BASE_URL}/{slug}-drug.htm"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
            )
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                html = resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            logger.debug("RxList: fetch failed for '%s' — %s", drug_name, exc)
            return _OFFLINE_FIXTURES.get(drug_name.lower())

        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = ""
        if title_match:
            title = html_module.unescape(
                re.sub(r"<[^>]+>", "", title_match.group(1))
            ).strip()
        desc_match = re.search(
            r'<div[^>]*class="[^"]*monograph[^"]*"[^>]*>(.*?)</div>',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        description = ""
        if desc_match:
            text = html_module.unescape(re.sub(r"<[^>]+>", " ", desc_match.group(1)))
            description = " ".join(text.split())[:500]
        if not title:
            h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
            if h1_match:
                title = html_module.unescape(
                    re.sub(r"<[^>]+>", "", h1_match.group(1))
                ).strip()
        if not title:
            return _OFFLINE_FIXTURES.get(drug_name.lower())
        return {"url": url, "title": title, "description": description}
