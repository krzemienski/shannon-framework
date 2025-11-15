# Git Workflow Protocol

**Version:** Shannon V3.5
**Status:** Production
**Last Updated:** November 15, 2025

## Overview

The Git Workflow Protocol defines a strict git workflow with atomic commits. NEVER leave uncommitted changes. NEVER commit unvalidated code. Every commit in your branch should be deployable and represent one validated change.

## Purpose

- **Maintain Clean History**: Each commit represents one logical, validated change
- **Enable Easy Rollback**: Revert specific changes without affecting others
- **Facilitate Code Review**: Small, focused commits are easier to review
- **Ensure Deployability**: Every commit passes all validations
- **Support Debugging**: Bisect through history to find issues

## Core Principles

> **1. Every commit must pass all three validation tiers**
> **2. Every commit must be atomic (one logical change)**
> **3. Never leave uncommitted changes**
> **4. Never commit directly to main/master**
> **5. Always use descriptive commit messages**

## Pre-Execution Checks

Before starting ANY work, perform these mandatory checks:

### 1. Verify Working Directory is Clean

```bash
git status --porcelain
```

**Expected output:** Empty (no output)

**If NOT empty:**
- User has uncommitted changes
- **ACTION:** ABORT and ask user to commit or stash changes

```bash
# Example of dirty working directory
$ git status --porcelain
 M src/index.ts
?? new-file.txt

# ❌ ABORT - User must clean this up first
```

### 2. Verify NOT on Main/Master Branch

```bash
git branch --show-current
```

**Expected output:** Anything EXCEPT `main` or `master`

**If on main/master:**
- **ACTION:** ABORT and create feature branch

```bash
# Example of being on main
$ git branch --show-current
main

# ❌ ABORT - Must create feature branch first
```

### 3. Create Feature Branch

Create a feature branch with a descriptive name following conventional format:

```bash
git checkout -b <type>/<description>
```

#### Branch Name Format

| Type | Use Case | Example |
|------|----------|---------|
| `fix/` | Bug fixes | `fix/ios-offscreen-login` |
| `feat/` | New features | `feat/user-avatar-upload` |
| `perf/` | Performance improvements | `perf/optimize-search-query` |
| `refactor/` | Code refactoring | `refactor/auth-module` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |
| `docs/` | Documentation changes | `docs/add-api-reference` |
| `test/` | Test additions/fixes | `test/add-login-tests` |

#### Good Branch Names

```bash
✅ git checkout -b fix/ios-offscreen-login
✅ git checkout -b feat/user-avatar-upload
✅ git checkout -b perf/optimize-search-query
✅ git checkout -b refactor/extract-auth-module
✅ git checkout -b chore/upgrade-react-18
✅ git checkout -b docs/add-deployment-guide
✅ git checkout -b test/add-integration-tests
```

#### Bad Branch Names

```bash
❌ git checkout -b my-changes        # Not descriptive
❌ git checkout -b updates            # Too vague
❌ git checkout -b john-dev           # Personal, not descriptive
❌ git checkout -b feature            # Missing description
❌ git checkout -b fix                # Missing description
```

## Execution Step Workflow

For EACH logical change (not the entire task), follow this workflow:

### Step 1: Make the Change

Modify, create, or delete files to implement ONE logical change.

**Keep changes atomic:**
- ✅ Add a single feature
- ✅ Fix a single bug
- ✅ Refactor a single module
- ❌ Add multiple unrelated features
- ❌ Fix multiple unrelated bugs

### Step 2: Run Tier 1 Validation (Build, Lint, Types)

```bash
# Example for TypeScript project
npx tsc --noEmit && npx eslint src/ && npm run build
```

**Outcome:**
- **✅ PASS** → Continue to Step 3
- **❌ FAIL** → Rollback and retry

**On failure:**
```bash
# Rollback immediately
git reset --hard HEAD
git clean -fd

# Analyze error, research solution, retry with alternative approach
```

### Step 3: Run Tier 2 Validation (Unit/Integration Tests)

```bash
# Example for TypeScript project
npm test
```

**Outcome:**
- **✅ PASS** → Continue to Step 4
- **❌ FAIL** → Rollback and retry

**On failure:**
```bash
# Rollback immediately
git reset --hard HEAD
git clean -fd

# Analyze test failure, fix root cause, retry
```

### Step 4: Run Tier 3 Validation (Functional - User Perspective)

```bash
# Example for web application
npm run dev &
sleep 5
# Manually test feature in browser
# Verify user can complete intended action
```

**Outcome:**
- **✅ PASS** → Ready to commit (Step 5)
- **❌ FAIL** → Rollback and retry

**On failure:**
```bash
# Rollback immediately
git reset --hard HEAD
git clean -fd

# Analyze why feature doesn't work, research solution, retry
```

### Step 5: Commit Immediately (All Three Tiers Passed)

Once ALL three validation tiers pass, commit IMMEDIATELY:

```bash
# Stage only the files you changed
git add <changed-files>

# Or stage all changes (if you're confident)
git add -A

# Commit with descriptive message (see format below)
git commit -m "<commit-message>"
```

**NEVER delay committing after successful validation.**

## Commit Message Format

Use this structured format for ALL commits:

```
<type>: <one-line summary in imperative mood>

WHY: <reasoning for this change>
WHAT: <specific changes made>
VALIDATION:
  - Build: PASS
  - Tests: X/X PASS
  - Functional: <what was tested and verified>
```

### Commit Message Components

| Component | Description | Example |
|-----------|-------------|---------|
| `<type>` | fix, feat, perf, refactor, chore, docs, test | `fix:` |
| `<summary>` | One-line summary in imperative mood | `Update login constraints to use safeAreaLayoutGuide` |
| `WHY:` | Why this change was necessary | `Login screen was rendering offscreen on iPhone X+` |
| `WHAT:` | What specifically changed | `Updated LoginViewController.swift lines 45-52` |
| `VALIDATION:` | Proof that all validations passed | See examples below |

### Commit Message Examples

#### Example 1: Bug Fix (iOS)

```
fix: Update login constraints to use safeAreaLayoutGuide

WHY: Login screen was rendering offscreen on iPhone X+ devices
     due to not accounting for safe area insets

WHAT: Updated LoginViewController.swift lines 45-52 to use
      view.safeAreaLayoutGuide.topAnchor instead of view.topAnchor
      for constraint anchoring

VALIDATION:
  - Build: 0 errors, 0 warnings
  - Tests: 12/12 XCTest PASS
  - Functional: Launched in iPhone 14 simulator, login screen
    visible and properly positioned, login button tappable
```

#### Example 2: New Feature (Web)

```
feat: Add user avatar upload with image resizing

WHY: Users need ability to upload and display profile pictures

WHAT: Created AvatarUpload.tsx component with drag-and-drop,
      image preview, and automatic resizing to 3 sizes (thumbnail,
      medium, large) using sharp library

VALIDATION:
  - Build: npm run build PASS
  - Tests: 8/8 Jest tests PASS (upload, resize, display)
  - Functional: Started dev server, uploaded test.jpg via UI,
    verified 3 sizes created, avatar displayed correctly in profile
```

#### Example 3: Performance Optimization (Database)

```
perf: Add GIN trigram index for user search query

WHY: User search endpoint was slow (850ms average) due to
     full table scan with ILIKE on unindexed columns

WHAT: Created migration adding GIN trigram index on users.username
      and users.email columns for fast ILIKE pattern matching

VALIDATION:
  - Build: pytest --collect-only PASS
  - Tests: 45/45 pytest PASS
  - Functional: EXPLAIN ANALYZE confirms index usage, performance
    benchmark shows 847ms → 2.8ms (302x faster)
```

#### Example 4: Refactoring

```
refactor: Extract authentication logic into AuthService

WHY: Authentication code scattered across multiple components,
     making it hard to maintain and test

WHAT: Created services/AuthService.ts and moved login, logout,
      register, and token refresh logic from components into
      centralized service with clear API

VALIDATION:
  - Build: npx tsc --noEmit PASS, 0 errors
  - Tests: 23/23 Jest tests PASS, coverage 95% → 97%
  - Functional: All auth flows work (login, logout, register),
    verified in dev environment
```

#### Example 5: Chore (Dependencies)

```
chore: Upgrade React from 18.2.0 to 18.3.1

WHY: Security vulnerability CVE-2024-XXXXX in React 18.2.0
     requires upgrade to 18.3.1

WHAT: Updated package.json React version, ran npm install,
      updated React types

VALIDATION:
  - Build: npm run build PASS, 0 deprecation warnings
  - Tests: 156/156 Jest tests PASS, no breaking changes
  - Functional: Smoke tested all major features, no regressions
```

#### Example 6: Documentation

```
docs: Add API authentication guide

WHY: New developers frequently ask how to authenticate API requests

WHAT: Created docs/api/authentication.md with step-by-step guide,
      code examples for JWT tokens, refresh flow, and error handling

VALIDATION:
  - Build: Markdown lint PASS
  - Tests: N/A (documentation)
  - Functional: Followed guide steps myself, successfully authenticated
    and made API calls using documented approach
```

### Commit Message Best Practices

**DO:**
- ✅ Use imperative mood ("Add feature", not "Added feature")
- ✅ Keep summary line under 72 characters
- ✅ Explain WHY the change was needed
- ✅ Include specific file/line numbers when helpful
- ✅ Document all three validation tiers
- ✅ Be specific about what was tested

**DON'T:**
- ❌ Use vague summaries ("Fix bug", "Update code")
- ❌ Skip the WHY section
- ❌ Omit validation details
- ❌ Use past tense ("Fixed bug")
- ❌ Include unrelated changes

## Rollback on Failure

If ANY validation tier fails, follow this procedure:

### 1. Immediately Rollback

```bash
# Reset to last commit (discards all changes)
git reset --hard HEAD

# Remove untracked files and directories
git clean -fd
```

**Warning:** `git reset --hard` is destructive. All uncommitted changes are LOST.

### 2. Verify Clean State

```bash
# Should show nothing
git status --porcelain
```

**Expected:** Empty output (clean working directory)

### 3. Analyze the Failure

Ask yourself:
- What validation tier failed?
- What was the error message?
- Why did it fail?
- What was I trying to accomplish?

**Document the failure:**
```markdown
## Failure Analysis

**Tier:** Tier 3 (Functional)
**Error:** Login button not responsive
**Cause:** Event handler not attached after refactor
**Fix:** Add onClick handler back to LoginButton component
```

### 4. Research Solution (If Unfamiliar Error)

- Check error message in Stack Overflow
- Review library documentation
- Search GitHub issues
- Check project's existing patterns

### 5. Create Alternative Approach

Based on research, create a new approach:

**Example:**
```
Attempt 1 (FAILED): Used custom CSS for layout
→ Layout broke on mobile devices

Attempt 2 (TRYING): Use Flexbox for responsive layout
→ Should work across all screen sizes
```

### 6. Retry with New Approach (Max 3 Attempts)

Retry the change with your new approach.

**Track attempts:**
```markdown
## Attempts Log

1. ❌ Custom CSS grid → Layout broke on mobile
2. ❌ CSS float → Elements overlapped
3. ✅ Flexbox → Works on all screen sizes
```

### 7. Escalate if 3 Attempts Fail

If 3 attempts all fail, escalate to user with detailed failure report:

```markdown
## Escalation Report

**Task:** Add responsive navigation menu
**Attempts:** 3
**Status:** BLOCKED

**Attempt 1:**
- Approach: Custom CSS grid
- Result: Layout broke on mobile devices
- Error: Elements rendering off-screen

**Attempt 2:**
- Approach: CSS float
- Result: Elements overlapped
- Error: z-index conflicts

**Attempt 3:**
- Approach: Flexbox
- Result: Works on desktop but menu not closing on mobile
- Error: Click handler not firing on mobile

**Request:**
Need guidance on mobile menu implementation approach.
Should I use a UI library (e.g., Headless UI) or continue
with custom implementation?
```

## Post-Execution Summary

After completing ALL work (all steps done), provide a summary:

### 1. Verify All Commits Validated

```bash
# View commit history
git log --oneline

# Example output:
# a1b2c3d fix: Update login constraints to use safeAreaLayoutGuide
# d4e5f6g feat: Add user avatar upload with image resizing
# g7h8i9j perf: Add GIN trigram index for user search query
```

Each commit should have passed ALL validations (documented in commit message).

### 2. Branch Ready for PR

```bash
# Push branch to remote
git push origin <branch-name>

# Create PR (if gh CLI available)
gh pr create --title "Implement user profile features" \
  --body "Fixes #123. Adds avatar upload, profile editing, and search optimization."
```

### 3. Report to User

Provide a comprehensive summary:

```markdown
## Execution Complete ✅

**Branch:** feat/user-profile-features
**Commits:** 3
**All Validations:** PASS

**What Was Accomplished:**
1. Fixed login screen layout on iPhone X+ devices
2. Added user avatar upload with automatic image resizing
3. Optimized user search query (302x faster)

**Validation Summary:**
- Tier 1 (Static): PASS on all commits
- Tier 2 (Tests): PASS (67/67 tests, 95% coverage)
- Tier 3 (Functional): PASS (all features verified working)

**Ready for:**
- Code review
- Pull request to main
- Deployment to staging

**Branch:** feat/user-profile-features
**Remote:** git@github.com:yourorg/yourrepo.git
```

## Strict Rules (NO EXCEPTIONS)

### NEVER Do These

❌ **NEVER leave uncommitted changes**
- Commit after every validated change
- Don't accumulate multiple changes

❌ **NEVER commit code that hasn't passed ALL three validation tiers**
- No shortcuts
- No "I'll fix it later"

❌ **NEVER make multiple unrelated changes before validating**
- Keep changes atomic
- Validate after each logical change

❌ **NEVER skip validation "because it's a small change"**
- Small changes can cause big problems
- Always validate

❌ **NEVER force push or rewrite history**
- Keep atomic commit history intact
- No `git push --force` (unless absolutely necessary and discussed)

❌ **NEVER commit directly to main/master**
- Always use feature branches
- Use pull requests for code review

### ALWAYS Do These

✅ **ALWAYS validate before committing (Tier 1 + 2 + 3)**
- No exceptions
- All three tiers must pass

✅ **ALWAYS rollback failed changes immediately**
- `git reset --hard`
- Don't leave broken code uncommitted

✅ **ALWAYS create descriptive commit messages**
- Include WHY, WHAT, VALIDATION
- Future you will thank present you

✅ **ALWAYS commit immediately after successful validation**
- Don't delay
- Atomic commits

✅ **ALWAYS use feature branches**
- Never commit to main/master directly
- Create branch per task/feature

✅ **ALWAYS document validation in commit message**
- Proof that code works
- Helps reviewers

## Workflow Comparison

### ❌ Bad Workflow (Avoid This)

```bash
# 1. Make 10 changes across multiple files
# 2. Don't validate incrementally
# 3. Try to validate everything at once
# 4. Something fails, not sure what
# 5. Spend hours debugging
# 6. Give up, revert everything
# 7. Start over
```

**Problems:**
- Hard to debug (what change caused the failure?)
- Wastes time
- Loses progress
- No atomic commits

### ✅ Good Workflow (Follow This)

```bash
# 1. Create feature branch
git checkout -b fix/ios-login-layout

# 2. Make ONE small change
# Update LoginViewController.swift lines 45-52

# 3. Validate Tier 1
swiftlint && xcodebuild -scheme MyApp
# ✅ PASS

# 4. Validate Tier 2
xcodebuild test -scheme MyApp
# ✅ PASS: 12/12 tests

# 5. Validate Tier 3
# Boot simulator, launch app, verify login screen works
# ✅ PASS: Login screen visible and functional

# 6. Commit immediately
git add LoginViewController.swift
git commit -m "fix: Update login constraints to use safeAreaLayoutGuide

WHY: Login screen was rendering offscreen on iPhone X+ devices
     due to not accounting for safe area insets

WHAT: Updated LoginViewController.swift lines 45-52 to use
      view.safeAreaLayoutGuide.topAnchor instead of view.topAnchor

VALIDATION:
  - Build: 0 errors, 0 warnings
  - Tests: 12/12 XCTest PASS
  - Functional: Launched in iPhone 14 simulator, login works"

# 7. Make NEXT change
# Repeat process for avatar upload feature

# Result: Clean history with atomic, validated commits
```

## Common Scenarios

### Scenario 1: Multiple Related Changes

**Wrong Approach:**
```bash
# Make 5 related changes
# Validate once
# Commit once with "Updated authentication module"
```

**Right Approach:**
```bash
# Change 1: Extract auth service
# Validate, commit: "refactor: Extract auth logic to AuthService"

# Change 2: Add token refresh
# Validate, commit: "feat: Add automatic token refresh"

# Change 3: Update login component
# Validate, commit: "refactor: Update LoginForm to use AuthService"

# Change 4: Add logout
# Validate, commit: "feat: Add logout functionality"

# Change 5: Add tests
# Validate, commit: "test: Add AuthService unit tests"

# Result: 5 atomic commits, easy to review and revert if needed
```

### Scenario 2: Validation Fails

```bash
# Make change
# Validate Tier 1 → PASS
# Validate Tier 2 → FAIL (test failure)

# Rollback immediately
git reset --hard HEAD
git clean -fd

# Analyze test failure
# Turns out: Broke existing feature

# New approach: Update feature, update test
# Validate again → PASS
# Commit
```

### Scenario 3: Feature Requires Multiple Steps

```bash
# Task: Add user avatar upload

# Step 1: Create database migration
git checkout -b feat/user-avatar-upload
# Create migration file
# Validate all tiers → PASS
git add migrations/
git commit -m "feat: Add avatar_url column to users table..."

# Step 2: Add backend endpoint
# Create POST /api/users/avatar endpoint
# Validate all tiers → PASS
git add src/api/
git commit -m "feat: Add avatar upload endpoint..."

# Step 3: Add frontend component
# Create AvatarUpload.tsx
# Validate all tiers → PASS
git add src/components/
git commit -m "feat: Add AvatarUpload component..."

# Step 4: Wire up everything
# Connect component to API
# Validate all tiers → PASS
git add src/pages/
git commit -m "feat: Integrate avatar upload in profile page..."

# Result: 4 atomic commits, each validated and deployable
```

## Git History Best Practices

### Good Git History

```bash
$ git log --oneline
a1b2c3d feat: Integrate avatar upload in profile page
d4e5f6g feat: Add AvatarUpload component with preview
g7h8i9j feat: Add avatar upload endpoint with S3 storage
j1k2l3m feat: Add avatar_url column to users table
m4n5o6p fix: Update login constraints for safe area
```

**Properties:**
- Each commit is descriptive
- Each commit represents one logical change
- Each commit passed all validations
- Easy to review
- Easy to revert specific changes

### Bad Git History

```bash
$ git log --oneline
a1b2c3d WIP
d4e5f6g fix stuff
g7h8i9j more changes
j1k2l3m updates
m4n5o6p asdf
```

**Problems:**
- No idea what changed
- Multiple unrelated changes per commit
- Unknown validation status
- Hard to review
- Hard to revert

## Emergency Procedures

### If You Accidentally Committed to Main/Master

```bash
# DON'T PANIC

# 1. Check if pushed to remote
git log origin/main..main

# 2a. If NOT pushed yet (safe)
# Reset to origin/main
git reset --hard origin/main

# Create proper feature branch
git checkout -b fix/accidental-commit

# Cherry-pick the commit
git cherry-pick <commit-hash>

# 2b. If ALREADY pushed (requires care)
# Contact team, coordinate revert
git revert <commit-hash>
git push origin main
```

### If You Need to Undo Last Commit (Not Pushed)

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Review changes
git status

# Make corrections, re-commit with better message
git add .
git commit -m "Better commit message"
```

### If You Need to Undo Last Commit (Already Pushed)

```bash
# Create revert commit (safe)
git revert HEAD
git push origin <branch-name>
```

## Tools and Automation

### Pre-commit Hooks

Automate Tier 1 + 2 validation with git hooks:

```bash
# .husky/pre-commit (using Husky)
#!/bin/bash

echo "Running Tier 1 validation..."
npm run lint
npm run type-check
npm run build

echo "Running Tier 2 validation..."
npm test

# If any command fails, commit is blocked
```

### Commit Message Template

```bash
# Create template
cat > ~/.gitmessage <<EOL
<type>: <summary>

WHY:
WHAT:
VALIDATION:
  - Build:
  - Tests:
  - Functional:
EOL

# Configure git to use template
git config --global commit.template ~/.gitmessage
```

### Validation Scripts

Create reusable validation scripts:

```bash
# scripts/validate.sh
#!/bin/bash
set -e

echo "🔍 Tier 1: Static Validation..."
npm run lint
npm run type-check
npm run build
echo "✅ Tier 1 PASS"

echo "🧪 Tier 2: Tests..."
npm test
echo "✅ Tier 2 PASS"

echo "🚀 Tier 3: Manual validation required"
echo "Start dev server and test functionality"
npm run dev
```

## Summary

The Git Workflow Protocol ensures:

1. **Clean working directory** at all times
2. **Feature branches** for all work
3. **Atomic commits** (one logical change per commit)
4. **Validated commits** (all three tiers pass)
5. **Descriptive commit messages** (WHY, WHAT, VALIDATION)
6. **Easy rollback** on validation failures
7. **PR-ready branches** with deployable commits

**Remember:**
- Commit after every validated change
- Never leave uncommitted changes
- Never skip validation
- Use descriptive commit messages
- Keep commit history clean and atomic

**Result:**
- Every commit in your branch is deployable
- Easy code review (one change per commit)
- Easy debugging (bisect through atomic commits)
- Easy revert (revert specific commit without affecting others)

---

**Related Protocols:**
- [Library Discovery Protocol](./LIBRARY_DISCOVERY_PROTOCOL.md) - Research before building
- [Functional Validation Protocol](./FUNCTIONAL_VALIDATION_PROTOCOL.md) - Three-tier validation
