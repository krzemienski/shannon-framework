---
name: shannon:execute-plan
description: |
  Execute implementation plan in batches with Shannon validation gates and review checkpoints.
  Loads plan with quantitative analysis, calculates complexity-based batch sizing, executes
  tasks with 3-tier validation, tracks metrics in Serena, reports progress quantitatively.

usage: |
  /shannon:execute-plan <plan_file>
  /shannon:execute-plan --latest
  /shannon:execute-plan <plan_file> --batch-size 3

examples:
  - /shannon:execute-plan docs/plans/2025-11-18-auth-system.md
  - /shannon:execute-plan --latest
  - /shannon:execute-plan plan.md --batch-size 2

delegates_to:
  - executing-plans

version: "5.4.0"
---

# /shannon:execute-plan - Execute Implementation Plan

## Purpose

Systematic execution of implementation plans with Shannon's quantitative validation:
- ✅ Complexity-based batch sizing
- ✅ 3-tier validation gates per task
- ✅ NO MOCKS enforcement
- ✅ Quantitative progress tracking
- ✅ Review checkpoints between batches
- ✅ Pattern learning via Serena

**Philosophy**: Systematic execution + quantitative validation = reliable delivery.

---

## Workflow

### Step 1: Invoke executing-plans Skill

The command delegates all execution logic to the executing-plans skill:

```
Invoke sub-skill:
@skill executing-plans

Plan File: {plan_file_path}
```

The skill handles:
- Plan loading and validation
- Shannon metadata extraction
- Complexity-based batch calculation
- Task execution with TDD
- Validation gate enforcement
- Progress tracking
- Serena persistence

### Step 2: Report Progress

After each batch, display Shannon quantitative report:

```markdown
## Batch 3/9 Complete

**Shannon Metrics**:
- Tasks: 2/2 ✅
- Complexity: 0.58 (avg)
- Duration: 45 min (est: 40 min, +12%)
- Validation: 3/3 tiers PASS

**Tier 1 (Flow)**: ✅
- TypeScript: 0 errors
- Linter: 0 errors

**Tier 2 (Artifacts)**: ✅
- Tests: 24/24 pass (+12 new)
- Build: exit 0

**Tier 3 (Functional)**: ✅
- E2E: 6/6 pass
- NO MOCKS: ✅ (Puppeteer + real DB)

**Files Changed**: 3 (+190 lines)
**Commits**: 2

**Progress**: 33% complete (6/18 tasks)

**Ready for feedback.**
```

### Step 3: Final Report

After all batches complete:

```markdown
✅ Execution Complete - Shannon Verification

**Overall Metrics**:
- Tasks: 18/18 ✅
- Batches: 9
- Duration: 7.5 hours (est: 8-10h, -12.5%)
- Avg batch: 50 min

**Validation Summary**:
- Tier 1: 18/18 PASS
- Tier 2: 18/18 PASS
- Tier 3: 18/18 PASS
- NO MOCKS: ✅ Verified

**Code Metrics**:
- Files created: 12
- Files modified: 8
- Lines added: 1,247
- Commits: 18

**Complexity**: 0.59 actual (0.62 planned, simpler than expected)

**Saved to Serena**: execution/{execution_id}

**Ready for integration testing and deployment.**
```

---

## Parameters

**<plan_file>**: Path to plan file (required unless --latest)  
**--latest**: Use most recent plan from docs/plans/  
**--batch-size**: Override complexity-based batch sizing  
**--auto**: Skip review checkpoints (run all batches)  
**--tier**: Validation tier level (1-3, default: 3)

---

## Integration with Shannon CLI

```python
# Shannon CLI code
async for message in sdk_client.query(
    prompt="/shannon:execute-plan docs/plans/feature.md",
    options=ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "{shannon_framework_path}"}],
        setting_sources=["user", "project"]
    )
):
    # Command executes executing-plans skill
    # Returns quantitative progress updates
```

---

## Examples

### Systematic Execution with Review

```bash
/shannon:execute-plan docs/plans/2025-11-18-auth-system.md

# Executes with:
# - Complexity-based batching (plan complexity: 0.62 → batch size: 2)
# - Review checkpoints after each batch
# - Full 3-tier validation
# - Quantitative progress reports
```

### Automatic Execution

```bash
/shannon:execute-plan docs/plans/simple-feature.md --auto

# Executes all batches without review checkpoints
# Still runs all validation gates
# Still tracks metrics in Serena
```

### Latest Plan

```bash
/shannon:execute-plan --latest

# Finds most recent plan in docs/plans/
# Executes with standard workflow
```

---

## Integration with Other Commands

**Requires**:
- **/shannon:write-plan** - Creates the plan to execute

**Uses during execution**:
- **/shannon:do** - Can delegate individual tasks if needed
- Validation gates (automatic)
- Serena tracking (automatic)

**Leads to**:
- Integration testing
- Deployment
- Production release

---

**Status**: Command complete, delegates to executing-plans skill

