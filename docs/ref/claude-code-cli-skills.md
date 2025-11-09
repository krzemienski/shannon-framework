# Claude Code CLI Skills - Complete Content

## Overview
Skills extend Claude's capabilities through organized folders containing instructions, scripts, and resources. They are **model-invoked** (Claude autonomously decides when to use them).

## Skill Types

**Personal Skills** (`~/.claude/skills/`): Individual workflows
**Project Skills** (`.claude/skills/`): Team workflows checked into git
**Plugin Skills**: Bundled with installed plugins

## Core Requirements

SKILL.md structure:
- `name`: lowercase letters, numbers, hyphens only (max 64 characters)
- `description`: What Skill does and when to use it (max 1024 characters)

## Key Features

**Supporting Files**: Reference docs, examples, scripts alongside SKILL.md
**Tool Restrictions**: Use `allowed-tools` frontmatter to limit tools
**Discovery**: Automatically discovered from three sources

## Common Issues

- Vague descriptions prevent discovery
- Invalid YAML syntax prevents loading
- Incorrect file paths
- Missing dependencies

Run `claude --debug` for error visibility.

## Sharing

**Recommended**: Distribute through plugins
**Alternative**: Commit project Skills to git
