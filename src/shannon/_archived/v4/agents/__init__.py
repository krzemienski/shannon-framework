"""Agent implementations for specialized tasks.

Provides concrete agent types for different roles:
- ResearchAgent: Library discovery and documentation research
- AnalysisAgent: Code analysis and complexity assessment
- TestingAgent: Test execution and validation
- ValidationAgent: Result validation and verification
- GitAgent: Git operations and commit management
- PlanningAgent: Task planning and dependency resolution
- MonitoringAgent: Progress tracking and metrics collection

Part of: Wave 6 - Agent Coordination
"""

from .base import BaseAgent
from .research import ResearchAgent
from .analysis import AnalysisAgent
from .testing import TestingAgent
from .validation import ValidationAgent
from .git import GitAgent
from .planning import PlanningAgent
from .monitoring import MonitoringAgent

__all__ = [
    'BaseAgent',
    'ResearchAgent',
    'AnalysisAgent',
    'TestingAgent',
    'ValidationAgent',
    'GitAgent',
    'PlanningAgent',
    'MonitoringAgent'
]
