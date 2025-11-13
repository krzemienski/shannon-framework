# Complete Audit & Cleanup Plan

**Based on**: COMPLETE_AUDIT_REPORT.md (765 lines, 294 files audited)
**Status**: Ready for execution
**Impact**: Transform from bloated/inconsistent to clean/accurate

---

## AUDIT FINDINGS SUMMARY

### Critical Issues Found

1. **71% Command Count Inflation**
   - Claimed: 48 commands
   - Actual: 14 commands
   - Cause: Documentation references 35 never-implemented sc_* commands

2. **15 Files Reference Phantom Commands**
   - sc_analyze, sc_implement, etc. documented but don't exist
   - Misleading users about functionality

3. **Duplicate README Files**
   - Root README: 2,861 lines
   - Plugin README: 248 lines (with wrong counts)

4. **Wrong Structure**
   - Currently: shannon-plugin/ subdirectory
   - Should be: Flat (plugin contents at root)

5. **Path References Broken**
   - Marketplace points to "./shannon-plugin"
   - Should point to "." after flattening

---

## CLEANUP PLAN

### Phase 1: Fix Documentation Counts (30 min)

**Accurate counts**:
- Commands: 14
- Agents: 24
- Skills: 17
- Core: 9
- Hooks: 5

**Files to update** (5 files):

1. **CLAUDE.md** (lines 59-61)
   - Change "48 commands" → "14 commands"
   - Change "26 agents" → "24 agents"
   - Change "20 skills" → "17 skills"

2. **README.md** (throughout)
   - Fix all count references
   - Remove sc_* mentions

3. **shannon-plugin/README.md** (lines 206-209)
   - "48 slash commands" → "14 slash commands"
   - Remove sc_* list
   - "26 specialized agents" → "24 specialized agents"

4. **shannon-plugin/ARCHITECTURE.md** (lines 598, 604, 610)
   - Update all counts

5. **CHANGELOG.md**
   - Update V4.0/V4.1 entries
   - Correct all historical counts

---

### Phase 2: Remove sc_* References (45 min)

**Files to update** (15 files):

1. shannon-plugin/USER_GUIDE.md - Remove sh_* vs sc_* comparison
2. shannon-plugin/ARCHITECTURE.md - Remove "35 enhanced commands" section
3. shannon-plugin/TROUBLESHOOTING.md - Remove sc_* FAQ
4. shannon-plugin/README.md - Remove sc_* command list
5. shannon-plugin/commands/shannon:status.md - Remove sc_* from status output
6. shannon-plugin/commands/shannon:analyze.md - Remove sc_analyze comparison
7-15. All test files with sc_* references

**Action**: Search/replace to remove ALL mentions of:
- sc_analyze, sc_implement, sc_build, sc_test, etc.
- "SuperClaude enhanced commands"
- "35 additional commands"

---

### Phase 3: Flatten Directory Structure (1 hour)

**Current**:
```
shannon-framework/
└── shannon-plugin/
    ├── commands/
    ├── agents/
    └── ...
```

**Target**:
```
shannon-framework/
├── .claude-plugin/
├── commands/
├── agents/
├── skills/
└── ...
```

**Steps**:

1. Move shannon-plugin contents to root:
   ```bash
   mv shannon-plugin/commands .
   mv shannon-plugin/agents .
   mv shannon-plugin/skills .
   mv shannon-plugin/core .
   mv shannon-plugin/hooks .
   mv shannon-plugin/modes .
   mv shannon-plugin/templates .
   mv shannon-plugin/.claude-plugin/plugin.json .claude-plugin/
   mv shannon-plugin/*.md .  # Move all docs
   mv shannon-plugin/llms.txt .
   mv shannon-plugin/LICENSE .
   ```

2. Merge shannon-plugin/tests/ with root tests/:
   ```bash
   mv shannon-plugin/tests/* tests/
   rmdir shannon-plugin/tests
   ```

3. Remove empty shannon-plugin/:
   ```bash
   rmdir shannon-plugin
   ```

4. Update marketplace.json:
   ```json
   {
     "plugins": [{
       "source": "."  // Was "./shannon-plugin"
     }]
   }
   ```

5. Update .gitignore if needed

---

### Phase 4: Consolidate Documentation (30 min)

**README Strategy**:
- **KEEP**: Root README.md as primary (update with correct counts)
- **REPLACE**: shannon-plugin/README.md → short pointer to root
- **RESULT**: One authoritative README

**Other Documentation**:
- ARCHITECTURE.md: Keep (update counts)
- INSTALLATION.md: Keep (most complete)
- TROUBLESHOOTING.md: Keep (update)
- USAGE_EXAMPLES.md: Keep
- USER_GUIDE.md: Keep

**Action**: After flattening, these docs are all at root (no shannon-plugin/ prefix needed)

---

### Phase 5: Update Path References (30 min)

**Files with shannon-plugin/ paths** (update all):

1. CLAUDE.md
2. README.md (if any remain after update)
3. CONTRIBUTING.md
4. All docs/ files referencing shannon-plugin/
5. Any test files with hardcoded paths

**Change**:
- `shannon-plugin/commands/` → `commands/`
- `shannon-plugin/skills/` → `skills/`
- etc.

---

### Phase 6: Remove Legacy Files (15 min)

**Safe to delete**:

1. docs/ref/archived-old-sdk-docs/ (15 files) - Old SDK docs
2. shannon-plugin/skills/context-preservation/SKILL-OLD.md - Old version
3. Any other *-OLD.md or *.bak files found

**Optional to archive**:
- docs/plans/sessions/v4.1-development/ (21 files) - Keep for history

---

## EXECUTION CHECKLIST

**Phase 1: Documentation Counts**
- [ ] Update CLAUDE.md (14 commands, 24 agents, 17 skills)
- [ ] Update README.md (all counts)
- [ ] Update shannon-plugin/README.md (all counts)
- [ ] Update shannon-plugin/ARCHITECTURE.md (all counts)
- [ ] Update CHANGELOG.md
- [ ] Commit: "docs: fix all component counts to accurate numbers"

**Phase 2: Remove sc_* References**
- [ ] Remove from shannon-plugin/USER_GUIDE.md
- [ ] Remove from shannon-plugin/ARCHITECTURE.md
- [ ] Remove from shannon-plugin/TROUBLESHOOTING.md
- [ ] Remove from shannon-plugin/README.md
- [ ] Remove from shannon-plugin/commands/shannon:status.md
- [ ] Remove from shannon-plugin/commands/shannon:analyze.md
- [ ] Remove from all test files
- [ ] Commit: "docs: remove all phantom sc_* command references"

**Phase 3: Flatten Structure**
- [ ] Move shannon-plugin/* to root
- [ ] Update marketplace.json source path
- [ ] Remove empty shannon-plugin/
- [ ] Commit: "refactor: flatten shannon-plugin to root directory"

**Phase 4: Consolidate Docs**
- [ ] Replace shannon-plugin/README.md with pointer
- [ ] Merge installation guides if duplicates remain
- [ ] Update cross-references
- [ ] Commit: "docs: consolidate documentation (single README)"

**Phase 5: Update Paths**
- [ ] Update all shannon-plugin/ references
- [ ] Test paths work
- [ ] Commit: "docs: update all path references after flattening"

**Phase 6: Clean Legacy**
- [ ] Delete archived-old-sdk-docs/
- [ ] Delete SKILL-OLD.md files
- [ ] Commit: "chore: remove legacy/archived files"

**Phase 7: Verify**
- [ ] Install plugin from marketplace
- [ ] Test all commands work
- [ ] Verify counts are accurate everywhere
- [ ] Commit: "docs: final verification and cleanup"

---

## EXPECTED OUTCOME

### Before Cleanup:
- 294 files
- 71% command count inflation
- 15 files with phantom command references
- Nested shannon-plugin/ structure
- Two conflicting READMEs

### After Cleanup:
- ~270 files (24 removed)
- 100% accurate counts
- 0 phantom references
- Flat plugin structure
- One authoritative README
- Clean, navigable, production-ready

---

## VALIDATION

After all phases complete:

```bash
# Verify structure
ls -la | grep -E "commands|agents|skills"
# Should show directories at root

# Verify marketplace
cat .claude-plugin/marketplace.json | grep source
# Should show "source": "."

# Verify installation
claude plugin uninstall shannon-plugin@shannon-framework
claude plugin marketplace add .
claude plugin install shannon-plugin@shannon-framework
claude --print -- "/shannon:sh_status"
# Should work

# Verify counts
grep -r "48 commands" .
# Should return nothing

grep -r "sc_analyze" .
# Should return nothing (except archived files)
```

---

**READY FOR APPROVAL AND EXECUTION**
