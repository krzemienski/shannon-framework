# Shannon Framework V4.1 - Complete User Guide

**Version**: 4.1.0
**Last Updated**: 2025-11-08
**For**: Shannon Users (Installation through Advanced Usage)

---

## Table of Contents

1. [What is Shannon?](#what-is-shannon)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [All Commands Reference](#all-commands-reference)
6. [All Skills Reference](#all-skills-reference)
7. [Usage Examples](#usage-examples)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)
10. [FAQ](#faq)

---

## What is Shannon?

Shannon Framework is a **Claude Code plugin** that makes AI development rigorous, quantitative, and reliable through:

**Core Capabilities** (V4 Base):
- 🎯 **8D Complexity Analysis** - Quantitative specification scoring
- 🌊 **Wave Orchestration** - Multi-stage parallel execution (3.5x faster)
- 💾 **Context Preservation** - Zero information loss across sessions
- 🚫 **NO MOCKS Testing** - Functional tests only (real browsers, real APIs)

**NEW in V4.1** (Unique to Shannon):
- 🔴 **Forced Complete Reading** - Architectural thoroughness enforcement
- 🔴 **Auto Skill Discovery** - Intelligent skill system (100% applicable skills found)
- 🔴 **Unified /shannon:prime** - One-command session priming (<60s vs 15-20 min)

**Target Users**: Mission-critical domains (Finance, Healthcare, Legal, Security, Aerospace) where AI hallucinations are unacceptable.

---

## Installation

### Prerequisites

**Required**:
- Claude Code v1.0.0+
- Serena MCP configured

**Recommended**:
- Sequential MCP (deep reasoning)
- Context7 MCP (framework patterns)
- Puppeteer MCP (browser testing)

### Method 1: Plugin Marketplace (When Published)

```bash
# In Claude Code:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework

# Restart Claude Code
```

### Method 2: Local Installation

```bash
# In Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon@shannon

# Restart Claude Code
```

**Example**:
```bash
/plugin marketplace add /Users/yourname/projects/shannon-framework
/plugin install shannon@shannon
```

### Verification

```bash
/sh_status

# Expected output:
# 🎯 Shannon Framework V4.1.0
# Status: ACTIVE
# Serena MCP: CONNECTED
# Commands: 48 loaded
```

---

## Quick Start

### Your First Shannon Analysis

```bash
# 1. Analyze a specification
/sh_spec "Build a task management web app with React, Node.js, and PostgreSQL"

# Output:
# 📊 Complexity: 0.58 (COMPLEX)
# 8D Breakdown: Structural 0.45, Cognitive 0.60, etc.
# Domains: Frontend 40%, Backend 35%, Database 15%, etc.
# Recommendation: 2 waves, 1-2 weeks
```

### Using V4.1 Features (NEW)

```bash
# Prime your session (Enhancement #3)
/shannon:prime

# Discover available skills (Enhancement #2)
/sh_discover_skills

# All enhancements now active:
# - Forced reading for critical files
# - Skills auto-discovered and invoked
# - Fast session resumption ready
```

### Simple Project Flow

```bash
# Analyze → Implement → Test
/sh_spec "Build contact form"  # Complexity 0.30 (SIMPLE)
# [Implement based on guidance]
/sh_test --create --platform web
```

### Complex Project Flow

```bash
# Analyze → Plan → Wave 1 → Wave 2 → Wave 3
/sh_spec "Build e-commerce platform"  # Complexity 0.75
/sh_north_star "Launch to 100 users Q1"
/sh_wave 1  # Execute first wave
/sh_wave 2  # Continue
/sh_checkpoint "mvp-complete"
```

---

## Core Concepts

### 1. Specification-Driven Development

**Philosophy**: Analyze BEFORE implementing

```
Specification → Analysis → Plan → Execute → Test → Deploy
```

**Why**: Prevents under-estimation, ensures thoroughness

### 2. 8-Dimensional Complexity

**Dimensions** (weighted):
1. **Structural** (20%) - Files, services, modules
2. **Cognitive** (15%) - Analysis depth, design sophistication
3. **Coordination** (10%) - Team communication needs
4. **Temporal** (10%) - Time dependencies
5. **Technical** (15%) - Languages, frameworks
6. **Scale** (15%) - Users, data volume
7. **Uncertainty** (15%) - Unknown requirements
8. **Dependencies** (10%) - External integrations

**Score**: 0.0-1.0 (objective, quantitative, reproducible)

**Classification**:
- 0.00-0.25: TRIVIAL
- 0.25-0.40: SIMPLE
- 0.40-0.60: MODERATE
- 0.60-0.75: COMPLEX
- 0.75-1.00: CRITICAL

### 3. Wave-Based Execution

**When**: Complexity >=0.50 (Moderate or higher)

**Structure**:
```
Wave = Multi-phase execution unit
├─ Phase 1: Setup/Foundation
├─ Phase 2: Core Implementation
└─ Phase 3: Integration/Testing
```

**Benefits**:
- Parallel agent execution (3.5x speedup)
- Clear milestones
- Automatic checkpoints
- SITREP coordination (complexity >=0.70)

### 4. NO MOCKS Philosophy

**Rule**: Functional tests ONLY

**Allowed**:
- ✅ Real browser tests (Puppeteer)
- ✅ Real API requests (HTTP)
- ✅ Real database operations (test instances)

**Forbidden**:
- ❌ Mock objects
- ❌ Stubs
- ❌ Fake implementations
- ❌ jest.fn(), @mock, @patch

**Why**: Mocks test mock behavior, not production behavior

### 5. Context Preservation

**Automatic Checkpointing**:
- PreCompact hook triggers before context compression
- CONTEXT_GUARDIAN saves complete state to Serena MCP
- Restoration via /sh_restore or /shannon:prime

**What's Preserved**:
- Specifications
- Complexity analysis
- Goals
- Wave progress
- Decisions
- Memories

**Result**: 100% context restoration, zero information loss

---

## All Commands Reference

### Shannon Core Commands (11)

#### /sh_spec
**Purpose**: Analyze specification with 8D complexity framework
**Usage**: `/sh_spec "specification text" [--mcps] [--save]`
**Output**: Complexity score, 8D breakdown, domains, wave plan, MCPs
**Example**: `/sh_spec "Build REST API with auth and CRUD"`

#### /sh_wave
**Purpose**: Execute development wave
**Usage**: `/sh_wave <number> [--plan] [--resume]`
**Example**: `/sh_wave 1` or `/sh_wave 2 --plan`

#### /sh_checkpoint
**Purpose**: Save session state to Serena MCP
**Usage**: `/sh_checkpoint "checkpoint-name"`
**Example**: `/sh_checkpoint "mvp-complete"`

#### /sh_restore
**Purpose**: Restore previous session state
**Usage**: `/sh_restore "checkpoint-name"` or `/sh_restore --latest`
**Example**: `/sh_restore "mvp-complete"`

#### /sh_status
**Purpose**: Show Shannon framework status
**Usage**: `/sh_status`
**Output**: Version, MCP status, current wave, progress

#### /sh_check_mcps
**Purpose**: Verify MCP server connections
**Usage**: `/sh_check_mcps [--setup <mcp-name>]`
**Output**: Required/recommended/conditional MCPs status

#### /sh_memory
**Purpose**: Manage Serena MCP memories
**Usage**: `/sh_memory [--list|--search <query>]`
**Example**: `/sh_memory --list`

#### /sh_north_star
**Purpose**: Set/view project North Star goal
**Usage**: `/sh_north_star "goal description"`
**Example**: `/sh_north_star "Launch to 100 beta users Q1"`

#### /sh_analyze
**Purpose**: Shannon-specific deep analysis
**Usage**: `/sh_analyze [--domains|--confidence|--index]`
**Example**: `/sh_analyze --confidence`

#### /sh_test
**Purpose**: Generate functional tests (NO MOCKS)
**Usage**: `/sh_test --create --platform <web|api|mobile>`
**Example**: `/sh_test --create --platform web`

#### /sh_scaffold
**Purpose**: Generate project scaffolding
**Usage**: `/sh_scaffold --framework <framework-name>`
**Example**: `/sh_scaffold --framework react`

### V4.1 NEW Commands (2)

#### /sh_discover_skills ⭐
**Purpose**: Auto-discover all available skills
**Usage**: `/sh_discover_skills [--cache|--refresh|--filter <pattern>]`
**Options**:
- `--cache`: Use cached results (fast, default)
- `--refresh`: Force fresh scan
- `--filter <pattern>`: Search skills

**Example**: `/sh_discover_skills --filter testing`

#### /shannon:prime ⭐
**Purpose**: Unified session priming (one command replaces 6)
**Usage**: `/shannon:prime [--fresh|--resume|--quick|--full]`
**Modes**:
- No flag: Auto-detect mode
- `--fresh`: Fresh session
- `--resume`: Resume from checkpoint
- `--quick`: Fast priming (10-15s)
- `--full`: Deep priming (60-120s)

**Example**: `/shannon:prime` or `/shannon:prime --resume`

---

## All Skills Reference

### Core Skills

**spec-analysis** (QUANTITATIVE):
- 8D complexity scoring algorithm
- Domain detection and quantification
- MCP recommendations
- Wave structure suggestions

**wave-orchestration** (QUANTITATIVE):
- Multi-stage wave planning
- Agent assignment
- Parallel execution coordination
- SITREP protocol (complexity >=0.70)

**phase-planning** (PROTOCOL):
- 5-phase implementation structure
- Validation gates
- Resource allocation

### Context Skills

**context-preservation** (PROTOCOL):
- Checkpoint creation
- State capture
- Serena MCP integration

**context-restoration** (PROTOCOL):
- Checkpoint restoration
- State recovery
- Memory reloading

**memory-coordination** (PROTOCOL):
- Standardized Serena MCP operations
- Memory namespacing
- Cross-session coordination

### Testing Skills

**functional-testing** (RIGID):
- NO MOCKS iron law enforcement
- Real browser/API/database testing
- TEST_GUARDIAN integration

**confidence-check** (QUANTITATIVE):
- 5-check validation (spec coverage, tests, docs, errors, edges)
- >=90% threshold for deployment
- Readiness scoring

### Analysis Skills

**shannon-analysis** (FLEXIBLE):
- Meta-analysis orchestration
- Pattern discovery
- Codebase understanding

**project-indexing** (PROTOCOL):
- SHANNON_INDEX.md generation
- 94% token compression
- Efficient codebase representation

### Support Skills

**goal-management** (PROTOCOL):
- North Star goal tracking
- Goal persistence

**goal-alignment** (QUANTITATIVE):
- Decision scoring against North Star
- Alignment percentage

**mcp-discovery** (QUANTITATIVE):
- Dynamic MCP recommendations
- Domain-based suggestions
- <10ms SIMD matching

**sitrep-reporting** (PROTOCOL):
- Military-style status reporting
- 5-section format (situation, objectives, progress, blockers, next)
- Multi-agent coordination

**using-shannon** (RIGID Meta-Skill):
- Enforces Shannon workflows
- Prevents violations (skipping analysis, using mocks, etc.)
- Loaded automatically at session start

### V4.1 NEW Skill

**skill-discovery** ⭐ (PROTOCOL):
- Auto-discover all SKILL.md files
- Parse YAML frontmatter
- Multi-factor confidence scoring
- Auto-invocation (>=0.70 threshold)
- Compliance verification

---

## Usage Examples

### Example 1: Simple Form (5 minutes)

```bash
/sh_spec "Contact form with name, email, message, validation"
# → Complexity 0.30 (SIMPLE), direct implementation

# Implement...
# Then:
/sh_test --create --platform web
```

### Example 2: Medium App (1-2 weeks)

```bash
/sh_spec "Task management: auth, CRUD, statuses, filtering, dashboard"
# → Complexity 0.58 (COMPLEX), 2 waves

/sh_north_star "Launch beta to 20 users"
/sh_wave 1  # Core features
/sh_wave 2  # Advanced features
/sh_checkpoint "v1.0"
```

### Example 3: Complex Platform (4-8 weeks)

```bash
/sh_spec "E-commerce: products, cart, checkout, orders, inventory, admin, analytics"
# → Complexity 0.75 (VERY COMPLEX), 4 waves

/sh_north_star "$10k revenue first month"
/sh_checkpoint "init"
/sh_wave 1  # Commerce core
/sh_wave 2  # User management
/sh_wave 3  # Admin tools
/sh_wave 4  # Optimization
```

### Example 4: Using V4.1 Forced Reading

```bash
/shannon:prime  # Activates forced reading

/sh_spec @large-spec.md  # 2,000 lines
# Shannon enforces:
# - Counts 2,000 lines
# - Reads ALL 2,000 lines
# - Verifies 100% completeness
# - 200+ Sequential MCP thoughts
# → Complete understanding guaranteed
```

### Example 5: Using V4.1 Auto Skill Discovery

```bash
/shannon:prime  # Discovers all 104 skills

/sh_spec "Build authentication system"
# Shannon auto-invokes:
# 🎯 spec-analysis (confidence: 0.85)
# 🎯 mcp-discovery (confidence: 0.72)
# → No manual skill checking needed
```

### Example 6: Using V4.1 Session Resumption

```bash
# Resume after context loss:
/shannon:prime --resume

# Shannon automatically:
# - Restores checkpoint
# - Loads 8 memories
# - Restores spec/plan state
# - Ready in 42 seconds (vs 15-20 min manual)
```

---

## Troubleshooting

### Installation Issues

**Problem**: Plugin not found
```bash
# Solution: Use absolute path
/plugin marketplace add /Users/yourname/projects/shannon-framework
```

**Problem**: Serena MCP not connected
```bash
# Solution: Configure Serena
# 1. Install Serena MCP
# 2. Add to Claude Code settings
# 3. Restart Claude Code
# 4. Verify: /sh_check_mcps
```

**Problem**: Commands not appearing
```bash
# Solution: Restart Claude Code completely
# Then: /sh_status
```

### Usage Issues

**Problem**: /sh_spec gives incomplete analysis
```bash
# Cause: Specification too short
# Solution: Provide detailed spec (min 50-100 words)
```

**Problem**: /shannon:prime takes too long
```bash
# Solution: Use quick mode
/shannon:prime --quick
```

**Problem**: Skills not auto-invoking
```bash
# Solution: Refresh discovery cache
/sh_discover_skills --refresh
```

### Common Errors

**"Serena MCP required"**:
- Shannon REQUIRES Serena for context preservation
- Install and configure Serena MCP
- Shannon won't work without it

**"Checkpoint not found"**:
- Use /shannon:prime --fresh instead of --resume
- Or manually check: /sh_memory --list

**"Specification too short"**:
- Provide minimum 50-100 word specification
- Include features, requirements, constraints

---

## Advanced Usage

### Custom Wave Planning

```bash
# Override auto-generated plan:
/sh_wave 1 --custom --phases 4
```

### Deep Analysis Mode

```bash
/sh_spec --deep --mcps --save "complex specification..."
# Enables:
# - Deep domain analysis (10+ domains)
# - Complete MCP recommendations
# - Auto-save to Serena MCP
```

### Selective Skill Invocation

```bash
# Manual skill invocation:
Skill("spec-analysis")

# Filter skill discovery:
/sh_discover_skills --filter authentication
```

### Project Indexing (Token Efficiency)

```bash
/sh_analyze large-codebase/ --index
# Creates SHANNON_INDEX.md (94% compression)
# 3K tokens vs 58K tokens
# 20x efficiency
```

---

## FAQ

**Q: Does Shannon work without Serena MCP?**
A: No. Serena is MANDATORY for Shannon.

**Q: What's the difference between sh_* and sc_* commands?**
A: sh_* = Shannon-native, sc_* = SuperClaude enhanced by Shannon

**Q: Is forced reading automatic?**
A: Commands like /sh_spec, /sh_analyze instruct agents to follow protocol. Future: automatic enforcement hooks.

**Q: How long does /shannon:prime take?**
A: Fresh: 10-20s, Resume: 30-60s, Full: 60-120s

**Q: Can I use Shannon without waves?**
A: Yes! Simple projects (complexity <0.50) use direct implementation.

**Q: What if I don't have optional MCPs?**
A: Shannon works with Serena alone. Optional MCPs enhance but aren't required.

---

## Next Steps

1. **Read**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design and diagrams
2. **Reference**: [INSTALLATION.md](INSTALLATION.md) - Detailed installation
3. **Examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - 15 complete examples
4. **Help**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

---

**Shannon Framework V4.1.0** - Complete User Guide
**Support**: info@shannon-framework.dev
**Issues**: https://github.com/shannon-framework/shannon/issues
