# Intelligent Shannon do Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build intelligent, context-aware shannon do command that auto-explores projects, manages validation gates, and caches context for speed.

**Architecture:** shannon do detects first-time vs returning, auto-onboards new projects, asks for validation gates, creates context-enhanced plans, executes via Shannon Framework exec skill, and caches everything for subsequent runs.

**Tech Stack:** Python 3.11, claude-agent-sdk 0.1.6, Shannon Framework Claude Code skills, Serena MCP for context storage

---

## Current Status (Session Handoff)

**What Works** ✅:
- Basic shannon do creates files (hello.py test passed)
- UnifiedOrchestrator invokes Shannon Framework exec skill
- Agent SDK integration correct (query() with ClaudeAgentOptions)
- 5 Shannon CLI Claude Code skills created
- Architecture simplified (6,500 lines archived)

**What's Missing** ❌:
- Context detection (first time vs returning)
- Auto-exploration on first time
- Validation gate management
- Change detection
- Context-enhanced planning

**Evidence**: `/tmp/test-shannon-do-exec/hello.py` exists with `print("hello world")`

---

## Task 1: Add Context Detection to UnifiedOrchestrator

**Files:**
- Modify: `src/shannon/unified_orchestrator.py:345-406` (execute_task method)
- Reference: `INTELLIGENT_SHANNON_DO_DESIGN.md` (complete workflow)

**Step 1: Add project_path parameter to execute_task()**

```python
async def execute_task(
    self,
    task: str,
    project_path: Optional[Path] = None,  # NEW
    dashboard_client: Optional[Any] = None,
    session_id: Optional[str] = None,
    auto_mode: bool = False  # NEW - for autonomous mode
) -> Dict[str, Any]:
```

**Step 2: Add context detection logic**

```python
# Determine project path
if not project_path:
    project_path = Path.cwd()

project_id = project_path.name

# Check if we have context for this project
if not await self._project_context_exists(project_id):
    # FIRST TIME workflow
    result = await self._first_time_workflow(
        task, project_id, project_path, auto_mode, dashboard_client
    )
else:
    # RETURNING workflow
    result = await self._returning_workflow(
        task, project_id, project_path, auto_mode, dashboard_client
    )

return result
```

**Step 3: Test compilation**

Run: `python -m py_compile src/shannon/unified_orchestrator.py`
Expected: Success (even though helper methods don't exist yet)

**Step 4: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Add context detection to shannon do execute_task

Added project_path and auto_mode parameters.
Split execution into first-time vs returning workflows.

Helper methods (_first_time_workflow, _returning_workflow) to be implemented."
```

---

## Task 2: Implement Helper Method - project_context_exists

**Files:**
- Modify: `src/shannon/unified_orchestrator.py` (add method after execute_task)
- Reference: `src/shannon/context/manager.py` (ContextManager API)

**Step 1: Add _project_context_exists() method**

```python
async def _project_context_exists(self, project_id: str) -> bool:
    """Check if we have context for this project.

    Checks both:
    1. ContextManager has the project
    2. Local config exists (~/.shannon/projects/<project_id>/config.json)
    """
    if not self.context:
        return False

    # Check ContextManager
    has_context = await self.context.project_exists(project_id)

    # Check local config
    config_path = self.config.config_dir / 'projects' / project_id / 'config.json'
    has_config = config_path.exists()

    return has_context and has_config
```

**Step 2: Test by running**

```bash
python3 <<EOF
import asyncio
from pathlib import Path
from shannon.unified_orchestrator import UnifiedOrchestrator

async def test():
    orch = UnifiedOrchestrator()
    exists = await orch._project_context_exists("nonexistent")
    print(f"Nonexistent project: {exists}")  # Should be False

asyncio.run(test())
EOF
```

Expected output: `Nonexistent project: False`

**Step 3: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Add project context detection helper

Checks both ContextManager and local config to determine
if we've worked in a project before."
```

---

## Task 3: Implement First-Time Workflow

**Files:**
- Modify: `src/shannon/unified_orchestrator.py`
- Reference: `INTELLIGENT_SHANNON_DO_DESIGN.md:75-145`

**Step 1: Add _first_time_workflow() method**

```python
async def _first_time_workflow(
    self,
    task: str,
    project_id: str,
    project_path: Path,
    auto_mode: bool,
    dashboard_client: Optional[Any]
) -> Dict[str, Any]:
    """Execute workflow for first time in a project.

    Steps:
    1. Auto-onboard project (explore codebase)
    2. Get validation gates (ask user or auto-detect)
    3. Save config for next time
    4. Execute with context-enhanced planning
    """
    logger.info(f"First time workflow for: {project_id}")

    # 1. Auto-onboard
    if not auto_mode:
        print(f"First time in {project_id} - exploring codebase...")

    context = await self.context.onboard_project(
        project_path=str(project_path),
        project_id=project_id
    )

    if not auto_mode:
        discovery = context.get('discovery', {})
        print(f"  Detected: {', '.join(discovery.get('tech_stack', []))}")
        print(f"  Files: {discovery.get('file_count', 0):,}")

    # 2. Validation gates
    if not auto_mode:
        gates = await self._ask_validation_gates(context)
    else:
        gates = await self._auto_detect_validation_gates(context)

    # 3. Save config
    await self._save_project_config(project_id, {
        'validation_gates': gates,
        'last_scan': datetime.now().isoformat(),
        'tech_stack': context.get('discovery', {}).get('tech_stack', [])
    })

    # 4. Execute with context
    result = await self._execute_with_context(
        task, context, gates, dashboard_client
    )

    return result
```

**Step 2: Test compilation**

Run: `python -m py_compile src/shannon/unified_orchestrator.py`
Expected: Success

**Step 3: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Implement first-time workflow for shannon do

Auto-onboards project, gets validation gates, saves config.
Calls _execute_with_context() to be implemented next."
```

---

## Task 4: Implement Returning Workflow

**Files:**
- Modify: `src/shannon/unified_orchestrator.py`

**Step 1: Add _returning_workflow() method**

```python
async def _returning_workflow(
    self,
    task: str,
    project_id: str,
    project_path: Path,
    auto_mode: bool,
    dashboard_client: Optional[Any]
) -> Dict[str, Any]:
    """Execute workflow for returning to known project.

    Steps:
    1. Load cached context
    2. Check for codebase changes
    3. Update context if needed
    4. Execute with cached validation gates
    """
    logger.info(f"Returning workflow for: {project_id}")

    # 1. Load context and config
    context = await self.context.load_project(project_id)
    config = await self._load_project_config(project_id)
    gates = config.get('validation_gates', {})

    # 2. Check for changes
    if await self._codebase_changed(project_path, config):
        if not auto_mode:
            print("Codebase changed - updating context...")

        context = await self.context.update_project(project_id)
        config['last_updated'] = datetime.now().isoformat()
        await self._save_project_config(project_id, config)
    else:
        if not auto_mode:
            print("Using cached context (< 1s)")

    # 3. Execute with context
    result = await self._execute_with_context(
        task, context, gates, dashboard_client
    )

    return result
```

**Step 2: Test compilation**

Run: `python -m py_compile src/shannon/unified_orchestrator.py`

**Step 3: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Implement returning workflow for shannon do

Loads cached context, detects changes, updates if needed.
Faster execution via caching."
```

---

## Task 5: Implement Validation Gate Management

**Files:**
- Modify: `src/shannon/unified_orchestrator.py`

**Step 1: Add _ask_validation_gates() method**

```python
async def _ask_validation_gates(self, context: Dict) -> Dict[str, str]:
    """Ask user for validation commands (interactive mode).

    Shows auto-detected gates, lets user accept/edit.
    """
    # Auto-detect first
    detected = await self._auto_detect_validation_gates(context)

    print("\nValidation Gates (what to run after making changes):")
    print(f"  Build: {detected.get('build_cmd', 'None detected')}")
    print(f"  Tests: {detected.get('test_cmd', 'None detected')}")
    print(f"  Lint: {detected.get('lint_cmd', 'None detected')}")
    print("\nAccept these gates? [Y/n]: ", end='', flush=True)

    # For now, return detected (user interaction TODO)
    return detected

async def _auto_detect_validation_gates(self, context: Dict) -> Dict[str, str]:
    """Auto-detect validation commands from project structure.

    Checks package.json, pyproject.toml, etc. for test commands.
    """
    gates = {}
    discovery = context.get('discovery', {})
    tech_stack = discovery.get('tech_stack', [])

    # Python projects
    if any('python' in t.lower() for t in tech_stack):
        gates['test_cmd'] = 'python -m pytest tests/ || python -m unittest discover'
        gates['lint_cmd'] = 'python -m ruff check . || python -m flake8'

    # Node.js projects
    if any('node' in t.lower() or 'npm' in t.lower() for t in tech_stack):
        gates['build_cmd'] = 'npm run build'
        gates['test_cmd'] = 'npm test'
        gates['lint_cmd'] = 'npm run lint'

    return gates
```

**Step 2: Test auto-detection**

```bash
python3 <<EOF
import asyncio
from shannon.unified_orchestrator import UnifiedOrchestrator

async def test():
    orch = UnifiedOrchestrator()
    context = {'discovery': {'tech_stack': ['Python/pip']}}
    gates = await orch._auto_detect_validation_gates(context)
    print(f"Python gates: {gates}")

asyncio.run(test())
EOF
```

Expected: Shows pytest/ruff commands

**Step 3: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Add validation gate detection and management

Auto-detects test/build/lint commands from tech stack.
Interactive asking to be enhanced later."
```

---

## Task 6: Implement Context-Enhanced Execution

**Files:**
- Modify: `src/shannon/unified_orchestrator.py`

**Step 1: Add _execute_with_context() method**

```python
async def _execute_with_context(
    self,
    task: str,
    context: Dict,
    validation_gates: Dict[str, str],
    dashboard_client: Optional[Any]
) -> Dict[str, Any]:
    """Execute task with project context awareness.

    Creates context-enhanced prompt that tells exec skill about:
    - Existing tech stack
    - Project patterns
    - Validation requirements
    """
    # Build context-enhanced prompt
    discovery = context.get('discovery', {})

    planning_prompt = f\"\"\"Task: {task}

PROJECT CONTEXT:
- Tech Stack: {', '.join(discovery.get('tech_stack', []))}
- Files: {discovery.get('file_count', 0)} files
- Modules: {len(discovery.get('modules', []))} modules
- Entry Points: {', '.join(discovery.get('entry_points', [])[:3])}

VALIDATION REQUIREMENTS:
- Test command: {validation_gates.get('test_cmd', 'None')}
- Build command: {validation_gates.get('build_cmd', 'None')}
- Lint command: {validation_gates.get('lint_cmd', 'None')}

REQUIREMENTS:
1. Integrate with existing code patterns
2. Use project's tech stack
3. Follow project conventions
4. Ensure code can be validated with above commands

Execute this task with full project awareness.
\"\"\"

    # V3: Model selection
    model = 'sonnet'
    if self.model_selector and self.budget_enforcer:
        try:
            complexity = len(task) / 100
            selection = self.model_selector.select_optimal_model(
                agent_complexity=complexity,
                context_size_tokens=len(planning_prompt) / 4,
                budget_remaining=self.budget_enforcer.get_status().remaining
            )
            model = selection.model
        except:
            pass

    # Execute via Shannon Framework exec skill
    logger.info("Executing with project context")
    messages = []

    async for msg in self.sdk_client.invoke_skill(
        skill_name='exec',
        prompt_content=planning_prompt
    ):
        messages.append(msg)
        if dashboard_client:
            await self._stream_message_to_dashboard(msg, dashboard_client)

    return self._parse_task_result(messages)
```

**Step 2: Verify code compiles**

Run: `python -m py_compile src/shannon/unified_orchestrator.py`

**Step 3: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Add context-enhanced execution

Builds planning prompt with project context.
Tells exec skill about tech stack, patterns, validation gates."
```

---

## Task 7: Implement Project Config Management

**Files:**
- Modify: `src/shannon/unified_orchestrator.py`

**Step 1: Add config save/load methods**

```python
async def _save_project_config(self, project_id: str, config: Dict) -> None:
    """Save project configuration (validation gates, timestamps, etc.)."""
    config_path = self.config.config_dir / 'projects' / project_id / 'config.json'
    config_path.parent.mkdir(parents=True, exist_ok=True)

    import json
    config_path.write_text(json.dumps(config, indent=2))
    logger.info(f"Saved config for {project_id}")

async def _load_project_config(self, project_id: str) -> Dict:
    """Load project configuration."""
    config_path = self.config.config_dir / 'projects' / project_id / 'config.json'

    if not config_path.exists():
        return {}

    import json
    return json.loads(config_path.read_text())

async def _codebase_changed(self, project_path: Path, config: Dict) -> bool:
    """Detect if codebase changed since last scan.

    Simple: Compare file count (sophisticated: git commit hash)
    """
    current_files = len(list(project_path.rglob('*.py')))
    last_files = config.get('file_count', 0)

    # Changed if file count differs by more than 5%
    return abs(current_files - last_files) > (last_files * 0.05)
```

**Step 2: Test methods**

```bash
python3 <<EOF
import asyncio
from pathlib import Path
from shannon.unified_orchestrator import UnifiedOrchestrator

async def test():
    orch = UnifiedOrchestrator()

    # Test save/load
    await orch._save_project_config("test-proj", {"test": "value"})
    loaded = await orch._load_project_config("test-proj")
    print(f"Loaded: {loaded}")

    # Test change detection
    changed = await orch._codebase_changed(Path.cwd(), {"file_count": 1000})
    print(f"Changed: {changed}")

asyncio.run(test())
EOF
```

Expected: Config saved and loaded, change detection works

**Step 3: Commit**

```bash
git add src/shannon/unified_orchestrator.py
git commit -m "feat: Add project config management

Save/load validation gates and timestamps.
Detect codebase changes for context updates."
```

---

## Task 8: Update shannon do Command to Pass project_path

**Files:**
- Modify: `src/shannon/cli/v4_commands/do.py:129-133`

**Step 1: Get project path in do_command**

```python
# In do_command function, after options setup:
from pathlib import Path

# Get project root (from option or cwd)
if 'project_root' in locals():
    project_path = Path(project_root).resolve()
else:
    project_path = Path.cwd()
```

**Step 2: Pass to execute_task()**

```python
result = await orchestrator.execute_task(
    task=task,
    project_path=project_path,  # NEW
    dashboard_client=dashboard_client,
    session_id=generated_session_id,
    auto_mode=False  # NEW - interactive by default
)
```

**Step 3: Add --auto flag to command**

```python
@click.option('--auto', is_flag=True, help='Autonomous mode (no questions)')
def do_command(
    task: str,
    dashboard: bool,
    session_id: Optional[str],
    verbose: bool,
    auto: bool  # NEW
):
```

Pass to execute_task: `auto_mode=auto`

**Step 4: Test compilation**

Run: `python -c "from shannon.cli.v4_commands.do import do_command; print('OK')"`

**Step 5: Commit**

```bash
git add src/shannon/cli/v4_commands/do.py
git commit -m "feat: Add project_path and --auto flag to shannon do

Passes project path for context detection.
--auto flag enables autonomous mode (no user prompts)."
```

---

## Task 9: Add Context Manager Methods

**Files:**
- Modify: `src/shannon/context/manager.py`

**Step 1: Check if project_exists() method exists**

Run: `grep -n "def project_exists" src/shannon/context/manager.py`

If NOT found, add:

```python
async def project_exists(self, project_id: str) -> bool:
    """Check if project context exists.

    Returns True if project has been onboarded.
    """
    project_dir = Path.home() / '.shannon' / 'projects' / project_id
    return project_dir.exists()
```

**Step 2: Check if load_project() exists**

If NOT found, add:

```python
async def load_project(self, project_id: str) -> Dict[str, Any]:
    """Load project context.

    Returns cached context for project.
    """
    project_dir = Path.home() / '.shannon' / 'projects' / project_id
    context_file = project_dir / 'context.json'

    if not context_file.exists():
        raise FileNotFoundError(f"No context for project: {project_id}")

    import json
    return json.loads(context_file.read_text())
```

**Step 3: Check if update_project() exists**

If NOT found, add:

```python
async def update_project(self, project_id: str) -> Dict[str, Any]:
    """Update project context (incremental scan).

    Faster than full re-onboard.
    """
    # For now, delegate to full onboard
    # TODO: Implement incremental update
    project_dir = Path.home() / '.shannon' / 'projects' / project_id
    if not project_dir.exists():
        raise FileNotFoundError(f"Project not onboarded: {project_id}")

    # Re-onboard for now (will be optimized later)
    return await self.onboard_project(
        project_path=str(project_dir.parent.parent.parent),
        project_id=project_id
    )
```

**Step 4: Test methods exist and compile**

Run: `python -c "from shannon.context.manager import ContextManager; print('OK')"`

**Step 5: Commit**

```bash
git add src/shannon/context/manager.py
git commit -m "feat: Add context methods for shannon do intelligence

project_exists(), load_project(), update_project() enable
first-time vs returning detection and context management."
```

---

## VALIDATION GATE 1: Functional Test - First Time Workflow

**Test Type**: FUNCTIONAL (NO PYTEST - Run actual CLI)

**Step 1: Create test script**

File: `tests/functional/test_shannon_do_first_time.sh`

```bash
#!/bin/bash
# Test shannon do first-time workflow in new project
# FUNCTIONAL TEST - runs actual CLI command

set -e

echo "Testing shannon do first-time workflow..."

# Create test project
TEST_DIR="/tmp/shannon-do-first-time-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create simple Python project
cat > main.py <<'EOF'
def hello():
    print("Hello")

if __name__ == '__main__':
    hello()
EOF

cat > requirements.txt <<'EOF'
requests==2.31.0
EOF

echo "✓ Test project created"

# Run shannon do (should auto-explore on first time)
export ANTHROPIC_API_KEY="sk-ant-..."
shannon do "create utils.py with helper functions" --auto > /tmp/shannon_do_first_time.log 2>&1

EXIT_CODE=$?

# VALIDATE
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Command executed successfully"
else
    echo "✗ Command failed (exit: $EXIT_CODE)"
    tail -20 /tmp/shannon_do_first_time.log
    exit 1
fi

# Verify context was saved
CONTEXT_DIR="$HOME/.shannon/projects/shannon-do-first-time-test-$$"
if [ -d "$CONTEXT_DIR" ]; then
    echo "✓ Context saved to ~/.shannon/projects/"
else
    echo "✗ Context not saved"
    exit 1
fi

# Verify config saved
if [ -f "$CONTEXT_DIR/config.json" ]; then
    echo "✓ Config saved (validation gates)"
    cat "$CONTEXT_DIR/config.json"
else
    echo "✗ Config not saved"
    exit 1
fi

# Verify file created
if [ -f "utils.py" ]; then
    echo "✓ File created: utils.py"
else
    echo "✗ File not created"
    exit 1
fi

# Cleanup
cd /
rm -rf "$TEST_DIR"

echo "✓ First-time workflow test PASSED"
exit 0
```

**Step 2: Make executable and run**

```bash
chmod +x tests/functional/test_shannon_do_first_time.sh
# Note: Requires ANTHROPIC_API_KEY set
export ANTHROPIC_API_KEY="sk-ant-..."
bash tests/functional/test_shannon_do_first_time.sh
```

**Expected**: Test passes, shows:
- ✓ Command executed successfully
- ✓ Context saved
- ✓ Config saved
- ✓ File created

**Step 3: Commit test**

```bash
git add tests/functional/test_shannon_do_first_time.sh
git commit -m "test: Add functional test for first-time workflow

Tests shannon do in new project:
- Auto-explores codebase
- Saves context and config
- Creates requested file

FUNCTIONAL TEST - runs actual shannon CLI, no pytest."
```

---

## VALIDATION GATE 2: Functional Test - Returning Workflow

**Test Type**: FUNCTIONAL (Run actual CLI, verify caching)

**Step 1: Create test script**

File: `tests/functional/test_shannon_do_returning.sh`

```bash
#!/bin/bash
# Test shannon do returning workflow (cached context)
# FUNCTIONAL TEST

set -e

echo "Testing shannon do returning workflow..."

TEST_DIR="/tmp/shannon-do-returning-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "def hello(): print('Hello')" > main.py

# First run (onboards)
export ANTHROPIC_API_KEY="sk-ant-..."
echo "First run (should onboard)..."
SECONDS=0
shannon do "create utils.py" --auto > /tmp/first_run.log 2>&1
FIRST_TIME=$SECONDS

echo "First run: ${FIRST_TIME}s"

# Second run (should use cache)
echo "Second run (should use cached context)..."
SECONDS=0
shannon do "create helpers.py" --auto > /tmp/second_run.log 2>&1
SECOND_TIME=$SECONDS

echo "Second run: ${SECOND_TIME}s"

# VALIDATE: Second run should be faster or same
# (Context loading < 1s vs onboarding ~10s)

if grep -q "Using cached context" /tmp/second_run.log; then
    echo "✓ Cache message shown"
elif grep -q "First time" /tmp/second_run.log; then
    echo "✗ Second run treated as first time (cache not working)"
    exit 1
fi

# Verify both files created
if [ -f "utils.py" ] && [ -f "helpers.py" ]; then
    echo "✓ Both files created"
else
    echo "✗ Files missing"
    exit 1
fi

cd /
rm -rf "$TEST_DIR"

echo "✓ Returning workflow test PASSED"
exit 0
```

**Step 2: Run test**

```bash
chmod +x tests/functional/test_shannon_do_returning.sh
export ANTHROPIC_API_KEY="sk-ant-..."
bash tests/functional/test_shannon_do_returning.sh
```

**Expected**:
- First run onboards
- Second run uses cache
- Both files created

**Step 3: Commit**

```bash
git add tests/functional/test_shannon_do_returning.sh
git commit -m "test: Add functional test for returning workflow

Tests context caching:
- First run: Onboards project
- Second run: Uses cached context (faster)

FUNCTIONAL TEST - actual CLI execution."
```

---

## VALIDATION GATE 3: Browser Test - Dashboard Integration

**Test Type**: FUNCTIONAL (Browser automation with Playwright MCP)

**Step 1: Create dashboard test**

File: `tests/functional/test_shannon_do_dashboard.sh`

```bash
#!/bin/bash
# Test shannon do with dashboard via Playwright
# FUNCTIONAL TEST - Real browser, real WebSocket

set -e

echo "Testing shannon do with dashboard..."

# Start services in background
echo "Starting WebSocket server..."
python -m shannon.server.app > /tmp/server.log 2>&1 &
SERVER_PID=$!
sleep 5

echo "Starting dashboard..."
cd dashboard && npm run dev > /tmp/dashboard.log 2>&1 &
DASHBOARD_PID=$!
cd ..
sleep 10

echo "Services started (server: $SERVER_PID, dashboard: $DASHBOARD_PID)"

# Create test directory
TEST_DIR="/tmp/dashboard-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Run shannon do with dashboard in background
export ANTHROPIC_API_KEY="sk-ant-..."
shannon do "create calculator.py with add and subtract" --dashboard > /tmp/command.log 2>&1 &
COMMAND_PID=$!

sleep 5

# Playwright verification
python3 <<'PLAYWRIGHT'
import asyncio

async def test():
    # Import Playwright MCP
    from mcp__playwright__browser_navigate import browser_navigate
    from mcp__playwright__browser_wait_for import browser_wait_for
    from mcp__playwright__browser_snapshot import browser_snapshot
    from mcp__playwright__browser_take_screenshot import browser_take_screenshot

    print("Opening dashboard...")
    await browser_navigate(url="http://localhost:5173")

    print("Waiting for connection...")
    await browser_wait_for(text="Connected", timeout=10000)
    print("✓ Dashboard connected")

    print("Waiting for task events...")
    await browser_wait_for(text="create", timeout=60000)  # 60s timeout
    print("✓ Task visible in dashboard")

    # Screenshot as evidence
    await browser_take_screenshot(filename="dashboard-shannon-do-proof.png")
    print("✓ Screenshot captured")

    # Verify snapshot
    snapshot = await browser_snapshot()
    if "calculator" in str(snapshot) or "create" in str(snapshot):
        print("✓ Dashboard shows task execution")
    else:
        print("⚠ Task not clearly visible")

    print("\n✓ Dashboard test PASSED")

asyncio.run(test())
PLAYWRIGHT

PLAYWRIGHT_EXIT=$?

# Cleanup
kill $SERVER_PID $DASHBOARD_PID $COMMAND_PID 2>/dev/null || true

# Results
if [ $PLAYWRIGHT_EXIT -eq 0 ]; then
    echo "✓ Dashboard browser test PASSED"
    echo "Evidence: dashboard-shannon-do-proof.png"
    exit 0
else
    echo "✗ Dashboard test FAILED"
    exit 1
fi
```

**Step 2: Run test (requires services)**

```bash
chmod +x tests/functional/test_shannon_do_dashboard.sh
# Manual run with services:
# Terminal 1: python -m shannon.server.app
# Terminal 2: cd dashboard && npm run dev
# Terminal 3: bash tests/functional/test_shannon_do_dashboard.sh
```

**Expected**: Screenshot showing dashboard with task events

**Step 3: Commit**

```bash
git add tests/functional/test_shannon_do_dashboard.sh
git commit -m "test: Add dashboard browser test for shannon do

Tests real-time dashboard updates via Playwright MCP.
FUNCTIONAL TEST - actual browser, actual WebSocket, no mocks.

Validates:
- WebSocket connection
- Event streaming
- Dashboard UI updates
- Real-time monitoring

Evidence: Screenshot captured."
```

---

## VALIDATION GATE 4: Complex Application Test

**Test Type**: FUNCTIONAL (10+ minute execution, complex app)

**Step 1: Create complex app test**

File: `tests/functional/test_shannon_do_complex_app.sh`

```bash
#!/bin/bash
# Test shannon do with complex application (10+ min execution)
# FUNCTIONAL TEST - Real API call, full execution, observable result

set -e

echo "Testing shannon do with complex application..."
echo "This will take 10-15 minutes - WILL NOT INTERRUPT"

TEST_DIR="/tmp/shannon-complex-app-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create README to give shannon do context
cat > README.md <<'EOF'
# Complex Test Project

Python/Flask project for testing Shannon do intelligence.
EOF

# Run complex task
export ANTHROPIC_API_KEY="sk-ant-..."

echo "Executing complex task (estimated 10-15 minutes)..."
echo "Task: Create Flask REST API with full features"
echo "Will wait for completion - NOT killing early"
echo

# Record start time
START_TIME=$(date +%s)

shannon do "create a Flask REST API with:
- User authentication (JWT tokens)
- CRUD endpoints for blog posts (/posts)
- SQLite database with models
- Input validation
- Error handling
- Unit tests for all endpoints
- README with API documentation
" --auto --verbose 2>&1 | tee /tmp/complex_app_execution.log

EXIT_CODE=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo
echo "Execution completed in ${DURATION} seconds"

# VALIDATION - Check files created
echo
echo "Validating created files..."

REQUIRED_FILES=(
    "app.py"
    "models.py"
    "requirements.txt"
    "README.md"
)

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        MISSING=$((MISSING + 1))
    fi
done

# Check for API endpoints in app.py
if grep -q "/posts" app.py 2>/dev/null; then
    echo "✓ API endpoints present"
else
    echo "⚠ API endpoints not found"
fi

# Try running the app (basic validation)
if python3 -m py_compile *.py 2>/dev/null; then
    echo "✓ All Python files compile"
else
    echo "✗ Python compilation errors"
    MISSING=$((MISSING + 1))
fi

# Capture evidence
echo
echo "=== EVIDENCE ==="
echo "Files created:"
ls -lh
echo
echo "Directory structure:"
find . -name "*.py" -o -name "*.md" -o -name "*.txt"
echo
echo "Execution time: ${DURATION}s"
echo "Exit code: $EXIT_CODE"

# Cleanup (save evidence first)
cp -r "$TEST_DIR" /tmp/shannon-complex-app-evidence-$$

cd /
rm -rf "$TEST_DIR"

# Final result
if [ $EXIT_CODE -eq 0 ] && [ $MISSING -eq 0 ]; then
    echo
    echo "✓ Complex app test PASSED"
    echo "Evidence saved: /tmp/shannon-complex-app-evidence-$$"
    exit 0
else
    echo
    echo "✗ Complex app test FAILED"
    echo "Missing files: $MISSING"
    echo "Exit code: $EXIT_CODE"
    exit 1
fi
```

**Step 2: Run test (WAIT FULL DURATION)**

```bash
chmod +x tests/functional/test_shannon_do_complex_app.sh
export ANTHROPIC_API_KEY="sk-ant-..."
bash tests/functional/test_shannon_do_complex_app.sh

# This will take 10-15 minutes
# DO NOT KILL IT
# WAIT for completion
# Capture all output
```

**Expected**:
- Execution: 10-15 minutes
- Files: app.py, models.py, tests, README
- All Python compiles
- Evidence directory saved

**Step 3: Document results**

Create: `COMPLEX_APP_TEST_RESULTS.md` with:
- Full execution log
- Files created (list)
- Code quality assessment
- Duration and metrics

**Step 4: Commit**

```bash
git add tests/functional/test_shannon_do_complex_app.sh COMPLEX_APP_TEST_RESULTS.md
git commit -m "test: Add complex application functional test

10-15 minute execution test creating full Flask REST API.
FUNCTIONAL TEST - actual API call, full execution, complete app.

Validates:
- Complex task handling
- Multiple file creation
- Code quality
- Full workflow completion

Evidence: Saved application directory, execution log."
```

---

## Task 10: Audit ALL Agent SDK Usage

**Files to Audit** (11 files):
- src/shannon/sdk/client.py
- src/shannon/cli/commands.py
- src/shannon/unified_orchestrator.py
- src/shannon/orchestrator.py
- src/shannon/executor/complete_executor.py
- src/shannon/sdk/message_parser.py
- src/shannon/sdk/interceptor.py
- src/shannon/executor/prompt_enhancer.py
- src/shannon/executor/code_executor.py
- src/shannon/executor/prompts.py
- src/shannon/ui/progress.py

**For EACH file, verify**:

**Step 1: Check imports**
```bash
grep "from claude_agent_sdk import" <file>
```
Verify: Imports match Agent SDK v0.1.6 API

**Step 2: Check query() usage**
```bash
grep -A 5 "query(" <file>
```
Verify:
- Has ClaudeAgentOptions ✓
- Has plugins parameter if using Framework ✓
- Has setting_sources=["project"] to load skills ✓
- Async iteration correct ✓

**Step 3: Check message type handling**
```bash
grep "isinstance.*Message" <file>
```
Verify: Uses correct types (AssistantMessage, TextBlock, etc.)

**Step 4: Document in audit report**

For each file, document:
- ✅ CORRECT: What's properly implemented
- ⚠️ REVIEW: What needs checking
- ❌ WRONG: What needs fixing

**Step 5: Create audit report**

File: `AGENT_SDK_USAGE_AUDIT.md`

Structure:
```markdown
# Agent SDK Usage Audit

## Summary
- Files audited: 11
- Correct usage: X
- Issues found: Y
- Fixes needed: Z

## Per-File Analysis

### src/shannon/sdk/client.py ✅
- invoke_skill(): Correct API
- ClaudeAgentOptions: All parameters valid
- setting_sources: Includes "project" ✓
- Message iteration: Correct async pattern

### src/shannon/cli/commands.py ⚠️
- query() usage: Correct
- Issue: Uses /spec instead of @skill spec-analysis
- Recommendation: Standardize on @skill syntax
...
```

**Step 6: Commit audit**

```bash
git add AGENT_SDK_USAGE_AUDIT.md
git commit -m "docs: Complete Agent SDK usage audit

Audited all 11 files using claude-agent-sdk.
Verified compliance with v0.1.6 API.

Found X issues, all documented with fixes.
Overall: SDK usage is sound."
```

---

## Final Task: Create Next Session Starter Document

**File:** `NEXT_SESSION_INTELLIGENT_SHANNON_DO.md`

```markdown
# Next Session: Complete Intelligent Shannon do

**Context**: Session ended after 11 hours, 610K tokens.
**Status**: Architecture correct, basic shannon do works, intelligence layer designed but not built.

## What to Load

1. Read: `INTELLIGENT_SHANNON_DO_DESIGN.md` (complete design)
2. Read: `SHANNON_V5_CORRECT_ARCHITECTURE_PLAN.md` (architecture)
3. Read: `SESSION_HANDOFF_V5_ARCHITECTURAL_RESET.md` (what happened)
4. Read: `SHANNON_DO_SUCCESS_EVIDENCE.md` (proof basic works)
5. Load Serena: `SHANNON_V5_ARCHITECTURAL_RESET_20251117`

## Continuation Checklist

- [ ] UnifiedOrchestrator has context detection methods
- [ ] First-time workflow implemented
- [ ] Returning workflow implemented
- [ ] Validation gates managed
- [ ] All functional tests passing
- [ ] Complex app test (10+ min) completed with evidence
- [ ] Dashboard browser test completed
- [ ] Agent SDK audit documented

## Execution Command

```bash
# From shannon-cli directory:
/execute-plan @docs/plans/2025-11-17-intelligent-shannon-do-implementation.md
```

This will execute all tasks with validation gates.

## Success Criteria

**Code**:
- shannon do has intelligent workflows ✅
- Context cached and reused ✅
- Validation gates managed ✅

**Testing**:
- First-time test passes ✅
- Returning test passes ✅
- Complex app test (10+ min) passes ✅
- Dashboard browser test passes ✅

**Evidence**:
- Working complex application ✅
- Screenshots of dashboard ✅
- Test logs showing success ✅

NO completion claims without this evidence.
```

**Commit:**

```bash
git add NEXT_SESSION_INTELLIGENT_SHANNON_DO.md
git commit -m "docs: Next session starter for intelligent shannon do

Complete handoff document for continuation:
- What to load
- Checklist of remaining work
- How to execute plan
- Success criteria with evidence requirements

Estimated: 7-10 hours to complete with proper testing."
```

---

## Estimated Timeline

**Total Work**: 7-10 hours

**Breakdown**:
- Tasks 1-9 (Implementation): 5-6 hours
- Validation Gates 1-4 (Functional Testing): 4-5 hours
  - Each functional test requires real execution
  - Complex app test: 15-20 min execution time
  - Dashboard test: Setup + verification
  - Must WAIT for completion, not kill early
- Agent SDK Audit: 1 hour (meticulous review)
- Documentation: Included in tasks

**Testing Philosophy**:
- NO PYTEST
- NO UNIT TESTS
- ONLY: Run actual shannon CLI commands
- ONLY: Browser automation (Playwright/Chrome DevTools MCP)
- Validate as END USER would experience

---

Plan complete and saved to `docs/plans/2025-11-17-intelligent-shannon-do-implementation.md`.

**This plan implements EXACTLY what you described**: intelligent shannon do with auto-exploration, context caching, and proper functional validation.
