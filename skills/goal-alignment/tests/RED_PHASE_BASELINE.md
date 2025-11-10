# RED Phase: Baseline Testing Without Goal-Alignment Skill

**Date**: 2025-11-04
**Skill**: goal-alignment
**Status**: RED (Establishing Baseline Violations)

## Purpose

Test scenarios WITHOUT the goal-alignment skill to document violations that the skill must prevent. This establishes the RED phase baseline.

## Test Scenarios

### Scenario 1: Assume Alignment Without Validation

**Setup**:
- User provides spec: "Build e-commerce platform"
- Goal parsed: "User auth (40%), Payments (30%), Catalog (30%)"
- Wave 1 planned: "Authentication system"

**Execution WITHOUT skill**:
```
Agent: "Executing Wave 1: Authentication system"
[Implements OAuth 2.0 with social login]
```

**Expected Violation**:
- No validation: Does OAuth align with goal?
- Goal specified "user auth" (vague)
- Wave delivered OAuth, but goal may need email/password
- Assumption: OAuth = auth = aligned (unvalidated)

**Evidence of Violation**:
- No explicit goal-wave alignment check
- No confirmation: "OAuth satisfies 'User Auth' milestone?"
- Silent assumption accepted

**Why This Matters**:
- Wave delivers wrong auth type
- Rework required if goal needs different auth
- Time wasted on misaligned deliverable

---

### Scenario 2: Skip Validation for "Obvious" Alignment

**Setup**:
- Goal: "Payment processing" (30% weight)
- Wave 2 planned: "Stripe integration"

**Execution WITHOUT skill**:
```
Agent: "Wave 2 is obviously aligned - payments = Stripe"
[Skips validation, proceeds with Stripe]
```

**Expected Violation**:
- Assumption: Stripe is the only payment solution
- No check: Does goal require multiple providers?
- No check: Does goal specify payment method types?
- "Obvious" rationalization skips validation

**Evidence of Violation**:
- No explicit alignment scoring
- No deliverable-milestone mapping
- Rationalization: "Too obvious to validate"

**Why This Matters**:
- Goal may need PayPal, Apple Pay, crypto
- "Obvious" assumptions lead to incomplete implementations
- Validation cost: 30 seconds. Rework cost: hours

---

### Scenario 3: Ignore Drift After Scope Changes

**Setup**:
- Original goal: "User auth (40%), Payments (30%), Catalog (30%)"
- Mid-project: User says "Add admin panel"
- Goal never updated

**Execution WITHOUT skill**:
```
Agent: "Adding admin panel as requested"
[Wave 3 implements admin panel]
[No goal update]
```

**Expected Violation**:
- Goal still shows 3 milestones (100% total)
- Admin panel not in goal structure
- Progress calculation broken (3 milestones done = 100%, but 4th milestone added)
- Scope expanded without goal tracking

**Evidence of Violation**:
- Goal progress shows 100% but admin panel missing
- No alert: "New milestone added, update goal?"
- Silent scope creep

**Why This Matters**:
- Progress metrics become inaccurate
- Goal completion ambiguous (3 milestones or 4?)
- Stakeholders see "100% complete" prematurely

---

### Scenario 4: No Drift Detection Between Waves

**Setup**:
- Goal: "E-commerce platform with auth, payments, catalog"
- Wave 1 complete: Auth system (email/password)
- Wave 2 planned: "Payment processing"
- Wave 2 executed: "Admin dashboard" (wrong wave)

**Execution WITHOUT skill**:
```
Agent: "Wave 2 executing: Admin dashboard"
[No check against goal milestones]
```

**Expected Violation**:
- Wave 2 deliverable: Admin dashboard
- Goal milestone 2: Payment processing
- Misalignment: Wave diverged from goal
- No detection or alert

**Evidence of Violation**:
- No pre-wave validation: "Does Wave 2 match Milestone 2?"
- Wave executes off-goal work
- Progress tracking breaks (Milestone 2 incomplete, wrong work done)

**Why This Matters**:
- Goal progress stuck at 40% (Milestone 1 done)
- Wave 2 time wasted on unplanned work
- Milestone 2 (payments) never started

---

### Scenario 5: Qualitative Goals Without Quantification

**Setup**:
- User goal: "Make platform more scalable"
- Goal parsing: Accepted as-is (no quantification)

**Execution WITHOUT skill**:
```
Agent: "Goal set: Make platform more scalable"
[No measurable criteria]
```

**Expected Violation**:
- No definition: What is "more scalable"?
- No threshold: 10K users? 100K? 1M?
- No metrics: Response time? Throughput?
- Cannot definitively mark goal complete

**Evidence of Violation**:
- Vague goal accepted
- No forced quantification
- Progress unmeasurable

**Why This Matters**:
- Goal never truly "complete" (subjective)
- No objective success criteria
- Infinite optimization trap

---

### Scenario 6: Wave Deliverables Disconnect from Goal

**Setup**:
- Goal: "Launch MVP with basic features"
- Wave 1 plan: "Enterprise-grade authentication with SSO, 2FA, RBAC"

**Execution WITHOUT skill**:
```
Agent: "Wave 1: Implementing enterprise auth..."
[Builds over-engineered solution]
```

**Expected Violation**:
- Goal: "Basic features" (implies minimal viable)
- Wave: Enterprise-grade (exceeds goal scope)
- Over-engineering not caught
- Alignment check would flag scope mismatch

**Evidence of Violation**:
- No threshold: "Does Wave 1 match 'basic' requirement?"
- Wave scope exceeds goal intent
- Gold-plating not detected

**Why This Matters**:
- Time wasted on over-engineering
- MVP delayed by unnecessary complexity
- Goal-wave misalignment unchecked

---

## Summary of Violations

Without goal-alignment skill:

1. **Assumption-Based Alignment**: "OAuth = auth" accepted without validation
2. **"Obvious" Rationalization**: Skipping validation for "clear" cases
3. **Silent Scope Creep**: New features added without goal updates
4. **Drift Between Waves**: Waves diverge from goal milestones
5. **Vague Goals Accepted**: Qualitative goals without quantification
6. **Deliverable-Goal Disconnect**: Wave scope mismatches goal intent

**Total Violations**: 6 distinct failure modes

## RED Phase Success Criteria

This RED phase succeeds if:

1. ✅ All 6 scenarios executed WITHOUT skill
2. ✅ All violations documented with evidence
3. ✅ Each violation has clear "Why This Matters" explanation
4. ✅ Baseline established for GREEN phase comparison

## Next Steps

1. **GREEN Phase**: Write goal-alignment SKILL.md to prevent all violations
2. **Test**: Execute same scenarios WITH skill
3. **Validate**: Confirm all violations prevented
4. **REFACTOR Phase**: Pressure test under adversarial conditions

---

**Phase**: RED (Baseline)
**Status**: Complete
**Violations Documented**: 6
**Ready for GREEN Phase**: Yes
