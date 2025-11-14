# Custom Tools in Claude Agent SDK

Build custom tools to extend Claude Code's capabilities through in-process MCP servers.

## Creating Tools

**Python:**
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
            "text": f"Temperature: 72°F"
        }]
    }

server = create_sdk_mcp_server(
    name="weather",
    version="1.0.0",
    tools=[get_weather]
)
```

## Using Custom Tools

**IMPORTANT:** Custom MCP tools require ClaudeSDKClient (streaming mode).

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers={"weather": server},
    allowed_tools=["mcp__weather__get_weather"]
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("What's the weather in SF?")
    async for msg in client.receive_response():
        print(msg)
```

## Tool Name Format

Pattern: `mcp__{server_name}__{tool_name}`

Example: `get_weather` in `my-tools` → `mcp__my-tools__get_weather`
