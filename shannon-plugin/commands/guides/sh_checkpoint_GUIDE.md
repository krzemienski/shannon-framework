# /sh_checkpoint Command - Complete Usage Guide

**Command**: `/sh_checkpoint`
**Purpose**: Create and manage session checkpoints for zero-context-loss workflows
**Skill**: Invokes context-preservation skill (562 lines)
**Output**: Comprehensive checkpoint saved to Serena MCP with restoration command

---

## Overview

The `/sh_checkpoint` command creates **comprehensive session snapshots** that preserve ALL project state (wave progress, goals, decisions, files, tests) enabling seamless restoration after context loss.

**Core Value**: Insurance against context compaction - no information loss ever.

**When to Use**:
- After major milestones (wave complete, phase complete, MVP launch)
- Before risky changes (architecture refactor, major dependency upgrade)
- Every 2-3 hours of continuous work (preventive checkpoints)
- Before leaving long-running session
- When manually requested by user

**Usage**:
```bash
/sh_checkpoint                            # Auto-labeled checkpoint
/sh_checkpoint "Phase 2 complete"         # Custom label
/sh_checkpoint --list                     # Show all checkpoints
/sh_checkpoint --load {checkpoint_id}     # Restore specific checkpoint
```

---

## The 10 Usage Examples

### Example 1: Basic Manual Checkpoint

**Input**:
```bash
/sh_checkpoint
```

**Output**:
```
✅ CHECKPOINT CREATED

**Checkpoint ID**: shannon_checkpoint_20251108_213000
**Label**: "Manual checkpoint"
**Type**: manual
**Size**: 45 KB

📦 Captured:
   - 12 entities, 18 relations
   - 15 completed tasks, 3 active
   - Wave 2 of 4, Phase 3 of 5
   - North Star alignment: 0.85

💾 Storage: Serena MCP
🔄 Restore: /sh_checkpoint --load shannon_checkpoint_20251108_213000
⏰ Expires: 2025-12-08 (30 days)

**Next Actions**:
- Complete Wave 2 synthesis
- Begin Wave 3 (Backend implementation)
```

**Key Learning**: No label needed - auto-generates with timestamp.

---

### Example 2: Custom-Labeled Checkpoint

**Input**:
```bash
/sh_checkpoint "MVP launch - all features complete, tests passing"
```

**Output**:
```
✅ CHECKPOINT CREATED

**Checkpoint ID**: shannon_checkpoint_20251108_213500
**Label**: "MVP launch - all features complete, tests passing"
**Type**: milestone
**Size**: 67 KB

📦 Captured:
   - 24 entities, 35 relations (large project)
   - Wave 5 of 5 COMPLETE ✅
   - Phase 5 of 5 COMPLETE ✅
   - All tests: 45 functional tests passing (NO MOCKS)
   - Goal: "Launch MVP to 100 beta users" - 100% complete

💾 Storage: Serena MCP
🔄 Restore: /sh_checkpoint --load shannon_checkpoint_20251108_213500

**Milestone Significance**:
This checkpoint marks production-ready state. Can roll back to this point if post-launch issues occur.
```

**Key Learning**: Custom labels make checkpoints easier to identify (especially for milestones).

---

### Example 3: List Available Checkpoints

**Input**:
```bash
/sh_checkpoint --list
```

**Output**:
```
📋 AVAILABLE CHECKPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. shannon_precompact_20251108_220000 (5 minutes ago)
   Label: "Auto-checkpoint before compaction"
   Type: precompact (automatic)
   Wave: 3, Phase: 4
   Progress: 18/25 tasks (72%)
   Size: 89 KB

2. shannon_checkpoint_20251108_213500 (1 hour ago)
   Label: "MVP launch - all features complete"
   Type: milestone
   Wave: 5 COMPLETE, Phase: 5 COMPLETE
   Progress: 45/45 tasks (100%)
   Size: 67 KB

3. wave_2_complete_20251108_180000 (5 hours ago)
   Label: "Wave 2 synthesis checkpoint"
   Type: wave-checkpoint (automatic)
   Wave: 2, Phase: 3
   Progress: 12/25 tasks (48%)
   Size: 52 KB

4. shannon_checkpoint_20251107_153000 (1 day ago)
   Label: "Phase 1 complete, architecture approved"
   Type: manual
   Wave: 1, Phase: 1
   Progress: 5/25 tasks (20%)
   Size: 34 KB

5. shannon_checkpoint_20251106_143000 (2 days ago)
   Label: "Initial specification analysis complete"
   Type: manual
   Wave: N/A, Phase: 1
   Progress: 2/25 tasks (8%)
   Size: 28 KB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Restore**: /sh_checkpoint --load {checkpoint_id}
**Most Recent**: shannon_precompact_20251108_220000 (auto-selected by /sh_restore)
```

**Key Learning**: --list shows ALL checkpoint types (manual, wave, precompact, milestone).

---

### Example 4: Wave Boundary Checkpoint (Automatic)

**Context**: WAVE_COORDINATOR completes Wave 2

**Automatic Execution**:
```
Wave 2 agents complete → WAVE_COORDINATOR synthesizes → Checkpoint auto-created
```

**Process**:
```
1. wave-orchestration skill detects Wave 2 complete
2. Invokes context-preservation automatically:
   /sh_checkpoint "Wave 2 complete"

3. Checkpoint captures:
   - Wave 2 deliverables (files created, components built)
   - Agent results (all 3 agents' work)
   - Integration status
   - Next wave requirements (Wave 3 needs X, Y, Z)
```

**Output**:
```
✅ WAVE CHECKPOINT CREATED (automatic)

**Checkpoint ID**: wave_2_complete_20251108_214000
**Label**: "Wave 2 complete - Foundation implementation"
**Type**: wave-checkpoint
**Wave**: 2 of 4

📦 Wave 2 Deliverables:
   - Database schema (12 tables, 8 relationships)
   - Backend API (18 endpoints, all tested)
   - Frontend scaffold (10 pages, 25 components)
   - Tests: 22 functional tests passing (NO MOCKS)

🔄 Next Wave Preview:
   Wave 3: Feature Implementation (5 agents, 6h)
   - User management
   - Content creation
   - Search functionality

💾 Auto-saved to Serena MCP
🔄 Restore: /sh_restore wave_2_complete_20251108_214000
```

**Key Learning**: Wave checkpoints auto-created by wave-orchestration (user doesn't call /sh_checkpoint explicitly).

---

### Example 5: PreCompact Emergency Checkpoint (Automatic)

**Context**: Context usage at 95%, Claude Code about to auto-compact

**Automatic Trigger**:
```
Context: 950K tokens / 1M limit (95%)
  ↓
PreCompact event fires
  ↓
precompact.py hook generates instructions
  ↓
CONTEXT_GUARDIAN invokes context-preservation:
  /sh_checkpoint "PreCompact emergency" (automatic)
  ↓
Comprehensive checkpoint saved (11 sections)
  ↓
Auto-compaction proceeds safely
```

**Output**:
```
🆘 PRECOMPACT CHECKPOINT CREATED (emergency)

**Checkpoint ID**: shannon_precompact_20251108_220000
**Trigger**: Auto-compact (context at 95%)
**Type**: precompact (automatic)
**Size**: 124 KB (large - comprehensive state)

📦 Comprehensive Capture:
   - All 15 Serena memory keys preserved
   - Active wave state (Wave 3, 65% complete)
   - Phase state (Phase 4, testing in progress)
   - 23 completed tasks, 8 active, 2 blocked
   - 12 architectural decisions
   - 35 files modified since last checkpoint
   - North Star goal: "Launch Q1 2025" (78% progress)

🔄 Restore: /shannon:prime --resume
   (Auto-detects most recent precompact checkpoint)

⏰ Expires: Never (precompact checkpoints retained indefinitely)

**Context Compaction Proceeding**:
950K → ~200K (conversation history compressed)
Checkpoint ensures ZERO information loss
```

**Key Learning**: PreCompact checkpoints are LARGEST (comprehensive) and auto-expire never (critical for recovery).

---

### Example 6: Milestone Checkpoint (Custom Type)

**Input**:
```bash
/sh_checkpoint "🎉 Version 1.0 Released to Production"
```

**Output**:
```
✅ MILESTONE CHECKPOINT CREATED

**Checkpoint ID**: shannon_milestone_20251108_220500
**Label**: "🎉 Version 1.0 Released to Production"
**Type**: milestone (auto-detected from celebration emoji)
**Size**: 98 KB

📦 Production Release State:
   - All 5 waves COMPLETE ✅
   - All 5 phases COMPLETE ✅
   - 156 files in production
   - 89 functional tests passing (NO MOCKS)
   - Deployment: https://app.example.com (LIVE)
   - North Star: "Launch v1.0" - 100% ACHIEVED 🎉

💾 Tagged: production-v1.0
🔄 Rollback: /sh_restore shannon_milestone_20251108_220500
   (If production issues, restore to this state)

⏰ Retention: Permanent (milestone checkpoints never expire)

**Deployment Info Captured**:
- Deployment URL
- Release notes
- Database migration version
- Infrastructure state (Docker images, K8s configs)
- Performance metrics (baseline for monitoring)
```

**Key Learning**: Milestone checkpoints (with celebration emojis or "release/launch" keywords) get permanent retention.

---

### Example 7: Before Risky Changes

**Input**:
```bash
# Before major refactor
/sh_checkpoint "Before database schema migration - rollback point"
```

**Output**:
```
✅ SAFETY CHECKPOINT CREATED

**Checkpoint ID**: shannon_checkpoint_20251108_221000
**Label**: "Before database schema migration - rollback point"
**Type**: safety (auto-detected from "before" + "rollback")
**Size**: 56 KB

📦 Pre-Migration State:
   - Database schema v2.3 (current)
   - All migrations applied: 001-045
   - Data: 15K records (production)
   - Tests: 34 passing (baseline)

🔄 Rollback Available:
   If migration fails:
   1. /sh_restore shannon_checkpoint_20251108_221000
   2. Revert migration: git reset --hard {commit_sha}
   3. Database: restore from checkpoint state

⏰ Expires: 7 days (safety checkpoints short retention)

**Risky Change Ahead**:
Checkpoint ensures you can restore if schema migration causes issues.
```

**Key Learning**: "Before" + risky keywords → safety checkpoint (short retention, optimized for rollback).

---

### Example 8: Periodic Work Checkpoint

**Input**:
```bash
# After 2.5 hours of work
/sh_checkpoint "End of day progress - partial Wave 3"
```

**Output**:
```
✅ WORK SESSION CHECKPOINT

**Checkpoint ID**: shannon_checkpoint_20251108_221500
**Label**: "End of day progress - partial Wave 3"
**Type**: work-session
**Size**: 41 KB

📦 Session Progress:
   - Duration: 2.5 hours
   - Wave 3: 40% complete (2/5 agents done)
   - Files modified: 18 files (8 new, 10 edited)
   - Tests added: 6 Puppeteer tests
   - North Star: 68% → 72% (+4% this session)

🔄 Tomorrow: /shannon:prime --resume
   Auto-loads this checkpoint
   Continues where you left off

**Incomplete Work**:
⚠️ Wave 3 agents still running:
  - Agent 3: Payment integration (60% complete)
  - Agent 4: Admin dashboard (30% complete)
  - Agent 5: Notification system (not started)

**Resume Strategy**:
  Option A: Wait for agents to complete, then checkpoint
  Option B: Save partial state now, respawn agents tomorrow
```

**Key Learning**: Periodic checkpoints capture partial progress - useful for multi-day work.

---

### Example 9: Checkpoint Comparison

**Input**:
```bash
/sh_checkpoint --compare shannon_checkpoint_20251107 shannon_checkpoint_20251108
```

**Output**:
```
🔍 CHECKPOINT COMPARISON

**Checkpoint A**: shannon_checkpoint_20251107 (yesterday)
**Checkpoint B**: shannon_checkpoint_20251108 (today)
**Time Delta**: 1 day

## Progress Comparison

| Metric | Checkpoint A | Checkpoint B | Delta |
|--------|--------------|--------------|-------|
| Wave | 1 of 4 | 3 of 4 | +2 waves |
| Phase | 2 of 5 | 4 of 5 | +2 phases |
| Tasks | 8/35 (23%) | 28/35 (80%) | +20 tasks |
| Files | 12 files | 64 files | +52 files |
| Tests | 3 tests | 34 tests | +31 tests |
| Goal | 25% | 80% | +55% |

## Detailed Changes

**Files Added** (52 new files):
- src/components/*.tsx (24 components)
- src/pages/*.tsx (8 pages)
- src/api/*.ts (12 endpoints)
- src/tests/*.spec.ts (8 test files)

**Architectural Decisions** (5 new):
1. Chose PostgreSQL over MongoDB (Wave 1)
2. Implemented JWT auth with refresh tokens (Wave 2)
3. Selected Stripe for payment processing (Wave 2)
4. Adopted Puppeteer for functional testing (Wave 3)
5. Deployed to AWS ECS (Wave 3)

**Velocity Analysis**:
- Tasks/day: 20 tasks
- Progress/day: 55%
- Projected completion: Tomorrow (1 more day at current velocity)

**Recommendation**: Maintain current velocity, expect completion in 1 day.
```

**Key Learning**: Checkpoint comparison shows quantitative progress over time.

---

### Example 10: Cross-Project Checkpoint Patterns

**Input**:
```bash
/sh_checkpoint --pattern analysis
```

**Output**:
```
📊 CHECKPOINT PATTERN ANALYSIS (Last 10 Checkpoints)

## Checkpoint Frequency

**Average Time Between Checkpoints**: 3.2 hours
**Most Common Labels**:
1. "Wave N complete" (40% of checkpoints)
2. "Phase N complete" (25%)
3. "Manual checkpoint" (20%)
4. "PreCompact emergency" (10%)
5. Custom milestones (5%)

## Checkpoint Sizes

**Average**: 58 KB
**Largest**: 124 KB (precompact checkpoint - comprehensive)
**Smallest**: 28 KB (early phase checkpoint - minimal state)

**Size Trend**: Grows 15-20 KB per wave (accumulating context)

## Recovery Usage

**Checkpoints Restored**: 3 times (last 30 days)
**Reasons**:
1. Context compaction (auto-restore via /shannon:prime)
2. Session interruption (manually restored)
3. Architecture rollback (reverted after failed migration)

**Recovery Success**: 100% (all checkpoints restored successfully)

## Recommendations

**Your Checkpoint Strategy**:
✅ GOOD: Checkpointing every 3.2h (recommended 2-4h)
✅ GOOD: Wave boundary checkpoints (100% coverage)
⚠️ IMPROVE: Add more safety checkpoints before risky changes

**Suggested**:
- Checkpoint before major refactors
- Checkpoint before dependency upgrades
- Checkpoint before deploying to production
```

**Key Learning**: Checkpoint patterns reveal project health and recovery readiness.

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Not Checkpointing Because "Quick Task"

**Symptom**:
```
User: "This is just a quick fix, no need to checkpoint"
[Makes changes for 2 hours]
[Context compaction happens]
[Lost 2 hours of work]
```

**Shannon Counter**:
```
⚠️ **CHECKPOINT RECOMMENDED**

**Reason**: "Quick" tasks often take longer than expected

**Statistics**:
- Tasks estimated <30 min actually take: 1-2 hours (66% avg)
- Risk of context compaction increases with time
- Checkpoint takes: 30 seconds
- Restoration from lost work: 2+ hours

**ROI**: 30s investment prevents 2h recovery

**Action**: Create checkpoint NOW
```

**Recommendation**: Checkpoint at session start, regardless of perceived task size.

---

### ❌ Anti-Pattern 2: Relying Only on PreCompact (No Manual Checkpoints)

**Symptom**:
```
User never runs /sh_checkpoint manually
Only PreCompact auto-checkpoints exist
```

**Why It Fails**:
- PreCompact fires at 95% context (emergency, not ideal)
- No labeled milestones (hard to find "Phase 2 complete")
- Miss opportunity for safety checkpoints before risky changes

**Recommendation**:
```
**Checkpoint Strategy** (layered):

1. **PreCompact** (automatic): Emergency only
2. **Wave Checkpoints** (automatic): After each wave
3. **Manual Checkpoints** (user-initiated):
   - After phases complete
   - Before risky changes
   - At end of work session
   - Major milestones

**Frequency**: Every 2-3 hours manually + automatic
```

---

### ❌ Anti-Pattern 3: Vague Labels Making Restoration Confusing

**Symptom**:
```bash
/sh_checkpoint "checkpoint 1"
/sh_checkpoint "checkpoint 2"
/sh_checkpoint "done"
```

**Later**:
```bash
/sh_checkpoint --list

# Output shows:
1. checkpoint 1
2. checkpoint 2
3. done

# User: "Which one was the working version before the bug?"
# Can't tell from labels
```

**Better Labels**:
```bash
/sh_checkpoint "Wave 2 complete - auth working, before payment integration"
/sh_checkpoint "Payment integration complete - Stripe test mode passing"
/sh_checkpoint "Production-ready - all tests passing, deployment validated"
```

**Recommendation**: Descriptive labels (what was accomplished + what's next).

---

## Integration with Other Commands

### /sh_checkpoint → /sh_restore

**Recovery Workflow**:
```bash
# Session 1: Create checkpoint
/sh_checkpoint "Phase 3 complete, all features implemented"

# [Session ends or context compaction occurs]

# Session 2: Restore
/sh_restore  # Auto-loads most recent
# OR
/sh_restore shannon_checkpoint_20251108_213000  # Specific checkpoint
```

---

### /sh_wave → /sh_checkpoint (Automatic)

**Integration**:
```
Wave execution automatically creates checkpoints:

Wave 1 complete → /sh_checkpoint "Wave 1 complete" (automatic)
Wave 2 complete → /sh_checkpoint "Wave 2 complete" (automatic)
...

User doesn't call /sh_checkpoint manually during waves
```

---

## Troubleshooting

### Issue: "Checkpoint save failed"

**Symptoms**:
- /sh_checkpoint runs but no confirmation
- Serena MCP errors

**Diagnosis**:
```bash
# Test Serena MCP
/list_memories
# If error → Serena not configured

# Check .serena directory
ls .serena/
# Should exist

# Test write
/create_entities [...]
# Should succeed
```

**Resolution**:
- Install/configure Serena MCP
- Verify .serena/ directory permissions
- Check disk space (checkpoints can be 100+ KB)

---

### Issue: "Checkpoint list empty but checkpoints exist"

**Cause**: Checkpoints in different Serena namespace

**Resolution**:
```bash
# List ALL Serena memories
/list_memories

# Look for:
# - shannon_checkpoint_*
# - wave_*_complete
# - precompact_*

# Restore manually:
/sh_restore {full_checkpoint_id}
```

---

## FAQ

**Q: How often should I checkpoint?**
A: Every 2-3 hours manually + automatic wave/precompact checkpoints

**Q: Do checkpoints slow down work?**
A: No. Takes 30s to create, saves hours if recovery needed. ROI: 100:1

**Q: How long are checkpoints retained?**
A:
  - Manual: 30 days
  - Wave: 30 days
  - PreCompact: Indefinite
  - Milestone: Indefinite
  - Safety: 7 days

**Q: Can I delete checkpoints?**
A: Yes, via Serena MCP directly (delete_entities). Not recommended for milestones.

**Q: What if Serena MCP unavailable?**
A: Checkpoints fail. Serena is MANDATORY for Shannon. Install before using /sh_checkpoint.

---

**Command**: /sh_checkpoint
**Skill**: context-preservation (shannon-plugin/skills/context-preservation/SKILL.md)
**Examples**: 10 comprehensive scenarios
**Anti-Patterns**: 3 common mistakes
**Integration**: Auto-checkpoints from /sh_wave, restoration via /sh_restore
