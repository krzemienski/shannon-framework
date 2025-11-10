# Shannon v5.0 Continuation - Complete SDK Testing and Verification

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Resume Shannon v5.0 verification with clean repository and working SDK foundation

**Status**: Previous session cleaned repository, saved docs, fixed SDK pattern. This session tests and executes v5 verification.

**Prerequisites**: Repository cleaned (sc_* removed), SDK docs saved, tier1 fixed with setting_sources

---

## CONTEXT FROM PREVIOUS SESSION

### What Was Completed

**Repository Cleanup** (commit 8b82255):
- Removed 25 sc_* SuperClaude legacy commands
- Shannon now has 14 pure commands

**Documentation Saved** (commits 781115d, de15cb7, d81143a):
- 21 files in docs/ref/ (4 specs + 12 SDK + 3 CLI + 2 llms)
- All 14 URLs from user saved
- Reference index created

**Metadata Fixed** (commit 838df78, 94ea4a2):
- README.md updated (14 commands, removed sc_* refs)
- plugin.json verified correct
- tier1_verify_analysis.py fixed with setting_sources

**Test Directory Cleaned** (commit 278b266):
- Removed 12 debug test files
- Kept only essential v5 verification scripts

### Critical SDK Discovery

**WORKING PATTERN** (verified from official docs):
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./shannon-plugin"}],
    setting_sources=["user", "project"],  # REQUIRED!
    permission_mode="bypassPermissions",
    allowed_tools=["Skill"]
)
```

**Without setting_sources**: plugins=[], skills=[], commands=[]
**With setting_sources**: Everything loads correctly

---

## Phase 1: Verify SDK Testing Works

### Task 1.1: Check tier1 Test Results

**Prerequisites:**
- tier1_verify_analysis.py running in background (process 5123bc)

**Step 1: Check if tier1 completed**

```bash
# Check background process
ps aux | grep tier1_verify_analysis

# Or check for output file
ls tests/.verification_report.txt
```

**Step 2: Review tier1 results**

If process complete, check output:
- Did all 4 specs get analyzed?
- Did Shannon commands load?
- Did /sh_spec produce output?
- What was the cost?

**Step 3: Document findings**

If PASSING:
```bash
# Tier1 works - proceed to tier2
echo "✅ Tier1 PASSED" >> tests/tier1_status.txt
```

If FAILING:
```bash
# Debug what's still wrong
echo "❌ Tier1 FAILED - [specific issue]" >> tests/tier1_status.txt
# Fix issues before continuing
```

**Step 4: Write results to Serena**

```python
mcp__serena__write_memory(
    "SHANNON_V5_TIER1_RESULTS",
    content="[tier1 test results and analysis]"
)
```

### Task 1.2: Fix tier2 Scripts

**Files:**
- Modify: `tests/tier2_build_prd_creator.py`
- Modify: `tests/tier2_build_mobile_expo.py`
- Modify: `tests/tier2_build_repo_nexus.py`
- Modify: `tests/tier2_build_shannon_cli.py`

**Step 1: Add setting_sources to each tier2 script**

For each file, find ClaudeAgentOptions and add:
```python
setting_sources=["user", "project"],  # REQUIRED
allowed_tools=["Skill", "Task", "Read", "Write", "Bash"]
```

**Step 2: Verify message handling correct**

Ensure all use isinstance() checks, iterate content blocks.

**Step 3: Test one tier2 script**

```bash
# Don't actually build - just verify SDK loads Shannon
python tests/tier2_build_prd_creator.py --dry-run
```

Expected: Shannon plugin loads, commands available

**Step 4: Commit fixes**

```bash
git add tests/tier2_*.py
git commit -m "fix: add setting_sources to tier2 scripts for plugin loading"
```

---

## Phase 2: Test Shannon via SDK (Tier 1)

### Task 2.1: Run Tier 1 Verification

**Execute:**
```bash
python tests/tier1_verify_analysis.py
```

**Expected Output:**
```
Testing: PRD Creator
✅ Shannon commands: [sh_spec, sh_wave, ...]
Output preview: "📊 Shannon Specification Analysis..."
Complexity: 0.40-0.50 ✅

Testing: Claude Code Expo
Output preview: "📊 Shannon Specification Analysis..."
Complexity: 0.65-0.72 ✅

...

Result: 4/4 specifications passed
```

**Step 2: Validate results**

Check:
- All 4 specs analyzed
- Complexity scores reasonable
- Output contains Shannon markers
- No SDK errors

**Step 3: Document to Serena**

If passing:
```python
mcp__serena__write_memory(
    "SHANNON_V5_TIER1_SUCCESS",
    content="""
    Tier 1 verification PASSED
    - All 4 specs analyzed via SDK
    - Shannon plugin loads correctly with setting_sources
    - /sh_spec command functional
    - Ready for Tier 2 (actual builds)
    """
)
```

---

## Phase 3: Decide Next Steps

### Task 3.1: Evaluate Tier 1 Results

**If Tier 1 PASSED:**
- ✅ SDK working
- ✅ Shannon loads
- ✅ Commands functional
- → Proceed to Tier 2 (build applications)

**If Tier 1 FAILED:**
- ❌ SDK issues remain
- → Debug and fix before Tier 2
- → Don't proceed until working

### Task 3.2: Create Tier 2 Execution Decision

**If proceeding to Tier 2:**

Choice A: Build ONE app (PRD Creator) - ~$60, 10-15h
- Proves Shannon can build applications
- Cheaper than building all 4
- Good for initial validation

Choice B: Build ALL 4 apps - ~$300-500, 60-100h
- Comprehensive validation
- Tests all domains (web, mobile, CLI)
- Meta-circular test (Shannon CLI)

**Document decision to Serena before executing**

---

## Phase 4: Session Handoff

### Task 4.1: Create Complete Handoff Document

**Files:**
- Create: `docs/plans/sessions/v5-session-2-handoff.md`

**Content:**
```markdown
# Session 2 Handoff - Repository Cleanup Complete

## What Was Done This Session

1. Removed SuperClaude legacy (25 sc_* commands)
2. Saved complete SDK documentation (21 files)
3. Fixed metadata (README, verified plugin.json)
4. Cleaned test directory (12 debug files removed)
5. Fixed SDK pattern (setting_sources requirement)

## Current State

- Shannon v5.0: Pure (14 commands, no hybrid)
- Documentation: Complete in docs/ref/
- SDK: Latest from GitHub, pattern verified
- Tests: tier1 fixed, tier2 ready

## What's Next

- Verify tier1 results
- Fix tier2 if needed
- Decide: Build 1 app or all 4
- Execute chosen tier
- Document findings

## Critical Knowledge

setting_sources=["user", "project"] REQUIRED for SDK plugin loading.

Without this, plugins don't load.
With this, Shannon works.
```

**Step 2: Commit handoff**

```bash
git add docs/plans/sessions/v5-session-2-handoff.md
git commit -m "docs: session 2 handoff - cleanup complete"
```

### Task 4.2: Update Serena with Complete State

**Write comprehensive memory:**

```python
mcp__serena__write_memory(
    "SHANNON_V5_SESSION_2_COMPLETE_STATE",
    content="""
    # Session 2: Repository Cleanup Complete

    ## Accomplished
    - Removed 25 sc_* commands
    - Saved 21 reference docs
    - Fixed README and metadata
    - Cleaned test directory
    - Fixed SDK with setting_sources
    - Verified pattern works

    ## Ready For
    - Tier 1 testing
    - Tier 2 builds
    - Complete v5 verification

    ## SDK Working Pattern
    ClaudeAgentOptions(
        plugins=[...],
        setting_sources=["user", "project"],  # CRITICAL!
        ...
    )
    """
)
```

---

## Success Criteria

**Session Complete When:**
- ✅ All documentation saved (21 files)
- ✅ Legacy commands removed (25 sc_* deleted)
- ✅ Metadata verified (README, plugin.json correct)
- ✅ Test directory clean
- ✅ SDK pattern fixed (setting_sources added)
- ✅ tier1 test executed
- ✅ Results documented to Serena
- ✅ Handoff created for next session

---

## Timeline

- Phase 1: 30 min (verify tier1, fix tier2)
- Phase 2: 10 min (run tier1 if not complete)
- Phase 3: 5 min (decide next steps)
- Phase 4: 15 min (create handoff)

**Total**: ~1 hour to complete handoff

---

**Plan Purpose**: Clean completion of repository cleanup work and proper handoff for v5 testing execution.
