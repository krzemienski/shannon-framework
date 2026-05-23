---
name: plan-deep
description: Deepest-plan style. Wraps plan-tournament + plan-converge with gate injection. Consensus + gates + synthesis.
replaces:
  - /deepest-plan:deepest
  - /deepest-plan:deepest-plan
argument-hint: "<problem> [--synthesis N] [--debate]"
---

# /shannon:plan-deep

The full deepest-plan treatment. Consensus across multiple perspectives + iterative convergence + functional validation gate injection.

## Inputs

- Positional: problem description
- `--synthesis N` — number of synthesis perspectives (default 3)
- `--debate` — enable debate mode (red-teamers argue findings, not just emit them)

## Behavior

1. **Tournament phase** — invoke `plan-tournament` skill with N candidates and distinct perspectives.
2. **Convergence phase** — feed tournament winner into `plan-converge` skill; run 2-3 rounds.
3. **Gate injection** — invoke `create-validation-plan` skill against the converged plan; for each phase add explicit validation gates (PASS criteria + required evidence type).
4. **Synthesis** — if `--debate`: red-teamers exchange critiques across candidates; `plan-author` synthesizes a final plan absorbing the strongest concerns.
5. Promote final plan to `plans/<date>-<slug>/`. Archive intermediate rounds under `_history/`.

## Success criteria

- Tournament + convergence + gate injection all executed.
- Final plan has explicit validation gate per phase.
- History preserved for audit.

## Hooks fired

- Standard chain

## Skills invoked

- `plan-tournament`
- `plan-converge`
- `plan-author`
- `red-teamer`
- `create-validation-plan`

## Examples

```
/shannon:plan-deep "Add E2E encryption to chat with key rotation"
/shannon:plan-deep "Multi-region failover" --synthesis 4 --debate
```
