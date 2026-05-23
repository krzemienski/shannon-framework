---
name: observability-report
description: Shannon-specific log reader. Powers /shannon:trace, /shannon:doctor, retrospective session analysis. Reads hooks.jsonl, hook-errors.jsonl, session JSONLs.
triggers:
  - "trace"
  - "doctor"
  - "session log audit"
  - "hooks fired log"
  - "observability"
---

# observability-report

The single skill for reading Shannon-produced logs + Claude Code session JSONLs.

## Behavior contract

### Mode: trace (for `/shannon:trace`)
1. Read `~/.claude/projects/<project>/<session-id>.jsonl`.
2. Stream-parse; filter to Shannon-relevant events (hook fires, skill triggers, tool calls, agent spawns).
3. Render chronological timeline.

### Mode: doctor (for `/shannon:doctor`)
1. Read `.claude-plugin/plugin.json` + `marketplace.json`.
2. Read `hooks/hooks.json` + verify scripts present.
3. Read `~/.claude/settings.json`.
4. Read `~/.claude/logs/shannon/hooks.jsonl` (last 100 lines) → confirm hooks have actually fired recently.
5. Emit per-check PASS/FAIL.

### Mode: session-log-audit (for `/shannon:retro` and `/shannon:audit --scope session`)
1. Walk `~/.claude/projects/<project>/` for sessions in date range.
2. Stream-parse each; extract user prompts, assistant turns, tool calls, commits.
3. Emit aggregate metrics + sample citations.

## Log paths Shannon writes to

- `~/.claude/logs/shannon/hooks.jsonl` — one line per hook fire (ts, script, matchedTool, decision, exitCode, ms, sessionId)
- `~/.claude/logs/shannon/hook-errors.jsonl` — one line per crash / slow-fire
- `~/.claude/logs/shannon/open-tasks.txt` — TaskCreate/TaskUpdate listener output (for stop-task-semantics)

## Iron rules

- Never invent log entries. If a log file is missing, report missing — don't fabricate.
- Stream-parse large files (some sessions are >100MB).
- Cite session-id + line number when surfacing claims.
