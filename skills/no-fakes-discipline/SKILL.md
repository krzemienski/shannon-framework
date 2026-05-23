---
name: no-fakes-discipline
description: Refuses circumvention of validation via fake substitutes. Reinforces the iron rule that the real system must be exercised.
triggers:
  - "add a fake"
  - "substitute the call"
  - "fixture-based response"
  - "fallback mode"
  - "fake the response"
  - "shim the endpoint"
---

# no-fakes-discipline

Active enforcement skill. Detects intent to substitute the real system; injects refusal stderr.

## Behavior contract

Pattern detection (triggered as InvocationLayer hint and reinforced by the `block-fab-files` PreToolUse:Write enforcement):

- Write tool target matches forbidden path patterns (test directories, spec files, mocks directories) → REFUSE.
- User prompt contains "add a substitute for X" or similar → InvocationLayer surfaces this skill BEFORE assistant writes code.

## When this skill fires

- PreToolUse:Write attempting to create a forbidden file → `block-fab-files` hook fires (no-fakes is the contract this hook enforces).
- User asks the assistant to add a substitute → InvocationLayer hint surfaces the skill so the assistant refuses-with-alternative.

## When NOT to fire

- Edit to existing legacy code containing pre-existing substitute patterns — Shannon's IRON RULES forbid CREATING new substitutes; pre-existing ones in legacy code are out of scope for this session.

## Alternatives the skill suggests

| Tempted by | Real-system alternative |
|---|---|
| Substitute HTTP server | Start a real dev server on a free port |
| Substitute the database | Seed local SQLite/Postgres with real data |
| Substitute auth | Real OAuth dev app with test credentials, or a real session cookie |
| Substitute filesystem | A real `/tmp/<run-id>/` directory |
| Substitute API response | Real API call against sandbox tier |

## Iron rules

- No "just temporary" exception. Temporary means present.
- No "fallback mode" — fallbacks are substitutes wearing a hat.
- No "just for tests" — there are no tests in Shannon.
