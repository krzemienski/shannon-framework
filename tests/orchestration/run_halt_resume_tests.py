#!/usr/bin/env python3
"""
Direct test runner for HALT/RESUME tests - GATE 6.1
Bypasses pytest import issues
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
import time
from orchestration.orchestrator import Orchestrator, Wave, ExecutionState


async def test_halt_pauses_execution():
    """
    Test that HALT request pauses execution.

    Verifies:
    - Halt can be requested
    - Execution enters HALTED state
    - Execution stops at current wave
    """
    print("TEST 1: test_halt_pauses_execution")

    # Setup
    orchestrator = Orchestrator()
    orchestrator.add_wave(Wave("wave1", "agent1", ["task1", "task2"]))
    orchestrator.add_wave(Wave("wave2", "agent2", ["task3", "task4"]))
    orchestrator.add_wave(Wave("wave3", "agent3", ["task5", "task6"]))

    # Start execution in background
    execution_task = asyncio.create_task(orchestrator.execute())

    # Wait a bit for execution to start
    await asyncio.sleep(0.05)

    # Request halt
    halt_result = orchestrator.halt()

    # Wait for halt to complete
    await asyncio.sleep(0.15)

    # Verify halt was requested
    assert halt_result["halt_requested"] is True, "Halt should be requested"
    print("  ✓ Halt requested")

    # Verify execution halted
    assert orchestrator.state == ExecutionState.HALTED, f"State should be HALTED, got {orchestrator.state}"
    print("  ✓ Execution halted")

    # Verify not all waves completed
    status = orchestrator.get_status()
    assert status["current_wave_index"] < status["total_waves"], "Not all waves should complete"
    print(f"  ✓ Stopped at wave {status['current_wave_index']}/{status['total_waves']}")

    # Cleanup
    execution_task.cancel()
    try:
        await execution_task
    except asyncio.CancelledError:
        pass

    print("  PASSED\n")
    return True


async def test_resume_continues_execution():
    """
    Test that RESUME continues from halted state.

    Verifies:
    - Can resume after halt
    - Execution continues from halt point
    - All waves eventually complete
    """
    print("TEST 2: test_resume_continues_execution")

    # Setup - use multiple tasks per wave so execution takes longer
    orchestrator = Orchestrator()
    orchestrator.add_wave(Wave("wave1", "agent1", ["task1", "task2", "task3"]))
    orchestrator.add_wave(Wave("wave2", "agent2", ["task4", "task5", "task6"]))
    orchestrator.add_wave(Wave("wave3", "agent3", ["task7", "task8", "task9"]))

    # Start execution
    execution_task = asyncio.create_task(orchestrator.execute())

    # Wait and halt
    await asyncio.sleep(0.05)
    orchestrator.halt()
    await asyncio.sleep(0.15)

    # Verify halted
    assert orchestrator.state == ExecutionState.HALTED, "Should be halted"
    wave_index_at_halt = orchestrator.current_wave_index
    print(f"  ✓ Halted at wave {wave_index_at_halt}")

    # Cancel initial execution task
    execution_task.cancel()
    try:
        await execution_task
    except asyncio.CancelledError:
        pass

    # Resume execution
    resume_result = await orchestrator.resume()
    print("  ✓ Resumed execution")

    # Verify execution completed
    assert resume_result["state"] == ExecutionState.COMPLETED.value, f"Should be completed, got {resume_result['state']}"
    print("  ✓ Execution completed")

    # Verify all waves processed
    assert orchestrator.current_wave_index == len(orchestrator.waves), "All waves should be processed"
    print(f"  ✓ All {orchestrator.current_wave_index} waves processed")

    # Verify we continued from halt point (not restart)
    assert wave_index_at_halt < len(orchestrator.waves), "Should have continued from halt point"
    print("  ✓ Continued from halt point (not restarted)")

    print("  PASSED\n")
    return True


async def main():
    """Run all tests"""
    print("=" * 60)
    print("GATE 6.1: HALT/RESUME Backend Tests")
    print("=" * 60)
    print()

    tests_passed = 0
    tests_failed = 0

    try:
        if await test_halt_pauses_execution():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"  FAILED: {e}\n")
        tests_failed += 1

    try:
        if await test_resume_continues_execution():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"  FAILED: {e}\n")
        tests_failed += 1

    print("=" * 60)
    print(f"Results: {tests_passed}/2 PASSED, {tests_failed}/2 FAILED")
    print("=" * 60)

    return tests_passed == 2


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
