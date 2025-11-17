# Shannon CLI Cleanup Quick Reference

**TL;DR**: 4 orchestrators, 3 active, 1 broken. Archive 15+ unused files, fix 1 critical bug.

---

## The 4 Orchestrators

| Name | File | Version | Status |
|------|------|---------|--------|
| **ContextAwareOrchestrator** | `orchestrator.py` | V3 | ✅ Active (8 subsystems) |
| **UnifiedOrchestrator** | `unified_orchestrator.py` | V5 | ✅ Active (delegates to V3) |
| **ResearchOrchestrator** | `research/orchestrator.py` | Wave 9 | ✅ Active (MCP research) |
| **Orchestrator** | `orchestration/orchestrator.py` | V4 | ❌ Broken (imports archived skills) |

---

## Commands → Orchestrators

```
shannon do         → UnifiedOrchestrator (V5)
shannon analyze    → UnifiedOrchestrator → ContextAwareOrchestrator (V5→V3)
shannon wave       → UnifiedOrchestrator → ContextAwareOrchestrator (V5→V3)
shannon exec       → CompleteExecutor (V3.5 autonomous)
shannon research   → ResearchOrchestrator (Wave 9)
shannon onboard    → ContextAwareOrchestrator (V3 direct)
shannon prime      → ContextAwareOrchestrator (V3 direct)
+ 6 more context   → ContextAwareOrchestrator (V3 direct)
```

---

## Critical Issues

### 🔴 Issue #1: Duplicate execute_task()
**File**: `unified_orchestrator.py`
**Lines**: 298-326 AND 328-383
**Fix**: Delete lines 298-326 (first definition)

### 🔴 Issue #2: Broken Imports
**Files**: 3 files import from non-existent `shannon.skills` module
- `orchestration/orchestrator.py` ❌
- `server/app.py` ❌ (check if critical)
- `cli/v4_commands/do_v4_original.py` ❌ (backup file)

### 🟡 Issue #3: Subsystem Duplication
**File**: `unified_orchestrator.py`
**Problem**: Creates subsystems, then creates V3 orchestrator, then injects subsystems into V3
**Fix**: Create V3 orchestrator first, use its subsystems

---

## Files to Archive (Immediate)

### V4 Skills Framework (Already Archived) ✅
```
_archived/skills_custom_framework/  (12 files)
```

### V4 Orchestrator (Broken, Unused)
```
orchestration/orchestrator.py  ❌ Broken imports
orchestration/agents/          (9 files - unused)
  base.py
  analysis.py
  planning.py
  git.py
  research.py
  testing.py
  validation.py
  monitoring.py
```

### V4 Skill Definitions (Root Directory)
```
/skills/built-in/  (5 YAML files)
```

### V4 Backup Command
```
cli/v4_commands/do_v4_original.py  (backup of old do command)
```

**Total to Archive**: 15+ files

---

## Files to Keep (Active)

### Core (3 orchestrators)
```
orchestrator.py                  ✅ ContextAwareOrchestrator (V3)
unified_orchestrator.py          ✅ UnifiedOrchestrator (V5)
research/orchestrator.py         ✅ ResearchOrchestrator (Wave 9)
```

### V3 Subsystems (30+ files)
```
cache/          (4 files)  ✅
context/        (6 files)  ✅
analytics/      (4 files)  ✅
optimization/   (3 files)  ✅
mcp/            (4 files)  ✅
agents/         (3 files)  ✅
metrics/        (3 files)  ✅
sdk/            (3 files)  ✅
```

### V3.5 Executor (11 files)
```
executor/       (11 files) ✅
```

### V5 Infrastructure (2 files)
```
orchestration/state_manager.py   ✅
orchestration/agent_pool.py      ✅
```

### Shared (15+ files)
```
config.py, core/, storage/, ui/, communication/, server/, setup/
```

**Total Active**: ~75-85 files (out of 125)

---

## Cleanup Timeline

### Phase 1: Critical Fixes (1 hour)
1. ✅ Fix duplicate `execute_task()` → Delete lines 298-326
2. ⚠️ Check if `server/app.py` is critical
3. ✅ Test commands still work

### Phase 2: Archive Unused (2 hours)
1. Move `orchestration/orchestrator.py` to `_archived/v4/`
2. Move `orchestration/agents/` to `_archived/v4/`
3. Move `cli/v4_commands/do_v4_original.py` to `_archived/v4/`
4. Move `/skills/built-in/` to `_archived/v4_skill_definitions/`
5. Test no broken imports remain

### Phase 3: Refactor (1-2 days)
1. Fix subsystem duplication in UnifiedOrchestrator
2. Standardize all commands to use UnifiedOrchestrator
3. Extract context workflows to ContextManager
4. Update documentation

---

## Before/After Comparison

### Before Cleanup
```
125 Python files
- 4 orchestrators (1 broken)
- 3 versions mixed (V3, V4, V5)
- Broken imports (shannon.skills)
- 15+ unused files
- Duplicate code
```

### After Cleanup
```
~85 Python files (-40)
- 3 orchestrators (all functional)
- Clear version boundaries
- No broken imports
- All files have purpose
- Minimal duplication
```

---

## Testing Checklist

```bash
# Before cleanup
✓ Git commit current state
✓ Run all commands (shannon --help, analyze, do, exec, research)
✓ Note which commands work

# After each phase
✓ Check no broken imports: python -c "import shannon.orchestrator"
✓ Test commands still work
✓ Verify no references to deleted files

# Final verification
✓ All commands functional
✓ No imports from _archived/
✓ No references to shannon.skills
✓ Documentation updated
```

---

## Risk Assessment

### Low Risk ✅
- Archiving unused V4 agents (no imports found)
- Archiving V4 orchestrator (broken, not used)
- Archiving backup do_v4_original.py
- Fixing duplicate execute_task() (obvious bug)

### Medium Risk ⚠️
- Refactoring subsystem initialization (changes object creation order)
- Updating server/app.py (need to verify server functionality)
- Moving skill definitions (need to verify nothing loads them)

### High Risk 🔴
- None identified (all changes are safe with proper testing)

---

## Quick Commands

```bash
# Verify V4 orchestrator unused
grep -r "from shannon.orchestration.orchestrator" src/

# Verify V4 agents unused
grep -r "from shannon.orchestration.agents" src/

# Find broken skill imports
grep -r "from shannon.skills" src/ --include="*.py"

# Test import works
python -c "from shannon.orchestrator import ContextAwareOrchestrator"

# Check active commands
grep "@cli.command()" src/shannon/cli/commands.py
```

---

## Key Insights

1. **V5 uses Claude Code skills**, not custom skills framework
2. **V4 skills framework is archived**, orchestrator has broken imports
3. **V3 subsystems are active**, used by ContextAwareOrchestrator
4. **UnifiedOrchestrator is facade**, delegates to V3
5. **CompleteExecutor is separate**, used by `shannon exec`

---

## Decision Tree

```
Is file in _archived/?
  YES → Safe to ignore
  NO  → Continue

Does file import shannon.skills?
  YES → Archive or fix imports
  NO  → Continue

Is file imported by any command?
  NO  → Archive
  YES → Keep

Does file have broken imports?
  YES → Archive
  NO  → Keep
```

---

**Next Action**: Review SHANNON_CLI_ARCHITECTURE_MAP.md for full details, then execute Phase 1 cleanup.
