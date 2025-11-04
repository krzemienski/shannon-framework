---
name: context-preservation
description: |
  Automatic checkpoint creation via Serena MCP before context loss. Triggers on PreCompact hook,
  manual /sh_checkpoint, or after major skill completion. Saves structured checkpoints with complete
  session state for zero-loss restoration. Use when: context nearing limit (automatic), before
  long tasks, want explicit save points.

skill-type: PROTOCOL
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      purpose: Checkpoint storage and git-backed persistence
      fallback: none
      degradation: high

allowed-tools: Serena, TodoWrite
---

# Context Preservation Skill

## Overview

The **context-preservation** skill provides automatic checkpoint creation via Serena MCP to prevent context loss across Claude Code auto-compact events. This is Shannon V4's **zero-context-loss guarantee**.

**Core Capability**: Systematically save complete session state before context is lost.

**Unique Innovation**: Only framework with PreCompact hook integration for automatic checkpoints.

---

## When This Skill Activates

### Automatic Triggers

1. **PreCompact Hook** (PRIMARY)
   - Claude Code about to auto-compact conversation
   - Hook fires BEFORE compact happens
   - Saves complete state automatically
   - **Result**: Zero context loss across compact events

2. **Major Skill Completion**
   - After spec-analysis completes
   - After phase-planning generates plan
   - After wave execution completes
   - **Result**: Natural restore points at skill boundaries

3. **Long-Running Task Start**
   - Before wave-orchestration begins
   - Before multi-step implementation
   - Before complex testing sequences
   - **Result**: Safety net for extended operations

### Manual Triggers

4. **User Command: /sh_checkpoint**
   - User explicitly requests checkpoint
   - Creates named checkpoint for future reference
   - **Result**: User-controlled save points

5. **Time-Based (Optional)**
   - Every 30 minutes during active session
   - Only if significant state changes occurred
   - **Result**: Incremental progress preservation

---

## Checkpoint Structure

### Complete Checkpoint JSON Schema

```json
{
  "checkpoint_id": "SHANNON-[TYPE]-[DATE]-[SEQ]",
  "timestamp": "2025-11-03T18:00:00Z",
  "checkpoint_type": "precompact|manual|skill_complete|wave_complete|phase_transition",
  "shannon_version": "4.0.0",
  "
  "context": {
    "active_command": "sh_spec|sh_implement|sh_test",
    "active_skill": "spec-analysis|wave-orchestration|...",
    "skill_execution_state": {
      "current_step": "8D complexity analysis",
      "completed_steps": ["domain_detection", "file_discovery"],
      "pending_steps": ["mcp_recommendations", "phase_planning"]
    },

    "shannon_state": {
      "active_phase": "Phase 1: Analysis|Phase 2: Planning|...",
      "current_wave": 1,
      "total_waves": 5,
      "completed_waves": [],
      "wave_progress": "25%"
    },

    "analysis_results": {
      "8d_scores": {
        "frontend_complexity": 7,
        "backend_complexity": 6,
        "database_complexity": 4,
        "infrastructure_complexity": 5,
        "testing_complexity": 6,
        "deployment_complexity": 3,
        "integration_complexity": 8,
        "ux_complexity": 7
      },
      "domain_breakdown": {
        "frontend": "35%",
        "backend": "30%",
        "database": "15%",
        "infrastructure": "10%",
        "testing": "10%"
      },
      "complexity_label": "high|moderate|low"
    },

    "planning_state": {
      "phase_plan": {
        "phase_1": {...},
        "phase_2": {...},
        "validation_gates": {...}
      },
      "wave_plan": {
        "wave_1": {...},
        "wave_2": {...},
        "dependencies": {...}
      }
    },

    "execution_state": {
      "files_created": ["/path/to/file1.ts", "/path/to/file2.tsx"],
      "files_modified": ["/path/to/existing.ts"],
      "pending_files": ["/path/to/planned.ts"],
      "current_focus": "Implementing authentication system"
    },

    "mcp_state": {
      "discovered_mcps": ["puppeteer", "context7", "sequential"],
      "active_mcps": ["serena", "puppeteer"],
      "mcp_recommendations": {...}
    },

    "decisions": [
      {
        "decision": "Use JWT with refresh tokens",
        "rationale": "Security best practice for stateless auth",
        "timestamp": "2025-11-03T17:45:00Z",
        "impact": "high"
      }
    ],

    "serena_memory_keys": [
      "spec_analysis_001",
      "phase_plan_001",
      "wave_1_complete_001",
      "project_decisions_001",
      "todo_list_001"
    ],

    "todo_state": {
      "active_todos": [
        {
          "content": "Complete JWT token generation",
          "status": "in_progress",
          "activeForm": "Completing JWT token generation"
        },
        {
          "content": "Add refresh token logic",
          "status": "pending",
          "activeForm": "Adding refresh token logic"
        }
      ]
    }
  },

  "metadata": {
    "session_id": "unique_session_identifier",
    "user_project_path": "/Users/nick/Projects/myapp",
    "git_commit": "abc123def456",
    "git_branch": "main",
    "serena_uri": "serena://shannon/checkpoints/2025-11-03/001",
    "restoration_priority": "high|medium|low",
    "estimated_restore_time": "30 seconds"
  }
}
```

---

## Execution Workflow

### Step 1: Detect Checkpoint Trigger

```python
# PreCompact hook detected
if hook_event == "PreCompact":
    checkpoint_type = "precompact"
    checkpoint_trigger = "auto"
    priority = "high"

# Manual checkpoint
elif user_command == "/sh_checkpoint":
    checkpoint_type = "manual"
    checkpoint_trigger = "user"
    priority = "medium"

# Skill completion
elif skill_just_completed:
    checkpoint_type = "skill_complete"
    checkpoint_trigger = "auto"
    priority = "high" if skill in ["spec-analysis", "wave-orchestration"] else "medium"
```

### Step 2: Gather Complete State

```python
# 1. List all Serena memory keys
serena_keys = serena.list_memories()

# 2. Gather active command state
active_command = get_current_command()  # "sh_spec", "sh_implement", etc.
active_skill = get_current_skill()  # "spec-analysis", "wave-orchestration", etc.

# 3. Gather Shannon state
shannon_state = {
    "active_phase": current_phase,
    "current_wave": current_wave,
    "total_waves": total_waves,
    "completed_waves": list_completed_waves()
}

# 4. Gather analysis results (if available)
analysis_results = {
    "8d_scores": read_serena("8d_complexity_scores"),
    "domain_breakdown": read_serena("domain_breakdown"),
    "complexity_label": read_serena("complexity_label")
}

# 5. Gather planning state (if available)
planning_state = {
    "phase_plan": read_serena("phase_plan"),
    "wave_plan": read_serena("wave_plan")
}

# 6. Gather execution state
execution_state = {
    "files_created": list_created_files(),
    "files_modified": list_modified_files(),
    "current_focus": get_current_focus()
}

# 7. Gather MCP state
mcp_state = {
    "discovered_mcps": read_serena("discovered_mcps"),
    "active_mcps": get_active_mcps()
}

# 8. Gather decisions
decisions = read_serena("project_decisions") or []

# 9. Gather todos
todo_state = TodoRead() if TodoWrite_available else None
```

### Step 3: Construct Checkpoint Object

```python
checkpoint = {
    "checkpoint_id": f"SHANNON-{checkpoint_type.upper()}-{date}-{seq}",
    "timestamp": current_timestamp(),
    "checkpoint_type": checkpoint_type,
    "shannon_version": "4.0.0",
    "context": {
        "active_command": active_command,
        "active_skill": active_skill,
        "skill_execution_state": skill_state,
        "shannon_state": shannon_state,
        "analysis_results": analysis_results,
        "planning_state": planning_state,
        "execution_state": execution_state,
        "mcp_state": mcp_state,
        "decisions": decisions,
        "serena_memory_keys": serena_keys,
        "todo_state": todo_state
    },
    "metadata": {
        "session_id": session_id,
        "user_project_path": project_path,
        "git_commit": get_git_commit(),
        "git_branch": get_git_branch(),
        "serena_uri": f"serena://shannon/checkpoints/{date}/{seq}",
        "restoration_priority": priority,
        "estimated_restore_time": "30 seconds"
    }
}
```

### Step 4: Save to Serena MCP

```python
# Save checkpoint
checkpoint_key = f"checkpoint-{checkpoint['checkpoint_id']}"
serena.write_memory(
    memory_name=checkpoint_key,
    content=json.dumps(checkpoint, indent=2)
)

# Update latest checkpoint pointer
serena.write_memory(
    memory_name="latest_checkpoint",
    content=checkpoint_key
)

# Git commit (if Serena git-backed)
serena.execute_shell_command(
    command=f"cd {serena_dir} && git add . && git commit -m 'checkpoint: {checkpoint['checkpoint_id']}'"
)
```

### Step 5: Confirm to User

```python
print(f"""
✅ Checkpoint Saved Successfully

📦 Checkpoint ID: {checkpoint['checkpoint_id']}
🕐 Timestamp: {checkpoint['timestamp']}
📁 Type: {checkpoint_type}
🔑 Serena Keys Preserved: {len(serena_keys)}
🎯 Priority: {priority}

🔄 Restore with: /sh_restore {checkpoint['checkpoint_id']}
🔄 Auto-restore: /sh_restore (uses latest)

{f"⚠️ Auto-compact will proceed - context secured" if checkpoint_type == "precompact" else ""}
""")
```

---

## PreCompact Hook Integration

### Hook File Location

**Path**: `~/.claude/hooks/precompact.py`

**Purpose**: Inject checkpoint instructions BEFORE auto-compact

**Trigger**: Claude Code runs this Python script when auto-compact imminent

### Complete Hook Script

```python
#!/usr/bin/env python3
"""
Shannon V4 PreCompact Hook
Prevents context loss by injecting checkpoint instructions
"""
import json
import sys
from datetime import datetime

def main():
    # Read hook input from Claude Code
    input_data = json.load(sys.stdin)

    # Only act on automatic compaction
    if input_data.get("trigger") == "auto":
        timestamp = datetime.now().isoformat()

        # Inject checkpoint instructions
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "additionalContext": f'''
🔴 CRITICAL: AUTO-COMPACT IMMINENT - SAVE STATE NOW

Execute context-preservation skill IMMEDIATELY.

## MANDATORY PRE-COMPACT CHECKPOINT

You MUST execute these steps before compact proceeds:

1. Activate context-preservation skill
2. Gather complete session state
3. Save checkpoint to Serena MCP
4. Confirm checkpoint saved
5. Report success to user

Checkpoint timestamp: {timestamp}
Checkpoint type: precompact
Priority: HIGH

If you do NOT save this checkpoint:
❌ All wave results will be lost
❌ Project decisions will be forgotten
❌ Current progress will be erased
❌ User must restart from scratch

EXECUTE CHECKPOINT NOW.
'''
            }
        }

        json.dump(output, sys.stdout)
    else:
        # Manual compact - no special action needed
        json.dump({"hookSpecificOutput": {}}, sys.stdout)

if __name__ == "__main__":
    main()
```

### Hook Installation

User must install this hook manually:

```bash
# Create hooks directory
mkdir -p ~/.claude/hooks

# Copy hook script
cp shannon-plugin/hooks/precompact.py ~/.claude/hooks/

# Make executable
chmod +x ~/.claude/hooks/precompact.py

# Test hook
echo '{"trigger": "auto"}' | ~/.claude/hooks/precompact.py
```

**Shannon Plugin Note**: Hook script should be distributed in `shannon-plugin/hooks/precompact.py` for users to copy.

---

## Checkpoint Types and Priorities

### Checkpoint Type Definitions

| Type | Trigger | Priority | When Created | Restore Urgency |
|------|---------|----------|--------------|-----------------|
| `precompact` | Auto | HIGH | Before auto-compact | IMMEDIATE |
| `skill_complete` | Auto | HIGH | After major skill | HIGH |
| `wave_complete` | Auto | HIGH | After wave execution | HIGH |
| `phase_transition` | Auto | MEDIUM | Between phases | MEDIUM |
| `manual` | User | MEDIUM | User /sh_checkpoint | VARIES |
| `time_based` | Auto | LOW | Every 30 min | LOW |

### Restoration Priority Logic

**HIGH Priority Checkpoints** (restore automatically):
- `precompact` - Just recovered from auto-compact
- `skill_complete` - Major work completed, need to continue
- `wave_complete` - Wave finished, next wave depends on it

**MEDIUM Priority Checkpoints** (restore on request):
- `phase_transition` - User may want to review phase
- `manual` - User created for specific reason

**LOW Priority Checkpoints** (archive after 7 days):
- `time_based` - Incremental snapshots, superseded by later checkpoints

---

## Serena MCP Operations

### Required Serena Operations

```python
# 1. Write Memory (save checkpoint)
serena.write_memory(
    memory_name="checkpoint-SHANNON-PRECOMPACT-2025-11-03-001",
    content=checkpoint_json
)

# 2. List Memories (gather state)
all_keys = serena.list_memories()

# 3. Read Memory (restore checkpoint)
checkpoint_data = serena.read_memory("checkpoint-SHANNON-PRECOMPACT-2025-11-03-001")

# 4. Execute Shell (git commit)
serena.execute_shell_command(
    command="cd .serena && git add . && git commit -m 'checkpoint: ...'"
)
```

### Serena Memory Naming Convention

**Checkpoint Keys**:
```
checkpoint-SHANNON-PRECOMPACT-2025-11-03-001
checkpoint-SHANNON-MANUAL-2025-11-03-002
checkpoint-SHANNON-SKILL-2025-11-03-003
checkpoint-SHANNON-WAVE-2025-11-03-004
```

**Pointer Keys**:
```
latest_checkpoint  # Points to most recent checkpoint key
project_checkpoint_[project_name]  # Points to project-specific checkpoint
```

**State Keys** (preserved in checkpoint):
```
spec_analysis_001
phase_plan_001
wave_1_complete_001
wave_2_complete_001
project_decisions_001
todo_list_001
8d_complexity_scores
domain_breakdown
mcp_recommendations
```

---

## Error Handling

### Serena MCP Unavailable

```python
if not serena_available():
    print("""
⚠️ CRITICAL: Serena MCP not available
❌ Cannot save checkpoint
❌ Context loss risk HIGH

IMMEDIATE ACTION REQUIRED:
1. Install Serena MCP
2. Retry /sh_checkpoint
3. Consider manual backup (copy conversation)

Without Serena, Shannon cannot guarantee zero context loss.
""")
    return False
```

### Checkpoint Save Failed

```python
try:
    serena.write_memory(checkpoint_key, checkpoint_data)
except Exception as e:
    print(f"""
⚠️ Checkpoint save FAILED
Error: {e}

FALLBACK OPTIONS:
1. Retry checkpoint save
2. Manual Serena write
3. Copy checkpoint JSON to file
4. User manual backup

Checkpoint JSON:
{checkpoint_json}
""")
    return False
```

### Partial State Available

```python
if not all_state_available():
    print("""
⚠️ Partial checkpoint created
Some state unavailable but core preserved

SAVED:
✅ Active command/skill
✅ Shannon state (phase/wave)
✅ Serena memory keys

MISSING:
❌ Analysis results (not yet generated)
❌ Planning state (not yet created)

Checkpoint still useful for restoration.
""")
    # Save partial checkpoint anyway
    save_checkpoint(partial_checkpoint)
```

---

## Validation

### Pre-Save Validation

```python
def validate_checkpoint(checkpoint):
    """Validate checkpoint before saving"""

    checks = {
        "has_checkpoint_id": bool(checkpoint.get("checkpoint_id")),
        "has_timestamp": bool(checkpoint.get("timestamp")),
        "has_context": bool(checkpoint.get("context")),
        "has_serena_keys": bool(checkpoint.get("context", {}).get("serena_memory_keys")),
        "has_active_command": bool(checkpoint.get("context", {}).get("active_command")),
        "valid_priority": checkpoint.get("metadata", {}).get("restoration_priority") in ["high", "medium", "low"]
    }

    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        raise ValueError(f"Checkpoint validation failed: {failed}")

    return True
```

### Post-Save Verification

```python
def verify_checkpoint_saved(checkpoint_key):
    """Verify checkpoint actually saved to Serena"""

    # Try to read back
    saved_data = serena.read_memory(checkpoint_key)

    if not saved_data:
        raise RuntimeError(f"Checkpoint {checkpoint_key} not found in Serena")

    # Verify latest pointer updated
    latest = serena.read_memory("latest_checkpoint")
    if latest != checkpoint_key:
        print(f"⚠️ Latest pointer not updated (expected {checkpoint_key}, got {latest})")

    return True
```

---

## Integration with Other Skills

### After spec-analysis

```python
# spec-analysis completes
analysis_results = {
    "8d_scores": {...},
    "domain_breakdown": {...},
    "complexity_label": "high"
}

# Trigger checkpoint
create_checkpoint(
    checkpoint_type="skill_complete",
    active_skill="spec-analysis",
    analysis_results=analysis_results,
    priority="high"
)
```

### After phase-planning

```python
# phase-planning completes
phase_plan = {
    "phase_1": {...},
    "phase_2": {...},
    "validation_gates": {...}
}

# Trigger checkpoint
create_checkpoint(
    checkpoint_type="skill_complete",
    active_skill="phase-planning",
    planning_state={"phase_plan": phase_plan},
    priority="high"
)
```

### After wave-orchestration

```python
# Wave completes
wave_results = {
    "wave_number": 1,
    "files_created": [...],
    "tests_passing": True,
    "status": "complete"
}

# Trigger checkpoint
create_checkpoint(
    checkpoint_type="wave_complete",
    active_skill="wave-orchestration",
    wave_number=1,
    execution_state=wave_results,
    priority="high"
)
```

---

## References

See `references/CONTEXT_MANAGEMENT.md` for:
- Complete checkpoint strategy
- PreCompact hook details
- Memory naming conventions
- Cleanup strategies

---

## Examples

See `examples/`:
- `precompact-checkpoint.md` - Automatic checkpoint before compact
- `manual-checkpoint.md` - User-requested checkpoint
- `wave-checkpoint.md` - Checkpoint after wave completion
