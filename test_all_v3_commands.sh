#!/bin/bash
# Comprehensive V3 command testing
# Tests all V3 commands to verify functionality

set +e  # Don't exit on errors - collect all results

echo "================================================================================"
echo "Shannon CLI V3 - Comprehensive Command Testing"
echo "================================================================================"
echo ""

PASS=0
FAIL=0

test_command() {
    local name="$1"
    local cmd="$2"
    local expected="$3"

    echo "Test: $name"
    echo "  Command: $cmd"

    output=$(eval "$cmd" 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ] && echo "$output" | grep -q "$expected"; then
        echo "  ✅ PASS"
        PASS=$((PASS + 1))
    else
        echo "  ❌ FAIL (exit: $exit_code)"
        echo "  Output: ${output:0:200}"
        FAIL=$((FAIL + 1))
    fi
    echo ""
}

# V3 Commands Testing
echo "=== Cache Commands ==="
test_command "cache stats" "shannon cache stats" "Cache Statistics"
test_command "cache clear" "shannon cache clear" "Cache cleared"
test_command "cache warm" "shannon cache warm test.md" "Cache warmed"

echo "=== Budget Commands ==="
test_command "budget set" "shannon budget set 50.00" "Budget set"
test_command "budget status" "shannon budget status" "Budget Status"

echo "=== Analytics & Optimization ==="
test_command "analytics" "shannon analytics" "Historical Analytics"
test_command "optimize" "shannon optimize" "Optimization Suggestions"

echo "=== Context Commands ==="
test_command "onboard" "shannon onboard . --force" "Onboarding"
test_command "context status" "shannon context status" "Context Status"

echo "=== Wave Control ==="
test_command "wave-agents" "shannon wave-agents" "agents"

echo "=== MCP ==="
test_command "mcp-install" "shannon mcp-install test 2>&1 | grep -i install" "Installing"

echo "================================================================================"
echo "Test Summary"
echo "================================================================================"
echo "PASSED: $PASS"
echo "FAILED: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✅ ALL TESTS PASSED"
    exit 0
else
    echo "⚠️  Some tests failed - review above"
    exit 1
fi
