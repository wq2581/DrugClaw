from __future__ import annotations

from drugclaw.agent_retriever import RetrieverAgent
from drugclaw.models import AgentState
from drugclaw.query_plan import QueryPlan


class _PlannerBypassLLMStub:
    def generate_json(self, messages, temperature=0.3):
        raise AssertionError("Retriever should consume state.query_plan instead of re-planning")


class _CoderStub:
    def generate_and_execute(self, skill_names, entities, query, max_results_per_skill=30):
        per_skill = {}
        for skill_name in skill_names:
            per_skill[skill_name] = {
                "output": f"Results from {skill_name}",
                "records": [],
                "code": "",
            }
        return {
            "text": "\n".join(f"Results from {name}" for name in skill_names),
            "per_skill": per_skill,
        }


class _RegistryStub:
    def get_skills_for_query(self, query):
        return ["ChEMBL"]

    def get_skill(self, skill_name):
        return None

    @property
    def skill_tree_prompt(self):
        return "stub tree"


def test_retriever_consumes_query_plan_when_present() -> None:
    state = AgentState(
        original_query="What does imatinib target?",
        query_plan=QueryPlan(
            question_type="target_lookup",
            entities={"drug": ["imatinib"]},
            subquestions=["What are the known targets of imatinib?"],
            preferred_skills=["BindingDB"],
            preferred_evidence_types=["database_record"],
            requires_graph_reasoning=False,
            requires_prediction_sources=False,
            requires_web_fallback=False,
            answer_risk_level="medium",
            notes=["Use direct target databases."],
        ),
    )

    retriever = RetrieverAgent(
        _PlannerBypassLLMStub(),
        _RegistryStub(),
        coder_agent=_CoderStub(),
    )

    updated = retriever.execute(state)

    assert "BindingDB" in updated.retrieved_text
    assert updated.current_query_entities == {"drug": ["imatinib"]}


def test_retriever_prefers_resource_filter_over_query_plan_hints() -> None:
    state = AgentState(
        original_query="What does imatinib target?",
        resource_filter=["DrugBank"],
        query_plan=QueryPlan(
            question_type="target_lookup",
            entities={"drug": ["imatinib"]},
            subquestions=["What are the known targets of imatinib?"],
            preferred_skills=["BindingDB"],
            preferred_evidence_types=["database_record"],
            requires_graph_reasoning=False,
            requires_prediction_sources=False,
            requires_web_fallback=False,
            answer_risk_level="medium",
            notes=["Use direct target databases."],
        ),
    )

    retriever = RetrieverAgent(
        _PlannerBypassLLMStub(),
        _RegistryStub(),
        coder_agent=_CoderStub(),
    )

    updated = retriever.execute(state)

    assert "DrugBank" in updated.retrieved_text
    assert "BindingDB" not in updated.retrieved_text
