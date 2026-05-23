---
name: create-validation-plan
description: Multi-phase project plan generator that injects functional validation gates with evidence requirements. Output: phase plans with gates per real-system PASS criterion.
triggers:
  - "create validation plan"
  - "validation phases"
  - "inject validation gates"
  - "plan with gates"
---

# create-validation-plan

Backs the gate-injection step of `/shannon:plan-deep` and the planning phase of `/shannon:validate`.

## Behavior contract

1. Read a base plan (from `plan-author`) OR a feature brief.
2. For each phase in the plan: derive a validation gate.
3. Gate structure (per phase):
   ```markdown
   ## Validation Gate (phase NN)
   - **Skill:** functional-validation | visual-inspection | api-validation | ...
   - **Real system to exercise:** <server | simulator | CLI invocation>
   - **Journey to execute:** <step-by-step actions>
   - **Evidence required:** <screenshot | response body | log tail>
   - **PASS criterion:** <specific assertion>
   - **FAIL → consequence:** halt + refusal-discipline OR retry via /shannon:fix
   ```
4. Emit the gate inline in the phase file (NOT a separate file — gate is part of the phase).
5. Refuse if the base plan has a phase claiming "tests pass" or "test coverage" as a gate — these are the patterns Shannon's iron rule forbids.

## When to use

- Phase 3 of `/shannon:plan-deep`
- Phase 1 of `/shannon:validate` (planning)
- Standalone gate-injection on an existing plan that lacks them

## When NOT to use

- Read-only changes (audits, doc updates)
- Pure refactor with no behavior change

## Iron rules

- **No mock-based gates.** Gate must exercise real system.
- **No "tests pass" gates.** Refuse and rewrite.
- **Evidence path specified at gate definition time** — not deferred.
- Gate is part of the phase, not a separate optional step.
