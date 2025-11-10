#!/usr/bin/env python3
"""
Example 3: Content Block Iteration

Tests the CORRECT pattern for iterating message content blocks.

Pattern from: agent-sdk-python-api-reference.md lines 804-855
"""

import os
import sys
import asyncio

os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ThinkingBlock
)

async def test_content_iteration():
    """Verify content block iteration pattern."""

    print("=" * 80)
    print("Example 3: Content Block Iteration")
    print("=" * 80)

    print("\n✅ CORRECT Pattern:")
    print("  for block in message.content:")
    print("      if isinstance(block, TextBlock):")
    print("          text = block.text")

    print("\n❌ WRONG Pattern (from old skill):")
    print("  text = message.content  # content is list, not string!")

    print("\n⏳ Testing pattern...")

    block_counts = {
        'TextBlock': 0,
        'ThinkingBlock': 0,
        'ToolUseBlock': 0,
        'Other': 0
    }

    text_collected = []

    options = ClaudeAgentOptions(
        max_turns=1,
        allowed_tools=[]
    )

    async for message in query(prompt="Say 'Hello' then explain why you said it", options=options):
        if isinstance(message, AssistantMessage):
            print(f"  💬 AssistantMessage with {len(message.content)} blocks:")

            # CORRECT: Iterate content blocks
            for block in message.content:
                if isinstance(block, TextBlock):
                    block_counts['TextBlock'] += 1
                    text_collected.append(block.text)
                    print(f"    📝 TextBlock: {block.text[:50]}...")

                elif isinstance(block, ThinkingBlock):
                    block_counts['ThinkingBlock'] += 1
                    print(f"    🧠 ThinkingBlock: {len(block.thinking)} chars")

                elif isinstance(block, ToolUseBlock):
                    block_counts['ToolUseBlock'] += 1
                    print(f"    🔧 ToolUseBlock: {block.name}")

                else:
                    block_counts['Other'] += 1
                    print(f"    ❓ Other block: {type(block).__name__}")

    # Validate
    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    print(f"Block type counts:")
    for block_type, count in block_counts.items():
        print(f"  {block_type}: {count}")

    full_text = ''.join(text_collected)
    print(f"\nExtracted text: {len(full_text)} chars")
    print(f"Sample: {full_text[:100]}...")

    # Expected: At least one TextBlock with "Hello"
    success = (
        block_counts['TextBlock'] >= 1 and
        len(full_text) > 0 and
        'Hello' in full_text
    )

    if success:
        print(f"\n✅ PASS: Content block iteration works correctly")
    else:
        print(f"\n❌ FAIL: Expected TextBlocks with 'Hello'")

    return 0 if success else 1

if __name__ == '__main__':
    exit_code = asyncio.run(test_content_iteration())
    sys.exit(exit_code)
