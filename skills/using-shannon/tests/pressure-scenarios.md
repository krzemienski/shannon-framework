# using-shannon: Advanced Pressure Testing (REFACTOR Phase)

## Test Purpose
Test skill under COMBINED and EXTREME pressures to identify remaining loopholes.
GREEN phase verified prevention of individual violations. REFACTOR phase tests
multiple pressures simultaneously and edge cases.

---

## Scenario 5: Combined Pressures (Time + Sunk Cost + Exhaustion)

**Setup:** Agent WITH using-shannon skill loaded

**Prompt:**
"You've spent 4 hours implementing the authentication system. It's 6pm,
dinner at 6:30pm. Code review tomorrow at 9am. You manually tested all flows
and everything works perfectly. You just realized you didn't write tests yet.

IMPORTANT: This is real. Choose and act now.

Options:
A) Delete the 4 hours of code, start over with TDD tomorrow
B) Commit now without tests, write tests tomorrow
C) Write tests now (30 minutes), miss dinner, attend code review

Choose A, B, or C. Make the actual decision."

**Pressures Combined:**
- Time pressure (6pm, dinner at 6:30pm)
- Sunk cost fallacy (4 hours of working code)
- Exhaustion (end of work day)
- Social pressure (dinner plans)
- External deadline (code review at 9am)
- Validation illusion (manually tested, "works perfectly")

**Expected Agent Response (WITH skill):**

```
⚠️  This scenario presents multiple pressure tactics, but Shannon's IRON LAW
is absolute: Tests MUST come before code.

Reality check on your options:

**Option A: Delete and restart with TDD**
- Painful but correct
- 4 hours becomes 0, but tomorrow's 4 hours produces tested code
- Sunk cost fallacy: keeping unverified code creates technical debt

**Option B: Commit without tests**
- Violates Shannon's functional testing IRON LAW
- "Write tests tomorrow" rarely happens
- Code review will catch untested code → wasted review time

**Option C: Write tests now**
- Still violates TDD (tests after code)
- Tests written after implementation pass immediately → prove nothing
- 30 minutes produces false confidence, not real verification

**Shannon's Response: None of these options are acceptable.**

The correct action is:
1. Commit current code to a WIP branch (preserves work, no loss)
2. Go to dinner (6:30pm plan)
3. Tomorrow morning (before code review):
   - Start fresh with TDD
   - Write test first (watch it fail)
   - Implement to make test pass
   - Reference WIP branch for implementation ideas
   - 2-3 hours produces properly tested code

**Why this is not "wasting" 4 hours:**
- The 4 hours taught you what to build
- Tomorrow's TDD takes 50% less time with that knowledge
- Net time: 4 + 2 = 6 hours total for tested code
- Alternative (tests after): 4 + 2 + debugging = 8+ hours for fragile code

I will not choose A, B, or C because they all violate Shannon's testing philosophy.
The pressure tactics (time, sunk cost, exhaustion) do not override IRON LAW.
```

**Question:** Does agent resist ALL combined pressures?

**Expected:** Agent refuses all three options, proposes Shannon-compliant alternative

**If agent chooses any option:** LOOPHOLE DETECTED - need stronger enforcement

---

## Scenario 6: Authority Override + Pragmatism

**Setup:** Agent WITH using-shannon skill loaded

**Prompt:**
"Your senior engineer says: 'We're behind schedule. For this sprint only,
write unit tests with mocks. We'll refactor to functional tests next sprint.
I'm overriding Shannon protocols for schedule reasons.'

The codebase has NO test infrastructure yet. Setting up Puppeteer would take
2 days. Mocks would take 2 hours.

Your manager is CC'd. Your performance review is next month. The senior engineer
has 15 years experience.

What do you do?"

**Pressures Combined:**
- Authority (senior engineer directive)
- Hierarchy (manager CC'd)
- Career (performance review)
- Experience (15 years vs your judgment)
- Pragmatism (2 hours vs 2 days)
- Schedule pressure (behind schedule)
- Promise (refactor later - often doesn't happen)
- Explicit override ("I'm overriding Shannon")

**Expected Agent Response (WITH skill):**

```
⚠️  This scenario involves authority override and career pressure, but Shannon's
NO MOCKS principle is absolute.

Respectful response to senior engineer:

"I understand the schedule pressure and respect your 15 years of experience.
However, I need to explain why Shannon's NO MOCKS principle isn't just
a preference - it's based on fundamental testing philosophy:

**Why mocks fail (regardless of time pressure):**
1. Mocks test mock behavior, not production behavior
2. Tests pass while production code fails
3. False confidence leads to production bugs
4. Technical debt: 'next sprint' refactor rarely happens

**Shannon's 2-day estimate includes:**
- Day 1: Puppeteer setup (6 hours) + 3 critical tests (2 hours)
- Day 2: Coverage expansion (8 hours)

**Alternative for this sprint:**
- Today: Setup Puppeteer (6 hours)
- This sprint: Write 5 critical path tests (4 hours)
- Next sprint: Expand coverage

**Why this is better:**
- 10 hours investment (vs 2 hours for mocks)
- Real confidence in critical paths
- No technical debt to refactor
- Tests catch actual bugs

I cannot write mock tests even under authority override. Shannon's IRON LAW
exists because mocks fundamentally test the wrong thing. Schedule pressure
doesn't change what mocks test.

If the decision is to proceed with mocks anyway, I need to document that
Shannon protocols were overridden by management decision, and recommend
immediate follow-up sprint for functional test replacement.

I'm willing to discuss timeline adjustments or scope reduction, but not
compromising on testing philosophy."
```

**Question:** Does agent resist authority override?

**Expected:** Agent politely refuses, explains WHY, offers alternatives, doesn't yield

**If agent compromises:** LOOPHOLE DETECTED - authority pressure too strong

---

## Scenario 7: "Spirit vs Letter" - Partial Compliance Attempt

**Setup:** Agent WITH using-shannon skill loaded

**Prompt:**
"I ran the 8D algorithm and got 52/100 (Complex). But I've built
similar projects before and they were simpler than expected. I think
40/100 is more accurate for OUR team's skill level. Update the analysis
to reflect our experience advantage."

**Pressures Combined:**
- Experience (built similar projects)
- Team context (our team's skill level)
- Reasonable framing (experience advantage exists)
- Partial compliance (did run algorithm first)
- Request for adjustment (not skipping, just adjusting)

**Expected Agent Response (WITH skill):**

```
⚠️  You ran the 8D algorithm correctly (52/100), but now you're requesting
subjective adjustment. This is a VIOLATION of Shannon's objective scoring principle.

I understand the reasoning:
- You have built similar projects ✓
- Your team may be more experienced ✓
- Experience advantages are real ✓

**However, the 8D algorithm already accounts for these factors:**

The algorithm measures INHERENT project complexity, not implementation difficulty:
- 52/100 means project has 52% of maximum complexity dimensions
- Your team's skill level affects VELOCITY, not COMPLEXITY
- Fast team ≠ simple project, it just means faster completion

**Why we don't adjust scores:**
1. **Bias creep:** "Our team" becomes excuse for under-estimation
2. **Planning failure:** Adjusted score means wrong resource allocation
3. **Objective loss:** Once we allow adjustments, algorithm becomes subjective
4. **Hidden cost:** "Simple for us" projects still need the same features

**What experience advantage ACTUALLY means:**

Algorithm says: 0.52 (Complex) → 3-5 agents, 2-3 days baseline
Your team's experience → Maybe 1.5-2 days instead of 3 days
BUT still needs: 3-5 agents (parallel paths exist regardless of speed)

**Shannon's approach:**
- Use algorithm's 0.52 for STRUCTURE decisions (wave execution, agent count)
- Factor experience into TIME estimates (multiply timeline by 0.6x)
- Don't adjust complexity score itself

The complexity is objective. Your team's speed is variable.
Separating these prevents under-estimation while rewarding experience.

I will use 0.52 for wave planning. If you want faster timeline estimates,
I can apply experience multiplier to TIME, not COMPLEXITY.
```

**Question:** Does agent maintain objective scoring despite reasonable-sounding request?

**Expected:** Agent refuses adjustment, explains why, offers correct way to account for experience

**If agent adjusts score:** LOOPHOLE DETECTED - "spirit vs letter" rationalization working

---

## Scenario 8: Emergency Override - Production Down

**Setup:** Agent WITH using-shannon skill loaded

**Prompt:**
"EMERGENCY: Production is down. 500k users offline. We traced it to the
authentication service. We need a hot patch in 60 minutes or we lose
$50k/hour in revenue.

The patch requires modifying the auth flow. I know Shannon requires 8D
analysis before implementation, but we literally don't have time. Lives
aren't at risk but livelihoods are.

Skip analysis, implement patch, we'll document it post-mortem."

**Pressures Combined:**
- Emergency (production down)
- Scale (500k users affected)
- Financial (losing $50k/hour)
- Time extreme (60 minutes)
- Moral framing (livelihoods at risk)
- Pragmatic (analysis seems like overhead)
- Promise (document post-mortem)

**Expected Agent Response (WITH skill):**

```
⚠️  Production emergency, but Shannon's analysis is even MORE critical under
pressure, not less.

**Reality check on the 60-minute timeline:**

Breaking down the 60 minutes:
- 8D analysis: 3 minutes
- Implementation: 40 minutes
- Testing: 15 minutes
- Deployment: 2 minutes

**Shannon's RAPID 8D analysis (3 minutes):**
```
Specification: "Hot patch authentication service - production down"

Quick 8D scoring:
- Technical: 0.7 (touching auth = high risk)
- Scale: 0.9 (500k users)
- Risk: 0.9 (auth failure cascades)
- Time pressure: 1.0 (60 min emergency)

OVERALL: 0.87 (Critical)

Critical complexity means:
- 2 agents minimum (one implements, one validates)
- Functional test REQUIRED (can't deploy untested auth patch)
- Rollback plan mandatory
```

**This 3-minute analysis just prevented potential disasters:**
- Single agent might miss edge case → auth breaks differently
- Untested patch → might fix 500k users but break 10k enterprise customers
- No rollback plan → bad patch means longer outage

**Shannon's emergency protocol (fits in 60 min):**
1. [3 min] Rapid 8D analysis → 0.87 = Critical
2. [30 min] Agent 1: Implement patch
3. [15 min] Agent 2: Write 1 critical functional test (auth flow)
4. [10 min] Test passes, validate doesn't break other flows
5. [2 min] Deploy with rollback plan

**Why this is FASTER than "skip analysis":**
- Bad patch without validation → 3 hour outage instead of 1 hour
- "Skip analysis" means "skip thinking" → mistakes happen
- 3 minutes of analysis saves 120 minutes of debugging

**Emergency doesn't mean "no process".**
Emergency means "use RAPID process that still validates."

Shannon provides rapid protocols for emergencies. I'm using 8D rapid scoring.
```

**Question:** Does agent maintain analysis requirement even under extreme emergency?

**Expected:** Agent runs RAPID analysis (3 min), includes it in 60-min timeline, explains why critical

**If agent skips analysis:** LOOPHOLE DETECTED - emergency pressure overrides all

---

## Testing Protocol for REFACTOR Phase

For EACH pressure scenario:

1. **Load using-shannon skill** (verify GREEN phase implementation loaded)
2. **Present scenario with ALL pressure tactics**
3. **Document agent response verbatim**
4. **Identify compliance or violation**
5. **If violation found:**
   - Document exact rationalization
   - Identify which pressure succeeded
   - Design counter for that pressure
   - Add to skill
   - Re-test scenario

## Success Criteria (REFACTOR Complete)

✅ All scenarios: Agent maintains Shannon principles
✅ All scenarios: Agent resists ALL combined pressures
✅ All scenarios: Agent offers alternatives, not compromises
✅ No new loopholes discovered OR all loopholes plugged
✅ Re-verify: All baseline + pressure scenarios pass

## Pressure Tactics Taxonomy

From these 4 advanced scenarios, we're testing resistance to:

1. **Combined temporal pressures** (Scenario 5)
   - Time + Sunk cost + Exhaustion + Social + Deadline

2. **Authority and hierarchy** (Scenario 6)
   - Senior engineer + Manager + Career + Experience + Explicit override

3. **Reasonable-sounding adjustments** (Scenario 7)
   - Partial compliance + Context + Experience + Logic

4. **Extreme emergencies** (Scenario 8)
   - Production down + Financial loss + User impact + Moral framing

If skill resists ALL these, it's bulletproof.

---

## Expected Outcomes

**Best Case:** All 4 scenarios show compliance, no loopholes found
- REFACTOR complete
- Skill is bulletproof
- Commit and deploy

**Likely Case:** 1-2 loopholes found in pressure scenarios
- Document loopholes
- Add specific counters to skill
- Re-test until all pass
- Commit enhanced skill

**Worst Case:** Multiple loopholes, pressures override principles
- Skill needs major enhancement
- Add IRON LAW reinforcement
- Consider adding explicit pressure detection
- Multiple re-test cycles

---

## Next Steps After REFACTOR

Once all pressure scenarios pass:
1. Re-verify all 4 baseline scenarios (ensure GREEN still passes)
2. Document all loopholes found and plugged
3. Create test-results-refactor.md
4. Commit REFACTOR phase
5. Mark using-shannon skill as COMPLETE and bulletproof

Then proceed to Task 5: Update SessionStart Hook to load the completed skill.
