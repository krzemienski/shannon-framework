---
name: evidence-gate
description: 5-question checklist applied before any completion claim. Any 'no' refuses completion.
triggers:
  - "marking complete"
  - "task complete"
  - "ready to ship"
  - "PR ready"
  - "ready for review"
  - "done"
---

# evidence-gate

Refusal-discipline gate. Five questions, all must be YES, or the gate refuses.

## Behavior contract

Before any TaskUpdate to `completed`, before any PR creation, before any "done" claim:

1. **READ evidence?** Did you personally read the cited evidence files? Not "an agent says so" — YOU.
2. **VIEW screenshot?** If UI work: did you visually inspect the screenshot? Not just confirm it exists.
3. **EXAMINE output?** If CLI / API work: did you read the actual stdout / response body? Not just exit code.
4. **CITE proof?** Does every claim of PASS cite a specific file path (with line range where relevant)?
5. **Skeptic agree?** Would a skeptical reviewer agree the cited evidence supports the claim?

Any answer of NO → REFUSE completion. Write findings, route to `refusal-discipline` skill.

## When to use

- About to set TaskUpdate status=completed
- About to write "ready to ship" in a PR
- About to commit with "feat: done" message
- Hook `evidence-gate-reminder` fires (PreToolUse:TaskUpdate)

## When NOT to use

- Mid-iteration in a loop (use only at the OUTER gate)
- Exploratory work without a completion claim

## Iron rules

- Gate is binary. Yes-to-all-5 OR refuse. No "mostly yes". No "I think so".
- Self-review counts. The skill is the gate — running through 5 questions personally IS the discipline.
- No override flag. Calling this gate and ignoring its refusal is a bug, not a feature.

## Example refusal

```
Q1 READ evidence: NO — I never opened step-03-login-success.png
Q2 VIEW screenshot: N/A
Q3 EXAMINE output: PARTIAL — read exit code, didn't read stdout
Q4 CITE proof: NO — claim "feature works" lacks file:line
Q5 Skeptic agree: NO — evidence dir has 2 zero-byte files

→ REFUSED. Re-run functional-validation, then re-gate.
```
