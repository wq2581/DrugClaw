"""
Retriever Agent — constrained retrieval planning + delegation to the Code Agent.

This version adds a planning layer before the LLM selection step:
  1. classify the query into a task family
  2. rank candidate skills using hard signals
     (availability, task fit, local-data readiness, access mode, historical usage)
  3. let the LLM choose only from the top-k candidates
  4. delegate actual querying to the Code Agent
"""
from pathlib import Path
import pickle
from typing import List, Dict, Any, Optional

from .models import AgentState
from .llm_client import LLMClient
from .skills.registry import SkillRegistry
from .agent_coder import CoderAgent


class RetrieverAgent:
    """
    Agent responsible for selecting skills and orchestrating retrieval.

    Uses LLM to navigate the 15-subcategory skill tree, then hands off
    to the Code Agent for actual querying.  Results come back as text.
    """

    def __init__(
        self,
        llm_client: LLMClient,
        skill_registry: SkillRegistry,
        coder_agent: Optional[CoderAgent] = None,
    ):
        self.llm = llm_client
        self.skill_registry = skill_registry
        self.coder = coder_agent or CoderAgent(llm_client, skill_registry)
        self._history_skill_scores = self._load_historical_skill_scores()

    # ------------------------------------------------------------------
    # Prompt builders
    # ------------------------------------------------------------------

    def get_system_prompt(self) -> str:
        """System prompt for skill selection."""
        tree_ctx = self.skill_registry.skill_tree_prompt
        return f"""You are the Retriever Agent of DrugClaw — a drug-specialized agentic RAG system covering 68 curated drug knowledge resources across 15 subcategories (DTI, ADR, DDI, drug mechanisms, pharmacogenomics, drug ontology, drug labeling, drug repurposing, drug toxicity, drug combinations, drug molecular properties, drug-disease associations, drug knowledge bases, drug reviews, and drug NLP datasets).

Your role is to:
1. Analyze the user's drug-related query
2. Navigate the 15-subcategory Skill Tree to select the most relevant resources
3. Extract key entities (drugs, genes, diseases, pathways) from the query
4. Decide which skills to query

---
{tree_ctx}
---

Each skill is marked:
  ✓ = implemented and available to call
  ○ = catalogued but not yet available (do NOT include in query_plan)

Skills also show their access mode:
  [CLI]        — Python package CLI (preferred; auto-detected if installed)
  [LOCAL_FILE] — requires pre-downloaded local data file under resources_metadata/
  [DATASET]    — benchmark dataset (mask when evaluating on it)
  (no tag)     — public REST/GraphQL API (always available)

For [LOCAL_FILE] skills, follow this policy:
- First prefer files already present in the local repository under resources_metadata/
- If a file is missing, prefer the curated mirror dataset `Mike2481/DrugClaw_resources_data`
- Do not assume the original upstream download URL is still alive unless the user explicitly asks to verify it
- If neither local nor mirrored data is available, avoid selecting that skill unless it is essential and you note the dependency clearly

Navigation strategy by subcategory:
- Drug targets, bioactivity, binding              → [dti]
- Side effects, pharmacovigilance                 → [adr]
- General drug info, encyclopedias, KGs           → [drug_knowledgebase]
- Mechanism of action paths                       → [drug_mechanism]
- FDA labels, prescribing info, dosing            → [drug_labeling]
- Drug codes, ATC, RxNorm, ontologies             → [drug_ontology]
- New indications, repositioning                  → [drug_repurposing]
- Variant-drug, PGx guidelines                   → [pharmacogenomics]
- Polypharmacy, drug interactions                 → [ddi]
- Hepatotoxicity, DILI, organ tox                → [drug_toxicity]
- Synergy, combination therapy                    → [drug_combination]
- QSAR, cell-line sensitivity, IC50              → [drug_molecular_property]
- Disease-drug semantic associations              → [drug_disease]
- Patient reviews, real-world effectiveness       → [drug_review]
- NLP corpora, relation extraction                → [drug_nlp]

Only select skills marked ✓ in your query_plan.
Respond with a structured plan for retrieval."""

    def get_query_planning_prompt(
        self,
        query: str,
        omics_constraints: str,
        iteration: int,
        task_plan: Dict[str, Any],
        candidate_skills: List[Dict[str, Any]],
    ) -> str:
        candidate_lines = "\n".join(
            (
                f"- {item['name']} | score={item['score']:.2f} | "
                f"subcategory={item['subcategory']} | access={item['access_mode']} | "
                f"evidence={item['evidence_type']} | local_ready={item['local_data_ready']} | "
                f"why={item['reason']}"
            )
            for item in candidate_skills
        ) or "- No ranked candidates available."
        return f"""Query: {query}

Biological Constraints:
{omics_constraints}

Task Classification:
- primary_task: {task_plan["primary_task"]}
- task_tags: {", ".join(task_plan["task_tags"]) or "none"}
- rationale: {task_plan["reasoning"]}

Top-ranked candidate skills (choose only from this list unless there is a compelling reason):
{candidate_lines}

Current Iteration: {iteration}

Use the Skill Tree in the system prompt, but constrain your final skill choice to
the ranked candidates above. Prefer the highest-ranked candidates unless the query
clearly needs broader coverage or cross-category evidence.

Provide your plan in JSON format:
{{
    "key_entities": {{
        "drugs": ["drug1", "drug2"],
        "genes": ["gene1", "gene2"],
        "diseases": ["disease1"],
        "pathways": ["pathway1"],
        "other": []
    }},
    "highly_related_entities": {{
        "drugs": ["related_drug1"],
        "genes": ["related_gene1"],
        "diseases": ["related_disease1"],
        "pathways": [],
        "other": []
    }},
    "selected_skills": ["ChEMBL", "DGIdb"],
    "reasoning": "Explain how the task family and ranked candidates shaped the final selection"
}}"""

    # ------------------------------------------------------------------
    # Main execute
    # ------------------------------------------------------------------

    def execute(self, state: AgentState) -> AgentState:
        """
        Execute retrieval step:
          1. Plan (LLM selects skills + extracts entities)
          2. Delegate to Code Agent for actual querying
          3. Store results as text in state.retrieved_text
        """
        print(f"\n[Retriever Agent] Iteration {state.iteration}")
        resource_filter = getattr(state, "resource_filter", [])
        if resource_filter:
            print(f"[Retriever Agent] resource_filter={resource_filter}")

        # Prepare omics constraints string
        omics_str = self._format_omics_constraints(state.omics_constraints)

        if resource_filter:
            query_plan = self._get_query_plan_filtered(
                state.original_query, omics_str, state.iteration, resource_filter,
            )
        else:
            query_plan = self._get_query_plan(
                state.original_query, omics_str, state.iteration,
            )

        # Extract info from the plan
        key_entities = query_plan.get("key_entities", {})
        selected_skills = query_plan.get("selected_skills", [])

        # Backward compat: also check query_plan list for skill names
        if not selected_skills:
            selected_skills = [
                step.get("database", "")
                for step in query_plan.get("query_plan", [])
                if step.get("database")
            ]

        print(f"[Retriever Agent] Task family: {query_plan.get('task_plan', {}).get('primary_task', 'unknown')}")
        print(f"[Retriever Agent] Selected skills: {selected_skills}")
        print(f"[Retriever Agent] Key entities: {key_entities}")

        # Normalize entities for Code Agent
        entities: Dict[str, List[str]] = {}
        for etype in ("drugs", "genes", "diseases", "pathways", "other"):
            vals = key_entities.get(etype, [])
            if isinstance(vals, str):
                vals = [vals]
            if vals:
                # Map plural to singular for consistency
                singular = etype.rstrip("s") if etype != "other" else "other"
                entities[singular] = vals

        # Delegate to Code Agent
        coder_result = self.coder.generate_and_execute(
            skill_names=selected_skills,
            entities=entities,
            query=state.original_query,
        )

        # Build a combined context string with query + entities + results
        context_parts = [
            f"Query: {state.original_query}",
            f"Task Plan: {query_plan.get('task_plan', {})}",
            f"Candidate Skills: {query_plan.get('candidate_skills', [])}",
            f"Key Entities: {key_entities}",
            f"Skills Used: {selected_skills}",
            "",
            coder_result["text"],
        ]

        # Include history if available
        if state.reasoning_steps:
            last_step = state.reasoning_steps[-1]
            context_parts.insert(
                3,
                f"Previous iteration answer (preview): "
                f"{last_step.intermediate_answer[:300]}...",
            )

        retrieved_text = "\n".join(context_parts)

        # Update state
        state.current_query_entities = key_entities
        state.retrieved_text = retrieved_text
        state.code_agent_code = "\n---\n".join(
            f"# Skill: {name}\n{info.get('code', '')}"
            for name, info in coder_result.get("per_skill", {}).items()
        )

        # Also populate retrieved_content for backward compat (flat list)
        # Parse from coder results if needed
        state.retrieved_content = self._text_to_retrieved_content(
            coder_result, selected_skills,
        )

        print(f"[Retriever Agent] Retrieved {len(retrieved_text)} chars of text")
        print(f"[Retriever Agent] {len(state.retrieved_content)} backward-compat records")

        return state

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _format_omics_constraints(self, constraints) -> str:
        if constraints is None:
            return "No specific biological constraints provided."
        parts = []
        if constraints.gene_sets:
            parts.append(f"Genes: {', '.join(constraints.gene_sets[:10])}")
        if constraints.pathway_sets:
            parts.append(f"Pathways: {', '.join(constraints.pathway_sets[:10])}")
        if constraints.disease_terms:
            parts.append(f"Diseases: {', '.join(constraints.disease_terms)}")
        if constraints.tissue_types:
            parts.append(f"Tissues: {', '.join(constraints.tissue_types)}")
        return "\n".join(parts) if parts else "No specific constraints."

    def _get_query_plan(
        self, query: str, omics_str: str, iteration: int,
    ) -> Dict[str, Any]:
        """Classify the task, rank candidate skills, then let the LLM select from top-k."""
        task_plan = self._classify_task(query, omics_str)
        candidates = self._rank_candidate_skills(query, task_plan)
        top_k = candidates[:6]

        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": self.get_query_planning_prompt(
                query, omics_str, iteration, task_plan=task_plan, candidate_skills=top_k,
            )},
        ]
        try:
            plan = self.llm.generate_json(messages)
            plan["task_plan"] = task_plan
            plan["candidate_skills"] = top_k
            plan["selected_skills"] = self._filter_selected_skills(
                plan.get("selected_skills", []), top_k,
            )
            if not plan["selected_skills"]:
                plan["selected_skills"] = [item["name"] for item in top_k[:3]]
            return plan
        except Exception as e:
            print(f"[Retriever Agent] Error generating plan: {e}")
            return {
                "key_entities": {"drugs": [], "genes": [], "diseases": [], "pathways": []},
                "task_plan": task_plan,
                "candidate_skills": top_k,
                "selected_skills": [item["name"] for item in top_k[:3]],
                "reasoning": "Fallback plan due to LLM error",
            }

    def _get_query_plan_filtered(
        self, query: str, omics_str: str, iteration: int,
        resource_filter: List[str],
    ) -> Dict[str, Any]:
        """Build a plan forcing the specified skills (skip LLM skill selection)."""
        entity_prompt = f"""Extract drug/gene/disease/pathway entities from this query for retrieval.
Query: {query}
Biological Constraints: {omics_str}

Respond in JSON:
{{
  "drugs": ["drugA"],
  "genes": ["geneA"],
  "diseases": ["diseaseA"],
  "pathways": [],
  "other": []
}}"""
        try:
            entities = self.llm.generate_json([{"role": "user", "content": entity_prompt}])
        except Exception:
            entities = {"drugs": [], "genes": [], "diseases": [], "pathways": []}

        return {
            "key_entities": entities,
            "task_plan": {
                "primary_task": "resource_filter",
                "task_tags": [],
                "reasoning": "resource_filter bypassed automatic planning",
            },
            "candidate_skills": [
                {"name": name, "score": 1.0, "reason": "resource_filter", "subcategory": "", "access_mode": "", "evidence_type": "", "local_data_ready": None}
                for name in resource_filter
            ],
            "selected_skills": resource_filter,
            "reasoning": f"resource_filter active: using {resource_filter}",
        }

    def _classify_task(self, query: str, omics_str: str) -> Dict[str, Any]:
        q = f"{query}\n{omics_str}".lower()
        task_rules = [
            ("ddi", ["interaction", "interact", "polypharmacy", "coadmin", "co-administer"]),
            ("adr", ["adverse", "side effect", "toxicity", "hepatotoxic", "safety", "dili"]),
            ("drug_labeling", ["label", "prescribing", "boxed warning", "dosage", "dose", "contraindication"]),
            ("pharmacogenomics", ["pgx", "pharmacogen", "genotype", "variant", "cpic", "metabolizer", "cyp2d6", "cyp2c19"]),
            ("drug_repurposing", ["repurpos", "reposition", "new indication"]),
            ("drug_mechanism", ["mechanism", "pathway", "moa", "signaling"]),
            ("drug_ontology", ["atc", "rxnorm", "ontology", "classification", "ingredient", "synonym"]),
            ("drug_review", ["review", "patient report", "experience", "effectiveness"]),
            ("drug_molecular_property", ["ic50", "sensitivity", "cell line", "gdsc"]),
            ("drug_disease", ["disease association", "semantic association"]),
            ("dti", ["target", "bind", "binding", "bioactivity", "ki", "kd", "ec50", "inhibit"]),
        ]

        matched = []
        for task, keywords in task_rules:
            if any(keyword in q for keyword in keywords):
                matched.append(task)

        if len(set(matched)) >= 2:
            primary = "multi_hop"
        elif matched:
            primary = matched[0]
        else:
            primary = "drug_knowledgebase"

        return {
            "primary_task": primary,
            "task_tags": sorted(set(matched)),
            "reasoning": (
                "keyword-driven task classification"
                if matched else
                "fallback to drug_knowledgebase due to weak task cues"
            ),
        }

    def _rank_candidate_skills(self, query: str, task_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        keyword_suggestions = set(self.skill_registry.get_skills_for_query(query))
        primary_task = task_plan.get("primary_task", "drug_knowledgebase")
        task_tags = set(task_plan.get("task_tags", []))

        ranked = []
        for profile in self.skill_registry.get_planner_profiles():
            score = 0.0
            reasons = []

            if not profile["available"]:
                continue

            score += 4.0
            reasons.append("available")

            if profile["subcategory"] == primary_task:
                score += 3.0
                reasons.append("primary task fit")
            elif profile["subcategory"] in task_tags:
                score += 2.0
                reasons.append("secondary task fit")
            elif primary_task == "multi_hop":
                score += 1.0
                reasons.append("multi-hop coverage")

            if profile["name"] in keyword_suggestions:
                score += 1.5
                reasons.append("keyword matched")

            local_ready = profile.get("local_data_ready")
            if local_ready is True:
                score += 1.0
                reasons.append("local data ready")
            elif local_ready is False:
                score -= 1.5
                reasons.append("local data missing")

            evidence_bonus = {
                "curated_database": 1.0,
                "knowledge_graph": 0.8,
                "api": 0.7,
                "dataset": 0.2,
                "web_search": 0.3,
            }
            score += evidence_bonus.get(profile["evidence_type"], 0.0)

            score += self._access_mode_score(profile["access_mode"])

            historical = self._history_skill_scores.get(primary_task, {}).get(profile["name"], 0.0)
            if historical:
                score += min(historical, 2.0)
                reasons.append(f"historical={historical:.2f}")

            ranked.append({
                **profile,
                "score": score,
                "reason": ", ".join(reasons[:4]) or "default",
            })

        ranked.sort(key=lambda item: (-item["score"], item["name"]))
        return ranked

    @staticmethod
    def _access_mode_score(access_mode: str) -> float:
        return {
            "CLI": 0.9,
            "REST_API": 0.8,
            "LOCAL_FILE": 0.7,
            "DATASET": 0.2,
        }.get(access_mode, 0.0)

    @staticmethod
    def _filter_selected_skills(selected: List[str], candidates: List[Dict[str, Any]]) -> List[str]:
        allowed = {item["name"] for item in candidates}
        if isinstance(selected, str):
            selected = [selected]
        return [name for name in selected if name in allowed]

    def _load_historical_skill_scores(self) -> Dict[str, Dict[str, float]]:
        """
        Infer lightweight skill priors from logged successful runs.

        We do not yet log explicit selected_skills, so this uses the source field
        from retrieved_content in detailed query logs as a proxy.
        """
        log_dir = Path("query_logs") / "detailed_logs"
        if not log_dir.exists():
            return {}

        scores: Dict[str, Dict[str, float]] = {}
        files = sorted(log_dir.glob("*.pkl"))[-200:]
        for path in files:
            try:
                with open(path, "rb") as fh:
                    payload = pickle.load(fh)
            except Exception:
                continue

            result = payload.get("full_result", {})
            if not result.get("success"):
                continue

            task = self._classify_task(payload.get("query", ""), "")["primary_task"]
            task_scores = scores.setdefault(task, {})
            reward = float(result.get("final_reward", 0.5) or 0.5)
            for item in result.get("retrieved_content", []):
                source = item.get("source")
                if source:
                    task_scores[source] = task_scores.get(source, 0.0) + reward

        normalized: Dict[str, Dict[str, float]] = {}
        for task, task_scores in scores.items():
            if not task_scores:
                continue
            max_score = max(task_scores.values()) or 1.0
            normalized[task] = {
                skill: round(score / max_score, 3)
                for skill, score in task_scores.items()
            }
        return normalized

    @staticmethod
    def _text_to_retrieved_content(
        coder_result: Dict[str, Any],
        skill_names: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Convert coder output to backward-compatible retrieved_content list.
        Each entry is a minimal dict with source + text.
        """
        records = []
        for skill_name in skill_names:
            info = coder_result.get("per_skill", {}).get(skill_name, {})
            output = info.get("output", "").strip()
            if output:
                records.append({
                    "source": skill_name,
                    "source_entity": "",
                    "source_type": "",
                    "target_entity": "",
                    "target_type": "",
                    "relationship": "",
                    "weight": 1.0,
                    "evidence_text": output[:2000],
                    "skill_category": "",
                })
        return records
