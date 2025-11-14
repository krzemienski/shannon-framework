#!/usr/bin/env python3
"""Interactive Demo: Shannon CLI V3.0 Metrics Dashboard

Demonstrates:
1. Live metrics dashboard with two-layer UI
2. Simulated SDK message stream
3. Real-time progress updates
4. Keyboard controls (Enter/Esc toggle)
5. Integration with MessageInterceptor

Usage:
    python examples/metrics/demo_dashboard.py

Controls:
    Enter - Expand to detailed view
    Esc   - Collapse to compact view
    q     - Quit demo
    p     - Pause/resume

Requirements:
    - Shannon CLI V3.0 (src/shannon/metrics)
    - Wave 1 SDK interceptor (src/shannon/sdk/interceptor.py)
    - Rich library
    - termios support (macOS/Linux)
"""

import asyncio
import sys
from dataclasses import dataclass
from typing import List, AsyncIterator
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from shannon.metrics import MetricsCollector, LiveDashboard
from shannon.sdk.interceptor import MessageInterceptor


# Simulated SDK message classes

@dataclass
class Usage:
    """Simulated SDK Usage block"""
    input_tokens: int
    output_tokens: int


@dataclass
class TextContent:
    """Simulated SDK text content"""
    text: str


@dataclass
class AssistantMessage:
    """Simulated SDK assistant message"""
    content: List[TextContent]
    usage: Usage


@dataclass
class StreamDelta:
    """Simulated SDK streaming delta"""
    text: str


@dataclass
class StreamMessage:
    """Simulated SDK streaming message"""
    delta: StreamDelta


# Demo simulation

async def simulate_spec_analysis() -> AsyncIterator:
    """
    Simulate Shannon spec analysis with realistic message stream

    Simulates analyzing SHANNON_CLI_V3_DETAILED_SPEC.md with 8 dimensions.
    """
    # Phase 1: Initialization
    yield AssistantMessage(
        content=[TextContent(text="Initializing Shannon CLI V3.0 spec analysis...")],
        usage=Usage(input_tokens=150, output_tokens=20)
    )
    await asyncio.sleep(0.5)

    yield StreamMessage(delta=StreamDelta(text="Loading specification document"))
    await asyncio.sleep(0.2)

    yield StreamMessage(delta=StreamDelta(text="Validating structure"))
    await asyncio.sleep(0.2)

    # Phase 2: Dimension analysis (8 dimensions)
    dimensions = [
        ("Structural", "45 files, 8 modules, modular architecture"),
        ("Cognitive", "Complex algorithms (cost optimization, smart context)"),
        ("Coordination", "6 teams, 8 integration points"),
        ("Temporal", "10 weeks timeline"),
        ("Technical", "Terminal control, SDK integration, streaming"),
        ("Scale", "Moderate orchestration complexity"),
        ("Uncertainty", "Low - detailed specification"),
        ("Dependencies", "SDK, Rich, MCPs")
    ]

    for i, (dim_name, details) in enumerate(dimensions, 1):
        # Dimension start
        yield StreamMessage(delta=StreamDelta(text=f"\\nAnalyzing {dim_name} dimension..."))
        await asyncio.sleep(0.3)

        # Dimension details
        yield StreamMessage(delta=StreamDelta(text=f"  {details}"))
        await asyncio.sleep(0.2)

        # Progress update
        progress = int((i / len(dimensions)) * 100)
        yield StreamMessage(delta=StreamDelta(text=f"Progress: {progress}%"))
        await asyncio.sleep(0.1)

        yield StreamMessage(delta=StreamDelta(text=f"Stage: Dimension {i}/8"))
        await asyncio.sleep(0.2)

        # Usage update
        tokens_used = 200 + (i * 150)
        yield AssistantMessage(
            content=[TextContent(text=f"Completed {dim_name}")],
            usage=Usage(input_tokens=tokens_used, output_tokens=tokens_used // 2)
        )
        await asyncio.sleep(0.4)

    # Phase 3: Synthesis
    yield StreamMessage(delta=StreamDelta(text="\\nSynthesizing analysis results..."))
    await asyncio.sleep(0.5)

    yield StreamMessage(delta=StreamDelta(text="Calculating complexity score"))
    await asyncio.sleep(0.3)

    yield StreamMessage(delta=StreamDelta(text="Generating recommendations"))
    await asyncio.sleep(0.3)

    # Final result
    yield AssistantMessage(
        content=[TextContent(text="Analysis complete! Complexity: 0.60 (COMPLEX)")],
        usage=Usage(input_tokens=2500, output_tokens=1200)
    )
    await asyncio.sleep(0.5)

    yield StreamMessage(delta=StreamDelta(text="\\n✓ All 8 dimensions analyzed"))
    yield StreamMessage(delta=StreamDelta(text="✓ Recommendations generated"))
    yield StreamMessage(delta=StreamDelta(text="✓ Timeline validated"))


async def run_demo():
    """
    Run interactive dashboard demo

    Simulates spec analysis with live dashboard.
    """
    print("Shannon CLI V3.0 - Live Metrics Dashboard Demo")
    print("=" * 60)
    print()
    print("This demo simulates analyzing SHANNON_CLI_V3_DETAILED_SPEC.md")
    print("with 8 dimensions using the live metrics dashboard.")
    print()
    print("Controls:")
    print("  Enter - Expand to detailed view")
    print("  Esc   - Collapse to compact view")
    print("  q     - Quit demo")
    print()
    print("Starting in 2 seconds...")
    print()
    await asyncio.sleep(2)

    # Create metrics collector
    collector = MetricsCollector(operation_name="spec-analysis")

    # Create dashboard
    dashboard = LiveDashboard(
        collector=collector,
        refresh_per_second=4
    )

    # Create interceptor
    interceptor = MessageInterceptor()

    # Start dashboard
    dashboard.start()

    try:
        # Simulate analysis with interception
        message_stream = simulate_spec_analysis()

        # Process messages with dashboard updates
        async for msg in interceptor.intercept(message_stream, [collector]):
            # Extract text for streaming buffer
            text = None
            if hasattr(msg, 'delta') and hasattr(msg.delta, 'text'):
                text = msg.delta.text
            elif hasattr(msg, 'content') and msg.content:
                if isinstance(msg.content, list) and msg.content:
                    text = msg.content[0].text if hasattr(msg.content[0], 'text') else None

            # Update dashboard
            dashboard.update(streaming_message=text)

            # Check for quit request
            if dashboard.quit_requested:
                print("\nQuitting demo...")
                break

            # Small delay for visual effect
            await asyncio.sleep(0.05)

        # Wait a bit to show final state
        if not dashboard.quit_requested:
            await asyncio.sleep(3)

    finally:
        # Stop dashboard
        dashboard.stop()

    # Show final summary
    snapshot = collector.get_snapshot()
    print("\nDemo Complete!")
    print("-" * 60)
    print(f"Messages processed: {snapshot.message_count}")
    print(f"Total cost: ${snapshot.cost_total:.4f}")
    print(f"Total tokens: {snapshot.tokens_total:,}")
    print(f"Duration: {snapshot.duration_seconds:.1f}s")
    print(f"Completed stages: {len(snapshot.completed_stages)}/{snapshot.total_stages}")


async def run_simple_demo():
    """
    Run simple dashboard demo (no keyboard required)

    Useful for testing without terminal interaction.
    """
    print("Shannon CLI V3.0 - Simple Dashboard Demo (No Keyboard)")
    print("=" * 60)
    print()

    # Create collector and dashboard
    collector = MetricsCollector(operation_name="simple-test")
    dashboard = LiveDashboard(collector=collector, refresh_per_second=4)

    # Start dashboard
    dashboard.start()

    try:
        # Simulate some messages
        for i in range(10):
            # Create message
            msg = AssistantMessage(
                content=[TextContent(text=f"Message {i}")],
                usage=Usage(input_tokens=100 * (i + 1), output_tokens=50 * (i + 1))
            )

            # Process message
            await collector.process(msg)

            # Update dashboard
            dashboard.update(streaming_message=f"Processing step {i+1}/10")

            # Wait
            await asyncio.sleep(0.5)

        # Complete
        await collector.on_stream_complete()

        # Show final state
        await asyncio.sleep(2)

    finally:
        dashboard.stop()

    print("\nDemo complete!")


if __name__ == '__main__':
    # Check for simple mode
    if '--simple' in sys.argv:
        asyncio.run(run_simple_demo())
    else:
        asyncio.run(run_demo())
