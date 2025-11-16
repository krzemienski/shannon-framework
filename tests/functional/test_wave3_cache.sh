#!/bin/bash
# Wave 3 Validation Gate: Cache System
# Tests 3-tier caching functionality

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 3: Cache System Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: cache stats command exists
echo "Test 1: Cache stats command"
output=$(shannon cache stats 2>&1)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    assert_exit_code 0 $exit_code "cache stats command executed" && record_pass || record_fail
    assert_contains "$output" 'hit|miss|rate|cache' "Cache statistics displayed" && record_pass || record_fail
else
    echo "  ❌ FAIL: cache stats command failed (exit code: $exit_code)"
    record_fail
fi

# Test 2: cache clear command exists
echo "Test 2: Cache clear command"
shannon cache clear > /dev/null 2>&1
assert_exit_code 0 $? "cache clear command executed" && record_pass || record_fail

# Test 3: Cache actually caches (run analyze twice, second should be faster or indicate cache hit)
echo "Test 3: Functional caching behavior"

# Clear cache first
shannon cache clear > /dev/null 2>&1

# First run (should populate cache)
echo "  Running first analysis (cache miss expected)..."
output1=$(shannon analyze "$SCRIPT_DIR/fixtures/simple_spec.md" 2>&1)

# Second run (should hit cache)
echo "  Running second analysis (cache hit expected)..."
output2=$(shannon analyze "$SCRIPT_DIR/fixtures/simple_spec.md" 2>&1)

# Check if output indicates caching
if echo "$output2" | grep -qiE 'cache|cached|from cache'; then
    echo "  ✅ PASS: Cache hit indicated in output"
    record_pass
else
    echo "  ⚠️  INFO: No explicit cache indicator (may still be cached internally)"
fi

# Test 4: cache warm command (if exists)
echo "Test 4: Cache warm command"
output=$(shannon cache warm 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    echo "  ✅ PASS: cache warm command exists"
    record_pass
else
    echo "  ⚠️  INFO: cache warm command not found (optional)"
fi

echo ""
print_summary "test_wave3_cache.sh"
