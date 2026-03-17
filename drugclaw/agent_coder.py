"""
Code Agent — generates and executes Python code to query drug knowledge skills.

Instead of forcing every skill through a rigid retrieve() → RetrievalResult pipeline,
the Code Agent reads each skill's description and example code, then writes
custom Python code to query the skill for the specific entities of interest.

The generated code is executed in a restricted namespace, and the output is
captured as a free-form string.  This "vibe coding" approach allows each skill
to be queried in its own natural way.
"""
from __future__ import annotations

import ast
import io
import signal
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Any, Dict, List, Optional

from .llm_client import LLMClient
from .skills.registry import SkillRegistry


class CoderAgent:
    """
    Agent that writes and executes Python code to query drug knowledge skills.

    Flow:
      1. Receive selected skill names + entity info from the Retriever Agent
      2. For each skill, read its description + example code
      3. Ask the LLM to write Python code that queries the skill for the
         specified entities
      4. Execute the code and capture stdout as the result string
      5. Aggregate results into a combined text block
    """

    def __init__(self, llm_client: LLMClient, skill_registry: SkillRegistry):
        self.llm = llm_client
        self.skill_registry = skill_registry

    # ------------------------------------------------------------------
    # Prompts
    # ------------------------------------------------------------------

    def get_system_prompt(self) -> str:
        return """You are the Code Agent of DrugClaw — a drug-specialized agentic RAG system.

Your role is to write Python code that queries drug knowledge resources for specific entities.

You will be given:
1. A skill's description (name, subcategory, access mode, aim)
2. Example Python code showing how to use the skill's API
3. The entities to search for (drugs, genes, diseases, pathways)
4. The original user query for context

Write a self-contained Python script that:
- Imports only standard library modules (urllib, json, csv, os) or modules already shown in the example
- Queries the skill for the specified entities
- Prints the results in a human-readable format
- Includes error handling (try/except) so the script never crashes
- Focuses on retrieving the most relevant information for the query

IMPORTANT:
- Use print() to output results — all printed text becomes the retrieval result
- Be concise but informative in the output
- Include source attribution (which database/resource the data came from)
- Handle cases where no results are found gracefully
- Do NOT use any interactive input or GUI
- Do NOT install packages or make system calls
- Keep timeouts short (10-15 seconds)
- For LOCAL_FILE skills, first look for files under this repository's `resources_metadata/`
- If a required local file is missing, mention the curated mirror `https://huggingface.co/datasets/Mike2481/DrugClaw_resources_data`
- Do not hard-code old absolute paths from legacy examples unless they are rewritten relative to the current repository

Return ONLY the Python code, no markdown formatting, no explanation."""

    def get_code_generation_prompt(
        self,
        skill_name: str,
        skill_info: str,
        entities: Dict[str, List[str]],
        query: str,
    ) -> str:
        entity_str = "\n".join(
            f"  {etype}: {', '.join(enames)}"
            for etype, enames in entities.items()
            if enames
        )
        if not entity_str:
            entity_str = "  (no specific entities extracted)"

        return f"""Write Python code to query the following skill for the given entities.

=== Skill Info ===
{skill_info}

=== Entities to Query ===
{entity_str}

=== Original Query ===
{query}

Write a Python script that queries this resource for the above entities and prints the results.
Focus on the information most relevant to answering the original query.
Return ONLY Python code."""

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def generate_and_execute(
        self,
        skill_names: List[str],
        entities: Dict[str, List[str]],
        query: str,
        max_results_per_skill: int = 30,
    ) -> Dict[str, Any]:
        """
        Generate and execute query code for each skill.

        Returns a dict with:
          - "text": combined result text (str)
          - "per_skill": dict mapping skill_name -> {"code": str, "output": str, "error": str}
        """
        all_outputs: List[str] = []
        per_skill: Dict[str, Dict[str, str]] = {}

        for skill_name in skill_names:
            print(f"[Code Agent] Generating code for skill: {skill_name}")

            # Try the code-generation path first
            skill_info = self.skill_registry.get_skill_info_for_coder(skill_name)
            code, output, error = self._generate_and_run_for_skill(
                skill_name, skill_info, entities, query,
            )

            if error and not output.strip():
                # Code-gen path failed — fallback to direct skill.retrieve()
                print(f"[Code Agent] Code execution failed for {skill_name}, "
                      f"falling back to skill.retrieve()")
                fallback_output, fallback_error = self._fallback_retrieve(
                    skill_name, entities, query, max_results_per_skill,
                )
                output = fallback_output
                error = fallback_error
                code = "(fallback: skill.retrieve())"

            per_skill[skill_name] = {
                "code": code,
                "output": output,
                "error": error,
            }

            if output.strip():
                all_outputs.append(
                    f"=== Results from {skill_name} ===\n{output.strip()}\n"
                )
            else:
                all_outputs.append(
                    f"=== Results from {skill_name} ===\n"
                    f"(no results retrieved{'; error: ' + error if error else ''})\n"
                )

        combined_text = "\n".join(all_outputs)
        return {
            "text": combined_text,
            "per_skill": per_skill,
        }

    def _generate_and_run_for_skill(
        self,
        skill_name: str,
        skill_info: str,
        entities: Dict[str, List[str]],
        query: str,
    ) -> tuple:
        """Generate code for a skill and execute it. Returns (code, output, error)."""
        # Ask LLM to write the code
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": self.get_code_generation_prompt(
                skill_name, skill_info, entities, query,
            )},
        ]
        try:
            code = self.llm.generate(messages, temperature=0.3)
        except Exception as exc:
            return "", "", f"LLM error: {exc}"

        # Clean up the code (remove markdown fences if any)
        code = self._clean_code(code)

        validation_error = self._validate_generated_code(code)
        if validation_error:
            return code, "", validation_error

        output, error = self._execute_code(code, timeout_seconds=30)
        return code, output, error

    def _fallback_retrieve(
        self,
        skill_name: str,
        entities: Dict[str, List[str]],
        query: str,
        max_results: int,
    ) -> tuple:
        """Fallback: use the skill's retrieve() method directly."""
        skill = self.skill_registry.get_skill(skill_name)
        if skill is None:
            return "", f"Skill '{skill_name}' not registered"

        try:
            results = skill.retrieve(
                entities=entities, query=query, max_results=max_results,
            )
            if not results:
                return "(no results)", ""

            lines = []
            for r in results[:max_results]:
                line = (
                    f"[{r.source}] {r.source_entity} ({r.source_type}) "
                    f"--{r.relationship}--> "
                    f"{r.target_entity} ({r.target_type})"
                )
                if r.evidence_text:
                    line += f"\n  Evidence: {r.evidence_text}"
                if r.sources:
                    line += f"\n  Sources: {', '.join(r.sources[:3])}"
                lines.append(line)
            return "\n".join(lines), ""
        except Exception as exc:
            return "", f"retrieve() error: {exc}"

    # ------------------------------------------------------------------
    # Code execution
    # ------------------------------------------------------------------

    def _execute_code(self, code: str, timeout_seconds: int = 30) -> tuple:
        """
        Execute generated Python code in a restricted namespace.

        Returns (stdout_output, error_message).
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # Build a restricted namespace with constrained imports.
        exec_globals = {
            "__builtins__": self._safe_builtins(),
            "__name__": "__coder_agent__",
        }

        def _timeout_handler(signum, frame):
            raise TimeoutError(f"generated code exceeded {timeout_seconds}s")

        previous_handler = signal.getsignal(signal.SIGALRM) if hasattr(signal, "SIGALRM") else None

        try:
            previous_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout_seconds)
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, exec_globals)
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous_handler)
            output = stdout_capture.getvalue()
            errors = stderr_capture.getvalue()
            return output, errors
        except Exception as exc:
            signal.alarm(0)
            if previous_handler is not None:
                signal.signal(signal.SIGALRM, previous_handler)
            output = stdout_capture.getvalue()
            error_msg = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
            return output, error_msg

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _clean_code(code: str) -> str:
        """Remove markdown code fences if present."""
        code = code.strip()
        if code.startswith("```python"):
            code = code[len("```python"):]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()

    @staticmethod
    def _validate_generated_code(code: str) -> str:
        """Static guardrail before executing generated code."""
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            return f"generated code is not valid Python: {exc}"

        forbidden_modules = {
            "subprocess", "socket", "ctypes", "multiprocessing",
            "pty", "resource", "shlex",
        }
        forbidden_names = {"eval", "exec", "compile", "input", "__import__"}
        forbidden_attrs = {"system", "popen", "fork", "remove", "unlink", "rmdir"}
        saw_print = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root in forbidden_modules:
                        return f"forbidden import in generated code: {root}"
            elif isinstance(node, ast.ImportFrom):
                module = (node.module or "").split(".")[0]
                if module in forbidden_modules:
                    return f"forbidden import in generated code: {module}"
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in forbidden_names:
                        return f"forbidden call in generated code: {node.func.id}"
                    if node.func.id == "print":
                        saw_print = True
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in forbidden_attrs:
                        return f"forbidden attribute call in generated code: {node.func.attr}"

        if not saw_print:
            return "generated code must print retrieval output"
        return ""

    @staticmethod
    def _safe_builtins() -> Dict[str, Any]:
        allowed_import_roots = {
            "collections", "csv", "drugclaw", "importlib", "io", "itertools",
            "json", "math", "os", "pathlib", "re", "skills", "statistics",
            "sys", "time", "typing", "urllib", "xml",
        }

        builtin_map = dict(__builtins__ if isinstance(__builtins__, dict) else __builtins__.__dict__)

        def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
            root = name.split(".")[0]
            if root not in allowed_import_roots:
                raise ImportError(f"Import of '{name}' is not allowed in generated code")
            return __import__(name, globals, locals, fromlist, level)

        allowed_names = {
            "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
            "len", "range", "min", "max", "sum", "sorted", "set", "list", "dict",
            "tuple", "str", "int", "float", "bool", "enumerate", "zip", "any",
            "all", "abs", "print", "open",
        }
        safe = {name: builtin_map[name] for name in allowed_names}
        safe["__import__"] = _safe_import
        return safe
