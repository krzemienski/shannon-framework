# Shannon CLI V3.0 - API Reference

**Version**: 3.0.0 | **Date**: 2025-11-14

> Complete API reference for programmatic usage of Shannon CLI V3.0

---

## Table of Contents

1. [Python API Overview](#python-api-overview)
2. [Core Modules](#core-modules)
3. [Context Module](#context-module)
4. [Cache Module](#cache-module)
5. [Metrics Module](#metrics-module)
6. [MCP Module](#mcp-module)
7. [Analytics Module](#analytics-module)
8. [Optimization Module](#optimization-module)
9. [Agents Module](#agents-module)
10. [SDK Integration](#sdk-integration)
11. [Type Hints](#type-hints)
12. [Examples](#examples)

---

## Python API Overview

Shannon CLI V3.0 can be used programmatically as a Python library.

### Installation

```bash
pip install shannon-cli
```

### Basic Usage

```python
import asyncio
from shannon import ContextManager, ContextAwareOrchestrator

async def main():
    # Initialize context manager
    context = ContextManager()

    # Onboard project
    await context.onboard("/path/to/project", project_id="my-app")

    # Create orchestrator
    orchestrator = ContextAwareOrchestrator.build_full_v3()

    # Execute analysis
    result = await orchestrator.execute_analyze(
        spec_file="spec.md",
        project_id="my-app"
    )

    print(f"Complexity: {result['complexity']}")
    print(f"Waves: {result['waves_recommended']}")

asyncio.run(main())
```

---

## Core Modules

### ContextAwareOrchestrator

Central integration hub coordinating all V3 features.

**Location**: `shannon.core.orchestrator`

#### Class: ContextAwareOrchestrator

```python
class ContextAwareOrchestrator:
    """Central orchestrator for Shannon CLI V3.0"""

    def __init__(
        self,
        context_manager: ContextManager,
        metrics_collector: MetricsCollector,
        cache_manager: CacheManager,
        mcp_manager: MCPManager,
        agent_tracker: AgentStateTracker,
        cost_optimizer: CostOptimizer,
        analytics: HistoricalAnalytics
    ):
        """
        Initialize orchestrator with all subsystems.

        Args:
            context_manager: Context management subsystem
            metrics_collector: Live metrics collection
            cache_manager: Multi-tier caching
            mcp_manager: MCP auto-installation
            agent_tracker: Agent state tracking
            cost_optimizer: Model selection and budgets
            analytics: Historical analytics database
        """
        pass
```

#### Method: execute_analyze

```python
async def execute_analyze(
    self,
    spec_file: str,
    project_id: Optional[str] = None,
    model: Optional[str] = None,
    use_cache: bool = True,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute complexity analysis with full V3 integration.

    Args:
        spec_file: Path to specification file
        project_id: Project ID for context loading (optional)
        model: Override model selection (optional)
        use_cache: Enable cache lookup (default: True)
        session_id: Specific session ID (optional)

    Returns:
        Dictionary containing:
            - complexity: Overall complexity score (0.0-1.0)
            - dimension_scores: Dict of 8D scores
            - domains: Domain breakdown percentages
            - waves_recommended: Number of waves
            - time_estimate_hours: Estimated time
            - cost_estimate: Estimated cost in dollars
            - model_selected: Model used
            - cache_hit: Whether cache was used
            - context_loaded: Whether context was loaded
            - mcps_installed: List of auto-installed MCPs

    Raises:
        FileNotFoundError: If spec_file doesn't exist
        ValueError: If project_id invalid
        BudgetExceededError: If estimated cost exceeds budget

    Example:
        >>> result = await orchestrator.execute_analyze(
        ...     spec_file="spec.md",
        ...     project_id="my-app"
        ... )
        >>> print(result['complexity'])
        0.35
        >>> print(result['cache_hit'])
        True
    """
    pass
```

#### Method: execute_wave

```python
async def execute_wave(
    self,
    request: str,
    session_id: Optional[str] = None,
    project_id: Optional[str] = None,
    show_metrics: bool = True,
    auto_mode: bool = False
) -> Dict[str, Any]:
    """
    Execute wave-based implementation with live monitoring.

    Args:
        request: Implementation request
        session_id: Session to continue (optional)
        project_id: Project ID for context (optional)
        show_metrics: Display live dashboard (default: True)
        auto_mode: Non-interactive mode (default: False)

    Returns:
        Dictionary containing:
            - session_id: Session identifier
            - waves_completed: Number of waves executed
            - total_tokens: Total tokens used
            - total_cost: Total cost in dollars
            - agents_spawned: List of agents spawned
            - status: Execution status

    Raises:
        SessionNotFoundError: If session_id doesn't exist
        BudgetExceededError: If budget limit reached
        AgentError: If agent execution fails

    Example:
        >>> result = await orchestrator.execute_wave(
        ...     request="Build authentication",
        ...     project_id="my-app",
        ...     show_metrics=True
        ... )
        >>> print(result['waves_completed'])
        2
        >>> print(result['total_cost'])
        2.45
    """
    pass
```

#### Factory Method: build_full_v3

```python
@classmethod
def build_full_v3(cls) -> "ContextAwareOrchestrator":
    """
    Build orchestrator with all V3 features enabled.

    Returns:
        Fully configured orchestrator instance

    Example:
        >>> orchestrator = ContextAwareOrchestrator.build_full_v3()
        >>> result = await orchestrator.execute_analyze("spec.md")
    """
    pass
```

---

## Context Module

Manages project context with 3-tier architecture (Hot/Warm/Cold).

**Location**: `shannon.context`

### ContextManager

```python
class ContextManager:
    """Manages project context across 3 tiers"""

    def __init__(
        self,
        hot_cache_size: int = 1000,
        warm_cache_dir: str = "~/.shannon/context",
        cold_storage: Optional[SerenaAdapter] = None
    ):
        """
        Initialize context manager.

        Args:
            hot_cache_size: In-memory cache size
            warm_cache_dir: Local cache directory
            cold_storage: Serena MCP adapter (optional)
        """
        pass
```

#### Method: onboard

```python
async def onboard(
    self,
    project_path: str,
    project_id: str,
    exclude_patterns: List[str] = None,
    max_files: int = 1000
) -> OnboardResult:
    """
    Onboard project into context system.

    Args:
        project_path: Path to project directory
        project_id: Unique project identifier
        exclude_patterns: Patterns to exclude (e.g., ["*.log", "node_modules"])
        max_files: Maximum files to index

    Returns:
        OnboardResult containing:
            - files_indexed: Number of files indexed
            - total_size_bytes: Total size
            - languages: Detected languages
            - framework: Detected framework
            - dependencies: List of dependencies
            - architecture: Detected patterns

    Example:
        >>> result = await context.onboard(
        ...     project_path="/path/to/project",
        ...     project_id="my-app"
        ... )
        >>> print(result.files_indexed)
        142
        >>> print(result.framework)
        'Next.js 14'
    """
    pass
```

#### Method: prime

```python
async def prime(
    self,
    project_id: str,
    load_content: bool = True,
    structure_only: bool = False
) -> ContextData:
    """
    Load context for fast session initialization.

    Args:
        project_id: Project identifier
        load_content: Load file contents (default: True)
        structure_only: Load structure only, faster (default: False)

    Returns:
        ContextData containing loaded context

    Example:
        >>> context_data = await context.prime(
        ...     project_id="my-app",
        ...     structure_only=True  # Fast load
        ... )
        >>> print(context_data.files_count)
        142
    """
    pass
```

#### Method: update

```python
async def update(
    self,
    project_id: str,
    force: bool = False,
    git_diff_since: Optional[str] = None
) -> UpdateResult:
    """
    Update project context incrementally.

    Args:
        project_id: Project identifier
        force: Force full reindex (default: False)
        git_diff_since: Git reference for diff (optional)

    Returns:
        UpdateResult containing:
            - files_updated: Number of files updated
            - files_added: New files
            - files_removed: Deleted files
            - dependencies_changed: Whether deps updated

    Example:
        >>> result = await context.update(
        ...     project_id="my-app",
        ...     git_diff_since="HEAD~5"
        ... )
        >>> print(result.files_updated)
        12
    """
    pass
```

#### Method: load_for_task

```python
async def load_for_task(
    self,
    task: str,
    project_id: str
) -> ContextData:
    """
    Load context optimized for specific task.

    Smart loading based on task type:
    - Backend task → Load API, database, business logic
    - Frontend task → Load components, styles, routing
    - Testing task → Load tests, test utilities

    Args:
        task: Task description
        project_id: Project identifier

    Returns:
        Task-optimized context data

    Example:
        >>> context_data = await context.load_for_task(
        ...     task="Add authentication endpoints",
        ...     project_id="my-app"
        ... )
        >>> # Loads: API files, auth logic, database schema
    """
    pass
```

### ContextLoader

```python
class ContextLoader:
    """Loads context from various sources"""

    async def load_from_serena(
        self,
        project_id: str,
        query: str
    ) -> List[ContextFile]:
        """
        Load context from Serena MCP (cold storage).

        Args:
            project_id: Project identifier
            query: Search query

        Returns:
            List of matching context files

        Example:
            >>> files = await loader.load_from_serena(
            ...     project_id="my-app",
            ...     query="authentication"
            ... )
        """
        pass
```

### ContextUpdater

```python
class ContextUpdater:
    """Updates context incrementally"""

    async def detect_changes(
        self,
        project_path: str,
        last_update: datetime
    ) -> ChangeSet:
        """
        Detect changes since last update.

        Args:
            project_path: Project directory
            last_update: Last update timestamp

        Returns:
            ChangeSet with added/modified/deleted files
        """
        pass
```

### Onboarder

```python
class Onboarder:
    """Handles project onboarding"""

    async def detect_framework(
        self,
        project_path: str
    ) -> FrameworkInfo:
        """
        Detect project framework.

        Returns:
            FrameworkInfo with name, version, language
        """
        pass

    async def analyze_dependencies(
        self,
        project_path: str
    ) -> List[Dependency]:
        """
        Analyze project dependencies.

        Returns:
            List of dependencies with versions
        """
        pass
```

---

## Cache Module

3-tier caching system for cost optimization.

**Location**: `shannon.cache`

### CacheManager

```python
class CacheManager:
    """Manages 3-tier caching system"""

    def __init__(
        self,
        cache_dir: str = "~/.shannon/cache",
        max_size_mb: int = 500,
        enable_lru: bool = True
    ):
        """
        Initialize cache manager.

        Args:
            cache_dir: Cache directory
            max_size_mb: Maximum cache size in MB
            enable_lru: Enable LRU eviction
        """
        pass
```

#### Method: get_analysis

```python
async def get_analysis(
    self,
    spec_text: str,
    framework_version: str,
    model: str,
    context_hash: Optional[str] = None
) -> Optional[AnalysisResult]:
    """
    Get cached analysis result.

    Args:
        spec_text: Specification text
        framework_version: Shannon Framework version
        model: Model used
        context_hash: Context hash (optional)

    Returns:
        Cached result or None if cache miss

    Example:
        >>> result = await cache.get_analysis(
        ...     spec_text="Build API...",
        ...     framework_version="2.1.0",
        ...     model="claude-sonnet-4"
        ... )
        >>> if result:
        ...     print("Cache HIT!")
    """
    pass
```

#### Method: save_analysis

```python
async def save_analysis(
    self,
    spec_text: str,
    framework_version: str,
    model: str,
    result: AnalysisResult,
    context_hash: Optional[str] = None,
    ttl_days: int = 7
) -> None:
    """
    Save analysis result to cache.

    Args:
        spec_text: Specification text
        framework_version: Shannon Framework version
        model: Model used
        result: Analysis result to cache
        context_hash: Context hash (optional)
        ttl_days: Time-to-live in days

    Example:
        >>> await cache.save_analysis(
        ...     spec_text="Build API...",
        ...     framework_version="2.1.0",
        ...     model="claude-sonnet-4",
        ...     result=analysis_result,
        ...     ttl_days=7
        ... )
    """
    pass
```

#### Method: get_stats

```python
def get_stats(self) -> CacheStats:
    """
    Get cache statistics.

    Returns:
        CacheStats containing:
            - total_hits: Total cache hits
            - total_misses: Total cache misses
            - hit_rate: Hit rate percentage
            - total_savings_dollars: Cost savings
            - size_mb: Current size in MB
            - entry_count: Number of entries

    Example:
        >>> stats = cache.get_stats()
        >>> print(f"Hit rate: {stats.hit_rate}%")
        >>> print(f"Savings: ${stats.total_savings_dollars}")
    """
    pass
```

### AnalysisCache

```python
class AnalysisCache:
    """Tier 1: Analysis result caching"""

    def compute_cache_key(
        self,
        spec_text: str,
        framework_version: str,
        model: str,
        context_hash: Optional[str] = None
    ) -> str:
        """
        Compute context-aware cache key.

        Returns:
            SHA-256 hash of key components
        """
        pass
```

### CommandCache

```python
class CommandCache:
    """Tier 2: Stable command caching"""

    async def get_command_result(
        self,
        command_name: str,
        framework_version: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached command result.

        Args:
            command_name: Command name (e.g., "prime", "discover-skills")
            framework_version: Framework version

        Returns:
            Cached result or None
        """
        pass
```

### MCPCache

```python
class MCPCache:
    """Tier 3: MCP recommendation caching"""

    def get_mcp_recommendations(
        self,
        domain_signature: str
    ) -> Optional[List[MCPRecommendation]]:
        """
        Get cached MCP recommendations.

        Args:
            domain_signature: Domain fingerprint

        Returns:
            List of recommended MCPs or None
        """
        pass
```

---

## Metrics Module

Live metrics collection and dashboard.

**Location**: `shannon.metrics`

### MetricsCollector

```python
class MetricsCollector:
    """Collects real-time metrics from SDK execution"""

    def __init__(self):
        self.tokens_input = 0
        self.tokens_output = 0
        self.total_cost = 0.0
        self.start_time = None
        self.streaming_buffer = []
```

#### Method: update_from_message

```python
def update_from_message(self, message: Any) -> None:
    """
    Update metrics from SDK message.

    Args:
        message: SDK message (TextBlock or ResultMessage)

    Example:
        >>> async for msg in sdk_stream:
        ...     collector.update_from_message(msg)
        ...     yield msg
    """
    pass
```

#### Method: get_snapshot

```python
def get_snapshot(self) -> MetricsSnapshot:
    """
    Get current metrics snapshot.

    Returns:
        MetricsSnapshot containing:
            - tokens_input: Input tokens
            - tokens_output: Output tokens
            - total_cost: Cost in dollars
            - elapsed_time_seconds: Time elapsed
            - eta_seconds: Estimated time remaining
            - recent_output: Last 20 lines

    Example:
        >>> snapshot = collector.get_snapshot()
        >>> print(f"Cost: ${snapshot.total_cost}")
    """
    pass
```

### LiveDashboard

```python
class LiveDashboard:
    """Live metrics dashboard with 4 Hz refresh"""

    def __init__(
        self,
        collector: MetricsCollector,
        refresh_rate_hz: int = 4
    ):
        """
        Initialize dashboard.

        Args:
            collector: Metrics collector
            refresh_rate_hz: Refresh rate (default: 4 Hz)
        """
        pass
```

#### Method: run

```python
async def run(
    self,
    sdk_stream: AsyncIterator[Any]
) -> AsyncIterator[Any]:
    """
    Run dashboard with live updates.

    Args:
        sdk_stream: SDK message stream

    Yields:
        SDK messages (passed through)

    Example:
        >>> dashboard = LiveDashboard(collector)
        >>> async for msg in dashboard.run(sdk_stream):
        ...     # Dashboard updates in background
        ...     process_message(msg)
    """
    pass
```

### KeyboardHandler

```python
class KeyboardHandler:
    """Non-blocking keyboard input handler"""

    def poll(self) -> Optional[str]:
        """
        Poll for keyboard input (non-blocking).

        Returns:
            Key pressed or None

        Example:
            >>> handler = KeyboardHandler()
            >>> key = handler.poll()
            >>> if key == 'p':
            ...     pause_execution()
        """
        pass
```

---

## MCP Module

MCP detection, installation, and verification.

**Location**: `shannon.mcp`

### MCPManager

```python
class MCPManager:
    """Manages MCP lifecycle"""

    async def detect_required_mcps(
        self,
        spec_text: str,
        domain_breakdown: Dict[str, int]
    ) -> List[MCPRecommendation]:
        """
        Detect required MCPs from specification.

        Args:
            spec_text: Specification text
            domain_breakdown: Domain percentages

        Returns:
            List of recommended MCPs

        Example:
            >>> mcps = await manager.detect_required_mcps(
            ...     spec_text="Build PostgreSQL API...",
            ...     domain_breakdown={"Backend": 60, "Database": 40}
            ... )
            >>> # Returns: [postgres, filesystem, git]
        """
        pass
```

#### Method: install_mcp

```python
async def install_mcp(
    self,
    mcp_name: str,
    verify: bool = True
) -> InstallResult:
    """
    Install MCP server.

    Args:
        mcp_name: MCP name (e.g., "serena", "postgres")
        verify: Verify after installation

    Returns:
        InstallResult with status

    Example:
        >>> result = await manager.install_mcp("serena", verify=True)
        >>> if result.success:
        ...     print("Installed successfully")
    """
    pass
```

#### Method: verify_mcp

```python
async def verify_mcp(
    self,
    mcp_name: str,
    deep_check: bool = False
) -> VerifyResult:
    """
    Verify MCP is working.

    Args:
        mcp_name: MCP name
        deep_check: Perform deep health check

    Returns:
        VerifyResult with health status

    Example:
        >>> result = await manager.verify_mcp("serena", deep_check=True)
        >>> print(result.status)  # "healthy" or "unhealthy"
    """
    pass
```

### MCPDetector

```python
class MCPDetector:
    """Detects required MCPs from specifications"""

    def detect_from_domains(
        self,
        domain_breakdown: Dict[str, int]
    ) -> List[str]:
        """
        Detect MCPs from domain breakdown.

        Args:
            domain_breakdown: Domain percentages

        Returns:
            List of MCP names

        Example:
            >>> mcps = detector.detect_from_domains({
            ...     "Backend": 50,
            ...     "Frontend": 30,
            ...     "Database": 20
            ... })
            >>> # Returns: ["filesystem", "postgres", "git"]
        """
        pass
```

### MCPInstaller

```python
class MCPInstaller:
    """Installs MCP servers"""

    async def install(
        self,
        mcp_name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Install MCP server.

        Args:
            mcp_name: MCP name
            config: Optional configuration

        Returns:
            True if successful
        """
        pass
```

### MCPVerifier

```python
class MCPVerifier:
    """Verifies MCP health"""

    async def verify_health(
        self,
        mcp_name: str
    ) -> HealthStatus:
        """
        Check MCP health.

        Returns:
            HealthStatus enum (HEALTHY, UNHEALTHY, UNKNOWN)
        """
        pass
```

---

## Analytics Module

Historical analytics with SQLite database.

**Location**: `shannon.analytics`

### HistoricalAnalytics

```python
class HistoricalAnalytics:
    """Analytics database manager"""

    def __init__(
        self,
        db_path: str = "~/.shannon/analytics.db"
    ):
        """
        Initialize analytics database.

        Args:
            db_path: Database file path
        """
        pass
```

#### Method: record_session

```python
async def record_session(
    self,
    session_id: str,
    project_id: Optional[str],
    complexity: float,
    waves_planned: int,
    waves_completed: int,
    total_tokens: int,
    total_cost: float,
    cache_hits: int,
    cache_misses: int,
    status: str
) -> None:
    """
    Record session to database.

    Args:
        session_id: Session identifier
        project_id: Project ID (optional)
        complexity: Complexity score
        waves_planned: Planned waves
        waves_completed: Completed waves
        total_tokens: Total tokens used
        total_cost: Total cost
        cache_hits: Cache hits
        cache_misses: Cache misses
        status: Session status

    Example:
        >>> await analytics.record_session(
        ...     session_id="abc123",
        ...     project_id="my-app",
        ...     complexity=0.35,
        ...     waves_planned=2,
        ...     waves_completed=2,
        ...     total_tokens=45200,
        ...     total_cost=2.25,
        ...     cache_hits=3,
        ...     cache_misses=2,
        ...     status="complete"
        ... )
    """
    pass
```

#### Method: get_cost_summary

```python
async def get_cost_summary(
    self,
    days: int = 30,
    project_id: Optional[str] = None
) -> CostSummary:
    """
    Get cost summary for time period.

    Args:
        days: Number of days to analyze
        project_id: Filter by project (optional)

    Returns:
        CostSummary containing:
            - total_cost: Total cost
            - avg_per_session: Average cost
            - cache_savings: Savings from cache
            - by_model: Breakdown by model
            - by_project: Breakdown by project

    Example:
        >>> summary = await analytics.get_cost_summary(days=30)
        >>> print(f"Total: ${summary.total_cost}")
        >>> print(f"Savings: ${summary.cache_savings}")
    """
    pass
```

#### Method: get_trends

```python
async def get_trends(
    self,
    metric: str,
    days: int = 30
) -> List[TrendPoint]:
    """
    Get trend data for metric.

    Args:
        metric: Metric name ("cost", "tokens", "sessions")
        days: Number of days

    Returns:
        List of trend points with date and value

    Example:
        >>> trends = await analytics.get_trends("cost", days=30)
        >>> for point in trends:
        ...     print(f"{point.date}: ${point.value}")
    """
    pass
```

### InsightsGenerator

```python
class InsightsGenerator:
    """Generates insights from analytics data"""

    async def generate_insights(
        self,
        analytics: HistoricalAnalytics
    ) -> List[Insight]:
        """
        Generate insights from data.

        Returns:
            List of insights with:
                - type: Insight type
                - message: Description
                - recommendation: Action recommendation

        Example:
            >>> insights = await generator.generate_insights(analytics)
            >>> for insight in insights:
            ...     print(insight.message)
            ...     print(insight.recommendation)
        """
        pass
```

---

## Optimization Module

Cost optimization and model selection.

**Location**: `shannon.optimization`

### CostOptimizer

```python
class CostOptimizer:
    """Optimizes costs through model selection"""

    def select_model(
        self,
        complexity: float,
        budget_remaining: Optional[int] = None
    ) -> str:
        """
        Select optimal model for complexity.

        Args:
            complexity: Complexity score (0.0-1.0)
            budget_remaining: Remaining budget in tokens

        Returns:
            Model name

        Example:
            >>> model = optimizer.select_model(complexity=0.25)
            >>> print(model)
            'claude-haiku-4'
        """
        pass
```

### BudgetEnforcer

```python
class BudgetEnforcer:
    """Enforces token budgets"""

    def __init__(
        self,
        max_tokens: int,
        warn_threshold: float = 0.80,
        pause_threshold: float = 0.95
    ):
        """
        Initialize budget enforcer.

        Args:
            max_tokens: Maximum token budget
            warn_threshold: Warning threshold (0.0-1.0)
            pause_threshold: Pause threshold (0.0-1.0)
        """
        pass
```

#### Method: check_budget

```python
def check_budget(
    self,
    current_tokens: int,
    estimated_tokens: int
) -> BudgetStatus:
    """
    Check budget status.

    Args:
        current_tokens: Current usage
        estimated_tokens: Estimated additional usage

    Returns:
        BudgetStatus enum (OK, WARNING, EXCEEDED)

    Example:
        >>> status = enforcer.check_budget(
        ...     current_tokens=80000,
        ...     estimated_tokens=15000
        ... )
        >>> if status == BudgetStatus.WARNING:
        ...     print("Approaching budget limit!")
    """
    pass
```

### CostEstimator

```python
class CostEstimator:
    """Estimates costs for operations"""

    def estimate_analysis_cost(
        self,
        spec_length: int,
        model: str
    ) -> float:
        """
        Estimate analysis cost.

        Args:
            spec_length: Specification length in characters
            model: Model to use

        Returns:
            Estimated cost in dollars

        Example:
            >>> cost = estimator.estimate_analysis_cost(
            ...     spec_length=5000,
            ...     model="claude-sonnet-4"
            ... )
            >>> print(f"Estimated: ${cost}")
        """
        pass
```

### ModelSelector

```python
class ModelSelector:
    """Selects optimal model"""

    MODEL_COSTS = {
        "claude-haiku-4": 0.25,   # per 1M tokens
        "claude-sonnet-4": 3.00,
        "claude-opus-4": 15.00
    }

    def select_by_complexity(
        self,
        complexity: float
    ) -> str:
        """
        Select model based on complexity.

        Thresholds:
        - <0.30: Haiku
        - 0.30-0.60: Sonnet
        - >0.60: Opus
        """
        pass
```

---

## Agents Module

Agent state tracking and control.

**Location**: `shannon.agents`

### AgentStateTracker

```python
class AgentStateTracker:
    """Tracks agent lifecycle and states"""

    def __init__(self):
        self.agents: Dict[str, AgentState] = {}
```

#### Method: track_spawn

```python
def track_spawn(
    self,
    agent_name: str,
    wave_number: int
) -> None:
    """
    Track agent spawn.

    Args:
        agent_name: Agent name (e.g., "BACKEND", "FRONTEND")
        wave_number: Wave number

    Example:
        >>> tracker.track_spawn("BACKEND", wave_number=1)
    """
    pass
```

#### Method: get_state

```python
def get_state(
    self,
    agent_name: str
) -> AgentState:
    """
    Get agent state.

    Returns:
        AgentState containing:
            - name: Agent name
            - status: Status enum (ACTIVE, PAUSED, COMPLETE, ERROR)
            - wave_number: Current wave
            - tokens_used: Tokens consumed
            - cost: Cost incurred
            - start_time: Start timestamp

    Example:
        >>> state = tracker.get_state("BACKEND")
        >>> print(state.status)
        >>> print(state.tokens_used)
    """
    pass
```

### AgentController

```python
class AgentController:
    """Controls agent execution"""

    async def pause_agent(
        self,
        agent_name: str
    ) -> bool:
        """
        Pause agent execution.

        Args:
            agent_name: Agent to pause

        Returns:
            True if successfully paused
        """
        pass

    async def resume_agent(
        self,
        agent_name: str
    ) -> bool:
        """
        Resume agent execution.

        Args:
            agent_name: Agent to resume

        Returns:
            True if successfully resumed
        """
        pass
```

### MessageRouter

```python
class MessageRouter:
    """Routes messages between agents"""

    def route_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str
    ) -> None:
        """
        Route message between agents.

        Args:
            from_agent: Source agent
            to_agent: Destination agent
            message: Message content
        """
        pass
```

---

## SDK Integration

Integration with Claude Agent SDK.

**Location**: `shannon.sdk`

### StreamHandler

```python
class StreamHandler:
    """Handles SDK streaming responses"""

    async def handle_stream(
        self,
        stream: AsyncIterator[Any],
        collectors: List[Callable]
    ) -> AsyncIterator[Any]:
        """
        Handle stream with collectors.

        Args:
            stream: SDK stream
            collectors: List of collector functions

        Yields:
            Stream messages

        Example:
            >>> async for msg in handler.handle_stream(
            ...     stream=sdk_stream,
            ...     collectors=[metrics.collect, analytics.collect]
            ... ):
            ...     process_message(msg)
        """
        pass
```

### MessageInterceptor

```python
class MessageInterceptor:
    """Intercepts and parses SDK messages"""

    def parse_complexity_score(
        self,
        messages: List[Any]
    ) -> Optional[float]:
        """
        Parse complexity score from messages.

        Handles formats:
        - "= 0.443 ≈ 0.44"
        - "Complexity: 0.44"

        Returns:
            Complexity score or None
        """
        pass

    def parse_dimension_scores(
        self,
        messages: List[Any]
    ) -> Dict[str, float]:
        """
        Parse 8D dimension scores.

        Returns:
            Dictionary mapping dimension to score
        """
        pass
```

---

## Type Hints

### Data Classes

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

@dataclass
class AnalysisResult:
    """Analysis result data"""
    complexity: float
    dimension_scores: Dict[str, float]
    domains: Dict[str, int]
    waves_recommended: int
    time_estimate_hours: float
    cost_estimate: float
    model_selected: str
    cache_hit: bool
    context_loaded: bool
    mcps_installed: List[str]

@dataclass
class OnboardResult:
    """Onboarding result data"""
    files_indexed: int
    total_size_bytes: int
    languages: Dict[str, int]
    framework: str
    dependencies: List[str]
    architecture: str

@dataclass
class ContextData:
    """Context data"""
    project_id: str
    files_count: int
    files: List[str]
    structure: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class CacheStats:
    """Cache statistics"""
    total_hits: int
    total_misses: int
    hit_rate: float
    total_savings_dollars: float
    size_mb: float
    entry_count: int

@dataclass
class MetricsSnapshot:
    """Metrics snapshot"""
    tokens_input: int
    tokens_output: int
    total_cost: float
    elapsed_time_seconds: float
    eta_seconds: Optional[float]
    recent_output: List[str]

@dataclass
class AgentState:
    """Agent state"""
    name: str
    status: "AgentStatus"
    wave_number: int
    tokens_used: int
    cost: float
    start_time: datetime

class AgentStatus(Enum):
    """Agent status enum"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    ERROR = "error"

class BudgetStatus(Enum):
    """Budget status enum"""
    OK = "ok"
    WARNING = "warning"
    EXCEEDED = "exceeded"

class HealthStatus(Enum):
    """Health status enum"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
```

---

## Examples

### Example 1: Complete Analysis Workflow

```python
import asyncio
from shannon import (
    ContextAwareOrchestrator,
    ContextManager,
    CacheManager,
    MetricsCollector
)

async def analyze_with_context():
    # Initialize
    orchestrator = ContextAwareOrchestrator.build_full_v3()
    context = ContextManager()

    # Onboard project (one-time)
    await context.onboard(
        project_path="/path/to/project",
        project_id="my-app"
    )

    # Analyze with context
    result = await orchestrator.execute_analyze(
        spec_file="spec.md",
        project_id="my-app",
        use_cache=True
    )

    print(f"Complexity: {result['complexity']}")
    print(f"Model: {result['model_selected']}")
    print(f"Cache: {'HIT' if result['cache_hit'] else 'MISS'}")
    print(f"Context: {'Loaded' if result['context_loaded'] else 'No context'}")
    print(f"Estimated cost: ${result['cost_estimate']}")

    # Execute waves
    wave_result = await orchestrator.execute_wave(
        request="Implement features from spec",
        project_id="my-app",
        show_metrics=True
    )

    print(f"Waves completed: {wave_result['waves_completed']}")
    print(f"Total cost: ${wave_result['total_cost']}")

asyncio.run(analyze_with_context())
```

### Example 2: Cache Management

```python
from shannon.cache import CacheManager

# Initialize cache
cache = CacheManager(
    cache_dir="~/.shannon/cache",
    max_size_mb=500
)

# Check for cached analysis
cached_result = await cache.get_analysis(
    spec_text=open("spec.md").read(),
    framework_version="2.1.0",
    model="claude-sonnet-4",
    context_hash="abc123def"
)

if cached_result:
    print("Cache HIT!")
    print(f"Complexity: {cached_result.complexity}")
else:
    print("Cache MISS - running analysis")
    # ... run analysis ...
    # Save to cache
    await cache.save_analysis(
        spec_text=spec_text,
        framework_version="2.1.0",
        model="claude-sonnet-4",
        result=analysis_result,
        ttl_days=7
    )

# View statistics
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate}%")
print(f"Savings: ${stats.total_savings_dollars}")
```

### Example 3: Live Metrics

```python
from shannon.metrics import MetricsCollector, LiveDashboard

# Initialize
collector = MetricsCollector()
dashboard = LiveDashboard(collector, refresh_rate_hz=4)

# Run with live dashboard
async for message in dashboard.run(sdk_stream):
    # Dashboard updates automatically in background
    # Process messages as normal
    process_message(message)

# Get final metrics
snapshot = collector.get_snapshot()
print(f"Total tokens: {snapshot.tokens_input + snapshot.tokens_output}")
print(f"Total cost: ${snapshot.total_cost}")
```

### Example 4: Budget Enforcement

```python
from shannon.optimization import BudgetEnforcer, CostEstimator

# Set budget
enforcer = BudgetEnforcer(
    max_tokens=100000,
    warn_threshold=0.80,
    pause_threshold=0.95
)

# Estimate cost
estimator = CostEstimator()
estimated_tokens = estimator.estimate_tokens(
    spec_file="spec.md",
    model="claude-sonnet-4"
)

# Check budget
status = enforcer.check_budget(
    current_tokens=50000,
    estimated_tokens=estimated_tokens
)

if status == BudgetStatus.WARNING:
    print("⚠️ Approaching budget limit!")
elif status == BudgetStatus.EXCEEDED:
    print("❌ Budget exceeded!")
    raise BudgetExceededError()
else:
    print("✓ Budget OK")
    # Proceed with execution
```

### Example 5: Agent Tracking

```python
from shannon.agents import AgentStateTracker, AgentController

# Initialize
tracker = AgentStateTracker()
controller = AgentController()

# Track agent spawn
tracker.track_spawn("BACKEND", wave_number=1)

# Check state
state = tracker.get_state("BACKEND")
print(f"Agent: {state.name}")
print(f"Status: {state.status}")
print(f"Tokens: {state.tokens_used}")
print(f"Cost: ${state.cost}")

# Pause if needed
if state.tokens_used > 50000:
    await controller.pause_agent("BACKEND")
    print("Agent paused due to high token usage")
```

### Example 6: Analytics Queries

```python
from shannon.analytics import HistoricalAnalytics

# Initialize
analytics = HistoricalAnalytics()

# Get cost summary
summary = await analytics.get_cost_summary(
    days=30,
    project_id="my-app"
)

print(f"Total cost: ${summary.total_cost}")
print(f"Avg per session: ${summary.avg_per_session}")
print(f"Cache savings: ${summary.cache_savings}")

# Get trends
trends = await analytics.get_trends("cost", days=30)
for point in trends:
    print(f"{point.date}: ${point.value}")

# Custom query
results = await analytics.query("""
    SELECT project_id, AVG(complexity) as avg_complexity
    FROM sessions
    WHERE created_at > date('now', '-30 days')
    GROUP BY project_id
    ORDER BY avg_complexity DESC
""")

for row in results:
    print(f"{row['project_id']}: {row['avg_complexity']}")
```

---

## Error Handling

### Custom Exceptions

```python
class ShannonError(Exception):
    """Base exception for Shannon CLI"""
    pass

class BudgetExceededError(ShannonError):
    """Raised when budget limit exceeded"""
    pass

class ContextNotFoundError(ShannonError):
    """Raised when context not found"""
    pass

class CacheMissError(ShannonError):
    """Raised when cache lookup fails"""
    pass

class MCPInstallError(ShannonError):
    """Raised when MCP installation fails"""
    pass

class AgentError(ShannonError):
    """Raised when agent execution fails"""
    pass
```

### Error Handling Example

```python
from shannon import ContextAwareOrchestrator, BudgetExceededError

try:
    orchestrator = ContextAwareOrchestrator.build_full_v3()
    result = await orchestrator.execute_analyze(
        spec_file="spec.md",
        project_id="my-app"
    )
except BudgetExceededError as e:
    print(f"Budget exceeded: {e}")
    # Increase budget or use cheaper model
except ContextNotFoundError as e:
    print(f"Context not found: {e}")
    # Onboard project first
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle generic error
```

---

## Configuration

### Programmatic Configuration

```python
from shannon import Config

# Load configuration
config = Config.load()

# Modify settings
config.cache.enabled = True
config.cache.max_size_mb = 500
config.metrics.enabled = True
config.budget.max_tokens = 100000

# Save configuration
config.save()

# Access settings
print(config.cache.enabled)
print(config.budget.max_tokens)
```

---

**Shannon CLI V3.0 API Reference** - Complete programmatic access to all features.

*Last Updated: 2025-11-14*
