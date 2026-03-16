# DrugClaw Remediation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the highest-risk security and runtime defects in DrugClaw, restore truthful CLI and graph-mode behavior, and make the project testable and maintainable.

**Architecture:** The remediation is split into three workstreams: execution safety, runtime correctness, and verification/tooling. Each workstream is shipped as small test-first changes so the system stays runnable after every commit and the riskiest defects are retired first.

**Tech Stack:** Python 3.12, pytest, argparse, LangGraph, OpenAI-compatible client, local resource-backed skill registry

---

## File Structure

**Existing files to modify**
- `drugclaw/agent_coder.py`: tighten generated-code execution policy and add explicit safe/unsafe modes.
- `drugclaw/config.py`: add remediation-era defaults for graph iteration, code execution, and log format.
- `drugclaw/query_logger.py`: replace unsafe pickle usage with safe structured storage.
- `drugclaw/agent_retriever.py`: stop loading historical priors from pickle; read safe structured history instead.
- `drugclaw/agent_reflector.py`: fix iteration stopping semantics.
- `drugclaw/cli.py`: lazy-load heavy runtime paths so `list` and `doctor` work in degraded environments.
- `drugclaw/main_system.py`: align runtime wiring with new config flags and log interfaces.
- `skills/base.py`: make local/data-backed availability reflect real resource readiness.
- `skills/__init__.py`: keep registry construction aligned with stricter availability checks.
- `README.md`: document the new safety model, doctor behavior, and resource readiness contract.

**Files to create**
- `tests/security/test_agent_coder_security.py`: regression tests for codegen execution restrictions and fallback behavior.
- `tests/logging/test_query_logger.py`: structured-log persistence tests and malicious-input regression coverage.
- `tests/system/test_graph_iteration.py`: graph-mode iteration and stop-condition tests.
- `tests/cli/test_cli.py`: lazy-import and degraded-environment CLI tests.
- `tests/skills/test_registry_availability.py`: availability/readiness tests for local and dataset skills.
- `tests/tools/test_smoke_scripts.py`: collection sanity tests for migrated smoke checks.
- `.github/workflows/pytest.yml`: CI for the new pytest-backed suite.

**Files to retire or reduce in importance**
- `tools/test_skills_66_68.py`: convert into assertion-based pytest coverage or keep only as a manual helper.

---

## Chunk 1: Safety Hardening

### Task 1: Disable Unsafe Arbitrary Code Execution by Default

**Files:**
- Modify: `drugclaw/agent_coder.py`
- Modify: `drugclaw/config.py`
- Modify: `drugclaw/main_system.py`
- Modify: `README.md`
- Test: `tests/security/test_agent_coder_security.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_generate_and_execute_skips_codegen_when_disabled(fake_registry, fake_llm):
    agent = CoderAgent(fake_llm, fake_registry, allow_codegen=False)
    result = agent.generate_and_execute(["UnsafeSkill"], {"drug": ["aspirin"]}, "query")
    assert result["per_skill"]["UnsafeSkill"]["mode"] == "template"
    assert "codegen disabled" in result["per_skill"]["UnsafeSkill"]["error"]


def test_safe_builtins_do_not_expose_open_or_os():
    safe = CoderAgent._safe_builtins()
    assert "open" not in safe
    with pytest.raises(ImportError):
        safe["__import__"]("os")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/security/test_agent_coder_security.py -q`
Expected: FAIL because `CoderAgent` currently always falls back to LLM-generated code and exposes `open` plus `os`.

- [ ] **Step 3: Write minimal implementation**

```python
class CoderAgent:
    def __init__(self, llm_client, skill_registry, allow_codegen: bool = False):
        self.allow_codegen = allow_codegen

    def generate_and_execute(...):
        if (error or not output.strip()) and not self.allow_codegen:
            error = "codegen disabled by configuration"
            execution_mode = "template"
```

```python
def _safe_builtins() -> Dict[str, Any]:
    allowed_import_roots = {"json", "csv", "re", "math", "statistics", "typing"}
    allowed_names = {"Exception", "ValueError", "TypeError", "len", "range", "min", "max", "sum", "sorted", "set", "list", "dict", "tuple", "str", "int", "float", "bool", "enumerate", "zip", "any", "all", "abs", "print"}
```

- [ ] **Step 4: Thread the config through runtime**

Run: edit `drugclaw/config.py` and `drugclaw/main_system.py`
Expected:
- `Config` exposes `ALLOW_CODEGEN_EXECUTION = False`
- `DrugClawSystem` passes the flag into `CoderAgent`
- `README.md` states that template retrieval is default and codegen is opt-in only

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/security/test_agent_coder_security.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add drugclaw/agent_coder.py drugclaw/config.py drugclaw/main_system.py README.md tests/security/test_agent_coder_security.py
git commit -m "fix: disable unsafe codegen execution by default"
```

### Task 2: Replace Pickle-Based Query Logs with Safe Structured Storage

**Files:**
- Modify: `drugclaw/query_logger.py`
- Modify: `drugclaw/agent_retriever.py`
- Modify: `drugclaw/main_system.py`
- Modify: `README.md`
- Test: `tests/logging/test_query_logger.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_query_logger_persists_detailed_log_as_json(tmp_path):
    logger = QueryLogger(log_dir=tmp_path)
    query_id = logger.log_query("q", {"answer": "a", "success": True, "retrieved_content": []})
    detailed = tmp_path / "detailed_logs" / f"{query_id}.json"
    assert detailed.exists()


def test_historical_skill_scores_ignore_non_json_payloads(tmp_path):
    (tmp_path / "query_logs" / "detailed_logs").mkdir(parents=True)
    retriever = RetrieverAgent(fake_llm, fake_registry)
    assert retriever._load_historical_skill_scores() == {}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/logging/test_query_logger.py -q`
Expected: FAIL because detailed logs are currently `.pkl` and retriever loads them with `pickle.load`.

- [ ] **Step 3: Write minimal implementation**

```python
payload = {
    "query_id": query_id,
    "timestamp": timestamp.isoformat(),
    "query": query,
    "full_result": result,
    "metadata": metadata or {},
}
detailed_file = self.pickle_log_dir / f"{query_id}.json"
detailed_file.write_text(json.dumps(payload, ensure_ascii=False, default=str))
```

```python
for path in files:
    payload = json.loads(path.read_text())
```

- [ ] **Step 4: Add compatibility and quarantine behavior**

Run: edit `drugclaw/query_logger.py`
Expected:
- old `.pkl` files are ignored or moved aside, never deserialized
- helper methods read `.json`
- any migration script is one-way and JSON-only

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/logging/test_query_logger.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add drugclaw/query_logger.py drugclaw/agent_retriever.py drugclaw/main_system.py README.md tests/logging/test_query_logger.py
git commit -m "fix: replace pickle query logs with structured json logs"
```

## Chunk 2: Runtime Correctness

### Task 3: Restore Real Multi-Iteration Graph Behavior

**Files:**
- Modify: `drugclaw/config.py`
- Modify: `drugclaw/agent_reflector.py`
- Modify: `drugclaw/main_system.py`
- Modify: `README.md`
- Test: `tests/system/test_graph_iteration.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_graph_mode_allows_second_iteration_when_reflection_requests_continue():
    config = make_config(max_iterations=2)
    state = AgentState(original_query="q")
    state.iteration = 0
    reflected = reflector.execute(state)
    assert reflected.should_continue is True
    assert reflected.max_iterations_reached is False


def test_graph_mode_stops_after_configured_iteration_limit():
    config = make_config(max_iterations=1)
    state = AgentState(original_query="q")
    state.iteration = 1
    reflected = reflector.execute(state)
    assert reflected.should_continue is False
    assert reflected.max_iterations_reached is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/system/test_graph_iteration.py -q`
Expected: FAIL because `MAX_ITERATIONS` defaults to `0` and the reflector stops immediately.

- [ ] **Step 3: Write minimal implementation**

```python
self.MAX_ITERATIONS = 2
```

```python
max_iterations_reached = state.iteration >= max(self.config.MAX_ITERATIONS, 1)
```

- [ ] **Step 4: Align docs and result reporting**

Run: edit `README.md` and `drugclaw/main_system.py`
Expected:
- README accurately describes default graph iteration count
- query result includes truthful iteration count semantics

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/system/test_graph_iteration.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add drugclaw/config.py drugclaw/agent_reflector.py drugclaw/main_system.py README.md tests/system/test_graph_iteration.py
git commit -m "fix: restore graph iteration semantics"
```

### Task 4: Make `list` and `doctor` Work Without Full Runtime Dependencies

**Files:**
- Modify: `drugclaw/cli.py`
- Modify: `drugclaw/__main__.py`
- Modify: `README.md`
- Test: `tests/cli/test_cli.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_list_command_does_not_import_langgraph(monkeypatch):
    monkeypatch.setitem(sys.modules, "langgraph", None)
    assert main(["list"]) == 0


def test_doctor_reports_missing_langgraph_instead_of_crashing(monkeypatch):
    monkeypatch.setitem(sys.modules, "langgraph", None)
    assert main(["doctor", "--key-file", "navigator_api_keys.example.json"]) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_cli.py -q`
Expected: FAIL because `drugclaw.cli` imports `DrugClawSystem` at module import time.

- [ ] **Step 3: Write minimal implementation**

```python
def _build_system(key_file: str) -> DrugClawSystem:
    from .main_system import DrugClawSystem
    config = Config(key_file=key_file)
    return DrugClawSystem(config)
```

```python
def _doctor_check_imports():
    try:
        import langgraph
    except Exception as exc:
        ...
```

- [ ] **Step 4: Keep first-run UX truthful**

Run: edit `README.md`
Expected:
- `list` and `doctor` are documented as safe entrypoints before full dependency installation
- missing imports are reported as doctor failures, not hard crashes

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/cli/test_cli.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add drugclaw/cli.py drugclaw/__main__.py README.md tests/cli/test_cli.py
git commit -m "fix: lazy-load cli runtime dependencies"
```

### Task 5: Make Skill Availability Reflect Real Data Readiness

**Files:**
- Modify: `skills/base.py`
- Modify: `skills/__init__.py`
- Modify: `drugclaw/cli.py`
- Modify: `README.md`
- Test: `tests/skills/test_registry_availability.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_local_file_skill_without_config_is_unavailable():
    skill = TTDSkill({"drug_target_tsv": ""})
    assert skill.is_available() is False


def test_dataset_skill_without_existing_path_is_unavailable():
    skill = WebMDReviewsSkill({})
    assert skill.is_available() is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/skills/test_registry_availability.py -q`
Expected: FAIL because those skills currently return `_implemented` regardless of missing resources.

- [ ] **Step 3: Write minimal implementation**

```python
def is_available(self) -> bool:
    if not self._implemented:
        return False
    readiness = self.planner_local_data_ready()
    return readiness is not False
```

- [ ] **Step 4: Surface unavailability in registry and doctor output**

Run: edit `skills/base.py`, `skills/__init__.py`, `drugclaw/cli.py`
Expected:
- planner profile includes `unavailable_reason`
- doctor output distinguishes `implemented but missing local data`
- selection prompts stop advertising empty local skills as ready

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/skills/test_registry_availability.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add skills/base.py skills/__init__.py drugclaw/cli.py README.md tests/skills/test_registry_availability.py
git commit -m "fix: make skill availability data-aware"
```

## Chunk 3: Verification and Tooling

### Task 6: Convert Smoke Scripts into Real Pytest Assertions

**Files:**
- Modify: `tools/test_skills_66_68.py`
- Create: `tests/tools/test_smoke_scripts.py`
- Modify: `README.md`

- [ ] **Step 1: Write the failing test**

```python
def test_pytest_collection_finds_more_than_manual_returning_tests(pytester):
    result = pytester.runpytest("--collect-only", "-q")
    result.stdout.fnmatch_lines(["*tests/tools/test_smoke_scripts.py::*"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/tools/test_smoke_scripts.py -q`
Expected: FAIL because the current smoke script lives only in `tools/` and its test functions return `SkillReport` objects.

- [ ] **Step 3: Write minimal implementation**

```python
def test_kegg_smoke():
    report = run_kegg_smoke()
    assert report.status == "PASS", report.problems_found
```

- [ ] **Step 4: Remove the collection warnings**

Run: `pytest --maxfail=1 -q`
Expected:
- no `PytestReturnNotNoneWarning`
- migrated smoke tests still expose detailed failure reasons through assertions

- [ ] **Step 5: Commit**

```bash
git add tools/test_skills_66_68.py tests/tools/test_smoke_scripts.py README.md
git commit -m "test: convert manual smoke scripts into pytest assertions"
```

### Task 7: Add CI for the New Safety and Runtime Regression Suite

**Files:**
- Create: `.github/workflows/pytest.yml`
- Modify: `README.md`

- [ ] **Step 1: Write the workflow**

```yaml
name: pytest
on:
  pull_request:
  push:
    branches: [main]
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e . --no-build-isolation pytest
      - run: pytest tests -q
```

- [ ] **Step 2: Run workflow-equivalent commands locally**

Run: `pip install -e . --no-build-isolation pytest && pytest tests -q`
Expected: PASS for the new targeted suite

- [ ] **Step 3: Document the supported test entrypoints**

Run: edit `README.md`
Expected:
- contributors know to use `pytest tests -q`
- legacy `tools/` scripts are documented as optional/manual only if they remain

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/pytest.yml README.md
git commit -m "ci: add pytest regression workflow"
```

## Acceptance Criteria

- `drugclaw list` works without `langgraph` installed.
- `drugclaw doctor` reports missing imports and missing local resources without crashing.
- default runtime does not execute LLM-generated Python.
- no production path uses `pickle.load` on project-managed query history.
- graph mode can run more than one iteration when configured to do so.
- local-file and dataset skills are only advertised as available when their resources exist.
- pytest collects the real regression suite under `tests/` and runs without `PytestReturnNotNoneWarning`.
- CI runs the remediation suite on every push and pull request.

## Execution Order

1. Chunk 1 first: retire the largest security risks before improving behavior.
2. Chunk 2 second: restore truthful runtime semantics and operator UX.
3. Chunk 3 last: lock the fixes in with enforceable tests and CI.

## Notes for the Implementer

- Do not broaden scope into new retrieval features during remediation.
- Prefer additive compatibility shims over destructive migrations unless the old behavior is explicitly unsafe.
- If any existing query logs contain only pickle payloads, quarantine them rather than loading them.
- Keep each task independently shippable; do not batch multiple chunks into one commit.
