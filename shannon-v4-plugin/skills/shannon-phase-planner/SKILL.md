---
name: shannon-phase-planner
display_name: "Shannon Phase Planner"
description: "5-phase implementation planning with effort distribution (Discovery 20%, Architecture 15%, Implementation 45%, Testing 15%, Deployment 5%)"
category: planning
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_plan command"
  - "plan requested"
  - "phase planning needed"
  - "create implementation plan"
mcp_servers:
  required:
    - serena
  recommended:
    - sequential
allowed_tools:
  - Read
  - Glob
  - Grep
  - serena_write_memory
  - serena_read_memory
  - sequential_thinking
progressive_disclosure:
  tier: 1
  metadata_tokens: 200
input:
  spec_analysis:
    type: object
    required: true
    description: "8D complexity analysis from shannon-spec-analyzer"
  north_star_goal:
    type: string
    required: true
    description: "Project's North Star goal"
  constraints:
    type: object
    required: false
    description: "Time, budget, resource constraints"
output:
  phase_plan:
    type: object
    description: "Complete 5-phase implementation plan"
  wave_structure:
    type: array
    description: "Wave groupings for each phase"
  validation_gates:
    type: array
    description: "Validation criteria for phase transitions"
---

# Shannon Phase Planner

> **Planning Specialist**: Decomposes project specifications into actionable 5-phase execution plans with wave-based task grouping and validation gates

## Purpose

Creates comprehensive implementation plans following Shannon's 5-phase methodology:
- **Discovery (20%)**: Requirements, research, context gathering
- **Architecture (15%)**: System design, technology decisions
- **Implementation (45%)**: Core development work
- **Testing (15%)**: Validation, quality assurance
- **Deployment (5%)**: Release, monitoring

## Key Innovation: Effort-Proportioned Planning

Shannon's 5-phase model distributes effort based on empirical data showing that:
- **20% upfront discovery** prevents costly rework
- **15% architecture** establishes foundation
- **45% implementation** is realistic (not 80% as commonly assumed)
- **15% testing** ensures quality (functional, no mocks)
- **5% deployment** handles release mechanics

## Capabilities

1. **Spec Analysis Integration**: Loads 8D complexity analysis
2. **Phase Decomposition**: Breaks project into 5 phases
3. **Wave Grouping**: Organizes tasks into dependency waves
4. **Effort Estimation**: Distributes effort across phases (20-15-45-15-5%)
5. **Validation Gates**: Defines phase transition criteria
6. **Risk Assessment**: Identifies blockers and dependencies
7. **Context Preservation**: Saves plan to Serena MCP

## Execution Algorithm

### Step 1: Load Context

```javascript
// Load spec analysis
const spec = await serena_read_memory("spec_analysis_[timestamp]");
const {complexity_score, domain_analysis, tech_stack, dimensions} = spec;

// Load North Star goal
const north_star = await serena_read_memory("north_star_goal");

// Load constraints (if any)
const constraints = await serena_read_memory("project_constraints");
```

### Step 2: Analyze Complexity for Planning

Use Sequential MCP for structured planning:

```javascript
const planning_analysis = await sequential_thinking({
  thought: "Analyzing project complexity for phase planning...",
  thoughtNumber: 1,
  totalThoughts: 5,
  context: {
    complexity_score: spec.complexity_score,
    dimensions: spec.dimensions,
    north_star: north_star
  }
});
```

**Complexity-Based Adjustments**:
- **Low complexity (0.0-0.3)**: Can compress Discovery to 15%, boost Implementation to 50%
- **Medium complexity (0.3-0.7)**: Standard 20-15-45-15-5% distribution
- **High complexity (0.7-1.0)**: Expand Discovery to 25%, Architecture to 20%, reduce Implementation to 40%

### Step 3: Phase 1 Planning - Discovery (20%)

**Objectives**:
- Understand complete project scope
- Gather technical context
- Identify dependencies and risks
- Establish coding standards
- Define success criteria

**Wave Structure**:

**Wave 1: Requirements Gathering** (parallel)
- Load existing documentation
- Identify stakeholders
- Extract functional requirements
- Extract non-functional requirements

**Wave 2: Technical Research** (parallel)
- Framework documentation (Context7 MCP)
- Dependency analysis
- Technology feasibility assessment
- Security and compliance requirements

**Wave 3: Context Building** (parallel)
- Codebase analysis (if existing)
- Database schema understanding
- API contracts review
- Integration points mapping

**Validation Gate: Discovery Complete**
- ✅ Requirements documented
- ✅ Technical feasibility confirmed
- ✅ Dependencies identified
- ✅ Risks assessed
- ✅ Context preserved in Serena

### Step 4: Phase 2 Planning - Architecture (15%)

**Objectives**:
- Design system architecture
- Make technology decisions
- Define module boundaries
- Establish data models
- Create API contracts

**Wave Structure**:

**Wave 1: Architectural Design** (sequential - analysis required)
- System architecture diagram
- Technology stack finalization
- Module structure definition
- Database schema design

**Wave 2: Contracts & Interfaces** (parallel)
- API contract definitions
- Data model specifications
- Integration interfaces
- Authentication/authorization design

**Wave 3: Infrastructure Planning** (parallel)
- Environment setup (dev, staging, prod)
- CI/CD pipeline design
- Monitoring and logging strategy
- Deployment architecture

**Validation Gate: Architecture Complete**
- ✅ Architecture documented and reviewed
- ✅ Technology decisions justified
- ✅ Contracts defined
- ✅ Infrastructure plan validated

### Step 5: Phase 3 Planning - Implementation (45%)

**Objectives**:
- Build core functionality
- Implement features
- Follow specifications strictly
- Maintain code quality
- Progressive feature delivery

**Wave Structure** (Example - actual waves depend on dependencies):

**Wave 1: Foundation**
- Database setup and migrations
- Authentication system
- Core data models
- Base API structure

**Wave 2: Core Features** (parallel where possible)
- Feature A implementation
- Feature B implementation
- Feature C implementation

**Wave 3: Integration** (sequential - requires Wave 2)
- Feature integration
- Cross-module connections
- Data flow implementation

**Wave 4: Refinement** (parallel)
- Error handling
- Logging and monitoring
- Performance optimization
- Code quality improvements

**Effort Distribution Within Implementation**:
- Foundation: 20% of implementation phase
- Core features: 50% of implementation phase
- Integration: 20% of implementation phase
- Refinement: 10% of implementation phase

**Validation Gate: Implementation Complete**
- ✅ All features implemented per spec
- ✅ Code quality standards met
- ✅ No spec deviations
- ✅ Integration points working

### Step 6: Phase 4 Planning - Testing (15%)

**Objectives**:
- Functional validation (NO MOCKS)
- Integration testing
- End-to-end testing
- Accessibility validation (if applicable)
- Performance testing

**Wave Structure**:

**Wave 1: Functional Testing** (parallel)
- Core feature functional tests
- API endpoint testing (real HTTP requests)
- Database operations testing (real database)
- Authentication flow testing (real authentication)

**Wave 2: Integration Testing** (sequential - requires Wave 1)
- Cross-module integration tests
- External service integration tests
- Data flow validation

**Wave 3: End-to-End Testing** (parallel)
- User journey testing (Puppeteer/Playwright for web)
- Critical path validation
- Error scenario testing

**Wave 4: Quality Assurance** (parallel)
- Accessibility testing (WCAG compliance)
- Performance testing
- Security testing
- Code review

**NO MOCKS Philosophy**:
- All tests use real browsers (Puppeteer/Playwright)
- All tests use real databases (Testcontainers or dedicated test DB)
- All HTTP requests are real (no axios-mock-adapter)
- Integration tests use real services

**Validation Gate: Testing Complete**
- ✅ All functional tests pass
- ✅ Integration tests pass
- ✅ End-to-end tests pass
- ✅ Quality standards met
- ✅ No critical bugs

### Step 7: Phase 5 Planning - Deployment (5%)

**Objectives**:
- Prepare production environment
- Deploy application
- Configure monitoring
- Verify production functionality
- Document deployment

**Wave Structure**:

**Wave 1: Pre-Deployment** (sequential)
- Production environment validation
- Database migrations (production)
- Configuration management
- Security audit

**Wave 2: Deployment** (sequential)
- Deploy to production
- Smoke tests (real production)
- Rollback plan validation

**Wave 3: Post-Deployment** (parallel)
- Monitoring setup verification
- Performance baseline establishment
- Documentation finalization
- Team handoff

**Validation Gate: Deployment Complete**
- ✅ Application running in production
- ✅ Smoke tests pass
- ✅ Monitoring operational
- ✅ Documentation complete
- ✅ Project delivered

### Step 8: Generate Phase Plan Document

Create comprehensive phase plan:

```javascript
const phase_plan = {
  project_id: generate_project_id(),
  north_star_goal: north_star,
  complexity_score: spec.complexity_score,

  effort_distribution: {
    discovery: "20%",
    architecture: "15%",
    implementation: "45%",
    testing: "15%",
    deployment: "5%"
  },

  phases: [
    {
      name: "Phase 1: Discovery",
      effort: "20%",
      objectives: [...],
      waves: [...],
      validation_gate: {...}
    },
    {
      name: "Phase 2: Architecture",
      effort: "15%",
      objectives: [...],
      waves: [...],
      validation_gate: {...}
    },
    // ... remaining phases
  ],

  total_waves: count_waves(),
  estimated_duration: estimate_duration(complexity_score, constraints),
  critical_path: identify_critical_path(),
  risks: assess_risks()
};
```

### Step 9: Save to Serena MCP

```javascript
// Save complete phase plan
await serena_write_memory("phase_plan_detailed", phase_plan);

// Save summary for quick reference
await serena_write_memory("phase_plan_summary", {
  phases: 5,
  waves: phase_plan.total_waves,
  estimated_duration: phase_plan.estimated_duration,
  current_phase: 1,
  current_wave: null
});

// Create knowledge graph entity
await serena_create_entities([{
  name: "phase_plan_" + project_id,
  type: "plan",
  metadata: phase_plan
}]);

// Link to project
await serena_create_relations([{
  from: project_id,
  to: "phase_plan_" + project_id,
  type: "has_plan"
}]);
```

### Step 10: Generate Planning SITREP

Generate standardized SITREP using shannon-status-reporter:

```javascript
// Generate planning SITREP
const sitrep_data = {
  agent_name: "shannon-phase-planner",
  task_id: `phase_plan_${project_id}_${timestamp}`,
  current_phase: "Planning",
  progress: 100, // Planning complete
  state: "completed",

  objective: `Create 5-phase implementation plan for: ${north_star_goal}`,
  scope: [
    "5-phase structure (Discovery, Architecture, Implementation, Testing, Deployment)",
    `${total_waves} waves across all phases`,
    "Validation gates and success criteria",
    "Complexity-adjusted effort distribution"
  ],
  dependencies: ["spec_analysis", "north_star_goal"],

  findings: [
    `Complexity score: ${complexity_score} (${complexity_dimensions.length} dimensions)`,
    `Total waves: ${total_waves}`,
    `Estimated duration: ${estimated_duration}`,
    `Effort distribution: ${effort_distribution.join(', ')}`,
    `Critical path: ${critical_path_length} sequential dependencies`,
    `Identified risks: ${risks.length} (${high_priority_risks.length} high-priority)`
  ],

  blockers: [],
  risks: risks.map(r => r.description),
  questions: [],

  next_steps: [
    "Review and approve this plan",
    `Begin Phase 1, Wave 1: ${phases[0].waves[0].name}`,
    "Use /sh:wave 1 to execute first wave"
  ],

  artifacts: [
    `phase_plan_detailed (saved to Serena)`,
    `wave_structure.json`,
    `validation_gates.json`,
    `risk_matrix.json`
  ],

  tests_executed: [
    "complexity_analysis",
    "dependency_validation",
    "wave_grouping",
    "effort_distribution_check"
  ],
  test_results: "All planning validations passed"
};

// Invoke shannon-status-reporter to generate SITREP
const sitrep = await generate_sitrep(sitrep_data);

// Save SITREP alongside phase plan
await serena_write_memory(`phase_plan_${project_id}_sitrep`, {
  sitrep_markdown: sitrep,
  sitrep_data,
  full_plan_summary: phases.map(p => ({
    phase: p.name,
    waves: p.waves.length,
    objectives: p.objectives
  }))
});

return sitrep;
```

## Complexity-Based Adjustments

### Low Complexity Projects (0.0-0.3)

**Example**: Simple CRUD app, static website

**Adjusted Effort**:
- Discovery: 15% (less research needed)
- Architecture: 10% (simpler design)
- Implementation: 55% (more straightforward)
- Testing: 15% (standard)
- Deployment: 5% (standard)

**Rationale**: Simpler projects need less upfront planning

### Medium Complexity Projects (0.3-0.7)

**Example**: Full-stack web app, mobile app

**Standard Effort**: 20-15-45-15-5%

**Rationale**: Balanced approach for typical projects

### High Complexity Projects (0.7-1.0)

**Example**: Distributed systems, complex integrations

**Adjusted Effort**:
- Discovery: 25% (extensive research)
- Architecture: 20% (critical design phase)
- Implementation: 40% (reduced percentage, but still major phase)
- Testing: 10% (continuous throughout)
- Deployment: 5% (standard)

**Rationale**: Complex projects require more upfront planning to avoid costly rework

## Wave Dependency Analysis

**Independence Check**:
```javascript
function can_execute_parallel(task_a, task_b) {
  // Check if tasks can run in parallel
  return !has_dependency(task_a, task_b) &&
         !has_dependency(task_b, task_a) &&
         !shares_mutable_resources(task_a, task_b);
}
```

**Wave Grouping Algorithm**:
```javascript
function group_into_waves(tasks) {
  const waves = [];
  let remaining = [...tasks];

  while (remaining.length > 0) {
    const wave = [];
    const next_remaining = [];

    for (const task of remaining) {
      // Can this task run in current wave?
      const dependencies_satisfied = task.dependencies.every(
        dep => completed_tasks.includes(dep)
      );

      const no_conflicts = wave.every(
        wave_task => can_execute_parallel(task, wave_task)
      );

      if (dependencies_satisfied && no_conflicts) {
        wave.push(task);
      } else {
        next_remaining.push(task);
      }
    }

    waves.push(wave);
    remaining = next_remaining;
  }

  return waves;
}
```

## Integration with Shannon v4

**Command Flow**:
```
/sh:plan → shannon-phase-planner activates
  ↓
Loads spec analysis from Serena
  ↓
Uses sequential thinking for planning
  ↓
Generates 5-phase plan with waves
  ↓
Invokes shannon-status-reporter to generate planning SITREP
  ↓
Saves plan and SITREP to Serena for wave execution
  ↓
Returns planning SITREP
```

**Wave Execution Integration**:
```
Phase plan saved → shannon-wave-orchestrator loads plan
  ↓
/sh:wave 1 → Execute first wave of current phase
  ↓
Validation gate → Move to next wave or next phase
```

## Validation Rules

**Phase Plan Must Include**:
- ✅ All 5 phases defined
- ✅ Effort distribution sums to 100%
- ✅ Each phase has objectives
- ✅ Each phase has waves
- ✅ Validation gates defined
- ✅ Dependencies mapped
- ✅ Risks identified

**Wave Structure Must Include**:
- ✅ Wave number and name
- ✅ Task list
- ✅ Dependency relationships
- ✅ Parallelization opportunities
- ✅ Validation criteria

## Examples

### Example 1: Simple React Dashboard

**Input**:
```yaml
Spec Analysis:
  complexity: 0.35
  domains:
    frontend: 80% (React 18, Vite)
    backend: 20% (REST API integration)
```

**Output**:
```yaml
Phase Plan:
  phases: 5
  waves: 8 total

  Phase 1: Discovery (15%)
    Wave 1: Requirements gathering (2 days)
    Wave 2: React patterns research (1 day)
    Validation: Requirements doc complete

  Phase 2: Architecture (10%)
    Wave 1: Component architecture (2 days)
    Validation: Architecture reviewed

  Phase 3: Implementation (55%)
    Wave 1: Setup React + Vite (1 day)
    Wave 2: Core components (4 days)
    Wave 3: API integration (2 days)
    Wave 4: Styling and polish (1 day)
    Validation: All features complete

  Phase 4: Testing (15%)
    Wave 1: Component tests (Playwright) (2 days)
    Wave 2: E2E tests (1 day)
    Validation: All tests pass

  Phase 5: Deployment (5%)
    Wave 1: Deploy to Vercel (1 day)
    Validation: Production functional
```

**SITREP Output (Example 1)**:
```markdown
## SITREP: shannon-phase-planner - phase_plan_reactdashboard_1730739600000

### Status
- **Current Phase**: Planning
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: Create 5-phase implementation plan for: Build React dashboard with charts
- **Scope**: 5-phase structure (Discovery, Architecture, Implementation, Testing, Deployment), 8 waves across all phases, Validation gates and success criteria, Complexity-adjusted effort distribution
- **Dependencies**: spec_analysis, north_star_goal

### Findings
- Complexity score: 0.35 (3 dimensions: frontend, backend, integration)
- Total waves: 8
- Estimated duration: ~3 weeks
- Effort distribution: 15%, 10%, 55%, 15%, 5%
- Critical path: 5 sequential phase dependencies
- Identified risks: 2 (0 high-priority)

### Issues
- **Blockers**: None
- **Risks**: API integration complexity, React state management patterns
- **Questions**: None

### Next Steps
- [ ] Review and approve this plan
- [ ] Begin Phase 1, Wave 1: Requirements gathering
- [ ] Use /sh:wave 1 to execute first wave

### Artifacts
- phase_plan_detailed (saved to Serena)
- wave_structure.json
- validation_gates.json
- risk_matrix.json

### Validation
- **Tests Executed**: complexity_analysis, dependency_validation, wave_grouping, effort_distribution_check
- **Results**: All planning validations passed
```

### Example 2: Complex Full-Stack SaaS

**Input**:
```yaml
Spec Analysis:
  complexity: 0.78
  domains:
    frontend: 40% (Next.js 14, React 18)
    backend: 40% (Node.js, Express, PostgreSQL)
    devops: 20% (Docker, AWS)
```

**Output**:
```yaml
Phase Plan:
  phases: 5
  waves: 18 total

  Phase 1: Discovery (25%)
    Wave 1: Requirements and stakeholder interviews (5 days)
    Wave 2: Technical research (Next.js 14, Prisma, AWS) (4 days)
    Wave 3: Codebase analysis and context (3 days)
    Wave 4: Security and compliance requirements (2 days)
    Validation: Comprehensive requirements doc

  Phase 2: Architecture (20%)
    Wave 1: System architecture design (4 days)
    Wave 2: Database schema design (3 days)
    Wave 3: API contracts (2 days)
    Wave 4: Infrastructure design (AWS, Docker) (2 days)
    Validation: Architecture approved by tech lead

  Phase 3: Implementation (40%)
    Wave 1: Foundation (DB, auth, base API) (5 days)
    Wave 2: Core backend features (parallel) (6 days)
    Wave 3: Core frontend features (parallel) (6 days)
    Wave 4: Integration (4 days)
    Wave 5: Refinement (3 days)
    Validation: All features per spec complete

  Phase 4: Testing (10%)
    Wave 1: API functional tests (3 days)
    Wave 2: Frontend E2E tests (Playwright) (3 days)
    Wave 3: Integration tests (2 days)
    Validation: 100% critical path coverage

  Phase 5: Deployment (5%)
    Wave 1: AWS infrastructure (ECS, RDS) (2 days)
    Wave 2: Deploy and smoke tests (1 day)
    Wave 3: Monitoring setup (1 day)
    Validation: Production operational
```

### Example 3: iOS Mobile App

**Input**:
```yaml
Spec Analysis:
  complexity: 0.62
  domains:
    mobile: 90% (Swift, SwiftUI, iOS 17+)
    backend: 10% (REST API integration)
```

**Output**:
```yaml
Phase Plan:
  phases: 5
  waves: 12 total

  Phase 1: Discovery (20%)
    Wave 1: App Store requirements (2 days)
    Wave 2: SwiftUI patterns research (2 days)
    Wave 3: API contract review (1 day)
    Validation: Requirements complete

  Phase 2: Architecture (15%)
    Wave 1: App architecture (MVVM) (3 days)
    Wave 2: Navigation structure (1 day)
    Wave 3: Data layer design (1 day)
    Validation: Architecture doc approved

  Phase 3: Implementation (45%)
    Wave 1: Project setup (Xcode, SPM) (1 day)
    Wave 2: Core views (3 days)
    Wave 3: Navigation and state (2 days)
    Wave 4: API integration (2 days)
    Wave 5: Polish and animations (1 day)
    Validation: All views implemented

  Phase 4: Testing (15%)
    Wave 1: XCTest unit tests (2 days)
    Wave 2: UI tests (Puppeteer via xcode MCP) (2 days)
    Validation: Tests pass

  Phase 5: Deployment (5%)
    Wave 1: TestFlight beta (1 day)
    Wave 2: App Store submission (1 day)
    Validation: App live on App Store
```

## Anti-Patterns to Avoid

### ❌ DON'T: Skip Discovery or Architecture

**Wrong**:
```
Jump straight to implementation without planning
```

**Why Wrong**: Leads to costly rework, scope creep, technical debt

**Correct**:
```
Phase 1: Discovery (20%) → Phase 2: Architecture (15%) → Phase 3: Implementation
```

### ❌ DON'T: Assume Implementation is 80% of Work

**Wrong**:
```yaml
Effort Distribution:
  implementation: 80%
  everything else: 20%
```

**Why Wrong**: Ignores planning, testing, deployment complexity

**Correct**:
```yaml
Effort Distribution:
  discovery: 20%
  architecture: 15%
  implementation: 45%
  testing: 15%
  deployment: 5%
```

### ❌ DON'T: Create Phases Without Validation Gates

**Wrong**:
```
Phase 1 → Phase 2 → Phase 3 (no gates, automatic progression)
```

**Why Wrong**: Can't verify phase completion, quality at risk

**Correct**:
```
Phase 1 → [Validation Gate] → Phase 2 → [Validation Gate] → Phase 3
```

### ❌ DON'T: Ignore Dependencies in Wave Planning

**Wrong**:
```
Wave 1: [All tasks in parallel regardless of dependencies]
```

**Why Wrong**: Tasks fail due to missing prerequisites

**Correct**:
```
Analyze dependencies → Group independent tasks → Create sequential waves
```

## Success Criteria

A valid phase plan must satisfy:

1. **Completeness**: All 5 phases present
2. **Effort Balance**: Distribution sums to 100%
3. **Wave Structure**: Each phase has logical wave groupings
4. **Dependencies**: All dependencies mapped
5. **Validation Gates**: Clear criteria for phase transitions
6. **Risk Assessment**: Potential blockers identified
7. **Context Preserved**: Plan saved to Serena MCP

---

**Shannon V4** - 5-Phase Planning for Methodical Execution 📋
