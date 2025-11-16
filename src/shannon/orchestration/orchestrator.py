"""Shannon Orchestration - Main Orchestrator

The Orchestrator ties everything together by:
- Parsing tasks with TaskParser
- Creating plans with ExecutionPlanner
- Executing skills in order
- Creating checkpoints via StateManager
- Handling HALT/RESUME via WebSocket
- Streaming events to dashboard

This is the main entry point for the `shannon do` command.

Example:
    orchestrator = Orchestrator(plan, executor, state_manager, event_bus)

    result = await orchestrator.execute()
    # Executes plan with checkpoints and event streaming
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable
from enum import Enum

from shannon.skills.executor import SkillExecutor
from shannon.skills.models import SkillResult, ExecutionContext
from shannon.orchestration.planner import ExecutionPlan, SkillStep
from shannon.orchestration.state_manager import StateManager, Checkpoint
from shannon.server.websocket import emit_skill_event, emit_execution_event

logger = logging.getLogger(__name__)


class ExecutionState(Enum):
    """Orchestrator execution state"""
    IDLE = "idle"
    RUNNING = "running"
    HALTED = "halted"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class OrchestratorResult:
    """Result of orchestrator execution"""
    success: bool
    plan_id: str
    steps_completed: int
    steps_total: int
    checkpoints_created: List[str]
    duration_seconds: float
    error: Optional[str] = None
    results: List[SkillResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'success': self.success,
            'plan_id': self.plan_id,
            'steps_completed': self.steps_completed,
            'steps_total': self.steps_total,
            'checkpoints_created': self.checkpoints_created,
            'duration_seconds': self.duration_seconds,
            'error': self.error,
            'results': [r.to_dict() for r in self.results]
        }


class OrchestratorError(Exception):
    """Base exception for orchestrator errors"""
    pass


class Orchestrator:
    """
    Main orchestrator for executing execution plans.

    The Orchestrator coordinates:
    1. Skill execution via SkillExecutor
    2. Checkpoint creation via StateManager
    3. Event emission for real-time monitoring
    4. HALT/RESUME handling
    5. Error recovery and rollback

    Supports:
    - Sequential execution (default)
    - Parallel execution (future enhancement)
    - Interactive decision points
    - Real-time dashboard streaming
    - Rollback on failure

    Usage:
        orchestrator = Orchestrator(
            plan=execution_plan,
            executor=skill_executor,
            state_manager=state_manager,
            session_id="session_123"
        )

        result = await orchestrator.execute()
    """

    def __init__(
        self,
        plan: ExecutionPlan,
        executor: SkillExecutor,
        state_manager: StateManager,
        session_id: Optional[str] = None,
        event_callback: Optional[Callable] = None,
        dashboard_url: Optional[str] = None
    ):
        """
        Initialize orchestrator.

        Args:
            plan: ExecutionPlan to execute
            executor: SkillExecutor for running skills
            state_manager: StateManager for checkpoints
            session_id: Optional session ID for event routing
            event_callback: Optional callback for event emission
            dashboard_url: Optional dashboard server URL for event streaming
        """
        self.plan = plan
        self.executor = executor
        self.state_manager = state_manager
        self.session_id = session_id
        self.event_callback = event_callback

        # Execution state
        self.state = ExecutionState.IDLE
        self.state_lock = asyncio.Lock()
        self.halt_event = asyncio.Event()
        self.halt_event.set()  # Not halted initially

        # Tracking
        self.current_step = 0
        self.checkpoints_created: List[str] = []
        self.execution_context = ExecutionContext(task=plan.task)

        # Dashboard client for event streaming
        self.dashboard_client = None
        if session_id and dashboard_url:
            from shannon.communication.dashboard_client import DashboardEventClient
            self.dashboard_client = DashboardEventClient(dashboard_url, session_id)
            logger.info(f"Dashboard client created for session: {session_id}")

        logger.info(f"Orchestrator initialized: {plan.plan_id}, {len(plan.steps)} steps")

    async def execute(self) -> OrchestratorResult:
        """
        Execute the complete plan.

        Returns:
            OrchestratorResult with execution details

        Raises:
            OrchestratorError: If execution fails critically
        """
        start_time = datetime.now()

        async with self.state_lock:
            if self.state != ExecutionState.IDLE:
                raise OrchestratorError(f"Cannot execute - state is {self.state.value}")
            self.state = ExecutionState.RUNNING

        # Connect to dashboard server if client configured
        if self.dashboard_client:
            connected = await self.dashboard_client.connect()
            if connected:
                logger.info("Dashboard client connected successfully")
            else:
                logger.warning("Dashboard client connection failed - continuing without dashboard")

        logger.info(f"Starting execution: plan={self.plan.plan_id}, steps={len(self.plan.steps)}")

        await self._emit_event('execution:started', {
            'plan_id': self.plan.plan_id,
            'task': self.plan.task,
            'steps_total': len(self.plan.steps)
        })

        try:
            # Execute each step
            for i, step in enumerate(self.plan.steps):
                self.current_step = i

                # Check for halt
                await self._check_halt()

                # Create checkpoint if needed
                if step.checkpoint_before:
                    await self._create_checkpoint(step)

                # Execute skill
                await self._execute_step(step, i)

            # Execution completed successfully
            async with self.state_lock:
                self.state = ExecutionState.COMPLETED

            duration = (datetime.now() - start_time).total_seconds()

            result = OrchestratorResult(
                success=True,
                plan_id=self.plan.plan_id,
                steps_completed=len(self.plan.steps),
                steps_total=len(self.plan.steps),
                checkpoints_created=self.checkpoints_created,
                duration_seconds=duration,
                results=self.execution_context.skill_results
            )

            # Emit completion with safe serialization
            try:
                completion_data = {
                    'success': result.success,
                    'plan_id': result.plan_id,
                    'steps_completed': result.steps_completed,
                    'steps_total': result.steps_total,
                    'duration_seconds': result.duration_seconds,
                    # Skip results list - may contain non-serializable data
                }
                await self._emit_event('execution:completed', completion_data)
            except Exception as e:
                logger.warning(f"Failed to emit execution:completed: {e}")
                # At least emit minimal completion
                await self._emit_event('execution:completed', {
                    'success': result.success,
                    'steps_completed': result.steps_completed
                })

            logger.info(
                f"Execution completed: {result.steps_completed}/{result.steps_total} steps, "
                f"{len(result.checkpoints_created)} checkpoints, {duration:.1f}s"
            )

            return result

        except Exception as e:
            # Execution failed
            async with self.state_lock:
                self.state = ExecutionState.FAILED

            duration = (datetime.now() - start_time).total_seconds()

            result = OrchestratorResult(
                success=False,
                plan_id=self.plan.plan_id,
                steps_completed=self.current_step,
                steps_total=len(self.plan.steps),
                checkpoints_created=self.checkpoints_created,
                duration_seconds=duration,
                error=str(e),
                results=self.execution_context.skill_results
            )

            await self._emit_event('execution:failed', {
                **result.to_dict(),
                'error': str(e)
            })

            logger.error(f"Execution failed at step {self.current_step}: {e}", exc_info=True)

            return result

        finally:
            # Disconnect dashboard client
            if self.dashboard_client:
                await self.dashboard_client.disconnect()
                logger.info("Dashboard client disconnected")

    async def halt(self, reason: str = "User requested"):
        """
        Halt execution (pause).

        Args:
            reason: Reason for halt
        """
        async with self.state_lock:
            if self.state != ExecutionState.RUNNING:
                logger.warning(f"Cannot halt - state is {self.state.value}")
                return

            self.state = ExecutionState.HALTED
            self.halt_event.clear()  # Block execution

        await self._emit_event('execution:halted', {
            'reason': reason,
            'current_step': self.current_step,
            'steps_total': len(self.plan.steps)
        })

        logger.info(f"Execution halted: {reason}")

    async def resume(self):
        """Resume halted execution"""
        async with self.state_lock:
            if self.state != ExecutionState.HALTED:
                logger.warning(f"Cannot resume - state is {self.state.value}")
                return

            self.state = ExecutionState.RUNNING
            self.halt_event.set()  # Unblock execution

        await self._emit_event('execution:resumed', {
            'current_step': self.current_step,
            'steps_remaining': len(self.plan.steps) - self.current_step
        })

        logger.info("Execution resumed")

    async def rollback(self, checkpoint_id: str):
        """
        Rollback to checkpoint.

        Args:
            checkpoint_id: ID of checkpoint to restore
        """
        logger.info(f"Rolling back to checkpoint: {checkpoint_id}")

        await self._emit_event('execution:rollback_started', {
            'checkpoint_id': checkpoint_id,
            'current_step': self.current_step
        })

        try:
            # Restore checkpoint
            await self.state_manager.restore_checkpoint(checkpoint_id)

            await self._emit_event('execution:rollback_completed', {
                'checkpoint_id': checkpoint_id
            })

            logger.info("Rollback completed successfully")

        except Exception as e:
            logger.error(f"Rollback failed: {e}", exc_info=True)

            await self._emit_event('execution:rollback_failed', {
                'checkpoint_id': checkpoint_id,
                'error': str(e)
            })

            raise

    async def _execute_step(self, step: SkillStep, step_index: int):
        """
        Execute a single skill step.

        Args:
            step: SkillStep to execute
            step_index: Index of step in plan
        """
        logger.info(
            f"Executing step {step_index + 1}/{len(self.plan.steps)}: {step.skill_name}"
        )

        await self._emit_event('skill:started', {
            'skill_name': step.skill_name,
            'step_index': step_index,
            'parameters': step.parameters
        })

        # Get skill from registry
        skill = self.executor.registry.get(step.skill_name)
        if skill is None:
            raise Exception(f"Skill not found: {step.skill_name}")

        # Execute skill
        result = await self.executor.execute(
            skill=skill,
            parameters=step.parameters,
            context=self.execution_context
        )

        # Add result to context
        self.execution_context.add_result(result)

        # Emit result event
        if result.success:
            await self._emit_event('skill:completed', {
                'skill_name': step.skill_name,
                'step_index': step_index,
                'duration': result.duration
            })
        else:
            await self._emit_event('skill:failed', {
                'skill_name': step.skill_name,
                'step_index': step_index,
                'error': result.error
            })

            # If critical skill fails, stop execution
            if step.critical:
                raise OrchestratorError(
                    f"Critical skill {step.skill_name} failed: {result.error}"
                )

    async def _create_checkpoint(self, step: SkillStep):
        """
        Create checkpoint before step.

        Args:
            step: Step to create checkpoint before
        """
        label = f"before_{step.skill_name}"

        logger.info(f"Creating checkpoint: {label}")

        checkpoint = await self.state_manager.create_checkpoint(
            label=label,
            skill_name=step.skill_name
        )

        self.checkpoints_created.append(checkpoint.id)

        await self._emit_event('checkpoint:created', {
            'checkpoint_id': checkpoint.id,
            'label': label,
            'skill_name': step.skill_name
        })

    async def _check_halt(self):
        """Check if execution is halted and wait if so"""
        if self.state == ExecutionState.HALTED:
            logger.info("Execution halted, waiting for resume...")
            await self.halt_event.wait()

    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """
        Emit event to both stdout and WebSocket dashboard.

        Args:
            event_type: Type of event
            data: Event data
        """
        # Keep stdout for CLI visibility
        print(f"Event: {event_type}")

        # Emit to dashboard via Socket.IO client
        if hasattr(self, 'dashboard_client') and self.dashboard_client:
            try:
                await self.dashboard_client.emit_event(event_type, data)
                logger.debug(f"Event sent to dashboard: {event_type}")
            except Exception as e:
                # Don't fail execution if dashboard emission fails
                logger.warning(f"Failed to send event to dashboard: {e}")

        # Also call event callback if provided
        if self.event_callback:
            try:
                await self.event_callback(event_type, data, self.session_id)
            except Exception as e:
                logger.warning(f"Event callback failed: {e}")
