---
name: sc:load
command: /sc:load
description: "Enhanced session lifecycle management with Shannon project activation and automatic checkpoint restoration"
category: command
complexity: standard
mcp-servers: [serena]
personas: [analyzer, architect]
wave-enabled: false
shannon-v3-enhanced: true
base-command: SuperClaude /sc:load
---

# /sc:load - Enhanced Project Context Loading

## Purpose

Load project context and establish session state with enhanced Shannon V3 capabilities:
- **SuperClaude Base**: Project activation, memory retrieval, session management
- **Shannon Enhancement**: Automatic checkpoint detection and restoration
- **Zero Context Loss**: Seamless recovery from auto-compact events
- **Wave Awareness**: Restore multi-wave execution state
- **Cross-Session Persistence**: Perfect continuation across session boundaries

## Activation Triggers

### Automatic
- Session initialization in Shannon-enabled projects
- New conversation start in registered Shannon project directory
- Context restored after Claude Code restart
- Project directory change detection

### Manual
- User types `/sc:load` or `/sc:load [path]`
- Checkpoint restoration needed: `/sc:load --restore`
- Force refresh: `/sc:load --refresh`
- Wave state recovery: `/sc:load --wave-state`

## Usage Patterns

```bash
# Basic project loading (SuperClaude + Shannon)
/sc:load

# Load specific project with Shannon activation
/sc:load /path/to/shannon/project

# Load with automatic checkpoint restoration
/sc:load --restore

# Load latest checkpoint explicitly
/sc:load --restore --latest

# Load specific checkpoint by name
/sc:load --restore shannon_checkpoint_before_wave_3

# List available checkpoints
/sc:load --list-checkpoints

# Refresh project context (re-analyze)
/sc:load --refresh

# Load with wave state recovery
/sc:load --wave-state

# Load dependency context
/sc:load --type deps --refresh

# Combine Shannon and SuperClaude flags
/sc:load --restore --analyze --refresh
```

## Shannon V3 Enhancements

### 1. Automatic Checkpoint Detection

When `/sc:load` executes in Shannon project:

```yaml
detection_flow:
  step_1: "Check if Serena MCP available"
  step_2: "list_memories() to scan for checkpoints"
  step_3: "Identify checkpoint types"
  step_4: "Detect PreCompact checkpoints (auto-saved)"
  step_5: "Present restoration options if found"
```

**Checkpoint Types Detected**:
- `shannon_precompact_checkpoint_*` - Auto-saved before context compact
- `shannon_checkpoint_*` - User-created manual checkpoints
- `wave_*_complete` - Wave execution state markers
- `spec_analysis_*` - Specification analysis results
- `phase_plan` - Execution planning state

### 2. Intelligent Restoration Logic

```yaml
restoration_priority:
  critical_context_loss:
    trigger: "No active session context found"
    action: "Auto-restore latest PreCompact checkpoint"
    user_prompt: false

  session_continuation:
    trigger: "Previous session detected (< 24 hours)"
    action: "Offer to restore last checkpoint"
    user_prompt: true

  normal_load:
    trigger: "Fresh session, no context loss"
    action: "Standard project activation"
    user_prompt: false

  explicit_restore:
    trigger: "--restore flag present"
    action: "Execute checkpoint restoration"
    user_prompt: "if checkpoint name not specified"
```

### 3. Shannon Project Activation

Enhanced beyond SuperClaude's project loading:

```yaml
shannon_activation:
  validate_shannon_project:
    check: "Shannon/Core/ directory exists"
    check: "SHANNON_V3_SPECIFICATION.md present"
    check: "Commands/ and Agents/ directories exist"

  load_shannon_core:
    action: "Read SPEC_ANALYSIS.md patterns"
    action: "Load TESTING_PHILOSOPHY.md"
    action: "Load PROJECT_MEMORY.md"
    action: "Load WAVE_ORCHESTRATION.md"

  activate_serena_integration:
    action: "activate_project for Shannon project"
    action: "Load all wave memories if present"
    action: "Restore execution state"

  establish_wave_context:
    action: "Identify active wave (if any)"
    action: "Load previous wave results"
    action: "Prepare for continuation"
```

## Execution Flow

### Phase 1: Initialization

```
┌─────────────────────────────────────────────────────┐
│ INITIALIZATION                                      │
├─────────────────────────────────────────────────────┤
│ 1. Establish Serena MCP connection                 │
│ 2. Identify project type (Shannon vs SuperClaude)  │
│ 3. Determine session state (new/continue/restore)  │
│ 4. Set restoration strategy                        │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
```

### Phase 2: Shannon Detection & Analysis

```
┌─────────────────────────────────────────────────────┐
│ SHANNON PROJECT DETECTION                           │
├─────────────────────────────────────────────────────┤
│ Check: Shannon/Core/ exists?                        │
│   YES: Shannon V3 project detected                  │
│        → Enhanced loading with checkpoint support   │
│   NO:  Standard SuperClaude project                 │
│        → Basic context loading                      │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────┐
│ CHECKPOINT SCAN (Shannon projects only)             │
├─────────────────────────────────────────────────────┤
│ Execute: list_memories()                            │
│                                                     │
│ Search for:                                         │
│ - shannon_precompact_checkpoint_* (auto)           │
│ - shannon_checkpoint_* (manual)                    │
│ - wave_*_complete (execution state)                │
│ - spec_analysis_* (spec results)                   │
│                                                     │
│ Sort by timestamp (most recent first)              │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
```

### Phase 3: Restoration Decision

```
┌─────────────────────────────────────────────────────┐
│ RESTORATION DECISION LOGIC                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│ IF --restore flag OR critical context loss:        │
│   → Execute automatic restoration                  │
│                                                     │
│ ELSE IF PreCompact checkpoint < 1 hour old:       │
│   → Offer restoration to user                      │
│   → "Recent checkpoint found, restore? (y/n)"      │
│                                                     │
│ ELSE:                                               │
│   → Standard project activation                    │
│   → Load available memories                        │
│                                                     │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
```

### Phase 4: Context Loading

```
┌─────────────────────────────────────────────────────┐
│ CONTEXT LOADING & RESTORATION                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Standard Loading (no checkpoint):                  │
│   1. activate_project(project_path)                │
│   2. list_memories() → identify available context  │
│   3. read_memory() for core memories               │
│   4. Establish project understanding               │
│                                                     │
│ Checkpoint Restoration (checkpoint detected):      │
│   1. read_memory("[checkpoint_name]")              │
│   2. Extract serena_memory_keys list               │
│   3. Load ALL memories from checkpoint             │
│   4. Restore wave state                            │
│   5. Restore todo list                             │
│   6. Resume from saved position                    │
│                                                     │
└─────────────┬───────────────────────────────────────┘
              │
              ▼
```

### Phase 5: Validation & Readiness

```
┌─────────────────────────────────────────────────────┐
│ VALIDATION & SESSION READINESS                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Validate:                                           │
│ ✓ Project context loaded                           │
│ ✓ Serena memories accessible                       │
│ ✓ Wave state identified (if applicable)            │
│ ✓ Next action clear                                │
│                                                     │
│ Report to user:                                     │
│ - Project name and type                            │
│ - Loaded memories count                            │
│ - Active wave (if any)                             │
│ - Restoration status                               │
│ - Next recommended action                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## MCP Integration

### Serena MCP (Mandatory)

**Core Operations**:
- `activate_project(path)` - Project activation and context establishment
- `list_memories()` - Enumerate all stored memories
- `read_memory(key)` - Retrieve specific memory content
- `search_nodes(query)` - Find relevant context by query

**Shannon-Specific Usage**:
```yaml
checkpoint_detection:
  tool: list_memories()
  filter: "shannon_checkpoint_*, shannon_precompact_checkpoint_*"
  sort: "timestamp descending"

checkpoint_restoration:
  step_1: read_memory("[checkpoint_name]")
  step_2: "Extract serena_memory_keys array"
  step_3: "read_memory() for each key"
  step_4: "Reconstruct session state"

wave_context_loading:
  tool: read_memory("wave_[N]_complete")
  action: "Load all previous wave results"
  purpose: "Cross-wave context for agents"
```

### Performance Requirements

```yaml
performance_targets:
  standard_load: "< 500ms"
  checkpoint_restoration: "< 2s for 20 memories"
  wave_context_loading: "< 1s per wave"
  serena_activation: "< 200ms"
```

## Output Format

### Standard Load (No Checkpoint)

```
🔧 Project Context Loading

PROJECT: /path/to/shannon/project
TYPE: Shannon V3 Project ✨

📋 Serena Memories Loaded:
  ✓ spec_analysis_001
  ✓ phase_plan
  ✓ wave_1_complete
  ✓ wave_2a_complete
  ✓ wave_2b_complete
  Total: 5 memories loaded

📊 Project State:
  • Framework: Shannon V3
  • Active Wave: Wave 3 (Integration Testing)
  • Phase: Implementation (Phase 3 of 5)
  • Completion: ~45%

🎯 Next Action:
  Continue Wave 3 integration testing
  Use /sh:execute-wave to resume

✅ Session Ready - Context Loaded
```

### Checkpoint Restoration

```
🔧 Project Context Loading with Checkpoint Restoration

PROJECT: /path/to/shannon/project
TYPE: Shannon V3 Project ✨

🔍 Checkpoint Detection:
  Found: shannon_precompact_checkpoint_001
  Created: 2025-09-29 19:45:23
  Reason: Auto-save before context compact
  Age: 15 minutes ago

📦 Restoring from Checkpoint...

✅ Checkpoint Loaded: shannon_precompact_checkpoint_001

📋 Context Restored (15 Serena keys):
  ✓ spec_analysis_001
  ✓ requirements_final
  ✓ architecture_complete
  ✓ phase_plan
  ✓ wave_1_complete
  ✓ wave_2a_complete
  ✓ wave_2b_complete
  ✓ wave_3_in_progress
  ... (15 total)

📊 Restored State:
  • Active Wave: Wave 3 (Integration Testing)
  • Phase: Implementation (Phase 3 of 5)
  • Todos: 7 active, 12 completed
  • Completion: ~45%

🎯 Resume From:
  Wave 3 integration testing
  Next: Complete frontend-backend integration tests

✅ Zero Context Loss - Ready to Continue
```

### Multiple Checkpoints Available

```
🔧 Project Context Loading

PROJECT: /path/to/shannon/project
TYPE: Shannon V3 Project ✨

🔍 Multiple Checkpoints Found:

1. shannon_precompact_checkpoint_002 (RECENT - AUTO)
   Created: 2025-09-29 21:30:15
   State: Wave 4 complete, starting Wave 5
   Age: 10 minutes ago ⚡

2. shannon_checkpoint_end_of_day (MANUAL)
   Created: 2025-09-29 18:00:00
   State: Wave 3 complete, validated
   Age: 3 hours ago

3. shannon_checkpoint_before_wave_3 (MANUAL)
   Created: 2025-09-29 14:30:00
   State: Waves 1-2 complete, ready for Wave 3
   Age: 7 hours ago

Which checkpoint to restore?
  [1] Latest PreCompact (recommended)
  [2] End of day checkpoint
  [3] Before Wave 3 checkpoint
  [0] None - standard load

>
```

## Tool Coordination

```yaml
primary_tools:
  - activate_project: "Serena MCP project activation"
  - list_memories: "Enumerate stored memories"
  - read_memory: "Load specific memory content"
  - Read: "Load Shannon core files"
  - Glob: "Discover Shannon project structure"

secondary_tools:
  - Grep: "Search Shannon specification files"
  - Write: "Create session documentation"
  - TodoWrite: "Initialize todo list from checkpoint"
```

## Integration with Other Commands

### Command Chaining Patterns

```bash
# Load and analyze
/sc:load && /sh:analyze-spec

# Load and continue wave execution
/sc:load --restore && /sh:execute-wave

# Load and create checkpoint
/sc:load && /sh:checkpoint before_risky_operation

# Load and show status
/sc:load && /sh:status
```

### Auto-Activation Patterns

- `/sh:*` commands automatically invoke `/sc:load` if context not loaded
- Wave execution commands verify context before proceeding
- Checkpoint commands verify Serena connection via load

## Examples

### Example 1: New Session in Shannon Project

```bash
User: /sc:load

Output:
🔧 Project Context Loading

PROJECT: /Users/dev/ecommerce-platform
TYPE: Shannon V3 Project ✨

📋 Serena Memories Loaded:
  ✓ spec_analysis_001 (E-commerce platform specification)
  ✓ phase_plan (5-phase implementation plan)
  Total: 2 memories loaded

📊 Project State:
  • Framework: Shannon V3
  • Status: Specification analyzed, planning complete
  • Phase: Ready for Wave 1 (Foundation)
  • Completion: 0% (implementation not started)

🎯 Next Action:
  Begin implementation with /sh:execute-wave
  Wave 1 will establish project foundation

✅ Session Ready - Context Loaded
```

### Example 2: Restoration After Auto-Compact

```bash
# Context automatically compacted by Claude Code
# User continues conversation

Claude: 🚨 Context Restoration Needed

🔍 PreCompact Checkpoint Detected:
  shannon_precompact_checkpoint_003
  Created: Just before auto-compact (5 minutes ago)
  State: Wave 3 in progress

Would you like to restore? (Recommended)

User: yes

Claude: 📦 Restoring from Checkpoint...

✅ Checkpoint Loaded: shannon_precompact_checkpoint_003

📋 Context Restored (18 Serena keys):
  ✓ All specification analysis
  ✓ All phase planning
  ✓ Wave 1 complete
  ✓ Wave 2a complete
  ✓ Wave 2b complete
  ✓ Wave 3 in progress (45% complete)

📊 Restored State:
  • Active Wave: Wave 3 (Integration Testing)
  • Active Todos: 7 tasks
  • Next: Complete frontend-backend integration

✅ Zero Context Loss - Seamlessly Resumed
```

### Example 3: Load Specific Checkpoint

```bash
User: /sc:load --restore shannon_checkpoint_before_experiment

Output:
📦 Loading Checkpoint: shannon_checkpoint_before_experiment

✅ Checkpoint Loaded

📋 Context Restored (12 Serena keys):
  ✓ Complete state before experimental approach
  ✓ Wave 2 validated and stable
  ✓ All tests passing

📊 Restored State:
  • Restored to: Before experimental refactoring
  • Active Wave: Wave 2 complete
  • Status: Stable baseline restored

🎯 Next Action:
  Re-attempt experiment or choose different approach

✅ Rollback Successful
```

### Example 4: List Available Checkpoints

```bash
User: /sc:load --list-checkpoints

Output:
📋 Available Shannon Checkpoints

🔄 PreCompact Checkpoints (Auto-saved):
1. shannon_precompact_checkpoint_003
   • Created: 2025-09-29 21:30:15 (10 min ago)
   • State: Wave 4 complete
   • Keys: 20 memories preserved

2. shannon_precompact_checkpoint_002
   • Created: 2025-09-29 18:45:00 (3 hours ago)
   • State: Wave 3 in progress
   • Keys: 18 memories preserved

📌 Manual Checkpoints:
1. shannon_checkpoint_end_of_day
   • Created: 2025-09-29 18:00:00 (3.5 hours ago)
   • State: Wave 3 complete, validated
   • Keys: 15 memories preserved

2. shannon_checkpoint_before_experiment
   • Created: 2025-09-29 14:30:00 (7 hours ago)
   • State: Wave 2 stable baseline
   • Keys: 12 memories preserved

To restore: /sc:load --restore [checkpoint-name]
```

## Boundaries

### Will

- Load project context with Serena MCP integration
- Detect and offer restoration from checkpoints
- Automatically activate Shannon V3 project features
- Restore complete session state from checkpoints
- Load wave execution context for continuation
- Provide session lifecycle management
- Initialize cross-session persistence

### Will Not

- Modify project structure without permission
- Execute wave commands automatically (user triggers execution)
- Create checkpoints (use `/sh:checkpoint` for that)
- Override existing context without confirmation
- Load context without Serena MCP availability
- Execute restoration without validation

### Relationship to Other Commands

- **Complements `/sh:checkpoint`**: Load reads checkpoints, checkpoint creates them
- **Enables `/sh:restore`**: Load can automatically restore, restore is explicit
- **Prerequisite for `/sh:execute-wave`**: Waves require loaded context
- **Works with `/sh:status`**: Load establishes state, status reports it
- **Integrates with `/sc:save`**: Load starts session, save ends it

## Performance Optimization

```yaml
optimization_strategies:
  lazy_loading:
    description: "Load only essential memories initially"
    defer: "Wave-specific memories until needed"

  parallel_operations:
    description: "Load multiple memories concurrently"
    batch_size: 5

  caching:
    description: "Cache loaded memories for session"
    duration: "session lifetime"

  smart_detection:
    description: "Quick filesystem checks before Serena queries"
    skip: "Skip Serena if not Shannon project"
```

## Error Handling

```yaml
error_scenarios:
  serena_unavailable:
    detection: "Serena MCP connection fails"
    fallback: "Basic project loading without memories"
    message: "⚠️ Serena MCP unavailable - limited context loading"

  checkpoint_corrupted:
    detection: "Checkpoint memory read fails"
    fallback: "Offer previous checkpoint or standard load"
    message: "⚠️ Checkpoint corrupted - trying previous checkpoint"

  no_shannon_project:
    detection: "Shannon/Core/ directory missing"
    action: "Standard SuperClaude load"
    message: "Standard project (not Shannon V3)"

  wave_state_mismatch:
    detection: "Wave state inconsistent with memories"
    action: "Report inconsistency, offer reconciliation"
    message: "⚠️ Wave state inconsistency detected"
```

## Quality Gates

### Pre-Load Validation
- Serena MCP connection verified
- Project directory accessible
- Shannon structure valid (if Shannon project)

### Post-Load Validation
- Required memories loaded successfully
- Session state established
- Next action identified
- User informed of status

### Restoration Validation
- All checkpoint memories restored
- Wave state consistent
- Todo list reconstructed
- Execution context valid

---

**Status**: Shannon V3 Enhanced
**Base Command**: SuperClaude /sc:load
**Enhancement Type**: Checkpoint integration, Shannon project support
**Critical Dependency**: Serena MCP
**Related Commands**: /sh:checkpoint, /sh:restore, /sh:execute-wave, /sh:status