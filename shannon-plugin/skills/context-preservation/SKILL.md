---
name: context-preservation
description: |
  PROTOCOL skill for checkpoint-based context preservation using Serena MCP.
  Automatically creates checkpoints at wave boundaries and before PreCompact.
  Enables zero-context-loss multi-session work with structured metadata collection.
  Use this skill for ALL Shannon projects - checkpoints are mandatory, not optional.

skill-type: PROTOCOL
shannon-version: ">=4.0.0"

# MCP INTEGRATION
mcp-requirements:
  required:
    - name: serena
      purpose: Persistent storage in knowledge graph for checkpoints
      fallback: ERROR - Cannot preserve context without Serena MCP
  recommended:
    - name: sequential
      purpose: Enhanced metadata analysis during checkpoint creation
      fallback: Use standard analysis (no sequential thinking)
      trigger: complexity >= 0.70

# COMPOSITION
required-sub-skills: []
optional-sub-skills:
  - goal-management
  - phase-planning

# PERMISSIONS
allowed-tools: [Serena, Read, Write, Grep, Sequential]
model: sonnet
---

# Context Preservation Skill

## Purpose

This skill implements Shannon Framework's zero-context-loss preservation system through systematic checkpoint creation, metadata collection, and Serena MCP storage. It ensures that no project progress is lost due to context compaction, session interruptions, or multi-wave execution.

**Core Value**: Transforms fragile multi-session work into reliable, resumable workflows with complete state preservation.

## When to Use

Use this skill in these situations:

**MANDATORY (Must Use)**:
- Before any wave transition (Wave 1 → Wave 2, etc.)
- When PreCompact hook triggers (automatic, emergency save)
- When user explicitly requests checkpoint (`/sh_checkpoint`)
- At end of session before closing Claude Code
- After completing significant milestones (MVP, release, major feature)

**RECOMMENDED (Should Use)**:
- After every 2-3 hours of continuous work
- Before starting risky/experimental changes
- After test suite passes completely
- Before context reaches 70% of token limit

**CONDITIONAL (May Use)**:
- User requests manual save point
- Handoff between agents requires state transfer
- Documentation milestone reached

DO NOT rationalize skipping checkpoints because:
- ❌ "This is a simple task" → Interruptions happen regardless of complexity
- ❌ "PreCompact hook will handle it" → Hook is emergency fallback, not primary strategy
- ❌ "User didn't ask for it" → Checkpoints are Shannon PROTOCOL, not user's responsibility
- ❌ "Checkpoints are overhead" → 30 seconds now saves hours of rework later
- ❌ "I'll checkpoint when I remember" → Must be systematic, not discretionary

## Core Competencies

1. **Checkpoint Creation**: Generates structured checkpoints with rich metadata (goals, waves, tests, files, agent states)
2. **Metadata Collection**: Gathers comprehensive context (project state, progress tracking, deliverables, blockers)
3. **Serena Storage**: Persists checkpoints to Serena MCP knowledge graph with relationships
4. **Restoration Logic**: Enables full project state restoration from checkpoint ID
5. **PreCompact Integration**: Automatic emergency saves when context compaction triggers
6. **Wave Coordination**: Checkpoint-based handoffs between waves and agents

## Inputs

**Required:**
- `mode` (string): Operation mode
  - `"checkpoint"`: Manual user-requested checkpoint
  - `"wave-checkpoint"`: Automatic wave boundary checkpoint
  - `"precompact"`: Emergency save triggered by PreCompact hook
  - `"session-end"`: Clean session closure checkpoint
- `label` (string): Human-readable checkpoint label (e.g., "wave-2-complete", "mvp-launch")

**Optional:**
- `wave_number` (integer): Current wave number if in wave execution
- `include_files` (boolean): Include modified file list (default: true)
- `include_tests` (boolean): Include test results if available (default: true)
- `compression` (boolean): Enable gzip compression for large checkpoints (default: true)

## Workflow

### Phase 1: Context Collection

**Step 1: Identify Active Context**
- Action: Determine what context is currently active
- Tool: Internal state analysis
- Output: Context type (wave, goal, test, implementation)

**Step 2: Collect Project Metadata**
- Action: Gather project information (name, path, domains, technologies, file count)
- Tool: Read (for .shannon/project.json if exists)
- Output: Project metadata object

**Step 3: Collect Goal State**
- Action: Query active goals from goal-management skill (if available)
- Tool: Serena MCP (`search_nodes` for shannon/goals)
- Output: Active goals with progress percentages

**Step 4: Collect Wave State**
- Action: Gather wave execution history (current wave, completed waves, agent states)
- Tool: Serena MCP (shannon/waves namespace)
- Output: Wave history object

**Step 5: Collect Task Progress**
- Action: Summarize task completion state (total, completed, in-progress, blocked)
- Tool: Read (TODO comments, task files)
- Output: Task summary object

**Step 6: Collect Test Results**
- Action: Gather most recent test execution results (platform, counts, NO MOCKS compliance)
- Tool: Read (test result files, logs)
- Output: Test results object

**Step 7: Collect Modified Files**
- Action: Identify files changed during this session
- Tool: Bash (`git status`, `git diff --name-only`)
- Output: Array of file paths with modification timestamps

**Step 8: Collect MCP Status**
- Action: Record which MCPs are available (required, recommended, conditional)
- Tool: Serena MCP introspection
- Output: MCP availability object

### Phase 2: Checkpoint Structure Creation

**Step 9: Generate Checkpoint ID**
- Action: Create unique checkpoint identifier
- Format: `SHANNON-W{wave}-{YYYYMMDD}T{HHMMSS}`
- Example: `SHANNON-W2-20251103T143000`

**Step 10: Create Conversation Summary**
- Action: Summarize conversation for restoration context (200-500 chars)
- Method: Extract key points from recent messages

**Step 11: Identify Next Actions**
- Action: Determine what should happen after restoration (3-5 actions)
- Sources: Current task, next wave, agent SITREP, user's last intent

**Step 12: Assemble Complete Checkpoint**
- Action: Combine all collected data into checkpoint structure
- Validation: Verify all required fields present

### Phase 3: Serena MCP Storage

**Step 13: Create Checkpoint Entity**
- Tool: Serena MCP `create_entities`
- Entity: Type=checkpoint, Name=checkpoint_id, Observations=[JSON checkpoint]

**Step 14: Create Context Relations**
- Tool: Serena MCP `create_relations`
- Relations: checkpoint→project, checkpoint→previous_checkpoint, checkpoint→wave_deliverables

**Step 15: Store Supplementary Data**
- Tool: Serena MCP `add_observations`
- Data: Wave deliverables, test results, project index, task details

**Step 16: Compute Integrity Hash**
- Action: Generate SHA-256 hash of checkpoint data for validation

### Phase 4: Confirmation & User Notification

**Step 17: Generate Restoration Command**
- Format: `/sh_restore {checkpoint_id}`

**Step 18: Calculate Checkpoint Size**
- Method: Count JSON string bytes, display in KB/MB

**Step 19: Present Checkpoint Summary**
- Display: Checkpoint ID, label, wave, progress, tests, files, size
- Include: Restoration command, storage location, retention period

**Step 20: Return Checkpoint ID**
- Output: checkpoint_id string for programmatic use

## Anti-Rationalization Section

**🚨 PROTOCOL ENFORCEMENT 🚨**

This section addresses every rationalization pattern from RED phase baseline testing:

### Rationalization 1: "Checkpoints are overhead for simple waves"

**Detection**: Task complexity < 0.30, single wave, "quick implementation"

**Violation**: Skip checkpoint creation due to perceived simplicity

**Counter-Argument**:
- Checkpoint creation: 30 seconds
- Context loss rework: 1-3 hours
- Interruption probability: 20-40% even for "simple" tasks
- ROI: 120x-360x return on 30 second investment

**Protocol**: Create checkpoint at wave boundary regardless of complexity score. Even 0.10 complexity tasks get checkpoints.

---

### Rationalization 2: "I'll checkpoint when I think of it"

**Detection**: No automated checkpoint trigger, relying on memory/discretion

**Violation**: Skip systematic checkpointing in favor of ad-hoc manual approach

**Counter-Argument**:
- Human memory is unreliable under cognitive load
- Discretionary checkpointing = 70-80% skip rate (RED phase data)
- Shannon Framework requires systematic, not discretionary checkpoints
- PROTOCOL skills follow structure, not judgment

**Protocol**: Mandatory checkpoints at wave boundaries. Discretion is not permitted. Follow the workflow.

---

### Rationalization 3: "User didn't ask for checkpoints"

**Detection**: User provides spec without mentioning checkpoints explicitly

**Violation**: Skip checkpoints because user request is missing

**Counter-Argument**:
- Users don't request "save file" either - it's automatic
- Checkpoints are Shannon Framework infrastructure, not user concern
- Context preservation is Claude Code's responsibility
- User assumes work will persist - checkpoints ensure it does

**Protocol**: Checkpoints are framework responsibility, not user's. Create them automatically as part of Shannon workflow.

---

### Rationalization 4: "PreCompact hook will handle it"

**Detection**: Approaching token limits, relying on emergency hook

**Violation**: Skip proactive checkpointing, rely on emergency fallback

**Counter-Argument**:
- PreCompact saves minimal context (emergency mode)
- Missing: wave deliverables, structured metadata, next actions
- Hook is last resort, not primary mechanism
- Proactive checkpoints have 10x more metadata

**Protocol**: PreCompact hook is emergency fallback. Create wave-checkpoints proactively with full metadata.

---

### Rationalization 5: "Checkpoints slow down development"

**Detection**: Time pressure, fast turnaround requested

**Violation**: Skip checkpoints to maximize implementation velocity

**Counter-Argument**:
- Checkpoint: 30 seconds per wave
- Mid-wave failure: 1-3 hours complete rework
- Time pressure increases interruption risk
- Net effect: Checkpoints SPEED development by preventing rework

**Protocol**: Time pressure increases checkpoint value. Never skip checkpoints to "go faster." 30s investment prevents hours of loss.

---

### Enforcement Mechanism

This skill is **PROTOCOL** type:
- Follow the workflow structure precisely
- No discretionary skipping of steps
- No "judgment calls" about whether checkpoint is needed
- If at wave boundary → create checkpoint, period

**Violation Detection**:
If you find yourself thinking any of these:
- "This task is too simple for a checkpoint"
- "I'll checkpoint later if needed"
- "User didn't ask for it"
- "The hook will handle it"
- "Checkpoints waste time"

**STOP**. You are rationalizing. Return to PROTOCOL workflow. Create the checkpoint.

## Outputs

Structured output object:

```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W2-20251103T143000",
  "label": "wave-2-complete",
  "type": "wave-checkpoint",
  "size_bytes": 45623,
  "size_kb": "44.6 KB",
  "compression": "gzip",
  "storage_location": "serena://shannon/checkpoints/SHANNON-W2-20251103T143000",
  "restore_command": "/sh_restore SHANNON-W2-20251103T143000",
  "retention_days": 30,
  "expires_at": "2025-12-03T14:30:00.000Z",
  "integrity_hash": "sha256:a7f2b3d4e5f6...",
  "summary": {
    "wave": 2,
    "wave_status": "complete",
    "tasks_completed": 35,
    "tasks_total": 47,
    "tests_passed": 23,
    "tests_total": 23,
    "files_modified": 12
  },
  "next_actions": [
    "Start Wave 3: Frontend integration with backend APIs",
    "Test complete auth flow with Puppeteer"
  ]
}
```

## Success Criteria

This skill succeeds if:

1. ✅ **Checkpoint Created**: Valid checkpoint entity in Serena MCP with complete metadata
2. ✅ **Relations Established**: Checkpoint linked to project, previous checkpoint, wave deliverables
3. ✅ **Integrity Verified**: SHA-256 hash generated and stored for validation
4. ✅ **User Notified**: Clear confirmation message with restore command displayed
5. ✅ **Restorable**: Checkpoint can be successfully restored by context-restoration skill

Validation:
```python
def validate_checkpoint(checkpoint_id):
    # Check 1: Entity exists in Serena
    checkpoint = serena.open_nodes([checkpoint_id])
    assert checkpoint is not None

    # Check 2: Has required fields
    data = json.loads(checkpoint.observations[0])
    assert "checkpoint_id" in data
    assert "context" in data
    assert "metadata" in data

    # Check 3: Integrity hash valid
    computed_hash = sha256(json.dumps(data, sort_keys=True))
    assert computed_hash == data["metadata"]["integrity_hash"]

    # Check 4: Can restore
    restoration_result = restore_checkpoint(checkpoint_id)
    assert restoration_result.success
```

## Common Pitfalls

### Pitfall 1: Skipping "Simple" Checkpoints

**Wrong:**
```
This is just a quick 2-phase task. No need for checkpoints.
Let me implement directly without the overhead.
```

**Right:**
```
Creating checkpoint before Wave 1, even for simple tasks.
Reason: Interruptions happen regardless of complexity.
Checkpoint cost: 30 seconds. Rework cost: 2 hours.
```

**Why**: Checkpoint overhead (30s) is trivial compared to rework cost (hours). Even "simple" tasks get interrupted. **Always checkpoint at wave boundaries**, regardless of complexity.

---

### Pitfall 2: Relying on PreCompact Hook Alone

**Wrong:**
```
There's a PreCompact hook, so checkpoints are automatic.
I don't need to create wave checkpoints manually.
```

**Right:**
```
PreCompact hook is emergency fallback, not primary strategy.
Creating structured wave-checkpoint with rich metadata now.
Emergency saves lack wave deliverables and context.
```

**Why**: PreCompact hook saves minimal context in emergency situations. **Proactive wave checkpoints** include structured metadata that emergency saves lack.

---

### Pitfall 3: Discretionary Checkpointing

**Wrong:**
```
User didn't ask for checkpoint. I'll create one if I remember,
or if I think the work is significant enough.
```

**Right:**
```
Checkpoints are Shannon PROTOCOL, not discretionary.
Wave boundary reached → checkpoint created automatically.
User request is not required for mandatory checkpoints.
```

**Why**: Checkpointing cannot be left to discretion. **Shannon mandates checkpoints** at wave boundaries, period. This is PROTOCOL skill type - follow the structure.

## Examples

### Example 1: Manual User-Requested Checkpoint

**Input:**
```json
{
  "mode": "checkpoint",
  "label": "mvp-feature-complete",
  "include_files": true,
  "include_tests": true
}
```

**Process:**
1. Collect context: E-commerce platform, MVP features complete
2. Gather metadata: 3 waves complete, 42/47 tasks, all tests passing
3. Create checkpoint structure with comprehensive metadata
4. Store in Serena: Entity + relations + supplementary data
5. Generate integrity hash
6. Return checkpoint ID and confirmation

**Output:**
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W3-20251103T163000",
  "label": "mvp-feature-complete",
  "type": "checkpoint",
  "size_kb": "52.3 KB",
  "restore_command": "/sh_restore SHANNON-W3-20251103T163000",
  "summary": {
    "wave": 3,
    "tasks_completed": 42,
    "tests_passed": 31,
    "files_modified": 18
  }
}
```

---

### Example 2: Automatic Wave Checkpoint

**Input:**
```json
{
  "mode": "wave-checkpoint",
  "label": "wave-2-complete",
  "wave_number": 2
}
```

**Process:**
1. Detect wave boundary transition (Wave 2 → Wave 3)
2. Collect wave deliverables from Wave 2
3. Query agent states (2 agents completed work)
4. Gather test results (23 tests, all passing)
5. Create wave-checkpoint with deliverables
6. Store completion artifacts in Serena
7. Link to Wave 2 deliverables entity

**Output:**
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-W2-20251103T140000",
  "label": "wave-2-complete",
  "type": "wave-checkpoint",
  "summary": {
    "wave": 2,
    "wave_status": "complete",
    "deliverables_count": 8,
    "agents_used": ["backend-dev", "test-dev"],
    "tests_passed": 23
  }
}
```

---

### Example 3: Emergency PreCompact Checkpoint

**Input:**
```json
{
  "mode": "precompact",
  "label": "emergency-20251103T153000",
  "compression": true
}
```

**Process:**
1. Triggered by PreCompact hook
2. Fast metadata collection (skip optional fields)
3. Aggressive gzip compression
4. Store critical context only
5. Mark as emergency type (extended retention)
6. Return immediately

**Output:**
```json
{
  "success": true,
  "checkpoint_id": "SHANNON-EMERGENCY-20251103T153000",
  "type": "precompact",
  "size_kb": "28.1 KB",
  "retention_days": 60,
  "note": "Emergency checkpoint - restore ASAP"
}
```

## Validation

How to verify this skill worked correctly:

1. **Serena Entity Created**: Use `search_nodes` to verify checkpoint entity exists
2. **Checkpoint Data Complete**: Use `open_nodes` to verify metadata present
3. **Relations Established**: Verify links to project, previous checkpoint, deliverables
4. **Integrity Hash Valid**: Compute SHA-256, compare to stored hash
5. **Restoration Works**: Invoke context-restoration skill, verify success

## Progressive Disclosure

**In SKILL.md** (this file):
- Core checkpoint workflow (~600 lines)
- Anti-rationalization patterns from RED phase
- Essential examples (manual, wave, emergency)

**In references/** (for deep details):
- `references/CHECKPOINT_SCHEMA.md`: Complete schema specification
- `references/SERENA_OPERATIONS.md`: Detailed MCP integration
- `references/PRECOMPACT_INTEGRATION.md`: Hook implementation

## References

- Core Documentation: `shannon-plugin/core/CONTEXT_MANAGEMENT.md`
- Related Skills: `@context-restoration`, `@goal-management`, `@wave-orchestration`
- MCP Setup: `/sh_check_mcps` for Serena MCP configuration
- Hook: `.claude-plugin/hooks/pre_compact.py`

---

**Skill Type**: PROTOCOL - Follow structure precisely, no discretionary skipping
