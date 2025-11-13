---
name: status
description: Display Shannon Framework status, version, MCP servers, and configuration
usage: /shannon:status [--mcps] [--goals] [--verbose]
---

# Shannon Framework Status Command

## Overview

Shows comprehensive status of Shannon Framework including version, active components, MCP server availability, and session state. This command orchestrates multiple skills to provide a complete health check.

## Purpose

This command provides a complete health check and status overview of Shannon Framework, helping you:
- Verify Shannon is properly installed and active
- Check MCP server availability and configuration
- View available commands and agents
- Monitor session context and checkpoints
- Display active goals and progress
- Diagnose configuration issues

## Prerequisites

- Shannon plugin installed and active

## Workflow

### Step 1: Display Shannon Version & Installation Status

Show basic Shannon information:
- Version from plugin manifest
- Installation type (Plugin System)
- Active status

### Step 2: Check MCP Servers (if --mcps flag)

If `--mcps` flag present, invoke mcp-discovery skill:

**Invocation:**
```
@skill mcp-discovery
- Input:
  * mode: "health-check"
  * verbose: [true if --verbose flag present]
- Output: mcp_status_result
```

The mcp-discovery skill will:
1. Detect available MCP servers
2. Check required MCPs (Serena)
3. Check recommended MCPs (Sequential, Context7, Puppeteer)
4. Check conditional MCPs (shadcn-ui, etc.)
5. Generate MCP status report

**Display Format:**
```
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

💡 Run /shannon:check_mcps for detailed MCP configuration guidance
```

### Step 3: Display Available Commands & Agents

Show Shannon components:

```
───────────────────────────────────────────────────────────────
⚡ AVAILABLE COMMANDS (31)
───────────────────────────────────────────────────────────────

Shannon Commands (6):
  /shannon:check_mcps, /shannon:check_mcps, /shannon:restore, /shannon:status, /shannon:check_mcps

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
```

### Step 4: Display Active Goals (if --goals flag)

If `--goals` flag present, invoke goal-management skill:

**Invocation:**
```
@skill goal-management
- Input:
  * mode: "list"
  * verbose: [true if --verbose flag present]
- Output: goals_list_result
```

The goal-management skill will:
1. Query active goals from Serena
2. Calculate progress percentages
3. Identify completed/in-progress/blocked goals
4. Generate goals summary

**Display Format:**
```
───────────────────────────────────────────────────────────────
🎯 ACTIVE GOALS
───────────────────────────────────────────────────────────────

📊 MVP Feature Complete: 75%
   Status: In Progress | Waves: 3/4 complete

🚀 Authentication System: 100%
   Status: Complete | Waves: 2/2 complete

📱 Mobile Responsive: 40%
   Status: In Progress | Waves: 1/3 complete
```

### Step 5: Display Session Context

Show current session information:
- Latest checkpoint (if exists)
- Active wave (if in wave execution)
- Project memory status
- Session duration

### Step 6: Display Documentation Links

```
───────────────────────────────────────────────────────────────
📚 DOCUMENTATION
───────────────────────────────────────────────────────────────

• Installation: docs/PLUGIN_INSTALL.md
• Commands: SHANNON_COMMANDS_GUIDE.md
• Specification: SHANNON_V3_SPECIFICATION.md
• Migration: docs/MIGRATION_GUIDE.md
```

### Step 7: Assemble Complete Status Report

Combine all sections into final output:

```
═══════════════════════════════════════════════════════════════
🌊 SHANNON FRAMEWORK STATUS
═══════════════════════════════════════════════════════════════

VERSION: v4.0.0
STATUS: ✅ ACTIVE | Installation: Plugin System

[MCP Status Section - if --mcps]
[Commands & Agents Section - always]
[Active Goals Section - if --goals]
[Session Context Section - always]
[Documentation Section - always]

═══════════════════════════════════════════════════════════════
```

## Skill Dependencies

- mcp-discovery (OPTIONAL) - Mode: health-check (only if --mcps flag)
- goal-management (OPTIONAL) - Mode: list (only if --goals flag)

## MCP Dependencies

- Serena MCP (recommended for session context and goals)

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same basic output structure
- Enhanced with optional --mcps and --goals flags

**Changes from V3:**
- Internal: Now orchestrates skills (was monolithic)
- Enhancement: --mcps flag for detailed MCP status
- Enhancement: --goals flag for active goals display
- Enhancement: Better session context detection
- No breaking changes

## Usage Examples

**Standard Status:**
```bash
/shannon:status
```

**Status with MCP Check:**
```bash
/shannon:status --mcps
```

**Status with Goals:**
```bash
/shannon:status --goals
```

**Full Status Report:**
```bash
/shannon:status --mcps --goals --verbose
```

## When to Use

- **After installation**: First command to verify setup
- **Debugging**: When Shannon commands aren't working
- **Regular health checks**: Ensure all systems operational
- **Before starting complex work**: Verify context preservation is active
- **Goal tracking**: Monitor progress on active goals

## Related Commands

- `/shannon:check_mcps` - Detailed MCP setup guidance
- `/help` - Full command catalog
- `/agents` - Agent capabilities

## Troubleshooting

If status shows issues:

**Serena Not Connected**:
1. Run /shannon:check_mcps for setup instructions
2. Configure Serena in Claude Code settings
3. Restart Claude Code
4. Run /shannon:status again to verify

**Commands Not Showing**:
1. Verify plugin installed: /plugin
2. Check plugin enabled
3. Restart Claude Code if needed

**Agents Not Available**:
1. Check /agents to see all available agents
2. Shannon agents should appear with descriptions
3. If missing, reinstall plugin
