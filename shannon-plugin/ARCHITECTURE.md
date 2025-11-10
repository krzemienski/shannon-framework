# Shannon Framework V4.1 - Architecture

**Version**: 4.1.0
**Last Updated**: 2025-11-08

---

## System Architecture Overview

Shannon Framework is a **behavioral programming framework** that modifies Claude Code's decision-making through prompt injection, not code execution.

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE                              │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              SHANNON FRAMEWORK V4.1                    │ │
│  │                                                        │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │ Enhancement  │  │ Enhancement  │  │ Enhancement │ │ │
│  │  │     #1       │  │     #2       │  │     #3      │ │ │
│  │  │   Forced     │  │    Auto      │  │   Unified   │ │ │
│  │  │   Reading    │  │    Skill     │  │   /shannon: │ │ │
│  │  │   Protocol   │  │  Discovery   │  │    prime    │ │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘ │ │
│  │         │                 │                  │        │ │
│  │         └─────────────────┴──────────────────┘        │ │
│  │                           │                           │ │
│  │  ┌────────────────────────┴────────────────────────┐ │ │
│  │  │         SHANNON V4 BASE FRAMEWORK               │ │ │
│  │  │                                                 │ │ │
│  │  │  • 8D Complexity Analysis                      │ │ │
│  │  │  • Wave Orchestration (3.5x speedup)           │ │ │
│  │  │  • Context Preservation (Serena MCP)           │ │ │
│  │  │  • NO MOCKS Testing                            │ │ │
│  │  │  • 48 Commands, 26 Agents, 16 Skills           │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │                   MCP SERVERS                          ││
│  │  • Serena (REQUIRED) - Context preservation           ││
│  │  • Sequential (recommended) - Deep reasoning           ││
│  │  • Context7 (recommended) - Framework patterns         ││
│  │  • Puppeteer (recommended) - Browser testing           ││
│  └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Layer 1: Commands (User Interface)

```
User Input: /sh_spec "Build web app"
     ↓
┌────────────────────────┐
│  Command Layer         │
│  (/sh_spec)            │
│  - Validate input      │
│  - Invoke skills       │
│  - Format output       │
└────────┬───────────────┘
         ↓
```

**48 Commands Total**:
- **Shannon (sh_*)**: 13 core commands
- **Shannon V4.1**: 1 new unified command (shannon_prime)

### Layer 2: Skills (Business Logic)

```
Command invokes skills
     ↓
┌────────────────────────┐
│  Skill Layer           │
│  (@skill spec-analysis)│
│  - 8D algorithm        │
│  - Domain detection    │
│  - MCP recommendations │
└────────┬───────────────┘
         ↓
```

**16 Skills Total**:
- **Core Skills**: spec-analysis, wave-orchestration, phase-planning
- **Context Skills**: context-preservation, context-restoration, memory-coordination
- **Testing Skills**: functional-testing, confidence-check
- **V4.1 NEW**: skill-discovery (auto-discovery + invocation)
- **Meta Skill**: using-shannon (enforces workflows)

### Layer 3: Agents (Specialized Execution)

```
Skills may spawn agents
     ↓
┌────────────────────────┐
│  Agent Layer           │
│  (SPEC_ANALYZER)       │
│  - Specialized prompts │
│  - Domain expertise    │
│  - Task execution      │
└────────┬───────────────┘
         ↓
```

**26 Agents Total**:
- **Orchestration**: WAVE_COORDINATOR, SPEC_ANALYZER, PHASE_ARCHITECT
- **Context**: CONTEXT_GUARDIAN
- **Testing**: TEST_GUARDIAN, QA
- **Development**: FRONTEND, BACKEND, MOBILE_DEVELOPER, etc.
- **Quality**: CODE_REVIEWER, PERFORMANCE, SECURITY
- **Documentation**: TECHNICAL_WRITER, SCRIBE

### Layer 4: Core Patterns (Behavioral Rules)

```
All layers reference core patterns
     ↓
┌────────────────────────┐
│  Core Pattern Layer    │
│  (SPEC_ANALYSIS.md)    │
│  - Behavioral rules    │
│  - Algorithms          │
│  - Protocols           │
└────────────────────────┘
```

**9 Core Patterns**:
1. SPEC_ANALYSIS.md - 8D complexity framework
2. WAVE_ORCHESTRATION.md - Multi-stage execution
3. PHASE_PLANNING.md - 5-phase structure
4. CONTEXT_MANAGEMENT.md - Checkpoint/restore patterns
5. TESTING_PHILOSOPHY.md - NO MOCKS enforcement
6. HOOK_SYSTEM.md - Hook lifecycle
7. PROJECT_MEMORY.md - Serena integration
8. MCP_DISCOVERY.md - Dynamic MCP recommendations
9. **FORCED_READING_PROTOCOL.md** - V4.1 NEW

### Layer 5: Hooks (Event Automation)

```
Claude Code events trigger hooks
     ↓
┌────────────────────────┐
│  Hook Layer            │
│  (PreCompact)          │
│  - Auto-checkpointing  │
│  - NO MOCKS enforcement│
│  - Goal injection      │
└────────────────────────┘
```

**5 Hooks**:
1. **SessionStart**: Load using-shannon meta-skill
2. **PreCompact**: Auto-checkpoint before context compression
3. **PostToolUse**: Enforce NO MOCKS in test files
4. **Stop**: Validate wave gates before completion
5. **UserPromptSubmit**: Inject North Star goal

---

## Data Flow Architecture

### Typical Workflow: Specification Analysis

```
1. User Input
   /sh_spec "Build e-commerce platform"
           ↓
2. Command (sh_spec.md)
   - Validates input
   - Checks for forced reading trigger
   - Invokes spec-analysis skill
           ↓
3. Skill (spec-analysis/SKILL.md)
   - If file attached: Apply FORCED_READING_PROTOCOL
   - Parse specification text
   - Apply 8D complexity algorithm
   - Detect domains
   - Generate MCP recommendations
           ↓
4. Agent (SPEC_ANALYZER) - Optional for complex specs
   - Deep domain analysis
   - Timeline estimation
   - Risk assessment
           ↓
5. Output
   - Complexity score: 0.68 (COMPLEX)
   - 8D breakdown
   - Domain percentages
   - MCP recommendations
   - Wave plan (3 waves)
   - Timeline: 2-4 weeks
```

---

## V4.1 Enhancement Architecture

### Enhancement #1: Forced Reading Flow

```
Agent needs to read critical file
           ↓
FORCED_READING_PROTOCOL activated
           ↓
Step 1: PRE-COUNT
├─ Count total lines: 2,000
├─ Cache line count
└─ Output: "File has 2,000 lines"
           ↓
Step 2: SEQUENTIAL READING
├─ Read line 1
├─ Read line 2
├─ ...
├─ Read line 2,000
└─ Track lines_read: {1, 2, ..., 2000}
           ↓
Step 3: VERIFY COMPLETENESS
├─ Check: lines_read == total_lines?
├─ If YES: Enable synthesis
└─ If NO: BLOCK synthesis, show missing lines
           ↓
Step 4: SEQUENTIAL SYNTHESIS
├─ Use Sequential MCP
├─ Minimum 200 thoughts (for 2K line file)
└─ Present comprehensive analysis
```

**Result**: Guaranteed complete understanding (100% reading completeness)

### Enhancement #2: Skill Discovery Flow

```
Session Start or /sh_discover_skills command
           ↓
skill-discovery SKILL activated
           ↓
Step 1: SCAN DIRECTORIES
├─ Project: ./skills/*/SKILL.md
├─ User: ~/.claude/skills/*/SKILL.md
└─ Plugin: <plugins>/*/skills/*/SKILL.md
           ↓
Step 2: PARSE YAML FRONTMATTER
├─ Extract: name, description, type
├─ Extract: MCP requirements
├─ Extract: triggers from description
└─ Build SkillMetadata
           ↓
Step 3: BUILD CATALOG
├─ 104 skills found
├─ Project: 16, User: 88, Plugin: 0
└─ Cache (1 hour TTL)
           ↓
Step 4: INTELLIGENT SELECTION (when command executed)
├─ Calculate confidence (4 factors)
│  ├─ Trigger match: 40%
│  ├─ Command compat: 30%
│  ├─ Context relevance: 20%
│  └─ Deps satisfied: 10%
├─ Filter: confidence >=0.70
└─ Auto-invoke applicable skills
           ↓
Step 5: COMPLIANCE VERIFICATION
├─ Check: Did agent follow skill?
├─ Skill-specific checkers
│  ├─ spec-analysis: Look for 8D scoring
│  ├─ functional-testing: Check for mocks
│  └─ wave-orchestration: Check for SITREP
└─ Log violations
```

**Result**: 100% applicable skills found and invoked (vs ~70% manual)

### Enhancement #3: Shannon Prime Flow

```
User: /shannon:prime
           ↓
shannon_prime command activated
           ↓
8-Step Priming Sequence:

Step 1: MODE DETECTION
├─ Check for checkpoints
├─ If recent (<24h): auto-resume
└─ If none/old: fresh
           ↓
Step 2: SKILL INVENTORY (Enhancement #2)
├─ Run /sh_discover_skills
├─ Find all 104 skills
└─ Cache for fast access
           ↓
Step 3: MCP VERIFICATION
├─ Check Serena (REQUIRED)
├─ Check Sequential (recommended)
├─ Check Context7 (recommended)
└─ Check Puppeteer (recommended)
           ↓
Step 4: CONTEXT RESTORATION (if resume)
├─ Run /sh_restore --latest
├─ Load checkpoint data
└─ Restore wave progress
           ↓
Step 5: MEMORY LOADING
├─ Load relevant Serena memories
├─ Spec, plan, progress memories
└─ 8-15 memories typically
           ↓
Step 6: SPEC/PLAN RESTORATION
├─ Restore specification ID
├─ Restore current phase
└─ Restore next actions
           ↓
Step 7: THINKING PREPARATION
└─ Prepare Sequential MCP
           ↓
Step 8: FORCED READING ACTIVATION (Enhancement #1)
├─ Enable FORCED_READING_PROTOCOL
└─ Display: "Forced reading: ACTIVE"
           ↓
READINESS REPORT
├─ Mode, skills, MCPs, context, memories
├─ Current state, next actions
└─ Rules active

Total Time: <60 seconds
```

**Result**: Complete priming in <60s (vs 15-20 min manual)

---

## Integration Architecture

### How Three Enhancements Work Together

```
USER SESSION START
     ↓
/shannon:prime (Enhancement #3)
     ├─ Discovers skills (Enhancement #2)
     │  └─ Finds spec-analysis, wave-orchestration, etc.
     ├─ Activates forced reading (Enhancement #1)
     └─ Generates readiness report
     ↓
USER: /sh_spec @large-spec.md
     ├─ Enhancement #2: Auto-invokes spec-analysis skill
     ├─ Enhancement #1: Enforces complete reading (all 2,000 lines)
     └─ Produces high-quality 8D analysis
     ↓
USER: /sh_wave 1
     ├─ Enhancement #2: Auto-invokes wave-orchestration skill
     ├─ Enhancement #1: Enforces complete reading of wave plan
     └─ Executes wave with SITREP coordination
     ↓
RESULT: Maximum quality + efficiency
```

---

## Technology Stack

### Plugin Components

```
Shannon Plugin Structure:
├── Prompts (.md files)
│   ├── Commands: Workflow orchestration
│   ├── Skills: Reusable protocols
│   ├── Agents: Specialized prompts
│   └── Core: Behavioral patterns
├── Hooks (Python/Shell scripts)
│   └── Event automation
└── Configuration (JSON)
    └── plugin.json, hooks.json
```

**NOT a code library** - it's a prompt/behavior framework

### External Dependencies

**Required**:
- Claude Code >=1.0.0
- Serena MCP >=2.0.0 (context preservation)

**Recommended**:
- Sequential MCP >=1.0.0 (deep reasoning)
- Context7 MCP >=3.0.0 (framework patterns)
- Puppeteer MCP >=1.0.0 (browser testing)

---

## Complexity Analysis Architecture

### 8-Dimensional Framework

```
Specification Input
     ↓
Dimension Analyzers (Parallel):
├─ Structural (20% weight)
│  └─ File count, services, modules
├─ Cognitive (15% weight)
│  └─ Analysis verbs, design complexity
├─ Coordination (10% weight)
│  └─ Team size, communication needs
├─ Temporal (10% weight)
│  └─ Time dependencies, scheduling
├─ Technical (15% weight)
│  └─ Languages, frameworks, algorithms
├─ Scale (15% weight)
│  └─ Users, data volume, concurrency
├─ Uncertainty (15% weight)
│  └─ Unknown requirements, risks
└─ Dependencies (10% weight)
   └─ External services, integrations
     ↓
Weighted Sum Algorithm:
complexity = Σ(dimension_score × weight)
     ↓
Classification:
├─ 0.00-0.25: TRIVIAL
├─ 0.25-0.40: SIMPLE
├─ 0.40-0.60: MODERATE
├─ 0.60-0.75: COMPLEX
└─ 0.75-1.00: VERY COMPLEX / CRITICAL
     ↓
Output: Quantitative score + recommendations
```

---

## Wave Orchestration Architecture

### Wave Structure

```
Complex Project (complexity >=0.50)
     ↓
WAVE_COORDINATOR activates
     ↓
Wave Decomposition:
┌─────────────────────────────┐
│  Wave 1: Foundation         │
│  ├─ Phase 1: Setup          │
│  ├─ Phase 2: Core           │
│  └─ Phase 3: Integration    │
│      Duration: 1-2 weeks    │
└────────┬────────────────────┘
         ↓
┌─────────────────────────────┐
│  Wave 2: Features           │
│  ├─ Phase 1: Implementation │
│  ├─ Phase 2: Integration    │
│  └─ Phase 3: Testing        │
│      Duration: 1-2 weeks    │
└────────┬────────────────────┘
         ↓
┌─────────────────────────────┐
│  Wave 3: Optimization       │
│  ├─ Phase 1: Performance    │
│  ├─ Phase 2: Security       │
│  └─ Phase 3: Deployment     │
│      Duration: 1 week       │
└─────────────────────────────┘
```

### Multi-Agent Coordination

```
WAVE_COORDINATOR
     ├─ Spawns agents in parallel:
     │  ├─ FRONTEND (React components)
     │  ├─ BACKEND (API endpoints)
     │  ├─ DATABASE_ARCHITECT (Schema design)
     │  └─ SECURITY (Auth implementation)
     │
     ├─ SITREP protocol (complexity >=0.70):
     │  Each agent reports:
     │  ├─ SITUATION: Current state
     │  ├─ OBJECTIVES: Goals
     │  ├─ PROGRESS: % complete
     │  ├─ BLOCKERS: Issues
     │  └─ NEXT: Actions
     │
     └─ Coordination:
        ├─ Resolve blockers
        ├─ Prevent duplicate work
        └─ Optimize execution order

Result: 3.5x speedup via parallelization
```

---

## Context Preservation Architecture

### Checkpoint System

```
User works on project
     ↓
Context grows (specifications, decisions, progress)
     ↓
Context compaction trigger (~1M tokens)
     ↓
┌─────────────────────────────┐
│  PreCompact Hook            │
│  (automatic)                │
│  └─ Activates CONTEXT       │
│      _GUARDIAN agent         │
└────────┬────────────────────┘
         ↓
CONTEXT_GUARDIAN creates checkpoint:
├─ Specification text
├─ Complexity analysis
├─ North Star goal
├─ Wave progress
├─ Phase state
├─ Agent assignments
├─ Decisions made
├─ Memory references
└─ Next actions
     ↓
Save to Serena MCP:
mcp__serena__write_memory(
  "shannon_checkpoint_{timestamp}",
  checkpoint_data
)
     ↓
Context compaction proceeds safely
     ↓
Later: User runs /sh_restore or /shannon:prime
     ↓
100% context restored from checkpoint
```

**Result**: Zero information loss across sessions

---

## V4.1 Enhancement Integration

### Three Enhancements as Architectural Layers

```
┌─────────────────────────────────────────┐
│  Enhancement #3: Unified Prime          │
│  /shannon:prime orchestrates:           │
│  ├─ Skill discovery (Enhancement #2)   │
│  ├─ Forced reading activation (#1)     │
│  └─ Complete priming sequence          │
└────────┬────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Enhancement #2: Auto Skill Discovery   │
│  skill-discovery skill:                 │
│  ├─ Scans all directories              │
│  ├─ Builds catalog (104 skills)        │
│  ├─ Scores confidence (4 factors)      │
│  └─ Auto-invokes (>=0.70)              │
└────────┬────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Enhancement #1: Forced Reading         │
│  FORCED_READING_PROTOCOL:               │
│  ├─ Pre-count lines                    │
│  ├─ Read sequentially                  │
│  ├─ Verify completeness                │
│  └─ Sequential synthesis               │
└────────┬────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Shannon V4 Base                        │
│  8D analysis + Wave orchestration       │
│  + NO MOCKS + Context preservation      │
└─────────────────────────────────────────┘
```

**Integration**: Each enhancement builds on the layer below

---

## File Structure Architecture

```
shannon-plugin/
│
├── .claude-plugin/          # Plugin Metadata
│   └── plugin.json         # Manifest (defines plugin)
│
├── commands/                # User Interface Layer (14 commands)
│   ├── sh_spec.md         # Specification analysis
│   ├── sh_wave.md         # Wave execution
│   ├── shannon_prime.md   # V4.1: Unified priming ⭐
│   └── sh_discover_skills.md  # V4.1: Skill discovery ⭐
│
├── skills/                  # Business Logic Layer (17 skills)
│   ├── spec-analysis/      # 8D algorithm
│   ├── wave-orchestration/ # Multi-stage execution
│   ├── skill-discovery/    # V4.1: Auto-discovery ⭐
│   └── using-shannon/      # Meta-skill (enforces workflows)
│
├── agents/                  # Specialized Execution Layer (24 agents)
│   ├── SPEC_ANALYZER.md
│   ├── WAVE_COORDINATOR.md
│   └── ... (24 more)
│
├── core/                    # Behavioral Rules Layer (9 patterns)
│   ├── SPEC_ANALYSIS.md
│   ├── WAVE_ORCHESTRATION.md
│   ├── FORCED_READING_PROTOCOL.md  # V4.1: Reading enforcement ⭐
│   └── ... (6 more)
│
├── hooks/                   # Event Automation Layer
│   ├── hooks.json          # Hook configuration
│   ├── precompact.py       # Auto-checkpointing
│   ├── session_start.sh    # Load meta-skill
│   └── ... (3 more scripts)
│
├── modes/                   # Execution Mode Configurations
│   ├── WAVE_EXECUTION.md
│   └── SHANNON_INTEGRATION.md
│
└── templates/               # Command Templates
    └── wave_plan_template.md
```

---

## Behavioral Programming Model

**Shannon's Core Innovation**: Behavioral programming via markdown prompts

### Traditional Framework
```
Code execution → Behavior emerges
```

### Shannon Framework
```
Prompts define behavior → Claude follows prompts → Consistent behavior
```

**Example**:

**Traditional** (code):
```python
def analyze_spec(spec):
    return complexity_score(spec)
```

**Shannon** (prompt):
```markdown
## When analyzing specifications:
1. Parse specification text
2. Apply 8D complexity algorithm
3. Score each dimension (0.0-1.0)
4. Calculate weighted sum
5. Classify and recommend approach
```

**Advantage**: Prompts are:
- ✅ Inspectable (read the .md file)
- ✅ Modifiable (edit instructions)
- ✅ Portable (works across Claude instances)
- ✅ Transparent (see exactly what influences behavior)

**vs Code**:
- ❌ Opaque (compiled/bundled)
- ❌ Hard to modify (requires dev environment)
- ❌ Not portable (environment-dependent)

---

## Security & Isolation

```
Shannon Plugin Sandbox:
┌─────────────────────────────────┐
│  Shannon operates WITHIN        │
│  Claude Code's security model:  │
│                                 │
│  • No direct file system access│
│  • No network access           │
│  • Tools via Claude Code only  │
│  • MCP servers sandboxed       │
│                                 │
│  Shannon CANNOT:                │
│  • Execute arbitrary code       │
│  • Access user files directly   │
│  • Make network requests        │
│                                 │
│  Shannon CAN:                   │
│  • Provide prompts/instructions │
│  • Invoke Claude Code tools     │
│  • Use configured MCP servers   │
│  • Create checkpoints (via      │
│    Serena MCP)                  │
└─────────────────────────────────┘
```

**Security Model**: Shannon enhances Claude's behavior through prompts, doesn't bypass security

---

## Performance Architecture

### Token Efficiency

**Project Indexing** (94% compression):
```
Without indexing:
Read all files → 58,000 tokens

With project-indexing skill:
SHANNON_INDEX.md → 3,000 tokens
Compression: 94% (20x reduction)
```

**Skill Discovery Caching** (10x speedup):
```
Cold discovery: 50-100ms (scan + parse)
Warm cache: <10ms (retrieve from memory)
Improvement: 10x faster
```

**Wave Parallelization** (3.5x speedup):
```
Sequential execution: 4 weeks
Parallel wave execution: ~11 days
Speedup: 3.5x
```

---

## Deployment Architecture

```
Development:
/path/to/shannon-framework
└── shannon-plugin/
     ↓
Local Installation:
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon@shannon
     ↓
Installed Plugin:
~/.claude/plugins/shannon/
├── All plugin files copied
└── Registered with Claude Code
     ↓
Runtime:
Claude Code loads plugin
├── Registers 14 commands
├── Registers 24 agents
├── Loads 17 skills
├── Activates 5 hooks
└── Shannon behaviors active
```

---

## Scalability Architecture

**Designed for Projects**:
- Small (complexity <0.40): Direct implementation
- Medium (0.40-0.60): 2 waves
- Large (0.60-0.75): 3-4 waves
- Critical (0.75-1.00): 5-8 waves

**Scales via**:
- Wave decomposition (break into manageable chunks)
- Parallel agent execution (multiple agents per wave)
- Context preservation (no loss across sessions)
- Checkpoint/restore (resume anytime)

**Tested on**:
- Trivial projects (<10 files)
- Complex systems (100-500 files)
- Enterprise architectures (1000+ files)

---

**Shannon Framework V4.1** - Architecture designed for mission-critical rigor
