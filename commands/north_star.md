---
name: shannon:north_star
description: Set and manage North Star goals with progress tracking
usage: /shannon:north_star [goal] [--update] [--history]
---

# North Star Goal Management Command

## Overview

Manages Shannon Framework's North Star goal system through delegation to the goal-management skill. Transforms vague goals into measurable milestones with persistent Serena MCP storage.

## Prerequisites

- Serena MCP available (check with `/shannon:check_mcps`)
- Goal text provided for setting new goals

## Workflow

### Step 1: Validate Input and Determine Mode

Parse command arguments to determine operation mode:

**Mode Detection:**
- No arguments → `mode: "list"` (show all active goals)
- `"history"` argument → `mode: "history"` (show goal history)
- Text argument + no `--update` → `mode: "set"` (create new goal)
- Text argument + `--update` → `mode: "update"` (update progress)
- Goal ID + `complete` → `mode: "complete"` (mark complete)

### Step 2: Invoke goal-management Skill

Delegate to `@skill goal-management` with appropriate mode:

**For SET mode (creating goal):**
```
@skill goal-management
- Input:
  * mode: "set"
  * goal_text: "{user's goal description}"
  * priority: "north-star" (default for /shannon:north_star)
- Output: goal_result
```

**For LIST mode (showing goals):**
```
@skill goal-management
- Input:
  * mode: "list"
- Output: goals_list
```

**For UPDATE mode (progress update):**
```
@skill goal-management
- Input:
  * mode: "update"
  * goal_id: "{goal_id from context or argument}"
  * notes: "{progress notes if provided}"
- Output: progress_result
```

**For HISTORY mode:**
```
@skill goal-management
- Input:
  * mode: "history"
- Output: history_result
```

**For COMPLETE mode:**
```
@skill goal-management
- Input:
  * mode: "complete"
  * goal_id: "{goal_id}"
- Output: completion_result
```

### Step 3: Present Results

Format skill output for user display:

**For SET mode:**
```markdown
🎯 NORTH STAR GOAL SET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Goal**: {goal_text}
**ID**: {goal_id}
**Priority**: North Star
**Progress**: 0%

**Milestones**:
{for each milestone}
├─ {milestone_name} ({weight}%)
   Status: {status}
   Criteria: {completion_criteria}

💾 Saved to Serena MCP
🔄 Restore: /shannon:restore {checkpoint_id}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Next Steps**:
- Track progress: /shannon:north_star
- Update progress: /shannon:north_star --update
- Create waves: @skill wave-orchestration
```

**For LIST mode:**
```markdown
🎯 ACTIVE GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ North Star Goal:
ID: {goal_id}
Goal: {goal_text}
Progress: {progress}% ({completed_milestones}/{total_milestones})
Next: {next_milestone_name}

{if other goals exist}
Other Goals:
{for each goal}
- {goal_text} ({priority}) - {progress}%
{end for}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**For UPDATE mode:**
```markdown
📊 PROGRESS UPDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Goal**: {goal_text}
**Progress**: {new_progress}% (+{progress_change}%)

**Completed Milestones**:
{for each completed}
✅ {milestone_name}

**Remaining Milestones**:
{for each remaining}
⏳ {milestone_name} ({weight}%)

{if progress >= 100}
🎉 Goal appears complete!
   Run: /shannon:north_star complete {goal_id}
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same required arguments
- Compatible output format
- Enhanced with Serena persistence

**Changes from V3:**
- Internal: Now uses goal-management skill (was monolithic command)
- Enhancement: Better milestone parsing from vague goals
- Enhancement: Progress tracking with health checks
- Enhancement: Milestone dependency validation
- No breaking changes to user interface

## Skill Dependencies

- goal-management (REQUIRED)

## MCP Dependencies

- Serena MCP (required for goal persistence)
- Sequential MCP (recommended for complex goal parsing)
