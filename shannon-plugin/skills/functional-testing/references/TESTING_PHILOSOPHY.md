# TESTING_PHILOSOPHY.md - Shannon Functional Testing Mandate

## Purpose Statement

Shannon enforces **FUNCTIONAL TESTING FIRST - NO MOCKS EVER**. All tests must interact with real systems, real browsers, real databases, and real APIs. This philosophy ensures that tests validate actual behavior, not mock implementations.

**Core Principle**: Tests should fail when production would fail. Mocks create a false sense of security.

---

## The NO MOCKS Mandate

### Why This Matters

**The Problem with Mocks**:
- Mock objects don't test real integration points
- Mocks hide production bugs until it's too late
- Mocks create false confidence in code quality
- Mocks require constant maintenance when implementations change
- Mock tests can pass while production fails

**Shannon's Solution**: Use real components exclusively. If a test requires mocking, it's testing the wrong layer.

### What NO MOCKS Means

You **MUST NEVER**:
- Use `unittest.mock` or `jest.mock()`
- Create stub functions or fake implementations
- Use in-memory databases for integration tests
- Mock API responses in integration tests
- Create "test doubles" or "test stubs"
- Use `sinon.stub()` or similar mocking libraries

You **MUST ALWAYS**:
- Use real browsers via Puppeteer/Playwright MCP
- Use real iOS simulators via xcodebuild/xcrun
- Use real HTTP requests to test servers
- Use real databases with real schemas
- Test actual user workflows end-to-end

### Enforcement Strategy

**Pre-Test Validation Checklist**:
```markdown
Before accepting ANY test, verify:
☐ No mock imports (unittest.mock, jest.mock, sinon, etc.)
☐ No stub functions created
☐ Real systems initialized (browser, server, database)
☐ Real interactions performed
☐ Real assertions on real data
☐ Cleanup properly handles real resources
```

**Red Flags (Immediate Rejection)**:
- Variable names containing "mock", "stub", "fake"
- Imports from mocking libraries
- In-memory databases when testing persistence
- Hard-coded "test" responses instead of real API calls
- Comments like "TODO: replace with real integration"

---

## Testing by Platform

### Web Applications - Puppeteer/Playwright MCP

**When to Use**: Any web application functionality requiring browser interaction

**Why Real Browsers**:
- Tests actual DOM rendering
- Validates JavaScript execution
- Tests CSS and visual behavior
- Catches browser-specific bugs
- Validates network requests
- Tests real user interactions

#### Complete Testing Pattern

```javascript
// ✅ CORRECT: Functional test with real browser
const { test, expect } = require('@playwright/test');

test('User can create and view task', async ({ page }) => {
  // 1. Real browser navigation
  await page.goto('http://localhost:3000');

  // 2. Wait for real backend to load
  await page.waitForSelector('[data-testid="task-form"]');

  // 3. Real form interaction
  await page.fill('[data-testid="task-title"]', 'Complete testing docs');
  await page.fill('[data-testid="task-description"]', 'Write comprehensive testing guide');
  await page.selectOption('[data-testid="task-priority"]', 'high');

  // 4. Real form submission (triggers real API call + DB insert)
  await page.click('[data-testid="submit-task"]');

  // 5. Wait for REAL backend response and DOM update
  await page.waitForSelector('[data-testid="task-1"]');

  // 6. Assert on REAL data from REAL database
  const taskTitle = await page.textContent('[data-testid="task-1-title"]');
  expect(taskTitle).toBe('Complete testing docs');

  // 7. Test real navigation
  await page.click('[data-testid="task-1"]');
  await page.waitForSelector('[data-testid="task-detail"]');

  // 8. Verify real data persistence
  const detailTitle = await page.textContent('[data-testid="detail-title"]');
  expect(detailTitle).toBe('Complete testing docs');

  // 9. Cleanup real data (optional, depends on test isolation strategy)
  await page.click('[data-testid="delete-task"]');
  await page.waitForSelector('[data-testid="task-1"]', { state: 'hidden' });
});
```

```javascript
// ❌ WRONG: Mock-based test
test('User can create task', async () => {
  // BAD: Mocking API
  jest.mock('./api', () => ({
    createTask: jest.fn().mockResolvedValue({ id: 1, title: 'Test' })
  }));

  // BAD: Not testing real behavior
  const result = await createTask({ title: 'Test' });
  expect(result.id).toBe(1);

  // This test proves nothing about production behavior
});
```

#### Testing Complex Interactions

```javascript
// ✅ CORRECT: Real-time updates testing
test('Tasks update in real-time via WebSocket', async ({ browser }) => {
  // Open two real browser contexts
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  // Both pages connect to real WebSocket server
  await page1.goto('http://localhost:3000');
  await page2.goto('http://localhost:3000');

  // User 1 creates task (real database insert)
  await page1.fill('[data-testid="task-title"]', 'Shared Task');
  await page1.click('[data-testid="submit-task"]');

  // Wait for REAL WebSocket message + DOM update on User 2's page
  await page2.waitForSelector('[data-task-title="Shared Task"]', { timeout: 5000 });

  // Verify real-time update worked
  const taskVisible = await page2.isVisible('[data-task-title="Shared Task"]');
  expect(taskVisible).toBe(true);

  // Cleanup
  await context1.close();
  await context2.close();
});
```

#### Testing Authentication Flows

```javascript
// ✅ CORRECT: Real authentication flow
test('User can register, login, and access protected route', async ({ page }) => {
  // 1. Real registration (creates real user in database)
  await page.goto('http://localhost:3000/register');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="register-button"]');

  // 2. Wait for REAL backend to process registration
  await page.waitForURL('**/login');

  // 3. Real login (validates against real database)
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="login-button"]');

  // 4. Wait for real JWT token + session creation
  await page.waitForURL('**/dashboard');

  // 5. Verify real authentication state
  const welcomeText = await page.textContent('[data-testid="welcome"]');
  expect(welcomeText).toContain('test@example.com');

  // 6. Test protected route (real token validation)
  await page.goto('http://localhost:3000/api/tasks');
  await page.waitForSelector('[data-testid="task-list"]');

  // 7. Cleanup (delete real user from database)
  await page.goto('http://localhost:3000/settings');
  await page.click('[data-testid="delete-account"]');
  await page.click('[data-testid="confirm-delete"]');
});
```

### iOS Applications - iOS Simulator Testing

**When to Use**: Any iOS SwiftUI or UIKit application

**Why Real Simulators**:
- Tests actual iOS runtime behavior
- Validates SwiftUI rendering
- Tests real iOS APIs
- Catches iOS version-specific bugs
- Validates app lifecycle
- Tests real user interactions

#### Complete Testing Pattern

```bash
#!/bin/bash
# ✅ CORRECT: Real simulator testing

# 1. Build app for simulator (real compilation)
xcodebuild build-for-testing \
  -scheme "TaskApp" \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -derivedDataPath ./build

# 2. Run XCUITests on REAL simulator
xcodebuild test-without-building \
  -xctestrun ./build/Build/Products/TaskApp_iphonesimulator17.0-arm64.xctestrun \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -resultBundlePath ./TestResults

# 3. Check test results
if [ $? -eq 0 ]; then
  echo "✅ Functional tests passed on real simulator"
else
  echo "❌ Tests failed - check ./TestResults for details"
  exit 1
fi
```

```swift
// ✅ CORRECT: XCUITest with real simulator
import XCTest

class TaskAppUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()

        // Launch REAL app on REAL simulator
        app.launch()
    }

    func testUserCanCreateTask() {
        // 1. Real navigation
        app.buttons["Add Task"].tap()

        // 2. Real text input
        let titleField = app.textFields["Task Title"]
        titleField.tap()
        titleField.typeText("Write tests")

        let descriptionField = app.textViews["Task Description"]
        descriptionField.tap()
        descriptionField.typeText("Complete functional testing guide")

        // 3. Real form submission (triggers real Core Data save)
        app.buttons["Save"].tap()

        // 4. Wait for REAL database write + UI update
        let taskCell = app.cells.containing(.staticText, identifier: "Write tests").element
        XCTAssertTrue(taskCell.waitForExistence(timeout: 5))

        // 5. Verify real data persistence
        app.terminate()
        app.launch()
        XCTAssertTrue(taskCell.exists, "Task should persist after app restart")

        // 6. Cleanup (delete from real database)
        taskCell.swipeLeft()
        app.buttons["Delete"].tap()
    }

    func testRealTimeSync() {
        // Test real network requests and data sync
        app.buttons["Sync"].tap()

        // Wait for REAL API call to complete
        let syncIndicator = app.activityIndicators["Syncing"]
        XCTAssertTrue(syncIndicator.waitForExistence(timeout: 2))
        XCTAssertFalse(syncIndicator.waitForNonExistence(timeout: 10),
                      "Sync should complete within 10 seconds")

        // Verify real data was synced from real backend
        let syncedTask = app.cells["server-task-123"]
        XCTAssertTrue(syncedTask.exists)
    }
}

extension XCUIElement {
    func waitForNonExistence(timeout: TimeInterval) -> Bool {
        let predicate = NSPredicate(format: "exists == false")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: self)
        let result = XCTWaiter().wait(for: [expectation], timeout: timeout)
        return result == .completed
    }
}
```

```swift
// ❌ WRONG: Unit test with mocks
import XCTest
@testable import TaskApp

class TaskServiceTests: XCTestCase {
    func testCreateTask() {
        // BAD: Mocking database
        let mockDB = MockDatabase()
        let service = TaskService(database: mockDB)

        // BAD: Not testing real behavior
        let task = service.createTask(title: "Test")
        XCTAssertEqual(task.title, "Test")

        // This proves nothing about production behavior
    }
}
```

### API Testing - Real HTTP Requests

**When to Use**: Testing REST APIs, GraphQL endpoints, WebSocket servers

**Why Real Requests**:
- Tests actual network layer
- Validates request/response handling
- Tests real database queries
- Catches serialization bugs
- Validates authentication/authorization
- Tests real error handling

#### Complete Testing Pattern

```javascript
// ✅ CORRECT: Real API testing
const fetch = require('node-fetch');

describe('Task API - Functional Tests', () => {
  const BASE_URL = 'http://localhost:3000';
  let authToken;
  let taskId;

  beforeAll(async () => {
    // Setup: Create real user in database
    const response = await fetch(`${BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'test@example.com',
        password: 'SecurePass123!'
      })
    });

    const data = await response.json();
    authToken = data.token; // Real JWT token
  });

  test('POST /api/tasks - Creates task in database', async () => {
    // 1. Real HTTP POST request
    const response = await fetch(`${BASE_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({
        title: 'Test Task',
        description: 'Functional test',
        priority: 'high'
      })
    });

    // 2. Verify real response
    expect(response.status).toBe(201);
    const task = await response.json();

    // 3. Verify real data structure
    expect(task).toHaveProperty('id');
    expect(task.title).toBe('Test Task');
    expect(task.priority).toBe('high');

    // 4. Save for later tests
    taskId = task.id;
  });

  test('GET /api/tasks/:id - Retrieves task from database', async () => {
    // Real HTTP GET request
    const response = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });

    // Verify real database retrieval
    expect(response.status).toBe(200);
    const task = await response.json();
    expect(task.id).toBe(taskId);
    expect(task.title).toBe('Test Task');
  });

  test('PUT /api/tasks/:id - Updates task in database', async () => {
    // Real HTTP PUT request
    const response = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({
        title: 'Updated Task',
        status: 'completed'
      })
    });

    expect(response.status).toBe(200);

    // Verify real database update
    const getResponse = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    const updatedTask = await getResponse.json();
    expect(updatedTask.title).toBe('Updated Task');
    expect(updatedTask.status).toBe('completed');
  });

  test('DELETE /api/tasks/:id - Removes task from database', async () => {
    // Real HTTP DELETE request
    const response = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${authToken}` }
    });

    expect(response.status).toBe(204);

    // Verify real database deletion
    const getResponse = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    expect(getResponse.status).toBe(404);
  });

  afterAll(async () => {
    // Cleanup: Delete real user from database
    await fetch(`${BASE_URL}/api/auth/delete`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
  });
});
```

```python
# ✅ CORRECT: Python API testing with requests
import requests
import pytest

BASE_URL = "http://localhost:3000"

@pytest.fixture(scope="module")
def auth_token():
    """Create real user and return auth token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )
    data = response.json()
    token = data["token"]

    yield token

    # Cleanup: Delete real user
    requests.delete(
        f"{BASE_URL}/api/auth/delete",
        headers={"Authorization": f"Bearer {token}"}
    )

def test_create_task_real_database(auth_token):
    """Test task creation with real database"""
    # Real HTTP POST
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        },
        json={
            "title": "Python Test Task",
            "priority": "high"
        }
    )

    # Verify real response
    assert response.status_code == 201
    task = response.json()
    assert "id" in task
    assert task["title"] == "Python Test Task"

    # Cleanup: Delete from real database
    requests.delete(
        f"{BASE_URL}/api/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
```

### Database Testing - Real Test Databases

**When to Use**: Testing data persistence, queries, migrations

**Why Real Databases**:
- Tests actual SQL/query behavior
- Validates schema correctness
- Tests real transactions
- Catches database-specific bugs
- Tests real indexes and performance
- Validates migrations

#### Complete Testing Pattern

```javascript
// ✅ CORRECT: Real database testing
const { Pool } = require('pg');

describe('Database Tests - Functional', () => {
  let pool;

  beforeAll(async () => {
    // Connect to REAL test database
    pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'task_app_test',
      user: 'test_user',
      password: 'test_password'
    });

    // Run real migrations
    await pool.query(`
      CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        priority VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
  });

  beforeEach(async () => {
    // Clean real database before each test
    await pool.query('TRUNCATE TABLE tasks RESTART IDENTITY CASCADE');
  });

  test('INSERT creates task in real database', async () => {
    // Real database INSERT
    const result = await pool.query(
      'INSERT INTO tasks (title, description, priority) VALUES ($1, $2, $3) RETURNING *',
      ['Test Task', 'Description', 'high']
    );

    // Verify real insertion
    expect(result.rows).toHaveLength(1);
    expect(result.rows[0].title).toBe('Test Task');
    expect(result.rows[0].id).toBeDefined();
  });

  test('SELECT retrieves tasks from real database', async () => {
    // Insert real data
    await pool.query(
      'INSERT INTO tasks (title, priority) VALUES ($1, $2), ($3, $4)',
      ['Task 1', 'high', 'Task 2', 'low']
    );

    // Real database SELECT
    const result = await pool.query('SELECT * FROM tasks ORDER BY priority DESC');

    // Verify real query results
    expect(result.rows).toHaveLength(2);
    expect(result.rows[0].title).toBe('Task 1'); // High priority first
    expect(result.rows[1].title).toBe('Task 2');
  });

  test('UPDATE modifies task in real database', async () => {
    // Insert real data
    const insertResult = await pool.query(
      'INSERT INTO tasks (title, status) VALUES ($1, $2) RETURNING id',
      ['Task to Update', 'pending']
    );
    const taskId = insertResult.rows[0].id;

    // Real database UPDATE
    await pool.query(
      'UPDATE tasks SET status = $1 WHERE id = $2',
      ['completed', taskId]
    );

    // Verify real update
    const selectResult = await pool.query('SELECT * FROM tasks WHERE id = $1', [taskId]);
    expect(selectResult.rows[0].status).toBe('completed');
  });

  test('DELETE removes task from real database', async () => {
    // Insert real data
    const insertResult = await pool.query(
      'INSERT INTO tasks (title) VALUES ($1) RETURNING id',
      ['Task to Delete']
    );
    const taskId = insertResult.rows[0].id;

    // Real database DELETE
    await pool.query('DELETE FROM tasks WHERE id = $1', [taskId]);

    // Verify real deletion
    const selectResult = await pool.query('SELECT * FROM tasks WHERE id = $1', [taskId]);
    expect(selectResult.rows).toHaveLength(0);
  });

  test('Transaction rollback works in real database', async () => {
    const client = await pool.connect();

    try {
      // Start real transaction
      await client.query('BEGIN');

      await client.query('INSERT INTO tasks (title) VALUES ($1)', ['Task 1']);
      await client.query('INSERT INTO tasks (title) VALUES ($1)', ['Task 2']);

      // Rollback real transaction
      await client.query('ROLLBACK');
    } finally {
      client.release();
    }

    // Verify real rollback
    const result = await pool.query('SELECT * FROM tasks');
    expect(result.rows).toHaveLength(0);
  });

  afterAll(async () => {
    // Drop real test database
    await pool.query('DROP TABLE IF EXISTS tasks CASCADE');
    await pool.end();
  });
});
```

---

## Testing Templates

### Complete Web Application Test Suite

```javascript
// ✅ CORRECT: Comprehensive functional test suite
const { test, expect } = require('@playwright/test');

test.describe('Task Management - Complete Functional Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to real application
    await page.goto('http://localhost:3000');
  });

  test('Complete user workflow: Register → Login → Create Task → Edit → Delete', async ({ page }) => {
    // 1. REGISTRATION (real database insert)
    await page.click('[data-testid="register-link"]');
    await page.fill('[data-testid="email"]', `test-${Date.now()}@example.com`);
    await page.fill('[data-testid="password"]', 'SecurePass123!');
    await page.click('[data-testid="register-submit"]');
    await page.waitForURL('**/login');

    // 2. LOGIN (real authentication)
    await page.fill('[data-testid="email"]', await page.inputValue('[data-testid="email"]'));
    await page.fill('[data-testid="password"]', 'SecurePass123!');
    await page.click('[data-testid="login-submit"]');
    await page.waitForURL('**/dashboard');

    // 3. CREATE TASK (real API call + database insert)
    await page.click('[data-testid="new-task"]');
    await page.fill('[data-testid="task-title"]', 'Integration Test Task');
    await page.fill('[data-testid="task-description"]', 'Complete functional test');
    await page.selectOption('[data-testid="task-priority"]', 'high');
    await page.click('[data-testid="save-task"]');
    await page.waitForSelector('[data-task-title="Integration Test Task"]');

    // 4. EDIT TASK (real update)
    await page.click('[data-task-title="Integration Test Task"]');
    await page.click('[data-testid="edit-task"]');
    await page.fill('[data-testid="task-title"]', 'Updated Test Task');
    await page.click('[data-testid="save-task"]');
    await page.waitForSelector('[data-task-title="Updated Test Task"]');

    // 5. DELETE TASK (real deletion)
    await page.click('[data-testid="delete-task"]');
    await page.click('[data-testid="confirm-delete"]');
    await page.waitForSelector('[data-task-title="Updated Test Task"]', { state: 'hidden' });

    // 6. LOGOUT (real session cleanup)
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout"]');
    await page.waitForURL('**/login');
  });
});
```

### Complete API Test Suite

```python
# ✅ CORRECT: Comprehensive API functional tests
import requests
import pytest
from time import sleep

BASE_URL = "http://localhost:3000"

class TestTaskAPIFunctional:
    """Complete functional test suite for Task API"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup and teardown for each test"""
        # Register real user
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": f"test-{int(time.time())}@example.com",
                "password": "SecurePass123!"
            }
        )
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

        yield

        # Cleanup: Delete real user and all associated data
        requests.delete(
            f"{BASE_URL}/api/auth/delete",
            headers=self.headers
        )

    def test_complete_crud_workflow(self):
        """Test complete CRUD workflow with real database"""

        # CREATE (real POST → database INSERT)
        create_response = requests.post(
            f"{BASE_URL}/api/tasks",
            headers=self.headers,
            json={
                "title": "Functional Test Task",
                "description": "Test CRUD operations",
                "priority": "high"
            }
        )
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]

        # READ (real GET → database SELECT)
        read_response = requests.get(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers=self.headers
        )
        assert read_response.status_code == 200
        read_task = read_response.json()
        assert read_task["title"] == "Functional Test Task"

        # UPDATE (real PUT → database UPDATE)
        update_response = requests.put(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers=self.headers,
            json={
                "title": "Updated Task",
                "status": "completed"
            }
        )
        assert update_response.status_code == 200

        # Verify update (real GET)
        verify_response = requests.get(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers=self.headers
        )
        assert verify_response.json()["title"] == "Updated Task"
        assert verify_response.json()["status"] == "completed"

        # DELETE (real DELETE → database DELETE)
        delete_response = requests.delete(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers=self.headers
        )
        assert delete_response.status_code == 204

        # Verify deletion (real GET should 404)
        verify_delete = requests.get(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers=self.headers
        )
        assert verify_delete.status_code == 404
```

---

## Test Validation Rules

### Pre-Test Checklist

Before running any test, verify:

```markdown
☐ **No Mock Imports**
  - No `jest.mock()`, `unittest.mock`, `sinon.stub()`
  - No mocking library imports

☐ **Real Systems Initialized**
  - Real browser launched (Puppeteer/Playwright)
  - Real server running
  - Real database connected
  - Real test environment ready

☐ **Real Interactions**
  - Actual HTTP requests made
  - Actual DOM manipulation
  - Actual database queries executed

☐ **Real Data**
  - Test data inserted into real database
  - Assertions check real API responses
  - Validations against real system state

☐ **Proper Cleanup**
  - Test data deleted from database
  - Real resources released (browser, connections)
  - System returned to clean state
```

### Red Flags (Immediate Rejection)

**Reject any test containing**:

```javascript
// ❌ WRONG: Mock imports
import { jest } from '@jest/globals';
jest.mock('./api');

// ❌ WRONG: Stub creation
const stubFunction = sinon.stub(myModule, 'myFunction');

// ❌ WRONG: Fake implementations
class FakeDatabase {
  async query() { return []; }
}

// ❌ WRONG: Mock variables
const mockUser = { id: 1, name: 'Test' };
const fakeResponse = { status: 200, data: [] };

// ❌ WRONG: In-memory database for integration tests
const db = new InMemoryDatabase();

// ❌ WRONG: Hard-coded responses
if (process.env.NODE_ENV === 'test') {
  return { success: true }; // Bypassing real logic
}
```

### Green Flags (Correct Patterns)

**Accept tests containing**:

```javascript
// ✅ CORRECT: Real browser
const browser = await puppeteer.launch();
const page = await browser.newPage();

// ✅ CORRECT: Real HTTP requests
const response = await fetch('http://localhost:3000/api/tasks');

// ✅ CORRECT: Real database
const pool = new Pool({ database: 'test_db' });
const result = await pool.query('SELECT * FROM tasks');

// ✅ CORRECT: Real iOS simulator
xcodebuild test -destination 'platform=iOS Simulator,name=iPhone 15'

// ✅ CORRECT: Real WebSocket
const ws = new WebSocket('ws://localhost:3000');
ws.onmessage = (event) => { /* test real messages */ };
```

---

## Common Anti-Patterns and Solutions

### Anti-Pattern 1: Mocking External APIs

```javascript
// ❌ WRONG: Mocking third-party API
jest.mock('stripe', () => ({
  charges: {
    create: jest.fn().mockResolvedValue({ id: 'ch_123', status: 'succeeded' })
  }
}));

// ✅ CORRECT: Use Stripe test mode with real API calls
const stripe = require('stripe')(process.env.STRIPE_TEST_KEY);
const charge = await stripe.charges.create({
  amount: 1000,
  currency: 'usd',
  source: 'tok_visa' // Stripe test token
});
expect(charge.status).toBe('succeeded');
```

### Anti-Pattern 2: In-Memory Database for Integration Tests

```javascript
// ❌ WRONG: In-memory database
const db = new InMemoryDatabase();

// ✅ CORRECT: Real test database
const { Pool } = require('pg');
const pool = new Pool({
  database: 'task_app_test',
  // ... real database config
});
```

### Anti-Pattern 3: Mocking Time/Dates

```javascript
// ❌ WRONG: Mocking Date
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));

// ✅ CORRECT: Use parameterized dates
async function createTask(title, createdAt = new Date()) {
  // Function accepts date parameter for testing
}

// Test with specific date
const testDate = new Date('2024-01-01');
const task = await createTask('Test', testDate);
expect(task.createdAt).toEqual(testDate);
```

### Anti-Pattern 4: Stubbing Network Requests

```javascript
// ❌ WRONG: Stubbing fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ data: 'fake' })
  })
);

// ✅ CORRECT: Real network request to test server
const response = await fetch('http://localhost:3000/api/test');
const data = await response.json();
expect(data).toBeDefined();
```

---

## Shannon Testing Worker Integration

The `testing-worker.md` sub-agent enforces these rules automatically:

```markdown
**testing-worker Responsibilities**:

1. **Pre-Test Validation**
   - Scan test files for mock imports
   - Verify real system initialization
   - Check for stub/fake patterns
   - Reject tests failing NO MOCKS mandate

2. **Test Execution**
   - Launch real browsers/simulators
   - Connect to real databases
   - Make real API requests
   - Execute functional tests

3. **Post-Test Validation**
   - Verify cleanup completed
   - Check for resource leaks
   - Validate test isolation
   - Report real test coverage

4. **Continuous Enforcement**
   - Monitor for mock creep
   - Educate on functional testing
   - Suggest real testing alternatives
   - Maintain NO MOCKS discipline
```

---

## Summary

**Shannon's Testing Philosophy**:

1. **NEVER use mocks** - Test real behavior, not mock implementations
2. **ALWAYS use real systems** - Real browsers, real databases, real APIs
3. **Test like production** - If it's different in tests, it's not validated
4. **Validate actual behavior** - Assert on real data, real responses, real state
5. **Enforce ruthlessly** - Reject any test that violates NO MOCKS

**Result**: Tests that actually validate production behavior and catch real bugs before deployment.

---

## Quick Reference

```markdown
❌ NEVER:
- jest.mock() / unittest.mock
- Stub functions
- Fake implementations
- In-memory databases (for integration)
- Hard-coded responses

✅ ALWAYS:
- Real browsers (Puppeteer/Playwright)
- Real simulators (xcodebuild)
- Real HTTP requests
- Real databases
- Real user workflows
- Real data assertions
```

**Testing Decision Tree**:
```
Need to test? → Is it production behavior?
  ├─ Yes → Use real system (NO MOCKS)
  └─ No → Don't test it
```
