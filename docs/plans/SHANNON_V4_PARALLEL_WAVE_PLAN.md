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

#### Implementation Tasks

**Backend**:
1. Enhance `src/shannon/orchestration/decision_engine.py`:
   - DecisionPoint dataclass (id, title, description, options[], recommended, confidence, status)
   - DecisionOption dataclass (id, label, description, pros[], cons[], confidence)
   - request_decision() method
   - Auto-approve if confidence >= 0.95
   - Emit decision:created for manual decisions
   - _wait_for_decision() polling loop (100ms intervals)

2. Update `src/shannon/server/websocket.py`:
   ```python
   @sio.event
   async def approve_decision(sid, data):
       decision_id = data['decision_id']
       option_id = data['option_id']

       # Notify orchestrator
       await sio.emit('decision:approved', {
           'decision_id': decision_id,
           'option_id': option_id
       })
   ```

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   ```typescript
   decisions: [] as DecisionPoint[],

   addDecision: (decision) => set((state) => ({
     decisions: [...state.decisions, decision]
   })),

   approveDecision: async (decisionId, optionId) => {
     const socket = get().socket;
     socket?.emit('approve_decision', {
       decision_id: decisionId,
       option_id: optionId
     });

     set((state) => ({
       decisions: state.decisions.map(d =>
         d.id === decisionId ? {...d, status: 'approved', selected_option: optionId} : d
       )
     }));
   },

   case 'decision:created':
     get().addDecision(data.data);
     break;
   ```

2. Update `dashboard/src/panels/Decisions.tsx`:
   - Render decision cards with yellow background
   - Display options with pros/cons (2-column grid)
   - Highlight recommended option (⭐)
   - Show confidence percentages
   - Enable approve button only when option selected
   - Handle click → approveDecision()

**Unit Tests** (TDD):
1. `tests/orchestration/test_decision_engine.py`:
   ```python
   @pytest.mark.asyncio
   async def test_auto_approve():
       engine = DecisionEngine()
       options = [DecisionOption(id='opt1', confidence=0.97, ...)]

       selected = await engine.request_decision(
           title="Test",
           options=options,
           recommended='opt1',
           auto_approve_threshold=0.95
       )

       assert selected.id == 'opt1'
       assert engine.pending_decisions == {}  # Not pending
   ```

2. Run: `pytest tests/orchestration/test_decision*.py -v`

#### AGENT 3 VALIDATION CRITERIA (34 total)

**Backend**:
1. [ ] DecisionPoint dataclass created with all fields
2. [ ] DecisionOption dataclass created
3. [ ] request_decision() auto-approves when confidence >= 0.95
4. [ ] request_decision() emits decision:created when confidence < 0.95
5. [ ] _wait_for_decision() polls every 100ms
6. [ ] approve_decision WebSocket handler works
7. [ ] pytest test_decision_engine.py: 3/3 PASS

**Frontend**:
8. [ ] Store handles decision:created
9. [ ] Store.approveDecision() emits correct event
10. [ ] Decisions component renders decision cards

**Integration - Manual Approval**:
11. [ ] Create test orchestrator with injected decision (confidence=0.70)
12. [ ] shannon do "decision test" --dashboard
13. [ ] Terminal shows: "Decision point: Select Approach"
14. [ ] Terminal shows: "Waiting for user approval..."
15. [ ] Execution PAUSED (doesn't continue on its own)
16. [ ] playwright.navigate("http://localhost:5175")
17. [ ] playwright.click("text=Decisions")
18. [ ] playwright.wait_for("text=Select Approach", timeout=10000)
19. [ ] options = playwright.evaluate("() => document.querySelectorAll('[data-testid=\"decision-option\"]').length")
20. [ ] options === 3 (shows 3 options)
21. [ ] playwright.wait_for("text=⭐ Recommended") - Recommended marked
22. [ ] playwright.wait_for("text=Pros:") - Pros visible
23. [ ] playwright.wait_for("text=Cons:") - Cons visible
24. [ ] playwright.click("[data-testid=\"decision-option-2\"]") - Select option 2 (NOT recommended)
25. [ ] Border turns blue (selected state)
26. [ ] playwright.click("text=Approve Selected Option")
27. [ ] playwright.wait_for("text=Decision approved")
28. [ ] Terminal shows: "Decision approved: opt2"
29. [ ] Execution RESUMES and uses option 2 approach
30. [ ] playwright.screenshot("agent3-decision-validated.png")

**Integration - Auto Approval**:
31. [ ] Test with confidence=0.97, threshold=0.95
32. [ ] Decision auto-approved (not shown in dashboard)
33. [ ] Execution continues immediately
34. [ ] Terminal shows: "Auto-approving (confidence: 0.97)"

**Regression**:
35. [ ] Batches 1-2 still work
36. [ ] pytest: All tests pass

**Evidence**:
37. [ ] Screenshot shows decision with 3 options
38. [ ] SITREP logs
39. [ ] Commit: "Agent 3 COMPLETE: Decisions - 34/34"

**AGENT 3 COMPLETE**: 34/34 pass

---

### AGENT 4: Research Orchestration

**Skill Invocation**:
```
Use test-driven-development
Use sitrep-reporting
Use verification-before-completion
```

**Mission**: shannon research gathers knowledge from Fire Crawl, Tavali, web search

**Duration**: 2-3 hours

#### Implementation Tasks

**Backend**:
1. Update `src/shannon/research/orchestrator.py`:
   - gather_from_firecrawl(query, urls)
   - gather_from_web(query) using tavily search
   - synthesize_knowledge(sources) - Combine + deduplicate
   - rank_by_relevance(insights)

2. Add CLI command `src/shannon/cli/commands.py`:
   ```python
   @cli.command('research')
   @click.argument('query')
   @click.option('--dashboard', is_flag=True)
   def research_command(query, dashboard):
       orchestrator = ResearchOrchestrator()
       results = asyncio.run(orchestrator.gather_knowledge(query))
       console.print(results.summary)
   ```

**Unit Tests** (TDD):
1. `tests/research/test_orchestrator.py`:
   ```python
   @pytest.mark.asyncio
   async def test_firecrawl_integration():
       orch = ResearchOrchestrator()
       results = await orch.gather_from_firecrawl("React hooks", ["https://react.dev/hooks"])
       assert len(results) > 0
       assert 'content' in results[0]
   ```

#### AGENT 4 VALIDATION CRITERIA (25 total)

**Prerequisites**:
1. [ ] Fire Crawl MCP connected: mcp-find firecrawl returns results
2. [ ] Tavily MCP connected: mcp-find tavily returns results

**Backend**:
3. [ ] gather_from_firecrawl() returns structured data
4. [ ] gather_from_web() returns articles
5. [ ] synthesize_knowledge() combines sources
6. [ ] rank_by_relevance() orders by score
7. [ ] pytest test_orchestrator.py: 3/3 PASS

**CLI**:
8. [ ] shannon research "React Server Components"
9. [ ] Terminal shows: "Fire Crawl: Scraping react.dev..."
10. [ ] Terminal shows: "Web search: Found 12 articles"
11. [ ] Terminal shows: "Synthesizing knowledge..."
12. [ ] Terminal displays summary (10-15 insights)
13. [ ] Results saved: .shannon/research/react_[timestamp].json
14. [ ] Exit code: 0

**Dashboard** (if --dashboard flag):
15. [ ] shannon research "Next.js" --dashboard
16. [ ] playwright.navigate("http://localhost:5175")
17. [ ] playwright.wait_for("text=Research: Next.js")
18. [ ] playwright.wait_for("text=Fire Crawl (3 sources)")
19. [ ] playwright.wait_for("text=Web (12 articles)")
20. [ ] Insights visible in panel
21. [ ] playwright.screenshot("agent4-research-validated.png")

**Quality**:
22. [ ] Manual review: Insights are relevant and coherent
23. [ ] No duplicate insights

**Regression**:
24. [ ] Previous batches work
25. [ ] pytest: All pass

**Evidence**:
26. [ ] Screenshot
27. [ ] .shannon/research/ has results
28. [ ] Commit: "Agent 4 COMPLETE: Research - 25/25"

**AGENT 4 COMPLETE**: 25/25 pass

---

### AGENT 5: Ultrathink Engine

**Skill Invocation**:
```
Use test-driven-development
Use sitrep-reporting
Use verification-before-completion
```

**Mission**: 500+ step reasoning using Sequential MCP

**Duration**: 3-4 hours

#### Implementation Tasks

**Backend**:
1. Update `src/shannon/modes/ultrathink.py`:
   ```python
   class UltrathinkEngine:
       async def analyze(self, task: str):
           thoughts = []
           thought_num = 1

           while thought_num <= 500:
               result = await mcp__sequential-thinking__sequentialthinking(
                   thought=f"THOUGHT {thought_num}: {self._generate_thought(task, thoughts)}",
                   thoughtNumber=thought_num,
                   totalThoughts=500,
                   nextThoughtNeeded=thought_num < 500
               )

               thoughts.append(result)
               thought_num += 1

           # Generate hypotheses from thoughts
           hypotheses = self._generate_hypotheses(thoughts)

           # Evaluate and compare
           comparison = self._compare_hypotheses(hypotheses)

           return UltrathinkResult(
               thoughts=thoughts,
               hypotheses=hypotheses,
               recommendation=comparison.best
           )
   ```

2. Add CLI command:
   ```python
   @cli.command('ultrathink')
   @click.argument('task')
   def ultrathink_command(task):
       engine = UltrathinkEngine()
       result = asyncio.run(engine.analyze(task))
       console.print(result.summary)
   ```

**Unit Tests** (TDD):
1. `tests/modes/test_ultrathink.py`:
   ```python
   @pytest.mark.asyncio
   async def test_generates_500_thoughts():
       engine = UltrathinkEngine()
       result = await engine.analyze("optimize database")
       assert len(result.thoughts) >= 500
   ```

#### AGENT 5 VALIDATION CRITERIA (25 total)

**Prerequisites**:
1. [ ] Sequential MCP connected

**Backend**:
2. [ ] UltrathinkEngine.analyze() calls sequential thinking
3. [ ] Generates 500+ thoughts (verify count)
4. [ ] generate_hypotheses() returns 3-5 hypotheses
5. [ ] compare_hypotheses() builds comparison matrix
6. [ ] pytest test_ultrathink.py: 2/2 PASS

**CLI**:
7. [ ] shannon ultrathink "redesign auth system"
8. [ ] Terminal shows: "ULTRATHINK MODE: 500+ steps"
9. [ ] Terminal shows progress: "Step 100/500", "Step 200/500", etc.
10. [ ] Completes all 500 thoughts
11. [ ] Terminal shows hypothesis comparison
12. [ ] Terminal shows recommendation
13. [ ] Duration: 5-15 minutes (reasonable)
14. [ ] Exit code: 0
15. [ ] Results saved: .shannon/ultrathink/auth_[timestamp].json

**Dashboard**:
16. [ ] shannon ultrathink "database optimization" --dashboard
17. [ ] playwright.navigate("http://localhost:5175")
18. [ ] playwright.wait_for("text=Ultrathink")
19. [ ] playwright.wait_for("text=Step 100/500", timeout=120000)
20. [ ] playwright.wait_for("text=Step 500/500", timeout=600000)
21. [ ] playwright.wait_for("text=Hypothesis 1")
22. [ ] hypothesis_count >= 3
23. [ ] playwright.screenshot("agent5-ultrathink-validated.png")

**Quality**:
24. [ ] Reasoning is coherent (manual review)
25. [ ] Recommendation is actionable

**Regression**:
26. [ ] Previous batches work
27. [ ] pytest: All pass

**Evidence**:
28. [ ] Screenshot shows 500/500
29. [ ] Commit: "Agent 5 COMPLETE: Ultrathink - 25/25"

**AGENT 5 COMPLETE**: 25/25 pass

---

### AGENT 6: Basic Interactive Controls

**Skill Invocation**:
```
Use test-driven-development
Use playwright-skill
Use sitrep-reporting
Use verification-before-completion
```

**Mission**: HALT, RESUME, ROLLBACK controls functional with <100ms response

**Duration**: 4-5 hours

#### Implementation Tasks

**Backend**:
1. Update `src/shannon/orchestration/orchestrator.py`:
   - Add halt_requested flag
   - Check before each step: if halt_requested: pause
   - Implement resume() method
   - Implement rollback(n_steps) with state restoration

2. Update `src/shannon/server/websocket.py`:
   - halt_execution(sid, data) handler
   - resume_execution(sid, data) handler
   - rollback_execution(sid, data) handler

3. Update `src/shannon/orchestration/state_manager.py`:
   - create_snapshot() before each step
   - rollback_to_snapshot(step_num)
   - Revert file changes via git

**Frontend**:
1. Update `dashboard/src/panels/ExecutionOverview.tsx`:
   - HALT button (enabled when running)
   - RESUME button (enabled when halted)
   - ROLLBACK input + button
   - Status indicator (Running/Halted)

**Unit Tests** (TDD):
1. `tests/orchestration/test_controls.py`:
   ```python
   @pytest.mark.asyncio
   async def test_halt_pauses():
       orch = Orchestrator()
       orch.halt_requested = True
       # Verify execution pauses

   @pytest.mark.asyncio
   async def test_rollback_reverts_state():
       state_mgr = StateManager()
       # Create snapshots
       # Rollback 5 steps
       # Verify state at step N-5
   ```

#### AGENT 6 VALIDATION CRITERIA (40 total)

**Backend**:
1. [ ] halt_requested=True pauses execution
2. [ ] resume() continues from halted step
3. [ ] rollback(5) restores to 5 steps back
4. [ ] File changes reverted correctly
5. [ ] pytest test_controls.py: 4/4 PASS

**HALT/RESUME Playwright**:
6. [ ] shannon do "long task with 10 steps" --dashboard
7. [ ] playwright.navigate("http://localhost:5175")
8. [ ] playwright.wait_for("text=Running")
9. [ ] t1 = Date.now()
10. [ ] playwright.click("button[data-testid=\"halt-button\"]")
11. [ ] t2 = Date.now()
12. [ ] Latency: t2-t1 < 100ms (SPEC REQUIREMENT)
13. [ ] playwright.wait_for("text=Halted")
14. [ ] Terminal shows: "Execution halted"
15. [ ] HALT button disabled, RESUME enabled
16. [ ] Wait 5 seconds: Execution stays paused
17. [ ] playwright.click("button[data-testid=\"resume-button\"]")
18. [ ] playwright.wait_for("text=Running")
19. [ ] Terminal shows: "Execution resumed"
20. [ ] Execution continues to completion
21. [ ] playwright.screenshot("agent6-halt-resume-validated.png")

**ROLLBACK Playwright**:
22. [ ] shannon do "task with 10 steps" --dashboard
23. [ ] playwright.wait_for("text=Step 7/10")
24. [ ] playwright.fill("input[data-testid=\"rollback-steps\"]", "5")
25. [ ] playwright.click("button[data-testid=\"rollback-button\"]")
26. [ ] playwright.click("text=Confirm")
27. [ ] playwright.wait_for("text=Step 2/10", timeout=5000)
28. [ ] Verify: Files from steps 3-7 removed (git status clean)
29. [ ] Execution continues from step 2
30. [ ] playwright.screenshot("agent6-rollback-validated.png")

**Response Time Validation**:
31. [ ] 10× HALT/RESUME cycles: All < 100ms
32. [ ] Average latency < 50ms

**Regression**:
33. [ ] All previous work functional
34. [ ] pytest: All pass

**Evidence**:
35. [ ] 2 screenshots
36. [ ] Latency measurements logged
37. [ ] Commit: "Agent 6 COMPLETE: Basic Controls - 40/40"

**AGENT 6 COMPLETE**: 40/40 pass

---

## WAVE 1 CONSOLIDATED VALIDATION

**After all 6 agents complete individually:**

### Integration Validation (Agents Working Together)

**Scenario 1: Multi-File + Agent Pool**:
1. [ ] shannon do "create 3 Python files using 3 analysis agents" --dashboard
2. [ ] 3 agents spawn
3. [ ] 3 files created
4. [ ] All agents visible in AgentPool panel
5. [ ] All files visible in event stream

**Scenario 2: Research + Decision**:
6. [ ] shannon do "task requiring research and decision"
7. [ ] Research gathers knowledge
8. [ ] Decision point created with research-informed options
9. [ ] User approves decision
10. [ ] Execution continues with selected approach

**Scenario 3: Ultrathink + Multi-Agent**:
11. [ ] shannon ultrathink "complex task" --then-execute --dashboard
12. [ ] 500 thoughts complete
13. [ ] Agents spawn for execution
14. [ ] All visible in dashboard

**Scenario 4: HALT during Multi-Agent**:
15. [ ] shannon do "task with 5 agents" --dashboard
16. [ ] 5 agents spawning
17. [ ] Click HALT
18. [ ] All 5 agents pause
19. [ ] Click RESUME
20. [ ] All 5 agents continue

**Cross-Feature Validation**:
21. [ ] All 6 features work independently
22. [ ] All 6 features work together
23. [ ] No conflicts or regressions
24. [ ] pytest: All tests pass (240+ tests)

**WAVE 1 RESULT**: 182+23 = 205 criteria pass → WAVE 1 COMPLETE

---

## WAVE 2: Advanced Features (2 PARALLEL AGENTS)

**Duration**: 3 hours wall time
**Depends on**: Wave 1 complete (needs decisions, agent pool, state management)

---

### AGENT 7: Advanced Interactive Controls

**Skills**: test-driven-development, playwright-skill, sitrep-reporting

**Mission**: REDIRECT, INJECT, APPROVE/OVERRIDE controls functional

**Duration**: 3-4 hours

#### Implementation

**Backend**:
1. REDIRECT: Orchestrator.redirect(new_constraints) → replanning
2. INJECT: ExecutionContext.add_constraint(text)
3. APPROVE/OVERRIDE: Integrate with DecisionEngine

**Frontend**:
1. REDIRECT button + constraint text area
2. INJECT button + context text area
3. APPROVE/OVERRIDE buttons on decision cards

#### AGENT 7 VALIDATION (31 criteria)

**REDIRECT**:
1-10. [REDIRECT validation - replan works, constraints applied]

**INJECT**:
11-18. [INJECT validation - context added mid-execution]

**APPROVE/OVERRIDE**:
19-25. [Decision approval/override works]

**Integration**:
26-28. [All controls work together]

**Evidence**:
29-31. [Screenshots, logs, commit]

**AGENT 7 COMPLETE**: 31/31 pass

---

### AGENT 8: FileDiff Panel

**Skills**: test-driven-development, playwright-skill, sitrep-reporting

**Mission**: File changes displayed with diffs in dashboard

**Duration**: 2-3 hours

#### Implementation

**Backend**:
1. Emit file:modified events with diffs

**Frontend**:
1. FileDiff panel renders file changes
2. Syntax highlighted diffs

#### AGENT 8 VALIDATION (17 criteria)

1-12. [File events flow, diffs display]
13-15. [Regression checks]
16-17. [Evidence]

**AGENT 8 COMPLETE**: 17/17 pass

---

## WAVE 2 CONSOLIDATED VALIDATION

**Cross-Feature**:
1. [ ] All 8 agents' features integrated
2. [ ] No conflicts
3. [ ] pytest: All tests pass

**WAVE 2 RESULT**: 48+3 = 51 criteria pass → WAVE 2 COMPLETE

---

## POST-WAVES: Integration + Release

### BATCH 2: Integration Testing (1 week)

**Full System Tests**:
- All features working together
- Edge cases
- Performance (<100ms responses)
- Stress tests (8 agents, complex tasks)

### BATCH 3: Documentation + Release (3-5 days)

**Deliverables**:
- README with all features
- CHANGELOG v4.0.0
- Usage guide
- Tag + release

---

## Execution Protocol

### Starting Wave 1

```
1. Validate Batch 1 complete (27/27)
2. Invoke: dispatching-parallel-agents skill
3. Provide 6 agent mission briefs
4. Agents execute independently
5. Monitor SITREPs from all 6
6. When all complete: Run consolidated validation
7. If any fail: Agent re-works until pass
8. When 205/205 pass: Wave 1 complete
```

### Agent Mission Brief Template

```
AGENT N: [Feature Name]

Mission: [One sentence goal]

Skills to invoke:
- test-driven-development (write tests FIRST)
- sitrep-reporting (report every 30 min)
- verification-before-completion (validate before claiming done)

Implementation:
[Detailed steps]

Validation Criteria: [X total]
[List all X criteria]

SITREP Schedule:
- Every 30 minutes
- Include: Criteria passing (N/X), phase, blockers, ETA

Success: X/X criteria pass + final SITREP shows COMPLETE
```

---

## Timeline Summary

**Batch 1**: 3 hours (validation streaming)
**Wave 1**: 4 hours (6 agents parallel, not 18h sequential)
**Wave 2**: 3 hours (2 agents parallel, not 6h sequential)
**Integration**: 1 week
**Release**: 3-5 days

**TOTAL: ~2 weeks** (vs 17 weeks sequential, vs 4-5 weeks batched)

---

## Validation Criteria Summary

**Batch 1**: 27 criteria
**Wave 1**:
- Agent 1: 26 criteria
- Agent 2: 32 criteria
- Agent 3: 34 criteria
- Agent 4: 25 criteria
- Agent 5: 25 criteria
- Agent 6: 40 criteria
- Integration: 23 criteria
- **Subtotal: 205 criteria**

**Wave 2**:
- Agent 7: 31 criteria
- Agent 8: 17 criteria
- Integration: 3 criteria
- **Subtotal: 51 criteria**

**TOTAL: 283 specific validation criteria**

Every single one must pass before release.

---

## READY FOR EXECUTION

✅ Parallel wave plan complete
✅ Validation gates defined (20-40 criteria each)
✅ Skills identified (dispatching-parallel-agents, test-driven-development, etc.)
✅ Timeline realistic (2 weeks)
✅ Evidence requirements clear

**Next**: Execute Batch 1 (Validation Streaming), then dispatch Wave 1 agents
