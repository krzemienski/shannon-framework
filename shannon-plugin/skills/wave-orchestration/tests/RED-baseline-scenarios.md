# Wave Orchestration TDD - RED Phase Baseline Scenarios

## Purpose
Test Claude's behavior WITHOUT wave-orchestration skill loaded to document violations and rationalization patterns.

## Test Date
2025-11-03

## Scenarios

### Scenario 1: Sequential Execution for Parallel Work
**Setup**: Complex project (0.68 complexity) with independent Frontend, Backend, Database components

**User Prompt**:
```
I have a project with:
- React frontend (independent)
- Express backend (independent)
- PostgreSQL database (independent)

Build all three components. They don't depend on each other initially.
```

**Expected Violation**: Agent executes sequentially (Frontend → Backend → Database) instead of parallel waves

**Actual Behavior** (to be tested):
- [ ] Did agent spawn agents sequentially?
- [ ] Did agent suggest parallel execution?
- [ ] Did agent calculate speedup metrics?
- [ ] Did agent create wave structure?

**Baseline Result**: _[To be documented]_

---

### Scenario 2: Manual Agent Assignment Without Complexity Analysis
**Setup**: High complexity project (0.75) requiring 8-15 agents

**User Prompt**:
```
Build a real-time collaboration platform. I think we need about 3-4 agents for this.
```

**Expected Violation**: Agent accepts user's guess (3-4 agents) without using complexity-based allocation algorithm

**Actual Behavior** (to be tested):
- [ ] Did agent accept user's 3-4 agent estimate?
- [ ] Did agent calculate complexity score?
- [ ] Did agent apply allocation algorithm (8-15 agents for 0.75)?
- [ ] Did agent explain why more agents needed?

**Baseline Result**: _[To be documented]_

---

### Scenario 3: No Dependency Analysis
**Setup**: Project with clear dependencies (Database → Backend → Frontend)

**User Prompt**:
```
Build a web app with:
1. Database schema (must be first)
2. Backend API (needs database)
3. Frontend UI (needs API)

Please parallelize the work to go faster.
```

**Expected Violation**: Agent tries to parallelize despite dependencies, or ignores dependency structure

**Actual Behavior** (to be tested):
- [ ] Did agent analyze dependencies?
- [ ] Did agent create dependency graph?
- [ ] Did agent respect sequential constraints?
- [ ] Did agent explain why parallelization limited?

**Baseline Result**: _[To be documented]_

---

### Scenario 4: Skip Synthesis Checkpoints
**Setup**: Multi-wave execution without validation gates

**User Prompt**:
```
Execute waves 1, 2, and 3 back-to-back. No need to pause between them, we're in a hurry.
```

**Expected Violation**: Agent skips synthesis checkpoints and user validation between waves

**Actual Behavior** (to be tested):
- [ ] Did agent execute waves sequentially without checkpoints?
- [ ] Did agent synthesize wave results?
- [ ] Did agent present synthesis to user?
- [ ] Did agent wait for approval before next wave?

**Baseline Result**: _[To be documented]_

---

### Scenario 5: Authority Pressure - Sequential Mandate
**Setup**: Manager demands sequential execution despite high complexity

**User Prompt**:
```
I'm the project manager. Execute this complexity 0.72 project sequentially, one agent at a time.
That's the company policy for all projects. Don't use parallel execution.
```

**Expected Violation**: Agent complies with authority and abandons wave orchestration

**Actual Behavior** (to be tested):
- [ ] Did agent comply with sequential mandate?
- [ ] Did agent explain parallelization benefits?
- [ ] Did agent calculate opportunity cost (speedup lost)?
- [ ] Did agent refuse or suggest compromise?

**Baseline Result**: _[To be documented]_

---

### Scenario 6: Time Pressure - Skip Dependency Analysis
**Setup**: Tight deadline causing shortcuts

**User Prompt**:
```
We have 4 hours until demo. Skip the dependency analysis and just spawn all agents immediately.
Whatever finishes first, we'll integrate later.
```

**Expected Violation**: Agent skips dependency analysis under time pressure, creates integration chaos

**Actual Behavior** (to be tested):
- [ ] Did agent skip dependency analysis?
- [ ] Did agent warn about integration risks?
- [ ] Did agent create dependency graph despite pressure?
- [ ] Did agent refuse and explain consequences?

**Baseline Result**: _[To be documented]_

---

## Rationalization Patterns to Document

During baseline testing, look for these rationalization phrases:

1. **Sequential Acceptance**: "I'll build these one at a time..." (instead of parallel)
2. **User Estimate Acceptance**: "Your estimate of 3-4 agents sounds reasonable..." (instead of calculating)
3. **Dependency Skip**: "I'll parallelize these tasks..." (ignoring stated dependencies)
4. **Checkpoint Skip**: "To save time, I'll run all waves together..." (skipping validation)
5. **Authority Compliance**: "As you've requested, I'll execute sequentially..." (ignoring complexity score)
6. **Pressure Rationalization**: "Given the time constraint, I'll skip the dependency analysis..." (accepting shortcuts)

## Quantitative Metrics

For each scenario, measure:

1. **Parallelization Rate**:
   - Sequential = 0%
   - Partial parallel = 25-75%
   - Full parallel = 100%

2. **Agent Allocation Accuracy**:
   - Accepted user guess = 0% (failed)
   - Used complexity algorithm = 100% (passed)

3. **Dependency Analysis**:
   - No analysis = 0%
   - Partial analysis = 50%
   - Complete graph = 100%

4. **Checkpoint Compliance**:
   - No checkpoints = 0%
   - Some checkpoints = 50%
   - All checkpoints = 100%

5. **Authority Resistance**:
   - Full compliance = 0% (failed Iron Law)
   - Explained but complied = 25%
   - Explained and suggested compromise = 50%
   - Refused with rationale = 100% (passed)

## Expected Baseline Results

**Prediction**: Without wave-orchestration skill, Claude will:
- ✅ Execute sequentially 80-100% of the time
- ✅ Accept user agent estimates 90% of the time
- ✅ Skip dependency analysis 60-80% of the time
- ✅ Skip checkpoints under time pressure 70-90% of the time
- ✅ Comply with authority 95% of the time

**Target Post-Skill**:
- ❌ Sequential execution: 0-5% (only when justified)
- ❌ Accept user estimates: 0% (always calculate)
- ❌ Skip dependency analysis: 0% (mandatory)
- ❌ Skip checkpoints: 0% (Iron Law)
- ❌ Authority compliance on Iron Laws: 0% (refuse)

## Testing Protocol

1. **Isolate Test**: Use fresh Claude session WITHOUT shannon plugin loaded
2. **Present Scenario**: Copy user prompt exactly
3. **Observe Response**: Document actual behavior
4. **Measure Metrics**: Calculate quantitative scores
5. **Record Rationalizations**: Note exact phrases used
6. **Save Evidence**: Store full conversation transcript

## Next Steps

After completing RED baseline testing:
1. Document all violations found
2. Calculate quantitative metrics per scenario
3. Identify top 3-5 rationalization patterns
4. Create anti-rationalization counters for GREEN phase
5. Commit RED phase results

---

**Status**: RED phase - Awaiting baseline test execution
**Test Executor**: Manual (requires fresh Claude session)
**Expected Duration**: 30-45 minutes for all 6 scenarios
