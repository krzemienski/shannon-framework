---
name: verification-before-completion
description: |
  Evidence-based completion protocol: No completion claims without fresh verification evidence.
  5-step gate process (Identify → Run → Read → Verify → Claim). Blocks "should", "probably", "seems to".
  Integrated with hooks to prevent commits without verification. NO COMPLETION WITHOUT EVIDENCE.

skill-type: PROTOCOL
shannon-version: ">=5.4.0"
category: collaboration

invoked-by-commands:
  - All Shannon commands before completion

related-skills:
  - systematic-debugging
  - executing-plans
  - finishing-branch
  - functional-testing

mcp-requirements:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: Store verification evidence for hook enforcement
      fallback: ERROR - Cannot enforce without evidence storage

allowed-tools: [Bash, Read, Serena]
---

# Verification Before Completion

## Purpose

**Evidence-based completion protocol** that prevents completion claims without fresh verification evidence. No assumptions, no "should work", no "looks good"—only verified facts.

**Core Principle**: "Evidence before claims, always."

**Shannon Integration**: Hook enforcement (blocks commits without verification), Serena evidence storage, quantified verification completeness.

---

## Iron Law

<IRON_LAW>

**NO COMPLETION CLAIMS WITHOUT VERIFICATION EVIDENCE**

You MUST execute verification commands and review output BEFORE any completion claim.

Violations:
- ❌ "Tests should pass now"
- ❌ "This probably works"
- ❌ "Looks like it's fixed"
- ❌ "Done!" (without running verification)

Required:
- ✅ Run test command
- ✅ Read complete output
- ✅ Verify exit code = 0
- ✅ THEN claim "Tests pass"

**No exceptions. Ever.**

</IRON_LAW>

---

## The Five-Step Gate Process

Before ANY completion claim, follow these exact steps:

### Step 1: Identify the Proving Command

**Goal**: Determine what command proves the claim

**Common Claims → Proving Commands**:

| Claim | Proving Command |
|-------|----------------|
| "Tests pass" | `npm test` or `pytest` or `go test` |
| "Linter clean" | `npm run lint` or `ruff check .` |
| "Build succeeds" | `npm run build` or `cargo build` |
| "Bug fixed" | Reproduce steps (must no longer show error) |
| "Feature complete" | Acceptance criteria checklist (line-by-line) |
| "No uncommitted changes" | `git status` |
| "Branch up to date" | `git fetch && git status` |
| "Documentation updated" | Read docs files, verify mentions of feature |

**Output**: Command string to execute

---

### Step 2: Run the Command

**Goal**: Execute command completely and freshly

**Requirements**:
- ✅ Run in current session (not based on previous run)
- ✅ Complete execution (don't interrupt)
- ✅ Capture full output (stdout + stderr)
- ✅ Capture exit code

**Bash Tool Pattern**:
```
Use Bash tool to run: {proving_command}
Wait for complete output
Note exit code
```

**Anti-Pattern** (NEVER DO THIS):
```
❌ "I ran tests earlier and they passed"
❌ "Tests should still pass from before"
❌ "Skipping test run, nothing changed"
```

**Correct Pattern**:
```
✅ Bash: npm test (runs NOW, captures output)
✅ Wait for completion
✅ Read exit code: 0
```

---

### Step 3: Read Full Output

**Goal**: Review COMPLETE output, not summary

**Requirements**:
- ✅ Read every line of output
- ✅ Check exit code explicitly
- ✅ Note any warnings or errors
- ✅ Verify expected patterns present

**What to Look For**:

Tests:
```
- Exit code: 0 (required)
- Pass count: All tests passed
- Fail count: 0 (required)
- Error count: 0 (required)
- Time: Reasonable duration
- Coverage: If available, note percentage
```

Linter:
```
- Exit code: 0 (required)
- Error count: 0 (required)
- Warning count: 0 or explained
- Files checked: Non-zero
```

Build:
```
- Exit code: 0 (required)
- Build output: Success message
- Artifacts: Files created
- No error messages
```

**Anti-Pattern**:
```
❌ Glance at output: "Looks good"
❌ Skip reading: "Exit code is 0, so it passed"
❌ Assume: "Usually it passes"
```

**Correct Pattern**:
```
✅ Read complete test output line by line
✅ Verify: "147 tests passed, 0 failed"
✅ Verify: Exit code 0
✅ Verify: No error messages in output
```

---

### Step 4: Verify Output Confirms Claim

**Goal**: Explicit verification that evidence supports claim

**Verification Checklist**:

For "Tests pass" claim:
```
[ ] Exit code is 0
[ ] Test count > 0 (tests actually ran)
[ ] Fail count = 0
[ ] Error count = 0
[ ] No "FAILED" messages in output
[ ] No "ERROR" messages in output
```

For "Bug fixed" claim:
```
[ ] Original reproduction steps executed
[ ] Error message no longer appears
[ ] Expected behavior now occurs
[ ] Related edge cases also work
[ ] Verified in current session (not memory)
```

For "Feature complete" claim:
```
[ ] All acceptance criteria listed
[ ] Each criterion checked individually
[ ] Evidence for EACH criterion (not bulk "all done")
[ ] No criterion skipped or assumed
```

**Decision Point**:
- All checkboxes ✅ → Claim is supported → Proceed to Step 5
- Any checkbox ❌ → Claim NOT supported → STOP, fix issues

---

### Step 5: State Result with Evidence

**Goal**: Make completion claim with explicit evidence reference

**Correct Pattern**:
```markdown
✅ Tests Pass

**Evidence**:
- Command: npm test
- Exit Code: 0
- Output: 147 tests passed, 0 failed
- Duration: 12.3s
- Timestamp: 2025-11-18 10:45:32
```

**Another Correct Pattern**:
```markdown
✅ Bug Fixed

**Evidence**:
- Reproduction: curl http://localhost:3000/api/users/999
- Previous: TypeError: Cannot read property 'id' of undefined
- Current: {"error": "User not found"} (expected behavior)
- Exit Code: 0 (API returns gracefully)
- Verified: 2025-11-18 10:47:15
```

**Incorrect Pattern** (BLOCKED):
```
❌ "Done! Tests pass" (no evidence)
❌ "Bug fixed" (no reproduction shown)
❌ "Everything works" (vague, no specifics)
```

---

## Critical Red Flags

If you catch yourself using these phrases, **STOP IMMEDIATELY** and run verification:

### 🚨 Red Flag 1: "Should" / "Probably" / "Seems to"

**Phrases to Watch**:
- "Tests should pass now"
- "This probably fixes it"
- "Seems to be working"
- "Appears correct"
- "Likely resolved"

**What This Means**: You're assuming, not verifying

**Required Action**:
1. STOP making the claim
2. Identify proving command (Step 1)
3. Run command (Step 2)
4. Read output (Step 3)
5. Verify explicitly (Step 4)
6. THEN state result (Step 5)

---

### 🚨 Red Flag 2: Satisfaction Expressions Before Verification

**Phrases to Watch**:
- "Done!"
- "Perfect!"
- "Great!"
- "Excellent!"
- "Finished!"

**What This Means**: You're celebrating before verification

**Required Action**:
- Satisfaction is appropriate AFTER verification
- Run verification first
- THEN express satisfaction

**Correct Pattern**:
```
1. Run: npm test
2. Verify: 147 passed, 0 failed, exit 0
3. Save to Serena: verification evidence
4. THEN: "✅ Tests pass! Feature complete."
```

---

### 🚨 Red Flag 3: "Earlier" / "Previous" / "Last Time"

**Phrases to Watch**:
- "Tests passed earlier"
- "I verified this previously"
- "Last run showed success"
- "Already checked"

**What This Means**: Using old evidence, not fresh verification

**Required Action**:
- Past verification does NOT count
- Code may have changed since
- Run verification FRESH in current session
- THEN make claim

**Why Fresh Matters**:
- You may have introduced regressions
- Dependencies may have changed
- Environment may differ
- Verification must be current

---

## Common Verification Requirements

### Tests Pass

**Proving Command**:
```bash
# Node.js
npm test

# Python
pytest

# Go
go test ./...

# Rust
cargo test
```

**Required Evidence**:
```
- Exit code: 0
- Pass count: > 0
- Fail count: 0
- Error count: 0
- Output: "X tests passed"
```

**Save to Serena**:
```
write_memory("shannon_verification_latest", {
  type: "tests",
  command: "npm test",
  exit_code: 0,
  passed: 147,
  failed: 0,
  duration: 12.3,
  timestamp: "{ISO_timestamp}"
})
```

---

### Linter Clean

**Proving Command**:
```bash
# Node.js
npm run lint

# Python
ruff check .

# Rust
cargo clippy
```

**Required Evidence**:
```
- Exit code: 0
- Error count: 0
- Warning count: 0 (or explicitly documented)
- Files checked: > 0
```

**Save to Serena**:
```
write_memory("shannon_verification_latest", {
  type: "lint",
  command: "npm run lint",
  exit_code: 0,
  errors: 0,
  warnings: 0,
  files_checked: 45,
  timestamp: "{ISO_timestamp}"
})
```

---

### Build Succeeds

**Proving Command**:
```bash
# Node.js
npm run build

# Rust
cargo build --release

# Go
go build ./cmd/app
```

**Required Evidence**:
```
- Exit code: 0
- Build artifacts created
- No error messages
- Success message present
```

**Save to Serena**:
```
write_memory("shannon_verification_latest", {
  type: "build",
  command: "npm run build",
  exit_code: 0,
  artifacts: ["dist/main.js", "dist/styles.css"],
  timestamp: "{ISO_timestamp}"
})
```

---

### Bug Fixed

**Proving Command**: Original reproduction steps

**Required Evidence**:
```
- Reproduce command executed
- Previous error documented
- Current output shows fix
- Expected behavior confirmed
```

**Example**:
```bash
# Previous: TypeError
# Current: Expected behavior

curl http://localhost:3000/api/users/999
# Output: {"error": "User not found"}
# Exit Code: 0
```

**Save to Serena**:
```
write_memory("shannon_verification_latest", {
  type: "bug_fix",
  reproduction_command: "curl http://localhost:3000/api/users/999",
  previous_error: "TypeError: Cannot read property 'id' of undefined",
  current_output: '{"error": "User not found"}',
  expected: true,
  timestamp: "{ISO_timestamp}"
})
```

---

### Requirements Met

**Proving Command**: Line-by-line checklist

**Required Evidence**:
```
- All requirements listed
- Each requirement verified individually
- Evidence per requirement
- No requirements skipped
```

**Example**:
```markdown
## Requirement Verification

[ ✅ ] User can register with email
      Evidence: POST /api/register → 201 Created

[ ✅ ] User receives confirmation email
      Evidence: Mailhog shows email sent, content verified

[ ✅ ] User can login with credentials
      Evidence: POST /api/login → 200 OK, token returned

[ ✅ ] Token grants API access
      Evidence: GET /api/profile (with token) → 200 OK
```

**Save to Serena**:
```
write_memory("shannon_verification_latest", {
  type: "requirements",
  total_requirements: 4,
  verified_requirements: 4,
  completion_percentage: 100,
  evidence: [list of verification items],
  timestamp: "{ISO_timestamp}"
})
```

---

## Hook Integration

### post_tool_use.py Enhancement

Shannon's `post_tool_use.py` hook blocks git commits without verification:

**Hook Logic**:
```python
def check_commit_verification(bash_command: str) -> bool:
    """Block commits without fresh verification evidence"""

    if 'git commit' not in bash_command:
        return True  # Not a commit, allow

    # Check Serena for verification evidence
    try:
        verification = serena.read_memory('shannon_verification_latest')
    except:
        return block_with_message(
            "❌ COMMIT BLOCKED: No verification evidence found.\n"
            "\n"
            "Required: Run verification gates before commit:\n"
            "  1. Tests: npm test (or pytest, go test, etc.)\n"
            "  2. Lint: npm run lint\n"
            "  3. Build: npm run build\n"
            "\n"
            "Or invoke: @skill verification-before-completion"
        )

    # Check verification is fresh (< 5 minutes old)
    age = time.time() - verification['timestamp']
    if age > 300:  # 5 minutes
        return block_with_message(
            "❌ COMMIT BLOCKED: Verification evidence too old.\n"
            f"\n"
            f"Evidence age: {age // 60} minutes\n"
            f"Required: Fresh verification within 5 minutes of commit.\n"
            "\n"
            "Re-run verification gates:\n"
            "  - npm test\n"
            "  - npm run lint\n"
            "  - npm run build"
        )

    # Check all gates passed
    if verification.get('exit_code') != 0:
        return block_with_message(
            f"❌ COMMIT BLOCKED: Verification failed.\n"
            f"\n"
            f"Type: {verification['type']}\n"
            f"Exit Code: {verification['exit_code']}\n"
            f"Command: {verification['command']}\n"
            "\n"
            "Fix failures before committing."
        )

    # All checks passed
    return True  # Allow commit
```

**Effect**: Impossible to commit without verification evidence

---

## Integration with Shannon Commands

This skill is invoked by ALL Shannon commands before completion:

**Pattern**:
```
shannon:do → Execute task
          → Before completion: @skill verification-before-completion
          → Verify tests/lint/build
          → Save evidence to Serena
          → THEN report completion
```

**Commands Using This Skill**:
- `/shannon:do` - before final report
- `/shannon:wave` - after wave execution
- `/shannon:exec` - after 3-tier validation
- `/shannon:debug` - after bug fix
- `/shannon:execute-plan` - after batch completion
- `/shannon:finish-branch` - comprehensive verification

---

## Why Past Failures Happened

**Documented Issues from Shannon History**:

1. **Undefined Functions Shipped**
   - Claim: "Code complete"
   - Reality: Function referenced but never defined
   - Cause: No `npm run build` verification
   - Hook: Would have caught via build failure

2. **Incomplete Features Deployed**
   - Claim: "Feature ready"
   - Reality: Only 60% of requirements implemented
   - Cause: No line-by-line checklist verification
   - Hook: Would have caught via requirements check

3. **Broken Tests Committed**
   - Claim: "Tests pass"
   - Reality: Tests skipped, failures ignored
   - Cause: Assumed tests passed without running
   - Hook: Would have caught via fresh test run requirement

**Pattern**: Every case involved **assumption without verification**

**Solution**: This skill makes assumptions impossible through hook enforcement

---

## Examples

### Example 1: Test Verification

**❌ WRONG (Blocked)**:
```
Claude: "I've fixed the bug. Tests should pass now. Done!"

Hook: BLOCKED - No verification evidence in Serena
```

**✅ CORRECT**:
```
Claude: "I've fixed the bug. Let me verify tests pass."

Step 1: Identify → "npm test"
Step 2: Run → Bash: npm test
Step 3: Read → "147 tests passed, 0 failed, exit code 0"
Step 4: Verify → All checks passed
Step 5: Claim → "✅ Tests pass. Bug fixed."

Evidence saved to Serena → Hook allows commit
```

---

### Example 2: Bug Fix Verification

**❌ WRONG (Blocked)**:
```
Claude: "Bug fixed by adding null check. Probably works now."

Hook: BLOCKED - "Probably" = no verification
```

**✅ CORRECT**:
```
Claude: "Bug fixed by adding null check. Let me verify."

Step 1: Identify → Original reproduction command
Step 2: Run → curl http://localhost:3000/api/users/999
Step 3: Read → {"error": "User not found"} (no TypeError!)
Step 4: Verify → Error message changed, expected behavior
Step 5: Claim → "✅ Bug fixed. Verified with original repro."

Evidence: curl output shows no TypeError
Save to Serena → Hook allows commit
```

---

### Example 3: Feature Completion

**❌ WRONG (Blocked)**:
```
Claude: "Feature complete! All requirements done."

Hook: BLOCKED - No requirement verification evidence
```

**✅ CORRECT**:
```
Claude: "Let me verify all requirements are met."

Step 1: Identify → Requirements checklist
Step 2: Run → Test each requirement individually
Step 3: Read → Results for each requirement
Step 4: Verify → Check each requirement:
  [ ✅ ] Req 1: User registration → POST /api/register → 201
  [ ✅ ] Req 2: Email confirmation → Mailhog shows email
  [ ✅ ] Req 3: User login → POST /api/login → 200 + token
  [ ✅ ] Req 4: Token auth → GET /api/profile → 200
Step 5: Claim → "✅ Feature complete. All requirements verified."

Evidence: 4/4 requirements met with individual verification
Save to Serena → Hook allows commit
```

---

## Quantitative Metrics

### Verification Completeness Score

```
completeness = (verification_steps_completed / 5) * 100

Steps:
1. Identify proving command
2. Run command
3. Read output
4. Verify evidence
5. State result

Shannon Target: 100% (all 5 steps)
```

### Verification Freshness

```
freshness = max(0, 1 - (age_seconds / 300))

Age < 1 min: 1.00 (FRESH)
Age 2-3 min: 0.60 (ACCEPTABLE)
Age > 5 min: 0.00 (STALE - blocked by hook)

Shannon Target: ≥0.60 (< 3 minutes old)
```

### Evidence Quality Score

```
quality = (evidence_items_present / required_items) * 1.00

Required items (test verification):
- Command executed
- Exit code
- Pass count
- Fail count
- Timestamp

Shannon Target: 1.00 (all required items)
```

---

## Anti-Rationalization

### Rationalization 1: "Simple change, verification not needed"

**COUNTER**:
- ❌ "Simple" changes cause bugs frequently
- ❌ Skipping verification = assumptions
- ✅ Verification takes 30 seconds
- ✅ Hook enforcement prevents bypassing

**Rule**: Verify ALL changes, no exceptions

---

### Rationalization 2: "I'm confident it works"

**COUNTER**:
- ❌ Confidence without evidence = overconfidence
- ❌ Humans are notoriously bad at predicting code behavior
- ✅ Evidence replaces confidence
- ✅ Verification converts confidence to fact

**Rule**: Confidence is not evidence. Verify.

---

### Rationalization 3: "Tests passed earlier, no new code since"

**COUNTER**:
- ❌ Environment may have changed
- ❌ Dependencies may have changed
- ❌ State may be corrupted
- ✅ Fresh verification guarantees current state
- ✅ Hook requires < 5 minutes freshness

**Rule**: Fresh verification always required

---

## Status

**Implementation Status**: ✅ Ready for hook integration
**Version**: 5.4.0
**Dependencies**: None
**MCP Required**: Serena (required for hook enforcement)
**Hook Integration**: post_tool_use.py enhancement required

---

**The Bottom Line**: Evidence before claims, always. Fresh verification, every time. No completion without proof. Hook-enforced, never optional.
