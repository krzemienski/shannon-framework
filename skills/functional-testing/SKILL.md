---
name: functional-testing
description: |
  Enforce NO MOCKS testing philosophy with real systems. Iron Law: no mock objects, no unit tests,
  no stubs. Test with real browsers (Puppeteer MCP), real databases, real APIs. Enforced via
  post_tool_use.py hook. Use when: writing any tests, tempted to use mocks, need testing guidance.

skill-type: RIGID
shannon-version: ">=4.0.0"

mcp-requirements:
  recommended:
    - name: puppeteer
      purpose: Real browser automation for UI tests
    - name: playwright
      purpose: Alternative browser automation
    - name: xc-mcp
      purpose: iOS simulator testing
    - name: chrome-devtools
      purpose: Chrome DevTools Protocol automation

allowed-tools: All
---

# Functional Testing - The NO MOCKS Iron Law

## Purpose

Shannon's RIGID testing philosophy that eliminates mock objects, stubs, and unit tests in favor of functional tests with real systems. Enforces testing with real browsers (Puppeteer/Playwright MCP), real databases, real APIs, and real user workflows. Prevents false confidence from passing tests that don't validate production behavior. Integrated with post_tool_use.py hook for automatic violation detection and enforcement.

## When to Use

Use this skill when:
- Writing ANY tests for Shannon projects
- Tempted to use mock objects or stubs
- Need guidance on functional testing patterns
- Setting up test infrastructure
- Reviewing test code for violations
- Training developers on NO MOCKS philosophy

DO NOT use when:
- Writing documentation tests (examples only, not validation)
- Generating test data fixtures (acceptable if used with real systems)
- Creating development utilities (not tests)

## Core Competencies

1. **NO MOCKS Enforcement**: Absolute prohibition of mock objects, stubs, fakes, and test doubles with automatic violation detection
2. **Real Browser Testing**: Puppeteer/Playwright MCP integration for testing actual DOM, JavaScript, CSS, and user interactions
3. **Real Database Testing**: Functional tests with actual PostgreSQL, MongoDB, D1, MySQL instances, real schemas, real transactions
4. **Real API Testing**: HTTP requests to staging/test environments with real authentication, real endpoints, real responses
5. **Platform Detection**: Identifies target platform (web, iOS, API, database) and recommends appropriate MCP integrations
6. **Anti-Pattern Detection**: Automatic scanning for mock imports, stub patterns, fake implementations via post_tool_use.py hook
7. **Test Environment Setup**: Guides creation of real test infrastructure (Docker containers, test databases, staging APIs)

## Inputs

**Required:**
- `platform` (string): Target platform - "web", "ios", "api", "database", "cli"
- `test_mode` (string): Test type - "e2e", "integration", "functional"
- `feature` (string): Feature or workflow being tested

**Optional:**
- `mcp_available` (array): List of installed MCPs (auto-detected)
- `test_environment` (object): Test infrastructure details (database connection, API endpoints, browser config)
- `test_framework` (string): Preferred framework (Playwright, Jest, Pytest, XCTest)

## Workflow

### Phase 1: Platform Detection & MCP Selection

1. **Identify Target Platform**
   - Action: Parse feature description for platform keywords
   - Tool: Regex pattern matching on "web UI", "iOS app", "REST API", "database"
   - Output: Platform type (web/ios/api/database/cli)

2. **Check Available MCPs**
   - Action: Query installed MCPs via `/sh_check_mcps` or MCP discovery
   - Tool: MCP server discovery
   - Output: List of available testing MCPs

3. **Recommend Primary MCP**
   - Action: Match platform to optimal MCP
   - Rules:
     - Web → Puppeteer MCP (preferred) or Playwright MCP
     - iOS → xc-mcp (iOS Simulator Tools)
     - API → Built-in HTTP libraries
     - Database → Database-specific drivers (psycopg2, mongodb, D1)
   - Output: MCP recommendation with setup instructions

4. **Check for Fallback Options**
   - Action: If primary MCP unavailable, recommend fallback
   - Fallback: Manual testing procedures if no MCP available
   - Output: Fallback strategy

### Phase 2: Test Generation

1. **Select Test Pattern Template**
   - Action: Choose appropriate pattern from library
   - Templates: Complete E2E workflow, Real-time sync test, CRUD workflow, Transaction test
   - Output: Base test structure

2. **Customize for Feature**
   - Action: Replace placeholders with feature-specific details
   - Customization: Selectors, API endpoints, data models, validation assertions
   - Output: Customized test code

3. **Add Real System Integration**
   - Action: Configure connections to real systems
   - Integration: Browser launch, database connection, API authentication
   - Output: Test code with real system setup

4. **Define Cleanup Procedures**
   - Action: Add cleanup code for test data and resources
   - Cleanup: Delete test records, close connections, terminate browsers
   - Output: Complete test with cleanup

### Phase 3: Violation Scanning

1. **Scan for Mock Imports**
   - Action: Search test code for forbidden patterns
   - Patterns: `unittest.mock`, `jest.mock`, `sinon.stub`, `@patch`
   - Output: List of violations or clean bill of health

2. **Scan for Stub Patterns**
   - Action: Detect fake implementations and test doubles
   - Patterns: `Mock()`, `FakeDatabase`, `InMemoryDatabase`, `stub_function`
   - Output: List of violations or clean bill of health

3. **Verify Real System Usage**
   - Action: Confirm test uses real browsers, databases, APIs
   - Verification: `puppeteer.launch`, `psycopg2.connect`, `requests.post`
   - Output: Confirmation of real system usage

4. **Report Violations**
   - Action: If violations found, explain why they're forbidden
   - Tool: Generate violation report with remediation guidance
   - Output: Violation report or success confirmation

### Phase 4: Test Environment Guidance

1. **Define Required Infrastructure**
   - Action: List real systems needed for test
   - Infrastructure: Test database, staging API, Docker containers
   - Output: Infrastructure requirements

2. **Provide Setup Instructions**
   - Action: Generate setup commands and configuration
   - Examples: Docker compose files, database init scripts, API test mode setup
   - Output: Setup documentation

3. **Document Cleanup Procedures**
   - Action: Explain how to clean test data between runs
   - Procedures: TRUNCATE tables, delete test users, reset state
   - Output: Cleanup documentation

## Outputs

Depending on scenario:

**Test Code Output** (when MCP available):
```javascript
// Example Puppeteer test
const { test, expect } = require('@playwright/test');

test('User completes login workflow', async ({ page }) => {
  // REAL browser navigation
  await page.goto('http://localhost:3000/login');

  // REAL form interaction
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="login-button"]');

  // Wait for REAL backend authentication
  await page.waitForURL('**/dashboard');

  // Assert on REAL result
  expect(page.url()).toContain('/dashboard');
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
});
```

**Manual Testing Procedures** (when no MCP available):
```markdown
1. Launch real browser manually
2. Navigate to http://localhost:3000/login
3. Enter email: test@example.com
4. Enter password: SecurePass123!
5. Click login button
6. Verify redirect to /dashboard
7. Verify user menu is visible
```

**Violation Report** (when violations detected):
```json
{
  "status": "violations_found",
  "violations": [
    {
      "type": "mock_import",
      "line": 3,
      "pattern": "from unittest.mock import Mock",
      "remediation": "Remove mock import. Use real database connection instead."
    }
  ],
  "correct_approach": "Connect to real test database using psycopg2.connect(...)"
}
```

## IRON LAW: Absolute Testing Requirements

<IRON_LAW>

These are **NOT GUIDELINES**. These are **MANDATORY REQUIREMENTS**.

Violating these = **AUTOMATIC TEST FAILURE**.

### The Six Iron Laws

1. **NO MOCK OBJECTS IN TESTS**
   - No `unittest.mock`, `jest.mock()`, `sinon.stub()`
   - No test doubles, fakes, or stubs
   - No mocking libraries of any kind

2. **NO UNIT TESTS - FUNCTIONAL TESTS ONLY**
   - Test complete workflows, not isolated functions
   - Test real user journeys
   - Test actual system integration

3. **NO PLACEHOLDERS OR STUBS IN PRODUCTION CODE**
   - No "TODO: replace with real implementation"
   - No conditional logic for test mode
   - No fake data generators for tests

4. **TEST WITH REAL BROWSERS**
   - Use Puppeteer MCP or Playwright MCP
   - Launch actual browsers (Chrome, Firefox, Safari)
   - Test real DOM, real JavaScript, real CSS

5. **TEST WITH REAL DATABASES**
   - Use actual D1, PostgreSQL, MySQL, etc.
   - Run real queries against real schemas
   - Test real transactions and constraints

6. **TEST WITH REAL APIs**
   - Make real HTTP requests
   - Connect to staging/test environments
   - Use real authentication and authorization

### Enforcement

These laws are enforced by:
- **post_tool_use.py hook**: Automatically scans test files for violations
- **This skill**: Provides anti-pattern detection and guidance
- **Shannon validators**: Automated checks during checkpoint/restore

</IRON_LAW>

---

## Why NO MOCKS?

### The Fundamental Problem

**Mock tests can pass while production fails.**

```python
# ❌ This test passes but proves NOTHING
def test_login():
    mock_db = Mock()
    mock_db.find_user.return_value = User(id=1, email="test@example.com")

    auth = AuthService(mock_db)
    result = auth.login("test@example.com", "password")

    assert result.success == True
    # ✓ Test passes
    # ✗ Real database query might fail
    # ✗ Real password hashing might fail
    # ✗ Real session creation might fail
```

### What Mocks Hide

1. **Integration Failures**: Real systems interact in complex ways
2. **Data Format Mismatches**: Mocks return convenient data, not realistic data
3. **Performance Issues**: Real queries may be slow, mocks are instant
4. **Race Conditions**: Real systems have timing issues, mocks don't
5. **Error Handling**: Real APIs return errors mocks don't simulate
6. **Schema Changes**: Database migrations break real code, not mocks

### The Shannon Solution

**Test the real thing, every time.**

```python
# ✅ This test actually validates production behavior
def test_login_functional():
    # REAL browser via Puppeteer MCP
    browser = puppeteer.launch()
    page = browser.new_page()

    # REAL navigation
    page.navigate("http://localhost:3000/login")

    # REAL form interaction
    page.fill("#email", "test@example.com")
    page.fill("#password", "SecurePass123!")
    page.click("button[type=submit]")

    # REAL database query happened
    # REAL password hash verification happened
    # REAL session token created
    # REAL redirect occurred

    # Assert on REAL result
    assert page.url() == "http://localhost:3000/dashboard"
    assert page.is_visible('[data-testid="user-menu"]')

    # Cleanup REAL data
    page.click('[data-testid="logout"]')
    browser.close()
```

---

## Rationalization Table

Shannon developers will be tempted to rationalize mock usage. **DO NOT ACCEPT THESE EXCUSES.**

| Rationalization | Why It's Wrong | Shannon Alternative |
|----------------|----------------|---------------------|
| "But mocks are faster!" | Speed doesn't matter if tests don't catch bugs. Real tests run in seconds with proper setup. | Use test database snapshots, parallel test execution |
| "But external APIs are expensive!" | Use staging/test API keys. Cost of bugs >> cost of API calls. | Use API test mode, request sandboxes |
| "But I can't control the database!" | Then you can't test your app properly. | Use Docker containers, test database per developer |
| "But mocks let me test edge cases!" | Only if those edge cases actually happen in production. | Seed test data with edge cases, trigger real errors |
| "But unit tests are best practice!" | Unit tests test units. You ship integrated systems. | Test the integrated system |
| "But refactoring will break all tests!" | If refactoring breaks tests, your design is coupled to implementation. | Test behavior, not implementation |
| "But CI/CD will be too slow!" | Slow CI is better than shipped bugs. Real tests parallelize well. | Use test parallelization, faster hardware |
| "But mocks help me test in isolation!" | Isolation doesn't exist in production. | Test real isolation: containers, separate DBs |
| "But the framework docs use mocks!" | The framework docs are wrong. | Follow Shannon, not framework conventions |
| "But I don't have access to a real X!" | Then you can't verify X works. | Get access to X (simulator, staging, Docker) |

### The Ultimate Test

**Ask yourself**: If this test passes, am I **CERTAIN** production will work?

- If you used mocks: **NO** ❌
- If you used real systems: **YES** ✅

---

## Testing Patterns by Technology

### 1. Web Applications (Puppeteer/Playwright MCP)

**When to use**: Any web UI functionality

**MCP Required**: `puppeteer` or `playwright`

#### Complete Test Pattern

```javascript
// ✅ CORRECT: Full functional test
const { test, expect } = require('@playwright/test');

test('User completes task workflow', async ({ page }) => {
  // 1. REAL navigation
  await page.goto('http://localhost:3000');

  // 2. REAL authentication
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="login"]');

  // Wait for REAL backend authentication
  await page.waitForURL('**/dashboard');

  // 3. REAL task creation
  await page.click('[data-testid="new-task"]');
  await page.fill('[data-testid="task-title"]', 'Complete testing');
  await page.selectOption('[data-testid="priority"]', 'high');
  await page.click('[data-testid="save"]');

  // Wait for REAL database insert + UI update
  await page.waitForSelector('[data-task-id="1"]');

  // 4. REAL data validation
  const taskTitle = await page.textContent('[data-task-id="1"] .title');
  expect(taskTitle).toBe('Complete testing');

  // 5. REAL task completion
  await page.click('[data-task-id="1"] [data-testid="complete"]');
  await page.waitForSelector('[data-task-id="1"].completed');

  // 6. REAL persistence check
  await page.reload();
  const isCompleted = await page.isVisible('[data-task-id="1"].completed');
  expect(isCompleted).toBe(true);

  // 7. REAL cleanup
  await page.click('[data-task-id="1"] [data-testid="delete"]');
  await page.waitForSelector('[data-task-id="1"]', { state: 'hidden' });
});
```

#### Testing Real-Time Features

```javascript
// ✅ CORRECT: Real WebSocket testing
test('Tasks sync in real-time', async ({ browser }) => {
  // Create TWO real browser contexts
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  // Both connect to REAL WebSocket server
  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  // User 1 creates task (REAL database insert)
  await page1.fill('[data-testid="task-title"]', 'Real-time task');
  await page1.click('[data-testid="save"]');

  // Wait for REAL WebSocket message delivery
  await page2.waitForSelector('[data-task-title="Real-time task"]', {
    timeout: 5000
  });

  // Verify REAL real-time sync worked
  const visible = await page2.isVisible('[data-task-title="Real-time task"]');
  expect(visible).toBe(true);

  await context1.close();
  await context2.close();
});
```

### 2. iOS Applications (xcodebuild/xcrun)

**When to use**: iOS SwiftUI or UIKit apps

**MCP Required**: `xc-mcp` (optional but recommended)

#### Complete Test Pattern

```swift
// ✅ CORRECT: Real iOS simulator test
import XCTest

class TaskAppUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()

        // Launch REAL app on REAL simulator
        app.launch()
    }

    func testCompleteTaskWorkflow() {
        // 1. REAL navigation
        app.buttons["Add Task"].tap()

        // 2. REAL input
        let titleField = app.textFields["Task Title"]
        titleField.tap()
        titleField.typeText("Write functional tests")

        // 3. REAL save (triggers Core Data insert)
        app.buttons["Save"].tap()

        // 4. Wait for REAL database write
        let taskCell = app.cells.containing(
            .staticText,
            identifier: "Write functional tests"
        ).element
        XCTAssertTrue(taskCell.waitForExistence(timeout: 5))

        // 5. REAL persistence test
        app.terminate()
        app.launch()
        XCTAssertTrue(taskCell.exists, "Task should persist")

        // 6. REAL cleanup
        taskCell.swipeLeft()
        app.buttons["Delete"].tap()
    }

    func testNetworkSync() {
        // Test REAL API integration
        app.buttons["Sync"].tap()

        // Wait for REAL network request
        let syncIndicator = app.activityIndicators["Syncing"]
        XCTAssertTrue(syncIndicator.waitForExistence(timeout: 2))

        // Wait for REAL API response
        XCTAssertFalse(
            syncIndicator.waitForNonExistence(timeout: 10),
            "Sync should complete in 10 seconds"
        )

        // Verify REAL data synced
        let syncedTask = app.cells["server-task-123"]
        XCTAssertTrue(syncedTask.exists)
    }
}
```

#### Bash Script for Real Simulator Testing

```bash
#!/bin/bash
# ✅ CORRECT: Real simulator test automation

# 1. Build for REAL simulator
xcodebuild build-for-testing \
  -scheme "TaskApp" \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -derivedDataPath ./build

# 2. Run tests on REAL simulator
xcodebuild test-without-building \
  -xctestrun ./build/Build/Products/TaskApp_iphonesimulator17.0-arm64.xctestrun \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -resultBundlePath ./TestResults

# 3. Check REAL results
if [ $? -eq 0 ]; then
  echo "✅ Functional tests passed"
  exit 0
else
  echo "❌ Tests failed"
  xcrun xcresulttool get --path ./TestResults
  exit 1
fi
```

### 3. API Testing (Real HTTP)

**When to use**: REST APIs, GraphQL, WebSockets

**MCP Required**: None (use built-in HTTP libraries)

#### Complete Test Pattern

```python
# ✅ CORRECT: Real API testing
import requests
import pytest

BASE_URL = "http://localhost:3000"

@pytest.fixture(scope="module")
def auth_token():
    """Create REAL user, return REAL token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )
    token = response.json()["token"]

    yield token

    # Cleanup: Delete REAL user
    requests.delete(
        f"{BASE_URL}/api/auth/delete",
        headers={"Authorization": f"Bearer {token}"}
    )

def test_complete_crud_workflow(auth_token):
    """Test CRUD with REAL database"""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # CREATE - REAL database INSERT
    create = requests.post(
        f"{BASE_URL}/api/tasks",
        headers=headers,
        json={"title": "Test Task", "priority": "high"}
    )
    assert create.status_code == 201
    task_id = create.json()["id"]

    # READ - REAL database SELECT
    read = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    assert read.status_code == 200
    assert read.json()["title"] == "Test Task"

    # UPDATE - REAL database UPDATE
    update = requests.put(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers=headers,
        json={"status": "completed"}
    )
    assert update.status_code == 200

    # Verify REAL update
    verify = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    assert verify.json()["status"] == "completed"

    # DELETE - REAL database DELETE
    delete = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    assert delete.status_code == 204

    # Verify REAL deletion
    check = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    assert check.status_code == 404
```

### 4. Database Testing (Real Databases)

**When to use**: Data persistence, queries, migrations

**MCP Required**: None (use database drivers)

#### Complete Test Pattern

```javascript
// ✅ CORRECT: Real PostgreSQL testing
const { Pool } = require('pg');

describe('Database Functional Tests', () => {
  let pool;

  beforeAll(async () => {
    // Connect to REAL test database
    pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'taskapp_test',
      user: 'test_user',
      password: 'test_password'
    });

    // Run REAL migrations
    await pool.query(`
      CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
  });

  beforeEach(async () => {
    // Clean REAL database
    await pool.query('TRUNCATE TABLE tasks RESTART IDENTITY CASCADE');
  });

  test('INSERT creates task', async () => {
    // REAL database INSERT
    const result = await pool.query(
      'INSERT INTO tasks (title) VALUES ($1) RETURNING *',
      ['Test Task']
    );

    expect(result.rows).toHaveLength(1);
    expect(result.rows[0].title).toBe('Test Task');
    expect(result.rows[0].id).toBeDefined();
  });

  test('Transaction rollback works', async () => {
    const client = await pool.connect();

    try {
      // Start REAL transaction
      await client.query('BEGIN');
      await client.query('INSERT INTO tasks (title) VALUES ($1)', ['Task 1']);
      await client.query('INSERT INTO tasks (title) VALUES ($1)', ['Task 2']);

      // Rollback REAL transaction
      await client.query('ROLLBACK');
    } finally {
      client.release();
    }

    // Verify REAL rollback
    const result = await pool.query('SELECT * FROM tasks');
    expect(result.rows).toHaveLength(0);
  });

  afterAll(async () => {
    await pool.query('DROP TABLE IF EXISTS tasks CASCADE');
    await pool.end();
  });
});
```

---

## Anti-Pattern Detection

### Automatic Violation Detection

This skill includes patterns to automatically detect violations:

```python
# Shannon will REJECT these patterns automatically

# ❌ Mock imports
from unittest.mock import Mock, patch, MagicMock
import mock
from jest import mock as jest_mock

# ❌ Stub creation
stub_function = lambda x: "fake_result"
fake_db = FakeDatabase()
mock_api = MockAPIClient()

# ❌ Conditional test logic
if os.getenv('TESTING'):
    return {"status": "success"}  # Bypasses real logic

# ❌ In-memory databases
db = InMemoryDatabase()
sqlite_memory = sqlite3.connect(':memory:')  # For integration tests

# ❌ Hard-coded responses
class FakeAPI:
    def get_user(self, id):
        return {"id": id, "name": "Test User"}
```

### Red Flags Checklist

Before accepting ANY test, verify it has:

```markdown
☐ NO mock imports
☐ NO stub functions
☐ NO fake classes
☐ REAL browser/simulator launched
☐ REAL HTTP requests made
☐ REAL database queries executed
☐ REAL assertions on real data
☐ REAL cleanup of real resources
```

---

## Common Violations and Solutions

### Violation 1: Mocking External APIs

```python
# ❌ WRONG: Mocking third-party API
from unittest.mock import patch

@patch('stripe.Charge.create')
def test_payment(mock_create):
    mock_create.return_value = {"id": "ch_123", "status": "succeeded"}
    result = process_payment(1000)
    assert result["status"] == "succeeded"
```

```python
# ✅ CORRECT: Use real API in test mode
import stripe

def test_payment():
    # Use REAL Stripe API with test key
    stripe.api_key = os.getenv('STRIPE_TEST_KEY')

    # Make REAL API call
    charge = stripe.Charge.create(
        amount=1000,
        currency='usd',
        source='tok_visa'  # Stripe test token
    )

    # Assert on REAL response
    assert charge.status == 'succeeded'
    assert charge.id.startswith('ch_')
```

### Violation 2: In-Memory Database for Integration Tests

```python
# ❌ WRONG: In-memory database
def test_user_creation():
    db = InMemoryDatabase()
    user = db.create_user(email="test@example.com")
    assert user.email == "test@example.com"
```

```python
# ✅ CORRECT: Real test database
import psycopg2

def test_user_creation():
    # Connect to REAL test database
    conn = psycopg2.connect(
        dbname="taskapp_test",
        user="test_user",
        password="test_password",
        host="localhost"
    )
    cursor = conn.cursor()

    # REAL database INSERT
    cursor.execute(
        "INSERT INTO users (email) VALUES (%s) RETURNING id, email",
        ("test@example.com",)
    )
    user = cursor.fetchone()

    # Assert on REAL data
    assert user[1] == "test@example.com"

    # Cleanup REAL data
    cursor.execute("DELETE FROM users WHERE id = %s", (user[0],))
    conn.commit()
    conn.close()
```

### Violation 3: Mocking Time/Dates

```javascript
// ❌ WRONG: Mocking system time
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));

test('creates timestamp', () => {
  const task = createTask('Test');
  expect(task.createdAt).toEqual(new Date('2024-01-01'));
});
```

```javascript
// ✅ CORRECT: Parameterize dates
function createTask(title, createdAt = new Date()) {
  return { title, createdAt };
}

test('creates timestamp', () => {
  const testDate = new Date('2024-01-01');
  const task = createTask('Test', testDate);
  expect(task.createdAt).toEqual(testDate);
});
```

### Violation 4: Stubbing Network Requests

```javascript
// ❌ WRONG: Stubbing fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ data: 'fake' })
  })
);

test('fetches data', async () => {
  const data = await fetchUserData(1);
  expect(data.data).toBe('fake');
});
```

```javascript
// ✅ CORRECT: Real HTTP request to test server
test('fetches data', async () => {
  // Make REAL HTTP request
  const response = await fetch('http://localhost:3000/api/users/1');
  const data = await response.json();

  // Assert on REAL response
  expect(data).toHaveProperty('id');
  expect(data).toHaveProperty('email');
  expect(response.status).toBe(200);
});
```

---

## Test Environment Setup

### Required Infrastructure

For functional testing, you MUST have:

1. **Real Test Database**
   - PostgreSQL test instance
   - SQLite test file
   - MongoDB test instance
   - D1 test database

2. **Real Test Server**
   - API server running on localhost
   - WebSocket server if needed
   - Background workers if needed

3. **Real Browser/Simulator**
   - Chrome/Firefox installed
   - Puppeteer/Playwright configured
   - iOS Simulator available

4. **Real Test Data**
   - Seed scripts for test data
   - Migration scripts
   - Cleanup scripts

### Setup Example: Node.js API

```javascript
// setup-tests.js - REAL test environment
const { Pool } = require('pg');
const app = require('./server');

let server;
let pool;

// Setup REAL infrastructure
beforeAll(async () => {
  // 1. Connect to REAL test database
  pool = new Pool({
    database: 'taskapp_test',
    user: 'test_user',
    password: 'test_password'
  });

  // 2. Run REAL migrations
  await pool.query(`
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email VARCHAR(255) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tasks (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id),
      title VARCHAR(255) NOT NULL,
      status VARCHAR(50) DEFAULT 'pending'
    );
  `);

  // 3. Start REAL server
  server = app.listen(3000);

  // Wait for REAL server to be ready
  await new Promise(resolve => {
    server.on('listening', resolve);
  });
});

// Clean REAL database between tests
beforeEach(async () => {
  await pool.query('TRUNCATE TABLE tasks, users RESTART IDENTITY CASCADE');
});

// Cleanup REAL infrastructure
afterAll(async () => {
  await pool.query('DROP TABLE IF EXISTS tasks, users CASCADE');
  await pool.end();
  await new Promise(resolve => server.close(resolve));
});
```

---

## Enforcement via post_tool_use.py Hook

Shannon V4 includes automatic enforcement:

```python
# Pseudo-code: post_tool_use.py

def check_test_file(file_path, content):
    """Scan test files for NO MOCKS violations"""

    violations = []

    # Check for mock imports
    mock_imports = [
        'from unittest.mock import',
        'import mock',
        'jest.mock(',
        'sinon.stub(',
        '@patch(',
    ]

    for pattern in mock_imports:
        if pattern in content:
            violations.append(f"VIOLATION: Mock import detected: {pattern}")

    # Check for stub patterns
    stub_patterns = [
        'Mock()',
        'MagicMock()',
        'fake_',
        'stub_',
        'FakeDatabase',
        'InMemoryDatabase'
    ]

    for pattern in stub_patterns:
        if pattern in content:
            violations.append(f"VIOLATION: Stub pattern detected: {pattern}")

    # Check for real system usage
    real_patterns = [
        'puppeteer.launch',
        'playwright.chromium.launch',
        'XCUIApplication',
        'requests.post',
        'fetch(',
        'Pool(',
        'psycopg2.connect'
    ]

    has_real_usage = any(pattern in content for pattern in real_patterns)

    if not has_real_usage:
        violations.append("VIOLATION: No real system usage detected")

    return violations

# If violations found:
# 1. Log to Shannon context
# 2. Trigger functional-testing skill
# 3. Provide remediation guidance
```

---

## Testing Decision Tree

```
Need to write a test?
│
├─ Does it test user-facing behavior?
│  ├─ YES → Functional test with REAL browser ✅
│  └─ NO → Don't test it ❌
│
├─ Does it test API endpoints?
│  ├─ YES → Functional test with REAL HTTP requests ✅
│  └─ NO → Don't test it ❌
│
├─ Does it test data persistence?
│  ├─ YES → Functional test with REAL database ✅
│  └─ NO → Don't test it ❌
│
└─ Does it test internal functions?
   ├─ Test through user-facing behavior ✅
   └─ Unit test with mocks ❌ FORBIDDEN
```

---

## Success Criteria

This skill succeeds if:

1. ✅ **Zero mock imports in generated test code**
   - No `unittest.mock`, `jest.mock()`, `sinon.stub()`, `@patch` imports
   - No stub functions or fake implementations
   - All test code uses real system connections

2. ✅ **Real system connections verified**
   - Web tests: `puppeteer.launch()` or `playwright.chromium.launch()` present
   - iOS tests: `XCUIApplication()` or `xcrun` commands present
   - API tests: Real HTTP requests (`requests.post`, `fetch()`) present
   - Database tests: Real database connections (`psycopg2.connect`, `Pool()`) present

3. ✅ **Complete test workflow coverage**
   - Tests cover full user journey from start to finish
   - Tests include setup, action, assertion, cleanup phases
   - Tests verify real persistence (reload pages, reconnect to DB)

4. ✅ **Cleanup procedures included**
   - Test data deleted after test runs
   - Database connections closed
   - Browser instances terminated
   - Resources released properly

5. ✅ **Violation scanning passed**
   - post_tool_use.py hook detected no violations
   - Manual review confirms real system usage
   - No conditional test logic or test-mode branches in production code

Validation:
```python
def validate_functional_test(test_code):
    # Scan for forbidden patterns
    forbidden = [
        'unittest.mock', 'jest.mock', 'sinon.stub', '@patch',
        'Mock()', 'MagicMock()', 'FakeDatabase', 'InMemoryDatabase',
        'if os.getenv("TESTING")', 'if ENV == "test"'
    ]
    for pattern in forbidden:
        assert pattern not in test_code, f"VIOLATION: Found forbidden pattern: {pattern}"

    # Verify real system usage
    real_patterns = {
        'web': ['puppeteer.launch', 'playwright.chromium.launch', 'page.goto'],
        'ios': ['XCUIApplication', 'xcrun simctl', 'xcodebuild test'],
        'api': ['requests.post', 'fetch(', 'http.request'],
        'database': ['psycopg2.connect', 'Pool(', 'mongoose.connect']
    }

    has_real_usage = any(
        any(pattern in test_code for pattern in patterns)
        for patterns in real_patterns.values()
    )
    assert has_real_usage, "VIOLATION: No real system usage detected"

    # Verify cleanup
    cleanup_patterns = ['finally:', 'tearDown', 'afterEach', 'DELETE FROM', 'close()', 'terminate()']
    has_cleanup = any(pattern in test_code for pattern in cleanup_patterns)
    assert has_cleanup, "WARNING: No cleanup procedures detected"
```

## Examples

### Example 1: Web Application with Puppeteer MCP

**Input:**
```
platform: "web"
test_mode: "e2e"
feature: "User login and task creation"
```

**Process:**
1. Detect platform: "web" → Recommend Puppeteer MCP
2. Check MCP availability: Puppeteer installed ✓
3. Select template: "Complete E2E workflow"
4. Customize: Add login flow + task creation flow
5. Add cleanup: Delete test task after completion
6. Scan violations: No mocks detected ✓

**Output:**
```javascript
const { test, expect } = require('@playwright/test');

test('User logs in and creates task', async ({ page }) => {
  // REAL browser navigation
  await page.goto('http://localhost:3000/login');

  // REAL authentication
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="login"]');
  await page.waitForURL('**/dashboard');

  // REAL task creation
  await page.click('[data-testid="new-task"]');
  await page.fill('[data-testid="task-title"]', 'Test Task');
  await page.click('[data-testid="save"]');

  // Wait for REAL database insert
  await page.waitForSelector('[data-task-id="1"]');

  // Verify REAL persistence
  await page.reload();
  const taskVisible = await page.isVisible('[data-task-id="1"]');
  expect(taskVisible).toBe(true);

  // REAL cleanup
  await page.click('[data-task-id="1"] [data-testid="delete"]');
});
```

### Example 2: API Testing with Manual Fallback

**Input:**
```
platform: "api"
test_mode: "integration"
feature: "POST /api/tasks endpoint"
mcp_available: []  // No MCPs installed
```

**Process:**
1. Detect platform: "api" → No MCP required (built-in HTTP)
2. Check MCP availability: None installed
3. Provide fallback: Manual cURL testing procedures
4. Generate test: Python requests library example
5. Add cleanup: DELETE request after test

**Output:**
```markdown
## Manual API Testing Procedure

Since no MCPs are required for API testing, use built-in HTTP libraries:

### Python Test Example:
```python
import requests

def test_create_task_functional():
    # REAL API authentication
    auth_response = requests.post(
        'http://localhost:3000/api/auth/login',
        json={'email': 'test@example.com', 'password': 'SecurePass123!'}
    )
    token = auth_response.json()['token']

    # REAL task creation
    create_response = requests.post(
        'http://localhost:3000/api/tasks',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test Task', 'priority': 'high'}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()['id']

    # Verify REAL database persistence
    get_response = requests.get(
        f'http://localhost:3000/api/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert get_response.json()['title'] == 'Test Task'

    # REAL cleanup
    delete_response = requests.delete(
        f'http://localhost:3000/api/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert delete_response.status_code == 204
```

## Common Pitfalls

### Pitfall 1: Using In-Memory Database for Integration Tests

**Wrong:**
```python
def test_user_creation():
    db = InMemoryDatabase()  # ❌ VIOLATION: Not a real database
    user = db.create_user(email="test@example.com")
    assert user.email == "test@example.com"
```

**Right:**
```python
import psycopg2

def test_user_creation():
    # REAL test database connection
    conn = psycopg2.connect(
        dbname="taskapp_test",
        user="test_user",
        password="test_password"
    )
    cursor = conn.cursor()

    # REAL INSERT
    cursor.execute(
        "INSERT INTO users (email) VALUES (%s) RETURNING id, email",
        ("test@example.com",)
    )
    user = cursor.fetchone()

    # Assert on REAL data
    assert user[1] == "test@example.com"

    # Cleanup REAL data
    cursor.execute("DELETE FROM users WHERE id = %s", (user[0],))
    conn.commit()
    conn.close()
```

**Why:** In-memory databases don't validate production behavior. Real database tests catch schema issues, constraint violations, transaction problems, and performance issues.

### Pitfall 2: Mocking External APIs

**Wrong:**
```python
from unittest.mock import patch  # ❌ VIOLATION: Mock import

@patch('stripe.Charge.create')
def test_payment(mock_create):
    mock_create.return_value = {"id": "ch_123", "status": "succeeded"}
    result = process_payment(1000)
    assert result["status"] == "succeeded"
```

**Right:**
```python
import stripe

def test_payment():
    # REAL Stripe API with test key
    stripe.api_key = os.getenv('STRIPE_TEST_KEY')

    # REAL API call
    charge = stripe.Charge.create(
        amount=1000,
        currency='usd',
        source='tok_visa'  # Stripe test token
    )

    # Assert on REAL response
    assert charge.status == 'succeeded'
    assert charge.id.startswith('ch_')
```

**Why:** Mocking external APIs hides integration failures, API contract changes, authentication issues, rate limiting problems, and network errors. Real API tests catch these issues.

### Pitfall 3: Stubbing System Time

**Wrong:**
```javascript
// ❌ VIOLATION: Mocking system time
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));

test('creates timestamp', () => {
  const task = createTask('Test');
  expect(task.createdAt).toEqual(new Date('2024-01-01'));
});
```

**Right:**
```javascript
// Parameterize time dependency
function createTask(title, createdAt = new Date()) {
  return { title, createdAt };
}

test('creates timestamp', () => {
  const testDate = new Date('2024-01-01');
  const task = createTask('Test', testDate);
  expect(task.createdAt).toEqual(testDate);

  // Or test with real time
  const taskNow = createTask('Test');
  expect(taskNow.createdAt).toBeInstanceOf(Date);
  expect(Date.now() - taskNow.createdAt.getTime()).toBeLessThan(100);
});
```

**Why:** Fake timers hide timing bugs, race conditions, timezone issues, and date calculation errors. Real time testing catches these issues.

---

## Summary

### The Shannon Testing Philosophy

1. **NEVER use mocks** - Test real behavior, not mock implementations
2. **ALWAYS use real systems** - Real browsers, real databases, real APIs
3. **Test like production** - If it's different in tests, it's not validated
4. **Validate actual behavior** - Assert on real data, real responses, real state
5. **Enforce ruthlessly** - Reject any test that violates NO MOCKS

### Quick Reference

```markdown
❌ NEVER:
- jest.mock() / unittest.mock
- Stub functions
- Fake implementations
- In-memory databases (for integration)
- Hard-coded test responses
- Conditional test logic

✅ ALWAYS:
- Real browsers (Puppeteer/Playwright MCP)
- Real simulators (xcodebuild/xcrun)
- Real HTTP requests
- Real databases
- Real user workflows
- Real data assertions
- Real cleanup
```

### Result

**Tests that actually validate production behavior and catch real bugs before deployment.**

When you use functional testing correctly:
- Production bugs are caught in tests
- Refactoring is safe (tests verify behavior, not implementation)
- Confidence in deployments is high
- Test failures indicate real problems
- Code coverage reflects real usage

When you use mocks:
- Tests pass, production fails
- Refactoring breaks tests
- False confidence in code quality
- Test failures are often false positives
- Code coverage is meaningless

---

## See Also

- `references/TESTING_PHILOSOPHY.md` - Full testing manifesto (1051 lines)
- `examples/puppeteer-browser-test.md` - Complete browser test examples
- `examples/ios-simulator-test.md` - Complete iOS test examples
- `examples/api-functional-test.md` - Complete API test examples
- `examples/database-functional-test.md` - Complete database test examples
- `anti-patterns/mock-violations.md` - Comprehensive violation catalog
- `anti-patterns/unit-test-violations.md` - Why unit tests fail
