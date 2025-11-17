#!/bin/bash
# Shannon V3 - Master Functional Test Suite
# Runs all V3 feature tests (NO pytest - Shannon mandate)

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Shannon V3 - Complete Functional Test Suite              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test tracking
PASSED=0
FAILED=0
SKIPPED=0

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_test() {
    local test_name="$1"
    local test_script="$2"

    echo "Running: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [ ! -f "$test_script" ]; then
        echo "⚠ SKIP: $test_script not found"
        SKIPPED=$((SKIPPED + 1))
        return
    fi

    if bash "$test_script"; then
        echo "✓ PASSED: $test_name"
        PASSED=$((PASSED + 1))
    else
        echo "✗ FAILED: $test_name"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# Run tests
run_test "Cache System" "$SCRIPT_DIR/test_cache.sh"
run_test "Cost Optimization" "$SCRIPT_DIR/test_cost.sh"
run_test "Analytics" "$SCRIPT_DIR/test_analytics.sh"
run_test "Full Integration" "$SCRIPT_DIR/test_integration.sh"

# Summary
TOTAL=$((PASSED + FAILED + SKIPPED))
echo "═══════════════════════════════════════════════════════════"
echo "Results: $PASSED passed, $FAILED failed, $SKIPPED skipped"
[ "$FAILED" -eq 0 ] && echo "✓ ALL TESTS PASSED" && exit 0
echo "✗ FAILURES DETECTED" && exit 1
