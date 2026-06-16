---
name: sh:restore
linked_skills:
  - shannon-context-restorer
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:restore
> **Skill-Based**: This command activates the `shannon-context-restorer` skill

## Description

Restores complete project state from a checkpoint, enabling:
- Session resumption after compaction
- Time-travel to previous project states
- Recovery from errors or mistakes
- Cross-session context continuity

Automatically triggered by **SessionStart hook** when PreCompact checkpoint detected.

## Usage

```bash
# Restore from specific checkpoint
/sh:restore checkpoint_myproject_1730739600000

# Restore latest checkpoint
/sh:restore --latest

# Restore with preview (don't apply)
/sh:restore checkpoint_id --preview

# Auto-restore (via SessionStart hook)
# Fires automatically on session start if PreCompact checkpoint exists
```

## Prerequisites

- Serena MCP must be available
- Valid checkpoint must exist

## Skill Activation

This command activates: **`shannon-context-restorer`**

📚 **Full restoration logic**: `skills/shannon-context-restorer/SKILL.md`

The skill will:
1. Load checkpoint from Serena MCP
2. Validate checkpoint integrity
3. Restore North Star goal
4. Restore active and pending todos
5. Restore phase and wave state
6. Restore decisions and context
7. Reload generated skills
8. Generate restoration report

## Auto-Restoration

**SessionStart Hook Integration**:
```
New session starts
  ↓
SessionStart hook checks for PreCompact checkpoint
  ↓
shannon-context-restorer activates automatically
  ↓
Context fully restored
  ↓
User can continue where they left off
```

**Result**: Seamless session resumption ✅

## Restoration Process

### Step 1: Load Checkpoint
```javascript
const checkpoint = await serena_read_memory(checkpoint_id);
const restore_info = await serena_read_memory(`${checkpoint_id}_restore_info`);
```

### Step 2: Restore State
```yaml
Restore Order:
  1. North Star goal → Foundation for all work
  2. Phase and wave → Position in plan
  3. Todos → Active work items
  4. Decisions → Historical context
  5. Files → Modified file list
  6. Skills → Generated skills reload
```

### Step 3: Validate Restoration
```yaml
Validation Checks:
  - North Star goal restored
  - Todos count matches checkpoint
  - Phase and wave correct
  - Generated skills available
  - File list accurate
```

## Output

The skill generates:
- Restoration confirmation
- State summary
- What was restored
- Files to review
- Next suggested actions

## Integration

**Command Flow**:
```
/sh:checkpoint → Creates checkpoint
  ↓
Session ends / Compaction occurs
  ↓
New session starts
  ↓
/sh:restore (auto) → shannon-context-restorer → Restores state
  ↓
Continue work seamlessly
```

## Examples

### Example 1: Manual Restore
```bash
$ /sh:restore checkpoint_myproject_1730739600000
🔄 Restoring from checkpoint...
✅ Context restored successfully

Restored State:
- North Star: "Build production-ready dashboard"
- Phase: Implementation (Phase 3)
- Wave: 2 of 4
- Todos: 3 active, 5 pending
- Files: 12 modified
- Skills: 3 generated (shannon-react-ui, shannon-postgres-prisma, shannon-browser-test)

Next Steps:
1. Review active todos
2. Continue Wave 2 tasks
3. Use /sh:wave 2 to execute
```

### Example 2: Auto-Restore (SessionStart)
```bash
# New session
👋 Welcome back to Shannon Framework

🔍 Detected PreCompact checkpoint from previous session
📅 Created: 2025-11-03 15:45:00 (2 hours ago)
🔄 Auto-restoring context...

✅ Context restored successfully

You were working on:
- Project: Production Dashboard
- Phase: Implementation
- Wave: 2 (in progress)
- Last checkpoint: "Completed authentication system"

Active Todos:
  1. Build user profile page
  2. Implement dashboard charts
  3. Add data export feature

Continue with: /sh:wave 2
```

### Example 3: Preview Mode
```bash
$ /sh:restore checkpoint_myproject_1730739600000 --preview
📋 Checkpoint Preview

Checkpoint ID: checkpoint_myproject_1730739600000
Created: 2025-11-03 14:30:00
Label: "Wave 2 complete"

Would Restore:
- Phase: Implementation → Implementation (no change)
- Wave: 3 → 2 (roll back 1 wave)
- Todos: 8 current → 6 from checkpoint (2 would be removed)
- Files: 15 modified → 12 from checkpoint
- Skills: Same (3 skills)

⚠️  Rolling back to earlier state. Proceed? (y/n)
```

## Restore Points

**Common Restore Scenarios**:

1. **After Compaction** (automatic):
   - PreCompact checkpoint created
   - Compaction occurs
   - SessionStart auto-restores
   - Result: Seamless continuity

2. **After Mistake**:
   - Made wrong changes
   - Restore to checkpoint before changes
   - Result: Clean rollback

3. **Branching Development**:
   - Save checkpoint at decision point
   - Try approach A
   - If doesn't work, restore checkpoint
   - Try approach B

4. **Cross-Session Work**:
   - Save checkpoint at end of day
   - Next day: restore to resume
   - Result: No loss of context

## Validation

Restoration validation ensures:
- ✅ Checkpoint exists and is valid
- ✅ All required fields present
- ✅ Restore metadata includes steps
- ✅ Generated skills are available
- ✅ State consistency verified

## Safety

**Restore Safety Checks**:
- Preview mode available
- Can't restore corrupted checkpoints
- Warning if rolling back significantly
- Confirmation for destructive restores

## See Also

- `/sh:checkpoint` - Create checkpoints
- `/sh:status` - View current state
- `/sh:memory` - Manage Serena MCP memories
- `/sh:wave` - Execute waves

---

**Shannon V4** - Context Restoration for Zero-Loss Continuity 🔄
