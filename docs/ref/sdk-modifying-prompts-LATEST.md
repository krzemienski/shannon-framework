# Modifying System Prompts in Claude Agent SDK

Four approaches to customize Claude's behavior.

## Method 1: CLAUDE.md Files

**CRITICAL:** Requires `setting_sources=["project"]` to load.

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Add React component",
    options=ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code"
        },
        setting_sources=["project"]  # REQUIRED to load CLAUDE.md!
    )
):
    print(message)
```

**Important:** The `claude_code` preset does NOT automatically load CLAUDE.md - must specify `setting_sources`.

## Method 2: systemPrompt with Append

```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "Always include docstrings and type hints."
    }
)
```

## Method 3: Custom System Prompts

```python
custom_prompt = "You are a Python specialist..."

options = ClaudeAgentOptions(
    system_prompt=custom_prompt
)
```

## Comparison

| Feature | CLAUDE.md | systemPrompt append | Custom |
|---------|-----------|---------------------|--------|
| Persistence | Per-project file | Session only | Session only |
| Requires setting_sources | ✅ Yes | ❌ No | ❌ No |
| Default tools | ✅ Preserved | ✅ Preserved | ❌ Lost |
