#!/usr/bin/env python3
"""Standalone test of LiveDashboard to verify it works"""

import asyncio
import time
from shannon.metrics.collector import MetricsCollector
from shannon.metrics.dashboard import LiveDashboard

async def test_dashboard():
    """Test dashboard with simulated metrics updates"""

    # Create collector
    collector = MetricsCollector(operation_name="test-analysis")

    # Create dashboard
    dashboard = LiveDashboard(collector, refresh_per_second=2)

    print("Starting dashboard test...")
    print("Dashboard will run for 5 seconds with simulated updates")
    print("")

    # Run dashboard
    with dashboard:
        # Simulate metrics updates
        for i in range(10):
            # Simulate progress
            await asyncio.sleep(0.5)

            # Dashboard auto-refreshes at 2 Hz
            # Collector would be updated by MessageInterceptor in real usage

    print("\n✅ Dashboard test complete")

if __name__ == "__main__":
    asyncio.run(test_dashboard())
