"""
Shannon Framework v4 - Wave Engine Models

Data structures for wave and phase execution.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class WaveStatus(Enum):
    """Wave execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class PhaseStatus(Enum):
    """Phase execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Individual task within a wave."""
    id: str
    description: str
    agent_type: str = "custom"
    prompt: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    priority: int = 0
    estimated_duration: int = 600  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Wave:
    """
    Wave definition - a group of related tasks.

    Waves are the primary unit of parallel execution in Shannon.
    """
    id: str
    name: str
    description: str
    phase_id: str

    # Tasks
    tasks: List[Task] = field(default_factory=list)

    # Execution control
    max_parallel: int = 8
    fail_fast: bool = False
    retry_on_failure: bool = True

    # Validation
    confidence_threshold: float = 0.90
    validation_required: bool = True

    # Success criteria
    min_success_rate: float = 1.0  # All tasks must succeed by default

    # Metadata
    estimated_duration: int = 0  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'phase_id': self.phase_id,
            'tasks': [
                {
                    'id': t.id,
                    'description': t.description,
                    'agent_type': t.agent_type,
                    'dependencies': t.dependencies,
                    'priority': t.priority,
                }
                for t in self.tasks
            ],
            'max_parallel': self.max_parallel,
            'fail_fast': self.fail_fast,
            'confidence_threshold': self.confidence_threshold,
            'validation_required': self.validation_required,
            'min_success_rate': self.min_success_rate,
            'estimated_duration': self.estimated_duration,
            'metadata': self.metadata,
        }


@dataclass
class Phase:
    """
    Phase definition - a collection of waves.

    Phases represent major milestones in project execution.
    """
    id: str
    name: str
    description: str
    phase_number: int

    # Waves
    waves: List[Wave] = field(default_factory=list)

    # Execution control
    skip_on_low_confidence: bool = True
    confidence_threshold: float = 0.90

    # Dependencies
    required_phases: List[str] = field(default_factory=list)

    # Metadata
    estimated_duration: int = 0  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'phase_number': self.phase_number,
            'waves': [wave.to_dict() for wave in self.waves],
            'skip_on_low_confidence': self.skip_on_low_confidence,
            'confidence_threshold': self.confidence_threshold,
            'required_phases': self.required_phases,
            'estimated_duration': self.estimated_duration,
            'metadata': self.metadata,
        }


@dataclass
class WaveResult:
    """Result of wave execution."""
    wave_id: str
    wave_name: str
    status: WaveStatus

    # Timing
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Task results
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0

    # Validation
    confidence_score: float = 0.0
    validation_passed: bool = False

    # Output
    sitrep: Optional[Dict[str, Any]] = None
    artifacts: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)

    # Errors
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'wave_id': self.wave_id,
            'wave_name': self.wave_name,
            'status': self.status.value,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'confidence_score': self.confidence_score,
            'validation_passed': self.validation_passed,
            'sitrep': self.sitrep,
            'artifacts': self.artifacts,
            'metrics': self.metrics,
            'errors': self.errors,
        }

    def get_success_rate(self) -> float:
        """Get task success rate."""
        if self.total_tasks == 0:
            return 1.0
        return self.completed_tasks / self.total_tasks


@dataclass
class PhaseResult:
    """Result of phase execution."""
    phase_id: str
    phase_name: str
    phase_number: int
    status: PhaseStatus

    # Timing
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Wave results
    wave_results: List[WaveResult] = field(default_factory=list)

    # Validation
    overall_confidence: float = 0.0
    validation_passed: bool = False

    # Output
    consolidated_sitrep: Optional[Dict[str, Any]] = None
    artifacts: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)

    # Errors
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'phase_id': self.phase_id,
            'phase_name': self.phase_name,
            'phase_number': self.phase_number,
            'status': self.status.value,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'wave_results': [wr.to_dict() for wr in self.wave_results],
            'overall_confidence': self.overall_confidence,
            'validation_passed': self.validation_passed,
            'consolidated_sitrep': self.consolidated_sitrep,
            'artifacts': self.artifacts,
            'metrics': self.metrics,
            'errors': self.errors,
        }

    def get_wave_success_rate(self) -> float:
        """Get wave success rate."""
        if not self.wave_results:
            return 1.0

        successful = sum(
            1 for wr in self.wave_results
            if wr.status == WaveStatus.COMPLETED and wr.validation_passed
        )
        return successful / len(self.wave_results)


@dataclass
class ExecutionPlan:
    """Complete execution plan with phases and waves."""
    id: str
    name: str
    specification_id: Optional[str] = None

    # Phases
    phases: List[Phase] = field(default_factory=list)

    # Execution control
    stop_on_phase_failure: bool = True
    checkpoint_frequency: str = "per_wave"  # per_wave, per_phase, manual

    # Validation
    global_confidence_threshold: float = 0.90

    # Metadata
    total_estimated_duration: int = 0  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'specification_id': self.specification_id,
            'phases': [phase.to_dict() for phase in self.phases],
            'stop_on_phase_failure': self.stop_on_phase_failure,
            'checkpoint_frequency': self.checkpoint_frequency,
            'global_confidence_threshold': self.global_confidence_threshold,
            'total_estimated_duration': self.total_estimated_duration,
            'metadata': self.metadata,
        }

    def get_phase(self, phase_id: str) -> Optional[Phase]:
        """Get phase by ID."""
        for phase in self.phases:
            if phase.id == phase_id:
                return phase
        return None

    def get_wave(self, wave_id: str) -> Optional[Wave]:
        """Get wave by ID."""
        for phase in self.phases:
            for wave in phase.waves:
                if wave.id == wave_id:
                    return wave
        return None
