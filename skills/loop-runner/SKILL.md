---
name: loop-runner
description: Iterative do-verify-reflect loop until verify skill PASSes or max-iter exhausted. Backs /shannon:loop.
triggers:
  - "ralph loop"
  - "iterate until done"
  - "do-verify-reflect"
  - "self-referential loop"
---

# loop-runner

Skill that backs `/shannon:loop`. Bounded iteration with verification + reflection.

## Behavior contract

Per iteration N (1..max-iter):

1. **Do**: spawn `executor` agent with iteration-N prompt; capture output to `e2e-evidence/loop-<run-id>/iter-N/`.
2. **Verify**: invoke `--verify-with` skill (default `functional-validation`). Read its verdict.
3. **Reflect**: invoke `reflect` skill against iteration-N artifact + verdict; produce gap analysis + next-iteration prompt.
4. Exit condition:
   - Verify PASS AND reflect → "converged": exit success.
   - Iteration == max-iter AND still failing: emit REFUSAL.md, exit failure.
   - Else: increment N, loop.

## When to use

- Goal is observable (you can write the verify skill) but path to it isn't
- Iterative refinement (perf tuning, prompt tuning, layout tuning)
- Convergent search where each round improves

## When NOT to use

- Goal isn't testable as a skill verdict → use `/shannon:cook` with explicit plan
- Time-bounded task with hard deadline → max-iter may exhaust
- Multi-actor coordination → use `/shannon:team`

## Anti-patterns

- Re-running same iteration with same prompt — `reflect` must produce DIFFERENT prompt each round.
- Skipping verify step → loop becomes uncontrolled.
- Verifying with a vague skill that always returns PASS → choose a strict verify skill.

## Iron rules

- Each iteration writes its own evidence directory.
- Verify result and reflect output BOTH persist on disk before next iteration.
- No override on max-iter — refusal exits gracefully.
