#!/usr/bin/env python3
"""
Minimal SDK test - Verify Shannon plugin loads and responds

Based on OFFICIAL python-agent-sdk.md documentation (1847 lines read completely).
This uses the CORRECT API with isinstance() checks, not the wrong message.type pattern.
"""

import os
import sys
import asyncio
from pathlib import Path

# CRITICAL: Set API key BEFORE importing SDK
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

# Import SDK types (AFTER setting API key)
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock
)

async def main():
    print("=" * 80)
    print("MINIMAL SDK TEST - Shannon Plugin Loading")
    print("=" * 80)

    # Verify plugin exists
    plugin_path = Path("./shannon-plugin")
    if not plugin_path.exists():
        print(f"❌ Plugin not found: {plugin_path.absolute()}")
        return 1

    print(f"✅ Plugin directory: {plugin_path.absolute()}")

    # Load Shannon plugin
    print("\nLoading Shannon plugin...")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(plugin_path)}],
        permission_mode="bypassPermissions"
    )

    # Simple test query
    print("Executing test query...")

    text_output = []
    tools_called = []
    session_id = None
    cost = 0.0

    try:
        async for message in query(prompt="Hello, please respond briefly", options=options):
            # AssistantMessage - Claude's responses
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text_output.append(block.text)
                        print(".", end="", flush=True)
                    elif isinstance(block, ToolUseBlock):
                        tools_called.append(block.name)

            # SystemMessage - Session events
            elif isinstance(message, SystemMessage):
                if message.subtype == 'init':
                    print("\n✅ Session initialized")
                    if 'plugins' in message.data:
                        print(f"   Plugins: {message.data['plugins']}")

            # ResultMessage - Final result with cost
            elif isinstance(message, ResultMessage):
                session_id = message.session_id
                cost = message.total_cost_usd or 0.0
                print(f"\n✅ Completed: {message.duration_ms/1000:.1f}s")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    output = ''.join(text_output)

    print(f"Session ID: {session_id}")
    print(f"Cost: ${cost:.4f}")
    print(f"Tools called: {len(tools_called)}")
    print(f"Output length: {len(output)} characters")

    if output:
        print(f"\nOutput preview:\n{output[:200]}...")
        print("\n✅ SUCCESS - Plugin loaded and responded")
        return 0
    else:
        print("\n❌ FAILURE - No output received")
        return 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
