#!/bin/bash
# Shannon V3 Agent Tracking - Functional Test

set -e

echo "Testing agent tracking feature..."
echo ""

# Require API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "✗ ANTHROPIC_API_KEY not set (required for wave execution)"
    echo "  Set API key to run this test"
    exit 1
fi

# Test 1: wave-agents command exists
echo "Test 1: wave-agents command exists"
shannon wave-agents --help > /dev/null 2>&1 || {
    echo "✗ wave-agents command not found"
    exit 1
}
echo "✓ wave-agents command exists"
echo ""

# Test 2: Create test project and analyze
echo "Test 2: Analyze spec (create session for wave)"
mkdir -p /tmp/test-agents
cd /tmp/test-agents

cat > spec.md << 'EOF'
Build a simple calculator with:
- Add two numbers
- Subtract two numbers
EOF

shannon analyze spec.md --json > /dev/null 2>&1 || {
    echo "✗ Analyze failed"
    exit 1
}
echo "✓ Analysis complete, session created"
echo ""

# Test 3: Run wave (should track agent)
echo "Test 3: Execute wave with agent tracking"
shannon wave "Implement calculator" 2>&1 | tee /tmp/wave_test_output.log | grep -q "Agent.*started" || {
    echo "✗ Agent tracking not initialized"
    exit 1
}

grep -q "Agent.*completed" /tmp/wave_test_output.log || {
    echo "✗ Agent not marked complete"
    exit 1
}
echo "✓ Wave executed with agent tracking"
echo ""

# Test 4: wave-agents shows tracked agent
echo "Test 4: wave-agents displays tracked agent"
shannon wave-agents 2>&1 | tee /tmp/agents_output.log

# Verify output contains agent data
grep -q "wave-1-agent" /tmp/agents_output.log || {
    echo "✗ Agent not found in wave-agents output"
    cat /tmp/agents_output.log
    exit 1
}

grep -q "complete" /tmp/agents_output.log || {
    echo "✗ Agent status not shown"
    exit 1
}

grep -q "100%" /tmp/agents_output.log || {
    echo "✗ Agent progress not shown"
    exit 1
}

echo "✓ wave-agents displays tracked agent correctly"
echo ""

# Test 5: Agent persistence (reload in new command)
echo "Test 5: Agent data persists across commands"
shannon wave-agents | grep -q "wave-1-agent" || {
    echo "✗ Agent data not persisted to session"
    exit 1
}
echo "✓ Agent data persists in session"
echo ""

# Cleanup
cd /
rm -rf /tmp/test-agents

echo "✓ All agent tracking tests passed"
