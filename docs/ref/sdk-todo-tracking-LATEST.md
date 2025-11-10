# Todo Tracking in Claude Agent SDK

Track and display todos using the Claude Agent SDK for organized task management.

## Overview

The Agent SDK provides access to Claude Code's todo system for tracking tasks programmatically.

## Usage

TodoWrite tool available in SDK with same interface as Claude Code CLI.

## Configuration

No special configuration needed - TodoWrite tool available by default when using Claude Agent SDK.

## Monitoring Todos

**Python:**
```python
from claude_agent_sdk import query, AssistantMessage, ToolUseBlock

async for message in query(
    prompt="Build app with todo tracking",
    options={"max_turns": 15}
):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock) and block.name == "TodoWrite":
                todos = block.input["todos"]
                for i, todo in enumerate(todos):
                    status = "✅" if todo["status"] == "completed" else \
                            "🔧" if todo["status"] == "in_progress" else "❌"
                    print(f"{i + 1}. {status} {todo['content']}")
```
