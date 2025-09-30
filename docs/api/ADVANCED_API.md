# Advanced Features API Reference

API documentation for Shannon Framework advanced components: Quantum, Neuromorphic, Swarm, Consensus, Holographic, Time Travel, Communication, and Integration systems.

## Table of Contents
- [Quantum Superposition](#quantum-superposition)
- [Swarm Intelligence](#swarm-intelligence)
- [Holographic State Encoding](#holographic-state-encoding)
- [Communication Topologies](#communication-topologies)
- [MCP Coordinator](#mcp-coordinator)

---

## Quantum Superposition

Quantum-inspired parallel universe exploration with probability amplitudes.

### SuperpositionEngine

```python
from shannon.quantum import SuperpositionEngine

class SuperpositionEngine:
    def __init__(
        self,
        max_parallel_universes: int = 10,
        collapse_strategy: str = "born_rule"
    )
```

**Parameters:**
- `max_parallel_universes` (int): Maximum parallel solutions (default: 10)
- `collapse_strategy` (str): How to select best solution
  - `"born_rule"`: Probability-weighted selection (default)
  - `"max_amplitude"`: Highest amplitude wins
  - `"consensus"`: Agreement across universes

### Methods

#### explore_superposition()

Explore multiple solution paths in superposition.

```python
async def explore_superposition(
    self,
    problem: Callable,
    search_space: List[Any],
    scorer: Callable[[Any], float]
) -> SuperpositionResult
```

**Parameters:**
- `problem` (Callable): Problem-solving function
- `search_space` (List[Any]): Possible solutions
- `scorer` (Callable): Solution quality scorer (returns 0.0-1.0)

**Returns:**
- `SuperpositionResult`: Best solution with probability data

**Example:**
```python
from shannon.quantum import SuperpositionEngine

engine = SuperpositionEngine(max_parallel_universes=8)

async def solve_optimization(params):
    # Solution logic
    return optimized_result

def score_solution(result):
    # Return quality score 0.0-1.0
    return calculate_fitness(result)

search_space = [
    {'learning_rate': 0.01, 'batch_size': 32},
    {'learning_rate': 0.001, 'batch_size': 64},
    # ... more parameter combinations
]

result = await engine.explore_superposition(
    problem=solve_optimization,
    search_space=search_space,
    scorer=score_solution
)

print(f"Best solution: {result.best_solution}")
print(f"Probability: {result.best_probability:.3f}")
print(f"Explored universes: {result.explored_universes}")
print(f"Coherence: {result.coherence:.3f}")
```

#### apply_quantum_interference()

Apply constructive/destructive interference to amplitudes.

```python
def apply_quantum_interference(
    self,
    states: List[QuantumState],
    interference_pattern: str = "constructive"
) -> List[QuantumState]
```

**Parameters:**
- `states` (List[QuantumState]): Quantum states
- `interference_pattern` (str): `"constructive"` or `"destructive"`

**Returns:**
- `List[QuantumState]`: Modified states

---

## Swarm Intelligence

Collective intelligence algorithms for optimization and search.

### AntColonyOptimizer

```python
from shannon.swarm import AntColonyOptimizer

class AntColonyOptimizer:
    def __init__(
        self,
        n_ants: int = 50,
        evaporation_rate: float = 0.1,
        alpha: float = 1.0,  # pheromone importance
        beta: float = 2.0    # heuristic importance
    )
```

### Methods

#### optimize_path()

Find optimal path through solution space using pheromone trails.

```python
async def optimize_path(
    self,
    distance_matrix: np.ndarray,
    n_iterations: int = 100
) -> Tuple[List[int], float]
```

**Parameters:**
- `distance_matrix` (np.ndarray): Distance/cost matrix
- `n_iterations` (int): Optimization iterations

**Returns:**
- `Tuple[List[int], float]`: Best path and cost

**Example:**
```python
from shannon.swarm import AntColonyOptimizer
import numpy as np

# Distance matrix for traveling salesman problem
distances = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

aco = AntColonyOptimizer(
    n_ants=50,
    evaporation_rate=0.1,
    alpha=1.0,
    beta=2.0
)

best_path, best_cost = await aco.optimize_path(
    distance_matrix=distances,
    n_iterations=100
)

print(f"Best path: {best_path}")
print(f"Total cost: {best_cost}")
```

### ParticleSwarmOptimizer

```python
from shannon.swarm import ParticleSwarmOptimizer

class ParticleSwarmOptimizer:
    def __init__(
        self,
        n_particles: int = 30,
        inertia: float = 0.7,
        cognitive: float = 1.5,
        social: float = 1.5
    )
```

### Methods

#### optimize()

Optimize continuous parameters using particle swarm.

```python
async def optimize(
    self,
    objective_function: Callable,
    bounds: List[Tuple[float, float]],
    n_iterations: int = 100
) -> Tuple[np.ndarray, float]
```

**Parameters:**
- `objective_function` (Callable): Function to optimize
- `bounds` (List[Tuple]): Parameter bounds [(min, max), ...]
- `n_iterations` (int): Optimization iterations

**Returns:**
- `Tuple[np.ndarray, float]`: Best parameters and fitness

**Example:**
```python
from shannon.swarm import ParticleSwarmOptimizer

def objective(params):
    # Example: Minimize Rosenbrock function
    x, y = params
    return (1 - x)**2 + 100*(y - x**2)**2

pso = ParticleSwarmOptimizer(
    n_particles=30,
    inertia=0.7,
    cognitive=1.5,
    social=1.5
)

bounds = [(-5.0, 5.0), (-5.0, 5.0)]

best_params, best_fitness = await pso.optimize(
    objective_function=objective,
    bounds=bounds,
    n_iterations=100
)

print(f"Best parameters: {best_params}")
print(f"Best fitness: {best_fitness}")
```

---

## Holographic State Encoding

FFT-based state compression with graceful degradation.

### HolographicEncoder

```python
from shannon.holographic import HolographicEncoder

class HolographicEncoder:
    def __init__(
        self,
        target_compression: float = 50.0,
        preserve_frequencies: int = 10
    )
```

**Parameters:**
- `target_compression` (float): Target compression ratio (default: 50:1)
- `preserve_frequencies` (int): Key frequencies to preserve (default: 10)

### Methods

#### encode_state()

Encode state using holographic compression.

```python
def encode_state(
    self,
    state: Dict[str, Any]
) -> Tuple[bytes, Dict[str, Any]]
```

**Parameters:**
- `state` (Dict): State to encode

**Returns:**
- `Tuple[bytes, Dict]`: Encoded data and metadata

**Example:**
```python
from shannon.holographic import HolographicEncoder

encoder = HolographicEncoder(
    target_compression=50.0,
    preserve_frequencies=10
)

state = {
    'agents': [...],  # Large agent state
    'results': [...], # Extensive results
    'metrics': {...}  # Performance data
}

encoded, metadata = encoder.encode_state(state)

print(f"Original size: {metadata['original_size']} bytes")
print(f"Compressed size: {metadata['compressed_size']} bytes")
print(f"Compression ratio: {metadata['compression_ratio']:.1f}:1")
```

#### decode_state()

Decode holographic state with graceful degradation.

```python
def decode_state(
    self,
    encoded: bytes,
    metadata: Dict[str, Any],
    fidelity: float = 1.0
) -> Dict[str, Any]
```

**Parameters:**
- `encoded` (bytes): Encoded state
- `metadata` (Dict): Encoding metadata
- `fidelity` (float): Reconstruction fidelity 0.0-1.0 (default: 1.0)

**Returns:**
- `Dict`: Decoded state

**Example:**
```python
# Full fidelity reconstruction
full_state = encoder.decode_state(encoded, metadata, fidelity=1.0)

# Partial reconstruction (faster, lower memory)
partial_state = encoder.decode_state(encoded, metadata, fidelity=0.5)

print(f"Full state keys: {list(full_state.keys())}")
print(f"Partial state keys: {list(partial_state.keys())}")
```

---

## Communication Topologies

Dynamic communication patterns for agent coordination.

### TopologyManager

```python
from shannon.communication import TopologyManager, TopologyType

class TopologyManager:
    def __init__(
        self,
        default_topology: TopologyType = TopologyType.MESH
    )
```

**Topology Types:**
- `MESH`: All-to-all communication
- `STAR`: Hub-and-spoke pattern
- `RING`: Circular communication
- `TREE`: Hierarchical structure
- `HYBRID`: Adaptive mixed topology

### Methods

#### create_topology()

Create communication topology for agents.

```python
def create_topology(
    self,
    agent_ids: List[str],
    topology_type: TopologyType
) -> Dict[str, List[str]]
```

**Parameters:**
- `agent_ids` (List[str]): Agent identifiers
- `topology_type` (TopologyType): Topology pattern

**Returns:**
- `Dict[str, List[str]]`: Agent communication graph

**Example:**
```python
from shannon.communication import TopologyManager, TopologyType

manager = TopologyManager()

agent_ids = ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5']

# Create mesh topology (full connectivity)
mesh = manager.create_topology(agent_ids, TopologyType.MESH)
print(f"Mesh connections: {len(sum(mesh.values(), []))} edges")

# Create star topology (central coordinator)
star = manager.create_topology(agent_ids, TopologyType.STAR)
print(f"Star hub: {[k for k, v in star.items() if len(v) > 1][0]}")

# Create ring topology (circular)
ring = manager.create_topology(agent_ids, TopologyType.RING)
print(f"Ring: each agent connects to {len(list(ring.values())[0])} neighbors")
```

#### route_message()

Route message through topology.

```python
async def route_message(
    self,
    message: Dict[str, Any],
    from_agent: str,
    to_agent: str,
    topology: Dict[str, List[str]]
) -> List[str]
```

**Parameters:**
- `message` (Dict): Message payload
- `from_agent` (str): Source agent
- `to_agent` (str): Destination agent
- `topology` (Dict): Communication graph

**Returns:**
- `List[str]`: Message path

**Example:**
```python
message = {'type': 'result', 'data': [...]}

path = await manager.route_message(
    message=message,
    from_agent='agent_1',
    to_agent='agent_5',
    topology=mesh
)

print(f"Message route: {' -> '.join(path)}")
```

---

## MCP Coordinator

Multi-MCP server orchestration and intelligent routing.

### MCPCoordinator

```python
from shannon.integration import MCPCoordinator

class MCPCoordinator:
    def __init__(
        self,
        available_servers: List[str],
        routing_strategy: str = "intelligent"
    )
```

**Parameters:**
- `available_servers` (List[str]): MCP server names
- `routing_strategy` (str): Routing method
  - `"intelligent"`: Capability-based routing (default)
  - `"round_robin"`: Balanced distribution
  - `"priority"`: Priority-based selection

**Available Servers:**
- `"sequential"`: Complex reasoning and analysis
- `"context7"`: Documentation and patterns
- `"magic"`: UI component generation
- `"morphllm"`: Bulk code transformation
- `"serena"`: Memory and reflection
- `"playwright"`: Browser automation

### Methods

#### route_request()

Route request to optimal MCP server.

```python
async def route_request(
    self,
    request_type: str,
    parameters: Dict[str, Any]
) -> Tuple[str, Any]
```

**Parameters:**
- `request_type` (str): Request classification
  - `"analysis"`: Deep analysis needed
  - `"documentation"`: Official docs lookup
  - `"ui_generation"`: UI component creation
  - `"bulk_edit"`: Pattern-based edits
  - `"memory"`: Memory operations
  - `"testing"`: Browser-based testing

**Returns:**
- `Tuple[str, Any]`: Selected server and result

**Example:**
```python
from shannon.integration import MCPCoordinator

coordinator = MCPCoordinator(
    available_servers=['sequential', 'context7', 'magic', 'serena'],
    routing_strategy='intelligent'
)

# Route analysis request
server, result = await coordinator.route_request(
    request_type='analysis',
    parameters={
        'code': 'async def process(...)',
        'focus': 'performance'
    }
)
print(f"Routed to: {server}")

# Route documentation request
server, result = await coordinator.route_request(
    request_type='documentation',
    parameters={
        'library': 'react',
        'topic': 'hooks'
    }
)
print(f"Routed to: {server}")

# Route UI generation
server, result = await coordinator.route_request(
    request_type='ui_generation',
    parameters={
        'component': 'data table',
        'framework': 'react'
    }
)
print(f"Routed to: {server}")
```

#### coordinate_multi_server()

Coordinate request across multiple servers.

```python
async def coordinate_multi_server(
    self,
    request: Dict[str, Any],
    required_servers: List[str]
) -> Dict[str, Any]
```

**Parameters:**
- `request` (Dict): Request specification
- `required_servers` (List[str]): Servers to involve

**Returns:**
- `Dict`: Aggregated results from all servers

**Example:**
```python
# Complex request requiring multiple servers
request = {
    'task': 'Implement authenticated feature',
    'requirements': [
        'Security analysis',
        'UI components',
        'Pattern application'
    ]
}

results = await coordinator.coordinate_multi_server(
    request=request,
    required_servers=['sequential', 'magic', 'context7']
)

print("Results from servers:")
for server, server_result in results.items():
    print(f"  {server}: {server_result['summary']}")
```

---

## Complete Advanced Example

```python
import asyncio
from shannon.quantum import SuperpositionEngine
from shannon.swarm import ParticleSwarmOptimizer
from shannon.holographic import HolographicEncoder
from shannon.communication import TopologyManager, TopologyType
from shannon.integration import MCPCoordinator

async def advanced_optimization():
    # Initialize systems
    quantum = SuperpositionEngine(max_parallel_universes=10)
    swarm = ParticleSwarmOptimizer(n_particles=30)
    encoder = HolographicEncoder(target_compression=50.0)
    topology = TopologyManager()
    mcp = MCPCoordinator(
        available_servers=['sequential', 'context7', 'serena'],
        routing_strategy='intelligent'
    )

    # 1. Quantum exploration of solution space
    search_space = generate_candidate_solutions()
    quantum_result = await quantum.explore_superposition(
        problem=solve_problem,
        search_space=search_space,
        scorer=evaluate_solution
    )

    print(f"Quantum exploration: {quantum_result.explored_universes} universes")
    print(f"Best probability: {quantum_result.best_probability:.3f}")

    # 2. Swarm optimization of parameters
    bounds = [(-10, 10), (-10, 10), (-10, 10)]
    swarm_result = await swarm.optimize(
        objective_function=objective,
        bounds=bounds,
        n_iterations=100
    )

    print(f"Swarm optimization: {swarm_result[0]}")

    # 3. Holographic state compression
    state = {
        'quantum_results': quantum_result,
        'swarm_results': swarm_result,
        'metadata': {...}
    }

    encoded, metadata = encoder.encode_state(state)
    print(f"Compression: {metadata['compression_ratio']:.1f}:1")

    # 4. Communication topology for agents
    agents = ['agent_1', 'agent_2', 'agent_3', 'agent_4']
    comm_graph = topology.create_topology(agents, TopologyType.HYBRID)

    # 5. MCP coordination
    analysis_result = await mcp.route_request(
        request_type='analysis',
        parameters={'results': quantum_result}
    )

    print(f"MCP analysis via: {analysis_result[0]}")

if __name__ == "__main__":
    asyncio.run(advanced_optimization())
```