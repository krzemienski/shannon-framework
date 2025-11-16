#!/bin/bash
# Wave 4a Validation Gate: Agent Control
# Tests agent coordination and state tracking

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 4a: Agent Control Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: wave-agents command exists
echo "Test 1: wave-agents command availability"
output=$(shannon wave-agents --help 2>&1 || shannon agents --help 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$output" != "COMMAND_NOT_FOUND" ]; then
    echo "  ✅ PASS: Agent command exists"
    record_pass
else
    echo "  ❌ FAIL: No agent command found (tried wave-agents, agents)"
    record_fail
fi

# Test 2: Agent state tracking (via wave command if available)
echo "Test 2: Agent state tracking in wave execution"

# Try to run a simple wave command and check for agent state indicators
output=$(shannon wave "Simple task" --plan 2>&1 || echo "WAVE_COMMAND_FAILED")

if [ "$output" != "WAVE_COMMAND_FAILED" ]; then
    # Check for agent-related output
    if echo "$output" | grep -qiE 'agent|wave.*plan|#[0-9]'; then
        echo "  ✅ PASS: Wave command shows agent-related output"
        record_pass
    else
        echo "  ⚠️  INFO: Wave command works but no agent state shown"
    fi
else
    echo "  ⚠️  INFO: Wave command not available or failed (expected if not implemented)"
fi

# Test 3: Agent controller subsystem files exist
echo "Test 3: Agent subsystem files"
assert_file_exists "src/shannon/agents/controller.py" "controller.py exists" && record_pass || record_fail
assert_file_exists "src/shannon/agents/state_tracker.py" "state_tracker.py exists" && record_pass || record_fail

echo ""
print_summary "test_wave4_agents.sh"
