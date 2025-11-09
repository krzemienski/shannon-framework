#!/usr/bin/env python3
"""
Verify if messages have .type attribute or only class-based type
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

from claude_agent_sdk import query, SystemMessage, AssistantMessage
import asyncio

async def main():
    print("Testing message attributes...")

    async for message in query(prompt="hello"):
        print(f"\n{'='*80}")
        print(f"Message class: {type(message)}")
        print(f"Has .type? {hasattr(message, 'type')}")

        if hasattr(message, 'type'):
            print(f"message.type = {message.type}")

        if isinstance(message, SystemMessage):
            print(f"IS SystemMessage")
            print(f"  subtype: {message.subtype}")
            if hasattr(message, 'type'):
                print(f"  type attr: {message.type}")
            print(f"  data keys: {list(message.data.keys())[:10]}")

        if isinstance(message, AssistantMessage):
            print(f"IS AssistantMessage")
            if hasattr(message, 'type'):
                print(f"  type attr: {message.type}")
            print(f"  model: {message.model}")

        # Test both patterns
        print("\nPattern tests:")
        print(f"  isinstance(message, SystemMessage): {isinstance(message, SystemMessage)}")

        if hasattr(message, 'type'):
            print(f"  message.type == 'system': {getattr(message, 'type', None) == 'system'}")

        if len([1 for _ in range(3)]) >= 2:  # After 2 messages
            break

    return 0

if __name__ == '__main__':
    asyncio.run(main())
