---
name: shannon-checkpoint-manager
display_name: "Shannon Checkpoint Manager"
description: "Context preservation and checkpoint creation for zero-context-loss across sessions and auto-compaction events"
category: management
version: "4.0.0"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_checkpoint command"
  - "checkpoint requested"
  - "save progress"
mcp_servers:
  required:
    - serena
allowed_tools:
  - serena_write_memory
  - serena_read_memory
  - serena_list_memories
  - serena_create_entities
  - serena_create_relations
  - Read
  - Glob
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
input:
  checkpoint_label:
    type: string
    description: "Human-readable checkpoint label"
    required: true
  include_files:
    type: boolean
    description: "Include modified file list"
    default: true
output:
  checkpoint_id:
    type: string
    description: "Unique checkpoint identifier"
  saved_state:
    type: object
    description: "Complete saved state"
  memory_keys:
    type: array
    description: "Serena memory keys written"
---

# Shannon Checkpoint Manager

> **Zero-Context-Loss**: Never lose project state across sessions or auto-compaction

## Purpose

Creates comprehensive project checkpoints that preserve:
- **Project State** - Current phase, wave, todos
- **Decisions** - Architecture decisions, trade-offs
- **Files Modified** - Complete change history
- **North Star Goal** - Project objective
- **Context** - All critical information

**Key Innovation**: Works with PreCompact hook for automatic checkpoint before auto-compaction.

## Capabilities

### 1. State Extraction
- Current project phase and wave
- Active todos (in_progress, pending)
- North Star goal
- Recent decisions
- Modified files list
- Generated skills
- MCP configuration

### 2. Serena Persistence
- Structured memory storage
- Knowledge graph relationships
- Queryable checkpoint history
- Cross-session durability

### 3. Checkpoint Metadata
- Timestamp and label
- Project identifier
- User context
- Session information

### 4. Restore Points
- Creates restore points for rollback
- Enables time-travel debugging
- Supports branching workflows

## Activation

**Automatic**:
```bash
/sh_checkpoint "Completed authentication system"
/sh_checkpoint "Wave 2 done"
```

**Manual**:
```bash
Skill("shannon-checkpoint-manager")
```

**PreCompact Hook** (Automatic):
```python
# Fires when token limit reached (75% threshold)
# Automatically creates checkpoint before compaction
```

## Execution Algorithm

### Step 1: Extract Project State

```javascript
const state = {
  project_id: extract_project_id(),

  // Current position
  current_phase: get_active_phase(),
  current_wave: get_active_wave(),

  // Active work
  active_todos: get_todos_by_status("in_progress"),
  pending_todos: get_todos_by_status("pending"),

  // Goals and decisions
  north_star_goal: read_memory("north_star_goal"),
  recent_decisions: extract_decisions(last_n_messages: 50),

  // Files and changes
  modified_files: get_modified_files(),
  file_summaries: summarize_file_changes(),

  // Skills and configuration
  generated_skills: list_generated_skills(),
  active_mcps: get_active_mcps(),

  // Metadata
  timestamp: Date.now(),
  session_id: get_session_id(),
  token_usage: get_token_usage()
};
```

### Step 2: Create Checkpoint Metadata

```javascript
const checkpoint = {
  id: `checkpoint_${state.project_id}_${state.timestamp}`,
  label: checkpoint_label,
  type: checkpoint_type, // "manual", "precompact", "wave_complete"
  project_id: state.project_id,
  created_at: state.timestamp,
  created_by: get_user_context(),

  // Quick access fields
  phase: state.current_phase,
  wave: state.current_wave,
  todos_count: state.active_todos.length + state.pending_todos.length,
  files_modified_count: state.modified_files.length
};
```

### Step 3: Save to Serena MCP

```javascript
// Primary checkpoint
await serena_write_memory(checkpoint.id, {
  checkpoint,
  state,
  version: "4.0.0"
});

// Create knowledge graph relationships
await serena_create_entities([
  {
    name: checkpoint.id,
    type: "checkpoint",
    metadata: checkpoint
  }
]);

// Link to project
await serena_create_relations([
  {
    from: state.project_id,
    to: checkpoint.id,
    type: "has_checkpoint"
  }
]);

// Index for quick access
await serena_write_memory("latest_checkpoint", {
  project_id: state.project_id,
  checkpoint_id: checkpoint.id,
  label: checkpoint_label,
  timestamp: state.timestamp
});
```

### Step 4: Create Restore Metadata

```javascript
// Save restore instructions
await serena_write_memory(`${checkpoint.id}_restore_info`, {
  restore_command: `/sh_restore ${checkpoint.id}`,
  restore_steps: [
    "Restore north_star_goal",
    "Restore active_todos",
    "Restore current_phase and wave",
    "Restore decisions and context",
    "Reload generated skills"
  ],
  files_to_review: state.modified_files
});
```

### Step 5: Generate Checkpoint Report

```javascript
const report = `
# Checkpoint Created ✅

**ID**: ${checkpoint.id}
**Label**: ${checkpoint_label}
**Timestamp**: ${new Date(state.timestamp).toISOString()}

## Project State
- **Phase**: ${state.current_phase}
- **Wave**: ${state.current_wave || 'N/A'}
- **Todos**: ${state.active_todos.length} in progress, ${state.pending_todos.length} pending

## North Star Goal
${state.north_star_goal || 'Not set'}

## Modified Files (${state.modified_files.length})
${state.modified_files.slice(0, 10).map(f => `- ${f}`).join('\n')}
${state.modified_files.length > 10 ? `... and ${state.modified_files.length - 10} more` : ''}

## Generated Skills (${state.generated_skills.length})
${state.generated_skills.map(s => `- ${s}`).join('\n')}

## Active MCPs
${state.active_mcps.map(m => `- ${m.name} (${m.status})`).join('\n')}

## Restore
To restore this checkpoint: \`/sh_restore ${checkpoint.id}\`

---
Saved to Serena MCP: ${checkpoint.id}
`;

return report;
```

## PreCompact Integration

**Automatic Zero-Context-Loss**:

```python
# hooks/precompact.py
def precompact_hook():
    """
    Fires automatically when token limit reached (75%)
    Creates checkpoint BEFORE auto-compaction
    """

    # Activate shannon-checkpoint-manager skill
    checkpoint_label = f"Auto-checkpoint before compaction"

    checkpoint_result = invoke_skill("shannon-checkpoint-manager", {
        "checkpoint_label": checkpoint_label,
        "include_files": True,
        "type": "precompact"
    })

    # Return success (allow compaction to proceed)
    return {"success": True, "checkpoint_id": checkpoint_result.id}
```

**SessionStart Restoration**:

```python
# hooks/session_start.py
def session_start_hook():
    """
    Automatically restores from latest checkpoint
    """

    latest = read_memory("latest_checkpoint")

    if latest and latest.type == "precompact":
        # Auto-restore from PreCompact checkpoint
        invoke_skill("shannon-context-restorer", {
            "checkpoint_id": latest.checkpoint_id
        })
```

## Checkpoint Types

### 1. Manual Checkpoint
```bash
/sh_checkpoint "Completed user authentication"
```
**Use**: Explicit save points during development

### 2. PreCompact Checkpoint
```python
# Automatic via hook
```
**Use**: Zero-context-loss before auto-compaction

### 3. Wave Complete Checkpoint
```bash
# Automatic after /sh_wave completes
```
**Use**: Save after each wave completion

### 4. Phase Complete Checkpoint
```bash
# Automatic after phase completion
```
**Use**: Major milestone save points

## Examples

### Example 1: Manual Checkpoint

```bash
# User creates checkpoint
/sh_checkpoint "Finished database schema design"

# Output:
# Checkpoint Created ✅
# ID: checkpoint_myproject_1699123456789
# Label: Finished database schema design
# Phase: Architecture
# Wave: 2
# Todos: 3 in progress, 5 pending
# Files Modified: 12 files
#
# Restore: /sh_restore checkpoint_myproject_1699123456789
```

### Example 2: PreCompact Auto-Checkpoint

```
[Token limit approaching 75%]
[PreCompact hook fires automatically]
[shannon-checkpoint-manager activates]
[Checkpoint created: checkpoint_myproject_precompact_1699123456789]
[Auto-compaction proceeds]
[SessionStart hook restores checkpoint automatically]
[Zero context loss ✅]
```

### Example 3: Checkpoint History

```bash
# List all checkpoints
/sh_memory list --filter checkpoint

# Output:
# checkpoint_myproject_1699100000000 - "Initial setup"
# checkpoint_myproject_1699110000000 - "Auth system complete"
# checkpoint_myproject_1699120000000 - "Wave 2 done"
# checkpoint_myproject_precompact_1699123456789 - "Auto-checkpoint"
```

## State Preserved

### Full State Structure

```javascript
{
  // Identity
  project_id: "my-react-app",
  session_id: "sess_abc123",

  // Position
  current_phase: "Implementation",
  current_wave: 3,

  // Work
  active_todos: [
    {id: 1, content: "Implement auth", status: "in_progress"},
    {id: 2, content: "Write tests", status: "in_progress"}
  ],
  pending_todos: [
    {id: 3, content: "Deploy", status: "pending"}
  ],

  // Goals
  north_star_goal: "Build production-ready React dashboard",

  // Decisions
  recent_decisions: [
    {
      decision: "Use PostgreSQL for database",
      rationale: "Better relational support",
      alternatives: ["MongoDB", "MySQL"],
      timestamp: 1699120000000
    }
  ],

  // Files
  modified_files: [
    "src/auth/AuthService.ts",
    "src/database/schema.sql",
    "tests/auth.test.ts"
  ],
  file_summaries: {
    "src/auth/AuthService.ts": "JWT authentication implementation",
    "src/database/schema.sql": "User and session tables"
  },

  // Skills
  generated_skills: [
    "shannon-react-ui",
    "shannon-postgres-prisma"
  ],

  // MCPs
  active_mcps: [
    {name: "serena", status: "connected"},
    {name: "puppeteer", status: "connected"}
  ],

  // Metadata
  timestamp: 1699123456789,
  token_usage: {total: 45000, remaining: 155000}
}
```

## Integration with Other Skills

**Used by**:
- shannon-wave-orchestrator (after wave completion)
- shannon-phase-planner (after phase completion)
- PreCompact hook (automatic)

**Uses**:
- shannon-serena-manager (for memory operations)

**Composition**:
```
/sh_checkpoint
  ↓
shannon-checkpoint-manager
  ↓ (uses)
shannon-serena-manager
  ↓
Serena MCP
```

## Performance

**Checkpoint Creation Time**: < 2 seconds
**Storage**: ~5-10KB per checkpoint (Serena)
**Restore Time**: < 1 second
**History**: Unlimited (Serena persistence)

## Best Practices

### DO ✅
- Create checkpoints after major milestones
- Use descriptive labels
- Create checkpoint before risky operations
- Review checkpoint history regularly

### DON'T ❌
- Create checkpoints too frequently (creates noise)
- Use generic labels ("checkpoint 1", "test")
- Skip checkpoints for multi-hour sessions
- Ignore PreCompact auto-checkpoints

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📚 **Checkpoint Patterns**: [resources/CHECKPOINT_PATTERNS.md](./resources/CHECKPOINT_PATTERNS.md)

---

**Shannon V4** - Zero-Context-Loss Guaranteed 🛡️
