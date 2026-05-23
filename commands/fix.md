---
name: fix
description: Scout → debug → implement → revalidate. Three-strike cap per VF forge convention. Each attempt writes fresh evidence directory.
replaces:
  - /ck:fix
  - /validationforge:validate-fix
  - /oh-my-claudecode:fix
argument-hint: "[bug-description | error-log-path] [--auto]"
---

# /shannon:fix

Bug-fix runner with strict revalidation. Three attempts, three different root-cause hypotheses, three fresh evidence directories.

## Inputs

- Positional: bug description OR path to error log
- `--auto` — autonomous mode (no AskUserQuestion checkpoints)

## Behavior

For attempt 1..3:

1. **Scout**: read the bug evidence (description, log, screenshot). Grep codebase for surface area.
2. **Debug**: invoke `root-cause-tracing` skill (reflection domain). Output: a single root-cause hypothesis with cited file:line evidence.
3. **Implement**: dispatch `executor` agent with a minimal fix targeting that root cause only. No drive-by improvements.
4. **Revalidate**: invoke `functional-validation` skill against the journey that originally exposed the bug.
5. Evidence per attempt under `e2e-evidence/fix-<run-id>/forge-attempt-<N>/`. Never reuse evidence across attempts.
6. If revalidate PASSes → exit success.
7. If FAIL: document why this hypothesis failed in `failed-approaches.md`. Move to attempt N+1 with a DIFFERENT root-cause hypothesis (per `instrument-before-theorize.md` rule).
8. If 3 attempts all FAIL → mark UNFIXABLE; emit refusal pointing to `failed-approaches.md`.

## Success criteria

- Revalidation PASS within 3 attempts.
- Each attempt cites a distinct root-cause hypothesis.
- No drive-by edits — every changed line traces directly to the cited root cause.

## Hooks fired

- Standard chain (block-fab-files, read-before-edit, evidence-gate-reminder, validation-not-compilation)

## Skills invoked

- `root-cause-tracing`
- `functional-validation`
- `error-recovery` (between attempts)

## Iron rules

- Three-strike cap is hard. No fourth attempt — refusal is correct outcome.
- Same hypothesis twice = retry, not new attempt. Hypothesis must change.

## Examples

```
/shannon:fix "Login button on /login does nothing in Safari"
/shannon:fix logs/build-failure.txt --auto
```
