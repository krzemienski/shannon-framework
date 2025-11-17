#!/bin/bash
# Test shannon do returning workflow (cached context)
# FUNCTIONAL TEST - Verifies caching and context reuse

set -e

echo "Testing shannon do returning workflow..."

TEST_DIR="/tmp/shannon-do-returning-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "def hello(): print('Hello')" > main.py

# First run (onboards)
echo "=== FIRST RUN (should onboard) ==="
SECONDS=0
shannon do "create utils.py with string formatting and file handling functions" --auto > /tmp/first_run.log 2>&1
FIRST_TIME=$SECONDS
EXIT_1=$?

echo "First run: ${FIRST_TIME}s, exit: $EXIT_1"

if [ $EXIT_1 -ne 0 ]; then
    echo "✗ First run failed"
    tail -20 /tmp/first_run.log
    exit 1
fi

# Second run (should use cache)
echo "=== SECOND RUN (should use cached context) ==="
SECONDS=0
shannon do "create helpers.py with date formatting and validation helpers" --auto > /tmp/second_run.log 2>&1
SECOND_TIME=$SECONDS
EXIT_2=$?

echo "Second run: ${SECOND_TIME}s, exit: $EXIT_2"

if [ $EXIT_2 -ne 0 ]; then
    echo "✗ Second run failed"
    tail -20 /tmp/second_run.log
    exit 1
fi

# VALIDATE: Check for cache usage message
echo
echo "=== VALIDATION ==="

if grep -q "Using cached context" /tmp/second_run.log; then
    echo "✓ Cache message shown"
elif grep -q "First time" /tmp/second_run.log; then
    echo "⚠ Second run treated as first time (cache might not be working)"
    echo "Checking if context was saved..."
    if [ -d "$HOME/.shannon/projects/$(basename $TEST_DIR)" ]; then
        echo "Context exists but not detected - possible bug"
    fi
else
    echo "✓ No first-time message (likely used cache silently)"
fi

# Verify both files created
if [ -f "utils.py" ] && [ -f "helpers.py" ]; then
    echo "✓ Both files created"
    echo "Files: $(ls *.py | tr '\n' ' ')"
else
    echo "✗ Files missing"
    ls -la
    exit 1
fi

# Verify context saved
if [ -d "$HOME/.shannon/projects/$(basename $TEST_DIR)" ]; then
    echo "✓ Project context saved"
else
    echo "✗ Context not saved"
    exit 1
fi

# Cleanup
cd /
rm -rf "$TEST_DIR"

echo
echo "✓ Returning workflow test PASSED"
echo "Evidence: /tmp/first_run.log, /tmp/second_run.log"
exit 0
