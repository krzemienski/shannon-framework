"""
Shannon Direct Mode - Skill Invocation Without SDK

Used when Shannon CLI is running INSIDE Claude Code (not standalone).
Directly invokes skills via Skill tool instead of using claude_agent_sdk.

This avoids circular invocation: Claude Code → shannon CLI → SDK → Claude Code
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def is_running_inside_claude_code() -> bool:
    """
    Detect if Shannon CLI is running inside Claude Code environment.

    Indicators:
    - CLAUDE_CODE_SESSION environment variable
    - Parent process is claude
    - Running in Claude Code working directory structure
    """
    # Check for Claude Code environment variable
    if os.getenv('CLAUDE_CODE_SESSION'):
        return True

    # Check if parent process is claude
    try:
        import psutil
        parent = psutil.Process().parent()
        if parent and 'claude' in parent.name().lower():
            return True
    except:
        pass

    # Check for .claude directory in cwd or parent directories
    current = Path.cwd()
    for _ in range(5):  # Check up to 5 levels up
        if (current / '.claude').exists():
            return True
        if current.parent == current:
            break
        current = current.parent

    return False


def invoke_spec_analysis_direct(spec_text: str) -> Dict[str, Any]:
    """
    Invoke spec-analysis skill directly without SDK.

    Returns analysis result as if it came from SDK, but generated
    by direct Claude Code skill invocation.

    Args:
        spec_text: Specification content

    Returns:
        Analysis result dictionary
    """
    # When running inside Claude Code, skills are available
    # Output instructions for Claude Code to execute
    print("\n" + "="*60)
    print("SHANNON DIRECT MODE: Running inside Claude Code")
    print("="*60)
    print("\nPlease invoke the spec-analysis skill with this specification:\n")
    print(spec_text)
    print("\n" + "="*60)
    print("Waiting for skill execution...")
    print("="*60 + "\n")

    # In direct mode, we rely on the operator (Claude Code user) to:
    # 1. See this message
    # 2. Invoke @skill spec-analysis manually
    # 3. Return the results

    # For now, return a placeholder that indicates direct mode was triggered
    return {
        "mode": "direct",
        "status": "awaiting_manual_invocation",
        "message": "Shannon CLI detected it's running inside Claude Code. Please invoke spec-analysis skill manually."
    }


def check_api_key_and_suggest() -> bool:
    """
    Check if ANTHROPIC_API_KEY is set and suggest alternatives if not.

    Returns:
        True if API key is set, False otherwise
    """
    if os.getenv('ANTHROPIC_API_KEY'):
        return True

    print("\n⚠️  ANTHROPIC_API_KEY not set")
    print("\nShannon CLI requires an API key to function.")
    print("\nOptions:")
    print("1. Set API key: export ANTHROPIC_API_KEY='sk-ant-...'")
    print("2. If running inside Claude Code, Shannon will use direct mode")
    print("\n")

    return False
