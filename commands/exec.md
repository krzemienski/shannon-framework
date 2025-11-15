---
name: exec
description: Autonomous task execution with library discovery and validation
tags: [execution, automation, libraries, validation, git, autonomous]
---

# Shannon Exec: Autonomous Task Execution

Execute tasks autonomously with automatic library discovery, 3-tier functional validation, and atomic git commits.

## Usage

```
/shannon:exec "task description"
/shannon:exec "task" --dry-run
/shannon:exec "task" --interactive
```

## What It Does

1. **Discovers Libraries**: Searches npm, PyPI, etc. for existing solutions
2. **Generates Code**: Uses /shannon:wave for AI code generation
3. **Validates Functionally**: Runs build + tests + actual functionality checks
4. **Commits Atomically**: Only validated code enters git history
5. **Retries on Failure**: Rolls back and retries (max 3x)

## Workflow

```
@skill exec
  task: {user_task}
  options:
    dry_run: false
    interactive: false
    max_iterations: 3
```

The exec skill orchestrates:
- Phase 1: Context preparation (/shannon:prime)
- Phase 2: Library discovery (shannon discover-libs)
- Phase 3: Task analysis (optional)
- Phase 4: Execution planning
- Phase 5: Code generation + validation + commit loop
- Phase 6: Execution report

## Examples

### Simple Task
```
/shannon:exec "create hello.py that prints hello world"
```
**Result**: hello.py created, validated, committed in ~20s

### Feature with Libraries
```
/shannon:exec "add authentication to React app"
```
**Result**: Discovers next-auth, uses it, validates, commits in ~5min

### Dry-Run Mode
```
/shannon:exec "build e-commerce platform" --dry-run
```
**Result**: Shows plan (libraries, steps) without executing

## Requirements

- **Shannon CLI** V3.5.0+ (provides executor modules)
- **Serena MCP** (required for caching)
- **Clean git state** (no uncommitted changes)

## Output

- Git branch with validated commits
- Execution report saved to Serena
- Libraries used documented
- Validation results per commit

---

See `skills/exec/SKILL.md` for complete workflow details.
