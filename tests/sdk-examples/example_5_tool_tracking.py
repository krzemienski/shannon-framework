#!/usr/bin/env python3
"""
Example 5: Tool Usage Tracking

Tests the pattern for tracking which tools Claude uses during execution.

Pattern from: agent-sdk-python-api-reference.md ToolUseBlock, SDK_PATTERNS_EXTRACTED.md
"""

import os
import sys
import asyncio

os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ToolUseBlock
)

async def test_tool_tracking():
    """Verify tool usage tracking pattern."""

    print("=" * 80)
    print("Example 5: Tool Usage Tracking")
    print("=" * 80)

    print("\n✅ Pattern:")
    print("  tools_used = []")
    print("  for message in query(...):")
    print("      if isinstance(message, AssistantMessage):")
    print("          for block in message.content:")
    print("              if isinstance(block, ToolUseBlock):")
    print("                  tools_used.append(block.name)")

    print("\n⏳ Testing pattern...")

    tools_used = []

    options = ClaudeAgentOptions(
        allowed_tools=["Read"],
        permission_mode="bypassPermissions",
        max_turns=2
    )

    # Ask Claude to use a tool
    async for message in query(prompt="Read the file ./README.md", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    tools_used.append({
                        'name': block.name,
                        'id': block.id,
                        'input_keys': list(block.input.keys())
                    })
                    print(f"  🔧 Tool: {block.name}")
                    print(f"     ID: {block.id}")
                    print(f"     Input keys: {block.input.keys()}")

    # Validate
    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    print(f"Tools tracked: {len(tools_used)}")

    if tools_used:
        print(f"\nTool details:")
        for i, tool in enumerate(tools_used, 1):
            print(f"  {i}. {tool['name']}")
            print(f"     Input params: {tool['input_keys']}")

    # Expected: At least one "Read" tool use
    read_tools = [t for t in tools_used if t['name'] == 'Read']
    success = len(read_tools) > 0

    if success:
        print(f"\n✅ PASS: Tool tracking works correctly")
        print(f"  - Tracked {len(tools_used)} tool uses")
        print(f"  - Found {len(read_tools)} Read tool uses")
    else:
        print(f"\n❌ FAIL: Expected at least one Read tool use")
        print(f"  - Got {len(tools_used)} tools: {[t['name'] for t in tools_used]}")

    return 0 if success else 1

if __name__ == '__main__':
    exit_code = asyncio.run(test_tool_tracking())
    sys.exit(exit_code)
