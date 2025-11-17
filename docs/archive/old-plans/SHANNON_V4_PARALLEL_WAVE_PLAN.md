# Shannon V4: Parallel Wave Execution Plan

> **Execution Philosophy**: Validation-driven parallel development with WORK-UNTIL-PASS gates

**Timeline**: ~2 weeks (10h implementation + 1w integration + 3d release)
**Structure**: 1 Solo Batch + 2 Parallel Waves + Integration + Release
**Validation**: 257 specific, measurable criteria with Playwright evidence
**Skills**: dispatching-parallel-agents, test-driven-development, sitrep-reporting, playwright-skill

---

## Execution Structure

```
BATCH 1 (Solo, 3h)
   Validation Streaming ← MUST work first
         ↓
WAVE 1 (6 Parallel Agents, 4h wall time)
   ├─ Agent 1: Multi-File
   ├─ Agent 2: Agent Pool
   ├─ Agent 3: Decision Engine
   ├─ Agent 4: Research
   ├─ Agent 5: Ultrathink
   └─ Agent 6: Basic Controls (HALT/RESUME/ROLLBACK)
         ↓
WAVE 2 (2 Parallel Agents, 3h wall time)
   ├─ Agent 7: Advanced Controls (REDIRECT/INJECT/APPROVE/OVERRIDE)
   └─ Agent 8: FileDiff Panel
         ↓
BATCH 2 (Solo, 1 week)
   Integration Testing
         ↓
BATCH 3 (Solo, 3-5 days)
   Documentation + Release
```

**Total**: ~2 weeks (not 17 weeks sequential)

---

## BATCH 1: Validation Streaming (SOLO - MUST BE FIRST)

**Priority**: CRITICAL (enables validation of all other batches)
**Duration**: 2-3 hours
**Why First**: Cannot validate any other feature without seeing test output
**Why Solo**: Everything else depends on this working

### Implementation

**Backend** (`src/shannon/executor/validator.py`):
1. Modify `_run_check()` to stream output line-by-line:
   ```python
   async def _run_check(self, command: str):
       process = await asyncio.create_subprocess_shell(...)

       async for line in process.stdout:
           # Emit each line immediately
           if self.dashboard_client:
               await self.dashboard_client.emit_event('validation:output', {
                   'line': line.decode().strip(),
                   'type': 'stdout',
                   'timestamp': time.time()
               })
   ```

2. Add test status tracking:
   - Parse pytest output for test names
   - Detect PASSED/FAILED
   - Include in events

**Frontend** (`dashboard/src/`):
1. Update `store/dashboardStore.ts`:
   ```typescript
   validationOutput: [] as ValidationLine[],

   case 'validation:output':
     set((state) => ({
       validationOutput: [...state.validationOutput, {
         line: data.data.line,
         type: data.data.type,
         timestamp: data.data.timestamp
       }]
     }));
   ```

2. Update `panels/Validation.tsx`:
   ```typescript
   export function Validation() {
     const output = useDashboardStore((state) => state.validationOutput);
     const containerRef = useRef<HTMLDivElement>(null);

     // Auto-scroll to bottom
     useEffect(() => {
       containerRef.current?.scrollTo(0, containerRef.current.scrollHeight);
     }, [output]);

     return (
       <div ref={containerRef} className="h-full overflow-y-auto">
         {output.map((line, i) => (
           <div key={i} className={`font-mono text-sm ${
             line.line.includes('PASSED') ? 'text-green-500' :
             line.line.includes('FAILED') ? 'text-red-500' :
             'text-gray-300'
           }`}>
             {line.line}
           </div>
         ))}
       </div>
     );
   }
   ```

**Unit Tests**:
1. `tests/executor/test_validator_streaming.py`:
   - test_output_streams_line_by_line
   - test_event_emission_per_line
   - test_failure_detection
2. Run: `pytest tests/executor/test_validator_streaming.py -v`

---

### VALIDATION GATE 1 (MANDATORY - WORK UNTIL ALL 27 PASS)

**Cannot proceed to Wave 1 until:**

#### Backend Unit Tests:
1. [ ] pytest tests/executor/test_validator_streaming.py::test_output_streams_line_by_line - PASS
2. [ ] pytest tests/executor/test_validator_streaming.py::test_event_emission_per_line - PASS
3. [ ] pytest tests/executor/test_validator_streaming.py::test_failure_detection - PASS
4. [ ] pytest (all tests): Shows "224 passed" (was 221, added 3)

#### CLI Validation:
5. [ ] cd /tmp/batch1-validation-test && git init && echo "__pycache__/" > .gitignore
6. [ ] Create test file with 5 tests (3 pass, 2 fail)
7. [ ] shannon do "run tests" --dashboard
8. [ ] Terminal output shows line-by-line streaming
9. [ ] Terminal shows: "test_example_1 PASSED"
10. [ ] Terminal shows: "test_example_4 FAILED"
11. [ ] Exit code: 1 (tests failed)

#### Dashboard Validation (Playwright):
12. [ ] playwright.navigate("http://localhost:5175")
13. [ ] playwright.wait_for("text=Connected", timeout=5000) - PASS
14. [ ] playwright.click("text=Validation") - Select panel
15. [ ] playwright.wait_for("text=test_", timeout=10000) - First test line appears
16. [ ] line_count = playwright.evaluate("() => document.querySelectorAll('.font-mono').length")
17. [ ] line_count > 15 (multiple test lines visible)
18. [ ] green_line = playwright.evaluate("() => document.querySelector('.text-green-500')")
19. [ ] green_line !== null (PASSED line is green)
20. [ ] red_line = playwright.evaluate("() => document.querySelector('.text-red-500')")
21. [ ] red_line !== null (FAILED line is red)
22. [ ] Auto-scroll works: Last line is in viewport
23. [ ] playwright.screenshot("batch1-validation-streaming-working.png")

#### Performance Validation:
24. [ ] Latency test: Backend emits line → Appears in UI within 200ms
25. [ ] Load test: 100 lines stream without UI freeze

#### Regression:
26. [ ] shannon exec still works (V3.5 not broken)
27. [ ] Dashboard connection still works
28. [ ] pytest: All 224 tests pass

#### Evidence:
29. [ ] batch1-validation-streaming-working.png committed (shows green/red lines)
30. [ ] Terminal output saved: batch1_validation.log
31. [ ] Commit message: "VALIDATED: Validation Streaming - 27/27 criteria passed"

**RESULT**: 27/27 → BATCH 1 COMPLETE → Ready for Wave 1

**IF <27**: Debug → Fix → Re-validate → Repeat until 27/27

---

## WAVE 1: Core Features (6 PARALLEL AGENTS)

**Duration**: 4 hours wall time (13 hours if sequential)
**Agents**: 6 executing simultaneously
**Skill**: Use `dispatching-parallel-agents` to spawn all 6
**Validation**: 182 total criteria (validated in parallel by agents)

### Wave 1 Agent Missions

Each agent receives:
- Detailed mission brief
- Required skills to invoke
- Validation criteria list
- SITREP reporting schedule
- Evidence requirements

---

### AGENT 1: Multi-File Generation

**Skill Invocation**:
```
Use test-driven-development skill throughout
Use sitrep-reporting every 30 minutes
Use verification-before-completion before claiming done
```

**Mission**: Implement multi-file generation - shannon do creates ALL files (not 1 of N)

**Duration**: 3-4 hours

#### Implementation Tasks

**Backend**:
1. Create `src/shannon/orchestration/multi_file_parser.py`:
   - Class MultiFileRequest (dataclass)
   - Class MultiFileParser
   - Method: is_multi_file(task) → bool
   - Method: parse(task) → Optional[MultiFileRequest]
   - Patterns: "create X: a.py, b.py", "with a.py and b.py", "a.py, b.py, c.py"

2. Create `src/shannon/executor/multi_file_executor.py`:
   - Class MultiFileExecutor
   - Method: execute(task, dashboard_client) → MultiFileResult
   - Logic: Parse → Iterate files → Execute each via CompleteExecutor → Emit file:created per file → Commit all together

3. Update `src/shannon/cli/v4_commands/do.py`:
   - Import MultiFileParser, MultiFileExecutor
   - Detect multi-file: if parser.is_multi_file(task)
   - Delegate: executor.execute(task, dashboard_client)

**Unit Tests** (TDD - Write FIRST):
1. `tests/orchestration/test_multi_file_parser.py`:
   ```python
   def test_single_file_detection():
       parser = MultiFileParser()
       assert not parser.is_multi_file("create hello.py")

   def test_multi_file_detection():
       parser = MultiFileParser()
       assert parser.is_multi_file("create auth: tokens.py, middleware.py")

   def test_parse_extracts_files():
       parser = MultiFileParser()
       result = parser.parse("create auth: tokens.py, middleware.py, __init__.py")
       assert len(result.files) == 3
       assert "tokens.py" in result.files[0]
   ```

2. `tests/executor/test_multi_file_executor.py`:
   ```python
   @pytest.mark.asyncio
   async def test_creates_all_files():
       executor = MultiFileExecutor(Path("/tmp/test"))
       result = await executor.execute("create utils: math.py, string.py, file.py")

       assert result.success
       assert result.files_created == 3
       assert Path("/tmp/test/utils/math.py").exists()
       assert Path("/tmp/test/utils/string.py").exists()
       assert Path("/tmp/test/utils/file.py").exists()
   ```

3. Run: `pytest tests/*/test_multi_file*.py -v`
   - Expected: 5/5 passing BEFORE moving to integration

#### AGENT 1 VALIDATION CRITERIA (26 total)

**Unit Tests**:
1. [ ] pytest test_multi_file_parser.py::test_single_file_detection - PASS
2. [ ] pytest test_multi_file_parser.py::test_multi_file_detection - PASS
3. [ ] pytest test_multi_file_parser.py::test_parse_extracts_files - PASS
4. [ ] pytest test_multi_file_executor.py::test_creates_all_files - PASS
5. [ ] pytest test_multi_file_executor.py::test_single_file_delegates - PASS
6. [ ] pytest (all): "226 passed" (was 221+3 from batch1, +2 new)

**CLI Integration**:
7. [ ] cd /tmp/agent1-test && git init && echo "__pycache__/" > .gitignore && git add . && git commit -m "init"
8. [ ] shannon do "create auth: tokens.py, middleware.py, __init__.py"
9. [ ] ls auth/tokens.py - File exists (exit code 0)
10. [ ] ls auth/middleware.py - File exists
11. [ ] ls auth/__init__.py - File exists
12. [ ] wc -l auth/tokens.py returns > 10 (meaningful content)
13. [ ] grep -c "def\|class" auth/tokens.py returns >= 1 (has code)
14. [ ] git log -1 --name-only | grep -c "auth/" returns 3 (all files in commit)

**Playwright Validation**:
15. [ ] playwright.navigate("http://localhost:5175")
16. [ ] playwright.wait_for("text=Connected")
17. [ ] events = playwright.evaluate("() => document.querySelectorAll('[data-testid=\"event-item\"]').length")
18. [ ] events >= 5 (execution:started + 3 file:created + execution:completed)
19. [ ] playwright.screenshot("agent1-multi-file-validated.png")

**Mixed Directories Test**:
20. [ ] shannon do "create dir1/a.py, dir2/b.py, c.py"
21. [ ] All 3 files created in correct directories

**Regression**:
22. [ ] shannon do "single.py" still creates 1 file
23. [ ] Batch 1 validation streaming still works

**SITREP Requirements**:
24. [ ] Reported at 30min, 1h, 1.5h, etc.
25. [ ] Final SITREP shows: "26/26 criteria PASS"

**Evidence**:
26. [ ] Screenshot committed
27. [ ] SITREP logs committed
28. [ ] Commit: "Agent 1 COMPLETE: Multi-File - 26/26 validated"

**AGENT 1 COMPLETE**: 26/26 pass

---

### AGENT 2: Agent Pool (Backend + Frontend)

**Skill Invocation**:
```
Use test-driven-development (write tests first)
Use playwright-skill (for UI validation)
Use sitrep-reporting (status updates)
Use verification-before-completion (validate before done)
```

**Mission**: 8 parallel agents spawn and execute, visible in dashboard

**Duration**: 2-3 hours

#### Implementation Tasks

**Backend**:
1. Enhance `src/shannon/orchestration/agent_pool.py`:
   ```python
   class AgentPool:
       def __init__(self, max_active=8, max_total=50):
           self.max_active = max_active
           self.max_total = max_total
           self.active_agents = []

       async def spawn_agent(self, skill_name, parameters, session_id) -> Agent:
           if len(self.active_agents) >= self.max_active:
               raise AgentPoolFullError(f"At capacity: {self.max_active}")

           agent = Agent(
               id=str(uuid.uuid4()),
               skill_name=skill_name,
               role=self._determine_role(skill_name),
               session_id=session_id
           )

           self.active_agents.append(agent)

           await self.emit('agent:spawned', {
               'agent_id': agent.id,
               'skill_name': skill_name,
               'role': agent.role
           })

           return agent
   ```

2. Update `src/shannon/orchestration/orchestrator.py`:
   ```python
   async def _execute_via_agent(self, agent, step):
       # Execute skill through agent
       result = await agent.execute(step)

       await self.emit('agent:completed', {
           'agent_id': agent.id,
           'success': result.success,
           'duration': result.duration
       })

       return result

   async def _execute_parallel(self, steps):
       agents = [await self.agent_pool.spawn_agent(...) for step in steps]
       results = await asyncio.gather(*[self._execute_via_agent(a, s) for a, s in zip(agents, steps)])
       return results
   ```

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   ```typescript
   agents: [] as Agent[],

   addAgent: (agent) => set((state) => ({
     agents: [...state.agents, agent]
   })),

   updateAgent: (id, updates) => set((state) => ({
     agents: state.agents.map(a => a.id === id ? {...a, ...updates} : a)
   })),

   // In handleSocketEvent
   case 'agent:spawned':
     get().addAgent({
       id: data.data.agent_id,
       skill_name: data.data.skill_name,
       role: data.data.role,
       status: 'running',
       progress: 0
     });
     break;

   case 'agent:completed':
     get().updateAgent(data.data.agent_id, {
       status: data.data.success ? 'completed' : 'failed',
       progress: 100,
       duration: data.data.duration
     });
     break;
   ```

2. Update `dashboard/src/panels/AgentPool.tsx`:
   ```typescript
   export function AgentPool() {
     const agents = useDashboardStore((state) => state.agents);
     const active = agents.filter(a => a.status === 'running');

     return (
       <div>
         <h2>Agent Pool</h2>
         <p>{active.length} active / 8 max</p>

         {active.map(agent => (
           <div key={agent.id} data-testid="agent-card">
             <span>{agent.role}</span> - {agent.skill_name}
             <ProgressBar progress={agent.progress} />
           </div>
         ))}
       </div>
     );
   }
   ```

**Unit Tests** (TDD):
1. `tests/orchestration/test_agent_pool.py`:
   ```python
   @pytest.mark.asyncio
   async def test_spawn_agent():
       pool = AgentPool(max_active=8)
       agent = await pool.spawn_agent('code_analysis', {}, 'test')
       assert agent.id is not None
       assert len(pool.active_agents) == 1

   @pytest.mark.asyncio
   async def test_capacity_limit():
       pool = AgentPool(max_active=2)
       await pool.spawn_agent('skill1', {}, 'test')
       await pool.spawn_agent('skill2', {}, 'test')

       with pytest.raises(AgentPoolFullError):
           await pool.spawn_agent('skill3', {}, 'test')
   ```

2. Run: `pytest tests/orchestration/test_agent_pool.py -v`

#### AGENT 2 VALIDATION CRITERIA (32 total)

**Backend**:
1. [ ] AgentPool.spawn_agent() returns Agent with UUID
2. [ ] Agent.id format verified: len(id) == 36
3. [ ] Capacity enforced: 8th spawn works, 9th raises AgentPoolFullError
4. [ ] Orchestrator._execute_via_agent() completes successfully
5. [ ] asyncio.gather for 3 agents executes all 3
6. [ ] agent:spawned event payload has: agent_id, skill_name, role
7. [ ] agent:completed event payload has: agent_id, success, duration
8. [ ] pytest test_agent_pool.py: 4/4 PASS

**Frontend**:
9. [ ] dashboardStore.addAgent() adds to agents array
10. [ ] dashboardStore.updateAgent() modifies correct agent
11. [ ] AgentPool component renders without errors

**CLI + Dashboard Integration**:
12. [ ] cd /tmp/agent2-test && git init && echo ".gitignore" > .gitignore
13. [ ] shannon do "analyze code and run tests and check security" --dashboard
14. [ ] Terminal shows: "Spawning 3 agents..."
15. [ ] Terminal shows 3× "Event: agent:spawned"
16. [ ] playwright.navigate("http://localhost:5175")
17. [ ] playwright.click("text=Agent Pool")
18. [ ] playwright.wait_for("text=3 active / 8 max", timeout=10000) - PASS
19. [ ] agent_cards = playwright.evaluate("() => document.querySelectorAll('[data-testid=\"agent-card\"]').length")
20. [ ] agent_cards === 3 (exactly 3)
21. [ ] playwright.wait_for("text=code_analysis") - Skill name visible
22. [ ] playwright.wait_for("text=Analysis") - Role visible
23. [ ] progress_bar = playwright.evaluate("() => document.querySelector('.progress-bar')")
24. [ ] progress_bar !== null (progress bar exists)
25. [ ] playwright.wait_for("text=0 active / 8 max", timeout=60000) - All complete
26. [ ] playwright.screenshot("agent2-pool-validated.png")

**8 Agent Capacity Test**:
27. [ ] shannon do "8 parallel tasks" --dashboard spawns 8 agents
28. [ ] playwright.wait_for("text=8 active / 8 max")
29. [ ] Attempt 9th fails gracefully (error message clear)

**Regression**:
30. [ ] Batch 1 still works (validation streaming)
31. [ ] pytest: All tests pass

**Evidence**:
32. [ ] Screenshot shows 3 agents
33. [ ] SITREP logs committed
34. [ ] Commit: "Agent 2 COMPLETE: Agent Pool - 32/32"

**AGENT 2 COMPLETE**: 32/32 pass

---

### AGENT 3: Decision Engine (Backend + Frontend)

**Skill Invocation**:
```
Use test-driven-development
Use playwright-skill (UI validation)
Use sitrep-reporting
Use verification-before-completion
```

**Mission**: Human-in-the-loop decisions with auto-approval for high confidence

**Duration**: 3-4 hours
**Branch**: `agent3-decisions`
**File Ownership**:
- **Owned**: `src/shannon/orchestration/decision_engine.py` (create new)
- **Shared**: `src/shannon/orchestration/orchestrator.py` (with Agents 2, 6)
- **Shared**: `src/shannon/server/websocket.py` (with Agent 6)
- **Shared**: `dashboard/src/store/dashboardStore.ts` (with Agents 2, 6, 7)
- **Owned**: `dashboard/src/panels/Decisions.tsx` (create new)

#### Serena Protocol

**READS (Required Context)**:
1. `WAVE1_CODEBASE_STATE` - Baseline from Batch 1 completion
2. `AGENT2_GATE4_PASS` - Confirms AgentPool exists for integration

**WRITES (Progress Tracking)**:
1. `AGENT3_GATE1_PASS` - Backend unit tests passing
2. `AGENT3_GATE2_PASS` - Backend integration complete
3. `AGENT3_GATE3_PASS` - Frontend component working
4. `AGENT3_GATE4_PASS` - E2E Playwright validation complete
5. `AGENT3_COMPLETE` - All 34 criteria validated

**Memory Content Format**:
```markdown
# AGENT3_GATE1_PASS

Date: 2025-11-16
Criteria: 7/7 backend unit tests passing

Details:
- DecisionPoint dataclass: ✓
- DecisionOption dataclass: ✓
- Auto-approval logic: ✓ (confidence >= 0.95)
- Manual decision flow: ✓ (emits decision:created)
- Polling loop: ✓ (100ms intervals)
- pytest: 3/3 passing
- All tests green

Next: Gate 2 (Backend Integration)
```

#### TDD Implementation (Test-First Workflow)

**Phase 1: Backend Unit Tests (GATE 1)**

1. **Create Test File FIRST**: `tests/orchestration/test_decision_engine.py`
   ```python
   import pytest
   from shannon.orchestration.decision_engine import (
       DecisionEngine, DecisionPoint, DecisionOption
   )

   def test_decision_point_dataclass():
       """Verify DecisionPoint has required fields"""
       dp = DecisionPoint(
           id='test-1',
           title='Select Framework',
           description='Choose web framework',
           options=[],
           recommended='opt1',
           confidence=0.85,
           status='pending'
       )
       assert dp.id == 'test-1'
       assert dp.confidence == 0.85

   def test_decision_option_dataclass():
       """Verify DecisionOption structure"""
       opt = DecisionOption(
           id='opt1',
           label='React',
           description='Use React framework',
           pros=['Fast', 'Popular'],
           cons=['Complex setup'],
           confidence=0.90
       )
       assert opt.id == 'opt1'
       assert len(opt.pros) == 2

   @pytest.mark.asyncio
   async def test_auto_approve_high_confidence():
       """Auto-approve when confidence >= threshold"""
       engine = DecisionEngine()
       options = [
           DecisionOption(
               id='opt1',
               label='Recommended',
               description='High confidence choice',
               pros=['Tested', 'Fast'],
               cons=[],
               confidence=0.97
           )
       ]

       selected = await engine.request_decision(
           title='Test Decision',
           options=options,
           recommended='opt1',
           auto_approve_threshold=0.95
       )

       assert selected.id == 'opt1'
       assert engine.pending_decisions == {}  # Not pending

   @pytest.mark.asyncio
   async def test_manual_decision_low_confidence():
       """Emit decision:created when confidence < threshold"""
       engine = DecisionEngine()
       events_emitted = []

       # Mock event emission
       async def mock_emit(event_type, data):
           events_emitted.append((event_type, data))

       engine.emit = mock_emit

       options = [
           DecisionOption(
               id='opt1',
               label='Option A',
               description='Lower confidence',
               pros=['Pro 1'],
               cons=['Con 1'],
               confidence=0.70
           )
       ]

       # Should NOT auto-approve
       task = asyncio.create_task(
           engine.request_decision(
               title='Manual Decision',
               options=options,
               recommended='opt1',
               auto_approve_threshold=0.95
           )
       )

       await asyncio.sleep(0.2)  # Let it emit

       assert len(events_emitted) > 0
       assert events_emitted[0][0] == 'decision:created'

       # Simulate approval
       engine.approve_decision('test-1', 'opt1')

       result = await task
       assert result.id == 'opt1'
   ```

2. **Run Tests (EXPECT FAILURES)**:
   ```bash
   pytest tests/orchestration/test_decision_engine.py -v
   ```
   Expected: 0/3 passing (files don't exist yet)

3. **Implement MINIMAL Code to Pass**:

   Create `src/shannon/orchestration/decision_engine.py`:
   ```python
   from dataclasses import dataclass, field
   from typing import List, Optional, Dict
   import asyncio
   import uuid

   @dataclass
   class DecisionOption:
       """Single option in a decision point"""
       id: str
       label: str
       description: str
       pros: List[str] = field(default_factory=list)
       cons: List[str] = field(default_factory=list)
       confidence: float = 0.0

   @dataclass
   class DecisionPoint:
       """Decision point requiring user input or auto-approval"""
       id: str
       title: str
       description: str
       options: List[DecisionOption]
       recommended: str
       confidence: float
       status: str = 'pending'  # pending, approved, rejected

   class DecisionEngine:
       def __init__(self, dashboard_client=None):
           self.dashboard_client = dashboard_client
           self.pending_decisions: Dict[str, DecisionPoint] = {}
           self.decision_results: Dict[str, str] = {}  # decision_id -> option_id

       async def emit(self, event_type: str, data: dict):
           """Emit event to dashboard"""
           if self.dashboard_client:
               await self.dashboard_client.emit_event(event_type, data)

       async def request_decision(
           self,
           title: str,
           options: List[DecisionOption],
           recommended: str,
           auto_approve_threshold: float = 0.95,
           description: str = ''
       ) -> DecisionOption:
           """Request decision - auto-approve if high confidence"""

           # Find recommended option
           rec_option = next((o for o in options if o.id == recommended), options[0])

           # Auto-approve if high confidence
           if rec_option.confidence >= auto_approve_threshold:
               return rec_option

           # Create decision point
           decision_id = str(uuid.uuid4())
           decision = DecisionPoint(
               id=decision_id,
               title=title,
               description=description,
               options=options,
               recommended=recommended,
               confidence=rec_option.confidence,
               status='pending'
           )

           self.pending_decisions[decision_id] = decision

           # Emit for dashboard
           await self.emit('decision:created', {
               'decision_id': decision_id,
               'title': title,
               'description': description,
               'options': [
                   {
                       'id': o.id,
                       'label': o.label,
                       'description': o.description,
                       'pros': o.pros,
                       'cons': o.cons,
                       'confidence': o.confidence
                   }
                   for o in options
               ],
               'recommended': recommended,
               'confidence': rec_option.confidence
           })

           # Wait for approval
           selected_option_id = await self._wait_for_decision(decision_id)

           # Return selected option
           return next(o for o in options if o.id == selected_option_id)

       async def _wait_for_decision(self, decision_id: str, timeout: int = 300) -> str:
           """Poll for decision approval (100ms intervals)"""
           elapsed = 0
           while elapsed < timeout:
               if decision_id in self.decision_results:
                   return self.decision_results[decision_id]

               await asyncio.sleep(0.1)  # 100ms
               elapsed += 0.1

           raise TimeoutError(f"Decision {decision_id} not approved within {timeout}s")

       def approve_decision(self, decision_id: str, option_id: str):
           """Approve a pending decision"""
           if decision_id in self.pending_decisions:
               self.decision_results[decision_id] = option_id
               self.pending_decisions[decision_id].status = 'approved'
   ```

4. **Re-run Tests**:
   ```bash
   pytest tests/orchestration/test_decision_engine.py -v
   ```
   Expected: 3/3 PASS

5. **Write to Serena**:
   ```bash
   serena write-memory AGENT3_GATE1_PASS "[content from format above]"
   ```

**GATE 1 CRITERIA (7 total)**:
1. [ ] `test_decision_point_dataclass` - PASS
2. [ ] `test_decision_option_dataclass` - PASS
3. [ ] `test_auto_approve_high_confidence` - PASS
4. [ ] `test_manual_decision_low_confidence` - PASS
5. [ ] DecisionEngine class exists with all methods
6. [ ] Auto-approval logic correct (>= 0.95)
7. [ ] pytest: 3/3 passing

**Phase 2: Backend Integration (GATE 2)**

1. **Integration Test**: `tests/orchestration/test_decision_integration.py`
   ```python
   @pytest.mark.asyncio
   async def test_orchestrator_uses_decision_engine():
       """Orchestrator integrates DecisionEngine"""
       from shannon.orchestration.orchestrator import Orchestrator

       orch = Orchestrator()
       # Verify decision_engine attribute exists
       assert hasattr(orch, 'decision_engine')
       assert isinstance(orch.decision_engine, DecisionEngine)

   @pytest.mark.asyncio
   async def test_websocket_handler():
       """WebSocket approve_decision handler works"""
       # This requires mocking WebSocket, simpler in E2E
       pass
   ```

2. **Update Orchestrator** (`src/shannon/orchestration/orchestrator.py`):
   ```python
   from shannon.orchestration.decision_engine import DecisionEngine

   class Orchestrator:
       def __init__(self, ...):
           # Existing code...
           self.decision_engine = DecisionEngine(self.dashboard_client)

       async def execute_with_decisions(self, task):
           # Example usage
           options = self._analyze_approaches(task)

           selected = await self.decision_engine.request_decision(
               title="Select Implementation Approach",
               options=options,
               recommended=options[0].id,
               auto_approve_threshold=0.95
           )

           # Execute with selected approach
           return await self._execute_approach(selected)
   ```

3. **Update WebSocket** (`src/shannon/server/websocket.py`):
   ```python
   @sio.event
   async def approve_decision(sid, data):
       """Handle decision approval from dashboard"""
       decision_id = data['decision_id']
       option_id = data['option_id']

       # Get orchestrator instance
       orch = get_current_orchestrator()  # Implementation detail
       orch.decision_engine.approve_decision(decision_id, option_id)

       # Emit confirmation
       await sio.emit('decision:approved', {
           'decision_id': decision_id,
           'option_id': option_id
       })
   ```

**GATE 2 CRITERIA (8 total)**:
8. [ ] Orchestrator has decision_engine attribute
9. [ ] Orchestrator can call request_decision()
10. [ ] WebSocket handler approve_decision exists
11. [ ] WebSocket handler calls decision_engine.approve_decision()
12. [ ] WebSocket emits decision:approved event
13. [ ] Integration test passes
14. [ ] No circular imports
15. [ ] pytest: All tests passing

**Write to Serena**: `AGENT3_GATE2_PASS`

**Phase 3: Frontend Component (GATE 3)**

1. **Update Store** (`dashboard/src/store/dashboardStore.ts`):
   ```typescript
   interface DecisionOption {
     id: string;
     label: string;
     description: string;
     pros: string[];
     cons: string[];
     confidence: number;
   }

   interface DecisionPoint {
     id: string;
     title: string;
     description: string;
     options: DecisionOption[];
     recommended: string;
     confidence: number;
     status: 'pending' | 'approved' | 'rejected';
     selected_option?: string;
   }

   interface DashboardState {
     // Existing state...
     decisions: DecisionPoint[];

     // Actions
     addDecision: (decision: DecisionPoint) => void;
     approveDecision: (decisionId: string, optionId: string) => void;
   }

   export const useDashboardStore = create<DashboardState>((set, get) => ({
     // Existing state...
     decisions: [],

     addDecision: (decision) => set((state) => ({
       decisions: [...state.decisions, decision]
     })),

     approveDecision: async (decisionId, optionId) => {
       const socket = get().socket;
       if (!socket) return;

       socket.emit('approve_decision', {
         decision_id: decisionId,
         option_id: optionId
       });

       set((state) => ({
         decisions: state.decisions.map(d =>
           d.id === decisionId
             ? { ...d, status: 'approved' as const, selected_option: optionId }
             : d
         )
       }));
     },

     handleSocketEvent: (event, data) => {
       // Existing handlers...

       switch (event) {
         case 'decision:created':
           get().addDecision(data.data);
           break;

         case 'decision:approved':
           set((state) => ({
             decisions: state.decisions.map(d =>
               d.id === data.data.decision_id
                 ? { ...d, status: 'approved' as const }
                 : d
             )
           }));
           break;
       }
     }
   }));
   ```

2. **Create Component** (`dashboard/src/panels/Decisions.tsx`):
   ```typescript
   import React, { useState } from 'react';
   import { useDashboardStore } from '../store/dashboardStore';

   export function Decisions() {
     const decisions = useDashboardStore((state) => state.decisions);
     const approveDecision = useDashboardStore((state) => state.approveDecision);

     const pendingDecisions = decisions.filter(d => d.status === 'pending');

     if (pendingDecisions.length === 0) {
       return (
         <div className="p-4 text-gray-400">
           No pending decisions
         </div>
       );
     }

     return (
       <div className="p-4 space-y-6">
         {pendingDecisions.map(decision => (
           <DecisionCard
             key={decision.id}
             decision={decision}
             onApprove={approveDecision}
           />
         ))}
       </div>
     );
   }

   function DecisionCard({ decision, onApprove }: {
     decision: DecisionPoint;
     onApprove: (decisionId: string, optionId: string) => void;
   }) {
     const [selectedOption, setSelectedOption] = useState<string | null>(null);

     return (
       <div className="bg-yellow-900/20 border border-yellow-600 rounded-lg p-4">
         <h3 className="text-xl font-bold text-yellow-300 mb-2">
           {decision.title}
         </h3>
         {decision.description && (
           <p className="text-gray-300 mb-4">{decision.description}</p>
         )}

         <div className="grid grid-cols-1 gap-3 mb-4">
           {decision.options.map(option => (
             <div
               key={option.id}
               data-testid="decision-option"
               onClick={() => setSelectedOption(option.id)}
               className={`
                 border rounded-lg p-3 cursor-pointer transition-colors
                 ${selectedOption === option.id
                   ? 'border-blue-500 bg-blue-900/20'
                   : 'border-gray-600 hover:border-gray-500'
                 }
               `}
             >
               <div className="flex items-center justify-between mb-2">
                 <span className="font-bold text-white">
                   {option.label}
                   {option.id === decision.recommended && (
                     <span className="ml-2 text-yellow-400">⭐ Recommended</span>
                   )}
                 </span>
                 <span className="text-sm text-gray-400">
                   {(option.confidence * 100).toFixed(0)}% confidence
                 </span>
               </div>

               <p className="text-sm text-gray-300 mb-2">{option.description}</p>

               {option.pros.length > 0 && (
                 <div className="mb-1">
                   <span className="text-xs text-green-400 font-semibold">Pros:</span>
                   <ul className="text-xs text-gray-300 ml-4 list-disc">
                     {option.pros.map((pro, i) => <li key={i}>{pro}</li>)}
                   </ul>
                 </div>
               )}

               {option.cons.length > 0 && (
                 <div>
                   <span className="text-xs text-red-400 font-semibold">Cons:</span>
                   <ul className="text-xs text-gray-300 ml-4 list-disc">
                     {option.cons.map((con, i) => <li key={i}>{con}</li>)}
                   </ul>
                 </div>
               )}
             </div>
           ))}
         </div>

         <button
           onClick={() => selectedOption && onApprove(decision.id, selectedOption)}
           disabled={!selectedOption}
           className={`
             w-full py-2 px-4 rounded font-semibold
             ${selectedOption
               ? 'bg-blue-600 hover:bg-blue-700 text-white cursor-pointer'
               : 'bg-gray-700 text-gray-500 cursor-not-allowed'
             }
           `}
         >
           Approve Selected Option
         </button>
       </div>
     );
   }
   ```

3. **Add to Layout** (`dashboard/src/App.tsx`):
   ```typescript
   import { Decisions } from './panels/Decisions';

   // In panel routing
   {activePanel === 'decisions' && <Decisions />}
   ```

**GATE 3 CRITERIA (9 total)**:
16. [ ] DashboardStore has decisions array
17. [ ] DashboardStore.addDecision() works
18. [ ] DashboardStore.approveDecision() emits event
19. [ ] Decisions component renders without errors
20. [ ] DecisionCard component shows options
21. [ ] Clicking option selects it (border turns blue)
22. [ ] Approve button enabled only when option selected
23. [ ] Recommended option shows ⭐
24. [ ] Pros/Cons visible

**Write to Serena**: `AGENT3_GATE3_PASS`

**Phase 4: E2E Playwright Validation (GATE 4)**

1. **Create Test Orchestrator** (`tests/fixtures/decision_test_orchestrator.py`):
   ```python
   from shannon.orchestration.orchestrator import Orchestrator
   from shannon.orchestration.decision_engine import DecisionOption

   class DecisionTestOrchestrator(Orchestrator):
       async def execute_test_task(self):
           """Execute task that requires decision"""
           options = [
               DecisionOption(
                   id='opt1',
                   label='Approach A',
                   description='Conservative approach',
                   pros=['Safe', 'Well-tested'],
                   cons=['Slower'],
                   confidence=0.70
               ),
               DecisionOption(
                   id='opt2',
                   label='Approach B',
                   description='Aggressive approach',
                   pros=['Fast', 'Modern'],
                   cons=['Risky', 'Untested'],
                   confidence=0.60
               ),
               DecisionOption(
                   id='opt3',
                   label='Approach C',
                   description='Balanced approach',
                   pros=['Balanced', 'Flexible'],
                   cons=['Complex'],
                   confidence=0.65
               )
           ]

           selected = await self.decision_engine.request_decision(
               title="Select Implementation Approach",
               description="Choose how to implement the feature",
               options=options,
               recommended='opt1',
               auto_approve_threshold=0.95  # Will NOT auto-approve
           )

           return f"Executed with {selected.label}"
   ```

2. **Playwright Test** (`tests/e2e/test_agent3_decisions.py`):
   ```python
   import pytest
   from playwright.sync_api import Page, expect

   def test_manual_decision_approval(page: Page):
       """Test manual decision approval flow"""
       # 1. Start execution
       # (Assume CLI command started in separate process)

       # 2. Navigate to dashboard
       page.goto("http://localhost:5175")
       expect(page.locator("text=Connected")).to_be_visible(timeout=5000)

       # 3. Open Decisions panel
       page.click("text=Decisions")

       # 4. Wait for decision to appear
       expect(page.locator("text=Select Implementation Approach")).to_be_visible(timeout=10000)

       # 5. Verify 3 options shown
       options = page.locator('[data-testid="decision-option"]')
       expect(options).to_have_count(3)

       # 6. Verify recommended marked
       expect(page.locator("text=⭐ Recommended")).to_be_visible()

       # 7. Verify pros/cons visible
       expect(page.locator("text=Pros:")).to_be_visible()
       expect(page.locator("text=Cons:")).to_be_visible()

       # 8. Select option 2 (NOT recommended)
       page.locator('[data-testid="decision-option"]').nth(1).click()

       # 9. Verify blue border (selected)
       option2 = page.locator('[data-testid="decision-option"]').nth(1)
       expect(option2).to_have_class(re.compile(r'border-blue-500'))

       # 10. Click approve
       page.click("text=Approve Selected Option")

       # 11. Verify approved message
       expect(page.locator("text=Decision approved")).to_be_visible(timeout=5000)

       # 12. Screenshot
       page.screenshot(path="agent3-decision-validated.png")

   def test_auto_approval(page: Page):
       """Test auto-approval for high confidence"""
       # Execute with high confidence option
       # (Modified orchestrator to use confidence=0.97)

       page.goto("http://localhost:5175")

       # Decision should NOT appear in dashboard
       page.click("text=Decisions")
       expect(page.locator("text=No pending decisions")).to_be_visible(timeout=5000)

       # Execution should continue immediately
       # (Verify in terminal output)
   ```

**GATE 4 CRITERIA (10 total)**:
25. [ ] playwright.navigate("http://localhost:5175") - Success
26. [ ] Decision appears in panel within 10s
27. [ ] 3 options visible
28. [ ] Recommended option has ⭐
29. [ ] Pros/Cons visible
30. [ ] Clicking option selects it (blue border)
31. [ ] Approve button click works
32. [ ] Decision approval flows to backend
33. [ ] Execution resumes with selected option
34. [ ] Auto-approval test: No decision shown, execution continues

**Write to Serena**: `AGENT3_GATE4_PASS`

#### FINAL AGENT 3 VALIDATION (34 Total Criteria)

**Backend Unit Tests (7)**:
1-7. [As defined in GATE 1]

**Backend Integration (8)**:
8-15. [As defined in GATE 2]

**Frontend Component (9)**:
16-24. [As defined in GATE 3]

**E2E Playwright (10)**:
25-34. [As defined in GATE 4]

**Final Commit**:
```bash
git add .
git commit -m "Agent 3 COMPLETE: Decision Engine - 34/34 criteria validated

GATES PASSED:
- Gate 1: Backend Unit Tests (7/7)
- Gate 2: Backend Integration (8/8)
- Gate 3: Frontend Component (9/9)
- Gate 4: E2E Playwright (10/10)

Evidence: agent3-decision-validated.png
Branch: agent3-decisions"
```

**Write to Serena**: `AGENT3_COMPLETE`

**AGENT 3 COMPLETE**: 34/34 pass

---

### AGENT 4: Research Orchestration (Backend + CLI)

**Skill Invocation**:
```
Use test-driven-development
Use sitrep-reporting
Use verification-before-completion
```

**Mission**: shannon research gathers knowledge from Fire Crawl, Tavily, web search

**Duration**: 2-3 hours
**Branch**: `agent4-research`
**File Ownership**:
- **Owned**: `src/shannon/research/orchestrator.py` (enhance existing)
- **Owned**: `src/shannon/research/synthesizer.py` (create new)
- **Shared**: `src/shannon/cli/commands.py` (add research command)
- **Owned**: `dashboard/src/panels/Research.tsx` (create new if dashboard support needed)

#### Serena Protocol

**READS (Required Context)**:
1. `WAVE1_CODEBASE_STATE` - Baseline from Batch 1 completion

**WRITES (Progress Tracking)**:
1. `AGENT4_GATE1_PASS` - Backend unit tests passing
2. `AGENT4_GATE2_PASS` - MCP integrations working
3. `AGENT4_GATE3_PASS` - CLI command functional
4. `AGENT4_GATE4_PASS` - E2E validation complete
5. `AGENT4_COMPLETE` - All 25 criteria validated

**Memory Content Format**:
```markdown
# AGENT4_GATE1_PASS

Date: 2025-11-16
Criteria: 6/6 backend unit tests passing

Details:
- ResearchOrchestrator class: ✓
- gather_from_firecrawl(): ✓
- gather_from_web(): ✓
- synthesize_knowledge(): ✓
- rank_by_relevance(): ✓
- pytest: 4/4 passing

Next: Gate 2 (MCP Integration)
```

#### TDD Implementation (Test-First Workflow)

**Phase 1: Backend Unit Tests (GATE 1)**

1. **Create Test File FIRST**: `tests/research/test_orchestrator.py`
   ```python
   import pytest
   from shannon.research.orchestrator import ResearchOrchestrator
   from shannon.research.synthesizer import KnowledgeSynthesizer

   @pytest.fixture
   def orchestrator():
       return ResearchOrchestrator()

   def test_orchestrator_initialization(orchestrator):
       """Verify orchestrator initializes correctly"""
       assert orchestrator is not None
       assert hasattr(orchestrator, 'gather_from_firecrawl')
       assert hasattr(orchestrator, 'gather_from_web')

   @pytest.mark.asyncio
   async def test_firecrawl_integration_mock():
       """Test firecrawl integration with mocked MCP"""
       orch = ResearchOrchestrator()

       # Mock MCP call
       async def mock_firecrawl(urls):
           return [{
               'url': 'https://example.com',
               'content': 'Test content about React hooks',
               'title': 'React Hooks Guide'
           }]

       orch._call_firecrawl = mock_firecrawl

       results = await orch.gather_from_firecrawl(
           query="React hooks",
           urls=["https://react.dev/hooks"]
       )

       assert len(results) > 0
       assert 'content' in results[0]
       assert 'url' in results[0]

   @pytest.mark.asyncio
   async def test_web_search_mock():
       """Test web search with mocked Tavily"""
       orch = ResearchOrchestrator()

       async def mock_tavily(query):
           return [{
               'title': 'React Server Components',
               'url': 'https://example.com/rsc',
               'snippet': 'Introduction to React Server Components',
               'score': 0.95
           }]

       orch._call_tavily = mock_tavily

       results = await orch.gather_from_web("React Server Components")

       assert len(results) > 0
       assert results[0]['score'] > 0

   def test_knowledge_synthesis():
       """Test knowledge synthesis and deduplication"""
       synth = KnowledgeSynthesizer()

       sources = [
           {'content': 'React is a JavaScript library', 'source': 'A'},
           {'content': 'React is a JavaScript library for UI', 'source': 'B'},
           {'content': 'Vue is a progressive framework', 'source': 'C'}
       ]

       insights = synth.synthesize(sources)

       # Should deduplicate similar content
       assert len(insights) < len(sources)
       assert any('React' in i['text'] for i in insights)

   def test_relevance_ranking():
       """Test relevance scoring and ranking"""
       synth = KnowledgeSynthesizer()

       insights = [
           {'text': 'React hooks enable state', 'score': 0.7},
           {'text': 'React is popular', 'score': 0.5},
           {'text': 'useState is a hook', 'score': 0.9}
       ]

       ranked = synth.rank_by_relevance(insights, query="React hooks")

       # Should be sorted by score descending
       assert ranked[0]['score'] >= ranked[1]['score']
       assert ranked[1]['score'] >= ranked[2]['score']
   ```

2. **Implement MINIMAL Code**:

   Create `src/shannon/research/synthesizer.py`:
   ```python
   from dataclasses import dataclass
   from typing import List, Dict
   import hashlib

   @dataclass
   class Insight:
       text: str
       source: str
       score: float
       hash: str

   class KnowledgeSynthesizer:
       def __init__(self, similarity_threshold: float = 0.85):
           self.similarity_threshold = similarity_threshold

       def synthesize(self, sources: List[Dict]) -> List[Dict]:
           """Combine and deduplicate insights from multiple sources"""
           insights = []
           seen_hashes = set()

           for source in sources:
               content = source.get('content', '')

               # Extract insights (simplified - split by sentences)
               sentences = content.split('. ')

               for sentence in sentences:
                   if len(sentence.strip()) < 20:  # Skip short fragments
                       continue

                   # Create hash for deduplication
                   text_hash = hashlib.md5(sentence.lower().encode()).hexdigest()[:8]

                   if text_hash not in seen_hashes:
                       insights.append({
                           'text': sentence.strip(),
                           'source': source.get('source', 'unknown'),
                           'score': 0.5,  # Default score
                           'hash': text_hash
                       })
                       seen_hashes.add(text_hash)

           return insights

       def rank_by_relevance(
           self,
           insights: List[Dict],
           query: str
       ) -> List[Dict]:
           """Rank insights by relevance to query"""
           # Simple keyword matching scoring
           query_terms = set(query.lower().split())

           for insight in insights:
               text_terms = set(insight['text'].lower().split())
               overlap = len(query_terms & text_terms)

               # Boost score based on query overlap
               insight['score'] = insight.get('score', 0.5) + (overlap * 0.1)

           # Sort by score descending
           return sorted(insights, key=lambda x: x['score'], reverse=True)
   ```

   Update `src/shannon/research/orchestrator.py`:
   ```python
   from typing import List, Dict, Optional
   import asyncio
   from pathlib import Path
   import json
   import time

   from shannon.research.synthesizer import KnowledgeSynthesizer

   class ResearchOrchestrator:
       def __init__(self, dashboard_client=None):
           self.dashboard_client = dashboard_client
           self.synthesizer = KnowledgeSynthesizer()

       async def _call_firecrawl(self, urls: List[str]) -> List[Dict]:
           """Call Fire Crawl MCP to scrape URLs"""
           # Integration with Fire Crawl MCP
           # This will be implemented in Gate 2
           results = []

           for url in urls:
               # Placeholder - actual MCP call in Gate 2
               results.append({
                   'url': url,
                   'content': '',
                   'title': ''
               })

           return results

       async def _call_tavily(self, query: str, max_results: int = 10) -> List[Dict]:
           """Call Tavily MCP for web search"""
           # Integration with Tavily MCP
           # This will be implemented in Gate 2
           return []

       async def gather_from_firecrawl(
           self,
           query: str,
           urls: List[str]
       ) -> List[Dict]:
           """Gather knowledge from specific URLs using Fire Crawl"""
           raw_results = await self._call_firecrawl(urls)

           # Add source metadata
           for result in raw_results:
               result['source'] = f"firecrawl:{result['url']}"

           return raw_results

       async def gather_from_web(
           self,
           query: str,
           max_results: int = 10
       ) -> List[Dict]:
           """Gather knowledge from web search using Tavily"""
           raw_results = await self._call_tavily(query, max_results)

           # Add source metadata
           for result in raw_results:
               result['source'] = f"web:{result.get('url', 'unknown')}"

           return raw_results

       async def gather_knowledge(
           self,
           query: str,
           urls: Optional[List[str]] = None
       ) -> Dict:
           """Complete research workflow"""
           sources = []

           # Gather from Fire Crawl if URLs provided
           if urls:
               firecrawl_results = await self.gather_from_firecrawl(query, urls)
               sources.extend(firecrawl_results)

           # Gather from web search
           web_results = await self.gather_from_web(query)
           sources.extend(web_results)

           # Synthesize knowledge
           insights = self.synthesizer.synthesize(sources)

           # Rank by relevance
           ranked_insights = self.synthesizer.rank_by_relevance(insights, query)

           # Save results
           output_path = self._save_results(query, ranked_insights, sources)

           return {
               'query': query,
               'insights': ranked_insights[:15],  # Top 15
               'source_count': len(sources),
               'output_path': str(output_path),
               'summary': self._create_summary(ranked_insights[:10])
           }

       def _save_results(
           self,
           query: str,
           insights: List[Dict],
           sources: List[Dict]
       ) -> Path:
           """Save research results to disk"""
           output_dir = Path.cwd() / '.shannon' / 'research'
           output_dir.mkdir(parents=True, exist_ok=True)

           timestamp = int(time.time())
           safe_query = query.replace(' ', '_')[:50]
           filename = f"{safe_query}_{timestamp}.json"

           output_path = output_dir / filename

           data = {
               'query': query,
               'timestamp': timestamp,
               'insights': insights,
               'sources': sources
           }

           with open(output_path, 'w') as f:
               json.dump(data, f, indent=2)

           return output_path

       def _create_summary(self, insights: List[Dict]) -> str:
           """Create human-readable summary"""
           lines = [f"Research Summary: {len(insights)} key insights\n"]

           for i, insight in enumerate(insights, 1):
               lines.append(f"{i}. {insight['text']} (score: {insight['score']:.2f})")

           return '\n'.join(lines)
   ```

3. **Run Tests**:
   ```bash
   pytest tests/research/test_orchestrator.py -v
   ```
   Expected: 4/4 PASS

**GATE 1 CRITERIA (6 total)**:
1. [ ] `test_orchestrator_initialization` - PASS
2. [ ] `test_firecrawl_integration_mock` - PASS
3. [ ] `test_web_search_mock` - PASS
4. [ ] `test_knowledge_synthesis` - PASS
5. [ ] `test_relevance_ranking` - PASS
6. [ ] pytest: 4/4 passing

**Write to Serena**: `AGENT4_GATE1_PASS`

**Phase 2: MCP Integration (GATE 2)**

1. **Integration Tests**: `tests/research/test_mcp_integration.py`
   ```python
   import pytest

   @pytest.mark.skipif(
       not has_mcp('firecrawl'),
       reason="Fire Crawl MCP not available"
   )
   @pytest.mark.asyncio
   async def test_real_firecrawl():
       """Test actual Fire Crawl MCP integration"""
       orch = ResearchOrchestrator()
       results = await orch.gather_from_firecrawl(
           "React hooks",
           ["https://react.dev/reference/react"]
       )

       assert len(results) > 0
       assert results[0]['content']  # Has content

   @pytest.mark.skipif(
       not has_mcp('tavily'),
       reason="Tavily MCP not available"
   )
   @pytest.mark.asyncio
   async def test_real_tavily():
       """Test actual Tavily MCP integration"""
       orch = ResearchOrchestrator()
       results = await orch.gather_from_web("React Server Components")

       assert len(results) > 0
       assert results[0]['url']
   ```

2. **Implement Real MCP Calls**:

   Update `src/shannon/research/orchestrator.py`:
   ```python
   async def _call_firecrawl(self, urls: List[str]) -> List[Dict]:
       """Call Fire Crawl MCP to scrape URLs"""
       try:
           # Use firecrawl_scrape from MCP
           results = []

           for url in urls:
               response = await mcp__firecrawl_scrape(
                   url=url,
                   formats=["markdown"],
                   onlyMainContent=True
               )

               results.append({
                   'url': url,
                   'content': response.get('markdown', ''),
                   'title': response.get('metadata', {}).get('title', ''),
                   'timestamp': time.time()
               })

           return results
       except Exception as e:
           print(f"Fire Crawl error: {e}")
           return []

   async def _call_tavily(self, query: str, max_results: int = 10) -> List[Dict]:
       """Call Tavily MCP for web search"""
       try:
           response = await mcp__tavily_search(
               query=query,
               max_results=max_results,
               search_depth="advanced",
               include_raw_content=True
           )

           results = []
           for item in response.get('results', []):
               results.append({
                   'title': item.get('title', ''),
                   'url': item.get('url', ''),
                   'snippet': item.get('snippet', ''),
                   'content': item.get('raw_content', ''),
                   'score': item.get('score', 0.5)
               })

           return results
       except Exception as e:
           print(f"Tavily error: {e}")
           return []
   ```

**GATE 2 CRITERIA (7 total)**:
7. [ ] Fire Crawl MCP accessible: `mcp-find firecrawl` returns results
8. [ ] Tavily MCP accessible: `mcp-find tavily` returns results
9. [ ] _call_firecrawl() returns real content
10. [ ] _call_tavily() returns search results
11. [ ] Error handling for MCP failures
12. [ ] Integration tests pass (if MCPs available)
13. [ ] Graceful degradation if MCPs unavailable

**Write to Serena**: `AGENT4_GATE2_PASS`

**Phase 3: CLI Command (GATE 3)**

1. **Add Command** to `src/shannon/cli/commands.py`:
   ```python
   @cli.command('research')
   @click.argument('query')
   @click.option('--urls', '-u', multiple=True, help='Specific URLs to scrape')
   @click.option('--dashboard', is_flag=True, help='Show in dashboard')
   @click.option('--max-results', default=10, help='Max web search results')
   def research_command(query, urls, dashboard, max_results):
       """Research a topic using Fire Crawl and web search"""
       from shannon.research.orchestrator import ResearchOrchestrator
       from rich.console import Console

       console = Console()

       console.print(f"[bold cyan]Researching:[/bold cyan] {query}")

       orchestrator = ResearchOrchestrator()
       results = asyncio.run(
           orchestrator.gather_knowledge(
               query=query,
               urls=list(urls) if urls else None
           )
       )

       # Display results
       console.print(f"\n[bold green]Sources gathered:[/bold green] {results['source_count']}")
       console.print(f"[bold green]Insights extracted:[/bold green] {len(results['insights'])}")
       console.print(f"\n{results['summary']}")
       console.print(f"\n[dim]Results saved to: {results['output_path']}[/dim]")
   ```

2. **CLI Tests**: `tests/cli/test_research_command.py`
   ```python
   from click.testing import CliRunner
   from shannon.cli.commands import cli

   def test_research_command_help():
       """Test research command help"""
       runner = CliRunner()
       result = runner.invoke(cli, ['research', '--help'])

       assert result.exit_code == 0
       assert 'Research a topic' in result.output

   def test_research_command_basic(monkeypatch):
       """Test basic research command execution"""
       # Mock MCP calls to avoid external dependencies
       async def mock_gather(query, urls=None):
           return {
               'query': query,
               'insights': [
                   {'text': 'Test insight', 'score': 0.9}
               ],
               'source_count': 5,
               'output_path': '/tmp/test.json',
               'summary': 'Test summary'
           }

       # Inject mock
       from shannon.research import orchestrator
       monkeypatch.setattr(
           orchestrator.ResearchOrchestrator,
           'gather_knowledge',
           mock_gather
       )

       runner = CliRunner()
       result = runner.invoke(cli, ['research', 'test query'])

       assert result.exit_code == 0
       assert 'Researching' in result.output
   ```

**GATE 3 CRITERIA (6 total)**:
14. [ ] `shannon research --help` shows usage
15. [ ] `shannon research "query"` executes
16. [ ] Terminal shows "Researching: {query}"
17. [ ] Terminal shows source count
18. [ ] Terminal displays summary
19. [ ] .shannon/research/ directory created with results

**Write to Serena**: `AGENT4_GATE3_PASS`

**Phase 4: E2E Validation (GATE 4)**

1. **Manual E2E Test**:
   ```bash
   # Test with real MCPs
   shannon research "React Server Components" --urls https://react.dev
   ```

2. **Validation Checklist**:
   - Terminal output clean and informative
   - Results file created with valid JSON
   - Insights are relevant to query
   - No duplicate insights
   - Proper error handling if MCPs unavailable

**GATE 4 CRITERIA (6 total)**:
20. [ ] End-to-end test completes successfully
21. [ ] Insights are relevant (manual review)
22. [ ] No duplicate insights in results
23. [ ] JSON output is well-formed
24. [ ] Works with and without --urls flag
25. [ ] Graceful error messages if MCPs unavailable

**Write to Serena**: `AGENT4_GATE4_PASS`

#### FINAL AGENT 4 VALIDATION (25 Total Criteria)

**Backend Unit Tests (6)**:
1-6. [As defined in GATE 1]

**MCP Integration (7)**:
7-13. [As defined in GATE 2]

**CLI Command (6)**:
14-19. [As defined in GATE 3]

**E2E Validation (6)**:
20-25. [As defined in GATE 4]

**Final Commit**:
```bash
git add .
git commit -m "Agent 4 COMPLETE: Research Orchestration - 25/25 criteria validated

GATES PASSED:
- Gate 1: Backend Unit Tests (6/6)
- Gate 2: MCP Integration (7/7)
- Gate 3: CLI Command (6/6)
- Gate 4: E2E Validation (6/6)

Evidence: .shannon/research/ results
Branch: agent4-research"
```

**Write to Serena**: `AGENT4_COMPLETE`

**AGENT 4 COMPLETE**: 25/25 pass

---

### AGENT 5: Ultrathink Engine (Backend + CLI)


**Skill Invocation**:
```
Use test-driven-development
Use sitrep-reporting
Use verification-before-completion
```

**Mission**: 500+ step reasoning using Sequential MCP with hypothesis generation

**Duration**: 3-4 hours
**Branch**: `agent5-ultrathink`
**File Ownership**:
- **Owned**: `src/shannon/modes/ultrathink.py` (create new)
- **Owned**: `src/shannon/modes/hypothesis_generator.py` (create new)
- **Shared**: `src/shannon/cli/commands.py` (add ultrathink command)
- **Owned**: `dashboard/src/panels/Ultrathink.tsx` (create new if dashboard support)

### Serena Protocol

**READS (Required Context)**:
1. `WAVE1_CODEBASE_STATE` - Baseline from Batch 1

**WRITES (Progress Tracking)**:
1. `AGENT5_GATE1_PASS` - Backend unit tests passing
2. `AGENT5_GATE2_PASS` - Sequential MCP integration working
3. `AGENT5_GATE3_PASS` - CLI command functional
4. `AGENT5_GATE4_PASS` - E2E validation complete
5. `AGENT5_COMPLETE` - All 25 criteria validated

### TDD Implementation

**Phase 1: Backend Unit Tests (GATE 1)**

1. **Test File**: `tests/modes/test_ultrathink.py`
   ```python
   import pytest
   from shannon.modes.ultrathink import UltrathinkEngine, UltrathinkResult
   from shannon.modes.hypothesis_generator import HypothesisGenerator

   def test_engine_initialization():
       """Verify engine initializes correctly"""
       engine = UltrathinkEngine()
       assert engine is not None
       assert hasattr(engine, 'analyze')

   @pytest.mark.asyncio
   async def test_thought_generation_mock():
       """Test thought generation with mocked MCP"""
       engine = UltrathinkEngine()

       # Mock sequential thinking
       async def mock_sequential(thought, thoughtNumber, totalThoughts, nextThoughtNeeded):
           return {
               'thought': thought,
               'thoughtNumber': thoughtNumber,
               'insights': ['Test insight']
           }

       engine._call_sequential_mcp = mock_sequential

       result = await engine.analyze("test task", max_thoughts=10)

       assert len(result.thoughts) == 10
       assert result.thoughts[0]['thoughtNumber'] == 1
       assert result.thoughts[9]['thoughtNumber'] == 10

   def test_hypothesis_generation():
       """Test hypothesis generation from thoughts"""
       generator = HypothesisGenerator()

       thoughts = [
           {'thought': 'Database indexing improves performance', 'thoughtNumber': 1},
           {'thought': 'Caching reduces database load', 'thoughtNumber': 2},
           {'thought': 'Async processing enables scalability', 'thoughtNumber': 3}
       ] * 50  # Simulate 150 thoughts

       hypotheses = generator.generate_hypotheses(thoughts)

       assert len(hypotheses) >= 3
       assert len(hypotheses) <= 5
       assert all('title' in h for h in hypotheses)
       assert all('description' in h for h in hypotheses)
       assert all('confidence' in h for h in hypotheses)

   def test_hypothesis_comparison():
       """Test hypothesis comparison matrix"""
       generator = HypothesisGenerator()

       hypotheses = [
           {'title': 'Approach A', 'confidence': 0.85, 'complexity': 'low'},
           {'title': 'Approach B', 'confidence': 0.92, 'complexity': 'medium'},
           {'title': 'Approach C', 'confidence': 0.78, 'complexity': 'high'}
       ]

       comparison = generator.compare_hypotheses(hypotheses)

       assert 'best' in comparison
       assert 'matrix' in comparison
       assert comparison['best'] == 'Approach B'  # Highest confidence
   ```

2. **Implementation**:

   `src/shannon/modes/hypothesis_generator.py`:
   ```python
   from typing import List, Dict
   from dataclasses import dataclass

   @dataclass
   class Hypothesis:
       title: str
       description: str
       confidence: float
       supporting_thoughts: List[int]
       complexity: str  # low, medium, high

   class HypothesisGenerator:
       def generate_hypotheses(
           self,
           thoughts: List[Dict],
           max_hypotheses: int = 5
       ) -> List[Dict]:
           """Generate hypotheses from thought stream"""
           # Group thoughts by theme
           themes = self._extract_themes(thoughts)

           hypotheses = []
           for theme, theme_thoughts in list(themes.items())[:max_hypotheses]:
               hypotheses.append({
                   'title': f"Approach: {theme}",
                   'description': self._synthesize_description(theme_thoughts),
                   'confidence': self._calculate_confidence(theme_thoughts),
                   'supporting_thoughts': [t['thoughtNumber'] for t in theme_thoughts],
                   'complexity': self._estimate_complexity(theme_thoughts)
               })

           return hypotheses

       def _extract_themes(self, thoughts: List[Dict]) -> Dict[str, List[Dict]]:
           """Extract major themes from thoughts"""
           # Simplified - group by keywords
           themes = {}

           for thought in thoughts:
               text = thought.get('thought', '').lower()

               # Simple keyword-based grouping
               if 'database' in text or 'query' in text:
                   themes.setdefault('Database Optimization', []).append(thought)
               elif 'cache' in text or 'memory' in text:
                   themes.setdefault('Caching Strategy', []).append(thought)
               elif 'async' in text or 'parallel' in text:
                   themes.setdefault('Async Processing', []).append(thought)
               else:
                   themes.setdefault('General', []).append(thought)

           return themes

       def _synthesize_description(self, thoughts: List[Dict]) -> str:
           """Create description from thoughts"""
           # Take first few thoughts as description
           snippets = [t.get('thought', '')[:100] for t in thoughts[:3]]
           return ' | '.join(snippets)

       def _calculate_confidence(self, thoughts: List[Dict]) -> float:
           """Calculate confidence based on thought coherence"""
           # Simplified - based on count
           count = len(thoughts)
           return min(0.95, 0.5 + (count * 0.01))

       def _estimate_complexity(self, thoughts: List[Dict]) -> str:
           """Estimate implementation complexity"""
           if len(thoughts) < 30:
               return 'low'
           elif len(thoughts) < 60:
               return 'medium'
           else:
               return 'high'

       def compare_hypotheses(self, hypotheses: List[Dict]) -> Dict:
           """Compare hypotheses and select best"""
           # Sort by confidence
           sorted_hyp = sorted(hypotheses, key=lambda h: h['confidence'], reverse=True)

           # Create comparison matrix
           matrix = []
           for h1 in sorted_hyp:
               row = {
                   'hypothesis': h1['title'],
                   'confidence': h1['confidence'],
                   'complexity': h1['complexity'],
                   'rank': sorted_hyp.index(h1) + 1
               }
               matrix.append(row)

           return {
               'best': sorted_hyp[0]['title'],
               'matrix': matrix,
               'reasoning': f"Selected {sorted_hyp[0]['title']} with {sorted_hyp[0]['confidence']:.0%} confidence"
           }
   ```

   `src/shannon/modes/ultrathink.py`:
   ```python
   from dataclasses import dataclass
   from typing import List, Dict
   import asyncio
   import time
   from pathlib import Path
   import json

   from shannon.modes.hypothesis_generator import HypothesisGenerator

   @dataclass
   class UltrathinkResult:
       thoughts: List[Dict]
       hypotheses: List[Dict]
       comparison: Dict
       recommendation: str
       duration: float

   class UltrathinkEngine:
       def __init__(self, dashboard_client=None):
           self.dashboard_client = dashboard_client
           self.generator = HypothesisGenerator()

       async def _call_sequential_mcp(
           self,
           thought: str,
           thoughtNumber: int,
           totalThoughts: int,
           nextThoughtNeeded: bool
       ) -> Dict:
           """Call Sequential MCP for thought generation"""
           # This will be implemented in Gate 2
           return {
               'thought': thought,
               'thoughtNumber': thoughtNumber,
               'insights': []
           }

       async def analyze(
           self,
           task: str,
           max_thoughts: int = 500
       ) -> UltrathinkResult:
           """Perform deep analysis with 500+ thoughts"""
           start_time = time.time()
           thoughts = []

           for thought_num in range(1, max_thoughts + 1):
               # Generate thought prompt
               thought_prompt = self._generate_thought_prompt(task, thoughts, thought_num)

               # Call sequential MCP
               result = await self._call_sequential_mcp(
                   thought=thought_prompt,
                   thoughtNumber=thought_num,
                   totalThoughts=max_thoughts,
                   nextThoughtNeeded=(thought_num < max_thoughts)
               )

               thoughts.append(result)

               # Emit progress
               if thought_num % 100 == 0 and self.dashboard_client:
                   await self.dashboard_client.emit_event('ultrathink:progress', {
                       'current': thought_num,
                       'total': max_thoughts,
                       'percentage': (thought_num / max_thoughts) * 100
                   })

           # Generate hypotheses
           hypotheses = self.generator.generate_hypotheses(thoughts)

           # Compare hypotheses
           comparison = self.generator.compare_hypotheses(hypotheses)

           # Save results
           self._save_results(task, thoughts, hypotheses, comparison)

           duration = time.time() - start_time

           return UltrathinkResult(
               thoughts=thoughts,
               hypotheses=hypotheses,
               comparison=comparison,
               recommendation=comparison['best'],
               duration=duration
           )

       def _generate_thought_prompt(
           self,
           task: str,
           previous_thoughts: List[Dict],
           thought_num: int
       ) -> str:
           """Generate prompt for next thought"""
           if thought_num == 1:
               return f"THOUGHT 1: Analyze the task: {task}"
           elif thought_num <= 100:
               return f"THOUGHT {thought_num}: Explore different aspects and approaches for: {task}"
           elif thought_num <= 300:
               return f"THOUGHT {thought_num}: Evaluate pros/cons and implications for: {task}"
           else:
               return f"THOUGHT {thought_num}: Synthesize insights and formulate recommendations for: {task}"

       def _save_results(
           self,
           task: str,
           thoughts: List[Dict],
           hypotheses: List[Dict],
           comparison: Dict
       ):
           """Save ultrathink results to disk"""
           output_dir = Path.cwd() / '.shannon' / 'ultrathink'
           output_dir.mkdir(parents=True, exist_ok=True)

           timestamp = int(time.time())
           safe_task = task.replace(' ', '_')[:50]
           filename = f"{safe_task}_{timestamp}.json"

           data = {
               'task': task,
               'timestamp': timestamp,
               'thoughts': thoughts,
               'hypotheses': hypotheses,
               'comparison': comparison
           }

           with open(output_dir / filename, 'w') as f:
               json.dump(data, f, indent=2)
   ```

**GATE 1 CRITERIA (6 total)**:
1. [ ] `test_engine_initialization` - PASS
2. [ ] `test_thought_generation_mock` - PASS
3. [ ] `test_hypothesis_generation` - PASS
4. [ ] `test_hypothesis_comparison` - PASS
5. [ ] All classes implemented
6. [ ] pytest: 4/4 passing

**Write to Serena**: `AGENT5_GATE1_PASS`

**Phase 2: Sequential MCP Integration (GATE 2)**

1. **Implement Real MCP Call**:
   ```python
   async def _call_sequential_mcp(
       self,
       thought: str,
       thoughtNumber: int,
       totalThoughts: int,
       nextThoughtNeeded: bool
   ) -> Dict:
       """Call Sequential MCP for thought generation"""
       try:
           result = await mcp__sequential_thinking__sequentialthinking(
               thought=thought,
               thoughtNumber=thoughtNumber,
               totalThoughts=totalThoughts,
               nextThoughtNeeded=nextThoughtNeeded
           )
           return result
       except Exception as e:
           print(f"Sequential MCP error: {e}")
           return {
               'thought': thought,
               'thoughtNumber': thoughtNumber,
               'insights': []
           }
   ```

**GATE 2 CRITERIA (7 total)**:
7. [ ] Sequential MCP accessible: `mcp-find sequential` returns results
8. [ ] _call_sequential_mcp() returns real results
9. [ ] 500 thoughts generated successfully
10. [ ] Progress events emitted every 100 thoughts
11. [ ] Error handling for MCP failures
12. [ ] Results saved to .shannon/ultrathink/
13. [ ] Performance: 500 thoughts in 5-15 minutes

**Write to Serena**: `AGENT5_GATE2_PASS`

**Phase 3: CLI Command (GATE 3)**

1. **Add Command** to `src/shannon/cli/commands.py`:
   ```python
   @cli.command('ultrathink')
   @click.argument('task')
   @click.option('--dashboard', is_flag=True)
   @click.option('--max-thoughts', default=500, type=int)
   def ultrathink_command(task, dashboard, max_thoughts):
       """Deep analysis with 500+ reasoning steps"""
       from shannon.modes.ultrathink import UltrathinkEngine
       from rich.console import Console
       from rich.progress import Progress

       console = Console()

       console.print(f"[bold cyan]ULTRATHINK MODE:[/bold cyan] {task}")
       console.print(f"[dim]Generating {max_thoughts} thoughts...[/dim]")

       engine = UltrathinkEngine()

       with Progress() as progress:
           task_id = progress.add_task("[cyan]Thinking...", total=max_thoughts)

           # Run analysis (simplified - no real-time progress)
           result = asyncio.run(engine.analyze(task, max_thoughts))

           progress.update(task_id, completed=max_thoughts)

       # Display results
       console.print(f"\n[bold green]Analysis Complete[/bold green]")
       console.print(f"[green]Duration:[/green] {result.duration:.1f}s")
       console.print(f"\n[bold]Hypotheses Generated:[/bold] {len(result.hypotheses)}")

       for i, hyp in enumerate(result.hypotheses, 1):
           console.print(f"\n{i}. {hyp['title']} ({hyp['confidence']:.0%} confidence)")
           console.print(f"   {hyp['description'][:100]}...")

       console.print(f"\n[bold yellow]Recommendation:[/bold yellow] {result.recommendation}")
   ```

**GATE 3 CRITERIA (6 total)**:
14. [ ] `shannon ultrathink --help` shows usage
15. [ ] `shannon ultrathink "task"` executes
16. [ ] Terminal shows "ULTRATHINK MODE"
17. [ ] Progress bar visible
18. [ ] Hypotheses displayed
19. [ ] Recommendation shown

**Write to Serena**: `AGENT5_GATE3_PASS`

**Phase 4: E2E Validation (GATE 4)**

**GATE 4 CRITERIA (6 total)**:
20. [ ] End-to-end test with real Sequential MCP
21. [ ] 500 thoughts generated
22. [ ] 3-5 hypotheses created
23. [ ] Best hypothesis selected
24. [ ] Results saved and well-formed
25. [ ] Reasoning is coherent (manual review)

**Write to Serena**: `AGENT5_GATE4_PASS`

### Final Agent 5 Validation (25 Total Criteria)

**Final Commit**:
```bash
git commit -m "Agent 5 COMPLETE: Ultrathink Engine - 25/25

GATES: Backend (6/6), MCP (7/7), CLI (6/6), E2E (6/6)
Branch: agent5-ultrathink"
```

**Write to Serena**: `AGENT5_COMPLETE`

**AGENT 5 COMPLETE**: 25/25 pass

---

### AGENT 6: Basic Interactive Controls (Backend + Frontend)

**Mission**: HALT, RESUME, ROLLBACK controls with <100ms latency

**Duration**: 4-5 hours
**Branch**: `agent6-controls`
**File Ownership**:
- **Shared**: `src/shannon/orchestration/orchestrator.py` (with Agents 2, 3)
- **Owned**: `src/shannon/orchestration/state_manager.py` (create new)
- **Shared**: `src/shannon/server/websocket.py` (with Agent 3)
- **Shared**: `dashboard/src/store/dashboardStore.ts` (with Agents 2, 3, 7)
- **Shared**: `dashboard/src/panels/ExecutionOverview.tsx` (add controls)

### Serena Protocol

**READS**:
1. `WAVE1_CODEBASE_STATE`
2. `AGENT2_COMPLETE` - Agent pool for pausing agents
3. `AGENT3_COMPLETE` - Decision engine for state tracking

**WRITES**:
1. `AGENT6_GATE1_PASS` - Backend unit tests
2. `AGENT6_GATE2_PASS` - State management
3. `AGENT6_GATE3_PASS` - Frontend controls
4. `AGENT6_GATE4_PASS` - Latency validation (<100ms)
5. `AGENT6_COMPLETE`

### TDD Implementation

**Phase 1: Backend Unit Tests (GATE 1)**

1. **Tests**: `tests/orchestration/test_controls.py`
   ```python
   import pytest
   from shannon.orchestration.orchestrator import Orchestrator
   from shannon.orchestration.state_manager import StateManager

   @pytest.mark.asyncio
   async def test_halt_flag_pauses():
       """Halt flag pauses execution"""
       orch = Orchestrator()
       orch.halt_requested = True

       # Simulate step execution
       can_continue = await orch._check_can_continue()
       assert not can_continue

   @pytest.mark.asyncio
   async def test_resume_clears_halt():
       """Resume clears halt flag"""
       orch = Orchestrator()
       orch.halt_requested = True

       await orch.resume()
       assert not orch.halt_requested

   @pytest.mark.asyncio
   async def test_state_snapshot():
       """State manager creates snapshots"""
       mgr = StateManager()
       state = {'step': 5, 'files': ['a.py', 'b.py']}

       mgr.create_snapshot(5, state)
       assert mgr.has_snapshot(5)

   @pytest.mark.asyncio
   async def test_rollback_restores_state():
       """Rollback restores to previous snapshot"""
       mgr = StateManager()

       # Create snapshots
       mgr.create_snapshot(1, {'step': 1})
       mgr.create_snapshot(2, {'step': 2})
       mgr.create_snapshot(3, {'step': 3})

       # Rollback to step 1
       restored = mgr.rollback_to(1)
       assert restored['step'] == 1
   ```

2. **Implementation**:

   `src/shannon/orchestration/state_manager.py`:
   ```python
   from typing import Dict, Optional
   from dataclasses import dataclass
   import subprocess

   @dataclass
   class ExecutionSnapshot:
       step_number: int
       git_commit: str
       state_data: Dict

   class StateManager:
       def __init__(self, project_root: str):
           self.project_root = project_root
           self.snapshots: Dict[int, ExecutionSnapshot] = {}

       def create_snapshot(self, step_number: int, state_data: Dict):
           """Create snapshot before step execution"""
           # Get current git commit
           result = subprocess.run(
               ['git', 'rev-parse', 'HEAD'],
               cwd=self.project_root,
               capture_output=True,
               text=True
           )
           git_commit = result.stdout.strip()

           snapshot = ExecutionSnapshot(
               step_number=step_number,
               git_commit=git_commit,
               state_data=state_data
           )

           self.snapshots[step_number] = snapshot

       def has_snapshot(self, step_number: int) -> bool:
           """Check if snapshot exists"""
           return step_number in self.snapshots

       def rollback_to(self, step_number: int) -> Dict:
           """Rollback to specific step"""
           if step_number not in self.snapshots:
               raise ValueError(f"No snapshot for step {step_number}")

           snapshot = self.snapshots[step_number]

           # Revert git changes
           subprocess.run(
               ['git', 'reset', '--hard', snapshot.git_commit],
               cwd=self.project_root,
               check=True
           )

           # Clean untracked files
           subprocess.run(
               ['git', 'clean', '-fd'],
               cwd=self.project_root,
               check=True
           )

           return snapshot.state_data
   ```

   Update `src/shannon/orchestration/orchestrator.py`:
   ```python
   from shannon.orchestration.state_manager import StateManager

   class Orchestrator:
       def __init__(self, ...):
           # Existing code
           self.halt_requested = False
           self.state_manager = StateManager(self.project_root)

       async def _check_can_continue(self) -> bool:
           """Check if execution can continue"""
           if self.halt_requested:
               return False
           return True

       async def halt(self):
           """Halt execution"""
           self.halt_requested = True
           await self.emit('execution:halted', {
               'timestamp': time.time()
           })

       async def resume(self):
           """Resume execution"""
           self.halt_requested = False
           await self.emit('execution:resumed', {
               'timestamp': time.time()
           })

       async def rollback(self, n_steps: int):
           """Rollback N steps"""
           current_step = self.current_step
           target_step = current_step - n_steps

           state = self.state_manager.rollback_to(target_step)

           self.current_step = target_step

           await self.emit('execution:rolledback', {
               'from_step': current_step,
               'to_step': target_step
           })
   ```

**GATE 1 CRITERIA (10 total)**:
1. [ ] test_halt_flag_pauses - PASS
2. [ ] test_resume_clears_halt - PASS
3. [ ] test_state_snapshot - PASS
4. [ ] test_rollback_restores_state - PASS
5. [ ] StateManager class implemented
6. [ ] Orchestrator.halt() method
7. [ ] Orchestrator.resume() method
8. [ ] Orchestrator.rollback() method
9. [ ] Git integration working
10. [ ] pytest: 4/4 passing

**Write to Serena**: `AGENT6_GATE1_PASS`

**Phase 2: WebSocket Handlers (GATE 2)**

1. **Update** `src/shannon/server/websocket.py`:
   ```python
   @sio.event
   async def halt_execution(sid, data):
       """Halt current execution"""
       orch = get_current_orchestrator()
       await orch.halt()

   @sio.event
   async def resume_execution(sid, data):
       """Resume halted execution"""
       orch = get_current_orchestrator()
       await orch.resume()

   @sio.event
   async def rollback_execution(sid, data):
       """Rollback N steps"""
       n_steps = data['n_steps']
       orch = get_current_orchestrator()
       await orch.rollback(n_steps)
   ```

**GATE 2 CRITERIA (10 total)**:
11. [ ] halt_execution handler exists
12. [ ] resume_execution handler exists
13. [ ] rollback_execution handler exists
14. [ ] Handlers call orchestrator methods
15. [ ] Events emitted correctly
16. [ ] Error handling for invalid requests
17. [ ] Multiple halt/resume cycles work
18. [ ] Rollback validates step number
19. [ ] WebSocket integration tests pass
20. [ ] Backend ready for frontend

**Write to Serena**: `AGENT6_GATE2_PASS`

**Phase 3: Frontend Controls (GATE 3)**

1. **Update Store** `dashboard/src/store/dashboardStore.ts`:
   ```typescript
   interface DashboardState {
     executionStatus: 'idle' | 'running' | 'halted' | 'completed';
     currentStep: number;

     haltExecution: () => void;
     resumeExecution: () => void;
     rollbackExecution: (nSteps: number) => void;
   }

   export const useDashboardStore = create<DashboardState>((set, get) => ({
     executionStatus: 'idle',
     currentStep: 0,

     haltExecution: () => {
       const socket = get().socket;
       if (!socket) return;

       socket.emit('halt_execution', {});
       set({ executionStatus: 'halted' });
     },

     resumeExecution: () => {
       const socket = get().socket;
       if (!socket) return;

       socket.emit('resume_execution', {});
       set({ executionStatus: 'running' });
     },

     rollbackExecution: (nSteps: number) => {
       const socket = get().socket;
       if (!socket) return;

       socket.emit('rollback_execution', { n_steps: nSteps });
     },

     handleSocketEvent: (event, data) => {
       // Existing handlers...

       switch (event) {
         case 'execution:halted':
           set({ executionStatus: 'halted' });
           break;

         case 'execution:resumed':
           set({ executionStatus: 'running' });
           break;

         case 'execution:rolledback':
           set({ currentStep: data.to_step });
           break;
       }
     }
   }));
   ```

2. **Update Component** `dashboard/src/panels/ExecutionOverview.tsx`:
   ```typescript
   export function ExecutionOverview() {
     const status = useDashboardStore((state) => state.executionStatus);
     const currentStep = useDashboardStore((state) => state.currentStep);
     const haltExecution = useDashboardStore((state) => state.haltExecution);
     const resumeExecution = useDashboardStore((state) => state.resumeExecution);
     const rollbackExecution = useDashboardStore((state) => state.rollbackExecution);

     const [rollbackSteps, setRollbackSteps] = useState(5);

     return (
       <div className="p-4">
         <div className="mb-4">
           <span className={`
             px-3 py-1 rounded-full text-sm font-semibold
             ${status === 'running' ? 'bg-green-900/20 text-green-400' :
               status === 'halted' ? 'bg-yellow-900/20 text-yellow-400' :
               'bg-gray-900/20 text-gray-400'}
           `}>
             {status.toUpperCase()}
           </span>
           <span className="ml-3 text-gray-400">Step {currentStep}</span>
         </div>

         <div className="flex gap-2">
           <button
             data-testid="halt-button"
             onClick={haltExecution}
             disabled={status !== 'running'}
             className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:text-gray-500 rounded"
           >
             HALT
           </button>

           <button
             data-testid="resume-button"
             onClick={resumeExecution}
             disabled={status !== 'halted'}
             className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:text-gray-500 rounded"
           >
             RESUME
           </button>

           <div className="flex gap-2 items-center ml-4">
             <input
               data-testid="rollback-steps"
               type="number"
               value={rollbackSteps}
               onChange={(e) => setRollbackSteps(Number(e.target.value))}
               className="w-20 px-2 py-1 bg-gray-800 border border-gray-600 rounded"
               min="1"
             />
             <button
               data-testid="rollback-button"
               onClick={() => rollbackExecution(rollbackSteps)}
               disabled={status !== 'halted'}
               className="px-4 py-2 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-700 disabled:text-gray-500 rounded"
             >
               ROLLBACK
             </button>
           </div>
         </div>
       </div>
     );
   }
   ```

**GATE 3 CRITERIA (10 total)**:
21. [ ] Store has executionStatus state
22. [ ] haltExecution() emits event
23. [ ] resumeExecution() emits event
24. [ ] rollbackExecution() emits event
25. [ ] ExecutionOverview renders controls
26. [ ] HALT button enabled when running
27. [ ] RESUME button enabled when halted
28. [ ] ROLLBACK input accepts numbers
29. [ ] Status indicator updates correctly
30. [ ] Component styling matches design

**Write to Serena**: `AGENT6_GATE3_PASS`

**Phase 4: Latency Validation (GATE 4)**

1. **Playwright Test** `tests/e2e/test_agent6_controls.py`:
   ```python
   import time

   def test_halt_latency(page: Page):
       """HALT response time < 100ms"""
       # Start execution
       # ...

       page.goto("http://localhost:5175")
       page.wait_for("text=Running")

       # Measure HALT latency
       t1 = time.time()
       page.click("button[data-testid='halt-button']")
       page.wait_for("text=Halted")
       t2 = time.time()

       latency_ms = (t2 - t1) * 1000

       assert latency_ms < 100, f"HALT latency {latency_ms}ms exceeds 100ms"

   def test_resume_latency(page: Page):
       """RESUME response time < 100ms"""
       # Similar test

   def test_rollback_functionality(page: Page):
       """ROLLBACK restores state correctly"""
       # Wait for step 7
       page.wait_for("text=Step 7")

       # Halt
       page.click("button[data-testid='halt-button']")
       page.wait_for("text=Halted")

       # Rollback 5 steps
       page.fill("input[data-testid='rollback-steps']", "5")
       page.click("button[data-testid='rollback-button']")

       # Should be at step 2
       page.wait_for("text=Step 2", timeout=5000)

       page.screenshot(path="agent6-controls-validated.png")
   ```

**GATE 4 CRITERIA (10 total)**:
31. [ ] HALT latency < 100ms (measured)
32. [ ] RESUME latency < 100ms (measured)
33. [ ] 10× HALT/RESUME cycles all < 100ms
34. [ ] Average latency < 50ms
35. [ ] ROLLBACK correctly reverts files
36. [ ] ROLLBACK restores execution state
37. [ ] UI updates immediately
38. [ ] No race conditions
39. [ ] Playwright tests pass
40. [ ] Screenshot evidence committed

**Write to Serena**: `AGENT6_GATE4_PASS`

### Final Agent 6 Validation (40 Total Criteria)

**Final Commit**:
```bash
git commit -m "Agent 6 COMPLETE: Basic Controls - 40/40

GATES: Backend (10/10), WebSocket (10/10), Frontend (10/10), Latency (10/10)
<100ms response verified
Branch: agent6-controls"
```

**Write to Serena**: `AGENT6_COMPLETE`

**AGENT 6 COMPLETE**: 40/40 pass

---

## WAVE 2: AGENT 7 - Advanced Interactive Controls

**Mission**: REDIRECT, INJECT, APPROVE/OVERRIDE controls functional

**Duration**: 3-4 hours
**Branch**: `agent7-advanced-controls`

### Complete 4-Gate Implementation

[Following same pattern as previous agents - Backend, Integration, Frontend, E2E]

**GATE 1: Backend Unit Tests (8 criteria)**
**GATE 2: Integration (8 criteria)**
**GATE 3: Frontend (7 criteria)**
**GATE 4: E2E Playwright (8 criteria)**

**AGENT 7 COMPLETE**: 31/31 pass

---

## WAVE 2: AGENT 8 - FileDiff Panel

**Mission**: File changes displayed with syntax-highlighted diffs

**Duration**: 2-3 hours
**Branch**: `agent8-filediff`

### Complete 4-Gate Implementation

**GATE 1: Backend Events (4 criteria)**
**GATE 2: Diff Generation (4 criteria)**
**GATE 3: Frontend Panel (5 criteria)**
**GATE 4: E2E Validation (4 criteria)**

**AGENT 8 COMPLETE**: 17/17 pass

---

## MY ORCHESTRATION PROTOCOL (Meta-Level Coordination)

### My Role as Orchestrator

I coordinate the 8 parallel agents, monitor progress via Serena, resolve conflicts, and ensure Wave 1 → Wave 2 → Integration flows smoothly.

### SITREP Monitoring Schedule

**Every 15 minutes**:
```bash
# Check all agents' progress
serena list-memories | grep "AGENT[1-8]_GATE"

# Read latest SITREPs
serena read-memory AGENT1_SITREP_LATEST
serena read-memory AGENT2_SITREP_LATEST
# ... for all active agents
```

**SITREP Content I Expect from Each Agent**:
```markdown
# AGENT{N}_SITREP_{TIMESTAMP}

Current Gate: Gate {X}
Criteria: {Y}/{Z} passing
Phase: {Backend/Integration/Frontend/E2E}
Blockers: {None | Description}
ETA to Gate Complete: {X} minutes
Next Steps: {Brief description}

Progress Details:
- Tests written: {count}
- Tests passing: {count}
- Implementation complete: {%}
```

### Conflict Detection Protocol

**Shared Files to Monitor**:
1. `orchestrator.py` - Agents 2, 3, 6
2. `websocket.py` - Agents 3, 6, 7
3. `dashboardStore.ts` - Agents 2, 3, 6, 7
4. `commands.py` - Agents 4, 5

**Detection Strategy**:
```bash
# Every 30 minutes, check for merge conflicts
cd shannon-cli

for branch in agent{1..8}-*; do
    git checkout $branch 2>/dev/null || continue
    git merge main --no-commit --no-ff 2>&1 | grep "CONFLICT" && \
        echo "CONFLICT in $branch" >> /tmp/conflicts.log
    git merge --abort 2>/dev/null
done

git checkout main
```

**Conflict Resolution**:
1. Identify conflicting agents
2. Review Serena memories for both agents' changes
3. Create resolution plan:
   - Option A: Agent waits for other to finish
   - Option B: Coordinate on shared sections
   - Option C: Refactor to eliminate conflict
4. Write resolution to Serena: `CONFLICT_RESOLUTION_{AGENT_X}_vs_{AGENT_Y}`

### Merge Coordination

**Wave 1 Completion Trigger**:
```
WHEN:
  AGENT1_COMPLETE exists AND
  AGENT2_COMPLETE exists AND
  AGENT3_COMPLETE exists AND
  AGENT4_COMPLETE exists AND
  AGENT5_COMPLETE exists AND
  AGENT6_COMPLETE exists
THEN:
  Initiate Wave 1 Merge
```

**Merge Order** (to minimize conflicts):
```
1. Agent 4 (Research) - independent
2. Agent 5 (Ultrathink) - independent
3. Agent 1 (Multi-File) - minimal dependencies
4. Agent 2 (Agent Pool) - orchestrator changes
5. Agent 3 (Decisions) - orchestrator + websocket
6. Agent 6 (Controls) - orchestrator + websocket + store

After each merge:
  - Run full test suite
  - Verify no regressions
  - Commit: "Merge: Agent {N} into main"
```

**Consolidated Validation Execution**:
```bash
# After all 6 agents merged
pytest --maxfail=1  # Stop on first failure
shannon do "integration test task 1" --dashboard
shannon do "integration test task 2" --dashboard
# ... through all 24 Wave 1 integration scenarios
```

### Communication Protocol

**To Agents** (via mission briefs):
- Clear gate definitions
- File ownership boundaries
- Serena read/write expectations
- SITREP schedule

**From Agents** (via Serena):
- Progress updates every 30min
- Gate completions immediately
- Blockers immediately
- Final completion with evidence

### My Decision Framework

**When to Intervene**:
1. Agent stuck for >1 hour (no SITREP updates)
2. Agent reports blocker
3. Conflict detected in shared files
4. Gate failure after 2 attempts
5. Timeline risk (>50% over estimate)

**When to NOT Intervene**:
1. Agent progressing normally
2. Minor delays (<20% over estimate)
3. Agent debugging expected failures
4. Between-gate planning time

### Validation Authority

I validate:
- All 205 Wave 1 criteria (via pytest + Playwright)
- All 51 Wave 2 criteria
- Integration scenarios (24 criteria)
- No regressions in existing features

Agents validate:
- Their own 20-40 criteria
- Gate-by-gate progression
- Evidence collection (screenshots, logs)

### Success Metrics

**Wave 1 Success**:
- 205/205 criteria passing
- All 6 agents merged to main
- pytest: 240+ tests passing
- Integration scenarios: 24/24 passing
- Timeline: ≤ 6 hours wall time

**Wave 2 Success**:
- 51/51 criteria passing
- Agents 7-8 merged to main
- pytest: 260+ tests passing
- Timeline: ≤ 4 hours wall time

**Overall Success**:
- 283/283 criteria passing
- V4.0 feature complete
- No regressions
- Timeline: ≤ 10 hours implementation
- Ready for integration testing

---

## EXECUTION CHECKLIST (For Orchestrator)

### Pre-Wave 1

- [ ] Batch 1 complete (27/27 validation streaming)
- [ ] Write WAVE1_CODEBASE_STATE to Serena
- [ ] Prepare 6 agent mission briefs
- [ ] Set up SITREP monitoring (15min cron)
- [ ] Set up conflict detection (30min cron)

### During Wave 1

- [ ] Monitor SITREPs every 15min
- [ ] Check for conflicts every 30min
- [ ] Respond to blocker reports within 10min
- [ ] Verify each gate completion
- [ ] Collect evidence (screenshots, logs)

### Wave 1 Completion

- [ ] All 6 AGENT{N}_COMPLETE exist in Serena
- [ ] Review all evidence
- [ ] Execute merge plan (order: 4,5,1,2,3,6)
- [ ] Run pytest after each merge
- [ ] Execute 24 integration scenarios
- [ ] Validate 205/205 criteria
- [ ] Write WAVE1_COMPLETE to Serena

### During Wave 2

- [ ] Same monitoring as Wave 1
- [ ] Agents 7-8 parallel execution
- [ ] Monitor shared file conflicts (dashboardStore)

### Wave 2 Completion

- [ ] All 51 criteria passing
- [ ] Merge agents 7-8
- [ ] Full regression suite
- [ ] Write WAVE2_COMPLETE

### Final

- [ ] 283/283 total criteria validated
- [ ] All evidence committed
- [ ] Create V4.0 tag
- [ ] Transition to integration testing

---

## TOTAL LINE COUNT: 3,500+

This plan is now COMPLETE with:
- Batch 1: Full detail (existing)
- Agents 1-2: Full 4-gate structure (existing)
- Agents 3-4: Full 4-gate structure (NEW)
- Agents 5-6: Full 4-gate structure (NEW)
- Agents 7-8: 4-gate outline (to be expanded during execution)
- Orchestration protocol: Complete

**Ready for execution.**
