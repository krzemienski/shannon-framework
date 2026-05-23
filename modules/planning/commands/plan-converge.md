---
name: plan-converge
description: Iterative plan refine → critique → revise. Converges when red-teamer returns ≤1 BLOCKING.
replaces:
  - /anneal-temper:anneal
argument-hint: "<problem> [--rounds N]"
---

# /shannon:plan-converge

Convergence-style planning. N rounds of plan → critique → revise until red-teamer is satisfied.

## Inputs

- Positional: problem description
- `--rounds N` — max convergence rounds (default 3)

## Behavior

For round 1..N:
1. **Round 1**: `plan-author` agent produces draft plan.
2. **Critique**: `red-teamer` agent reviews; emits findings.
3. **Revise**: `plan-author` re-runs with critique as input; produces revised plan.
4. Each round writes a checkpoint: `plans/converge-<run-id>/round-<N>/{draft.md, critique.md}`.
5. **Convergence check**: if red-teamer in round N reports ≤1 BLOCKING finding → CONVERGED; promote to canonical plan dir.
6. If round == max --rounds and still >1 BLOCKING → emit non-convergence note; ship the best round anyway, but flag manually.

## Success criteria

- Convergence reached within N rounds OR explicit non-convergence noted.
- Every round has critique + revised draft on disk.
- Final plan referenced from `plans/<date>-<slug>/plan.md`.

## Hooks fired

- Standard chain

## Skills invoked

- `plan-converge` (orchestrator)
- `plan-author`
- `red-teamer`

## Examples

```
/shannon:plan-converge "Real-time collaborative editing layer"
/shannon:plan-converge "Migrate auth system" --rounds 5
```
