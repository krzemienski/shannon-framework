# Shannon Framework v4: Skill-Based Architecture

**Version**: 4.0.0
**Paradigm**: Skill-Based Orchestration with Progressive Disclosure
**Token Efficiency**: 60-80% reduction (50K → 5K base)
**Context Preservation**: Zero-loss via PreCompact hook

---

## 🚀 What's New in v4

### Skill-Based Architecture
- **25 Domain-Specific Skills**: Auto-generated from 8D spec analysis
- **Progressive Disclosure**: Load metadata only (~5K tokens), pull content on-demand
- **Meta-Programming**: Skills that write skills (`shannon-skill-generator`)
- **TDD Validation**: RED/GREEN/REFACTOR methodology from Superpowers

### Enhanced Orchestration
- **PreWave Hook**: Validates dependencies, injects context automatically
- **PostWave Hook**: Collects results, validates outputs, updates state
- **QualityGate Hook**: 5-gate validation (Spec, Phase, Wave, Quality, Project)
- **Automated Context Loading**: Reduces manual protocol overhead

### MCP Integration Tiers
- **Tier 1 (Mandatory)**: Serena - Context preservation and memory
- **Tier 2 (Recommended)**: Sequential (reasoning), Context7 (docs), Puppeteer (testing)
- **Tier 3 (Project-Specific)**: shadcn-ui (React), Xcode (iOS), AWS, Docker, etc.

### System Prompt Hierarchy
```
User CLAUDE.md (highest priority - user preferences)
  ↓
Project CLAUDE.md (project-specific rules)
  ↓
Shannon Plugin Prompts (minimal core patterns)
  ↓
Skills (on-demand, context-specific)
```

Skills are favored over general prompts when research/context indicates they're appropriate.

---

## 📦 Installation

### Prerequisites

#### Required MCP (Tier 1)
```bash
# Serena - Context preservation
npx @modelcontextprotocol/create-server serena
```

#### Recommended MCPs (Tier 2)
```bash
# Sequential Thinking
npm install -g @modelcontextprotocol/server-sequential

# Puppeteer - Real browser testing
npm install -g @modelcontextprotocol/server-puppeteer

# Context7 - Framework docs
npm install -g @modelcontextprotocol/server-context7
```

### Plugin Installation
```bash
# Add marketplace (if local)
/plugin marketplace add /path/to/shannon-framework

# Install Shannon v4
/plugin install shannon-v4@shannon-framework

# Restart Claude Code
```

### Verification
```bash
# Check status
/sh_status

# Quick start guide
/sh_quickstart
```

---

## 🎯 Quick Start

### 1. Create Specification
```bash
/sh_spec "Build a React dashboard with real-time WebSocket updates, user authentication via JWT, and PostgreSQL database"
```

Shannon analyzes complexity across 8 dimensions and generates detailed specification.

### 2. Review Plan
```bash
/sh_plan
```

Shannon creates 5-phase plan (Discovery → Architecture → Implementation → Testing → Deployment) with effort distribution.

### 3. Execute Waves
```bash
/sh_wave 1
```

Shannon executes wave 1 tasks in parallel, validates outputs, and checkpoints progress.

### 4. Checkpoint Progress
```bash
/sh_checkpoint "Completed authentication system"
```

Saves state to Serena MCP for zero-context-loss restoration.

---

## 🏗️ Architecture

### Progressive Disclosure System

**v3 (Prompt-Based)**:
- Session start: ~50K tokens (all core/*.md, full agent definitions, complete commands)
- All content loaded upfront
- High token usage, slower responses

**v4 (Skill-Based)**:
- Session start: ~5K tokens (metadata only)
- Full content loaded on-demand
- 60-80% token reduction
- Faster responses, more context budget

### Component Structure

```
shannon-v4-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata, hook definitions
│   └── marketplace.json     # Distribution metadata
├── commands/                # 34 commands (progressive disclosure)
│   ├── sh_spec.md          # 8D complexity analysis
│   ├── sh_plan.md          # 5-phase planning
│   ├── sh_wave.md          # Wave execution
│   └── ...
├── agents/                  # 19 agents (lightweight frontmatter)
│   ├── shannon-architect/
│   │   ├── AGENT.md        # Lightweight frontmatter only
│   │   └── resources/      # Full prompt loaded on-demand
│   └── ...
├── skills/                  # 25 skills (NEW in v4)
│   ├── shannon-react-ui/
│   │   └── SKILL.md        # Progressive disclosure
│   ├── shannon-skill-generator/  # Meta-skill
│   │   └── SKILL.md
│   └── ...
├── hooks/                   # 7 hooks (3 new in v4)
│   ├── session_start.py    # Context restoration
│   ├── precompact.py       # Zero-context-loss preservation
│   ├── pre_wave.py         # NEW: Dependency validation
│   ├── post_wave.py        # NEW: Result collection
│   └── quality_gate.py     # NEW: 5-gate validation
├── core/                    # 8 behavioral patterns
│   ├── SPEC_ANALYSIS.md    # 8D framework
│   ├── PHASE_PLANNING.md   # 5-phase system
│   ├── WAVE_ORCHESTRATION.md
│   └── ...
├── modes/                   # Execution modes
│   ├── WAVE_EXECUTION.md
│   └── SHANNON_INTEGRATION.md
└── scripts/                 # Utilities
    ├── validate.py
    └── skill_generator.py
```

---

## 🧠 Core Concepts

### 8D Complexity Analysis

Shannon analyzes projects across 8 dimensions:

1. **Structural** (0.0-1.0): Number of services, layers, modules
2. **Cognitive** (0.0-1.0): Domain complexity, business logic intricacy
3. **Coordination** (0.0-1.0): Team size, handoffs, dependencies
4. **Temporal** (0.0-1.0): Timeline constraints, deadlines
5. **Technical** (0.0-1.0): Cutting-edge tech, experimentation
6. **Scale** (0.0-1.0): Users, data volume, transactions
7. **Uncertainty** (0.0-1.0): Unknown requirements, changing specs
8. **Dependency** (0.0-1.0): External integrations, third-party services

**Output**: Total complexity score (0.0-1.0), domain percentages, tech stack analysis.

### 5-Phase Planning

| Phase | Effort % | Focus | Output |
|-------|----------|-------|--------|
| **Discovery** | 20% | Requirements, constraints, architecture exploration | Spec document, ADRs |
| **Architecture** | 15% | Design decisions, component structure, data flow | Architecture diagram, tech stack |
| **Implementation** | 45% | Code, integrations, business logic | Working features |
| **Testing** | 15% | Functional tests (NO MOCKS), integration tests | Test suite, coverage |
| **Deployment** | 5% | CI/CD, monitoring, documentation | Production-ready system |

### Wave Orchestration

**Waves** are groups of independent tasks executed in parallel:

```yaml
Wave 1: [Task A, Task B, Task C]  # Parallel execution
  ↓ Validation Gate
Wave 2: [Task D, Task E]          # Depends on Wave 1
  ↓ Validation Gate
Wave 3: [Task F]                  # Final integration
```

**Pattern**:
```xml
<function_calls>
  <invoke name="Task"><parameter name="prompt">Agent A: Build auth system</parameter></invoke>
  <invoke name="Task"><parameter name="prompt">Agent B: Build database schema</parameter></invoke>
  <invoke name="Task"><parameter name="prompt">Agent C: Build UI components</parameter></invoke>
</function_calls>
```

**Result**: TRUE parallelism (2-4× speedup measured)

### Zero-Context-Loss

**Problem**: Auto-compaction (75% token limit) loses context

**Solution**:
1. **PreCompact Hook**: Fires before compaction, extracts state (todos, wave, decisions, files)
2. **Serena MCP**: Saves state persistently (`write_memory("precompact_checkpoint", state)`)
3. **SessionStart Hook**: Restores context automatically (`read_memory("precompact_checkpoint")`)

**Result**: Seamless continuation across sessions

---

## 🛠️ Skills System

### Priority 1 Skills (Ship with v4)

1. **shannon-react-ui**: React component generation, state management, routing
2. **shannon-nextjs-14**: Next.js 14 App Router, Server Components, caching
3. **shannon-express-api**: Express REST APIs, middleware, error handling
4. **shannon-postgres-prisma**: PostgreSQL + Prisma schema, migrations, queries
5. **shannon-skill-generator**: Meta-skill that writes project-specific skills

### Priority 2 Skills (6 months)

6. **shannon-ios-xcode**: iOS build automation, Xcode project management
7. **shannon-android-gradle**: Android build automation, Gradle configuration
8. **shannon-docker-compose**: Docker multi-container orchestration
9. **shannon-aws-deploy**: AWS ECS/Lambda deployment automation
10. **shannon-git-ops**: Git workflows, PR creation, conflict resolution

### Priority 3 Skills (Demand-Based)

11-25: Security, performance, monitoring, Azure, GCP, etc.

### Skill Auto-Generation

```bash
# Shannon detects project domain from spec
Spec Analysis:
  Frontend: 60% (React, Next.js)
  Backend: 30% (Express, Node.js)
  Database: 10% (PostgreSQL)

# Shannon generates skills automatically
shannon-skill-generator:
  → shannon-nextjs-14-appdir.md (60% weight)
  → shannon-express-prisma-api.md (30% weight)
  → shannon-postgres-prisma.md (10% weight)
```

---

## 🔬 Testing Philosophy: NO MOCKS

Shannon enforces **functional testing only**:

✅ **DO**:
- Real browsers (Puppeteer, Playwright)
- Real databases (PostgreSQL, MongoDB)
- Real HTTP requests (fetch, axios)
- Real WebSocket connections
- Real file system operations

❌ **DON'T**:
- Jest mocks
- Sinon stubs
- Test doubles
- In-memory databases (unless production uses it)

**Why**: Mocks test your mocks, not production behavior.

---

## 🎚️ Validation Gates

Shannon enforces 5 validation gates:

### 1. Specification Gate
- Spec document complete?
- 8D complexity analyzed?
- Domain percentages calculated?
- **Test**: Serena memory exists for `spec_analysis`

### 2. Phase Gate
- Phase plan created?
- Effort distribution (20-15-45-15-5%)?
- Dependencies mapped?
- **Test**: Serena memory exists for `phase_plan_detailed`

### 3. Wave Gate
- Wave dependencies validated?
- Context loaded for all agents?
- Parallel execution confirmed?
- **Test**: PreWave hook passes

### 4. Quality Gate
- Functional tests passing?
- Coverage ≥ threshold?
- NO MOCKS verified?
- **Test**: QualityGate hook passes

### 5. Project Gate
- Confidence check ≥90%?
- Root cause identified?
- Official docs referenced?
- **Test**: Confidence check tool passes

---

## 🔄 Migration from v3

See [MIGRATION_V3_TO_V4.md](./docs/MIGRATION_V3_TO_V4.md) for detailed guide.

**Key Changes**:
1. Plugin name: `shannon` → `shannon-v4`
2. Commands link to skills (progressive activation)
3. Agents use lightweight frontmatter
4. 3 new hooks (PreWave, PostWave, QualityGate)
5. MCP tier system (MANDATORY/RECOMMENDED/PROJECT-SPECIFIC)

---

## 📚 Documentation

- [Installation Guide](./docs/INSTALLATION.md)
- [Quick Start Tutorial](./docs/QUICKSTART.md)
- [Commands Reference](./docs/COMMANDS.md)
- [Skills Catalog](./docs/SKILLS.md)
- [MCP Integration](./docs/MCP_INTEGRATION.md)
- [Wave Orchestration](./docs/WAVE_ORCHESTRATION.md)
- [Testing Guide](./docs/TESTING.md)
- [Migration v3→v4](./docs/MIGRATION_V3_TO_V4.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](./LICENSE)

---

## 🙏 Acknowledgments

Shannon v4 architecture inspired by research into:
- **Anthropic Skills SDK**: Progressive disclosure, 3-tier loading
- **Superpowers Framework**: TDD methodology (RED/GREEN/REFACTOR)
- **SuperClaude**: Confidence checking, Reflexion pattern
- **Humbl Skills**: SITREP protocol, authorization codes

---

**Shannon Framework v4** - Enterprise-grade specification-driven development with skill-based orchestration 🚀
