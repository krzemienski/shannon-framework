# Functional Validation Protocol

**Version:** Shannon V3.5
**Status:** Production
**Last Updated:** November 15, 2025

## Overview

The Functional Validation Protocol defines a three-tier validation approach that ALL code changes must pass before being committed. This protocol ensures that code doesn't just compile—it actually works from the user's perspective.

## Purpose

- **Prevent Deployment Failures**: Catch issues before they reach production
- **Ensure User Functionality**: Code that compiles but doesn't work is worthless
- **Maintain Code Quality**: Enforce quality gates at every change
- **Reduce Debugging Time**: Catch issues early when context is fresh

## Core Principle

> **Building ≠ Compiling ≠ Working**
>
> Code that compiles and passes tests but doesn't work for users is worthless.
> Tier 3 functional validation is THE most important validation.

## Three-Tier Validation System

ALL code changes MUST pass ALL three tiers before committing. Compiling successfully is NOT enough. The feature must ACTUALLY WORK.

### Tier 1: Static Validation (~10 seconds)

**Purpose:** Catch syntax errors, type errors, and build failures.

**ALL applicable checks MUST pass:**

| Check | Description | Failure Action |
|-------|-------------|----------------|
| ✅ Syntax | Code parses correctly | STOP, fix syntax error |
| ✅ Types | Type checking passes | STOP, fix type errors |
| ✅ Lint | Linter passes | STOP, fix lint violations |
| ✅ Build | Compile/transpile succeeds | STOP, fix build errors |
| ✅ Imports | All imports resolve | STOP, fix import paths |

#### Commands by Project Type

##### TypeScript/JavaScript
```bash
# Type checking
npx tsc --noEmit

# Linting
npx eslint src/

# Build
npm run build

# Combined (recommended)
npx tsc --noEmit && npx eslint src/ && npm run build
```

##### Python
```bash
# Type checking
mypy .

# Linting
ruff check .

# Syntax check
python -m py_compile src/**/*.py

# Combined (recommended)
mypy . && ruff check . && python -m py_compile src/**/*.py
```

##### Swift/iOS
```bash
# Linting
swiftlint

# Build
xcodebuild -scheme MyApp -configuration Debug

# Combined (recommended)
swiftlint && xcodebuild -scheme MyApp
```

##### Rust
```bash
# Linting + static analysis
cargo clippy

# Build
cargo build

# Combined (recommended)
cargo clippy && cargo build
```

##### Java/Android
```bash
# Check + Lint
./gradlew check

# Build
./gradlew build

# Combined (recommended)
./gradlew check build
```

#### Tier 1 Success Criteria

- ✅ Zero syntax errors
- ✅ Zero type errors
- ✅ Zero lint violations (or only warnings, no errors)
- ✅ Build completes successfully
- ✅ All imports resolve correctly

**If ANY Tier 1 check fails → STOP, fix immediately, re-validate. Do NOT proceed to Tier 2.**

---

### Tier 2: Unit & Integration Tests (~1-5 minutes)

**Purpose:** Ensure changes don't break existing functionality and prevent regressions.

**ALL test suites MUST pass:**

| Check | Description | Failure Action |
|-------|-------------|----------------|
| ✅ Unit Tests | Individual component tests | STOP, analyze failure, fix |
| ✅ Integration Tests | Component interaction tests | STOP, analyze failure, fix |
| ✅ Regression Tests | Existing feature verification | STOP, analyze breakage, fix |
| ✅ Coverage | Code coverage maintained/improved | Review uncovered code |

#### Commands by Project Type

##### JavaScript/TypeScript
```bash
# Run all tests
npm test

# With coverage
npm test -- --coverage

# Watch mode (during development)
npm test -- --watch

# Specific test file
npm test -- path/to/test.spec.ts
```

##### Python
```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=src/

# Specific test file
pytest tests/test_calculator.py

# Verbose output
pytest tests/ -v
```

##### Swift/iOS
```bash
# Run tests
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 14'

# Or via xcodebuild
xcodebuild test -scheme MyApp
```

##### Rust
```bash
# Run all tests
cargo test

# With output
cargo test -- --nocapture

# Specific test
cargo test test_name
```

##### Java/Android
```bash
# Run tests
./gradlew test

# Android instrumented tests
./gradlew connectedAndroidTest
```

#### Test Failure Analysis

When tests fail, follow this process:

1. **Read the error message carefully**
   ```
   FAILED tests/test_calculator.py::test_divide - AssertionError: assert 0 == ZeroDivisionError
   ```

2. **Identify the root cause**
   - Is it a regression (broke existing feature)?
   - Is it expected behavior (test needs update)?
   - Is it a bug in the new code?

3. **Fix appropriately**
   - If regression → Revert changes, rethink approach
   - If test needs update → Update test, document why
   - If bug in new code → Fix bug, re-run tests

4. **Verify fix**
   - Re-run failing test: `npm test -- path/to/test.spec.ts`
   - Re-run full suite: `npm test`

#### Tier 2 Success Criteria

- ✅ All unit tests pass (100%)
- ✅ All integration tests pass (100%)
- ✅ No regressions detected
- ✅ Code coverage maintained or improved
- ✅ Test execution time reasonable (<5 minutes)

**If ANY test fails → STOP, analyze failure, fix root cause, re-validate. Do NOT proceed to Tier 3.**

---

### Tier 3: Functional Validation (~2-10 minutes)

**Purpose:** Validate from USER PERSPECTIVE. Can a user actually use this feature?

**THIS IS THE MOST IMPORTANT TIER.**

Code that compiles and passes tests but doesn't work for users is WORTHLESS.

#### Validation Approach by Project Type

##### iOS/macOS Application

**Process:**
```bash
# 1. Boot simulator
xcrun simctl boot "iPhone 14"

# 2. Build and install
xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 14' build

# 3. Launch app
xcrun simctl launch booted com.yourcompany.MyApp
```

**Verify:**
- ✅ App launches without crash
- ✅ UI renders correctly (no layout issues)
- ✅ Feature is accessible (user can navigate to it)
- ✅ Feature works as intended (complete user flow)
- ✅ No console errors or warnings
- ✅ Performance acceptable (no lag, smooth animations)

**Example: Login Screen Validation**
```bash
# Boot simulator
xcrun simctl boot "iPhone 14"

# Build and run
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 14'

# Manual verification:
# 1. Login screen visible? ✅
# 2. Email field tappable? ✅
# 3. Password field tappable? ✅
# 4. Login button tappable? ✅
# 5. Keyboard appears? ✅
# 6. Login succeeds with valid credentials? ✅
# 7. Error shows for invalid credentials? ✅
# 8. Navigation to home screen works? ✅
```

##### Web Application (Frontend)

**Process:**
```bash
# 1. Start dev server
npm run dev &
SERVER_PID=$!

# 2. Wait for startup
sleep 5

# 3. Health check
curl http://localhost:3000

# 4. If health check passes, server is ready
```

**Verify:**
- ✅ Server starts without errors
- ✅ Page loads in browser
- ✅ UI renders correctly
- ✅ Feature is visible and accessible
- ✅ User interactions work (click, type, submit)
- ✅ Expected behavior occurs (success message, data saved, UI updates)
- ✅ No console errors
- ✅ Network requests succeed

**Example: User Profile Page Validation**
```bash
# Start dev server
npm run dev &

# Wait for startup
sleep 5

# Check server responds
curl -I http://localhost:3000/profile

# Manual verification in browser:
# 1. Navigate to /profile ✅
# 2. Profile data loads and displays ✅
# 3. Avatar upload button visible ✅
# 4. Click upload, select file ✅
# 5. Image preview appears ✅
# 6. Click save ✅
# 7. Success message displays ✅
# 8. Avatar updates in header ✅
# 9. Check browser console: 0 errors ✅

# Cleanup
kill $SERVER_PID
```

##### Web Application (Backend/API)

**Process:**
```bash
# 1. Start server
uvicorn main:app --reload &
SERVER_PID=$!

# 2. Wait for startup
sleep 3

# 3. Health check
curl http://localhost:8000/health

# 4. Test endpoint
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test1234!"}'
```

**Verify:**
- ✅ Server starts without errors
- ✅ Health endpoint responds (200 OK)
- ✅ API endpoint responds correctly
- ✅ Response has correct structure
- ✅ Response contains expected data
- ✅ Database records created (if applicable)
- ✅ Error handling works (invalid input → 400/422)

**Example: User Registration Endpoint Validation**
```bash
# Start server
uvicorn main:app --reload &
SERVER_PID=$!

# Wait for startup
sleep 3

# Test successful registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }' | jq '.'

# Expected: 201 Created, returns user object with id
# ✅ Status: 201
# ✅ Response: {"id": 1, "email": "newuser@example.com", "name": "Test User"}

# Test duplicate email (should fail)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "AnotherPass123!",
    "name": "Duplicate User"
  }' | jq '.'

# Expected: 400 Bad Request, error message
# ✅ Status: 400
# ✅ Response: {"detail": "Email already registered"}

# Test weak password (should fail)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "another@example.com",
    "password": "weak",
    "name": "Another User"
  }' | jq '.'

# Expected: 422 Unprocessable Entity
# ✅ Status: 422
# ✅ Response: {"detail": [{"loc": ["body", "password"], "msg": "Password must be at least 8 characters"}]}

# Verify database record
psql -d myapp -c "SELECT * FROM users WHERE email='newuser@example.com';"
# ✅ Record exists with correct data

# Cleanup
kill $SERVER_PID
```

##### Database Changes

**Process:**
```bash
# 1. Run migration
alembic upgrade head

# 2. Verify schema
psql -d myapp -c "\d users"

# 3. Test query
psql -d myapp -c "SELECT * FROM users LIMIT 1;"

# 4. Performance check
psql -d myapp -c "EXPLAIN ANALYZE SELECT * FROM users WHERE email='test@example.com';"
```

**Verify:**
- ✅ Migration runs without errors
- ✅ Table/column exists in schema
- ✅ Constraints work correctly
- ✅ Indexes exist and are used
- ✅ Query returns expected data
- ✅ Performance acceptable (query time < target)
- ✅ Data integrity maintained

**Example: Add User Email Index**
```bash
# Run migration
alembic upgrade head
# ✅ No errors

# Verify index exists
psql -d myapp -c "\d users"
# ✅ Index "idx_users_email" exists

# Test query uses index
psql -d myapp -c "EXPLAIN ANALYZE SELECT * FROM users WHERE email='test@example.com';"
# ✅ Output shows "Index Scan using idx_users_email"
# ✅ Query time: 0.123ms (< 100ms target)

# Test email uniqueness constraint
psql -d myapp -c "INSERT INTO users (email, name) VALUES ('duplicate@example.com', 'User 1');"
# ✅ Success

psql -d myapp -c "INSERT INTO users (email, name) VALUES ('duplicate@example.com', 'User 2');"
# ✅ Error: duplicate key value violates unique constraint "idx_users_email"
```

##### React Native/Expo

**Process:**
```bash
# 1. Start Metro bundler
npx expo start &
METRO_PID=$!

# 2. Open in Expo Go or simulator
# Scan QR code with Expo Go app
# Or press 'i' for iOS simulator

# 3. Wait for bundle to load
sleep 10
```

**Verify:**
- ✅ App loads without errors
- ✅ Feature screen accessible
- ✅ UI renders correctly
- ✅ Touch interactions work (tap, swipe)
- ✅ Text input works
- ✅ Navigation works
- ✅ Data persists (if applicable)
- ✅ No red screen errors

**Example: Profile Edit Screen Validation**
```bash
# Start Metro
npx expo start &

# Open in iOS simulator (press 'i' when prompted)

# Manual verification:
# 1. Navigate to Profile tab ✅
# 2. Tap "Edit Profile" button ✅
# 3. Edit Profile screen opens ✅
# 4. Name field shows current name ✅
# 5. Tap name field, keyboard appears ✅
# 6. Type new name ✅
# 7. Tap "Save" button ✅
# 8. Loading indicator shows ✅
# 9. Success toast appears ✅
# 10. Navigate back to profile ✅
# 11. New name displays ✅
# 12. Close and reopen app ✅
# 13. New name persists ✅
```

##### Performance Optimization

**Process:**
```bash
# 1. Benchmark BEFORE changes
# Record baseline performance

# 2. Apply changes

# 3. Benchmark AFTER changes
# Measure improvement

# 4. Compare results
# Calculate speedup
```

**Verify:**
- ✅ Performance meets target
- ✅ Improvement measurable
- ✅ No regressions elsewhere
- ✅ Resource usage acceptable (CPU, memory)

**Example: Database Query Optimization**
```bash
# BEFORE: Benchmark current query
psql -d myapp -c "EXPLAIN ANALYZE SELECT * FROM users WHERE username ILIKE '%john%';"
# Result: Seq Scan on users (cost=0.00..1823.50) Time: 847.234 ms

# Apply change: Add GIN trigram index
psql -d myapp -c "CREATE INDEX idx_users_username_trgm ON users USING gin(username gin_trgm_ops);"

# AFTER: Benchmark optimized query
psql -d myapp -c "EXPLAIN ANALYZE SELECT * FROM users WHERE username ILIKE '%john%';"
# Result: Bitmap Index Scan using idx_users_username_trgm (cost=12.25..84.50) Time: 2.809 ms

# Calculate improvement
# Before: 847.234ms
# After: 2.809ms
# Speedup: 302x faster (847.234 / 2.809 = 301.6)
# ✅ Meets target (<100ms)
```

#### Using Available Tools for Validation

Leverage available tools and MCPs for Tier 3 validation:

| Tool | Use Case | Example |
|------|----------|---------|
| `Bash` | Launch apps, start servers, run tests | `npm run dev` |
| `firecrawl` | Scrape and verify web pages | Verify content rendered |
| `puppeteer` | Browser automation, screenshots | Automate UI testing |
| `playwright` | End-to-end testing | Full user flow testing |
| `curl` / `httpx` | HTTP endpoint testing | API validation |
| `simctl` | iOS simulator control | Launch, interact with iOS apps |

**Example: Automated Web App Validation with Playwright**
```typescript
// validation.spec.ts
import { test, expect } from '@playwright/test';

test('user can upload and save profile avatar', async ({ page }) => {
  // Navigate to profile page
  await page.goto('http://localhost:3000/profile');

  // Verify upload button visible
  await expect(page.locator('[data-testid="avatar-upload"]')).toBeVisible();

  // Upload file
  await page.setInputFiles('[data-testid="avatar-upload"]', 'test-avatar.jpg');

  // Verify preview appears
  await expect(page.locator('[data-testid="avatar-preview"]')).toBeVisible();

  // Click save
  await page.click('[data-testid="save-button"]');

  // Verify success message
  await expect(page.locator('.success-toast')).toContainText('Avatar updated');

  // Verify avatar updated in header
  const headerAvatar = page.locator('[data-testid="header-avatar"]');
  await expect(headerAvatar).toHaveAttribute('src', /test-avatar/);
});
```

```bash
# Run validation
npx playwright test validation.spec.ts

# Result: ✅ 1 passed
```

#### Tier 3 Success Criteria

**ALL criteria MUST be met:**

- ✅ Application starts without errors
- ✅ Feature is accessible (user can find and navigate to it)
- ✅ Feature works as intended (user can complete the intended action)
- ✅ No console errors or warnings
- ✅ Expected behavior observed (data saved, UI updated, correct output)
- ✅ Performance meets requirements (if optimization)
- ✅ User experience is smooth (no lag, crashes, or confusion)

**If Tier 3 fails → This is a REAL problem. The feature doesn't work for users.**

Analysis process:
1. What specifically failed?
2. Why did it fail?
3. Is there an error message?
4. Research solution (check docs, Stack Overflow, GitHub issues)
5. Try alternative approach
6. Re-validate

---

## Validation Workflow Summary

```
Code Change Made
    ↓
Run Tier 1: Static Validation
    ↓
PASS? → Continue
FAIL? → Fix errors, re-run Tier 1
    ↓
Run Tier 2: Tests
    ↓
PASS? → Continue
FAIL? → Analyze, fix, re-run Tier 2
    ↓
Run Tier 3: Functional Validation
    ↓
PASS? → Ready to commit ✅
FAIL? → Analyze, research, fix, re-run Tier 3
```

## Common Validation Scenarios

### Scenario 1: Frontend Component Change

```bash
# Tier 1: Static
npx tsc --noEmit && npx eslint src/ && npm run build
# ✅ PASS

# Tier 2: Tests
npm test
# ✅ PASS: 45/45 tests

# Tier 3: Functional
npm run dev &
sleep 5
curl http://localhost:3000
# Open browser, navigate to component
# Test user interactions
# ✅ PASS: Component works as expected

# Ready to commit ✅
```

### Scenario 2: Backend API Endpoint

```bash
# Tier 1: Static
mypy . && ruff check . && python -m py_compile src/**/*.py
# ✅ PASS

# Tier 2: Tests
pytest tests/ --cov=src/
# ✅ PASS: 67/67 tests, 92% coverage

# Tier 3: Functional
uvicorn main:app --reload &
sleep 3
curl -X POST http://localhost:8000/api/users -d '{"email":"test@example.com"}'
# ✅ PASS: 201 Created, correct response

# Ready to commit ✅
```

### Scenario 3: Database Migration

```bash
# Tier 1: Static
python -m py_compile migrations/*.py
# ✅ PASS

# Tier 2: Tests
pytest tests/test_migrations.py
# ✅ PASS: 12/12 tests

# Tier 3: Functional
alembic upgrade head
psql -d myapp -c "\d users"
# ✅ PASS: New column exists

psql -d myapp -c "EXPLAIN ANALYZE SELECT * FROM users WHERE email='test@example.com';"
# ✅ PASS: Index used, query < 10ms

# Ready to commit ✅
```

## Validation Failure Handling

### When Validation Fails

1. **STOP immediately** - Don't proceed to next tier
2. **Rollback changes** - `git reset --hard HEAD`
3. **Analyze failure** - Read error messages carefully
4. **Research solution** - Check docs, Stack Overflow, GitHub issues
5. **Try alternative approach** - Max 3 attempts
6. **Escalate if stuck** - Report to user with detailed failure info

### Example Failure Analysis

**Scenario:** Tier 3 fails - User can't log in

```bash
# Tier 3 validation
npm run dev &
# Open browser, navigate to /login
# Enter credentials
# Click "Login"
# ❌ FAIL: Nothing happens, no error message

# Analysis:
# 1. Check browser console
#    → Error: "POST /api/auth/login 404 Not Found"
#
# 2. Check API route
#    → Route is /api/auth/signin (not /login)
#
# 3. Root cause identified
#    → Frontend calling wrong endpoint

# Solution:
# Fix endpoint in login.tsx:
# - const response = await fetch('/api/auth/login', ...)
# + const response = await fetch('/api/auth/signin', ...)

# Re-validate Tier 3
# ✅ PASS: Login works correctly

# Ready to commit ✅
```

## Best Practices

### 1. Validate Incrementally

Don't make large changes before validating. Make small, incremental changes and validate after each.

**Bad:**
```
- Change 10 files
- Add 500 lines of code
- Validate (fails, hard to debug)
```

**Good:**
```
- Change 1 file
- Add 50 lines
- Validate (passes)
- Commit
- Repeat
```

### 2. Keep Validation Scripts

Create validation scripts for common scenarios:

```bash
# scripts/validate-tier1.sh
#!/bin/bash
set -e
npx tsc --noEmit
npx eslint src/
npm run build
echo "✅ Tier 1 PASS"

# scripts/validate-tier2.sh
#!/bin/bash
set -e
npm test
echo "✅ Tier 2 PASS"

# scripts/validate-tier3.sh
#!/bin/bash
set -e
npm run dev &
SERVER_PID=$!
sleep 5
curl -f http://localhost:3000
kill $SERVER_PID
echo "✅ Tier 3 PASS"

# scripts/validate-all.sh
#!/bin/bash
./scripts/validate-tier1.sh
./scripts/validate-tier2.sh
./scripts/validate-tier3.sh
echo "✅✅✅ ALL TIERS PASS"
```

### 3. Document Validation Steps

In your README or CONTRIBUTING.md, document validation steps:

```markdown
## Validation

All changes must pass three tiers of validation:

### Tier 1: Static Validation
\`\`\`bash
npm run validate:tier1
\`\`\`

### Tier 2: Tests
\`\`\`bash
npm test
\`\`\`

### Tier 3: Functional
\`\`\`bash
npm run dev
# Manually test feature in browser
\`\`\`
```

### 4. Automate Where Possible

Use pre-commit hooks to enforce Tier 1 + 2:

```bash
# .husky/pre-commit
#!/bin/bash
npm run validate:tier1
npm test
```

### 5. Keep Fast Feedback Loops

Optimize validation to be as fast as possible:
- Use incremental type checking
- Run only affected tests
- Use watch mode during development

## Summary

The Functional Validation Protocol ensures:

1. **Code compiles correctly** (Tier 1: Static)
2. **Code doesn't break existing functionality** (Tier 2: Tests)
3. **Code actually works for users** (Tier 3: Functional)

**Remember:**
- Building ≠ Compiling ≠ Working
- ALL three tiers MUST pass before committing
- Tier 3 is THE most important validation
- Users don't care if tests pass—they care if it works

---

**Next Steps:**
- After successful validation, proceed to [Git Workflow Protocol](./GIT_WORKFLOW_PROTOCOL.md) for atomic commits
- Document validation results in commit message
