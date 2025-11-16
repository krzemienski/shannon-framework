#!/bin/bash
# Wave 1 Validation Gate: Metrics & Dashboard
# Tests operational telemetry and LiveDashboard functionality

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 1: Metrics & Dashboard Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: Dashboard appears during execution
echo "Test 1: Dashboard rendering"
output=$(shannon analyze "$SCRIPT_DIR/fixtures/simple_spec.md" 2>&1)
exit_code=$?

assert_exit_code 0 $exit_code "Command execution successful" && record_pass || record_fail

# Test 2: Dashboard header present
assert_contains "$output" "Shannon:" "Dashboard header displayed" && record_pass || record_fail

# Test 3: Command name shown
assert_contains "$output" "analyze" "Command name shown in dashboard" && record_pass || record_fail

# Test 4: Cost metric displayed
assert_contains "$output" '\$[0-9]+\.[0-9]+' "Cost displayed (\$X.XX format)" && record_pass || record_fail

# Test 5: Token count displayed
assert_contains "$output" '[0-9]+\.?[0-9]*K? tokens?|[0-9]+ tokens?' "Token count shown" && record_pass || record_fail

# Test 6: Duration displayed
assert_contains "$output" '[0-9]+s|[0-9]+m [0-9]+s' "Duration shown" && record_pass || record_fail

# Test 7: Progress indicator
assert_contains "$output" '[0-9]+%|▓|░' "Progress indicator present" && record_pass || record_fail

# Test 8: State indicator
assert_contains "$output" 'ACTIVE|COMPLETE|WAITING|RUNNING' "Operational state shown" && record_pass || record_fail

# Test 9: Interactive controls hint (if applicable)
if echo "$output" | grep -qE 'Press|↵|Enter|ESC'; then
    echo "  ✅ PASS: Interactive controls hint present"
    record_pass
else
    echo "  ⚠️  INFO: No interactive controls hint (may not be applicable)"
fi

echo ""
print_summary "test_wave1_dashboard.sh"
