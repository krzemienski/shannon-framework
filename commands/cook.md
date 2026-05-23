---
name: cook
description: Execute a plan or task brief end-to-end with iron-rule validation and evidence gates. Wraps planning, execution, functional validation, and completion gate.
replaces:
  - /ck:cook
  - /oh-my-claudecode:cook
  - /validationforge:validate-fix
  - /crucible:plan-and-execute
argument-hint: "[plan-path | task-description] [--auto] [--fast] [--no-validate]"
---

# /shannon:cook

End-to-end implementation runner. Plan if needed, execute against real system, validate functionally, gate on evidence before declaring done.

## Inputs

- Positional: plan path OR free-form task description
- `--auto` — small-task path: skip `plan-author`, dispatch executor directly (UQ-CMD-1)
- `--fast` — skip non-critical refinement loops
- `--no-validate` — skip post-execution functional validation (NOT recommended)

## Behavior

1. Argument classification: if arg resolves to filesystem path → read as plan; else treat as brief.
2. If brief AND not `--auto`: invoke `plan-author` skill → emits `plans/{date}-{slug}/{plan.md, phase-NN-*.md}`.
3. If brief AND `--auto`: skip plan author, synthesize a one-shot phase prompt in-memory.
4. Spawn `executor` agent with phase plan + IRON-RULE injection (no fakes, no mocks, no test files).
5. After executor completes each phase: invoke `functional-validation` skill against the affected surface (unless `--no-validate`).
6. Before marking task complete: invoke `evidence-gate` skill — 5-question checklist must all answer yes.
7. On any FAIL: route to `/shannon:fix` flow (3-strike cap) OR surface refusal via `refusal-discipline`.

## Success criteria

- All phases executed and committed (or staged) in worktree
- `e2e-evidence/<run-id>/` populated with non-empty artifacts per phase
- `evidence-gate` PASS
- No FAIL verdicts open at exit

## Hooks fired

- `evidence-gate-reminder` (PreToolUse:TaskUpdate when status=completed)
- `validation-not-compilation` (PostToolUse:Bash after build commands)
- `validation-skill-tripwire` (InvocationLayer; fires if build succeeds without functional-validation invoked)
- `block-fab-files` (PreToolUse:Write blocks `*.test.*`, `*.spec.*`, `tests/`, `__tests__/`)
- `read-before-edit` (PreToolUse:Edit reminder)
- `subagent-governance-inject` (PreToolUse:Task injects IRON RULE before executor spawn)

## Skills invoked

- `plan-author` (unless `--auto` or arg is path)
- `executor` (agent, not skill — via Task)
- `functional-validation`
- `evidence-gate`
- `refusal-discipline` (only if gate refuses)

## Examples

```
/shannon:cook plans/260523-1334-feature-x/
/shannon:cook "Add OAuth login to settings screen" --with-validation
/shannon:cook "Bump prisma to 6.4" --auto
/shannon:cook plans/.../ --no-validate    # NOT RECOMMENDED — explicit waiver only
```
