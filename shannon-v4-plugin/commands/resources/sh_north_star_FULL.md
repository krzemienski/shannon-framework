# /sh:north-star - North Star Goal Management - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sh:north-star - North Star Goal Management

## Purpose

Set, manage, and maintain the North Star goal that acts as a persistent beacon ensuring all waves, operations, and decisions align with original intent throughout sessions.

**Core Objective**: Prevent scope creep and drift by anchoring all work to a clear, measurable goal that guides decision-making and resource allocation.

---

## Command Metadata

```yaml
command: /sh:north-star
aliases: [shannon:goal, shannon:north, shannon:ns]
category: Goal Management
sub_agent: NORTH_STAR_KEEPER
mcp_servers:
  primary: Serena
  secondary: Sequential
tools:
  - Read
  - Write
  - mcp__memory__create_entities
  - mcp__memory__add_observations
outputs:
  - Goal statements
  - Alignment scores
  - Strategic guidance
  - Drift warnings
```

---

## Usage Patterns

### Basic Usage
```bash
# Set North Star goal
/sh:north-star "Build secure, scalable authentication system"

# Get current goal
/sh:north-star

# Check alignment
/sh:north-star check "Add social login feature"

# View goal history
/sh:north-star history
```

### Context-Aware Usage
```bash
# Session start
User: "Let's build an auth system"
Response: /sh:north-star "Build production-ready authentication with JWT and OAuth"
→ Goal established for session guidance

# Mid-development drift detection
User: "Should we also add a payment system?"
Response: /sh:north-star check "Add payment system"
→ Alignment: 0.15 (MISALIGNED)
→ Warning: Scope creep detected

# Goal evolution
User: "Requirements changed - need to support SSO"
Response: /sh:north-star "Build enterprise auth with JWT, OAuth, and SSO"
→ Goal updated with rationale
→ History preserved
```

---

## North Star Actions

### SET - Establish Goal

**Purpose**: Define the guiding objective for all operations

**Goal Quality Criteria**:
```yaml
goal_characteristics:
  clear_and_specific:
    ✅ "Build JWT authentication with refresh tokens"
    ❌ "Make auth better"
  
  measurable_outcomes:
    ✅ "Achieve <100ms token validation"
    ❌ "Fast performance"
  
  time_bounded:
    ✅ "Launch MVP auth by end of sprint"
    ⚠️  "Eventually have auth" (acceptable if long-term)
  
  achievable:
    ✅ "Add rate limiting to existing auth"
    ❌ "Build AI-powered quantum blockchain auth"
  
  aligned_with_intent:
    ✅ Reflects user's actual request
    ❌ Interpreted differently than intended
```

**Example**:
```bash
/sh:north-star "Build secure authentication system with <100ms response time"

# Output:
🎯 NORTH STAR GOAL SET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Goal**: Build secure authentication system with <100ms response time

**Quality Assessment**:
✅ Clear and specific (authentication system defined)
✅ Measurable (<100ms performance target)
⚠️  Time-bounded (no explicit deadline - acceptable for now)
✅ Achievable (realistic technical goal)
✅ Aligned (matches user intent)

**Overall Quality**: 🟢 HIGH (4/5 criteria strong)

💾 Saved to: Serena memory + ~/.claude/shannon/north_star.txt

🧭 All subsequent operations will be evaluated against this goal
```

### GET - Retrieve Current Goal

**Purpose**: Display active North Star goal and metrics

**Example**:
```bash
/sh:north-star

# Output:
🎯 CURRENT NORTH STAR GOAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Goal**: Build secure authentication system with <100ms response time

**Set**: 2025-10-03 12:00:00 (4 hours ago)
**Status**: ✅ ACTIVE

**Recent Aligned Operations** (Last 10):
1. ✅ Implemented JWT token generation (Alignment: 1.0)
2. ✅ Added token validation middleware (Alignment: 1.0)
3. ✅ Optimized database queries (Alignment: 0.9)
4. ⚠️  Added user profile features (Alignment: 0.4)
5. ✅ Implemented rate limiting (Alignment: 0.95)

**Overall Alignment**: 0.85 (Good)

**Drift Warnings**: 1 operation below 0.5 threshold (#4)
```

### CHECK - Alignment Verification

**Purpose**: Verify if proposed operation aligns with goal

**Alignment Scoring**:
```yaml
scoring_rubric:
  direct_alignment: 1.0
    - Core functionality for goal
    - Essential requirement
    Example: "Add JWT validation" for "Build JWT auth" = 1.0
  
  partial_alignment: 0.5-0.9
    - Supports goal but not core
    - Enhances primary functionality
    Example: "Add password strength meter" = 0.7
  
  indirect_support: 0.2-0.5
    - Tangentially related
    - Nice-to-have feature
    Example: "Improve UI animations" = 0.3
  
  misalignment: <0.2
    - Scope creep
    - Unrelated feature
    - Goal drift
    Example: "Add payment processing" = 0.1
```

**Example**:
```bash
/sh:north-star check "Add OAuth social login"

# Output:
🧭 ALIGNMENT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Operation**: Add OAuth social login
**North Star**: Build secure authentication system with <100ms response time

**Alignment Analysis**:
📊 Score: 0.85 (Strong alignment)

**Rationale**:
✅ Direct support: OAuth is authentication mechanism
✅ Security: Leverages provider security (Google, GitHub)
⚠️  Performance: May add latency (external API calls)
✅ Scope: Within authentication system boundaries

**Recommendation**: ✅ PROCEED
Operation strongly aligns with North Star goal

**Considerations**:
- Monitor OAuth response times (keep <100ms budget)
- Implement caching for provider data
- Add fallback if OAuth providers slow
```

### HISTORY - Goal Evolution

**Purpose**: Show how North Star has evolved

**Example**:
```bash
/sh:north-star history

# Output:
📜 NORTH STAR HISTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Current Goal** (Active):
"Build secure authentication with <100ms response time"
Set: 2025-10-03 12:00:00
Duration: 4 hours
Operations: 23 aligned

**Previous Goals**:

1. "Build basic authentication" (Replaced)
   Set: 2025-10-03 08:00:00
   Duration: 2 hours
   Reason for change: "Performance requirement added"
   Impact: Expanded scope, added optimization focus

2. "Create user login system" (Replaced)
   Set: 2025-10-02 14:00:00
   Duration: 6 hours
   Reason for change: "Clarified security requirements"
   Impact: Added security emphasis, broader scope

**Evolution Insights**:
- Goals becoming more specific (good)
- Performance focus added (strategic improvement)
- Scope expanding gradually (monitor for creep)
```

---

## Execution Flow

### Step 1: Activate NORTH_STAR_KEEPER

**Sub-Agent Activation**:
```python
# Activate goal management specialist
activate_agent("NORTH_STAR_KEEPER")

# Agent characteristics:
# - Strategic alignment assessor
# - Scope creep detector
# - Goal evolution tracker
# - Decision guidance provider
```

### Step 2: Parse Action

**Action Router**:
```python
action = detect_action(command)

if no_arguments:
    action = "get"
elif is_goal_statement(arguments):
    action = "set"
elif arguments.startswith("check"):
    action = "check"
elif arguments == "history":
    action = "history"

params = extract_parameters(arguments, action)
```

### Step 3: Execute Action

**Action-Specific Logic**:
```python
if action == "set":
    # Validate goal quality
    quality = assess_goal_quality(params["goal"])
    if quality["score"] < 0.6:
        warn_user("Goal quality below threshold")
    
    # Store goal
    store_goal(params["goal"])
    create_entities([{
        "name": "north_star_goal",
        "entityType": "Goal",
        "observations": [params["goal"]]
    }])

elif action == "check":
    # Calculate alignment
    alignment = calculate_alignment(
        operation=params["operation"],
        goal=current_goal
    )
    
    # Provide guidance
    if alignment < 0.2:
        recommendation = "STOP - Misaligned"
    elif alignment < 0.5:
        recommendation = "RECONSIDER - Low alignment"
    elif alignment < 0.8:
        recommendation = "PROCEED with caution"
    else:
        recommendation = "PROCEED - Strong alignment"
```

---

## Sub-Agent Integration

### NORTH_STAR_KEEPER Role

**Specialization**: Goal alignment and strategic guidance

**Responsibilities**:
1. **Goal Management**: Set, update, and track North Star
2. **Alignment Scoring**: Calculate operation-goal fit
3. **Drift Detection**: Identify scope creep and misalignment
4. **Strategic Guidance**: Recommend aligned vs misaligned operations
5. **Evolution Tracking**: Monitor goal changes and impacts

**Agent Characteristics**:
```yaml
personality: Strategic, protective, alignment-focused
communication_style: Clear guidance with evidence
focus_areas:
  - Goal clarity and quality
  - Alignment assessment
  - Scope creep prevention
  - Strategic decision support
strengths:
  - Alignment calculation
  - Scope boundary enforcement
  - Goal evolution tracking
  - Strategic recommendations
```

---

## Integration with Shannon Commands

### Related Commands

**Goal-Aware Commands**:
- `/sh:wave` - Evaluates each wave against North Star
- `/sh:analyze` - Includes goal alignment layer
- `/sh:checkpoint` - Preserves North Star in snapshots
- `/sh:status` - Shows current goal and alignment

### Workflow Integration

```bash
# Goal-driven development
/sh:north-star "Build REST API with <50ms latency"
/sh:wave linear Implement API endpoints
# [During wave execution]
/sh:north-star check "Add GraphQL support"
→ Alignment: 0.3 (scope creep warning)
→ Decision: Defer to separate project
/sh:checkpoint  # Preserve aligned work
```

---

## Success Criteria

**North Star management succeeds when**:
- ✅ Goals are clear and measurable
- ✅ Alignment scoring is accurate
- ✅ Drift is detected early
- ✅ Decisions guided by goal
- ✅ Goal evolution tracked
- ✅ Scope boundaries enforced

**North Star management fails if**:
- ❌ Goals too vague to guide decisions
- ❌ Alignment scoring inconsistent
- ❌ Scope creep not detected
- ❌ Goal ignored in decisions

---

## Summary

`/sh:north-star` provides strategic goal management through:

- **Set**: Establish clear, measurable objectives
- **Get**: Review current goal and alignment metrics
- **Check**: Verify operation alignment before proceeding
- **History**: Track goal evolution and impacts

**Key Principle**: A clear North Star prevents drift, guides decisions, and ensures all work delivers value toward the intended outcome.
