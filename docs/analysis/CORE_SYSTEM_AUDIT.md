# Shannon Framework v5.6 - Core System Audit

**Version**: 5.6.0  
**Core Files**: 10  
**Last Updated**: November 29, 2025  

---

## Overview

The Shannon Framework Core System consists of 10 foundational documents that define the framework's behavioral patterns, methodologies, and philosophies.

---

## Core Files Inventory

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| CONTEXT_MANAGEMENT.md | Serena checkpoint strategy | ~200 | ✅ |
| FORCED_READING_PROTOCOL.md | Line-by-line reading enforcement | ~150 | ✅ |
| HOOK_SYSTEM.md | Claude Code lifecycle integration | ~300 | ✅ |
| MCP_DISCOVERY.md | MCP server recommendation | ~250 | ✅ |
| PHASE_PLANNING.md | 5-phase project methodology | ~200 | ✅ |
| PROJECT_CUSTOM_INSTRUCTIONS.md | Auto-generated conventions | ~150 | ✅ |
| PROJECT_MEMORY.md | Serena memory organization | ~200 | ✅ |
| SPEC_ANALYSIS.md | 8D complexity scoring | ~350 | ✅ |
| TESTING_PHILOSOPHY.md | NO MOCKS Iron Law | ~250 | ✅ |
| WAVE_ORCHESTRATION.md | Parallel sub-agent coordination | ~400 | ✅ |

---

## 1. CONTEXT_MANAGEMENT.md

### Purpose
Defines Shannon's strategy for preserving context across sessions using Serena MCP checkpoints.

### Key Concepts

#### Checkpoint Strategy
```markdown
When to Checkpoint:
- Before PreCompact (automatic via hook)
- Wave boundaries (automatic via WAVE_COORDINATOR)
- Manual via /shannon:checkpoint
- Before major refactoring
```

#### Checkpoint Data Structure
```json
{
  "checkpoint_type": "auto|manual|wave_boundary",
  "timestamp": "ISO8601",
  "session_id": "...",
  "serena_memory_keys": ["key1", "key2"],
  "active_wave_state": {
    "current_wave": 2,
    "wave_phase": "execution",
    "wave_progress": "60%",
    "active_sub_agents": ["FRONTEND", "BACKEND"]
  },
  "phase_state": {
    "current_phase": 3,
    "phase_name": "Implementation"
  },
  "project_context": {
    "north_star_goal": "...",
    "project_name": "...",
    "current_focus": "..."
  },
  "todo_state": {...},
  "decisions_made": [...],
  "next_steps": [...]
}
```

#### Memory Naming Convention
```
{project}_{context}_{identifier}_{timestamp}
Examples:
- myapp_spec_analysis_20241129
- myapp_wave_2_complete_20241129
- myapp_checkpoint_auto_20241129_1200
```

---

## 2. FORCED_READING_PROTOCOL.md

### Purpose
Mandates complete line-by-line reading of critical documents before any synthesis or action.

### Key Concepts

#### The Iron Law
```markdown
BEFORE synthesizing or acting on ANY document:
1. PRE-COUNT: Count total lines/characters
2. SEQUENTIAL READING: Read every line from 1 to N
3. VERIFY COMPLETENESS: Confirm lines_read == total_lines
4. THEN: Sequential synthesis using Sequential MCP
```

#### Activation Triggers
- Manual: `/shannon:forced_read`
- Automatic: Via user_prompt_submit.py hook
  - Large prompts (>3000 chars)
  - Large file references (>5000 lines)
  - Specification keywords detected

#### Prohibited During Reading
- Summary generation
- Inference or assumption
- Skipping sections
- Parallel processing

---

## 3. HOOK_SYSTEM.md

### Purpose
Documents Shannon's integration with Claude Code's lifecycle hooks for automatic enforcement.

### Key Concepts

#### Available Hooks
| Hook | Trigger | Shannon Use |
|------|---------|-------------|
| SessionStart | Session begins | Load using-shannon |
| UserPromptSubmit | User sends prompt | North Star + Forced Reading |
| PreCompact | Before compaction | Auto-checkpoint |
| PostToolUse | After tool use | NO MOCKS enforcement |
| Stop | Task completion | Wave validation |

#### Hook Configuration
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "type": "command",
        "command": "${PLUGIN_ROOT}/hooks/post_tool_use.py",
        "timeout": 3000
      }
    ]
  }
}
```

---

## 4. MCP_DISCOVERY.md

### Purpose
Defines Shannon's intelligent system for discovering and recommending MCP servers based on project needs.

### Key Concepts

#### MCP Tiers
```markdown
TIER 1 - MANDATORY:
- Serena: Knowledge graph, context preservation
- Sequential: Deep reasoning (ultrathink)

TIER 2 - RECOMMENDED:
- Context7: Framework documentation
- Tavily: Research and best practices
- Puppeteer: Browser testing (NO MOCKS)

TIER 3 - OPTIONAL:
- Playwright: Cross-browser E2E
- iOS Simulator: Mobile testing
- Morphllm: Bulk code transformations
```

#### Capability Matrix
| Project Need | Recommended MCP |
|--------------|-----------------|
| Context persistence | Serena |
| Deep debugging | Sequential |
| Library docs | Context7 |
| Web research | Tavily |
| Browser tests | Puppeteer |
| React/Next.js UI | Shadcn UI |
| Mobile testing | iOS Simulator |

---

## 5. PHASE_PLANNING.md

### Purpose
Defines Shannon's standard 5-phase project methodology.

### Key Concepts

#### 5 Phases
```markdown
1. DISCOVERY (20% effort)
   - Stakeholder alignment
   - Requirements gathering
   - Technical assessment
   - Risk identification

2. ARCHITECTURE (15% effort)
   - System design
   - Technology selection
   - Integration planning
   - Security architecture

3. IMPLEMENTATION (45% effort)
   - Feature development
   - Code reviews
   - Integration
   - Documentation

4. TESTING (15% effort)
   - Functional testing (NO MOCKS)
   - Performance testing
   - Security testing
   - User acceptance

5. DEPLOYMENT (5% effort)
   - Production setup
   - Monitoring configuration
   - Rollback procedures
   - Launch verification
```

#### Validation Gates
Each phase has validation gates that must pass before proceeding:
- Discovery: Requirements signed off
- Architecture: Design reviewed
- Implementation: Code reviewed, tests pass
- Testing: All functional tests pass
- Deployment: Smoke tests pass

---

## 6. PROJECT_CUSTOM_INSTRUCTIONS.md

### Purpose
Describes the auto-generation of project-specific conventions and guidelines.

### Key Concepts

#### Auto-Generated Content
```markdown
.shannon/custom_instructions.md contains:
- Project conventions (naming, structure)
- Build commands (npm/pip/cargo)
- Testing configuration
- Coding standards
- Linting rules
- Git workflow
```

#### Detection Sources
- package.json → Node.js conventions
- requirements.txt → Python conventions
- Cargo.toml → Rust conventions
- go.mod → Go conventions
- .editorconfig → Editor settings
- .eslintrc → Linting rules

---

## 7. PROJECT_MEMORY.md

### Purpose
Defines how project context is persistently managed using Serena MCP.

### Key Concepts

#### Memory Categories
```markdown
1. Specification Analysis
   - spec_analysis: 8D complexity results
   - domain_breakdown: Component analysis
   
2. Planning
   - phase_plan_overview: 5-phase structure
   - phase_plan_detailed: Task breakdown
   
3. Execution
   - wave_N_complete: Wave results
   - wave_N_synthesis: Synthesized output
   
4. Context
   - project_context: North Star, focus
   - checkpoint_*: Session checkpoints
```

#### Memory Lifecycle
```
Write → Read → Update → Archive
```

---

## 8. SPEC_ANALYSIS.md

### Purpose
Defines Shannon's 8-Dimensional Complexity Framework for objective project assessment.

### Key Concepts

#### 8 Dimensions
```markdown
1. STRUCTURAL (20% weight)
   - Component count
   - Integration points
   - Hierarchy depth

2. COGNITIVE (15% weight)
   - Business rule complexity
   - Decision tree depth
   - Domain expertise required

3. COORDINATION (15% weight)
   - Team/agent count
   - Communication channels
   - Synchronization points

4. TEMPORAL (10% weight)
   - Deadline pressure
   - Sequence dependencies
   - Real-time requirements

5. TECHNICAL (15% weight)
   - Technology novelty
   - Stack complexity
   - Performance requirements

6. SCALE (10% weight)
   - Data volume
   - User count
   - Geographic distribution

7. UNCERTAINTY (10% weight)
   - Requirement clarity
   - Technology maturity
   - External dependencies

8. DEPENDENCIES (5% weight)
   - External APIs
   - Third-party services
   - Library dependencies
```

#### Complexity Formula
```python
total_complexity = (
    0.20 × structural +
    0.15 × cognitive +
    0.15 × coordination +
    0.10 × temporal +
    0.15 × technical +
    0.10 × scale +
    0.10 × uncertainty +
    0.05 × dependencies
)
```

#### Complexity Bands
| Range | Classification | Agents | Execution |
|-------|----------------|--------|-----------|
| 0.00-0.30 | Simple | 1-2 | Sequential |
| 0.30-0.50 | Moderate | 2-3 | 1-2 waves |
| 0.50-0.70 | Complex | 3-7 | Waves mandatory |
| 0.70-0.85 | High | 8-15 | SITREP required |
| 0.85-1.00 | Critical | 15-25 | Full orchestration |

---

## 9. TESTING_PHILOSOPHY.md

### Purpose
Defines Shannon's NO MOCKS testing philosophy - the "Iron Law" of functional testing.

### Key Concepts

#### The Iron Law
```markdown
Shannon Mandate: NO MOCKS

Tests must validate REAL system behavior with:
✅ Real browsers (Puppeteer/Playwright)
✅ Real databases (Docker containers)
✅ Real APIs (staging environments)
✅ Real file systems
✅ Real network calls

❌ PROHIBITED:
- Mock objects
- Stubs and fakes
- Unit tests with mocked dependencies
- In-memory fake databases
- Simulated HTTP responses
```

#### Why NO MOCKS?
```markdown
1. Mocks test YOUR ASSUMPTIONS, not reality
2. Mock behavior diverges from real systems
3. Integration bugs only appear in production
4. False confidence from passing mock tests
5. Technical debt from maintaining mocks
```

#### Enforcement Layers
```markdown
Layer 1: TESTING_PHILOSOPHY.md (documentation)
Layer 2: functional-testing skill (guidance)
Layer 3: post_tool_use.py hook (real-time blocking)
Layer 4: TEST_GUARDIAN agent (review oversight)
```

#### Recommended Testing Tools
| Domain | Tool | Purpose |
|--------|------|---------|
| Web | Puppeteer MCP | Real browser testing |
| Web | Playwright MCP | Cross-browser E2E |
| Mobile | iOS Simulator MCP | Real device testing |
| API | Real HTTP | Actual endpoint calls |
| Database | Docker | Real database instances |

---

## 10. WAVE_ORCHESTRATION.md

### Purpose
Defines Shannon's behavioral framework for orchestrating parallel sub-agent execution.

### Key Concepts

#### What is a Wave?
```markdown
A wave is a group of independent tasks that can be executed in parallel by multiple sub-agents.
```

#### Wave Lifecycle
```
1. DEPENDENCY ANALYSIS
   - Build task dependency graph
   - Identify parallel groups
   
2. WAVE GENERATION
   - Group independent tasks
   - Assign to agents
   
3. PARALLEL EXECUTION
   - Spawn agents concurrently
   - Collect SITREP reports
   
4. SYNTHESIS
   - Aggregate results
   - Create checkpoint
   - Present to user
   
5. VALIDATION
   - User approves wave
   - Proceed to next wave
```

#### Agent Allocation Algorithm
```python
def calculate_agents(complexity: float) -> int:
    if complexity < 0.30:
        return 1
    elif complexity < 0.50:
        return min(3, int(complexity * 6))
    elif complexity < 0.70:
        return min(7, int(complexity * 10))
    elif complexity < 0.85:
        return min(15, int(complexity * 18))
    else:
        return min(25, int(complexity * 30))
```

#### SITREP Protocol
```markdown
Every agent reports:
🟢 ON TRACK - Proceeding as planned
🟡 AT RISK - Issues detected, mitigation in progress
🔴 BLOCKED - Cannot proceed, requires intervention

Format:
**SITREP - {AGENT_NAME}**
**Status**: {STATUS}
**Progress**: {X}% complete
**Blockers**: {None | Description}
**Next**: {Immediate next action}
```

#### Proven Speedup
```markdown
Sequential Execution: 10 hours
Wave Execution: 2.86 hours
Speedup: 3.5x
```

---

## Integration Map

```
┌─────────────────────────────────────────────────────────────┐
│                    SPEC_ANALYSIS.md                         │
│                   (8D Complexity)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   PHASE_PLANNING.md                         │
│                   (5-Phase Plan)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           │           ▼
┌─────────────────┐   │   ┌─────────────────┐
│ MCP_DISCOVERY   │   │   │  PROJECT_CUSTOM │
│ (Tool Selection)│   │   │  _INSTRUCTIONS  │
└─────────────────┘   │   └─────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 WAVE_ORCHESTRATION.md                       │
│                 (Parallel Execution)                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           │           ▼
┌─────────────────┐   │   ┌─────────────────┐
│ TESTING_        │   │   │ CONTEXT_        │
│ PHILOSOPHY.md   │   │   │ MANAGEMENT.md   │
│ (NO MOCKS)      │   │   │ (Checkpoints)   │
└─────────────────┘   │   └─────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   HOOK_SYSTEM.md                            │
│                 (Runtime Enforcement)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│               FORCED_READING_PROTOCOL.md                    │
│                 (Critical Documents)                        │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  PROJECT_MEMORY.md                          │
│                 (Persistent State)                          │
└─────────────────────────────────────────────────────────────┘
```

---

**Core System Audit Complete**: November 29, 2025
