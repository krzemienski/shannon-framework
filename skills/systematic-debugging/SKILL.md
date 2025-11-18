---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation with quantitative tracking, pattern analysis, hypothesis testing, implementation) that ensures understanding before attempting solutions
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle**: ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when**:
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when**:
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix**:

#### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

#### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Shannon tracking**: Record reproduction steps in Serena:
```python
serena.write_memory(f"debugging/{bug_id}/reproduction", {
    "steps": ["Step 1", "Step 2", "Step 3"],
    "reproducible": True/False,
    "frequency": "100%" / "50%" / "intermittent",
    "timestamp": ISO_timestamp
})
```

#### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes
- Environmental differences

**Shannon integration**: Use git log with metrics:
```bash
git log --since="1 week ago" --oneline --stat
# Track: files_changed, lines_added, complexity_diff
```

#### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components** (CI → build → signing, API → service → database):

**BEFORE proposing fixes, add diagnostic instrumentation**:
```
For EACH component boundary:
  - Log what data enters component
  - Log what data exits component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify failing component
THEN investigate that specific component
```

**Example (multi-layer system)**:
```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3: Signing script
echo "=== Keychain state: ==="
security list-keychains
security find-identity -v

# Layer 4: Actual signing
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

**This reveals**: Which layer fails (secrets → workflow ✓, workflow → build ✗)

**Shannon tracking**: Save diagnostic results:
```python
serena.write_memory(f"debugging/{bug_id}/diagnostics", {
    "layer_results": {
        "layer1": {"status": "PASS", "evidence": "..."},
        "layer2": {"status": "FAIL", "evidence": "..."},
    },
    "failing_layer": "layer2",
    "timestamp": ISO_timestamp
})
```

#### 5. Trace Data Flow

**WHEN error is deep in call stack**:

**REQUIRED SUB-SKILL**: Use shannon:root-cause-tracing for backward tracing technique

**Quick version**:
- Where does bad value originate?
- What called this with bad value?
- Keep tracing up until you find the source
- Fix at source, not at symptom

**Shannon enhancement**: Quantitative trace tracking:
```python
serena.write_memory(f"debugging/{bug_id}/trace", {
    "trace_depth": 5,  # How many layers traced
    "root_cause_layer": "user_input_validation",
    "trace_path": ["handler", "service", "validator", "input", "user"],
    "time_to_trace": "15 minutes",
    "timestamp": ISO_timestamp
})
```

### Phase 2: Pattern Analysis

**Find the pattern before fixing**:

#### 1. Find Working Examples

- Locate similar working code in same codebase
- What works that's similar to what's broken?

**Shannon integration**: Use codebase_search:
```python
# Find working examples automatically
working_examples = codebase_search(
    query="working implementation of authentication",
    target_directories=["src/"]
)
```

#### 2. Compare Against References

- If implementing pattern, read reference implementation COMPLETELY
- Don't skim - read every line (use forced-reading-protocol skill)
- Understand the pattern fully before applying

**Shannon requirement**: Must use forced-reading-protocol for reference docs

#### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

**Shannon tracking**: Quantify differences:
```python
differences = {
    "config_differences": 3,
    "code_differences": 7,
    "dependency_differences": 2,
    "total_diff_lines": 45
}
```

#### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

**Shannon integration**: Use mcp-discovery skill to find relevant MCPs:
```python
# Need database debugging? Find db MCPs
relevant_mcps = mcp_discovery.find_for_domain("database debugging")
```

### Phase 3: Hypothesis and Testing

**Scientific method**:

#### 1. Form Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

**Shannon requirement**: Quantify confidence:
```python
hypothesis = {
    "theory": "Missing environment variable causes auth failure",
    "reasoning": "Layer 2 diagnostics show IDENTITY unset",
    "confidence": 0.85,  # 85% confidence (0.00-1.00)
    "evidence_strength": "STRONG",  # Based on diagnostic evidence
    "timestamp": ISO_timestamp
}

serena.write_memory(f"debugging/{bug_id}/hypothesis", hypothesis)
```

#### 2. Test Minimally

- Make the SMALLEST possible change to test hypothesis
- One variable at a time
- Don't fix multiple things at once

**Shannon tracking**: Record test result:
```python
test_result = {
    "hypothesis_id": hypothesis_id,
    "change_made": "Set IDENTITY env var in workflow",
    "outcome": "SUCCESS" / "FAILURE",
    "confidence_update": 0.95 if success else 0.10,
    "timestamp": ISO_timestamp
}
```

#### 3. Verify Before Continuing

- Did it work? Yes → Phase 4
- Didn't work? Form NEW hypothesis
- DON'T add more fixes on top

**Shannon enhancement**: Track attempt count:
```python
attempts = get_attempt_count(bug_id)  # From Serena

if attempts >= 3:
    # CRITICAL: Question architecture (see Phase 4.5 below)
    alert_architectural_smell(bug_id)
```

#### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask for help
- Research more

**Shannon integration**: Use research MCPs:
```python
# Use Tavily for best practices
research = tavily.search("best practices for X")

# Use Context7 for library docs
docs = context7.get_library_docs("library/name")

# Save research to Serena
serena.write_memory(f"debugging/{bug_id}/research", research)
```

### Phase 4: Implementation

**Fix the root cause, not the symptom**:

#### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- One-off test script if no framework
- MUST have before fixing
- **REQUIRED SUB-SKILL**: Use shannon:test-driven-development for proper failing tests (with REAL systems, NO MOCKS)

**Shannon requirement**: Test must use real systems:
```typescript
// ✅ GOOD: Real system test
test('auth fails with missing env var', async () => {
  // DON'T mock - use real auth system
  const result = await realAuthSystem.authenticate(credentials);
  expect(result.error).toBe('Missing IDENTITY');
});

// ❌ BAD: Mocked test
test('auth fails', () => {
  const mock = jest.fn().mockRejection('error');
  // This doesn't prove real system behavior
});
```

#### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

**Shannon tracking**: Record fix details:
```python
fix = {
    "root_cause": "Missing IDENTITY env var",
    "fix_applied": "Added IDENTITY to workflow secrets",
    "files_changed": 1,
    "lines_changed": 3,
    "fix_type": "configuration",
    "timestamp": ISO_timestamp
}
```

#### 3. Verify Fix

- Test passes now?
- No other tests broken?
- Issue actually resolved?

**Shannon requirement**: Use verification-before-completion skill:
```
MANDATORY: Run all 3 validation tiers
- Tier 1 (Flow): Code compiles
- Tier 2 (Artifacts): Tests pass
- Tier 3 (Functional): Real system verification

NO claims without verification evidence.
```

#### 4. If Fix Doesn't Work

**STOP**

Count: How many fixes have you tried?

**If < 3**: Return to Phase 1, re-analyze with new information

**If ≥ 3**: STOP and question the architecture (step 5 below)

DON'T attempt Fix #4 without architectural discussion

#### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating architectural problem**:
- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**Shannon tracking**: Architectural smell detection:
```python
debugging_history = serena.query_memory(f"debugging/{bug_id}/*")

attempts = len([h for h in debugging_history if h["type"] == "fix_attempt"])

if attempts >= 3:
    pattern = analyze_failure_pattern(debugging_history)

    architectural_smell = {
        "attempts": attempts,
        "pattern": pattern,  # "each_fix_reveals_new_problem" etc
        "recommendation": "REFACTOR_ARCHITECTURE",
        "confidence": 0.95,
        "timestamp": ISO_timestamp
    }

    serena.write_memory(f"debugging/{bug_id}/architectural_smell", architectural_smell)
```

**STOP and question fundamentals**:
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

**Discuss with your human partner before attempting more fixes**

This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean**: STOP. Return to Phase 1.

**If 3+ fixes failed**: Question the architecture (see Phase 4.5)

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections**:
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultrathink this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

**When you see these**: STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Shannon Enhancement: Quantitative Metrics

**Track debugging metrics in Serena**:

```python
debugging_session = {
    "bug_id": bug_id,
    "start_time": start_timestamp,
    "end_time": end_timestamp,
    "duration_minutes": 45,

    # Phase completion
    "phases_completed": ["investigation", "analysis", "hypothesis", "implementation"],

    # Quantitative metrics
    "reproduction_attempts": 3,
    "reproduction_success": True,
    "trace_depth": 5,
    "hypotheses_tested": 2,
    "fix_attempts": 1,
    "success": True,

    # Pattern recognition
    "similar_bugs_resolved": 3,  # From Serena history
    "root_cause_category": "configuration",
    "architectural_smell": False,

    # Evidence quality
    "diagnostic_evidence_strength": "STRONG",
    "hypothesis_confidence": 0.95,
    "fix_verification": "3/3 tiers PASS",

    "timestamp": ISO_timestamp
}

serena.write_memory(f"debugging/sessions/{session_id}", debugging_session)
```

**Pattern learning over time**:
```python
# Query historical debugging data
auth_bugs = serena.query_memory("debugging/*/root_cause_category:auth")

# Learn patterns
pattern = {
    "category": "authentication",
    "total_bugs": len(auth_bugs),
    "avg_resolution_time": average([b["duration_minutes"] for b in auth_bugs]),
    "common_root_causes": {
        "missing_env_vars": 12,  # 80% of auth bugs
        "expired_tokens": 2,
        "config_mismatch": 1
    },
    "architectural_refactors_triggered": 0,  # No refactors yet
    "recommendation": "Add env var validation at startup"
}
```

## Quick Reference

| Phase | Key Activities | Success Criteria | Shannon Enhancement |
|-------|---------------|------------------|---------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY | Quantitative tracking in Serena |
| **2. Pattern** | Find working examples, compare | Identify differences | Automated pattern search |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis | Confidence scoring (0.00-1.00) |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass | 3-tier validation gates |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated (save to Serena)
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But**: 95% of "no root cause" cases are incomplete investigation.

## Integration with Other Skills

**This skill requires using**:
- **root-cause-tracing** - REQUIRED when error is deep in call stack (see Phase 1, Step 5)
- **test-driven-development** - REQUIRED for creating failing test case (see Phase 4, Step 1)
- **verification-before-completion** - REQUIRED for verifying fix worked (see Phase 4, Step 3)

**Complementary skills**:
- **defense-in-depth** - Add validation at multiple layers after finding root cause
- **mcp-discovery** - Find debugging MCPs for specific domains

**Shannon integration**:
- **Serena MCP** - Track all debugging sessions, learn patterns
- **Sequential MCP** - Deep analysis when stuck (100+ thoughts)
- **Tavily/Context7** - Research when don't understand issue

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**Shannon tracking proves this**: Query debugging_sessions with success:true vs failed attempts.

## The Bottom Line

**Systematic > Random. Evidence > Guessing. Root Cause > Symptom.**

Shannon's quantitative tracking turns debugging from art into science.

Measure everything. Learn from patterns. Never fix without understanding.

