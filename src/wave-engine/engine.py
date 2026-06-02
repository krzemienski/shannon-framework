"""
Shannon Framework v4 - Wave Execution Engine

Executes waves and phases with validation gates and checkpointing.
"""

from typing import Optional, Dict, Any, Callable
from datetime import datetime
from .models import (
    ExecutionPlan, Phase, Wave, WaveResult, PhaseResult,
    WaveStatus, PhaseStatus, Task
)


class WaveExecutionError(Exception):
    """Exception raised during wave execution."""
    pass


class WaveExecutionEngine:
    """
    Executes waves and phases with validation gates.

    Features:
    - Wave-based parallel execution
    - Confidence-based validation gates
    - Automatic checkpointing
    - Progress tracking
    - SITREP generation
    """

    def __init__(
        self,
        orchestrator=None,
        context_manager=None,
        validator=None
    ):
        """
        Initialize wave execution engine.

        Args:
            orchestrator: SubAgentOrchestrator instance
            context_manager: ContextManager instance
            validator: ValidationGate instance
        """
        self.orchestrator = orchestrator
        self.context_manager = context_manager
        self.validator = validator

        self.current_plan: Optional[ExecutionPlan] = None
        self.current_phase: Optional[Phase] = None
        self.current_wave: Optional[Wave] = None

        # Results tracking
        self.phase_results: Dict[str, PhaseResult] = {}
        self.wave_results: Dict[str, WaveResult] = {}

    def execute_plan(self, plan: ExecutionPlan) -> Dict[str, PhaseResult]:
        """
        Execute complete execution plan.

        Args:
            plan: ExecutionPlan to execute

        Returns:
            Dictionary of phase results by phase ID
        """
        self.current_plan = plan
        self.phase_results = {}

        # Create initial checkpoint
        if self.context_manager:
            from ..context_manager import CheckpointType
            self.context_manager.auto_checkpoint(
                CheckpointType.PRE_PHASE,
                f"Before execution plan: {plan.name}"
            )

        # Execute phases in order
        for phase in plan.phases:
            # Check if phase should be executed
            if not self._should_execute_phase(phase):
                phase_result = PhaseResult(
                    phase_id=phase.id,
                    phase_name=phase.name,
                    phase_number=phase.phase_number,
                    status=PhaseStatus.SKIPPED,
                    start_time=datetime.now(),
                    end_time=datetime.now()
                )
                self.phase_results[phase.id] = phase_result
                continue

            # Execute phase
            phase_result = self.execute_phase(phase)
            self.phase_results[phase.id] = phase_result

            # Check if should continue
            if plan.stop_on_phase_failure and phase_result.status == PhaseStatus.FAILED:
                break

        # Create final checkpoint
        if self.context_manager:
            self.context_manager.auto_checkpoint(
                CheckpointType.POST_PHASE,
                f"After execution plan: {plan.name}"
            )

        return self.phase_results

    def execute_phase(self, phase: Phase) -> PhaseResult:
        """
        Execute a phase (collection of waves).

        Args:
            phase: Phase to execute

        Returns:
            PhaseResult
        """
        self.current_phase = phase

        result = PhaseResult(
            phase_id=phase.id,
            phase_name=phase.name,
            phase_number=phase.phase_number,
            status=PhaseStatus.RUNNING,
            start_time=datetime.now()
        )

        # Pre-phase checkpoint
        if self.context_manager:
            from ..context_manager import CheckpointType
            self.context_manager.auto_checkpoint(
                CheckpointType.PRE_PHASE,
                f"Before Phase {phase.phase_number}: {phase.name}"
            )

        # Execute waves
        for wave in phase.waves:
            wave_result = self.execute_wave(wave)
            result.wave_results.append(wave_result)
            self.wave_results[wave.id] = wave_result

            # Check validation
            if wave.validation_required and not wave_result.validation_passed:
                result.status = PhaseStatus.FAILED
                result.errors.append(
                    f"Wave '{wave.name}' failed validation "
                    f"(confidence: {wave_result.confidence_score:.2%})"
                )
                break

        # Calculate overall confidence
        if result.wave_results:
            result.overall_confidence = sum(
                wr.confidence_score for wr in result.wave_results
            ) / len(result.wave_results)

        # Determine final status
        if result.status != PhaseStatus.FAILED:
            all_completed = all(
                wr.status == WaveStatus.COMPLETED
                for wr in result.wave_results
            )
            result.status = PhaseStatus.COMPLETED if all_completed else PhaseStatus.FAILED

        # Validate phase
        result.validation_passed = (
            result.overall_confidence >= phase.confidence_threshold and
            result.status == PhaseStatus.COMPLETED
        )

        # Finalize timing
        result.end_time = datetime.now()
        result.duration_seconds = (
            result.end_time - result.start_time
        ).total_seconds()

        # Post-phase checkpoint
        if self.context_manager:
            from ..context_manager import CheckpointType
            self.context_manager.auto_checkpoint(
                CheckpointType.POST_PHASE,
                f"After Phase {phase.phase_number}: {phase.name}"
            )

            # Update context
            self.context_manager.update_context(
                current_phase=phase.phase_number,
                completed_phases=list(self.phase_results.keys())
            )

        return result

    def execute_wave(self, wave: Wave) -> WaveResult:
        """
        Execute a wave (group of tasks).

        Args:
            wave: Wave to execute

        Returns:
            WaveResult
        """
        self.current_wave = wave

        result = WaveResult(
            wave_id=wave.id,
            wave_name=wave.name,
            status=WaveStatus.RUNNING,
            start_time=datetime.now(),
            total_tasks=len(wave.tasks)
        )

        # Pre-wave checkpoint
        if self.context_manager and self.current_plan:
            if self.current_plan.checkpoint_frequency == "per_wave":
                from ..context_manager import CheckpointType
                self.context_manager.auto_checkpoint(
                    CheckpointType.PRE_WAVE,
                    f"Before wave: {wave.name}"
                )

        try:
            # Execute wave tasks using orchestrator
            if self.orchestrator:
                orch_result = self._execute_wave_with_orchestrator(wave)

                # Update result from orchestration
                result.completed_tasks = orch_result.get('completed_tasks', 0)
                result.failed_tasks = orch_result.get('failed_tasks', 0)
                result.sitrep = orch_result.get('sitrep')
                result.artifacts = orch_result.get('artifacts', {})
                result.metrics = orch_result.get('metrics', {})
                result.errors = orch_result.get('errors', [])

            else:
                # No orchestrator - mark as completed (placeholder)
                result.completed_tasks = result.total_tasks
                result.status = WaveStatus.COMPLETED

            # Validate wave
            if wave.validation_required and self.validator:
                validation_result = self.validator.validate_wave(wave, result)
                result.confidence_score = validation_result.get('confidence', 0.0)
                result.validation_passed = validation_result.get('passed', False)
            else:
                # No validation - assume passed if success rate met
                success_rate = result.get_success_rate()
                result.confidence_score = success_rate
                result.validation_passed = success_rate >= wave.min_success_rate

            # Determine final status
            if result.failed_tasks > 0:
                max_failures = result.total_tasks * (1.0 - wave.min_success_rate)
                if result.failed_tasks > max_failures:
                    result.status = WaveStatus.FAILED
                else:
                    result.status = WaveStatus.COMPLETED
            else:
                result.status = WaveStatus.COMPLETED

        except Exception as e:
            result.status = WaveStatus.FAILED
            result.errors.append(str(e))

        # Finalize timing
        result.end_time = datetime.now()
        result.duration_seconds = (
            result.end_time - result.start_time
        ).total_seconds()

        # Post-wave checkpoint
        if self.context_manager and self.current_plan:
            if self.current_plan.checkpoint_frequency == "per_wave":
                from ..context_manager import CheckpointType
                self.context_manager.auto_checkpoint(
                    CheckpointType.POST_WAVE,
                    f"After wave: {wave.name}"
                )

            # Update context
            if self.current_phase:
                completed_waves = [
                    wr.wave_id for wr in self.phase_results.get(
                        self.current_phase.id, PhaseResult(
                            phase_id='', phase_name='', phase_number=0,
                            status=PhaseStatus.PENDING, start_time=datetime.now()
                        )
                    ).wave_results
                    if wr.status == WaveStatus.COMPLETED
                ]
                self.context_manager.update_context(
                    current_wave=wave.id,
                    completed_waves=completed_waves
                )

        return result

    def _execute_wave_with_orchestrator(self, wave: Wave) -> Dict[str, Any]:
        """
        Execute wave using orchestrator.

        Args:
            wave: Wave to execute

        Returns:
            Orchestration result dictionary
        """
        from ..orchestrator import create_plan, create_task, OrchestrationStrategy

        # Create orchestration plan
        orch_plan = create_plan(
            name=wave.name,
            strategy="dependency",
            max_parallel=wave.max_parallel,
            fail_fast=wave.fail_fast
        )

        # Add tasks
        for task in wave.tasks:
            agent_task = create_task(
                id=task.id,
                name=task.description,
                prompt=task.prompt or task.description,
                agent_type=task.agent_type,
                priority=task.priority,
                dependencies=task.dependencies,
                timeout=task.estimated_duration * 1000,  # Convert to ms
            )
            orch_plan.add_task(agent_task)

        # Execute
        orch_result = self.orchestrator.execute_plan(orch_plan)

        # Extract results
        return {
            'completed_tasks': orch_result.completed_tasks,
            'failed_tasks': orch_result.failed_tasks,
            'sitrep': orch_result.consolidated_sitrep,
            'artifacts': orch_result.artifacts,
            'metrics': orch_result.metrics,
            'errors': orch_result.errors,
        }

    def _should_execute_phase(self, phase: Phase) -> bool:
        """
        Check if phase should be executed.

        Args:
            phase: Phase to check

        Returns:
            True if should execute
        """
        # Check required phases
        for required_phase_id in phase.required_phases:
            if required_phase_id not in self.phase_results:
                return False

            required_result = self.phase_results[required_phase_id]
            if required_result.status != PhaseStatus.COMPLETED:
                return False

            # Check confidence
            if phase.skip_on_low_confidence:
                if required_result.overall_confidence < phase.confidence_threshold:
                    return False

        return True

    def get_progress(self) -> Dict[str, Any]:
        """
        Get current execution progress.

        Returns:
            Progress dictionary
        """
        if not self.current_plan:
            return {}

        total_phases = len(self.current_plan.phases)
        completed_phases = sum(
            1 for pr in self.phase_results.values()
            if pr.status == PhaseStatus.COMPLETED
        )

        total_waves = sum(len(phase.waves) for phase in self.current_plan.phases)
        completed_waves = len([
            wr for wr in self.wave_results.values()
            if wr.status == WaveStatus.COMPLETED
        ])

        return {
            'plan_name': self.current_plan.name,
            'total_phases': total_phases,
            'completed_phases': completed_phases,
            'phase_progress': completed_phases / total_phases if total_phases > 0 else 0.0,
            'total_waves': total_waves,
            'completed_waves': completed_waves,
            'wave_progress': completed_waves / total_waves if total_waves > 0 else 0.0,
            'current_phase': self.current_phase.name if self.current_phase else None,
            'current_wave': self.current_wave.name if self.current_wave else None,
        }

    def pause_execution(self):
        """Pause execution at current point."""
        if self.current_wave:
            # Create checkpoint
            if self.context_manager:
                from ..context_manager import CheckpointType
                self.context_manager.create_checkpoint(
                    checkpoint_type=CheckpointType.MANUAL,
                    description="Execution paused by user"
                )

    def resume_execution(self, checkpoint_id: str = None):
        """
        Resume execution from checkpoint.

        Args:
            checkpoint_id: Optional checkpoint to resume from
        """
        if checkpoint_id and self.context_manager:
            # Restore from checkpoint
            result = self.context_manager.restore_checkpoint(checkpoint_id)
            if not result.success:
                raise WaveExecutionError(f"Failed to restore checkpoint: {result.errors}")
