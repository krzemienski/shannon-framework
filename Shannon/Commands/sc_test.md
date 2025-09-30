---
name: sc:test
command: /sc:test
description: Shannon V3 enhanced testing command with NO MOCKS enforcement and functional validation
category: command
wave-enabled: false
performance-profile: standard
base: SuperClaude /test command
enhancements: NO MOCKS enforcement, Puppeteer/Simulator testing, TEST_GUARDIAN activation
authority: TEST_GUARDIAN blocks non-compliant tests
---

# /sc:test - Shannon V3 Enhanced Testing Command

**Base**: Enhanced from SuperClaude's `/test` command
**Enhancement Focus**: Functional testing first, NO MOCKS philosophy, platform-specific validation
**Primary Agent**: TEST_GUARDIAN (enforcement authority)
**Secondary Agents**: QA persona, implementation-worker (test code generation)

---

## Purpose Statement

The `/sc:test` command generates and executes functional tests that validate **real system behavior** against **real components**. Unlike traditional testing approaches that rely on mocks and stubs, Shannon V3 mandates functional testing that exercises actual browsers, databases, APIs, and user interfaces.

**Core Philosophy**: Mock-based tests create false confidence. Only functional tests that interact with real components can validate production readiness.

---

## Shannon V3 Enhancements Over SuperClaude

### 1. NO MOCKS Enforcement (Critical)

**Problem**: SuperClaude's `/test` command doesn't specify testing approach, allowing mock-based tests.

**Shannon Solution**: Absolute NO MOCKS mandate enforced by TEST_GUARDIAN agent.

**Enforcement Mechanism**:
- TEST_GUARDIAN automatically activates on `/sc:test` command
- Scans all test files for mock patterns (unittest.mock, jest.mock, @Mock, sinon.stub)
- **BLOCKS** phase progression if mocks detected
- Provides functional alternatives for every mock usage

**Prohibited Patterns**:
```python
# ❌ PROHIBITED - Mock usage
from unittest.mock import Mock, patch
@patch('app.services.EmailService')
def test_send_email(mock_email):
    ...

# ✅ REQUIRED - Functional testing
def test_send_email():
    # Real email service (MailHog test server)
    result = EmailService().send(to='test@example.com', subject='Test')

    # Validate real email received
    mailhog = MailHogClient('http://localhost:8025')
    assert len(mailhog.get_emails()) == 1
```

### 2. Platform-Specific Testing Strategies

**Web Applications** → Puppeteer MCP (primary) / Playwright MCP (alternative)
**iOS Applications** → iOS Simulator + XCUITest
**Backend APIs** → Real HTTP requests + Real database
**Desktop Apps** → Platform automation tools

### 3. TEST_GUARDIAN Integration

**TEST_GUARDIAN Agent**: Unwavering enforcer of NO MOCKS philosophy with authority to block phases.

**Activation**: Automatic on `/sc:test`, Phase 4 (Testing), or mock pattern detection

**Capabilities**:
- Mock detection sweeps across codebase
- Functional test generation (platform-specific templates)
- Test environment provisioning (Docker Compose, simulator setup)
- Quality gate validation (coverage, compliance, execution)

### 4. Real Component Validation

Every test must validate against:
- ✅ Real browser (Puppeteer launches Chrome/Firefox)
- ✅ Real database (PostgreSQL/MongoDB test instance)
- ✅ Real API server (actual Express/FastAPI process)
- ✅ Real UI interactions (actual clicks, typing, navigation)
- ✅ Real data persistence (database writes verified)

---

## Command Usage

### Basic Syntax

```bash
/sc:test [type] [scope] [flags]
```

### Usage Patterns

**1. Generate Functional Tests for Feature**
```bash
/sc:test feature auth-flow

# Generates:
# - Puppeteer tests for login UI (web)
# - XCUITests for login flow (iOS)
# - HTTP tests for auth API endpoints
# - Database validation tests
```

**2. Generate Tests for Specific Platform**
```bash
/sc:test web --scope src/components/TaskList.tsx

# Generates Puppeteer functional tests:
# - Render task list with real API data
# - Add task through real UI interaction
# - Delete task and verify real database removal
# - Filter tasks with real backend filtering
```

**3. Run Compliance Scan**
```bash
/sc:test --scan-mocks

# TEST_GUARDIAN scans codebase for:
# - Mock library imports
# - Stub/fake implementations
# - Simulated responses
# - Reports violations with functional alternatives
```

**4. Generate Test Environment**
```bash
/sc:test --setup-env

# Generates:
# - docker-compose.test.yml (services)
# - Test database initialization scripts
# - Environment variable configuration
# - Setup/teardown scripts
```

**5. Execute Full Test Suite**
```bash
/sc:test --run-all

# Executes:
# 1. Start test environment (Docker Compose)
# 2. Run all functional tests
# 3. Collect coverage metrics
# 4. Validate quality gates
# 5. Generate completion report
```

### Arguments

**[type]** (optional):
- `feature` - Test entire feature end-to-end
- `web` - Web application functional tests
- `ios` - iOS simulator tests
- `backend` - Backend API functional tests
- `integration` - Cross-component integration tests
- `e2e` - Full end-to-end user journeys

**[scope]** (optional):
- File path: `/sc:test web src/components/TaskList.tsx`
- Directory: `/sc:test backend src/api/`
- Feature name: `/sc:test feature user-registration`

### Flags

**Testing Strategy**:
- `--functional` - Functional tests (default, always enforced)
- `--scan-mocks` - Scan for mock usage violations
- `--setup-env` - Generate test environment
- `--generate-only` - Generate tests without execution

**Execution Control**:
- `--run-all` - Execute all tests with coverage
- `--watch` - Watch mode for iterative development
- `--platform <web|ios|backend>` - Target specific platform
- `--coverage` - Generate coverage report (default: true)

**Quality Gates**:
- `--strict` - Enforce 100% coverage on critical paths
- `--validate-phase` - Run Phase 4 quality gate validation
- `--block-on-fail` - Block progression if tests fail (default: true)

**Environment**:
- `--docker` - Use Docker for test environment (default: true)
- `--simulator <device>` - iOS simulator device (default: iPhone 15)
- `--headless` - Headless browser mode (default: true)
- `--debug` - Debug mode with browser/simulator visible

---

## Execution Flow

### Phase 1: Activation & Context Loading

**Step 1: Agent Activation**
```
User types: /sc:test web src/components/TaskList.tsx

Claude Code reads: ~/.claude/commands/sc_test.md
Behavioral instructions injected as system prompt

Activated Agents:
- TEST_GUARDIAN (primary, enforcement authority)
- QA persona (test strategy)
- implementation-worker (test code generation)
```

**Step 2: Context Loading (Universal Shannon Pattern)**
```
MANDATORY: Load ALL previous wave results from Serena MCP

Execute:
1. list_memories() → See available Serena memories
2. read_memory("spec_analysis") → Load project specification
3. read_memory("phase_plan") → Load testing phase requirements
4. read_memory("wave_1_*") → Load architecture decisions
5. read_memory("wave_2_*") → Load implementation details
6. read_memory("testing_requirements") → Load coverage targets

Context Needed:
- What components were built? (from implementation-worker)
- What APIs exist? (from backend-architect)
- What user flows exist? (from frontend-architect)
- What databases are used? (from data-architect)
- What testing coverage is required? (from phase-planner)
```

### Phase 2: Mock Detection Sweep (TEST_GUARDIAN)

**Step 3: Scan Codebase for Mock Usage**
```bash
TEST_GUARDIAN executes:

# Scan for Python mocks
grep -r "from unittest.mock import" . --include="*.py"
grep -r "@patch\|@mock" . --include="*.py"

# Scan for JavaScript mocks
grep -r "jest.mock\|sinon" . --include="*.js" --include="*.ts"
grep -r "createMock\|mockImplementation" . --include="*.js" --include="*.ts"

# Scan for Java mocks
grep -r "@Mock\|Mockito" . --include="*.java"

# Scan for Swift mocks (rare, but check)
grep -r "protocol.*Mock" . --include="*.swift"
```

**Step 4: Violation Handling**
```
IF mocks detected:
  ACTION: STOP execution
  OUTPUT: Mock Violation Report (see format below)
  PROVIDE: Functional alternatives for each violation
  BLOCK: Phase progression until resolved

ELSE:
  OUTPUT: ✅ NO MOCKS compliance verified
  CONTINUE: To test generation
```

### Phase 3: Test Strategy Planning

**Step 5: Platform Detection & Strategy Selection**
```
Analyze scope and determine testing approach:

IF scope contains .tsx/.jsx/.vue files:
  platform = "web"
  tool = "Puppeteer MCP"
  approach = "Real browser functional testing"

ELIF scope contains .swift/.m files:
  platform = "ios"
  tool = "iOS Simulator + XCUITest"
  approach = "Real simulator UI testing"

ELIF scope contains API routes/controllers:
  platform = "backend"
  tool = "Real HTTP client"
  approach = "Real HTTP requests + Real database"

ELIF scope contains database models:
  platform = "data"
  tool = "Real database connection"
  approach = "Real CRUD operations"
```

**Step 6: Test Scenario Design**
```
For identified platform, design test scenarios:

1. Identify critical user journeys
2. Map component interactions
3. Define real components needed
4. Plan data setup/teardown
5. Design assertions for real behavior
6. Estimate test execution time
```

### Phase 4: Functional Test Generation

**Step 7: Generate Platform-Specific Tests**

**Web Application (Puppeteer MCP)**:
```javascript
// ✅ Generated Functional Test - NO MOCKS
const puppeteer = require('puppeteer');

describe('TaskList Component - Functional Tests', () => {
  let browser, page;

  beforeAll(async () => {
    // Start test environment
    await exec('docker-compose -f docker-compose.test.yml up -d');
    await exec('sleep 5'); // Wait for services
  });

  afterAll(async () => {
    // Cleanup test environment
    await exec('docker-compose -f docker-compose.test.yml down -v');
  });

  beforeEach(async () => {
    // Launch real browser
    browser = await puppeteer.launch({ headless: true });
    page = await browser.newPage();

    // Navigate to real application
    await page.goto('http://localhost:3000/tasks');
  });

  afterEach(async () => {
    await browser.close();
  });

  test('User can view task list from real database', async () => {
    // Wait for real API call and DOM render
    await page.waitForSelector('.task-item', { timeout: 5000 });

    // Validate real DOM from real backend
    const taskCount = await page.$$eval('.task-item', items => items.length);
    expect(taskCount).toBeGreaterThan(0);
  });

  test('User can add task through real UI and API', async () => {
    // Real user interaction
    await page.click('#add-task-button');
    await page.type('#task-title', 'Write functional tests');
    await page.type('#task-description', 'NO MOCKS, real components only');
    await page.click('#save-task');

    // Wait for real API POST and DOM update
    await page.waitForSelector('.task-item:last-child');

    // Validate real DOM update
    const newTaskTitle = await page.$eval('.task-item:last-child .title',
      el => el.textContent);
    expect(newTaskTitle).toBe('Write functional tests');

    // Validate real database persistence
    await page.reload();
    await page.waitForSelector('.task-item:last-child');
    const persistedTitle = await page.$eval('.task-item:last-child .title',
      el => el.textContent);
    expect(persistedTitle).toBe('Write functional tests');
  });

  test('User can delete task and verify real database removal', async () => {
    await page.waitForSelector('.task-item');

    // Count initial tasks
    const initialCount = await page.$$eval('.task-item', items => items.length);

    // Real delete interaction
    await page.click('.task-item:first-child .delete-button');
    await page.click('.confirm-delete'); // Confirm dialog

    // Wait for real API DELETE and DOM update
    await page.waitForTimeout(500);

    // Validate real DOM removal
    const finalCount = await page.$$eval('.task-item', items => items.length);
    expect(finalCount).toBe(initialCount - 1);

    // Validate real database deletion persists
    await page.reload();
    const persistedCount = await page.$$eval('.task-item', items => items.length);
    expect(persistedCount).toBe(initialCount - 1);
  });
});
```

**iOS Application (Simulator + XCUITest)**:
```swift
// ✅ Generated Functional Test - NO MOCKS
import XCTest

class TaskListUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false

        // Launch real app on simulator
        app = XCUIApplication()
        app.launch()
    }

    func testUserCanViewTaskListFromRealCoreData() {
        // Wait for real data load
        let taskList = app.tables["TaskList"]
        XCTAssertTrue(taskList.waitForExistence(timeout: 5))

        // Validate real CoreData fetch
        let cells = taskList.cells
        XCTAssertTrue(cells.count > 0)
    }

    func testUserCanAddTaskThroughRealUI() {
        // Real UI interaction
        app.buttons["Add Task"].tap()

        let titleField = app.textFields["Task Title"]
        titleField.tap()
        titleField.typeText("Write functional tests")

        let descField = app.textViews["Task Description"]
        descField.tap()
        descField.typeText("NO MOCKS, real components only")

        app.buttons["Save"].tap()

        // Wait for real CoreData save and UI update
        sleep(1)

        // Validate real UI update
        XCTAssertTrue(app.staticTexts["Write functional tests"].exists)

        // Validate real persistence (terminate and relaunch)
        app.terminate()
        app.launch()
        XCTAssertTrue(app.staticTexts["Write functional tests"].exists)
    }

    func testUserCanDeleteTaskAndVerifyRealRemoval() {
        let taskList = app.tables["TaskList"]
        let initialCount = taskList.cells.count

        // Real delete interaction
        taskList.cells.firstMatch.swipeLeft()
        app.buttons["Delete"].tap()

        // Wait for real CoreData delete
        sleep(1)

        // Validate real removal
        XCTAssertEqual(taskList.cells.count, initialCount - 1)

        // Validate persistence
        app.terminate()
        app.launch()
        XCTAssertEqual(taskList.cells.count, initialCount - 1)
    }
}
```

**Backend API (Real HTTP)**:
```javascript
// ✅ Generated Functional Test - NO MOCKS
const axios = require('axios');

describe('Task API - Functional Tests', () => {
  const API_URL = 'http://localhost:3000/api';

  beforeAll(async () => {
    // Start test environment
    await exec('docker-compose -f docker-compose.test.yml up -d');
    await exec('sleep 5');
  });

  afterAll(async () => {
    await exec('docker-compose -f docker-compose.test.yml down -v');
  });

  beforeEach(async () => {
    // Clear real test database
    await axios.delete(`${API_URL}/test/reset`);
  });

  test('POST /tasks creates task in real database', async () => {
    // Real HTTP request
    const response = await axios.post(`${API_URL}/tasks`, {
      title: 'Write functional tests',
      description: 'NO MOCKS, real components only',
      completed: false
    });

    // Validate real HTTP response
    expect(response.status).toBe(201);
    expect(response.data.title).toBe('Write functional tests');

    const taskId = response.data.id;

    // Validate real database persistence
    const getResponse = await axios.get(`${API_URL}/tasks/${taskId}`);
    expect(getResponse.data.title).toBe('Write functional tests');
  });

  test('DELETE /tasks/:id removes task from real database', async () => {
    // Create task
    const createResponse = await axios.post(`${API_URL}/tasks`, {
      title: 'Test task',
      completed: false
    });
    const taskId = createResponse.data.id;

    // Real HTTP DELETE
    const deleteResponse = await axios.delete(`${API_URL}/tasks/${taskId}`);
    expect(deleteResponse.status).toBe(204);

    // Validate real database deletion
    try {
      await axios.get(`${API_URL}/tasks/${taskId}`);
      fail('Task should not exist');
    } catch (error) {
      expect(error.response.status).toBe(404);
    }
  });
});
```

### Phase 5: Test Environment Provisioning

**Step 8: Generate Test Environment Configuration**
```yaml
# docker-compose.test.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgresql://test:test@db:5432/testdb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    command: npm run dev

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=testdb
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=test
    ports:
      - "5432:5432"
    volumes:
      - ./tests/db-init:/docker-entrypoint-initdb.d

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Step 9: Generate Setup Scripts**
```bash
#!/bin/bash
# tests/setup-env.sh

set -e

echo "🚀 Starting test environment..."

# Start services
docker-compose -f docker-compose.test.yml up -d

# Wait for database
echo "⏳ Waiting for database..."
until docker-compose exec -T db pg_isready; do
  sleep 1
done

# Run database migrations
echo "📊 Running database migrations..."
npm run migrate:test

# Seed test data
echo "🌱 Seeding test data..."
npm run seed:test

echo "✅ Test environment ready!"
```

### Phase 6: Test Execution & Validation

**Step 10: Execute Tests**
```bash
# Generated test execution script
#!/bin/bash
set -e

# Setup
./tests/setup-env.sh

# Run tests with coverage
echo "🧪 Running functional tests..."
npm test -- --coverage

# Extract coverage metrics
LINES_COVERAGE=$(npx nyc report --reporter=text-summary | grep "Lines" | awk '{print $3}' | sed 's/%//')
FUNCTIONS_COVERAGE=$(npx nyc report --reporter=text-summary | grep "Functions" | awk '{print $3}' | sed 's/%//')
BRANCHES_COVERAGE=$(npx nyc report --reporter=text-summary | grep "Branches" | awk '{print $3}' | sed 's/%//')

# Validate thresholds
echo "📊 Coverage: Lines ${LINES_COVERAGE}%, Functions ${FUNCTIONS_COVERAGE}%, Branches ${BRANCHES_COVERAGE}%"

if (( $(echo "$LINES_COVERAGE < 80" | bc -l) )); then
  echo "❌ Lines coverage below 80%"
  exit 1
fi

if (( $(echo "$FUNCTIONS_COVERAGE < 80" | bc -l) )); then
  echo "❌ Functions coverage below 80%"
  exit 1
fi

if (( $(echo "$BRANCHES_COVERAGE < 75" | bc -l) )); then
  echo "❌ Branches coverage below 75%"
  exit 1
fi

echo "✅ All coverage thresholds met"

# Cleanup
./tests/teardown-env.sh
```

**Step 11: Quality Gate Validation**
```
TEST_GUARDIAN evaluates:

Required Criteria (ALL must pass):
✅ NO MOCKS compliance: 0 violations detected
✅ All tests passing: {pass_count}/{total_count}
✅ Lines coverage: {percentage}% >= 80%
✅ Functions coverage: {percentage}% >= 80%
✅ Branches coverage: {percentage}% >= 75%
✅ Real component validation: All tests use real browsers/databases/APIs

IF all criteria pass:
  OUTPUT: Phase 4 Completion Report (APPROVED)
  ACTION: write_memory("phase_4_complete", results)
  ALLOW: Progression to Phase 5 (Deployment)

ELSE:
  OUTPUT: Phase 4 Completion Report (BLOCKED)
  ACTION: List failures and required actions
  BLOCK: Phase progression until issues resolved
```

### Phase 7: Results Storage

**Step 12: Save to Serena MCP**
```
write_memory("test_results_[timestamp]", {
  "platform": "web|ios|backend",
  "test_count": total_tests,
  "passing": pass_count,
  "failing": fail_count,
  "coverage": {
    "lines": line_percentage,
    "functions": function_percentage,
    "branches": branch_percentage
  },
  "no_mocks_compliance": true,
  "real_components_validated": [
    "Real browser (Puppeteer)",
    "Real database (PostgreSQL)",
    "Real API server"
  ],
  "quality_gate_status": "PASS|BLOCKED",
  "phase_4_approved": true|false
})
```

---

## Sub-Agent Integration

### TEST_GUARDIAN (Primary)

**Role**: Enforcement authority for NO MOCKS philosophy

**Activation**: Automatic on `/sc:test`, Phase 4, or mock detection

**Responsibilities**:
1. **Mock Detection**: Scan codebase for prohibited mock patterns
2. **Violation Blocking**: STOP execution if mocks detected
3. **Functional Alternatives**: Provide real component test patterns
4. **Quality Gates**: Validate coverage and compliance before phase approval
5. **Environment Setup**: Guide test infrastructure provisioning

**Authority Level**: Can **BLOCK** phase progression

**Output**: Mock Violation Reports, Functional Test Plans, Phase Completion Reports

### QA Persona (Secondary)

**Role**: Test strategy and comprehensive coverage planning

**Activation**: Automatic when TEST_GUARDIAN activates

**Responsibilities**:
1. Test scenario design (critical paths, edge cases)
2. Coverage target definition
3. Test data management strategy
4. Performance testing requirements
5. Accessibility validation (web/mobile)

**Collaboration**: Works under TEST_GUARDIAN's NO MOCKS mandate

### implementation-worker (Test Code Generation)

**Role**: Generate functional test code following TEST_GUARDIAN templates

**Activation**: After TEST_GUARDIAN approves test strategy

**Responsibilities**:
1. Generate platform-specific test files
2. Create test environment configuration
3. Write setup/teardown scripts
4. Implement real component integration
5. Add test assertions for real behavior validation

**Constraint**: ALL generated code must pass TEST_GUARDIAN compliance scan

---

## Output Format

### 1. Mock Violation Report (when mocks detected)

```markdown
# 🚨 MOCK USAGE VIOLATION REPORT

**Generated by**: TEST_GUARDIAN
**Scan Date**: {timestamp}
**Total Violations**: {count}
**Severity**: CRITICAL
**Status**: ⛔ PHASE BLOCKED

---

## Violations Detected

### Violation 1: {file_path}:{line_number}

**Type**: unittest.mock.patch usage
**Code**:
```python
@mock.patch('app.services.EmailService')
def test_send_notification(self, mock_email):
    mock_email.send.return_value = True
    result = send_notification('test@example.com')
    assert result == True
```

**Why This Violates NO MOCKS**:
This test mocks EmailService, preventing validation of:
- Actual email sending logic
- SMTP configuration and connection
- Email template rendering
- Error handling for failed sends
- Real integration with email provider

**Functional Alternative**:
```python
def test_send_notification():
    # Use real test email service (MailHog)
    result = send_notification('test@example.com')

    # Validate real email received
    mailhog = MailHogClient('http://localhost:8025')
    emails = mailhog.get_emails()

    assert len(emails) == 1
    assert emails[0].to == 'test@example.com'
    assert 'Notification' in emails[0].subject
```

---

## Required Actions

1. **Remove all mock usage** from {file_path}
2. **Implement functional alternatives** provided above
3. **Setup test email service** (MailHog: `docker run -p 8025:8025 mailhog/mailhog`)
4. **Re-run tests** against real components
5. **Verify NO mock imports** remain in codebase

---

⛔ **PHASE 4 BLOCKED** until all violations resolved

**Next Steps**:
1. Fix violations listed above
2. Re-run: `/sc:test --scan-mocks` to verify
3. Continue with test generation after clean scan
```

### 2. Functional Test Plan (test generation)

```markdown
# Functional Test Plan: TaskList Component

**Generated by**: TEST_GUARDIAN
**Date**: {timestamp}
**Platform**: Web Application
**Testing Tool**: Puppeteer MCP
**Target**: src/components/TaskList.tsx

---

## Test Scenarios

### Scenario 1: View Task List (Critical Path)

**Objective**: Validate task list loads and displays real data from backend API

**Real Components**:
- ✅ Real browser (Chrome via Puppeteer)
- ✅ Real React application (localhost:3000)
- ✅ Real Express API server (localhost:3000/api)
- ✅ Real PostgreSQL database (test instance)

**Test Steps**:
1. Navigate to http://localhost:3000/tasks
2. Wait for real API GET /tasks call
3. Verify real DOM renders task items
4. Count task items matches database records

**Expected Outcome**:
- Task list visible within 3 seconds
- All database tasks displayed correctly
- Real API response reflected in UI

### Scenario 2: Add Task (Critical Path)

**Objective**: Validate user can create task through real UI and API

**Real Components**: Same as Scenario 1

**Test Steps**:
1. Click "Add Task" button (real DOM interaction)
2. Type task title in input field (real keyboard events)
3. Type description in textarea (real keyboard events)
4. Click "Save" button (real submit)
5. Wait for real API POST /tasks call
6. Verify real DOM updates with new task
7. Reload page
8. Verify task persists (validates real database write)

**Expected Outcome**:
- New task appears in list immediately
- Task persists after page reload (real database)
- API returns 201 Created

---

## Test Implementation

### File: tests/functional/TaskList.test.js

```javascript
{generated_test_code}
```

---

## Test Environment

### Setup

```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Wait for services
sleep 5

# Run database migrations
npm run migrate:test

# Seed test data
npm run seed:test
```

### Verification

```bash
# Check services running
docker-compose ps

# Verify database
docker-compose exec db psql -U test -d testdb -c "SELECT COUNT(*) FROM tasks;"

# Verify application
curl http://localhost:3000/api/health
```

---

## Coverage Target

- **Critical Paths**: 100% (view, add, delete tasks)
- **Core Features**: 90% (edit, filter, sort)
- **Edge Cases**: 70% (empty state, errors)

**Current Coverage**: 0% (tests not yet generated)
**Status**: NEEDS_IMPLEMENTATION
```

### 3. Phase 4 Completion Report

```markdown
# Phase 4: Testing & Validation - Completion Report

**Phase**: Testing & Quality Assurance
**Status**: ✅ COMPLETE
**Guardian**: TEST_GUARDIAN
**Date**: {timestamp}

---

## Quality Gate Results

### ✅ NO MOCKS Compliance

**Status**: PASS
**Violations Detected**: 0
**Verification Method**: Full codebase scan (grep patterns)
**Last Scan**: {timestamp}

```bash
# Scan results
Python mocks: 0 files
JavaScript mocks: 0 files
Java mocks: 0 files
✅ NO mock usage detected
```

### ✅ Functional Test Coverage

**Lines**: 87.3% (Target: 80%) ✅
**Functions**: 91.2% (Target: 80%) ✅
**Branches**: 78.6% (Target: 75%) ✅

**Status**: PASS - All thresholds exceeded

**Coverage by Domain**:
- Web UI (Puppeteer): 89.5%
- Backend API (HTTP): 92.1%
- Database Layer: 85.7%

### ✅ Test Execution Results

**Total Tests**: 47
**Passing**: 47 ✅
**Failing**: 0
**Flaky**: 0
**Execution Time**: 3m 42s

**Test Breakdown**:
- Puppeteer functional: 23 tests (all passing)
- Backend API functional: 18 tests (all passing)
- Integration end-to-end: 6 tests (all passing)

### ✅ Real Component Validation

**Web (Puppeteer)**:
- ✅ 23 tests execute against real Chrome browser
- ✅ All tests interact with real running application
- ✅ All tests validate real DOM from real API responses

**Backend (HTTP Client)**:
- ✅ 18 tests make real HTTP requests
- ✅ All tests use real PostgreSQL test database
- ✅ All tests validate real data persistence

**Integration**:
- ✅ 6 tests validate real end-to-end user journeys
- ✅ All components communicate through real APIs
- ✅ Database transactions verified through actual queries

---

## Test Suite Summary

### Web Application (Puppeteer MCP)

**Test Count**: 23 functional tests
**Tool**: Puppeteer (real Chrome browser)
**Coverage**: User flows from login to task management

**Key Tests**:
- User authentication flow (login/logout)
- Task CRUD operations (create, read, update, delete)
- Task filtering and sorting
- Real-time updates (WebSocket integration)
- Responsive design validation

**Real Components**:
- Real Chrome browser instance
- Real React application running on localhost:3000
- Real Express API server
- Real PostgreSQL database with test data
- Real WebSocket connections

### Backend API (HTTP Client)

**Test Count**: 18 functional tests
**Tool**: axios (real HTTP requests)
**Coverage**: All API endpoints with real database operations

**Key Tests**:
- POST /tasks (create with database write)
- GET /tasks (list from real database)
- PUT /tasks/:id (update with database write)
- DELETE /tasks/:id (remove from real database)
- Authentication endpoints
- Error handling with real error responses

**Real Components**:
- Real Express server process
- Real PostgreSQL database instance
- Real JWT token generation and validation
- Real database transactions and rollbacks

### Integration Tests (End-to-End)

**Test Count**: 6 functional tests
**Coverage**: Complete user journeys across all layers

**Key Tests**:
- Complete task lifecycle (create → edit → complete → delete)
- Multi-user collaboration scenarios
- Error recovery and retry logic
- Performance under load (concurrent users)

---

## Phase Approval

✅ **PHASE 4 COMPLETE**

All quality gates passed. System validated through comprehensive functional testing with NO MOCKS.

**Validation Confirmation**:
- Zero mock usage detected across entire codebase
- All tests execute against real components
- Coverage exceeds all thresholds
- No test failures or flakiness detected
- Real system behavior validated end-to-end

**Ready for Phase 5 (Deployment)**

---

**Signed**: TEST_GUARDIAN
**Date**: {timestamp}
**Authority**: Enforcement Agent for Shannon V3 NO MOCKS Philosophy
```

---

## Examples

### Example 1: Generate Web Tests

```
User: /sc:test web src/components/TaskList.tsx

Claude Code reads: ~/.claude/commands/sc_test.md
TEST_GUARDIAN activates
QA persona activates

Output:

✅ NO MOCKS Compliance: Verified (0 violations)

📋 Generating Functional Test Plan for TaskList Component...

Platform: Web Application
Tool: Puppeteer MCP (real browser automation)

Test Scenarios:
1. View Task List (Critical Path)
   - Real browser navigates to localhost:3000/tasks
   - Validates real API GET /tasks response
   - Verifies real DOM rendering from real data

2. Add Task (Critical Path)
   - Real UI interaction (click, type, submit)
   - Real API POST /tasks with real database write
   - Real DOM update validation
   - Real persistence verification (page reload)

3. Delete Task (Critical Path)
   - Real delete button click
   - Real API DELETE /tasks/:id
   - Real database removal validation
   - Real DOM update verification

[Generated test file: tests/functional/TaskList.test.js]
[Generated test environment: docker-compose.test.yml]
[Generated setup script: tests/setup-env.sh]

To execute:
  npm test tests/functional/TaskList.test.js
```

### Example 2: Mock Detection Scan

```
User: /sc:test --scan-mocks

TEST_GUARDIAN activates

Scanning codebase for mock usage...

⛔ VIOLATIONS DETECTED

tests/api/tasks.test.js:15
- Type: jest.mock() usage
- Violation: Mocking database service
- Impact: Database integration not validated

tests/components/TaskList.test.tsx:8
- Type: Mock API responses
- Violation: fetch() calls intercepted
- Impact: Real API behavior not tested

Total: 2 violations

📋 Functional Alternatives Provided:
- Real database testing with Docker Compose
- Real API testing with Puppeteer

⛔ PHASE BLOCKED until violations resolved
```

### Example 3: iOS Simulator Tests

```
User: /sc:test ios --scope TaskApp

TEST_GUARDIAN activates

Platform: iOS Application
Tool: iOS Simulator + XCUITest

Generating XCUITest functional tests...

Test Target: TaskApp.xcodeproj
Simulator: iPhone 15 (iOS 17.0)

Test Scenarios:
1. Task List View (CoreData validation)
2. Add Task (Real UI + CoreData write)
3. Delete Task (Real UI + CoreData delete)

[Generated: TaskAppUITests/TaskListTests.swift]
[Generated: scripts/run-ios-tests.sh]

To execute:
  ./scripts/run-ios-tests.sh

Or manually:
  xcodebuild test -project TaskApp.xcodeproj -scheme TaskApp \
    -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.0'
```

---

## Notes

- **Type command in Claude Code conversation window**, not terminal
- **Auto-activation**: TEST_GUARDIAN activates on any testing-related keywords
- **Mandatory Serena MCP**: Shannon requires Serena for context preservation
- **NO MOCKS Non-Negotiable**: TEST_GUARDIAN has authority to BLOCK phases
- **Real Components Required**: All tests must interact with actual systems
- **Platform Detection**: Automatic based on file extensions and project structure
- **Coverage Thresholds**: 80/80/75 (lines/functions/branches) enforced
- **Docker Compose**: Default test environment provisioning method
- **Reproducibility**: Same tests run identically across environments
- **PreCompact Hook**: Test results automatically saved before context compaction

---

**END OF /sc:test COMMAND DEFINITION**

**Shannon V3 Testing Philosophy**: No Mocks. No Compromises. No Exceptions.