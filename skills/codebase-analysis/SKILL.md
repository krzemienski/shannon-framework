---
name: codebase-analysis
description: Build repo-wide context before any modification. File inventory, module map, dependency manifests, hot-path identification. Read-only.
triggers:
  - "analyze codebase"
  - "repo context"
  - "module map"
  - "hot path identification"
  - "dependency manifest survey"
---

# codebase-analysis

Phase 1 of `/shannon:forge`. Read-only repo survey that grounds the planning phase.

## Behavior contract

Produces `e2e-evidence/<run-id>/codebase-analysis/` containing:

1. **File inventory** (`file-inventory.txt`) — all files in scope, with size + last-modified.
2. **Module map** (`module-map.md`) — directory tree with brief purpose per top-level dir.
3. **Dependency manifest survey** (`deps-summary.md`) — `package.json` / `Cargo.toml` / `pyproject.toml` parsed; flag outdated majors.
4. **Hot-path identification** (`hot-paths.md`) — entry points (CLI bins, route handlers, main functions). For each: which modules they touch most.
5. **README.md + INDEX.md** per evidence-indexing skill convention.

## Methodology

- `find` / `glob` for inventory (NOT find when searching code — Glob).
- Read top-level config files (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Gemfile`).
- Read CLAUDE.md and `docs/codebase-summary.md` if they exist.
- Grep for entry-point patterns (`#!/usr/bin/env`, `if __name__`, `func main`, `export default function`).

## When to use

- Phase 1 of `/shannon:forge`.
- Before any non-trivial refactor (`/shannon:plan` may invoke this as a prerequisite).
- Onboarding a new repo to Shannon governance.

## When NOT to use

- Single-file edit
- Documentation-only change
- Already-cached analysis < 7 days old

## Iron rules

- **Read-only.** No source modifications.
- **No invention.** Every claim in module-map / hot-paths must trace to a grepped/read file.
- **Citations specific** — file paths, not handwave.
