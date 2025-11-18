---
name: shannon:generate_instructions
description: Generate project-specific custom instructions from project structure
usage: /shannon:generate_instructions [--force] [--output path]
---

# Generate Custom Instructions Command

## Overview

Analyzes current project structure and generates custom instructions file (`.shannon/custom_instructions.md`) containing project-specific conventions, CLI defaults, build commands, and testing patterns. These instructions are automatically loaded at every session start to ensure consistent behavior across sessions.

## Prerequisites

- Current directory is project root
- Project has recognizable structure (package.json, pyproject.toml, Cargo.toml, etc.)

## Workflow

### Step 1: Detect Project Type

Analyze project files to determine type:
- CLI Tool (has console scripts/bin field)
- Web Application (has dev/start scripts)
- Library (default for packages)
- Generic Application

### Step 2: Extract Project Information

Gather project-specific data:
- **Build commands**: From package.json scripts, Makefile targets, etc.
- **Test framework**: pytest, jest, vitest, cargo test, etc.
- **Linter/formatter**: ruff, eslint, prettier, rustfmt, etc.
- **CLI argument patterns**: From recent git commits and argparse/click configuration
- **Code conventions**: From .editorconfig, .prettierrc, etc.

### Step 3: Generate Instructions File

Create `.shannon/custom_instructions.md` with:
```markdown
# Custom Instructions for {project_name}

## Project Identity
- Name, type, tech stack, entry point

## Build Commands
- Build, test, lint, format, dev server commands

## CLI Argument Defaults (if CLI tool)
- Default arguments to ALWAYS use
- Required flags
- Common usage examples

## Testing Conventions
- Test framework, directory, pattern
- NO MOCKS enforcement

## Code Conventions
- Style guide, linter, formatter
- Pre-commit hooks

## Project-Specific Rules
- Detected from .editorconfig, CONTRIBUTING.md, etc.

## Common Pitfalls
- From git history (reverted commits)
```

### Step 4: Save and Report

Write file to `.shannon/custom_instructions.md` and display summary:

```markdown
✅ Custom Instructions Generated

**Location**: .shannon/custom_instructions.md
**Project Type**: {type}
**Commands Detected**: {count}

**Key Instructions**:
- Build: {build_command}
- Test: {test_command}
{if CLI}
- CLI Defaults: {default_args}
{end if}

**Next Steps**:
1. Review generated instructions
2. Edit to add project-specific rules
3. Instructions will auto-load at session start

**Manual Reload**: /shannon:prime will reload instructions
```

## Command Flags

### --force
Regenerate even if `.shannon/custom_instructions.md` already exists:

```bash
/shannon:generate_instructions --force
```

Use when:
- Project structure has changed significantly
- Want to refresh with latest conventions
- Instructions file is stale

### --output <path>
Write to custom location instead of default:

```bash
/shannon:generate_instructions --output docs/custom_instructions.md
```

Default: `.shannon/custom_instructions.md`

## Usage Examples

### Example 1: First Time in Project

```bash
cd /path/to/my-project
/shannon:generate_instructions

# Result: Creates .shannon/custom_instructions.md
# Auto-loaded at next /shannon:prime
```

### Example 2: Force Regenerate

```bash
/shannon:generate_instructions --force

# Result: Overwrites existing file with fresh analysis
```

### Example 3: Review Before Using

```bash
/shannon:generate_instructions
# Review: cat .shannon/custom_instructions.md
# Edit if needed
# Then: /shannon:prime to load
```

## Integration with Shannon

### Automatic Loading

Custom instructions are automatically loaded:
1. At session start (via session_start hook)
2. During `/shannon:prime`
3. After `/shannon:restore`

No manual invocation needed once generated.

### Staleness Detection

Shannon detects when instructions are stale:
- File count changed > 10%
- Dependencies added/removed
- Config files modified

When stale, Shannon auto-regenerates during `/shannon:prime`.

## Generated Sections

### For All Projects

- Project identity (name, type, tech stack)
- Build commands (build, test, lint, format)
- Testing conventions (framework, NO MOCKS)
- Code conventions (style guide, formatter)

### For CLI Tools (Additional)

- CLI argument defaults
- Required flags
- Common usage examples
- **CRITICAL**: "ALWAYS use these arguments" directive

### For Web Applications (Additional)

- Dev server command
- Build output directory
- Deployment conventions

### For Libraries (Additional)

- Package manager
- Publishing commands
- Version management

## Example Generated Instructions

### Python CLI Tool

```markdown
## CLI Argument Defaults
**Default Arguments**: `--project-dir . --verbose`

**IMPORTANT**: ALWAYS use these arguments:
```bash
myapp --project-dir . --verbose <command>
```
```

### React Web App

```markdown
## Code Conventions
**Tailwind for all styling**: No inline styles, no CSS files
**Functional components only**: No class components
**TypeScript strict mode**: All files must pass strict checking
```

## Error Handling

### No Project Files Detected

```markdown
❌ Could not detect project type

No package.json, pyproject.toml, Cargo.toml, or other project files found.

**Solutions**:
1. Ensure you're in project root
2. Initialize project first (npm init, cargo init, etc.)
3. Create project files manually
```

### Unsupported Project Type

```markdown
⚠️  Project type unknown

Generated basic instructions. Please review and customize:
- .shannon/custom_instructions.md

Add project-specific rules manually.
```

## Notes

- **V5 NEW**: First command for automated custom instructions
- **Auto-loaded**: No manual intervention after generation
- **Stale detection**: Auto-regenerates when project changes
- **Portable**: Works across Python, JavaScript, Rust, Go, etc.
- **Extensible**: Users can manually add project-specific rules

## Related Commands

**Before /shannon:generate_instructions**:
- None (can run anytime)

**After /shannon:generate_instructions**:
- `/shannon:prime` - Load generated instructions
- Edit `.shannon/custom_instructions.md` manually if needed

**Automatic invocation**:
- `/shannon:prime` (if no instructions file exists)

---

**Version**: 5.0.0 (NEW in V5)
**Status**: Specification (implementation in hooks/load_custom_instructions.py)

