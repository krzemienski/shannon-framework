# Shannon CLI V3.0 - Full Implementation Design

**Date**: 2025-11-13
**Scope**: Complete V3.0 implementation (all 8 features)
**Timeline**: 11 weeks
**Lines**: ~5,700 new + 6,469 existing = 12,169 total
**Status**: Design validated, ready for implementation

---

## Executive Summary

Shannon CLI V3.0 transforms the V2 thin wrapper into a production-grade development platform with real-time monitoring, intelligent caching, cost optimization, agent control, historical analytics, and context management for existing codebases.

**Key Achievement**: "10x more capable than Shannon Framework alone" through programmatic SDK control.

**Architecture**: Unified integration via ContextAwareOrchestrator pattern - all features work together, not in isolation.

---

## Design Decisions

### Decision 1: ContextAwareOrchestrator Pattern

**Problem**: V3 spec describes 8 features that must integrate seamlessly.

**Solution**: Central orchestrator that coordinates all features for every command.

**Pattern**:
```python
class ContextAwareOrchestrator:
    def __init__(
        self,
        context: ContextManager,
        metrics: MetricsCollector,
        cache: CacheManager,
        mcp: MCPManager,
        agents: AgentStateTracker,
        cost: CostOptimizer,
        analytics: HistoricalAnalytics
    ):
        # Dependency injection for testability
        self.context = context
        self.metrics = metrics
        self.cache = cache
        self.mcp = mcp
        self.agents = agents
        self.cost = cost
        self.analytics = analytics
```

**Why This Matters**:
- Every command (analyze, wave, task) flows through Orchestrator
- Adding new feature = plug into Orchestrator, all commands benefit automatically
- No feature fragmentation
- Single source of truth for execution flow

**Alternative Considered**: Individual feature flags per command (rejected - fragmentation risk)

---

### Decision 2: MessageInterceptor for Unified Parsing

**Problem**: V2 MessageParser bug + V3 Metrics + V3 Agent Control all need to parse SDK messages.

**Solution**: Single robust MessageInterceptor used by all features.

**Design**:
```python
class MessageInterceptor:
    """Unified SDK message parsing for all V3 features"""

    def parse_complexity_score(self, messages: List) -> float:
        """Handles multiple formats:
        - '= 0.443 ≈ 0.44' (actual Shannon Framework format)
        - 'Complexity: 0.44' (alternative format)
        """
        # Robust regex with fallback patterns

    def parse_dimension_scores(self, messages: List) -> Dict[str, float]:
        """Extract from markdown tables"""

    def parse_domains(self, messages: List) -> Dict[str, int]:
        """Extract domain percentages"""

    def extract_streaming_output(self, msg: TextBlock) -> str:
        """For live dashboard display"""

    def extract_cost_metrics(self, msg: ResultMessage) -> CostMetrics:
        """For real-time cost tracking"""
```

**Benefits**:
- Fixes V2 bug
- Enables V3 Metrics
- Enables V3 Agent Control
- Single parsing logic (no duplication)

---

### Decision 3: Three-Tier Caching Strategy

**Design** (from spec):

**Tier 1: Analysis Cache**
- Key: SHA-256(spec_text + framework_version + model + context_hash)
- Location: `~/.shannon/cache/analyses/{hash}.json`
- TTL: 7 days
- Purpose: Cache expensive analyses

**Tier 2: Command Cache**
- Key: `{command_name}_{framework_version}`
- Location: `~/.shannon/cache/commands/{key}.json`
- TTL: 30 days
- Purpose: Cache stable commands (prime, discover-skills)

**Tier 3: MCP Recommendation Cache**
- Key: Domain signature (e.g., "F40B35D25")
- Location: `~/.shannon/cache/mcps/{signature}.json`
- TTL: 90 days (deterministic mapping)
- Purpose: Instant MCP suggestions

**Expected Savings**: 50-80% cost reduction, 65% hit rate after 20+ projects

---

## Implementation Plan

### Phase 0: Foundation (Week 1-2)

**Week 1: V2 Bug Fix + Orchestrator Skeleton**
```
Tasks:
1. Fix MessageParser with robust regex patterns
   - Support format: '= X.XXX ≈ 0.XX'
   - Support format: 'Complexity: X.XX'
   - Fallback pattern matching
   - File: src/shannon/sdk/message_parser.py:256

2. Build MessageInterceptor
   - Extract parsing logic from MessageParser
   - Add streaming output extraction
   - Add cost metrics extraction
   - New file: src/shannon/sdk/message_interceptor.py (150 lines)

3. Create ContextAwareOrchestrator skeleton
   - Define interface with 7 manager dependencies
   - Implement execute_analyze() shell
   - Implement execute_wave() shell
   - New file: src/shannon/core/orchestrator.py (200 lines)

4. Test V2 commands work perfectly
   - shannon analyze test_spec.md (should complete successfully)
   - shannon wave "simple task" (validate wave execution)
   - 10+ test specs for validation
```

**Week 2: Integration Contracts + Builder**
```
Tasks:
1. Define manager interfaces
   - ContextManager interface
   - CacheManager interface
   - MetricsCollector interface
   - Cost/MCP/Agent/Analytics interfaces
   - New file: src/shannon/core/interfaces.py (200 lines)

2. Create OrchestratorBuilder
   - build_full_v3() factory method
   - build_v3_core() factory method (for phased rollout)
   - Dependency wiring
   - New file: src/shannon/core/builder.py (150 lines)

3. Shell script test framework
   - tests/functional/test_analyze.sh
   - tests/functional/test_wave.sh
   - tests/functional/run_all.sh
   - New directory: tests/functional/ (3 scripts)
```

**Deliverable**: Solid foundation, V2 bug fixed, integration architecture ready
**Lines**: ~700 lines

---

### Phase 1: Core Monitoring Features (Week 2-5)

**Feature 1: Live Metrics Dashboard (Week 2-3)**
```
Week 2 Tasks:
1. Build LiveDashboard class
   - create_compact_layout() - 4-line panel
   - create_detailed_layout() - Rich Layout with 5 sections
   - File: src/shannon/metrics/dashboard.py (400 lines)

2. Build KeyboardHandler
   - Non-blocking input with select.select()
   - Handle Enter/Esc/q/p keys
   - Terminal mode management
   - File: src/shannon/metrics/keyboard.py (50 lines)

Week 3 Tasks:
3. Build MetricsCollector
   - Real-time progress tracking
   - Cost/token accumulation
   - Streaming buffer (last 20 lines)
   - ETA calculation
   - File: src/shannon/metrics/collector.py (150 lines)

4. Integrate with commands
   - Modify analyze command to use metrics
   - Modify wave command to use metrics
   - Add --metrics flag for optional display
   - Updates: src/shannon/cli/commands.py

5. Test metrics dashboard
   - Run shannon analyze with various specs
   - Test keyboard controls (Enter/Esc/q/p)
   - Validate streaming display
   - Shell script: tests/functional/test_metrics.sh
```

**Feature 3: Multi-Level Caching (Week 3-4)**
```
Week 3-4 Tasks:
1. Build AnalysisCache
   - SHA-256 key computation (with context hash)
   - 7-day TTL checking
   - File: src/shannon/cache/analysis_cache.py (200 lines)

2. Build CommandCache
   - Stable command detection
   - 30-day TTL
   - File: src/shannon/cache/command_cache.py (150 lines)

3. Build MCPRecommendationCache
   - Domain signature computation
   - 90-day TTL (deterministic)
   - File: src/shannon/cache/mcp_cache.py (50 lines)

4. Build CacheManager
   - Orchestrate 3 tiers
   - LRU eviction (500 MB limit)
   - Stats calculation (hit rate, savings)
   - File: src/shannon/cache/manager.py (150 lines)

5. Integrate with Orchestrator
   - Cache check before analyze
   - Cache save after analyze
   - Add cache commands: shannon cache stats/clear
   - Updates: src/shannon/cli/commands.py

6. Test caching
   - Run same spec twice (verify cache hit)
   - Modify spec slightly (verify cache miss)
   - Test cache stats command
   - Shell script: tests/functional/test_cache.sh
```

**Feature 6: Cost Optimization (Week 4-5)**
```
Week 4-5 Tasks:
1. Build ModelSelector
   - Complexity-based selection rules
   - Context size considerations
   - Budget constraints
   - File: src/shannon/optimization/model_selector.py (200 lines)

2. Build CostEstimator
   - Estimate with reuse factor from context
   - Historical cost data analysis
   - File: src/shannon/optimization/cost_estimator.py (150 lines)

3. Build BudgetEnforcer
   - Pre-execution budget checks
   - Hard limit enforcement
   - Warning thresholds (90% budget)
   - File: src/shannon/optimization/budget_enforcer.py (150 lines)

4. Integrate with Orchestrator + Metrics
   - Pre-execution cost estimate
   - Real-time budget tracking in metrics
   - Model optimization suggestions
   - Add commands: shannon config set budget, shannon optimize

5. Test cost optimization
   - Test auto model selection (haiku vs sonnet)
   - Test budget enforcement (reject if over budget)
   - Test optimization recommendations
   - Shell script: tests/functional/test_cost.sh
```

**Phase 1 Deliverable**: V3 Core working (Metrics, Cache, Cost)
**Cumulative Lines**: ~2,500 lines
**Value**: 80% of V3 benefits

---

### Phase 2: Developer Experience Features (Week 5-7)

**Feature 2: MCP Auto-Installation (Week 5)**
```
Tasks:
1. Build MCPDetector
   - CLI detection: parse 'claude mcp list'
   - SDK detection: query for mcp__{name}__* tools
   - Tool enumeration
   - File: src/shannon/mcp/detector.py (150 lines)

2. Build MCPInstaller
   - Run 'claude mcp add {name}' with subprocess
   - Progress feedback with Rich status
   - Timeout handling (60s)
   - File: src/shannon/mcp/installer.py (150 lines)

3. Build MCPVerifier
   - Test MCP functionality after install
   - Verify tools available
   - File: src/shannon/mcp/verifier.py (100 lines)

4. Integration points
   - Setup wizard (Step 5: MCP Configuration)
   - Post-analysis (auto-install recommended MCPs)
   - Pre-wave check (verify required MCPs)
   - Updates: src/shannon/setup/wizard.py, src/shannon/cli/commands.py

5. Test MCP workflow
   - Uninstall test MCP
   - Run shannon analyze (should prompt to install)
   - Verify installation works
   - Shell script: tests/functional/test_mcp_install.sh
```

**Feature 5: Agent-Level Control (Week 6-7)**
```
Week 6 Tasks:
1. Build AgentStateTracker
   - Track AgentState for each spawned agent
   - Capture: messages, cost, tokens, files, prompt
   - Real-time progress updates
   - File: src/shannon/agents/state_tracker.py (250 lines)

2. Build AgentController
   - Pause logic (graceful wait after current agents)
   - Retry logic (rerun from checkpoint)
   - Agent filtering
   - File: src/shannon/agents/controller.py (150 lines)

Week 7 Tasks:
3. Build MessageRouter
   - Route messages to specific agent streams
   - Filter by agent_id
   - File: src/shannon/agents/message_router.py (100 lines)

4. New commands
   - shannon wave agents (list with table)
   - shannon wave follow <id> (stream one agent)
   - shannon wave pause (graceful pause)
   - shannon wave retry <id> (rerun agent)
   - Updates: src/shannon/cli/commands.py

5. Test agent control
   - Run multi-wave execution
   - Test wave agents command
   - Test wave follow (stream one agent)
   - Test wave pause/retry
   - Shell scripts: tests/functional/test_agent_control.sh
```

**Phase 2 Deliverable**: MCP automation + agent debugging
**Cumulative Lines**: ~3,400 lines

---

### Phase 3: Intelligence Features (Week 7-10)

**Feature 7: Historical Analytics (Week 7-8)**
```
Week 7 Tasks:
1. Build AnalyticsDatabase
   - SQLite schema (sessions, dimensions, domains, waves)
   - Connection management
   - Migration support
   - File: src/shannon/analytics/database.py (300 lines)

2. Build TrendsCalculator
   - Complexity trends (last 3 months vs previous)
   - Domain evolution (your patterns vs industry)
   - Timeline accuracy (optimistic % by complexity band)
   - Cost analysis (avg per project, by complexity)
   - File: src/shannon/analytics/trends.py (200 lines)

Week 8 Tasks:
3. Build InsightsGenerator
   - Pattern matching (MCP usage, wave performance)
   - ML recommendations (basic regression for timeline)
   - Personalized suggestions
   - File: src/shannon/analytics/insights.py (100 lines)

4. Integrate with Orchestrator
   - Record after every analyze/wave
   - Track context usage impact
   - Add command: shannon analytics
   - Updates: src/shannon/core/orchestrator.py, src/shannon/cli/commands.py

5. Test analytics
   - Run 20+ analyses (build history)
   - Test shannon analytics command
   - Validate trend calculations
   - Shell script: tests/functional/test_analytics.sh
```

**Feature 8: Context Management System (Week 8-10)**
```
Week 8 Tasks:
1. Build CodebaseOnboarder
   - Directory tree scanning
   - Tech stack detection
   - Pattern extraction (APIs, auth, database)
   - Critical files identification
   - File: src/shannon/context/onboarder.py (400 lines)

2. Build SerenaAdapter
   - Knowledge graph integration
   - Entity/relation creation
   - Observation storage
   - File: src/shannon/context/serena_adapter.py (300 lines)

3. Build ContextPrimer
   - Quick reload from Serena
   - File validation (check files exist)
   - MCP verification
   - File: src/shannon/context/primer.py (200 lines)

Week 9 Tasks:
4. Build ContextUpdater
   - Git diff analysis for changes
   - Incremental Serena updates
   - File: src/shannon/context/updater.py (250 lines)

5. Build ContextSanitizer
   - Stale entity detection
   - Archive old context
   - File: src/shannon/context/sanitizer.py (150 lines)

6. Build SmartContextLoader
   - Keyword extraction from tasks
   - Semantic search in Serena
   - Relevance-based file loading
   - File: src/shannon/context/loader.py (300 lines)

Week 10 Tasks:
7. Build ContextManager
   - Lifecycle management
   - Multi-tier storage (hot/warm/cold)
   - Project metadata tracking
   - File: src/shannon/context/manager.py (200 lines)

8. Integrate with Orchestrator
   - Context loading in execute_analyze()
   - Context-aware cache keys
   - Context-enhanced prompts
   - New commands: shannon onboard, shannon prime --project, shannon context update/clean/status
   - Updates: src/shannon/core/orchestrator.py, src/shannon/cli/commands.py, src/shannon/setup/wizard.py

9. Test context management
   - Test onboard on sample codebase
   - Test prime reload
   - Test context update after changes
   - Test context-aware analysis (verify reuse detection)
   - Shell scripts: tests/functional/test_context_*.sh
```

**Phase 3 Deliverable**: Analytics + Context Management complete
**Cumulative Lines**: ~5,300 lines

---

### Phase 4: Integration & Testing (Week 10-11)

```
Week 10-11 Tasks:
1. Integration testing
   - Test all features working together
   - Test Orchestrator with all 7 managers
   - Validate cache + cost + metrics integration
   - Validate context + analytics integration

2. Shell script test suite expansion
   - tests/functional/test_full_integration.sh
   - tests/functional/test_backwards_compatibility.sh
   - tests/functional/run_all_v3.sh
   - Coverage: All 32 commands tested

3. Documentation updates
   - README.md (add V3 features)
   - Command guides for new commands
   - V3 architecture diagram
   - Migration guide (V2 → V3)

4. Performance optimization
   - Profile cache performance
   - Optimize metrics refresh rate
   - Reduce memory usage in analytics

5. Bug fixes from integration
   - Fix integration issues
   - Handle edge cases
   - Error message improvements
```

**Final Deliverable**: Shannon CLI V3.0 Complete
**Total Lines**: ~5,700 new lines

---

## File Structure

```
shannon-cli/ (V3)
└── src/shannon/
    ├── [V2 components - 6,469 lines]
    │   ├── cli/
    │   │   ├── commands.py (610 lines) ← UPDATED for V3
    │   │   └── output.py
    │   ├── sdk/
    │   │   ├── client.py (253 lines)
    │   │   ├── message_parser.py (580 lines) ← FIXED
    │   │   └── message_interceptor.py (150 lines) ← NEW
    │   ├── ui/
    │   │   ├── formatters.py
    │   │   └── progress.py
    │   ├── storage/
    │   │   ├── models.py
    │   │   └── __init__.py
    │   ├── setup/
    │   │   ├── framework_detector.py
    │   │   └── wizard.py ← UPDATED for V3
    │   ├── core/
    │   │   ├── session_manager.py
    │   │   ├── orchestrator.py (200 lines) ← NEW
    │   │   ├── builder.py (150 lines) ← NEW
    │   │   └── interfaces.py (200 lines) ← NEW
    │   ├── config.py
    │   └── logger.py
    │
    └── [V3 new components - 5,700 lines]
        ├── metrics/
        │   ├── dashboard.py (400 lines)
        │   ├── collector.py (150 lines)
        │   └── keyboard.py (50 lines)
        │
        ├── cache/
        │   ├── analysis_cache.py (200 lines)
        │   ├── command_cache.py (150 lines)
        │   ├── mcp_cache.py (50 lines)
        │   └── manager.py (150 lines)
        │
        ├── mcp/
        │   ├── detector.py (150 lines)
        │   ├── installer.py (150 lines)
        │   └── verifier.py (100 lines)
        │
        ├── agents/
        │   ├── state_tracker.py (250 lines)
        │   ├── controller.py (150 lines)
        │   └── message_router.py (100 lines)
        │
        ├── optimization/
        │   ├── model_selector.py (200 lines)
        │   ├── cost_estimator.py (150 lines)
        │   └── budget_enforcer.py (150 lines)
        │
        ├── analytics/
        │   ├── database.py (300 lines)
        │   ├── trends.py (200 lines)
        │   └── insights.py (100 lines)
        │
        └── context/
            ├── onboarder.py (400 lines)
            ├── primer.py (200 lines)
            ├── updater.py (250 lines)
            ├── sanitizer.py (150 lines)
            ├── loader.py (300 lines)
            ├── manager.py (200 lines)
            └── serena_adapter.py (300 lines)
```

**Total**: 12,169 lines (V2: 6,469 + V3: 5,700)

---

## Testing Strategy

**Principle**: NO PYTEST, functional shell scripts only (Shannon mandate)

**Test Categories**:

1. **Unit-Level Functional Tests** (test individual features):
   - tests/functional/test_metrics.sh
   - tests/functional/test_cache.sh
   - tests/functional/test_cost.sh
   - tests/functional/test_mcp_install.sh
   - tests/functional/test_agent_control.sh
   - tests/functional/test_analytics.sh
   - tests/functional/test_context.sh

2. **Integration Tests** (test feature combinations):
   - tests/functional/test_full_integration.sh
   - tests/functional/test_orchestrator.sh
   - tests/functional/test_backwards_compatibility.sh

3. **End-to-End Tests** (test complete workflows):
   - tests/functional/test_analyze_workflow.sh
   - tests/functional/test_wave_workflow.sh
   - tests/functional/test_task_workflow.sh

4. **Master Test Suite**:
   - tests/functional/run_all_v3.sh (runs all tests)
   - Exit code 0 if all pass
   - CI/CD compatible

**Self-Validation Pattern** (from ultrathinking Thought 28):
- Build Metrics → Use metrics while building Cache
- Build Cache → Use cache while building Cost
- Build Cost → Use cost optimization while building remaining features
- Each feature validates previous features through real usage

---

## Backward Compatibility

**Preserved from V2**:
- ✅ All command syntax (`shannon analyze spec.md`)
- ✅ All flags (--json, --session-id, --verbose)
- ✅ Session file format (~/.shannon/sessions/*.json)
- ✅ Config file format (~/.shannon/config.json)
- ✅ Exit codes for CI/CD
- ✅ SDK integration (plugin loading, skill invocation)

**Added in V3** (backward compatible):
- ✅ New commands (cache, analytics, onboard, prime, context, optimize)
- ✅ New flags (--cache, --optimize-cost, --metrics, --project)
- ✅ New directories (~/.shannon/cache/, ~/.shannon/analytics.db)
- ✅ Optional features (all toggleable with flags)

**Migration**: V2 → V3 is seamless upgrade (no breaking changes)

---

## Success Criteria

Shannon CLI V3.0 succeeds when:

**Functional**:
- ✅ All 32 commands work correctly
- ✅ V2 commands unchanged (backward compatible)
- ✅ MessageParser bug fixed
- ✅ Live metrics dashboard functional
- ✅ Caching achieves 50%+ hit rate after 10 projects
- ✅ Cost optimization saves 30%+ on average
- ✅ Agent control enables debugging
- ✅ Analytics provides actionable insights
- ✅ Context management works with existing codebases

**Quality**:
- ✅ All functional tests pass (shell scripts)
- ✅ No pytest usage (spec compliant)
- ✅ Comprehensive documentation
- ✅ Clean code (type hints, docstrings)

**Performance**:
- ✅ Cache hits < 500ms
- ✅ Metrics dashboard 4 FPS refresh
- ✅ Context loading < 30 seconds
- ✅ Memory < 200 MB during execution

**Integration**:
- ✅ All features work together via Orchestrator
- ✅ No feature fragmentation
- ✅ Clean interfaces between components

---

## Risk Analysis

**High Risk**:
- Context Management (1,800 lines, complex, Serena integration)
- Mitigation: Build last, extensive testing, fallback to manual context

**Medium Risk**:
- Live Metrics (terminal UI, keyboard handling, async complexity)
- Mitigation: Build early (Week 2-3), test extensively

**Low Risk**:
- Caching (straightforward file operations)
- Cost Optimization (simple logic)
- MCP Installation (subprocess management)

---

## Future Extensions (Post-V3.0)

Possible V3.1 features:
- Web UI for metrics (alternative to terminal)
- GitHub integration (track issues, PRs)
- Team collaboration (shared analytics)
- Cloud caching (shared across machines)
- Advanced ML (better timeline prediction)

---

## Design Complete

**Shannon CLI V3.0 Full Implementation Design**
- ✅ 8 features specified
- ✅ 11-week timeline
- ✅ ContextAwareOrchestrator integration architecture
- ✅ Complete file structure
- ✅ Testing strategy (functional shell scripts)
- ✅ Backward compatibility preserved
- ✅ Risk analysis complete

Ready for implementation planning.
