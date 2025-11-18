#!/usr/bin/env -S python3
"""
Shannon UserPromptSubmit Hook - Context Injection & Forced Reading Activation

Purpose: Automatically injects context and activates forced reading protocol when needed
         to ensure all work aligns with goals and critical content is fully comprehended.

How It Works:
1. Hook fires when user submits any prompt
2. Checks for North Star goal in Serena storage
3. Detects large prompts (>3000 chars) or large file references (>5000 lines)
4. Auto-injects forced-reading-protocol skill for complete comprehension
5. Recommends Sequential MCP (ultrathinking) for synthesis
6. Claude sees all context and activation instructions

Benefits: 
- Transforms North Star from stored data to active context
- Prevents skimming of critical content
- Ensures complete understanding before action

Author: Shannon Framework
Version: 5.4.0 (Enhanced with Forced Reading Detection)
License: MIT
Copyright (c) 2024 Shannon Framework Team
"""

import json
import sys
import re
import os
from pathlib import Path
from typing import List, Dict, Any


def detect_large_prompt(prompt: str, threshold: int = 3000) -> bool:
    """Check if prompt exceeds character threshold."""
    return len(prompt) > threshold


def detect_file_references(prompt: str, working_dir: Path) -> List[Dict[str, Any]]:
    """
    Detect file path references in prompt and check if they're large.
    
    Returns list of dicts with file info for large files.
    """
    # Regex patterns for file paths
    patterns = [
        r'(?:^|[\s\("`\'])([./~]?[\w\-./]+\.(?:md|py|ts|tsx|js|jsx|go|java|rb|php|yaml|json|txt))',
        r'(?:file|read|check|analyze|review)\s+([`"\']?)([^`"\'<>\n]+\.(?:md|py|ts|tsx|js|jsx|go|java))\1',
        r'@([^\s]+\.(?:md|py|ts|tsx|js|jsx))',  # @file.md syntax
    ]
    
    potential_files = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, prompt, re.IGNORECASE)
        for match in matches:
            # Handle different regex capture groups
            filepath = match if isinstance(match, str) else (match[1] if len(match) > 1 else match[0])
            if filepath:
                potential_files.add(filepath.strip())
    
    large_files = []
    
    for filepath in potential_files:
        # Try multiple path resolutions
        paths_to_try = [
            working_dir / filepath,  # Relative to working dir
            Path(filepath),  # Absolute or relative to current
            working_dir / filepath.lstrip('./'),  # Clean relative
        ]
        
        for path in paths_to_try:
            try:
                if path.exists() and path.is_file():
                    info = check_large_file(path)
                    if info['is_large']:
                        large_files.append(info)
                    break  # Found the file, stop trying other paths
            except (OSError, PermissionError):
                continue
    
    return large_files


def check_large_file(filepath: Path, line_threshold: int = 5000, size_threshold: int = 50 * 1024) -> Dict[str, Any]:
    """
    Check if file is large (by lines or size).
    
    Returns dict with file info.
    """
    try:
        stat = filepath.stat()
        
        # Check size first (faster)
        if stat.st_size > size_threshold:
            return {
                'is_large': True,
                'path': str(filepath),
                'size_kb': stat.st_size // 1024,
                'reason': 'size',
                'threshold': size_threshold // 1024
            }
        
        # Count lines for text files
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for _ in f)
            
            if line_count > line_threshold:
                return {
                    'is_large': True,
                    'path': str(filepath),
                    'lines': line_count,
                    'reason': 'lines',
                    'threshold': line_threshold
                }
        except Exception:
            pass
        
        return {'is_large': False, 'path': str(filepath)}
        
    except (OSError, PermissionError):
        return {'is_large': False, 'path': str(filepath)}


def detect_specification_keywords(prompt: str) -> bool:
    """Detect if prompt contains specification/requirements keywords."""
    keywords = [
        'specification', 'requirements', 'design doc', 'design document',
        'architecture doc', 'technical spec', 'requirement doc',
        'SPEC_', 'PLAN_', 'comprehensive analysis'
    ]
    prompt_lower = prompt.lower()
    return any(keyword.lower() in prompt_lower for keyword in keywords)


def inject_forced_reading_protocol(large_items: List[Dict[str, Any]], is_large_prompt: bool, has_spec_keywords: bool):
    """Inject forced reading protocol activation."""
    print("")
    print("=" * 80)
    print("📖 **SHANNON FORCED READING PROTOCOL - AUTO-ACTIVATED**")
    print("=" * 80)
    print("")
    
    if is_large_prompt:
        print("✋ **LARGE PROMPT DETECTED**")
        print("   - Prompt length: >3000 characters")
        print("   - Risk: Incomplete reading, missed details")
        print("")
    
    if large_items:
        print("✋ **LARGE FILE REFERENCES DETECTED**")
        for item in large_items:
            if item['reason'] == 'lines':
                print(f"   - {item['path']}: {item['lines']} lines (threshold: {item['threshold']})")
            elif item['reason'] == 'size':
                print(f"   - {item['path']}: {item['size_kb']}KB (threshold: {item['threshold']}KB)")
        print("")
    
    if has_spec_keywords:
        print("✋ **SPECIFICATION KEYWORDS DETECTED**")
        print("   - Content appears to be critical specification/requirements")
        print("")
    
    print("**MANDATORY PROTOCOL** (shannon:forced-reading-protocol skill):")
    print("")
    print("**Step 1: PRE-COUNT**")
    print("  - Count total lines/chars BEFORE reading ANY content")
    print("  - Output: 'File has N lines. Now I will read all N lines completely.'")
    print("")
    print("**Step 2: SEQUENTIAL READING**")
    print("  - Read EVERY line sequentially from 1 to N")
    print("  - NO skipping, NO 'relevant sections', NO partial reading")
    print("")
    print("**Step 3: VERIFY COMPLETENESS**")
    print("  - Verify: lines_read == total_lines")
    print("  - Output verification: '✅ COMPLETE READING VERIFIED'")
    print("")
    print("**Step 4: SEQUENTIAL SYNTHESIS**")
    print("  - Use Sequential MCP (mcp_sequential-thinking_sequentialthinking)")
    print("  - Minimum thoughts:")
    if large_items:
        max_lines = max([item.get('lines', 0) for item in large_items] + [0])
        if max_lines > 5000:
            print("    - 500+ thoughts (critical size file >5000 lines)")
        elif max_lines > 2000:
            print("    - 200+ thoughts (large file >2000 lines)")
        elif max_lines > 500:
            print("    - 100+ thoughts (medium file >500 lines)")
        else:
            print("    - 50+ thoughts")
    else:
        print("    - 100+ thoughts (large prompt)")
    print("  - ONLY AFTER complete reading verified")
    print("")
    print("**NO SYNTHESIS UNTIL READING COMPLETE**")
    print("  ❌ NO analysis during reading")
    print("  ❌ NO conclusions during reading")  
    print("  ❌ NO 'I noticed' during reading")
    print("  ✅ ONLY after Step 3 verification passes")
    print("")
    print("=" * 80)
    print("")


def main():
    """
    Main execution for UserPromptSubmit hook

    Enhanced with forced reading protocol activation.
    """
    try:
        # Read hook input
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get('prompt', '')
        
        # Get working directory
        working_dir = Path(os.getenv('SERENA_PROJECT_ROOT', 
                                     os.getenv('CLAUDE_PROJECT_DIR', 
                                              os.getenv('PWD', '.'))))

        # === NORTH STAR INJECTION (Existing) ===
        serena_root = Path(os.getenv('SERENA_PROJECT_ROOT', os.getenv('CLAUDE_PROJECT_DIR', '.')))
        north_star_file = serena_root / ".serena" / "north_star.txt"

        if north_star_file.exists():
            north_star = north_star_file.read_text().strip()

            if north_star:
                print("🎯 **North Star Goal**: " + north_star)
                print("**Context**: All work must align with this overarching goal.")
                print("---")

        # === WAVE CONTEXT INJECTION (Existing) ===
        wave_status_file = serena_root / ".serena" / "active_wave_status.txt"
        if wave_status_file.exists():
            wave_status = wave_status_file.read_text().strip()
            if wave_status:
                print(f"🌊 **Active Wave**: {wave_status}")
                print("---")

        # === FORCED READING PROTOCOL ACTIVATION (NEW v5.4) ===
        
        # Detect large prompt
        is_large_prompt = detect_large_prompt(prompt)
        
        # Detect file references
        large_file_refs = detect_file_references(prompt, working_dir)
        
        # Detect specification keywords
        has_spec_keywords = detect_specification_keywords(prompt)
        
        # Activate forced reading protocol if triggered
        if is_large_prompt or large_file_refs or has_spec_keywords:
            inject_forced_reading_protocol(large_file_refs, is_large_prompt, has_spec_keywords)

    except Exception as e:
        # Silent failure - don't break user's prompt
        # Log to stderr for debugging
        print(f"[Shannon UserPromptSubmit] Warning: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        pass

    # Always allow prompt to proceed
    sys.exit(0)


if __name__ == "__main__":
    main()
