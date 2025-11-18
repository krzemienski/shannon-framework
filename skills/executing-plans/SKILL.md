---
name: executing-plans
description: Use when partner provides a complete implementation plan to execute in controlled batches with review checkpoints - loads plan, reviews critically with Shannon quantitative analysis, executes tasks in complexity-based batches, runs validation gates, reports for review between batches
---

# Executing Plans

## Overview

Load plan, review critically with Shannon's quantitative lens, execute tasks in batches, run validation gates, report for review between batches.

**Core principle**: Batch execution with checkpoints + Shannon validation gates = systematic quality.

**Announce at start**: "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan with Shannon Analysis

**1. Read plan file** (use forced-reading-protocol if >3000 lines)

**2. Extract Shannon metadata**:
```python
metadata = {
    "complexity": extract_complexity_score(plan),  # 0.00-1.00
    "total_tasks": count_tasks(plan),
    "estimated_duration": extract_duration(plan),
    "validation_tiers": extract_validation_tiers(plan),
    "mcp_requirements": extract_mcps(plan),
    "domain_distribution": extract_domains(plan)
}
```

**3. Review critically**:
- Identify any questions or concerns about the plan
- Check if Shannon metadata is present
- Verify validation gates are specified
- Confirm MCP requirements are available

**4. If concerns**: Raise them with your human partner before starting

**5. If no concerns**: Create TodoWrite and proceed

**Shannon tracking**: Save plan review to Serena:
```python
serena.write_memory(f"execution/{execution_id}/review", {
    "plan_id": plan_id,
    "metadata": metadata,
    "concerns": [],
    "ready_to_execute": True,
    "timestamp": ISO_timestamp
})
```

### Step 2: Calculate Batch Size (Shannon Enhancement)

**Complexity-based batch sizing**:

```python
def calculate_batch_size(plan_complexity: float) -> int:
    """
    Shannon formula: More complex = smaller batches
    
    complexity=0.1 → batch=5 (simple, can do many)
    complexity=0.5 → batch=3 (moderate, typical)
    complexity=0.9 → batch=1 (complex, one at a time)
    """
    base_size = max(1, min(5, int(10 * (1 - plan_complexity))))
    return base_size

# Example:
plan_complexity = 0.62  # From plan header
batch_size = calculate_batch_size(0.62)  # = 2 tasks per batch
```

**Report to user**:
```
Shannon batch sizing: Complexity 0.62 → 2 tasks per batch
Total batches: 9 (18 tasks / 2 per batch)
```

### Step 3: Execute Batch

**For each task in batch**:

**Mark as in_progress**:
```python
todo_write(task_id, status="in_progress")
```

**Follow each step exactly** (plan has bite-sized steps):
- Step 1: Write failing test (TDD RED)
- Step 2: Verify test fails
- Step 3: Implement minimal code (TDD GREEN)
- Step 4: Verify test passes
- Step 5: Run validation gates
- Step 6: Commit

**Shannon enhancement**: Track metrics per task:
```python
task_metrics = {
    "task_id": task_id,
    "start_time": start_time,
    "end_time": end_time,
    "duration_minutes": duration,
    "validation_results": {
        "tier1": {"pass": True, "errors": 0},
        "tier2": {"pass": True, "tests": "12/12"},
        "tier3": {"pass": True, "no_mocks": True}
    },
    "files_changed": 3,
    "lines_added": 45,
    "commits": 1
}

serena.write_memory(f"execution/{execution_id}/task_{task_id}", task_metrics)
```

**Run verifications as specified**:

**Tier 1 (Flow)**:
```bash
tsc --noEmit
ruff check .
```

**Tier 2 (Artifacts)**:
```bash
npm test
npm run build
```

**Tier 3 (Functional - NO MOCKS)**:
```bash
npm run test:e2e
# VERIFY: Tests use real systems (Puppeteer, real DB, etc.)
```

**Shannon requirement**: All tiers must pass before marking task complete.

**Mark as completed**:
```python
todo_write(task_id, status="completed")
```

### Step 4: Report (Shannon Quantitative Style)

When batch complete:

```markdown
## Batch N Complete

**Shannon Metrics**:
- Tasks completed: 2/2
- Batch complexity: 0.58 (avg of task complexities)
- Duration: 45 minutes (estimated: 40 min, variance: +12%)
- Validation: 3/3 tiers PASS

**Tier 1 (Flow)**: ✅ PASS
- TypeScript: 0 errors
- Linter: 0 errors

**Tier 2 (Artifacts)**: ✅ PASS
- Tests: 24/24 pass (12 new tests added)
- Build: exit 0

**Tier 3 (Functional)**: ✅ PASS
- E2E tests: 6/6 pass
- NO MOCKS verified: ✅ (using Puppeteer + real database)

**Files Changed**:
- src/auth/middleware.ts (+67 lines)
- src/auth/validation.ts (+34 lines)
- tests/auth/middleware.test.ts (+89 lines)

**Commits**: 2
- feat: add auth middleware validation
- test: add middleware integration tests

**Ready for feedback.**
```

**Shannon tracking**: Save batch metrics:
```python
batch_metrics = {
    "batch_id": batch_id,
    "tasks": [task_ids],
    "complexity": 0.58,
    "duration_minutes": 45,
    "estimated_minutes": 40,
    "variance_percent": 12.5,
    "validation_results": {tier_results},
    "files_changed": 3,
    "lines_added": 190,
    "commits": 2,
    "success": True
}

serena.write_memory(f"execution/{execution_id}/batch_{batch_id}", batch_metrics)
```

### Step 5: Continue

Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat Steps 3-4 until complete

**Shannon enhancement**: Learn from feedback:
```python
if feedback_requires_changes:
    # Track what type of feedback
    serena.write_memory(f"execution/{execution_id}/feedback_{batch_id}", {
        "feedback_type": "missing_validation" / "logic_error" / "style",
        "tasks_affected": [task_ids],
        "time_to_fix": 15  # minutes
    })
```

### Step 6: Complete Development

After all tasks complete and verified:

**Shannon final verification**:

```markdown
## Execution Complete - Shannon Verification

**Overall Metrics**:
- Total tasks: 18/18 ✅
- Total batches: 9
- Total duration: 7.5 hours (estimated: 8-10h, -12.5% under estimate)
- Avg batch duration: 50 minutes

**Validation Summary**:
- Tier 1: 18/18 tasks PASS
- Tier 2: 18/18 tasks PASS  
- Tier 3: 18/18 tasks PASS
- NO MOCKS: ✅ Verified (all tests use real systems)

**Code Metrics**:
- Files created: 12
- Files modified: 8
- Lines added: 1,247
- Lines removed: 34
- Commits: 18

**Complexity vs Actual**:
- Planned complexity: 0.62
- Actual complexity: 0.59 (simpler than expected)

**Risk Mitigation**:
- HIGH risks: Resolved (security patterns verified)
- MEDIUM risks: Resolved (session management tested)
- LOW risks: No issues

**MCP Usage**:
- puppeteer: 18 tasks (E2E testing)
- sequential: 3 tasks (security analysis)

**Ready for integration testing and deployment.**
```

**Integration with other skills**:
- **REQUIRED SUB-SKILL**: Use shannon:verification-before-completion
- Verify ALL tests pass
- Run complete validation suite
- Present deployment options

## When to Stop and Ask for Help

**STOP executing immediately when**:
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly
- Batch exceeds estimated time by >50%

**Ask for clarification rather than guessing.**

**Shannon tracking**: Record blockers:
```python
blocker = {
    "type": "missing_dependency" / "test_failure" / "unclear_instruction",
    "task_id": task_id,
    "batch_id": batch_id,
    "description": "...",
    "time_spent_before_blocker": 25,  # minutes
    "resolution": "awaiting_feedback"
}

serena.write_memory(f"execution/{execution_id}/blocker_{blocker_id}", blocker)
```

## When to Revisit Earlier Steps

**Return to Review (Step 1) when**:
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking
- Discover plan is missing critical Shannon metadata

**Don't force through blockers** - stop and ask.

## Shannon Enhancement: Wave Orchestration

**For tasks that can run in parallel**:

If plan indicates tasks are independent:

```python
# Detect parallelizable tasks
parallel_tasks = find_independent_tasks(current_batch)

if len(parallel_tasks) > 1:
    # Use wave orchestration
    wave_result = execute_wave(parallel_tasks)
    # Still validate each task's results
```

**Integration with wave-orchestration skill**:
- Batch can contain sequential OR parallel execution
- Shannon's wave orchestration handles parallelization
- Each task still gets individual validation

## Shannon Pattern Learning

**After execution completes**:

```python
# Query similar executions
similar = serena.query_memory("execution/*/metadata:complexity~0.6")

# Learn patterns
patterns = {
    "avg_duration_for_complexity_0.6": average([e["duration"] for e in similar]),
    "common_blockers": most_common([b for e in similar for b in e["blockers"]]),
    "avg_variance": average([e["variance_percent"] for e in similar]),
    "recommendations": [
        "Complexity 0.6: Plan for 8 hours, batch size 2-3",
        "Common blocker: Missing test database - prepare in advance"
    ]
}

serena.write_memory(f"patterns/execution/complexity_0.6", patterns)
```

**Use patterns for future estimates**:
- More accurate time estimates
- Better batch sizing
- Proactive blocker prevention

## Remember

- Review plan critically first
- Calculate batch size based on complexity (Shannon formula)
- Follow plan steps exactly
- Run validation gates per task (Shannon 3-tier)
- Don't skip verifications
- Verify NO MOCKS compliance
- Reference skills when plan says to
- Between batches: quantitative report and wait
- Stop when blocked, don't guess
- Track everything in Serena for pattern learning

## Integration with Other Skills

**This skill requires**:
- **writing-plans** - Plan created by this skill
- **forced-reading-protocol** - If plan >3000 lines
- **test-driven-development** - For TDD steps
- **verification-before-completion** - Before claiming batch complete

**This skill may use**:
- **wave-orchestration** - For parallel task execution
- **systematic-debugging** - If tasks encounter bugs
- **defense-in-depth** - When adding validation layers

**Shannon integration**:
- **Serena MCP** - Track all execution metrics
- **Sequential MCP** - Deep analysis for complex decisions
- **MCP requirements** - Use MCPs specified in plan

## The Bottom Line

**Systematic execution + Shannon quantitative validation = reliable delivery.**

Not "tasks completed" - "18/18 tasks complete, 3/3 validation tiers PASS, complexity 0.59, 7.5 hours (-12% under estimate), NO MOCKS verified".

Measure everything. Learn from patterns. Never skip validation.

