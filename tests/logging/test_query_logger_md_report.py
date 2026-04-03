from __future__ import annotations

import json
from pathlib import Path

from drugclaw.query_logger import QueryLogger


def _sample_result() -> dict:
    return {
        "query": "What does imatinib target?",
        "normalized_query": "What does imatinib target?",
        "resolved_entities": {"drug": ["imatinib"]},
        "input_resolution": {
            "status": "resolved",
            "canonical_drug_names": ["imatinib"],
            "alias_candidates": ["gleevec"],
            "identifier_resolution": {
                "status": "resolved",
                "detected_identifiers": [
                    {
                        "type": "chembl_id",
                        "raw_text": "CHEMBL941",
                        "normalized_value": "CHEMBL941",
                    }
                ],
                "resolved_records": [
                    {
                        "identifier_type": "chembl_id",
                        "identifier_value": "CHEMBL941",
                        "canonical_drug_name": "imatinib",
                    }
                ],
                "errors": [],
            },
        },
        "answer": "Known Targets:\n- imatinib -> ABL1",
        "mode": "simple",
        "resource_filter": ["BindingDB"],
        "iterations": 0,
        "evidence_graph_size": 0,
        "final_reward": 0.0,
        "reasoning_history": [],
        "retrieved_content": [],
        "retrieved_text": "",
        "web_search_results": [],
        "success": True,
        "final_answer_structured": {
            "summary_confidence": 0.83,
            "task_type": "mechanism",
            "final_outcome": "partial_with_weak_support",
            "diagnostics": {
                "strong_record_count": 1,
                "weak_support_count": 0,
            },
            "key_claims": [
                {
                    "claim": "Imatinib targets ABL1.",
                    "confidence": 0.83,
                    "evidence_ids": ["bindingdb:1"],
                }
            ],
            "evidence_items": [
                {
                    "evidence_id": "bindingdb:1",
                    "source_skill": "BindingDB",
                    "source_locator": "BindingDB",
                    "metadata": {
                        "source_entity": "imatinib",
                        "relationship": "targets",
                        "target_entity": "ABL1",
                    },
                    "confidence": 0.83,
                }
            ],
            "citations": ["[bindingdb:1] BindingDB — BindingDB"],
            "warnings": [],
            "limitations": [],
        },
    }


def test_query_logger_writes_md_report_when_requested(tmp_path: Path) -> None:
    logger = QueryLogger(log_dir=str(tmp_path / "query_logs"))

    query_id = logger.log_query(
        "What does imatinib target?",
        _sample_result(),
        save_md_report=True,
    )

    report_path = tmp_path / "query_logs" / query_id / "report.md"

    assert report_path.exists()
    markdown = report_path.read_text(encoding="utf-8")
    assert "# DrugClaw Query Report" in markdown
    assert "What does imatinib target?" in markdown
    assert "imatinib -> ABL1" in markdown
    assert "BindingDB" in markdown
    assert "partial_with_weak_support" in markdown


def test_query_logger_skips_md_report_when_not_requested(tmp_path: Path) -> None:
    logger = QueryLogger(log_dir=str(tmp_path / "query_logs"))

    query_id = logger.log_query(
        "What does imatinib target?",
        _sample_result(),
        save_md_report=False,
    )

    report_path = tmp_path / "query_logs" / query_id / "report.md"

    assert not report_path.exists()


def test_query_logger_persists_input_resolution_metadata(tmp_path: Path) -> None:
    logger = QueryLogger(log_dir=str(tmp_path / "query_logs"))

    query_id = logger.log_query(
        "What does Gleevec target?",
        _sample_result(),
        save_md_report=False,
    )

    metadata_path = tmp_path / "query_logs" / query_id / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    assert metadata["query"] == "What does Gleevec target?"
    assert metadata["normalized_query"] == "What does imatinib target?"
    assert metadata["resolved_entities"] == {"drug": ["imatinib"]}
    assert metadata["input_resolution"]["canonical_drug_names"] == ["imatinib"]
    assert metadata["input_resolution"]["identifier_resolution"]["resolved_records"][0]["identifier_value"] == "CHEMBL941"
