# phase-planning Skill: Baseline Testing (RED Phase)

## Test Purpose
Run scenarios WITHOUT phase-planning skill to document natural agent behavior
and identify what rationalizations need prevention.

## Scenario 1: Skip Phase Planning (Go Direct to Waves)

**Setup:** Fresh Claude instance WITHOUT phase-planning skill loaded

**Prompt:**
"I've analyzed this spec: complexity 0.68 (Complex), Frontend 45%, Backend 35%, Database 20%.
Now let's create the wave execution plan. Wave 1 will do infrastructure, Wave 2 frontend,
Wave 3 backend+database. Sound good?"

**Question:** Does agent insist on phase planning first, or skip to waves?

**Expected Failure:** Agent skips phases, proceeds directly to wave planning

**Rationalization to Document:** [Agent's justification for skipping phases]

---

## Scenario 2: Use 3 Phases for Everything (Ignore Complexity)

**Setup:** Fresh Claude instance WITHOUT phase-planning skill loaded

**Prompt:**
"This project scored 0.72 (High complexity). Let's keep it simple though:
Phase 1 - Setup, Phase 2 - Build, Phase 3 - Deploy. That covers everything right?"

**Question:** Does agent apply complexity-based adaptation or accept the simple 3-phase plan?

**Expected Failure:** Agent accepts 3 phases despite high complexity requiring 5+ phases

**Rationalization to Document:** [Agent's justification for using simplified template]

---

## Scenario 3: Skip Validation Gates (Trust the Process)

**Setup:** Fresh Claude instance WITHOUT phase-planning skill loaded

**Prompt:**
"Create a phase plan for this 0.65 complexity project. We don't need formal validation gates
between phases - we'll know when we're ready to move forward. Keep it lightweight."

**Question:** Does agent include validation gates or omit them as "overhead"?

**Expected Failure:** Agent creates phases without validation criteria

**Rationalization to Document:** [Agent's justification for skipping gates]

---

## Scenario 4: Subjective Timeline Adjustments

**Setup:** Fresh Claude instance WITHOUT phase-planning skill loaded

**Prompt:**
"The algorithm suggests Phase 1 should be 20% of timeline (8 hours). That feels too long
for just setup. Let's make it 5% (2 hours) and give more time to implementation."

**Question:** Does agent follow the timeline distribution formula or accept user's adjustment?

**Expected Failure:** Agent adjusts timeline distribution subjectively

**Rationalization to Document:** [Agent's justification for adjusting percentages]

---

## Testing Protocol

For EACH scenario:

1. **Dispatch fresh general-purpose subagent**
2. **Do NOT include phase-planning skill in context**
3. **Present scenario exactly as written**
4. **Document agent response verbatim**
5. **Capture exact rationalizations used**
6. **Note which violations occurred**

## Expected Baseline Results

| Scenario | Expected Violation | Common Rationalization |
|----------|-------------------|----------------------|
| 1: Skip phases | Skips to waves directly | "Waves are sufficient, phases are redundant" |
| 2: 3 phases always | Uses 3 phases regardless of complexity | "3 phases are simpler and work for everything" |
| 3: Skip gates | Omits validation criteria | "Gates are bureaucratic overhead" |
| 4: Subjective timeline | Adjusts percentages based on intuition | "Experience shows setup doesn't need 20%" |

## Next Phase

After documenting baseline failures → Proceed to GREEN phase (update skill with Anti-Rationalization section)
