# Shannon Framework V5: Command Orchestration Guide

## Overview

This document provides definitive guidance on **when to use which Shannon command** and how commands orchestrate together. Shannon Framework has 22 commands organized into a clear hierarchy.

---

## Command Hierarchy

```
META-COMMANDS (orchestrate other commands)
├─ /shannon:prime      → Session initialization (skills + MCPs + context)
└─ /shannon:task       → Full workflow automation (prime→spec→wave)

PREPARATION (explore & plan)
├─ /shannon:brainstorm → Divergent option generation with 8D scoring
├─ /shannon:write_plan → Detailed implementation plan w/ files/tests
└─ /shannon:execute_plan → Guided plan execution w/ checkpoints

CORE EXECUTION (do the work)
├─ /shannon:do         → Intelligent execution (auto-detects context, research, spec)
├─ /shannon:exec       → Autonomous execution (library discovery + validation + git)
└─ /shannon:wave       → Wave-based parallel execution

ANALYSIS (understand the work)
├─ /shannon:spec       → 8D complexity analysis for specifications
└─ /shannon:analyze    → Shannon-aware project analysis

GOAL MANAGEMENT
├─ /shannon:north_star → Set and track North Star goals
└─ /shannon:reflect    → Honest gap analysis (post-execution validation)

CONTEXT MANAGEMENT
├─ /shannon:checkpoint → Manual checkpoint creation
└─ /shannon:restore    → Restore from checkpoint

SKILL MANAGEMENT
└─ /shannon:discover_skills → Discover all available skills

MCP MANAGEMENT
└─ /shannon:check_mcps → Validate MCP connections

MEMORY MANAGEMENT
└─ /shannon:memory     → Memory operations

PROJECT SETUP
└─ /shannon:scaffold   → Project scaffolding

TESTING
└─ /shannon:test       → Functional testing (NO MOCKS)

DIAGNOSTICS
├─ /shannon:status     → Framework health check
└─ /shannon:ultrathink → Deep debugging with sequential thinking (V5 NEW)
```

---

## Decision Tree: Which Command To Use?

### "I want to execute a task"

**Option 1: /shannon:do** (Recommended for most cases)
- **Use when**: General task execution in any project
- **Intelligence**: Auto-detects if needs spec analysis, research, context exploration
- **Best for**: Both new and existing projects, simple to complex tasks
- **Example**: `/shannon:do "add authentication with Auth0"`
- **Workflow**:
  1. Checks Serena for project context (< 1s)
  2. If first time: Explores project OR runs spec if complex
  3. If returning: Loads cached context
  4. Detects if research needed (external libraries)
  5. Executes with full context
  6. Saves to Serena for next time

**Option 2: /shannon:exec** (Structured approach)
- **Use when**: You want explicit library discovery + validation gates
- **Intelligence**: Systematic library research, 3-tier functional validation
- **Best for**: Projects requiring external dependencies, strict validation
- **Example**: `/shannon:exec "add authentication to React app"`
- **Workflow**:
  1. Runs /shannon:prime for context
  2. Discovers libraries (npm, PyPI, etc.)
  3. Analyzes task
  4. Generates code with discovered libraries
  5. Validates functionally (build + tests + functionality)
  6. Commits atomically (only validated code)
  7. Retries on failure (max 3x)

**Option 3: /shannon:task** (Full automation)
- **Use when**: You want complete automation from spec to execution
- **Intelligence**: Orchestrates prime→spec→wave automatically
- **Best for**: Well-defined specifications, large projects
- **Example**: `/shannon:task "Build REST API with auth" --auto`
- **Workflow**:
  1. Runs /shannon:prime (session setup)
  2. Runs /shannon:spec (8D analysis)
  3. If complexity >= 0.50: Runs /shannon:wave
  4. Returns ready-to-develop state

**Quick Comparison**:
| Command | Best For | Intelligence Level | Automation |
|---------|----------|-------------------|------------|
| do      | General tasks | High (auto-detects everything) | Medium |
| exec    | Validated execution | Medium (structured process) | High |
| task    | Full workflow | Medium (follows workflow) | Highest |

---

### "I want to design an approach before coding"

**Use: /shannon:brainstorm**
- **When**: Requirements or architecture still fluid, need ≥3 options.
- **Output**: `docs/plans/brainstorm/YYYY-MM-DD-<slug>.md` with option pros/cons, 8D mini-scores, wave recommendations.
- **Best for**: Large features, failing waves, or unfamiliar domains.
- **Next**: `/shannon:spec` (quantify) → `/shannon:write_plan`.

---

### "I want to convert the chosen option into a plan"

**Use: /shannon:write_plan**
- **When**: Direction locked, execution requires multiple agents or careful sequencing.
- **Output**: Implementation plan with files, code snippets, NO MOCKS tests, commit instructions.
- **Best for**: Complex refactors, multi-step features, onboarding new collaborators.
- **Next**: `/shannon:execute_plan <plan>` or `/shannon:do` (if intelligent execution preferred).

---

### "I want to execute a documented plan"

**Use: /shannon:execute_plan**
- **When**: Plan exists and you want deterministic execution with checkpoints.
- **Modes**: `--mode subagent` (pause after each task) or `--mode solo`.
- **Behavior**: Replays plan tasks exactly, runs failing tests first, checkpoints via Serena.
- **Best for**: Compliance-sensitive work, multi-operator handoffs, long-running features.

---

### "I want to analyze complexity"

**Option 1: /shannon:spec** (Specification analysis)
- **Use when**: You have a specification/requirements and need 8D complexity score
- **Output**: 8D scores, domain breakdown, execution strategy, MCP recommendations
- **Example**: `/shannon:spec "Build e-commerce platform with inventory, payments, admin dashboard"`
- **When required**: MANDATORY before any implementation (Shannon Iron Law)

**Option 2: /shannon:analyze** (Project analysis)
- **Use when**: You have existing code and need architecture/technical debt assessment
- **Output**: Architecture patterns, tech stack, technical debt, complexity hotspots
- **Example**: `/shannon:analyze authentication --deep`
- **Use case**: Understanding existing projects, planning refactors

---

### "I want to set up my session"

**Use: /shannon:prime**
- **Purpose**: Complete session initialization
- **Workflow**: Discovers skills → Verifies MCPs → Restores context (if resume) → Loads memories → Activates forced reading
- **Options**:
  - `--fresh`: Force fresh session
  - `--resume`: Force resume from checkpoint
  - `--quick`: Fast mode (< 10s)
  - `--full`: Deep mode (90s)
- **Example**: `/shannon:prime` (auto-detects fresh vs resume)
- **When**: At the start of every session

---

### "I want parallel execution"

**Use: /shannon:wave**
- **Purpose**: Wave-based parallel sub-agent execution
- **When**: Complexity >= 0.50 (Shannon threshold)
- **Benefits**: 3.5x average speedup through true parallelism
- **Prerequisites**: Must run /shannon:spec first
- **Options**:
  - `--plan`: Generate plan without executing
  - `--dry-run`: Detailed execution plan with impact analysis
- **Example**: `/shannon:wave Build authentication system`
- **Workflow**:
  1. Creates pre-wave checkpoint
  2. Invokes wave-orchestration skill
  3. WAVE_COORDINATOR spawns agents in parallel
  4. Synthesis checkpoints between waves
  5. Functional testing (NO MOCKS)
  6. Goal alignment validation
  7. Post-wave checkpoint

---

### "I want to manage goals"

**Use: /shannon:north_star**
- **Purpose**: Set and track North Star goals with measurable milestones
- **Operations**:
  - Set goal: `/shannon:north_star "Build production-ready SaaS platform"`
  - List goals: `/shannon:north_star`
  - Update progress: `/shannon:north_star --update`
  - View history: `/shannon:north_star --history`
- **Integration**: goal-alignment skill validates wave results against North Star

---

### "I want to validate my work"

**Use: /shannon:reflect**
- **Purpose**: Honest gap analysis before claiming work complete
- **When**: BEFORE any "work complete" claim
- **Workflow**:
  1. Reads original plan
  2. Inventories delivered work
  3. Compares plan vs delivery
  4. Runs 100+ sequential thoughts
  5. Calculates honest completion %
  6. Presents options (complete remaining, fix critical, accept as-is)
- **Options**:
  - `--scope plan|project|session`
  - `--min-thoughts N` (default: 100)
- **Example**: `/shannon:reflect --min-thoughts 150`

---

### "I want to debug deeply"

**Use: /shannon:ultrathink** (V5 NEW)
- **Purpose**: Deep debugging with sequential thinking + systematic debugging
- **When**: Hard problems, root cause analysis, complex bugs
- **Workflow**:
  1. Invokes sequential-thinking MCP (100+ thoughts)
  2. Applies systematic debugging protocol
  3. Uses forced reading for all relevant code
  4. Root cause tracing
  5. Generates solution with verification
- **Options**:
  - `--thoughts N`: Minimum thoughts (default: 150)
  - `--verify`: Auto-verify solution
- **Example**: `/shannon:ultrathink "Race condition in payment processing"`
- **MCP Requirements**: sequential-thinking (MANDATORY)

---

### "I want to manage context"

**Checkpoint: /shannon:checkpoint**
- **Use when**: Before long-running tasks, explicit save points
- **Note**: PreCompact hook handles automatically - manual use rarely needed
- **Example**: `/shannon:checkpoint "before-refactor"`

**Restore: /shannon:restore**
- **Use when**: Resuming after context loss, continuing from checkpoint
- **Options**:
  - `--latest`: Restore most recent checkpoint
  - Specific ID: `/shannon:restore SHANNON-W3-20251108T140000`
- **Example**: `/shannon:restore --latest`

---

## Command → Skill Invocation Map

| Command | Invokes Skills |
|---------|---------------|
| /shannon:do | intelligent-do → (spec-analysis, wave-orchestration, memory-coordination) |
| /shannon:exec | exec → (wave-orchestration, functional-testing) |
| /shannon:task | (calls /shannon:prime, /shannon:spec, /shannon:wave) |
| /shannon:wave | wave-orchestration, context-preservation, functional-testing (conditional), goal-alignment |
| /shannon:spec | spec-analysis |
| /shannon:analyze | shannon-analysis, confidence-check (if --deep) |
| /shannon:prime | skill-discovery, context-restoration, memory-coordination |
| /shannon:north_star | goal-management |
| /shannon:reflect | honest-reflections |
| /shannon:ultrathink | (sequential-thinking MCP, systematic-debugging, forced-reading) |
| /shannon:discover_skills | skill-discovery |
| /shannon:test | functional-testing |

---

## Skill → Command Invocation Map

| Skill | Invoked By Commands |
|-------|-------------------|
| intelligent-do | /shannon:do |
| exec | /shannon:exec |
| spec-analysis | /shannon:spec, /shannon:do (auto), /shannon:task (auto) |
| wave-orchestration | /shannon:wave, /shannon:do (auto if complex), /shannon:exec, /shannon:task (auto) |
| shannon-analysis | /shannon:analyze |
| confidence-check | /shannon:analyze --deep |
| goal-management | /shannon:north_star |
| honest-reflections | /shannon:reflect |
| functional-testing | /shannon:test, /shannon:wave (auto), /shannon:exec (auto) |
| skill-discovery | /shannon:prime, /shannon:discover_skills |
| context-preservation | /shannon:checkpoint, /shannon:wave (auto), PreCompact hook (auto) |
| context-restoration | /shannon:restore, /shannon:prime --resume |
| memory-coordination | /shannon:do, /shannon:prime, /shannon:memory |
| goal-alignment | /shannon:wave (auto if north_star exists) |

---

## MCP Requirements By Command

### Mandatory MCPs

**Serena MCP** (REQUIRED for all Shannon commands)
- Used by: All commands that save/load context
- Fallback: None (Shannon cannot function without Serena)
- Commands affected: /shannon:do, /shannon:exec, /shannon:wave, /shannon:prime, /shannon:checkpoint, /shannon:restore, /shannon:spec, /shannon:task

**Sequential Thinking MCP** (REQUIRED for ultrathink)
- Used by: /shannon:ultrathink
- Fallback: Command fails without it
- Purpose: 100+ thought deep analysis

### Recommended MCPs

**Sequential Thinking MCP** (RECOMMENDED for complex analysis)
- Used by: /shannon:spec (complexity >= 0.70), /shannon:reflect, /shannon:analyze --deep
- Fallback: Works without it but less effective
- Purpose: Deep complexity analysis, reflection

**Context7 MCP** (RECOMMENDED for library research)
- Used by: /shannon:do (auto library detection), /shannon:exec
- Fallback: Uses Tavily/Firecrawl instead
- Purpose: Library documentation lookup

**Tavily/Firecrawl MCP** (RECOMMENDED for research)
- Used by: /shannon:do (auto research), /shannon:exec
- Fallback: Skips research
- Purpose: Best practices research

**Puppeteer MCP** (RECOMMENDED for functional testing)
- Used by: /shannon:test, /shannon:wave (if UI testing), /shannon:exec
- Fallback: Manual testing instructions
- Purpose: Real browser testing (NO MOCKS enforcement)

---

## Common Workflows

### Workflow 1: Start New Project

```bash
# 1. Initialize session
/shannon:prime

# 2. Analyze specification
/shannon:spec "Build task management app with React, Node.js, PostgreSQL"

# 3. Execute with waves (if complexity >= 0.50)
/shannon:wave

# OR: Use task for full automation
/shannon:task "Build task management app with React, Node.js, PostgreSQL" --auto
```

### Workflow 2: Work on Existing Project

```bash
# 1. Initialize session (auto-resumes if recent work)
/shannon:prime

# 2. Execute task intelligently
/shannon:do "add password reset feature"

# do command will:
# - Load project context from Serena (< 1s)
# - Detect tech stack
# - Execute with full context
# - Save results
```

### Workflow 3: Complex Bug Investigation

```bash
# 1. Deep debugging
/shannon:ultrathink "Race condition causing intermittent payment failures" --thoughts 200 --verify

# ultrathink will:
# - Run 200+ sequential thoughts
# - Apply systematic debugging
# - Force-read all relevant code
# - Trace root cause
# - Generate verified solution
```

### Workflow 4: Project Health Check

```bash
# 1. Analyze project
/shannon:analyze --deep

# 2. If technical debt high, create refactor plan
/shannon:spec "Refactor authentication module to reduce technical debt"

# 3. Execute refactoring with waves
/shannon:wave
```

### Workflow 5: Goal-Driven Development

```bash
# 1. Set North Star goal
/shannon:north_star "Launch production-ready SaaS platform by Q2"

# 2. Execute tasks with goal alignment
/shannon:do "build user authentication system"

# 3. Validate alignment after major milestones
/shannon:reflect
```

---

## Shannon Iron Laws

These workflows are **MANDATORY** and cannot be violated:

### Iron Law 1: Spec Before Implementation
- **Rule**: ALWAYS run `/shannon:spec` before any implementation
- **Why**: Removes subjective bias from complexity estimation
- **Enforced by**: using-shannon skill (session start)
- **Violation**: Implementation without quantitative analysis

### Iron Law 2: Wave Execution for Complexity >= 0.50
- **Rule**: Use `/shannon:wave` for projects scoring >= 0.50
- **Why**: 3.5x proven speedup through true parallelism
- **Enforced by**: spec-analysis skill recommendations
- **Violation**: Sequential execution for Complex+ projects

### Iron Law 3: NO MOCKS Testing
- **Rule**: Functional tests ONLY (real browsers, real DBs, real APIs)
- **Why**: Mocks test mock behavior, not production behavior
- **Enforced by**: functional-testing skill, post_tool_use.py hook
- **Violation**: Unit tests with mocks/stubs

### Iron Law 4: Automatic Checkpointing
- **Rule**: PreCompact hook triggers automatically
- **Why**: Prevents context loss from compaction
- **Enforced by**: PreCompact hook (automatic)
- **Violation**: Manual checkpoint management after compaction

### Iron Law 5: Synthesis After Every Wave
- **Rule**: Mandatory user validation between waves
- **Why**: Prevents duplicate work, ensures context sharing
- **Enforced by**: wave-orchestration skill
- **Violation**: Skipping synthesis checkpoints

### Iron Law 6: Forced Reading Sentinel
- **Rule**: When sentinel banner appears, pause and perform full-file reading.
- **Why**: Large prompts/files (>10k chars, >400 lines, large code blocks, explicit ranges) cause comprehension failures.
- **Enforced by**: `hooks/user_prompt_submit.py` + `skills/forced-reading-sentinel`.
- **Violation**: Responding without confirming full read & summary.

---

## V5 New Features

### 1. /shannon:ultrathink Command
- Deep debugging with sequential thinking
- Systematic debugging protocol
- Forced reading enforcement
- Root cause tracing
- 150+ thought minimum by default

### 2. Project-Specific Custom Instructions
- Auto-generated from project conventions
- Persisted in `.shannon/custom_instructions.md`
- Loaded at session start
- Examples: CLI argument defaults, build commands, test patterns

### 3. Command Namespacing
- All commands now use `shannon:` prefix
- Prevents conflicts with other plugins
- Examples: `/shannon:do`, `/shannon:wave`, `/shannon:spec`

### 4. Enhanced Skill Discovery
- Automatic at `/shannon:prime`
- Caches results for fast reloading
- Discovers 100+ skills across project/user/plugin

### 5. Planning Command Suite
- `/shannon:brainstorm` – divergent option generation with 8D mini-scores.
- `/shannon:write_plan` – detailed plan docs with files/tests/checkpoints.
- `/shannon:execute_plan` – deterministic plan execution with Serena checkpoints.
- Provides feature parity with superpowers writing/executing workflows while enforcing NO MOCKS and wave heuristics.

### 6. Systematic Debugging + Root Cause Skills
- New `skills/systematic-debugging` and `skills/root-cause-analysis`.
- `/shannon:ultrathink` now explicitly delegates to these skills.
- Output includes hypothesis logs, causal chains, and prevention steps.

### 7. Forced Reading Sentinel
- `skills/forced-reading-sentinel` + `hooks/user_prompt_submit.py` watch for large prompts/files.
- Thresholds: ≥10k characters, ≥400 lines, ≥200-line code block, explicit range references.
- Injects banner instructing agent to follow `core/FORCED_READING_PROTOCOL.md` before responding.

---

## Migration from V4 to V5

### Breaking Changes
- **Command Namespacing**: All commands require `shannon:` prefix
  - Old: `/do "task"`
  - New: `/shannon:do "task"`

### New Additions (Non-Breaking)
- `/shannon:ultrathink` - New deep debugging command
- Project-specific custom instructions system
- Enhanced MCP requirement documentation

### Compatibility
- V4 workflows still work with prefix added
- All skill invocations remain the same
- Serena checkpoints are compatible
- No re-priming needed for existing projects

---

## Troubleshooting

### "Which command should I use?"

**Use this decision tree**:
1. Starting session? → `/shannon:prime`
2. Have specification? → `/shannon:spec` first
3. Want to execute task? → `/shannon:do` (intelligent) OR `/shannon:exec` (structured)
4. Want full automation? → `/shannon:task`
5. Complexity >= 0.50? → `/shannon:wave`
6. Deep debugging needed? → `/shannon:ultrathink`
7. Want to validate work? → `/shannon:reflect`

### "Do I need to run prime first?"

**No, most commands work without priming**, but priming is recommended because:
- Discovers all available skills
- Verifies MCP connections
- Restores context if returning
- Activates forced reading

**Commands that require priming**:
- `/shannon:task` (runs prime automatically)
- None - all other commands work standalone

### "When should I use waves?"

**Use `/shannon:wave` when**:
- Complexity score >= 0.50 (Shannon threshold)
- Project has parallelizable work streams
- Want 3.5x speedup vs sequential

**Don't use waves when**:
- Complexity < 0.50 (overhead exceeds benefits)
- Work is inherently sequential
- Single-file tasks

---

## References

- Complete 8D Algorithm: `core/SPEC_ANALYSIS.md`
- Wave Orchestration: `core/WAVE_ORCHESTRATION.md`
- Testing Philosophy: `core/TESTING_PHILOSOPHY.md`
- Hook System: `core/HOOK_SYSTEM.md`
- Forced Reading Protocol: `core/FORCED_READING_PROTOCOL.md`

---

**Version**: 5.4.0
**Last Updated**: 2025-11-18
**Status**: Definitive orchestration guide

