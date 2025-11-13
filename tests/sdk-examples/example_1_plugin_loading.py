#!/usr/bin/env python3
"""
Example 1: Basic Plugin Loading with setting_sources

Tests THE most critical SDK requirement: setting_sources for filesystem loading.

Pattern from: agent-sdk-skills.md line 16, agent-sdk-plugins.md lines 9-47
"""

import os
import sys
import asyncio

# Set API key FIRST
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage

async def test_plugin_loading():
    """Verify Shannon plugin loads with correct configuration."""

    print("=" * 80)
    print("Example 1: Plugin Loading with setting_sources")
    print("=" * 80)

    # CORRECT configuration
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        setting_sources=["user", "project"],  # REQUIRED!
        permission_mode="bypassPermissions",
        max_turns=1
    )

    print("\n✅ Configuration:")
    print("  - plugins: ./shannon-plugin")
    print("  - setting_sources: ['user', 'project']")
    print("  - permission_mode: bypassPermissions")

    print("\n⏳ Loading plugin...")

    plugins_loaded = []
    commands_available = []

    async for message in query(prompt="hello", options=options):
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            plugins_loaded = message.data.get('plugins', [])
            commands_available = message.data.get('slash_commands', [])

            print(f"\n📊 Results:")
            print(f"  Plugins loaded: {len(plugins_loaded)}")
            print(f"  Commands available: {len(commands_available)}")

            # Check for Shannon commands
            shannon_commands = [c for c in commands_available
                               if c.startswith('/shannon:')]
            print(f"  Shannon commands: {len(shannon_commands)}")

            if shannon_commands:
                print(f"\n✅ Shannon commands found:")
                for cmd in sorted(shannon_commands)[:5]:
                    print(f"    - {cmd}")
                if len(shannon_commands) > 5:
                    print(f"    ... and {len(shannon_commands) - 5} more")

    # Validate
    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    success = True

    if len(plugins_loaded) == 0:
        print("❌ FAIL: No plugins loaded")
        print("   Check: setting_sources=["user", "project"] is set")
        success = False
    else:
        print(f"✅ PASS: {len(plugins_loaded)} plugin(s) loaded")

    if len(shannon_commands) == 0:
        print("❌ FAIL: No Shannon commands found")
        print("   Check: Plugin loaded correctly")
        success = False
    else:
        print(f"✅ PASS: {len(shannon_commands)} Shannon command(s) available")

    return 0 if success else 1

if __name__ == '__main__':
    exit_code = asyncio.run(test_plugin_loading())
    sys.exit(exit_code)
