# Legacy Local Resource Path Cleanup Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove legacy machine-specific `/blue/.../DrugClaw` local-data paths from runnable skill examples and skill docs without changing the main retrieval pipeline.

**Architecture:** Keep the fix scoped to `skills/**/example.py`, `skills/**/SKILL.md`, and repository-surface regression tests. Default local-data resolution should point at this cloned repository's `resources_metadata/` tree, with existing environment-variable overrides preserved where they already exist.

**Tech Stack:** Python, pathlib, pytest, Markdown

---

## Chunk 1: Guardrails

### Task 1: Add failing repository-surface tests

**Files:**
- Modify: `tests/project/test_repository_surface.py`

- [ ] Add a repository constant for the legacy `/blue/.../DrugClaw` prefix
- [ ] Add a failing test covering `skills/**/example.py`
- [ ] Add a failing test covering `skills/**/SKILL.md`
- [ ] Run `pytest tests/project/test_repository_surface.py -q` and confirm red

## Chunk 2: Runtime example cleanup

### Task 2: Migrate runnable example paths to repo-local defaults

**Files:**
- Modify: `skills/**/example.py` files that still reference `/blue/.../DrugClaw`

- [ ] For each affected example file, replace legacy absolute defaults with repo-local path resolution based on `Path(__file__).resolve()`
- [ ] Preserve existing env-var overrides where already supported
- [ ] Keep query logic unchanged; touch path/docstring setup only
- [ ] Run `pytest tests/project/test_repository_surface.py -q` and confirm example-path guard passes

## Chunk 3: Skill docs cleanup

### Task 3: Update SKILL.md path guidance for new users

**Files:**
- Modify: `skills/**/SKILL.md` files that still reference `/blue/.../DrugClaw`

- [ ] Replace machine-specific paths with repo-local `resources_metadata/...` guidance
- [ ] Mention env-var override names where the example supports them
- [ ] Keep usage semantics unchanged
- [ ] Run `pytest tests/project/test_repository_surface.py -q` and confirm doc guard passes

## Chunk 4: Verification

### Task 4: Run targeted and full verification

**Files:**
- Verify only

- [ ] Run direct smoke checks for representative local examples
- [ ] Run `pytest tests/project/test_repository_surface.py tests/skills/test_local_resource_example_paths.py -q`
- [ ] Run `pytest -q`
- [ ] Check `git status --short`
- [ ] Only after green verification, commit and push
