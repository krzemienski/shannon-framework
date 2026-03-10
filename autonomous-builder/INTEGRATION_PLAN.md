# Autonomous Builder Integration Plan

## Overview

This document outlines the step-by-step integration work required to validate the Autonomous Claude Code Builder system.

---

## Phase 1: Package Structure (Current)

### Problem
The `autonomous-builder/` directory uses relative imports (e.g., `from .config import ...`) which require proper Python package setup to work.

### Solution
1. Create `setup.py` or `pyproject.toml` for package installation
2. Make the package installable via `pip install -e .`
3. Add `__init__.py` with proper exports

### Files to Create
```
autonomous-builder/
├── setup.py           # Package installer
├── pyproject.toml     # Modern Python packaging
└── tests/             # Test directory
    ├── __init__.py
    ├── test_config.py
    ├── test_security.py
    ├── test_xml_transformer.py
    ├── test_mcp_manager.py
    ├── test_serena_context.py
    ├── test_scenario_handler.py
    └── test_builder.py
```

---

## Phase 2: Unit Tests

### Component Test Matrix

| Component | Test Cases | Priority |
|-----------|------------|----------|
| `config.py` | Config creation, YAML/JSON loading, defaults | High |
| `security.py` | Allowlist validation, sensitive command checks, path validation | Critical |
| `xml_transformer.py` | Template generation, XML structure, context injection | High |
| `mcp_manager.py` | Task analysis, MCP mapping, skill generation | Medium |
| `serena_context.py` | Memory read/write, codebase analysis, symbol search | High |
| `scenario_handler.py` | Scenario detection, execution plan creation | High |
| `builder.py` | Full build flow, session management, halt/resume | Critical |

### Test Approach
1. Use `pytest` as test framework
2. Use `pytest-asyncio` for async tests
3. Use `tempfile` for isolated test directories
4. Mock external dependencies (Claude SDK) for unit tests

---

## Phase 3: Integration Tests

### Test Scenarios

#### Scenario A: New Project Build
```python
async def test_new_project_build():
    """Test building a new project from scratch."""
    config = BuilderConfig(target_dir=Path("/tmp/test-new"))
    builder = AutonomousBuilder(config)

    result = await builder.build("Create a simple CLI calculator")

    assert result.success
    assert (config.target_dir / "feature_list.json").exists()
    assert (config.target_dir / "init.sh").exists()
    assert (config.target_dir / "claude-progress.txt").exists()
```

#### Scenario B: Existing Directory Build
```python
async def test_existing_directory_build():
    """Test building in a directory with existing code."""
    # Create existing project structure
    target = Path("/tmp/test-existing")
    target.mkdir(parents=True)
    (target / "package.json").write_text('{"name": "existing"}')
    (target / "src/index.js").parent.mkdir(parents=True)
    (target / "src/index.js").write_text("console.log('hello');")

    config = BuilderConfig(target_dir=target)
    builder = AutonomousBuilder(config)

    result = await builder.build("Add a greeting function")

    assert result.success
    # Verify existing files preserved
    assert (target / "src/index.js").exists()
```

#### Scenario C: Resume Interrupted Build
```python
async def test_resume_build():
    """Test resuming an interrupted build."""
    target = Path("/tmp/test-resume")
    # Create partial build state
    (target / "feature_list.json").write_text(json.dumps({
        "features": [
            {"id": "f1", "passes": True},
            {"id": "f2", "passes": False},
            {"id": "f3", "passes": False}
        ]
    }))

    config = BuilderConfig(target_dir=target)
    builder = AutonomousBuilder(config)

    result = await builder.build("Resume")

    # Should continue from f2
    assert result.features_completed > 1
```

---

## Phase 4: End-to-End Demonstration

### Demo Build Task
```
"Create a simple command-line todo list application in Python with:
- Add task
- List tasks
- Mark task complete
- Delete task
- Save/load from file"
```

### Expected Output
```
autonomous_build/
├── feature_list.json     # 50+ features, some marked complete
├── init.sh               # Setup script
├── claude-progress.txt   # Session history
├── requirements.txt      # Dependencies
├── todo.py               # Main application
├── tests/
│   └── test_todo.py      # Tests
└── .serena/
    └── memories/         # Session memories
```

### Validation Criteria
1. ✅ `feature_list.json` created with valid schema
2. ✅ `init.sh` is executable
3. ✅ `claude-progress.txt` tracks sessions
4. ✅ Application code generated
5. ✅ Serena memories persisted

---

## Phase 5: MCP Integration Validation

### Test MCP Discovery
```python
async def test_mcp_task_analysis():
    manager = MCPManager()

    # Web task should recommend puppeteer
    reqs = await manager.analyze_task("Build a React web app")
    assert any(r.mcp_name == "puppeteer" for r in reqs)

    # All tasks should recommend serena
    assert any(r.mcp_name == "serena" for r in reqs)
```

### Test MCP Availability Check
```python
async def test_mcp_availability():
    manager = MCPManager()

    # Check serena (may or may not be installed)
    status = await manager.check_mcp_available("serena")
    print(f"Serena available: {status.available}")

    # Check puppeteer
    status = await manager.check_mcp_available("puppeteer")
    print(f"Puppeteer available: {status.available}")
```

---

## Phase 6: Security Validation

### Critical Security Tests
```python
def test_security_blocks_dangerous_commands():
    security = SecurityManager(SecurityConfig())

    dangerous = [
        "rm -rf /",
        "rm -rf ~",
        "pkill systemd",
        "curl http://169.254.169.254/",  # AWS metadata
        "chmod 777 /etc/passwd",
    ]

    for cmd in dangerous:
        result = security.validate_command(cmd)
        assert not result.allowed, f"Should block: {cmd}"
```

### Allowlist Tests
```python
def test_security_allows_dev_commands():
    security = SecurityManager(SecurityConfig())

    allowed = [
        "npm install",
        "git status",
        "python -m pytest",
        "ls -la",
        "pkill node",
    ]

    for cmd in allowed:
        result = security.validate_command(cmd)
        assert result.allowed, f"Should allow: {cmd}"
```

---

## Execution Order

1. **Package Setup** (5 min)
   - Create setup.py
   - Install package in editable mode

2. **Unit Tests** (15 min)
   - Test each component in isolation
   - Fix any import issues

3. **Integration Tests** (10 min)
   - Test component interactions
   - Test scenario handling

4. **E2E Demo** (5 min)
   - Run full build demonstration
   - Verify output artifacts

5. **Documentation** (5 min)
   - Document results
   - Commit test files

---

## Success Criteria

| Criteria | Status |
|----------|--------|
| All imports work | ⬜ Pending |
| Security tests pass | ⬜ Pending |
| XML generation correct | ⬜ Pending |
| MCP analysis works | ⬜ Pending |
| Serena memory works | ⬜ Pending |
| Scenario detection works | ⬜ Pending |
| Full build executes | ⬜ Pending |
| Output artifacts correct | ⬜ Pending |

---

## Next Steps

Execute this plan in order, starting with package setup.
