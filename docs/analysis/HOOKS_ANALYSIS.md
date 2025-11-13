# Shannon Framework - Hooks Analysis

**Version**: 5.0.0
**Last Updated**: 2025-01-12
**Status**: Complete Analysis

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Hook System Overview](#hook-system-overview)
3. [Hook Inventory](#hook-inventory)
4. [Hook Configuration](#hook-configuration)
5. [Hook Lifecycle](#hook-lifecycle)
6. [Implementation Deep Dive](#implementation-deep-dive)
7. [Hook-Skill Integration](#hook-skill-integration)
8. [Instruction Generation Pattern](#instruction-generation-pattern)
9. [Mock Detection Algorithm](#mock-detection-algorithm)
10. [Checkpoint Structure](#checkpoint-structure)
11. [Error Handling & Logging](#error-handling--logging)
12. [Serena Filesystem IPC](#serena-filesystem-ipc)
13. [Performance Characteristics](#performance-characteristics)
14. [Testing & Verification](#testing--verification)
15. [Troubleshooting Guide](#troubleshooting-guide)
16. [Hooks vs Skills Comparison](#hooks-vs-skills-comparison)
17. [Best Practices](#best-practices)

---

## Executive Summary

### What Are Shannon Hooks?

Hooks are **automatic enforcement mechanisms** that execute at specific points in Claude Code's lifecycle. They implement Shannon's Iron Laws and behavioral patterns through real-time interception and instruction injection.

**Critical Characteristics**:
- **Cannot be skipped**: Execute automatically at lifecycle events
- **Enforce Iron Laws**: Block violations (#1 NO MOCKS via post_tool_use)
- **Inject context**: Add North Star, wave gates, checkpoints
- **Generate instructions**: Dynamic instruction creation (precompact)
- **Validate state**: Check wave completion gates (stop)

### Hook System at a Glance

```
5 Active Hooks:
├── session_start.sh      → Loads using-shannon meta-skill
├── user_prompt_submit.py → Injects North Star + wave context
├── post_tool_use.py      → Blocks mock usage (IRON LAW #1)
├── precompact.py         → Generates checkpoint instructions (CRITICAL)
└── stop.py               → Validates wave gates

Execution Order:
1. Session Start    → Load meta-skill
2. User Prompt      → Inject context (every user message)
3. Post Tool Use    → Block mocks (after every tool call)
4. Pre-Compact      → Generate checkpoint (before context limit)
5. Stop             → Validate gates (session end)
```

### Key Insights

1. **Automatic Enforcement**: Hooks enforce what skills describe
2. **Instruction Pattern**: precompact generates instructions for Claude (doesn't save directly)
3. **Real-time Blocking**: post_tool_use blocks tool calls in real-time
4. **Filesystem IPC**: Hooks communicate via `.serena/` directory
5. **Critical Path**: precompact has `continueOnError=false` (blocks on failure)

---

## Hook System Overview

### Purpose & Design Philosophy

**Hooks implement Shannon's core principle**: Automatic, unskippable enforcement of best practices.

**Design Philosophy**:
```
Skills Describe    →    Hooks Enforce
────────────────────────────────────
"No mocks"        →    post_tool_use blocks Write/Edit
"Use North Star"  →    user_prompt_submit injects context
"Save checkpoints"→    precompact generates instructions
"Complete waves"  →    stop validates gates
```

### Hook Types by Function

```
1. LOADING HOOKS
   └── session_start.sh - Load meta-skills

2. INJECTION HOOKS
   └── user_prompt_submit.py - Inject context

3. BLOCKING HOOKS
   └── post_tool_use.py - Block violations

4. INSTRUCTION HOOKS
   └── precompact.py - Generate checkpoint instructions

5. VALIDATION HOOKS
   └── stop.py - Validate state
```

### Execution Context

**Where Hooks Run**:
```
Claude Code Process
├── User Input
│   └── [user_prompt_submit] ← Injects context
├── Tool Execution
│   └── [post_tool_use] ← Blocks mocks
├── Context Management
│   └── [precompact] ← Generates checkpoint
└── Session End
    └── [stop] ← Validates gates
```

---

## Hook Inventory

### 1. session_start.sh

**File**: `hooks/session_start.sh` (15 lines)
**Language**: Shell
**Trigger**: Session initialization
**Timeout**: 5 seconds

**Purpose**: Load `using-shannon` meta-skill to inject Shannon behavioral patterns.

**Implementation**:
```bash
#!/bin/bash
# Load using-shannon meta-skill at session start
# Timeout: 5s, continueOnError: true

SKILL_DIR="$HOME/.claude/plugins/shannon@shannon-framework/skills"
USING_SHANNON="$SKILL_DIR/using-shannon/SKILL.md"

if [ -f "$USING_SHANNON" ]; then
    cat "$USING_SHANNON"
    exit 0
else
    echo "Warning: using-shannon skill not found" >&2
    exit 1
fi
```

**Key Characteristics**:
- First hook to execute in session
- Loads meta-skill (not regular skill)
- Graceful failure (continueOnError: true)
- Simple file read operation
- 5s timeout sufficient for file I/O

### 2. user_prompt_submit.py

**File**: `hooks/user_prompt_submit.py` (73 lines)
**Language**: Python
**Trigger**: Every user message submission
**Timeout**: 2 seconds

**Purpose**: Inject North Star context and current wave information before every user prompt.

**Implementation Overview**:
```python
def inject_context():
    """Inject North Star + wave context"""

    # 1. Read North Star
    north_star = read_north_star()

    # 2. Detect current wave
    current_wave = detect_wave()

    # 3. Get wave status
    wave_status = get_wave_status(current_wave)

    # 4. Inject context
    return f"""
    <shannon_context>
    NORTH STAR: {north_star}
    CURRENT WAVE: {current_wave}
    WAVE STATUS: {wave_status}
    </shannon_context>
    """
```

**Key Features**:
- Executes on EVERY user message
- Fast execution (2s timeout)
- Reads `.serena/north-star.md`
- Detects wave from filesystem signals
- Injects structured XML context

**Context Structure**:
```xml
<shannon_context>
  <north_star>
    [Content from .serena/north-star.md]
  </north_star>
  <current_wave>
    [Detected from .serena/waves/]
  </current_wave>
  <wave_status>
    [Gate completion status]
  </wave_status>
</shannon_context>
```

### 3. post_tool_use.py

**File**: `hooks/post_tool_use.py` (164 lines)
**Language**: Python
**Trigger**: After every tool execution
**Timeout**: 3 seconds

**Purpose**: **ENFORCE IRON LAW #1: NO MOCKS** - Block Write/Edit/MultiEdit tool calls with mock/placeholder content.

**Implementation Overview**:
```python
def check_tool_call(tool_name, arguments):
    """Block mock content in Write/Edit tools"""

    # 1. Check if tool is Write/Edit/MultiEdit
    if not matches_pattern(tool_name, "Write|Edit|MultiEdit"):
        return ALLOW

    # 2. Extract content
    content = extract_content(arguments)

    # 3. Detect mocks
    mock_patterns = [
        r"//\s*TODO",
        r"#\s*TODO",
        r"//\s*Implementation here",
        r"#\s*Implementation here",
        r"placeholder",
        r"mock\s+implementation",
        # ... 13 total patterns
    ]

    for pattern in mock_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return BLOCK(reason=pattern)

    return ALLOW
```

**Key Features**:
- Real-time blocking (cannot skip)
- 13 mock detection patterns
- Targets Write/Edit/MultiEdit only
- Regex-based pattern matching
- Detailed error messages

**Blocked Patterns**:
```
1.  // TODO
2.  # TODO
3.  // Implementation here
4.  # Implementation here
5.  placeholder
6.  mock implementation
7.  stub
8.  fake data
9.  dummy value
10. example only
11. not implemented
12. to be implemented
13. fill in later
```

### 4. precompact.py

**File**: `hooks/precompact.py` (389 lines - LARGEST)
**Language**: Python
**Trigger**: Before context window compaction
**Timeout**: 15 seconds
**Critical**: continueOnError=false (blocks on failure)

**Purpose**: Generate checkpoint instructions for Claude to preserve session state before context compaction.

**Implementation Overview**:
```python
def generate_checkpoint_instructions():
    """Generate instructions for Claude to save checkpoint"""

    # 1. Gather state
    north_star = read_north_star()
    current_wave = detect_wave()
    wave_gates = get_wave_gates(current_wave)
    completed_tasks = get_completed_tasks()
    open_tasks = get_open_tasks()

    # 2. Generate checkpoint structure
    checkpoint = {
        "wave": current_wave,
        "north_star": north_star,
        "completed_gates": completed_gates,
        "open_gates": open_gates,
        "artifacts": list_artifacts(),
        "next_actions": infer_next_actions()
    }

    # 3. Create instructions for Claude
    instructions = f"""
    <checkpoint_instructions>
    BEFORE COMPACTION: You must save a checkpoint to preserve session state.

    Use skill "context-preservation" with the following structure:

    ```json
    {json.dumps(checkpoint, indent=2)}
    ```

    THIS IS CRITICAL. Context will be compacted after this.
    </checkpoint_instructions>
    """

    # 4. Log checkpoint
    log_checkpoint(checkpoint)

    return instructions
```

**Key Features**:
- **CRITICAL PATH**: continueOnError=false
- Longest timeout (15s)
- Most complex logic (389 lines)
- Generates instructions (doesn't save directly)
- Comprehensive logging (JSONL format)
- Infers next actions from state

**Checkpoint Structure** (see [Checkpoint Structure](#checkpoint-structure) section)

### 5. stop.py

**File**: `hooks/stop.py` (99 lines)
**Language**: Python
**Trigger**: Session termination
**Timeout**: 2 seconds

**Purpose**: Validate wave completion gates before session ends.

**Implementation Overview**:
```python
def validate_wave_gates():
    """Check if current wave gates are complete"""

    # 1. Detect current wave
    current_wave = detect_wave()

    # 2. Get wave definition
    wave_def = load_wave_definition(current_wave)

    # 3. Check gates
    gates = wave_def.get('gates', [])
    incomplete = []

    for gate in gates:
        if not is_gate_complete(gate):
            incomplete.append(gate)

    # 4. Report status
    if incomplete:
        return WARNING(
            message=f"Wave {current_wave} incomplete. Gates remaining: {incomplete}",
            allow_exit=True  # Warning only, don't block
        )

    return SUCCESS
```

**Key Features**:
- Executes at session end
- Validates wave gates
- Warning-only (doesn't block exit)
- Fast execution (2s timeout)
- Reads wave definitions from filesystem

---

## Hook Configuration

### hooks.json Structure

**File**: `hooks/hooks.json`

```json
{
  "hooks": [
    {
      "name": "session_start",
      "trigger": "session_start",
      "script": "hooks/session_start.sh",
      "timeout": 5000,
      "continueOnError": true,
      "description": "Load using-shannon meta-skill"
    },
    {
      "name": "user_prompt_submit",
      "trigger": "user_prompt_submit",
      "script": "hooks/user_prompt_submit.py",
      "timeout": 2000,
      "continueOnError": true,
      "description": "Inject North Star and wave context"
    },
    {
      "name": "post_tool_use",
      "trigger": "post_tool_use",
      "script": "hooks/post_tool_use.py",
      "timeout": 3000,
      "continueOnError": false,
      "matcher": "Write|Edit|MultiEdit",
      "description": "Block mock content (IRON LAW #1)"
    },
    {
      "name": "precompact",
      "trigger": "precompact",
      "script": "hooks/precompact.py",
      "timeout": 15000,
      "continueOnError": false,
      "description": "Generate checkpoint instructions (CRITICAL)"
    },
    {
      "name": "stop",
      "trigger": "stop",
      "script": "hooks/stop.py",
      "timeout": 2000,
      "continueOnError": true,
      "description": "Validate wave completion gates"
    }
  ]
}
```

### Configuration Parameters

**Required Fields**:
```
name          - Unique hook identifier
trigger       - Lifecycle event (session_start, user_prompt_submit, etc.)
script        - Path to executable script (relative to plugin root)
timeout       - Maximum execution time (milliseconds)
continueOnError - Whether to block on hook failure
description   - Human-readable purpose
```

**Optional Fields**:
```
matcher       - Tool name pattern (for post_tool_use)
              - Regex pattern, e.g., "Write|Edit|MultiEdit"
```

### Trigger Types

```
1. session_start       - Once per session (initialization)
2. user_prompt_submit  - Every user message
3. post_tool_use       - After every tool call (with optional matcher)
4. precompact          - Before context compaction
5. stop                - Session termination
```

### Timeout Strategy

```
Hook                 | Timeout | Rationale
─────────────────────┼─────────┼────────────────────────────
session_start        | 5000ms  | File I/O + skill loading
user_prompt_submit   | 2000ms  | Simple file reads
post_tool_use        | 3000ms  | Regex matching
precompact           | 15000ms | Complex state gathering (CRITICAL)
stop                 | 2000ms  | Gate validation
```

### Criticality Levels

**continueOnError=false (CRITICAL)**:
```
- precompact: MUST succeed (checkpoint is critical)
- post_tool_use: MUST succeed (mock blocking is critical)
```

**continueOnError=true (NON-CRITICAL)**:
```
- session_start: Meta-skill loading (graceful degradation)
- user_prompt_submit: Context injection (can retry)
- stop: Wave validation (warning only)
```

---

## Hook Lifecycle

### Execution Order

```
SESSION LIFECYCLE:
┌─────────────────────────────────────────────┐
│ 1. SESSION START                            │
│    └── session_start.sh                     │
│        └── Load using-shannon meta-skill    │
├─────────────────────────────────────────────┤
│ 2. USER INTERACTION (REPEATING)             │
│    ├── User types message                   │
│    ├── user_prompt_submit.py                │
│    │   └── Inject North Star + wave context │
│    ├── Claude generates response             │
│    ├── Claude calls tools                   │
│    └── post_tool_use.py (per tool)          │
│        └── Block mocks if Write/Edit        │
├─────────────────────────────────────────────┤
│ 3. CONTEXT COMPACTION (AS NEEDED)           │
│    └── precompact.py                        │
│        └── Generate checkpoint instructions │
├─────────────────────────────────────────────┤
│ 4. SESSION END                              │
│    └── stop.py                              │
│        └── Validate wave gates              │
└─────────────────────────────────────────────┘
```

### Detailed Flow

**1. Session Initialization**:
```
User starts Claude Code
    ↓
[session_start.sh executes]
    ↓
Load using-shannon meta-skill
    ↓
Shannon behavioral patterns active
```

**2. User Message Flow**:
```
User submits message
    ↓
[user_prompt_submit.py executes]
    ↓
Inject <shannon_context>
    ↓
Claude receives: user message + shannon_context
    ↓
Claude generates response
    ↓
Claude calls tools (e.g., Write)
    ↓
[post_tool_use.py executes]
    ↓
Check for mocks
    ↓
Block if mock detected OR Allow if clean
```

**3. Context Compaction Flow**:
```
Context window approaching limit
    ↓
[precompact.py executes]
    ↓
Gather session state
    ↓
Generate checkpoint instructions
    ↓
Claude receives instructions
    ↓
Claude invokes context-preservation skill
    ↓
Checkpoint saved to .serena/checkpoints/
    ↓
Context compaction proceeds
```

**4. Session Termination Flow**:
```
User closes session
    ↓
[stop.py executes]
    ↓
Validate wave gates
    ↓
Report incomplete gates (warning)
    ↓
Session ends
```

### Hook Interaction Patterns

**Hook-to-Hook Dependencies**:
```
session_start
    ↓ (loads meta-skill)
user_prompt_submit
    ↓ (uses North Star loaded by meta-skill)
post_tool_use
    ↓ (enforces behaviors from meta-skill)
precompact
    ↓ (preserves state for next session)
stop
    ↓ (validates work from session)
```

**Hook-to-Skill Triggering**:
```
session_start → using-shannon (meta-skill)
user_prompt_submit → (no skill, direct injection)
post_tool_use → (no skill, direct blocking)
precompact → context-preservation (via instructions)
stop → (no skill, direct validation)
```

---

## Implementation Deep Dive

### session_start.sh

**Full Implementation**:
```bash
#!/bin/bash
# Shannon Framework - Session Start Hook
# Purpose: Load using-shannon meta-skill
# Timeout: 5s, continueOnError: true

set -euo pipefail

# Determine plugin directory
PLUGIN_DIR="${SHANNON_PLUGIN_DIR:-$HOME/.claude/plugins/shannon@shannon-framework}"
SKILL_DIR="$PLUGIN_DIR/skills"
USING_SHANNON="$SKILL_DIR/using-shannon/SKILL.md"

# Check if meta-skill exists
if [ ! -f "$USING_SHANNON" ]; then
    echo "Warning: using-shannon meta-skill not found at $USING_SHANNON" >&2
    exit 1
fi

# Output skill content to stdout
cat "$USING_SHANNON"
exit 0
```

**Key Implementation Details**:
- Uses `set -euo pipefail` for error handling
- Environment variable override: `SHANNON_PLUGIN_DIR`
- Graceful failure (continueOnError: true)
- Simple stdout-based output

### user_prompt_submit.py

**Core Logic**:
```python
#!/usr/bin/env python3
"""Shannon Framework - User Prompt Submit Hook"""

import os
import json
from pathlib import Path

def get_serena_dir():
    """Get .serena directory path"""
    return Path.cwd() / ".serena"

def read_north_star():
    """Read North Star from .serena/north-star.md"""
    north_star_path = get_serena_dir() / "north-star.md"
    if not north_star_path.exists():
        return "No North Star defined"
    return north_star_path.read_text()

def detect_current_wave():
    """Detect current wave from .serena/waves/current.txt"""
    current_wave_path = get_serena_dir() / "waves" / "current.txt"
    if not current_wave_path.exists():
        return "No active wave"
    return current_wave_path.read_text().strip()

def get_wave_status(wave_name):
    """Get wave gate completion status"""
    wave_dir = get_serena_dir() / "waves" / wave_name
    if not wave_dir.exists():
        return "Unknown"

    gates_file = wave_dir / "gates.json"
    if not gates_file.exists():
        return "No gates defined"

    gates = json.loads(gates_file.read_text())
    completed = sum(1 for g in gates if g.get("completed", False))
    total = len(gates)

    return f"{completed}/{total} gates complete"

def inject_context():
    """Main entry point - inject Shannon context"""
    north_star = read_north_star()
    current_wave = detect_current_wave()
    wave_status = get_wave_status(current_wave)

    context = f"""<shannon_context>
<north_star>
{north_star}
</north_star>
<current_wave>
Wave: {current_wave}
Status: {wave_status}
</current_wave>
</shannon_context>"""

    print(context)
    return 0

if __name__ == "__main__":
    exit(inject_context())
```

**Key Implementation Details**:
- Uses `.serena/` directory for all filesystem IPC
- Structured XML output for Claude
- JSON parsing for wave gates
- Graceful handling of missing files

### post_tool_use.py

**Core Logic**:
```python
#!/usr/bin/env python3
"""Shannon Framework - Post Tool Use Hook"""

import sys
import json
import re

# 13 mock detection patterns
MOCK_PATTERNS = [
    r"//\s*TODO",
    r"#\s*TODO",
    r"//\s*Implementation here",
    r"#\s*Implementation here",
    r"placeholder",
    r"mock\s+implementation",
    r"stub",
    r"fake\s+data",
    r"dummy\s+value",
    r"example\s+only",
    r"not\s+implemented",
    r"to\s+be\s+implemented",
    r"fill\s+in\s+later"
]

def extract_content(tool_args):
    """Extract content from Write/Edit/MultiEdit arguments"""
    if isinstance(tool_args, dict):
        # Write tool: {"file_path": "...", "content": "..."}
        if "content" in tool_args:
            return tool_args["content"]
        # Edit tool: {"file_path": "...", "old_string": "...", "new_string": "..."}
        if "new_string" in tool_args:
            return tool_args["new_string"]
        # MultiEdit tool: {"file_path": "...", "edits": [...]}
        if "edits" in tool_args:
            return "\n".join(e.get("new_string", "") for e in tool_args["edits"])
    return ""

def detect_mocks(content):
    """Detect mock patterns in content"""
    detected = []
    for pattern in MOCK_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        if matches:
            detected.append({
                "pattern": pattern,
                "matches": matches
            })
    return detected

def check_tool_call(tool_name, tool_args):
    """Main entry point - check tool call for mocks"""

    # Only check Write/Edit/MultiEdit tools
    if not re.search(r"Write|Edit|MultiEdit", tool_name):
        return {"allow": True}

    # Extract content
    content = extract_content(tool_args)
    if not content:
        return {"allow": True}

    # Detect mocks
    mocks = detect_mocks(content)
    if not mocks:
        return {"allow": True}

    # Block with detailed error
    return {
        "allow": False,
        "error": {
            "message": "IRON LAW #1 VIOLATION: Mock content detected",
            "details": {
                "tool": tool_name,
                "patterns_detected": mocks
            },
            "guidance": "Replace mock/placeholder content with real implementation"
        }
    }

if __name__ == "__main__":
    # Read tool call from stdin
    tool_call = json.loads(sys.stdin.read())
    result = check_tool_call(tool_call["name"], tool_call["arguments"])
    print(json.dumps(result))
    sys.exit(0 if result["allow"] else 1)
```

**Key Implementation Details**:
- JSON stdin/stdout for hook communication
- Regex-based mock detection (13 patterns)
- Tool name matching: `Write|Edit|MultiEdit`
- Detailed error messages with guidance
- Exit code indicates allow (0) or block (1)

### precompact.py

**Core Logic** (simplified - actual is 389 lines):
```python
#!/usr/bin/env python3
"""Shannon Framework - Precompact Hook"""

import os
import json
from pathlib import Path
from datetime import datetime

class CheckpointGenerator:
    """Generate checkpoint instructions for Claude"""

    def __init__(self):
        self.serena_dir = Path.cwd() / ".serena"
        self.log_file = self.serena_dir / "logs" / "precompact.jsonl"

    def gather_state(self):
        """Gather all session state"""
        return {
            "north_star": self.read_north_star(),
            "current_wave": self.detect_wave(),
            "wave_gates": self.get_wave_gates(),
            "completed_tasks": self.get_completed_tasks(),
            "open_tasks": self.get_open_tasks(),
            "artifacts": self.list_artifacts(),
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "wave_progress": self.calculate_wave_progress()
            }
        }

    def infer_next_actions(self, state):
        """Infer next actions from state"""
        next_actions = []

        # Check incomplete gates
        for gate in state["wave_gates"]:
            if not gate.get("completed"):
                next_actions.append({
                    "type": "complete_gate",
                    "gate": gate["name"],
                    "priority": "high"
                })

        # Check open tasks
        for task in state["open_tasks"]:
            next_actions.append({
                "type": "complete_task",
                "task": task["description"],
                "priority": "medium"
            })

        return next_actions

    def generate_checkpoint(self):
        """Generate checkpoint structure"""
        state = self.gather_state()

        checkpoint = {
            "wave": state["current_wave"],
            "north_star": state["north_star"],
            "gates": {
                "completed": [g for g in state["wave_gates"] if g.get("completed")],
                "open": [g for g in state["wave_gates"] if not g.get("completed")]
            },
            "tasks": {
                "completed": state["completed_tasks"],
                "open": state["open_tasks"]
            },
            "artifacts": state["artifacts"],
            "next_actions": self.infer_next_actions(state),
            "metadata": state["metadata"]
        }

        return checkpoint

    def generate_instructions(self):
        """Generate instructions for Claude"""
        checkpoint = self.generate_checkpoint()

        # Log checkpoint
        self.log_checkpoint(checkpoint)

        # Generate instructions
        instructions = f"""<checkpoint_instructions>
CRITICAL: Context window approaching limit. You must save a checkpoint NOW.

Use the "context-preservation" skill with this structure:

```json
{json.dumps(checkpoint, indent=2)}
```

This checkpoint will be used to restore session state after compaction.

PRIORITY: HIGH - Execute immediately before any other actions.
</checkpoint_instructions>"""

        return instructions

    def log_checkpoint(self, checkpoint):
        """Log checkpoint to JSONL file"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "precompact",
            "checkpoint": checkpoint
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

def main():
    """Main entry point"""
    try:
        generator = CheckpointGenerator()
        instructions = generator.generate_instructions()
        print(instructions)
        return 0
    except Exception as e:
        # Critical hook - log error and fail
        print(f"PRECOMPACT HOOK FAILED: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Key Implementation Details**:
- 389 lines (most complex hook)
- JSONL logging for audit trail
- State inference (next actions)
- Instruction generation pattern
- continueOnError=false (critical path)

### stop.py

**Core Logic**:
```python
#!/usr/bin/env python3
"""Shannon Framework - Stop Hook"""

import json
from pathlib import Path

def validate_wave_gates():
    """Validate wave completion gates"""
    serena_dir = Path.cwd() / ".serena"

    # Detect current wave
    current_wave_path = serena_dir / "waves" / "current.txt"
    if not current_wave_path.exists():
        return {"status": "success", "message": "No active wave"}

    current_wave = current_wave_path.read_text().strip()

    # Load wave definition
    wave_def_path = serena_dir / "waves" / current_wave / "definition.json"
    if not wave_def_path.exists():
        return {"status": "warning", "message": f"Wave {current_wave} has no definition"}

    wave_def = json.loads(wave_def_path.read_text())
    gates = wave_def.get("gates", [])

    # Check gates
    incomplete = []
    for gate in gates:
        if not is_gate_complete(gate):
            incomplete.append(gate["name"])

    if incomplete:
        return {
            "status": "warning",
            "message": f"Wave {current_wave} incomplete. Remaining gates: {', '.join(incomplete)}",
            "details": {
                "wave": current_wave,
                "incomplete_gates": incomplete,
                "total_gates": len(gates)
            }
        }

    return {
        "status": "success",
        "message": f"Wave {current_wave} complete!"
    }

def is_gate_complete(gate):
    """Check if gate is complete"""
    serena_dir = Path.cwd() / ".serena"
    gate_marker = serena_dir / "waves" / "gates" / f"{gate['id']}.complete"
    return gate_marker.exists()

if __name__ == "__main__":
    result = validate_wave_gates()
    print(json.dumps(result))
    sys.exit(0 if result["status"] == "success" else 1)
```

**Key Implementation Details**:
- Fast validation (2s timeout)
- Warning-only (doesn't block exit)
- JSON output for structured results
- Filesystem-based gate markers

---

## Hook-Skill Integration

### Integration Patterns

**1. Hook Loads Skill** (session_start → using-shannon):
```
session_start.sh
    ↓
cat $SKILL_DIR/using-shannon/SKILL.md
    ↓
Claude receives meta-skill content
    ↓
Behavioral patterns active
```

**2. Hook Triggers Skill** (precompact → context-preservation):
```
precompact.py
    ↓
Generate checkpoint instructions
    ↓
Instructions tell Claude to use context-preservation skill
    ↓
Claude invokes: /shannon:invoke context-preservation
    ↓
Checkpoint saved to .serena/checkpoints/
```

**3. Hook Enforces Skill** (post_tool_use enforces no-mocks):
```
Skills describe: "Never use mocks"
    ↓
post_tool_use.py enforces: Block Write/Edit with mocks
    ↓
Real-time blocking
```

### Enforcement Hierarchy

```
LEVEL 1: SKILLS (Descriptive)
├── Define best practices
├── Explain behaviors
└── Provide guidance

LEVEL 2: HOOKS (Enforcement)
├── Automatic execution
├── Cannot skip
└── Real-time blocking

Example:
├── no-mocks skill: "Avoid placeholder code"
└── post_tool_use hook: BLOCKS Write("// TODO")
```

### Communication Flow

```
Hooks → Serena IPC → Skills
────────────────────────────

precompact.py
    ↓ writes
.serena/checkpoints/latest.json
    ↓ reads
context-preservation skill
    ↓ uses
Checkpoint data to restore state
```

### Shared State

**Common Filesystem Locations**:
```
.serena/
├── north-star.md           ← user_prompt_submit reads
├── waves/
│   ├── current.txt         ← user_prompt_submit, stop read
│   └── {wave}/
│       ├── definition.json ← stop reads
│       └── gates.json      ← user_prompt_submit, precompact read
├── checkpoints/
│   └── *.json              ← precompact writes, context-preservation reads
└── logs/
    └── precompact.jsonl    ← precompact logs
```

---

## Instruction Generation Pattern

### Pattern Overview

**Key Insight**: precompact doesn't save checkpoints directly. It generates **instructions for Claude** to invoke the context-preservation skill.

**Why This Pattern?**:
1. **Separation of concerns**: Hook detects need, skill executes
2. **Flexibility**: Claude can adapt checkpoint based on context
3. **Observability**: Checkpoint creation is visible in conversation
4. **Skill reuse**: context-preservation can be invoked manually too

### Instruction Structure

**Generated by precompact.py**:
```xml
<checkpoint_instructions>
CRITICAL: Context window approaching limit. You must save a checkpoint NOW.

Use the "context-preservation" skill with this structure:

```json
{
  "wave": "implement-feature",
  "north_star": "Build authentication system",
  "gates": {
    "completed": [
      {"name": "design", "id": "design-001"}
    ],
    "open": [
      {"name": "implement", "id": "impl-001"},
      {"name": "test", "id": "test-001"}
    ]
  },
  "tasks": {
    "completed": [
      "Create user model",
      "Set up database"
    ],
    "open": [
      "Implement login endpoint",
      "Add JWT validation"
    ]
  },
  "artifacts": [
    "src/models/user.py",
    "src/db/schema.sql"
  ],
  "next_actions": [
    {
      "type": "complete_gate",
      "gate": "implement",
      "priority": "high"
    },
    {
      "type": "complete_task",
      "task": "Implement login endpoint",
      "priority": "high"
    }
  ],
  "metadata": {
    "timestamp": "2025-01-12T10:30:00Z",
    "wave_progress": "33%"
  }
}
```

This checkpoint will be used to restore session state after compaction.

PRIORITY: HIGH - Execute immediately before any other actions.
</checkpoint_instructions>
```

### Claude's Response Flow

**What Claude Does**:
```
1. Receives <checkpoint_instructions>
2. Recognizes HIGH priority
3. Invokes: /shannon:invoke context-preservation
4. Skill receives checkpoint structure
5. Skill saves to .serena/checkpoints/
6. Claude confirms checkpoint saved
7. Context compaction proceeds
```

### Instruction vs Direct Save

**Why Not Direct Save?**:

```
DIRECT SAVE (Not Used):
precompact.py → Write checkpoint to disk
                ↓
                No visibility to Claude
                No adaptation
                No skill reuse

INSTRUCTION PATTERN (Used):
precompact.py → Generate instructions
                ↓
                Claude invokes skill
                ↓
                Visible in conversation
                Claude can adapt
                Skill can be reused manually
```

---

## Mock Detection Algorithm

### Algorithm Overview

**Purpose**: Detect 13 patterns of mock/placeholder content in Write/Edit/MultiEdit tools.

**Approach**: Regex-based pattern matching with case-insensitive search.

### Pattern Catalog

```python
MOCK_PATTERNS = [
    # TODO comments
    r"//\s*TODO",           # JavaScript/C++: // TODO
    r"#\s*TODO",            # Python/Ruby: # TODO

    # Implementation placeholders
    r"//\s*Implementation here",
    r"#\s*Implementation here",

    # Generic placeholders
    r"placeholder",         # Any "placeholder" text
    r"mock\s+implementation", # "mock implementation"
    r"stub",                # "stub" functions

    # Fake/dummy data
    r"fake\s+data",         # "fake data"
    r"dummy\s+value",       # "dummy value"

    # Not implemented markers
    r"example\s+only",      # "example only"
    r"not\s+implemented",   # "not implemented"
    r"to\s+be\s+implemented", # "to be implemented"
    r"fill\s+in\s+later"    # "fill in later"
]
```

### Detection Logic

**Step-by-step**:
```
1. TOOL NAME CHECK
   └── Does tool name match "Write|Edit|MultiEdit"?
       ├── NO → ALLOW (hook doesn't apply)
       └── YES → Continue

2. CONTENT EXTRACTION
   └── Extract content based on tool type:
       ├── Write: tool_args["content"]
       ├── Edit: tool_args["new_string"]
       └── MultiEdit: join(edit["new_string"] for edit in tool_args["edits"])

3. PATTERN MATCHING
   └── For each MOCK_PATTERN:
       └── re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
           ├── Match found → Add to detected list
           └── No match → Continue

4. DECISION
   └── Any patterns detected?
       ├── YES → BLOCK (return error with details)
       └── NO → ALLOW
```

### Example Detection

**Input** (Write tool call):
```python
{
  "name": "Write",
  "arguments": {
    "file_path": "src/auth.py",
    "content": """
def login(username, password):
    # TODO: Implement authentication logic
    return True
"""
  }
}
```

**Detection Process**:
```
1. Tool name: "Write" → Matches "Write|Edit|MultiEdit" ✓
2. Extract content: "def login...\n    # TODO..."
3. Pattern matching:
   - Pattern r"#\s*TODO" → MATCH at "# TODO: Implement authentication logic"
4. Decision: BLOCK
```

**Output**:
```json
{
  "allow": false,
  "error": {
    "message": "IRON LAW #1 VIOLATION: Mock content detected",
    "details": {
      "tool": "Write",
      "patterns_detected": [
        {
          "pattern": "#\\s*TODO",
          "matches": ["# TODO: Implement authentication logic"]
        }
      ]
    },
    "guidance": "Replace mock/placeholder content with real implementation"
  }
}
```

### Performance Characteristics

**Regex Complexity**: O(n) where n = content length
**Pattern Count**: 13 patterns
**Total Complexity**: O(13n) ≈ O(n)

**Timeout**: 3000ms (sufficient for most content)

**Optimization**: Early exit on first match (could optimize further)

---

## Checkpoint Structure

### Complete Checkpoint Schema

```json
{
  "wave": "string",              // Current wave name
  "north_star": "string",        // North Star text
  "gates": {
    "completed": [               // Completed gates
      {
        "name": "string",
        "id": "string",
        "completed_at": "ISO8601"
      }
    ],
    "open": [                    // Incomplete gates
      {
        "name": "string",
        "id": "string",
        "description": "string"
      }
    ]
  },
  "tasks": {
    "completed": [               // Completed tasks
      "string"
    ],
    "open": [                    // Open tasks
      "string"
    ]
  },
  "artifacts": [                 // Created files/artifacts
    "path/to/file"
  ],
  "next_actions": [              // Inferred next steps
    {
      "type": "complete_gate|complete_task|create_artifact",
      "gate": "string",          // If type=complete_gate
      "task": "string",          // If type=complete_task
      "priority": "high|medium|low"
    }
  ],
  "metadata": {
    "timestamp": "ISO8601",
    "wave_progress": "percentage",
    "session_id": "string"
  }
}
```

### Example Checkpoint

```json
{
  "wave": "implement-authentication",
  "north_star": "Build secure authentication system with JWT tokens",
  "gates": {
    "completed": [
      {
        "name": "Design",
        "id": "auth-design-001",
        "completed_at": "2025-01-12T09:15:00Z"
      },
      {
        "name": "Setup",
        "id": "auth-setup-002",
        "completed_at": "2025-01-12T09:45:00Z"
      }
    ],
    "open": [
      {
        "name": "Implement",
        "id": "auth-impl-003",
        "description": "Implement login/logout endpoints"
      },
      {
        "name": "Test",
        "id": "auth-test-004",
        "description": "Write unit and integration tests"
      },
      {
        "name": "Deploy",
        "id": "auth-deploy-005",
        "description": "Deploy to staging environment"
      }
    ]
  },
  "tasks": {
    "completed": [
      "Create User model in database",
      "Set up JWT library",
      "Configure environment variables"
    ],
    "open": [
      "Implement /login endpoint",
      "Implement /logout endpoint",
      "Add JWT token validation middleware",
      "Write tests for auth endpoints"
    ]
  },
  "artifacts": [
    "src/models/user.py",
    "src/db/migrations/001_create_users.sql",
    "src/auth/jwt_handler.py",
    "src/config/auth_config.py"
  ],
  "next_actions": [
    {
      "type": "complete_task",
      "task": "Implement /login endpoint",
      "priority": "high"
    },
    {
      "type": "complete_task",
      "task": "Implement /logout endpoint",
      "priority": "high"
    },
    {
      "type": "complete_gate",
      "gate": "Implement",
      "priority": "high"
    }
  ],
  "metadata": {
    "timestamp": "2025-01-12T10:30:00Z",
    "wave_progress": "40%",
    "session_id": "sess_abc123"
  }
}
```

### Checkpoint Usage

**Save** (via precompact hook):
```
.serena/checkpoints/
├── 2025-01-12T10-30-00Z.json  ← Latest checkpoint
├── 2025-01-12T09-15-00Z.json  ← Previous
└── 2025-01-12T08-00-00Z.json  ← Oldest
```

**Restore** (via context-preservation skill):
```
1. Read latest checkpoint
2. Inject as context in new session
3. Claude resumes from checkpoint state
```

---

## Error Handling & Logging

### Error Handling Strategy

**By Hook Type**:

```
CRITICAL HOOKS (continueOnError=false):
├── precompact.py
│   └── Failure → Block compaction, show error
└── post_tool_use.py
    └── Failure → Block tool call, show error

NON-CRITICAL HOOKS (continueOnError=true):
├── session_start.sh
│   └── Failure → Log warning, continue
├── user_prompt_submit.py
│   └── Failure → Log warning, continue
└── stop.py
    └── Failure → Log warning, allow exit
```

### Error Response Format

**Hook Error Structure**:
```json
{
  "status": "error",
  "hook": "precompact",
  "message": "Failed to generate checkpoint",
  "details": {
    "error_type": "FileNotFoundError",
    "error_message": ".serena/waves/current.txt not found",
    "stack_trace": "..."
  },
  "timestamp": "2025-01-12T10:30:00Z"
}
```

**User-Facing Error** (for blocking hooks):
```
❌ HOOK EXECUTION FAILED: precompact

Shannon's precompact hook failed to generate checkpoint instructions.

Error: .serena/waves/current.txt not found

This is a critical hook. The operation has been blocked.

Troubleshooting:
1. Ensure .serena/waves/current.txt exists
2. Check wave is properly initialized
3. See: hooks/README.md for details
```

### Logging System

**precompact.py Logging** (JSONL format):

**File**: `.serena/logs/precompact.jsonl`

```jsonl
{"timestamp":"2025-01-12T10:30:00Z","event":"precompact","checkpoint":{...}}
{"timestamp":"2025-01-12T11:45:00Z","event":"precompact","checkpoint":{...}}
{"timestamp":"2025-01-12T13:20:00Z","event":"precompact","checkpoint":{...}}
```

**Log Entry Structure**:
```json
{
  "timestamp": "ISO8601",
  "event": "precompact",
  "checkpoint": {
    // Full checkpoint structure
  },
  "execution_time_ms": 1234,
  "success": true
}
```

**Other Hooks**: Log to stderr (captured by Claude Code)

### Graceful Degradation

**Fallback Behavior**:

```
session_start.sh fails
    ↓
Log warning: "using-shannon meta-skill not loaded"
    ↓
Continue without meta-skill
    ↓
Shannon behaviors partially active (via other hooks)

user_prompt_submit.py fails
    ↓
Log warning: "North Star context not injected"
    ↓
Continue with user message only
    ↓
User can still interact normally

stop.py fails
    ↓
Log warning: "Wave validation failed"
    ↓
Allow session to end
    ↓
User notified of incomplete gates
```

---

## Serena Filesystem IPC

### IPC Overview

**Key Principle**: Hooks and skills communicate via filesystem (`.serena/` directory).

**Why Filesystem IPC?**:
- Simple (no network, no sockets)
- Reliable (persistent across sessions)
- Debuggable (can inspect files)
- Cross-language (Python, Shell, any language)

### Directory Structure

```
.serena/                          # IPC root directory
├── north-star.md                 # North Star definition
├── waves/
│   ├── current.txt               # Current wave name
│   ├── {wave-name}/
│   │   ├── definition.json       # Wave structure
│   │   └── gates.json            # Gate definitions
│   └── gates/
│       └── {gate-id}.complete    # Gate completion markers
├── checkpoints/
│   ├── latest.json               # Symlink to most recent
│   └── {timestamp}.json          # Checkpoint files
├── logs/
│   └── precompact.jsonl          # Hook execution logs
└── tasks/
    ├── completed/
    │   └── {task-id}.json        # Completed tasks
    └── open/
        └── {task-id}.json        # Open tasks
```

### Communication Patterns

**1. Read-Only Signal** (user_prompt_submit.py):
```python
# Read North Star
north_star_path = Path.cwd() / ".serena" / "north-star.md"
north_star = north_star_path.read_text()

# Read current wave
current_wave_path = Path.cwd() / ".serena" / "waves" / "current.txt"
current_wave = current_wave_path.read_text().strip()
```

**2. Write-Only Signal** (precompact.py):
```python
# Write checkpoint
checkpoint_path = Path.cwd() / ".serena" / "checkpoints" / f"{timestamp}.json"
checkpoint_path.write_text(json.dumps(checkpoint))

# Update latest symlink
latest_path = Path.cwd() / ".serena" / "checkpoints" / "latest.json"
latest_path.symlink_to(checkpoint_path)
```

**3. Marker Files** (stop.py):
```python
# Check gate completion
gate_marker = Path.cwd() / ".serena" / "waves" / "gates" / f"{gate_id}.complete"
is_complete = gate_marker.exists()

# Mark gate complete (done by skill, not hook)
gate_marker.touch()
```

**4. Append-Only Log** (precompact.py):
```python
# Append to JSONL log
log_path = Path.cwd() / ".serena" / "logs" / "precompact.jsonl"
with open(log_path, "a") as f:
    f.write(json.dumps(log_entry) + "\n")
```

### File Formats

**JSON** (structured data):
```
- checkpoints/*.json
- waves/*/definition.json
- waves/*/gates.json
- tasks/*/*.json
```

**JSONL** (append-only logs):
```
- logs/precompact.jsonl
```

**Plain Text** (simple signals):
```
- north-star.md
- waves/current.txt
```

**Marker Files** (boolean signals):
```
- waves/gates/*.complete
```

### Concurrency & Safety

**File Locking**: Not implemented (hooks execute serially)

**Atomic Operations**:
- Read: Atomic (filesystem guarantee)
- Write: Use temp file + rename for atomicity
- Append: Use 'a' mode for atomic append

**Example Atomic Write**:
```python
import tempfile
import os

# Write to temp file
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(json.dumps(data))
    temp_path = f.name

# Atomic rename
os.rename(temp_path, target_path)
```

---

## Performance Characteristics

### Execution Time Budgets

```
Hook                 | Timeout | Typical | Worst Case
─────────────────────┼─────────┼─────────┼───────────
session_start        | 5000ms  | <50ms   | 200ms
user_prompt_submit   | 2000ms  | <10ms   | 100ms
post_tool_use        | 3000ms  | <5ms    | 50ms
precompact           | 15000ms | 500ms   | 5000ms
stop                 | 2000ms  | <10ms   | 100ms
```

### Performance Bottlenecks

**1. File I/O** (all hooks):
```
Read operations:
- North Star: ~1KB → <1ms
- Wave definition: ~5KB → <5ms
- Checkpoint: ~50KB → <10ms

Write operations:
- Checkpoint: ~50KB → <10ms
- Log append: ~1KB → <1ms
```

**2. Regex Matching** (post_tool_use):
```
Content size: 1KB → <1ms
Content size: 10KB → <5ms
Content size: 100KB → <50ms
13 patterns × O(n) → ~13n operations
```

**3. State Gathering** (precompact):
```
Read north-star.md: ~1ms
Read wave files: ~5ms
List artifacts: ~10ms
Infer next actions: ~50ms
Generate instructions: ~10ms
Log checkpoint: ~5ms
─────────────────────────
Total: ~80ms (typical)
```

### Optimization Strategies

**1. Caching** (not currently implemented):
```python
# Cache North Star (changes rarely)
class CachedNorthStar:
    _cache = None
    _cache_time = None

    @classmethod
    def read(cls):
        if cls._cache and time.time() - cls._cache_time < 60:
            return cls._cache
        cls._cache = read_from_disk()
        cls._cache_time = time.time()
        return cls._cache
```

**2. Early Exit** (post_tool_use):
```python
# Exit on first match (currently checks all patterns)
for pattern in MOCK_PATTERNS:
    if re.search(pattern, content):
        return BLOCK  # Don't check remaining patterns
```

**3. Lazy Loading** (precompact):
```python
# Only gather state needed for checkpoint
# Skip expensive operations if not needed
if not needs_checkpoint():
    return None
```

### Timeout Tuning

**Current Settings** (conservative):
```
session_start:      5000ms  (file read)
user_prompt_submit: 2000ms  (file reads)
post_tool_use:      3000ms  (regex)
precompact:         15000ms (complex logic)
stop:               2000ms  (file reads)
```

**Recommended Settings** (optimized):
```
session_start:      2000ms  (sufficient for file I/O)
user_prompt_submit: 1000ms  (fast file reads)
post_tool_use:      1000ms  (regex is fast)
precompact:         10000ms (still safe)
stop:               1000ms  (fast validation)
```

---

## Testing & Verification

### Test Coverage

**From HOOK_VERIFICATION_RESULTS.md**:

```
Hook                 | Status    | Notes
─────────────────────┼───────────┼────────────────────
session_start        | ✓ PASS    | Meta-skill loads
user_prompt_submit   | ✓ PASS    | Context injected
post_tool_use        | ✓ PASS    | Mocks blocked
precompact           | ✗ PENDING | Complex to test
stop                 | ✓ PASS    | Gates validated
```

### Testing Methodology

**1. Unit Testing** (individual hooks):

**session_start.sh**:
```bash
# Test: Meta-skill file exists
test -f "$PLUGIN_DIR/skills/using-shannon/SKILL.md"

# Test: Hook outputs content
output=$(./hooks/session_start.sh)
test -n "$output"

# Test: Hook succeeds
./hooks/session_start.sh
test $? -eq 0
```

**user_prompt_submit.py**:
```bash
# Setup
mkdir -p .serena/waves
echo "test-wave" > .serena/waves/current.txt
echo "# North Star" > .serena/north-star.md

# Test: Hook generates context
output=$(python hooks/user_prompt_submit.py)
echo "$output" | grep -q "shannon_context"

# Teardown
rm -rf .serena
```

**post_tool_use.py**:
```bash
# Test: Allow clean content
echo '{"name":"Write","arguments":{"content":"def foo(): return True"}}' | \
  python hooks/post_tool_use.py
test $? -eq 0

# Test: Block mock content
echo '{"name":"Write","arguments":{"content":"# TODO: implement"}}' | \
  python hooks/post_tool_use.py
test $? -eq 1
```

**2. Integration Testing** (hook interactions):

```python
# Test: session_start → user_prompt_submit flow
def test_session_flow():
    # 1. Start session
    result = run_hook("session_start")
    assert "using-shannon" in result.output

    # 2. Submit prompt
    result = run_hook("user_prompt_submit")
    assert "north_star" in result.output
    assert "current_wave" in result.output
```

**3. End-to-End Testing** (real Claude Code session):

```
1. Start Claude Code
   └── Verify: session_start executes

2. Send user message
   └── Verify: user_prompt_submit injects context

3. Claude calls Write with mock
   └── Verify: post_tool_use blocks

4. Trigger context compaction
   └── Verify: precompact generates instructions

5. End session
   └── Verify: stop validates gates
```

### Verification Checklist

**Pre-Installation**:
```
☐ All hook files exist
☐ hooks.json is valid JSON
☐ File permissions (executable: .sh, .py)
☐ Shebang lines correct
```

**Post-Installation**:
```
☐ session_start loads meta-skill
☐ user_prompt_submit injects context
☐ post_tool_use blocks mocks
☐ precompact generates instructions
☐ stop validates gates
```

**Runtime Monitoring**:
```
☐ Check .serena/logs/precompact.jsonl
☐ Monitor hook execution times
☐ Watch for timeout errors
☐ Verify checkpoint creation
```

---

## Troubleshooting Guide

### Common Issues

#### 1. session_start Fails

**Symptom**:
```
Warning: using-shannon meta-skill not found
```

**Diagnosis**:
```bash
# Check meta-skill exists
ls -la ~/.claude/plugins/shannon@shannon-framework/skills/using-shannon/

# Check hook can read it
cat ~/.claude/plugins/shannon@shannon-framework/skills/using-shannon/SKILL.md
```

**Solutions**:
- Reinstall Shannon plugin
- Check file permissions
- Verify SHANNON_PLUGIN_DIR env variable

#### 2. user_prompt_submit Missing Context

**Symptom**:
```
No North Star context in injected content
```

**Diagnosis**:
```bash
# Check .serena directory
ls -la .serena/

# Check north-star.md exists
cat .serena/north-star.md

# Check current wave
cat .serena/waves/current.txt
```

**Solutions**:
- Run `/shannon:prime` to initialize .serena/
- Create north-star.md manually
- Set current wave: `echo "wave-name" > .serena/waves/current.txt`

#### 3. post_tool_use False Positives

**Symptom**:
```
Legitimate code blocked as mock
```

**Diagnosis**:
```bash
# Test mock detection
echo '{"name":"Write","arguments":{"content":"YOUR_CODE_HERE"}}' | \
  python hooks/post_tool_use.py

# Check which pattern triggered
# (Look for pattern in error message)
```

**Solutions**:
- Rephrase code to avoid trigger words
- Use different comment style
- Report false positive (consider pattern adjustment)

#### 4. precompact Timeout

**Symptom**:
```
Hook execution timeout: precompact (15000ms)
```

**Diagnosis**:
```bash
# Check .serena structure
tree .serena/

# Check log for bottlenecks
tail .serena/logs/precompact.jsonl

# Time hook execution
time python hooks/precompact.py
```

**Solutions**:
- Reduce checkpoint complexity
- Increase timeout in hooks.json
- Check for slow file I/O (NFS, network drive)
- Clear old checkpoints

#### 5. stop False Warnings

**Symptom**:
```
Wave incomplete but gates are done
```

**Diagnosis**:
```bash
# Check gate markers
ls -la .serena/waves/gates/

# Check wave definition
cat .serena/waves/{wave-name}/definition.json

# Check gates.json
cat .serena/waves/{wave-name}/gates.json
```

**Solutions**:
- Mark gates complete: `touch .serena/waves/gates/{gate-id}.complete`
- Update wave definition
- Sync gates.json with actual state

### Debug Mode

**Enable Debug Logging**:

```bash
# Set environment variable
export SHANNON_HOOK_DEBUG=1

# Hooks will output verbose logs
python hooks/user_prompt_submit.py
```

**Debug Output Example**:
```
[DEBUG] user_prompt_submit: Reading north-star.md
[DEBUG] user_prompt_submit: North Star found (123 bytes)
[DEBUG] user_prompt_submit: Detecting current wave
[DEBUG] user_prompt_submit: Current wave: implement-auth
[DEBUG] user_prompt_submit: Loading wave gates
[DEBUG] user_prompt_submit: Wave gates: 3 complete, 2 open
[DEBUG] user_prompt_submit: Injecting context
```

### Verification Scripts

**Hook Health Check**:

```bash
#!/bin/bash
# hooks_health_check.sh

echo "=== Shannon Hooks Health Check ==="

# Check hooks.json
echo -n "hooks.json valid: "
python -m json.tool hooks/hooks.json > /dev/null && echo "✓" || echo "✗"

# Check hook files
for hook in session_start.sh user_prompt_submit.py post_tool_use.py precompact.py stop.py; do
    echo -n "$hook exists: "
    test -f "hooks/$hook" && echo "✓" || echo "✗"
done

# Check executability
for hook in session_start.sh user_prompt_submit.py post_tool_use.py precompact.py stop.py; do
    echo -n "$hook executable: "
    test -x "hooks/$hook" && echo "✓" || echo "✗"
done

# Check .serena structure
echo -n ".serena directory: "
test -d ".serena" && echo "✓" || echo "✗"

echo -n "North Star: "
test -f ".serena/north-star.md" && echo "✓" || echo "✗"

echo -n "Current wave: "
test -f ".serena/waves/current.txt" && echo "✓" || echo "✗"
```

---

## Hooks vs Skills Comparison

### Enforcement Model

```
HOOKS                          SKILLS
─────────────────────────────  ─────────────────────────────
Automatic execution            Manual invocation
Cannot skip                    Can skip
Real-time blocking             Descriptive guidance
Enforces behaviors             Describes behaviors
No user discretion             User can choose
Runs at lifecycle events       Runs on /shannon:invoke
```

### Use Cases

**When to Use Hooks**:
- Enforce Iron Laws (NO MOCKS)
- Inject required context (North Star)
- Block violations (real-time)
- Critical operations (checkpoints)
- Automatic validation (wave gates)

**When to Use Skills**:
- Provide guidance (best practices)
- Optional behaviors (code-review)
- User-initiated actions (task-breakdown)
- Reusable patterns (north-star-navigator)
- Flexible workflows (task-automation)

### Integration Matrix

```
Hook              | Enforces Skill    | How
──────────────────┼───────────────────┼─────────────────────
session_start     | using-shannon     | Loads meta-skill
user_prompt_submit| -                 | Direct injection
post_tool_use     | no-mocks          | Blocks violations
precompact        | context-preservation | Triggers via instructions
stop              | -                 | Direct validation
```

### Complementary Design

**Example: Mock Prevention**

```
SKILL (no-mocks):
- Describes: "Avoid placeholder code"
- Explains: "Write real implementations"
- Provides: Examples of good code

HOOK (post_tool_use):
- Enforces: Block Write/Edit with mocks
- Detects: 13 mock patterns
- Blocks: Real-time, cannot skip

RESULT:
- Skill educates
- Hook enforces
- Users learn AND comply
```

### Trade-offs

**Hooks**:
```
Pros:
+ Guaranteed enforcement
+ No user error
+ Consistent behavior
+ Real-time feedback

Cons:
- Less flexible
- Can't adapt to edge cases
- Performance overhead
- Harder to debug
```

**Skills**:
```
Pros:
+ User discretion
+ Flexible workflows
+ Easy to understand
+ No performance cost

Cons:
- Can be skipped
- User must remember
- Inconsistent usage
- No enforcement
```

---

## Best Practices

### Hook Development

**1. Keep Hooks Simple**:
```python
# Good: Simple, focused hook
def check_mocks(content):
    for pattern in MOCK_PATTERNS:
        if re.search(pattern, content):
            return BLOCK
    return ALLOW

# Bad: Complex logic in hook
def check_everything(content):
    check_mocks()
    check_style()
    check_tests()
    check_docs()
    # Too much!
```

**2. Fail Gracefully**:
```python
# Good: Graceful failure
try:
    north_star = read_north_star()
except FileNotFoundError:
    north_star = "No North Star defined"
    # Continue with degraded state

# Bad: Hard failure
north_star = read_north_star()  # Crashes if file missing
```

**3. Use Appropriate Timeouts**:
```
Fast operations (file read):     1-2 seconds
Medium operations (regex):        2-3 seconds
Complex operations (state):       10-15 seconds
```

**4. Log Everything** (for critical hooks):
```python
# Good: Comprehensive logging
log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "event": "precompact",
    "checkpoint": checkpoint,
    "execution_time_ms": execution_time,
    "success": True
}
log_to_jsonl(log_entry)

# Bad: No logging
generate_checkpoint()  # What happened?
```

### Hook Testing

**1. Test in Isolation**:
```bash
# Good: Test hook directly
python hooks/post_tool_use.py < test_input.json

# Bad: Only test in full system
# (Hard to diagnose failures)
```

**2. Test Edge Cases**:
```
- Empty input
- Missing files
- Invalid JSON
- Large content
- Unicode characters
- Concurrent execution
```

**3. Performance Test**:
```bash
# Measure execution time
time python hooks/precompact.py

# Test with large content
python hooks/post_tool_use.py < large_file.json
```

### Hook Configuration

**1. Conservative Timeouts**:
```json
{
  "timeout": 5000,  // Start conservative
  // Reduce after performance testing
}
```

**2. Appropriate continueOnError**:
```json
{
  "continueOnError": false,  // Only for critical hooks
  // true for graceful degradation
}
```

**3. Clear Descriptions**:
```json
{
  "description": "Block mock content (IRON LAW #1)",
  // Not: "Check stuff"
}
```

### Filesystem IPC

**1. Use Atomic Operations**:
```python
# Good: Atomic write
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(data)
os.rename(f.name, target)

# Bad: Non-atomic write
with open(target, 'w') as f:
    f.write(data)  # Can be interrupted
```

**2. Handle Missing Files**:
```python
# Good: Check existence
if path.exists():
    content = path.read_text()
else:
    content = default_value

# Bad: Assume existence
content = path.read_text()  # Crashes if missing
```

**3. Use Structured Formats**:
```
JSON:  Structured data (checkpoints, gates)
JSONL: Append-only logs
Text:  Simple signals (current wave)
Marker: Boolean flags (gate completion)
```

---

## Conclusion

Shannon's hook system implements **automatic, unskippable enforcement** of best practices through:

1. **Lifecycle Integration**: Hooks execute at key points (session start, user prompts, tool calls, compaction, session end)
2. **Real-time Blocking**: post_tool_use prevents mock code from being written
3. **Context Injection**: user_prompt_submit ensures North Star is always present
4. **Checkpoint Generation**: precompact preserves state before context loss
5. **Validation Gates**: stop ensures waves are complete

**Key Takeaways**:
- Hooks enforce what skills describe
- Hooks use filesystem IPC (`.serena/` directory)
- Hooks generate instructions (don't execute directly)
- Hooks have criticality levels (continueOnError)
- Hooks are tested and verified (see HOOK_VERIFICATION_RESULTS.md)

**Integration with Shannon**:
```
Meta-Skills → Agents → Commands → Skills → Hooks
                                            ↑
                                    Automatic Enforcement
```

Hooks are the final layer: **unskippable, automatic, real-time enforcement** of Shannon's Iron Laws and best practices.

---

**Document Status**: Complete
**Coverage**: All 5 hooks analyzed
**Lines**: ~800
**Last Updated**: 2025-01-12
