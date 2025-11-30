# /sh:checkpoint - Checkpoint Management - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sh:checkpoint - Checkpoint Management

## Purpose

Create, load, and manage execution checkpoints that capture complete system state for rollback, recovery, and session continuity across context compactions.

**Core Objective**: Enable time-travel debugging and recovery by preserving complete state snapshots at critical execution boundaries.

---

## Command Metadata

```yaml
command: /sh:checkpoint
aliases: [shannon:cp, shannon:save]
category: State Management
sub_agent: CHECKPOINT_GUARDIAN
mcp_servers:
  primary: Serena
  required: true
tools:
  - Read
  - Write
  - TodoWrite
  - mcp__memory__read_graph
outputs:
  - Checkpoint files
  - State snapshots
  - Recovery metadata
  - Comparison reports
```

---

## Usage Patterns

### Basic Usage
```bash
# Create checkpoint at current state
/sh:checkpoint

# Create named checkpoint
/sh:checkpoint create important_milestone

# Load specific checkpoint
/sh:checkpoint load cp_abc123

# List recent checkpoints
/sh:checkpoint list

# Compare checkpoints
/sh:checkpoint compare cp_abc123 cp_def456

# Rollback to checkpoint
/sh:checkpoint rollback cp_abc123
```

### Context-Aware Usage
```bash
# Before risky operation
User: "About to refactor entire auth system"
Response: /sh:checkpoint create before_auth_refactor
→ Safe recovery point established

# After auto-compact
Context compacted → PreCompact hook triggered
→ /sh:checkpoint create precompact_auto
→ Full state preserved

# Session resumption
New session starts → Context limited
Response: /sh:checkpoint load latest
→ Full context restored from checkpoint
```

---

## Checkpoint Actions

### CREATE - Create New Checkpoint

**Purpose**: Capture current complete state

**What Gets Captured**:
```yaml
checkpoint_content:
  memory_snapshot:
    - Complete memory graph (all entities and relations)
    - Entity observations
    - Relationship types and metadata
  
  execution_state:
    - Active TodoWrite items with status
    - Completed tasks today
    - Current phase and wave info
    - Operation progress percentage
  
  goal_context:
    - North Star goal (if set)
    - Goal alignment scores
    - Recent aligned operations
  
  session_metadata:
    - Wave session ID
    - Wave strategy type
    - Phase boundaries crossed
    - Time elapsed
  
  decision_history:
    - Recent decisions and rationale
    - Trade-offs considered
    - Alternative paths explored
  
  execution_timeline:
    - Operation start time
    - Phase completion times
    - Checkpoint creation time
```

**Auto-Checkpoint Triggers**:
- End of each wave phase
- Before context compaction (PreCompact hook)
- Major decision points
- Error recovery situations
- Every 30 minutes during long operations

**Example**:
```bash
/sh:checkpoint create end_of_phase_2

# Output:
✅ Checkpoint created: cp_20251003_143022_a7f3
📦 Captured:
   - 42 entities, 78 relations
   - 5 active todos, 12 completed
   - Wave 3, Phase 2/4
   - North Star alignment: 0.85
💾 Saved to: ~/.claude/shannon/checkpoints/cp_20251003_143022_a7f3.json
```

### LOAD - Load Checkpoint

**Purpose**: Restore state from saved checkpoint

**What Gets Restored**:
- Memory graph entities and relations
- TodoWrite state
- Wave session context
- North Star goal
- Execution timeline

**Example**:
```bash
/sh:checkpoint load cp_20251003_143022_a7f3

# Output:
🔄 Loading checkpoint: cp_20251003_143022_a7f3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Checkpoint Date: 2025-10-03 14:30:22 (2 hours ago)

✅ Restored:
   - 42 entities, 78 relations → Memory graph
   - 5 todos (3 pending, 2 complete) → TodoWrite
   - Wave 3, Phase 2/4 → Session context
   - "Build secure auth" → North Star goal

🎯 Ready to continue from Phase 2
```

### LIST - List Available Checkpoints

**Purpose**: Show recent checkpoints for selection

**Example**:
```bash
/sh:checkpoint list

# Output:
📋 AVAILABLE CHECKPOINTS (Last 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. cp_20251003_160015_x9k2 (15 min ago) - Manual: "end_of_session"
   Wave 3, Phase 4/4 | 47 entities | Alignment: 0.91

2. cp_20251003_143022_a7f3 (2 hours ago) - Auto: "phase_boundary"
   Wave 3, Phase 2/4 | 42 entities | Alignment: 0.85

3. cp_20251003_120500_p3m1 (4 hours ago) - Auto: "precompact"
   Wave 2, Phase 3/3 | 38 entities | Alignment: 0.78

4. cp_20251002_173045_q8r7 (Yesterday) - Manual: "daily_save"
   Wave 1, Complete | 35 entities | Alignment: 0.82

[... more checkpoints ...]
```

### COMPARE - Compare Two Checkpoints

**Purpose**: Identify differences between checkpoint states

**Example**:
```bash
/sh:checkpoint compare cp_abc123 cp_def456

# Output:
🔍 CHECKPOINT COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Checkpoint A**: cp_abc123 (Wave 2, Phase 1)
**Checkpoint B**: cp_def456 (Wave 2, Phase 3)
**Time Delta**: 1 hour 15 minutes

**Memory Changes**:
➕ Added: 8 entities, 15 relations
➖ Removed: 2 entities
✏️  Modified: 12 entities (observations updated)

**Progress Changes**:
➕ Completed: 7 todos
🔄 In Progress: 2 todos (was 0)
📋 New Todos: 3 added

**Goal Alignment**:
Before: 0.78
After: 0.85
Change: +0.07 (improved)

**Key Differences**:
1. Auth implementation completed
2. OAuth integration added
3. Rate limiting entity created
```

### ROLLBACK - Rollback to Checkpoint

**Purpose**: Revert to previous checkpoint state

**Options**:
- Full rollback (discard all changes)
- Partial rollback (preserve memory changes)

**Example**:
```bash
/sh:checkpoint rollback cp_abc123

# Output:
⚠️  ROLLBACK CONFIRMATION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Target Checkpoint**: cp_abc123 (2 hours ago)
**Current State**: Wave 3, Phase 3/4
**Rollback Target**: Wave 2, Phase 1/3

**Changes to Discard**:
- 2 completed waves (Wave 2 Phase 2-3, Wave 3)
- 15 new memory entities
- 8 completed todos

**Preserve memory changes?** [y/N]

# After confirmation:
✅ Rolled back to cp_abc123
🔄 State restored to Wave 2, Phase 1
📊 Memory: Full rollback (entities removed)
🎯 North Star: Preserved
```

---

## Execution Flow

### Step 1: Activate CHECKPOINT_GUARDIAN

**Sub-Agent Activation**:
```python
# Activate checkpoint management agent
activate_agent("CHECKPOINT_GUARDIAN")

# Agent characteristics:
# - State preservation specialist
# - Recovery coordinator
# - Consistency validator
# - Timeline manager
```

### Step 2: Parse Action and Parameters

**Action Router**:
```python
# STEP 1: Parse command
action = parse_action(command)  # create, load, list, compare, rollback
params = parse_parameters(command)

# STEP 2: Validate action
if action not in VALID_ACTIONS:
    error("Invalid action. Use: create, load, list, compare, rollback")
    
# STEP 3: Validate required parameters
validate_parameters(action, params)
```

### Step 3: Execute Action Logic

**Action-Specific Execution**:
```python
if action == "create":
    execute_create_checkpoint(params.get("checkpoint_name"))
    
elif action == "load":
    execute_load_checkpoint(params["checkpoint_id"])
    
elif action == "list":
    execute_list_checkpoints(params.get("limit", 10))
    
elif action == "compare":
    execute_compare_checkpoints(params["checkpoint1"], params["checkpoint2"])
    
elif action == "rollback":
    execute_rollback_checkpoint(
        params["checkpoint_id"],
        params.get("preserve_memory", False)
    )
```

### Step 4: Update Memory and Storage

**Persistence Operations**:
```python
# For CREATE
def execute_create_checkpoint(name: str):
    # Read current memory graph
    memory_graph = read_graph()
    
    # Capture todo state
    todo_state = get_current_todos()
    
    # Build checkpoint
    checkpoint = {
        "id": generate_checkpoint_id(),
        "name": name,
        "timestamp": now(),
        "memory_graph": memory_graph,
        "todo_state": todo_state,
        "wave_session": get_wave_state(),
        "north_star": read_memory("north_star_goal"),
        "version": "3.0"
    }
    
    # Save to storage
    save_checkpoint(checkpoint)
    
    # Update memory
    create_entities(entities=[{
        "name": f"checkpoint_{checkpoint['id']}",
        "entityType": "Checkpoint",
        "observations": [
            f"Created: {checkpoint['timestamp']}",
            f"Entities: {len(memory_graph['entities'])}",
            f"Name: {name}"
        ]
    }])
```

---

## Sub-Agent Integration

### CHECKPOINT_GUARDIAN Role

**Specialization**: State preservation and recovery management

**Responsibilities**:
1. **Checkpoint Creation**: Capture complete system state
2. **State Validation**: Ensure checkpoint consistency
3. **Recovery Coordination**: Manage checkpoint loading
4. **Timeline Management**: Track checkpoint history
5. **Rollback Safety**: Validate rollback operations

**Agent Characteristics**:
```yaml
personality: Careful, methodical, safety-focused
communication_style: Clear warnings and confirmations
focus_areas:
  - State consistency
  - Recovery reliability
  - Timeline integrity
  - Data preservation
strengths:
  - Complete state capture
  - Safe rollback procedures
  - Timeline visualization
  - Recovery validation
```

---

## Integration with Shannon Commands

### Related Commands

**Before Checkpoints**:
- `/sh:wave` - Executes with automatic checkpoints
- `/sh:north-star` - Goal included in checkpoints

**With Checkpoints**:
- `/sh:status checkpoint` - Check checkpoint status
- `/sh:memory` - Memory included in checkpoints

**After Checkpoints**:
- `/sh:wave` - Resume from checkpoint
- `/sh:restore` - Alternative restore command

---

## Technical Implementation

### Checkpoint Storage Format

```json
{
  "id": "cp_20251003_143022_a7f3",
  "name": "end_of_phase_2",
  "timestamp": "2025-10-03T14:30:22Z",
  "version": "3.0",
  
  "memory_graph": {
    "entities": [...],
    "relations": [...]
  },
  
  "todo_state": {
    "active": [...],
    "completed": [...]
  },
  
  "wave_session": {
    "wave_id": "wave_20251003_120000",
    "strategy": "linear",
    "current_phase": 2,
    "total_phases": 4,
    "phase_history": [...]
  },
  
  "north_star": {
    "goal": "Build secure authentication system",
    "alignment_score": 0.85
  },
  
  "execution_timeline": {
    "start_time": "2025-10-03T12:00:00Z",
    "phase_completions": [...],
    "checkpoint_time": "2025-10-03T14:30:22Z"
  }
}
```

---

## Success Criteria

**Checkpoint operations succeed when**:
- ✅ Complete state captured in checkpoints
- ✅ Memory graph fully queryable after restore
- ✅ Rollback preserves consistency
- ✅ Checkpoints properly versioned
- ✅ Timeline integrity maintained
- ✅ Storage limits respected (50 checkpoints)
- ✅ Load operations restore full functionality

**Checkpoint operations fail if**:
- ❌ Incomplete state capture
- ❌ Memory corruption after restore
- ❌ Inconsistent rollback state
- ❌ Missing critical data
- ❌ Storage limit exceeded without cleanup

---

## Summary

`/sh:checkpoint` provides comprehensive state management through:

- **Create**: Capture complete system snapshots
- **Load**: Restore previous states seamlessly
- **List**: Browse checkpoint history
- **Compare**: Identify state differences
- **Rollback**: Revert to previous state safely

**Key Principle**: Checkpoints enable fearless experimentation and guaranteed recovery, making complex operations safe and reversible.
