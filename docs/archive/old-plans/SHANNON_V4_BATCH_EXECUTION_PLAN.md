# Shannon V4: Batch Execution Plan with Rigorous Validation Gates

> **Execution Philosophy**: Implement → Validate → WORK UNTIL PASS → Next Batch
>
> **NO proceeding with failing validation. NO "infrastructure ready". ONLY "PROVEN WORKING".**

---

## Executive Summary

**Current Status**: 25-30% of shannon-cli-4.md spec functional
**Target**: 100% functional with Playwright-verified validation gates
**Approach**: 12 batches with mandatory validation gates
**Timeline**: 4-5 weeks realistic (30-40 hours implementation + 2 weeks QA + 3-5 days docs)

**Batches**: Organized by FEATURE (deliverable functionality) not TIME (weeks)
**Validation**: THROUGHOUT execution, not at end
**Evidence**: Playwright screenshots, test logs, for EVERY batch

---

## Batch Philosophy

### What is a Batch?

A batch is a **complete, validated, functional feature** ready for user use.

**Batch = Implementation + Validation Gate**

Each batch includes:
1. Backend implementation (Python)
2. Frontend implementation (React/TypeScript)
3. Unit tests (pytest)
4. Integration tests (CLI + Dashboard)
5. **VALIDATION GATE** (20-30 specific criteria)
6. Evidence (screenshots, logs)
7. Git commit (only when validated)

### Batch Completion Criteria

A batch is complete when **ALL validation criteria pass**:

✅ **Code Complete**: All modules implemented, imports working
✅ **Unit Tests Pass**: pytest shows all tests passing
✅ **CLI Works**: Terminal command produces expected results
✅ **Dashboard Updates**: Playwright verifies UI changes
✅ **Integration Verified**: Front-end + back-end work together
✅ **No Regressions**: Existing tests/features still work
✅ **Evidence Captured**: Screenshots + logs committed

**IF ANY CRITERIA FAIL**: Debug → Fix → Re-validate → Repeat until ALL pass

**NEVER PROCEED** with partial completion or "infrastructure ready"

---

## Validation Gate Structure

Every batch has a validation gate with **20-30 specific, measurable criteria**.

### Criterion Quality Standards

**GOOD Criterion** (specific, measurable, actionable):
- ✅ "playwright.wait_for('text=3 active / 8 max', timeout=10000) - PASS"
- ✅ "ls auth/tokens.py && echo $? returns 0"
- ✅ "grep -c 'def' auth/tokens.py returns >= 2 (has functions)"

**BAD Criterion** (vague, unmeasurable):
- ❌ "Agent pool works correctly"
- ❌ "Files are created"
- ❌ "Dashboard updates properly"

### Validation Gate Template

```
### VALIDATION GATE (MANDATORY - WORK UNTIL ALL PASS)

**Backend Validation** (Unit Tests):
1. [ ] pytest [specific test] - PASS
2. [ ] [Module].[method]() returns [expected output]
...

**CLI Validation** (Functional):
7. [ ] Run: [exact command]
8. [ ] Verify: [exact terminal output or file check]
9. [ ] Exit code: echo $? returns 0
...

**Dashboard Validation** (Playwright):
15. [ ] playwright.navigate("http://localhost:5175")
16. [ ] playwright.wait_for("text=[specific text]", timeout=[ms])
17. [ ] playwright.click("[selector]")
18. [ ] playwright.evaluate("() => [specific check]") === [expected]
19. [ ] playwright.screenshot("[filename].png")
...

**Integration Validation**:
22. [ ] [End-to-end flow test]
...

**Regression Validation**:
25. [ ] pytest: All existing tests pass
26. [ ] Previous batches: Re-run their validations
...

**Evidence**:
28. [ ] Screenshot exists and committed
29. [ ] Terminal output logged
30. [ ] Commit message: "VALIDATED: 30/30 criteria passed"

TOTAL: 30 criteria
PASS: 30/30 → Proceed to next batch
FAIL: <30 → Debug, fix, repeat
```

---

## Complete Batch Sequence

### PHASE 1: CRITICAL FOUNDATIONS (Batches 1-3)

**Estimated**: 10-12 hours work + validation
**Goal**: Multi-file generation, agent pool, decision engine all PROVEN working

---

## BATCH 1: Multi-File Generation

**Priority**: CRITICAL (user called out explicitly)
**Goal**: shannon do creates ALL files in multi-file request (not just 1 of N)
**Estimated**: 3-4 hours

### Implementation Steps

**Backend**:
1. Create `src/shannon/orchestration/multi_file_parser.py`
2. Implement MultiFileParser class:
   - `is_multi_file(task)` - Pattern detection
   - `parse(task)` - Extract file list and descriptions
3. Create `src/shannon/executor/multi_file_executor.py`
4. Implement MultiFileExecutor class:
   - `execute(task)` - Iterate through files
   - File-by-file execution via CompleteExecutor
   - Emit file:created events per file
5. Integrate with `src/shannon/cli/v4_commands/do.py`:
   - Import MultiFileParser, MultiFileExecutor
   - Detect multi-file requests
   - Delegate to MultiFileExecutor

**Frontend**:
- No changes needed (uses existing event handling)

**Unit Tests**:
1. Create `tests/orchestration/test_multi_file_parser.py`
   - test_single_file_detection
   - test_multi_file_detection
   - test_parse_multi_file (3 files)
   - test_parse_with_descriptions
2. Create `tests/executor/test_multi_file_executor.py`
   - test_multi_file_execution (3 files)
   - test_single_file_delegates
   - test_mixed_directories
3. Run: `pytest tests/orchestration/test_multi_file*.py tests/executor/test_multi_file*.py -v`

---

### VALIDATION GATE 1 (MANDATORY - WORK UNTIL ALL PASS)

**Cannot proceed to Batch 2 until ALL 26 criteria met:**

#### Backend Validation (Unit Tests):
1. [ ] pytest tests/orchestration/test_multi_file_parser.py::test_single_file_detection - PASS
2. [ ] pytest tests/orchestration/test_multi_file_parser.py::test_multi_file_detection - PASS
3. [ ] pytest tests/orchestration/test_multi_file_parser.py::test_parse_multi_file - PASS (returns 3 files)
4. [ ] pytest tests/executor/test_multi_file_executor.py::test_multi_file_execution - PASS
5. [ ] pytest tests/executor/test_multi_file_executor.py::test_single_file_delegates - PASS
6. [ ] pytest (all tests): Shows "226 passed" (was 221, added 5)

#### CLI Validation (Functional):
7. [ ] cd /tmp/batch1-test && rm -rf * .git .shannon* && git init
8. [ ] shannon do "create auth: tokens.py, middleware.py, __init__.py"
9. [ ] Exit code: echo $? returns 0
10. [ ] File exists: [ -f auth/tokens.py ] && echo "PASS" returns "PASS"
11. [ ] File exists: [ -f auth/middleware.py ] && echo "PASS" returns "PASS"
12. [ ] File exists: [ -f auth/__init__.py ] && echo "PASS" returns "PASS"
13. [ ] Content check: wc -l auth/tokens.py returns > 10 (has meaningful content)
14. [ ] Content check: grep -c "def\|class" auth/tokens.py returns >= 1 (has code)
15. [ ] Git check: git log -1 --name-only | grep -c "auth/" returns 3 (all files committed)

#### Dashboard Validation (Playwright):
16. [ ] playwright.navigate("http://localhost:5175")
17. [ ] playwright.wait_for("text=Connected", timeout=5000) - PASS
18. [ ] event_count = playwright.evaluate("() => document.querySelectorAll('[data-testid=\"event-item\"]').length")
19. [ ] event_count >= 5 (execution:started + 3 file:created + execution:completed)
20. [ ] playwright.screenshot("batch1-multi-file-validated.png")
21. [ ] Screenshot file size: ls -lh batch1-multi-file-validated.png shows > 10KB (not blank)

#### Integration Validation:
22. [ ] Mixed directories test: shannon do "create dir1/a.py, dir2/b.py, c.py"
23. [ ] Verify: All 3 files created in correct directories

#### Regression Validation:
24. [ ] Single-file still works: shannon do "test.py" creates 1 file
25. [ ] shannon exec still works: shannon exec "calc.py" (V3.5 not broken)

#### Evidence:
26. [ ] batch1-multi-file-validated.png committed to repo
27. [ ] Terminal output saved to batch1_validation.log
28. [ ] Commit message includes: "VALIDATED: 26/26 criteria passed"

**RESULT**: 26/26 pass → BATCH 1 COMPLETE → Proceed to Batch 2
**OR**: <26 pass → Debug, fix, re-validate, repeat

**WORK UNTIL**: Every single criterion passes

---

## BATCH 2: Agent Pool + Dashboard Panel

**Priority**: HIGH (user priority #2)
**Goal**: 8 agents execute in parallel, visible in dashboard
**Estimated**: 2-3 hours
**Depends on**: Batch 1 (need multi-file for complex test tasks)

### Implementation Steps

**Backend**:
1. Enhance `src/shannon/orchestration/agent_pool.py`:
   - Add spawn_agent(skill_name, parameters, session_id)
   - Enforce capacity limits (8 active, 50 total)
   - Emit agent:spawned events
   - Implement terminate_agent()
2. Update `src/shannon/orchestration/orchestrator.py`:
   - Add _execute_via_agent(agent, step)
   - Add _execute_parallel_steps(steps) with asyncio.gather
   - Emit agent:spawned and agent:completed events
3. Update agent classes in `src/shannon/orchestration/agents/`:
   - Ensure all 7 agent types (Research, Analysis, Testing, Validation, Git, Planning, Monitoring) work

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   - Add agents: Agent[] state
   - Add addAgent(), updateAgent(), removeAgent()
   - Handle agent:spawned event (adds to agents array)
   - Handle agent:completed event (updates status to completed/failed)
2. Update `dashboard/src/panels/AgentPool.tsx`:
   - Render active agents (status === 'running')
   - Show "X active / 8 max" count
   - Display agent cards with skill name, role, progress
   - Collapsible section for completed agents

**Unit Tests**:
1. Create `tests/orchestration/test_agent_pool_enhanced.py`:
   - test_spawn_single_agent
   - test_capacity_limits (enforce 8 max)
   - test_agent_role_determination
2. Create `tests/orchestration/test_orchestrator_agents.py`:
   - test_single_agent_spawning
   - test_parallel_agent_execution (3 agents)
3. Run: `pytest tests/orchestration/test_agent*.py -v`

---

### VALIDATION GATE 2 (MANDATORY - WORK UNTIL ALL PASS)

**Cannot proceed to Batch 3 until ALL 29 criteria met:**

#### Backend Validation:
1. [ ] AgentPool(max_active=8).spawn_agent() returns Agent with unique ID
2. [ ] agent.id is UUID format (len == 36, has dashes)
3. [ ] AgentPool with 8 active agents raises AgentPoolFullError on 9th spawn
4. [ ] Orchestrator._execute_via_agent() executes skill successfully
5. [ ] asyncio.gather() for 3 agents completes all 3
6. [ ] pytest tests/orchestration/test_agent_pool_enhanced.py: 3/3 PASS
7. [ ] pytest tests/orchestration/test_orchestrator_agents.py: 2/2 PASS
8. [ ] pytest (all tests): Shows "231 passed" (was 226, added 5)

#### CLI Validation:
9. [ ] cd /tmp/batch2-test && rm -rf * .git .shannon* && git init && echo ".gitignore" > .gitignore
10. [ ] shannon do "analyze code and run tests and check security" --dashboard
11. [ ] Terminal output shows: "Spawning 3 agents for parallel execution"
12. [ ] Terminal shows 3 × "Event: agent:spawned" messages
13. [ ] Terminal shows 3 × "Event: agent:completed" messages
14. [ ] Exit code: echo $? returns 0
15. [ ] Execution time: < 60 seconds (parallel faster than sequential)

#### Dashboard Validation (Playwright):
16. [ ] playwright.navigate("http://localhost:5175")
17. [ ] playwright.wait_for("text=Connected", timeout=5000) - PASS
18. [ ] playwright.click("text=Agent Pool") (select panel tab)
19. [ ] playwright.wait_for("text=3 active / 8 max", timeout=10000) - PASS
20. [ ] agent_cards = playwright.evaluate("() => document.querySelectorAll('[data-testid=\"agent-card\"]').length")
21. [ ] agent_cards === 3 (exactly 3 agents shown)
22. [ ] First agent card: playwright.wait_for("text=code_analysis") - skill name visible
23. [ ] First agent card: playwright.wait_for("text=Analysis") - role visible
24. [ ] Progress bar visible: playwright.evaluate("() => document.querySelector('.progress-bar') !== null") === true
25. [ ] Wait for completion: playwright.wait_for("text=0 active / 8 max", timeout=60000) - PASS
26. [ ] Completed section: playwright.click("text=Completed Agents")
27. [ ] Completed count: playwright.wait_for("text=3") in completed section
28. [ ] playwright.screenshot("batch2-agent-pool-validated.png")

#### Regression Validation:
29. [ ] Multi-file still works: shannon do "create a.py, b.py, c.py" creates 3 files
30. [ ] ExecutionOverview still updates correctly
31. [ ] pytest: All 231 tests pass (no regressions)

#### Evidence:
32. [ ] batch2-agent-pool-validated.png committed
33. [ ] batch2_validation.log with terminal output committed
34. [ ] Commit message: "VALIDATED: Agent Pool - 32/32 criteria passed"

**RESULT**: 32/32 criteria met → BATCH 2 COMPLETE → Proceed to Batch 3
**OR**: <32 criteria → WORK UNTIL ALL PASS

---

## BATCH 3: Decision Engine + Dashboard Panel

**Priority**: HIGHEST (user priority #1)
**Goal**: Human-in-the-loop decisions with auto-approval for high confidence
**Estimated**: 3-4 hours
**Depends on**: Batch 2 (decisions about agent approaches)

### Implementation Steps

**Backend**:
1. Enhance `src/shannon/orchestration/decision_engine.py`:
   - Define DecisionPoint and DecisionOption dataclasses
   - Implement request_decision(title, description, options, recommended, auto_approve_threshold)
   - Auto-approve if confidence >= threshold (default 0.95)
   - Emit decision:created event for manual decisions
   - Implement _wait_for_decision() polling loop
   - Track decision_history
2. Update `src/shannon/server/websocket.py`:
   - Add approve_decision(sid, data) handler
   - Emit decision:approved back to orchestrator
3. Integrate into Orchestrator:
   - Call decision_engine.request_decision() when needed
   - Resume execution with selected option

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   - Add decisions: DecisionPoint[] state
   - Add addDecision(), approveDecision()
   - Handle decision:created event (add to decisions array)
   - Handle decision:approved event (update status)
2. Update `dashboard/src/panels/Decisions.tsx`:
   - Render pending decisions with yellow background
   - Display options with pros/cons in 2-column grid
   - Highlight recommended option with ⭐
   - Show confidence percentage per option
   - Enable approve button only when option selected
   - Collapsible completed decisions section

**Unit Tests**:
1. Create `tests/orchestration/test_decision_engine.py`:
   - test_auto_approve_high_confidence (0.97 > 0.95)
   - test_manual_approval_low_confidence (0.70 < 0.95)
   - test_decision_history_tracking
2. Run: `pytest tests/orchestration/test_decision*.py -v`

---

### VALIDATION GATE 3 (MANDATORY - WORK UNTIL ALL PASS)

**Cannot proceed to Batch 4 until ALL 28 criteria met:**

#### Backend Validation:
1. [ ] DecisionEngine().request_decision() with confidence=0.97, threshold=0.95 auto-approves
2. [ ] Returns selected DecisionOption immediately (no waiting)
3. [ ] Decision saved to decision_history
4. [ ] DecisionEngine().request_decision() with confidence=0.70, threshold=0.95 emits decision:created
5. [ ] decision:created payload includes: decision_id, title, description, options[], recommended
6. [ ] pytest tests/orchestration/test_decision_engine.py: 3/3 PASS
7. [ ] pytest (all tests): Shows "234 passed" (added 3)

#### CLI Validation with Manual Decision:
8. [ ] cd /tmp/batch3-test && git init && echo ".gitignore" > .gitignore
9. [ ] Modify orchestrator to inject test decision (confidence=0.70)
10. [ ] shannon do "test decision flow" --dashboard
11. [ ] Terminal shows: "Decision point: Select Database Strategy"
12. [ ] Terminal shows: "Waiting for user approval..."
13. [ ] Terminal paused (not completing execution)

#### Dashboard Validation (Playwright):
14. [ ] playwright.navigate("http://localhost:5175")
15. [ ] playwright.wait_for("text=Connected", timeout=5000)
16. [ ] playwright.click("text=Decisions") (select panel)
17. [ ] playwright.wait_for("text=Select Database Strategy", timeout=10000) - Decision appears
18. [ ] option_count = playwright.evaluate("() => document.querySelectorAll('[data-testid=\"decision-option\"]').length")
19. [ ] option_count === 3 (shows 3 options)
20. [ ] playwright.wait_for("text=⭐ Recommended") - Recommended option highlighted
21. [ ] playwright.wait_for("text=Pros:") and playwright.wait_for("text=Cons:") - Both visible
22. [ ] playwright.click("[data-testid=\"decision-option-2\"]") - Click option 2 (NOT recommended)
23. [ ] Border turns blue: playwright.evaluate("() => document.querySelector('[data-testid=\"decision-option-2\"]').classList.contains('border-blue-500')") === true
24. [ ] playwright.click("text=Approve Selected Option")
25. [ ] playwright.wait_for("text=Decision approved", timeout=5000)
26. [ ] Terminal shows: "Decision approved: opt2"
27. [ ] Execution continues (terminal shows next steps)
28. [ ] playwright.screenshot("batch3-decision-validated.png")

#### Auto-Approval Validation:
29. [ ] Modify test: confidence=0.97, threshold=0.95
30. [ ] shannon do "auto approval test" --dashboard
31. [ ] Terminal shows: "Auto-approving decision (confidence: 0.97)"
32. [ ] Decision NOT shown in dashboard (auto-approved)
33. [ ] Execution continues immediately (no pause)

#### Integration Validation:
34. [ ] Decision selection affects execution: Option 2 chosen → Execution uses Option 2 approach

#### Regression Validation:
35. [ ] Batch 1 validation re-run: Multi-file creates 3 files
36. [ ] Batch 2 validation re-run: Agent pool spawns 3 agents
37. [ ] pytest: All 234 tests pass

#### Evidence:
38. [ ] batch3-decision-validated.png shows decision card with 3 options
39. [ ] Terminal log shows approval flow
40. [ ] Commit: "VALIDATED: Decision Engine - 34/34 criteria passed"

**RESULT**: 34/34 criteria → BATCH 3 COMPLETE → Proceed to Batch 4

**WORK UNTIL**: Every criterion passes (not 33/34, not "almost there")

---

## BATCH 4: Validation Streaming + Panel

**Priority**: HIGH (user priority #5, enables validation of future batches)
**Goal**: Test output streams to dashboard in real-time
**Estimated**: 2-3 hours
**Depends on**: Validator exists (from V3.5)

### Implementation Steps

**Backend**:
1. Update `src/shannon/executor/validator.py`:
   - Modify _run_check() to stream output line-by-line
   - Emit validation:output event for each line
   - Include test status (running, passed, failed)
   - Include error traces for failures
2. Add language detection for syntax highlighting hints

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   - Add validationOutput: string[] state
   - Handle validation:output event (append to array)
   - Handle validation:started, validation:completed events
2. Update `dashboard/src/panels/Validation.tsx`:
   - Render output lines with auto-scroll
   - Syntax highlight test output
   - Highlight failures in red, passes in green
   - Show test summary (X passed, Y failed)

**Unit Tests**:
1. Update `tests/executor/test_validator.py`:
   - test_streaming_output
   - test_failure_highlighting
2. Run: `pytest tests/executor/test_validator.py -v`

---

### VALIDATION GATE 4 (MANDATORY - WORK UNTIL ALL PASS)

**Cannot proceed to Batch 5 until ALL 27 criteria met:**

#### Backend Validation:
1. [ ] ValidationOrchestrator.validate_tier2() streams output line-by-line
2. [ ] Each line emits validation:output event
3. [ ] validation:output payload includes: line (string), type (stdout/stderr)
4. [ ] Test failure includes error trace in payload
5. [ ] pytest tests/executor/test_validator.py: All pass

#### CLI Validation with Failing Tests:
6. [ ] cd /tmp/batch4-test && git init
7. [ ] Create test project with 5 tests (3 pass, 2 fail)
8. [ ] shannon do "run tests" --dashboard
9. [ ] Terminal shows: "Running tests..."
10. [ ] Terminal streams test output line-by-line

#### Dashboard Validation (Playwright):
11. [ ] playwright.navigate("http://localhost:5175")
12. [ ] playwright.wait_for("text=Connected", timeout=5000)
13. [ ] playwright.click("text=Validation") (select panel)
14. [ ] playwright.wait_for("text=Running tests...", timeout=5000)
15. [ ] Wait for first output: playwright.wait_for("text=test_", timeout=10000) - Test name appears
16. [ ] line_count = playwright.evaluate("() => document.querySelectorAll('.validation-line').length")
17. [ ] line_count > 10 (multiple lines visible)
18. [ ] Red line visible: playwright.evaluate("() => document.querySelector('.text-red-500') !== null") === true
19. [ ] Green line visible: playwright.evaluate("() => document.querySelector('.text-green-500') !== null") === true
20. [ ] Final summary: playwright.wait_for("text=3 passed, 2 failed", timeout=30000)
21. [ ] Auto-scroll: Last line is visible in viewport
22. [ ] playwright.screenshot("batch4-validation-streaming.png")

#### Performance Validation:
23. [ ] Latency test: Output line appears < 200ms after backend emits (check timestamp correlation)
24. [ ] Load test: Stream 1000 lines, UI doesn't freeze, all lines visible

#### Integration Validation:
25. [ ] Validation streaming works during shannon do execution
26. [ ] Validation panel updates while other panels also active

#### Regression Validation:
27. [ ] Batches 1-3 validations re-run and pass
28. [ ] pytest: All tests pass

#### Evidence:
29. [ ] batch4-validation-streaming.png shows red/green highlighted output
30. [ ] Commit: "VALIDATED: Validation Streaming - 27/27 criteria"

**RESULT**: 27/27 → BATCH 4 COMPLETE → Proceed to Batch 5

---

## BATCH 5a: Research - Fire Crawl Integration

**Priority**: HIGH (user priority #3, part 1 of 2)
**Goal**: shannon research uses Fire Crawl to gather documentation
**Estimated**: 2-3 hours
**Depends on**: Fire Crawl MCP connected

### Implementation Steps

**Backend**:
1. Update `src/shannon/research/orchestrator.py`:
   - Implement gather_from_firecrawl(query, urls)
   - Call mcp__firecrawl-mcp__firecrawl_scrape for each URL
   - Parse and structure results
   - Cache results to avoid redundant crawls
2. Add CLI command stub in `src/shannon/cli/commands.py`:
   - shannon research command basic structure

**Frontend**:
- No dashboard changes yet (Batch 5b)

**Unit Tests**:
1. Create `tests/research/test_firecrawl_integration.py`:
   - test_firecrawl_scrape_single_url
   - test_firecrawl_multiple_urls
   - test_result_caching
2. Run: `pytest tests/research/test_firecrawl*.py -v`

---

### VALIDATION GATE 5a (MANDATORY)

**Cannot proceed to Batch 5b until ALL 20 criteria met:**

#### Backend Validation:
1. [ ] Fire Crawl MCP connected: mcp-find firecrawl returns results
2. [ ] ResearchOrchestrator.gather_from_firecrawl() returns structured data
3. [ ] Result includes: content, title, url, timestamp
4. [ ] Caching works: Second call same URL returns cached (instant)
5. [ ] pytest tests/research/test_firecrawl*.py: 3/3 PASS

#### CLI Validation:
6. [ ] shannon research "React documentation" --source firecrawl
7. [ ] Terminal shows: "Fire Crawl: Scraping https://react.dev..."
8. [ ] Terminal shows: "Extracted: 1,234 words"
9. [ ] Results saved to .shannon/research/react_[timestamp].json
10. [ ] Exit code: 0

#### Functional Validation:
11. [ ] cat .shannon/research/react_*.json shows structured data
12. [ ] JSON has keys: query, sources, content, extracted_at
13. [ ] Content is meaningful (not empty or error)

#### Performance Validation:
14. [ ] First scrape: < 30 seconds
15. [ ] Cached scrape: < 1 second

#### Integration Validation:
16. [ ] shannon do "build React app" auto-triggers research (if configured)
17. [ ] Research results accessible to executor

#### Regression Validation:
18. [ ] Batches 1-4 still functional
19. [ ] pytest: All tests pass

#### Evidence:
20. [ ] Terminal log shows Fire Crawl output
21. [ ] .shannon/research/ directory has results
22. [ ] Commit: "VALIDATED: Fire Crawl Integration - 20/20"

**RESULT**: 20/20 → BATCH 5a COMPLETE → Proceed to Batch 5b

---

## BATCH 5b: Research - Synthesis + Dashboard

**Priority**: HIGH (user priority #3, part 2 of 2)
**Goal**: Synthesize multi-source research and display in dashboard
**Estimated**: 2-3 hours
**Depends on**: Batch 5a (Fire Crawl working)

### Implementation Steps

**Backend**:
1. Add to `src/shannon/research/orchestrator.py`:
   - gather_from_web(query) using web search MCP
   - synthesize_knowledge(sources) - Combine Fire Crawl + web results
   - rank_by_relevance() - Score and order insights
   - deduplicate() - Remove redundant information
2. Complete shannon research command:
   - Support --depth flag (quick, comprehensive)
   - Display synthesis in terminal
   - Save to .shannon/research/

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   - Add research: ResearchResult state
   - Handle research:started, research:result events
2. Create `dashboard/src/panels/Research.tsx` (if doesn't exist):
   - Show research query and status
   - List sources (Fire Crawl, web search)
   - Display insights with relevance scores
   - Show synthesis summary

**Unit Tests**:
1. Create `tests/research/test_synthesis.py`:
   - test_knowledge_synthesis
   - test_ranking_by_relevance
   - test_deduplication
2. Run: `pytest tests/research/test_synthesis.py -v`

---

### VALIDATION GATE 5b (MANDATORY)

**Cannot proceed to Batch 6 until ALL 25 criteria met:**

#### Backend Validation:
1. [ ] synthesize_knowledge([source1, source2]) returns merged insights
2. [ ] rank_by_relevance() orders by score (highest first)
3. [ ] deduplicate() removes identical insights
4. [ ] pytest tests/research/test_synthesis.py: 3/3 PASS

#### CLI Validation:
5. [ ] shannon research "React Server Components best practices"
6. [ ] Terminal shows: "Fire Crawl: 3 sources"
7. [ ] Terminal shows: "Web search: 12 articles"
8. [ ] Terminal shows: "Synthesizing knowledge..."
9. [ ] Terminal displays synthesis summary (10-15 key insights)
10. [ ] Exit code: 0
11. [ ] Results in .shannon/research/ include both Fire Crawl and web results

#### Dashboard Validation (Playwright):
12. [ ] shannon research "Next.js routing" --dashboard
13. [ ] playwright.navigate("http://localhost:5175")
14. [ ] playwright.wait_for("text=Research: Next.js routing", timeout=10000)
15. [ ] playwright.wait_for("text=Fire Crawl (3 sources)") - Sources listed
16. [ ] playwright.wait_for("text=Web (12 articles)")
17. [ ] Insights visible: playwright.evaluate("() => document.querySelectorAll('.insight-item').length") >= 10
18. [ ] Relevance scores shown: playwright.wait_for("text=Relevance:")
19. [ ] playwright.screenshot("batch5b-research-validated.png")

#### Quality Validation:
20. [ ] Manual review: Insights are coherent and relevant (not garbage)
21. [ ] No duplicate insights in list
22. [ ] Sources cited for each insight

#### Integration Validation:
23. [ ] shannon do "complex task" auto-triggers research when knowledge gap detected

#### Regression Validation:
24. [ ] Batches 1-4 validations pass
25. [ ] pytest: All tests pass

#### Evidence:
26. [ ] batch5b-research-validated.png committed
27. [ ] Commit: "VALIDATED: Research Synthesis - 25/25"

**RESULT**: 25/25 → BATCH 5 COMPLETE → Proceed to Batch 6

---

## BATCH 6a: Ultrathink - Sequential MCP Integration

**Priority**: HIGH (user priority #4, part 1 of 2)
**Goal**: 500+ step reasoning using Sequential MCP
**Estimated**: 3-4 hours
**Depends on**: Sequential MCP connected

### Implementation Steps

**Backend**:
1. Update `src/shannon/modes/ultrathink.py`:
   - Implement UltrathinkEngine.analyze(task)
   - Call mcp__sequential-thinking__sequentialthinking in loop
   - Track thought count (target: 500+)
   - Extract key insights from thoughts
   - Save reasoning trace
2. Add shannon ultrathink command to CLI

**Frontend**:
1. Create `dashboard/src/panels/Ultrathink.tsx`:
   - Show reasoning progress (Step X/500)
   - Display current thought
   - Show phase (Decomposition, Research, Evaluation, etc.)

**Unit Tests**:
1. Create `tests/modes/test_ultrathink.py`:
   - test_sequential_mcp_integration
   - test_thought_count_reaches_target
2. Run: `pytest tests/modes/test_ultrathink.py -v`

---

### VALIDATION GATE 6a (MANDATORY)

**Cannot proceed to Batch 6b until ALL 22 criteria met:**

#### Backend Validation:
1. [ ] Sequential MCP connected: mcp-find sequential returns results
2. [ ] UltrathinkEngine.analyze() calls sequential thinking
3. [ ] Thought count reaches 500+ (verify in logs)
4. [ ] Reasoning trace saved to .shannon/ultrathink/
5. [ ] pytest tests/modes/test_ultrathink.py: 2/2 PASS

#### CLI Validation:
6. [ ] shannon ultrathink "redesign auth system"
7. [ ] Terminal shows: "ULTRATHINK MODE: 500+ steps"
8. [ ] Terminal shows progress: "Step 1/500", "Step 100/500", etc.
9. [ ] Completes 500+ thoughts (verify in final output)
10. [ ] Duration: 5-15 minutes (reasonable for 500 thoughts)
11. [ ] Exit code: 0
12. [ ] Results in .shannon/ultrathink/auth_[timestamp].json

#### Dashboard Validation (Playwright):
13. [ ] shannon ultrathink "database optimization" --dashboard
14. [ ] playwright.navigate("http://localhost:5175")
15. [ ] playwright.wait_for("text=Ultrathink: database optimization", timeout=10000)
16. [ ] playwright.wait_for("text=Step 1/500")
17. [ ] Wait for progress: playwright.wait_for("text=Step 100/500", timeout=120000)
18. [ ] playwright.wait_for("text=Step 500/500", timeout=600000) - Completes
19. [ ] playwright.screenshot("batch6a-ultrathink-validated.png")

#### Quality Validation:
20. [ ] Manual review: Reasoning is coherent (not random thoughts)
21. [ ] Thoughts build on each other (not independent)
22. [ ] Final output has actionable recommendation

#### Regression Validation:
23. [ ] Batches 1-5 still functional
24. [ ] pytest: All tests pass

#### Evidence:
25. [ ] batch6a-ultrathink-validated.png shows 500/500
26. [ ] Commit: "VALIDATED: Ultrathink Sequential - 22/22"

**RESULT**: 22/22 → BATCH 6a COMPLETE → Proceed to Batch 6b

---

## BATCH 6b: Ultrathink - Hypothesis Engine

**Priority**: HIGH (user priority #4, part 2 of 2)
**Goal**: Multi-hypothesis generation, comparison, selection
**Estimated**: 2-3 hours
**Depends on**: Batch 6a (sequential reasoning working)

### Implementation Steps

**Backend**:
1. Add to `src/shannon/modes/ultrathink.py`:
   - generate_hypotheses() - Create 3-5 alternative approaches
   - evaluate_hypothesis() - Score each hypothesis
   - compare_hypotheses() - Build comparison matrix
   - select_best() - Choose highest scoring approach

**Frontend**:
1. Update `dashboard/src/panels/Ultrathink.tsx`:
   - Display hypothesis cards (3-5 hypotheses)
   - Show comparison matrix with scores
   - Highlight recommended hypothesis

**Unit Tests**:
1. Add to `tests/modes/test_ultrathink.py`:
   - test_hypothesis_generation (3-5 hypotheses)
   - test_hypothesis_evaluation
   - test_comparison_matrix
2. Run: `pytest tests/modes/test_ultrathink.py -v`

---

### VALIDATION GATE 6b (MANDATORY)

**Cannot proceed to Batch 7 until ALL 25 criteria met:**

#### Backend Validation:
1. [ ] generate_hypotheses() returns 3-5 distinct hypotheses
2. [ ] Each hypothesis has: id, label, description, pros[], cons[], confidence
3. [ ] evaluate_hypothesis() returns score 0.0-10.0
4. [ ] compare_hypotheses() builds comparison matrix
5. [ ] select_best() returns highest scoring hypothesis
6. [ ] pytest: Hypothesis tests pass

#### CLI Validation:
7. [ ] shannon ultrathink "optimize database queries"
8. [ ] Terminal shows: "Generating hypotheses..."
9. [ ] Terminal displays 3 hypotheses with pros/cons
10. [ ] Terminal shows comparison matrix
11. [ ] Terminal highlights recommended: "⭐ Hypothesis 2 (Score: 8.9/10)"
12. [ ] Exit code: 0

#### Dashboard Validation (Playwright):
13. [ ] shannon ultrathink "API redesign" --dashboard
14. [ ] playwright.navigate("http://localhost:5175")
15. [ ] playwright.wait_for("text=Ultrathink")
16. [ ] playwright.wait_for("text=Hypothesis 1", timeout=600000) - First hypothesis appears
17. [ ] hypothesis_count = playwright.evaluate("() => document.querySelectorAll('.hypothesis-card').length")
18. [ ] hypothesis_count >= 3 (shows 3+ hypotheses)
19. [ ] playwright.wait_for("text=Pros:") and playwright.wait_for("text=Cons:")
20. [ ] playwright.wait_for("text=Score:") - Scores visible
21. [ ] playwright.wait_for("text=⭐") - Recommended marked
22. [ ] playwright.screenshot("batch6b-hypothesis-validated.png")

#### Quality Validation:
23. [ ] Hypotheses are genuinely different approaches (not variations)
24. [ ] Scoring makes sense (higher score = better approach)
25. [ ] Recommendation is logical given comparison

#### Regression Validation:
26. [ ] All previous batches validated
27. [ ] pytest: All tests pass

#### Evidence:
28. [ ] batch6b-hypothesis-validated.png shows comparison
29. [ ] Commit: "VALIDATED: Hypothesis Engine - 25/25"

**RESULT**: 25/25 → BATCH 6 COMPLETE → Proceed to Batch 7

---

## BATCH 7a: Interactive Controls - HALT + RESUME

**Priority**: HIGH (user priority #6, part 1 of 3)
**Goal**: HALT pauses execution <100ms, RESUME continues
**Estimated**: 2-3 hours
**Depends on**: State management (exists)

### Implementation Steps

**Backend**:
1. Update `src/shannon/orchestration/orchestrator.py`:
   - Add halt_requested flag
   - Check flag before each step
   - Pause execution if halt_requested
   - Implement resume() method
2. Update `src/shannon/server/websocket.py`:
   - Add halt_execution(sid, data) handler
   - Add resume_execution(sid, data) handler
   - Emit execution:halted, execution:resumed events
3. Add state saving on halt

**Frontend**:
1. Update `dashboard/src/panels/ExecutionOverview.tsx`:
   - HALT button triggers halt_execution event
   - Disable HALT when not running
   - Enable RESUME when halted
   - Show halted status visually (orange/yellow)

**Unit Tests**:
1. Create `tests/orchestration/test_halt_resume.py`:
   - test_halt_pauses_execution
   - test_resume_continues_execution
2. Run: `pytest tests/orchestration/test_halt*.py -v`

---

### VALIDATION GATE 7a (MANDATORY)

**Cannot proceed to Batch 7b until ALL 23 criteria met:**

#### Backend Validation:
1. [ ] Orchestrator.halt_requested = True pauses before next step
2. [ ] Orchestrator.resume() continues from halted step
3. [ ] State saved on halt (can restore if crashed)
4. [ ] pytest tests/orchestration/test_halt_resume.py: 2/2 PASS

#### CLI + Dashboard Validation (Playwright):
5. [ ] Terminal 1: shannon do "long running task with 10 steps" --dashboard
6. [ ] Terminal 2: playwright.navigate("http://localhost:5175")
7. [ ] playwright.wait_for("text=Running", timeout=5000)
8. [ ] Record timestamp T1: const t1 = Date.now()
9. [ ] playwright.click("button[data-testid=\"halt-button\"]")
10. [ ] Record timestamp T2: const t2 = Date.now()
11. [ ] Halt latency: T2 - T1 < 100ms (spec requirement)
12. [ ] playwright.wait_for("text=Halted", timeout=5000)
13. [ ] Terminal shows: "Execution halted by user"
14. [ ] HALT button disabled, RESUME button enabled
15. [ ] Execution does NOT proceed (stays on same step for 5+ seconds)
16. [ ] playwright.click("button[data-testid=\"resume-button\"]")
17. [ ] playwright.wait_for("text=Running", timeout=2000)
18. [ ] Terminal shows: "Execution resumed"
19. [ ] Execution continues to completion
20. [ ] playwright.screenshot("batch7a-halt-resume-validated.png")

#### Response Time Validation:
21. [ ] 10 HALT/RESUME cycles, all < 100ms response
22. [ ] Average latency: < 50ms

#### Regression Validation:
23. [ ] All previous batches validated
24. [ ] pytest: All tests pass

#### Evidence:
25. [ ] batch7a-halt-resume-validated.png shows Halted state
26. [ ] Latency measurements logged
27. [ ] Commit: "VALIDATED: HALT/RESUME <100ms - 23/23"

**RESULT**: 23/23 → BATCH 7a COMPLETE → Proceed to Batch 7b

---

## BATCH 7b: Interactive Controls - ROLLBACK + INJECT + INSPECT

**Priority**: MEDIUM (user priority #6, part 2 of 3)
**Goal**: ROLLBACK undoes N steps, INJECT adds context, INSPECT shows state
**Estimated**: 3-4 hours
**Depends on**: Batch 7a (HALT/RESUME working)

### Implementation Steps

**Backend**:
1. Implement ROLLBACK:
   - StateManager.create_snapshot() before each step
   - StateManager.rollback(n_steps) restores to step N-n
   - Revert file changes via git
   - Update orchestrator state
2. Implement INJECT:
   - ExecutionContext.add_constraint(text)
   - Re-plan if constraints change approach
3. Implement INSPECT:
   - StateManager.get_complete_state() returns full context
   - Include: current step, modified files, agent status, decision history

**Frontend**:
1. Add ROLLBACK UI:
   - Input field for N (number of steps)
   - "Rollback N Steps" button
   - Show confirmation dialog
2. Add INJECT UI:
   - Text area for constraint
   - "Inject Context" button
3. Add INSPECT UI:
   - "Inspect State" button opens modal
   - Display JSON state tree

**Unit Tests**:
1. Create `tests/orchestration/test_rollback.py`:
   - test_rollback_1_step
   - test_rollback_5_steps
   - test_file_changes_reverted
2. Create `tests/orchestration/test_inject.py`:
   - test_context_injection
   - test_replan_triggered
3. Run: `pytest tests/orchestration/test_roll*.py tests/orchestration/test_inject.py -v`

---

### VALIDATION GATE 7b (MANDATORY)

**Cannot proceed to Batch 7c until ALL 28 criteria met:**

#### ROLLBACK Validation:
1. [ ] StateManager creates snapshots before each step
2. [ ] rollback(5) restores state to 5 steps ago
3. [ ] File changes reverted via git reset
4. [ ] pytest test_rollback*.py: All pass

#### ROLLBACK Playwright Validation:
5. [ ] shannon do "task with 10 steps" --dashboard
6. [ ] playwright.wait_for("text=Step 7/10") - Execution at step 7
7. [ ] playwright.fill("input[data-testid=\"rollback-steps\"]", "5")
8. [ ] playwright.click("button[data-testid=\"rollback-button\"]")
9. [ ] playwright.click("text=Confirm") in confirmation dialog
10. [ ] playwright.wait_for("text=Step 2/10", timeout=5000) - Rolled back to step 2
11. [ ] Verify: Files from steps 3-7 deleted (git status clean)
12. [ ] Execution continues from step 2
13. [ ] playwright.screenshot("batch7b-rollback-validated.png")

#### INJECT Validation:
14. [ ] pytest test_inject.py: Pass

#### INJECT Playwright Validation:
15. [ ] shannon do "task" --dashboard
16. [ ] playwright.wait_for("text=Running")
17. [ ] playwright.click("button[data-testid=\"inject-button\"]")
18. [ ] playwright.fill("textarea", "New constraint: Must use TypeScript")
19. [ ] playwright.click("text=Inject")
20. [ ] Terminal shows: "Context injected: Must use TypeScript"
21. [ ] Verify: Subsequent code generation uses TypeScript (not JavaScript)
22. [ ] playwright.screenshot("batch7b-inject-validated.png")

#### INSPECT Validation:
23. [ ] playwright.click("button[data-testid=\"inspect-button\"]")
24. [ ] Modal opens with state tree
25. [ ] playwright.wait_for("text=current_step") - State keys visible
26. [ ] playwright.wait_for("text=modified_files")
27. [ ] playwright.screenshot("batch7b-inspect-validated.png")

#### Regression Validation:
28. [ ] All previous batches validated
29. [ ] pytest: All tests pass

#### Evidence:
30. [ ] 3 screenshots committed
31. [ ] Commit: "VALIDATED: ROLLBACK/INJECT/INSPECT - 28/28"

**RESULT**: 28/28 → BATCH 7b COMPLETE → Proceed to Batch 7c

---

## BATCH 7c: Interactive Controls - REDIRECT

**Priority**: MEDIUM (user priority #6, part 3 of 3)
**Goal**: REDIRECT changes execution approach mid-execution
**Estimated**: 2-3 hours
**Depends on**: Batch 7b (state management working)

### Implementation Steps

**Backend**:
1. Implement REDIRECT:
   - Orchestrator.redirect(new_constraints) triggers re-planning
   - ExecutionPlanner.replan(task, constraints, current_state)
   - Merge current progress with new plan
   - Continue from current step with new approach

**Frontend**:
1. Add REDIRECT UI:
   - "Redirect" button
   - Text area for new constraints
   - Show new plan preview before applying

**Unit Tests**:
1. Create `tests/orchestration/test_redirect.py`:
   - test_redirect_replans
   - test_merge_with_current_progress
2. Run: `pytest tests/orchestration/test_redirect.py -v`

---

### VALIDATION GATE 7c (MANDATORY)

**Cannot proceed to Batch 8 until ALL 20 criteria met:**

#### Backend Validation:
1. [ ] Orchestrator.redirect() triggers replanning
2. [ ] New plan generated with constraints
3. [ ] Current progress preserved
4. [ ] pytest test_redirect.py: 2/2 PASS

#### Playwright Validation:
5. [ ] shannon do "build app with JavaScript" --dashboard
6. [ ] playwright.wait_for("text=Running")
7. [ ] playwright.click("button[data-testid=\"redirect-button\"]")
8. [ ] playwright.fill("textarea", "Change to TypeScript instead")
9. [ ] playwright.click("text=Apply Redirect")
10. [ ] playwright.wait_for("text=Re-planning...", timeout=5000)
11. [ ] playwright.wait_for("text=New plan: 7 steps", timeout=10000)
12. [ ] Terminal shows: "Redirecting execution..."
13. [ ] Terminal shows: "New constraint: Change to TypeScript"
14. [ ] Execution continues with TypeScript (not JavaScript)
15. [ ] playwright.screenshot("batch7c-redirect-validated.png")

#### Integration Validation:
16. [ ] HALT → REDIRECT → RESUME flow works
17. [ ] REDIRECT during multi-agent execution works
18. [ ] REDIRECT with decision points works

#### Regression Validation:
19. [ ] All previous batches validated
20. [ ] pytest: All tests pass

#### Evidence:
21. [ ] batch7c-redirect-validated.png committed
22. [ ] Commit: "VALIDATED: REDIRECT - 20/20"

**RESULT**: 20/20 → BATCH 7 COMPLETE → All interactive controls functional

---

## BATCH 8: FileDiff Panel + File Events

**Priority**: MEDIUM (nice-to-have, not in user priorities)
**Goal**: Dashboard shows file changes with diffs
**Estimated**: 2-3 hours
**Depends on**: File events being emitted

### Implementation Steps

**Backend**:
1. Update `src/shannon/executor/complete_executor.py`:
   - Track file changes during code generation
   - Emit file:modified event for each changed file
   - Include: file_path, content, diff, language
   - Generate git diff output

**Frontend**:
1. Update `dashboard/src/store/dashboardStore.ts`:
   - Add files: FileChange[] state
   - Handle file:modified event
2. Update `dashboard/src/panels/FileDiff.tsx`:
   - Display file changes with diffs
   - Syntax highlight diffs
   - Show file stats (lines, size)
   - Add Approve/Revert buttons (UI only, functionality deferred)

**Unit Tests**:
1. Update `tests/executor/test_complete_executor.py`:
   - test_file_event_emission
2. Run: `pytest tests/executor/test_complete*.py -v`

---

### VALIDATION GATE 8 (MANDATORY)

**Cannot proceed to Batch 9 until ALL 20 criteria met:**

#### Backend Validation:
1. [ ] file:modified event emitted when file created
2. [ ] Payload includes: file_path, content, diff, lines, size_bytes
3. [ ] Git diff generated correctly
4. [ ] pytest: File event test passes

#### CLI + Dashboard Validation:
5. [ ] shannon do "create app.py" --dashboard
6. [ ] playwright.navigate("http://localhost:5175")
7. [ ] playwright.click("text=File Diff")
8. [ ] playwright.wait_for("text=app.py", timeout=15000)
9. [ ] Diff visible: playwright.wait_for("text=+") - Shows additions
10. [ ] File stats: playwright.wait_for("text=lines") and playwright.wait_for("text=bytes")
11. [ ] playwright.screenshot("batch8-filediff-validated.png")

#### Multi-File Integration:
12. [ ] shannon do "create auth: a.py, b.py, c.py" --dashboard
13. [ ] FileDiff panel shows 3 files
14. [ ] Each file has its own diff

#### Regression Validation:
15. [ ] All previous batches validated
16. [ ] pytest: All tests pass

#### Evidence:
17. [ ] batch8-filediff-validated.png committed
18. [ ] Commit: "VALIDATED: FileDiff Panel - 17/17"

**RESULT**: 17/17 → BATCH 8 COMPLETE → Core features DONE

---

## PHASE 2: QUALITY ASSURANCE (Batches 9-10)

**Estimated**: 2 weeks
**Goal**: Integration testing, edge cases, performance validation

---

## BATCH 9: Integration Testing

**Priority**: CRITICAL (ensure all batches work together)
**Goal**: All features integrated and working together
**Estimated**: 1 week

### Integration Test Scenarios

**Scenario 1: Full Stack - Research → Agents → Decisions → Execution**
1. [ ] shannon do "build complex app" --dashboard (uses research, agents, decisions)
2. [ ] Playwright validates: Research panel → Agent pool → Decision approval → Validation streaming → FileDiff
3. [ ] All panels update correctly
4. [ ] All features integrated

**Scenario 2: Multi-Agent with Decisions**
5. [ ] Task requires 8 agents AND has decision point
6. [ ] Agents spawn, decision presented, approval works, execution continues
7. [ ] Playwright validates full flow

**Scenario 3: Ultrathink → Execute**
8. [ ] shannon ultrathink "task" --then-execute
9. [ ] 500+ reasoning completes → Decision made → Execution starts automatically
10. [ ] Validates ultrathink feeds into execution

**Scenario 4: Interactive Steering**
11. [ ] Start task → HALT → INJECT constraint → RESUME
12. [ ] Constraint applied → REDIRECT → New plan → Execution continues
13. [ ] Validates all controls work together

**Scenario 5: Error Handling**
14. [ ] Task that fails validation
15. [ ] ROLLBACK triggered
16. [ ] State restored correctly
17. [ ] User can retry or abandon

### Test Matrix

| Feature 1 | Feature 2 | Feature 3 | Validated |
|-----------|-----------|-----------|-----------|
| Multi-file | Agent pool | Decisions | [ ] |
| Research | Ultrathink | Execute | [ ] |
| HALT | INJECT | RESUME | [ ] |
| Agents | Decisions | Validation | [ ] |
| ROLLBACK | Re-execute | Success | [ ] |

**Validation**: ALL 25 combinations tested and working

---

## BATCH 10: Edge Cases + Performance

**Priority**: HIGH (production readiness)
**Goal**: Handle edge cases, meet performance requirements
**Estimated**: 1 week

### Edge Case Testing

**Edge Case 1: Capacity Limits**
- [ ] Spawn 8 agents (max) → 9th attempt fails gracefully
- [ ] Error message clear
- [ ] Dashboard shows capacity warning

**Edge Case 2: Network Failures**
- [ ] WebSocket disconnects mid-execution
- [ ] Auto-reconnect works
- [ ] State syncs after reconnect

**Edge Case 3: Invalid Inputs**
- [ ] shannon do "" (empty task) → Error message
- [ ] shannon research "!!!" (garbage query) → Handled gracefully
- [ ] Invalid file paths → Clear error

**Edge Case 4: Resource Exhaustion**
- [ ] Extremely long task (100+ steps)
- [ ] Memory usage stays reasonable
- [ ] Dashboard doesn't freeze

### Performance Testing

**Latency Requirements** (from spec):
- [ ] HALT response: < 100ms (avg < 50ms)
- [ ] Event streaming: < 50ms (Playwright timestamp correlation)
- [ ] Dashboard updates: < 100ms (smooth animations)

**Throughput Testing**:
- [ ] 8 concurrent agents execute without blocking
- [ ] 1000 validation output lines stream smoothly
- [ ] 50 decision points handled without memory leak

**Validation**: All performance requirements met

---

## PHASE 3: RELEASE (Batch 11)

**Estimated**: 3-5 days
**Goal**: Documentation, version bump, release

---

## BATCH 11: Documentation + Release

**Priority**: FINAL
**Goal**: Production-ready v4.0.0 release
**Estimated**: 3-5 days

### Documentation Tasks

1. [ ] Update README.md:
   - Add V4 features section
   - Document all 6 commands with examples
   - Add dashboard panel descriptions
   - Include screenshots
2. [ ] Update CHANGELOG.md:
   - Add v4.0.0 section
   - List all new features (batches 1-8)
   - Note breaking changes (if any)
3. [ ] Create docs/USAGE_GUIDE_V4.md:
   - Getting started guide
   - Each command with examples
   - Dashboard guide
   - Troubleshooting
4. [ ] Create docs/ARCHITECTURE_V4.md:
   - System architecture diagram
   - Component interactions
   - Event flow documentation

### Release Tasks

5. [ ] Bump version to 4.0.0:
   - pyproject.toml
   - src/shannon/__version__.py
   - package.json (dashboard)
6. [ ] Final smoke test:
   - shannon --version shows 4.0.0
   - All commands work
   - Dashboard connects
7. [ ] Tag release:
   - git tag v4.0.0
   - git push --tags
8. [ ] Create GitHub release notes

### VALIDATION GATE 11 (FINAL)

**Cannot release until:**
1. [ ] README.md complete (5+ pages)
2. [ ] CHANGELOG.md has v4.0.0 entry
3. [ ] Usage guide complete (20+ pages)
4. [ ] Architecture docs complete
5. [ ] Version shows 4.0.0 everywhere
6. [ ] All batches 1-10 validated
7. [ ] pytest: All tests pass
8. [ ] Tag v4.0.0 created
9. [ ] Release notes published

**RESULT**: 9/9 → SHANNON V4.0.0 RELEASED

---

## EXECUTION PROTOCOL

### Starting a Batch

1. Read plan for batch N
2. Review implementation steps
3. Create TodoWrite todos for each step
4. Begin implementation (back-end first, then front-end)

### During Batch Execution

1. Implement each step
2. Write unit tests as you go
3. Run tests frequently (catch issues early)
4. Mark todos as completed

### Validation Gate Protocol

1. **Run ALL validation criteria** (automated script ideal)
2. **Check each criterion**: PASS or FAIL
3. **IF ALL PASS**:
   - Capture evidence (screenshots, logs)
   - Commit with "VALIDATED: [Batch Name] - X/X criteria"
   - Proceed to next batch
4. **IF ANY FAIL**:
   - Identify failing criteria
   - Debug root cause
   - Fix issue
   - Re-run ENTIRE validation gate
   - Repeat until ALL pass

### Evidence Requirements

**For each batch, commit:**
- Playwright screenshots (batch#-[feature]-validated.png)
- Terminal output logs (batch#_validation.log)
- Commit message with validation count

**Example commit**:
```
feat: Agent Pool with parallel execution

VALIDATED: Batch 2 - 32/32 criteria passed

Backend:
- AgentPool.spawn_agent() with capacity limits
- Orchestrator parallel execution
- agent:spawned, agent:completed events

Frontend:
- AgentPool panel shows active agents
- Real-time count updates
- Progress bars visible

Playwright verification:
- 3 agents spawned and displayed
- Active count: "3 active / 8 max"
- All agents complete successfully

Screenshot: batch2-agent-pool-validated.png
Validation log: batch2_validation.log

No regressions, all 231 tests passing
```

---

## BATCH DEPENDENCY GRAPH

```
BATCH 1 (Multi-file)
  ↓
BATCH 2 (Agent Pool) ← Needs multi-file for complex tests
  ↓
BATCH 3 (Decisions) ← Needs agents for decision contexts
  ↓
BATCH 4 (Validation Streaming) ← Enables validation of 5-6
  ↓ ↓
BATCH 5 (Research) ← Can use decisions + validation
BATCH 6 (Ultrathink) ← Can use research + validation
  ↓ ↓
BATCH 7 (Controls) ← Controls all previous features
  ↓
BATCH 8 (FileDiff) ← Nice-to-have
  ↓
BATCH 9 (Integration Testing) ← Tests all combinations
  ↓
BATCH 10 (Edge Cases) ← Polish and performance
  ↓
BATCH 11 (Release) ← Documentation and publish
```

**Must execute in order** - Each batch depends on previous batches working.

---

## NOT INCLUDED (Deferred)

**shannon debug command**:
- User said don't prioritize
- Defer to v4.1 or later
- Focus on user priorities first

---

## REALISTIC TIMELINE

**Batch Implementation** (Batches 1-8):
- 8 batches × 2.5 hours avg = 20 hours
- Validation time = 10 hours
- Bug fixing = 10 hours
- **Subtotal: 40 hours (1-2 weeks intensive)**

**QA Phase** (Batches 9-10):
- Integration testing: 1 week
- Edge cases: 1 week
- **Subtotal: 2 weeks**

**Release** (Batch 11):
- Documentation: 2-3 days
- Release prep: 1-2 days
- **Subtotal: 3-5 days**

**TOTAL: 4-5 weeks** (not 17 weeks!)

---

## SUCCESS METRICS

**After each batch:**
- Feature X is PROVEN functional (not "infrastructure ready")
- Playwright screenshot evidence
- No regressions

**After Batch 8:**
- All user priorities implemented
- All features validated
- Ready for integration testing

**After Batch 10:**
- Production ready
- All edge cases handled
- Performance requirements met

**After Batch 11:**
- Shannon V4.0.0 released
- Documentation complete
- Users can adopt immediately

---

## CURRENT STATUS

✅ **Phase 0 Complete**: Git bug fixed (commit 5658707)
📋 **Ready to Execute**: Batch 1 (Multi-File Generation)
🎯 **Next Step**: Begin Batch 1 implementation

**Awaiting user approval to begin Batch 1 execution.**
