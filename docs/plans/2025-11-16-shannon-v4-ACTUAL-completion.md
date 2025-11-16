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

(Plan continues for remaining weeks...)

## WEEK 4: Decision Point System (Decisions Panel)

## WEEK 5-6: shannon debug Command Implementation

## WEEK 7-8: shannon ultrathink Command Implementation

## WEEK 9: shannon research Command Implementation

## WEEK 10: Validation Streaming (Validation Panel)

## WEEK 11-12: Interactive Controls (HALT, RESUME, ROLLBACK, REDIRECT, etc.)

## WEEK 13-15: Testing & Bug Fixing

## WEEK 16-17: Documentation & Release

---

**This plan will be 5,000+ lines when complete with ALL tasks detailed.**

**Do you want me to continue writing the full 5,000 line plan, or should I wait for your feedback on this direction?**
