---
name: shannon:execute_plan
description: Execute a Shannon implementation plan task-by-task with validation gates and checkpoints
usage: /shannon:execute_plan docs/plans/YYYY-MM-DD-slug.md [--mode subagent|solo] [--start-at task-number]
tags: [execution, validation, parity, testing]
version: "5.4.0"
delegates_to:
  - executing-plans
  - functional-testing
  - wave-orchestration
---

# /shannon:execute_plan – Guided Plan Execution

## Purpose

Executes a previously generated plan (from `/shannon:write_plan`) with tight feedback loops, validation gates, and Shannon’s NO MOCKS enforcement. Inspired by superpowers’ executing-plans command but layered with wave checkpoints and Serena integration.

## Preconditions

- Plan file exists under `docs/plans/`.
- Plan includes task numbering + tests.
- North Star goal defined (optional but recommended).

If prerequisites missing, prompt user to run `/shannon:write_plan` first.

## Execution Flow

1. **Load Plan**: Parse Markdown, build ordered task list.
2. **Confirm Mode**:
   - `subagent` (default): spawn fresh execution loop per task, pause for review.
   - `solo`: run tasks sequentially without pause.
3. **For Each Task**:
   - Restate context (files, goal, dependencies).
   - **Step 0**: Run specified failing test (should fail). Note result.
   - **Step 1..N**: Follow instructions exactly, referencing required skills (functional-testing, context-preservation, etc.).
   - **Step N+1**: Run verification command(s) until PASS.
   - **Step N+2**: Commit with plan-specified message.
   - Log trace to `.shannon/waves/<plan>/task-<n>.md`.
4. **Between Tasks**:
   - Re-run smoke tests enumerated in plan.
   - Create Serena checkpoint (`/shannon:checkpoint plan-<n>`).
5. **After Final Task**:
   - Trigger `/shannon:reflect` automatically.
   - Summarize coverage + outstanding follow-ups.

## Commands / Flags

| Flag | Description |
|------|-------------|
| `--mode subagent|solo` | Default `subagent` (pause between tasks). |
| `--start-at N` | Resume from specific task number if interrupted. |
| `--dry-run` (future) | (Planned) Validate plan format without executing. |

## Failure Handling

- If test fails unexpectedly, stop and record details under `docs/plans/<plan>#blocked`.
- If instructions ambiguous, create clarification step before continuing.
- Never skip steps—even if "obvious".

## Required Prompts

- Before first task: confirm plan + mode.
- Before each task: "Ready to execute Task N? (y/N)" in subagent mode.
- After each task: "Task N complete. Continue?".

## Deliverables

- Updated plan file with checkmarks.
- `.shannon/waves/<plan>/` execution logs.
- Commit history aligned with tasks.

## Related Skills & Commands

- `skills/executing-plans/SKILL.md`
- `/shannon:write_plan`
- `/shannon:reflect`
- `/shannon:checkpoint`
