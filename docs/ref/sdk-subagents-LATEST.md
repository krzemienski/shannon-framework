# Subagents in the SDK

Subagents are specialized AIs orchestrated by the main agent.

## Two Definition Approaches

1. **Programmatic** (recommended): Using `agents` parameter
2. **Filesystem**: Markdown files in `.claude/agents/`

## Benefits

- **Context Management**: Separate context from main agent
- **Parallelization**: Multiple subagents run concurrently
- **Specialized Instructions**: Tailored system prompts
- **Tool Restrictions**: Limited to specific tools

## Programmatic Definition

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Review authentication module",
    options=ClaudeAgentOptions(
        agents={
            'code-reviewer': {
                'description': 'Expert code review specialist',
                'prompt': 'You are a code reviewer...',
                'tools': ['Read', 'Grep', 'Glob'],
                'model': 'sonnet'
            }
        }
    )
):
    print(message)
```

## AgentDefinition Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | Yes | When to use this agent |
| `prompt` | string | Yes | System prompt |
| `tools` | string[] | No | Allowed tools (inherits all if omitted) |
| `model` | 'sonnet'\|'opus'\|'haiku'\|'inherit' | No | Model override |
