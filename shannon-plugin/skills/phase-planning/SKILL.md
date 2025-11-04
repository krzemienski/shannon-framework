---
name: phase-planning
description: |
  Generate 5-phase implementation plan with validation gates and resource allocation. Adapts
  phase count and timeline based on complexity score. Includes validation gates between phases.
  Use when: planning implementation, need structured timeline, want validation checkpoints.

skill-type: PROTOCOL
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      purpose: Phase storage and retrieval

allowed-tools: Read, Serena
---

# Phase Planning Skill

## Overview

The phase-planning skill generates structured, complexity-adaptive implementation plans using a 5-phase framework with validation gates. It adapts phase count and timeline distribution based on project complexity, ensuring appropriate rigor for simple scripts through critical systems.

**When to Use**:
- Planning implementation after spec analysis complete
- Need structured timeline with validation checkpoints
- Want systematic progression with quality gates
- Require resource allocation and effort distribution

**Key Features**:
- Complexity-adaptive phase structure (3-5+ phases)
- Validation gates between phases
- Timeline distribution based on complexity
- Integration with wave orchestration
- Serena memory preservation

---

## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically rationalize skipping or adjusting phase planning patterns. Below are the 4 most common rationalizations detected in baseline testing, with mandatory counters.

### Rationalization 1: "Let's skip to waves, phases are redundant"
**Example**: User says "Let's create the wave execution plan" → Agent responds "That wave structure looks reasonable..." and skips phase planning entirely

**COUNTER**:
- ❌ **NEVER** skip phase planning when user jumps to waves
- ✅ Phases structure work; waves coordinate agents
- ✅ Phases MUST come before waves (phases define WHAT, waves define WHO)
- ✅ If user suggests waves first, respond: "First we need phase planning to structure the work, THEN we can create waves"

**Rule**: Phases always precede waves. No exceptions.

### Rationalization 2: "3 phases work for everything, keep it simple"
**Example**: User says "Let's use Setup-Build-Deploy for this 0.72 complexity project" → Agent responds "That simplified structure makes sense..."

**COUNTER**:
- ❌ **NEVER** accept 3-phase template for complex projects
- ✅ Complexity score determines phase count (algorithm, not preference)
- ✅ 0.70-0.85 complexity REQUIRES 5 phases + extended gates
- ✅ Simplification bias under-estimates effort by 40-60%
- ✅ "Keep it simple" means follow the algorithm, not skip rigor

**Rule**: Apply complexity-based adaptation. Simple ≠ fewer phases for complex work.

### Rationalization 3: "Validation gates are overhead, team will coordinate naturally"
**Example**: User says "We don't need formal gates" → Agent creates phases without validation criteria

**COUNTER**:
- ❌ **NEVER** omit validation gates to reduce "overhead"
- ✅ Gates prevent downstream failures (catch issues early)
- ✅ "Natural coordination" = unvalidated assumptions = technical debt
- ✅ Gates take 5-10 minutes to define, prevent hours of rework
- ✅ Every phase transition MUST have explicit success criteria

**Rule**: Every phase MUST have validation gate. Not optional.

### Rationalization 4: "Timeline percentages feel wrong, adjust them"
**Example**: User says "20% for setup feels too long" → Agent adjusts to 5% based on intuition

**COUNTER**:
- ❌ **NEVER** adjust timeline distribution based on "feeling"
- ✅ Percentages are algorithmic (complexity + domain adjustments)
- ✅ If percentages feel wrong, the algorithm is right
- ✅ "Feels too long" often means under-estimating hidden complexity
- ✅ Only recalculate if you find FORMULA ERROR (wrong calculation, wrong weights)

**Rule**: Follow timeline distribution formula. Intuition doesn't override math.

### Detection Signal
**If you're tempted to**:
- Skip phases and go to waves
- Use 3 phases regardless of complexity
- Omit validation gates
- Adjust timeline percentages subjectively

**Then you are rationalizing.** Stop. Follow the protocol. Apply the algorithm.

---

## Core Algorithm

### 5-Phase Framework

```
Phase 1: Foundation & Setup (10-20% timeline)
├─ Infrastructure, tooling, environment
├─ Project scaffolding, dependencies
└─ Initial configuration

Phase 2: Core Implementation (30-40% timeline)
├─ Primary functionality
├─ Core algorithms and logic
└─ Essential features

Phase 3: Integration & Enhancement (20-30% timeline)
├─ Service integration
├─ Advanced features
└─ Cross-component functionality

Phase 4: Quality & Polish (15-25% timeline)
├─ Testing (NO MOCKS)
├─ Performance optimization
└─ Code refinement

Phase 5: Deployment & Handoff (10-15% timeline)
├─ Production deployment
├─ Documentation
└─ Knowledge transfer
```

### Complexity-Based Adaptation

**Simple (0.00-0.30)**: 3 phases
```
Phase 1: Setup & Core (30%)
Phase 2: Features & Testing (50%)
Phase 3: Deploy (20%)
```

**Moderate (0.30-0.50)**: 3-4 phases
```
Phase 1: Setup (20%)
Phase 2: Implementation (45%)
Phase 3: Testing (25%)
Phase 4: Deploy (10%)
```

**Complex (0.50-0.70)**: 5 phases (standard)
```
All 5 phases with standard distribution
```

**High (0.70-0.85)**: 5 phases + extended
```
All 5 phases + extended validation gates
+ Risk mitigation checkpoints
+ Progress review gates
```

**Critical (0.85-1.00)**: 5 phases + risk mitigation
```
All 5 phases + risk mitigation phases
+ Extensive validation gates
+ Architecture review gates
+ Security review gates
+ Performance validation gates
```

## Implementation Protocol

### Step 1: Load Context

```
REQUIRED INPUTS:
1. read_memory("spec_analysis") - Get complexity score
2. read_memory("8d_assessment") - Get domain breakdown
3. Current specification document
4. Project timeline constraints

EXTRACT:
- Complexity score: [0.0-1.0]
- Total timeline: [hours/days]
- Domain percentages: {frontend, backend, database, ...}
- Critical requirements: [list]
```

### Step 2: Determine Phase Structure

```python
def determine_phase_count(complexity: float) -> int:
    if complexity < 0.30:
        return 3  # Simple
    elif complexity < 0.50:
        return 4  # Moderate (3-4 flexible)
    elif complexity < 0.70:
        return 5  # Complex
    elif complexity < 0.85:
        return 5  # High (+ extended gates)
    else:
        return 6  # Critical (+ risk mitigation)
```

### Step 3: Calculate Timeline Distribution

**Standard 5-Phase Distribution**:
```
Phase 1: 15% (10-20% range)
Phase 2: 35% (30-40% range)
Phase 3: 25% (20-30% range)
Phase 4: 20% (15-25% range)
Phase 5: 5% (10-15% range)
```

**Complexity Adjustments**:
```
Simple (0.00-0.30):
  Phase 1: +5% (more setup proportionally)
  Phase 2: +10% (straightforward implementation)
  Phase 3: -15% (less integration complexity)

Complex (0.50-0.70):
  Phase 1: +5% (more planning needed)
  Phase 2: -5% (parallel execution helps)
  Phase 3: +5% (more integration work)
  Phase 4: -5% (offset)

High (0.70-0.85):
  Phase 1: +10% (extensive planning)
  Phase 2: -10% (higher coordination overhead)
  Phase 3: +5% (complex integration)
  Phase 4: +5% (rigorous testing)

Critical (0.85-1.00):
  Phase 1: +15% (exhaustive planning)
  Phase 2: -15% (very high coordination)
  Phase 3: +5% (critical integration)
  Phase 4: +10% (extensive testing)
  Phase 5: +5% (careful deployment)
```

**Domain-Based Adjustments**:
```
If Frontend-Heavy (>50%):
  Phase 2: +5% (UI work time-consuming)
  Phase 4: +5% (E2E testing)
  Phase 5: -10% (static hosting simpler)

If Backend-Heavy (>50%):
  Phase 1: +5% (API design critical)
  Phase 4: +5% (integration testing complex)
  Phase 2: -10% (offset)

If Database-Heavy (>30%):
  Phase 1: +5% (schema design critical)
  Phase 2: -5% (offset from Phase 1)
```

### Step 4: Define Validation Gates

**Phase 1 → Phase 2 Gate**:
```
Criteria:
☐ Requirements fully documented
☐ Technical approach confirmed
☐ All dependencies identified
☐ Environment setup complete
☐ No blocking unknowns

Verification:
- Review requirements.md completeness
- Verify all MCPs installed
- Confirm technical stack validated
- Check for unresolved questions
```

**Phase 2 → Phase 3 Gate**:
```
Criteria:
☐ Core functionality complete
☐ Unit tests passing
☐ Code review completed
☐ Performance acceptable
☐ No critical bugs

Verification:
- Run test suite (100% pass required)
- Execute code quality checks
- Measure performance benchmarks
- Review bug tracker
```

**Phase 3 → Phase 4 Gate**:
```
Criteria:
☐ All integrations working
☐ Advanced features complete
☐ Integration tests passing
☐ API contracts validated
☐ Cross-component flows verified

Verification:
- Test all service integrations
- Verify API endpoint responses
- Check data flow end-to-end
- Validate authentication/authorization
```

**Phase 4 → Phase 5 Gate**:
```
Criteria:
☐ All tests passing (NO MOCKS)
☐ Code coverage >= 80%
☐ Performance optimized
☐ Documentation complete
☐ Security audit passed

Verification:
- Run full test suite
- Generate coverage report
- Execute performance benchmarks
- Review security checklist
- Verify documentation completeness
```

**Phase 5 → Complete Gate**:
```
Criteria:
☐ Deployed to staging
☐ Smoke tests passing
☐ Deployment docs complete
☐ Handoff checklist complete
☐ Production-ready

Verification:
- Test staging environment
- Run smoke test suite
- Review deployment guide
- Complete knowledge transfer
```

### Step 5: Create Wave Mapping (Phase 3)

**Determine Parallelization**:
```
IF complexity >= 0.5 AND multiple domains >= 30% THEN:
  Use parallel wave execution

Wave Pattern 1 (Two Parallel + Integration):
  Wave 3a: Frontend (parallel)
  Wave 3b: Backend + Database (parallel)
  Wave 3c: Integration (sequential)

Wave Pattern 2 (Three Parallel + Integration):
  Wave 3a: Frontend (parallel)
  Wave 3b: Backend (parallel)
  Wave 3c: Database (parallel)
  Wave 3d: Integration (sequential)

Wave Pattern 3 (Sequential):
  Wave 3a: All implementation (sequential)
```

### Step 6: Generate Phase Plan Document

**Output Structure**:
```markdown
# Implementation Plan: [Project Name]

## Executive Summary
- Complexity Score: [0.0-1.0]
- Phase Count: [3-6]
- Total Timeline: [X hours/days]
- Parallelization: [Yes/No]

## Phase Breakdown

### Phase 1: Foundation & Setup ([X%] - [Y hours])
**Objectives**:
- [Objective 1]
- [Objective 2]

**Key Activities**:
1. [Activity 1] (Z% of phase)
2. [Activity 2] (W% of phase)

**Deliverables**:
- [Deliverable 1]
- [Deliverable 2]

**Validation Gate**:
☐ Criteria 1
☐ Criteria 2

**Estimated Duration**: [X hours]

[Repeat for all phases...]

## Risk Mitigation (Critical/High only)
[Risk mitigation phases/checkpoints]

## Success Metrics
- Timeline adherence: ±[X]%
- Quality gates: 100% pass rate
- Test coverage: >= 80%
```

### Step 7: Store in Serena Memory

```
write_memory("phase_plan", {
  project_name: string,
  complexity_score: float,
  phase_count: int,
  total_timeline: string,
  phases: [
    {
      number: int,
      name: string,
      percentage: float,
      duration: string,
      objectives: string[],
      activities: string[],
      deliverables: string[],
      validation_criteria: string[]
    }
  ],
  wave_plan: {
    enabled: boolean,
    pattern: string,
    waves: Wave[]
  },
  risk_mitigations: RiskMitigation[],
  created_at: timestamp
})
```

## Usage Examples

### Example 1: Simple Project (Complexity 0.25)

**Input**:
```
Complexity: 0.25
Timeline: 8 hours
Domains: Backend 70%, Frontend 30%
```

**Output**:
```
3-Phase Plan:

Phase 1: Setup & Core (30% - 2.4h)
- Project scaffolding
- Backend API implementation
- Basic frontend

Phase 2: Features & Testing (50% - 4h)
- Feature completion
- Integration
- Testing (NO MOCKS)

Phase 3: Deploy (20% - 1.6h)
- Deployment
- Documentation
```

### Example 2: Complex Project (Complexity 0.65)

**Input**:
```
Complexity: 0.65
Timeline: 40 hours
Domains: Frontend 45%, Backend 35%, Database 20%
```

**Output**:
```
5-Phase Plan:

Phase 1: Foundation (20% - 8h)
- Environment setup
- Database schema design
- API contract definition

Phase 2: Core Implementation (35% - 14h)
Wave 2a: Frontend (parallel)
Wave 2b: Backend + DB (parallel)
Wave 2c: Integration (sequential)

Phase 3: Integration (25% - 10h)
- Service integration
- Advanced features
- Cross-component flows

Phase 4: Quality (15% - 6h)
- Comprehensive testing
- Performance optimization
- Code refinement

Phase 5: Deployment (5% - 2h)
- Staging deployment
- Documentation
- Handoff
```

### Example 3: Critical Project (Complexity 0.92)

**Input**:
```
Complexity: 0.92
Timeline: 80 hours
Domains: Frontend 30%, Backend 40%, Database 20%, Security 10%
```

**Output**:
```
6-Phase Plan (5 + Risk Mitigation):

Phase 1: Foundation (25% - 20h)
- Extensive requirements analysis
- Architecture review
- Security planning
- Environment setup

Phase 2: Core Implementation (25% - 20h)
Wave 2a: Frontend (parallel)
Wave 2b: Backend (parallel)
Wave 2c: Database (parallel)
Wave 2d: Integration (sequential)

Phase 3: Integration (20% - 16h)
- Complex service integration
- Security implementation
- Advanced features

Phase 4: Quality (20% - 16h)
- Extensive testing (NO MOCKS)
- Security audit
- Performance testing
- Load testing

Phase 5: Risk Mitigation (5% - 4h)
- Vulnerability scanning
- Penetration testing
- Disaster recovery testing
- Compliance verification

Phase 6: Deployment (5% - 4h)
- Staged rollout
- Monitoring setup
- Comprehensive documentation
- Knowledge transfer
```

## Validation Checklist

Before finalizing phase plan:

**Completeness**:
☐ All phases have clear objectives
☐ Timeline distribution sums to 100%
☐ Each phase has validation criteria
☐ Deliverables clearly defined
☐ Wave execution plan (if applicable)

**Feasibility**:
☐ Timeline matches project constraints
☐ Resource allocation realistic
☐ Dependencies properly sequenced
☐ Parallel work properly identified
☐ Risk mitigations adequate

**Integration**:
☐ Compatible with spec analysis
☐ Aligns with 8D assessment
☐ Matches complexity score
☐ Wave plan matches domain breakdown
☐ Stored in Serena memory

## Integration Points

### With Other Skills

**spec-analysis** → **phase-planning**:
```
Input: Complexity score, domain breakdown
Usage: Determines phase count and distribution
```

**phase-planning** → **wave-orchestration**:
```
Output: Wave execution plan for Phase 2/3
Usage: Parallel execution coordination
```

**phase-planning** → **context-preservation**:
```
Action: Store phase plan in Serena
Usage: Cross-session persistence
```

### With Core Patterns

**PHASE_PLANNING.md**:
```
Reference: Detailed 5-phase framework
Usage: Complete methodology and examples
```

**WAVE_ORCHESTRATION.md**:
```
Coordination: Wave execution within phases
Usage: Parallel implementation patterns
```

**TESTING_PHILOSOPHY.md**:
```
Constraint: NO MOCKS in Phase 4
Usage: Test planning requirements
```

## Common Patterns

### Pattern 1: Simple Script

```
Complexity: < 0.3
Phases: 3
Wave: Sequential
Timeline: < 1 day

Focus: Rapid iteration, minimal overhead
```

### Pattern 2: Standard Application

```
Complexity: 0.3-0.7
Phases: 4-5
Wave: Parallel (Frontend/Backend)
Timeline: 1-5 days

Focus: Structured progression, quality gates
```

### Pattern 3: Critical System

```
Complexity: > 0.85
Phases: 5-6
Wave: Parallel + Sequential integration
Timeline: > 5 days

Focus: Rigorous validation, risk mitigation
```

## Anti-Patterns to Avoid

❌ **Phase Skipping**: Never skip validation gates
❌ **Premature Optimization**: Don't over-engineer simple projects
❌ **Under-Planning**: Don't under-estimate critical systems
❌ **Ignoring Complexity**: Always use complexity score
❌ **Fixed Templates**: Always adapt to project needs

## References

- **PHASE_PLANNING.md**: Complete 5-phase methodology (1562 lines)
- **5-phase-examples.md**: Detailed examples (3 scenarios)
- **phase-template.md**: Reusable phase structure
- **validation-gate.md**: Gate criteria templates

---

**Version**: 1.0.0
**Last Updated**: 2025-11-03
**Shannon Version**: 4.0.0+
