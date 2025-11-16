#!/bin/bash
# Shannon CLI Test Helper Functions
# Common utilities for functional testing

# CRITICAL: Set required environment variables for testing
export ANTHROPIC_API_KEY="***REMOVED_API_KEY***"
export SHANNON_TEST_MODE=1

# Assert output contains expected pattern
assert_contains() {
    local output="$1"
    local pattern="$2"
    local test_name="$3"

    if echo "$output" | grep -qE "$pattern"; then
        echo "  ✅ PASS: $test_name"
        return 0
    else
        echo "  ❌ FAIL: $test_name"
        echo "     Expected pattern: $pattern"
        echo "     Output preview: $(echo "$output" | head -3)"
        return 1
    fi
}

# Assert exit code matches expected
assert_exit_code() {
    local expected=$1
    local actual=$2
    local test_name="$3"

    if [ "$actual" -eq "$expected" ]; then
        echo "  ✅ PASS: $test_name (exit code: $actual)"
        return 0
    else
        echo "  ❌ FAIL: $test_name"
        echo "     Expected exit code: $expected"
        echo "     Actual exit code: $actual"
        return 1
    fi
}

# Assert command exists and is executable
assert_command_exists() {
    local command_name="$1"
    local test_name="$2"

    if command -v "$command_name" &> /dev/null; then
        echo "  ✅ PASS: $test_name (command: $command_name)"
        return 0
    else
        echo "  ❌ FAIL: $test_name"
        echo "     Command not found: $command_name"
        return 1
    fi
}

# Extract metric value from output
extract_metric() {
    local output="$1"
    local metric_pattern="$2"

    echo "$output" | grep -oE "$metric_pattern" | head -1
}

# Run shannon command with timeout and capture output
run_shannon() {
    local timeout_seconds="${SHANNON_TEST_TIMEOUT:-300}"
    timeout "$timeout_seconds" shannon "$@" 2>&1
}

# Assert file exists
assert_file_exists() {
    local file_path="$1"
    local test_name="$2"

    if [ -f "$file_path" ]; then
        echo "  ✅ PASS: $test_name"
        return 0
    else
        echo "  ❌ FAIL: $test_name"
        echo "     File not found: $file_path"
        return 1
    fi
}

# Assert directory exists
assert_dir_exists() {
    local dir_path="$1"
    local test_name="$2"

    if [ -d "$dir_path" ]; then
        echo "  ✅ PASS: $test_name"
        return 0
    else
        echo "  ❌ FAIL: $test_name"
        echo "     Directory not found: $dir_path"
        return 1
    fi
}

# Track test results
TEST_PASSED=0
TEST_FAILED=0

record_pass() {
    TEST_PASSED=$((TEST_PASSED + 1))
}

record_fail() {
    TEST_FAILED=$((TEST_FAILED + 1))
}

# Print test summary
print_summary() {
    local test_file="$1"
    echo ""
    echo "─────────────────────────────────────"
    echo "Summary for $(basename "$test_file")"
    echo "  Passed: $TEST_PASSED"
    echo "  Failed: $TEST_FAILED"
    echo "─────────────────────────────────────"
    echo ""

    if [ $TEST_FAILED -eq 0 ]; then
        return 0
    else
        return 1
    fi
}
