# Shannon V3.5 Implementation Plan

**Generated**: 2025-11-15
**Based on**: SHANNON_V3.5_REVISED_SPEC.md
**Ultrathinking**: 60 sequential thoughts completed
**Status**: Ready for execution

---

## 🎯 Executive Summary

Shannon V3.5 is an **enhancement layer** on existing Shannon Framework that adds autonomous execution:

**What it adds**: ~2,500 lines of orchestration, validation, and git automation
**What it reuses**: ~15,000+ lines of existing Shannon infrastructure
**Timeline**: 10 days (8 implementation + 2 testing/docs)
**Result**: `shannon exec "anything"` → working code with validated commits

### Core Capabilities:
1. **System Prompt Enhancement**: Inject library discovery, validation, git workflow instructions
2. **Library Discovery**: Search npm/PyPI/CocoaPods instead of reinventing wheels
3. **3-Tier Validation**: Build + Tests + Functional validation before commits
4. **Git Automation**: Atomic commits per validated change with rollback
5. **Orchestration**: Wraps existing `/shannon:prime`, `/shannon:analyze`, `/shannon:wave` skills

### Architecture Principle:
**NOT** a separate system → **IS** an orchestration layer that makes Shannon autonomous

---

## Phase 0: Critical Assumption Validation 🔬

**Type**: Prototype & Risk Mitigation
**Duration**: 0.5 days (4 hours)
**Risk Level**: HIGH - Validates architecture viability

### Files Created:
- `tests/prototypes/test_system_prompt_append.py` (100 lines)
- `tests/prototypes/minimal_exec_skill.ts` (50 lines)
- `tests/prototypes/PROTOTYPE_RESULTS.md` (documentation)

### Tasks:
- [ ] **T0.1**: Research Claude Agent SDK `ClaudeAgentOptions.system_prompt` API
- [ ] **T0.2**: Create minimal test script that injects custom instructions
- [ ] **T0.3**: Create minimal Framework skill that echoes enhanced prompts
- [ ] **T0.4**: Document findings and path forward

### Verification Criteria:
- [ ] SDK documentation confirms `system_prompt.append` exists OR alternative identified
- [ ] Test script successfully injects custom instructions
- [ ] Agent response contains injected instructions
- [ ] Path forward is clear

### Exit Criteria:
- **Success**: system_prompt.append confirmed working → Proceed to Wave 1
- **Pivot**: append not available → Revise to skill-based injection → Modify Wave 1

**⚠️ CRITICAL**: DO NOT proceed past Phase 0 until validation completes.

---

## Wave 1: Enhanced System Prompts 📝

**Type**: Infrastructure
**Duration**: 1 day (8 hours)
**Dependencies**: Phase 0 success
**Files**: 7 files, ~650 lines

### Files Created/Modified:
- `src/shannon/executor/__init__.py` (10 lines) - NEW module
- `src/shannon/executor/models.py` (100 lines) - Data structures
- `src/shannon/executor/prompts.py` (250 lines) - Core prompt templates
- `src/shannon/executor/task_enhancements.py` (150 lines) - Project-specific prompts
- `src/shannon/executor/prompt_enhancer.py` (150 lines) - Prompt builder
- `src/shannon/sdk/client.py` (+50 lines) - Add append support
- `src/shannon/cli/commands.py` (+50 lines) - Stub exec command

### Tasks:
- [ ] **T1.1**: Create data models (LibraryRecommendation, ExecutionStep, ValidationCriteria, ExecutionPlan, ExecutionResult)
- [ ] **T1.2**: Create core prompt templates (LIBRARY_DISCOVERY, FUNCTIONAL_VALIDATION, GIT_WORKFLOW)
- [ ] **T1.3**: Create project-specific enhancements (iOS, React Native, React Web, Python FastAPI)
- [ ] **T1.4**: Create PromptEnhancer (build_enhancements, detect_project_type, generate_task_hints)
- [ ] **T1.5**: Modify ShannonSDKClient (invoke_with_enhancements method)
- [ ] **T1.6**: Create exec CLI command stub
- [ ] **T1.7**: Functional test (verify prompts build and inject correctly)

### Verification Criteria:
- [ ] All 5 data models defined with proper types
- [ ] All 3 core prompt templates complete (~600 lines)
- [ ] All 4 project-specific enhancements complete
- [ ] PromptEnhancer detects React/iOS/Python projects correctly
- [ ] SDK successfully injects enhanced prompts
- [ ] Test agent echoes back enhanced instructions
- [ ] `shannon exec "test"` runs without errors

### Exit Criteria:
Can build and inject enhanced system prompts for React/iOS/Python projects. Agent receives and acknowledges enhanced instructions.

---

## Wave 2: Library Discovery 🔍

**Type**: Integration
**Duration**: 2 days (16 hours)
**Dependencies**: Wave 1 complete
**Files**: 3 files, ~400 lines

### Files Created/Modified:
- `src/shannon/executor/library_discoverer.py` (250 lines)
- `src/shannon/cli/commands.py` (+100 lines) - `shannon discover-libs` command
- `tests/functional/test_wave2_library_discovery.sh` (50 lines)

### Tasks:
- [ ] **T2.1**: Implement LibraryDiscoverer base class
- [ ] **T2.2**: Implement npm registry search (firecrawl integration)
- [ ] **T2.3**: Implement PyPI registry search
- [ ] **T2.4**: Implement Swift Package Index search
- [ ] **T2.5**: Implement ranking algorithm (stars 40%, maintenance 30%, downloads 20%, license 10%)
- [ ] **T2.6**: Implement Serena caching (7-day TTL)
- [ ] **T2.7**: Create `shannon discover-libs` CLI command
- [ ] **T2.8**: Functional tests (React UI, Python jobs, verify caching)

### Verification Criteria:
- [ ] Can search npm/PyPI/Swift registries
- [ ] Ranking algorithm scores libraries correctly
- [ ] Serena caching works (second search <1s)
- [ ] CLI command displays ranked results
- [ ] Returns top 5 options per search

### Exit Criteria:
`shannon discover-libs "feature"` returns ranked library recommendations. Results cached in Serena.

---

## Wave 3: Validation Orchestrator ✅

**Type**: Testing Infrastructure
**Duration**: 2 days (16 hours)
**Dependencies**: Wave 1 complete
**Files**: 3 files, ~450 lines

### Files Created/Modified:
- `src/shannon/executor/validator.py` (300 lines)
- `src/shannon/cli/commands.py` (+100 lines) - `shannon validate` command
- `tests/functional/test_wave3_validation.sh` (50 lines)

### Tasks:
- [ ] **T3.1**: Implement test infrastructure auto-detection
- [ ] **T3.2**: Implement Tier 1 validation (build, lint, type check)
- [ ] **T3.3**: Implement Tier 2 validation (unit/integration tests)
- [ ] **T3.4**: Implement Tier 3 validation - Node.js (dev server + E2E)
- [ ] **T3.5**: Implement Tier 3 validation - Python (uvicorn + curl)
- [ ] **T3.6**: Implement Tier 3 validation - iOS (simulator + UI tests)
- [ ] **T3.7**: Create unified validate_all method
- [ ] **T3.8**: Create `shannon validate` CLI command
- [ ] **T3.9**: Functional tests (all 3 tiers on sample projects)

### Verification Criteria:
- [ ] Auto-detects test commands for Node.js/Python/iOS
- [ ] All 3 tiers run correctly
- [ ] Returns structured ValidationResult
- [ ] CLI command works and returns JSON
- [ ] Duration <10min for typical validation

### Exit Criteria:
Can run 3-tier validation on real projects. Returns structured results with pass/fail details.

---

## Wave 4: Git Manager 🗂️

**Type**: Infrastructure
**Duration**: 1 day (8 hours)
**Dependencies**: Wave 3 complete
**Files**: 3 files, ~300 lines

### Files Created/Modified:
- `src/shannon/executor/git_manager.py` (200 lines)
- `src/shannon/cli/commands.py` (+50 lines) - `shannon git-commit` command
- `tests/functional/test_wave4_git.sh` (50 lines)

### Tasks:
- [ ] **T4.1**: Implement GitManager base class
- [ ] **T4.2**: Implement state verification (clean state, not on main)
- [ ] **T4.3**: Implement branch creation (semantic naming)
- [ ] **T4.4**: Implement commit message generation (structured format)
- [ ] **T4.5**: Implement atomic commit (stage + commit + track)
- [ ] **T4.6**: Implement rollback (git reset --hard + clean)
- [ ] **T4.7**: Implement analytics tracking
- [ ] **T4.8**: Create `shannon git-commit` CLI command
- [ ] **T4.9**: Functional tests (branch, commit, rollback, verify)

### Verification Criteria:
- [ ] Generates semantic branch names (feat/, fix/, etc.)
- [ ] Creates commits with structured messages
- [ ] Rollback reverts all changes
- [ ] Tracks commits in analytics DB
- [ ] Git history is clean

### Exit Criteria:
Can create feature branches, commit validated changes atomically, rollback failed changes. Ready for orchestration.

---

## Wave 5: Exec Skill + CLI Integration 🚀

**Type**: Orchestration
**Duration**: 2 days (16 hours)
**Dependencies**: Waves 1-4 complete, Shannon Framework repo access
**Files**: 5 files, ~900 lines

### Repository: Shannon Framework
- `.claude-skills/exec.ts` (400 lines)
- `.claude-skills/prompts/exec-enhancements.md` (200 lines)

### Repository: Shannon CLI
- `src/shannon/cli/commands.py` (+150 lines) - Complete exec command
- `src/shannon/analytics/schema.sql` (+100 lines) - Execution tables
- `src/shannon/analytics/database.py` (+100 lines) - Execution tracking

### Tasks:
- [ ] **T5.1**: Design exec.ts skill structure (6 phases)
- [ ] **T5.2**: Implement Phase 1 - Context (invoke /shannon:prime)
- [ ] **T5.3**: Implement Phase 2 - Library Discovery (call shannon discover-libs)
- [ ] **T5.4**: Implement Phase 3 - Analysis (invoke /shannon:analyze)
- [ ] **T5.5**: Implement Phase 4 - Planning (sequential-thinking MCP)
- [ ] **T5.6**: Implement Phase 5 - Execution Loop (invoke /shannon:wave per step)
- [ ] **T5.7**: Implement retry with research (firecrawl integration)
- [ ] **T5.8**: Implement Phase 6 - Report (execution summary)
- [ ] **T5.9**: Complete exec CLI command (enhancement + invocation + streaming)
- [ ] **T5.10**: Add analytics tracking (executions, steps, libraries tables)
- [ ] **T5.11**: Functional E2E tests (simple task, libraries, multi-step, failure retry)

### Verification Criteria:
- [ ] exec.ts skill runs all 6 phases
- [ ] Invokes existing skills correctly
- [ ] Calls CLI modules successfully
- [ ] Handles success and failure
- [ ] Generates execution report
- [ ] CLI streams to dashboard
- [ ] Analytics tracks everything
- [ ] E2E test passes

### Exit Criteria:
`shannon exec "task"` works end-to-end: discovers libraries, plans, executes via wave, validates, commits, handles failures, reports results.

---

## Wave 6: Integration Testing 🧪

**Type**: Testing
**Duration**: 1 day (8 hours)
**Dependencies**: Wave 5 complete
**Files**: 8 test files, ~400 lines

### Files Created:
- `tests/functional/test_exec_simple_task.sh`
- `tests/functional/test_exec_with_libraries.sh`
- `tests/functional/test_exec_multi_step.sh`
- `tests/functional/test_exec_failure_retry.sh`
- `tests/functional/test_exec_ios.sh`
- `tests/functional/test_exec_python.sh`
- `tests/functional/test_exec_edge_cases.sh`
- `tests/functional/run_exec_tests.sh`

### Tasks:
- [ ] **T6.1**: Test simple task (fix typo)
- [ ] **T6.2**: Test library discovery (form validation → react-hook-form)
- [ ] **T6.3**: Test multi-step (authentication → multiple commits)
- [ ] **T6.4**: Test failure retry (intentional failure → research → success)
- [ ] **T6.5**: Test iOS project (SwiftUI button → simulator validation)
- [ ] **T6.6**: Test Python project (FastAPI endpoint → curl validation)
- [ ] **T6.7**: Test edge cases (ambiguous, no libraries, max retries, unclean state, on main)
- [ ] **T6.8**: Test analytics tracking (verify DB records)

### Verification Criteria:
- [ ] All 8 tests pass
- [ ] Tests run in <30 minutes total
- [ ] Produces verifiable artifacts (commits, branches, analytics)
- [ ] Edge cases handled gracefully
- [ ] NO MOCKS - real shannon exec

### Exit Criteria:
V3.5 validated across platforms and scenarios. All tests pass. System proven robust.

---

## Wave 7: Documentation & Examples 📚

**Type**: Documentation
**Duration**: 0.5 days (4 hours)
**Dependencies**: Wave 6 complete
**Files**: 4 docs, ~800 lines

### Files Created/Modified:
- `docs/SHANNON_V3.5_USER_GUIDE.md` (400 lines)
- `docs/SHANNON_V3.5_ARCHITECTURE.md` (200 lines)
- `examples/exec_react_auth.md` (100 lines)
- `examples/exec_ios_feature.md` (100 lines)
- `README.md` (+50 lines)

### Tasks:
- [ ] **T7.1**: Write user guide (installation, usage, troubleshooting)
- [ ] **T7.2**: Write architecture doc (system design, integration points)
- [ ] **T7.3**: Create React auth example (next-auth integration)
- [ ] **T7.4**: Create iOS example (image picker with PhotosUI)
- [ ] **T7.5**: Update README with V3.5 section

### Verification Criteria:
- [ ] User guide covers all features
- [ ] Architecture doc explains design
- [ ] Examples are reproducible
- [ ] Documentation accurate
- [ ] README updated

### Exit Criteria:
Complete documentation enables users to understand, install, use, and troubleshoot V3.5.

---

## 📊 Implementation Metrics

### Code Distribution:
| Component | Lines | Repository |
|-----------|-------|------------|
| Data models | 100 | Shannon CLI |
| Prompt templates | 400 | Shannon CLI |
| Prompt enhancer | 150 | Shannon CLI |
| Library discoverer | 250 | Shannon CLI |
| Validation orchestrator | 300 | Shannon CLI |
| Git manager | 200 | Shannon CLI |
| CLI commands | 350 | Shannon CLI |
| Analytics extensions | 200 | Shannon CLI |
| **CLI Subtotal** | **1,950** | |
| Exec skill | 400 | Shannon Framework |
| Skill prompts | 200 | Shannon Framework |
| **Framework Subtotal** | **600** | |
| Test suite | 400 | Shannon CLI |
| Documentation | 800 | Shannon CLI |
| **Grand Total** | **3,750** | |

### Timeline Breakdown:
| Phase | Days | Lines | Cumulative |
|-------|------|-------|------------|
| Phase 0 | 0.5 | 150 | 150 |
| Wave 1 | 1.0 | 650 | 800 |
| Wave 2 | 2.0 | 400 | 1,200 |
| Wave 3 | 2.0 | 450 | 1,650 |
| Wave 4 | 1.0 | 300 | 1,950 |
| Wave 5 | 2.0 | 900 | 2,850 |
| Wave 6 | 1.0 | 400 | 3,250 |
| Wave 7 | 0.5 | 800 | 4,050 |
| **Total** | **10.0** | **4,050** | |

### Risk Assessment:
- **HIGH RISK**: system_prompt.append API existence (mitigated by Phase 0)
- **MEDIUM RISK**: Firecrawl MCP rate limits (mitigated by Serena caching)
- **MEDIUM RISK**: Tier 3 validation complexity (mitigated by incremental platform support)
- **LOW RISK**: TypeScript skill integration (can test incrementally)

### Success Criteria:
- [ ] All 8 functional tests pass
- [ ] Works for React, React Native, iOS, Python projects
- [ ] Library discovery >80% accuracy
- [ ] Validation catches issues before commit (>95%)
- [ ] Git history contains only validated commits
- [ ] Documentation complete

---

## 🔗 Integration Points with Existing Shannon

### Reuses Existing Skills:
- `/shannon:prime` - Context preparation (Phase 1 of exec)
- `/shannon:analyze` - 8D complexity analysis (Phase 3 of exec)
- `/shannon:wave` - Agent orchestration (Phase 5 execution per step)

### Reuses Existing Systems:
- **AgentController**: Multi-agent execution (via wave skill)
- **ContextManager**: Codebase scanning (via prime skill)
- **SessionManager**: Session storage (plan persistence)
- **Analytics DB**: Execution tracking (extended with new tables)
- **V3.1 Dashboard**: Real-time visibility (shows exec progress)

### Reuses Existing MCPs:
- **Serena**: Caching (libraries, context, research)
- **Sequential-thinking**: Planning (execution plan creation)
- **Firecrawl**: Web search (library discovery, research)

### New Additions:
- **Prompt Enhancement**: System instruction injection
- **Library Discovery**: Package registry search + ranking
- **3-Tier Validation**: Build + Test + Functional
- **Git Automation**: Atomic commits + rollback
- **Orchestration**: Exec skill that wraps existing skills

---

## 🚀 Deployment Strategy

### Per-Wave Deployment:
- **Wave 1**: Deploy to dev environment, test prompt injection
- **Wave 2**: Deploy discovery module, test library search
- **Wave 3**: Deploy validator, test 3-tier validation
- **Wave 4**: Deploy git manager, test commits
- **Wave 5**: Deploy exec skill + CLI, test E2E
- **Wave 6**: Run full test suite
- **Wave 7**: Publish docs

### Testing Philosophy (Shannon NO MOCKS):
- **NO unit tests**: Only functional/E2E tests
- **Real execution**: Actual `shannon exec` commands
- **Real artifacts**: Verify git commits, analytics records
- **Real validation**: Run builds, tests, servers
- **User perspective**: Test what users will experience

### Version Control:
- Create branch: `feat/v3.5-autonomous-executor`
- Commit per wave: "feat(v3.5): Complete Wave X - {description}"
- Squash before merge: Single commit for V3.5 release
- Tag: `v3.5.0` when complete

---

## 📋 Pre-Implementation Checklist

Before starting Phase 0:
- [ ] Shannon CLI V3.0 verified operational
- [ ] Shannon Framework repo accessible
- [ ] Firecrawl MCP configured and working
- [ ] Serena MCP configured and working
- [ ] Sequential-thinking MCP configured
- [ ] Git state clean (no uncommitted changes)
- [ ] On feature branch (not main/master)

Before starting Wave 5:
- [ ] Waves 1-4 complete and tested
- [ ] Shannon Framework repo cloned
- [ ] Can create .claude-skills/ files
- [ ] Can test Framework skills locally

---

## 🎯 Expected Outcomes

### After Phase 0:
- ✅ Confirmed: system_prompt.append works
- ✅ OR: Alternative approach designed and documented
- ✅ Architecture validated or revised
- ✅ Ready to proceed with confidence

### After Wave 5:
- ✅ `shannon exec "task"` works end-to-end
- ✅ Discovers and uses existing libraries
- ✅ Validates all changes (3 tiers)
- ✅ Creates atomic git commits
- ✅ Handles failures with retry
- ✅ Produces execution report

### After Wave 6:
- ✅ Proven robust across platforms
- ✅ All edge cases handled
- ✅ Test suite proves reliability
- ✅ Ready for production use

### After Wave 7:
- ✅ Users can understand and use V3.5
- ✅ Architecture documented for contributors
- ✅ Real-world examples available
- ✅ V3.5 launch ready

---

## 🔄 Comparison: What We're Building

| Aspect | Before (V3.0) | After (V3.5) |
|--------|---------------|--------------|
| Usage | `shannon wave` (manual planning) | `shannon exec` (autonomous) |
| Libraries | Manual research | Auto-discovery + ranking |
| Validation | Manual testing | 3-tier automated |
| Git | Manual commits | Atomic validated commits |
| Retry | Manual debugging | Auto-research + retry |
| Prompts | Standard Claude Code | Enhanced with best practices |
| Result | Requires human oversight | Autonomous with validation |

---

**Status**: ✅ PLAN COMPLETE - Ready for Phase 0 execution
**Next**: Validate system_prompt.append API → Begin implementation
