#!/usr/bin/env python3
"""
Debug: Print actual claude CLI command that SDK executes

Add instrumentation to see what command SDK builds
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

# Monkey-patch SDK to show command
import claude_agent_sdk._internal.transport.subprocess_cli as subprocess_cli

original_build_command = subprocess_cli.SubprocessCLITransport._build_command

def debug_build_command(self):
    """Wrapped _build_command that prints the command"""
    cmd = original_build_command(self)

    print("\n" + "=" * 80)
    print("SDK COMMAND DEBUG")
    print("=" * 80)
    print("Command parts:")
    for i, part in enumerate(cmd):
        print(f"  [{i}] {part}")
    print("\nFull command:")
    print(" ".join(cmd))
    print("=" * 80 + "\n")

    return cmd

subprocess_cli.SubprocessCLITransport._build_command = debug_build_command

# Now run normal test
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
import asyncio

async def main():
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        permission_mode="bypassPermissions"
    )

    print("Executing query with Shannon plugin...")

    async for message in query(prompt="hello", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Response: {block.text[:100]}...")

    return 0

if __name__ == '__main__':
    asyncio.run(main())
