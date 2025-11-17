# UnifiedOrchestrator Design Document

**Status**: Design Complete - Ready for Implementation
**Version**: 1.0
**Date**: 2025-11-17
**Author**: Shannon CLI Architecture Team

---

## Executive Summary

This document specifies the **UnifiedOrchestrator** - a facade-based consolidation layer that integrates two existing orchestrators without reimplementing their logic. The design prioritizes reuse, minimal command changes, and thread-safe subsystem sharing.

### Current State
- **ContextAwareOrchestrator** (V3): 481 lines, 8 subsystems, FUNCTIONAL ✅
- **orchestration.Orchestrator** (V4): 459 lines, skills-based, PARTIAL ⚠️
- **Problem**: Architectural layering confusion, duplicate initialization, unclear command integration

### Solution
**UnifiedOrchestrator** (~500 lines) delegates to both orchestrators via facade pattern, shares common subsystems, provides unified command interface.

---

## Architecture Overview

### 1. Architectural Pattern: Facade + Adapter

```
┌─────────────────────────────────────────────────────────────┐
│                    UnifiedOrchestrator                      │
│                     (Facade Layer)                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          Shared Subsystems (Thread-Safe)              │  │
│  │  - CacheManager                                       │  │
│  │  - ContextManager                                     │  │
│  │  - AnalyticsDatabase                                  │  │
│  │  - CostEstimator / BudgetEnforcer                     │  │
│  │  - MetricsCollector                                   │  │
│  │  - AgentPool                                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────┐              ┌───────────────────┐   │
│  │   V3 Adapter     │              │   V4 Adapter      │   │
│  │  (Intelligence)  │              │  (Execution)      │   │
│  └────────┬─────────┘              └─────────┬─────────┘   │
└───────────┼─────────────────────────────────┼──────────────┘
            │                                 │
            ▼                                 ▼
┌───────────────────────┐        ┌────────────────────────┐
│ ContextAwareOrchest.  │        │ orchestration.         │
│ (V3 - 481 lines)      │        │ Orchestrator           │
│                       │        │ (V4 - 459 lines)       │
│ Methods:              │        │                        │
│ - execute_analyze()   │        │ Methods:               │
│ - execute_wave()      │        │ - execute()            │
│ - execute_task()      │        │ - halt()               │
│                       │        │ - resume()             │
│ Subsystems:           │        │ - rollback()           │
│ - SDK Client          │        │                        │
│ - Model Selector      │        │ Subsystems:            │
│ - MCP Manager         │        │ - SkillExecutor        │
│ - Insights Generator  │        │ - ExecutionPlanner     │
└───────────────────────┘        │ - StateManager         │
                                 └────────────────────────┘
```

### 2. Key Design Principles

1. **Delegation Not Duplication**: UnifiedOrchestrator calls existing orchestrators, never reimplements
2. **Shared State**: Common subsystems instantiated once, passed to both orchestrators
3. **Minimal Changes**: Commands.py changes limited to import and initialization
4. **Graceful Degradation**: System works if individual subsystems fail
5. **Thread Safety**: Shared subsystems protected by locks where needed

---

## Interface Specification

### UnifiedOrchestrator Class

```python
class UnifiedOrchestrator:
    """Unified facade for V3 intelligence and V4 execution coordination.

    Consolidates two orchestrators without merging their implementations:
    - V3 ContextAwareOrchestrator: Analysis, context, optimization
    - V4 orchestration.Orchestrator: Skills, planning, state management

    Shares subsystems (cache, analytics, context, metrics) between both flows
    while maintaining separation of concerns.
    """

    def __init__(
        self,
        config: Optional[ShannonConfig] = None,
        enable_v3: bool = True,
        enable_v4: bool = True
    ):
        """Initialize unified orchestrator with shared subsystems.

        Args:
            config: Optional configuration (creates default if not provided)
            enable_v3: Enable V3 orchestrator (analysis intelligence)
            enable_v4: Enable V4 orchestrator (skills execution)
        """
        pass

    # ==========================================
    # V3 Intelligence Methods (Analysis Path)
    # ==========================================

    async def execute_analyze(
        self,
        spec_text: str,
        project_id: Optional[str] = None,
        use_cache: bool = True,
        show_metrics: bool = True,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute V3 specification analysis (delegates to ContextAwareOrchestrator).

        Signature matches ContextAwareOrchestrator.execute_analyze() EXACTLY.

        Args:
            spec_text: Specification text to analyze
            project_id: Optional project ID for context-aware analysis
            use_cache: Whether to check/use cache
            show_metrics: Whether to show live metrics dashboard
            session_id: Optional session ID for tracking

        Returns:
            Analysis result with complexity scores, domains, recommendations
        """
        pass

    async def execute_wave(
        self,
        wave_request: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Execute V3 wave-based implementation (delegates to ContextAwareOrchestrator).

        Args:
            wave_request: Wave execution request
            project_id: Optional project ID for context
            session_id: Session ID for tracking
            use_cache: Whether to use cached results

        Returns:
            Wave execution results
        """
        pass

    async def execute_task(
        self,
        spec_or_request: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute V3 combined analyze + wave workflow.

        Args:
            spec_or_request: Specification text or task request
            project_id: Optional project ID
            session_id: Session ID for tracking

        Returns:
            Combined analysis and wave results
        """
        pass

    # ==========================================
    # V4 Skills Methods (Execution Path)
    # ==========================================

    async def execute_skills(
        self,
        plan: ExecutionPlan,
        session_id: Optional[str] = None,
        dashboard_url: Optional[str] = None
    ) -> OrchestratorResult:
        """Execute V4 skills-based plan (delegates to orchestration.Orchestrator).

        Args:
            plan: ExecutionPlan to execute
            session_id: Optional session ID for event routing
            dashboard_url: Optional dashboard URL for streaming

        Returns:
            OrchestratorResult with execution details
        """
        pass

    async def halt_execution(self, reason: str = "User requested"):
        """Halt V4 execution (pause)."""
        pass

    async def resume_execution(self):
        """Resume V4 halted execution."""
        pass

    async def rollback(self, checkpoint_id: str):
        """Rollback V4 execution to checkpoint."""
        pass

    # ==========================================
    # Unified Methods (Combined Intelligence + Execution)
    # ==========================================

    async def execute_unified(
        self,
        spec_text: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        auto_execute: bool = False
    ) -> Dict[str, Any]:
        """Execute unified workflow: V3 analysis → V4 skills execution.

        Workflow:
        1. V3: Analyze specification (complexity, domains, recommendations)
        2. V4: Generate execution plan from analysis
        3. V4: Execute plan with skills
        4. Return combined results

        Args:
            spec_text: Specification to analyze and execute
            project_id: Optional project ID for context
            session_id: Session ID for tracking
            auto_execute: If False, pause before execution for approval

        Returns:
            Combined analysis and execution results
        """
        pass

    # ==========================================
    # Subsystem Access (Read-Only)
    # ==========================================

    @property
    def cache(self) -> Optional[CacheManager]:
        """Access shared cache manager."""
        pass

    @property
    def context(self) -> Optional[ContextManager]:
        """Access shared context manager."""
        pass

    @property
    def analytics(self) -> Optional[AnalyticsDatabase]:
        """Access shared analytics database."""
        pass

    @property
    def cost_optimizer(self) -> Dict[str, Any]:
        """Access shared cost optimization subsystems."""
        pass

    @property
    def agent_pool(self) -> Optional[AgentPool]:
        """Access shared agent pool."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get unified orchestrator status.

        Returns:
            Status including:
            - Enabled orchestrators (V3, V4)
            - Subsystem health
            - Current execution state
            - Resource utilization
        """
        pass
```

---

## Subsystem Sharing Strategy

### Shared Subsystems (Instantiated Once, Used by Both)

| Subsystem | Owner | V3 Usage | V4 Usage | Thread Safety |
|-----------|-------|----------|----------|---------------|
| **CacheManager** | Unified | Analysis caching | Skill result caching | ✅ Built-in locks |
| **ContextManager** | Unified | Project context loading | Context-aware execution | ✅ Read-only |
| **AnalyticsDatabase** | Unified | Session recording | Execution metrics | ✅ SQLite thread-safe |
| **CostEstimator** | Unified | Model selection | Skill cost tracking | ✅ Stateless |
| **BudgetEnforcer** | Unified | Budget checks | Cost limiting | ⚠️ Needs lock |
| **MetricsCollector** | Per-call | Live dashboards | Execution metrics | ✅ Instance per call |
| **AgentPool** | Unified | Agent state tracking | Parallel execution | ✅ Built-in locks |

### Specialized Subsystems (Not Shared)

| Subsystem | Orchestrator | Purpose |
|-----------|--------------|---------|
| **ShannonSDKClient** | V3 Only | Framework skill invocation |
| **ModelSelector** | V3 Only | Optimal model selection |
| **MCPManager** | V3 Only | MCP recommendation/installation |
| **InsightsGenerator** | V3 Only | Trend analysis and insights |
| **SkillExecutor** | V4 Only | Skills execution engine |
| **ExecutionPlanner** | V4 Only | Plan generation |
| **StateManager** | V4 Only | Checkpoints and rollback |

### Thread Safety Implementation

```python
# BudgetEnforcer requires locking (shared state)
import threading

class UnifiedOrchestrator:
    def __init__(self, config):
        # ...
        self._budget_lock = threading.RLock()
        self.budget_enforcer = BudgetEnforcer() if enabled else None

    async def _check_budget(self, cost: float) -> bool:
        """Thread-safe budget check."""
        if not self.budget_enforcer:
            return True

        with self._budget_lock:
            return self.budget_enforcer.check_available(cost)
```

---

## Migration Path

### Phase 1: Create UnifiedOrchestrator (1-2 hours)

**File**: `src/shannon/unified_orchestrator.py` (~500 lines)

```python
# Core structure
class UnifiedOrchestrator:
    def __init__(self, config, enable_v3=True, enable_v4=True):
        # Initialize shared subsystems
        self._init_shared_subsystems(config)

        # Initialize V3 orchestrator if enabled
        if enable_v3:
            self._init_v3_orchestrator(config)

        # Initialize V4 orchestrator if enabled
        if enable_v4:
            self._init_v4_orchestrator(config)

    def _init_shared_subsystems(self, config):
        """Initialize subsystems shared between V3 and V4."""
        # Cache, context, analytics, cost optimization, agent pool
        pass

    def _init_v3_orchestrator(self, config):
        """Initialize V3 orchestrator with shared subsystems."""
        # Create ContextAwareOrchestrator, inject shared subsystems
        pass

    def _init_v4_orchestrator(self, config):
        """Initialize V4 orchestrator with shared subsystems."""
        # Create orchestration.Orchestrator components
        pass
```

### Phase 2: Update Commands.py (30 minutes)

**Before** (Current - scattered imports):
```python
# In analyze command
from shannon.orchestrator import ContextAwareOrchestrator
orchestrator = ContextAwareOrchestrator(config)
result = await orchestrator.execute_analyze(spec_text, ...)

# In wave command
from shannon.orchestrator import ContextAwareOrchestrator
orchestrator = ContextAwareOrchestrator(config)
result = await orchestrator.execute_wave(wave_request, ...)
```

**After** (Unified):
```python
# At top of commands.py
from shannon.unified_orchestrator import UnifiedOrchestrator

# In analyze command
orchestrator = UnifiedOrchestrator(config)
result = await orchestrator.execute_analyze(spec_text, ...)

# In wave command
orchestrator = UnifiedOrchestrator(config)
result = await orchestrator.execute_wave(wave_request, ...)
```

**Changes Required**:
- Update 9 import statements
- Change initialization (same signature)
- No method signature changes (backward compatible)

### Phase 3: Testing & Validation (1 hour)

1. **Unit Tests**: Test subsystem sharing and delegation
2. **Integration Tests**: Test both V3 and V4 paths
3. **Command Tests**: Verify all commands still work

---

## Implementation Plan

### File Structure

```
src/shannon/
├── unified_orchestrator.py          # NEW: UnifiedOrchestrator (500 lines)
├── orchestrator.py                   # UNCHANGED: ContextAwareOrchestrator
├── orchestration/
│   ├── orchestrator.py               # UNCHANGED: orchestration.Orchestrator
│   └── ...
├── cli/
│   └── commands.py                   # MODIFIED: Update imports (9 lines)
└── tests/
    └── test_unified_orchestrator.py  # NEW: Test suite
```

### Estimated Lines of Code

```
UnifiedOrchestrator Implementation:
  - Class definition & init:        ~100 lines
  - Shared subsystem management:     ~80 lines
  - V3 delegation methods:           ~60 lines
  - V4 delegation methods:           ~60 lines
  - Unified methods:                 ~80 lines
  - Status & health checks:          ~40 lines
  - Thread safety & locking:         ~30 lines
  - Documentation & type hints:      ~50 lines

Total:                               ~500 lines
```

### Implementation Checklist

#### Step 1: Core Infrastructure (2 hours)
- [ ] Create `src/shannon/unified_orchestrator.py`
- [ ] Implement `__init__()` with shared subsystem initialization
- [ ] Add thread safety for BudgetEnforcer
- [ ] Implement graceful degradation (subsystems optional)

#### Step 2: V3 Delegation (1 hour)
- [ ] Implement `execute_analyze()` delegation
- [ ] Implement `execute_wave()` delegation
- [ ] Implement `execute_task()` delegation
- [ ] Pass shared subsystems to ContextAwareOrchestrator

#### Step 3: V4 Delegation (1 hour)
- [ ] Implement `execute_skills()` delegation
- [ ] Implement `halt_execution()`, `resume_execution()`, `rollback()`
- [ ] Configure V4 orchestrator with shared subsystems

#### Step 4: Unified Methods (1 hour)
- [ ] Implement `execute_unified()` workflow
- [ ] Add analysis → plan → execute pipeline
- [ ] Add approval gate for auto_execute=False

#### Step 5: Observability (30 minutes)
- [ ] Implement `get_status()` method
- [ ] Add subsystem health checks
- [ ] Add resource utilization tracking

#### Step 6: Commands Integration (30 minutes)
- [ ] Update `commands.py` imports
- [ ] Test `shannon analyze` command
- [ ] Test `shannon wave` command
- [ ] Test all other commands using orchestrator

#### Step 7: Testing (2 hours)
- [ ] Write unit tests for subsystem sharing
- [ ] Write integration tests for V3 path
- [ ] Write integration tests for V4 path
- [ ] Write integration tests for unified path
- [ ] Test thread safety under concurrent load

---

## Detailed Class Implementation

### Initialization Flow

```python
def __init__(
    self,
    config: Optional[ShannonConfig] = None,
    enable_v3: bool = True,
    enable_v4: bool = True
):
    """Initialize unified orchestrator with shared subsystems."""
    self.config = config or ShannonConfig()

    # ==========================================
    # Step 1: Initialize Shared Subsystems
    # ==========================================

    # Context Management (read-only, thread-safe)
    try:
        self.context = ContextManager()
        logger.info("Shared ContextManager initialized")
    except Exception as e:
        logger.warning(f"ContextManager init failed: {e}")
        self.context = None

    # Cache Management (has internal locks)
    try:
        cache_dir = self.config.config_dir / 'cache'
        self.cache = CacheManager(base_dir=cache_dir)
        logger.info("Shared CacheManager initialized")
    except Exception as e:
        logger.warning(f"CacheManager init failed: {e}")
        self.cache = None

    # Analytics Database (SQLite thread-safe)
    try:
        analytics_db_path = self.config.config_dir / 'analytics.db'
        self.analytics_db = AnalyticsDatabase(db_path=analytics_db_path)
        self.trend_analyzer = TrendAnalyzer(self.analytics_db)
        self.insights_generator = InsightsGenerator(
            self.analytics_db, self.trend_analyzer
        )
        logger.info("Shared Analytics subsystem initialized")
    except Exception as e:
        logger.warning(f"Analytics init failed: {e}")
        self.analytics_db = None
        self.trend_analyzer = None
        self.insights_generator = None

    # Cost Optimization (needs locking for BudgetEnforcer)
    self._budget_lock = threading.RLock()
    try:
        self.model_selector = ModelSelector()
        self.cost_estimator = CostEstimator()
        self.budget_enforcer = BudgetEnforcer()
        logger.info("Shared Cost Optimization initialized")
    except Exception as e:
        logger.warning(f"Cost optimization init failed: {e}")
        self.model_selector = None
        self.cost_estimator = None
        self.budget_enforcer = None

    # Agent Pool (has internal locks)
    try:
        self.agent_pool = AgentPool(max_active=8, max_total=50)
        logger.info("Shared AgentPool initialized")
    except Exception as e:
        logger.warning(f"AgentPool init failed: {e}")
        self.agent_pool = None

    # Metrics (created per-operation, not shared)
    # Each operation creates its own MetricsCollector instance

    # ==========================================
    # Step 2: Initialize V3 Orchestrator
    # ==========================================

    self.v3_orchestrator = None
    if enable_v3:
        try:
            # Create V3 orchestrator but override its subsystems
            # with our shared instances
            self.v3_orchestrator = ContextAwareOrchestrator(config)

            # Inject shared subsystems
            self.v3_orchestrator.context = self.context
            self.v3_orchestrator.cache = self.cache
            self.v3_orchestrator.analytics_db = self.analytics_db
            self.v3_orchestrator.trend_analyzer = self.trend_analyzer
            self.v3_orchestrator.insights_generator = self.insights_generator
            self.v3_orchestrator.model_selector = self.model_selector
            self.v3_orchestrator.cost_estimator = self.cost_estimator
            self.v3_orchestrator.budget_enforcer = self.budget_enforcer
            self.v3_orchestrator.agent_pool = self.agent_pool

            logger.info("V3 ContextAwareOrchestrator initialized with shared subsystems")
        except Exception as e:
            logger.warning(f"V3 orchestrator init failed: {e}")
            self.v3_orchestrator = None

    # ==========================================
    # Step 3: Initialize V4 Orchestrator Components
    # ==========================================

    self.v4_executor = None
    self.v4_planner = None
    self.v4_state_manager = None
    self.v4_orchestrator = None

    if enable_v4:
        try:
            from shannon.skills.registry import SkillRegistry
            from shannon.skills.executor import SkillExecutor
            from shannon.orchestration.planner import ExecutionPlanner
            from shannon.orchestration.state_manager import StateManager

            # Initialize V4 components
            registry = SkillRegistry()
            registry.auto_discover()

            self.v4_executor = SkillExecutor(
                registry=registry,
                cache_manager=self.cache  # Share cache
            )

            self.v4_planner = ExecutionPlanner()

            state_dir = self.config.config_dir / 'state'
            self.v4_state_manager = StateManager(state_dir=state_dir)

            logger.info("V4 orchestrator components initialized with shared subsystems")
        except Exception as e:
            logger.warning(f"V4 components init failed: {e}")

    logger.info(
        f"UnifiedOrchestrator initialized: "
        f"V3={'enabled' if self.v3_orchestrator else 'disabled'}, "
        f"V4={'enabled' if self.v4_executor else 'disabled'}"
    )
```

### V3 Delegation Methods

```python
async def execute_analyze(
    self,
    spec_text: str,
    project_id: Optional[str] = None,
    use_cache: bool = True,
    show_metrics: bool = True,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Execute V3 specification analysis."""
    if not self.v3_orchestrator:
        raise RuntimeError("V3 orchestrator not available")

    logger.info("Delegating to V3 ContextAwareOrchestrator.execute_analyze()")

    # Direct delegation - signature matches exactly
    return await self.v3_orchestrator.execute_analyze(
        spec_text=spec_text,
        project_id=project_id,
        use_cache=use_cache,
        show_metrics=show_metrics,
        session_id=session_id
    )

async def execute_wave(
    self,
    wave_request: str,
    project_id: Optional[str] = None,
    session_id: Optional[str] = None,
    use_cache: bool = True
) -> Dict[str, Any]:
    """Execute V3 wave-based implementation."""
    if not self.v3_orchestrator:
        raise RuntimeError("V3 orchestrator not available")

    logger.info("Delegating to V3 ContextAwareOrchestrator.execute_wave()")

    return await self.v3_orchestrator.execute_wave(
        wave_request=wave_request,
        project_id=project_id,
        session_id=session_id,
        use_cache=use_cache
    )

async def execute_task(
    self,
    spec_or_request: str,
    project_id: Optional[str] = None,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Execute V3 combined analyze + wave workflow."""
    if not self.v3_orchestrator:
        raise RuntimeError("V3 orchestrator not available")

    logger.info("Delegating to V3 ContextAwareOrchestrator.execute_task()")

    return await self.v3_orchestrator.execute_task(
        spec_or_request=spec_or_request,
        project_id=project_id,
        session_id=session_id
    )
```

### V4 Delegation Methods

```python
async def execute_skills(
    self,
    plan: ExecutionPlan,
    session_id: Optional[str] = None,
    dashboard_url: Optional[str] = None
) -> OrchestratorResult:
    """Execute V4 skills-based plan."""
    if not self.v4_executor:
        raise RuntimeError("V4 orchestrator not available")

    logger.info("Creating V4 Orchestrator instance for plan execution")

    from shannon.orchestration.orchestrator import Orchestrator

    # Create V4 orchestrator with shared subsystems
    self.v4_orchestrator = Orchestrator(
        plan=plan,
        executor=self.v4_executor,
        state_manager=self.v4_state_manager,
        session_id=session_id,
        dashboard_url=dashboard_url
    )

    # Execute plan
    return await self.v4_orchestrator.execute()

async def halt_execution(self, reason: str = "User requested"):
    """Halt V4 execution."""
    if not self.v4_orchestrator:
        raise RuntimeError("No active V4 execution")

    await self.v4_orchestrator.halt(reason)

async def resume_execution(self):
    """Resume V4 execution."""
    if not self.v4_orchestrator:
        raise RuntimeError("No active V4 execution")

    await self.v4_orchestrator.resume()

async def rollback(self, checkpoint_id: str):
    """Rollback V4 execution."""
    if not self.v4_orchestrator:
        raise RuntimeError("No active V4 execution")

    await self.v4_orchestrator.rollback(checkpoint_id)
```

### Unified Method

```python
async def execute_unified(
    self,
    spec_text: str,
    project_id: Optional[str] = None,
    session_id: Optional[str] = None,
    auto_execute: bool = False
) -> Dict[str, Any]:
    """Execute unified workflow: V3 analysis → V4 skills execution.

    This is the FUTURE of Shannon - combining V3 intelligence with V4 execution.
    """
    if not self.v3_orchestrator or not self.v4_executor:
        raise RuntimeError("Unified mode requires both V3 and V4 enabled")

    logger.info("Starting unified workflow: V3 analysis → V4 execution")

    # ==========================================
    # Phase 1: V3 Analysis (Intelligence)
    # ==========================================

    logger.info("Phase 1: Analyzing specification with V3")
    analysis_result = await self.execute_analyze(
        spec_text=spec_text,
        project_id=project_id,
        session_id=session_id
    )

    # ==========================================
    # Phase 2: V4 Plan Generation
    # ==========================================

    logger.info("Phase 2: Generating execution plan from analysis")

    # Convert analysis to plan request
    complexity = analysis_result.get('complexity_score', 0.0)
    domains = analysis_result.get('domains', {})

    plan_request = f"""
    Implement specification with:
    - Complexity: {complexity}
    - Domains: {', '.join(domains.keys())}
    - Context: Project {project_id}

    Specification:
    {spec_text}
    """

    from shannon.orchestration.task_parser import TaskParser

    parser = TaskParser()
    parsed_task = parser.parse(plan_request)

    plan = self.v4_planner.create_plan(parsed_task)

    # ==========================================
    # Phase 3: Approval Gate (if not auto)
    # ==========================================

    if not auto_execute:
        logger.info("Approval required - pausing before execution")
        # In real implementation, would prompt user or wait for approval
        print(f"\nGenerated plan with {len(plan.steps)} steps")
        print("Set auto_execute=True to skip approval")
        return {
            'analysis': analysis_result,
            'plan': plan.to_dict(),
            'status': 'awaiting_approval'
        }

    # ==========================================
    # Phase 4: V4 Execution
    # ==========================================

    logger.info("Phase 4: Executing plan with V4")
    execution_result = await self.execute_skills(
        plan=plan,
        session_id=session_id
    )

    # ==========================================
    # Phase 5: Return Unified Results
    # ==========================================

    return {
        'analysis': analysis_result,
        'plan': plan.to_dict(),
        'execution': execution_result.to_dict(),
        'status': 'completed' if execution_result.success else 'failed'
    }
```

---

## Benefits Analysis

### Immediate Benefits

1. **No Duplication**: ~940 lines of working code reused, zero reimplementation
2. **Minimal Changes**: 9 line changes in commands.py vs 50+ line rewrites
3. **Backward Compatible**: All existing command signatures preserved
4. **Graceful Degradation**: System works even if subsystems fail
5. **Thread Safety**: Shared state properly protected

### Long-Term Benefits

1. **Clear Separation**: V3 = intelligence, V4 = execution, UnifiedOrchestrator = coordination
2. **Easy Testing**: Can test V3 and V4 paths independently
3. **Future Migration**: Can deprecate V3 or V4 without breaking commands
4. **Subsystem Efficiency**: Cache/analytics/context shared, no duplicate state
5. **Observability**: Single `get_status()` shows entire system health

### Performance Benefits

1. **Memory**: Single instance of cache/analytics/context vs duplicates
2. **Speed**: Shared cache means both orchestrators benefit from same entries
3. **Cost**: Single BudgetEnforcer tracks total cost across both paths
4. **Metrics**: Unified metrics collection across all operations

---

## Testing Strategy

### Unit Tests

```python
# tests/test_unified_orchestrator.py

class TestUnifiedOrchestrator:
    def test_shared_subsystem_initialization(self):
        """Verify shared subsystems instantiated once."""
        orch = UnifiedOrchestrator()

        # Both orchestrators share same instances
        assert orch.v3_orchestrator.cache is orch.cache
        assert orch.v3_orchestrator.context is orch.context

    def test_v3_delegation(self):
        """Verify V3 methods delegate correctly."""
        # Test that execute_analyze calls through to V3
        pass

    def test_v4_delegation(self):
        """Verify V4 methods delegate correctly."""
        # Test that execute_skills calls through to V4
        pass

    def test_thread_safety(self):
        """Verify shared subsystems are thread-safe."""
        # Concurrent calls to both V3 and V4
        pass

    def test_graceful_degradation(self):
        """Verify system works with failed subsystems."""
        # Disable cache, verify analysis still works
        pass
```

### Integration Tests

```python
async def test_unified_workflow():
    """Test complete V3 analysis → V4 execution workflow."""
    orch = UnifiedOrchestrator()

    result = await orch.execute_unified(
        spec_text="Build a REST API",
        auto_execute=True
    )

    assert 'analysis' in result
    assert 'execution' in result
    assert result['status'] == 'completed'
```

---

## Risk Mitigation

### Risk 1: Subsystem Initialization Failures

**Mitigation**: Graceful degradation built into `__init__()`. Each subsystem wrapped in try/except, orchestrator continues with warnings.

### Risk 2: Thread Safety Issues

**Mitigation**:
- BudgetEnforcer protected by RLock
- CacheManager has internal locks
- ContextManager is read-only
- SQLite is thread-safe

### Risk 3: Breaking Changes to Commands

**Mitigation**: UnifiedOrchestrator methods match V3 signatures exactly. Commands.py changes limited to imports.

### Risk 4: V4 Orchestrator State Conflicts

**Mitigation**: V4 Orchestrator created per-execution, not shared. Each call gets fresh instance with shared subsystems.

---

## Success Criteria

### Implementation Success
- [ ] UnifiedOrchestrator passes all unit tests
- [ ] Both V3 and V4 paths work independently
- [ ] Unified path works end-to-end
- [ ] All 9 commands still functional after migration
- [ ] No performance regression vs current implementation

### Code Quality Success
- [ ] ~500 lines total (not exceeding 600)
- [ ] 100% type hints coverage
- [ ] Comprehensive docstrings
- [ ] Logging at INFO level for all operations
- [ ] Thread safety verified under load

### Integration Success
- [ ] `shannon analyze` works (V3 path)
- [ ] `shannon wave` works (V3 path)
- [ ] `shannon do` works (V4 path, future)
- [ ] Shared cache improves performance
- [ ] Analytics tracks both V3 and V4 operations

---

## Appendix A: Subsystem Interface Summary

### CacheManager
```python
class CacheManager:
    def __init__(self, base_dir: Path): ...

    # Analysis cache (V3 usage)
    def analysis.get(spec_text: str, context: Any) -> Optional[Dict]: ...
    def analysis.save(spec_text: str, result: Dict, context: Any): ...

    # Skill cache (V4 usage)
    def skill.get(skill_name: str, params: Dict) -> Optional[SkillResult]: ...
    def skill.save(skill_name: str, params: Dict, result: SkillResult): ...
```

### ContextManager
```python
class ContextManager:
    def load_project(project_id: str) -> Dict[str, Any]: ...
    def update_analysis_metadata(project_id: str, analysis: Dict): ...
    # Read-only operations - thread-safe
```

### AnalyticsDatabase
```python
class AnalyticsDatabase:
    def __init__(self, db_path: Path): ...

    def record_session(
        session_id: str,
        spec_hash: str,
        complexity_score: float,
        ...
    ): ...

    # SQLite handles concurrent writes internally
```

### BudgetEnforcer
```python
class BudgetEnforcer:
    def check_available(cost: float) -> bool: ...
    def record_usage(cost: float): ...
    def get_status() -> BudgetStatus: ...
    # NEEDS LOCKING - mutable state
```

### AgentPool
```python
class AgentPool:
    def __init__(self, max_active: int, max_total: int): ...

    def acquire(agent_type: str) -> Agent: ...
    def release(agent: Agent): ...
    # HAS INTERNAL LOCKS - thread-safe
```

---

## Appendix B: Commands.py Diff

```diff
# src/shannon/cli/commands.py

- from shannon.orchestrator import ContextAwareOrchestrator
+ from shannon.unified_orchestrator import UnifiedOrchestrator

  @cli.command()
  def analyze(...):
-     orchestrator = ContextAwareOrchestrator(config)
+     orchestrator = UnifiedOrchestrator(config)
      result = await orchestrator.execute_analyze(...)

  @cli.command()
  def wave(...):
-     orchestrator = ContextAwareOrchestrator(config)
+     orchestrator = UnifiedOrchestrator(config)
      result = await orchestrator.execute_wave(...)

  # Repeat for all 9 commands that use orchestrator
  # Total: 9 lines changed (imports + initializations)
```

---

## Conclusion

The UnifiedOrchestrator design provides a clean, maintainable consolidation of V3 and V4 orchestrators through delegation rather than reimplementation. The facade pattern ensures minimal changes to commands.py while enabling efficient subsystem sharing and clear separation of concerns.

**Estimated Implementation Time**: 8-10 hours total
- Core implementation: 5-6 hours
- Testing: 2-3 hours
- Integration & validation: 1 hour

**Next Steps**:
1. Review and approve this design
2. Implement `UnifiedOrchestrator` class
3. Update `commands.py` imports
4. Run full test suite
5. Deploy to production

---

**Document Status**: ✅ DESIGN COMPLETE - READY FOR IMPLEMENTATION
