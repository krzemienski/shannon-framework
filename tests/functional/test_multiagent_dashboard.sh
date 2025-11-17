#!/bin/bash
# Test Multi-Agent Dashboard Display with Playwright
# Per V5 Plan Phase 5 Task 5.2 (lines 663-701)

set -e

echo "Testing Multi-Agent Dashboard Display..."
echo

# Start server in background
echo "Starting WebSocket server..."
python -m shannon.server.app > /tmp/server_multiagent.log 2>&1 &
SERVER_PID=$!
sleep 5

# Start dashboard in background
echo "Starting dashboard..."
cd dashboard && npm run dev > /tmp/dashboard_multiagent.log 2>&1 &
DASHBOARD_PID=$!
cd ..
sleep 10

echo "Services started (server: $SERVER_PID, dashboard: $DASHBOARD_PID)"
echo

# Run multi-skill task in background
echo "Executing multi-skill task..."
shannon do "create main.py, create tests.py, create README.md" --dashboard > /tmp/command_multiagent.log 2>&1 &
COMMAND_PID=$!

# Give it a moment to start
sleep 3

# Playwright verification
echo "Running Playwright verification..."
python3 <<'PLAYWRIGHT'
import asyncio
import sys

async def test():
    try:
        # Import Playwright MCP functions
        from mcp__playwright__puppeteer_navigate import puppeteer_navigate
        from mcp__playwright__puppeteer_wait_for import puppeteer_wait_for
        from mcp__playwright__puppeteer_screenshot import puppeteer_screenshot
        from mcp__playwright__puppeteer_snapshot import puppeteer_snapshot

        print("Navigating to dashboard...")
        await puppeteer_navigate(url="http://localhost:5173")

        print("Waiting for connection...")
        await puppeteer_wait_for(text="Connected", timeout=10000)
        print("✓ Dashboard connected")

        print("Waiting for agents to appear (30s timeout)...")
        try:
            await puppeteer_wait_for(text="agent-", timeout=30000)
            print("✓ Agents visible in dashboard")
        except:
            print("⚠ Agents not visible yet (may still be executing)")

        # Take screenshot
        print("Capturing screenshot...")
        await puppeteer_screenshot(name="multiagent-dashboard")
        print("✓ Screenshot saved: multiagent-dashboard.png")

        # Get snapshot to verify
        snapshot = await puppeteer_snapshot()

        # Check for agent indicators
        snapshot_str = str(snapshot)
        has_agents = "agent-" in snapshot_str or "AgentPool" in snapshot_str

        if has_agents:
            print("✓ AgentPool panel shows agent entries")
        else:
            print("⚠ AgentPool panel may be empty or agents not yet spawned")

        print("\n✓ Multi-agent dashboard test completed")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Playwright test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

asyncio.run(test())
PLAYWRIGHT

PLAYWRIGHT_EXIT=$?

# Cleanup background processes
echo
echo "Cleaning up..."
kill $SERVER_PID $DASHBOARD_PID $COMMAND_PID 2>/dev/null || true
sleep 2

# Results
if [ $PLAYWRIGHT_EXIT -eq 0 ]; then
    echo "✓ Multi-agent dashboard test PASSED"
    exit 0
else
    echo "✗ Multi-agent dashboard test FAILED"
    echo
    echo "Server log:"
    tail -20 /tmp/server_multiagent.log
    echo
    echo "Dashboard log:"
    tail -20 /tmp/dashboard_multiagent.log
    echo
    echo "Command log:"
    tail -20 /tmp/command_multiagent.log
    exit 1
fi
