---
name: sh:wave
command: /sh:wave
description: Initiate wave-based planning and execution with memory coordination
category: command
sub_agents: [WAVE_ORCHESTRATOR]
mcp_servers: [serena, sequential, context7]
version: 3.0
---

# /sh:wave - Wave-Based Planning and Execution

## Purpose

Execute complex tasks through wave-based orchestration, combining strategic planning, memory coordination, and adaptive execution patterns to achieve goals efficiently.

**Core Objective**: Decompose complex requests into coordinated wave phases with automatic memory tracking, checkpointing, and North Star alignment.

---

## Command Metadata

```yaml
command: /sh:wave
aliases: [shannon:plan, shannon:waves]
category: Planning & Execution
sub_agent: WAVE_ORCHESTRATOR
mcp_servers:
  primary: Serena
  secondary: Sequential
  tertiary: Context7
tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Grep
  - Glob
  - TodoWrite
  - Task
  - mcp__memory__create_entities
  - mcp__memory__create_relations
  - mcp__memory__search_nodes
  - mcp__memory__read_graph
outputs:
  - Wave execution plan
  - Phase-by-phase progress
  - Memory graph evolution
  - Checkpoints at boundaries
  - Final execution report
```

---

## Usage Patterns

### Basic Usage
```bash
# Adaptive strategy (auto-selected)
/sh:wave Build authentication system

# Specific strategy
/sh:wave linear Implement API endpoints
/sh:wave parallel Build full-stack feature
/sh:wave iterative Optimize performance
```

### Context-Aware Usage
```bash
# Complex implementation
User: "Build a complete authentication system with JWT, OAuth, and 2FA"
Response: /sh:wave adaptive [full request]
→ WAVE_ORCHESTRATOR analyzes complexity
→ Selects adaptive strategy
→ Decomposes into discovery → design → implementation → validation

# Performance optimization
User: "The app is slow, need to optimize"
Response: /sh:wave iterative Optimize application performance
→ Iteration 1: Identify bottlenecks
→ Iteration 2: Apply optimizations
→ Iteration 3: Validate improvements

# Multi-track development
User: "Implement user dashboard with backend API"
Response: /sh:wave parallel Build user dashboard feature
→ Track 1: Frontend UI components
→ Track 2: Backend API endpoints
→ Sync: Integration testing
```

---

## Execution Flow

### Step 1: Activate WAVE_ORCHESTRATOR

**Sub-Agent Activation**:
```python
# Activate specialized wave coordination agent
activate_agent("WAVE_ORCHESTRATOR")

# Agent characteristics:
# - Strategic planner for complex tasks
# - Adaptive strategy selector
# - Phase coordinator and checkpoint manager
# - Memory evolution tracker
```

### Step 2: Check North Star Goal

**Goal Alignment**:
```python
# STEP 1: Query for active North Star goal
try:
    north_star = read_memory("north_star_goal")
    has_goal = True
except:
    north_star = None
    has_goal = False

# STEP 2: Align wave with goal
if has_goal:
    alignment_score = calculate_alignment(request, north_star)
    if alignment_score < 0.3:
        warn_user("Wave request may not align with North Star goal")
```

### Step 3: Load Strategy Template

**Strategy Selection Logic**:
```python
# STEP 1: Determine strategy (user-specified or auto-select)
if strategy_specified:
    wave_strategy = user_strategy
else:
    # Auto-select based on request analysis
    complexity = analyze_complexity(request)
    dependencies = identify_dependencies(request)
    
    if has_clear_sequence(request):
        wave_strategy = "linear"
    elif has_parallel_tracks(request):
        wave_strategy = "parallel"
    elif is_optimization_task(request):
        wave_strategy = "iterative"
    else:
        wave_strategy = "adaptive"

# STEP 2: Load strategy template from Context7
strategy_template = context7.get_pattern(f"wave_strategy_{wave_strategy}")
```

### Step 4: Query Serena Memory

**Context Loading**:
```python
# STEP 1: Search for related entities
related_entities = search_nodes(query=request_keywords)

# STEP 2: Load relevant context
for entity in related_entities:
    entity_data = open_nodes(names=[entity.name])
    context.add(entity_data)

# STEP 3: Identify memory gaps
gaps = identify_context_gaps(request, context)
if gaps:
    log_gaps_for_discovery_phase(gaps)
```

### Step 5: Decompose Into Wave Phases

**Phase Planning**:
```python
# Strategy-specific phase decomposition
if wave_strategy == "linear":
    phases = ["analysis", "design", "implementation", "validation"]
elif wave_strategy == "parallel":
    phases = identify_parallel_tracks(request)
elif wave_strategy == "iterative":
    phases = ["iteration_1", "iteration_2", "iteration_3"]
elif wave_strategy == "adaptive":
    phases = ["discovery"]  # More phases added dynamically
    
# Create memory entities for tracking
for phase in phases:
    create_entities(entities=[{
        "name": f"wave_{session_id}_phase_{phase}",
        "entityType": "WavePhase",
        "observations": [f"Phase: {phase}", f"Status: pending"]
    }])
```

### Step 6: Initialize TodoWrite Tracking

**Task Tracking Setup**:
```python
# Create todo items for each phase
todo_items = []
for phase in phases:
    todo_items.append({
        "content": f"Complete {phase} phase",
        "activeForm": f"Executing {phase} phase",
        "status": "pending"
    })

# Initialize TodoWrite
TodoWrite(todos=todo_items)
```

### Step 7: Execute Wave with Checkpoints

**Wave Execution**:
```python
# Execute each phase
for phase in phases:
    # Mark phase as in_progress
    update_todo_status(phase, "in_progress")
    
    # Execute phase logic
    phase_result = execute_phase(phase, strategy_template)
    
    # Create checkpoint at phase boundary
    create_checkpoint(phase_id=phase, state=current_state)
    
    # Update memory with phase completion
    add_observations(
        entityName=f"wave_{session_id}_phase_{phase}",
        contents=[f"Completed: {timestamp}", f"Result: {phase_result}"]
    )
    
    # Mark phase complete
    update_todo_status(phase, "completed")
```

### Step 8: Update Memory with Outcomes

**Final Memory Update**:
```python
# Create wave summary entity
create_entities(entities=[{
    "name": f"wave_{session_id}_complete",
    "entityType": "WaveCompletion",
    "observations": [
        f"Strategy: {wave_strategy}",
        f"Phases completed: {len(phases)}",
        f"Duration: {total_time}",
        f"Goal alignment: {final_alignment_score}"
    ]
}])

# Create relationships
create_relations(relations=[{
    "from": f"wave_{session_id}_complete",
    "to": "north_star_goal",
    "relationType": "achieved"
}])

# Generate execution report
generate_wave_report()
```

---

## Wave Strategies

### Linear Strategy
**When to Use**: Clear sequential dependencies, well-defined requirements

**Phases**:
1. Analysis - Understand requirements and context
2. Design - Plan architecture and approach
3. Implementation - Build the solution
4. Validation - Test and verify

**Checkpoints**: After each phase

**Example Output**:
```markdown
🌊 WAVE EXECUTION: Linear Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Build authentication system
🎯 North Star: Secure, scalable auth implementation
📊 Strategy: Linear (4 phases)

Phase 1/4: Analysis ✅ Complete (5 min)
→ Requirements gathered
→ Security requirements identified
→ Checkpoint: cp_phase1_abc123

Phase 2/4: Design ✅ Complete (8 min)  
→ JWT architecture designed
→ Database schema created
→ Checkpoint: cp_phase2_def456

Phase 3/4: Implementation 🔄 In Progress (15 min)
→ Auth endpoints: 70% complete
→ Token management: Done
→ Next: OAuth integration

Phase 4/4: Validation ⏳ Pending
```

### Parallel Strategy
**When to Use**: Independent work streams, multi-domain tasks

**Tracks**:
- Frontend
- Backend
- Infrastructure

**Sync Points**: Design, Implementation, Integration

**Example Output**:
```markdown
🌊 WAVE EXECUTION: Parallel Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Build user dashboard feature
🎯 North Star: Complete dashboard implementation
📊 Strategy: Parallel (3 tracks)

Track 1: Frontend ✅ Complete
→ React components built
→ State management implemented
→ UI responsive and accessible

Track 2: Backend 🔄 In Progress
→ API endpoints: 80% complete
→ Data aggregation done
→ Next: Performance optimization

Track 3: Infrastructure ⏳ Pending
→ Waiting for Track 2 completion

Sync Point: Integration Testing ⏳ Scheduled
```

### Iterative Strategy  
**When to Use**: Optimization tasks, refinement work, progressive enhancement

**Iterations**:
1. Functionality - Get it working
2. Performance - Make it fast
3. Polish - Perfect the details

**Example Output**:
```markdown
🌊 WAVE EXECUTION: Iterative Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Optimize application performance
🎯 North Star: 10x performance improvement
📊 Strategy: Iterative (3 cycles)

Iteration 1: Functionality ✅ Complete
→ Baseline established: 2.5s load time
→ Bottlenecks identified: DB queries, rendering
→ Improvement: 2.5s → 1.8s (28%)

Iteration 2: Performance 🔄 In Progress
→ Query optimization: Done
→ Caching implemented: Done  
→ Current: 1.8s → 0.9s (50% total)
→ Next: Code splitting

Iteration 3: Polish ⏳ Pending
→ Target: < 0.5s load time
```

### Adaptive Strategy
**When to Use**: Uncertain requirements, exploratory work, complex unknowns

**Dynamic Phases**: Discovered during execution

**Example Output**:
```markdown
🌊 WAVE EXECUTION: Adaptive Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Research and implement authentication solution
🎯 North Star: Optimal auth system
📊 Strategy: Adaptive (dynamic phases)

Phase 1: Discovery ✅ Complete
→ Evaluated: JWT, OAuth, Session-based
→ Decision: JWT + OAuth for social login
→ New phases identified: 4 additional

Phase 2: JWT Implementation 🔄 In Progress
→ Core JWT logic: Done
→ Token refresh: In progress
→ Discovered requirement: Rate limiting

Phase 3: OAuth Integration ⏳ Added (discovered)

Phase 4: Rate Limiting ⏳ Added (discovered)

Phase 5: Integration Testing ⏳ Planned
```

---

## Sub-Agent Integration

### WAVE_ORCHESTRATOR Role

**Specialization**: Strategic wave planning and execution coordination

**Responsibilities**:
1. **Strategy Selection**: Choose optimal wave approach
2. **Phase Decomposition**: Break complex tasks into manageable phases
3. **Memory Coordination**: Track context evolution across phases
4. **Checkpoint Management**: Create recovery points at boundaries
5. **Progress Monitoring**: Track and report wave execution
6. **Goal Alignment**: Ensure all phases support North Star

**Agent Characteristics**:
```yaml
personality: Strategic, adaptive, systematic
communication_style: Clear phase updates with progress metrics
focus_areas:
  - Complex task orchestration
  - Multi-phase coordination
  - Memory-driven planning
  - Adaptive strategy selection
strengths:
  - Pattern recognition for strategy selection
  - Phase dependency management
  - Checkpoint timing optimization
  - Progress visualization
```

---

## Integration with Shannon Commands

### Related Commands

**Before /sh:wave**:
- `/sh:north-star` - Set guiding goal
- `/sh:status` - Check system readiness

**During /sh:wave**:
- `/sh:checkpoint` - Manual checkpoint creation
- `/sh:memory track` - Monitor memory evolution
- `/sh:status wave` - Check wave progress

**After /sh:wave**:
- `/sh:memory pattern` - Analyze wave patterns
- `/sh:checkpoint list` - Review wave checkpoints

### Workflow Integration

```bash
# Complete wave workflow
/sh:north-star "Build scalable auth system"
/sh:wave adaptive Research and implement auth
# [Wave executes with automatic checkpoints]
/sh:memory pattern  # Analyze what was learned
/sh:status         # Verify completion
```

---

## Examples

### Example 1: Linear Wave

**Input**:
```bash
/sh:wave linear Build user registration API
```

**Output**:
```markdown
🌊 WAVE STARTED: Linear Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Build user registration API
🎯 North Star: Complete user management system  
📊 Strategy: Linear
⏱️  Estimated: 25-35 minutes

📅 PHASE PLAN:
1. Analysis (5-7 min) - Requirements and data model
2. Design (6-8 min) - API structure and validation
3. Implementation (10-15 min) - Code and tests
4. Validation (4-5 min) - Integration testing

🚀 Starting Phase 1: Analysis...

[Execution proceeds with checkpoints after each phase]
```

### Example 2: Parallel Wave

**Input**:
```bash
/sh:wave parallel Implement dashboard with analytics
```

**Output**:
```markdown
🌊 WAVE STARTED: Parallel Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Implement dashboard with analytics
🎯 North Star: User analytics dashboard
📊 Strategy: Parallel (3 tracks)

🔀 PARALLEL TRACKS:
Track 1 (Frontend): React dashboard UI
Track 2 (Backend): Analytics API + data aggregation  
Track 3 (Infrastructure): Metrics collection setup

🔗 SYNC POINTS:
- Design Review: After initial planning
- Integration: When tracks 1 & 2 complete
- Final Validation: All tracks complete

🚀 Starting all tracks in parallel...

[Tracks execute concurrently with coordination]
```

### Example 3: Iterative Wave

**Input**:
```bash
/sh:wave iterative Polish user experience
```

**Output**:
```markdown
🌊 WAVE STARTED: Iterative Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request: Polish user experience
🎯 North Star: Delightful user experience
📊 Strategy: Iterative (3 cycles)

🔄 ITERATION PLAN:
Cycle 1: Functionality - Ensure everything works
Cycle 2: Performance - Make it fast and smooth
Cycle 3: Polish - Perfect the details

🎯 Success Criteria:
- Load time < 1s
- Smooth interactions (60fps)
- Accessible (WCAG AA)
- Delightful micro-interactions

🚀 Starting Iteration 1: Functionality...

[Cycles execute with progressive refinement]
```

---

## Technical Implementation

### Strategy Selection Algorithm

```python
def select_wave_strategy(request: str, context: dict) -> str:
    """
    Intelligently select wave strategy based on request analysis
    """
    # Analyze request characteristics
    has_sequence = detect_sequential_dependencies(request)
    has_parallel = detect_parallel_opportunities(request)
    is_optimization = detect_optimization_keywords(request)
    is_exploratory = detect_uncertainty(request)
    
    # Decision logic
    if has_sequence and not has_parallel:
        return "linear"
    elif has_parallel:
        return "parallel"
    elif is_optimization:
        return "iterative"
    elif is_exploratory:
        return "adaptive"
    else:
        # Default to adaptive for complex cases
        return "adaptive"
```

### Phase Decomposition

```python
def decompose_into_phases(request: str, strategy: str) -> list:
    """
    Break request into executable phases based on strategy
    """
    if strategy == "linear":
        return [
            {"name": "analysis", "focus": "requirements"},
            {"name": "design", "focus": "architecture"},
            {"name": "implementation", "focus": "code"},
            {"name": "validation", "focus": "testing"}
        ]
    
    elif strategy == "parallel":
        tracks = identify_parallel_tracks(request)
        sync_points = identify_sync_needs(tracks)
        return create_parallel_plan(tracks, sync_points)
    
    elif strategy == "iterative":
        return [
            {"name": "iteration_1", "focus": "functionality"},
            {"name": "iteration_2", "focus": "performance"},
            {"name": "iteration_3", "focus": "polish"}
        ]
    
    elif strategy == "adaptive":
        # Start with discovery, add phases dynamically
        return [{"name": "discovery", "focus": "exploration"}]
```

### Memory Coordination

```python
def track_wave_in_memory(wave_id: str, phases: list):
    """
    Create memory entities for wave tracking
    """
    # Create wave entity
    create_entities(entities=[{
        "name": f"wave_{wave_id}",
        "entityType": "WaveExecution",
        "observations": [
            f"Strategy: {strategy}",
            f"Start: {timestamp}",
            f"Phases: {len(phases)}"
        ]
    }])
    
    # Create phase entities and relationships
    for phase in phases:
        create_entities(entities=[{
            "name": f"wave_{wave_id}_phase_{phase['name']}",
            "entityType": "WavePhase",
            "observations": [
                f"Focus: {phase['focus']}",
                f"Status: pending"
            ]
        }])
        
        create_relations(relations=[{
            "from": f"wave_{wave_id}",
            "to": f"wave_{wave_id}_phase_{phase['name']}",
            "relationType": "contains"
        }])
```

---

## Success Criteria

**Wave execution succeeds when**:
- ✅ Strategy appropriately selected for request type
- ✅ All phases completed or explicitly stopped
- ✅ Checkpoints created at phase boundaries
- ✅ Memory graph updated with wave progress
- ✅ North Star alignment maintained (>0.7)
- ✅ TodoWrite reflects accurate progress
- ✅ Final execution report generated

**Wave execution fails if**:
- ❌ Strategy selection inappropriate for task
- ❌ Phase dependencies not respected
- ❌ Checkpoints missing at critical boundaries
- ❌ Memory coordination breaks down
- ❌ Goal alignment drops below threshold

---

## Summary

`/sh:wave` provides intelligent wave-based orchestration for complex tasks, combining:

- **Strategic Planning**: Automatic strategy selection (linear/parallel/iterative/adaptive)
- **Memory Coordination**: Track context evolution across wave phases
- **Checkpoint Management**: Recovery points at phase boundaries
- **Goal Alignment**: Continuous North Star alignment checking
- **Progress Tracking**: Real-time phase execution monitoring
- **Adaptive Execution**: Dynamic phase adjustment based on discoveries

**Key Principle**: Complex tasks achieve better outcomes through strategic wave decomposition with memory-coordinated execution.
