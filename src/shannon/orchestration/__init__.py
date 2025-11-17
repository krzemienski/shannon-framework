"""Shannon Orchestration Layer - Infrastructure components.

V5: Simplified to infrastructure only.
Custom skills framework (TaskParser, ExecutionPlanner) archived.
Shannon V5 uses Shannon Framework Claude Code skills instead.

Components:
- StateManager: Checkpoint and rollback management
- AgentPool: Parallel agent execution infrastructure

Created for: Shannon V5
Purpose: Provide execution infrastructure (not orchestration logic)
"""

from shannon.orchestration.state_manager import StateManager, Checkpoint
from shannon.orchestration.agent_pool import AgentPool, Agent, AgentTask

__all__ = [
    'StateManager',
    'Checkpoint',
    'AgentPool',
    'Agent',
    'AgentTask',
]
