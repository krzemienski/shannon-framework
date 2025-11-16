"""Base agent implementation."""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from ..agent_pool import AgentRole, AgentStatus, AgentTask


@dataclass
class AgentResult:
    """Result from agent execution."""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    duration: float = 0.0
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseAgent(ABC):
    """Base class for all specialized agents."""

    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        project_root: Optional[Path] = None
    ):
        """Initialize base agent.

        Args:
            agent_id: Unique agent identifier
            role: Agent specialization
            project_root: Project directory
        """
        self.agent_id = agent_id
        self.role = role
        self.project_root = project_root or Path.cwd()
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute assigned task.

        Args:
            task: Task to execute

        Returns:
            Execution result
        """
        pass

    async def run_task(self, task: AgentTask) -> AgentResult:
        """Run task with status tracking.

        Args:
            task: Task to run

        Returns:
            Task result
        """
        self.current_task = task
        self.status = AgentStatus.ACTIVE
        start_time = datetime.now()

        try:
            result = await self.execute(task)
            result.duration = (datetime.now() - start_time).total_seconds()
            self.status = AgentStatus.IDLE if result.success else AgentStatus.FAILED
            return result

        except Exception as e:
            self.status = AgentStatus.FAILED
            return AgentResult(
                success=False,
                error=str(e),
                duration=(datetime.now() - start_time).total_seconds()
            )

        finally:
            self.current_task = None

    def get_status(self) -> Dict:
        """Get current agent status."""
        return {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'status': self.status.value,
            'current_task': self.current_task.task_id if self.current_task else None
        }
