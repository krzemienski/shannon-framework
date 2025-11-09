#!/usr/bin/env python3
"""
Test if setting_sources is needed for plugin loading

From skills.md: "By default, the SDK does not load any filesystem settings.
To use Skills, you must explicitly configure setting_sources=['user', 'project']"

Maybe plugins need same?
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, AssistantMessage, TextBlock
import asyncio

async def main():
    print("Testing plugin loading WITH setting_sources...")
    print("=" * 80)

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        setting_sources=["user", "project", "local"],  # Add this!
        permission_mode="bypassPermissions",
        allowed_tools=["Skill"]  # Also enable Skill tool
    )

    async for message in query(prompt="hello", options=options):
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            print(f"\n✅ Session initialized")
            print(f"Plugins: {message.data.get('plugins')}")
            print(f"Skills: {len(message.data.get('skills', []))}")

            slash_cmds = message.data.get('slash_commands', [])
            shannon_cmds = [c for c in slash_cmds if 'sh_' in c or 'shannon' in c]

            print(f"\nTotal slash commands: {len(slash_cmds)}")
            print(f"Shannon commands: {shannon_cmds}")

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\nResponse: {block.text[:200]}...")

    return 0

if __name__ == '__main__':
    asyncio.run(main())
