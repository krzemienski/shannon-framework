#!/usr/bin/env python3
"""
Check what commands are available after loading Shannon plugin
"""

import os
import sys
import asyncio

os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, AssistantMessage, TextBlock

async def main():
    print("Checking Shannon plugin commands...")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        permission_mode="bypassPermissions"
    )

    async for message in query(prompt="hello", options=options):
        if isinstance(message, SystemMessage):
            if message.subtype == 'init':
                print("\nSystemMessage init data:")
                for key in message.data.keys():
                    print(f"  {key}: {message.data[key]}")

                if 'slash_commands' in message.data:
                    commands = message.data['slash_commands']
                    print(f"\nSlash commands available: {len(commands)}")
                    for cmd in commands[:20]:  # First 20
                        print(f"  /{cmd}")

                if 'plugins' in message.data:
                    plugins = message.data['plugins']
                    print(f"\nPlugins loaded: {plugins}")

        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\nClaude response: {block.text[:100]}...")

    return 0

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
