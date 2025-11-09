#!/usr/bin/env python3
"""
Simple test: Verify Shannon plugin loads via SDK

This is a diagnostic test to verify the Shannon plugin can be loaded
programmatically via Claude Agents SDK before attempting complex verification.
"""

import asyncio
import sys
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    print("=" * 80)
    print("DIAGNOSTIC: Shannon Plugin Loading Test")
    print("=" * 80)

    # Verify plugin directory exists
    plugin_path = Path("./shannon-plugin")
    if not plugin_path.exists():
        print(f"❌ Plugin directory not found: {plugin_path.absolute()}")
        return 1

    plugin_json = plugin_path / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        print(f"❌ Plugin manifest not found: {plugin_json}")
        return 1

    print(f"✅ Plugin directory exists: {plugin_path.absolute()}")
    print(f"✅ Plugin manifest exists: {plugin_json}")

    # Load Shannon plugin
    print("\nAttempting to load Shannon plugin...")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(plugin_path)}],
        model="claude-sonnet-4-5"
    )

    # Simple query to trigger plugin loading
    print("\nSending test query...")

    messages = []
    init_received = False

    try:
        async for msg in query(prompt="Hello, are you there?", options=options):
            msg_type = getattr(msg, 'type', None)

            print(f"  Message type: {msg_type}")

            if msg_type == 'system':
                subtype = getattr(msg, 'subtype', None)
                print(f"    Subtype: {subtype}")

                if subtype == 'init':
                    init_received = True
                    plugins = getattr(msg, 'plugins', [])
                    print(f"    Plugins loaded: {plugins}")

            elif msg_type == 'assistant':
                content = getattr(msg, 'content', '')
                messages.append(content)
                print(f"    Content: {content[:80]}...")

            elif msg_type == 'tool_call':
                tool_name = getattr(msg, 'tool_name', 'unknown')
                print(f"    Tool: {tool_name}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    output = ''.join(messages)

    print(f"Init message received: {init_received}")
    print(f"Messages received: {len(messages)}")
    print(f"Output length: {len(output)} characters")

    if output:
        print(f"\nOutput preview:\n{output[:200]}...")

    if messages:
        print("\n✅ SUCCESS: Plugin loaded and responded")
        return 0
    else:
        print("\n❌ FAILURE: No response from Claude")
        return 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
