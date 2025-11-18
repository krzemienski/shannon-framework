---
name: shannon:reflect
description: Honest gap analysis before claiming work complete - prevents premature completion
usage: /shannon:reflect [--scope plan|project|session] [--min-thoughts 100]
---

# Honest Reflection Command

## Overview

Invokes the honest-reflections skill to perform systematic gap analysis using 100+ sequential thoughts. Prevents premature completion claims by revealing discrepancies between claimed and actual delivery.

**When to Use**: BEFORE any "work complete" claim

## Prerequisites

- Sequential MCP recommended (for 100+ thought systematic analysis)
- Serena MCP recommended (for storing reflection results)
- Original plan/specification document

## Workflow

### Step 1: Invoke honest-reflections Skill

```
@skill honest-reflections
- Input:
  * scope: "plan"|"project"|"session" (default: session)
  * min_thoughts: 100 (or user-specified)
  * plan_file: path to original plan (auto-detect or specify)
- Output: reflection_result
```

The honest-reflections skill will:
1. Read original plan completely
2. Inventory delivered work (commits, files, lines)
3. Compare plan vs delivery task-by-task
4. Run 100+ sequential thoughts for gap identification
5. Calculate honest completion percentage
6. Detect rationalization patterns
7. Present options (complete remaining, fix critical, accept as-is)

### Step 2: Present Reflection Results

```markdown
🔍 Honest Reflection Complete

**Analysis**: [min_thoughts]+ sequential thoughts
**Duration**: [minutes]

## Completion Assessment

**Claimed**: [from commits/docs]
**Actual**: [calculated percentage]%
**Discrepancy**: [gap] percentage points
**Status**: [HONEST / OVERCLAIMED / UNDERCLAIMED]

## Gaps Found: [total count]

[Detailed gap listing]

## Options

**A**: Complete remaining work ([hours]h)
**B**: Fix critical gaps only ([hours]h)
**C**: Accept with honest disclosure

**Recommendation**: [skill's recommendation]
```

## Command Flags

**--scope plan**: Analyze against original project plan
**--scope project**: Analyze against project requirements
**--scope session**: Analyze current work session only

**--min-thoughts N**: Require minimum N sequential thoughts (default: 100)

## Example Usage

```bash
# Before declaring phase complete
/shannon:reflect

# Deep reflection with 150 thoughts
/shannon:reflect --min-thoughts 150

# Analyze against specific plan
/shannon:reflect --scope plan docs/plans/enhancement-plan.md
```

## Integration

- **Before git commit "complete"**: Run /shannon:reflect
- **After major phase**: Run /shannon:reflect
- **Weekly on long projects**: Run /shannon:reflect

## Skill Dependencies

- honest-reflections (REQUIRED)

## MCP Dependencies

- Sequential MCP (recommended for systematic 100+ thought analysis)
- Serena MCP (recommended for saving reflection results)
