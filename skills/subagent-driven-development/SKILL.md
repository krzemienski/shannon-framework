---
name: subagent-driven-development
description: Use for implementation plans - dispatches fresh subagent per task with quality scoring (0.00-1.00), code review gates, Serena pattern learning, and MCP tracking
---

# Subagent-Driven Development (Shannon-Enhanced)

## Overview

**Execute plans with fresh subagent per task + quantitative quality gates.**

Each task: Subagent implementation → Code review → Quality score → Advance if > 0.80.

Shannon enhancement: Numerical quality scoring, pattern learning from task history, MCP work tracking.

## When to Use

**Same-session task execution:**
- Staying in this session
- Tasks mostly independent
- Want continuous progress with quality gates
- Plan already written and validated

**Don't use when:**
- Need to review plan first
- Tasks are tightly coupled
- Plan needs revision

## Quality Scoring (0.00-1.00)

**Per-task scoring:**
```
task_quality_score = (
  (implementation_completeness) * 0.4 +
  (test_coverage) * 0.35 +
  (code_review_score) * 0.25
)
```

**Thresholds:**
- 0.00-0.50: Needs major rework (Critical issues)
- 0.51-0.80: Has issues, fixable (Important issues)
- 0.81-0.95: Good, minor cleanup (Minor issues)
- 0.96-1.00: Excellent, ready to advance

**Gate rule:** Only advance to next task if task_quality_score > 0.80

## The Process

### 1. Load Plan & Setup Tracking

```bash
# Serena metric initialization
plan_metadata = {
  plan_file: "path/to/plan.md",
  total_tasks: N,
  tasks_completed: 0,
  cumulative_quality_score: 0.0,
  estimated_completion_time: "X hours"
}
```

Create TodoWrite with all tasks, all in "pending" state.

### 2. Execute Task (Fresh Subagent)

Mark task as in_progress. Dispatch:

```markdown
**Task N:** [task_name]
Implementation scope: [read task N from plan]

Requirements:
1. Implement exactly what task specifies
2. Write tests (TDD if task requires)
3. Verify all tests pass
4. Commit with conventional message
5. Report: what you implemented, test results, files changed

Work directory: [path]
```

Subagent reports implementation summary.

### 3. Code Review Gate

**Dispatch code-reviewer with metrics:**

```bash
# Review metrics (Serena)
review_context = {
  task_number: N,
  what_implemented: "[subagent report]",
  plan_requirement: "[task N from plan]",
  base_commit: "[SHA before task]",
  head_commit: "[SHA after task]",
  test_results: "[pass/fail counts]"
}
```

Reviewer returns: Strengths, Issues (Critical/Important/Minor), Assessment.

**Calculate code_review_score:**
```
code_review_score = (
  0.0 if critical_issues > 0 else (
    1.0 - (important_issues * 0.15) - (minor_issues * 0.05)
  )
)
```

### 4. Calculate Task Quality Score

```bash
task_quality_score = (
  implementation_completeness * 0.4 +  # Did they do what task asked?
  test_coverage * 0.35 +               # Tests > 80% code coverage?
  code_review_score * 0.25             # Review assessment score
)
```

Log to Serena with timestamp.

### 5. Gate Decision

```
IF task_quality_score > 0.80:
  ✓ ADVANCE: Mark complete, next task
ELSE:
  ⚠ NEEDS FIXES: Dispatch fix subagent
    "Fix issues from review: [list critical/important]"
    Re-review and recalculate score
    Loop until > 0.80
```

### 6. All Tasks Complete

After all tasks pass gates:

```bash
# Calculate cumulative metrics
cumulative_quality = average(all_task_quality_scores)
tasks_requiring_rework = count(tasks with score < 0.85 initially)

# Log to Serena for pattern learning
completion_metrics = {
  cumulative_quality_score: X.XX,
  tasks_completed: N,
  total_rework_cycles: R,
  average_quality_trend: "improving|stable|declining"
}
```

Dispatch final code-reviewer: "Review all completed tasks for integration readiness."

### 7. Finish Development

After final review passes:

```
I'm using the finishing-a-development-branch skill to complete this work.
```

Follow finishing-a-development-branch workflow.

## Pattern Learning (Serena)

**Track across plans:**
- Task types that consistently score > 0.90
- Common issue patterns (missing tests, incomplete docs)
- Rework cycles per task type
- Average time per quality level

**Use historical patterns to:**
- Predict which new tasks might need rework
- Alert if task_quality_score declining (need different approach)
- Estimate completion time more accurately
- Identify high-risk task patterns

## Metrics Checklist

- [ ] plan_metadata initialized (Serena)
- [ ] TodoWrite created with all tasks
- [ ] Task 1 marked in_progress
- [ ] Subagent dispatched, reports back
- [ ] Code review completed, metrics logged
- [ ] task_quality_score calculated > 0.80
- [ ] Task 1 marked completed, next task in_progress
- [ ] ... repeat until all tasks complete
- [ ] cumulative_quality_score calculated
- [ ] Final review passes
- [ ] finishing-a-development-branch invoked

## Common Mistakes

❌ Skip code review between tasks
✅ Review every task before advancing

❌ Ignore task_quality_score, advance anyway
✅ Enforce quality gate > 0.80

❌ Don't track metrics
✅ Log all scores to Serena for learning

❌ Parallel implementation subagents (conflicts)
✅ One subagent at a time, sequential

## Red Flags

**Never:**
- Skip quality gate
- Proceed with critical issues unfixed
- Dispatch multiple implementation agents simultaneously
- Advance without code review

## Integration

**Requires:**
- **writing-plans** - Creates plan file
- **requesting-code-review** - Reviews each task
- **finishing-a-development-branch** - Completes development

**With:**
- **testing-skills-with-subagents** - Subagent tests its code
- **dispatching-parallel-agents** - Could test code in parallel

## Real-World Impact

Sample implementation (4 tasks):
- Task 1: quality_score 0.92 ✓ advance
- Task 2: quality_score 0.76 ⚠ rework → 0.88 ✓ advance
- Task 3: quality_score 0.91 ✓ advance
- Task 4: quality_score 0.85 ✓ advance
- cumulative_quality: 0.89
- 1 task required rework
- Pattern learning: Note task 2 type for future
