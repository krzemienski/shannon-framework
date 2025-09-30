"""
Shannon Framework v2.1 - Wave Configuration

Defines wave configuration structures, phases, and validation logic.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class WavePhase(Enum):
    """Wave execution phases"""
    DISCOVERY = "discovery"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    IMPLEMENTATION = "implementation"
    VALIDATION = "validation"


class ValidationLevel(Enum):
    """Validation strictness levels"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    STRICT = "strict"
    PRODUCTION = "production"


@dataclass
class AgentAllocation:
    """Agent distribution across wave phases"""
    phase: WavePhase
    agent_count: int
    agent_types: List[str]
    parallel_execution: bool
    timeout_seconds: int
    retry_limit: int = 3

    def __post_init__(self):
        """Validate allocation parameters"""
        if self.agent_count < 1:
            raise ValueError(f"Agent count must be positive, got {self.agent_count}")
        if self.timeout_seconds < 1:
            raise ValueError(f"Timeout must be positive, got {self.timeout_seconds}")
        if self.retry_limit < 0:
            raise ValueError(f"Retry limit cannot be negative, got {self.retry_limit}")
        if not self.agent_types:
            raise ValueError("Agent types cannot be empty")


@dataclass
class WaveConfig:
    """Complete wave configuration specification"""
    wave_id: str
    objective: str
    phases: List[AgentAllocation]
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    max_parallel_agents: int = 5
    total_timeout_seconds: int = 3600
    enable_learning: bool = True
    enable_reflection: bool = True
    checkpoint_interval_seconds: int = 300
    metadata: Dict[str, any] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)

    def __post_init__(self):
        """Validate wave configuration"""
        if not self.wave_id:
            raise ValueError("Wave ID cannot be empty")
        if not self.objective:
            raise ValueError("Objective cannot be empty")
        if not self.phases:
            raise ValueError("Phases cannot be empty")

        # Validate phase ordering
        phase_order = [WavePhase.DISCOVERY, WavePhase.ANALYSIS, WavePhase.SYNTHESIS,
                      WavePhase.IMPLEMENTATION, WavePhase.VALIDATION]
        phase_indices = {}
        for alloc in self.phases:
            if alloc.phase in phase_indices:
                logger.warning(f"Duplicate phase {alloc.phase} in wave {self.wave_id}")
            phase_indices[alloc.phase] = phase_order.index(alloc.phase)

        # Validate constraints
        if self.max_parallel_agents < 1:
            raise ValueError(f"Max parallel agents must be positive, got {self.max_parallel_agents}")
        if self.total_timeout_seconds < 1:
            raise ValueError(f"Total timeout must be positive, got {self.total_timeout_seconds}")
        if self.checkpoint_interval_seconds < 1:
            raise ValueError(f"Checkpoint interval must be positive, got {self.checkpoint_interval_seconds}")

    def get_phase_allocation(self, phase: WavePhase) -> Optional[AgentAllocation]:
        """Get allocation for specific phase"""
        for alloc in self.phases:
            if alloc.phase == phase:
                return alloc
        return None

    def total_agent_count(self) -> int:
        """Calculate total agents across all phases"""
        return sum(alloc.agent_count for alloc in self.phases)

    def estimated_duration_seconds(self) -> int:
        """Estimate total wave duration"""
        duration = 0
        for alloc in self.phases:
            if alloc.parallel_execution:
                duration += alloc.timeout_seconds
            else:
                duration += alloc.timeout_seconds * alloc.agent_count
        return duration

    def validate_dependencies(self, available_waves: Set[str]) -> bool:
        """Check if all dependencies are satisfied"""
        return self.dependencies.issubset(available_waves)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'wave_id': self.wave_id,
            'objective': self.objective,
            'phases': [
                {
                    'phase': alloc.phase.value,
                    'agent_count': alloc.agent_count,
                    'agent_types': alloc.agent_types,
                    'parallel_execution': alloc.parallel_execution,
                    'timeout_seconds': alloc.timeout_seconds,
                    'retry_limit': alloc.retry_limit
                }
                for alloc in self.phases
            ],
            'validation_level': self.validation_level.value,
            'max_parallel_agents': self.max_parallel_agents,
            'total_timeout_seconds': self.total_timeout_seconds,
            'enable_learning': self.enable_learning,
            'enable_reflection': self.enable_reflection,
            'checkpoint_interval_seconds': self.checkpoint_interval_seconds,
            'metadata': self.metadata,
            'dependencies': list(self.dependencies)
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'WaveConfig':
        """Deserialize from dictionary"""
        phases = [
            AgentAllocation(
                phase=WavePhase(p['phase']),
                agent_count=p['agent_count'],
                agent_types=p['agent_types'],
                parallel_execution=p['parallel_execution'],
                timeout_seconds=p['timeout_seconds'],
                retry_limit=p.get('retry_limit', 3)
            )
            for p in data['phases']
        ]

        return cls(
            wave_id=data['wave_id'],
            objective=data['objective'],
            phases=phases,
            validation_level=ValidationLevel(data['validation_level']),
            max_parallel_agents=data['max_parallel_agents'],
            total_timeout_seconds=data['total_timeout_seconds'],
            enable_learning=data['enable_learning'],
            enable_reflection=data['enable_reflection'],
            checkpoint_interval_seconds=data['checkpoint_interval_seconds'],
            metadata=data.get('metadata', {}),
            dependencies=set(data.get('dependencies', []))
        )


@dataclass
class WaveResult:
    """Aggregated wave execution results"""
    wave_id: str
    success: bool
    phase_results: Dict[WavePhase, List['AgentResult']]
    total_duration_seconds: float
    agents_executed: int
    agents_succeeded: int
    agents_failed: int
    insights: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, any] = field(default_factory=dict)

    def success_rate(self) -> float:
        """Calculate agent success rate"""
        if self.agents_executed == 0:
            return 0.0
        return self.agents_succeeded / self.agents_executed

    def phase_success_rate(self, phase: WavePhase) -> float:
        """Calculate success rate for specific phase"""
        if phase not in self.phase_results:
            return 0.0
        results = self.phase_results[phase]
        if not results:
            return 0.0
        succeeded = sum(1 for r in results if r.success)
        return succeeded / len(results)

    def get_all_agent_results(self) -> List['AgentResult']:
        """Flatten all agent results across phases"""
        all_results = []
        for results in self.phase_results.values():
            all_results.extend(results)
        return all_results

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'wave_id': self.wave_id,
            'success': self.success,
            'phase_results': {
                phase.value: [r.to_dict() for r in results]
                for phase, results in self.phase_results.items()
            },
            'total_duration_seconds': self.total_duration_seconds,
            'agents_executed': self.agents_executed,
            'agents_succeeded': self.agents_succeeded,
            'agents_failed': self.agents_failed,
            'insights': self.insights,
            'errors': self.errors,
            'metadata': self.metadata
        }