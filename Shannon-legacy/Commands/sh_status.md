---
name: sh:status
command: /sh:status
description: Display comprehensive Shannon Framework status and session state
category: command
sub_agents: [CONTEXT_GUARDIAN]
mcp_servers: [serena]
version: 3.0
---

# /sh:status - Shannon Framework Status Dashboard

## Purpose

Display comprehensive Shannon Framework status by querying Serena MCP for stored memories and presenting organized overview of project state, active operations, and system health.

**Core Objective**: Provide instant visibility into all Shannon components with component-specific filtering for focused inspection.

---

## Command Metadata

```yaml
command: /sh:status
aliases: [shannon:info, shannon:state]
category: Monitoring
sub_agent: CONTEXT_GUARDIAN
mcp_servers:
  primary: Serena
  required: true
tools:
  - Read
  - TodoWrite
  - mcp__memory__read_graph
outputs:
  - Status dashboard (all or filtered)
  - Health metrics
  - Progress indicators
  - Alert notifications
```

---

## Usage Patterns

### Basic Usage
```bash
# Full status display
/sh:status

# Component-specific views
/sh:status wave        # Wave session details only
/sh:status memory      # Memory statistics only
/sh:status checkpoint  # Checkpoint status only
/sh:status goal        # North Star goal only
/sh:status session     # Session info only

# Brief overview
/sh:status --brief
```

### Context-Aware Usage
```bash
# Morning session start
User starts new session → /sh:status
Response: Yesterday's progress, current phase, today's priorities

# After auto-compact
Context restored → /sh:status checkpoint
Response: Checkpoint validity, memory integrity, recovery status

# Mid-development check
During wave execution → /sh:status wave
Response: Current wave progress, phase status, next checkpoint

# Memory health check
After long session → /sh:status memory
Response: Memory statistics, coordination score, optimization needs
```

---

## Status Components

### North Star Component

**Display Elements**:
```yaml
north_star_display:
  - Current goal text
  - Time since set
  - Overall alignment score
  - Recent aligned operations
  - Drift warnings
```

**Example**:
```bash
/sh:status goal

# Output:
🎯 NORTH STAR STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Goal**: Build secure authentication with <100ms response time
**Set**: 4 hours ago (2025-10-03 12:00:00)
**Alignment**: 0.85 (Good)

**Recent Operations**:
✅ JWT implementation (1.0)
✅ Rate limiting (0.95)
✅ Token optimization (0.9)
⚠️  UI enhancements (0.4 - LOW)

**Drift Warnings**: 1 operation below threshold
```

### Wave Session Component

**Display Elements**:
```yaml
wave_display:
  - Active wave type/strategy
  - Current phase
  - Progress percentage
  - Time elapsed
  - Next checkpoint timing
```

**Example**:
```bash
/sh:status wave

# Output:
🌊 WAVE SESSION STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Strategy**: Linear
**Phase**: 3/4 (Implementation)
**Progress**: [████████░░] 75%
**Elapsed**: 2h 15min
**Est. Remaining**: 45min

**Phase History**:
✅ Phase 1: Analysis (25min)
✅ Phase 2: Design (35min)
🔄 Phase 3: Implementation (1h 15min - IN PROGRESS)
⏳ Phase 4: Validation (pending)

**Next Checkpoint**: Phase 3 completion (est. 30min)
```

### Memory Component

**Display Elements**:
```yaml
memory_display:
  - Total entities and relations
  - Recent additions
  - Access patterns
  - Coordination score
  - Health status
```

**Example**:
```bash
/sh:status memory

# Output:
💾 MEMORY STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Graph Size**:
- Entities: 42
- Relations: 78
- Observations: 247
- Ratio: 1.86 relations/entity (✅ healthy)

**Recent Activity** (Last hour):
➕ Added: 3 entities, 7 relations, 15 observations
🔄 Modified: 5 entities (observations updated)

**Access Patterns**:
🔥 Hot: authentication (23 accesses)
🔥 Hot: user_service (18 accesses)
❄️  Cold: legacy_payment (1 access)

**Health Metrics**:
- Coordination: 0.78 (Good)
- Freshness: 87% recent
- Efficiency: 0.81 (Good)

**Overall**: ✅ HEALTHY
```

### Checkpoint Component

**Display Elements**:
```yaml
checkpoint_display:
  - Recent checkpoints (last 5)
  - Current checkpoint ID
  - Time since last checkpoint
  - Rollback availability
```

**Example**:
```bash
/sh:status checkpoint

# Output:
💾 CHECKPOINT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Latest**: cp_20251003_143022_a7f3
**Created**: 2 hours ago
**Type**: Auto (phase boundary)

**Recent Checkpoints**:
1. cp_20251003_143022_a7f3 (2h ago) - Phase 2 boundary
2. cp_20251003_120500_p3m1 (4h ago) - PreCompact auto
3. cp_20251002_173045_q8r7 (1d ago) - Manual save
4. cp_20251002_120000_x9k2 (2d ago) - Wave complete
5. cp_20251001_160000_m5n3 (3d ago) - Daily checkpoint

**Status**: ✅ CURRENT (< 3 hours old)
**Rollback**: Available to any checkpoint
```

### Session Component

**Display Elements**:
```yaml
session_display:
  - Session start time
  - Operations completed
  - Memory evolution
  - Goal achievement progress
```

**Example**:
```bash
/sh:status session

# Output:
⏱️  SESSION STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Start**: 2025-10-03 12:00:00 (4 hours ago)
**Duration**: 4h 15min

**Operations Completed**: 23 total
- Analysis: 5
- Implementation: 12
- Testing: 4
- Documentation: 2

**Memory Evolution**:
Start: 35 entities → Current: 42 entities (+7)
Growth: 1.75 entities/hour

**Goal Progress**:
North Star: "Build secure auth <100ms"
→ Auth core: ✅ Complete
→ Performance: 🔄 85% complete (120ms → 95ms)
→ Security: ✅ Complete

**Est. Completion**: 30-45 minutes
```

---

## Execution Flow

### Step 1: Activate CONTEXT_GUARDIAN

**Sub-Agent Activation**:
```python
# Activate status monitoring agent
activate_agent("CONTEXT_GUARDIAN")

# Agent characteristics:
# - Comprehensive status collector
# - Health metric calculator
# - Component-aware reporter
# - Alert generator
```

### Step 2: Parse Component Filter

**Filter Application**:
```python
# STEP 1: Detect component parameter
component = parse_component(command)  # all, wave, memory, checkpoint, goal, session

# STEP 2: Validate component
if component not in VALID_COMPONENTS:
    error(f"Invalid component. Use: {VALID_COMPONENTS}")
    
# STEP 3: Set display scope
if component == "all":
    components_to_display = ALL_COMPONENTS
else:
    components_to_display = [component]
```

### Step 3: Collect Component Data

**Data Gathering**:
```python
status_data = {}

for component in components_to_display:
    if component == "north_star":
        status_data["north_star"] = get_north_star_status()
    elif component == "wave":
        status_data["wave"] = get_wave_session_status()
    elif component == "memory":
        status_data["memory"] = get_memory_statistics()
    elif component == "checkpoint":
        status_data["checkpoint"] = get_checkpoint_status()
    elif component == "session":
        status_data["session"] = get_session_info()
```

### Step 4: Calculate Health Metrics

**Health Score Formula**:
```python
def calculate_health_score(status_data: dict) -> float:
    """
    Overall Shannon Framework health score
    
    Formula:
    (goal_alignment × 0.3) +
    (memory_coordination × 0.3) +
    (checkpoint_frequency × 0.2) +
    (wave_progress × 0.2)
    
    Range: 0.0 to 1.0
    - Healthy: >= 0.7
    - Warning: 0.4 - 0.7
    - Critical: < 0.4
    """
    goal_alignment = status_data["north_star"]["alignment"]
    memory_coord = status_data["memory"]["coordination_score"]
    
    # Checkpoint frequency (1.0 if < 30min, decays to 0.0 at 3h)
    checkpoint_age_min = status_data["checkpoint"]["age_minutes"]
    checkpoint_freq = max(0, 1.0 - (checkpoint_age_min / 180))
    
    # Wave progress (0-1 based on phase completion)
    wave_progress = status_data["wave"]["progress_percentage"] / 100
    
    health = (
        goal_alignment * 0.3 +
        memory_coord * 0.3 +
        checkpoint_freq * 0.2 +
        wave_progress * 0.2
    )
    
    return round(health, 2)
```

### Step 5: Generate Dashboard

**Output Assembly**:
```python
# Build status dashboard
dashboard = generate_status_dashboard(
    status_data,
    health_score,
    component_filter
)

# Add visual elements
add_progress_bars(dashboard)
add_status_indicators(dashboard)
add_alerts(dashboard)

# Display
display(dashboard)
```

---

## Output Formats

### Full Dashboard (Default)

```markdown
📊 SHANNON FRAMEWORK STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Overall Health
**Score**: 0.85 🟢 HEALTHY
**Components**: All operational
**Last Update**: Just now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 North Star Goal
**Goal**: Build secure authentication <100ms
**Alignment**: [█████████░] 0.85
**Status**: ✅ On track

## 🌊 Wave Session
**Strategy**: Linear (Phase 3/4)
**Progress**: [████████░░] 75%
**Time**: 2h 15min elapsed

## 💾 Memory
**Entities**: 42 | **Relations**: 78
**Coordination**: [████████░░] 0.78
**Health**: ✅ Healthy

## 💾 Checkpoints
**Latest**: cp_a7f3 (2h ago)
**Status**: ✅ Current
**Rollback**: Available

## ⏱️  Session
**Duration**: 4h 15min
**Operations**: 23 completed
**Est. Completion**: 30-45min

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Status**: ✅ ALL SYSTEMS OPERATIONAL
```

### Component-Specific Views

(Examples shown in individual component sections above)

---

## Alert System

### Alert Conditions

```yaml
alerts:
  critical:
    - memory_coordination < 0.5
    - no_checkpoint_in_3_hours
    - goal_alignment < 0.3
    - wave_stalled_15_min
  
  warning:
    - memory_coordination < 0.7
    - no_checkpoint_in_30_min
    - goal_alignment < 0.5
    - wave_progress_slow
  
  info:
    - new_checkpoint_created
    - goal_updated
    - wave_phase_complete
```

### Alert Display

```markdown
🚨 ALERTS (2 Active)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  WARNING: No checkpoint in 45 minutes
→ Action: Run /sh:checkpoint to create recovery point

⚠️  WARNING: Memory coordination: 0.62 (below 0.7 target)
→ Action: Run /sh:memory optimize for recommendations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Sub-Agent Integration

### CONTEXT_GUARDIAN Role

**Specialization**: Comprehensive status monitoring and health assessment

**Responsibilities**:
1. **Status Collection**: Gather data from all Shannon components
2. **Health Calculation**: Compute system health metrics
3. **Alert Generation**: Identify issues requiring attention
4. **Visualization**: Create clear status dashboards
5. **Guidance**: Recommend corrective actions

**Agent Characteristics**:
```yaml
personality: Vigilant, systematic, health-focused
communication_style: Clear dashboards with actionable alerts
focus_areas:
  - System health monitoring
  - Component status tracking
  - Alert management
  - Recovery guidance
strengths:
  - Comprehensive data collection
  - Metric calculation
  - Dashboard visualization
  - Proactive alerting
```

---

## Integration with Shannon Commands

### Related Commands

**Status Providers**:
- `/sh:wave` - Contributes wave session data
- `/sh:north-star` - Provides goal information
- `/sh:memory` - Supplies memory statistics
- `/sh:checkpoint` - Reports checkpoint state

**Status Consumers**:
- User - Makes informed decisions
- Other commands - Adapt based on status

### Workflow Integration

```bash
# Daily workflow
/sh:status                     # Morning health check
# [Work throughout day]
/sh:status wave                # Check wave progress
# [Continue work]
/sh:status checkpoint          # Verify checkpoint recency
/sh:checkpoint                 # Create if needed
```

---

## Technical Implementation

### Health Score Calculation

```python
def calculate_health_score(components: dict) -> dict:
    """
    Calculate overall Shannon Framework health
    """
    # Component scores
    goal_score = components["north_star"]["alignment"]
    memory_score = components["memory"]["coordination"]
    checkpoint_score = calculate_checkpoint_freshness(
        components["checkpoint"]["age_minutes"]
    )
    wave_score = components["wave"]["progress"] / 100
    
    # Weighted combination
    health = (
        goal_score * 0.3 +
        memory_score * 0.3 +
        checkpoint_score * 0.2 +
        wave_score * 0.2
    )
    
    # Determine status
    if health >= 0.7:
        status = "HEALTHY"
        indicator = "🟢"
    elif health >= 0.4:
        status = "WARNING"
        indicator = "🟡"
    else:
        status = "CRITICAL"
        indicator = "🔴"
    
    return {
        "score": round(health, 2),
        "status": status,
        "indicator": indicator
    }
```

### Alert Detection

```python
def detect_alerts(components: dict) -> list:
    """
    Identify conditions requiring user attention
    """
    alerts = []
    
    # Memory coordination check
    if components["memory"]["coordination"] < 0.5:
        alerts.append({
            "level": "CRITICAL",
            "message": f"Memory coordination: {components['memory']['coordination']}",
            "action": "/sh:memory optimize"
        })
    elif components["memory"]["coordination"] < 0.7:
        alerts.append({
            "level": "WARNING",
            "message": f"Memory coordination: {components['memory']['coordination']}",
            "action": "/sh:memory pattern"
        })
    
    # Checkpoint freshness check
    age_min = components["checkpoint"]["age_minutes"]
    if age_min > 180:
        alerts.append({
            "level": "CRITICAL",
            "message": f"No checkpoint in {age_min} minutes",
            "action": "/sh:checkpoint"
        })
    elif age_min > 30:
        alerts.append({
            "level": "WARNING",
            "message": f"Checkpoint age: {age_min} minutes",
            "action": "/sh:checkpoint recommended"
        })
    
    # Goal alignment check
    if components["north_star"]["alignment"] < 0.3:
        alerts.append({
            "level": "CRITICAL",
            "message": "Severe goal misalignment",
            "action": "Review North Star or current work"
        })
    
    return alerts
```

---

## Success Criteria

**Status display succeeds when**:
- ✅ All requested components displayed accurately
- ✅ Health metrics calculated correctly
- ✅ Alerts identified and prioritized
- ✅ Visual elements clear and helpful
- ✅ Actionable guidance provided
- ✅ User understands system state completely

**Status display fails if**:
- ❌ Missing component data
- ❌ Incorrect health calculations
- ❌ Alerts missed or wrong priority
- ❌ Visual elements confusing
- ❌ No actionable guidance

---

## Summary

`/sh:status` provides comprehensive system visibility through:

- **Full Dashboard**: All components in single view
- **Component Filters**: Focused views (wave, memory, checkpoint, goal, session)
- **Health Metrics**: System-wide health scoring
- **Alert System**: Proactive issue detection
- **Actionable Guidance**: Clear next steps

**Key Principle**: Complete transparency into system state enables informed decisions and proactive issue resolution.
