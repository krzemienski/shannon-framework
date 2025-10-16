# Shannon Framework V3 - Plugin Development Context

<!--
  ⚠️ NOTICE: Shannon v3.0.0+ is distributed as a Claude Code PLUGIN

  FOR SHANNON USERS:
  Install via plugin system instead of this CLAUDE.md:
    /plugin marketplace add shannon-framework/shannon
    /plugin install shannon@shannon-framework
  See: docs/PLUGIN_INSTALL.md

  FOR SHANNON DEVELOPERS:
  This file provides development context when working on Shannon itself.
  The plugin source is in shannon-plugin/ directory.
-->

# Shannon Plugin Development Guide

## Quick Reference

**Plugin Location**: `shannon-plugin/`
**Commands**: `shannon-plugin/commands/` (33 commands)
**Agents**: `shannon-plugin/agents/` (19 agents)
**Hooks**: `shannon-plugin/hooks/` (PreCompact, SessionStart)
**Core Patterns**: `shannon-plugin/core/` (8 behavioral documents)
**Documentation**: `shannon-plugin/README.md`, `docs/`

## Development Workflow

When developing Shannon Framework:

### 1. Make Changes
Edit files in `shannon-plugin/`:
- Commands: `shannon-plugin/commands/*.md`
- Agents: `shannon-plugin/agents/*.md`
- Hooks: `shannon-plugin/hooks/hooks.json` or `hooks/*.py`
- Core: `shannon-plugin/core/*.md`

### 2. Test Locally
```bash
# In Claude Code:
/plugin marketplace add /Users/nick/Documents/shannon
/plugin uninstall shannon@shannon  # If already installed
/plugin install shannon@shannon

# Restart Claude Code

# Test your changes:
/sh_status
/sh_spec "test specification"
```

### 3. Validate
```bash
# Run automated validation
python3 shannon-plugin/scripts/validate.py

# Check JSON syntax
jq . .claude-plugin/marketplace.json
jq . shannon-plugin/.claude-plugin/plugin.json
jq . shannon-plugin/hooks/hooks.json
```

### 4. Commit
```bash
git add shannon-plugin/
git commit -m "feat(component): description of change"
```

## Key Components for Development

### Core Behavioral Patterns
Reference documentation in `shannon-plugin/core/`:
- SPEC_ANALYSIS.md - 8D complexity framework
- PHASE_PLANNING.md - 5-phase planning system
- WAVE_ORCHESTRATION.md - Multi-stage execution
- CONTEXT_MANAGEMENT.md - Checkpoint/restore patterns
- TESTING_PHILOSOPHY.md - NO MOCKS principles
- HOOK_SYSTEM.md - Hook integration
- PROJECT_MEMORY.md - Serena memory patterns
- MCP_DISCOVERY.md - Dynamic MCP recommendations

### Execution Modes
Reference in `shannon-plugin/modes/`:
- WAVE_EXECUTION.md - Wave orchestration behaviors
- SHANNON_INTEGRATION.md - SuperClaude coordination

## MCP Requirements for Development

Testing Shannon requires:
- **Serena MCP** (mandatory) - Context preservation
- **Sequential MCP** (recommended) - Complex analysis
- **Context7 MCP** (recommended) - Framework patterns
- **Puppeteer MCP** (recommended) - Browser testing

See: `docs/PLUGIN_INSTALL.md` for MCP configuration

## Testing Your Changes

### Manual Testing
1. Install plugin locally (see above)
2. Test commands: `/sh_spec`, `/sh_checkpoint`, etc.
3. Test agents: Check auto-activation works
4. Test hooks: Verify PreCompact triggers

### Automated Testing
```bash
# Structure validation
python3 tests/validate_structure.py

# Frontmatter validation
python3 tests/validate_frontmatter.py

# Hook testing
python3 tests/test_hooks.py
```

## Documentation

When developing Shannon, reference:
- **Plugin Spec**: `SHANNON_V3_SPECIFICATION.md`
- **Commands**: `SHANNON_COMMANDS_GUIDE.md`
- **Installation**: `docs/PLUGIN_INSTALL.md`
- **Migration**: `docs/MIGRATION_GUIDE.md`
- **Testing**: `docs/TEST_PLAN.md`

## Important Notes

- **This CLAUDE.md**: For Shannon development only
- **Plugin Installation**: Primary method for Shannon users
- **Legacy Shannon/**: Deprecated, see Shannon-legacy/
- **Active Plugin**: Install shannon-plugin/ as plugin for actual use

---

**For Development Questions**: See `docs/DEVELOPER_GUIDE.md` (to be created)

**For Plugin Usage**: Install Shannon plugin, don't use this CLAUDE.md
