# Shannon Framework V4 - Skill Reference

Complete reference for all 15 Shannon V4 skills.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Skills](#core-skills)
3. [Orchestration Skills](#orchestration-skills)
4. [Context Skills](#context-skills)
5. [Testing Skills](#testing-skills)
6. [Analysis Skills](#analysis-skills)
7. [Support Skills](#support-skills)
8. [Integration Skills](#integration-skills)

---

## Overview

Shannon V4 uses a skill-based architecture where each command delegates to specialized skills. Skills are composable, reusable units of behavior that encapsulate specific capabilities.

### Skill Categories

| Category | Skills | Purpose |
|----------|--------|---------|
| **Core** | spec-analysis, wave-orchestration, phase-planning | Foundation workflows |
| **Context** | context-preservation, context-restoration, memory-coordination | State management |
| **Testing** | functional-testing, confidence-check | Quality assurance |
| **Analysis** | shannon-analysis, project-indexing | Deep analysis |
| **Support** | goal-management, goal-alignment, mcp-discovery, sitrep-reporting | Supporting capabilities |
| **Integration** | using-shannon | User guidance |

### Skill Activation

Skills are activated by:
- **Commands**: `/sh_spec` → spec-analysis skill
- **Agents**: Agents automatically activate required skills
- **Dependencies**: Skills can require other skills

---

## Core Skills

### spec-analysis

**Purpose:** 8-dimensional quantitative complexity analysis with domain detection

**Activated By:**
- `/sh_spec` command
- SPEC_ANALYZER agent

**Capabilities:**
- 8D complexity scoring (0.0-1.0 per dimension)
- Domain detection with percentages
- Implementation recommendations
- Wave count estimation
- MCP requirement analysis

**Dimensions Analyzed:**
1. **Technical** - Language features, algorithms, patterns
2. **Temporal** - Time-dependent operations, scheduling
3. **Integration** - External APIs, third-party services
4. **Cognitive** - Domain knowledge, business logic
5. **Environmental** - Deployment, infrastructure, configuration
6. **Data** - Data structures, transformations, persistence
7. **Scale** - Performance, concurrency, load handling
8. **Unknown** - Novel requirements, unclear specifications

**Output:**
```
8D Complexity Analysis:
├─ Technical: 0.75
├─ Temporal: 0.45
├─ Integration: 0.80
├─ Cognitive: 0.60
├─ Environmental: 0.55
├─ Data: 0.70
├─ Scale: 0.65
└─ Unknown: 0.30

Overall: 0.62 (COMPLEX)

Domains: Backend (45%), Database (30%), Security (15%), API (10%)
```

**MCP Requirements:**
- **Required:** Serena (save analysis)
- **Recommended:** Sequential (deep thinking for complex specs)

**Sub-Skills:**
- mcp-discovery
- phase-planning

**Triggers Wave Orchestration:** When complexity ≥ 0.50

---

### wave-orchestration

**Purpose:** Multi-stage project execution with agent coordination

**Activated By:**
- `/sh_wave` command
- WAVE_COORDINATOR agent
- spec-analysis skill (if complex)

**Capabilities:**
- Phase-based execution planning
- Agent assignment and coordination
- Parallel task execution
- Progress tracking
- Automatic checkpointing
- Deliverable validation

**Wave Structure:**
```
Wave N:
├─ Phase 1: Foundation
│  ├─ Task 1 (Agent A)
│  ├─ Task 2 (Agent B)
│  └─ Task 3 (Agent A)
├─ Phase 2: Implementation
│  ├─ Task 4 (Agent C)
│  └─ Task 5 (Agent D) [parallel with Task 4]
└─ Phase 3: Integration
   ├─ Task 6 (Agent A)
   └─ Task 7 (All agents)
```

**MCP Requirements:**
- **Required:** Serena (save wave state)
- **Recommended:** Sequential (wave planning)

**Sub-Skills:**
- phase-planning
- context-preservation

**Agent Coordination:**
- Activates domain agents as needed
- Coordinates parallel execution
- Manages dependencies
- Handles handoffs

---

### phase-planning

**Purpose:** Decomposes work into 5-phase execution plans

**Activated By:**
- wave-orchestration skill
- PHASE_ARCHITECT agent

**Capabilities:**
- Break specifications into phases
- Estimate phase durations
- Identify dependencies
- Assign agents
- Define deliverables

**5-Phase Framework:**
1. **Foundation** - Setup, configuration, infrastructure
2. **Implementation** - Core feature development
3. **Integration** - Component assembly, API integration
4. **Validation** - Testing, verification, quality checks
5. **Documentation** - Docs, runbooks, handoff materials

**Output:**
```
Phase Plan:

Phase 1: Foundation (Days 1-2)
├─ Database schema design
├─ API structure definition
└─ Environment setup

Phase 2: Implementation (Days 2-4)
├─ Backend service development
├─ Frontend component creation
└─ Business logic implementation

[etc...]
```

**MCP Requirements:**
- **Required:** Serena (save phase plans)

---

## Context Skills

### context-preservation

**Purpose:** Creates comprehensive checkpoints of project state

**Activated By:**
- `/sh_checkpoint` command
- CONTEXT_GUARDIAN agent
- wave-orchestration skill (automatic)

**Capabilities:**
- Capture complete project state
- Save to Serena MCP
- Generate checkpoint metadata
- Version checkpoint data
- Enable restoration

**Saved Context:**
- Specification text
- Complexity analysis (8D scores)
- North star goal
- Wave progress
- Agent assignments
- Memory entries
- Project metadata

**Checkpoint Structure:**
```json
{
  "name": "checkpoint-name",
  "timestamp": "2025-01-15T14:30:00Z",
  "specification": "...",
  "complexity": {"overall": 0.62, "dimensions": {...}},
  "north_star": "...",
  "wave_state": {...},
  "agents": [...],
  "memory": {...}
}
```

**MCP Requirements:**
- **Required:** Serena (store checkpoints)

---

### context-restoration

**Purpose:** Restores complete project context from checkpoints

**Activated By:**
- `/sh_restore` command
- CONTEXT_GUARDIAN agent

**Capabilities:**
- Load checkpoint from Serena MCP
- Restore all project state
- Reactivate agents
- Verify integrity
- Resume workflows

**Restoration Process:**
1. Load checkpoint data
2. Validate integrity
3. Restore specification
4. Restore analysis
5. Restore goals
6. Restore wave state
7. Reactivate agents
8. Confirm ready

**MCP Requirements:**
- **Required:** Serena (load checkpoints)

**Zero Context Loss:** Guarantees 100% state restoration

---

### memory-coordination

**Purpose:** Coordinates with Serena MCP memory system

**Activated By:**
- `/sh_memory` command
- context-preservation skill
- context-restoration skill

**Capabilities:**
- Save structured memories
- Retrieve memories by name
- List all memories
- Delete memories
- Search memory content

**Memory Types:**
- **Architecture** - System design decisions
- **Standards** - Coding conventions
- **Deployment** - Ops procedures
- **Patterns** - Implementation patterns
- **Decisions** - Historical decisions

**MCP Requirements:**
- **Required:** Serena (memory storage)

---

## Testing Skills

### functional-testing

**Purpose:** Generates functional tests following NO MOCKS philosophy

**Activated By:**
- `/sh_test` command
- TEST_GUARDIAN agent

**Capabilities:**
- Generate web tests (Puppeteer MCP)
- Generate API tests (real HTTP)
- Generate mobile tests (real devices)
- Enforce NO MOCKS principles
- Create test documentation

**NO MOCKS Enforcement:**
- ✅ Real browsers (Puppeteer MCP)
- ✅ Real HTTP clients
- ✅ Real databases (test instances)
- ✅ Real third-party APIs (dev/staging)
- ❌ No jest.mock()
- ❌ No sinon stubs
- ❌ No test doubles

**Test Structure:**
```typescript
// Generated web test
describe('User Login', () => {
  it('should redirect to dashboard on valid login', async () => {
    // Uses Puppeteer MCP - real browser
    await page.navigate('https://app.test/login');
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('#login-button');

    // Real navigation, real DOM, real backend
    expect(await page.url()).toContain('/dashboard');
  });
});
```

**MCP Requirements:**
- **Required:** Puppeteer (web tests)
- **Fallback:** Manual test guidance

**Sub-Skills:**
- mcp-discovery (find testing MCPs)

---

### confidence-check

**Purpose:** Validates readiness and completion criteria

**Activated By:**
- wave-orchestration skill
- Domain agents

**Capabilities:**
- Verify wave completion
- Check deliverable quality
- Validate test coverage
- Assess documentation
- Confirm deployment readiness

**Confidence Levels:**
- **High (≥ 0.80)** - Ready to proceed
- **Medium (0.60-0.79)** - Minor concerns
- **Low (< 0.60)** - Significant issues

**Checks:**
```
Confidence Check: Wave 2

Deliverables:
├─ Payment API: ✅ Complete
├─ Integration tests: ✅ Passing
├─ Documentation: ⚠️  Incomplete
└─ Performance tests: ❌ Missing

Confidence: 0.65 (MEDIUM)

Recommendations:
- Complete API documentation
- Add performance tests
- Then proceed to Wave 3
```

**MCP Requirements:**
- **Required:** Serena (save checks)

---

## Analysis Skills

### shannon-analysis

**Purpose:** Meta-analysis of Shannon's own execution

**Activated By:**
- `/sh_analyze` command
- Quality review agents

**Capabilities:**
- Analyze Shannon's decisions
- Review complexity scoring
- Validate agent assignments
- Audit wave planning
- Identify improvement opportunities

**Analysis Dimensions:**
- Decision quality
- Agent utilization
- Wave efficiency
- Estimation accuracy
- Context preservation effectiveness

**Output:**
```
Shannon Execution Analysis

Project: E-commerce Platform
Duration: 18 days (estimated 21 days)

Complexity Accuracy: 94%
├─ Estimated: 0.68
└─ Actual: 0.71

Agent Efficiency: 87%
├─ BACKEND: 92% (high)
├─ DATABASE: 85% (good)
└─ SECURITY: 80% (acceptable)

Wave Planning Accuracy: 91%
├─ Wave 1: On time
├─ Wave 2: 1 day early
└─ Wave 3: On time

Recommendations:
- Increase security agent involvement earlier
- Add performance testing to Wave 2
```

**MCP Requirements:**
- **Required:** Serena (execution history)
- **Recommended:** Sequential (deep analysis)

---

### project-indexing

**Purpose:** Indexes project structure and dependencies

**Activated By:**
- `/sh_analyze --dependencies`
- `/sh_scaffold` command

**Capabilities:**
- Scan project structure
- Identify dependencies
- Map file relationships
- Detect frameworks
- Find configuration files

**Index Structure:**
```
Project Index:

Structure:
├─ src/ (27 files)
│  ├─ components/ (12 components)
│  ├─ pages/ (5 pages)
│  └─ utils/ (10 utilities)
├─ tests/ (15 test files)
└─ config/ (3 configs)

Dependencies:
├─ react@18.2.0
├─ express@4.18.0
├─ postgresql@3.3.0
└─ redis@4.6.0

Frameworks:
├─ Frontend: React + TypeScript
├─ Backend: Express
└─ Database: PostgreSQL
```

**MCP Requirements:**
- **Required:** Serena (save index)

**Tools Used:**
- Read, Glob, Grep (codebase scanning)

---

## Support Skills

### goal-management

**Purpose:** Manages project goals and alignment

**Activated By:**
- `/sh_north_star` command
- goal-alignment skill

**Capabilities:**
- Set north star goals
- Track goal progress
- Validate goal alignment
- Update goals
- Archive completed goals

**Goal Structure:**
```json
{
  "type": "north_star",
  "goal": "Launch MVP to 100 beta users by Q1",
  "metrics": ["user_count", "launch_date"],
  "created": "2025-01-01",
  "status": "active"
}
```

**MCP Requirements:**
- **Required:** Serena (save goals)

---

### goal-alignment

**Purpose:** Ensures decisions align with north star

**Activated By:**
- wave-orchestration skill
- phase-planning skill
- Domain agents

**Capabilities:**
- Validate decisions against goals
- Prioritize features by goal impact
- Flag misalignments
- Recommend corrections
- Track alignment metrics

**Alignment Check:**
```
Goal Alignment Check

North Star: Launch MVP by Q1

Wave 2 Decisions:
├─ Add payment processing: ✅ Aligned (critical for MVP)
├─ Add advanced analytics: ⚠️  Misaligned (post-MVP feature)
└─ Security hardening: ✅ Aligned (pre-launch requirement)

Recommendations:
- Defer analytics to Wave 4 (post-MVP)
- Keep security in Wave 2
- Focus on core MVP features
```

**MCP Requirements:**
- **Required:** Serena (load goals)

---

### mcp-discovery

**Purpose:** Discovers and recommends MCPs for current context

**Activated By:**
- `/sh_check_mcps` command
- All skills (automatic MCP detection)

**Capabilities:**
- Detect available MCPs
- Recommend missing MCPs
- Provide installation guidance
- Configure fallback behavior
- Test MCP connectivity

**Discovery Output:**
```
MCP Discovery Report

Required:
├─ Serena: ✅ Available

Recommended:
├─ Sequential: ✅ Available
│  └─ Use for: Complex spec analysis
├─ Puppeteer: ❌ Missing
│  └─ Install: npm install -g @anthropic/puppeteer-mcp
└─ Context7: ✅ Available
   └─ Use for: Framework patterns

Fallbacks Configured:
├─ Puppeteer → Manual testing guidance
└─ Sequential → Native thinking
```

**Fallback Chains:**
- Puppeteer → Manual testing
- Sequential → Native thinking
- Context7 → Built-in patterns

**MCP Requirements:**
- None (self-contained)

---

### sitrep-reporting

**Purpose:** Generates situation reports for SuperClaude coordination

**Activated By:**
- SuperClaude commands
- Wave completion
- Checkpoint creation

**Capabilities:**
- Generate SITREP documents
- Summarize project state
- Report wave progress
- List deliverables
- Flag blockers

**SITREP Format:**
```markdown
# SITREP: Project Status

## Current State
- Specification: Analyzed (complexity: 0.68)
- Wave: 2 of 4 (50% complete)
- Status: On track

## Completed
- Wave 1: Backend foundation ✅
- Wave 2: Frontend components ✅

## In Progress
- Wave 3: Integration (60% complete)

## Blockers
- None

## Next Actions
- Complete Wave 3 testing
- Begin Wave 4 planning
```

**MCP Requirements:**
- **Required:** Serena (project state)

---

### using-shannon

**Purpose:** Provides user guidance and onboarding

**Activated By:**
- First-time usage
- Help requests
- Error conditions

**Capabilities:**
- Show quick start guide
- Explain commands
- Suggest workflows
- Provide examples
- Troubleshoot issues

**Guidance Topics:**
- Getting started
- Command usage
- Workflow patterns
- MCP setup
- Best practices
- Common errors

**MCP Requirements:**
- None (self-contained)

---

## Skill Composition

Skills can compose with each other:

### Example: spec-analysis Composition

```
/sh_spec "Build app" triggers:
├─ spec-analysis (primary)
│  ├─ Uses: mcp-discovery
│  │  └─ Finds: Sequential MCP
│  ├─ Uses: phase-planning
│  │  └─ Generates: 5-phase plan
│  └─ Triggers: wave-orchestration (if complex)
│     ├─ Uses: phase-planning
│     ├─ Uses: context-preservation
│     └─ Uses: goal-alignment
```

### Example: Testing Composition

```
/sh_test triggers:
├─ functional-testing (primary)
│  ├─ Uses: mcp-discovery
│  │  └─ Finds: Puppeteer MCP
│  ├─ Uses: project-indexing
│  │  └─ Scans: Test structure
│  └─ Uses: confidence-check
│     └─ Validates: Test coverage
```

---

## Skill Development

Skills are located in `shannon-plugin/skills/<skill-name>/SKILL.md`

### Skill Structure

```markdown
---
name: skill-name
description: What this skill does
skill-type: QUANTITATIVE | QUALITATIVE | HYBRID
shannon-version: ">=4.0.0"
mcp-requirements:
  required: [...]
  recommended: [...]
required-sub-skills: [...]
optional-sub-skills: [...]
allowed-tools: [...]
---

# Skill Content
[Detailed skill behavior...]
```

### Adding New Skills

1. Create `skills/<name>/SKILL.md`
2. Define metadata in frontmatter
3. Write skill behavior
4. Add to plugin.json
5. Create tests
6. Update documentation

---

## Skill Reference Matrix

| Skill | Commands | Agents | MCP Required | MCP Recommended |
|-------|----------|--------|--------------|-----------------|
| spec-analysis | sh_spec | SPEC_ANALYZER | Serena | Sequential |
| wave-orchestration | sh_wave | WAVE_COORDINATOR | Serena | Sequential |
| phase-planning | sh_wave | PHASE_ARCHITECT | Serena | - |
| context-preservation | sh_checkpoint | CONTEXT_GUARDIAN | Serena | - |
| context-restoration | sh_restore | CONTEXT_GUARDIAN | Serena | - |
| memory-coordination | sh_memory | - | Serena | - |
| functional-testing | sh_test | TEST_GUARDIAN | - | Puppeteer |
| confidence-check | - | All agents | Serena | - |
| shannon-analysis | sh_analyze | - | Serena | Sequential |
| project-indexing | sh_analyze, sh_scaffold | - | Serena | - |
| goal-management | sh_north_star | - | Serena | - |
| goal-alignment | - | All agents | Serena | - |
| mcp-discovery | sh_check_mcps | All skills | - | - |
| sitrep-reporting | - | SuperClaude | Serena | - |
| using-shannon | - | - | - | - |

---

## Best Practices

### Skill Usage

1. **Let Skills Compose**: Don't manually invoke sub-skills
2. **Trust Fallbacks**: Skills handle missing MCPs gracefully
3. **Check Status**: Use `/sh_status` to see active skills
4. **Review Output**: Skills provide detailed output for transparency

### Skill Development

1. **Clear Purpose**: Each skill has single responsibility
2. **Define Dependencies**: Explicit MCP and sub-skill requirements
3. **Implement Fallbacks**: Graceful degradation without optional MCPs
4. **Document Behavior**: Comprehensive SKILL.md documentation
5. **Test Thoroughly**: Unit and integration tests

---

## Troubleshooting Skills

### Skill Not Activating

**Check:**
1. Command syntax correct?
2. Required MCPs available?
3. Agent properly configured?

**Solution:**
```bash
/sh_check_mcps  # Verify MCPs
/sh_status      # Check project state
```

### Skill Errors

**Common Causes:**
- Missing MCP (check requirements)
- Invalid input
- State inconsistency

**Solution:**
```bash
/sh_restore "<last-checkpoint>"  # Restore good state
```

### Performance Issues

**Common Causes:**
- Complex specifications
- Large project scans
- MCP latency

**Solution:**
- Break specs into smaller chunks
- Use specific directory scans
- Check MCP connections

---

For implementation details, see:
- User Guide: `SHANNON_V4_USER_GUIDE.md`
- Command Reference: `SHANNON_V4_COMMAND_REFERENCE.md`
- Migration Guide: `SHANNON_V4_MIGRATION_GUIDE.md`

For skill source code:
- `shannon-plugin/skills/<skill-name>/SKILL.md`
