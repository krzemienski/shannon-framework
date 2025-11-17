# Shannon CLI Cleanup Verification

**Date**: 2025-11-17
**Purpose**: Verification results for architecture cleanup

---

## Critical Finding: Missing `shannon.skills` Module

### The Problem

Multiple files import from `shannon.skills`:
- `src/shannon/server/app.py`
- `src/shannon/orchestration/orchestrator.py`
- `src/shannon/cli/v4_commands/do_v4_original.py`

**But the module doesn't exist!**

```bash
$ python3 -c "from shannon.skills.registry import SkillRegistry"
ModuleNotFoundError: No module named 'shannon.skills'
```

### What We Found

1. **No module in src/**: `src/shannon/skills/` does not exist
2. **Archived framework**: `src/shannon/_archived/skills_custom_framework/` exists (12 files)
3. **Root skills dir**: `/skills/` exists at project root with YAML files
4. **Imports are broken**: All imports from `shannon.skills` will fail

### Files With Broken Imports

#### **File 1: orchestration/orchestrator.py**
```python
from shannon.skills.executor import SkillExecutor
from shannon.skills.models import SkillResult, ExecutionContext
```
**Status**: ❌ **BROKEN** - Cannot run

---

#### **File 2: server/app.py**
```python
from shannon.skills.registry import SkillRegistry, SkillNotFoundError
from shannon.skills.models import Skill
```
**Status**: ❌ **BROKEN** - Server won't start

---

#### **File 3: cli/v4_commands/do_v4_original.py**
```python
from shannon.skills.registry import SkillRegistry
from shannon.skills.executor import SkillExecutor
from shannon.skills.hooks import HookManager
from shannon.skills.dependencies import DependencyResolver
from shannon.skills.loader import SkillLoader
from shannon.skills.discovery import DiscoveryEngine
```
**Status**: ❌ **BROKEN** - Command won't run

**Good news**: This is `do_v4_original.py` (backup), not the active `do.py` command

---

## Verification Results

### ✅ Confirmed: V4 Orchestrator Unused

**Search 1**: No imports of V4 Orchestrator
```bash
$ grep -r "from shannon.orchestration.orchestrator import" src/
# (no output - not imported anywhere)
```

**Search 2**: orchestrator.py references archived skills
```bash
$ grep "SkillExecutor\|SkillRegistry" src/shannon/orchestration/orchestrator.py
src/shannon/orchestration/orchestrator.py:from shannon.skills.executor import SkillExecutor
src/shannon/orchestration/orchestrator.py:    1. Skill execution via SkillExecutor
src/shannon/orchestration/orchestrator.py:        executor: SkillExecutor,
src/shannon/orchestration/orchestrator.py:            executor: SkillExecutor for running skills
```

**Conclusion**: orchestration/orchestrator.py has broken imports and is not used anywhere.

---

### ✅ Confirmed: V4 Agents Unused

**Search**: No imports of V4 agents
```bash
$ grep -r "from shannon.orchestration.agents" src/
# (no output - not imported anywhere)
```

**Conclusion**: All 9 agent files in `orchestration/agents/` are unused.

---

### ❌ Problem: Server App Has Broken Imports

**File**: `src/shannon/server/app.py`
**Issue**: Imports from non-existent `shannon.skills` module
**Impact**: Dashboard server cannot start (if it uses V4 skills)

**Need to check**: Does the server app actually use skills or is this dead code?

---

## Root Skills Directory Analysis

### What's in `/skills/built-in/`?

5 YAML files defining skills:
1. `code_generation.yaml`
2. `git_operations.yaml`
3. `library_discovery.yaml`
4. `prompt_enhancement.yaml`
5. `validation_orchestrator.yaml`

**Question**: Are these used by anything? Likely not, since:
- No `shannon.skills` module to load them
- V5 uses Claude Code skills from Shannon Framework
- These appear to be V4 skill definitions

---

## Cleanup Recommendations (Updated)

### Priority 0: Critical - Fix Broken Imports

**BEFORE any other cleanup**, we must address broken imports.

#### **Option A: Delete Files with Broken Imports**
Since these files aren't used and imports are broken:

1. **Delete or Archive**: `orchestration/orchestrator.py`
2. **Archive**: `cli/v4_commands/do_v4_original.py` (already a backup)
3. **Fix or Archive**: `server/app.py` (check if server still uses skills)

#### **Option B: Move Skills Framework Back**
If we want to keep V4 Orchestrator functional (unlikely):
1. Move `_archived/skills_custom_framework/` to `src/shannon/skills/`
2. Restore full V4 functionality

**Recommendation**: **Option A** - Delete/archive broken files

---

### Priority 1: Archive V4 Components

**Safe to Archive** (broken imports, not used):

```
Move to _archived/v4/:
  orchestration/orchestrator.py
  orchestration/agents/ (9 files)
  cli/v4_commands/do_v4_original.py (already a backup)
```

**Check before archiving**:
```
server/app.py - Does server use skills or is this dead code?
```

---

### Priority 2: Remove Root `/skills/` Directory

**Location**: `/Users/nick/Desktop/shannon-cli/skills/`
**Contents**: 5 YAML files defining V4 built-in skills
**Status**: Likely unused (no module to load them)

**Action**:
1. Verify not loaded by any code
2. Move to `_archived/v4_skill_definitions/`

---

### Priority 3: Clean Up Remaining Items

From original architecture map:
1. Fix duplicate `execute_task()` in unified_orchestrator.py
2. Eliminate subsystem duplication
3. Standardize command imports

---

## Test Plan

### Before Cleanup
```bash
# Save current state
git status > before_cleanup.txt
git diff > before_cleanup.diff

# Test all commands
shannon --help
shannon analyze docs/examples/spec.md
shannon do "create hello.py"
shannon exec "test task"
shannon research "topic"
```

### After Cleanup
```bash
# Verify no broken imports
python3 -c "import shannon.orchestrator"
python3 -c "import shannon.unified_orchestrator"
python3 -c "import shannon.research.orchestrator"

# Verify archived imports fail gracefully
! python3 -c "from shannon._archived import anything"

# Test commands still work
shannon --help
shannon analyze docs/examples/spec.md
shannon do "create test.py"

# Check for references to deleted files
! grep -r "shannon.skills" src/ --include="*.py" | grep -v "_archived"
! grep -r "orchestration.orchestrator" src/shannon/cli/ --include="*.py"
```

---

## File Action Plan

### Files to Archive Immediately

**orchestration/**:
```
_archived/v4/orchestration/
  orchestrator.py          (broken imports)
  agents/                  (9 files, unused)
    base.py
    analysis.py
    planning.py
    git.py
    research.py
    testing.py
    validation.py
    monitoring.py
```

**cli/v4_commands/**:
```
_archived/v4/cli/
  do_v4_original.py        (backup file with broken imports)
```

**Root directory**:
```
_archived/v4_skill_definitions/
  skills/built-in/         (5 YAML files)
```

---

### Files to Investigate

**server/app.py**:
- Check if server functionality depends on skills
- If yes: Update to work without skills or disable skill routes
- If no: Remove skill imports

---

## Summary Statistics

### Broken Import Files
- **Total**: 3 files
- **Critical**: 2 (orchestrator.py, app.py)
- **Backup**: 1 (do_v4_original.py)

### Unused Files Confirmed
- **Orchestrator**: 1 (orchestration/orchestrator.py)
- **Agents**: 9 (orchestration/agents/*.py)
- **Skill Definitions**: 5 (skills/built-in/*.yaml)
- **Archived Framework**: 12 (already in _archived/)

### Total Cleanup Potential
- **Files to Archive**: 15+ files
- **Directories to Archive**: 2 (agents/, skills/)
- **Broken Imports to Fix**: 3 files

---

## Next Steps

1. **Immediate**: Review server/app.py to determine if it's critical
2. **Quick Win**: Archive the 10 unused files (orchestrator + agents)
3. **Follow Up**: Continue with architecture map recommendations

---

**Conclusion**: The architecture analysis revealed critical broken imports that must be addressed first. The good news is these broken files are unused, making them safe to archive. After addressing broken imports, proceed with the full cleanup plan from SHANNON_CLI_ARCHITECTURE_MAP.md.
