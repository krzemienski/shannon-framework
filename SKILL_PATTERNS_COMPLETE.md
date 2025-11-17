# Shannon Skill Patterns - Complete Reference

**Purpose**: Extract every pattern needed to build intelligent-do skill

---

## 1. Universal Skill Structure

### 1.1 YAML Frontmatter Pattern

```yaml
---
name: skill-name                    # Lowercase, hyphens only
description: |
  Multi-line description
  When to use: [conditions]

skill-type: QUANTITATIVE | PROTOCOL | ORCHESTRATION
shannon-version: ">=5.0.0"
complexity-triggers: [0.50-1.00]    # Optional, for QUANTITATIVE

mcp-requirements:
  required:
    - name: serena
      purpose: Context preservation
      fallback: ERROR or local-storage
      degradation: critical or medium
  recommended:
    - name: sequential
      purpose: Deep thinking
      fallback: native-thinking
      trigger: complexity >= 0.60

required-sub-skills:
  - dependency-skill-1
  - dependency-skill-2

optional-sub-skills:
  - enhancement-skill-1

allowed-tools: [Read, Write, Bash, Serena, Sequential, TodoWrite]
---
```

### 1.2 Markdown Content Pattern

```markdown
# Skill Name

## Purpose
One-paragraph summary of what skill does and key innovation

## When to Use
### MANDATORY when:
- Condition 1
- Condition 2

### RECOMMENDED when:
- Condition A

### DO NOT USE when:
- Condition X

## Anti-Rationalization
[Common rationalizations agents make under pressure]

## Iron Laws
[Non-negotiable rules even under deadline/authority pressure]

## Workflow
### Step 1: [Name] (Duration)
**Action**: What to do
**Purpose**: Why
**Output**: What's produced

### Step 2: [Name] (Duration)
...

## Examples
### Example 1: [Simple Case]
**Input**: ...
**Execution**: ...
**Output**: ...

## Success Criteria
- ✅ Check 1
- ✅ Check 2

## Common Pitfalls
### Pitfall 1: [Name]
**Problem**: What goes wrong
**Why It Fails**: Root cause
**Solution**: How to fix

## Integration
- **With skill-x**: How they connect
- **With MCP-y**: How MCP is used

## References
- Full algorithm: references/DETAILED_ALGO.md
- Templates: templates/output.md
```

---

## 2. Skill Type Patterns

### 2.1 PROTOCOL Skills (Orchestration)

**Examples**: exec, task-automation, wave-orchestration

**Characteristics**:
- Coordinate other skills/commands
- Define execution sequences
- Handle error recovery
- Provide user interaction points

**Pattern**:
```markdown
## Workflow
Phase 1: Preparation
→ SlashCommand("/shannon:prime")
→ Verify prerequisites

Phase 2: Analysis
→ @skill spec-analysis
    specification: {user_input}

Phase 3: Execution
→ IF condition: @skill execution-skill
    parameter: value

Phase 4: Validation
→ Check results
→ Report to user

Phase 5: Completion
→ Summary
→ Save to Serena
```

**Serena Usage**:
```javascript
// Save workflow state
write_memory("workflow_state_{name}", {
  current_phase: N,
  completed_steps: [...],
  next_actions: [...]
})

// Load context
read_memory("previous_workflow_result")
```

### 2.2 QUANTITATIVE Skills (Analysis)

**Example**: spec-analysis

**Characteristics**:
- Produce numeric scores (0.0-1.0)
- Use deterministic algorithms
- Provide interpretation bands
- Generate recommendations based on scores

**Pattern**:
```markdown
## Scoring Algorithm

### Dimension 1: Name (Weight%)
```python
score = calculate_dimension_1(input)
# Formula: specific calculation
# Range: 0.0-1.0
# Examples: score=0.50 means X
```

### Dimension 2: Name (Weight%)
...

### Weighted Total:
```python
total = (weight1 × dim1) + (weight2 × dim2) + ...
interpretation = map_to_band(total)
```

## Interpretation Bands:
- 0.00-0.30: Simple (1-2 agents, hours)
- 0.30-0.50: Moderate (2-3 agents, days)
- 0.50-0.70: Complex (3-7 agents, days)
- 0.70-0.85: High (8-15 agents, weeks)
- 0.85-1.00: Critical (15-25 agents, weeks)
```

### 2.3 ORCHESTRATION Skills (Parallel Execution)

**Example**: wave-orchestration

**Characteristics**:
- Manage parallel agent execution
- Handle dependency graphs
- Create synthesis checkpoints
- Track performance metrics

**Pattern**:
```markdown
## True Parallelism (CRITICAL)

<!-- CORRECT: All agents in ONE message -->
<function_calls>
  <invoke name="Task"><parameter name="prompt">Agent 1</parameter></invoke>
  <invoke name="Task"><parameter name="prompt">Agent 2</parameter></invoke>
  <invoke name="Task"><parameter name="prompt">Agent 3</parameter></invoke>
</function_calls>

## Context Loading (MANDATORY for every agent)

Every agent prompt MUST include:
1. list_memories()
2. read_memory("context_key_1")
3. read_memory("context_key_2")
...
Your task: [specific instructions]

## Synthesis Checkpoint (After EVERY wave)

1. Collect all agent results
2. Aggregate deliverables
3. Cross-validate (no conflicts, gaps, duplicates)
4. Create synthesis document
5. Present to user
6. Wait for approval
```

---

## 3. Skill Invocation Patterns

### 3.1 From Skill to Skill

```markdown
@skill target-skill-name
  parameter1: value1
  parameter2: value2
  parameter3: |
    Multi-line
    value
```

**Example from exec**:
```markdown
@skill wave-orchestration
  task: {step.description}
  enhanced_context: |
    RECOMMENDED LIBRARIES: {libraries}
    CRITICAL INSTRUCTIONS:
    - Use recommended libraries
    - Make minimal changes
    - Follow project conventions
```

### 3.2 From Skill to Command

```markdown
SlashCommand("/shannon:command \"argument\" --flag")
```

**Example from task-automation**:
```markdown
SlashCommand("/shannon:prime")
SlashCommand("/shannon:spec \"[specification]\" --save")
SlashCommand("/shannon:wave")
```

### 3.3 From Skill to MCP

```javascript
// Serena MCP
write_memory("key", {data: "value"})
read_memory("key")
list_memories()

// Sequential MCP
@mcp sequential-thinking
  task: Break down complex problem
  context: Available information
  format: Structured output

// Other MCPs
@mcp firecrawl
  search: "solution to problem"
```

---

## 4. Serena MCP Patterns (CRITICAL)

### 4.1 Memory Key Naming Convention

```
{domain}_{type}_{identifier}

Examples:
spec_analysis_20250103_143022          # Analysis result
wave_1_complete                         # Wave synthesis
wave_2_backend_builder_results         # Agent result
library_cache_authentication           # Cached discovery
exec_result_20250103_150000            # Execution report
checkpoint_pre_wave_3                  # Manual checkpoint
shannon_precompact_checkpoint_20250103 # Auto checkpoint
shannon_latest_checkpoint              # Pointer
```

### 4.2 Save Analysis Pattern

```javascript
const analysis_id = `spec_analysis_${timestamp}`

write_memory(analysis_id, {
  analysis_type: "spec-analysis",
  timestamp: "2025-01-03T14:30:22Z",
  complexity_score: 0.68,
  domain_percentages: {
    Frontend: 34,
    Backend: 29,
    Database: 20,
    DevOps: 17
  },
  mcp_recommendations: [...],
  phase_plan: [...],
  execution_strategy: "wave-based",
  timeline_estimate: "10-12 days"
})

// Verify save
const verify = read_memory(analysis_id)
if (!verify) throw Error("Serena save failed")
```

### 4.3 Context Loading Pattern

```javascript
// Discover available context
list_memories()

// Load systematic context
const spec = read_memory("spec_analysis")
const plan = read_memory("phase_plan_detailed")
const architecture = read_memory("architecture_complete")

// Load previous wave results
for (let i = 1; i < current_wave; i++) {
  const wave_result = read_memory(`wave_${i}_complete`)
  if (wave_result) {
    // Use context
  }
}
```

### 4.4 Checkpoint Pattern

```javascript
// Create checkpoint
write_memory("checkpoint_pre_wave_3", {
  checkpoint_type: "manual",
  timestamp: "2025-01-03T15:00:00Z",
  wave_state: {
    current_wave: 3,
    completed_waves: [1, 2],
    wave_progress: "ready_to_start"
  },
  todo_state: {
    active_todos: [...],
    completed_todos: [...]
  },
  serena_memory_keys: [
    "spec_analysis",
    "wave_1_complete",
    "wave_2_complete"
  ],
  decisions_made: [...],
  integration_status: {...},
  next_steps: [...]
})

// Update latest pointer
write_memory("shannon_latest_checkpoint", {
  checkpoint_key: "checkpoint_pre_wave_3",
  timestamp: "2025-01-03T15:00:00Z",
  type: "manual"
})
```

### 4.5 Library Cache Pattern

```javascript
// Cache discovered libraries (7-day TTL)
write_memory("library_cache_authentication", {
  feature: "authentication",
  cached_at: "2025-01-03T14:00:00Z",
  expires_at: "2025-01-10T14:00:00Z",
  libraries: [
    {
      name: "next-auth",
      score: 95.0,
      why_recommended: "15k+ stars, maintained 4 days ago",
      install_command: "npm install next-auth",
      category: "auth"
    }
  ]
})

// Check cache before re-discovery
const cached = read_memory("library_cache_authentication")
if (cached && Date.now() < cached.expires_at) {
  // Use cached
} else {
  // Re-discover
}
```

---

## 5. TodoWrite Pattern

### 5.1 Create Todo List

```javascript
TodoWrite([
  {
    content: "Phase 1: Context Preparation",
    status: "in_progress",
    activeForm: "Preparing context"
  },
  {
    content: "Phase 2: Library Discovery",
    status: "pending",
    activeForm: "Discovering libraries"
  },
  {
    content: "Phase 3: Task Analysis",
    status: "pending",
    activeForm: "Analyzing task"
  },
  {
    content: "Phase 4: Execution Planning",
    status: "pending",
    activeForm: "Planning execution"
  },
  {
    content: "Phase 5: Execute Steps",
    status: "pending",
    activeForm: "Executing steps"
  },
  {
    content: "Phase 6: Generate Report",
    status: "pending",
    activeForm: "Generating report"
  }
])
```

### 5.2 Update Todo Status

```javascript
// Mark phase 1 complete, phase 2 in progress
TodoWrite([
  {
    content: "Phase 1: Context Preparation",
    status: "completed",
    activeForm: "Prepared context"
  },
  {
    content: "Phase 2: Library Discovery",
    status: "in_progress",
    activeForm: "Discovering libraries"
  },
  {
    content: "Phase 3: Task Analysis",
    status: "pending",
    activeForm: "Analyzing task"
  }
  // ... rest
])
```

### 5.3 Todo Granularity

**For multi-step workflows**:
- One todo per major phase
- Update as phases complete

**For simple tasks**:
- Skip TodoWrite (overhead not justified)

---

## 6. Validation Patterns

### 6.1 3-Tier Validation (from exec)

```bash
# Tier 1: Static validation (10s)
shannon validate --tier 1 --json

# Expected output:
{
  "tier1_passed": true,
  "build": "PASS",
  "typecheck": "PASS",
  "lint": "PASS"
}

# Tier 2: Tests (1-5min)
shannon validate --tier 2 --json

# Expected output:
{
  "tier2_passed": true,
  "tests_passed": 12,
  "tests_failed": 0,
  "test_details": [...]
}

# Tier 3: Functional (2-10min)
shannon validate --tier 3 --json

# Expected output:
{
  "tier3_passed": true,
  "functional_test": "Feature works in browser",
  "details": "..."
}
```

### 6.2 Validation Decision Tree

```
IF tier1_passed AND tier2_passed AND tier3_passed:
    → shannon git-commit (atomic commit)
    → Proceed to next step

ELSE IF any tier failed:
    → shannon git-rollback
    → Research solution (if research enabled)
    → Retry (attempt N of 3)

IF all attempts failed:
    → Document failure
    → Return partial results
    → Recommend manual intervention
```

---

## 7. Git Automation Patterns

### 7.1 Atomic Commit Pattern

```bash
shannon git-commit \
  --step "Add authentication feature" \
  --files "package.json,src/auth/login.tsx,src/auth/middleware.ts" \
  --validation-json '{"tier1_passed": true, "tier2_passed": true, "tier3_passed": true}'
```

**Commit Message Generated**:
```
feat: Add authentication feature

VALIDATION:
- Build: PASS
- Tests: 12/12 PASS
- Functional: Feature works in browser

Files: package.json, src/auth/login.tsx, src/auth/middleware.ts
```

### 7.2 Rollback Pattern

```bash
shannon git-rollback
```

**Behavior**:
- Reverts to last validated commit
- Clears working directory
- Preserves git history

---

## 8. Error Handling Patterns

### 8.1 Graceful Error Pattern

```markdown
## Error Handling Protocol

IF error_type == "validation_failed":
    1. Display validation failures
    2. Offer options:
       - Retry (with adjustments)
       - Skip step (if non-critical)
       - Abort (with summary)
    3. Handle user choice

IF error_type == "mcp_unavailable":
    IF mcp_tier == "required":
        ERROR: Cannot continue without {mcp}
        Suggest: Install MCP, check configuration
    ELSE:
        WARN: {mcp} unavailable, functionality degraded
        Continue: With fallback

IF error_type == "wave_failed":
    1. Display wave error
    2. Offer options:
       - Retry wave
       - Skip wave (if possible)
       - Rollback to previous wave
       - Abort execution
    3. Handle user choice
```

### 8.2 Recovery Pattern

```markdown
## Recovery Protocol

Step 1: Identify error type and severity

Step 2: Attempt automatic recovery:
  - Validation failed → Research + Retry (max 3)
  - MCP unavailable → Fallback or degrade
  - Timeout → Resume from checkpoint

Step 3: If automatic recovery fails:
  - Present clear error message
  - Show recovery options
  - Let user decide
  - Never silently fail

Step 4: Document failure in Serena:
write_memory("error_log_{timestamp}", {
  error_type: "...",
  error_message: "...",
  attempted_recovery: [...],
  final_state: "..."
})
```

---

## 9. User Interaction Patterns

### 9.1 Decision Point Pattern

```markdown
## User Decision Point

Present situation:
- Current state
- Available options
- Recommended option

Ask user:
```
Continue with {recommended}?
1. Yes (execute recommended)
2. Alternative A
3. Alternative B
4. Abort

Choice:
```

Handle response:
- 1/yes → Proceed with recommended
- 2 → Execute alternative A
- 3 → Execute alternative B
- 4/abort → Exit gracefully

With --auto flag: Skip prompt, execute recommended
```

### 9.2 Approval Gate Pattern

```markdown
## Approval Gate (Iron Law)

After completing wave {N}:

1. Present synthesis:
   - Agents deployed: {count}
   - Execution time: {duration}
   - Deliverables: {list}
   - Decisions made: {summary}
   - Quality checks: {status}

2. Wait for explicit approval:
   "Wave {N} approved" or "Continue"

3. Only proceed after approval

4. No bypass even under:
   - Deadline pressure
   - CEO authority
   - "Trust me" requests

5. If approval denied:
   - Investigate issues
   - Iterate if needed
   - Re-present for approval
```

---

## 10. Iron Laws Pattern (Non-Negotiable)

### 10.1 Structure

```markdown
## Iron Laws (Non-Negotiable Even Under Pressure)

These rules CANNOT be violated even under:
- ✋ CEO/executive authority
- ✋ Critical deadlines
- ✋ "Trust me, I'm experienced"
- ✋ Time pressure
- ✋ Budget constraints

### Iron Law 1: [Name]

**Rule**: Clear statement of rule

**Cannot be skipped for**:
- Urgent deadlines
- Authority demands
- Time pressure

**Rationale**: Why this is non-negotiable

**If user insists on skipping**:
```
"I cannot skip [Iron Law X] even under [pressure type].

Rationale: [Why rule exists]

Impact of skipping: [Consequences]

Alternative: [What I can do instead]"
```

### Iron Law 2: [Name]
...
```

### 10.2 Authority Resistance Protocol

```markdown
When authority figure demands violation of Iron Law:

Step 1: Acknowledge Authority
"I understand you're [CEO/manager] and have authority."

Step 2: Explain Iron Law
"However, [Iron Law X] is non-negotiable because [rationale]."

Step 3: Present Data
"Let me show you the impact:
- Your approach: [outcome]
- Shannon approach: [outcome]
- Difference: [quantitative impact]"

Step 4: Calculate Opportunity Cost
"Proceeding without [Iron Law X]:
- Time cost: +[X hours]
- Risk: [specific failure mode]"

Step 5: Offer Compromise
"I can [alternative] while [addressing concern]."

Step 6: Document Override (If Insisted)
"I'll document this decision:
- Overridden: [Iron Law X]
- Rationale: [Authority decision]
- Expected impact: [consequences]
- Risk: [failure modes]
Proceeding with your approach..."

Step 7: Warn About Timeline Impact
"Warning: This will likely add [X hours] to timeline."
```

---

## 11. Anti-Rationalization Pattern

### 11.1 Structure

```markdown
## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically rationalize away [correct behavior] under pressure.

### Rationalization 1: "[Agent's typical rationalization]"
**Example**: User says "[trigger]" → Agent responds "[rationalized response]"

**COUNTER**:
- ❌ **NEVER** [what not to do]
- ✅ [What to do instead]
- ✅ [Why it matters]
- ✅ [How to do it correctly]

**Rule**: [One-line rule to follow]

### Rationalization 2: "[Another common rationalization]"
...

### Detection Signal
**If you're tempted to**:
- [Temptation 1]
- [Temptation 2]
- [Temptation 3]

**Then you are rationalizing.** Stop. [Correct action].
```

---

## 12. Synthesis Patterns (Wave Orchestration)

### 12.1 Wave Synthesis Protocol

```markdown
## Wave Synthesis Protocol (MANDATORY after EVERY wave)

### Step 1: Collect All Agent Results
```javascript
const results = []
for (const agent of wave_agents) {
  const result = read_memory(`wave_${N}_${agent.type}_results`)
  results.push(result)
}

// Verify all completed
if (results.some(r => r.status !== "completed")) {
  ERROR: "Agent failures detected"
}
```

### Step 2: Aggregate Deliverables
```javascript
const deliverables = {
  files_created: merge_all(results.map(r => r.files_created)),
  components_built: list_all(results.map(r => r.components)),
  decisions_made: compile_all(results.map(r => r.decisions)),
  tests_created: sum(results.map(r => r.test_count))
}
```

### Step 3: Cross-Validate Results
Quality Checks:
☐ Conflicting Implementations (check for contradictions)
☐ Missing Integrations (check for connection gaps)
☐ Duplicate Work (check for redundancy)
☐ Incomplete Deliverables (check for missing work)
☐ Test Coverage (check all components tested)
☐ NO MOCKS Compliance (verify functional tests only)

### Step 4: Create Wave Synthesis Document
```javascript
write_memory(`wave_${N}_complete`, {
  wave_number: N,
  wave_name: "Wave N: Description",
  agents_deployed: count,
  execution_time_minutes: actual_time,
  parallel_efficiency: speedup_calculation,
  deliverables: {...},
  decisions: [...],
  integration_status: {...},
  quality_metrics: {...},
  next_wave_context: {...}
})
```

### Step 5: Present Synthesis to User
Show:
- Execution summary (performance, deliverables)
- Key accomplishments
- Important decisions
- Integration status
- Quality validation
- Next wave requirements

### Step 6: Wait for User Approval
User must explicitly approve before next wave
Options: "approved", feedback for iteration, report issues
```

---

## 13. Complete Example: Building a New Skill

### 13.1 intelligent-do Skill Template

```yaml
---
name: intelligent-do
description: |
  Intelligent task execution with context awareness and auto-exploration.
  Analyzes user intent, explores codebase, discovers libraries, validates
  functionally, commits atomically. Use when: user says "do X" without
  detailed specification.

skill-type: PROTOCOL
shannon-version: ">=5.1.0"

mcp-requirements:
  required:
    - name: serena
      purpose: Context storage, library cache, decision history
      fallback: ERROR
      degradation: critical
  recommended:
    - name: sequential
      purpose: Intent analysis, exploration planning
      fallback: native-thinking
      trigger: intent_ambiguous OR complexity >= 0.50

required-sub-skills:
  - exec
  - spec-analysis

optional-sub-skills:
  - wave-orchestration
  - context-preservation

allowed-tools: [Bash, Read, Write, Grep, Glob, Serena, Sequential, TodoWrite]
---

# Intelligent Do Skill

## Purpose
Execute tasks intelligently with minimal specification by analyzing intent, exploring existing codebase context, discovering optimal libraries, and delivering validated, committed implementations autonomously.

**Key Innovation**: Transforms "do authentication" → complete spec analysis → library discovery → implementation → validation → commit, all from 2-word intent.

## When to Use

### MANDATORY when:
- User provides task intent without full specification ("do authentication", "add dashboard")
- Need intelligent context discovery from existing codebase
- Want autonomous execution with validation

### RECOMMENDED when:
- Working in established codebase (patterns exist to discover)
- Task requires library selection (auto-discovery beneficial)
- User wants minimal friction execution

### DO NOT USE when:
- User provides complete, detailed specification (use exec directly)
- Task requires extensive design discussion (use spec-analysis + wave)
- Greenfield project with no existing context (no patterns to discover)

## Anti-Rationalization

### Rationalization 1: "Intent is obvious, skip analysis"
**Example**: User says "do login" → Agent assumes authentication without analysis

**COUNTER**:
- ❌ **NEVER** assume intent without analysis
- ✅ "Login" could mean: authentication, login form UI, SSO integration, password reset, etc.
- ✅ ALWAYS run intent analysis with Sequential MCP
- ✅ If ambiguous, ask clarifying questions

**Rule**: Always analyze intent, even for "obvious" tasks

### Rationalization 2: "Skip codebase exploration, start coding"
**Example**: Agent jumps to implementation without checking existing patterns

**COUNTER**:
- ❌ **NEVER** skip codebase exploration
- ✅ Existing patterns MUST inform new implementations
- ✅ Discovery takes 2-5 min, prevents hours of rework
- ✅ Use Glob + Grep + Read to build context map

**Rule**: Explore first, code second

### Rationalization 3: "Simple task, use direct execution"
**Example**: User says "do navbar" → Agent codes directly without spec

**COUNTER**:
- ❌ **NEVER** skip spec synthesis
- ✅ Even "simple" tasks need complexity assessment
- ✅ Spec determines: libraries needed, wave count, timeline
- ✅ Synthesis takes 30s-2min, ensures quality

**Rule**: Always synthesize spec from intent + context

## Iron Laws

### Iron Law 1: Intent Analysis MUST Complete Before Exploration

**Rule**: Cannot begin codebase exploration until intent is fully analyzed and clarified

**Rationale**: Exploring without clear intent wastes time searching irrelevant patterns

**If tempted to skip**:
```
"I must analyze your intent before exploring the codebase.

Your request: '{user_intent}'

Clarifying questions:
1. [Question about scope]
2. [Question about approach]
3. [Question about integration]

Or I can analyze with Sequential MCP and present interpretation for approval."
```

### Iron Law 2: Spec MUST Be Synthesized Before Execution

**Rule**: Cannot invoke exec without synthesized specification (even if intent seems simple)

**Rationale**: exec requires clear spec for library discovery, wave planning, validation

**If tempted to skip**:
```
"I cannot execute without a specification.

I'll synthesize one from:
- Your intent: '{intent}'
- Discovered context: {context_summary}
- Existing patterns: {patterns}

Synthesized spec ready for /shannon:spec analysis."
```

### Iron Law 3: User Approval Required After Synthesis

**Rule**: Must present synthesized spec + complexity + plan for user approval before execution

**Rationale**: User may have different interpretation, prevents wasted execution

**Approval Gate**:
```
📊 Synthesized Specification

**Your Intent**: {original_intent}
**Interpreted As**: {interpretation}
**Complexity**: {score} ({label})
**Approach**: {strategy}
**Estimated**: {timeline}

Proceed with this interpretation? (yes/revise/abort)
```

## Workflow

### Phase 1: Intent Analysis (1-2 min)

**Action**: Analyze user's "do X" command

**Process**:
```javascript
// Use Sequential MCP for deep analysis
@mcp sequential-thinking
  task: Analyze intent "{user_input}"
  context: User in codebase, previous tasks from Serena
  output: {
    primary_intent: "...",
    scope: "feature|enhancement|fix|refactor",
    domains: ["Frontend", "Backend", ...],
    ambiguities: [...],
    clarifying_questions: [...]
  }

// If ambiguities exist
if (analysis.ambiguities.length > 0) {
  ask_user(analysis.clarifying_questions)
  re_analyze_with_answers()
}
```

**Output**: Clear intent with scope, domains, no ambiguities

### Phase 2: Context Discovery (2-5 min)

**Action**: Explore codebase for relevant patterns

**Process**:
```javascript
TodoWrite([
  {content: "Discover file structure", status: "in_progress", activeForm: "Discovering files"},
  {content: "Find similar implementations", status: "pending", activeForm: "Finding patterns"},
  {content: "Extract key patterns", status: "pending", activeForm: "Extracting patterns"}
])

// Step 1: Discover file structure
const files = Glob("**/*.{js,jsx,ts,tsx,py,go,rs}")

// Step 2: Find similar implementations
const similar = Grep(pattern="{intent_keywords}", output_mode="files_with_matches")

// Step 3: Read key files
const patterns = []
for (const file of similar.slice(0, 5)) {
  const content = Read(file)
  patterns.push(extract_patterns(content))
}

// Step 4: Search Serena for previous decisions
const previous_decisions = search_nodes({query: "{intent_keywords}"})

// Step 5: Build context map
const context_map = {
  file_structure: analyze_structure(files),
  similar_implementations: similar,
  key_patterns: patterns,
  previous_decisions: previous_decisions,
  dependencies: extract_dependencies(),
  conventions: extract_conventions(patterns)
}

// Save to Serena
write_memory("intelligent_do_context_map", context_map)
```

**Output**: Complete context map with patterns, conventions, decisions

### Phase 3: Specification Synthesis (30s-2min)

**Action**: Generate full specification from intent + context

**Process**:
```javascript
// Synthesize spec
const spec = `
Build {intent} for {project}

Requirements:
${derive_requirements_from(intent, context_map)}

Technical Approach:
${recommend_approach_from(context_map.patterns)}

Integration Points:
${identify_integration_points(context_map.file_structure)}

Existing Patterns to Follow:
${extract_patterns(context_map.conventions)}

Dependencies:
${context_map.dependencies}

Validation Requirements:
- Functional tests (NO MOCKS)
-