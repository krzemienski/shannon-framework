---
name: sh:restore
command: /sh:restore
description: "Restore project state from Serena MCP checkpoint"
category: command
purpose: Restore project state from Serena MCP checkpoint
triggers: [restore, resume, recover, reload, continue]
sub_agents: [CONTEXT_GUARDIAN]
mcp_servers: [serena]
priority: critical
---

# /sh:restore - Project State Restoration Command

## Purpose Statement

The `/sh:restore` command restores complete project state from Serena MCP checkpoints, enabling zero context loss after auto-compact events, session breaks, or context loss scenarios. This command activates the CONTEXT_GUARDIAN sub-agent to perform comprehensive context recovery.

**Core Function**: Load checkpoint → Restore all memories → Rebuild context → Resume work seamlessly

**Zero Context Loss Goal**: Restore 100% of project context within 30 seconds

---

## Command Activation

### Primary Trigger
```bash
/sh:restore
```

### Alternative Triggers
```bash
/sh:restore [checkpoint_key]           # Restore specific checkpoint
/sh:restore latest                     # Restore most recent checkpoint
/sh:restore [project_id]               # Restore specific project context
/sh:resume                             # Alias for /sh:restore
/sh:recover                            # Alias for /sh:restore
```

### Auto-Activation Scenarios
1. **Post Auto-Compact**: Detect new conversation thread with active project history
2. **Session Resumption**: User returns after extended break (>4 hours)
3. **Context Loss Detection**: Claude recognizes missing context during active session
4. **Project Switch**: User explicitly switches between multiple projects
5. **Error Recovery**: System failure or unexpected context loss

---

## Usage Patterns

### Pattern 1: Default Restoration (Latest Checkpoint)
```bash
User: /sh:restore
```

**Execution**:
1. Read `latest_checkpoint` pointer from Serena
2. Load most recent checkpoint data
3. Restore all referenced memory keys
4. Validate restoration completeness
5. Present context summary to user
6. Resume from saved state

### Pattern 2: Specific Checkpoint Restoration
```bash
User: /sh:restore precompact_checkpoint_20250930T143000Z
```

**Execution**:
1. Load specified checkpoint directly
2. Restore all referenced memory keys
3. Validate against checkpoint metadata
4. Present restoration details
5. Resume from specified checkpoint state

### Pattern 3: Project Context Switch
```bash
User: /sh:restore project_taskapp
```

**Execution**:
1. Search for most recent checkpoint with project_taskapp ID
2. Load project-specific context
3. Restore wave/phase state
4. Present project status
5. Resume project work

### Pattern 4: Emergency Recovery
```bash
User: /sh:restore fallback
```

**Execution**:
1. Search all checkpoints in reverse chronological order
2. Attempt restoration from each until successful
3. Report which checkpoint was used
4. Highlight any missing or incomplete context
5. Provide recovery recommendations

---

## Execution Flow

### Phase 1: Checkpoint Discovery

**Objective**: Locate the appropriate checkpoint to restore

**CONTEXT_GUARDIAN Actions**:

```python
# Step 1: Determine restoration target
if user_specified_checkpoint:
    checkpoint_key = user_input
elif user_specified_project:
    # Find most recent checkpoint for project
    all_keys = list_memories()
    project_checkpoints = [k for k in all_keys
                          if "checkpoint" in k and project_id in k]
    checkpoint_key = sorted(project_checkpoints, reverse=True)[0]
else:
    # Use latest checkpoint pointer
    checkpoint_key = read_memory("latest_checkpoint")

# Step 2: Validate checkpoint exists
checkpoint_data = read_memory(checkpoint_key)
if not checkpoint_data:
    # Fallback: Find most recent checkpoint
    all_checkpoints = [k for k in list_memories() if "checkpoint" in k]
    checkpoint_key = sorted(all_checkpoints, reverse=True)[0]
    checkpoint_data = read_memory(checkpoint_key)
```

**Success Criteria**:
- ✅ Valid checkpoint located
- ✅ Checkpoint data readable
- ✅ Checkpoint contains required metadata

**Failure Handling**:
- ❌ No checkpoints found → Inform user, cannot restore
- ❌ Checkpoint corrupted → Try next most recent
- ❌ All checkpoints fail → Report complete context loss

---

### Phase 2: Memory Key Restoration

**Objective**: Restore all Serena memory keys referenced in checkpoint

**CONTEXT_GUARDIAN Actions**:

```python
# Step 1: Extract memory key list from checkpoint
memory_keys = checkpoint_data["serena_memory_keys"]
required_keys = checkpoint_data.get("required_keys", [])
optional_keys = checkpoint_data.get("optional_keys", [])

# Step 2: Restore each memory key
restored_memories = {}
failed_keys = []

for key in memory_keys:
    try:
        content = read_memory(key)
        if content is not None:
            restored_memories[key] = content
        else:
            failed_keys.append(key)
    except Exception as e:
        failed_keys.append(key)
        log_error(f"Failed to restore {key}: {e}")

# Step 3: Validate critical memories restored
critical_keys = ["spec_analysis", "phase_plan"]
missing_critical = [k for k in critical_keys
                   if k not in restored_memories]

if missing_critical:
    report_warning(f"Critical memories missing: {missing_critical}")
```

**Memory Restoration Priority**:

1. **Critical** (MUST restore):
   - spec_analysis_*
   - phase_plan_*
   - active_phase_*
   - current_wave_*

2. **Important** (SHOULD restore):
   - wave_*_complete
   - project_decisions_*
   - validation_gates_*

3. **Optional** (NICE to restore):
   - session_*
   - temp_*
   - log_*

**Success Criteria**:
- ✅ All critical memories restored
- ✅ >80% of important memories restored
- ✅ Restoration completed within 30 seconds

---

### Phase 3: Context Reconstruction

**Objective**: Rebuild complete project understanding from restored memories

**CONTEXT_GUARDIAN Actions**:

```python
# Step 1: Extract project metadata
project_id = checkpoint_data["project_id"]
project_phase = checkpoint_data["active_phase"]
current_wave = checkpoint_data.get("current_wave", 1)
total_waves = checkpoint_data.get("total_waves", 1)

# Step 2: Rebuild phase context
if "phase_plan" in restored_memories:
    phase_plan = restored_memories["phase_plan"]
    phase_goals = phase_plan.get("phases", {}).get(project_phase, {})

# Step 3: Rebuild wave context
completed_waves = []
for wave_key in restored_memories:
    if "wave_" in wave_key and "_complete" in wave_key:
        wave_data = restored_memories[wave_key]
        completed_waves.append(wave_data)

# Step 4: Rebuild work context
current_focus = checkpoint_data.get("current_focus", "Unknown")
pending_tasks = checkpoint_data.get("pending_tasks", [])
in_progress_files = checkpoint_data.get("in_progress_files", [])

# Step 5: Rebuild decision context
if "project_decisions" in restored_memories:
    decisions = restored_memories["project_decisions"]
    key_decisions = decisions.get("decisions", [])
```

**Context Validation Checks**:

```python
validation_results = {
    "checkpoint_loaded": checkpoint_data is not None,
    "memories_restored": len(restored_memories) > 0,
    "critical_keys_present": all(k in restored_memories for k in critical_keys),
    "phase_valid": project_phase in ["analysis", "planning", "implementation", "testing", "deployment"],
    "wave_valid": 0 < current_wave <= total_waves,
    "tasks_present": len(pending_tasks) > 0 or current_focus != "Unknown"
}

restoration_quality = sum(validation_results.values()) / len(validation_results)
```

**Success Criteria**:
- ✅ Restoration quality ≥ 80%
- ✅ All critical context elements present
- ✅ Phase and wave state valid

---

### Phase 4: State Resumption

**Objective**: Resume work seamlessly from restored state

**CONTEXT_GUARDIAN Actions**:

```python
# Step 1: Generate restoration report
report = f"""
✅ CONTEXT RESTORED SUCCESSFULLY

📦 Checkpoint: {checkpoint_key}
🕐 Saved: {checkpoint_data['timestamp']}
📚 Restored: {len(restored_memories)}/{len(memory_keys)} memories
🎯 Quality: {restoration_quality*100:.0f}%

## Project State
🔢 Project: {project_id}
📊 Phase: {project_phase}
🌊 Wave: {current_wave}/{total_waves}

## Current Focus
💡 Focus: {current_focus}

## Pending Tasks
{format_task_list(pending_tasks)}

## Completed Waves
{format_wave_summary(completed_waves)}

## Next Steps
{generate_next_steps(project_phase, current_wave, pending_tasks)}

▶️ Ready to continue where you left off.
"""

# Step 2: Log restoration event
write_memory(f"restore_log_{timestamp}", {
    "checkpoint_used": checkpoint_key,
    "memories_restored": len(restored_memories),
    "failed_keys": failed_keys,
    "restoration_quality": restoration_quality,
    "timestamp": timestamp,
    "success": restoration_quality >= 0.8
})

# Step 3: Update session state
write_memory("current_session", {
    "project_id": project_id,
    "active_phase": project_phase,
    "current_wave": current_wave,
    "restored_from": checkpoint_key,
    "session_start": timestamp
})

# Step 4: Present report to user
print(report)

# Step 5: Resume execution
if pending_tasks:
    # Resume first pending task
    resume_task(pending_tasks[0])
elif in_progress_files:
    # Resume work on in-progress files
    resume_file_work(in_progress_files)
else:
    # Wait for user direction
    await_user_input()
```

---

## Sub-Agent Integration: CONTEXT_GUARDIAN

### CONTEXT_GUARDIAN Persona

**Identity**: Context preservation specialist focused on zero data loss

**Responsibilities**:
1. Checkpoint discovery and validation
2. Memory key restoration with priority handling
3. Context reconstruction and validation
4. State resumption coordination
5. Error recovery and fallback strategies

**Decision Framework**:
- **Completeness > Speed**: Prioritize restoring all context over quick restoration
- **Validation > Assumption**: Validate every restored element
- **Recovery > Failure**: Always attempt fallback strategies before reporting failure

**Communication Style**:
- Clear status updates during multi-step restoration
- Transparent about missing or failed memories
- Detailed restoration reports with quality metrics
- Actionable recommendations for incomplete restorations

---

### CONTEXT_GUARDIAN Activation

**Trigger**: `/sh:restore` command execution

**Initialization**:
```python
# CONTEXT_GUARDIAN receives:
context_guardian_input = {
    "command": "/sh:restore",
    "user_args": {
        "checkpoint_key": checkpoint_key,  # Optional
        "project_id": project_id,          # Optional
        "restoration_mode": "latest|specific|fallback"
    },
    "current_session": {
        "session_id": session_id,
        "conversation_context": conversation_summary
    },
    "restoration_requirements": {
        "critical_keys": ["spec_analysis", "phase_plan"],
        "min_quality_threshold": 0.8,
        "max_restoration_time": 30  # seconds
    }
}
```

**Execution Authority**:
- ✅ Full access to all Serena MCP read operations
- ✅ Authority to create restoration logs
- ✅ Authority to update session state
- ❌ NO write access to original checkpoint data (read-only)

---

## Output Format

### Successful Restoration Output

```markdown
✅ CONTEXT RESTORED SUCCESSFULLY

📦 Checkpoint: precompact_checkpoint_20250930T143000Z
🕐 Saved: 2025-09-30T14:30:00Z
📚 Restored: 12/12 memories (100%)
🎯 Quality: 95%

## Project State
🔢 Project: shannon_taskapp
📊 Phase: implementation
🌊 Wave: 3/5

## Current Focus
💡 Implementing JWT authentication system with refresh tokens

## Pending Tasks
1. ⏳ Complete token generation logic (auth.ts:45)
2. ⏳ Add refresh token endpoint (api/auth/refresh.ts)
3. ⏳ Test full authentication flow
4. ⏳ Update API documentation

## Completed Waves
✅ Wave 1: Frontend Components (2025-09-30)
   - Login/Register forms
   - User profile dashboard
   - Navigation components

✅ Wave 2: Backend API Structure (2025-09-30)
   - Express server setup
   - Database models
   - Base API routes

🔄 Wave 3: Authentication System (IN PROGRESS)
   - JWT implementation (80% complete)
   - Token refresh logic (pending)

## Key Decisions
📝 2025-09-30T12:00:00Z - Use JWT over session-based auth
   Rationale: Stateless, scalable, industry standard

📝 2025-09-30T13:15:00Z - Implement refresh token rotation
   Rationale: Enhanced security, prevents token theft

## Next Steps
1. Resume token generation in auth.ts
2. Complete refresh token endpoint
3. Run authentication flow tests
4. Update API documentation with auth endpoints

▶️ Ready to continue where you left off.
```

---

### Partial Restoration Output

```markdown
⚠️ CONTEXT PARTIALLY RESTORED

📦 Checkpoint: manual_checkpoint_20250929T180000Z
🕐 Saved: 2025-09-29T18:00:00Z
📚 Restored: 8/12 memories (67%)
🎯 Quality: 70%

## Restoration Status
✅ Critical memories restored:
   - spec_analysis_001
   - phase_plan_001

⚠️ Missing memories:
   - wave_2_results_backend (failed to load)
   - project_decisions_recent (not found)
   - session_temp_state (expired)

## Project State
🔢 Project: shannon_taskapp
📊 Phase: implementation (restored)
🌊 Wave: 2/5 (partial context)

## Current Focus
💡 Backend API development (some context missing)

## Recommendations
1. Review Wave 2 progress manually
2. Recreate missing decision log
3. Consider creating new checkpoint after validation

## Recovery Options
- Option A: Continue with partial context (risk: incomplete understanding)
- Option B: Restore from older checkpoint with complete data
- Option C: Manually rebuild missing context elements

Would you like to:
1. Continue with current restoration
2. Try alternative checkpoint
3. Review missing memories in detail
```

---

### Failed Restoration Output

```markdown
❌ RESTORATION FAILED

📦 Attempted checkpoint: latest_checkpoint
⚠️ Status: No valid checkpoints found

## Issue Details
- No checkpoint pointer in Serena
- No checkpoint memories found
- Project context appears to be lost

## Possible Causes
1. PreCompact hook did not execute
2. Checkpoints were manually deleted
3. New project with no prior checkpoints
4. Serena MCP storage issue

## Recovery Steps
1. List all available memories: /sh:list-context
2. Attempt manual context reconstruction
3. Check for backup checkpoint files
4. Start fresh session with new checkpoint

## Prevention
- Verify PreCompact hook is installed: ~/.claude/hooks/precompact.py
- Create manual checkpoints regularly: /sh:checkpoint
- Test restoration after important work: /sh:restore --dry-run

Would you like to:
1. Search for any recoverable context
2. Start fresh with new checkpoint
3. View troubleshooting guide
```

---

## Examples

### Example 1: Post Auto-Compact Restoration

```bash
# User notices context loss after auto-compact
User: /sh:restore

# CONTEXT_GUARDIAN activates
✅ CONTEXT RESTORED SUCCESSFULLY

📦 Checkpoint: precompact_checkpoint_20250930T143000Z
🕐 Saved: 2025-09-30T14:30:00Z (5 minutes ago)
📚 Restored: 15/15 memories (100%)
🎯 Quality: 100%

## Auto-Compact Recovery
✅ PreCompact checkpoint was saved successfully
✅ All wave progress preserved
✅ No context lost during compaction

## Project State
🔢 Project: enterprise_dashboard
📊 Phase: testing
🌊 Wave: 4/5

## Current Focus
💡 Running E2E tests for user authentication flow

▶️ Resuming test execution...
```

---

### Example 2: Project Context Switch

```bash
# User switches between projects
User: I need to work on the blog project now
User: /sh:restore project_blog

# CONTEXT_GUARDIAN switches context
✅ PROJECT CONTEXT SWITCHED

📦 Previous: enterprise_dashboard (checkpoint saved)
📦 Loading: project_blog
🕐 Last activity: 2025-09-28T16:30:00Z (2 days ago)

## Project State
🔢 Project: project_blog
📊 Phase: implementation
🌊 Wave: 2/3

## Progress Summary
✅ Wave 1: Content management system (complete)
🔄 Wave 2: User commenting system (75% complete)
⏳ Wave 3: Email notifications (pending)

## Current Focus
💡 Completing comment moderation interface

## Pending Tasks
1. ⏳ Add comment approval workflow
2. ⏳ Implement spam filtering
3. ⏳ Create admin moderation panel

▶️ Ready to continue blog project development.
```

---

### Example 3: Fallback Recovery

```bash
# Latest checkpoint corrupted
User: /sh:restore

⚠️ Primary checkpoint failed, attempting fallback...

✅ CONTEXT RESTORED FROM FALLBACK

📦 Checkpoint: manual_checkpoint_20250930T120000Z
🕐 Saved: 2025-09-30T12:00:00Z (2 hours ago)
📚 Restored: 10/12 memories (83%)
🎯 Quality: 85%

## Fallback Notice
⚠️ Most recent checkpoint (14:30) was corrupted
✅ Restored from manual checkpoint (12:00)
⚠️ ~2 hours of progress may need review

## Missing Context
- Changes between 12:00 and 14:30
- Most recent task updates
- Latest commit decisions

## Recommendations
1. Review git commits since 12:00
2. Check file modification timestamps
3. Recreate recent decisions if needed
4. Create new checkpoint after validation

▶️ Context restored. Please verify recent changes.
```

---

## Success Criteria

**Restoration Quality Metrics**:
- ✅ Critical memories: 100% restoration required
- ✅ Important memories: ≥80% restoration target
- ✅ Overall quality: ≥80% for successful restoration
- ✅ Restoration time: <30 seconds target
- ✅ User satisfaction: Seamless continuation of work

**Context Completeness**:
- ✅ Project phase and wave state accurate
- ✅ All completed wave results accessible
- ✅ Current focus and pending tasks clear
- ✅ Key decisions documented and available
- ✅ File states and changes tracked

---

## Integration Points

### PreCompact Hook Integration
- Hook creates checkpoint → /sh:restore reads checkpoint
- Automatic failsafe against context loss
- Seamless pre/post compact workflow

### Wave Orchestration Integration
- Wave completion creates checkpoint
- /sh:restore loads wave context for next wave
- Cross-wave context preservation

### Sub-Agent Integration
- All sub-agents can trigger /sh:restore
- Sub-agents load context before execution
- Consistent context across agent handoffs

---

## Best Practices

1. **Always validate restoration quality** - Don't proceed if quality <80%
2. **Report missing memories transparently** - User needs to know what's lost
3. **Provide recovery options** - Offer alternatives when primary restore fails
4. **Log all restoration events** - Maintain audit trail for debugging
5. **Test restoration regularly** - Verify checkpoints are restorable
6. **Use fallback strategies** - Never report total failure without trying alternatives
7. **Maintain session continuity** - Restore should feel seamless to user

---

**Result**: Zero context loss through comprehensive checkpoint restoration powered by CONTEXT_GUARDIAN and Serena MCP integration.