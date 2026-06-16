#!/usr/bin/env -S python3
"""
Shannon UserPromptSubmit Hook - North Star Goal Injection

Purpose: Automatically injects North Star goal into every user prompt to ensure
         all work aligns with the overarching project goal.

How It Works:
1. Hook fires when user submits any prompt
2. Checks for North Star goal in Serena storage
3. If found, injects goal as context before prompt
4. Claude sees goal in every interaction
5. All decisions made with goal alignment

Benefits: Transforms North Star from stored data to active context

Author: Shannon Framework
Version: 3.0.1
License: MIT
Copyright (c) 2024 Shannon Framework Team
"""

import json
import sys
from pathlib import Path
import os


def main():
    """
    Main execution for UserPromptSubmit hook

    Injects North Star goal into prompt context if available.
    """
    try:
        # Read hook input
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get('prompt', '')

        # Try to load North Star from Serena storage
        serena_root = Path(os.getenv('SERENA_PROJECT_ROOT', os.getenv('CLAUDE_PROJECT_DIR', '.')))
        north_star_file = serena_root / ".serena" / "north_star.txt"

        if north_star_file.exists():
            north_star = north_star_file.read_text().strip()

            if north_star:
                # Inject North Star as context
                print("🎯 **North Star Goal**: " + north_star)
                print("**Context**: All work must align with this overarching goal.")
                print("---")

        # Check for active wave context
        wave_status_file = serena_root / ".serena" / "active_wave_status.txt"
        if wave_status_file.exists():
            wave_status = wave_status_file.read_text().strip()
            if wave_status:
                print(f"🌊 **Active Wave**: {wave_status}")
                print("---")

    except Exception as e:
        # Silent failure - don't break user's prompt
        # Log to stderr for debugging
        print(f"[Shannon UserPromptSubmit] Warning: {e}", file=sys.stderr)
        pass

    # Always allow prompt to proceed
    sys.exit(0)


if __name__ == "__main__":
    main()
