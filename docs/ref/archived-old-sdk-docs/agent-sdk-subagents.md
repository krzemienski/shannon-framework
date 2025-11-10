# Subagents in the Claude Agent SDK - Complete Content

## Overview

"Specialized AIs that are orchestrated by the main agent" with two definition approaches: programmatically (recommended) via the `agents` parameter, or filesystem-based using markdown files in `.claude/agents/`.

## Key Benefits

**Context Management**: Subagents maintain isolated contexts
**Parallelization**: Multiple subagents execute concurrently
**Specialized Instructions**: Tailored system prompts
**Tool Restrictions**: Limited to specific tools

## Programmatic Definition (TypeScript)

```typescript
const result = query({
  prompt: "Review the authentication module",
  options: {
    agents: {
      'code-reviewer': {
        description: 'Expert code review specialist',
        prompt: `You are a code reviewer...`,
        tools: ['Read', 'Grep', 'Glob'],
        model: 'sonnet'
      }
    }
  }
});
```

## AgentDefinition Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | `string` | Yes | When to use this agent |
| `prompt` | `string` | Yes | System prompt |
| `tools` | `string[]` | No | Allowed tools |
| `model` | `'sonnet'\|'opus'\|'haiku'\|'inherit'` | No | Model override |

## Filesystem-Based Definition

Create markdown files in `.claude/agents/` with YAML frontmatter.

**Note**: "Programmatically defined agents take precedence over filesystem-based agents with the same name."
