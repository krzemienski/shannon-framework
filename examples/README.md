# Shannon CLI V3.0 - Examples

Complete examples demonstrating all V3 features.

---

## Quick Start Examples

### Basic Usage

```python
# examples/quickstart.py
import asyncio
from shannon import ContextAwareOrchestrator

async def quick_analysis():
    """Quick start example - analyze specification"""

    # Initialize orchestrator with all V3 features
    orchestrator = ContextAwareOrchestrator.build_full_v3()

    # Execute analysis
    result = await orchestrator.execute_analyze(
        spec_file="spec.md",
        use_cache=True
    )

    print(f"Complexity: {result['complexity']}")
    print(f"Model: {result['model_selected']}")
    print(f"Cost: ${result['cost_estimate']}")
    print(f"Cache: {'HIT' if result['cache_hit'] else 'MISS'}")

if __name__ == "__main__":
    asyncio.run(quick_analysis())
```

### With Context

```python
# examples/context_example.py
import asyncio
from shannon.context import ContextManager
from shannon import ContextAwareOrchestrator

async def analyze_with_context():
    """Analyze with project context for complexity reduction"""

    # Initialize
    context = ContextManager()
    orchestrator = ContextAwareOrchestrator.build_full_v3()

    # Onboard project (one-time)
    await context.onboard(
        project_path="/path/to/project",
        project_id="my-app"
    )

    # Analyze with context
    result = await orchestrator.execute_analyze(
        spec_file="spec.md",
        project_id="my-app"
    )

    print(f"Complexity: {result['complexity']}")
    print(f"Context loaded: {result['context_loaded']}")
    print(f"Files indexed: {result.get('context_files_count', 0)}")

if __name__ == "__main__":
    asyncio.run(analyze_with_context())
```

---

## Feature Examples

### 1. Live Metrics Dashboard

See: [examples/metrics/demo_dashboard.py](metrics/demo_dashboard.py)

```python
from shannon.metrics import MetricsCollector, LiveDashboard

async def demo_live_metrics():
    collector = MetricsCollector()
    dashboard = LiveDashboard(collector, refresh_rate_hz=4)

    async for message in dashboard.run(sdk_stream):
        # Dashboard updates automatically
        # Press Enter to toggle compact/detailed
        # Press p to pause, q to quit
        process_message(message)
```

### 2. Intelligent Caching

See: [examples/cache_demo.py](cache_demo.py)

```python
from shannon.cache import CacheManager

async def demo_caching():
    cache = CacheManager()

    # First analysis - cache miss
    result1 = await orchestrator.execute_analyze("spec.md")
    print(f"First run: ${result1['cost_estimate']}, Cache: MISS")

    # Second analysis - cache hit
    result2 = await orchestrator.execute_analyze("spec.md")
    print(f"Second run: $0.00, Cache: HIT")
    print(f"Saved: ${result1['cost_estimate']}")

    # View statistics
    stats = cache.get_stats()
    print(f"Hit rate: {stats.hit_rate}%")
    print(f"Total savings: ${stats.total_savings_dollars}")
```

### 3. Context Management

See: [examples/context_demo.py](context_demo.py)

```python
from shannon.context import ContextManager

async def demo_context():
    context = ContextManager()

    # Onboard project
    result = await context.onboard(
        project_path="/path/to/project",
        project_id="my-app"
    )
    print(f"Files indexed: {result.files_indexed}")
    print(f"Framework: {result.framework}")

    # Prime context (fast reload)
    context_data = await context.prime(project_id="my-app")
    print(f"Files loaded: {context_data.files_count}")

    # Update context (after changes)
    update_result = await context.update(project_id="my-app")
    print(f"Files updated: {update_result.files_updated}")
```

### 4. MCP Management

See: [examples/mcp_demo.py](mcp_demo.py)

```python
from shannon.mcp import MCPManager

async def demo_mcp():
    manager = MCPManager()

    # Auto-detect required MCPs
    mcps = await manager.detect_required_mcps(
        spec_text="Build PostgreSQL API...",
        domain_breakdown={"Backend": 60, "Database": 40}
    )
    print(f"Recommended: {[mcp.name for mcp in mcps]}")

    # Install MCP
    result = await manager.install_mcp("postgres", verify=True)
    print(f"Installed: {result.success}")

    # Verify health
    health = await manager.verify_mcp("postgres", deep_check=True)
    print(f"Health: {health.status}")
```

### 5. Cost Optimization

See: [examples/cost_optimization_demo.py](cost_optimization_demo.py)

```python
from shannon.optimization import CostOptimizer, BudgetEnforcer

async def demo_cost_optimization():
    optimizer = CostOptimizer()

    # Smart model selection
    model = optimizer.select_model(complexity=0.25)
    print(f"Model: {model}")  # claude-haiku-4

    # Budget enforcement
    enforcer = BudgetEnforcer(max_tokens=100000)
    status = enforcer.check_budget(
        current_tokens=80000,
        estimated_tokens=25000
    )
    print(f"Budget status: {status}")
```

### 6. Analytics

See: [examples/analytics_demo.py](analytics_demo.py)

```python
from shannon.analytics import HistoricalAnalytics

async def demo_analytics():
    analytics = HistoricalAnalytics()

    # Cost summary
    summary = await analytics.get_cost_summary(days=30)
    print(f"Total cost: ${summary.total_cost}")
    print(f"Cache savings: ${summary.cache_savings}")

    # Trends
    trends = await analytics.get_trends("cost", days=30)
    for point in trends:
        print(f"{point.date}: ${point.value}")
```

### 7. Agent Control

See: [examples/agent_demo.py](agent_demo.py)

```python
from shannon.agents import AgentStateTracker, AgentController

async def demo_agent_control():
    tracker = AgentStateTracker()
    controller = AgentController()

    # Track agent
    tracker.track_spawn("BACKEND", wave_number=1)

    # Get state
    state = tracker.get_state("BACKEND")
    print(f"Agent: {state.name}, Status: {state.status}")

    # Pause agent
    await controller.pause_agent("BACKEND")

    # Resume agent
    await controller.resume_agent("BACKEND")
```

---

## Advanced Examples

### Complete Workflow

See: [examples/advanced_usage.py](advanced_usage.py)

Demonstrates complete V3 workflow:
- Context onboarding
- Analysis with caching
- Live metrics during waves
- Budget enforcement
- Agent control
- Analytics review

### Programmatic API

See: [examples/sdk_integration_demo.py](sdk_integration_demo.py)

Using Shannon CLI as a library in Python applications.

### CI/CD Integration

See: [examples/ci_cd_example.sh](ci_cd_example.sh)

Shell script for CI/CD pipelines.

---

## Running Examples

```bash
# Install dependencies
pip install shannon-cli

# Run quick start
python examples/quickstart.py

# Run specific example
python examples/context_demo.py

# Run all examples
bash examples/run_all.sh
```

---

## Example Projects

### 1. Authentication System

Spec: `examples/projects/auth-system/spec.md`

Demonstrates:
- Medium complexity (0.35)
- Backend + Database domains
- 2-wave execution
- Cost: ~$2.40

### 2. Full-Stack App

Spec: `examples/projects/fullstack-app/spec.md`

Demonstrates:
- High complexity (0.65)
- Multi-domain (Backend, Frontend, Database, DevOps)
- 4-wave execution
- Context usage for consistency
- Cost: ~$8.50

### 3. Simple API

Spec: `examples/projects/simple-api/spec.md`

Demonstrates:
- Low complexity (0.25)
- Haiku model selection (cost optimization)
- Single wave
- Cost: ~$0.30

---

## Tutorials

### Tutorial 1: Getting Started

Location: `examples/tutorials/01-getting-started.md`

Learn:
- Installation and setup
- First analysis
- First wave execution
- Session management

### Tutorial 2: Context Management

Location: `examples/tutorials/02-context-management.md`

Learn:
- Onboarding projects
- Context benefits
- Update strategies
- Best practices

### Tutorial 3: Cost Optimization

Location: `examples/tutorials/03-cost-optimization.md`

Learn:
- Caching strategies
- Model selection
- Budget enforcement
- Analytics review

### Tutorial 4: Advanced Features

Location: `examples/tutorials/04-advanced-features.md`

Learn:
- Agent control
- MCP integration
- Custom workflows
- Programmatic API

---

## Testing Examples

All examples include tests:

```bash
# Test examples
pytest examples/tests/

# Test specific example
pytest examples/tests/test_context_demo.py
```

---

## Documentation

For complete documentation, see:
- [User Guide](../docs/USER_GUIDE.md)
- [API Reference](../docs/API_REFERENCE.md)
- [Migration Guide](../docs/MIGRATION_V2_V3.md)

---

**Shannon CLI V3.0 Examples** - Learn by example.

*Last Updated: 2025-11-14*
