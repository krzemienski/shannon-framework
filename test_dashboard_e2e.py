#!/usr/bin/env python3
"""End-to-end test: Shannon analyze with LiveDashboard"""

import asyncio
from pathlib import Path
from shannon.metrics.collector import MetricsCollector
from shannon.metrics.dashboard import LiveDashboard
from shannon.sdk.interceptor import MessageInterceptor
from shannon.sdk.client import ShannonSDKClient

async def test_analyze_with_dashboard():
    """Run actual Shannon analysis with live dashboard"""

    print("=" * 80)
    print("Shannon CLI V3 - Live Dashboard End-to-End Test")
    print("=" * 80)
    print()

    # Read test spec
    spec_text = Path("tests/functional/fixtures/simple_spec.md").read_text()

    # Create SDK client
    client = ShannonSDKClient()

    # Create metrics collector
    collector = MetricsCollector(operation_name="e2e-test")

    # Create dashboard
    dashboard = LiveDashboard(collector, refresh_per_second=4)

    # Create interceptor
    interceptor = MessageInterceptor()

    print("Starting analysis with live dashboard...")
    print("Watch for:")
    print("  • Progress bar updating")
    print("  • Cost/tokens increasing")
    print("  • Duration counting")
    print()
    print("-" * 80)
    print()

    messages = []

    try:
        # Import query function
        from claude_agent_sdk import query

        # Create query iterator
        query_iter = query(
            prompt=f"/shannon:spec {spec_text}",
            options=client.base_options
        )

        # Intercept for metrics
        instrumented_iter = interceptor.intercept(query_iter, [collector])

        # Run with dashboard
        with dashboard:
            async for msg in instrumented_iter:
                messages.append(msg)
                # Dashboard updates automatically via collector

        print()
        print("-" * 80)
        print("✅ Analysis complete!")
        print(f"Messages received: {len(messages)}")

        # Show final metrics
        snapshot = collector.get_snapshot()
        print(f"\nFinal Metrics:")
        print(f"  Cost: ${snapshot.cost_usd:.4f}")
        print(f"  Tokens: {snapshot.tokens_total:,}")
        print(f"  Duration: {snapshot.duration_seconds:.1f}s")
        print(f"  Progress: {snapshot.progress_percent}%")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_analyze_with_dashboard())
