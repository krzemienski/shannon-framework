---
name: shannon:write_plan
description: Generate exhaustive implementation plans (files, code, tests, verification) before execution
usage: /shannon:write_plan "feature or refactor" [--source docs/plans/brainstorm/...md] [--output docs/plans/YYYY-MM-DD-slug.md] [--handoff execute|subagent]
tags: [planning, documentation, parity, testing]
version: "5.4.0"
delegates_to:
  - writing-plans
  - phase-planning
---

# /shannon:write_plan – Shannon Implementation Plan Command

## Purpose

Creates Shannon-style implementation plans that rival superpowers' writing-plans skill while preserving strict NO MOCKS, 8D complexity, and wave orchestration requirements.

Use immediately after `/shannon:brainstorm` or `/shannon:spec` to convert decisions into actionable, test-first steps that any engineer (even with zero repo context) can execute.

## Workflow

1. **Announce**: "Running `/shannon:write_plan` to produce the implementation plan."
2. **Gather Context**:
   - Link to brainstorm/spec doc (or ask user).
   - Confirm target branch/worktree.
   - Capture acceptance criteria + testing/perf requirements.
3. **Generate Plan File**:
   - Save to `docs/plans/YYYY-MM-DD-<slug>.md`.
   - Include header:
     ```markdown
     # <Feature> Implementation Plan
     > **Required Next Command:** /shannon:execute_plan docs/plans/YYYY-MM-DD-<slug>.md
     ```
4. **Task Sections** – each includes:
   - File paths to create/modify.
   - Complete code snippets (not "add validation").
   - Test steps (command + expected result) – NO MOCKS.
   - Commit guidance (`git add`, `git commit -m "feat: …"`).
   - Wave checkpoints (if complexity >= 0.50).
5. **Handoff** – prompt user to choose between:
   - `/shannon:execute_plan` (structured execution).
   - `/shannon:task` or `/shannon:do` (intelligent execution).

## Required Sections

```markdown
## Context
- Goal
- Dependencies / Constraints
- 8D Complexity Summary
- Wave Strategy (if needed)

## Task 1 – <Name>
- Files
- Steps (each 2-5 minutes)
- Tests (exact command)
- Expected Output
- Commit

## Task 2 – …

## Validation Matrix
- Tests to re-run before completion
- Observability hooks / dashboards

## Handoff
- /shannon:execute_plan docs/plans/YYYY-MM-DD-<slug>.md
- /shannon:reflect before completion
```

## Guardrails

- Minimum 3 tasks (unless trivially small; explain exception).
- Reference relevant skills (e.g., `@skills/functional-testing`) in-context.
- If tests require new fixtures/data, describe creation steps.
- Avoid speculative requirements—ask user if unsure.

## Related Assets

- `skills/writing-plans/SKILL.md`
- `/shannon:execute_plan`
- `/shannon:brainstorm`
- `/shannon:spec`
