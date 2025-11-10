# Claude Code CLI Slash Commands - Complete Content

## Overview
Slash commands control Claude's behavior during interactive sessions.

## Built-in Commands (33)

**Session**: /exit, /clear, /rewind
**Configuration**: /config, /model, /login, /logout
**Information**: /help, /status, /cost, /usage, /context
**Code Review**: /review, /bug
**Management**: /compact, /export, /memory, /todos
**Advanced**: /sandbox, /vim, /agents, /hooks, /mcp

## Custom Slash Commands

**Storage Locations**:
- Project: `.claude/commands/`
- Personal: `~/.claude/commands/`

**Syntax**: `/<command-name> [arguments]`

### Features

**Arguments**:
- `$ARGUMENTS` - All arguments
- `$1`, `$2` - Individual positions
- `argument-hint` frontmatter for autocomplete

**Bash Integration**: "!" prefix executes shell
**File References**: "@" prefix includes file contents
**Thinking Mode**: Keywords trigger extended thinking

### Frontmatter Options

| Field | Purpose |
|-------|---------|
| `allowed-tools` | Tools available |
| `argument-hint` | Autocomplete help |
| `description` | Brief description |
| `model` | Specific model |
| `disable-model-invocation` | Prevents SlashCommand tool |

## Plugin Commands

Format: `/plugin-name:command-name`
Distribute via marketplaces

## MCP Slash Commands

Format: `/mcp__<server>__<prompt> [args]`
Dynamically discovered from MCP servers

## SlashCommand Tool

Claude executes custom commands programmatically.

## Slash Commands vs. Skills

**Commands**: Simple prompts, direct invocation
**Skills**: Complex capabilities, auto-discovery
