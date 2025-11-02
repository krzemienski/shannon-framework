# PROJECT_MEMORY.md - Project Memory Management System

## Purpose

This document defines behavioral patterns for storing, retrieving, and managing project context across sessions using Serena MCP. Project memory enables Shannon to maintain complete understanding of projects across auto-compact events, session breaks, and context interruptions.

**Core Objective**: Never lose project context, decisions, or progress through systematic memory management.

---

## What is Project Memory?

Project memory is the persistent storage of project-related information in Serena MCP that survives:
- Auto-compact events (conversation compression)
- Session endings (user closes Claude Code)
- Context loss (window fills up)
- Multi-day breaks (user returns days later)
- Project switching (moving between different projects)

**Key Insight**: Project memory transforms ephemeral conversation into permanent project knowledge.

---

## Memory Structure

### Hierarchical Memory Organization

Shannon uses a 5-level memory hierarchy optimized for discovery, restoration, and cleanup:

```yaml
# LEVEL 1: Project Foundation (Indefinite Retention)
project_[id]_spec_analysis          # Original specification analysis
project_[id]_phase_plan             # 5-phase execution plan
project_[id]_decisions              # Architectural decisions log
project_[id]_final_results          # Project completion summary

# LEVEL 2: Wave Context (30-Day Retention)
project_[id]_wave_[n]_plan          # Wave execution plan
project_[id]_wave_[n]_complete      # Wave completion results
project_[id]_wave_[n]_[component]   # Component-specific results

# LEVEL 3: Phase Context (30-Day Retention)
project_[id]_phase_[name]_start     # Phase initialization context
project_[id]_phase_[name]_complete  # Phase completion status
project_[id]_phase_[name]_gates     # Validation gate results

# LEVEL 4: Session State (7-Day Retention)
session_[id]_active_work            # Current work in progress
session_[id]_todo_list              # Session-specific tasks
session_[id]_focus                  # Current focus area

# LEVEL 5: Checkpoints (Recovery Points)
precompact_checkpoint_[timestamp]   # Auto-saved before compact
manual_checkpoint_[name]_[ts]       # User-requested checkpoint
phase_checkpoint_[phase]_[ts]       # Phase transition checkpoint
wave_checkpoint_[wave]_[ts]         # Wave completion checkpoint
```

---

## Session Lifecycle

### Session Start: Context Loading

**When Starting Any Session**:

1. **Detect Project Context**
   - Check if user mentions project name
   - Look for project files in working directory
   - Check for recent project activity

2. **Load Project Foundation**
   ```python
   # Step 1: Check for existing project memory
   all_keys = list_memories()
   project_keys = [k for k in all_keys if k.startswith("project_")]

   # Step 2: If project found, load foundation
   if project_keys:
       spec = read_memory("project_[id]_spec_analysis")
       plan = read_memory("project_[id]_phase_plan")
       decisions = read_memory("project_[id]_decisions")
   ```

3. **Load Latest Checkpoint**
   ```python
   # Step 3: Find most recent checkpoint
   latest_checkpoint = read_memory("latest_checkpoint")

   # Step 4: Restore session state
   if latest_checkpoint:
       checkpoint_data = read_memory(latest_checkpoint)
       restore_session_state(checkpoint_data)
   ```

4. **Confirm Context Loaded**
   ```
   ✅ Project Context Loaded

   📦 Project: [project_name]
   🔄 Phase: [current_phase]
   🎯 Wave: [current_wave]/[total_waves]
   📋 Active Tasks: [count]
   ```

---

### Session Active: Continuous Saving

**During Active Work**:

1. **Save Decisions Immediately**
   ```python
   # Every architectural decision
   write_memory(f"decision_{topic}_{timestamp}", {
       "decision": "What was decided",
       "rationale": ["Reason 1", "Reason 2"],
       "alternatives": ["Option A (rejected)", "Option B (rejected)"],
       "impact": "What this affects",
       "date": timestamp
   })
   ```

2. **Update Wave Progress**
   ```python
   # As each wave progresses
   write_memory(f"project_{id}_wave_{n}_progress", {
       "wave_number": n,
       "status": "in_progress",
       "completion_percent": 60,
       "files_modified": [...],
       "pending_tasks": [...],
       "blockers": []
   })
   ```

3. **Maintain Todo List**
   ```python
   # Keep current task list updated
   write_memory(f"project_{id}_todo_current", {
       "tasks": [
           {"task": "Implement auth", "status": "in_progress"},
           {"task": "Add tests", "status": "pending"},
           {"task": "Deploy", "status": "pending"}
       ],
       "updated": timestamp
   })
   ```

4. **Time-Based Checkpoints** (Every 30 minutes)
   ```python
   # Automatic periodic checkpoint
   if minutes_elapsed >= 30:
       create_checkpoint("time_based")
   ```

---

### Session End: State Preservation

**Before Session Ends**:

1. **Create Final Session Checkpoint**
   ```python
   # Save complete session state
   write_memory(f"session_{id}_final_checkpoint", {
       "session_id": session_id,
       "end_time": timestamp,
       "project_id": project_id,
       "active_phase": current_phase,
       "current_wave": current_wave,
       "completed_today": [...],
       "pending_tomorrow": [...],
       "important_notes": [...]
   })
   ```

2. **Update Latest Checkpoint Pointer**
   ```python
   # Point to most recent checkpoint
   write_memory("latest_checkpoint", f"session_{id}_final_checkpoint")
   ```

3. **Confirm Save**
   ```
   ✅ Session Saved

   📦 Checkpoint: session_[id]_final_checkpoint
   🔄 Progress Preserved
   ▶️ Resume anytime with: /sh:restore
   ```

---

## Command Integration

### /sh:checkpoint Command

**Manual Checkpoint Creation**:

```markdown
# User types: /sh:checkpoint [optional_name]

# STEP 1: Gather Current State
current_state = {
    "timestamp": now(),
    "project_id": current_project,
    "active_phase": current_phase,
    "current_wave": current_wave,
    "todo_list": current_todos,
    "in_progress": current_files,
    "decisions": recent_decisions,
    "notes": user_notes
}

# STEP 2: List All Serena Keys
all_keys = list_memories()

# STEP 3: Create Checkpoint
checkpoint_name = f"manual_checkpoint_{name}_{timestamp}"
write_memory(checkpoint_name, {
    "checkpoint_type": "manual",
    "state": current_state,
    "serena_keys": all_keys,
    "user_requested": True,
    "name": name if name else "unnamed"
})

# STEP 4: Update Pointer
write_memory("latest_checkpoint", checkpoint_name)

# STEP 5: Confirm
print(f"✅ Checkpoint Created: {checkpoint_name}")
print(f"📦 Preserved {len(all_keys)} memories")
print(f"🔄 Restore with: /sh:restore {name}")
```

**When to Use /sh:checkpoint**:
- Before risky operations (major refactors, experiments)
- End of work day (daily checkpoint)
- Before switching projects (context boundary)
- After completing major milestones (celebration point)
- Before taking long breaks (vacation, weekend)

---

### /sh:restore Command

**Context Restoration**:

```markdown
# User types: /sh:restore [optional_checkpoint_name]

# STEP 1: Find Checkpoint
if checkpoint_name_provided:
    checkpoint = read_memory(checkpoint_name)
else:
    # Use latest checkpoint
    latest = read_memory("latest_checkpoint")
    checkpoint = read_memory(latest)

# STEP 2: Load Checkpoint Data
checkpoint_data = checkpoint
serena_keys = checkpoint_data["serena_keys"]

# STEP 3: Restore All Keys
restored = {}
for key in serena_keys:
    try:
        restored[key] = read_memory(key)
    except:
        log_warning(f"Missing: {key}")

# STEP 4: Rebuild Context
project_id = checkpoint_data["state"]["project_id"]
active_phase = checkpoint_data["state"]["active_phase"]
current_wave = checkpoint_data["state"]["current_wave"]
todo_list = checkpoint_data["state"]["todo_list"]

# STEP 5: Report Restoration
print("✅ Context Restored Successfully")
print(f"📦 Checkpoint: {checkpoint_name}")
print(f"🔄 Phase: {active_phase}, Wave: {current_wave}")
print(f"📚 Restored {len(restored)} memories")
print(f"📋 Active Tasks: {len(todo_list)}")
print("\n▶️ Ready to continue where you left off")
```

**When to Use /sh:restore**:
- After auto-compact event (context lost)
- Starting new session (resuming work)
- After context confusion (need refresh)
- Switching back to project (from other work)
- Error recovery (rollback to known good state)

---

### /sh:status Command

**View Current Memory State**:

```markdown
# User types: /sh:status

# STEP 1: List All Memories
all_keys = list_memories()

# STEP 2: Categorize Memories
project_memories = [k for k in all_keys if "project_" in k]
wave_memories = [k for k in all_keys if "wave_" in k]
checkpoint_memories = [k for k in all_keys if "checkpoint" in k]
session_memories = [k for k in all_keys if "session_" in k]

# STEP 3: Get Latest Checkpoint
latest_checkpoint = read_memory("latest_checkpoint")
checkpoint_data = read_memory(latest_checkpoint) if latest_checkpoint else None

# STEP 4: Display Status
print("📊 Project Memory Status")
print(f"\n📦 Total Memories: {len(all_keys)}")
print(f"🏗️ Project Memories: {len(project_memories)}")
print(f"🌊 Wave Memories: {len(wave_memories)}")
print(f"💾 Checkpoints: {len(checkpoint_memories)}")
print(f"📝 Session Memories: {len(session_memories)}")

if checkpoint_data:
    print(f"\n✅ Latest Checkpoint: {latest_checkpoint}")
    print(f"🕐 Saved: {checkpoint_data['timestamp']}")
    print(f"🔄 Phase: {checkpoint_data['state']['active_phase']}")
    print(f"🎯 Wave: {checkpoint_data['state']['current_wave']}")
else:
    print("\n⚠️ No checkpoint found - consider creating one")
```

---

## Memory Naming Conventions

### Structured Naming Patterns

**Project-Level Memories**:
```
project_{project_id}_spec_analysis
project_{project_id}_phase_plan
project_{project_id}_decisions
project_{project_id}_mcp_config
project_{project_id}_testing_strategy
```

**Wave-Level Memories**:
```
project_{project_id}_wave_{n}_plan
project_{project_id}_wave_{n}_complete
project_{project_id}_wave_{n}_results_{component}
project_{project_id}_wave_{n}_agents_{agent_list}
```

**Phase-Level Memories**:
```
project_{project_id}_phase_{name}_start
project_{project_id}_phase_{name}_complete
project_{project_id}_phase_{name}_validation
project_{project_id}_phase_{name}_gates
```

**Decision Memories**:
```
decision_{topic}_{timestamp}
decision_{component}_{choice}_{timestamp}
decision_architecture_{decision_name}_{timestamp}
```

**Checkpoint Memories**:
```
precompact_checkpoint_{timestamp}
manual_checkpoint_{name}_{timestamp}
phase_checkpoint_{phase_name}_{timestamp}
wave_checkpoint_{wave_number}_{timestamp}
session_checkpoint_{session_id}
```

### Naming Best Practices

**Good Names** (Clear, Discoverable, Sortable):
```
✅ project_taskapp_spec_analysis_20250930
✅ wave_3_backend_api_results_20250930
✅ decision_auth_jwt_tokens_20250930T143000
✅ precompact_checkpoint_20250930T150000Z
✅ phase_implementation_complete_20250930
```

**Bad Names** (Vague, Unsortable, Non-descriptive):
```
❌ temp
❌ data
❌ backup_final_v2
❌ stuff_20250930
❌ important_thing
```

**Timestamp Format**: Always use ISO 8601 for chronological sorting
```
YYYYMMDD          # Date only: 20250930
YYYYMMDDTHHMMSS   # Full datetime: 20250930T143000
ISO8601           # Full ISO: 2025-09-30T14:30:00Z
```

---

## Context Preservation Strategy

### What to Save

**Always Save (Critical Context)**:
1. **Specification Analysis**: Complete 8-dimensional complexity analysis
2. **Phase Plan**: Full 5-phase execution plan with validation gates
3. **Architectural Decisions**: Every design choice with rationale
4. **Wave Results**: Complete results from each wave execution
5. **Current Progress**: Active work, pending tasks, blockers

**Usually Save (Important Context)**:
1. **MCP Configuration**: Which MCP servers are being used
2. **Testing Strategy**: Functional testing approach per platform
3. **File Modifications**: List of files created/modified
4. **Integration Points**: How components connect
5. **Quality Metrics**: Test pass rates, coverage, performance

**Sometimes Save (Nice-to-Have)**:
1. **Experiment Results**: Alternative approaches tried
2. **Performance Data**: Build times, test durations
3. **Team Notes**: Collaboration context
4. **External References**: Links to documentation
5. **Lessons Learned**: What worked, what didn't

**Never Save (Ephemeral Data)**:
1. Temporary file paths
2. Debug output
3. Random notes
4. Duplicate information
5. Obsolete data

---

### When to Save

**Automatic Save Triggers**:
```yaml
precompact_auto:
  trigger: "PreCompact hook fires"
  frequency: "Every 2-3 hours"
  content: "Complete session state"
  critical: true

wave_completion:
  trigger: "Wave successfully completes"
  frequency: "Per wave (3-8 times/project)"
  content: "Wave results and handoff"
  critical: true

phase_transition:
  trigger: "Moving to next phase"
  frequency: "4-5 times per project"
  content: "Phase completion + next phase prep"
  critical: true

time_based:
  trigger: "Every 30 minutes active work"
  frequency: "Automatic during session"
  content: "Incremental progress snapshot"
  critical: false

decision_made:
  trigger: "Architectural decision finalized"
  frequency: "As needed"
  content: "Decision with rationale"
  critical: true
```

**Manual Save Triggers**:
```yaml
user_checkpoint:
  command: "/sh:checkpoint [name]"
  frequency: "On user request"
  use_cases: ["Before risky operation", "End of day", "Before break"]

project_milestone:
  trigger: "Major milestone reached"
  frequency: "As needed"
  examples: ["MVP complete", "Tests passing", "Deployed"]

error_recovery:
  trigger: "Before attempting fix"
  frequency: "Before risky recovery"
  purpose: "Rollback point"
```

---

## Cross-Session Continuity

### Resuming Work After Break

**Morning Resume Pattern**:
```python
# User returns next morning

# STEP 1: Detect Returning User
# Check for recent project activity

# STEP 2: Load Latest Checkpoint
latest = read_memory("latest_checkpoint")
checkpoint = read_memory(latest)

# STEP 3: Rebuild Yesterday's Context
yesterday_work = checkpoint["state"]["completed_today"]
pending_work = checkpoint["state"]["pending_tomorrow"]
decisions_made = checkpoint["state"]["decisions"]

# STEP 4: Summarize for User
print("🌅 Good morning! Here's where we left off:")
print(f"\n✅ Yesterday's Progress:")
for item in yesterday_work:
    print(f"  - {item}")

print(f"\n📋 Today's Focus:")
for item in pending_work[:3]:  # Top 3 priorities
    print(f"  - {item}")

print(f"\n💡 Recent Decisions:")
for decision in decisions_made[-2:]:  # Last 2 decisions
    print(f"  - {decision['decision']}")

print("\n▶️ Ready to continue. What would you like to tackle first?")
```

---

### Multi-Project Management

**Project Switching Pattern**:
```python
# User switches from Project A to Project B

# STEP 1: Save Project A Context
write_memory("current_project_checkpoint", {
    "project_id": "project_a",
    "state": current_project_a_state,
    "timestamp": now()
})

# STEP 2: Load Project B Context
project_b_checkpoint = read_memory("project_b_latest_checkpoint")
project_b_state = read_memory(project_b_checkpoint)

# STEP 3: Restore Project B Context
restore_full_context(project_b_state)

# STEP 4: Update Current Project Pointer
write_memory("active_project", "project_b")

# STEP 5: Confirm Switch
print("🔄 Switched to Project B")
print(f"📦 Context loaded from: {project_b_checkpoint}")
print(f"🔄 Phase: {project_b_state['active_phase']}")
```

---

## Memory Validation

### Validation Checks

**Checkpoint Integrity**:
```python
def validate_checkpoint(checkpoint_data):
    """
    Validate checkpoint contains required data
    """
    required_fields = [
        "timestamp",
        "project_id",
        "serena_keys",
        "state"
    ]

    for field in required_fields:
        if field not in checkpoint_data:
            return False, f"Missing required field: {field}"

    # Validate serena_keys list is not empty
    if len(checkpoint_data["serena_keys"]) == 0:
        return False, "No Serena keys preserved"

    # Validate timestamp format
    try:
        parse_timestamp(checkpoint_data["timestamp"])
    except:
        return False, "Invalid timestamp format"

    return True, "Checkpoint valid"
```

**Memory Key Validation**:
```python
def validate_memory_key(key):
    """
    Validate memory key follows naming conventions
    """
    # Check for valid prefix
    valid_prefixes = [
        "project_", "wave_", "phase_", "session_",
        "decision_", "checkpoint", "precompact_"
    ]

    if not any(key.startswith(prefix) for prefix in valid_prefixes):
        return False, "Invalid key prefix"

    # Check for timestamp if checkpoint
    if "checkpoint" in key:
        if not has_timestamp(key):
            return False, "Checkpoint missing timestamp"

    return True, "Key valid"
```

**Restoration Validation**:
```python
def validate_restoration(restored_data):
    """
    Validate restored context is complete
    """
    checks = {
        "has_spec": "spec_analysis" in restored_data,
        "has_plan": "phase_plan" in restored_data,
        "has_wave_context": any("wave_" in k for k in restored_data),
        "has_recent_checkpoint": check_recent_checkpoint(restored_data)
    }

    missing = [k for k, v in checks.items() if not v]

    if missing:
        return False, f"Incomplete restoration: {missing}"

    return True, "Restoration complete"
```

---

## Memory Cleanup

### Cleanup Policies

**Retention Policies**:
```yaml
indefinite_retention:
  patterns:
    - "project_{id}_spec_analysis"
    - "project_{id}_phase_plan"
    - "project_{id}_decisions"
    - "project_{id}_final_results"
  rationale: "Essential project artifacts"

thirty_day_retention:
  patterns:
    - "wave_{n}_complete"
    - "phase_{name}_checkpoint"
    - "precompact_checkpoint_*"
  rationale: "Recent history for recovery"

seven_day_retention:
  patterns:
    - "wave_{n}_plan"
    - "session_*"
    - "temp_*"
  rationale: "Short-term working memory"

one_day_retention:
  patterns:
    - "scratch_*"
    - "tmp_*"
    - "debug_*"
  rationale: "Truly temporary data"
```

**Cleanup Execution**:
```python
def cleanup_old_memories(retention_days):
    """
    Remove memories older than retention period
    """
    all_keys = list_memories()
    now = datetime.now()

    for key in all_keys:
        # Extract timestamp from key
        timestamp = extract_timestamp(key)
        if not timestamp:
            continue

        # Calculate age
        age_days = (now - timestamp).days

        # Determine retention period for this key type
        retention = get_retention_period(key)

        # Delete if too old
        if age_days > retention:
            delete_memory(key)
            log_cleanup(f"Deleted old memory: {key}")
```

---

## Integration with Sub-Agents

### Mandatory Context Loading

**Every sub-agent MUST start with**:
```python
# MANDATORY: Load context before any work

# Step 1: Load project foundation
spec = read_memory("project_{id}_spec_analysis")
phase_plan = read_memory("project_{id}_phase_plan")
decisions = read_memory("project_{id}_decisions")

# Step 2: Load wave context
current_wave = read_memory("active_wave_number")
if current_wave > 1:
    previous_wave = read_memory(f"wave_{current_wave-1}_complete")

# Step 3: Load agent-specific context
my_context = read_memory(f"agent_{my_name}_context")

# Step 4: Validate context loaded
assert spec is not None, "No spec analysis found"
assert phase_plan is not None, "No phase plan found"

# Step 5: Proceed with full understanding
execute_with_complete_context(spec, phase_plan, decisions, previous_wave)
```

---

## Troubleshooting

### Common Issues

**Issue: Checkpoint Not Created**
```
Symptoms:
- No checkpoint after auto-compact
- Context lost
- User frustrated

Solution:
1. Verify PreCompact hook installed: ls ~/.claude/hooks/precompact.py
2. Test hook manually: python3 ~/.claude/hooks/precompact.py
3. Create manual checkpoint: /sh:checkpoint emergency
4. Check Serena MCP connection: list_memories()
```

**Issue: Cannot Restore Context**
```
Symptoms:
- /sh:restore fails
- Memories not found
- Incomplete restoration

Solution:
1. List all checkpoints: list_memories() | grep checkpoint
2. Try latest: read_memory("latest_checkpoint")
3. Try manual restore: read_memory("precompact_checkpoint_*")
4. Partial restoration: Load critical memories only
5. If all fail: Start fresh, inform user of data loss
```

**Issue: Too Many Memories**
```
Symptoms:
- list_memories() slow
- Storage warnings
- Memory operations laggy

Solution:
1. Run cleanup: /sh:cleanup-context
2. Delete old sessions: cleanup_context("session")
3. Archive old checkpoints: keep last 5 only
4. Consolidate wave results: merge related memories
```

---

## Best Practices

### Memory Management Principles

1. **Save Early, Save Often**
   - Don't wait for auto-compact
   - Create checkpoints at logical boundaries
   - Document decisions as they happen

2. **Use Descriptive Keys**
   - Include context in key names
   - Add timestamps for sorting
   - Follow naming conventions

3. **Validate Before Saving**
   - Check data completeness
   - Verify JSON structure
   - Confirm key uniqueness

4. **Restore Intelligently**
   - Load in priority order (critical first)
   - Handle missing memories gracefully
   - Validate restoration success

5. **Clean Up Regularly**
   - Delete obsolete memories
   - Archive completed projects
   - Maintain lean memory store

---

## Summary

**Project Memory Enables**:
- ✅ Zero context loss across auto-compact
- ✅ Seamless session resumption
- ✅ Multi-project management
- ✅ Complete audit trail
- ✅ Error recovery capability

**Key Components**:
- 5-level hierarchical memory structure
- Session lifecycle (start, active, end)
- Command integration (/sh:checkpoint, /sh:restore, /sh:status)
- Structured naming conventions
- Context preservation strategy
- Validation and cleanup systems

**Integration Points**:
- Wave orchestration (cross-wave context)
- Phase planning (phase transitions)
- Sub-agents (mandatory context loading)
- PreCompact hook (automatic checkpoint)

**Result**: Shannon achieves complete project continuity through systematic memory management integrated with Serena MCP.