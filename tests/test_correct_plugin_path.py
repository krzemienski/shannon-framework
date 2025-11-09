#!/usr/bin/env python3
"""
Test Shannon with CORRECT plugin path (.claude/plugins/shannon)
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, AssistantMessage, TextBlock
import asyncio

async def main():
    print("Testing Shannon with CORRECT path...")
    print("=" * 80)

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": ".claude/plugins/shannon"}],  # CORRECT path!
        setting_sources=["user", "project"],  # Load filesystem settings
        permission_mode="bypassPermissions"
    )

    async for message in query(prompt="/sh_spec 'Build React app'", options=options):
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            print(f"Plugins: {message.data.get('plugins')}")

            slash_cmds = message.data.get('slash_commands', [])
            shannon_cmds = [c for c in slash_cmds if 'sh_' in c or 'shannon' in c]

            print(f"Shannon commands: {shannon_cmds}")

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\n{block.text}")

    return 0

if __name__ == '__main__':
    asyncio.run(main())
