---
name: systematic-debugging
description: |
  Four-phase root cause investigation protocol: Investigation → Pattern Analysis → Hypothesis Testing → Implementation.
  NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. Prevents shotgun debugging, requires evidence-based diagnosis,
  implements defense-in-depth. Integrates Sequential MCP for deep thinking, Serena for session persistence.

skill-type: PROTOCOL
shannon-version: ">=5.4.0"
category: debugging

invoked-by-commands:
  - /shannon:debug

related-skills:
  - root-cause-tracing
  - defense-in-depth
  - verification-before-completion
  - functional-testing

mcp-requirements:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: Persist debugging sessions for pattern detection
      fallback: ERROR - Cannot save debug history
  recommended:
    - name: sequential
      purpose: Deep thinking during root cause analysis (100+ thoughts)

allowed-tools: [Read, Grep, Bash, TodoWrite, Sequential, Serena, Skill]
---

# Systematic Debugging

## Purpose

Four-phase root cause investigation that **prevents fixes before understanding**, eliminating shotgun debugging and ensuring evidence-based solutions with defense-in-depth protection.

**Core Philosophy**: Process over guessing. Root cause over symptoms. Evidence over assumptions.

**Shannon Integration**: Quantified hypothesis confidence, Sequential MCP deep thinking, Serena session persistence, NO MOCKS compliance.

---

## Iron Law

<IRON_LAW>

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

You MUST complete Phase 1 (Root Cause Investigation) before proposing ANY fix.

Violations:
- ❌ "Let me try this quick fix"
- ❌ "This should solve it"
- ❌ "Testing multiple changes simultaneously"
- ❌ "Skipping test creation"

Required:
- ✅ Complete Phase 1: Identify root cause
- ✅ Formulate written hypothesis with confidence score
- ✅ Test with minimal isolated change
- ✅ Verify before implementing full fix

**After 3 failed fixes: STOP. Question architecture, not patches.**

</IRON_LAW>

---

## The Four Phases

### Phase 1: Root Cause Investigation

**Goal**: Find the ACTUAL problem, not symptoms

**Steps**:

1. **Analyze Error Evidence**
   ```
   - Read complete error message (every line)
   - Read full stack trace (entry to exit)
   - Note error type, line numbers, function names
   - Identify WHERE error manifests (not necessarily WHERE it originates)
   ```

2. **Reproduce Consistently**
   ```
   - Document exact reproduction steps
   - Test reproduction 3 times → Success rate
   - Capture reproduction command/script
   - Note any reproduction variability
   ```

3. **Review Recent Changes**
   ```bash
   # Use Bash tool
   git log --oneline --since="1 week ago" --all -- <affected_file>
   git diff HEAD~10 HEAD -- <affected_file>
   ```

   Questions:
   - What changed in affected areas?
   - When did bug first appear?
   - What was working before?

4. **Multi-Component Boundary Diagnosis** (if applicable)

   For systems with multiple layers (API → Service → Database, Frontend → Backend → Cache):

   ```
   Add diagnostic logging at EACH boundary:
   - Input entering component
   - Output leaving component
   - Error states within component

   Goal: Identify WHICH component fails
   ```

   Example:
   ```python
   # At each boundary
   logger.error(f"[BOUNDARY] Input: {input_data}")
   try:
       result = process(input_data)
       logger.error(f"[BOUNDARY] Output: {result}")
   except Exception as e:
       logger.error(f"[BOUNDARY] Error: {e}", exc_info=True)
   ```

5. **Backward Data Flow Tracing**

   If component identified, invoke sub-skill:
   ```
   @skill root-cause-tracing

   Error Location: <identified_component>
   Symptom: <error_message>
   Call Stack: <stack_trace>
   ```

   This traces backward through call chain to original trigger.

6. **Deep Thinking via Sequential MCP**

   Use Sequential MCP for synthesis:
   ```
   @tool sequential-thinking

   Question: What is the root cause of [error]?

   Evidence:
   - Error: [full message]
   - Stack trace: [complete trace]
   - Recent changes: [git diff summary]
   - Boundary diagnosis: [which component failed]
   - Data flow trace: [backward trace results]

   Thinking Required: 100+ thoughts minimum
   Output: Root cause hypothesis with confidence score (0.00-1.00)
   ```

**Output**: Root cause hypothesis with confidence score

**Phase 1 Completion Criteria**:
- ✅ Error reproduced consistently (3/3 times)
- ✅ Recent changes reviewed
- ✅ Component boundary identified (if multi-component)
- ✅ Data flow traced backward to trigger
- ✅ Sequential MCP analysis complete (100+ thoughts)
- ✅ Hypothesis formulated with confidence score ≥ 0.70

**Save to Serena**:
```
write_memory("shannon_debug_{timestamp}", {
  phase: "root_cause_investigation",
  error: "{error_message}",
  reproduction_rate: {success_rate},
  hypothesis: "{root_cause_hypothesis}",
  confidence: {0.00-1.00},
  evidence: [list of findings],
  timestamp: "{ISO_timestamp}"
})
```

---

### Phase 2: Pattern Analysis

**Goal**: Find working implementations to compare against

**Steps**:

1. **Locate Similar Working Code**
   ```bash
   # Use Grep tool
   grep -r "similar_pattern" --include="*.{py,js,ts}" codebase/
   ```

   Find:
   - Functions that do similar operations successfully
   - Same framework patterns elsewhere
   - Reference implementations

2. **Read Completely (Forced Reading)**

   For each working implementation:
   ```
   - Count total lines
   - Read ALL lines (no skimming)
   - Verify completeness (100%)
   ```

3. **Document Every Difference**

   Create comparison table:

   | Aspect | Working Code | Broken Code | Impact |
   |--------|--------------|-------------|---------|
   | Validation | Checks input not null | No validation | HIGH |
   | Error handling | try/catch present | No error handling | HIGH |
   | Data type | Uses string | Uses int | MEDIUM |
   | Async handling | await promise | Direct call | HIGH |

4. **Analyze Dependencies**
   ```
   Compare:
   - Import statements
   - Configuration files
   - Environment variables
   - External library versions
   ```

5. **Quantify Similarity Score**
   ```
   similarity_score = (common_patterns / total_patterns) * 100

   Example:
   - Common patterns: 7
   - Total patterns: 10
   - Similarity: 70%
   ```

**Output**: Difference table with quantified similarity score

**Phase 2 Completion Criteria**:
- ✅ At least 2 working implementations found
- ✅ All working code read completely
- ✅ Difference table with 5+ comparisons
- ✅ Similarity score calculated
- ✅ Dependencies analyzed

**Save to Serena**:
```
write_memory("shannon_debug_{timestamp}", {
  ...existing_data,
  phase: "pattern_analysis",
  working_implementations: [list of files],
  differences: [table data],
  similarity_score: {percentage},
  timestamp: "{ISO_timestamp}"
})
```

---

### Phase 3: Hypothesis Testing

**Goal**: Test hypothesis with minimal, isolated change

**Steps**:

1. **Formulate Written Hypothesis**

   Template:
   ```markdown
   ## Hypothesis

   **Root Cause**: [specific cause identified]

   **Confidence**: {0.00-1.00} (Shannon metric)

   **Evidence Supporting**:
   - [evidence item 1]
   - [evidence item 2]
   - [evidence item 3]

   **Predicted Fix**: [minimal change to test]

   **Expected Outcome**: [what should change if hypothesis correct]
   ```

2. **Create Minimal Test Change**

   Requirements:
   - Change ONE thing only
   - Smallest possible modification
   - Easily reversible
   - Isolated from other changes

3. **Test Hypothesis**

   ```bash
   # Reproduce error again
   {reproduction_command}
   # Expected: Error still occurs (baseline)

   # Apply minimal change
   # Test again
   {reproduction_command}
   # Expected: Different outcome if hypothesis correct
   ```

4. **Evaluate Results**

   | Outcome | Confidence Adjustment | Next Action |
   |---------|----------------------|-------------|
   | Error resolved completely | +0.20 | Proceed to Phase 4 |
   | Error partially improved | +0.10 | Refine hypothesis, test again |
   | No change | -0.15 | Revise hypothesis, return to Phase 1 |
   | New error appeared | -0.25 | Wrong hypothesis, return to Phase 1 |

5. **Track Failed Attempts**
   ```
   failed_fixes_count += 1

   IF failed_fixes_count >= 3:
     STOP → Architectural problem
     INVOKE: @skill verification-before-completion (check if architecture needs redesign)
   ```

**Output**: Hypothesis test results with updated confidence score

**Phase 3 Completion Criteria**:
- ✅ Written hypothesis with initial confidence ≥ 0.70
- ✅ Minimal change tested in isolation
- ✅ Results documented
- ✅ Confidence score updated based on results
- ✅ Final confidence ≥ 0.85 to proceed

**Save to Serena**:
```
write_memory("shannon_debug_{timestamp}", {
  ...existing_data,
  phase: "hypothesis_testing",
  hypothesis: "{written_hypothesis}",
  initial_confidence: {0.00-1.00},
  test_change: "{minimal_change}",
  test_result: "{outcome}",
  final_confidence: {0.00-1.00},
  failed_attempts: {count},
  timestamp: "{ISO_timestamp}"
})
```

---

### Phase 4: Implementation

**Goal**: Implement complete fix with defense-in-depth

**Steps**:

1. **Create Failing Test First**

   Following Shannon's NO MOCKS philosophy:
   ```
   - Create test that reproduces bug
   - Test MUST use real systems (no mocks)
   - Test MUST fail before fix
   - Test MUST pass after fix
   ```

2. **Implement Root Cause Fix**

   Requirements:
   - Address root cause (not symptom)
   - Minimal change principle
   - Single fix (not multiple unrelated changes)

3. **Apply Defense-in-Depth**

   Invoke sub-skill:
   ```
   @skill defense-in-depth

   Root Cause: {identified_cause}
   Fix Applied: {fix_description}
   System Layers: [list of layers in system]

   Goal: Add validation at multiple layers to make bug structurally impossible
   ```

   This adds 4 layers of protection:
   - Layer 1: Entry point validation
   - Layer 2: Business logic validation
   - Layer 3: Environment guards
   - Layer 4: Debug instrumentation

4. **Verify Fix**

   Following Shannon's verification protocol:
   ```
   1. Run failing test → MUST pass now
   2. Run full test suite → All tests pass
   3. Manual reproduction → Error no longer occurs
   4. Edge case testing → Related scenarios work
   ```

5. **Run Validation Gates**
   ```bash
   # Tests
   npm test  # or pytest, go test, etc.
   # Exit code: 0 (all pass)

   # Lint
   npm run lint
   # Exit code: 0 (clean)

   # Build
   npm run build
   # Exit code: 0 (success)
   ```

6. **Evidence-Based Completion**

   Invoke sub-skill:
   ```
   @skill verification-before-completion

   Claim: Bug is fixed
   Evidence Required:
   - Test output showing pass
   - Reproduction command showing no error
   - Full test suite passing
   - All validation gates passed
   ```

**Output**: Complete fix with defense-in-depth + verification evidence

**Phase 4 Completion Criteria**:
- ✅ Failing test created (NO MOCKS)
- ✅ Test failed before fix
- ✅ Root cause fix implemented
- ✅ Defense-in-depth applied (4 layers)
- ✅ Test passes after fix
- ✅ Full test suite passes
- ✅ All validation gates passed (test, lint, build)
- ✅ Verification evidence documented

**Save to Serena**:
```
write_memory("shannon_debug_{timestamp}", {
  ...existing_data,
  phase: "implementation",
  test_created: "{test_file_path}",
  fix_implemented: "{fix_description}",
  defense_layers: [list of 4 layers],
  test_suite_status: "PASSED",
  validation_gates: {
    tests: "PASSED",
    lint: "PASSED",
    build: "PASSED"
  },
  verification_evidence: "{evidence}",
  completed: true,
  timestamp: "{ISO_timestamp}"
})
```

---

## Critical Red Flags

If you catch yourself doing ANY of these, **STOP IMMEDIATELY**:

### 🚨 Red Flag 1: "Let me try this quick fix"

**Why This is Wrong**:
- Bypasses Phase 1 (root cause investigation)
- Treats symptom, not cause
- Creates more bugs

**Required Action**:
- Return to Phase 1
- Complete root cause investigation
- No fixes until hypothesis ≥ 0.85 confidence

---

### 🚨 Red Flag 2: "I'll test multiple changes at once"

**Why This is Wrong**:
- Cannot isolate which change worked
- Violates Phase 3 (minimal isolated testing)
- Confounds results

**Required Action**:
- Test ONE change at a time
- Document result before next change
- Update confidence score per change

---

### 🚨 Red Flag 3: "Skip test creation, I'll add it later"

**Why This is Wrong**:
- Violates NO MOCKS philosophy
- No evidence of fix
- Bug can reappear silently

**Required Action**:
- Create test FIRST (must fail)
- Apply fix
- Verify test passes
- No completion without test

---

### 🚨 Red Flag 4: "Three fixes failed, let me try a fourth"

**Why This is Wrong**:
- Signals architectural problem
- More patches won't help
- Need redesign, not more fixes

**Required Action**:
- STOP patching
- Document pattern of failures
- Discuss architectural redesign
- Don't attempt fix #4

---

## Multi-Component Diagnostic Pattern

For systems with multiple components (workflows, services, databases, caches):

**Strategy**: Log at every boundary to identify which component fails

**Implementation**:
```python
# At each component boundary
def process_request(data):
    # Entry logging
    logger.error(f"[ENTRY] Component: {component_name}, Input: {data}")

    try:
        # Process
        result = component_logic(data)

        # Exit logging
        logger.error(f"[EXIT] Component: {component_name}, Output: {result}")
        return result
    except Exception as e:
        # Error logging
        logger.error(
            f"[ERROR] Component: {component_name}, "
            f"Exception: {e}, "
            f"Stack: {traceback.format_exc()}"
        )
        raise
```

**Goal**: Pinpoint EXACTLY where failure occurs, enabling focused investigation

---

## Integration with Shannon Commands

### Invoked By: `/shannon:debug`

The `/shannon:debug` command delegates to this skill:

```bash
/shannon:debug --error "TypeError: Cannot read property 'id' of undefined" --file src/api/users.ts
```

Workflow:
1. Command captures error description and file
2. Invokes this skill with error context
3. Skill executes 4 phases
4. Returns fix + verification evidence
5. Debug session saved to Serena

---

## Integration with Shannon Skills

**Uses**:
- `root-cause-tracing` (Phase 1: backward data flow)
- `defense-in-depth` (Phase 4: multi-layer protection)
- `verification-before-completion` (Phase 4: evidence gates)
- `functional-testing` (Phase 4: NO MOCKS tests)

**Used By**:
- User via `/shannon:debug`
- `intelligent-do` when errors encountered
- `wave-orchestration` when tasks fail

---

## Examples

### Example 1: Simple Bug - Missing Null Check

**Phase 1: Root Cause Investigation**
```
Error: TypeError: Cannot read property 'id' of undefined
File: src/api/users.ts:45

Reproduction: 100% (3/3)
Command: curl http://localhost:3000/api/users/999

Sequential Analysis: user not found returns undefined, then accessed .id
Hypothesis: Missing null check before accessing user.id
Confidence: 0.90
```

**Phase 2: Pattern Analysis**
```
Working Implementation: src/api/products.ts:32
Difference: Products checks if product exists before accessing properties
Similarity Score: 85%
```

**Phase 3: Hypothesis Testing**
```
Minimal Change: Add if (!user) return null before accessing user.id
Test Result: Error resolved
Confidence: 0.95 → Proceed to Phase 4
```

**Phase 4: Implementation**
```
1. Created test: tests/api/users.test.ts (NO MOCKS)
2. Test failed (reproduced bug)
3. Applied fix: null check
4. Applied defense-in-depth:
   - Layer 1: API validates user ID format
   - Layer 2: Service checks user existence before access
   - Layer 3: Database query returns null for not found
   - Layer 4: Added logging for null cases
5. Test passed
6. Full suite passed: 147/147
7. Validation gates: ✅ Tests ✅ Lint ✅ Build
```

**Session Duration**: 12 minutes
**Confidence Final**: 0.98

---

### Example 2: Complex Bug - Race Condition

**Phase 1: Root Cause Investigation**
```
Error: Race condition in cache updates (intermittent)
File: src/services/cache.ts:67

Reproduction: 40% (2/5 attempts - intermittent!)

Sequential Analysis:
- Two requests simultaneously update same cache key
- Last writer wins, data inconsistent
- No locking mechanism

Hypothesis: Race condition due to non-atomic read-modify-write
Confidence: 0.75
```

**Phase 2: Pattern Analysis**
```
Working Implementation: Redis atomic operations in src/services/redis.ts
Differences:
- Working: Uses WATCH/MULTI/EXEC (atomic)
- Broken: Separate READ then WRITE (non-atomic)
Similarity Score: 60%
```

**Phase 3: Hypothesis Testing**
```
Minimal Change: Add mutex lock around read-modify-write
Test Result: Reproduction rate dropped from 40% to 0% (20 attempts)
Confidence: 0.88 → Proceed to Phase 4
```

**Phase 4: Implementation**
```
1. Created test: tests/services/cache-race.test.ts (spawns real concurrent requests)
2. Test failed (reproduced race 3/10 times)
3. Applied fix: Mutex-based critical section
4. Applied defense-in-depth:
   - Layer 1: Mutex lock at cache service entry
   - Layer 2: Redis WATCH/MULTI/EXEC fallback
   - Layer 3: Optimistic locking with version numbers
   - Layer 4: Race detection instrumentation
5. Test passed (0/100 races detected)
6. Full suite passed: 147/147
7. Validation gates: ✅ Tests ✅ Lint ✅ Build
```

**Session Duration**: 45 minutes
**Confidence Final**: 0.92

---

## Testing Requirements

Following Shannon's functional testing protocol:

### RED Phase (Baseline)
Test systematic-debugging WITHOUT enforcement:
- Agent proposes fix before Phase 1 complete
- Agent tests multiple changes simultaneously
- Agent skips test creation
- Document all violations

### GREEN Phase (Compliance)
Test systematic-debugging WITH enforcement:
- Agent blocked from fixes until Phase 1 complete
- Agent tests changes in isolation
- Agent creates tests first
- All violations prevented

### REFACTOR Phase (Pressure)
Test under maximum pressure:
- Complex multi-component bug
- Intermittent reproduction
- 3 failed hypothesis tests
- Time pressure
- Verify enforcement holds

**Success Criteria**: >90% of bugs fixed with evidence, <3 failed attempts per bug

---

## Anti-Rationalization

### Rationalization 1: "This is a simple bug, skip to the fix"

**COUNTER**:
- ❌ "Simple" bugs often have complex root causes
- ❌ Skipping Phase 1 = treating symptoms
- ✅ Phase 1 takes 2-5 minutes for simple bugs
- ✅ Ensures fix addresses root cause, not symptom

**Rule**: Complete Phase 1 for ALL bugs, no exceptions.

---

### Rationalization 2: "I already know the cause from experience"

**COUNTER**:
- ❌ "Knowing" without evidence = assumption
- ❌ Assumptions cause wrong fixes
- ✅ Phase 1 provides evidence
- ✅ Sequential MCP thinking reveals nuances

**Rule**: Experience informs hypothesis, evidence confirms it.

---

### Rationalization 3: "Testing multiple changes is more efficient"

**COUNTER**:
- ❌ Multiple changes = cannot isolate which worked
- ❌ "Efficient" debugging = confounded results
- ✅ Isolated testing = clear causation
- ✅ 5 minutes per test < hours of confusion

**Rule**: ONE change per test, always.

---

## Serena Memory Integration

**Session Start**:
```
session_id = f"shannon_debug_{timestamp}"
write_memory(session_id, {phase: "started", error: "..."})
```

**Phase Transitions**:
```
write_memory(session_id, {...existing, phase: "pattern_analysis", ...})
```

**Session Complete**:
```
write_memory(session_id, {
  ...all_phases,
  completed: true,
  success: true,
  duration_minutes: {duration},
  confidence_final: {0.00-1.00}
})
```

**Pattern Detection Across Sessions**:
```
# Query similar bugs
all_debug_sessions = list_memories(pattern="shannon_debug_*")
similar_bugs = [s for s in all_debug_sessions if s.error_type == current_error_type]
# Learn from past solutions
```

---

## Status

**Implementation Status**: ✅ Ready for functional testing
**Version**: 5.4.0
**Dependencies**: root-cause-tracing, defense-in-depth, verification-before-completion, functional-testing
**MCP Required**: Serena (required), Sequential (recommended)

---

**The Bottom Line**: Process over guessing. Root cause over symptoms. Evidence over assumptions. Defense-in-depth over single fixes.
