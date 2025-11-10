#!/usr/bin/env python3
"""Debug: Try absolute path for plugin"""

import os
import sys
import asyncio
from pathlib import Path

if 'ANTHROPIC_API_KEY' not in os.environ:
    raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage

async def test_absolute():
    plugin_path = Path.cwd() / "shannon-plugin"
    abs_path = str(plugin_path.absolute())

    print(f"Plugin path: {abs_path}")
    print(f"Exists: {plugin_path.exists()}")
    print(f"plugin.json exists: {(plugin_path / '.claude-plugin/plugin.json').exists()}")

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": abs_path}],
        setting_sources=["user", "project"],
        max_turns=1
    )

    async for message in query(prompt="hello", options=options):
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            plugins = message.data.get('plugins', [])
            print(f"\nPlugins loaded: {len(plugins)}")
            for p in plugins:
                print(f"  - {p['name']}")

            commands = message.data.get('slash_commands', [])
            shannon_cmds = [c for c in commands if 'sh_' in c or 'shannon' in c.lower()]
            print(f"\nShannon commands: {shannon_cmds}")

asyncio.run(test_absolute())
