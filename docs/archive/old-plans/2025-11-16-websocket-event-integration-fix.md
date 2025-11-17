# WebSocket Event Integration Fix Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix shannon do to emit execution events to WebSocket so dashboard shows real-time updates

**Current State:**
- shannon do emits events to stdout (print statements)
- Events NOT sent to Socket.IO server
- Dashboard connected but sees no execution events

**Target State:**
- shannon do emits events to WebSocket
- Dashboard receives all execution events
- UI updates in real-time during execution

**Tech Stack:** Python asyncio, Socket.IO, FastAPI

---

## Root Cause Analysis

**Problem**: `src/shannon/orchestration/orchestrator.py` has `_emit_event()` method that only prints to stdout:

```python
async def _emit_event(self, event_type: str, data: Dict):
    """Emit event for monitoring"""
    print(f"Event: {event_type}")  # Only prints!
    # Missing: WebSocket emission
```

**Solution**: Integrate with Socket.IO server's emit_event helper

---

## Task 1: Add WebSocket Event Emission to Orchestrator

**Files:**
- Modify: `src/shannon/orchestration/orchestrator.py`

**Step 1: Import WebSocket emitter**

At top of file, add:
```python
from shannon.server.websocket import emit_skill_event, emit_execution_event
```

**Step 2: Store session_id in orchestrator**

In `__init__`:
```python
def __init__(
    self,
    plan: ExecutionPlan,
    executor: SkillExecutor,
    state_manager: StateManager,
    session_id: Optional[str] = None,  # Add this parameter
    event_callback: Optional[Callable] = None
):
    # ... existing code
    self.session_id = session_id  # Store it
```

**Step 3: Update _emit_event to use WebSocket**

Replace current _emit_event method:
```python
async def _emit_event(self, event_type: str, data: Dict):
    """Emit event to both stdout and WebSocket"""

    # Keep stdout for CLI visibility
    print(f"Event: {event_type}")

    # Add WebSocket emission
    if self.session_id:
        try:
            if event_type.startswith('skill:'):
                await emit_skill_event(event_type, data, self.session_id)
            elif event_type.startswith('execution:'):
                await emit_execution_event(event_type, data, self.session_id)
            elif event_type.startswith('checkpoint:'):
                await emit_execution_event(event_type, data, self.session_id)
        except Exception as e:
            # Don't fail execution if WebSocket emission fails
            logger.warning(f"Failed to emit event to WebSocket: {e}")
```

**Step 4: Run test**

```bash
cd /tmp
mkdir test-ws-events
cd test-ws-events
git init && echo "# Test" > README.md && git add . && git commit -m "init"
echo ".shannon/
.shannon_cache/" > .gitignore
git add .gitignore && git commit -m "Add gitignore"

# Start server (Terminal 1)
cd /Users/nick/Desktop/shannon-cli
poetry run python run_server.py

# Start dashboard (Terminal 2)
cd dashboard && npm run dev

# Run with dashboard (Terminal 3)
shannon do "create hello.py" --dashboard
```

Expected: Dashboard Event Stream shows skill:started, skill:completed events

**Step 5: Commit**

```bash
git add src/shannon/orchestration/orchestrator.py
git commit -m "fix: Emit execution events to WebSocket for dashboard monitoring

WHY: Events were only printed to stdout, dashboard received nothing
WHAT: Integrated orchestrator with Socket.IO emit_skill_event/emit_execution_event
VALIDATION: shannon do --dashboard now shows events in dashboard Event Stream"
```

---

## Task 2: Pass session_id from CLI to Orchestrator

**Files:**
- Modify: `src/shannon/cli/commands/do.py`

**Step 1: Generate session_id when --dashboard flag used**

```python
@cli.command('do')
@click.argument('task')
@click.option('--dashboard', is_flag=True, help='Enable dashboard monitoring')
async def do(task: str, dashboard: bool, ...):
    """Execute task with orchestration"""

    session_id = None

    if dashboard:
        # Generate unique session ID for WebSocket routing
        import uuid
        session_id = f"do_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        console.print(f"Session ID: {session_id}")

    # ... create orchestrator with session_id
    orchestrator = Orchestrator(
        plan=plan,
        executor=executor,
        state_manager=state_manager,
        session_id=session_id  # Pass it here
    )
```

**Step 2: Test session_id propagation**

```python
# Add debug log
console.print(f"[DEBUG] Orchestrator session_id: {orchestrator.session_id}")
```

**Step 3: Run test**

```bash
shannon do "create test.py" --dashboard --verbose
```

Expected output includes: "Session ID: do_20251116_XXXXXX_YYYYYYYY"

**Step 4: Commit**

```bash
git add src/shannon/cli/commands/do.py
git commit -m "feat: Pass session_id to orchestrator for WebSocket event routing

WHY: Orchestrator needs session_id to emit events to correct dashboard client
WHAT: Generate unique session_id when --dashboard flag used, pass to orchestrator
VALIDATION: session_id appears in logs, orchestrator receives it"
```

---

## Task 3: Verify Events Arrive at Dashboard

**Step 1: Start server and dashboard**

Terminal 1: `poetry run python run_server.py`
Terminal 2: `cd dashboard && npm run dev`

**Step 2: Open Playwright**

```python
await playwright.navigate("http://localhost:5173")
await playwright.wait_for("2000")
```

**Step 3: Run shannon do with dashboard**

Terminal 3:
```bash
cd /tmp/test-events
shannon do "create greet.py" --dashboard
```

**Step 4: Wait for execution to start**

```python
await playwright.wait_for("5000")
```

**Step 5: Check Event Stream count**

```python
event_count = await playwright.evaluate("""() => {
  const stream = document.querySelector('[data-testid="event-stream"]')
  return stream ? stream.textContent.match(/\\d+/)[0] : '0'
}""")
print(f"Events received: {event_count}")
```

Expected: More than 2 events (skill:started, skill:completed, etc.)

**Step 6: Click Event Stream to expand**

```python
await playwright.click('text=Event Stream')
```

**Step 7: Verify event types**

```python
events = await playwright.evaluate("""() => {
  const eventElements = document.querySelectorAll('[class*="event-item"]')
  return Array.from(eventElements).map(el => ({
    type: el.querySelector('[class*="event-type"]')?.textContent,
    time: el.querySelector('[class*="event-time"]')?.textContent
  }))
}""")
```

Expected: Events with types like "skill:started", "skill:completed", "checkpoint:created"

**Step 8: Take screenshot**

```python
await playwright.screenshot("dashboard-events-flowing.png")
```

**Step 9: Document success**

Create `WEBSOCKET_INTEGRATION_VERIFIED.md` with:
- Screenshot evidence
- Event list
- Verification that events flow from CLI → WebSocket → Dashboard

**Step 10: Commit**

```bash
git add WEBSOCKET_INTEGRATION_VERIFIED.md dashboard-events-flowing.png
git commit -m "test: Verify WebSocket events flow from shannon do to dashboard

Evidence: Playwright shows 10+ events in dashboard Event Stream
Events include: skill:started, skill:completed, checkpoint:created, execution:completed
Dashboard receives real-time updates during execution"
```

---

## Task 4: Auto-Create .gitignore

**Files:**
- Modify: `src/shannon/orchestration/orchestrator.py`

**Step 1: Add gitignore helper method**

```python
async def _ensure_gitignore(self):
    """Ensure .gitignore exists with Shannon directories"""
    from pathlib import Path

    gitignore_path = Path.cwd() / '.gitignore'
    shannon_entries = ['.shannon/', '.shannon_cache/']

    if gitignore_path.exists():
        content = gitignore_path.read_text()
        missing = [entry for entry in shannon_entries if entry not in content]

        if missing:
            # Append missing entries
            with open(gitignore_path, 'a') as f:
                f.write('\n' + '\n'.join(missing))
            logger.info(f"Updated .gitignore with Shannon directories")
    else:
        # Create new .gitignore
        gitignore_path.write_text('\n'.join(shannon_entries) + '\n')
        logger.info(f"Created .gitignore with Shannon directories")
```

**Step 2: Call before execution**

In `execute()` method, add after state check:
```python
async def execute(self) -> OrchestratorResult:
    # ... existing state check code

    # Ensure .gitignore before execution
    await self._ensure_gitignore()

    logger.info(f"Starting execution: plan={self.plan.plan_id}...")
```

**Step 3: Test in new project**

```bash
cd /tmp
mkdir test-gitignore-auto
cd test-gitignore-auto
git init && echo "# Test" > README.md && git add . && git commit -m "init"
# NO .gitignore created manually

shannon do "create hello.py"
```

Expected:
- .gitignore created automatically
- Contains .shannon/ and .shannon_cache/
- hello.py created successfully

**Step 4: Verify .gitignore**

```bash
cat .gitignore
```

Expected:
```
.shannon/
.shannon_cache/
```

**Step 5: Commit**

```bash
git add src/shannon/orchestration/orchestrator.py
git commit -m "fix: Auto-create .gitignore for Shannon directories

WHY: shannon do was failing with 'working directory not clean' in new projects
WHAT: Orchestrator now ensures .gitignore exists with .shannon/ entries before execution
VALIDATION: Test in new project shows .gitignore created, file generation succeeds"
```

---

## Task 5: Retest Full Stack with Playwright

**Step 1: Start fresh servers**

```bash
cd /Users/nick/Desktop/shannon-cli
poetry run python run_server.py > /tmp/final-server.log 2>&1 &
cd dashboard && npm run dev > /tmp/final-dashboard.log 2>&1 &
sleep 5
```

**Step 2: Open dashboard in Playwright**

```python
await playwright.navigate("http://localhost:5173")
await playwright.wait_for("3000")  # Wait for connection
```

**Step 3: Verify connected state**

```python
connected = await playwright.evaluate("""() => {
  return document.querySelector('[class*="connected"]')?.textContent || 'unknown'
}""")
```

Expected: "Connected"

**Step 4: Start execution in terminal**

```bash
cd /tmp/final-test
git init && echo "# Test" > README.md && git add . && git commit -m "init"
shannon do "create calculator.py with add and multiply" --dashboard
```

**Step 5: Monitor dashboard updates in Playwright**

```python
# Wait for events to arrive
await playwright.wait_for("5000")

# Check ExecutionOverview updates
task_name = await playwright.evaluate("""() => {
  return document.querySelector('[data-testid="task-name"]')?.textContent ||
         document.querySelector('.task')?.textContent
}""")
```

Expected: Shows "create calculator.py with add and multiply"

**Step 6: Check skills panel**

```python
skills_count = await playwright.evaluate("""() => {
  return document.querySelector('[data-testid="skills-count"]')?.textContent ||
         document.querySelectorAll('[class*="skill-item"]').length.toString()
}""")
```

Expected: Shows 3+ skills (library_discovery, prompt_enhancement, code_generation)

**Step 7: Take screenshot of active execution**

```python
await playwright.screenshot("dashboard-executing.png")
```

**Step 8: Wait for completion**

```python
await playwright.wait_for("text=Execution Complete", timeout=120000)
```

**Step 9: Verify file created**

```bash
ls /tmp/final-test/calculator.py
cat /tmp/final-test/calculator.py
```

Expected: File exists with add() and multiply() functions

**Step 10: Take final screenshot**

```python
await playwright.screenshot("dashboard-complete.png")
```

**Step 11: Document full stack success**

Create `FULL_STACK_VERIFIED.md` with:
- All screenshots
- Console logs
- Server logs
- File evidence
- Proof that dashboard ACTUALLY WORKS end-to-end

**Step 12: Commit**

```bash
git add FULL_STACK_VERIFIED.md dashboard-executing.png dashboard-complete.png
git commit -m "test: Full stack end-to-end verification with Playwright

VERIFIED:
- Dashboard loads and connects ✅
- WebSocket events flow from shannon do ✅
- ExecutionOverview updates in real-time ✅
- Skills panel shows executing skills ✅
- File created successfully ✅
- Full user experience functional ✅

Evidence: Screenshots show dashboard updating during execution"
```

---

## Validation Gates

### Gate 1: Events Emitted to WebSocket
- [ ] orchestrator.py uses Socket.IO emit functions
- [ ] session_id passed from CLI
- [ ] Test shows events in server logs
- [ ] Dashboard Event Stream > 2 events

### Gate 2: Dashboard Updates During Execution
- [ ] ExecutionOverview shows task name
- [ ] Skills panel shows ≥3 skills
- [ ] Status changes from "Idle" to "Running"
- [ ] Verified with Playwright

### Gate 3: File Creation Works
- [ ] .gitignore auto-created
- [ ] calculator.py file exists
- [ ] Functions work correctly
- [ ] Git commit created

### Gate 4: Full Stack Proven
- [ ] All screenshots captured
- [ ] All evidence documented
- [ ] Can reproduce reliably
- [ ] User experience verified

---

## Success Criteria

**Can only claim "Dashboard Functional" when:**
- ✅ Playwright shows dashboard loading
- ✅ WebSocket connection in browser console
- ✅ Events appear in Event Stream during execution
- ✅ ExecutionOverview panel updates with task info
- ✅ Skills panel shows skills executing
- ✅ File actually created and works
- ✅ All verified with screenshots
- ✅ No critical bugs found

**Until then:** "Dashboard infrastructure complete, integration in progress"

---

## Estimated Effort

- Task 1 (WebSocket emit): 1-2 hours
- Task 2 (session_id): 30 min
- Task 3 (Verify events): 30 min
- Task 4 (.gitignore): 1 hour
- Task 5 (Full test): 1 hour

**Total**: 4-5 hours

---

**Status**: Plan ready for execution
**Next**: Execute Task 1 to integrate WebSocket event emission
