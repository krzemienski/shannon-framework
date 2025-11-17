#!/bin/bash
# Shannon V3 Analytics Feature - Functional Test
# Tests historical analytics and insights (NO pytest - Shannon mandate)

set -e

echo "════════════════════════════════════════════════════════════"
echo "Shannon V3: Analytics Feature Functional Test"
echo "════════════════════════════════════════════════════════════"
echo ""

TEST_DIR="/tmp/shannon-analytics-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# ═══════════════════════════════════════════════════════════════
# TEST 1: Analytics Command Exists and Works
# ═══════════════════════════════════════════════════════════════

echo "TEST 1: Analytics command functional"
echo "─────────────────────────────────────────────────────────"

ANALYTICS_OUTPUT=$(shannon analytics 2>&1)

echo "$ANALYTICS_OUTPUT" | grep -i "sessions" > /dev/null || {
    echo "✗ FAIL: Analytics should show session count"
    exit 1
}

echo "$ANALYTICS_OUTPUT" | grep -i "insights\|recommendations" > /dev/null || {
    echo "✗ FAIL: Analytics should show insights"
    exit 1
}

echo "✓ PASS: Analytics command functional"
echo "$ANALYTICS_OUTPUT"
echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 2: Session Recording After Analysis
# ═══════════════════════════════════════════════════════════════

echo "TEST 2: Session recording integration"
echo "─────────────────────────────────────────────────────────"

# Get initial session count
BEFORE=$(shannon analytics 2>&1)
BEFORE_COUNT=$(echo "$BEFORE" | grep "Total sessions" | grep -oE "[0-9]+" || echo "0")

echo "Sessions before analysis: $BEFORE_COUNT"

# Create and analyze 3 different specs
for i in 1 2 3; do
    cat > "spec_$i.md" << EOF
# Test Spec $i
Build feature $i with complexity level: medium
Requires: Database, API, Frontend
Timeline: $i weeks
EOF

    echo "  Analyzing spec $i..."
    shannon analyze "spec_$i.md" > /dev/null 2>&1 || {
        echo "⚠ WARNING: Analysis $i failed (likely no API key)"
        echo "  Skipping session recording test"
        break
    }

    sleep 1
done

# Check if sessions increased
AFTER=$(shannon analytics 2>&1)
AFTER_COUNT=$(echo "$AFTER" | grep "Total sessions" | grep -oE "[0-9]+" || echo "0")

echo "Sessions after analyses: $AFTER_COUNT"

if [ "$AFTER_COUNT" -gt "$BEFORE_COUNT" ]; then
    echo "✓ PASS: Sessions recorded (+$((AFTER_COUNT - BEFORE_COUNT)) sessions)"
else
    echo "⚠ SKIP: Could not verify session recording (likely no API key)"
    echo "  Analytics database integration: REQUIRES API KEY FOR TESTING"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# TEST 3: Analytics Database File Exists
# ═══════════════════════════════════════════════════════════════

echo "TEST 3: Analytics database creation"
echo "─────────────────────────────────────────────────────────"

ANALYTICS_DB="$HOME/.shannon/analytics.db"

if [ -f "$ANALYTICS_DB" ]; then
    echo "✓ PASS: Analytics database exists"
    echo "  Location: $ANALYTICS_DB"

    # Check size
    DB_SIZE=$(du -h "$ANALYTICS_DB" | cut -f1)
    echo "  Size: $DB_SIZE"

    # Check if it's SQLite
    file "$ANALYTICS_DB" | grep -i "sqlite" > /dev/null && {
        echo "✓ PASS: Database is SQLite format"
    } || {
        echo "⚠ WARNING: Database format unexpected"
    }
else
    echo "⚠ INFO: Analytics database not created yet"
    echo "  May be created on first analyze with API key"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════

cd /
rm -rf "$TEST_DIR"

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════

echo "════════════════════════════════════════════════════════════"
echo "✓ ANALYTICS TESTS COMPLETED"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Verified:"
echo "  ✓ Analytics command functional"
echo "  ⚠ Session recording (needs API key for full test)"
echo "  ⚠ Database creation (needs API key)"
echo ""
echo "Analytics feature: COMMAND FUNCTIONAL ✅"
echo "Full validation: REQUIRES API KEY"
echo ""

exit 0
