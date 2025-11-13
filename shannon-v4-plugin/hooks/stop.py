#!/usr/bin/env -S python3
"""
Shannon Stop Hook - Wave Validation Gate Enforcement

Purpose: Enforces Shannon's validation gate philosophy by blocking completion
         until wave validation is approved by user.

How It Works:
1. Hook fires when Claude attempts to stop/complete
2. Checks for pending wave validation marker
3. If wave validation pending, blocks completion
4. Prompts user to review wave synthesis and approve
5. Only allows completion after validation

Benefits: Ensures quality gates are never skipped

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
    Main execution for Stop hook

    Blocks completion if wave validation is pending.
    """
    try:
        # Read hook input
        input_data = json.loads(sys.stdin.read())

        # Check for pending wave validation
        serena_root = Path(os.getenv('SERENA_PROJECT_ROOT', os.getenv('CLAUDE_PROJECT_DIR', '.')))
        validation_pending_file = serena_root / ".serena" / "wave_validation_pending"

        if validation_pending_file.exists():
            wave_info = validation_pending_file.read_text().strip()

            # Block completion until validation
            output = {
                "decision": "block",
                "reason": f"""⚠️  Shannon Wave Validation Required

{wave_info}

**Required Actions**:
1. Present wave synthesis to user
2. Request explicit approval: "Wave X approved" or "Continue to next wave"
3. Create checkpoint: /sh_checkpoint
4. Mark validation complete

**Do not proceed until user has reviewed and approved wave results.**

To bypass (not recommended): Remove .serena/wave_validation_pending file"""
            }

            print(json.dumps(output))
            sys.exit(0)

        # Check for incomplete todo items marked as critical
        critical_todos_file = serena_root / ".serena" / "critical_todos_incomplete"
        if critical_todos_file.exists():
            todos_info = critical_todos_file.read_text().strip()

            output = {
                "decision": "block",
                "reason": f"""⚠️  Shannon Critical Tasks Incomplete

{todos_info}

**Required Actions**:
1. Complete all critical tasks before finishing
2. Or explicitly mark them as deferred with user approval

Run /sh_status to see current task state."""
            }

            print(json.dumps(output))
            sys.exit(0)

    except Exception as e:
        # Don't block on errors - silent failure
        print(f"[Shannon Stop] Warning: {e}", file=sys.stderr)
        pass

    # Allow normal completion
    sys.exit(0)


if __name__ == "__main__":
    main()
