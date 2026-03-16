# GitHub-Facing Repository Cleanup Design

**Date:** 2026-03-16

## Goal

Make the repository easier for first-time GitHub users to understand by reducing root-level noise, removing machine-specific instructions, and clarifying the official entrypoints without breaking the current Python package and test flows.

## Problem Statement

The current repository mixes several audiences at the top level:

- new users looking for install and demo instructions
- contributors looking for package code and tests
- maintainers using one-off helper scripts and historical compatibility entrypoints

This creates three concrete problems:

1. `README.md` and `README_CN.md` still show machine-local commands such as `cd /data/boom/Agent/DrugClaw`.
2. The repository root contains a mix of package metadata, user examples, internal helper scripts, local build artifacts, and compatibility wrappers.
3. New users cannot quickly tell which files are official entrypoints and which are legacy or maintainer-only utilities.

## Constraints

- Do not rename or relocate core package paths that are already imported by runtime code.
- Do not rename `skills/`, `skillexamples/`, `tools/`, `support/`, or `resources_metadata/` in this pass.
- Preserve current CLI entrypoints: `python -m drugclaw ...` and `drugclaw ...`.
- Keep the cleanup safe enough to land alongside the ongoing remediation branch.

## Options Considered

### Option 1: Documentation-only cleanup

Update READMEs and add a repository guide, but keep the file layout unchanged.

- Pros: minimal risk
- Cons: root-level noise remains; GitHub homepage still looks cluttered

### Option 2: Moderate repository cleanup

Move obvious user examples and maintainer helper scripts into dedicated folders, update docs, and keep compatibility only where needed.

- Pros: strong GitHub-facing improvement with manageable risk
- Cons: requires path updates and verification for moved scripts

### Option 3: Deep repository reorganization

Rename broader directories such as `skillexamples/` and restructure testing/layout conventions.

- Pros: cleanest end state
- Cons: high regression risk because many docs, tests, and scripts already reference those paths

## Selected Approach

Use Option 2.

This pass will clean up the repository surface area without changing the core internal topology. The project should look more deliberate on GitHub, while runtime imports and existing broad directory conventions remain stable.

## Proposed Repository Shape

### Root should emphasize

- project metadata: `README.md`, `README_CN.md`, `pyproject.toml`
- package/runtime code: `drugclaw/`
- skill implementation trees: `skills/`, `skillexamples/`
- developer/support material: `docs/`, `tools/`, `support/`, `resources_metadata/`
- safe public template files: `navigator_api_keys.example.json`

### Root should no longer carry loose helper files

The following kinds of files should move out of the root:

- runnable examples such as `example_usage.py`
- compatibility/demo scripts such as `run_minimal.py`
- internal or historical helper scripts such as `get_reason_detail.py`
- ad hoc helper files such as `query_teamplate.py`

## Directory Strategy

### `examples/`

Use for user-facing runnable examples and convenience entrypoints.

Initial candidates:

- `example_usage.py`
- `run_minimal.py`

### `scripts/`

Use for maintainer-oriented helpers that are not part of the public package interface.

Initial candidates:

- `get_reason_detail.py`
- `query_teamplate.py`

If a helper is clearly historical or not part of supported user flows, place it under `scripts/legacy/`.

## Documentation Strategy

### README updates

Both `README.md` and `README_CN.md` should:

- remove absolute local `cd` commands
- assume the user is already in the cloned repository root
- present the official first-run path as:
  - `python -m drugclaw list`
  - `python -m drugclaw doctor`
  - `python -m drugclaw demo`
- describe `examples/` as optional exploration material rather than the main entrypoint
- explain what the major top-level directories are for

### New repository guide

Add a short doc under `docs/` that explains:

- what a new user should read first
- where examples live
- where maintainer scripts live
- which directories are core runtime surfaces vs support material

## Compatibility Rules

- Prefer updating docs and internal references to the new locations instead of keeping redundant root wrappers.
- Keep a root-level wrapper only if removing it would break an already documented supported workflow that is still worth preserving.
- Avoid changing Python import packages unless necessary; this is a repository layout cleanup, not a package rename.

## Out of Scope

- Renaming `skillexamples/`
- Renaming `tools/`
- Refactoring skill implementations for style only
- Changing resource layout under `resources_metadata/`
- Reworking the package/module structure under `drugclaw/`

## Verification Plan

At minimum, verify:

1. `pytest tests -q`
2. `python -m drugclaw list`
3. `python -m drugclaw doctor`
4. README command examples no longer depend on machine-specific absolute paths
5. The repository root reads cleanly in `ls`

## Expected Outcome

After this cleanup:

- a new GitHub visitor can identify the official entrypoints quickly
- the root directory looks intentionally organized instead of locally accumulated
- maintainer-only scripts are still present, but clearly separated from user-facing materials
- the current runtime and remediation work remain stable
