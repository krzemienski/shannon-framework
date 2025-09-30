# Reflection System API Reference

Complete API documentation for Shannon Framework reflection and learning components with Serena MCP integration.

## Table of Contents
- [ReflectionEngine](#reflectionengine)
- [WaveReflectionHooks](#wavereflectionhooks)
- [Serena MCP Integration](#serena-mcp-integration)

---

## ReflectionEngine

5-stage reflection protocol with Serena MCP integration for continuous learning.

### Reflection Stages

1. **Information Assessment** (`think_about_collected_information`)
2. **Task Adherence Check** (`think_about_task_adherence`)
3. **Completion Evaluation** (`think_about_whether_you_are_done`)
4. **Pattern Learning** (extract and store patterns)
5. **Memory Persistence** (`write_memory` to Serena MCP)

### Class Definition

```python
class ReflectionEngine:
    def __init__(self, mcp_available: bool = True)
```

**Parameters:**
- `mcp_available` (bool): Whether Serena MCP tools are available (default: True)

**Features:**
- Automatic reflection at wave boundaries
- Real Serena MCP tool integration
- Pattern learning and cross-session persistence
- Evidence-based confidence adjustment
- Replanning triggers for course correction

### Methods

#### reflect()

Perform 5-stage reflection using Serena MCP tools.

```python
async def reflect(
    self,
    context: ReflectionContext
) -> ReflectionResult
```

**Parameters:**
- `context` (ReflectionContext): Reflection context with wave state
  - `wave_id` (str): Wave identifier
  - `phase` (str): Current wave phase
  - `point` (ReflectionPoint): When reflection occurs
  - `collected_information` (Dict): Information gathered
  - `task_adherence_score` (float): How well on-track (0.0-1.0)
  - `confidence_level` (float): Current confidence (0.0-1.0)
  - `errors_encountered` (List[str]): Error messages
  - `patterns_detected` (List[str]): Detected patterns
  - `decisions_made` (List[Dict]): Decisions made
  - `execution_time` (float): Execution time (seconds)
  - `resource_usage` (Dict): Resource metrics

**Returns:**
- `ReflectionResult`: Reflection outcome
  - `insights` (List[str]): Generated insights
  - `recommendations` (List[str]): Action recommendations
  - `confidence_adjustment` (float): Confidence delta (-1.0 to 1.0)
  - `should_continue` (bool): Whether to continue execution
  - `should_replan` (bool): Whether replanning needed
  - `learned_patterns` (Dict): Newly learned patterns
  - `memory_updates` (List[Dict]): Serena memory writes
  - `quality_score` (float): Information quality (0.0-1.0)
  - `completeness_score` (float): Task completion (0.0-1.0)

**Example:**
```python
from shannon.reflection import ReflectionEngine, ReflectionContext, ReflectionPoint

engine = ReflectionEngine(mcp_available=True)

# Create reflection context
context = ReflectionContext(
    wave_id="wave_2",
    phase="implementation",
    point=ReflectionPoint.POST_WAVE,
    collected_information={
        'files_modified': 15,
        'tests_passed': 42,
        'tests_failed': 3
    },
    task_adherence_score=0.85,
    confidence_level=0.90,
    patterns_detected=['async pattern', 'error handling pattern'],
    execution_time=450.5
)

# Perform reflection
result = await engine.reflect(context)

print(f"Insights: {len(result.insights)}")
for insight in result.insights:
    print(f"  - {insight}")

print(f"\nRecommendations: {len(result.recommendations)}")
for rec in result.recommendations:
    print(f"  - {rec}")

print(f"\nQuality Score: {result.quality_score:.2f}")
print(f"Confidence Adjustment: {result.confidence_adjustment:+.2f}")
print(f"Should Continue: {result.should_continue}")
print(f"Should Replan: {result.should_replan}")

# Learned patterns available for future waves
if result.learned_patterns:
    print(f"\nLearned Patterns: {len(result.learned_patterns)}")
    for pattern_name, pattern_data in result.learned_patterns.items():
        print(f"  {pattern_name}: {pattern_data}")
```

#### get_metrics()

Get reflection system metrics.

```python
def get_metrics(self) -> Dict[str, Any]
```

**Returns:**
- `Dict`: Reflection metrics
  - `total_reflections` (int): Total reflection count
  - `insights_generated` (int): Total insights
  - `replanning_triggered` (int): Replanning events
  - `patterns_learned` (int): Patterns discovered
  - `memory_writes` (int): Serena writes
  - `mcp_calls` (int): MCP tool calls
  - `avg_quality_score` (float): Average quality

**Example:**
```python
metrics = engine.get_metrics()

print(f"Total Reflections: {metrics['total_reflections']}")
print(f"Insights Generated: {metrics['insights_generated']}")
print(f"Patterns Learned: {metrics['patterns_learned']}")
print(f"Avg Quality: {metrics['avg_quality_score']:.2f}")
```

---

## ReflectionPoint

Enum defining when reflection occurs in wave execution.

### Values

```python
class ReflectionPoint(Enum):
    PRE_WAVE = "pre_wave"        # Before wave execution
    MID_WAVE = "mid_wave"        # During wave execution
    POST_WAVE = "post_wave"      # After wave completion
    INTER_WAVE = "inter_wave"    # Between multi-wave operations
    EMERGENCY = "emergency"      # Triggered by failures
```

**Usage:**
- **PRE_WAVE**: Validate readiness, load relevant memories
- **MID_WAVE**: Check progress, assess information quality
- **POST_WAVE**: Evaluate completion, learn patterns, persist memories
- **INTER_WAVE**: Synthesize cross-wave insights, adjust strategy
- **EMERGENCY**: Rapid assessment when errors occur or confusion detected

**Example:**
```python
from shannon.reflection import ReflectionPoint

# Pre-wave reflection
pre_context = ReflectionContext(
    wave_id="wave_3",
    phase="discovery",
    point=ReflectionPoint.PRE_WAVE,
    collected_information={},
    task_adherence_score=1.0,
    confidence_level=0.8
)

# Mid-wave check
mid_context = ReflectionContext(
    wave_id="wave_3",
    phase="analysis",
    point=ReflectionPoint.MID_WAVE,
    collected_information={'files_analyzed': 50},
    task_adherence_score=0.75,
    confidence_level=0.85
)

# Post-wave learning
post_context = ReflectionContext(
    wave_id="wave_3",
    phase="validation",
    point=ReflectionPoint.POST_WAVE,
    collected_information={'validation_complete': True},
    task_adherence_score=0.90,
    confidence_level=0.95
)
```

---

## WaveReflectionHooks

Integration hooks for wave orchestrator reflection.

### Class Definition

```python
class WaveReflectionHooks:
    def __init__(
        self,
        engine: ReflectionEngine,
        enable_pre_wave: bool = True,
        enable_mid_wave: bool = True,
        enable_post_wave: bool = True,
        mid_wave_interval: int = 5
    )
```

**Parameters:**
- `engine` (ReflectionEngine): Reflection engine instance
- `enable_pre_wave` (bool): Enable pre-wave reflection (default: True)
- `enable_mid_wave` (bool): Enable mid-wave reflection (default: True)
- `enable_post_wave` (bool): Enable post-wave reflection (default: True)
- `mid_wave_interval` (int): Agent interval for mid-wave checks (default: 5)

### Methods

#### pre_wave_reflection()

Execute pre-wave reflection before wave starts.

```python
async def pre_wave_reflection(
    self,
    wave_config: WaveConfig
) -> ReflectionResult
```

**Parameters:**
- `wave_config` (WaveConfig): Wave configuration

**Returns:**
- `ReflectionResult`: Pre-wave assessment

**Example:**
```python
from shannon.reflection import WaveReflectionHooks, ReflectionEngine
from shannon import WaveConfig

engine = ReflectionEngine()
hooks = WaveReflectionHooks(engine)

# Before wave execution
result = await hooks.pre_wave_reflection(wave_config)

if not result.should_continue:
    print("⚠️ Pre-wave check failed, aborting")
    for rec in result.recommendations:
        print(f"  - {rec}")
else:
    print("✅ Pre-wave check passed, proceeding")
```

#### mid_wave_reflection()

Execute mid-wave reflection during execution.

```python
async def mid_wave_reflection(
    self,
    wave_id: str,
    current_phase: str,
    agents_completed: int,
    agents_total: int,
    partial_results: List[AgentResult]
) -> ReflectionResult
```

**Parameters:**
- `wave_id` (str): Wave identifier
- `current_phase` (str): Current phase name
- `agents_completed` (int): Agents completed
- `agents_total` (int): Total agents
- `partial_results` (List[AgentResult]): Results so far

**Returns:**
- `ReflectionResult`: Mid-wave assessment

**Example:**
```python
# During wave execution
result = await hooks.mid_wave_reflection(
    wave_id="wave_2",
    current_phase="implementation",
    agents_completed=3,
    agents_total=5,
    partial_results=completed_agents
)

if result.should_replan:
    print("🔄 Replanning triggered")
    for rec in result.recommendations:
        print(f"  - {rec}")
    # Trigger replanning logic
```

#### post_wave_reflection()

Execute post-wave reflection after completion.

```python
async def post_wave_reflection(
    self,
    wave_result: WaveResult
) -> ReflectionResult
```

**Parameters:**
- `wave_result` (WaveResult): Complete wave results

**Returns:**
- `ReflectionResult`: Post-wave learning

**Example:**
```python
# After wave completion
result = await hooks.post_wave_reflection(wave_result)

print(f"✅ Wave complete")
print(f"Quality Score: {result.quality_score:.2f}")
print(f"Completeness: {result.completeness_score:.1%}")

print(f"\nInsights:")
for insight in result.insights:
    print(f"  - {insight}")

print(f"\nPatterns Learned: {len(result.learned_patterns)}")
print(f"Serena Memories Written: {len(result.memory_updates)}")
```

---

## Serena MCP Integration

Shannon's reflection system integrates with Serena MCP tools for deep learning capabilities.

### Integrated Serena Tools

#### think_about_collected_information()

Stage 1 reflection tool - assess information quality and completeness.

```python
# Called automatically by ReflectionEngine during stage 1
# MCP tool signature:
mcp__serena__think_about_collected_information()
```

**Purpose**: Evaluate gathered information
**Returns**: Quality assessment, gaps identified
**Triggers**: MID_WAVE, POST_WAVE reflection points

#### think_about_task_adherence()

Stage 2 reflection tool - verify staying on track.

```python
# Called automatically by ReflectionEngine during stage 2
# MCP tool signature:
mcp__serena__think_about_task_adherence()
```

**Purpose**: Check alignment with objectives
**Returns**: Adherence score, correction recommendations
**Triggers**: When task_adherence_score < 0.8

#### think_about_whether_you_are_done()

Stage 3 reflection tool - evaluate completion.

```python
# Called automatically by ReflectionEngine during stage 3
# MCP tool signature:
mcp__serena__think_about_whether_you_are_done()
```

**Purpose**: Assess task completion
**Returns**: Completion percentage, remaining tasks
**Triggers**: POST_WAVE reflection point

#### write_memory()

Stage 5 persistence tool - store learnings.

```python
# Called automatically by ReflectionEngine during stage 5
# MCP tool signature:
mcp__serena__write_memory(memory_name: str, content: str)
```

**Purpose**: Persist insights and patterns
**Returns**: Memory key for future retrieval
**Triggers**: When insights, patterns, or POST_WAVE

### Memory Naming Conventions

Shannon uses structured memory names for cross-session learning:

```python
# Wave synthesis memories
f"wave_{wave_id}_synthesis"

# Pattern memories
f"pattern_{pattern_type}_{timestamp}"

# Insight memories
f"insight_{domain}_{timestamp}"

# Reflection histories
f"reflection_{wave_id}_{phase}"
```

**Example:**
```python
# Memories created during reflection
memory_updates = [
    {
        'memory_name': 'wave_2_synthesis',
        'content': 'Wave 2 implementation insights...'
    },
    {
        'memory_name': 'pattern_async_execution_2024',
        'content': 'Async execution pattern discovered...'
    }
]
```

### Reading Memories

```python
# Read previous wave learnings
# MCP tool signature:
mcp__serena__read_memory(memory_file_name: str)

# Example usage in reflection
previous_insights = await serena.read_memory("wave_1_synthesis")
previous_patterns = await serena.read_memory("pattern_error_handling_2024")
```

---

## Complete Usage Example

```python
import asyncio
from shannon import WaveOrchestrator, WaveConfig, WavePhase, AgentAllocation
from shannon.reflection import (
    ReflectionEngine,
    WaveReflectionHooks,
    ReflectionContext,
    ReflectionPoint
)

async def main():
    # Initialize reflection system
    engine = ReflectionEngine(mcp_available=True)
    hooks = WaveReflectionHooks(
        engine=engine,
        enable_pre_wave=True,
        enable_mid_wave=True,
        enable_post_wave=True,
        mid_wave_interval=5
    )

    # Initialize orchestrator
    orchestrator = WaveOrchestrator({
        'complexity_threshold': 0.7,
        'max_concurrent_agents': 10,
        'reflection_engine': engine,
        'reflection_hooks': hooks
    })

    # Create wave configuration
    wave_config = WaveConfig(
        wave_id="wave_3",
        objective="Implement advanced features",
        phases=[
            AgentAllocation(
                phase=WavePhase.IMPLEMENTATION,
                agent_count=5,
                agent_types=['FeatureImplementer'] * 5,
                parallel_execution=True,
                timeout_seconds=600
            )
        ],
        enable_reflection=True
    )

    # Pre-wave reflection
    print("🔍 Pre-wave reflection...")
    pre_result = await hooks.pre_wave_reflection(wave_config)

    if not pre_result.should_continue:
        print("⚠️ Pre-wave check failed")
        return

    # Execute wave with reflection
    print("\n🚀 Executing wave...")
    wave_result = await orchestrator.execute_wave(
        wave_config,
        agent_factory={'FeatureImplementer': MyAgent}
    )

    # Post-wave reflection
    print("\n💭 Post-wave reflection...")
    post_result = await hooks.post_wave_reflection(wave_result)

    # Display results
    print(f"\n✅ Wave Complete")
    print(f"Success Rate: {wave_result.success_rate():.1%}")
    print(f"Quality Score: {post_result.quality_score:.2f}")
    print(f"Completeness: {post_result.completeness_score:.1%}")

    print(f"\nInsights: {len(post_result.insights)}")
    for insight in post_result.insights:
        print(f"  • {insight}")

    print(f"\nLearned Patterns: {len(post_result.learned_patterns)}")
    for pattern_name in post_result.learned_patterns:
        print(f"  • {pattern_name}")

    print(f"\nSerena Memories: {len(post_result.memory_updates)}")
    for memory in post_result.memory_updates:
        print(f"  • {memory['memory_name']}")

    # Get reflection metrics
    metrics = engine.get_metrics()
    print(f"\nReflection Metrics:")
    print(f"  Total Reflections: {metrics['total_reflections']}")
    print(f"  Insights Generated: {metrics['insights_generated']}")
    print(f"  Patterns Learned: {metrics['patterns_learned']}")
    print(f"  Avg Quality: {metrics['avg_quality_score']:.2f}")

    # Cleanup
    await orchestrator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Emergency Reflection

Triggered automatically when critical issues occur:

```python
# Automatic triggers:
# - task_adherence_score < 0.5
# - Multiple agent failures
# - Resource exhaustion
# - Unexpected errors

# Emergency reflection provides:
# - Rapid assessment
# - Urgent action recommendations
# - Immediate replanning if needed
# - Error pattern analysis

# Example emergency context:
emergency_context = ReflectionContext(
    wave_id="wave_2",
    phase="implementation",
    point=ReflectionPoint.EMERGENCY,
    collected_information={'error_count': 5},
    task_adherence_score=0.3,
    confidence_level=0.4,
    errors_encountered=[
        'Agent timeout',
        'Resource limit exceeded',
        'Dependency conflict'
    ]
)

emergency_result = await engine.reflect(emergency_context)

if emergency_result.should_replan:
    print("🚨 Emergency replanning required")
    for action in emergency_result.recommendations:
        print(f"  ⚡ {action}")
```