# Shannon Commands - Complete Reference

> **Comprehensive command syntax, parameters, flags, and technical specifications for all Shannon Framework commands**

---

## Quick Command Reference

| Command | Syntax | Primary Use | Key Parameters |
|---------|--------|-------------|----------------|
| `/sh:north-sta I took a look at all the various frames inside of the transition zero path that you're looking at. And based on my findings, Yes, so the DURING looks perfect. That absolutely means this is happening. If I look at frame 174 and that, no, that is still a DURING. Basically 180, which is stable, that would be the start of the SHORT 1. That's perfect. And basically 150 though, basically 150 is the old current SHORT, meaning you are still stable. That is before transition is really what that is, right? Frame 150 is what it's looking at. And then basically 164 at transition, yes.r` | `/sh:north-star ["goal"]` | Goal management | Actions: get, check, history |
| `/sh:wave` | `/sh:wave [strategy] [request]` | Wave orchestration | Strategies: linear, parallel, iterative, adaptive |
| `/sh:analyze` | `/sh:analyze [target] [depth]` | Multi-layer analysis | Depths: surface, structural, comprehensive, exhaustive |
| `/sh:checkpoint` | `/sh:checkpoint [action] [id]` | State management | Actions: create, load, list, compare, rollback |
| `/sh:memory` | `/sh:memory [action] [entity]` | Memory intelligence | Actions: track, pattern, visualize, optimize, stats |
| `/sh:status` | `/sh:status [component]` | System monitoring | Components: all, wave, memory, checkpoint, goal, session |

---

## Complete Command Specifications

## 1. /sh:north-star - Goal Management

### Full Syntax
```bash
# Set goal (implicit action)
/sh:north-star "goal statement"

# Get current goal
/sh:north-star
/sh:north-star get

# Check operation alignment
/sh:north-star check "operation description"

# View goal history
/sh:north-star history
```

### Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `goal` | string | No | Goal statement to set | `"Build JWT auth <100ms"` |
| `action` | enum | No | Action to perform | `get`, `check`, `history` |
| `operation` | string | Conditional | Operation to check (with `check`) | `"Add password reset"` |

### Actions

**SET** (implicit when providing goal string):
- **Input**: Goal statement in quotes
- **Output**: Goal quality assessment, alignment setup
- **Technical Result**: Creates `north_star_goal` entity in Serena with quality score

**GET** (default when no parameters):
- **Input**: None
- **Output**: Current goal, set time, alignment metrics, recent operations
- **Technical Result**: Queries Serena for goal entity and alignment history

**CHECK** (alignment verification):
- **Input**: Operation description
- **Output**: Alignment score (0-1), recommendation, rationale
- **Technical Result**: Semantic similarity calculation, threshold-based decision

**HISTORY** (goal evolution):
- **Input**: None
- **Output**: Current + previous goals with timestamps, change rationale
- **Technical Result**: Queries goal change history from Serena

### Alignment Scoring

```yaml
direct_alignment: 1.0
  description: "Core functionality for goal"
  example: "Add JWT validation" for "Build JWT auth" = 1.0

partial_alignment: 0.5-0.9
  description: "Supports goal but not core"
  example: "Add password strength meter" = 0.7

indirect_support: 0.2-0.5
  description: "Tangentially related"
  example: "Improve UI animations" = 0.3

misalignment: <0.2
  description: "Scope creep, unrelated"
  example: "Add payment processing" = 0.1

thresholds:
  proceed_strong: ">= 0.8"
  proceed_caution: "0.5 - 0.8"
  reconsider: "< 0.5"
```

### Technical Results

**Memory State Changes**:
```yaml
before_set:
  entities: []

after_set:
  entities:
    - north_star_goal:
        type: Goal
        observations:
          - "Build production-ready JWT authentication with <100ms token validation"
          - "Set: 2025-10-07 12:00:00"
          - "Quality score: 0.95"
```

**Example Output**:
```markdown
🎯 NORTH STAR GOAL SET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Goal**: Build production-ready JWT authentication with <100ms token validation

**Quality Assessment**:
✅ Clear and specific (JWT authentication defined)
✅ Measurable (<100ms performance target)
⚠️  Time-bounded (no explicit deadline - acceptable)
✅ Achievable (realistic technical goal)
✅ Aligned (matches user intent)

**Overall Quality**: 🟢 HIGH (4/5 criteria strong)

💾 Saved to: Serena memory + ~/.claude/shannon/north_star.txt
```

---

## 2. /sh:wave - Wave Orchestration

### Full Syntax
```bash
# Auto-select strategy (adaptive)
/sh:wave [request description]

# Specific strategy
/sh:wave linear [request]
/sh:wave parallel [request]
/sh:wave iterative [request]
/sh:wave adaptive [request]
```

### Parameters

| Parameter | Type | Required | Description | Values/Example |
|-----------|------|----------|-------------|----------------|
| `strategy` | enum | No | Wave execution strategy | `linear`, `parallel`, `iterative`, `adaptive` |
| `request` | string | Yes | Task description | `"Build authentication system"` |

### Wave Strategies

**LINEAR** - Sequential phases with dependencies:
```yaml
use_when: "Clear sequential dependencies, well-defined requirements"
phases: [analysis, design, implementation, validation]
checkpoint_timing: "After each phase"
best_for: "Traditional feature development"
example: "/sh:wave linear Build API endpoints"

technical_flow:
  1. Analysis phase executes
  2. Checkpoint created: cp_phase1
  3. Design phase executes
  4. Checkpoint created: cp_phase2
  5. Implementation phase executes
  6. Checkpoint created: cp_phase3
  7. Validation phase executes
  8. Checkpoint created: cp_phase4
  9. Wave complete entity created
```

**PARALLEL** - Multi-track concurrent execution:
```yaml
use_when: "Independent work streams, multi-domain tasks"
tracks: [frontend, backend, infrastructure]
sync_points: [design, implementation, integration]
best_for: "Full-stack features, multi-component work"
example: "/sh:wave parallel Implement user dashboard"

technical_flow:
  1. Wave splits into N parallel tracks
  2. Each track creates entities independently
  3. Tracks execute concurrently
  4. Sync points coordinate integration
  5. Final merge and validation
```

**ITERATIVE** - Progressive refinement cycles:
```yaml
use_when: "Optimization, refinement, progressive enhancement"
iterations: [functionality, performance, polish]
checkpoint_timing: "After each iteration"
best_for: "Performance optimization, quality improvement"
example: "/sh:wave iterative Optimize application performance"

technical_flow:
  1. Iteration 1: Get it working (baseline metrics)
  2. Checkpoint + memory update
  3. Iteration 2: Make it fast (optimization)
  4. Checkpoint + memory update
  5. Iteration 3: Perfect details (polish)
  6. Final checkpoint + learnings captured
```

**ADAPTIVE** - Discovery-driven dynamic planning:
```yaml
use_when: "Uncertain requirements, exploratory work, research needed"
initial_phase: "discovery"
dynamic: "Phases added based on findings"
best_for: "Research, exploration, unclear scope"
example: "/sh:wave adaptive Research and implement caching strategy"

technical_flow:
  1. Discovery phase reveals options
  2. Decision point adds new phases dynamically
  3. Phases execute based on discoveries
  4. Additional phases can be added during execution
  5. Wave complete when all discovered work done
```

### Technical Results

**Memory Evolution Example** (Linear wave):
```yaml
t0_wave_start:
  entities: 1
  relations: 0

t1_after_analysis:
  entities: 5  # +4 (wave, phase, requirements entities)
  relations: 2

t2_after_design:
  entities: 9  # +4 (architecture entities)
  relations: 6  # +4

t3_after_implementation:
  entities: 23  # +14 (code entities)
  relations: 38  # +32

t4_after_validation:
  entities: 27  # +4 (test entities)
  relations: 54  # +16

coordination_score: 0.82
```

**Expected Output**:
```markdown
🌊 WAVE EXECUTION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Total Duration**: 52 minutes
**Phases Completed**: 4/4 (100%)
**Checkpoints Created**: 4
**Memory Evolution**: 4 → 23 entities

**Deliverables**:
✅ JWT token generation and validation
✅ OAuth integration (Google, GitHub)
✅ Rate limiting middleware
✅ Session management
✅ Security hardening
✅ Comprehensive test suite (87% coverage)

**Goal Alignment**: 0.94 (Excellent)
**Coordination Score**: 0.82
```

---

## 3. /sh:analyze - Multi-Layer Analysis

### Full Syntax
```bash
# Analyze current context (default: comprehensive depth)
/sh:analyze

# Analyze specific target
/sh:analyze [target]

# Specify analysis depth
/sh:analyze [target] [depth]

# Examples
/sh:analyze authentication
/sh:analyze src/ structural
/sh:analyze "user authentication flow" comprehensive
/sh:analyze performance exhaustive
```

### Parameters

| Parameter | Type | Required | Description | Values/Example |
|-----------|------|----------|-------------|----------------|
| `target` | string | No | What to analyze | `authentication`, `src/`, `"user flow"`, `current context` |
| `depth` | enum | No | Analysis depth | `surface`, `structural`, `comprehensive`, `exhaustive` |

### Analysis Depths

**SURFACE** - Quick overview:
```yaml
layers: [surface]
time_estimate: "2-5 minutes"
use_when: "Quick check, initial exploration"
provides:
  - Visible structure
  - Obvious patterns
  - Immediate issues
  - Direct relationships
```

**STRUCTURAL** - Architecture analysis:
```yaml
layers: [surface, structural]
time_estimate: "5-15 minutes"
use_when: "Understanding architecture, design review"
provides:
  - System architecture
  - Design patterns
  - Dependencies
  - Information flow
```

**COMPREHENSIVE** - Full analysis (DEFAULT):
```yaml
layers: [surface, structural, strategic]
time_estimate: "15-30 minutes"
use_when: "Most analysis tasks, default choice"
provides:
  - All structural analysis
  - Goal alignment assessment
  - Trade-offs identified
  - Long-term impact evaluation
```

**EXHAUSTIVE** - Complete investigation:
```yaml
layers: [surface, structural, strategic, memory_coordination]
time_estimate: "30-60 minutes"
use_when: "Critical decisions, complete understanding needed"
provides:
  - All comprehensive analysis
  - Memory access patterns
  - Coordination efficiency metrics
  - Optimization opportunities
```

### Analysis Layers Explained

**Layer 1: Surface Analysis**
- What: Immediately visible structure and patterns
- How: File reading, pattern recognition
- Output: Visible structure, obvious issues, direct relationships

**Layer 2: Structural Analysis**
- What: Architecture and design patterns
- How: Dependency mapping, design pattern detection
- Output: Architecture assessment, pattern usage, dependency analysis

**Layer 3: Strategic Analysis**
- What: Goal alignment and long-term impact
- How: North Star comparison, risk assessment
- Output: Alignment score, trade-offs, strategic implications

**Layer 4: Memory Coordination Analysis**
- What: How memory is constructed and used
- How: Access logging, traversal analysis
- Output: Coordination score, efficiency metrics, optimization suggestions

### Technical Results

**Memory Access Tracking**:
```json
{
  "entities_accessed": ["north_star_goal", "auth_service", "jwt_handler", "oauth_provider"],
  "access_log": [
    {"entity": "north_star_goal", "timestamp": "12:00:00", "hop": 0},
    {"entity": "auth_service", "timestamp": "12:00:02", "hop": 1},
    {"entity": "jwt_handler", "timestamp": "12:00:04", "hop": 2}
  ],
  "coordination_metrics": {
    "access_efficiency": 0.78,
    "pattern_consistency": 0.82,
    "evolution_coherence": 0.76,
    "coordination_score": 0.79
  }
}
```

**Expected Output Format**:
```markdown
🔍 DEEP ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Executive Summary
**Target**: Authentication System
**Depth**: Comprehensive
**Duration**: 12 minutes
**Coordination**: 0.78 (Good)

**Key Findings**:
1. Security architecture sound but missing rate limiting
2. Performance bottleneck in token validation
3. Strategic misalignment (score: 0.65)

## Layer 1: Surface Analysis
[Immediate observations]

## Layer 2: Structural Analysis
[Architecture and patterns]

## Layer 3: Strategic Analysis
[Goal alignment and impact]

## Recommendations
1. Add rate limiting (HIGH)
2. Optimize token validation (HIGH)
3. Improve observability (MEDIUM)
```

---

## 4. /sh:checkpoint - State Management

### Full Syntax
```bash
# Create checkpoint (default action)
/sh:checkpoint
/sh:checkpoint create [name]

# Load checkpoint
/sh:checkpoint load [checkpoint_id]

# List checkpoints
/sh:checkpoint list [--limit N]

# Compare checkpoints
/sh:checkpoint compare [id1] [id2]

# Rollback to checkpoint
/sh:checkpoint rollback [id] [--preserve-memory]
```

### Parameters

| Parameter | Type | Required | Description | Values/Example |
|-----------|------|----------|-------------|----------------|
| `action` | enum | No | Checkpoint operation | `create`, `load`, `list`, `compare`, `rollback` |
| `name` | string | No | Checkpoint name | `"before_refactoring"`, `"milestone_v2"` |
| `checkpoint_id` | string | Conditional | Checkpoint identifier | `cp_20251007_143022_a7f3` |
| `id1`, `id2` | string | For compare | Two checkpoint IDs to compare | - |
| `--preserve-memory` | flag | No | Keep memory changes during rollback | - |
| `--limit` | integer | No | Max checkpoints to list | Default: 10, Max: 50 |

### Actions Explained

**CREATE**:
```yaml
what_gets_captured:
  - Complete memory graph (all entities and relations)
  - Active and completed todos
  - Wave session state (if active)
  - North Star goal
  - Execution timeline
  - Recent decisions

storage_location: "~/.claude/shannon/checkpoints/[checkpoint_id].json"
serena_entity: "checkpoint_[id]"
auto_triggers: ["wave phase boundaries", "before auto-compact", "major decisions"]

technical_result:
  - JSON file written to disk
  - Checkpoint entity created in Serena
  - latest_checkpoint pointer updated
```

**LOAD**:
```yaml
what_gets_restored:
  - Memory graph entities and relations
  - TodoWrite state
  - Wave session context
  - North Star goal

validation:
  - Checkpoint file exists
  - JSON is valid
  - All required fields present

technical_result:
  - Current Serena state cleared
  - Checkpoint entities recreated
  - Todos restored to TodoWrite
  - Session context reestablished
```

**LIST**:
```yaml
display_format:
  - Checkpoint ID and name
  - Creation timestamp
  - Wave/phase context
  - Entity count
  - Alignment score

sorting: "Most recent first"
default_limit: 10
```

**COMPARE**:
```yaml
comparison_metrics:
  - Entity differences (added, removed, modified)
  - Relation changes
  - Todo state changes
  - Goal alignment delta
  - Time between checkpoints

output_format:
  - Side-by-side comparison
  - Delta summary
  - Impact assessment
```

**ROLLBACK**:
```yaml
safety_features:
  - Confirmation prompt (shows what will be lost)
  - Optional memory preservation
  - Consistency validation
  - Rollback verification

process:
  1. Load checkpoint data
  2. Show user impact
  3. Request confirmation
  4. Clear current state
  5. Restore checkpoint state
  6. Validate consistency

technical_result:
  - All entities created after checkpoint: DELETED
  - Checkpoint entities: RESTORED
  - Todos: RESTORED to checkpoint state
  - Wave context: RESTORED
```

### Technical Results

**Checkpoint JSON Structure**:
```json
{
  "id": "cp_20251007_143022_a7f3",
  "name": "phase_2_complete",
  "timestamp": "2025-10-07T14:30:22Z",
  "version": "3.0",

  "memory_graph": {
    "entities": [...42 entities],
    "relations": [...78 relations]
  },

  "todo_state": {
    "active": [...5 active todos],
    "completed": [...12 completed todos]
  },

  "wave_session": {
    "wave_id": "wave_20251007_120000",
    "strategy": "linear",
    "current_phase": 2,
    "total_phases": 4
  },

  "north_star": {
    "goal": "Build secure authentication <100ms",
    "alignment_score": 0.87
  }
}
```

---

## 5. /sh:memory - Memory Intelligence

### Full Syntax
```bash
# Track entity evolution
/sh:memory track [entity_name]

# Analyze all patterns
/sh:memory pattern

# Visualize memory graph
/sh:memory visualize

# Get optimization suggestions
/sh:memory optimize

# Show statistics
/sh:memory stats
```

### Parameters

| Parameter | Type | Required | Description | Values/Example |
|-----------|------|----------|-------------|----------------|
| `action` | enum | Yes | Memory operation | `track`, `pattern`, `visualize`, `optimize`, `stats` |
| `entity` | string | Conditional | Entity to track (for `track`) | `authentication`, `jwt_service` |

### Actions Explained

**TRACK** - Entity Evolution:
```yaml
monitors:
  - Observation accumulation rate
  - Relationship formation patterns
  - Context building progression
  - Access frequency over time

timeline: "Shows entity history from creation to current"

output:
  - Timeline visualization
  - Observation count per period
  - Relationship additions
  - Access pattern graph
  - Health assessment

technical_result:
  - Queries Serena for entity
  - Analyzes observation timestamps
  - Calculates growth metrics
  - Generates evolution report
```

**PATTERN** - Overall Analysis:
```yaml
analyzes:
  - Entity clustering (community detection)
  - Relationship type distribution
  - Access patterns (hot/cold entities)
  - Evolution trajectories
  - Coordination effectiveness

algorithms:
  - Graph clustering (detect communities)
  - Centrality measures (identify key entities)
  - Temporal analysis (growth patterns)

output:
  - Cluster visualization
  - Distribution statistics
  - Hot/warm/cold classification
  - Health assessment

technical_result:
  coordination_score: "(access_efficiency × 0.33) + (pattern_consistency × 0.33) + (evolution_coherence × 0.34)"
  cluster_count: "Number of strongly connected components"
  pareto_compliance: "Whether 80/20 rule applies to access distribution"
```

**VISUALIZE** - Graph Visualization:
```yaml
output_formats:
  - Mermaid diagram (graph TB)
  - Access heatmap (ASCII visualization)
  - Cluster map (colored by community)

node_styling:
  hot_entities: "fill:#ff6b6b (>20 accesses)"
  warm_entities: "fill:#ffd43b (10-20 accesses)"
  cool_entities: "fill:#51cf66 (5-10 accesses)"
  cold_entities: "fill:#95a5a6 (<5 accesses)"

technical_result:
  - Queries complete memory graph from Serena
  - Calculates access statistics
  - Generates Mermaid syntax
  - Renders in markdown output
```

**OPTIMIZE** - Optimization Recommendations:
```yaml
identifies:
  - Redundant entities (duplicates)
  - Orphaned entities (no relationships)
  - Stale observations (>30 days)
  - Missing relationships (should exist)

recommendations:
  - Merge similar entities
  - Delete/archive orphans
  - Prune old observations
  - Add critical relationships

impact_prediction:
  - Coordination score delta
  - Access efficiency improvement
  - Token usage reduction

technical_result:
  - Scans graph for issues
  - Calculates impact per fix
  - Prioritizes by impact/effort
  - Generates action plan
```

**STATS** - Memory Statistics:
```yaml
metrics_reported:
  - Total entities, relations, observations
  - Growth rate (entities/day)
  - Access distribution (hot/warm/cool/cold)
  - Coordination score components
  - Health status indicators

health_indicators:
  entity_relation_ratio: "0.4-0.6 optimal"
  observation_freshness: "% within 7 days"
  pareto_distribution: "Does 80/20 rule apply?"
  evolution_consistency: "Steady vs erratic growth"

technical_result:
  overall_health: "healthy | warning | critical"
  recommendations: "Based on metric thresholds"
```

### Technical Results

**Coordination Score Calculation**:
```python
access_efficiency = unique_accesses / total_accesses  # 7/9 = 0.78
pattern_consistency = analyze_pattern_predictability()  # 0.82
evolution_coherence = analyze_evolution_logic()  # 0.76

coordination_score = (
    access_efficiency * 0.33 +
    pattern_consistency * 0.33 +
    evolution_coherence * 0.34
) = 0.79
```

**Example Output** (pattern):
```markdown
📈 MEMORY PATTERN ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Entity Clustering**:
Cluster 1: Authentication (8 entities) - Dense
Cluster 2: Database (5 entities) - Moderate
Cluster 3: UI Components (12 entities) - Sparse

**Relationship Distribution**:
- implements: 23 (32%)
- requires: 18 (25%)
- coordinates_with: 15 (21%)

**Access Patterns**:
🔥 Hot: authentication (47 accesses)
❄️  Cold: legacy_payment (1 access)

**Coordination**: 0.78 (Good)
```

---

## 6. /sh:status - System Monitoring

### Full Syntax
```bash
# Full dashboard
/sh:status
/sh:status all

# Component-specific views
/sh:status wave
/sh:status memory
/sh:status checkpoint
/sh:status goal
/sh:status session

# Brief mode
/sh:status --brief
```

### Parameters

| Parameter | Type | Required | Description | Values |
|-----------|------|----------|-------------|--------|
| `component` | enum | No | Specific component to view | `all`, `wave`, `memory`, `checkpoint`, `goal`, `session` |
| `--brief` | flag | No | Show abbreviated output | - |

### Components

**ALL** (default):
```yaml
displays:
  - Overall health score
  - North Star goal status
  - Wave session progress
  - Memory statistics
  - Checkpoint status
  - Session information
  - Active alerts

calculation:
  health_score: "(goal_alignment × 0.3) + (memory_coord × 0.3) + (checkpoint_fresh × 0.2) + (wave_progress × 0.2)"

thresholds:
  healthy: ">= 0.7"
  warning: "0.4 - 0.7"
  critical: "< 0.4"
```

**WAVE**:
```yaml
displays:
  - Strategy type
  - Current phase
  - Progress percentage
  - Time elapsed
  - Estimated remaining
  - Phase history
  - Next checkpoint timing

technical_data:
  - Wave execution state from Serena
  - TodoWrite progress tracking
  - Phase timestamps
```

**MEMORY**:
```yaml
displays:
  - Entity and relation counts
  - Recent additions
  - Access patterns summary
  - Coordination score
  - Health status

metrics:
  - Graph size
  - Growth rate
  - Access distribution
  - Coordination components
```

**CHECKPOINT**:
```yaml
displays:
  - Latest checkpoint ID and timestamp
  - Last 5 checkpoints
  - Time since last checkpoint
  - Rollback availability

alert_thresholds:
  - > 30 min: Suggest checkpoint
  - > 3 hours: Critical alert
```

**GOAL**:
```yaml
displays:
  - Current North Star goal
  - Set timestamp
  - Alignment score
  - Recent operations alignment
  - Drift warnings
```

**SESSION**:
```yaml
displays:
  - Session start time
  - Duration
  - Operations completed
  - Memory evolution
  - Goal progress
```

### Technical Results

**Health Score Calculation Example**:
```yaml
inputs:
  goal_alignment: 0.85
  memory_coordination: 0.78
  checkpoint_age_minutes: 25
  wave_progress_percent: 75

calculation:
  goal_contrib: 0.85 × 0.3 = 0.255
  memory_contrib: 0.78 × 0.3 = 0.234
  checkpoint_fresh: (1.0 - 25/180) × 0.2 = 0.172
  wave_contrib: 0.75 × 0.2 = 0.150

  total: 0.811

status: "🟢 HEALTHY (>= 0.7)"
```

**Example Output** (full dashboard):
```markdown
📊 SHANNON FRAMEWORK STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Overall Health: 0.85 🟢 HEALTHY

🎯 North Star Goal
Goal: Build JWT auth <100ms
Alignment: [█████████░] 0.85

🌊 Wave Session
Strategy: Linear (Phase 3/4)
Progress: [████████░░] 75%

💾 Memory
Entities: 42 | Relations: 78
Coordination: [████████░░] 0.78

💾 Checkpoints
Latest: cp_a7f3 (2h ago) ✅

Status: ✅ ALL SYSTEMS OPERATIONAL
```

---

## Command Integration Patterns

### Common Workflows

**Workflow 1: Feature Implementation**
```bash
# 1. Set goal
/sh:north-star "Build user authentication with JWT and OAuth"

# 2. Check readiness
/sh:status

# 3. Execute wave
/sh:wave linear Build complete authentication system

# 4. Monitor progress
/sh:status wave

# 5. Checkpoint at milestones
# (automatic at phase boundaries)

# 6. Analyze results
/sh:analyze authentication comprehensive

# 7. Review patterns
/sh:memory pattern

# 8. Final checkpoint
/sh:checkpoint create auth_complete
```

**Workflow 2: Performance Optimization**
```bash
# 1. Set performance goal
/sh:north-star "Achieve 10x performance improvement (2500ms → 250ms)"

# 2. Baseline analysis
/sh:analyze performance comprehensive

# 3. Iterative optimization
/sh:wave iterative Optimize application performance

# 4. Track optimization patterns
/sh:memory track performance_optimization

# 5. Validate results
/sh:analyze performance exhaustive

# 6. Save learnings
/sh:checkpoint create optimization_complete
```

**Workflow 3: Exploratory Development**
```bash
# 1. Set exploratory goal
/sh:north-star "Research and implement optimal caching strategy"

# 2. Adaptive wave
/sh:wave adaptive Research caching solutions for our API

# 3. Monitor discoveries
/sh:status wave  # Shows dynamically added phases

# 4. Checkpoint at decision points
/sh:checkpoint create cache_decision_redis

# 5. Review learning journey
/sh:memory pattern

# 6. Final validation
/sh:status
```

---

## File Operation Examples

### Working with Specifications

**Scenario**: Implement from spec file

```bash
# 1. Read specification
/sh:analyze @docs/auth_spec.md comprehensive

# 2. Set goal from spec
/sh:north-star "Build authentication system per auth_spec.md requirements"

# 3. Execute implementation wave
/sh:wave linear Implement authentication system from @docs/auth_spec.md

# Wave will:
# - Read spec file in analysis phase
# - Extract requirements
# - Design architecture
# - Implement code
# - Validate against spec
```

### Reading and Analyzing Files

**Directory Analysis**:
```bash
# Analyze entire directory
/sh:analyze src/ comprehensive

# Analyze specific module
/sh:analyze src/auth/ structural

# Analyze single file
/sh:analyze src/auth/jwt.ts exhaustive
```

**Multi-File Analysis**:
```bash
# Analyze authentication flow across files
/sh:analyze "authentication flow in src/auth/*.ts" comprehensive

# Wave can read multiple files
/sh:wave linear Review and refactor all authentication files in src/auth/
```

### Implementing from Documentation

**Pattern**: Read → Plan → Execute → Validate

```bash
# 1. Analyze existing documentation
/sh:analyze @README.md surface
/sh:analyze @docs/architecture.md structural

# 2. Set implementation goal
/sh:north-star "Implement feature X as specified in docs/feature_x.md"

# 3. Execute with documentation awareness
/sh:wave linear Implement feature X following docs/feature_x.md specification

# During wave execution:
# - Analysis phase: Reads docs/feature_x.md
# - Design phase: Creates architecture matching spec
# - Implementation: Builds code per specification
# - Validation: Verifies against acceptance criteria in spec
```

---

## Advanced Usage Patterns

### Checkpoint-Driven Experimentation

**Safe Refactoring**:
```bash
# 1. Create safety checkpoint
/sh:checkpoint create before_risky_refactoring

# 2. Attempt refactoring
/sh:wave linear Refactor authentication to use dependency injection

# 3. Test results
# If tests pass: Continue
# If tests fail: Rollback

/sh:checkpoint rollback before_risky_refactoring
```

### Memory-Informed Development

**Leverage Previous Work**:
```bash
# 1. Check for previous implementations
/sh:memory track authentication

# If found: "Entity auth_v1 from 6 months ago with 45 observations"

# 2. Analyze previous learnings
/sh:analyze auth_v1 comprehensive

# 3. Apply learnings to new work
/sh:wave linear Build new auth system incorporating lessons from auth_v1

# Wave will reference previous challenges and solutions
```

### Goal-Driven Alignment

**Prevent Scope Creep**:
```bash
# 1. Set clear goal
/sh:north-star "Build minimal viable product for task management"

# 2. Before adding features, check alignment
/sh:north-star check "Add calendar integration"
# Result: 0.3 alignment (LOW) → Reconsider

/sh:north-star check "Add basic task CRUD operations"
# Result: 1.0 alignment (DIRECT) → Proceed

# 3. Monitor alignment during development
/sh:status goal  # Shows alignment score
```

---

## Flags and Options Summary

### Global Flags (if implemented)

```yaml
--brief:
  commands: [/sh:status]
  effect: "Abbreviated output"
  example: "/sh:status --brief"

--verbose:
  commands: [all]
  effect: "Detailed output with technical details"
  example: "/sh:analyze auth --verbose"

--limit N:
  commands: [/sh:checkpoint list]
  effect: "Limit results to N items"
  example: "/sh:checkpoint list --limit 5"

--preserve-memory:
  commands: [/sh:checkpoint rollback]
  effect: "Keep memory changes during rollback"
  example: "/sh:checkpoint rollback cp_abc123 --preserve-memory"
```

### Strategy Flags (wave command)

```yaml
strategy_selection:
  explicit: "/sh:wave [strategy] [request]"
  auto: "/sh:wave [request]"  # Analyzes and selects

strategies:
  linear: "Sequential phases"
  parallel: "Concurrent tracks"
  iterative: "Progressive refinement"
  adaptive: "Discovery-driven"
```

### Depth Flags (analyze command)

```yaml
depth_levels:
  surface: "Quick overview (1 layer)"
  structural: "Architecture (2 layers)"
  comprehensive: "Full analysis (3 layers) - DEFAULT"
  exhaustive: "Complete (4 layers)"

syntax: "/sh:analyze [target] [depth]"
```

---

## Technical Output Specifications

### Common Output Elements

**All Commands Include**:
```yaml
execution_metadata:
  - Command name and version
  - Execution timestamp
  - Duration
  - Success/failure status
  - Sub-agent activated

serena_operations:
  - Entities created/modified
  - Relations added
  - Observations appended
  - Queries executed

performance_metrics:
  - Execution time
  - Memory operations count
  - Coordination score impact
```

### Success Indicators

```yaml
successful_execution:
  - Returns structured output
  - All required fields present
  - State consistent after execution
  - Memory graph valid
  - Checkpoints created (if applicable)

failure_indicators:
  - Error message in output
  - degradedMode: true
  - Partial results with warnings
  - Serena connection issues logged
```

---

## Error Handling and Degraded Mode

### Graceful Degradation

**When Serena MCP Unavailable**:
```yaml
fallback_behavior:
  /sh:north-star: "Uses file-based storage (~/.claude/shannon/north_star.txt)"
  /sh:wave: "Executes without memory tracking (degraded)"
  /sh:analyze: "Surface analysis only (no memory layer)"
  /sh:checkpoint: "File-only checkpoints (no Serena entity)"
  /sh:memory: "Error: requires Serena"
  /sh:status: "Shows file-based state only"

degradation_signal:
  - degradedMode: true in output
  - Warning message to user
  - Recommendation to fix Serena
```

### Error Messages

**Common Error Formats**:
```json
{
  "error": true,
  "errorMessage": "Serena MCP connection failed",
  "degradedMode": true,
  "fallbackAction": "Using cached context from 5 minutes ago",
  "recommendation": "Check Serena MCP installation: claude mcp list"
}
```

---

## Performance Characteristics

### Execution Times (Typical)

```yaml
/sh:north-star:
  set: "< 1 second"
  get: "< 1 second"
  check: "1-2 seconds"

/sh:wave:
  planning: "5-30 seconds"
  execution: "varies by task (minutes to hours)"

/sh:analyze:
  surface: "2-5 minutes"
  structural: "5-15 minutes"
  comprehensive: "15-30 minutes"
  exhaustive: "30-60 minutes"

/sh:checkpoint:
  create: "5-15 seconds"
  load: "10-30 seconds"
  list: "< 5 seconds"

/sh:memory:
  track: "3-10 seconds"
  pattern: "10-30 seconds"
  stats: "< 5 seconds"

/sh:status:
  all: "5-10 seconds"
  component: "2-5 seconds"
```

### Resource Usage

```yaml
memory_operations_per_command:
  /sh:north-star: "1-3 Serena calls"
  /sh:wave: "10-50+ Serena calls (depends on phases)"
  /sh:analyze: "5-20 Serena calls"
  /sh:checkpoint: "1 read_graph + 1 write_memory"
  /sh:memory: "1 read_graph + analysis"
  /sh:status: "1-6 Serena queries (component-dependent)"

token_usage_estimates:
  /sh:north-star: "500-1000 tokens"
  /sh:wave: "5000-50000 tokens (depends on complexity)"
  /sh:analyze: "3000-15000 tokens"
  /sh:checkpoint: "2000-10000 tokens (depends on checkpoint size)"
  /sh:memory: "2000-8000 tokens"
  /sh:status: "1000-5000 tokens"
```

---

## Best Practices

### Command Selection Guide

**When to Use Each Command**:

```yaml
start_of_session:
  1. /sh:status  # Understand current state
  2. /sh:north-star "goal"  # Set or confirm goal
  3. /sh:wave [strategy] [request]  # Execute work

during_development:
  - /sh:status wave  # Check progress
  - /sh:north-star check  # Validate alignment
  - /sh:analyze [target]  # Understand systems

before_risky_operations:
  - /sh:checkpoint create [name]  # Safety net

after_completion:
  - /sh:memory pattern  # Extract learnings
  - /sh:status  # Final health check
  - /sh:checkpoint create [milestone]  # Save state

troubleshooting:
  - /sh:status  # Identify issues
  - /sh:memory stats  # Check coordination
  - /sh:checkpoint list  # Find recovery points
```

### Command Chaining

**Effective Sequences**:

```bash
# Analysis → Planning → Execution
/sh:analyze requirements.md comprehensive && \
/sh:north-star "Build feature per requirements" && \
/sh:wave linear Implement feature

# Optimization Cycle
/sh:analyze performance exhaustive && \
/sh:wave iterative Optimize based on analysis && \
/sh:memory pattern  # Capture what worked

# Safe Experimentation
/sh:checkpoint create before_experiment && \
/sh:wave adaptive Try experimental approach && \
[if failed] /sh:checkpoint rollback before_experiment
```

---

## Troubleshooting Common Issues

### Issue: Command Not Found

**Symptom**: `/sh:wave: command not found`

**Solution**:
```bash
# 1. Verify installation
python3 setup/install.py verify

# 2. Check commands directory
ls ~/.claude/commands/sh_*.md

# 3. Reinstall if missing
python3 setup/install.py install

# 4. Restart Claude Code
```

### Issue: Low Coordination Score

**Symptom**: `/sh:memory stats` shows coordination <0.5

**Solution**:
```bash
# 1. Analyze patterns
/sh:memory pattern

# 2. Get recommendations
/sh:memory optimize

# 3. Apply optimizations as suggested

# 4. Verify improvement
/sh:memory stats  # Should show higher score
```

### Issue: Goal Misalignment

**Symptom**: `/sh:status` shows alignment <0.5

**Solution**:
```bash
# Option 1: Refocus on goal
/sh:north-star  # Review current goal
# Return to goal-aligned work

# Option 2: Update goal (if requirements changed)
/sh:north-star "Updated goal incorporating new requirements"
```

### Issue: Wave Stalled

**Symptom**: Wave progress stuck, not advancing

**Solution**:
```bash
# 1. Check current state
/sh:status wave

# 2. Review last checkpoint
/sh:checkpoint list

# 3. Rollback to last good state
/sh:checkpoint rollback cp_last_good

# 4. Try alternative strategy
/sh:wave adaptive [same request with different approach]
```

---

## Summary

Shannon commands provide an intelligent coordination system that:

1. **Maintains Strategic Focus** (/sh:north-star)
   - Prevents scope creep
   - Validates all work aligns with goals
   - Tracks goal evolution

2. **Orchestrates Complex Work** (/sh:wave)
   - 4 execution strategies
   - Automatic memory tracking
   - Phase-based checkpointing

3. **Provides Deep Understanding** (/sh:analyze)
   - 4-layer analysis framework
   - Memory coordination tracking
   - Evidence-based recommendations

4. **Enables Time-Travel** (/sh:checkpoint)
   - Complete state snapshots
   - Instant rollback capability
   - Safe experimentation

5. **Optimizes Intelligence** (/sh:memory)
   - Pattern recognition
   - Evolution tracking
   - Coordination optimization

6. **Monitors Health** (/sh:status)
   - Component-specific dashboards
   - Health scoring
   - Proactive alerts

**Result**: Strategic, recoverable, self-improving AI development system.
