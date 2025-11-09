#!/usr/bin/env python3
"""
Test if Shannon commands need plugin namespace prefix
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, SystemMessage
import asyncio

async def test_command_variants():
    """Try different command formats"""

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        permission_mode="bypassPermissions"
    )

    # Test variants
    commands = [
        "/sh_spec 'Build React app'",           # Without namespace
        "/shannon:sh_spec 'Build React app'",   # With shannon namespace
        "shannon:sh_spec 'Build React app'",    # Without slash
    ]

    for cmd in commands:
        print(f"\n{'='*80}")
        print(f"Testing: {cmd}")
        print('='*80)

        text_output = []

        try:
            async for message in query(prompt=cmd, options=options):
                if isinstance(message, SystemMessage) and message.subtype == 'init':
                    if 'slash_commands' in message.data:
                        cmds = message.data['slash_commands']
                        shannon_cmds = [c for c in cmds if 'sh_' in c or 'shannon' in c]
                        print(f"Shannon commands found: {shannon_cmds[:5]}")

                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            text_output.append(block.text)

        except Exception as e:
            print(f"Error: {e}")

        output = ''.join(text_output)

        if output:
            print(f"✅ Got output ({len(output)} chars)")
            print(f"Preview: {output[:150]}...")
        else:
            print("❌ No output")

    return 0

if __name__ == '__main__':
    asyncio.run(test_command_variants())
