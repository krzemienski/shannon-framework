#!/usr/bin/env python3
"""
Direct test runner for ROLLBACK tests - GATE 6.2
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import asyncio
from orchestration.orchestrator import Orchestrator, Wave, ExecutionState


async def test_snapshot_creation():
    """
    Test that snapshots are created during execution.

    Verifies:
    - Snapshots created after each wave
    - Snapshot contains correct state
    - Multiple snapshots accumulate
    """
    print("TEST 1: test_snapshot_creation")

    # Setup
    orchestrator = Orchestrator()
    orchestrator.add_wave(Wave("wave1", "agent1", ["task1"]))
    orchestrator.add_wave(Wave("wave2", "agent2", ["task2"]))
    orchestrator.add_wave(Wave("wave3", "agent3", ["task3"]))

    # Execute all waves
    await orchestrator.execute()

    # Verify snapshots were created
    status = orchestrator.get_status()
    snapshots_count = status["snapshots_available"]

    assert snapshots_count >= 3, f"Should have at least 3 snapshots, got {snapshots_count}"
    print(f"  ✓ Created {snapshots_count} snapshots")

    # Verify execution completed
    assert status["state"] == "completed", f"Should be completed, got {status['state']}"
    print("  ✓ Execution completed")

    print("  PASSED\n")
    return True


async def test_rollback_reverts_state():
    """
    Test that rollback reverts execution state.

    Verifies:
    - Can rollback N steps
    - Wave index reverts correctly
    - Execution history reverts
    - Can continue from rollback point
    """
    print("TEST 2: test_rollback_reverts_state")

    # Setup
    orchestrator = Orchestrator()
    orchestrator.add_wave(Wave("wave1", "agent1", ["task1"]))
    orchestrator.add_wave(Wave("wave2", "agent2", ["task2"]))
    orchestrator.add_wave(Wave("wave3", "agent3", ["task3"]))

    # Execute all waves
    await orchestrator.execute()

    final_wave_index = orchestrator.current_wave_index
    final_history_length = len(orchestrator.execution_history)

    print(f"  Before rollback: wave_index={final_wave_index}, history_length={final_history_length}")

    # Rollback 2 steps
    rollback_result = orchestrator.rollback(2)

    # Verify rollback occurred
    assert rollback_result["rollback_steps"] == 2, "Should rollback 2 steps"
    print("  ✓ Rollback executed")

    # Verify wave index reverted
    current_wave_index = orchestrator.current_wave_index
    assert current_wave_index < final_wave_index, f"Wave index should revert: {current_wave_index} < {final_wave_index}"
    print(f"  ✓ Wave index reverted to {current_wave_index}")

    # Verify history reverted
    current_history_length = len(orchestrator.execution_history)
    assert current_history_length < final_history_length, f"History should revert: {current_history_length} < {final_history_length}"
    print(f"  ✓ History reverted to {current_history_length} entries")

    # Verify state is IDLE (ready to continue)
    assert orchestrator.state == ExecutionState.IDLE, f"Should be IDLE, got {orchestrator.state}"
    print("  ✓ State is IDLE (ready to continue)")

    # Verify we can continue execution from rollback point
    await orchestrator.execute()
    assert orchestrator.state == ExecutionState.COMPLETED, "Should complete after rollback"
    print("  ✓ Can continue execution from rollback point")

    print("  PASSED\n")
    return True


async def main():
    """Run all tests"""
    print("=" * 60)
    print("GATE 6.2: ROLLBACK Backend Tests")
    print("=" * 60)
    print()

    tests_passed = 0
    tests_failed = 0

    try:
        if await test_snapshot_creation():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"  FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        tests_failed += 1

    try:
        if await test_rollback_reverts_state():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"  FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        tests_failed += 1

    print("=" * 60)
    print(f"Results: {tests_passed}/2 PASSED, {tests_failed}/2 FAILED")
    print("=" * 60)

    return tests_passed == 2


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
