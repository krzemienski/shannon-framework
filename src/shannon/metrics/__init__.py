"""Shannon CLI V3.0 Metrics Dashboard Module

Live metrics dashboard with two-layer UI and keyboard control.

Public API:
    - MetricsCollector: Implements MessageCollector for SDK integration
    - MetricsSnapshot: Immutable metrics data
    - LiveDashboard: Two-layer UI (compact/detailed)
    - KeyboardHandler: Non-blocking keyboard input
    - Key: Keyboard key enum

Usage Example:

    from shannon.metrics import MetricsCollector, LiveDashboard
    from shannon.sdk.interceptor import MessageInterceptor

    # Create collector
    collector = MetricsCollector(operation_name="spec-analysis")

    # Create interceptor with collector
    interceptor = MessageInterceptor()

    # Run with dashboard
    dashboard = LiveDashboard(collector)
    with dashboard:
        # SDK query with metrics collection
        async for msg in interceptor.intercept(query_iter, [collector]):
            # Messages flow through
            # Collector updates metrics in background
            # Dashboard shows live progress
            dashboard.update(streaming_message=msg.text if hasattr(msg, 'text') else None)

Integration with Wave 1:
    - MetricsCollector implements MessageCollector from sdk.interceptor
    - Plugs directly into MessageInterceptor.intercept()
    - Zero-latency message streaming maintained
    - Metrics collected in parallel
"""

from shannon.metrics.collector import (
    MetricsCollector,
    MetricsSnapshot
)

from shannon.metrics.dashboard import (
    LiveDashboard,
    run_with_dashboard
)

from shannon.metrics.keyboard import (
    KeyboardHandler,
    Key,
    wait_for_key
)


__all__ = [
    # Collector
    'MetricsCollector',
    'MetricsSnapshot',

    # Dashboard
    'LiveDashboard',
    'run_with_dashboard',

    # Keyboard
    'KeyboardHandler',
    'Key',
    'wait_for_key',
]


# Module metadata
__version__ = '3.0.0'
__author__ = 'Shannon CLI Team'
__description__ = 'Live metrics dashboard for Shannon CLI'
