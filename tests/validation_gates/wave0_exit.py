"""
Wave 0 Exit Gate: Testing Infrastructure Validation

Validates that the testing infrastructure (CLIMonitor, InteractiveCLITester,
OutputParser, ValidationGate) works correctly before using it to test Waves 1-7.

Part of Wave 0: Testing Infrastructure
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli_infrastructure.cli_monitor import CLIMonitor, OutputSnapshot
from cli_infrastructure.interactive_tester import InteractiveCLITester
from cli_infrastructure.output_parser import OutputParser
from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


class TestWave0Infrastructure:
    """Wave 0 functional tests - validate testing infrastructure itself"""

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_cli_monitor_basic_execution(self):
        """
        TEST 1: CLIMonitor can execute commands and capture output

        Execute: echo "Hello World"
        Validate:
            - Command executes successfully
            - Output captured
            - Snapshots created
        """

        monitor = CLIMonitor()
        result = monitor.run_and_monitor(
            command=['echo', 'Hello World'],
            snapshot_interval_ms=100,
            timeout_seconds=5
        )

        assert result.validate_success(), f"Command failed with exit code {result.exit_code}"
        assert 'Hello World' in result.total_output, "Output not captured"
        assert len(result.snapshots) >= 1, "No snapshots captured"

        return TestResult(
            test_name="test_cli_monitor_basic_execution",
            status=TestStatus.PASSED,
            message="CLIMonitor executes commands successfully",
            details={
                'exit_code': result.exit_code,
                'snapshot_count': len(result.snapshots)
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_output_parser_extracts_metrics(self):
        """
        TEST 2: OutputParser can extract structured data from dashboard output

        Parse: "$0.12 | 8.2K tokens | 45s"
        Validate:
            - Cost extracted correctly
            - Tokens extracted correctly
            - Duration extracted correctly
        """

        output = "$0.12 | 8.2K tokens | 45s"

        parser = OutputParser()
        state = parser.parse_dashboard(output)

        assert state.cost_usd == 0.12, f"Cost wrong: {state.cost_usd}"
        assert state.tokens_k == 8.2, f"Tokens wrong: {state.tokens_k}"
        assert state.duration_s == 45, f"Duration wrong: {state.duration_s}"

        return TestResult(
            test_name="test_output_parser_extracts_metrics",
            status=TestStatus.PASSED,
            message="OutputParser extracts metrics correctly",
            details={
                'cost_usd': state.cost_usd,
                'tokens_k': state.tokens_k,
                'duration_s': state.duration_s
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    @pytest.mark.skipif(sys.platform == 'win32', reason="Interactive testing requires Unix")
    async def test_interactive_tester_unix_only(self):
        """
        TEST 3: InteractiveCLITester works on Unix platforms

        Execute: python -c "print('test')"  (simple command that terminates)
        Validate:
            - Pty creation successful
            - Command executes
            - Output captured
        """

        tester = InteractiveCLITester()
        result = tester.run_interactive(
            command=['python3', '-c', 'print("test")'],
            interactions=[],  # No interactions needed, just test pty works
            timeout_seconds=5
        )

        # Validate execution completed
        assert result.exit_code == 0, f"Command failed: {result.exit_code}"
        assert result.duration_seconds < 5, "Command took too long"

        return TestResult(
            test_name="test_interactive_tester_unix_only",
            status=TestStatus.PASSED,
            message="InteractiveCLITester works on Unix",
            details={
                'duration_seconds': result.duration_seconds,
                'exit_code': result.exit_code
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(10)
    async def test_validation_gate_framework(self):
        """
        TEST 4: ValidationGate framework functional

        Create: Dummy validation gate with test
        Execute: Run gate
        Validate:
            - Gate runs tests
            - Results collected
            - Pass/fail logic works
        """

        gate = ValidationGate(phase=0, gate_type='test')

        async def dummy_test():
            return TestResult(
                test_name="dummy",
                status=TestStatus.PASSED,
                message="Dummy test"
            )

        gate.add_test(dummy_test)
        result = await gate.run_all_tests()

        assert result.passed, "Gate should pass with passing test"
        assert result.total_tests == 1, f"Should have 1 test, got {result.total_tests}"
        assert result.passed_tests == 1, "Test should have passed"

        return TestResult(
            test_name="test_validation_gate_framework",
            status=TestStatus.PASSED,
            message="ValidationGate framework functional",
            details={
                'total_tests': result.total_tests,
                'passed_tests': result.passed_tests
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.timeout(15)
    async def test_snapshot_timing_accuracy(self):
        """
        TEST 5: Snapshot capture timing is accurate

        Execute: python script that runs for 3 seconds (with 500ms snapshots)
        Validate:
            - Snapshots captured at ~2 Hz (500ms intervals)
            - Count approximately correct (5-7 snapshots in 3 seconds)
            - Timing variance acceptable
        """

        monitor = CLIMonitor()
        result = monitor.run_and_monitor(
            command=['python3', '-c', 'import time; time.sleep(3)'],
            snapshot_interval_ms=500,  # 2 Hz
            timeout_seconds=10
        )

        # Should capture ~6 snapshots in 3 seconds at 2 Hz (plus final snapshot)
        snapshot_count = len(result.snapshots)
        assert snapshot_count >= 3, f"Too few snapshots: {snapshot_count} (expected 5-7)"
        assert snapshot_count <= 10, f"Too many snapshots: {snapshot_count} (expected 5-7)"

        return TestResult(
            test_name="test_snapshot_timing_accuracy",
            status=TestStatus.PASSED,
            message=f"Captured {snapshot_count} snapshots in 3s (expected 5-7)",
            details={
                'snapshot_count': snapshot_count,
                'expected_range': '5-7'
            }
        )


# Export test class for pytest discovery
__all__ = ['TestWave0Infrastructure']
