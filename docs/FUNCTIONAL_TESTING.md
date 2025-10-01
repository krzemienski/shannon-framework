# Shannon Framework Functional Testing Guide

## Table of Contents

1. [What Functional Testing Proves](#what-functional-testing-proves)
2. [Testing Architecture](#testing-architecture)
3. [Test Categories](#test-categories)
4. [Manual Testing Process](#manual-testing-process)
5. [Automated Testing Process](#automated-testing-process)
6. [Debug Workflow](#debug-workflow)
7. [Iteration Process](#iteration-process)
8. [Expected Results](#expected-results)
9. [Troubleshooting](#troubleshooting)
10. [Examples](#examples)

---

## What Functional Testing Proves

Functional tests validate that Shannon behavioral patterns actually work when executed in Claude Code. Unlike structural tests that validate file formats and syntax, functional tests prove the framework **executes correctly** in real usage scenarios.

### Core Validation Goals

1. **Commands Execute Correctly**
   - Shannon commands (`/sh:*`, `/sc:*`) are recognized by Claude
   - Commands trigger correct behavioral patterns
   - Output matches expected format and content
   - Error handling works as designed

2. **Artifacts Created Properly**
   - Files generated in correct locations
   - Content matches specifications
   - Directory structures follow conventions
   - File permissions and formats correct

3. **Behavior Modified Appropriately**
   - Claude follows Shannon patterns (not generic responses)
   - Personas activate automatically when triggered
   - MCP servers used correctly (shadcn for React, not Magic)
   - Wave orchestration coordinates multi-step operations

4. **Context Preserved Across Sessions**
   - Serena checkpoints save state correctly
   - PreCompact hook optimizes context before save
   - Context restoration works after reload
   - Session continuity maintained

5. **NO MOCKS Policy Enforced**
   - Real browsers used (Playwright)
   - Real mobile simulators used (Expo)
   - Real database operations (not mocked)
   - Real API calls (with appropriate test environments)

### What Tests DON'T Prove

- **User Experience**: Tests validate functionality, not UX quality
- **Performance**: No load testing or performance benchmarks
- **Security**: No penetration testing or security audits
- **Edge Cases**: Limited coverage of unusual scenarios
- **Production Readiness**: Tests run in controlled environments

---

## Testing Architecture

The Shannon testing system consists of four layers, each building on the previous:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Integration Tests (TODO)                          │
│ - Checkpoint/restore cycles                                │
│ - Wave orchestration workflows                             │
│ - Multi-command sequences                                  │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Behavioral Tests (IN PROGRESS)                    │
│ - Shannon patterns active                                  │
│ - MCP usage validation                                     │
│ - Agent activation logic                                   │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Command Tests (IN PROGRESS)                       │
│ - Command execution                                        │
│ - Output format validation                                │
│ - Artifact creation                                        │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Structural Tests (DONE ✅)                         │
│ - File validation                                          │
│ - YAML frontmatter parsing                                 │
│ - Component relationships                                  │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Structural Tests (DONE ✅)

**Purpose**: Validate framework files are properly structured

**Components**:
- `tests/structural/test_structure.py` - File existence and YAML parsing
- `tests/structural/test_components.py` - Component relationship validation
- `tests/structural/test_yaml_frontmatter.py` - Frontmatter syntax validation

**What They Prove**:
- All required Shannon files exist
- YAML frontmatter is valid
- Component dependencies are correct
- File naming follows conventions

**Status**: Complete and passing

### Layer 2: Command Tests (IN PROGRESS)

**Purpose**: Validate Shannon commands execute correctly

**Components**:
- `tests/functional/test_sh_commands.py` - `/sh:*` command suite
- `tests/functional/test_sc_commands.py` - `/sc:*` command suite
- `tests/functional/test_command_output.py` - Output format validation

**What They Prove**:
- Commands recognized by Claude
- Expected artifacts created
- Output matches specifications
- Error messages appropriate

**Status**: Core tests implemented, expanding coverage

### Layer 3: Behavioral Tests (IN PROGRESS)

**Purpose**: Validate Shannon behavioral patterns activate

**Components**:
- `tests/functional/test_personas.py` - Persona activation logic
- `tests/functional/test_mcp_usage.py` - MCP server selection
- `tests/functional/test_patterns.py` - Pattern adherence
- `tests/functional/test_no_mocks.py` - NO MOCKS enforcement

**What They Prove**:
- Personas activate automatically
- Correct MCP servers used
- Shannon patterns followed
- Mock detection and prevention

**Status**: Initial tests implemented, needs expansion

### Layer 4: Integration Tests (TODO)

**Purpose**: Validate multi-step workflows and state management

**Components**:
- `tests/functional/test_checkpoints.py` - Serena checkpoint/restore
- `tests/functional/test_waves.py` - Wave orchestration
- `tests/functional/test_workflows.py` - Multi-command sequences
- `tests/functional/test_precompact.py` - PreCompact hook optimization

**What They Prove**:
- State persists across sessions
- Waves coordinate properly
- Complex workflows complete
- Context optimization works

**Status**: Not yet implemented

---

## Test Categories

### Command Execution Tests

**Purpose**: Validate commands execute and produce expected results

**Test Cases**:
- `/sh:spec` - Generate PRD from natural language
- `/sh:checkpoint` - Save session state with Serena
- `/sh:restore` - Restore previous session
- `/sc:implement` - Implement features from specs
- `/sc:test` - Run test suites
- `/sc:wave` - Execute wave orchestration

**Validation Checklist**:
- [ ] Command recognized by Claude
- [ ] No "unknown command" errors
- [ ] Expected artifacts created
- [ ] Output format correct
- [ ] Execution time reasonable
- [ ] Error handling appropriate

**Example Test**:
```python
def test_sh_spec_execution():
    """Test /sh:spec command creates PRD"""
    # Execute command
    result = execute_command("/sh:spec @user-request.md")

    # Validate execution
    assert result.success, "Command failed to execute"
    assert result.execution_time < 60, "Command too slow"

    # Validate artifacts
    assert Path("specs/user-request.md").exists()
    assert validate_prd_format("specs/user-request.md")
```

### Behavioral Pattern Tests

**Purpose**: Validate Shannon behavioral modifications active

**Test Cases**:
- Persona auto-activation
- MCP server selection
- Pattern adherence
- Context preservation
- NO MOCKS enforcement

**Validation Checklist**:
- [ ] Correct persona activated
- [ ] Appropriate MCP servers used
- [ ] Shannon patterns followed (not generic)
- [ ] Context maintained across operations
- [ ] No mocks detected in output

**Example Test**:
```python
def test_react_implementation_uses_shadcn():
    """Test React implementation uses shadcn MCP, not Magic"""
    # Execute implementation command
    result = execute_command("/sc:implement @spec.md --react")

    # Validate MCP usage
    mcp_calls = extract_mcp_calls(result.debug_log)
    assert "mcp__shadcn" in mcp_calls, "Should use shadcn MCP"
    assert "mcp__magic" not in mcp_calls, "Should NOT use Magic MCP"

    # Validate component structure
    component = read_file("src/components/Feature.tsx")
    assert "from '@/components/ui'" in component
```

### Integration Tests

**Purpose**: Validate multi-step workflows and state management

**Test Cases**:
- Checkpoint → Restore cycle
- Wave orchestration (5+ operations)
- Multi-command workflows
- PreCompact hook optimization
- Cross-session continuity

**Validation Checklist**:
- [ ] State saved correctly
- [ ] State restored accurately
- [ ] Waves coordinate properly
- [ ] Context preserved
- [ ] PreCompact reduces size

**Example Test**:
```python
def test_checkpoint_restore_cycle():
    """Test full checkpoint and restore workflow"""
    # Initial state
    execute_command("/sh:spec @request.md")
    initial_context = get_context_state()

    # Checkpoint
    checkpoint_result = execute_command("/sh:checkpoint")
    assert checkpoint_result.success

    # Simulate session end
    clear_context()

    # Restore
    restore_result = execute_command("/sh:restore")
    restored_context = get_context_state()

    # Validate restoration
    assert restored_context == initial_context
```

### End-to-End Tests

**Purpose**: Validate complete user workflows

**Test Cases**:
- Idea → Spec → Implementation → Test → Deploy
- Bug Report → Debug → Fix → Test → PR
- Feature Request → Research → Design → Implement → Document
- Legacy Code → Analyze → Refactor → Test → Modernize

**Validation Checklist**:
- [ ] All steps complete successfully
- [ ] Artifacts created at each step
- [ ] Context preserved throughout
- [ ] Final output meets requirements
- [ ] NO MOCKS used anywhere

**Example Test**:
```python
def test_full_feature_workflow():
    """Test complete feature development workflow"""
    # Step 1: Spec
    spec_result = execute_command("/sh:spec 'Add user authentication'")
    assert Path("specs/user-authentication.md").exists()

    # Step 2: Implement
    impl_result = execute_command("/sc:implement @specs/user-authentication.md")
    assert Path("src/auth/").exists()

    # Step 3: Test
    test_result = execute_command("/sc:test --focus auth")
    assert test_result.tests_passed > 0

    # Step 4: Document
    doc_result = execute_command("/sc:document @src/auth/")
    assert Path("docs/authentication.md").exists()
```

---

## Manual Testing Process

Manual testing is used when:
- Automated testing not yet available
- Complex scenarios require human judgment
- Visual validation needed
- Exploratory testing helpful

### Step 1: Select Test Case

Choose from manual test templates in `tests/functional/manual/`:

| Test Case | Purpose | Complexity |
|-----------|---------|------------|
| `test_case_sh_spec.md` | Validate PRD generation | Low |
| `test_case_sh_checkpoint.md` | Validate state persistence | Medium |
| `test_case_sc_implement_react.md` | Validate React + shadcn | High |
| `test_case_wave_orchestration.md` | Validate wave coordination | High |
| `test_case_precompact_hook.md` | Validate context optimization | Medium |
| `test_case_no_mocks_enforcement.md` | Validate NO MOCKS policy | Medium |

**Selection Criteria**:
- **Priority**: Critical path features first
- **Complexity**: Start simple, increase gradually
- **Dependencies**: Test prerequisites before dependents
- **Risk**: High-risk areas need more testing

### Step 2: Prepare Test Environment

1. **Clean Workspace**:
```bash
cd /Users/nick/Documents/shannon-framework
git status # Ensure clean state
rm -rf test-project/ # Remove previous test artifacts
```

2. **Create Test Project** (if needed):
```bash
mkdir test-project
cd test-project
npm init -y # For React/Node tests
```

3. **Load Shannon Context**:
```bash
# In Claude Code
/load /Users/nick/Documents/shannon
```

4. **Verify Prerequisites**:
- [ ] Shannon framework loaded
- [ ] MCP servers available (check status)
- [ ] Test environment clean
- [ ] Required tools installed (Node, Python, etc.)

### Step 3: Execute Test Case

Follow step-by-step instructions in the manual test template:

**Example: test_case_sh_spec.md**

```markdown
## Test Case: /sh:spec Command

### Prerequisites
- Shannon framework loaded
- Clean workspace
- Sample user request available

### Execution Steps

1. **Prepare Input**:
   - Create `user-request.md` with natural language feature request

2. **Execute Command**:
   ```
   /sh:spec @user-request.md
   ```

3. **Observe Execution**:
   - Note execution time
   - Watch for errors or warnings
   - Observe MCP server calls
   - Check Claude's reasoning process

4. **Validate Output Checklist**:
   - [ ] PRD file created in `specs/` directory
   - [ ] PRD contains all required sections
   - [ ] Format matches specification template
   - [ ] Content is specific (not generic)
   - [ ] No placeholder text (e.g., "TODO", "[...]")
   - [ ] Requirements are testable
   - [ ] Technical details included

5. **Validate Artifacts Checklist**:
   - [ ] File: `specs/[feature-name].md`
   - [ ] Size: > 1KB (not empty or minimal)
   - [ ] Format: Valid Markdown with YAML frontmatter
   - [ ] Structure: Follows PRD template sections
   - [ ] Content: Specific to user request

6. **Collect Debug Information**:
   - Command output (copy full text)
   - Claude's reasoning (if visible)
   - MCP server calls (if logged)
   - Any error messages
   - Execution time
```

### Step 4: Record Results

Save all test artifacts to `test-results/[test-id]/`:

**Directory Structure**:
```
test-results/
└── TR-20250110-001/
    ├── result.json           # Pass/fail with details
    ├── output.md             # Command output
    ├── artifacts/            # Created files
    │   └── specs/
    │       └── feature.md
    ├── screenshots/          # Execution screenshots
    │   ├── 01-command.png
    │   ├── 02-execution.png
    │   └── 03-output.png
    ├── logs/                 # Debug logs
    │   ├── mcp-calls.log
    │   └── execution.log
    └── notes.md              # Additional observations
```

**result.json Format**:
```json
{
  "test_id": "TR-20250110-001",
  "test_case": "test_case_sh_spec",
  "timestamp": "2025-01-10T14:30:00Z",
  "status": "pass",
  "execution_time": 45.3,
  "checklist": {
    "output_validation": {
      "prd_created": true,
      "all_sections_present": true,
      "format_correct": true,
      "content_specific": true,
      "no_placeholders": true,
      "requirements_testable": true,
      "technical_details": true
    },
    "artifact_validation": {
      "file_created": true,
      "correct_location": true,
      "proper_size": true,
      "valid_format": true,
      "matches_template": true,
      "content_quality": true
    }
  },
  "issues": [],
  "notes": "Execution completed successfully. PRD quality high."
}
```

### Step 5: Analyze Results

**For Passing Tests**:
1. Document successful patterns
2. Note best practices observed
3. Update automation candidates list
4. Archive results for reference

**For Failing Tests**:
1. Categorize failure type:
   - Command not recognized
   - Incorrect behavior
   - Missing artifacts
   - Format errors
   - Performance issues
2. Collect debug information
3. Create GitHub issue (if framework bug)
4. Update test case (if test issue)
5. Proceed to debug workflow

---

## Automated Testing Process

Automated tests run without human intervention, providing fast feedback and regression detection.

### Running Tests

**Run All Tests**:
```bash
cd /Users/nick/Documents/shannon
python3 tests/functional/run_tests.py
```

**Output**:
```
Shannon Framework Functional Tests
==================================

Running structural tests...
✅ test_structure.py ...................... 15/15 passed
✅ test_components.py ..................... 8/8 passed
✅ test_yaml_frontmatter.py ............... 12/12 passed

Running command tests...
✅ test_sh_commands.py .................... 10/12 passed
❌ test_sc_commands.py .................... 6/10 passed

Running behavioral tests...
✅ test_personas.py ....................... 5/5 passed
⚠️  test_mcp_usage.py ..................... 3/4 passed

Summary:
--------
Total: 59 tests
Passed: 54 (91.5%)
Failed: 4 (6.8%)
Warnings: 1 (1.7%)

Time: 2m 34s

See test-results/TEST_REPORT_20250110_143000.md for details.
```

**Run Specific Category**:
```bash
# Structural tests only
python3 tests/functional/run_tests.py --category structural

# Command tests only
python3 tests/functional/run_tests.py --category command

# Behavioral tests only
python3 tests/functional/run_tests.py --category behavioral
```

**Run Specific Test File**:
```bash
python3 tests/functional/run_tests.py --file test_sh_commands.py
```

**Run with Verbose Output**:
```bash
python3 tests/functional/run_tests.py --verbose
```

**Run with Debug Information**:
```bash
python3 tests/functional/run_tests.py --debug
```

### Understanding Test Results

**Test Report Format**:

`test-results/TEST_REPORT_20250110_143000.md`:
```markdown
# Shannon Framework Test Report

**Date**: 2025-01-10 14:30:00
**Total Tests**: 59
**Passed**: 54 (91.5%)
**Failed**: 4 (6.8%)
**Warnings**: 1 (1.7%)

## Summary by Category

### Structural Tests: ✅ 35/35 (100%)
All structural tests passed.

### Command Tests: ⚠️ 16/22 (72.7%)
Issues detected in SC commands.

### Behavioral Tests: ✅ 8/9 (88.9%)
Minor MCP usage issue.

## Failed Tests

### ❌ test_sc_implement_react_component
**Category**: Command
**Failure**: Component not created
**Error**: FileNotFoundError: src/components/Feature.tsx
**Location**: tests/functional/test_sc_commands.py:145
**Debug**: See test-results/failed/test_sc_implement_react_component/

### ❌ test_sc_implement_uses_shadcn
**Category**: Behavioral
**Failure**: Wrong MCP server used
**Error**: Magic MCP called instead of shadcn
**Location**: tests/functional/test_mcp_usage.py:78
**Debug**: See test-results/failed/test_sc_implement_uses_shadcn/

## Warnings

### ⚠️ test_persona_activation_timing
**Category**: Behavioral
**Warning**: Persona activated slower than expected (3.2s vs 2.0s target)
**Impact**: Functional but performance concern
**Location**: tests/functional/test_personas.py:92

## Recommendations

1. **Fix Critical**: test_sc_implement_react_component
   - Root cause: Command not creating component file
   - Action: Debug /sc:implement command logic

2. **Fix High Priority**: test_sc_implement_uses_shadcn
   - Root cause: MCP selection logic incorrect
   - Action: Update MCP routing rules

3. **Investigate**: test_persona_activation_timing
   - Root cause: Slower than expected activation
   - Action: Profile persona activation code
```

### Continuous Integration

**GitHub Actions Workflow** (`.github/workflows/test.yml`):
```yaml
name: Shannon Framework Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run structural tests
      run: |
        python3 tests/functional/run_tests.py --category structural

    - name: Run command tests
      run: |
        python3 tests/functional/run_tests.py --category command

    - name: Run behavioral tests
      run: |
        python3 tests/functional/run_tests.py --category behavioral

    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: test-results/

    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('test-results/TEST_REPORT_latest.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: report
          });
```

---

## Debug Workflow

When tests fail, systematic debugging identifies and resolves issues efficiently.

### Step 1: Review Test Report

Start with the high-level test report to understand failure patterns:

```bash
cat test-results/TEST_REPORT_latest.md
```

**Key Questions**:
- How many tests failed?
- Are failures clustered in one category?
- Are failures related (same root cause)?
- Are there new failures (regression)?

### Step 2: Examine Failed Test Details

Navigate to failed test directory:

```bash
cd test-results/failed/test_sc_implement_react_component/
ls -la
```

**Files to Review**:
- `error.log` - Exception details and stack trace
- `output.md` - Command output before failure
- `context.json` - Test environment state
- `debug.log` - Verbose execution log
- `mcp-calls.log` - MCP server interactions

**Example error.log**:
```
Traceback (most recent call last):
  File "tests/functional/test_sc_commands.py", line 148, in test_sc_implement_react_component
    assert Path("src/components/Feature.tsx").exists()
AssertionError: Component file not created

Test Context:
- Command: /sc:implement @specs/feature.md --react
- Working Dir: /tmp/test-project-20250110-143045/
- Expected: src/components/Feature.tsx
- Actual: File not found

Debug Information:
- Command recognized: Yes
- Execution completed: Yes
- Error during execution: No
- Artifacts created: 0
- MCP calls made: 3 (serena, context7, shadcn)
```

### Step 3: Identify Root Cause

Use the iteration debugger to analyze failure:

```bash
python3 tests/functional/iteration_debugger.py \
  --test test_sc_implement_react_component \
  --result test-results/failed/test_sc_implement_react_component/
```

**Debugger Output**:
```
Shannon Framework Iteration Debugger
====================================

Analyzing: test_sc_implement_react_component

Root Cause Analysis:
-------------------

1. Command Execution: ✅ SUCCESS
   - Command recognized by Claude
   - Execution completed without errors
   - Runtime: 12.3s (normal)

2. Persona Activation: ✅ SUCCESS
   - Implementer persona activated
   - Activation time: 0.8s
   - Confidence: 0.95

3. MCP Server Usage: ✅ SUCCESS
   - Correct servers called (serena, context7, shadcn)
   - No Magic MCP calls detected
   - MCP responses received successfully

4. Artifact Creation: ❌ FAILURE
   - Expected: src/components/Feature.tsx
   - Actual: File not created
   - Reason: Implementation logic did not execute file write

5. Shannon Pattern Adherence: ⚠️ WARNING
   - Pattern followed: Yes
   - Completeness: Partial
   - Issue: Implementation stopped after planning

Root Cause: Implementation command completed planning phase but did not
execute file creation. Likely issue in transition from planning to execution.

Recommended Actions:
1. Review /sc:implement command logic for execution phase
2. Check if file write operations are being called
3. Verify working directory is correct
4. Add logging to implementation execution phase

Similar Failures: 2 related tests also failing with same pattern
- test_sc_implement_api_endpoint
- test_sc_implement_database_schema
```

### Step 4: Classify Failure Type

Categorize the failure to determine appropriate fix:

**Failure Types**:

1. **Command Not Recognized**
   - Symptom: "Unknown command" error
   - Root Cause: Command not registered or typo
   - Fix: Update command registry or fix command name

2. **Incorrect Behavior**
   - Symptom: Command executes but wrong behavior
   - Root Cause: Logic error in command implementation
   - Fix: Debug and fix command logic

3. **Missing Artifacts**
   - Symptom: Expected files not created
   - Root Cause: File write operations not executing
   - Fix: Add/fix file creation code

4. **Format Errors**
   - Symptom: Artifacts created but wrong format
   - Root Cause: Template or formatting issue
   - Fix: Update templates or formatting logic

5. **Performance Issues**
   - Symptom: Tests pass but too slow
   - Root Cause: Inefficient operations
   - Fix: Optimize code or MCP usage

6. **Flaky Tests**
   - Symptom: Tests pass sometimes, fail sometimes
   - Root Cause: Race conditions or external dependencies
   - Fix: Add proper waits or mock external dependencies

### Step 5: Apply Fix

Based on root cause, apply appropriate fix:

**Example Fix for Missing Artifacts**:

Before (broken):
```yaml
# agents/implementer.md
steps:
  plan_implementation:
    action: "Analyze spec and create implementation plan"
    output: "Implementation plan"

  # Missing: actual implementation step
```

After (fixed):
```yaml
# agents/implementer.md
steps:
  plan_implementation:
    action: "Analyze spec and create implementation plan"
    output: "Implementation plan"

  execute_implementation:
    action: "Create files based on implementation plan"
    operations:
      - write_component_files
      - write_test_files
      - update_imports
    validation:
      - verify_files_created
      - verify_syntax_valid
```

### Step 6: Verify Fix

Run the specific test again to verify fix:

```bash
python3 tests/functional/run_tests.py \
  --file test_sc_commands.py \
  --test test_sc_implement_react_component \
  --verbose
```

**Expected Output**:
```
Running test_sc_implement_react_component...

✅ Command recognized
✅ Persona activated
✅ MCP servers called correctly
✅ Component file created
✅ Test file created
✅ Imports updated
✅ Syntax valid

Test: PASSED (12.3s)
```

### Step 7: Check for Regressions

Run full test suite to ensure fix didn't break other tests:

```bash
python3 tests/functional/run_tests.py
```

**Regression Checklist**:
- [ ] All previously passing tests still pass
- [ ] No new failures introduced
- [ ] Performance not degraded
- [ ] Related tests still pass

---

## Iteration Process

Functional testing follows an iterative improve-test-fix cycle until all tests pass.

### Iteration Cycle

```
┌─────────────────────────────────────────────────────────┐
│ Iteration N                                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Run Tests          → test-results/REPORT_N.md      │
│     └─ Record results  → N tests passed, M tests failed│
│                                                         │
│  2. Analyze Failures   → Identify root causes          │
│     └─ Group by type   → Command / Behavioral / etc    │
│                                                         │
│  3. Prioritize Fixes   → Critical → High → Medium      │
│     └─ Select targets  → Fix K highest priority issues │
│                                                         │
│  4. Apply Fixes        → Update Shannon files          │
│     └─ Document changes→ Update CHANGELOG.md           │
│                                                         │
│  5. Verify Fixes       → Run affected tests            │
│     └─ Check regressions→ Run full suite               │
│                                                         │
│  6. Update Metrics     → Track progress                │
│     └─ Record learnings→ Document patterns             │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
           All tests passing? ──No──→ Iteration N+1
                         │
                        Yes
                         │
                         ▼
                  ✅ Testing Complete
```

### Example Iteration Sequence

**Iteration 1: Initial Run**
```bash
python3 tests/functional/run_tests.py
```

**Results**:
```
Total: 30 tests
Passed: 20 (66.7%)
Failed: 10 (33.3%)

Failed Tests:
- 6 command tests (missing artifacts)
- 3 behavioral tests (wrong MCP usage)
- 1 integration test (checkpoint failure)
```

**Actions**:
1. Fix missing artifacts issue (affects 6 tests)
2. Update MCP routing rules (affects 3 tests)
3. Debug checkpoint logic (affects 1 test)

---

**Iteration 2: After Fixes**
```bash
python3 tests/functional/run_tests.py
```

**Results**:
```
Total: 30 tests
Passed: 27 (90.0%)
Failed: 3 (10.0%)

Failed Tests:
- 2 behavioral tests (persona timing)
- 1 integration test (wave coordination)
```

**Analysis**:
- Previous fixes successful ✅
- New issues discovered in performance and coordination
- No regressions detected ✅

**Actions**:
1. Optimize persona activation (affects 2 tests)
2. Debug wave orchestration logic (affects 1 test)

---

**Iteration 3: Performance Fixes**
```bash
python3 tests/functional/run_tests.py
```

**Results**:
```
Total: 30 tests
Passed: 29 (96.7%)
Failed: 1 (3.3%)

Failed Tests:
- 1 integration test (wave coordination edge case)
```

**Analysis**:
- Persona timing fixed ✅
- Wave coordination issue persists
- Deep dive needed into wave logic

**Actions**:
1. Debug wave coordination with verbose logging
2. Review wave orchestration patterns
3. Add additional validation to wave execution

---

**Iteration 4: Final Fix**
```bash
python3 tests/functional/run_tests.py
```

**Results**:
```
Total: 30 tests
Passed: 30 (100.0%) ✅

All tests passing!
```

**Actions**:
1. Document iteration insights
2. Update testing documentation
3. Create regression test suite
4. Archive test results

### Tracking Progress

**Progress Metrics** (`test-results/PROGRESS.md`):
```markdown
# Shannon Framework Testing Progress

## Iteration History

| Iteration | Date | Tests | Passed | Failed | Pass Rate |
|-----------|------|-------|--------|--------|-----------|
| 1 | 2025-01-08 | 30 | 20 | 10 | 66.7% |
| 2 | 2025-01-09 | 30 | 27 | 3 | 90.0% |
| 3 | 2025-01-10 | 30 | 29 | 1 | 96.7% |
| 4 | 2025-01-10 | 30 | 30 | 0 | 100.0% ✅ |

## Issues Fixed by Iteration

### Iteration 1 → 2 (7 fixes)
- Fixed missing artifact creation in /sc:implement
- Updated MCP routing to prefer shadcn over Magic
- Fixed checkpoint serialization format

### Iteration 2 → 3 (2 fixes)
- Optimized persona activation timing
- Fixed wave coordination edge case

### Iteration 3 → 4 (1 fix)
- Resolved wave orchestration state management

## Lessons Learned

1. **Systematic Approach Works**: Fixing high-impact issues first maximized progress
2. **Root Cause Analysis Essential**: Debugger tool identified related failures
3. **Regression Testing Critical**: Full suite runs caught side effects early
4. **Documentation Helps**: Clear test cases made debugging faster
```

---

## Expected Results

When functional testing is complete and all tests pass, you can confidently claim:

### ✅ Commands Execute Correctly

**Proof**:
- All Shannon commands (`/sh:*`, `/sc:*`) recognized by Claude
- Commands execute without errors
- Execution time within acceptable ranges
- Error handling works as designed

**Test Coverage**:
- 15+ command execution tests passing
- Edge case handling validated
- Error recovery tested

### ✅ Artifacts Created Properly

**Proof**:
- All expected files generated
- Files in correct locations
- Content matches specifications
- Formats valid (YAML, Markdown, code)

**Test Coverage**:
- File creation tests for each command
- Directory structure validation
- Content format verification

### ✅ Behavior Modified Appropriately

**Proof**:
- Shannon patterns active (not generic Claude responses)
- Personas activate automatically when triggered
- MCP servers selected correctly
- Wave orchestration coordinates operations

**Test Coverage**:
- Persona activation tests
- MCP usage validation tests
- Pattern adherence tests
- Wave coordination tests

### ✅ Context Preserved Across Sessions

**Proof**:
- Serena checkpoints save state correctly
- PreCompact hook optimizes context
- State restores accurately after reload
- Session continuity maintained

**Test Coverage**:
- Checkpoint/restore cycle tests
- PreCompact optimization tests
- Cross-session persistence tests

### ✅ NO MOCKS Policy Enforced

**Proof**:
- Real browsers used (Playwright)
- Real mobile simulators used
- No mock objects detected in output
- Production-like testing environments

**Test Coverage**:
- Mock detection tests
- Real system integration tests
- End-to-end workflow tests

### Confidence Levels

**High Confidence (90%+)**:
- Structural tests: 100% coverage, all passing
- Command tests: 95%+ passing
- Core behaviors: 90%+ passing

**Medium Confidence (70-90%)**:
- Complex workflows: 80%+ passing
- Edge cases: 75%+ passing
- Performance: Within targets

**Areas Needing Improvement (<70%)**:
- Integration tests: Not yet fully implemented
- Load testing: Not yet covered
- Security testing: Not yet covered

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Tests Fail with "Command Not Recognized"

**Symptoms**:
```
Error: Unknown command '/sh:spec'
Command not found in Claude Code
```

**Root Causes**:
1. Shannon framework not loaded
2. Command registry not initialized
3. Typo in command name

**Solutions**:
```bash
# Verify Shannon loaded
/load /Users/nick/Documents/shannon

# Check command registry
cat /Users/nick/Documents/shannon/core/COMMANDS.md

# Verify command name spelling
grep -r "command:" /Users/nick/Documents/shannon/
```

#### Issue: Artifacts Not Created

**Symptoms**:
```
AssertionError: Expected file not found
FileNotFoundError: src/components/Feature.tsx
```

**Root Causes**:
1. File write operations not executing
2. Working directory incorrect
3. Path resolution issues

**Solutions**:
```python
# Add debug logging
def test_with_debugging():
    print(f"Working directory: {os.getcwd()}")
    result = execute_command("/sc:implement @spec.md")
    print(f"Files created: {os.listdir('src/')}")

# Check command output
print(result.stdout)  # Look for file creation messages

# Verify paths
assert Path("src/components/").exists(), "Component directory not created"
```

#### Issue: Wrong MCP Server Used

**Symptoms**:
```
AssertionError: Magic MCP called instead of shadcn
Expected: mcp__shadcn
Actual: mcp__magic
```

**Root Causes**:
1. MCP routing rules incorrect
2. Context not properly set
3. Persona not activated

**Solutions**:
```yaml
# Update MCP routing in core/MCP.md
react_implementation:
  primary: shadcn  # Force shadcn, not Magic
  fallback: context7
  blocked: [magic]  # Explicitly block Magic

# Verify persona activation
assert "implementer" in get_active_personas()
```

#### Issue: Tests Pass Locally, Fail in CI

**Symptoms**:
```
Local: 30/30 tests passing ✅
CI: 25/30 tests failing ❌
```

**Root Causes**:
1. Environment differences
2. Missing dependencies
3. Timing issues (race conditions)
4. File path differences

**Solutions**:
```yaml
# Add explicit waits
- name: Wait for MCP servers
  run: sleep 5

# Install all dependencies
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    npm install

# Use absolute paths
test_path = os.path.join(os.getcwd(), "test-project")

# Add retries for flaky tests
@pytest.mark.flaky(reruns=3)
def test_sometimes_fails():
    pass
```

#### Issue: Slow Test Execution

**Symptoms**:
```
Total test time: 15 minutes (expected: 3 minutes)
Individual tests timing out
```

**Root Causes**:
1. Too many sequential operations
2. Not using parallelization
3. Inefficient MCP calls
4. Large file operations

**Solutions**:
```python
# Run tests in parallel
pytest -n auto  # Use all CPU cores

# Batch operations
results = execute_commands_batch([
    "/sh:spec @request1.md",
    "/sh:spec @request2.md",
    "/sh:spec @request3.md"
])

# Cache MCP results
@lru_cache(maxsize=128)
def get_mcp_result(query):
    return mcp_call(query)

# Use smaller test fixtures
test_project = create_minimal_project()  # Not full project
```

#### Issue: Flaky Tests

**Symptoms**:
```
Test passes: Run 1, Run 3, Run 5
Test fails: Run 2, Run 4, Run 6
```

**Root Causes**:
1. Race conditions
2. External dependencies
3. Non-deterministic behavior
4. State leakage between tests

**Solutions**:
```python
# Add explicit waits
import time
execute_command("/sh:spec @request.md")
time.sleep(2)  # Wait for file system sync
assert Path("specs/request.md").exists()

# Isolate test state
@pytest.fixture(autouse=True)
def reset_state():
    clear_context()
    delete_test_artifacts()
    yield
    cleanup()

# Make tests deterministic
random.seed(12345)  # Fixed seed
os.environ["DETERMINISTIC"] = "true"

# Retry flaky tests
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_sometimes_flaky():
    pass
```

### Debug Tools

#### Test Runner Debug Mode

```bash
# Verbose output
python3 tests/functional/run_tests.py --verbose

# Full debug information
python3 tests/functional/run_tests.py --debug

# Stop on first failure
python3 tests/functional/run_tests.py --failfast

# Run single test with debugging
python3 -m pytest tests/functional/test_sc_commands.py::test_sc_implement -vv -s
```

#### Iteration Debugger

```bash
# Analyze specific test failure
python3 tests/functional/iteration_debugger.py \
  --test test_sc_implement_react_component \
  --result test-results/failed/test_sc_implement_react_component/

# Compare iterations
python3 tests/functional/iteration_debugger.py \
  --compare iteration1 iteration2

# Generate debug report
python3 tests/functional/iteration_debugger.py \
  --report test-results/DEBUG_REPORT.md
```

#### MCP Call Inspector

```bash
# View MCP calls for test
python3 tests/functional/mcp_inspector.py \
  --test test_sc_implement_react_component \
  --log test-results/failed/.../mcp-calls.log

# Compare expected vs actual MCP usage
python3 tests/functional/mcp_inspector.py \
  --expected shadcn,context7,serena \
  --actual magic,context7,serena \
  --diff
```

---

## Examples

### Example 1: Manual Test Execution

**Test Case**: Validate `/sh:spec` command creates PRD

**Setup**:
```bash
cd /Users/nick/Documents/shannon-framework
mkdir test-project
cd test-project

# Create user request
cat > user-request.md << 'EOF'
# User Request

I need a user authentication system with:
- Email/password login
- OAuth integration (Google, GitHub)
- Session management
- Password reset flow
EOF

# Load Shannon
# In Claude Code:
/load /Users/nick/Documents/shannon
```

**Execution**:
```
User: /sh:spec @user-request.md

Claude: I'll create a comprehensive PRD for the authentication system.

[Persona Activation]: Analyzer activated for requirement analysis
[MCP Usage]: Context7 for auth patterns, Serena for session storage

Creating PRD...

✅ PRD created: specs/user-authentication.md

Key sections:
- Product Overview
- User Stories (5 stories)
- Technical Requirements
- Security Considerations
- API Specifications
- Testing Strategy
```

**Validation**:
```bash
# Check file created
ls specs/user-authentication.md
# Output: specs/user-authentication.md

# Validate content
head -20 specs/user-authentication.md
# Output:
# ---
# id: user-authentication
# type: product-specification
# status: draft
# created: 2025-01-10
# ---
#
# # User Authentication System PRD
#
# ## Product Overview
# ...

# Check size
wc -l specs/user-authentication.md
# Output: 287 specs/user-authentication.md
```

**Result**: ✅ PASS
- PRD created in correct location
- Contains all required sections
- Content is specific (not generic)
- 287 lines (substantial detail)
- YAML frontmatter valid

### Example 2: Automated Test Run

**Test**: Validate React implementation uses shadcn MCP

**Test Code**:
```python
def test_sc_implement_uses_shadcn():
    """Test React implementation uses shadcn MCP, not Magic"""

    # Setup
    create_test_project()
    create_spec_file("specs/feature.md")

    # Execute
    result = execute_command("/sc:implement @specs/feature.md --react")

    # Validate MCP usage
    mcp_calls = extract_mcp_calls(result.debug_log)

    assert "mcp__shadcn" in mcp_calls, \
        f"Should use shadcn MCP. Actual calls: {mcp_calls}"

    assert "mcp__magic" not in mcp_calls, \
        f"Should NOT use Magic MCP. Actual calls: {mcp_calls}"

    # Validate component structure
    component_path = Path("src/components/Feature.tsx")
    assert component_path.exists(), "Component file not created"

    component_code = component_path.read_text()
    assert "from '@/components/ui'" in component_code, \
        "Should import from shadcn UI components"

    assert "use client" in component_code, \
        "Should be a client component"
```

**Execution**:
```bash
pytest tests/functional/test_mcp_usage.py::test_sc_implement_uses_shadcn -vv
```

**Output**:
```
tests/functional/test_mcp_usage.py::test_sc_implement_uses_shadcn

Setup: Creating test project...
Setup: Creating spec file...

Executing: /sc:implement @specs/feature.md --react
MCP Calls Detected:
  - mcp__serena (context management)
  - mcp__context7 (React patterns)
  - mcp__shadcn (UI components)

Validating MCP usage...
✅ shadcn MCP used correctly
✅ Magic MCP not called
✅ Component file created
✅ Component imports shadcn UI
✅ Component is client component

PASSED [100%]
```

### Example 3: Debug Workflow

**Scenario**: Test failing - component not created

**Initial Failure**:
```
❌ test_sc_implement_react_component
AssertionError: Component file not created
Expected: src/components/Feature.tsx
Actual: File not found
```

**Debug Step 1: Review Test Output**
```bash
cat test-results/failed/test_sc_implement_react_component/output.md
```

Output shows:
```
Command: /sc:implement @specs/feature.md --react
Execution: Completed
Duration: 12.3s
Personas: Implementer (activated)
MCP Calls: serena, context7, shadcn
Artifacts: 0 files created ⚠️
```

**Debug Step 2: Run Iteration Debugger**
```bash
python3 tests/functional/iteration_debugger.py \
  --test test_sc_implement_react_component
```

Debugger identifies:
```
Root Cause: Implementation logic completed planning but did not
execute file creation operations.

Issue Location: agents/implementer.md
Missing: File write operations in execute_implementation step

Recommendation: Add file creation logic to implementation execution
```

**Debug Step 3: Review Implementation Agent**
```bash
cat agents/implementer.md | grep -A 20 "execute_implementation"
```

Finds:
```yaml
execute_implementation:
  action: "Create implementation based on plan"
  # Missing: actual file operations
```

**Debug Step 4: Apply Fix**
```yaml
# agents/implementer.md
execute_implementation:
  action: "Create implementation based on plan"
  operations:
    - create_component_file:
        path: "src/components/{ComponentName}.tsx"
        template: "react_component"
        data: "{component_props}"
    - create_test_file:
        path: "src/components/{ComponentName}.test.tsx"
        template: "react_test"
        data: "{test_cases}"
  validation:
    - verify_files_exist
    - verify_syntax_valid
```

**Debug Step 5: Verify Fix**
```bash
pytest tests/functional/test_sc_commands.py::test_sc_implement_react_component -vv
```

Result:
```
✅ Component file created
✅ Test file created
✅ Syntax valid
✅ All validations passed

PASSED [100%]
```

### Example 4: Wave Orchestration Test

**Test**: Validate wave coordinates multi-step feature implementation

**Manual Test Template** (`tests/functional/manual/test_case_wave_orchestration.md`):

```markdown
## Test Case: Wave Orchestration

### Objective
Validate wave system coordinates complex multi-step operations

### Prerequisites
- Shannon framework loaded
- Test project with multiple features
- Clean workspace

### Execution Steps

1. **Create Complex Spec**:
   Feature requiring 5+ operations:
   - Database schema
   - API endpoints
   - React components
   - Tests
   - Documentation

2. **Execute Wave Command**:
   ```
   /sc:wave @specs/complex-feature.md
   ```

3. **Observe Wave Coordination**:
   - Wave 1: Analysis and planning
   - Wave 2: Database implementation
   - Wave 3: API implementation
   - Wave 4: UI implementation
   - Wave 5: Testing and documentation

4. **Validate Artifacts**:
   - [ ] Database schema created
   - [ ] API endpoints created
   - [ ] React components created
   - [ ] Tests created
   - [ ] Documentation created

5. **Validate Coordination**:
   - [ ] Waves executed in correct order
   - [ ] Dependencies respected
   - [ ] Context preserved between waves
   - [ ] All operations completed
   - [ ] No errors or warnings
```

**Automated Test**:
```python
def test_wave_orchestration_complex_feature():
    """Test wave system coordinates complex multi-step feature"""

    # Create complex spec
    spec = create_complex_spec(
        database=True,
        api=True,
        ui=True,
        tests=True,
        docs=True
    )

    # Execute wave
    wave_result = execute_command(f"/sc:wave @{spec}")

    # Validate wave execution
    assert wave_result.success
    assert wave_result.wave_count == 5

    # Validate artifacts
    artifacts = [
        "db/schema.sql",
        "api/endpoints.ts",
        "src/components/Feature.tsx",
        "tests/feature.test.tsx",
        "docs/feature.md"
    ]

    for artifact in artifacts:
        assert Path(artifact).exists(), f"Missing: {artifact}"

    # Validate coordination
    wave_log = parse_wave_log(wave_result.log)

    assert wave_log.waves[0].type == "analysis"
    assert wave_log.waves[1].type == "database"
    assert wave_log.waves[2].type == "api"
    assert wave_log.waves[3].type == "ui"
    assert wave_log.waves[4].type == "finalization"

    # Verify dependencies respected
    assert wave_log.waves[2].started_after(wave_log.waves[1])  # API after DB
    assert wave_log.waves[3].started_after(wave_log.waves[2])  # UI after API
```

---

## Additional Resources

### Documentation
- [Shannon Framework README](../README.md)
- [Architecture Documentation](./ARCHITECTURE.md)
- [Command Reference](../core/COMMANDS.md)
- [Testing Strategy](./TESTING_STRATEGY.md)

### Test Templates
- Manual test cases: `tests/functional/manual/`
- Automated test suite: `tests/functional/`
- Test utilities: `tests/functional/utils/`

### Debug Tools
- Iteration debugger: `tests/functional/iteration_debugger.py`
- MCP inspector: `tests/functional/mcp_inspector.py`
- Test report generator: `tests/functional/report_generator.py`

### Support
- GitHub Issues: https://github.com/nicholasgriffintn/shannon/issues
- Discussions: https://github.com/nicholasgriffintn/shannon/discussions

---

**Last Updated**: 2025-01-10
**Version**: 1.0.0
**Status**: Active
