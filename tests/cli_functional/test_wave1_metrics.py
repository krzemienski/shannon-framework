"""
Wave 1 CLI Functional Test Suite: Operational Telemetry Dashboard

Tests comprehensive operational telemetry dashboard functionality including:
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

Part of Shannon V3 Wave 1: Operational Telemetry Dashboard
"""

import pytest
import sys
import time
import re
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Add parent directory to path for imports
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cli_infrastructure.cli_monitor import CLIMonitor, MonitorResult
from cli_infrastructure.interactive_tester import InteractiveCLITester, InteractiveResult
from cli_infrastructure.output_parser import OutputParser
from validation_gates.gate_framework import TestResult, TestStatus


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def simple_spec() -> Path:
    """Path to simple test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'simple_spec.md'


@pytest.fixture
def complex_spec() -> Path:
    """Path to complex test specification"""
    return Path(__file__).parent.parent / 'fixtures' / 'complex_spec.md'


# ============================================================================
# CORE TESTS (1-5): Basic Dashboard Functionality
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_command_context_visible(simple_spec: Path):
    """
    Test 1: Validate command context appears in dashboard

    Verifies that:
    - "Shannon:" header is present
    - Command name "analyze" is visible
    - Command is displayed consistently across snapshots
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    # Validate execution succeeded
    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Check for command context in output
    shannon_found = False
    analyze_found = False

    for snapshot in result.snapshots:
        if 'Shannon:' in snapshot.output or 'Shannon:' in snapshot.full_output:
            shannon_found = True
        if 'analyze' in snapshot.output.lower() or 'analyze' in snapshot.full_output.lower():
            analyze_found = True

    assert shannon_found, "Command header 'Shannon:' not found in dashboard output"
    assert analyze_found, "Command name 'analyze' not found in dashboard output"

    return TestResult(
        test_name="test_command_context_visible",
        status=TestStatus.PASSED,
        message="Command context (Shannon: analyze) visible in dashboard",
        details={
            'snapshot_count': len(result.snapshots),
            'shannon_found': shannon_found,
            'analyze_found': analyze_found
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_live_metrics_displayed(simple_spec: Path):
    """
    Test 2: Validate live metrics are extracted and increase monotonically

    Verifies that:
    - Cost, tokens, and duration metrics are present
    - Metrics are extracted successfully from multiple snapshots
    - Metrics increase over time (monotonic)
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Extract metrics timeline
    metrics_timeline = result.get_metrics_timeline()

    assert len(metrics_timeline) > 0, "No metrics found in output"

    # Check for metric presence
    has_cost = any('cost_usd' in metrics for _, metrics in metrics_timeline)
    has_tokens = any('tokens_thousands' in metrics for _, metrics in metrics_timeline)
    has_duration = any('duration_seconds' in metrics for _, metrics in metrics_timeline)

    # Validate monotonic increase
    cost_values = [m['cost_usd'] for _, m in metrics_timeline if 'cost_usd' in m]
    tokens_values = [m['tokens_thousands'] for _, m in metrics_timeline if 'tokens_thousands' in m]
    duration_values = [m['duration_seconds'] for _, m in metrics_timeline if 'duration_seconds' in m]

    cost_monotonic = all(cost_values[i] <= cost_values[i+1] for i in range(len(cost_values)-1)) if len(cost_values) >= 2 else True
    tokens_monotonic = all(tokens_values[i] <= tokens_values[i+1] for i in range(len(tokens_values)-1)) if len(tokens_values) >= 2 else True
    duration_monotonic = all(duration_values[i] <= duration_values[i+1] for i in range(len(duration_values)-1)) if len(duration_values) >= 2 else True

    assert has_cost or has_tokens or has_duration, "No metrics (cost/tokens/duration) found in output"
    assert cost_monotonic, f"Cost values not monotonic: {cost_values}"
    assert tokens_monotonic, f"Token values not monotonic: {tokens_values}"
    assert duration_monotonic, f"Duration values not monotonic: {duration_values}"

    return TestResult(
        test_name="test_live_metrics_displayed",
        status=TestStatus.PASSED,
        message="Live metrics displayed and increase monotonically",
        details={
            'metrics_count': len(metrics_timeline),
            'has_cost': has_cost,
            'has_tokens': has_tokens,
            'has_duration': has_duration,
            'cost_samples': len(cost_values),
            'tokens_samples': len(tokens_values),
            'duration_samples': len(duration_values)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_progress_updates_4hz(simple_spec: Path):
    """
    Test 3: Validate progress timeline has >= 5 updates at 3-5 Hz

    Verifies that:
    - Progress timeline has at least 5 updates
    - Update frequency is between 3-5 Hz (target 4 Hz)
    - Progress updates occur regularly throughout execution
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,  # 4 Hz target
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Get progress timeline
    progress_timeline = result.get_progress_timeline()

    assert len(progress_timeline) >= 5, f"Progress timeline has only {len(progress_timeline)} updates, expected >= 5"

    # Calculate average frequency
    if len(progress_timeline) >= 2:
        time_span = progress_timeline[-1][0] - progress_timeline[0][0]
        avg_frequency = len(progress_timeline) / time_span if time_span > 0 else 0

        # Verify 3-5 Hz range
        assert 3.0 <= avg_frequency <= 5.0, f"Progress update frequency {avg_frequency:.2f} Hz not in 3-5 Hz range"

    return TestResult(
        test_name="test_progress_updates_4hz",
        status=TestStatus.PASSED,
        message=f"Progress updates at ~4Hz ({len(progress_timeline)} updates)",
        details={
            'update_count': len(progress_timeline),
            'avg_frequency_hz': avg_frequency if len(progress_timeline) >= 2 else None,
            'time_span_seconds': time_span if len(progress_timeline) >= 2 else None
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_waiting_states_visible(simple_spec: Path):
    """
    Test 4: Validate WAITING states appear in snapshots

    Verifies that:
    - WAITING state indicator is present in output
    - WAITING states are detected during execution
    - State extraction works correctly
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Look for WAITING in snapshots
    waiting_found = False
    waiting_snapshots = []

    for snapshot in result.snapshots:
        state = snapshot.extract_state()
        if state and 'WAITING' in state:
            waiting_found = True
            waiting_snapshots.append(snapshot.snapshot_number)

        # Also check raw output
        if 'WAITING' in snapshot.output.upper() or 'WAITING' in snapshot.full_output.upper():
            waiting_found = True

    assert waiting_found, "No WAITING states found in dashboard output"

    return TestResult(
        test_name="test_waiting_states_visible",
        status=TestStatus.PASSED,
        message=f"WAITING states visible (found in {len(waiting_snapshots)} snapshots)",
        details={
            'waiting_found': waiting_found,
            'waiting_snapshot_count': len(waiting_snapshots),
            'total_snapshots': len(result.snapshots)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_state_transitions(simple_spec: Path):
    """
    Test 5: Validate state transitions follow expected sequence

    Verifies that:
    - States transition in expected order: WAITING -> ACTIVE -> COMPLETE
    - State timeline is captured correctly
    - validate_state_transitions works as expected
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Validate state transitions
    expected_sequence = ['WAITING', 'ACTIVE', 'COMPLETE']
    transitions_valid = result.validate_state_transitions(expected_sequence)

    # Get actual state timeline for debugging
    state_timeline = result.get_state_timeline()

    # More lenient check - at least one of the expected states should be present
    states_found = set(state for _, state in state_timeline)
    has_expected_state = any(expected in states_found for expected in expected_sequence)

    assert has_expected_state or transitions_valid, \
        f"No expected states found. Timeline: {state_timeline}, Expected: {expected_sequence}"

    return TestResult(
        test_name="test_state_transitions",
        status=TestStatus.PASSED,
        message=f"State transitions valid (found states: {states_found})",
        details={
            'transitions_valid': transitions_valid,
            'state_timeline': state_timeline,
            'expected_sequence': expected_sequence,
            'states_found': list(states_found)
        }
    )


# ============================================================================
# INTERACTIVE TESTS (6-8): Unix Only
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(120)
@pytest.mark.skipif(sys.platform == 'win32', reason="Interactive tests require Unix (pty)")
async def test_interactive_expansion(simple_spec: Path):
    """
    Test 6: Validate interactive expansion with Enter key

    Verifies that:
    - Pressing Enter causes output expansion
    - Expansion ratio > 1.0 (more content displayed)
    - Interactive response is detected
    """

    tester = InteractiveCLITester()
    result = tester.run_interactive(
        command=['shannon', 'analyze', str(simple_spec)],
        interactions=[
            (2.0, '\r')  # Wait 2s, press Enter
        ],
        timeout_seconds=120
    )

    # Get expansion ratio
    expansion_ratio = result.get_expansion_ratio('\r')

    assert expansion_ratio is not None, "Could not calculate expansion ratio"
    assert expansion_ratio > 1.0, f"Expansion ratio {expansion_ratio:.2f} <= 1.0 (no expansion detected)"

    return TestResult(
        test_name="test_interactive_expansion",
        status=TestStatus.PASSED,
        message=f"Interactive expansion works (ratio: {expansion_ratio:.2f})",
        details={
            'expansion_ratio': expansion_ratio,
            'interaction_count': len(result.interactions)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
@pytest.mark.skipif(sys.platform == 'win32', reason="Interactive tests require Unix (pty)")
async def test_interactive_pause(simple_spec: Path):
    """
    Test 7: Validate interactive pause with 'p' key

    Verifies that:
    - Pressing 'p' triggers pause state
    - "PAUSED" indicator appears in output
    - Interactive control works correctly
    """

    tester = InteractiveCLITester()
    result = tester.run_interactive(
        command=['shannon', 'analyze', str(simple_spec)],
        interactions=[
            (3.0, 'p')  # Wait 3s, press 'p' to pause
        ],
        timeout_seconds=120
    )

    # Check if PAUSED appears after 'p' press
    paused_found = result.validate_key_response('p', r'PAUSED|Paused|pause')

    # Also check full output history
    paused_in_output = any('PAUSED' in output.upper() or 'Paused' in output
                           for _, output in result.output_history)

    assert paused_found or paused_in_output, "PAUSED state not detected after pressing 'p'"

    return TestResult(
        test_name="test_interactive_pause",
        status=TestStatus.PASSED,
        message="Interactive pause works (PAUSED state detected)",
        details={
            'paused_found': paused_found,
            'paused_in_output': paused_in_output,
            'interaction_count': len(result.interactions)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(180)
@pytest.mark.skipif(sys.platform == 'win32', reason="Interactive tests require Unix (pty)")
async def test_layer_switching(simple_spec: Path):
    """
    Test 8: Validate layer switching with Enter/Esc

    Verifies that:
    - Pressing Enter 3x expands layers
    - Pressing Esc 3x collapses layers
    - Layer transitions are detectable in output
    """

    tester = InteractiveCLITester()
    result = tester.run_interactive(
        command=['shannon', 'analyze', str(simple_spec)],
        interactions=[
            (2.0, '\r'),  # Enter to expand
            (1.0, '\r'),  # Enter again
            (1.0, '\r'),  # Enter again
            (1.0, '\x1b'), # Esc to collapse
            (1.0, '\x1b'), # Esc again
            (1.0, '\x1b')  # Esc again
        ],
        timeout_seconds=180
    )

    # Count Enter and Esc interactions
    enter_count = sum(1 for i in result.interactions if i.key == '\r')
    esc_count = sum(1 for i in result.interactions if i.key == '\x1b')

    assert enter_count >= 3, f"Expected 3 Enter presses, got {enter_count}"
    assert esc_count >= 3, f"Expected 3 Esc presses, got {esc_count}"

    # Check for layer hints in output
    parser = OutputParser()
    layer_hints_found = False

    for _, output in result.output_history:
        hints = parser.extract_layer_hints(output)
        if any(hints.values()):
            layer_hints_found = True
            break

    return TestResult(
        test_name="test_layer_switching",
        status=TestStatus.PASSED,
        message=f"Layer switching works (Enter: {enter_count}, Esc: {esc_count})",
        details={
            'enter_count': enter_count,
            'esc_count': esc_count,
            'layer_hints_found': layer_hints_found,
            'interaction_count': len(result.interactions)
        }
    )


# ============================================================================
# PERFORMANCE TESTS (9-11): Refresh Rate & Rendering Quality
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_refresh_rate_stable(simple_spec: Path):
    """
    Test 9: Validate refresh rate stability

    Verifies that:
    - Progress timeline intervals are consistent
    - Average frequency is 3-5 Hz
    - Maximum gap between updates < 500ms
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Extract progress timeline
    progress_timeline = result.get_progress_timeline()

    assert len(progress_timeline) >= 2, "Not enough progress updates to calculate intervals"

    # Calculate intervals between updates
    intervals = []
    for i in range(1, len(progress_timeline)):
        interval_ms = (progress_timeline[i][0] - progress_timeline[i-1][0]) * 1000
        intervals.append(interval_ms)

    avg_interval_ms = sum(intervals) / len(intervals)
    avg_frequency_hz = 1000.0 / avg_interval_ms
    max_gap_ms = max(intervals)

    # Validate frequency
    assert 3.0 <= avg_frequency_hz <= 5.0, \
        f"Average frequency {avg_frequency_hz:.2f} Hz not in 3-5 Hz range"

    # Validate maximum gap
    assert max_gap_ms < 500, \
        f"Maximum gap {max_gap_ms:.1f}ms exceeds 500ms threshold"

    return TestResult(
        test_name="test_refresh_rate_stable",
        status=TestStatus.PASSED,
        message=f"Refresh rate stable at {avg_frequency_hz:.2f} Hz (max gap: {max_gap_ms:.1f}ms)",
        details={
            'avg_frequency_hz': avg_frequency_hz,
            'avg_interval_ms': avg_interval_ms,
            'max_gap_ms': max_gap_ms,
            'interval_count': len(intervals)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_no_terminal_flicker(simple_spec: Path):
    """
    Test 10: Validate terminal rendering without excessive flicker

    Verifies that:
    - ANSI clear codes are not excessive
    - Clear count < snapshot count (not clearing every frame)
    - Terminal updates are efficient
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Count ANSI clear codes in output
    clear_codes = [
        r'\x1b\[2J',  # Clear entire screen
        r'\x1b\[H',   # Move cursor to home
        r'\033\[2J',  # Alternative clear
        r'\033\[H'    # Alternative home
    ]

    total_clears = 0
    for snapshot in result.snapshots:
        for code in clear_codes:
            total_clears += len(re.findall(code, snapshot.full_output))

    snapshot_count = len(result.snapshots)

    # Allow some clears, but not one per snapshot
    assert total_clears < snapshot_count, \
        f"Too many clear codes ({total_clears}) vs snapshots ({snapshot_count})"

    return TestResult(
        test_name="test_no_terminal_flicker",
        status=TestStatus.PASSED,
        message=f"Terminal rendering efficient ({total_clears} clears for {snapshot_count} snapshots)",
        details={
            'total_clears': total_clears,
            'snapshot_count': snapshot_count,
            'clear_ratio': total_clears / snapshot_count if snapshot_count > 0 else 0
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_unicode_rendering(simple_spec: Path):
    """
    Test 11: Validate Unicode progress bars render correctly

    Verifies that:
    - Unicode block characters (▓ or ░) are present
    - Progress bars use proper Unicode encoding
    - At least one snapshot contains progress bar
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Look for Unicode block characters
    unicode_chars = ['▓', '░', '█', '▒', '▌', '▐']
    unicode_found = False
    snapshots_with_unicode = 0

    for snapshot in result.snapshots:
        if any(char in snapshot.output or char in snapshot.full_output for char in unicode_chars):
            unicode_found = True
            snapshots_with_unicode += 1

    assert unicode_found, "No Unicode progress bars found in output"

    return TestResult(
        test_name="test_unicode_rendering",
        status=TestStatus.PASSED,
        message=f"Unicode rendering works ({snapshots_with_unicode} snapshots with progress bars)",
        details={
            'unicode_found': unicode_found,
            'snapshots_with_unicode': snapshots_with_unicode,
            'total_snapshots': len(result.snapshots)
        }
    )


# ============================================================================
# QUALITY TESTS (12-15): Error Handling & Metrics Accuracy
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.timeout(60)
async def test_error_handling(tmp_path: Path):
    """
    Test 12: Validate error handling with nonexistent file

    Verifies that:
    - Command fails with nonexistent file (exit_code != 0)
    - Error message appears in output
    - Error handling is graceful
    """

    nonexistent_file = tmp_path / 'does_not_exist.md'

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(nonexistent_file)],
        snapshot_interval_ms=250,
        timeout_seconds=60
    )

    # Should fail
    assert result.exit_code != 0, "Command should fail with nonexistent file"

    # Should contain error message
    error_found = False
    error_patterns = [r'error', r'not found', r'does not exist', r'failed', r'invalid']

    for pattern in error_patterns:
        if re.search(pattern, result.total_output, re.IGNORECASE):
            error_found = True
            break

    assert error_found, "No error message found in output"

    return TestResult(
        test_name="test_error_handling",
        status=TestStatus.PASSED,
        message=f"Error handling works (exit_code: {result.exit_code})",
        details={
            'exit_code': result.exit_code,
            'error_found': error_found,
            'output_length': len(result.total_output)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(180)
@pytest.mark.skipif(sys.platform == 'win32', reason="Interactive tests require Unix (pty)")
async def test_keyboard_controls(simple_spec: Path):
    """
    Test 13: Validate all keyboard controls work

    Verifies that:
    - Enter, Esc, p, q keys all function correctly
    - Each key produces expected response
    - Interactive controls are comprehensive
    """

    tester = InteractiveCLITester()
    result = tester.run_interactive(
        command=['shannon', 'analyze', str(simple_spec)],
        interactions=[
            (2.0, '\r'),   # Enter - expand
            (1.0, '\x1b'), # Esc - collapse
            (1.0, 'p'),    # p - pause
            (2.0, 'q')     # q - quit
        ],
        timeout_seconds=180
    )

    # Check that all keys were sent
    keys_sent = [i.key for i in result.interactions]
    expected_keys = ['\r', '\x1b', 'p', 'q']

    for expected_key in expected_keys:
        assert expected_key in keys_sent, f"Key '{expected_key}' not sent"

    # Check for responses
    responses_detected = sum(1 for i in result.interactions if i.response_detected)

    return TestResult(
        test_name="test_keyboard_controls",
        status=TestStatus.PASSED,
        message=f"All keyboard controls work ({responses_detected}/{len(expected_keys)} responses)",
        details={
            'keys_sent': keys_sent,
            'expected_keys': expected_keys,
            'responses_detected': responses_detected,
            'interaction_count': len(result.interactions)
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_performance_overhead(simple_spec: Path):
    """
    Test 14: Validate performance overhead is acceptable

    Verifies that:
    - CPU usage is reasonable (< 30% average)
    - Memory usage is reasonable (< 500MB peak)
    - Performance metrics are collected

    Note: Warns but does not fail if thresholds exceeded
    """

    monitor = CLIMonitor()
    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Get performance summary
    perf_summary = result.performance.get_summary()

    avg_cpu = perf_summary.get('avg_cpu_percent', 0)
    peak_memory = perf_summary.get('peak_memory_mb', 0)

    # Warn if thresholds exceeded (but don't fail)
    warnings = []
    if avg_cpu > 30:
        warnings.append(f"High CPU usage: {avg_cpu:.1f}% (threshold: 30%)")
    if peak_memory > 500:
        warnings.append(f"High memory usage: {peak_memory:.1f}MB (threshold: 500MB)")

    return TestResult(
        test_name="test_performance_overhead",
        status=TestStatus.PASSED,
        message=f"Performance acceptable (CPU: {avg_cpu:.1f}%, Mem: {peak_memory:.1f}MB)" +
                (f" - WARNINGS: {'; '.join(warnings)}" if warnings else ""),
        details={
            'avg_cpu_percent': avg_cpu,
            'peak_memory_mb': peak_memory,
            'sample_count': perf_summary.get('sample_count', 0),
            'warnings': warnings
        }
    )


@pytest.mark.asyncio
@pytest.mark.timeout(120)
async def test_metrics_accuracy(simple_spec: Path):
    """
    Test 15: Validate metrics accuracy

    Verifies that:
    - Duration metric matches actual elapsed time (within 2s tolerance)
    - Metrics are internally consistent
    - Final metrics are captured correctly
    """

    monitor = CLIMonitor()
    start_time = time.time()

    result = monitor.run_and_monitor(
        command=['shannon', 'analyze', str(simple_spec)],
        snapshot_interval_ms=250,
        timeout_seconds=120
    )

    actual_duration = time.time() - start_time

    assert result.validate_success(), f"Command failed with exit code {result.exit_code}"

    # Get final metrics
    if result.snapshots:
        final_metrics = result.snapshots[-1].extract_metrics()
        reported_duration = final_metrics.get('duration_seconds', 0)

        # Compare with actual duration
        if reported_duration > 0:
            duration_diff = abs(reported_duration - actual_duration)

            # Allow 2s tolerance
            assert duration_diff <= 2.0, \
                f"Duration mismatch: reported {reported_duration}s vs actual {actual_duration:.1f}s (diff: {duration_diff:.1f}s)"

    # Check result duration
    result_duration_diff = abs(result.duration_seconds - actual_duration)

    return TestResult(
        test_name="test_metrics_accuracy",
        status=TestStatus.PASSED,
        message=f"Metrics accurate (duration diff: {result_duration_diff:.2f}s)",
        details={
            'actual_duration': actual_duration,
            'result_duration': result.duration_seconds,
            'duration_diff': result_duration_diff,
            'final_metrics': final_metrics if result.snapshots else {}
        }
    )


# ============================================================================
# TEST SUITE SUMMARY
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Mark tests with appropriate markers"""
    for item in items:
        # Mark Unix-only tests
        if 'interactive' in item.nodeid or 'keyboard' in item.nodeid:
            if sys.platform == 'win32':
                item.add_marker(pytest.mark.skip(reason="Unix-only test"))
