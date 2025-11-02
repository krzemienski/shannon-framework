---
activates:
- ANALYZER
- ORCHESTRATOR
base: SuperClaude /select-tool command
category: command
command: /sc:select-tool
complexity: low-to-moderate
description: Intelligent tool and MCP server selection with Shannon MCP awareness
enhancement: Shannon V3 MCP matrix + dynamic server suggestions
mcp-servers:
- serena
name: sc:select_tool
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
tools:
- Read
- Grep
- Glob
wave-enabled: false
---

/sc:select-tool - Intelligent Tool Selection Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

> **Enhanced from SuperClaude's `/select-tool` command with Shannon V3 MCP server awareness, comprehensive tool selection matrix, and intelligent recommendations based on operation context.**

## Usage Patterns

### Basic Usage

```bash
# Get tool recommendations for an operation
/sc:select-tool "analyze authentication flow"

# Get MCP server suggestions for testing
/sc:select-tool "E2E test user registration" --focus mcp

# Compare tool options
/sc:select-tool "bulk rename functions" --compare

# Get recommendations with examples
/sc:select-tool "research best practices" --examples
```

##

## Skill Integration

**v4 NEW**: This command activates skills:


## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
