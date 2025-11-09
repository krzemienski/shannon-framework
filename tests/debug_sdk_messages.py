#!/usr/bin/env python3
"""Debug SDK message structure"""

import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # Set API key
    os.environ['ANTHROPIC_API_KEY'] = "YOUR_API_KEY_HERE"

    print("Sending simple query to inspect message structure...")

    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5"
    )

    count = 0
    async for msg in query(prompt="Say hello", options=options):
        count += 1
        print(f"\n--- Message {count} ---")
        print(f"Type: {type(msg)}")
        print(f"Dir: {dir(msg)}")

        # Try to access common attributes
        for attr in ['type', 'content', 'role', 'text', 'message']:
            if hasattr(msg, attr):
                print(f"{attr}: {getattr(msg, attr)}")

        if count > 5:
            break

    return 0

if __name__ == '__main__':
    asyncio.run(main())
