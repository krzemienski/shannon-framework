"""Shannon Framework - Swarm Intelligence Package"""

from .collective_intelligence import (
    SwarmType,
    SwarmAgent,
    PheromoneTrail,
    AntColonyOptimizer,
    ParticleSwarmOptimizer,
    FlockingController,
    SwarmCoordinator
)

__all__ = [
    'SwarmType',
    'SwarmAgent',
    'PheromoneTrail',
    'AntColonyOptimizer',
    'ParticleSwarmOptimizer',
    'FlockingController',
    'SwarmCoordinator'
]