# GitHub-Facing Repository Cleanup Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repository surface so GitHub newcomers see clear entrypoints, while preserving the current `drugclaw` package and CLI behavior.

**Architecture:** Keep the package and existing large directory boundaries stable, but move obvious root-level examples and maintainer helpers into dedicated folders. Back the cleanup with a small regression test that checks the intended top-level layout and README invariants.

**Tech Stack:** Python, pytest, Markdown documentation, git worktrees

---

## Chunk 1: Repository Surface Cleanup

### Task 1: Add a repository layout regression test

**Files:**
- Create: `tests/project/test_repository_surface.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_root_does_not_expose_legacy_helper_files():
    assert not (ROOT / "example_usage.py").exists()
    assert not (ROOT / "run_minimal.py").exists()
    assert not (ROOT / "get_reason_detail.py").exists()
    assert not (ROOT / "query_teamplate.py").exists()


def test_readme_does_not_contain_machine_specific_cd():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "cd /data/boom/Agent/DrugClaw" not in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/project/test_repository_surface.py -q`
Expected: FAIL because the root-level files still exist and `README.md` still contains the absolute path.

- [ ] **Step 3: Make pytest collect the new tests cleanly**

Update `pyproject.toml` with a minimal pytest config so `pytest tests -q` is the official regression command:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 4: Run the focused test again**

Run: `pytest tests/project/test_repository_surface.py -q`
Expected: still FAIL, but now only against the intended cleanup assertions.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml tests/project/test_repository_surface.py
git commit -m "test: add repository surface regression coverage"
```

### Task 2: Move loose root files into clear directories

**Files:**
- Create: `examples/README.md`
- Create: `examples/example_usage.py`
- Create: `examples/run_minimal.py`
- Create: `scripts/legacy/get_reason_detail.py`
- Create: `scripts/legacy/query_teamplate.py`
- Delete: `example_usage.py`
- Delete: `run_minimal.py`
- Delete: `get_reason_detail.py`
- Delete: `query_teamplate.py`
- Test: `tests/project/test_repository_surface.py`

- [ ] **Step 1: Move user-facing examples into `examples/`**

Place the current root example scripts under `examples/` and keep their behavior unchanged.

- [ ] **Step 2: Move maintainer-only helpers into `scripts/legacy/`**

Preserve the current file contents, but remove them from the root.

- [ ] **Step 3: Add a short `examples/README.md`**

Document that `examples/` contains optional runnable examples, while the supported first-run path remains `python -m drugclaw ...`.

- [ ] **Step 4: Run the focused regression test**

Run: `pytest tests/project/test_repository_surface.py -q`
Expected: PASS for the moved-file assertions, but README-related assertions may still fail until Task 3.

- [ ] **Step 5: Commit**

```bash
git add examples scripts tests/project/test_repository_surface.py
git rm example_usage.py run_minimal.py get_reason_detail.py query_teamplate.py
git commit -m "refactor: reorganize root-level examples and helper scripts"
```

## Chunk 2: Documentation and Verification

### Task 3: Rewrite GitHub-facing docs around the cleaned structure

**Files:**
- Modify: `README.md`
- Modify: `README_CN.md`
- Create: `docs/repository-guide.md`
- Test: `tests/project/test_repository_surface.py`

- [ ] **Step 1: Update `README.md`**

Make these changes:

- remove `cd /data/boom/Agent/DrugClaw`
- assume the user is already in the cloned repository root
- make `python -m drugclaw list`, `doctor`, and `demo` the primary entrypoints
- point compatibility/example material to `examples/`
- add a short top-level directory guide

- [ ] **Step 2: Update `README_CN.md`**

Mirror the same structural cleanup in Chinese.

- [ ] **Step 3: Add `docs/repository-guide.md`**

Describe:

- where new users should start
- what lives in `drugclaw/`, `skills/`, `skillexamples/`, `tools/`, `examples/`, and `scripts/legacy/`
- which paths are runtime surfaces vs support material

- [ ] **Step 4: Expand the regression test if needed**

Assert at least:

- `README_CN.md` also does not contain the absolute path
- `examples/` and `scripts/legacy/` exist

- [ ] **Step 5: Run verification**

Run: `pytest tests -q`
Expected: PASS

Run: `python -m drugclaw list`
Expected: PASS and print the quick navigation output.

Run: `python -m drugclaw doctor`
Expected: exit non-zero only for local setup issues such as missing `navigator_api_keys.json`, not for import or CLI crashes.

- [ ] **Step 6: Commit**

```bash
git add README.md README_CN.md docs/repository-guide.md tests/project/test_repository_surface.py
git commit -m "docs: make repository layout GitHub-friendly"
```
