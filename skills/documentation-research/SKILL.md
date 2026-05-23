---
name: documentation-research
description: Fetch and cite current upstream documentation for every external dependency in scope. ISO-8601-stamped sources. Refuse memory-only references.
triggers:
  - "documentation research"
  - "fetch upstream docs"
  - "research API"
  - "verify SDK usage"
  - "library docs"
---

# documentation-research

Phase 2 of `/shannon:forge`. Grounds every external dependency claim in fetched documentation, not training-data recall.

## Behavior contract

Produces `e2e-evidence/<run-id>/documentation-research/` containing:

1. `sources/` — raw markdown of each fetched documentation page, with `<source>-<ISO-8601-timestamp>.md` naming.
2. `SUMMARY.md` — citing 3-5 verified facts per source, each linking to the local `sources/` filename.
3. `README.md` + `INDEX.md`.

## Methodology

For each external dependency identified by `codebase-analysis`:

1. Prefer `context7` MCP for library docs (current, version-aware).
2. Fall back to `WebFetch` against the canonical docs URL.
3. Save the raw markdown to `sources/<lib>-<timestamp>.md`.
4. In `SUMMARY.md`, write 3-5 facts with `[source: sources/<file>]` inline citations.

## When to use

- Phase 2 of `/shannon:forge`.
- Before any SDK / API integration.
- When training data may be stale (recently released libraries, breaking changes in current major).

## When NOT to use

- Pure internal-codebase work with no external deps.
- Already-fetched docs < 7 days old (cite the existing source file instead).

## Iron rules

- **Refuse memory-only references.** Every external-fact claim must cite a `sources/` file.
- **ISO-8601 timestamps mandatory.** Stale docs are surfaced, not silently used.
- **No invented URLs.** WebFetch only against URLs the user provided or context7 returned.
