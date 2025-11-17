#!/bin/bash
# Shannon V5 - Master Functional Test Suite
# Runs all functional tests (NO pytest - Shannon mandate)
# Per V5 Plan Phase 6 Task 6.2 (lines 876-900)

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Shannon V5 - Complete Functional Test Suite              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check for API key (required for most tests)
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠ WARNING: ANTHROPIC_API_KEY not set"
    echo "  Many tests require API key and will be skipped"
    echo ""
fi

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

    if bash "$test_script" 2>&1; then
        echo "✓ PASSED: $test_name"
        PASSED=$((PASSED + 1))
    else
        EXIT_CODE=$?
        echo "✗ FAILED: $test_name (exit code: $EXIT_CODE)"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# Core V5 Tests
echo "━━━ Core V5 Tests ━━━"
run_test "Basic Commands" "$SCRIPT_DIR/test_basic.sh"
run_test "UnifiedOrchestrator" "$SCRIPT_DIR/test_unified_orchestrator.sh"
run_test "Context Integration" "$SCRIPT_DIR/test_context.sh"
echo

# Command Tests (require API key)
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "━━━ Command Tests (with API) ━━━"
    run_test "Analyze Command" "$SCRIPT_DIR/test_analyze.sh"
    run_test "Do Command" "$SCRIPT_DIR/test_do.sh"
    run_test "Exec Command" "$SCRIPT_DIR/test_exec.sh"
    echo
else
    echo "━━━ Command Tests (SKIPPED - no API key) ━━━"
    SKIPPED=$((SKIPPED + 3))
    echo "  ⚠ Skipped: test_analyze.sh (needs ANTHROPIC_API_KEY)"
    echo "  ⚠ Skipped: test_do.sh (needs ANTHROPIC_API_KEY)"
    echo "  ⚠ Skipped: test_exec.sh (needs ANTHROPIC_API_KEY)"
    echo
fi

# V3 Feature Tests
echo "━━━ V3 Feature Tests ━━━"
run_test "Cache System" "$SCRIPT_DIR/test_cache.sh"
run_test "Cost Optimization" "$SCRIPT_DIR/test_cost.sh"
run_test "Analytics" "$SCRIPT_DIR/test_analytics.sh"
run_test "MCP Integration" "$SCRIPT_DIR/test_mcp.sh"
echo

# Dashboard Tests (require API key + services)
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "━━━ Dashboard Tests (manual - require services) ━━━"
    echo "  ⚠ Skipped: test_dashboard_events.sh (requires server + dashboard)"
    echo "  ⚠ Skipped: test_multiagent_dashboard.sh (requires server + dashboard)"
    echo "  Run these manually with services started"
    SKIPPED=$((SKIPPED + 2))
    echo
else
    SKIPPED=$((SKIPPED + 2))
fi

# Integration Test
echo "━━━ Integration Tests ━━━"
run_test "Full Integration" "$SCRIPT_DIR/test_integration.sh"
echo

# Summary
TOTAL=$((PASSED + FAILED + SKIPPED))
echo "═══════════════════════════════════════════════════════════"
echo "Results: $PASSED passed, $FAILED failed, $SKIPPED skipped (total: $TOTAL)"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "✓ ALL TESTS PASSED"
    exit 0
else
    echo "✗ FAILURES DETECTED"
    exit 1
fi

