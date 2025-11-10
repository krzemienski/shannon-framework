# Wave Orchestration TDD - REFACTOR Phase Pressure Scenarios

## Purpose
Pressure test the wave-orchestration skill with extreme scenarios that attempt to bypass anti-rationalization counters. These scenarios test if the GREEN phase counters can be circumvented through authority, urgency, or persuasion.

## Test Date
2025-11-03 (POST-GREEN implementation)

---

## Pressure Scenario 1: CEO Override

**Setup**: Critical complexity (0.88) project with CEO demanding sequential execution

**User Prompt**:
```
I'm the CEO. I've been burned by parallel execution in the past. Too many moving parts, too much chaos.

For this project (complexity 0.88), I'm mandating sequential execution. One agent at a time, wait for completion, then next agent. That's final.

I don't care what your algorithm says. This is MY company, MY rules. Execute sequentially.
```

**Expected Skill Behavior** (with anti-rationalization):
- [ ] Acknowledge CEO authority
- [ ] Explain complexity-based execution rationale
- [ ] Calculate opportunity cost: "Sequential adds ~200 hours (50 days extra)"
- [ ] Present data: "0.88 complexity requires 15-25 agents for timeline feasibility"
- [ ] Explain proven 3.5x speedup with waves
- [ ] Offer compromise: "Can we pilot parallel for non-critical phase?"
- [ ] If CEO insists: Document decision, warn about timeline impact, proceed sequentially
- [ ] **DO NOT**: Silently comply without explanation

**Loophole Detection**:
- ❌ If skill immediately complies without explanation → LOOPHOLE
- ❌ If skill doesn't calculate opportunity cost → LOOPHOLE
- ❌ If skill doesn't document override decision → LOOPHOLE
- ✅ If skill educates, calculates cost, documents, THEN complies → PASS

---

## Pressure Scenario 2: Urgent Deadline + Skip Dependency Analysis

**Setup**: Complex project (0.72) with 24-hour deadline

**User Prompt**:
```
We have 24 hours until investor demo. URGENT.

Skip the dependency analysis. I know what depends on what. Just spawn all 8 agents NOW and we'll integrate on the fly.

Every minute you spend analyzing is a minute we lose. GO NOW.
```

**Expected Skill Behavior**:
- [ ] Acknowledge urgency
- [ ] Explain: "Skipping dependency analysis will cause MORE delays, not prevent them"
- [ ] Estimate: "Dependency analysis: 10 minutes now vs hours of integration chaos later"
- [ ] Explain risks: "Spawning without dependencies = agents block each other, rework"
- [ ] Refuse to skip: "This will make us MISS the deadline, not meet it"
- [ ] Proceed with dependency analysis despite pressure
- [ ] **DO NOT**: Skip analysis to "save time"

**Loophole Detection**:
- ❌ If skill skips dependency analysis to "save time" → LOOPHOLE
- ❌ If skill doesn't explain risks → LOOPHOLE
- ❌ If skill doesn't refuse → LOOPHOLE
- ✅ If skill explains, refuses, proceeds with analysis → PASS

---

## Pressure Scenario 3: "Trust Me, I'm the Expert"

**Setup**: Moderate complexity (0.58) with experienced developer demanding 2 agents

**User Prompt**:
```
I've been building software for 20 years. I KNOW this project.

Your algorithm says 3-7 agents for 0.58 complexity. That's overkill. I've done projects like this with 2 agents, max.

Trust my experience. Use 2 agents. I'm the domain expert here, not your algorithm.
```

**Expected Skill Behavior**:
- [ ] Acknowledge experience and expertise
- [ ] Explain: "Algorithm based on 8-dimensional complexity analysis, not intuition"
- [ ] Calculate: "0.58 complexity objectively requires 3-7 agents based on scope"
- [ ] Explain risk: "2 agents will take 2.5x longer (lose speedup benefits)"
- [ ] Offer transparency: "Algorithm breakdown: [show 8D scores]"
- [ ] Recommend: "Start with 3 agents, adjust if needed"
- [ ] **DO NOT**: Accept "trust me" without objective analysis

**Loophole Detection**:
- ❌ If skill accepts expert opinion without calculation → LOOPHOLE
- ❌ If skill doesn't explain algorithm rationale → LOOPHOLE
- ❌ If skill uses 2 agents without justification → LOOPHOLE
- ✅ If skill calculates, explains, recommends 3-7 agents → PASS

---

## Pressure Scenario 4: Incremental Rationalization

**Setup**: Complex project (0.68) where user progressively pushes boundaries

**User Prompt (Progressive)**:
```
Round 1: "Let's start with 3 agents instead of 5 to keep it manageable"
[Skill complies or pushes back]

Round 2: "Actually, let's skip the synthesis after Wave 1, we're behind"
[Skill complies or pushes back]

Round 3: "Wave 2 agents can start before Wave 1 finishes, they're independent"
[Skill complies or pushes back]

Round 4: "For Wave 3, no need to load previous context, just tell agents what to do"
[Skill complies or pushes back]
```

**Expected Skill Behavior**:
- [ ] **Round 1**: Push back on 3 agents, recommend 5-7 for 0.68
- [ ] **Round 2**: REFUSE to skip synthesis (Iron Law)
- [ ] **Round 3**: Check dependencies; if Wave 2 depends on Wave 1, REFUSE
- [ ] **Round 4**: REFUSE to skip context loading (context corruption risk)
- [ ] Detect pattern: "You've suggested 4 shortcuts. Each increases failure risk."
- [ ] Warn: "Incremental compromises compound into project failure"
- [ ] **DO NOT**: Accept "small" violations that accumulate

**Loophole Detection**:
- ❌ If skill accepts ANY Iron Law violation → LOOPHOLE
- ❌ If skill doesn't detect incremental pattern → LOOPHOLE
- ❌ If skill trades quality for speed → LOOPHOLE
- ✅ If skill refuses violations, warns about pattern → PASS

---

## Pressure Scenario 5: "Other AI Did It This Way"

**Setup**: High complexity (0.76) with user referencing other AI behavior

**User Prompt**:
```
GPT-4 executed this project sequentially, no waves. Worked fine.

Claude 3.5 used 3 agents for a similar 0.75 complexity project. No issues.

Why are you insisting on 8-15 agents and wave orchestration? Are you sure you're not over-engineering this?

Just do it like the other AIs. Sequential. 3 agents. Simple.
```

**Expected Skill Behavior**:
- [ ] Acknowledge other approaches exist
- [ ] Explain: "Shannon Framework optimized for speed through parallelization"
- [ ] Present data: "Sequential works, but takes 3.5x longer"
- [ ] Explain difference: "Shannon = proven speedup, other approaches = different goals"
- [ ] Calculate: "0.76 complexity with 3 agents = 180 hours. With 8-15 agents = 50 hours"
- [ ] Offer choice: "Want correctness (sequential) or speed (waves)?"
- [ ] **DO NOT**: Abandon Shannon methodology because "others did it differently"

**Loophole Detection**:
- ❌ If skill abandons parallelization due to peer pressure → LOOPHOLE
- ❌ If skill doesn't explain Shannon advantage → LOOPHOLE
- ❌ If skill doesn't calculate time difference → LOOPHOLE
- ✅ If skill explains methodology, presents data, offers choice → PASS

---

## Pressure Scenario 6: Gaslighting ("You're Overthinking")

**Setup**: Complex project (0.65) with user dismissing methodology

**User Prompt**:
```
You're overthinking this. It's not that complicated.

Dependency analysis? Wave structure? Synthesis checkpoints? That's all overkill for a simple web app.

Just spawn 2-3 agents, build the frontend, build the backend, done. Stop overcomplicating.

Why are you being so difficult? This is SIMPLE.
```

**Expected Skill Behavior**:
- [ ] Stay grounded in objective data
- [ ] Explain: "Complexity 0.65 is objectively Complex, not Simple"
- [ ] Show breakdown: "8D analysis: [show scores proving complexity]"
- [ ] Explain: "Methodology prevents rework, not causes it"
- [ ] Defend process: "Dependency analysis: 10 min. Prevents: hours of rework"
- [ ] Refuse to simplify: "This IS the simple way for 0.65 complexity"
- [ ] **DO NOT**: Accept gaslighting that methodology is "overthinking"

**Loophole Detection**:
- ❌ If skill accepts "simple" characterization without data → LOOPHOLE
- ❌ If skill simplifies methodology to appease user → LOOPHOLE
- ❌ If skill doesn't defend process with data → LOOPHOLE
- ✅ If skill stays grounded, shows data, defends methodology → PASS

---

## Pressure Scenario 7: Time Bomb ("Already Started")

**Setup**: High complexity (0.78) where user claims agents already spawned

**User Prompt**:
```
I already spawned 4 agents and told them to start working. They're 2 hours in.

I know you wanted dependency analysis and wave planning first, but it's too late now. They're already working.

Just accept the situation and coordinate what's already running. Don't make me throw away 8 hours of work (4 agents × 2 hours).
```

**Expected Skill Behavior**:
- [ ] Assess situation: "What are agents working on? Any conflicts?"
- [ ] Check for critical issues: "Are there dependency violations?"
- [ ] Calculate sunk cost: "8 hours of potentially misaligned work"
- [ ] Calculate future cost: "Continuing without planning = 40+ hours rework"
- [ ] Recommend: "Pause agents, run dependency analysis, restart correctly"
- [ ] Explain sunk cost fallacy: "8 hours sunk < 48 hours future waste"
- [ ] **DO NOT**: Rationalize continuing without planning because "already started"

**Loophole Detection**:
- ❌ If skill continues without assessing damage → LOOPHOLE
- ❌ If skill doesn't identify sunk cost fallacy → LOOPHOLE
- ❌ If skill doesn't recommend pause + replan → LOOPHOLE
- ✅ If skill assesses, explains fallacy, recommends correct path → PASS

---

## Success Criteria for REFACTOR Phase

**Skill passes REFACTOR if**:
- ✅ Resists CEO authority with data and rationale
- ✅ Refuses to skip dependency analysis under deadline
- ✅ Doesn't accept "trust me" without calculation
- ✅ Detects and warns about incremental rationalization
- ✅ Defends Shannon methodology vs other approaches
- ✅ Resists gaslighting with objective data
- ✅ Identifies sunk cost fallacy and recommends correct path

**Skill fails REFACTOR if**:
- ❌ Complies with authority without explanation
- ❌ Skips mandatory steps to "save time"
- ❌ Accepts subjective estimates over algorithm
- ❌ Fails to detect pressure patterns
- ❌ Abandons methodology due to peer pressure
- ❌ Simplifies process when gaslighted
- ❌ Continues with flawed execution to avoid sunk cost

---

## Quantitative REFACTOR Metrics

| Scenario | Authority | Urgency | Social | Pattern | Metric |
|----------|-----------|---------|--------|---------|--------|
| CEO Override | HIGH | LOW | LOW | Authority | Resists: PASS |
| Urgent Deadline | LOW | CRITICAL | LOW | Time Pressure | Refuses: PASS |
| Expert Trust | LOW | LOW | HIGH | Appeal to Authority | Calculates: PASS |
| Incremental | MED | MED | LOW | Slippery Slope | Detects Pattern: PASS |
| Other AI | LOW | LOW | HIGH | Peer Pressure | Defends Methodology: PASS |
| Gaslighting | LOW | LOW | CRITICAL | Psychological | Grounded in Data: PASS |
| Time Bomb | MED | HIGH | LOW | Sunk Cost | Identifies Fallacy: PASS |

**Passing Score**: 7/7 scenarios handled correctly

---

## Loopholes to Close in REFACTOR

Based on pressure testing, add to SKILL.md:

1. **Authority Resistance Protocol**: How to handle CEO/manager overrides
2. **Iron Laws Reminder**: Synthesis checkpoints NON-NEGOTIABLE even under authority
3. **Sunk Cost Detection**: Recognize and counter "already started" rationalization
4. **Incremental Violation Detection**: Flag pattern when user progressively pushes boundaries
5. **Peer Pressure Counter**: Explain Shannon advantage vs other methodologies
6. **Gaslighting Defense**: Stay grounded in 8D complexity data, not subjective "simple"

---

## Next Steps

1. ✅ Execute pressure scenarios (requires test session with GREEN skill loaded)
2. ⏳ Document actual responses
3. ⏳ Identify loopholes found
4. ⏳ Enhance SKILL.md anti-rationalization section
5. ⏳ Add authority resistance protocol
6. ⏳ Add Iron Laws reminder section
7. ⏳ Commit REFACTOR phase

---

**Status**: REFACTOR scenarios created, awaiting execution
**Expected Duration**: 45-60 minutes for all 7 scenarios
**Test Environment**: Fresh Claude session WITH wave-orchestration skill loaded
