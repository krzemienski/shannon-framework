# Shannon Framework v5.6 - Complete Skills Catalog

**Version**: 5.6.0  
**Total Skills**: 42  
**Last Updated**: November 29, 2025  

---

## Overview

This document provides a complete catalog of all 42 skills in Shannon Framework v5.6.0, organized by enforcement type.

---

## Skills by Enforcement Type

| Type | Count | Description |
|------|-------|-------------|
| RIGID | 5 | Mandatory, no exceptions ever |
| PROTOCOL | 20 | Structured workflows |
| QUANTITATIVE | 8 | Measurable metrics |
| FLEXIBLE | 5 | Adaptable patterns |
| STRUCTURAL | 1 | Architecture tracking |
| ANALYTICAL | 1 | Analysis patterns |
| MONITORING | 1 | Performance tracking |
| SECURITY | 1 | Security scanning |

---

## 1. RIGID Skills (5)

These skills are mandatory and have no exceptions.

### 1.1 using-shannon
```yaml
name: using-shannon
type: RIGID
purpose: Session start workflows establishment
trigger: Session begins
```
**Description**: Establishes Shannon Framework workflows at session start. Enforces 8D analysis before implementation, NO MOCKS testing, wave-based execution for complexity ≥0.50, and Serena checkpointing.

**Iron Laws**:
1. Analyze specifications with 8D scoring BEFORE any implementation
2. Use wave-based execution for complexity ≥0.50
3. Use FUNCTIONAL TESTS ONLY (NO MOCKS)
4. Checkpoint to Serena MCP before context compaction
5. Follow SITREP protocol for multi-agent coordination

---

### 1.2 functional-testing
```yaml
name: functional-testing
type: RIGID
purpose: NO MOCKS enforcement
trigger: Test creation or execution
```
**Description**: Enforces Shannon's NO MOCKS testing philosophy. Prohibits mock objects, stubs, and unit tests. Mandates functional tests with real systems.

**Prohibited**:
- jest.mock(), unittest.mock
- sinon.stub(), sinon.spy()
- @Mock annotations
- In-memory fake databases

**Required**:
- Puppeteer/Playwright for browser tests
- Real database instances (Docker)
- Real API endpoints (staging)
- Real mobile simulators

---

### 1.3 forced-reading-auto-activation
```yaml
name: forced-reading-auto-activation
type: RIGID
purpose: Auto-enforce reading for large content
trigger: Prompt >3000 chars OR file >5000 lines
```
**Description**: Automatically enforces forced-reading-protocol when large prompts or files are detected. Prevents skimming of critical content.

**Triggers**:
- Prompt length >3000 characters
- File references >5000 lines
- Specification keywords detected

---

### 1.4 test-driven-development
```yaml
name: test-driven-development
type: RIGID
purpose: TDD + NO MOCKS
trigger: Feature implementation
```
**Description**: Implements TDD combined with NO MOCKS philosophy. Mandates writing failing test first using REAL systems, then minimal implementation to pass.

**Cycle**:
1. RED: Write failing functional test (real systems)
2. GREEN: Minimal implementation to pass
3. REFACTOR: Improve while staying green

---

### 1.5 forced-reading-protocol
```yaml
name: forced-reading-protocol
type: RIGID (when activated)
purpose: Line-by-line mandatory reading
trigger: Manual or auto-activation
```
**Description**: Mandates complete line-by-line reading of critical documents before synthesis.

**Steps**:
1. PRE-COUNT: Count total lines before reading
2. SEQUENTIAL READING: Read every line from 1 to N
3. VERIFY COMPLETENESS: Confirm lines_read == total_lines
4. SEQUENTIAL SYNTHESIS: Use Sequential MCP for analysis

---

## 2. PROTOCOL Skills (20)

These skills define structured workflows.

### 2.1 context-preservation
```yaml
name: context-preservation
type: PROTOCOL
purpose: Zero-context-loss via checkpoints
trigger: Wave boundaries, PreCompact, session end
```
**Checkpoint Data**:
- Session state
- Wave progress
- Active todos
- Decisions made
- Integration status

---

### 2.2 context-restoration
```yaml
name: context-restoration
type: PROTOCOL
purpose: Restore from checkpoints
trigger: Session resume, /shannon:restore
```
**Restoration Process**:
1. Discover available checkpoints
2. Select appropriate checkpoint
3. Load state from Serena
4. Verify restoration completeness
5. Continue from checkpoint state

---

### 2.3 defense-in-depth
```yaml
name: defense-in-depth
type: PROTOCOL
purpose: Multi-layer validation
trigger: Code quality enforcement
```
**Validation Layers**:
1. Input validation
2. Business logic validation
3. Data layer validation
4. Output validation
5. Integration validation

---

### 2.4 exec
```yaml
name: exec
type: PROTOCOL
purpose: Autonomous 6-phase execution
trigger: /shannon:exec command
```
**Phases**:
1. Library Discovery
2. Implementation
3. Static Analysis (Tier 1)
4. Unit/Integration Tests (Tier 2)
5. Functional Tests (Tier 3 - NO MOCKS)
6. Git Commit

---

### 2.5 executing-plans
```yaml
name: executing-plans
type: PROTOCOL
purpose: Batch execution with validation
trigger: /shannon:execute-plan command
```
**Features**:
- Complexity-based batch sizing
- Review checkpoints between batches
- 3-tier validation per batch
- Quantitative progress tracking

---

### 2.6 finishing-a-development-branch
```yaml
name: finishing-a-development-branch
type: PROTOCOL
purpose: Branch readiness scoring
trigger: Before merge/PR
```
**Readiness Score** (0.00-1.00):
- Test Validation: 40%
- Code Quality: 30%
- Integration Readiness: 30%

---

### 2.7 honest-reflections
```yaml
name: honest-reflections
type: PROTOCOL
purpose: Gap analysis with 100+ thoughts
trigger: /shannon:reflect command
```
**Process**:
1. Read original plan/requirements
2. Compare plan vs actual delivery
3. Run 100+ sequential thoughts
4. Calculate honest completion %
5. Identify gaps and assumptions

---

### 2.8 memory-coordination
```yaml
name: memory-coordination
type: PROTOCOL
purpose: Serena naming conventions
trigger: Serena MCP operations
```
**Naming Pattern**:
```
{project}_{context}_{identifier}_{timestamp}
```

---

### 2.9 phase-planning
```yaml
name: phase-planning
type: PROTOCOL
purpose: 5-phase plan generation
trigger: /shannon:spec result processing
```
**Phases**:
1. DISCOVERY (20% effort)
2. ARCHITECTURE (15% effort)
3. IMPLEMENTATION (45% effort)
4. TESTING (15% effort)
5. DEPLOYMENT (5% effort)

---

### 2.10 project-indexing
```yaml
name: project-indexing
type: PROTOCOL
purpose: Token reduction via indexing
trigger: Large codebase analysis
```
**Benefits**:
- 94% token reduction
- Fast agent onboarding
- Structured codebase summary

---

### 2.11 project-onboarding
```yaml
name: project-onboarding
type: PROTOCOL
purpose: Codebase analysis for existing projects
trigger: /shannon:init command
```
**Generates**:
- SHANNON_INDEX
- Architecture detection
- Validation gate configuration
- NO MOCKS audit
- Shannon Readiness Score (0-100)

---

### 2.12 root-cause-tracing
```yaml
name: root-cause-tracing
type: PROTOCOL
purpose: Backward bug tracing
trigger: Bug investigation
```
**Process**:
1. Trace backward through call stack
2. Identify root cause
3. Fix at source (not symptom)
4. Add defense-in-depth

---

### 2.13 sitrep-reporting
```yaml
name: sitrep-reporting
type: PROTOCOL
purpose: Military-style status reporting
trigger: Multi-agent coordination
```
**Status Codes**:
- 🟢 ON TRACK
- 🟡 AT RISK
- 🔴 BLOCKED

---

### 2.14 skill-discovery
```yaml
name: skill-discovery
type: PROTOCOL
purpose: SKILL.md catalog building
trigger: /shannon:discover_skills
```
**Process**:
1. Scan directories for SKILL.md files
2. Parse YAML frontmatter
3. Build skill catalog
4. Enable intelligent skill selection

---

### 2.15 systematic-debugging
```yaml
name: systematic-debugging
type: PROTOCOL
purpose: 4-phase debugging framework
trigger: Bug investigation
```
**Phases**:
1. Root Cause Investigation
2. Pattern Analysis
3. Hypothesis Testing
4. Implementation

---

### 2.16 task-automation
```yaml
name: task-automation
type: PROTOCOL
purpose: prime→spec→wave orchestration
trigger: /shannon:task command
```
**Workflow**:
1. /shannon:prime (session setup)
2. /shannon:spec (complexity analysis)
3. /shannon:wave (parallel execution)

---

### 2.17 testing-anti-patterns
```yaml
name: testing-anti-patterns
type: PROTOCOL
purpose: Anti-pattern detection
trigger: Test file analysis
```
**Detects**:
- Testing mock behavior
- Test-only methods in production
- Skipped tests
- Flaky test patterns

---

### 2.18 testing-skills-with-subagents
```yaml
name: testing-skills-with-subagents
type: PROTOCOL
purpose: TDD for documentation
trigger: Skill creation/editing
```
**TDD Cycle**:
- RED: Run baseline WITHOUT skill
- GREEN: Write skill, verify compliance
- REFACTOR: Close loopholes

---

### 2.19 verification-before-completion
```yaml
name: verification-before-completion
type: PROTOCOL
purpose: Evidence before claims
trigger: Completion claims
```
**Gate Function**:
1. IDENTIFY: What command proves this claim?
2. RUN: Execute full command
3. READ: Check output and exit code
4. VERIFY: Does output confirm claim?
5. THEN: Make claim with evidence

---

### 2.20 writing-plans
```yaml
name: writing-plans
type: PROTOCOL
purpose: Quantitative implementation plans
trigger: /shannon:write-plan command
```
**Plan Structure**:
- Shannon Quantitative Analysis
- 8D Domain Distribution
- Validation Strategy (3-tier)
- MCP Requirements
- Task breakdown (2-5 min each)

---

### 2.21 writing-skills
```yaml
name: writing-skills
type: PROTOCOL
purpose: TDD for skill creation
trigger: New skill development
```
**Process**:
1. Create pressure scenarios
2. Run WITHOUT skill (baseline)
3. Write skill addressing violations
4. Run WITH skill (verify compliance)
5. Close loopholes iteratively

---

## 3. QUANTITATIVE Skills (8)

These skills produce measurable metrics.

### 3.1 confidence-check
```yaml
name: confidence-check
type: QUANTITATIVE
purpose: 90% confidence gate
trigger: Before implementation
```
**5-Check Algorithm**:
1. Requirements clarity
2. Technical understanding
3. Resource availability
4. Risk assessment
5. Dependency resolution

**Threshold**: ≥90% confidence required

---

### 3.2 goal-alignment
```yaml
name: goal-alignment
type: QUANTITATIVE
purpose: Validate against North Star
trigger: Wave deliverable review
```
**Alignment Score** (0-100%):
- Measures deliverable alignment with North Star goal
- Alerts on unaligned work
- Detects scope drift

---

### 3.3 goal-management
```yaml
name: goal-management
type: QUANTITATIVE
purpose: North Star tracking
trigger: /shannon:north_star command
```
**Features**:
- Parse vague goals into measurable criteria
- Persist to Serena MCP
- Track progress over time

---

### 3.4 intelligent-do
```yaml
name: intelligent-do
type: QUANTITATIVE
purpose: Context-aware execution
trigger: /shannon:do command
```
**Auto-Detection**:
- New vs existing project
- Spec analysis needed
- Context available in Serena
- MCP requirements

---

### 3.5 mcp-discovery
```yaml
name: mcp-discovery
type: QUANTITATIVE
purpose: MCP recommendation engine
trigger: Project analysis
```
**Tier-Based Priority**:
- Tier 1: Mandatory (Serena, Sequential)
- Tier 2: Recommended (Context7, Tavily, Puppeteer)
- Tier 3: Optional (Playwright, iOS Simulator)

---

### 3.6 spec-analysis
```yaml
name: spec-analysis
type: QUANTITATIVE
purpose: 8D complexity scoring
trigger: /shannon:spec command
```
**8 Dimensions**:
1. Structural (20%)
2. Cognitive (15%)
3. Coordination (15%)
4. Temporal (10%)
5. Technical (15%)
6. Scale (10%)
7. Uncertainty (10%)
8. Dependencies (5%)

**Output**: 0.00-1.00 complexity score

---

### 3.7 subagent-driven-development
```yaml
name: subagent-driven-development
type: QUANTITATIVE
purpose: Quality-gated task execution
trigger: Plan execution
```
**Features**:
- Fresh subagent per task
- Quality scoring
- Code review gates
- Pattern learning via Serena

---

### 3.8 wave-orchestration
```yaml
name: wave-orchestration
type: QUANTITATIVE
purpose: 3.5x parallel speedup
trigger: Complexity ≥0.50
```
**Features**:
- Dependency analysis
- Wave structure generation
- Agent allocation algorithm
- Synthesis checkpoints
- Speedup calculation

**Proven**: 3.5x speedup for complex projects

---

## 4. FLEXIBLE Skills (5)

These skills adapt to context.

### 4.1 brainstorming
```yaml
name: brainstorming
type: FLEXIBLE
purpose: Design refinement
trigger: Rough idea exploration
```
**Process**:
1. Explore possibilities
2. Quantitative validation (8D)
3. Document systematically
4. Persist to Serena

---

### 4.2 dispatching-parallel-agents
```yaml
name: dispatching-parallel-agents
type: FLEXIBLE
purpose: Multi-agent debugging
trigger: 3+ independent failures
```
**Features**:
- Parallel investigation
- Wave coordination
- Success score calculation

---

### 4.3 shannon-analysis
```yaml
name: shannon-analysis
type: FLEXIBLE
purpose: Analysis orchestration
trigger: /shannon:analyze command
```
**Analysis Types**:
- Codebase analysis
- Architecture analysis
- Technical debt analysis
- Complexity analysis

---

### 4.4 condition-based-waiting
```yaml
name: condition-based-waiting
type: FLEXIBLE
purpose: Flaky test prevention
trigger: Test with timing issues
```
**Pattern**:
```javascript
// ❌ Bad: Arbitrary sleep
await sleep(5000);

// ✅ Good: Condition polling
await waitFor(() => element.isVisible());
```

---

## 5. Specialized Skills (4)

### 5.1 mutation-testing
```yaml
name: mutation-testing
type: ANALYTICAL
purpose: Test quality via mutations
trigger: Test quality validation
```
**Mutation Score** (0.00-1.00):
- Inject code mutations
- Measure tests that catch mutations
- Auto-generate missing tests

---

### 5.2 performance-regression-detection
```yaml
name: performance-regression-detection
type: MONITORING
purpose: Benchmark tracking
trigger: Performance testing
```
**Features**:
- Track benchmarks over time
- Detect regressions >10%
- Analyze historical trends
- Calculate regression score

---

### 5.3 security-pattern-detection
```yaml
name: security-pattern-detection
type: SECURITY
purpose: OWASP scanning
trigger: Security analysis
```
**Detects**:
- SQL Injection
- XSS
- CSRF
- Insecure dependencies
- Hardcoded secrets

**Security Score** (0.00-1.00)

---

### 5.4 architecture-evolution-tracking
```yaml
name: architecture-evolution-tracking
type: STRUCTURAL
purpose: ADR compliance
trigger: Architecture changes
```
**Features**:
- Track Architecture Decision Records
- Detect drift from ADRs
- Calculate alignment score
- Provide refactoring guidance

---

## Quick Reference Table

| # | Skill | Type | Purpose |
|---|-------|------|---------|
| 1 | using-shannon | RIGID | Session workflows |
| 2 | functional-testing | RIGID | NO MOCKS |
| 3 | forced-reading-auto-activation | RIGID | Large content |
| 4 | test-driven-development | RIGID | TDD + NO MOCKS |
| 5 | forced-reading-protocol | RIGID | Line-by-line reading |
| 6 | context-preservation | PROTOCOL | Checkpoints |
| 7 | context-restoration | PROTOCOL | Restore state |
| 8 | defense-in-depth | PROTOCOL | Multi-layer validation |
| 9 | exec | PROTOCOL | 6-phase execution |
| 10 | executing-plans | PROTOCOL | Batch execution |
| 11 | finishing-a-development-branch | PROTOCOL | Branch readiness |
| 12 | honest-reflections | PROTOCOL | Gap analysis |
| 13 | memory-coordination | PROTOCOL | Serena naming |
| 14 | phase-planning | PROTOCOL | 5-phase plans |
| 15 | project-indexing | PROTOCOL | Token reduction |
| 16 | project-onboarding | PROTOCOL | Existing projects |
| 17 | root-cause-tracing | PROTOCOL | Bug tracing |
| 18 | sitrep-reporting | PROTOCOL | Status reporting |
| 19 | skill-discovery | PROTOCOL | Catalog building |
| 20 | systematic-debugging | PROTOCOL | 4-phase debugging |
| 21 | task-automation | PROTOCOL | prime→spec→wave |
| 22 | testing-anti-patterns | PROTOCOL | Anti-pattern detection |
| 23 | testing-skills-with-subagents | PROTOCOL | TDD for docs |
| 24 | verification-before-completion | PROTOCOL | Evidence before claims |
| 25 | writing-plans | PROTOCOL | Implementation plans |
| 26 | writing-skills | PROTOCOL | Skill creation |
| 27 | confidence-check | QUANTITATIVE | 90% confidence |
| 28 | goal-alignment | QUANTITATIVE | North Star validation |
| 29 | goal-management | QUANTITATIVE | Goal tracking |
| 30 | intelligent-do | QUANTITATIVE | Context-aware execution |
| 31 | mcp-discovery | QUANTITATIVE | MCP recommendations |
| 32 | spec-analysis | QUANTITATIVE | 8D scoring |
| 33 | subagent-driven-development | QUANTITATIVE | Quality-gated tasks |
| 34 | wave-orchestration | QUANTITATIVE | Parallel execution |
| 35 | brainstorming | FLEXIBLE | Design refinement |
| 36 | dispatching-parallel-agents | FLEXIBLE | Multi-agent debugging |
| 37 | shannon-analysis | FLEXIBLE | Analysis orchestration |
| 38 | condition-based-waiting | FLEXIBLE | Flaky test prevention |
| 39 | mutation-testing | ANALYTICAL | Test quality |
| 40 | performance-regression-detection | MONITORING | Benchmark tracking |
| 41 | security-pattern-detection | SECURITY | OWASP scanning |
| 42 | architecture-evolution-tracking | STRUCTURAL | ADR compliance |

---

**Catalog Complete**: November 29, 2025
