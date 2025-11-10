# Session Management in Claude Agent SDK

## Core Functionality

"Sessions allow you to continue conversations across multiple interactions while maintaining full context."

## Obtaining Session IDs

Sessions are automatically created. The SDK returns session identifier in initial system message.

**Python implementation:**
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

## Resuming Previous Conversations

The `resume` parameter allows reconnection to prior sessions with full context preservation.

**Python resumption:**
```python
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

The `fork_session` parameter creates independent branches from existing sessions.
