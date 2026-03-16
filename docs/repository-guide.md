# Repository Guide

## Start Here

If you are new to DrugClaw, read `README.md` first and use the CLI from the repository root:

```bash
python -m drugclaw list
python -m drugclaw doctor
python -m drugclaw demo
```

## Top-Level Directories

### `drugclaw/`

The runtime package. This is the main place to look for the CLI, config handling, retrieval flow, and agent orchestration.

### `skills/`

Implemented skill code grouped by drug task category.

### `skillexamples/`

Resource-specific examples and compact operator notes. Useful when you want to understand how a specific skill is supposed to be queried.

### `examples/`

Optional runnable examples and compatibility wrappers. These are not the primary user entrypoints.

### `tools/`

Maintainer-oriented validation and smoke scripts for resources and skill behavior.

### `scripts/legacy/`

Historical helper scripts kept for reference. Treat these as maintainer utilities rather than supported public interfaces.

### `resources_metadata/`

Local datasets and curated fixtures used by `LOCAL_FILE` skills and tests.

### `support/`

Project images and visual assets used in the README and related docs.

## Runtime Surface vs Support Material

The main runtime surface is:

- `drugclaw/`
- `python -m drugclaw ...`
- `drugclaw ...` after editable install

Support material includes:

- `examples/`
- `skillexamples/`
- `tools/`
- `scripts/legacy/`
- `docs/`

## Contributor Orientation

If you are debugging the package behavior, start in `drugclaw/`.

If you are checking whether a skill is implemented or data-backed, look in `skills/` and `resources_metadata/`.

If you are validating a specific resource path or historical example, check `skillexamples/`, `tools/`, and `scripts/legacy/`.
