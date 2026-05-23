---
name: team
description: Spawn coordinated multi-agent teammates with shared TaskList, charter-driven roles, and stop-task semantics. Replaces OMC team and VF validate-team orchestrators.
replaces:
  - /oh-my-claudecode:team
  - /oh-my-claudecode:omc-teams
  - /validationforge:validate-team
argument-hint: "<team-name> --charter <file> [--size N]"
---

# /shannon:team

Multi-teammate orchestration. Lead spawns N parallel teammates with file-ownership boundaries and a shared TaskList.

## Inputs

- `<team-name>` — slug; identifies team config dir under `~/.claude/teams/<team-name>/`
- `--charter <file>` — required; markdown charter defining roles, file ownership, success criteria
- `--size N` — number of teammates (default from charter; max 8)

## Behavior

1. Parse charter; resolve roles, per-teammate file-ownership globs, dispatch graph.
2. `coordinator` agent reads charter and creates TaskList entries via `TaskCreate`.
3. Lead spawns N teammates via `Task` tool — each gets `subagent-governance-inject` IRON-RULE delivered through PreToolUse:Task stderr.
4. Teammates claim tasks by ID (lowest unblocked first); set `owner` + `status=in_progress` via `TaskUpdate`.
5. Teammates work within file-ownership glob; cross-glob writes refused.
6. `team-coordinator` skill polls TaskList; synthesizes findings; resolves conflicts.
7. `stop-task-semantics` hook (PreToolUse:Stop) blocks Stop if any teammate task still `in_progress`.

## Success criteria

- All teammate tasks `completed`
- No orphan `in_progress` tasks
- Lead verdict written to `plans/reports/team-<run-id>.md`
- File-ownership violations: zero

## Hooks fired

- `subagent-governance-inject` (PreToolUse:Task, every spawn)
- `stop-task-semantics` (PreToolUse:Stop, blocks if teammates still running)
- `evidence-gate-reminder` (per teammate TaskUpdate completion)

## Skills invoked

- `team-coordinator` (lead)
- per teammate: whatever charter specifies (commonly `functional-validation`, `plan-author`, `evidence-gate`)

## Examples

```
/shannon:team shannon-rebuild --charter team-charter.md --size 4
/shannon:team blog-audit --charter plans/audit-charter.md
```
