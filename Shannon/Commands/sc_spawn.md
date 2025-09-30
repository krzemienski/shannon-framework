---
command: /sc:spawn
name: sc_spawn
description: Enhanced meta-orchestration command with wave coordination awareness and Serena context sharing
category: orchestration
priority: high
base: SuperClaude /spawn command
enhancements: [wave_orchestration, serena_context_sharing, parallel_coordination]
triggers: [spawn, orchestrate, coordinate, multi-agent, parallel-execution]
auto_activate: false
tools: [Task, TodoWrite, Read, Grep]
mcp_servers: [serena, sequential]
sub_agents: [WAVE_COORDINATOR, PHASE_ARCHITECT, domain_specialists]
deliverables: [spawned_agents, coordination_plans, execution_results]
---

# /sc:spawn - Enhanced Task Orchestration Command

## Purpose Statement

**Base Capability** (SuperClaude): Meta-system task orchestration with intelligent breakdown and delegation for complex multi-domain operations.

**Shannon V3 Enhancements**: Wave orchestration awareness, Serena-based context sharing, WAVE_COORDINATOR integration, and parallel sub-agent coordination with complete context preservation.

## Core Functionality

### Base SuperClaude Capabilities

**Task Orchestration**: Intelligently spawn sub-agents for complex operations
**Intelligent Breakdown**: Decompose complex tasks into manageable agent assignments
**Dynamic Routing**: Select appropriate agents based on operation characteristics
**Result Aggregation**: Combine outputs from multiple agents into unified deliverables
**Mode Awareness**: Adapt orchestration strategy based on active modes

### Shannon V3 Enhancements

**Wave Orchestration Integration**: Seamlessly coordinate with WAVE_COORDINATOR for parallel execution
**Serena Context Sharing**: ALL spawned agents access complete project history via Serena MCP
**Context Preservation**: Zero information loss through mandatory context loading protocols
**Parallel Coordination**: True parallel agent execution (not sequential) with ONE message spawning
**Checkpoint Creation**: Automatic pre-spawn checkpoints for waves ≥5 agents
**Validation Gates**: User approval required between major orchestration phases
**NO MOCKS Enforcement**: All spawned testing agents follow functional testing philosophy

## Command Syntax

```bash
# Basic spawn
/sc:spawn [operation] [target]

# With explicit agents
/sc:spawn --agents [agent1,agent2,agent3] [task]

# With wave coordination
/sc:spawn --wave [operation]

# With execution mode
/sc:spawn --mode [parallel|sequential] [operation]

# With context checkpointing
/sc:spawn --checkpoint [task]

# Examples
/sc:spawn analyze codebase
/sc:spawn --agents analyzer,refactorer improve-quality
/sc:spawn --wave implement-phase-3
/sc:spawn --checkpoint build-microservices
```

## Shannon V3 Enhancements

### Enhancement 1: Wave Orchestration Awareness

**Integration with WAVE_COORDINATOR**:

```yaml
spawn_pattern:
  detect_wave_opportunity:
    conditions:
      - complexity >= 0.7
      - multiple_parallel_tasks: true
      - wave_plan_exists: true
    action: "Activate WAVE_COORDINATOR for orchestration"

  coordinate_with_waves:
    before_spawn: "Load wave execution plan from Serena"
    agent_selection: "Align with wave structure and dependencies"
    context_protocol: "Include mandatory context loading in ALL agent prompts"
    spawn_method: "Single message for parallel waves, respect dependencies"

  post_spawn_coordination:
    synthesis: "Collect results from all spawned agents"
    validation: "User approval before next wave"
    context_save: "Write aggregated results to Serena for future waves"
```

**Wave Detection Logic**:
```
IF operation is complex (complexity ≥ 0.7):
  1. Check if wave_execution_plan exists in Serena
  2. IF yes:
       Defer to WAVE_COORDINATOR for orchestration
       Follow wave structure and dependencies
  3. IF no:
       Analyze if wave orchestration beneficial
       Suggest /sh:create-waves if appropriate
       Fall back to traditional spawn if not

IF operation is simple (complexity < 0.7):
  Use traditional spawn without wave coordination
```

### Enhancement 2: Serena Context Sharing

**Mandatory Context Loading Protocol**:

EVERY spawned agent receives this protocol in their prompt:

```markdown
MANDATORY CONTEXT LOADING PROTOCOL:
Execute these commands BEFORE your assigned task:

1. list_memories() - discover all available Serena memories
2. read_memory("spec_analysis") - understand project requirements
3. read_memory("phase_plan_detailed") - know execution structure
4. read_memory("architecture_complete") if exists - system design
5. read_memory("wave_1_complete") if exists - previous wave results
6. read_memory("wave_[N-1]_complete") if exists - immediate prior wave
... (read ALL previous wave contexts)

Verify you understand:
✓ What we're building (from spec_analysis)
✓ How it's designed (from architecture_complete)
✓ What's been built (from previous waves)
✓ Your specific task (detailed below)

IF any required context is missing, STOP and request it before proceeding.
```

**Context Aggregation After Spawn**:

```yaml
post_spawn_synthesis:
  step_1: "Collect all spawned agent results"
  step_2: "Cross-validate for conflicts/gaps"
  step_3: "Aggregate deliverables (files, components, decisions)"
  step_4: "Save unified results to Serena with descriptive key"
  step_5: "Prepare context summary for future spawns"

  serena_key_pattern: "spawn_[operation]_[timestamp]_complete"

  synthesis_contents:
    - operation_summary
    - agents_deployed
    - execution_duration
    - deliverables_created
    - decisions_made
    - issues_encountered
    - next_actions_required
```

### Enhancement 3: Checkpoint System

**Pre-Spawn Checkpoint Creation**:

```yaml
checkpoint_triggers:
  agent_count: "≥5 agents"
  token_usage: "≥75% of context window"
  high_risk: "Production deployments, architectural changes"
  user_flag: "--checkpoint explicitly provided"

checkpoint_content:
  write_memory("pre_spawn_checkpoint", {
    operation: "[Operation name]",
    about_to_spawn: "[Agent count] agents",
    current_context: {
      serena_keys: [all loaded keys],
      project_state: [summary],
      pending_tasks: [list]
    },
    restoration_instructions: "Restore from here if spawn fails",
    timestamp: "[ISO 8601]"
  })
```

**Context Window Monitoring**:

```
BEFORE spawning agents:
  Check: current_tokens / max_tokens

  IF >75%: WARN user, suggest checkpoint
  IF >85%: MANDATORY checkpoint creation
  IF >95%: ERROR - must compact or clear before spawn

  Provide token estimate for spawn operation
```

### Enhancement 4: Parallel Coordination

**True Parallel Execution Pattern**:

```xml
ONE MESSAGE spawn for parallel agents:

<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">agent-1</parameter>
    <parameter name="description">Task 1 description</parameter>
    <parameter name="prompt">
MANDATORY CONTEXT LOADING PROTOCOL:
[Full context loading instructions]

YOUR TASK:
[Detailed task description]
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">agent-2</parameter>
    <parameter name="description">Task 2 description</parameter>
    <parameter name="prompt">
MANDATORY CONTEXT LOADING PROTOCOL:
[Full context loading instructions]

YOUR TASK:
[Detailed task description]
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">agent-3</parameter>
    <parameter name="description">Task 3 description</parameter>
    <parameter name="prompt">
MANDATORY CONTEXT LOADING PROTOCOL:
[Full context loading instructions]

YOUR TASK:
[Detailed task description]
    </parameter>
  </invoke>
</function_calls>

Result: All 3 agents execute SIMULTANEOUSLY
Duration: max(agent_times) not sum(agent_times)
```

## Execution Flow

### Standard Spawn Flow (No Wave Coordination)

```
Phase 1: PRE-SPAWN ANALYSIS
├─> Parse operation and target
├─> Analyze complexity (0.0-1.0 scale)
├─> Check for existing Serena context
├─> Determine if wave coordination beneficial
└─> Select appropriate agents for operation

Phase 2: AGENT PREPARATION
├─> Load required context from Serena
├─> Construct agent prompts with context loading protocol
├─> Determine spawn method (parallel vs sequential)
├─> Create checkpoint if needed (≥5 agents or high risk)
└─> Estimate token usage for spawn

Phase 3: AGENT SPAWN
├─> Spawn agents (ONE message for parallel, sequential for dependencies)
├─> Monitor agent execution
├─> Track progress with TodoWrite
└─> Collect agent results

Phase 4: POST-SPAWN SYNTHESIS
├─> Aggregate all agent results
├─> Cross-validate for conflicts/gaps
├─> Create unified deliverable summary
├─> Save aggregated results to Serena
└─> Present results to user

Phase 5: VALIDATION & CONTINUATION
├─> User reviews spawn results
├─> User approves or requests changes
├─> If approved: Mark complete, proceed
└─> If changes: Iterate with context from spawn results
```

### Wave-Coordinated Spawn Flow

```
Phase 1: WAVE DETECTION
├─> Check if wave_execution_plan exists in Serena
├─> Determine current wave number
├─> Load previous wave contexts
└─> Verify wave dependencies satisfied

Phase 2: WAVE_COORDINATOR ACTIVATION
├─> Activate WAVE_COORDINATOR agent
├─> Transfer operation details
├─> Provide complete context access
└─> Defer orchestration to WAVE_COORDINATOR

Phase 3: WAVE_COORDINATOR EXECUTION
├─> WAVE_COORDINATOR loads wave plan
├─> Determines agents for current wave
├─> Spawns wave agents (ONE message, parallel)
├─> Monitors wave execution
└─> Synthesizes wave results

Phase 4: WAVE VALIDATION GATE
├─> User reviews wave completion
├─> User approves to proceed to next wave
└─> Context preserved for subsequent waves

Phase 5: CONTINUATION
├─> Next wave spawned by WAVE_COORDINATOR
└─> Complete project through wave progression
```

## Sub-Agent Integration

### WAVE_COORDINATOR Integration

**When to Activate**:
```yaml
activation_criteria:
  complexity: "≥ 0.7"
  wave_plan_exists: true
  parallel_opportunities: "≥3 tasks"
  user_flag: "--wave provided"

activation_pattern:
  detect: "Analyze operation for wave suitability"
  check_serena: "Look for wave_execution_plan"
  activate: "Spawn WAVE_COORDINATOR if criteria met"
  transfer: "Provide complete context and operation details"
  monitor: "Track WAVE_COORDINATOR progress"
```

**WAVE_COORDINATOR Responsibilities**:
- Load wave execution plan from Serena
- Determine current wave to execute
- Spawn wave agents with complete context
- Synthesize wave results
- Manage validation gates
- Coordinate cross-wave context sharing

**Integration Pattern**:
```
/sc:spawn analyze-and-implement → Detects wave opportunity
                                ↓
                         Activates WAVE_COORDINATOR
                                ↓
                    WAVE_COORDINATOR spawns Wave 1 agents
                                ↓
                      Wave 1 synthesis and validation
                                ↓
                    WAVE_COORDINATOR spawns Wave 2 agents
                                ↓
                              ... continues
```

### Domain Specialist Coordination

**Agent Selection Matrix**:

```yaml
frontend_operations:
  agents: [frontend-implementer, ui-specialist, accessibility-expert]
  pattern: "Parallel spawn for independent components"
  context: "All agents load architecture_complete + previous waves"

backend_operations:
  agents: [backend-architect, api-developer, database-engineer]
  pattern: "Sequential if dependencies, parallel if independent"
  context: "All agents load spec + architecture + frontend results"

testing_operations:
  agents: [testing-worker, qa-specialist]
  pattern: "Spawn after implementation waves complete"
  context: "All agents load implementation results + NO MOCKS mandate"
  mandate: "Functional tests only, zero mocks allowed"

infrastructure_operations:
  agents: [devops-engineer, security-specialist]
  pattern: "Parallel spawn for orthogonal concerns"
  context: "All agents load complete system state"
```

### Context Loading Enforcement

**Agent Prompt Template** (included in EVERY spawned agent):

```markdown
You are a [AGENT_TYPE] sub-agent spawned by /sc:spawn.

═══════════════════════════════════════════════════════
MANDATORY CONTEXT LOADING PROTOCOL
═══════════════════════════════════════════════════════

EXECUTE THESE COMMANDS BEFORE YOUR TASK:

1. list_memories()
   → Discover all available Serena memories

2. read_memory("spec_analysis")
   → Understand: What we're building, requirements, scope

3. read_memory("phase_plan_detailed")
   → Understand: How project is structured, phases, waves

4. read_memory("architecture_complete") if exists
   → Understand: System design decisions, component structure

5. read_memory("wave_1_complete") if exists
   → Understand: What Wave 1 built

6. read_memory("wave_[N-1]_complete") if exists
   → Understand: Immediate previous wave results

7. Verify understanding:
   ✓ Project goal and requirements
   ✓ Current phase and wave
   ✓ What's been built so far
   ✓ Your specific task within larger context

IF required context missing: STOP and request context before proceeding

═══════════════════════════════════════════════════════
YOUR ASSIGNED TASK
═══════════════════════════════════════════════════════

[Detailed task description follows...]
```

## Output Formats

### Standard Spawn Output

```markdown
## 🚀 Spawning Sub-Agents: [Operation Name]

**Operation Details**:
- Operation: [Description]
- Complexity: [score] / 1.0
- Agent Count: [N] agents
- Execution Pattern: Parallel | Sequential
- Checkpoint: Created | Not required

**Context Setup**:
Loaded from Serena:
✓ spec_analysis
✓ phase_plan_detailed
✓ architecture_complete (if exists)
✓ Previous spawn results (if exists)

**Agent Assignments**:
1. **[Agent Type 1]** - [Task description]
2. **[Agent Type 2]** - [Task description]
3. **[Agent Type 3]** - [Task description]
... (continue for all agents)

**Spawning [N] Agents** [in PARALLEL | SEQUENTIALLY]:

[Agent execution occurs here]

---

## ✅ Spawn Complete: [Operation Name]

**Execution Summary**:
- Agents Deployed: [count]
- Execution Duration: [minutes]
- Files Created: [count]
- Components Built: [list]

**Key Accomplishments**:
- [Achievement 1]
- [Achievement 2]
- [Achievement 3]

**Decisions Made**:
- [Decision 1]
- [Decision 2]

**Integration Status**:
✓ All agents completed successfully
✓ Results aggregated
✓ No conflicts detected

**Saved to Serena**: `spawn_[operation]_[timestamp]_complete`

**Next Actions**:
[What should happen next based on spawn results]
```

### Wave-Coordinated Spawn Output

```markdown
## 🌊 Wave Coordination Detected

**Analysis**:
- Complexity: [score] / 1.0 (≥ 0.7 threshold met)
- Wave Plan: Found in Serena
- Current Wave: [N]
- Parallel Opportunities: [count] tasks

**Activating WAVE_COORDINATOR** for orchestration...

[WAVE_COORDINATOR takes over, manages wave execution]
[See WAVE_COORDINATOR.md for wave execution output format]

**Post-Wave Synthesis**:
- Wave [N] completed by WAVE_COORDINATOR
- Results aggregated to Serena
- Validation gate passed
- Ready for Wave [N+1]
```

### Checkpoint Output

```markdown
## 💾 Pre-Spawn Checkpoint Created

**Checkpoint Details**:
- Operation: [Operation name]
- Agents to Spawn: [count]
- Token Usage: [percentage]%
- Checkpoint Key: `pre_spawn_checkpoint`

**Context Preserved**:
✓ All Serena keys: [list]
✓ Project state: [summary]
✓ Pending tasks: [list]

**Restoration**: If spawn fails, restore from this checkpoint with:
```
read_memory("pre_spawn_checkpoint")
```

Proceeding with spawn...
```

## Usage Examples

### Example 1: Simple Multi-Agent Analysis

```bash
User: /sc:spawn analyze codebase --focus security,performance

Claude:
## 🚀 Spawning Sub-Agents: Codebase Analysis

**Operation Details**:
- Operation: Comprehensive codebase analysis
- Complexity: 0.6 / 1.0 (medium)
- Agent Count: 2 agents
- Execution Pattern: Parallel
- Checkpoint: Not required

**Context Setup**:
Loaded from Serena:
✓ spec_analysis (project requirements)
✓ architecture_complete (system design)

**Agent Assignments**:
1. **security-specialist** - Security vulnerability scan and threat modeling
2. **performance-analyst** - Performance bottleneck identification and optimization

**Spawning 2 Agents in PARALLEL**:

[Both agents execute simultaneously with context loading]

---

## ✅ Spawn Complete: Codebase Analysis

**Execution Summary**:
- Agents Deployed: 2
- Execution Duration: 4 minutes
- Issues Identified: 12 security findings, 8 performance bottlenecks

**Key Accomplishments**:
- Complete security scan with OWASP compliance check
- Performance profiling across all critical paths
- Actionable recommendations for both domains

**Saved to Serena**: `spawn_codebase_analysis_2025_complete`
```

### Example 2: Wave-Coordinated Implementation

```bash
User: /sc:spawn implement phase-3 --wave

Claude:
## 🌊 Wave Coordination Detected

**Analysis**:
- Complexity: 0.85 / 1.0 (high complexity)
- Wave Plan: Found in Serena (wave_execution_plan)
- Current Wave: Wave 2a
- Parallel Opportunities: 5 independent implementation tasks

**Activating WAVE_COORDINATOR** for orchestration...

[WAVE_COORDINATOR loads wave plan, determines agents, spawns Wave 2a]

**WAVE_COORDINATOR**: Spawning Wave 2a - Core Implementation
- 5 agents in PARALLEL (ONE message)
- All agents loaded complete context via Serena
- Expected duration: 25 minutes

[Wave execution proceeds under WAVE_COORDINATOR management]
[Wave synthesis and validation follows]
```

### Example 3: Checkpoint-Protected Spawn

```bash
User: /sc:spawn build-microservices --checkpoint

Claude:
## 💾 Pre-Spawn Checkpoint Created

**Checkpoint Details**:
- Operation: Build Microservices Architecture
- Agents to Spawn: 8 agents (auth, payments, inventory, shipping, notifications, gateway, monitoring, logging)
- Token Usage: 72% (checkpoint recommended)
- Checkpoint Key: `pre_spawn_checkpoint`

**Context Preserved**:
✓ All Serena keys: [spec_analysis, phase_plan_detailed, architecture_complete, wave_1_complete]
✓ Project state: Phase 3 implementation in progress
✓ Pending tasks: 18 implementation tasks remaining

**Restoration**: If spawn fails, restore from this checkpoint

Proceeding with spawn...

---

## 🚀 Spawning Sub-Agents: Build Microservices

**Agent Assignments**:
1. **backend-architect** - Auth microservice
2. **backend-architect** - Payments microservice
3. **backend-architect** - Inventory microservice
... (8 agents total)

**Spawning 8 Agents in PARALLEL**:

[All agents execute with full context]
```

### Example 4: Sequential Dependency Spawn

```bash
User: /sc:spawn test-and-deploy --mode sequential

Claude:
## 🚀 Spawning Sub-Agents: Test and Deploy

**Operation Details**:
- Operation: Test validation then production deployment
- Execution Pattern: Sequential (dependencies)
- Agent Count: 2 agents
- Checkpoint: Not required

**Dependency Chain**:
Agent 1 (testing-worker) → Agent 2 (devops-engineer)
(Deployment only proceeds if tests pass)

**Phase 1: Testing Agent**
Spawning testing-worker...

[Testing agent executes, validates all tests pass]

✅ Testing Complete: All tests passed (functional, NO MOCKS)

**Phase 2: Deployment Agent**
Spawning devops-engineer with test results...

[Deployment agent executes with test validation context]

✅ Deployment Complete: Production deployment successful
```

## Quality Standards

### Spawn Success Criteria

✅ **Context Completeness**: All agents have complete project history via Serena
✅ **Parallel Efficiency**: Parallel spawns measurably faster than sequential
✅ **Zero Duplication**: Agents don't redo work from previous spawns
✅ **Clean Integration**: Agent outputs compatible with no conflicts
✅ **Checkpoint Safety**: Checkpoints created for risky/large spawns
✅ **Validation Gates**: User approvals obtained for major operations
✅ **NO MOCKS Compliance**: All testing agents follow functional testing philosophy

### Pre-Spawn Validation

```yaml
checks_required:
  context_available:
    - spec_analysis exists OR operation self-contained
    - Previous spawn results loaded if continuation
    - Architecture available if implementation task

  token_capacity:
    - Current usage < 75% for normal spawn
    - Current usage < 60% for large spawn (≥5 agents)
    - Checkpoint created if usage ≥75%

  agent_availability:
    - Selected agents appropriate for operation
    - MCP servers available if required by agents
    - Tools available for agent execution

  dependency_satisfaction:
    - Prerequisites completed if sequential spawn
    - Previous wave complete if wave-coordinated
    - Required files/components exist if build operation
```

### Post-Spawn Validation

```yaml
checks_required:
  execution_success:
    - All agents completed without errors
    - Agent outputs collected successfully
    - No agent timeouts or failures

  result_quality:
    - Deliverables match expectations
    - No conflicts between agent outputs
    - Integration points validated
    - Tests present if implementation (NO MOCKS)

  context_preservation:
    - Results saved to Serena with descriptive key
    - Next actions documented
    - Decisions captured for future reference

  user_satisfaction:
    - User reviews spawn results
    - User confirms quality acceptable
    - User approves continuation if multi-stage
```

## Integration with Shannon Components

### With /sh:analyze-spec
- Spawn agents for domain-specific spec analysis if needed
- Respect complexity score for spawn orchestration decisions

### With /sh:plan-phases
- Spawn PHASE_ARCHITECT for phase plan creation
- Coordinate with wave plans from phase planning

### With /sh:create-waves
- Defer to WAVE_COORDINATOR when wave plan exists
- Follow wave structure for spawn orchestration

### With /sh:checkpoint
- Automatic checkpoint creation for large/risky spawns
- Manual checkpoint triggering with --checkpoint flag

### With Shannon Testing Philosophy
- All spawned testing agents receive NO MOCKS mandate
- Functional testing requirement included in agent prompts

## Command Comparison

| Aspect | SuperClaude /spawn | Shannon /sc:spawn |
|--------|-------------------|-------------------|
| **Base Capability** | Meta-orchestration | Same + wave awareness |
| **Context Sharing** | Agent-specific | Serena-based, project-wide |
| **Parallel Execution** | Task tool (appears parallel) | True parallel with ONE message |
| **Context Preservation** | Agent results only | Complete synthesis to Serena |
| **Wave Coordination** | No | WAVE_COORDINATOR integration |
| **Checkpoints** | No | Automatic for ≥5 agents |
| **Validation Gates** | No | User approval required |
| **Testing Philosophy** | Undefined | NO MOCKS mandate |

## Best Practices

### DO
✅ Check for wave_execution_plan before spawning (defer to WAVE_COORDINATOR if exists)
✅ Include mandatory context loading protocol in EVERY agent prompt
✅ Spawn parallel agents in ONE message for true parallelism
✅ Create checkpoints before large spawns (≥5 agents)
✅ Save aggregated results to Serena with descriptive keys
✅ Request user validation for major operations
✅ Monitor token usage and warn user if approaching limits
✅ Enforce NO MOCKS requirement for all testing agents

### DON'T
❌ Spawn parallel agents in separate messages (creates sequential execution)
❌ Skip context loading protocol (causes information loss)
❌ Proceed without checking dependencies (breaks sequential operations)
❌ Forget to synthesize results to Serena (loses context for future spawns)
❌ Allow testing agents to use mocks (violates Shannon philosophy)
❌ Spawn large waves without checkpoints (risky if failure occurs)
❌ Continue without user validation for major operations

## Notes

- Base command inherited from SuperClaude framework
- Enhanced with Shannon V3 wave orchestration patterns
- Required for complex multi-agent operations in Shannon workflow
- Works seamlessly with WAVE_COORDINATOR for structured projects
- Critical for context preservation through Serena integration