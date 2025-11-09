#!/usr/bin/env python3
"""
Check message.data['type'] vs isinstance()
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, AssistantMessage
import asyncio

async def main():
    print("Checking message.data['type'] values...")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}]
    )

    count = 0
    async for message in query(prompt="hello", options=options):
        count += 1
        print(f"\n--- Message {count} ---")

        if isinstance(message, SystemMessage):
            print(f"Class: SystemMessage")
            print(f"message.data['type']: {message.data.get('type')}")
            print(f"message.subtype: {message.subtype}")

            if message.subtype == 'init':
                print(f"\nPlugins loaded: {message.data.get('plugins')}")
                print(f"Slash commands: {len(message.data.get('slash_commands', []))}")

        elif isinstance(message, AssistantMessage):
            print(f"Class: AssistantMessage")
            if hasattr(message, 'data'):
                print(f"Has data: {message.data}")

        if count >= 3:
            break

    return 0

if __name__ == '__main__':
    asyncio.run(main())
