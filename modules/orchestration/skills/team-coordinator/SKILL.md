---
name: team-coordinator
description: Multi-teammate orchestration. Maintains shared TaskList, assigns work by file-ownership glob, synthesizes findings, blocks Stop on incomplete tasks.
triggers:
  - "spawn team"
  - "coordinate teammates"
  - "multi-agent team"
  - "team charter"
---

# team-coordinator

Skill that backs `/shannon:team`. Lead-side orchestration.

## Behavior contract

1. Parse team charter (markdown): extract roles, file-ownership globs, dispatch dependencies.
2. Create TaskList entries per role + per task via `TaskCreate`.
3. Spawn N teammates via `Task` tool. Each spawn fires `subagent-governance-inject` (PreToolUse:Task) — IRON RULE delivered to teammate stderr at startup.
4. Poll TaskList: track in_progress, completed, blocked.
5. On teammate completion: read teammate report under `plans/reports/`, integrate into running synthesis.
6. On file-ownership violation (detected via post-edit grep against ownership glob): refuse and re-assign.
7. On Stop event: `stop-task-semantics` hook blocks if any teammate task still `in_progress`.

## When to use

- 3+ independent workstreams that can parallelize
- Tasks with clear file-ownership boundaries (no overlap)
- Need shared TaskList visibility across teammates

## When NOT to use

- Single workstream → use `/shannon:cook`
- Workstreams share files heavily → sequential is safer
- Exploratory / unknown decomposition → use `/shannon:plan` first

## File ownership rule (LOAD-BEARING)

Every task description must include `File ownership: <glob>`. Teammates refusing to honor ownership are halted by lead and re-tasked. No exceptions.

## Iron rules

- No partial verdicts. Wait for ALL teammates before final synthesis.
- Verdict writer reads ALL evidence, not just inventories.
- Contradictions escalate to lead; lead resolves with citation, never invents.
