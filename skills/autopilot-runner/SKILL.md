---
name: autopilot-runner
description: Refusal-driven retry orchestration for /shannon:autopilot. Wraps /shannon:cook with REFUSAL.md parsing and remediation prompt synthesis.
triggers:
  - "autopilot"
  - "run autonomously"
  - "keep retrying until it works"
  - "refusal-driven retry"
---

# autopilot-runner

Skill that backs `/shannon:autopilot`. Provides the retry loop logic, refusal parsing, and remediation prompt synthesis.

## Behavior contract

Given a task and max-attempts N:

1. For attempt 1..N:
   - Invoke `/shannon:cook` with current prompt.
   - Read `e2e-evidence/<run-id>/completion-gate/report.json`.
   - If `verdict == "COMPLETE"`: return success with cited evidence.
   - If `verdict == "REFUSED"`:
     - Parse `REFUSAL.md` cited blockers.
     - Synthesize remediation prompt (next-attempt brief targeting only failing MSCs).
     - Continue.
2. If N attempts exhausted and still REFUSED: write final `REFUSAL.md` to `plans/reports/autopilot-<run-id>-REFUSAL.md`; return failure.

## When to use

- User invokes `/shannon:autopilot`
- User says "run this autonomously until done"
- Long-running tasks where refusal-driven retry is preferred over manual oversight

## When NOT to use

- User wants single-pass execution → use `/shannon:cook` directly
- Task is exploratory / no clear success criteria → use `/shannon:loop` instead
- Production deploy where refusal must escalate to a human gate

## Examples

```
attempt-1 → cook → REFUSED ("evidence missing for journey: login-flow")
attempt-2 → cook with prompt "Re-run login-flow journey; capture screenshot at /login after submit" → COMPLETE
```

## Iron rules

- Never invent COMPLETE verdict — must be cited by completion-gate.
- Never override REFUSAL.md — read it, act on its blockers, retry.
- No `--force-complete` flag. Ever.
