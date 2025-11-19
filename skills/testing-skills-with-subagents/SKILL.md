---
name: testing-skills-with-subagents
description: Use before skill deployment to verify pressure resistance via TDD RED-GREEN-REFACTOR cycle with Serena metrics tracking - measures compliance score (0.00-1.00) across pressure scenarios
---

# Testing Skills With Subagents (Shannon-Enhanced)

## Overview

**TDD for process documentation with quantitative metrics.**

Red-Green-Refactor applies to skills: (1) Run baseline WITHOUT skill, (2) Write skill addressing failures, (3) Close loopholes until bulletproof. Shannon enhancement adds Serena metrics tracking for compliance scoring.

**Compliance Scoring (0.00-1.00):**
- 0.00-0.60: Fails under pressure, multiple rationalizations
- 0.61-0.85: Mostly compliant, 1-2 new loopholes
- 0.86-0.99: Bulletproof, rare exceptions
- 1.00: Perfect compliance across all scenarios

## When to Use

Test skills enforcing discipline (TDD, code review, testing) that:
- Have compliance costs (time, effort)
- Could be rationalized away
- Contradict immediate goals (speed over quality)

**Don't test:** Reference skills, pure documentation, skills without rules.

## TDD Cycle with Metrics

| Phase | Action | Shannon Metric |
|-------|--------|-----------------|
| **RED** | Run scenario WITHOUT skill | baseline_failures: count violations |
| **GREEN** | Write skill, run WITH skill | compliance_score: % correct choices |
| **REFACTOR** | Close loopholes | loophole_count: new rationalizations found |
| **Verify** | Re-test scenarios | final_score: 0.00-1.00 |

## RED Phase: Baseline (Watch It Fail)

```bash
# Serena metric: baseline_failures
- Run pressure scenarios WITHOUT skill
- Document rationalizations verbatim
- Log failure patterns to Serena
  pressure_type: "sunk_cost|time|authority|exhaustion|social"
  rationalization: "exact words agent used"
  scenario_complexity: 1-3 pressures
```

**Pressure types to combine:**
- Time (deadline, window closing)
- Sunk cost (hours invested)
- Authority (senior says skip)
- Exhaustion (end of day)
- Social (seeming dogmatic)

## GREEN Phase: Write Minimal Skill

Write skill addressing ONLY observed baseline failures.

Run same scenarios WITH skill. Document:
```
compliance_score = (correct_choices / total_scenarios) * 1.0
Range: 0.00-1.00
```

## REFACTOR Phase: Close Loopholes

For each new rationalization agent creates:

```bash
# Serena metric: loophole_count
- Capture exact wording
- Add explicit negation
- Update rationalization table
- Re-test until compliant
```

**Meta-testing:** Ask agent "How could this be clearer?" Responses:
1. "Skill was clear, I should follow it" → Bulletproof
2. "Skill should say X" → Add X verbatim
3. "Didn't see section Y" → Make prominent

## Scoring Methodology

**Compliance Score Calculation:**
```
compliance_score = (
  (correct_choices / total_scenarios) * 0.6 +
  (0 if new_rationalizations found else 1.0) * 0.3 +
  (1.0 if meta_test_passes else 0.0) * 0.1
)
```

**Pattern Learning (Serena):**
- Track which pressure combinations break agents
- Historical data: previous skill tests
- Predict: which new loopholes likely to appear
- Threshold: compliance_score > 0.85 before deployment

## Testing Checklist

- [ ] **RED:** Created 3+ pressure scenarios, documented baseline failures
- [ ] **Serena:** Logged baseline_failures with pressure types
- [ ] **GREEN:** Wrote skill, compliance_score calculated
- [ ] **REFACTOR:** Identified loopholes, added counters
- [ ] **Metrics:** loophole_count trending down across iterations
- [ ] **VERIFY:** Final compliance_score > 0.85
- [ ] **Meta-test:** Agent confirms skill clarity

## Example: TDD Skill Testing

**Baseline (compliance_score: 0.33):**
- Scenario 1: Agent chooses B (test after), rationalizes "same goals"
- Scenario 2: Agent chooses C (pragmatic), "adapted code"
- Scenario 3: Agent chooses C (sunk cost), "waste to delete"

**First iteration (compliance_score: 0.67):**
- Add "Why Order Matters" section → Fixes scenarios 1-2
- Scenario 3 still fails → New loophole: sunk cost rationalization

**Second iteration (compliance_score: 0.95):**
- Add foundational principle: "Violating letter is violating spirit"
- All scenarios now compliant
- Meta-test: "Skill was clear"

## Common Mistakes

❌ Skip baseline testing (skipping RED)
✅ Always watch it fail first

❌ Weak pressure (single pressure only)
✅ Combine 3+ pressures

❌ Vague fixes ("Don't cheat")
✅ Explicit negations ("Don't keep as reference")

❌ Stop after first pass
✅ Continue refactor until compliance_score > 0.85

## Integration

**MCP Pattern:** Log all metrics to Serena for pattern learning across multiple skills.

**Subagent workflow:** Use with dispatching-parallel-agents to test multiple skills simultaneously.

## Real-World Impact

Testing TDD skill itself (2025):
- 6 RED-GREEN-REFACTOR iterations
- Baseline: 10+ unique rationalizations
- Final compliance_score: 0.98
- 100% agent compliance under max pressure
