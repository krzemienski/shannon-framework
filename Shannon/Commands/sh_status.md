---
name: sh:status
command: /sh:status
description: Display current project state and memory overview from Serena MCP
category: command
sub_agents: [CONTEXT_GUARDIAN]
mcp_servers: [serena]
version: 3.0
---

# /sh:status - Project Status Dashboard

## Purpose

Display comprehensive project status by querying Serena MCP for all stored memories and presenting an organized overview of project state, progress, and context.

**Core Objective**: Provide instant visibility into project state, memory health, and continuation readiness.

---

## Command Metadata

```yaml
command: /sh:status
aliases: [status, state, project-status]
category: Project Management
sub_agent: CONTEXT_GUARDIAN
mcp_servers:
  primary: Serena
  required: true
tools:
  - list_memories
  - read_memory
outputs:
  - Project status dashboard
  - Memory category breakdown
  - Checkpoint information
  - Continuation readiness
```

---

## Usage Patterns

### Basic Usage
```bash
# Display full project status
/sh:status

# Quick status check (abbreviated)
/sh:status --brief

# Status for specific project
/sh:status project_taskapp
```

### Context-Aware Usage
```bash
# After session break
User returns after break → /sh:status
Claude shows: Last checkpoint, pending work, project phase

# Before starting work
Morning session start → /sh:status
Claude shows: Yesterday's progress, today's priorities

# After auto-compact
Context restored → /sh:status
Claude shows: Checkpoint validity, memory integrity
```

---

## Execution Flow

### Step 1: Activate CONTEXT_GUARDIAN

**Sub-Agent Activation**:
```python
# Activate specialized memory inspection agent
activate_agent("CONTEXT_GUARDIAN")

# Agent characteristics:
# - Reads all Serena memory keys
# - Categorizes by memory hierarchy
# - Validates checkpoint integrity
# - Reports memory health
```

### Step 2: List All Memories

**Serena MCP Query**:
```python
# STEP 1: List all available memory keys
all_keys = list_memories()

# STEP 2: Categorize by hierarchy level
categorized = {
    'project_foundation': [],
    'wave_context': [],
    'phase_context': [],
    'session_state': [],
    'checkpoints': [],
    'decisions': [],
    'other': []
}

for key in all_keys:
    if 'project_' in key and any(x in key for x in ['spec_analysis', 'phase_plan', 'decisions', 'final_results']):
        categorized['project_foundation'].append(key)
    elif 'wave_' in key:
        categorized['wave_context'].append(key)
    elif 'phase_' in key:
        categorized['phase_context'].append(key)
    elif 'session_' in key:
        categorized['session_state'].append(key)
    elif 'checkpoint' in key:
        categorized['checkpoints'].append(key)
    elif 'decision_' in key:
        categorized['decisions'].append(key)
    else:
        categorized['other'].append(key)
```

### Step 3: Read Latest Checkpoint

**Checkpoint Analysis**:
```python
# STEP 1: Find latest checkpoint
try:
    latest_checkpoint_key = read_memory("latest_checkpoint")
    checkpoint_data = read_memory(latest_checkpoint_key)
    checkpoint_valid = True
except:
    checkpoint_valid = False
    checkpoint_data = None

# STEP 2: Extract checkpoint details
if checkpoint_valid:
    project_id = checkpoint_data.get('project_id')
    active_phase = checkpoint_data['state'].get('active_phase')
    current_wave = checkpoint_data['state'].get('current_wave')
    timestamp = checkpoint_data.get('timestamp')
    todo_list = checkpoint_data['state'].get('todo_list', [])
    completed_today = checkpoint_data['state'].get('completed_today', [])
```

### Step 4: Analyze Memory Health

**Health Metrics**:
```python
# Calculate memory health indicators
health_metrics = {
    'total_memories': len(all_keys),
    'has_foundation': len(categorized['project_foundation']) > 0,
    'has_checkpoint': checkpoint_valid,
    'recent_activity': check_recent_timestamps(all_keys),
    'memory_age': calculate_oldest_memory(all_keys),
    'checkpoint_age': calculate_checkpoint_age(checkpoint_data)
}

# Determine health status
if health_metrics['has_foundation'] and health_metrics['has_checkpoint']:
    health_status = "✅ HEALTHY"
elif health_metrics['has_foundation']:
    health_status = "⚠️ CHECKPOINT MISSING"
else:
    health_status = "🚨 NO PROJECT CONTEXT"
```

### Step 5: Generate Status Dashboard

**Output Assembly**:
```python
# Build comprehensive status report
status_dashboard = generate_dashboard(
    categorized_memories=categorized,
    checkpoint_data=checkpoint_data,
    health_metrics=health_metrics,
    health_status=health_status
)

# Return formatted output
return status_dashboard
```

---

## Output Format

### Full Dashboard Template

```markdown
📊 PROJECT STATUS DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Overall Status
**Health**: ✅ HEALTHY
**Total Memories**: 24
**Last Checkpoint**: precompact_checkpoint_20250930_143000
**Project**: project_taskapp

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Memory Breakdown by Category

### 📦 Project Foundation (Indefinite Retention)
- project_taskapp_spec_analysis_20250930
- project_taskapp_phase_plan_20250930
- project_taskapp_decisions
- project_taskapp_mcp_config

**Status**: ✅ Complete foundation established

### 🌊 Wave Context (30-Day Retention)
- project_taskapp_wave_1_plan
- project_taskapp_wave_1_complete
- project_taskapp_wave_2_plan
- project_taskapp_wave_2_progress

**Status**: ✅ Wave 2 in progress

### 🔄 Phase Context (30-Day Retention)
- project_taskapp_phase_requirements_complete
- project_taskapp_phase_implementation_start

**Status**: ✅ Implementation phase active

### 💾 Checkpoints (Recovery Points)
- precompact_checkpoint_20250930_143000 (2 hours ago)
- manual_checkpoint_endofday_20250929
- wave_checkpoint_wave1_20250929

**Status**: ✅ Recent checkpoint available

### 📝 Session State (7-Day Retention)
- session_20250930_active_work
- session_20250930_todo_list
- session_20250930_focus

**Status**: ✅ Active session context

### 🎯 Decisions (Indefinite Retention)
- decision_auth_jwt_20250929
- decision_database_postgresql_20250929
- decision_ui_react_20250929

**Status**: ✅ 3 architectural decisions recorded

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Latest Checkpoint Details

**Checkpoint**: precompact_checkpoint_20250930_143000
**Saved**: 2025-09-30 14:30:00 (2 hours ago)
**Type**: Automatic (PreCompact Hook)

**Project State**:
- Phase: Implementation
- Wave: 2 of 5
- Active Tasks: 3
- Completed Today: 5

**Active Work**:
- ✅ Database schema implementation
- ✅ API authentication endpoints
- 🔄 User registration flow (in progress)
- 📋 Email verification (pending)
- 📋 Password reset (pending)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Continuation Readiness

✅ **READY TO CONTINUE**

All critical context preserved:
- ✅ Specification analysis available
- ✅ Phase plan available
- ✅ Recent checkpoint (< 3 hours)
- ✅ Wave context complete
- ✅ Architectural decisions documented

**Next Steps**:
1. Resume work on user registration flow
2. Complete pending authentication tasks
3. Progress to Wave 3 after Wave 2 validation

**Commands Available**:
- `/sh:restore` - Load checkpoint if context lost
- `/sh:checkpoint` - Create new manual checkpoint
- Continue working - Context already loaded

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Status Check Complete** | 📅 2025-09-30 16:45:00
```

### Brief Output Template

```markdown
📊 PROJECT STATUS (Brief)

**Health**: ✅ HEALTHY
**Memories**: 24 total
**Checkpoint**: 2 hours ago
**Phase**: Implementation (Wave 2/5)
**Active**: 3 tasks in progress

✅ Ready to continue - Full details: /sh:status
```

### Warning States

**Missing Checkpoint**:
```markdown
📊 PROJECT STATUS

**Health**: ⚠️ CHECKPOINT MISSING
**Memories**: 18 total
**Checkpoint**: None found

⚠️ **Action Required**:
Create checkpoint before continuing: /sh:checkpoint
```

**No Project Context**:
```markdown
📊 PROJECT STATUS

**Health**: 🚨 NO PROJECT CONTEXT
**Memories**: 0 project memories found

🚨 **Action Required**:
1. Start new project: /sh:analyze-spec [specification]
2. Or restore existing: /sh:restore
```

---

## Sub-Agent Integration

### CONTEXT_GUARDIAN Role

**Specialization**: Memory inspection and health monitoring

**Responsibilities**:
1. **Memory Enumeration**: List all Serena MCP keys
2. **Categorization**: Organize by hierarchy and retention policy
3. **Validation**: Check checkpoint integrity and completeness
4. **Health Assessment**: Evaluate memory health metrics
5. **Reporting**: Generate human-readable status dashboard

**Agent Characteristics**:
```yaml
personality: Systematic, detail-oriented, protective
communication_style: Clear status reports with actionable insights
focus_areas:
  - Memory health monitoring
  - Checkpoint validation
  - Context preservation
  - Recovery readiness
strengths:
  - Comprehensive memory inspection
  - Health metric calculation
  - Status visualization
  - Recovery guidance
```

---

## Integration with Shannon Commands

### Related Commands

**Before /sh:status**:
- `/sh:analyze-spec` - Creates project foundation
- `/sh:checkpoint` - Creates checkpoint to inspect

**After /sh:status**:
- `/sh:restore` - If checkpoint issues found
- `/sh:checkpoint` - If no recent checkpoint
- `/sh:cleanup-context` - If too many old memories

### Workflow Integration

```bash
# Morning workflow
/sh:status                    # Check project state
/sh:restore                   # If needed
Continue work                 # Context ready

# End of day workflow
/sh:status                    # Review progress
/sh:checkpoint endofday       # Save state
Exit session                  # Safe to leave

# After auto-compact
Session starts                # New conversation
/sh:status                    # Assess recovery
/sh:restore                   # Load checkpoint
Continue work                 # Context restored
```

---

## Examples

### Example 1: Healthy Project

**Input**:
```bash
/sh:status
```

**Output**:
```markdown
📊 PROJECT STATUS DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Overall Status
**Health**: ✅ HEALTHY
**Total Memories**: 24
**Last Checkpoint**: precompact_checkpoint_20250930_143000 (2h ago)
**Project**: project_taskapp

[Full dashboard output...]

✅ **READY TO CONTINUE** - All critical context preserved
```

### Example 2: Missing Checkpoint

**Input**:
```bash
/sh:status
```

**Output**:
```markdown
📊 PROJECT STATUS DASHBOARD

## Overall Status
**Health**: ⚠️ CHECKPOINT MISSING
**Total Memories**: 18
**Last Checkpoint**: None found

[Memory breakdown...]

⚠️ **Action Required**: Create checkpoint before continuing
Run: /sh:checkpoint
```

### Example 3: Fresh Session

**Input**:
```bash
/sh:status
```

**Output**:
```markdown
📊 PROJECT STATUS

**Health**: 🚨 NO PROJECT CONTEXT
**Memories**: No project memories found

🚨 **Action Required**:
1. Start new project: /sh:analyze-spec [specification]
2. Or restore existing: /sh:restore [checkpoint_name]
```

---

## Technical Implementation

### Memory Query Optimization

```python
# Efficient memory listing
def get_categorized_memories():
    """
    Efficiently categorize all memories in single pass
    """
    all_keys = list_memories()

    categories = {
        'project_foundation': [],
        'wave_context': [],
        'phase_context': [],
        'session_state': [],
        'checkpoints': [],
        'decisions': []
    }

    # Single-pass categorization
    for key in all_keys:
        if 'checkpoint' in key:
            categories['checkpoints'].append(key)
        elif key.startswith('project_') and any(x in key for x in ['spec', 'plan', 'decisions', 'final']):
            categories['project_foundation'].append(key)
        elif 'wave_' in key:
            categories['wave_context'].append(key)
        elif 'phase_' in key:
            categories['phase_context'].append(key)
        elif 'session_' in key:
            categories['session_state'].append(key)
        elif 'decision_' in key:
            categories['decisions'].append(key)

    return categories
```

### Checkpoint Validation

```python
def validate_checkpoint(checkpoint_data):
    """
    Validate checkpoint contains required fields
    """
    required_fields = ['timestamp', 'project_id', 'state']

    for field in required_fields:
        if field not in checkpoint_data:
            return False, f"Missing field: {field}"

    # Check state completeness
    if 'active_phase' not in checkpoint_data['state']:
        return False, "Missing phase information"

    return True, "Valid checkpoint"
```

---

## Success Criteria

**Command succeeds when**:
- ✅ All Serena memory keys enumerated
- ✅ Memories categorized by hierarchy level
- ✅ Latest checkpoint identified and validated
- ✅ Health status accurately determined
- ✅ Dashboard generated with actionable insights
- ✅ User understands project state clearly
- ✅ Continuation readiness communicated

**Command fails if**:
- ❌ Cannot connect to Serena MCP
- ❌ list_memories() returns error
- ❌ Dashboard generation incomplete

---

## Summary

`/sh:status` provides comprehensive visibility into project state through Serena MCP memory inspection, enabling users to:

- **Assess Health**: Understand memory health and checkpoint status
- **Track Progress**: See active work and completed tasks
- **Plan Continuation**: Know exactly how to resume work
- **Identify Issues**: Detect missing checkpoints or context gaps
- **Make Decisions**: Determine if checkpoint or restoration needed

**Key Principle**: Transparency into project state enables confident continuation and recovery.