# Shannon V5 - CORRECT Architecture Plan
## Leveraging Claude Code Skills Properly

**Date**: 2025-11-17
**Analysis**: 200 ultrathinking thoughts
**Status**: ARCHITECTURAL RESET after discovering fundamental misunderstanding

---

## What I Learned About Claude Code Skills

### Claude Code Skills Are:
- ✅ Markdown files (SKILL.md) with YAML frontmatter + instructions
- ✅ Located in ~/.claude/skills/ or .claude/skills/
- ✅ Model-invoked: Claude decides when to use them
- ✅ Behavioral patterns that extend Claude's capabilities
- ✅ Work in Claude Code, Agent SDK, and plugins

### Claude Code Skills Are NOT:
- ❌ Python code with classes and methods
- ❌ YAML configuration files
- ❌ Custom frameworks you build
- ❌ Explicitly called by user code

---

## The Architectural Mistake

### What I Built (WRONG):
**Custom "skills framework"** (5,500 lines):
- src/shannon/skills/registry.py (SkillRegistry)
- src/shannon/skills/executor.py (SkillExecutor)
- src/shannon/skills/loader.py (SkillLoader)
- src/shannon/skills/discovery.py (DiscoveryEngine)
- src/shannon/orchestration/planner.py (ExecutionPlanner)
- src/shannon/orchestration/task_parser.py (TaskParser)
- schemas/skill.schema.json (YAML schema)

**Problem**: Tried to implement a parallel skills system competing with Shannon Framework.

**Result**:
- shannon do looks for YAML skills (code_generation.yaml, etc.)
- These skills don't exist
- Fails with "skills not found"
- 5,500 lines of code doing nothing

### What EXISTS and WORKS:
**Shannon Framework** (separate repo):
- ✅ 19 Claude Code skills with SKILL.md files
- ✅ spec-analysis, wave-orchestration, exec, task-automation, etc.
- ✅ Loaded as Claude Code plugin
- ✅ Claude can invoke these automatically

**Shannon CLI commands that USE these** (WORKING):
- ✅ shannon analyze → Invokes spec-analysis skill via `/spec` command
- ✅ shannon wave → Invokes wave-orchestration skill via SDK
- ✅ shannon exec → Invokes wave skill via CompleteExecutor

**These work BECAUSE they use Shannon Framework skills**, not custom framework.

---

## CORRECT V5 Architecture

### Core Principle: Thin Wrapper Around Claude Code Skills

```
┌─────────────────────────────────────────────────────────┐
│              Shannon CLI (Thin Wrapper)                 │
│                  ~15,000 lines                          │
├─────────────────────────────────────────────────────────┤
│  UnifiedOrchestrator (~600 lines):                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ V3 Intelligence (KEEP - adds value):              │  │
│  │  - CacheManager (before/after skill calls)       │  │
│  │  - AnalyticsDatabase (record sessions)           │  │
│  │  - ContextManager (project awareness)            │  │
│  │  - CostOptimizer (model selection, budget)       │  │
│  │  - MCPManager (auto-install MCPs)                │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Delegation Methods:                               │  │
│  │  execute_analysis() → invoke spec-analysis skill │  │
│  │  execute_wave() → invoke wave-orchestration      │  │
│  │  execute_task() → invoke task-automation skill   │  │
│  │  execute_exec() → delegate to CompleteExecutor   │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Commands (~2,000 lines):                               │
│   - shannon analyze, wave, do, exec                     │
│   - Each: ~60-80 lines (thin wrapper)                   │
├─────────────────────────────────────────────────────────┤
│  V3 Subsystems (KEEP - 10,641 lines):                   │
│   - cache/, analytics/, context/, optimization/,        │
│     mcp/, metrics/, agents/                             │
├─────────────────────────────────────────────────────────┤
│  V3.5 Executor (KEEP - 3,528 lines):                    │
│   - executor/ (CompleteExecutor - proven working)       │
├─────────────────────────────────────────────────────────┤
│  Infrastructure (KEEP - ~3,000 lines):                  │
│   - communication/, server/, orchestration/agent_pool,  │
│     orchestration/state_manager                         │
└─────────────────────────────────────────────────────────┘
                          ↓ Calls via Anthropic SDK
         ┌────────────────────────────────────────┐
         │   Claude (with Shannon Framework)      │
         ├────────────────────────────────────────┤
         │  Shannon Framework Plugin Loaded:      │
         │   - 19 Claude Code skills available    │
         │   - spec-analysis, wave-orchestration, │
         │     task-automation, exec, etc.        │
         │                                        │
         │  Claude uses skills to execute:        │
         │   - Analyzes specs                     │
         │   - Orchestrates waves                 │
         │   - Automates tasks                    │
         │   - Generates code                     │
         └────────────────────────────────────────┘
```

### DELETE (Custom Skills Framework):
- ❌ src/shannon/skills/ (entire directory - 5,500 lines)
- ❌ src/shannon/orchestration/planner.py
- ❌ src/shannon/orchestration/task_parser.py
- ❌ schemas/skill.schema.json

**Why**: Shannon Framework provides this via Claude Code skills.

### KEEP (V3 Intelligence):
- ✅ cache/, analytics/, context/, optimization/, mcp/, metrics/, agents/
- ✅ 10,641 lines that ADD value (caching, tracking, optimization)

### KEEP (Working Components):
- ✅ executor/ (V3.5 - CompleteExecutor proven working)
- ✅ communication/, server/ (WebSocket for dashboard)
- ✅ orchestration/agent_pool, state_manager (infrastructure)

### SIMPLIFY (UnifiedOrchestrator):
- Remove V4 initialization (skills_registry, planner, v4_executor)
- Keep V3 initialization
- Add execute_task() for shannon do
- ~600 lines focused on V3 wrapper + SDK delegation

---

## Correct Implementation

### UnifiedOrchestrator.execute_task()

```python
async def execute_task(
    self,
    task: str,
    dashboard_client: Optional[Any] = None,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Execute task via Shannon Framework task-automation skill.

    Wraps Shannon Framework skill with V3 features:
    - Cache check before execution
    - Cost optimization (model selection)
    - Dashboard streaming during execution
    - Cache save after execution
    - Analytics recording
    """

    # V3: Cache check
    if self.cache:
        cached_result = await self.cache.get(task)
        if cached_result:
            logger.info("Task cache hit - returning cached result")
            return cached_result

    # V3: Cost optimization
    model = 'sonnet'  # Default
    if self.model_selector and self.budget_enforcer:
        complexity_estimate = len(task) / 100  # Simple heuristic
        budget_status = self.budget_enforcer.get_status()

        selection = self.model_selector.select_optimal_model(
            agent_complexity=complexity_estimate,
            context_size_tokens=0,
            budget_remaining=budget_status.remaining
        )
        model = selection.model
        logger.info(f"Selected model: {model} (saves ${selection.savings_vs_sonnet:.2f})")

    # Execute via Shannon Framework task-automation skill
    logger.info(f"Invoking task-automation skill for: {task}")
    messages = []

    async for msg in self.sdk_client.query(
        prompt=f"@skill task-automation\n\nTask: {task}",
        model=model
    ):
        messages.append(msg)

        # Stream to dashboard
        if dashboard_client:
            await self._stream_message_to_dashboard(msg, dashboard_client)

    # Parse result from messages
    result = self._parse_task_result(messages)

    # V3: Save to cache
    if self.cache:
        await self.cache.save(task, result)
        logger.info("Task result cached")

    # V3: Record to analytics
    if self.analytics_db and session_id:
        await self.analytics_db.record_task_execution(
            session_id=session_id,
            task=task,
            result=result
        )
        logger.info("Task execution recorded to analytics")

    return result

async def _stream_message_to_dashboard(
    self,
    msg: Any,
    dashboard_client: Any
) -> None:
    """Stream message to dashboard for real-time updates."""
    from claude_agent_sdk import TextBlock, ToolUseBlock, ThinkingBlock

    if isinstance(msg, TextBlock):
        await dashboard_client.emit_event('task:progress', {
            'type': 'text',
            'content': msg.text
        })
    elif isinstance(msg, ToolUseBlock):
        await dashboard_client.emit_event('tool:use', {
            'name': msg.name,
            'input': str(msg.input)[:200]  # Truncate
        })
    elif isinstance(msg, ThinkingBlock):
        await dashboard_client.emit_event('task:thinking', {
            'content': msg.thinking[:500]  # Truncate
        })

def _parse_task_result(self, messages: List) -> Dict[str, Any]:
    """Parse task execution result from Claude messages."""
    from claude_agent_sdk import ResultMessage, ToolUseBlock

    # Extract result message
    result_msgs = [m for m in messages if isinstance(m, ResultMessage)]
    files_created = []

    # Find file operations
    for msg in messages:
        if hasattr(msg, 'content'):
            for block in msg.content:
                if isinstance(block, ToolUseBlock) and block.name in ['Write', 'Edit']:
                    files_created.append(block.input.get('file_path'))

    return {
        'success': len(result_msgs) > 0 and not result_msgs[-1].is_error if result_msgs else True,
        'files_created': files_created,
        'message_count': len(messages),
        'result_messages': result_msgs
    }
```

### shannon do Command (Simplified)

```python
@click.command(name='do')
@click.argument('task')
@click.option('--dashboard', '-d', is_flag=True, help='Enable real-time dashboard')
@click.option('--session-id', help='Session ID')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def do_command(task: str, dashboard: bool, session_id: Optional[str], verbose: bool):
    """Execute task via Shannon Framework task-automation skill.

    V5: Combines V3 intelligence (cache, analytics, cost) with
    Shannon Framework task-automation Claude Code skill.

    Examples:
        shannon do "create authentication system"
        shannon do "fix login bug" --dashboard
        shannon do "add tests for user API"
    """
    async def run_do():
        console = Console()
        config = ShannonConfig()

        # Generate session ID
        generated_session_id = session_id or f"do_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        console.print()
        console.print(f"[bold cyan]Shannon V5 Task Execution[/bold cyan]")
        console.print(f"[dim]Task: {task}[/dim]")
        console.print(f"[dim]Session: {generated_session_id}[/dim]\n")

        # Initialize UnifiedOrchestrator
        orchestrator = UnifiedOrchestrator(config)

        # Setup dashboard
        dashboard_client = None
        if dashboard:
            from shannon.communication.dashboard_client import DashboardEventClient
            dashboard_client = DashboardEventClient('http://localhost:8000', generated_session_id)
            connected = await dashboard_client.connect()

            if connected:
                console.print("[dim]✓ Dashboard connected[/dim]\n")
            else:
                console.print("[yellow]⚠ Dashboard unavailable[/yellow]\n")
                dashboard_client = None

        # Execute via UnifiedOrchestrator (invokes Shannon Framework skill)
        with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
            task_progress = progress.add_task("Executing task...")

            result = await orchestrator.execute_task(
                task=task,
                dashboard_client=dashboard_client,
                session_id=generated_session_id
            )

            progress.update(task_progress, completed=True)

        console.print()

        # Display results
        if result.get('success'):
            console.print("[bold green]✓ Task Complete[/bold green]")

            files = result.get('files_created', [])
            if files:
                console.print(f"\n[cyan]Files created:[/cyan] {len(files)}")
                for f in files[:10]:  # Show first 10
                    console.print(f"  {f}")
                if len(files) > 10:
                    console.print(f"  ... and {len(files)-10} more")
        else:
            console.print("[bold red]✗ Task Failed[/bold red]")

        console.print()
        sys.exit(0 if result.get('success') else 1)

    import anyio
    anyio.run(run_do)
```

**Total**: ~80 lines (vs 388 lines in current broken version)

---

## Implementation Steps

### STEP 1: Simplify UnifiedOrchestrator (2-3 hours)

**1.1. Remove Custom Skills Framework Initialization**:
```python
# DELETE from _initialize_v4_components():
- self.skills_registry = ... ❌ DELETE
- self.hook_manager = ... ❌ DELETE
- self.planner = ... ❌ DELETE
- self.v4_executor = ... ❌ DELETE

# KEEP:
- self.state_manager ✅ (for checkpoints)
```

**1.2. Add execute_task() Method**:
- Implement as shown above (~100 lines)
- Invoke task-automation skill via SDK
- Wrap with V3 features (cache, analytics, cost)
- Stream to dashboard

**1.3. Add Helper Methods**:
- _stream_message_to_dashboard() (~30 lines)
- _parse_task_result() (~40 lines)

**Deliverable**: Simplified UnifiedOrchestrator (~650 lines, down from ~800)

---

### STEP 2: Rewrite shannon do (1-2 hours)

**2.1. Replace v4_commands/do.py**:
- Create new implementation using UnifiedOrchestrator.execute_task()
- ~80 lines total (see above)
- Keep dashboard integration
- Remove all custom orchestration code

**2.2. Test Compilation**:
```bash
python -m py_compile src/shannon/cli/v4_commands/do.py
python -c "from shannon.cli.v4_commands.do import do_command; print('OK')"
```

**Deliverable**: Working shannon do command that uses Claude Code skills

---

### STEP 3: Delete Obsolete Code (30 minutes)

**Archive then delete**:
```bash
# Archive for reference
git mv src/shannon/skills src/shannon/skills_archived
git mv src/shannon/orchestration/planner.py src/shannon/orchestration/planner_archived.py
git mv src/shannon/orchestration/task_parser.py src/shannon/orchestration/task_parser_archived.py

# Commit
git commit -m "refactor: Archive custom skills framework

Moved custom skills framework to archived/ for reference.
Shannon V5 uses Shannon Framework Claude Code skills instead.

Archived:
- skills/ (5,500 lines)
- orchestration/planner.py
- orchestration/task_parser.py

Shannon CLI now properly leverages Claude Code skills from
Shannon Framework plugin, not custom reimplementation."
```

**Deliverable**: Cleaner codebase (-5,500 lines)

---

### STEP 4: REAL Testing with shannon do (6-10 hours)

**Test 1: Simple File Creation** (30 min):
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
cd /tmp/test-shannon-do
shannon do "create hello.py that prints hello world"

# WAIT for completion (2-5 minutes)
# VERIFY: hello.py exists
# VERIFY: Contains print statement
# VERIFY: Exit code 0
```

**Test 2: Complex Application** (2-3 hours):
```bash
shannon do "create Flask REST API with:
  - User authentication (JWT tokens)
  - CRUD endpoints for blog posts
  - SQLite database with models
  - Unit tests for all endpoints
  - README with setup instructions"

# WAIT: 10-15 minutes (as you requested!)
# DO NOT KILL IT
# WATCH: Files being created
# VERIFY: All components present
# TEST: Application actually works
# Evidence: Save directory listing, test app runs
```

**Test 3: With Dashboard** (2-3 hours):
```bash
# Terminal 1: Start server
python -m shannon.server.app

# Terminal 2: Start dashboard
cd dashboard && npm run dev

# Terminal 3: Execute with dashboard
shannon do "create calculator module with add, subtract, multiply, divide" --dashboard

# Browser: Open http://localhost:5173
# WATCH: Events appear in real-time
# Use Playwright: Automate verification
```

**Test 4: Multi-Agent** (1-2 hours):
```bash
shannon do "create main.py, create utils.py, create tests.py" --dashboard

# Verify: AgentPool shows 3 agents
# Verify: Agents tracked and displayed
```

**Bug Fixing Buffer** (2-4 hours):
- Fix issues discovered
- Re-run tests
- Document fixes

---

### STEP 5: Dashboard Browser Validation (3-4 hours)

**Using Playwright MCP** (the RIGHT way):

```bash
# Start services
python -m shannon.server.app &
cd dashboard && npm run dev &
sleep 15

# Run command with dashboard
shannon do "create simple app" --dashboard &

# Use Playwright
```

```python
from mcp import playwright

# Navigate
await playwright.browser_navigate("http://localhost:5173")

# Wait for connection
await playwright.browser_wait_for(text="Connected", timeout=10000)

# Wait for task events (ACTUALLY WAIT - don't kill)
await playwright.browser_wait_for(text="create", timeout=60000)  # 60 seconds

# Take screenshot (EVIDENCE)
await playwright.browser_take_screenshot(filename="dashboard-working-proof.png")

# Verify snapshot
snapshot = await playwright.browser_snapshot()
assert "create" in str(snapshot), "Task not shown in dashboard"

print("✓ Dashboard integration VALIDATED with browser")
```

**Deliverable**: Screenshots proving dashboard works

---

### STEP 6: Evidence Collection (2 hours)

**Create**:
1. **Screenshots**: Dashboard showing events (~5 screenshots)
2. **Test logs**: Full output of working tests
3. **Working demo**: Complete application that runs
4. **Video** (optional): Screen recording of 10-min execution
5. **Metrics**: Actual performance numbers (cache speed, memory usage)

**Document in**: VALIDATION_EVIDENCE.md

---

## What This Achieves

### shannon do Now:
- ✅ Uses Shannon Framework task-automation Claude Code skill
- ✅ Gets V3 intelligence (cache, analytics, context, cost)
- ✅ Streams to dashboard in real-time
- ✅ Simple, clean implementation (~80 lines)
- ✅ Actually works (will be proven by testing)

### shannon exec:
- ✅ Already works (proven in memories)
- ✅ Uses Shannon Framework wave skill
- ✅ Keep as-is

### shannon analyze:
- ✅ Already works
- ✅ Uses Shannon Framework spec-analysis skill
- ✅ Keep as-is

### shannon wave:
- ✅ Already works
- ✅ Uses Shannon Framework wave-orchestration skill
- ✅ Keep as-is

---

## Timeline

**Architectural Cleanup**: 3-4 hours
- Simplify UnifiedOrchestrator
- Rewrite shannon do
- Delete custom skills framework

**Real Validation**: 10-14 hours
- Test shannon do with simple task (30min)
- Test shannon do with complex task (3h)
- Test with dashboard (3h)
- Browser validation with Playwright (3-4h)
- Fix bugs discovered (4h buffer)

**Evidence Collection**: 2 hours
- Screenshots, logs, demos

**Total**: 15-20 hours

**This is HONEST timeline including:**
- Actual 10-15 minute test executions
- Browser validation
- Bug fixing time
- Evidence collection

---

## Success Criteria (With Evidence)

### shannon do works:
- ✅ Executes task via task-automation skill
- ✅ Creates files (observable in filesystem)
- ✅ Exit code 0 on success
- ✅ Test output logged

### Dashboard integration works:
- ✅ Browser shows "Connected"
- ✅ Events appear in Skills panel
- ✅ Real-time updates (< 1s latency)
- ✅ Screenshot proves it

### V3 features work:
- ✅ Cache hit on second run (< 500ms)
- ✅ Analytics session recorded (visible in database)
- ✅ Cost optimization active (model selection logged)

### Evidence exists:
- ✅ Screenshots (5+)
- ✅ Test logs showing success
- ✅ Working demo application
- ✅ Observable proof

---

## What I'll Do Next

**Awaiting your approval of this plan.**

Then I will:
1. Execute each step systematically
2. ACTUALLY run tests to completion (no killing)
3. WAIT for 10-15 minute executions
4. WATCH dashboard in browser
5. COLLECT evidence (screenshots, logs)
6. NO completion claims without proof

**Estimated**: 15-20 hours of REAL work with REAL validation.

**No shortcuts. No rushing. Evidence-based completion.**
