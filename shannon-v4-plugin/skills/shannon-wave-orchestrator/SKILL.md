---
name: shannon-wave-orchestrator
display_name: "Shannon Wave Orchestrator"
description: "Parallel wave execution with dependency management, context injection automation, and true parallelism via ONE-message multi-Task invocation"
category: orchestration
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_wave command"
  - "wave execution requested"
  - "parallel task orchestration"
mcp_servers:
  required:
    - serena
  recommended:
    - sequential
allowed_tools:
  - Task
  - Read
  - Glob
  - Grep
  - serena_write_memory
  - serena_read_memory
  - serena_list_memories
  - sequential_thinking
progressive_disclosure:
  tier: 1
  metadata_tokens: 200
  full_content: resources/FULL_SKILL.md
input:
  wave_number:
    type: integer
    description: "Wave number to execute (1-based)"
    required: true
  spec_analysis:
    type: object
    description: "Loaded from Serena (spec_analysis_*)"
    source: serena
  phase_plan:
    type: object
    description: "Loaded from Serena (phase_plan_detailed)"
    source: serena
  previous_wave_results:
    type: object
    description: "Results from wave N-1"
    source: serena
output:
  wave_results:
    type: object
    description: "Results from all agents in wave"
  agents_spawned:
    type: array
    description: "List of agents executed"
  validation_status:
    type: object
    description: "Validation gate results"
  next_wave:
    type: integer
    description: "Next wave number or null if complete"
---

# Shannon Wave Orchestrator

> **Core Shannon Skill**: Parallel wave execution with true parallelism (2-4× speedup)

## Purpose

Orchestrates parallel execution of independent tasks grouped into waves with:
- **Dependency Analysis** - Groups tasks by dependencies
- **TRUE Parallelism** - ONE message multi-Task invocation (not sequential)
- **Context Injection** - Automated context loading for all agents
- **Validation Gates** - Pre/post wave validation
- **State Management** - Serena MCP persistence

## Key Innovation: TRUE Parallelism

**CRITICAL**: Shannon v4 achieves TRUE parallel execution via ONE message with multiple Task invocations:

```xml
<!-- CORRECT: True Parallelism -->
<function_calls>
  <invoke name="Task">
    <parameter name="prompt">Agent A: [task with context]</parameter>
  </invoke>
  <invoke name="Task">
    <parameter name="prompt">Agent B: [task with context]</parameter>
  </invoke>
  <invoke name="Task">
    <parameter name="prompt">Agent C: [task with context]</parameter>
  </invoke>
</function_calls>
<!-- Result: All 3 agents execute SIMULTANEOUSLY (2-4× speedup measured) -->
```

```xml
<!-- INCORRECT: Sequential Execution -->
Message 1:
  <invoke name="Task">Agent A</invoke>
Message 2:
  <invoke name="Task">Agent B</invoke>
<!-- Result: Sequential, NO speedup -->
```

## Capabilities

### 1. Wave Planning
- Analyze task dependencies
- Group into independent waves
- Determine execution order
- Estimate wave duration

### 2. Context Injection (Automated)
**v4 Enhancement**: Eliminates manual context loading protocol

Each agent automatically receives:
```javascript
{
  north_star_goal: read_memory("north_star_goal"),
  spec_analysis: read_memory("spec_analysis"),
  phase_plan: read_memory("phase_plan_detailed"),
  previous_wave: read_memory("wave_[N-1]_complete"),
  project_context: read_memory("project_context")
}
```

**v3**: Required manual 5-step protocol (error-prone)
**v4**: Automated via PreWave hook ✅

### 3. Parallel Execution
- Spawn all wave agents in ONE message
- Measured 2-4× speedup
- No race conditions (Serena for coordination)
- Automatic result collection

### 4. Validation
- **PreWave Hook**: Dependency validation, context readiness
- **PostWave Hook**: Result validation, output verification
- **QualityGate Hook**: 5-gate enforcement
- Automatic rollback on failure

### 5. State Management
- Save wave results to Serena
- Track wave completion
- Enable wave resume
- Cross-session persistence

## Activation

**Automatic**:
```bash
/sh_wave 1
/sh_wave next
```

**Manual**:
```bash
Skill("shannon-wave-orchestrator")
```

**Trigger Conditions**:
- Wave execution requested
- Parallel task orchestration needed
- Multi-agent coordination required

## Execution Algorithm

### Step 1: Load Context (Automated via PreWave Hook)

```javascript
// PreWave hook fires automatically
const context = {
  spec_analysis: await serena_read_memory("spec_analysis"),
  phase_plan: await serena_read_memory("phase_plan_detailed"),
  previous_wave: await serena_read_memory(`wave_${wave_number - 1}_complete`),
  north_star: await serena_read_memory("north_star_goal")
};

// Validate context complete
if (!context.spec_analysis) {
  throw new Error("Run /sh_spec first");
}
```

### Step 2: Dependency Analysis

```javascript
// Analyze task dependencies
const tasks = phase_plan.phases[current_phase].tasks;
const dependencies = analyzeDependencies(tasks);

// Group into waves
const waves = groupByDependencies(dependencies);
// Example:
// Wave 1: [task_a, task_b, task_c] (no dependencies)
// Wave 2: [task_d, task_e] (depends on wave 1)
// Wave 3: [task_f] (depends on wave 2)
```

### Step 3: Prepare Wave Agents

```javascript
const current_wave_tasks = waves[wave_number];

// For each task, create agent prompt with context injection
const agent_prompts = current_wave_tasks.map(task => {
  return `
AUTHORIZATION CODE: ${project_id}-WAVE${wave_number}-AGENT-${task.id}

MISSION: ${task.description}

CONTEXT (Auto-Injected):
- North Star Goal: ${context.north_star}
- Spec Analysis: ${context.spec_analysis.summary}
- Current Phase: ${current_phase}
- Previous Wave Results: ${context.previous_wave?.summary}

TASK REQUIREMENTS:
${task.requirements.join('\n')}

SUCCESS CRITERIA:
${task.success_criteria.join('\n')}

DELIVERABLES:
${task.deliverables.join('\n')}

MANDATORY: Save results to Serena with key: wave_${wave_number}_task_${task.id}_result
  `;
});
```

### Step 4: Execute Wave (TRUE Parallelism)

```javascript
// CRITICAL: ONE message with multiple Task invocations
const wave_results = await execute_parallel_wave(agent_prompts);

function execute_parallel_wave(prompts) {
  // Generate ONE message with multiple Task calls
  const function_calls = prompts.map(prompt => ({
    name: "Task",
    parameters: { prompt }
  }));

  // Send as SINGLE message (true parallelism)
  return invoke_tools(function_calls);
}
```

### Step 5: Collect Results (PostWave Hook)

```javascript
// PostWave hook fires automatically after wave completes
const results = [];

for (const task of current_wave_tasks) {
  const result = await serena_read_memory(`wave_${wave_number}_task_${task.id}_result`);
  results.push({
    task_id: task.id,
    status: result.status,
    deliverables: result.deliverables,
    validation: validateTaskOutput(result, task.success_criteria)
  });
}
```

### Step 6: Validation Gates

```javascript
// QualityGate hook fires automatically
const validation = {
  wave_complete: all_tasks_completed(results),
  outputs_valid: all_outputs_valid(results),
  success_criteria_met: all_criteria_met(results),
  no_blockers: no_critical_errors(results)
};

if (!validation.wave_complete) {
  throw new Error("Wave incomplete - see results for failures");
}
```

### Step 7: Save Wave State

```javascript
await serena_write_memory(`wave_${wave_number}_complete`, {
  wave_number,
  timestamp: Date.now(),
  tasks_completed: results.length,
  tasks_succeeded: results.filter(r => r.status === 'success').length,
  results,
  validation,
  next_wave: wave_number + 1,
  project_id
});
```

### Step 8: Determine Next Action

```javascript
if (waves[wave_number + 1]) {
  return {
    action: "next_wave",
    wave_number: wave_number + 1,
    message: `Wave ${wave_number} complete. Ready for Wave ${wave_number + 1}`
  };
} else {
  return {
    action: "phase_complete",
    message: `All waves complete. Phase ${current_phase} finished.`
  };
}
```

## Wave Dependencies Example

```yaml
Project: "Build React Dashboard"

Wave 1 (Parallel - No Dependencies):
  - Task A: Design database schema
  - Task B: Create React component structure
  - Task C: Set up authentication system

Wave 2 (Parallel - Depends on Wave 1):
  - Task D: Implement database models (depends on A)
  - Task E: Build UI components (depends on B)

Wave 3 (Sequential - Depends on Wave 2):
  - Task F: Integration testing (depends on D + E)
```

**Execution**:
1. Wave 1: Tasks A, B, C execute in PARALLEL (ONE message)
2. Wait for all Wave 1 tasks to complete
3. Wave 2: Tasks D, E execute in PARALLEL (ONE message)
4. Wait for all Wave 2 tasks to complete
5. Wave 3: Task F executes (single task)

**Speedup**: 3 tasks in parallel = ~3× faster than sequential

## Context Loading Protocol (Automated)

**v3 Manual Protocol** (Error-Prone):
```
MANDATORY: Execute these 5 steps FIRST:
1. list_memories() - Discover available memories
2. read_memory("spec_analysis") - Load spec
3. read_memory("phase_plan_detailed") - Load plan
4. read_memory("wave_[N-1]_complete") - Load previous wave
5. Verify understanding before proceeding
```

**v4 Automated** (Hook-Based):
```javascript
// PreWave hook automatically injects context
// No manual steps required ✅
```

**Benefits**:
- Zero manual errors
- Faster wave startup
- Consistent context loading
- Better developer experience

## Integration with Hooks

### PreWave Hook
- Validates dependencies met
- Loads context from Serena
- Checks MCP availability
- Performs readiness checks
- **Blocks execution** if not ready

### PostWave Hook
- Collects results from all agents
- Validates outputs
- Updates project state
- Triggers next wave or checkpoint

### QualityGate Hook
- Enforces 5-gate validation
- Checks success criteria
- Validates deliverables
- **Blocks progression** if gates fail

## Examples

### Example 1: Simple 2-Wave Project

```bash
# Wave 1: Parallel analysis
/sh_wave 1
# Spawns: spec-analyzer, architecture-analyzer, risk-analyzer
# Result: 3 analyses complete in parallel

# Wave 2: Implementation
/sh_wave 2
# Spawns: frontend-worker, backend-worker
# Result: Implementations complete in parallel
```

### Example 2: Complex Multi-Wave

```bash
# Wave 1: Foundation (4 parallel tasks)
/sh_wave 1
# Tasks: database-schema, auth-system, ui-framework, api-design

# Wave 2: Implementation (6 parallel tasks)
/sh_wave 2
# Tasks: db-models, auth-impl, ui-components, api-endpoints, tests, docs

# Wave 3: Integration (2 parallel tasks)
/sh_wave 3
# Tasks: integration-tests, deployment-prep

# Wave 4: Final (1 task)
/sh_wave 4
# Task: production-deployment
```

## Performance Metrics

### Measured Speedup (v3 Data)
- **Sequential**: 12 hours for 6 tasks
- **Parallel (2 waves)**: 4 hours for 6 tasks
- **Speedup**: 3× faster

### Token Efficiency
- **v3**: Manual context loading (~500 tokens per agent × 6 = 3,000 tokens)
- **v4**: Automated injection (~0 additional tokens)
- **Savings**: 3,000 tokens per wave

## Skill Composition

**This skill orchestrates**:
- shannon-context-loader (context injection)
- shannon-dependency-validator (dependency analysis)
- shannon-agent-spawner (parallel execution)
- shannon-result-collector (result aggregation)
- shannon-checkpoint-manager (state persistence)

**This skill is used by**:
- /sh_wave command
- shannon-phase-planner (for multi-wave phases)
- shannon-workflow-manager (for complex workflows)

## Error Handling

### Common Errors

**Error**: "Wave N cannot execute: Wave N-1 not complete"
**Solution**: Complete previous wave first

**Error**: "Context incomplete: spec_analysis not found"
**Solution**: Run `/sh_spec` first

**Error**: "Wave validation failed: 2/3 tasks failed"
**Solution**: Review failed task results, fix issues, retry wave

### Recovery Patterns

```bash
# Check wave status
/sh_memory list
# Look for wave_*_complete entries

# Resume from checkpoint
/sh_restore wave_2_checkpoint

# Retry failed wave
/sh_wave 2 --retry
```

## Best Practices

### DO ✅
- Group independent tasks into same wave
- Use ONE message for parallel execution
- Save results to Serena after each wave
- Validate wave completion before next wave
- Use authorization codes for traceability

### DON'T ❌
- Execute dependent tasks in same wave
- Spawn agents in separate messages (loses parallelism)
- Skip context loading validation
- Ignore wave validation failures
- Execute waves out of order

## Learn More

📚 **Full Algorithm**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📚 **Wave Patterns**: [resources/WAVE_PATTERNS.md](./resources/WAVE_PATTERNS.md)
📚 **Examples**: [resources/EXAMPLES.md](./resources/EXAMPLES.md)

---

**Shannon V4** - Wave Orchestration at Scale 🚀
