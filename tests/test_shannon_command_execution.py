#!/usr/bin/env python3
"""
Test Shannon command execution via SDK

Tests that Shannon commands actually execute and return output.
"""

import os
import sys
import asyncio
from pathlib import Path

if 'ANTHROPIC_API_KEY' not in os.environ:
    raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock
)

async def test_shannon_command():
    """Test /sh_status command execution"""

    print("="*80)
    print("Testing Shannon Command Execution")
    print("="*80)

    # Read a small spec for testing
    spec_file = Path("docs/ref/prd-creator-spec.md")
    spec_text = spec_file.read_text()[:500]  # Small sample

    options = ClaudeAgentOptions(
        setting_sources=["user", "project"],  # Required!
        permission_mode="bypassPermissions",
        allowed_tools=["Skill"],
        max_turns=3
    )

    print("\n⏳ Executing /shannon-plugin:sh_spec with small sample...")

    text_output = []
    plugins_loaded = []

    async for message in query(prompt=f'/shannon-plugin:sh_spec "{spec_text}"', options=options):
        if isinstance(message, SystemMessage) and message.subtype == 'init':
            plugins_loaded = message.data.get('plugins', [])
            shannon = [p for p in plugins_loaded if 'shannon' in p['name'].lower()]
            print(f"\n✅ Shannon plugin found: {shannon[0]['name'] if shannon else 'NOT FOUND'}")

        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_output.append(block.text)
                    print(".", end="", flush=True)

        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            print(f"\n\n✅ Complete: ${cost:.4f}")

    output = ''.join(text_output)

    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")
    print(f"Output length: {len(output)} chars")
    print(f"Has output: {'✅' if len(output) > 0 else '❌'}")

    if len(output) > 0:
        print(f"\nFirst 500 chars:")
        print(output[:500])
        return 0
    else:
        print("❌ NO OUTPUT - Command didn't execute")
        return 1

if __name__ == '__main__':
    sys.exit(asyncio.run(test_shannon_command()))
