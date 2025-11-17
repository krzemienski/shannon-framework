#!/bin/bash
# Test shannon do first-time workflow in new project
# FUNCTIONAL TEST - runs actual CLI command

set -e

echo "Testing shannon do first-time workflow..."

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY not set"
    exit 1
fi

# Create test project
TEST_DIR="/tmp/shannon-do-first-time-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create simple Python project
cat > main.py <<'EOF'
def hello():
    print("Hello")

if __name__ == '__main__':
    hello()
EOF

cat > requirements.txt <<'EOF'
requests==2.31.0
EOF

echo "✓ Test project created: $TEST_DIR"

# Run shannon do (should auto-explore on first time)
echo "Running shannon do --auto (this will take 1-3 minutes)..."
shannon do "create utils.py with helper functions" --auto > /tmp/shannon_do_first_time.log 2>&1

EXIT_CODE=$?

# VALIDATE
echo
echo "=== VALIDATION ==="

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Command executed successfully (exit: $EXIT_CODE)"
else
    echo "✗ Command failed (exit: $EXIT_CODE)"
    echo "Last 30 lines of log:"
    tail -30 /tmp/shannon_do_first_time.log
    exit 1
fi

# Verify context was saved
CONTEXT_DIR="$HOME/.shannon/projects/shannon-do-first-time-test-$$"
if [ -d "$CONTEXT_DIR" ]; then
    echo "✓ Context saved to ~/.shannon/projects/"
else
    echo "✗ Context not saved"
    echo "Expected: $CONTEXT_DIR"
    exit 1
fi

# Verify config saved
if [ -f "$CONTEXT_DIR/config.json" ]; then
    echo "✓ Config saved (validation gates)"
    echo "Config contents:"
    cat "$CONTEXT_DIR/config.json"
else
    echo "✗ Config not saved"
    exit 1
fi

# Verify file created
if [ -f "utils.py" ]; then
    echo "✓ File created: utils.py"
    echo "File contents:"
    head -10 utils.py
else
    echo "✗ File not created"
    ls -la
    exit 1
fi

# Cleanup
cd /
rm -rf "$TEST_DIR"

echo
echo "✓ First-time workflow test PASSED"
echo "Evidence: /tmp/shannon_do_first_time.log"
exit 0
