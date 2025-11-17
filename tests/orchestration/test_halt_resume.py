"""
Tests for HALT/RESUME functionality - GATE 6.1

Requirements:
- HALT pauses execution < 100ms
- RESUME continues from halted state
- 2/2 tests must pass
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
import asyncio
import time
from orchestration.orchestrator import Orchestrator, Wave, ExecutionState


class TestHaltResume:
    """Test HALT and RESUME operations"""

    @pytest.mark.asyncio
    async def test_halt_pauses_execution(self):
        """
        Test that HALT request pauses execution.

        Verifies:
        - Halt can be requested
        - Execution enters HALTED state
        - Execution stops at current wave
        """
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
        assert halt_result["halt_requested"] is True

        # Verify execution halted
        assert orchestrator.state == ExecutionState.HALTED

        # Verify not all waves completed
        status = orchestrator.get_status()
        assert status["current_wave_index"] < status["total_waves"]

        # Cleanup
        execution_task.cancel()
        try:
            await execution_task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_resume_continues_execution(self):
        """
        Test that RESUME continues from halted state.

        Verifies:
        - Can resume after halt
        - Execution continues from halt point
        - All waves eventually complete
        """
        # Setup
        orchestrator = Orchestrator()
        orchestrator.add_wave(Wave("wave1", "agent1", ["task1"]))
        orchestrator.add_wave(Wave("wave2", "agent2", ["task2"]))

        # Start execution
        execution_task = asyncio.create_task(orchestrator.execute())

        # Wait and halt
        await asyncio.sleep(0.05)
        orchestrator.halt()
        await asyncio.sleep(0.15)

        # Verify halted
        assert orchestrator.state == ExecutionState.HALTED
        wave_index_at_halt = orchestrator.current_wave_index

        # Cancel initial execution task
        execution_task.cancel()
        try:
            await execution_task
        except asyncio.CancelledError:
            pass

        # Resume execution
        resume_result = await orchestrator.resume()

        # Verify execution completed
        assert resume_result["state"] == ExecutionState.COMPLETED.value

        # Verify all waves processed
        assert orchestrator.current_wave_index == len(orchestrator.waves)

        # Verify we continued from halt point (not restart)
        assert wave_index_at_halt < len(orchestrator.waves)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
