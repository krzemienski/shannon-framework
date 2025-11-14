"""
Shannon CLI V3.0 - Agent Control System

Provides agent state tracking, control, and message routing for wave execution.

Main Components:
- AgentState: Complete agent state snapshot
- AgentStateTracker: Thread-safe state management
- AgentController: High-level control (follow, pause, retry)
- MessageRouter: Message distribution to agents

Public API:
    from shannon.agents import (
        AgentState,
        AgentStateTracker,
        AgentController,
        MessageRouter,
        AgentMessageCollector
    )

    # Create tracker
    tracker = AgentStateTracker()

    # Register agents
    state = tracker.register_agent(
        agent_id="agent-1",
        wave_number=2,
        agent_type="backend-builder",
        task_description="Build authentication API"
    )

    # Create controller
    controller = AgentController(tracker)

    # Create router
    router = MessageRouter(tracker)
    router.register_agent("agent-1")

    # Use with SDK interceptor
    collector = router.create_collector()
    # ... integrate with MessageInterceptor

    # Control operations
    await controller.follow_agent("agent-1")
    controller.pause_wave(2)
    await controller.retry_agent("agent-1")

Architecture:
    See SHANNON_CLI_V3_ARCHITECTURE.md sections:
    - 2.4 Agent Control (500 lines)
    - 4.1 SDK Message Interception Strategy

Implementation:
    - state_tracker.py: AgentState, AgentStateTracker (250 lines)
    - controller.py: AgentController (150 lines)
    - message_router.py: MessageRouter (100 lines)
"""

from .state_tracker import AgentState, AgentStateTracker
from .controller import AgentController
from .message_router import MessageRouter, AgentMessageCollector

__all__ = [
    'AgentState',
    'AgentStateTracker',
    'AgentController',
    'MessageRouter',
    'AgentMessageCollector',
]

__version__ = '3.0.0'
