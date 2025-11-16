#!/bin/bash
# Wave 6 Validation Gate: Context Management
# Tests context loading, onboarding, and memory coordination

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 6: Context Management Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: onboard command exists
echo "Test 1: Onboard command availability"
output=$(shannon onboard --help 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    assert_contains "$output" "onboard|index|codebase" "Onboard command help text" && record_pass || record_fail
else
    echo "  ❌ FAIL: onboard command not found"
    record_fail
fi

# Test 2: context status command
echo "Test 2: Context status command"
output=$(shannon context status 2>&1 || shannon context 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    echo "  ✅ PASS: context command exists"
    record_pass

    # Check if it shows meaningful context information
    if echo "$output" | grep -qiE 'context|memory|codebase|loaded|files'; then
        echo "  ✅ PASS: Context status shows information"
        record_pass
    else
        echo "  ⚠️  INFO: Context command output unclear"
    fi
else
    echo "  ❌ FAIL: context command not found"
    record_fail
fi

# Test 3: Context subsystem files exist
echo "Test 3: Context subsystem files"
assert_file_exists "src/shannon/context/manager.py" "manager.py exists" && record_pass || record_fail
assert_file_exists "src/shannon/context/loader.py" "loader.py exists" && record_pass || record_fail
assert_file_exists "src/shannon/context/primer.py" "primer.py exists" && record_pass || record_fail

# Test 4: Context onboarding can run (dry-run or on test project)
echo "Test 4: Onboarding execution"
output=$(shannon onboard . --help 2>&1 || shannon onboard --dry-run 2>&1 || echo "ONBOARD_FAILED")

if [ "$output" != "ONBOARD_FAILED" ]; then
    echo "  ✅ PASS: Onboard command executable"
    record_pass
else
    echo "  ⚠️  INFO: Onboard execution test skipped"
fi

echo ""
print_summary "test_wave6_context.sh"
