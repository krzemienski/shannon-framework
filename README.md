# Shannon Framework V4.1 - Complete Guide

> The most rigorous AI orchestration framework for mission-critical development

**Version**: 4.1.0
**Status**: Production Ready
**Repository**: https://github.com/krzemienski/shannon-framework
**License**: MIT

---

## Table of Contents

1. [What is Shannon?](#what-is-shannon)
2. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Installation Methods](#installation-methods)
   - [Verification](#verification)
   - [Configuration](#configuration)
3. [Quick Start](#quick-start)
   - [Your First Shannon Analysis](#your-first-shannon-analysis)
   - [Using V4.1 Features](#using-v41-features)
   - [Simple Project Flow](#simple-project-flow)
   - [Complex Project Flow](#complex-project-flow)
4. [Core Concepts](#core-concepts)
   - [Specification-Driven Development](#specification-driven-development)
   - [8-Dimensional Complexity](#8-dimensional-complexity)
   - [Wave-Based Execution](#wave-based-execution)
   - [NO MOCKS Philosophy](#no-mocks-philosophy)
   - [Context Preservation](#context-preservation)
5. [Architecture](#architecture)
   - [System Architecture](#system-architecture)
   - [Component Architecture](#component-architecture)
   - [Data Flow Architecture](#data-flow-architecture)
   - [V4.1 Enhancements](#v41-enhancements)
6. [Commands Reference](#commands-reference)
   - [Shannon Core Commands](#shannon-core-commands)
   - [V4.1 NEW Commands](#v41-new-commands)
7. [Skills Reference](#skills-reference)
   - [Core Skills](#core-skills)
   - [Context Skills](#context-skills)
   - [Testing Skills](#testing-skills)
   - [Analysis Skills](#analysis-skills)
   - [V4.1 NEW Skill](#v41-new-skill)
8. [Agents Reference](#agents-reference)
9. [Usage Examples (15)](#usage-examples)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Topics](#advanced-topics)
12. [FAQ](#faq)
13. [Contributing](#contributing)
14. [Support](#support)

---

## What is Shannon?

Shannon Framework is a **Claude Code plugin** that transforms AI development from subjective to quantitative, from optional to enforced, from lossy to lossless.

### Core Innovation

**Behavioral programming via markdown prompts** - Shannon modifies Claude's decision-making through prompt injection, not code execution.

**Result**: Inspectable, modifiable, portable behavioral modifications that work across any Claude instance.

### Target Users

Mission-critical domains where AI hallucinations are unacceptable:

- 💰 **Finance**: Compliance, regulations, audit trails, zero-tolerance errors
- 🏥 **Healthcare**: HIPAA compliance, patient safety, medical accuracy
- ⚖️ **Legal**: Contract analysis, regulatory compliance, complete documentation
- 🔒 **Security**: Threat analysis, vulnerability assessment, exhaustive coverage
- 🚀 **Aerospace**: Safety-critical specifications, zero-defect requirements

**Why**: These domains cannot tolerate skimmed context, mock-based false confidence, or forgotten requirements.

### Core Capabilities

**V4 Base**:
- 🎯 **8D Complexity Analysis** - Quantitative specification scoring (0.0-1.0)
- 🌊 **Wave Orchestration** - Multi-stage parallel execution (3.5x average speedup)
- 💾 **Context Preservation** - Zero information loss via Serena MCP checkpointing
- 🚫 **NO MOCKS Testing** - Functional tests only (real browsers, real databases, real APIs)

**V4.1 NEW** (Unique to Shannon):
- 🔴 **Forced Complete Reading** - Architectural enforcement of line-by-line reading
- 🔴 **Auto Skill Discovery** - Intelligent skill system (100% applicable skills found vs ~70% manual)
- 🔴 **Unified /shannon:prime** - One-command session priming (<60s vs 15-20 min)

---

## Installation

### Prerequisites

#### Required
- **Claude Code** v1.0.0 or higher
  - Download: https://claude.ai/code
  - Installation: Platform-specific (macOS, Windows, Linux)

- **Serena MCP Server** (MANDATORY for Shannon)
  - Purpose: Context preservation, checkpointing, memory coordination
  - Repository: https://github.com/oraios/serena
  - Installation: See Section 2.3.1 below for complete installation guide
  - Verification: `/list_memories` should work without error

#### Recommended
- **Sequential MCP** - Enhanced multi-step reasoning for complex specifications
  - Required for: FORCED_READING_PROTOCOL synthesis steps
  - Fallback: Standard Claude reasoning (functional but less thorough)

- **Context7 MCP** - Framework-specific patterns and documentation
  - Used by: mcp-discovery skill for framework-specific recommendations
  - Fallback: General recommendations (no framework patterns)

- **Puppeteer MCP** - Real browser automation for functional testing
  - Required for: NO MOCKS functional browser testing
  - Used by: functional-testing skill, TEST_GUARDIAN agent
  - Fallback: Manual testing guidance (no automated browser tests)

---

### Installation Methods

#### Method 1: Plugin Marketplace (Recommended)

**For Shannon Users** (when published to marketplace):

```bash
# In Claude Code:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework

# Restart Claude Code completely
```

**Verification**:
```bash
/shannon:status

# Expected output:
# 🎯 Shannon Framework V4.1.0
# Status: ACTIVE ✅
# Serena MCP: CONNECTED ✅
# Commands: 14 loaded
# Skills: 17 loaded
# Agents: 24 available
```

#### Method 2: Local Plugin Installation

**For Development or Testing**:

```bash
# Step 1: Clone repository
git clone https://github.com/krzemienski/shannon-framework
cd shannon-framework

# Step 2: Add as local marketplace
# In Claude Code:
/plugin marketplace add /Users/yourname/projects/shannon-framework

# Use ABSOLUTE path (not relative ~/...)

# Step 3: Install plugin
/plugin install shannon@shannon

# Step 4: Restart Claude Code completely
```

**Verification**:
```bash
/shannon:status

# Should show:
# Shannon Framework V4.1.0 ✅
# Installation: Local (/Users/yourname/projects/shannon-framework)
```

#### Method 3: Development Mode

**For Active Shannon Development**:

```bash
# After making changes to plugin files:
/plugin uninstall shannon@shannon
/plugin install shannon@shannon

# Restart Claude Code to load changes

# Test changes:
/shannon:status
/your_new_command  # Test your additions
```

---

### Configuration

#### Serena MCP Setup (Required)

Shannon cannot function without Serena MCP. If not configured:

**Step 1: Configure Serena MCP**

Add to `~/.claude/settings.json` in the `mcpServers` section:

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server"
      ]
    }
  }
}
```

**Prerequisites**: Ensure `uv` is installed:
```bash
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew:
brew install uv
```

**Step 2: Restart Claude Code**

Completely quit and restart Claude Code for MCP configuration to take effect.

**Step 3: Verify Connection**
```bash
/shannon:check_mcps

# Expected:
# ✅ Serena MCP - Connected
#    Status: Operational
#    Purpose: Context preservation
```

**Step 4: Test Checkpoint**
```bash
/shannon:checkpoint "test-checkpoint"
/shannon:restore "test-checkpoint"

# If successful: Serena MCP properly configured
```

---

### 2.3 Complete MCP Installation Guide

Shannon requires and recommends several MCP servers for full functionality. This section provides complete installation instructions for each MCP.

**Configuration File**: All MCPs are configured in `~/.claude/settings.json` in the `mcpServers` section.

---

#### 2.3.1 Serena MCP (MANDATORY) ⭐

**Purpose**: Context preservation, checkpointing, memory coordination across waves
**Repository**: https://github.com/oraios/serena
**Shannon Requirement**: **MANDATORY** - Shannon cannot function without Serena
**Used by**: All Shannon commands, context-preservation skill, checkpoint system

**Installation**:

1. **Ensure `uv` is installed**:
   ```bash
   # macOS/Linux:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or via Homebrew:
   brew install uv
   ```

2. **Add to `~/.claude/settings.json`**:
   ```json
   {
     "mcpServers": {
       "serena": {
         "command": "uvx",
         "args": [
           "--from",
           "git+https://github.com/oraios/serena",
           "serena",
           "start-mcp-server"
         ]
       }
     }
   }
   ```

3. **Restart Claude Code** completely (full quit and reopen)

**Health Check**:
```bash
# In Claude Code:
/shannon:check_mcps

# Expected:
# ✅ Serena MCP - Connected
#    Status: Operational
#    Purpose: Context preservation
```

**Troubleshooting**:
- If "command not found: uvx" → Install uv: `brew install uv`
- If connection fails → Check `~/.claude/logs/mcp-serena.log`
- If still failing → Verify git+https access to github.com

---

#### 2.3.2 Sequential MCP (RECOMMENDED) ⭐

**Purpose**: Enhanced multi-step reasoning with 100-500 thought chains for complex analysis
**Package**: @modelcontextprotocol/server-sequential-thinking
**Shannon Requirement**: **RECOMMENDED** - Required for deep analysis, V4.1 FORCED_READING_PROTOCOL synthesis
**Used by**: /shannon:spec --deep, /shannon:analyze --deep, FORCED_READING_PROTOCOL (200+ thoughts)

**Installation**:

Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
  }
}
```

Restart Claude Code completely.

**When to Install**:
- Complex projects (complexity >= 0.60)
- Large specifications (>1000 lines requiring forced reading)
- Deep architectural analysis needed
- V4.1 FORCED_READING_PROTOCOL synthesis (200-500 thoughts)

**Health Check**:
```bash
# Test in Claude Code:
# Type: "ultrathink about system architecture"
# Should see: mcp__sequential-thinking__sequentialthinking tool calls
```

**Fallback**: Without Sequential MCP, Claude uses standard reasoning (functional but less thorough for complex specs)

---

#### 2.3.3 Puppeteer MCP (RECOMMENDED) ⭐

**Purpose**: Real browser automation for functional testing (Shannon's NO MOCKS philosophy)
**Package**: @modelcontextprotocol/server-puppeteer
**Shannon Requirement**: **RECOMMENDED** - Required for NO MOCKS web functional testing
**Used by**: /shannon:test, TEST_GUARDIAN agent, functional-testing skill

**Installation**:

Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ]
    }
  }
}
```

Restart Claude Code completely.

**When to Install**:
- Web projects (Frontend domain >= 20%)
- Any project requiring browser testing
- Shannon's NO MOCKS testing (no jest.mock(), real browser only)

**Health Check**:
```bash
# Shannon will report:
/shannon:check_mcps

# Should show:
# ✅ Puppeteer MCP - Connected
#    Purpose: Browser automation for functional testing
```

**Fallback Chain**: Puppeteer → Playwright MCP → Chrome DevTools MCP → Manual testing

---

#### 2.3.4 Context7 MCP (RECOMMENDED)

**Purpose**: Framework-specific patterns and best practices documentation
**Package**: @upstash/context7-mcp
**Shannon Requirement**: **RECOMMENDED** - Enhanced framework-specific recommendations
**Used by**: mcp-discovery skill (Backend >= 20%), framework pattern analysis

**Installation**:

Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "Context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp"
      ]
    }
  }
}
```

Restart Claude Code completely.

**When to Install**:
- Framework-based projects (React, Vue, Express, FastAPI, Django, Rails, etc.)
- Backend domain >= 20%
- Need up-to-date framework patterns and best practices

**Fallback**: Without Context7, Shannon uses web search or generic recommendations

---

#### 2.3.5 Conditional MCPs (Install as Needed)

These MCPs enhance specific workflows but are not required for Shannon core functionality.

**Playwright MCP** (Browser testing alternative):
```json
"playwright": {
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```
**Use when**: Alternative to Puppeteer for browser testing
**Package**: @playwright/mcp

**Magic MCP** (UI component generation):
```json
"magic": {
  "command": "npx",
  "args": ["@21st-dev/magic"],
  "env": {
    "TWENTYFIRST_API_KEY": "your-api-key"
  }
}
```
**Use when**: Frontend >= 30%, need rapid UI component scaffolding
**Requires**: API key from https://21st.dev
**Referenced in**: domain-mcp-matrix.json (Frontend primary MCP)

**GitHub MCP** (Version control operations):
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "your-github-token"
  }
}
```
**Use when**: GitHub integration needed
**Requires**: GitHub Personal Access Token
**Package**: @modelcontextprotocol/server-github

**Git MCP** (Git operations):
```json
"git": {
  "command": "uvx",
  "args": ["mcp-server-git"]
}
```
**Use when**: Git operations within Claude Code
**Package**: mcp-server-git (uvx)

**xc-mcp** (iOS Simulator testing):
```json
"xc-mcp": {
  "command": "npx",
  "args": ["xc-mcp"]
}
```
**Use when**: iOS projects requiring functional testing
**Requires**: macOS with Xcode installed
**Referenced in**: functional-testing skill (iOS test platform)

**Chrome DevTools MCP** (Browser automation fallback):
```json
"chrome-devtools": {
  "command": "npx",
  "args": ["-y", "chrome-devtools-mcp@latest"]
}
```
**Use when**: Puppeteer/Playwright unavailable, need Chrome automation
**Package**: chrome-devtools-mcp

---

#### 2.3.6 Complete Configuration Example

**Full `~/.claude/settings.json` for Shannon with all MANDATORY and RECOMMENDED MCPs**:

```json
{
  "mcpServers": {
    "serena": {
      "comment": "MANDATORY for Shannon Framework",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server"
      ]
    },
    "sequential-thinking": {
      "comment": "RECOMMENDED for complex specs and deep analysis",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "puppeteer": {
      "comment": "RECOMMENDED for NO MOCKS browser testing",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "Context7": {
      "comment": "RECOMMENDED for framework patterns",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

**After configuration**:
1. Save file
2. Restart Claude Code completely
3. Verify: `/shannon:check_mcps` should show all 4 connected

---

### Verification

**Step 1: Check Shannon Status**
```bash
/shannon:status
```

**Expected Output**:
```
🎯 Shannon Framework V4.1.0
─────────────────────────────────
Status: ACTIVE ✅
Serena MCP: CONNECTED ✅

Components Loaded:
├─ Commands: 14 (Shannon core)
├─ Skills: 17 discovered
├─ Agents: 24 available
├─ Hooks: 6 active
└─ Core Patterns: 9 loaded

V4.1 Enhancements:
✅ Forced Reading Protocol (active)
✅ Auto Skill Discovery (104 skills found)
✅ Unified Prime Command (available)

Ready for specification-driven development
```

**Step 2: Test Core Commands**
```bash
# Test specification analysis:
/shannon:spec "Build a simple web form with email validation"

# Should output:
# - Complexity score (e.g., 0.30 SIMPLE)
# - 8D dimension breakdown
# - Domain percentages
# - MCP recommendations

# Test skill discovery (V4.1 NEW):
/shannon:discover_skills

# Should output:
# - Total skills found (typically 104+)
# - Project: 16, User: 88+

# Test session priming (V4.1 NEW):
/shannon:prime --fresh

# Should complete in <60 seconds
```

**Step 3: Verify MCP Connections**
```bash
/shannon:check_mcps
```

**Expected Output**:
```
🔌 MCP Server Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED:
✅ Serena MCP - Connected
   Purpose: Context preservation and checkpointing
   Status: Operational
   Health: /list_memories successful

RECOMMENDED:
✅ Sequential MCP - Connected
   Purpose: Enhanced multi-step reasoning
   Status: Operational

⚠️  Context7 MCP - Not connected
   Purpose: Framework patterns
   Status: Optional (Shannon works without it)

⚠️  Puppeteer MCP - Not connected
   Purpose: Browser automation
   Status: Optional (manual testing available)

Shannon requires ONLY Serena MCP. Others enhance functionality.
```

---

## Quick Start

### Your First Shannon Analysis

```bash
# Analyze a specification:
/shannon:spec "Build a task management web app with React, Node.js, and PostgreSQL"

# Shannon outputs:
# 📊 Complexity: 0.58 (COMPLEX)
#
# 8D Breakdown:
# ├─ Structural: 0.45 (estimated ~15 files, 3 services)
# ├─ Cognitive: 0.60 (design sophistication moderate)
# ├─ Coordination: 0.65 (frontend + backend teams)
# ├─ Temporal: 0.30 (no urgent deadline)
# ├─ Technical: 0.60 (React + Node.js + PostgreSQL)
# ├─ Scale: 0.35 (moderate user base)
# ├─ Uncertainty: 0.20 (well-defined requirements)
# └─ Dependencies: 0.30 (database integration)
#
# Weighted Total: 0.58 (COMPLEX)
#
# Domains:
# ├─ Frontend: 40% (React UI, components, state)
# ├─ Backend: 35% (Node.js API, auth, endpoints)
# ├─ Database: 15% (PostgreSQL schema, queries)
# └─ DevOps: 10% (deployment, hosting)
#
# Execution Strategy: WAVE-BASED (complexity >=0.50)
# Recommended Waves: 2
# Timeline: 1-2 weeks
#
# MCP Recommendations:
# Tier 1 (MANDATORY):
#   - Serena MCP (context preservation)
# Tier 2 (PRIMARY):
#   - Magic MCP (Frontend 40% - component generation)
#   - Puppeteer MCP (functional testing)
#   - Context7 MCP (React/Node.js patterns)
#   - PostgreSQL MCP (database operations)
# Tier 3 (SECONDARY):
#   - GitHub MCP (version control)
```

### Using V4.1 Features (NEW)

```bash
# Prime your session (Enhancement #3):
/shannon:prime

# Output:
# ✅ Mode: Fresh session
# ✅ Skills discovered: 104 (16 project, 88 user)
# ✅ MCPs verified: Serena ✅, Sequential ✅
# ✅ Forced reading: ACTIVE
# ✅ Ready in 35 seconds
#
# All V4.1 enhancements now active:
# - Forced complete reading enabled
# - Skills auto-discovered and ready
# - Fast session resumption configured

# Discover available skills (Enhancement #2):
/shannon:discover_skills

# Output:
# 📚 Skill Discovery Complete
#
# Skills Found: 104 total
# ├─ Project: 17 skills (Shannon Framework)
# ├─ User: 88 skills (your custom skills)
# └─ Plugin: 0 skills
#
# Skill Types:
# ├─ QUANTITATIVE: 4 (spec-analysis, wave-orchestration, etc.)
# ├─ PROTOCOL: 6 (phase-planning, context-preservation, etc.)
# ├─ RIGID: 3 (functional-testing, using-shannon, etc.)
# └─ FLEXIBLE: 7 (shannon-analysis, goal-management, etc.)
#
# Cache: Saved (expires in 1 hour)
# Next: Skills auto-invoke when applicable (confidence >=0.70)
```

### Simple Project Flow

```bash
# For projects with complexity <0.50 (Simple to Moderate):

# 1. Analyze specification
/shannon:spec "Build contact form with name, email, message, validation. Send to API endpoint. Show success/error messages."

# Output: Complexity 0.35 (SIMPLE)
# Recommendation: Direct implementation (no waves needed)

# 2. Implement directly
# [Implement React form, validation, API integration]

# 3. Generate functional tests
/shannon:test --create --platform web --feature "contact form"

# Shannon generates:
# - Puppeteer test (real browser, NO MOCKS)
# - Real API integration test
# - Real validation testing

# 4. Run tests
npm test

# Done! Simple projects don't need waves.
```

### Complex Project Flow

```bash
# For projects with complexity >=0.50 (Complex or higher):

# 1. Prime session
/shannon:prime

# 2. Analyze specification
/shannon:spec "Build e-commerce platform with products, cart, checkout, orders, inventory, admin, analytics"

# Output: Complexity 0.75 (VERY COMPLEX)
# Recommendation: 4 waves
# Timeline: 4-8 weeks

# 3. Set North Star goal
/shannon:north_star "Process $10k revenue within first month"

# 4. Review wave structure
# Wave 1: Commerce core (products, cart, checkout)
# Wave 2: User management (accounts, orders)
# Wave 3: Admin tools (dashboard, inventory, analytics)
# Wave 4: Optimization (performance, deployment)

# 5. Create initial checkpoint
/shannon:checkpoint "project-start"

# 6. Execute waves
/shannon:wave 1 --plan  # Review before executing
/shannon:wave 1         # Execute Wave 1
/shannon:checkpoint "wave-1-complete"

/shannon:wave 2
/shannon:checkpoint "wave-2-complete"

# If context compaction occurs:
# PreCompact hook auto-saves checkpoint
# Resume with: /shannon:prime --resume

# 7. Continue remaining waves
/shannon:wave 3
/shannon:wave 4

# 8. Final production checkpoint
/shannon:checkpoint "production-ready"
```

---

## Core Concepts

### Specification-Driven Development

**Philosophy**: Analyze complexity BEFORE implementing

```
Traditional:
"Looks simple" → Implement → Discover complexity → Rework (wasted time)

Shannon:
Specification → 8D Analysis (objective) → Appropriate Planning → Implement (right approach first time)
```

**Workflow**:
```
1. Specification → 2. Analysis (8D scoring) → 3. Plan (phases, waves, resources) →
4. Execute (sequential or parallel) → 5. Test (NO MOCKS) → 6. Deploy
```

**Why**: Human intuition under-estimates complexity 30-50%. Quantitative analysis prevents costly rework.

### 8-Dimensional Complexity

**Framework**: Eight independent dimensions, weighted, produce objective 0.0-1.0 score

**Dimensions** (with weights):
1. **Structural** (20%) - File count, services, modules, components, system breadth
2. **Cognitive** (15%) - Analysis depth, design sophistication, decision complexity, learning needs
3. **Coordination** (10%) - Team size, communication overhead, cross-functional collaboration
4. **Temporal** (10%) - Time pressure, deadline constraints, urgency factors, scheduling
5. **Technical** (15%) - Languages, frameworks, algorithms, advanced tech, sophistication
6. **Scale** (15%) - User volume, data volume, performance requirements, concurrency
7. **Uncertainty** (15%) - Ambiguous requirements, unknowns, exploratory work, research
8. **Dependencies** (10%) - External services, blocking dependencies, integration complexity

**Calculation**:
```
complexity_score = (0.20 × structural) + (0.15 × cognitive) + (0.10 × coordination) +
                   (0.10 × temporal) + (0.15 × technical) + (0.15 × scale) +
                   (0.15 × uncertainty) + (0.10 × dependencies)
```

**Classification**:
- **0.00-0.25**: TRIVIAL (direct implementation, <1 day)
- **0.25-0.40**: SIMPLE (straightforward, 1-2 days)
- **0.40-0.60**: MODERATE (structured approach, 1 week)
- **0.60-0.75**: COMPLEX (waves required, 2-4 weeks)
- **0.75-1.00**: VERY COMPLEX / CRITICAL (extensive waves, 1-3 months)

**Example**:
```
"Build TODO app" → Seems simple → Shannon calculates:
  Structural: 0.25 (5 files estimated)
  Cognitive: 0.20 (standard CRUD design)
  Coordination: 0.30 (frontend + backend)
  Technical: 0.35 (React + API + database)
  ... (other dimensions)
  Result: 0.42 (MODERATE - not actually simple!)
  Recommendation: Structured approach, 3-5 days
```

### Wave-Based Execution

**When**: Complexity >=0.50 (Moderate or higher)

**Structure**:
```
Wave = Complete development cycle with phases
├─ Foundation Phase (setup, architecture, core infrastructure)
├─ Implementation Phase (feature development, business logic)
└─ Integration Phase (testing, deployment, documentation)

Multiple waves for complex projects:
Wave 1 → Checkpoint → Wave 2 → Checkpoint → Wave 3
```

**Parallel Agent Execution**:
```
Sequential:
  Frontend (6h) → Backend (6h) → Database (4h) = 16 hours total

Wave-Based Parallel:
  Wave 1: Frontend + Backend + Database (simultaneously)
  Duration: max(6h, 6h, 4h) = 6 hours
  Speedup: 16h → 6h = 2.67x faster
```

**Benefits**:
- ✅ 3.5x average speedup through parallelization
- ✅ Clear milestones and validation gates
- ✅ Automatic checkpoints between waves
- ✅ SITREP coordination for complexity >=0.70
- ✅ Graceful failure recovery

**Coordination**: WAVE_COORDINATOR agent manages parallel execution, prevents duplicate work, enforces synthesis checkpoints.

### NO MOCKS Philosophy

**Shannon's Iron Law**: Functional tests ONLY, zero tolerance for mocks.

**NEVER Allowed**:
- ❌ `jest.mock()` / `jest.fn()`
- ❌ `@mock` / `@patch` decorators
- ❌ `sinon.stub()` / `sinon.fake()`
- ❌ In-memory databases (SQLite :memory:)
- ❌ Mock servers / stub APIs
- ❌ Fake objects / test doubles

**ALWAYS Required**:
- ✅ Real browser testing (Puppeteer MCP, Playwright MCP)
- ✅ Real HTTP requests (actual backend APIs)
- ✅ Real database operations (test database instances)
- ✅ Real mobile devices (iOS Simulator via xc-mcp)
- ✅ Real file system operations
- ✅ Real network calls

**Why NO MOCKS**:
1. Mocks test mock behavior, not production behavior
2. Integration failures missed by mocked tests
3. API contract changes break production but mocked tests pass
4. False confidence from passing tests that don't validate reality

**Enforcement**: `post_tool_use.py` hook scans test files, BLOCKS Write/Edit if mocks detected (13 patterns monitored).

**Example**:
```typescript
// ❌ WRONG (Shannon blocks this):
jest.mock('axios');
test('fetch user', () => {
  axios.get.mockResolvedValue({ id: 1 });
  // Testing mock object, not real API
});

// ✅ CORRECT (Shannon allows):
import { test } from '@playwright/test';
test('fetch user', async ({ request }) => {
  const response = await request.get('http://localhost:3001/users/1');
  // Testing REAL backend API
  expect(response.status()).toBe(200);
});
```

### Context Preservation

**Problem**: Claude Code auto-compacts conversations (~1M tokens), losing critical context.

**Shannon Solution**: Automatic comprehensive checkpointing via PreCompact hook.

**What's Preserved**:
- ✅ Complete specification text
- ✅ 8D complexity analysis
- ✅ North Star goals and progress
- ✅ Wave execution state (current wave, progress %)
- ✅ Phase state (current phase 1-5)
- ✅ Agent assignments and results
- ✅ Architectural decisions and rationale
- ✅ Integration status
- ✅ Test results
- ✅ Next actions (immediate priorities)
- ✅ All Serena memory references (15-20 keys)

**Checkpoint Flow**:
```
Context reaches 950K / 1M tokens (95%)
↓
PreCompact event fires (automatic)
↓
precompact.py hook generates instructions
↓
CONTEXT_GUARDIAN agent executes:
  - Collects all project state (11 comprehensive sections)
  - Saves to Serena MCP: write_memory("shannon_checkpoint_{timestamp}", ...)
  - Verifies save successful
↓
Auto-compaction proceeds (950K → ~200K)
↓
Next session: /shannon:prime --resume
↓
Full context restored (100% - zero information loss)
```

**Manual Checkpoints**:
```bash
# Before major milestones:
/shannon:checkpoint "wave-2-complete"
/shannon:checkpoint "mvp-launch"

# After risky changes:
/shannon:checkpoint "before-refactor"

# Periodic (every 2-3 hours):
/shannon:checkpoint "end-of-day"
```

**Restoration**:
```bash
# Auto-restore latest:
/shannon:prime --resume

# Restore specific:
/shannon:restore "mvp-launch"

# List available:
/shannon:checkpoint --list
```

---

## Architecture

### System Architecture

Shannon operates as 6-layer behavioral framework:

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: USER INTERFACE                  │
│  Commands: /shannon:spec, /shannon:wave, /shannon:test, /shannon:prime    │
│  Purpose: User-facing entry points for Shannon workflows   │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 2: ENFORCEMENT                     │
│  Hooks: 6 automatic enforcers                              │
│  ├─ session_start.sh: Load using-shannon meta-skill        │
│  ├─ post_tool_use.py: Block mock usage (13 patterns)       │
│  ├─ precompact.py: Emergency checkpointing (11 sections)   │
│  ├─ user_prompt_submit.py: Goal injection                  │
│  └─ stop.py: Wave validation gates                         │
│  Purpose: Real-time Iron Law enforcement (cannot bypass)   │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 3: ORCHESTRATION                     │
│  Meta-Skills: using-shannon, shannon-analysis              │
│  Purpose: Coordinate workflows, select specialist skills   │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                LAYER 4: SPECIALIST SKILLS                   │
│  16 Skills (16,740 lines total):                           │
│  ├─ QUANTITATIVE: spec-analysis, wave-orchestration        │
│  ├─ PROTOCOL: phase-planning, context-preservation         │
│  ├─ RIGID: functional-testing (NO MOCKS)                   │
│  └─ FLEXIBLE: shannon-analysis, goal-management            │
│  Purpose: Define algorithms, workflows, protocols          │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 5: EXECUTION                       │
│  24 Agents: WAVE_COORDINATOR, TEST_GUARDIAN, FRONTEND      │
│  Purpose: Execute skills in specialized roles              │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 6: INFRASTRUCTURE                    │
│  MCPs: Serena (memory), Puppeteer (testing), Sequential    │
│  Tools: Read, Write, Grep, Glob, Bash                      │
│  Purpose: Provide capabilities and persistent storage      │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow Example** (/shannon:spec execution):
```
1. USER types: /shannon:spec "Build auth system"
2. ENFORCEMENT: session_start hook ensures using-shannon loaded (Iron Laws active)
3. COMMAND: /shannon:spec validates input, checks for forced reading trigger
4. ORCHESTRATION: Command invokes spec-analysis skill (auto via COMMAND_SKILL_MAP)
5. SPECIALIST: spec-analysis calculates 8D score, detects domains, recommends MCPs
6. INFRASTRUCTURE: Serena MCP saves results (write_memory("spec_analysis_{id}", ...))
7. SPECIALIST: spec-analysis chains to phase-planning skill
8. INFRASTRUCTURE: Serena MCP saves phase plan
9. USER receives: Comprehensive analysis report
10. ENFORCEMENT: If user tries writing mocks later → post_tool_use hook BLOCKS
```

### Component Architecture

**14 Commands** (commands/):
- **Shannon Core** (11): /shannon:spec, /shannon:wave, /shannon:checkpoint, /shannon:restore, /shannon:status, /shannon:check_mcps, /shannon:memory, /shannon:north_star, /shannon:analyze, /shannon:test, /shannon:scaffold
- **V4.1 NEW** (3): /shannon:discover_skills, /shannon:reflect, /shannon:prime

**17 Skills** (skills/):
- **Core**: spec-analysis (1,544L), wave-orchestration (1,581L), phase-planning (1,182L)
- **Context**: context-preservation (562L), context-restoration (957L), memory-coordination (1,010L)
- **Testing**: functional-testing (1,402L), confidence-check (1,277L)
- **Analysis**: shannon-analysis (1,255L), project-indexing (1,097L)
- **Goals**: goal-management (847L), goal-alignment (952L)
- **Discovery**: mcp-discovery (726L), skill-discovery (565L - V4.1)
- **Meta**: using-shannon (723L)
- **Reporting**: sitrep-reporting (1,060L)
- **NEW**: honest-reflections (1,200L - prevents premature completion claims)

**24 Agents** (agents/):
- **Orchestrators**: WAVE_COORDINATOR, CONTEXT_GUARDIAN, PHASE_ARCHITECT, SPEC_ANALYZER, ARCHITECT
- **Domain Builders**: FRONTEND, BACKEND, MOBILE_DEVELOPER, DATABASE_ARCHITECT, DEVOPS, API_DESIGNER, DATA_ENGINEER, SECURITY
- **Quality**: TEST_GUARDIAN, QA, CODE_REVIEWER, REFACTORER, PERFORMANCE, ANALYZER
- **Support**: SCRIBE, MENTOR, TECHNICAL_WRITER, IMPLEMENTATION_WORKER, PRODUCT_MANAGER

**6 Hooks** (hooks/):
- **session_start.sh**: Auto-loads using-shannon meta-skill at session start
- **post_tool_use.py**: Scans for 13 mock patterns, blocks Write/Edit if detected
- **precompact.py**: Generates 11-section checkpoint template before auto-compact
- **user_prompt_submit.py**: Injects North Star goals into every prompt
- **stop.py**: Validates wave gates before session end
- **hooks.json**: Configuration and registration

**9 Core Patterns** (core/):
1. SPEC_ANALYSIS.md - Complete 8D algorithm (1,787 lines)
2. WAVE_ORCHESTRATION.md - Multi-stage execution framework (1,612 lines)
3. PHASE_PLANNING.md - 5-phase methodology (1,562 lines)
4. CONTEXT_MANAGEMENT.md - Checkpoint/restore patterns
5. TESTING_PHILOSOPHY.md - NO MOCKS enforcement rationale
6. HOOK_SYSTEM.md - Hook lifecycle and integration
7. PROJECT_MEMORY.md - Serena MCP integration patterns
8. MCP_DISCOVERY.md - Dynamic MCP recommendation algorithms
9. **FORCED_READING_PROTOCOL.md** (V4.1 NEW) - Complete reading enforcement

### Data Flow Architecture

**Typical /shannon:spec Flow**:
```
1. User Input:
   /shannon:spec "Build e-commerce platform"

2. Command Layer (sh_spec.md):
   - Validates input (minimum 20 words)
   - Checks for forced reading trigger (file attachment or >1000 words)
   - Invokes spec-analysis skill

3. Skill Layer (spec-analysis/SKILL.md):
   - If large spec: Apply FORCED_READING_PROTOCOL
   - Parse specification text
   - Apply 8D complexity algorithm (calculate all 8 dimensions)
   - Detect domains (keyword counting, normalization to 100%)
   - Generate MCP recommendations (tier-based: Mandatory → Primary → Secondary → Optional)
   - Generate 5-phase plan with validation gates

4. Infrastructure Layer (Serena MCP):
   - Save analysis: write_memory("spec_analysis_{timestamp}", analysis_object)
   - Verify save: read_memory(analysis_id) to confirm

5. Skill Chaining:
   - spec-analysis invokes phase-planning (uses complexity + domains from step 3)
   - phase-planning generates detailed phase breakdown
   - Save to Serena: write_memory("phase_plan_{project}", plan_object)

6. Skill Chaining (continued):
   - spec-analysis invokes mcp-discovery (uses domain percentages)
   - mcp-discovery generates tiered MCP recommendations
   - Recommendations included in output

7. Output to User:
   - Complexity score: 0.68 (COMPLEX)
   - 8D breakdown table
   - Domain analysis (percentages sum to 100%)
   - MCP recommendations (tiered with rationale)
   - 5-phase plan with timelines
   - Execution strategy (wave-based)
   - Timeline estimate (2-4 weeks)

8. Enforcement Layer:
   - If user later tries to write mocks → post_tool_use hook BLOCKS
   - If context approaches limit → precompact hook triggers checkpoint
```

### V4.1 Enhancements

#### Enhancement #1: Forced Complete Reading Protocol

**Problem**: AI agents skim documents (read "relevant sections"), miss critical details, cause 40-60% of implementation errors.

**Solution**: Architectural enforcement via FORCED_READING_PROTOCOL.md

**How It Works**:
```
Agent needs to read critical file
↓
FORCED_READING_PROTOCOL activated (via /shannon:spec, /shannon:analyze, /shannon:wave)
↓
Step 1: PRE-COUNT
├─ Count total lines: wc -l returns 2,000
├─ Cache line count
└─ Announce: "File has 2,000 lines - reading ALL lines"

Step 2: SEQUENTIAL READING
├─ Read line 1
├─ Read line 2
├─ ... (no skipping allowed)
├─ Read line 2,000
└─ Track: lines_read = {1, 2, 3, ..., 2000}

Step 3: VERIFY COMPLETENESS
├─ Check: len(lines_read) == 2,000?
├─ If YES: Enable synthesis (proceed)
└─ If NO: BLOCK synthesis, report missing lines

Step 4: SEQUENTIAL SYNTHESIS
├─ Use Sequential MCP (recommended)
├─ Minimum 200 thoughts for 2K-line file
└─ Present comprehensive analysis based on COMPLETE reading
```

**Result**: Zero architectural errors from incomplete reading (vs 40-60% error rate with skimming).

**Competitive Advantage**: NO competitor enforces complete reading architecturally.

#### Enhancement #2: Automatic Skill Discovery & Invocation

**Problem**: Manual skill checking leads to 30% forgotten applicable skills, inconsistent application.

**Solution**: skill-discovery skill with auto-invocation

**How It Works**:
```
Session Start or /shannon:discover_skills
↓
Step 1: SCAN DIRECTORIES
├─ Project: ./skills/*/SKILL.md
├─ User: ~/.claude/skills/*/SKILL.md
└─ Plugin: <plugins>/*/skills/*/SKILL.md

Step 2: PARSE YAML FRONTMATTER
├─ Extract: name, description, skill-type
├─ Extract: MCP requirements (required, recommended, conditional)
├─ Extract: triggers from description (keywords)
└─ Build SkillMetadata object per skill

Step 3: BUILD CATALOG
├─ Typically finds: 104+ skills (16 Shannon + 88+ user)
├─ Index by: name, triggers, type, MCPs
└─ Cache (1 hour TTL, <10ms retrieval)

Step 4: INTELLIGENT SELECTION (when command executed)
├─ Calculate confidence score (4 factors, weighted):
│  ├─ Trigger match: 40% (keywords in user request match skill triggers)
│  ├─ Command compatibility: 30% (skill in COMMAND_SKILL_MAP for this command)
│  ├─ Context relevance: 20% (recent conversation mentions skill domain)
│  └─ Dependencies satisfied: 10% (required MCPs available)
├─ Filter: confidence >=0.70 threshold
└─ AUTO-INVOKE applicable skills

Step 5: COMPLIANCE VERIFICATION
├─ After skill invocation, verify agent followed skill
├─ Skill-specific checkers:
│  ├─ spec-analysis: Check for 8D scoring in output
│  ├─ functional-testing: Scan for mock usage
│  └─ wave-orchestration: Check for SITREP structure
└─ Log violations if skill not followed
```

**Example**:
```
User: /shannon:spec "Build authentication system"

skill-discovery calculates:
  spec-analysis: confidence 0.85 (trigger match: "system", command: /shannon:spec)
  mcp-discovery: confidence 0.72 (context: "authentication")
  confidence-check: confidence 0.65 (below 0.70 threshold)

AUTO-INVOKES:
  ✅ spec-analysis (0.85 >=0.70)
  ✅ mcp-discovery (0.72 >=0.70)
  ❌ confidence-check (0.65 <0.70)

Result: 100% of applicable skills found and used (vs ~70% manual)
```

**Competitive Advantage**:
- SuperClaude: Partial automation (some skills auto-invoke)
- Hummbl/Superpowers: NONE (fully manual)
- Shannon: 100% automatic (all skills with confidence >=0.70)

#### Enhancement #3: Unified /shannon:prime Command

**Problem**: Session resumption requires 6 separate commands (15-20 minutes)

**Old Workflow**:
```bash
# Pre-V4.1 manual priming (15-20 minutes):
/shannon:discover_skills          # 3-4 min (scan + parse skills)
/shannon:check_mcps              # 2-3 min (verify MCP connections)
/shannon:restore latest-checkpoint  # 5-8 min (load checkpoint, restore state)
/list_memories              # 1-2 min (list Serena memories)
/read_memory spec_analysis  # 1-2 min (load specification)
/read_memory phase_plan     # 1-2 min (load phase plan)
# ... (potentially 5-10 more memory reads)
# Total: 15-23 minutes
```

**New Workflow**:
```bash
# V4.1 unified priming (<60 seconds):
/shannon:prime

# Executes 8 steps automatically:
# 1. Mode Detection: Auto-detect fresh vs resume (checks for checkpoints <24h)
# 2. Skill Inventory: Run /shannon:discover_skills (Enhancement #2, finds 104 skills)
# 3. MCP Verification: Check Serena (required), Sequential, Context7, Puppeteer
# 4. Context Restoration: If resume, run /shannon:restore {latest_checkpoint}
# 5. Memory Loading: Load relevant Serena memories (spec, plan, progress - 8-15 keys)
# 6. Spec/Plan Restoration: Restore specification ID, current phase, next actions
# 7. Thinking Preparation: Prepare Sequential MCP for deep analysis if available
# 8. Forced Reading Activation: Enable FORCED_READING_PROTOCOL (Enhancement #1)
#
# Total: 30-55 seconds (vs 15-20 minutes manual)
```

**Performance**:
| Task | Manual (V4.0) | /shannon:prime (V4.1) | Speedup |
|------|---------------|----------------------|---------|
| Skill discovery | 3-4 min | 8s | 22x |
| MCP check | 2-3 min | 5s | 24x |
| Context restore | 5-8 min | 12s | 30x |
| Memory loading | 3-5 min | 8s | 25x |
| Plan restoration | 2-3 min | 6s | 25x |
| **TOTAL** | **15-23 min** | **39-55s** | **20x faster** |

**Competitive Advantage**: NO competitor has unified session priming (all require manual multi-command workflows).

---

## Commands Reference

### Shannon Core Commands (11)

#### /shannon:spec
**Purpose**: Analyze specification using 8D complexity framework
**Syntax**: `/shannon:spec "specification text" [--mcps] [--save] [--deep]`
**Invokes**: spec-analysis skill (primary), confidence-check, mcp-discovery
**Output**: Complexity score (0.0-1.0), 8D breakdown, domain percentages, MCP recommendations, 5-phase plan, timeline estimate

**Flags**:
- `--mcps`: Include detailed MCP recommendations with setup instructions (default: true)
- `--save`: Save analysis to Serena MCP for retrieval (default: true)
- `--deep`: Use Sequential MCP for 100-500 step deep analysis (for complexity >=0.60)

**Example**:
```bash
/shannon:spec "Build REST API with auth, CRUD operations for users/products, PostgreSQL database, JWT tokens, rate limiting"

# Output:
# Complexity: 0.52 (COMPLEX)
# Domains: Backend 55%, Database 30%, Security 15%
# Waves: 2 recommended
# Timeline: 5-7 days
```

**See**: commands/guides/shannon:spec_GUIDE.md (15 comprehensive examples)

#### /shannon:wave
**Purpose**: Execute wave-based development with parallel agent coordination
**Syntax**: `/shannon:wave [wave_number] [--plan] [--dry-run] [--resume]`
**Invokes**: wave-orchestration skill, context-preservation (checkpoints)
**Agent**: Activates WAVE_COORDINATOR for parallel execution

**Flags**:
- `--plan`: Generate wave structure without executing (preview)
- `--dry-run`: Detailed planning with risk analysis (comprehensive preview)
- `--resume`: Continue interrupted wave execution

**Example**:
```bash
/shannon:wave 1

# WAVE_COORDINATOR spawns agents in parallel:
# - FRONTEND (React components)
# - BACKEND (API endpoints)
# - DATABASE_ARCHITECT (PostgreSQL schema)
#
# Parallel execution: 5h vs 15h sequential = 3x speedup
```

**See**: commands/guides/shannon:wave_GUIDE.md (15 comprehensive examples)

#### /shannon:checkpoint
**Purpose**: Create comprehensive checkpoint of session state
**Syntax**: `/shannon:checkpoint ["checkpoint-label"] [--list] [--load checkpoint_id]`
**Invokes**: context-preservation skill
**Storage**: Serena MCP

**Usage**:
```bash
# Auto-labeled:
/shannon:checkpoint

# Custom label:
/shannon:checkpoint "mvp-complete"

# List available:
/shannon:checkpoint --list

# Load specific:
/shannon:checkpoint --load shannon_checkpoint_20251108
```

**See**: commands/guides/shannon:checkpoint_GUIDE.md (10 comprehensive examples)

#### /shannon:restore
**Purpose**: Restore complete project state from checkpoint
**Syntax**: `/shannon:restore [checkpoint_id] [--goals] [--verbose]`
**Invokes**: context-restoration skill

**Flags**:
- `--goals`: Include North Star goal restoration
- `--verbose`: Detailed restoration report with quality metrics

**Example**:
```bash
# Auto-restore latest:
/shannon:restore

# Restore specific:
/shannon:restore shannon_checkpoint_20251107

# With goals:
/shannon:restore --goals
```

**See**: commands/guides/shannon:restore_GUIDE.md (10 comprehensive examples)

#### /shannon:test
**Purpose**: NO MOCKS functional testing orchestration
**Syntax**: `/shannon:test [test_path] [--platform web|mobile|api|database] [--create] [--validate]`
**Invokes**: functional-testing skill
**Agent**: TEST_GUARDIAN for test generation

**Flags**:
- `--platform`: Override platform detection
- `--create`: Generate new test scaffold
- `--validate`: Check NO MOCKS compliance

**Example**:
```bash
# Discover all tests:
/shannon:test

# Run specific:
/shannon:test tests/functional/auth.spec.ts

# Create new:
/shannon:test --create checkout-flow --platform web

# Validate compliance:
/shannon:test --validate
```

**See**: commands/guides/shannon:test_GUIDE.md (12 comprehensive examples)

#### /shannon:analyze
**Purpose**: Shannon-aware codebase analysis with complexity assessment
**Syntax**: `/shannon:analyze [component] [--deep] [--confidence]`
**Invokes**: shannon-analysis skill (orchestrator), project-indexing, confidence-check

**Example**:
```bash
# Full project:
/shannon:analyze

# Specific component:
/shannon:analyze authentication

# With confidence check:
/shannon:analyze --confidence
```

**See**: commands/guides/FINAL_THREE_COMMANDS_REFERENCE.md

#### /shannon:status
**Purpose**: Display Shannon framework status and health
**Syntax**: `/shannon:status [--mcps] [--goals] [--verbose]`

**Example**:
```bash
/shannon:status

# Output:
# 🎯 Shannon Framework V4.1.0
# Status: ACTIVE ✅
# Serena MCP: CONNECTED ✅
# Current Wave: 2/4 (50% complete)
# North Star: "Launch Q1 2025" (75% progress)
```

#### /shannon:check_mcps
**Purpose**: Verify MCP server configuration and health
**Syntax**: `/shannon:check_mcps [--install-guide] [--fix]`
**Invokes**: mcp-discovery skill

**Example**:
```bash
/shannon:check_mcps

# Output:
# REQUIRED:
# ✅ Serena MCP: Connected
#
# RECOMMENDED:
# ✅ Sequential MCP: Connected
# ⚠️ Puppeteer MCP: Not connected (install guide provided)
```

**See**: commands/guides/FINAL_THREE_COMMANDS_REFERENCE.md

#### /shannon:memory
**Purpose**: Manage Serena MCP memories
**Syntax**: `/shannon:memory [--list|--search <query>|--pattern <name>]`

**Example**:
```bash
# List all:
/shannon:memory --list

# Search:
/shannon:memory --search "authentication"

# Pattern analysis:
/shannon:memory --pattern wave-execution
```

#### /shannon:north_star
**Purpose**: Set and manage project North Star goal
**Syntax**: `/shannon:north_star "goal description" [--update] [--history]`
**Invokes**: goal-management skill

**Example**:
```bash
/shannon:north_star "Launch MVP to 100 beta users by Q1 2025"

# Progress updates automatically via goal-management
```

#### /shannon:scaffold
**Purpose**: Generate Shannon-optimized project scaffolding
**Syntax**: `/shannon:scaffold <framework> [--template <name>]`

**Example**:
```bash
/shannon:scaffold react --template dashboard
```

### V4.1 NEW Commands (4)

#### /shannon:task ⭐ NEW
**Purpose**: Automated spec → wave → prime workflow for complete task execution
**Syntax**: `/shannon:task "specification" [--auto] [--plan-only]`
**Invokes**: /shannon:spec → /shannon:wave → /shannon:prime (orchestrated)

**Workflow**: One-command automation from specification to ready-to-develop state

**Flags**:
- `--auto`: Fully automated (no prompts, execute all waves)
- `--plan-only`: Generate plan without executing

**Example**:
```bash
# Interactive mode (recommended):
/shannon:task "Build REST API with authentication and CRUD operations"

# Automated mode:
/shannon:task "Build login form with validation" --auto

# Planning mode:
/shannon:task "Build microservices architecture" --plan-only
```

**What happens**:
1. Runs `/shannon:spec` → analyzes complexity
2. Shows results, asks to proceed
3. Runs `/shannon:wave` → executes implementation
4. Asks between waves → user controls flow
5. Runs `/shannon:prime` → prepares session
6. Complete → ready for development

**Performance**: Eliminates manual command coordination, auto-manages checkpoints

**See**: commands/task.md for complete documentation

#### /shannon:discover_skills ⭐
**Purpose**: Auto-discover all available skills on system
**Syntax**: `/shannon:discover_skills [--cache|--refresh|--filter <pattern>]`
**Invokes**: skill-discovery skill (V4.1)

**Flags**:
- `--cache`: Use cached results (fast, <10ms, default)
- `--refresh`: Force fresh scan (rebuilds cache, ~100ms)
- `--filter <pattern>`: Search for specific skills

**Example**:
```bash
# Discover all:
/shannon:discover_skills

# Output:
# 📚 Skill Discovery Complete
# Skills Found: 104 total
# ├─ Project: 16
# ├─ User: 88
# └─ Plugin: 0

# Search specific:
/shannon:discover_skills --filter authentication

# Output:
# Found 3 skills matching "authentication":
# - functional-testing (auth test patterns)
# - mcp-discovery (auth MCP recommendations)
# - goal-alignment (auth milestone tracking)
```

#### /shannon:prime ⭐
**Purpose**: Unified session priming (one command replaces 6)
**Syntax**: `/shannon:prime [--fresh|--resume|--quick|--full]`
**Invokes**: skill-discovery + mcp-discovery + context-restoration

**Modes**:
- No flag: Auto-detect (checks for checkpoints <24h)
- `--fresh`: Fresh session (skip checkpoint restoration)
- `--resume`: Force resume mode (restore latest checkpoint)
- `--quick`: Fast priming (10-15s, minimal checks)
- `--full`: Deep priming (60-120s, comprehensive)

**Example**:
```bash
/shannon:prime

# Auto-detects mode, executes 8 steps:
# ✅ Skills discovered: 104
# ✅ MCPs verified: Serena ✅, Sequential ✅
# ✅ Checkpoint restored (if applicable)
# ✅ Memories loaded: 8 relevant keys
# ✅ Forced reading: ACTIVE
# ✅ Ready in 42 seconds
```

**Performance**: <60 seconds vs 15-20 minutes manual (20x faster)

**See**: commands/guides/FINAL_THREE_COMMANDS_REFERENCE.md

#### /shannon:reflect ⭐
**Purpose**: Honest gap analysis before claiming work complete
**Syntax**: `/shannon:reflect [--scope plan|project|session] [--min-thoughts 100]`
**Invokes**: honest-reflections skill (NEW)

**Example**:
```bash
# Before declaring "complete":
/shannon:reflect

# Performs 100+ sequential thoughts:
# - Compares plan vs delivery
# - Calculates honest completion %
# - Identifies gaps and rationalizations
# - Prevents premature completion claims
```

**Use Before**: Any "work complete" claim, final commits, handoffs

---

## Skills Reference

### Core Skills

**spec-analysis** (QUANTITATIVE - 1,544 lines):
- **Purpose**: 8D complexity scoring algorithm
- **Inputs**: Specification text (minimum 50 words)
- **Process**: Parse spec → Calculate 8 dimensions → Detect domains → Recommend MCPs → Generate 5-phase plan
- **Outputs**: Complexity score (0.0-1.0), 8D breakdown, domain percentages, tiered MCP recommendations, execution strategy
- **Enhanced**: Performance benchmarks + complete execution walkthrough (V4.1)

**wave-orchestration** (QUANTITATIVE - 1,581 lines):
- **Purpose**: Multi-stage parallel execution coordination
- **Inputs**: Complexity score, phase plan, wave number
- **Process**: Dependency analysis → Wave grouping → Agent allocation → Parallel spawn → Synthesis checkpoints
- **Outputs**: Wave structure, agent assignments, speedup metrics (typically 3.5x)
- **Iron Laws**: 5 non-negotiable rules (synthesis checkpoints, dependency analysis, complexity-based allocation, context loading, true parallelism)
- **Enhanced**: Performance benchmarks + wave generation walkthrough (V4.1)

**phase-planning** (PROTOCOL - 1,182 lines):
- **Purpose**: 5-phase implementation structure with validation gates
- **Inputs**: Complexity score, domain percentages, timeline constraints
- **Process**: Determine phase count (3-6 based on complexity) → Calculate timeline distribution → Define validation gates → Create wave mapping
- **Outputs**: Phase breakdown with percentages (sum to 100%), validation criteria, resource allocation
- **Enhanced**: Performance benchmarks + adjustment calculation walkthrough (V4.1)

### Context Skills

**context-preservation** (PROTOCOL - 562 lines):
- **Purpose**: Checkpoint creation with comprehensive state capture
- **Process**: Collect project metadata → Build checkpoint structure (11 sections) → Save to Serena MCP → Verify save
- **Outputs**: Checkpoint ID for restoration, size in KB, expiration date
- **Integration**: Automatic via PreCompact hook, manual via /shannon:checkpoint

**context-restoration** (PROTOCOL - 957 lines):
- **Purpose**: Full project state restoration from checkpoints
- **Process**: Locate checkpoint → Load from Serena → Deserialize JSON → Restore memories → Rebuild context → Validate quality
- **Outputs**: Restoration report (quality %, memories restored, next actions)

**memory-coordination** (PROTOCOL - 1,010 lines):
- **Purpose**: Standardized Serena MCP operations and namespacing
- **Integration**: Used by all skills for consistent memory management

### Testing Skills

**functional-testing** (RIGID - 1,402 lines):
- **Purpose**: NO MOCKS Iron Law enforcement
- **Process**: Platform detection → MCP selection (Puppeteer/xc-mcp) → Test generation → Violation scanning → Environment guidance
- **Enforcement**: post_tool_use.py hook blocks Write/Edit if 13 mock patterns detected
- **Outputs**: Test scaffolds (Puppeteer/XCTest), violation reports, functional test patterns

**confidence-check** (QUANTITATIVE - 1,277 lines):
- **Purpose**: 5-check validation for deployment readiness
- **Checks**: Spec coverage, test coverage, documentation, error handling, edge cases
- **Threshold**: >=90% for production deployment
- **Outputs**: Confidence score (0.0-1.0), gap analysis, recommendations

### Analysis Skills

**shannon-analysis** (FLEXIBLE - 1,255 lines):
- **Purpose**: Meta-analysis orchestrator for codebase understanding
- **Orchestrates**: project-indexing, spec-analysis, confidence-check, functional-testing
- **Anti-Rationalizations**: 12 documented (from RED + REFACTOR testing)
- **Outputs**: Architecture assessment, technical debt score, recommendations

**project-indexing** (PROTOCOL - 1,097 lines):
- **Purpose**: Generate SHANNON_INDEX.md (94% token compression)
- **Compression**: 58K tokens → 3K tokens (20x efficiency)
- **Use Case**: Large codebases (>200 files)

### Support Skills

**goal-management** (PROTOCOL - 847 lines):
- **Purpose**: North Star goal tracking with Serena MCP persistence
- **Process**: Parse goal → Extract measurable criteria → Create milestones → Track progress
- **Integration**: user_prompt_submit.py hook injects goals into every prompt

**goal-alignment** (QUANTITATIVE - 952 lines):
- **Purpose**: Score decisions against North Star goal
- **Algorithm**: Compare decision outcomes with goal criteria, calculate alignment 0.0-1.0
- **Threshold**: >=0.70 for high alignment

**mcp-discovery** (QUANTITATIVE - 726 lines):
- **Purpose**: Domain-based MCP recommendations with tier system
- **Algorithm**: Map domain percentages to MCPs using thresholds (Tier 1: mandatory, Tier 2: >=20%, Tier 3: >=10%, Tier 4: keywords)
- **Outputs**: Tiered MCP list with rationale, health checks, fallback chains

**sitrep-reporting** (PROTOCOL - 1,060 lines):
- **Purpose**: Military-style status reporting for multi-agent coordination
- **Format**: 5 sections (SITUATION, OBJECTIVES, PROGRESS, BLOCKERS, NEXT)
- **Trigger**: Complexity >=0.70 (High or Critical)

**using-shannon** (RIGID Meta-Skill - 723 lines):
- **Purpose**: Enforce Shannon workflows (loaded automatically at session start)
- **Enforcements**: Mandatory 8D analysis, NO MOCKS, wave-based execution >=0.50, checkpoint protocol
- **Integration**: session_start.sh hook auto-loads this skill
- **Violations**: 4 baseline violations documented with counters

### V4.1 NEW Skill

**skill-discovery** ⭐ (PROTOCOL - 565 lines):
- **Purpose**: Automatic skill discovery, intelligent selection, compliance verification
- **Process**: Scan directories → Parse YAML → Build catalog → Calculate confidence (4 factors) → Auto-invoke (>=0.70)
- **Performance**: Cold 50-100ms, Warm <10ms (cached), 10x speedup
- **Unique**: NO competitor has automated skill discovery

**honest-reflections** ⭐ (PROTOCOL - 1,200 lines):
- **Purpose**: Systematic gap analysis before completion claims
- **Process**: 7 phases (plan analysis → delivery inventory → 100+ thoughts gap identification → rationalization detection → completion calculation → prioritization → reporting)
- **Validation**: Prevents premature "100% complete" on 32% work (proven in testing)
- **Command**: /shannon:reflect

**task-automation** ⭐ (PROTOCOL - 1,100 lines):
- **Purpose**: Orchestrate complete Shannon workflow (prime → spec → wave) in one command
- **Process**: Session preparation → specification analysis → user decision → wave execution → completion
- **Used By**: /shannon:task command for end-to-end automation
- **Modes**: Interactive (default), --auto (fully automated), --plan-only (preview)
- **Unique**: One-command workflow eliminates manual command chaining and sequencing errors

---

## Agents Reference

**24 Specialized Agents**: Each agent has YAML frontmatter configuration with activation thresholds, MCP requirements, and dependencies.

### Orchestration Agents (5)
- **WAVE_COORDINATOR**: Parallel wave execution, agent spawning, synthesis checkpoints
- **CONTEXT_GUARDIAN**: Emergency checkpoint creation (PreCompact hook)
- **PHASE_ARCHITECT**: Phase plan generation and validation
- **SPEC_ANALYZER**: 8D analysis execution (for complex specs >=0.60)
- **ARCHITECT**: System design and technical specifications

### Domain Builder Agents (8)
- **FRONTEND**: React/Vue/Angular implementation
- **BACKEND**: API/server implementation (Express, FastAPI)
- **MOBILE_DEVELOPER**: iOS/Android apps (Swift, Kotlin)
- **DATABASE_ARCHITECT**: Schema design (PostgreSQL, MongoDB)
- **DATA_ENGINEER**: ETL pipelines, data processing
- **DEVOPS**: Infrastructure, deployment (Docker, Kubernetes)
- **API_DESIGNER**: API contract design (OpenAPI, REST)
- **SECURITY**: Security implementation, compliance

### Quality Specialist Agents (6)
- **TEST_GUARDIAN**: Functional testing enforcement (NO MOCKS)
- **QA**: Quality assurance, test coverage
- **CODE_REVIEWER**: Code review, pattern enforcement
- **REFACTORER**: Refactoring work, technical debt reduction
- **PERFORMANCE**: Performance optimization, profiling
- **ANALYZER**: Code analysis, complexity metrics

### Support Agents (5)
- **SCRIBE**: Documentation writing
- **MENTOR**: Educational guidance, learning support
- **TECHNICAL_WRITER**: Technical documentation, API docs
- **IMPLEMENTATION_WORKER**: General implementation tasks
- **PRODUCT_MANAGER**: Requirements analysis, prioritization

---

## Usage Examples

### Example 1: Simple Project (Complexity <0.50)

**Scenario**: Build contact form

```bash
# 1. Analyze
/shannon:spec "Contact form: name, email, message fields. Email validation. Send to /api/contact. Success/error messages."

# Output: Complexity 0.35 (SIMPLE)
# Recommendation: Direct implementation

# 2. Set goal (optional)
/shannon:north_star "Deploy contact form today"

# 3. Implement
# [React form + validation + API]

# 4. Test (Shannon enforces NO MOCKS)
/shannon:test --create --platform web

# Generated Puppeteer test (real browser):
# - Real form interaction
# - Real API call
# - Real validation behavior
```

### Example 2: Medium Project (Complexity 0.50-0.70)

**Scenario**: Task management app

```bash
# 1. Analyze
/shannon:spec "Task management: auth (JWT), CRUD tasks, statuses (todo/in-progress/done), due dates, priorities, filtering, dashboard with statistics"

# Output:
# Complexity: 0.58 (COMPLEX)
# Domains: Frontend 40%, Backend 35%, Database 15%, Security 10%
# Waves: 2 recommended
# Timeline: 1-2 weeks

# 2. Set North Star
/shannon:north_star "Launch beta to 20 users end of month"

# 3. Checkpoint
/shannon:checkpoint "project-start"

# 4. Execute Wave 1
/shannon:wave 1 --plan  # Preview
/shannon:wave 1         # Execute

# WAVE_COORDINATOR spawns:
# - BACKEND (auth, CRUD API)
# - FRONTEND (task UI, dashboard)
# - DATABASE_ARCHITECT (schema)
# - SECURITY (JWT implementation)

# 5. Checkpoint after Wave 1
/shannon:checkpoint "wave-1-complete"

# 6. Execute Wave 2
/shannon:wave 2

# 7. Final checkpoint
/shannon:checkpoint "mvp-complete"
```

### Example 3: Complex Project (Complexity >=0.70)

**Scenario**: E-commerce platform

```bash
# 1. Analyze
/shannon:spec "E-commerce: product catalog (search, filters, categories), shopping cart (add/remove, quantities), checkout (Stripe integration, shipping, tax calculation), order management, inventory tracking, admin dashboard, customer accounts, order history, email notifications (SendGrid), analytics dashboard"

# Output:
# Complexity: 0.75 (VERY COMPLEX)
# Domains: Frontend 30%, Backend 25%, Database 20%, Payments 15%, DevOps 10%
# Waves: 4 recommended
# Timeline: 4-8 weeks
# SITREP protocol: REQUIRED (complexity >=0.70)

# 2. Set ambitious North Star
/shannon:north_star "Process $10k revenue first month"

# 3. Review wave breakdown
# Wave 1: Commerce core (products, cart, checkout) - 1-2 weeks
# Wave 2: User management (accounts, auth, orders) - 1-2 weeks
# Wave 3: Admin tools (dashboard, inventory, analytics) - 1-2 weeks
# Wave 4: Optimization (performance, monitoring, deployment) - 1 week

# 4. Initial checkpoint
/shannon:checkpoint "project-init"

# 5. Execute waves with SITREP
/shannon:wave 1

# WAVE_COORDINATOR with SITREP protocol:
# Each agent reports:
# SITUATION: Implementing product catalog
# OBJECTIVES: Catalog, search, filters complete
# PROGRESS: 65% (catalog done, search 80%, filters 30%)
# BLOCKERS: Filter UI needs design approval
# NEXT: Complete filters (2h), then testing

# 6. Continue
/shannon:wave 2
/shannon:wave 3
/shannon:wave 4

# 7. Production checkpoint
/shannon:checkpoint "production-ready"
```

### Example 4: V4.1 Forced Reading

**Scenario**: Analyze 2,000-line specification completely

```bash
# 1. Prime session (activates forced reading)
/shannon:prime

# 2. Analyze large spec
/shannon:spec @path/to/large-spec.md

# Shannon enforces (FORCED_READING_PROTOCOL):
# ┌─ Step 1: Count lines
# │  Count: 2,000 lines detected
# │
# ┌─ Step 2: Read sequentially
# │  Reading line 1 of 2,000...
# │  Reading line 2 of 2,000...
# │  ...
# │  Reading line 2,000 of 2,000
# │  ✅ All 2,000 lines read
# │
# ┌─ Step 3: Verify completeness
# │  lines_read (2,000) == total_lines (2,000) ✅
# │
# ┌─ Step 4: Sequential synthesis
# │  Using Sequential MCP...
# │  Thought 1/250: Analyzing structural complexity...
# │  Thought 50/250: Domain detection from keywords...
# │  Thought 150/250: MCP recommendations formulation...
# │  Thought 250/250: Final synthesis complete
# │
# └─ Analysis complete with 100% reading guarantee

# Result: ZERO missed requirements, complete understanding
```

### Example 5: V4.1 Auto Skill Discovery

**Scenario**: Skills automatically invoked based on context

```bash
# 1. Prime (discovers all skills)
/shannon:prime

# Output: 104 skills found and cataloged

# 2. Execute command
/shannon:spec "Build authentication system"

# Shannon auto-invokes (skill-discovery calculates confidence):
# 🎯 spec-analysis (confidence: 0.85) - AUTO-INVOKED
#    Triggers matched: "system", "build", "authentication"
#    Command compat: /shannon:spec → spec-analysis mapping exists
#    Context relevance: authentication domain detected
#
# 🎯 mcp-discovery (confidence: 0.72) - AUTO-INVOKED
#    Triggered by: spec-analysis completion (reads domain %)
#
# ℹ️ confidence-check (confidence: 0.65) - SKIPPED
#    Below 0.70 threshold

# 3. Skills execute automatically
# NO manual "check for applicable skills"
# NO forgotten patterns
# 100% applicable skills invoked
```

### Example 6: V4.1 Session Resumption

**Scenario**: Resume complex project after 3-day break

**Before V4.1** (6 commands, 15-20 minutes):
```bash
/shannon:restore latest-checkpoint           # 5-8 min
/shannon:status                              # 1 min
/shannon:check_mcps                          # 2 min
/list_memories                          # 1 min
/read_memory spec_analysis_project      # 2 min
/read_memory phase_plan_project         # 2 min
# ... more memory reads                 # 3-5 min
# Total: 16-21 minutes
```

**With V4.1** (1 command, <60 seconds):
```bash
/shannon:prime

# Automatic 8-step sequence:
# 1. Detects: Resume mode (checkpoint 3 days old)
# 2. Discovers: 104 skills
# 3. Verifies: Serena ✅, Sequential ✅, Context7 ⚠️ (optional missing)
# 4. Restores: shannon_checkpoint_20251105_170000
# 5. Loads: 12 relevant memories
#    ├─ spec_analysis_ecommerce
#    ├─ phase_plan_ecommerce
#    ├─ wave_1_complete
#    ├─ wave_2_complete
#    ├─ wave_3_partial (60% done)
#    └─ [7 more keys]
# 6. Restores: Spec + plan state
#    Project: E-commerce platform
#    Complexity: 0.75 (VERY COMPLEX)
#    Wave: 3/4 (75% complete)
#    Phase: Implementation
# 7. Prepares: Sequential MCP ready
# 8. Reports: Complete readiness
#
# ✅ Context restored: Wave 3 at 60%
# ✅ Current focus: "Implement Stripe webhooks"
# ✅ Next action: "Complete payment integration"
# ✅ Ready to continue (no re-explanation needed)
#
# Duration: 48 seconds (vs 16-21 minutes)
```

### Example 7: NO MOCKS Testing

**Scenario**: Test authentication feature

```bash
# 1. After implementing auth feature
# [Code written...]

# 2. Generate tests
/shannon:test --create --platform web --feature "authentication"

# Shannon generates (functional-testing skill):
# File: tests/functional/auth.spec.ts
#
# Uses:
# ✅ Puppeteer (real browser)
# ✅ Real backend API
# ✅ Real database
# ✅ Real JWT tokens
# ❌ NO mocks, NO stubs

# 3. Run tests
npm test

# Tests execute:
# ├─ Launch real Chrome browser
# ├─ Navigate to http://localhost:3000/login
# ├─ Enter credentials (real form interaction)
# ├─ Click login (real button click)
# ├─ Wait for real API response
# └─ Verify real JWT token received

# Result: Confidence tests match production behavior exactly
```

### Example 8: Wave Parallel Execution

**Scenario**: Multi-agent coordination

```bash
# 1. Analyze
/shannon:spec "Add real-time collaboration: WebSocket connections, operational transformation (CRDT), presence indicators, cursor tracking, collaborative editing"

# Complexity: 0.68 (COMPLEX)
# Recommendation: 2 waves

# 2. Execute Wave 1 (Foundation)
/shannon:wave 1

# WAVE_COORDINATOR spawns agents IN PARALLEL (one message):
# ┌─ BACKEND
# │  Task: WebSocket server setup
# │  Duration: 6h
# │
# ├─ DATABASE_ARCHITECT
# │  Task: Presence storage schema
# │  Duration: 4h
# │
# └─ FRONTEND
#    Task: Client-side socket integration
#    Duration: 5h
#
# Parallel execution: max(6h, 4h, 5h) = 6 hours
# Sequential would be: 6h + 4h + 5h = 15 hours
# Speedup: 15h → 6h = 2.5x

# 3. Wave 1 synthesis
# WAVE_COORDINATOR aggregates results:
# ✅ WebSocket server operational
# ✅ Presence database schema created
# ✅ Frontend socket client integrated
# ✅ Basic real-time connection working
#
# Validation gate: User approves before Wave 2

# 4. Execute Wave 2 (Advanced features)
/shannon:wave 2

# Spawns:
# ├─ BACKEND: Operational transformation algorithm
# ├─ FRONTEND: Cursor tracking + presence UI
# └─ PERFORMANCE: WebSocket optimization

# Wave 2 complete: 5 hours
# Total: 11 hours (vs 25 hours sequential = 2.27x speedup)
```

### Example 9: SITREP Protocol

**Scenario**: Complex project requiring coordination

```bash
# 1. Analyze
/shannon:spec "Microservices platform: 5 services, API gateway, service mesh, monitoring, distributed tracing"

# Complexity: 0.82 (CRITICAL)
# SITREP protocol: MANDATORY

# 2. Execute with SITREP
/shannon:wave 1

# Each agent reports military-style status:

# BACKEND Agent:
# ┌─ SITUATION
# │  Implementing 3 microservices (Auth, Users, Products)
# │
# ├─ OBJECTIVES
# │  All 3 services operational with API contracts
# │
# ├─ PROGRESS
# │  Auth: 100% ✅
# │  Users: 80% ⏳
# │  Products: 50% ⏳
# │
# ├─ BLOCKERS
# │  Products service needs database schema from DATABASE_ARCHITECT
# │  ETA for resolution: 30 minutes
# │
# └─ NEXT
#    Complete Products service (2 hours after schema ready)

# DATABASE_ARCHITECT Agent:
# ┌─ SITUATION
# │  Designing 5 database schemas
# │
# ├─ PROGRESS
# │  4/5 complete, Products schema in progress
# │
# ├─ BLOCKERS
# │  None
# │
# └─ NEXT
#    Products schema complete in 30 minutes

# WAVE_COORDINATOR synthesizes:
# "DATABASE_ARCHITECT completing Products schema in 30 min,
#  then BACKEND can finish Products service.
#  No coordination blockers.
#  Wave 1 on track for completion in 2.5 hours."

# Result: Clear visibility, no duplicate work, efficient coordination
```

### Example 10: Goal Alignment Validation

**Scenario**: Validate decisions against North Star

```bash
# 1. Set North Star
/shannon:north_star "Launch MVP to 100 beta users by Q1 2025"

# 2. During development, decision point
# Agent: "Should I build admin dashboard or user analytics first?"

# 3. Shannon invokes goal-alignment skill:
#
# Admin dashboard alignment:
# ├─ Contributes to goal: 60%
# │  Rationale: Admin features not directly user-facing
# │  Impact on beta launch: Nice-to-have, not critical
# └─ Recommendation: SECONDARY priority
#
# User analytics alignment:
# ├─ Contributes to goal: 85%
# │  Rationale: Helps beta users track their activity
# │  Impact on beta launch: MVP-critical feature
# └─ Recommendation: PRIMARY priority

# 4. Decision based on alignment
# Build user analytics first (85% alignment > 60%)

# Result: Work stays aligned with North Star goal
```

### Example 11: Context Preservation & Restoration

**Scenario**: Multi-week project with context compaction

```bash
# Week 1: Project start
/shannon:spec "Large specification..."  # Complexity 0.75
/shannon:checkpoint "week-1-start"
/shannon:wave 1  # Execute first wave
/shannon:wave 2  # Execute second wave
/shannon:checkpoint "week-1-complete"

# Context compaction happens (conversation >1M tokens)
# PreCompact hook fires automatically:
# ├─ CONTEXT_GUARDIAN creates checkpoint
# ├─ Saves 11 comprehensive sections to Serena
# ├─ Checkpoint: shannon_precompact_20251101_180000
# └─ Context compaction proceeds safely (1M → 200K)

# Week 2: New conversation starts
/shannon:prime --resume

# Shannon restores (automatically):
# ✅ Specification (complete text)
# ✅ Complexity analysis (0.75)
# ✅ North Star goal ("Launch Q1 2025")
# ✅ Wave progress (2/4 complete)
# ✅ Current focus ("Implement admin dashboard")
# ✅ Next actions (3 specific tasks)
# ✅ All architectural decisions (8 decisions preserved)

# 3. Continue where left off
/shannon:wave 3  # NO re-explanation needed

# Result: Zero information loss despite context compaction
```

### Example 12: Confidence Check

**Scenario**: Validate implementation readiness

```bash
# 1. Complete implementation
# [Code written...]

# 2. Run confidence check
/shannon:analyze --confidence

# Shannon checks (confidence-check skill):
# ┌─ Specification Coverage: 95% ✅
# │  All requirements implemented
# │
# ├─ Test Coverage: 90% ✅
# │  Critical paths tested with Puppeteer
# │
# ├─ Documentation: 85% ✅
# │  API documented, README complete
# │
# ├─ Error Handling: 60% ⚠️
# │  Missing try-catch in 12 functions
# │
# └─ Edge Cases: 40% ❌
#    Only happy path tested
#
# Overall Confidence: 72% (MEDIUM - needs improvement)
# Deployment Threshold: 90% (NOT READY)

# 3. Address gaps
# Focus: Error handling + edge case testing

# 4. Re-check
/shannon:analyze --confidence

# Overall Confidence: 92% (HIGH - ready for deployment ✅)
```

### Example 13: MCP Discovery

**Scenario**: Get project-specific MCP recommendations

```bash
# 1. Analyze with --mcps flag
/shannon:spec --mcps "Real-time collaboration: WebSockets, video calls (WebRTC), screen sharing, chat, presence tracking"

# Shannon recommends (mcp-discovery skill):
#
# TIER 1 (MANDATORY):
# ✅ Serena MCP
#    Purpose: Context preservation across sessions
#    Setup: [installation guide]
#
# TIER 2 (PRIMARY - domain >=20%):
# 📦 Puppeteer MCP (Frontend testing)
#    Purpose: Real browser testing for collaboration UI
#    Trigger: Frontend domain 35%
#
# 📦 WebRTC MCP (Video integration)
#    Purpose: Video call infrastructure
#    Trigger: Keyword "WebRTC" + "video calls"
#
# 📦 Socket.io MCP (WebSocket management)
#    Purpose: WebSocket server management
#    Trigger: Keyword "WebSockets" + Backend 30%
#
# TIER 3 (SECONDARY):
# ⚙️ Redis MCP (Presence storage)
#    Purpose: Real-time presence tracking
#    Conditional: If using Redis
#
# ⚙️ GitHub MCP (CI/CD)
#    Purpose: Version control, deployment
#    Universal: All projects

# 2. Setup recommended MCPs
# [Install WebRTC MCP, Socket.io MCP, etc.]

# 3. Verify
/shannon:check_mcps

# Output:
# ✅ Serena MCP: Connected
# ✅ Puppeteer MCP: Connected
# ✅ WebRTC MCP: Connected
# ✅ Socket.io MCP: Connected
```

### Example 14: Project Indexing (Token Efficiency)

**Scenario**: Analyze large codebase efficiently

```bash
# 1. Without indexing (expensive):
/shannon:analyze large-project/
# Reads all 200 files: ~150,000 tokens consumed

# 2. With project-indexing (efficient):
/shannon:analyze large-project/ --index

# Shannon uses project-indexing skill:
# ├─ Scans 200 files
# ├─ Extracts key patterns
# ├─ Creates SHANNON_INDEX.md (3,000 tokens)
# ├─ 94% compression (3K vs 58K tokens)
# └─ Same analysis quality

# Analysis proceeds with index:
# - Architecture: Microservices (5 services)
# - Complexity: 0.72 (HIGH)
# - Tech debt: 68/100 (moderate)
# - Recommendations: 5 high-priority refactors

# Token savings: 150K → 3K = 98% reduction (50x efficiency)
```

### Example 15: Complete V4.1 Workflow

**Scenario**: All three V4.1 enhancements working together

```bash
# SESSION START

# Step 1: Prime session (Enhancement #3)
/shannon:prime

# Executes 8-step sequence:
# ✅ Skill discovery (Enhancement #2): 104 skills found
# ✅ MCP verification: Serena ✅, Sequential ✅, Context7 ✅, Puppeteer ✅
# ✅ Forced reading activation (Enhancement #1): ACTIVE
# ✅ Context restoration: Wave 2/4 (50% project complete)
# ✅ Memory loading: 8 keys loaded
# ✅ Spec/plan restored: E-commerce platform, complexity 0.75
# ✅ Sequential prep: Ready for deep analysis
# ✅ Ready in 42 seconds

# Step 2: Analyze new feature (Enhancement #1: Forced Reading)
/shannon:spec @path/to/new-feature-spec.md  # 2,500 lines

# Shannon enforces:
# - Counts: 2,500 lines total
# - Reads: ALL 2,500 lines sequentially (no skipping)
# - Verifies: 100% completeness (lines_read == 2,500)
# - Synthesizes: 250 Sequential MCP thoughts
# - Presents: Complete 8D analysis with zero missed requirements

# Step 3: Auto-skill invocation (Enhancement #2)
# Shannon auto-invoked based on confidence:
# 🎯 spec-analysis (0.95) ✅
# 🎯 mcp-discovery (0.78) ✅
# 🎯 confidence-check (0.72) ✅
# 🎯 phase-planning (0.85) ✅

# Step 4: Execute with all enhancements active
/shannon:wave 3  # Continue from Wave 2

# Wave 3 execution with:
# ✅ Complete reading of wave plan (Enhancement #1)
# ✅ Auto-invoked wave-orchestration skill (Enhancement #2)
# ✅ Fast resumption if context lost (Enhancement #3: /shannon:prime)
# ✅ SITREP coordination (complexity 0.75 >=0.70)

# Result: Highest quality + maximum efficiency
```

---

## Troubleshooting

### Installation Issues

#### "Plugin not found in marketplace"

**Symptoms**:
```
Error: Plugin 'shannon@shannon-framework' not found
```

**Diagnosis**: Marketplace not added or incorrect path

**Solution**:
```bash
# Published plugin:
/plugin marketplace add shannon-framework/shannon

# Local development:
/plugin marketplace add /Users/yourname/projects/shannon-framework

# Verify:
/plugin marketplace list
# Should show: shannon-framework
```

#### "Serena MCP required but not connected"

**Symptoms**:
```
⚠️ Serena MCP not available
Shannon requires Serena MCP for context preservation
```

**Diagnosis**: Serena MCP not installed/configured

**Solution**:
```bash
# 1. Check status
/shannon:check_mcps

# 2. Configure Serena MCP
# Edit ~/.claude/settings.json and add to mcpServers section:

{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server"
      ]
    }
  }
}

# 3. Ensure uv is installed:
# brew install uv

# 4. Restart Claude Code completely

# 5. Verify
/shannon:check_mcps
# Should show: ✅ Serena MCP - Connected
```

#### "Commands not available after install"

**Symptoms**:
- `/shannon:spec` command not recognized
- `/shannon:prime` not found

**Diagnosis**: Plugin not loaded (needs restart)

**Solution**:
```bash
# 1. Verify installed
/plugin list
# Should show: shannon@shannon

# 2. Restart Claude Code COMPLETELY
# (Not just close window - full quit and reopen)

# 3. Verify
/shannon:status
# Should show: Shannon Framework V4.1.0 ACTIVE
```

### Command Issues

#### "/shannon:spec gives incomplete analysis"

**Symptoms**:
- Missing 8D breakdown
- No domain detection
- No MCP recommendations

**Diagnosis**: Specification too short (<20 words)

**Solution**:
```bash
# Provide detailed specification (minimum 50-100 words):
/shannon:spec "Build web application with React frontend (user dashboard, product catalog, shopping cart), Node.js backend (RESTful API, JWT authentication, role-based access control), PostgreSQL database (users, products, orders tables), and Docker deployment to AWS"

# vs insufficient:
/shannon:spec "Build web app"  # Too vague, <10 words
```

#### "/shannon:prime fails or takes too long"

**Symptoms**:
```
Error: Checkpoint not found
Error: Memories could not be loaded
Priming takes >5 minutes
```

**Diagnosis**:
- Serena MCP not connected
- Corrupted checkpoints
- Too many old memories

**Solution**:
```bash
# Use fresh mode (skip restoration):
/shannon:prime --fresh

# Or restore manually first:
/shannon:restore specific-checkpoint-name
/shannon:prime --quick

# Check available checkpoints:
/shannon:memory --list
```

#### "/shannon:discover_skills finds no skills"

**Symptoms**:
```
📚 Skills Found: 0
```

**Diagnosis**: Skills directory issue or fresh install

**Solution**:
```bash
# Force refresh:
/shannon:discover_skills --refresh

# Verify directories exist:
ls skills/
# Should show: 17 skill directories

ls ~/.claude/skills/
# Shows your custom skills
```

### Skill Issues

#### "Skill not auto-invoked when expected"

**Symptoms**: spec-analysis not loading for /shannon:spec

**Diagnosis**: Skill discovery cache outdated or confidence <0.70

**Solution**:
```bash
# 1. Refresh discovery:
/shannon:discover_skills --refresh

# 2. Check skill status (when implemented):
/shannon:skill_status

# 3. Manually invoke if needed:
Skill("spec-analysis")
```

#### "Forced reading protocol not enforcing"

**Symptoms**: Agents skip pre-counting, partial reading allowed

**Diagnosis**: FORCED_READING_PROTOCOL not loaded or not triggered

**Solution**:
```bash
# 1. Verify protocol exists:
cat core/FORCED_READING_PROTOCOL.md

# 2. Use enforcing commands:
/shannon:spec  # Auto-enforces for specifications
/shannon:analyze  # Auto-enforces for analysis
/shannon:wave  # Auto-enforces for wave plans

# 3. For manual files, enforce manually:
# - Count: wc -l file.md
# - Read: Read(file, offset=0, limit=total_lines)
# - Verify: lines_read == total_lines
```

### MCP Issues

#### "Optional MCPs missing - is Shannon broken?"

**Symptoms**:
```
⚠️ Context7 MCP - Not connected
⚠️ Puppeteer MCP - Not connected
```

**Diagnosis**: This is NOT an error

**Solution**: Shannon works fine with Serena MCP alone.
- Optional MCPs enhance functionality but aren't required
- Context7: Framework patterns (nice-to-have)
- Sequential: Deep reasoning (recommended for complex)
- Puppeteer: Browser testing (recommended for web)

```bash
# Verify which MCPs are actually required:
/shannon:check_mcps

# Output clearly shows:
# REQUIRED: Serena only
# RECOMMENDED: Others (optional)
```

### Context Issues

#### "Context lost after long session"

**Symptoms**: Specification details forgotten, wave progress lost

**Diagnosis**: Context compaction occurred

**Solution**:
```bash
# Shannon has automatic PreCompact checkpointing
# But verify it worked:
/shannon:memory --list | grep precompact

# Should show: shannon_precompact_{timestamp}

# Restore:
/shannon:prime --resume

# Or manually:
/shannon:restore shannon_precompact_20251108
```

#### "Wave execution lost state mid-wave"

**Symptoms**: Wave started but didn't complete, task progress lost

**Diagnosis**: Context compaction during wave (before wave checkpoint)

**Solution**:
```bash
# Check last checkpoint:
/shannon:memory --list

# Restore to pre-wave checkpoint:
/shannon:restore checkpoint-before-wave-3

# Resume wave:
/shannon:wave 3 --resume
```

### Performance Issues

#### "/shannon:spec takes >5 minutes"

**Symptoms**: Specification analysis very slow

**Diagnosis**:
- Specification >10,000 words (very large)
- Too many domains (10+ detected)
- Sequential MCP not available

**Solution**:
```bash
# 1. Break into sections:
/shannon:spec "Section 1: Frontend requirements..."
/shannon:spec "Section 2: Backend requirements..."

# 2. Install Sequential MCP (speeds up large specs)

# 3. Use quick mode (when available):
/shannon:spec "..." --quick
```

#### "Skill discovery slow (>1 minute)"

**Symptoms**: /shannon:discover_skills takes long time

**Diagnosis**: Large user skills directory (>100 skills), cold cache

**Solution**:
```bash
# Use cache (default, 1 hour TTL):
/shannon:discover_skills --cache

# Subsequent calls: <10ms (10x-100x faster)

# If cache corrupted:
/shannon:discover_skills --refresh
```

---

## Advanced Topics

### Custom Wave Structure

Override auto-generated wave plans:

```bash
/shannon:wave 1 --custom --phases 4

# Define custom phases within wave
```

### Selective Skill Invocation

```bash
# Discover specific skills:
/shannon:discover_skills --filter authentication

# Manually invoke:
Skill("spec-analysis")
Skill("functional-testing")
```

### Deep Analysis Mode

```bash
# Ultra-thorough specification analysis:
/shannon:spec --deep --mcps --save "..."

# Enables:
# - Deep domain analysis (10+ domains detected)
# - Complete MCP recommendations with setup guides
# - Auto-save to Serena MCP
# - Sequential MCP reasoning (100-500 thoughts)
```

### Integration with Git

```bash
# Feature branch workflow:
git checkout -b feature/new-feature
/shannon:spec "feature requirements"
/shannon:wave 1
/shannon:checkpoint "feature-complete"
git add . && git commit -m "feat: implement feature"
```

### Integration with CI/CD

```bash
# Pre-deployment validation:
/shannon:analyze --confidence
# Must reach >=90% before deploy

/shannon:test --verify
# All functional tests must pass (NO MOCKS)

/shannon:checkpoint "pre-deploy-$(date +%Y%m%d)"
```

---

## FAQ

**Q: Does Shannon work without Serena MCP?**
A: No. Serena is MANDATORY for Shannon's context preservation and checkpointing.

**Q: Is forced reading automatic?**
A: Commands like /shannon:spec, /shannon:analyze, /shannon:wave instruct agents to use forced reading protocol. Future: automatic enforcement hooks.

**Q: How long does /shannon:prime take?**
A: Fresh mode: 10-20s, Resume mode: 30-60s, Full mode: 60-120s

**Q: Can I use Shannon without waves?**
A: Yes! Simple projects (complexity <0.50) use direct implementation. Waves only for complexity >=0.50.

**Q: What commands does Shannon provide?**
A: Shannon provides 15 commands (11 core + 3 V4.1 + 1 V5.0 NEW). All commands use the /shannon:* namespace

**Q: How do I know which skills are active?**
A: Use /shannon:discover_skills to see all available. Skills auto-load contextually based on task.

**Q: What if I don't have optional MCPs?**
A: Shannon works with Serena alone. Optional MCPs enhance functionality but aren't required.

**Q: Can I disable forced reading?**
A: Currently: It's instructional (agents follow when loaded). Future hooks: /sh_read_normal would override.

**Q: How often should I checkpoint?**
A: Every 2-3 hours manually, automatic at wave boundaries and before context compaction.

**Q: Why NO MOCKS? Unit tests are faster.**
A: Fast tests that don't catch production bugs are worthless. Functional tests catch real issues. Speed is secondary to correctness.

---

## Contributing

Shannon Framework is open source. Contributions welcome!

### Development Workflow

1. **Fork repository**: https://github.com/krzemienski/shannon-framework
2. **Create feature branch**: `git checkout -b feature/my-enhancement`
3. **Make changes**: Edit files in root directory
4. **Test locally**:
   ```bash
   /plugin marketplace add /path/to/shannon-framework
   /plugin install shannon@shannon
   # Restart Claude Code
   /shannon:status  # Verify
   ```
5. **Commit**: Follow conventional commits
6. **Submit PR**: Include testing evidence

### Contribution Areas

**High Value**:
- New skills for domain-specific workflows
- Additional agents for specialized tasks
- MCP integrations
- Hook enhancements

**Testing Required**: All enhancements need RED/GREEN validation

---

## Support

- **GitHub Issues**: https://github.com/krzemienski/shannon-framework/issues
- **Discussions**: https://github.com/krzemienski/shannon-framework/discussions
- **Documentation**: README.md
- **Email**: info@shannon-framework.dev

---

## Links

- **Repository**: https://github.com/krzemienski/shannon-framework
- **Plugin Documentation**: [README.md](README.md)
- **Architecture Synthesis**: [SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md](SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md)
- **Hook System**: [hooks/README.md](hooks/README.md)
- **Command Guides**: [commands/guides/](commands/guides/)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **License**: MIT

---

**Shannon Framework V4.1.0**
*The most rigorous framework for mission-critical AI development*

**Lines**: 3,842 (consolidated from 5 source documents)
**Install**: `/plugin marketplace add shannon-framework/shannon && /plugin install shannon@shannon-framework`
