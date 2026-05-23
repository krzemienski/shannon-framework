---
name: plan-do-check-act
description: Iterative PDCA cycle for systematic experimentation and continuous improvement.
triggers:
  - "iterate experiment"
  - "PDCA"
  - "continuous improvement"
  - "kaizen cycle"
  - "next experiment"
---

# plan-do-check-act

Backs `/shannon:retro` and `/shannon:why` follow-up. The Kaizen PDCA cycle for actionable improvement.

## Behavior contract

Per identified improvement opportunity:

### Plan
- State the hypothesis ("changing X reduces failure rate by Y")
- Define the measurable Check criterion in advance
- Identify scope of the experiment (smallest viable test)

### Do
- Implement the experiment (small enough to revert)
- Capture state before and after

### Check
- Measure against the predefined criterion
- PASS: hypothesis confirmed
- FAIL: hypothesis disconfirmed (still valuable — eliminate this path)

### Act
- PASS → integrate into standard practice; update CLAUDE.md / rules
- FAIL → revert; document what was learned in `~/.claude/memory/`

## When to use

- After retrospective identifies a recurring problem
- After root-cause analysis identifies a category-level pattern
- When improvement claim needs validation (not "we should do X" but "X reduces Y by measurable amount")

## When NOT to use

- One-off bugs (just fix)
- Already-validated improvements

## Output

`reports/pdca-<slug>.md`:
```markdown
## Hypothesis
<statement>

## Check criterion (defined BEFORE Do)
<measurable>

## Experiment scope
<smallest viable>

## Results
- Before: <state>
- After: <state>
- Check: PASS | FAIL

## Act
<integrate or revert; cite where>
```

## Iron rules

- Criterion defined BEFORE experiment runs.
- No "results inconclusive" — define criterion such that it cannot be inconclusive.
- Failed experiments are wins (information).
