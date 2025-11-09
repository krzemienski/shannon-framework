#!/usr/bin/env python3
"""
Test if Shannon commands work via SDK at all
"""

import os
import sys
import asyncio
from pathlib import Path

os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, SystemMessage, ResultMessage, TextBlock, ToolUseBlock

async def main():
    print("Testing Shannon command execution via SDK")
    print("=" * 80)

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        permission_mode="bypassPermissions"
    )

    # Try different Shannon commands
    commands = [
        "/sh_status",
        "/shannon:prime",
        "/sh_spec 'Build a simple web form with React'",
    ]

    for cmd in commands:
        print(f"\n\nTesting: {cmd}")
        print("-" * 80)

        text_output = []
        tools = []

        try:
            async for message in query(prompt=cmd, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            text_output.append(block.text)
                        elif isinstance(block, ToolUseBlock):
                            tools.append(block.name)

                elif isinstance(message, SystemMessage):
                    if message.subtype == 'init' and 'plugins' in message.data:
                        print(f"Plugins loaded: {message.data['plugins']}")

                elif isinstance(message, ResultMessage):
                    print(f"Cost: ${message.total_cost_usd or 0:.4f}")

            output = ''.join(text_output)
            print(f"Output length: {len(output)}")
            print(f"Tools called: {len(tools)}")

            if output:
                print(f"Output preview:\n{output[:300]}...")
            else:
                print("❌ NO OUTPUT")

        except Exception as e:
            print(f"ERROR: {e}")

    return 0

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
