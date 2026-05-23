---
name: trace
description: Read session JSONL. Emit chronological timeline of hooks fired, skills invoked, tools called. Proves which Shannon hooks fire in real sessions.
replaces:
  - /oh-my-claudecode:trace
argument-hint: "[--session <id>] [--last-N <num>] [--filter hooks|skills|agents|tools]"
---

# /shannon:trace

Session JSONL analyzer. Renders chronological timeline of Shannon-side activity.

## Inputs

- `--session <id>` (default: current session)
- `--last-N <num>` — show only most recent N events (default: all)
- `--filter hooks|skills|agents|tools|all` (default `all`)

## Behavior

1. Resolve session JSONL path from `~/.claude/projects/<project>/<session-id>.jsonl`.
2. Stream-parse JSONL (large files OK).
3. Per relevant event line, extract:
   - timestamp
   - event type (hook fire, skill invocation, tool call, agent spawn)
   - identifier (which hook / skill / tool / agent name)
   - duration (ms)
   - exit code / decision (for hooks)
4. Render chronological timeline:
   ```
   [2026-05-23T13:34:12.001Z] HOOK PreToolUse:Write block-fab-files → rc=0 (ms=4)
   [2026-05-23T13:34:12.045Z] SKILL functional-validation → ACTIVATED (trigger: "validate this")
   [2026-05-23T13:34:13.500Z] TOOL Bash → "pnpm build" (rc=0, ms=1455)
   [2026-05-23T13:34:14.100Z] HOOK PostToolUse:Bash validation-not-compilation → rc=0 (ms=2)
   ```
5. Optionally write to `reports/trace-<session>.md`.

## Success criteria

- Timeline rendered; events ordered by timestamp.
- Every Shannon hook fire visible.

## Hooks fired

None — read-only.

## Skills invoked

- `observability-report`

## Examples

```
/shannon:trace
/shannon:trace --last-N 50 --filter hooks
/shannon:trace --session abc123-def456
```
