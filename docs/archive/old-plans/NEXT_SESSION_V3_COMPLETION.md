# Shannon V3 Completion Plan - Next Session
## Complete Remaining 30% with Functional Validation

> **For Claude:** Use systematic-debugging skill for issues, playwright-skill for all dashboard testing, test-driven-development for new features

**Current Status**: V3 70% complete (5 of 8 features integrated)
**Goal**: Achieve V3 100% complete with full functional validation
**Estimated**: 10-12 hours (single focused session or 2 shorter sessions)
**Testing**: NO pytest - functional shell scripts + Playwright only

---

## Prerequisites (15 minutes)

### LOAD CONTEXT

**Serena Memory**:
```python
mcp__serena__activate_project("shannon-cli")
mcp__serena__read_memory("V3_INTEGRATION_SESSION_20251117")
```

**Read Summaries**:
- `FINAL_SESSION_SUMMARY.md` (complete overview)
- `SESSION_V3_INTEGRATION_COMPLETE.md` (detailed process)
- `docs/plans/2025-11-13-shannon-cli-v3-full-implementation-design.md` (V3 spec)

**Verify Commits**:
```bash
git log --oneline -6
# Should see: d6e058a, 7c6b679, 1ed0bc8, 6e01ba0, b9926f0, 9832d11
```

**Current State Checklist**:
- [ ] At commit d6e058a or later
- [ ] V3 features integrated: cache, cost, analytics, MCP
- [ ] 5 shell scripts exist in tests/functional/
- [ ] Dashboard code exists
- [ ] Working directory: /Users/nick/Desktop/shannon-cli

---

## Phase 1: Fix WebSocket Server (1-2 hours)

### CRITICAL PATH - Blocks all dashboard testing

**Current Problem**: Server exits after startup instead of staying running

#### Task 1.1: Diagnose Server Exit Issue

**Skill**: Use `systematic-debugging` skill

**Steps**:
1. Read server/app.py completely:
   ```python
   mcp__serena__read_file("src/shannon/server/app.py")
   ```

2. Check how server is started:
   ```bash
   grep -n "uvicorn" src/shannon/server/app.py
   grep -n "if __name__" src/shannon/server/app.py
   ```

3. Run server with verbose logging:
   ```bash
   cd /Users/nick/Desktop/shannon-cli
   python -m shannon.server.app 2>&1 | tee server_debug.log
   # Observe: Does it exit immediately? Error messages?
   ```

4. Common causes to check:
   - Missing `reload=False` in uvicorn.run()
   - Exception in startup event handler
   - Port already in use
   - FastAPI async event loop issues

**Validation Gate 1.1**:
- [ ] Root cause identified
- [ ] Documented in server_debug.log or notes
- [ ] Ready to implement fix

---

#### Task 1.2: Fix Server Startup

**Steps**:
1. Fix identified issue in server/app.py

   Common fix patterns:
   ```python
   # Ensure blocking run
   if __name__ == "__main__":
       uvicorn.run(
           app,
           host="0.0.0.0",
           port=8000,
           log_level="info",
           reload=False  # Disable reload for stability
       )
   ```

2. Test server stays running:
   ```bash
   python -m shannon.server.app &
   SERVER_PID=$!
   sleep 10

   # Check if still running
   ps -p $SERVER_PID || fail "Server exited"

   # Check responds
   curl http://localhost:8000 || fail "Server not responding"

   kill $SERVER_PID
   ```

3. Commit fix:
   ```bash
   git add src/shannon/server/app.py
   git commit -m "fix: WebSocket server persistence

   Fixed server exiting after startup:
   - [specific fix applied]
   - Server now runs persistently
   - Dashboard can maintain connection

   Tested: Server runs 10+ seconds without exit
   Next: Dashboard connection test"
   ```

**Validation Gate 1.2**:
- [ ] Server runs persistently (60+ seconds)
- [ ] curl http://localhost:8000 succeeds
- [ ] No errors in logs
- [ ] Commit created
- [ ] Exit code 0

---

#### Task 1.3: Verify Dashboard Connection

**Skill**: Use `playwright-skill` for verification

**Steps**:
1. Start server in background:
   ```bash
   python -m shannon.server.app > /dev/null 2>&1 &
   SERVER_PID=$!
   sleep 3
   ```

2. Start dashboard:
   ```bash
   cd dashboard
   npm run dev > /dev/null 2>&1 &
   DASHBOARD_PID=$!
   sleep 5
   ```

3. Test with Playwright:
   ```python
   # Navigate to dashboard
   mcp__playwright__browser_navigate(url="http://localhost:5176")

   # Wait for connection
   mcp__playwright__browser_wait_for(text="Connected", timeout=10000)

   # Take screenshot
   mcp__playwright__browser_take_screenshot(filename="dashboard-connected.png")
   ```

4. Verify connection indicator:
   - Should show "Connected" in green
   - Should show "http://localhost:8000"
   - Should NOT show "Disconnected" in red

5. Kill processes:
   ```bash
   kill $SERVER_PID $DASHBOARD_PID
   ```

**Validation Gate 1.3**:
- [ ] Playwright sees "Connected" text
- [ ] Screenshot shows green connection indicator
- [ ] No WebSocket errors in console
- [ ] Dashboard functional
- [ ] Exit code 0

**PHASE 1 COMPLETE WHEN**:
✅ Server runs persistently
✅ Dashboard connects successfully
✅ Playwright verification passed
✅ Screenshot evidence: dashboard-connected.png

---

## Phase 2: Agent Tracking Integration (3-4 hours)

### Integrate AgentStateTracker with wave execution

**Current State**: AgentStateTracker code exists (546 lines), not wired into wave command

#### Task 2.1: Design Agent Event Capture

**Skill**: Use `systematic-debugging` to trace event flow

**Steps**:
1. Read agent tracking implementation:
   ```python
   mcp__serena__read_file("src/shannon/agents/state_tracker.py")
   mcp__serena__read_file("src/shannon/agents/controller.py")
   ```

2. Understand required events:
   - agent:spawned (when agent starts)
   - agent:progress (during execution)
   - agent:completed (when done)
   - agent:failed (on error)

3. Check where Shannon Framework emits these:
   - During /shannon:wave execution
   - Need to capture from SDK message stream
   - Parse for agent-related events

4. Design integration points:
   ```python
   # In wave command:
   # 1. Initialize AgentStateTracker before wave
   # 2. During message streaming, detect agent events
   # 3. Update tracker with agent states
   # 4. Emit to dashboard client if present
   ```

5. Document design:
   ```bash
   cat > AGENT_INTEGRATION_DESIGN.md << 'EOF'
   # Agent Tracking Integration Design

   Event Flow:
   Shannon Framework → SDK messages → Wave command → AgentStateTracker → Dashboard

   [detailed design notes]
   EOF
   ```

**Validation Gate 2.1**:
- [ ] agent_state_tracker.py read completely
- [ ] Event types documented
- [ ] Integration design written
- [ ] Clear implementation plan

---

#### Task 2.2: Implement Agent Tracking in Wave Command

**Skill**: Use `test-driven-development` skill for correct implementation

**Steps**:
1. Add AgentStateTracker to wave command:
   ```python
   # In src/shannon/cli/commands.py wave() function

   # Initialize agent tracker
   if orchestrator and orchestrator.agents:
       agent_tracker = orchestrator.agents
       agent_tracker.start_wave(wave_number=1)

   # During message streaming
   async for msg in wave_iter:
       messages.append(msg)

       # Check for agent events
       if hasattr(msg, 'type') and 'agent' in msg.type.lower():
           # Parse agent event
           agent_data = parse_agent_event(msg)

           # Update tracker
           if agent_data:
               agent_tracker.update_agent(
                   agent_id=agent_data['id'],
                   status=agent_data['status'],
                   progress=agent_data.get('progress', 0.0)
               )

               # Emit to dashboard if connected
               if dashboard_client:
                   await dashboard_client.emit_event('agent:updated', agent_data)
   ```

2. Compile and check syntax:
   ```bash
   python -m py_compile src/shannon/cli/commands.py
   ```

3. Commit:
   ```bash
   git add src/shannon/cli/commands.py
   git commit -m "feat: Integrate agent tracking into wave command

   AgentStateTracker now captures agent events during wave:
   - Detects agent:spawned, agent:progress, agent:completed
   - Updates agent states in tracker
   - Emits to dashboard for real-time display

   Next: Test wave command shows agents"
   ```

**Validation Gate 2.2**:
- [ ] Code compiles (syntax valid)
- [ ] AgentStateTracker initialized in wave
- [ ] Agent events captured from messages
- [ ] Dashboard events emitted
- [ ] Commit created

---

#### Task 2.3: Implement wave agents Command

**Steps**:
1. Find where wave agents command is defined:
   ```bash
   grep -n "def wave_agents" src/shannon/cli/commands.py
   ```

2. Implement list functionality:
   ```python
   @cli.command('wave-agents')
   @click.option('--session-id', help='Session ID (uses latest if not provided)')
   def wave_agents(session_id: Optional[str]) -> None:
       """List active agents in current wave.

       Shows agent status, progress, and metrics.
       """
       from rich.console import Console
       from rich.table import Table
       from shannon.config import ShannonConfig
       from shannon.core.session_manager import SessionManager

       config = ShannonConfig()
       console = Console()

       # Load session
       if not session_id:
           sessions = SessionManager.list_all_sessions(config)
           if not sessions:
               console.print("[yellow]No sessions found[/yellow]")
               return
           session_id = sessions[-1]

       session = SessionManager(session_id, config)

       # Get agent states from tracker
       # (Stored in session or orchestrator state)
       agents = session.read_memory('active_agents') or []

       if not agents:
           console.print("[dim]No active agents[/dim]")
           return

       # Display agents table
       table = Table(title="Active Agents")
       table.add_column("ID", style="cyan")
       table.add_column("Type", style="green")
       table.add_column("Status")
       table.add_column("Progress", justify="right")
       table.add_column("Duration")

       for agent in agents:
           table.add_row(
               agent['id'][:8],
               agent['type'],
               agent['status'],
               f"{agent.get('progress', 0):.0f}%",
               f"{agent.get('duration', 0):.1f}s"
           )

       console.print(table)
   ```

3. Test command:
   ```bash
   shannon wave-agents
   # Should show table or "No active agents"
   ```

4. Commit:
   ```bash
   git add src/shannon/cli/commands.py
   git commit -m "feat: Implement wave-agents command

   Lists active agents with status table:
   - Agent ID, type, status, progress, duration
   - Uses Rich table formatting
   - Loads from session agent state

   Tested: shannon wave-agents shows table
   Next: Test with actual wave execution"
   ```

**Validation Gate 2.3**:
- [ ] wave-agents command implemented
- [ ] Shows Rich table
- [ ] Displays agent information
- [ ] Tested (shows "No active agents" or actual agents)
- [ ] Commit created

---

#### Task 2.4: Functional Testing - Agent Tracking

**Create**: tests/functional/test_agents.sh

**Content**:
```bash
#!/bin/bash
# Shannon V3 Agent Tracking - Functional Test

set -e

echo "Testing agent tracking feature..."

# Test 1: wave-agents command exists
shannon wave-agents || fail "wave-agents command not found"
echo "✓ wave-agents command exists"

# Test 2: During wave execution (requires API key)
# shannon wave "complex task" should spawn agents
# shannon wave-agents should show them
# Playwright should see them in AgentPool panel

# Test 3: Agent state persistence
# Agents should be saved to session
# Rerunning wave-agents should show same agents

echo "✓ Agent tracking tests complete"
```

**Run Test**:
```bash
bash tests/functional/test_agents.sh
```

**Validation Gate 2.4**:
- [ ] test_agents.sh created and executable
- [ ] Test passes (exit 0)
- [ ] Agent tracking validated functionally
- [ ] Commit created

---

#### Task 2.5: Playwright - Verify AgentPool Panel

**Skill**: Use `playwright-skill` for comprehensive dashboard testing

**Steps**:
1. Start server and dashboard:
   ```bash
   python -m shannon.server.app > /dev/null 2>&1 &
   cd dashboard && npm run dev > /dev/null 2>&1 &
   sleep 5
   ```

2. Navigate to dashboard:
   ```python
   mcp__playwright__browser_navigate(url="http://localhost:5176")
   mcp__playwright__browser_wait_for(text="Connected", timeout=10000)
   ```

3. Run wave that spawns agents:
   ```bash
   # In separate terminal
   cd /tmp/agent-test
   shannon wave "analyze codebase and run tests" --dashboard
   ```

4. Verify agents appear in panel:
   ```python
   # Wait for agents to appear
   mcp__playwright__browser_wait_for(text="active", timeout=30000)

   # Check agent count
   mcp__playwright__browser_snapshot()
   # Should see agents in AgentPool section

   # Screenshot
   mcp__playwright__browser_take_screenshot(filename="agent-pool-active.png")
   ```

5. Verify agent details:
   - Agent ID shown
   - Agent type/role shown
   - Status indicator (running/complete)
   - Progress bar if running

**Validation Gate 2.5**:
- [ ] Playwright sees AgentPool panel
- [ ] Agents visible during wave execution
- [ ] Status updates in real-time
- [ ] Screenshot: agent-pool-active.png
- [ ] Panel functional ✅

**PHASE 2 COMPLETE WHEN**:
✅ AgentStateTracker integrated into wave command
✅ wave-agents command functional
✅ test_agents.sh passing
✅ Playwright verification: agents visible in dashboard
✅ Screenshot evidence
✅ All commits created

---

## Phase 3: Context Management Completion (3-4 hours)

### Complete shannon onboard workflow with Serena integration

**Current State**: Context modules exist (2,709 lines), onboarding workflow incomplete

#### Task 3.1: Read Context Implementation

**Steps**:
1. Read all context modules completely:
   ```python
   mcp__serena__read_file("src/shannon/context/manager.py")
   mcp__serena__read_file("src/shannon/context/onboarder.py")
   mcp__serena__read_file("src/shannon/context/serena_adapter.py")
   mcp__serena__read_file("src/shannon/context/primer.py")
   ```

2. Understand onboarding workflow:
   - CodebaseOnboarder scans directory tree
   - Extracts tech stack, patterns, critical files
   - SerenaAdapter stores in knowledge graph
   - ContextPrimer enables quick reload

3. Check if shannon onboard command exists:
   ```bash
   shannon onboard --help 2>&1
   # If exists: check what it does
   # If not: needs implementation
   ```

**Validation Gate 3.1**:
- [ ] All 4 context files read completely
- [ ] Onboarding workflow understood
- [ ] Current command status known
- [ ] Implementation plan clear

---

#### Task 3.2: Implement or Fix shannon onboard Command

**Skill**: Use `test-driven-development` for correctness

**Steps**:
1. Check current implementation:
   ```bash
   grep -n "def onboard" src/shannon/cli/commands.py -A 30
   ```

2. If incomplete, implement:
   ```python
   @cli.command('onboard')
   @click.argument('project_path', type=click.Path(exists=True))
   @click.option('--project-id', help='Project ID (defaults to directory name)')
   def onboard(project_path: str, project_id: Optional[str]) -> None:
       """Onboard a codebase for context-aware analysis.

       Scans codebase and stores structure in Serena knowledge graph
       for fast context loading in future analyses.

       Example:
           shannon onboard /path/to/project
           shannon onboard ../my-app --project-id my_app
       """
       from pathlib import Path
       from rich.console import Console
       from shannon.context.manager import ContextManager
       from shannon.config import ShannonConfig

       console = Console()
       project_path = Path(project_path).resolve()

       if not project_id:
           project_id = project_path.name

       console.print(f"\n[bold cyan]Onboarding Project:[/bold cyan] {project_id}")
       console.print(f"[dim]Path: {project_path}[/dim]\n")

       try:
           config = ShannonConfig()
           context_mgr = ContextManager()

           # Run onboarding
           with console.status("[yellow]Scanning codebase..."):
               result = asyncio.run(context_mgr.onboard_project(
                   project_path=project_path,
                   project_id=project_id
               ))

           # Display results
           console.print("[green]✓[/green] Onboarding complete\n")
           console.print(f"Files scanned: {result['files_count']}")
           console.print(f"Tech stack: {', '.join(result['tech_stack'])}")
           console.print(f"Modules found: {result['modules_count']}")
           console.print(f"Stored in Serena: {result['entities_created']} entities\n")

           console.print(f"[dim]Project ID: {project_id}[/dim]")
           console.print(f"[dim]Use: shannon analyze spec.md --project {project_id}[/dim]\n")

       except Exception as e:
           console.print(f"[red]Error:[/red] Onboarding failed: {e}\n")
           sys.exit(1)
   ```

3. Test command:
   ```bash
   # Create test project
   mkdir -p /tmp/test-onboard-project/src
   echo "print('hello')" > /tmp/test-onboard-project/src/main.py
   echo "# Test Project" > /tmp/test-onboard-project/README.md

   # Run onboard
   shannon onboard /tmp/test-onboard-project
   ```

4. Commit:
   ```bash
   git add src/shannon/cli/commands.py
   git commit -m "feat: Complete shannon onboard command implementation

   Onboarding workflow:
   - Scans project directory tree
   - Detects tech stack and patterns
   - Stores in Serena knowledge graph
   - Displays summary (files, modules, tech stack)

   Tested: shannon onboard /tmp/test-project completes
   Next: Verify Serena storage and context-aware analysis"
   ```

**Validation Gate 3.2**:
- [ ] shannon onboard command works
- [ ] Completes without errors
- [ ] Displays summary (files, tech stack, modules)
- [ ] Functional test passes
- [ ] Commit created

---

#### Task 3.3: Verify Serena Knowledge Graph Storage

**Steps**:
1. After onboarding, check Serena has entities:
   ```python
   # Read knowledge graph
   mcp__serena__read_memory("project_test-onboard-project")
   # Or search for entities
   mcp__serena__search_for_pattern(
       substring_pattern="test-onboard-project",
       relative_path=""
   )
   ```

2. Verify entities exist:
   - Project entity
   - File entities
   - Module entities
   - Relationships between them

3. If entities missing, debug SerenaAdapter:
   ```python
   mcp__serena__read_file("src/shannon/context/serena_adapter.py")
   # Check create_entities() method
   # Check if actually called during onboard
   ```

**Validation Gate 3.3**:
- [ ] Serena knowledge graph has project entities
- [ ] Entity count matches onboard summary
- [ ] Relationships created
- [ ] Can query for project in Serena

---

#### Task 3.4: Test Context-Aware Analysis

**Steps**:
1. Run analysis with project context:
   ```bash
   cd /tmp/test-onboard-project

   # Create spec referencing project
   cat > spec.md << 'EOF'
   Add user authentication to this project.
   Use existing patterns and tech stack.
   EOF

   # Run with --project flag
   shannon analyze spec.md --project test-onboard-project
   ```

2. Verify context is used:
   - Check logs for "Loaded context for project"
   - Check if analysis mentions existing patterns
   - Check if recommendations align with tech stack

3. Test context shows in orchestrator:
   ```python
   # orchestrator should load project context
   # _build_context_prompt() should inject it
   # Analysis should be context-aware
   ```

**Validation Gate 3.4**:
- [ ] shannon analyze --project works
- [ ] Context loaded (check logs)
- [ ] Analysis is context-aware
- [ ] Functional test passes

---

#### Task 3.5: Create Context Functional Test

**Create**: tests/functional/test_context.sh

**Content**:
```bash
#!/bin/bash
# Shannon V3 Context Management - Functional Test

set -e

# Test 1: shannon onboard command
mkdir -p /tmp/ctx-test/src
echo "test" > /tmp/ctx-test/src/app.py
shannon onboard /tmp/ctx-test || fail "Onboard failed"

# Test 2: shannon context status
shannon context status | grep "Projects: 1" || fail "Project not recorded"

# Test 3: Context-aware analysis
cd /tmp/ctx-test
shannon analyze <(echo "Add feature") --project ctx-test || true
# Check logs for context loading

echo "✓ Context management functional"
```

**Run**:
```bash
bash tests/functional/test_context.sh
```

**Commit**:
```bash
git add tests/functional/test_context.sh
git commit -m "test: Add context management functional test

Tests shannon onboard and context-aware analysis
NO pytest - functional shell script

Validates:
✅ Onboarding workflow
✅ Serena storage
✅ Context loading in analysis
✅ shannon context commands"
```

**Validation Gate 3.5**:
- [ ] test_context.sh created
- [ ] Test passes (exit 0)
- [ ] Context feature validated functionally
- [ ] Commit created

**PHASE 3 COMPLETE WHEN**:
✅ shannon onboard command functional
✅ Serena knowledge graph stores project data
✅ Context-aware analysis works (--project flag)
✅ test_context.sh passing
✅ shannon context status shows projects
✅ All commits created

---

## Phase 4: Comprehensive Functional Testing (2-3 hours)

### Run all tests and fix discovered issues

#### Task 4.1: Run All Shell Scripts

**Steps**:
1. Ensure ANTHROPIC_API_KEY is set:
   ```bash
   echo $ANTHROPIC_API_KEY
   # Must be set for tests that run analyze
   ```

2. Run master test suite:
   ```bash
   cd /Users/nick/Desktop/shannon-cli
   bash tests/functional/run_all.sh 2>&1 | tee test_results.log
   ```

3. Check results:
   ```bash
   grep "PASSED\|FAILED\|SKIPPED" test_results.log
   # Count each category
   ```

4. For each failure:
   - Read test output
   - Identify root cause (use systematic-debugging skill if complex)
   - Fix issue
   - Re-run test
   - Commit fix

**Validation Gate 4.1**:
- [ ] All shell scripts executed
- [ ] Pass/fail/skip counts recorded
- [ ] All failures diagnosed
- [ ] Fixes implemented
- [ ] 100% pass rate achieved

---

#### Task 4.2: Dashboard E2E Testing with Playwright

**Skill**: Use `playwright-skill` for complete dashboard validation

**Test Each Panel**:

**Panel 1: ExecutionOverview**
```python
# Start execution
shannon do "create test.py" --dashboard &

# Playwright
mcp__playwright__browser_navigate("http://localhost:5176")
mcp__playwright__browser_wait_for(text="Connected")
mcp__playwright__browser_wait_for(text="create test.py")  # Task name

# Verify
mcp__playwright__browser_snapshot()
# Should show: task name, status (active), progress (updating)

# Screenshot
mcp__playwright__browser_take_screenshot(filename="panel-execution.png")
```

**Panel 2: Skills**
```python
# During execution, skills should appear
mcp__playwright__browser_wait_for(text="skill", timeout=15000)

# Verify skills list populates
mcp__playwright__browser_snapshot()

# Screenshot
mcp__playwright__browser_take_screenshot(filename="panel-skills.png")
```

**Panel 3: Validation**
```python
# Run task with tests
shannon do "run pytest tests/" --dashboard &

# Wait for output
mcp__playwright__browser_wait_for(text="test", timeout=20000)

# Verify output streaming
mcp__playwright__browser_snapshot()
# Should show green/red test output lines

# Screenshot
mcp__playwright__browser_take_screenshot(filename="panel-validation.png")
```

**Panel 4: File Changes**
```python
# Run task that creates file
shannon do "create hello.py" --dashboard &

# Wait for file event
mcp__playwright__browser_wait_for(text="hello.py", timeout=15000)

# Verify file shown with diff
mcp__playwright__browser_snapshot()

# Screenshot
mcp__playwright__browser_take_screenshot(filename="panel-files.png")
```

**Panel 5: AgentPool** (if Phase 2 complete)
```python
# Run multi-agent wave
shannon wave "complex multi-step task" --dashboard &

# Wait for agents
mcp__playwright__browser_wait_for(text="active", timeout=20000)

# Verify agents listed
mcp__playwright__browser_snapshot()

# Screenshot
mcp__playwright__browser_take_screenshot(filename="panel-agents.png")
```

**Panel 6: Decisions** (if implemented)
```python
# Trigger decision point
# Verify decision card appears
# Verify options shown
# Test approve button

# Screenshot
mcp__playwright__browser_take_screenshot(filename="panel-decisions.png")
```

**Validation Gate 4.2**:
- [ ] All 4-6 panels tested with Playwright
- [ ] Each panel renders correctly
- [ ] Events flow properly
- [ ] 4-6 screenshots saved as evidence
- [ ] No console errors
- [ ] Dashboard fully functional ✅

---

#### Task 4.3: Create Dashboard E2E Test Script

**Create**: tests/functional/test_dashboard_e2e.sh

**Content**:
```bash
#!/bin/bash
# Shannon Dashboard E2E - Functional Test with Playwright

# Start server + dashboard
# Run Playwright tests for each panel
# Verify all panels functional
# Save screenshots

# Uses Playwright MCP - NO pytest
```

**Validation Gate 4.3**:
- [ ] test_dashboard_e2e.sh created
- [ ] Uses Playwright for all UI testing
- [ ] Tests all panels
- [ ] NO pytest - functional only
- [ ] Commit created

**PHASE 4 COMPLETE WHEN**:
✅ All shell scripts passing (run_all.sh exit 0)
✅ All dashboard panels tested with Playwright
✅ Screenshots for each panel
✅ test_dashboard_e2e.sh created
✅ No regressions in existing features
✅ 100% functional validation achieved

---

## Phase 5: Documentation & V3 Completion (1-2 hours)

### Final polish and documentation

#### Task 5.1: Update README.md

**Steps**:
1. Read current README:
   ```python
   mcp__serena__read_file("README.md")
   ```

2. Add V3 Features section:
   ```markdown
   ## V3 Features

   ### 🚀 Live Metrics Dashboard
   Real-time progress tracking with 4 FPS refresh rate
   ```
   shannon analyze spec.md
   # Press Enter for detailed view
   ```

   ### 💾 Multi-Level Caching
   Instant results for repeated analyses (50%+ hit rate)
   ```
   shannon cache stats
   shannon cache clear
   ```

   ### 💰 Cost Optimization
   Automatic model selection and budget enforcement
   ```
   shannon budget status
   shannon budget set 50
   ```

   [... document all 8 features]
   ```

3. Add testing documentation:
   ```markdown
   ## Testing

   Shannon uses functional testing (NO pytest):
   ```bash
   # Run all functional tests
   bash tests/functional/run_all.sh

   # Individual feature tests
   bash tests/functional/test_cache.sh
   bash tests/functional/test_cost.sh
   ```

   Dashboard testing uses Playwright for browser automation.
   ```

4. Commit:
   ```bash
   git add README.md
   git commit -m "docs: Add V3 features to README

   Documented all 8 V3 features:
   - Live metrics dashboard
   - Multi-level caching
   - Cost optimization
   - MCP auto-installation
   - Agent tracking
   - Historical analytics
   - Context management
   - Full integration via Orchestrator

   Added testing documentation (functional, NO pytest)"
   ```

**Validation Gate 5.1**:
- [ ] README.md updated
- [ ] All V3 features documented
- [ ] Examples provided
- [ ] Testing section added
- [ ] Commit created

---

#### Task 5.2: Update CHANGELOG.md

**Steps**:
1. Add v3.0.0 release section:
   ```markdown
   ## [3.0.0] - 2025-11-XX

   ### Added - 8 Major Features

   **Live Metrics Dashboard**
   - Real-time progress tracking with Rich terminal UI
   - 4 FPS refresh rate
   - Keyboard controls (Enter/Esc/q/p)
   - Cost and token tracking

   **Multi-Level Caching**
   - 3-tier cache system (analysis/command/MCP)
   - Context-aware cache keys
   - 7/30/90 day TTL by tier
   - LRU eviction (500MB limit)
   - Commands: cache stats, cache clear

   [... all features]

   ### Changed
   - analyze command now uses ContextAwareOrchestrator
   - Automatic cache checking and saving
   - Automatic cost optimization
   - Automatic analytics recording

   ### Testing
   - Switched to functional shell scripts (NO pytest)
   - Shannon mandate compliance
   - Playwright for dashboard E2E
   ```

2. Commit:
   ```bash
   git add CHANGELOG.md
   git commit -m "docs: Add v3.0.0 release notes to CHANGELOG

   Complete documentation of V3 changes:
   - 8 new features
   - ContextAwareOrchestrator integration
   - Testing philosophy (functional only)
   - Breaking changes (none - backward compatible)"
   ```

**Validation Gate 5.2**:
- [ ] CHANGELOG.md updated
- [ ] v3.0.0 section added
- [ ] All features listed
- [ ] Commit created

---

#### Task 5.3: Final V3 Success Criteria Check

**From V3 Plan (lines 653-682)**, verify ALL criteria met:

**Functional** (9/9):
- [ ] All 32 commands work correctly
- [ ] V2 commands unchanged (backward compatible)
- [ ] MessageParser bug fixed
- [ ] Live metrics dashboard functional
- [ ] Caching achieves 50%+ hit rate (measure after 10 runs)
- [ ] Cost optimization saves 30%+ (compare runs)
- [ ] Agent control enables debugging
- [ ] Analytics provides actionable insights
- [ ] Context management works with codebases

**Quality** (4/4):
- [ ] All functional tests pass (shell scripts)
- [ ] NO pytest usage
- [ ] Comprehensive documentation
- [ ] Clean code (type hints, docstrings)

**Performance** (4/4):
- [ ] Cache hits < 500ms (measure)
- [ ] Metrics dashboard 4 FPS (measure)
- [ ] Context loading < 30 seconds (measure)
- [ ] Memory < 200 MB during execution (measure)

**Integration** (3/3):
- [ ] All features work together via Orchestrator
- [ ] No feature fragmentation
- [ ] Clean interfaces between components

**Validation Gate 5.3**:
- [ ] All success criteria checked
- [ ] 100% criteria met
- [ ] Evidence documented
- [ ] V3 COMPLETE ✅

---

#### Task 5.4: Tag V3 Completion

**Steps**:
1. Final smoke test:
   ```bash
   # Test core workflow
   shannon analyze tests/fixtures/simple_spec.md
   shannon cache stats
   shannon budget status
   shannon analytics
   shannon context status

   # All should work without errors
   ```

2. Tag release:
   ```bash
   git tag -a v3.0.0-complete -m "Shannon CLI V3.0 Complete

   All 8 features integrated and functional:
   ✅ Live Metrics Dashboard
   ✅ Multi-Level Caching
   ✅ Cost Optimization
   ✅ MCP Auto-Installation
   ✅ Agent Tracking
   ✅ Historical Analytics
   ✅ Context Management
   ✅ Full Orchestrator Integration

   Tested: Functional shell scripts + Playwright E2E
   Philosophy: NO pytest (Shannon mandate)
   Status: Production ready"
   ```

3. Create completion summary:
   ```bash
   cat > V3_COMPLETE_FINAL.md << 'EOF'
   # Shannon V3.0 - COMPLETE

   [Summary of entire V3 journey]
   [All features listed]
   [Test results]
   [Screenshots]
   EOF

   git add V3_COMPLETE_FINAL.md
   git commit -m "docs: V3 completion summary"
   ```

**Validation Gate 5.4**:
- [ ] Final smoke test passes
- [ ] Tag v3.0.0-complete created
- [ ] Completion summary written
- [ ] All commits pushed (if applicable)
- [ ] V3.0 OFFICIALLY COMPLETE ✅

**PHASE 5 COMPLETE WHEN**:
✅ README and CHANGELOG updated
✅ All success criteria met and verified
✅ Tag created
✅ Completion documented
✅ Shannon CLI V3.0 production ready

---

## Execution Strategy

### Work Systematically (No Sub-Agents)
- Do all work yourself
- Read code completely before changing
- Test functionally after each change
- Commit incrementally
- No rushed agent dispatch

### Functional Testing Only (NO pytest)
- Use shell scripts (bash tests/functional/*.sh)
- Use actual CLI commands (shannon analyze, etc.)
- Use Playwright for dashboard (browser testing)
- Observe real behavior
- Check exit codes
- NO test_*.py files
- NO pytest

### Validation Gates Are Mandatory
- Cannot proceed to next task until current gate passed
- Each gate requires evidence (output/screenshot/test pass)
- If gate fails, debug and fix before continuing
- No skipping gates

### Skills to Use

**systematic-debugging**: When diagnosing any issue (server, agents, context)
**test-driven-development**: When building new features (onboard command)
**playwright-skill**: For ALL dashboard testing (every panel)
**honest-reflections**: Before claiming V3 complete (verify all criteria)

---

## Session Checklist

**At Start**:
- [ ] Load context from Serena
- [ ] Read FINAL_SESSION_SUMMARY.md
- [ ] Verify at correct commit (d6e058a+)
- [ ] Understand current state (70% complete)

**During Work**:
- [ ] Pass each validation gate before proceeding
- [ ] Test functionally (NO pytest)
- [ ] Commit after each task
- [ ] Take screenshots for evidence

**At End**:
- [ ] All 5 phases complete
- [ ] All validation gates passed
- [ ] V3 success criteria met (100%)
- [ ] Documentation complete
- [ ] Tag created
- [ ] Ready for users

---

## Estimated Timeline

**Single Focused Session** (10-12 hours):
- Phase 1: 1-2 hours
- Phase 2: 3-4 hours
- Phase 3: 3-4 hours
- Phase 4: 2-3 hours
- Phase 5: 1-2 hours

**Two Sessions** (5-6 hours each):
- Session 1: Phases 1-2 (server + agents)
- Session 2: Phases 3-5 (context + testing + docs)

**Buffer**: Add 20% for unexpected issues = 12-15 hours total

---

## Success Definition

**V3.0 Complete = ALL of:**
✅ All 8 features functional and integrated
✅ All shell scripts passing (run_all.sh exit 0)
✅ All dashboard panels working (Playwright verified)
✅ All V3 success criteria met (plan lines 653-682)
✅ Documentation complete (README, CHANGELOG)
✅ NO pytest files (Shannon mandate)
✅ Tag v3.0.0-complete created

**NOT complete until ALL checked.**

---

## Recovery Plan

**If stuck on any task**:
1. Use systematic-debugging skill
2. Read relevant code completely
3. Test functionally to isolate issue
4. Fix incrementally
5. Validate before proceeding

**If validation gate fails**:
1. Don't skip - diagnose why
2. Fix root cause
3. Re-test until passes
4. Document what was wrong

**If running out of time**:
1. Complete current phase
2. Commit progress
3. Write honest status update
4. Plan continuation for next session

---

## Next Session Commands

**To Start**:
```bash
cd /Users/nick/Desktop/shannon-cli
git status  # Should be on master, clean
git log --oneline -6  # Verify d6e058a present

# Load context
# Read FINAL_SESSION_SUMMARY.md
# Begin Phase 1
```

**Testing Throughout**:
```bash
# After each change
python -m py_compile [modified file]
bash tests/functional/[relevant test].sh

# Dashboard testing
# Use Playwright MCP for all UI verification
```

**At Completion**:
```bash
bash tests/functional/run_all.sh
# All tests passing

git tag v3.0.0-complete
git log --oneline -10
# Should show ~10-15 commits for complete V3 implementation
```

---

**Plan Status**: ✅ COMPLETE
**Validation Gates**: 20+ checkpoints defined
**Testing**: 100% functional (NO pytest)
**Skills**: Explicitly called out
**Ready**: For systematic V3 completion execution
