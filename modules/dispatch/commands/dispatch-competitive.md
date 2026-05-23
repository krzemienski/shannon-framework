---
name: dispatch-competitive
description: N parallel subagents on same task; multi-judge evaluation; evidence-based synthesis.
replaces:
  - /sadd:do-competitively
  - /sadd:do-and-judge
argument-hint: "<task> --candidates N"
---

# /shannon:dispatch-competitive

Competitive generation. Multiple subagents attempt the same task; judges select the best.

## Inputs

- Positional: task description
- `--candidates N` — number of competing subagents (default 3)

## Behavior

1. Spawn N subagents in parallel via `Task` — each gets identical task, isolated output directory.
2. Wait for all to complete.
3. Invoke `judge` skill per candidate output → individual scores.
4. Invoke meta-judge / `judge-with-debate` mode → debate-based ranking with cited reasoning.
5. Promote winning candidate; archive losers under `_rejected/`.

## Success criteria

- All N candidates produced output.
- Each candidate judged.
- Winner selected with cited reasoning.

## Hooks fired

- `subagent-governance-inject` per spawn

## Skills invoked

- `dispatch-parallel` (competitive variant)
- `judge` (with debate mode)
- `tree-of-thoughts` (optional, when candidates branch into sub-options)

## When to use

- High-stakes single-output decision (e.g. choosing best architectural diagram, picking copy variant)
- Stuck on tradeoffs and want multiple-perspective view

## When NOT to use

- Routine task (waste of compute)
- Decision already obvious

## Examples

```
/shannon:dispatch-competitive "Draft hero copy for /products page" --candidates 4
/shannon:dispatch-competitive "Design API for batch endpoint" --candidates 3
```
