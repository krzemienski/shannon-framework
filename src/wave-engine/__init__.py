"""
Shannon Framework v4 - Wave Execution Engine

Purpose: Wave and phase execution with validation gates and checkpointing.

Components:
  - WaveExecutionEngine: Main execution engine
  - ExecutionPlan: Multi-phase execution plan
  - Phase: Collection of waves
  - Wave: Group of parallel tasks

Execution Flow:
  1. Plan → Phases (sequential)
  2. Phase → Waves (sequential with validation gates)
  3. Wave → Tasks (parallel via orchestrator)
  4. Checkpoints at wave/phase boundaries
  5. Validation gates (≥90% confidence)

Features:
  - Wave-based parallel execution
  - Confidence-based validation gates
  - Automatic checkpointing (per_wave, per_phase, manual)
  - Progress tracking
  - SITREP generation and consolidation
  - Pause/resume support

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    ExecutionPlan,
    Phase,
    Wave,
    Task,
    WaveResult,
    PhaseResult,
    WaveStatus,
    PhaseStatus,
)
from .engine import (
    WaveExecutionEngine,
    WaveExecutionError,
)

__all__ = [
    # Engine
    'WaveExecutionEngine',

    # Models
    'ExecutionPlan',
    'Phase',
    'Wave',
    'Task',
    'WaveResult',
    'PhaseResult',

    # Enums
    'WaveStatus',
    'PhaseStatus',

    # Exceptions
    'WaveExecutionError',
]

__version__ = '1.0.0'


# Convenience functions

def create_execution_plan(
    name: str,
    specification_id: str = None,
    stop_on_failure: bool = True,
    checkpoint_frequency: str = "per_wave"
) -> ExecutionPlan:
    """
    Create execution plan.

    Args:
        name: Plan name
        specification_id: Associated specification ID
        stop_on_failure: Stop on phase failure
        checkpoint_frequency: Checkpoint frequency (per_wave, per_phase, manual)

    Returns:
        ExecutionPlan instance
    """
    import uuid
    return ExecutionPlan(
        id=f"plan_{uuid.uuid4().hex[:8]}",
        name=name,
        specification_id=specification_id,
        stop_on_phase_failure=stop_on_failure,
        checkpoint_frequency=checkpoint_frequency
    )


def create_phase(
    name: str,
    description: str,
    phase_number: int,
    confidence_threshold: float = 0.90,
    required_phases: list = None
) -> Phase:
    """
    Create phase.

    Args:
        name: Phase name
        description: Phase description
        phase_number: Phase number (1-based)
        confidence_threshold: Minimum confidence (0.0-1.0)
        required_phases: List of required phase IDs

    Returns:
        Phase instance
    """
    import uuid
    return Phase(
        id=f"phase_{phase_number}_{uuid.uuid4().hex[:8]}",
        name=name,
        description=description,
        phase_number=phase_number,
        confidence_threshold=confidence_threshold,
        required_phases=required_phases or []
    )


def create_wave(
    name: str,
    description: str,
    phase_id: str,
    max_parallel: int = 8,
    confidence_threshold: float = 0.90,
    min_success_rate: float = 1.0
) -> Wave:
    """
    Create wave.

    Args:
        name: Wave name
        description: Wave description
        phase_id: Parent phase ID
        max_parallel: Max parallel tasks
        confidence_threshold: Minimum confidence (0.0-1.0)
        min_success_rate: Minimum task success rate (0.0-1.0)

    Returns:
        Wave instance
    """
    import uuid
    return Wave(
        id=f"wave_{uuid.uuid4().hex[:8]}",
        name=name,
        description=description,
        phase_id=phase_id,
        max_parallel=max_parallel,
        confidence_threshold=confidence_threshold,
        min_success_rate=min_success_rate
    )


def create_task(
    description: str,
    agent_type: str = "custom",
    prompt: str = None,
    dependencies: list = None,
    priority: int = 0,
    estimated_duration: int = 600
) -> Task:
    """
    Create task.

    Args:
        description: Task description
        agent_type: Agent type (research, implementation, testing, etc.)
        prompt: Agent prompt (defaults to description)
        dependencies: List of dependency task IDs
        priority: Priority (higher = more important)
        estimated_duration: Estimated duration in seconds

    Returns:
        Task instance
    """
    import uuid
    return Task(
        id=f"task_{uuid.uuid4().hex[:8]}",
        description=description,
        agent_type=agent_type,
        prompt=prompt or description,
        dependencies=dependencies or [],
        priority=priority,
        estimated_duration=estimated_duration
    )
