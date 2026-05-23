---
name: retro
description: Mine session JSONLs over N days; aggregate decisions, lessons, gotchas; write retrospective report.
replaces:
  - /ck:retro
  - /retrospective-analyzer:retrospective-analyzer
  - /retro:retro
  - /kaizen:plan-do-check-act
argument-hint: "[--days N] [--scope project|session]"
---

# /shannon:retro

Sprint / weekly retrospective from session evidence. No prose-only summaries — every claim cites a session log.

## Inputs

- `--days N` (default 7)
- `--scope project|session` (default project)

## Behavior

1. Read session JSONLs from `~/.claude/projects/<project>/` for the last N days.
2. Extract decisions, lessons, gotchas, completed plans.
3. Group by week/day; aggregate metrics:
   - Tasks completed
   - Plans drafted vs executed
   - Failed approaches (count + categories)
   - Decisions made (with cite to session/turn)
4. Apply `plan-do-check-act` skill: per category, identify the next experiment.
5. Output: `reports/retrospective-<date>.md`.

## Report structure

```markdown
# Retrospective — <date range>

## What shipped
- <list with PR / commit citations>

## What we learned
- <lesson> [source: session-<id>.jsonl turn N]

## What broke
- <gotcha> [source: ...]

## Decisions
- <decision> [source: ...]

## Next experiments (PDCA)
- Plan: <what to try>
- Do: <action>
- Check: <success criterion>
- Act: <integrate or revert>
```

## Hooks fired

- Standard chain (read-mostly).

## Skills invoked

- `retrospective-validation` (folded into reflect for now; uses session search)
- `plan-do-check-act`
- `session-log-audit` (via observability-report)

## Iron rules

- No invented lessons — every claim cites a session log line.
- No "we should do X" — propose PDCA experiments with measurable Check criterion.

## Examples

```
/shannon:retro
/shannon:retro --days 14 --scope project
```
