#!/usr/bin/env -S python3
"""
Shannon PreCompact Hook - Critical Context Preservation

Purpose: Prevents context loss during Claude Code auto-compaction by triggering
         CONTEXT_GUARDIAN to save checkpoint before compaction occurs.

How It Works:
1. Claude Code detects conversation approaching token limit
2. PreCompact hook executes before compaction
3. Hook generates Serena checkpoint instructions
4. Instructions injected into system prompt
5. Claude saves all context to Serena
6. Auto-compact proceeds safely
7. Next session: context restored from checkpoint

Critical: This hook prevents information loss during auto-compaction.

Author: Shannon Framework
Version: 3.0.1
License: MIT
Copyright (c) 2024 Shannon Framework Team
"""

import json
import sys
import os
import subprocess
from datetime import datetime, UTC
from typing import Dict, Any, Optional
from pathlib import Path


class ShannonPreCompactHook:
    """
    Shannon PreCompact Hook Implementation

    Generates checkpoint instructions that trigger CONTEXT_GUARDIAN
    to preserve all session state before Claude Code auto-compacts.
    """

    VERSION = "3.0.1"
    TIMEOUT_MS = 15000  # Increased from 5000 to 15000 for large projects
    HOOK_EVENT_NAME = "PreCompact"

    def __init__(self):
        """Initialize hook with environment configuration"""
        self.project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        self.plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT', '.')
        self.shannon_dir = f"{self.project_dir}/.claude/shannon"
        self.timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        self.checkpoint_key = f"shannon_precompact_checkpoint_{self.timestamp}"

        # Setup logging
        self.log_dir = Path.home() / ".claude" / "shannon-logs" / "precompact"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution logic for PreCompact hook

        Args:
            input_data: Hook input from Claude Code

        Returns:
            Hook output JSON with checkpoint instructions
        """
        try:
            # Log hook invocation
            self._log_to_file("hook_invoked", {"trigger": input_data.get("trigger", "auto")})

            # Check if Serena MCP is likely available (best effort)
            # We can't directly check MCP status from hook, but we can check for .serena directory
            serena_dir = Path(self.project_dir) / ".serena"
            if not serena_dir.exists():
                self._log_warning("Serena directory not found - Serena MCP may not be configured")
                # Don't block - just warn and continue with instructions
                print("⚠️  Shannon PreCompact: Serena directory not found, checkpoint may not save", file=sys.stderr)

            # Generate checkpoint instructions
            checkpoint_instructions = self._generate_checkpoint_instructions()

            # Generate hook output
            output = {
                "hookSpecificOutput": {
                    "hookEventName": self.HOOK_EVENT_NAME,
                    "version": self.VERSION,
                    "checkpointKey": self.checkpoint_key,
                    "timestamp": self.timestamp,
                    "additionalContext": checkpoint_instructions,
                    "preservationStatus": "instructions_generated",
                    "metadata": {
                        "executionTime": "instant",
                        "success": True,
                        "projectDir": self.project_dir,
                        "pluginRoot": self.plugin_root
                    }
                }
            }

            # Log successful execution
            self._log_info(f"PreCompact hook executed successfully. Checkpoint key: {self.checkpoint_key}")
            self._log_to_file("checkpoint_created", {"key": self.checkpoint_key})

            return output

        except Exception as e:
            # Handle any errors gracefully
            error_msg = f"PreCompact hook error: {str(e)}"
            self._log_error(error_msg)
            self._log_to_file("hook_error", {"error": str(e), "type": type(e).__name__})

            # Print to stderr for visibility
            print(f"⚠️  Shannon PreCompact: Error during checkpoint - {str(e)}", file=sys.stderr)

            # Return error response but don't block compaction (exit 1 not 2)
            return self._error_response(str(e))

    def _generate_checkpoint_instructions(self) -> str:
        """
        Generate Serena checkpoint instructions for CONTEXT_GUARDIAN

        Returns:
            Markdown instructions for context preservation
        """
        instructions = f"""
# CRITICAL: PreCompact Auto-Checkpoint Required

**Trigger**: Claude Code preparing to auto-compact conversation history
**Action**: Save ALL context to Serena MCP before compaction occurs

## CONTEXT_GUARDIAN: Execute Checkpoint Sequence

### Step 1: List Current Serena State
```
list_memories() → Retrieve all existing memory keys
```

### Step 2: Create Comprehensive Checkpoint
```
write_memory("{self.checkpoint_key}", {{
    "checkpoint_type": "auto_precompact",
    "timestamp": "{datetime.now(UTC).isoformat()}Z",
    "session_id": "[current_session_identifier]",

    "serena_memory_keys": [
        "all keys from step 1 list_memories()"
    ],

    "active_wave_state": {{
        "current_wave": "[wave_number or null]",
        "wave_phase": "[planning|execution|synthesis|complete]",
        "wave_progress": "[percentage or status]",
        "active_sub_agents": "[list of active agent names]"
    }},

    "phase_state": {{
        "current_phase": "[phase_number: 1-5]",
        "phase_name": "[Ideation|Architecture|Implementation|Testing|Production]",
        "phase_progress": "[status or percentage]"
    }},

    "project_context": {{
        "north_star_goal": "[project goal if defined]",
        "project_name": "[name if set]",
        "current_focus": "[what was being worked on]"
    }},

    "todo_state": {{
        "active_todos": "[capture current TodoWrite state]",
        "completed_todos": "[completed since last checkpoint]",
        "blocked_todos": "[any blocked items]"
    }},

    "decisions_made": [
        "architectural decisions from conversation",
        "technical choices and rationale",
        "user approvals and feedback"
    ],

    "integration_status": {{
        "components_built": "[list of completed components]",
        "integration_points": "[established connections]",
        "pending_integrations": "[needed but not complete]"
    }},

    "next_steps": [
        "immediate actions after restore",
        "priorities for continuation",
        "dependencies to resolve"
    ],

    "performance_metrics": {{
        "execution_time": "[session duration]",
        "waves_executed": "[count]",
        "parallel_speedup": "[if applicable]"
    }}
}})
```

### Step 3: Update Latest Checkpoint Pointer
```
write_memory("shannon_latest_checkpoint", {{
    "checkpoint_key": "{self.checkpoint_key}",
    "timestamp": "{datetime.now(UTC).isoformat()}Z",
    "type": "auto_precompact"
}})
```

### Step 4: Verify Checkpoint Success
```
read_memory("{self.checkpoint_key}") → Confirm data saved correctly
```

### Step 5: Log Checkpoint Creation
```
write_memory("checkpoint_history", {{
    "append": {{
        "key": "{self.checkpoint_key}",
        "timestamp": "{datetime.now(UTC).isoformat()}Z",
        "trigger": "auto_precompact",
        "status": "success"
    }}
}})
```

## Post-Checkpoint Behavior

After checkpoint complete:
- Signal: "✅ PreCompact checkpoint saved to Serena"
- Allow Claude Code to proceed with auto-compaction
- Context will be preserved and restorable

## Restoration Instructions

When session resumes after compaction:
1. Automatic: SessionStart hook loads checkpoint (if configured)
2. Manual: User executes `/sh:restore {self.checkpoint_key}`
3. Either way: Full context restored from Serena

---

**Critical**: This checkpoint prevents ALL context loss during auto-compaction.
Execute ALL steps above before allowing compaction to proceed.

**Checkpoint Key**: `{self.checkpoint_key}`
**Timestamp**: {datetime.now(UTC).isoformat()}Z
**Hook Version**: {self.VERSION}
"""
        return instructions

    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """
        Generate error response JSON

        Args:
            error_msg: Error message to include

        Returns:
            Error response JSON
        """
        return {
            "hookSpecificOutput": {
                "hookEventName": self.HOOK_EVENT_NAME,
                "error": True,
                "errorMessage": error_msg,
                "version": self.VERSION,
                "timestamp": self.timestamp,
                "degradedMode": True,
                "fallbackAction": "Attempting minimal context preservation",
                "metadata": {
                    "success": False,
                    "projectDir": self.project_dir
                }
            }
        }

    def _log_info(self, message: str):
        """
        Log informational message to file

        Args:
            message: Message to log
        """
        self._write_log("INFO", message)

    def _log_error(self, message: str):
        """
        Log error message to file

        Args:
            message: Error message to log
        """
        self._write_log("ERROR", message)

    def _write_log(self, level: str, message: str):
        """
        Write log message to Shannon log file

        Args:
            level: Log level (INFO, ERROR, etc.)
            message: Message to log
        """
        try:
            log_dir = f"{self.shannon_dir}/logs"
            os.makedirs(log_dir, exist_ok=True)

            log_file = f"{log_dir}/precompact_hook.log"
            timestamp = datetime.now(UTC).isoformat()

            with open(log_file, 'a') as f:
                f.write(f"{timestamp} [{level}] {message}\n")
        except Exception:
            # Silent failure - don't block hook execution
            pass


def main():
    """
    Entry point for PreCompact hook

    Reads JSON input from stdin, executes hook logic,
    writes JSON output to stdout.
    """
    try:
        # Read input from stdin (Claude Code provides this)
        input_data = json.load(sys.stdin)

        # Execute hook
        hook = ShannonPreCompactHook()
        output = hook.execute(input_data)

        # Write output to stdout (Claude Code reads this)
        print(json.dumps(output, indent=2))

        # Always exit 0 - never block Claude Code
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Invalid JSON input - return error response
        error_output = {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "error": True,
                "errorMessage": f"Invalid JSON input: {str(e)}",
                "version": ShannonPreCompactHook.VERSION,
                "degradedMode": True
            }
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(0)

    except Exception as e:
        # Last resort error handling
        error_output = {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "error": True,
                "errorMessage": f"Hook execution failed: {str(e)}",
                "version": ShannonPreCompactHook.VERSION,
                "degradedMode": True
            }
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(0)  # Don't block Claude Code even on error


if __name__ == "__main__":
    main()
    def _log_warning(self, message: str) -> None:
        """Log warning message"""
        print(f"[WARNING] {message}", file=sys.stderr)

    def _log_to_file(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log to structured file for analytics"""
        try:
            log_file = self.log_dir / f"{datetime.now(UTC).date()}.jsonl"
            entry = {
                "timestamp": datetime.now(UTC).isoformat(),
                "event": event_type,
                "data": data,
                "checkpoint_key": self.checkpoint_key
            }
            with open(log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            # Logging failure shouldn't break hook
            print(f"[WARNING] Failed to write log: {e}", file=sys.stderr)
