"""
Wave 1 Exit Gate: Operational Telemetry Dashboard Validation

Runs all 15 Wave 1 functional tests to validate:
- Command context visibility
- Live metrics (cost, tokens, duration)
- 4Hz progress updates
- WAITING state visibility
- State transitions
- Interactive expansion/pause/layer switching
- Refresh rate stability
- Terminal rendering quality
- Error handling
- Keyboard controls
- Performance overhead monitoring
- Metrics accuracy validation

Requires 100% pass rate to proceed to Wave 2.

Part of Shannon V3 Wave 1: Operational Telemetry Dashboard
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation_gates.gate_framework import ValidationGate
from cli_functional.test_wave1_metrics import (
    TestWave1Dashboard,
    TestWave1Metrics,
    TestWave1Performance
)


async def wave1_exit_gate() -> bool:
    """
    Run Wave 1 exit gate - all 15 functional tests

    Returns:
        bool: True if all tests pass
    """
    gate = ValidationGate(phase=1, gate_type='exit')

    # Instantiate test classes
    dashboard_tests = TestWave1Dashboard()
    metrics_tests = TestWave1Metrics()
    performance_tests = TestWave1Performance()

    # Add all 15 Wave 1 tests
    # TestWave1Dashboard (5 tests)
    gate.add_test(dashboard_tests.test_command_context_visibility)
    gate.add_test(dashboard_tests.test_live_metrics_updates)
    gate.add_test(dashboard_tests.test_waiting_state_visibility)
    gate.add_test(dashboard_tests.test_state_transitions)
    gate.add_test(dashboard_tests.test_dashboard_render_quality)

    # TestWave1Metrics (5 tests)
    gate.add_test(metrics_tests.test_metrics_accuracy)
    gate.add_test(metrics_tests.test_cost_calculation)
    gate.add_test(metrics_tests.test_token_counting)
    gate.add_test(metrics_tests.test_duration_tracking)
    gate.add_test(metrics_tests.test_metrics_persistence)

    # TestWave1Performance (5 tests)
    gate.add_test(performance_tests.test_refresh_rate_4hz)
    gate.add_test(performance_tests.test_performance_overhead)
    gate.add_test(performance_tests.test_interactive_controls)
    gate.add_test(performance_tests.test_error_handling)
    gate.add_test(performance_tests.test_dashboard_stability)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave1_exit_gate())
    sys.exit(0 if success else 1)
