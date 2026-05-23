---
name: research
description: Parallel researcher agents on sub-topics; aggregator writes cited research summary. Standalone command, not subcommand (UQ-CMD-2).
replaces:
  - /autoresearch:autoresearch
  - /oh-my-claudecode:autoresearch
  - /ck:research
  - /deep-research:deep-research
argument-hint: "<topic> [--sources N] [--depth shallow|standard|deep]"
---

# /shannon:research

Topic research with parallel sub-agent fan-out. Separate from `/shannon:plan` — research often happens without planning a build (per UQ-CMD-2).

## Inputs

- Positional: research topic
- `--sources N` — minimum sources required (default 5)
- `--depth shallow|standard|deep` (default standard)

## Behavior

1. Decompose topic into sub-topics (3-5 typically).
2. Spawn one `researcher` agent per sub-topic in parallel via `Task`.
3. Each researcher:
   - Uses `WebFetch` and `context7` for primary sources.
   - Writes findings to `research/<topic-slug>/researcher-<N>.md` with inline citations.
4. Aggregator (`plan-author` in research mode) reads all researcher reports; writes `research/<topic-slug>/SUMMARY.md` synthesizing findings with cross-citations to researcher reports.

## Success criteria

- N+ citations across the SUMMARY.
- Every claim cites a researcher report file or external URL.
- No memory-only claims.

## Hooks fired

- Standard chain
- `subagent-governance-inject` per researcher spawn

## Skills invoked

- `research-validation`
- `sequential-analysis`

## Iron rules

- Citations always specific (URL + retrieval timestamp).
- No "according to my training data" — refuse, fetch live.

## Examples

```
/shannon:research "OAuth2 PKCE best practices 2025"
/shannon:research "Postgres logical replication for blue-green deploys" --depth deep
```
