#!/usr/bin/env python3
"""
Example 4: Complete Text Extraction Pattern

Tests the complete pattern for extracting text from Claude's responses.

Pattern from: agent-sdk-python-api-reference.md lines 76-94, SDK_PATTERNS_EXTRACTED.md
"""

import os
import sys
import asyncio

os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def test_text_extraction():
    """Verify complete text extraction pattern."""

    print("=" * 80)
    print("Example 4: Text Extraction Pattern")
    print("=" * 80)

    print("\n✅ Pattern:")
    print("  text_parts = []")
    print("  for message in query(...):")
    print("      if isinstance(message, AssistantMessage):")
    print("          for block in message.content:")
    print("              if isinstance(block, TextBlock):")
    print("                  text_parts.append(block.text)")
    print("  output = ''.join(text_parts)")

    print("\n⏳ Testing pattern...")

    # Collect text using the pattern
    text_parts = []

    options = ClaudeAgentOptions(
        max_turns=1,
        allowed_tools=[]
    )

    async for message in query(prompt="Write a haiku about coding", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_parts.append(block.text)
                    print(".", end="", flush=True)

    output = ''.join(text_parts)

    # Validate
    print(f"\n\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    print(f"Text parts collected: {len(text_parts)}")
    print(f"Total output length: {len(output)} chars")
    print(f"\nExtracted text:")
    print("-" * 80)
    print(output)
    print("-" * 80)

    # Expected: Non-empty output with haiku content
    success = len(output) > 0 and len(text_parts) > 0

    if success:
        print(f"\n✅ PASS: Text extraction works correctly")
        print(f"  - Collected {len(text_parts)} text blocks")
        print(f"  - Total {len(output)} characters")
    else:
        print(f"\n❌ FAIL: No text extracted")

    return 0 if success else 1

if __name__ == '__main__':
    exit_code = asyncio.run(test_text_extraction())
    sys.exit(exit_code)
