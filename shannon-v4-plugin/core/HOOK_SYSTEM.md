---
name: HOOK_SYSTEM
description: Behavioral instructions for Claude Code hook system integration with Shannon Framework
category: core-behavioral
priority: critical
triggers: [hook, context-injection, precompact, memory-checkpoint]
auto_activate: true
mcp_servers: [serena]
---

# Hook System Behavioral Framework

> **Purpose**: Define how Shannon Framework integrates with Claude Code's hook system to preserve context, prevent information loss during auto-compaction, and maintain session continuity through memory checkpoints.

This document provides behavioral instructions for implementing and operating Shannon's hook-based integration with Claude Code. The hook system is Shannon's primary mechanism for injecting contextual awareness and preventing context loss during Claude Code's automatic session compaction.

---

## Table of Contents

1. [Hook System Overview](#hook-system-overview)
2. [PreCompact Hook - Critical Context Preservation](#precompact-hook-critical-context-preservation)
3. [Hook Activation Logic](#hook-activation-logic)
4. [Hook Output Format Specification](#hook-output-format-specification)
5. [Integration with Serena MCP](#integration-with-serena-mcp)
6. [Hook Installation and Deployment](#hook-installation-and-deployment)
7. [Testing and Validation](#testing-and-validation)
8. [Hook Development Guidelines](#hook-development-guidelines)

---

## 1. Hook System Overview

### What Hooks Do

**Core Purpose**: Hooks are executable scripts that Claude Code invokes at specific lifecycle events to augment AI behavior with external intelligence and context.

**Shannon's Hook Strategy**:
```yaml
context_preservation:
  mechanism: "Hooks capture critical state before context loss"
  storage: "Serena MCP memory graph"
  retrieval: "Subsequent sessions load from memory"
  benefit: "Perfect session continuity despite compaction"

intelligent_augmentation:
  mechanism: "Hooks inject relevant context into prompts"
  selection: "Query Serena for task-relevant memories"
  injection: "Append context to system prompt"
  benefit: "AI has full project history without manual loading"

lifecycle_awareness:
  mechanism: "Hooks execute at key Claude Code lifecycle events"
  events: ["SessionStart", "UserPromptSubmit", "PreCompact", "PostToolUse"]
  coordination: "Serena MCP orchestrates state management"
  benefit: "Seamless integration with Claude Code workflows"
```

### Hook Types in Shannon

**SessionStart Hook**:
- **When**: Claude Code session begins
- **Purpose**: Load project context from previous sessions
- **Action**: Query Serena, inject project history into initial prompt
- **Benefit**: AI starts with full awareness of project state

**UserPromptSubmit Hook**:
- **When**: User submits a Shannon command (`/shannon:*`)
- **Purpose**: Inject command-specific context and wave strategies
- **Action**: Load relevant memories, select wave strategy, augment prompt
- **Benefit**: Commands execute with full project context

**PreCompact Hook** (CRITICAL):
- **When**: Claude Code prepares to compact conversation history
- **Purpose**: Preserve essential context before it's lost
- **Action**: Extract critical state, save to Serena, create checkpoint
- **Benefit**: Zero information loss during compaction

**PostToolUse Hook**:
- **When**: After tool execution completes
- **Purpose**: Track performance, update coordination state
- **Action**: Log metrics, update wave progress, detect drift
- **Benefit**: Real-time coordination and performance monitoring

---

## 2. PreCompact Hook - Critical Context Preservation

### The Compaction Problem

**Claude Code Auto-Compaction**:
```markdown
Problem: Claude Code automatically compacts conversation history when approaching token limits

What Gets Lost:
- Tool use results and outputs
- Intermediate reasoning and decisions
- Task progress and todo lists
- Agent coordination state
- Wave execution history
- Performance metrics
- User feedback and approvals

Impact Without PreCompact Hook:
- AI "forgets" what was accomplished
- Duplicate work across sessions
- Lost architectural decisions
- Broken wave continuity
- Cannot resume complex tasks
```

### PreCompact Hook Solution

**Behavioral Pattern**:
```markdown
WHEN Claude Code signals impending compaction:

1. INTERCEPT before compaction occurs
   Trigger: PreCompact hook executes

2. EXTRACT critical state from conversation
   What to preserve:
   - Active todos and their status
   - Completed work and deliverables
   - Architectural decisions made
   - Wave progress and phase
   - Integration points established
   - User approvals and feedback
   - Performance metrics
   - Open issues and blockers

3. SAVE to Serena memory graph
   How to save:
   - write_memory("session_checkpoint_[timestamp]", state)
   - write_memory("active_todos_snapshot", todos)
   - write_memory("wave_progress_snapshot", progress)
   - Update existing wave_complete memories if needed

4. CONFIRM preservation
   What to verify:
   - All critical state saved successfully
   - Serena confirms write operations
   - Checkpoint is retrievable
   - No data corruption

5. ALLOW compaction
   Only after preservation complete:
   - Signal Claude Code: safe to compact
   - Compaction proceeds
   - Context lost from conversation
   - BUT preserved in Serena

6. RESUME after compaction
   Next prompt:
   - SessionStart hook loads checkpoint
   - AI continues seamlessly
   - User sees no interruption
   - Work continues without duplication
```

### What PreCompact Hook Preserves

**Essential State Categories**:

```javascript
// PreCompact extracts and saves this structure
checkpoint = {
  // Session Identity
  session_id: "unique-session-id",
  checkpoint_timestamp: "2024-01-15T14:30:00Z",
  compaction_trigger: "token_limit_75_percent",

  // Project Context
  project_name: "TaskTracker Pro",
  north_star_goal: "Build production-ready task management system",
  current_phase: "Phase 2: Implementation",
  current_wave: "Wave 2b: Post-Core Implementation",

  // Active Work State
  active_todos: [
    {
      description: "Build state management with Redux Toolkit",
      status: "in_progress",
      assignee: "state-manager-agent",
      started_at: "2024-01-15T14:00:00Z"
    }
    // ... all active todos
  ],

  // Completed Work
  completed_work: {
    waves_complete: ["Wave 1", "Wave 2a"],
    components_built: ["TaskCard", "TaskList", "TaskForm", "API endpoints", "Database schema"],
    tests_created: 15,
    files_modified: ["src/components/*", "server/api/*", "db/migrations/*"]
  },

  // Critical Decisions
  decisions_made: [
    "Using TypeScript for type safety",
    "Material-UI for component library",
    "PostgreSQL for database",
    "Redux Toolkit for state management"
  ],

  // Integration Points
  integration_status: {
    frontend_backend: "established",
    backend_database: "established",
    state_management: "in_progress",
    testing: "partial"
  },

  // Wave Coordination
  wave_progress: {
    current_wave: "Wave 2b",
    agents_active: 1,
    agents_complete: 2,
    estimated_completion: "5 minutes",
    dependencies_satisfied: ["Wave 2a complete"]
  },

  // User Feedback
  user_approvals: [
    {wave: "Wave 1", approved: true, feedback: "Architecture looks good"},
    {wave: "Wave 2a", approved: true, feedback: "Components work perfectly"}
  ],

  // Open Issues
  issues: [
    {
      type: "blocker",
      description: "State management needs API integration",
      wave: "Wave 2b",
      resolution: "pending Wave 2b completion"
    }
  ],

  // Performance Metrics
  metrics: {
    total_execution_time: 45,
    parallel_speedup: "2.5x",
    token_efficiency: "87%",
    waves_executed: 3
  },

  // Next Steps
  next_actions: [
    "Complete Wave 2b state management",
    "Synthesize Wave 2b results",
    "Get user approval",
    "Proceed to Wave 2c testing"
  ]
}
```

### PreCompact Hook Execution Flow

**Step-by-Step Behavior**:

```markdown
## PreCompact Hook Execution

### Signal Detection
Claude Code: "Conversation approaching token limit (75%)"
→ Triggers PreCompact hook execution

### Hook Activation
Python script: shannon_precompact_hook.py
→ Receives conversation transcript as input
→ Has ~5 seconds to complete (timeout limit)

### State Extraction Phase
1. Parse conversation transcript:
   - Identify TodoWrite calls (extract todos)
   - Find completed tasks (status updates)
   - Extract Serena write_memory operations (decisions saved)
   - Locate user approvals (explicit confirmations)
   - Identify wave boundaries (synthesis points)

2. Build state snapshot:
   - Active todos from TodoWrite
   - Completed work from agent results
   - Decisions from conversation history
   - Wave progress from coordination tracking
   - Integration status from synthesis

3. Validate completeness:
   Check: All active todos captured?
   Check: All completed work logged?
   Check: All critical decisions preserved?
   Check: Wave state accurate?
   If incomplete: Log warning, save partial state

### Serena Persistence Phase
1. Connect to Serena MCP:
   subprocess: claude mcp call serena write_memory

2. Save checkpoint:
   write_memory("session_checkpoint_[timestamp]", checkpoint)
   write_memory("active_todos_snapshot_[timestamp]", active_todos)
   write_memory("wave_progress_snapshot_[timestamp]", wave_progress)

3. Update continuity chain:
   write_memory("latest_checkpoint", "session_checkpoint_[timestamp]")
   This allows SessionStart to find most recent state

4. Verify persistence:
   Query Serena: read_memory("session_checkpoint_[timestamp]")
   If read succeeds: Persistence confirmed ✓
   If read fails: Retry save, escalate if still fails

### Output Generation Phase
Hook returns JSON to Claude Code:
{
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "preservationStatus": "success",
    "checkpointKey": "session_checkpoint_[timestamp]",
    "itemsPreserved": {
      "todos": 5,
      "decisions": 12,
      "wavesComplete": 2,
      "metricsLogged": true
    }
  }
}

Claude Code receives confirmation, proceeds with compaction

### Post-Compaction Recovery
Next user prompt after compaction:
→ SessionStart hook executes
→ Loads: read_memory("latest_checkpoint")
→ Injects checkpoint state into prompt
→ AI continues with full context restored
→ User experiences seamless continuation
```

---

## 3. Hook Activation Logic

### Event-Based Activation

**Activation Rules**:

```yaml
SessionStart:
  when: "Claude Code session begins"
  condition: "Always (every session)"
  timeout: 3000ms
  purpose: "Load project context from previous sessions"

UserPromptSubmit:
  when: "User submits prompt"
  condition: "Prompt matches pattern: /shannon:.*"
  timeout: 5000ms
  purpose: "Inject Shannon command context"

PreCompact:
  when: "Token usage crosses threshold"
  condition: "Always (automatic trigger)"
  timeout: 5000ms
  purpose: "Preserve context before compaction"
  critical: true

PostToolUse:
  when: "After any tool execution"
  condition: "Tool name matches: Task|TodoWrite|Write|Edit"
  timeout: 2000ms
  purpose: "Track coordination and performance"
```

### Matcher Patterns

**UserPromptSubmit Matchers**:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "^/shannon:.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_context_injector.py"
          }
        ]
      },
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_universal_context.py"
          }
        ]
      }
    ]
  }
}
```

**Explanation**:
- First matcher: Shannon commands get full context injection
- Second matcher: All prompts get basic context (North Star, phase, wave)
- Order matters: Specific matchers before general

### Conditional Execution

**Smart Activation**:

```python
def should_hook_execute(hook_type, context):
    """
    Determine if hook should execute based on context
    """
    if hook_type == "SessionStart":
        # Always execute to load context
        return True

    if hook_type == "PreCompact":
        # Always execute to preserve state
        return True

    if hook_type == "UserPromptSubmit":
        prompt = context.get("prompt", "")
        # Execute for Shannon commands
        if prompt.startswith("/shannon:"):
            return True
        # Execute if project has active Shannon session
        if serena_has_active_session():
            return True
        return False

    if hook_type == "PostToolUse":
        tool_name = context.get("tool_name", "")
        # Only for coordination-relevant tools
        return tool_name in ["Task", "TodoWrite", "Write", "Edit", "MultiEdit"]

    return False
```

### Timeout Management

**Behavioral Rules**:

```markdown
Hook Timeout Protocol:

1. Timeout Limits (Claude Code enforced):
   - SessionStart: 3000ms (3 seconds)
   - UserPromptSubmit: 5000ms (5 seconds)
   - PreCompact: 5000ms (5 seconds) - CRITICAL
   - PostToolUse: 2000ms (2 seconds)

2. Hook Behavior Under Timeout Pressure:
   - Fast path: If Serena responds quickly (<1s), full processing
   - Slow path: If Serena slow (>1s), use cached data
   - Emergency path: If timeout imminent, return partial results
   - Never block: ALWAYS return within timeout, even if incomplete

3. Partial Results Strategy:
   If timeout approaching:
   - Return what's been computed so far
   - Set flag: "incomplete: true" in output
   - Log missing data for later recovery
   - AI continues with partial context (better than none)

4. Timeout Recovery:
   If hook times out:
   - Claude Code continues without hook output
   - SessionStart: AI has no context (degraded but functional)
   - PreCompact: Context not preserved (risk of information loss)
   - PostToolUse: Metrics not logged (minor impact)
   - User experience: May notice AI "forgot" things
   - Resolution: User can manually trigger context reload
```

---

## 4. Hook Output Format Specification

### JSON Structure

**Standard Hook Output**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart|UserPromptSubmit|PreCompact|PostToolUse",
    "additionalContext": "string - text to inject into system prompt",
    "metadata": {
      "executionTime": 1234,
      "success": true,
      "itemsProcessed": 5,
      "serenaQueries": 3,
      "cacheHits": 2
    }
  }
}
```

**Field Specifications**:

```yaml
hookSpecificOutput:
  required: true
  type: object
  description: "Container for all hook-specific data"

hookEventName:
  required: true
  type: string
  enum: ["SessionStart", "UserPromptSubmit", "PreCompact", "PostToolUse"]
  description: "Identifies which hook is responding"

additionalContext:
  required: false
  type: string
  description: "Text to append to system prompt (SessionStart, UserPromptSubmit only)"
  max_length: 4000
  format: "markdown"

metadata:
  required: false
  type: object
  description: "Operational data for debugging and optimization"
```

### Context Injection Format

**SessionStart Context Injection**:

```markdown
# Shannon Framework - Session Resumption

## Project Context Restored

**Project**: {project_name}
**North Star Goal**: {north_star_goal}
**Current Phase**: {phase_number} - {phase_name}
**Current Wave**: {wave_number} - {wave_name}

## Previous Session Summary

**Waves Completed**: {list of completed waves}
**Components Built**: {count} components
**Tests Created**: {count} functional tests (NO MOCKS)
**Critical Decisions Made**: {count}

## Active Work

**Todos in Progress**:
{list of active todos with status}

**Current Focus**: {what was being worked on when session ended}

## Integration Status

{summary of component integration state}

## Next Steps

{recommended actions based on project state}

---

**Instructions**: Continue the project with full awareness of the above context. All previous decisions and work are preserved in Serena memory graph. You can query additional details using Serena MCP tools.
```

**UserPromptSubmit Context Injection** (Shannon commands):

```markdown
# Shannon Command Context

## Command: {command_name}

## Relevant Memory Context

{query results from Serena based on command type}

## Wave Strategy

{selected wave strategy template for this command}

## Coordination Rules

1. Maintain alignment with North Star goal
2. Update wave progress after each agent completion
3. Preserve all decisions to Serena
4. Track metrics for performance optimization
5. Detect and correct context drift

---

**Instructions**: Execute this Shannon command with full project awareness and coordination tracking.
```

### Error Handling in Output

**Error Response Format**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "error": true,
    "errorMessage": "Failed to connect to Serena MCP",
    "errorDetails": {
      "component": "serena_client",
      "attemptedRetries": 2,
      "lastError": "Connection timeout after 2000ms"
    },
    "fallbackAction": "Using cached context from 5 minutes ago",
    "degradedMode": true
  }
}
```

**Behavioral Rules for Errors**:

```markdown
When Hook Encounters Error:

1. DO NOT raise exception (would block Claude Code)
2. DO capture error details in output JSON
3. DO attempt fallback strategies:
   - Use cached data if available
   - Use partial results if computed
   - Use empty context if no alternatives
4. DO set degradedMode flag to true
5. DO log error to file for later debugging
6. DO return valid JSON within timeout

Effect on AI:
- AI receives error notification in context
- AI knows to operate with degraded information
- AI can inform user of degraded state
- AI can suggest manual recovery actions
```

---

## 5. Integration with Serena MCP

### Why Serena for Hooks

**Serena's Role**:

```yaml
persistent_storage:
  need: "Hooks must save state across sessions"
  serena: "Knowledge graph persists between Claude Code sessions"
  alternative: "Files (less structured, harder to query)"

semantic_retrieval:
  need: "Hooks must find relevant context efficiently"
  serena: "Graph queries: search_nodes, open_nodes"
  alternative: "File search (slower, less precise)"

relationship_tracking:
  need: "Understand relationships between entities"
  serena: "Native graph relations and connections"
  alternative: "Manual tracking in JSON (complex)"

session_continuity:
  need: "Link sessions together over time"
  serena: "Entities can reference previous sessions"
  alternative: "Timestamps and naming conventions (fragile)"
```

### Hook-Serena Communication Pattern

**Calling Serena from Hooks**:

```python
import subprocess
import json

def serena_write_memory(key, value):
    """
    Save memory to Serena MCP from hook
    """
    payload = {
        "memory_name": key,
        "content": json.dumps(value)
    }

    try:
        result = subprocess.run(
            ['claude', 'mcp', 'call', 'serena', 'write_memory'],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=2  # 2 second timeout
        )

        if result.returncode == 0:
            return {"success": True, "key": key}
        else:
            return {"success": False, "error": result.stderr}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Serena timeout"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def serena_read_memory(key):
    """
    Read memory from Serena MCP in hook
    """
    payload = {"memory_file_name": key}

    try:
        result = subprocess.run(
            ['claude', 'mcp', 'call', 'serena', 'read_memory'],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=1
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return None

    except Exception:
        return None


def serena_search_nodes(query):
    """
    Search Serena knowledge graph from hook
    """
    payload = {"query": query}

    try:
        result = subprocess.run(
            ['claude', 'mcp', 'call', 'serena', 'search_nodes'],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=1
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return []

    except Exception:
        return []
```

### Memory Key Conventions

**Standard Memory Keys**:

```yaml
Checkpoints:
  format: "session_checkpoint_{timestamp}"
  example: "session_checkpoint_20240115_143000"
  usage: "PreCompact hook saves, SessionStart hook loads"

Todo Snapshots:
  format: "active_todos_snapshot_{timestamp}"
  example: "active_todos_snapshot_20240115_143000"
  usage: "PreCompact hook saves current TodoWrite state"

Wave Progress:
  format: "wave_progress_snapshot_{timestamp}"
  example: "wave_progress_snapshot_20240115_143000"
  usage: "Track which wave is active and agent status"

Latest Pointer:
  key: "latest_checkpoint"
  value: "{most_recent_checkpoint_key}"
  usage: "SessionStart always reads this to find newest checkpoint"

Performance Metrics:
  format: "metrics_{session_id}"
  example: "metrics_session_abc123"
  usage: "PostToolUse hook accumulates performance data"
```

### Error Recovery with Serena

**Fallback Strategy**:

```markdown
Hook-Serena Communication Failure Scenarios:

Scenario 1: Serena MCP Not Available
→ Cause: Serena not installed or not running
→ Detection: subprocess call fails immediately
→ Recovery:
  - Use last known cached state (if any)
  - Set degradedMode: true
  - Continue with empty context
  - Log error for user notification

Scenario 2: Serena Timeout
→ Cause: Serena slow to respond (>2 seconds)
→ Detection: subprocess.TimeoutExpired exception
→ Recovery:
  - Use cached data from previous hook execution
  - Set degradedMode: true
  - Return partial results
  - Suggest user restart Serena

Scenario 3: Serena Returns Error
→ Cause: Invalid query or corrupted data
→ Detection: returncode != 0
→ Recovery:
  - Parse error message from stderr
  - Attempt alternative query format
  - Use fallback empty context
  - Log specific error

Scenario 4: Memory Key Not Found
→ Cause: First session or checkpoint missing
→ Detection: read_memory returns None
→ Recovery:
  - This is expected for first session
  - Initialize new project state
  - Create initial checkpoint
  - Continue normally

Graceful Degradation:
- NEVER crash the hook due to Serena issues
- ALWAYS return valid JSON
- PREFER partial context over no context
- LOG all errors for debugging
- USER may experience degraded AI awareness but system continues
```

---

## 6. Hook Installation and Deployment

### Installation Location

**Directory Structure**:

```
$CLAUDE_PROJECT_DIR/
├── .claude/
│   └── shannon/
│       ├── hooks/                          ← Hook scripts deployed here
│       │   ├── shannon_session_start.py
│       │   ├── shannon_context_injector.py
│       │   ├── shannon_precompact_hook.py  ← CRITICAL
│       │   └── shannon_performance_tracker.py
│       └── config/
│           └── hook_settings.json

~/.claude/
├── settings.json                           ← Register hooks here
└── shannon/
    └── hooks/                               ← Global hook templates (optional)
```

### Hook Registration

**Updating .claude/settings.json**:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_session_start.py",
            "timeout": 3000
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "^/shannon:.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_context_injector.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_precompact_hook.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Task|TodoWrite|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_performance_tracker.py",
            "timeout": 2000
          }
        ]
      }
    ]
  }
}
```

### Installation Script

**Automated Installation**:

```bash
#!/bin/bash
# install_shannon_hooks.sh

set -e

PROJECT_DIR="${1:-.}"
SHANNON_DIR="$PROJECT_DIR/.claude/shannon"
HOOKS_DIR="$SHANNON_DIR/hooks"

echo "Installing Shannon hooks to $PROJECT_DIR..."

# Create directory structure
mkdir -p "$HOOKS_DIR"

# Copy hook scripts from Shannon repo
cp hooks/shannon_session_start.py "$HOOKS_DIR/"
cp hooks/shannon_context_injector.py "$HOOKS_DIR/"
cp hooks/shannon_precompact_hook.py "$HOOKS_DIR/"
cp hooks/shannon_performance_tracker.py "$HOOKS_DIR/"

# Make hooks executable
chmod +x "$HOOKS_DIR"/*.py

# Verify Serena MCP is installed
echo "Verifying Serena MCP installation..."
if claude mcp list | grep -q "serena"; then
    echo "✓ Serena MCP found"
else
    echo "✗ Serena MCP not found"
    echo "Installing Serena MCP..."
    claude mcp add serena --transport stdio -- npx serena-mcp-server
fi

# Register hooks in settings.json
python3 << 'EOF'
import json
import os
from pathlib import Path

settings_file = Path.home() / ".claude" / "settings.json"

# Load existing settings
if settings_file.exists():
    with open(settings_file) as f:
        settings = json.load(f)
else:
    settings = {}

# Add hooks
if "hooks" not in settings:
    settings["hooks"] = {}

# Register Shannon hooks
shannon_hooks = {
    "SessionStart": [{
        "hooks": [{
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_session_start.py",
            "timeout": 3000
        }]
    }],
    "UserPromptSubmit": [{
        "matcher": "^/shannon:.*",
        "hooks": [{
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_context_injector.py",
            "timeout": 5000
        }]
    }],
    "PreCompact": [{
        "hooks": [{
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_precompact_hook.py",
            "timeout": 5000
        }]
    }],
    "PostToolUse": [{
        "matcher": "Task|TodoWrite|Write|Edit",
        "hooks": [{
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/shannon/hooks/shannon_performance_tracker.py",
            "timeout": 2000
        }]
    }]
}

# Merge (don't overwrite existing hooks)
for event, hooks in shannon_hooks.items():
    if event not in settings["hooks"]:
        settings["hooks"][event] = []
    settings["hooks"][event].extend(hooks)

# Save settings
with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print("✓ Hooks registered in settings.json")
EOF

echo "✓ Shannon hooks installed successfully"
echo ""
echo "Test with: claude /shannon:status"
```

### Verification After Installation

**Manual Verification**:

```bash
# 1. Check hook files exist
ls -la .claude/shannon/hooks/

# Expected output:
# shannon_session_start.py
# shannon_context_injector.py
# shannon_precompact_hook.py
# shannon_performance_tracker.py

# 2. Check hooks are executable
stat -f "%A %N" .claude/shannon/hooks/*.py

# Expected: -rwxr-xr-x for all

# 3. Verify settings.json has hooks
cat ~/.claude/settings.json | jq '.hooks'

# Expected: JSON with SessionStart, UserPromptSubmit, PreCompact, PostToolUse

# 4. Test hook execution
.claude/shannon/hooks/shannon_session_start.py <<< '{}'

# Expected: Valid JSON output with hookSpecificOutput

# 5. Test Serena integration
claude mcp call serena write_memory <<< '{"memory_name":"test","content":"test"}'

# Expected: Success response
```

---

## 7. Testing and Validation

### Unit Testing Hooks

**Test Individual Hook Behavior**:

```python
#!/usr/bin/env python3
# test_shannon_hooks.py

import json
import subprocess
import unittest

class TestShannonHooks(unittest.TestCase):

    def test_session_start_hook_basic(self):
        """Test SessionStart hook returns valid JSON"""
        input_data = json.dumps({})

        result = subprocess.run(
            ['.claude/shannon/hooks/shannon_session_start.py'],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=3
        )

        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertIn('hookSpecificOutput', output)
        self.assertEqual(output['hookSpecificOutput']['hookEventName'], 'SessionStart')

    def test_precompact_hook_preserves_state(self):
        """Test PreCompact hook saves to Serena"""
        # Create test conversation state
        input_data = json.dumps({
            "transcript": "User completed Wave 1 architecture design"
        })

        result = subprocess.run(
            ['.claude/shannon/hooks/shannon_precompact_hook.py'],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )

        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertTrue(output['hookSpecificOutput']['preservationStatus'] == 'success')

        # Verify saved to Serena
        checkpoint_key = output['hookSpecificOutput']['checkpointKey']
        serena_result = subprocess.run(
            ['claude', 'mcp', 'call', 'serena', 'read_memory'],
            input=json.dumps({"memory_file_name": checkpoint_key}),
            capture_output=True,
            text=True
        )

        self.assertEqual(serena_result.returncode, 0)
        checkpoint = json.loads(serena_result.stdout)
        self.assertIn('session_id', checkpoint)

    def test_hook_timeout_handling(self):
        """Test hook completes within timeout"""
        import time
        start = time.time()

        result = subprocess.run(
            ['.claude/shannon/hooks/shannon_context_injector.py'],
            input=json.dumps({"prompt": "/shannon:status"}),
            capture_output=True,
            text=True,
            timeout=5
        )

        elapsed = time.time() - start
        self.assertLess(elapsed, 5.0)
        self.assertEqual(result.returncode, 0)

    def test_hook_error_graceful_degradation(self):
        """Test hook handles Serena unavailability gracefully"""
        # Temporarily make Serena unavailable (rename serena MCP)

        result = subprocess.run(
            ['.claude/shannon/hooks/shannon_session_start.py'],
            input=json.dumps({}),
            capture_output=True,
            text=True,
            timeout=3
        )

        # Should still succeed (degraded mode)
        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertTrue(output['hookSpecificOutput'].get('degradedMode', False))

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

**Test Hook-Claude-Serena Flow**:

```bash
#!/bin/bash
# test_hook_integration.sh

echo "=== Shannon Hook Integration Test ==="

# 1. Clean slate
echo "1. Cleaning test environment..."
rm -rf /tmp/shannon_test_project
mkdir -p /tmp/shannon_test_project/.claude/shannon/hooks

# 2. Install hooks
echo "2. Installing hooks..."
./install_shannon_hooks.sh /tmp/shannon_test_project

# 3. Initialize Serena memory
echo "3. Initializing Serena..."
cd /tmp/shannon_test_project
claude mcp call serena write_memory <<< '{"memory_name":"test_init","content":"initialized"}'

# 4. Test SessionStart hook
echo "4. Testing SessionStart hook..."
.claude/shannon/hooks/shannon_session_start.py <<< '{}' > /tmp/session_start_output.json
if jq -e '.hookSpecificOutput.hookEventName == "SessionStart"' /tmp/session_start_output.json; then
    echo "✓ SessionStart hook works"
else
    echo "✗ SessionStart hook failed"
    exit 1
fi

# 5. Test UserPromptSubmit hook
echo "5. Testing UserPromptSubmit hook..."
.claude/shannon/hooks/shannon_context_injector.py <<< '{"prompt":"/shannon:status"}' > /tmp/user_prompt_output.json
if jq -e '.hookSpecificOutput.hookEventName == "UserPromptSubmit"' /tmp/user_prompt_output.json; then
    echo "✓ UserPromptSubmit hook works"
else
    echo "✗ UserPromptSubmit hook failed"
    exit 1
fi

# 6. Test PreCompact hook critical path
echo "6. Testing PreCompact hook..."
.claude/shannon/hooks/shannon_precompact_hook.py <<< '{"transcript":"Wave 1 complete"}' > /tmp/precompact_output.json
if jq -e '.hookSpecificOutput.preservationStatus == "success"' /tmp/precompact_output.json; then
    echo "✓ PreCompact hook works"
    checkpoint_key=$(jq -r '.hookSpecificOutput.checkpointKey' /tmp/precompact_output.json)

    # Verify saved to Serena
    claude mcp call serena read_memory <<< "{\"memory_file_name\":\"$checkpoint_key\"}" > /tmp/checkpoint_verify.json
    if jq -e '.session_id' /tmp/checkpoint_verify.json; then
        echo "✓ Checkpoint saved to Serena"
    else
        echo "✗ Checkpoint not in Serena"
        exit 1
    fi
else
    echo "✗ PreCompact hook failed"
    exit 1
fi

# 7. Test PostToolUse hook
echo "7. Testing PostToolUse hook..."
.claude/shannon/hooks/shannon_performance_tracker.py <<< '{"tool_name":"Task"}' > /tmp/post_tool_output.json
if jq -e '.hookSpecificOutput.hookEventName == "PostToolUse"' /tmp/post_tool_output.json; then
    echo "✓ PostToolUse hook works"
else
    echo "✗ PostToolUse hook failed"
    exit 1
fi

echo ""
echo "=== All Integration Tests Passed ✓ ==="
```

### End-to-End Validation

**Real Session Test**:

```markdown
## E2E Test: Session Continuity Through Compaction

### Setup
1. Start new Claude Code session in test project
2. Ensure Shannon hooks installed
3. Verify Serena MCP available

### Test Scenario
1. Execute: /shannon:init
   Verify: Serena has shannon_config entity

2. Execute: /shannon:plan "Build simple todo app" --waves 3
   Verify: TodoWrite shows 3 wave planning tasks
   Verify: Serena has phase_plan_detailed memory

3. Execute: /shannon:analyze src/
   Verify: Analysis completes
   Verify: Serena has spec_analysis memory

4. Trigger artificial compaction:
   - Use enough tokens to cross 75% threshold
   - OR manually trigger if Claude Code allows

5. Verify PreCompact hook executed:
   Check: ~/.claude/logs/ for hook execution
   Check: Serena has session_checkpoint_* memory

6. Continue session after compaction:
   Execute: /shannon:status
   Expected: AI knows all previous context
   Expected: TodoWrite status preserved
   Expected: No duplicate work

7. Verify continuity:
   AI should reference:
   - Previous analysis results
   - Wave plan created earlier
   - All decisions made before compaction

### Success Criteria
✓ PreCompact hook executed before compaction
✓ Checkpoint saved to Serena successfully
✓ SessionStart loaded checkpoint after compaction
✓ AI maintained full project awareness
✓ No information loss detected
✓ User experienced seamless continuation
```

---

## 8. Hook Development Guidelines

### Best Practices

**Performance**:
```markdown
1. Fast Path First:
   - Try cached data before querying Serena
   - Use timeouts aggressively (prefer fast partial data)
   - Parallelize independent operations

2. Lazy Loading:
   - Don't load all memories if only need subset
   - Use Serena search_nodes instead of read_graph for targeted queries
   - Cache frequently accessed data in hook memory

3. Timeout Awareness:
   - ALWAYS complete within configured timeout
   - Use subprocess timeout parameter
   - Return partial results if running long

4. Error Budget:
   - Allocate 80% of timeout to main logic
   - Reserve 20% for error handling and output generation
   - If 80% elapsed, abort and return partial
```

**Reliability**:
```markdown
1. Graceful Degradation:
   - NEVER crash or raise unhandled exceptions
   - ALWAYS return valid JSON
   - Prefer degraded mode over failure

2. Idempotency:
   - Hooks may be called multiple times
   - Use unique keys (timestamps) for new data
   - Update existing keys rather than duplicate

3. Error Logging:
   - Log all errors to file (not stdout)
   - Include timestamp, error type, context
   - Don't spam logs (rate limit)

4. State Validation:
   - Verify Serena writes succeeded
   - Check for corrupted data
   - Validate JSON structure before returning
```

**Maintainability**:
```markdown
1. Code Structure:
   - One class per hook
   - Separate concerns: parsing, querying, formatting
   - Unit testable functions

2. Configuration:
   - Externalize timeouts, retry counts
   - Use config files for tunable parameters
   - Don't hardcode Serena memory keys

3. Documentation:
   - Docstrings for all functions
   - Explain why, not just what
   - Examples for complex logic

4. Versioning:
   - Include version number in hook output
   - Handle backward compatibility
   - Migrate old checkpoint formats
```

### Anti-Patterns to Avoid

**DON'T**:
```markdown
❌ Block indefinitely waiting for Serena
   Instead: Use timeouts, return partial results

❌ Assume Serena is always available
   Instead: Handle connection failures gracefully

❌ Load entire knowledge graph
   Instead: Query specific nodes needed

❌ Return HTML or arbitrary text
   Instead: Always return structured JSON

❌ Ignore timeout limits
   Instead: Respect timeout, return early if needed

❌ Throw exceptions on errors
   Instead: Catch all exceptions, log, return error JSON

❌ Mutate conversation transcript
   Instead: Only read transcript, write to Serena

❌ Depend on specific Claude Code version
   Instead: Use documented hook API only

❌ Assume hook order or sequence
   Instead: Make hooks independent and stateless

❌ Store secrets in hook code
   Instead: Use environment variables
```

### Hook Template

**Standard Hook Structure**:

```python
#!/usr/bin/env python3
"""
Shannon {Hook Name} Hook
Purpose: {What this hook does}
"""

import json
import sys
import subprocess
import os
from typing import Dict, Any, Optional

class Shannon{HookName}Hook:
    """
    {Hook description}
    """

    VERSION = "1.0.0"
    TIMEOUT_MS = {timeout_value}

    def __init__(self):
        self.project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        self.shannon_dir = f"{self.project_dir}/.claude/shannon"
        self.cache = {}

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution logic
        """
        try:
            # 1. Parse input
            # 2. Query Serena (with timeout)
            # 3. Process data
            # 4. Format output
            # 5. Return JSON
            pass

        except Exception as e:
            return self._error_response(str(e))

    def _query_serena(self, operation: str, payload: Dict) -> Optional[Any]:
        """
        Query Serena with timeout and error handling
        """
        try:
            result = subprocess.run(
                ['claude', 'mcp', 'call', 'serena', operation],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=2  # 2 second Serena timeout
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                self._log_error(f"Serena error: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            self._log_error("Serena timeout")
            return None

        except Exception as e:
            self._log_error(f"Serena exception: {str(e)}")
            return None

    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """
        Generate error response JSON
        """
        return {
            "hookSpecificOutput": {
                "hookEventName": "{HookEventName}",
                "error": True,
                "errorMessage": error_msg,
                "version": self.VERSION,
                "degradedMode": True
            }
        }

    def _log_error(self, message: str):
        """
        Log error to file (not stdout)
        """
        log_file = f"{self.shannon_dir}/logs/hook_errors.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        with open(log_file, 'a') as f:
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            f.write(f"{timestamp} [{self.__class__.__name__}] {message}\n")

def main():
    """
    Entry point
    """
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        # Execute hook
        hook = Shannon{HookName}Hook()
        output = hook.execute(input_data)

        # Return JSON to stdout
        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        # Last resort error handling
        error_output = {
            "hookSpecificOutput": {
                "hookEventName": "{HookEventName}",
                "error": True,
                "errorMessage": str(e)
            }
        }
        print(json.dumps(error_output))
        sys.exit(0)  # Don't block Claude Code

if __name__ == "__main__":
    main()
```

---

## Conclusion

Shannon's hook system is the critical bridge between Claude Code's event lifecycle and Shannon's intelligent coordination framework. By implementing hooks correctly—especially the PreCompact hook—Shannon achieves:

✅ **Zero Information Loss**: Context preserved across session compaction
✅ **Seamless Continuity**: Sessions resume with full project awareness
✅ **Intelligent Context Injection**: AI receives relevant context automatically
✅ **Performance Tracking**: Real-time coordination and drift detection
✅ **Graceful Degradation**: System continues even if components fail

**Critical Success Factors**:
1. PreCompact hook MUST execute before compaction
2. Hooks MUST complete within timeout limits
3. Hooks MUST handle Serena unavailability gracefully
4. Hooks MUST return valid JSON always
5. SessionStart hook MUST load latest checkpoint

**Testing is Mandatory**:
- Unit test each hook independently
- Integration test hook-Serena communication
- E2E test session continuity through compaction
- Verify graceful degradation under failure
- Validate performance under load

By following these behavioral guidelines, Shannon's hooks ensure that Claude Code sessions maintain perfect context continuity, enabling complex multi-session projects to succeed without information loss or duplicate work.