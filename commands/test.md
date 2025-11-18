---
name: shannon:test
description: NO MOCKS functional testing orchestration with platform detection
usage: /shannon:test [test_path] [--platform web|mobile|api] [--create]
---

# Functional Testing Command (V4)

## Overview

Orchestrates Shannon's NO MOCKS functional testing philosophy through delegation to the functional-testing skill. Automatically detects platform (web, mobile, API), discovers existing tests, executes tests with real dependencies, and creates new test scaffolds.

**Core Principle**: Shannon NEVER uses mocks. All tests run against real browsers (Puppeteer), real mobile devices (iOS Simulator), real APIs (HTTP), and real databases.

## Prerequisites

- Project with testable components
- Platform-specific MCPs:
  - **Web**: Puppeteer MCP (real browser testing)
  - **Mobile**: iOS Simulator MCPs (real device testing)
  - **API**: HTTP client (real API requests)
  - **Database**: Database MCP (real database operations)

## Workflow

### Step 1: Validate Input and Detect Mode

Parse command arguments:

**Mode Detection**:
- No arguments → `mode: "discover"` (find all tests)
- Test path provided → `mode: "execute"` (run specific test)
- `--create` flag → `mode: "create"` (scaffold new test)
- `--platform` specified → Override auto-detection

**Platform Detection** (if not specified):
- Scan for web patterns: `*.test.js` with `puppeteer`, `playwright`
- Scan for mobile patterns: `*.swift` with `XCTest`, `XCUITest`
- Scan for API patterns: `*.test.js` with `supertest`, `axios`
- Scan for database patterns: SQL files, migration tests

### Step 2: Invoke functional-testing Skill

Delegate to `@skill functional-testing` with appropriate mode:

**For DISCOVER mode:**
```
@skill functional-testing
- Input:
  * mode: "discover"
  * platform: {detected_platform}
  * scope: "all" | {test_directory}
- Output: test_inventory
```

The skill will:
1. Scan project for test files
2. Classify by platform (web/mobile/api/db)
3. Identify test coverage gaps
4. Report test health metrics

**For EXECUTE mode:**
```
@skill functional-testing
- Input:
  * mode: "execute"
  * test_path: {user_provided_path}
  * platform: {detected_platform}
  * real_dependencies: true
  * no_mocks: true (enforced)
- Output: test_results
```

The skill will:
1. Validate test uses NO MOCKS
2. Setup real dependencies (browser, device, API, DB)
3. Execute test against real environment
4. Capture results with screenshots/logs
5. Clean up test environment

**For CREATE mode:**
```
@skill functional-testing
- Input:
  * mode: "create"
  * test_type: {web|mobile|api|database}
  * target: {component_to_test}
  * platform: {detected_platform}
- Output: test_scaffold
```

The skill will:
1. Detect target component type
2. Generate NO MOCKS test scaffold
3. Include real dependency setup
4. Add Shannon test patterns
5. Generate test documentation

### Step 3: Present Results

Format and display based on mode:

**DISCOVER Mode Output:**
```markdown
🧪 Shannon Functional Test Inventory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Platform**: {primary_platform}
**Total Tests**: {test_count}
**Coverage**: {coverage_percentage}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Breakdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Web Tests (Puppeteer):
{for each web_test}
├─ {test_file}
   └─ Tests: {test_count}, Status: {passing|failing}

Mobile Tests (iOS Simulator):
{for each mobile_test}
├─ {test_file}
   └─ Tests: {test_count}, Status: {passing|failing}

API Tests (Real HTTP):
{for each api_test}
├─ {test_file}
   └─ Tests: {test_count}, Status: {passing|failing}

Database Tests (Real DB):
{for each db_test}
├─ {test_file}
   └─ Tests: {test_count}, Status: {passing|failing}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Coverage Gaps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Missing Tests:
{for each gap}
⚠️  {component_name}
   - Priority: {priority}
   - Suggested: /shannon:test --create {component_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Health
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ NO MOCKS Compliance: {compliance_percentage}%
{if violations}
⚠️  Mock Usage Detected:
{for each violation}
   - {test_file}: Uses {mock_library}
   - Action: Refactor to use real dependencies
{end if}

⏱️  Average Test Duration: {avg_duration}s
📊 Flakiness Score: {flakiness_score}/10 ({interpretation})
```

**EXECUTE Mode Output:**
```markdown
🧪 Shannon Functional Test Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test**: {test_path}
**Platform**: {platform}
**NO MOCKS**: ✅ Verified
**Duration**: {duration}s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if passed}
✅ PASSED ({passed_count}/{total_count} tests)

Test Details:
{for each test}
✓ {test_name} ({duration}ms)
{end for}

{else}
❌ FAILED ({failed_count}/{total_count} tests)

Failures:
{for each failure}
✗ {test_name}
  Error: {error_message}
  Location: {file}:{line}

  Stack Trace:
  {stack_trace}

  {if screenshot_available}
  Screenshot: {screenshot_path}
  {end if}
{end for}

{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if web_platform}
Browser: {browser_name} {browser_version}
Viewport: {width}x{height}
{end if}

{if mobile_platform}
Device: {device_name}
iOS Version: {ios_version}
Simulator UDID: {udid}
{end if}

{if api_platform}
API Base: {api_url}
Response Time: {avg_response_time}ms
{end if}

{if database_platform}
Database: {db_type}
Test Instance: {db_connection_string}
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if passed}
✅ All tests passing
- Continue development with confidence
- Consider adding more test coverage

{else}
⚠️  Test failures detected
- Review failure details above
- Fix issues and re-run: /shannon:test {test_path}
- Check screenshot artifacts if available
{end if}
```

**CREATE Mode Output:**
```markdown
🧪 Shannon Test Scaffold Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Test File**: {created_test_path}
**Platform**: {platform}
**Type**: Functional (NO MOCKS)
**Target**: {target_component}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated Test Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{test_scaffold_code}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Patterns Included
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Real dependency setup
✅ NO MOCKS enforcement
✅ Shannon test conventions
✅ Cleanup/teardown
✅ Error handling
✅ Screenshot capture (if applicable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review generated test: {created_test_path}
2. Customize test steps for your use case
3. Run test: /shannon:test {created_test_path}
4. Iterate until passing
```

### Step 4: Validate NO MOCKS Compliance

The functional-testing skill automatically validates:

```
✅ Check 1: No mock libraries imported
   - Verify no `jest.mock()`, `sinon`, `mockito`, etc.

✅ Check 2: Real browser/device used
   - Puppeteer launches real Chrome
   - iOS Simulator uses real device
   - Not using jsdom or fake DOM

✅ Check 3: Real API calls
   - HTTP requests hit actual endpoints
   - Not using mock server or stubs

✅ Check 4: Real database operations
   - Connects to test database instance
   - Not using in-memory or fake DB
```

If violations detected:
```
⚠️  NO MOCKS VIOLATION DETECTED

File: {test_file}
Line: {line_number}
Issue: {violation_description}

{suggested_fix}

Shannon requires real dependencies. Refactor this test.
```

## Output Format

See Step 3 presentation templates above.

## Skill Dependencies

- functional-testing (REQUIRED)

## MCP Dependencies

**Required (based on platform)**:
- **Web**: Puppeteer MCP (real browser automation)
- **Mobile**: iOS Simulator MCP, XCTest tools
- **API**: HTTP client (axios, fetch)
- **Database**: PostgreSQL/MongoDB/MySQL MCP (based on DB type)

**Recommended**:
- Serena MCP (save test results and history)
- Sequential MCP (complex test scenario planning)

## Examples

### Example 1: Discover All Tests

```bash
/shannon:test
```

Scans project, finds all functional tests, reports coverage.

### Example 2: Run Specific Test

```bash
/shannon:test tests/functional/login.test.js
```

Executes login test with real browser.

### Example 3: Run with Platform Override

```bash
/shannon:test tests/api/auth.test.js --platform api
```

Forces API platform detection (if auto-detect ambiguous).

### Example 4: Create New Web Test

```bash
/shannon:test --create checkout-flow --platform web
```

Generates Puppeteer test scaffold for checkout flow.

### Example 5: Create Mobile Test

```bash
/shannon:test --create login-screen --platform mobile
```

Generates iOS Simulator test scaffold for login screen.

## NO MOCKS Iron Law

Shannon Framework has ZERO TOLERANCE for mocks:

**NEVER**:
- ❌ `jest.mock()`
- ❌ `sinon.stub()`
- ❌ `mockito.mock()`
- ❌ In-memory databases
- ❌ jsdom or fake DOM
- ❌ Mock servers
- ❌ Stub APIs

**ALWAYS**:
- ✅ Puppeteer (real browser)
- ✅ iOS Simulator (real device)
- ✅ Real HTTP requests
- ✅ Test database instance
- ✅ Real file system
- ✅ Real network calls

**Why?** Mocks give false confidence. They test mocks, not code. Shannon tests the real system.

## Notes

- **NEW in V4**: This is a new command that delegates to functional-testing skill
- **Philosophy**: NO MOCKS is a Shannon Iron Law (see shannon-plugin/core/TESTING_PHILOSOPHY.md)
- **Coverage**: Functional tests only; no unit tests (Shannon doesn't believe in unit tests with mocks)
- **Performance**: Tests are slower (real dependencies) but catch real bugs
- **CI/CD**: All tests must pass before deployment
