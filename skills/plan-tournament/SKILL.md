---
name: plan-tournament
description: Tournament orchestrator. Spawns N plan-author candidates with distinct perspectives, red-teamer per candidate, tournament-judge selects winner.
triggers:
  - "plan tournament"
  - "compare plans"
  - "anneal cast"
  - "competing plans"
---

# plan-tournament

Backs `/shannon:plan-tournament`. Tournament-style consensus planning.

## Behavior contract

1. Read user problem statement.
2. Determine candidate perspectives (default 3): security-first, performance-first, simplicity-first. Configurable to add: scalability-first, accessibility-first, cost-first.
3. Spawn N `plan-author` agents in parallel via `Task`. Each gets:
   - The same problem
   - A distinct lens prompt
   - Isolated output directory: `plans/tournament-<run-id>/candidate-<N>/`
4. After all candidates emit plans: spawn `red-teamer` agent per candidate. Red-teamer reads candidate plan, emits findings BLOCKING/HIGH/MEDIUM/LOW with cited file:line per finding.
5. Score candidates:
   - +10 per HIGH or BLOCKING avoided vs other candidates
   - -5 per BLOCKING introduced (security holes, scope inversions)
   - -2 per HIGH introduced
   - Bonus +5 for simplicity (lower line count, fewer phases) — KISS principle
6. Select winner. Write `plans/tournament-<run-id>/VERDICT.md` citing score breakdown + selection reasoning.
7. Promote winner to `plans/<date>-<slug>/`. Move losers to `_rejected/`.

## When to use

- High-stakes decisions where multiple approaches exist
- Cross-cutting concerns (security AND performance AND simplicity all matter)
- Pre-architecture-review

## When NOT to use

- Routine feature with obvious approach
- Speed-critical iteration (tournament is 3× wall time)
- Tight scope where one perspective dominates

## File ownership

- Coordinator: writes VERDICT.md ONLY.
- Candidate-N: writes ONLY `candidate-<N>/` subdirectory.
- Red-teamer: writes ONLY `candidate-<N>/red-team-findings.md`.
