---
name: audit
description: Read-only audit with severity classification. Screen, app, session, or drift scopes. No edits.
replaces:
  - /validationforge:validate-audit
  - /lynx:audit-screen
  - /lynx:full-ui-experience-audit
  - /seven-day-drift-audit:seven-day-drift-audit
  - /session-retrospective-audit:session-retrospective-audit
argument-hint: "--scope screen|app|session|drift [--days N]"
---

# /shannon:audit

Read-only audit. Produces a severity-classified findings report. Never edits source.

## Inputs

- `--scope screen|app|session|drift` (required)
  - `screen` — single UI screen visual + interaction audit
  - `app` — full app audit (every screen, every endpoint)
  - `session` — retrospective on session JSONL data
  - `drift` — compare plan claims vs actual codebase state over N days
- `--days N` — drift window (default 7)

## Behavior

### scope=screen
- Invoke `visual-inspection` skill on the screenshot under audit.
- Output: `reports/audit-screen-<slug>.md` with findings classified BLOCKING / HIGH / MEDIUM / LOW.

### scope=app
- Walk every route / view / screen; invoke `visual-inspection` per surface; invoke `full-functional-audit` skill for interaction inventory.
- Output: `reports/audit-app-<run-id>.md`.

### scope=session
- Read recent session JSONLs from `~/.claude/projects/`.
- Invoke `session-log-audit` skill (delegated through `observability-report`).
- Output: `reports/audit-session-<run-id>.md`.

### scope=drift
- Read `plans/` directory for the past `--days` days.
- For each completed plan: search session evidence for the work, grep codebase for the claims.
- Classify: VERIFIED (claim present in code) / DRIFT (claim not present) / SUPERSEDED (intentionally undone).
- Output: `reports/audit-drift-<window>-days.md`.

## Success criteria

- Every finding cites a specific file path or screenshot artifact.
- Severity assigned to every finding.
- No code edits performed (verified by `git diff` empty at exit).

## Hooks fired

None — read-only. No PreToolUse:Edit fires because audit never edits.

## Skills invoked

- `visual-inspection`
- `full-functional-audit`
- `baseline-quality-assessment`
- `session-log-audit` (via observability-report)

## Examples

```
/shannon:audit --scope screen
/shannon:audit --scope app
/shannon:audit --scope drift --days 14
```
