---
name: finishing-a-development-branch
description: Use at development completion - guides branch integration with Shannon 3-tier validation (0.00-1.00 readiness score), MCP merge pattern analysis, and Serena risk assessment
---

# Finishing a Development Branch (Shannon-Enhanced)

## Overview

**Structured branch completion with quantitative readiness validation.**

Verify → 3-tier validation → Present options → Execute → Cleanup.

Shannon enhancement: Numerical readiness scoring, merge pattern analysis via MCP, Serena risk assessment.

**Readiness Score (0.00-1.00):**
- 0.00-0.60: Not ready (tests failing, validation incomplete)
- 0.61-0.80: Mostly ready (minor issues, could proceed carefully)
- 0.81-0.95: Ready (validates on all tiers, low risk)
- 0.96-1.00: Excellent (perfect readiness)

## The 3-Tier Validation

### Tier 1: Test Validation

```bash
# Run full test suite
readiness_score_tier1 = 0.0

if test_suite_passes:
  readiness_score_tier1 = 1.0
  log to Serena: {test_count, coverage_pct, duration}
else:
  readiness_score_tier1 = (tests_passed / total_tests)
  log failures: "[list failing tests]"
  STOP: Cannot proceed with Tiers 2-3
```

**GATE:** If Tier 1 < 0.90, must fix before continuing.

### Tier 2: Code Quality Validation

```bash
# Metrics gathering (Serena)
code_quality = {
  files_modified: count,
  lines_added: count,
  lines_deleted: count,
  commits: count,
  test_coverage_change: delta_pct
}

# MCP pattern analysis: compare to historical merges
pattern_match = compare_to_historical_merges({
  scope_size: files_modified,
  change_magnitude: lines_added,
  test_coverage_delta: coverage_change
})

readiness_score_tier2 = pattern_match.risk_assessment_inverse
# 1.0 = safe pattern, 0.0 = high-risk pattern

Log to Serena:
  historical_similar_merges: N (count)
  avg_merge_success_rate: X.XX (from history)
  risk_level: "low|medium|high"
```

**GATE:** If Tier 2 < 0.75, alert but can override.

### Tier 3: Integration Readiness

```bash
# Final checklist validation
integration_checks = {
  base_branch_exists: bool,          # +0.1
  branch_synced_with_base: bool,     # +0.2
  no_conflicting_changes: bool,      # +0.3
  commit_messages_compliant: bool,   # +0.2
  no_breaking_changes_detected: bool # +0.2
}

readiness_score_tier3 = sum(passing_checks) / total_checks
# Range: 0.0-1.0
```

**GATE:** If Tier 3 < 0.80, prompt for manual fixes.

## Overall Readiness Calculation

```
readiness_score = (
  readiness_score_tier1 * 0.5 +  # Tests are mandatory
  readiness_score_tier2 * 0.25 + # Code quality important
  readiness_score_tier3 * 0.25   # Integration critical
)

Range: 0.00-1.00
```

**Interpretation:**
- **< 0.80:** NOT READY - Fix before continuing
- **0.80-0.89:** PROCEED CAREFULLY - Flag potential issues
- **0.90+:** READY - Safe to merge/PR

## Process Steps

### Step 1: Tier 1 Verification (Test Validation)

```bash
# Run project's full test suite
npm test / cargo test / pytest / go test ./...

If tests_fail:
  readiness_score = test_pass_rate
  Report: "[N failing tests]"
  STOP - Cannot proceed to Tiers 2-3
Else:
  readiness_score_tier1 = 1.0
  Continue to Tier 2
```

### Step 2: Tier 2 Validation (Code Quality)

```bash
# MCP pattern analysis
git diff base_branch...HEAD | MCP analyze
  scope_size: files_modified count
  magnitude: lines_added + lines_deleted
  coverage: test coverage delta

# Serena historical comparison
Find similar merges in history
  readiness_score_tier2 = inverse(risk_score)

Log alert if tier2 < 0.75
```

### Step 3: Tier 3 Validation (Integration Readiness)

```bash
# Base branch check
git merge-base HEAD main || git merge-base HEAD master

# Sync check
git status | grep "ahead|behind"

# Conflict check
git merge --no-commit --no-ff base_branch

# Commit message check (conventional commits)
git log base_branch...HEAD --format="%B"

# Calculate tier3_score from checks
```

### Step 4: Calculate Overall Readiness & Present Options

```
Overall readiness_score = [calculated above]

If readiness_score >= 0.90:
  "✓ READY TO INTEGRATE"
Else:
  "⚠ CAUTION NEEDED [score: X.XX]"
  Alert on which tier failed

Present 4 options:
  1. Merge back to <base-branch> locally
  2. Push and create a Pull Request
  3. Keep the branch as-is
  4. Discard this work
```

### Step 5: Execute Choice

**Option 1: Merge Locally**
```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test-command>  # Re-verify Tier 1
git branch -d <feature-branch>
# Cleanup worktree
```

**Option 2: Push and Create PR**
```bash
git push -u origin <feature-branch>
# Create PR with readiness_score in description
gh pr create --title "[readiness: X.XX] Title" \
  --body "Readiness: Tier1=X.XX Tier2=X.XX Tier3=X.XX"
# Keep worktree
```

**Option 3: Keep As-Is**
```
Report: "Keeping branch. Readiness: X.XX"
# Don't cleanup
```

**Option 4: Discard**
```bash
# Confirm first (typed confirmation: "discard")
git checkout <base-branch>
git branch -D <feature-branch>
# Cleanup worktree
```

## Metrics Checklist

- [ ] Tier 1: readiness_score_tier1 calculated (tests pass/fail)
- [ ] Tier 2: MCP pattern analysis, Serena risk assessment done
- [ ] Tier 3: Integration checks passed
- [ ] Overall readiness_score calculated (0.00-1.00)
- [ ] Score > 0.80 for safe merge/PR
- [ ] Choice executed correctly
- [ ] Worktree cleanup done (Options 1, 4 only)

## Common Mistakes

❌ Skip test verification
✅ Always Tier 1 first

❌ Merge with failing tests
✅ Tier 1 must be 1.0

❌ Ignore readiness_score
✅ Alert if score < 0.90

❌ Force push without reason
✅ Only if explicitly requested

## Serena Pattern Learning

Track across all branches:
- Historical readiness_score distributions
- Correlation between Tier 2 risk and actual merge issues
- Which code patterns correlate with merge problems
- Average readiness by change size/scope

Use to improve future predictions.

## Integration

**Called by:**
- **subagent-driven-development** (after all tasks complete)
- **executing-plans** (after all batches complete)

**Pairs with:**
- **using-git-worktrees** (cleans up worktree)

## Real-World Impact

Example branch completion:
- Tier 1: 0.99 (1 flaky test, 98 pass)
- Tier 2: 0.82 (moderate scope, similar history)
- Tier 3: 0.95 (clean integration)
- **readiness_score: 0.92** ✓ Safe to merge
- Historical pattern matched 4 similar merges (100% success)
