# Wave Execution Plan Template

## Project Information

**Project Name**: [Project Name]
**Complexity Score**: [0.0-1.0]
**Interpretation Band**: [Simple/Moderate/Complex/High/Critical]
**Total Timeline**: [X hours/days]
**Wave Strategy**: [Sequential/Parallel]
**Expected Speedup**: [Xx faster than sequential]

---

## Dependency Analysis

### Phase Dependency Graph

```
[Phase ID] → [Dependencies] → [Blocks]

Example:
P1_DATABASE → [] → [P2_BACKEND, P3_INTEGRATION]
P2_BACKEND → [P1_DATABASE] → [P3_INTEGRATION, P4_FRONTEND]
P3_INTEGRATION → [P1_DATABASE, P2_BACKEND] → [P4_FRONTEND]
P4_FRONTEND → [P3_INTEGRATION] → []
```

### Dependency Validation

- [ ] No circular dependencies detected
- [ ] All prerequisites identified
- [ ] Blocking relationships clear
- [ ] Critical path calculated

**Critical Path**: [List of phases on critical path]
**Critical Path Duration**: [X hours]

---

## Wave Structure

### Wave 1: [Wave Name]

**Wave ID**: W1
**Wave Type**: [Sequential/Parallel]
**Estimated Duration**: [X hours]
**Parallel Efficiency**: [N/A for sequential, XX% for parallel]

#### Phases in Wave 1

1. **[Phase Name]** (Phase ID: P1)
   - **Dependencies**: [None/P0]
   - **Agent Type**: [generalist-builder/frontend-builder/backend-builder/database-builder/testing-specialist]
   - **Estimated Time**: [X hours]
   - **Deliverables**:
     - [Deliverable 1]
     - [Deliverable 2]
   - **Success Criteria**:
     - [ ] [Criterion 1]
     - [ ] [Criterion 2]

2. **[Phase Name]** (Phase ID: P2) _[if parallel]_
   - **Dependencies**: [None/P0]
   - **Agent Type**: [agent type]
   - **Estimated Time**: [X hours]
   - **Deliverables**: [List]
   - **Success Criteria**: [List]

#### Agent Allocation

**Total Agents**: [N] (based on complexity [score])
**Complexity Band**: [Simple: 1-2, Moderate: 2-3, Complex: 3-7, High: 8-15, Critical: 15-25]

| Agent # | Phase | Type | Task Summary | Context Needed |
|---------|-------|------|--------------|----------------|
| Agent 1 | P1 | [type] | [Summary] | [Serena keys] |
| Agent 2 | P2 | [type] | [Summary] | [Serena keys] |

#### Pre-Wave Checklist

Before spawning Wave 1:

- [ ] Load wave execution plan: `read_memory("wave_execution_plan")`
- [ ] Verify this is Wave 1 (correct sequence)
- [ ] Verify prerequisites: N/A (first wave)
- [ ] Load project context:
  - [ ] `read_memory("spec_analysis")`
  - [ ] `read_memory("phase_plan_detailed")`
  - [ ] `read_memory("architecture_complete")` if exists
- [ ] Verify MCP servers:
  - [ ] Serena MCP connected
  - [ ] [Other required MCPs]
- [ ] Estimate token usage: Current + (agents × 3000) < 150000?
- [ ] Prepare agent prompts with context loading protocol

#### Wave 1 Synthesis Checkpoint

**Checkpoint ID**: wave_1_checkpoint
**Serena Keys**:
- `wave_1_complete` - Synthesis document
- `wave_1_[agent-type]_results` - Individual agent results

**Validation Criteria**:
- [ ] All agents completed successfully
- [ ] Agent results saved to Serena
- [ ] No integration conflicts detected
- [ ] Quality metrics satisfied (no TODOs, functional tests)
- [ ] All deliverables present

**Synthesis Tasks**:
1. Collect all agent results from Serena
2. Aggregate deliverables (files, components, tests)
3. Cross-validate for conflicts and gaps
4. Create wave synthesis document
5. Present to user for validation
6. **WAIT FOR USER APPROVAL** before Wave 2

**User Validation Required**: ✅ YES

---

### Wave 2: [Wave Name]

**Wave ID**: W2
**Wave Type**: [Sequential/Parallel]
**Dependencies**: [W1]
**Estimated Duration**: [X hours]
**Parallel Efficiency**: [XX%]

#### Phases in Wave 2

[Repeat phase structure from Wave 1]

#### Agent Allocation

[Repeat allocation table]

#### Pre-Wave Checklist

Before spawning Wave 2:

- [ ] Load wave execution plan: `read_memory("wave_execution_plan")`
- [ ] Verify this is Wave 2 (correct sequence)
- [ ] Verify prerequisites:
  - [ ] `read_memory("wave_1_complete")` exists
  - [ ] Wave 1 deliverables present
  - [ ] Wave 1 approved by user
- [ ] Load previous wave contexts:
  - [ ] `read_memory("wave_1_complete")`
- [ ] Load project context: [same as Wave 1]
- [ ] Verify MCP servers: [same as Wave 1]
- [ ] Estimate token usage: [same formula]
- [ ] Prepare agent prompts with Wave 1 context

#### Wave 2 Synthesis Checkpoint

[Repeat synthesis structure]

---

### Wave N: [Wave Name]

[Repeat for additional waves]

---

## Agent Context Loading Protocol

**MANDATORY for EVERY agent in EVERY wave**:

```markdown
## MANDATORY CONTEXT LOADING PROTOCOL

Execute these commands BEFORE your task:

1. list_memories() - Discover all available Serena memories
2. read_memory("spec_analysis") - Understand project requirements
3. read_memory("phase_plan_detailed") - Know execution structure
4. read_memory("architecture_complete") if exists - System design
5. read_memory("wave_1_complete") if exists - Learn from Wave 1
6. read_memory("wave_2_complete") if exists - Learn from Wave 2
...
7. read_memory("wave_[N-1]_complete") - Immediate previous wave

Verify you understand:
✓ What we're building (from spec_analysis)
✓ How it's designed (from architecture_complete)
✓ What's been built (from previous waves)
✓ Your specific task (detailed below)

If ANY verification fails → STOP and request clarification

## YOUR SPECIFIC TASK

[Agent-specific task description]

## DELIVERABLES

You must deliver:
1. [Deliverable 1 with format]
2. [Deliverable 2 with format]

## SAVE RESULTS

After completing your task:

write_memory("wave_[N]_[agent-type]_results", {
  agent_type: "[type]",
  phase: "[phase name]",
  status: "complete",
  deliverables: {
    files_created: [list],
    components_built: [list],
    decisions_made: [list],
    tests_created: [count]
  },
  execution_time_minutes: [actual],
  issues_encountered: [list or "none"],
  next_wave_context: {
    what_next_wave_needs: "[info]"
  }
})
```

---

## Performance Metrics

### Speedup Calculation

**Sequential Time** (hypothetical):
```
Wave 1: [X hours]
Wave 2: [Y hours]
Wave 3: [Z hours]
Total Sequential: [X + Y + Z] hours
```

**Parallel Time** (actual):
```
Wave 1: max([agent times]) = [X hours]
Wave 2: max([agent times]) = [Y hours]
Wave 3: max([agent times]) = [Z hours]
Total Parallel: [max(X) + max(Y) + max(Z)] hours
```

**Speedup**: [Sequential / Parallel] = [N.Nx faster]

**Expected Speedup by Agent Count**:
- 2 agents: 1.5-1.8x
- 3 agents: 2.0-2.5x
- 5 agents: 3.0-4.0x
- 7+ agents: 3.5-5.0x

### Efficiency Targets

**Efficiency** = Speedup / Agent Count

- >80%: Excellent
- 60-80%: Good
- 40-60%: Acceptable
- <40%: Poor (reconsider wave structure)

---

## Error Recovery Protocol

### Agent Failure Decision Tree

```
Agent failure detected?
├─ Critical to wave? (blocks other work)
│  └─ YES: MUST fix before proceeding
│     1. Analyze failure
│     2. Respawn with fixes
│     3. Wait for completion
│     4. Re-synthesize
│
└─ NO: Can defer or skip
   └─ Document in synthesis
      Present options to user
      Proceed based on choice
```

### Failure Types

1. **Tool Failure**: Retry with corrected context or alternative tool
2. **Task Misunderstanding**: Respawn with clarified instructions
3. **Timeout/Crash**: Resume from last state or respawn
4. **Context Corruption**: Restore from checkpoint, respawn
5. **Integration Failure**: Spawn integration-fixer agent

---

## Success Criteria

Wave orchestration succeeds when:

✅ **Parallelism Verified**: Speedup ≥ 1.5x vs sequential
   - Evidence: Timestamps show concurrent execution
   - Metric: parallel_time = max(agent_times), not sum

✅ **Zero Duplicate Work**: No redundant agent tasks
   - Check: No files created by multiple agents
   - Check: No decisions made multiple times

✅ **Perfect Context Sharing**: Every agent has complete history
   - Check: All agents loaded required Serena memories
   - Check: No decisions based on incomplete info

✅ **Clean Validation Gates**: User approval between waves
   - Check: Synthesis presented after each wave
   - Check: Explicit user approval obtained

✅ **Complete Memory Trail**: All wave results saved
   - Check: wave_[N]_complete exists for all waves
   - Check: Individual agent results saved

✅ **Production Quality**: No TODOs, functional tests only
   - Check: No placeholders in code
   - Check: All tests functional (NO MOCKS)

---

## Execution Tracking

### Wave Execution Log

| Wave | Start Time | End Time | Duration | Agents | Status | Notes |
|------|-----------|----------|----------|--------|--------|-------|
| W1 | [HH:MM] | [HH:MM] | [X min] | [N] | [Complete/Failed] | [Notes] |
| W2 | [HH:MM] | [HH:MM] | [Y min] | [N] | [Complete/Failed] | [Notes] |

### Issue Log

| Issue ID | Wave | Description | Resolution | Impact |
|----------|------|-------------|------------|--------|
| I1 | W1 | [Description] | [Resolution] | [Impact] |

---

## References

- **WAVE_ORCHESTRATION.md**: Complete behavioral framework (1612 lines)
- **spec-analysis**: Project complexity and domain breakdown
- **phase-plan**: 5-phase implementation structure
- **TESTING_PHILOSOPHY.md**: NO MOCKS enforcement

---

**Version**: 1.0.0
**Template Created**: 2025-11-03
**Shannon Version**: 4.0.0+
