# Plugins in the Agent SDK

## Overview
Plugins allow you to extend Claude Code with custom functionality that can be shared across projects. Through the Agent SDK, developers can programmatically load plugins from local directories to add custom slash commands, agents, skills, hooks, and MCP servers.

## Plugin Components
Plugins are packages that can include custom slash commands, specialized subagents, model-invoked capabilities, event handlers, and external tool integrations via Model Context Protocol.

## Loading Plugins - Python Example
```python
import asyncio
from claude_agent_sdk import query

async def main():
    async for message in query(
        prompt="Hello",
        options={
            "plugins": [
                {"type": "local", "path": "./my-plugin"},
                {"type": "local", "path": "/absolute/path/to/another-plugin"}
            ]
        }
    ):
        pass

asyncio.run(main())
```

## Path Specifications
Plugin paths can be relative (resolved from current working directory) or absolute (full file system paths). The path should point to the plugin's root directory (the directory containing `.claude-plugin/plugin.json`).

## Verification - Python Example
```python
import asyncio
from claude_agent_sdk import query

async def main():
    async for message in query(
        prompt="Hello",
        options={"plugins": [{"type": "local", "path": "./my-plugin"}]}
    ):
        if message.type == "system" and message.subtype == "init":
            print("Plugins:", message.data.get("plugins"))
            print("Commands:", message.data.get("slash_commands"))

asyncio.run(main())
```

## Using Plugin Commands - Python Example
```python
import asyncio
from claude_agent_sdk import query, AssistantMessage, TextBlock

async def main():
    async for message in query(
        prompt="/demo-plugin:greet",
        options={"plugins": [{"type": "local", "path": "./plugins/demo-plugin"}]}
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")

asyncio.run(main())
```

## Complete Example - Python
```python
#!/usr/bin/env python3
"""Example demonstrating how to use plugins with the Agent SDK."""

from pathlib import Path
import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    query,
)

async def run_with_plugin():
    """Example using a custom plugin."""
    plugin_path = Path(__file__).parent / "plugins" / "demo-plugin"
    print(f"Loading plugin from: {plugin_path}")

    options = ClaudeAgentOptions(
        plugins=[
            {"type": "local", "path": str(plugin_path)}
        ],
        max_turns=3,
    )

    async for message in query(
        prompt="What custom commands do you have available?",
        options=options
    ):
        if message.type == "system" and message.subtype == "init":
            print(f"Loaded plugins: {message.data.get('plugins')}")
            print(f"Available commands: {message.data.get('slash_commands')}")

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Assistant: {block.text}")

if __name__ == "__main__":
    anyio.run(run_with_plugin)
```

## Plugin Directory Structure
A plugin requires `.claude-plugin/plugin.json` and may optionally include commands, agents, skills, hooks, and MCP configurations.

## Common Use Cases
Plugins support development/testing without global installation, project-specific extensions for team consistency, and combining plugins from multiple locations.

## Troubleshooting Guidance
Check that paths point to plugin root directories, validate plugin.json syntax, ensure file permissions are readable, use the `plugin-name:command-name` namespace format, verify commands appear in initialization messages, and use absolute paths for reliability.
