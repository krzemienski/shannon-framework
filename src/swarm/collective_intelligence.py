"""
Shannon Framework - Swarm Intelligence Module

Production-ready collective intelligence algorithms:
- Ant Colony Optimization (ACO) with pheromone trails
- Particle Swarm Optimization (PSO) for parameter tuning
- Flocking behavior with Reynolds rules
- Async swarm coordination
"""

import asyncio
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional, Tuple, Any
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SwarmType(Enum):
    """Types of swarm algorithms available"""
    ANT_COLONY = "ant_colony"
    PARTICLE_SWARM = "particle_swarm"
    FLOCKING = "flocking"
    HYBRID = "hybrid"


@dataclass
class SwarmAgent:
    """Individual agent in a swarm"""
    id: str
    position: np.ndarray
    velocity: np.ndarray
    fitness: float = 0.0
    best_position: np.ndarray = field(default_factory=lambda: np.array([]))
    best_fitness: float = float('-inf')
    pheromone_trail: List[Tuple[np.ndarray, float]] = field(default_factory=list)

    def __post_init__(self):
        if len(self.best_position) == 0:
            self.best_position = self.position.copy()


@dataclass
class PheromoneTrail:
    """Pheromone trail for ACO"""
    path: List[int]
    intensity: float
    evaporation_rate: float = 0.1
    timestamp: datetime = field(default_factory=datetime.now)

    def evaporate(self) -> None:
        """Apply pheromone evaporation"""
        self.intensity *= (1 - self.evaporation_rate)

    def reinforce(self, amount: float) -> None:
        """Add pheromone to trail"""
        self.intensity += amount


class AntColonyOptimizer:
    """
    Ant Colony Optimization implementation

    Uses pheromone trails and heuristic information to find optimal paths
    through solution spaces. Suitable for combinatorial optimization.
    """

    def __init__(
        self,
        n_ants: int = 50,
        evaporation_rate: float = 0.1,
        alpha: float = 1.0,  # pheromone importance
        beta: float = 2.0,   # heuristic importance
        q0: float = 0.9,     # exploitation vs exploration
        initial_pheromone: float = 0.1
    ):
        self.n_ants = n_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.q0 = q0
        self.initial_pheromone = initial_pheromone

        self.pheromone_matrix: Optional[np.ndarray] = None
        self.best_path: Optional[List[int]] = None
        self.best_cost: float = float('inf')
        self.iteration = 0

    def initialize_pheromones(self, n_nodes: int) -> None:
        """Initialize pheromone matrix"""
        self.pheromone_matrix = np.full(
            (n_nodes, n_nodes),
            self.initial_pheromone
        )

    def compute_transition_probabilities(
        self,
        current_node: int,
        unvisited: List[int],
        heuristic: np.ndarray
    ) -> np.ndarray:
        """
        Compute probabilities for transitioning to next node

        P_ij = (tau_ij^alpha * eta_ij^beta) / sum(tau_ik^alpha * eta_ik^beta)
        where tau is pheromone and eta is heuristic information
        """
        if len(unvisited) == 0:
            return np.array([])

        pheromones = self.pheromone_matrix[current_node, unvisited]
        heuristics = heuristic[current_node, unvisited]

        # Avoid division by zero
        heuristics = np.where(heuristics == 0, 1e-10, heuristics)

        numerator = (pheromones ** self.alpha) * (heuristics ** self.beta)
        denominator = numerator.sum()

        if denominator == 0:
            return np.ones(len(unvisited)) / len(unvisited)

        return numerator / denominator

    def select_next_node(
        self,
        current_node: int,
        unvisited: List[int],
        heuristic: np.ndarray
    ) -> int:
        """Select next node using pseudo-random proportional rule"""
        if len(unvisited) == 0:
            return current_node

        q = np.random.random()

        if q < self.q0:
            # Exploitation: choose best option
            pheromones = self.pheromone_matrix[current_node, unvisited]
            heuristics = heuristic[current_node, unvisited]
            values = (pheromones ** self.alpha) * (heuristics ** self.beta)
            best_idx = np.argmax(values)
            return unvisited[best_idx]
        else:
            # Exploration: probabilistic selection
            probabilities = self.compute_transition_probabilities(
                current_node, unvisited, heuristic
            )
            chosen_idx = np.random.choice(len(unvisited), p=probabilities)
            return unvisited[chosen_idx]

    def construct_solution(
        self,
        start_node: int,
        n_nodes: int,
        heuristic: np.ndarray,
        cost_matrix: np.ndarray
    ) -> Tuple[List[int], float]:
        """Construct a solution path for one ant"""
        path = [start_node]
        unvisited = list(range(n_nodes))
        unvisited.remove(start_node)
        total_cost = 0.0

        current = start_node

        while unvisited:
            next_node = self.select_next_node(current, unvisited, heuristic)
            path.append(next_node)
            total_cost += cost_matrix[current, next_node]
            unvisited.remove(next_node)
            current = next_node

        # Return to start
        total_cost += cost_matrix[current, start_node]
        path.append(start_node)

        return path, total_cost

    def update_pheromones(
        self,
        paths: List[List[int]],
        costs: List[float]
    ) -> None:
        """Update pheromone trails based on ant solutions"""
        # Evaporation
        self.pheromone_matrix *= (1 - self.evaporation_rate)

        # Deposit pheromones
        for path, cost in zip(paths, costs):
            if cost > 0:
                deposit = 1.0 / cost
                for i in range(len(path) - 1):
                    from_node = path[i]
                    to_node = path[i + 1]
                    self.pheromone_matrix[from_node, to_node] += deposit

    def optimize(
        self,
        cost_matrix: np.ndarray,
        heuristic: Optional[np.ndarray] = None,
        n_iterations: int = 100,
        start_node: int = 0
    ) -> Tuple[List[int], float]:
        """
        Run ACO optimization

        Args:
            cost_matrix: NxN matrix of costs between nodes
            heuristic: NxN matrix of heuristic values (e.g., 1/distance)
            n_iterations: Number of iterations to run
            start_node: Starting node for all ants

        Returns:
            (best_path, best_cost)
        """
        n_nodes = cost_matrix.shape[0]
        self.initialize_pheromones(n_nodes)

        if heuristic is None:
            # Use inverse of cost as heuristic
            heuristic = np.where(cost_matrix > 0, 1.0 / cost_matrix, 0)

        for iteration in range(n_iterations):
            paths = []
            costs = []

            # Each ant constructs a solution
            for _ in range(self.n_ants):
                path, cost = self.construct_solution(
                    start_node, n_nodes, heuristic, cost_matrix
                )
                paths.append(path)
                costs.append(cost)

                # Track best solution
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_path = path.copy()

            # Update pheromones
            self.update_pheromones(paths, costs)
            self.iteration += 1

            logger.debug(
                f"ACO Iteration {iteration}: "
                f"Best cost = {self.best_cost:.4f}"
            )

        return self.best_path, self.best_cost


class ParticleSwarmOptimizer:
    """
    Particle Swarm Optimization implementation

    Uses particles moving through solution space, influenced by personal
    and global best positions. Suitable for continuous optimization.
    """

    def __init__(
        self,
        n_particles: int = 30,
        n_dimensions: int = 10,
        w: float = 0.7,      # inertia weight
        c1: float = 1.5,     # cognitive component
        c2: float = 1.5,     # social component
        bounds: Optional[Tuple[float, float]] = None
    ):
        self.n_particles = n_particles
        self.n_dimensions = n_dimensions
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.bounds = bounds or (-100, 100)

        self.particles: List[SwarmAgent] = []
        self.global_best_position: Optional[np.ndarray] = None
        self.global_best_fitness: float = float('-inf')
        self.iteration = 0

    def initialize_swarm(self) -> None:
        """Initialize particle swarm with random positions and velocities"""
        self.particles = []

        for i in range(self.n_particles):
            position = np.random.uniform(
                self.bounds[0],
                self.bounds[1],
                self.n_dimensions
            )
            velocity = np.random.uniform(-1, 1, self.n_dimensions)

            agent = SwarmAgent(
                id=f"particle_{i}",
                position=position,
                velocity=velocity
            )
            self.particles.append(agent)

    def evaluate_fitness(
        self,
        fitness_func: Callable[[np.ndarray], float]
    ) -> None:
        """Evaluate fitness for all particles"""
        for particle in self.particles:
            fitness = fitness_func(particle.position)
            particle.fitness = fitness

            # Update personal best
            if fitness > particle.best_fitness:
                particle.best_fitness = fitness
                particle.best_position = particle.position.copy()

            # Update global best
            if fitness > self.global_best_fitness:
                self.global_best_fitness = fitness
                self.global_best_position = particle.position.copy()

    def update_velocities(self) -> None:
        """Update particle velocities using PSO formula"""
        for particle in self.particles:
            r1 = np.random.random(self.n_dimensions)
            r2 = np.random.random(self.n_dimensions)

            # v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
            cognitive = self.c1 * r1 * (particle.best_position - particle.position)
            social = self.c2 * r2 * (self.global_best_position - particle.position)

            particle.velocity = (
                self.w * particle.velocity +
                cognitive +
                social
            )

    def update_positions(self) -> None:
        """Update particle positions and enforce bounds"""
        for particle in self.particles:
            particle.position += particle.velocity

            # Enforce bounds
            particle.position = np.clip(
                particle.position,
                self.bounds[0],
                self.bounds[1]
            )

    def optimize(
        self,
        fitness_func: Callable[[np.ndarray], float],
        n_iterations: int = 100,
        verbose: bool = False
    ) -> Tuple[np.ndarray, float]:
        """
        Run PSO optimization

        Args:
            fitness_func: Function to maximize (takes position, returns fitness)
            n_iterations: Number of iterations to run
            verbose: Whether to log progress

        Returns:
            (best_position, best_fitness)
        """
        self.initialize_swarm()

        for iteration in range(n_iterations):
            self.evaluate_fitness(fitness_func)
            self.update_velocities()
            self.update_positions()
            self.iteration += 1

            if verbose and iteration % 10 == 0:
                logger.info(
                    f"PSO Iteration {iteration}: "
                    f"Best fitness = {self.global_best_fitness:.6f}"
                )

        return self.global_best_position, self.global_best_fitness


class FlockingController:
    """
    Flocking behavior implementation using Reynolds rules

    Three rules:
    1. Separation: Avoid crowding neighbors
    2. Alignment: Steer towards average heading of neighbors
    3. Cohesion: Steer towards average position of neighbors
    """

    def __init__(
        self,
        n_agents: int = 50,
        n_dimensions: int = 3,
        separation_radius: float = 5.0,
        alignment_radius: float = 10.0,
        cohesion_radius: float = 10.0,
        max_speed: float = 2.0,
        separation_weight: float = 1.5,
        alignment_weight: float = 1.0,
        cohesion_weight: float = 1.0
    ):
        self.n_agents = n_agents
        self.n_dimensions = n_dimensions
        self.separation_radius = separation_radius
        self.alignment_radius = alignment_radius
        self.cohesion_radius = cohesion_radius
        self.max_speed = max_speed
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight

        self.agents: List[SwarmAgent] = []
        self.iteration = 0

    def initialize_flock(self, bounds: Tuple[float, float] = (-50, 50)) -> None:
        """Initialize flock with random positions and velocities"""
        self.agents = []

        for i in range(self.n_agents):
            position = np.random.uniform(
                bounds[0],
                bounds[1],
                self.n_dimensions
            )
            velocity = np.random.uniform(-1, 1, self.n_dimensions)
            velocity = velocity / np.linalg.norm(velocity) * self.max_speed / 2

            agent = SwarmAgent(
                id=f"bird_{i}",
                position=position,
                velocity=velocity
            )
            self.agents.append(agent)

    def get_neighbors(
        self,
        agent: SwarmAgent,
        radius: float
    ) -> List[SwarmAgent]:
        """Get neighbors within radius of agent"""
        neighbors = []

        for other in self.agents:
            if other.id != agent.id:
                distance = np.linalg.norm(agent.position - other.position)
                if distance < radius:
                    neighbors.append(other)

        return neighbors

    def separation(self, agent: SwarmAgent) -> np.ndarray:
        """Compute separation steering force"""
        neighbors = self.get_neighbors(agent, self.separation_radius)

        if not neighbors:
            return np.zeros(self.n_dimensions)

        steering = np.zeros(self.n_dimensions)

        for neighbor in neighbors:
            diff = agent.position - neighbor.position
            distance = np.linalg.norm(diff)

            if distance > 0:
                # Weight by inverse of distance
                steering += diff / distance

        if np.linalg.norm(steering) > 0:
            steering = steering / np.linalg.norm(steering) * self.max_speed
            steering -= agent.velocity

        return steering * self.separation_weight

    def alignment(self, agent: SwarmAgent) -> np.ndarray:
        """Compute alignment steering force"""
        neighbors = self.get_neighbors(agent, self.alignment_radius)

        if not neighbors:
            return np.zeros(self.n_dimensions)

        avg_velocity = np.mean(
            [n.velocity for n in neighbors],
            axis=0
        )

        steering = avg_velocity - agent.velocity

        if np.linalg.norm(steering) > 0:
            steering = steering / np.linalg.norm(steering) * self.max_speed

        return steering * self.alignment_weight

    def cohesion(self, agent: SwarmAgent) -> np.ndarray:
        """Compute cohesion steering force"""
        neighbors = self.get_neighbors(agent, self.cohesion_radius)

        if not neighbors:
            return np.zeros(self.n_dimensions)

        center = np.mean(
            [n.position for n in neighbors],
            axis=0
        )

        desired = center - agent.position

        if np.linalg.norm(desired) > 0:
            desired = desired / np.linalg.norm(desired) * self.max_speed

        steering = desired - agent.velocity

        return steering * self.cohesion_weight

    def update_flock(self) -> None:
        """Update all agent positions based on flocking rules"""
        new_velocities = []

        for agent in self.agents:
            # Compute steering forces
            sep = self.separation(agent)
            ali = self.alignment(agent)
            coh = self.cohesion(agent)

            # Combine forces
            acceleration = sep + ali + coh
            new_velocity = agent.velocity + acceleration

            # Limit speed
            speed = np.linalg.norm(new_velocity)
            if speed > self.max_speed:
                new_velocity = new_velocity / speed * self.max_speed

            new_velocities.append(new_velocity)

        # Update all agents
        for agent, new_velocity in zip(self.agents, new_velocities):
            agent.velocity = new_velocity
            agent.position += agent.velocity

        self.iteration += 1

    def simulate(self, n_steps: int = 100) -> List[np.ndarray]:
        """
        Run flocking simulation

        Returns:
            List of position arrays at each timestep
        """
        positions_history = []

        for _ in range(n_steps):
            self.update_flock()
            positions = np.array([a.position for a in self.agents])
            positions_history.append(positions)

        return positions_history


class SwarmCoordinator:
    """
    High-level coordinator for swarm intelligence operations

    Manages multiple swarm algorithms and provides unified interface
    for async swarm execution.
    """

    def __init__(self):
        self.active_swarms: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}

    async def run_ant_colony_async(
        self,
        swarm_id: str,
        cost_matrix: np.ndarray,
        **kwargs
    ) -> Tuple[List[int], float]:
        """Run ACO asynchronously"""
        logger.info(f"Starting ACO swarm: {swarm_id}")

        aco = AntColonyOptimizer(**kwargs)
        self.active_swarms[swarm_id] = aco

        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            aco.optimize,
            cost_matrix
        )

        self.results[swarm_id] = {
            'type': SwarmType.ANT_COLONY,
            'best_path': result[0],
            'best_cost': result[1],
            'timestamp': datetime.now()
        }

        return result

    async def run_particle_swarm_async(
        self,
        swarm_id: str,
        fitness_func: Callable[[np.ndarray], float],
        n_dimensions: int,
        **kwargs
    ) -> Tuple[np.ndarray, float]:
        """Run PSO asynchronously"""
        logger.info(f"Starting PSO swarm: {swarm_id}")

        pso = ParticleSwarmOptimizer(n_dimensions=n_dimensions, **kwargs)
        self.active_swarms[swarm_id] = pso

        # Run in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            pso.optimize,
            fitness_func
        )

        self.results[swarm_id] = {
            'type': SwarmType.PARTICLE_SWARM,
            'best_position': result[0],
            'best_fitness': result[1],
            'timestamp': datetime.now()
        }

        return result

    async def run_flocking_async(
        self,
        swarm_id: str,
        n_steps: int = 100,
        **kwargs
    ) -> List[np.ndarray]:
        """Run flocking simulation asynchronously"""
        logger.info(f"Starting flocking swarm: {swarm_id}")

        flock = FlockingController(**kwargs)
        flock.initialize_flock()
        self.active_swarms[swarm_id] = flock

        # Run in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            flock.simulate,
            n_steps
        )

        self.results[swarm_id] = {
            'type': SwarmType.FLOCKING,
            'positions_history': result,
            'n_steps': n_steps,
            'timestamp': datetime.now()
        }

        return result

    async def run_parallel_swarms(
        self,
        swarm_configs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Run multiple swarms in parallel

        Args:
            swarm_configs: List of dicts with keys:
                - swarm_id: str
                - swarm_type: SwarmType
                - params: dict of algorithm-specific params

        Returns:
            Dict mapping swarm_id to results
        """
        tasks = []

        for config in swarm_configs:
            swarm_id = config['swarm_id']
            swarm_type = config['swarm_type']
            params = config.get('params', {})

            if swarm_type == SwarmType.ANT_COLONY:
                task = self.run_ant_colony_async(
                    swarm_id,
                    params.pop('cost_matrix'),
                    **params
                )
            elif swarm_type == SwarmType.PARTICLE_SWARM:
                task = self.run_particle_swarm_async(
                    swarm_id,
                    params.pop('fitness_func'),
                    params.pop('n_dimensions'),
                    **params
                )
            elif swarm_type == SwarmType.FLOCKING:
                task = self.run_flocking_async(swarm_id, **params)
            else:
                logger.warning(f"Unknown swarm type: {swarm_type}")
                continue

            tasks.append(task)

        # Execute all swarms in parallel
        await asyncio.gather(*tasks)

        return self.results

    def get_result(self, swarm_id: str) -> Optional[Dict[str, Any]]:
        """Get results for a specific swarm"""
        return self.results.get(swarm_id)

    def get_all_results(self) -> Dict[str, Any]:
        """Get all swarm results"""
        return self.results.copy()