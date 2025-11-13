---
name: shannon-goal-tracker
display_name: "Shannon Goal Tracker (North Star Management)"
description: "Manages the North Star goal - the primary project objective that guides all decisions and priorities"
category: management
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_north_star command"
  - "north star requested"
  - "set project goal"
  - "update project goal"
mcp_servers:
  required:
    - serena
allowed_tools:
  - serena_write_memory
  - serena_read_memory
  - serena_list_memories
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
input:
  action:
    type: string
    description: "Action: set, get, update, validate"
    required: true
  goal:
    type: string
    description: "The North Star goal (for set/update)"
    required: false
output:
  north_star_goal:
    type: string
    description: "Current North Star goal"
  validation:
    type: object
    description: "Goal validation results"
  sitrep:
    type: object
    description: "Standardized SITREP (via shannon-status-reporter)"
---

# Shannon Goal Tracker

> **North Star Management**: Define and maintain the primary project objective

## Purpose

Manages the North Star goal - the single, clear objective that guides all project decisions, priorities, and validations.

**Key Principle**: Every feature, decision, and task must serve the North Star goal.

## Capabilities

### 1. Goal Setting
- Define clear, actionable North Star goal
- Validate goal clarity and measurability
- Store to Serena MCP for persistence
- Generate goal-setting SITREP

### 2. Goal Retrieval
- Load current North Star from Serena
- Display goal to user
- Check goal alignment with project state
- Report goal status

### 3. Goal Update
- Modify existing North Star goal
- Track goal evolution history
- Maintain audit trail
- Validate goal changes

### 4. Goal Validation
- Ensure goal is SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- Check alignment with current work
- Identify drift from North Star
- Recommend corrections

## Activation

**Automatic**:
```bash
/sh_north_star set "Build production-ready React dashboard"
/sh_north_star get
/sh_north_star update "Build production-ready React dashboard with real-time charts"
/sh_north_star validate
```

**Manual**:
```bash
Skill("shannon-goal-tracker")
```

## Execution Algorithm

### Step 1: Determine Action

```javascript
const action = input.action; // "set", "get", "update", "validate"
const project_id = extract_project_id();
const timestamp = Date.now();

// Load current goal if exists
const current_goal = await serena_read_memory("north_star_goal");
```

### Step 2: Execute Action

#### Action: SET

```javascript
async function setNorthStar(goal) {
  // Validate goal format
  const validation = validateGoal(goal);

  if (!validation.is_valid) {
    throw new Error(`Invalid goal: ${validation.errors.join(', ')}`);
  }

  // Store to Serena
  await serena_write_memory("north_star_goal", {
    goal,
    project_id,
    created_at: timestamp,
    created_by: get_user_context(),
    version: 1,
    validation
  });

  // Create goal entity in knowledge graph
  await serena_create_entities([{
    name: "north_star_goal",
    type: "goal",
    metadata: { goal, project_id, timestamp }
  }]);

  return { action: "set", goal, validation };
}
```

#### Action: GET

```javascript
async function getNorthStar() {
  const goal_data = await serena_read_memory("north_star_goal");

  if (!goal_data) {
    return {
      action: "get",
      goal: null,
      message: "No North Star goal set. Use /sh_north_star set \"your goal\""
    };
  }

  return {
    action: "get",
    goal: goal_data.goal,
    created_at: goal_data.created_at,
    version: goal_data.version,
    validation: goal_data.validation
  };
}
```

#### Action: UPDATE

```javascript
async function updateNorthStar(new_goal) {
  const current = await serena_read_memory("north_star_goal");

  if (!current) {
    throw new Error("No goal to update. Use 'set' instead.");
  }

  // Validate new goal
  const validation = validateGoal(new_goal);

  if (!validation.is_valid) {
    throw new Error(`Invalid goal: ${validation.errors.join(', ')}`);
  }

  // Save history
  await serena_write_memory(`north_star_goal_history_v${current.version}`, {
    goal: current.goal,
    replaced_at: timestamp,
    version: current.version
  });

  // Update current goal
  await serena_write_memory("north_star_goal", {
    goal: new_goal,
    project_id,
    created_at: current.created_at,
    updated_at: timestamp,
    updated_by: get_user_context(),
    version: current.version + 1,
    validation,
    previous_goal: current.goal
  });

  return {
    action: "update",
    goal: new_goal,
    previous_goal: current.goal,
    version: current.version + 1,
    validation
  };
}
```

#### Action: VALIDATE

```javascript
async function validateNorthStar() {
  const current = await serena_read_memory("north_star_goal");

  if (!current) {
    return {
      action: "validate",
      is_valid: false,
      message: "No North Star goal set"
    };
  }

  // SMART validation
  const validation = validateGoal(current.goal);

  // Check alignment with current work
  const phase_plan = await serena_read_memory("phase_plan_detailed");
  const alignment = checkAlignment(current.goal, phase_plan);

  return {
    action: "validate",
    goal: current.goal,
    validation,
    alignment,
    recommendations: generateRecommendations(validation, alignment)
  };
}
```

### Step 3: Validate Goal (SMART Criteria)

```javascript
function validateGoal(goal) {
  const errors = [];
  const warnings = [];

  // Specific: Clear and unambiguous
  if (goal.length < 10) {
    errors.push("Goal too vague (< 10 characters)");
  }

  if (!containsActionVerb(goal)) {
    warnings.push("Goal should start with action verb (Build, Create, Implement, etc.)");
  }

  // Measurable: Has clear success criteria
  const has_measurable =
    /\d/.test(goal) || // Contains numbers
    /(complete|ready|functional|working|deployed)/i.test(goal); // Or clear state

  if (!has_measurable) {
    warnings.push("Goal lacks measurable criteria");
  }

  // Achievable: Not too broad
  if (goal.length > 200) {
    warnings.push("Goal might be too broad (> 200 characters)");
  }

  // Relevant: Contains project context
  const has_context = /(app|website|system|service|api|dashboard|platform)/i.test(goal);

  if (!has_context) {
    warnings.push("Goal lacks project context");
  }

  // Time-bound: Implicit or explicit timeline
  const has_timeline = /(by|within|before|deadline)/i.test(goal);

  // Time-bound is optional for North Star goals (they're strategic)

  return {
    is_valid: errors.length === 0,
    errors,
    warnings,
    score: calculateGoalScore(errors, warnings),
    criteria: {
      specific: errors.length === 0 && goal.length >= 10,
      measurable: has_measurable,
      achievable: goal.length <= 200,
      relevant: has_context,
      time_bound: has_timeline // optional
    }
  };
}

function calculateGoalScore(errors, warnings) {
  if (errors.length > 0) return 0;
  const warning_penalty = warnings.length * 0.15;
  return Math.max(0, 1.0 - warning_penalty);
}

function containsActionVerb(goal) {
  const action_verbs = [
    'build', 'create', 'implement', 'develop', 'design', 'deploy',
    'establish', 'launch', 'deliver', 'provide', 'enable', 'support'
  ];

  const first_word = goal.toLowerCase().split(' ')[0];
  return action_verbs.includes(first_word);
}
```

### Step 4: Check Alignment with Current Work

```javascript
function checkAlignment(goal, phase_plan) {
  if (!phase_plan) {
    return {
      aligned: "unknown",
      message: "No phase plan exists yet"
    };
  }

  // Extract key terms from goal
  const goal_terms = extractKeyTerms(goal);

  // Extract key terms from phase plan objectives
  const plan_terms = phase_plan.phases.flatMap(p =>
    extractKeyTerms(p.objectives.join(' '))
  );

  // Calculate overlap
  const overlap = goal_terms.filter(term => plan_terms.includes(term));
  const alignment_score = overlap.length / goal_terms.length;

  return {
    aligned: alignment_score > 0.5 ? "yes" : "partial",
    alignment_score,
    overlapping_terms: overlap,
    missing_terms: goal_terms.filter(term => !plan_terms.includes(term)),
    message: alignment_score > 0.7
      ? "Phase plan strongly aligned with North Star"
      : alignment_score > 0.5
      ? "Phase plan partially aligned with North Star"
      : "Phase plan may not fully serve North Star goal"
  };
}

function extractKeyTerms(text) {
  // Simple term extraction (in real implementation, use NLP)
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, '')
    .split(/\s+/)
    .filter(w => w.length > 4); // Filter out short words

  return [...new Set(words)]; // Unique terms
}
```

### Step 5: Generate SITREP

```javascript
// Generate standardized SITREP using shannon-status-reporter
const sitrep_data = {
  agent_name: "shannon-goal-tracker",
  task_id: `north_star_${action}_${timestamp}`,
  current_phase: "Goal Management",
  progress: 100, // Goal management action complete
  state: "completed",

  objective: `${action.toUpperCase()} North Star goal`,
  scope: [
    `Action: ${action}`,
    action === "set" || action === "update" ? `Goal: ${goal}` : "Goal retrieval/validation"
  ],
  dependencies: ["serena"],

  findings: [
    `Action completed: ${action}`,
    current_goal ? `Current goal: ${current_goal.goal}` : "No previous goal",
    validation ? `Validation score: ${validation.score}` : "N/A",
    alignment ? `Alignment: ${alignment.aligned}` : "N/A"
  ].filter(Boolean),

  blockers: validation && !validation.is_valid ? validation.errors : [],
  risks: validation && validation.warnings ? validation.warnings : [],
  questions: [],

  next_steps: [
    action === "get" && !current_goal ? "Set North Star goal with /sh_north_star set \"your goal\"" : null,
    action === "set" || action === "update" ? "Create phase plan with /sh:plan" : null,
    alignment && alignment.aligned === "partial" ? "Review phase plan alignment with North Star" : null
  ].filter(Boolean),

  artifacts: [
    "north_star_goal (saved to Serena)",
    action === "update" ? `north_star_goal_history_v${current.version}` : null
  ].filter(Boolean),

  tests_executed: ["goal_validation", "smart_criteria_check", action === "validate" ? "alignment_check" : null].filter(Boolean),
  test_results: validation && validation.is_valid ? "All validations passed" : "Validation warnings present"
};

// Invoke shannon-status-reporter to generate SITREP
const sitrep = await generate_sitrep(sitrep_data);

// Save SITREP alongside goal
await serena_write_memory(`north_star_${action}_${timestamp}_sitrep`, {
  sitrep_markdown: sitrep,
  sitrep_data
});

return sitrep;
```

## Examples

### Example 1: Set North Star Goal

```bash
/sh_north_star set "Build production-ready React dashboard with real-time data visualization"
```

**SITREP Output**:
```markdown
## SITREP: shannon-goal-tracker - north_star_set_1730739600000

### Status
- **Current Phase**: Goal Management
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: SET North Star goal
- **Scope**: Action: set, Goal: Build production-ready React dashboard with real-time data visualization
- **Dependencies**: serena

### Findings
- Action completed: set
- No previous goal
- Validation score: 1.0
- SMART criteria: ✅ Specific, ✅ Measurable, ✅ Achievable, ✅ Relevant

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- [ ] Create phase plan with /sh:plan

### Artifacts
- north_star_goal (saved to Serena)

### Validation
- **Tests Executed**: goal_validation, smart_criteria_check
- **Results**: All validations passed
```

### Example 2: Validate North Star Alignment

```bash
/sh_north_star validate
```

**SITREP Output**:
```markdown
## SITREP: shannon-goal-tracker - north_star_validate_1730739700000

### Status
- **Current Phase**: Goal Management
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: VALIDATE North Star goal
- **Scope**: Action: validate, Goal retrieval/validation
- **Dependencies**: serena

### Findings
- Action completed: validate
- Current goal: Build production-ready React dashboard with real-time data visualization
- Validation score: 1.0
- Alignment: yes (alignment score: 0.85)

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- (None - goal validated and aligned)

### Artifacts
- north_star_goal (saved to Serena)

### Validation
- **Tests Executed**: goal_validation, smart_criteria_check, alignment_check
- **Results**: All validations passed
```

### Example 3: Update North Star Goal

```bash
/sh_north_star update "Build production-ready React dashboard with real-time data visualization and user authentication"
```

**SITREP Output** shows version history and goal evolution.

## Integration with Shannon v4

**Used by**:
- /sh_north_star command (primary interface)
- shannon-spec-analyzer (validates spec serves North Star)
- shannon-phase-planner (ensures plan serves North Star)
- shannon-wave-orchestrator (validates wave serves North Star)

**Uses**:
- shannon-status-reporter (SITREP generation)
- serena MCP (goal persistence)

**Goal-Driven Validation**:
```
Every decision → Check against North Star → Approve or reject
```

## Best Practices

### DO ✅
- Set North Star at project start
- Make goal specific and measurable
- Validate alignment regularly
- Update goal when project pivots
- Use goal to resolve ambiguity

### DON'T ❌
- Set vague goals ("Make it better")
- Change goal frequently (creates chaos)
- Ignore alignment warnings
- Set multiple North Stars (one primary goal only)
- Skip SMART validation

## Goal Examples

**Good North Star Goals**:
- ✅ "Build production-ready e-commerce platform with payment processing"
- ✅ "Deploy secure REST API with OAuth2 authentication"
- ✅ "Create mobile app with offline-first architecture"
- ✅ "Implement real-time chat system supporting 10K concurrent users"

**Poor North Star Goals**:
- ❌ "Make website" (too vague)
- ❌ "Fix bugs" (not strategic)
- ❌ "Improve performance and add features and refactor code" (too broad, multiple goals)
- ❌ "Build the next Facebook" (not achievable)

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📚 **Goal Setting Patterns**: [resources/GOAL_PATTERNS.md](./resources/GOAL_PATTERNS.md)

---

**Shannon V4** - North Star Management 🎯
