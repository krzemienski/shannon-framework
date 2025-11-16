# Shannon CLI

**Version**: 3.1 (Dashboard) + 3.5 (Autonomous Executor Core)  
**Status**: Production (V3.1), Core Complete (V3.5)

---

## Overview

Shannon CLI provides:
- **V3.1**: Interactive 4-layer dashboard for monitoring AI agent execution (htop/k9s-level TUI)
- **V3.5**: Autonomous execution modules (enhanced prompts, library discovery, validation, git automation)

---

## Quick Start

### Try V3.1 Dashboard

```bash
# Interactive demo with mock data
./RUN_DASHBOARD_DEMO.sh

# Automated tests
python3 test_dashboard_interactive.py
```

### Test V3.5 Modules

```bash
# Test all modules
python3 test_all_v3.5_modules.py

# Test end-to-end integration
python3 test_v3.5_end_to_end.py
```

---

## shannon exec - Autonomous Code Generation

**NEW in V3.5**: The `shannon exec` command enables autonomous code generation with built-in validation and git automation.

### Basic Usage

```bash
shannon exec "create a calculator module with basic math operations"
```

**What happens**:
1. 🔍 **Library Discovery**: Searches npm/PyPI for relevant libraries (auto-detects project type)
2. 💡 **Enhanced Prompts**: 17k+ character behavioral guidance injected
3. 🤖 **Autonomous Generation**: Claude generates code following project patterns
4. ✅ **3-Tier Validation**: Static checks → Tests → Functional validation
5. 🔄 **Auto-Retry**: Up to 3 attempts if validation fails
6. ✨ **Git Automation**: Creates semantic branch + atomic commit

### Examples

**Simple Task** (Python):
```bash
shannon exec "add logging utility with file and console handlers"
```
Result: Creates `utils/logger.py` with complete implementation, tested and committed

**Library-Heavy Task** (Node.js):
```bash
shannon exec "add Express REST API with /health and /metrics endpoints"
```
Result: Discovers Express, creates `server.js`, updates `package.json`, validates endpoint works

**Complex Task** (Multi-file):
```bash
shannon exec "implement user authentication with JWT tokens"
```
Result: Creates `auth/tokens.py`, `auth/middleware.py`, `models/user.py` with complete flow

### Flags

- `--dry-run`: Preview changes without executing (shows plan, libraries, estimated changes)
- `--auto-commit`: Skip commit confirmation (auto-commits on successful validation)
- `--verbose`: Show detailed execution logs (prompts, API calls, validation output)
- `--no-validation`: Skip validation tiers (use with caution!)
- `--max-retries N`: Set retry limit (default: 3)

### Features

✅ **Smart Library Discovery**:
- Searches npm (JavaScript/TypeScript projects)
- Searches PyPI (Python projects)
- Searches Swift Package Index (iOS projects)
- Quality scoring: stars + maintenance + downloads + license
- 7-day Serena caching for speed

✅ **3-Tier Validation**:
- **Tier 1** (Static): Build/compile, lint, type checking
- **Tier 2** (Tests): Unit tests, integration tests
- **Tier 3** (Functional): E2E tests, actual execution validation

✅ **Git Automation**:
- Semantic branch naming: `feat/`, `fix/`, `perf/`, `refactor/`
- Structured commits with validation proof
- Atomic rollback on validation failure
- Clean git state enforcement

✅ **Project Intelligence**:
- Auto-detects: Python, Node.js, iOS, React, Next.js, Django, FastAPI
- Finds test infrastructure: pytest, jest, npm test
- Detects linters: ruff, eslint, mypy, typescript
- Respects existing patterns and conventions

### Requirements

**Minimum**:
- Python 3.10+
- Git installed
- Project with valid package manager (npm, pip, etc.)

**Recommended** (for best results):
- Shannon Framework installed (`npm install -g @shannon/framework`)
- Project with test suite configured
- Linter/formatter configured (ruff, eslint, black)

### Limitations

- ⚠️ Requires clean git state (uncommitted changes block execution)
- ⚠️ Node.js support requires Node 18+ with npm
- ⚠️ iOS support requires Xcode CLI tools
- ⚠️ Validation quality depends on test suite coverage

---

## V3.1 Interactive Dashboard

**4-layer interactive TUI** for monitoring Shannon Framework execution:

- **Layer 1**: Session overview (goal, phase, progress, metrics)
- **Layer 2**: Agent list (multi-agent wave selection)
- **Layer 3**: Agent detail (context, tools, current operation)
- **Layer 4**: Message stream (full SDK conversation with scrolling)

**Features**:
- Full keyboard navigation (Enter/Esc/1-9/arrows/h/q)
- Agent selection and focusing
- Message stream with virtual scrolling (1000+ messages)
- 4 Hz refresh rate, <50ms render time
- Context-aware help overlay

**Status**: ✅ Production ready (test with real Shannon execution first)

---

## V3.5 Autonomous Executor Modules

**Core modules** for building autonomous execution:

### PromptEnhancer
Generates 17k+ character enhanced system prompts with:
- Library discovery instructions (don't reinvent wheel)
- Functional validation requirements (3-tier: static, unit, E2E)
- Git workflow automation (atomic commits)
- Project-specific guidelines (iOS, React, Python, etc.)

### LibraryDiscoverer
Discovers and recommends open-source libraries:
- Knowledge base: npm, PyPI, CocoaPods, Swift PM
- Quality scoring (stars + maintenance + downloads + license)
- File-based caching

### ValidationOrchestrator
3-tier validation framework:
- Tier 1: Static (build, lint, types)
- Tier 2: Unit/Integration tests
- Tier 3: Functional (E2E, user perspective)
- **Runs REAL tests** via subprocess

### GitManager
Git workflow automation:
- Semantic branch naming (fix/, feat/, perf/, refactor/)
- **Executes REAL git commands** via subprocess
- Atomic commits with validation proof
- Rollback on failure

### CompleteExecutor
Full autonomous execution with:
- Iteration/retry logic (up to 3 attempts)
- Validation loop
- Git integration
- **Template-based code generation** for simple tasks

**Status**: ✅ Core modules functional, full autonomy needs Shannon Framework integration

---

## Usage

### V3.1 Dashboard

```python
from shannon.ui.dashboard_v31 import InteractiveDashboard

dashboard = InteractiveDashboard(
    metrics=metrics_collector,
    agents=agent_tracker,
    context=context_mgr,
    session=session_mgr
)

with dashboard:
    # Dashboard shows real-time execution
    await your_operation()
```

### V3.5 Modules

```python
from shannon.executor import (
    PromptEnhancer,
    LibraryDiscoverer,
    ValidationOrchestrator,
    GitManager
)

# Build enhanced prompts
prompts = PromptEnhancer().build_enhancements(task, project_root)

# Discover libraries
libs = await LibraryDiscoverer(project_root).discover_for_feature("auth")

# Validate code
result = await ValidationOrchestrator(project_root).validate_all_tiers(changes)

# Manage git
branch = await GitManager(project_root).create_feature_branch(task)
```

---

## Testing

### Run All Tests

```bash
./RUN_ALL_TESTS.sh
# Expected: 16/16 tests PASSING
```

### Individual Tests

```bash
# V3.1 Dashboard
python3 test_dashboard_interactive.py    # 8/8 tests

# V3.5 Modules
python3 test_all_v3.5_modules.py         # 6/6 tests

# V3.5 End-to-End
python3 test_v3.5_end_to_end.py          # 1/1 test

# V3.5 Complete Executor
python3 test_complete_v3.5.py            # 1/1 test
```

---

## Documentation

- **SHANNON_V3.1_INTERACTIVE_DASHBOARD_SPEC.md** - Complete V3.1 specification (2,632 lines)
- **SHANNON_V3.5_REVISED_SPEC.md** - Complete V3.5 specification (2,490 lines)
- **HONEST_REFLECTION.md** - Honest assessment of what works and what doesn't
- **FINAL_DELIVERY.md** - Final delivery summary
- **CHANGELOG.md** - Version history

---

## Project Structure

```
src/shannon/
├── ui/dashboard_v31/        # V3.1 Interactive Dashboard
│   ├── models.py            # Data models
│   ├── data_provider.py     # Data aggregation
│   ├── navigation.py        # Keyboard navigation
│   ├── keyboard.py          # Terminal input
│   ├── renderers.py         # 4-layer rendering
│   ├── dashboard.py         # Main dashboard
│   ├── optimizations.py     # Virtual scrolling
│   └── help.py              # Help overlay
│
├── executor/                # V3.5 Autonomous Executor
│   ├── prompts.py           # Core prompt templates
│   ├── task_enhancements.py # Project-specific prompts
│   ├── prompt_enhancer.py   # Prompt builder
│   ├── library_discoverer.py # Library search & ranking
│   ├── validator.py         # 3-tier validation
│   ├── git_manager.py       # Git operations
│   ├── simple_executor.py   # Simple orchestrator
│   ├── complete_executor.py # Full autonomous with iteration
│   ├── code_executor.py     # Code generation scaffold
│   └── models.py            # Data models
│
├── sdk/                     # SDK Integration
│   └── client.py            # Enhanced with system_prompt.append
│
├── core/                    # Core Systems
│   └── session_manager.py   # Session tracking
│
└── metrics/                 # Metrics & Dashboard
    └── dashboard.py         # LiveDashboard with V3.1 delegation
```

---

## Status

**V3.1**: ✅ Production ready (Interactive Dashboard complete)
**V3.5**: ✅ **shannon exec** command ready for release
- Library Discovery: npm + PyPI APIs validated ✅
- 3-Tier Validation: Working with real test execution ✅
- Git Automation: Atomic commits + rollback verified ✅
- Enhanced Prompts: 17k+ character injection complete ✅

**Tests**: ✅ 16/16 passing (100%)
**Code Quality**: ✅ Clean, no dead code, real implementations (no mocks)

---

## License

See LICENSE file

---

## Contributing

See contribution guidelines in docs/

---

*Shannon CLI - Making AI agent development transparent and autonomous*
