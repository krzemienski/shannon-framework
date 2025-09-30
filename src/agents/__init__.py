"""
Shannon Framework - Agent System
=================================

Evolutionary agent system with genetic algorithms.
"""

from .dna import (
    # Gene Types
    GeneType,
    ToolPreferenceGene,
    MCPAffinityGene,
    ParallelismGene,
    MemoryTierGene,
    ErrorStrategyGene,
    TopologyGene,
    OptimizationGene,

    # Core Classes
    Gene,
    AgentDNA,
    FitnessEvaluator,
    EvolutionEngine,
)

__all__ = [
    # Gene Types
    "GeneType",
    "ToolPreferenceGene",
    "MCPAffinityGene",
    "ParallelismGene",
    "MemoryTierGene",
    "ErrorStrategyGene",
    "TopologyGene",
    "OptimizationGene",

    # Core Classes
    "Gene",
    "AgentDNA",
    "FitnessEvaluator",
    "EvolutionEngine",
]