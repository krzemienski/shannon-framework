#!/usr/bin/env python3
"""Test LiveDashboard with actual metric updates"""

import asyncio
from shannon.metrics.collector import MetricsCollector
from shannon.metrics.dashboard import LiveDashboard
from claude_agent_sdk import TextBlock, ToolUseBlock, ResultMessage

async def test_dashboard_with_updates():
    """Test dashboard with simulated SDK messages"""

    # Create collector
    collector = MetricsCollector(operation_name="spec-analysis")

    # Create dashboard
    dashboard = LiveDashboard(collector, refresh_per_second=4)

    print("Testing dashboard with metric updates...")
    print("")

    # Run dashboard
    with dashboard:
        # Simulate SDK messages
        for i in range(20):
            # Create fake message
            if i % 3 == 0:
                msg = ToolUseBlock(name="Read", input={"file_path": f"file{i}.py"})
            else:
                msg = TextBlock(text=f"Processing dimension {i}...")

            # Update collector
            collector.update(msg)

            # Wait (dashboard auto-refreshes at 4 Hz)
            await asyncio.sleep(0.3)

    print("\n✅ Dashboard with updates complete")
    print(f"Final snapshot: {collector.get_snapshot()}")

if __name__ == "__main__":
    asyncio.run(test_dashboard_with_updates())
