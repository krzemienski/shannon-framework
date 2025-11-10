#!/usr/bin/env python3
"""
Example 2: Correct Message Type Checking with isinstance()

Tests the CORRECT pattern for checking message types (NOT .type attribute).

Pattern from: agent-sdk-python-api-reference.md lines 767-800
"""

import os
import sys
import asyncio

os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage
)

async def test_message_isinstance():
    """Verify isinstance() pattern for message type checking."""

    print("=" * 80)
    print("Example 2: Message Type Checking with isinstance()")
    print("=" * 80)

    print("\n✅ CORRECT Pattern:")
    print("  isinstance(message, AssistantMessage)")
    print("  isinstance(message, SystemMessage)")
    print("  isinstance(message, ResultMessage)")

    print("\n❌ WRONG Pattern (from old skill):")
    print("  if message.type == 'assistant'  # NO .type attribute!")

    print("\n⏳ Testing pattern...")

    message_counts = {
        'SystemMessage': 0,
        'AssistantMessage': 0,
        'ResultMessage': 0,
        'Other': 0
    }

    options = ClaudeAgentOptions(
        max_turns=1,
        allowed_tools=[]
    )

    async for message in query(prompt="Say 'Hello World'", options=options):
        # CORRECT pattern: isinstance() checks
        if isinstance(message, SystemMessage):
            message_counts['SystemMessage'] += 1
            print(f"  📨 SystemMessage (subtype: {message.subtype})")

        elif isinstance(message, AssistantMessage):
            message_counts['AssistantMessage'] += 1
            print(f"  💬 AssistantMessage ({len(message.content)} blocks)")

        elif isinstance(message, ResultMessage):
            message_counts['ResultMessage'] += 1
            print(f"  ✅ ResultMessage (duration: {message.duration_ms}ms)")

        else:
            message_counts['Other'] += 1
            print(f"  ❓ Other: {type(message).__name__}")

    # Validate
    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    print(f"Message type counts:")
    for msg_type, count in message_counts.items():
        print(f"  {msg_type}: {count}")

    # Expected: SystemMessage (init), AssistantMessage (content), ResultMessage (final)
    success = (
        message_counts['SystemMessage'] >= 1 and
        message_counts['AssistantMessage'] >= 1 and
        message_counts['ResultMessage'] >= 1
    )

    if success:
        print(f"\n✅ PASS: isinstance() pattern works correctly")
    else:
        print(f"\n❌ FAIL: Expected System + Assistant + Result messages")

    return 0 if success else 1

if __name__ == '__main__':
    exit_code = asyncio.run(test_message_isinstance())
    sys.exit(exit_code)
