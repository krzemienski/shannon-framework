---
name: shannon:checkpoint
description: Create, load, or manage execution checkpoints for recovery
usage: /shannon:checkpoint [label] [--load checkpoint_id] [--list]
---

# Checkpoint Management Command

## Overview

Creates and manages Shannon Framework checkpoints through delegation to the context-preservation skill. Enables zero-context-loss multi-session work with comprehensive state snapshots.

## Prerequisites

- Serena MCP available (check with `/shannon:check_mcps`)

## Workflow

### Step 1: Validate Input and Determine Mode

Parse command arguments to determine checkpoint operation:

**Mode Detection:**
- No arguments → `mode: "checkpoint"` (create checkpoint)
- Text label provided → `mode: "checkpoint"` with custom label
- `--load {checkpoint_id}` → `mode: "load"` (restore checkpoint)
- `--list` → `mode: "list"` (show available checkpoints)
- `--compare {id1} {id2}` → `mode: "compare"` (compare two checkpoints)

### Step 2: Invoke context-preservation Skill

Delegate to `@skill context-preservation` with appropriate mode:

**For CREATE mode (manual checkpoint):**
```
@skill context-preservation
- Input:
  * mode: "checkpoint"
  * label: "{user_label or auto-generated}"
  * include_files: true
  * include_tests: true
  * compression: true
- Output: checkpoint_result
```

**For WAVE-CHECKPOINT mode (automatic):**
```
@skill context-preservation
- Input:
  * mode: "wave-checkpoint"
  * label: "wave-{wave_number}-complete"
  * wave_number: {current_wave}
  * include_files: true
  * include_tests: true
- Output: checkpoint_result
```

**For PRECOMPACT mode (emergency):**
```
@skill context-preservation
- Input:
  * mode: "precompact"
  * label: "emergency-{timestamp}"
  * compression: true
- Output: checkpoint_result
```

**For LIST mode:**
```
@skill context-restoration
- Input:
  * mode: "list"
  * limit: 10
- Output: checkpoints_list
```

**For LOAD mode:**
```
@skill context-restoration
- Input:
  * mode: "restore"
  * checkpoint_id: "{checkpoint_id}"
- Output: restoration_result
```

### Step 3: Present Results

Format skill output for user display:

**For CREATE mode:**
```markdown
✅ CHECKPOINT CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Checkpoint ID**: {checkpoint_id}
**Label**: {label}
**Type**: {type}
**Size**: {size_kb} KB

📦 Captured:
   - {entity_count} entities, {relation_count} relations
   - {tasks_completed} completed tasks, {tasks_active} active
   - Wave {wave_number}, Phase {phase}/{total_phases}
   - North Star alignment: {alignment_score}

💾 Storage: Serena MCP
🔄 Restore: /shannon:checkpoint --load {checkpoint_id}
⏰ Expires: {expires_at} ({retention_days} days)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Next Actions**:
{for each next_action}
- {action_description}
```

**For LIST mode:**
```markdown
📋 AVAILABLE CHECKPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{for each checkpoint}
{index}. {checkpoint_id} ({time_ago})
   Label: {label}
   Type: {type}
   Wave: {wave_number}, Phase: {phase}
   Progress: {tasks_completed}/{tasks_total} tasks
   Size: {size_kb} KB

{end for}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Restore**: /shannon:checkpoint --load {checkpoint_id}
**Compare**: /shannon:checkpoint --compare {id1} {id2}
```

**For LOAD mode:**
```markdown
🔄 CHECKPOINT RESTORED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Checkpoint**: {checkpoint_id}
**Created**: {created_at} ({time_ago})
**Label**: {label}

✅ Restored:
   - {entity_count} entities → Memory graph
   - {tasks_active} active tasks → TodoWrite
   - Wave {wave_number}, Phase {phase} → Session context
   - "{north_star_goal}" → North Star goal

🎯 Ready to Continue
{for each next_action}
- {action_description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same required arguments
- Compatible output format
- Enhanced with automatic wave checkpoints

**Changes from V3:**
- Internal: Now uses context-preservation skill (was monolithic command)
- Enhancement: Richer metadata collection (goals, waves, tests, agent states)
- Enhancement: Better compression for large checkpoints
- Enhancement: Automatic wave boundary checkpoints
- Enhancement: PreCompact hook integration
- No breaking changes to user interface

## Skill Dependencies

- context-preservation (REQUIRED for checkpoint creation)
- context-restoration (REQUIRED for checkpoint loading)

## MCP Dependencies

- Serena MCP (required for checkpoint storage)
- Sequential MCP (recommended for metadata analysis, complexity >= 0.70)
