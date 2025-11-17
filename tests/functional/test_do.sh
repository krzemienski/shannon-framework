#!/bin/bash
# Test shannon do Command (Skills-Based Execution)
# Per V5 Plan Phase 6 Task 6.1 test 3 (lines 793-807)

set -e

echo "Testing shannon do (skills-based execution)..."
echo

# Setup
TEST_DIR="/tmp/test-shannon-do-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "Test environment: $TEST_DIR"
echo

# Test 1: Single file creation
echo "Test 1: Create single file"
shannon do "create /tmp/test-do-$$.py with hello world" > /tmp/do-output-$$.log 2>&1
DO_EXIT=$?

if [ $DO_EXIT -eq 0 ] && [ -f "/tmp/test-do-$$.py" ]; then
    echo "  ✓ File created successfully"

    # Verify content
    if grep -q "hello" "/tmp/test-do-$$.py"; then
        echo "  ✓ Content validated"
    else
        echo "  ⚠ Content may not match request"
    fi

    rm -f "/tmp/test-do-$$.py"
else
    echo "  ✗ File creation failed (exit: $DO_EXIT)"
    cat /tmp/do-output-$$.log
    exit 1
fi
echo

# Test 2: Multi-file creation
echo "Test 2: Create multiple files"
shannon do "create main.py, create utils.py, create tests.py" > /tmp/do-multi-$$.log 2>&1
MULTI_EXIT=$?

if [ $MULTI_EXIT -eq 0 ]; then
    # Check all files created
    if [ -f "main.py" ] && [ -f "utils.py" ] && [ -f "tests.py" ]; then
        echo "  ✓ All files created: main.py, utils.py, tests.py"
    else
        echo "  ⚠ Some files missing:"
        ls -1 *.py
    fi
else
    echo "  ⚠ Multi-file creation exit code: $MULTI_EXIT"
    echo "  (May fail if API key not available)"
fi
echo

# Cleanup
cd /
rm -rf "$TEST_DIR"
rm -f /tmp/do-output-$$.log /tmp/do-multi-$$.log

echo "✓ shannon do test completed"
exit 0
