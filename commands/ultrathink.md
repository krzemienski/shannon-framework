name: shannon:ultrathink
description: Deep debugging with sequential thinking, systematic debugging, and forced reading
usage: /shannon:ultrathink "problem description" [--thoughts N] [--verify]
tags: [debugging, parity, testing, root-cause]
version: "5.4.0"
delegates_to:
  - systematic-debugging
  - root-cause-analysis
  - forced-reading-sentinel
---

# Shannon UltraThink: Deep Debugging Command

## Overview

**Ultra-deep debugging** for hard problems, complex bugs, and root cause analysis. Combines sequential thinking MCP (150+ thoughts), systematic debugging protocol, forced complete reading, and root cause tracing to solve problems other approaches miss.

**When Standard Debugging Fails**: Use /shannon:ultrathink

> Automatically activates `skills/systematic-debugging`, `skills/root-cause-analysis`, and `skills/forced-reading-sentinel`. Refer to those skills for checklists and response patterns.

## Prerequisites

**MANDATORY**:
- Sequential Thinking MCP (REQUIRED - command fails without it)

**RECOMMENDED**:
- Serena MCP (for saving analysis results)
- Project context available

## Workflow

### Step 1: Validate Prerequisites

Check that Sequential Thinking MCP is available:

```
IF sequential_thinking_mcp NOT available THEN
  ERROR: "Sequential Thinking MCP is REQUIRED for /shannon:ultrathink"
  MESSAGE: "Install: See /shannon:check_mcps for setup instructions"
  EXIT
END IF
```

### Step 2: Parse Problem Description

Extract problem context from user input:

- **Problem statement**: User's description
- **Thought count**: From --thoughts flag (default: 150)
- **Verification**: From --verify flag (default: false)
- **Context files**: Auto-detect or user-provided

### Step 3: Forced Complete Reading

**BEFORE any analysis**, enforce complete reading of all relevant files:

```
FOR each relevant_file IN context:
  1. Count total lines: line_count = count_lines(relevant_file)
  2. Display intention: "Reading {relevant_file} ({line_count} lines)"
  3. Read COMPLETELY: read_file(relevant_file) # No offset/limit
  4. Verify completeness: assert read_lines == line_count
  5. Only THEN proceed to analysis
END FOR
```

**No shortcuts**: Every file read completely before any reasoning.

### Step 4: Invoke Sequential Thinking MCP

Use Sequential Thinking MCP for deep analysis:

**Invocation**:
```
@mcp sequential-thinking
Prompt: "Deep analysis of problem: {problem_description}"
Minimum Thoughts: {thought_count} (default: 150)
Analysis Mode: "systematic_debugging"
```

**Thought Process**:
```
Thoughts 1-30: Problem Understanding
  - Parse error messages
  - Identify symptoms vs root cause
  - List known facts vs assumptions
  - Trace execution flow
  
Thoughts 31-80: Hypothesis Generation
  - Generate possible root causes
  - Evaluate each hypothesis against facts
  - Eliminate impossible causes
  - Rank remaining hypotheses by likelihood
  
Thoughts 81-120: Systematic Investigation
  - Test top hypothesis
  - Gather evidence (logs, state, traces)
  - Invalidate or confirm
  - Repeat for next hypothesis
  
Thoughts 121-150: Solution Design
  - Design fix for confirmed root cause
  - Consider edge cases
  - Plan verification approach
  - Estimate implementation effort
```

### Step 5: Apply Systematic Debugging Protocol

Use systematic debugging patterns:

**Protocol Steps**:
1. **Reproduce Reliably**: Can you make it happen on demand?
2. **Minimize Reproduction**: What's the smallest case that triggers it?
3. **Isolate Variables**: Change one thing at a time
4. **Binary Search**: Divide and conquer the problem space
5. **State Inspection**: What's the actual state vs expected state?
6. **Timeline Analysis**: When did this start working incorrectly?
7. **Dependency Check**: What changed recently?

**Output**: Structured debugging analysis

### Step 6: Root Cause Tracing

Trace from symptom to root cause:

```
symptom → immediate_cause → deeper_cause → root_cause

Example:
  symptom: "Payment fails intermittently"
  immediate_cause: "Database timeout on payment table"
  deeper_cause: "Lock contention from concurrent updates"
  root_cause: "Missing transaction isolation level configuration"
```

**Output**: Complete causal chain

### Step 7: Solution Generation

Generate solution with verification plan:

```
Solution:
  - Root Cause: {identified_root_cause}
  - Fix Description: {what_to_change}
  - Implementation: {code_changes}
  - Why This Works: {explanation}
  
Verification Plan:
  - Test Case 1: {test_that_reproduces_bug}
  - Expected Before Fix: {fails_with_X_error}
  - Expected After Fix: {succeeds_with_Y_result}
  - Edge Cases: {list_of_edge_cases_to_verify}
```

### Step 8: Auto-Verification (if --verify flag)

If --verify flag provided, automatically test the solution:

**Verification Steps**:
1. Create test that reproduces the bug
2. Run test (should fail before fix)
3. Apply the fix
4. Run test (should pass after fix)
5. Run edge case tests
6. Report results

**Output**: Verification results with pass/fail status

### Step 9: Save to Serena

Save analysis for future reference:

```
Use Serena MCP:
write_memory("shannon_ultrathink_{timestamp}", {
  problem: "{problem_description}",
  thoughts_count: {thought_count},
  root_cause: "{identified_root_cause}",
  solution: "{solution_description}",
  verification_status: "{verified|not_verified}",
  files_analyzed: [list_of_files],
  timestamp: "{ISO_timestamp}"
})
```

### Step 10: Present Results

Format comprehensive analysis report:

```markdown
🧠 SHANNON ULTRATHINK ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**PROBLEM**: {problem_description}

**ANALYSIS DEPTH**: {thought_count} sequential thoughts
**DURATION**: {minutes} minutes
**FILES ANALYZED**: {file_count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ROOT CAUSE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**SYMPTOM**: {observed_symptom}
**IMMEDIATE CAUSE**: {immediate_cause}
**DEEPER CAUSE**: {deeper_cause}
**ROOT CAUSE**: {root_cause}

Causal Chain:
{symptom} ← {cause_1} ← {cause_2} ← {root_cause}

Evidence:
{for each piece of evidence}
✓ {evidence_description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEMATIC DEBUGGING RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Reproducibility**: {reliable|intermittent|irreproducible}
**Minimal Reproduction**: {minimal_case}
**Variables Isolated**: {isolated_variables}
**State Inspection**: {actual_state} vs {expected_state}

Key Findings:
{for each finding}
├─ {finding_description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOLUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Fix Description**: {what_to_change}

**Implementation**:
```{language}
{code_changes}
```

**Why This Works**: {explanation}

**Impact**: {impact_description}
**Effort**: {effort_estimate}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFICATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test Case**: {test_description}

Before Fix (Expected):
  Status: FAIL
  Error: {expected_error}

After Fix (Expected):
  Status: PASS
  Result: {expected_result}

Edge Cases to Verify:
{for each edge_case}
├─ {edge_case_description}

{if --verify flag}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTO-VERIFICATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Before Fix**: {test_failed_as_expected}
**After Fix**: {test_passed_as_expected}
**Edge Cases**: {edge_cases_passed} / {total_edge_cases}

{if all_tests_passed}
✅ SOLUTION VERIFIED
{else}
⚠️  VERIFICATION INCOMPLETE
   Failed: {failed_test_list}
{end if}
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if saved_to_serena}
💾 Analysis saved to Serena MCP
Key: shannon_ultrathink_{timestamp}
Restore: /shannon:restore {timestamp}
{else}
⚠️  Analysis not saved (Serena MCP unavailable)
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if --verify AND all_passed}
1. Review solution implementation
2. Apply fix to codebase
3. Run full test suite
4. Deploy to staging for final validation

{else if --verify AND some_failed}
1. Investigate failed test cases
2. Refine solution
3. Re-run verification: /shannon:ultrathink "{problem}" --verify

{else} # No --verify flag
1. Review verification plan
2. Implement test case
3. Run verification: /shannon:ultrathink "{problem}" --verify
4. Apply fix after verification passes

{end if}
```

---

## Command Flags

### --thoughts N
Minimum number of sequential thoughts (default: 150)

**Usage**:
```bash
/shannon:ultrathink "Complex race condition" --thoughts 200
```

**Guidelines**:
- **Simple bugs**: 100-150 thoughts
- **Moderate complexity**: 150-250 thoughts
- **Complex issues**: 250-500 thoughts
- **Critical bugs**: 500+ thoughts

### --verify
Auto-verify solution after generation

**Usage**:
```bash
/shannon:ultrathink "Payment processing fails intermittently" --verify
```

**Behavior**:
- Generates solution as normal
- Automatically creates test case
- Runs test before fix (should fail)
- Applies fix
- Runs test after fix (should pass)
- Reports verification results

---

## Usage Examples

### Example 1: Intermittent Bug

```bash
/shannon:ultrathink "Payment processing fails 1 in 10 times with no error logs" --thoughts 200

# Result:
# - 200 sequential thoughts analyzing the problem
# - Forced reading of payment processing code
# - Systematic debugging protocol applied
# - Root cause: Race condition in transaction handling
# - Solution: Add transaction isolation level
# - Verification plan: Concurrent payment test
```

### Example 2: Performance Issue

```bash
/shannon:ultrathink "API response time degrades after 1000 requests" --verify

# Result:
# - 150 thoughts analyzing performance
# - Root cause: Connection pool exhaustion
# - Solution: Increase pool size + add connection recycling
# - Auto-verification: Load test shows improvement
```

### Example 3: Complex Logic Bug

```bash
/shannon:ultrathink "Calculation produces wrong result for specific input combinations" --thoughts 300

# Result:
# - 300 thoughts tracing calculation logic
# - Root cause: Integer overflow in edge case
# - Solution: Use BigInt for intermediate calculations
# - Verification plan: Test edge cases
```

---

## When to Use UltraThink

**Use /shannon:ultrathink when**:
- Standard debugging hasn't found root cause
- Bug is intermittent or hard to reproduce
- Problem involves complex interactions
- Need systematic analysis
- Root cause unclear
- Multiple possible causes
- Critical production bug
- Time-sensitive debugging needed

**Don't use UltraThink when**:
- Simple syntax errors (use linter)
- Obvious bugs (standard debugging is faster)
- Need quick fix (UltraThink is thorough, not fast)
- Sequential Thinking MCP unavailable

---

## Integration with Shannon Framework

**UltraThink complements other commands**:

```bash
# 1. Project analysis finds complexity hotspot
/shannon:analyze --deep

# 2. Hotspot has intermittent bug
/shannon:ultrathink "Concurrency issue in user service" --thoughts 250 --verify

# 3. Solution implemented and verified
/shannon:reflect  # Validate fix completeness

# 4. Save checkpoint
/shannon:checkpoint "bug-fixed"
```

---

## MCP Dependencies

**REQUIRED**:
- **Sequential Thinking MCP**: Deep thought analysis (100+ thoughts)

**RECOMMENDED**:
- **Serena MCP**: Save analysis results
- **Context7 MCP**: Library documentation if bug involves external dependencies

**OPTIONAL**:
- **Puppeteer MCP**: If bug involves UI/browser behavior
- **Tavily MCP**: Research similar bugs/solutions

---

## Success Criteria

UltraThink succeeds when:
- ✅ Root cause identified (not just symptom)
- ✅ Complete causal chain traced
- ✅ Solution addresses root cause
- ✅ Verification plan created
- ✅ (If --verify) Solution verified with tests
- ✅ Analysis depth proportional to problem complexity
- ✅ All relevant files read completely (forced reading)
- ✅ Systematic debugging protocol applied

---

## Anti-Rationalization

Common mistakes to avoid:

| ❌ Rationalization | ✅ Reality |
|-------------------|-----------|
| "150 thoughts is overkill" | Hard bugs need deep analysis - shortcuts miss root cause |
| "I can skip reading file X" | Forced reading prevents assumptions - read ALL relevant files |
| "This is obviously a Y problem" | Obvious diagnoses are often wrong - follow systematic protocol |
| "Verification can wait" | Use --verify to catch wrong solutions before implementing |
| "Sequential MCP is optional" | UltraThink REQUIRES Sequential MCP - it's the core capability |

---

## Performance

**Typical UltraThink Times**:
- Simple bug (150 thoughts): 3-5 minutes
- Moderate bug (200 thoughts): 5-8 minutes
- Complex bug (300 thoughts): 8-12 minutes
- Critical bug (500 thoughts): 15-20 minutes

**Value Proposition**: 
- 10 minutes of UltraThink analysis vs 2 hours of manual debugging
- Higher accuracy (root cause vs symptom fixes)
- Verified solutions (with --verify flag)

---

## Notes

- **V5 NEW**: First Shannon command requiring specific MCP
- **Philosophy**: Solve hard problems correctly, not quickly
- **Forced Reading**: EVERY file read completely before analysis
- **Sequential Thinking**: 150+ thoughts minimum (vs 50 standard)
- **Systematic Protocol**: Structured debugging approach prevents missed causes
- **Auto-Verification**: --verify flag tests solution before implementation

---

## Related Commands

**Before /shannon:ultrathink**:
- `/shannon:analyze` - Identify complexity hotspots
- `/shannon:status` - Check Sequential MCP availability

**During /shannon:ultrathink**:
- (Automatic: forced reading, sequential thinking, systematic debugging)

**After /shannon:ultrathink**:
- `/shannon:reflect` - Validate solution completeness
- `/shannon:test` - Create functional tests for fix
- `/shannon:checkpoint` - Save analysis results

---

**Version**: 5.0.0 (NEW in V5)
**Status**: Core debugging command
**MCP Requirement**: Sequential Thinking (MANDATORY)

