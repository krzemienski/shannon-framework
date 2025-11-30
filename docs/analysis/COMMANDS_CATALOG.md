# Shannon Framework v5.6 - Complete Commands Catalog

**Version**: 5.6.0  
**Total Commands**: 23  
**Last Updated**: November 29, 2025  

---

## Overview

Shannon Framework provides 23 user-facing commands, all prefixed with `shannon:` to prevent collision with other plugins or Claude Code built-in commands.

---

## Command Categories

| Category | Commands | Purpose |
|----------|----------|---------|
| Execution | 5 | Task and plan execution |
| Analysis | 3 | Specification and project analysis |
| Session | 4 | Session management |
| Goals | 2 | Goal tracking |
| Skills | 1 | Skill discovery |
| MCPs | 1 | MCP validation |
| Planning | 3 | Project planning |
| Testing | 1 | Functional testing |
| Memory | 1 | Serena operations |
| Health | 1 | Framework health |
| Setup | 1 | Project setup |

---

## 1. Execution Commands

### 1.1 /shannon:do

```yaml
command: /shannon:do
category: Execution
purpose: Intelligent task execution
skill: intelligent-do
```

**Usage**:
```
/shannon:do "implement user authentication"
```

**Features**:
- Auto-detects new vs existing project
- Checks for existing spec analysis
- Loads context from Serena
- Recommends appropriate MCPs

---

### 1.2 /shannon:exec

```yaml
command: /shannon:exec
category: Execution
purpose: Autonomous 6-phase execution
skill: exec
```

**Usage**:
```
/shannon:exec "build REST API for users"
```

**Phases**:
1. Library Discovery (Context7)
2. Implementation
3. Static Analysis (Tier 1)
4. Unit/Integration Tests (Tier 2)
5. Functional Tests (Tier 3 - NO MOCKS)
6. Git Commit

---

### 1.3 /shannon:task

```yaml
command: /shannon:task
category: Execution
purpose: Full workflow automation
skill: task-automation
```

**Usage**:
```
/shannon:task "build e-commerce platform"
```

**Workflow**:
```
prime → spec → wave (if complex)
```

---

### 1.4 /shannon:wave

```yaml
command: /shannon:wave
category: Execution
purpose: Wave-based parallel execution
skill: wave-orchestration
```

**Usage**:
```
/shannon:wave start
/shannon:wave status
/shannon:wave synthesize
```

**Features**:
- Parallel sub-agent execution
- 3.5x speedup for complex projects
- SITREP coordination
- Automatic synthesis

---

### 1.5 /shannon:execute-plan

```yaml
command: /shannon:execute-plan
category: Execution
purpose: Batch plan execution
skill: executing-plans
```

**Usage**:
```
/shannon:execute-plan
/shannon:execute-plan --batch-size 5
```

**Features**:
- Complexity-based batch sizing
- Review checkpoints
- 3-tier validation per batch

---

## 2. Analysis Commands

### 2.1 /shannon:spec

```yaml
command: /shannon:spec
category: Analysis
purpose: 8D complexity analysis
skill: spec-analysis
```

**Usage**:
```
/shannon:spec "specification text here"
/shannon:spec @SPEC.md
```

**Output**:
```
📊 Shannon Analysis Complete

Complexity Score: 0.65 (Complex)

8D Breakdown:
- Structural: 0.7 (20%)
- Cognitive: 0.6 (15%)
- Coordination: 0.7 (15%)
- Temporal: 0.5 (10%)
- Technical: 0.8 (15%)
- Scale: 0.6 (10%)
- Uncertainty: 0.5 (10%)
- Dependencies: 0.4 (5%)

Recommended Agents: 5
Execution Mode: Wave-based
```

---

### 2.2 /shannon:analyze

```yaml
command: /shannon:analyze
category: Analysis
purpose: Project analysis
skill: shannon-analysis
```

**Usage**:
```
/shannon:analyze
/shannon:analyze --type architecture
/shannon:analyze --type debt
```

**Analysis Types**:
- Codebase analysis
- Architecture analysis
- Technical debt analysis
- Complexity analysis

---

### 2.3 /shannon:ultrathink

```yaml
command: /shannon:ultrathink
category: Analysis
purpose: Deep debugging with 150+ thoughts
skill: systematic-debugging
mcp: Sequential MCP (mandatory)
```

**Usage**:
```
/shannon:ultrathink "why does authentication fail intermittently?"
```

**Features**:
- 150+ sequential thoughts
- Root cause analysis
- Hypothesis testing
- No premature conclusions

---

## 3. Session Commands

### 3.1 /shannon:prime

```yaml
command: /shannon:prime
category: Session
purpose: Session initialization
skill: using-shannon, skill-discovery
```

**Usage**:
```
/shannon:prime
```

**Actions**:
1. Load Shannon Framework
2. Discover available skills
3. Check MCP availability
4. Initialize Serena context
5. Display status

---

### 3.2 /shannon:status

```yaml
command: /shannon:status
category: Session
purpose: Framework health check
```

**Usage**:
```
/shannon:status
```

**Output**:
```
🔧 Shannon Framework v5.6.0 Status

Skills: 42 loaded
Commands: 23 available
Agents: 24 ready
Hooks: 9 active

MCP Status:
✅ Serena: Connected
✅ Sequential: Connected
⚠️  Context7: Not configured
⚠️  Puppeteer: Not configured
```

---

### 3.3 /shannon:checkpoint

```yaml
command: /shannon:checkpoint
category: Session
purpose: Manual checkpoint creation
skill: context-preservation
```

**Usage**:
```
/shannon:checkpoint
/shannon:checkpoint "before major refactor"
```

**Saves to Serena**:
- Session state
- Wave progress
- Active todos
- Decisions made
- Integration status

---

### 3.4 /shannon:restore

```yaml
command: /shannon:restore
category: Session
purpose: Context restoration
skill: context-restoration
```

**Usage**:
```
/shannon:restore
/shannon:restore --checkpoint "checkpoint_20241129_1200"
```

**Restores**:
- Previous session state
- Wave progress
- Active todos
- Decisions
- Context

---

## 4. Goal Commands

### 4.1 /shannon:north_star

```yaml
command: /shannon:north_star
category: Goals
purpose: Goal management
skill: goal-management
```

**Usage**:
```
/shannon:north_star "Build production-ready e-commerce platform"
/shannon:north_star --show
/shannon:north_star --update "Add mobile support"
```

**Features**:
- Parse vague goals into measurable criteria
- Persist to Serena MCP
- Track progress over time
- Inject into all prompts

---

### 4.2 /shannon:reflect

```yaml
command: /shannon:reflect
category: Goals
purpose: Honest gap analysis
skill: honest-reflections
```

**Usage**:
```
/shannon:reflect
```

**Process**:
1. Read original plan/requirements
2. Compare plan vs actual delivery
3. Run 100+ sequential thoughts
4. Calculate honest completion %
5. Identify gaps and assumptions

**Output**:
```
📝 Honest Reflection

Original Plan: 15 features
Implemented: 12 features
Completion: 80%

Gaps:
- Feature X: Partially implemented (70%)
- Feature Y: Not started
- Feature Z: Different from spec

Assumptions Made:
- Assumed OAuth2 instead of SAML
- Assumed PostgreSQL instead of MySQL
```

---

## 5. Skills Command

### 5.1 /shannon:discover_skills

```yaml
command: /shannon:discover_skills
category: Skills
purpose: Skill discovery
skill: skill-discovery
```

**Usage**:
```
/shannon:discover_skills
/shannon:discover_skills --filter testing
```

**Output**:
```
🔍 Discovered 42 Skills

RIGID (5):
- using-shannon
- functional-testing
- forced-reading-auto-activation
- test-driven-development
- forced-reading-protocol

PROTOCOL (20):
- context-preservation
- context-restoration
...

QUANTITATIVE (8):
- confidence-check
- spec-analysis
...
```

---

## 6. MCPs Command

### 6.1 /shannon:check_mcps

```yaml
command: /shannon:check_mcps
category: MCPs
purpose: MCP validation
skill: mcp-discovery
```

**Usage**:
```
/shannon:check_mcps
```

**Output**:
```
🔌 MCP Status Check

MANDATORY:
✅ Serena: Connected
   - Memory operations: Working
   - Knowledge graph: Accessible
✅ Sequential: Connected
   - Deep reasoning: Available

RECOMMENDED:
⚠️  Context7: Not configured
   - Install: npx context7-mcp
✅ Tavily: Connected
⚠️  Puppeteer: Not configured
   - Required for NO MOCKS testing
```

---

## 7. Planning Commands

### 7.1 /shannon:write-plan

```yaml
command: /shannon:write-plan
category: Planning
purpose: Create implementation plan
skill: writing-plans
```

**Usage**:
```
/shannon:write-plan
```

**Output**:
- 5-phase plan
- 8D analysis
- Wave structure
- Task breakdown (2-5 min each)
- Validation strategy

---

### 7.2 /shannon:init

```yaml
command: /shannon:init
category: Planning
purpose: Project initialization
skill: project-onboarding
```

**Usage**:
```
/shannon:init
```

**Actions**:
1. Generate SHANNON_INDEX
2. Detect architecture
3. Configure validation gates
4. Run NO MOCKS audit
5. Calculate Shannon Readiness Score

---

### 7.3 /shannon:scaffold

```yaml
command: /shannon:scaffold
category: Planning
purpose: Project scaffolding
skill: phase-planning
```

**Usage**:
```
/shannon:scaffold --type react
/shannon:scaffold --type node-api
/shannon:scaffold --type fullstack
```

**Outputs**:
- Project structure
- Configuration files
- Initial tests (NO MOCKS)
- Documentation templates

---

## 8. Testing Command

### 8.1 /shannon:test

```yaml
command: /shannon:test
category: Testing
purpose: Functional testing
skill: functional-testing
```

**Usage**:
```
/shannon:test
/shannon:test --puppeteer
/shannon:test --coverage
```

**Features**:
- Runs functional tests only
- Blocks mock-based tests
- Reports coverage
- Validates NO MOCKS compliance

---

## 9. Memory Command

### 9.1 /shannon:memory

```yaml
command: /shannon:memory
category: Memory
purpose: Serena operations
skill: memory-coordination
```

**Usage**:
```
/shannon:memory list
/shannon:memory read spec_analysis
/shannon:memory write "key" "value"
/shannon:memory delete "key"
```

**Operations**:
- List all memories
- Read specific memory
- Write new memory
- Delete memory
- Search memories

---

## 10. Health Command

### 10.1 /shannon:health

```yaml
command: /shannon:health
category: Health
purpose: Health dashboard (v5.6 NEW)
```

**Usage**:
```
/shannon:health
/shannon:health --verbose
```

**Dashboard**:
```
🏥 Shannon Health Dashboard

Framework: v5.6.0 ✅
Skills: 42/42 loaded ✅
Commands: 23/23 available ✅
Agents: 24/24 ready ✅
Hooks: 9/9 active ✅

MCP Health:
- Serena: Healthy (latency: 45ms)
- Sequential: Healthy (latency: 120ms)
- Context7: Not configured

Recent Activity:
- Last checkpoint: 15 min ago
- Active wave: None
- North Star: Set
```

---

## 11. Setup Command

### 11.1 /shannon:generate_instructions

```yaml
command: /shannon:generate_instructions
category: Setup
purpose: Generate project instructions
skill: project-onboarding
```

**Usage**:
```
/shannon:generate_instructions
```

**Generates**:
- `.shannon/custom_instructions.md`
- Project conventions
- Build commands
- Testing configuration
- Coding standards

---

## Quick Reference Table

| # | Command | Category | Purpose |
|---|---------|----------|---------|
| 1 | /shannon:do | Execution | Intelligent task execution |
| 2 | /shannon:exec | Execution | 6-phase autonomous execution |
| 3 | /shannon:task | Execution | Full workflow automation |
| 4 | /shannon:wave | Execution | Wave-based parallel execution |
| 5 | /shannon:execute-plan | Execution | Batch plan execution |
| 6 | /shannon:spec | Analysis | 8D complexity analysis |
| 7 | /shannon:analyze | Analysis | Project analysis |
| 8 | /shannon:ultrathink | Analysis | Deep debugging (150+ thoughts) |
| 9 | /shannon:prime | Session | Session initialization |
| 10 | /shannon:status | Session | Framework health check |
| 11 | /shannon:checkpoint | Session | Manual checkpoint |
| 12 | /shannon:restore | Session | Context restoration |
| 13 | /shannon:north_star | Goals | Goal management |
| 14 | /shannon:reflect | Goals | Honest gap analysis |
| 15 | /shannon:discover_skills | Skills | Skill discovery |
| 16 | /shannon:check_mcps | MCPs | MCP validation |
| 17 | /shannon:write-plan | Planning | Implementation plan |
| 18 | /shannon:init | Planning | Project initialization |
| 19 | /shannon:scaffold | Planning | Project scaffolding |
| 20 | /shannon:test | Testing | Functional testing |
| 21 | /shannon:memory | Memory | Serena operations |
| 22 | /shannon:health | Health | Health dashboard |
| 23 | /shannon:generate_instructions | Setup | Project instructions |

---

**Commands Catalog Complete**: November 29, 2025
