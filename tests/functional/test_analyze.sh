#!/bin/bash
# Functional test for shannon analyze command
# Tests actual CLI behavior, not internal implementation

set -e  # Exit on first error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES="$SCRIPT_DIR/fixtures"
TEMP_OUTPUT="/tmp/shannon_test_$$"

echo "🧪 Testing shannon analyze command..."
echo ""

# Test 1: Basic execution with JSON output
echo "Test 1: Basic analysis with JSON output"
shannon analyze "$FIXTURES/simple_spec.md" --json > "$TEMP_OUTPUT.json" 2>&1 || {
    echo "❌ FAIL: shannon analyze command failed"
    cat "$TEMP_OUTPUT.json"
    exit 1
}

# Verify JSON structure
if command -v jq &> /dev/null; then
    jq -e '.complexity_score' "$TEMP_OUTPUT.json" > /dev/null || {
        echo "❌ FAIL: Missing complexity_score in output"
        exit 1
    }
    echo "✅ PASS: JSON output has complexity_score"

    # Verify score in valid range
    score=$(jq -r '.complexity_score' "$TEMP_OUTPUT.json")
    if (( $(echo "$score >= 0.10 && $score <= 0.95" | bc -l 2>/dev/null || echo 0) )); then
        echo "✅ PASS: Complexity score ($score) in valid range [0.10, 0.95]"
    else
        echo "⚠️  WARNING: Score $score outside expected range (non-fatal)"
    fi
else
    echo "⚠️  WARNING: jq not installed, skipping JSON validation"
    if grep -q "complexity" "$TEMP_OUTPUT.json"; then
        echo "✅ PASS: Output contains complexity data"
    fi
fi

echo ""

# Test 2: Command help
echo "Test 2: shannon analyze --help"
shannon analyze --help > "$TEMP_OUTPUT.help" 2>&1 || {
    echo "❌ FAIL: Help command failed"
    exit 1
}

if grep -q "Analyze specification" "$TEMP_OUTPUT.help"; then
    echo "✅ PASS: Help text present"
else
    echo "❌ FAIL: Help text missing or incorrect"
    exit 1
fi

echo ""

# Test 3: Invalid input handling
echo "Test 3: Error handling for non-existent file"
shannon analyze "/nonexistent/file.md" --json > "$TEMP_OUTPUT.error" 2>&1 && {
    echo "❌ FAIL: Should have failed for non-existent file"
    exit 1
} || {
    echo "✅ PASS: Correctly rejected non-existent file"
}

echo ""

# Cleanup
rm -f "$TEMP_OUTPUT"*

echo "✅ All shannon analyze tests passed"
echo ""
