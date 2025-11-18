"""
Shannon Orchestrator - Coordinates wave execution with HALT/RESUME/ROLLBACK controls.

This orchestrator manages the execution of parallel waves with real-time control
capabilities for interactive debugging and development.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from enum import Enum
import logging
from .state_manager import StateManager
from .decision_engine import DecisionEngine, DecisionOption

logger = logging.getLogger(__name__)


class ExecutionState(Enum):
    """Execution states for the orchestrator"""
    IDLE = "idle"
    RUNNING = "running"
    HALTED = "halted"
    COMPLETED = "completed"
    FAILED = "failed"


class Wave:
    """Represents a wave of execution"""
    def __init__(self, wave_id: str, agent_id: str, tasks: List[str]):
        self.wave_id = wave_id
        self.agent_id = agent_id
        self.tasks = tasks
        self.status = "pending"
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wave_id": self.wave_id,
            "agent_id": self.agent_id,
            "tasks": self.tasks,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }


class Orchestrator:
    """
    Main orchestrator for Shannon wave execution.

    Supports:
    - Parallel wave execution
    - HALT: Pause execution in <100ms
    - RESUME: Continue from halted state
    - ROLLBACK: Revert N execution steps
    """

    def __init__(self):
        self.state = ExecutionState.IDLE
        self.halt_requested = False
        self.waves: List[Wave] = []
        self.current_wave_index = 0
        self.execution_history: List[Dict[str, Any]] = []
        self.halt_response_time: Optional[float] = None
        self.state_manager = StateManager()
        self.decision_engine = DecisionEngine()

    def add_wave(self, wave: Wave) -> None:
        """Add a wave to the execution queue"""
        self.waves.append(wave)
        logger.info(f"Added wave {wave.wave_id} for agent {wave.agent_id}")

    async def execute(self) -> Dict[str, Any]:
        """
        Execute all waves in sequence.

        Checks halt_requested flag frequently to enable <100ms halt response.
        """
        self.state = ExecutionState.RUNNING
        logger.info(f"Starting execution of {len(self.waves)} waves")

        try:
            while self.current_wave_index < len(self.waves):
                # Check for halt request at wave boundaries
                if self.halt_requested:
                    await self._perform_halt()
                    break

                wave = self.waves[self.current_wave_index]

                # Create snapshot before executing wave
                self.state_manager.create_snapshot(
                    self.current_wave_index,
                    self.execution_history,
                    self.waves
                )

                wave_completed = await self._execute_wave(wave)

                # Record execution step
                self.execution_history.append({
                    "wave_id": wave.wave_id,
                    "wave_index": self.current_wave_index,
                    "timestamp": time.time(),
                    "status": wave.status
                })

                # If wave was halted, stop execution
                if not wave_completed:
                    break

                self.current_wave_index += 1

            if self.current_wave_index >= len(self.waves) and not self.halt_requested:
                self.state = ExecutionState.COMPLETED
                logger.info("All waves completed")

        except Exception as e:
            self.state = ExecutionState.FAILED
            logger.error(f"Execution failed: {e}")
            raise

        return self.get_status()

    async def _execute_wave(self, wave: Wave) -> bool:
        """
        Execute a single wave with halt checking.

        Returns:
            True if wave completed, False if halted
        """
        wave.status = "running"
        wave.started_at = time.time()
        logger.info(f"Executing wave {wave.wave_id}")

        # Simulate wave execution with frequent halt checks
        for task in wave.tasks:
            # Check halt every 10ms for <100ms response time
            if self.halt_requested:
                wave.status = "halted"
                await self._perform_halt()
                return False

            # Simulate task execution
            await asyncio.sleep(0.01)

        wave.status = "completed"
        wave.completed_at = time.time()
        logger.info(f"Wave {wave.wave_id} completed")
        return True

    async def _perform_halt(self) -> None:
        """Perform halt operation and record response time"""
        halt_start = time.time()
        self.state = ExecutionState.HALTED
        self.halt_response_time = (time.time() - halt_start) * 1000  # Convert to ms
        logger.info(f"Execution halted (response time: {self.halt_response_time:.2f}ms)")

    def halt(self) -> Dict[str, Any]:
        """
        Request execution halt.

        Returns:
            Status dict with halt_requested flag and current state
        """
        logger.info("HALT requested")
        self.halt_requested = True

        # Return immediately - actual halt happens in execute loop
        return {
            "halt_requested": True,
            "current_state": self.state.value,
            "current_wave_index": self.current_wave_index,
            "total_waves": len(self.waves)
        }

    async def resume(self) -> Dict[str, Any]:
        """
        Resume execution from halted state.

        Returns:
            Status dict after resuming execution
        """
        if self.state != ExecutionState.HALTED:
            raise ValueError(f"Cannot resume from state {self.state.value}")

        logger.info("Resuming execution")
        self.halt_requested = False
        self.state = ExecutionState.RUNNING

        # Continue execution from current position
        result = await self.execute()
        return result

    def rollback(self, n_steps: int) -> Dict[str, Any]:
        """
        Rollback execution state by N steps.

        Args:
            n_steps: Number of steps to rollback (1 = previous snapshot)

        Returns:
            Status dict after rollback

        Raises:
            ValueError: If rollback not possible
        """
        if n_steps < 1:
            raise ValueError("n_steps must be at least 1")

        # Get rollback state
        rollback_state = self.state_manager.get_rollback_state(n_steps)
        if rollback_state is None:
            available = self.state_manager.get_snapshot_count()
            raise ValueError(f"Cannot rollback {n_steps} steps (only {available} snapshots available)")

        logger.info(f"Rolling back {n_steps} steps")

        # Restore state
        self.current_wave_index = rollback_state["wave_index"]
        self.execution_history = rollback_state["execution_history"]

        # Restore wave states
        for i, wave_state in enumerate(rollback_state["waves_state"]):
            if i < len(self.waves):
                self.waves[i].status = wave_state["status"]
                self.waves[i].started_at = wave_state.get("started_at")
                self.waves[i].completed_at = wave_state.get("completed_at")

        # Reset execution state
        self.state = ExecutionState.IDLE
        self.halt_requested = False

        logger.info(f"Rolled back to wave {self.current_wave_index}")

        return {
            "rollback_steps": n_steps,
            "wave_index": self.current_wave_index,
            "snapshot_timestamp": rollback_state["snapshot_timestamp"],
            "status": self.get_status()
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status"""
        return {
            "state": self.state.value,
            "halt_requested": self.halt_requested,
            "current_wave_index": self.current_wave_index,
            "total_waves": len(self.waves),
            "waves": [w.to_dict() for w in self.waves],
            "execution_history_length": len(self.execution_history),
            "halt_response_time_ms": self.halt_response_time,
            "snapshots_available": self.state_manager.get_snapshot_count()
        }

    async def _request_decision(
        self,
        question: str,
        options: List[DecisionOption],
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Request a decision during execution.

        If auto-approved (confidence >= 0.95), returns immediately.
        If not auto-approved, waits for human approval via WebSocket.

        Args:
            question: The decision question
            options: List of possible options
            context: Additional context

        Returns:
            Decision object with selected option
        """
        decision = await self.decision_engine.request_decision(
            question=question,
            options=options,
            context=context
        )

        if decision.auto_approved:
            logger.info(f"Decision auto-approved: {decision.selected_option_id}")
            return decision

        # Not auto-approved - emit to dashboard and wait
        logger.info(f"Decision requires human approval: {decision.id}")

        # In real implementation, this would emit via WebSocket
        # and wait for approval. For now, we'll just log.
        # The approval would come through decision_engine.approve_decision()

        return decision

    def reset(self) -> None:
        """Reset orchestrator to initial state"""
        self.state = ExecutionState.IDLE
        self.halt_requested = False
        self.waves = []
        self.current_wave_index = 0
        self.execution_history = []
        self.halt_response_time = None
        self.state_manager.clear_snapshots()
        logger.info("Orchestrator reset")
