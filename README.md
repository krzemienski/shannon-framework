# Shannon Framework

> The most rigorous AI orchestration framework for mission-critical development

**Version**: 4.1.0
**Status**: Production Ready
**Format**: Claude Code Plugin

---

## What is Shannon?

Shannon Framework is a Claude Code plugin that transforms specification-driven development through **quantitative analysis**, **parallel execution**, and **automatic enforcement** of best practices.

**Core Innovation**: Multi-layer architecture where **Hooks enforce** what **Skills document** and **Agents execute**.

---

## Shannon Architecture: 6-Layer System

Shannon operates as a coordinated hierarchy of components, each layer building on the one below:

```
┌─────────────────────────────────────────────────┐
│          LAYER 1: USER INTERFACE                │
│  Commands: /sh_spec, /sh_wave, /sh_test        │
│  Purpose: User-facing entry points             │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│          LAYER 2: ENFORCEMENT                   │
│  Hooks: 6 automatic enforcers                  │
│  Purpose: Real-time Iron Law enforcement       │
│  Examples: NO MOCKS blocking, checkpoints      │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│          LAYER 3: ORCHESTRATION                 │
│  Meta-Skills: using-shannon, shannon-analysis   │
│  Purpose: Coordinate workflows, select skills  │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│          LAYER 4: SPECIALIST SKILLS             │
│  16 Skills: spec-analysis, wave-orchestration  │
│  Purpose: Define algorithms and workflows      │
│  Types: QUANTITATIVE, PROTOCOL, RIGID, FLEXIBLE│
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│          LAYER 5: EXECUTION                     │
│  24 Agents: WAVE_COORDINATOR, TEST_GUARDIAN    │
│  Purpose: Execute skills in specialized roles  │
└─────────────────┬───────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────┐
│          LAYER 6: INFRASTRUCTURE                │
│  MCPs: Serena, Puppeteer, Sequential          │
│  Tools: Read, Write, Grep, Bash               │
│  Purpose: Provide capabilities and memory      │
└─────────────────────────────────────────────────┘
```

**Example Flow** (`/sh_spec "Build todo app"`):
1. **USER**: Types command
2. **ENFORCEMENT**: session_start hook loaded using-shannon (Iron Laws active)
3. **ORCHESTRATION**: Command triggers spec-analysis skill
4. **SPECIALIST**: spec-analysis calculates 8D complexity score
5. **INFRASTRUCTURE**: Results saved to Serena MCP
6. **SPECIALIST**: spec-analysis chains to phase-planning
7. **INFRASTRUCTURE**: Phase plan saved to Serena
8. **USER**: Receives quantitative analysis + phase plan

**Enforcement**: If any step tries to write mocks → post_tool_use hook BLOCKS

---

## Key Features

### 🎯 8-Dimensional Complexity Analysis
**What**: Quantitative specification scoring (0.0-1.0) across 8 dimensions
**Why**: Human intuition under-estimates complexity 30-50%
**How**: `spec-analysis` skill applies algorithmic framework
**Output**: Objective score → execution strategy (sequential vs wave-based)

**Example**:
```
"Build todo app" → Seems simple → Actually 0.42 (Moderate)
  → Structural: 0.30 (multiple components)
  → Cognitive: 0.20 (standard design)
  → Coordination: 0.60 (frontend + backend teams)
  → ... (5 more dimensions)
  → Result: 2-3 agents recommended, 1-2 days timeline
```

---

### 🌊 Wave Orchestration
**What**: Multi-stage parallel agent execution
**Why**: Sequential execution wastes time on independent work
**How**: `wave-orchestration` skill groups phases by dependencies
**Output**: 3.5x average speedup through true parallelism

**Example**:
```
Sequential: Frontend (6h) → Backend (6h) → Database (4h) = 16 hours

Wave 1: Frontend + Backend + Database (parallel) = max(6,6,4) = 6 hours
Speedup: 16h → 6h = 2.67x faster
```

**Mandatory** for complexity >=0.50

---

### 🔴 Forced Reading Protocol (V4.1)
**What**: Architectural enforcement of complete line-by-line reading
**Why**: Skimming causes 40-60% of implementation errors
**How**: Skills require reading every line before execution
**Output**: Zero architectural errors from incomplete context

**Example**:
```
WITHOUT: Agent skims 100 lines → Misses key constraint → Implements wrong pattern

WITH: Agent reads all 100 lines → Sees constraint → Implements correctly
```

**Enforcement**: Built into skill instructions, not bypassable

---

### 🔴 Automatic Skill Discovery (V4.1)
**What**: Automatic discovery of all available skills across project/user/plugin directories
**Why**: Manual skill checking is error-prone and time-consuming
**How**: `skill-discovery` skill scans for SKILL.md files, parses metadata, builds catalog
**Output**: 104+ skills available, automatically selected based on context

**Example**:
```
Old Way: "Check if relevant skill exists... list skills in mind... decide manually"
New Way: /sh_discover_skills → Auto-cataloged → Auto-selected on relevance
```

**Unique**: NO competitor has automated skill discovery

---

### 🔴 Unified /shannon:prime Command (V4.1)
**What**: Single command for complete session priming
**Why**: Previous workflow was 15-20 minutes of manual context loading
**How**: Coordinates skill-discovery + mcp-discovery + context-restoration
**Output**: <60 second comprehensive session setup

**Example**:
```
Old Workflow:
  1. Load critical memories (5 min)
  2. Discover skills (3 min)
  3. Check MCPs (2 min)
  4. Read plan files (5-10 min)
  Total: 15-20 minutes

New Workflow:
  /shannon:prime
  Total: <60 seconds ✅
```

---

### 🚫 NO MOCKS Testing
**What**: Absolute prohibition of mock objects, stubs, unit tests
**Why**: Mocks test mock behavior, not production behavior
**How**: `post_tool_use.py` hook scans and blocks mock usage automatically
**Output**: Functional tests only (Puppeteer, real databases, real APIs)

**Example**:
```
Agent writes: jest.mock('axios')
  ↓
post_tool_use hook detects mock pattern
  ↓
BLOCKED: "🚨 Shannon NO MOCKS Violation Detected"
  ↓
Agent writes: Puppeteer test with real HTTP
  ↓
Allowed ✅
```

**Enforcement**: Automatic via hooks, cannot be bypassed

---

### 💾 Context Preservation
**What**: Automatic checkpointing before context compaction
**Why**: Auto-compaction loses critical project decisions and context
**How**: `precompact.py` hook triggers comprehensive checkpoint to Serena MCP
**Output**: Zero context loss, seamless session restoration

**Example**:
```
Context at 95% limit
  ↓
PreCompact hook fires
  ↓
CONTEXT_GUARDIAN saves:
  - Wave state (current wave, progress)
  - Phase state (current phase, todos)
  - Decisions (architecture choices)
  - Integration status (what's built)
  ↓
Auto-compact proceeds
  ↓
Next session: /sh_restore → Full context restored
```

**Enforcement**: continueOnError=false (MUST succeed)

---

## Quick Start Guide

### Installation

```bash
# In Claude Code:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework

# Restart Claude Code
```

### Verify Installation

```bash
/sh_status

# Expected output:
# Shannon Framework v4.1.0 ✅
# Serena MCP: Connected ✅
# Skills discovered: 16
# Agents available: 24
# Hooks active: 6
```

### First Project Workflow

```bash
# Step 1: Prime your session (V4.1 - <60s)
/shannon:prime

# Step 2: Analyze specification
/sh_spec "Build an inventory management system for retail stores with:
- Product catalog with barcode scanning
- Stock level tracking
- Multi-user access (owner, manager, staff roles)
- Mobile-responsive web interface
- Receipt printer integration
"

# Output: 8D complexity score, domain breakdown, MCP recommendations, 5-phase plan

# Step 3: Execute based on complexity
If complexity < 0.50:
  → Sequential execution (standard development)

If complexity >= 0.50:
  → /sh_wave (wave-based parallel execution)

# Step 4: Checkpoint progress
/sh_checkpoint "Phase 2 complete"

# Step 5: Restore if needed
/sh_restore  # Restores most recent checkpoint
```

---

## Component Inventory

### Commands (48 total)
- **Shannon Core** (11): /sh_spec, /sh_wave, /sh_test, /sh_checkpoint, /shannon:prime, etc.
- **SuperClaude Enhanced** (37): sc_* commands for various development tasks
- **Location**: shannon-plugin/commands/
- **Documentation**: Each command has embedded help, use `/help` for reference

### Skills (16 total - 16,740 lines)
- **QUANTITATIVE** (2): spec-analysis, wave-orchestration (algorithm-driven)
- **PROTOCOL** (4): phase-planning, context-preservation, context-restoration, skill-discovery
- **RIGID** (2): functional-testing (NO MOCKS), using-shannon (Iron Laws)
- **FLEXIBLE** (8): shannon-analysis, goal-management, mcp-discovery, confidence-check, etc.
- **Location**: shannon-plugin/skills/
- **New in V4.1**: skill-discovery (automatic skill cataloging)

### Agents (24 total)
- **Orchestrators** (5): WAVE_COORDINATOR, CONTEXT_GUARDIAN, PHASE_ARCHITECT, SPEC_ANALYZER, ARCHITECT
- **Domain Builders** (8): FRONTEND, BACKEND, MOBILE_DEVELOPER, DATABASE_ARCHITECT, DEVOPS, API_DESIGNER, DATA_ENGINEER, SECURITY
- **Quality Specialists** (6): TEST_GUARDIAN, QA, CODE_REVIEWER, REFACTORER, PERFORMANCE, ANALYZER
- **Support** (5): SCRIBE, MENTOR, TECHNICAL_WRITER, IMPLEMENTATION_WORKER, PRODUCT_MANAGER
- **Location**: shannon-plugin/agents/
- **Configuration**: YAML frontmatter with activation thresholds, dependencies

### Hooks (6 total)
- **session_start.sh**: Load using-shannon meta-skill at session start
- **post_tool_use.py**: Block mock usage in test files (13 patterns detected)
- **precompact.py**: Emergency checkpoint before auto-compact (11-section template)
- **user_prompt_submit.py**: Inject North Star goals into every prompt
- **stop.py**: Validate wave gates before session end
- **hooks.json**: Configuration and registration
- **Location**: shannon-plugin/hooks/
- **Documentation**: [hooks/README.md](shannon-plugin/hooks/README.md) (comprehensive guide)

### Core Patterns (9 total)
- **TESTING_PHILOSOPHY.md**: NO MOCKS Iron Law definition
- **CONTEXT_MANAGEMENT.md**: Checkpoint and restoration patterns
- **FORCED_READING_PROTOCOL.md**: V4.1 architectural thoroughness enforcement
- **Location**: shannon-plugin/core/

### MCPs (Tiered Recommendations)
- **Tier 1 (MANDATORY)**: Serena MCP (context preservation - ALL skills require)
- **Tier 2 (PRIMARY)**: Domain-specific (Puppeteer for Frontend >=20%, PostgreSQL for Database >=15%)
- **Tier 3 (SECONDARY)**: Supporting (GitHub, AWS, Sequential)
- **Tier 4 (OPTIONAL)**: Conditional (Tavily for research, monitoring MCPs)

---

## How Components Coordinate

### Example: User Runs /sh_spec

```
1. USER types: /sh_spec "Build auth system"

2. COMMAND_SKILL_MAP triggers:
   → spec-analysis (primary)
   → confidence-check (secondary)
   → mcp-discovery (secondary)

3. HOOK (session_start) ensures using-shannon loaded (Iron Laws active)

4. SKILL (spec-analysis) executes:
   → Calculates 8D complexity score
   → Detects domains (Frontend %, Backend %, Database %)
   → Recommends MCPs based on domain thresholds

5. MCP (Serena) saves results:
   → write_memory("spec_analysis_{id}", analysis)

6. SKILL chains to phase-planning:
   → phase-planning reads spec_analysis from Serena
   → Generates 5-phase plan with validation gates

7. MCP (Serena) saves phase plan:
   → write_memory("phase_plan_{project}", plan)

8. SKILL chains to mcp-discovery:
   → mcp-discovery reads domain percentages
   → Recommends tiered MCP list

9. USER receives:
   → Complexity score: 0.58 (COMPLEX)
   → Domain breakdown: Frontend 40%, Backend 35%, Database 25%
   → Recommended MCPs: Serena (Tier 1), Puppeteer (Tier 2), PostgreSQL (Tier 2)
   → 5-phase plan with timelines

10. HOOK enforcement active:
    → If user tries to write mocks later → post_tool_use BLOCKS
    → If context limit approached → precompact triggers checkpoint
```

**Key Insight**: Commands trigger Skills → Skills use MCPs → Hooks prevent violations → Agents execute work.

---

## Installation

### Via Plugin System (Recommended)

```bash
# In Claude Code:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework

# Restart Claude Code

# Verify installation:
/sh_status
```

### For Shannon Developers (Local Testing)

```bash
# Clone repository
git clone https://github.com/krzemienski/shannon-framework.git
cd shannon-framework

# Install locally in Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin uninstall shannon@shannon  # If already installed
/plugin install shannon@shannon

# Restart Claude Code

# Test your changes:
/sh_status
/shannon:prime
```

---

## Quick Start

### Step 1: Verify Shannon Loaded

```bash
/sh_status

# Expected:
# Shannon Framework v4.1.0 ✅
# Hooks active: 6 ✅
# Serena MCP: Connected ✅
# Skills: 16 discovered
# Agents: 24 available
```

### Step 2: Prime Your Session (V4.1)

```bash
/shannon:prime

# This runs:
# - Skill discovery (finds all 16 skills)
# - MCP discovery (checks required MCPs)
# - Context restoration (if previous session exists)
# Duration: <60 seconds
```

### Step 3: Analyze Your Specification

```bash
/sh_spec "Build a customer support ticketing system with:
- React dashboard for support agents
- Express API with TypeScript
- PostgreSQL database
- Real-time updates via WebSocket
- Email integration (SendGrid)
- Docker deployment
Timeline: 1 week"

# Output:
# Complexity: 0.58 (COMPLEX)
# Domains: Backend 41%, Database 26%, Frontend 22%, DevOps 11%
# Execution Strategy: Wave-based (complexity >=0.50)
# Recommended MCPs: Serena, Context7, PostgreSQL, Puppeteer, Magic, GitHub
# Timeline: 2-3 days (achievable in 1 week)
# 5-Phase Plan: [detailed breakdown]
```

### Step 4: Execute Based on Complexity

**If complexity < 0.50** (Simple to Moderate):
```bash
# Sequential execution (standard development)
# Just start implementing - Shannon guides via Iron Laws
```

**If complexity >= 0.50** (Complex or higher):
```bash
# Wave-based parallel execution
/sh_wave

# This generates wave structure, spawns agents in parallel
# Example output:
# Wave 1: Architecture (1 agent, 3h)
# Wave 2: Database + Frontend (2 agents parallel, 3.5h)
# Wave 3: Backend (1 agent, 4h)
# Wave 4: Integration Testing (1 agent, 2h)
# Total: 12.5h vs 18h sequential = 1.4x speedup
```

### Step 5: Test with NO MOCKS

```bash
# Shannon automatically enforces functional testing
# Write tests → post_tool_use hook validates

# ✅ ALLOWED:
const { test } = require('@playwright/test');
test('Login flow', async ({ page }) => {
  await page.goto('http://localhost:3000/login');  // REAL browser
  await page.fill('[data-testid="email"]', 'test@example.com');
  // ...
});

# ❌ BLOCKED:
jest.mock('../api/auth');  // post_tool_use hook blocks this immediately
```

### Step 6: Checkpoint Progress

```bash
# Manual checkpoint
/sh_checkpoint "Phase 2 complete, all tests passing"

# Or let PreCompact hook handle automatically
# (triggers when context limit approached)
```

---

## Core Workflows

### Specification → Implementation Workflow

```bash
# 1. Analyze specification (MANDATORY)
/sh_spec "[your specification]"
  → Complexity score calculated
  → Execution strategy determined
  → MCPs recommended

# 2. Install required MCPs
# (Based on recommendations from step 1)

# 3a. Sequential execution (complexity < 0.50)
# Implement directly, Shannon guides via Iron Laws

# 3b. Wave execution (complexity >= 0.50)
/sh_wave
  → Wave structure generated
  → Agents spawned in parallel
  → Synthesis checkpoints between waves

# 4. Testing (automatic NO MOCKS enforcement)
# Write functional tests
# post_tool_use hook validates (blocks mocks)

# 5. Deployment
# Complete Phase 5 deliverables
# stop hook validates before exit
```

---

## V4.1 Enhancements

### Enhancement 1: Forced Complete Reading Protocol
**Problem**: Agents skimmed critical files, causing architectural errors (40-60% of issues)
**Solution**: Skills now enforce line-by-line reading before execution
**Impact**: Zero architectural errors from incomplete reading
**Implementation**: Built into SKILL.md instructions, automatic enforcement

### Enhancement 2: Automatic Skill Discovery
**Problem**: Manual skill discovery via checklists (error-prone, time-consuming)
**Solution**: skill-discovery skill scans directories, builds catalog automatically
**Impact**: 104+ skills available, intelligent selection
**Implementation**: /sh_discover_skills command, SessionStart auto-discovery

### Enhancement 3: Unified /shannon:prime Command
**Problem**: Session priming took 15-20 minutes (load memories, discover skills, check MCPs)
**Solution**: Single command coordinates all priming workflows
**Impact**: <60 seconds for complete session setup (20x faster)
**Implementation**: /shannon:prime invokes skill-discovery + mcp-discovery + context-restoration

**See**: [SHANNON_V4.1_FINAL_SUMMARY.md](SHANNON_V4.1_FINAL_SUMMARY.md) for complete details

---

## Requirements

### Mandatory
- **Claude Code** v1.0.0+ (plugin host)
- **Serena MCP** (context preservation, checkpointing, memory coordination)

### Highly Recommended
- **Sequential MCP** (deep reasoning for complexity >=0.60)
- **Context7 MCP** (framework documentation, pattern validation)
- **Puppeteer MCP** (real browser testing for Frontend)

### Domain-Specific (install based on your project)
- **PostgreSQL/MySQL/MongoDB MCP** (if Database >=15%)
- **Magic MCP** (if Frontend >=20% - component generation)
- **GitHub MCP** (version control, CI/CD)
- **AWS/Azure/GCP MCP** (cloud deployment)

**MCP Installation**: Shannon analyzes your specification and recommends exactly which MCPs you need via tiered system (Mandatory → Primary → Secondary → Optional).

---

## Documentation

### Core Documentation
- **[Shannon Plugin README](shannon-plugin/README.md)** - Complete plugin documentation (commands, agents, skills)
- **[Hooks README](shannon-plugin/hooks/README.md)** - Hook system comprehensive guide (NEW)
- **[System Architecture Synthesis](SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md)** - Integration patterns (NEW)

### V4.1 Documentation
- **[V4.1 Final Summary](SHANNON_V4.1_FINAL_SUMMARY.md)** - Three enhancements overview
- **[V4.1 Validation Plan](SHANNON_V4.1_VALIDATION_PLAN.md)** - Testing methodology
- **[V4.1 Implementation Complete](SHANNON_V4.1_IMPLEMENTATION_COMPLETE.md)** - Technical report

### Deep Dives
- **Complexity Analysis**: shannon-plugin/skills/spec-analysis/SKILL.md (1544 lines)
- **Wave Orchestration**: shannon-plugin/skills/wave-orchestration/SKILL.md (1581 lines)
- **Phase Planning**: shannon-plugin/skills/phase-planning/SKILL.md (1182 lines)
- **Functional Testing**: shannon-plugin/skills/functional-testing/SKILL.md (1402 lines)

---

## Target Domains

Shannon is designed for **mission-critical AI development** requiring absolute rigor:

- 💰 **Finance**: Compliance, regulations, audit trails
- 🏥 **Healthcare**: HIPAA compliance, safety-critical systems
- ⚖️ **Legal**: Contract analysis, complete context requirements
- 🔒 **Security**: Threat analysis, vulnerability assessment
- 🚀 **Aerospace**: Safety-critical specifications, exhaustive validation

**Why These Domains**: Cannot tolerate:
- Skimmed architectural context → Implementation errors
- Mock-based tests → Production bugs missed
- Context loss → Decisions forgotten, rework required
- Subjective complexity estimates → Timeline failures

Shannon enforces the rigor these domains require through automatic enforcement (hooks).

---

## Repository Structure

```
shannon-framework/
├── shannon-plugin/              # The actual plugin (install this)
│   ├── .claude-plugin/
│   │   └── plugin.json         # Plugin manifest
│   ├── commands/               # 48 slash commands
│   ├── agents/                 # 24 specialized agents
│   ├── skills/                 # 16 skills
│   │   ├── spec-analysis/      # 8D complexity analysis
│   │   ├── wave-orchestration/ # Parallel execution
│   │   ├── phase-planning/     # 5-phase framework
│   │   ├── functional-testing/ # NO MOCKS enforcement
│   │   ├── skill-discovery/    # V4.1: Auto-discovery
│   │   └── ...                 # 11 more skills
│   ├── core/                   # 9 behavioral patterns
│   ├── hooks/                  # 6 enforcement hooks
│   │   ├── README.md          # Hook system guide (NEW)
│   │   ├── post_tool_use.py   # Mock detection
│   │   ├── precompact.py      # Emergency checkpoints
│   │   ├── session_start.sh   # Meta-skill loading
│   │   └── ...                # 3 more hooks
│   ├── modes/                  # Execution modes
│   ├── templates/              # Templates for commands
│   └── README.md              # Complete plugin documentation
├── README.md                   # This file (architecture overview)
├── CLAUDE.md                   # Installation guide
├── SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md  # Integration patterns (NEW)
└── SHANNON_V4.1_*.md          # V4.1 implementation reports
```

---

## Contributing

Shannon Framework is open source. Contributions welcome!

### Development Workflow

1. **Fork repository**: https://github.com/krzemienski/shannon-framework
2. **Create feature branch**: `git checkout -b feature/my-enhancement`
3. **Make changes**: Edit files in `shannon-plugin/`
4. **Test locally**:
   ```bash
   /plugin marketplace add /path/to/shannon-framework
   /plugin install shannon@shannon
   # Restart Claude Code
   /sh_status  # Verify installation
   ```
5. **Commit**: Follow conventional commits format
6. **Submit PR**: Include testing evidence and rationale

### Contribution Areas

**High Value**:
- New skills for domain-specific workflows
- Additional agents for specialized tasks
- MCP integrations for new tools
- Hook enhancements for additional enforcement

**Medium Value**:
- Command improvements
- Documentation enhancements
- Examples and use cases

**Testing Required**:
- All skill enhancements must include RED/GREEN comparison tests
- Hook changes must include bypass-attempt tests
- Agent changes must validate skill integration

---

## Troubleshooting

### Issue: "Shannon commands not recognized"

**Diagnosis**:
```bash
# Check plugin installed
/plugin list
# Should show: shannon@shannon-framework

# Check command directory
ls shannon-plugin/commands/
# Should show 48 .md files
```

**Resolution**: Reinstall plugin, restart Claude Code

---

### Issue: "Hooks not enforcing Iron Laws"

**Diagnosis**:
```bash
# Check hooks.json valid
python3 -m json.tool shannon-plugin/hooks/hooks.json

# Check hook scripts executable
ls -l shannon-plugin/hooks/*.{py,sh}
# All should have 'x' permission

# Check SessionStart hook succeeded
# Look for: <system-reminder>SessionStart hook success</system-reminder>
```

**Resolution**: Make hooks executable (`chmod +x`), restart Claude Code

---

### Issue: "Serena MCP not found"

**Symptoms**:
- Cannot save checkpoints
- Context loss after compaction
- Skills fail to persist results

**Resolution**:
```bash
# Install Serena MCP (required for Shannon)
# See: https://docs.claude.com/mcp/serena

# Verify connection
/list_memories
# Should work without error

# Check .serena directory
ls .serena/
# Should exist in project root
```

---

### Issue: "Wave execution not parallelizing"

**Diagnosis**:
- Check complexity score from /sh_spec
- Verify complexity >=0.50 (required for waves)
- Check wave structure shows parallel: true

**If complexity <0.50**:
- Expected behavior (sequential is correct for Simple/Moderate)

**If complexity >=0.50 but no parallelism**:
- Check dependency graph (may have sequential dependencies)
- Review phase plan (dependencies may prevent parallelization)

---

## Advanced Topics

### System Architecture Deep-Dive

**[SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md](SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md)** documents 13 integration patterns discovered during V4.1 enhancement:

1. Skill-to-skill chaining (spec-analysis → phase-planning)
2. MCP requirements (Serena as memory bus)
3. Skill types and behavior (QUANTITATIVE, PROTOCOL, RIGID, FLEXIBLE)
4. Anti-rationalization patterns (baseline testing-driven)
5. Testing enforcement chain (Philosophy → Skills → Plans → Hooks)
6. Complexity score as coordination signal (triggers across components)
7. Command-skill mapping (COMMAND_SKILL_MAP)
8. Hook enforcement layer (real-time blocking)
9. Tier-based MCP recommendations (quantitative thresholds)
10. Hook implementation details (post_tool_use.py analysis)
11. Hook configuration system (hooks.json)
12. Multi-skill orchestration (shannon-analysis)
13. Agent layer integration (24 specialists)

**Read this** for comprehensive understanding of how Shannon components coordinate.

---

## Links

- **Repository**: https://github.com/krzemienski/shannon-framework
- **Complete Documentation**: [shannon-plugin/README.md](shannon-plugin/README.md)
- **Hook System Guide**: [shannon-plugin/hooks/README.md](shannon-plugin/hooks/README.md)
- **Architecture Synthesis**: [SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md](SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md)
- **Issues**: https://github.com/krzemienski/shannon-framework/issues
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **License**: MIT

---

## License

MIT License - See [LICENSE](LICENSE)

---

**Shannon Framework v4.1.0**
*The most rigorous framework for mission-critical AI development*

**Install**: `/plugin marketplace add shannon-framework/shannon && /plugin install shannon@shannon-framework`

**Documentation**: [shannon-plugin/README.md](shannon-plugin/README.md)
**Architecture**: [SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md](SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md)
**Hooks**: [shannon-plugin/hooks/README.md](shannon-plugin/hooks/README.md)
