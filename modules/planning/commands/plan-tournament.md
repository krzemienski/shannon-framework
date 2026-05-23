---
name: plan-tournament
description: Tournament-style plan generation. N parallel plan-author candidates with distinct perspectives; red-teamer per candidate; tournament-judge selects winner.
replaces:
  - /anneal-cast:anneal
argument-hint: "<problem> [--candidates N]"
---

# /shannon:plan-tournament

Spawn multiple plan candidates from distinct perspectives; red-team each; pick the winner.

## Inputs

- Positional: problem description
- `--candidates N` — number of competing plans (default 3)

## Behavior

1. Spawn N `plan-author` agents in parallel via `Task`. Each gets a distinct perspective:
   - Candidate 1: **security-first** — minimize attack surface, principle of least privilege
   - Candidate 2: **performance-first** — optimize for hot paths, latency-sensitive
   - Candidate 3: **simplicity-first** — YAGNI/KISS, minimum viable approach
   - (Candidates 4..N: configurable additional lenses)
2. Each candidate emits a complete plan to `plans/tournament-<run-id>/candidate-<N>/`.
3. For each candidate plan: spawn `red-teamer` agent against it. Red-teamer emits findings BLOCKING/HIGH/MEDIUM/LOW.
4. `plan-tournament` skill aggregates: scores plans against criteria (completeness, red-team severity, complexity), selects winner.
5. Winner plan promoted to `plans/<date>-<slug>/`. Loser plans archived under `plans/<date>-<slug>/_rejected/`.

## Success criteria

- All N candidates produced complete plans.
- Each candidate red-teamed.
- Winner selected with cited reasoning.
- Losers archived (never deleted — they're evidence of considered alternatives).

## Hooks fired

- Standard chain per candidate
- `subagent-governance-inject` per spawn

## Skills invoked

- `plan-tournament` (orchestrator)
- `plan-author` (×N candidates)
- `red-teamer` (×N evaluations)

## Examples

```
/shannon:plan-tournament "Add OAuth2 with PKCE"
/shannon:plan-tournament "Migrate auth to Better Auth" --candidates 4
```
