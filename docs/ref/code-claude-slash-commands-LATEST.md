# Slash Commands in Claude Code

Control Claude's behavior with commands starting with `/`.

## Built-in Commands

| Command | Purpose |
|---------|---------|
| `/compact` | Compact conversation history |
| `/clear` | Clear conversation |
| `/help` | Get usage help |
| `/plugin` | Manage plugins |
| `/mcp` | Manage MCP servers |
| `/todos` | List todos |

## Custom Slash Commands

### Locations

- **Project**: `.claude/commands/` (shared via git)
- **Personal**: `~/.claude/commands/` (personal only)

### File Format

Filename (without `.md`) becomes command name.

**Basic example** (`.claude/commands/optimize.md`):
```markdown
Analyze this code for performance issues and suggest optimizations.
```

Creates `/optimize` command.

**With frontmatter** (`.claude/commands/fix-issue.md`):
```markdown
---
description: Fix GitHub issue
argument-hint: [issue-number] [priority]
allowed-tools: Read, Write, Bash
---

Fix issue #$1 with priority $2.
Check issue description and implement changes.
```

### Features

**Arguments:**
- `$ARGUMENTS` - All arguments
- `$1`, `$2`, etc. - Individual arguments

**Bash execution:**
```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

Current status: !`git status`
Changes: !`git diff HEAD`
```

**File references:**
```markdown
Review @src/utils/helpers.js
```

## Skills vs Slash Commands

| Aspect | Slash Commands | Skills |
|--------|---------------|--------|
| Invocation | Manual (`/command`) | Automatic (model-invoked) |
| Complexity | Simple prompts | Complex workflows |
| Structure | Single .md file | Directory with resources |
| Files | One file only | Multiple files, scripts |
