---
name: plan-author
description: Linear hierarchical plan author. plan.md + phase-NN.md files with measurable success criteria and validation gates per phase.
triggers:
  - "plan this"
  - "create plan"
  - "implementation plan"
  - "write a plan"
  - "draft plan"
---

# plan-author

Backs `/shannon:plan`, `/shannon:plan-tournament` (per candidate), `/shannon:plan-converge` (per round), `/shannon:plan-deep`, `/shannon:prd` (PRD mode).

## Behavior contract

1. Read user brief.
2. Read project context: `CLAUDE.md`, `docs/codebase-summary.md`, `docs/system-architecture.md`, `docs/code-standards.md`.
3. Decompose into phases. Each phase:
   - Atomic (can be executed and validated independently)
   - File-scoped (explicit list of files to modify/create/delete)
   - Has measurable success criteria
   - Has explicit validation gates
4. Write `plans/<date-prefix>-<slug>/`:
   - `plan.md` (overview, <80 lines, phase list with status)
   - `phase-01-<name>.md` ... `phase-NN-<name>.md`
5. Final phase is always validation (real-system exercise + evidence-gate) for any user-facing change.

## Phase file canonical structure

```markdown
# Phase NN: <name>

## Context Links
- Related reports / files / docs

## Overview
- Priority: <high | medium | low>
- Status: <pending | in_progress | completed>
- Description: <one paragraph>

## Key Insights
- <bullets from research / scout>

## Requirements
- Functional: <list>
- Non-functional: <perf, security, a11y>

## Architecture
- <diagrams or prose>

## Related Code Files
- Modify: <file paths>
- Create: <file paths>
- Delete: <file paths>

## Implementation Steps
1. <numbered>
2. ...

## Todo List
- [ ] <item>
- [ ] <item>

## Success Criteria
- <measurable; e.g. `curl /api/foo returns 200 with body matching schema-foo.json`>

## Validation Gate
- Skill: functional-validation
- Evidence required: <screenshot | API response | CLI stdout | build log>
- PASS criteria: <specific>

## Risk Assessment
- <likelihood × impact + mitigation>

## Security Considerations
- <auth, input validation, secrets>

## Next Steps
- Dependencies: <other phases>
- Follow-up: <future work>
```

## When to use

- `/shannon:plan` invocation
- `/shannon:plan-tournament` per-candidate spawn
- `/shannon:plan-converge` per-round spawn
- `/shannon:prd` PRD mode

## Iron rules

- Every phase has measurable success criteria — no "feature works" vague language.
- Every user-facing phase has a validation gate.
- No phase claims "tests pass" as success — phases never include test files.
- File ownership explicit per phase.
