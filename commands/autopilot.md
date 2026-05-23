---
name: autopilot
description: Refusal-driven retry loop around /shannon:cook. Preserves Crucible's REFUSAL.md pattern.
replaces:
  - /oh-my-claudecode:autopilot
  - /crucible:autopilot
  - /deepest-plan:deepest-validate
argument-hint: "<task> [--max-attempts N]"
---

# /shannon:autopilot

Fully autonomous execution. Wraps `/shannon:cook` in a refusal-driven retry loop.

## Inputs

- `<task>` — task description or plan path
- `--max-attempts N` — retry cap (default 3)

## Behavior

For attempt 1..N:
1. Invoke `/shannon:cook <task>`.
2. After cook returns, check `completion-gate` verdict:
   - `COMPLETE` → exit success.
   - `REFUSED` → read `REFUSAL.md`, parse cited blockers, build remediation prompt for next attempt.
3. If attempt == max-attempts AND still REFUSED → emit final REFUSAL.md to `plans/reports/autopilot-<run-id>-REFUSAL.md`; exit failure.

Per Crucible discipline: refusal is a feature, not a bug. No override flag. No force-complete.

## Success criteria

- `completion-gate` returns COMPLETE
- All cited blockers from prior attempts resolved with new evidence

## Hooks fired

- Full chain per attempt (entire validation + completion stack)
- `evidence-gate-reminder` critical at each cook completion
- `stop-task-semantics` (if multi-teammate execution inside cook)

## Skills invoked

- `/shannon:cook` (delegated)
- `completion-gate`
- `refusal-discipline`

## Examples

```
/shannon:autopilot "Add SSO with Okta to admin panel"
/shannon:autopilot plans/260523-feature-y/ --max-attempts 5
```
