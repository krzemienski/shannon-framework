# Slash Commands in the Agent SDK - Complete Reference

## Overview
"Slash commands provide a way to control Claude Code sessions with special commands that start with `/`". They enable actions like clearing conversation history, compacting messages, or obtaining assistance.

## Discovering Commands

The system initialization message reveals available slash commands:

```python
import asyncio
from claude_agent_sdk import query

async def main():
    async for message in query(
        prompt="Hello Claude",
        options={"max_turns": 1}
    ):
        if message.type == "system" and message.subtype == "init":
            print("Available slash commands:", message.slash_commands)

asyncio.run(main())
```

## Sending Slash Commands

Commands are transmitted by including them within your prompt string:

```python
import asyncio
from claude_agent_sdk import query

async def main():
    async for message in query(
        prompt="/compact",
        options={"max_turns": 1}
    ):
        if message.type == "result":
            print("Command executed:", message.result)

asyncio.run(main())
```

## Built-in Commands

### `/compact` - Reduce Conversation History
### `/clear` - Start Fresh Session

## Custom Slash Commands

### Storage Locations

"Custom slash commands are stored in designated directories based on their scope":

- **Project commands**: `.claude/commands/` directory
- **Personal commands**: `~/.claude/commands/` directory

### Basic Structure

"The filename (without `.md` extension) becomes the command name" and "The file content defines what the command does".
