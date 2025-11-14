#!/usr/bin/env python3
"""Capture dashboard screenshots for documentation"""

import asyncio
import sys
from pathlib import Path
from io import StringIO

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from shannon.metrics import MetricsCollector, LiveDashboard
from shannon.metrics.collector import MetricsSnapshot
from rich.console import Console


def capture_compact_view():
    """Capture compact view screenshot"""
    collector = MetricsCollector(operation_name="spec-analysis")

    # Create string buffer console
    buffer = StringIO()
    console = Console(file=buffer, width=80, force_terminal=True, legacy_windows=False)

    dashboard = LiveDashboard(collector=collector, console=console)

    # Create snapshot with sample data
    snapshot = MetricsSnapshot(
        cost_total=0.12,
        tokens_total=8200,
        duration_seconds=45.0,
        progress=0.6,
        current_operation="spec-analysis",
        total_stages=8,
        completed_stages=["Structural", "Cognitive", "Coordination", "Temporal", "Technical"]
    )

    # Render compact view
    compact = dashboard._create_compact_layout(snapshot)
    console.print(compact)

    return buffer.getvalue()


def capture_detailed_view():
    """Capture detailed view screenshot"""
    collector = MetricsCollector(operation_name="spec-analysis")

    # Create string buffer console
    buffer = StringIO()
    console = Console(file=buffer, width=100, force_terminal=True, legacy_windows=False)

    dashboard = LiveDashboard(collector=collector, console=console)

    # Add streaming messages
    dashboard.streaming_buffer.append("Initializing Shannon CLI V3.0 spec analysis...")
    dashboard.streaming_buffer.append("Loading specification document")
    dashboard.streaming_buffer.append("Validating structure")
    dashboard.streaming_buffer.append("")
    dashboard.streaming_buffer.append("Analyzing Structural dimension...")
    dashboard.streaming_buffer.append("  45 files, 8 modules, modular architecture")
    dashboard.streaming_buffer.append("Progress: 62%")
    dashboard.streaming_buffer.append("Stage: Dimension 5/8")

    # Create snapshot with sample data
    snapshot = MetricsSnapshot(
        cost_total=0.1234,
        cost_input=0.0234,
        cost_output=0.1000,
        tokens_total=8234,
        tokens_input=1234,
        tokens_output=7000,
        duration_seconds=45.2,
        progress=0.625,
        current_stage="Technical Analysis",
        current_operation="spec-analysis",
        total_stages=8,
        completed_stages=["Structural", "Cognitive", "Coordination", "Temporal", "Technical"],
        message_count=42,
        error_count=0
    )

    # Render detailed view
    detailed = dashboard._create_detailed_layout(snapshot)
    console.print(detailed)

    return buffer.getvalue()


if __name__ == '__main__':
    print("=== COMPACT VIEW ===")
    print(capture_compact_view())
    print()
    print()
    print("=== DETAILED VIEW ===")
    print(capture_detailed_view())
