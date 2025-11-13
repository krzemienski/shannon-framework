# /shannon:test Command - Complete Usage Guide

**Command**: `/shannon:test`
**Purpose**: NO MOCKS functional testing orchestration with automatic platform detection
**Skill**: Invokes functional-testing skill (1402 lines)
**Agent**: Activates TEST_GUARDIAN for test generation and validation
**Output**: Test execution results, NO MOCKS compliance report, coverage analysis

---

## Overview

The `/shannon:test` command enforces Shannon's **NO MOCKS Iron Law** through automatic platform detection, test discovery, functional test execution with real dependencies, and test scaffold generation.

**Core Value**: Tests that validate REAL production behavior, not mock behavior.

**Iron Law**: Shannon NEVER allows mocks, stubs, fakes, or test doubles. All tests use:
- Real browsers (Puppeteer/Playwright)
- Real devices (iOS Simulator)
- Real APIs (HTTP requests)
- Real databases (PostgreSQL, MongoDB)

**Usage**:
```bash
/shannon:test                                  # Discover and run all tests
/shannon:test [test_path]                      # Run specific test file
/shannon:test --platform web                   # Platform-specific testing
/shannon:test --create login-flow             # Generate test scaffold
/shannon:test --validate                       # Check NO MOCKS compliance
```

---

## The 12 Usage Examples

### Example 1: Discover All Tests (Default)

**Input**:
```bash
/shannon:test
```

**Process**:
```
1. Scan project for test files:
   Glob patterns: **/*.test.*, **/*.spec.*, **/*_test.*, **/tests/**/*

2. Classify by platform:
   - Web: Files with puppeteer, playwright imports
   - Mobile: Files with XCTest, XCUITest
   - API: Files with supertest, axios tests
   - Database: Files with database connection tests

3. Analyze NO MOCKS compliance:
   Scan each test for 13 mock patterns
   Violations flagged

4. Calculate coverage:
   Count tested components vs total components
```

**Output**:
```
🧪 Shannon Functional Test Inventory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Total Tests**: 45
**Platforms**: Web (34), API (8), Database (3)
**Coverage**: 78% (components tested / total components)
**NO MOCKS Compliance**: 91% (41/45 tests compliant)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Web Tests (Puppeteer) - 34 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ tests/functional/login.spec.ts
   Tests: 5, Duration: 12s, Status: PASSING
   ├─ Login with valid credentials ✅
   ├─ Login with invalid credentials ✅
   ├─ Password reset flow ✅
   ├─ Remember me functionality ✅
   └─ Logout flow ✅

✅ tests/functional/checkout.spec.ts
   Tests: 8, Duration: 24s, Status: PASSING
   ├─ Add to cart flow ✅
   ├─ Update cart quantity ✅
   ├─ Apply discount code ✅
   ├─ Stripe checkout integration ✅
   └─ [4 more tests...]

⚠️ tests/functional/admin.spec.ts
   Tests: 6, Duration: 18s, Status: 1 FAILING
   ├─ Admin login ✅
   ├─ User management ✅
   ├─ Product management ❌ (timeout after 30s)
   └─ [3 more tests...]

[More test files...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API Tests (Real HTTP) - 8 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ tests/api/auth.test.ts (4 tests, PASSING)
✅ tests/api/products.test.ts (4 tests, PASSING)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Database Tests (Real DB) - 3 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ tests/db/migrations.test.ts (3 tests, PASSING)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Coverage Gaps - 22% Untested
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Missing Tests (Priority Components):
⚠️ SearchBar component (no tests)
   - Priority: HIGH
   - Suggested: /shannon:test --create search-flow --platform web

⚠️ PasswordReset component (no tests)
   - Priority: MEDIUM
   - Suggested: /shannon:test --create password-reset --platform web

⚠️ OrderHistory API (no tests)
   - Priority: MEDIUM
   - Suggested: /shannon:test --create order-api --platform api

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NO MOCKS Compliance - 91%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Compliant: 41/45 tests (91%)

⚠️ Violations (4 tests):
❌ tests/unit/utils.test.ts
   Line 12: jest.mock('../api/client')
   Action: Refactor to functional test with real API

❌ tests/unit/auth.test.ts
   Line 8: @patch('database.connect')
   Action: Use real test database

❌ tests/unit/stripe.test.ts
   Line 15: sinon.stub(stripe, 'createCharge')
   Action: Use Stripe test mode (real Stripe API)

❌ tests/helpers/mockData.ts
   Line 45: createMockUser()
   Action: Use real user creation in test database

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended Actions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 1: Fix NO MOCKS violations (4 tests)
Priority 2: Add tests for coverage gaps (3 components)
Priority 3: Fix failing test (admin product management timeout)

Next: /shannon:test --validate (check compliance in detail)
```

**Key Learning**: Default mode discovers ALL tests, reports coverage, flags NO MOCKS violations.

---

### Example 2: Run Specific Test File

**Input**:
```bash
/shannon:test tests/functional/checkout.spec.ts
```

**Output**:
```
🧪 Shannon Functional Test Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test**: tests/functional/checkout.spec.ts
**Platform**: Web (Puppeteer)
**NO MOCKS**: ✅ Verified (real browser, real API, real Stripe)
**Duration**: 24.3s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 8/8 PASSING ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Add product to cart (2.1s)
✓ Update cart quantity (1.8s)
✓ Remove from cart (1.5s)
✓ Apply discount code (2.3s)
✓ Stripe checkout integration (8.9s)
✓ Order confirmation page (3.2s)
✓ Email receipt sent (2.8s)
✓ Order appears in history (1.7s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Browser: Chrome 119.0.6045.105
Viewport: 1280x720
Base URL: http://localhost:3000
API: http://localhost:3001 (real backend)
Database: PostgreSQL test instance (real DB)
Stripe: Test mode (real Stripe API, test keys)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Artifacts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Screenshots: 8 saved (checkout-flow/*.png)
Videos: 1 recording (full-checkout-flow.webm)
Logs: Browser console logs captured
Network: HAR file with all requests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All checkout tests passing
✅ Real Stripe integration validated
✅ NO MOCKS compliance verified

Continue with confidence - checkout flow production-ready
```

**Key Learning**: Specific test execution shows detailed results + artifacts (screenshots, videos, logs).

---

### Example 3: Platform Override (--platform)

**Input**:
```bash
/shannon:test tests/app.test.ts --platform mobile
```

**Output**:
```
🧪 Shannon Mobile Test Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test**: tests/app.test.ts
**Platform**: Mobile (iOS Simulator) - OVERRIDE
**NO MOCKS**: ✅ Verified (real iOS device simulation)
**Duration**: 45.8s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 12/12 PASSING ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ App launches successfully (5.2s)
✓ Login screen appears (1.8s)
✓ Login with credentials (3.4s)
✓ Dashboard loads (2.9s)
✓ Product search functional (4.1s)
✓ Add to cart (2.3s)
✓ Cart badge updates (1.2s)
✓ Checkout navigation (1.9s)
✓ Apple Pay integration (12.5s)
✓ Order confirmation (3.2s)
✓ Push notification received (4.8s)
✓ App backgrounding/resuming (2.5s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Device: iPhone 15 Pro Simulator
iOS Version: 17.0
UDID: A1B2C3D4-E5F6-7890-ABCD-1234567890AB
App Build: Debug (TestFlight configuration)
Backend: http://localhost:3001 (real API)
Push: APNs sandbox (real notifications)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Artifacts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Screenshots: 12 saved (iOS simulator captures)
Videos: 1 recording (full-app-flow.mov)
Logs: Xcode console logs
Network: Charles Proxy HAR file
```

**Key Learning**: --platform overrides auto-detection (useful when ambiguous test files).

---

### Example 4: Create New Test Scaffold (--create)

**Input**:
```bash
/shannon:test --create product-search --platform web
```

**Output**:
```
🧪 Shannon Test Scaffold Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test File**: tests/functional/product-search.spec.ts
**Platform**: Web (Puppeteer)
**Type**: Functional (NO MOCKS)
**Target**: Product search functionality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated Test Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```typescript
import { test, expect } from '@playwright/test';

test.describe('Product Search - Functional Tests (NO MOCKS)', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Real browser, real backend, real database
    await page.goto('http://localhost:3000');
  });

  test('User searches for product by name', async ({ page }) => {
    // Navigate to search
    await page.click('[data-testid="search-button"]');

    // Type search query (REAL keyboard input to REAL browser)
    await page.fill('[data-testid="search-input"]', 'wireless mouse');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Wait for REAL API response
    await page.waitForSelector('[data-testid="search-results"]');

    // Assert REAL results from REAL database
    const results = await page.locator('[data-testid="product-card"]').count();
    expect(results).toBeGreaterThan(0);

    // Verify product details from REAL data
    const firstProduct = page.locator('[data-testid="product-card"]').first();
    await expect(firstProduct).toContainText('wireless mouse');
  });

  test('Search handles no results gracefully', async ({ page }) => {
    await page.click('[data-testid="search-button"]');
    await page.fill('[data-testid="search-input"]', 'xyznonexistent123');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Real API returns empty results
    await page.waitForSelector('[data-testid="no-results-message"]');
    await expect(page.locator('[data-testid="no-results-message"]'))
      .toContainText('No products found');
  });

  test('Search filters work correctly', async ({ page }) => {
    // Test REAL filtering with REAL data
    await page.goto('http://localhost:3000/products');
    await page.selectOption('[data-testid="category-filter"]', 'electronics');

    // Wait for REAL backend filter response
    await page.waitForLoadState('networkidle');

    // Verify REAL filtered results
    const products = page.locator('[data-testid="product-card"]');
    const count = await products.count();
    expect(count).toBeGreaterThan(0);

    // All should be electronics category
    for (let i = 0; i < count; i++) {
      const category = await products.nth(i).getAttribute('data-category');
      expect(category).toBe('electronics');
    }
  });

  test.afterEach(async ({ page }) => {
    // Cleanup: Close browser
    await page.close();
  });
});
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shannon Test Patterns Included
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Real browser automation (Puppeteer)
✅ Real backend API calls (http://localhost:3001)
✅ Real database queries (PostgreSQL test instance)
✅ NO MOCKS (zero test doubles)
✅ Shannon conventions (describe blocks, test names)
✅ Cleanup/teardown (browser close)
✅ Realistic test data (actual search queries)
✅ Assertions on real behavior

❌ EXCLUDED (Shannon prohibits):
- jest.mock() - NO MOCKS
- Fake APIs - Real HTTP only
- In-memory DB - Real PostgreSQL required
- Mock responses - Real backend responses

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review: tests/functional/product-search.spec.ts
2. Customize: Add your specific search scenarios
3. Setup: Ensure Puppeteer MCP configured (/shannon:check_mcps)
4. Run: /shannon:test tests/functional/product-search.spec.ts
5. Iterate: Add more test cases as needed
```

**Key Learning**: --create generates Shannon-compliant test scaffolds (NO MOCKS, real dependencies).

---

### Example 5: NO MOCKS Violation Detection

**Input**:
```bash
/shannon:test tests/unit/payment.test.ts
```

**Process**:
```
1. Load test file
2. Scan for mock patterns:
   Found: jest.mock('stripe') on line 8

3. post_tool_use.py hook triggers (automatic)
4. Violation detected
```

**Output**:
```
🚨 Shannon NO MOCKS Violation Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**File**: tests/unit/payment.test.ts
**Line**: 8
**Violation**: jest.mock('stripe')

**Shannon Testing Philosophy**:
Tests must validate REAL system behavior, not mocked responses.

**Why NO MOCKS**:
❌ Mocks create false confidence
❌ Production bugs missed by mocked tests
❌ Integration failures not caught
❌ Refactoring breaks hidden by mocks

**What You're Testing**:
Currently: Mock Stripe object (fake behavior)
Should Be: Real Stripe test mode API

**Required Action - Refactor to Functional Test**:

❌ WRONG (Current):
```typescript
jest.mock('stripe');
test('createCharge', () => {
  stripe.charges.create = jest.fn().mockResolvedValue({ id: 'ch_123' });
  // Testing mock, not Stripe
});
```

✅ CORRECT (Shannon):
```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_TEST_KEY); // REAL Stripe

test('createCharge with real Stripe', async () => {
  // Real Stripe API call in test mode
  const charge = await stripe.charges.create({
    amount: 1000,
    currency: 'usd',
    source: 'tok_visa', // Stripe test token
  });

  expect(charge.id).toMatch(/^ch_/); // Real Stripe response
  expect(charge.amount).toBe(1000);
});
```

**Setup Real Stripe Testing**:
1. Get Stripe test keys: https://dashboard.stripe.com/test/apikeys
2. Set environment: STRIPE_TEST_KEY=sk_test_...
3. Use test tokens: tok_visa, tok_mastercard (Stripe provides)
4. Real API calls, test mode (no real charges)

**Verify MCP**:
```bash
/shannon:check_mcps
# Ensure Puppeteer configured for full checkout flow testing
```

**Test Blocked**: Cannot execute until mocks removed
**Refactor**: Update test to use real Stripe test mode
**Re-run**: /shannon:test tests/functional/payment.spec.ts (after refactor)
```

**Key Learning**: NO MOCKS violations caught automatically, detailed refactoring guidance provided.

---

### Example 6: Create Mobile Test

**Input**:
```bash
/shannon:test --create login-screen --platform mobile
```

**Output**:
```
🧪 Shannon Mobile Test Scaffold Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test File**: tests/ios/LoginScreenTests.swift
**Platform**: Mobile (iOS Simulator via XCUITest)
**Type**: Functional (NO MOCKS - real device simulation)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated Test Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```swift
import XCTest

class LoginScreenTests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false

        // Launch REAL app on REAL simulator (NO MOCKS)
        app = XCUIApplication()
        app.launch()
    }

    func testLoginWithValidCredentials() {
        // Navigate to login screen (REAL UI interaction)
        app.buttons["Login"].tap()

        // Enter credentials (REAL text input on REAL device)
        let emailField = app.textFields["Email"]
        emailField.tap()
        emailField.typeText("test@example.com")

        let passwordField = app.secureTextFields["Password"]
        passwordField.tap()
        passwordField.typeText("SecurePassword123")

        // Tap login (REAL button tap, REAL API call)
        app.buttons["Submit"].tap()

        // Wait for REAL backend authentication response
        let dashboardTitle = app.staticTexts["Dashboard"]
        XCTAssertTrue(dashboardTitle.waitForExistence(timeout: 5))

        // Verify REAL navigation occurred
        XCTAssertEqual(app.navigationBars.element.identifier, "Dashboard")
    }

    func testLoginWithInvalidCredentials() {
        app.buttons["Login"].tap()

        // Real invalid credentials
        app.textFields["Email"].tap()
        app.textFields["Email"].typeText("wrong@example.com")

        app.secureTextFields["Password"].tap()
        app.secureTextFields["Password"].typeText("wrongpass")

        app.buttons["Submit"].tap()

        // Real backend returns 401 error
        let errorMessage = app.staticTexts["Invalid credentials"]
        XCTAssertTrue(errorMessage.waitForExistence(timeout: 3))
    }

    override func tearDown() {
        // Cleanup
        app.terminate()
        super.tearDown()
    }
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shannon Mobile Test Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Real iOS Simulator launch
✅ Real UI element interaction
✅ Real backend API calls (authentication)
✅ Real device behavior (tap, type, wait)
✅ NO MOCKS (no test doubles)
✅ Assertions on real app behavior

**MCP Required**: iOS Simulator MCP or xc-mcp
**Setup**: /shannon:check_mcps

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Open in Xcode: tests/ios/LoginScreenTests.swift
2. Add to test target
3. Run: /shannon:test tests/ios/LoginScreenTests.swift
4. Or: xcodebuild test -scheme YourApp -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

**Key Learning**: Mobile test scaffolds use XCUITest with real simulator, real API calls.

---

### Example 7: API Test Creation

**Input**:
```bash
/shannon:test --create user-api --platform api
```

**Output**:
```
🧪 Shannon API Test Scaffold Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test File**: tests/api/user-api.test.ts
**Platform**: API (Real HTTP requests)
**Type**: Functional (NO MOCKS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated Test Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:3001';
const api = axios.create({ baseURL: API_BASE });

describe('User API - Functional Tests (NO MOCKS)', () => {
  let authToken: string;
  let testUserId: string;

  beforeAll(async () => {
    // Setup: Create test user in REAL database
    const response = await api.post('/auth/register', {
      email: `test-${Date.now()}@example.com`,
      password: 'TestPassword123!',
      name: 'Test User'
    });

    authToken = response.data.token; // REAL JWT token
    testUserId = response.data.user.id;
  });

  it('GET /users/:id returns user data', async () => {
    // REAL HTTP request to REAL backend
    const response = await api.get(`/users/${testUserId}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    });

    // Assert on REAL database data
    expect(response.status).toBe(200);
    expect(response.data).toMatchObject({
      id: testUserId,
      email: expect.stringContaining('@example.com'),
      name: 'Test User'
    });
  });

  it('PUT /users/:id updates user profile', async () => {
    // REAL update request
    const response = await api.put(`/users/${testUserId}`,
      { name: 'Updated Name' },
      { headers: { Authorization: `Bearer ${authToken}` } }
    );

    expect(response.status).toBe(200);
    expect(response.data.name).toBe('Updated Name');

    // Verify update persisted in REAL database
    const verify = await api.get(`/users/${testUserId}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    });
    expect(verify.data.name).toBe('Updated Name');
  });

  it('DELETE /users/:id requires admin role', async () => {
    // REAL request with non-admin token
    try {
      await api.delete(`/users/${testUserId}`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      fail('Should have thrown 403 error');
    } catch (error) {
      // REAL 403 error from REAL authorization check
      expect(error.response.status).toBe(403);
      expect(error.response.data.error).toContain('Admin access required');
    }
  });

  afterAll(async () => {
    // Cleanup: Delete test user from REAL database
    try {
      await api.delete(`/users/${testUserId}`, {
        headers: { Authorization: `Bearer ${ADMIN_TOKEN}` }
      });
    } catch (error) {
      console.warn('Cleanup failed:', error.message);
    }
  });
});
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shannon API Test Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Real HTTP requests (axios, not mocked)
✅ Real backend responses
✅ Real database operations (create, read, update, delete)
✅ Real authentication (JWT tokens)
✅ Real authorization checks (403 errors)
✅ Cleanup after tests (delete test data)
✅ NO MOCKS (no axios.mock, no nock, no msw)

**Backend Must Be Running**:
```bash
npm run dev  # Start real backend on localhost:3001
# Tests will make REAL requests to this server
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Start backend: npm run dev
2. Run test: /shannon:test tests/api/user-api.test.ts
3. Add more API endpoint tests
4. Ensure test database has seed data
```

**Key Learning**: API tests use real HTTP, real backend, real database - no mocking libraries.

---

### Example 8: Database Test Validation

**Input**:
```bash
/shannon:test tests/db/migrations.test.ts --platform database
```

**Output**:
```
🧪 Shannon Database Test Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test**: tests/db/migrations.test.ts
**Platform**: Database (Real PostgreSQL instance)
**NO MOCKS**: ✅ Verified (real database connection)
**Duration**: 8.3s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results: 15/15 PASSING ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Migration 001: Create users table (234ms)
✓ Migration 002: Add email index (156ms)
✓ Migration 003: Create products table (289ms)
✓ Migration 004: Add product categories (198ms)
✓ Migration 005: Create orders table (312ms)
✓ Migration 006: Add foreign keys (245ms)
✓ Migration 007: Create sessions table (189ms)
✓ Migration 008: Add cart items table (267ms)
✓ Rollback test: All migrations revert cleanly (892ms)
✓ Idempotency: Re-running migrations safe (456ms)
✓ Data integrity: Foreign keys enforced (123ms)
✓ Index performance: Queries use indexes (78ms)
✓ Constraint validation: NOT NULL enforced (67ms)
✓ Trigger functionality: Updated_at auto-updates (89ms)
✓ Full migration cycle: Up and down clean (1.2s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Database: PostgreSQL 15.3
Test Instance: localhost:5432/test_db
Connection: Direct (NO in-memory, NO sqlite substitute)
Migrations: 8 applied, 8 verified
Schema Version: 008_latest

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Artifacts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Schema Dump: tests/artifacts/schema_post_migrations.sql
Query Plans: tests/artifacts/explain_plans/ (index usage verified)
Data Samples: tests/artifacts/sample_data/ (test records)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Database Health
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All tables created successfully
✅ All indexes present and used by queries
✅ All foreign keys enforced
✅ All constraints validated
✅ Migration history table accurate

**Database ready for application testing**
```

**Key Learning**: Database tests use REAL PostgreSQL, validate actual schema behavior, no in-memory substitutes.

---

### Example 9: Test Coverage Report

**Input**:
```bash
/shannon:test --coverage
```

**Output**:
```
📊 Shannon Test Coverage Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Coverage**: 78% (good, target: 80%)
**NO MOCKS Compliance**: 91% (41/45 tests)
**Platforms**: Web (75%), API (100%), Database (100%), Mobile (0%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Component Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Frontend Components** (32 total):
✅ Tested (24): 75% coverage
   - ProductCard, ShoppingCart, Checkout, Login, etc.

⚠️ Untested (8): 25% gap
   - SearchBar (HIGH priority)
   - PasswordReset (MEDIUM priority)
   - UserProfile (MEDIUM)
   - AdminDashboard (LOW - admin-only)
   - [4 more...]

**Backend Endpoints** (28 total):
✅ Tested (24): 86% coverage
   - Auth endpoints (100%)
   - Product endpoints (90%)
   - Order endpoints (80%)

⚠️ Untested (4): 14% gap
   - GET /admin/analytics (LOW - admin analytics)
   - POST /admin/reports (LOW)
   - GET /users/preferences (MEDIUM)
   - PATCH /orders/:id/cancel (HIGH priority)

**Database Operations** (12 tables):
✅ Tested (10): 83% coverage
   - CRUD operations tested
   - Constraints validated
   - Migrations verified

⚠️ Untested (2): 17% gap
   - Audit_logs table (no tests)
   - User_preferences table (no tests)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User Journey Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Complete Journeys (Puppeteer E2E):
1. Browse → Add to Cart → Checkout → Purchase ✅ (18s)
2. Register → Login → Update Profile ✅ (12s)
3. Search → Filter → View Product ✅ (8s)

⚠️ Partial Journeys:
4. Password Reset Flow (missing email verification step)
5. Admin Product Management (missing bulk upload)

❌ Missing Journeys:
6. Wishlist functionality (no tests at all)
7. Product reviews (no tests)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Priority 1**: Fix NO MOCKS violations (4 tests)
   Impact: 91% → 100% compliance
   Time: ~2 hours

**Priority 2**: Add HIGH priority component tests
   - SearchBar functional test
   - PATCH /orders/:id/cancel API test
   Time: ~3 hours
   Impact: 78% → 85% coverage

**Priority 3**: Complete partial journeys
   - Password reset email verification
   - Admin bulk upload
   Time: ~2 hours

**Total to 80%**: ~5 hours, achievable before deployment
```

**Key Learning**: --coverage provides actionable test gap analysis with priorities.

---

### Example 10: Validate Existing Tests (NO MOCKS Check)

**Input**:
```bash
/shannon:test --validate
```

**Output**:
```
🔍 Shannon NO MOCKS Compliance Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Scanning**: All test files in project
**Patterns Checked**: 13 mock patterns
**Mode**: Static analysis (no execution)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Compliance Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall**: 91% compliant (41/45 tests)

✅ COMPLIANT TESTS (41):
All functional tests using real dependencies:
- Puppeteer tests (34) - Real browser ✅
- API tests (5) - Real HTTP ✅
- Database tests (2) - Real PostgreSQL ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIOLATIONS FOUND (4 tests)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ tests/unit/payment.test.ts
   Line 8: jest.mock('stripe')
   Pattern: Jest mocking
   Impact: Tests mock Stripe, not real Stripe test mode
   Fix: Use real Stripe with test keys (tok_visa)

❌ tests/unit/auth.test.ts
   Line 15: @patch('bcrypt.hash')
   Pattern: Python mock decorator
   Impact: Tests mock password hashing, not real bcrypt
   Fix: Use real bcrypt with test passwords

❌ tests/unit/email.test.ts
   Line 23: sinon.stub(sendgrid, 'send')
   Pattern: Sinon stubbing
   Impact: Tests stub email sending, doesn't validate SendGrid integration
   Fix: Use SendGrid test API or capture emails in test mode

❌ tests/helpers/mockData.ts
   Line 67: function createMockUser()
   Pattern: Mock factory
   Impact: Creates fake users instead of real test database users
   Fix: Create real users in test database, cleanup after tests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended Actions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Refactor Priority**:
1. payment.test.ts (HIGH - Stripe integration critical)
2. auth.test.ts (HIGH - security testing critical)
3. email.test.ts (MEDIUM - email delivery validation)
4. mockData.ts (MEDIUM - affects multiple tests)

**Estimated Refactor Time**: 4-6 hours total
- payment.test.ts: 1.5h (Stripe setup + test mode)
- auth.test.ts: 1h (real bcrypt + test database)
- email.test.ts: 1.5h (SendGrid test mode)
- mockData.ts: 1-2h (convert to real test data creation)

**Post-Refactor**:
- Compliance: 91% → 100% ✅
- Confidence: Tests validate production behavior
- Shannon compliant: Full NO MOCKS adherence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review violations above
2. Refactor tests to use real dependencies
3. Re-run: /shannon:test --validate
4. Target: 100% NO MOCKS compliance
```

**Key Learning**: --validate scans without executing, identifies all mock violations for batch refactoring.

---

### Example 11: Multi-Platform Test Suite

**Input**:
```bash
/shannon:test --all-platforms
```

**Output**:
```
🧪 Shannon Multi-Platform Test Suite
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Platforms Detected**: Web, API, Database
**Total Tests**: 45
**Execution Mode**: Sequential by platform

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform 1: Web (Puppeteer) - 34 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running web tests with real Chrome browser...

Results: 33/34 PASSING (97%)
Duration: 3m 42s
Failures: 1 (admin.spec.ts timeout)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform 2: API (Real HTTP) - 8 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running API tests against http://localhost:3001...

Results: 8/8 PASSING ✅
Duration: 12s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform 3: Database (PostgreSQL) - 3 tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running database tests on test_db instance...

Results: 3/3 PASSING ✅
Duration: 2.8s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 44/45 PASSING (98%)
Duration: 4m 56s
NO MOCKS Compliance: 100% ✅ (all executed tests)

**Failure**: tests/functional/admin.spec.ts (product management timeout)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Fix failing test: admin product management timeout
   Likely: Slow query, need index on products.category

✅ All other platforms validated and production-ready
```

**Key Learning**: Multi-platform testing runs all test types sequentially, provides comprehensive validation.

---

### Example 12: Performance Benchmarking Tests

**Input**:
```bash
/shannon:test --benchmark performance
```

**Output**:
```
⚡ Shannon Performance Benchmark Tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Mode**: Performance validation with REAL load
**Platform**: Web + API combined
**Load**: Simulated real user behavior

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Page Load Performance (Puppeteer)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Homepage:
✅ First Paint: 421ms (target <500ms)
✅ Largest Contentful Paint: 1.2s (target <2s)
✅ Time to Interactive: 1.8s (target <3s)

Product Page:
⚠️ First Paint: 678ms (target <500ms) - SLOW
✅ LCP: 1.9s (target <2s)
⚠️ TTI: 3.4s (target <3s) - SLOW

Checkout Page:
✅ First Paint: 445ms
✅ LCP: 1.6s
✅ TTI: 2.4s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API Response Times (Real HTTP Load)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GET /products (100 requests):
✅ p50: 45ms
✅ p95: 89ms
✅ p99: 134ms (target <200ms)

POST /orders (50 requests):
✅ p50: 123ms
✅ p95: 287ms
⚠️ p99: 456ms (target <300ms) - SLOW

GET /search (100 requests):
⚠️ p50: 234ms (target <100ms) - SLOW
🔴 p95: 678ms (target <200ms) - CRITICAL
🔴 p99: 1.2s (target <300ms) - CRITICAL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Database Query Performance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Products table (10K records):
✅ SELECT with index: 12ms avg
⚠️ Full-text search: 234ms avg (needs optimization)

Orders table (5K records):
✅ User orders query: 34ms avg
✅ Admin dashboard query: 89ms avg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Performance Issues Identified
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL: Search API slow (678ms p95)
   - Cause: Full-text search on products table (10K records)
   - Fix: Add PostgreSQL full-text index
   - Expected: 678ms → <100ms

⚠️ MODERATE: Product page slow (678ms first paint)
   - Cause: Large image loading
   - Fix: Image optimization + lazy loading
   - Expected: 678ms → <400ms

**Recommended Actions**:
1. Add full-text index: CREATE INDEX ON products USING GIN(to_tsvector(...))
2. Optimize images: compress, webp format, lazy load
3. Re-run: /shannon:test --benchmark performance
4. Target: All metrics GREEN
```

**Key Learning**: Performance tests use REAL load, identify actual bottlenecks (not mock performance).

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Using Unit Tests with Mocks

**Symptom**:
```typescript
// tests/unit/api.test.ts
jest.mock('axios');

test('fetchUser', async () => {
  axios.get.mockResolvedValue({ data: { id: 1 } });
  const user = await fetchUser(1);
  expect(user.id).toBe(1);
});
```

**Why Shannon Blocks This**:
```
🚨 post_tool_use.py hook detects jest.mock()

❌ VIOLATION: Mock-based unit test

**What You're Testing**: Mock axios object (fake)
**What You Should Test**: Real HTTP request to real backend

**Problems with Mocks**:
1. Tests pass even if real API broken
2. Integration failures missed
3. Authentication issues not caught
4. Network errors not validated
5. Response format changes break production but tests pass
```

**Shannon Alternative**:
```typescript
// tests/functional/api.spec.ts (NO MOCKS)
import { test, expect } from '@playwright/test';

test('fetchUser retrieves real user data', async ({ request }) => {
  // REAL HTTP request to REAL backend
  const response = await request.get('http://localhost:3001/users/1');

  // Assert on REAL response from REAL database
  expect(response.status()).toBe(200);
  const user = await response.json();
  expect(user).toHaveProperty('id');
  expect(user).toHaveProperty('email');
});
```

**Recommendation**: Delete unit tests, write functional tests with Puppeteer/real HTTP.

---

### ❌ Anti-Pattern 2: In-Memory Database for Speed

**Symptom**:
```typescript
// Using sqlite :memory: instead of real PostgreSQL
const db = new Database(':memory:');
```

**Why Shannon Prohibits**:
```
❌ In-memory databases are NOT real databases

**Differences from PostgreSQL**:
- Different SQL dialect (SQLite vs PostgreSQL)
- Missing features (no JSONB, no advanced indexes)
- Different transaction behavior
- Different constraint enforcement
- Different query performance characteristics

**Problems**:
1. Tests pass with SQLite, fail with PostgreSQL in production
2. PostgreSQL-specific features untested (full-text search, JSONB)
3. Performance characteristics different (index usage)
```

**Shannon Alternative**:
```typescript
// Real PostgreSQL test instance
import { Pool } from 'pg';

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'test_db',  // REAL PostgreSQL database
  user: 'test_user',
  password: 'test_pass'
});

// Docker makes this easy:
// docker run -d -p 5432:5432 -e POSTGRES_DB=test_db postgres:15

// Tests run against REAL PostgreSQL
```

**Recommendation**: Use Docker for real database in tests (spin up in 30s, matches production).

---

### ❌ Anti-Pattern 3: Skipping Cleanup (Test Data Pollution)

**Symptom**:
```typescript
test('create user', async () => {
  const user = await createUser({ email: 'test@example.com' });
  expect(user.id).toBeDefined();
  // NO CLEANUP - test data remains in database
});

// Next test run:
// Error: Email 'test@example.com' already exists
```

**Shannon Counter**:
```
⚠️ **TEST DATA CLEANUP REQUIRED**

**Problem**: Tests leave data in database
**Impact**: Tests fail on subsequent runs (unique constraints)

**Shannon Pattern**:
```typescript
describe('User API', () => {
  let testUserId: string;

  afterEach(async () => {
    // CLEANUP: Delete test data from REAL database
    if (testUserId) {
      await db.query('DELETE FROM users WHERE id = $1', [testUserId]);
      testUserId = null;
    }
  });

  test('create user', async () => {
    const user = await createUser({ email: `test-${Date.now()}@example.com` });
    testUserId = user.id; // Store for cleanup
    expect(user.id).toBeDefined();
  });
  // afterEach cleanup ensures test data removed
});
```

**Alternative**: Use database transactions (rollback after test)
```typescript
beforeEach(async () => {
  await db.query('BEGIN');  // Start transaction
});

afterEach(async () => {
  await db.query('ROLLBACK');  // Rollback transaction (auto-cleanup)
});
```

**Recommendation**: Always cleanup test data (delete records or use transactions).

---

## Integration with Other Commands

### /shannon:test → /shannon:test Flow

**Workflow**:
```bash
# Step 1: Analyze spec
/shannon:test "Build e-commerce platform..."

# Output includes:
# Phase 4: Testing (15% timeline)
# - Puppeteer tests for Frontend
# - Real HTTP tests for Backend
# - Real database tests

# Step 2: Implement features
[Development work...]

# Step 3: Create tests
/shannon:test --create checkout-flow --platform web

# Step 4: Run tests
/shannon:test tests/functional/checkout-flow.spec.ts

# Step 5: Validate compliance
/shannon:test --validate
```

---

### /shannon:test → /shannon:test Integration

**Wave 4 (Testing Phase)**:
```bash
# Wave orchestration includes testing wave
/shannon:test

# Wave 4 automatically:
1. Activates TEST_GUARDIAN agent
2. TEST_GUARDIAN runs: /shannon:test --validate
3. Identifies NO MOCKS violations
4. Refactors tests to Shannon compliance
5. Runs: /shannon:test (full suite)
6. Reports results in wave synthesis
```

---

## Troubleshooting

### Issue: "Tests pass locally, fail in CI"

**Cause**: Environment differences (mocks hide this, real tests catch it)

**Diagnosis**:
- Real tests require backend running
- Real tests require database seeded
- Real tests require correct environment variables

**Resolution**:
```yaml
# CI configuration (GitHub Actions example)
- name: Start backend
  run: npm run dev &

- name: Start database
  run: docker run -d -p 5432:5432 postgres:15

- name: Run tests
  run: /shannon:test --all-platforms
```

---

## FAQ

**Q: Why NO MOCKS? Unit tests are faster.**
A: Fast tests that don't catch bugs are worthless. Real tests catch real bugs. Speed is secondary to correctness.

**Q: How do I test external APIs (Stripe, SendGrid)?**
A: Use test mode:
   - Stripe: Test API keys + test tokens (tok_visa)
   - SendGrid: Test API + capture mode
   - Real APIs provide test modes specifically for this

**Q: Real tests are slow, how to speed up?**
A: Parallelize (run tests concurrently), but don't mock. Shannon's wave orchestration can parallelize test execution.

**Q: What about database tests?**
A: Docker PostgreSQL test instance (docker run... takes 30s to start). Use transactions for cleanup (instant rollback).

---

**Command**: /shannon:test
**Skill**: functional-testing (shannon-plugin/skills/functional-testing/SKILL.md)
**Agent**: TEST_GUARDIAN (shannon-plugin/agents/TEST_GUARDIAN.md)
**Examples**: 12 comprehensive scenarios
**Anti-Patterns**: 3 common violations (mocks, in-memory DB, no cleanup)
**Iron Law**: NO MOCKS - enforced by post_tool_use.py hook
