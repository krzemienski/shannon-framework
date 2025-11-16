# Shannon V4.0 Usage Guide

## Quick Start

### Installation

```bash
# Install Shannon CLI
pip install shannon-cli  # or poetry install

# Verify installation
shannon --version  # Should show 4.0.0
```

### Basic Usage - Autonomous Mode

```bash
# Simple file creation
shannon exec "create hello.py that prints hello world"

# Complex module
shannon exec "create authentication module with JWT tokens"
```

### Advanced Usage - Interactive Mode

```bash
# Start server (Terminal 1)
poetry run python run_server.py

# Start dashboard (Terminal 2)
cd dashboard && npm run dev

# Execute with monitoring (Terminal 3)
shannon do "implement user registration" --dashboard

# Open browser: http://localhost:5173
# Watch real-time execution!
```

## Command Reference

### shannon exec (Autonomous)

**Purpose**: Fast autonomous code generation

**Syntax**:
```bash
shannon exec "<task>" [--dry-run] [--auto-commit] [--verbose]
```

**Examples**:
```bash
# Python utility
shannon exec "create utils/helpers.py with file I/O functions"

# React component
shannon exec "create LoginForm.tsx with form validation"

# API endpoint
shannon exec "add /users POST endpoint with validation"
```

### shannon do (Interactive)

**Purpose**: Orchestrated execution with visibility and control

**Syntax**:
```bash
shannon do "<task>" [--dashboard] [--auto] [--dry-run] [--verbose]
```

**Examples**:
```bash
# With dashboard monitoring
shannon do "refactor authentication system" --dashboard

# Autonomous mode (no dashboard)
shannon do "add error handling to API" --auto

# Plan only (no execution)
shannon do "migrate database schema" --dry-run
```

## When to Use What

| Scenario | Command | Reason |
|----------|---------|--------|
| Quick file creation | shannon exec | Faster, proven for simple tasks |
| Complex refactoring | shannon do --dashboard | Need visibility and control |
| Critical production changes | shannon do --dashboard | Want to monitor and HALT if needed |
| Learning/exploration | shannon do --dry-run | See plan without executing |
| CI/CD automation | shannon exec --auto-commit | Non-interactive automation |

## Creating Custom Skills

```bash
# Create project skill
mkdir -p .shannon/skills
cat > .shannon/skills/my_deploy.yaml << 'EOF'
name: deploy_to_staging
version: 1.0.0
description: Deploy application to staging environment
category: deployment

execution:
  type: script
  script: ./scripts/deploy.sh
  timeout: 300

hooks:
  pre:
    - validation_orchestrator
  post:
    - notify_team
EOF

# Auto-discovered on next run!
shannon do "deploy to staging"
```

## Dashboard Features

### ExecutionOverview Panel
- Task name and description
- Current phase and progress %
- Elapsed time and ETA
- HALT/RESUME buttons

### SkillsView Panel
- Active skills with progress bars
- Queued skills
- Completed skills
- Skill details on click

### FileDiff Panel
- Live code changes as they happen
- Syntax-highlighted diffs
- Approve/Revert buttons (planned)

### AgentPool Panel
- Multi-agent status (framework ready)
- Agent progress tracking
- Spawn/terminate controls (planned)

### Decisions Panel
- Decision points requiring input (planned)
- Option selection UI

### Validation Panel
- Real-time test output (planned)
- Validation tier status

## Troubleshooting

### shannon do doesn't create files
**Solution**: Ensure code_generation skill exists in `skills/built-in/`

### Dashboard won't connect
**Solution**:
1. Check server running: `curl http://localhost:8000/health`
2. Check dashboard: Browser console for errors
3. Verify WebSocket URL in dashboard config

### Skills not discovered
**Solution**: Run `shannon do "test" --verbose` to see discovery logs

### Validation fails
**Solution**: Check project has test infrastructure (pytest, npm test, etc.)

## Architecture

Shannon V4.0 architecture:
- V3.0 Base: SDK integration, context, metrics, analytics
- V3.5 Layer: Autonomous execution modules
- V4.0 Layer: Skills framework + orchestration + dashboard

All three layers work together seamlessly.
