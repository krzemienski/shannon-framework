# Shannon CLI V5: Consolidation & Integration Plan

**Date**: 2025-11-17
**Vision**: Unified platform combining V3 intelligence + V4 execution
**Timeline**: 46 hours (fits 2M token extended session)
**Philosophy**: Functional testing ONLY - NO pytest, real executions, browser validation

---

## Executive Summary

Shannon V5 consolidates V3 (context-aware analysis platform) and V4 (skills-based execution system) into a unified, production-ready platform. This plan focuses on **integration over innovation** - all code exists (41,865 lines), we're wiring it together and cleaning up architectural confusion.

**Key Changes**:
- V3 + V4 → V5 (unified orchestrator)
- 40 commands → 25 commands (consolidated)
- Dual orchestrators → UnifiedOrchestrator
- Cleanup: Delete pytest (412 tests), archive 50+ status files
- Testing: 100% functional (shell scripts + Playwright browser tests)

**Success Criteria**:
- ✅ `shannon do` fully functional with real-time dashboard
- ✅ All V3 features (cache, analytics, context) integrated
- ✅ All functional tests passing (NO pytest)
- ✅ Dashboard shows real-time updates (all 6 panels)
- ✅ Production ready, documented, tagged v5.0.0

---

## Skills Required (Invoke These Proactively)

### MANDATORY First
- **session-context-priming**: FIRST action in next session (200+ thoughts, read all files)

### Phase-Specific Skills
- **systematic-debugging**: Event emission debugging (Phase 3), test failures (Phase 6)
- **playwright-skill**: ALL dashboard testing (Phase 3, 6)
- **test-driven-development**: All new integrations (Phases 1, 2, 4)
- **code-reviewer**: After each phase completion
- **refactoring-expert**: UnifiedOrchestrator creation (Phase 1)
- **architecture-reviewer**: After Phase 1 (verify consolidation sound)
- **honest-reflections**: Before tagging v5.0.0 (Phase 7)

---

## Phase 0: Pre-Execution Context Loading (MANDATORY)

**Duration**: Part of session startup (handled by session-context-priming skill)

**CRITICAL**: Next session MUST start with:
```
Skill("session-context-priming")
```

This enforces:
- ✅ Read COMPREHENSIVE_ARCHITECTURE_ANALYSIS.md (924 lines) completely
- ✅ Read orchestrator.py (481 lines) completely
- ✅ Read orchestration/orchestrator.py (459 lines) completely
- ✅ Read commands.py structure (know all 40 commands)
- ✅ Pull Context7: FastAPI events, Socket.IO async server, Click commands
- ✅ Read latest 5 memories from this session
- ✅ Check git state (verify at commit 7bc5bf8 or later)
- ✅ 200+ ultrathink thoughts on V5 strategy

**No work begins until context COMPLETELY loaded.**

---

## Phase 1: Code Cleanup & Organization (2-3 hours)

**Goal**: Clean workspace before building V5

### Task 1.1: Delete Pytest Files (30 min)

**Rationale**: Pytest violates Shannon testing mandate (functional only)

**Actions**:
```bash
# Delete all pytest test files
rm -rf tests/cli/
rm -rf tests/server/
rm -rf tests/skills/
rm -rf tests/orchestration/
rm -rf tests/e2e/
rm -rf tests/integration/
rm -f tests/*.py
rm -f tests/functional/test_*.py  # Only delete .py, keep .sh

# Keep only functional directory
ls tests/functional/*.sh  # Verify these remain
```

**Validation Gate 1.1**:
- ✅ No .py files in tests/ (except __init__.py if needed)
- ✅ tests/functional/*.sh files still exist (5 shell scripts)
- ✅ Git status shows deletions
- ✅ Commit: "cleanup: Remove all pytest files per Shannon mandate"

### Task 1.2: Archive Status Files (30 min)

**Actions**:
```bash
# Create archive
mkdir -p docs/archive/session-status

# Move all status files
mv FINAL_*.md docs/archive/session-status/
mv BRUTAL_*.md docs/archive/session-status/
mv HONEST_*.md docs/archive/session-status/
mv AGENT*_COMPLETE.md docs/archive/session-status/
mv AGENT*_MISSION*.md docs/archive/session-status/
mv AGENT*_SITREP*.md docs/archive/session-status/
mv SESSION_*.md docs/archive/session-status/
mv WAVE*_COMPLETE.md docs/archive/session-status/
mv *_VALIDATION.md docs/archive/session-status/
mv HANDOFF_*.md docs/archive/session-status/
mv TASK_*.md docs/archive/session-status/

# Keep only essential docs
ls *.md | grep -E "README|CHANGELOG|COMPREHENSIVE_ARCHITECTURE"
```

**Validation Gate 1.2**:
- ✅ Root directory has < 10 .md files
- ✅ docs/archive/session-status/ has ~50 files
- ✅ Essential docs remain (README, CHANGELOG, COMPREHENSIVE_ARCHITECTURE_ANALYSIS)
- ✅ Commit: "cleanup: Archive session status files to docs/archive/"

### Task 1.3: Consolidate Plans (30 min)

**Actions**:
```bash
# Archive old plans
mkdir -p docs/archive/old-plans
mv docs/plans/2025-11-13-*.md docs/archive/old-plans/
mv docs/plans/2025-11-16-*.md docs/archive/old-plans/
mv docs/plans/SHANNON_V4_*.md docs/archive/old-plans/
mv docs/plans/NEXT_SESSION_V3_COMPLETION.md docs/archive/old-plans/

# Keep only V5 plan
ls docs/plans/  # Should show SHANNON_V5_CONSOLIDATION_PLAN.md only
```

**Validation Gate 1.3**:
- ✅ docs/plans/ has 1-2 files (V5 plan + maybe 1 reference)
- ✅ docs/archive/old-plans/ has 10+ archived plans
- ✅ Commit: "cleanup: Archive old version plans"

### Task 1.4: Clean Serena Memories (30 min)

**Actions**:
```bash
# Archive old session memories
mkdir -p .serena/archive
mv .serena/memories/WAVE1_*.md .serena/archive/ 2>/dev/null || true
mv .serena/memories/AGENT_*.md .serena/archive/ 2>/dev/null || true
mv .serena/memories/V3_INTEGRATION_*.md .serena/archive/ 2>/dev/null || true

# Keep only recent critical memories
ls .serena/memories/  # Should be minimal
```

**Validation Gate 1.4**:
- ✅ .serena/memories/ has < 10 files
- ✅ .serena/archive/ has archived memories
- ✅ Commit: "cleanup: Archive old Serena memories"

**PHASE 1 COMPLETE WHEN**:
- ✅ All pytest files deleted
- ✅ All status files archived
- ✅ All old plans archived
- ✅ Serena memories cleaned
- ✅ 4 commits created
- ✅ Workspace clean and organized

---

## Phase 2: UnifiedOrchestrator Implementation (8-10 hours)

**Goal**: Create single orchestrator consolidating V3 + V4 capabilities

### Task 2.1: Design UnifiedOrchestrator (1 hour)

**Skill**: Use `refactoring-expert` for consolidation design

**Actions**:
1. Read ContextAwareOrchestrator completely (orchestrator.py)
2. Read orchestration.Orchestrator completely (orchestration/orchestrator.py)
3. Identify common patterns and differences
4. Design unified interface
5. Create UNIFIED_ORCHESTRATOR_DESIGN.md

**Design Spec**:
```python
class UnifiedOrchestrator:
    """V5 orchestrator consolidating V3 + V4 capabilities."""

    def __init__(self, config):
        # V3 subsystems
        self.context = ContextManager()
        self.cache = CacheManager()
        self.analytics = AnalyticsDatabase()
        self.cost_optimizer = CostOptimizer()

        # V4 subsystems
        self.skills = SkillRegistry()
        self.planner = ExecutionPlanner()
        self.agent_pool = AgentPool()

        # Shared
        self.dashboard_client = DashboardEventClient()

    async def execute_analysis(self, spec_text, **opts):
        """V3 analysis with all features."""
        # Use ContextAwareOrchestrator logic

    async def execute_skills(self, task, **opts):
        """V4 skills-based execution."""
        # Use orchestration.Orchestrator logic

    async def execute_unified(self, request, **opts):
        """Intelligent routing: analysis OR skills based on request."""
        # Auto-detect: spec file → analysis, task → skills
```

**Validation Gate 2.1**:
- ✅ Design document created (UNIFIED_ORCHESTRATOR_DESIGN.md)
- ✅ Interface clearly defined
- ✅ Migration path from both orchestrators specified
- ✅ Reviewed with architecture-reviewer skill
- ✅ Commit: "design: UnifiedOrchestrator consolidation architecture"

### Task 2.2: Implement UnifiedOrchestrator Core (4 hours)

**Skill**: Use `test-driven-development` - write functional test first

**Test First** (tests/functional/test_unified_orchestrator.sh):
```bash
#!/bin/bash
# Test UnifiedOrchestrator handles both analysis and execution

# Test 1: Analysis path
shannon do "analyze this spec" spec.md
# Verify: Uses V3 cache, analytics, context

# Test 2: Execution path
shannon do "create hello.py with print statement"
# Verify: Uses V4 skills, creates file

# Test 3: Unified features
shannon do "analyze and implement" spec.md
# Verify: Uses BOTH V3 analysis + V4 execution
```

**Implementation**:
1. Create src/shannon/core/unified_orchestrator.py
2. Implement __init__ (wire all subsystems)
3. Implement execute_analysis (delegate to ContextAwareOrchestrator)
4. Implement execute_skills (delegate to orchestration.Orchestrator)
5. Implement execute_unified (intelligent routing)
6. Add error handling, graceful degradation

**Validation Gate 2.2**:
- ✅ Python compiles: `python -m py_compile src/shannon/core/unified_orchestrator.py`
- ✅ Imports work: `python -c "from shannon.core.unified_orchestrator import UnifiedOrchestrator; print('OK')"`
- ✅ Can instantiate: Test creates instance without errors
- ✅ Commit: "feat: Implement UnifiedOrchestrator core"

### Task 2.3: Wire UnifiedOrchestrator into Commands (2-3 hours)

**Actions**:
1. Update `shannon analyze` to use UnifiedOrchestrator.execute_analysis()
2. Update `shannon wave` to use UnifiedOrchestrator (keep wave logic)
3. Update `shannon do` to use UnifiedOrchestrator.execute_skills()
4. Update `shannon exec` to use UnifiedOrchestrator (keep exec logic)

**Example for analyze**:
```python
@cli.command()
def analyze(spec_file, ...):
    async def run():
        # OLD: orchestrator = ContextAwareOrchestrator()
        # NEW: orchestrator = UnifiedOrchestrator()
        result = await orchestrator.execute_analysis(spec_text, ...)
    anyio.run(run)
```

**Validation Gate 2.3**:
- ✅ `shannon analyze spec.md` works (uses unified orchestrator)
- ✅ Cache, analytics, cost features still work
- ✅ `shannon do "create file.py"` works (uses unified orchestrator)
- ✅ All 4 commands compile and run
- ✅ Commit: "refactor: Wire UnifiedOrchestrator into all commands"

### Task 2.4: Test UnifiedOrchestrator End-to-End (1 hour)

**Skill**: Use `test-driven-development` validation

**Functional Test**:
```bash
#!/bin/bash
# tests/functional/test_unified_orchestrator.sh

echo "Testing UnifiedOrchestrator integration..."

# Test analyze path
shannon analyze /tmp/test_spec.md
[ $? -eq 0 ] || exit 1

# Test do path
shannon do "create /tmp/test.py"
[ -f /tmp/test.py ] || exit 1

# Test cache works
time shannon analyze /tmp/test_spec.md  # Should be < 1s

echo "✓ UnifiedOrchestrator tests passed"
```

**Validation Gate 2.4**:
- ✅ Test script exits 0
- ✅ Both analyze and do commands work
- ✅ Cache still functional
- ✅ No regressions from V3/V4
- ✅ Commit: "test: Add UnifiedOrchestrator functional tests"

**PHASE 2 COMPLETE WHEN**:
- ✅ UnifiedOrchestrator implemented and tested
- ✅ All commands use unified orchestrator
- ✅ V3 and V4 features accessible from single entry point
- ✅ Functional test passing
- ✅ 4 commits created

---

## Phase 3: Fix Dashboard Event Integration (8-10 hours)

**Goal**: Fix critical blocker - dashboard real-time updates

### Task 3.1: Debug Event Emission (2-3 hours)

**Skill**: Use `systematic-debugging` MANDATORY

**Investigation Steps**:
1. Start server + dashboard
2. Run: `shannon do "create test.py"` with verbose logging
3. Check: orchestrator logs for emit_skill_event() calls
4. Check: server logs for Socket.IO emissions
5. Check: dashboard console for received events
6. Identify: Where does event emission break?

**Hypothesis Testing**:
- Hypothesis 1: dashboard_client not created in do command
- Hypothesis 2: emit_skill_event() not being called
- Hypothesis 3: Socket.IO broadcast not working
- Test each, find root cause

**Validation Gate 3.1**:
- ✅ Root cause identified and documented
- ✅ Evidence gathered (logs from all 3 layers)
- ✅ Fix approach determined
- ✅ Document: EVENT_EMISSION_DEBUG_FINDINGS.md

### Task 3.2: Implement Event Emission Fix (2-3 hours)

**Based on debugging findings, implement fix**

**Likely Scenarios**:

**Scenario A: dashboard_client not initialized**
```python
# In do command or UnifiedOrchestrator
dashboard_client = DashboardEventClient(url, session_id)
await dashboard_client.connect()
orchestrator.set_dashboard_client(dashboard_client)
```

**Scenario B: emit calls not in execution path**
```python
# In _execute_step or execute_skills
await self._emit_event('skill:started', {...})
# Execute skill
await self._emit_event('skill:completed', {...})
```

**Scenario C: Socket.IO emission broken**
```python
# Fix in websocket.py or communication/dashboard_client.py
await sio.emit(event_type, {'timestamp': ..., 'data': data})
```

**Validation Gate 3.2**:
- ✅ Code changes implemented
- ✅ Python compiles
- ✅ Manual test: Server logs show emission
- ✅ Commit: "fix: Dashboard event emission [root cause]"

### Task 3.3: Verify Dashboard Updates with Playwright (3-4 hours)

**Skill**: Use `playwright-skill` for ALL browser testing

**Test Script** (tests/functional/test_dashboard_events.sh):
```bash
#!/bin/bash
# Comprehensive dashboard event flow test

# Start server
python -m shannon.server.app > /tmp/server.log 2>&1 &
SERVER_PID=$!
sleep 5

# Start dashboard
cd dashboard && npm run dev > /tmp/dashboard.log 2>&1 &
DASHBOARD_PID=$!
sleep 10

# Run command with dashboard
shannon do "create /tmp/hello.py with hello world" --dashboard &
COMMAND_PID=$!

# Playwright verification
python << 'PLAYWRIGHT'
import asyncio
from mcp import playwright

async def test():
    # Navigate
    await playwright.browser_navigate("http://localhost:5173")

    # Wait for connection
    await playwright.browser_wait_for(text="Connected", timeout=10000)

    # Wait for skill execution
    await playwright.browser_wait_for(text="create", timeout=30000)

    # Take screenshot
    await playwright.browser_take_screenshot(filename="dashboard-events-working.png")

    # Verify Skills panel updated
    snapshot = await playwright.browser_snapshot()
    assert "create" in str(snapshot), "Skill not shown in dashboard"

    print("✓ Dashboard events working")

asyncio.run(test())
PLAYWRIGHT

# Cleanup
kill $SERVER_PID $DASHBOARD_PID $COMMAND_PID 2>/dev/null
```

**Validation Gate 3.3**:
- ✅ Playwright test passes
- ✅ Screenshot shows "create" in Skills panel
- ✅ Console logs show events: skill:started, skill:completed
- ✅ Dashboard updates in real-time (< 1s latency)
- ✅ Commit: "test: Dashboard event flow validated with Playwright"

**PHASE 3 COMPLETE WHEN**:
- ✅ Dashboard events emission working
- ✅ Real-time updates visible in UI
- ✅ Playwright test passing
- ✅ Screenshot evidence
- ✅ 3 commits created

---

## Phase 4: Complete V3 Context Integration (6-8 hours)

**Goal**: Wire V3 context management into UnifiedOrchestrator

### Task 4.1: Implement shannon onboard Command (2 hours)

**Currently**: Stub (lines 2491-2511 in commands.py)

**Implementation**:
```python
@cli.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--project-id', help='Project ID (defaults to dir name)')
@click.option('--force', is_flag=True, help='Force re-onboarding')
def onboard(project_path: str, project_id: Optional[str], force: bool):
    """Onboard existing codebase for context-aware operations."""
    async def run():
        config = ShannonConfig()
        orchestrator = UnifiedOrchestrator(config)

        # Call actual onboarding
        result = await orchestrator.context.onboard_project(
            project_path=Path(project_path).resolve(),
            project_id=project_id
        )

        # Display results
        console.print(f"✓ Onboarded: {result['project_id']}")
        console.print(f"  Files: {result['discovery']['file_count']}")
        console.print(f"  Lines: {result['discovery']['total_lines']}")
        console.print(f"  Tech: {', '.join(result['discovery']['tech_stack'])}")

    anyio.run(run)
```

**Validation Gate 4.1**:
- ✅ `shannon onboard /tmp/test-project` completes
- ✅ Creates ~/.shannon/projects/test-project/
- ✅ Displays: Files, lines, tech stack
- ✅ Exit code 0
- ✅ Commit: "feat: Complete shannon onboard implementation"

### Task 4.2: Verify Serena Storage (1 hour)

**Test Serena Integration**:
```bash
# After onboarding, check Serena
python << 'CHECK'
from mcp import search_nodes, open_nodes

# Search for project
results = search_nodes(query="test-project")
print(f"Serena entities: {len(results)}")

# Should find: project entity + modules + patterns
assert len(results) >= 3, "Missing Serena entities"
print("✓ Serena storage working")
CHECK
```

**Validation Gate 4.2**:
- ✅ Serena has project entity
- ✅ search_nodes returns >= 3 entities
- ✅ Entity count matches onboarding summary
- ✅ Test script exits 0

### Task 4.3: Test Context-Aware Analysis (2 hours)

**Functional Test**:
```bash
#!/bin/bash
# tests/functional/test_context.sh

# Setup
mkdir -p /tmp/test-context-project/src
echo "print('hello')" > /tmp/test-context-project/src/main.py
echo "# Test" > /tmp/test-context-project/README.md

# Onboard
shannon onboard /tmp/test-context-project --project-id test-ctx
[ $? -eq 0 ] || exit 1

# Analyze WITH context
cd /tmp/test-context-project
shannon analyze <(echo "Add logging feature") --project test-ctx > /tmp/with_context.txt

# Analyze WITHOUT context
shannon analyze <(echo "Add logging feature") > /tmp/without_context.txt

# Compare: With context should mention existing code
grep -q "existing" /tmp/with_context.txt || {
    echo "✗ Context not used in analysis"
    exit 1
}

echo "✓ Context-aware analysis working"
```

**Validation Gate 4.3**:
- ✅ Test script exits 0
- ✅ Analysis WITH context differs from WITHOUT
- ✅ Mentions existing code/patterns
- ✅ Commit: "test: Context-aware analysis validated"

### Task 4.4: Implement Remaining Context Commands (1-2 hours)

**Commands to complete**:
- `shannon context update` - Update context after code changes
- `shannon context clean` - Remove stale context

**Implementation**:
```python
@cli.command(name='context-update')
@click.option('--project', help='Project ID')
def context_update(project: Optional[str]):
    """Update project context after code changes."""
    async def run():
        orchestrator = UnifiedOrchestrator()
        changeset = await orchestrator.context.update_project(project)
        console.print(f"✓ Updated: {changeset.total_changes} changes")
    anyio.run(run)
```

**Validation Gate 4.4**:
- ✅ `shannon context update` works
- ✅ `shannon context clean` works
- ✅ Both commands functional, tested
- ✅ Commit: "feat: Complete context management commands"

**PHASE 4 COMPLETE WHEN**:
- ✅ shannon onboard functional
- ✅ Serena storage verified
- ✅ Context-aware analysis working
- ✅ All context commands implemented
- ✅ Functional test passing
- ✅ 4 commits created

---

## Phase 5: Wire Multi-Agent Execution (6-8 hours)

**Goal**: Activate AgentPool for parallel execution

### Task 5.1: Implement Agent Spawning in UnifiedOrchestrator (3 hours)

**Current**: AgentPool exists but never used

**Implementation**:
```python
# In UnifiedOrchestrator.execute_skills()
async def execute_skills(self, task, **opts):
    # Parse task into skills
    plan = await self.planner.create_plan(task)

    # For each skill in plan
    for skill_step in plan.steps:
        # Create agent task
        agent_task = AgentTask(
            task_id=f"task-{skill_step.skill_name}",
            description=skill_step.description,
            role=AgentRole.GENERIC
        )

        # Submit to pool (spawns agent)
        await self.agent_pool.submit_task(agent_task)

        # Register with tracker
        agent_id = f"agent-{agent_task.task_id}"
        self.agent_tracker.register_agent(
            agent_id=agent_id,
            wave_number=1,
            agent_type=skill_step.skill_name,
            task_description=skill_step.description
        )

        # Execute and track
        self.agent_tracker.mark_started(agent_id)
        result = await self._execute_with_tracking(skill_step, agent_id)
        self.agent_tracker.mark_complete(agent_id)

        # Emit event
        await self.dashboard_client.emit_event('agent:completed', {
            'agent_id': agent_id,
            'status': 'complete'
        })
```

**Validation Gate 5.1**:
- ✅ Code compiles
- ✅ Manual test: Logs show agent created
- ✅ AgentPool.get_agent_stats() shows agents > 0
- ✅ Commit: "feat: Wire AgentPool into UnifiedOrchestrator"

### Task 5.2: Test Multi-Agent Dashboard Display (2 hours)

**Skill**: Use `playwright-skill`

**Test**:
```bash
#!/bin/bash
# Start services
python -m shannon.server.app &
cd dashboard && npm run dev &
sleep 15

# Run multi-skill task
shannon do "create main.py, create tests.py, create README.md" --dashboard &

# Playwright: Verify AgentPool panel
python << 'TEST'
from mcp import playwright

await playwright.browser_navigate("http://localhost:5173")
await playwright.browser_wait_for(text="Connected")

# Wait for agents to appear
await playwright.browser_wait_for(text="agent-", timeout=30000)

# Screenshot
await playwright.browser_take_screenshot(filename="agents-active.png")

# Verify multiple agents
snapshot = await playwright.browser_snapshot()
# Should see agent entries in AgentPool panel

print("✓ Agents visible in dashboard")
TEST
```

**Validation Gate 5.2**:
- ✅ Playwright test passes
- ✅ Screenshot shows agents in AgentPool panel
- ✅ Real-time updates visible
- ✅ Commit: "test: Multi-agent dashboard verification"

### Task 5.3: Complete Agent Control Commands (1-2 hours)

**Implement**:
- `shannon wave follow <agent_id>` - Stream one agent's messages
- `shannon wave pause` - Pause execution
- `shannon wave resume` - Resume execution

**Using AgentController**:
```python
@cli.command(name='wave-follow')
@click.argument('agent_id')
def wave_follow(agent_id: str):
    """Stream messages from specific agent."""
    async def run():
        orchestrator = UnifiedOrchestrator()

        # Use AgentController.follow_agent()
        def print_message(msg):
            console.print(msg)

        await orchestrator.agent_controller.follow_agent(
            agent_id,
            message_callback=print_message
        )
    anyio.run(run)
```

**Validation Gate 5.3**:
- ✅ All 3 commands functional
- ✅ `shannon wave follow agent-X` streams messages
- ✅ `shannon wave pause` works
- ✅ Exit codes correct
- ✅ Commit: "feat: Complete agent control commands"

**PHASE 5 COMPLETE WHEN**:
- ✅ AgentPool spawns agents during execution
- ✅ AgentStateTracker tracks them
- ✅ Dashboard shows agents real-time
- ✅ Agent control commands functional
- ✅ Playwright verification passed
- ✅ 3 commits created

---

## Phase 6: Comprehensive Functional Testing (8-10 hours)

**Goal**: Validate EVERYTHING with functional tests only

### Task 6.1: Create Complete Test Suite (4 hours)

**Create ALL functional tests** (tests/functional/):

**1. test_basic.sh** (30 min):
```bash
#!/bin/bash
# Basic command functionality

shannon --version
shannon --help
shannon status
shannon config

echo "✓ Basic commands work"
```

**2. test_analyze.sh** (1 hour):
```bash
#!/bin/bash
# Analyze with full V3 integration

# First run (cache miss)
time shannon analyze spec.md | tee /tmp/analyze1.log
FIRST_TIME=$SECONDS

# Second run (cache hit)
SECONDS=0
shannon analyze spec.md | tee /tmp/analyze2.log
SECOND_TIME=$SECONDS

# Verify cache hit
[ $SECOND_TIME -lt 1 ] || exit 1
grep -q "Cache hit" /tmp/analyze2.log || exit 1

# Verify analytics recorded
shannon analytics | grep -q "session" || exit 1

echo "✓ Analyze with cache + analytics works"
```

**3. test_do.sh** (1 hour):
```bash
#!/bin/bash
# Skills-based execution

# Create file
shannon do "create /tmp/test.py with hello world"
[ -f /tmp/test.py ] || exit 1
grep -q "hello" /tmp/test.py || exit 1

# Multi-file
shannon do "create main.py, utils.py, tests.py"
[ -f main.py ] && [ -f utils.py ] && [ -f tests.py ] || exit 1

echo "✓ shannon do works"
```

**4. test_exec.sh** (1 hour):
```bash
#!/bin/bash
# V3.5 autonomous executor

shannon exec "create calculator.py that adds two numbers"
[ -f calculator.py ] || exit 1
python calculator.py  # Should run without errors

echo "✓ shannon exec works"
```

**5. test_context.sh** (from Phase 4)

**6. test_dashboard.sh** (1.5 hours):
```bash
#!/bin/bash
# Complete dashboard integration

# Start services
python -m shannon.server.app &
cd dashboard && npm run dev &
sleep 15

# Test all 6 panels with Playwright
python << 'TEST'
from mcp import playwright

await playwright.browser_navigate("http://localhost:5173")
await playwright.browser_wait_for(text="Connected")

# Run command in background
# shannon do "create test.py" --dashboard &

# Wait for each panel to update
# ExecutionOverview
await playwright.browser_wait_for(text="create test.py")
await playwright.browser_take_screenshot(filename="panel-execution.png")

# Skills
# Verify skills panel shows skill

# Validation
# Verify validation panel (if validation runs)

# FileChanges
await playwright.browser_wait_for(text="test.py")
await playwright.browser_take_screenshot(filename="panel-files.png")

# AgentPool
# Verify agents shown

print("✓ All dashboard panels functional")
TEST
```

**Validation Gate 6.1**:
- ✅ All 6 test scripts created
- ✅ Each script has clear validation logic
- ✅ No pytest, all functional
- ✅ Commit: "test: Complete functional test suite"

### Task 6.2: Run All Tests and Fix Failures (3-4 hours)

**Requires**: ANTHROPIC_API_KEY set

**Run Suite**:
```bash
#!/bin/bash
# tests/functional/run_all.sh

export ANTHROPIC_API_KEY="..."  # From environment

PASSED=0
FAILED=0

for test in tests/functional/test_*.sh; do
    echo "Running $test..."
    if bash $test; then
        PASSED=$((PASSED + 1))
        echo "✓ PASSED"
    else
        FAILED=$((FAILED + 1))
        echo "✗ FAILED"
    fi
done

echo ""
echo "Results: $PASSED passed, $FAILED failed"

[ $FAILED -eq 0 ] || exit 1
```

**For Each Failure**:
1. Use `systematic-debugging` skill
2. Identify root cause
3. Fix incrementally
4. Re-run test
5. Commit fix

**Validation Gate 6.2**:
- ✅ run_all.sh exits 0 (all tests pass)
- ✅ Each test validated individually
- ✅ Evidence: run_all.sh output shows "N passed, 0 failed"
- ✅ Commits: One per major fix (if needed)

### Task 6.3: Performance Validation (1-2 hours)

**Measure against V3 criteria**:

```bash
#!/bin/bash
# tests/functional/test_performance.sh

# Cache speed (< 500ms)
SECONDS=0
shannon analyze cached_spec.md  # Second run
TIME=$SECONDS
[ $TIME -lt 1 ] || exit 1

# Memory usage (< 200MB)
shannon analyze big_spec.md &
PID=$!
sleep 5
MEM=$(ps -o rss= -p $PID | awk '{print $1/1024}')
[ $(echo "$MEM < 200" | bc) -eq 1 ] || exit 1

# Context loading (< 30s)
SECONDS=0
shannon prime --project test-ctx
TIME=$SECONDS
[ $TIME -lt 30 ] || exit 1

echo "✓ All performance targets met"
```

**Validation Gate 6.3**:
- ✅ Cache hits < 500ms
- ✅ Memory < 200MB
- ✅ Context loading < 30s
- ✅ All 4 performance criteria met

**PHASE 6 COMPLETE WHEN**:
- ✅ All functional tests created (6 scripts)
- ✅ run_all.sh passes (100% pass rate)
- ✅ Performance validated
- ✅ Evidence: Test outputs + measurements
- ✅ 5+ commits created

---

## Phase 7: Command Consolidation (4-5 hours)

**Goal**: Rationalize 40 → 25 commands

### Task 7.1: Deprecate Redundant Commands (2 hours)

**Deprecate** (don't delete, just mark deprecated):
```python
@cli.command()
@click.pass_context
def task(ctx):
    """[DEPRECATED] Use 'shannon do' instead."""
    ctx.invoke(do_command, ...)  # Redirect to do
```

**Commands to deprecate**:
- `task` → alias to `do`
- `test` → absorbed into validation
- `checkpoint`, `restore` → internal operations
- `prime` → auto-invoked by context commands
- `discover_skills` → auto-invoked by do
- `check_mcps` → auto-invoked by analyze

**Validation Gate 7.1**:
- ✅ Commands still work (redirected)
- ✅ Show deprecation warning
- ✅ Help text updated
- ✅ Commit: "refactor: Deprecate redundant commands"

### Task 7.2: Update Help and Documentation (2 hours)

**Update**:
- `shannon --help` shows only 25 primary commands
- Each command help updated
- Deprecated commands in separate section

**Validation Gate 7.2**:
- ✅ `shannon --help` shows clean command list
- ✅ No confusion about which commands to use
- ✅ Commit: "docs: Update command help for V5"

**PHASE 7 COMPLETE WHEN**:
- ✅ 40 → 25 command rationalization complete
- ✅ Help text updated
- ✅ 2 commits created

---

## Phase 8: Final Documentation & Release (4-5 hours)

**Goal**: Production-ready V5.0 release

### Task 8.1: Update README.md (1.5 hours)

**Complete rewrite** focusing on:
- V5 unified vision
- Primary commands: do, exec, analyze
- Quick start guide
- Feature showcase
- Installation
- Examples

**Validation Gate 8.1**:
- ✅ README accurate, complete
- ✅ Examples all work
- ✅ Commit: "docs: V5 README rewrite"

### Task 8.2: Update CHANGELOG.md (1 hour)

**Add V5 entry**:
```markdown
## [5.0.0] - 2025-11-XX

### 🎉 V5: Unified Platform

Consolidates V3 (context-aware analysis) and V4 (skills-based execution) into unified system.

### Added
- UnifiedOrchestrator: Single orchestrator for all operations
- Real-time dashboard updates (all 6 panels functional)
- Multi-agent parallel execution
- Complete context management (onboard, update, clean)
- Agent control commands (wave-agents, wave-follow, wave-pause)

### Changed
- All commands use UnifiedOrchestrator
- 40 commands → 25 commands (deprecated redundant)
- Testing: 100% functional (deleted all pytest per mandate)

### Fixed
- Dashboard WebSocket event emission
- Context onboarding integration
- Agent tracking persistence
- Cache datetime serialization
- Analytics parameter mismatch

### Removed
- 412 pytest test files (Shannon mandate: functional only)
- 50+ status documentation files (archived)
- Duplicate orchestration code
```

**Validation Gate 8.2**:
- ✅ CHANGELOG complete
- ✅ Commit: "docs: V5 CHANGELOG"

### Task 8.3: Final Success Criteria Check (1 hour)

**Skill**: Use `honest-reflections` MANDATORY

**Check ALL criteria**:

**Functional** (V3 + V4 combined):
- ✅ shannon do fully functional
- ✅ shannon exec fully functional
- ✅ shannon analyze with all V3 features
- ✅ Dashboard real-time updates
- ✅ Multi-agent coordination
- ✅ Context management complete
- ✅ All 25 commands work

**Quality**:
- ✅ All functional tests passing (run_all.sh exits 0)
- ✅ NO pytest files
- ✅ Clean codebase
- ✅ Complete documentation

**Performance**:
- ✅ Cache < 500ms
- ✅ Memory < 200MB
- ✅ Context < 30s
- ✅ Dashboard < 1s latency

**Integration**:
- ✅ UnifiedOrchestrator coordinates all features
- ✅ V3 and V4 features work together
- ✅ No duplicate systems

**Validation Gate 8.3**:
- ✅ ALL criteria checked
- ✅ Honest assessment documented
- ✅ Any gaps noted for post-V5

### Task 8.4: Tag V5.0.0 Release (30 min)

**Final Steps**:
```bash
# Verify clean state
git status  # Should be clean

# Create annotated tag
git tag -a v5.0.0 -m "Shannon CLI V5.0: Unified Platform

V5 consolidates V3 (context-aware analysis) and V4 (skills-based execution)
into a unified, production-ready platform.

Key Features:
- UnifiedOrchestrator coordinating all subsystems
- Real-time dashboard with WebSocket updates
- Multi-agent parallel execution
- Complete context management
- 25 primary commands (consolidated from 40)
- 100% functional testing (deleted pytest per mandate)

Stats:
- 41,865 lines of Python
- 25 commands
- 6 dashboard panels
- All functional tests passing
- Production ready

See CHANGELOG.md for complete details.
"

# Verify tag
git tag -l -n9 v5.0.0
```

**Validation Gate 8.4**:
- ✅ Tag created
- ✅ Annotated with complete message
- ✅ Points to final V5 commit
- ✅ Git log shows tag

**PHASE 8 COMPLETE WHEN**:
- ✅ README updated
- ✅ CHANGELOG updated
- ✅ All success criteria verified
- ✅ Tag v5.0.0 created
- ✅ Shannon CLI V5.0 production ready

---

## Validation Philosophy

### Functional Testing ONLY

**NO**:
- ❌ pytest files
- ❌ Unit tests
- ❌ Mock objects
- ❌ Test fixtures
- ❌ Isolated component tests

**YES**:
- ✅ Shell scripts (tests/functional/*.sh)
- ✅ Real CLI commands (`shannon do "..."`)
- ✅ Real API calls (require ANTHROPIC_API_KEY)
- ✅ Real file system operations
- ✅ Browser automation (Playwright MCP)
- ✅ Real WebSocket connections
- ✅ Observable behavior verification

### Validation Gate Pattern

**Every gate follows this structure**:
```bash
#!/bin/bash
# Test: Feature X works

# ARRANGE: Setup test conditions
mkdir -p /tmp/test && cd /tmp/test

# ACT: Execute REAL command
shannon do "create file.py" > /tmp/output.log 2>&1
EXIT_CODE=$?

# ASSERT: Verify observable behavior
[ $EXIT_CODE -eq 0 ] || exit 1
[ -f file.py ] || exit 1
grep -q "def" file.py || exit 1

# EVIDENCE: Capture proof
echo "Exit code: $EXIT_CODE"
echo "File created: $(ls file.py)"
echo "Content: $(head -3 file.py)"

echo "✓ Test passed"
exit 0
```

**For Dashboard Tests** (using Playwright MCP):
```python
# Via browser MCP
from mcp import playwright

# Navigate
await playwright.browser_navigate("http://localhost:5173")

# Wait for expected state
await playwright.browser_wait_for(text="Expected Text", timeout=10000)

# Take screenshot (EVIDENCE)
await playwright.browser_take_screenshot(filename="evidence.png")

# Verify state
snapshot = await playwright.browser_snapshot()
assert "Expected Element" in str(snapshot)

print("✓ Browser test passed")
```

**MANDATORY**:
- Real execution (not mocked)
- Observable outcome (file created, dashboard updated, exit code 0)
- Evidence captured (logs, screenshots, files)
- Clear pass/fail (exit 0 or exit 1)

---

## Timeline & Estimates

**Total**: 46 hours across 8 phases

| Phase | Duration | Complexity | Blockers |
|-------|----------|------------|----------|
| 0. Context Loading | Auto | N/A | None (skill handles) |
| 1. Cleanup | 2-3h | Low | None |
| 2. UnifiedOrchestrator | 8-10h | High | Design complexity |
| 3. Dashboard Events | 8-10h | High | Root cause unknown |
| 4. Context Integration | 6-8h | Medium | Serena dependency |
| 5. Multi-Agent | 6-8h | Medium | Agent system consolidation |
| 6. Testing | 8-10h | Medium | API key required |
| 7. Commands | 4-5h | Low | None |
| 8. Documentation | 4-5h | Low | None |

**Critical Path**: Phase 2 (orchestrator) → Phase 3 (events) → Phase 5 (agents)

**Parallelizable**: Phase 4 (context) can be done alongside Phase 2

**Buffer**: +20% for unexpected issues = 55 hours total

---

## 2M Token Context Strategy

**Session will be LONG** - plan for extended execution:

### Context Preservation (Every 500K tokens)
1. Create checkpoint with TodoWrite
2. Save progress to Serena memory
3. Document current state
4. If approaching 1.5M tokens: Create handoff document

### File Reading Strategy
- Use Serena MCP `read_file` with max_answer_chars limits
- Read complete files once, reference in thoughts
- Use `find_symbol` for targeted reading
- Cache understanding in working memory

### Working Memory Management
- Keep: Current phase goals, validation gates, code changes
- Discard: Old debugging output, superseded analysis
- Checkpoint: After each phase completion

### Priming for Continuation
If session ends before V5 complete:
1. Write COMPREHENSIVE_V5_STATUS.md (what's done, what's left)
2. Save to Serena: "SHANNON_V5_SESSION_CHECKPOINT"
3. Next session starts with session-context-priming (reads checkpoint)

---

## Recovery & Blockers

### If Stuck on Any Task

**STOP Immediately**:
- Use `systematic-debugging` skill
- Document blocker
- Don't guess/patch
- Ask for guidance if needed

### If Validation Gate Fails

**DO NOT SKIP**:
- Diagnose why test failed
- Fix root cause
- Re-run until passes
- Document what was wrong

### If Running Out of Time

**Graceful Degradation**:
1. Complete current phase
2. Commit all progress
3. Create detailed handoff
4. Document: "V5 80% complete, Phase X remaining"

**Phases in Priority Order**:
1. Phase 2 (UnifiedOrchestrator) - CRITICAL
2. Phase 3 (Dashboard events) - CRITICAL
3. Phase 6 (Testing) - MUST DO
4. Phase 4 (Context) - IMPORTANT
5. Phase 5 (Agents) - IMPORTANT
6. Phase 7 (Commands) - NICE TO HAVE
7. Phase 8 (Docs) - NICE TO HAVE
8. Phase 1 (Cleanup) - CAN DEFER

---

## Success Criteria (ALL Must Be Met)

### Functional
- ✅ shannon do executes tasks with real-time dashboard
- ✅ shannon exec generates code autonomously
- ✅ shannon analyze provides 8D analysis with caching
- ✅ shannon onboard indexes codebases
- ✅ shannon wave-agents shows agent status
- ✅ All 25 primary commands functional

### Quality
- ✅ 0 pytest files (all deleted)
- ✅ All functional tests passing (tests/functional/run_all.sh exits 0)
- ✅ Clean codebase (< 10 .md files in root)
- ✅ Comprehensive documentation

### Performance
- ✅ Cache hits < 500ms
- ✅ Memory usage < 200MB
- ✅ Context loading < 30s
- ✅ Dashboard latency < 1s

### Integration
- ✅ UnifiedOrchestrator coordinates V3 + V4
- ✅ Dashboard shows real-time updates (all 6 panels)
- ✅ V3 features available to all commands
- ✅ V4 features available to all commands

### Production Readiness
- ✅ README accurate and complete
- ✅ CHANGELOG with V5 entry
- ✅ Tag v5.0.0 created
- ✅ No known critical bugs

---

## Execution Workflow for Next Session

### Step 1: Session Startup (Auto - 60-90 min)
```
/execute-plan @docs/plans/SHANNON_V5_CONSOLIDATION_PLAN.md
# Auto-invokes session-context-priming first
# Reads all files, memories, 200+ thoughts
# Then begins plan execution
```

### Step 2: Phase Execution (Batched)
- Batch 1: Phase 1 (Cleanup - 3 tasks)
- Batch 2: Phase 2 Part A (Design + Core - 2 tasks)
- Batch 3: Phase 2 Part B (Wiring + Testing - 2 tasks)
- Batch 4: Phase 3 (Events debugging + fix - 3 tasks)
- Batch 5: Phase 4 (Context complete - 4 tasks)
- Batch 6: Phase 5 (Agents wiring - 3 tasks)
- Batch 7: Phase 6 (Testing - 3 tasks)
- Batch 8: Phase 7 (Commands - 2 tasks)
- Batch 9: Phase 8 (Docs + Release - 4 tasks)

**Between batches**: Report, get feedback, continue

### Step 3: Validation (Continuous)
- After each task: Pass validation gate or debug
- After each phase: Comprehensive verification
- Before release: Final success criteria check

---

## Critical Dependencies

**Required for Testing**:
- ✅ ANTHROPIC_API_KEY environment variable
- ✅ Shannon Framework installed/accessible
- ✅ Playwright browser installed
- ✅ Node.js + npm (for dashboard)
- ✅ Python 3.10+

**External Services**:
- Serena MCP for context storage
- (Optional) Other MCPs as discovered during execution

---

## Post-V5 Roadmap

**After V5 Complete**:
1. Performance optimization (< 100ms response times)
2. Additional built-in skills (15+ total)
3. Skill marketplace
4. Cloud backend option
5. Team collaboration features

---

**END OF SHANNON V5 CONSOLIDATION PLAN**

**This plan represents a systematic path to consolidating V3 + V4 into unified V5 platform with 100% functional testing, clean architecture, and production readiness.**

**Next Session**: Start with session-context-priming, then execute phases 1-8 in batches with mandatory validation gates.
