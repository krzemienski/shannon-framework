# Claude Agent SDK: Streaming Input Overview

## Core Distinction

The Claude Agent SDK provides two input approaches:

**Streaming Input Mode** is presented as the default and recommended option, functioning as "a persistent, interactive session" that maintains conversation context across multiple turns.

**Single Message Input** operates differently—it delivers "one-shot queries that use session state and resuming," suitable for stateless environments like Lambda functions.

## Streaming Input Capabilities

Streaming mode enables several advanced features including image attachments, sequential message processing with interruption capability, tool integration, lifecycle hooks, real-time response generation, and natural conversation continuity.

### Python Implementation Example

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock
import asyncio

async def streaming_analysis():
    options = ClaudeAgentOptions(
        max_turns=10,
        allowed_tools=["Read", "Grep"]
    )

    async with ClaudeSDKClient(options) as client:
        await client.query("Analyze this codebase")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)

asyncio.run(streaming_analysis())
```

## Single Message Input Limitations

Single message input explicitly does not support "direct image attachments in messages, dynamic message queueing, real-time interruption, hook integration, [or] natural multi-turn conversations."
