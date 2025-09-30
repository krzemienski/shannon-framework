"""
Shannon Framework v2.1 - Core Module

Exports core orchestration, agent, and wave management classes.
"""

from .orchestrator import (
    WaveOrchestrator,
    ComplexityAnalyzer,
    WaveStrategy,
    AgentSpawner,
    ComplexityScore,
    OrchestrationDecision
)
from .agent import (
    BaseAgent,
    AgentState,
    AgentMetrics,
    AgentCapability,
    AgentResult
)
from .wave_config import (
    WaveConfig,
    WavePhase,
    AgentAllocation,
    ValidationLevel
)

__all__ = [
    # Orchestrator components
    'WaveOrchestrator',
    'ComplexityAnalyzer',
    'WaveStrategy',
    'AgentSpawner',
    'ComplexityScore',
    'OrchestrationDecision',

    # Agent components
    'BaseAgent',
    'AgentState',
    'AgentMetrics',
    'AgentCapability',
    'AgentResult',

    # Wave configuration
    'WaveConfig',
    'WavePhase',
    'AgentAllocation',
    'ValidationLevel',
]

__version__ = '2.1.0'