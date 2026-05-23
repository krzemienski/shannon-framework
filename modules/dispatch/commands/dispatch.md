---
name: dispatch
description: Sequential subagent chain. Each subagent gets IRON-RULE inject. Judge confirms each output before next dispatches.
replaces:
  - /sadd:do-in-steps
  - /sadd:launch-sub-agent
  - /sadd:subagent-driven-development
argument-hint: "<task-list-path | inline-tasks> [--model opus|sonnet|haiku]"
---

# /shannon:dispatch

Sequential subagent chain. Use when each step's output informs the next.

## Inputs

- Positional: path to task list OR inline tasks (newline-separated)
- `--model opus|sonnet|haiku` (default opus per project rule)

## Behavior

1. Parse task list. Each task is one subagent invocation.
2. For task 1..N:
   a. Spawn subagent via `Task`. PreToolUse:Task fires `subagent-governance-inject` (IRON RULE to stderr).
   b. Wait for subagent completion.
   c. Invoke `judge` skill on subagent output. Judge emits PASS / FAIL / NEEDS_REVISION.
   d. PASS → proceed to task N+1.
   e. FAIL → halt; report to user.
   f. NEEDS_REVISION → re-dispatch task N with judge feedback as additional context. Max 2 revision rounds per task.
3. After all tasks: aggregate output into `reports/dispatch-<run-id>.md`.

## Success criteria

- Every task PASSed judge.
- No revision loops exceeded 2 rounds.
- Aggregate report written.

## Hooks fired

- `subagent-governance-inject` (PreToolUse:Task per spawn)
- `stop-task-semantics` (PreToolUse:Stop; blocks if subagent task still in_progress)

## Skills invoked

- `dispatch-parallel` (sequential variant; same skill, sequential mode)
- `judge`

## Examples

```
/shannon:dispatch tasks.md
/shannon:dispatch "research X" "summarize X" "outline post about X"
```
