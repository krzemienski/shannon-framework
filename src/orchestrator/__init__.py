"""
Shannon Framework v4 - Sub-Agent Orchestrator

Purpose: Multi-agent coordination with dependency management.

Components:
  - SubAgentOrchestrator: Main orchestrator
  - DependencyResolver: Dependency graph resolution
  - Models: OrchestrationPlan, AgentTask, AgentResult

Orchestration Strategies:
  - PARALLEL: All agents run in parallel
  - SEQUENTIAL: Agents run one by one
  - DEPENDENCY: Respect dependency graph (recommended)
  - PRIORITY: Execute by priority order

Features:
  - Dependency resolution with cycle detection
  - Parallel execution with configurable limits
  - Retry logic with exponential backoff
  - SITREP collection and consolidation
  - Fail-fast support
  - Critical path analysis

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    OrchestrationPlan,
    OrchestrationResult,
    AgentTask,
    AgentResult,
    AgentStatus,
    AgentType,
    OrchestrationStrategy,
)
from .dependency import (
    DependencyResolver,
    CircularDependencyError,
)
from .orchestrator import (
    SubAgentOrchestrator,
    OrchestrationError,
)

__all__ = [
    # Main orchestrator
    'SubAgentOrchestrator',

    # Models
    'OrchestrationPlan',
    'OrchestrationResult',
    'AgentTask',
    'AgentResult',

    # Enums
    'AgentStatus',
    'AgentType',
    'OrchestrationStrategy',

    # Dependency resolution
    'DependencyResolver',

    # Exceptions
    'CircularDependencyError',
    'OrchestrationError',
]

__version__ = '1.0.0'


# Convenience functions

def create_plan(
    name: str,
    strategy: str = "dependency",
    max_parallel: int = 8,
    fail_fast: bool = False
) -> OrchestrationPlan:
    """
    Create orchestration plan.

    Args:
        name: Plan name
        strategy: Strategy (parallel, sequential, dependency, priority)
        max_parallel: Max parallel agents
        fail_fast: Stop on first failure

    Returns:
        OrchestrationPlan instance
    """
    import uuid
    return OrchestrationPlan(
        id=f"plan_{uuid.uuid4().hex[:8]}",
        name=name,
        strategy=OrchestrationStrategy[strategy.upper()],
        max_parallel=max_parallel,
        fail_fast=fail_fast
    )


def create_task(
    name: str,
    prompt: str,
    agent_type: str = "custom",
    priority: int = 0,
    dependencies: list = None,
    **kwargs
) -> AgentTask:
    """
    Create agent task.

    Args:
        name: Task name
        prompt: Agent prompt
        agent_type: Agent type
        priority: Priority (higher = more important)
        dependencies: List of dependency task IDs
        **kwargs: Additional task parameters

    Returns:
        AgentTask instance
    """
    import uuid
    return AgentTask(
        id=kwargs.get('id', f"agent_{uuid.uuid4().hex[:8]}"),
        name=name,
        agent_type=AgentType[agent_type.upper()],
        prompt=prompt,
        priority=priority,
        dependencies=dependencies or [],
        **{k: v for k, v in kwargs.items() if k != 'id'}
    )
