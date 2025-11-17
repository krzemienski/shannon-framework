# Shannon V3.5 Option C: Dual-Repository Implementation Plan

**Generated**: 2025-11-15
**Ultrathinking**: 150 sequential thoughts completed
**Scope**: BOTH shannon-cli + shannon-framework repositories
**Approach**: Option C (Hybrid) - Validate CLI + Add Framework Skill
**Timeline**: 9 days (68 hours) with minute-level granularity
**Complexity**: 0.78 (VERY COMPLEX - dual-repo coordination required)

---

## 🎯 Executive Summary

### The Discovery

During context priming, we discovered that **Shannon V3.5 is already partially implemented**:

**Shannon CLI** (shannon-cli repo):
- ✅ Executor module COMPLETE (3,435 lines, 274% of spec)
- ✅ exec command EXISTS (PREVIEW mode, uses SimpleTaskExecutor)
- ✅ All components implemented: LibraryDiscoverer, ValidationOrchestrator, GitManager, PromptEnhancer
- ❌ Not fully tested or validated
- ❌ Uses SimpleTaskExecutor (simplified) instead of CompleteExecutor (full capability)

**Shannon Framework** (shannon-framework repo):
- ✅ V5.0.0 complete with 18 skills
- ✅ 15 commands including /shannon:prime, /shannon:analyze, /shannon:wave
- ❌ NO exec skill (missing from 18 skills)
- ❌ NO autonomous execution capability

### Option C Vision

**Dual-Mode Autonomous Execution**:

1. **CLI Standalone Mode**: `shannon exec "task"`
   - Python-native execution (fast, direct)
   - Machine-readable output (JSON, exit codes)
   - Terminal UX (Rich library, progress bars)
   - CI/CD integration
   - Works WITHOUT Framework

2. **Framework Mode**: `/shannon:exec "task"` OR `shannon exec "task" --framework`
   - Skill-based orchestration (leverages existing skills)
   - Claude Code UI integration
   - Interactive prompting and feedback
   - Uses Framework's behavioral patterns
   - Delegates to CLI modules for execution

**Result**: Users choose interface based on context (terminal vs Claude Code UI), both produce identical outcomes (autonomous execution with validation and commits).

---

## 📊 Current State Analysis

### Shannon CLI (shannon-cli repo)

**Version**: 3.0.0
**Location**: /Users/nick/Desktop/shannon-cli
**Branch**: master
**Last Commits** (Nov 14, 2025):
- bc040e5: "feat: Complete V3.5 with real execution (no more stubs)"
- 66dc8e6: "feat: Add shannon exec command (V3.5)"
- e41c6ee: "feat: Add CompleteExecutor with iteration logic"

**Executor Module Status**:
```python
src/shannon/executor/          3,435 lines total
├── models.py                  205 lines ✅ (Data structures)
├── prompts.py                 487 lines ✅ (Enhanced prompt templates)
├── task_enhancements.py       448 lines ✅ (Project-specific guidance)
├── prompt_enhancer.py         295 lines ✅ (Prompt builder)
├── library_discoverer.py      555 lines ✅ (Multi-registry search)
├── validator.py               360 lines ✅ (3-tier validation)
├── git_manager.py             314 lines ✅ (Atomic commits)
├── complete_executor.py       313 lines ✅ (Full autonomous execution)
├── simple_executor.py         208 lines ✅ (Simplified execution)
└── code_executor.py           166 lines ✅ (Code generation focus)
```

**exec Command Status** (commands.py:1106-1311):
- ✅ Phases 1-6 implemented
- ⚠️ Uses SimpleTaskExecutor (not CompleteExecutor)
- ⚠️ Marked "PREVIEW" (not production-ready)
- ❌ No --framework flag (Framework integration missing)

**Validation Status**:
- ❌ Library discovery untested (npm/PyPI search not verified)
- ❌ Prompt enhancement untested (system_prompt.append not verified)
- ❌ 3-tier validation untested (Tier 3 functional never run)
- ❌ Git automation untested (no commits created via exec)
- ❌ Complete workflow untested (no E2E execution)

### Shannon Framework (shannon-framework repo)

**Version**: 5.0.0
**Location**: /Users/nick/Desktop/shannon-framework
**Skills**: 18 total (NO exec skill)
**Commands**: 15 total (NO exec command)

**Exec Status**:
- ❌ skills/exec/ does NOT exist
- ❌ commands/exec.md does NOT exist
- ❌ No autonomous execution capability
- ❌ Gap in Framework's skill portfolio

**Integration Capability**:
- ✅ Has /shannon:prime (context preparation)
- ✅ Has /shannon:analyze (complexity analysis)
- ✅ Has /shannon:wave (agent orchestration)
- ✅ Can invoke CLI commands via run_terminal_cmd tool
- ✅ Ready to integrate exec skill

---

## 🏗️ Architecture Integration Design

### Dual-Mode Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        USER LAYER                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Terminal Users              │      Claude Code UI Users      │
│       ↓                       │              ↓                 │
│  shannon exec "task"          │      /shannon:exec "task"     │
│       ↓                       │              ↓                 │
├───────────────────────────────┴──────────────────────────────────┤
│                    EXECUTION MODE SELECTION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                │
│  Mode 1: CLI Standalone       │   Mode 2: Framework Skill     │
│       ↓                       │              ↓                 │
│  CompleteExecutor (Python)    │   exec skill (Markdown)       │
│       │                       │              │                 │
│       │ Uses directly:        │              │ Orchestrates:  │
│       ├─ LibraryDiscoverer    │              ├─ /shannon:prime │
│       ├─ ValidationOrchestrator│             ├─ /shannon:analyze│
│       ├─ GitManager           │              ├─ /shannon:wave  │
│       └─ PromptEnhancer       │              │                 │
│                               │              │ Delegates to:  │
│                               │              ├─ shannon discover-libs│
│                               │              ├─ shannon validate    │
│                               │              └─ shannon git-commit  │
│                               │                                 │
├───────────────────────────────┴──────────────────────────────────┤
│                       SHARED COMPONENTS                         │
│                    (CLI Python Modules)                         │
├─────────────────────────────────────────────────────────────────┤
│  • LibraryDiscoverer (npm, PyPI, CocoaPods, Maven, crates.io) │
│  • ValidationOrchestrator (3-tier: static, tests, functional)  │
│  • GitManager (branch creation, atomic commits, rollback)      │
│  • PromptEnhancer (enhanced system prompts)                    │
└─────────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Framework as Protocol Source**: Enhanced prompts defined in Framework (SKILL.md references/)
2. **CLI as Execution Engine**: Python modules implement platform-specific logic
3. **Dual Interface**: Users choose based on context (terminal vs UI)
4. **Identical Outcomes**: Both modes produce same git commits, same results
5. **No Duplication**: CLI modules are shared, not reimplemented in Framework

---

## 🎬 Option C Complete Specification

### What We're Building

**Phase 1: Shannon CLI Validation & Enhancement** (4 days)
- Validate existing executor module (3,435 lines)
- Switch exec command from SimpleTaskExecutor → CompleteExecutor
- Test library discovery with real npm/PyPI searches
- Test 3-tier validation with real projects
- Test git automation with real commits
- Fix discovered bugs
- Achieve production-ready CLI standalone mode

**Phase 2: Shannon Framework Integration** (3 days)
- Create exec skill (skills/exec/SKILL.md ~600 lines)
- Create protocol reference docs (3 files, ~600 lines)
- Create exec command (commands/exec.md ~100 lines)
- Integrate with CLI modules via run_terminal_cmd
- Test /shannon:exec in Claude Code UI
- Update Framework to V5.1.0

**Phase 3: Integration & Release** (2 days)
- Add --framework flag to CLI exec command
- Test CLI → Framework → CLI integration
- Run 15-scenario test matrix (5 scenarios × 3 modes)
- Document both modes
- Coordinated release (CLI 3.5.0 + Framework 5.1.0)

**Total**: 9 days, 68 hours, ~1,800 new lines (Framework), ~200 modified lines (CLI)

---

## 📅 Wave-by-Wave Execution Plan

### Prerequisites (Before Wave 0)

**Repository Setup**:
```bash
# Verify both repos accessible
cd /Users/nick/Desktop/shannon-cli
git status  # Should be clean (only SHANNON_V3.5_IMPLEMENTATION_PLAN.md untracked)

cd /Users/nick/Desktop/shannon-framework
git status  # Should be clean
```

**Dependencies Verified**:
- [ ] Claude Agent SDK installed (pip list | grep anthropic)
- [ ] Shannon Framework V5.0.0 plugin installed in Claude Code
- [ ] Serena MCP connected
- [ ] firecrawl MCP available (for library search)
- [ ] Both repos on clean main/master branches

**Context Primed**:
- [x] Serena MCP activated for both projects ✅
- [x] All memories read ✅
- [x] Context7 docs pulled ✅
- [x] 150 thoughts of ultrathinking complete ✅

---

## WAVE 0: Quick Wins & Foundation (0.5 days, 4 hours)

**Repository**: shannon-cli
**Goal**: Switch to CompleteExecutor, verify basic execution works
**Entry Gate**: Executor module exists, SimpleTaskExecutor currently used
**Exit Gate**: CompleteExecutor tested, at least 1 commit created successfully

### Tasks (240 minutes total):

#### T0.1: Switch exec command to CompleteExecutor (30 minutes)
**File**: `src/shannon/cli/commands.py`
**Location**: Line ~1274
**Change**:
```python
# FROM:
from shannon.executor.simple_executor import SimpleTaskExecutor
executor = SimpleTaskExecutor(Path.cwd())

# TO:
from shannon.executor.complete_executor import CompleteExecutor
executor = CompleteExecutor(Path.cwd())
```

**Validation**:
```bash
# Verify import works
python3 -c "from shannon.executor.complete_executor import CompleteExecutor; print('OK')"
```

#### T0.2: Test basic execution flow (60 minutes)
**Test**: Create simple test task
```bash
# Create test file
echo "# Test\nThis is a test file." > /tmp/test_exec_input.txt

# Run exec in dry-run mode
shannon exec "fix typo in /tmp/test_exec_input.txt" --dry-run

# Expected output:
# - Phase 1-6 headers shown
# - CompleteExecutor mentioned (not SimpleTaskExecutor)
# - Branch name generated
# - No errors
```

**Validation**: Dry-run completes without errors, shows all 6 phases

#### T0.3: Test actual execution (minimal task) (90 minutes)
**Test**: Run exec on real simple task in test directory
```bash
# Create test project
mkdir -p /tmp/shannon-exec-test
cd /tmp/shannon-exec-test
git init
echo "# Test Project" > README.md
git add README.md
git commit -m "Initial commit"

# Run exec with auto-commit
cd /Users/nick/Desktop/shannon-cli
shannon exec "add Python script that prints hello world to /tmp/shannon-exec-test" --auto-commit

# Expected:
# - Branch created (feat/*)
# - hello.py file created
# - Validation runs (at least Tier 1)
# - Commit created
# - No crashes
```

**Validation**:
```bash
cd /tmp/shannon-exec-test
git log --oneline  # Should show new commit
ls hello.py  # Should exist
git branch  # Should show feat/* branch
```

#### T0.4: Debug and fix issues (60 minutes)
**Expected Issues**:
- Import errors (fix imports)
- Async errors (fix await patterns)
- Path errors (fix Path() handling)
- Library discovery might fail (skip for now, test in Wave 1)

**Fix Strategy**: Focus on making ONE complete execution work, even if simplified

### Entry Gate:
- [ ] CompleteExecutor exists and imports successfully
- [ ] exec command code can be modified
- [ ] Test environment ready

### Exit Gate:
- [ ] exec command uses CompleteExecutor (verified in code)
- [ ] Dry-run mode works (shows all 6 phases)
- [ ] At least one simple execution completes (hello world task)
- [ ] At least one git commit created via exec
- [ ] No critical bugs preventing execution

**Deliverable**: Working shannon exec with CompleteExecutor. Foundation proven for deeper testing.

---

## WAVE 1: CLI Prompt Enhancement & Library Discovery (1 day, 8 hours)

**Repository**: shannon-cli
**Goal**: Validate prompt system and library discovery work correctly
**Entry Gate**: Wave 0 complete (CompleteExecutor working)
**Exit Gate**: Prompts build correctly, library discovery finds real packages

### Tasks (480 minutes total):

#### T1.1: Test PromptEnhancer for multiple project types (120 minutes)

**Test 1: React Project**
```bash
# Create mock React project
mkdir -p /tmp/test-react && cd /tmp/test-react
echo '{"dependencies": {"react": "^18.0.0", "next": "14.0.0"}}' > package.json

# Test prompt builder
python3 -c "
from shannon.executor import PromptEnhancer
from pathlib import Path

enhancer = PromptEnhancer()
prompts = enhancer.build_enhancements('add auth', Path('/tmp/test-react'))
print(f'Prompts length: {len(prompts)}')
print('LIBRARY_DISCOVERY' in prompts)
print('FUNCTIONAL_VALIDATION' in prompts)
print('GIT_WORKFLOW' in prompts)
print('React' in prompts or 'next-auth' in prompts)
"
```

**Expected**:
- Prompts length: 1500-3000 chars
- All 3 core sections present
- React-specific guidance included

**Test 2: Python FastAPI Project**
```bash
mkdir -p /tmp/test-python && cd /tmp/test-python
echo '[tool.poetry.dependencies]\nfastapi = "^0.104.0"' > pyproject.toml

# Test detection
python3 -c "
from shannon.executor import PromptEnhancer
from pathlib import Path

enhancer = PromptEnhancer()
project_type = enhancer._detect_project_type(Path('/tmp/test-python'))
print(f'Detected: {project_type}')
# Expected: 'python-fastapi' or 'python'
"
```

**Test 3: iOS Swift Project**
```bash
# If xcodeproj available, test iOS detection
# Otherwise, document as manual test
```

**Validation Criteria**:
- [ ] Detects React/Next.js projects correctly
- [ ] Detects Python/FastAPI projects correctly
- [ ] Prompts contain all 3 core sections
- [ ] Project-specific enhancements inject correctly
- [ ] Task-specific hints generate (auth → library recommendations)

#### T1.2: Test LibraryDiscoverer with real searches (180 minutes)

**Test 1: npm Search (React UI components)**
```bash
python3 << 'EOF'
import asyncio
from shannon.executor import LibraryDiscoverer
from pathlib import Path
import sys

async def test_npm():
    discoverer = LibraryDiscoverer(Path('/tmp/test-react'))
    print(f"Language: {discoverer.language}")
    print(f"Package manager: {discoverer._get_package_manager()}")

    # This will make REAL API calls
    libraries = await discoverer.discover_for_feature(
        "UI components",
        category="ui"
    )

    print(f"\nFound {len(libraries)} libraries:")
    for lib in libraries[:3]:
        print(f"  - {lib.name}: {lib.overall_score:.1f}/100")
        print(f"    {lib.why_recommended}")

    return len(libraries) > 0

result = asyncio.run(test_npm())
sys.exit(0 if result else 1)
EOF
```

**Expected Output**:
```
Language: javascript
Package manager: npm
Found 5 libraries:
  - react-native-paper: 92.0/100
    High stars (15k+), actively maintained, Material Design
  - @mui/material: 88.0/100
    Very high stars (85k+), actively maintained
  - chakra-ui: 85.0/100
    High stars (35k+), actively maintained
```

**Test 2: PyPI Search (Python background jobs)**
```bash
# Similar test for Python
python3 << 'EOF'
import asyncio
from shannon.executor import LibraryDiscoverer
from pathlib import Path

async def test_pypi():
    discoverer = LibraryDiscoverer(Path('/tmp/test-python'))
    libraries = await discoverer.discover_for_feature(
        "background jobs",
        category="data"
    )

    print(f"Found {len(libraries)} libraries:")
    for lib in libraries[:3]:
        print(f"  - {lib.name}: {lib.overall_score:.1f}/100")

    return len(libraries) > 0

asyncio.run(test_pypi())
EOF
```

**Expected**: Finds Arq, Celery, Dramatiq with quality scores

**Test 3: Cache Verification**
```bash
# Run same search twice, second should be instant
python3 << 'EOF'
import asyncio
import time
from shannon.executor import LibraryDiscoverer
from pathlib import Path

async def test_cache():
    discoverer = LibraryDiscoverer(Path('/tmp/test-react'))

    # First search (cold)
    start = time.time()
    libs1 = await discoverer.discover_for_feature("UI components", "ui")
    duration1 = time.time() - start

    # Second search (should hit cache)
    start = time.time()
    libs2 = await discoverer.discover_for_feature("UI components", "ui")
    duration2 = time.time() - start

    print(f"First search: {duration1:.1f}s ({len(libs1)} results)")
    print(f"Second search: {duration2:.1f}s ({len(libs2)} results)")
    print(f"Speedup: {duration1 / duration2:.1f}x")

    # Cache should be 10x+ faster
    return duration2 < duration1 / 5

asyncio.run(test_cache())
EOF
```

**Expected**: Second search <1s (cached), 10x+ speedup

**Validation Criteria**:
- [ ] npm search returns 3-5 React libraries with metadata
- [ ] PyPI search returns 3-5 Python libraries
- [ ] Quality scoring algorithm ranks correctly (verify against known libraries)
- [ ] Serena caching works (second search <1s)
- [ ] install_command generated correctly for each package manager

#### T1.3: Test system_prompt.append in SDK (120 minutes)

**Test**: Verify ClaudeAgentOptions.system_prompt.append works
```bash
# Create test script
cat > /tmp/test_prompt_injection.py << 'EOF'
import asyncio
from shannon.sdk import ShannonSDKClient
from claude_agent_sdk import ClaudeAgentOptions, AssistantMessage, TextBlock

async def test_append():
    client = ShannonSDKClient()

    # Create options with system_prompt.append
    custom_instructions = """
CRITICAL TEST INSTRUCTION:
When responding, start with the phrase "INSTRUCTION_RECEIVED"
"""

    options = ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": custom_instructions
        },
        max_turns=1
    )

    # Query with enhanced prompt
    messages = []
    async for msg in client._client.messages.create_stream(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": "Say hello"}],
        # Note: Need to verify SDK API for system_prompt injection
        max_tokens=100
    ):
        messages.append(msg)

    # Check if instruction was received
    response_text = ""
    for msg in messages:
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    response_text += block.text

    print(f"Response: {response_text}")
    return "INSTRUCTION_RECEIVED" in response_text

result = asyncio.run(test_append())
print(f"Test {'PASSED' if result else 'FAILED'}")
EOF

python3 /tmp/test_prompt_injection.py
```

**Expected**: Response contains "INSTRUCTION_RECEIVED" (proves append works)

**If Fails**: Research alternative injection methods, document workaround

**Validation Criteria**:
- [ ] system_prompt.append parameter exists in ClaudeAgentOptions
- [ ] Custom instructions delivered to agent
- [ ] Agent follows injected instructions
- [ ] Can inject 2000+ character prompts

#### T1.4: Integration test - Enhanced execution (60 minutes)

**Test**: Run exec with enhanced prompts on auth task
```bash
shannon exec "add authentication to /tmp/test-react" --dry-run --verbose

# Verify output shows:
# - Enhanced prompts mention next-auth, clerk, auth0
# - Library discovery recommendations
# - Validation strategy described
# - Git workflow explained
```

**Validation**: Verbose output shows enhanced prompts were used

### Entry Gate (checked before Wave 1):
- [x] Wave 0 complete (CompleteExecutor working)
- [ ] Test projects created (/tmp/test-react, /tmp/test-python)
- [ ] Python async works (no import errors)

### Exit Gate (checked after Wave 1):
- [ ] PromptEnhancer builds prompts for React/iOS/Python
- [ ] LibraryDiscoverer finds libraries from npm and PyPI
- [ ] Serena caching verified (<1s second search)
- [ ] system_prompt.append works OR alternative documented
- [ ] Enhanced prompts include library recommendations
- [ ] All tests pass (3 prompt tests + 3 library tests + 1 SDK test)

**Duration**: 8 hours (1 day)
**Deliverable**: Prompt enhancement and library discovery validated as production-ready

---

## WAVE 2: CLI Validation Orchestrator (1 day, 8 hours)

**Repository**: shannon-cli
**Goal**: Validate 3-tier validation system works across platforms
**Entry Gate**: Wave 1 complete (prompts and library discovery working)
**Exit Gate**: All 3 tiers execute correctly for Node.js, Python, and iOS

### Tasks (480 minutes total):

#### T2.1: Test auto-detection of test infrastructure (120 minutes)

**Test 1: Node.js Project**
```bash
# Create Node.js project with test scripts
mkdir -p /tmp/test-nodejs && cd /tmp/test-nodejs
cat > package.json << 'EOF'
{
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint .",
    "type-check": "tsc --noEmit",
    "dev": "node server.js"
  }
}
EOF

# Test auto-detection
python3 << 'PYEOF'
from shannon.executor import ValidationOrchestrator
from pathlib import Path

validator = ValidationOrchestrator(Path('/tmp/test-nodejs'))
config = validator.test_config

print(f"Project type: {config['project_type']}")
print(f"Build: {config['build_cmd']}")
print(f"Test: {config['test_cmd']}")
print(f"Lint: {config['lint_cmd']}")
print(f"Type check: {config['type_check_cmd']}")
print(f"Start: {config['start_cmd']}")

assert config['project_type'] == 'nodejs'
assert 'jest' in config['test_cmd']
print("✓ Node.js detection PASSED")
PYEOF
```

**Expected**: Detects all 5 commands from package.json scripts

**Test 2: Python Project**
```bash
mkdir -p /tmp/test-python-project && cd /tmp/test-python-project
cat > pyproject.toml << 'EOF'
[tool.poetry]
name = "test"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
EOF

# Test detection
python3 << 'PYEOF'
from shannon.executor import ValidationOrchestrator
from pathlib import Path

validator = ValidationOrchestrator(Path('/tmp/test-python-project'))
config = validator.test_config

print(f"Project type: {config['project_type']}")
assert config['project_type'] == 'python'
assert 'pytest' in config['test_cmd']
print("✓ Python detection PASSED")
PYEOF
```

**Test 3: Shannon CLI itself**
```bash
cd /Users/nick/Desktop/shannon-cli
python3 << 'PYEOF'
from shannon.executor import ValidationOrchestrator
from pathlib import Path

validator = ValidationOrchestrator(Path.cwd())
print(f"Detected: {validator.test_config}")
# Should detect Shannon CLI's own pytest configuration
PYEOF
```

**Validation Criteria**:
- [ ] Node.js projects: Detects build, test, lint, type-check, dev commands
- [ ] Python projects: Infers pytest, mypy, ruff
- [ ] Shannon CLI: Detects own test infrastructure

#### T2.2: Test Tier 1 validation (static) (120 minutes)

**Test on Shannon CLI itself**:
```bash
cd /Users/nick/Desktop/shannon-cli

# Run Tier 1 validation
python3 << 'PYEOF'
import asyncio
from shannon.executor import ValidationOrchestrator
from pathlib import Path

async def test_tier1():
    validator = ValidationOrchestrator(Path.cwd())

    # Mock changes object (or use real if available)
    class FakeChanges:
        pass

    result = await validator.validate_tier1(FakeChanges())

    print(f"Tier 1 Result: {result.passed}")
    print(f"Details: {result.details}")
    if result.failures:
        print(f"Failures: {result.failures}")

    return result.passed

passed = asyncio.run(test_tier1())
print(f"Tier 1: {'PASS' if passed else 'FAIL'}")
PYEOF
```

**Expected**: Tier 1 validation runs (might fail if code has issues, that's OK for now)

**Validation**: Code executes without crashes, returns TierResult object

#### T2.3: Test Tier 2 validation (unit tests) (120 minutes)

**Test**: Run Shannon CLI's own pytest suite via validator
```bash
python3 << 'PYEOF'
import asyncio
from shannon.executor import ValidationOrchestrator
from pathlib import Path

async def test_tier2():
    validator = ValidationOrchestrator(Path.cwd())

    class FakeChanges:
        pass

    result = await validator.validate_tier2(FakeChanges())

    print(f"Tier 2 Result: {result.passed}")
    print(f"Test output preview: {str(result.details)[:200]}")

    return result

asyncio.run(test_tier2())
PYEOF
```

**Expected**: pytest runs (even if some tests fail), output captured

**Validation**: Tier 2 executes, captures test output

#### T2.4: Test Tier 3 validation (functional) (180 minutes)

**This is the CRITICAL tier** - validates code actually works from user perspective.

**Test 1: Mock Node.js functional validation**
```bash
# Create simple Express server
mkdir -p /tmp/test-nodejs-server && cd /tmp/test-nodejs-server
npm init -y
npm install express

cat > server.js << 'EOF'
const express = require('express');
const app = express();
app.get('/health', (req, res) => res.json({ status: 'ok' }));
app.listen(3000, () => console.log('Server started'));
EOF

# Test Tier 3
python3 << 'PYEOF'
import asyncio
from shannon.executor.validator import ValidationOrchestrator
from pathlib import Path

async def test_tier3_nodejs():
    validator = ValidationOrchestrator(Path('/tmp/test-nodejs-server'))

    # Define functional criteria
    criteria = ["Server starts on port 3000", "Health endpoint returns 200"]

    result = await validator.validate_tier3(None, criteria)

    print(f"Tier 3 Result: {result.passed}")
    print(f"Details: {result.details}")

    return result

asyncio.run(test_tier3_nodejs())
PYEOF
```

**Expected**:
- Server starts in background
- Health check passes
- Validation returns success

**Test 2: Python functional validation**
```bash
# Create simple FastAPI app
mkdir -p /tmp/test-fastapi && cd /tmp/test-fastapi
pip install fastapi uvicorn

cat > main.py << 'EOF'
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
EOF

# Test Tier 3
python3 << 'PYEOF'
import asyncio
from shannon.executor.validator import ValidationOrchestrator
from pathlib import Path

async def test_tier3_python():
    validator = ValidationOrchestrator(Path('/tmp/test-fastapi'))
    result = await validator.validate_tier3(None, ["Health endpoint OK"])
    print(f"Result: {result.passed}")
    return result

asyncio.run(test_tier3_python())
PYEOF
```

**Validation Criteria**:
- [ ] Tier 3 can start Node.js dev servers
- [ ] Tier 3 can start Python servers (uvicorn)
- [ ] Health checks execute and verify
- [ ] Background processes managed correctly (cleanup after test)

### Entry Gate:
- [x] Wave 1 complete
- [ ] Test projects created for validation
- [ ] Network available (for library searches)

### Exit Gate:
- [ ] All 3 prompt tests pass (React, Python, iOS detection)
- [ ] npm search returns 3+ libraries
- [ ] PyPI search returns 3+ libraries
- [ ] Caching verified (10x+ speedup)
- [ ] Tier 1 validation executes (build/lint/types)
- [ ] Tier 2 validation executes (test suite)
- [ ] Tier 3 validation executes (functional tests)
- [ ] Auto-detection works for Node.js and Python

**Duration**: 8 hours
**Deliverable**: Complete validation system proven across all 3 tiers

---

## WAVE 3: CLI Git Automation (1 day, 8 hours)

**Repository**: shannon-cli
**Goal**: Validate git automation creates proper commits and rollback works
**Entry Gate**: Waves 1-2 complete
**Exit Gate**: Can create branches, commit validated changes, rollback failures

### Tasks (480 minutes total):

#### T3.1: Test branch creation (60 minutes)

**Test**: Generate semantic branch names
```bash
python3 << 'EOF'
from shannon.executor import GitManager
from pathlib import Path

git_mgr = GitManager(Path.cwd())

tests = [
    ("fix the login bug", "fix/login-bug"),
    ("add authentication feature", "feat/authentication-feature"),
    ("optimize database queries", "perf/database-queries"),
    ("refactor code structure", "refactor/code-structure"),
]

for task, expected_prefix in tests:
    branch = git_mgr._generate_branch_name(task)
    print(f"{task[:30]:30} → {branch}")
    assert branch.startswith(expected_prefix.split('/')[0])

print("✓ Branch naming PASSED")
EOF
```

**Validation**: All branch names use correct semantic prefixes

#### T3.2: Test commit message generation (120 minutes)

**Test**: Generate structured commit messages
```bash
python3 << 'EOF'
from shannon.executor import GitManager
from shannon.executor.models import ValidationResult, TierResult
from pathlib import Path

git_mgr = GitManager(Path.cwd())

# Mock validation result
validation = ValidationResult(
    tier1_passed=True,
    tier2_passed=True,
    tier3_passed=True,
    tier1_details={"build": "PASS"},
    tier2_details={"tests": "12/12 PASS"},
    tier3_details={"functional": "Login works in browser"},
    failures=[],
    duration_seconds=45.2
)

message = git_mgr._generate_commit_message(
    "Add login form with validation",
    validation
)

print("Generated commit message:")
print(message)
print()

# Verify structure
assert "VALIDATION:" in message
assert "Build: PASS" in message
assert "Tests: PASS" in message
assert "Functional: PASS" in message
print("✓ Commit message structure PASSED")
EOF
```

**Expected Output**:
```
feat: Add login form with validation

VALIDATION:
- Build: PASS
- Tests: PASS
- Functional: PASS
```

#### T3.3: Test atomic commit (actual git operations) (120 minutes)

**Test**: Create real commit in test repo
```bash
# Create test repo
mkdir -p /tmp/test-git && cd /tmp/test-git
git init
echo "# Test" > README.md
git add README.md
git commit -m "Initial commit"

# Create changes
echo "print('hello')" > test.py

# Test GitManager commit
python3 << 'PYEOF'
import asyncio
from shannon.executor import GitManager
from shannon.executor.models import ValidationResult, TierResult
from pathlib import Path

async def test_commit():
    git_mgr = GitManager(Path('/tmp/test-git'))

    # Verify clean state
    is_clean = await git_mgr.ensure_clean_state()
    print(f"Clean state: {is_clean}")  # Should be False (test.py untracked)

    # Create branch
    branch = await git_mgr.create_feature_branch("test commit")
    print(f"Created branch: {branch}")

    # Stage file
    await git_mgr._run_git("add test.py")

    # Create validation result
    validation = ValidationResult(
        tier1_passed=True,
        tier2_passed=True,
        tier3_passed=True,
        tier1_details={},
        tier2_details={},
        tier3_details={},
        failures=[],
        duration_seconds=1.0
    )

    # Commit
    commit = await git_mgr.commit_validated_changes(
        files=["test.py"],
        step_description="Add test script",
        validation_result=validation
    )

    print(f"Created commit: {commit.hash[:8]}")
    print(f"Message: {commit.message.split(chr(10))[0]}")

    return commit

asyncio.run(test_commit())
PYEOF

# Verify in git
cd /tmp/test-git
git log --oneline -1  # Should show new commit
git show --stat HEAD  # Should show test.py added
```

**Validation**: Commit appears in git log, contains test.py, message is structured

#### T3.4: Test rollback functionality (60 minutes)

**Test**: Verify git reset --hard works
```bash
cd /tmp/test-git

# Make uncommitted changes
echo "print('broken')" >> test.py
git diff  # Should show changes

# Test rollback
python3 << 'PYEOF'
import asyncio
from shannon.executor import GitManager
from pathlib import Path

async def test_rollback():
    git_mgr = GitManager(Path('/tmp/test-git'))

    # Rollback
    success = await git_mgr.rollback_to_last_commit()
    print(f"Rollback success: {success}")

    return success

asyncio.run(test_rollback())
PYEOF

# Verify changes reverted
git diff  # Should show nothing
cat test.py  # Should NOT have 'broken' line
```

**Validation**: Uncommitted changes removed, working directory clean

#### T3.5: Test complete git workflow (180 minutes)

**Test**: Full exec with git automation
```bash
cd /tmp/test-nodejs

# Ensure clean state
git init
echo "# Project" > README.md
git add README.md
git commit -m "Initial"

# Run exec that creates commit
cd /Users/nick/Desktop/shannon-cli
shannon exec "add package.json with express dependency to /tmp/test-nodejs" --auto-commit

# Verify:
cd /tmp/test-nodejs
git log --oneline  # Should have new commit
git branch  # Should show feat/* branch
cat package.json  # Should exist with express
```

**Expected**:
- Branch created (feat/package-json-express)
- package.json created
- Validation ran
- Commit created with structured message
- Can see validation results in commit message

**Validation**: Complete git workflow produces clean history with validated commits

### Entry Gate:
- [x] Waves 1-2 complete
- [ ] Test git repos created
- [ ] Git available (git --version)

### Exit Gate:
- [ ] Auto-detection works for Node.js, Python, Shannon CLI
- [ ] Tier 1 executes (build/lint/type commands)
- [ ] Tier 2 executes (test suite)
- [ ] Tier 3 executes (start servers, health checks)
- [ ] Branch creation works with semantic naming
- [ ] Commit creation works with structured messages
- [ ] Rollback works (git reset --hard verified)
- [ ] Full exec creates at least 1 real commit
- [ ] Git history is clean (only validated commits)

**Duration**: 8 hours
**Deliverable**: Git automation fully validated, atomic commits proven

---

## WAVE 4: CLI Complete Integration Testing (1 day, 8 hours)

**Repository**: shannon-cli
**Goal**: Test end-to-end workflows with CompleteExecutor
**Entry Gate**: Waves 0-3 complete (all modules validated)
**Exit Gate**: Complex multi-step execution works with iteration

### Tasks (480 minutes total):

#### T4.1: Test simple task E2E (60 minutes)

**Test**: Complete workflow for trivial task
```bash
mkdir -p /tmp/exec-test-simple && cd /tmp/exec-test-simple
git init
git commit --allow-empty -m "Initial"

cd /Users/nick/Desktop/shannon-cli
shannon exec "create README.md with project description in /tmp/exec-test-simple"

# Verify ALL components worked:
cd /tmp/exec-test-simple
git log --oneline -5  # Check commits
git branch  # Check branch
cat README.md  # Check file created
```

**Validation**:
- [ ] Task completes successfully
- [ ] README.md created
- [ ] Validation ran (all 3 tiers OR appropriate subset)
- [ ] Commit created
- [ ] Duration <2 minutes

#### T4.2: Test library-heavy task (120 minutes)

**Test**: Task that SHOULD discover libraries
```bash
mkdir -p /tmp/exec-test-libraries && cd /tmp/exec-test-libraries
npm init -y
git init
git add package.json
git commit -m "Initial"

cd /Users/nick/Desktop/shannon-cli
shannon exec "add form validation with react-hook-form and zod" --verbose

# Expected:
# - Library discovery mentions react-hook-form, zod
# - npm install commands run
# - Validation includes dependency checks
# - Commits show libraries added
```

**Validation**:
- [ ] Library discovery finds react-hook-form and zod
- [ ] Recommendations shown in output
- [ ] Libraries actually installed (check package.json)
- [ ] Doesn't build custom validation (uses libraries)

#### T4.3: Test multi-step task (180 minutes)

**Test**: Task requiring multiple steps
```bash
mkdir -p /tmp/exec-test-multistep && cd /tmp/exec-test-multistep
npx create-next-app . --typescript --tailwind --app --no-src-dir --import-alias="@/*"
git add .
git commit -m "Initial Next.js"

cd /Users/nick/Desktop/shannon-cli
shannon exec "add authentication with next-auth including login page and protected routes"

# Expected:
# - Multiple steps (install, configure, login page, protected routes, test)
# - Multiple commits (one per step if atomic commit working)
# - Each step validated independently
# - Iteration if any step fails
```

**Validation**:
- [ ] Plan shows multiple steps
- [ ] Multiple commits created (one per validated step)
- [ ] Each commit has validation results
- [ ] Authentication actually works (can test login)

#### T4.4: Test iteration after failure (120 minutes)

**Test**: Intentionally cause failure, verify retry
```bash
# Create task that will likely fail first attempt
shannon exec "add non-existent-library-xyz to test project"

# Expected:
# - Attempt 1: Fails (library not found)
# - Research triggered (search for alternative)
# - Attempt 2: Success with alternative OR
# - After 3 attempts: Graceful failure with clear error
```

**Validation**:
- [ ] Validation failure detected
- [ ] Rollback executed (git reset --hard)
- [ ] Research integration attempted (if implemented)
- [ ] Retry with alternative approach
- [ ] OR graceful failure after max attempts

### Entry Gate:
- [x] Waves 0-3 complete
- [ ] All module tests passed
- [ ] Test projects ready

### Exit Gate:
- [ ] Simple task: Completes in <2 min, creates 1 commit
- [ ] Library task: Discovers and uses libraries, doesn't reinvent
- [ ] Multi-step task: Creates multiple commits, each validated
- [ ] Failure handling: Retries OR fails gracefully with clear error
- [ ] CompleteExecutor proves superior to SimpleTaskExecutor
- [ ] CLI standalone mode production-ready

**Duration**: 8 hours
**Deliverable**: CLI proven capable of autonomous execution. Standalone mode complete.

---

## WAVE 5: Framework Exec Skill Creation (2 days, 16 hours)

**Repository**: shannon-framework
**Goal**: Create /shannon:exec skill for Claude Code UI users
**Entry Gate**: CLI Waves 0-4 complete, Framework repo accessible
**Exit Gate**: /shannon:exec works in Claude Code, produces commits

### Tasks (960 minutes total):

#### T5.1: Design exec skill specification (240 minutes - 4 hours)

**Research existing Shannon skills**:
```bash
cd /Users/nick/Desktop/shannon-framework

# Read wave-orchestration skill as template
cat skills/wave-orchestration/SKILL.md | head -100

# Read spec-analysis skill structure
cat skills/spec-analysis/SKILL.md | head -100

# Read task-automation skill (closest to exec)
cat skills/task-automation/SKILL.md | head -100
```

**Design exec skill structure**:
```markdown
# Exec Skill Specification (SKILL.md)

## When to Use
- User wants autonomous task execution
- Library discovery needed
- Functional validation required
- Git automation desired

## Input
- task (string): Natural language task description
- options (optional):
  - dry_run (bool): Plan only, don't execute
  - interactive (bool): Confirm before each step
  - max_iterations (int): Retry attempts per step

## Workflow

### Phase 1: Context Preparation
- Invoke: /shannon:prime
- Purpose: Load project context, discover skills
- Output: Context ready

### Phase 2: Library Discovery
- Call: shannon discover-libs [extracted feature]
- Parse: JSON library recommendations
- Cache: Store in Serena MCP
- Output: Top 5 libraries ranked

### Phase 3: Task Analysis
- Invoke: /shannon:analyze [task]
- Parse: Complexity score, domains
- Strategy: Determine execution approach
- Output: Analysis complete

### Phase 4: Execution Planning
- Use: sequential-thinking MCP
- Create: ExecutionPlan with steps
- Include: Libraries, validation criteria
- Output: Step-by-step plan

### Phase 5: Execution Loop
FOR EACH step:
  - Convert to WaveTask format
  - Invoke: /shannon:wave with single-task wave
  - Call: shannon validate --tier all
  - Parse: ValidationResult
  - IF all tiers pass:
    - Call: shannon git-commit
    - Continue to next step
  - ELSE:
    - Research solution (firecrawl)
    - Replan step
    - Rollback: shannon git-rollback
    - Retry (max 3x)

### Phase 6: Execution Report
- Summarize: Steps, commits, duration, cost
- Report: Libraries used, validations passed
- Output: ExecutionReport

## Integration Points
- /shannon:prime (Phase 1)
- /shannon:analyze (Phase 3)
- /shannon:wave (Phase 5, per step)
- shannon discover-libs (Phase 2)
- shannon validate (Phase 5)
- shannon git-commit (Phase 5)
- shannon git-rollback (Phase 5 on failure)

## Output
- ExecutionReport object
- Git branch with validated commits
- Saved to Serena MCP

## Success Criteria
- All 6 phases complete
- Commits created only for validated changes
- Libraries used instead of custom implementation
- Task actually works (functional validation)

## Common Pitfalls
- Skipping functional validation
- Building custom code when library exists
- Committing unvalidated changes
- Not using iteration on failure

## Related Skills
- spec-analysis (invoked in Phase 3)
- wave-orchestration (invoked in Phase 5)
- context-preservation (automatic checkpoints)
- functional-testing (Tier 3 validation philosophy)
```

**Document**:
- Create skills/exec/SKILL_DESIGN.md with full specification
- Est lines: 600-800

#### T5.2: Create protocol reference documents (360 minutes - 6 hours)

**File 1**: `skills/exec/references/LIBRARY_DISCOVERY_PROTOCOL.md` (200 lines)
```markdown
# Library Discovery Protocol

## Philosophy
ALWAYS search for existing open-source libraries before building custom solutions.

## Process
1. Identify feature needed
2. Search package registry (npm, PyPI, CocoaPods, Maven, crates.io)
3. Evaluate top 3-5 options:
   - GitHub stars (prefer >1000)
   - Last update (prefer <6 months)
   - Maintenance status
   - Compatibility
   - License (MIT/Apache/BSD)
   - Documentation quality
4. SELECT best option, document why
5. Add to project dependencies
6. USE in implementation

## Common Libraries by Category
[Copy from V3.5 spec lines 182-214]

## Execution
Call: shannon discover-libs "[feature]" --category [ui|auth|networking|data|forms]
Parse: JSON response with ranked recommendations
```

**File 2**: `skills/exec/references/FUNCTIONAL_VALIDATION_PROTOCOL.md` (200 lines)
```markdown
# Functional Validation Protocol

## 3-Tier Validation

### Tier 1: Static (~10s)
- Build/compile succeeds
- Type checking passes
- Linter passes
- No syntax errors

### Tier 2: Unit/Integration (~1-5min)
- Test suite runs
- All existing tests pass
- New tests pass (if added)
- Coverage maintained

### Tier 3: Functional (~2-10min)
- **Run the actual application**
- **Test from USER PERSPECTIVE**
- Verify: "Can a user actually use this feature?"

## Platform-Specific Tier 3

### Node.js/React
1. npm run dev (start server)
2. Wait for http://localhost:3000
3. Test feature in browser
4. Verify expected behavior

### Python/FastAPI
1. uvicorn main:app (start server)
2. curl http://localhost:8000/endpoint
3. Verify response (200 OK, correct data)
4. Test error cases (400, 401)

### iOS/Swift
1. xcrun simctl boot "iPhone 16"
2. xcodebuild test -scheme MyApp
3. Verify UI tests pass
4. Check element visible/tappable

## Execution
Call: shannon validate --tier [1|2|3|all]
Parse: ValidationResult JSON
```

**File 3**: `skills/exec/references/GIT_WORKFLOW_PROTOCOL.md` (200 lines)
```markdown
# Git Workflow Protocol

## Atomic Commits per Validated Change

### Pre-Execution
1. Verify: git status is clean
2. Verify: Not on main/master
3. Create: git checkout -b [type]/[description]

### Per Step
1. Make changes (modify files)
2. Tier 1: Build, lint, types → PASS or rollback
3. Tier 2: Tests → PASS or rollback
4. Tier 3: Functional → PASS or rollback
5. All pass → git add + git commit

### Commit Message Format
<type>: <summary>

VALIDATION:
  - Build: PASS
  - Tests: X/X PASS
  - Functional: [description]

### Rollback on Failure
git reset --hard HEAD
git clean -fd

### Execution
Branch: shannon git-branch "[task]"
Commit: shannon git-commit --step "[desc]" --validation [json]
Rollback: shannon git-rollback
```

#### T5.3: Write exec skill SKILL.md (360 minutes - 6 hours)

**File**: `skills/exec/SKILL.md`

**Structure** (following Shannon skill patterns):
1. Frontmatter (name, description, when to use)
2. When to Use section
3. Input specification
4. Complete workflow (6 phases)
5. Integration points (CLI commands, Shannon skills)
6. Helper functions (executeStepViaWave, validateStep, etc.)
7. Output specification
8. Success criteria
9. Common pitfalls
10. Related skills and commands
11. Examples (3-4 realistic scenarios)

**Estimated**: 600-800 lines (similar to wave-orchestration.md complexity)

**Content**:
- Copy 6-phase workflow from design
- Add code examples for each phase
- Document CLI integration points
- Include error handling
- Add retry logic specification

#### T5.4: Create exec command (60 minutes - 1 hour)

**File**: `commands/exec.md`

**Content** (following Shannon command pattern):
```markdown
---
name: exec
description: Autonomous task execution with library discovery and validation
tags: [execution, automation, libraries, validation, git]
---

# Shannon Exec: Autonomous Task Execution

Execute tasks autonomously with automatic library discovery, 3-tier validation, and atomic git commits.

## Usage

```
/shannon:exec "task description"
/shannon:exec "task" --dry-run
/shannon:exec "task" --interactive
```

## Workflow

@skill exec
  task: {user_provided_task}
  options:
    dry_run: {--dry-run flag}
    interactive: {--interactive flag}

## Output

- ExecutionReport with commits created
- Git branch ready for PR
- Libraries documented
- Validation results

## Examples

### Simple Task
```
/shannon:exec "fix typo in README.md"
```

### Complex Task
```
/shannon:exec "add authentication to React app"
```

### Planning Mode
```
/shannon:exec "build e-commerce platform" --dry-run
```

## Related
- /shannon:wave (execution engine)
- /shannon:prime (context preparation)
- /shannon:analyze (task analysis)
```

**Estimated**: 80-120 lines

#### T5.5: Update Framework metadata (30 minutes)

**Files to modify**:

1. `.claude-plugin/plugin.json`:
```json
{
  "version": "5.1.0"  // Bump from 5.0.0
}
```

2. `README.md`:
Add to commands section:
```markdown
### Execution
- **/shannon:exec** - Autonomous task execution with libraries, validation, commits
```

3. `CHANGELOG.md`:
```markdown
## [5.1.0] - 2025-11-[XX]

### Added
- **/shannon:exec** command for autonomous task execution
- exec skill with 6-phase orchestration
- Integration with Shannon CLI Python modules
- Library discovery, 3-tier validation, git automation
```

#### T5.6: Test exec skill in Claude Code (180 minutes - 3 hours)

**Prerequisites**:
```bash
# Ensure Shannon CLI installed
cd /Users/nick/Desktop/shannon-cli
pip install -e .

# Ensure Shannon Framework updated
cd /Users/nick/Desktop/shannon-framework
# Verify changes committed
git status

# Reload plugin in Claude Code
/plugin uninstall shannon@shannon-framework
/plugin marketplace add /Users/nick/Desktop/shannon-framework
/plugin install shannon@shannon-framework
```

**Test 1: Dry-run mode**
```
/shannon:exec "add dark mode toggle to React app" --dry-run
```

**Expected**:
- Phase 1: Context preparation (30-60s)
- Phase 2: Library discovery (finds theme libraries)
- Phase 3: Analysis (complexity score)
- Phase 4: Planning (execution plan with steps)
- Phase 5: Shows what WOULD execute (but doesn't)
- Phase 6: Report (no commits, planning only)

**Test 2: Simple execution**
```
# Create test project in Claude Code workspace
mkdir test-exec-framework
cd test-exec-framework
git init
git commit --allow-empty -m "Initial"

/shannon:exec "create index.html with hello world"
```

**Expected**:
- All 6 phases execute
- index.html created
- Validation runs
- Commit created
- Branch created
- Duration: 2-5 minutes

**Test 3: Verify CLI integration**
- Phase 2 should call `shannon discover-libs` and show output
- Phase 5 should call `shannon validate` and show results
- Phase 5 should call `shannon git-commit` and confirm

**Validation Criteria**:
- [ ] exec skill loads successfully
- [ ] All 6 phases execute
- [ ] Can invoke /shannon:prime, /shannon:analyze, /shannon:wave
- [ ] Can call shannon CLI commands via run_terminal_cmd
- [ ] Creates actual git commits
- [ ] Report generated and displayed

### Entry Gate:
- [x] CLI Waves 0-4 complete (standalone mode working)
- [ ] Framework repo clean (git status)
- [ ] Can create skills/ directory
- [ ] Can modify commands/

### Exit Gate:
- [ ] skills/exec/SKILL.md created (600-800 lines)
- [ ] skills/exec/references/ created (3 files, 600 lines)
- [ ] commands/exec.md created (80-120 lines)
- [ ] plugin.json version = 5.1.0
- [ ] README and CHANGELOG updated
- [ ] /shannon:exec loads in Claude Code
- [ ] Dry-run test passes
- [ ] Simple execution test passes
- [ ] CLI commands callable from skill
- [ ] At least 1 commit created via Framework exec

**Duration**: 16 hours (2 days)
**Deliverable**: Framework exec skill operational. Claude Code users can use /shannon:exec.

---

## WAVE 6: CLI Framework Integration (1 day, 8 hours)

**Repository**: shannon-cli
**Goal**: Add --framework flag for CLI to use Framework skill
**Entry Gate**: Wave 5 complete (Framework exec skill working)
**Exit Gate**: `shannon exec --framework` works

### Tasks (480 minutes total):

#### T6.1: Add --framework flag to exec command (60 minutes)

**File**: `src/shannon/cli/commands.py`
**Modification**: exec command function signature

Add flag:
```python
@click.option('--framework', is_flag=True, help='Use Shannon Framework exec skill (requires Framework installed)')
def exec(
    task: str,
    # ... existing parameters ...
    framework: bool,  # NEW
    verbose: bool
) -> None:
```

#### T6.2: Implement framework mode handler (180 minutes - 3 hours)

**Add to exec command**:
```python
async def run_exec() -> None:
    # ... existing setup ...

    if framework:
        # Framework mode: Invoke /shannon:exec skill
        ui.console.print("[cyan]Using Shannon Framework exec skill...[/cyan]")

        # Verify Framework installed
        # (Add shannon check-framework command first)
        framework_check = await check_framework_installed()
        if not framework_check.success:
            ui.error("Shannon Framework V5.1.0+ required for --framework mode")
            ui.console.print("Install: /plugin install shannon@shannon-framework")
            sys.exit(1)

        # Invoke Framework skill
        client = ShannonSDKClient()
        async for message in client.invoke_skill(
            'exec',
            task,
            options={'dry_run': dry_run, 'interactive': interactive}
        ):
            # Stream messages to console
            ui.display_message(message)

        ui.success("Framework execution complete")
    else:
        # Standalone mode: Use CompleteExecutor (existing code)
        # ... existing Python execution ...
```

#### T6.3: Create shannon check-framework command (60 minutes)

**File**: `src/shannon/cli/commands.py`

**New command**:
```python
@cli.command()
def check_framework() -> None:
    """Verify Shannon Framework installation and version."""
    # Check if Framework plugin installed
    # Verify version >= 5.1.0
    # Report status
```

**Implementation**:
- Check Claude Code plugins directory
- Parse plugin.json version
- Verify exec skill exists
- Return structured result

#### T6.4: Test framework mode (180 minutes - 3 hours)

**Test 1: Framework detection**
```bash
shannon check-framework

# Expected output:
# ✓ Shannon Framework found
#   Version: 5.1.0
#   Location: ~/.claude/plugins/shannon
#   Exec skill: Available
# Status: READY
```

**Test 2: Framework exec invocation**
```bash
cd /tmp/test-react
shannon exec "add button component" --framework

# Expected:
# - Shows "Using Shannon Framework exec skill..."
# - Phases 1-6 execute via Framework
# - Calls shannon discover-libs (visible in output)
# - Calls shannon validate (visible in output)
# - Creates commit via shannon git-commit
# - Same outcome as standalone mode
```

**Test 3: Compare modes**
```bash
# Test same task in both modes
cd /tmp/test-comparison
git init && git commit --allow-empty -m "Initial"

# Standalone mode
git checkout -b test-standalone
shannon exec "add config.json file"
git log --oneline -1 > standalone-result.txt

# Framework mode
git checkout master
git checkout -b test-framework
shannon exec "add config.json file" --framework
git log --oneline -1 > framework-result.txt

# Compare outcomes
diff standalone-result.txt framework-result.txt
# Should be similar commit messages, same files created
```

**Validation**: Both modes produce equivalent results

### Entry Gate:
- [x] Wave 5 complete (Framework skill working)
- [ ] Framework installed in Claude Code
- [ ] CLI can invoke SDK

### Exit Gate:
- [ ] --framework flag added to exec command
- [ ] shannon check-framework command works
- [ ] Framework mode detects missing Framework gracefully
- [ ] Framework mode invokes /shannon:exec successfully
- [ ] Standalone mode still works (no regression)
- [ ] Both modes tested on same task
- [ ] Outcomes are equivalent (same commits, same quality)

**Duration**: 8 hours
**Deliverable**: Dual-mode CLI complete. Users can choose standalone or Framework.

---

## WAVE 7: Comprehensive Testing Matrix (1 day, 8 hours)

**Repositories**: BOTH (shannon-cli + shannon-framework)
**Goal**: Validate parity across 15 test scenarios
**Entry Gate**: Waves 0-6 complete
**Exit Gate**: All 15 tests pass (5 scenarios × 3 modes)

### Testing Matrix (300 minutes - 5 hours)

**5 Test Scenarios**:
1. **Simple**: Fix typo in README
2. **Library-Heavy**: Add form validation (should find react-hook-form + zod)
3. **Multi-Step**: Add authentication (install + configure + UI + test)
4. **Platform-Specific**: iOS SwiftUI button (should use built-in components)
5. **Failure-Retry**: Intentional failure → research → retry → success

**3 Execution Modes**:
- Mode A: CLI Standalone (`shannon exec`)
- Mode B: Framework Skill (`/shannon:exec` in Claude Code)
- Mode C: CLI Framework Mode (`shannon exec --framework`)

**15 Tests Total**: Each scenario × each mode

#### Test Execution Strategy (60 min per mode × 5 scenarios × 3 modes = 900 min)

**Optimize**: Run in parallel batches
- Batch 1: All Mode A tests (5 tests, 300 min)
- Batch 2: All Mode B tests (5 tests, 300 min)
- Batch 3: All Mode C tests (5 tests, 300 min)

**Actual**: 5 hours with parallelization via test runner

#### T7.1: Create test runner script (60 minutes)

**File**: `tests/functional/test_exec_parity.sh`

```bash
#!/bin/bash
# Shannon V3.5 Exec Parity Test Suite

SCENARIOS=(
  "S1:fix-typo:Fix typo in README.md"
  "S2:form-validation:Add form validation to React app"
  "S3:authentication:Add authentication with next-auth"
  "S4:ios-button:Add button to SwiftUI view"
  "S5:failure-retry:Add non-existent library (test retry)"
)

MODES=("standalone" "framework" "cli-framework")

# Run all combinations
for scenario in "${SCENARIOS[@]}"; do
  for mode in "${MODES[@]}"; do
    run_test "$scenario" "$mode"
    validate_outcome "$scenario" "$mode"
  done
done

generate_report
```

#### T7.2: Execute test matrix (300 minutes - 5 hours)

Run the test suite, collect results, analyze failures

#### T7.3: Fix discovered issues (120 minutes - 2 hours)

Allocate time for debugging integration issues found during testing

### Entry Gate:
- [x] Waves 0-6 complete
- [ ] Test runner script created
- [ ] Test projects ready
- [ ] Both repos committed (clean state for testing)

### Exit Gate:
- [ ] All 15 tests executed
- [ ] Pass rate ≥80% (12/15 tests pass)
- [ ] Known failures documented
- [ ] Critical bugs fixed
- [ ] Test report generated

**Duration**: 8 hours
**Deliverable**: Parity proven across modes. Both implementations validated.

---

## WAVE 8: Documentation & Release (1 day, 8 hours)

**Repositories**: BOTH
**Goal**: Complete documentation, coordinated release
**Entry Gate**: Waves 0-7 complete, all tests passing
**Exit Gate**: Both repos documented and released

### Tasks (480 minutes total):

#### T8.1: Shannon CLI Documentation (180 minutes - 3 hours)

**File 1**: `docs/SHANNON_V3.5_USER_GUIDE.md` (400 lines)
```markdown
# Shannon V3.5 User Guide

## Overview
Shannon V3.5 adds autonomous task execution...

## Installation
pip install shannon-cli

## Basic Usage
shannon exec "task description"

## Modes
- Standalone: Fast Python execution
- Framework: Orchestrated via Shannon Framework skill

## Features
- Library discovery
- 3-tier validation
- Atomic git commits
- Iteration on failure

## Examples
[5-6 detailed examples]

## Troubleshooting
[Common issues and solutions]
```

**File 2**: `examples/exec_react_auth.md` (100 lines)
- Complete transcript of adding next-auth to Next.js
- Show library discovery finding next-auth
- Show validation tiers
- Show commits created

**File 3**: `examples/exec_ios_feature.md` (100 lines)
- Add image picker to SwiftUI app
- Show built-in PhotosUI discovered
- Show simulator validation

**File 4**: Update `README.md` (60 lines addition)
```markdown
### Autonomous Execution (V3.5)

**shannon exec** - Execute tasks autonomously with validation

Execute natural language tasks with automatic library discovery,
3-tier functional validation, and atomic git commits.

```bash
shannon exec "add authentication to React app"
shannon exec "optimize database query" --dry-run
shannon exec "add dark mode toggle" --framework
```

Features:
- 🔍 Library discovery (npm, PyPI, CocoaPods, Maven, crates.io)
- ✅ 3-tier validation (build + tests + functional)
- 🔄 Iteration with research on failure
- 📝 Atomic git commits (only validated changes)
- 🎯 Dual mode (standalone Python or Framework skill)
```

**File 5**: Update `CHANGELOG.md`
```markdown
## [3.5.0] - 2025-11-[XX]

### Added
- **shannon exec** command for autonomous task execution
- Library discovery across npm, PyPI, CocoaPods, Maven, crates.io
- 3-tier validation (static, tests, functional)
- Git automation with atomic commits
- Enhanced system prompts (library-first, validation-focused)
- Iteration with research on validation failure
- Dual-mode execution (standalone or --framework)
- Integration with Shannon Framework V5.1.0 exec skill

### Components
- LibraryDiscoverer (555 lines)
- ValidationOrchestrator (360 lines)
- GitManager (314 lines)
- PromptEnhancer (295 lines)
- CompleteExecutor (313 lines)

See docs/SHANNON_V3.5_USER_GUIDE.md for details.
```

**File 6**: Bump version in `pyproject.toml`
```toml
version = "3.5.0"  # From 3.0.0
```

#### T8.2: Shannon Framework Documentation (120 minutes - 2 hours)

**File 1**: `skills/exec/README.md` (200 lines)
```markdown
# Exec Skill

Autonomous task execution with library discovery and validation.

## Overview
The exec skill orchestrates Shannon's capabilities...

## Integration
Calls Shannon CLI Python modules:
- shannon discover-libs
- shannon validate
- shannon git-commit

## Usage
/shannon:exec "task description"

## See Also
- SKILL.md (complete workflow)
- references/ (protocols)
```

**File 2**: Update Framework `README.md`
```markdown
### Execution
- **/shannon:exec** - Autonomous task execution (V5.1+)
  ```
  /shannon:exec "add authentication to React app"
  ```
  - Library discovery
  - 3-tier validation
  - Atomic git commits
  - Requires Shannon CLI installed
```

**File 3**: Update Framework `CHANGELOG.md`
```markdown
## [5.1.0] - 2025-11-[XX]

### Added
- **/shannon:exec** command and skill
- Autonomous task execution capability
- Integration with Shannon CLI executor modules
- Protocol references (library discovery, validation, git workflow)

Requires Shannon CLI V3.5.0+ for full functionality.
```

#### T8.3: Create cross-repository integration guide (120 minutes - 2 hours)

**File**: `docs/SHANNON_CLI_FRAMEWORK_INTEGRATION.md` (both repos)

```markdown
# Shannon CLI + Framework Integration Guide

## Overview
Shannon V3.5 (CLI) and V5.1 (Framework) work together...

## Architecture
[Diagram showing CLI ↔ Framework interaction]

## Installation
```bash
# Install CLI
pip install shannon-cli

# Install Framework plugin
/plugin install shannon@shannon-framework
```

## Usage Modes

### Mode 1: CLI Standalone
Fast Python execution, machine-readable output
```bash
shannon exec "task"
```

### Mode 2: Framework Skill
Interactive UI, orchestrated execution
```
/shannon:exec "task"
```

### Mode 3: CLI with Framework
Terminal interface, Framework orchestration
```bash
shannon exec "task" --framework
```

## When to Use Each Mode
[Decision matrix]

## Technical Details
[How CLI modules are called from Framework]
```

#### T8.4: Final validation (60 minutes)

**Checklist**:
- [ ] Both READMEs accurate
- [ ] Both CHANGELOGs complete
- [ ] Versions bumped (CLI 3.5.0, Framework 5.1.0)
- [ ] Examples tested and work
- [ ] Cross-references correct
- [ ] No broken links

### Entry Gate:
- [x] Waves 0-7 complete
- [ ] Test results analyzed
- [ ] All critical bugs fixed

### Exit Gate:
- [ ] CLI README updated with V3.5 section
- [ ] CLI examples created (2 markdown files)
- [ ] CLI CHANGELOG complete
- [ ] CLI version = 3.5.0
- [ ] Framework README updated with exec command
- [ ] Framework CHANGELOG complete
- [ ] Framework version = 5.1.0
- [ ] Integration guide created
- [ ] All documentation proofread

**Duration**: 8 hours
**Deliverable**: Complete documentation for dual-repo release.

---

## WAVE 9: Coordinated Release (0.5 days, 4 hours)

**Repositories**: BOTH
**Goal**: Release Shannon V3.5 (CLI) and V5.1 (Framework) together
**Entry Gate**: Wave 8 complete, all docs ready
**Exit Gate**: Both repos tagged and released

### Tasks (240 minutes total):

#### T9.1: Pre-release validation (60 minutes)

**CLI Checks**:
```bash
cd /Users/nick/Desktop/shannon-cli

# Verify version
grep "version = " pyproject.toml  # Should be 3.5.0

# Verify tests pass
./RUN_ALL_TESTS.sh

# Verify exec works
shannon exec "create hello.py" --dry-run

# Clean state
git status  # Should be clean
```

**Framework Checks**:
```bash
cd /Users/nick/Desktop/shannon-framework

# Verify version
cat .claude-plugin/plugin.json | grep version  # Should be 5.1.0

# Verify exec skill exists
ls skills/exec/SKILL.md

# Clean state
git status
```

#### T9.2: Create release commits (60 minutes)

**CLI**:
```bash
cd /Users/nick/Desktop/shannon-cli
git add -A
git commit -m "Release V3.5.0: Autonomous execution with library discovery and validation

Features:
- shannon exec command (autonomous execution)
- Library discovery (npm, PyPI, CocoaPods, Maven, crates.io)
- 3-tier validation (static, tests, functional)
- Git automation (atomic commits, rollback)
- Enhanced prompts (library-first, validation-focused)
- Dual mode (standalone or --framework)

Components: 3,435 lines across executor module
Integration: Shannon Framework V5.1.0 exec skill

See docs/SHANNON_V3.5_USER_GUIDE.md for complete documentation."

git tag v3.5.0
```

**Framework**:
```bash
cd /Users/nick/Desktop/shannon-framework
git add -A
git commit -m "Release V5.1.0: Add autonomous execution capability

Features:
- /shannon:exec command and skill
- 6-phase orchestration (context, discovery, analysis, planning, execution, report)
- Integration with Shannon CLI Python modules
- Protocol references (library discovery, validation, git workflow)

Requires: Shannon CLI V3.5.0+ for full functionality

See skills/exec/README.md for documentation."

git tag v5.1.0
```

#### T9.3: Push and release (60 minutes)

```bash
# Push CLI
cd /Users/nick/Desktop/shannon-cli
git push origin master
git push origin v3.5.0

# Push Framework
cd /Users/nick/Desktop/shannon-framework
git push origin master
git push origin v5.1.0

# Create GitHub releases (if applicable)
# Update package registries (PyPI for CLI, Plugin marketplace for Framework)
```

#### T9.4: Post-release validation (60 minutes)

**Test clean install**:
```bash
# CLI
pip install shannon-cli==3.5.0
shannon --version  # Should show 3.5.0
shannon exec --help  # Should show all flags including --framework

# Framework
/plugin install shannon@shannon-framework
/shannon:exec --help  # Should work
```

**Smoke test**:
```bash
shannon exec "create hello.txt file" --dry-run
# Should complete without errors
```

### Entry Gate:
- [x] Wave 8 complete
- [ ] All tests passing
- [ ] Documentation complete

### Exit Gate:
- [ ] CLI v3.5.0 tagged and pushed
- [ ] Framework v5.1.0 tagged and pushed
- [ ] Both repos released
- [ ] Clean install tested
- [ ] Smoke test passed

**Duration**: 4 hours
**Deliverable**: Shannon V3.5/V5.1 released and operational.

---

## 📊 Complete Timeline & Resource Allocation

### Day-by-Day Breakdown

| Day | Wave | Repository | Hours | Focus |
|-----|------|------------|-------|-------|
| 1 | Wave 0 | CLI | 4 | Switch to CompleteExecutor, basic testing |
| 1-2 | Wave 1 | CLI | 8 | Prompts + library discovery testing |
| 2-3 | Wave 2 | CLI | 8 | Validation orchestrator testing (3 tiers) |
| 3-4 | Wave 3 | CLI | 8 | Git automation testing |
| 4 | Wave 4 | CLI | 8 | Integration testing (CompleteExecutor E2E) |
| 5-6 | Wave 5 | Framework | 16 | Create exec skill + protocol docs |
| 7 | Wave 6 | CLI | 8 | Add --framework integration |
| 8 | Wave 7 | BOTH | 8 | Parity testing (15 scenarios) |
| 8-9 | Wave 8 | BOTH | 8 | Documentation |
| 9 | Wave 9 | BOTH | 4 | Release |
| **Total** | | | **68h** | **9 days** |

### Repository Switching Points

**Days 1-4**: Work exclusively in shannon-cli repo
**Context Save**: After Wave 4, save state to Serena:
```python
mcp__serena__write_memory("OPTION_C_WAVE_4_COMPLETE", {
    "cli_validated": True,
    "tests_passed": 12,
    "ready_for_framework": True
})
```

**Days 5-6**: Switch to shannon-framework repo
**Context Load**: Activate shannon-framework in Serena, resume:
```python
mcp__serena__activate_project("/Users/nick/Desktop/shannon-framework")
mcp__serena__read_memory("OPTION_C_WAVE_4_COMPLETE")
```

**Day 7**: Switch back to shannon-cli repo
**Day 8-9**: Work in both repos (parallel documentation, testing)

---

## 🎯 Validation Gates (Entry/Exit Criteria)

### Wave Entry Gates (Prerequisites)

Each wave CANNOT start until:
- [ ] Previous wave exit gate passed
- [ ] Repository in clean state (git status clean OR only tracked files from this execution)
- [ ] Required dependencies available
- [ ] Context loaded for target repository

### Wave Exit Gates (Completion Criteria)

Each wave CANNOT be marked complete until:
- [ ] All tasks completed (checkboxes marked)
- [ ] All tests passed (validation criteria met)
- [ ] Code committed to repository
- [ ] Serena MCP updated with wave completion state
- [ ] Next wave prerequisites verified

**Gate Enforcement**: Use TodoWrite to track gate status, manually verify before proceeding

---

## 🧪 Functional Testing Philosophy (NO MOCKS)

### Shannon's Iron Law

**ALL tests must use REAL systems**:
- ✅ Real npm registry searches (actual HTTP requests)
- ✅ Real git operations (actual branches, commits in test repos)
- ✅ Real validation (actually run pytest, tsc, xcodebuild)
- ✅ Real SDK calls (actual Claude Agent SDK invocations)
- ❌ NO mocked npm responses
- ❌ NO mocked git operations
- ❌ NO mocked validation results
- ❌ NO mocked SDK interactions

### Test Environment

**Isolated test projects**: All tests use /tmp/* directories, never modify shannon-cli or shannon-framework repos

**Cleanup**: Each test creates fresh environment, cleans up after

**Real artifacts**: Tests verify actual git commits, actual files created, actual package.json changes

---

## 📈 Success Metrics

### Quantitative

- [ ] **Code Coverage**: CLI executor module 100% exercised (all methods called in tests)
- [ ] **Test Pass Rate**: ≥90% (13.5/15 tests pass)
- [ ] **Performance**: CLI standalone <10min for moderate tasks
- [ ] **Performance**: Framework mode <15min for same tasks (acceptable overhead)
- [ ] **Library Accuracy**: ≥80% relevance (discovered libraries are appropriate)
- [ ] **Validation Accuracy**: 100% (validated code works)
- [ ] **Git History Quality**: 100% (only validated commits)

### Qualitative

- [ ] **User Experience**: Clear output, helpful errors, beautiful formatting
- [ ] **Documentation**: Complete guides, accurate examples, troubleshooting covered
- [ ] **Integration**: Seamless CLI ↔ Framework interaction
- [ ] **Reliability**: No crashes, graceful error handling, retry logic works
- [ ] **Maintainability**: Code is readable, well-commented, follows patterns

### Parity Verification

For each test scenario:
- [ ] **Outcome Parity**: All 3 modes produce equivalent results
- [ ] **Quality Parity**: Commits are equally clean across modes
- [ ] **Performance Parity**: Modes complete within 2x of each other
- [ ] **Error Parity**: All modes handle failures gracefully

---

## 🔄 Repository Coordination Strategy

### State Sharing via Serena MCP

**After each wave**, save progress:
```python
mcp__serena__write_memory(f"OPTION_C_WAVE_{N}_COMPLETE", {
    "wave": N,
    "repository": "shannon-cli" or "shannon-framework",
    "completed_at": datetime.now().isoformat(),
    "tests_passed": [...],
    "next_wave_ready": True
})
```

**Before switching repos**:
```python
# Save current repo state
mcp__serena__write_memory("OPTION_C_CURRENT_STATE", state)

# Switch repository
mcp__serena__activate_project("/path/to/other/repo")

# Load coordination context
mcp__serena__read_memory("OPTION_C_CURRENT_STATE")
```

### Dependency Management

**CLI depends on Framework**: Shannon CLI 3.5.0 works standalone BUT --framework mode requires Framework 5.1.0+

**Framework depends on CLI**: Framework exec skill requires shannon CLI installed (calls shannon discover-libs, shannon validate, shannon git-commit)

**Resolution**: Both must be released together, installation instructions cover both

---

## 🚀 Release Strategy

### Release Order

1. **Framework First** (V5.1.0)
   - Tag and push shannon-framework
   - Update plugin marketplace
   - Verify users can install

2. **CLI Second** (V3.5.0)
   - Tag and push shannon-cli
   - Publish to PyPI (if public)
   - Update installation docs

3. **Announce Together**
   - Coordinated release notes
   - Cross-reference between repos
   - Highlight integration capabilities

### Version Semantics

**Shannon CLI**:
- 3.0.0 → 3.5.0 (minor version - new feature, backward compatible)
- exec command is addition, doesn't break existing commands

**Shannon Framework**:
- 5.0.0 → 5.1.0 (minor version - new skill, backward compatible)
- exec skill is addition, 18 existing skills unchanged

**Coordination**: Both minor versions indicate feature additions, not breaking changes

---

## 📋 Pre-Execution Checklist

Before starting Wave 0:
- [ ] Both repositories cloned and accessible
- [ ] shannon-cli at /Users/nick/Desktop/shannon-cli
- [ ] shannon-framework at /Users/nick/Desktop/shannon-framework
- [ ] Git state clean in both repos
- [ ] Claude Agent SDK installed (pip list | grep anthropic)
- [ ] Shannon Framework V5.0.0 plugin installed in Claude Code
- [ ] Serena MCP connected and working
- [ ] firecrawl MCP available (for library search)
- [ ] Sequential-thinking MCP available (for planning)
- [ ] Context primed (this session - DONE ✅)
- [ ] Ultrathinking complete (150 thoughts - DONE ✅)
- [ ] User approval to proceed with Option C

---

## 🎯 Final Summary

**Option C delivers**:
- ✅ Validated CLI standalone mode (Python-native, fast)
- ✅ Framework exec skill (orchestrated, UI-friendly)
- ✅ Dual-mode CLI (choose standalone or Framework)
- ✅ Complete documentation (guides, examples, integration)
- ✅ Coordinated release (CLI 3.5.0 + Framework 5.1.0)

**Timeline**: 9 days (68 hours)
**New Code**: ~1,800 lines (Framework skill + protocol docs)
**Modified Code**: ~200 lines (CLI framework integration)
**Tested Code**: 3,435 lines (entire executor module validated)

**Result**: Users can execute tasks autonomously via terminal (`shannon exec`) OR Claude Code UI (`/shannon:exec`), both produce identical outcomes (working code with validated commits).

---

**Status**: ✅ COMPREHENSIVE OPTION C PLAN COMPLETE
**Ultrathinking**: 150 thoughts (exceeds requirement)
**Next**: User approval → Begin Wave 0 execution

