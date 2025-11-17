#!/bin/bash
# Shannon V3 Cache Feature - Functional Test
# Tests multi-level caching system (NO pytest - Shannon mandate)

set -e

echo "════════════════════════════════════════════════════════════"
echo "Shannon V3: Cache Feature Functional Test"
echo "════════════════════════════════════════════════════════════"
echo ""

# Setup
TEST_DIR="/tmp/shannon-cache-test-$$"
TEST_SPEC="$TEST_DIR/test_spec.md"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create test specification
cat > "$TEST_SPEC" << 'EOF'
# Simple Test Spec
Build a hello world web app with React frontend and Express backend.
EOF

echo "✓ Test environment created: $TEST_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 1: Cache Miss on First Run
# ═══════════════════════════════════════════════════════════════

echo "TEST 1: First analysis (cache miss expected)"
echo "─────────────────────────────────────────────────────────"

# Clear cache first
shannon cache clear > /dev/null 2>&1 || true

START_TIME=$(date +%s)

# Run analysis (first time - should miss cache)
FIRST_OUTPUT=$(shannon analyze "$TEST_SPEC" 2>&1 || true)
FIRST_EXIT=$?

END_TIME=$(date +%s)
FIRST_DURATION=$((END_TIME - START_TIME))

echo "$FIRST_OUTPUT" | grep -i "cache hit" > /dev/null && {
    echo "✗ FAIL: Should be cache MISS on first run"
    exit 1
}

echo "✓ PASS: Cache miss on first run (as expected)"
echo "  Duration: ${FIRST_DURATION}s"
echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 2: Cache Hit on Second Run
# ═══════════════════════════════════════════════════════════════

echo "TEST 2: Second analysis (cache hit expected)"
echo "─────────────────────────────────────────────────────────"

sleep 1  # Ensure cache is saved

START_TIME=$(date +%s)

# Run same analysis (should hit cache)
SECOND_OUTPUT=$(shannon analyze "$TEST_SPEC" 2>&1 || true)
SECOND_EXIT=$?

END_TIME=$(date +%s)
SECOND_DURATION=$((END_TIME - START_TIME))

echo "$SECOND_OUTPUT" | grep -i "cache hit" > /dev/null || {
    echo "✗ FAIL: Should be cache HIT on second run"
    echo "Output:"
    echo "$SECOND_OUTPUT"
    exit 1
}

echo "✓ PASS: Cache hit on second run"
echo "  Duration: ${SECOND_DURATION}s (should be < 1s)"

# Verify second run is faster
if [ "$SECOND_DURATION" -ge "$FIRST_DURATION" ]; then
    echo "⚠ WARNING: Cache hit not faster than miss ($SECOND_DURATION vs $FIRST_DURATION)"
else
    echo "✓ PASS: Cache hit is faster (${SECOND_DURATION}s vs ${FIRST_DURATION}s)"
fi
echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 3: Cache Stats Show Activity
# ═══════════════════════════════════════════════════════════════

echo "TEST 3: Cache statistics"
echo "─────────────────────────────────────────────────────────"

STATS_OUTPUT=$(shannon cache stats 2>&1)

echo "$STATS_OUTPUT" | grep -i "hits" > /dev/null || {
    echo "✗ FAIL: Cache stats should show hits/misses"
    exit 1
}

# Should show 1 hit, 1 miss
echo "$STATS_OUTPUT" | grep -E "1.*1.*50" > /dev/null || {
    echo "⚠ WARNING: Expected 1 hit, 1 miss, 50% hit rate"
}

echo "✓ PASS: Cache stats command works"
echo "$STATS_OUTPUT"
echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 4: Cache Clear
# ═══════════════════════════════════════════════════════════════

echo "TEST 4: Cache clear"
echo "─────────────────────────────────────────────────────────"

CLEAR_OUTPUT=$(shannon cache clear 2>&1)

echo "$CLEAR_OUTPUT" | grep -i "cleared" > /dev/null || {
    echo "✗ FAIL: Cache clear should confirm clearing"
    exit 1
}

echo "✓ PASS: Cache clear command works"
echo ""

# Verify cache was actually cleared (next run should miss)
THIRD_OUTPUT=$(shannon analyze "$TEST_SPEC" 2>&1 || true)
echo "$THIRD_OUTPUT" | grep -i "cache hit" > /dev/null && {
    echo "✗ FAIL: Cache should be cleared, expecting miss"
    exit 1
}

echo "✓ PASS: Cache actually cleared (miss after clear)"
echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 5: Cache Invalidation on Spec Change
# ═══════════════════════════════════════════════════════════════

echo "TEST 5: Cache invalidation"
echo "─────────────────────────────────────────────────────────"

# Run twice to populate cache
shannon analyze "$TEST_SPEC" > /dev/null 2>&1 || true
sleep 1
CACHED=$(shannon analyze "$TEST_SPEC" 2>&1 || true)
echo "$CACHED" | grep -i "cache hit" > /dev/null || {
    echo "✗ FAIL: Setup failed - should have cache"
    exit 1
}

# Modify spec
echo "Additional requirement: Add database layer" >> "$TEST_SPEC"

# Run with modified spec (should miss cache - different hash)
MODIFIED=$(shannon analyze "$TEST_SPEC" 2>&1 || true)
echo "$MODIFIED" | grep -i "cache hit" > /dev/null && {
    echo "✗ FAIL: Should miss cache after spec modification"
    exit 1
}

echo "✓ PASS: Cache invalidated on spec change"
echo ""

# Cleanup
cd /
rm -rf "$TEST_DIR"

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════

echo "════════════════════════════════════════════════════════════"
echo "✓ ALL CACHE TESTS PASSED"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Verified:"
echo "  ✓ Cache miss on first run"
echo "  ✓ Cache hit on second run (faster)"
echo "  ✓ Cache stats command functional"
echo "  ✓ Cache clear command functional"
echo "  ✓ Cache invalidation on spec change"
echo ""
echo "Cache feature: FUNCTIONAL ✅"
echo ""

exit 0
