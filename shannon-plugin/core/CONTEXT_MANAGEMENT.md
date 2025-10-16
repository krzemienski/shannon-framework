# CONTEXT_MANAGEMENT.md - Context Preservation System

## Purpose
Instructions for preserving project context across sessions using Serena MCP integration.

When Claude Code auto-compacts conversations (typically every 2-3 hours), all conversation history is compressed and context can be lost. Shannon's context management system prevents this through:
1. **PreCompact Hook**: Triggers BEFORE auto-compact to save state
2. **Checkpoint Strategy**: Systematic state preservation
3. **Restore Strategy**: Complete context recovery
4. **Serena MCP Integration**: Persistent memory storage across sessions

**Goal**: Zero context loss across auto-compact events and session breaks

---

## Serena MCP Tools

You have access to these memory operations through Serena MCP:

### Core Memory Operations
- `list_memories()` - List all saved memory keys
- `read_memory(key)` - Read specific memory content
- `write_memory(key, content)` - Save memory with key
- `delete_memory(key)` - Remove memory by key

### Memory Key Patterns
Use structured naming for organization and discovery:

```yaml
# Checkpoint memories
precompact_checkpoint_[timestamp]  # Auto-saved before compact
manual_checkpoint_[timestamp]      # User-requested checkpoint
session_checkpoint_[session_id]    # Session-specific checkpoint

# Analysis memories
spec_analysis_[project_id]         # Specification analysis results
complexity_score_[project_id]      # 8-dimensional complexity data
domain_breakdown_[project_id]      # Domain percentage calculations
mcp_suggestions_[project_id]       # Recommended MCP servers

# Planning memories
phase_plan_[project_id]            # 5-phase execution plan
wave_plan_[project_id]_[wave_n]    # Individual wave plans
validation_gates_[project_id]      # Quality gate definitions

# Execution memories
wave_[n]_complete_[timestamp]      # Wave completion status
wave_[n]_[component]_results       # Component-specific results
active_wave_[project_id]           # Current wave number
active_phase_[project_id]          # Current phase number

# Project memories
project_decisions_[project_id]     # Architectural decisions
project_context_[project_id]       # General project information
todo_list_[project_id]             # Current todo items
```

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
- **Trigger**: User types `/sh:checkpoint`
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
Shannon V3 PreCompact Hook
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
│ - User types: /sh:restore                      │
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

## Restore Strategy

### When to Restore Context

Restore context in these situations:

**1. After Auto-Compact**
- **Detection**: New conversation thread, but project was active
- **Action**: Check for recent checkpoint and restore automatically
- **Command**: Automatic or `/sh:restore`

**2. Starting New Session**
- **Detection**: User returns after hours/days
- **Action**: Find most recent checkpoint for project
- **Command**: `/sh:restore` or automatic on project detection

**3. After Context Loss**
- **Detection**: Claude doesn't remember recent work
- **Action**: Restore from most recent checkpoint
- **Command**: `/sh:restore`

**4. Switching Between Projects**
- **Detection**: User switches from Project A to Project B
- **Action**: Save Project A context, load Project B context
- **Command**: `/sh:checkpoint` then `/sh:restore [project_b]`

**5. Error Recovery**
- **Detection**: Something went wrong, need to rollback
- **Action**: Restore from last known good checkpoint
- **Command**: `/sh:restore [checkpoint_key]`

---

### Restore Execution Steps

**Complete Restoration Process**:

```python
# STEP 1: Find Most Recent Checkpoint
# ========================================

# Option A: Use latest checkpoint pointer
latest_key = read_memory("latest_checkpoint")
checkpoint_key = latest_key

# Option B: List all checkpoints and find most recent
all_keys = list_memories()
checkpoint_keys = [k for k in all_keys if "checkpoint" in k]
checkpoint_keys_sorted = sorted(checkpoint_keys, reverse=True)
checkpoint_key = checkpoint_keys_sorted[0]  # Most recent

# Option C: User specifies checkpoint
# User says: "Restore from precompact_checkpoint_001"
checkpoint_key = "precompact_checkpoint_001"


# STEP 2: Load Checkpoint Data
# ========================================

checkpoint_data = read_memory(checkpoint_key)

"""
checkpoint_data structure:
{
  "timestamp": "2025-09-30T14:30:00Z",
  "serena_memory_keys": [...],  # CRITICAL LIST
  "active_phase": "implementation",
  "current_wave": 3,
  "pending_tasks": [...],
  ...
}
"""


# STEP 3: Restore All Serena Memory Keys
# ========================================

# Get list of ALL memory keys that were saved
memory_keys = checkpoint_data["serena_memory_keys"]

# Read EACH memory to restore full context
restored_memories = {}
for key in memory_keys:
    try:
        content = read_memory(key)
        restored_memories[key] = content
    except:
        # Log missing memory but continue
        log_warning(f"Could not restore: {key}")

"""
Example restoration:
- spec_analysis_001 → Full specification analysis
- phase_plan_001 → 5-phase execution plan
- wave_1_complete_001 → Wave 1 results
- wave_2_complete_001 → Wave 2 results
- project_decisions_001 → Architectural decisions
- todo_list_001 → Current tasks
"""


# STEP 4: Rebuild Context Understanding
# ========================================

# Project Context
project_id = checkpoint_data["project_id"]
project_phase = checkpoint_data["active_phase"]
current_wave = checkpoint_data["current_wave"]
total_waves = checkpoint_data["total_waves"]

# Work Context
current_focus = checkpoint_data["current_focus"]
pending_tasks = checkpoint_data["pending_tasks"]
in_progress_files = checkpoint_data["in_progress_files"]

# Historical Context
completed_waves = checkpoint_data["completed_waves"]
key_decisions = checkpoint_data["key_decisions"]


# STEP 5: Validate Restoration
# ========================================

validation_checks = {
    "checkpoint_loaded": checkpoint_data is not None,
    "memories_restored": len(restored_memories) > 0,
    "phase_known": project_phase in ["analysis", "planning", "implementation", "testing", "deployment"],
    "wave_valid": current_wave <= total_waves,
    "tasks_present": len(pending_tasks) > 0
}

all_valid = all(validation_checks.values())


# STEP 6: Resume Work
# ========================================

if all_valid:
    # Inform user of successful restoration
    report = f"""
✅ Context Restored Successfully

📦 Checkpoint: {checkpoint_key}
🕐 Saved: {checkpoint_data['timestamp']}
📚 Restored {len(restored_memories)} memories
🔄 Current: Phase {project_phase}, Wave {current_wave}/{total_waves}

🎯 Current Focus: {current_focus}

📋 Pending Tasks:
{format_tasks(pending_tasks)}

🏆 Completed Waves:
{format_waves(completed_waves)}

▶️ Ready to continue where you left off.
"""

    print(report)

    # Continue from saved state
    # - Load wave plan for current wave
    # - Access previous wave results
    # - Execute pending tasks
    # - Maintain full context

else:
    # Report restoration issues
    failed_checks = [k for k, v in validation_checks.items() if not v]
    print(f"⚠️ Restoration incomplete. Failed checks: {failed_checks}")
    print("Attempting partial restoration...")
```

---

### Restoration Best Practices

**1. Always Verify Restoration**
```python
# After restore, check critical context
assert read_memory("spec_analysis_001") is not None
assert read_memory("phase_plan_001") is not None
assert current_wave > 0 and current_wave <= total_waves
```

**2. Log Restoration Events**
```python
write_memory(f"restore_log_{timestamp}", {
    "checkpoint_used": checkpoint_key,
    "memories_restored": len(restored_memories),
    "restoration_time": timestamp,
    "success": all_valid
})
```

**3. Handle Missing Memories Gracefully**
```python
# If critical memory missing, flag but continue
if "spec_analysis" not in restored_memories:
    print("⚠️ Spec analysis missing - may need to re-analyze")
else:
    # Proceed normally
    spec = restored_memories["spec_analysis"]
```

**4. Progressive Restoration**
```python
# Restore in priority order:
# 1. Critical (spec, phase plan)
# 2. Important (wave results, decisions)
# 3. Nice-to-have (logs, temporary state)

priority_keys = ["spec_analysis", "phase_plan", "wave_*_complete"]
for key in priority_keys:
    restore_memory(key)
```

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

**Cleanup Command**: `/sh:cleanup-context` or automatic

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

    elif cleanup_type == "all":
        # Complete cleanup (use with caution)
        # Keep only essential project memories
        essential_patterns = ["spec_analysis", "phase_plan", "final_results"]
        delete_keys = [k for k in all_keys
                      if not any(pattern in k for pattern in essential_patterns)]
        for key in delete_keys:
            delete_memory(key)
        print(f"🧹 Complete cleanup: removed {len(delete_keys)} memories")
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

---

## Integration with Other Shannon Components

### Integration with Wave Orchestration

**Wave Start**:
```python
# Before wave starts, load previous wave context
if wave_number > 1:
    previous_wave_key = f"wave_{wave_number-1}_complete"
    previous_results = read_memory(previous_wave_key)
    # Use previous results to inform current wave
```

**Wave Completion**:
```python
# After wave completes, save results
write_memory(f"wave_{wave_number}_complete_{timestamp}", {
    "wave_number": wave_number,
    "agents_used": ["agent1", "agent2"],
    "files_created": [...],
    "decisions_made": [...],
    "next_wave_context": "..."
})
```

---

### Integration with Phase Planning

**Phase Transition**:
```python
# When moving to next phase
write_memory(f"phase_{current_phase}_complete", {
    "phase": current_phase,
    "validation_gates": "passed",
    "duration": calculate_duration(),
    "next_phase": next_phase,
    "handoff_context": "..."
})
```

---

### Integration with Sub-Agents

**All sub-agents MUST load context at start**:

```python
# MANDATORY context loading in every sub-agent
def sub_agent_initialization():
    # Step 1: Load project context
    spec = read_memory("spec_analysis")
    phase_plan = read_memory("phase_plan")

    # Step 2: Load wave context
    current_wave = read_memory("active_wave")
    previous_wave_results = read_memory(f"wave_{current_wave-1}_complete")

    # Step 3: Load specific context for this agent
    my_context = read_memory(f"agent_{agent_name}_context")

    # Step 4: Proceed with full understanding
    execute_with_context(spec, phase_plan, previous_wave_results, my_context)
```

---

## Troubleshooting

### Problem: Checkpoint Not Saved Before Auto-Compact

**Symptoms**:
- Context lost after auto-compact
- Previous work not accessible
- User complains of having to restart

**Solution**:
```python
# Verify PreCompact hook installed
check_hook_installed("~/.claude/hooks/precompact.py")

# Manually create checkpoint
create_manual_checkpoint()

# Test hook
test_precompact_hook()
```

---

### Problem: Cannot Restore Context

**Symptoms**:
- restore command fails
- Memories not found
- Incomplete restoration

**Solution**:
```python
# List all checkpoints
checkpoints = [k for k in list_memories() if "checkpoint" in k]

# Try each checkpoint until one works
for checkpoint_key in sorted(checkpoints, reverse=True):
    try:
        restore_from_checkpoint(checkpoint_key)
        break
    except:
        continue

# If all fail, start fresh but inform user
if not restored:
    print("⚠️ Could not restore context. Starting fresh.")
    print("Previous work may be lost. Consider manual recovery.")
```

---

### Problem: Too Many Memories (Storage Full)

**Symptoms**:
- Slow memory operations
- Storage warnings
- list_memories() takes too long

**Solution**:
```python
# Execute cleanup
cleanup_context("old_checkpoints")
cleanup_context("session")

# Archive old memories
archive_old_memories(days_threshold=30)

# Optimize memory usage
consolidate_related_memories()
```

---

### Problem: Memory Key Not Found

**Symptoms**:
- read_memory() returns None
- Expected context missing
- Wave results unavailable

**Solution**:
```python
# Search for similar keys
all_keys = list_memories()
similar = [k for k in all_keys if target_pattern in k]

# Use fuzzy matching
possible_matches = fuzzy_match_keys(target_key, all_keys)

# Inform user of issue
print(f"⚠️ Memory '{target_key}' not found")
print(f"Similar keys: {similar}")
print("Proceeding with partial context...")
```

---

## Summary

**Context Management Goals**:
- ✅ Zero context loss across auto-compact events
- ✅ Complete session state preservation
- ✅ Fast context restoration (<30 seconds)
- ✅ Cross-wave context sharing
- ✅ Efficient memory usage

**Key Components**:
1. **PreCompact Hook**: Automatic checkpoint before compact
2. **Checkpoint Strategy**: Systematic state preservation
3. **Restore Strategy**: Complete context recovery
4. **Memory Naming**: Organized, discoverable key patterns
5. **Cleanup Strategy**: Efficient storage management

**Integration Points**:
- Wave orchestration (wave context)
- Phase planning (phase transitions)
- Sub-agents (mandatory context loading)
- Commands (checkpoint/restore commands)

**Best Practices**:
- Save before risky operations
- Document key decisions
- Cross-reference memories
- Use discovery for rebuilding
- Clean up regularly

---

**Result**: Shannon V3 achieves zero context loss through systematic context preservation using PreCompact hook + Serena MCP integration.