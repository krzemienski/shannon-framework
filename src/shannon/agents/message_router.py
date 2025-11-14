"""
Shannon CLI V3.0 - Message Router

Routes SDK messages to appropriate agent collectors.
Enables parallel message distribution and agent-specific filtering.

Architecture:
- MessageCollector integration with MessageInterceptor
- Agent-specific message filtering
- Parallel message distribution to multiple agents
- Thread-safe routing logic

Usage:
    router = MessageRouter(state_tracker)

    # Register collectors for agents
    router.register_agent("agent-1", [MetricsCollector(), ContextCollector()])

    # Create router collector for SDK interceptor
    collector = router.create_collector()

    # Use with interceptor
    interceptor = MessageInterceptor()
    async for msg in interceptor.intercept(query_iter, [collector]):
        yield msg
"""

from typing import Dict, List, Optional, Any
from .state_tracker import AgentStateTracker
from shannon.sdk.interceptor import MessageCollector
import asyncio
import logging


class AgentMessageCollector(MessageCollector):
    """
    Message collector for specific agent.

    Routes messages to agent's state tracker and optional sub-collectors.

    This is the bridge between SDK message stream and agent state tracking.
    """

    def __init__(
        self,
        agent_id: str,
        state_tracker: AgentStateTracker,
        sub_collectors: Optional[List[MessageCollector]] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize agent message collector.

        Args:
            agent_id: Agent to collect for
            state_tracker: AgentStateTracker instance
            sub_collectors: Optional additional collectors
            logger: Optional logger
        """
        self.agent_id = agent_id
        self.tracker = state_tracker
        self.sub_collectors = sub_collectors or []
        self.logger = logger or self._default_logger()

    async def process(self, message: Any) -> None:
        """
        Process message for agent.

        Updates agent state and forwards to sub-collectors.

        Args:
            message: SDK message
        """
        try:
            # Add message to agent's history
            self.tracker.add_message(self.agent_id, message)

            # Extract message type and update agent state
            await self._update_agent_state(message)

            # Forward to sub-collectors
            for collector in self.sub_collectors:
                try:
                    await collector.process(message)
                except Exception as e:
                    self.logger.error(
                        f"Sub-collector {collector.__class__.__name__} error: {e}"
                    )

        except Exception as e:
            self.logger.error(
                f"Error processing message for agent {self.agent_id}: {e}"
            )

    async def on_stream_complete(self) -> None:
        """Called when message stream completes."""
        # Forward to sub-collectors
        for collector in self.sub_collectors:
            try:
                await collector.on_stream_complete()
            except Exception as e:
                self.logger.error(
                    f"Sub-collector {collector.__class__.__name__} completion error: {e}"
                )

    async def on_stream_error(self, error: Exception) -> None:
        """
        Called when message stream errors.

        Args:
            error: Exception that occurred
        """
        # Forward to sub-collectors
        for collector in self.sub_collectors:
            try:
                await collector.on_stream_error(error)
            except Exception as e:
                self.logger.error(
                    f"Sub-collector {collector.__class__.__name__} error handling error: {e}"
                )

    async def _update_agent_state(self, message: Any) -> None:
        """
        Update agent state based on message content.

        Extracts information from message and updates appropriate
        agent state fields.

        Args:
            message: SDK message to process

        Note:
            This is a simplified implementation. Full implementation requires:
            - SDK message type detection (AssistantMessage, ToolUseBlock, etc.)
            - Cost extraction from usage metadata
            - Token counting from message content
            - Progress estimation heuristics
        """
        # TODO: Implement full message parsing when SDK integration is complete
        # For now, just log the message type
        message_type = type(message).__name__
        self.logger.debug(f"Agent {self.agent_id} received {message_type}")

        # Placeholder: Update progress based on message count
        # In real implementation, this would use message content
        state = self.tracker.get_state(self.agent_id)
        message_count = len(state.all_messages)

        # Simple progress heuristic: 10% per message (cap at 90%)
        progress = min(message_count * 10, 90)
        self.tracker.update_progress(self.agent_id, progress)

    def _default_logger(self) -> logging.Logger:
        """Create default logger if none provided."""
        return logging.getLogger(__name__)


class MessageRouter:
    """
    Routes messages to appropriate agent collectors.

    Manages agent-to-collector mappings and provides unified
    MessageCollector for SDK interceptor integration.

    Thread Safety:
        All operations are thread-safe via AgentStateTracker's lock.

    Usage:
        router = MessageRouter(state_tracker)

        # Register agent collectors
        router.register_agent("agent-1", [MetricsCollector()])
        router.register_agent("agent-2", [ContextCollector()])

        # Create unified collector
        collector = router.create_collector()

        # Use with interceptor
        interceptor = MessageInterceptor()
        async for msg in interceptor.intercept(query_iter, [collector]):
            # Messages automatically routed to registered agents
            yield msg
    """

    def __init__(
        self,
        state_tracker: AgentStateTracker,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize message router.

        Args:
            state_tracker: AgentStateTracker instance
            logger: Optional logger
        """
        self.tracker = state_tracker
        self.logger = logger or self._default_logger()
        self._collectors: Dict[str, AgentMessageCollector] = {}

    def register_agent(
        self,
        agent_id: str,
        sub_collectors: Optional[List[MessageCollector]] = None
    ) -> AgentMessageCollector:
        """
        Register agent for message routing.

        Creates AgentMessageCollector for agent and registers it.

        Args:
            agent_id: Agent to register
            sub_collectors: Optional additional collectors

        Returns:
            Created AgentMessageCollector

        Raises:
            KeyError: If agent not found in state tracker
            ValueError: If agent already registered
        """
        # Verify agent exists
        _ = self.tracker.get_state(agent_id)

        if agent_id in self._collectors:
            raise ValueError(f"Agent {agent_id} already registered")

        collector = AgentMessageCollector(
            agent_id=agent_id,
            state_tracker=self.tracker,
            sub_collectors=sub_collectors,
            logger=self.logger
        )

        self._collectors[agent_id] = collector
        self.logger.info(f"Registered message collector for agent {agent_id}")

        return collector

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregister agent from message routing.

        Args:
            agent_id: Agent to unregister

        Raises:
            KeyError: If agent not registered
        """
        if agent_id not in self._collectors:
            raise KeyError(f"Agent {agent_id} not registered")

        del self._collectors[agent_id]
        self.logger.info(f"Unregistered message collector for agent {agent_id}")

    def get_collector(self, agent_id: str) -> AgentMessageCollector:
        """
        Get collector for agent.

        Args:
            agent_id: Agent to get collector for

        Returns:
            AgentMessageCollector instance

        Raises:
            KeyError: If agent not registered
        """
        if agent_id not in self._collectors:
            raise KeyError(f"Agent {agent_id} not registered")

        return self._collectors[agent_id]

    def create_collector(self) -> MessageCollector:
        """
        Create unified collector that routes to all registered agents.

        Returns:
            MessageCollector that distributes to all agent collectors

        Usage:
            collector = router.create_collector()
            interceptor = MessageInterceptor()
            async for msg in interceptor.intercept(query_iter, [collector]):
                yield msg
        """
        return RouterCollector(self._collectors, self.logger)

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


class RouterCollector(MessageCollector):
    """
    Collector that distributes messages to multiple agent collectors.

    This is the unified collector returned by MessageRouter.create_collector()
    that forwards messages to all registered agent collectors.
    """

    def __init__(
        self,
        collectors: Dict[str, AgentMessageCollector],
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize router collector.

        Args:
            collectors: Dict of agent_id → AgentMessageCollector
            logger: Optional logger
        """
        self.collectors = collectors
        self.logger = logger or logging.getLogger(__name__)

    async def process(self, message: Any) -> None:
        """
        Distribute message to all agent collectors.

        Args:
            message: SDK message
        """
        # Process in parallel for all agents
        tasks = [
            collector.process(message)
            for collector in self.collectors.values()
        ]

        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Log any errors
        for agent_id, result in zip(self.collectors.keys(), results):
            if isinstance(result, Exception):
                self.logger.error(
                    f"Error processing message for agent {agent_id}: {result}"
                )

    async def on_stream_complete(self) -> None:
        """Forward completion to all agent collectors."""
        tasks = [
            collector.on_stream_complete()
            for collector in self.collectors.values()
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def on_stream_error(self, error: Exception) -> None:
        """
        Forward error to all agent collectors.

        Args:
            error: Exception that occurred
        """
        tasks = [
            collector.on_stream_error(error)
            for collector in self.collectors.values()
        ]
        await asyncio.gather(*tasks, return_exceptions=True)
