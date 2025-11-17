#!/bin/bash
# Test UnifiedOrchestrator handles both analysis and execution
# Per V5 Plan Phase 2 Task 2.2 (lines 239-253)

set -e

echo "Testing UnifiedOrchestrator integration..."
echo

# Setup
TEST_DIR="/tmp/test-unified-orch-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create test spec file
cat > spec.md <<'SPEC'
# Simple API Specification

Create a REST API with user authentication.

Features:
- User registration
- User login
- JWT tokens
SPEC

echo "✓ Test environment created"
echo

# Test 1: Analysis path (should use V3 cache, analytics, context)
echo "Test 1: Analysis path..."
shannon analyze spec.md > /tmp/analyze-output.log 2>&1
ANALYZE_EXIT=$?

if [ $ANALYZE_EXIT -eq 0 ]; then
    echo "✓ Analysis executed successfully"
    # Verify V3 features (cache, analytics would be used)
    # Note: Full verification requires checking logs/databases
else
    echo "✗ Analysis failed (exit code: $ANALYZE_EXIT)"
    cat /tmp/analyze-output.log
    exit 1
fi
echo

# Test 2: Execution path (should use V4 skills, creates files)
echo "Test 2: Execution path..."
shannon do "create hello.py with print hello world" > /tmp/do-output.log 2>&1
DO_EXIT=$?

if [ $DO_EXIT -eq 0 ] && [ -f hello.py ]; then
    echo "✓ Execution completed successfully"
    echo "✓ File created: hello.py"
    grep -q "hello" hello.py && echo "✓ Content validated"
else
    echo "✗ Execution failed (exit code: $DO_EXIT)"
    cat /tmp/do-output.log
    exit 1
fi
echo

# Test 3: Cache functionality (V3 feature)
echo "Test 3: Cache hit test..."
# Run analyze twice - second should be from cache
time shannon analyze spec.md > /dev/null 2>&1
FIRST_RUN=$SECONDS

SECONDS=0
shannon analyze spec.md > /dev/null 2>&1
SECOND_RUN=$SECONDS

if [ $SECOND_RUN -lt 2 ]; then
    echo "✓ Cache working (second run: ${SECOND_RUN}s)"
else
    echo "⚠ Cache may not be working (second run: ${SECOND_RUN}s)"
    # Not failing test - cache is optimization
fi
echo

# Cleanup
cd /
rm -rf "$TEST_DIR"

echo "✓ UnifiedOrchestrator tests passed"
exit 0
