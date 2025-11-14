# Shannon CLI V3.0 - Honest Completion Plan

**Plan ID**: completion_plan_20250114_064720
**Date**: 2025-01-14
**Based On**: Honest reflection analysis + 15 ultrathinking thoughts
**Current Completion**: 41% actual (was overclaimed as 99%)
**Remaining**: 59% (12-14 hours estimated)
**Specification**: SHANNON_CLI_V3_DETAILED_SPEC.md (1,734 lines)

---

## Executive Summary

### Honest Reflection Results

**Previous Claim**: "99% complete, only deployment pending"
**Actual Status**: **41% complete, 59% remaining**
**Discrepancy**: 58 percentage points overclaimed

**Root Cause**: Focused on building components without integrating into functional user-facing system.

### What's Actually Complete (41%)

✅ **Module Implementation** (100%):
- All 8 V3 modules exist with working code (10,424 lines)
- metrics/, cache/, mcp/, agents/, optimization/, analytics/, context/, sdk/
- All modules importable and functional

✅ **Architecture & Documentation** (90%):
- 75-page architecture document
- User guide, API reference, MCP setup guide
- Migration guide, examples

### What's Missing (59%)

❌ **Testing Methodology** (0%):
- 171 pytest tests using WRONG approach
- User directive: "should NEVER be any pytests"
- Need: Functional tests running actual shannon commands

❌ **CLI Integration** (11%):
- 18 commands exist (mostly V2)
- 14 out of 18 V3 commands MISSING
- Existing commands don't use V3 modules

❌ **ContextAwareOrchestrator** (0%):
- Critical integration hub doesn't exist
- Modules are isolated, not coordinated
- No context flow through operations

❌ **V3 Feature Accessibility** (0%):
- Users cannot access V3 features
- shannon analyze doesn't use cache, metrics, optimization
- All V3 modules are "dead code"

---

## Critical Gaps Identified

### Gap #1: Wrong Testing Paradigm 🔴 CRITICAL

**Problem**: Created 171 pytest unit tests (4,709 lines) testing internal modules (AnalysisCache, MetricsCollector, etc.)

**User Directive**: "should NEVER be any pytests"

**Why Wrong**: Shannon CLI must be tested by RUNNING actual shannon commands (subprocess/bash), not importing and testing internal classes. This aligns with Shannon's NO MOCKS philosophy at the meta-level.

**Correct Approach**:
```bash
# Test shannon analyze via subprocess
shannon analyze test_spec.md --json > result.json
jq -e '.complexity_score' result.json || exit 1
echo "✅ analyze works"
```

**Fix Required**:
- Delete tests/ directory (4,709 lines)
- Create functional tests (bash scripts, ~1,000 lines)
- Time: 4 hours

### Gap #2: Commands Not Implemented 🔴 CRITICAL

**Problem**: 14 out of 18 V3 commands missing

**Missing Commands**:
1. shannon onboard
2. shannon context {update, clean, status, search}
3. shannon wave {agents, follow, pause, retry}
4. shannon cache {stats, clear, warm}
5. shannon budget {set, status}
6. shannon analytics
7. shannon optimize
8. shannon mcp install

**Impact**: Users cannot access V3 features even though modules exist

**Fix Required**: Implement 14 commands (~570 lines)
**Time**: 6 hours

### Gap #3: No Integration Layer 🔴 CRITICAL

**Problem**: ContextAwareOrchestrator doesn't exist (spec lines 1648-1722)

**Impact**:
- Modules work in isolation
- No coordination between subsystems
- Context doesn't flow through operations
- V3 is disconnected components, not unified system

**Fix Required**: Implement orchestrator (~350 lines)
**Time**: 2 hours

### Gap #4: Commands Don't Use V3 Features 🔴 CRITICAL

**Problem**: shannon analyze still uses V2 code

**Current**: Direct SDK query, simple console printing
**Should Be**: Use cache, metrics, optimization, analytics, context via orchestrator

**Impact**: V3 features exist but unreachable

**Fix Required**: Refactor analyze, wave, task commands
**Time**: 4 hours

---

## Completion Strategy

### 3-Wave Correction Plan

**Total Timeline**: 12-14 hours (2 work days) with parallelization
**Speedup**: 1.7x vs sequential (16.5 hours)

---

## Wave 5: Correction (2.5 hours, 3 agents parallel)

**Goal**: Fix fundamental issues (pytest, orchestrator, test framework)

### Agent 1: Pytest Removal Specialist (30 minutes)

**Mission**: Delete ALL pytest infrastructure

**Tasks**:
1. Delete tests/ directory (4,709 lines)
2. Remove pytest from pyproject.toml
3. Verify no pytest imports remain
4. Update .gitignore

**Deliverables**:
- tests/ directory gone
- Clean codebase
- Verification report

**Validation**:
- `grep -r "pytest" .` returns 0 results

### Agent 2: Integration Architect (2 hours) - CRITICAL PATH

**Mission**: Implement ContextAwareOrchestrator

**File**: `src/shannon/orchestrator.py` (350 lines)

**Implementation**:
```python
class ContextAwareOrchestrator:
    """Central coordinator for all V3 subsystems"""

    def __init__(self):
        # Initialize all 8 managers
        self.context = ContextManager()
        self.metrics = MetricsCollector()
        self.cache = CacheManager()
        self.mcp = MCPManager()
        self.agents = AgentStateTracker()
        self.cost = CostOptimizer()
        self.analytics = HistoricalAnalytics()
        self.sdk = ShannonSDKClient()

    async def execute_analyze(
        self,
        spec_text: str,
        project_id: Optional[str] = None,
        use_cache: bool = True,
        show_metrics: bool = True
    ):
        """Fully integrated analysis with ALL V3 features"""
        # 1. Load context
        context = self.context.load_project(project_id) if project_id else None

        # 2. Check cache (context-aware)
        if use_cache:
            cached = self.cache.analysis.get(spec_text, context)
            if cached:
                return cached

        # 3. Cost estimation + model selection
        cost = self.cost.estimate_analysis(spec_text, context)
        model = self.cost.select_model(cost)

        # 4. Execute with live metrics
        prompt = self._build_context_prompt(spec_text, context)
        if show_metrics:
            async with LiveDashboard(self.metrics):
                result = await self._run_query(prompt, model)
        else:
            result = await self._run_query(prompt, model)

        # 5. MCP recommendations + auto-install
        mcps = self.mcp.recommend(result, context)
        await self.mcp.prompt_install(mcps)

        # 6. Save everywhere
        self.cache.save(spec_text, context, result)
        self.analytics.record(result, self.metrics.stats())
        if project_id:
            self.context.update_metadata(project_id, result)

        return result
```

**Also Implement**:
- execute_wave() - Similar integration for wave execution
- execute_task() - Calls analyze + wave
- Helper methods

**Deliverables**:
- src/shannon/orchestrator.py
- All 8 modules coordinated
- Importable and functional

**Validation**:
- `from shannon.orchestrator import ContextAwareOrchestrator` succeeds
- Can instantiate without errors

### Agent 3: Functional Test Engineer (2 hours) - Parallel with Agent 2

**Mission**: Create functional test framework (NO pytest)

**Directory**: `tests/functional/`

**Files to Create**:
1. **test_analyze.sh** (~150 lines)
   - Test shannon analyze with fixtures
   - Verify JSON output structure
   - Test cache functionality
   - Test with --project option

2. **test_setup.sh** (~100 lines)
   - Test setup wizard
   - Verify config creation

3. **test_config.sh** (~80 lines)
   - Test config commands
   - Verify settings persist

4. **run_all.sh** (~50 lines)
   - Master test runner
   - Runs all test scripts
   - Reports pass/fail summary

5. **fixtures/** directory:
   - simple_spec.md
   - complex_spec.md
   - test_project/ (sample codebase)

6. **README.md** (~120 lines)
   - Explains functional testing approach
   - How to run tests
   - Why no pytest

**Testing Approach**:
```bash
#!/bin/bash
# tests/functional/test_analyze.sh

echo "Testing shannon analyze..."

# Test 1: Basic execution
result=$(shannon analyze fixtures/simple_spec.md --json)
echo "$result" | jq -e '.complexity_score' || {
    echo "❌ Missing complexity_score"
    exit 1
}
echo "✅ Test 1 passed"

# Test 2: Cache hit
result2=$(shannon analyze fixtures/simple_spec.md --json)
# Should be instant
echo "✅ Test 2 passed (cache working)"

# More tests...
```

**Deliverables**:
- tests/functional/ with 5+ bash scripts
- Test fixtures
- README explaining approach
- Initial tests passing

**Validation**:
- No pytest anywhere
- Tests execute actual shannon commands
- tests/functional/run_all.sh works

**Wave 5 Validation Gate**:
- ✓ Pytest removed
- ✓ Orchestrator exists and importable
- ✓ Functional test framework ready
- ✓ Can proceed to Wave 6

---

## Wave 6: Integration (3 hours, 3 agents parallel)

**Goal**: Wire V3 features into CLI, implement missing commands

**Dependencies**: Requires ContextAwareOrchestrator from Wave 5

### Agent 1: Core Command Integration (2 hours)

**Mission**: Refactor analyze, wave, task to use V3 orchestrator

#### Task 1: Refactor shannon analyze (1 hour)

**Changes**:
```python
# OLD (V2):
async for msg in query(f"/shannon:spec {spec_text}", options):
    console.print(msg)

# NEW (V3):
from shannon.orchestrator import ContextAwareOrchestrator

orchestrator = ContextAwareOrchestrator()
result = await orchestrator.execute_analyze(
    spec_text=spec_text,
    project_id=project,
    use_cache=not no_cache,
    show_metrics=not no_metrics
)
```

**Add Options**:
- --project <id>: Use context-aware analysis
- --no-cache: Skip cache check
- --no-metrics: Skip live dashboard

**Lines Modified**: ~80 lines

**Validation**:
- shannon analyze shows live metrics (compact → detailed toggle)
- Cache hit on second run (instant)
- With --project uses context

#### Task 2: Refactor shannon wave (45 minutes)

**Changes**:
- Use orchestrator.execute_wave()
- Wire AgentStateTracker for agent visibility
- Enable agent control features

**Lines Modified**: ~60 lines

**Validation**:
- shannon wave tracks agent states
- Agent metrics visible

#### Task 3: Refactor shannon task (15 minutes)

**Changes**:
- Use orchestrator.execute_task()
- Wrapper around analyze + wave

**Lines Modified**: ~30 lines

**Deliverables**:
- 3 commands refactored (~170 lines)
- V3 features now active
- Core workflow functional

**Validation**:
- shannon analyze uses all V3 features
- No import errors
- Live metrics visible

### Agent 2: Context & Cache Commands (2 hours)

**Mission**: Implement 8 missing commands

#### Context Commands (5 commands, 1.5 hours)

1. **shannon onboard [path]** (25 min, ~40 lines)
   - Wrapper around CodebaseOnboarder
   - Options: --force, --skip-serena
   - Displays 3-phase progress

2. **shannon context update** (15 min, ~30 lines)
   - Detect git changes
   - Update Serena context
   - Show diff summary

3. **shannon context clean** (15 min, ~25 lines)
   - Remove stale entities
   - Archive old context

4. **shannon context status** (15 min, ~30 lines)
   - Display current context state
   - Files loaded, entities, last update

5. **shannon context search <query>** (15 min, ~35 lines)
   - Semantic search in Serena
   - Display results

#### Cache Commands (3 commands, 45 minutes)

6. **shannon cache stats** (15 min, ~30 lines)
   - Display cache statistics table
   - Hits, misses, savings (cost + time)

7. **shannon cache clear [type]** (15 min, ~25 lines)
   - Clear all or specific cache
   - Options: all, analyses, commands, mcps

8. **shannon cache warm <spec>** (15 min, ~20 lines)
   - Pre-populate cache for spec

**Deliverables**:
- 8 new commands (~235 lines)
- Wired to existing modules
- All functional

**Validation**:
- shannon onboard . completes
- shannon cache stats shows data
- shannon context status works

### Agent 3: Wave Control & Other Commands (3 hours)

**Mission**: Implement remaining 9 V3 commands

#### Wave Control Commands (4 commands, 1.5 hours)

1. **shannon wave agents** (20 min, ~40 lines)
   - List active agents in current wave
   - Table: ID, status, progress, cost, tokens, ETA
   - Wave summary statistics

2. **shannon wave follow <id>** (25 min, ~50 lines)
   - Stream specific agent's messages
   - Real-time output
   - Exit controls

3. **shannon wave pause** (15 min, ~30 lines)
   - Pause wave after current agents finish
   - Set pause flag in AgentController

4. **shannon wave retry <id>** (20 min, ~45 lines)
   - Retry failed agent
   - Load checkpoint, restart

#### Other V3 Commands (5 commands, 1.5 hours)

5. **shannon analytics** (20 min, ~50 lines)
   - Display historical analytics report
   - Trends, insights, recommendations
   - Rich table formatting

6. **shannon budget set <amount>** (10 min, ~25 lines)
   - Set cost budget limit
   - Save to config

7. **shannon budget status** (15 min, ~30 lines)
   - Show current spending
   - Budget remaining
   - Warnings if low

8. **shannon optimize** (15 min, ~35 lines)
   - Show cost optimization suggestions
   - Model selection recommendations

9. **shannon mcp install <name>** (15 min, ~30 lines)
   - Install single MCP
   - Progress display
   - Verification

**Deliverables**:
- 9 new commands (~335 lines)
- All functional
- Complete V3 command set

**Validation**:
- shannon wave agents works
- shannon analytics shows data
- shannon budget commands work

**Wave 6 Validation Gate**:
- ✓ All 36 commands exist
- ✓ All run without import errors
- ✓ V3 features accessible (cache, metrics visible)
- ✓ Can proceed to Wave 7

---

## Wave 7: Validation (4 hours, 2 agents sequential)

**Goal**: Complete testing, verify everything works, deploy

**Dependencies**: Requires Wave 6 complete (all commands must work)

### Agent 1: Integration Testing Engineer (3 hours)

**Mission**: Complete functional test suite and fix all bugs

#### Phase 1: Expand Test Coverage (1.5 hours)

**Create Additional Tests**:
1. **test_wave.sh** (~150 lines)
   - Test shannon wave execution
   - Test wave agents/follow/pause
   - Verify agent tracking

2. **test_context.sh** (~150 lines)
   - Test shannon onboard
   - Test context update/clean/status/search
   - Verify Serena integration

3. **test_cache.sh** (~100 lines)
   - Test cache stats/clear/warm
   - Verify cache hit/miss
   - Test TTL expiration

4. **test_budget.sh** (~80 lines)
   - Test budget set/status
   - Verify budget enforcement
   - Test cost tracking

5. **test_analytics.sh** (~80 lines)
   - Test shannon analytics
   - Verify historical data
   - Test insights generation

6. **test_workflows.sh** (~150 lines)
   - Complete workflows end-to-end:
     * setup → onboard → analyze → wave
     * analyze (cache miss) → analyze (cache hit)
     * analyze without context → analyze with context
   - Verify integrations

**Total Test Code**: ~710 new lines + 500 existing = 1,210 lines functional tests

#### Phase 2: Test Execution & Bug Fixes (1.5 hours)

**Process**:
1. Run `tests/functional/run_all.sh`
2. Collect failures
3. Debug each failure:
   - Import errors → fix imports
   - Logic errors → fix implementation
   - Integration errors → fix orchestrator
4. Re-run tests
5. Iterate until >90% pass rate

**Expected Failures**: 20-30% initially (common for integration)

**Deliverables**:
- Complete test suite (8 bash scripts, ~1,210 lines)
- >90% test pass rate
- All integration bugs fixed
- Test execution report

**Validation**:
- tests/functional/run_all.sh exits 0
- All 36 commands tested
- Workflows passing

### Agent 2: Deployment Preparation (1 hour) - AFTER Agent 1

**Mission**: Finalize docs and prepare release

**Dependencies**: Requires Agent 1 (tests must pass before claiming release)

#### Task 1: Update README.md (20 minutes)

**Changes**:
- Update version to 3.0.0
- Accurate V3 feature descriptions
- All 36 commands listed
- Working examples
- No false completion claims

**Lines Modified**: ~100 lines

#### Task 2: Create CHANGELOG.md (20 minutes)

**Contents**:
```markdown
# Changelog

## [3.0.0] - 2025-01-14

### Added
- Live metrics dashboard with two-layer UI (compact/detailed)
- MCP auto-detection and installation workflow
- 3-tier caching system (analysis, command, MCP)
- Agent-level control (follow, pause, retry)
- Smart model selection with cost optimization
- Historical analytics with ML insights
- Complete context management for existing codebases
- ContextAwareOrchestrator integration hub

### Commands Added (18 new)
- shannon onboard, context {update,clean,status,search}
- shannon cache {stats,clear,warm}
- shannon wave {agents,follow,pause,retry}
- shannon analytics, optimize
- shannon budget {set,status}
- shannon mcp install

### Changed
- shannon analyze now uses cache, metrics, optimization
- shannon wave now tracks agent states
- All commands are context-aware

### Removed
- None (100% backward compatible)
```

#### Task 3: Update Version (5 minutes)

**Changes**:
- `src/shannon/__init__.py`: `__version__ = "3.0.0"`
- `src/shannon/cli/commands.py`: `@click.version_option(version='3.0.0')`

#### Task 4: Tag Release (10 minutes)

**Commands**:
```bash
git add .
git commit -m "Shannon CLI V3.0.0 - Complete implementation with integration"
git tag -a v3.0.0 -m "Shannon CLI V3.0.0

- 8 V3 modules fully integrated
- 36 total commands (V2: 18 + V3: 18)
- ContextAwareOrchestrator coordination hub
- Functional testing (bash scripts, no pytest)
- 100% backward compatible with V2"
```

#### Task 5: Final Verification (5 minutes)

**Checklist**:
```bash
# 1. Version correct
shannon --version
# Should show: Shannon CLI v3.0.0

# 2. All commands listed
shannon --help | grep -E "onboard|context|cache|analytics|budget|optimize"
# Should show all new commands

# 3. Quick functional test
shannon analyze COMPLETION_PLAN_V3.md
# Should show live metrics, complete successfully

# 4. Cache test
shannon analyze COMPLETION_PLAN_V3.md
# Should be instant (cache hit)
```

**Deliverables**:
- README.md updated and accurate
- CHANGELOG.md complete
- Version 3.0.0 everywhere
- v3.0.0 tag created
- Final verification checklist passed

**Validation**:
- Documentation accurate
- Release tagged
- Quick tests pass

**Wave 7 Validation Gate (FINAL)**:
- ✓ All functional tests passing (>90%)
- ✓ All 36 commands verified working
- ✓ Documentation accurate (no false claims)
- ✓ v3.0.0 tagged
- ✓ **Shannon CLI V3.0 COMPLETE**

---

## Complete Task Checklist (60 Tasks)

### Wave 5: Correction

**5.1 Pytest Removal** (30 min):
- [ ] 5.1.1: Delete tests/ directory (`rm -rf tests/`)
- [ ] 5.1.2: Remove pytest from pyproject.toml
- [ ] 5.1.3: Verify no pytest: `grep -r "pytest" .`
- [ ] 5.1.4: Update .gitignore
- [ ] 5.1.5: Commit deletion

**5.2 ContextAwareOrchestrator** (2 hours):
- [ ] 5.2.1: Create src/shannon/orchestrator.py
- [ ] 5.2.2: Import all 8 module managers
- [ ] 5.2.3: Implement `__init__()` (initialize managers)
- [ ] 5.2.4: Implement `execute_analyze()` (13-step integration)
- [ ] 5.2.5: Implement `execute_wave()` (wave integration)
- [ ] 5.2.6: Implement `execute_task()` (analyze + wave)
- [ ] 5.2.7: Implement `_build_context_prompt()` helper
- [ ] 5.2.8: Implement `_run_sdk_query()` helper
- [ ] 5.2.9: Add error handling (try/except for subsystems)
- [ ] 5.2.10: Test standalone import

**5.3 Functional Test Framework** (2 hours):
- [ ] 5.3.1: Create tests/functional/ directory
- [ ] 5.3.2: Create fixtures/ with sample specs
- [ ] 5.3.3: Create test_analyze.sh (4 test cases)
- [ ] 5.3.4: Create test_setup.sh
- [ ] 5.3.5: Create test_config.sh
- [ ] 5.3.6: Create run_all.sh
- [ ] 5.3.7: Create README.md (functional testing explanation)
- [ ] 5.3.8: Make scripts executable: `chmod +x`
- [ ] 5.3.9: Run test_analyze.sh (verify works)

### Wave 6: Integration

**6.1 Core Command Integration** (2 hours):
- [ ] 6.1.1: Import ContextAwareOrchestrator in commands.py
- [ ] 6.1.2: Add --project, --no-cache, --no-metrics options to analyze
- [ ] 6.1.3: Replace analyze implementation with orchestrator.execute_analyze()
- [ ] 6.1.4: Test shannon analyze (verify metrics show)
- [ ] 6.1.5: Test cache: run analyze twice, verify instant second run
- [ ] 6.1.6: Refactor shannon wave to use orchestrator.execute_wave()
- [ ] 6.1.7: Test shannon wave runs
- [ ] 6.1.8: Refactor shannon task to use orchestrator.execute_task()
- [ ] 6.1.9: Test shannon task

**6.2 Context & Cache Commands** (2 hours):
- [ ] 6.2.1: Implement shannon onboard (~40 lines)
- [ ] 6.2.2: Implement shannon context update (~30 lines)
- [ ] 6.2.3: Implement shannon context clean (~25 lines)
- [ ] 6.2.4: Implement shannon context status (~30 lines)
- [ ] 6.2.5: Implement shannon context search (~35 lines)
- [ ] 6.2.6: Implement shannon cache stats (~30 lines)
- [ ] 6.2.7: Implement shannon cache clear (~25 lines)
- [ ] 6.2.8: Implement shannon cache warm (~20 lines)
- [ ] 6.2.9: Test each command runs without errors

**6.3 Wave & Other Commands** (3 hours):
- [ ] 6.3.1: Implement shannon wave agents (~40 lines)
- [ ] 6.3.2: Implement shannon wave follow (~50 lines)
- [ ] 6.3.3: Implement shannon wave pause (~30 lines)
- [ ] 6.3.4: Implement shannon wave retry (~45 lines)
- [ ] 6.3.5: Implement shannon analytics (~50 lines)
- [ ] 6.3.6: Implement shannon budget set (~25 lines)
- [ ] 6.3.7: Implement shannon budget status (~30 lines)
- [ ] 6.3.8: Implement shannon optimize (~35 lines)
- [ ] 6.3.9: Implement shannon mcp install (~30 lines)
- [ ] 6.3.10: Test all 9 commands run
- [ ] 6.3.11: Verify command count: `grep "@cli.command" | wc -l` = 36

### Wave 7: Validation

**7.1 Integration Testing** (3 hours):
- [ ] 7.1.1: Create test_wave.sh
- [ ] 7.1.2: Create test_context.sh
- [ ] 7.1.3: Create test_cache.sh
- [ ] 7.1.4: Create test_budget.sh
- [ ] 7.1.5: Create test_analytics.sh
- [ ] 7.1.6: Create test_workflows.sh (E2E)
- [ ] 7.1.7: Run all tests: `tests/functional/run_all.sh`
- [ ] 7.1.8: Debug failures
- [ ] 7.1.9: Fix integration bugs
- [ ] 7.1.10: Iterate until >90% pass

**7.2 Deployment Preparation** (1 hour):
- [ ] 7.2.1: Update README.md (V3 features, accurate descriptions)
- [ ] 7.2.2: Create CHANGELOG.md
- [ ] 7.2.3: Update version to 3.0.0 in __init__.py
- [ ] 7.2.4: Update version in commands.py
- [ ] 7.2.5: Commit all changes
- [ ] 7.2.6: Tag v3.0.0
- [ ] 7.2.7: Run final verification checklist

**Total**: 60 bite-sized tasks

---

## Timeline & Effort Estimates

### Optimistic Scenario (9.5 hours)
- Wave 5: 2.5h (everything works first try)
- Wave 6: 3h (no integration bugs)
- Wave 7: 4h (tests pass immediately)

**Probability**: 20%

### Realistic Scenario (12 hours)
- Wave 5: 3h (orchestrator debugging)
- Wave 6: 4h (command integration bugs)
- Wave 7: 5h (test failures, fixes)

**Probability**: 60%
**Recommended Planning Basis**

### Conservative Scenario (14 hours)
- Wave 5: 3.5h (complex orchestrator issues)
- Wave 6: 5h (many integration bugs)
- Wave 7: 5.5h (extensive test failures)

**Probability**: 20%
**Worst Case Buffer**

**Recommendation**: Plan for **12 hours** (1.5 work days), have 14-hour buffer available.

---

## Critical Path

**Longest Dependency Chain**:
1. Wave 5 Agent 2: Build Orchestrator (2h)
2. Wave 6 Agent 3: Implement 9 commands (3h)
3. Wave 7 Agent 1: Integration testing (3h)
4. Wave 7 Agent 2: Deployment (1h)

**Total Critical Path**: 9 hours minimum

**With Realistic Debugging**: 12 hours

---

## Validation Gates (Prevent Overclaiming)

### Wave 5 Gate
**Before proceeding to Wave 6**:
- [ ] Pytest deleted: `ls tests/` returns "No such file"
- [ ] Orchestrator importable: `python -c "from shannon.orchestrator import ContextAwareOrchestrator"`
- [ ] Functional test framework: `tests/functional/run_all.sh` exists
- [ ] At least 1 test passing

**If any fail**: STOP, fix Wave 5 before continuing

### Wave 6 Gate
**Before proceeding to Wave 7**:
- [ ] Command count: `grep "@cli.command" src/shannon/cli/commands.py | wc -l` = 36
- [ ] shannon analyze shows live metrics (run and observe)
- [ ] Cache works: Run shannon analyze twice, second is instant
- [ ] shannon cache stats returns data
- [ ] shannon onboard . completes without errors
- [ ] shannon analytics returns data

**If any fail**: STOP, fix Wave 6 before continuing

### Wave 7 Gate (FINAL)
**Before declaring complete**:
- [ ] Functional tests: `tests/functional/run_all.sh` exits 0
- [ ] Pass rate: >90% of tests passing
- [ ] All 36 commands tested
- [ ] Workflows tested end-to-end
- [ ] README accurate (no false claims)
- [ ] CHANGELOG complete
- [ ] v3.0.0 tagged
- [ ] Quick verification: 5 commands work manually

**If any fail**: Return to appropriate wave for fixes

**Only After ALL Gates Pass**: Declare Shannon CLI V3.0 Complete

---

## Success Metrics

### Quantitative Targets

- [ ] **36 commands functional** (currently 18)
- [ ] **0 pytest tests** (currently 171)
- [ ] **1 ContextAwareOrchestrator** (currently 0)
- [ ] **>90% functional test pass rate**
- [ ] **100% completion** (honest measurement)

### Qualitative Validation

**User Can**:
- [ ] Run shannon analyze and see live metrics dashboard
- [ ] Press Enter to toggle detailed view
- [ ] Run analyze twice and get instant cache hit
- [ ] Run shannon onboard . and index codebase
- [ ] Run shannon analytics and see historical data
- [ ] Run shannon cache stats and see savings
- [ ] Execute complete workflow: setup → onboard → analyze → wave

**System Can**:
- [ ] Coordinate all 8 V3 modules via orchestrator
- [ ] Flow context through operations
- [ ] Degrade gracefully if subsystem fails
- [ ] Record analytics for all operations
- [ ] Optimize cost via model selection
- [ ] Auto-install recommended MCPs

---

## Risk Assessment

### High Risks

**Risk 1: Orchestrator Integration Complexity**
- Probability: 40%
- Impact: +2-4 hours
- Mitigation: Incremental implementation, graceful degradation, extensive testing

**Risk 2: Command Implementation Bugs**
- Probability: 60%
- Impact: +1-2 hours
- Mitigation: Test each command immediately, functional tests catch issues

**Risk 3: Time Estimate Optimism**
- Probability: 50%
- Impact: +2-3 hours
- Mitigation: 25% buffer, track actual time, adjust estimates

### Medium Risks

**Risk 4: Functional Test Coverage**
- Probability: 30%
- Impact: +1 hour
- Mitigation: Prioritize critical tests, iterate

**Risk 5: Documentation Accuracy**
- Probability: 20%
- Impact: +0.5 hour
- Mitigation: Test all examples before documenting

---

## Quality Assurance

### Definition of "Complete"

**Complete means**:
- ✅ All 36 commands WORK (can run, produce correct output)
- ✅ V3 features ACCESSIBLE (cache hits, metrics show, analytics records)
- ✅ ContextAwareOrchestrator COORDINATES operations
- ✅ Functional tests PASS (bash scripts, not pytest)
- ✅ Documentation ACCURATE (describes working features)
- ✅ No CRITICAL bugs

**Complete does NOT mean**:
- ❌ Modules exist but aren't used
- ❌ Commands imported but crash
- ❌ Tests exist but use wrong framework
- ❌ Documentation describes non-functional features
- ❌ "Components built but not integrated"

### Verification Checklist (Before Claiming Complete)

**Run These Commands**:
```bash
# 1. No pytest
grep -r "pytest" . --include="*.py" | wc -l
# Must return: 0

# 2. Command count
grep "@cli.command" src/shannon/cli/commands.py | wc -l
# Must return: 36

# 3. Orchestrator exists
python -c "from shannon.orchestrator import ContextAwareOrchestrator; print('✓')"
# Must print: ✓

# 4. Analyze works with V3
shannon analyze simple_spec.md
# Must show: Live metrics dashboard

# 5. Cache works
shannon analyze simple_spec.md
# Must be: Instant (cache hit)

# 6. Functional tests pass
tests/functional/run_all.sh
# Must exit: 0 (>90% pass rate)

# 7. All commands exist
shannon --help
# Must list: All 36 commands including onboard, context, cache, etc.
```

**Only if ALL 7 pass**: Declare complete

---

## Implementation Notes

### ContextAwareOrchestrator Key Design

**Purpose**: Make all V3 features work together, not in isolation

**Pattern**:
Every operation flows through orchestrator:
```
User Command
    ↓
ContextAwareOrchestrator
    ├─> Load context (ContextManager)
    ├─> Check cache (CacheManager)
    ├─> Optimize cost (CostOptimizer)
    ├─> Run with metrics (MetricsCollector)
    ├─> Recommend MCPs (MCPManager)
    ├─> Track agents (AgentStateTracker)
    ├─> Record analytics (HistoricalAnalytics)
    └─> Execute via SDK
    ↓
Result (cached, tracked, optimized, contextualized)
```

**Error Handling**:
```python
# Graceful degradation
try:
    cached = self.cache.get(spec, context)
except Exception as e:
    logger.warning(f"Cache failed: {e}")
    cached = None  # Continue without cache
```

### Functional Testing Philosophy

**Shannon CLI testing = Running Shannon CLI**:
- Don't import internal modules
- Run actual commands via subprocess
- Verify actual user experience
- Test complete workflows

**Example**:
```bash
# CORRECT: Test user behavior
shannon analyze spec.md --json > result.json
jq -e '.complexity_score' result.json

# WRONG: Test internal implementation
python -c "from shannon.cache import AnalysisCache; AnalysisCache().get('spec')"
```

---

## Execution Strategy

**Recommended Approach**: Wave-based with parallelization

**Wave 5**: 3 agents parallel (max duration: 2.5h)
**Wave 6**: 3 agents parallel (max duration: 3h)
**Wave 7**: 2 agents sequential (total: 4h)

**Total with Parallelization**: 9.5-12 hours
**vs Sequential**: 16.5 hours
**Speedup**: 1.4-1.7x

**Benefits of Waves**:
- Faster completion (parallelization)
- Clear validation gates
- Modular progress tracking
- Easy to pause/resume

---

## Post-Completion Actions

**After Wave 7 Gate Passes**:
1. Run `/shannon:reflect` again
   - Should show 100% completion
   - Verify no gaps remain

2. Save to Serena MCP:
   ```python
   mcp__serena__write_memory(
       "shannon_cli_v3_final_completion",
       "Shannon CLI V3.0 - 100% complete, all features functional"
   )
   ```

3. Update completion memories
4. Notify user of completion
5. Provide quick start guide

---

## Summary

**Current State**: 41% (modules exist, not integrated)
**Target State**: 100% (36 commands working, fully integrated)
**Gap**: 59% (orchestrator + commands + integration + testing)
**Timeline**: 12-14 hours (2 work days)
**Strategy**: 3 waves with parallelization
**Confidence**: HIGH (clear plan, realistic estimates, validation gates)

**Critical Success Factors**:
1. Build ContextAwareOrchestrator first (enables everything)
2. Wire V3 into analyze to prove integration works
3. Implement commands systematically
4. Use functional tests (bash scripts, NO pytest)
5. Validate at every gate (prevent overclaiming)

**Next Action**: Execute Wave 5 (Correction) to fix pytest issue and build orchestrator.

---

**Plan Status**: ✅ READY FOR EXECUTION