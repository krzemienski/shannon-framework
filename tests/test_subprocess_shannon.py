#!/usr/bin/env python3
"""
Test Shannon via subprocess (calling claude CLI directly)

Since SDK doesn't load plugins, we call Claude Code as subprocess
and parse the output. This works because Shannon is proven to work
in interactive Claude Code.
"""

import subprocess
import sys
import os

def test_shannon_command():
    """Test Shannon /sh_spec command via subprocess"""

    print("Testing Shannon /sh_spec via subprocess...")
    print("=" * 80)

    # Simple spec to test
    spec = "Build a web form with React, email validation, submit to API endpoint"

    # Call Claude Code CLI with Shannon command
    # Using --headless for non-interactive mode
    result = subprocess.run(
        [
            'claude',
            '--headless',
            '--',
            f'/sh_spec "{spec}"'
        ],
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, 'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY')}
    )

    print(f"Exit code: {result.returncode}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"Stderr length: {len(result.stderr)}")

    if result.stdout:
        print(f"\nOutput preview:\n{result.stdout[:500]}...")

    if result.stderr:
        print(f"\nStderr:\n{result.stderr[:500]}...")

    # Validate
    if "Complexity" in result.stdout or "Shannon" in result.stdout:
        print("\n✅ Shannon command executed")
        return 0
    else:
        print("\n❌ Shannon command failed")
        return 1

if __name__ == '__main__':
    sys.exit(test_shannon_command())
