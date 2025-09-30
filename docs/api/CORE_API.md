# Core API Reference

Complete API documentation for Shannon Framework core components.

## Table of Contents
- [WaveOrchestrator](#waveorchestrator)
- [ComplexityAnalyzer](#complexityanalyzer)
- [BaseAgent](#baseagent)
- [WaveConfig](#waveconfig)
- [WaveResult](#waveresult)

---

## WaveOrchestrator

Master coordination class for wave execution, complexity analysis, and agent lifecycle management.

### Class Definition

```python
class WaveOrchestrator:
    def __init__(self, config: Dict[str, Any])
```

**Parameters:**
- `config` (Dict[str, Any]): Orchestrator configuration
  - `complexity_threshold` (float, optional): Threshold for auto-triggering (default: 0.7)
  - `max_concurrent_agents` (int, optional): Maximum concurrent agents (default: 10)

**Example:**
```python
orchestrator = WaveOrchestrator({
    'complexity_threshold': 0.7,
    'max_concurrent_agents': 10
})
```

### Methods

#### analyze_and_decide()

Analyze task complexity and determine if wave orchestration is needed.

```python
async def analyze_and_decide(
    self,
    task: Dict[str, Any]
) -> OrchestrationDecision
```

**Parameters:**
- `task` (Dict[str, Any]): Task specification with complexity indicators
  - `scope_indicators` (Dict): File/directory/line counts
  - `dependencies` (List): Task dependencies
  - `operations` (List): Operation specifications
  - `domains` (List): Domain classifications
  - `parallel_opportunities` (int): Parallelization count
  - `risk_indicators` (Dict): Risk assessment data

**Returns:**
- `OrchestrationDecision`: Analysis result with recommendation

**Example:**
```python
task = {
    'scope_indicators': {
        'file_count': 75,
        'dir_count': 12,
        'line_count': 15000
    },
    'operations': [
        {'type': 'refactor'},
        {'type': 'test'}
    ],
    'domains': ['backend', 'frontend'],
    'parallel_opportunities': 8
}

decision = await orchestrator.analyze_and_decide(task)
print(f"Orchestrate: {decision.should_orchestrate}")
print(f"Strategy: {decision.recommended_strategy.value}")
print(f"Agents: {decision.recommended_agent_count}")
```

#### execute_wave()

Execute complete wave with all phases.

```python
async def execute_wave(
    self,
    wave_config: WaveConfig,
    agent_factory: Dict[str, type]
) -> WaveResult
```

**Parameters:**
- `wave_config` (WaveConfig): Wave execution configuration
- `agent_factory` (Dict[str, type]): Mapping of agent type names to agent classes

**Returns:**
- `WaveResult`: Aggregated execution results

**Example:**
```python
from shannon import WaveConfig, WavePhase, ValidationLevel, AgentAllocation

wave_config = WaveConfig(
    wave_id="wave_001",
    objective="Refactor authentication system",
    phases=[
        AgentAllocation(
            phase=WavePhase.ANALYSIS,
            agent_count=2,
            agent_types=['CodeAnalyzer', 'SecurityAnalyzer'],
            parallel_execution=True,
            timeout_seconds=300
        ),
        AgentAllocation(
            phase=WavePhase.IMPLEMENTATION,
            agent_count=3,
            agent_types=['Refactorer', 'Tester', 'Documenter'],
            parallel_execution=False,
            timeout_seconds=600
        )
    ],
    validation_level=ValidationLevel.STRICT
)

agent_factory = {
    'CodeAnalyzer': CodeAnalyzerAgent,
    'SecurityAnalyzer': SecurityAnalyzerAgent,
    'Refactorer': RefactorerAgent,
    'Tester': TesterAgent,
    'Documenter': DocumenterAgent
}

result = await orchestrator.execute_wave(wave_config, agent_factory)
print(f"Success: {result.success}")
print(f"Duration: {result.total_duration_seconds:.2f}s")
print(f"Success Rate: {result.success_rate():.1%}")
```

#### cleanup()

Clean up orchestrator resources.

```python
async def cleanup(self)
```

**Example:**
```python
await orchestrator.cleanup()
```

---

## ComplexityAnalyzer

8-dimensional complexity analysis engine for automatic wave triggering.

### Class Definition

```python
class ComplexityAnalyzer:
    def __init__(self, threshold: float = 0.7)
```

**Parameters:**
- `threshold` (float): Complexity threshold (0.0-1.0, default: 0.7)

**Raises:**
- `ValueError`: If threshold outside valid range

### Methods

#### analyze()

Perform 8-dimensional complexity analysis.

```python
async def analyze(
    self,
    task: Dict[str, Any]
) -> ComplexityScore
```

**Dimensions Analyzed:**
1. **Scope**: File/directory/line counts
2. **Dependencies**: Internal and external dependencies
3. **Operations**: Operation type complexity
4. **Domains**: Multi-domain involvement
5. **Concurrency**: Parallelization opportunities
6. **Uncertainty**: Requirement clarity
7. **Risk**: Production/security impact
8. **Scale**: User/data/request volume

**Returns:**
- `ComplexityScore`: 8-dimensional analysis result
  - Each dimension scored 0.0-1.0
  - `total`: Averaged complexity score
  - `threshold_exceeded`: Boolean trigger flag

**Example:**
```python
analyzer = ComplexityAnalyzer(threshold=0.7)

task = {
    'scope_indicators': {'file_count': 50, 'dir_count': 8},
    'dependencies': ['auth', 'db', 'cache'],
    'operations': [{'type': 'refactor'}, {'type': 'optimize'}],
    'domains': ['backend', 'frontend', 'database'],
    'parallel_opportunities': 5,
    'risk_indicators': {'production_impact': True},
    'scale_indicators': {'user_count': 100000}
}

complexity = await analyzer.analyze(task)
print(f"Total: {complexity.total:.3f}")
print(f"Scope: {complexity.scope:.3f}")
print(f"Risk: {complexity.risk:.3f}")
print(f"Trigger: {complexity.threshold_exceeded}")
```

---

## BaseAgent

Abstract base agent with state management and execution framework.

### Class Definition

```python
class BaseAgent(ABC):
    def __init__(
        self,
        agent_id: str,
        capabilities: Set[AgentCapability],
        config: Dict[str, Any]
    )
```

**Parameters:**
- `agent_id` (str): Unique agent identifier
- `capabilities` (Set[AgentCapability]): Agent capability set
- `config` (Dict[str, Any]): Agent configuration dictionary

**Agent States:**
- `CREATED`: Initial state
- `INITIALIZING`: Resource initialization in progress
- `READY`: Ready for execution
- `EXECUTING`: Task execution in progress
- `COMPLETED`: Successfully completed
- `FAILED`: Execution failed
- `CANCELLED`: Execution cancelled

**Agent Capabilities:**
- `ANALYSIS`: Code and system analysis
- `BUILDING`: Building and compilation
- `TESTING`: Testing and validation
- `DOCUMENTATION`: Documentation generation
- `OPTIMIZATION`: Performance optimization
- `VALIDATION`: Quality validation
- `RESEARCH`: Research and investigation
- `INTEGRATION`: System integration

### Methods

#### initialize()

Initialize agent resources and prepare for execution.

```python
async def initialize(self) -> bool
```

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
agent = MyAgent(
    agent_id="agent_001",
    capabilities={AgentCapability.ANALYSIS, AgentCapability.TESTING},
    config={'timeout': 300}
)

success = await agent.initialize()
if success:
    print(f"Agent {agent.agent_id} ready")
```

#### run()

Execute agent task with full lifecycle management.

```python
async def run(
    self,
    task: Dict[str, Any]
) -> AgentResult
```

**Parameters:**
- `task` (Dict[str, Any]): Task specification dictionary

**Returns:**
- `AgentResult`: Execution result with metrics
  - `success` (bool): Execution success flag
  - `output` (Any): Task output
  - `metrics` (AgentMetrics): Performance metrics
  - `error_message` (Optional[str]): Error message if failed
  - `error_traceback` (Optional[str]): Full traceback if failed

**Example:**
```python
task = {
    'action': 'analyze_code',
    'files': ['module1.py', 'module2.py'],
    'focus': 'security'
}

result = await agent.run(task)
if result.success:
    print(f"Output: {result.output}")
    print(f"Duration: {result.metrics.execution_time_seconds:.2f}s")
else:
    print(f"Error: {result.error_message}")
```

#### execute()

Abstract method for agent-specific task logic. Must be implemented by subclasses.

```python
@abstractmethod
async def execute(
    self,
    task: Dict[str, Any]
) -> Any
```

**Parameters:**
- `task` (Dict[str, Any]): Task specification

**Returns:**
- `Any`: Task execution result

**Example Implementation:**
```python
class MyAnalyzerAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        files = task.get('files', [])
        focus = task.get('focus', 'general')

        # Perform analysis
        results = []
        for file in files:
            analysis = self._analyze_file(file, focus)
            results.append(analysis)

        return {
            'analyzed_files': len(files),
            'findings': results,
            'focus_area': focus
        }
```

#### cancel()

Cancel agent execution.

```python
async def cancel(self)
```

**Example:**
```python
# In another coroutine
await agent.cancel()
```

#### has_capability()

Check if agent has specific capability.

```python
def has_capability(
    self,
    capability: AgentCapability
) -> bool
```

**Returns:**
- `bool`: True if agent has capability

**Example:**
```python
if agent.has_capability(AgentCapability.TESTING):
    print("Agent can perform testing")
```

---

## WaveConfig

Complete wave configuration specification.

### Class Definition

```python
@dataclass
class WaveConfig:
    wave_id: str
    objective: str
    phases: List[AgentAllocation]
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    max_parallel_agents: int = 5
    total_timeout_seconds: int = 3600
    enable_learning: bool = True
    enable_reflection: bool = True
    checkpoint_interval_seconds: int = 300
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)
```

**Parameters:**
- `wave_id` (str): Unique wave identifier
- `objective` (str): Wave objective description
- `phases` (List[AgentAllocation]): Phase allocations
- `validation_level` (ValidationLevel): Validation strictness
  - `MINIMAL`: Basic validation
  - `STANDARD`: Normal validation (default)
  - `STRICT`: Enhanced validation
  - `PRODUCTION`: Maximum validation
- `max_parallel_agents` (int): Max concurrent agents (default: 5)
- `total_timeout_seconds` (int): Total wave timeout (default: 3600)
- `enable_learning` (bool): Enable pattern learning (default: True)
- `enable_reflection` (bool): Enable reflection hooks (default: True)
- `checkpoint_interval_seconds` (int): Checkpoint frequency (default: 300)
- `metadata` (Dict): Additional metadata
- `dependencies` (Set[str]): Dependent wave IDs

**Validation:**
- All fields validated on initialization
- Phase ordering verified
- Constraints checked

### Methods

#### get_phase_allocation()

Get allocation for specific phase.

```python
def get_phase_allocation(
    self,
    phase: WavePhase
) -> Optional[AgentAllocation]
```

**Returns:**
- `AgentAllocation`: Phase allocation or None

#### total_agent_count()

Calculate total agents across all phases.

```python
def total_agent_count(self) -> int
```

#### estimated_duration_seconds()

Estimate total wave duration.

```python
def estimated_duration_seconds(self) -> int
```

#### validate_dependencies()

Check if all dependencies are satisfied.

```python
def validate_dependencies(
    self,
    available_waves: Set[str]
) -> bool
```

#### to_dict() / from_dict()

Serialize/deserialize configuration.

```python
def to_dict(self) -> Dict
@classmethod
def from_dict(cls, data: Dict) -> 'WaveConfig'
```

**Example:**
```python
config = WaveConfig(
    wave_id="refactor_auth",
    objective="Refactor authentication system",
    phases=[
        AgentAllocation(
            phase=WavePhase.ANALYSIS,
            agent_count=2,
            agent_types=['SecurityAnalyzer', 'CodeAnalyzer'],
            parallel_execution=True,
            timeout_seconds=300,
            retry_limit=3
        )
    ],
    validation_level=ValidationLevel.PRODUCTION,
    enable_reflection=True
)

# Serialize
config_dict = config.to_dict()

# Deserialize
restored_config = WaveConfig.from_dict(config_dict)
```

---

## WaveResult

Aggregated wave execution results.

### Class Definition

```python
@dataclass
class WaveResult:
    wave_id: str
    success: bool
    phase_results: Dict[WavePhase, List[AgentResult]]
    total_duration_seconds: float
    agents_executed: int
    agents_succeeded: int
    agents_failed: int
    insights: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Parameters:**
- `wave_id` (str): Wave identifier
- `success` (bool): Overall success flag
- `phase_results` (Dict): Results by phase
- `total_duration_seconds` (float): Total execution time
- `agents_executed` (int): Total agents executed
- `agents_succeeded` (int): Successful agents
- `agents_failed` (int): Failed agents
- `insights` (List[str]): Learned insights
- `errors` (List[str]): Error messages
- `metadata` (Dict): Additional metadata

### Methods

#### success_rate()

Calculate agent success rate.

```python
def success_rate(self) -> float
```

**Returns:**
- `float`: Success rate (0.0-1.0)

#### phase_success_rate()

Calculate success rate for specific phase.

```python
def phase_success_rate(
    self,
    phase: WavePhase
) -> float
```

**Returns:**
- `float`: Phase success rate

#### get_all_agent_results()

Flatten all agent results across phases.

```python
def get_all_agent_results(self) -> List[AgentResult]
```

**Returns:**
- `List[AgentResult]`: All agent results

#### to_dict()

Serialize to dictionary.

```python
def to_dict(self) -> Dict
```

**Example:**
```python
result = await orchestrator.execute_wave(config, agent_factory)

print(f"Wave: {result.wave_id}")
print(f"Success: {result.success}")
print(f"Duration: {result.total_duration_seconds:.2f}s")
print(f"Agents: {result.agents_executed} executed, {result.agents_succeeded} succeeded")
print(f"Success Rate: {result.success_rate():.1%}")

# Phase-specific metrics
for phase in WavePhase:
    rate = result.phase_success_rate(phase)
    if rate > 0:
        print(f"{phase.value}: {rate:.1%} success")

# All results
all_results = result.get_all_agent_results()
for agent_result in all_results:
    print(f"  Agent {agent_result.agent_id}: {agent_result.success}")
```

---

## AgentAllocation

Agent distribution across wave phases.

### Class Definition

```python
@dataclass
class AgentAllocation:
    phase: WavePhase
    agent_count: int
    agent_types: List[str]
    parallel_execution: bool
    timeout_seconds: int
    retry_limit: int = 3
```

**Parameters:**
- `phase` (WavePhase): Wave phase
  - `DISCOVERY`: Initial discovery
  - `ANALYSIS`: Analysis and investigation
  - `SYNTHESIS`: Synthesis and planning
  - `IMPLEMENTATION`: Implementation and changes
  - `VALIDATION`: Testing and validation
- `agent_count` (int): Number of agents (must be positive)
- `agent_types` (List[str]): Agent type identifiers
- `parallel_execution` (bool): Execute agents in parallel
- `timeout_seconds` (int): Phase timeout (must be positive)
- `retry_limit` (int): Retry attempts (default: 3)

**Validation:**
- All parameters validated on initialization
- Agent count must match agent_types length

**Example:**
```python
allocation = AgentAllocation(
    phase=WavePhase.IMPLEMENTATION,
    agent_count=3,
    agent_types=['Refactorer', 'Tester', 'Documenter'],
    parallel_execution=False,
    timeout_seconds=600,
    retry_limit=2
)
```

---

## Complete Usage Example

```python
import asyncio
from shannon import (
    WaveOrchestrator,
    WaveConfig,
    WavePhase,
    AgentAllocation,
    ValidationLevel,
    BaseAgent,
    AgentCapability
)

# Define custom agent
class MyAnalyzerAgent(BaseAgent):
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Implement analysis logic
        return {'analysis': 'complete', 'findings': []}

# Initialize orchestrator
orchestrator = WaveOrchestrator({
    'complexity_threshold': 0.7,
    'max_concurrent_agents': 10
})

# Analyze task
task = {
    'scope_indicators': {'file_count': 75},
    'operations': [{'type': 'refactor'}],
    'domains': ['backend', 'frontend']
}

decision = await orchestrator.analyze_and_decide(task)

if decision.should_orchestrate:
    # Create wave configuration
    config = WaveConfig(
        wave_id="wave_001",
        objective="Refactor system",
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

    # Execute wave
    agent_factory = {'Analyzer': MyAnalyzerAgent}
    result = await orchestrator.execute_wave(config, agent_factory)

    print(f"Success: {result.success}")
    print(f"Duration: {result.total_duration_seconds:.2f}s")

# Cleanup
await orchestrator.cleanup()
```