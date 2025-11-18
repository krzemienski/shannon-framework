---
name: writing-plans
description: Create exhaustive implementation plans with file paths, code snippets, and NO MOCKS verification
skill-type: PLAYBOOK
shannon-version: ">=5.4.0"
complexity-triggers: [0.20-1.00]
requires:
  - phase-planning
  - functional-testing
  - forced-reading-protocol
---

# Writing Plans Skill

## Mission

Translate approved solution direction into a concrete, test-first plan that any engineer can follow without prior repo context.

## Inputs

- Brainstorm or spec document reference
- Confirmed goal + success metrics
- Active branch/worktree
- Complexity score + wave recommendation
- Constraints (tech stack, compliance, deadlines)

## Output Requirements

1. Markdown saved to `docs/plans/YYYY-MM-DD-<slug>.md`.
2. Header:
   ```
   # <Feature> Implementation Plan
   > **Required Next Command:** /shannon:execute_plan docs/plans/YYYY-MM-DD-<slug>.md
   ```
3. Sections:
   - Context (goal, constraints, dependencies, complexity recap)
   - Task list (≥3 tasks, each 2-5 min steps, no skipped tests)
   - Validation matrix (tests to re-run post-plan)
   - Observability/rollout notes
   - Handoff instructions (execute_plan vs intelligent do)

## Task Template

```
## Task N – <Name>
**Files**
- Create: path/file.ext
- Modify: path/file.ext:L123-L150
- Tests: tests/path/test_file.py::test_case

**Steps**
1. Write failing test (code block)
2. Run test → EXPECT FAIL (log output)
3. Implement minimal code (code block)
4. Re-run tests → EXPECT PASS
5. Commit (exact command)
```

## Guardrails

- Every task references exact files + line ranges.
- Include full code snippets (never "add validation").
- Testing commands must enforce NO MOCKS (call out puppeteer/docker/etc.).
- Document expected failures before implementation.
- Align commits with tasks (no mega-commits).
- Mention checkpoint frequency (e.g., `checkpoint plan-task-3`).

## Handoff Script

End plan with:
```
Plan complete and saved to docs/plans/….md.
Two execution paths:
1. /shannon:execute_plan docs/plans/….md --mode subagent (structured)
2. /shannon:do "<feature summary>" (intelligent execution)
Which do you prefer?
```

## Related Commands

- `/shannon:write_plan`
- `/shannon:execute_plan`
- `/shannon:reflect`
