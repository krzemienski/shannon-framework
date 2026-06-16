---
name: sh:checkpoint
linked_skills:
  - shannon-checkpoint-manager
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:checkpoint
> **Skill-Based**: This command activates the `shannon-checkpoint-manager` skill

## Description

Creates comprehensive project checkpoints preserving complete state for zero-context-loss across sessions:
- Current phase and wave
- Active and pending todos
- North Star goal and recent decisions
- Modified files and generated skills
- MCP configuration state

Integrates with **PreCompact hook** for automatic checkpointing before context compaction.

## Usage

```bash
# Create manual checkpoint
/sh:checkpoint "Completed authentication system"

# Create checkpoint with label
/sh:checkpoint --label "Wave 2 complete"

# Auto-checkpoint (via PreCompact hook)
# Fires automatically at 75% token limit
```

## Prerequisites

- Serena MCP must be available
- Project must be initialized

## Skill Activation

This command activates: **`shannon-checkpoint-manager`**

📚 **Full checkpoint logic**: `skills/shannon-checkpoint-manager/SKILL.md`

The skill will:
1. Extract complete project state (8 required fields)
2. Create checkpoint with standard ID format (`checkpoint_${project}_${timestamp}`)
3. Save to Serena MCP
4. Create knowledge graph entities and relations
5. Save restore metadata
6. Generate checkpoint report

## Zero-Context-Loss Guarantee

**PreCompact Hook Integration**:
```
Token usage reaches 75%
  ↓
PreCompact hook triggers automatically
  ↓
shannon-checkpoint-manager creates checkpoint
  ↓
Auto-compaction proceeds (safe)
  ↓
SessionStart hook restores context automatically
```

**Result**: No context loss even after compaction ✅

## Checkpoint Structure

Every checkpoint includes:
```yaml
Required Fields (8):
  - project_id
  - current_phase
  - current_wave
  - active_todos
  - pending_todos
  - north_star_goal
  - modified_files
  - generated_skills
```

## Output

The skill generates:
- Checkpoint ID (e.g., `checkpoint_myproject_1730739600000`)
- Restore command
- State summary
- Files included
- Success confirmation

## Integration

**Command Flow**:
```
/sh:checkpoint → shannon-checkpoint-manager → Saves checkpoint
  ↓
Checkpoint ID returned
  ↓
/sh:restore checkpoint_id → shannon-context-restorer → Restores state
```

## Examples

### Example 1: Manual Checkpoint
```bash
$ /sh:checkpoint "Finished Wave 2"
✅ Checkpoint created: checkpoint_myproject_1730739600000

State Captured:
- Phase: Implementation
- Wave: 2 (completed)
- Todos: 3 active, 5 pending
- Files: 12 modified
- Skills: 3 generated
```

### Example 2: Auto-Checkpoint (PreCompact)
```bash
# Token usage: 75% reached
⚠️  Approaching token limit, creating auto-checkpoint...
✅ Auto-checkpoint: checkpoint_myproject_precompact_1730739700000
✅ Compaction proceeding safely
```

### Example 3: Session Resumption
```bash
# New session starts
🔄 Detected PreCompact checkpoint from previous session
✅ Context restored: checkpoint_myproject_precompact_1730739700000

Restored State:
- Phase: Implementation
- Wave: 2
- Todos: 3 active
- North Star: "Build production-ready dashboard"
```

## Validation

Checkpoint validation ensures:
- ✅ All 8 required fields present
- ✅ Standard ID format used
- ✅ Saved to Serena MCP successfully
- ✅ Knowledge graph relationships created
- ✅ Restore metadata included

## See Also

- `/sh:restore` - Restore from checkpoint
- `/sh:status` - View current state
- `/sh:memory` - Manage Serena MCP memories

---

**Shannon V4** - Zero-Context-Loss Checkpoint System 💾
