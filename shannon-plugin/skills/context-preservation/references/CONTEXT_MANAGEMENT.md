# Context Management Reference

> Extracted from shannon-plugin/core/CONTEXT_MANAGEMENT.md
> Focus: Checkpoint preservation sections for context-preservation skill

---

## Checkpoint Strategy

### When to Checkpoint

Create checkpoints at these critical moments:

**1. Automatic PreCompact Checkpoint**
- **Trigger**: PreCompact hook fires before auto-compact
- **Frequency**: Every auto-compact event (~2-3 hours)
- **Content**: Complete session state
- **Critical**: This is THE key checkpoint preventing context loss

**2. Wave Completion Checkpoint**
- **Trigger**: After each wave completes successfully
- **Frequency**: Per wave (typically 3-8 waves per project)
- **Content**: Wave results, decisions, files created

**3. Manual Checkpoint**
- **Trigger**: User types `/sh_checkpoint`
- **Frequency**: On-demand (before risky operations, end of day)
- **Content**: Current work state, pending tasks

**4. Phase Transition Checkpoint**
- **Trigger**: Moving between 5 phases (Analysis → Planning → Implementation → Testing → Deployment)
- **Frequency**: 4-5 times per project
- **Content**: Phase completion status, next phase context

**5. Time-Based Checkpoint**
- **Trigger**: Every 30 minutes during long sessions
- **Frequency**: Automatic during active work
- **Content**: Incremental progress, current focus

---

### What to Save in Each Checkpoint

**Checkpoint Content Structure**:

```yaml
checkpoint_content:
  # Metadata
  timestamp: "2025-09-30T14:30:00Z"
  checkpoint_type: "precompact|manual|wave|phase|time"
  session_id: "unique_session_identifier"

  # Project State
  project_id: "project_identifier"
  active_phase: "analysis|planning|implementation|testing|deployment"
  current_wave: 3
  total_waves: 5

  # Serena Memory Keys (CRITICAL)
  serena_memory_keys: [
    "spec_analysis_001",
    "phase_plan_001",
    "wave_1_complete_001",
    "wave_2_complete_001",
    "wave_3_results_frontend",
    "project_decisions_001",
    "todo_list_001"
  ]

  # Active Work
  current_focus: "Implementing authentication system"
  in_progress_files: [
    "/path/to/auth.ts",
    "/path/to/login.tsx"
  ]
  pending_tasks: [
    "Complete JWT token generation",
    "Add refresh token logic",
    "Test login flow"
  ]

  # Recent Decisions
  key_decisions: [
    {
      decision: "Use JWT with refresh tokens",
      rationale: "Security best practice",
      timestamp: "2025-09-30T14:15:00Z"
    }
  ]

  # Wave Context
  completed_waves: [
    {
      wave_number: 1,
      name: "Frontend Components",
      status: "complete",
      agents: ["frontend-architect", "implementation-worker"],
      results_key: "wave_1_complete_001"
    },
    {
      wave_number: 2,
      name: "Backend API",
      status: "complete",
      agents: ["backend-architect", "implementation-worker"],
      results_key: "wave_2_complete_001"
    }
  ]
  pending_waves: [
    {
      wave_number: 3,
      name: "Database Integration",
      status: "in_progress",
      agents: ["implementation-worker", "testing-worker"]
    }
  ]

  # Sub-Agent Context
  active_agents: ["implementation-worker"]
  agent_handoff_data: {
    from_agent: "backend-architect",
    to_agent: "implementation-worker",
    context: "Complete auth implementation per plan"
  }

  # Quality State
  validation_status: {
    phase_2_gates: "passed",
    phase_3_gates: "in_progress"
  }
  tests_passing: true
  known_issues: []
```

---

### Checkpoint Execution Steps

**When creating ANY checkpoint:**

```python
# Step 1: List all current Serena memories
memory_keys = list_memories()

# Step 2: Gather checkpoint metadata
checkpoint_data = {
    "timestamp": current_timestamp(),
    "checkpoint_type": checkpoint_type,
    "session_id": current_session_id,
    "serena_memory_keys": memory_keys,
    "active_phase": current_phase,
    "current_wave": current_wave,
    # ... all checkpoint content
}

# Step 3: Save checkpoint to Serena
checkpoint_key = f"{checkpoint_type}_checkpoint_{timestamp}"
write_memory(checkpoint_key, checkpoint_data)

# Step 4: Confirm save
confirm_message = f"✅ Checkpoint saved: {checkpoint_key}"
confirm_message += f"\n📦 Preserved {len(memory_keys)} memory keys"
confirm_message += f"\n🔄 Restore with: read_memory('{checkpoint_key}')"

# Step 5: Log checkpoint for discoverability
write_memory("latest_checkpoint", checkpoint_key)
```

---

## PreCompact Hook Integration

### How PreCompact Hook Works

**PreCompact Hook Location**: `~/.claude/hooks/precompact.py`

**Hook Trigger**: Claude Code runs this Python script BEFORE auto-compact

**Hook Purpose**: Inject instructions telling Claude to save checkpoint

**Complete Hook Script**:

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
        # Generate checkpoint timestamp
        timestamp = datetime.now().isoformat()

        # Inject checkpoint instructions
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "additionalContext": f'''
🔴 CRITICAL: AUTO-COMPACT IMMINENT - SAVE STATE NOW

You are about to experience auto-compact which will compress conversation history.
To prevent context loss, you MUST save complete state to Serena MCP.

## MANDATORY PRE-COMPACT CHECKPOINT

Execute these steps IN ORDER:

### Step 1: List All Serena Memories
```
current_keys = list_memories()
```

### Step 2: Create Checkpoint Object
```yaml
checkpoint_data:
  timestamp: "{timestamp}"
  checkpoint_type: "precompact"
  trigger: "auto"

  # CRITICAL: List ALL Serena keys for restoration
  serena_memory_keys: [current_keys from step 1]

  # Current session state
  session_id: [current session identifier]
  active_phase: [current phase: analysis|planning|implementation|testing|deployment]
  current_wave: [current wave number]
  total_waves: [total planned waves]

  # Active work
  current_focus: [what you're working on right now]
  in_progress_files: [files being edited]
  pending_tasks: [incomplete todos]

  # Wave status
  completed_waves: [list of completed waves with result keys]
  pending_waves: [list of pending waves]

  # Decisions and context
  key_decisions: [recent architectural decisions]
  project_context: [essential project information]
```

### Step 3: Save Checkpoint to Serena
```
checkpoint_key = "precompact_checkpoint_{timestamp}"
write_memory(checkpoint_key, checkpoint_data)
```

### Step 4: Update Latest Checkpoint Pointer
```
write_memory("latest_checkpoint", checkpoint_key)
```

### Step 5: Confirm Save
```
Respond to user:
"✅ Pre-compact checkpoint saved: {{checkpoint_key}}"
"📦 Preserved {{count}} Serena memory keys"
"🔄 Auto-compact will proceed - context secured"
```

## AFTER AUTO-COMPACT RESTORATION

When you resume after auto-compact:
1. read_memory("latest_checkpoint") to get most recent checkpoint key
2. read_memory(checkpoint_key) to restore full context
3. Read all Serena keys listed in checkpoint
4. Resume from saved wave/phase/task

## FAILURE TO CHECKPOINT = CONTEXT LOSS

If you do NOT save this checkpoint:
- ❌ All wave results will be lost
- ❌ Project decisions will be forgotten
- ❌ Current progress will be erased
- ❌ User must restart from scratch

This checkpoint is CRITICAL. Execute it now before compact.
'''
            }
        }

        # Return instructions to Claude Code
        json.dump(output, sys.stdout)

    else:
        # Manual compact - no special action needed
        json.dump({"hookSpecificOutput": {}}, sys.stdout)

if __name__ == "__main__":
    main()
```

---

### PreCompact Hook Workflow

**Complete Auto-Compact Lifecycle**:

```
┌─────────────────────────────────────────────────┐
│ STEP 1: Normal Claude Code Operation           │
│                                                 │
│ User working on project...                     │
│ - Wave 3 in progress                           │
│ - Multiple Serena memories created             │
│ - Context building up                          │
│ - Conversation growing long (~2-3 hours)       │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Claude Code detects conversation length
                   │ Decides to auto-compact
                   ▼
┌─────────────────────────────────────────────────┐
│ STEP 2: PreCompact Hook Triggers               │
│                                                 │
│ Claude Code:                                    │
│ 1. Pauses before compacting                    │
│ 2. Runs ~/.claude/hooks/precompact.py          │
│ 3. Hook detects trigger="auto"                 │
│ 4. Hook generates checkpoint instructions      │
│ 5. Hook returns additionalContext to Claude    │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Instructions injected into Claude's context
                   ▼
┌─────────────────────────────────────────────────┐
│ STEP 3: Claude Executes Checkpoint             │
│                                                 │
│ Claude reads injected instructions and:        │
│ 1. list_memories() → gets all Serena keys      │
│ 2. Creates checkpoint object with all state    │
│ 3. write_memory("precompact_checkpoint_X", {}) │
│ 4. write_memory("latest_checkpoint", key)      │
│ 5. Confirms: "✅ Checkpoint saved"             │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Checkpoint complete, safe to compact
                   ▼
┌─────────────────────────────────────────────────┐
│ STEP 4: Auto-Compact Proceeds                  │
│                                                 │
│ Claude Code:                                    │
│ - Compresses conversation history              │
│ - Removes old messages                         │
│ - Frees up context window                      │
│ - Creates new conversation thread              │
│                                                 │
│ ⚠️ WITHOUT checkpoint: ALL context lost        │
│ ✅ WITH checkpoint: State preserved in Serena  │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Compact complete, user continues
                   ▼
┌─────────────────────────────────────────────────┐
│ STEP 5: Post-Compact Restoration               │
│                                                 │
│ Option A: Automatic Restoration                │
│ - Claude checks for recent checkpoint          │
│ - read_memory("latest_checkpoint")             │
│ - Restores context automatically               │
│                                                 │
│ Option B: Manual Restoration                   │
│ - User types: /sh_restore                      │
│ - restore.md command activates                 │
│ - Full context restoration                     │
│                                                 │
│ Option C: Continue Working                     │
│ - User continues working                       │
│ - Claude accesses preserved Serena keys        │
│ - No interruption to workflow                  │
└─────────────────────────────────────────────────┘
```

**Result**: Zero context loss across auto-compact event

---

## Memory Naming Conventions

### Hierarchical Key Structure

Use consistent naming patterns for easy discovery and organization:

```yaml
# Level 1: Project Memories (long-lived)
project_[id]_spec_analysis
project_[id]_phase_plan
project_[id]_decisions

# Level 2: Wave Memories (per-wave lifecycle)
project_[id]_wave_[n]_plan
project_[id]_wave_[n]_complete
project_[id]_wave_[n]_results_[component]

# Level 3: Session Memories (temporary)
session_[id]_checkpoint
session_[id]_active_work
session_[id]_todo_list

# Level 4: Checkpoint Memories (recovery points)
precompact_checkpoint_[timestamp]
manual_checkpoint_[timestamp]
phase_checkpoint_[phase_name]_[timestamp]

# Level 5: Global Pointers (navigation)
latest_checkpoint
current_project
active_session
```

---

### Naming Pattern Examples

**Good Naming Patterns**:
```
✅ project_taskapp_spec_analysis_20250930
✅ wave_3_backend_results_20250930
✅ precompact_checkpoint_20250930T143000Z
✅ decision_auth_jwt_20250930
✅ phase_implementation_complete_20250930
```

**Bad Naming Patterns**:
```
❌ temp
❌ stuff
❌ data123
❌ backup
❌ old_version
```

---

### Naming Convention Benefits

**1. Easy Discovery**
```python
# Find all wave results
wave_results = [k for k in list_memories() if "wave_" in k and "_results" in k]

# Find all checkpoints
checkpoints = [k for k in list_memories() if "checkpoint" in k]

# Find project-specific memories
project_memories = [k for k in list_memories() if k.startswith(f"project_{project_id}")]
```

**2. Temporal Ordering**
```python
# ISO 8601 timestamps sort chronologically
checkpoints_sorted = sorted([k for k in list_memories() if "checkpoint" in k])
latest = checkpoints_sorted[-1]
oldest = checkpoints_sorted[0]
```

**3. Automatic Cleanup**
```python
# Delete all session memories older than 7 days
old_sessions = [k for k in list_memories()
                if k.startswith("session_")
                and parse_timestamp(k) < seven_days_ago]
for key in old_sessions:
    delete_memory(key)
```

---

## Cleanup Strategy

### When to Clean Up

**1. Project Completion**
- Delete all session memories
- Keep project memories (spec, decisions)
- Delete old checkpoints (keep final checkpoint)

**2. Wave Completion**
- Delete temporary wave planning memories
- Keep wave results for future reference
- Archive old wave details

**3. Phase Transition**
- Delete phase-specific temporary memories
- Keep phase completion records
- Archive validation results

**4. Session End**
- Delete session-specific memories
- Keep project context memories
- Archive session logs

**5. Storage Management**
- Delete memories older than 30 days (configurable)
- Keep essential project memories indefinitely
- Archive infrequently accessed memories

---

### Cleanup Execution

**Cleanup Command**: `/sh_cleanup_context` or automatic

```python
def cleanup_context(cleanup_type, project_id=None):
    """
    Execute context cleanup based on type
    """

    all_keys = list_memories()

    if cleanup_type == "session":
        # Delete temporary session memories
        session_keys = [k for k in all_keys if "session_" in k]
        for key in session_keys:
            delete_memory(key)
        print(f"🧹 Cleaned up {len(session_keys)} session memories")

    elif cleanup_type == "wave":
        # Keep wave results, delete wave planning
        wave_planning_keys = [k for k in all_keys
                              if "wave_" in k and "_plan" in k
                              and "_complete" not in k]
        for key in wave_planning_keys:
            delete_memory(key)
        print(f"🧹 Cleaned up {len(wave_planning_keys)} wave planning memories")

    elif cleanup_type == "project":
        # Archive project memories, delete temporary
        if project_id:
            temp_keys = [k for k in all_keys
                        if project_id in k
                        and any(temp in k for temp in ["temp", "tmp", "scratch"])]
            for key in temp_keys:
                delete_memory(key)
            print(f"🧹 Cleaned up {len(temp_keys)} temporary project memories")

    elif cleanup_type == "old_checkpoints":
        # Keep last 5 checkpoints, delete older
        checkpoint_keys = sorted([k for k in all_keys if "checkpoint" in k],
                                reverse=True)
        old_checkpoints = checkpoint_keys[5:]  # Keep 5 most recent
        for key in old_checkpoints:
            delete_memory(key)
        print(f"🧹 Cleaned up {len(old_checkpoints)} old checkpoints")
```

---

### Cleanup Policies

**Memory Retention Policy**:

```yaml
# Indefinite retention (never delete)
indefinite:
  - spec_analysis_*
  - final_phase_plan_*
  - project_decisions_*
  - final_results_*

# 30-day retention
thirty_days:
  - wave_*_complete
  - phase_*_checkpoint
  - precompact_checkpoint_*

# 7-day retention
seven_days:
  - wave_*_plan
  - session_*
  - temp_*

# 1-day retention
one_day:
  - scratch_*
  - tmp_*
  - debug_*
```

---

## Context Management Best Practices

### 1. Always Save Before Risky Operations

```python
# Before major changes
write_memory(f"pre_refactor_checkpoint_{timestamp}", current_state)

# Perform risky operation
execute_major_refactor()

# If successful, can delete checkpoint
# If failure, restore from checkpoint
```

---

### 2. Use Checkpoint Points as Restore Points

```python
# Create restore point
checkpoint_key = create_checkpoint("before_experiment")

# Try experimental approach
try:
    experiment_with_new_architecture()
except:
    # Restore from checkpoint
    restore_from_checkpoint(checkpoint_key)
```

---

### 3. Document Key Decisions in Memories

```python
write_memory(f"decision_auth_approach_{timestamp}", {
    "decision": "Use JWT tokens with refresh tokens",
    "rationale": [
        "Industry standard",
        "Stateless authentication",
        "Scalable architecture"
    ],
    "alternatives_considered": [
        "Session-based auth (rejected: not scalable)",
        "OAuth2 only (rejected: over-engineering)"
    ],
    "date": timestamp,
    "phase": current_phase
})
```

---

### 4. Cross-Reference Related Memories

```python
# When creating wave results, reference previous wave
write_memory(f"wave_3_results_{timestamp}", {
    "wave_number": 3,
    "dependencies": ["wave_1_complete_001", "wave_2_complete_001"],
    "builds_on": "Frontend from Wave 1, API from Wave 2",
    "results": {...}
})
```

---

### 5. Use Memory Discovery for Context Rebuilding

```python
# Find all related memories for a component
auth_memories = [k for k in list_memories() if "auth" in k]

# Read all auth-related context
auth_context = {k: read_memory(k) for k in auth_memories}

# Rebuild complete understanding
understand_auth_system(auth_context)
```
