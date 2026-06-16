# /sc:workflow - Enhanced Workflow Orchestration Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:workflow - Enhanced Workflow Orchestration Command

> **Shannon V3 Enhancement**: SuperClaude's `/workflow` command enhanced with wave-based workflow orchestration, 5-phase integration, systematic validation gates, and structured execution templates.

## Purpose Statement

Comprehensive workflow orchestration that transforms specifications into structured execution plans:

- **5-Phase Integration** - Aligns workflows with Discovery → Architecture → Implementation → Testing → Deployment
- **Wave-Based Orchestration** - Parallel execution of workflow stages through specialized sub-agents
- **Validation Gate System** - Mandatory checkpoints between workflow phases with approval gates
- **Structured Templates** - Pre-built workflow patterns for common project types
- **Context Preservation** - Complete workflow state saved to Serena MCP across sessions
- **Progress Tracking** - Real-time workflow status with milestone visualization
- **Dependency Management** - Automatic task ordering based on dependency analysis
- **Resource Optimization** - Intelligent workload distribution across sub-agents

**What Makes This Different**: SuperClaude's `/workflow` provides basic task coordination. Shannon's `/sc:workflow` orchestrates complex multi-phase projects with parallel execution, systematic validation, and complete context preservation.

## Shannon V3 Enhancements Over SuperClaude

### 1. Wave-Based Workflow Execution (NEW)
**SuperClaude**: Sequential task execution
**Shannon**: Parallel workflow orchestration with wave coordination

```yaml
wave_workflow_execution:
  wave_1_discovery:
    parallel_tasks:
      - requirements-analyst → Requirements finalization
      - system-architect → Technical research
      - business-analyst → Stakeholder analysis

  validation_gate_1:
    required: "User approval of discovery outputs"

  wave_2_architecture:
    parallel_tasks:
      - system-architect → System design
      - database-architect → Data model design
      - integration-architect → API specifications

  validation_gate_2:
    required: "Architecture approval before implementation"

  wave_3_implementation:
    parallel_waves:
      - frontend-developer → UI implementation
      - backend-developer → API implementation
      - devops-engineer → Infrastructure setup
```

### 2. 5-Phase Integration (ENHANCED)
**SuperClaude**: No phase structure
**Shannon**: Explicit 5-phase alignment with effort distribution

```yaml
phase_integration:
  phase_1_discovery:
    effort_percentage: 20%
    workflow_focus: "Requirements, research, planning"
    validation: "Requirements approval gate"

  phase_2_architecture:
    effort_percentage: 15%
    workflow_focus: "Design, specifications, diagrams"
    validation: "Architecture review gate"

  phase_3_implementation:
    effort_percentage: 45%
    workflow_focus: "Parallel wave execution"
    validation: "Code review + functional tests"

  phase_4_testing:
    effort_percentage: 15%
    workflow_focus: "Integration, E2E, performance"
    validation: "Test results approval"

  phase_5_deployment:
    effort_percentage: 5%
    workflow_focus: "Release, monitoring, documentation"
    validation: "Production deployment approval"
```

### 3. Validation Gate System (NEW)
**SuperClaude**: No systematic validation
**Shannon**: Mandatory gates with approval tracking

```yaml
validation_gates:
  gate_structure:
    - Pre-conditions: "What must be complete"
    - Validation criteria: "How to verify quality"
    - Deliverables: "Required outputs"
    - Approval: "User sign-off required"

  gate_enforcement:
    - Cannot proceed without approval
    - Serena tracks approval status
    - Rollback capability if issues found
```

### 4. Workflow Templates (NEW)
**SuperClaude**: Manual workflow creation
**Shannon**: Pre-built templates for common scenarios

```yaml
workflow_templates:
  - fullstack_web_app
  - mobile_app_development
  - api_backend_service
  - data_pipeline
  - infrastructure_automation
  - migration_project
  - refactoring_initiative
```

## Usage Patterns

**Basic Usage**:
```
/sc:workflow [project-name]
/sc:workflow "E-commerce Platform"
/sc:workflow @specs/project-spec.md
```

**With Template Selection**:
```
/sc:workflow [project] --template fullstack
/sc:workflow [project] --template mobile
/sc:workflow [project] --template api-service
/sc:workflow [project] --template custom
```

**With Phase Targeting**:
```
/sc:workflow [project] --start-phase 2
/sc:workflow [project] --phases 1-3
/sc:workflow [project] --skip-discovery
```

**With Wave Control**:
```
/sc:workflow [project] --waves 4
/sc:workflow [project] --sequential (disable parallelization)
/sc:workflow [project] --max-concurrent 3
```

**With Checkpoint Management**:
```
/sc:workflow [project] --auto-checkpoint
/sc:workflow [project] --checkpoint-interval 30m
/sc:workflow [project] --resume-from-checkpoint
```

**Type in Claude Code conversation window** (not terminal)

## Execution Flow

```mermaid
graph TD
    A[/sc:workflow initiated] --> B{Load Context}
    B -->|New| C[Select Template]
    B -->|Resume| D[Restore Checkpoint]
    C --> E[Generate Workflow Plan]
    D --> E
    E --> F[Present Plan for Approval]
    F -->|Approved| G[Phase 1: Discovery]
    F -->|Rejected| E
    G --> H{Gate 1 Validation}
    H -->|Pass| I[Phase 2: Architecture]
    H -->|Fail| G
    I --> J{Gate 2 Validation}
    J -->|Pass| K[Phase 3: Implementation Waves]
    J -->|Fail| I
    K --> L{Gate 3 Validation}
    L -->|Pass| M[Phase 4: Testing]
    L -->|Fail| K
    M --> N{Gate 4 Validation}
    N -->|Pass| O[Phase 5: Deployment]
    N -->|Fail| M
    O --> P{Gate 5 Validation}
    P -->|Pass| Q[Workflow Complete]
    P -->|Fail| O
```

## Sub-Agent Integration

### Primary Sub-Agents

**WAVE_COORDINATOR**
```yaml
role: "Orchestrate parallel workflow execution"
activation: "Always for /sc:workflow"
responsibilities:
  - Workflow decomposition into waves
  - Dependency analysis and ordering
  - Sub-agent coordination
  - Progress monitoring
  - Validation gate enforcement
tools: [Task, TodoWrite, Read, Sequential]
mcp: [Serena (context), Sequential (planning)]
```

**PHASE_ARCHITECT**
```yaml
role: "Align workflow with 5-phase structure"
activation: "Auto for complex workflows"
responsibilities:
  - Phase boundary definition
  - Effort distribution calculation
  - Validation criteria specification
  - Template customization
  - Gate configuration
tools: [Write, Read, Sequential]
mcp: [Sequential (phase planning)]
```

**REQUIREMENTS_ANALYST**
```yaml
role: "Discovery phase coordination"
activation: "Phase 1 (Discovery)"
responsibilities:
  - Requirements documentation
  - User story creation
  - Acceptance criteria definition
  - Priority assignment
tools: [Write, Read]
mcp: [Serena (memory)]
```

**SYSTEM_ARCHITECT**
```yaml
role: "Architecture phase leadership"
activation: "Phase 2 (Architecture)"
responsibilities:
  - System design
  - Technical specifications
  - Diagram generation
  - Technology selection
tools: [Write, Read, Glob]
mcp: [Context7 (patterns), Sequential (design)]
```

**IMPLEMENTATION_WORKER**
```yaml
role: "Implementation wave execution"
activation: "Phase 3 (Implementation)"
responsibilities:
  - Parallel implementation coordination
  - Code quality enforcement
  - NO MOCKS testing
  - Integration management
tools: [Write, Edit, MultiEdit, Bash]
mcp: [Magic (UI), Context7 (patterns), Serena (context)]
```

## Workflow Templates

### 1. Full-Stack Web Application

```yaml
template: fullstack_web_app
phases:
  phase_1_discovery:
    duration: "2-3 days"
    deliverables:
      - requirements.md
      - user_stories.md
      - tech_stack_analysis.md
    validation: "Stakeholder approval + tech feasibility"

  phase_2_architecture:
    duration: "1-2 days"
    deliverables:
      - system_architecture.md
      - database_schema.md
      - api_specification.md
      - component_hierarchy.md
    validation: "Architecture review approval"

  phase_3_implementation:
    duration: "5-8 days"
    waves:
      wave_1:
        - Frontend foundation (routing, state, layout)
        - Backend foundation (server, middleware, auth)
        - Database setup (migrations, seeds)
      wave_2:
        - Frontend features (components, pages)
        - Backend APIs (endpoints, validation)
        - Database operations (queries, relations)
      wave_3:
        - Integration (frontend ↔ backend)
        - Error handling
        - Loading states
    validation: "Code review + functional tests pass"

  phase_4_testing:
    duration: "1-2 days"
    activities:
      - E2E tests (Playwright)
      - Integration tests
      - Performance testing
      - Security scanning
    validation: "All tests green + performance benchmarks met"

  phase_5_deployment:
    duration: "0.5-1 day"
    activities:
      - Production build
      - Environment setup
      - Deployment
      - Monitoring setup
      - Documentation
    validation: "Production deployment successful + monitoring active"
```

### 2. Mobile Application

```yaml
template: mobile_app
phases:
  phase_1_discovery:
    deliverables:
      - requirements.md
      - user_flows.md
      - platform_selection.md (iOS/Android/Both)
    validation: "Requirements + platform approval"

  phase_2_architecture:
    deliverables:
      - app_architecture.md
      - navigation_structure.md
      - state_management_plan.md
      - api_integration_spec.md
    validation: "Architecture review"

  phase_3_implementation:
    waves:
      wave_1:
        - Project setup (Xcode/Android Studio)
        - Navigation scaffolding
        - State management foundation
      wave_2:
        - Screen implementations
        - API integration
        - Local storage
      wave_3:
        - Polish (animations, gestures)
        - Error handling
        - Offline support
    validation: "Simulator tests + code review"

  phase_4_testing:
    activities:
      - Functional tests (XCTest/Espresso)
      - UI tests on real devices
      - Performance testing
      - Memory leak detection
    validation: "All tests pass + no memory leaks"

  phase_5_deployment:
    activities:
      - App Store / Play Store preparation
      - Beta testing (TestFlight/Firebase)
      - Production release
      - Analytics setup
    validation: "App published + analytics tracking"
```

### 3. API Backend Service

```yaml
template: api_backend_service
phases:
  phase_1_discovery:
    deliverables:
      - api_requirements.md
      - endpoints_list.md
      - data_model_draft.md
    validation: "API contract approval"

  phase_2_architecture:
    deliverables:
      - api_specification.md (OpenAPI/Swagger)
      - database_schema.md
      - authentication_design.md
      - deployment_architecture.md
    validation: "API design review"

  phase_3_implementation:
    waves:
      wave_1:
        - Server setup + middleware
        - Database connection + migrations
        - Authentication system
      wave_2:
        - Endpoint implementations
        - Validation logic
        - Error handling
      wave_3:
        - Business logic
        - Data transformations
        - Query optimization
    validation: "Integration tests pass"

  phase_4_testing:
    activities:
      - API integration tests
      - Load testing
      - Security testing
      - Documentation validation
    validation: "Performance benchmarks + security scan clean"

  phase_5_deployment:
    activities:
      - Container setup (Docker)
      - CI/CD pipeline
      - Production deployment
      - Monitoring + logging
      - API documentation publication
    validation: "API live + monitoring active"
```

### 4. Infrastructure Automation

```yaml
template: infrastructure_automation
phases:
  phase_1_discovery:
    deliverables:
      - infrastructure_requirements.md
      - resource_inventory.md
      - automation_scope.md
    validation: "Scope approval"

  phase_2_architecture:
    deliverables:
      - infrastructure_design.md
      - terraform_structure.md
      - pipeline_design.md
    validation: "Architecture review"

  phase_3_implementation:
    waves:
      wave_1:
        - Base infrastructure (VPC, networking)
        - IAM setup
        - State management
      wave_2:
        - Compute resources
        - Storage setup
        - Database provisioning
      wave_3:
        - Application setup
        - Load balancers
        - DNS configuration
    validation: "Infrastructure validates in staging"

  phase_4_testing:
    activities:
      - Terraform validation
      - Security compliance checks
      - Cost analysis
      - Failover testing
    validation: "All checks pass + cost approved"

  phase_5_deployment:
    activities:
      - Production deployment
      - Monitoring setup
      - Runbook creation
      - Team training
    validation: "Production live + team trained"
```

## Validation Gates

### Gate Structure

Each validation gate enforces quality standards before phase progression:

```yaml
validation_gate_template:
  gate_id: "gate_N"
  phase: "Phase N"

  pre_conditions:
    - "Deliverable X complete"
    - "Deliverable Y reviewed"
    - "Quality checks passed"

  validation_criteria:
    - "Acceptance criteria met"
    - "No blockers remaining"
    - "Stakeholder approval obtained"

  deliverables_required:
    - "document_name.md"
    - "artifact_name"

  approval_process:
    - Present deliverables
    - Address feedback
    - Obtain sign-off

  failure_action:
    - Return to phase
    - Address issues
    - Re-validate
```

### Automated Gate Checks

```yaml
automated_checks:
  code_quality:
    - Linting passes
    - Type checking passes
    - No TODO comments in production code
    - Test coverage ≥ 80%

  functional_validation:
    - All tests green
    - NO MOCKS (functional tests only)
    - Integration tests pass

  documentation:
    - README updated
    - API docs current
    - Inline documentation present

  security:
    - No secrets in code
    - Dependencies up-to-date
    - Security scan clean
```

## Context Preservation

### Serena Integration

**Workflow State Preservation**:
```yaml
serena_workflow_memory:
  workflow_plan:
    key: "workflow_plan_[project]"
    content: "Complete workflow definition with phases, waves, gates"

  phase_status:
    key: "phase_[N]_status"
    content: "Current phase progress, deliverables, validation status"

  wave_results:
    key: "wave_[N]_results"
    content: "Completed wave outputs, decisions, issues"

  gate_approvals:
    key: "gate_[N]_approval"
    content: "Approval status, feedback, timestamp"

  checkpoint_state:
    key: "workflow_checkpoint_[timestamp]"
    content: "Complete workflow state snapshot"
```

**Session Operations**:
```
# Session start
1. read_memory("workflow_plan_[project]") → Load workflow
2. read_memory("phase_*_status") → Resume from last position
3. read_memory("gate_*_approval") → Check validation status

# During execution
1. write_memory("wave_N_results", outputs) → Save wave results
2. write_memory("phase_N_status", progress) → Update progress
3. write_memory("checkpoint_[timestamp]", full_state) → Create checkpoint

# Session end
1. write_memory("workflow_summary", final_state) → Save summary
2. list_memories() → Verify persistence
```

## Progress Tracking

### Visual Progress Indicators

```
Workflow: E-commerce Platform
Progress: ████████████████░░░░ 80% Complete

Phase 1: Discovery        ✅ COMPLETE (Gate 1 ✓ Approved)
  └─ Requirements         ✅ requirements.md
  └─ User Stories         ✅ user_stories.md
  └─ Tech Stack           ✅ tech_stack_analysis.md

Phase 2: Architecture     ✅ COMPLETE (Gate 2 ✓ Approved)
  └─ System Design        ✅ system_architecture.md
  └─ Database Schema      ✅ database_schema.md
  └─ API Specification    ✅ api_specification.md

Phase 3: Implementation   🔄 IN PROGRESS (Wave 2/3)
  ├─ Wave 1: Foundation   ✅ COMPLETE
  │   ├─ Frontend Setup   ✅ Complete
  │   ├─ Backend Setup    ✅ Complete
  │   └─ Database Setup   ✅ Complete
  ├─ Wave 2: Features     🔄 IN PROGRESS
  │   ├─ Frontend Comp.   ✅ 8/10 Complete
  │   ├─ Backend APIs     🔄 5/8 In Progress
  │   └─ DB Operations    ⏳ 0/6 Pending
  └─ Wave 3: Integration  ⏳ PENDING

Phase 4: Testing          ⏳ PENDING (Gate 3 pending)
Phase 5: Deployment       ⏳ PENDING (Gate 4 pending)

Next Action: Complete Backend APIs (3 remaining)
Blocker: None
ETA: 2 days to Phase 3 completion
```

## Output Format

### Workflow Plan Presentation

```markdown
# Workflow Plan: [Project Name]

## Overview
- **Template**: [Template Name]
- **Total Duration**: [Estimated Days]
- **Phases**: 5
- **Validation Gates**: 5
- **Parallel Waves**: [Count]

## Phase Breakdown

### Phase 1: Discovery (20% effort, [X] days)
**Objective**: [Phase objective]

**Sub-Agents**:
- requirements-analyst
- system-architect

**Deliverables**:
1. requirements.md
2. user_stories.md
3. tech_stack_analysis.md

**Validation Gate 1**:
- Criteria: [Specific criteria]
- Approval Required: Yes

### Phase 2: Architecture (15% effort, [X] days)
[Similar structure...]

### Phase 3: Implementation (45% effort, [X] days)
**Wave 1 (Parallel)**:
- frontend-specialist → UI foundation
- backend-specialist → API foundation
- database-specialist → Schema setup

**Wave 2 (Parallel)**:
- frontend-specialist → Feature components
- backend-specialist → API endpoints
- database-specialist → Queries

**Wave 3 (Integration)**:
- integration-specialist → Connect all layers

**Validation Gate 3**:
- Criteria: Code review + tests pass
- Approval Required: Yes

[Continue for remaining phases...]

## Approval
Do you approve this workflow plan? (Reply: approve/modify)
```

## Integration with Other Commands

### Command Combinations

**Discovery Phase**:
```
/sc:workflow "Project" --start-phase 1
  ↓ Triggers
/sc:brainstorm @requirements
  ↓ Then
/sc:analyze-spec @requirements.md
```

**Architecture Phase**:
```
/sc:workflow resume
  ↓ Phase 2 activates
/sc:design system --architecture
  ↓ Then
/sc:document architecture
```

**Implementation Phase**:
```
/sc:workflow resume
  ↓ Phase 3 wave execution
/sc:implement @features --waves 3
  ↓ Each wave runs
/sc:test --functional
```

**Testing Phase**:
```
/sc:workflow resume
  ↓ Phase 4 activates
/sc:test --comprehensive
  ↓ Then
/sc:improve --quality
```

**Deployment Phase**:
```
/sc:workflow resume
  ↓ Phase 5 activates
/sc:git commit-phase
  ↓ Then
Deploy to production
```

## Examples

### Example 1: Full-Stack Application

**Input**:
```
/sc:workflow "Task Management App" --template fullstack
```

**Output** (abbreviated):
```
📋 Workflow Plan Generated: Task Management App

Template: Full-Stack Web Application
Duration: 10-16 days
Phases: 5 | Gates: 5 | Waves: 9

Phase 1: Discovery (2-3 days)
├─ requirements-analyst → requirements.md
├─ requirements-analyst → user_stories.md
└─ system-architect → tech_stack_analysis.md
Validation Gate 1: Requirements approval

Phase 2: Architecture (1-2 days)
├─ system-architect → system_architecture.md
├─ database-architect → database_schema.md
└─ api-architect → api_specification.md
Validation Gate 2: Architecture review

Phase 3: Implementation (6-10 days)
Wave 1 (Parallel):
  ├─ frontend-specialist → React setup + routing
  ├─ backend-specialist → Express server + auth
  └─ database-specialist → PostgreSQL + migrations
Wave 2 (Parallel):
  ├─ frontend-specialist → Task components
  ├─ backend-specialist → Task APIs
  └─ database-specialist → Task queries
Wave 3 (Integration):
  └─ integration-specialist → Connect frontend ↔ backend

Validation Gate 3: Code review + tests

Phase 4: Testing (1-2 days)
├─ Playwright E2E tests
├─ Integration tests
└─ Performance benchmarks
Validation Gate 4: All tests pass

Phase 5: Deployment (0.5-1 day)
├─ Production build
├─ Deploy to hosting
└─ Monitoring setup
Validation Gate 5: Live deployment

✅ Workflow plan ready. Approve to begin? (yes/modify/cancel)
```

### Example 2: Resume Workflow from Checkpoint

**Input**:
```
/sc:workflow resume
```

**Output**:
```
📂 Loading workflow state...

Workflow: Task Management App
Last Checkpoint: 2 hours ago
Current Phase: Phase 3 (Implementation)
Current Wave: Wave 2/3

Progress:
✅ Phase 1: Discovery (COMPLETE)
✅ Phase 2: Architecture (COMPLETE)
🔄 Phase 3: Implementation (IN PROGRESS - 60%)
  ✅ Wave 1: Foundation (COMPLETE)
  🔄 Wave 2: Features (IN PROGRESS)
    ✅ Frontend components: 8/10
    🔄 Backend APIs: 5/8
    ⏳ Database queries: 0/6
  ⏳ Wave 3: Integration (PENDING)
⏳ Phase 4: Testing (PENDING)
⏳ Phase 5: Deployment (PENDING)

Resuming Wave 2 execution...
Next task: Complete remaining 3 backend APIs

Continue? (yes/modify/new-checkpoint)
```

## Related Commands

- `/sc:analyze-spec` - Initial specification analysis before workflow
- `/sc:plan-phase` - Detailed individual phase planning
- `/sc:implement` - Implementation wave execution
- `/sc:test` - Testing phase coordination
- `/sc:spawn` - Complex sub-agent orchestration
- `/sc:task` - Long-term project management
- `/sc:save` - Checkpoint workflow state