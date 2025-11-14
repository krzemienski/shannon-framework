# Shannon CLI V3.0 - Architecture Summary

**Quick Reference**: Key architectural decisions and integration points

---

## Executive Summary

Shannon CLI V3.0 transforms from a simple command wrapper (5,102 lines) to an intelligent development orchestration platform (9,902 lines) through 8 new subsystems that work in concert.

**Core Innovation**: SDK message interception as architectural primitive enables all V3 features without breaking existing functionality.

---

## Critical Architectural Decisions

### 1. SDK Message Interception (Foundation)

**Decision**: Transparent async wrapper with parallel collectors

```python
# Zero-latency message interception
async for msg in interceptor.intercept(query_stream, collectors):
    # Collectors run in parallel (asyncio.create_task)
    # Messages yielded immediately (no blocking)
    yield msg
```

**Why**: Enables metrics, tracking, and context collection without breaking SDK contract

---

### 2. 3-Tier Context Architecture

**Decision**: Hot (memory) → Warm (local files) → Cold (Serena MCP)

```
Hot:   Instant, session-only, current state
Warm:  ~100ms, permanent, local index
Cold:  ~500ms, permanent, searchable knowledge graph
```

**Why**: Optimal performance while supporting unlimited history

---

### 3. Context-Aware Cache Keys

**Decision**: SHA-256(spec + framework_version + model + context_hash)

```python
# Different cache entries for same spec with/without context
without_context: hash(spec + ver + model)        → Entry 1
with_context:    hash(spec + ver + model + ctx)  → Entry 2
```

**Why**: Ensures cached results reflect actual context availability

---

### 4. Central State Coordination

**Decision**: ContextAwareOrchestrator as single integration hub

```python
orchestrator = ContextAwareOrchestrator(
    context_manager,     # 3-tier context storage
    metrics_collector,   # Live dashboard
    cache_manager,       # 3-level caching
    mcp_manager,         # Auto-installation
    agent_tracker,       # State tracking
    cost_optimizer,      # Model selection
    analytics           # Historical tracking
)
```

**Why**: No feature works in isolation; all leverage context and metrics

---

### 5. Functional Testing Only (NO MOCKS)

**Decision**: All tests use real SDK, real MCPs, real file system

```python
async def test_analysis_with_context():
    # Real onboarding
    await onboarder.onboard(test_project_path)

    # Real SDK call
    result = await orchestrator.execute_analyze(spec, project_id)

    # Real verification
    assert result['complexity_score'] < 0.50  # Context reduces complexity
```

**Why**: Shannon philosophy - validate actual behavior, not mocked behavior

---

## Module Architecture

### 8 New Subsystems (4,800 lines)

```
1. metrics/       (600 lines) - Live dashboard, 4 Hz refresh
2. cache/         (500 lines) - 3-tier caching (analysis, command, MCP)
3. mcp/           (400 lines) - Auto-detect, install, verify MCPs
4. agents/        (500 lines) - Track, pause, resume, retry agents
5. optimization/  (500 lines) - Smart model selection, budget enforcement
6. analytics/     (600 lines) - SQLite database, trends, insights
7. context/     (1,800 lines) - Onboard, prime, update, smart loading
8. orchestrator.py (400 lines) - Integration hub coordinating all subsystems
```

### Data Flow (Complete Integration)

```
shannon analyze spec.md --project my-app
    ↓
ContextAwareOrchestrator
    ↓
1. Load context (ContextManager → Serena MCP)
2. Check cache (CacheManager → context-aware key)
3. Check budget (BudgetEnforcer → estimate cost)
4. Execute with metrics (LiveDashboard → 4 Hz refresh)
5. Auto-install MCPs (MCPManager → post-analysis)
6. Save to cache (CacheManager → with context hash)
7. Record analytics (AnalyticsDatabase → SQLite)
8. Update context (ContextManager → metadata)
    ↓
Return result (with context, metrics, cost tracked)
```

---

## Integration Points

### Every Command Enhanced

- **analyze**: Context-aware, cached, metered, recorded
- **wave**: Agent tracking, model optimization, pause/resume
- **onboard**: Create context, auto-install MCPs, Serena storage
- **prime**: Fast context reload, MCP verification
- **task**: Full workflow with context throughout

### No Isolated Features

```
Metrics   ←→  Context   (shows loaded files)
Cache     ←→  Context   (context-aware keys)
MCP       ←→  Context   (tech stack detection)
Agents    ←→  Context   (agents receive context)
Cost      ←→  Context   (reuse estimation)
Analytics ←→  Context   (track effectiveness)
```

---

## Risk Mitigation

### 1. SDK Breaking Changes
- **Risk**: SDK updates break interception
- **Mitigation**: Version pinning, interface abstraction, graceful degradation

### 2. Serena Unavailability
- **Risk**: Serena MCP not installed
- **Mitigation**: Fallback to local files, auto-install in setup

### 3. Budget Exhaustion
- **Risk**: Budget runs out mid-wave
- **Mitigation**: Pre-wave check, pause mechanism, checkpoint/resume

### 4. Context Staleness
- **Risk**: Cached context becomes outdated
- **Mitigation**: Age warnings, update prompts, git diff detection

### 5. Terminal Compatibility
- **Risk**: Terminal doesn't support Rich/termios
- **Mitigation**: Capability detection, graceful degradation, plain text mode

---

## Performance Targets

- **UI Refresh**: 4 Hz (250ms intervals)
- **Context Load**: <500ms warm, <2s cold
- **Cache Hit Rate**: >70%
- **Keyboard Latency**: <100ms
- **Cost Savings**: 30-50% via model optimization

---

## Testing Strategy

### NO MOCKS Philosophy

```python
# 60% of tests are functional (real components)
Functional Tests (primary):
  - Real SDK calls to Claude
  - Real Serena MCP
  - Real file system
  - Real SQLite database

Integration Tests:
  - Module interactions
  - Data flow validation

Unit Tests (minimal):
  - Pure functions only
  - No I/O, no mocking
```

### Coverage Targets
- Overall: 70%
- Critical paths: 90%
- New V3 modules: 80%

---

## Implementation Phases (10 weeks)

1. **Weeks 1-2**: Metrics & Interception (foundation)
2. **Weeks 2-3**: MCP Management (auto-install)
3. **Weeks 3-4**: Caching (3-tier system)
4. **Weeks 4-5**: Agent Control (tracking, pause/resume)
5. **Weeks 5-6**: Cost Optimization (model selection, budget)
6. **Weeks 6-7**: Analytics (SQLite, trends, insights)
7. **Weeks 7-9**: Context Management (onboard, smart loading)
8. **Weeks 9-10**: Integration & Testing (orchestrator, tests)

---

## Key Design Patterns

### 1. Transparent Interception
```python
# Pattern: Wrap without breaking
original_stream = sdk.query(prompt)
enhanced_stream = interceptor.intercept(original_stream, collectors)
# Caller receives identical interface
```

### 2. Collector Pattern
```python
# Pattern: Parallel processing via collectors
class MetricsCollector(MessageCollector):
    async def process(self, msg):
        # Extract metrics asynchronously
        pass
```

### 3. 3-Tier Storage
```python
# Pattern: Hot → Warm → Cold cascade
result = hot_cache.get(key) or \
         warm_cache.get(key) or \
         cold_storage.get(key)
```

### 4. Context Injection
```python
# Pattern: Enhance prompts with context
prompt_enhanced = f"""
{original_prompt}

Existing Project Context:
{context['summary']}
{context['relevant_files']}
"""
```

### 5. Smart Loading
```python
# Pattern: Load relevant subset
keywords = extract_keywords(task)
relevant_files = search_and_rank(keywords)
load_top_n(relevant_files, max_lines=5000)
```

---

## Success Criteria

### Technical
- SDK interception adds zero latency
- Cache hit rate >70%
- Context loading <500ms
- Test coverage >70%
- No circular dependencies

### User Experience
- Cost savings 30-50%
- Time savings 60-80% (cache hits)
- Context improves accuracy 30%
- MCP install rate >80%

### Quality
- Functional tests >60% of total
- Bug rate <1 per 1000 lines
- Code complexity within limits
- Documentation complete

---

## Architecture Validation

**Ready for Implementation**: YES

- All critical decisions documented with rationale
- All integration points defined
- All risks identified with mitigations
- All modules specified with line counts
- All tests planned (functional-first)
- Complete data flow diagrams
- Clear implementation roadmap

**Next Step**: Wave 1 - Metrics & Interception (Weeks 1-2)

---

## Quick Reference: File Structure

```
src/shannon/
├── [V2 Base - 5,102 lines]
│   cli/, sdk/, ui/, storage/, setup/, core/
│
├── [V3 New - 4,800 lines]
│   ├── metrics/              # Live dashboard
│   ├── cache/                # 3-tier caching
│   ├── mcp/                  # Auto-installation
│   ├── agents/               # State tracking
│   ├── optimization/         # Model selection
│   ├── analytics/            # SQLite + insights
│   ├── context/              # Onboarding + loading
│   └── orchestrator.py       # Integration hub
│
└── Total: 9,902 lines
```

---

**Architecture Version**: 1.0
**Status**: APPROVED
**Implementation**: Ready to begin
**Full Document**: SHANNON_CLI_V3_ARCHITECTURE.md
