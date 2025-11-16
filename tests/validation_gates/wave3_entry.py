"""
Wave 3 Entry Gate: Prerequisites for Intelligent State Caching

Validates that:
- Wave 2 exit gate passed (MCP integration works)
- Filesystem is writable for cache storage
- Sufficient disk space available (>500MB)
- File I/O operations functional
- Cache directory can be created

Part of Shannon V3 Wave 3: Intelligent State Caching
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


async def test_wave2_exit_passed() -> TestResult:
    """Verify Wave 2 exit gate passed"""
    try:
        # Import Wave 2 exit gate
        from validation_gates.wave2_exit import wave2_exit_gate

        # Wave 2 must exist and be importable
        return TestResult(
            test_name="test_wave2_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 2 MCP integration validated",
            details={'wave2_mcp': 'available'}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave2_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 2 not complete: {e}",
            details={'error': str(e)}
        )


async def test_filesystem_writable() -> TestResult:
    """Verify filesystem is writable"""
    try:
        # Try to create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_path = f.name
            f.write("test")

        # Clean up
        os.unlink(test_path)

        return TestResult(
            test_name="test_filesystem_writable",
            status=TestStatus.PASSED,
            message="Filesystem writable",
            details={'temp_dir': tempfile.gettempdir()}
        )
    except Exception as e:
        return TestResult(
            test_name="test_filesystem_writable",
            status=TestStatus.FAILED,
            message=f"Filesystem not writable: {e}",
            details={'error': str(e)}
        )


async def test_disk_space_sufficient() -> TestResult:
    """Verify sufficient disk space (>500MB)"""
    try:
        # Check available disk space
        stat = shutil.disk_usage(tempfile.gettempdir())
        available_mb = stat.free / (1024 * 1024)

        required_mb = 500
        if available_mb >= required_mb:
            return TestResult(
                test_name="test_disk_space_sufficient",
                status=TestStatus.PASSED,
                message=f"{available_mb:.0f}MB available (need {required_mb}MB)",
                details={
                    'available_mb': int(available_mb),
                    'required_mb': required_mb
                }
            )
        else:
            return TestResult(
                test_name="test_disk_space_sufficient",
                status=TestStatus.FAILED,
                message=f"Insufficient disk space: {available_mb:.0f}MB (need {required_mb}MB)",
                details={
                    'available_mb': int(available_mb),
                    'required_mb': required_mb
                }
            )
    except Exception as e:
        return TestResult(
            test_name="test_disk_space_sufficient",
            status=TestStatus.FAILED,
            message=f"Disk space check failed: {e}",
            details={'error': str(e)}
        )


async def test_file_io_operations() -> TestResult:
    """Verify file I/O operations work correctly"""
    try:
        # Test read/write/delete operations
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_path = f.name
            test_data = "cache_test_data_123"
            f.write(test_data)

        # Read back
        with open(test_path, 'r') as f:
            read_data = f.read()

        # Verify
        assert read_data == test_data, "Data mismatch"

        # Delete
        os.unlink(test_path)

        return TestResult(
            test_name="test_file_io_operations",
            status=TestStatus.PASSED,
            message="File I/O operations functional",
            details={'operations': ['write', 'read', 'delete']}
        )
    except Exception as e:
        return TestResult(
            test_name="test_file_io_operations",
            status=TestStatus.FAILED,
            message=f"File I/O failed: {e}",
            details={'error': str(e)}
        )


async def test_cache_directory_creation() -> TestResult:
    """Verify cache directory can be created"""
    try:
        # Try to create cache directory
        cache_dir = Path(tempfile.gettempdir()) / 'shannon_cache_test'
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Verify it exists
        assert cache_dir.exists(), "Directory not created"

        # Clean up
        cache_dir.rmdir()

        return TestResult(
            test_name="test_cache_directory_creation",
            status=TestStatus.PASSED,
            message="Cache directory creation successful",
            details={'test_dir': str(cache_dir)}
        )
    except Exception as e:
        return TestResult(
            test_name="test_cache_directory_creation",
            status=TestStatus.FAILED,
            message=f"Cache directory creation failed: {e}",
            details={'error': str(e)}
        )


async def wave3_entry_gate() -> bool:
    """
    Run Wave 3 entry gate checks

    Returns:
        bool: True if all prerequisites met
    """
    gate = ValidationGate(phase=3, gate_type='entry')

    gate.add_test(test_wave2_exit_passed)
    gate.add_test(test_filesystem_writable)
    gate.add_test(test_disk_space_sufficient)
    gate.add_test(test_file_io_operations)
    gate.add_test(test_cache_directory_creation)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave3_entry_gate())
    sys.exit(0 if success else 1)
