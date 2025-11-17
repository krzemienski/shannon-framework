# Wave 1 Debugging & Continuation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans OR superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal**: Fix 48 failing tests, complete validation streaming, relocate Agents 3,6, achieve 100% test pass rate

**Architecture**: Systematic debugging with parallel sub-agents, root cause tracing, Serena MCP coordination

**Tech Stack**: Python, React/TypeScript, pytest, Playwright, git cherry-pick, Serena MCP

**Current Status**: 364/412 tests passing (88%), Wave 1 delivered 4 major features

---

## Phase 1: Systematic Analysis (30 minutes)

### Task 1.1: Write Current State to Serena

**Serena Memories to Create**:

```bash
# Already written:
# - WAVE1_EXECUTION_COMPLETE_20251116
# - WAVE1_TEST_FAILURES_CATEGORIZED

# Still need:
mcp__serena__write_memory("WAVE1_WORKING_DIRECTORY", "/Users/nick/Desktop/shannon-cli")
mcp__serena__write_memory("WAVE1_AGENT_DELIVERABLES", {
  "agent1": "multi-file generation (34 tests, merged)",
  "agent2": "agent pool (9 tests, merged)",
  "agent4": "research (38 tests, merged)",
  "agent5": "ultrathink (32 tests, merged)",
  "agent3": "decisions (20 tests, WRONG REPO)",
  "agent6": "controls (40 tests, WRONG REPO)"
})
```

**Verification**:
```bash
mcp__serena__list_memories()
# Should show WAVE1_* memories
```

---

### Task 1.2: Analyze Test Failures with Root Cause Tracing

**Skill**: Use `root-cause-tracing` skill

**File**: tests/integration/test_orchestration.py (4 failures)

**Step 1**: Run failing test with verbose output
```bash
pytest tests/integration/test_orchestration.py::test_execution_planner -vv --tb=long
```

**Step 2**: Identify AttributeError location

**Step 3**: Trace back to root cause:
- What attribute is missing?
- Why was it removed/changed?
- What V4 change caused this?

**Step 4**: Document in Serena
```python
mcp__serena__write_memory("TEST_FAILURE_ROOT_CAUSE_ORCHESTRATION", {
  "test": "test_execution_planner",
  "error": "AttributeError: ...",
  "root_cause": "[Identified cause]",
  "fix_approach": "[How to fix]"
})
```

**Repeat for all 4 integration tests**

---

## Phase 2: Critical Fixes (2-3 hours)

### Task 2.1: Fix Integration Tests

**Skill**: Use `systematic-debugging` + `test-driven-development`

**Files**:
- Fix: `src/shannon/orchestration/orchestrator.py`
- Fix: `src/shannon/orchestration/planner.py`
- Test: `tests/integration/test_orchestration.py`

**Step 1: Fix test_execution_planner**

Read current test:
```bash
cat tests/integration/test_orchestration.py | grep -A 20 "def test_execution_planner"
```

Identify what changed in V4 ExecutionPlanner API

Update test for V4 interface:
```python
# Before (V3):
planner = ExecutionPlanner()
plan = planner.create_plan(task)

# After (V4):
planner = ExecutionPlanner(orchestrator)  # Now needs orchestrator?
plan = await planner.create_plan(task)  # Now async?
```

**Step 2: Run test**
```bash
pytest tests/integration/test_orchestration.py::test_execution_planner -v
```

Expected: PASS

**Step 3: Repeat for remaining 3 integration tests**

**Step 4: Commit**
```bash
git add tests/integration/test_orchestration.py
git commit -m "fix: Update integration tests for V4 orchestrator API

Fixed 4 integration tests:
- test_execution_planner (ExecutionPlanner API)
- test_orchestrator_execution (async execution)
- test_orchestrator_halt_resume (new halt API)
- test_end_to_end_workflow (updated workflow)

Tests now: 368/412 passing (89%)"
```

**Validation**: pytest tests/integration/ shows all PASS

---

### Task 2.2: Fix Agent Pool Tests

**Files**:
- Test: `tests/cli_functional/test_wave4_agents.py`

**Step 1**: Update test_agent_states_visible for V4 AgentPool

```python
# Test expects V3 agent interface
# Update for V4 AgentPool.spawn_agent() API

def test_agent_states_visible():
    """Agent states visible in dashboard"""
    pool = AgentPool(max_active=8)
    agent = await pool.spawn_agent('test_skill', {}, 'session-123')

    # V4: Agent has status, role, id
    assert agent.status == 'running'
    assert agent.role is not None
    assert agent.id is not None
```

**Step 2**: Run test
```bash
pytest tests/cli_functional/test_wave4_agents.py::test_agent_states_visible -v
```

**Step 3**: Repeat for remaining 4 agent tests

**Step 4**: Commit
```bash
git commit -m "fix: Update agent tests for V4 AgentPool API (5 tests fixed)"
```

**Validation**: pytest tests/cli_functional/test_wave4_agents.py shows all PASS

---

### Task 2.3: Fix Validation Streaming Event Flow

**Skill**: Use `root-cause-tracing` to trace event flow

**Files**:
- Check: `src/shannon/orchestration/orchestrator.py`
- Check: `src/shannon/cli/v4_commands/do.py`
- Fix: Where ValidationOrchestrator is instantiated

**Step 1**: Trace validator instantiation in orchestrator

```bash
grep -rn "ValidationOrchestrator(" src/shannon/
```

**Step 2**: Find where orchestrator creates validator

Check `src/shannon/orchestration/orchestrator.py`:
```python
# Does orchestrator.py create its own validator?
# If so, does it pass self.dashboard_client?
```

**Step 3**: Fix if not passing dashboard_client

```python
# In Orchestrator.__init__ or execute method:
self.validator = ValidationOrchestrator(
    project_root=self.project_root,
    logger=self.logger,
    dashboard_client=self.dashboard_client  # ADD THIS
)
```

**Step 4**: Test with real execution

```bash
cd /tmp/validation-test
shannon do "run pytest" --dashboard
```

Use Playwright to verify output appears in dashboard

**Step 5**: Commit
```bash
git commit -m "fix: Validation streaming - wire dashboard_client through orchestrator

Events now flow: validator → dashboard_client → server → dashboard UI
Validation panel displays real-time test output

Verified with Playwright"
```

**Validation**: Playwright sees validation:output events in dashboard

---

## Phase 3: Agent Relocation (1-2 hours)

### Task 3.1: Cherry-Pick Agent 3 (Decision Engine)

**Files**:
- Source: /Users/nick/Desktop/shannon-framework (branch: agent3-decisions)
- Target: /Users/nick/Desktop/shannon-cli (branch: master)

**Step 1**: List Agent 3 commits in framework repo

```bash
cd /Users/nick/Desktop/shannon-framework
git checkout agent3-decisions
git log --oneline master..agent3-decisions
```

**Step 2**: Identify commit hashes to cherry-pick

**Step 3**: Cherry-pick to shannon-cli

```bash
cd /Users/nick/Desktop/shannon-cli
git cherry-pick <commit1> <commit2> <commit3>
```

**Step 4**: Resolve path conflicts if any
- shannon-framework paths → shannon-cli paths
- Adjust imports if needed

**Step 5**: Run Agent 3 tests

```bash
pytest tests/orchestration/test_decision_engine.py -v
```

Expected: 20/20 PASS (tests should work after cherry-pick)

**Step 6**: Commit
```bash
git commit -m "feat: Add Decision Engine from Agent 3 (cherry-picked from framework)

Relocated from shannon-framework/agent3-decisions
Tests: 20/20 passing
Feature: Human-in-the-loop decisions with auto-approval"
```

**Validation**: Decision engine tests passing in shannon-cli

---

### Task 3.2: Cherry-Pick Agent 6 (Basic Controls)

**Same process as Task 3.1 but for agent6-controls branch**

Expected result: 40/40 tests passing for controls

---

## Phase 4: V3 Test Cleanup (Deferred - Can be parallel with Phase 3)

### Task 4.1: Analyze V3 Feature Tests

**Skill**: Use `verification-before-completion` to decide keep vs remove

**For each V3 test file**:
1. Read test file
2. Check if feature still exists in V4
3. If exists: Update test for V4 API
4. If not exists: Remove test or mark @pytest.mark.skip

**Can dispatch sub-agents for each category**:
- Agent: V3 Cache Tests (7 tests)
- Agent: V3 Optimization Tests (4 tests)
- Agent: V3 Analytics Tests (6 tests)
- Agent: V3 Context Tests (6 tests)

---

## Phase 5: Final Validation (1 hour)

### Task 5.1: Run Complete Test Suite

**Step 1**: Run all tests

```bash
pytest tests/ -v --tb=short
```

**Step 2**: Verify targets met:
- Integration tests: 4/4 PASS (was 0/4)
- Agent tests: 5/5 PASS (was 0/5)
- WebSocket tests: 2/2 PASS (was 0/2)
- Total: 380+/412 PASS (92%+)

**Step 3**: Remaining failures acceptable?
- If V3 feature tests: OK to defer
- If core functionality: Continue debugging

**Step 4**: Write final status to Serena

```python
mcp__serena__write_memory("WAVE1_DEBUGGING_COMPLETE", {
  "tests_passing": "X/412",
  "critical_issues_resolved": True,
  "validation_streaming": "working",
  "agents_3_6_relocated": True
})
```

---

## Sub-Agent Exact Prompts

### Agent A: Integration Test Fixes

```
MISSION: Fix 4 failing integration tests in tests/integration/test_orchestration.py

WORKING DIRECTORY: /Users/nick/Desktop/shannon-cli

SKILLS TO USE:
- systematic-debugging (root cause analysis)
- test-driven-development (fix tests properly)

SERENA COORDINATION:
READ: WAVE1_EXECUTION_COMPLETE_20251116 (understand Wave 1 changes)
WRITE: AGENT_A_INTEGRATION_FIXES (document fixes)

TASKS:
1. Run: pytest tests/integration/test_orchestration.py -vv
2. For each failure:
   a. Identify AttributeError or API mismatch
   b. Check src/shannon/orchestration/ for V4 API
   c. Update test to use V4 API
   d. Verify test passes
3. Commit when all 4 tests pass

VALIDATION: pytest tests/integration/test_orchestration.py shows 4/4 PASS

WORK UNTIL: All 4 tests passing
```

### Agent B: Agent Pool Test Fixes

```
MISSION: Fix 5 failing agent tests in tests/cli_functional/test_wave4_agents.py

WORKING DIRECTORY: /Users/nick/Desktop/shannon-cli

SKILLS TO USE:
- test-driven-development
- verification-before-completion

SERENA COORDINATION:
READ: WAVE1_EXECUTION_COMPLETE_20251116
WRITE: AGENT_B_AGENT_TESTS_FIXED

TASKS:
1. Read Agent 2 implementation: src/shannon/orchestrator.py (agent_pool)
2. Understand V4 AgentPool API (spawn_agent, capacity limits)
3. Update each test for V4 interface
4. Run: pytest tests/cli_functional/test_wave4_agents.py -v
5. Commit when all 5 pass

VALIDATION: 5/5 tests PASS

WORK UNTIL: All tests passing
```

### Agent C: WebSocket Test Fixes

```
MISSION: Fix 2 failing websocket tests in tests/server/test_websocket.py

WORKING DIRECTORY: /Users/nick/Desktop/shannon-cli

SKILLS TO USE:
- systematic-debugging
- test-driven-development

SERENA COORDINATION:
READ: WAVE1_EXECUTION_COMPLETE_20251116
WRITE: AGENT_C_WEBSOCKET_FIXED

TASKS:
1. Examine V4 event structure in src/shannon/server/websocket.py
2. Update tests for V4 event format (nested data structure)
3. Run: pytest tests/server/test_websocket.py -v
4. Commit when both pass

VALIDATION: 2/2 tests PASS

WORK UNTIL: Both tests passing
```

### Agent D: Validation Streaming E2E Fix

```
MISSION: Complete validation streaming integration (events to dashboard UI)

WORKING DIRECTORY: /Users/nick/Desktop/shannon-cli

SKILLS TO USE:
- root-cause-tracing (trace event flow)
- systematic-debugging (find broken link)
- playwright-skill (validate UI receives events)

SERENA COORDINATION:
READ: WAVE1_EXECUTION_COMPLETE_20251116
WRITE: AGENT_D_VALIDATION_STREAMING_COMPLETE

TASKS:
1. Trace event flow:
   - validator.py emits validation:output ✓
   - dashboard_client sends to server (verify)
   - server relays to dashboard (verify)
   - dashboard receives (verify)
   - store updates validationOutput (verify)
   - Validation.tsx renders (verify)

2. Find broken link in chain

3. Fix (likely: orchestrator not passing dashboard_client to validator)

4. Test with Playwright:
   - shannon do "run pytest" --dashboard
   - Playwright: Verify output appears in Validation panel
   - Screenshot: validation-streaming-working.png

5. Commit when E2E working

VALIDATION: Playwright sees green/red lines in Validation panel

WORK UNTIL: Validation streaming fully functional
```

### Agent E: Relocate Agent 3 (Decisions)

```
MISSION: Cherry-pick Agent 3 (Decision Engine) from shannon-framework to shannon-cli

WORKING DIRECTORY: /Users/nick/Desktop/shannon-cli

TASKS:
1. cd /Users/nick/Desktop/shannon-framework
2. git checkout agent3-decisions
3. git log --oneline master..agent3-decisions > /tmp/agent3-commits.txt
4. cd /Users/nick/Desktop/shannon-cli
5. For each commit in agent3-commits.txt:
   git cherry-pick <hash>
6. Resolve any path conflicts
7. Run: pytest tests/orchestration/test_decision_engine.py -v
8. Commit: "feat: Add Decision Engine (Agent 3 relocated)"

VALIDATION: 20/20 Decision Engine tests passing in shannon-cli

WORK UNTIL: All tests passing after relocation
```

### Agent F: Relocate Agent 6 (Controls)

```
MISSION: Cherry-pick Agent 6 (Basic Controls) from shannon-framework to shannon-cli

WORKING DIRECTORY: /Users/nick/Desktop/shannon-cli

Same process as Agent E but for agent6-controls branch

VALIDATION: 40/40 Controls tests passing in shannon-cli

WORK UNTIL: All tests passing
```

---

## Parallel Execution Strategy

**Phase 2: Critical Fixes (Parallel)**
```
Dispatch simultaneously:
- Agent A: Integration tests (1-2h)
- Agent B: Agent tests (1-2h)
- Agent C: WebSocket tests (30min)
- Agent D: Validation streaming (1-2h)

Wall time: max(2h) = 2h
Sequential: 5-6h
Savings: 3-4h
```

**Phase 3: Relocations (Parallel)**
```
Dispatch simultaneously:
- Agent E: Cherry-pick Agent 3 (30min)
- Agent F: Cherry-pick Agent 6 (30min)

Wall time: 30min
```

**Total**: 2.5h with parallelization (vs 6h sequential)

---

## Execution Coordination via Serena

**Before Dispatching Agents**:
```python
# I write:
mcp__serena__write_memory("PHASE2_AGENT_ASSIGNMENTS", {
  "agent_a": "Integration tests (4 failures)",
  "agent_b": "Agent pool tests (5 failures)",
  "agent_c": "WebSocket tests (2 failures)",
  "agent_d": "Validation streaming E2E",
  "agent_e": "Relocate Agent 3",
  "agent_f": "Relocate Agent 6"
})

mcp__serena__write_memory("PHASE2_COORDINATION_PROTOCOL", {
  "agents_read": ["WAVE1_EXECUTION_COMPLETE", "WAVE1_TEST_FAILURES"],
  "agents_write": ["AGENT_X_COMPLETE", "AGENT_X_FINDINGS"],
  "conflict_files": ["orchestrator.py (agents A,B might both touch)"],
  "merge_order": "D→E→F→A→B→C (validation first, then features, then test fixes)"
})
```

**During Execution**:
```python
# Every 15 minutes, I check:
mcp__serena__read_memory("AGENT_A_SITREP")
mcp__serena__read_memory("AGENT_B_SITREP")
# etc.

# Monitor progress, detect blockers
```

**After All Complete**:
```python
# I merge results and validate:
mcp__serena__read_memory("AGENT_A_COMPLETE")
# etc.

# Run consolidated validation
pytest tests/ -v

# Write final status
mcp__serena__write_memory("PHASE2_DEBUGGING_COMPLETE", results)
```

---

## Success Criteria

**Phase 2 Complete When**:
- [ ] Integration tests: 4/4 PASS (was 0/4)
- [ ] Agent tests: 5/5 PASS (was 0/5)
- [ ] WebSocket tests: 2/2 PASS (was 0/2)
- [ ] Validation streaming: E2E working with Playwright proof
- [ ] Tests passing: 375+/412 (91%+)

**Phase 3 Complete When**:
- [ ] Agent 3 relocated: 20/20 tests in shannon-cli
- [ ] Agent 6 relocated: 40/40 tests in shannon-cli
- [ ] Decisions panel working in shannon-cli dashboard
- [ ] Controls working in shannon-cli dashboard
- [ ] Tests passing: 395+/412 (96%+)

**Overall Success**:
- [ ] 95%+ tests passing (390+/412)
- [ ] All critical features functional
- [ ] All user priorities delivered
- [ ] Validation streaming E2E working
- [ ] Ready for Wave 2 or release

---

## Execution Options

**Option 1: Subagent-Driven (This Session)**
- Stay in current session
- Dispatch agents one at a time or in parallel
- Review between agents
- Fast iteration
- **REQUIRED SUB-SKILL**: Use `superpowers:subagent-driven-development`

**Option 2: Parallel Session (New Session)**
- Open new session
- Load this plan
- Execute all tasks in batches
- Checkpoints between phases
- **REQUIRED SUB-SKILL**: New session uses `superpowers:executing-plans`

**Recommendation**: Option 1 (subagent-driven) - Faster for debugging work, already in context

---

## Notes for Engineer

- **Working directory**: /Users/nick/Desktop/shannon-cli (VERIFY BEFORE ALL WORK)
- **Test philosophy**: NO MOCKS (functional tests only)
- **Validation**: Playwright for all UI features
- **Commits**: Frequent (after each fix)
- **Serena**: Read context, write progress
- **WORK UNTIL PASS**: Don't proceed with failing validations

---

**Plan saved**: docs/plans/2025-11-16-wave1-debugging-continuation.md
**Ready for execution**
