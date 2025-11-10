#!/usr/bin/env python3
"""
Debug: Check if Shannon plugin actually loads via SDK
"""

import os
import sys
import asyncio

if 'ANTHROPIC_API_KEY' not in os.environ:
    raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, AssistantMessage, TextBlock

async def debug_loading():
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        setting_sources=["user", "project"],
        permission_mode="bypassPermissions",
        max_turns=1
    )

    print("Testing plugin loading...")

    async for message in query(prompt="hello", options=options):
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            print(f"\nSystemMessage init data:")
            print(f"  plugins: {message.data.get('plugins', [])}")
            print(f"  slash_commands: {len(message.data.get('slash_commands', []))}")

            commands = message.data.get('slash_commands', [])
            shannon_cmds = [c for c in commands if 'sh_' in c or 'shannon' in c]
            print(f"  Shannon commands: {shannon_cmds}")

        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\nResponse: {block.text}")

if __name__ == '__main__':
    asyncio.run(debug_loading())
