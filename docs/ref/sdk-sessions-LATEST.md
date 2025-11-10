# Session Management in Claude Agent SDK

Sessions allow you to continue conversations across multiple interactions while maintaining full context.

## Getting Session ID

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

session_id = None

async for message in query(
    prompt="Help me build a web application",
    options=ClaudeAgentOptions(model="claude-sonnet-4-5")
):
    if hasattr(message, 'subtype') and message.subtype == 'init':
        session_id = message.data.get('session_id')
        print(f"Session: {session_id}")
```

## Resuming Sessions

```python
# Resume previous session
async for message in query(
    prompt="Continue implementing authentication",
    options=ClaudeAgentOptions(
        resume="session-xyz",
        model="claude-sonnet-4-5"
    )
):
    print(message)
```

## Session Forking

Create independent branches from existing sessions:

```python
async for message in query(
    prompt="Try a different approach",
    options=ClaudeAgentOptions(
        resume=session_id,
        fork_session=True,  # Creates new session ID
        model="claude-sonnet-4-5"
    )
):
    print(message)
```

| Behavior | `fork_session=False` (default) | `fork_session=True` |
|----------|-------------------------------|---------------------|
| Session ID | Same as original | New session ID |
| History | Appends to original | Creates new branch |
| Original Session | Modified | Preserved unchanged |
