---
name: shannon:wave
description: Execute wave-based planning and execution with skill orchestration
usage: /shannon:wave [request] [--plan] [--dry-run]
---

# Wave Execution Command

## Overview

Orchestrates complex wave-based execution through skill invocation. Manages pre-wave checkpoints, wave planning/execution, agent coordination, functional testing, and goal alignment validation with post-wave preservation.

## Prerequisites

- Active specification context (run `/shannon:spec` first)
- Serena MCP available for checkpoints
- Complexity ≥ 0.50 for optimal wave benefits

## Workflow

### Step 1: Pre-Wave Checkpoint

Create checkpoint before wave execution:

**Invocation:**
```
@skill context-preservation
- checkpoint_name: "pre-wave-execution"
- context_to_save: [
    "spec_analysis",
    "phase_plan_detailed",
    "architecture_complete",
    "all_previous_wave_results"
  ]
- purpose: "Restore point before wave execution"
```

The context-preservation skill will save current state to Serena MCP for recovery if needed.

### Step 2: Wave Planning or Execution

Invoke wave orchestration skill based on flags:

**Planning Mode (--plan or --dry-run):**
```
@skill wave-orchestration --mode=plan
- Input: User's wave request
- Options:
  * analyze_dependencies: true
  * generate_wave_structure: true
  * allocate_agents: true
  * create_execution_plan: true
  * dry_run: true (if --dry-run flag)
  * save_to_serena: true
- Output: wave_execution_plan (not executed)
```

**Execution Mode (default):**
```
@skill wave-orchestration --mode=execute
- Input: User's wave request
- Options:
  * load_existing_plan: true (if wave_execution_plan exists)
  * execute_waves: true
  * true_parallelism: true (spawn all wave agents in one message)
  * synthesis_checkpoints: true (mandatory after each wave)
  * save_results: true
- Output: wave_execution_results
```

The wave-orchestration skill will:
1. Load specification and phase plan from Serena
2. Analyze dependencies and group into waves
3. Allocate agents based on complexity score
4. Execute waves with true parallel spawning (or plan if --plan)
5. Enforce synthesis checkpoints between waves
6. Save all wave results to Serena

### Step 3: Agent Coordination

Activate WAVE_COORDINATOR agent for orchestration:

**Activation:**
```
@agent WAVE_COORDINATOR
- Purpose: Manage parallel sub-agent execution across waves
- Responsibilities:
  * Spawn wave agents in parallel (one message)
  * Enforce context loading protocol for every agent
  * Synthesize results after each wave
  * Enforce validation gates between waves
  * Manage wave dependencies and sequencing
- Context Required:
  * spec_analysis (from Serena)
  * phase_plan_detailed (from Serena)
  * wave_execution_plan (from wave-orchestration skill)
  * All previous wave completions
```

WAVE_COORDINATOR will:
- Load complete context from all previous waves
- Spawn wave agents in TRUE parallel (multiple Task in one message)
- Enforce mandatory context loading in every agent prompt
- Create synthesis after each wave with user validation gate
- Ensure zero duplicate work and perfect context sharing

### Step 4: Functional Testing (If Tests Exist)

If project includes tests, invoke functional testing validation:

**Invocation (conditional):**
```
@skill functional-testing
- Input: Wave execution results
- Options:
  * test_type: "functional" (NO MOCKS mandate)
  * run_existing_tests: true
  * validate_coverage: true
  * verify_no_mocks: true (Iron Law)
- Output: test_results
```

Only invoked if:
- Tests exist in project
- Wave execution included implementation
- User hasn't skipped testing (with --skip-tests)

### Step 5: Goal Alignment Validation

Validate wave results align with North Star goal:

**Invocation:**
```
@skill goal-alignment
- Input: Wave execution results
- Options:
  * load_north_star: true (from Serena if exists)
  * calculate_alignment: true
  * threshold: 0.7 (minimum alignment score)
  * report_gaps: true
- Output: alignment_validation
```

The goal-alignment skill will:
1. Load North Star goal from Serena (if exists)
2. Analyze wave results against goal
3. Calculate alignment score (0.0-1.0)
4. Report alignment gaps if score < 0.7
5. Recommend corrections if needed

### Step 6: Post-Wave Checkpoint

Create checkpoint after successful wave completion:

**Invocation:**
```
@skill context-preservation
- checkpoint_name: "post-wave-{wave_number}"
- context_to_save: [
    "wave_execution_results",
    "wave_{N}_complete",
    "test_results",
    "alignment_validation",
    "all_agent_results"
  ]
- purpose: "Preserve complete wave execution state"
```

### Step 7: Present Results

Format and display wave execution summary:

```markdown
🌊 Wave Execution Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Execution Summary:**
- Strategy: {strategy_name}
- Total Waves: {wave_count}
- Agents Deployed: {total_agents}
- Execution Time: {duration}
- Speedup: {speedup}x vs sequential

**Waves Executed:**
{for each wave}
├─ Wave {N}: {wave_name}
   ├─ Agents: {agent_count}
   ├─ Duration: {wave_duration}
   ├─ Deliverables: {files_created} files, {components_built} components
   └─ Tests: {tests_created} functional tests (NO MOCKS)

**Key Accomplishments:**
- {accomplishment_1}
- {accomplishment_2}
- {accomplishment_3}

**Goal Alignment:** {alignment_score} / 1.0
{if alignment_score < 0.7}
⚠️  Alignment below threshold. Gaps: {gap_list}
{end if}

**Checkpoints Created:**
✓ Pre-wave: {pre_checkpoint_key}
✓ Post-wave: {post_checkpoint_keys}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
{if all_complete}
- Project complete! Review deliverables
- Run /shannon:status for final validation
{else}
- Continue with remaining waves
- Review wave results in Serena
{end if}
```

## Command Flags

### --plan
Generate wave execution plan without executing:
```bash
/shannon:wave Build full-stack app --plan
```

Shows:
- Wave structure with dependencies
- Agent allocation per wave
- Estimated timeline
- Parallelization opportunities

Does NOT execute - just planning.

### --dry-run
Generate detailed execution plan with impact analysis:
```bash
/shannon:wave Implement microservices --dry-run
```

Shows everything from --plan PLUS:
- Token usage estimates per wave
- Risk analysis for each wave
- Checkpoint recommendations
- Execution order with dependencies

Does NOT execute - comprehensive planning only.

## Usage Examples

### Example 1: Basic Wave Execution
```bash
/shannon:wave Build authentication system with JWT and OAuth
```

**What happens:**
1. Pre-wave checkpoint created
2. wave-orchestration analyzes spec, creates waves
3. WAVE_COORDINATOR spawns agents in parallel
4. Each wave executes with synthesis validation
5. Functional tests run (NO MOCKS)
6. Goal alignment validated
7. Post-wave checkpoint created

### Example 2: Planning Mode
```bash
/shannon:wave Implement dashboard with analytics --plan
```

**What happens:**
1. wave-orchestration creates execution plan
2. Shows wave structure, agent allocation, timeline
3. Saves plan to Serena as "wave_execution_plan"
4. Does NOT execute waves
5. User can review and approve before execution

### Example 3: Dry Run
```bash
/shannon:wave Build microservices architecture --dry-run
```

**What happens:**
1. Complete execution plan generated
2. Risk analysis performed
3. Token usage estimated
4. Checkpoint strategy recommended
5. Detailed timeline with dependencies
6. Does NOT execute - comprehensive analysis only

## Wave Strategies

The wave-orchestration skill automatically selects strategy:

### Linear Strategy
**When:** Clear sequential dependencies
- Phases: Analysis → Design → Implementation → Validation
- Checkpoints: After each phase
- Use Case: Well-defined requirements

### Parallel Strategy
**When:** Independent work streams
- Tracks: Frontend | Backend | Infrastructure
- Sync Points: Design, Implementation, Integration
- Use Case: Multi-domain development

### Iterative Strategy
**When:** Optimization tasks
- Iterations: Functionality → Performance → Polish
- Refinement: Progressive enhancement
- Use Case: Performance work, refactoring

### Adaptive Strategy
**When:** Uncertain requirements
- Phases: Discovered during execution
- Flexibility: Dynamic phase addition
- Use Case: Exploratory work, research

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained

**Same from V3:**
- Command syntax: `/shannon:wave [request]`
- Required arguments: Wave request text
- Strategy auto-selection
- Serena MCP integration
- WAVE_ORCHESTRATOR (now WAVE_COORDINATOR) activation

**Enhanced in V4:**
- Internal: Now uses skill orchestration pattern
- Enhancement: Pre/post-wave checkpoints via context-preservation skill
- Enhancement: Explicit functional-testing skill invocation (NO MOCKS)
- Enhancement: Goal alignment validation via goal-alignment skill
- Enhancement: Planning modes (--plan, --dry-run)
- Enhancement: Better agent coordination via WAVE_COORDINATOR

**Breaking Changes:** None

**Migration:**
- V3 commands work unchanged in V4
- New flags (--plan, --dry-run) are optional
- Skill invocations are automatic (transparent to user)
- Same output format with additional metrics

## Skill Dependencies

- **wave-orchestration** (REQUIRED) - Wave structure and execution
- **context-preservation** (REQUIRED) - Pre/post-wave checkpoints
- **functional-testing** (CONDITIONAL) - Post-wave test validation
- **goal-alignment** (OPTIONAL) - North Star alignment validation

## Agent Dependencies

- **WAVE_COORDINATOR** (REQUIRED) - Parallel agent orchestration

## MCP Dependencies

- **Serena MCP** (REQUIRED) - Checkpoint storage, wave context preservation
- **Sequential MCP** (RECOMMENDED) - Dependency analysis, complex reasoning

## Iron Laws

These cannot be violated even under pressure:

1. **Synthesis Checkpoint After Every Wave** - Mandatory user validation
2. **Dependency Analysis is Mandatory** - No spawning without dependency graph
3. **Complexity-Based Agent Allocation** - Algorithm determines agent count
4. **Context Loading for Every Agent** - All agents must load complete context
5. **True Parallelism** - All wave agents spawn in ONE message

See wave-orchestration skill for complete Iron Law documentation.

## Performance Metrics

Wave orchestration achieves **3.5x average speedup** through:
- True parallelism (agents spawn simultaneously)
- Complete context sharing (zero information loss)
- Systematic synthesis (validation after each wave)
- Smart dependencies (maximize parallel work)

Expected speedup by wave size:
- 2 agents: 1.5-1.8x
- 3 agents: 2.0-2.5x
- 5 agents: 3.0-4.0x
- 7+ agents: 3.5-5.0x

## Success Criteria

Wave execution succeeds when:
- ✅ All waves execute in planned order
- ✅ Parallel waves measurably faster than sequential
- ✅ Zero duplicate work between agents
- ✅ Perfect context sharing via Serena
- ✅ Clean validation gates at wave boundaries
- ✅ Functional tests pass (NO MOCKS)
- ✅ Goal alignment ≥ 0.7

## Notes

- **Most Complex Command**: sh_wave orchestrates Shannon's entire wave execution system
- **Skill-Heavy**: Delegates to 4+ skills for different aspects
- **Agent Coordination**: WAVE_COORDINATOR manages parallel execution
- **Checkpoint Safety**: Pre/post-wave checkpoints enable recovery
- **Quality Gates**: Synthesis validation after every wave (Iron Law)
- **NO MOCKS**: All functional tests use real implementations (Shannon mandate)

## Related Commands

**Before /shannon:wave:**
- `/shannon:spec` - Analyze specification (required)
- `/shannon:north_star` - Set guiding goal (recommended)
- `/shannon:check_mcps` - Verify MCP availability

**During /shannon:wave:**
- `/shannon:checkpoint` - Manual checkpoint (automatic in wave execution)
- `/shannon:status wave` - Check wave progress

**After /shannon:wave:**
- `/shannon:memory pattern` - Analyze wave patterns
- `/shannon:restore` - Restore from checkpoint if needed
- `/shannon:status` - Verify completion
