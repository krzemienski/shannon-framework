---
name: executing-plans
description: Step-by-step execution of Shannon implementation plans with validation gates and checkpoints
skill-type: PLAYBOOK
shannon-version: ">=5.4.0"
complexity-triggers: [0.20-1.00]
requires:
  - functional-testing
  - wave-orchestration
  - context-preservation
---

# Executing Plans Skill

## Intent

Consume a plan created by `/shannon:write_plan` and execute each task with discipline:

- Each step validated (tests, lint, build).
- Serena checkpoints after meaningful increments.
- Clear logging for auditing or handoff.

## Inputs

- Path to plan markdown file.
- Mode: `subagent` (default) or `solo`.
- Optional `start-at` task number.

## Execution Loop

1. **Load Plan**
   - Verify file exists + parse headings.
   - Extract tasks, tests, expected outputs.

2. **Task Preparation**
   - Announce task name + summary.
   - Confirm files + dependencies exist.
   - If context missing, run `forced-reading-protocol`.

3. **Follow Steps**
   - Execute plan steps literally.
   - For each code block, restate rationale.
   - Run failing tests BEFORE implementation; capture failure text.
   - Implement minimal change; rerun tests until green.

4. **Validation & Logging**
   - Record results in `.shannon/waves/<plan>/task-N.md`.
   - Save test output + diffs.
   - Create checkpoint `plan-task-N`.

5. **Commit**
   - Use plan-provided commit message.
   - Append `[plan:<slug>]` suffix for traceability.

6. **Review Pause (subagent mode)**
   - Ask operator to review diff/log.
   - Only proceed on approval.

7. **Completion**
   - After final task, run entire validation matrix.
   - Trigger `/shannon:reflect`.

## Guardrails

- If plan lacks tests for a task, halt and request update.
- Never bulk-edit files outside plan scope unless operator approves.
- Document deviations in plan file (append "Adjustments" section).
- Respect NO MOCKS—fail fast if plan instructs mocking.

## Related Commands

- `/shannon:execute_plan`
- `/shannon:write_plan`
- `/shannon:checkpoint`
- `/shannon:reflect`
