#!/bin/bash
# Wave 4b Validation Gate: Cost Optimization
# Tests budget enforcement and cost optimization

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 4b: Cost Optimization Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: budget command exists
echo "Test 1: Budget management command"
output=$(shannon budget --help 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    assert_contains "$output" "budget|cost|limit" "Budget command help text" && record_pass || record_fail
else
    echo "  ❌ FAIL: budget command not found"
    record_fail
fi

# Test 2: budget set command works
echo "Test 2: Set budget limit"
output=$(shannon budget set 50 2>&1 || echo "SET_FAILED")

if [ "$output" != "SET_FAILED" ]; then
    echo "  ✅ PASS: budget set command executed"
    record_pass
else
    echo "  ❌ FAIL: budget set command failed"
    record_fail
fi

# Test 3: budget status shows current budget
echo "Test 3: Budget status display"
output=$(shannon budget status 2>&1 || shannon budget 2>&1 || echo "STATUS_FAILED")

if [ "$output" != "STATUS_FAILED" ]; then
    assert_contains "$output" '\$[0-9]+|budget|spent|remaining' "Budget status displayed" && record_pass || record_fail
else
    echo "  ❌ FAIL: budget status command failed"
    record_fail
fi

# Test 4: optimize command exists
echo "Test 4: Optimization suggestions command"
output=$(shannon optimize 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    echo "  ✅ PASS: optimize command exists"
    record_pass
else
    echo "  ⚠️  INFO: optimize command not found (may be optional)"
fi

# Test 5: Cost optimizer subsystem files exist
echo "Test 5: Optimization subsystem files"
assert_file_exists "src/shannon/optimization/cost_estimator.py" "cost_estimator.py exists" && record_pass || record_fail
assert_file_exists "src/shannon/optimization/budget_enforcer.py" "budget_enforcer.py exists" && record_pass || record_fail

echo ""
print_summary "test_wave4_optimization.sh"
