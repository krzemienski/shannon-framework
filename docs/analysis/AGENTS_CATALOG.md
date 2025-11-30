# Shannon Framework v5.6 - Complete Agents Catalog

**Version**: 5.6.0
**Total Agents**: 24
**Last Updated**: November 29, 2025

---

## Overview

Shannon Framework includes 24 specialized sub-agents that can be spawned for parallel wave execution. Each agent follows mandatory protocols and enforces the NO MOCKS testing philosophy.

---

## Mandatory Agent Protocols

### 1. Context Loading Protocol

Every agent MUST execute before starting any task:

```markdown
BEFORE starting ANY task:
1. list_memories() - Discover available context
2. read_memory("spec_analysis") - Project requirements
3. read_memory("phase_plan_detailed") - Execution structure
4. read_memory("wave_N_complete") - Previous wave results
5. read_memory("project_context") - North Star and focus
```

### 2. SITREP Reporting Protocol

Every agent MUST report status:

```markdown
Status Codes:
🟢 ON TRACK - Proceeding as planned
🟡 AT RISK - Issues detected, mitigation in progress
🔴 BLOCKED - Cannot proceed, requires intervention

Format:
**SITREP - {AGENT_NAME}**
**Status**: {🟢|🟡|🔴} {STATUS}
**Progress**: {X}% complete
**Blockers**: {None | Description}
**Next**: {Immediate next action}
```

### 3. NO MOCKS Compliance

Every agent MUST enforce functional testing:

```markdown
❌ PROHIBITED: Mock objects, stubs, fakes
✅ REQUIRED: Real systems via Puppeteer, real databases, real APIs
```

---

## Agent Roster

### 1. ANALYZER

```yaml
name: ANALYZER
specialization: Analysis orchestration
triggers: /shannon:analyze, complexity analysis
```

**Responsibilities**:
- Orchestrate codebase analysis
- Generate SHANNON_INDEX
- Calculate complexity metrics
- Coordinate with other analysis agents

**Outputs**:
- Complexity scores (8D)
- Architecture diagrams
- Dependency graphs
- Technical debt inventory

---

### 2. API_DESIGNER

```yaml
name: API_DESIGNER
specialization: API specification and design
triggers: API-related tasks
```

**Responsibilities**:
- Design RESTful/GraphQL APIs
- Generate OpenAPI specifications
- Plan authentication/authorization
- Define error handling patterns

**Outputs**:
- OpenAPI/Swagger specs
- API documentation
- Endpoint contracts
- Rate limiting plans

---

### 3. ARCHITECT

```yaml
name: ARCHITECT
specialization: System architecture design
triggers: Architecture decisions, system design
```

**Responsibilities**:
- Define system architecture
- Create architecture decision records (ADRs)
- Plan scalability strategies
- Design component interactions

**Outputs**:
- Architecture diagrams
- ADRs
- Component specifications
- Integration patterns

---

### 4. BACKEND

```yaml
name: BACKEND
specialization: Server-side implementation
triggers: Backend tasks, API implementation
```

**Responsibilities**:
- Implement server-side logic
- Build API endpoints
- Integrate databases
- Implement business logic

**Testing Mandate**:
- Real database tests (Docker)
- Real API endpoint tests
- NO mock HTTP clients

---

### 5. CODE_REVIEWER

```yaml
name: CODE_REVIEWER
specialization: Code quality analysis
triggers: PR review, code quality checks
```

**Responsibilities**:
- Review code for quality
- Check for security issues
- Verify coding standards
- Suggest improvements

**Review Criteria**:
- NO MOCKS violations
- Security patterns
- Performance issues
- Code maintainability

---

### 6. CONTEXT_GUARDIAN

```yaml
name: CONTEXT_GUARDIAN
specialization: Context preservation and restoration
triggers: PreCompact, checkpoints, session management
```

**Responsibilities**:
- Create Serena checkpoints
- Restore session context
- Manage memory organization
- Prevent context loss

**Critical Role**:
- Executes during PreCompact hook
- Creates comprehensive checkpoints
- Ensures zero-context-loss

---

### 7. DATA_ENGINEER

```yaml
name: DATA_ENGINEER
specialization: Data pipelines and ETL
triggers: Data processing tasks
```

**Responsibilities**:
- Design data pipelines
- Implement ETL processes
- Optimize data flows
- Handle data transformations

**Testing Mandate**:
- Real data processing tests
- Actual file/stream handling
- NO mock data sources

---

### 8. DATABASE_ARCHITECT

```yaml
name: DATABASE_ARCHITECT
specialization: Database design and optimization
triggers: Schema design, database tasks
```

**Responsibilities**:
- Design database schemas
- Create migrations
- Optimize queries
- Plan indexing strategies

**Testing Mandate**:
- Real database instances
- Actual migration tests
- NO in-memory fakes

---

### 9. DEVOPS

```yaml
name: DEVOPS
specialization: Infrastructure and deployment
triggers: CI/CD, infrastructure tasks
```

**Responsibilities**:
- Configure CI/CD pipelines
- Set up infrastructure
- Manage deployments
- Handle containerization

**Testing Mandate**:
- Real container tests
- Actual deployment verification
- NO mock infrastructure

---

### 10. FRONTEND

```yaml
name: FRONTEND
specialization: UI implementation
triggers: Frontend tasks, UI development
```

**Responsibilities**:
- Implement UI components
- Handle state management
- Integrate with APIs
- Ensure accessibility

**Testing Mandate**:
- Puppeteer browser tests
- Real DOM interactions
- NO Jest DOM mocks

---

### 11. IMPLEMENTATION_WORKER

```yaml
name: IMPLEMENTATION_WORKER
specialization: General task execution
triggers: Wave task execution
```

**Responsibilities**:
- Execute assigned tasks
- Follow implementation plans
- Report progress via SITREP
- Coordinate with other workers

**Key Feature**:
- Generic worker for any task type
- Follows Shannon quantitative methodology

---

### 12. MENTOR

```yaml
name: MENTOR
specialization: Guidance and best practices
triggers: Questions, guidance requests
```

**Responsibilities**:
- Provide technical guidance
- Explain best practices
- Answer questions
- Suggest improvements

**Expertise Areas**:
- Shannon methodology
- Testing practices
- Architecture patterns
- Tool usage

---

### 13. MOBILE_DEVELOPER

```yaml
name: MOBILE_DEVELOPER
specialization: Mobile app development
triggers: Mobile tasks, React Native/Flutter
```

**Responsibilities**:
- Build mobile apps
- Handle platform-specific code
- Integrate native features
- Optimize mobile performance

**Testing Mandate**:
- Real device/simulator tests
- iOS Simulator MCP
- NO mock navigation/APIs

---

### 14. PERFORMANCE

```yaml
name: PERFORMANCE
specialization: Performance optimization
triggers: Performance tasks, optimization
```

**Responsibilities**:
- Profile applications
- Identify bottlenecks
- Optimize critical paths
- Benchmark improvements

**Tools**:
- Real profiling tools
- Actual benchmark suites
- NO mock performance data

---

### 15. PHASE_ARCHITECT

```yaml
name: PHASE_ARCHITECT
specialization: Phase planning and structure
triggers: /shannon:write-plan, phase planning
```

**Responsibilities**:
- Generate 5-phase plans
- Estimate effort distribution
- Define validation gates
- Plan wave structure

**Outputs**:
- Phase plans with effort %
- Wave dependency graphs
- Validation strategies
- MCP requirements

---

### 16. PRODUCT_MANAGER

```yaml
name: PRODUCT_MANAGER
specialization: Requirements and priorities
triggers: Product decisions, requirements
```

**Responsibilities**:
- Clarify requirements
- Prioritize features
- Define acceptance criteria
- Manage scope

**Outputs**:
- User stories
- Acceptance criteria
- Priority rankings
- Scope decisions

---

### 17. QA

```yaml
name: QA
specialization: Quality assurance
triggers: Testing tasks, quality checks
```

**Responsibilities**:
- Design test strategies
- Execute test plans
- Report quality metrics
- Verify fixes

**Testing Mandate**:
- Functional tests ONLY
- NO mock-based tests
- Real system verification

---

### 18. REFACTORER

```yaml
name: REFACTORER
specialization: Code improvement
triggers: Refactoring tasks
```

**Responsibilities**:
- Improve code structure
- Reduce technical debt
- Apply design patterns
- Maintain behavior

**Testing Mandate**:
- Verify behavior preserved
- Real regression tests
- NO mock assertions

---

### 19. SCRIBE

```yaml
name: SCRIBE
specialization: Documentation generation
triggers: Documentation tasks
```

**Responsibilities**:
- Write documentation
- Generate README files
- Create API docs
- Document decisions

**Outputs**:
- README.md files
- API documentation
- Architecture docs
- Change logs

---

### 20. SECURITY

```yaml
name: SECURITY
specialization: Security analysis
triggers: Security tasks, vulnerability scanning
```

**Responsibilities**:
- Scan for vulnerabilities
- Review authentication
- Check authorization
- Audit data handling

**Testing Mandate**:
- Real security scans
- Actual penetration testing
- NO mock security responses

---

### 21. SPEC_ANALYZER

```yaml
name: SPEC_ANALYZER
specialization: Specification analysis
triggers: /shannon:spec, spec analysis
```

**Responsibilities**:
- Parse specifications
- Calculate 8D complexity
- Identify ambiguities
- Recommend clarifications

**Outputs**:
- 8D complexity scores
- Domain distribution
- Ambiguity list
- Clarification questions

---

### 22. TECHNICAL_WRITER

```yaml
name: TECHNICAL_WRITER
specialization: Technical documentation
triggers: Technical docs, guides
```

**Responsibilities**:
- Write technical guides
- Create tutorials
- Document APIs
- Explain complex systems

**Outputs**:
- Technical guides
- How-to tutorials
- Reference documentation
- System explanations

---

### 23. TEST_GUARDIAN

```yaml
name: TEST_GUARDIAN
specialization: Testing oversight
triggers: Test creation, NO MOCKS enforcement
```

**Responsibilities**:
- Enforce NO MOCKS philosophy
- Review test implementations
- Guide functional testing
- Reject mock-based tests

**Critical Role**:
- Final authority on test quality
- Blocks mock usage
- Guides Puppeteer/real system usage

---

### 24. WAVE_COORDINATOR

```yaml
name: WAVE_COORDINATOR
specialization: Wave orchestration
triggers: Multi-agent coordination
```

**Responsibilities**:
- Coordinate wave execution
- Manage agent allocation
- Collect SITREP reports
- Synthesize wave results

**Outputs**:
- Wave status dashboard
- Agent coordination instructions
- Synthesis reports
- Checkpoint triggers

---

## Agent Allocation by Complexity

### Simple Projects (0.00-0.30)

```yaml
agents:
  - SPEC_ANALYZER
  - IMPLEMENTATION_WORKER
total: 1-2 agents
execution: Sequential
```

### Moderate Projects (0.30-0.50)

```yaml
agents:
  - SPEC_ANALYZER
  - ARCHITECT
  - IMPLEMENTATION_WORKER
  - QA
total: 2-4 agents
execution: 1-2 waves
```

### Complex Projects (0.50-0.70)

```yaml
agents:
  - SPEC_ANALYZER
  - ARCHITECT
  - FRONTEND
  - BACKEND
  - DATABASE_ARCHITECT
  - QA
  - TEST_GUARDIAN
total: 3-7 agents
execution: Multiple waves, SITREP required
```

### High Complexity (0.70-0.85)

```yaml
agents:
  - WAVE_COORDINATOR
  - SPEC_ANALYZER
  - ARCHITECT
  - API_DESIGNER
  - FRONTEND
  - BACKEND
  - DATABASE_ARCHITECT
  - DEVOPS
  - SECURITY
  - QA
  - TEST_GUARDIAN
  - SCRIBE
total: 8-15 agents
execution: Structured waves, mandatory SITREP
```

### Critical Complexity (0.85-1.00)

```yaml
agents:
  All 24 agents potentially active
total: 15-25 agents
execution: Full wave orchestration, continuous SITREP
```

---

## Quick Reference Table

| # | Agent | Specialization | Key Output |
|---|-------|----------------|------------|
| 1 | ANALYZER | Analysis orchestration | SHANNON_INDEX |
| 2 | API_DESIGNER | API design | OpenAPI specs |
| 3 | ARCHITECT | System design | ADRs, diagrams |
| 4 | BACKEND | Server-side code | APIs, business logic |
| 5 | CODE_REVIEWER | Code quality | Review feedback |
| 6 | CONTEXT_GUARDIAN | Context preservation | Checkpoints |
| 7 | DATA_ENGINEER | Data pipelines | ETL processes |
| 8 | DATABASE_ARCHITECT | Database design | Schemas, migrations |
| 9 | DEVOPS | Infrastructure | CI/CD, deployment |
| 10 | FRONTEND | UI implementation | Components |
| 11 | IMPLEMENTATION_WORKER | Task execution | Code changes |
| 12 | MENTOR | Guidance | Advice, answers |
| 13 | MOBILE_DEVELOPER | Mobile apps | Native code |
| 14 | PERFORMANCE | Optimization | Benchmarks |
| 15 | PHASE_ARCHITECT | Phase planning | 5-phase plans |
| 16 | PRODUCT_MANAGER | Requirements | User stories |
| 17 | QA | Quality assurance | Test results |
| 18 | REFACTORER | Code improvement | Refactored code |
| 19 | SCRIBE | Documentation | README, docs |
| 20 | SECURITY | Security analysis | Vulnerability reports |
| 21 | SPEC_ANALYZER | Spec analysis | 8D scores |
| 22 | TECHNICAL_WRITER | Technical docs | Guides, tutorials |
| 23 | TEST_GUARDIAN | Testing oversight | Test validation |
| 24 | WAVE_COORDINATOR | Wave orchestration | Coordination |

---

**Agents Catalog Complete**: November 29, 2025
