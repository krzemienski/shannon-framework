---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, passing, or successful, before committing or creating PRs - requires running verification commands and confirming output before making ANY success claims; evidence before assertions always, no exceptions
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle**: Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| All validations pass | 3-tier validation output | Individual tiers passed separately |

## Shannon Enhancement: Validation Gates

**Shannon-specific**: Projects have 3-tier validation gates:

### Tier 1: Flow Validation
**Purpose**: Code compiles, dependencies resolve, syntax correct

**Common commands**:
- TypeScript: `tsc --noEmit`
- Python: `ruff check .` or `flake8 .`
- Go: `go vet ./...`
- Rust: `cargo check`

**Required output**: 0 errors, 0 warnings (zero tolerance)

### Tier 2: Artifact Validation
**Purpose**: Tests pass, builds succeed, artifacts created

**Common commands**:
- Tests: `npm test`, `pytest`, `go test ./...`, `cargo test`
- Build: `npm run build`, `cargo build --release`

**Required output**:
- Tests: X/X pass, 0 failures, 0 skipped (without reason)
- Build: exit 0, artifacts created

### Tier 3: Functional Validation
**Purpose**: Real system behavior verified (NO MOCKS)

**Shannon requirement**: Tests must use real systems:
- Web: Puppeteer/Playwright against real browser
- Mobile: iOS Simulator/Android Emulator
- Database: Real database instance (not mocked)
- API: Real HTTP calls (not mocked fetch)

**Required evidence**:
- Browser screenshot (Puppeteer)
- Simulator logs (iOS Simulator MCP)
- Actual HTTP responses (not mocked)

## Verification Workflow

### Step 1: Identify Required Verifications

**Based on work type**:
- New feature → All 3 tiers
- Bug fix → Tier 2 + Tier 3 (functional must reproduce then pass)
- Refactor → All 3 tiers (especially regression tests)
- Documentation → Build/deploy test

**Auto-detect gates**:
```python
# Shannon detects validation gates from project
gates = detect_validation_gates(project_path)
# Returns: {
#   "tier1": ["tsc --noEmit", "ruff check ."],
#   "tier2": ["npm test", "npm run build"],
#   "tier3": ["npm run test:e2e"]
# }
```

### Step 2: Run Verifications (Fresh)

**MANDATORY: Fresh execution in this message**.

**Not acceptable**:
- ❌ "Tests passed earlier"
- ❌ "I ran this before making the claim"
- ❌ "Output looks good from previous run"

**REQUIRED**:
- ✅ Run command NOW
- ✅ Wait for complete output
- ✅ Capture exit code
- ✅ Read ALL output lines

### Step 3: Parse Results (Quantitative)

**Shannon requirement**: Quantitative reporting.

**Good examples**:
```
✅ Tier 1 (Flow): tsc --noEmit
   Exit code: 0
   Errors: 0
   Warnings: 0
   Status: PASS

✅ Tier 2 (Artifacts): npm test
   Exit code: 0
   Tests: 34/34 pass
   Failures: 0
   Skipped: 0
   Duration: 2.3s
   Status: PASS

✅ Tier 3 (Functional): npm run test:e2e
   Exit code: 0
   Browser tests: 12/12 pass
   Screenshots captured: 12
   Real browser: Chrome
   Status: PASS (NO MOCKS verified)
```

**Bad examples**:
```
❌ "Tests passed"
❌ "Build looks good"
❌ "Everything works"
❌ "Linter is clean"
```

### Step 4: Make Claim (With Evidence)

**Format**:
```markdown
## Verification Complete

[Evidence from steps above]

**Claim**: All validations pass. Work is complete.
**Evidence**: 3/3 tiers verified above.
**Ready for**: Commit / PR / Deployment
```

## Red Flags - STOP

If you catch yourself about to:
- Use "should", "probably", "seems to"
- Express satisfaction before verification ("Great!", "Perfect!", "Done!")
- Commit/push/PR without verification
- Trust agent success reports
- Rely on partial verification
- Think "just this once"
- Feel tired and want work over
- Use ANY wording implying success without having run verification

**ALL OF THESE MEAN**: STOP. Run verifications. THEN claim.

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Shannon-Specific Patterns

### NO MOCKS Verification

**MANDATORY for Tier 3**: Verify tests use real systems.

**Check for violations**:
```python
# Scan test files for mock imports
violations = grep_r("import.*mock|from.*mock|jest.mock", "tests/")

if violations:
    ERROR: "MOCK VIOLATION: Tests use mocking"
    EVIDENCE: [list violations]
    STATUS: FAIL (Shannon NO MOCKS requirement violated)
```

**Acceptable real systems**:
- ✅ Puppeteer (`await page.goto(...)`)
- ✅ iOS Simulator MCP (`ios_simulator.launch_app(...)`)
- ✅ Real database (`await db.connect(...)`)
- ✅ Real HTTP (`await fetch(actual_url)`)

**NOT acceptable**:
- ❌ `jest.mock('puppeteer')`
- ❌ `unittest.mock.patch(...)`
- ❌ `sinon.stub(...)`
- ❌ In-memory fake database

### Regression Test Verification

**MANDATORY for bug fixes**: Prove test catches the bug.

**RED-GREEN cycle**:
```
1. Write test reproducing bug
2. Run test → MUST FAIL with bug present
3. Fix bug
4. Run test → MUST PASS with fix
5. Revert fix (temporarily)
6. Run test → MUST FAIL again (proves test works)
7. Restore fix
8. Run test → MUST PASS (final verification)
```

**Required evidence**:
```markdown
## Regression Test Verification

✅ RED: Test failed with bug present
   Output: [failure message matching bug symptom]

✅ GREEN: Test passed with fix
   Output: [success]

✅ RED (reverified): Test failed with fix reverted
   Output: [same failure as step 1]

✅ GREEN (final): Test passed with fix restored
   Output: [success]

**Claim**: Regression test verified via RED-GREEN cycle.
**Evidence**: 4/4 phases above.
```

### Validation Gates Reporting

**Format for Shannon 3-tier validation**:
```markdown
## Shannon Validation Gates

| Tier | Gate | Command | Result | Evidence |
|------|------|---------|--------|----------|
| 1 (Flow) | TypeScript | `tsc --noEmit` | ✅ PASS | 0 errors, 0 warnings |
| 1 (Flow) | Linter | `ruff check .` | ✅ PASS | 0 errors, 0 warnings |
| 2 (Artifacts) | Tests | `pytest` | ✅ PASS | 45/45 pass, 0 failures |
| 2 (Artifacts) | Build | `npm run build` | ✅ PASS | exit 0, dist/ created |
| 3 (Functional) | E2E | `npm run test:e2e` | ✅ PASS | 8/8 pass, real browser |

**Overall**: 5/5 gates PASS
**NO MOCKS**: Verified (Tier 3 uses Puppeteer)
**Status**: READY FOR COMMIT
```

## Integration with Shannon Commands

**Commands that require this skill**:

**/shannon:do**: Before claiming task complete:
```
1. Run all validation gates
2. Verify 3/3 tiers pass
3. Check NO MOCKS compliance
4. THEN claim completion
```

**/shannon:wave**: Before marking wave complete:
```
1. Run validation gates for wave
2. Verify all tasks' tests pass
3. Check NO MOCKS compliance
4. THEN report wave success
```

**/shannon:execute-plan**: After each batch:
```
1. Run gates for batch
2. Verify tier results
3. Quantitative reporting
4. THEN proceed to next batch
```

## Integration with Other Skills

**This skill is prerequisite for**:
- **executing-plans** - Verify before claiming batch complete
- **wave-orchestration** - Verify before claiming wave complete
- **systematic-debugging** - Verify fix worked (Phase 4)

**Complementary skills**:
- **test-driven-development** - Verification ensures RED-GREEN cycle worked
- **defense-in-depth** - Multiple verification layers
- **forced-reading-protocol** - Both enforce thoroughness over speed

## Example: Complete Workflow

**Scenario**: Bug fix for authentication

**Work done**:
- Fixed middleware validation
- Added regression test
- Updated documentation

**Verification**:
```markdown
## Verification Report

### Tier 1: Flow Validation

**TypeScript Check**:
```bash
$ tsc --noEmit
# (no output)
```
Exit code: 0
Errors: 0
Warnings: 0
✅ PASS

**Linter Check**:
```bash
$ ruff check .
All checks passed!
```
Exit code: 0
Issues: 0
✅ PASS

### Tier 2: Artifact Validation

**Unit Tests**:
```bash
$ pytest tests/
====== 67 passed in 3.42s ======
```
Exit code: 0
Tests: 67/67 pass
Failures: 0
Duration: 3.42s
✅ PASS

**Build**:
```bash
$ npm run build
Build successful. Output: dist/
```
Exit code: 0
Artifacts: dist/ created (2.3 MB)
✅ PASS

### Tier 3: Functional Validation

**E2E Tests (NO MOCKS)**:
```bash
$ npm run test:e2e:auth
  ✓ User login with valid credentials (browser)
  ✓ User login with invalid credentials (browser)
  ✓ Session persistence (browser)
  ✓ Logout flow (browser)

4 passed (12.5s)
```
Exit code: 0
Tests: 4/4 pass
Real browser: Chromium via Puppeteer
Screenshots: 4 captured
✅ PASS (NO MOCKS verified)

### Regression Test Verification

**RED phase** (bug present):
```bash
$ git stash  # Revert fix temporarily
$ pytest tests/test_auth_middleware.py::test_empty_token
FAILED: Expected 401, got 500
```
✅ Test correctly fails with bug

**GREEN phase** (fix applied):
```bash
$ git stash pop  # Restore fix
$ pytest tests/test_auth_middleware.py::test_empty_token
PASSED
```
✅ Test passes with fix

## Summary

| Category | Result | Evidence |
|----------|--------|----------|
| Tier 1 (Flow) | 2/2 PASS | tsc + ruff clean |
| Tier 2 (Artifacts) | 2/2 PASS | 67/67 tests, build succeeded |
| Tier 3 (Functional) | 1/1 PASS | 4/4 E2E, real browser |
| Regression Test | VERIFIED | RED-GREEN cycle complete |
| NO MOCKS | VERIFIED | Puppeteer used, no mocks |

**Overall**: 5/5 validations PASS
**Status**: READY FOR COMMIT

**Claim**: Bug fix verified complete. All gates pass. Ready for deployment.
**Evidence**: Complete verification report above.
```

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

**For mission-critical work**: False completion claims = production failures.

If you follow verification for code reviews, follow it for ALL completion claims.

