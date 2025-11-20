# /sh_status - Shannon Framework Status - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sh_status - Shannon Framework Status

Shows comprehensive status of Shannon Framework including version, active components, MCP server availability, and session state.

## Purpose

This command provides a complete health check and status overview of Shannon Framework, helping you:
- Verify Shannon is properly installed and active
- Check MCP server availability and configuration
- View available commands and agents
- Monitor session context and checkpoints
- Diagnose configuration issues

## Usage

```bash
/sh_status              # Standard status display
/sh_status --verbose    # Detailed diagnostic information
/sh_status --mcps-only  # MCP server status only
```

## Output Format

```
═══════════════════════════════════════════════════════════════
🌊 SHANNON FRAMEWORK STATUS
═══════════════════════════════════════════════════════════════

VERSION: v3.0.0
STATUS: ✅ ACTIVE | Installation: Plugin System

───────────────────────────────────────────────────────────────
📡 MCP SERVER STATUS
───────────────────────────────────────────────────────────────

REQUIRED:
  ✅ Serena MCP       Connected | Context preservation active

RECOMMENDED:
  ✅ Sequential MCP   Connected | Complex reasoning available
  ✅ Context7 MCP     Connected | Documentation patterns ready
  ⚠️  Puppeteer MCP   Not Found | Browser testing unavailable

CONDITIONAL:
  ✅ shadcn-ui MCP    Connected | React UI components ready

💡 Run /sh_check_mcps for detailed MCP configuration guidance

───────────────────────────────────────────────────────────────
⚡ AVAILABLE COMMANDS (31)
───────────────────────────────────────────────────────────────

Shannon Commands (6):
  /sh_spec, /sh_checkpoint, /sh_restore, /sh_status, /sh_check_mcps

Enhanced SuperClaude Commands (25):
  /sc_analyze, /sc_implement, /sc_build, /sc_test, and 21 more...

📖 Run /help for complete command details

───────────────────────────────────────────────────────────────
🤖 AVAILABLE AGENTS (19)
───────────────────────────────────────────────────────────────

Shannon Agents (5):
  • SPEC_ANALYZER, PHASE_ARCHITECT, WAVE_COORDINATOR, CONTEXT_GUARDIAN, TEST_GUARDIAN

Enhanced SuperClaude Agents (14):
  • ANALYZER, ARCHITECT, FRONTEND, BACKEND, PERFORMANCE, SECURITY, QA, REFACTORER,
    DEVOPS, MENTOR, SCRIBE, DATA_ENGINEER, MOBILE_DEVELOPER, IMPLEMENTATION_WORKER

🤖 Run /agents for detailed agent capabilities

───────────────────────────────────────────────────────────────
📚 DOCUMENTATION
───────────────────────────────────────────────────────────────

• Installation: docs/PLUGIN_INSTALL.md
• Commands: SHANNON_COMMANDS_GUIDE.md
• Specification: SHANNON_V3_SPECIFICATION.md
• Migration: docs/MIGRATION_GUIDE.md

═══════════════════════════════════════════════════════════════
```

## What This Command Does

### 1. Displays Shannon Version
Shows current Shannon Framework version from plugin manifest

### 2. Checks MCP Server Status
Detects MCP availability by checking for their characteristic tools:
- **Serena**: mcp__serena__list_memories
- **Sequential**: mcp__sequential-thinking__sequentialthinking
- **Context7**: mcp__Context7__resolve-library-id
- **Puppeteer**: mcp__puppeteer__puppeteer_navigate
- **shadcn-ui**: mcp__shadcn-ui__get_component

### 3. Lists Available Components
Shows all Shannon commands and agents with brief descriptions

### 4. Displays Session Context
Shows current checkpoint status, wave execution state (if active), project memory status

## When to Use

- **After installation**: First command to verify setup
- **Debugging**: When Shannon commands aren't working
- **Regular health checks**: Ensure all systems operational
- **Before starting complex work**: Verify context preservation is active

## Related Commands

- `/sh_check_mcps` - Detailed MCP setup guidance
- `/help` - Full command catalog
- `/agents` - Agent capabilities

## Troubleshooting

If status shows issues:

**Serena Not Connected**:
1. Run /sh_check_mcps for setup instructions
2. Configure Serena in Claude Code settings
3. Restart Claude Code
4. Run /sh_status again to verify

**Commands Not Showing**:
1. Verify plugin installed: /plugin
2. Check plugin enabled
3. Restart Claude Code if needed

**Agents Not Available**:
1. Check /agents to see all available agents
2. Shannon agents should appear with descriptions
3. If missing, reinstall plugin

This command is Shannon's "health check" - run it anytime you're unsure about Shannon's status.
