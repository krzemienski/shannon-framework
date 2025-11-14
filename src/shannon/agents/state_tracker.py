"""
Shannon CLI V3.0 - Agent State Tracker

Tracks state, progress, and metrics for individual agents during wave execution.
Supports concurrent agent tracking with thread-safe state updates.

Architecture (from SHANNON_CLI_V3_ARCHITECTURE.md):
- AgentState dataclass: Complete agent state snapshot
- AgentStateTracker: Thread-safe state management
- State transitions: pending → active → complete/failed
- Message-based progress tracking
- Integration with analytics database

State Machine:
    pending → active → complete
                   └→ failed

Thread Safety:
    All state updates protected by threading.Lock
    No race conditions on concurrent updates
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Literal, Any
from datetime import datetime
from threading import Lock
import logging


@dataclass
class AgentState:
    """
    Complete state snapshot for a single agent.

    Tracks identity, status, progress, metrics, and artifacts.
    Designed per Feature 5 specification.
    """

    # Identity
    agent_id: str
    wave_number: int
    agent_type: str
    task_description: str

    # Status
    status: Literal['pending', 'active', 'complete', 'failed'] = 'pending'
    progress_percent: float = 0.0

    # Messages (populated from SDK stream)
    all_messages: List[Any] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    thinking_blocks: List[str] = field(default_factory=list)

    # Metrics
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cost_usd: float = 0.0
    tokens_input: int = 0
    tokens_output: int = 0

    # Artifacts
    files_created: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)

    # Recovery
    last_checkpoint: Dict[str, Any] = field(default_factory=dict)

    # Errors
    error_message: Optional[str] = None

    @property
    def duration_minutes(self) -> float:
        """Calculate duration in minutes."""
        if not self.started_at:
            return 0.0

        end_time = self.completed_at or datetime.now()
        duration_seconds = (end_time - self.started_at).total_seconds()
        return duration_seconds / 60.0

    @property
    def is_active(self) -> bool:
        """Check if agent is currently active."""
        return self.status == 'active'

    @property
    def is_complete(self) -> bool:
        """Check if agent completed successfully."""
        return self.status == 'complete'

    @property
    def is_failed(self) -> bool:
        """Check if agent failed."""
        return self.status == 'failed'

    @property
    def is_finished(self) -> bool:
        """Check if agent is in terminal state (complete or failed)."""
        return self.status in ('complete', 'failed')

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'agent_id': self.agent_id,
            'wave_number': self.wave_number,
            'agent_type': self.agent_type,
            'task_description': self.task_description,
            'status': self.status,
            'progress_percent': self.progress_percent,
            'message_count': len(self.all_messages),
            'tool_call_count': len(self.tool_calls),
            'thinking_block_count': len(self.thinking_blocks),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_minutes': self.duration_minutes,
            'cost_usd': self.cost_usd,
            'tokens_input': self.tokens_input,
            'tokens_output': self.tokens_output,
            'files_created': self.files_created,
            'files_modified': self.files_modified,
            'error_message': self.error_message
        }


class AgentStateTracker:
    """
    Thread-safe tracker for multiple concurrent agents.

    Manages agent lifecycle, state transitions, and progress updates.
    Integrates with MessageInterceptor for real-time updates.

    Thread Safety:
        All public methods use self._lock for thread-safe operations.
        Safe for concurrent updates from multiple agent streams.

    Usage:
        tracker = AgentStateTracker()

        # Register agent
        state = tracker.register_agent(
            agent_id="agent-1",
            wave_number=2,
            agent_type="backend-builder",
            task_description="Build authentication API"
        )

        # Update from message stream
        tracker.update_from_message(agent_id, message)

        # Mark transitions
        tracker.mark_started(agent_id)
        tracker.mark_complete(agent_id)

        # Query state
        agents = tracker.get_active_agents()
        summary = tracker.get_wave_summary(wave_number=2)
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize agent state tracker.

        Args:
            logger: Optional logger for debugging
        """
        self.logger = logger or self._default_logger()
        self.agents: Dict[str, AgentState] = {}
        self._lock = Lock()

    def register_agent(
        self,
        agent_id: str,
        wave_number: int,
        agent_type: str,
        task_description: str
    ) -> AgentState:
        """
        Register new agent with initial state.

        Args:
            agent_id: Unique agent identifier
            wave_number: Wave index (1-based)
            agent_type: Agent type/role
            task_description: Description of agent's task

        Returns:
            Created AgentState instance

        Raises:
            ValueError: If agent_id already exists
        """
        with self._lock:
            if agent_id in self.agents:
                raise ValueError(f"Agent {agent_id} already registered")

            state = AgentState(
                agent_id=agent_id,
                wave_number=wave_number,
                agent_type=agent_type,
                task_description=task_description,
                status='pending'
            )

            self.agents[agent_id] = state
            self.logger.info(f"Registered agent {agent_id} (Wave {wave_number})")

            return state

    def mark_started(self, agent_id: str) -> None:
        """
        Mark agent as started (pending → active).

        Args:
            agent_id: Agent to update

        Raises:
            KeyError: If agent not found
            ValueError: If agent not in pending state
        """
        with self._lock:
            state = self._get_state(agent_id)

            if state.status != 'pending':
                raise ValueError(
                    f"Agent {agent_id} must be pending to start (current: {state.status})"
                )

            state.status = 'active'
            state.started_at = datetime.now()

            self.logger.info(f"Agent {agent_id} started")

    def mark_complete(self, agent_id: str) -> None:
        """
        Mark agent as successfully completed (active → complete).

        Args:
            agent_id: Agent to update

        Raises:
            KeyError: If agent not found
            ValueError: If agent not in active state
        """
        with self._lock:
            state = self._get_state(agent_id)

            if state.status != 'active':
                raise ValueError(
                    f"Agent {agent_id} must be active to complete (current: {state.status})"
                )

            state.status = 'complete'
            state.completed_at = datetime.now()
            state.progress_percent = 100.0

            self.logger.info(
                f"Agent {agent_id} completed "
                f"({state.duration_minutes:.1f} min, ${state.cost_usd:.2f})"
            )

    def mark_failed(self, agent_id: str, error_message: str) -> None:
        """
        Mark agent as failed (active → failed).

        Args:
            agent_id: Agent to update
            error_message: Error description

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)

            state.status = 'failed'
            state.completed_at = datetime.now()
            state.error_message = error_message

            self.logger.error(
                f"Agent {agent_id} failed after {state.duration_minutes:.1f} min: {error_message}"
            )

    def update_progress(self, agent_id: str, progress: float) -> None:
        """
        Update agent progress percentage.

        Args:
            agent_id: Agent to update
            progress: Progress percentage (0-100)

        Raises:
            KeyError: If agent not found
            ValueError: If progress out of range
        """
        if not 0 <= progress <= 100:
            raise ValueError(f"Progress must be 0-100, got {progress}")

        with self._lock:
            state = self._get_state(agent_id)
            state.progress_percent = progress

    def update_metrics(
        self,
        agent_id: str,
        cost_delta: float = 0.0,
        tokens_in_delta: int = 0,
        tokens_out_delta: int = 0
    ) -> None:
        """
        Update agent metrics (incremental).

        Args:
            agent_id: Agent to update
            cost_delta: Cost to add (USD)
            tokens_in_delta: Input tokens to add
            tokens_out_delta: Output tokens to add

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)

            state.cost_usd += cost_delta
            state.tokens_input += tokens_in_delta
            state.tokens_output += tokens_out_delta

    def add_message(self, agent_id: str, message: Any) -> None:
        """
        Add message to agent's history.

        Args:
            agent_id: Agent to update
            message: SDK message to append

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)
            state.all_messages.append(message)

    def add_tool_call(self, agent_id: str, tool_call: Dict[str, Any]) -> None:
        """
        Record tool call.

        Args:
            agent_id: Agent to update
            tool_call: Tool call data (name, args, result)

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)
            state.tool_calls.append(tool_call)

    def add_thinking(self, agent_id: str, thinking: str) -> None:
        """
        Record thinking block.

        Args:
            agent_id: Agent to update
            thinking: Thinking content

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)
            state.thinking_blocks.append(thinking)

    def add_file_created(self, agent_id: str, file_path: str) -> None:
        """
        Record file creation.

        Args:
            agent_id: Agent to update
            file_path: Path to created file

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)
            if file_path not in state.files_created:
                state.files_created.append(file_path)

    def add_file_modified(self, agent_id: str, file_path: str) -> None:
        """
        Record file modification.

        Args:
            agent_id: Agent to update
            file_path: Path to modified file

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            state = self._get_state(agent_id)
            if file_path not in state.files_modified:
                state.files_modified.append(file_path)

    def get_state(self, agent_id: str) -> AgentState:
        """
        Get agent state (thread-safe copy).

        Args:
            agent_id: Agent to retrieve

        Returns:
            AgentState instance

        Raises:
            KeyError: If agent not found
        """
        with self._lock:
            return self._get_state(agent_id)

    def get_active_agents(self) -> List[AgentState]:
        """
        Get all active agents.

        Returns:
            List of active AgentState instances
        """
        with self._lock:
            return [
                state for state in self.agents.values()
                if state.is_active
            ]

    def get_wave_agents(self, wave_number: int) -> List[AgentState]:
        """
        Get all agents for specific wave.

        Args:
            wave_number: Wave index to filter

        Returns:
            List of AgentState instances for wave
        """
        with self._lock:
            return [
                state for state in self.agents.values()
                if state.wave_number == wave_number
            ]

    def get_wave_summary(self, wave_number: int) -> Dict[str, Any]:
        """
        Get summary statistics for wave.

        Args:
            wave_number: Wave index

        Returns:
            Dict with wave metrics:
                - total_agents: Total agent count
                - active_agents: Active agent count
                - complete_agents: Completed agent count
                - failed_agents: Failed agent count
                - total_cost: Total wave cost (USD)
                - total_tokens: Total tokens (input + output)
                - duration_minutes: Max duration across agents
                - files_created: Total files created
                - files_modified: Total files modified
        """
        with self._lock:
            agents = self.get_wave_agents(wave_number)

            if not agents:
                return {
                    'total_agents': 0,
                    'active_agents': 0,
                    'complete_agents': 0,
                    'failed_agents': 0,
                    'total_cost': 0.0,
                    'total_tokens': 0,
                    'duration_minutes': 0.0,
                    'files_created': 0,
                    'files_modified': 0
                }

            return {
                'total_agents': len(agents),
                'active_agents': sum(1 for a in agents if a.is_active),
                'complete_agents': sum(1 for a in agents if a.is_complete),
                'failed_agents': sum(1 for a in agents if a.is_failed),
                'total_cost': sum(a.cost_usd for a in agents),
                'total_tokens': sum(a.tokens_input + a.tokens_output for a in agents),
                'duration_minutes': max((a.duration_minutes for a in agents), default=0.0),
                'files_created': sum(len(a.files_created) for a in agents),
                'files_modified': sum(len(a.files_modified) for a in agents)
            }

    def _get_state(self, agent_id: str) -> AgentState:
        """
        Internal method to get state (caller must hold lock).

        Args:
            agent_id: Agent to retrieve

        Returns:
            AgentState instance

        Raises:
            KeyError: If agent not found
        """
        if agent_id not in self.agents:
            raise KeyError(f"Agent {agent_id} not found")

        return self.agents[agent_id]

    def _default_logger(self) -> logging.Logger:
        """Create default logger if none provided."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
