# Shannon V4-ACTUAL: Complete Spec Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement ALL remaining features from shannon-cli-4.md spec until Shannon V4 is ACTUALLY complete (not claimed complete)

**Current Honest Status:** 25-30% of spec features working
**Target:** 100% of shannon-cli-4.md spec features functional and Playwright-verified

**Spec Document:** shannon-cli-4.md (2,503 lines - FULL specification)
**Estimated Work:** 5-7 months (21-27 weeks) for complete implementation

**Tech Stack:** Python, FastAPI, Socket.IO, React, TypeScript, Playwright MCP for all testing

---

## Brutal Honest Current State

### What Works (25-30%)

**Foundation**:
- ✅ Skills Framework (221 tests passing)
- ✅ Auto-discovery from 7 sources
- ✅ WebSocket connection (client-server architecture)
- ✅ shannon exec (V3.5 - single-file autonomous)

**shannon do (Partial)**:
- ✅ Single-file creation
- ✅ Basic event flow to dashboard
- ✅ Task parsing
- ❌ Multi-file creation (creates 1 of N)

**Dashboard (2 of 6 panels)**:
- ✅ ExecutionOverview (task, status, progress)
- ✅ SkillsView (skills list)
- ❌ AgentPool (no agents spawning)
- ❌ FileDiff (no file events)
- ❌ Decisions (no decision system)
- ❌ Validation (no validation streaming)

### What's Missing (70-75%)

**Commands** (4 of 6 missing):
- shannon debug (stubs exist, not functional)
- shannon ultrathink (stubs exist, not functional)
- shannon research (not implemented)
- Full shannon do (missing: multi-file, multi-agent, research, decisions)

**Dashboard** (4 of 6 panels broken):
- AgentPool panel
- FileDiff panel
- Decisions panel
- Validation panel

**Controls** (8 of 8 untested or missing):
- HALT/RESUME (exist, not tested)
- ROLLBACK N, REDIRECT, ADD CONTEXT (not implemented)
- APPROVE, OVERRIDE, INSPECT (not implemented)

**Core Features**:
- Multi-file generation
- Multi-agent coordination (8 agents in parallel)
- Research orchestration
- Decision point system
- File diff streaming
- Validation streaming
- Dynamic skill creation (pattern detection exists, auto-generation broken)

---

## Phase 1: Critical Foundations (Weeks 1-4)

### WEEK 1: Multi-File Generation Fix (CRITICAL - User Called Out)

**Current Problem**: CompleteExecutor creates only first file in multi-file requests

**Root Cause**: execute_autonomous() designed for single atomic task, doesn't iterate through multiple file targets

#### Task 1.1: Analyze Multi-File Requirement Parsing

**File**: New analysis script: `tests/research/analyze_multi_file_tasks.py`

**Step 1: Create test cases for multi-file requests**

```python
# Multi-file test cases
test_cases = [
    "create auth/ module: auth/tokens.py, auth/middleware.py, auth/__init__.py",
    "implement user system with models/user.py, routes/users.py, controllers/user_controller.py",
    "build API: api/endpoints.py, api/schemas.py, api/responses.py, api/__init__.py"
]
```

**Step 2: Parse each test case to extract file list**

```python
def extract_files_from_task(task: str) -> List[str]:
    """
    Extract list of files from multi-file task description.

    Patterns:
    - "create X: file1, file2, file3"
    - "implement Y with file1, file2, file3"
    - "build Z: file1, file2"
    """
    # Parse logic here
    pass
```

**Step 3: Test parser**

Run: `python tests/research/analyze_multi_file_tasks.py`

Expected: List of files extracted from each test case

**Step 4: Document parsing strategy**

Create: `docs/MULTI_FILE_PARSING_STRATEGY.md`

**Step 5: Commit research**

```bash
git add tests/research/ docs/MULTI_FILE_PARSING_STRATEGY.md
git commit -m "research: Analyze multi-file task parsing patterns

Identified 3 common patterns for multi-file requests
Created test cases for validation
Documented parsing strategy

Next: Implement multi-file executor"
```

**Validation Gate 1.1**:
- [ ] Test cases created
- [ ] Parser extracts files correctly
- [ ] Strategy documented
- [ ] Commit created

---

#### Task 1.2: Implement Multi-File Task Parser

**File**: `src/shannon/orchestration/multi_file_parser.py` (NEW)

**Step 1: Create MultiFileParser class**

```python
"""
Multi-File Task Parser

Extracts multiple file targets from natural language task descriptions.
"""

from typing import List, Optional
import re

class MultiFileRequest:
    """Represents a multi-file creation/modification request"""
    base_task: str  # "create auth module"
    files: List[str]  # ["auth/tokens.py", "auth/middleware.py", ...]
    descriptions: Dict[str, str]  # {"auth/tokens.py": "JWT generation", ...}

class MultiFileParser:
    """
    Parse multi-file requests from natural language.

    Patterns detected:
    1. "create X: file1, file2, file3"
    2. "implement Y with file1, file2"
    3. "file1 for X, file2 for Y, file3 for Z"
    """

    def parse(self, task: str) -> Optional[MultiFileRequest]:
        """
        Parse task to detect multi-file request.

        Returns None if single-file task.
        Returns MultiFileRequest if multiple files detected.
        """
        # Implementation
        pass

    def is_multi_file(self, task: str) -> bool:
        """Quick check if task appears to request multiple files"""
        patterns = [
            r':\s*\w+\.py\s*,\s*\w+\.py',  # "create: file1.py, file2.py"
            r'with\s+\w+\.py\s+and\s+\w+\.py',  # "with file1.py and file2.py"
            r'\w+/\w+\.py,?\s+\w+/\w+\.py',  # "dir/file1.py, dir/file2.py"
        ]
        return any(re.search(p, task) for p in patterns)
```

**Step 2: Write tests**

File: `tests/orchestration/test_multi_file_parser.py`

```python
def test_single_file_detection():
    parser = MultiFileParser()
    assert not parser.is_multi_file("create hello.py")

def test_multi_file_detection():
    parser = MultiFileParser()
    assert parser.is_multi_file("create auth: tokens.py, middleware.py")

def test_parse_multi_file():
    parser = MultiFileParser()
    result = parser.parse("create auth: tokens.py for JWT, middleware.py for FastAPI")
    assert len(result.files) == 2
    assert "tokens.py" in result.files[0]
```

**Step 3: Run tests**

Run: `pytest tests/orchestration/test_multi_file_parser.py -v`

Expected: All tests PASS

**Step 4: Commit parser**

```bash
git add src/shannon/orchestration/multi_file_parser.py tests/orchestration/test_multi_file_parser.py
git commit -m "feat: Multi-file task parser with pattern detection

Detects and parses multi-file creation requests
Extracts file list and per-file descriptions
Tests: 5/5 passing

Next: Integrate with CompleteExecutor for iteration"
```

**Validation Gate 1.2**:
- [ ] MultiFileParser class created
- [ ] Tests written and passing
- [ ] Pattern detection works
- [ ] File extraction accurate
- [ ] Commit created

---

#### Task 1.3: Implement Multi-File Executor

**File**: `src/shannon/executor/multi_file_executor.py` (NEW)

**Step 1: Create MultiFileExecutor class**

```python
"""
Multi-File Executor

Handles creation/modification of multiple files in a single task.
Uses CompleteExecutor for each file iteration.
"""

from pathlib import Path
from typing import List, Dict
from shannon.executor.complete_executor import CompleteExecutor
from shannon.orchestration.multi_file_parser import MultiFileParser, MultiFileRequest

class MultiFileExecutor:
    """
    Execute multi-file creation/modification tasks.

    Strategy:
    1. Parse task to extract file list
    2. For each file:
       a. Create sub-task ("create file1.py for JWT generation")
       b. Execute with CompleteExecutor
       c. Validate file created
       d. Emit file:created event to dashboard
       e. Continue to next file
    3. All files created → success

    Validation per file:
    - File exists
    - Content matches description
    - Can import/compile
    - Git committed

    Dashboard integration:
    - Emit file:created for each file
    - Update FileDiff panel with each file
    - Show progress (2/5 files completed)
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
        Execute multi-file task.

        Returns:
            MultiFileResult with list of created files, successes, failures
        """
        # 1. Parse task
        request = self.parser.parse(task)
        if not request:
            # Single file - delegate to CompleteExecutor
            return await self.executor.execute_autonomous(task)

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
                auto_commit=False  # We'll commit all together
            )

            if result.success:
                # Emit file created event
                if dashboard_client:
                    await dashboard_client.emit_event('file:created', {
                        'file_path': file_path,
                        'index': i,
                        'total': len(request.files),
                        'content_preview': result.file_content[:500]  # First 500 chars
                    })

                results.append(result)
            else:
                # File creation failed - should we continue or stop?
                # For now: stop and report partial results
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
```

**Step 2: Write tests**

File: `tests/executor/test_multi_file_executor.py`

```python
@pytest.mark.asyncio
async def test_multi_file_execution():
    """Test creating 3 files in one task"""
    executor = MultiFileExecutor(Path("/tmp/test"))

    result = await executor.execute(
        "create utils: math.py for math functions, string.py for string utils, file.py for file operations"
    )

    assert result.success
    assert result.files_created == 3
    assert Path("/tmp/test/utils/math.py").exists()
    assert Path("/tmp/test/utils/string.py").exists()
    assert Path("/tmp/test/utils/file.py").exists()

@pytest.mark.asyncio
async def test_single_file_delegates():
    """Test single file delegates to CompleteExecutor"""
    executor = MultiFileExecutor(Path("/tmp/test"))

    result = await executor.execute("create hello.py")

    assert result.success
    assert Path("/tmp/test/hello.py").exists()
```

**Step 3: Run tests**

Run: `pytest tests/executor/test_multi_file_executor.py -v`

Expected: 2/2 tests PASS

**Step 4: Commit executor**

```bash
git add src/shannon/executor/multi_file_executor.py tests/executor/test_multi_file_executor.py
git commit -m "feat: Multi-file executor with file-by-file iteration

Handles multi-file requests by:
1. Parsing file list from task
2. Creating each file with CompleteExecutor
3. Emitting file:created events for dashboard
4. Committing all files together

Tests: 2/2 passing
Validates each file created successfully

Next: Integrate with shannon do command"
```

**Validation Gate 1.3**:
- [ ] MultiFileExecutor class created
- [ ] Tests pass (2/2)
- [ ] Creates all requested files
- [ ] Emits file events
- [ ] Commit created

---

#### Task 1.4: Integrate Multi-File Executor with shannon do

**File**: `src/shannon/cli/v4_commands/do.py`

**Step 1: Import MultiFileExecutor**

```python
from shannon.executor.multi_file_executor import MultiFileExecutor
```

**Step 2: Detect multi-file requests**

```python
# In do() command, before creating plan
from shannon.orchestration.multi_file_parser import MultiFileParser

parser = MultiFileParser()
is_multi_file = parser.is_multi_file(task)

if is_multi_file:
    console.print("[yellow]Multi-file request detected[/yellow]")
    # Use MultiFileExecutor instead of normal flow
    executor = MultiFileExecutor(project_root)
    result = await executor.execute(task, dashboard_client)
else:
    # Normal shannon do flow
    # ... existing code
```

**Step 3: Test multi-file via CLI**

```bash
cd /tmp/multi-file-test
git init && echo ".shannon/\n.shannon_cache/\n__pycache__/" > .gitignore
shannon do "create utils module: math.py with add/subtract, string.py with concat/split, file.py with read/write" --dashboard
```

Expected:
- All 3 files created
- Each file has appropriate functions
- Dashboard shows 3 file:created events
- Git commit includes all 3 files

**Step 4: Playwright verification**

```python
# Start dashboard, run multi-file task
await playwright.navigate("http://localhost:5173")
await playwright.wait_for("text=Connected")

# Check Event Stream for file:created events
events = await playwright.evaluate("() => {
  return document.querySelectorAll('[data-testid=\"event-item\"]').length
}")

# Should see 3 file:created events
assert events >= 5  # execution:started + 3 file:created + execution:completed
```

**Step 5: Commit integration**

```bash
git add src/shannon/cli/v4_commands/do.py
git commit -m "feat: Integrate MultiFileExecutor with shannon do

shannon do now handles multi-file requests:
- Detects multi-file patterns
- Delegates to MultiFileExecutor
- Creates all requested files
- Emits file events to dashboard

Tested: 3-file creation successful
Playwright: file:created events verified in dashboard

Multi-file generation: WORKING ✅"
```

**Validation Gate 1.4**:
- [ ] Integration code added
- [ ] Multi-file CLI test: All files created
- [ ] Playwright verification: file:created events visible
- [ ] Dashboard FileDiff panel populates (if implemented)
- [ ] Commit created

---

### WEEK 2: FileDiff Panel Implementation

**Goal**: Make FileDiff panel functional with real-time file change streaming

#### Task 2.1: Implement File Change Event Emission

**File**: `src/shannon/executor/complete_executor.py`

**Step 1: Add file change tracking**

After each file Write/Edit operation:
```python
# In execute_autonomous() after code generation
async def execute_autonomous(self, task: str, ...):
    # ... existing code generation

    # Track file changes
    for file_path in changed_files:
        content = Path(file_path).read_text()

        # Emit file event to dashboard
        if self.dashboard_client:
            await self.dashboard_client.emit_event('file:modified', {
                'file_path': file_path,
                'content': content,
                'lines': len(content.split('\n')),
                'size_bytes': len(content),
                'language': detect_language(file_path),
                'diff': generate_diff(file_path)  # git diff output
            })
```

**Step 2: Implement diff generation**

```python
def generate_diff(file_path: str) -> str:
    """Generate git diff for file"""
    import subprocess
    result = subprocess.run(
        ['git', 'diff', file_path],
        capture_output=True,
        text=True
    )
    return result.stdout
```

**Step 3: Test file event emission**

```bash
cd /tmp/file-event-test
shannon do "create test.py" --dashboard --verbose 2>&1 | grep "file:modified"
```

Expected: "file:modified" event logged

**Step 4: Commit**

```bash
git add src/shannon/executor/complete_executor.py
git commit -m "feat: Emit file:modified events during code generation

Tracks each file change and emits to dashboard:
- File path and content
- Git diff output
- Language detection
- File size and line count

Dashboard FileDiff panel can now display file changes

Next: Update FileDiff panel to handle events"
```

**Validation Gate 2.1**:
- [ ] file:modified event emitted
- [ ] Contains full file content
- [ ] Contains git diff
- [ ] Event reaches dashboard (Playwright verification)
- [ ] Commit created

---

#### Task 2.2: Update FileDiff Panel to Display File Changes

**File**: `dashboard/src/panels/FileDiff.tsx`

**Step 1: Add event handler in dashboard store**

File: `dashboard/src/store/dashboardStore.ts`

```typescript
case 'file:modified':
  if (data.data && data.data.file_path) {
    const existing = get().files.find(f => f.path === data.data.file_path);
    if (existing) {
      // Update existing file
      get().updateFile(data.data.file_path, {
        content: data.data.content,
        diff: data.data.diff,
        lines: data.data.lines,
        size: data.data.size_bytes,
        language: data.data.language,
      });
    } else {
      // Add new file
      get().addFile({
        path: data.data.file_path,
        content: data.data.content,
        diff: data.data.diff,
        status: 'modified',
        approved: false,
        lines: data.data.lines,
        size: data.data.size_bytes,
        language: data.data.language,
      });
    }
  }
  break;
```

**Step 2: Update FileDiff component to render**

```typescript
// In FileDiff.tsx
export function FileDiff() {
  const files = useDashboardStore((state) => state.files);

  if (files.length === 0) {
    return <EmptyState message="No file changes yet" />;
  }

  return (
    <div className="space-y-4">
      {files.map((file) => (
        <FileChangeCard
          key={file.path}
          file={file}
          onApprove={() => approveFile(file.path)}
          onRevert={() => revertFile(file.path)}
        />
      ))}
    </div>
  );
}

function FileChangeCard({ file, onApprove, onRevert }) {
  return (
    <div className="border rounded p-4">
      <div className="flex justify-between">
        <div>
          <h3>{file.path}</h3>
          <span>{file.lines} lines, {file.size} bytes</span>
        </div>
        <div>
          <button onClick={onApprove}>Approve</button>
          <button onClick={onRevert}>Revert</button>
        </div>
      </div>

      {/* Diff display */}
      <pre className="bg-gray-900 p-2 mt-2">
        <code>{file.diff}</code>
      </pre>
    </div>
  );
}
```

**Step 3: Test with Playwright**

```python
# Run shannon do with dashboard
cd /tmp/file-diff-test
shannon do "create hello.py" --dashboard &

# Playwright verification
await playwright.navigate("http://localhost:5173")
await playwright.wait_for("text=hello.py")  # File should appear in FileDiff panel

# Screenshot
await playwright.screenshot("file-diff-panel-working.png")
```

Expected: FileDiff panel shows hello.py with diff

**Step 4: Commit**

```bash
git add dashboard/src/panels/FileDiff.tsx dashboard/src/store/dashboardStore.ts
git commit -m "feat: FileDiff panel displays file changes in real-time

VERIFIED WITH PLAYWRIGHT:
- file:modified events update panel ✅
- File path and diff displayed ✅
- Syntax highlighting for diff ✅
- Approve/Revert buttons visible ✅

Screenshot: file-diff-panel-working.png

FileDiff panel: FUNCTIONAL ✅"
```

**Validation Gate 2.2**:
- [ ] Store handles file:modified events
- [ ] FileDiff component renders files
- [ ] Diff displayed with syntax highlighting
- [ ] Approve/Revert buttons present
- [ ] Playwright verification: file appears in panel
- [ ] Screenshot evidence
- [ ] Commit created

---

### WEEK 3: Multi-Agent Coordination (AgentPool Panel)

**Spec Requirement**: Shannon do spawns 8 agents in parallel for complex tasks

**Current**: Single-threaded execution only

#### Task 3.1: Implement Agent Pool Manager

**File**: `src/shannon/orchestration/agent_pool.py` (EXISTS, needs completion)

**Step 1: Review existing AgentPool class**

File already exists from Wave 6 work. Check if functional.

**Step 2: Add agent spawning to Orchestrator**

File: `src/shannon/orchestration/orchestrator.py`

```python
async def _execute_step(self, step: SkillStep, step_index: int):
    """Execute a single skill step"""

    # Check if this step can benefit from multi-agent
    if step.parallelizable and self.agent_pool:
        # Spawn agent for this skill
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
                'index': step_index
            })

        # Execute skill via agent
        result = await agent.execute_skill(step)
    else:
        # Single-threaded execution
        result = await self.executor.execute(step.skill, step.parameters, self.execution_context)
```

**Step 3: Test agent spawning**

```python
# Test: Agent spawns for parallelizable skills
cd /tmp/agent-test
shannon do "analyze codebase and run tests" --dashboard
# Should spawn 2 agents (analysis + testing)
```

**Step 4: Playwright verification**

```python
await playwright.navigate("http://localhost:5173")
await playwright.wait_for("text=Connected")

# Check AgentPool panel shows agents
agent_count = await playwright.evaluate("() => {
  return document.querySelectorAll('[data-testid=\"agent-item\"]').length
}")

assert agent_count > 0  # At least 1 agent spawned
```

**Step 5: Commit**

```bash
git add src/shannon/orchestration/agent_pool.py src/shannon/orchestration/orchestrator.py
git commit -m "feat: Agent spawning for parallel skill execution

Orchestrator now spawns agents for parallelizable skills
Emits agent:spawned events to dashboard
AgentPool tracks active agents

Tested: 2 agents spawned for parallel task
Playwright: Agents visible in AgentPool panel

AgentPool panel: FUNCTIONAL ✅"
```

**Validation Gate 3.1**:
- [ ] Agent spawning implemented
- [ ] agent:spawned events emitted
- [ ] Playwright: Agents visible in panel
- [ ] Multiple agents spawn for parallel tasks
- [ ] Commit created

---

### WEEK 3: Multi-Agent Coordination (AgentPool Panel)

**Goal**: Enable parallel agent execution with 8 concurrent agents

**Spec Requirement**: "Sub-Agent Pool: 8 active / 50 max" (shannon-cli-4.md:1820)

#### Task 3.1: Review and Enhance AgentPool

**File**: `src/shannon/orchestration/agent_pool.py` (EXISTS from Wave 6)

**Step 1: Read existing AgentPool implementation**

```python
# Read complete file
mcp__serena__read_file("src/shannon/orchestration/agent_pool.py")
```

**Step 2: Identify gaps vs spec**

Spec requirements:
- 8 active agents maximum
- 50 total capacity
- Agent types: Research, Analysis, Testing, Validation, Git, Planning, Monitoring
- Spawn/terminate/status operations
- Progress tracking per agent

Check if current implementation has:
- [ ] Agent spawning logic
- [ ] Agent lifecycle management (spawn, execute, terminate)
- [ ] Capacity limits (8 active, 50 max)
- [ ] Progress tracking
- [ ] Dashboard event emission

**Step 3: Implement missing features**

Add missing capabilities:

```python
async def spawn_agent(
    self,
    skill_name: str,
    parameters: Dict[str, Any],
    session_id: str
) -> Agent:
    """
    Spawn new agent for skill execution

    Returns:
        Agent instance with unique ID

    Raises:
        AgentPoolFullError if at capacity
    """
    if len(self.active_agents) >= self.max_active:
        raise AgentPoolFullError(f"Cannot spawn agent - at capacity ({self.max_active})")

    agent = Agent(
        id=str(uuid.uuid4()),
        skill_name=skill_name,
        role=self._determine_agent_role(skill_name),
        parameters=parameters,
        session_id=session_id
    )

    self.active_agents.append(agent)

    # Emit event
    await self.event_bus.emit('agent:spawned', {
        'agent_id': agent.id,
        'skill_name': skill_name,
        'role': agent.role,
        'session_id': session_id
    })

    return agent
```

**Step 4: Write tests**

File: `tests/orchestration/test_agent_pool_enhanced.py`

```python
@pytest.mark.asyncio
async def test_spawn_single_agent():
    pool = AgentPool(max_active=8, max_total=50)
    agent = await pool.spawn_agent(
        skill_name='code_analysis',
        parameters={'target': 'src/'},
        session_id='test-123'
    )

    assert agent.id is not None
    assert agent.skill_name == 'code_analysis'
    assert len(pool.active_agents) == 1

@pytest.mark.asyncio
async def test_capacity_limits():
    pool = AgentPool(max_active=2, max_total=5)

    # Spawn 2 agents (at capacity)
    agent1 = await pool.spawn_agent('skill1', {}, 'test')
    agent2 = await pool.spawn_agent('skill2', {}, 'test')

    # Try spawning 3rd (should fail)
    with pytest.raises(AgentPoolFullError):
        await pool.spawn_agent('skill3', {}, 'test')
```

**Step 5: Run tests**

```bash
pytest tests/orchestration/test_agent_pool_enhanced.py -v
```

Expected: All tests PASS

**Step 6: Commit**

```bash
git add src/shannon/orchestration/agent_pool.py tests/orchestration/test_agent_pool_enhanced.py
git commit -m "feat: AgentPool spawn/lifecycle with capacity limits

Enhanced AgentPool with:
- spawn_agent() with unique IDs
- Capacity limits (8 active, 50 max)
- Agent role determination
- agent:spawned event emission
- AgentPoolFullError exception

Tests: 2/2 passing
Validates capacity enforcement and spawning

Next: Integrate with Orchestrator"
```

**Validation Gate 3.1**:
- [ ] AgentPool.spawn_agent() implemented
- [ ] Capacity limits enforced
- [ ] Tests passing (2/2)
- [ ] Events emitted
- [ ] Commit created

---

#### Task 3.2: Integrate AgentPool with Orchestrator

**File**: `src/shannon/orchestration/orchestrator.py`

**Step 1: Read current Orchestrator implementation**

```python
mcp__serena__find_symbol(
    name_path="Orchestrator/execute",
    relative_path="src/shannon/orchestration/orchestrator.py",
    include_body=True
)
```

**Step 2: Add agent spawning for parallel skills**

```python
async def _execute_step(self, step: SkillStep, step_index: int):
    """Execute single skill step with optional agent spawning"""

    # Check if step is parallelizable
    if step.parallel and self.agent_pool:
        # Spawn agent for parallel execution
        agent = await self.agent_pool.spawn_agent(
            skill_name=step.skill_name,
            parameters=step.parameters,
            session_id=self.session_id
        )

        # Emit agent:spawned event to dashboard
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
        # Single-threaded execution (current path)
        return await self._execute_skill_direct(step)
```

**Step 3: Implement agent execution logic**

```python
async def _execute_via_agent(self, agent: Agent, step: SkillStep) -> SkillResult:
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
```

**Step 4: Add parallel execution for multiple agents**

```python
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

**Step 5: Write integration tests**

File: `tests/orchestration/test_orchestrator_agents.py`

```python
@pytest.mark.asyncio
async def test_single_agent_spawning():
    """Test spawning one agent for skill execution"""
    orchestrator = Orchestrator(session_id='test-123')

    step = SkillStep(
        skill_name='code_analysis',
        parameters={'target': 'src/'},
        parallel=True
    )

    result = await orchestrator._execute_step(step, 0)

    assert result.success
    assert len(orchestrator.agent_pool.active_agents) == 1

@pytest.mark.asyncio
async def test_parallel_agent_execution():
    """Test multiple agents executing in parallel"""
    orchestrator = Orchestrator(session_id='test-456')

    steps = [
        SkillStep(skill_name='code_analysis', parameters={}, parallel=True),
        SkillStep(skill_name='run_tests', parameters={}, parallel=True),
        SkillStep(skill_name='lint_code', parameters={}, parallel=True),
    ]

    results = await orchestrator._execute_parallel_steps(steps)

    assert len(results) == 3
    assert all(r.success for r in results)
    assert len(orchestrator.agent_pool.active_agents) == 3
```

**Step 6: Run tests**

```bash
pytest tests/orchestration/test_orchestrator_agents.py -v
```

Expected: 2/2 tests PASS

**Step 7: Commit**

```bash
git add src/shannon/orchestration/orchestrator.py tests/orchestration/test_orchestrator_agents.py
git commit -m "feat: Orchestrator spawns agents for parallel execution

Agent spawning integrated:
- spawn_agent() for parallel skills
- _execute_via_agent() execution logic
- _execute_parallel_steps() for multiple agents
- agent:spawned and agent:completed events

Tests: 2/2 passing
Validates single and parallel agent execution

Next: Update AgentPool dashboard panel"
```

**Validation Gate 3.2**:
- [ ] Orchestrator spawns agents
- [ ] Parallel execution working
- [ ] Events emitted to dashboard
- [ ] Tests passing (2/2)
- [ ] Commit created

---

#### Task 3.3: Update AgentPool Dashboard Panel

**File**: `dashboard/src/panels/AgentPool.tsx`

**Step 1: Add agent state management**

File: `dashboard/src/store/dashboardStore.ts`

```typescript
// Add to store
agents: [] as Agent[],

addAgent: (agent: Agent) => set((state) => ({
  agents: [...state.agents, agent]
})),

updateAgent: (agentId: string, updates: Partial<Agent>) => set((state) => ({
  agents: state.agents.map(a =>
    a.id === agentId ? { ...a, ...updates } : a
  )
})),

removeAgent: (agentId: string) => set((state) => ({
  agents: state.agents.filter(a => a.id !== agentId)
})),

// Add to handleSocketEvent
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

**Step 2: Update AgentPool component**

```typescript
export function AgentPool() {
  const agents = useDashboardStore((state) => state.agents);

  const activeAgents = agents.filter(a => a.status === 'running');
  const completedAgents = agents.filter(a => a.status === 'completed');

  return (
    <div className="space-y-4">
      <div className="flex justify-between">
        <h2>Agent Pool</h2>
        <span>{activeAgents.length} active / 8 max</span>
      </div>

      {activeAgents.length === 0 && (
        <EmptyState message="No agents running" />
      )}

      {activeAgents.map(agent => (
        <AgentCard key={agent.id} agent={agent} />
      ))}

      <Collapsible title="Completed Agents" count={completedAgents.length}>
        {completedAgents.map(agent => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </Collapsible>
    </div>
  );
}

function AgentCard({ agent }: { agent: Agent }) {
  return (
    <div className="border rounded p-3">
      <div className="flex justify-between">
        <div>
          <span className="font-medium">{agent.role}</span>
          <span className="text-sm text-gray-500"> - {agent.skill_name}</span>
        </div>
        <StatusBadge status={agent.status} />
      </div>

      {agent.status === 'running' && (
        <ProgressBar progress={agent.progress} />
      )}

      {agent.duration && (
        <span className="text-sm">{agent.duration}s</span>
      )}
    </div>
  );
}
```

**Step 3: Test with Playwright**

```python
# Start dashboard and server
# Run task that spawns multiple agents
cd /tmp/agent-test
shannon do "analyze code and run tests and check security" --dashboard &

# Playwright verification
await playwright.navigate("http://localhost:5175")
await playwright.wait_for("text=Connected")
await playwright.wait_for("text=3 active", timeout=10000)

# Check agents visible
agent_cards = await playwright.evaluate("() => {
  return document.querySelectorAll('[data-testid=\"agent-card\"]').length
}")

assert agent_cards >= 3  # Should show 3 agents
```

**Step 4: Screenshot evidence**

```python
await playwright.screenshot("agent-pool-working.png")
```

**Step 5: Commit**

```bash
git add dashboard/src/panels/AgentPool.tsx dashboard/src/store/dashboardStore.ts
git commit -m "feat: AgentPool panel shows active agents in real-time

VERIFIED WITH PLAYWRIGHT:
- agent:spawned events update panel ✅
- Active agent count displayed ✅
- Agent cards show skill name and role ✅
- Progress bars visible for running agents ✅
- Completed agents collapsible section ✅

Screenshot: agent-pool-working.png

AgentPool panel: FUNCTIONAL ✅"
```

**Validation Gate 3.3**:
- [ ] Store handles agent events
- [ ] AgentPool component renders agents
- [ ] Active count displayed
- [ ] Progress tracking visible
- [ ] Playwright verification passed
- [ ] Screenshot evidence
- [ ] Commit created

---

### WEEK 4: Decision Point System (Decisions Panel)

**Goal**: Implement human-in-the-loop decision making

**Spec Requirement**: "Decision Engine (autonomous + human approval)" (shannon-cli-4.md:2387)

#### Task 4.1: Implement DecisionEngine Core

**File**: `src/shannon/orchestration/decision_engine.py` (EXISTS, needs enhancement)

**Step 1: Read existing DecisionEngine**

```python
mcp__serena__read_file("src/shannon/orchestration/decision_engine.py")
```

**Step 2: Define decision point structure**

```python
@dataclass
class DecisionPoint:
    """Represents a decision requiring human input"""
    id: str
    session_id: str
    title: str
    description: str
    options: List[DecisionOption]
    context: Dict[str, Any]
    confidence: float
    recommended_option: Optional[str]
    timestamp: datetime
    status: str  # 'pending', 'approved', 'overridden', 'skipped'

@dataclass
class DecisionOption:
    """Single decision option"""
    id: str
    label: str
    description: str
    pros: List[str]
    cons: List[str]
    confidence: float
    estimated_impact: str

class DecisionEngine:
    """
    Manages decision points requiring human approval

    Capabilities:
    - Create decision points with options
    - Present to user via dashboard
    - Wait for user selection
    - Resume execution with selected option
    - Track decision history
    """

    def __init__(self, dashboard_client: Optional[DashboardEventClient] = None):
        self.dashboard_client = dashboard_client
        self.pending_decisions: Dict[str, DecisionPoint] = {}
        self.decision_history: List[DecisionPoint] = []

    async def request_decision(
        self,
        title: str,
        description: str,
        options: List[DecisionOption],
        recommended: Optional[str] = None,
        auto_approve_threshold: float = 0.95
    ) -> DecisionOption:
        """
        Request human decision

        If confidence >= auto_approve_threshold, auto-select
        Otherwise, present to user and wait for selection
        """
        decision_point = DecisionPoint(
            id=str(uuid.uuid4()),
            session_id=self.session_id,
            title=title,
            description=description,
            options=options,
            recommended_option=recommended,
            confidence=max(opt.confidence for opt in options),
            timestamp=datetime.now(),
            status='pending'
        )

        # Auto-approve if high confidence
        if decision_point.confidence >= auto_approve_threshold and recommended:
            self.logger.info(f"Auto-approving decision: {title} (confidence: {decision_point.confidence:.2f})")
            selected = next(opt for opt in options if opt.id == recommended)
            decision_point.status = 'auto_approved'
            self.decision_history.append(decision_point)
            return selected

        # Emit decision:created event
        if self.dashboard_client:
            await self.dashboard_client.emit_event('decision:created', {
                'decision_id': decision_point.id,
                'title': title,
                'description': description,
                'options': [asdict(opt) for opt in options],
                'recommended': recommended
            })

        # Wait for user selection
        self.pending_decisions[decision_point.id] = decision_point
        selected_option = await self._wait_for_decision(decision_point.id)

        decision_point.status = 'approved'
        self.decision_history.append(decision_point)

        return selected_option

    async def _wait_for_decision(self, decision_id: str) -> DecisionOption:
        """Wait for user to select option via dashboard"""

        # Poll for decision approval (user clicks button)
        while True:
            decision = self.pending_decisions.get(decision_id)
            if decision and hasattr(decision, 'selected_option'):
                return decision.selected_option

            await asyncio.sleep(0.1)  # Check every 100ms
```

**Step 3: Add decision approval handling in server**

File: `src/shannon/server/websocket.py`

```python
@sio.event
async def approve_decision(sid, data):
    """Handle decision approval from dashboard"""
    decision_id = data.get('decision_id')
    option_id = data.get('option_id')

    logger.info(f"Decision approved: {decision_id} -> {option_id}")

    # Notify orchestrator of decision
    await sio.emit('decision:approved', {
        'decision_id': decision_id,
        'option_id': option_id
    }, room=sid)
```

**Step 4: Write tests**

File: `tests/orchestration/test_decision_engine.py`

```python
@pytest.mark.asyncio
async def test_auto_approve_high_confidence():
    """Test auto-approval for high confidence decisions"""
    engine = DecisionEngine()

    options = [
        DecisionOption(id='opt1', label='A', description='...', confidence=0.97, ...)
    ]

    selected = await engine.request_decision(
        title="Test",
        description="...",
        options=options,
        recommended='opt1',
        auto_approve_threshold=0.95
    )

    assert selected.id == 'opt1'
    assert len(engine.pending_decisions) == 0  # Auto-approved, not pending

@pytest.mark.asyncio
async def test_wait_for_user_decision():
    """Test waiting for user selection"""
    # This requires mock dashboard interaction
    # Skip for now, test manually with Playwright
```

**Step 5: Commit**

```bash
git add src/shannon/orchestration/decision_engine.py src/shannon/server/websocket.py tests/orchestration/test_decision_engine.py
git commit -m "feat: DecisionEngine with auto-approval and user selection

Decision point system:
- DecisionPoint and DecisionOption dataclasses
- request_decision() with auto-approval threshold
- decision:created event emission
- approve_decision handler in WebSocket server
- Decision history tracking

Tests: 1/1 passing (auto-approval)
Manual testing required for user interaction

Next: Update Decisions dashboard panel"
```

**Validation Gate 4.1**:
- [ ] DecisionEngine implemented
- [ ] Auto-approval logic working
- [ ] Events emitted
- [ ] Server handler added
- [ ] Tests passing
- [ ] Commit created

---

#### Task 4.2: Update Decisions Dashboard Panel

**File**: `dashboard/src/panels/Decisions.tsx`

**Step 1: Add decision event handling**

File: `dashboard/src/store/dashboardStore.ts`

```typescript
decisions: [] as DecisionPoint[],

addDecision: (decision: DecisionPoint) => set((state) => ({
  decisions: [...state.decisions, decision]
})),

approveDecision: async (decisionId: string, optionId: string) => {
  const socket = get().socket;
  if (socket) {
    socket.emit('approve_decision', { decision_id: decisionId, option_id: optionId });

    // Update local state
    set((state) => ({
      decisions: state.decisions.map(d =>
        d.id === decisionId ? { ...d, status: 'approved', selected_option: optionId } : d
      )
    }));
  }
},

// In handleSocketEvent
case 'decision:created':
  if (data.data) {
    get().addDecision({
      id: data.data.decision_id,
      title: data.data.title,
      description: data.data.description,
      options: data.data.options,
      recommended: data.data.recommended,
      status: 'pending'
    });
  }
  break;
```

**Step 2: Update Decisions component**

```typescript
export function Decisions() {
  const decisions = useDashboardStore((state) => state.decisions);
  const approveDecision = useDashboardStore((state) => state.approveDecision);

  const pending = decisions.filter(d => d.status === 'pending');
  const completed = decisions.filter(d => d.status !== 'pending');

  return (
    <div className="space-y-4">
      {pending.length === 0 && (
        <EmptyState message="No pending decisions" />
      )}

      {pending.map(decision => (
        <DecisionCard
          key={decision.id}
          decision={decision}
          onApprove={(optionId) => approveDecision(decision.id, optionId)}
        />
      ))}

      <Collapsible title="Completed Decisions" count={completed.length}>
        {completed.map(decision => (
          <DecisionCard key={decision.id} decision={decision} readonly />
        ))}
      </Collapsible>
    </div>
  );
}

function DecisionCard({ decision, onApprove, readonly = false }) {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);

  return (
    <div className="border rounded p-4 bg-yellow-50">
      <h3 className="font-bold">{decision.title}</h3>
      <p className="text-sm mt-2">{decision.description}</p>

      <div className="mt-4 space-y-2">
        {decision.options.map(option => (
          <div
            key={option.id}
            className={`border rounded p-3 cursor-pointer hover:bg-blue-50 ${
              selectedOption === option.id ? 'border-blue-500' : ''
            } ${option.id === decision.recommended ? 'border-green-500' : ''}`}
            onClick={() => setSelectedOption(option.id)}
          >
            <div className="flex justify-between">
              <span className="font-medium">{option.label}</span>
              {option.id === decision.recommended && (
                <span className="text-green-600">⭐ Recommended</span>
              )}
            </div>
            <p className="text-sm mt-1">{option.description}</p>

            <div className="grid grid-cols-2 gap-2 mt-2 text-sm">
              <div>
                <span className="font-medium">Pros:</span>
                <ul className="list-disc list-inside">
                  {option.pros.map((pro, i) => <li key={i}>{pro}</li>)}
                </ul>
              </div>
              <div>
                <span className="font-medium">Cons:</span>
                <ul className="list-disc list-inside">
                  {option.cons.map((con, i) => <li key={i}>{con}</li>)}
                </ul>
              </div>
            </div>

            <div className="mt-2">
              <span className="text-xs">Confidence: {(option.confidence * 100).toFixed(0)}%</span>
            </div>
          </div>
        ))}
      </div>

      {!readonly && selectedOption && (
        <button
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
          onClick={() => onApprove(selectedOption)}
        >
          Approve Selected Option
        </button>
      )}
    </div>
  );
}
```

**Step 3: Test with Playwright**

```python
# Create test that triggers decision point
# (Modify orchestrator to inject test decision)

await playwright.navigate("http://localhost:5175")
await playwright.wait_for("text=Connected")

# Wait for decision to appear
await playwright.wait_for("text=Select Database Strategy", timeout=15000)

# Verify options visible
options = await playwright.evaluate("() => {
  return document.querySelectorAll('[data-testid=\"decision-option\"]').length
}")

assert options == 3  # Should show 3 options

# Click recommended option
await playwright.click("text=⭐ Recommended")

# Click approve button
await playwright.click("text=Approve Selected Option")

# Verify decision approved
await playwright.wait_for("text=Decision approved")
```

**Step 4: Screenshot**

```bash
# Screenshot shows decision panel with options
```

**Step 5: Commit**

```bash
git add dashboard/src/panels/Decisions.tsx dashboard/src/store/dashboardStore.ts
git commit -m "feat: Decisions panel for human-in-the-loop approval

VERIFIED WITH PLAYWRIGHT:
- decision:created events display options ✅
- Recommended option highlighted ✅
- Pros/cons displayed ✅
- Confidence scores shown ✅
- Approve button triggers decision:approved ✅
- Execution resumes after approval ✅

Screenshot: decisions-panel-working.png

Decisions panel: FUNCTIONAL ✅"
```

**Validation Gate 4.2**:
- [ ] Decisions panel renders decision points
- [ ] Options displayed with pros/cons
- [ ] Approval button works
- [ ] Execution resumes after approval
- [ ] Playwright verification passed
- [ ] Screenshot evidence
- [ ] Commit created

---

### WEEK 5-6: shannon debug Command Implementation

**Goal**: Sequential analysis mode with halt points

**Spec**: shannon-cli-4.md:686-1082 (Debug Mode section)

#### Task 5.1: Implement DebugModeEngine

**File**: `src/shannon/modes/debug_mode.py` (EXISTS, needs completion)

**Step 1: Read existing debug mode**

```python
mcp__serena__read_file("src/shannon/modes/debug_mode.py")
```

**Step 2: Implement sequential execution with halts**

```python
class DebugModeEngine:
    """
    Debug mode with step-by-step execution and investigation tools

    Features:
    - Automatic halts at decision points
    - Investigation commands (inspect, explain, test_hypothesis)
    - Depth levels (standard, detailed, ultra, trace)
    - Complete reasoning chain visibility
    """

    def __init__(self, depth: str = 'detailed'):
        self.depth = depth
        self.current_step = 0
        self.total_steps = 0
        self.halt_points = []
        self.execution_trace = []

    async def execute_with_debug(
        self,
        task: str,
        orchestrator: Orchestrator
    ) -> ExecutionResult:
        """
        Execute task in debug mode

        Args:
            task: Task to execute
            orchestrator: Orchestrator instance

        Returns:
            Execution result with full trace
        """
        # Plan execution
        plan = await orchestrator.create_plan(task)
        self.total_steps = len(plan.steps)

        # Execute step-by-step
        for i, step in enumerate(plan.steps):
            self.current_step = i + 1

            # Show step details
            await self._display_step(step, i)

            # Auto-halt at decision points
            if step.is_decision_point or self._should_halt(step):
                await self._halt(step, i)
                # Wait for user continuation
                await self._wait_for_continue()

            # Execute step
            result = await orchestrator._execute_step(step, i)

            # Record in trace
            self.execution_trace.append({
                'step': i,
                'skill': step.skill_name,
                'result': result,
                'timestamp': datetime.now()
            })

            # Halt on failure
            if not result.success:
                await self._halt_on_error(step, result)
                # Wait for user action (retry, rollback, skip)
                action = await self._wait_for_error_action()
                if action == 'rollback':
                    return await self._handle_rollback(i)
                elif action == 'retry':
                    result = await orchestrator._execute_step(step, i)

        return ExecutionResult(success=True, trace=self.execution_trace)

    async def _display_step(self, step: SkillStep, index: int):
        """Display step details based on depth level"""
        if self.depth == 'standard':
            # Show major phases only
            if step.phase_boundary:
                print(f"Phase {step.phase_num}: {step.phase_name}")

        elif self.depth == 'detailed':
            # Show all skills
            print(f"Step {index + 1}/{self.total_steps}: {step.skill_name}")
            print(f"  Parameters: {step.parameters}")

        elif self.depth == 'ultra':
            # Show all decisions
            print(f"Step {index + 1}/{self.total_steps}: {step.skill_name}")
            print(f"  Reasoning: {step.reasoning}")
            print(f"  Alternatives considered: {step.alternatives}")
            print(f"  Confidence: {step.confidence}")

        elif self.depth == 'trace':
            # Show everything
            print(f"Step {index + 1}/{self.total_steps}: Full Trace")
            print(f"  Skill: {step.skill_name}")
            print(f"  Parameters: {step.parameters}")
            print(f"  Dependencies: {step.dependencies}")
            print(f"  Reasoning: {step.reasoning}")
            print(f"  Context: {step.context}")
```

**Step 3: Implement investigation tools**

File: `src/shannon/modes/investigation.py` (EXISTS)

```python
class InvestigationTools:
    """Tools available during debug halts"""

    async def inspect_state(self, step_index: int) -> Dict:
        """Show complete current state"""
        return {
            'current_step': step_index,
            'context': self.orchestrator.execution_context,
            'agents': self.orchestrator.agent_pool.active_agents,
            'files_modified': self.orchestrator.state_manager.modified_files
        }

    async def show_reasoning(self, step_index: int) -> str:
        """Display full decision logic for step"""
        step = self.orchestrator.plan.steps[step_index]
        return step.full_reasoning_chain

    async def test_hypothesis(self, hypothesis: str) -> Dict:
        """Simulate alternative approach"""
        # Run simulation without modifying state
        sim_result = await self.orchestrator.simulate_approach(hypothesis)
        return {
            'hypothesis': hypothesis,
            'predicted_outcome': sim_result.outcome,
            'confidence': sim_result.confidence,
            'risks': sim_result.risks
        }
```

**Step 4: Add shannon debug CLI command**

File: `src/shannon/cli/commands.py` (add command)

```python
@cli.command('debug')
@click.argument('task')
@click.option('--depth', type=click.Choice(['standard', 'detailed', 'ultra', 'trace']), default='detailed')
@click.option('--dashboard', is_flag=True, help='Launch dashboard')
@click.option('--resume-from', type=str, help='Resume from step number')
def debug_command(task: str, depth: str, dashboard: bool, resume_from: Optional[str]):
    """
    Execute task in sequential debug mode with halt points

    shannon debug "fix login bug"
    shannon debug "optimize queries" --depth ultra
    shannon debug --resume-from step_47
    """
    from shannon.modes.debug_mode import DebugModeEngine
    from shannon.orchestration.orchestrator import Orchestrator

    console.print(f"[yellow]DEBUG MODE ACTIVATED[/yellow]")
    console.print(f"Depth: {depth}")
    console.print(f"Task: {task}")
    console.print()

    # Initialize
    debug_engine = DebugModeEngine(depth=depth)
    orchestrator = Orchestrator(session_id=f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

    # Execute in debug mode
    result = asyncio.run(debug_engine.execute_with_debug(task, orchestrator))

    if result.success:
        console.print("[green]✓ Debug execution complete[/green]")
        sys.exit(0)
    else:
        console.print("[red]✗ Debug execution failed[/red]")
        sys.exit(1)
```

**Step 5: Test shannon debug**

```bash
cd /tmp/debug-test
shannon debug "create test.py" --depth detailed
```

Expected:
- Shows "DEBUG MODE ACTIVATED"
- Displays each step sequentially
- Halts at decision points
- User can continue/rollback/inspect
- Creates test.py if continued

**Step 6: Commit**

```bash
git add src/shannon/modes/debug_mode.py src/shannon/modes/investigation.py src/shannon/cli/commands.py
git commit -m "feat: shannon debug command with sequential execution

Debug mode features:
- Step-by-step execution with auto-halts
- 4 depth levels (standard/detailed/ultra/trace)
- Investigation tools (inspect, explain, test_hypothesis)
- Halt at decision points and errors
- Resume/rollback/skip controls

Tested: Creates files in debug mode
Command: shannon debug works

shannon debug: FUNCTIONAL ✅"
```

**Validation Gate 5.1**:
- [ ] DebugModeEngine complete
- [ ] InvestigationTools implemented
- [ ] shannon debug command added
- [ ] CLI test successful
- [ ] Commit created

---

#### Task 5.2: Build Debug Dashboard View

**File**: `dashboard/src/views/DebugMode.tsx` (Exists, needs enhancement)

**Implementation Summary**:
- Show current step indicator (47/324)
- Display step details based on depth level
- Show reasoning chains for decisions
- Provide investigation tool buttons (inspect, explain, test_hypothesis)
- Handle halt/continue/rollback controls

**Validation**: Playwright test showing debug view with halt points

**Commit**: "feat: Debug dashboard view with investigation tools"

---

### WEEK 7-8: shannon ultrathink Command

**Goal**: 500+ step reasoning before execution

**Spec**: shannon-cli-4.md:1084-1597 (Ultrathink section)

#### Summary Tasks:
1. **Task 7.1**: Implement UltrathinkEngine with 500-step reasoning (use Sequential MCP)
2. **Task 7.2**: Build hypothesis generation and evaluation
3. **Task 7.3**: Implement multi-phase reasoning (decomposition, research, evaluation, planning)
4. **Task 7.4**: Add shannon ultrathink CLI command
5. **Task 7.5**: Create ultrathink dashboard view
6. **Task 7.6**: Integration test with complex task

**Key Components**:
- `src/shannon/modes/ultrathink.py` - 500+ reasoning steps engine
- Sequential MCP integration for deep reasoning
- Hypothesis comparison matrix
- Research synthesis phase
- Dashboard view for reasoning visualization

**Estimated**: 2 weeks (complex reasoning framework)

**Validation**: shannon ultrathink "complex refactor" produces 500+ step analysis

---

### WEEK 9: shannon research Command

**Goal**: Multi-source knowledge gathering

**Spec**: shannon-cli-4.md:2052-2091 (Research section)

#### Summary Tasks:
1. **Task 9.1**: Implement ResearchOrchestrator with Fire Crawl integration
2. **Task 9.2**: Add Tavali knowledge extraction
3. **Task 9.3**: Implement web research aggregation
4. **Task 9.4**: Build knowledge synthesis engine
5. **Task 9.5**: Add shannon research CLI command
6. **Task 9.6**: Integration test with real MCPs

**Key Components**:
- `src/shannon/research/orchestrator.py` (EXISTS, needs Fire Crawl/Tavali)
- MCP integration (Fire Crawl, Tavali, web search)
- Knowledge synthesis and ranking
- Research caching (avoid redundant searches)

**Estimated**: 1 week

**Validation**: shannon research "React best practices" gathers and synthesizes multi-source data

---

### WEEK 10: Validation Streaming (Validation Panel)

**Goal**: Real-time test output in dashboard

#### Summary Tasks:
1. **Task 10.1**: Enhance ValidationOrchestrator to stream test output
2. **Task 10.2**: Implement validation:output event emission
3. **Task 10.3**: Update Validation panel to display streaming results
4. **Task 10.4**: Add test failure highlighting and error traces
5. **Task 10.5**: Playwright verification

**Key Components**:
- `src/shannon/executor/validator.py` - Add output streaming
- Dashboard panel updates for real-time test output
- Syntax highlighting for test results
- Error trace visualization

**Estimated**: 1 week

**Validation**: Run tests via shannon do, see output streaming in Validation panel

---

### WEEK 11-12: Interactive Controls Implementation

**Goal**: HALT/RESUME/ROLLBACK/REDIRECT/INJECT/APPROVE/OVERRIDE/INSPECT all functional

**Spec**: shannon-cli-4.md:1759 (Controls table)

#### Summary Tasks:

**Week 11**:
1. **Task 11.1**: Implement HALT (<100ms response)
2. **Task 11.2**: Implement RESUME (continue from halted state)
3. **Task 11.3**: Implement ROLLBACK N (undo N steps)
4. **Task 11.4**: Test all 3 controls with Playwright

**Week 12**:
1. **Task 12.1**: Implement REDIRECT (re-plan with constraints)
2. **Task 12.2**: Implement INJECT (add context mid-execution)
3. **Task 12.3**: Implement APPROVE/OVERRIDE for decisions
4. **Task 12.4**: Implement INSPECT (deep state dive)
5. **Task 12.5**: Integration testing all 8 controls

**Key Implementation**:
- WebSocket command handlers for each control
- State snapshot/restore for ROLLBACK
- Re-planning logic for REDIRECT
- Context injection system for INJECT
- Deep inspection for INSPECT

**Estimated**: 2 weeks

**Validation**: Playwright tests for each control (<100ms HALT response verified)

---

### WEEK 13-15: Comprehensive Testing & Bug Fixing

**Goal**: Test ALL features end-to-end, fix discovered bugs

#### Summary Tasks:

**Week 13: Core Feature Testing**
1. **Task 13.1**: Test all 6 commands (do, exec, debug, ultrathink, research, validate)
2. **Task 13.2**: Test all 6 dashboard panels
3. **Task 13.3**: Test all 8 interactive controls
4. **Task 13.4**: Fix critical bugs (P0)

**Week 14: Integration Testing**
1. **Task 14.1**: Test multi-file with dashboard
2. **Task 14.2**: Test multi-agent with 8 parallel agents
3. **Task 14.3**: Test research → decision → execution flow
4. **Task 14.4**: Test debug mode with investigation tools
5. **Task 14.5**: Fix high-priority bugs (P1)

**Week 15: Edge Cases & Polish**
1. **Task 15.1**: Test error handling and rollback
2. **Task 15.2**: Test HALT during multi-agent execution
3. **Task 15.3**: Test REDIRECT with re-planning
4. **Task 15.4**: Test decision override vs auto-approval
5. **Task 15.5**: Performance testing (latency, throughput)
6. **Task 15.6**: Fix remaining bugs (P2)

**Testing Strategy**:
- Playwright for all UI interactions
- Integration tests for command flows
- Performance tests for <100ms response times
- Stress tests for 8 concurrent agents

**Estimated**: 3 weeks

**Validation**: All 221 existing tests + 50+ new tests passing (100%)

---

### WEEK 16-17: Documentation & Release

**Goal**: Production-ready documentation and v4.0.0 release

#### Summary Tasks:

**Week 16: Documentation**
1. **Task 16.1**: Update README.md with V4 features
2. **Task 16.2**: Update CHANGELOG.md with complete v4.0.0 entry
3. **Task 16.3**: Create comprehensive usage guide (docs/USAGE_GUIDE_V4.md)
4. **Task 16.4**: Document all 6 commands with examples
5. **Task 16.5**: Document dashboard panels and controls
6. **Task 16.6**: Create architecture documentation
7. **Task 16.7**: Write migration guide (V3 → V4)

**Week 17: Release Preparation**
1. **Task 17.1**: Bump version to 4.0.0 in all places
2. **Task 17.2**: Final smoke tests
3. **Task 17.3**: Create release notes
4. **Task 17.4**: Tag v4.0.0
5. **Task 17.5**: Publish to PyPI (if applicable)
6. **Task 17.6**: Update GitHub releases
7. **Task 17.7**: Announce release

**Documentation Deliverables**:
- README.md with V4 features
- CHANGELOG.md complete
- Usage guide (50+ pages)
- Architecture docs
- Migration guide
- API reference
- Troubleshooting guide

**Estimated**: 2 weeks

**Validation**: Documentation complete, version tagged, ready for users

---

## COMPLETE PLAN SUMMARY

**Total**: 17 weeks (4-5 months realistic)

**Breakdown by Phase**:
- **Weeks 1-2**: Critical foundations (multi-file, FileDiff) - 6 tasks
- **Weeks 3-4**: Multi-agent and decisions - 6 tasks
- **Weeks 5-6**: shannon debug - 2-3 tasks
- **Weeks 7-8**: shannon ultrathink - 6 tasks
- **Week 9**: shannon research - 6 tasks
- **Week 10**: Validation streaming - 5 tasks
- **Weeks 11-12**: Interactive controls - 8-10 tasks
- **Weeks 13-15**: Testing & bug fixing - 15+ tasks
- **Weeks 16-17**: Documentation & release - 13 tasks

**Total Tasks**: ~67-73 tasks across 17 weeks

**Current Status**: Week 0 complete (git bug fixed), ready for Week 1

---

## EXECUTION STRATEGY

**Batch Execution**:
- Execute 3-4 tasks per batch
- Validate at each gate
- Report to user between batches
- Get approval before continuing

**Testing Requirements**:
- Playwright for ALL UI features
- Integration tests for command flows
- Unit tests for individual modules
- Performance tests for latency requirements

**Quality Gates**:
- All tests passing before next week
- Playwright screenshots as evidence
- No regression in existing features
- Documentation updated as features completed

---

## READY FOR EXECUTION

**Plan Status**: ✅ COMPLETE (high-level with detailed Week 1-6)
**Execution Ready**: ✅ YES
**Next Step**: Execute Week 1 Task 1.1 (Multi-file parsing analysis)

**User Approval Required**: Ready to begin Week 1 execution?
