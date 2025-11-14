# Shannon V3 Wave Execution Plan - Test-First Validation Strategy

**Date**: 2025-11-14
**Approach**: Test-First Validation (not greenfield rebuild)
**Philosophy**: Leverage existing code + systematic bash testing
**Timeline**: 8-12 hours to validated 100% completion

---

## Executive Summary

**Current Reality**:
- ✅ ALL 8 subsystem directories exist with code (~7,080 lines)
- ❌ NO systematic validation gates implemented
- ✅ Test framework partially exists (test_analyze.sh, run_all.sh)
- ❌ Missing: fixtures/, helpers.sh, validation gate tests for Waves 1-7

**Root Cause**: Code written without functional validation gates → cannot claim completion

**Strategy**: Complete testing infrastructure → Run all tests → Fix failures in parallel → Validate

---

## Wave Execution Plan

### WAVE 0: Complete Testing Infrastructure (FOUNDATION)

**Agent**: 1 agent (testing-infrastructure-builder)
**Duration**: 2-3 hours
**Parallelization**: None (foundation must be solid)

**Deliverables**:
1. **tests/fixtures/** directory with sample specs:
   - simple_spec.md (~100 words, complexity ~0.25)
   - moderate_spec.md (~500 words, complexity ~0.50)
   - complex_spec.md (~1500 words, complexity ~0.75)

2. **tests/functional/helpers.sh** (~50 lines):
   ```bash
   #!/bin/bash
   # Common test helper functions
   
   assert_contains() {
       local output="$1"
       local pattern="$2"
       local test_name="$3"
       if echo "$output" | grep -q "$pattern"; then
           echo "  ✅ $test_name"
           return 0
       else
           echo "  ❌ FAIL: $test_name"
           echo "     Expected pattern: $pattern"
           return 1
       fi
   }
   
   assert_exit_code() {
       local expected=$1
       local actual=$2
       local test_name="$3"
       if [ "$actual" -eq "$expected" ]; then
           echo "  ✅ $test_name"
       else
           echo "  ❌ FAIL: $test_name (expected $expected, got $actual)"
           return 1
       fi
   }
   
   extract_metric() {
       local output="$1"
       local metric_pattern="$2"
       echo "$output" | grep -oP "$metric_pattern" | head -1
   }
   ```

3. **Validation Gate Test Scripts** (8 scripts, ~40-60 lines each):

   **tests/functional/test_wave1_dashboard.sh**:
   ```bash
   #!/bin/bash
   source "$(dirname $0)/helpers.sh"
   
   echo "Testing Wave 1: Metrics & Dashboard"
   
   output=$(shannon analyze fixtures/simple_spec.md 2>&1)
   exit_code=$?
   
   assert_exit_code 0 $exit_code "Command execution"
   assert_contains "$output" "Shannon:" "Dashboard header"
   assert_contains "$output" "analyze" "Command name shown"
   assert_contains "$output" '\$[0-9]\+\.[0-9]\+' "Cost displayed"
   assert_contains "$output" "[0-9]\+\.*[0-9]*K\? tokens" "Tokens shown"
   assert_contains "$output" "[0-9]\+s" "Duration shown"
   assert_contains "$output" "[0-9]\+%" "Progress percentage"
   assert_contains "$output" "ACTIVE\|COMPLETE\|WAITING" "State indicator"
   
   echo "✅ Wave 1 validation PASSED"
   ```

   **tests/functional/test_wave2_mcp.sh**:
   ```bash
   #!/bin/bash
   source "$(dirname $0)/helpers.sh"
   
   echo "Testing Wave 2: MCP Management"
   
   # Test mcp-install command exists
   shannon mcp-install --help > /dev/null 2>&1
   assert_exit_code 0 $? "mcp-install command exists"
   
   # Test MCP server listing
   output=$(shannon mcp list 2>&1 || shannon mcp-list 2>&1 || echo "command_missing")
   if [ "$output" != "command_missing" ]; then
       echo "✅ MCP listing command exists"
   fi
   
   echo "✅ Wave 2 validation PASSED"
   ```

   **tests/functional/test_wave3_cache.sh**:
   ```bash
   #!/bin/bash
   source "$(dirname $0)/helpers.sh"
   
   echo "Testing Wave 3: Cache System"
   
   # Test cache stats command
   output=$(shannon cache stats 2>&1)
   assert_exit_code 0 $? "cache stats command"
   assert_contains "$output" "hit\|miss\|rate" "Cache metrics shown"
   
   # Test cache clear command
   shannon cache clear > /dev/null 2>&1
   assert_exit_code 0 $? "cache clear command"
   
   echo "✅ Wave 3 validation PASSED"
   ```

   **tests/functional/test_wave4_agents.sh** (agent control)
   **tests/functional/test_wave4_optimization.sh** (cost optimization)
   **tests/functional/test_wave5_analytics.sh** (analytics database)
   **tests/functional/test_wave6_context.sh** (context management)
   **tests/functional/test_wave7_integration.sh** (E2E integration)

**Validation Gate**: run_all.sh executes all 8 tests, all must pass

---

### DIAGNOSTIC: Run All Tests (AUTOMATED)

**Command**: `tests/functional/run_all.sh`
**Duration**: 5-10 minutes
**Output**: Pass/fail data for all 8 waves

**Expected Outcome**:
```
═══════════════════════════════════════════════════════
Shannon CLI Functional Test Suite
═══════════════════════════════════════════════════════

Running: test_analyze
✅ test_analyze PASSED

Running: test_wave1_dashboard
❌ test_wave1_dashboard FAILED
   (Dashboard not rendering correctly)

Running: test_wave2_mcp
✅ test_wave2_mcp PASSED

Running: test_wave3_cache
❌ test_wave3_cache FAILED
   (Cache stats command missing)

...

═══════════════════════════════════════════════════════
Test Summary
═══════════════════════════════════════════════════════
Total:  8
Passed: 3
Failed: 5

❌ SOME TESTS FAILED
```

**Analysis**: Identifies exactly which waves need fixing

---

### WAVE 1: Parallel Subsystem Fixes (DATA-DRIVEN)

**Agents**: N agents (where N = failed wave count from diagnostic)
**Duration**: 4-6 hours (max of all agents, not sum)
**Parallelization**: TRUE (independent subsystem fixes)

**Agent Allocation** (based on diagnostic results):

If Wave 1 (metrics) failed:
- **Agent 1: metrics-fixer**
  - Task: Fix src/shannon/metrics/dashboard.py rendering issues
  - Tests: Re-run test_wave1_dashboard.sh until passing
  - Deliverable: Working LiveDashboard with all metrics

If Wave 3 (cache) failed:
- **Agent 2: cache-fixer**
  - Task: Fix src/shannon/cache/ integration issues
  - Tests: Re-run test_wave3_cache.sh until passing
  - Deliverable: Working cache stats/clear commands

If Wave 4a (agents) failed:
- **Agent 3: agents-fixer**
  - Task: Fix src/shannon/agents/ controller issues
  - Tests: Re-run test_wave4_agents.sh until passing
  - Deliverable: Working agent coordination

... (spawn 1 agent per failed wave)

**Execution**: All agents spawn in ONE message for true parallelism

**Synthesis Checkpoint**: After all agents complete:
- Collect all fixes from Serena
- Aggregate test results
- Validate no conflicts between fixes
- Present to user for approval

---

### VALIDATION RUN: Re-Test All (AUTOMATED)

**Command**: `tests/functional/run_all.sh`
**Duration**: 5-10 minutes
**Expected**: All 8 tests PASS

If any tests still fail → Create Wave 2 (Additional Fixes) and iterate

---

## Dependency Graph

```
Wave 0 (Testing Infrastructure)
    ↓
Diagnostic Run (collect failure data)
    ↓
Wave 1 (Parallel Fixes) ←─── Based on diagnostic results
    ├─ Agent 1: Fix Wave 1 issues
    ├─ Agent 2: Fix Wave 3 issues      [TRUE PARALLELISM]
    ├─ Agent 3: Fix Wave 4a issues
    └─ ... (N agents for N failures)
    ↓
Validation Run (verify all tests pass)
    ↓
Wave 2 (If Needed) ←─── Only if tests still failing
    ↓
Final Validation → 100% Complete
```

---

## Complexity & Resource Estimates

**Wave 0 Complexity**: 0.30 (MODERATE)
- Task: Create bash test scripts (well-specified utilities)
- Agents: 1
- Duration: 2-3 hours

**Wave 1 Complexity**: Varies (0.40-0.70 depending on failure count)
- Task: Fix failing subsystems
- Agents: 3-7 (estimated, based on typical failure rate)
- Duration: 4-6 hours (parallel)
- Speedup: 2.5-3.5x vs sequential fixes

**Total Project Complexity**: 0.67 (COMPLEX) - validates wave-based approach

---

## Success Criteria

Shannon V3 is 100% complete when:
- ✅ All 8 validation gate tests pass (test_wave1 through test_wave7 + test_analyze)
- ✅ All Shannon commands functional (analyze, wave, cache, budget, analytics, etc.)
- ✅ All subsystems integrated through orchestrator
- ✅ NO MOCKS - all tests use real CLI execution
- ✅ Documentation updated with validated examples
- ✅ Final checkpoint created in Serena with "100% validated" status

**Evidence**: `tests/functional/run_all.sh` returns exit code 0 (all tests passed)

---

## Timeline Estimate

Best case (3 failures):
- Wave 0: 2 hours
- Diagnostic: 10 min
- Wave 1 (3 parallel fixes): 4 hours
- Validation: 10 min
- **Total: ~6.5 hours**

Worst case (7 failures):
- Wave 0: 3 hours
- Diagnostic: 10 min
- Wave 1 (7 parallel fixes): 6 hours
- Validation: 10 min
- Wave 2 (remaining fixes): 3 hours
- Final validation: 10 min
- **Total: ~12.5 hours**

Average case (5 failures):
- **Total: ~8-10 hours**

---

## Next Immediate Actions

1. ✅ Create pre-wave checkpoint (DONE - in Serena)
2. → Execute Wave 0: Single agent creates complete test framework
3. → Run diagnostic to collect objective failure data
4. → Based on results: Spawn parallel fix agents
5. → Validate all tests pass
6. → Create final validated checkpoint

---

**Strategy**: TEST-FIRST VALIDATION leveraging existing code with systematic bash testing framework

**Alignment**: Master plan's NO MOCKS philosophy + wave orchestration + validation gates

**Outcome**: Validated 100% completion in 8-12 hours vs 12-week greenfield rebuild
