# Custom Tools in Claude Agent SDK

## Overview
Custom tools extend Claude Code's capabilities through in-process MCP servers.

## Core Concepts

**Creating Tools**: Use `createSdkMcpServer` and `tool` helper functions for type-safe custom tools.

**Tool Naming**: MCP tools follow pattern `mcp__{server_name}__{tool_name}`

## Key Requirements

**Streaming Input Mode**: "Custom MCP tools require streaming input mode."

**Configuration**: Pass custom servers via `mcpServers` as dictionary.

## Python Implementation Example

```python
from claude_agent_sdk import tool, create_sdk_mcp_server
from typing import Any

@tool("get_weather", "Get temperature for location",
      {"latitude": float, "longitude": float})
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    # Implementation
    return {
        "content": [{
            "type": "text",
            "text": f"Temperature: {temp}°F"
        }]
    }

custom_server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[get_weather]
)
```

## Error Handling Pattern

Tools should return error messages within content structure rather than raising exceptions.
