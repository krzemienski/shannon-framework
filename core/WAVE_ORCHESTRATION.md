---
name: WAVE_ORCHESTRATION
description: Behavioral instructions for parallel sub-agent wave execution with context sharing and synthesis
category: core-behavioral
priority: critical
triggers: [wave, parallel, coordinate, multi-agent, orchestrate]
auto_activate: true
activation_threshold: 0.7
mcp_servers: [serena, sequential]
---

# Wave Orchestration Behavioral Framework

> **Purpose**: Define how Claude orchestrates parallel sub-agent execution through waves, ensuring true parallelism, complete context sharing, and systematic synthesis.

This document provides behavioral instructions for coordinating multiple sub-agents working simultaneously across multiple execution waves. It ensures zero duplicate work, perfect context continuity, and measurably faster execution through genuine parallelism.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Wave Execution Patterns](#wave-execution-patterns)
3. [Agent Spawning Logic](#agent-spawning-logic)
4. [Context Sharing via Serena](#context-sharing-via-serena)
5. [Wave Synthesis](#wave-synthesis)
6. [Dependency Management](#dependency-management)
7. [Wave Size Optimization](#wave-size-optimization)
8. [Error Recovery](#error-recovery)
9. [Performance Optimization](#performance-optimization)

---

## 1. Core Principles

### Principle 1: True Parallelism

**MANDATORY RULE**: To achieve genuine parallel execution, spawn ALL wave agents in ONE message.

**Correct Pattern** (DO THIS):
```
ONE MESSAGE containing multiple Task invocations:
<function_calls>
  <invoke name="Task">...</invoke>
  <invoke name="Task">...</invoke>
  <invoke name="Task">...</invoke>
</function_calls>

Result: All agents execute simultaneously
Speedup: max(agent_times) not sum(agent_times)
```

**Incorrect Pattern** (NEVER DO THIS):
```
MULTIPLE MESSAGES:
Message 1: <invoke name="Task">...</invoke>
Wait for completion...
Message 2: <invoke name="Task">...</invoke>
Wait for completion...

Result: Sequential execution disguised as parallel
Speedup: NONE - same as doing tasks one by one
```

**Why This Matters**:
- Single message = Claude Code executes all agents at same time
- Multiple messages = Claude Code executes agents one after another
- Parallel efficiency is measured: 3 agents in 10 minutes > 30 minutes sequential

### Principle 2: Context Preservation

**MANDATORY RULE**: EVERY sub-agent in EVERY wave MUST load ALL previous wave context.

**Context Loading Protocol**:
```markdown
EVERY agent prompt MUST include:

MANDATORY CONTEXT LOADING PROTOCOL:
Execute these commands BEFORE your task:
1. list_memories() - discover all available Serena memories
2. read_memory("spec_analysis") - understand project requirements
3. read_memory("phase_plan_detailed") - know execution structure
4. read_memory("architecture_complete") if exists - understand system design
5. read_memory("wave_1_complete") if exists - learn from Wave 1
6. read_memory("wave_2_complete") if exists - learn from Wave 2
... (read all previous waves)
7. read_memory("wave_[N-1]_complete") - immediate previous wave

Verify you understand:
✓ What we're building (from spec_analysis)
✓ How it's designed (from architecture_complete)
✓ What's been built (from previous waves)
✓ Your specific task (detailed below)
```

**Effect**:
- Wave 3 agents know everything from Waves 1 and 2
- No duplicate analysis
- No missed decisions
- No conflicting implementations
- Perfect continuity

### Principle 3: Wave Synthesis

**MANDATORY RULE**: After each wave completes, synthesize ALL agent results before next wave.

**Synthesis Process**:
```
1. All wave agents complete and return results
2. Coordinator reads ALL agent results from Serena
3. Coordinator combines results into coherent synthesis
4. Coordinator saves synthesis: write_memory("wave_[N]_complete", synthesis)
5. Coordinator presents synthesis to user for validation
6. Coordinator WAITS for user approval before next wave
```

**Why This Matters**:
- User maintains control and visibility
- Issues caught early between waves
- Context for next wave is clean and validated
- Prevents cascading errors from bad decisions

### Principle 4: Dependency Management

**MANDATORY RULE**: Respect wave dependencies - don't spawn dependent waves until prerequisites complete.

**Dependency Logic**:
```
IF wave has dependencies:
  Check if prerequisite waves are complete
  Read prerequisite wave results from Serena
  Verify prerequisite deliverables exist
  THEN spawn dependent wave with full context

IF wave has no dependencies:
  Spawn immediately
  Can parallel with other independent waves

IF wave has partial dependencies:
  Split into sub-waves
  First sub-wave: independent tasks
  Second sub-wave: dependent tasks
```

**Example**:
```
Wave 2a: [React UI, Express API, Database] - all depend only on architecture (PARALLEL)
Wave 2b: [State Mgmt, WebSocket, Auth] - depend on Wave 2a (PARALLEL internally)
Wave 2c: [Puppeteer Tests] - depend on Wave 2a + 2b
Wave 3: [Integration Tests] - depend on ALL above

Execution Order:
1. Spawn Wave 2a (3 agents in ONE message)
2. Wait for Wave 2a completion + synthesis + validation
3. Spawn Wave 2b (3 agents in ONE message)
4. Wait for Wave 2b completion + synthesis + validation
5. Spawn Wave 2c (1 agent)
6. Wait for Wave 2c completion + synthesis + validation
7. Spawn Wave 3 (1 agent)
8. Complete
```

---

## 2. Wave Execution Patterns

### Pattern 1: Independent Parallel Wave

**When to Use**: Multiple tasks with same prerequisites and no inter-dependencies.

**Characteristics**:
- All agents can start simultaneously
- No agent needs results from another agent in same wave
- Maximum parallelization opportunity
- Fastest execution pattern

**Example**:
```
Wave 2a: Frontend + Backend + Database
├─ Agent 1: Build React UI components (reads: architecture_complete)
├─ Agent 2: Build Express API endpoints (reads: architecture_complete)
└─ Agent 3: Create database schema (reads: architecture_complete)

All agents:
- Read same prerequisite (architecture_complete)
- Work on independent components
- Save results independently
- Complete in parallel
```

**Spawning Template**:
```markdown
## Spawning Wave 2a: Core Implementation (Independent Parallel)

**Wave Configuration**:
- Type: Fully Parallel
- Agents: 3
- Dependencies: architecture_complete only
- Estimated Duration: max(agent_times) = 15 minutes

**Spawning 3 agents in ONE message**:

<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">frontend-builder</parameter>
    <parameter name="description">Build React UI components</parameter>
    <parameter name="prompt">
[Full agent prompt with context loading protocol]
YOUR TASK: Build TaskCard, TaskList, TaskForm components
[...complete instructions...]
SAVE: write_memory("wave_2a_frontend_results", {...})
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">backend-builder</parameter>
    <parameter name="description">Build Express API endpoints</parameter>
    <parameter name="prompt">
[Full agent prompt with context loading protocol]
YOUR TASK: Implement /api/tasks CRUD endpoints
[...complete instructions...]
SAVE: write_memory("wave_2a_backend_results", {...})
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">database-builder</parameter>
    <parameter name="description">Create PostgreSQL schema</parameter>
    <parameter name="prompt">
[Full agent prompt with context loading protocol]
YOUR TASK: Create tasks, users, sessions tables
[...complete instructions...]
SAVE: write_memory("wave_2a_database_results", {...})
    </parameter>
  </invoke>
</function_calls>

**Execution**: All 3 agents run simultaneously
**Expected Completion**: 15 minutes (not 45 minutes sequential)
```

### Pattern 2: Dependent Sequential Wave

**When to Use**: Task requires outputs from previous task in same logical phase.

**Characteristics**:
- Must execute in order
- Each agent reads previous agent's results
- No parallelization possible within wave
- Slower but necessary for dependencies

**Example**:
```
Wave 2b-sequential: State Management → Testing
├─ Agent 1: Implement state management (reads: wave_2a_frontend_results)
│   └─ Saves: wave_2b_state_results
└─ Agent 2: Create Puppeteer tests (reads: wave_2a_frontend_results + wave_2b_state_results)
    └─ Saves: wave_2b_testing_results

Execution:
Message 1: Spawn Agent 1, wait for completion
Message 2: Spawn Agent 2 (now has Agent 1 results), wait for completion
```

**When to Use Sequential Within Phase**:
- Component B needs Component A's interface definitions
- Testing needs implementation to exist first
- Integration needs all components built
- Optimization needs baseline to compare against

### Pattern 3: Mixed Parallel-Sequential Wave

**When to Use**: Some tasks are independent, others have dependencies.

**Strategy**: Split into sub-waves with parallel execution where possible.

**Example**:
```
Wave 2b: Post-Core Implementation
├─ Sub-wave 2b-parallel: [State Mgmt, WebSocket, Auth]
│   (all read wave_2a_complete, none depend on each other)
└─ Sub-wave 2b-sequential: [Puppeteer Tests]
    (reads wave_2a_complete + wave_2b_parallel results)

Execution:
1. Spawn 3 agents for 2b-parallel (ONE message)
2. Wait for all 3 to complete
3. Synthesize 2b-parallel results
4. Spawn 1 agent for 2b-sequential (ONE message)
5. Wait for completion
6. Synthesize wave_2b_complete
```

### Pattern 4: Incremental Parallel Wave

**When to Use**: Large number of similar tasks that can be batched.

**Strategy**: Divide into multiple smaller parallel waves for manageability.

**Example**:
```
Wave 3: Build 20 UI Components

Instead of spawning 20 agents at once:
├─ Wave 3a: Components 1-5 (5 agents, ONE message)
├─ Wave 3b: Components 6-10 (5 agents, ONE message)
├─ Wave 3c: Components 11-15 (5 agents, ONE message)
└─ Wave 3d: Components 16-20 (5 agents, ONE message)

Benefits:
- More manageable synthesis
- Token usage spread across waves
- Can course-correct between batches
- Still parallel within each batch
```

---

## 3. Agent Spawning Logic

### Pre-Spawn Checklist

**MANDATORY** before spawning ANY wave:

```markdown
☐ 1. Load wave execution plan
   read_memory("wave_execution_plan")

☐ 2. Verify this is the correct wave to execute next
   Check: Is this the next wave in sequence?
   Check: Are we in the right phase?

☐ 3. Verify prerequisites complete
   Check: Do prerequisite waves have _complete memories?
   Check: Are all expected deliverables present?

☐ 4. Load all previous wave contexts
   read_memory("wave_1_complete") if exists
   read_memory("wave_2_complete") if exists
   ... (all previous waves)

☐ 5. Verify MCP servers available
   Check: Serena connected
   Check: Required MCPs active (Magic, Context7, Puppeteer, etc.)

☐ 6. Estimate token usage
   Current tokens + (agents × ~3000 tokens per agent)
   Check: Will this exceed 75% token usage?
   If yes: Create checkpoint first

☐ 7. Prepare agent prompts
   Include context loading protocol in EVERY prompt
   Include specific task instructions
   Include save-to-Serena instructions
```

### Agent Prompt Structure

**Every agent prompt MUST follow this structure**:

```markdown
You are Wave [N], Agent [X]: [Agent Type Name]

## MANDATORY CONTEXT LOADING PROTOCOL
[Standard context loading commands - see Principle 2]

## YOUR TASK
[Specific, detailed task description]

## YOUR TOOLS
[Specific tools this agent should use]
- Read, Write, Edit for file operations
- Bash for running commands
- Magic MCP for UI components (if frontend)
- Context7 MCP for framework patterns
- Puppeteer MCP for functional testing (if testing)

## YOUR APPROACH
[Step-by-step approach tailored to task]
1. [First step]
2. [Second step]
...

## YOUR DELIVERABLES
[Specific files, components, or outputs to produce]
- File: path/to/file.ext
- Component: ComponentName
- Test: path/to/test.ext

## PRODUCTION READY REQUIREMENTS
- NO placeholders ("TODO: implement later")
- NO incomplete functions
- NO stub implementations
- All code must work immediately
- All functions fully implemented

## TESTING REQUIREMENTS (if applicable)
- NO MOCKS (Shannon mandate)
- Use Puppeteer for web
- Use iOS Simulator for iOS
- Use real HTTP for APIs
- Use real database for data tests

## SAVE YOUR WORK
write_memory("wave_[N]_[component]_results", {
  agent_id: "[agent-type]",
  agent_number: [X],
  wave_number: [N],
  task_completed: true,
  files_created: [list all files with paths],
  components_built: [list all components],
  decisions_made: [list key decisions],
  tests_created: [if applicable],
  no_mocks_confirmed: true (if tests),
  issues_encountered: [any problems],
  integration_notes: [how this integrates with other components],
  next_steps: [recommendations for next wave]
})

Memory key: wave_[N]_[component]_results
```

### Spawning Message Template

```markdown
## Spawning Wave [N]: [Wave Name]

**Wave Information**:
- Wave Number: [N]
- Wave Name: [Descriptive name]
- Agents: [count] sub-agents
- Type: Independent Parallel | Dependent Sequential | Mixed
- Dependencies: [List prerequisite waves] or None
- Estimated Duration: [hours/minutes]
- Token Estimate: [tokens]

**Context Setup Complete**:
Loaded from Serena:
✓ spec_analysis
✓ phase_plan_detailed
✓ architecture_complete
✓ wave_1_complete (if exists)
✓ wave_2_complete (if exists)
... (all previous waves)

**Agent Assignments**:
1. [Agent Type 1]: [Brief task description]
   → Deliverable: [What this agent will produce]

2. [Agent Type 2]: [Brief task description]
   → Deliverable: [What this agent will produce]

[... for all agents in wave]

**Spawning [count] agents in PARALLEL** (ONE message):

<function_calls>
  [All agent Task invocations here]
</function_calls>

**Execution**: All [count] agents execute simultaneously
**Expected Duration**: max(agent_times) = [time] minutes
**Next**: Wait for all agents to complete, then synthesize results
```

---

## 4. Context Sharing via Serena

### Serena Memory Structure

**Standard Memory Keys**:

```yaml
Project Context:
  spec_analysis: "8-dimensional spec analysis from /sh:analyze-spec"
  phase_plan_detailed: "5-phase execution plan from /sh:create-waves"
  architecture_complete: "System architecture from Phase 2"
  api_contracts_final: "API endpoint definitions"
  database_schema_final: "Database schema"
  testing_strategy_final: "Testing approach and requirements"

Wave Results:
  wave_1_complete: "Architecture design wave synthesis"
  wave_2a_complete: "Core implementation wave synthesis"
  wave_2b_complete: "Post-core implementation wave synthesis"
  wave_3_complete: "Integration wave synthesis"

Individual Agent Results:
  wave_2a_frontend_results: "Frontend agent specific results"
  wave_2a_backend_results: "Backend agent specific results"
  wave_2a_database_results: "Database agent specific results"

Checkpoints:
  pre_wave_[N]_checkpoint: "Context snapshot before wave N"
  phase_[N]_checkpoint: "Context snapshot at phase transition"
```

### Agent Result Schema

**Every agent saves results in this format**:

```javascript
write_memory("wave_[N]_[component]_results", {
  // Agent Metadata
  agent_id: "frontend-builder",
  agent_number: 1,
  wave_number: 2,
  wave_name: "Core Implementation",
  task_assigned: "Build React UI components",

  // Completion Status
  task_completed: true,
  completion_timestamp: "2024-01-15T14:30:00Z",
  execution_time_minutes: 12,

  // Deliverables
  files_created: [
    "src/components/TaskCard.tsx",
    "src/components/TaskList.tsx",
    "src/components/TaskForm.tsx"
  ],
  total_files: 3,

  components_built: [
    "TaskCard",
    "TaskList",
    "TaskForm"
  ],
  total_components: 3,

  // Decisions
  decisions_made: [
    "Used TypeScript for type safety",
    "Implemented Material-UI components",
    "Added error boundaries for resilience"
  ],

  // Testing
  tests_created: [
    "tests/functional/TaskCard.test.js"
  ],
  test_type: "functional",
  no_mocks_confirmed: true,
  all_tests_pass: true,

  // Integration
  integration_notes: {
    dependencies: ["react", "material-ui"],
    exports: ["TaskCard", "TaskList", "TaskForm"],
    state_management: "Redux toolkit required",
    next_wave_needs: "State management implementation"
  },

  // Issues & Recommendations
  issues_encountered: [
    "Material-UI version mismatch resolved"
  ],
  next_steps: [
    "Connect components to state management",
    "Add Puppeteer tests for user interactions"
  ],

  // Quality
  production_ready: true,
  no_placeholders: true,
  all_functions_implemented: true
})
```

### Context Loading Best Practices

**Progressive Context Loading**:

```markdown
Strategy: Load context in layers based on relevance

Layer 1: ALWAYS LOAD (Universal Context)
- spec_analysis
- phase_plan_detailed
- Previous wave synthesis (wave_[N-1]_complete)

Layer 2: LOAD IF EXISTS (Phase Context)
- architecture_complete (if past Phase 2)
- database_schema_final (if backend task)
- api_contracts_final (if API task)
- testing_strategy_final (if testing task)

Layer 3: LOAD IF NEEDED (Specific Context)
- Individual agent results from current/previous waves
- Only load if agent needs to integrate with specific components

Example:
Agent: state-manager in Wave 2b
Layer 1: spec_analysis, phase_plan_detailed, wave_2a_complete ✓
Layer 2: architecture_complete ✓
Layer 3: wave_2a_frontend_results (needs to know component interfaces) ✓
Layer 3: wave_2a_backend_results (NOT needed) ✗
```

**Verification After Loading**:

```markdown
EVERY agent must verify understanding:

✓ What we're building:
  From spec_analysis: [Summarize in 1 sentence]

✓ How it's designed:
  From architecture_complete: [Key architectural decisions]

✓ What's been built:
  From wave_[N-1]_complete: [Major accomplishments so far]

✓ My specific task:
  [Agent's assigned task]

If ANY verification fails → STOP and request clarification
```

---

## 5. Wave Synthesis

### Post-Wave Synthesis Process

**MANDATORY after EVERY wave completion**:

```markdown
## Wave [N] Synthesis Protocol

### Step 1: Collect All Agent Results

Execute in sequence:
```javascript
results = []
results.push(read_memory("wave_[N]_agent1_results"))
results.push(read_memory("wave_[N]_agent2_results"))
results.push(read_memory("wave_[N]_agent3_results"))
... (for all agents in wave)
```

Verify: All agents completed successfully
If any agent failed: Trigger error recovery (see Section 8)

### Step 2: Aggregate Deliverables

Combine from all agent results:

Files Created:
- Merge all file lists from all agents
- Remove duplicates (if any)
- Organize by type (components, tests, configs)
- Total count: [X] files

Components Built:
- List all components from all agents
- Verify no naming conflicts
- Total count: [Y] components

Decisions Made:
- Compile decision log from all agents
- Identify critical architectural decisions
- Flag any conflicting decisions for resolution

Tests Created:
- Sum test counts from all agents
- Verify: All are functional (NO MOCKS)
- Total count: [Z] tests

### Step 3: Cross-Validate Results

Quality Checks:

☐ Conflicting Implementations
  Check: Do agents' decisions contradict each other?
  Example: Agent 1 uses REST, Agent 2 uses GraphQL
  If found: Document conflict, recommend resolution

☐ Missing Integrations
  Check: Do components connect properly?
  Example: Frontend component expects API endpoint that doesn't exist
  If found: Document gap, recommend fix

☐ Duplicate Work
  Check: Did agents do same thing?
  Example: Both created same utility function
  If found: Document duplication, recommend consolidation

☐ Incomplete Deliverables
  Check: Was planned work not completed?
  Example: Agent was supposed to create 5 files, only created 3
  If found: Document missing work, assess criticality

☐ Test Coverage
  Check: Do all components have functional tests?
  If gaps: Document untested components

☐ NO MOCKS Compliance
  Check: Are all tests functional (no mocking libraries)?
  Verify: No unittest.mock, jest.mock, sinon, Mockito
  If violations: Document non-compliant tests

### Step 4: Create Wave Synthesis Document

write_memory("wave_[N]_complete", {
  // Wave Metadata
  wave_number: N,
  wave_name: "[Name]",
  wave_type: "parallel|sequential|mixed",
  phase_number: [phase],

  // Execution Metrics
  agents_deployed: [count],
  execution_time_minutes: [actual time from timestamps],
  parallel_efficiency: "[speedup calculation]",
  token_usage: [approximate],

  // Deliverables (Aggregated)
  deliverables: {
    files_created: [aggregated list with paths],
    total_files: [count],
    components_built: [list with descriptions],
    total_components: [count],
    tests_created: [count],
    test_type: "functional (NO MOCKS)",
    all_tests_pass: true
  },

  // Decisions (Compiled)
  decisions: [
    "Decision 1: [Description]",
    "Decision 2: [Description]",
    ...
  ],

  // Integration Status
  integration_status: {
    ready_for_next_wave: true|false,
    integration_issues: [
      "Issue 1: [Description and impact]"
    ],
    resolution_recommendations: [
      "Fix 1: [How to resolve Issue 1]"
    ]
  },

  // Quality Metrics
  quality_metrics: {
    code_completeness: "100% (no TODOs or placeholders)",
    production_ready: true,
    test_coverage: "[Z] functional tests created",
    no_mocks_compliance: true,
    conflicts_detected: [count],
    gaps_detected: [count]
  },

  // Context for Next Wave
  next_wave_context: {
    what_next_wave_needs_to_know: [
      "Key fact 1 for next wave",
      "Key fact 2 for next wave"
    ],
    serena_keys_to_read: [
      "wave_[N]_component1_results",
      "wave_[N]_component2_results"
    ],
    dependencies_satisfied: [
      "Dependency 1 now available"
    ]
  },

  // Recommendations
  recommendations: [
    "Recommendation 1 for next wave",
    "Recommendation 2 for overall project"
  ]
})
```

### Step 5: Present Synthesis to User

**User Validation Template**:

```markdown
# Wave [N]: [Wave Name] Complete ✅

## Execution Summary

**Performance**:
- Agents Deployed: [count]
- Execution Time: [minutes] minutes
- Parallel Efficiency: [speedup vs sequential]
  Example: "3 agents × 12 min = 12 min parallel vs 36 min sequential (3× faster)"
- Token Usage: ~[estimate] tokens

**Deliverables**:
- Files Created: [count] files
  [Show first 10, then "... and X more"]
- Components Built: [count] components
  • Component 1: [Brief description]
  • Component 2: [Brief description]
  [... list all components]
- Tests Created: [count] functional tests (NO MOCKS)

## Key Accomplishments

[Bullet list of major achievements this wave]
• Built complete frontend UI with 5 components
• Implemented 8 REST API endpoints
• Created PostgreSQL schema with 4 tables
• Added Puppeteer tests for all user flows

## Important Decisions Made

[Bullet list of critical decisions]
• Decision 1: [What was decided and why]
• Decision 2: [What was decided and why]

## Integration Status

[Assessment of how well components integrate]

✅ **Ready for Next Wave**:
- All components integrate cleanly
- No conflicts detected
- All tests passing

OR

⚠️ **Integration Issues** (if any):
- Issue 1: [Description and impact]
  Fix: [How to resolve]

## Quality Validation

[Quality checklist presentation]
✅ Code Completeness: 100% (no TODOs)
✅ Production Ready: All functions implemented
✅ Test Coverage: [Z] functional tests
✅ NO MOCKS: Confirmed - all functional testing
✅ All Tests Pass: Verified

## Next Wave Requirements

**What Wave [N+1] Needs**:
[List of context and dependencies for next wave]
- Context: Read wave_[N]_complete from Serena
- Dependencies: [List what's now available]
- Recommendations: [What to focus on next]

## Approval Required

Please review the implementation and confirm:

☐ All expected components are present and working
☐ Quality meets your standards
☐ Integration looks correct
☐ Ready to proceed to Wave [N+1]

**Type "approved" to proceed, or provide feedback for iteration.**
```

### Step 6: Handle User Response

**If User Approves**:
```markdown
1. Update todo list:
   TodoWrite: Mark wave [N] tasks as completed ✅

2. Proceed to next wave:
   Check: Is there a Wave [N+1]?
   If yes: Begin next wave spawn process (Section 3)
   If no: Phase complete, proceed to next phase or conclude

3. Maintain momentum:
   User approved → no delays → move to next wave immediately
```

**If User Requests Changes**:
```markdown
1. Acknowledge feedback:
   "Understood. I'll [make requested changes]"

2. Load wave context:
   read_memory("wave_[N]_complete") - understand what was built
   read_memory("wave_[N]_[component]_results") - specific details

3. Make changes:
   Use appropriate tools (Edit, Write, Bash)
   Follow same quality standards

4. Re-test if applicable:
   Run affected functional tests
   Verify: All tests still pass

5. Re-synthesize:
   Update wave_[N]_complete with changes
   Document what was modified

6. Re-validate:
   Present updated results to user
   Request approval again
```

**If User Reports Issues**:
```markdown
1. Investigate:
   Load wave context
   Review agent results
   Identify root cause

2. Classify issue:
   Critical: Blocks next wave → Must fix immediately
   Important: Impacts quality → Should fix before proceeding
   Minor: Can defer → Document for later

3. Resolve or defer:
   If critical: Fix immediately, re-synthesize
   If important: User decides (fix now or later)
   If minor: Add to backlog, proceed
```

---

## 6. Dependency Management

### Dependency Graph Construction

**Algorithm**:

```python
# Phase: Implementation Phase tasks
tasks = [
  {id: 1, name: "React UI", depends_on: ["architecture"]},
  {id: 2, name: "State Mgmt", depends_on: ["React UI"]},
  {id: 3, name: "Puppeteer Tests", depends_on: ["React UI", "State Mgmt"]},
  {id: 4, name: "Express API", depends_on: ["architecture"]},
  {id: 5, name: "Database", depends_on: ["architecture"]},
  {id: 6, name: "WebSocket", depends_on: ["Database"]},
  {id: 7, name: "Auth", depends_on: ["Database"]},
  {id: 8, name: "Integration Tests", depends_on: ["ALL"]}
]

# Build dependency graph
graph = {}
for task in tasks:
  graph[task.id] = {
    "name": task.name,
    "depends_on": task.depends_on,
    "blocks": []
  }

# Calculate which tasks each task blocks
for task in tasks:
  for dep_task in tasks:
    if task.name in dep_task.depends_on:
      graph[task.id].blocks.append(dep_task.id)
```

**Result**:
```
Task 1 (React UI) → blocks [2, 3]
Task 2 (State Mgmt) → blocks [3]
Task 4 (Express API) → blocks [8]
Task 5 (Database) → blocks [6, 7, 8]
Task 6 (WebSocket) → blocks [8]
Task 7 (Auth) → blocks [8]
Task 3, 8 → block nothing (terminal tasks)
```

### Wave Grouping Algorithm

**Algorithm**:

```python
# Group tasks into waves based on dependencies
waves = []
remaining_tasks = tasks.copy()
wave_number = 1

while remaining_tasks:
  # Find tasks with all dependencies satisfied
  ready_tasks = []
  for task in remaining_tasks:
    deps_satisfied = all(
      dep in completed_tasks or dep == "architecture"
      for dep in task.depends_on
    )
    if deps_satisfied:
      ready_tasks.append(task)

  # If no tasks ready, error (circular dependency)
  if not ready_tasks:
    ERROR: "Circular dependency detected"
    break

  # Create wave from ready tasks
  waves.append({
    "wave_number": wave_number,
    "wave_name": f"Wave {wave_number}",
    "tasks": ready_tasks,
    "parallel": True  # All tasks in this wave can run parallel
  })

  # Remove ready tasks from remaining
  for task in ready_tasks:
    remaining_tasks.remove(task)
    completed_tasks.add(task.name)

  wave_number += 1

return waves
```

**Example Output**:
```
Wave 2a: [React UI, Express API, Database]
  Parallel: Yes (all depend only on architecture)
  Agents: 3

Wave 2b: [State Mgmt, WebSocket, Auth]
  Parallel: Yes (depend on different Wave 2a outputs)
  Agents: 3

Wave 2c: [Puppeteer Tests]
  Parallel: N/A (single task)
  Agents: 1

Wave 3: [Integration Tests]
  Parallel: N/A (single task)
  Agents: 1
```

### Dependency Verification Before Spawn

**Pre-Spawn Dependency Check**:

```markdown
Before spawning Wave [N], verify dependencies:

FOR each task in wave:
  FOR each dependency of task:
    Check: Does Serena memory exist?
      Example: "wave_2a_complete" or "architecture_complete"

    If missing:
      ERROR: Cannot spawn wave - dependency not satisfied
      Instruct: Complete prerequisite wave first

    If exists:
      Load dependency context: read_memory("[dependency]_complete")
      Verify deliverables exist:
        Check: Are expected files/components present?
        Check: Is dependency marked as complete?

      If deliverables missing:
        ERROR: Dependency incomplete or corrupted
        Instruct: Re-run or fix dependency wave

All dependencies satisfied → Proceed with spawn
```

### Handling Optional Dependencies

**Pattern**:

```markdown
Some tasks have optional dependencies (can work with or without):

Example:
Task: Implement state management
Required Dependency: React UI components exist
Optional Dependency: API endpoints defined

Approach:
1. Check optional dependency: read_memory("wave_2a_backend_results")
2. If exists: Use real API integration
3. If missing: Use mock data (temporary), document for later integration

Agent prompt includes:
```
Optional Context: read_memory("wave_2a_backend_results") if exists
If backend available: Integrate with real API
If backend missing: Use placeholder data, will integrate in next wave
Document: "Requires backend integration in Wave [X]"
```
```

---

## 7. Wave Size Optimization

### Optimal Wave Size Calculation

**Factors**:

```yaml
Token Budget:
  available_tokens: 200000 (context window)
  current_usage: [check token counter]
  buffer: 20000 (safety margin)
  available: available_tokens - current_usage - buffer

Agent Token Cost:
  average_per_agent: 3000 tokens
  max_agents: available / average_per_agent

Task Complexity:
  simple_task: 1 agent
  moderate_task: 1-2 agents
  complex_task: 2-3 agents

Parallelization Benefit:
  benefit = (sequential_time - parallel_time) / sequential_time
  minimum_benefit: 0.3 (30% faster to justify parallel)

User Experience:
  max_wait_time: 30 minutes per wave
  if estimated_time > 30: split into smaller waves

Synthesis Overhead:
  time_per_agent_synthesis: 2 minutes
  if agents > 10: synthesis takes too long, split wave
```

**Algorithm**:

```python
def calculate_optimal_wave_size(tasks, available_tokens):
  # Start with all parallelizable tasks
  parallel_tasks = [t for t in tasks if can_parallel(t)]

  # Calculate max agents from token budget
  max_agents_tokens = available_tokens / 3000

  # Calculate max agents from synthesis overhead
  max_agents_synthesis = 10

  # Take minimum
  max_agents = min(max_agents_tokens, max_agents_synthesis)

  # If more tasks than max, split into batches
  if len(parallel_tasks) > max_agents:
    waves = split_into_batches(parallel_tasks, max_agents)
    return waves
  else:
    return [parallel_tasks]  # Single wave

def split_into_batches(tasks, batch_size):
  batches = []
  for i in range(0, len(tasks), batch_size):
    batch = tasks[i:i+batch_size]
    batches.append(batch)
  return batches
```

**Example**:

```
Scenario: 15 UI components to build, all parallel

Token Budget: 180,000 available
Max Agents (tokens): 180000 / 3000 = 60 agents ✓
Max Agents (synthesis): 10 agents
Actual Max: 10 agents

Wave Strategy:
Wave 3a: Components 1-5 (5 agents)
Wave 3b: Components 6-10 (5 agents)
Wave 3c: Components 11-15 (5 agents)

Result: 3 waves of 5 agents each = manageable
```

### Wave Size Guidelines

**Small Wave** (1-3 agents):
- Use when: High complexity tasks, learning new domain, first wave
- Benefits: Easy to manage, detailed synthesis, quick validation
- Drawbacks: Less parallelization benefit

**Medium Wave** (4-7 agents):
- Use when: Standard implementation, proven patterns, mid-project
- Benefits: Good balance of speed and control
- Drawbacks: Moderate synthesis complexity

**Large Wave** (8-10 agents):
- Use when: Simple repetitive tasks, late project, high confidence
- Benefits: Maximum parallelization, fastest execution
- Drawbacks: Complex synthesis, harder to debug issues

**Never Exceed 10 Agents** per wave:
- Synthesis becomes unmanageable
- Token usage risk
- Debugging complexity too high
- User validation burden too large

---

## 8. Error Recovery

### Agent Failure Types

**Type 1: Tool Failure**
```
Symptom: Agent reports tool error (e.g., file not found, command failed)
Recovery:
1. Retry same agent with corrected context
2. If persistent: Switch to alternative tool
3. Document workaround in wave synthesis
```

**Type 2: Task Misunderstanding**
```
Symptom: Agent completes but deliverable is wrong
Recovery:
1. Load agent's result: read_memory("wave_[N]_agent_results")
2. Identify what was misunderstood
3. Respawn agent with clarified instructions
4. Emphasize the corrected requirement in prompt
```

**Type 3: Timeout/Crash**
```
Symptom: Agent doesn't complete, no result saved to Serena
Recovery:
1. Check: Did agent start? (any partial results?)
2. If started: Resume from last saved state
3. If crashed early: Respawn completely
4. If timeout: Increase complexity estimate, split task
```

**Type 4: Context Corruption**
```
Symptom: Agent loaded wrong context, made decisions based on bad data
Recovery:
1. Identify corrupted memory key
2. Restore from checkpoint (if available)
3. OR Re-run dependency wave
4. Respawn failed agent with corrected context
```

**Type 5: Integration Failure**
```
Symptom: Wave synthesis reveals components don't integrate
Recovery:
1. Analyze incompatibility in synthesis
2. Spawn integration-fixer agent (single task)
3. Update one or both components to compatible
4. Re-test integration
```

### Partial Wave Failure Handling

**Scenario**: Wave with 5 agents, 4 succeed, 1 fails

**Decision Tree**:

```
Agent failure detected in Wave [N]:
├─ Is failed task critical to wave completion?
│  ├─ YES (blocks other work)
│  │  └─ MUST fix before proceeding
│  │     1. Analyze failure: root-cause-analyst
│  │     2. Respawn failed agent with fixes
│  │     3. Wait for completion
│  │     4. Re-synthesize wave with all 5 results
│  │     5. Validate with user
│  │
│  └─ NO (nice-to-have or isolated)
│     └─ Can defer or skip
│        1. Document failure in wave_[N]_complete
│        2. Synthesize with 4 successful results
│        3. Present to user with:
│           "4/5 agents succeeded. Agent [X] failed (non-critical)."
│           "Options: (a) Fix now (b) Defer to later (c) Skip"
│        4. Proceed based on user choice
```

### Wave-Level Failure Handling

**Scenario**: Entire wave fails (all agents fail or fundamental issue)

**Recovery Process**:

```markdown
1. Capture State:
   - Save partial results (if any)
   - Document what went wrong
   - Identify root cause

2. Assess Impact:
   - Can project continue without this wave?
   - Can we work around the failure?
   - Is this a blocking issue?

3. Recovery Options:

   Option A: Retry Wave
   - Fix root cause
   - Respawn entire wave
   - Monitor for same issue

   Option B: Redesign Wave
   - Split into smaller waves
   - Change approach
   - Use different agents/tools

   Option C: Skip Wave
   - If non-critical
   - Document what was skipped
   - Adjust next waves accordingly

   Option D: Rollback
   - Restore from pre-wave checkpoint
   - Re-plan from stable state
   - Try different strategy

4. User Decision:
   Present options to user with recommendations
   Wait for user choice
   Execute chosen recovery path

5. Document Learning:
   write_memory("failure_analysis_wave_[N]", {
     what_failed: [...],
     root_cause: "...",
     recovery_chosen: "...",
     lessons_learned: [...]
   })
```

### Checkpoint-Based Recovery

**Pre-Wave Checkpoints**:

```markdown
Before spawning large/risky waves, create checkpoint:

write_memory("pre_wave_[N]_checkpoint", {
  wave_about_to_spawn: N,
  current_state: "About to spawn Wave [N]",
  completed_waves: [1, 2, ...],
  serena_keys: [all existing keys],
  context_summary: "...",
  restoration_instructions: "If Wave [N] fails catastrophically, restore by reading this checkpoint"
})

If wave fails catastrophically:
1. read_memory("pre_wave_[N]_checkpoint")
2. Verify all previous waves' context still intact
3. Re-plan Wave [N] with different strategy
4. Attempt again
```

### Error Documentation

**Always document errors**:

```javascript
write_memory("wave_[N]_errors", {
  wave_number: N,
  errors_encountered: [
    {
      agent_id: "frontend-builder",
      error_type: "tool_failure",
      error_message: "...",
      attempted_fixes: ["Retry", "Alternative tool"],
      resolution: "Resolved with alternative tool",
      time_lost_minutes: 5
    }
  ],
  overall_impact: "Minor - resolved within wave",
  lessons_learned: ["Always verify tool availability before spawn"]
})
```

---

## 9. Performance Optimization

### Parallelization Metrics

**Measure and Report**:

```markdown
After EVERY parallel wave, calculate speedup:

Sequential Time (hypothetical):
  sum(agent_completion_times)
  Example: Agent 1 (12m) + Agent 2 (15m) + Agent 3 (10m) = 37 minutes

Parallel Time (actual):
  max(agent_completion_times)
  Example: max(12m, 15m, 10m) = 15 minutes

Speedup:
  sequential_time / parallel_time
  Example: 37 / 15 = 2.47× faster

Efficiency:
  speedup / num_agents
  Example: 2.47 / 3 = 82% efficiency

Report in synthesis:
"Wave 2a: 3 agents completed in 15 minutes (vs 37 sequential) = 2.47× speedup"
```

### Token Usage Optimization

**Strategies**:

```markdown
1. Minimize Redundant Context Loading:
   - Don't load same memory multiple times per agent
   - Load once, reference throughout

2. Use Context Summaries:
   - For long wave_complete memories, create summary_wave_complete
   - Next wave loads summary instead of full detail

3. Incremental Context:
   - Early agents load full context
   - Later agents in same wave load delta only

4. Lazy Loading:
   - Only load memories agent actually needs
   - Don't load "just in case"

5. Context Compression:
   - After each phase, compress historical context
   - Keep decisions, discard verbose details
```

**Example**:

```markdown
Wave 4 agents don't need to read full Waves 1-3 results.

Instead of:
- read_memory("wave_1_complete") (5000 tokens)
- read_memory("wave_2_complete") (8000 tokens)
- read_memory("wave_3_complete") (6000 tokens)
Total: 19,000 tokens per agent

Use:
- read_memory("project_summary") (2000 tokens)
  Contains: Key decisions from all previous waves
Total: 2000 tokens per agent
Savings: 17,000 tokens per agent = 51,000 tokens for 3-agent wave
```

### Agent Task Sizing

**Optimal Task Granularity**:

```markdown
Too Small (Anti-Pattern):
Task: "Create TaskCard.tsx"
Problem: Overhead of agent spawn not justified
Solution: Combine into larger task "Create all task UI components"

Too Large (Anti-Pattern):
Task: "Build entire frontend"
Problem: Single agent takes 2 hours, no parallelization
Solution: Split into components, state, routing, testing

Optimal Size:
Task: "Build 3-5 related components" (10-20 minutes per agent)
Benefits:
- Meaningful parallelization opportunity
- Reasonable agent execution time
- Manageable synthesis
```

### Wave Scheduling Optimization

**Execution Timing**:

```markdown
Early Waves (1-2):
- Smaller waves (1-3 agents)
- More validation gates
- Conservative approach
- Build confidence and patterns

Mid Waves (3-5):
- Larger waves (5-7 agents)
- Proven patterns can scale
- Faster execution
- Less validation needed

Late Waves (6+):
- Flexible sizing
- Known environment
- Can push limits (8-10 agents if appropriate)
- Faster iteration
```

### Caching and Reuse

**MCP Result Caching**:

```markdown
When multiple agents use same MCP:

Example: 5 agents all need React patterns from Context7

Strategy:
1. First agent: Call Context7, save to Serena
   write_memory("context7_react_patterns", {...})

2. Remaining agents: Read from Serena instead of calling Context7
   read_memory("context7_react_patterns")

Benefits:
- Faster execution (memory read vs MCP call)
- Reduced MCP API usage
- Consistent patterns across agents
```

### Synthesis Optimization

**Incremental Synthesis**:

```markdown
For very large waves (8-10 agents):

Instead of synthesizing all at once:

1. Group agents by component domain:
   Group A: Frontend components (3 agents)
   Group B: Backend services (3 agents)
   Group C: Database & auth (2 agents)
   Group D: Testing (2 agents)

2. Synthesize each group:
   write_memory("wave_[N]_frontend_synthesis", {...})
   write_memory("wave_[N]_backend_synthesis", {...})
   write_memory("wave_[N]_data_synthesis", {...})
   write_memory("wave_[N]_testing_synthesis", {...})

3. Final wave synthesis combines group syntheses:
   write_memory("wave_[N]_complete", {
     frontend: read_memory("wave_[N]_frontend_synthesis"),
     backend: read_memory("wave_[N]_backend_synthesis"),
     ...
   })

Benefits:
- More manageable synthesis process
- Clearer organization
- Easier debugging
- Better user presentation
```

---

## Success Criteria

**Wave orchestration is successful when**:

✅ **Parallelism Verified**: All parallel waves measurably faster than sequential
   - Metric: speedup = sequential_time / parallel_time ≥ 1.5×
   - Evidence: Timestamps in agent results show concurrent execution

✅ **Zero Duplicate Work**: Agents don't redo what previous waves did
   - Check: No files created by multiple agents
   - Check: No decisions made multiple times
   - Evidence: Cross-reference agent results

✅ **Perfect Context Sharing**: Every agent has complete project history
   - Check: All agents loaded required Serena memories
   - Check: No agent made decisions based on incomplete information
   - Evidence: Agent results show correct context understanding

✅ **Clean Validation Gates**: User approvals obtained between waves
   - Check: Synthesis presented to user after each wave
   - Check: User explicitly approved before next wave
   - Evidence: Conversation shows validation and approval

✅ **All Wave Results Saved**: Complete Serena memory trail
   - Check: wave_[N]_complete exists for all waves
   - Check: Individual agent results saved
   - Evidence: list_memories() shows all expected keys

✅ **Resumability**: Next wave can resume perfectly from previous waves
   - Check: New agent can load all previous context and continue
   - Test: Spawn test agent that loads context and reports understanding
   - Evidence: Agent reports complete project history

✅ **Quality Maintained**: Production-ready code, functional tests, no mocks
   - Check: No TODOs or placeholders
   - Check: All tests functional (no mocking libraries)
   - Evidence: Code review and test analysis

---

## Conclusion

Wave orchestration transforms sequential agent execution into genuinely parallel workflows, achieving 40-60% faster completion through:

1. **True Parallelism**: All wave agents spawn in single message
2. **Complete Context**: Every agent loads full project history via Serena
3. **Systematic Synthesis**: Each wave ends with validation and context saving
4. **Smart Dependencies**: Waves respect prerequisites while maximizing parallelization
5. **Optimal Sizing**: Waves sized for balance of speed and manageability
6. **Robust Recovery**: Failures handled gracefully with multiple recovery paths
7. **Performance Focus**: Measured speedup, optimized token usage, efficient synthesis

By following these behavioral patterns, Claude Code achieves systematic, predictable, and measurably faster project execution while maintaining perfect context continuity and production-ready quality standards.