# /sh_restore Command - Complete Usage Guide

**Command**: `/sh_restore`
**Purpose**: Restore complete project state from Serena MCP checkpoints
**Skill**: Invokes context-restoration skill (957 lines)
**Output**: Full context restoration with wave/phase/goal/task state rebuilt

---

## Overview

The `/sh_restore` command enables **perfect session resumption** by loading comprehensive checkpoints from Serena MCP. Restores ALL context: specification analysis, wave progress, phase state, North Star goals, architectural decisions, and next actions.

**Core Value**: Zero context loss - resume exactly where you left off, no re-explanation needed.

**Usage**:
```bash
/sh_restore                               # Auto-load most recent checkpoint
/sh_restore {checkpoint_id}               # Load specific checkpoint
/sh_restore --goals                       # Include goal restoration
/sh_restore --verbose                     # Detailed restoration report
```

---

## The 10 Usage Examples

### Example 1: Auto-Restore Most Recent

**Scenario**: Context compaction occurred, need to resume

**Input**:
```bash
/sh_restore
```

**Process**:
```
1. Query Serena for most recent checkpoint:
   list_memories() | filter("shannon_checkpoint_*" OR "shannon_precompact_*")
   Sort by timestamp descending
   Select: shannon_precompact_20251108_220000 (most recent)

2. Load checkpoint data:
   checkpoint = read_memory("shannon_precompact_20251108_220000")

3. Deserialize checkpoint JSON (11 sections)

4. Restore Serena memory keys:
   For each key in checkpoint["serena_memory_keys"]:
     Already in Serena (no action needed)
     Verify accessible: read_memory(key)

5. Rebuild project context:
   - Project: customer_portal
   - Wave: 3 of 4 (75% complete)
   - Phase: 4 of 5 (testing phase)
   - Goal: "Launch MVP to 50 beta users" (80% progress)

6. Restore TodoWrite state:
   - 28 completed tasks
   - 5 active tasks
   - 2 blocked tasks

7. Present restoration report
```

**Output**:
```
✅ CONTEXT RESTORED SUCCESSFULLY

📦 Checkpoint: shannon_precompact_20251108_220000
🕐 Saved: 2025-11-08 22:00:00 (2 hours ago)
📚 Restored: 15/15 memories (100%)
🎯 Quality: 98% (excellent restoration)

## Project State
🔢 Project: customer_portal
📊 Phase: 4 of 5 (Integration & Testing)
🌊 Wave: 3 of 4 (Backend Implementation - 75% complete)

## Current Focus
💡 Implementing Stripe payment integration (Wave 3, 60% done)
   Next: Complete webhook handling, write Puppeteer checkout tests

## Pending Tasks
1. ⏳ Complete Stripe webhook handling
2. ⏳ Write Puppeteer checkout flow tests
3. ⏳ Integrate SendGrid for receipts
4. ⏳ Deploy to staging environment
5. ⏳ Run full E2E test suite

## Completed Waves
✅ Wave 1: Foundation (Database schema, API contracts)
   Completed: 2025-11-07 14:30
   Deliverables: PostgreSQL schema (12 tables), API spec (18 endpoints)

✅ Wave 2: Core Implementation (Frontend + Database)
   Completed: 2025-11-08 09:15
   Deliverables: React components (24), Database migrations (8)

⏳ Wave 3: Backend Implementation (IN PROGRESS - 75%)
   Started: 2025-11-08 14:00
   Progress: Auth complete, Payments 60%, Email pending

## Active Goals
🎯 Launch MVP to 50 beta users: 80%
   Status: On track for launch 2025-11-15

## Next Steps
1. Complete Stripe webhook handling (~2h remaining)
2. Write Puppeteer tests for checkout flow
3. Begin Wave 4 (Integration Testing)

▶️ Ready to continue where you left off.
```

**Key Learning**: Auto-restore intelligently selects most recent checkpoint, rebuilds complete context.

---

### Example 2: Restore Specific Checkpoint

**Scenario**: Need to rollback to specific milestone

**Input**:
```bash
/sh_restore shannon_milestone_20251107_180000
```

**Output**:
```
✅ MILESTONE RESTORED

📦 Checkpoint: shannon_milestone_20251107_180000
🏷️ Label: "Phase 2 complete - Architecture approved"
🕐 Saved: 2025-11-07 18:00:00 (1 day ago)
📚 Restored: 8/8 memories (100%)

## Restored State (1 day ago)
🔢 Project: customer_portal
📊 Phase: 2 of 5 (Architecture & Design)
🌊 Wave: 1 of 4 COMPLETE

## Architecture Decisions (Restored)
1. PostgreSQL for database (over MongoDB)
2. Express with TypeScript for backend
3. Next.js for frontend (SSR + API routes)
4. Stripe for payments
5. Docker for deployment

## What You're Giving Up (from current state)
⚠️ Rolling back from Wave 3 (75% complete) to Wave 1 complete
Lost work:
- Wave 2 deliverables (Frontend components)
- Wave 3 partial (Backend implementation 75%)
- Estimated 12 hours of work

## Restore Confirmation Required
This rollback will lose recent progress. Confirm?
- [ ] YES - Restore to this checkpoint (lose Wave 2-3 work)
- [ ] NO - Keep current state
- [ ] COMPARE - Show diff between states

[User must explicitly confirm rollback]
```

**Key Learning**: Restoring old checkpoints shows what will be lost (safety mechanism).

---

### Example 3: Restore with Goals (--goals)

**Input**:
```bash
/sh_restore --goals
```

**Output**:
```
✅ CONTEXT + GOALS RESTORED

📦 Checkpoint: shannon_checkpoint_20251108_153000
📚 Restored: 12/12 memories + 2 goals

[Standard restoration output...]

## Restored Goals
🎯 PRIMARY: "Launch MVP to 50 beta users by Nov 15"
   Progress: 65% (restored)
   Milestones:
   ✅ User Authentication (100%)
   ✅ Product Catalog (100%)
   ⏳ Shopping Cart (80%)
   ⏳ Checkout Flow (40%)
   ⏳ Admin Dashboard (0%)

🎯 SECONDARY: "Achieve <2s page load time"
   Progress: 30% (restored)
   Metrics:
   ✅ Homepage: 1.2s ✅
   ⚠️ Product page: 2.8s ❌ (needs optimization)
   ⏳ Checkout: Not tested yet

## Goal Alignment
Active wave aligns with goals: ✅
- Wave 3 (Checkout Flow) → PRIMARY goal milestone
- Performance testing planned for Wave 4 → SECONDARY goal

**Goals Guide Next Actions**:
Priority 1: Complete Checkout Flow (PRIMARY 40% → 100%)
Priority 2: Test page load times (SECONDARY validation)
```

**Key Learning**: --goals flag restores North Star context, prioritizes work based on goal alignment.

---

### Example 4: Verbose Restoration (--verbose)

**Input**:
```bash
/sh_restore --verbose
```

**Output**:
```
🔍 DETAILED CONTEXT RESTORATION

📦 Checkpoint Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: shannon_precompact_20251108_220000
Type: precompact (automatic)
Created: 2025-11-08T22:00:00Z (2h 30m ago)
Size: 124 KB (large - comprehensive state)
Integrity: SHA-256 verified ✅

## Restoration Process (Detailed)

Step 1: Load checkpoint from Serena
   Duration: 234ms
   Status: ✅ Success

Step 2: Validate checkpoint integrity
   Checksum: Verified ✅
   Schema version: 4.1.0 ✅
   Serena keys: 15 found

Step 3: Restore Serena memories (15 keys)
   1. spec_analysis_customer_portal ✅ (45 KB)
   2. phase_plan_customer_portal ✅ (32 KB)
   3. wave_1_complete ✅ (56 KB)
   4. wave_2_complete ✅ (78 KB)
   5. wave_3_partial ✅ (92 KB)
   6. architecture_complete ✅ (41 KB)
   7. north_star_goal_mvp ✅ (12 KB)
   8. project_decisions ✅ (28 KB)
   9. integration_status ✅ (18 KB)
   10. test_results_wave_2 ✅ (34 KB)
   11-15. [Additional keys...]

   Total restored: 523 KB
   Duration: 1,234ms

Step 4: Rebuild project context
   Project ID: customer_portal
   Complexity: 0.58 (COMPLEX)
   Domains: Backend 41%, Frontend 33%, Database 26%
   Timeline: 2-3 days (32 hours estimated)
   Elapsed: 18 hours (56% complete)

Step 5: Restore wave state
   Total waves: 4
   Completed: 2 (Wave 1, Wave 2)
   In progress: 1 (Wave 3 - 75%)
   Pending: 1 (Wave 4)

   Wave 3 agents:
   ✅ Frontend integration: Complete
   ⏳ Backend API: 75% (Stripe pending)
   ⏳ Database migrations: 60% (indexes pending)

Step 6: Restore phase state
   Current phase: 4 of 5 (Integration & Testing)
   Phase 3 validation gates: PASSED ✅
   Phase 4 validation gates: In progress (3/5 criteria met)

Step 7: Restore TodoWrite state
   Reconstructed 35 todos:
   - 28 completed ✅
   - 5 active ⏳
   - 2 blocked 🔴

Step 8: Restore architectural decisions (12 decisions)
   1. PostgreSQL over MongoDB (Wave 1, rationale: relational data)
   2. JWT with refresh tokens (Wave 1, rationale: security)
   3. Next.js over React SPA (Wave 1, rationale: SSR + API routes)
   ...
   12. Stripe over PayPal (Wave 2, rationale: better API)

Step 9: Rebuild integration status
   Components built: 47
   Integration points: 12 established, 3 pending
   Tests: 34 Puppeteer tests passing (NO MOCKS ✅)

Step 10: Extract next actions
   Immediate: Complete Stripe webhook handling
   Next: Write checkout flow Puppeteer tests
   Then: Begin Wave 4 (Integration Testing)

## Restoration Quality Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Completeness: 100% (all 15 Serena keys restored)
Integrity: 100% (SHA-256 checksums verified)
Context Accuracy: 98% (minor: 2% inferred from context)
Goal Alignment: 100% (North Star restored)
Decision History: 100% (all 12 decisions preserved)

Overall Quality: 98/100 (EXCELLENT)

## Performance Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total restoration time: 2.1 seconds
Memory loading: 1.2s (15 keys)
Context rebuilding: 0.9s
Presentation: instant

**Restoration successful** ✅

▶️ Resuming work: Complete Stripe webhook handling (Wave 3, 75% → 100%)
```

**Key Learning**: --verbose shows detailed restoration process, quality metrics, performance timing.

---

### Example 5: Restore After Long Break (Multi-Day)

**Scenario**: Returning to project after 1 week

**Input**:
```bash
# Week later, new session
/sh_restore
```

**Output**:
```
✅ CONTEXT RESTORED (After 7-day break)

📦 Checkpoint: shannon_checkpoint_20251101_170000
🕐 Saved: 2025-11-01 17:00:00 (7 days ago)
⚠️ Checkpoint Age: 168 hours (1 week)

## Project State (When You Left Off)
🔢 Project: e_commerce_platform
📊 Phase: 3 of 5 (Implementation - 60% complete)
🌊 Wave: 2 of 5

## Context Refresher (What You Were Building)

**Specification** (restored):
Build e-commerce platform with:
- Product catalog with search
- Shopping cart
- Stripe payment processing
- User accounts
- Admin dashboard
- Complexity: 0.68 (COMPLEX)

**Progress When You Left**:
- Wave 1: Complete (Database + Backend scaffold)
- Wave 2: Complete (Product catalog + Cart)
- Wave 3: Next (Stripe integration + User accounts)

**Decisions Made** (7 days ago):
1. PostgreSQL for database
2. Next.js frontend (SSR)
3. Stripe for payments (over PayPal)
4. Redis for sessions

## Restored Tasks
✅ Completed: 18 tasks
⏳ Active: 7 tasks (where to resume)
   1. Integrate Stripe checkout
   2. Implement user registration
   3. Add cart persistence to Redis
   4. Write Puppeteer checkout tests
   5-7. [More tasks...]

## Memory Refresher

**What's Built**:
- Database: PostgreSQL with 15 tables
- Backend: Express API (24 endpoints)
- Frontend: Product catalog (12 components)
- Tests: 18 Puppeteer tests passing

**What's Next**:
- Stripe integration (Wave 3)
- User accounts (Wave 3)
- Then Wave 4: Integration testing

## Recommended Actions After Long Break
1. Review codebase quickly: ls src/ (see what exists)
2. Run tests to verify state: npm test
3. Check if dependencies outdated: npm outdated
4. Resume Wave 3: Begin Stripe integration

⏰ Estimated to complete: 2 days (12 hours remaining)

▶️ Welcome back! Ready to continue Wave 3.
```

**Key Learning**: Long breaks get extra context (refresher on what was built, decisions made).

---

### Example 6: Partial Restoration (Missing Memories)

**Scenario**: Some Serena memories not found

**Input**:
```bash
/sh_restore shannon_checkpoint_20251106_140000
```

**Output**:
```
⚠️ CONTEXT PARTIALLY RESTORED

📦 Checkpoint: shannon_checkpoint_20251106_140000
📚 Restored: 8/12 memories (67%)

## Successfully Restored
✅ spec_analysis_project
✅ phase_plan_project
✅ wave_1_complete
✅ architecture_complete
✅ north_star_goal
✅ project_decisions
✅ integration_status
✅ test_results

## Missing Memories (4)
❌ wave_2_complete (not found in Serena)
❌ wave_3_results_frontend (not found)
❌ wave_3_results_backend (not found)
❌ advanced_features_plan (not found)

## Impact Assessment

**Can Continue**: YES (with limitations)
- Core context intact (spec, phase plan, architecture)
- Wave 1 preserved
- Goals preserved

**Limitations**:
- Wave 2 deliverables unknown (must infer from codebase)
- Wave 3 results missing (check filesystem for actual work)
- Advanced features undefined (may need re-planning)

## Recommended Recovery

**Option 1: Rebuild Missing Context**
```bash
# Analyze codebase to infer Wave 2 work
/sh_analyze --waves

# Creates wave_2_inferred from filesystem analysis
```

**Option 2: Continue with Partial Context**
```bash
# Review what exists in filesystem
ls src/

# Infer Wave 2 work from files
# Continue from current state
```

**Option 3: Rollback to Earlier Complete Checkpoint**
```bash
/sh_checkpoint --list
# Find earlier checkpoint with 100% restoration
/sh_restore {earlier_checkpoint_id}
```

## Proceeding with Option 1 (Rebuild Missing)
Analyzing codebase to reconstruct Wave 2 context...
```

**Key Learning**: Partial restoration provides options (rebuild, continue, rollback).

---

### Example 7: Restore to Different Branch/Approach

**Scenario**: Exploring alternative approach, want to restore original

**Input**:
```bash
# On experimental branch
git checkout -b experiment

# Try new approach for 3 hours
# [Doesn't work well]

# Restore to main branch approach
git checkout main
/sh_restore shannon_checkpoint_main_20251108
```

**Output**:
```
✅ BRANCH-SPECIFIC RESTORATION

📦 Checkpoint: shannon_checkpoint_main_20251108 (main branch)
🌿 Branch: Restored to 'main' approach

## Context Switch

**Experimental Approach** (discarded):
- Tried: Serverless architecture
- Result: Too complex for timeline
- Time spent: 3 hours

**Main Approach** (restored):
- Architecture: Monolithic Express + PostgreSQL
- Status: Wave 2 complete, Wave 3 pending
- Validated: Architecture approved, tests passing

## Restored Project State
[Standard restoration output...]

## Experiment Captured (For Learning)
Saved experiment notes to:
- Serena: experiment_serverless_attempt_20251108
- Rationale: Complexity too high, timeline insufficient
- Learning: Stick with monolithic for MVP

▶️ Continuing with main branch approach
```

**Key Learning**: Checkpoints enable experimentation with safe rollback.

---

### Example 8: Restore Goal State Only

**Scenario**: Need to remember project goals after context loss

**Input**:
```bash
/sh_restore --goals
```

**Output**:
```
🎯 GOALS RESTORED

📦 Checkpoint: shannon_precompact_20251108_220000

## Active Goals (Restored)

### PRIMARY: "Launch MVP to 50 beta users by Nov 15"
**Progress**: 80%
**Status**: On track
**Deadline**: 2025-11-15 (6 days remaining)

**Milestones**:
✅ User Authentication (100%) - Completed Nov 5
✅ Product Catalog (100%) - Completed Nov 6
✅ Shopping Cart (100%) - Completed Nov 7
⏳ Checkout Flow (60%) - In progress
⏳ Admin Dashboard (20%) - Started Nov 8
⏳ Deployment (0%) - Planned Nov 14

**Blockers**: None
**Risks**: Checkout integration taking longer than expected (+2h)

### SECONDARY: "Achieve 95% Puppeteer test coverage"
**Progress**: 72%
**Status**: Behind (target 80% by now)

**Coverage**:
- Product catalog: 95% ✅
- Shopping cart: 85% ✅
- Checkout: 45% ⚠️ (needs more tests)
- Admin: 30% 🔴 (significantly behind)

**Action Required**: Prioritize checkout and admin test writing

## Goal-Driven Next Actions
1. 🎯 Complete Checkout Flow (PRIMARY 60% → 100%) - 4h
2. 🎯 Write Puppeteer tests for checkout (SECONDARY 45% → 80%) - 2h
3. 🎯 Begin Admin Dashboard (PRIMARY 20% → 60%) - 6h

## Alignment Score: 0.82 / 1.0
Recent work aligns well with goals.

▶️ Focus on PRIMARY goal first (MVP launch)
```

**Key Learning**: --goals focuses restoration on goal state (useful when that's primary concern).

---

### Example 9: Restore from PreCompact Emergency

**Scenario**: Auto-compaction triggered PreCompact hook

**Input**:
```bash
# Context compacted automatically
# New session starts

/shannon:prime --resume
# (Internally uses /sh_restore with most recent precompact)
```

**Output**:
```
🆘 PRECOMPACT CHECKPOINT RESTORED

📦 Checkpoint: shannon_precompact_20251108_235900
🔔 Trigger: Auto-compact (context at 98%)
📚 Restored: 18/18 memories (100%)

## Emergency Preservation Details

**Why PreCompact Fired**:
- Context usage: 980K / 1M tokens (98%)
- Conversation length: 847 messages
- Auto-compact imminent

**What Was Preserved** (11 comprehensive sections):
✅ All Serena memory keys (18 total)
✅ Active wave state (Wave 4, synthesis phase)
✅ Phase state (Phase 5, deployment)
✅ Project context (goals, focus, name)
✅ TodoWrite state (42 todos)
✅ Architectural decisions (15 decisions)
✅ Integration status (components, connections)
✅ Next steps (5 immediate actions)
✅ Performance metrics (18h executed, 3.2x speedup achieved)
✅ Conversation summary (500 chars)
✅ Test results (67 functional tests, NO MOCKS ✅)

## Restored Session State (Exact Moment Before Compaction)

**You Were**:
- Completing Wave 4 synthesis
- About to begin Wave 5 (Deployment)
- All tests passing (67 Puppeteer tests ✅)
- Goal: 95% complete (almost done!)

**Context Preserved**:
Despite 980K → 200K compaction, ZERO information lost
Shannon's PreCompact hook saved everything

**Next Action** (Immediate):
Continue Wave 4 synthesis, get user approval, begin Wave 5

▶️ **ZERO CONTEXT LOSS** - Continue exactly where auto-compact interrupted
```

**Key Learning**: PreCompact checkpoints are COMPREHENSIVE (11 sections), enable perfect resumption after auto-compact.

---

### Example 10: Restore Comparison (Before/After)

**Input**:
```bash
/sh_restore --compare shannon_checkpoint_20251107 shannon_checkpoint_20251108
```

**Output**:
```
🔍 CHECKPOINT COMPARISON

**Checkpoint A**: shannon_checkpoint_20251107_140000 (yesterday)
**Checkpoint B**: shannon_checkpoint_20251108_140000 (today)
**Time Delta**: 24 hours

## Progress Delta Analysis

| Metric | Yesterday (A) | Today (B) | Change |
|--------|---------------|-----------|--------|
| Wave | 1 of 4 (25%) | 3 of 4 (75%) | +2 waves ✅ |
| Phase | 2 of 5 (40%) | 4 of 5 (80%) | +2 phases ✅ |
| Tasks | 8/35 (23%) | 31/35 (89%) | +23 tasks ✅ |
| Files | 12 files | 78 files | +66 files ✅ |
| Tests | 3 tests | 45 tests | +42 tests ✅ |
| Goal | 30% | 85% | +55% ✅ |

## Detailed Changes

**Waves Completed** (between checkpoints):
✅ Wave 2: Core Implementation (completed Nov 7 evening)
   - Frontend: 24 React components
   - Backend: 18 API endpoints
   - Database: 8 migrations

✅ Wave 3: Feature Implementation (completed Nov 8 morning)
   - Stripe integration
   - User accounts
   - Admin dashboard (partial)

**Files Added** (66 new files):
- src/components/*.tsx (24 React components)
- src/pages/*.tsx (8 pages)
- src/api/*.ts (18 endpoints)
- src/tests/*.spec.ts (16 Puppeteer tests)

**Decisions Made** (5 new):
6. Stripe checkout vs custom (chose Stripe)
7. Session storage: Redis vs PostgreSQL (chose Redis)
8. Email service: SendGrid vs AWS SES (chose SendGrid)
9. Image hosting: S3 vs Cloudinary (chose S3)
10. Deployment: ECS vs Lambda (chose ECS)

**Velocity Analysis**:
- Tasks/day: 23 tasks
- Progress/day: 55% goal progress
- Waves/day: 2 waves
- Files/day: 66 files

## Recommendations Based on Delta

**Velocity**: EXCELLENT (2 waves/day, 55% progress/day)
**Trend**: Accelerating (Wave 3 faster than Wave 2)
**Projection**: Wave 4 completion tomorrow (Nov 9)
**Timeline**: ON TRACK (estimated 2-3 days, currently Day 2)

**Maintain Current Velocity**:
✅ Wave synthesis checkpoints working well
✅ No blockers or delays
✅ Test coverage increasing appropriately

**Predicted Completion**: Nov 9 EOD (1 day early!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Restoring to**: Checkpoint B (today) - most recent state
```

**Key Learning**: Comparison analysis shows velocity, trends, projections.

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Assuming Checkpoint Exists Without Verification

**Symptom**:
```bash
/sh_restore some_checkpoint_id
# Checkpoint doesn't exist
# Error: Not found
```

**Shannon Response**:
```
❌ CHECKPOINT NOT FOUND

**Requested**: some_checkpoint_id
**Search Results**: 0 matches in Serena

**Available Checkpoints**:
Run /sh_checkpoint --list to see available checkpoints

**Common Causes**:
1. Typo in checkpoint ID
2. Checkpoint from different project
3. Checkpoint expired (older than retention period)
4. Serena MCP was not configured when checkpoint created

**Resolution**:
1. List checkpoints: /sh_checkpoint --list
2. Copy exact ID from list
3. Retry: /sh_restore {correct_id}
```

**Recommendation**: Use /sh_checkpoint --list first to see available checkpoints.

---

### ❌ Anti-Pattern 2: Restoring Without Reading Restoration Report

**Symptom**:
```bash
/sh_restore
# [Reads restoration output but doesn't review details]
# Starts working on wrong task (not what checkpoint indicated)
```

**Why It Fails**:
- Restoration report shows NEXT ACTIONS (what should be done)
- Ignoring = working on wrong priority
- Goal misalignment

**Shannon Counter**:
```
⚠️ **REVIEW RESTORATION REPORT**

Restoration report shows:
✓ Current focus: "Complete Stripe webhook handling"
✓ Next actions:
   1. Complete Stripe webhook handling (~2h)
   2. Write Puppeteer checkout tests
   3. Begin Wave 4

**You Started Working On**: Admin dashboard

**Issue**: Admin dashboard is Wave 3, but Stripe is incomplete
Wave 3 cannot be marked complete with incomplete work

**Correct Sequence**:
1. Finish Stripe (Wave 3 blocker)
2. Then complete Wave 3 synthesis
3. Then begin Wave 4
4. Admin dashboard in Wave 4 (not Wave 3)

**Please follow Next Actions from restoration report**
```

**Recommendation**: Read and follow "Next Steps" section from restoration report.

---

### ❌ Anti-Pattern 3: Not Verifying Serena MCP Before Restore

**Symptom**:
```bash
# Serena MCP not configured
/sh_restore

# Error: Serena MCP unavailable
```

**Shannon Response**:
```
❌ RESTORATION FAILED - Serena MCP Required

**Issue**: Serena MCP not available
**Impact**: Cannot access checkpoints (stored in Serena)

**Check MCP Status**:
```bash
/sh_check_mcps
```

**If Serena Missing**:
1. Install Serena MCP:
   - See: https://github.com/anthropics/serena-mcp
   - Configure in Claude Code settings

2. Verify installation:
   ```bash
   /list_memories
   # Should work without error
   ```

3. Retry restoration:
   ```bash
   /sh_restore
   ```

**Cannot restore without Serena MCP** (checkpoints live there)
```

**Recommendation**: Run /sh_check_mcps first to verify Serena available.

---

## Integration with Other Commands

### /sh_checkpoint → /sh_restore Flow

**Complete Workflow**:
```bash
# Session 1: Create checkpoint
/sh_checkpoint "Phase 3 complete"

# [Context compaction or session end]

# Session 2: Restore
/sh_restore
# Auto-loads most recent checkpoint
```

---

### /shannon:prime → /sh_restore (V4.1)

**Unified Priming**:
```bash
# V4.1 unified command
/shannon:prime --resume

# Internally executes:
1. Detect mode: resume (vs fresh)
2. Find most recent checkpoint
3. Execute: /sh_restore {checkpoint_id}
4. Execute: /sh_discover_skills
5. Execute: /sh_check_mcps
6. Load: Spec analysis + phase plan
7. Result: Complete session primed (<60s)
```

**Value**: /shannon:prime orchestrates restoration + discovery (faster than manual).

---

## Troubleshooting

### Issue: "Restoration quality low (<70%)"

**Cause**: Checkpoint incomplete or corrupted

**Resolution**:
```bash
# List all checkpoints
/sh_checkpoint --list

# Try earlier checkpoint
/sh_restore {earlier_checkpoint_id}

# If quality still low:
# Manually rebuild context:
1. /sh_analyze (infer from codebase)
2. Review git log (see recent decisions)
3. Reconstruct manually
```

---

### Issue: "Restored to wrong project"

**Cause**: Multiple projects, checkpoint ambiguous

**Resolution**:
```bash
# List checkpoints with project filter
/sh_checkpoint --list | grep project_name

# Restore specific project checkpoint
/sh_restore shannon_checkpoint_{project_name}_*
```

---

### Issue: "Cannot restore - Serena keys missing"

**Cause**: Serena database pruned or corrupted

**Resolution**:
```bash
# Check Serena health
/list_memories

# If many memories missing:
# Serena database may be corrupted

# Recovery:
1. Restore from latest checkpoint that DOES work
2. Or: Analyze codebase to infer state (/sh_analyze)
3. Or: Manual context reconstruction
```

---

## FAQ

**Q: How far back can I restore?**
A: Depends on retention policy:
   - Precompact checkpoints: Indefinite
   - Milestone checkpoints: Indefinite
   - Wave checkpoints: 30 days
   - Manual checkpoints: 30 days
   - Safety checkpoints: 7 days

**Q: What if I want to restore goal but not code state?**
A: Use /sh_restore --goals (restores goals only, keeps current code state)

**Q: Can I restore to a checkpoint from a different computer?**
A: Yes, if Serena MCP synced (cloud-based Serena) or if .serena/ directory copied

**Q: What if restoration fails?**
A: Try earlier checkpoint, check Serena MCP health, or manually rebuild context

**Q: Does restoration overwrite current work?**
A: No - restoration loads context into memory. Current files unchanged. You choose what to do with restored context.

---

**Command**: /sh_restore
**Skill**: context-restoration (shannon-plugin/skills/context-restoration/SKILL.md)
**Examples**: 10 comprehensive scenarios
**Anti-Patterns**: 3 common mistakes
**Integration**: Works with /sh_checkpoint, /shannon:prime
