# Shannon Framework - Structural Map

**Generated**: 2025-01-12
**Purpose**: Complete structural overview of Shannon Framework plugin architecture
**Version Analyzed**: v5.0.0

---

## Executive Summary

Shannon Framework is a **Claude Code plugin** that enforces rigorous development practices through a multi-layer architectural system. The plugin is primarily **prompt-based** (not code-based), using markdown files to inject instructions and modify Claude's behavior.

**Core Architecture**: 4-layer enforcement pyramid
1. **Core Files** (Base Layer) - Always active, modify base behavior
2. **Hooks** (Automatic Layer) - Event-driven, cannot be skipped
3. **Skills** (Workflow Layer) - On-demand, enforce methodologies
4. **Commands** (Surface Layer) - User-facing entry points

**Scale**: 230+ markdown files, 18 skills, 15 commands, 9 core files, 8 hooks, 25 agent guides

---

## Directory Structure

```
shannon-framework/
├── .claude-plugin/           # Plugin manifest and configuration
│   └── plugin.json           # Name: shannon, Version: 5.0.0
│
├── commands/                 # 15 user-invocable slash commands
│   ├── analyze.md           # Shannon analysis workflow
│   ├── check_mcps.md        # MCP server discovery
│   ├── checkpoint.md        # Context checkpoint creation
│   ├── discover_skills.md   # Skill discovery and auto-invocation
│   ├── memory.md            # Project memory management
│   ├── north_star.md        # North Star goal definition
│   ├── prime.md             # Session priming protocol
│   ├── reflect.md           # Honest reflection workflow
│   ├── restore.md           # Context restoration
│   ├── scaffold.md          # Project scaffolding
│   ├── spec.md              # 8D specification analysis
│   ├── status.md            # Shannon status check
│   ├── task.md              # Task automation
│   ├── test.md              # Testing workflow
│   └── wave.md              # Wave orchestration
│
├── skills/                   # 18 reusable behavioral patterns
│   ├── confidence-check/     # Confidence verification before completion
│   ├── context-preservation/ # Context checkpoint management
│   ├── context-restoration/  # Session state restoration
│   ├── functional-testing/   # NO MOCKS testing enforcement
│   ├── goal-alignment/       # North Star alignment verification
│   ├── goal-management/      # Goal lifecycle management
│   ├── honest-reflections/   # Self-assessment and improvement
│   ├── mcp-discovery/        # MCP server discovery and integration
│   ├── memory-coordination/  # Memory system coordination
│   ├── phase-planning/       # Context-safe phase creation
│   ├── project-indexing/     # Codebase indexing and navigation
│   ├── shannon-analysis/     # Shannon-specific analysis workflow
│   ├── sitrep-reporting/     # Situation report generation
│   ├── skill-discovery/      # Automatic skill discovery and invocation
│   ├── spec-analysis/        # 8D complexity specification analysis
│   ├── task-automation/      # Task breakdown and automation
│   ├── using-shannon/        # Meta-skill for Shannon usage
│   ├── wave-orchestration/   # Parallel wave execution
│   └── README.md             # Skills overview
│
├── hooks/                    # 8 event-driven automation scripts
│   ├── hooks.json           # Hook configuration and lifecycle
│   ├── session_start.sh     # SessionStart: Load using-shannon meta-skill
│   ├── user_prompt_submit.py # UserPromptSubmit: Inject North Star + wave context
│   ├── post_tool_use.py     # PostToolUse: Block mock usage (NO MOCKS)
│   ├── precompact.py        # PreCompact: Context preservation checkpoint
│   ├── stop.py              # Stop: Wave validation gate enforcement
│   ├── README.md            # Hooks documentation
│   └── HOOK_VERIFICATION_RESULTS.md # Hook testing results
│
├── core/                     # 9 always-on behavioral pattern files
│   ├── CONTEXT_MANAGEMENT.md        # Context preservation patterns
│   ├── FORCED_READING_PROTOCOL.md   # Complete reading enforcement
│   ├── HOOK_SYSTEM.md               # Hook architecture and usage
│   ├── MCP_DISCOVERY.md             # MCP server discovery patterns
│   ├── PHASE_PLANNING.md            # Context-safe phase planning
│   ├── PROJECT_MEMORY.md            # Memory system architecture
│   ├── SPEC_ANALYSIS.md             # 8D complexity analysis methodology
│   ├── TESTING_PHILOSOPHY.md        # NO MOCKS testing philosophy
│   └── WAVE_ORCHESTRATION.md        # Parallel wave execution patterns
│
├── agents/                   # 25 guides for using Claude Code agents
│   ├── ANALYZER.md          # Code analysis agent guide
│   ├── ARCHITECT.md         # System architecture agent guide
│   ├── BACKEND.md           # Backend development agent guide
│   ├── CODE_REVIEWER.md     # Code review agent guide
│   ├── CONTEXT_GUARDIAN.md  # Context preservation agent guide
│   ├── DATA_ENGINEER.md     # Data engineering agent guide
│   ├── DATABASE_ARCHITECT.md # Database design agent guide
│   ├── DEVOPS.md            # DevOps agent guide
│   ├── FRONTEND.md          # Frontend development agent guide
│   ├── IMPLEMENTATION_WORKER.md # Implementation agent guide
│   ├── MENTOR.md            # Teaching/mentoring agent guide
│   ├── MOBILE_DEVELOPER.md  # Mobile development agent guide
│   ├── PERFORMANCE.md       # Performance optimization agent guide
│   ├── PHASE_ARCHITECT.md   # Phase planning agent guide
│   ├── PRODUCT_MANAGER.md   # Product management agent guide
│   ├── QA.md                # Quality assurance agent guide
│   ├── REFACTORER.md        # Refactoring agent guide
│   ├── SCRIBE.md            # Documentation agent guide
│   ├── SECURITY.md          # Security agent guide
│   ├── SPEC_ANALYZER.md     # Specification analysis agent guide
│   ├── TECHNICAL_WRITER.md  # Technical writing agent guide
│   ├── TEST_GUARDIAN.md     # Test enforcement agent guide
│   ├── WAVE_COORDINATOR.md  # Wave coordination agent guide
│   ├── guides/              # Additional agent guides
│   └── [2 more agent files]
│
├── docs/                     # Comprehensive documentation
│   ├── ref/                 # 17 reference documents (official Claude Code docs)
│   │   ├── claude-code-llms-full.txt
│   │   ├── claude-code-llms.txt
│   │   ├── code-claude-skills-LATEST.md
│   │   ├── code-claude-slash-commands-LATEST.md
│   │   ├── plugin-marketplaces-LATEST.md
│   │   ├── sdk-*.md (7 SDK documentation files)
│   │   └── *-spec.md (various specification files)
│   ├── guides/              # User and developer guides
│   │   ├── agents/          # Agent usage guides
│   │   └── commands/        # Command usage guides
│   ├── plans/               # Planning documents and session records
│   │   └── sessions/        # Historical session documentation
│   └── templates/           # Documentation templates
│
├── tests/                    # Testing and verification
│   ├── sdk-examples/        # Python SDK integration examples
│   └── verification-skill/  # Comprehensive verification framework
│       ├── inspection-lib/  # Inspection utilities
│       ├── flow-specs/      # Workflow specifications
│       ├── domain-verifiers/ # Domain-specific validators
│       └── scenarios/       # Test scenarios
│
├── modes/                    # 2 mode definition files
│   ├── SHANNON_INTEGRATION.md  # Shannon integration mode
│   └── WAVE_EXECUTION.md       # Wave execution mode
│
├── templates/                # 1 template file
│   └── SKILL_TEMPLATE.md    # Template for creating new skills
│
├── .serena/                  # Project memory system
│   └── memories/            # Serena MCP memory files
│
└── Root Level Files
    ├── README.md            # Main documentation (88KB - comprehensive)
    ├── CLAUDE.md            # Installation and development guide
    ├── CHANGELOG.md         # Version history
    ├── CONTRIBUTING.md      # Contribution guidelines
    ├── COMPLETE_AUDIT_REPORT.md        # Recent audit results
    ├── COMPLETE_FILE_INVENTORY.md      # File inventory documentation
    ├── COMPLETE_AUDIT_AND_CLEANUP_PLAN.md # Maintenance planning
    ├── validate_shannon_v5.py          # v5.0 validation script
    └── .gitignore           # Git ignore rules
```

---

## Component Inventory

### Commands (15 Total)
User-invocable slash commands following pattern: `/shannon:command_name`

| Command | Purpose |
|---------|---------|
| analyze | Shannon analysis workflow |
| check_mcps | MCP server discovery |
| checkpoint | Create context checkpoint |
| discover_skills | Discover and auto-invoke skills |
| memory | Project memory management |
| north_star | Define North Star goal |
| prime | Session priming protocol |
| reflect | Honest reflection workflow |
| restore | Restore context from checkpoint |
| scaffold | Project scaffolding |
| spec | 8D specification analysis |
| status | Shannon status check |
| task | Task automation |
| test | Testing workflow |
| wave | Wave orchestration |

**File Format**: Markdown (.md)
**Invocation**: Via SlashCommand tool → /shannon:command_name
**Mechanism**: Command file content expands into Claude's prompt

### Skills (18 Total)
Reusable behavioral patterns, each in its own directory with SKILL.md

| Skill | Category | Purpose |
|-------|----------|---------|
| using-shannon | Meta | Master skill for Shannon usage patterns |
| skill-discovery | Meta | Automatic skill discovery and invocation |
| spec-analysis | Planning | 8D complexity specification analysis |
| shannon-analysis | Planning | Shannon-specific analysis workflow |
| phase-planning | Planning | Context-safe phase creation |
| task-automation | Planning | Task breakdown and automation |
| wave-orchestration | Execution | Parallel wave execution management |
| functional-testing | Quality | NO MOCKS testing enforcement |
| confidence-check | Quality | Pre-completion confidence verification |
| honest-reflections | Quality | Self-assessment and improvement |
| goal-alignment | Process | North Star alignment verification |
| goal-management | Process | Goal lifecycle management |
| context-preservation | Context | Checkpoint creation and management |
| context-restoration | Context | Session state restoration |
| memory-coordination | Context | Memory system coordination |
| project-indexing | Navigation | Codebase indexing and search |
| sitrep-reporting | Reporting | Situation report generation |
| mcp-discovery | Integration | MCP server discovery patterns |

**File Format**: SKILL.md in named directory
**Invocation**: Via Skill tool or command expansion
**Mechanism**: Skill content loaded into context when invoked

### Hooks (8 Total)
Event-driven automation scripts with lifecycle triggers

| Hook | Event | Purpose | Timeout |
|------|-------|---------|---------|
| session_start.sh | SessionStart | Load using-shannon meta-skill | 5000ms |
| user_prompt_submit.py | UserPromptSubmit | Inject North Star + wave context | 2000ms |
| post_tool_use.py | PostToolUse (Write/Edit/MultiEdit) | Block mock usage | 3000ms |
| precompact.py | PreCompact | Create context checkpoint | 15000ms |
| stop.py | Stop | Enforce wave validation gates | 2000ms |
| hooks.json | N/A | Hook configuration manifest | N/A |

**File Formats**: Shell (.sh), Python (.py), JSON (.json)
**Execution**: Automatic on lifecycle events
**Mechanism**: Claude Code hook system (cannot be skipped by user)

### Core Files (9 Total)
Always-on behavioral pattern files loaded at plugin initialization

| Core File | Domain | Purpose |
|-----------|--------|---------|
| CONTEXT_MANAGEMENT.md | Context | Context preservation patterns |
| FORCED_READING_PROTOCOL.md | Quality | Complete reading enforcement |
| HOOK_SYSTEM.md | System | Hook architecture documentation |
| MCP_DISCOVERY.md | Integration | MCP server discovery patterns |
| PHASE_PLANNING.md | Planning | Context-safe phase methodology |
| PROJECT_MEMORY.md | Memory | Memory system architecture |
| SPEC_ANALYSIS.md | Analysis | 8D complexity methodology |
| TESTING_PHILOSOPHY.md | Quality | NO MOCKS testing philosophy |
| WAVE_ORCHESTRATION.md | Execution | Parallel wave patterns |

**File Format**: Markdown (.md)
**Loading**: Automatic at plugin initialization
**Mechanism**: Injected into Claude's base system prompt

### Agent Guides (25 Total)
Documentation for using Claude Code's built-in agents effectively

Organized by role:
- **Analysis**: ANALYZER, SPEC_ANALYZER
- **Architecture**: ARCHITECT, PHASE_ARCHITECT
- **Development**: BACKEND, FRONTEND, MOBILE_DEVELOPER, IMPLEMENTATION_WORKER
- **Data**: DATA_ENGINEER, DATABASE_ARCHITECT
- **Quality**: CODE_REVIEWER, QA, TEST_GUARDIAN, REFACTORER
- **Security**: SECURITY
- **Performance**: PERFORMANCE
- **DevOps**: DEVOPS
- **Documentation**: SCRIBE, TECHNICAL_WRITER, MENTOR
- **Management**: PRODUCT_MANAGER
- **Orchestration**: WAVE_COORDINATOR, CONTEXT_GUARDIAN

**File Format**: Markdown (.md)
**Purpose**: Guide Claude Code agent usage in Shannon methodology
**Type**: Documentation, not implementation

---

## File Statistics

### By Type
- **Markdown**: 230 files
- **Python**: ~5 files (hooks)
- **Shell**: 1 file (session_start.sh)
- **JSON**: 5 files (plugin.json, hooks.json, etc.)

### By Component
- **Commands**: 15 markdown files
- **Skills**: 18 directories, each with SKILL.md (+ examples, tests, references)
- **Core**: 9 markdown files
- **Hooks**: 5 Python scripts + 1 shell script + 1 JSON config
- **Agents**: 25 markdown guides
- **Documentation**: ~150+ markdown files (reference, guides, examples, tests)
- **Tests**: Multiple directories with verification framework
- **Memories**: Serena MCP memory files in .serena/memories/

### Documentation Depth
- **Reference docs**: 17 files in docs/ref/ (official Claude Code documentation)
- **Guides**: Multiple directories (agents/, commands/)
- **Examples**: Embedded in skills/ and tests/
- **Plans**: Historical session documentation in docs/plans/
- **Templates**: SKILL_TEMPLATE.md for creating new skills

---

## Plugin Manifest

**File**: `.claude-plugin/plugin.json`

```json
{
  "name": "shannon",
  "description": "Shannon Framework for mission-critical AI development with 8D complexity analysis and wave orchestration",
  "version": "5.0.0",
  "author": {
    "name": "Shannon Framework Team",
    "email": "info@shannon-framework.dev"
  },
  "homepage": "https://github.com/krzemienski/shannon-framework",
  "repository": "https://github.com/krzemienski/shannon-framework",
  "license": "MIT",
  "keywords": ["specification-analysis", "wave-orchestration", "testing", "complexity-scoring"]
}
```

**Key Capabilities** (from keywords):
1. **Specification Analysis**: 8D complexity scoring methodology
2. **Wave Orchestration**: Parallel task execution framework
3. **Testing**: NO MOCKS functional testing philosophy
4. **Complexity Scoring**: Multi-dimensional specification evaluation

---

## Hook System Architecture

**Configuration**: `hooks/hooks.json`

### Hook Lifecycle Events

```
SessionStart
    ↓
    session_start.sh → Loads using-shannon meta-skill

UserPromptSubmit (every prompt)
    ↓
    user_prompt_submit.py → Injects North Star + wave context

PostToolUse (after Write/Edit/MultiEdit)
    ↓
    post_tool_use.py → Blocks mock usage in tests

PreCompact (before auto-compression)
    ↓
    precompact.py → Creates context checkpoint (15s timeout)

Stop (session end)
    ↓
    stop.py → Enforces wave validation gates
```

### Hook Enforcement Mechanisms

1. **UserPromptSubmit**: Cannot be bypassed - injects context into EVERY prompt
2. **PostToolUse**: Matcher pattern `Write|Edit|MultiEdit` - blocks mock code
3. **PreCompact**: `continueOnError: false` - MUST succeed before compaction
4. **Stop**: Validation gates - blocks completion until satisfied
5. **SessionStart**: Auto-loads using-shannon - ensures Shannon patterns active

---

## Architecture Patterns

### Multi-Layer Enforcement Pyramid

```
                    User
                      │
                      ↓
        ┌─────────────────────────┐
        │   COMMANDS (Layer 4)    │ ← User-facing entry points
        │   15 slash commands     │    /shannon:spec, /shannon:prime, etc.
        └───────────┬─────────────┘
                    ↓
        ┌─────────────────────────┐
        │   SKILLS (Layer 3)      │ ← Workflow enforcement
        │   18 behavioral patterns│    TDD, NO MOCKS, phase planning
        └───────────┬─────────────┘
                    ↓
        ┌─────────────────────────┐
        │   HOOKS (Layer 2)       │ ← Automatic enforcement
        │   8 event-driven scripts│    Cannot be skipped
        └───────────┬─────────────┘
                    ↓
        ┌─────────────────────────┐
        │   CORE FILES (Layer 1)  │ ← Base behavior modification
        │   9 always-on patterns  │    Loaded at plugin init
        └─────────────────────────┘
```

### Component Interaction Model

```
Installation:
  1. Plugin manifest (plugin.json) registers Shannon
  2. Core files injected into base system prompt
  3. Commands registered as slash commands
  4. Skills available for invocation
  5. Hooks registered for lifecycle events

Invocation Flow:
  User → /shannon:spec
         ↓
  Command expands to prompt
         ↓
  Prompt invokes spec-analysis skill
         ↓
  Skill enforces 8D analysis workflow
         ↓
  UserPromptSubmit hook injects North Star context
         ↓
  PostToolUse hook blocks mocks if writing tests
         ↓
  Stop hook validates before completion
```

---

## Naming Conventions

### Commands
- **Format**: `{action}.md` (analyze.md, spec.md, prime.md)
- **Invocation**: `/shannon:{action}` (/shannon:spec, /shannon:prime)
- **Pattern**: Verb or noun describing the action

### Skills
- **Format**: `{name}/SKILL.md` (spec-analysis/SKILL.md)
- **Directory**: Kebab-case names (spec-analysis, phase-planning)
- **Invocation**: Via Skill tool or command expansion
- **Pattern**: Descriptive name indicating purpose

### Hooks
- **Format**: `{event_name}.{py|sh}` (session_start.sh, stop.py)
- **Pattern**: Lowercase snake_case matching lifecycle event

### Core Files
- **Format**: `{CONCEPT}.md` (TESTING_PHILOSOPHY.md)
- **Pattern**: UPPER_SNAKE_CASE, concept-focused names

### Agent Guides
- **Format**: `{ROLE}.md` (ANALYZER.md, ARCHITECT.md)
- **Pattern**: UPPERCASE, role-focused names

---

## File Organization Principles

### 1. Separation of Concerns
- **Plugin Components** (commands/, skills/, hooks/, core/) - Actual functionality
- **Documentation** (docs/, agents/) - Usage guides and references
- **Testing** (tests/) - Validation and verification
- **Development** (.claude/, .serena/) - Local development tooling

### 2. Component Co-location
Each skill directory contains:
- SKILL.md (main skill file)
- examples/ (usage examples)
- tests/ (skill-specific tests)
- references/ (supporting documentation)

This keeps related files together for easier navigation and maintenance.

### 3. Documentation Hierarchy
- **Top Level** (README.md, CLAUDE.md) - Entry points
- **Reference** (docs/ref/) - Official external documentation
- **Guides** (docs/guides/) - Usage documentation
- **Inline** (Component-specific README files) - Component documentation

### 4. Version Tracking
- **Plugin Version**: plugin.json (authoritative source)
- **Changelog**: CHANGELOG.md (version history)
- **Validation**: validate_shannon_v5.py (version-specific validation)
- **Documentation**: Version references in README, CLAUDE.md

---

## Repository Characteristics

### Scale Indicators
- **Total Files**: 230+ markdown files indicates mature, well-documented project
- **Component Ratio**: 15 commands : 18 skills : 9 core files suggests balanced architecture
- **Documentation Density**: ~10:1 documentation-to-implementation ratio (high)

### Architectural Sophistication
- **Multi-layer enforcement**: 4 distinct layers (core, hooks, skills, commands)
- **Event-driven automation**: 5 hook events covering full lifecycle
- **Reference-grounded**: 17 official documentation files maintained
- **Verification framework**: Dedicated testing infrastructure

### Maintenance Quality
- **Recent audits**: Complete audit report and cleanup plan present
- **Version validation**: Dedicated validation script (validate_shannon_v5.py)
- **Inventory tracking**: Complete file inventory maintained
- **Contributing guidelines**: Formal contribution process documented

---

## Key Architectural Insights (Phase 1)

### 1. Prompt-Based, Not Code-Based
Shannon is fundamentally a **prompt engineering framework**. Only 1 shell script and ~5 Python scripts exist - everything else is markdown-based instruction injection.

**Implication**: Shannon works by modifying how Claude THINKS, not by executing external code.

### 2. Multi-Layer Enforcement
Four distinct enforcement layers provide defense-in-depth:
- Core files: Can't be disabled (always loaded)
- Hooks: Can't be skipped (automatic firing)
- Skills: Must be followed (strong prompt enforcement)
- Commands: Entry points (user chooses when to invoke)

**Implication**: Shannon can enforce critical behaviors while allowing flexibility at higher layers.

### 3. Comprehensive Coverage
Components span entire development lifecycle:
- Specification → Planning → Execution → Testing → Reflection
- Context management throughout
- Quality gates at critical points
- Memory preservation across sessions

**Implication**: Shannon is a COMPLETE methodology, not a point solution.

### 4. Reference-Grounded Design
17 official Claude Code documentation files maintained in docs/ref/

**Implication**: Shannon's architecture is built on authoritative understanding of Claude Code capabilities, not speculation.

### 5. Quality-Focused
Multiple quality enforcement mechanisms:
- NO MOCKS testing philosophy (core + hook)
- Confidence checks before completion
- Honest reflections on work
- Wave validation gates
- Comprehensive verification framework

**Implication**: Shannon prioritizes correctness over speed.

---

## Navigation Guide

### For Users (Installation & Usage)
Start here:
1. `README.md` - Complete overview and usage guide
2. `CLAUDE.md` - Installation instructions
3. `/shannon:status` - Check installation
4. `/shannon:prime` - Start a Shannon session
5. `/shannon:discover_skills` - Find relevant skills

### For Developers (Contributing & Extending)
Start here:
1. `CONTRIBUTING.md` - Contribution guidelines
2. `.claude-plugin/plugin.json` - Plugin manifest
3. `templates/SKILL_TEMPLATE.md` - Create new skills
4. `tests/` - Validation framework
5. `validate_shannon_v5.py` - Version validation

### For Researchers (Understanding Architecture)
Start here:
1. This document (STRUCTURAL_MAP.md) - Structure overview
2. `core/` files - Core behavioral patterns
3. `hooks/hooks.json` - Hook system configuration
4. `docs/ref/` - Official Claude Code documentation
5. Individual component analysis docs (next phases)

---

## Questions for Next Phases

### Phase 2 (Reference Documentation)
- What are Claude Code's official plugin capabilities?
- How do skills, commands, and hooks work according to Anthropic?
- What can plugins enforce vs. what users can override?

### Phase 3 (Commands)
- Do commands use sh_* prefix in invocation but different names in files?
- Which commands invoke which skills?
- What do commands enforce directly vs. delegate to skills?

### Phase 4 (Skills)
- Which skills have checklists requiring TodoWrite?
- How do skills reference each other?
- What makes using-shannon a "meta-skill"?

### Phase 5 (Hooks)
- Why Python for most hooks but shell for session_start?
- How does post_tool_use detect mock usage?
- What are "wave validation gates" in stop.py?

### Phase 6 (Core)
- How are core files injected into system prompt?
- Do core files have priority/loading order?
- How do core files relate to skills with similar names?

### Phase 7-10
- Integration patterns, user experience, synthesis, documentation

---

## Phase 1 Completion Status

✅ **All Tasks Completed**:
- [x] Listed all top-level directories and their purposes
- [x] Counted and categorized all files by type
- [x] Identified entry points and manifest files
- [x] Mapped directory structure to plugin architecture components
- [x] Documented file naming conventions and patterns
- [x] Used sequential thinking (16 thoughts) to hypothesize about component relationships

✅ **All Verification Criteria Met**:
- [x] Complete directory tree documented
- [x] All file types identified and counted
- [x] Manifest/configuration files located
- [x] Component categories clearly defined
- [x] Structural map can guide subsequent phases

✅ **Exit Criteria Satisfied**:
Clear mental model of WHERE everything is and WHAT types of components exist. Ready to understand HOW they work in subsequent phases.

---

## Next Phase

**Phase 2: Reference Documentation Deep Dive**
- Read all 17 files in docs/ref/
- Build authoritative understanding of Claude Code plugin architecture
- Establish framework for analyzing Shannon's implementation
