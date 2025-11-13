"""
Shannon Framework v4 - Orchestrator Models

Data structures for sub-agent orchestration.
"""

from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    """Agent execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class AgentType(Enum):
    """Types of agents."""
    RESEARCH = "research"           # Research and analysis
    IMPLEMENTATION = "implementation"  # Code implementation
    TESTING = "testing"             # Testing and validation
    REVIEW = "review"               # Code review
    DOCUMENTATION = "documentation"  # Documentation generation
    CUSTOM = "custom"               # Custom agent type


class OrchestrationStrategy(Enum):
    """Orchestration execution strategies."""
    PARALLEL = "parallel"           # All agents run in parallel
    SEQUENTIAL = "sequential"       # Agents run one by one
    DEPENDENCY = "dependency"       # Respect dependency graph
    PRIORITY = "priority"           # Execute by priority order


@dataclass
class AgentTask:
    """Task definition for a sub-agent."""
    id: str
    name: str
    agent_type: AgentType
    prompt: str

    # Execution parameters
    priority: int = 0  # Higher = more important
    timeout: int = 600000  # 10 minutes default
    max_retries: int = 0

    # Dependencies
    dependencies: List[str] = field(default_factory=list)  # Agent IDs
    required_skills: List[str] = field(default_factory=list)

    # Context
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Callbacks
    on_complete: Optional[Callable] = None
    on_error: Optional[Callable] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'agent_type': self.agent_type.value,
            'prompt': self.prompt,
            'priority': self.priority,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'dependencies': self.dependencies,
            'required_skills': self.required_skills,
            'context': self.context,
            'metadata': self.metadata,
        }


@dataclass
class AgentResult:
    """Result from agent execution."""
    agent_id: str
    agent_name: str
    status: AgentStatus

    # Timing
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Output
    output: Optional[str] = None
    sitrep: Optional[Dict[str, Any]] = None  # SITREP data
    artifacts: Dict[str, Any] = field(default_factory=dict)

    # Error handling
    error: Optional[str] = None
    retry_count: int = 0

    # Metrics
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'status': self.status.value,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'output': self.output,
            'sitrep': self.sitrep,
            'artifacts': self.artifacts,
            'error': self.error,
            'retry_count': self.retry_count,
            'metrics': self.metrics,
        }

    def is_success(self) -> bool:
        """Check if agent completed successfully."""
        return self.status == AgentStatus.COMPLETED and not self.error

    def is_failure(self) -> bool:
        """Check if agent failed."""
        return self.status in [AgentStatus.FAILED, AgentStatus.TIMEOUT]


@dataclass
class OrchestrationPlan:
    """Plan for orchestrating multiple agents."""
    id: str
    name: str
    strategy: OrchestrationStrategy

    # Tasks
    tasks: List[AgentTask] = field(default_factory=list)

    # Execution control
    max_parallel: int = 8  # Max parallel agents
    fail_fast: bool = False  # Stop on first failure

    # Timeouts
    global_timeout: Optional[int] = None  # Overall timeout

    # Context
    shared_context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'strategy': self.strategy.value,
            'tasks': [task.to_dict() for task in self.tasks],
            'max_parallel': self.max_parallel,
            'fail_fast': self.fail_fast,
            'global_timeout': self.global_timeout,
            'shared_context': self.shared_context,
            'metadata': self.metadata,
        }

    def add_task(self, task: AgentTask):
        """Add task to plan."""
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[AgentTask]:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_ready_tasks(self, completed_ids: set) -> List[AgentTask]:
        """
        Get tasks that are ready to execute.

        Args:
            completed_ids: Set of completed task IDs

        Returns:
            List of tasks with satisfied dependencies
        """
        ready = []
        for task in self.tasks:
            # Check if all dependencies are satisfied
            if all(dep in completed_ids for dep in task.dependencies):
                ready.append(task)
        return ready


@dataclass
class OrchestrationResult:
    """Result of orchestration execution."""
    plan_id: str
    plan_name: str

    # Timing
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Results
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)  # agent_id -> result

    # Status
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    cancelled_tasks: int = 0

    # Aggregated output
    consolidated_sitrep: Optional[Dict[str, Any]] = None
    artifacts: Dict[str, Any] = field(default_factory=dict)

    # Errors
    errors: List[str] = field(default_factory=list)

    # Metrics
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'plan_id': self.plan_id,
            'plan_name': self.plan_name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'agent_results': {
                agent_id: result.to_dict()
                for agent_id, result in self.agent_results.items()
            },
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'cancelled_tasks': self.cancelled_tasks,
            'consolidated_sitrep': self.consolidated_sitrep,
            'artifacts': self.artifacts,
            'errors': self.errors,
            'metrics': self.metrics,
        }

    def is_success(self) -> bool:
        """Check if orchestration completed successfully."""
        return (
            self.failed_tasks == 0 and
            self.completed_tasks == self.total_tasks
        )

    def get_success_rate(self) -> float:
        """Get success rate (0.0 to 1.0)."""
        if self.total_tasks == 0:
            return 1.0
        return self.completed_tasks / self.total_tasks

    def get_failed_agents(self) -> List[AgentResult]:
        """Get all failed agent results."""
        return [
            result for result in self.agent_results.values()
            if result.is_failure()
        ]

    def get_successful_agents(self) -> List[AgentResult]:
        """Get all successful agent results."""
        return [
            result for result in self.agent_results.values()
            if result.is_success()
        ]
