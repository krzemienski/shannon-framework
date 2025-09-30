# Shannon Framework V3 - Project Configuration

<!--
  This CLAUDE.md activates Shannon behavioral patterns for THIS project only.

  Project-level CLAUDE.md files override user-level ~/.claude/ instructions
  for files within this project directory. This prevents global pollution
  while enabling Shannon's specialized behavioral patterns for Shannon projects.

  When Claude Code operates on Shannon files, it automatically loads this
  configuration and activates Shannon-specific behaviors, commands, agents,
  and execution modes.
-->

# ═══════════════════════════════════════════════════
# Shannon Framework Core Components
# ═══════════════════════════════════════════════════

## Core Behavioral Patterns

@Shannon/Core/SPEC_ANALYSIS.md
@Shannon/Core/PHASE_PLANNING.md
@Shannon/Core/WAVE_ORCHESTRATION.md
@Shannon/Core/CONTEXT_MANAGEMENT.md
@Shannon/Core/TESTING_PHILOSOPHY.md
@Shannon/Core/HOOK_SYSTEM.md
@Shannon/Core/PROJECT_MEMORY.md
@Shannon/Core/MCP_DISCOVERY.md

# ═══════════════════════════════════════════════════
# Shannon Sub-Agents
# ═══════════════════════════════════════════════════

## New Shannon Agents (5)

@Shannon/Agents/SPEC_ANALYZER.md
@Shannon/Agents/PHASE_ARCHITECT.md
@Shannon/Agents/WAVE_COORDINATOR.md
@Shannon/Agents/CONTEXT_GUARDIAN.md
@Shannon/Agents/TEST_GUARDIAN.md

## Enhanced SuperClaude Agents (14)

@Shannon/Agents/IMPLEMENTATION_WORKER.md
@Shannon/Agents/ANALYZER.md
@Shannon/Agents/ARCHITECT.md
@Shannon/Agents/REFACTORER.md
@Shannon/Agents/SECURITY.md
@Shannon/Agents/FRONTEND.md
@Shannon/Agents/BACKEND.md
@Shannon/Agents/PERFORMANCE.md
@Shannon/Agents/DEVOPS.md
@Shannon/Agents/QA.md
@Shannon/Agents/MENTOR.md
@Shannon/Agents/SCRIBE.md
@Shannon/Agents/DATA_ENGINEER.md
@Shannon/Agents/MOBILE_DEVELOPER.md

# ═══════════════════════════════════════════════════
# Shannon Commands
# ═══════════════════════════════════════════════════

## New Shannon Commands (4)

@Shannon/Commands/sh_spec.md
@Shannon/Commands/sh_checkpoint.md
@Shannon/Commands/sh_restore.md
@Shannon/Commands/sh_status.md

## Enhanced SuperClaude Commands (25)

@Shannon/Commands/sc_analyze.md
@Shannon/Commands/sc_brainstorm.md
@Shannon/Commands/sc_build.md
@Shannon/Commands/sc_business_panel.md
@Shannon/Commands/sc_cleanup.md
@Shannon/Commands/sc_design.md
@Shannon/Commands/sc_document.md
@Shannon/Commands/sc_estimate.md
@Shannon/Commands/sc_explain.md
@Shannon/Commands/sc_git.md
@Shannon/Commands/sc_help.md
@Shannon/Commands/sc_implement.md
@Shannon/Commands/sc_improve.md
@Shannon/Commands/sc_index.md
@Shannon/Commands/sc_load.md
@Shannon/Commands/sc_reflect.md
@Shannon/Commands/sc_research.md
@Shannon/Commands/sc_save.md
@Shannon/Commands/sc_select_tool.md
@Shannon/Commands/sc_spawn.md
@Shannon/Commands/sc_spec_panel.md
@Shannon/Commands/sc_task.md
@Shannon/Commands/sc_test.md
@Shannon/Commands/sc_troubleshoot.md
@Shannon/Commands/sc_workflow.md

# ═══════════════════════════════════════════════════
# Shannon Execution Modes
# ═══════════════════════════════════════════════════

@Shannon/Modes/WAVE_EXECUTION.md
@Shannon/Modes/SHANNON_INTEGRATION.md

# ═══════════════════════════════════════════════════
# Required MCP Servers
# ═══════════════════════════════════════════════════

## Critical MCP Servers (Shannon Framework Requirements)

Shannon Framework requires these MCP servers to be configured for full functionality:

### 1. Serena MCP (MANDATORY)
**Purpose**: Context preservation, memory management, checkpoint/restore
**Why Required**: Shannon's core context preservation system depends on Serena
**Configuration**: Must be configured in Claude Code settings

### 2. shadcn MCP (MANDATORY for React/Next.js UI)
**Purpose**: React/Next.js UI components and blocks from shadcn/ui library
**Why Required**: Shannon enforces shadcn/ui for ALL React UI work
**Package**: @jpisnice/shadcn-ui-mcp-server
**Configuration**:
```json
{
  "mcpServers": {
    "shadcn-ui": {
      "command": "npx",
      "args": ["@jpisnice/shadcn-ui-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

**MCP Tools Provided**:
- `get_component(name)` - Get component source code
- `list_components()` - Browse all shadcn components
- `get_block(name)` - Get pre-built block implementations
- `list_blocks()` - Browse all shadcn blocks
- `get_component_demo(name)` - View component usage examples

**Why Shannon Enforces shadcn**:
- Accessible by default (Radix UI primitives)
- Production-ready (battle-tested by major companies)
- Customizable (copied into your project)
- Type-safe (TypeScript-first)
- NO MOCKS testable (real Puppeteer tests)

### 3. Sequential MCP (Recommended)
**Purpose**: Complex multi-step reasoning and analysis
**Why Recommended**: Enhances specification analysis and planning
**Configuration**: Recommended for best Shannon experience

### 4. Puppeteer MCP (Recommended for Testing)
**Purpose**: Real browser testing for web applications
**Why Recommended**: NO MOCKS testing philosophy requires real browsers
**Configuration**: Required for web UI testing workflows

### 5. Context7 MCP (Recommended)
**Purpose**: Official library documentation and patterns
**Why Recommended**: Provides React, Next.js, and framework-specific patterns
**Configuration**: Enhances development with official documentation

## MCP Configuration Guide

See `docs/SHADCN_INTEGRATION.md` for complete shadcn MCP setup instructions.

For other MCP servers, refer to user-level ~/.claude/ configuration.

# ═══════════════════════════════════════════════════
# Activation & Configuration
# ═══════════════════════════════════════════════════

## How Shannon Activates

When Claude Code operates on files within `/Users/nick/Documents/shannon/`:
1. This CLAUDE.md is automatically loaded
2. Shannon behavioral patterns activate
3. Shannon commands become available (/sh:* commands)
4. Sub-agents are accessible for delegation
5. Wave execution mode is enabled
6. shadcn MCP enforced for React UI work

## Verification

To verify Shannon is active in your Claude Code session:

```bash
# Check Shannon commands are available
/sh:status

# Verify shadcn MCP is configured
# Should show shadcn MCP server in available tools

# Test specification analysis
/sh:spec "Build a simple todo app"
# Should produce 8-dimensional complexity analysis
```

## Configuration Hierarchy

1. **Project-Level** (this file): Active for Shannon project files
2. **User-Level** (~/.claude/): Fallback for non-Shannon work
3. **Global Defaults**: Claude Code base behavior

This hierarchy ensures Shannon patterns activate ONLY for Shannon work,
preventing behavioral pollution in other projects.

## Integration with SuperClaude

Shannon V3 is designed to complement SuperClaude framework:
- Shannon commands integrate with `/sc:*` commands
- Sub-agents work alongside SuperClaude personas
- Wave execution coordinates with SuperClaude orchestration
- Quality gates align with SuperClaude validation
- **shadcn MCP**: Used by Shannon for React UI (replaces Magic MCP)

Both frameworks can be active simultaneously, with Shannon handling
spec-driven development workflows and SuperClaude managing general
engineering operations.

## Important Notes

- **React/Next.js UI**: Shannon REQUIRES shadcn MCP and FORBIDS Magic MCP
- **Other Frameworks**: Magic MCP still available for Vue, Angular, Svelte
- **NO MOCKS Philosophy**: All tests use real browsers, simulators, databases
- **Context Preservation**: PreCompact hook requires Serena MCP configuration