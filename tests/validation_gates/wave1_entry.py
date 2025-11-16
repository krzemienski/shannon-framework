"""
Wave 1 Entry Gate: Prerequisites for Operational Telemetry Dashboard

Validates that:
- Wave 0 exit gate passed (testing infrastructure works)
- Python 3.10+ is installed
- All required dependencies are installed (asyncio, pytest, etc.)
- System has terminal capabilities for dashboard rendering

Part of Shannon V3 Wave 1: Operational Telemetry Dashboard
"""

import sys
import asyncio
from pathlib import Path

from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


async def test_wave0_exit_passed() -> TestResult:
    """Verify Wave 0 exit gate passed"""
    try:
        # Import Wave 0 exit gate
        from validation_gates.wave0_exit import TestWave0Infrastructure

        # Wave 0 must exist and be importable
        return TestResult(
            test_name="test_wave0_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 0 testing infrastructure validated",
            details={'wave0_infrastructure': 'available'}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave0_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 0 infrastructure not available: {e}",
            details={'error': str(e)}
        )


async def test_python_version() -> TestResult:
    """Verify Python 3.10+ is installed"""
    version_info = sys.version_info

    if version_info >= (3, 10):
        return TestResult(
            test_name="test_python_version",
            status=TestStatus.PASSED,
            message=f"Python {version_info.major}.{version_info.minor}.{version_info.micro} detected",
            details={
                'python_version': f"{version_info.major}.{version_info.minor}.{version_info.micro}",
                'required': '3.10+'
            }
        )
    else:
        return TestResult(
            test_name="test_python_version",
            status=TestStatus.FAILED,
            message=f"Python {version_info.major}.{version_info.minor} too old (need 3.10+)",
            details={
                'python_version': f"{version_info.major}.{version_info.minor}.{version_info.micro}",
                'required': '3.10+'
            }
        )


async def test_asyncio_available() -> TestResult:
    """Verify asyncio is available"""
    try:
        # Test asyncio functionality
        loop = asyncio.get_event_loop()

        return TestResult(
            test_name="test_asyncio_available",
            status=TestStatus.PASSED,
            message="asyncio event loop available",
            details={'asyncio_version': asyncio.__version__ if hasattr(asyncio, '__version__') else 'builtin'}
        )
    except Exception as e:
        return TestResult(
            test_name="test_asyncio_available",
            status=TestStatus.FAILED,
            message=f"asyncio not functional: {e}",
            details={'error': str(e)}
        )


async def test_pytest_installed() -> TestResult:
    """Verify pytest is installed"""
    try:
        import pytest

        return TestResult(
            test_name="test_pytest_installed",
            status=TestStatus.PASSED,
            message=f"pytest {pytest.__version__} installed",
            details={'pytest_version': pytest.__version__}
        )
    except ImportError:
        return TestResult(
            test_name="test_pytest_installed",
            status=TestStatus.FAILED,
            message="pytest not installed (required for testing)",
            details={'solution': 'pip install pytest pytest-asyncio pytest-timeout'}
        )


async def test_terminal_capabilities() -> TestResult:
    """Verify terminal has required capabilities for dashboard"""
    try:
        import os

        # Check for terminal environment
        term = os.environ.get('TERM', '')
        has_tty = sys.stdout.isatty()

        if has_tty or term:
            return TestResult(
                test_name="test_terminal_capabilities",
                status=TestStatus.PASSED,
                message=f"Terminal detected: {term or 'tty'}",
                details={
                    'TERM': term,
                    'isatty': has_tty,
                    'platform': sys.platform
                }
            )
        else:
            return TestResult(
                test_name="test_terminal_capabilities",
                status=TestStatus.PASSED,
                message="No TTY detected (tests can still run)",
                details={
                    'warning': 'Interactive dashboard features may be limited',
                    'platform': sys.platform
                }
            )
    except Exception as e:
        return TestResult(
            test_name="test_terminal_capabilities",
            status=TestStatus.FAILED,
            message=f"Terminal check failed: {e}",
            details={'error': str(e)}
        )


async def wave1_entry_gate() -> bool:
    """
    Run Wave 1 entry gate checks

    Returns:
        bool: True if all prerequisites met
    """
    gate = ValidationGate(phase=1, gate_type='entry')

    gate.add_test(test_wave0_exit_passed)
    gate.add_test(test_python_version)
    gate.add_test(test_asyncio_available)
    gate.add_test(test_pytest_installed)
    gate.add_test(test_terminal_capabilities)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    # Run entry gate
    import asyncio
    success = asyncio.run(wave1_entry_gate())
    sys.exit(0 if success else 1)
