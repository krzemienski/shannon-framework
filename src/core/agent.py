"""
Shannon Framework v2.1 - Agent Implementation

Base agent class, state management, metrics tracking, and execution framework.
"""

import asyncio
import time
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent lifecycle states"""
    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentCapability(Enum):
    """Agent capability types"""
    ANALYSIS = "analysis"
    BUILDING = "building"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    OPTIMIZATION = "optimization"
    VALIDATION = "validation"
    RESEARCH = "research"
    INTEGRATION = "integration"


@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    agent_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    execution_time_seconds: float = 0.0
    state_transitions: List[tuple[AgentState, float]] = field(default_factory=list)
    tasks_completed: int = 0
    tasks_failed: int = 0
    memory_usage_mb: float = 0.0
    cpu_time_seconds: float = 0.0
    retries: int = 0
    errors: List[str] = field(default_factory=list)

    def record_state_transition(self, new_state: AgentState):
        """Record state change with timestamp"""
        self.state_transitions.append((new_state, time.time()))

    def calculate_duration(self) -> float:
        """Calculate total execution duration"""
        if self.start_time > 0 and self.end_time > 0:
            return self.end_time - self.start_time
        return 0.0

    def success_rate(self) -> float:
        """Calculate task success rate"""
        total = self.tasks_completed + self.tasks_failed
        if total == 0:
            return 0.0
        return self.tasks_completed / total

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'agent_id': self.agent_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'execution_time_seconds': self.execution_time_seconds,
            'state_transitions': [(s.value, t) for s, t in self.state_transitions],
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'memory_usage_mb': self.memory_usage_mb,
            'cpu_time_seconds': self.cpu_time_seconds,
            'retries': self.retries,
            'errors': self.errors
        }


@dataclass
class AgentResult:
    """Agent execution result"""
    agent_id: str
    agent_type: str
    success: bool
    output: Any
    metrics: AgentMetrics
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'success': self.success,
            'output': self.output,
            'metrics': self.metrics.to_dict(),
            'error_message': self.error_message,
            'error_traceback': self.error_traceback,
            'metadata': self.metadata
        }


class BaseAgent(ABC):
    """
    Abstract base agent with state management and execution framework.

    All Shannon agents inherit from this class and implement execute() method.
    """

    def __init__(self, agent_id: str, capabilities: Set[AgentCapability], config: Dict[str, Any]):
        """
        Initialize agent with ID, capabilities, and configuration.

        Args:
            agent_id: Unique agent identifier
            capabilities: Set of agent capabilities
            config: Agent configuration dictionary
        """
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.config = config
        self.state = AgentState.CREATED
        self.metrics = AgentMetrics(agent_id=agent_id)
        self._lock = asyncio.Lock()
        self._cancel_event = asyncio.Event()

        logger.info(f"Agent {agent_id} created with capabilities: {[c.value for c in capabilities]}")

    async def initialize(self) -> bool:
        """
        Initialize agent resources and prepare for execution.

        Returns:
            True if initialization successful, False otherwise
        """
        async with self._lock:
            if self.state != AgentState.CREATED:
                logger.warning(f"Agent {self.agent_id} already initialized, state: {self.state}")
                return False

            try:
                self._transition_state(AgentState.INITIALIZING)
                success = await self._initialize_resources()
                if success:
                    self._transition_state(AgentState.READY)
                    logger.info(f"Agent {self.agent_id} initialized successfully")
                else:
                    self._transition_state(AgentState.FAILED)
                    logger.error(f"Agent {self.agent_id} initialization failed")
                return success
            except Exception as e:
                logger.error(f"Agent {self.agent_id} initialization error: {e}")
                self._transition_state(AgentState.FAILED)
                self.metrics.errors.append(str(e))
                return False

    async def run(self, task: Dict[str, Any]) -> AgentResult:
        """
        Execute agent task with full lifecycle management.

        Args:
            task: Task specification dictionary

        Returns:
            AgentResult with execution outcome
        """
        if self.state != AgentState.READY:
            error_msg = f"Agent {self.agent_id} not ready, state: {self.state}"
            logger.error(error_msg)
            return AgentResult(
                agent_id=self.agent_id,
                agent_type=self.__class__.__name__,
                success=False,
                output=None,
                metrics=self.metrics,
                error_message=error_msg
            )

        async with self._lock:
            self._transition_state(AgentState.EXECUTING)
            self.metrics.start_time = time.time()

        try:
            logger.info(f"Agent {self.agent_id} starting execution")
            output = await self.execute(task)

            async with self._lock:
                self.metrics.end_time = time.time()
                self.metrics.execution_time_seconds = self.metrics.calculate_duration()
                self.metrics.tasks_completed += 1
                self._transition_state(AgentState.COMPLETED)

            logger.info(f"Agent {self.agent_id} completed successfully in {self.metrics.execution_time_seconds:.2f}s")

            return AgentResult(
                agent_id=self.agent_id,
                agent_type=self.__class__.__name__,
                success=True,
                output=output,
                metrics=self.metrics
            )

        except asyncio.CancelledError:
            async with self._lock:
                self.metrics.end_time = time.time()
                self.metrics.execution_time_seconds = self.metrics.calculate_duration()
                self._transition_state(AgentState.CANCELLED)

            logger.warning(f"Agent {self.agent_id} cancelled after {self.metrics.execution_time_seconds:.2f}s")

            return AgentResult(
                agent_id=self.agent_id,
                agent_type=self.__class__.__name__,
                success=False,
                output=None,
                metrics=self.metrics,
                error_message="Agent execution cancelled"
            )

        except Exception as e:
            error_trace = traceback.format_exc()

            async with self._lock:
                self.metrics.end_time = time.time()
                self.metrics.execution_time_seconds = self.metrics.calculate_duration()
                self.metrics.tasks_failed += 1
                self.metrics.errors.append(str(e))
                self._transition_state(AgentState.FAILED)

            logger.error(f"Agent {self.agent_id} failed: {e}\n{error_trace}")

            return AgentResult(
                agent_id=self.agent_id,
                agent_type=self.__class__.__name__,
                success=False,
                output=None,
                metrics=self.metrics,
                error_message=str(e),
                error_traceback=error_trace
            )

    async def cancel(self):
        """Cancel agent execution"""
        logger.info(f"Cancelling agent {self.agent_id}")
        self._cancel_event.set()

    def is_cancelled(self) -> bool:
        """Check if agent execution is cancelled"""
        return self._cancel_event.is_set()

    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability"""
        return capability in self.capabilities

    def _transition_state(self, new_state: AgentState):
        """Transition to new state and record metrics"""
        old_state = self.state
        self.state = new_state
        self.metrics.record_state_transition(new_state)
        logger.debug(f"Agent {self.agent_id} state: {old_state.value} -> {new_state.value}")

    async def _initialize_resources(self) -> bool:
        """
        Initialize agent-specific resources.

        Override in subclasses to add custom initialization.

        Returns:
            True if successful, False otherwise
        """
        return True

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Any:
        """
        Execute agent-specific task logic.

        Must be implemented by all agent subclasses.

        Args:
            task: Task specification dictionary

        Returns:
            Task execution result
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.agent_id} state={self.state.value}>"


class SimpleAgent(BaseAgent):
    """
    Simple agent implementation for testing and examples.

    Executes a synchronous or asynchronous callable.
    """

    def __init__(self, agent_id: str, capabilities: Set[AgentCapability], config: Dict[str, Any]):
        super().__init__(agent_id, capabilities, config)
        self.callable = config.get('callable')
        if self.callable is None:
            raise ValueError("SimpleAgent requires 'callable' in config")

    async def execute(self, task: Dict[str, Any]) -> Any:
        """Execute the configured callable"""
        if asyncio.iscoroutinefunction(self.callable):
            return await self.callable(task)
        else:
            return self.callable(task)