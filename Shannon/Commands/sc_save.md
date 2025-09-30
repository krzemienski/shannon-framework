---
command: /sc:save
aliases: [save]
category: session-management
base_command: SuperClaude /save
shannon_mapping: /sh:checkpoint
complexity: standard
mcp-servers: [serena]
personas: []
sub-agents: [CONTEXT_GUARDIAN]
priority: critical
triggers: [save, checkpoint, backup, preserve, end-session]
---

# /sc:save - Enhanced Session Checkpoint

**Purpose**: SuperClaude-compatible session checkpoint command that maps to Shannon's `/sh:checkpoint` for comprehensive state preservation.

**Shannon V3 Enhancement**: Maintains SuperClaude `/save` compatibility while leveraging Shannon's advanced checkpoint system powered by CONTEXT_GUARDIAN agent.

---

## Purpose Statement

The `/sc:save` command creates comprehensive session checkpoints by preserving all project context to Serena MCP. This enhanced version of SuperClaude's `/save` maps directly to Shannon's `/sh:checkpoint` system, enabling zero context loss across session boundaries, auto-compact events, and project interruptions.

**Core Function**: Save session state → Preserve all memories → Create restoration point → Enable seamless recovery

**Base SuperClaude Command**: `/save` (session lifecycle management)
**Shannon Mapping**: `/sh:checkpoint` (enhanced checkpoint system)
**Key Enhancement**: CONTEXT_GUARDIAN-powered comprehensive state preservation

---

## Shannon V3 Enhancements

### Mapping to /sh:checkpoint

The `/sc:save` command serves as SuperClaude-compatible alias for Shannon's `/sh:checkpoint`:

```yaml
command_relationship:
  superclaude_command: /sc:save
  shannon_native: /sh:checkpoint
  compatibility: full
  behavior: identical

enhancement_layer:
  base: SuperClaude session save
  added: Shannon checkpoint system
  agent: CONTEXT_GUARDIAN
  storage: Serena MCP
  recovery: /sh:restore
```

### Key Enhancements Over Base /save

1. **Complete Serena State Preservation**: All memory keys catalogued and preserved
2. **Wave Context Capture**: Current wave state, phase, and progress
3. **CONTEXT_GUARDIAN Integration**: Specialized agent ensures no data loss
4. **Restoration Instructions**: Automatic generation of recovery procedures
5. **Decision History**: Key architectural and implementation decisions recorded
6. **Multi-Project Support**: Project-specific checkpoint isolation

---

## Usage Patterns

### Basic Usage
```bash
# Auto-generated checkpoint name
/sc:save

# Named checkpoint
/sc:save [checkpoint-name]

# Before ending session
/sc:save end_of_day

# Before risky operation
/sc:save before_experiment
```

### Advanced Usage
```bash
# Auto-name with timestamp
/sc:save --auto-name

# Include code snapshots
/sc:save --with-code

# Wave completion checkpoint
/sc:save wave_3_complete

# Phase transition checkpoint
/sc:save phase_2_to_3
```

### Integration Patterns
```bash
# Save before wave execution
/sc:save && /sh:execute-wave 3

# Save after implementation
/sc:implement auth && /sc:save impl_auth

# Save and end session
/sc:save end_session && exit
```

---

## Activation Triggers

### Automatic Triggers
- Context usage approaching 75% (yellow zone)
- Before wave execution starts
- After major phase completion
- Before risky operations (experimental code)

### Manual Triggers
- Explicit `/sc:save` command
- End of work session
- Before leaving project
- Project milestone completion

### Integration Triggers
- After `/sc:implement` completion
- Post-wave validation success
- Before `/sc:git` major operations
- After `/sc:build` success

---

## Execution Flow

### Step 1: CONTEXT_GUARDIAN Activation

**Sub-Agent Initialization**:
```python
# Activate specialized checkpoint agent
activate_agent("CONTEXT_GUARDIAN")

# Agent receives command context
context_guardian_input = {
    "command": "/sc:save",
    "checkpoint_name": user_provided_or_auto_generated,
    "reason": checkpoint_trigger_reason,
    "session_context": current_session_state
}
```

### Step 2: Current State Collection

**CONTEXT_GUARDIAN Actions**:
```python
# Gather comprehensive session state
current_state = {
    "wave_context": {
        "current_wave": active_wave_number_or_null,
        "wave_status": wave_execution_state,
        "phase_number": current_phase,
        "phase_name": phase_identifier
    },
    "work_progress": {
        "active_todos": TodoWrite_current_state,
        "completed_count": finished_tasks,
        "pending_count": remaining_tasks,
        "completion_percent": progress_estimate
    },
    "last_activity": recent_completed_operation,
    "next_activity": planned_next_step
}
```

### Step 3: Serena Memory Cataloguing

**CONTEXT_GUARDIAN Actions**:
```python
# List all Serena memory keys
all_memories = list_memories()

# Categorize memories
memory_catalog = {
    "specification_keys": filter(spec_related),
    "wave_keys": filter(wave_related),
    "implementation_keys": filter(code_related),
    "decision_keys": filter(decision_related),
    "checkpoint_keys": filter(checkpoint_related)
}

# Example result:
[
  "spec_analysis_001",
  "requirements_final",
  "user_stories",
  "architecture_complete",
  "wave_1_complete",
  "wave_2_complete",
  "implementation_auth",
  "decisions_database"
]
```

### Step 4: Checkpoint Creation

**CONTEXT_GUARDIAN Actions**:
```python
# Create comprehensive checkpoint
write_memory("shannon_checkpoint_[name]", {
    "checkpoint_metadata": {
        "name": checkpoint_name,
        "created_at": ISO_timestamp,
        "created_by": "sc:save",
        "checkpoint_type": "manual",
        "superclaude_compatible": true
    },

    "context_preservation": {
        "serena_keys": all_memories,
        "total_keys": count,
        "last_updated": most_recent_key,
        "key_categories": memory_catalog
    },

    "project_state": {
        "current_wave": wave_number,
        "current_phase": phase_details,
        "completion_percent": progress,
        "last_activity": recent_work,
        "next_activity": planned_next
    },

    "work_in_progress": {
        "active_todos": current_todos,
        "completed_todos": finished_count,
        "pending_validations": gates_waiting
    },

    "key_decisions": [
        "Architectural decisions made",
        "Technology choices",
        "Implementation strategies"
    ],

    "mcp_integration": {
        "servers_used": ["serena", "magic", "sequential"],
        "primary_storage": "serena"
    },

    "restoration_instructions": {
        "command": "/sh:restore shannon_checkpoint_[name]",
        "steps": [
            "read_memory('shannon_checkpoint_[name]')",
            "Load all keys from serena_keys list",
            "Restore project state",
            "Resume from next_activity"
        ]
    },

    "context_metadata": {
        "token_usage_percent": estimated_usage,
        "reason_for_checkpoint": trigger_reason,
        "session_duration": time_elapsed
    }
})
```

### Step 5: Verification & Confirmation

**CONTEXT_GUARDIAN Actions**:
```python
# Verify checkpoint creation
verify_checkpoint = read_memory("shannon_checkpoint_[name]")

# Confirm all keys preserved
if verify_checkpoint and all_keys_present:
    generate_confirmation_report()
else:
    retry_checkpoint_creation()
```

---

## Sub-Agent Integration: CONTEXT_GUARDIAN

`/sc:save` activates the **CONTEXT_GUARDIAN** sub-agent for comprehensive checkpoint orchestration.

### CONTEXT_GUARDIAN Responsibilities

**Primary Role**: Session checkpoint specialist ensuring complete state preservation

**Core Capabilities**:
- Comprehensive Serena memory cataloguing
- Wave and phase state capture
- Decision history preservation
- Restoration instruction generation
- Verification and validation

**Quality Standards**:
- 100% memory key preservation
- Accurate state capture
- Valid restoration instructions
- Verifiable checkpoint integrity

### Activation Pattern
```python
# User executes command
User: /sc:save before_wave_3

# Shannon activates CONTEXT_GUARDIAN
→ activate_agent(CONTEXT_GUARDIAN)
→ collect_session_state()
→ catalog_serena_memories()
→ create_checkpoint()
→ verify_checkpoint()
→ generate_report()
```

---

## Output Format

### Successful Checkpoint
```markdown
✅ SESSION CHECKPOINT CREATED

**Checkpoint Details**:
- Name: shannon_checkpoint_before_wave_3
- Created: 2025-09-30T14:30:00Z
- Type: Manual (sc:save)
- Serena Key: shannon_checkpoint_before_wave_3

**Context Preserved**:
- Serena Memory Keys: 12 keys catalogued
- Wave State: Wave 2 complete, ready for Wave 3
- Todo State: 8/12 completed
- Token Usage: 68% at checkpoint

**Memory Keys Preserved**:
1. spec_analysis_001
2. requirements_final
3. user_stories
4. architecture_complete
5. database_schema_final
6. wave_1_complete
7. wave_2_complete
8. implementation_auth
9. implementation_api
10. decisions_database
11. decisions_authentication
12. phase_plan

**Restoration**:
```bash
/sh:restore shannon_checkpoint_before_wave_3
```

**Status**: Safe to continue or end session
```

### Checkpoint with Warnings
```markdown
⚠️ CHECKPOINT CREATED WITH WARNINGS

**Checkpoint**: shannon_checkpoint_high_usage
**Created**: 2025-09-30T16:45:00Z

**Context Status**:
- Token Usage: 82% (HIGH - recommend compaction soon)
- Serena Keys: 18 keys preserved
- Wave State: Mid-execution Wave 3

**Warnings**:
⚠️ High token usage - consider /compact after current wave
⚠️ Wave in progress - checkpoint captures mid-wave state

**Safe to Continue**: Yes, checkpoint provides recovery point
```

---

## Examples

### Example 1: End of Day Checkpoint
```bash
# User finishing work for the day
User: /sc:save end_of_day_sept30

# CONTEXT_GUARDIAN creates comprehensive checkpoint
✅ SESSION CHECKPOINT CREATED

Checkpoint: shannon_checkpoint_end_of_day_sept30
Preserved: 15 Serena keys
Wave State: Wave 2 complete, Wave 3 planned
Next Session: Run /sh:restore shannon_checkpoint_end_of_day_sept30

Status: Safe to exit session
```

### Example 2: Before Risky Operation
```bash
# User about to try experimental approach
User: /sc:save before_experiment

✅ CHECKPOINT CREATED (Rollback Point)

Checkpoint: shannon_checkpoint_before_experiment
Purpose: Pre-experiment safety checkpoint
Preserved: Complete project state

If experiment fails:
/sh:restore shannon_checkpoint_before_experiment
```

### Example 3: Wave Completion Checkpoint
```bash
# After completing major wave
User: /sc:implement wave2 tasks...
[Wave 2 completes]

User: /sc:save wave_2_complete

✅ WAVE COMPLETION CHECKPOINT

Checkpoint: shannon_checkpoint_wave_2_complete
Wave 2 Status: ✅ Validated and complete
Wave 3 Ready: All prerequisites satisfied
Preserved: 18 memory keys including wave outputs

Next: Execute /sh:execute-wave 3
```

### Example 4: Auto-Name with High Context
```bash
# Context usage at 78%
User: /sc:save --auto-name

⚠️ HIGH CONTEXT USAGE DETECTED

Checkpoint: shannon_checkpoint_20250930T143000Z
Context Usage: 78% (recommend checkpoint before continuing)
Preserved: Complete state

Recommendations:
1. Checkpoint created (safe to continue)
2. Consider /compact after next major operation
3. Monitor context usage during wave execution
```

---

## Integration with Shannon Commands

### Complements
- **`/sh:restore`**: Load saves checkpoint, restore recovers it
- **`/sh:checkpoint`**: Direct mapping, identical behavior
- **`/sh:status`**: Status shows checkpoint availability
- **`/sc:load`**: Load reads checkpoints for project activation

### Workflow Integration
```bash
# Typical session pattern
/sc:load project_name          # Start: load project
[work on implementation]
/sc:save checkpoint_1           # Checkpoint: preserve progress
[continue work]
/sc:save checkpoint_2           # Checkpoint: additional save point
[complete wave]
/sc:save wave_complete          # Checkpoint: milestone
```

---

## Command Boundaries

### Will Do
- Create comprehensive Serena checkpoint
- Preserve ALL memory keys
- Capture complete wave and phase state
- Generate restoration instructions
- Verify checkpoint integrity
- Support SuperClaude compatibility

### Will NOT Do
- Modify project files or code
- Execute or restore checkpoints (that's `/sh:restore`)
- Compact context (that's `/compact`)
- Delete or modify existing checkpoints
- Create git commits (that's `/sc:git`)
- Override checkpoints without confirmation

---

## Relationship to Other Commands

```yaml
command_ecosystem:
  base_command: SuperClaude /save
  shannon_native: /sh:checkpoint

  complements:
    - /sh:restore: "Restoration from checkpoint"
    - /sh:status: "Shows checkpoint availability"
    - /sc:load: "Uses checkpoints for project activation"
    - /sh:execute-wave: "Checkpoints before wave execution"

  workflow_position:
    before: [/sh:restore, session-end]
    after: [major-completions, risky-operations]
    parallel: [ongoing-work]
```

---

## Quality Standards

### Checkpoint Integrity
- 100% memory key preservation
- Accurate state capture
- Valid restoration instructions
- Verifiable checkpoint structure

### CONTEXT_GUARDIAN Performance
- Complete state collection (<2s)
- Memory cataloguing accuracy (100%)
- Checkpoint creation reliability (99.9%)
- Verification thoroughness (all keys checked)

---

**Status**: Shannon V3 Enhanced
**Base Command**: SuperClaude /save
**Enhancement Type**: Maps to /sh:checkpoint with CONTEXT_GUARDIAN
**Critical Dependency**: Serena MCP
**Related Commands**: /sh:checkpoint (direct mapping), /sh:restore, /sh:status, /sc:load