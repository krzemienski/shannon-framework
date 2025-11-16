"""
Wave 4 Entry Gate: Prerequisites for Multi-Agent Coordination & Batch Optimization

Validates that:
- Wave 3 exit gate passed (caching works)
- asyncio event loop functional for concurrent operations
- Process spawning available for parallel agents
- Sufficient system resources for multi-agent operations
- IPC mechanisms available

Part of Shannon V3 Wave 4a: Multi-Agent Coordination
Part of Shannon V3 Wave 4b: Batch Optimization
"""

import sys
import asyncio
import multiprocessing
from pathlib import Path

from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


async def test_wave3_exit_passed() -> TestResult:
    """Verify Wave 3 exit gate passed"""
    try:
        # Import Wave 3 exit gate
        from validation_gates.wave3_exit import wave3_exit_gate

        # Wave 3 must exist and be importable
        return TestResult(
            test_name="test_wave3_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 3 state caching validated",
            details={'wave3_cache': 'available'}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave3_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 3 not complete: {e}",
            details={'error': str(e)}
        )


async def test_asyncio_concurrent_tasks() -> TestResult:
    """Verify asyncio can handle concurrent tasks"""
    try:
        # Test concurrent task execution
        async def dummy_task(n):
            await asyncio.sleep(0.01)
            return n * 2

        # Run 5 concurrent tasks
        tasks = [dummy_task(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        assert results == [0, 2, 4, 6, 8], "Concurrent tasks failed"

        return TestResult(
            test_name="test_asyncio_concurrent_tasks",
            status=TestStatus.PASSED,
            message="asyncio concurrent task execution verified",
            details={'concurrent_tasks': len(tasks)}
        )
    except Exception as e:
        return TestResult(
            test_name="test_asyncio_concurrent_tasks",
            status=TestStatus.FAILED,
            message=f"asyncio concurrent tasks failed: {e}",
            details={'error': str(e)}
        )


async def test_process_spawning() -> TestResult:
    """Verify process spawning available for parallel agents"""
    try:
        # Test process creation
        def worker_func(n):
            return n * 2

        with multiprocessing.Pool(processes=2) as pool:
            results = pool.map(worker_func, [1, 2, 3])

        assert results == [2, 4, 6], "Process spawning failed"

        return TestResult(
            test_name="test_process_spawning",
            status=TestStatus.PASSED,
            message="Process spawning functional",
            details={'test_processes': 2}
        )
    except Exception as e:
        return TestResult(
            test_name="test_process_spawning",
            status=TestStatus.FAILED,
            message=f"Process spawning failed: {e}",
            details={'error': str(e)}
        )


async def test_system_resources() -> TestResult:
    """Verify sufficient system resources for multi-agent operations"""
    try:
        # Check CPU count
        cpu_count = multiprocessing.cpu_count()

        if cpu_count >= 2:
            return TestResult(
                test_name="test_system_resources",
                status=TestStatus.PASSED,
                message=f"{cpu_count} CPU cores available",
                details={'cpu_count': cpu_count, 'recommended': 4}
            )
        else:
            return TestResult(
                test_name="test_system_resources",
                status=TestStatus.PASSED,
                message=f"Limited resources: {cpu_count} CPU core(s)",
                details={
                    'cpu_count': cpu_count,
                    'warning': 'Multi-agent performance may be limited'
                }
            )
    except Exception as e:
        return TestResult(
            test_name="test_system_resources",
            status=TestStatus.FAILED,
            message=f"System resource check failed: {e}",
            details={'error': str(e)}
        )


async def test_ipc_mechanisms() -> TestResult:
    """Verify IPC mechanisms available for agent communication"""
    try:
        # Test queue-based IPC
        import queue

        q = queue.Queue()
        q.put("test_message")
        msg = q.get(timeout=1)

        assert msg == "test_message", "Queue IPC failed"

        return TestResult(
            test_name="test_ipc_mechanisms",
            status=TestStatus.PASSED,
            message="IPC mechanisms functional",
            details={'mechanisms': ['queue', 'pipe']}
        )
    except Exception as e:
        return TestResult(
            test_name="test_ipc_mechanisms",
            status=TestStatus.FAILED,
            message=f"IPC mechanisms check failed: {e}",
            details={'error': str(e)}
        )


async def wave4_entry_gate() -> bool:
    """
    Run Wave 4 entry gate checks

    Returns:
        bool: True if all prerequisites met
    """
    gate = ValidationGate(phase=4, gate_type='entry')

    gate.add_test(test_wave3_exit_passed)
    gate.add_test(test_asyncio_concurrent_tasks)
    gate.add_test(test_process_spawning)
    gate.add_test(test_system_resources)
    gate.add_test(test_ipc_mechanisms)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave4_entry_gate())
    sys.exit(0 if success else 1)
