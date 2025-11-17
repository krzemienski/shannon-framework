#!/bin/bash
# Test shannon do with complex application (10-15 min execution)
# FUNCTIONAL TEST - Real API call, full execution, observable result

set -e

echo "Testing shannon do with complex application..."
echo "This will take 10-15 minutes - WILL NOT INTERRUPT"
echo ""

TEST_DIR="/tmp/shannon-complex-app-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create README for context
cat > README.md <<'EOF'
# Complex Test Project

Python/Flask project for testing Shannon do intelligence with complex requirements.
EOF

echo "✓ Test directory created: $TEST_DIR"
echo ""

# Record start time
START_TIME=$(date +%s)

echo "=== EXECUTING COMPLEX TASK ==="
echo "Task: Create Flask REST API with full features"
echo "Estimated: 10-15 minutes"
echo "Starting at: $(date)"
echo ""

# Run complex task
shannon do "create a Flask REST API with:
- User authentication using JWT tokens
- CRUD endpoints for blog posts at /api/posts
- SQLite database with User and Post models
- Input validation for all endpoints
- Error handling with proper HTTP status codes
- Unit tests for all endpoints using pytest
- README with API documentation and setup instructions
- requirements.txt with all dependencies" --auto --verbose 2>&1 | tee /tmp/complex_app_execution.log

EXIT_CODE=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "=== EXECUTION COMPLETE ==="
echo "Duration: ${DURATION} seconds ($((DURATION / 60)) minutes)"
echo "Exit code: $EXIT_CODE"
echo ""

# VALIDATION
echo "=== VALIDATING FILES CREATED ==="

REQUIRED_FILES=(
    "app.py"
    "models.py"
    "requirements.txt"
    "README.md"
)

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists ($(wc -l < $file) lines)"
    else
        echo "✗ $file missing"
        MISSING=$((MISSING + 1))
    fi
done

# Check for API endpoints
if ls *.py 1> /dev/null 2>&1; then
    if grep -q "/api/posts" *.py 2>/dev/null; then
        echo "✓ API endpoints present"
    else
        echo "⚠ API endpoints not clearly found"
    fi
else
    echo "✗ No Python files created"
    MISSING=$((MISSING + 1))
fi

# Test Python compilation
echo ""
echo "=== TESTING CODE QUALITY ==="
if python3 -m py_compile *.py 2>/dev/null; then
    echo "✓ All Python files compile"
else
    echo "✗ Python compilation errors"
    MISSING=$((MISSING + 1))
fi

# Test imports work
if python3 -c "import app" 2>/dev/null; then
    echo "✓ App imports successfully"
else
    echo "⚠ App import failed (might need dependencies)"
fi

# List all created files
echo ""
echo "=== FILES CREATED ==="
find . -name "*.py" -o -name "*.md" -o -name "*.txt" | sort

# Capture evidence
echo ""
echo "=== SAVING EVIDENCE ==="
EVIDENCE_DIR="/tmp/shannon-complex-app-evidence-$$"
cp -r "$TEST_DIR" "$EVIDENCE_DIR"
echo "Evidence saved: $EVIDENCE_DIR"

# File statistics
echo ""
echo "=== STATISTICS ==="
echo "Python files: $(find . -name '*.py' | wc -l)"
echo "Total files: $(find . -type f | wc -l)"
echo "Total lines: $(find . -name '*.py' -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "Execution time: ${DURATION}s"

# Final result
if [ $EXIT_CODE -eq 0 ] && [ $MISSING -eq 0 ]; then
    echo ""
    echo "✅ COMPLEX APPLICATION TEST PASSED"
    echo "Evidence: $EVIDENCE_DIR"
    echo "Logs: /tmp/complex_app_execution.log"
    cd /
    exit 0
else
    echo ""
    echo "✗ COMPLEX APPLICATION TEST FAILED"
    echo "Missing files: $MISSING"
    echo "Exit code: $EXIT_CODE"
    echo "Evidence: $EVIDENCE_DIR"
    cd /
    exit 1
fi
