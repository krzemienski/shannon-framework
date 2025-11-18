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
import os
import re
import sys
from pathlib import Path
from typing import List


CHAR_THRESHOLD = 10_000
LINE_THRESHOLD = 400
CODE_BLOCK_LINE_THRESHOLD = 200


def detect_large_prompt(prompt: str, files_meta) -> List[str]:
    """
    Determine whether the incoming prompt references large content.
    Returns a list of human-readable reasons.
    """
    reasons: List[str] = []
    if not prompt:
        return reasons

    char_len = len(prompt)
    if char_len >= CHAR_THRESHOLD:
        reasons.append(f"{char_len:,} characters")

    line_count = prompt.count("\n") + 1
    if line_count >= LINE_THRESHOLD:
        reasons.append(f"{line_count:,} lines")

    if re.search(r"lines?\s+\d+\s*[-–]\s*\d+", prompt, flags=re.IGNORECASE):
        reasons.append("explicit line range reference")

    if re.search(r"L\d+\|", prompt):
        reasons.append("annotated line numbers (L###|)")

    code_blocks = re.findall(r"```.*?```", prompt, flags=re.DOTALL)
    for block in code_blocks:
        block_lines = block.count("\n") - 1
        if block_lines >= CODE_BLOCK_LINE_THRESHOLD:
            reasons.append(f"code block with {block_lines:,} lines")
            break

    # Optional metadata from editors (Cursor/Claude) – lineCount, size, etc.
    for meta in files_meta:
        line_info = meta.get("lineCount") or meta.get("lines")
        char_info = meta.get("charCount") or meta.get("size")
        path = meta.get("path") or meta.get("name", "file")
        if isinstance(line_info, (int, float)) and line_info >= LINE_THRESHOLD:
            reasons.append(f"{path} contains {int(line_info):,} lines")
        elif isinstance(char_info, (int, float)) and char_info >= CHAR_THRESHOLD:
            reasons.append(f"{path} contains {int(char_info):,} characters")

    return reasons


def main():
    """
    Main execution for UserPromptSubmit hook

    Injects North Star goal into prompt context if available.
    """
    try:
        # Read hook input
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get('prompt', '')
        files_meta = input_data.get('files') or []

        # Forced Reading Sentinel check
        sentinel_reasons = detect_large_prompt(prompt, files_meta)
        if sentinel_reasons:
            print("📏 **Forced Reading Sentinel Activated**")
            print(f"- Reason: {', '.join(sentinel_reasons)}")
            print("- Directive: Follow `skills/forced-reading-sentinel` + `core/FORCED_READING_PROTOCOL.md`.")
            print("  1. Read the referenced file(s) sequentially without skipping.")
            print("  2. Summarize each major block before proposing edits.")
            print("  3. Confirm understanding or request clarification before coding.")
            print("---")

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
