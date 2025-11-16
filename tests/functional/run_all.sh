#!/bin/bash
# Master functional test runner for Shannon CLI
# Runs all functional tests and reports summary

set +e  # Don't exit on first error - we want to run all tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASSED=0
FAILED=0
TOTAL=0

echo "═══════════════════════════════════════════════════════"
echo "Shannon CLI Functional Test Suite"
echo "═══════════════════════════════════════════════════════"
echo ""

# Function to run a test script
run_test() {
    local test_script="$1"
    local test_name=$(basename "$test_script" .sh)

    TOTAL=$((TOTAL + 1))

    echo "Running: $test_name"
    echo "───────────────────────────────────────────────────────"

    if bash "$test_script"; then
        PASSED=$((PASSED + 1))
        echo "✅ $test_name PASSED"
    else
        FAILED=$((FAILED + 1))
        echo "❌ $test_name FAILED"
    fi

    echo ""
}

# Run all test scripts
for test_script in "$SCRIPT_DIR"/test_*.sh; do
    if [ -f "$test_script" ] && [ -x "$test_script" ]; then
        run_test "$test_script"
    fi
done

# Summary
echo "═══════════════════════════════════════════════════════"
echo "Test Summary"
echo "═══════════════════════════════════════════════════════"
echo "Total:  $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "✅ ALL TESTS PASSED"
    echo ""
    exit 0
else
    echo ""
    echo "❌ SOME TESTS FAILED"
    echo ""
    exit 1
fi
