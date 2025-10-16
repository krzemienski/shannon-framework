---
name: sc:task
command: /sc:task
description: "Long-term project management with wave orchestration, phase tracking, and cross-session persistence"
category: command
base: SuperClaude /task command
shannon_enhancement: true
description: Long-term project management with wave orchestration, phase tracking, and cross-session persistence
auto_persona: [architect, analyzer]
mcp_servers: [serena, sequential]
sub_agents: [WAVE_COORDINATOR, PHASE_ARCHITECT]
tools: [Task, TodoWrite, Read, Write]
wave_enabled: true
complexity_threshold: 0.6
---

# /sc:task - Project Task Management with Wave Orchestration

> **Shannon V3 Enhancement**: SuperClaude's `/task` command enhanced with wave orchestration, PHASE_ARCHITECT integration, Serena-based progress tracking, and multi-session project continuity.

## Purpose Statement

**Core Mission**: Manage complex, multi-session projects through structured phase execution, parallel wave orchestration, and persistent progress tracking.

**SuperClaude Foundation**:
- Long-term project management (days to weeks)
- Hierarchical task structure (Epic → Story → Task)
- Cross-session state management

**Shannon V3 Enhancements**:
- **Wave Orchestration**: Automatic parallel task execution via WAVE_COORDINATOR
- **Phase Integration**: Links with PHASE_ARCHITECT for structured project flow
- **Serena Tracking**: Persistent progress tracking across sessions with context preservation
- **Progress Visibility**: Real-time project status, wave completion, phase gates
- **Context Continuity**: Zero information loss through PreCompact hook integration

## Command Signature

```bash
/sc:task [operation] [arguments] [flags]

# Operations
/sc:task create [name] [description]     # Create new project task
/sc:task list                            # List all active projects
/sc:task status [name]                   # Show project status
/sc:task execute [name]                  # Execute next phase/wave
/sc:task checkpoint [name]               # Save current state
/sc:task resume [name]                   # Resume from checkpoint
/sc:task complete [name]                 # Mark project complete

# Flags
--wave            # Enable wave orchestration (auto for complexity ≥0.7)
--phase-plan      # Show detailed phase plan
--progress        # Display progress dashboard
--no-gates        # Skip validation gates (not recommended)
--checkpoint-freq [minutes]  # Auto-checkpoint interval (default: 30)
```

## Shannon V3 Enhancements

### 1. Wave Orchestration Integration

**Automatic Wave Coordination**:
- Complexity ≥ 0.7 automatically activates WAVE_COORDINATOR
- Tasks grouped into parallel waves based on dependencies
- True parallel execution (not sequential)
- Cross-wave context sharing via Serena MCP

**Wave Execution Pattern**:
```yaml
project_structure:
  phase_1_discovery:
    wave_1: [requirements-analysis, tech-research, mcp-verification]
    execution: parallel (all agents spawn in single message)
    duration: max(agent_times) not sum(agent_times)

  phase_2_architecture:
    wave_2a: [frontend-design, backend-design, database-schema]
    wave_2b: [api-contracts, integration-points]
    execution: wave_2a parallel, wave_2b sequential after 2a

  phase_3_implementation:
    wave_3a: [frontend-build, backend-build, database-setup]
    wave_3b: [feature-integration, api-testing]
    wave_3c: [e2e-testing]
    execution: 3a parallel → 3b parallel → 3c sequential
```

### 2. PHASE_ARCHITECT Integration

**Structured Project Flow**:
```yaml
phase_architecture:
  phase_1_discovery:
    duration: "20% of project"
    activities: [requirements, tech-stack, user-stories]
    validation_gate: "Requirements approval"
    deliverables: [requirements.md, user_stories.md, tech_stack.md]

  phase_2_architecture:
    duration: "15% of project"
    activities: [system-design, api-contracts, database-schema]
    validation_gate: "Architecture approval"
    deliverables: [architecture.md, api_spec.yaml, schema.sql]

  phase_3_implementation:
    duration: "45% of project"
    activities: [frontend-build, backend-build, integration]
    validation_gate: "Code review + tests pass"
    deliverables: [working_code, test_suite, integration_tests]

  phase_4_testing:
    duration: "15% of project"
    activities: [functional-tests, e2e-tests, performance-tests]
    validation_gate: "All tests passing"
    deliverables: [test_results, bug_reports, fixes]

  phase_5_deployment:
    duration: "5% of project"
    activities: [deploy-staging, production-deploy, monitoring]
    validation_gate: "Production validation"
    deliverables: [deployment_docs, monitoring_setup, runbook]
```

### 3. Serena Progress Tracking

**Cross-Session Persistence**:
```yaml
memory_structure:
  project_[name]:
    created: timestamp
    specification: original_spec
    complexity_score: float
    domain_breakdown: percentages

  project_[name]_phase_plan:
    phases: [phase_1_details, phase_2_details, ...]
    timeline: estimated_hours
    resources: [sub_agents, mcps, tools]

  project_[name]_phase_[N]_status:
    phase: phase_name
    status: pending|in_progress|validation|complete
    activities_completed: [list]
    deliverables: [list]
    validation_gate: approval_status

  project_[name]_wave_[N]_complete:
    wave_id: identifier
    phase: parent_phase
    agents: [agent_results]
    deliverables: [artifacts]
    duration: actual_time

  project_[name]_checkpoint_[timestamp]:
    current_phase: phase_number
    current_wave: wave_number
    completed_activities: [list]
    pending_work: [list]
    context_snapshot: full_state
```

**Progress Tracking**:
- Real-time phase status updates
- Wave completion tracking
- Activity completion percentage
- Timeline vs. actual progress
- Validation gate status

### 4. Progress Visibility

**Status Dashboard**:
```
PROJECT STATUS: E-Commerce Web Application
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERALL PROGRESS: 65% (26 of 40 hours)

🔄 CURRENT PHASE: Phase 3 - Implementation (in progress)
  ├─ Wave 3a: COMPLETE ✅ (frontend + backend + database)
  ├─ Wave 3b: IN PROGRESS 🔄 (integration + testing)
  └─ Wave 3c: PENDING ⏳ (e2e testing)

✅ COMPLETED PHASES:
  ├─ Phase 1: Discovery (6.4h) ✓ Gate passed
  └─ Phase 2: Architecture (4.8h) ✓ Gate passed

📋 VALIDATION GATES:
  ✅ Phase 1: Requirements approved
  ✅ Phase 2: Architecture approved
  🔄 Phase 3: Code review pending

⏱️  TIMELINE:
  Estimated: 40 hours
  Actual: 26 hours (65%)
  Remaining: 14 hours (35%)

🎯 NEXT ACTIONS:
  1. Complete Wave 3b integration work
  2. Run integration test suite
  3. Pass Phase 3 validation gate (code review)
  4. Begin Phase 4 testing activities
```

## Usage Patterns

### Pattern 1: Create New Project

```bash
# Create project with automatic wave orchestration
/sc:task create e-commerce "Build e-commerce web app with React, Express, PostgreSQL"

# System Response:
Creating project: e-commerce
- Analyzing specification via SPEC_ANALYZER
- Generating phase plan via PHASE_ARCHITECT
- Calculating wave structure via WAVE_COORDINATOR
- Saving project state to Serena

PROJECT CREATED: e-commerce
Complexity: 0.78 (high)
Timeline: 40 hours across 5 phases
Wave orchestration: ENABLED (9 waves planned)
Validation gates: 5 defined

Ready to execute Phase 1 Discovery
Run: /sc:task execute e-commerce
```

### Pattern 2: Execute Phase/Wave

```bash
# Execute next phase
/sc:task execute e-commerce

# System Response:
EXECUTING: Phase 1 - Discovery (Wave 1)

Spawning parallel agents (TRUE parallelism):
  ├─ requirements-analyst → requirements.md
  ├─ tech-researcher → tech_stack_analysis.md
  └─ mcp-verifier → mcp_ready.md

Wave 1 executing... (context loaded from Serena)

[Agents complete in parallel]

Wave 1 COMPLETE ✅
Deliverables saved to Serena:
  ├─ requirements.md (15 requirements, 8 P0, 5 P1, 2 P2)
  ├─ tech_stack_analysis.md (React + Express + PostgreSQL selected)
  └─ mcp_ready.md (serena, sequential, context7 installed)

VALIDATION GATE: Phase 1 Discovery Complete
Presenting deliverables for approval:
  - requirements.md
  - tech_stack_analysis.md
  - user_stories.md (15 stories with acceptance criteria)

Awaiting approval: "Approve Phase 1 to proceed to architecture"
```

### Pattern 3: Check Project Status

```bash
# View detailed status
/sc:task status e-commerce --progress

# Displays progress dashboard (shown above)
```

### Pattern 4: Checkpoint Project

```bash
# Manual checkpoint
/sc:task checkpoint e-commerce

# System Response:
CHECKPOINT SAVED: e-commerce_checkpoint_2025-09-30T14:30:00

Saved to Serena:
  ├─ Current phase: Phase 3 Implementation
  ├─ Current wave: Wave 3b (integration)
  ├─ Completed activities: 18 of 27
  ├─ All wave results: Wave 1-3a complete
  ├─ Context snapshot: full session state

Safe to end session - zero context loss guaranteed
```

### Pattern 5: Resume Project

```bash
# Resume from checkpoint
/sc:task resume e-commerce

# System Response:
RESUMING: e-commerce (from checkpoint 2025-09-30T14:30:00)

Loading context from Serena:
  ✓ Specification analysis
  ✓ Phase plan (5 phases)
  ✓ Wave 1 results (discovery complete)
  ✓ Wave 2a-2b results (architecture complete)
  ✓ Wave 3a results (implementation in progress)
  ✓ Current wave: Wave 3b (integration)

CONTEXT RESTORED: Ready to continue Wave 3b
  Pending: API integration testing
  Next: Complete integration → Pass Phase 3 gate → Begin Phase 4

Continue with: /sc:task execute e-commerce
```

### Pattern 6: Complete Project

```bash
# Mark project complete
/sc:task complete e-commerce

# System Response:
PROJECT COMPLETION CHECKLIST:

✓ Phase 1: Discovery (100%)
✓ Phase 2: Architecture (100%)
✓ Phase 3: Implementation (100%)
✓ Phase 4: Testing (100%)
✓ Phase 5: Deployment (100%)

All validation gates passed ✅
All deliverables saved to Serena ✅
All tests passing ✅

MARKING COMPLETE: e-commerce

Final statistics:
  Timeline: 42 hours (planned: 40 hours, 5% over)
  Phases: 5 of 5 complete
  Waves: 9 of 9 complete
  Validation gates: 5 of 5 passed

Project archived in Serena:
  ├─ project_e-commerce_complete
  ├─ All phase results preserved
  ├─ All wave results preserved
  └─ Complete execution history

Project successfully completed! 🎉
```

## Execution Flow

### Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ 1. PROJECT CREATION                                     │
│    /sc:task create [name] [spec]                       │
└────────────┬────────────────────────────────────────────┘
             │
             ├──> SPEC_ANALYZER: Analyze specification
             │    ├─ Calculate complexity score
             │    ├─ Identify domains
             │    ├─ Suggest MCPs
             │    └─ Save: spec_analysis
             │
             ├──> PHASE_ARCHITECT: Generate phase plan
             │    ├─ Create 5-phase structure
             │    ├─ Define validation gates
             │    ├─ Estimate timeline
             │    └─ Save: phase_plan_detailed
             │
             └──> WAVE_COORDINATOR: Plan wave structure
                  ├─ Analyze dependencies
                  ├─ Group into waves
                  ├─ Optimize parallelism
                  └─ Save: wave_execution_plan

┌─────────────────────────────────────────────────────────┐
│ 2. PHASE EXECUTION                                      │
│    /sc:task execute [name]                             │
└────────────┬────────────────────────────────────────────┘
             │
             ├──> Load Context from Serena
             │    ├─ Read: spec_analysis
             │    ├─ Read: phase_plan_detailed
             │    ├─ Read: wave_execution_plan
             │    └─ Read: all completed wave results
             │
             ├──> WAVE_COORDINATOR: Execute current wave
             │    ├─ Spawn ALL agents in ONE message (true parallel)
             │    ├─ Each agent loads context from Serena
             │    ├─ Agents work simultaneously
             │    └─ Collect results
             │
             ├──> Save Wave Results
             │    ├─ Write: wave_[N]_complete
             │    ├─ Save all deliverables
             │    └─ Update phase status
             │
             └──> Check Phase Completion
                  ├─ All waves complete?
                  └─ Yes → Validation Gate

┌─────────────────────────────────────────────────────────┐
│ 3. VALIDATION GATE                                      │
│    (Automatic after phase completion)                   │
└────────────┬────────────────────────────────────────────┘
             │
             ├──> Present Deliverables
             │    ├─ Show all phase deliverables
             │    ├─ Display completion checklist
             │    └─ Request user approval
             │
             ├──> User Decision
             │    ├─ APPROVE → Proceed to next phase
             │    ├─ REJECT → Iterate on current phase
             │    └─ MODIFY → Apply changes, re-validate
             │
             └──> Update Status
                  ├─ Write: phase_[N]_status (complete/iterate)
                  └─ If approved: Ready for next phase

┌─────────────────────────────────────────────────────────┐
│ 4. PROGRESS TRACKING                                    │
│    /sc:task status [name]                              │
└────────────┬────────────────────────────────────────────┘
             │
             └──> Generate Dashboard
                  ├─ Read all phase/wave status from Serena
                  ├─ Calculate completion percentage
                  ├─ Show current phase/wave
                  ├─ Display validation gate status
                  └─ Estimate remaining time

┌─────────────────────────────────────────────────────────┐
│ 5. CHECKPOINT & RESUME                                  │
│    /sc:task checkpoint/resume [name]                   │
└────────────┬────────────────────────────────────────────┘
             │
             ├──> CHECKPOINT
             │    ├─ Save current phase/wave
             │    ├─ Save completed activities
             │    ├─ Save pending work
             │    └─ Write: checkpoint_[timestamp]
             │
             └──> RESUME
                  ├─ Read: latest checkpoint
                  ├─ Read: all wave results
                  ├─ Restore full context
                  └─ Continue from saved state
```

## Sub-Agent Integration

### WAVE_COORDINATOR

**Primary Orchestrator**: Manages parallel wave execution

**Responsibilities**:
- Analyze task dependencies
- Group tasks into parallel waves
- Spawn all wave agents in single message (true parallelism)
- Ensure every agent loads complete context from Serena
- Collect and synthesize wave results
- Save wave completion status

**Activation**:
- Automatic when complexity ≥ 0.7
- Automatic for Phase 3 Implementation (always has waves)
- Manual with `--wave` flag

**Wave Execution Pattern**:
```yaml
wave_2a_frontend:
  agents:
    - frontend-implementer: "Build React UI"
    - state-manager: "Implement state management"
    - style-engineer: "Create responsive styling"

  spawn_pattern:
    method: single_message
    parallelism: true
    function_calls:
      - Task(frontend-implementer, prompt_with_context)
      - Task(state-manager, prompt_with_context)
      - Task(style-engineer, prompt_with_context)

  context_loading:
    mandatory_for_every_agent:
      - list_memories()
      - read_memory("spec_analysis")
      - read_memory("phase_plan_detailed")
      - read_memory("architecture_complete")
      - read_memory("wave_1_complete")
```

### PHASE_ARCHITECT

**Planning Specialist**: Creates detailed phase plans

**Responsibilities**:
- Transform spec analysis into 5-phase structure
- Define validation gates with approval criteria
- Allocate resources (agents, MCPs, tools) to activities
- Create realistic timelines with buffers
- Design wave structures for parallel execution
- Provide deliverable templates

**Activation**:
- Automatic after SPEC_ANALYZER completes
- Automatic for projects with complexity ≥ 0.6
- Manual with `/sh:plan-phases` command

**Phase Plan Output**:
```yaml
phase_plan_structure:
  overview:
    total_duration: "40 hours"
    phases: 5
    waves: 9
    validation_gates: 5

  phase_1_discovery:
    duration: "8 hours (20%)"
    wave_1:
      agents: [requirements-analyst, tech-researcher, mcp-verifier]
      parallelism: true
    deliverables: [requirements.md, tech_stack.md, mcp_ready.md]
    validation_gate: "Requirements approval"

  # ... phases 2-5 with same structure
```

## Output Format

### Project Creation Output

```markdown
# PROJECT CREATED: [project-name]

## 📋 Specification Summary
[Brief description of what's being built]

## 📊 Complexity Analysis
- **Complexity Score**: 0.78 (high)
- **Domains**: Frontend (40%), Backend (35%), Database (15%), DevOps (10%)
- **Timeline**: 40 hours across 5 phases
- **Risk Level**: Moderate

## 🏗️ Phase Structure
- **Phase 1**: Discovery (8h, 20%)
- **Phase 2**: Architecture (6h, 15%)
- **Phase 3**: Implementation (18h, 45%)
- **Phase 4**: Testing (6h, 15%)
- **Phase 5**: Deployment (2h, 5%)

## 🌊 Wave Orchestration
- **Total Waves**: 9
- **Parallel Waves**: 7
- **Sequential Waves**: 2
- **Parallelism Gain**: 3.2x speedup

## 🔧 MCP Servers
- **Required**: serena (memory), sequential (analysis)
- **Primary**: magic (UI), context7 (docs), puppeteer (testing)
- **Optional**: github (version control), docker (deployment)

## ✅ Validation Gates
1. Requirements approval (Phase 1)
2. Architecture approval (Phase 2)
3. Code review + tests pass (Phase 3)
4. All tests passing (Phase 4)
5. Production validation (Phase 5)

## 🚀 Next Steps
Run: `/sc:task execute [project-name]` to begin Phase 1
```

### Execution Output

```markdown
# EXECUTING: Phase 3 - Implementation (Wave 3a)

## 🌊 Wave Details
- **Wave ID**: 3a
- **Phase**: Implementation
- **Agents**: 3 (parallel execution)
- **Dependencies**: architecture_complete

## 🤖 Spawning Agents (TRUE PARALLELISM)
All agents spawned in SINGLE message:

1️⃣ **frontend-implementer**
   Task: Build React UI components
   Context: Loaded spec + architecture + Wave 1-2 results
   Duration: ~4 hours

2️⃣ **backend-implementer**
   Task: Build Express REST API
   Context: Loaded spec + architecture + Wave 1-2 results
   Duration: ~5 hours

3️⃣ **database-engineer**
   Task: Implement PostgreSQL schema
   Context: Loaded spec + architecture + Wave 1-2 results
   Duration: ~3 hours

## ⏱️ Execution Metrics
- **Spawn Time**: 0.5 seconds
- **Parallel Execution**: TRUE (all agents working simultaneously)
- **Expected Duration**: max(4h, 5h, 3h) = 5 hours
- **Sequential Would Be**: 4h + 5h + 3h = 12 hours
- **Speedup**: 2.4x faster

[Agents execute in parallel with progress updates]

## ✅ Wave 3a COMPLETE

### Deliverables
- ✓ `src/components/` - React UI components (frontend-implementer)
- ✓ `src/api/` - Express routes (backend-implementer)
- ✓ `src/db/schema.sql` - Database schema (database-engineer)
- ✓ All deliverables saved to Serena

### Next Steps
- Wave 3b: Integration + API testing (sequential after 3a)
- Run: `/sc:task execute [project-name]` to continue
```

### Status Output

```markdown
# PROJECT STATUS: E-Commerce Web Application

## 📊 Overall Progress
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65%

**26 of 40 hours complete** (14 hours remaining)

## 🔄 Current Status
**Phase**: 3 - Implementation (IN PROGRESS)
**Wave**: 3b - Integration & Testing
**Activity**: API integration testing

## ✅ Completed Phases
- ✓ Phase 1: Discovery (8h) - Gate PASSED
- ✓ Phase 2: Architecture (6h) - Gate PASSED

## 🔄 In Progress
- Phase 3: Implementation (12h of 18h complete)
  - ✓ Wave 3a: Frontend + Backend + Database
  - 🔄 Wave 3b: Integration testing (IN PROGRESS)
  - ⏳ Wave 3c: E2E testing (PENDING)

## ⏳ Pending Phases
- Phase 4: Testing (6h)
- Phase 5: Deployment (2h)

## 🎯 Validation Gates
- ✅ Phase 1: Requirements approved
- ✅ Phase 2: Architecture approved
- 🔄 Phase 3: Code review pending
- ⏳ Phase 4: Not reached
- ⏳ Phase 5: Not reached

## 📈 Timeline Analysis
- **Estimated**: 40 hours
- **Actual**: 26 hours (65%)
- **Remaining**: 14 hours (35%)
- **Pace**: On track (±2 hours buffer)

## 🚀 Next Actions
1. Complete Wave 3b integration testing
2. Run integration test suite (Puppeteer)
3. Pass Phase 3 validation gate (code review)
4. Begin Phase 4 testing activities

Run: `/sc:task execute e-commerce` to continue
```

## Examples

### Example 1: Full Project Lifecycle

```bash
# Create project
/sc:task create portfolio "Build portfolio website with Next.js, Tailwind, blog"

# Execute Phase 1 (Discovery)
/sc:task execute portfolio
# ... Wave 1 runs (requirements, tech-stack, mcp-setup)
# Validation gate: Approve requirements

# Execute Phase 2 (Architecture)
/sc:task execute portfolio
# ... Wave 2 runs (system-design, api-contracts, component-structure)
# Validation gate: Approve architecture

# Checkpoint before implementation
/sc:task checkpoint portfolio

# Execute Phase 3 (Implementation) - Multiple waves
/sc:task execute portfolio  # Wave 3a: Build components (parallel)
/sc:task execute portfolio  # Wave 3b: Integrate features (parallel)
/sc:task execute portfolio  # Wave 3c: E2E tests (sequential)
# Validation gate: Code review + tests pass

# Execute Phase 4 (Testing)
/sc:task execute portfolio
# ... Wave 4 runs (functional-tests, performance-tests, accessibility-tests)
# Validation gate: All tests passing

# Execute Phase 5 (Deployment)
/sc:task execute portfolio
# ... Wave 5 runs (deploy-vercel, setup-analytics, configure-domain)
# Validation gate: Production validation

# Complete project
/sc:task complete portfolio
```

### Example 2: Resume After Interruption

```bash
# Working on project, session interrupted
/sc:task execute e-commerce
# ... Wave 3b in progress, context fills up
# PreCompact hook triggers, saves checkpoint automatically

# New session, resume
/sc:task list
# Shows: e-commerce (Phase 3, Wave 3b, 65% complete)

/sc:task resume e-commerce
# Loads complete context from Serena
# Restores to exact Wave 3b state
# Zero information loss

/sc:task execute e-commerce
# Continues Wave 3b exactly where it left off
```

### Example 3: Status Monitoring

```bash
# Check status during long project
/sc:task status e-commerce

# Quick status
/sc:task status e-commerce --brief
# Output: "Phase 3 Wave 3b (65% complete, on track)"

# Detailed status with progress dashboard
/sc:task status e-commerce --progress
# (Shows full dashboard as above)

# Show phase plan
/sc:task status e-commerce --phase-plan
# (Shows detailed phase breakdown with validation gates)
```

## Integration with Shannon V3

### Context Preservation System

**PreCompact Hook Integration**:
```python
# ~/.claude/hooks/precompact.py automatically saves project state

CRITICAL: Before compacting, save project state:
1. list_memories() → get all Serena keys
2. write_memory("project_[name]_precompact_[timestamp]", {
     "current_phase": phase_number,
     "current_wave": wave_id,
     "completed_activities": list,
     "all_wave_results": all_keys,
     "pending_work": remaining_tasks
   })
3. After compact: read_memory and restore full state
```

**Cross-Session Continuity**:
- All project state stored in Serena MCP
- PreCompact hook prevents context loss
- Resume command restores complete project context
- Wave results persist across sessions
- Zero duplicate work across waves

### MCP Server Coordination

**Required MCPs**:
- **Serena**: Project state, wave results, phase tracking
- **Sequential**: Complex reasoning for dependency analysis

**Suggested MCPs** (based on domains):
- **Frontend**: magic (UI gen), context7 (docs), puppeteer (testing)
- **Backend**: context7 (framework docs), sequential (analysis)
- **Mobile**: swiftlens (iOS), context7 (docs)
- **Research**: tavily (search), firecrawl (scraping)

### Tool Coordination

**Primary Tools**:
- **Task**: Spawn sub-agents for wave execution
- **TodoWrite**: Track phase activities and validation gates
- **Read/Write**: Access and create deliverables

**Tool Usage Pattern**:
```yaml
discovery_phase:
  tool: Write
  purpose: Create deliverables (requirements.md, tech_stack.md)

architecture_phase:
  tool: Write
  purpose: Create design docs (architecture.md, schema.sql)

implementation_phase:
  tool: Task
  purpose: Spawn parallel implementation agents

testing_phase:
  tool: Puppeteer
  purpose: Run functional E2E tests (NO MOCKS)
```

### Validation & Quality Gates

**Shannon Testing Philosophy**:
- **NO MOCKS EVER**: Functional testing only (Puppeteer, simulator)
- **Real Components**: Test actual implementations, not stubs
- **Validation Required**: Every phase must pass gate to proceed

**Validation Gate Pattern**:
```yaml
phase_3_validation:
  name: "Code Review + Tests Pass"
  checklist:
    - "☐ All features implemented"
    - "☐ Puppeteer E2E tests pass"
    - "☐ Integration tests pass"
    - "☐ No TODO comments in code"
    - "☐ Code follows style guide"

  approval_required: true
  if_failed: "Iterate on Phase 3 based on feedback"
  if_passed: "Proceed to Phase 4 Testing"
```

## Notes

### Complexity Thresholds

**Wave orchestration auto-activates when**:
- Complexity score ≥ 0.7
- Project timeline > 20 hours
- Multiple domains involved (>2)
- User explicitly requests: `--wave`

**Phase planning auto-activates when**:
- Complexity score ≥ 0.6
- Project timeline > 8 hours
- User explicitly requests phase structure

### Parallelism Best Practices

**TRUE Parallelism Pattern**:
```xml
<!-- CORRECT: All agents in ONE message -->
<function_calls>
  <invoke name="Task"><parameter>agent1</parameter></invoke>
  <invoke name="Task"><parameter>agent2</parameter></invoke>
  <invoke name="Task"><parameter>agent3</parameter></invoke>
</function_calls>
<!-- Result: All 3 execute simultaneously -->

<!-- WRONG: Agents in separate messages -->
Message 1: <invoke name="Task">agent1</invoke>
Message 2: <invoke name="Task">agent2</invoke>
<!-- Result: Sequential execution (slow!) -->
```

### Context Loading Protocol

**Every sub-agent MUST load context**:
```markdown
MANDATORY at agent startup:
1. list_memories()
2. read_memory("spec_analysis")
3. read_memory("phase_plan_detailed")
4. read_memory("architecture_complete") if exists
5. read_memory("wave_1_complete") if exists
... (all previous waves)

This ensures:
- Zero duplicate work
- Complete project understanding
- Consistent implementation
- Proper dependency handling
```

### Checkpoint Strategy

**Auto-checkpoint triggers**:
- Every 30 minutes (configurable)
- After wave completion
- Before validation gates
- On user request
- Before PreCompact (automatic)

**Manual checkpoints recommended**:
- Before risky operations
- Before long-running waves
- At natural breakpoints
- End of session

### Error Recovery

**If wave fails**:
1. Review wave_[N]_complete status in Serena
2. Identify failed agent(s)
3. Re-spawn failed agents only (not entire wave)
4. Load context + previous results
5. Continue from failure point

**If validation gate fails**:
1. Review deliverables and checklist
2. Identify gaps/issues
3. Create targeted todo items
4. Execute fixes
5. Re-present for validation

---

**Ready to Use**: `/sc:task create [name] [specification]`