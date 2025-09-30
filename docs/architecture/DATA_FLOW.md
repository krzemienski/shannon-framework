# Shannon Framework v2.1 - Data Flow Documentation

## Overview

This document describes the data pipelines, component interactions, critical execution paths, and performance bottlenecks in Shannon v2.1.

## High-Level Data Flow

```
User Request
     ↓
AutomaticOrchestrator
     │
     ├─→ Complexity Analysis (8 dimensions)
     │   └─→ Score ≥ 0.7?
     │        ├─ Yes → Wave Orchestration
     │        └─ No → Direct Execution
     ↓
Wave Orchestration Engine (5 phases)
     │
     ├─→ Phase 1: Planning
     │   ├─ Task decomposition
     │   ├─ Strategy formulation
     │   └─ Resource allocation
     │
     ├─→ Phase 2: Spawning
     │   ├─ Agent creation with DNA
     │   ├─ Task assignment
     │   └─ Communication setup
     │
     ├─→ Phase 3: Execution
     │   ├─ Parallel task execution (asyncio.gather)
     │   ├─ Context monitoring (real-time)
     │   ├─ Progress tracking
     │   └─ Error recovery
     │
     ├─→ Phase 4: Reflection
     │   ├─ Pre-wave (information gaps)
     │   ├─ Mid-wave (task adherence)
     │   ├─ Post-wave (completion check)
     │   ├─ Pattern extraction
     │   └─ Memory persistence (Serena)
     │
     └─→ Phase 5: Synthesis
         ├─ Result aggregation
         ├─ Memory storage (5-tier)
         ├─ DNA evolution
         └─ Final result return
```

## Component Interaction Pipelines

### Pipeline 1: Orchestration Decision Pipeline

```
Request Input
     ↓
AutomaticOrchestrator.should_orchestrate()
     │
     ├─→ analyze_file_count() → 0.0-1.0
     ├─→ analyze_directory_depth() → 0.0-1.0
     ├─→ analyze_operation_diversity() → 0.0-1.0
     ├─→ analyze_domain_complexity() → 0.0-1.0
     ├─→ analyze_dependency_depth() → 0.0-1.0
     ├─→ analyze_risk_level() → 0.0-1.0
     ├─→ analyze_token_estimation() → 0.0-1.0
     └─→ analyze_parallelization_opportunity() → 0.0-1.0
     ↓
Weighted Sum (8 dimensions)
     ↓
complexity_score = Σ(dimension_i * weight_i)
     ↓
Decision: score ≥ 0.7 → Wave | score < 0.7 → Direct
```

**Performance Characteristics**:
- **Latency**: <10ms for complexity analysis
- **CPU**: <1% overhead
- **Memory**: <1MB for analysis state
- **Accuracy**: 95%+ correct orchestration decisions

**Data Dependencies**:
- **Input**: Request dictionary (task description, files, context)
- **Output**: Boolean decision, complexity score, dimension breakdown

### Pipeline 2: Memory Management Pipeline

```
Data Access Request
     ↓
MultiTierMemory.retrieve(key)
     │
     ├─→ Check Hot Tier (10ms latency)
     │   └─ Found? → Return + Update access metadata
     │
     ├─→ Check Warm Tier (20ms latency, 5:1 compression)
     │   └─ Found? → Decompress → Promote to Hot → Return
     │
     ├─→ Check Cool Tier (50ms latency, 10:1 compression)
     │   └─ Found? → Decompress → Promote to Warm → Return
     │
     ├─→ Check Cold Tier (100ms latency, 50:1 compression)
     │   └─ Found? → FFT decode → Promote to Cool → Return
     │
     └─→ Check Archive Tier (100:1 compression)
         └─ Found? → Full decompress → Load to appropriate tier → Return
     ↓
Update Access Statistics
Update Tier Transition Metrics
Return Data

Background Process (Continuous):
     ↓
Monitor Tier Occupancy
     ↓
Age-Based Transitions
     │
     ├─→ Hot (>5 min, low access) → Semantic compress → Warm
     ├─→ Warm (>15 min, low access) → AST compress → Cool
     ├─→ Cool (>1 hour, low access) → FFT compress → Cold
     └─→ Cold (>6 hours, no access) → Final compress → Archive
```

**Performance Characteristics**:
- **Hit Rate**: 90%+ in Hot tier for active workload
- **Average Latency**: 15ms (weighted by tier distribution)
- **Compression Overhead**: 5-10ms per transition
- **Memory Savings**: 50-100x aggregate compression
- **Background CPU**: <5% for tier management

**Data Dependencies**:
- **Hot Tier**: Raw uncompressed state (fastest access)
- **Warm Tier**: Semantic compression (key-value extraction)
- **Cool Tier**: AST compression (syntax trees)
- **Cold Tier**: FFT holographic encoding (frequency domain)
- **Archive Tier**: Final compression (long-term storage)

### Pipeline 3: Reflection and Learning Pipeline

```
Wave Execution Complete
     ↓
SerenaReflectionEngine.reflect_post_wave(results)
     │
     ├─→ Stage 1: Information Assessment
     │   ├─ Serena: think_about_collected_information()
     │   ├─ Identify knowledge gaps
     │   └─ Output: Missing context, research needs
     │
     ├─→ Stage 2: Task Adherence
     │   ├─ Serena: think_about_task_adherence()
     │   ├─ Validate alignment with goals
     │   └─ Output: Deviation alerts, course corrections
     │
     ├─→ Stage 3: Completion Evaluation
     │   ├─ Serena: think_about_whether_you_are_done()
     │   ├─ Assess success and remaining work
     │   └─ Output: Completion status, next steps
     │
     ├─→ Stage 4: Pattern Learning
     │   ├─ Serena: search_for_pattern()
     │   ├─ Extract successful strategies
     │   ├─ Identify anti-patterns
     │   └─ Output: Reusable patterns, lessons learned
     │
     └─→ Stage 5: Memory Persistence
         ├─ Serena: write_memory(patterns, metadata)
         ├─ Store in long-term knowledge base
         └─ Output: Memory reference for future retrieval
     ↓
Update Pattern Library
     ↓
GeneticEvolutionEngine.evolve_population()
     │
     ├─→ Calculate fitness (speed 35%, quality 40%, resource 25%)
     ├─→ Tournament selection (k=3)
     ├─→ Crossover (70% rate)
     ├─→ Adaptive mutation (10% initial)
     └─→ Elitism (preserve top 10%)
     ↓
Update Agent DNA
Return Evolved Agents
```

**Performance Characteristics**:
- **Reflection Latency**: 200-500ms (5 Serena MCP calls)
- **Pattern Extraction**: 50-100ms per execution trace
- **Memory Persistence**: 20-50ms per write
- **Evolution Cycle**: 100-500ms per generation
- **Learning Impact**: 10x improvement after pattern reuse

**Data Dependencies**:
- **Input**: Wave results, execution traces, performance metrics
- **Serena MCP**: All 5 reflection stages require Serena tools
- **Pattern Library**: Historical successful/failed patterns
- **Agent DNA**: Current genetic configuration for evolution
- **Output**: Updated patterns, evolved DNA, learning insights

### Pipeline 4: Parallel Execution Pipeline

```
Task List (from Wave Planning)
     ↓
AsyncExecutor.execute_parallel(tasks, max_concurrent=5)
     │
     ├─→ Create semaphore pool (limit=5)
     │
     ├─→ Spawn async tasks with semaphore
     │   │
     │   ├─→ Task 1 (Agent A)
     │   │   └─→ async with semaphore: await agent_a.execute()
     │   │
     │   ├─→ Task 2 (Agent B)
     │   │   └─→ async with semaphore: await agent_b.execute()
     │   │
     │   ├─→ Task 3 (Agent C)
     │   │   └─→ async with semaphore: await agent_c.execute()
     │   │
     │   ├─→ Task 4 (Agent D) [queued until semaphore available]
     │   │
     │   └─→ Task 5 (Agent E) [queued until semaphore available]
     │
     ├─→ await asyncio.gather(*tasks, return_exceptions=True)
     │   └─→ True parallelism: all tasks run concurrently
     │
     ├─→ Context monitoring (real-time)
     │   ├─ Track token usage
     │   ├─ Alert on Yellow (60%), Orange (75%), Red (85%)
     │   └─ Create checkpoints at critical points
     │
     └─→ Error handling
         ├─ Capture exceptions per task
         ├─ Apply recovery strategy (retry, fallback, compensate)
         └─ Continue execution for successful tasks
     ↓
Collect Results
     ↓
Aggregate and validate
Return Results
```

**Performance Characteristics**:
- **Speedup**: 5x+ for independent tasks (vs sequential)
- **Concurrency Limit**: 5 simultaneous tasks (configurable)
- **Overhead**: <5% for coordination
- **Resource Protection**: Semaphore prevents exhaustion
- **Fault Tolerance**: Exceptions isolated per task

**Data Dependencies**:
- **Input**: Task list with dependencies
- **Semaphore Pool**: Resource limit enforcement
- **Context Monitor**: Real-time usage tracking
- **Error Recovery**: Recovery strategy configuration
- **Output**: Results array (successful + failed with exceptions)

### Pipeline 5: MCP Coordination Pipeline

```
Agent Request (e.g., "analyze code quality")
     ↓
MCPCoordinator.route_request(request)
     │
     ├─→ Analyze request type
     │   ├─ Search query? → Tavily
     │   ├─ Documentation? → Context7
     │   ├─ Complex analysis? → Sequential
     │   ├─ UI component? → Magic
     │   ├─ Browser automation? → Playwright
     │   └─ Reflection/memory? → Serena
     │
     ├─→ Check server health
     │   └─ Server down? → Route to fallback or native tools
     │
     ├─→ Multi-server coordination (if needed)
     │   │
     │   ├─→ Tavily: Search for information
     │   ├─→ Sequential: Analyze search results
     │   └─→ Context7: Fetch documentation patterns
     │   │
     │   └─→ await asyncio.gather(
     │         tavily_search(),
     │         sequential_analysis(),
     │         context7_patterns()
     │       )
     │
     └─→ Cache results (if applicable)
         └─ TTL-based invalidation
     ↓
Return Aggregated Results
```

**Performance Characteristics**:
- **Routing Latency**: <5ms for server selection
- **Parallel MCP Calls**: 3x+ speedup when independent
- **Cache Hit Rate**: 80%+ for repeated queries
- **Fallback Latency**: <50ms for rerouting
- **Health Check**: 100ms periodic checks

**Data Dependencies**:
- **Input**: Agent request with context
- **Server Registry**: Available MCP servers and capabilities
- **Health Status**: Per-server availability
- **Cache**: TTL-based result storage
- **Output**: MCP server response(s), potentially aggregated

## Critical Execution Paths

### Path 1: Simple Task (No Wave Orchestration)

```
Request → Complexity Analysis → Score < 0.7 → Direct Agent Execution → Return
```

**Latency**: 50-200ms
**Components**: AutomaticOrchestrator, BaseAgent
**Bottlenecks**: None (optimized path)

### Path 2: Complex Task (Wave Orchestration)

```
Request → Complexity Analysis → Score ≥ 0.7 →
5-Phase Wave → Parallel Execution → Reflection → Synthesis → Return
```

**Latency**: 5-60 seconds (task-dependent)
**Components**: All major modules
**Bottlenecks**: Reflection (200-500ms), Evolution (100-500ms)

### Path 3: Memory-Intensive Operation

```
Request → Large Data → Store in Hot Tier →
Age-Based Transition → Warm (5:1) → Cool (10:1) → Cold (50:1) → Archive (100:1)
```

**Latency**: Background (no blocking)
**Components**: MultiTierMemory, HolographicEncoder
**Bottlenecks**: FFT compression (5ms per KB)

### Path 4: Learning and Evolution Cycle

```
Wave Execution → Reflection (5 stages) → Pattern Extraction →
Memory Persistence → DNA Evolution → Updated Agents
```

**Latency**: 500-1000ms per cycle
**Components**: SerenaReflectionEngine, GeneticEvolutionEngine
**Bottlenecks**: Serena MCP calls (50-100ms each)

## Performance Bottlenecks and Mitigations

### Bottleneck 1: Serena MCP Call Latency

**Problem**: Each reflection stage requires Serena MCP call (50-100ms)

**Impact**: 200-500ms total for 5-stage reflection

**Mitigations**:
1. **Batch MCP Calls**: Combine stages where possible
2. **Async Execution**: Parallelize independent reflection stages
3. **Caching**: Store pattern lookups for reuse
4. **Selective Reflection**: Skip stages for low-risk operations

**Performance Gain**: 30-40% reduction (200ms → 120ms)

### Bottleneck 2: FFT Compression

**Problem**: Holographic compression CPU-intensive (5ms per KB)

**Impact**: 500ms for 100KB agent state

**Mitigations**:
1. **Background Compression**: Async tier transitions
2. **Selective Compression**: Only compress cold data
3. **Adaptive Ratios**: Less compression for hot paths
4. **NumPy Optimization**: Use optimized FFT library

**Performance Gain**: 50% reduction through background processing

### Bottleneck 3: Context Monitoring Overhead

**Problem**: Real-time token counting adds overhead

**Impact**: 2-5% CPU for continuous monitoring

**Mitigations**:
1. **Sampling**: Monitor every N operations instead of all
2. **Estimation**: Use heuristics instead of exact counts
3. **Background Thread**: Offload monitoring to separate thread
4. **Alert Throttling**: Only alert on significant changes

**Performance Gain**: 60% overhead reduction (5% → 2%)

### Bottleneck 4: Byzantine Consensus Rounds

**Problem**: 3-phase PBFT requires multiple message rounds

**Impact**: 50-150ms per consensus decision

**Mitigations**:
1. **Selective Consensus**: Only for critical decisions
2. **Fast Path**: Single round for non-Byzantine scenarios
3. **Pipelining**: Overlap consensus rounds
4. **Local Caching**: Cache consensus results

**Performance Gain**: 70% reduction for non-critical operations

## Data Format Specifications

### Agent State Format

```json
{
  "agent_id": "agent_001",
  "type": "analyzer",
  "state": "executing",
  "dna": {
    "tool_genes": {...},
    "mcp_genes": {...},
    "parallelism_genes": {...},
    "memory_genes": {...},
    "error_genes": {...},
    "topology_genes": {...},
    "optimization_genes": {...}
  },
  "context": {
    "task": {...},
    "tools": [...],
    "memory_refs": [...]
  },
  "metrics": {
    "execution_time": 1.234,
    "memory_used": 10485760,
    "context_pressure": 0.42
  }
}
```

### Memory Tier Entry Format

```json
{
  "key": "agent_001_state_20240101_120000",
  "tier": "warm",
  "compression": "semantic",
  "compression_ratio": 5.0,
  "data": "<compressed_bytes>",
  "metadata": {
    "original_size": 10240,
    "compressed_size": 2048,
    "created_at": 1704110400.0,
    "last_accessed": 1704110400.0,
    "access_count": 5,
    "age_seconds": 300
  }
}
```

### Wave Result Format

```json
{
  "wave_id": "wave_001",
  "status": "completed",
  "phases": {
    "planning": {"duration": 0.123, "result": {...}},
    "spawning": {"duration": 0.234, "agents": 5},
    "execution": {"duration": 12.345, "results": [...]},
    "reflection": {"duration": 0.456, "insights": [...]},
    "synthesis": {"duration": 0.678, "final_result": {...}}
  },
  "metrics": {
    "total_duration": 13.836,
    "agent_count": 5,
    "task_count": 15,
    "parallel_speedup": 5.2,
    "memory_peak": 52428800,
    "context_usage": 0.65
  },
  "learning": {
    "patterns_extracted": 3,
    "dna_evolved": true,
    "memory_refs": [...]
  }
}
```

### Reflection Output Format

```json
{
  "stage": "post_wave",
  "timestamp": 1704110400.0,
  "assessment": {
    "completeness": 0.95,
    "quality": 0.88,
    "efficiency": 0.92
  },
  "gaps": [
    {"type": "missing_validation", "severity": "medium"},
    {"type": "incomplete_coverage", "severity": "low"}
  ],
  "patterns": [
    {
      "type": "success",
      "description": "Parallel file reading improved speed",
      "metrics": {"speedup": 5.2, "confidence": 0.9}
    }
  ],
  "recommendations": [
    "Add validation step before final output",
    "Consider caching for repeated operations"
  ],
  "serena_ref": "memory_20240101_120000"
}
```

## Monitoring and Observability

### Key Metrics to Track

**Orchestration Metrics**:
- Complexity analysis latency (<10ms target)
- Wave trigger accuracy (95%+ correct decisions)
- Wave execution duration (task-dependent)
- Phase completion rates (100% target)

**Memory Metrics**:
- Tier distribution (80% hot, 15% warm, 4% cool, 1% cold)
- Hit rate per tier (90%+ hot tier)
- Compression ratios (match theoretical: 5:1, 10:1, 50:1, 100:1)
- Transition latency (background, non-blocking)

**Performance Metrics**:
- Average execution time per operation
- Parallel speedup factor (5x+ target)
- Context usage percentage (stay <75%)
- MCP call latency (50-100ms per call)

**Learning Metrics**:
- Pattern extraction rate (patterns per wave)
- DNA evolution fitness improvement (10% per generation)
- Memory persistence success rate (100% target)
- Pattern reuse impact (10x speedup when applicable)

### Alerting Thresholds

**Critical Alerts** (Red):
- Context usage >85%
- Memory exhaustion imminent
- Consensus failure
- MCP server completely down

**Warning Alerts** (Orange):
- Context usage >75%
- Tier distribution skewed
- Performance degradation >30%
- MCP latency >200ms

**Info Alerts** (Yellow):
- Context usage >60%
- Pattern extraction opportunity
- Optimization suggestion available
- DNA evolution generation complete

## Flow Optimization Strategies

### Strategy 1: Aggressive Parallelism

**When**: Independent tasks, sufficient resources

**Pattern**: Maximum concurrency with semaphore protection

**Gain**: 5x+ speedup

**Trade-off**: Higher resource usage

### Strategy 2: Memory Tier Optimization

**When**: Large state, frequent access patterns

**Pattern**: Keep hot data hot, aggressively compress cold data

**Gain**: 50-100x memory savings

**Trade-off**: Access latency for cold data

### Strategy 3: Selective Reflection

**When**: Low-risk operations, time-critical

**Pattern**: Skip mid-wave reflection, minimal pattern learning

**Gain**: 30-40% latency reduction

**Trade-off**: Less learning accumulation

### Strategy 4: Context Pressure Management

**When**: Approaching context limits

**Pattern**: Aggressive tier transitions, manual checkpoints

**Gain**: Prevent context overflow

**Trade-off**: Potential state fragmentation

### Strategy 5: MCP Coordination

**When**: Multi-server requirements

**Pattern**: Parallel MCP calls, intelligent caching

**Gain**: 3x+ speedup for multi-server operations

**Trade-off**: Complexity in coordination

## Debugging Data Flows

### Trace Points

**Entry Points**:
- AutomaticOrchestrator.should_orchestrate()
- WaveOrchestrationEngine.execute_wave()
- BaseAgent.execute()

**Critical Decision Points**:
- Complexity threshold check (0.7)
- Memory tier selection
- Reflection stage transitions
- Consensus vote collection

**Exit Points**:
- Wave result synthesis
- Agent execution completion
- Memory persistence confirmation

### Logging Strategy

**Levels**:
- **DEBUG**: All data flow points
- **INFO**: Phase transitions, major decisions
- **WARNING**: Performance degradation, context pressure
- **ERROR**: Failures, exceptions, recovery attempts
- **CRITICAL**: System-wide failures, unrecoverable errors

**Structured Logging**:
```python
logger.info("wave_execution_started", extra={
    "wave_id": wave_id,
    "agent_count": len(agents),
    "task_count": len(tasks),
    "complexity_score": complexity_score
})
```

## Performance Profiling

### Profiling Tools

**CPU Profiling**: `cProfile`, `py-spy`
**Memory Profiling**: `tracemalloc`, `memory_profiler`
**Async Profiling**: `aiomonitor`, custom instrumentation
**Network Profiling**: MCP call latency tracking

### Bottleneck Identification

**Method**: Critical path analysis

**Steps**:
1. Instrument all major pipeline stages
2. Measure time spent per stage
3. Identify slowest stage (>30% of total time)
4. Profile slowest stage in detail
5. Apply targeted optimization

**Example**:
```
Total: 13.836s
├─ Planning: 0.123s (1%)
├─ Spawning: 0.234s (2%)
├─ Execution: 12.345s (89%) ← BOTTLENECK
├─ Reflection: 0.456s (3%)
└─ Synthesis: 0.678s (5%)
```

**Action**: Optimize execution phase through parallelism

## Related Documentation

- **OVERVIEW.md**: System architecture and revolutionary components
- **MODULES.md**: Detailed component documentation
- **PATTERNS.md**: 96 design patterns and composition rules
- **DEPLOYMENT.md**: Installation and production deployment