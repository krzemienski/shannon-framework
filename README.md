# Shannon Framework V4

**Specification-Driven Development Framework for Claude Code**

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/shannon-framework/shannon)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Plugin](https://img.shields.io/badge/claude--code-plugin-purple.svg)](https://docs.claude.com/en/docs/claude-code/plugins)

Transform how you build software with quantitative complexity analysis, intelligent wave orchestration, and functional testing principles.

---

## 🚀 Quick Start

```bash
# 1. Add Shannon marketplace
/plugin marketplace add shannon-framework/shannon

# 2. Install Shannon V4
/plugin install shannon@shannon-framework

# 3. Restart Claude Code

# 4. Verify installation
/sh_status

# 5. Analyze your first specification
/sh_spec "Build REST API with user authentication and CRUD operations"
```

**Complete Installation Guide**: [docs/SHANNON_V4_USER_GUIDE.md](docs/SHANNON_V4_USER_GUIDE.md)

**Migrating from V3?**: [docs/SHANNON_V4_MIGRATION_GUIDE.md](docs/SHANNON_V4_MIGRATION_GUIDE.md) (< 5 minutes, 100% compatible)

---

## What's New in V4

### 🧩 Skill-Based Architecture
- **15 composable skills** - Reusable behavioral units
- **Modular design** - Skills compose to create workflows
- **Clear separation** - Each skill has single responsibility

### 🤖 Enhanced Agent System
- **19 specialized agents** - From 5 in V3 to 19 in V4
- **Domain expertise** - Frontend, Backend, Database, Mobile, DevOps, Security, etc.
- **Better coordination** - WAVE_COORDINATOR orchestrates multi-agent workflows

### 📊 8D Complexity Analysis
- **Quantitative scoring** - 0.0-1.0 scores across 8 dimensions
- **Domain detection** - Automatically identifies technical domains
- **Wave recommendations** - Suggests optimal project structure
- **MCP recommendations** - Identifies which MCPs will help

### 🌊 Wave Orchestration
- **Multi-stage execution** - Break complex projects into waves
- **Parallel execution** - Tasks execute in parallel where possible
- **Automatic checkpoints** - Zero context loss
- **Progress tracking** - Clear visibility into project status

### ✅ NO MOCKS Testing
- **Functional tests only** - Test real implementations, not mocks
- **Puppeteer integration** - Real browser testing
- **API testing** - Real HTTP requests
- **Test Guardian** - Enforces NO MOCKS principles

### 🔌 Enhanced MCP Integration
- **Automatic discovery** - `/sh_check_mcps` shows MCP status
- **Graceful degradation** - Works without optional MCPs
- **Fallback chains** - Seamless fallback to alternatives
- **Clear guidance** - Installation help for missing MCPs

---

## Core Concepts

### 8-Dimensional Complexity Analysis

Shannon analyzes specifications across 8 dimensions:

1. **Technical** - Language features, algorithms, architecture
2. **Temporal** - Time-dependent operations, scheduling
3. **Integration** - External APIs, third-party services
4. **Cognitive** - Domain knowledge, business logic complexity
5. **Environmental** - Deployment, infrastructure, configuration
6. **Data** - Data structures, transformations, persistence
7. **Scale** - Performance, concurrency, load handling
8. **Unknown** - Novel requirements, unclear specifications

**Output:** Overall complexity score (0.0-1.0) + dimension breakdown

```
Example Output:
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

Recommendation: Wave-based approach (3 waves, 14-21 days)
Domains: Backend (45%), Database (30%), Security (15%), API (10%)
```

---

### Wave-Based Execution

For complex projects (≥ 0.50 complexity), Shannon orchestrates work into waves:

```
Wave 1: Foundation
├─ Phase 1: Setup & Configuration
├─ Phase 2: Core Implementation
└─ Phase 3: Integration & Testing

Wave 2: Feature Development
├─ Phase 1: Feature Implementation
├─ Phase 2: Integration
└─ Phase 3: Testing & Documentation

Wave 3: Optimization & Deployment
├─ Phase 1: Performance Optimization
├─ Phase 2: Security Hardening
└─ Phase 3: Deployment & Monitoring
```

Each wave includes:
- Clear deliverables
- Agent assignments
- Duration estimates
- Automatic checkpoints

---

### Context Preservation

Shannon never loses context:

- **Checkpoints** - Save complete project state anytime
- **Restoration** - Restore 100% of context in new conversations
- **Serena MCP** - All state persists across sessions
- **Zero Manual Re-entry** - Never re-explain your project

```bash
# Create checkpoint
/sh_checkpoint "feature-complete"

# Later, in new conversation...
/sh_restore "feature-complete"
# Everything restored: spec, goals, progress, agents, memories
```

---

## Commands

### Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/sh_spec` | Analyze specification | `/sh_spec "Build e-commerce platform"` |
| `/sh_wave` | Execute development wave | `/sh_wave 1` |
| `/sh_checkpoint` | Save project state | `/sh_checkpoint "milestone-1"` |
| `/sh_restore` | Restore project state | `/sh_restore "milestone-1"` |
| `/sh_status` | Show project status | `/sh_status` |
| `/sh_north_star` | Set project goal | `/sh_north_star "Launch Q1"` |

### Utility Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/sh_check_mcps` | Check MCP status | `/sh_check_mcps` |
| `/sh_memory` | Manage memories | `/sh_memory --list` |
| `/sh_analyze` | Deep analysis | `/sh_analyze --domains` |
| `/sh_test` | Generate tests | `/sh_test --create --platform web` |
| `/sh_scaffold` | Generate scaffolding | `/sh_scaffold --framework react` |

**Complete Reference**: [docs/SHANNON_V4_COMMAND_REFERENCE.md](docs/SHANNON_V4_COMMAND_REFERENCE.md)

---

## Example Workflows

### Simple Project (< 0.50 complexity)

```bash
# 1. Analyze specification
/sh_spec "Build contact form with email validation"
# Output: Complexity 0.35 (SIMPLE)
# Recommendation: Direct implementation

# 2. Implement following guidance
# [Implement...]

# 3. Generate tests
/sh_test --create --platform web --feature "contact form"

# Done!
```

---

### Complex Project (≥ 0.50 complexity)

```bash
# 1. Analyze specification
/sh_spec "Build e-commerce platform with payments, inventory, order tracking"
# Output: Complexity 0.68 (COMPLEX)
# Recommendation: 3 waves, 14-21 days

# 2. Set north star goal
/sh_north_star "Launch MVP to 100 beta customers by Q1"

# 3. Create initial checkpoint
/sh_checkpoint "project-start"

# 4. Review wave 1 plan
/sh_wave 1 --plan
# Shows: Tasks, phases, agents, deliverables

# 5. Execute wave 1
/sh_wave 1
# WAVE_COORDINATOR activates
# Agents coordinate work
# Automatic checkpoint created

# 6. Check status
/sh_status
# Shows: Wave complete, next steps

# 7. Continue with wave 2
/sh_wave 2 --plan
/sh_wave 2

# 8. Create milestone checkpoint
/sh_checkpoint "mvp-complete"
```

---

## Skills

Shannon V4 includes 15 specialized skills:

### Core Skills
- **spec-analysis** - 8D complexity analysis
- **wave-orchestration** - Multi-stage execution
- **phase-planning** - 5-phase decomposition

### Context Skills
- **context-preservation** - Checkpoint creation
- **context-restoration** - State recovery
- **memory-coordination** - Serena MCP integration

### Testing Skills
- **functional-testing** - NO MOCKS test generation
- **confidence-check** - Readiness validation

### Analysis Skills
- **shannon-analysis** - Meta-analysis
- **project-indexing** - Structure analysis

### Support Skills
- **goal-management** - Goal tracking
- **goal-alignment** - Decision validation
- **mcp-discovery** - MCP recommendations
- **sitrep-reporting** - Status reporting
- **using-shannon** - User guidance

**Complete Reference**: [docs/SHANNON_V4_SKILL_REFERENCE.md](docs/SHANNON_V4_SKILL_REFERENCE.md)

---

## Agents

Shannon V4 includes 19 specialized agents:

### Core Agents
- WAVE_COORDINATOR - Orchestrates waves
- SPEC_ANALYZER - Analyzes specifications
- PHASE_ARCHITECT - Plans phases
- CONTEXT_GUARDIAN - Manages context
- TEST_GUARDIAN - Enforces NO MOCKS

### Domain Agents
- FRONTEND - Frontend development
- BACKEND - Backend services
- DATABASE_ARCHITECT - Database design
- MOBILE_DEVELOPER - Mobile apps
- DEVOPS - Infrastructure & deployment
- SECURITY - Security review
- PERFORMANCE_ENGINEER - Performance optimization
- QA_ENGINEER - Quality assurance
- DATA_ENGINEER - Data pipelines
- ARCHITECT - System architecture
- PRODUCT_MANAGER - Product strategy
- TECHNICAL_WRITER - Documentation
- API_DESIGNER - API design
- CODE_REVIEWER - Code quality

---

## Requirements

### Mandatory
- **Claude Code** >=1.0.0
- **Serena MCP** >=2.0.0 - Context preservation (required)

### Recommended
- **Sequential MCP** >=1.0.0 - Enhanced reasoning for complex specs
- **Puppeteer MCP** >=1.0.0 - Browser automation for testing
- **Context7 MCP** >=3.0.0 - Framework-specific patterns

Shannon works with Serena alone but benefits from optional MCPs.

---

## Documentation

### User Documentation
- **[User Guide](docs/SHANNON_V4_USER_GUIDE.md)** - Getting started, workflows, best practices
- **[Command Reference](docs/SHANNON_V4_COMMAND_REFERENCE.md)** - All commands with examples
- **[Skill Reference](docs/SHANNON_V4_SKILL_REFERENCE.md)** - All skills explained
- **[Migration Guide](docs/SHANNON_V4_MIGRATION_GUIDE.md)** - V3 → V4 migration (< 5 min)
- **[Troubleshooting](docs/SHANNON_V4_TROUBLESHOOTING.md)** - Common issues & solutions

### Technical Documentation
- **[Integration Tests](shannon-plugin/tests/integration_test_suite.md)** - Test scenarios
- **[Release Checklist](docs/RELEASE_CHECKLIST_V4.md)** - Release process
- **[Validation Results](shannon-plugin/tests/VALIDATION_RESULTS.md)** - Test results

---

## Philosophy

### Specification-Driven Development

Shannon starts with specifications, not code:

1. **Analyze** - Understand complexity quantitatively
2. **Plan** - Break into phases and waves
3. **Execute** - Coordinate agents and tasks
4. **Test** - Validate with functional tests
5. **Deliver** - Ship with confidence

### NO MOCKS Testing

Shannon rejects mock testing:

❌ **Mocks test mock behavior** - Not real behavior
✅ **Functional tests** - Test real implementations

Shannon generates:
- Real browser tests (Puppeteer MCP)
- Real API tests (actual HTTP)
- Real database tests (test instances)
- Real integration tests (actual services)

### Zero Context Loss

Shannon preserves all context:

- Specifications
- Complexity analysis
- Goals
- Wave progress
- Agent state
- Decisions
- Memories

Nothing is lost. Everything is recoverable.

---

## Backward Compatibility

Shannon V4 maintains **100% backward compatibility** with V3:

✅ All V3 commands work identically
✅ Same arguments and outputs
✅ V3 checkpoints work in V4
✅ V3 workflows unchanged
✅ No breaking changes
✅ < 5 minute migration

**Migration Guide**: [docs/SHANNON_V4_MIGRATION_GUIDE.md](docs/SHANNON_V4_MIGRATION_GUIDE.md)

---

## Version History

### V4.0.0 (2025-01-XX) - Current

**Major Features:**
- Skill-based architecture (15 skills)
- Enhanced agents (19 agents)
- 8D complexity analysis
- Wave orchestration
- NO MOCKS testing
- Enhanced MCP integration

**New Commands:**
- `/sh_check_mcps` - MCP status
- `/sh_analyze` - Deep analysis
- `/sh_test` - Test generation
- `/sh_scaffold` - Project scaffolding

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)

### V3.0.1 (2024-XX-XX)

- Plugin architecture
- 5 core agents
- Basic complexity analysis
- Checkpoint system

---

## Support

### Getting Help

- **Documentation**: All docs in `docs/` directory
- **Issues**: [GitHub Issues](https://github.com/shannon-framework/shannon/issues)
- **Community**: [Shannon Community](https://shannon-framework.dev/community)

### Troubleshooting

Common issues? Check:
1. `/sh_status` - Project status
2. `/sh_check_mcps` - MCP connections
3. [Troubleshooting Guide](docs/SHANNON_V4_TROUBLESHOOTING.md)

---

## Contributing

Shannon Framework is open source (MIT License).

Contributions welcome:
- Bug reports
- Feature requests
- Documentation improvements
- Code contributions

---

## License

MIT License - See [LICENSE](LICENSE) file.

---

## What Shannon Actually Is

Shannon is a **behavioral framework** that modifies how Claude Code thinks about development through system prompt injection.

**Shannon is not**:
- A code library
- A JavaScript framework
- A Python package

**Shannon is**:
- Behavioral programming via markdown
- System prompt engineering
- Decision framework injection

The markdown files ARE the framework - they modify Claude's decision-making, priorities, and execution patterns.

**Learn more**: [CLAUDE.md](CLAUDE.md) explains Shannon's behavioral programming paradigm.

---

**Shannon Framework V4** - Build better software with quantitative complexity analysis, intelligent orchestration, and functional testing principles.
