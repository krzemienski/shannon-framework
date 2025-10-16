---
name: sh:analyze
command: /sh:analyze
description: Deep contextual analysis with memory coordination tracking
category: command
sub_agents: [DEEP_ANALYZER]
mcp_servers: [sequential, serena, context7]
version: 3.0
---

# /sh:analyze - Deep Contextual Analysis

## Purpose

Perform multi-layered contextual analysis with comprehensive memory coordination tracking, providing actionable insights across surface, structural, strategic, and memory dimensions.

**Core Objective**: Deliver evidence-based analysis that reveals patterns, identifies opportunities, and guides decision-making through systematic investigation.

---

## Command Metadata

```yaml
command: /sh:analyze
aliases: [shannon:deep, shannon:context]
category: Analysis & Investigation
sub_agent: DEEP_ANALYZER
mcp_servers:
  primary: Sequential
  secondary: Serena
  tertiary: Context7
tools:
  - Read
  - Grep
  - Glob
  - TodoWrite
  - Task
  - mcp__memory__search_nodes
  - mcp__memory__read_graph
  - mcp__memory__open_nodes
  - mcp__sequential-thinking__sequentialthinking
outputs:
  - Multi-layer analysis report
  - Memory utilization metrics
  - Goal alignment assessment
  - Actionable recommendations
  - Next steps roadmap
```

---

## Usage Patterns

### Basic Usage
```bash
# Analyze current context
/sh:analyze

# Analyze specific target
/sh:analyze authentication

# Specify analysis depth
/sh:analyze src/ comprehensive
/sh:analyze "user flow" exhaustive
```

### Context-Aware Usage
```bash
# System architecture review
User: "Analyze our microservices architecture"
Response: /sh:analyze architecture comprehensive
→ Structural layer: Component relationships
→ Strategic layer: Scalability assessment
→ Memory layer: Pattern evolution tracking

# Security assessment
User: "Check authentication for vulnerabilities"
Response: /sh:analyze authentication exhaustive
→ Surface layer: Immediate issues
→ Structural layer: Design weaknesses
→ Strategic layer: Long-term security posture

# Performance investigation
User: "Why is the app slow?"
Response: /sh:analyze performance comprehensive
→ Discovery: Bottleneck identification
→ Examination: Root cause analysis
→ Synthesis: Optimization recommendations
```

---

## Analysis Layers

### Layer 1: Surface Analysis
**Focus**: Immediate observations and obvious patterns

**What It Examines**:
- Visible structure and organization
- Obvious patterns and anti-patterns
- Direct relationships and dependencies
- Immediate context and environment

**Output Example**:
```markdown
## SURFACE LAYER FINDINGS

**Visible Structure**:
- 15 microservices identified
- API gateway at entry point
- Message queue for async operations

**Obvious Patterns**:
✅ RESTful API design
✅ Service isolation
⚠️  Inconsistent error handling
❌ Missing rate limiting

**Direct Relationships**:
- Auth service → User database
- Payment service → External gateway
- Notification service → Message queue
```

### Layer 2: Structural Analysis
**Focus**: Architectural and design patterns

**What It Examines**:
- System architecture and topology
- Design pattern usage and consistency
- Dependency management and coupling
- Information flow and data models
- Component interaction patterns

**Output Example**:
```markdown
## STRUCTURAL LAYER FINDINGS

**Architecture Assessment**:
- Pattern: Microservices with event-driven communication
- Coupling: Loose (services communicate via events)
- Cohesion: High (each service has single responsibility)

**Design Patterns Identified**:
✅ Circuit Breaker (external calls)
✅ Saga Pattern (distributed transactions)
⚠️  Inconsistent retry strategies
❌ Missing bulkhead isolation

**Dependency Analysis**:
- Critical path: Auth → User → Profile → Display
- Circular dependency detected: Service A ↔ Service B
- External dependencies: 12 third-party services
```

### Layer 3: Strategic Analysis
**Focus**: Goal alignment and long-term implications

**What It Examines**:
- North Star goal alignment
- Strategic implications of current design
- Trade-offs and opportunity costs
- Long-term impact and sustainability
- Risk assessment and mitigation

**Output Example**:
```markdown
## STRATEGIC LAYER FINDINGS

**North Star Alignment**: ⚠️  0.65 (Below optimal)

**Strategic Implications**:
- Current: Optimized for development speed
- Trade-off: Sacrificed operational simplicity
- Impact: Higher maintenance overhead

**Risk Assessment**:
🔴 HIGH: Single point of failure in auth service
🟡 MEDIUM: Service discovery relies on one registry
🟢 LOW: Data backup and recovery tested

**Long-term Sustainability**:
✅ Scalability: Horizontal scaling supported
⚠️  Maintainability: Complexity increasing
❌ Observability: Limited distributed tracing
```

### Layer 4: Memory Coordination Analysis
**Focus**: How memory is utilized and evolves

**What It Examines**:
- Entity access patterns and frequency
- Relationship traversal paths
- Context building progression
- Memory gaps and missing connections
- Coordination effectiveness metrics

**Output Example**:
```markdown
## MEMORY COORDINATION FINDINGS

**Entity Access Patterns**:
- Most accessed: "authentication" (47 times)
- Relationship heavy: "user_service" (23 connections)
- Orphaned: "legacy_payment" (no relationships)

**Traversal Analysis**:
- Efficient paths: auth → user → profile (2 hops)
- Inefficient: notification → user (5 hops via circuitous route)
- Missing shortcuts: Could relate auth directly to notification

**Memory Gaps Identified**:
❌ No entity for "API gateway configuration"
❌ Missing relationship: security ↔ compliance
❌ Incomplete observations for "deployment pipeline"

**Coordination Effectiveness**: 0.72 (Good)
- Access efficiency: 0.78
- Pattern consistency: 0.71
- Evolution coherence: 0.67
```

---

## Execution Flow

### Step 1: Activate DEEP_ANALYZER

**Sub-Agent Activation**:
```python
# Activate specialized deep analysis agent
activate_agent("DEEP_ANALYZER")

# Agent characteristics:
# - Multi-layer analytical thinking
# - Pattern recognition specialist
# - Memory coordination expert
# - Strategic alignment assessor
```

### Step 2: Check North Star Goal

**Goal Context Loading**:
```python
# STEP 1: Query for active North Star
try:
    north_star = read_memory("north_star_goal")
    has_goal = True
except:
    north_star = None
    has_goal = False

# STEP 2: Load goal context for alignment analysis
if has_goal:
    goal_entities = search_nodes(query=north_star)
    goal_context = build_goal_context(goal_entities)
```

### Step 3: Query Relevant Memory

**Memory Context Building**:
```python
# STEP 1: Identify target for analysis
target = parse_target(request)  # "authentication", "src/", etc.

# STEP 2: Search for related entities
related = search_nodes(query=target)

# STEP 3: Load entity details and relationships
memory_graph = {}
for entity in related:
    details = open_nodes(names=[entity.name])
    memory_graph[entity.name] = details

# STEP 4: Identify memory gaps
gaps = find_memory_gaps(target, memory_graph)
```

### Step 4: Execute Discovery Phase

**Information Gathering**:
```python
# STEP 1: Gather all relevant information
if target_is_file_or_directory(target):
    content = Read(file_path=target)
    related_files = Glob(pattern=f"{target}/**/*")
    references = Grep(pattern=target)
else:
    # Conceptual target
    content = search_nodes(query=target)
    related_files = []
    references = []

# STEP 2: Query memory for related entities
memory_entities = search_nodes(query=target)

# STEP 3: Identify patterns and structures
patterns = identify_patterns(content)
structures = map_structures(content, related_files)

# STEP 4: Map relationships
relationships = map_relationships(patterns, structures, memory_entities)
```

### Step 5: Execute Examination Phase

**Deep Analysis with Sequential Thinking**:
```python
# Use Sequential MCP for complex reasoning
analysis_result = sequentialthinking(
    thought="Analyzing patterns in detail. Layer 1: Surface observations show...",
    thoughtNumber=1,
    totalThoughts=10,
    nextThoughtNeeded=True
)

# Track memory access during examination
access_log = []
for entity in memory_entities:
    entity_data = open_nodes(names=[entity.name])
    access_log.append({
        "entity": entity.name,
        "timestamp": now(),
        "context": "examination_phase"
    })

# Detailed pattern analysis
pattern_details = {}
for pattern in patterns:
    details = analyze_pattern_deeply(pattern, context)
    pattern_details[pattern.name] = details
```

### Step 6: Execute Synthesis Phase

**Insight Generation**:
```python
# STEP 1: Combine findings from all layers
synthesis = {
    "surface": surface_findings,
    "structural": structural_findings,
    "strategic": strategic_findings,
    "memory": memory_findings
}

# STEP 2: Identify key insights
insights = extract_insights(synthesis)

# STEP 3: Assess goal alignment
if has_goal:
    alignment = assess_alignment(synthesis, north_star)
    alignment_score = calculate_score(alignment)
else:
    alignment_score = None

# STEP 4: Generate recommendations
recommendations = generate_recommendations(
    insights,
    alignment_score,
    memory_gaps
)
```

### Step 7: Track Memory Utilization

**Memory Coordination Metrics**:
```python
# Document entities accessed during analysis
entities_accessed = list(set([log["entity"] for log in access_log]))

# Track relationship traversals
traversals = []
for i in range(len(access_log) - 1):
    traversals.append({
        "from": access_log[i]["entity"],
        "to": access_log[i+1]["entity"],
        "purpose": "analysis_navigation"
    })

# Monitor observation patterns
observation_patterns = analyze_observation_usage(access_log)

# Identify memory gaps
gaps_found = identify_gaps(target, entities_accessed)

# Measure coordination efficiency
efficiency = calculate_efficiency(
    access_log,
    traversals,
    observation_patterns,
    gaps_found
)
```

### Step 8: Generate Output

**Report Assembly**:
```python
# Build comprehensive analysis report
report = {
    "executive_summary": create_summary(insights),
    "layer_findings": {
        "surface": surface_findings,
        "structural": structural_findings,
        "strategic": strategic_findings,
        "memory_coordination": memory_findings
    },
    "memory_utilization": {
        "entities_accessed": entities_accessed,
        "traversals": traversals,
        "gaps": gaps_found,
        "efficiency": efficiency
    },
    "goal_alignment": {
        "score": alignment_score,
        "assessment": alignment_details
    },
    "recommendations": recommendations,
    "next_steps": generate_next_steps(recommendations)
}

# Display formatted report
display_analysis_report(report)
```

---

## Output Format

### Comprehensive Analysis Template

```markdown
🔍 DEEP ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Executive Summary

**Target**: Authentication System
**Depth**: Comprehensive
**Analysis Duration**: 12 minutes
**Entities Accessed**: 23
**Coordination Efficiency**: 0.78 (Good)

**Key Findings**:
1. Security architecture is sound but missing rate limiting
2. Performance bottleneck in token validation (2x slower than optimal)
3. Strategic misalignment with "zero-trust" North Star goal (0.65 score)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Layer 1: Surface Analysis

[Surface findings as shown above]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Layer 2: Structural Analysis

[Structural findings as shown above]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Layer 3: Strategic Analysis

[Strategic findings as shown above]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Layer 4: Memory Coordination

[Memory findings as shown above]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Recommendations

### High Priority 🔴
1. **Add Rate Limiting** (Security)
   - Impact: Prevents DoS attacks
   - Effort: 2-4 hours
   - Aligns with: Zero-trust goal

2. **Optimize Token Validation** (Performance)
   - Impact: 2x speed improvement
   - Effort: 4-6 hours
   - Aligns with: User experience goal

### Medium Priority 🟡
3. **Improve Observability** (Operations)
4. **Add Circuit Breakers** (Reliability)

### Low Priority 🟢
5. **Refactor Error Messages** (UX)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Next Steps

1. Implement rate limiting (Priority 1)
2. Profile token validation for optimization (Priority 2)
3. Re-analyze after changes to measure improvement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Analysis Complete** | 📅 2025-10-03 | ⏱️  12min | 🎯 Alignment: 0.65
```

---

## Sub-Agent Integration

### DEEP_ANALYZER Role

**Specialization**: Multi-layer contextual analysis with memory coordination

**Responsibilities**:
1. **Multi-Layer Analysis**: Surface, structural, strategic, memory
2. **Pattern Recognition**: Identify anti-patterns and best practices
3. **Memory Coordination**: Track and optimize entity usage
4. **Goal Alignment**: Assess strategic fit with North Star
5. **Insight Generation**: Extract actionable recommendations

**Agent Characteristics**:
```yaml
personality: Analytical, thorough, evidence-based
communication_style: Structured findings with clear evidence
focus_areas:
  - Multi-dimensional analysis
  - Memory access optimization
  - Strategic alignment assessment
  - Pattern-based insights
strengths:
  - Complex system understanding
  - Memory coordination tracking
  - Strategic thinking
  - Actionable recommendations
```

---

## Integration with Shannon Commands

### Related Commands

**Before /sh:analyze**:
- `/sh:north-star` - Set analysis goal context
- `/sh:status` - Understand current state

**During /sh:analyze**:
- `/sh:memory track` - Monitor memory evolution
- Sequential thinking - Complex reasoning

**After /sh:analyze**:
- `/sh:wave` - Execute recommendations
- `/sh:checkpoint` - Save analysis insights

### Workflow Integration

```bash
# Analysis-driven workflow
/sh:north-star "Build zero-trust security"
/sh:analyze authentication comprehensive
# [Analysis reveals gaps]
/sh:wave iterative Implement rate limiting and optimization
/sh:analyze authentication  # Re-analyze improvements
```

---

## Examples

### Example 1: File Analysis

**Input**:
```bash
/sh:analyze src/auth/jwt.ts structural
```

**Output**:
```markdown
🔍 STRUCTURAL ANALYSIS: src/auth/jwt.ts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Architecture**: JWT token management module

**Design Patterns**:
✅ Factory Pattern: Token creation
✅ Singleton: Token validator instance
⚠️  Missing: Strategy pattern for different token types

**Dependencies**:
- jsonwebtoken (external)
- crypto (built-in)
- ./config (internal)

**Information Flow**:
user credentials → generateToken() → JWT string → validateToken() → decoded user

**Recommendations**:
1. Add token refresh strategy
2. Implement token blacklisting
3. Consider rotation for signing keys
```

### Example 2: Conceptual Analysis

**Input**:
```bash
/sh:analyze "user authentication flow" comprehensive
```

**Output**:
```markdown
🔍 COMPREHENSIVE ANALYSIS: User Authentication Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Surface Layer**:
- Login endpoint: POST /api/auth/login
- Social OAuth: Google, GitHub supported
- Session management: JWT-based

**Structural Layer**:
- Pattern: OAuth 2.0 + JWT hybrid
- Flow: Credentials → Validation → Token → Protected Resources
- Missing: Refresh token rotation

**Strategic Layer**:
- Goal Alignment: 0.72 with "secure authentication"
- Trade-off: Simplicity vs. enterprise features
- Risk: Token theft vulnerability

**Memory Coordination**:
- Entities: auth_service, user_service, token_validator
- Efficient path: auth → user (1 hop)
- Gap: No "session_manager" entity

**Recommendations**:
1. Add refresh token rotation (CRITICAL)
2. Implement device tracking
3. Add suspicious login detection
```

---

## Technical Implementation

### Multi-Layer Analysis Engine

```python
def analyze_target(target: str, depth: str) -> dict:
    """
    Execute multi-layer analysis based on depth
    """
    layers_to_execute = {
        "surface": ["surface"],
        "structural": ["surface", "structural"],
        "comprehensive": ["surface", "structural", "strategic"],
        "exhaustive": ["surface", "structural", "strategic", "memory"]
    }
    
    results = {}
    layers = layers_to_execute.get(depth, ["surface"])
    
    for layer in layers:
        if layer == "surface":
            results["surface"] = surface_analysis(target)
        elif layer == "structural":
            results["structural"] = structural_analysis(target)
        elif layer == "strategic":
            results["strategic"] = strategic_analysis(target)
        elif layer == "memory":
            results["memory"] = memory_coordination_analysis(target)
    
    return results
```

### Memory Access Tracking

```python
def track_memory_access(entity_name: str, context: str):
    """
    Track entity access for coordination analysis
    """
    access_log.append({
        "entity": entity_name,
        "timestamp": datetime.now(),
        "context": context,
        "access_type": "read"
    })
    
    # Update access frequency
    access_frequency[entity_name] = access_frequency.get(entity_name, 0) + 1
```

### Coordination Efficiency Calculation

```python
def calculate_coordination_efficiency(access_log: list) -> float:
    """
    Calculate memory coordination effectiveness
    """
    # Access efficiency: unique entities / total accesses
    unique_entities = len(set([log["entity"] for log in access_log]))
    total_accesses = len(access_log)
    access_efficiency = unique_entities / total_accesses if total_accesses > 0 else 0
    
    # Pattern consistency: how predictable is access pattern
    pattern_consistency = analyze_pattern_predictability(access_log)
    
    # Evolution coherence: logical progression of accesses
    evolution_coherence = analyze_access_sequence_logic(access_log)
    
    # Combined score
    coordination_score = (
        access_efficiency * 0.33 +
        pattern_consistency * 0.33 +
        evolution_coherence * 0.34
    )
    
    return coordination_score
```

---

## Success Criteria

**Analysis succeeds when**:
- ✅ All requested layers completed thoroughly
- ✅ Memory coordination tracked comprehensively
- ✅ Goal alignment assessed (if North Star exists)
- ✅ Actionable recommendations provided
- ✅ No significant gaps in coverage
- ✅ Evidence supports all findings
- ✅ Next steps clearly defined

**Analysis fails if**:
- ❌ Layer coverage incomplete
- ❌ Memory access not tracked
- ❌ Recommendations not actionable
- ❌ Findings lack evidence
- ❌ Goal alignment not assessed

---

## Summary

`/sh:analyze` provides comprehensive multi-layer analysis combining:

- **Surface Layer**: Immediate observations and patterns
- **Structural Layer**: Architecture and design analysis  
- **Strategic Layer**: Goal alignment and long-term impact
- **Memory Coordination**: Entity access and optimization

**Key Principle**: Effective analysis requires examining multiple dimensions while tracking how knowledge is constructed and utilized through memory coordination.
