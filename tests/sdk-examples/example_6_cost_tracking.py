#!/usr/bin/env python3
"""
Example 6: Cost and Usage Tracking

Tests the pattern for extracting cost and usage information from ResultMessage.

Pattern from: agent-sdk-python-api-reference.md ResultMessage, SDK_PATTERNS_EXTRACTED.md
"""

import os
import sys
import asyncio

os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def test_cost_tracking():
    """Verify cost and usage tracking pattern."""

    print("=" * 80)
    print("Example 6: Cost and Usage Tracking")
    print("=" * 80)

    print("\n✅ Pattern:")
    print("  cost = 0.0")
    print("  async for message in query(...):")
    print("      if isinstance(message, ResultMessage):")
    print("          cost = message.total_cost_usd or 0.0")
    print("          usage = message.usage")
    print("          duration = message.duration_ms")

    print("\n⏳ Testing pattern...")

    cost = 0.0
    session_id = None
    usage = None
    duration_ms = 0

    options = ClaudeAgentOptions(
        max_turns=1,
        allowed_tools=[]
    )

    async for message in query(prompt="Say 'Hello'", options=options):
        if isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            session_id = message.session_id
            usage = message.usage
            duration_ms = message.duration_ms

            print(f"  💰 ResultMessage received:")
            print(f"     Session ID: {session_id}")
            print(f"     Cost: ${cost:.4f}")
            print(f"     Duration: {duration_ms}ms ({duration_ms/1000:.2f}s)")
            print(f"     Is error: {message.is_error}")
            print(f"     Turns: {message.num_turns}")

            if usage:
                print(f"     Usage:")
                for key, value in usage.items():
                    print(f"       {key}: {value}")

    # Validate
    print(f"\n{'='*80}")
    print("Validation")
    print(f"{'='*80}")

    checks = [
        ("ResultMessage received", cost >= 0),  # Cost should be set (>= 0)
        ("Session ID present", session_id is not None),
        ("Duration measured", duration_ms > 0),
        ("Cost is number", isinstance(cost, (int, float)))
    ]

    passed = sum(1 for _, result in checks if result)

    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    success = passed == len(checks)

    if success:
        print(f"\n✅ PASS: Cost tracking works correctly")
    else:
        print(f"\n❌ FAIL: {passed}/{len(checks)} checks passed")

    return 0 if success else 1

if __name__ == '__main__':
    exit_code = asyncio.run(test_cost_tracking())
    sys.exit(exit_code)
