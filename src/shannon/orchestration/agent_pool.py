"""Agent Pool Management System.

Manages a pool of specialized agents for parallel execution:
- Pool size: 8 active / 50 max
- Agent roles: Research, Analysis, Testing, Validation, Git, Planning, Monitoring
- Progress tracking per agent
- Resource allocation and task distribution

Part of: Wave 6 - Agent Coordination
"""

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import json


class AgentRole(Enum):
    """Agent specialization roles."""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    TESTING = "testing"
    VALIDATION = "validation"
    GIT = "git"
    PLANNING = "planning"
    MONITORING = "monitoring"
    GENERIC = "generic"


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class AgentTask:
    """Task assigned to an agent."""
    task_id: str
    description: str
    role: AgentRole
    priority: int = 5
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None


@dataclass
class Agent:
    """Individual agent in the pool."""
    agent_id: str
    role: AgentRole
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[AgentTask] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_time: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'status': self.status.value,
            'current_task': self.current_task.task_id if self.current_task else None,
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'total_time': self.total_time,
            'last_active': self.last_active.isoformat()
        }


class AgentPool:
    """Manages pool of agents for parallel execution.

    Features:
    - Dynamic agent allocation (8 active / 50 max)
    - Role-based task assignment
    - Priority queue management
    - Progress tracking
    - Resource monitoring
    """

    def __init__(
        self,
        max_active: int = 8,
        max_total: int = 50,
        project_root: Optional[Path] = None
    ):
        """Initialize agent pool.

        Args:
            max_active: Maximum concurrent active agents
            max_total: Maximum total agents in pool
            project_root: Project directory for context
        """
        self.max_active = max_active
        self.max_total = max_total
        self.project_root = project_root or Path.cwd()

        # Agent tracking
        self.agents: Dict[str, Agent] = {}
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: Dict[str, AgentTask] = {}
        self.failed_tasks: Dict[str, AgentTask] = {}

        # Locks for thread safety
        self._agent_lock = asyncio.Lock()
        self._task_lock = asyncio.Lock()

        # Statistics
        self.total_tasks_processed = 0
        self.pool_start_time = time.time()

    async def create_agent(self, role: AgentRole) -> Agent:
        """Create a new agent with specified role.

        Args:
            role: Agent specialization

        Returns:
            Created agent instance
        """
        async with self._agent_lock:
            if len(self.agents) >= self.max_total:
                raise RuntimeError(f"Agent pool at maximum capacity ({self.max_total})")

            agent_id = f"{role.value}_{len(self.agents) + 1}"
            agent = Agent(agent_id=agent_id, role=role)
            self.agents[agent_id] = agent

            return agent

    async def assign_task(self, task: AgentTask) -> Optional[Agent]:
        """Assign task to available agent.

        Args:
            task: Task to assign

        Returns:
            Agent assigned to task, or None if none available
        """
        async with self._agent_lock:
            # Find agent with matching role that's idle
            available_agents = [
                agent for agent in self.agents.values()
                if agent.role == task.role and agent.status == AgentStatus.IDLE
            ]

            if not available_agents:
                # No matching agent available, queue task
                async with self._task_lock:
                    self.task_queue.append(task)
                return None

            # Assign to first available agent
            agent = available_agents[0]
            agent.status = AgentStatus.ACTIVE
            agent.current_task = task
            agent.last_active = datetime.now()

            task.started_at = datetime.now()

            return agent

    async def complete_task(
        self,
        agent_id: str,
        result: Optional[Dict] = None,
        error: Optional[str] = None
    ):
        """Mark task as completed.

        Args:
            agent_id: ID of agent completing task
            result: Task result data
            error: Error message if task failed
        """
        async with self._agent_lock:
            agent = self.agents.get(agent_id)
            if not agent or not agent.current_task:
                return

            task = agent.current_task
            task.completed_at = datetime.now()
            task.result = result
            task.error = error

            # Update agent stats
            if error:
                agent.tasks_failed += 1
                agent.status = AgentStatus.FAILED
                self.failed_tasks[task.task_id] = task
            else:
                agent.tasks_completed += 1
                agent.status = AgentStatus.IDLE
                self.completed_tasks[task.task_id] = task

            # Calculate task duration
            if task.started_at:
                duration = (task.completed_at - task.started_at).total_seconds()
                agent.total_time += duration

            agent.current_task = None
            self.total_tasks_processed += 1

            # Try to assign next queued task
            await self._process_queue()

    async def _process_queue(self):
        """Process queued tasks and assign to available agents."""
        async with self._task_lock:
            if not self.task_queue:
                return

            # Sort by priority (higher first)
            self.task_queue.sort(key=lambda t: t.priority, reverse=True)

            # Try to assign tasks
            remaining_tasks = []
            for task in self.task_queue:
                assigned = await self.assign_task(task)
                if not assigned:
                    remaining_tasks.append(task)

            self.task_queue = remaining_tasks

    async def submit_task(self, task: AgentTask) -> str:
        """Submit task to pool.

        Args:
            task: Task to submit

        Returns:
            Task ID
        """
        # Check if agent with required role exists
        role_agents = [a for a in self.agents.values() if a.role == task.role]

        if not role_agents:
            # Create agent for this role if under max
            if len(self.agents) < self.max_total:
                await self.create_agent(task.role)

        # Try to assign immediately or queue
        await self.assign_task(task)

        return task.task_id

    def get_active_agents(self) -> List[Agent]:
        """Get list of currently active agents."""
        return [
            agent for agent in self.agents.values()
            if agent.status in (AgentStatus.ACTIVE, AgentStatus.BUSY)
        ]

    def get_agent_stats(self) -> Dict:
        """Get pool statistics."""
        active_agents = self.get_active_agents()
        idle_agents = [a for a in self.agents.values() if a.status == AgentStatus.IDLE]

        return {
            'total_agents': len(self.agents),
            'active_agents': len(active_agents),
            'idle_agents': len(idle_agents),
            'max_active': self.max_active,
            'max_total': self.max_total,
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'failed_tasks': len(self.failed_tasks),
            'total_processed': self.total_tasks_processed,
            'pool_uptime': time.time() - self.pool_start_time
        }

    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    async def shutdown(self):
        """Shutdown agent pool gracefully."""
        # Wait for active tasks to complete
        timeout = 30.0
        start = time.time()

        while self.get_active_agents() and (time.time() - start) < timeout:
            await asyncio.sleep(0.5)

        # Force stop remaining agents
        for agent in self.agents.values():
            if agent.status in (AgentStatus.ACTIVE, AgentStatus.BUSY):
                agent.status = AgentStatus.FAILED
                if agent.current_task:
                    agent.current_task.error = "Shutdown timeout"

    def to_dict(self) -> Dict:
        """Convert pool state to dictionary."""
        return {
            'agents': [agent.to_dict() for agent in self.agents.values()],
            'stats': self.get_agent_stats(),
            'active_agents': [a.agent_id for a in self.get_active_agents()],
            'queued_tasks': len(self.task_queue)
        }


class AgentCoordinator:
    """Coordinates multiple agent pools for complex workflows.

    Features:
    - Multi-pool management
    - Cross-pool communication
    - Resource balancing
    - Global progress tracking
    """

    def __init__(self):
        """Initialize agent coordinator."""
        self.pools: Dict[str, AgentPool] = {}
        self.global_tasks: Dict[str, AgentTask] = {}

    async def create_pool(
        self,
        pool_id: str,
        max_active: int = 8,
        max_total: int = 50
    ) -> AgentPool:
        """Create new agent pool.

        Args:
            pool_id: Unique pool identifier
            max_active: Max concurrent agents
            max_total: Max total agents

        Returns:
            Created pool
        """
        if pool_id in self.pools:
            return self.pools[pool_id]

        pool = AgentPool(max_active=max_active, max_total=max_total)
        self.pools[pool_id] = pool

        return pool

    async def submit_global_task(
        self,
        task: AgentTask,
        pool_id: Optional[str] = None
    ) -> str:
        """Submit task to coordinator for routing.

        Args:
            task: Task to submit
            pool_id: Specific pool to use (optional)

        Returns:
            Task ID
        """
        self.global_tasks[task.task_id] = task

        if pool_id:
            # Submit to specific pool
            pool = self.pools.get(pool_id)
            if pool:
                return await pool.submit_task(task)
        else:
            # Find best pool based on role and load
            best_pool = self._find_best_pool(task.role)
            if best_pool:
                return await best_pool.submit_task(task)

        raise RuntimeError("No suitable pool found for task")

    def _find_best_pool(self, role: AgentRole) -> Optional[AgentPool]:
        """Find best pool for task based on role and load."""
        if not self.pools:
            return None

        # Find pool with matching role agents and lowest load
        candidate_pools = []

        for pool in self.pools.values():
            role_agents = [a for a in pool.agents.values() if a.role == role]
            if role_agents:
                active_count = len(pool.get_active_agents())
                load = active_count / pool.max_active if pool.max_active > 0 else 1.0
                candidate_pools.append((pool, load))

        if not candidate_pools:
            # Return least loaded pool
            return min(self.pools.values(), key=lambda p: len(p.get_active_agents()))

        # Return pool with lowest load
        return min(candidate_pools, key=lambda x: x[1])[0]

    def get_global_stats(self) -> Dict:
        """Get statistics across all pools."""
        total_agents = sum(len(p.agents) for p in self.pools.values())
        total_active = sum(len(p.get_active_agents()) for p in self.pools.values())
        total_completed = sum(len(p.completed_tasks) for p in self.pools.values())
        total_failed = sum(len(p.failed_tasks) for p in self.pools.values())

        return {
            'pools': len(self.pools),
            'total_agents': total_agents,
            'total_active': total_active,
            'total_completed': total_completed,
            'total_failed': total_failed,
            'global_tasks': len(self.global_tasks)
        }

    async def shutdown_all(self):
        """Shutdown all pools."""
        for pool in self.pools.values():
            await pool.shutdown()


# Convenience function for creating default pool
async def create_default_pool() -> AgentPool:
    """Create default agent pool with standard configuration."""
    pool = AgentPool(max_active=8, max_total=50)

    # Pre-create agents for common roles
    await pool.create_agent(AgentRole.RESEARCH)
    await pool.create_agent(AgentRole.ANALYSIS)
    await pool.create_agent(AgentRole.TESTING)
    await pool.create_agent(AgentRole.VALIDATION)
    await pool.create_agent(AgentRole.GIT)
    await pool.create_agent(AgentRole.PLANNING)

    return pool
