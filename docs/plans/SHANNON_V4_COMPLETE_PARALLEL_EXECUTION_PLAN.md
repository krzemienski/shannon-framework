# Shannon V4: Complete Parallel Wave Execution Plan

> **Execution Philosophy**: Validation-driven parallel development with WORK-UNTIL-PASS gates and Serena MCP coordination
>
> **Timeline**: ~2 weeks (10h implementation + 1w integration + 3d release)
> **Structure**: 1 Solo Batch + 2 Parallel Waves + Integration + Release
> **Validation**: 283 specific, measurable criteria with Playwright evidence
> **Coordination**: Serena MCP memories for agent synchronization
> **Branch Strategy**: agent1-multifile, agent2-pool, agent3-decisions, agent4-research, agent5-ultrathink, agent6-controls, agent7-advanced, agent8-filediff

---

## Table of Contents

1. [Execution Architecture](#execution-architecture)
2. [File Ownership Map](#file-ownership-map)
3. [Serena MCP Coordination Protocol](#serena-mcp-coordination-protocol)
4. [Branch Strategy](#branch-strategy)
5. [Orchestrator Responsibilities](#orchestrator-responsibilities)
6. [Batch 1: Validation Streaming (Solo)](#batch-1-validation-streaming-solo)
7. [Wave 1: Core Features (6 Agents)](#wave-1-core-features-6-agents)
8. [Wave 2: Advanced Features (2 Agents)](#wave-2-advanced-features-2-agents)
9. [Integration & Release](#integration-release)

---

## Execution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (You)                        │
│  - Monitor SITREPs from all agents                          │
│  - Coordinate via Serena memories                           │
│  - Merge branches when validated                            │
│  - Run integration tests                                    │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │ BATCH 1 │         │ WAVE 1  │         │ WAVE 2  │
   │  Solo   │────────▶│ 6 Agents│────────▶│ 2 Agents│
   │ 3 hours │         │ 4 hours │         │ 3 hours │
   └─────────┘         └─────────┘         └─────────┘
        │                    │                    │
        └────────────────────┴────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  INTEGRATION    │
                    │  1 week         │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   RELEASE       │
                    │   3-5 days      │
                    └─────────────────┘
```

### Parallel Execution Benefits

**Sequential (OLD)**: Batch 1 (3h) → Agent 1 (3h) → Agent 2 (3h) → ... → Agent 8 (3h) = **27 hours**

**Parallel (NEW)**: Batch 1 (3h) → Wave 1 [6 agents parallel] (4h) → Wave 2 [2 agents parallel] (3h) = **10 hours**

**Time Savings**: 63% reduction (27h → 10h)

---

## File Ownership Map

**Purpose**: Prevent merge conflicts by assigning file ownership to specific agents

### Backend Files

| File | Owner | Shared? | Conflict Strategy |
|------|-------|---------|-------------------|
| `src/shannon/orchestration/multi_file_parser.py` | Agent 1 | No | N/A |
| `src/shannon/executor/multi_file_executor.py` | Agent 1 | No | N/A |
| `src/shannon/orchestration/agent_pool.py` | Agent 2 | No | N/A |
| `src/shannon/orchestration/orchestrator.py` | **Multiple** | **YES** | **Merge strategy below** |
| `src/shannon/orchestration/decision_engine.py` | Agent 3 | No | N/A |
| `src/shannon/research/orchestrator.py` | Agent 4 | No | N/A |
| `src/shannon/modes/ultrathink.py` | Agent 5 | No | N/A |
| `src/shannon/modes/debug_mode.py` | Agent 6 | No | N/A |
| `src/shannon/server/websocket.py` | **Multiple** | **YES** | **Merge strategy below** |
| `src/shannon/executor/validator.py` | Batch 1 | No | N/A |

### Frontend Files

| File | Owner | Shared? | Conflict Strategy |
|------|-------|---------|-------------------|
| `dashboard/src/store/dashboardStore.ts` | **Multiple** | **YES** | **Merge strategy below** |
| `dashboard/src/panels/AgentPool.tsx` | Agent 2 | No | N/A |
| `dashboard/src/panels/Decisions.tsx` | Agent 3 | No | N/A |
| `dashboard/src/panels/Validation.tsx` | Batch 1 | No | N/A |
| `dashboard/src/panels/FileDiff.tsx` | Agent 8 | No | N/A |

### Shared File Merge Strategy

**For `orchestrator.py`**:
- Agent 2 adds: `_execute_via_agent()`, `_execute_parallel_steps()`
- Agent 3 adds: `_handle_decision_point()`
- Agent 6 adds: `halt_requested` flag, `resume()`, `rollback()`

**Merge Protocol**:
1. Each agent works in their own section of the file
2. Agents add methods, don't modify existing ones
3. Orchestrator (you) merges branches sequentially:
   - Merge agent2-pool → master
   - Merge agent3-decisions → master (now includes agent2 changes)
   - Merge agent6-controls → master (now includes agent2+3 changes)
4. After each merge: Run full test suite to detect conflicts

**For `dashboardStore.ts`**:
- Agent 2 adds: `agents` state, `addAgent()`, `updateAgent()`
- Agent 3 adds: `decisions` state, `addDecision()`, `approveDecision()`
- Batch 1 adds: `validationOutput` state

**Merge Protocol**:
1. Each agent adds their own state variables and methods
2. Each agent adds their own event handlers in `handleSocketEvent()`
3. Orchestrator merges in dependency order:
   - Merge batch1-validation (foundation)
   - Merge agent2-pool
   - Merge agent3-decisions
4. Test dashboard after each merge

**For `websocket.py`**:
- Agent 3 adds: `approve_decision(sid, data)` handler
- Agent 6 adds: `halt_execution(sid, data)`, `resume_execution(sid, data)`, `rollback_execution(sid, data)` handlers
- Agent 7 adds: `redirect_execution(sid, data)`, `inject_context(sid, data)` handlers

**Merge Protocol**:
1. Each agent adds independent event handlers
2. No modification of existing handlers
3. Orchestrator merges all branches (handlers don't conflict)

---

## Serena MCP Coordination Protocol

**Purpose**: Enable agents to coordinate without direct communication

### Memory Structure

**Location**: `.serena/project-memories/shannon-v4-parallel-wave/`

**Memory Files**:
1. `agent-status.md` - Agent health and progress
2. `shared-state.md` - Cross-agent coordination data
3. `file-locks.md` - File access coordination
4. `test-results.md` - Validation outcomes
5. `blockers.md` - Agent blockers requiring orchestrator intervention

### Memory Format Examples

**agent-status.md**:
```markdown
# Agent Status Tracking

## Agent 1: Multi-File (agent1-multifile branch)
- Status: IN_PROGRESS
- Phase: Backend Implementation (Phase 2/4)
- Last Updated: 2025-11-16T14:30:00Z
- Progress: 12/26 criteria
- Blockers: None
- ETA: 1.5 hours remaining

## Agent 2: Agent Pool (agent2-pool branch)
- Status: WAITING_ON_DEPENDENCY
- Waiting For: Agent 1 multi-file functionality
- Last Updated: 2025-11-16T14:25:00Z
- Progress: 0/32 criteria
- Blockers: Cannot test until Agent 1 completes
- ETA: Starts after Agent 1

## Agent 3: Decisions (agent3-decisions branch)
- Status: NOT_STARTED
- Last Updated: 2025-11-16T14:20:00Z
```

**shared-state.md**:
```markdown
# Shared State Coordination

## Dashboard Connection
- Port: 5175
- Status: RUNNING
- Started By: Batch 1
- Available For: All agents

## Test Database
- Location: /tmp/shannon-v4-test
- Initialized: Yes
- Clean State: Yes

## MCP Connections
- Sequential Thinking: CONNECTED
- Fire Crawl: CONNECTED
- Tavily: CONNECTED
- Serena: CONNECTED (you're reading this!)
```

**file-locks.md**:
```markdown
# File Access Locks

## LOCKED Files
- `src/shannon/orchestrator.py` - LOCKED by Agent 2 (14:25:00Z)
- `dashboard/src/store/dashboardStore.ts` - LOCKED by Batch 1 (14:20:00Z)

## Available Files
- All other files available for modification
```

**test-results.md**:
```markdown
# Test Validation Results

## Batch 1: Validation Streaming
- Status: COMPLETED
- Criteria: 27/27 PASS
- Evidence: batch1-validation-streaming-working.png
- Timestamp: 2025-11-16T13:00:00Z

## Agent 1: Multi-File
- Status: IN_PROGRESS
- Criteria: 12/26 PASS
- Current Gate: Backend Unit Tests (Gate 1/4)
- Last Test Run: 2025-11-16T14:28:00Z
```

**blockers.md**:
```markdown
# Agent Blockers

## Agent 2: Agent Pool
**Blocker**: Cannot test multi-agent functionality without multi-file working
**Severity**: BLOCKING
**Requested**: Orchestrator approval to begin after Agent 1 Gate 2
**Status**: WAITING

## Agent 5: Ultrathink
**Blocker**: Sequential MCP connection unstable (timeout after 300 thoughts)
**Severity**: HIGH
**Requested**: Orchestrator investigate MCP connection
**Status**: INVESTIGATING
```

### Serena Read/Write Protocol

**Before Starting Work** (Every Agent):
```python
# Read current agent status
status = serena.read_memory("agent-status.md")
# Check for blockers
blockers = serena.read_memory("blockers.md")
# Verify file not locked
locks = serena.read_memory("file-locks.md")
```

**During Work** (Every 15 minutes):
```python
# Update agent status
serena.write_memory("agent-status.md", f"""
## Agent {N}: {Feature}
- Status: {current_status}
- Phase: {current_phase}
- Last Updated: {timestamp}
- Progress: {criteria_passing}/{total_criteria} criteria
- Blockers: {blockers_list}
- ETA: {estimated_time_remaining}
""")
```

**Before Modifying Shared File**:
```python
# Acquire lock
serena.write_memory("file-locks.md", f"""
## LOCKED Files
- `{file_path}` - LOCKED by Agent {N} ({timestamp})
""")

# Do work on file

# Release lock
serena.write_memory("file-locks.md", f"""
## Available Files
- `{file_path}` - Available (released by Agent {N})
""")
```

**After Completing Gate**:
```python
# Report gate completion
serena.write_memory("test-results.md", f"""
## Agent {N}: {Feature}
- Status: GATE_{gate_num}_COMPLETE
- Criteria: {criteria_passing}/{total_criteria} PASS
- Evidence: {screenshot_filename}
- Timestamp: {timestamp}
- Next Gate: Gate {gate_num + 1} ({gate_name})
""")
```

**When Blocked**:
```python
# Report blocker
serena.write_memory("blockers.md", f"""
## Agent {N}: {Feature}
**Blocker**: {description}
**Severity**: {BLOCKING|HIGH|MEDIUM|LOW}
**Requested**: {action_from_orchestrator}
**Status**: WAITING
**Timestamp**: {timestamp}
""")
```

### Orchestrator (Your) Serena Protocol

**Every 10 Minutes**:
```python
# Check all agent statuses
status = serena.read_memory("agent-status.md")
# Review blockers
blockers = serena.read_memory("blockers.md")
# Check test results
tests = serena.read_memory("test-results.md")

# Take action if needed:
# - Resolve blockers
# - Merge completed branches
# - Coordinate dependencies
```

**When Agent Reports GATE_COMPLETE**:
```python
# Read test results
results = serena.read_memory("test-results.md")
# Verify evidence exists
verify_screenshot(results.evidence)
# If validated, merge branch
if all_criteria_pass:
    merge_agent_branch(agent_num)
    update_status("MERGED")
```

---

## Branch Strategy

### Branch Naming Convention

- `master` - Main integration branch
- `batch1-validation` - Batch 1 solo work
- `agent1-multifile` - Agent 1: Multi-File Generation
- `agent2-pool` - Agent 2: Agent Pool
- `agent3-decisions` - Agent 3: Decision Engine
- `agent4-research` - Agent 4: Research Orchestration
- `agent5-ultrathink` - Agent 5: Ultrathink Engine
- `agent6-controls` - Agent 6: Basic Controls
- `agent7-advanced` - Agent 7: Advanced Controls
- `agent8-filediff` - Agent 8: FileDiff Panel

### Branch Lifecycle

**Creation**:
```bash
# Orchestrator creates branch for each agent
git checkout -b agent1-multifile
git push -u origin agent1-multifile

# Agent 1 starts work in this branch
# All commits go to agent1-multifile
```

**During Work**:
```bash
# Agent commits frequently
git add src/shannon/orchestration/multi_file_parser.py
git commit -m "feat: MultiFileParser pattern detection"

# Push to remote for backup
git push origin agent1-multifile
```

**After Gate Completion**:
```bash
# Agent reports via Serena
serena.write_memory("test-results.md", "Agent 1 Gate 4/4 COMPLETE")

# Orchestrator verifies and merges
git checkout master
git merge agent1-multifile --no-ff -m "Merge agent1-multifile: Multi-File Generation - 26/26 validated"
git push origin master

# Branch kept for reference (not deleted)
```

### Merge Order (Critical!)

**Wave 1 Dependencies**:
1. `batch1-validation` → `master` (FIRST - foundation)
2. `agent1-multifile` → `master` (SECOND - needed by agent 2 tests)
3. `agent2-pool` → `master` (uses orchestrator.py)
4. `agent3-decisions` → `master` (uses orchestrator.py, agents)
5. `agent4-research` → `master` (independent)
6. `agent5-ultrathink` → `master` (independent)
7. `agent6-controls` → `master` (modifies orchestrator.py)

**Wave 2 Dependencies**:
1. `agent7-advanced` → `master` (builds on agent6-controls)
2. `agent8-filediff` → `master` (independent)

**Conflict Resolution**:
- If merge conflict in shared file:
  1. Identify conflicting sections
  2. Agent who merged last resolves conflict
  3. Run full test suite after resolution
  4. Re-validate affected criteria

---

## Orchestrator Responsibilities

**Your Role**: Master coordinator, merger, validator

### Daily Responsibilities

**Morning** (Every Day):
1. Read Serena `agent-status.md` - Check agent health
2. Read Serena `blockers.md` - Identify blocking issues
3. Review SITREPs from overnight work (if async)
4. Plan day: Which agents to merge today?

**Every 2 Hours** (During Active Development):
1. Check Serena memories for updates
2. Review SITREP reports (agents report every 30 min)
3. Merge completed agent branches
4. Run integration tests after merge
5. Update orchestrator status in Serena

**When Agent Reports GATE COMPLETE**:
1. Read `test-results.md` for agent's gate
2. Verify evidence exists (screenshot, logs)
3. Pull agent's branch
4. Run validation criteria locally
5. If all pass: Merge to master
6. If any fail: Report back to agent via Serena blocker

**When Agent Reports BLOCKER**:
1. Read `blockers.md` for details
2. Investigate issue (MCP connection, dependency, etc.)
3. Resolve if possible
4. Update blocker status in Serena
5. Notify agent to resume

### Merge Protocol (Step-by-Step)

```bash
# 1. Agent reports Gate 4/4 complete via Serena
# 2. You verify in test-results.md

# 3. Pull latest master
git checkout master
git pull origin master

# 4. Pull agent's branch
git fetch origin agent1-multifile
git checkout agent1-multifile
git pull origin agent1-multifile

# 5. Verify tests pass in agent's branch
pytest tests/orchestration/test_multi_file*.py -v
# Expected: All tests PASS

# 6. Verify evidence exists
ls batch1-multi-file-validated.png
# Expected: File exists

# 7. Merge to master (no fast-forward to preserve history)
git checkout master
git merge agent1-multifile --no-ff -m "Merge agent1-multifile: Multi-File Generation

VALIDATED: 26/26 criteria passed

Backend:
- MultiFileParser: Pattern detection working
- MultiFileExecutor: Creates all files correctly
- Integration: shannon do multi-file working

Frontend:
- file:created events flowing
- FileDiff panel populates (if implemented)

Tests: 226 passing (added 5)
Evidence: batch1-multi-file-validated.png
Agent: Claude Agent 1
Branch: agent1-multifile
"

# 8. Run full test suite on master
pytest -v
# Expected: All tests pass (including new tests)

# 9. Push to remote
git push origin master

# 10. Update Serena
serena.write_memory("agent-status.md", "Agent 1: MERGED")
serena.write_memory("test-results.md", "Agent 1: MERGED to master at {timestamp}")
```

### Integration Test Protocol

**After Each Merge**:
```bash
# 1. Run full test suite
pytest -v --tb=short
# Must: ALL tests pass

# 2. Start dashboard
cd dashboard && npm run dev &
# Wait for "Local: http://localhost:5175"

# 3. Test merged feature via CLI + Dashboard
cd /tmp/integration-test
shannon do "test merged feature" --dashboard

# 4. Playwright verification
# Use playwright-skill to verify feature in dashboard

# 5. If any issues:
# - Document in blockers.md
# - Rollback merge if critical
# - Notify agent to fix
```

### SITREP Monitoring

**Agent SITREP Format** (Every 30 Minutes):
```
SITREP: Agent 1 - Multi-File Generation
Time: 14:30:00
Status: IN_PROGRESS
Phase: Backend Unit Tests (Gate 1/4)
Progress: 4/6 backend criteria PASS
Blockers: None
Next: Complete backend validation, move to CLI integration
ETA: 1 hour to Gate 1 complete
```

**Your Response**:
- Acknowledge SITREP (optional, via Serena)
- Take action if blocker reported
- Plan merge if gate completion imminent

---

## Batch 1: Validation Streaming (Solo)

**Priority**: CRITICAL (enables validation of all waves)
**Duration**: 2-3 hours
**Why First**: Cannot validate any other feature without seeing test output
**Why Solo**: Everything depends on this working
**Branch**: `batch1-validation`

### Implementation Overview

**Goal**: Stream pytest output line-by-line to dashboard Validation panel

**Backend Changes**:
- File: `src/shannon/executor/validator.py`
- Modify `_run_check()` to stream output
- Emit `validation:output` event per line

**Frontend Changes**:
- File: `dashboard/src/store/dashboardStore.ts`
- Add `validationOutput` state
- Handle `validation:output` events

- File: `dashboard/src/panels/Validation.tsx`
- Render streaming output
- Auto-scroll to bottom
- Highlight PASSED (green) and FAILED (red)

### Detailed Implementation Steps

#### Step 1: Backend - Streaming Output Emission

**File**: `src/shannon/executor/validator.py`

**Current Code** (synchronous):
```python
async def _run_check(self, command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
```

**New Code** (streaming):
```python
async def _run_check(self, command: str):
    """Run validation check with line-by-line streaming"""
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Stream stdout line by line
    async for line in process.stdout:
        line_text = line.decode().strip()

        # Emit to dashboard immediately
        if self.dashboard_client:
            await self.dashboard_client.emit_event('validation:output', {
                'line': line_text,
                'type': 'stdout',
                'timestamp': time.time(),
                'test_status': self._detect_test_status(line_text)  # 'running', 'passed', 'failed'
            })

    # Wait for completion
    await process.wait()
    return process.returncode

def _detect_test_status(self, line: str) -> str:
    """Detect test status from pytest output"""
    if 'PASSED' in line:
        return 'passed'
    elif 'FAILED' in line:
        return 'failed'
    elif 'test_' in line and '::' in line:
        return 'running'
    else:
        return 'output'
```

**Test This**:
```python
# tests/executor/test_validator_streaming.py
@pytest.mark.asyncio
async def test_output_streams_line_by_line():
    """Verify each line emits event immediately"""
    validator = ValidationOrchestrator()
    events = []

    async def capture_event(event_type, data):
        events.append(data)

    validator.dashboard_client.emit_event = capture_event

    # Run simple test
    await validator._run_check("pytest tests/sample/test_simple.py -v")

    # Verify: Multiple events (one per line)
    assert len(events) > 5
    # Verify: Each has 'line' field
    assert all('line' in e for e in events)
```

#### Step 2: Frontend - Store State Management

**File**: `dashboard/src/store/dashboardStore.ts`

**Add State**:
```typescript
interface ValidationLine {
  line: string;
  type: 'stdout' | 'stderr';
  timestamp: number;
  test_status: 'running' | 'passed' | 'failed' | 'output';
}

// In store interface
validationOutput: ValidationLine[];
validationInProgress: boolean;
```

**Add Event Handler**:
```typescript
case 'validation:started':
  set({
    validationInProgress: true,
    validationOutput: [] // Clear previous
  });
  break;

case 'validation:output':
  if (data.data) {
    set((state) => ({
      validationOutput: [...state.validationOutput, {
        line: data.data.line,
        type: data.data.type,
        timestamp: data.data.timestamp,
        test_status: data.data.test_status
      }]
    }));
  }
  break;

case 'validation:completed':
  set({ validationInProgress: false });
  break;
```

#### Step 3: Frontend - Validation Panel Component

**File**: `dashboard/src/panels/Validation.tsx`

**Implementation**:
```typescript
export function Validation() {
  const output = useDashboardStore((state) => state.validationOutput);
  const inProgress = useDashboardStore((state) => state.validationInProgress);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new output arrives
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [output]);

  if (output.length === 0 && !inProgress) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        No validation output yet
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-2 border-b flex items-center justify-between">
        <h2 className="font-semibold">Validation Output</h2>
        {inProgress && (
          <span className="text-sm text-blue-500">Running...</span>
        )}
      </div>

      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto p-2 bg-gray-950 font-mono text-sm"
      >
        {output.map((line, i) => (
          <div
            key={i}
            className={`
              ${line.test_status === 'passed' ? 'text-green-500' : ''}
              ${line.test_status === 'failed' ? 'text-red-500' : ''}
              ${line.test_status === 'running' ? 'text-yellow-500' : ''}
              ${line.test_status === 'output' ? 'text-gray-300' : ''}
            `}
          >
            {line.line}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Validation Gates (4 Gates - WORK UNTIL ALL PASS)

#### GATE 1: Backend Unit Tests (6 criteria)

**Cannot proceed to Gate 2 until:**

1. [ ] `pytest tests/executor/test_validator_streaming.py::test_output_streams_line_by_line` - PASS
2. [ ] `pytest tests/executor/test_validator_streaming.py::test_event_emission_per_line` - PASS
3. [ ] `pytest tests/executor/test_validator_streaming.py::test_failure_detection` - PASS
4. [ ] Event payload contains: `line`, `type`, `timestamp`, `test_status` keys
5. [ ] `_detect_test_status()` correctly identifies: 'passed', 'failed', 'running'
6. [ ] `pytest` (all tests): Shows "224 passed" (was 221, added 3 for streaming)

**Evidence**: Terminal output showing all tests passing

**If <6 pass**: Debug → Fix → Re-run Gate 1 → Repeat until 6/6

---

#### GATE 2: CLI Integration (5 criteria)

**Prerequisites**: Gate 1 complete (6/6)

**Cannot proceed to Gate 3 until:**

1. [ ] Create test project: `cd /tmp/batch1-test && git init && echo "__pycache__/" > .gitignore`
2. [ ] Create test file with 5 tests (3 pass, 2 fail): `touch test_sample.py`
3. [ ] Run: `shannon do "run tests" --dashboard`
4. [ ] Terminal shows line-by-line streaming output (not batched)
5. [ ] Terminal shows: `test_example_1 PASSED` (green in terminal)
6. [ ] Terminal shows: `test_example_4 FAILED` (red in terminal)
7. [ ] Exit code: `echo $?` returns 1 (tests failed)

**Evidence**: Terminal log saved to `batch1_cli_validation.log`

**If <7 pass**: Debug → Fix → Re-run Gate 2 → Repeat

---

#### GATE 3: Dashboard Validation (15 criteria - Playwright)

**Prerequisites**: Gate 2 complete (7/7)

**Cannot proceed to Gate 4 until:**

1. [ ] Start dashboard: `cd dashboard && npm run dev` (http://localhost:5175)
2. [ ] Start backend with dashboard: `shannon do "run tests" --dashboard`
3. [ ] `playwright.navigate("http://localhost:5175")`
4. [ ] `playwright.wait_for("text=Connected", timeout=5000)` - WebSocket connected
5. [ ] `playwright.click("text=Validation")` - Select Validation panel
6. [ ] `playwright.wait_for("text=test_", timeout=10000)` - First test line appears
7. [ ] Line count check:
   ```typescript
   const lineCount = await playwright.evaluate(() => {
     return document.querySelectorAll('.font-mono > div').length;
   });
   ```
8. [ ] `lineCount > 15` - Multiple test lines visible (not 1 or 2)
9. [ ] Green line check:
   ```typescript
   const greenLine = await playwright.evaluate(() => {
     return document.querySelector('.text-green-500') !== null;
   });
   ```
10. [ ] `greenLine === true` - PASSED line is green
11. [ ] Red line check:
    ```typescript
    const redLine = await playwright.evaluate(() => {
      return document.querySelector('.text-red-500') !== null;
    });
    ```
12. [ ] `redLine === true` - FAILED line is red
13. [ ] Auto-scroll verification: Last line visible in viewport (not scrolled to top)
14. [ ] `playwright.screenshot("batch1-validation-streaming-working.png")`
15. [ ] Screenshot file exists and size > 10KB (not blank)

**Evidence**:
- `batch1-validation-streaming-working.png` showing green/red lines
- Playwright test script saved to `batch1_playwright_validation.ts`

**If <15 pass**: Debug → Fix → Re-run Gate 3 → Repeat

---

#### GATE 4: Performance & Regression (6 criteria)

**Prerequisites**: Gate 3 complete (15/15)

**Cannot proceed to Wave 1 until:**

1. [ ] Latency test: Backend emits line → Line appears in UI within 200ms
   - Measure: Backend timestamp in event vs. DOM timestamp
   - Method: Add `data-timestamp` attribute to line divs, compare
2. [ ] Load test: Stream 100 lines rapidly → UI doesn't freeze
   - Run: pytest with 100 tests
   - Verify: Dashboard remains responsive, can click other panels
3. [ ] Regression: `shannon exec "calc.py"` still works (V3.5 not broken)
4. [ ] Regression: Dashboard connection still works (WebSocket not broken)
5. [ ] Regression: All existing tests pass
   ```bash
   pytest -v --tb=short
   # Expected: All 224 tests PASS
   ```
6. [ ] Branch ready: All changes committed to `batch1-validation` branch

**Evidence**:
- Latency measurement log: `batch1_latency_test.log`
- Regression test output: `batch1_regression.log`

**If <6 pass**: Debug → Fix → Re-run Gate 4 → Repeat

---

### Batch 1 Completion Criteria

**TOTAL GATES**: 4
**TOTAL CRITERIA**: 32 (6 + 7 + 15 + 6)

**BATCH 1 COMPLETE** when:
- ✅ Gate 1: 6/6 pass (Backend unit tests)
- ✅ Gate 2: 7/7 pass (CLI integration)
- ✅ Gate 3: 15/15 pass (Dashboard Playwright)
- ✅ Gate 4: 6/6 pass (Performance & regression)

**Result**: 32/32 criteria pass → Validation Streaming PROVEN WORKING

**Evidence Bundle**:
1. `batch1-validation-streaming-working.png`
2. `batch1_cli_validation.log`
3. `batch1_playwright_validation.ts`
4. `batch1_latency_test.log`
5. `batch1_regression.log`

**Git Commit**:
```bash
git add .
git commit -m "VALIDATED: Batch 1 - Validation Streaming - 32/32 criteria PASS

Gates:
- Gate 1: Backend unit tests (6/6)
- Gate 2: CLI integration (7/7)
- Gate 3: Dashboard Playwright (15/15)
- Gate 4: Performance & regression (6/6)

Evidence:
- Screenshot: batch1-validation-streaming-working.png
- Logs: batch1_cli_validation.log, batch1_regression.log
- Latency: <200ms verified

Validation streaming: PROVEN WORKING ✅
Ready for Wave 1 agent dispatch
"
```

**Serena Memory Update**:
```python
serena.write_memory("test-results.md", """
## Batch 1: Validation Streaming
- Status: COMPLETED
- Criteria: 32/32 PASS
- Gates: 4/4 COMPLETE
- Evidence: batch1-validation-streaming-working.png
- Timestamp: {timestamp}
- Branch: batch1-validation
- Merge Status: READY
""")
```

---

## Wave 1: Core Features (6 Agents)

**Duration**: 4 hours wall time (13 hours if sequential)
**Agents**: 6 executing simultaneously using `dispatching-parallel-agents` skill
**Prerequisites**: Batch 1 complete (32/32 criteria)
**Coordination**: Serena MCP memories
**Branches**: agent1-multifile, agent2-pool, agent3-decisions, agent4-research, agent5-ultrathink, agent6-controls

### Wave 1 Agent Dispatch Protocol

**Step 1: Orchestrator Preparation**

```bash
# 1. Verify Batch 1 merged
git log -1 --oneline
# Should show: "VALIDATED: Batch 1 - Validation Streaming..."

# 2. Create agent branches
git checkout -b agent1-multifile && git push -u origin agent1-multifile
git checkout master && git checkout -b agent2-pool && git push -u origin agent2-pool
git checkout master && git checkout -b agent3-decisions && git push -u origin agent3-decisions
git checkout master && git checkout -b agent4-research && git push -u origin agent4-research
git checkout master && git checkout -b agent5-ultrathink && git push -u origin agent5-ultrathink
git checkout master && git checkout -b agent6-controls && git push -u origin agent6-controls

# 3. Initialize Serena memories
serena.write_memory("agent-status.md", """
# Wave 1 Agent Status

## Agent 1: Multi-File
- Status: NOT_STARTED
- Branch: agent1-multifile

## Agent 2: Agent Pool
- Status: WAITING_ON_DEPENDENCY (Agent 1)
- Branch: agent2-pool

## Agent 3: Decisions
- Status: NOT_STARTED
- Branch: agent3-decisions

## Agent 4: Research
- Status: NOT_STARTED
- Branch: agent4-research

## Agent 5: Ultrathink
- Status: NOT_STARTED
- Branch: agent5-ultrathink

## Agent 6: Basic Controls
- Status: NOT_STARTED
- Branch: agent6-controls
""")
```

**Step 2: Invoke Dispatching Skill**

Use the `dispatching-parallel-agents` skill to spawn all 6 agents simultaneously:

```
Invoke skill: dispatching-parallel-agents

Provide the following 6 agent mission briefs (detailed in sections below):
1. Agent 1: Multi-File Generation Mission Brief
2. Agent 2: Agent Pool Mission Brief
3. Agent 3: Decision Engine Mission Brief
4. Agent 4: Research Orchestration Mission Brief
5. Agent 5: Ultrathink Engine Mission Brief
6. Agent 6: Basic Controls Mission Brief
```

**Step 3: Monitor Progress**

Every 30 minutes:
```python
# Read agent statuses
status = serena.read_memory("agent-status.md")
print(status)

# Read blockers
blockers = serena.read_memory("blockers.md")
if blockers:
    print("BLOCKERS DETECTED:")
    print(blockers)
    # Take action

# Read test results
results = serena.read_memory("test-results.md")
print("Completed Gates:")
print(results)
```

---

## AGENT 1: Multi-File Generation - Complete Mission Brief

**Branch**: `agent1-multifile`
**Priority**: CRITICAL (user called out explicitly)
**Duration**: 3-4 hours
**Dependencies**: Batch 1 (validation streaming)
**Coordination**: Serena MCP for status updates

### Mission Statement

**Goal**: Enable `shannon do` to create ALL files in multi-file requests (currently creates only 1 of N)

**Success Criteria**: 26/26 validation criteria pass across 4 internal gates

**Skills to Invoke**:
- `test-driven-development` (write tests FIRST, see them fail, then implement)
- `sitrep-reporting` (report status every 30 minutes)
- `verification-before-completion` (validate before claiming done)

### Architecture Overview

**Problem**: `CompleteExecutor.execute_autonomous()` designed for single file, doesn't iterate

**Solution**: New multi-file pipeline

```
User: "create auth: tokens.py, middleware.py, __init__.py"
           │
           ▼
    MultiFileParser
    ┌─────────────────┐
    │ is_multi_file() │──No──▶ CompleteExecutor (single file)
    │ parse()         │
    └────────┬────────┘
             │ Yes
             ▼
    MultiFileExecutor
    ┌─────────────────┐
    │ For each file:  │
    │  1. Create task │
    │  2. Execute     │
    │  3. Emit event  │
    │  4. Continue    │
    └─────────────────┘
             │
             ▼
    All files created ✅
```

### Files You Will Create/Modify

**New Files**:
1. `src/shannon/orchestration/multi_file_parser.py` - Pattern detection and parsing
2. `src/shannon/executor/multi_file_executor.py` - Multi-file execution logic
3. `tests/orchestration/test_multi_file_parser.py` - Parser tests
4. `tests/executor/test_multi_file_executor.py` - Executor tests

**Modified Files**:
1. `src/shannon/cli/v4_commands/do.py` - Integration point

**File Ownership**: All files exclusively yours (no conflicts expected)

### Implementation Plan (TDD - Tests First!)

#### Phase 1: Backend - Parser (Gate 1/4)

**Step 1.1: Create Test File FIRST**

**File**: `tests/orchestration/test_multi_file_parser.py`

```python
"""
Tests for multi-file task parsing

These tests define the behavior BEFORE implementation.
Run them and watch them FAIL, then implement until PASS.
"""
import pytest
from shannon.orchestration.multi_file_parser import MultiFileParser, MultiFileRequest

class TestMultiFileDetection:
    """Test is_multi_file() pattern detection"""

    def test_single_file_not_detected(self):
        """Single file request returns False"""
        parser = MultiFileParser()

        # Test cases that should NOT be multi-file
        assert not parser.is_multi_file("create hello.py")
        assert not parser.is_multi_file("build calculator app")
        assert not parser.is_multi_file("fix bug in auth.py")

    def test_multi_file_detected_colon_pattern(self):
        """Pattern: 'create X: file1, file2' detected"""
        parser = MultiFileParser()

        assert parser.is_multi_file("create auth: tokens.py, middleware.py")
        assert parser.is_multi_file("create utils: math.py, string.py, file.py")

    def test_multi_file_detected_with_pattern(self):
        """Pattern: 'with file1 and file2' detected"""
        parser = MultiFileParser()

        assert parser.is_multi_file("implement auth with tokens.py and middleware.py")

    def test_multi_file_detected_comma_separated(self):
        """Pattern: 'file1.py, file2.py' detected"""
        parser = MultiFileParser()

        assert parser.is_multi_file("create a.py, b.py, c.py")


class TestMultiFileParsing:
    """Test parse() file extraction"""

    def test_parse_extracts_file_list(self):
        """Parse extracts all file paths"""
        parser = MultiFileParser()

        result = parser.parse("create auth: tokens.py, middleware.py, __init__.py")

        assert result is not None
        assert isinstance(result, MultiFileRequest)
        assert len(result.files) == 3
        assert "tokens.py" in result.files[0]
        assert "middleware.py" in result.files[1]
        assert "__init__.py" in result.files[2]

    def test_parse_extracts_base_task(self):
        """Parse extracts base task description"""
        parser = MultiFileParser()

        result = parser.parse("create auth module: tokens.py, middleware.py")

        assert result.base_task == "create auth module"

    def test_parse_handles_mixed_directories(self):
        """Parse handles files in different directories"""
        parser = MultiFileParser()

        result = parser.parse("create dir1/a.py, dir2/b.py, c.py")

        assert len(result.files) == 3
        assert "dir1/a.py" in result.files[0]
        assert "dir2/b.py" in result.files[1]
        assert "c.py" in result.files[2]

    def test_parse_single_file_returns_none(self):
        """Single file request returns None"""
        parser = MultiFileParser()

        result = parser.parse("create hello.py")

        assert result is None
```

**Run Tests (they will FAIL)**:
```bash
pytest tests/orchestration/test_multi_file_parser.py -v
# Expected: All tests FAIL (classes don't exist yet)
```

**Step 1.2: Implement MultiFileParser**

**File**: `src/shannon/orchestration/multi_file_parser.py`

```python
"""
Multi-File Task Parser

Detects and parses natural language requests for multiple file creation.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict
import re


@dataclass
class MultiFileRequest:
    """Represents a multi-file creation request"""
    base_task: str  # "create auth module"
    files: List[str]  # ["auth/tokens.py", "auth/middleware.py", ...]
    descriptions: Dict[str, str]  # {"tokens.py": "JWT generation", ...}


class MultiFileParser:
    """
    Parse multi-file requests from natural language

    Detected Patterns:
    1. "create X: file1, file2, file3"
    2. "implement Y with file1 and file2"
    3. "file1.py, file2.py, file3.py"
    4. "dir1/file1.py, dir2/file2.py"
    """

    # Patterns that indicate multi-file request
    MULTI_FILE_PATTERNS = [
        r':\s*\w+\.py\s*,\s*\w+\.py',  # "create: file1.py, file2.py"
        r'with\s+\w+\.py\s+and\s+\w+\.py',  # "with file1.py and file2.py"
        r'\w+/\w+\.py,?\s+\w+/\w+\.py',  # "dir/file1.py, dir/file2.py"
        r'\w+\.py,\s*\w+\.py',  # "file1.py, file2.py"
    ]

    def is_multi_file(self, task: str) -> bool:
        """
        Quick check if task appears to request multiple files

        Args:
            task: Natural language task description

        Returns:
            True if multiple files detected, False otherwise
        """
        return any(re.search(pattern, task) for pattern in self.MULTI_FILE_PATTERNS)

    def parse(self, task: str) -> Optional[MultiFileRequest]:
        """
        Parse task to extract file list

        Args:
            task: Natural language task description

        Returns:
            MultiFileRequest if multi-file detected, None otherwise
        """
        if not self.is_multi_file(task):
            return None

        # Extract base task (text before colon or "with")
        base_task = task
        if ':' in task:
            base_task = task.split(':')[0].strip()
        elif ' with ' in task.lower():
            base_task = task.split(' with ')[0].strip()

        # Extract file list
        files = self._extract_files(task)

        if not files:
            return None

        # Extract per-file descriptions (if present)
        descriptions = self._extract_descriptions(task, files)

        return MultiFileRequest(
            base_task=base_task,
            files=files,
            descriptions=descriptions
        )

    def _extract_files(self, task: str) -> List[str]:
        """Extract file paths from task"""
        # Pattern: Find all .py files (with or without directory prefix)
        file_pattern = r'[\w/]+\.py'
        files = re.findall(file_pattern, task)

        return files

    def _extract_descriptions(self, task: str, files: List[str]) -> Dict[str, str]:
        """Extract per-file descriptions if present"""
        descriptions = {}

        # Pattern: "file.py for description" or "file.py with description"
        for file in files:
            # Look for description after file name
            pattern = rf'{file}\s+(for|with)\s+([\w\s]+?)(?:,|$|\.|;)'
            match = re.search(pattern, task)
            if match:
                descriptions[file] = match.group(2).strip()

        return descriptions
```

**Run Tests Again (they should PASS now)**:
```bash
pytest tests/orchestration/test_multi_file_parser.py -v
# Expected: All 8 tests PASS
```

**Step 1.3: Report to Serena**

```python
serena.write_memory("agent-status.md", f"""
## Agent 1: Multi-File
- Status: GATE_1_IN_PROGRESS
- Phase: Backend Parser Implementation
- Last Updated: {timestamp}
- Progress: 8/26 criteria (8 parser tests passing)
- Blockers: None
- ETA: 2.5 hours remaining
- Branch: agent1-multifile
""")
```

**GATE 1 VALIDATION** (Must PASS before continuing):

1. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_single_file_not_detected` - PASS
2. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_multi_file_detected_colon_pattern` - PASS
3. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_multi_file_detected_with_pattern` - PASS
4. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_multi_file_detected_comma_separated` - PASS
5. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_parse_extracts_file_list` - PASS
6. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_parse_extracts_base_task` - PASS
7. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_parse_handles_mixed_directories` - PASS
8. [ ] `pytest tests/orchestration/test_multi_file_parser.py::test_parse_single_file_returns_none` - PASS

**IF ALL 8 PASS**: Proceed to Phase 2
**IF ANY FAIL**: Debug → Fix → Re-run Gate 1

---

#### Phase 2: Backend - Executor (Gate 2/4)

**Step 2.1: Create Executor Test FIRST**

**File**: `tests/executor/test_multi_file_executor.py`

```python
"""
Tests for multi-file execution

Write tests FIRST, watch them FAIL, then implement.
"""
import pytest
from pathlib import Path
from shannon.executor.multi_file_executor import MultiFileExecutor


class TestMultiFileExecution:
    """Test multi-file creation end-to-end"""

    @pytest.mark.asyncio
    async def test_creates_all_three_files(self, tmp_path):
        """Execute multi-file request and verify all files created"""
        executor = MultiFileExecutor(tmp_path)

        result = await executor.execute(
            "create utils: math.py for math functions, string.py for string utils, file.py for file operations"
        )

        # Verify result
        assert result.success
        assert result.files_created == 3
        assert result.files_total == 3

        # Verify files exist
        assert (tmp_path / "utils" / "math.py").exists()
        assert (tmp_path / "utils" / "string.py").exists()
        assert (tmp_path / "utils" / "file.py").exists()

    @pytest.mark.asyncio
    async def test_single_file_delegates_to_complete_executor(self, tmp_path):
        """Single file request uses CompleteExecutor"""
        executor = MultiFileExecutor(tmp_path)

        result = await executor.execute("create hello.py")

        assert result.success
        assert (tmp_path / "hello.py").exists()

    @pytest.mark.asyncio
    async def test_emits_file_created_events(self, tmp_path, mock_dashboard):
        """Emits file:created event for each file"""
        executor = MultiFileExecutor(tmp_path)
        events = []

        async def capture_event(event_type, data):
            events.append((event_type, data))

        mock_dashboard.emit_event = capture_event
        executor.dashboard_client = mock_dashboard

        await executor.execute("create a.py, b.py, c.py")

        # Verify 3 file:created events
        file_events = [e for e in events if e[0] == 'file:created']
        assert len(file_events) == 3

        # Verify event data
        assert file_events[0][1]['file_path'] == 'a.py'
        assert file_events[1][1]['file_path'] == 'b.py'
        assert file_events[2][1]['file_path'] == 'c.py'

    @pytest.mark.asyncio
    async def test_mixed_directories(self, tmp_path):
        """Files in different directories all created"""
        executor = MultiFileExecutor(tmp_path)

        result = await executor.execute("create dir1/a.py, dir2/b.py, c.py")

        assert result.success
        assert (tmp_path / "dir1" / "a.py").exists()
        assert (tmp_path / "dir2" / "b.py").exists()
        assert (tmp_path / "c.py").exists()
```

**Run Tests (will FAIL)**:
```bash
pytest tests/executor/test_multi_file_executor.py -v
# Expected: All tests FAIL (MultiFileExecutor doesn't exist)
```

**Step 2.2: Implement MultiFileExecutor**

**File**: `src/shannon/executor/multi_file_executor.py`

```python
"""
Multi-File Executor

Handles creation/modification of multiple files in a single task.
"""
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

from shannon.executor.complete_executor import CompleteExecutor
from shannon.orchestration.multi_file_parser import MultiFileParser, MultiFileRequest
from shannon.server.dashboard_client import DashboardEventClient


@dataclass
class MultiFileResult:
    """Result of multi-file execution"""
    success: bool
    files_created: int
    files_total: int
    results: List[any]  # Individual file results


class MultiFileExecutor:
    """
    Execute multi-file creation/modification tasks

    Strategy:
    1. Parse task to extract file list
    2. For each file:
       a. Create sub-task ("create file1.py for JWT generation")
       b. Execute with CompleteExecutor
       c. Validate file created
       d. Emit file:created event to dashboard
       e. Continue to next file
    3. All files created → success
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.parser = MultiFileParser()
        self.executor = CompleteExecutor(project_root)

    async def execute(
        self,
        task: str,
        dashboard_client: Optional[DashboardEventClient] = None
    ) -> MultiFileResult:
        """
        Execute multi-file task

        Args:
            task: Natural language task description
            dashboard_client: Optional dashboard client for events

        Returns:
            MultiFileResult with list of created files
        """
        # 1. Parse task
        request = self.parser.parse(task)

        if not request:
            # Single file - delegate to CompleteExecutor
            result = await self.executor.execute_autonomous(task)
            return MultiFileResult(
                success=result.success,
                files_created=1 if result.success else 0,
                files_total=1,
                results=[result]
            )

        # 2. Execute each file
        results = []
        for i, file_path in enumerate(request.files):
            # Create sub-task for this file
            file_desc = request.descriptions.get(file_path, "")
            sub_task = f"create {file_path}"
            if file_desc:
                sub_task += f" for {file_desc}"

            # Execute with CompleteExecutor
            result = await self.executor.execute_autonomous(
                task=sub_task,
                auto_commit=False  # We'll commit all together at end
            )

            if result.success:
                # Emit file:created event
                if dashboard_client:
                    content = Path(self.project_root / file_path).read_text() if Path(self.project_root / file_path).exists() else ""

                    await dashboard_client.emit_event('file:created', {
                        'file_path': file_path,
                        'index': i,
                        'total': len(request.files),
                        'content_preview': content[:500]  # First 500 chars
                    })

                results.append(result)
            else:
                # File creation failed - stop and report partial results
                break

        # 3. Commit all files together
        if results:
            await self._commit_multi_file(results, request.base_task)

        return MultiFileResult(
            success=len(results) == len(request.files),
            files_created=len(results),
            files_total=len(request.files),
            results=results
        )

    async def _commit_multi_file(self, results, base_task):
        """Commit all files together"""
        # TODO: Implement git commit for all files
        # For now, CompleteExecutor handles individual commits
        pass
```

**Run Tests (should PASS now)**:
```bash
pytest tests/executor/test_multi_file_executor.py -v
# Expected: All 4 tests PASS
```

**Step 2.3: Report Gate 2**

```python
serena.write_memory("agent-status.md", f"""
## Agent 1: Multi-File
- Status: GATE_2_COMPLETE
- Phase: Backend Executor Complete
- Last Updated: {timestamp}
- Progress: 12/26 criteria (parser + executor tests passing)
- Blockers: None
- ETA: 1.5 hours remaining
- Branch: agent1-multifile
- Next: CLI Integration (Gate 3)
""")

serena.write_memory("test-results.md", f"""
## Agent 1: Multi-File - Gate 2
- Status: COMPLETE
- Parser Tests: 8/8 PASS
- Executor Tests: 4/4 PASS
- Total Backend: 12/12 PASS
- Timestamp: {timestamp}
- Next Gate: CLI Integration
""")
```

**GATE 2 VALIDATION**:

1. [ ] All Gate 1 criteria still pass (8/8)
2. [ ] `pytest tests/executor/test_multi_file_executor.py::test_creates_all_three_files` - PASS
3. [ ] `pytest tests/executor/test_multi_file_executor.py::test_single_file_delegates_to_complete_executor` - PASS
4. [ ] `pytest tests/executor/test_multi_file_executor.py::test_emits_file_created_events` - PASS
5. [ ] `pytest tests/executor/test_multi_file_executor.py::test_mixed_directories` - PASS

**IF ALL 13 PASS** (8 from Gate 1 + 5 from Gate 2): Proceed to Phase 3
**IF ANY FAIL**: Debug → Fix → Re-run Gate 2

---

#### Phase 3: Integration (Gate 3/4)

**Step 3.1: Integrate with shannon do Command**

**File**: `src/shannon/cli/v4_commands/do.py`

**Add Imports**:
```python
from shannon.orchestration.multi_file_parser import MultiFileParser
from shannon.executor.multi_file_executor import MultiFileExecutor
```

**Modify do() Command** (find the execution section):
```python
async def do(task: str, dashboard: bool = False):
    """Execute task using autonomous agent"""

    # ... existing setup code ...

    # NEW: Detect multi-file requests
    parser = MultiFileParser()
    is_multi_file = parser.is_multi_file(task)

    if is_multi_file:
        console.print("[yellow]Multi-file request detected[/yellow]")

        # Use MultiFileExecutor
        executor = MultiFileExecutor(project_root)
        result = await executor.execute(task, dashboard_client)

        if result.success:
            console.print(f"[green]✓ Created {result.files_created} files successfully[/green]")
            sys.exit(0)
        else:
            console.print(f"[red]✗ Created {result.files_created}/{result.files_total} files[/red]")
            sys.exit(1)
    else:
        # Existing single-file flow
        # ... existing code ...
```

**Step 3.2: Test via CLI**

```bash
# Test 1: Multi-file creation
cd /tmp/agent1-cli-test
rm -rf * .git .shannon*
git init
echo "__pycache__/" > .gitignore

shannon do "create auth: tokens.py, middleware.py, __init__.py"

# Verify
ls auth/
# Expected: tokens.py, middleware.py, __init__.py all exist

# Test 2: Single file still works
shannon do "create hello.py"

# Verify
ls hello.py
# Expected: hello.py exists
```

**Step 3.3: Test with Dashboard**

```bash
# Terminal 1: Start dashboard
cd dashboard && npm run dev

# Terminal 2: Run multi-file with dashboard
cd /tmp/agent1-dashboard-test
shannon do "create utils: math.py, string.py, file.py" --dashboard
```

**Step 3.4: Report Gate 3**

```python
serena.write_memory("agent-status.md", f"""
## Agent 1: Multi-File
- Status: GATE_3_IN_PROGRESS
- Phase: CLI Integration Testing
- Last Updated: {timestamp}
- Progress: 17/26 criteria (backend + CLI tests)
- Blockers: None
- ETA: 1 hour remaining
- Branch: agent1-multifile
- Next: Dashboard Validation (Gate 4)
""")
```

**GATE 3 VALIDATION**:

1. [ ] `cd /tmp/gate3-test && git init`
2. [ ] `shannon do "create auth: tokens.py, middleware.py, __init__.py"`
3. [ ] Exit code: `echo $?` returns 0
4. [ ] File exists: `[ -f auth/tokens.py ] && echo PASS` → "PASS"
5. [ ] File exists: `[ -f auth/middleware.py ] && echo PASS` → "PASS"
6. [ ] File exists: `[ -f auth/__init__.py ] && echo PASS` → "PASS"
7. [ ] Content check: `wc -l auth/tokens.py` returns > 10
8. [ ] Content check: `grep -c "def\|class" auth/tokens.py` returns >= 1
9. [ ] Git check: `git log -1 --name-only | grep -c "auth/"` returns 3
10. [ ] Mixed dirs test: `shannon do "create dir1/a.py, dir2/b.py, c.py"`
11. [ ] All 3 files created in correct directories
12. [ ] Regression: `shannon do "single.py"` still creates 1 file

**IF ALL 25 PASS** (13 backend + 12 CLI): Proceed to Phase 4
**IF ANY FAIL**: Debug → Fix → Re-run Gate 3

---

#### Phase 4: Dashboard Validation (Gate 4/4 - FINAL)

**Step 4.1: Playwright Verification**

**Create Test Script**: `batch1_agent1_playwright.ts`

```typescript
import { test, expect } from '@playwright/test';

test('Multi-file events flow to dashboard', async ({ page }) => {
  // 1. Navigate to dashboard
  await page.goto('http://localhost:5175');

  // 2. Wait for WebSocket connection
  await expect(page.locator('text=Connected')).toBeVisible({ timeout: 5000 });

  // 3. Run multi-file command in background
  // (In real scenario, run `shannon do` in separate terminal)

  // 4. Wait for file:created events
  await page.waitForTimeout(10000);  // Give time for execution

  // 5. Check event stream
  const eventItems = page.locator('[data-testid="event-item"]');
  const count = await eventItems.count();

  expect(count).toBeGreaterThanOrEqual(5);  // execution:started + 3 file:created + execution:completed

  // 6. Screenshot evidence
  await page.screenshot({ path: 'batch1-agent1-multi-file-validated.png' });
});
```

**Run Playwright Test**:
```bash
# Terminal 1: Dashboard running
cd dashboard && npm run dev

# Terminal 2: Execute multi-file task
cd /tmp/playwright-test
shannon do "create a.py, b.py, c.py" --dashboard

# Terminal 3: Run Playwright
playwright test batch1_agent1_playwright.ts
```

**Step 4.2: Final Validation & Evidence**

**GATE 4 VALIDATION** (FINAL):

1. [ ] `playwright.navigate("http://localhost:5175")`
2. [ ] `playwright.wait_for("text=Connected", timeout=5000)` - PASS
3. [ ] Event count: `document.querySelectorAll('[data-testid="event-item"]').length >= 5`
4. [ ] File events present (3× file:created)
5. [ ] `playwright.screenshot("batch1-agent1-multi-file-validated.png")`
6. [ ] Screenshot file > 10KB
7. [ ] Regression: All existing tests still pass
   ```bash
   pytest -v
   # Expected: 226 tests pass (221 original + 5 new)
   ```

**IF ALL 26 PASS**: Agent 1 COMPLETE
**IF ANY FAIL**: Debug → Fix → Re-run Gate 4

---

### Agent 1 Completion Protocol

**When all 26/26 criteria pass:**

**Step 1: Final Serena Update**
```python
serena.write_memory("agent-status.md", f"""
## Agent 1: Multi-File
- Status: COMPLETE
- All Gates: 4/4 COMPLETE
- Total Criteria: 26/26 PASS
- Branch: agent1-multifile
- Evidence: batch1-agent1-multi-file-validated.png
- Timestamp: {timestamp}
- Ready for Merge: YES
""")

serena.write_memory("test-results.md", f"""
## Agent 1: Multi-File - FINAL
- Status: COMPLETE
- Gate 1: Backend Parser (8/8)
- Gate 2: Backend Executor (5/5)
- Gate 3: CLI Integration (12/12)
- Gate 4: Dashboard Validation (6/6)
- Total: 26/26 PASS
- Evidence: batch1-agent1-multi-file-validated.png
- Branch: agent1-multifile
- Merge Status: READY
""")
```

**Step 2: Git Commit**
```bash
git add .
git commit -m "Agent 1 COMPLETE: Multi-File Generation - 26/26 validated

GATES COMPLETED:
- Gate 1: Backend Parser (8/8 tests)
- Gate 2: Backend Executor (5/5 tests)
- Gate 3: CLI Integration (12/12 criteria)
- Gate 4: Dashboard Validation (6/6 Playwright)

IMPLEMENTATION:
- MultiFileParser: Pattern detection working
- MultiFileExecutor: Creates all files correctly
- Integration: shannon do multi-file functional

EVIDENCE:
- Tests: 226 passing (added 13 new)
- Screenshot: batch1-agent1-multi-file-validated.png
- Playwright: Validated event flow

SKILLS USED:
- test-driven-development ✅
- sitrep-reporting ✅
- verification-before-completion ✅

Ready for orchestrator merge to master
"

git push origin agent1-multifile
```

**Step 3: Final SITREP**
```
SITREP: Agent 1 - Multi-File Generation
Time: {timestamp}
Status: COMPLETE
Total Gates: 4/4
Total Criteria: 26/26 PASS
Evidence: batch1-agent1-multi-file-validated.png
Branch: agent1-multifile pushed to remote
Blockers: None
Ready for Merge: YES

Multi-file generation is PROVEN WORKING ✅
Awaiting orchestrator merge to master
```

---

### Agent 1 Serena Protocol Summary

**Before Starting**:
- Read `agent-status.md` for current state
- Read `blockers.md` for known issues
- Write initial status to `agent-status.md`

**Every 30 Minutes** (SITREP):
- Update `agent-status.md` with progress
- Report any blockers to `blockers.md`
- Continue work

**After Each Gate**:
- Update `test-results.md` with gate status
- Update `agent-status.md` with next gate
- Screenshot evidence saved

**When Complete**:
- Update `agent-status.md` to COMPLETE
- Update `test-results.md` with final results
- Final SITREP
- Wait for orchestrator merge

---

## AGENT 2: Agent Pool - Complete Mission Brief

**Branch**: `agent2-pool`
**Priority**: HIGH (user priority #2)
**Duration**: 2-3 hours
**Dependencies**: Agent 1 (multi-file needed for complex test tasks)
**Coordination**: Serena MCP for status and dependency tracking

### Mission Statement

**Goal**: Enable 8 agents to execute in parallel, visible in dashboard AgentPool panel

**Success Criteria**: 32/32 validation criteria pass across 4 internal gates

**Skills to Invoke**:
- `test-driven-development`
- `playwright-skill` (UI validation)
- `sitrep-reporting`
- `verification-before-completion`

### Architecture Overview

**Current**: Single-threaded execution only
**Target**: Up to 8 agents in parallel

```
Orchestrator receives complex task:
"analyze code, run tests, check security"
           │
           ▼
    Planner splits into 3 skill steps:
    1. code_analysis
    2. run_tests
    3. security_check
           │
           ▼
    AgentPool.spawn_agent() × 3
    ┌──────────┬──────────┬──────────┐
    │ Agent 1  │ Agent 2  │ Agent 3  │
    │ Analysis │ Testing  │ Security │
    └────┬─────┴────┬─────┴────┬─────┘
         │          │          │
         ▼          ▼          ▼
    Execute in parallel via asyncio.gather()
         │          │          │
         └──────────┴──────────┘
                   │
                   ▼
         All results combined
```

### Files You Will Create/Modify

**Modified Files**:
1. `src/shannon/orchestration/agent_pool.py` - Enhance with spawn/lifecycle
2. `src/shannon/orchestration/orchestrator.py` - Add agent execution logic (**SHARED FILE**)
3. `dashboard/src/store/dashboardStore.ts` - Add agent state (**SHARED FILE**)
4. `dashboard/src/panels/AgentPool.tsx` - Render active agents

**New Test Files**:
1. `tests/orchestration/test_agent_pool_enhanced.py`
2. `tests/orchestration/test_orchestrator_agents.py`

**Conflict Strategy**:
- `orchestrator.py`: Add new methods, don't modify existing
- `dashboardStore.ts`: Add new state vars, new event handlers
- Coordinate via Serena file locks

### Implementation Plan (4 Gates)

#### Phase 1: Backend - AgentPool Enhancement (Gate 1/4)

**Step 1.1: TDD - Write Test First**

**File**: `tests/orchestration/test_agent_pool_enhanced.py`

```python
"""
Tests for enhanced AgentPool

Write tests FIRST, watch FAIL, then implement.
"""
import pytest
from shannon.orchestration.agent_pool import AgentPool, Agent, AgentPoolFullError


class TestAgentSpawning:
    """Test spawn_agent() functionality"""

    @pytest.mark.asyncio
    async def test_spawn_single_agent(self):
        """Spawn one agent successfully"""
        pool = AgentPool(max_active=8, max_total=50)

        agent = await pool.spawn_agent(
            skill_name='code_analysis',
            parameters={'target': 'src/'},
            session_id='test-123'
        )

        # Verify agent created
        assert agent is not None
        assert agent.id is not None
        assert len(agent.id) == 36  # UUID format
        assert agent.skill_name == 'code_analysis'

        # Verify pool tracking
        assert len(pool.active_agents) == 1
        assert pool.active_agents[0] == agent

    @pytest.mark.asyncio
    async def test_capacity_limit_enforced(self):
        """Cannot exceed max_active capacity"""
        pool = AgentPool(max_active=2, max_total=10)

        # Spawn 2 agents (at capacity)
        agent1 = await pool.spawn_agent('skill1', {}, 'test')
        agent2 = await pool.spawn_agent('skill2', {}, 'test')

        # Try spawning 3rd (should fail)
        with pytest.raises(AgentPoolFullError) as exc_info:
            await pool.spawn_agent('skill3', {}, 'test')

        assert "at capacity" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_agent_role_determination(self):
        """Agents assigned correct roles based on skill"""
        pool = AgentPool(max_active=8)

        # Test different skill → role mappings
        research = await pool.spawn_agent('research_knowledge', {}, 'test')
        assert research.role == 'Research'

        analysis = await pool.spawn_agent('code_analysis', {}, 'test')
        assert analysis.role == 'Analysis'

        testing = await pool.spawn_agent('run_tests', {}, 'test')
        assert testing.role == 'Testing'
```

**Run (will FAIL)**:
```bash
pytest tests/orchestration/test_agent_pool_enhanced.py -v
# Expected: Tests fail (methods don't exist)
```

**Step 1.2: Implement AgentPool Enhancement**

**File**: `src/shannon/orchestration/agent_pool.py`

```python
"""
Agent Pool - Manages concurrent agent execution

Enhanced with spawn/lifecycle management for parallel execution.
"""
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio


class AgentPoolFullError(Exception):
    """Raised when agent pool is at capacity"""
    pass


@dataclass
class Agent:
    """Represents a spawned agent"""
    id: str
    skill_name: str
    role: str
    parameters: Dict[str, Any]
    session_id: str
    status: str = 'running'
    progress: int = 0
    duration: float = 0.0


class AgentPool:
    """
    Manages pool of concurrent agents

    Capacity:
    - max_active: 8 agents running simultaneously
    - max_total: 50 agents total across session

    Agent Types:
    - Research: Knowledge gathering
    - Analysis: Code analysis
    - Testing: Test execution
    - Validation: Validation checks
    - Git: Git operations
    - Planning: Task planning
    - Monitoring: System monitoring
    """

    def __init__(self, max_active: int = 8, max_total: int = 50):
        self.max_active = max_active
        self.max_total = max_total
        self.active_agents: List[Agent] = []
        self.all_agents: List[Agent] = []  # Historical record
        self.event_bus = None  # Set by orchestrator

    async def spawn_agent(
        self,
        skill_name: str,
        parameters: Dict[str, Any],
        session_id: str
    ) -> Agent:
        """
        Spawn new agent for skill execution

        Args:
            skill_name: Skill to execute (e.g., 'code_analysis')
            parameters: Skill parameters
            session_id: Session identifier

        Returns:
            Agent instance with unique ID

        Raises:
            AgentPoolFullError: If at max_active capacity
        """
        # Check capacity
        if len(self.active_agents) >= self.max_active:
            raise AgentPoolFullError(
                f"Cannot spawn agent - at capacity ({self.max_active} active)"
            )

        if len(self.all_agents) >= self.max_total:
            raise AgentPoolFullError(
                f"Cannot spawn agent - total capacity reached ({self.max_total})"
            )

        # Create agent
        agent = Agent(
            id=str(uuid.uuid4()),
            skill_name=skill_name,
            role=self._determine_agent_role(skill_name),
            parameters=parameters,
            session_id=session_id,
            status='running',
            progress=0
        )

        # Track agent
        self.active_agents.append(agent)
        self.all_agents.append(agent)

        # Emit event
        if self.event_bus:
            await self.event_bus.emit('agent:spawned', {
                'agent_id': agent.id,
                'skill_name': skill_name,
                'role': agent.role,
                'session_id': session_id
            })

        return agent

    def _determine_agent_role(self, skill_name: str) -> str:
        """Determine agent role from skill name"""
        role_mapping = {
            'research': 'Research',
            'code_analysis': 'Analysis',
            'analyze': 'Analysis',
            'run_tests': 'Testing',
            'test': 'Testing',
            'validate': 'Validation',
            'validation': 'Validation',
            'git': 'Git',
            'plan': 'Planning',
            'monitor': 'Monitoring',
        }

        # Match skill name against role keywords
        for keyword, role in role_mapping.items():
            if keyword in skill_name.lower():
                return role

        return 'Generic'

    async def terminate_agent(self, agent_id: str):
        """Mark agent as completed and remove from active pool"""
        agent = next((a for a in self.active_agents if a.id == agent_id), None)
        if agent:
            agent.status = 'completed'
            self.active_agents.remove(agent)
```

**Run Tests (should PASS)**:
```bash
pytest tests/orchestration/test_agent_pool_enhanced.py -v
# Expected: All 3 tests PASS
```

**Step 1.3: Report Gate 1**

```python
serena.write_memory("agent-status.md", f"""
## Agent 2: Agent Pool
- Status: GATE_1_COMPLETE
- Phase: Backend AgentPool Enhanced
- Progress: 3/32 criteria
- Blockers: None
- Next: Orchestrator Integration (Gate 2)
- Branch: agent2-pool
""")
```

**GATE 1 VALIDATION**:

1. [ ] `pytest tests/orchestration/test_agent_pool_enhanced.py::test_spawn_single_agent` - PASS
2. [ ] `pytest tests/orchestration/test_agent_pool_enhanced.py::test_capacity_limit_enforced` - PASS
3. [ ] `pytest tests/orchestration/test_agent_pool_enhanced.py::test_agent_role_determination` - PASS

**IF ALL 3 PASS**: Proceed to Phase 2
**IF ANY FAIL**: Debug → Fix → Retry Gate 1

---

#### Phase 2: Backend - Orchestrator Integration (Gate 2/4)

**Step 2.1: Acquire File Lock (Shared File)**

```python
# Check if orchestrator.py is locked
locks = serena.read_memory("file-locks.md")
if "orchestrator.py" in locks:
    # File locked by another agent, WAIT
    serena.write_memory("blockers.md", f"""
## Agent 2: Agent Pool
**Blocker**: orchestrator.py locked by another agent
**Severity**: BLOCKING
**Requested**: Wait for file release
**Status**: WAITING
**Timestamp**: {timestamp}
""")
    # Wait...
else:
    # Acquire lock
    serena.write_memory("file-locks.md", f"""
## LOCKED Files
- `src/shannon/orchestration/orchestrator.py` - LOCKED by Agent 2 ({timestamp})
""")
```

**Step 2.2: TDD - Orchestrator Agent Tests**

**File**: `tests/orchestration/test_orchestrator_agents.py`

```python
"""
Tests for orchestrator agent integration

Write FIRST, watch FAIL, then implement.
"""
import pytest
from shannon.orchestration.orchestrator import Orchestrator
from shannon.orchestration.agent_pool import Agent


class TestOrchesterAgentExecution:
    """Test agent-based execution in orchestrator"""

    @pytest.mark.asyncio
    async def test_single_agent_spawning(self):
        """Orchestrator spawns agent for parallelizable skill"""
        orchestrator = Orchestrator(session_id='test-123')

        step = SkillStep(
            skill_name='code_analysis',
            parameters={'target': 'src/'},
            parallel=True  # Indicates parallelizable
        )

        result = await orchestrator._execute_step(step, 0)

        # Verify agent spawned
        assert result.success
        assert len(orchestrator.agent_pool.active_agents) == 1
        agent = orchestrator.agent_pool.active_agents[0]
        assert agent.skill_name == 'code_analysis'

    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self):
        """Multiple agents execute in parallel"""
        orchestrator = Orchestrator(session_id='test-456')

        steps = [
            SkillStep(skill_name='code_analysis', parameters={}, parallel=True),
            SkillStep(skill_name='run_tests', parameters={}, parallel=True),
            SkillStep(skill_name='security_check', parameters={}, parallel=True),
        ]

        # Execute all in parallel
        results = await orchestrator._execute_parallel_steps(steps)

        # Verify all executed
        assert len(results) == 3
        assert all(r.success for r in results)

        # Verify agents spawned
        assert len(orchestrator.agent_pool.all_agents) == 3
```

**Run (will FAIL)**:
```bash
pytest tests/orchestration/test_orchestrator_agents.py -v
# Expected: Tests fail (methods don't exist)
```

**Step 2.3: Implement Orchestrator Agent Methods**

**File**: `src/shannon/orchestration/orchestrator.py`

**Add methods (don't modify existing)**:

```python
# ADD THESE METHODS to Orchestrator class:

async def _execute_step(self, step: SkillStep, step_index: int):
    """
    Execute single skill step with optional agent spawning

    New behavior: If step.parallel=True, spawn agent for execution
    """
    # Check if step is parallelizable
    if hasattr(step, 'parallel') and step.parallel and self.agent_pool:
        # Spawn agent for parallel execution
        agent = await self.agent_pool.spawn_agent(
            skill_name=step.skill_name,
            parameters=step.parameters,
            session_id=self.session_id
        )

        # Emit agent:spawned event
        if self.dashboard_client:
            await self.dashboard_client.emit_event('agent:spawned', {
                'agent_id': agent.id,
                'skill_name': step.skill_name,
                'role': agent.role,
                'step_index': step_index,
                'session_id': self.session_id
            })

        # Execute skill through agent
        result = await self._execute_via_agent(agent, step)

        # Emit agent:completed event
        if self.dashboard_client:
            await self.dashboard_client.emit_event('agent:completed', {
                'agent_id': agent.id,
                'success': result.success,
                'duration': result.duration
            })

        return result
    else:
        # Single-threaded execution (existing path)
        return await self._execute_skill_direct(step)

async def _execute_via_agent(self, agent: Agent, step: SkillStep):
    """Execute skill through spawned agent"""
    # Get agent executor
    agent_executor = self._get_agent_executor(agent.role)

    # Execute with progress tracking
    result = await agent_executor.execute(
        skill_name=step.skill_name,
        parameters=step.parameters,
        context=self.execution_context
    )

    # Update agent status
    agent.status = 'completed' if result.success else 'failed'
    agent.duration = result.duration

    return result

async def _execute_parallel_steps(self, steps: List[SkillStep]):
    """Execute multiple steps in parallel using agent pool"""
    # Spawn agents for each step
    agents_and_steps = []
    for i, step in enumerate(steps):
        agent = await self.agent_pool.spawn_agent(
            skill_name=step.skill_name,
            parameters=step.parameters,
            session_id=self.session_id
        )
        agents_and_steps.append((agent, step))

    # Execute all in parallel
    tasks = [
        self._execute_via_agent(agent, step)
        for agent, step in agents_and_steps
    ]

    results = await asyncio.gather(*tasks)

    return results
```

**Step 2.4: Release File Lock**

```python
serena.write_memory("file-locks.md", f"""
## Available Files
- `src/shannon/orchestration/orchestrator.py` - Available (released by Agent 2 at {timestamp})
""")
```

**Run Tests (should PASS)**:
```bash
pytest tests/orchestration/test_orchestrator_agents.py -v
# Expected: All 2 tests PASS
```

**Step 2.5: Report Gate 2**

```python
serena.write_memory("agent-status.md", f"""
## Agent 2: Agent Pool
- Status: GATE_2_COMPLETE
- Phase: Orchestrator Integration Complete
- Progress: 8/32 criteria (3 pool + 5 orchestrator tests)
- Blockers: None
- Next: Frontend Dashboard (Gate 3)
- Branch: agent2-pool
""")
```

**GATE 2 VALIDATION**:

1. [ ] All Gate 1 tests still pass (3/3)
2. [ ] `pytest tests/orchestration/test_orchestrator_agents.py::test_single_agent_spawning` - PASS
3. [ ] `pytest tests/orchestration/test_orchestrator_agents.py::test_parallel_agent_execution` - PASS
4. [ ] agent:spawned event emitted with correct payload
5. [ ] agent:completed event emitted after execution

**IF ALL 8 PASS**: Proceed to Phase 3
**IF ANY FAIL**: Debug → Fix → Retry Gate 2

---

#### Phase 3: Frontend - Dashboard Panel (Gate 3/4)

**Step 3.1: Acquire Dashboard Store Lock**

```python
locks = serena.read_memory("file-locks.md")
if "dashboardStore.ts" in locks:
    # Wait for lock release
    # Report blocker...
else:
    serena.write_memory("file-locks.md", f"""
## LOCKED Files
- `dashboard/src/store/dashboardStore.ts` - LOCKED by Agent 2 ({timestamp})
""")
```

**Step 3.2: Update Dashboard Store**

**File**: `dashboard/src/store/dashboardStore.ts`

**Add agent state**:

```typescript
// ADD to store interface:
agents: Agent[];

// ADD action methods:
addAgent: (agent: Agent) => void;
updateAgent: (agentId: string, updates: Partial<Agent>) => void;
removeAgent: (agentId: string) => void;

// IMPLEMENT actions:
addAgent: (agent) => set((state) => ({
  agents: [...state.agents, agent]
})),

updateAgent: (agentId, updates) => set((state) => ({
  agents: state.agents.map(a =>
    a.id === agentId ? { ...a, ...updates } : a
  )
})),

removeAgent: (agentId) => set((state) => ({
  agents: state.agents.filter(a => a.id !== agentId)
})),

// ADD to handleSocketEvent switch:
case 'agent:spawned':
  if (data.data && data.data.agent_id) {
    get().addAgent({
      id: data.data.agent_id,
      skill_name: data.data.skill_name,
      role: data.data.role,
      status: 'running',
      progress: 0,
      session_id: data.data.session_id
    });
  }
  break;

case 'agent:completed':
  if (data.data && data.data.agent_id) {
    get().updateAgent(data.data.agent_id, {
      status: data.data.success ? 'completed' : 'failed',
      progress: 100,
      duration: data.data.duration
    });
  }
  break;
```

**Step 3.3: Release Dashboard Store Lock**

```python
serena.write_memory("file-locks.md", f"""
## Available Files
- `dashboard/src/store/dashboardStore.ts` - Available (released by Agent 2 at {timestamp})
""")
```

**Step 3.4: Update AgentPool Panel**

**File**: `dashboard/src/panels/AgentPool.tsx`

```typescript
export function AgentPool() {
  const agents = useDashboardStore((state) => state.agents);

  const activeAgents = agents.filter(a => a.status === 'running');
  const completedAgents = agents.filter(a => a.status === 'completed' || a.status === 'failed');

  if (agents.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        No agents spawned yet
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col p-4 space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">Agent Pool</h2>
        <span className="text-sm text-gray-400">
          {activeAgents.length} active / 8 max
        </span>
      </div>

      {/* Active Agents */}
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-400">Active Agents</h3>
        {activeAgents.length === 0 && (
          <div className="text-sm text-gray-500">No active agents</div>
        )}
        {activeAgents.map(agent => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>

      {/* Completed Agents (Collapsible) */}
      {completedAgents.length > 0 && (
        <details className="space-y-2">
          <summary className="text-sm font-medium text-gray-400 cursor-pointer">
            Completed Agents ({completedAgents.length})
          </summary>
          <div className="space-y-2 mt-2">
            {completedAgents.map(agent => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        </details>
      )}
    </div>
  );
}

function AgentCard({ agent }: { agent: Agent }) {
  return (
    <div
      data-testid="agent-card"
      className="border rounded p-3 bg-gray-900"
    >
      <div className="flex justify-between items-start">
        <div>
          <span className="font-medium text-white">{agent.role}</span>
          <span className="text-sm text-gray-400"> - {agent.skill_name}</span>
        </div>
        <StatusBadge status={agent.status} />
      </div>

      {agent.status === 'running' && (
        <div className="mt-2">
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="progress-bar bg-blue-500 h-2 rounded-full transition-all"
              style={{ width: `${agent.progress}%` }}
            />
          </div>
        </div>
      )}

      {agent.duration > 0 && (
        <div className="mt-2 text-xs text-gray-400">
          Duration: {agent.duration.toFixed(2)}s
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors = {
    running: 'bg-blue-500',
    completed: 'bg-green-500',
    failed: 'bg-red-500'
  };

  return (
    <span className={`px-2 py-1 rounded text-xs text-white ${colors[status] || 'bg-gray-500'}`}>
      {status}
    </span>
  );
}
```

**Step 3.5: Report Gate 3**

```python
serena.write_memory("agent-status.md", f"""
## Agent 2: Agent Pool
- Status: GATE_3_COMPLETE
- Phase: Frontend Dashboard Complete
- Progress: 11/32 criteria (backend + frontend implementation)
- Blockers: None
- Next: Playwright Validation (Gate 4 - FINAL)
- Branch: agent2-pool
""")
```

**GATE 3 VALIDATION**:

1. [ ] dashboardStore has `agents` state variable
2. [ ] dashboardStore has `addAgent()` method
3. [ ] dashboardStore has `updateAgent()` method
4. [ ] dashboardStore handles `agent:spawned` event
5. [ ] dashboardStore handles `agent:completed` event
6. [ ] AgentPool component renders without errors
7. [ ] Active agent count displays correctly
8. [ ] Agent cards render with skill name and role

**IF ALL 19 PASS**: Proceed to Phase 4 (final gate)
**IF ANY FAIL**: Debug → Fix → Retry Gate 3

---

#### Phase 4: Playwright Validation (Gate 4/4 - FINAL)

**Step 4.1: CLI + Dashboard Integration Test**

```bash
# Terminal 1: Start dashboard
cd dashboard && npm run dev

# Terminal 2: Run multi-agent task
cd /tmp/agent2-test
git init && echo ".gitignore" > .gitignore

# Ensure Agent 1 merged (multi-file working)
shannon do "analyze code and run tests and check security" --dashboard
```

**Step 4.2: Playwright Test Script**

**File**: `agent2_playwright.ts`

```typescript
import { test, expect } from '@playwright/test';

test('Agent pool shows 3 active agents', async ({ page }) => {
  // Navigate
  await page.goto('http://localhost:5175');
  await expect(page.locator('text=Connected')).toBeVisible({ timeout: 5000 });

  // Select Agent Pool panel
  await page.click('text=Agent Pool');

  // Wait for agents to spawn
  await expect(page.locator('text=3 active / 8 max')).toBeVisible({ timeout: 10000 });

  // Count agent cards
  const agentCards = page.locator('[data-testid="agent-card"]');
  await expect(agentCards).toHaveCount(3);

  // Verify skill names visible
  await expect(page.locator('text=code_analysis')).toBeVisible();

  // Verify roles visible
  await expect(page.locator('text=Analysis')).toBeVisible();

  // Verify progress bar present
  const progressBar = page.locator('.progress-bar');
  await expect(progressBar).toBeVisible();

  // Wait for completion
  await expect(page.locator('text=0 active / 8 max')).toBeVisible({ timeout: 60000 });

  // Verify completed section
  await page.click('text=Completed Agents');
  await expect(page.locator('text=3')).toBeVisible();  // 3 completed

  // Screenshot
  await page.screenshot({ path: 'batch2-agent2-pool-validated.png' });
});
```

**Run Playwright**:
```bash
playwright test agent2_playwright.ts
```

**Step 4.3: Final Validation**

**GATE 4 VALIDATION** (FINAL - 32/32 total):

1. [ ] All previous gates pass (19 criteria)
2. [ ] Terminal shows: "Spawning 3 agents for parallel execution"
3. [ ] Terminal shows 3× "Event: agent:spawned"
4. [ ] Terminal shows 3× "Event: agent:completed"
5. [ ] Exit code: 0
6. [ ] Execution time: < 60 seconds (parallel faster than sequential)
7. [ ] `playwright.navigate("http://localhost:5175")` - Success
8. [ ] `playwright.wait_for("text=Connected")` - Success
9. [ ] `playwright.click("text=Agent Pool")` - Success
10. [ ] `playwright.wait_for("text=3 active / 8 max", timeout=10000)` - Success
11. [ ] Agent card count: 3
12. [ ] Skill name visible: `code_analysis`
13. [ ] Role visible: `Analysis`
14. [ ] Progress bar visible
15. [ ] Wait for completion: `text=0 active / 8 max` appears
16. [ ] Completed section shows 3 agents
17. [ ] Screenshot captured and > 10KB
18. [ ] Regression: Multi-file still works (Agent 1 not broken)
19. [ ] Regression: Validation streaming still works (Batch 1 not broken)
20. [ ] pytest: All tests pass (including new agent tests)

**IF ALL 32 PASS**: Agent 2 COMPLETE ✅
**IF ANY FAIL**: Debug → Fix → Retry Gate 4

---

### Agent 2 Completion Protocol

**Final Serena Update**:
```python
serena.write_memory("agent-status.md", f"""
## Agent 2: Agent Pool
- Status: COMPLETE
- All Gates: 4/4
- Total Criteria: 32/32 PASS
- Branch: agent2-pool
- Evidence: batch2-agent2-pool-validated.png
- Ready for Merge: YES
""")
```

**Final Commit**:
```bash
git add .
git commit -m "Agent 2 COMPLETE: Agent Pool - 32/32 validated

GATES:
- Gate 1: AgentPool Enhancement (3/3)
- Gate 2: Orchestrator Integration (5/5)
- Gate 3: Frontend Dashboard (11/11)
- Gate 4: Playwright Validation (13/13)

IMPLEMENTATION:
- AgentPool.spawn_agent() with capacity limits
- Orchestrator parallel execution
- Agent cards in dashboard
- Real-time agent status updates

EVIDENCE:
- Screenshot: batch2-agent2-pool-validated.png
- Playwright: 3 agents validated
- Tests: All passing

Ready for orchestrator merge
"
git push origin agent2-pool
```

---

Due to character limits, I'll continue the plan in the next write. This establishes the pattern - each agent gets:
- 4 internal validation gates
- 20-40 specific validation criteria
- Serena coordination protocol
- File ownership/locking
- Branch strategy
- Complete mission brief with TDD implementation steps

Shall I continue with Agents 3-8, the orchestrator protocol, and integration sections?
