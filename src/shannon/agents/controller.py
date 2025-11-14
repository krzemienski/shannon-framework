"""
Shannon CLI V3.0 - Agent Controller

High-level controller for agent lifecycle and operations.
Implements commands: follow, pause, retry.

Architecture (from SHANNON_CLI_V3_ARCHITECTURE.md):
- Controls agent execution flow
- Wave-level pause/resume
- Individual agent retry
- Message stream following
- Integration with AgentStateTracker

Commands:
    shannon wave follow <agent_id>  # Stream agent messages
    shannon wave pause              # Pause wave after current agents
    shannon wave retry <agent_id>   # Retry failed agent
"""

from typing import Optional, Callable, Any, AsyncIterator
from .state_tracker import AgentStateTracker, AgentState
import asyncio
import logging


class AgentController:
    """
    Controller for agent lifecycle and operations.

    Manages:
    - Following agent message streams
    - Pausing wave execution
    - Retrying failed agents
    - Wave-level control flow

    Integration:
        - AgentStateTracker: Query and update agent states
        - MessageRouter: Route messages to appropriate agents
        - Analytics: Record control events

    Usage:
        controller = AgentController(state_tracker)

        # Follow agent stream
        await controller.follow_agent("agent-1", output_callback)

        # Pause wave
        controller.pause_wave(wave_number=2)

        # Retry failed agent
        await controller.retry_agent("agent-3")
    """

    def __init__(
        self,
        state_tracker: AgentStateTracker,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize agent controller.

        Args:
            state_tracker: AgentStateTracker instance
            logger: Optional logger
        """
        self.tracker = state_tracker
        self.logger = logger or self._default_logger()
        self._pause_requested: dict[int, bool] = {}  # wave_number → pause flag

    async def follow_agent(
        self,
        agent_id: str,
        message_callback: Optional[Callable[[Any], None]] = None
    ) -> None:
        """
        Follow agent's message stream in real-time.

        Streams all messages from agent to callback function.
        Blocks until agent completes or fails.

        Args:
            agent_id: Agent to follow
            message_callback: Optional callback for each message
                            Signature: callback(message) -> None

        Raises:
            KeyError: If agent not found
            ValueError: If agent not started

        Example:
            def print_message(msg):
                print(f"Message: {msg}")

            await controller.follow_agent("agent-1", print_message)
        """
        # Verify agent exists
        state = self.tracker.get_state(agent_id)

        if not state.started_at:
            raise ValueError(f"Agent {agent_id} has not started yet")

        self.logger.info(f"Following agent {agent_id}")

        # Get current message count
        start_index = len(state.all_messages)

        # Poll for new messages until agent finishes
        try:
            while not state.is_finished:
                # Get updated state
                state = self.tracker.get_state(agent_id)

                # Check for new messages
                current_messages = state.all_messages
                if len(current_messages) > start_index:
                    # Process new messages
                    for msg in current_messages[start_index:]:
                        if message_callback:
                            message_callback(msg)

                    start_index = len(current_messages)

                # Brief sleep to avoid tight polling
                await asyncio.sleep(0.1)

            # Agent finished - get final state
            state = self.tracker.get_state(agent_id)

            if state.is_complete:
                self.logger.info(
                    f"Agent {agent_id} completed successfully "
                    f"({state.duration_minutes:.1f} min, ${state.cost_usd:.2f})"
                )
            else:
                self.logger.error(
                    f"Agent {agent_id} failed: {state.error_message}"
                )

        except KeyboardInterrupt:
            self.logger.info(f"Stopped following agent {agent_id}")
            raise

    def pause_wave(self, wave_number: int) -> None:
        """
        Request wave pause after current agents complete.

        Does NOT immediately stop agents. Instead, sets flag that prevents
        new agents from starting after current agents finish.

        Args:
            wave_number: Wave to pause

        Example:
            # Wave 2 has 3 agents, 2 active, 1 pending
            controller.pause_wave(2)
            # Active agents complete
            # Pending agent does NOT start
            # Wave paused
        """
        self._pause_requested[wave_number] = True
        self.logger.info(f"Wave {wave_number} pause requested (will pause after active agents)")

    def resume_wave(self, wave_number: int) -> None:
        """
        Resume paused wave.

        Clears pause flag, allowing pending agents to start.

        Args:
            wave_number: Wave to resume
        """
        self._pause_requested[wave_number] = False
        self.logger.info(f"Wave {wave_number} resumed")

    def is_wave_paused(self, wave_number: int) -> bool:
        """
        Check if wave is paused.

        Args:
            wave_number: Wave to check

        Returns:
            True if pause requested, False otherwise
        """
        return self._pause_requested.get(wave_number, False)

    def should_start_agent(self, agent_id: str) -> bool:
        """
        Check if agent should start (respects wave pause).

        Args:
            agent_id: Agent to check

        Returns:
            True if agent can start, False if wave paused

        Raises:
            KeyError: If agent not found
        """
        state = self.tracker.get_state(agent_id)
        wave_number = state.wave_number

        if self.is_wave_paused(wave_number):
            self.logger.info(
                f"Agent {agent_id} blocked by wave {wave_number} pause"
            )
            return False

        return True

    async def retry_agent(
        self,
        agent_id: str,
        task_executor: Optional[Callable[[AgentState], Any]] = None
    ) -> None:
        """
        Retry failed agent from last checkpoint.

        Creates new agent state with checkpoint data and re-executes task.

        Args:
            agent_id: Failed agent to retry
            task_executor: Optional async function to execute agent task
                          Signature: async task_executor(state) -> None

        Raises:
            KeyError: If agent not found
            ValueError: If agent not failed or no checkpoint

        Example:
            async def execute_task(state: AgentState):
                # Execute agent task
                pass

            await controller.retry_agent("agent-3", execute_task)

        Note:
            This is a stub implementation. Full retry logic requires:
            - Checkpoint serialization/deserialization
            - Task execution framework integration
            - State restoration
        """
        # Verify agent exists and is failed
        state = self.tracker.get_state(agent_id)

        if not state.is_failed:
            raise ValueError(
                f"Agent {agent_id} is not failed (status: {state.status})"
            )

        if not state.last_checkpoint:
            raise ValueError(
                f"Agent {agent_id} has no checkpoint for retry"
            )

        self.logger.info(
            f"Retrying agent {agent_id} from checkpoint "
            f"(original duration: {state.duration_minutes:.1f} min)"
        )

        # Create new agent ID for retry
        retry_id = f"{agent_id}-retry-1"
        retry_count = 1

        # Ensure unique retry ID
        while retry_id in self.tracker.agents:
            retry_count += 1
            retry_id = f"{agent_id}-retry-{retry_count}"

        # Register retry agent with original task
        retry_state = self.tracker.register_agent(
            agent_id=retry_id,
            wave_number=state.wave_number,
            agent_type=state.agent_type,
            task_description=f"[RETRY] {state.task_description}"
        )

        # TODO: Restore checkpoint state
        # This requires checkpoint format specification and
        # integration with task execution framework

        if task_executor:
            # Execute task with retry state
            self.tracker.mark_started(retry_id)
            try:
                await task_executor(retry_state)
                self.tracker.mark_complete(retry_id)
                self.logger.info(f"Agent {retry_id} completed successfully")
            except Exception as e:
                self.tracker.mark_failed(retry_id, str(e))
                self.logger.error(f"Agent {retry_id} failed again: {e}")
                raise
        else:
            self.logger.warning(
                f"No task executor provided for retry {retry_id} - agent registered but not executed"
            )

    def get_wave_status(self, wave_number: int) -> dict:
        """
        Get comprehensive wave status.

        Args:
            wave_number: Wave to query

        Returns:
            Dict with:
                - summary: Wave summary stats
                - agents: List of agent states
                - paused: Pause status
                - bottleneck: Slowest active agent (if any)
        """
        summary = self.tracker.get_wave_summary(wave_number)
        agents = self.tracker.get_wave_agents(wave_number)

        # Find bottleneck (slowest active agent)
        active_agents = [a for a in agents if a.is_active]
        bottleneck = None

        if active_agents:
            # Sort by duration descending
            bottleneck = max(active_agents, key=lambda a: a.duration_minutes)

        return {
            'summary': summary,
            'agents': [a.to_dict() for a in agents],
            'paused': self.is_wave_paused(wave_number),
            'bottleneck': bottleneck.to_dict() if bottleneck else None
        }

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
