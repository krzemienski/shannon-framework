---
name: sh:checkpoint
command: /sh:checkpoint
description: "Manual context checkpoint - saves complete project state to Serena MCP for recovery"
category: command
complexity: standard
mcp-servers: [serena]
personas: []
sub-agents: [CONTEXT_GUARDIAN]
priority: critical
triggers: [checkpoint, save, backup, preserve]
---

# /sh:checkpoint - Manual Context Checkpoint

> **Critical Command**: Manually save complete session state to Serena MCP before context fills up or risky operations.

## Purpose

Creates comprehensive checkpoint of current project state including:
- All Serena memory keys (for complete restoration)
- Active wave and phase information
- Todo list and pending tasks
- Recent decisions and architectural context
- Sub-agent state and handoff data
- Quality validation status

**Goal**: Enable complete context recovery after auto-compact, session breaks, or errors.

---

## Activation Triggers

**Automatic Triggers**:
- Context usage ≥75% (yellow zone)
- Before major phase transitions
- Before spawning wave execution
- Before long-running operations
- PreCompact hook fires (auto-compact imminent)

**Manual Triggers**:
- User types `/sh:checkpoint`
- Before risky operations or experiments
- Before ending work session
- Before switching projects
- User requests "save state" or "backup context"

**Keywords**: checkpoint, save, backup, preserve, save state, create restore point

---

## Usage Patterns

### Basic Usage
```bash
/sh:checkpoint
# Auto-generates timestamp-based name
```

### Named Checkpoint
```bash
/sh:checkpoint before_wave_3
# Creates: shannon_checkpoint_before_wave_3
```

### Pre-Operation Checkpoint
```bash
/sh:checkpoint before_refactor
# Creates: shannon_checkpoint_before_refactor
```

### End-of-Session Checkpoint
```bash
/sh:checkpoint end_of_day_sept29
# Creates: shannon_checkpoint_end_of_day_sept29
```

---

## Command Execution Flow

When `/sh:checkpoint` activates:

### Phase 1: Context Collection
**Objective**: Gather all current state information

```python
# Step 1: Collect active work state
current_state = {
    "active_wave": current_wave_number,
    "active_phase": current_phase_name,
    "current_focus": what_working_on,
    "in_progress_files": list_of_files,
    "pending_tasks": active_todos
}

# Step 2: Collect completion status
completion_data = {
    "phase_completion_percent": estimated_percent,
    "waves_completed": list_of_completed_waves,
    "waves_pending": list_of_pending_waves,
    "last_completed_activity": recent_activity
}

# Step 3: Collect decision context
decision_context = {
    "recent_decisions": list_of_key_decisions,
    "architectural_choices": design_decisions,
    "technical_debt": known_issues
}
```

### Phase 2: Serena Memory Inventory
**Objective**: Capture ALL memory keys for restoration

```python
# CRITICAL STEP: List all Serena memories
all_memory_keys = list_memories()

# Categorize by type
categorized_keys = {
    "project_keys": [k for k in all_memory_keys if "project_" in k],
    "wave_keys": [k for k in all_memory_keys if "wave_" in k],
    "phase_keys": [k for k in all_memory_keys if "phase_" in k],
    "decision_keys": [k for k in all_memory_keys if "decision_" in k],
    "checkpoint_keys": [k for k in all_memory_keys if "checkpoint" in k]
}

# Example output:
"""
Found 15 Serena memory keys:
- spec_analysis_taskapp_20250930
- phase_plan_taskapp_20250930
- wave_1_complete_20250930
- wave_2_frontend_results
- wave_2_backend_results
- project_decisions_auth
- project_decisions_database
- active_wave_3
- todo_list_current
- ...
"""
```

### Phase 3: Checkpoint Creation
**Objective**: Write complete checkpoint to Serena

```python
# Generate checkpoint name
if user_provided_name:
    checkpoint_key = f"shannon_checkpoint_{user_provided_name}"
else:
    checkpoint_key = f"shannon_checkpoint_{ISO_timestamp}"

# Create comprehensive checkpoint object
checkpoint_data = {
    "checkpoint_metadata": {
        "checkpoint_name": checkpoint_key,
        "created_at": "2025-09-30T14:30:00Z",
        "session_id": current_session_id,
        "checkpoint_type": "manual",
        "created_by_command": "/sh:checkpoint",
        "trigger_reason": "user_requested|context_75%|before_wave|etc"
    },

    "context_preservation": {
        "serena_memory_keys": all_memory_keys,
        "total_keys": len(all_memory_keys),
        "last_key_updated": most_recent_key,
        "categorized_keys": categorized_keys
    },

    "project_state": {
        "current_wave": 3,
        "current_phase": {
            "number": 3,
            "name": "implementation",
            "completion_percent": 65
        },
        "last_activity": "Completed authentication middleware",
        "next_activity": "Implement API endpoints",
        "project_id": "taskapp_001"
    },

    "work_context": {
        "current_focus": "Building REST API endpoints",
        "in_progress_files": [
            "/src/api/auth.ts",
            "/src/middleware/jwt.ts"
        ],
        "pending_tasks": [
            "Complete user registration endpoint",
            "Add password reset flow",
            "Write API tests"
        ]
    },

    "wave_status": {
        "completed_waves": [
            {
                "wave_number": 1,
                "name": "Frontend Components",
                "status": "complete",
                "results_key": "wave_1_complete_20250930"
            },
            {
                "wave_number": 2,
                "name": "Backend API Structure",
                "status": "complete",
                "results_key": "wave_2_complete_20250930"
            }
        ],
        "active_wave": {
            "wave_number": 3,
            "name": "Database Integration",
            "status": "in_progress",
            "progress_percent": 40
        },
        "pending_waves": [
            {
                "wave_number": 4,
                "name": "Testing & Validation",
                "status": "planned"
            }
        ]
    },

    "decisions_context": {
        "architectural_decisions": [
            "JWT authentication with refresh tokens",
            "PostgreSQL for relational data",
            "Redis for session caching"
        ],
        "technical_choices": [
            "TypeScript strict mode",
            "Express.js framework",
            "Jest for testing"
        ],
        "known_issues": []
    },

    "sub_agent_context": {
        "active_agents": ["implementation-worker"],
        "agent_handoff_data": {
            "from_agent": "backend-architect",
            "to_agent": "implementation-worker",
            "context": "Complete auth implementation per wave 3 plan"
        }
    },

    "quality_state": {
        "validation_status": {
            "phase_1_gates": "passed",
            "phase_2_gates": "passed",
            "phase_3_gates": "in_progress"
        },
        "tests_passing": true,
        "known_issues": [],
        "tech_debt": []
    },

    "restoration_instructions": {
        "restore_command": "/sh:restore " + checkpoint_key,
        "restore_steps": [
            "1. Execute /sh:restore command",
            "2. Load all Serena keys listed above",
            "3. Resume from current wave/phase/task",
            "4. Continue with pending tasks"
        ]
    }
}

# Write checkpoint to Serena
write_memory(checkpoint_key, checkpoint_data)
```

### Phase 4: Verification & Confirmation
**Objective**: Verify checkpoint saved successfully

```python
# Verify checkpoint exists
verification = read_memory(checkpoint_key)

if verification:
    # Update latest checkpoint pointer
    write_memory("shannon_latest_checkpoint", checkpoint_key)

    # Success confirmation
    print(f"""
✅ CHECKPOINT SAVED SUCCESSFULLY

**Checkpoint Key**: {checkpoint_key}
**Created**: {timestamp}
**Preserved**: {len(all_memory_keys)} Serena memory keys
**Current State**: Phase {phase_number}, Wave {wave_number}
**Progress**: {completion_percent}% complete

**To Restore**:
/sh:restore {checkpoint_key}

**Safe to Continue**: Context preserved, can proceed safely.
    """)
else:
    # Failure handling
    print("❌ Checkpoint save failed. Retrying...")
```

---

## Sub-Agent Integration: CONTEXT_GUARDIAN

`/sh:checkpoint` activates the **CONTEXT_GUARDIAN** sub-agent for checkpoint orchestration.

### CONTEXT_GUARDIAN Responsibilities

**Role**: Checkpoint creation specialist ensuring complete state preservation

**Activation**: When `/sh:checkpoint` command executes

**Tasks**:
1. **Comprehensive Inventory**: List ALL Serena memory keys without omission
2. **State Collection**: Gather all project, wave, phase, and work context
3. **Structured Checkpoint**: Create properly formatted checkpoint object
4. **Verification**: Validate checkpoint saved correctly
5. **Confirmation**: Report checkpoint details to user

**Tools Used**:
- `list_memories()` - Inventory all Serena keys
- `read_memory(key)` - Load current state information
- `write_memory(key, data)` - Save checkpoint to Serena

**Quality Gates**:
- ✅ All memory keys captured (no omissions)
- ✅ Checkpoint structure complete (all required fields)
- ✅ Verification successful (checkpoint readable)
- ✅ User confirmation provided (clear instructions)

---

## Checkpoint Data Structure

### Required Fields

```yaml
checkpoint_metadata:
  checkpoint_name: string (unique identifier)
  created_at: ISO8601 timestamp
  session_id: string
  checkpoint_type: "manual|precompact|phase|wave"
  created_by_command: "/sh:checkpoint"
  trigger_reason: string

context_preservation:
  serena_memory_keys: array (CRITICAL - enables restoration)
  total_keys: integer
  last_key_updated: string
  categorized_keys: object

project_state:
  current_wave: integer
  current_phase: object
  last_activity: string
  next_activity: string
  project_id: string

work_context:
  current_focus: string
  in_progress_files: array
  pending_tasks: array

wave_status:
  completed_waves: array
  active_wave: object
  pending_waves: array

decisions_context:
  architectural_decisions: array
  technical_choices: array
  known_issues: array

restoration_instructions:
  restore_command: string
  restore_steps: array
```

---

## Checkpoint Naming Patterns

### Auto-Generated Names
```
shannon_checkpoint_20250930T143000Z
```
Format: `shannon_checkpoint_[ISO8601_timestamp]`

### User-Provided Names
```
shannon_checkpoint_before_wave_3
shannon_checkpoint_end_of_day
shannon_checkpoint_before_refactor
```
Format: `shannon_checkpoint_[user_name]`

### Checkpoint Discovery
```python
# Find all checkpoints
checkpoints = [k for k in list_memories() if "shannon_checkpoint_" in k]

# Find latest checkpoint
latest = read_memory("shannon_latest_checkpoint")

# Find specific checkpoint
specific = read_memory("shannon_checkpoint_before_wave_3")
```

---

## Integration with Other Commands

### Integration with /sh:restore
**Relationship**: Checkpoint creates restore point, restore loads it

```bash
# Create checkpoint
/sh:checkpoint before_experiment

# Work proceeds...
# Something goes wrong...

# Restore from checkpoint
/sh:restore before_experiment
```

### Integration with PreCompact Hook
**Relationship**: PreCompact creates automatic checkpoints, manual checkpoint gives user control

**PreCompact** (automatic):
- Triggers when auto-compact imminent
- Creates: `precompact_checkpoint_[timestamp]`
- User doesn't need to do anything

**/sh:checkpoint** (manual):
- User runs proactively
- Creates: `shannon_checkpoint_[name]`
- User controls timing and naming

**Together**: Complete coverage of checkpoint scenarios

### Integration with Wave Orchestration
**Relationship**: Checkpoint before/after wave execution

```bash
# Before wave
/sh:checkpoint before_wave_3

# Execute wave
[Wave 3 runs...]

# After wave (automatic checkpoint in wave completion)
```

---

## Output Examples

### Example 1: Basic Checkpoint
```bash
User: /sh:checkpoint

Output:
✅ CHECKPOINT SAVED SUCCESSFULLY

**Checkpoint Key**: shannon_checkpoint_20250930T143052Z
**Created**: 2025-09-30 14:30:52 UTC
**Preserved**: 12 Serena memory keys
**Current State**: Phase 3 (Implementation), Wave 3
**Progress**: 65% complete

**Memory Keys Preserved**:
- spec_analysis_taskapp_20250930
- phase_plan_taskapp_20250930
- wave_1_complete_20250930
- wave_2_complete_20250930
- wave_3_frontend_results
- project_decisions_auth
- active_wave_3
- todo_list_current
- (4 more...)

**To Restore**:
/sh:restore shannon_checkpoint_20250930T143052Z

**Safe to Continue**: Context preserved, can proceed safely.
```

### Example 2: Named Checkpoint
```bash
User: /sh:checkpoint before_database_migration

Output:
✅ CHECKPOINT SAVED SUCCESSFULLY

**Checkpoint Key**: shannon_checkpoint_before_database_migration
**Created**: 2025-09-30 15:45:00 UTC
**Preserved**: 15 Serena memory keys
**Current State**: Phase 3 (Implementation), Wave 4
**Progress**: 78% complete

**Checkpoint Purpose**: Pre-migration safety point
**Can Rollback With**: /sh:restore before_database_migration

**Safe to Proceed**: Database migration can proceed safely.
```

### Example 3: Context Full Warning
```bash
System: ⚠️ Context usage at 76% (yellow zone)

User: /sh:checkpoint

Output:
✅ CHECKPOINT SAVED SUCCESSFULLY (Context Pressure)

**Checkpoint Key**: shannon_checkpoint_20250930T160000Z
**Created**: 2025-09-30 16:00:00 UTC
**Preserved**: 18 Serena memory keys
**Context Status**: 76% full → Checkpoint created

**Recommendation**: Consider running /compact after current task completes
**Auto-Compact Protection**: PreCompact hook will create additional checkpoint

**Safe to Continue**: Context preserved for restoration if auto-compact triggers.
```

---

## Best Practices

### When to Create Checkpoints

**Before Risky Operations**:
- Major refactoring
- Database migrations
- Architecture changes
- Experimental approaches

**Context Pressure Points**:
- Context ≥75% full
- Before long wave execution
- Before multi-hour work sessions
- Before complex multi-step operations

**Natural Break Points**:
- End of work day
- Completed wave
- Phase transitions
- Before switching projects

### Checkpoint Naming Tips

**Good Names**:
```
✅ before_wave_3
✅ end_of_day_sept29
✅ pre_refactor
✅ stable_state_before_experiment
```

**Bad Names**:
```
❌ checkpoint
❌ backup
❌ temp
❌ save1
```

### Checkpoint Lifecycle

**Create → Use → Clean**:
```
1. Create checkpoint before risky operation
2. Perform operation
3. If successful: Keep checkpoint temporarily, delete after next checkpoint
4. If failed: Restore from checkpoint
5. Regular cleanup: Keep last 5 checkpoints, delete older ones
```

---

## Error Handling

### Checkpoint Save Failure
```python
if not write_memory_successful:
    # Retry once
    retry_write_memory(checkpoint_key, checkpoint_data)

    if still_failed:
        print("❌ Checkpoint save failed")
        print("Possible causes:")
        print("- Serena MCP server unavailable")
        print("- Network connectivity issue")
        print("- Storage quota exceeded")
        print("\nRecommendation: Retry or use /compact to free space")
```

### Missing Memory Keys
```python
# If some keys cannot be read
missing_keys = []
for key in all_keys:
    if not read_memory(key):
        missing_keys.append(key)

if missing_keys:
    print(f"⚠️ Warning: {len(missing_keys)} keys could not be accessed")
    print("Checkpoint created with available keys")
    print("May result in incomplete restoration")
```

---

## Boundaries

### WILL DO

**Checkpoint Operations**:
- ✅ Save complete current state to Serena MCP
- ✅ Preserve ALL memory keys for restoration
- ✅ Create restoration instructions
- ✅ Verify checkpoint success
- ✅ Update latest checkpoint pointer
- ✅ Provide confirmation to user

**State Capture**:
- ✅ Capture active wave and phase
- ✅ Capture pending tasks and todos
- ✅ Capture recent decisions and context
- ✅ Capture sub-agent state
- ✅ Capture quality validation status

### WILL NOT DO

**Out of Scope**:
- ❌ Modify project files or code
- ❌ Execute or restore checkpoints (that's `/sh:restore`)
- ❌ Compact conversation context (that's Claude Code's `/compact`)
- ❌ Delete or modify existing memories (except updating pointers)
- ❌ Make architectural or technical decisions
- ❌ Execute wave operations or sub-agents

---

## Success Criteria

Checkpoint command succeeds when:

✅ **All memory keys captured**: No omissions in Serena key list
✅ **Checkpoint saved**: write_memory() successful
✅ **Verification passed**: read_memory(checkpoint_key) returns data
✅ **User confirmation**: Clear output with restoration instructions
✅ **Latest pointer updated**: shannon_latest_checkpoint points to new checkpoint
✅ **Complete structure**: All required checkpoint fields present

**Quality Standard**: User can restore complete context from checkpoint alone

---

## Related Commands

- **`/sh:restore`**: Restore context from checkpoint
- **`/sh:cleanup-context`**: Clean up old checkpoints
- **`/compact`**: Claude Code's context compaction (separate from Shannon)

---

## Technical Notes

**Storage**: Checkpoints stored in Serena MCP persistent memory
**Retention**: Indefinite (until manually deleted or cleanup runs)
**Size**: Typically 2-5KB per checkpoint
**Performance**: <2 seconds to create checkpoint
**Limitations**: Serena MCP server must be available