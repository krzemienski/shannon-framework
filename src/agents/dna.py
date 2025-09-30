"""
Agent DNA System for Shannon Framework
=======================================

Genetic algorithm implementation for agent evolution and optimization.
Enables agents to learn, adapt, and improve performance over time.

Features:
- 7 specialized gene types for comprehensive agent configuration
- Multi-objective fitness evaluation (speed, quality, resource efficiency)
- Multiple crossover strategies (uniform, single-point, two-point)
- Adaptive mutation with Gaussian and categorical strategies
- Selection mechanisms: tournament, elite preservation, roulette
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple, Set
from enum import Enum
from datetime import datetime
import json
import random
import numpy as np


# ============================================================================
# GENE TYPE DEFINITIONS
# ============================================================================

class GeneType(Enum):
    """Seven specialized gene types for agent DNA."""
    TOOL_PREFERENCE = "tool_preference"
    MCP_AFFINITY = "mcp_affinity"
    PARALLELISM = "parallelism"
    MEMORY_TIER = "memory_tier"
    ERROR_STRATEGY = "error_strategy"
    TOPOLOGY = "topology"
    OPTIMIZATION = "optimization"


@dataclass
class ToolPreferenceGene:
    """Controls agent's tool selection preferences."""
    tool_name: str
    preference_weight: float  # 0.0-1.0
    success_threshold: float  # 0.0-1.0
    retry_count: int
    timeout_seconds: int


@dataclass
class MCPAffinityGene:
    """Controls MCP server integration preferences."""
    server_name: str  # "sequential", "context7", "magic", "playwright", etc.
    affinity_score: float  # 0.0-1.0
    priority: int  # 1-10
    fallback_enabled: bool
    cache_strategy: str  # "aggressive", "moderate", "minimal"


@dataclass
class ParallelismGene:
    """Controls parallel execution behavior."""
    max_parallel_ops: int
    batch_size: int
    async_enabled: bool
    coordination_strategy: str  # "gather", "race", "sequential"
    thread_pool_size: int


@dataclass
class MemoryTierGene:
    """Controls memory management and storage."""
    tier_level: int  # 1-3 (L1=fast, L2=moderate, L3=persistent)
    cache_size_mb: int
    retention_seconds: int
    compression_enabled: bool
    eviction_policy: str  # "lru", "lfu", "fifo"


@dataclass
class ErrorStrategyGene:
    """Controls error handling and recovery."""
    strategy_type: str  # "retry", "fallback", "skip", "escalate"
    max_retries: int
    backoff_multiplier: float
    circuit_breaker_threshold: int
    recovery_enabled: bool


@dataclass
class TopologyGene:
    """Controls agent communication topology."""
    topology_type: str  # "star", "mesh", "ring", "tree"
    max_connections: int
    broadcast_enabled: bool
    gossip_interval_seconds: float
    consensus_required: bool


@dataclass
class OptimizationGene:
    """Controls performance optimization strategies."""
    optimization_level: str  # "speed", "quality", "balanced", "resource"
    caching_enabled: bool
    prefetch_enabled: bool
    batch_processing: bool
    lazy_evaluation: bool


# ============================================================================
# BASE GENE CLASS
# ============================================================================

@dataclass
class Gene:
    """
    Universal gene wrapper supporting all gene types.

    Attributes:
        gene_type: Type classification for the gene
        name: Human-readable identifier
        value: Gene-specific dataclass instance
        dominance: Expression probability (0.0-1.0)
        mutation_rate: Probability of mutation (0.0-1.0)
        fitness_impact: Contribution to fitness score
    """
    gene_type: GeneType
    name: str
    value: Any  # One of the specialized gene dataclasses
    dominance: float = 0.5
    mutation_rate: float = 0.1
    fitness_impact: float = 1.0

    def mutate(self) -> 'Gene':
        """Apply mutation based on gene type and value type."""
        if random.random() >= self.mutation_rate:
            return self

        mutated_value = self._mutate_value(self.value)
        mutated_dominance = np.clip(
            self.dominance + random.gauss(0, 0.1),
            0.0,
            1.0
        )

        return Gene(
            gene_type=self.gene_type,
            name=self.name,
            value=mutated_value,
            dominance=mutated_dominance,
            mutation_rate=self.mutation_rate,
            fitness_impact=self.fitness_impact
        )

    def _mutate_value(self, value: Any) -> Any:
        """Mutate value based on type."""
        if isinstance(value, bool):
            return not value if random.random() < 0.5 else value

        elif isinstance(value, int):
            std_dev = max(1, abs(value) * 0.2)
            return max(0, int(value + random.gauss(0, std_dev)))

        elif isinstance(value, float):
            std_dev = max(0.1, abs(value) * 0.2)
            return np.clip(value + random.gauss(0, std_dev), 0.0, 1.0)

        elif isinstance(value, str):
            # Categorical mutation
            mutations = self._get_categorical_mutations(value)
            return random.choice(mutations) if mutations else value

        elif isinstance(value, (ToolPreferenceGene, MCPAffinityGene, ParallelismGene,
                                MemoryTierGene, ErrorStrategyGene, TopologyGene,
                                OptimizationGene)):
            # Mutate dataclass fields
            return self._mutate_dataclass(value)

        return value

    def _mutate_dataclass(self, obj: Any) -> Any:
        """Mutate dataclass instance fields."""
        obj_dict = asdict(obj)
        mutated_dict = {}

        for key, val in obj_dict.items():
            if random.random() < 0.3:  # 30% chance to mutate each field
                mutated_dict[key] = self._mutate_value(val)
            else:
                mutated_dict[key] = val

        return type(obj)(**mutated_dict)

    def _get_categorical_mutations(self, value: str) -> List[str]:
        """Get valid mutation options for categorical values."""
        categorical_options = {
            # Cache strategies
            "aggressive": ["moderate", "minimal"],
            "moderate": ["aggressive", "minimal"],
            "minimal": ["moderate", "aggressive"],
            # Coordination strategies
            "gather": ["race", "sequential"],
            "race": ["gather", "sequential"],
            "sequential": ["gather", "race"],
            # Eviction policies
            "lru": ["lfu", "fifo"],
            "lfu": ["lru", "fifo"],
            "fifo": ["lru", "lfu"],
            # Error strategies
            "retry": ["fallback", "skip", "escalate"],
            "fallback": ["retry", "skip", "escalate"],
            "skip": ["retry", "fallback", "escalate"],
            "escalate": ["retry", "fallback", "skip"],
            # Topology types
            "star": ["mesh", "ring", "tree"],
            "mesh": ["star", "ring", "tree"],
            "ring": ["star", "mesh", "tree"],
            "tree": ["star", "mesh", "ring"],
            # Optimization levels
            "speed": ["quality", "balanced", "resource"],
            "quality": ["speed", "balanced", "resource"],
            "balanced": ["speed", "quality", "resource"],
            "resource": ["speed", "quality", "balanced"],
        }
        return categorical_options.get(value, [value])


# ============================================================================
# AGENT DNA
# ============================================================================

@dataclass
class AgentDNA:
    """
    Complete genetic blueprint for an agent.

    Attributes:
        agent_id: Unique identifier
        generation: Evolutionary generation number
        genes: Dictionary of gene_name -> Gene
        fitness_score: Overall performance score
        parent_ids: IDs of parent agents (for genealogy)
        creation_time: ISO timestamp of creation
        performance_history: Historical fitness scores
    """
    agent_id: str
    generation: int
    genes: Dict[str, Gene]
    fitness_score: float = 0.0
    parent_ids: List[str] = field(default_factory=list)
    creation_time: str = field(default_factory=lambda: datetime.now().isoformat())
    performance_history: List[float] = field(default_factory=list)

    def get_chromosome(self, gene_type: GeneType) -> Dict[str, Gene]:
        """Extract all genes of specific type (chromosome)."""
        return {
            name: gene for name, gene in self.genes.items()
            if gene.gene_type == gene_type
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "agent_id": self.agent_id,
            "generation": self.generation,
            "genes": {
                name: {
                    "gene_type": gene.gene_type.value,
                    "name": gene.name,
                    "value": asdict(gene.value) if hasattr(gene.value, '__dataclass_fields__') else gene.value,
                    "dominance": gene.dominance,
                    "mutation_rate": gene.mutation_rate,
                    "fitness_impact": gene.fitness_impact
                }
                for name, gene in self.genes.items()
            },
            "fitness_score": self.fitness_score,
            "parent_ids": self.parent_ids,
            "creation_time": self.creation_time,
            "performance_history": self.performance_history
        }


# ============================================================================
# FITNESS EVALUATOR
# ============================================================================

class FitnessEvaluator:
    """
    Multi-objective fitness evaluation system.

    Evaluates agents on:
    - Speed: Execution time, response latency
    - Quality: Accuracy, completeness, correctness
    - Resource Efficiency: Memory usage, CPU utilization
    """

    def __init__(self):
        self.weights = {
            "speed": 0.35,
            "quality": 0.40,
            "resource_efficiency": 0.25
        }

    def calculate_fitness(
        self,
        agent: AgentDNA,
        metrics: Dict[str, float]
    ) -> float:
        """
        Calculate weighted fitness score.

        Args:
            agent: Agent DNA to evaluate
            metrics: Performance measurements
                - execution_time_ms: Task completion time
                - accuracy: Correctness score (0-1)
                - memory_mb: Memory consumption
                - cpu_percent: CPU utilization
                - task_completion_rate: Success rate (0-1)

        Returns:
            Fitness score (0.0-1.0)
        """
        # Extract metrics with defaults
        exec_time = metrics.get("execution_time_ms", 1000)
        accuracy = metrics.get("accuracy", 0.5)
        memory = metrics.get("memory_mb", 100)
        cpu = metrics.get("cpu_percent", 50)
        completion = metrics.get("task_completion_rate", 0.5)

        # Calculate component scores (0-1 scale)
        speed_score = self._calculate_speed_score(exec_time)
        quality_score = self._calculate_quality_score(accuracy, completion)
        resource_score = self._calculate_resource_score(memory, cpu)

        # Apply gene fitness impacts
        speed_score *= self._get_gene_impact(agent, GeneType.PARALLELISM)
        quality_score *= self._get_gene_impact(agent, GeneType.ERROR_STRATEGY)
        resource_score *= self._get_gene_impact(agent, GeneType.MEMORY_TIER)

        # Weighted combination
        fitness = (
            self.weights["speed"] * speed_score +
            self.weights["quality"] * quality_score +
            self.weights["resource_efficiency"] * resource_score
        )

        # Update agent
        agent.fitness_score = fitness
        agent.performance_history.append(fitness)

        return fitness

    def _calculate_speed_score(self, exec_time_ms: float) -> float:
        """Speed score: lower time = higher score."""
        # 100ms = 1.0, 10000ms = 0.0 (logarithmic scale)
        normalized = np.log10(max(1, exec_time_ms))
        score = 1.0 - np.clip((normalized - 2.0) / 2.0, 0.0, 1.0)
        return score

    def _calculate_quality_score(
        self,
        accuracy: float,
        completion: float
    ) -> float:
        """Quality score: weighted accuracy and completion."""
        return 0.6 * accuracy + 0.4 * completion

    def _calculate_resource_score(
        self,
        memory_mb: float,
        cpu_percent: float
    ) -> float:
        """Resource score: lower usage = higher score."""
        memory_score = 1.0 - np.clip(memory_mb / 1000.0, 0.0, 1.0)
        cpu_score = 1.0 - np.clip(cpu_percent / 100.0, 0.0, 1.0)
        return 0.6 * memory_score + 0.4 * cpu_score

    def _get_gene_impact(self, agent: AgentDNA, gene_type: GeneType) -> float:
        """Get average fitness impact of genes of specific type."""
        chromosome = agent.get_chromosome(gene_type)
        if not chromosome:
            return 1.0
        impacts = [gene.fitness_impact for gene in chromosome.values()]
        return np.mean(impacts)


# ============================================================================
# EVOLUTION ENGINE
# ============================================================================

class EvolutionEngine:
    """
    Genetic algorithm implementation for agent evolution.

    Features:
    - Multiple crossover strategies
    - Adaptive mutation
    - Tournament selection
    - Elite preservation
    - Diversity maintenance
    """

    def __init__(self, population_size: int = 20):
        self.population: Dict[str, AgentDNA] = {}
        self.generation_count = 0
        self.population_size = population_size
        self.fitness_evaluator = FitnessEvaluator()

        # Evolution parameters
        self.elite_ratio = 0.2  # Top 20% preserved
        self.mutation_rate_base = 0.1
        self.crossover_rate = 0.7
        self.tournament_size = 3

        # Evolution history
        self.evolution_history: List[Dict[str, Any]] = []

    def initialize_population(self) -> Dict[str, AgentDNA]:
        """Create initial random population."""
        for i in range(self.population_size):
            agent_id = f"agent_gen0_{i}"
            agent = self._create_random_agent(agent_id)
            self.population[agent_id] = agent

        return self.population

    def _create_random_agent(self, agent_id: str) -> AgentDNA:
        """Create agent with random DNA."""
        genes = {}

        # Tool preferences (2-3 tools)
        tool_names = ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
        for tool in random.sample(tool_names, random.randint(2, 3)):
            genes[f"tool_{tool.lower()}"] = Gene(
                gene_type=GeneType.TOOL_PREFERENCE,
                name=tool,
                value=ToolPreferenceGene(
                    tool_name=tool,
                    preference_weight=random.uniform(0.5, 1.0),
                    success_threshold=random.uniform(0.7, 0.95),
                    retry_count=random.randint(1, 3),
                    timeout_seconds=random.randint(10, 60)
                ),
                dominance=random.uniform(0.4, 0.9)
            )

        # MCP affinities (1-2 servers)
        mcp_servers = ["sequential", "context7", "magic", "playwright"]
        for server in random.sample(mcp_servers, random.randint(1, 2)):
            genes[f"mcp_{server}"] = Gene(
                gene_type=GeneType.MCP_AFFINITY,
                name=server,
                value=MCPAffinityGene(
                    server_name=server,
                    affinity_score=random.uniform(0.6, 1.0),
                    priority=random.randint(1, 10),
                    fallback_enabled=random.choice([True, False]),
                    cache_strategy=random.choice(["aggressive", "moderate", "minimal"])
                ),
                dominance=random.uniform(0.5, 0.9)
            )

        # Parallelism
        genes["parallelism"] = Gene(
            gene_type=GeneType.PARALLELISM,
            name="parallel_config",
            value=ParallelismGene(
                max_parallel_ops=random.randint(2, 10),
                batch_size=random.randint(3, 8),
                async_enabled=random.choice([True, False]),
                coordination_strategy=random.choice(["gather", "race", "sequential"]),
                thread_pool_size=random.randint(2, 8)
            ),
            dominance=random.uniform(0.6, 0.9)
        )

        # Memory tier
        genes["memory"] = Gene(
            gene_type=GeneType.MEMORY_TIER,
            name="memory_config",
            value=MemoryTierGene(
                tier_level=random.randint(1, 3),
                cache_size_mb=random.randint(50, 500),
                retention_seconds=random.randint(300, 3600),
                compression_enabled=random.choice([True, False]),
                eviction_policy=random.choice(["lru", "lfu", "fifo"])
            ),
            dominance=random.uniform(0.5, 0.8)
        )

        # Error strategy
        genes["error"] = Gene(
            gene_type=GeneType.ERROR_STRATEGY,
            name="error_config",
            value=ErrorStrategyGene(
                strategy_type=random.choice(["retry", "fallback", "skip", "escalate"]),
                max_retries=random.randint(1, 5),
                backoff_multiplier=random.uniform(1.5, 3.0),
                circuit_breaker_threshold=random.randint(3, 10),
                recovery_enabled=random.choice([True, False])
            ),
            dominance=random.uniform(0.6, 0.9)
        )

        # Topology
        genes["topology"] = Gene(
            gene_type=GeneType.TOPOLOGY,
            name="topology_config",
            value=TopologyGene(
                topology_type=random.choice(["star", "mesh", "ring", "tree"]),
                max_connections=random.randint(3, 15),
                broadcast_enabled=random.choice([True, False]),
                gossip_interval_seconds=random.uniform(0.5, 5.0),
                consensus_required=random.choice([True, False])
            ),
            dominance=random.uniform(0.4, 0.7)
        )

        # Optimization
        genes["optimization"] = Gene(
            gene_type=GeneType.OPTIMIZATION,
            name="opt_config",
            value=OptimizationGene(
                optimization_level=random.choice(["speed", "quality", "balanced", "resource"]),
                caching_enabled=random.choice([True, False]),
                prefetch_enabled=random.choice([True, False]),
                batch_processing=random.choice([True, False]),
                lazy_evaluation=random.choice([True, False])
            ),
            dominance=random.uniform(0.5, 0.9)
        )

        return AgentDNA(
            agent_id=agent_id,
            generation=self.generation_count,
            genes=genes,
            fitness_score=0.0
        )

    def crossover(self, parent1: AgentDNA, parent2: AgentDNA) -> AgentDNA:
        """
        Perform crossover between two parents.

        Strategies:
        - uniform: Random gene selection per gene
        - single_point: Split at one point
        - two_point: Split at two points
        """
        strategy = random.choice(["uniform", "single_point", "two_point"])
        child_genes = {}

        all_gene_names = set(parent1.genes.keys()) | set(parent2.genes.keys())
        gene_list = sorted(list(all_gene_names))

        if strategy == "uniform":
            for gene_name in gene_list:
                if gene_name in parent1.genes and gene_name in parent2.genes:
                    # Both have gene - select based on dominance
                    g1, g2 = parent1.genes[gene_name], parent2.genes[gene_name]
                    selected = g1 if random.random() < g1.dominance else g2
                elif gene_name in parent1.genes:
                    selected = parent1.genes[gene_name]
                else:
                    selected = parent2.genes[gene_name]

                child_genes[gene_name] = selected

        elif strategy == "single_point":
            point = random.randint(1, len(gene_list) - 1)
            for i, gene_name in enumerate(gene_list):
                parent = parent1 if i < point else parent2
                if gene_name in parent.genes:
                    child_genes[gene_name] = parent.genes[gene_name]

        elif strategy == "two_point":
            p1 = random.randint(1, len(gene_list) - 2)
            p2 = random.randint(p1 + 1, len(gene_list) - 1)
            for i, gene_name in enumerate(gene_list):
                parent = parent2 if p1 <= i < p2 else parent1
                if gene_name in parent.genes:
                    child_genes[gene_name] = parent.genes[gene_name]

        child_id = f"agent_gen{self.generation_count}_{len(self.population)}"
        return AgentDNA(
            agent_id=child_id,
            generation=self.generation_count,
            genes=child_genes,
            parent_ids=[parent1.agent_id, parent2.agent_id]
        )

    def mutate(self, agent: AgentDNA, mutation_pressure: float = 1.0) -> AgentDNA:
        """Apply mutations to agent DNA."""
        mutated_genes = {}

        for gene_name, gene in agent.genes.items():
            # Adjust mutation rate
            original_rate = gene.mutation_rate
            gene.mutation_rate *= mutation_pressure

            mutated_gene = gene.mutate()
            mutated_genes[gene_name] = mutated_gene

            # Restore original rate
            gene.mutation_rate = original_rate

        agent.genes = mutated_genes
        agent.generation = self.generation_count

        return agent

    def tournament_selection(self, population: List[AgentDNA]) -> AgentDNA:
        """Select agent via tournament."""
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        return max(tournament, key=lambda a: a.fitness_score)

    def evolve_population(
        self,
        performance_metrics: Dict[str, Dict[str, float]]
    ) -> List[AgentDNA]:
        """
        Main evolution loop.

        Steps:
        1. Evaluate fitness
        2. Select elite agents
        3. Generate offspring via crossover
        4. Apply mutation
        5. Replace population

        Args:
            performance_metrics: Dict of agent_id -> metrics

        Returns:
            New population list
        """
        self.generation_count += 1

        # Calculate fitness
        for agent_id, agent in self.population.items():
            if agent_id in performance_metrics:
                self.fitness_evaluator.calculate_fitness(
                    agent,
                    performance_metrics[agent_id]
                )

        # Sort by fitness
        sorted_agents = sorted(
            self.population.values(),
            key=lambda a: a.fitness_score,
            reverse=True
        )

        # Elite preservation
        num_elite = max(1, int(len(sorted_agents) * self.elite_ratio))
        elite_agents = sorted_agents[:num_elite]

        # Build new population
        new_population = {}

        # Keep elites
        for agent in elite_agents:
            new_population[agent.agent_id] = agent

        # Generate offspring
        while len(new_population) < self.population_size:
            # Selection
            parent1 = self.tournament_selection(sorted_agents)
            parent2 = self.tournament_selection(sorted_agents)

            # Crossover
            if random.random() < self.crossover_rate and parent1 != parent2:
                child = self.crossover(parent1, parent2)
            else:
                # Clone
                child = self._clone_agent(parent1)

            # Mutation
            mutation_pressure = self._calculate_mutation_pressure(sorted_agents)
            child = self.mutate(child, mutation_pressure)

            new_population[child.agent_id] = child

        # Update population
        self.population = new_population

        # Record history
        self._record_history(sorted_agents, elite_agents)

        return list(new_population.values())

    def _clone_agent(self, agent: AgentDNA) -> AgentDNA:
        """Clone agent with new ID."""
        return AgentDNA(
            agent_id=f"{agent.agent_id}_clone_{self.generation_count}",
            generation=self.generation_count,
            genes=agent.genes.copy(),
            parent_ids=[agent.agent_id]
        )

    def _calculate_mutation_pressure(self, agents: List[AgentDNA]) -> float:
        """Calculate adaptive mutation pressure based on diversity."""
        if len(agents) < 2:
            return 1.0

        fitness_values = [a.fitness_score for a in agents]
        variance = np.var(fitness_values)

        # Low variance = low diversity = high mutation
        if variance < 0.01:
            return 2.0
        elif variance < 0.1:
            return 1.5
        else:
            return 1.0

    def _record_history(
        self,
        sorted_agents: List[AgentDNA],
        elite_agents: List[AgentDNA]
    ):
        """Record evolution statistics."""
        self.evolution_history.append({
            "generation": self.generation_count,
            "timestamp": datetime.now().isoformat(),
            "population_size": len(sorted_agents),
            "elite_count": len(elite_agents),
            "best_fitness": sorted_agents[0].fitness_score if sorted_agents else 0.0,
            "avg_fitness": np.mean([a.fitness_score for a in sorted_agents]),
            "fitness_variance": np.var([a.fitness_score for a in sorted_agents])
        })

    def get_best_agents(self, n: int = 5) -> List[AgentDNA]:
        """Get top N performing agents."""
        return sorted(
            self.population.values(),
            key=lambda a: a.fitness_score,
            reverse=True
        )[:n]