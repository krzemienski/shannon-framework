# Shannon Framework API Index

Complete API reference for Shannon Framework v2.1 - Multi-agent wave orchestration with continuous learning.

## Quick Navigation

- **[Core API](#core-api)** - Wave orchestration, complexity analysis, agents
- **[Memory API](#memory-api)** - 5-tier memory, context monitoring, checkpoints
- **[Reflection API](#reflection-api)** - Learning system with Serena MCP integration
- **[Advanced API](#advanced-api)** - Quantum, swarm, holographic, communication

---

## Core API

Foundation components for wave orchestration and agent coordination.

### WaveOrchestrator

Master coordination of wave execution with automatic complexity analysis.

```python
from shannon import WaveOrchestrator

orchestrator = WaveOrchestrator({
    'complexity_threshold': 0.7,
    'max_concurrent_agents': 10
})

decision = await orchestrator.analyze_and_decide(task)
result = await orchestrator.execute_wave(wave_config, agent_factory)
```

**Key Methods:**
- `analyze_and_decide()` - Analyze task complexity and determine orchestration need
- `execute_wave()` - Execute complete wave with all phases
- `cleanup()` - Clean up orchestrator resources

**📖 [Full Documentation](CORE_API.md#waveorchestrator)**

### ComplexityAnalyzer

8-dimensional complexity analysis for automatic wave triggering.

```python
from shannon import ComplexityAnalyzer

analyzer = ComplexityAnalyzer(threshold=0.7)
complexity = await analyzer.analyze(task)

print(f"Total: {complexity.total:.3f}")
print(f"Trigger: {complexity.threshold_exceeded}")
```

**Dimensions:**
- Scope, Dependencies, Operations, Domains
- Concurrency, Uncertainty, Risk, Scale

**📖 [Full Documentation](CORE_API.md#complexityanalyzer)**

### BaseAgent

Abstract base agent with state management and execution framework.

```python
from shannon import BaseAgent, AgentCapability

class MyAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> Any:
        # Implement agent logic
        return result

agent = MyAgent(
    agent_id="agent_001",
    capabilities={AgentCapability.ANALYSIS},
    config={'timeout': 300}
)

await agent.initialize()
result = await agent.run(task)
```

**States:** CREATED, INITIALIZING, READY, EXECUTING, COMPLETED, FAILED, CANCELLED

**📖 [Full Documentation](CORE_API.md#baseagent)**

### WaveConfig

Complete wave configuration specification with validation.

```python
from shannon import WaveConfig, WavePhase, AgentAllocation, ValidationLevel

config = WaveConfig(
    wave_id="wave_001",
    objective="Refactor authentication",
    phases=[
        AgentAllocation(
            phase=WavePhase.ANALYSIS,
            agent_count=2,
            agent_types=['Analyzer', 'SecurityChecker'],
            parallel_execution=True,
            timeout_seconds=300
        )
    ],
    validation_level=ValidationLevel.STRICT
)
```

**Phases:** DISCOVERY, ANALYSIS, SYNTHESIS, IMPLEMENTATION, VALIDATION

**📖 [Full Documentation](CORE_API.md#waveconfig)**

### WaveResult

Aggregated wave execution results with metrics.

```python
result = await orchestrator.execute_wave(config, agent_factory)

print(f"Success: {result.success}")
print(f"Duration: {result.total_duration_seconds:.2f}s")
print(f"Success Rate: {result.success_rate():.1%}")
```

**📖 [Full Documentation](CORE_API.md#waveresult)**

---

## Memory API

5-tier memory hierarchy with automatic transitions and intelligent compression.

### MemoryTierManager

Hierarchical memory management with automatic tier transitions.

```python
from shannon.memory import MemoryTierManager, MemoryTier

manager = MemoryTierManager()
await manager.start()

# Store memory
item = manager.store(
    key="analysis_2024",
    content={'files': 150, 'issues': 23},
    metadata={'project': 'auth'}
)

# Retrieve memory
content = manager.retrieve("analysis_2024")

# Get statistics
stats = manager.get_tier_stats()
print(f"Avg compression: {stats['avg_compression_ratio']:.1f}:1")
```

**Tiers:**
- **Working** (0-1min): No compression, instant access
- **Hot** (1min-1hr): 5:1 semantic compression
- **Warm** (1hr-24hr): 10:1 AST compression
- **Cold** (24hr-7d): 50:1 holographic compression
- **Archive** (>7d): 100:1 maximum compression

**📖 [Full Documentation](MEMORY_API.md#memorytier manager)**

### ContextMonitor

Real-time token usage monitoring with 4-level alert system.

```python
from shannon.memory import ContextMonitor, AlertLevel

monitor = ContextMonitor(tokens_limit=200000)

# Register alert callback
def on_yellow_alert(level, usage_percent):
    print(f"⚠️ {usage_percent:.1f}% usage")

monitor.register_alert_callback(AlertLevel.YELLOW, on_yellow_alert)

# Update usage
monitor.update_usage(130000)  # Triggers YELLOW alert

# Get recommendations
recommendations = monitor.get_recommendations()
```

**Alert Levels:**
- **GREEN** (0-60%): Normal operation
- **YELLOW** (60-75%): Optimization suggested
- **ORANGE** (75-85%): Warning alerts
- **RED** (85-95%): Force efficiency modes
- **CRITICAL** (95%+): Emergency protocols

**📖 [Full Documentation](MEMORY_API.md#contextmonitor)**

### ManualCheckpointManager

Manual checkpoint management with context preservation (v2.1 critical feature).

```python
from shannon.memory import ManualCheckpointManager

manager = ManualCheckpointManager()

checkpoint = manager.create_checkpoint(
    checkpoint_id="wave_2_complete",
    description="Wave 2 implementation complete",
    context_monitor=monitor,
    wave_state={'phase': 'implementation'},
    user_notes="Ready for next wave"
)

# Get restoration instructions
instructions = manager.get_restoration_instructions("wave_2_complete")
```

**📖 [Full Documentation](MEMORY_API.md#manualcheckpointmanager)**

---

## Reflection API

5-stage reflection protocol with Serena MCP integration for continuous learning.

### ReflectionEngine

Orchestrates reflection with Serena MCP tools.

```python
from shannon.reflection import ReflectionEngine, ReflectionContext, ReflectionPoint

engine = ReflectionEngine(mcp_available=True)

context = ReflectionContext(
    wave_id="wave_2",
    phase="implementation",
    point=ReflectionPoint.POST_WAVE,
    collected_information={'files_modified': 15},
    task_adherence_score=0.85,
    confidence_level=0.90
)

result = await engine.reflect(context)

print(f"Insights: {len(result.insights)}")
print(f"Quality: {result.quality_score:.2f}")
print(f"Should Replan: {result.should_replan}")
```

**Reflection Stages:**
1. Information Assessment (`think_about_collected_information`)
2. Task Adherence Check (`think_about_task_adherence`)
3. Completion Evaluation (`think_about_whether_you_are_done`)
4. Pattern Learning (extract and store patterns)
5. Memory Persistence (`write_memory` to Serena MCP)

**📖 [Full Documentation](REFLECTION_API.md#reflectionengine)**

### WaveReflectionHooks

Integration hooks for wave orchestrator reflection.

```python
from shannon.reflection import WaveReflectionHooks

hooks = WaveReflectionHooks(
    engine=engine,
    enable_pre_wave=True,
    enable_mid_wave=True,
    enable_post_wave=True
)

# Pre-wave reflection
pre_result = await hooks.pre_wave_reflection(wave_config)

# Mid-wave check
mid_result = await hooks.mid_wave_reflection(
    wave_id="wave_2",
    current_phase="implementation",
    agents_completed=3,
    agents_total=5,
    partial_results=results
)

# Post-wave learning
post_result = await hooks.post_wave_reflection(wave_result)
```

**Reflection Points:**
- **PRE_WAVE**: Before wave execution
- **MID_WAVE**: During wave execution
- **POST_WAVE**: After wave completion
- **INTER_WAVE**: Between multi-wave operations
- **EMERGENCY**: Triggered by failures

**📖 [Full Documentation](REFLECTION_API.md#wavereflectionhooks)**

### Serena MCP Integration

Shannon integrates with Serena MCP tools for deep learning.

**Integrated Tools:**
- `think_about_collected_information()` - Information assessment
- `think_about_task_adherence()` - Task alignment check
- `think_about_whether_you_are_done()` - Completion evaluation
- `write_memory()` - Pattern persistence
- `read_memory()` - Previous learnings retrieval

**📖 [Full Documentation](REFLECTION_API.md#serena-mcp-integration)**

---

## Advanced API

Quantum, swarm, holographic, and communication systems.

### Quantum Superposition

Parallel universe exploration with probability amplitudes.

```python
from shannon.quantum import SuperpositionEngine

engine = SuperpositionEngine(max_parallel_universes=10)

result = await engine.explore_superposition(
    problem=solve_optimization,
    search_space=candidates,
    scorer=evaluate_solution
)

print(f"Best solution: {result.best_solution}")
print(f"Probability: {result.best_probability:.3f}")
print(f"Explored: {result.explored_universes} universes")
```

**📖 [Full Documentation](ADVANCED_API.md#quantum-superposition)**

### Swarm Intelligence

Collective intelligence algorithms for optimization.

```python
from shannon.swarm import AntColonyOptimizer, ParticleSwarmOptimizer

# Ant Colony Optimization
aco = AntColonyOptimizer(n_ants=50)
path, cost = await aco.optimize_path(distance_matrix, n_iterations=100)

# Particle Swarm Optimization
pso = ParticleSwarmOptimizer(n_particles=30)
params, fitness = await pso.optimize(objective, bounds, n_iterations=100)
```

**📖 [Full Documentation](ADVANCED_API.md#swarm-intelligence)**

### Holographic State Encoding

FFT-based state compression with graceful degradation.

```python
from shannon.holographic import HolographicEncoder

encoder = HolographicEncoder(target_compression=50.0)

encoded, metadata = encoder.encode_state(large_state)
decoded = encoder.decode_state(encoded, metadata, fidelity=1.0)

print(f"Compression: {metadata['compression_ratio']:.1f}:1")
```

**📖 [Full Documentation](ADVANCED_API.md#holographic-state-encoding)**

### Communication Topologies

Dynamic communication patterns for agent coordination.

```python
from shannon.communication import TopologyManager, TopologyType

manager = TopologyManager()

# Create topology
topology = manager.create_topology(agent_ids, TopologyType.MESH)

# Route messages
path = await manager.route_message(message, from_agent, to_agent, topology)
```

**Topology Types:** MESH, STAR, RING, TREE, HYBRID

**📖 [Full Documentation](ADVANCED_API.md#communication-topologies)**

### MCP Coordinator

Multi-MCP server orchestration and intelligent routing.

```python
from shannon.integration import MCPCoordinator

coordinator = MCPCoordinator(
    available_servers=['sequential', 'context7', 'magic', 'serena'],
    routing_strategy='intelligent'
)

# Route to optimal server
server, result = await coordinator.route_request(
    request_type='analysis',
    parameters={'code': '...', 'focus': 'performance'}
)

# Coordinate across multiple servers
results = await coordinator.coordinate_multi_server(
    request=complex_request,
    required_servers=['sequential', 'magic', 'context7']
)
```

**📖 [Full Documentation](ADVANCED_API.md#mcp-coordinator)**

---

## Quick Reference

### Import Shortcuts

```python
# Core components
from shannon import (
    WaveOrchestrator,
    ComplexityAnalyzer,
    BaseAgent,
    WaveConfig,
    WaveResult,
    WavePhase,
    AgentCapability,
    ValidationLevel
)

# Memory system
from shannon.memory import (
    MemoryTierManager,
    ContextMonitor,
    ManualCheckpointManager,
    SerenaReferenceTracker,
    MemoryTier,
    AlertLevel
)

# Reflection system
from shannon.reflection import (
    ReflectionEngine,
    WaveReflectionHooks,
    ReflectionContext,
    ReflectionPoint
)

# Advanced features
from shannon.quantum import SuperpositionEngine
from shannon.swarm import AntColonyOptimizer, ParticleSwarmOptimizer
from shannon.holographic import HolographicEncoder
from shannon.communication import TopologyManager, TopologyType
from shannon.integration import MCPCoordinator
```

### Common Patterns

#### Basic Wave Execution

```python
orchestrator = WaveOrchestrator({'complexity_threshold': 0.7})
decision = await orchestrator.analyze_and_decide(task)

if decision.should_orchestrate:
    config = WaveConfig(...)
    result = await orchestrator.execute_wave(config, agent_factory)
```

#### Memory Management

```python
manager = MemoryTierManager()
await manager.start()

item = manager.store("key", content, metadata)
content = manager.retrieve("key")
stats = manager.get_tier_stats()
```

#### Context Monitoring

```python
monitor = ContextMonitor(tokens_limit=200000)
monitor.register_alert_callback(AlertLevel.YELLOW, on_alert)
monitor.update_usage(current_tokens)
recommendations = monitor.get_recommendations()
```

#### Reflection Integration

```python
engine = ReflectionEngine()
hooks = WaveReflectionHooks(engine)

pre_result = await hooks.pre_wave_reflection(config)
# Execute wave
post_result = await hooks.post_wave_reflection(result)
```

---

## Version Information

- **Current Version**: 2.1.0
- **Python Required**: 3.10+
- **Key Dependencies**: numpy, asyncio, Serena MCP

---

## Additional Resources

- **[GitHub Repository](https://github.com/shannon-framework/shannon)** - Source code and issues
- **[Examples Directory](../examples/)** - Complete working examples
- **[Architecture Guide](../ARCHITECTURE.md)** - System architecture documentation
- **[Contributing Guide](../../CONTRIBUTING.md)** - Contribution guidelines

---

## API Documentation Files

- **[CORE_API.md](CORE_API.md)** - Core orchestration and agent APIs
- **[MEMORY_API.md](MEMORY_API.md)** - Memory system and context management APIs
- **[REFLECTION_API.md](REFLECTION_API.md)** - Reflection and learning system APIs
- **[ADVANCED_API.md](ADVANCED_API.md)** - Quantum, swarm, and advanced feature APIs

---

## Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](https://github.com/shannon-framework/shannon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shannon-framework/shannon/discussions)
- **Email**: support@shannon-framework.org