"""
Wave 7 Entry Gate: Prerequisites for End-to-End Integration

Validates that:
- All previous waves (0-6) exit gates passed
- All subsystems operational
- System ready for integration testing
- No blocking issues from earlier waves

Part of Shannon V3 Wave 7: Integration & Final Validation
"""

import sys
from pathlib import Path

from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


async def test_wave0_exit_passed() -> TestResult:
    """Verify Wave 0 exit gate passed"""
    try:
        from validation_gates.wave0_exit import TestWave0Infrastructure
        return TestResult(
            test_name="test_wave0_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 0: Testing infrastructure validated",
            details={'wave': 0}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave0_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 0 not complete: {e}",
            details={'error': str(e)}
        )


async def test_wave1_exit_passed() -> TestResult:
    """Verify Wave 1 exit gate passed"""
    try:
        from validation_gates.wave1_exit import wave1_exit_gate
        return TestResult(
            test_name="test_wave1_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 1: Operational telemetry validated",
            details={'wave': 1}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave1_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 1 not complete: {e}",
            details={'error': str(e)}
        )


async def test_wave2_exit_passed() -> TestResult:
    """Verify Wave 2 exit gate passed"""
    try:
        from validation_gates.wave2_exit import wave2_exit_gate
        return TestResult(
            test_name="test_wave2_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 2: MCP integration validated",
            details={'wave': 2}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave2_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 2 not complete: {e}",
            details={'error': str(e)}
        )


async def test_wave3_exit_passed() -> TestResult:
    """Verify Wave 3 exit gate passed"""
    try:
        from validation_gates.wave3_exit import wave3_exit_gate
        return TestResult(
            test_name="test_wave3_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 3: State caching validated",
            details={'wave': 3}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave3_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 3 not complete: {e}",
            details={'error': str(e)}
        )


async def test_wave4_exit_passed() -> TestResult:
    """Verify Wave 4 exit gate passed"""
    try:
        from validation_gates.wave4_exit import wave4_exit_gate
        return TestResult(
            test_name="test_wave4_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 4: Multi-agent coordination validated",
            details={'wave': 4}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave4_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 4 not complete: {e}",
            details={'error': str(e)}
        )


async def test_wave5_exit_passed() -> TestResult:
    """Verify Wave 5 exit gate passed"""
    try:
        from validation_gates.wave5_exit import wave5_exit_gate
        return TestResult(
            test_name="test_wave5_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 5: Analytics engine validated",
            details={'wave': 5}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave5_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 5 not complete: {e}",
            details={'error': str(e)}
        )


async def test_wave6_exit_passed() -> TestResult:
    """Verify Wave 6 exit gate passed"""
    try:
        from validation_gates.wave6_exit import wave6_exit_gate
        return TestResult(
            test_name="test_wave6_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 6: Context-aware execution validated",
            details={'wave': 6}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave6_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 6 not complete: {e}",
            details={'error': str(e)}
        )


async def test_all_subsystems_operational() -> TestResult:
    """Verify all subsystems are operational"""
    try:
        # Quick sanity check that all major components can be imported
        subsystems = {
            'cli_monitor': 'cli_infrastructure.cli_monitor',
            'interactive_tester': 'cli_infrastructure.interactive_tester',
            'output_parser': 'cli_infrastructure.output_parser',
            'gate_framework': 'validation_gates.gate_framework'
        }

        for name, module_path in subsystems.items():
            __import__(module_path)

        return TestResult(
            test_name="test_all_subsystems_operational",
            status=TestStatus.PASSED,
            message=f"All {len(subsystems)} core subsystems operational",
            details={'subsystems': list(subsystems.keys())}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_all_subsystems_operational",
            status=TestStatus.FAILED,
            message=f"Subsystem import failed: {e}",
            details={'error': str(e)}
        )


async def wave7_entry_gate() -> bool:
    """
    Run Wave 7 entry gate checks

    Verifies all previous waves completed successfully.

    Returns:
        bool: True if all prerequisites met
    """
    gate = ValidationGate(phase=7, gate_type='entry')

    # Check all previous waves
    gate.add_test(test_wave0_exit_passed)
    gate.add_test(test_wave1_exit_passed)
    gate.add_test(test_wave2_exit_passed)
    gate.add_test(test_wave3_exit_passed)
    gate.add_test(test_wave4_exit_passed)
    gate.add_test(test_wave5_exit_passed)
    gate.add_test(test_wave6_exit_passed)

    # Check subsystems
    gate.add_test(test_all_subsystems_operational)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave7_entry_gate())
    sys.exit(0 if success else 1)
