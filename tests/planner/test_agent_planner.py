from __future__ import annotations

from drugclaw.query_plan import build_fallback_query_plan


def test_fallback_query_plan_is_conservative() -> None:
    plan = build_fallback_query_plan("What does imatinib target?")

    assert plan.question_type == "unknown"
    assert plan.requires_graph_reasoning is False
    assert plan.preferred_skills == []
