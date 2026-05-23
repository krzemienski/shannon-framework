---
name: loop
description: Self-referential do-verify-reflect loop until goal verified or max iterations hit. Absorbs all ralph variants.
replaces:
  - /oh-my-claudecode:ralph
  - /ralph-loop:ralph-loop
  - /ralph-planner:ralph-loop
  - /ralph-specum:ralph-loop
  - /ralphex:ralph-loop
  - /ralph-wiggum-marketer:ralph-loop
argument-hint: "<goal> [--max-iter N] [--verify-with <skill>]"
---

# /shannon:loop

Iterative {do → verify → reflect} loop. Converges when verify skill PASSes or max iterations exhausted.

## Inputs

- `<goal>` — natural language goal statement
- `--max-iter N` — iteration cap (default 5)
- `--verify-with <skill>` — verify skill name (default `functional-validation`)

## Behavior

Each iteration:
1. **Do** — `executor` agent attempts goal step with current best understanding.
2. **Verify** — invoke `--verify-with` skill against the artifact produced this iteration.
3. **Reflect** — invoke `reflect` skill; identify gap; produce next-iteration prompt.
4. If verify PASS AND `reflect` returns "converged" → exit success.
5. If iteration count == max-iter → emit REFUSAL.md citing unmet criteria; exit failure.

The loop persists state under `e2e-evidence/loop-<run-id>/iter-N/` so iterations are inspectable.

## Success criteria

- Verify skill returns PASS with cited evidence
- `reflect` skill confirms convergence (no actionable gaps remain)

## Hooks fired

- Standard chain per iteration (block-fab-files, validation-not-compilation, evidence-quality-check)
- `evidence-gate-reminder` on final TaskUpdate

## Skills invoked

- `loop-runner` (Shannon-specific orchestrator)
- User-specified verify skill (default `functional-validation`)
- `reflect`
- `refusal-discipline` (on max-iter exhaustion)

## Examples

```
/shannon:loop "Fix flaky CI in deploy-preview job"
/shannon:loop "Get LCP under 2.0s on /products" --max-iter 8 --verify-with functional-validation
```
