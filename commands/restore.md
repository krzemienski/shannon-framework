---
name: shannon:restore
description: Restore project state from Serena MCP checkpoint
usage: /shannon:restore [checkpoint_id] [--goals] [--verbose]
---

# Project State Restoration Command

## Overview

Restores complete project state from Serena MCP checkpoints, enabling zero context loss after auto-compact events, session breaks, or context loss scenarios. This command orchestrates the context-restoration and goal-management skills to perform comprehensive context recovery.

## Prerequisites

- Serena MCP available (check with `/shannon:check_mcps`)
- Valid checkpoint exists (created by `/shannon:checkpoint` or PreCompact hook)

## Workflow

### Step 1: Validate Checkpoint Availability

Check that Serena MCP is available:
- Tool: Internal MCP detection
- Fallback: Display error message with setup instructions

### Step 2: Invoke context-preservation Skill (Restore Mode)

Use the `@skill context-preservation` skill with restore mode:

**Invocation:**
```
@skill context-preservation
- Input:
  * mode: "restore"
  * checkpoint_id: [user_provided_id or "latest"]
  * include_goals: [true if --goals flag present]
  * verbose: [true if --verbose flag present]
- Output: restoration_result
```

The context-preservation skill will:
1. Locate checkpoint (latest or specified)
2. Load checkpoint data from Serena
3. Restore all memory keys
4. Reconstruct project context
5. Validate restoration quality
6. Generate restoration report

### Step 3: Restore Goals (Optional)

If `--goals` flag present, invoke goal-management skill:

**Invocation:**
```
@skill goal-management
- Input:
  * mode: "restore"
  * checkpoint_id: [same as above]
- Output: goals_restoration_result
```

The goal-management skill will:
1. Load goal state from checkpoint
2. Restore active goals
3. Update goal progress tracking
4. Link goals to current context

### Step 4: Present Restoration Report

Format and display results:

```markdown
✅ CONTEXT RESTORED SUCCESSFULLY

📦 Checkpoint: {checkpoint_id}
🕐 Saved: {timestamp}
📚 Restored: {memory_count}/{total_memories} memories ({percentage}%)
🎯 Quality: {restoration_quality}%

## Project State
🔢 Project: {project_id}
📊 Phase: {active_phase}
🌊 Wave: {current_wave}/{total_waves}

## Current Focus
💡 {current_focus_description}

## Pending Tasks
{for each pending_task}
{index}. ⏳ {task_description}

## Completed Waves
{for each completed_wave}
✅ Wave {wave_number}: {wave_title} ({completion_date})
   {wave_summary}

{if goals_restored}
## Active Goals
{for each active_goal}
🎯 {goal_title}: {progress}%
   Status: {goal_status}
{end if}

## Next Steps
{recommended_next_actions}

▶️ Ready to continue where you left off.
```

## Output Format

### Success Output
```
✅ CONTEXT RESTORED SUCCESSFULLY
[Complete restoration report as shown above]
```

### Partial Restoration Output
```
⚠️ CONTEXT PARTIALLY RESTORED
[Report with missing memories and recovery recommendations]
```

### Failed Restoration Output
```
❌ RESTORATION FAILED
[Error details and recovery steps]
```

## Skill Dependencies

- context-preservation (REQUIRED) - Mode: restore
- goal-management (OPTIONAL) - Mode: restore (only if --goals flag)

## MCP Dependencies

- Serena MCP (required for checkpoint storage/retrieval)

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same required arguments (checkpoint_id optional)
- Compatible output format
- Enhanced restoration with skill orchestration

**Changes from V3:**
- Internal: Now orchestrates context-preservation skill (was monolithic)
- Enhancement: Better restoration quality validation
- Enhancement: Optional goal restoration with --goals flag
- Enhancement: Improved error recovery strategies
- No breaking changes

## Usage Examples

**Default Restoration (Latest Checkpoint):**
```bash
/shannon:restore
```

**Restore Specific Checkpoint:**
```bash
/shannon:restore SHANNON-W2-20251103T143000
```

**Restore with Goals:**
```bash
/shannon:restore --goals
```

**Verbose Restoration:**
```bash
/shannon:restore --verbose
```
