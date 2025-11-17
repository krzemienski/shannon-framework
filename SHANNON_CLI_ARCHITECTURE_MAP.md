# Shannon CLI Architecture Map

**Date**: 2025-11-17
**Version**: V5 Analysis
**Purpose**: Complete architectural analysis for cleanup planning

---

## Executive Summary

Shannon CLI has evolved through multiple versions (V3 → V4 → V5), resulting in **4 different orchestrator implementations** with overlapping responsibilities and significant technical debt. The codebase contains **125 Python files** with extensive version mixing, archived code still being imported, and unclear command-to-orchestrator mappings.

### Critical Findings

1. **Multiple Orchestrators** - 4 different orchestrators with unclear boundaries
2. **Version Mixing** - V3, V4, V5, and V3.5 components intermingled
3. **Dead Code** - Archived skills framework still present (not used in V5)
4. **Import Confusion** - Commands import from multiple orchestrator locations
5. **Duplication** - V3 subsystems duplicated in UnifiedOrchestrator initialization

---

## 1. Orchestrator Analysis

### 1.1 The Four Orchestrators

#### **ContextAwareOrchestrator** (V3)
- **Location**: `/Users/nick/Desktop/shannon-cli/src/shannon/orchestrator.py`
- **Version**: V3 (Wave 5 - Integration Layer)
- **Purpose**: Central integration hub for 8 V3 subsystems
- **Key Features**:
  - Context-aware analysis
  - Multi-tier caching
  - Cost optimization
  - MCP recommendations
  - Analytics recording
  - Agent state tracking
  - Live metrics dashboard

**Subsystems Managed** (8 total):
1. ContextManager - Project context loading
2. CacheManager - Multi-tier caching
3. MCPManager - MCP server recommendations
4. AgentStateTracker + AgentController - Agent monitoring
5. ModelSelector + CostEstimator + BudgetEnforcer - Cost optimization
6. AnalyticsDatabase + TrendAnalyzer + InsightsGenerator - Historical analytics
7. MetricsCollector - Live metrics
8. AgentPool - Parallel execution

**Methods**:
- `execute_analyze()` - 8D complexity analysis
- `execute_wave()` - Wave-based implementation
- `execute_task()` - Combined analyze + wave

**Status**: ✅ **ACTIVE** - Used by multiple commands

---

#### **UnifiedOrchestrator** (V5)
- **Location**: `/Users/nick/Desktop/shannon-cli/src/shannon/unified_orchestrator.py`
- **Version**: V5 Consolidation Layer
- **Purpose**: Facade pattern consolidating V3 and V4 capabilities
- **Architecture**: Delegates to ContextAwareOrchestrator but creates own subsystem instances

**Key Issues**:
- **Duplicates V3 subsystems**: Initializes CacheManager, ContextManager, etc. even though ContextAwareOrchestrator already has them
- **Shared subsystem injection**: Lines 180-189 inject shared instances into V3 orchestrator, overriding its own
- **Duplicate execute_task()**: Has TWO `execute_task()` methods (lines 298-326 and 328-383)
- **Removed V4 skills framework**: Comments indicate V4 custom skills framework removed in favor of Claude Code skills

**Methods**:
- `execute_analysis()` - Delegates to ContextAwareOrchestrator
- `execute_wave()` - Delegates to ContextAwareOrchestrator
- `execute_task()` - TWO DEFINITIONS (bug!)
- `_first_time_workflow()` - Auto-onboarding on first use
- `_returning_workflow()` - Cached context on return

**V5 Intelligence Features**:
- Context detection (first time vs returning)
- Auto-onboarding via ContextManager
- Validation gate detection
- Project config persistence

**Status**: ✅ **ACTIVE** - Primary orchestrator for V5

---

#### **Orchestrator** (V4)
- **Location**: `/Users/nick/Desktop/shannon-cli/src/shannon/orchestration/orchestrator.py`
- **Purpose**: Skill execution orchestration with checkpoints
- **Architecture**: Sequential skill execution with state management

**Features**:
- Checkpoint creation via StateManager
- HALT/RESUME execution control
- Rollback support
- WebSocket event streaming
- Dashboard integration

**Dependencies**:
- SkillExecutor - Executes skills from SkillRegistry
- StateManager - Creates/restores checkpoints
- ExecutionPlan - Defines skill sequence
- DashboardEventClient - Real-time streaming

**Methods**:
- `execute()` - Run complete plan
- `halt()` - Pause execution
- `resume()` - Resume from halt
- `rollback()` - Restore checkpoint

**Status**: ⚠️ **QUESTIONABLE** - References SkillExecutor and SkillRegistry which may be archived

---

#### **ResearchOrchestrator** (Wave 9)
- **Location**: `/Users/nick/Desktop/shannon-cli/src/shannon/research/orchestrator.py`
- **Version**: Wave 9 - Ultrathink & Research
- **Purpose**: Multi-source research coordination
- **Features**:
  - Web search via Tavily MCP
  - Documentation scraping via FireCrawl MCP
  - Library docs via Context7 MCP
  - Knowledge synthesis

**Methods**:
- `research()` - Conduct multi-source research
- `gather_from_web()` - Tavily search
- `gather_from_firecrawl()` - Website crawling
- `get_library_docs()` - Context7 lookup
- `synthesize_knowledge()` - Combine findings

**Status**: ✅ **ACTIVE** - Used by `shannon research` command

---

### 1.2 Orchestrator Comparison Matrix

| Orchestrator | Version | Primary Purpose | Key Dependencies | Active? |
|--------------|---------|-----------------|------------------|---------|
| **ContextAwareOrchestrator** | V3 | Integration hub for 8 subsystems | All V3 subsystems | ✅ Yes |
| **UnifiedOrchestrator** | V5 | V3+V4 facade | ContextAwareOrchestrator | ✅ Yes |
| **Orchestrator** | V4 | Skill execution | SkillExecutor, StateManager | ⚠️ Unclear |
| **ResearchOrchestrator** | Wave 9 | Research coordination | MCP servers | ✅ Yes |

---

## 2. Command-to-Orchestrator Mapping

### 2.1 CLI Command Inventory

Total commands found: **20+** (from line numbers in commands.py)

### 2.2 Command Flow Analysis

#### **`shannon do`** (V5 Command)
- **File**: `/Users/nick/Desktop/shannon-cli/src/shannon/cli/v4_commands/do.py`
- **Orchestrator**: UnifiedOrchestrator
- **Flow**:
  ```
  shannon do "task"
    ↓
  UnifiedOrchestrator.execute_task()
    ↓
  First time: _first_time_workflow()
    - context.onboard_project() (auto-explore)
    - _ask_validation_gates() (ask user)
    - _save_project_config() (persist)
    - _execute_with_context() (run with context)

  Returning: _returning_workflow()
    - context.load_project() (< 1s)
    - Check for changes
    - _execute_with_context() (run with cached context)
    ↓
  SDK invokes 'task-automation' Claude Code skill
    (from Shannon Framework plugin)
  ```

**Key Insight**: V5 `shannon do` uses **Claude Code skills** from Shannon Framework, NOT custom skills framework.

---

#### **`shannon analyze`**
- **File**: `/Users/nick/Desktop/shannon-cli/src/shannon/cli/commands.py` (line 118)
- **Orchestrator**: UnifiedOrchestrator (in V5 mode) OR SDK direct (in test mode)
- **Flow**:
  ```
  shannon analyze spec.md
    ↓
  Check if running in Claude Code (direct mode)
  If yes:
    Print spec, ask Claude to analyze directly
  If no:
    UnifiedOrchestrator.execute_analysis()
      ↓
    ContextAwareOrchestrator.execute_analyze()
      ↓
    SDK invokes 'spec-analysis' skill
  ```

---

#### **`shannon wave`**
- **File**: `/Users/nick/Desktop/shannon-cli/src/shannon/cli/commands.py` (line 632)
- **Orchestrator**: UnifiedOrchestrator
- **Flow**:
  ```
  shannon wave "implement X"
    ↓
  UnifiedOrchestrator.execute_wave()
    ↓
  ContextAwareOrchestrator.execute_wave()
    ↓
  SDK invokes 'wave-orchestration' skill
    ↓
  AgentStateTracker records agent states
  ```

---

#### **`shannon exec`**
- **File**: `/Users/nick/Desktop/shannon-cli/src/shannon/cli/commands.py` (line 1317)
- **Orchestrator**: CompleteExecutor (from executor module)
- **Flow**:
  ```
  shannon exec "task"
    ↓
  CompleteExecutor (V3.5 enhancement layer)
    ↓
  Orchestrates Shannon Framework skills:
    - /shannon:prime (context)
    - /shannon:analyze (understanding)
    - /shannon:wave (execution)
    ↓
  Wraps with:
    - LibraryDiscoverer
    - ValidationOrchestrator
    - GitManager
  ```

**Key Insight**: `shannon exec` is V3.5 autonomous executor, different from `shannon do`

---

#### **`shannon research`**
- **File**: `/Users/nick/Desktop/shannon-cli/src/shannon/cli/commands.py` (line 1638)
- **Orchestrator**: ResearchOrchestrator
- **Flow**:
  ```
  shannon research "query"
    ↓
  ResearchOrchestrator.research()
    ↓
  Parallel gathering:
    - Tavily MCP (web search)
    - FireCrawl MCP (documentation)
    - Context7 MCP (library docs)
    ↓
  synthesize_knowledge()
  ```

---

#### **Other Commands** (use ContextAwareOrchestrator directly)

Commands importing ContextAwareOrchestrator:
- `shannon onboard` (line 1823)
- `shannon prime` (line 1928)
- `shannon update-context` (line 1975)
- `shannon discover` (line 2028)
- `shannon scan` (line 2073)
- `shannon validate-context` (line 2115)
- `shannon export-context` (line 2158)

All use `ContextAwareOrchestrator()` directly without UnifiedOrchestrator wrapper.

---

### 2.3 Command Orchestrator Matrix

| Command | Orchestrator | Version | Status |
|---------|--------------|---------|--------|
| `shannon do` | UnifiedOrchestrator | V5 | ✅ Active |
| `shannon analyze` | UnifiedOrchestrator → ContextAwareOrchestrator | V5/V3 | ✅ Active |
| `shannon wave` | UnifiedOrchestrator → ContextAwareOrchestrator | V5/V3 | ✅ Active |
| `shannon exec` | CompleteExecutor | V3.5 | ✅ Active |
| `shannon research` | ResearchOrchestrator | Wave 9 | ✅ Active |
| `shannon onboard` | ContextAwareOrchestrator | V3 | ✅ Active |
| `shannon prime` | ContextAwareOrchestrator | V3 | ✅ Active |
| Context commands (6) | ContextAwareOrchestrator | V3 | ✅ Active |

---

## 3. Version Component Classification

### 3.1 V3 Components (Wave 5 Integration)

**Core Orchestrator**:
- `orchestrator.py` - ContextAwareOrchestrator ✅

**8 V3 Subsystems** (all active):

1. **Context Management**:
   - `context/manager.py` - ContextManager ✅
   - `context/loader.py` - ContextLoader ✅
   - `context/onboarder.py` - ProjectOnboarder ✅
   - `context/primer.py` - ContextPrimer ✅
   - `context/updater.py` - ContextUpdater ✅
   - `context/serena_adapter.py` - SerenaAdapter ✅

2. **Cache System**:
   - `cache/manager.py` - CacheManager ✅
   - `cache/analysis_cache.py` - AnalysisCache ✅
   - `cache/command_cache.py` - CommandCache ✅
   - `cache/mcp_cache.py` - MCPCache ✅

3. **Analytics & Trends**:
   - `analytics/database.py` - AnalyticsDatabase ✅
   - `analytics/trends.py` - TrendAnalyzer ✅
   - `analytics/insights.py` - InsightsGenerator ✅

4. **Cost Optimization**:
   - `optimization/model_selector.py` - ModelSelector ✅
   - `optimization/cost_estimator.py` - CostEstimator ✅
   - `optimization/budget_enforcer.py` - BudgetEnforcer ✅

5. **MCP Integration**:
   - `mcp/manager.py` - MCPManager ✅
   - `mcp/detector.py` - MCPDetector ✅
   - `mcp/installer.py` - MCPInstaller ✅
   - `mcp/verifier.py` - MCPVerifier ✅

6. **Agent Tracking**:
   - `agents/state_tracker.py` - AgentStateTracker ✅
   - `agents/controller.py` - AgentController ✅
   - `agents/message_router.py` - MessageRouter ✅

7. **Metrics & Dashboard**:
   - `metrics/collector.py` - MetricsCollector ✅
   - `metrics/dashboard.py` - LiveDashboard ✅
   - `metrics/keyboard.py` - KeyboardHandler ✅
   - `ui/dashboard_v31/*` - V3.1 Dashboard (9 files) ✅

8. **SDK & Integration**:
   - `sdk/client.py` - ShannonSDKClient ✅
   - `sdk/message_parser.py` - MessageParser ✅
   - `sdk/interceptor.py` - MessageInterceptor ✅

**Status**: All V3 subsystems are **active** and used by ContextAwareOrchestrator

---

### 3.2 V3.5 Components (Autonomous Executor)

**Executor Module** (`executor/`):
- `complete_executor.py` - CompleteExecutor ✅
- `prompt_enhancer.py` - PromptEnhancer ✅
- `library_discoverer.py` - LibraryDiscoverer ✅
- `git_manager.py` - GitManager ✅
- `validator.py` - ValidationOrchestrator ✅
- `multi_file_executor.py` - MultiFileExecutor ✅
- `code_executor.py` - CodeExecutor ✅
- `simple_executor.py` - SimpleExecutor ✅
- `task_enhancements.py` - Task enhancement utilities ✅
- `prompts.py` - Prompt templates ✅
- `models.py` - Data models ✅

**Purpose**: Enhancement layer on Shannon Framework
- Used by `shannon exec` command
- Adds library discovery, validation, git integration
- Orchestrates Shannon Framework skills

**Status**: ✅ **ACTIVE** - Separate from V4/V5, used by exec command

---

### 3.3 V4 Components (Skills Framework - ARCHIVED)

**⚠️ CRITICAL FINDING**: V4 custom skills framework is **REMOVED IN V5**

**Location**: `orchestration/` directory

**V4 Infrastructure** (likely inactive):
- `orchestration/orchestrator.py` - Skill execution orchestrator ⚠️
- `orchestration/planner.py` - ExecutionPlanner ⚠️ (NOT FOUND - may be deleted)
- `orchestration/state_manager.py` - StateManager ✅ (kept for checkpoints)
- `orchestration/agent_pool.py` - AgentPool ✅ (kept for parallel execution)

**V4 Agents** (9 files in `orchestration/agents/`):
- `base.py` - Base agent class ⚠️
- `analysis.py` - Analysis agent ⚠️
- `planning.py` - Planning agent ⚠️
- `git.py` - Git agent ⚠️
- `research.py` - Research agent ⚠️
- `testing.py` - Testing agent ⚠️
- `validation.py` - Validation agent ⚠️
- `monitoring.py` - Monitoring agent ⚠️

**Skills Framework** (ARCHIVED):
- `_archived/skills_custom_framework/` - Complete V4 skills system ❌
  - `registry.py` - SkillRegistry
  - `executor.py` - SkillExecutor
  - `loader.py` - SkillLoader
  - `generator.py` - SkillGenerator
  - `catalog.py` - SkillCatalog
  - `dependencies.py` - DependencyResolver
  - `pattern_detector.py` - PatternDetector
  - `performance.py` - PerformanceMonitor
  - Plus 3 more files

**Why Archived**: UnifiedOrchestrator comments (lines 196-215) state:
```python
"""Initialize V4-specific components (not custom skills framework).

V5: Removed custom skills framework (SkillRegistry, Planner, Executor).
Shannon V5 uses Shannon Framework Claude Code skills instead.

Keeping only:
- StateManager: For execution checkpoints
"""
```

**Status**: ❌ **ARCHIVED** - V4 custom skills replaced by Claude Code skills

---

### 3.4 V5 Components (Unified Layer)

**Primary**:
- `unified_orchestrator.py` - UnifiedOrchestrator ✅
- `cli/v4_commands/do.py` - V5 do command ✅

**V5 Architecture**:
- Facade pattern over V3 ContextAwareOrchestrator
- Delegates to Shannon Framework Claude Code skills
- Adds intelligent context-aware workflows:
  - First-time auto-onboarding
  - Cached context on return
  - Validation gate detection

**Kept from V4**:
- `orchestration/state_manager.py` - StateManager ✅
- `orchestration/agent_pool.py` - AgentPool ✅

**Status**: ✅ **ACTIVE** - Primary architecture for V5

---

### 3.5 Wave 9 Components (Research & Ultrathink)

**Research System**:
- `research/orchestrator.py` - ResearchOrchestrator ✅

**Ultrathink Mode**:
- `modes/ultrathink.py` - Ultrathink mode ✅

**Debug Mode**:
- `modes/debug_mode.py` - Debug mode ✅
- `modes/investigation.py` - Investigation mode ✅

**Status**: ✅ **ACTIVE** - Used by research command

---

### 3.6 Shared Infrastructure (All Versions)

**Configuration**:
- `config.py` - ShannonConfig ✅
- `setup/wizard.py` - Setup wizard ✅
- `setup/framework_detector.py` - Framework detection ✅

**Session Management**:
- `core/session_manager.py` - SessionManager ✅

**Storage**:
- `storage/models.py` - Data models ✅

**UI Components**:
- `ui/progress.py` - ProgressUI ✅
- `ui/formatters.py` - OutputFormatter ✅

**Communication**:
- `communication/dashboard_client.py` - DashboardEventClient ✅

**Server** (WebSocket dashboard):
- `server/websocket.py` - WebSocket server ✅

**Status**: ✅ **ACTIVE** - Used across all versions

---

## 4. Technical Debt Report

### 4.1 Critical Issues

#### **Issue #1: Duplicate execute_task() Method**
- **File**: `unified_orchestrator.py`
- **Lines**: 298-326 AND 328-383
- **Impact**: Second definition overwrites first
- **Severity**: 🔴 **CRITICAL** - Runtime bug
- **Fix**: Remove first definition (lines 298-326), it's simpler delegation

---

#### **Issue #2: Subsystem Duplication**
- **File**: `unified_orchestrator.py`
- **Problem**: Initializes own instances of V3 subsystems (lines 98-154) then injects them into ContextAwareOrchestrator (lines 180-189)
- **Impact**: Double initialization, wasted resources
- **Why**: UnifiedOrchestrator could just use ContextAwareOrchestrator's subsystems
- **Severity**: 🟡 **MEDIUM** - Inefficient but works
- **Fix**: Either:
  1. Create ContextAwareOrchestrator first, use its subsystems
  2. Don't create ContextAwareOrchestrator at all, implement directly

---

#### **Issue #3: V4 Skills Framework References**
- **File**: `orchestration/orchestrator.py`
- **Problem**: References `SkillExecutor` and `SkillRegistry` which are in archived directory
- **Impact**: May not be functional, unclear if used
- **Severity**: 🟡 **MEDIUM** - Unclear status
- **Fix**: Determine if V4 Orchestrator is used:
  - If YES: Update to work without skills framework
  - If NO: Archive or delete

---

#### **Issue #4: Archived Code Import Risk**
- **Search Result**: No imports from `_archived` found
- **Good News**: Archived code is properly isolated
- **Severity**: ✅ **NONE** - No issue found

---

### 4.2 Unused/Dead Code

#### **Definitely Unused** (Safe to Archive/Delete):

1. **V4 Custom Skills Framework** (already archived):
   - `_archived/skills_custom_framework/*` (12 files)
   - Already in archived directory ✅

2. **V4 Agents** (likely unused, need verification):
   - `orchestration/agents/*.py` (9 files)
   - References SkillExecutor which is archived
   - **Action**: Verify no imports, then archive

3. **V4 Planner** (missing):
   - Referenced in V4 Orchestrator but file not found
   - **Action**: Remove references or restore file

---

#### **Possibly Unused** (Needs Investigation):

1. **V4 Orchestrator**:
   - `orchestration/orchestrator.py`
   - Not imported in CLI commands
   - References archived SkillExecutor
   - **Action**: Search all files for imports

2. **Some Executor Components**:
   - `executor/simple_executor.py` - May be superseded by CompleteExecutor
   - `executor/code_executor.py` - May be unused
   - **Action**: Check imports and usage

3. **UI Dashboard V3.1** (9 files):
   - `ui/dashboard_v31/*`
   - Listed as "V3.1" but V5 is current
   - May be replaced by web dashboard
   - **Action**: Check if still used by LiveDashboard

---

### 4.3 Code Duplication

#### **Duplication #1: Orchestrator Initialization**
- **Where**: ContextAwareOrchestrator and UnifiedOrchestrator both initialize same subsystems
- **Lines**:
  - `orchestrator.py`: 62-124
  - `unified_orchestrator.py`: 98-154
- **Impact**: Same code in two places
- **Fix**: Single source of truth

#### **Duplication #2: Context Workflows**
- **Where**: UnifiedOrchestrator has context loading logic, but ContextManager also has it
- **Impact**: Business logic duplication
- **Fix**: Move workflow logic to ContextManager

---

### 4.4 Import Confusion

#### **Multiple Orchestrator Imports**:

Commands import from 3 different locations:
1. `from shannon.orchestrator import ContextAwareOrchestrator`
2. `from shannon.unified_orchestrator import UnifiedOrchestrator`
3. `from shannon.orchestration.orchestrator import Orchestrator` (unused?)

**Problem**: Unclear which orchestrator to use for new commands

**Fix**: Standardize on UnifiedOrchestrator as single entry point

---

### 4.5 Version Mixing Examples

#### **Example #1**: analyze command
```python
# Uses V5 UnifiedOrchestrator
orchestrator = UnifiedOrchestrator(config)
  ↓
# Which delegates to V3 ContextAwareOrchestrator
result = self.v3_orchestrator.execute_analyze()
  ↓
# Which uses V3 subsystems
self.cache.analysis.get()
```

**Issue**: 3 versions in one call chain

---

#### **Example #2**: Context commands
```python
# Bypass UnifiedOrchestrator entirely, go direct to V3
from shannon.orchestrator import ContextAwareOrchestrator
orchestrator = ContextAwareOrchestrator()
```

**Issue**: Some commands use V5, others skip it

---

## 5. Module Dependency Graph

### 5.1 High-Level Architecture

```
CLI Commands (commands.py + v4_commands/do.py)
    ↓
┌───────────────────────────────────────────┐
│ UnifiedOrchestrator (V5)                  │
│ - Facade pattern                          │
│ - Intelligent workflows                   │
└───────────────┬───────────────────────────┘
                ↓
┌───────────────────────────────────────────┐
│ ContextAwareOrchestrator (V3)             │
│ - 8 Subsystem Integration                 │
└───────────────┬───────────────────────────┘
                ↓
        ┌───────┴───────┐
        ↓               ↓
┌──────────────┐  ┌─────────────────┐
│ V3 Subsystems│  │ Shannon Framework│
│ (8 modules)  │  │ via SDK Client  │
└──────────────┘  └─────────────────┘
```

**Parallel Paths**:
- `shannon exec` → CompleteExecutor (V3.5) → Shannon Framework
- `shannon research` → ResearchOrchestrator (Wave 9) → MCP servers

---

### 5.2 Subsystem Dependencies

**ContextAwareOrchestrator depends on**:
1. ContextManager (context/)
2. CacheManager (cache/)
3. MCPManager (mcp/)
4. AgentStateTracker + AgentController (agents/)
5. ModelSelector + CostEstimator + BudgetEnforcer (optimization/)
6. AnalyticsDatabase + TrendAnalyzer + InsightsGenerator (analytics/)
7. MetricsCollector + LiveDashboard (metrics/)
8. AgentPool (orchestration/agent_pool.py)
9. ShannonSDKClient (sdk/)

**UnifiedOrchestrator depends on**:
1. All of ContextAwareOrchestrator's dependencies (duplicated)
2. StateManager (orchestration/)
3. ContextAwareOrchestrator (orchestrator.py)

**CompleteExecutor depends on**:
1. PromptEnhancer (executor/)
2. LibraryDiscoverer (executor/)
3. ValidationOrchestrator (executor/)
4. GitManager (executor/)
5. ShannonSDKClient (sdk/)

---

### 5.3 Circular Dependencies

**None found** ✅

All dependencies flow downward in clear hierarchy.

---

### 5.4 Orphaned Modules (Nothing Imports Them)

**Candidates** (needs verification):
1. `orchestration/orchestrator.py` - V4 Orchestrator
2. `orchestration/agents/*.py` - V4 agent implementations
3. `executor/simple_executor.py` - May be superseded
4. `executor/code_executor.py` - May be unused

**Action**: Run grep to confirm no imports exist

---

## 6. Cleanup Recommendations

### 6.1 Immediate Critical Fixes

#### **Priority 1: Fix duplicate execute_task()**
```python
# File: unified_orchestrator.py
# Remove lines 298-326 (first execute_task definition)
# Keep lines 328-383 (intelligent context-aware version)
```

**Impact**: Fixes runtime bug
**Risk**: Low (second definition is correct one)

---

### 6.2 Short-Term Refactoring

#### **Priority 2: Eliminate Subsystem Duplication**

**Current**:
```python
UnifiedOrchestrator.__init__():
    self._initialize_shared_subsystems()  # Creates cache, context, etc.
    self._initialize_v3_components()      # Creates ContextAwareOrchestrator
    # Then injects shared into v3_orchestrator (lines 180-189)
```

**Recommended**:
```python
UnifiedOrchestrator.__init__():
    # Create V3 orchestrator first
    self.v3_orchestrator = ContextAwareOrchestrator(config)

    # Use its subsystems (don't duplicate)
    self.cache = self.v3_orchestrator.cache
    self.context = self.v3_orchestrator.context
    # etc.
```

**Impact**: Reduces initialization overhead, cleaner architecture
**Risk**: Low (just rearranging initialization order)

---

#### **Priority 3: Archive V4 Agents**

**Action**:
1. Verify no imports: `grep -r "from shannon.orchestration.agents" src/`
2. If none: Move `orchestration/agents/` to `_archived/v4_agents/`

**Files to Archive** (9 files):
- `orchestration/agents/base.py`
- `orchestration/agents/analysis.py`
- `orchestration/agents/planning.py`
- `orchestration/agents/git.py`
- `orchestration/agents/research.py`
- `orchestration/agents/testing.py`
- `orchestration/agents/validation.py`
- `orchestration/agents/monitoring.py`

**Keep**:
- `orchestration/agent_pool.py` (used by V5)

**Impact**: Reduces confusion, clarifies V5 architecture
**Risk**: Low if no imports found

---

#### **Priority 4: Archive or Fix V4 Orchestrator**

**Decision Point**: Is `orchestration/orchestrator.py` used?

**Test**:
```bash
grep -r "from shannon.orchestration.orchestrator" src/
grep -r "from shannon.orchestration import.*Orchestrator" src/
```

**If NO imports found**:
- Move to `_archived/v4_orchestrator.py`
- Document as "Skills framework orchestrator (V4), replaced by Claude Code skills in V5"

**If YES imports found**:
- Update to work without SkillExecutor/SkillRegistry
- Or replace with UnifiedOrchestrator

**Impact**: Clarifies active orchestrators
**Risk**: Medium (need to verify no hidden usage)

---

### 6.3 Medium-Term Architecture Improvements

#### **Improvement 1: Standardize Command Entry Point**

**Current**: Commands import from 3 different places:
- `from shannon.orchestrator import ContextAwareOrchestrator` (6 commands)
- `from shannon.unified_orchestrator import UnifiedOrchestrator` (4 commands)
- Direct executor imports (exec command)

**Recommended**: All commands through UnifiedOrchestrator
```python
# Single import for all commands
from shannon.unified_orchestrator import UnifiedOrchestrator

# Let UnifiedOrchestrator delegate internally
orchestrator = UnifiedOrchestrator(config)
result = orchestrator.execute_XXX()
```

**Impact**: Clearer architecture, single entry point
**Risk**: Low (just changing imports)

---

#### **Improvement 2: Extract Context Workflows**

**Current**: UnifiedOrchestrator has business logic for workflows (first-time, returning)

**Better**: Move to ContextManager
```python
# Instead of this in UnifiedOrchestrator:
async def _first_time_workflow(...)
async def _returning_workflow(...)

# Do this in ContextManager:
class ContextManager:
    async def ensure_context(project_id, project_path):
        """Smart context loading with auto-onboarding."""
        if not self.project_exists(project_id):
            return await self.onboard_project(...)
        else:
            return await self.load_project(project_id)
```

**Impact**: Better separation of concerns
**Risk**: Low (just moving code)

---

#### **Improvement 3: Consolidate Executor Module**

**Current**: 11 files in executor/, some may be unused

**Action**:
1. Check usage of each file
2. Consolidate into fewer files
3. Keep clear API

**Possible Structure**:
```
executor/
  __init__.py
  complete_executor.py  # Main executor
  enhancers.py          # PromptEnhancer, LibraryDiscoverer
  validators.py         # ValidationOrchestrator
  git.py                # GitManager
  models.py             # Data models
```

**Impact**: Cleaner module structure
**Risk**: Medium (need careful refactoring)

---

### 6.4 Long-Term Architectural Vision

#### **Vision: Three Clear Layers**

```
┌────────────────────────────────────────┐
│ CLI Layer (commands.py)                │
│ - User interface                       │
│ - Argument parsing                     │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ Orchestration Layer                    │
│ - UnifiedOrchestrator (single entry)   │
│ - Context workflows                    │
│ - Task routing                         │
└────────────┬───────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│ Execution Layer                        │
│ - V3 Subsystems (intelligence)         │
│ - Shannon Framework (Claude Code)      │
│ - MCP Servers (research)               │
└────────────────────────────────────────┘
```

**Benefits**:
- Clear separation of concerns
- Single entry point (UnifiedOrchestrator)
- Easy to test each layer
- Obvious where new features go

---

## 7. Specific File Actions

### 7.1 Files to Archive

**Move to `_archived/` directory**:

1. **V4 Agents** (9 files):
   ```
   _archived/v4_agents/
     base.py
     analysis.py
     planning.py
     git.py
     research.py
     testing.py
     validation.py
     monitoring.py
   ```

2. **V4 Orchestrator** (if unused):
   ```
   _archived/v4_orchestrator.py
   ```

3. **Possibly Unused Executors**:
   ```
   _archived/executor_simple.py  (if unused)
   _archived/executor_code.py    (if unused)
   ```

---

### 7.2 Files to Fix

1. **unified_orchestrator.py**:
   - Remove duplicate execute_task() (lines 298-326)
   - Refactor subsystem initialization (lines 98-189)

2. **commands.py**:
   - Standardize orchestrator imports
   - Use UnifiedOrchestrator consistently

---

### 7.3 Files to Keep (Active)

**Core Orchestrators** (3):
- `orchestrator.py` - ContextAwareOrchestrator ✅
- `unified_orchestrator.py` - UnifiedOrchestrator ✅
- `research/orchestrator.py` - ResearchOrchestrator ✅

**V3 Subsystems** (8 modules, ~30 files):
- All files in: cache/, context/, analytics/, optimization/, mcp/, agents/, metrics/

**V3.5 Executor** (11 files):
- All files in: executor/

**V5 Infrastructure** (2 files):
- `orchestration/state_manager.py`
- `orchestration/agent_pool.py`

**Shared Infrastructure** (~15 files):
- config.py, core/, storage/, ui/, communication/, server/, setup/, sdk/

**Total Active Files**: ~70-80 files (out of 125)

---

## 8. Testing Strategy

### 8.1 Before Cleanup

**Verify Unused Status**:
```bash
# Check V4 Orchestrator usage
grep -r "from shannon.orchestration.orchestrator" src/
grep -r "Orchestrator" src/shannon/cli/ | grep -v "#"

# Check V4 Agents usage
grep -r "from shannon.orchestration.agents" src/
grep -r "orchestration.agents" src/

# Check Executor usage
grep -r "simple_executor\|code_executor" src/
```

**Document Findings**: Create `CLEANUP_VERIFICATION.md` with results

---

### 8.2 After Cleanup

**Test All Commands**:
```bash
shannon --help
shannon analyze docs/examples/spec.md
shannon wave "create hello world"
shannon do "create test file"
shannon exec "implement feature"
shannon research "topic"
shannon status
```

**Verify Imports**:
```bash
# No broken imports
python -c "from shannon.orchestrator import ContextAwareOrchestrator"
python -c "from shannon.unified_orchestrator import UnifiedOrchestrator"

# No imports from archived
! grep -r "from shannon._archived" src/ --include="*.py"
```

---

## 9. Summary

### 9.1 Key Findings

1. **4 Orchestrators**: Only 3 are active (ContextAwareOrchestrator, UnifiedOrchestrator, ResearchOrchestrator)
2. **V4 Skills Framework**: Archived, replaced by Claude Code skills in V5
3. **Version Mixing**: V3, V3.5, V5 all active, V4 partially archived
4. **Duplicate Code**: Subsystem initialization duplicated in UnifiedOrchestrator
5. **Critical Bug**: Duplicate execute_task() method
6. **Cleanup Potential**: ~40-50 files could be archived

---

### 9.2 Recommended Cleanup Order

**Phase 1 - Critical Fixes** (1 hour):
1. Fix duplicate execute_task() method
2. Verify V4 Orchestrator unused
3. Test all commands still work

**Phase 2 - Quick Wins** (2-3 hours):
1. Archive V4 agents (9 files)
2. Archive V4 orchestrator (if unused)
3. Verify no imports from archived
4. Test commands again

**Phase 3 - Refactoring** (1-2 days):
1. Eliminate subsystem duplication
2. Standardize command imports
3. Extract context workflows
4. Consolidate executor module

**Phase 4 - Polish** (1 day):
1. Update documentation
2. Create architecture diagrams
3. Write migration guide

---

### 9.3 Final Architecture (After Cleanup)

```
CLI Commands
    ↓
UnifiedOrchestrator (single entry point)
    ├─ ContextAwareOrchestrator (V3 intelligence)
    │   └─ 8 V3 Subsystems
    │
    ├─ CompleteExecutor (V3.5 autonomous)
    │   └─ Shannon Framework Skills
    │
    └─ ResearchOrchestrator (Wave 9)
        └─ MCP Servers (Tavily, FireCrawl, Context7)
```

**Result**: Clean, clear, maintainable architecture with obvious extension points.

---

## Appendix A: File Count by Module

| Module | Total Files | Active | Archived | Unclear |
|--------|-------------|--------|----------|---------|
| orchestration/ | 15 | 2 | 0 | 13 |
| executor/ | 11 | 11 | 0 | 0 |
| context/ | 6 | 6 | 0 | 0 |
| cache/ | 4 | 4 | 0 | 0 |
| analytics/ | 4 | 4 | 0 | 0 |
| optimization/ | 3 | 3 | 0 | 0 |
| mcp/ | 4 | 4 | 0 | 0 |
| agents/ | 3 | 3 | 0 | 0 |
| metrics/ | 3 | 3 | 0 | 0 |
| ui/ | 12 | 12 | 0 | 0 |
| sdk/ | 3 | 3 | 0 | 0 |
| cli/ | 5 | 5 | 0 | 0 |
| _archived/ | 14 | 0 | 14 | 0 |
| Other | 38 | 38 | 0 | 0 |
| **Total** | **125** | **98** | **14** | **13** |

---

## Appendix B: Import Graph

**Most Imported Modules** (dependencies):
1. `ShannonConfig` - 20+ files import
2. `ShannonSDKClient` - 15+ files import
3. `ContextManager` - 10+ files import
4. `CacheManager` - 8+ files import

**Least Imported** (candidates for archival):
1. `orchestration/agents/*` - 0 imports found
2. `orchestration/orchestrator.py` - 0 imports found (needs verification)

---

**End of Architecture Map**

*This document provides the foundation for informed cleanup decisions. All recommendations include risk assessments and verification steps.*
