---
name: plan-converge
description: Convergence orchestrator. Iterative plan-author → red-teamer → plan-author until red-teamer reports ≤1 BLOCKING.
triggers:
  - "plan converge"
  - "iteratively refine plan"
  - "anneal temper"
  - "converge plan"
---

# plan-converge

Backs `/shannon:plan-converge`. Iterative convergence between author and red-teamer.

## Behavior contract

For round 1..max-rounds:

1. Round 1: `plan-author` agent produces draft.
2. `red-teamer` agent reviews draft; emits findings.
3. Round N (N>1): `plan-author` reads previous round's critique; produces revised draft.
4. Convergence check: red-teamer in round N reports ≤1 BLOCKING finding → CONVERGED.
5. Each round writes:
   - `plans/converge-<run-id>/round-<N>/draft.md`
   - `plans/converge-<run-id>/round-<N>/critique.md`
6. On convergence: promote final draft to `plans/<date>-<slug>/`; archive `converge-<run-id>/` to `_history/`.
7. On non-convergence at max-rounds: ship the best-scoring round anyway with a NON_CONVERGED.md note explaining why.

## When to use

- Topic where author and critic perspectives are productive (security review, perf review)
- Plan needs iterative hardening but not full tournament
- Time-bounded planning with quality bar

## When NOT to use

- Decision needs multiple distinct lenses simultaneously → use `/shannon:plan-tournament`
- Small change with obvious plan → use `/shannon:plan`

## Iron rules

- Each round MUST produce a NEW draft — re-emitting prior round unchanged = invalid.
- Red-teamer MUST cite file:line per finding.
- Max-rounds is hard.
