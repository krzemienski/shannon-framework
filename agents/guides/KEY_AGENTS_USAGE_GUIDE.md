# Shannon Key Agents: Usage Guide

**Agents Covered**: WAVE_COORDINATOR, TEST_GUARDIAN, CONTEXT_GUARDIAN
**Purpose**: Practical guide to Shannon's three critical orchestrator agents
**Audience**: Shannon users and developers

---

## Overview

Shannon's agent system includes 24 specialized agents. Three are CRITICAL orchestrators that most users will encounter:

1. **WAVE_COORDINATOR**: Manages parallel multi-agent execution
2. **TEST_GUARDIAN**: Enforces NO MOCKS functional testing
3. **CONTEXT_GUARDIAN**: Prevents context loss through checkpoints

---

## Agent 1: WAVE_COORDINATOR

### When It Activates

**Automatic** (Priority: CRITICAL):
- Complexity ≥ 0.7 (from /sh_spec)
- User runs /sh_wave command
- Phase plan identifies parallel opportunities
- Keywords: "wave", "parallel", "coordinate", "multi-agent"

**Manual**:
```
"Use wave-coordinator to orchestrate parallel execution"
```

### What It Does

**Core Function**: Coordinates 3-10 agents working in parallel across multiple waves

**Key Capabilities**:
1. Dependency analysis (which tasks can run in parallel)
2. True parallel spawning (all agents in ONE message)
3. Context preservation (every agent loads full history)
4. Wave synthesis (aggregates results, validates, requests approval)
5. Failure recovery (respawns failed agents)

### How to Use It

**Step 1**: Run /sh_spec to get complexity score
**Step 2**: If complexity ≥0.50, run /sh_wave
**Step 3**: WAVE_COORDINATOR activates automatically
**Step 4**: Coordinator spawns agents, waits for completion
**Step 5**: Review synthesis, approve to continue

**Example Flow**:
```
User: /sh_spec "Build e-commerce platform..."
Output: Complexity 0.75 → Wave execution recommended

User: /sh_wave
WAVE_COORDINATOR: "Spawning Wave 1: 3 agents in parallel..."

[Agents execute simultaneously]

WAVE_COORDINATOR: "Wave 1 complete. Review synthesis?"
User: "approved"

WAVE_COORDINATOR: "Spawning Wave 2: 5 agents in parallel..."
```

### Critical Patterns

**TRUE PARALLELISM** (Correct):
```xml
<function_calls>
  <invoke name="Task">Agent 1</invoke>
  <invoke name="Task">Agent 2</invoke>
  <invoke name="Task">Agent 3</invoke>
</function_calls>

All 3 execute SIMULTANEOUSLY
```

**SEQUENTIAL** (Wrong - No Speedup):
```
Message 1: <invoke>Agent 1</invoke>
Message 2: <invoke>Agent 2</invoke>
Message 3: <invoke>Agent 3</invoke>

Agents execute ONE AT A TIME
```

### Integration Points

- **With spec-analysis**: Uses complexity score to determine agent count
- **With phase-planning**: Uses phase plan tasks for wave grouping
- **With context-preservation**: Creates checkpoints between waves
- **With SITREP**: Collects status from all agents (complexity ≥0.70)

### Validation

**Successful coordination when**:
✅ Parallel waves measurably faster than sequential
✅ Zero duplicate work between agents  
✅ Every agent has complete context
✅ Clean validation gates between waves
✅ All wave results saved to Serena

---

## Agent 2: TEST_GUARDIAN

### When It Activates

**Automatic** (Priority: HIGH):
- Phase 4 (Testing) begins
- User mentions "test", "testing", "QA"
- Code contains mock patterns (jest.mock, @patch, sinon.stub)
- Pull request includes test files

**Manual**:
```
/sh_test --create
```

### What It Does

**Core Function**: Enforces NO MOCKS philosophy, ensures functional testing only

**Key Capabilities**:
1. Mock detection (scans for unittest.mock, jest.fn(), etc.)
2. Functional test generation (Puppeteer, XCUITest, real HTTP)
3. Test environment setup (Docker Compose, simulators)
4. Coverage validation (80/80/75 thresholds)
5. Phase 4 quality gate enforcement

### How to Use It

**Step 1**: Complete implementation (Phase 3)
**Step 2**: Enter Phase 4 (Testing)
**Step 3**: TEST_GUARDIAN activates automatically
**Step 4**: Guardian scans for mocks, generates functional tests
**Step 5**: Run tests, verify coverage, get phase approval

**Example Interaction**:
```
[Agent writes test with jest.mock()]

TEST_GUARDIAN: "⛔ MOCK DETECTED
File: tests/api.test.js:8
Violation: jest.mock('axios')

Functional Alternative:
Use real HTTP requests:
```javascript
const response = await fetch('http://localhost:3000/api/users');
const data = await response.json();
expect(data.length).toBeGreaterThan(0);
```

Remove mocks and use real components."

[Agent updates test to use real HTTP]

TEST_GUARDIAN: "✅ NO MOCKS compliance verified. Test uses real HTTP requests."
```

### Critical Patterns

**NO MOCKS** (Shannon Mandate):
```javascript
// ❌ WRONG: Mock-based
jest.mock('../api');
test('fetch users', () => {
  api.getUsers.mockResolvedValue([{id: 1}]);
  // Tests mock, not real API
});

// ✅ CORRECT: Functional
test('fetch users', async ({page}) => {
  await page.goto('http://localhost:3000');
  // Tests real browser, real API, real database
  const users = await page.$$('.user-card');
  expect(users.length).toBeGreaterThan(0);
});
```

### Integration Points

- **With functional-testing skill**: Follows NO MOCKS philosophy
- **With post_tool_use hook**: Hook blocks, Guardian provides fix
- **With wave-orchestration**: Testing wave follows implementation waves
- **With Puppeteer MCP**: Primary tool for browser automation

### Validation

**Guardian succeeds when**:
✅ Zero mock usage in entire codebase
✅ All tests use real components
✅ Coverage ≥80% lines, ≥80% functions, ≥75% branches
✅ Phase 4 quality gates pass
✅ Tests run against real browsers/databases/APIs

---

## Agent 3: CONTEXT_GUARDIAN

### When It Activates

**Automatic** (Priority: CRITICAL):
- PreCompact hook fires (auto-compact imminent)
- Token usage >75% (context limit approaching)
- Wave completion (create wave checkpoint)
- Phase transition (create phase checkpoint)

**Manual**:
```
/sh_checkpoint "milestone-name"
```

### What It Does

**Core Function**: Creates/restores checkpoints to prevent context loss

**Key Capabilities**:
1. Comprehensive checkpoint creation (captures all Serena memories)
2. Validation (verifies checkpoint integrity)
3. Context restoration (loads checkpoint, rebuilds state)
4. Memory inventory (tracks all session memories)
5. Continuation instructions (tells you what to do next)

### How to Use It

**Checkpoint Creation**:
```
User: /sh_checkpoint "wave-2-complete"
CONTEXT_GUARDIAN: Activates, creates checkpoint
Output: "✅ CHECKPOINT SAVED: shannon_checkpoint_20251109_HHMMSS"
```

**Context Restoration**:
```
[After auto-compact]
User: /sh_restore
CONTEXT_GUARDIAN: Activates, loads latest checkpoint
Output: "✅ CONTEXT RESTORED: 12 memories loaded, Wave 2 of 4, ready to continue"
```

**Automatic (PreCompact)**:
```
[Context reaches 95% limit]
PreCompact Hook: Triggers CONTEXT_GUARDIAN
CONTEXT_GUARDIAN: "🔴 PRECOMPACT CHECKPOINT EXECUTING..."
[Creates comprehensive checkpoint]
Output: "✅ Context secured, auto-compact can proceed safely"
```

### Critical Patterns

**Checkpoint Structure** (11 sections preserved):
1. Metadata (timestamp, type, trigger)
2. Project state (phase, wave, progress)
3. Memory keys (ALL Serena memories)
4. Active work (current focus, in-progress files)
5. Wave context (completed/pending waves)
6. Decisions (architectural choices logged)
7. Integration status (components built, connections)
8. Quality state (validation gates, test results)
9. Next steps (continuation instructions)
10. MCP status (which MCPs active)
11. TodoWrite state (task list)

**Restoration Validation**:
- Checkpoint integrity check
- Memory coverage (90%+ restored)
- Critical memories present (spec, plan)
- Continuation instructions available

### Integration Points

- **With PreCompact hook**: Triggered automatically before context loss
- **With wave-orchestration**: Checkpoints at wave boundaries
- **With context-preservation skill**: Uses skill protocol
- **With Serena MCP**: Stores all checkpoints in knowledge graph

### Validation

**Guardian succeeds when**:
✅ Zero context loss across auto-compact events
✅ All checkpoints validate correctly
✅ Restorations recover 90%+ memories
✅ Users resume work immediately
✅ Wave results persist across sessions
✅ No forgotten decisions or progress

---

## Using Multiple Agents Together

### Typical Shannon Workflow

```
Phase 1-2: Analysis & Planning
→ spec-analyzer, phase-planner agents

Phase 3: Implementation (if complexity ≥0.50)
→ WAVE_COORDINATOR spawns:
  - frontend-implementer
  - backend-architect
  - database-engineer
  - [3-7 more agents in parallel]

Phase 4: Testing
→ TEST_GUARDIAN enforces:
  - NO MOCKS compliance
  - Functional test coverage
  - Quality gates

Throughout: CONTEXT_GUARDIAN
→ Automatic checkpoints:
  - After each wave
  - Before auto-compact
  - At phase transitions
```

### Agent Coordination Example

```
User: /sh_spec "Build marketplace..."
Complexity: 0.78 (HIGH)

User: /sh_wave
→ WAVE_COORDINATOR: "Spawning Wave 1: 4 agents..."
  [Agents execute in parallel]
→ CONTEXT_GUARDIAN: Creates wave_1_complete checkpoint
→ WAVE_COORDINATOR: "Wave 1 synthesis ready"

User: "approved"
→ WAVE_COORDINATOR: "Spawning Wave 2: 5 agents..."
  [Agents execute in parallel]
→ CONTEXT_GUARDIAN: Creates wave_2_complete checkpoint
→ WAVE_COORDINATOR: "Wave 2 synthesis ready"

[Phase 4 begins]
→ TEST_GUARDIAN: "Scanning for mock usage..."
→ TEST_GUARDIAN: "0 violations found ✅"
→ TEST_GUARDIAN: "Generating functional tests..."
→ TEST_GUARDIAN: "Coverage 85% ✅ Phase 4 APPROVED"

→ CONTEXT_GUARDIAN: Creates phase_4_complete checkpoint

Result: Coordinated multi-agent execution with quality enforcement and zero context loss
```

---

## Troubleshooting

### WAVE_COORDINATOR Issues

**Problem**: Waves executing sequentially (no speedup)
- **Cause**: Tasks have strict dependencies
- **Resolution**: This is correct - some projects are inherently sequential

**Problem**: Agents missing context
- **Cause**: Context loading protocol not in agent prompts
- **Resolution**: WAVE_COORDINATOR includes protocol in all spawned agents

### TEST_GUARDIAN Issues

**Problem**: Guardian not detecting mocks
- **Cause**: post_tool_use hook not installed
- **Resolution**: Verify hooks/post_tool_use.py exists and executable

**Problem**: Guardian blocks legitimate test code
- **Cause**: Word "mock" in comment triggers detection
- **Resolution**: Rename variable or rephrase comment

### CONTEXT_GUARDIAN Issues

**Problem**: Checkpoint not found
- **Cause**: Serena MCP not configured
- **Resolution**: Install Serena MCP (mandatory for Shannon)

**Problem**: Partial restoration (missing memories)
- **Cause**: Some memories deleted or corrupted
- **Resolution**: Guardian provides graceful degradation, lists missing items

---

## FAQ

**Q: How do I manually invoke these agents?**
A: Use Task tool:
```
Task(subagent_type="wave-coordinator", prompt="...")
```
But typically they auto-activate based on triggers.

**Q: Can I skip TEST_GUARDIAN for quick prototypes?**
A: No. Shannon mandate is NO MOCKS for ALL projects. Guardian enforces this.

**Q: What if CONTEXT_GUARDIAN checkpoint fails?**
A: Critical issue - Serena MCP must be operational. Shannon cannot function without it.

**Q: How many waves does WAVE_COORDINATOR typically create?**
A: Depends on complexity:
- 0.50-0.60: 2-3 waves
- 0.60-0.70: 3-5 waves
- 0.70-0.85: 5-7 waves
- 0.85-1.00: 7-10 waves

**Q: Does TEST_GUARDIAN work with all testing frameworks?**
A: Yes, but enforces NO MOCKS regardless of framework (Jest, Pytest, XCTest, etc.)

**Q: How often does CONTEXT_GUARDIAN checkpoint?**
A: Automatically at:
- Wave boundaries
- Phase transitions
- Every 30 minutes
- Before auto-compact (PreCompact hook)
- Manual user request

---

## Summary

These 3 agents form Shannon's **orchestration backbone**:

- **WAVE_COORDINATOR**: Makes parallel execution work (3.5x speedup)
- **TEST_GUARDIAN**: Ensures tests validate reality (NO MOCKS enforcement)
- **CONTEXT_GUARDIAN**: Prevents information loss (checkpointing)

**Together they enable**:
- Efficient multi-agent coordination
- Production-ready testing
- Seamless cross-session work

**All are automatic** - you don't manage them, they manage the system for you.

---

**Version**: 1.0
**Shannon**: 4.1.0
**Last Updated**: 2025-11-09
