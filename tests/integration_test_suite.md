# Shannon V4 Integration Test Plan

## Overview

This document provides comprehensive integration test scenarios for Shannon V4. These tests verify end-to-end workflows, context preservation, NO MOCKS enforcement, MCP integration, and backward compatibility.

**Testing Philosophy:** All tests follow Shannon's NO MOCKS principle - they must be executed in real Claude Code environments with actual MCPs. No simulation or mocking is permitted.

---

## Test 1: Complete Workflow (Specification → Implementation)

**Scenario:** User provides spec, Shannon analyzes, creates phases, executes wave

**Objective:** Verify end-to-end workflow from specification analysis through wave execution

**Steps:**

1. **Analyze Specification**
   ```bash
   /shannon:spec "Build REST API for task management with user authentication, CRUD operations, and real-time updates"
   ```

   **Expected Output:**
   - Complexity score displayed (should be ≥ 0.50 for this spec)
   - 8D analysis breakdown (technical, temporal, integration, etc.)
   - Domain identification (Backend, Database, Security, API)
   - Recommended wave count
   - Analysis saved to Serena MCP

2. **Verify Analysis Storage**
   ```bash
   /shannon:status
   ```

   **Expected Output:**
   - Current specification displayed
   - Complexity score shown
   - Project state: "analyzed"

3. **Plan Wave Execution**
   ```bash
   /shannon:wave 1 --plan
   ```

   **Expected Output:**
   - Wave 1 plan generated
   - Tasks broken down by phase
   - Agent assignments shown
   - Estimated duration provided

4. **Execute Wave**
   ```bash
   /shannon:wave 1
   ```

   **Expected Output:**
   - Wave coordinator agent activates
   - Progress updates displayed
   - Tasks executed in sequence
   - Checkpoints created automatically

5. **Verify Completion**
   ```bash
   /shannon:status
   ```

   **Expected Output:**
   - Wave 1 marked complete
   - Deliverables listed
   - Next steps recommended

**Success Criteria:**
- ✅ All commands execute without errors
- ✅ Data persists between commands via Serena MCP
- ✅ Agents activate and coordinate properly
- ✅ Wave completes all planned tasks

---

## Test 2: Context Preservation & Restoration

**Scenario:** Create checkpoint, simulate context loss, restore successfully

**Objective:** Verify zero context loss through checkpoint/restore cycle

**Steps:**

1. **Initial Setup**
   ```bash
   /shannon:spec "Build mobile app with offline sync"
   ```

2. **Set North Star Goal**
   ```bash
   /shannon:north_star "Launch MVP to 100 beta users by end of Q1"
   ```

3. **Create Checkpoint**
   ```bash
   /shannon:checkpoint "pre-implementation"
   ```

   **Expected Output:**
   - Checkpoint ID generated
   - Saved to Serena MCP
   - Confirmation message displayed

4. **Verify Checkpoint Saved**
   ```bash
   /shannon:status
   ```

   **Expected Output:**
   - Checkpoint listed in project state
   - North star goal preserved

5. **Simulate Context Loss**
   - Start new conversation in Claude Code
   - Clear local context (simulating memory loss)

6. **Restore Checkpoint**
   ```bash
   /shannon:restore "pre-implementation"
   ```

   **Expected Output:**
   - Specification restored
   - North star goal restored
   - Complexity analysis restored
   - Project state restored

7. **Verify Full Restoration**
   ```bash
   /shannon:status
   ```

   **Expected Output:**
   - All original data present
   - No information loss
   - Ready to continue work

**Success Criteria:**
- ✅ Checkpoint captures all critical state
- ✅ Restore recovers 100% of context
- ✅ Zero manual re-entry required
- ✅ Work can resume immediately

---

## Test 3: NO MOCKS Enforcement

**Scenario:** Request tests, verify NO MOCKS philosophy enforced

**Objective:** Ensure generated tests use real environments, not mocks

**Steps:**

1. **Request Web Tests**
   ```bash
   /shannon:test --create --platform web --feature "user login"
   ```

   **Expected Output:**
   - Test suite generated
   - Uses Puppeteer MCP for browser automation
   - No mock objects in code
   - Tests interact with real browser

2. **Inspect Generated Test Code**

   **Verify:**
   - Uses `mcp__puppeteer__*` tools
   - No mock frameworks imported (no jest.mock, sinon, etc.)
   - Real browser navigation commands
   - Actual DOM interaction
   - Real network requests

3. **Request API Tests**
   ```bash
   /shannon:test --create --platform api --endpoint "/api/tasks"
   ```

   **Expected Output:**
   - Test suite generated
   - Uses real HTTP client (fetch, axios)
   - Tests hit actual endpoints
   - No mocked responses

4. **Verify Test Guardian Enforcement**

   **Check:**
   - Test Guardian agent activated during test creation
   - NO MOCKS philosophy documented in test file
   - Instructions for running tests against real services
   - No bypass mechanisms present

**Success Criteria:**
- ✅ Zero mock objects in generated tests
- ✅ All tests use real environments
- ✅ Puppeteer MCP integrated for browser tests
- ✅ Test Guardian enforces principles
- ✅ Test files include NO MOCKS documentation

---

## Test 4: MCP Integration

**Scenario:** Verify graceful degradation without optional MCPs

**Objective:** Shannon works with only Serena, degrades gracefully without optional MCPs

**Test 4A: Sequential MCP Missing**

1. **Check MCP Status**
   ```bash
   /shannon:check_mcps
   ```

   **Note:** Sequential MCP status

2. **Analyze Complex Spec (Without Sequential)**
   ```bash
   /shannon:spec "Build distributed microservices architecture with event sourcing"
   ```

   **Expected Behavior:**
   - Falls back to default analysis
   - Still completes successfully
   - Shows warning about Sequential MCP benefit
   - Provides valid complexity score
   - Does not crash or fail

3. **Compare with Sequential Available**
   - Install Sequential MCP
   - Run same analysis
   - Note improved reasoning depth

**Test 4B: Puppeteer MCP Missing**

1. **Request Web Tests (Without Puppeteer)**
   ```bash
   /shannon:test --create --platform web
   ```

   **Expected Behavior:**
   - Recognizes Puppeteer unavailable
   - Falls back to manual testing guidance
   - Provides test checklist instead
   - Suggests installing Puppeteer
   - Does not crash or fail

**Test 4C: Context7 MCP Missing**

1. **Request Framework Pattern (Without Context7)**
   ```bash
   /shannon:scaffold --framework react
   ```

   **Expected Behavior:**
   - Uses built-in patterns
   - Still generates valid scaffolding
   - Shows note about Context7 benefit
   - Does not crash or fail

**Success Criteria:**
- ✅ Shannon works with Serena MCP only
- ✅ Graceful degradation for optional MCPs
- ✅ Clear warnings about missing capabilities
- ✅ No crashes or failures
- ✅ Helpful suggestions for MCP installation

---

## Test 5: Backward Compatibility

**Scenario:** Verify all V3 commands work identically in V4

**Objective:** 100% V3 backward compatibility confirmed

**Steps:**

1. **Test V3 Commands with V3 Syntax**

   ```bash
   # Original V3 commands should work identically
   /shannon:spec "Build app"
   /shannon:checkpoint "test"
   /shannon:restore "test"
   /shannon:status
   /shannon:north_star "Goal"
   ```

2. **Compare Output Formats**

   **Verify:**
   - Same output structure as V3
   - Same required arguments
   - Same optional arguments
   - Same error messages
   - Same success confirmations

3. **Test Edge Cases**

   ```bash
   # V3 edge cases should work
   /shannon:spec ""  # Empty spec (should error)
   /shannon:restore "nonexistent"  # Missing checkpoint (should error)
   /shannon:checkpoint ""  # Empty name (should error)
   ```

   **Expected:**
   - Same error handling as V3
   - Same error messages
   - Same guidance provided

4. **Test V3 Workflows**

   Execute complete V3 workflow:
   - Analyze spec
   - Set north star
   - Create checkpoint
   - Simulate loss
   - Restore checkpoint
   - Verify state

   **Compare:**
   - Same behavior as V3
   - Same data persistence
   - Same user experience

**Success Criteria:**
- ✅ All V3 commands work unchanged
- ✅ Same output formats maintained
- ✅ Same argument signatures
- ✅ Same error handling
- ✅ V3 workflows complete successfully
- ✅ Zero breaking changes

---

## Test Execution Protocol

### Prerequisites

1. **Claude Code Environment**
   - Claude Code installed and running
   - Shannon V4 plugin installed
   - Project directory accessible

2. **Required MCPs**
   - Serena MCP installed (mandatory)

3. **Optional MCPs** (for full testing)
   - Sequential MCP
   - Puppeteer MCP
   - Context7 MCP

### Execution Guidelines

1. **Manual Execution Required**
   - All tests must be run manually in Claude Code
   - NO automation or scripting (follows NO MOCKS)
   - Real user interaction required

2. **Documentation**
   - Record all test results
   - Document any failures
   - Capture unexpected behavior
   - Note performance issues

3. **Test Environment**
   - Clean project directory for each test suite
   - Fresh conversation for context loss tests
   - Document MCP configuration for each test

### Results Documentation

Create `test-results.txt` with format:

```
Shannon V4 Integration Test Results
Date: [DATE]
Tester: [NAME]
Environment: [DESCRIPTION]

Test 1: Complete Workflow
Status: [PASS/FAIL]
Notes: [OBSERVATIONS]

Test 2: Context Preservation
Status: [PASS/FAIL]
Notes: [OBSERVATIONS]

Test 3: NO MOCKS Enforcement
Status: [PASS/FAIL]
Notes: [OBSERVATIONS]

Test 4: MCP Integration
Status: [PASS/FAIL]
Notes: [OBSERVATIONS]

Test 5: Backward Compatibility
Status: [PASS/FAIL]
Notes: [OBSERVATIONS]

Overall: [PASS/FAIL]
Issues Found: [COUNT]
Critical Bugs: [COUNT]
Recommendations: [LIST]
```

---

## Validation Checklist

- [ ] All 5 tests executed
- [ ] All tests passed
- [ ] Test results documented
- [ ] MCP configurations tested
- [ ] Edge cases verified
- [ ] Performance acceptable
- [ ] No critical bugs found
- [ ] V3 compatibility confirmed
- [ ] NO MOCKS philosophy upheld
- [ ] Ready for release

---

## Notes

- These tests verify Shannon V4 core functionality
- Additional domain-specific tests may be needed
- Performance benchmarks should be separate
- Security audit should be separate
- Documentation completeness tested separately

**Testing Philosophy:** These integration tests follow Shannon's NO MOCKS principle - they must be executed in real environments with actual integrations. This ensures we validate real-world behavior, not simulated behavior.
