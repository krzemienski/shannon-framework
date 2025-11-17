# Next Session: Shannon Framework intelligent-do Skill

**Date**: 2025-11-17
**Status**: Shannon CLI cleanup COMPLETE, basic validation passing, complex test RUNNING
**Next**: Build proper Shannon Framework intelligent-do skill

---

## Current Session Completion

### ✅ What's Done:

**1. Technical Debt Cleanup**:
- Analyzed 125 Python files completely
- Fixed 2 critical bugs
- Archived 15 V4 files
- Architecture documented (12,000 words)

**2. Intelligent shannon do (Shannon CLI)**:
- 10 methods implemented (workflows, validation gates, caching)
- Using wave-orchestration skill for code generation
- First-time workflow: PASSING ✅
- Returning workflow: PASSING ✅
- Complex test: RUNNING (in progress)

**3. Shannon Framework Plan**:
- Comprehensive 1,500-line plan created
- Complete Framework exploration done
- Ready to execute

---

## What to Load Next Session

### Critical Documents:

1. **SESSION_SUMMARY_CLEANUP_AND_PLANNING.md** - Complete session summary
2. **SHANNON_CLI_ARCHITECTURE_MAP.md** - Full architecture analysis
3. **docs/plans/2025-11-17-shannon-framework-intelligent-do-implementation.md** - Framework plan
4. **CLEANUP_COMPLETE_SUMMARY.md** - Cleanup results

### Serena Memory:
```python
mcp__serena__read_memory("CLEANUP_COMPLETE_ARCHITECTURE_CLEAR_20251117")
```

---

## Execute This Plan

**File**: `docs/plans/2025-11-17-shannon-framework-intelligent-do-implementation.md`

**Timeline**: 13-20 hours (6 phases)

**What It Builds**:
- Shannon Framework intelligent-do skill (SKILL.md)
- /shannon:do command (do.md)
- Serena MCP backend integration
- Research auto-detection
- Complete testing with sub-agents
- Shannon CLI integration

---

## Phase 1: Shannon Framework Deep Dive (2-3 hours)

**Already Done** ✅:
- Framework exploration complete
- 19 skills documented
- 16 commands mapped
- MCP integration understood

**Skip to Phase 2**: Skill design

---

## Phase 2: Skill Design (3-4 hours)

**Tasks**:
1. Design complete decision tree ✅ (already done in plan)
2. Design Serena entity model ✅ (already specified)
3. Write skill frontmatter (15 min)
4. Write entry & context check (30 min)
5. Write first-time workflow (1 hour)
6. Write returning workflow (1 hour)
7. Write research integration (30 min)
8. Add examples (15 min)

**Location**: `/Users/nick/Desktop/shannon-framework/skills/intelligent-do/`

**Output**: Complete SKILL.md file

---

## Phase 3: Create /shannon:do Command (1-2 hours)

**File**: `shannon-framework/commands/do.md`

**Content**:
- YAML frontmatter (name, description, usage)
- Delegates to intelligent-do skill
- Parameter handling (--auto, --interactive)
- Output formatting

---

## Phase 4: Testing (2-3 hours)

**Tests**:
- Standalone skill test (in Framework)
- Sub-agent spawn test
- Research integration test
- Serena MCP integration test

**Location**: `shannon-framework/skills/intelligent-do/tests/`

---

## Phase 5: Shannon CLI Integration (1-2 hours)

**Update**: `shannon-cli/src/shannon/unified_orchestrator.py`

**Change**:
```python
# In _execute_with_context():
async for msg in self.sdk_client.invoke_skill(
    skill_name='intelligent-do',  # NEW (was wave-orchestration)
    prompt_content=simplified_prompt  # Skill handles context loading
):
```

**Simplification**:
- Skill loads context from Serena (not passed from CLI)
- CLI keeps V3 wrappers (cache, analytics, cost)
- Can eventually remove _first_time_workflow, _returning_workflow (skill handles)

---

## Phase 6: Complete Validation (4-6 hours)

**Tests** (all with evidence collection):
1. Standalone Framework skill test
2. Shannon CLI integration test
3. First-time workflow
4. Returning workflow with Serena
5. Research integration (Stripe example)
6. Complex application (10-15 min)
7. Dashboard browser test
8. Sub-agent test

**Evidence Required**:
- Serena graph exports (showing entities/relations)
- Test logs (all passing)
- Screenshots (dashboard, working apps)
- Working applications (full directory listings)
- Performance metrics (timing comparisons)

---

## Current Implementation Status

### Shannon CLI shannon do ✅:
- First-time: Auto-onboards, saves local config ✅
- Returning: Loads cache, detects changes ✅
- Validation gates: Auto-detected ✅
- File creation: Working (wave-orchestration) ✅
- Backend: Local JSON files (~/.shannon/projects/)

### What Framework Skill Adds:
- Backend: Serena MCP (persistent graph)
- Research: Auto-detection + execution
- Priming: Smart decision (only when needed)
- Spec: Smart decision (skip for simple tasks)
- Memory: Cross-session learning
- Sub-agents: Proper testing

---

## Bugs Found & Fixed This Session

**Bug #1**: Duplicate execute_task() - Fixed ✅
**Bug #2**: Broken shannon.skills imports - Fixed ✅
**Bug #3**: get_status() references V4 components - Fixed ✅
**Bug #4**: load_project() format mismatch - Fixed ✅
**Bug #5**: Returning workflow ChangeSet handling - Fixed ✅

**All compilation errors resolved** ✅

---

## Complex Test Status

**Running Now**: Complex Flask API generation
**Started**: 10:38:14
**Expected Duration**: 10-15 minutes
**Progress**: wave-orchestration skill executing
**Will Check**: Every 2-3 minutes until complete
**Evidence Collection**: Automatic (test script captures everything)

---

## After Complex Test Completes

**If PASSES**:
1. Check evidence (/tmp/shannon-complex-app-evidence-*)
2. Verify files created (app.py, models.py, tests, etc.)
3. Run dashboard browser test (Gate 4)
4. Create complete evidence package
5. Tag shannon-cli v5.1.0-beta
6. **Then**: Execute Shannon Framework plan (Path B)

**If FAILS**:
1. Analyze failure (what went wrong?)
2. Fix issue
3. Re-run
4. Then proceed to dashboard test

---

## Success Criteria (Path A)

**Shannon CLI v5.1.0-beta Release Requirements**:
- ✅ First-time workflow test passing
- ✅ Returning workflow test passing
- ⏳ Complex application test passing (RUNNING)
- ⏳ Dashboard browser test passing (pending)
- ✅ All commands working
- ✅ No broken imports
- ✅ Architecture clean

**Evidence Package Must Include**:
- Test logs (4 functional tests)
- Working complex application (directory + files)
- Screenshot of dashboard (Playwright capture)
- Performance metrics (timing data)

---

## Success Criteria (Path B - Framework)

**Shannon Framework v5.2.0 Release Requirements**:
- ✅ intelligent-do skill created (SKILL.md complete)
- ✅ /shannon:do command created (do.md complete)
- ✅ Serena MCP integration working
- ✅ Research auto-detection working
- ✅ All sub-skills integrated (spec, wave, research, testing)
- ✅ Sub-agent testing passing
- ✅ Shannon CLI integration working

**Then Shannon CLI v5.2.0**:
- Uses Framework intelligent-do skill
- Simplified code (intelligence in skill)
- All validation passing

---

## Token Budget

**Used**: 318K / 1M (32%)
**Remaining**: 682K (68%)

**Path A Needs**: ~20K (< 2%)
**Path B Needs**: ~250-350K (25-35%)
**Buffer**: Plenty (can complete both paths)

---

## Commits This Session (19 total)

Track record of all work:
- f1cc631 through dd3b20f: Intelligent workflows (9 commits)
- 64c4891, 50d9b7f: Critical bug fixes
- bf427fb, 152a778, e84d680: Cleanup (3 commits)
- 8af4299: SDK audit
- 1b2ee3d, 0d83fc2: Skill switching and fixes
- 2d19ac1: get_status() fix
- 877f9fc: Session summary

---

**Ready for**:
- Complex test completion (monitoring now)
- Dashboard test (next)
- Path B execution (after Path A complete)

**No interruptions - letting complex test run to completion.**
