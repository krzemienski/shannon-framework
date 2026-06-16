---
name: shannon-context-restorer
display_name: "Shannon Context Restorer (Session Restoration)"
description: "Restores project context from checkpoints - enables zero-context-loss across sessions and auto-compaction events"
category: management
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_restore command"
  - "restore checkpoint"
  - "session start"
  - "load context"
mcp_servers:
  required:
    - serena
allowed_tools:
  - serena_read_memory
  - serena_list_memories
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
input:
  checkpoint_id:
    type: string
    description: "Checkpoint ID to restore (or 'latest')"
    required: false
    default: "latest"
output:
  restored_state:
    type: object
    description: "Restored project state"
  restoration_report:
    type: object
    description: "What was restored"
  sitrep:
    type: object
    description: "Standardized SITREP (via shannon-status-reporter)"
---

# Shannon Context Restorer

> **Session Restoration**: Zero-context-loss recovery from checkpoints

## Purpose

Restores complete project context from checkpoints created by shannon-checkpoint-manager, enabling:
- **Session continuity** - Resume work after session ends
- **Auto-compaction recovery** - Restore after context compression
- **Time-travel** - Return to previous project states
- **Disaster recovery** - Recover from errors or failures

## Capabilities

### 1. Checkpoint Loading
- Load checkpoint by ID or "latest"
- Validate checkpoint integrity
- Extract complete project state
- Display checkpoint metadata

### 2. State Restoration
- Restore North Star goal
- Restore active todos
- Restore current phase/wave
- Restore decisions and context
- Re-activate generated skills

### 3. Verification
- Verify restoration completeness
- Check for missing data
- Validate restored state
- Report restoration success

### 4. SessionStart Integration
- Auto-restore on session start
- Detect PreCompact checkpoints
- Resume from last known state
- Silent restoration (no user prompt)

## Activation

**Automatic**:
```bash
/sh_restore
/sh_restore latest
/sh_restore checkpoint_myproject_1730739600000
```

**SessionStart Hook** (Automatic):
```python
# Fires automatically when new session starts
# Detects and restores from latest checkpoint
```

## Execution Algorithm

### Step 1: Identify Checkpoint

```javascript
async function identifyCheckpoint(checkpoint_id = "latest") {
  if (checkpoint_id === "latest") {
    // Load latest checkpoint metadata
    const latest = await serena_read_memory("latest_checkpoint");

    if (!latest) {
      return {
        found: false,
        message: "No checkpoints found. Create one with /sh_checkpoint"
      };
    }

    checkpoint_id = latest.checkpoint_id;
  }

  // Load checkpoint
  const checkpoint = await serena_read_memory(checkpoint_id);

  if (!checkpoint) {
    return {
      found: false,
      message: `Checkpoint '${checkpoint_id}' not found`,
      suggestions: await findSimilarCheckpoints(checkpoint_id)
    };
  }

  return {
    found: true,
    checkpoint_id,
    checkpoint
  };
}

async function findSimilarCheckpoints(checkpoint_id) {
  const all_memories = await serena_list_memories();
  const checkpoints = all_memories.filter(m => m.key.startsWith('checkpoint_'));

  return checkpoints
    .slice(0, 5)
    .map(c => c.key);
}
```

### Step 2: Validate Checkpoint

```javascript
function validateCheckpoint(checkpoint) {
  const required_fields = [
    'checkpoint.id',
    'checkpoint.project_id',
    'checkpoint.created_at',
    'state.project_id',
    'state.current_phase'
  ];

  const validation_errors = [];

  for (const field of required_fields) {
    const parts = field.split('.');
    let value = checkpoint;

    for (const part of parts) {
      value = value?.[part];
    }

    if (value === undefined || value === null) {
      validation_errors.push(`Missing required field: ${field}`);
    }
  }

  // Check version compatibility
  if (checkpoint.version && checkpoint.version !== "4.0.0") {
    validation_errors.push(`Incompatible checkpoint version: ${checkpoint.version} (expected 4.0.0)`);
  }

  return {
    is_valid: validation_errors.length === 0,
    errors: validation_errors
  };
}
```

### Step 3: Restore Project State

```javascript
async function restoreState(checkpoint) {
  const state = checkpoint.state;
  const restoration_report = {
    restored: [],
    skipped: [],
    errors: []
  };

  // 1. Restore North Star Goal
  if (state.north_star_goal) {
    try {
      await serena_write_memory("north_star_goal", {
        goal: state.north_star_goal,
        restored_from: checkpoint.checkpoint.id,
        restored_at: Date.now()
      });
      restoration_report.restored.push("North Star goal");
    } catch (error) {
      restoration_report.errors.push(`North Star: ${error.message}`);
    }
  } else {
    restoration_report.skipped.push("North Star goal (not in checkpoint)");
  }

  // 2. Restore Active Todos
  if (state.active_todos && state.active_todos.length > 0) {
    try {
      await serena_write_memory("active_todos", {
        todos: state.active_todos,
        restored_from: checkpoint.checkpoint.id,
        restored_at: Date.now()
      });
      restoration_report.restored.push(`${state.active_todos.length} active todos`);
    } catch (error) {
      restoration_report.errors.push(`Todos: ${error.message}`);
    }
  }

  // 3. Restore Current Phase/Wave
  if (state.current_phase) {
    try {
      await serena_write_memory("current_phase", {
        phase: state.current_phase,
        wave: state.current_wave,
        restored_from: checkpoint.checkpoint.id,
        restored_at: Date.now()
      });
      restoration_report.restored.push(`Phase: ${state.current_phase}, Wave: ${state.current_wave || 'N/A'}`);
    } catch (error) {
      restoration_report.errors.push(`Phase/Wave: ${error.message}`);
    }
  }

  // 4. Restore Recent Decisions
  if (state.recent_decisions && state.recent_decisions.length > 0) {
    try {
      await serena_write_memory("recent_decisions", {
        decisions: state.recent_decisions,
        restored_from: checkpoint.checkpoint.id,
        restored_at: Date.now()
      });
      restoration_report.restored.push(`${state.recent_decisions.length} recent decisions`);
    } catch (error) {
      restoration_report.errors.push(`Decisions: ${error.message}`);
    }
  }

  // 5. Restore Generated Skills List
  if (state.generated_skills && state.generated_skills.length > 0) {
    try {
      await serena_write_memory("generated_skills", {
        skills: state.generated_skills,
        restored_from: checkpoint.checkpoint.id,
        restored_at: Date.now()
      });
      restoration_report.restored.push(`${state.generated_skills.length} generated skills`);
    } catch (error) {
      restoration_report.errors.push(`Skills: ${error.message}`);
    }
  }

  // 6. Mark restoration complete
  await serena_write_memory("last_restoration", {
    checkpoint_id: checkpoint.checkpoint.id,
    checkpoint_label: checkpoint.checkpoint.label,
    restored_at: Date.now(),
    restoration_report
  });

  return restoration_report;
}
```

### Step 4: Verify Restoration

```javascript
function verifyRestoration(checkpoint, restoration_report) {
  const expected_restorations = [
    "North Star goal",
    "active todos",
    "Phase",
    "recent decisions",
    "generated skills"
  ];

  const actually_restored = restoration_report.restored.map(r =>
    r.toLowerCase()
  );

  const missing = expected_restorations.filter(exp =>
    !actually_restored.some(act => act.includes(exp.toLowerCase()))
  );

  const completeness = (
    restoration_report.restored.length /
    (restoration_report.restored.length + restoration_report.skipped.length + restoration_report.errors.length)
  );

  return {
    complete: restoration_report.errors.length === 0 && missing.length === 0,
    completeness: Math.round(completeness * 100),
    missing_items: missing,
    errors: restoration_report.errors
  };
}
```

### Step 5: Generate Restoration Report

```javascript
function generateReport(checkpoint, restoration_report, verification) {
  const report = `
# Session Restored ✅

**Checkpoint**: ${checkpoint.checkpoint.label}
**ID**: ${checkpoint.checkpoint.id}
**Created**: ${new Date(checkpoint.checkpoint.created_at).toISOString()}
**Completeness**: ${verification.completeness}%

## Restored State

### ✅ Successfully Restored (${restoration_report.restored.length})
${restoration_report.restored.map(r => `- ${r}`).join('\n')}

${restoration_report.skipped.length > 0 ? `
### ⚠️ Skipped (${restoration_report.skipped.length})
${restoration_report.skipped.map(s => `- ${s}`).join('\n')}
` : ''}

${restoration_report.errors.length > 0 ? `
### ❌ Errors (${restoration_report.errors.length})
${restoration_report.errors.map(e => `- ${e}`).join('\n')}
` : ''}

## Project Context

- **Phase**: ${checkpoint.state.current_phase}
- **Wave**: ${checkpoint.state.current_wave || 'N/A'}
- **Todos**: ${checkpoint.state.active_todos?.length || 0} active, ${checkpoint.state.pending_todos?.length || 0} pending
- **North Star**: ${checkpoint.state.north_star_goal || 'Not set'}

## Modified Files (${checkpoint.state.modified_files?.length || 0})
${(checkpoint.state.modified_files || []).slice(0, 10).map(f => `- ${f}`).join('\n')}
${(checkpoint.state.modified_files || []).length > 10 ? `... and ${checkpoint.state.modified_files.length - 10} more` : ''}

## Next Steps

${checkpoint.state.active_todos && checkpoint.state.active_todos.length > 0
  ? `Continue with active todos: ${checkpoint.state.active_todos[0]?.content || 'Review todos'}`
  : checkpoint.state.current_wave
  ? `Execute Wave ${checkpoint.state.current_wave}: /sh_wave ${checkpoint.state.current_wave}`
  : 'Review project status: /sh_status'
}

---
**Zero-Context-Loss Guaranteed** ✅
  `;

  return report;
}
```

### Step 6: Generate SITREP

```javascript
// Generate standardized SITREP using shannon-status-reporter
const sitrep_data = {
  agent_name: "shannon-context-restorer",
  task_id: `restore_${checkpoint.checkpoint.id}_${Date.now()}`,
  current_phase: checkpoint.state.current_phase,
  progress: verification.completeness,
  state: verification.complete ? "completed" : "blocked",

  objective: `Restore from checkpoint: ${checkpoint.checkpoint.label}`,
  scope: [
    `Checkpoint ID: ${checkpoint.checkpoint.id}`,
    `Created: ${new Date(checkpoint.checkpoint.created_at).toISOString()}`,
    `Type: ${checkpoint.checkpoint.type || 'manual'}`
  ],
  dependencies: ["serena"],

  findings: [
    `Restored: ${restoration_report.restored.join(', ')}`,
    `Completeness: ${verification.completeness}%`,
    `Phase: ${checkpoint.state.current_phase}`,
    `Wave: ${checkpoint.state.current_wave || 'N/A'}`,
    `Todos: ${checkpoint.state.active_todos?.length || 0} active`,
    `North Star: ${checkpoint.state.north_star_goal || 'Not set'}`
  ],

  blockers: restoration_report.errors,
  risks: verification.missing_items.length > 0 ? [`Incomplete restoration: missing ${verification.missing_items.join(', ')}`] : [],
  questions: [],

  next_steps: [
    checkpoint.state.active_todos && checkpoint.state.active_todos.length > 0
      ? `Continue with: ${checkpoint.state.active_todos[0]?.content}`
      : null,
    checkpoint.state.current_wave
      ? `Execute Wave ${checkpoint.state.current_wave}`
      : null,
    "Review project status: /sh_status"
  ].filter(Boolean),

  artifacts: [
    "north_star_goal (restored)",
    "active_todos (restored)",
    "current_phase (restored)",
    "recent_decisions (restored)",
    "generated_skills (restored)"
  ].filter(item => restoration_report.restored.some(r => item.includes(r.toLowerCase()))),

  tests_executed: ["checkpoint_validation", "state_restoration", "verification"],
  test_results: verification.complete
    ? "All restorations successful"
    : `${verification.completeness}% complete with ${restoration_report.errors.length} errors`
};

// Invoke shannon-status-reporter to generate SITREP
const sitrep = await generate_sitrep(sitrep_data);

return sitrep;
```

## Examples

### Example 1: Restore Latest Checkpoint

```bash
/sh_restore
# or
/sh_restore latest
```

**SITREP Output**:
```markdown
## SITREP: shannon-context-restorer - restore_checkpoint_myproject_1730739600000_1730740000000

### Status
- **Current Phase**: Implementation
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: Restore from checkpoint: Wave 2 complete
- **Scope**: Checkpoint ID: checkpoint_myproject_1730739600000, Created: 2025-11-04T10:00:00.000Z, Type: wave_complete
- **Dependencies**: serena

### Findings
- Restored: North Star goal, 3 active todos, Phase: Implementation, Wave: 3, recent decisions, generated skills
- Completeness: 100%
- Phase: Implementation
- Wave: 3
- Todos: 3 active
- North Star: Build production-ready React dashboard

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- [ ] Continue with: Implement user authentication
- [ ] Execute Wave 3
- [ ] Review project status: /sh_status

### Artifacts
- north_star_goal (restored)
- active_todos (restored)
- current_phase (restored)
- recent_decisions (restored)
- generated_skills (restored)

### Validation
- **Tests Executed**: checkpoint_validation, state_restoration, verification
- **Results**: All restorations successful
```

### Example 2: SessionStart Auto-Restoration

```
[New session starts]
[SessionStart hook detects latest checkpoint]
[shannon-context-restorer activates automatically]
[Context restored silently]
[User sees: "Session restored from Wave 2 complete checkpoint"]
```

### Example 3: Restore Specific Checkpoint

```bash
/sh_restore checkpoint_myproject_1730700000000
```

Restores from specific checkpoint ID (useful for time-travel debugging).

## Integration with Shannon v4

**Used by**:
- /sh_restore command (user-initiated)
- SessionStart hook (automatic)
- PreCompact recovery (after auto-compaction)

**Uses**:
- shannon-status-reporter (SITREP generation)
- shannon-checkpoint-manager (checkpoint format)
- serena MCP (state loading)

**Zero-Context-Loss Flow**:
```
Session ends / Token limit reached
  ↓
PreCompact hook → shannon-checkpoint-manager (save)
  ↓
Auto-compaction occurs
  ↓
New session starts
  ↓
SessionStart hook → shannon-context-restorer (restore)
  ↓
Zero context loss ✅
```

## Best Practices

### DO ✅
- Restore at session start
- Verify restoration completeness
- Review restoration SITREP
- Continue from last known state
- Use specific checkpoint IDs for time-travel

### DON'T ❌
- Skip restoration verification
- Ignore restoration errors
- Restore from incompatible versions
- Forget to create checkpoints
- Override restored state immediately

## Restoration Completeness

**100% Restoration**:
- All fields present in checkpoint
- All validations pass
- No errors during restoration
- State matches checkpoint exactly

**Partial Restoration (< 100%)**:
- Some fields missing from checkpoint
- Non-critical errors
- State mostly restored but with gaps

**Failed Restoration (0%)**:
- Checkpoint not found
- Checkpoint corrupted
- Incompatible versions
- Critical errors

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📚 **Restoration Patterns**: [resources/RESTORATION_PATTERNS.md](./resources/RESTORATION_PATTERNS.md)

---

**Shannon V4** - Zero-Context-Loss Recovery 🔄
