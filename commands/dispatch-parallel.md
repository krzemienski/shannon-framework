---
name: dispatch-parallel
description: Parallel subagents on independent tasks. Meta-judge + LLM-as-judge verification per sadd's pattern.
replaces:
  - /sadd:do-in-parallel
  - /superpowers:dispatching-parallel-agents
argument-hint: "<task-list> [--max-parallel N]"
---

# /shannon:dispatch-parallel

Parallel subagent fan-out. Use when tasks are independent (no inter-task dependencies).

## Inputs

- Positional: task list (path or inline newline-separated)
- `--max-parallel N` — concurrency cap (default 5)

## Behavior

1. Parse task list.
2. Group tasks into batches of size `--max-parallel`.
3. Per batch: spawn all subagents in parallel via `Task` (multiple tool calls in same response).
4. Wait for all batch subagents to complete.
5. Invoke `judge` skill on each subagent's output → PASS / FAIL.
6. Aggregate batch results; proceed to next batch.
7. After all batches: meta-judge synthesizes ALL outputs (cross-subagent consistency check) → emits final verdict.

## Success criteria

- Every task PASSed judge.
- Meta-judge consistency check PASSED.
- No file-ownership violations across parallel subagents (each must own distinct file globs).

## Hooks fired

- `subagent-governance-inject` per spawn
- `stop-task-semantics` (blocks Stop while any subagent in_progress)

## Skills invoked

- `dispatch-parallel`
- `judge`

## Iron rules

- Tasks MUST be independent (file ownership separates them).
- No shared mutable state between parallel subagents.
- Meta-judge reads ALL outputs before emitting verdict.

## Examples

```
/shannon:dispatch-parallel "fix file-a.ts" "fix file-b.ts" "fix file-c.ts"
/shannon:dispatch-parallel tasks-by-file.md --max-parallel 8
```
