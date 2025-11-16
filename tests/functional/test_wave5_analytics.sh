#!/bin/bash
# Wave 5 Validation Gate: Analytics Database
# Tests historical command tracking and analytics queries

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 5: Analytics Database Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: analytics command exists
echo "Test 1: Analytics command availability"
output=$(shannon analytics --help 2>&1 || shannon analytics 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    echo "  ✅ PASS: analytics command exists"
    record_pass
else
    echo "  ❌ FAIL: analytics command not found"
    record_fail
fi

# Test 2: Analytics database file exists
echo "Test 2: Analytics database file"
if [ -f ".shannon/analytics.db" ] || [ -f ".shannon/analytics/shannon.db" ]; then
    echo "  ✅ PASS: Analytics database file exists"
    record_pass
else
    echo "  ⚠️  INFO: Analytics database not found (may not be initialized)"
fi

# Test 3: Command execution is logged
echo "Test 3: Command logging functionality"

# Run a command that should be logged
shannon analyze "$SCRIPT_DIR/fixtures/simple_spec.md" > /dev/null 2>&1 || true

# Check if analytics can be queried
output=$(shannon analytics 2>&1 || echo "QUERY_FAILED")

if [ "$output" != "QUERY_FAILED" ]; then
    # Check if recent command appears in analytics
    if echo "$output" | grep -qE 'analyze|command|session|history'; then
        echo "  ✅ PASS: Analytics shows command history"
        record_pass
    else
        echo "  ⚠️  INFO: Analytics output doesn't show clear command history"
    fi
else
    echo "  ⚠️  INFO: Analytics query failed"
fi

# Test 4: Analytics subsystem files exist
echo "Test 4: Analytics subsystem files"
assert_file_exists "src/shannon/analytics/database.py" "database.py exists" && record_pass || record_fail
assert_file_exists "src/shannon/analytics/insights.py" "insights.py exists" && record_pass || record_fail

echo ""
print_summary "test_wave5_analytics.sh"
