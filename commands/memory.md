---
name: shannon:memory
description: Track and analyze memory coordination patterns and evolution
usage: /shannon:memory [track|pattern|visualize|optimize|stats] [entity_name]
---

# Memory Coordination Command

## Overview

Track, analyze, and optimize memory coordination patterns, revealing how knowledge evolves and is utilized throughout Shannon operations. This command delegates to the memory-coordination skill for all operations.

## Purpose

Transform memory from passive storage into active intelligence by tracking usage patterns, identifying optimization opportunities, and measuring coordination effectiveness.

## Prerequisites

- Serena MCP available (check with `/shannon:check_mcps`)
- Shannon entities in knowledge graph (created by Shannon commands/skills)

## Workflow

### Step 1: Parse User Intent

Determine operation type from user input:
- `track [entity]` → Track specific entity evolution
- `pattern` → Analyze overall memory patterns
- `visualize` → Create graph visualization
- `optimize` → Generate optimization recommendations
- `stats` → Display memory statistics

### Step 2: Invoke memory-coordination Skill

Use the `@skill memory-coordination` skill for all operations:

**For TRACK Operation:**
```
@skill memory-coordination
- Input:
  * operation: "track"
  * entity_name: [user_specified_entity]
  * verbose: [true if --verbose flag]
- Output: entity_evolution_report
```

**For PATTERN Operation:**
```
@skill memory-coordination
- Input:
  * operation: "pattern"
  * include_clusters: true
  * include_relationships: true
  * include_access_patterns: true
- Output: pattern_analysis_report
```

**For VISUALIZE Operation:**
```
@skill memory-coordination
- Input:
  * operation: "visualize"
  * format: "mermaid"
  * include_heatmap: true
- Output: graph_visualization
```

**For OPTIMIZE Operation:**
```
@skill memory-coordination
- Input:
  * operation: "optimize"
  * include_impact_scores: true
  * include_recommendations: true
- Output: optimization_report
```

**For STATS Operation:**
```
@skill memory-coordination
- Input:
  * operation: "stats"
  * include_growth_metrics: true
  * include_health_status: true
- Output: statistics_dashboard
```

### Step 3: Present Results

The memory-coordination skill handles all analysis and returns formatted results. Display the skill's output directly to the user.

**Track Output Example:**
```
📊 ENTITY EVOLUTION: authentication
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Timeline:
Day 1: Entity created with 3 observations
Day 2: +5 observations, 2 relationships added
Day 3: +12 observations, 4 relationships added (Current)

Observations (20 total):
- Early (1-5): Basic requirements and design decisions
- Middle (6-15): Implementation details and challenges
- Recent (16-20): Performance optimization, security hardening

Relationships (6 total):
- implements → jwt_service
- requires → user_database
- coordinates_with → session_manager
- validates_via → token_validator
- integrates_with → oauth_provider
- monitored_by → security_scanner

Access Patterns:
- Total accesses: 47
- Peak: Phase 2 implementation (23 accesses)
- Recent: 5 accesses this session
- Efficiency: 0.76 (good reuse)

Health: ✅ Healthy evolution (balanced growth)
```

**Pattern Output Example:**
```
📈 MEMORY PATTERN ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entity Clustering:
Cluster 1: Authentication (8 entities) - Dense, well-connected
Cluster 2: Database (5 entities) - Moderate connectivity
Cluster 3: UI Components (12 entities) - Sparse connections
Orphans: 3 entities with no relationships

Relationship Distribution:
- implements: 23 (32%)
- requires: 18 (25%)
- coordinates_with: 15 (21%)
- validates_via: 8 (11%)
- integrates_with: 8 (11%)

Access Patterns:
🔥 Hot entities (>20 accesses): authentication, user, database
❄️  Cold entities (<5 accesses): legacy_payment, old_session
📊 Access distribution: 80/20 rule (20% entities = 80% accesses)

Evolution Trajectories:
📈 Growing: authentication (+15 obs/day), api_gateway (+8/day)
➡️  Stable: database (±2 obs/day)
📉 Declining: legacy_session (-3 obs/day, candidate for pruning)

Coordination Effectiveness: 0.78 (Good)
```

**Visualize Output Example:**
```
🎨 MEMORY GRAPH VISUALIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Mermaid diagram with colored nodes and relationships]

Legend:
🔴 Hot (>20 accesses) | 🟡 Warm (10-20) | 🟢 Cool (5-10) | ⚪ Cold (<5)

Access Heatmap:
authentication: ████████████████████░ 95%
user_database:  ████████████░░░░░░░░░ 60%
jwt_service:    ██████████░░░░░░░░░░░ 50%
legacy_payment: █░░░░░░░░░░░░░░░░░░░░  5%
```

**Optimize Output Example:**
```
💡 MEMORY OPTIMIZATION RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

High Impact 🔴:
1. Merge Redundant Entities
   - "user_auth" + "authentication" → Single "authentication" entity
   - Impact: Reduce confusion, improve access efficiency
   - Effort: Low (automated merge)

2. Add Critical Relationship
   - authentication →[validates_via]→ rate_limiter (MISSING)
   - Impact: Complete security context
   - Effort: Low (single relationship)

Medium Impact 🟡:
3. Prune Stale Observations
   - "legacy_payment" has 45 observations, 40 are >30 days old
   - Impact: Reduce noise, focus on relevant
   - Effort: Low (automated pruning with review)

Estimated Gains:
- Coordination score: 0.78 → 0.88 (+13%)
- Access efficiency: 0.71 → 0.82 (+15%)
- Token usage: -10% (reduced graph traversal)
```

**Stats Output Example:**
```
📊 MEMORY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Graph Size:
- Total Entities: 42
- Total Relations: 78
- Total Observations: 247
- Avg Observations/Entity: 5.9

Growth Metrics:
- Entities added (7 days): +12 (1.7/day)
- Relations added (7 days): +23 (3.3/day)
- Observations added (7 days): +89 (12.7/day)

Access Distribution:
- Hot entities (>20 accesses): 4 (9.5%)
- Warm entities (10-20): 8 (19%)
- Cool entities (5-10): 12 (28.6%)
- Cold entities (<5): 18 (42.9%)

Coordination Score: 0.78
- Access efficiency: 0.81
- Pattern consistency: 0.76
- Evolution coherence: 0.77

Health Status: ✅ HEALTHY
```

## Skill Dependencies

- memory-coordination (REQUIRED) - All operations

## MCP Dependencies

- Serena MCP (required for knowledge graph access)
- Sequential MCP (recommended for complex pattern analysis)

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same operation types (track, pattern, visualize, optimize, stats)
- Compatible output format

**Changes from V3:**
- Internal: Now delegates to memory-coordination skill (was monolithic)
- Enhancement: Better pattern recognition with Sequential MCP
- Enhancement: More detailed optimization recommendations
- Enhancement: Improved visualization with access heatmaps
- No breaking changes

## Usage Examples

**Track Specific Entity:**
```bash
/shannon:memory track authentication
```

**Analyze Patterns:**
```bash
/shannon:memory pattern
```

**Visualize Graph:**
```bash
/shannon:memory visualize
```

**Get Optimization Recommendations:**
```bash
/shannon:memory optimize
```

**Display Statistics:**
```bash
/shannon:memory stats
```

## When to Use

- **During Development**: Track entity evolution (authentication, API, database)
- **After Wave Completion**: Analyze patterns that emerged during implementation
- **Performance Optimization**: Check if memory is being used efficiently
- **Regular Maintenance**: Monitor graph health and identify cleanup opportunities
- **Before Major Refactoring**: Understand entity relationships and dependencies

## Related Commands

- `/shannon:\1` - Shows memory health in session context
- `/shannon:\1` - Creates checkpoint with memory snapshot
- `/shannon:\1` - Restores memory state from checkpoint
