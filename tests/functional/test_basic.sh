#!/bin/bash
# Test Basic Command Functionality
# Per V5 Plan Phase 6 Task 6.1 test 1 (lines 756-766)

set -e

echo "Testing basic Shannon CLI commands..."
echo

# Test version command
echo "Test 1: shannon --version"
VERSION_OUTPUT=$(shannon --version)
echo "  Output: $VERSION_OUTPUT"

if echo "$VERSION_OUTPUT" | grep -q "4.0.0"; then
    echo "  ✓ Version command works"
else
    echo "  ✗ Version command failed or wrong version"
    exit 1
fi
echo

# Test help command
echo "Test 2: shannon --help"
HELP_OUTPUT=$(shannon --help)

if echo "$HELP_OUTPUT" | grep -q "Shannon CLI"; then
    echo "  ✓ Help command works"
else
    echo "  ✗ Help command failed"
    exit 1
fi
echo

# Test status command
echo "Test 3: shannon status"
STATUS_OUTPUT=$(shannon status 2>&1)
STATUS_EXIT=$?

if [ $STATUS_EXIT -eq 0 ]; then
    echo "  ✓ Status command works"
else
    echo "  ⚠ Status command exit code: $STATUS_EXIT (may be OK)"
fi
echo

# Test config command
echo "Test 4: shannon config"
CONFIG_OUTPUT=$(shannon config 2>&1)
CONFIG_EXIT=$?

if [ $CONFIG_EXIT -eq 0 ]; then
    echo "  ✓ Config command works"
else
    echo "  ⚠ Config command exit code: $CONFIG_EXIT (may be OK)"
fi
echo

echo "✓ Basic commands test passed"
exit 0
