# Shannon Framework

**Version 5.6.0** | [Installation](#installation) | [Quick Start](#quick-start) | [Documentation](#documentation) | [GitHub](https://github.com/krzemienski/shannon-framework)

> **🚀 V5.6.0 "Comprehensive Quality & Intelligence"**: 14 new skills, `/shannon:health` dashboard, advanced testing, security automation!
> See [docs/v5.6/CHANGELOG.md](docs/v5.6/CHANGELOG.md) for complete details.

---

## Overview

Shannon Framework is a **Claude Code plugin** that transforms AI-assisted development from ad-hoc interactions into a rigorous, quantitative, reproducible methodology. Built for mission-critical domains—Finance, Healthcare, Legal, Security, Aerospace—Shannon replaces subjective judgments with objective measurements throughout the development lifecycle.

### What Shannon IS

- **Complete Development Methodology**: Specification → Planning → Execution → Testing → Reflection
- **Multi-Layer Enforcement Architecture**: 4 layers (Commands → Skills → Hooks → Core Files) enforcing same principles
- **Quantitative Framework**: Replace "seems complex" with 8D complexity scores (0.00-1.00)
- **Production-Tested System**: Built by observing actual LLM violations, creating explicit counters

### What Shannon IS NOT

- ❌ Code generation tool
- ❌ Testing framework
- ❌ Project scaffolder
- ✅ **Complete methodology** for specification-driven development with quantitative rigor

### Core Value Proposition

**Quantitative Over Qualitative**: Replace ALL subjective judgments with objective measurements.

| Traditional Approach | Shannon Framework |
|---------------------|-------------------|
| "Seems complex" | 8D complexity score: 0.72/1.00 (VERY COMPLEX) |
| "Need 3-4 agents" | Formula: complexity × bands = 8-15 agents |
| "Making progress" | Quantified: 65% complete (+12% this session) |
| "Tests look fine" | NO MOCKS compliance: 100% or fail |
| "Architecture aligns" | Alignment score: 87/100 (STRONG) |

---

## Architecture

### 4-Layer Enforcement Pyramid

```
                         USER
                           │
                           ↓
            ┌──────────────────────────┐
            │   COMMANDS (Layer 4)     │  ← User-facing interface
            │   15 slash commands      │     /shannon:spec, /shannon:wave
            └────────────┬─────────────┘     Delegate to skills
                         ↓                   Format output
            ┌──────────────────────────┐
            │   SKILLS (Layer 3)       │  ← Workflow implementation
            │   18 behavioral patterns │     Execute methodologies
            └────────────┬─────────────┘     Save to Serena
                         ↓                   Reference core files
            ┌──────────────────────────┐
            │   HOOKS (Layer 2)        │  ← Automatic enforcement
            │   5 lifecycle scripts    │     Block violations
            └────────────┬─────────────┘     Inject context
                         ↓                   Cannot be skipped
            ┌──────────────────────────┐
            │  CORE FILES (Layer 1)    │  ← Foundational specs
            │  9 reference documents   │     11K lines total
            └──────────────────────────┘     Complete algorithms
                         ↓
                   SERENA MCP
              (Central State Store)
```

### Component Inventory

| Layer | Count | Purpose | Examples |
|-------|-------|---------|----------|
| **Commands** | 20 | User entry points | shannon:init, shannon:do, shannon:wave, shannon:spec, shannon:ultrathink |
| **Skills** | 21 | Workflow implementation | project-onboarding, spec-analysis, wave-orchestration, intelligent-do |
| **Hooks** | 5 | Automatic enforcement | post_tool_use (NO MOCKS), precompact |
| **Core Files** | 9 | Reference specs (11K lines) | TESTING_PHILOSOPHY, SPEC_ANALYSIS |
| **Agent Guides** | 25 | Agent usage documentation | WAVE_COORDINATOR, TEST_GUARDIAN |

### Infrastructure Dependencies

**Mandatory**:
- **Claude Code**: Plugin platform (required)
- **Serena MCP**: Persistent state store (61% of skills require it)

**Recommended**:
- **Sequential MCP**: Deep reasoning (100+ thoughts for complex analysis), **REQUIRED for `/shannon:ultrathink`**
- **Context7 MCP**: Framework-specific documentation
- **Tavily MCP**: Best practices research

**Conditional** (based on project type):
- **Puppeteer MCP**: Web testing (NO MOCKS requirement)
- **iOS Simulator MCP**: Mobile testing
- **Platform-specific MCPs**: As needed for real system testing

---

## Installation

### Prerequisites

1. **Claude Code** (latest version)
2. **Serena MCP** (mandatory - 61% of skills require it)
3. **Sequential MCP** (recommended for complex analysis)

### Installation Steps

**⭐ Recommended: Universal Installation** (Works for both Claude Code and Cursor IDE)

```bash
# Clone repository
git clone https://github.com/shannon-framework/shannon.git
cd shannon

# Install for both editors
./install_universal.sh

# Or install for specific editor
./install_universal.sh --cursor   # Cursor IDE only
./install_universal.sh --claude   # Claude Code only

# Restart your editor
```

**Alternative Options**:

1. **Local Installation (Claude Code only)**:
   ```bash
   ./install_local.sh
   ```
   More reliable than plugin system. See [INSTALL_LOCAL.md](INSTALL_LOCAL.md)

2. **Plugin Installation (Claude Code only)**:
   ```bash
   # In Claude Code CLI:
   /plugin marketplace add shannon-framework/shannon
   /plugin install shannon@shannon-framework
   ```
   May have discovery issues. Use local/universal installation instead.

**Installation Guides**:
- **Universal (Both Editors)**: [INSTALL_UNIVERSAL.md](INSTALL_UNIVERSAL.md) ⭐ Recommended
- **Claude Code Local**: [INSTALL_LOCAL.md](INSTALL_LOCAL.md)
- **Plugin (Legacy)**: May not discover components properly

### Verification

```bash
# Check Shannon is installed
/shannon:status

# Expected output:
# ✅ Shannon Framework v5.0.0
# ✅ Serena MCP: Connected
# ✅ Skills loaded: 18/18
# ✅ Commands available: 15/15
```

### Quick Start

```bash
# Prime your session (loads skills, MCPs, context)
/shannon:prime

# Analyze a specification
/shannon:spec "Build a task management web app with React and Node.js"

# Execute with wave orchestration
/shannon:wave

# Run functional tests (NO MOCKS)
/shannon:test

# Reflect before completion
/shannon:reflect
```

---

## Core Concepts

### 1. 8D Complexity Analysis

**What**: Quantitative specification scoring across 8 dimensions

**Dimensions**:
1. **Structural** (0-10): Codebase organization complexity
2. **Cognitive** (0-15): Mental model complexity
3. **Coordination** (0-10): Team/agent coordination needs
4. **Temporal** (0-10): Time-based dependencies
5. **Environmental** (0-10): External integrations
6. **Algorithmic** (0-15): Logic complexity
7. **Uncertainty** (0-15): Unknown factors
8. **Risk** (0-15): Failure impact

**Output**: Total score 0.00-1.00
- 0.00-0.30: SIMPLE (1-3 agents, 1-3 hours)
- 0.30-0.50: MODERATE (3-5 agents, 5-15 hours)
- 0.50-0.70: COMPLEX (5-8 agents, 1-4 days)
- 0.70-1.00: VERY COMPLEX (8-15 agents, 4-12 days)

**Why It Matters**: Replaces "seems complex" with objective measurement. Drives resource allocation, timeline estimation, wave planning.

**Example**:
```
Specification: "E-commerce platform with inventory, payments, recommendations"
8D Score: 0.72 (VERY COMPLEX)
Recommended: 8-15 agents, 3-7 days, 4-6 waves
```

### 2. Wave Orchestration

**What**: Parallel execution of independent work units

**How It Works**:
1. Complexity analysis determines work can be parallelized
2. Break into independent units (waves)
3. Spawn agents in parallel (all in ONE Claude Code message)
4. Create checkpoints between waves
5. Synthesize results

**Performance**:
- 2 agents: 1.5-1.8x speedup
- 3 agents: 2.0-2.5x speedup
- 5 agents: 3.0-4.0x speedup
- 7+ agents: 3.5-5.0x speedup
- **Average**: 3.5x faster than sequential

**Example**:
```bash
/shannon:wave

# Shannon analyzes spec (0.68 complexity)
# Creates 3 waves:
#   Wave 1: Backend API (agents: BACKEND, DATABASE_ARCHITECT)
#   Wave 2: Frontend UI (agents: FRONTEND, MOBILE_DEVELOPER)
#   Wave 3: Testing (agents: TEST_GUARDIAN, QA)
#
# All agents spawn in parallel
# Checkpoint after each wave
# 3.2x speedup vs sequential
```

### 3. NO MOCKS Testing (Iron Law)

**What**: Functional tests ONLY. Zero tolerance for mocks.

**Enforcement** (4 layers):
1. **Core File**: TESTING_PHILOSOPHY.md explains why
2. **Meta-Skill**: using-shannon declares as Iron Law
3. **Skill**: functional-testing implements patterns
4. **Hook**: post_tool_use.py blocks mock usage automatically

**Why**: Mocks test code, not functionality. Real dependencies test integration, failure modes, performance.

**Detection**:
- PostToolUse hook scans all Write/Edit operations
- Patterns: `jest.mock()`, `@mock`, `sinon.stub()`, etc.
- **Action**: Block write, force real implementation

**Fallback Strategy**:
- Web → Puppeteer MCP (real browser)
- Mobile → iOS Simulator MCP (real device)
- API → HTTP client (real requests)
- Database → Database MCP (real DB, test schema)

**Authority Resistance**: If authority demands mocks:
1. Explain functional testing value (15min)
2. Show data (mock coverage ≠ functional coverage)
3. Calculate cost (mock debt accumulation)
4. Offer compromise (critical paths functional, rest can be mocked)
5. Document decision and risks
6. Comply if authority insists (with documented objection)
7. Escalate if pattern emerges

### 4. Context Preservation

**What**: Zero-loss state management across sessions

**Mechanism**:
- **PreCompact Hook**: Fires before context compression (15s timeout)
- Creates checkpoint in Serena MCP
- Stores: specs, goals, waves, progress, decisions
- **Guaranteed**: Cannot compress without checkpoint

**Usage**:
```bash
# Manual checkpoint
/shannon:checkpoint "before-refactor"

# Automatic checkpoints (via PreCompact hook)
# [Happens automatically when context fills]

# Restore from checkpoint
/shannon:restore --latest
/shannon:restore "before-refactor"

# List available
/shannon:checkpoint --list
```

**Why**: Context loss = lost decisions, rationale, progress. Shannon eliminates this entirely.

### 5. Goal Management (North Star)

**What**: Project-level goal tracking and alignment validation

**Workflow**:
```bash
# Set North Star goal
/shannon:north_star "Build production-ready task manager with 99.9% uptime"

# Goal injected into EVERY prompt (via UserPromptSubmit hook)

# Validate alignment
/shannon:wave  # (automatically checks goal alignment)

# Output includes:
# ✅ Goal Alignment: 94/100 (STRONG)
#    - Core features align perfectly
#    - Performance requirements met
#    - Production readiness on track
```

**Purpose**: Prevents scope drift. Every decision validated against original goal.

---

## Components Deep Dive

### Commands (15 Total)

User-invocable slash commands. Invocation: `/shannon:command_name`

#### Session Management (4)

| Command | Purpose | Skill(s) |
|---------|---------|----------|
| `prime` | Session initialization, auto-resume | skill-discovery, mcp-discovery, context-restoration, goal-management |
| `checkpoint` | Create state snapshot | context-preservation |
| `restore` | Load from checkpoint | context-restoration, goal-management |
| `status` | Shannon health check | mcp-discovery, goal-management |

#### Analysis & Planning (3)

| Command | Purpose | Skill(s) |
|---------|---------|----------|
| `spec` | 8D complexity analysis | spec-analysis |
| `analyze` | Project analysis with confidence | shannon-analysis, confidence-check |
| `discover_skills` | Catalog available skills | skill-discovery |

#### Execution (4)

| Command | Purpose | Skill(s) |
|---------|---------|----------|
| `exec` | **NEW V5.1** Autonomous execution with libraries & validation | exec, wave-orchestration, context-preservation |
| `wave` | Parallel wave execution | wave-orchestration, context-preservation, functional-testing, goal-alignment |
| `task` | Automated prime→spec→wave | [Chains multiple commands] |
| `scaffold` | Generate project structure | spec-analysis, project-indexing, functional-testing |

#### Quality & Testing (2)

| Command | Purpose | Skill(s) |
|---------|---------|----------|
| `test` | NO MOCKS functional testing | functional-testing |
| `reflect` | Honest gap analysis | honest-reflections |

#### Infrastructure (2)

| Command | Purpose | Skill(s) |
|---------|---------|----------|
| `check_mcps` | Verify MCP configuration | mcp-discovery |
| `memory` | Memory system coordination | memory-coordination |

#### Goals (1)

| Command | Purpose | Skill(s) |
|---------|---------|----------|
| `north_star` | Set/manage project goal | goal-management |

### Skills (18 Total)

Reusable behavioral patterns. Categorized by enforcement type.

#### RIGID Skills (2) - 100% Enforcement

| Skill | Purpose | MCP |
|-------|---------|-----|
| `using-shannon` | Meta-skill for Shannon usage patterns | Serena (REQUIRED) |
| `functional-testing` | NO MOCKS testing enforcement | Serena (REQUIRED) |

#### PROTOCOL Skills (8) - 90% Enforcement

| Skill | Purpose | MCP |
|-------|---------|-----|
| `skill-discovery` | Automatic skill discovery and invocation | Serena (REQUIRED) |
| `phase-planning` | Context-safe phase creation | Serena (REQUIRED) |
| `task-automation` | Task breakdown and automation | Serena (REQUIRED) |
| `honest-reflections` | Self-assessment before completion | Serena (REQUIRED) |
| `context-preservation` | Checkpoint creation | Serena (REQUIRED) |
| `context-restoration` | Session state restoration | Serena (REQUIRED) |
| `memory-coordination` | Cross-session memory management | Serena (REQUIRED) |
| `sitrep-reporting` | Structured situation reports | Serena (REQUIRED) |

#### QUANTITATIVE Skills (5) - 80% Enforcement

| Skill | Purpose | MCP |
|-------|---------|-----|
| `spec-analysis` | 8D complexity specification analysis | Serena (RECOMMENDED) |
| `wave-orchestration` | Parallel wave execution management | Serena (REQUIRED) |
| `confidence-check` | Pre-completion confidence verification | Serena (RECOMMENDED) |
| `goal-alignment` | North Star alignment validation | Serena (RECOMMENDED) |
| `mcp-discovery` | MCP server discovery patterns | Serena (RECOMMENDED) |

#### FLEXIBLE Skills (3) - 70% Enforcement

| Skill | Purpose | MCP |
|-------|---------|-----|
| `shannon-analysis` | Shannon-specific analysis workflow | Serena (RECOMMENDED) |
| `goal-management` | Goal lifecycle management | Serena (RECOMMENDED) |
| `shannon-quantified` | Shannon principle adherence measurement | Serena (RECOMMENDED) |

**Note**: 61% of skills (11/18) REQUIRE Serena MCP. The remaining 39% (7/18) have degraded fallbacks but strongly recommend Serena.

### Hooks (5 Total)

Event-driven automation scripts. Execute automatically on lifecycle events.

| Hook | Event | Purpose | Timeout |
|------|-------|---------|---------|
| `session_start.sh` | SessionStart | Load using-shannon meta-skill | 5000ms |
| `user_prompt_submit.py` | UserPromptSubmit | Inject North Star + wave context | 2000ms |
| `post_tool_use.py` | PostToolUse (Write/Edit/MultiEdit) | Block mock usage (NO MOCKS) | 3000ms |
| `precompact.py` | PreCompact | Create context checkpoint | 15000ms |
| `stop.py` | Stop | Enforce wave validation gates | 2000ms |

**Key Features**:
- `user_prompt_submit.py`: Fires on EVERY prompt (cannot skip)
- `post_tool_use.py`: Matcher pattern blocks mock writes automatically
- `precompact.py`: `continueOnError: false` - MUST succeed before compaction
- All hooks automatic - no user action required

### Core Files (9 Total)

Always-on behavioral pattern files (11,045 lines total).

| Core File | Domain | Purpose |
|-----------|--------|---------|
| `CONTEXT_MANAGEMENT.md` | Context | Context preservation patterns |
| `FORCED_READING_PROTOCOL.md` | Quality | Complete reading enforcement |
| `HOOK_SYSTEM.md` | System | Hook architecture documentation |
| `MCP_DISCOVERY.md` | Integration | MCP server discovery patterns |
| `PHASE_PLANNING.md` | Planning | Context-safe phase methodology |
| `PROJECT_MEMORY.md` | Memory | Memory system architecture |
| `SPEC_ANALYSIS.md` | Analysis | 8D complexity methodology |
| `TESTING_PHILOSOPHY.md` | Quality | NO MOCKS testing philosophy |
| `WAVE_ORCHESTRATION.md` | Execution | Parallel wave patterns |

**Loading**: Injected into Claude's system prompt at plugin initialization.

---

## Usage Guide

### First-Time Setup

```bash
# 1. Verify installation
/shannon:status

# 2. Check MCP servers
/shannon:check_mcps

# 3. Set project goal
/shannon:north_star "Build production-ready authentication system with 99.9% uptime"

# 4. Prime session
/shannon:prime

# 5. Ready to work!
```

### Common Workflows

#### New Project

```bash
# 1. Set goal
/shannon:north_star "Build e-commerce platform with inventory, payments, recommendations"

# 2. Analyze specification
/shannon:spec "Detailed specification text here..."

# Output:
# 8D Complexity: 0.72 (VERY COMPLEX)
# Recommended: 8-15 agents, 4-6 waves, 3-7 days

# 3. Execute with waves
/shannon:wave

# Or use task command (automates prime→spec→wave)
/shannon:task "specification text" --auto
```

#### Session Resume

```bash
# Automatic detection and restoration
/shannon:prime

# Output:
# ✅ Previous session detected
# ✅ Restored: spec, goals, waves, progress
# ✅ Ready to continue from: Wave 3/5 (62% complete)
```

#### Complex Project

```bash
# 1. Deep analysis
/shannon:analyze --deep

# 2. Review complexity
/shannon:spec "full specification"

# 3. Plan waves
/shannon:wave --plan

# 4. Review plan, then execute
/shannon:wave

# 5. Create checkpoint before risky work
/shannon:checkpoint "before-refactor"

# 6. Test (NO MOCKS)
/shannon:test

# 7. Reflect before completion
/shannon:reflect
```

### Best Practices

1. **Always Prime**: Start sessions with `/shannon:prime`
2. **Set North Star**: Define clear project goal upfront
3. **Trust 8D Scores**: Don't override complexity analysis without data
4. **Use Waves**: Parallel execution = 3.5x average speedup
5. **NO MOCKS**: Functional tests only, real dependencies
6. **Checkpoint Often**: Before refactors, major changes
7. **Reflect Before Complete**: Honest gap analysis prevents premature completion

### Performance Tips

1. **Cache Skills**: Use `--cache` flag (12x faster discovery)
2. **Auto-Resume**: `/shannon:prime` auto-detects previous session
3. **Quick Mode**: `/shannon:prime --quick` for time-sensitive work
4. **Parallel Waves**: Let Shannon determine agent count (don't override)

---

## Advanced Topics

### Creating Custom Skills

Shannon skills follow a strict template. See `templates/SKILL_TEMPLATE.md` for complete structure.

**Required Sections**:
- Frontmatter (name, description, type, allowed-tools)
- Purpose and When to Use
- Prerequisites
- Workflow (step-by-step)
- Anti-Rationalization (violations and counters)
- Validation
- Examples
- MCP Requirements

**Enforcement Types**:
- RIGID (100%): Exact execution, no adaptation
- PROTOCOL (90%): Required structure, adaptable details
- QUANTITATIVE (80%): Score-based, measurement-driven
- FLEXIBLE (70%): Principle-guided, contextual

### Understanding Enforcement Levels

Shannon uses **defense in depth** for critical behaviors:

**Example: NO MOCKS Testing**

1. **Layer 1 (Core)**: TESTING_PHILOSOPHY.md explains why
2. **Layer 2 (Hooks)**: post_tool_use.py blocks mock writes automatically
3. **Layer 3 (Skills)**: functional-testing enforces patterns
4. **Layer 4 (Commands)**: /shannon:test invokes enforcement stack

To violate, must defeat ALL 4 layers. Single-layer enforcement can be circumvented; multi-layer cannot.

### MCP Configuration Strategies

**Mandatory Setup**:
```bash
# Serena MCP (required for 61% of skills)
claude mcp add serena

# Verify
/shannon:check_mcps
```

**Recommended Setup**:
```bash
# Sequential MCP (deep reasoning)
claude mcp add sequential-thinking

# Context7 MCP (framework docs)
claude mcp add context7
```

**Conditional Setup** (project-specific):
```bash
# Web testing
claude mcp add puppeteer

# Mobile testing
claude mcp add ios-simulator

# API testing
claude mcp add http-client
```

**Validation**:
```bash
/shannon:check_mcps --verbose

# Output shows:
# ✅ Required: Serena (connected)
# ✅ Recommended: Sequential (connected)
# ⚠️ Conditional: Puppeteer (not installed, needed for web testing)
```

### Multi-Wave Project Patterns

For VERY COMPLEX projects (0.70-1.00), use multi-wave strategy:

**Wave 1: Foundation**
- Setup infrastructure
- Database schema
- Core models
- **Checkpoint**: `foundation-complete`

**Wave 2: Core Features**
- Authentication
- Primary workflows
- Business logic
- **Checkpoint**: `core-complete`

**Wave 3: Integration**
- External APIs
- Payment systems
- Email/notifications
- **Checkpoint**: `integration-complete`

**Wave 4: Testing & Polish**
- Functional tests (NO MOCKS)
- Performance optimization
- Security hardening
- **Checkpoint**: `testing-complete`

**Wave 5: Production Prep**
- Documentation
- Deployment automation
- Monitoring/logging
- **Checkpoint**: `production-ready`

Each wave creates checkpoint. If wave fails, restore and retry without losing previous work.

---

## Troubleshooting

### Common Issues

#### "Serena MCP not connected"

**Problem**: Commands fail with Serena errors

**Solution**:
```bash
# Check MCP status
claude mcp list

# Add Serena if missing
claude mcp add serena

# Verify
/shannon:check_mcps
```

#### "Skills not loading"

**Problem**: `/shannon:prime` shows 0/18 skills

**Solution**:
```bash
# Reinstall plugin
/plugin uninstall shannon@shannon-framework
/plugin install shannon@shannon-framework

# Restart Claude Code
```

#### "Wave execution slow"

**Problem**: Waves not parallelizing (no speedup)

**Solution**: Check complexity score
```bash
/shannon:spec "your spec"

# If complexity < 0.50:
# - May not warrant parallelization
# - Use --force flag if needed

/shannon:wave --force
```

#### "PostToolUse hook blocking legitimate code"

**Problem**: Hook detects non-mock code as mock

**Solution**:
```bash
# Review detection pattern in code
# Common false positives:
#   - "mock" in variable names
#   - "stub" in comments

# Rename variables if needed
# Or use --skip-hooks (not recommended)
```

#### "Context loss despite checkpoints"

**Problem**: Restored session missing data

**Solution**:
```bash
# List available checkpoints
/shannon:checkpoint --list

# Restore specific checkpoint
/shannon:restore "checkpoint-name"

# Check Serena memory
/serena:memory list
```

### Getting Help

- **Documentation**: This README + `/shannon:status --help`
- **Examples**: Each skill includes examples in `skills/{name}/examples/`
- **GitHub Issues**: [github.com/krzemienski/shannon-framework/issues](https://github.com/krzemienski/shannon-framework/issues)
- **Community**: Check GitHub Discussions

---

## Version History

### v5.0.0 (Current - January 2025)

**Major**:
- Comprehensive functional verification (4 test applications)
- Three-layer validation (Flow + Artifacts + Functionality)
- Enhanced architecture documentation (10 analysis documents)

**Status**: Functional verification in progress

### v4.1.0 (December 2024)

**Major Enhancements**:
1. **Forced Complete Reading Protocol**: Ensures complete content consumption
2. **Automatic Skill Discovery & Invocation**: Skills auto-activate based on context
3. **Unified /shannon:prime Command**: Single command for session initialization

**Performance**:
- Skill discovery: 12x faster (cache)
- Prime command: 35-50s auto-resume mode
- Wave orchestration: 3.5x average speedup

**Backward Compatibility**: ✅ Full V3 compatibility maintained

### v4.0.0 (November 2024)

**Major Refactor**:
- Commands refactored to delegate to skills (was monolithic)
- Hook system introduced (5 lifecycle hooks)
- Core files formalized (9 behavioral patterns)
- Serena MCP integration (61% of skills require it)

**New Commands**: analyze, task, scaffold
**New Skills**: confidence-check, goal-alignment, shannon-quantified
**Breaking Changes**: None (V3 compatibility maintained)

### v3.x (Legacy)

Monolithic command architecture (all logic in commands). Deprecated but backward-compatible.

---

## Contributing & Support

### Contributing

See `CONTRIBUTING.md` for:
- Code of conduct
- Development workflow
- Testing requirements
- PR process

### Creating Skills

1. Copy `templates/SKILL_TEMPLATE.md`
2. Fill all required sections
3. Add anti-rationalization (violations + counters)
4. Include examples and tests
5. Submit PR

### Testing

```bash
# Validate Shannon v5.0
python validate_shannon_v5.py

# Run skill tests
cd skills/{skill-name}/tests
./run_tests.sh
```

### Support

- **Issues**: [GitHub Issues](https://github.com/krzemienski/shannon-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/krzemienski/shannon-framework/discussions)
- **Email**: info@shannon-framework.dev

---

## License

MIT License - see LICENSE file for details

---

## Acknowledgments

Built with Claude Code and inspired by Claude Shannon's information theory principles. Special thanks to the Anthropic team for Claude Code's plugin architecture and MCP ecosystem.

---

**Install Shannon**: `/plugin install shannon@shannon-framework`

**Documentation**: This README + skill-specific guides in `skills/` directory

**Version**: 5.0.0 | **License**: MIT | **Maintainer**: Shannon Framework Team
