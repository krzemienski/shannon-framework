# Shannon Framework: System Architecture Synthesis

**Purpose**: Document how Skills, Commands, Hooks, MCPs, and Agents coordinate
**Status**: Living document - updated as patterns discovered during V4.1 enhancement
**Date**: 2025-11-08

---

## Discovered Integration Patterns

### Pattern 1: Skill → Skill Chaining (spec-analysis → phase-planning)

**Discovery**: spec-analysis skill references phase-planning as required sub-skill

**Integration Mechanism**:
```
spec-analysis SKILL.md (line 28):
  required-sub-skills:
    - phase-planning

Execution flow:
1. User: "Analyze this spec"
2. spec-analysis runs → generates complexity score, domain percentages
3. spec-analysis invokes phase-planning (via Skill tool)
4. phase-planning receives spec_analysis output as input
5. phase-planning generates 5-phase plan using complexity/domains
```

**Key Insight**: Skills declare dependencies in frontmatter. Execution is hierarchical.

---

### Pattern 2: MCP Requirements (Serena as Foundation)

**Discovery**: ALL 3 enhanced skills require Serena MCP

**Evidence**:
```yaml
# spec-analysis/SKILL.md
mcp-requirements:
  required:
    - name: serena
      purpose: Save analysis for cross-session retrieval

# wave-orchestration/SKILL.md
mcp-requirements:
  required:
    - name: serena
      purpose: Wave checkpoint storage

# phase-planning/SKILL.md
mcp-requirements:
  required:
    - name: serena
      purpose: Phase storage and retrieval
```

**Integration Points**:
- spec-analysis saves: `write_memory("spec_analysis_ID", analysis_json)`
- phase-planning reads: `read_memory("spec_analysis")`
- wave-orchestration reads: `read_memory("phase_plan")`, `read_memory("wave_N_complete")`

**Key Insight**: Serena MCP is Shannon's "shared memory bus" - all skills communicate through it.

---

### Pattern 3: Skill Types Determine Behavior

**Discovery**: Skills have `skill-type` frontmatter (QUANTITATIVE, PROTOCOL, RIGID)

**Observed Types**:
```
QUANTITATIVE: spec-analysis, wave-orchestration
  → Must follow algorithm precisely
  → Outputs are calculated, not inferred
  → Validation via numeric criteria

PROTOCOL: phase-planning, context-preservation
  → Defines processes and workflows
  → Enforces sequence and checkpoints
  → Behavior is procedural

RIGID: functional-testing, using-shannon
  → Iron Laws (non-negotiable)
  → Absolute rules enforced
  → No flexibility allowed
```

**Key Insight**: skill-type signals enforcement level. RIGID skills cannot be adapted.

---

### Pattern 4: Anti-Rationalization Sections (Baseline Testing-Driven)

**Discovery**: All 3 enhanced skills + using-shannon have anti-rationalization sections

**Pattern**:
```
1. Identified rationalization (from baseline testing)
2. Example of agent violating rule
3. Explicit COUNTER with detection signal
4. Rule restatement

Example from spec-analysis:
"Rationalization 1: 'User's assessment seems reasonable'"
→ COUNTER: "NEVER accept user's subjective score without running algorithm"
→ Rule: "Apply algorithm. User intuition doesn't override calculation."
```

**Integration with Hooks**:
- Hooks likely ENFORCE what anti-rationalization sections WARN about
- post_tool_use.py: Scans for mock violations (functional-testing anti-pattern)
- PreCompact hook: Forces checkpoints (context-preservation anti-pattern)

**Key Insight**: Skills document violations; Hooks prevent them.

---

### Pattern 5: Testing Philosophy Enforcement Chain

**Discovery**: NO MOCKS appears in multiple components

**Enforcement Chain**:
```
1. Core Document: shannon-plugin/core/TESTING_PHILOSOPHY.md (line 831 reference)
   → Defines Iron Law: No mocks, no unit tests, no stubs

2. functional-testing skill (RIGID type)
   → Provides implementation guidance for NO MOCKS
   → "Use real browsers, real databases, real APIs"

3. spec-analysis skill
   → Phase 4 planning: "Puppeteer tests for Frontend, real HTTP for Backend, real DB (NO MOCKS)"
   → Embeds NO MOCKS into generated plans

4. phase-planning skill
   → Validation gates: "NO MOCKS compliance verified" (line 1041)
   → Testing requirements enforce philosophy

5. post_tool_use.py hook (referenced in functional-testing)
   → AUTOMATIC SCANNING for mock imports
   → Blocks execution if violations detected
```

**Key Insight**: Philosophy → Skills → Plans → Hooks (4-layer enforcement)

---

### Pattern 6: Complexity Score as Coordination Signal

**Discovery**: Complexity score triggers different execution strategies across skills

**Trigger Thresholds**:
```
Complexity < 0.30 (Simple):
  → phase-planning: 3 phases
  → wave-orchestration: NOT USED (sequential execution)
  → spec-analysis: No Sequential MCP needed

Complexity 0.30-0.50 (Moderate):
  → phase-planning: 3-4 phases
  → wave-orchestration: OPTIONAL (if multi-domain)
  → spec-analysis: Standard analysis

Complexity >= 0.50 (Complex):
  → phase-planning: 5 phases
  → wave-orchestration: MANDATORY
  → spec-analysis: Consider Sequential MCP for deep analysis

Complexity >= 0.60:
  → spec-analysis: RECOMMEND Sequential MCP (100-500 reasoning steps)

Complexity >= 0.70 (High):
  → wave-orchestration: SITREP protocol recommended
  → phase-planning: Extended validation gates

Complexity >= 0.85 (Critical):
  → phase-planning: Risk mitigation phases added
  → wave-orchestration: 15-25 agents, 5-8 waves
```

**Key Insight**: Complexity score is Shannon's "central nervous system" - all skills read it to determine behavior.

---

### Pattern 7: Command-Skill Mapping System

**Discovery**: skill-discovery documents explicit command-to-skill mappings (lines 238-253)

**Mapping Table**:
```python
COMMAND_SKILL_MAP = {
  '/sh_spec': ['spec-analysis', 'confidence-check', 'mcp-discovery'],
  '/sh_analyze': ['shannon-analysis', 'project-indexing', 'confidence-check'],
  '/sh_wave': ['wave-orchestration', 'sitrep-reporting', 'context-preservation'],
  '/sh_test': ['functional-testing'],
  '/sh_checkpoint': ['context-preservation'],
  '/sh_restore': ['context-restoration'],
  '/shannon:prime': ['skill-discovery', 'mcp-discovery', 'context-restoration'],
}
```

**Execution Flow**:
```
User types: /sh_spec "Build auth system"
↓
Command dispatcher reads COMMAND_SKILL_MAP
↓
Auto-loads: spec-analysis (primary), confidence-check, mcp-discovery
↓
Skills execute with command context
↓
Results coordinated (spec-analysis → mcp-discovery uses domain %)
```

**Key Insight**: Commands are skill TRIGGERS, not implementations. Skills do the work.

---

### Pattern 8: Hook Enforcement Layer

**Discovery**: 6 hooks found in shannon-plugin/hooks/

**Hook Inventory**:
```bash
shannon-plugin/hooks/
├── hooks.json              (2,205 bytes) - Configuration/registration
├── session_start.sh        (425 bytes)   - Skill auto-loading
├── post_tool_use.py        (4,530 bytes) - Mock violation detection
├── precompact.py           (12,583 bytes) - Emergency checkpointing
├── user_prompt_submit.py   (2,182 bytes) - Input validation
└── stop.py                 (2,734 bytes)  - Session cleanup
```

**Hook Integration with Skills**:

**session_start.sh** → using-shannon skill:
- Hook triggers at session start
- Auto-loads using-shannon meta-skill
- Establishes Iron Laws before user interaction

**post_tool_use.py** → functional-testing skill:
- Referenced in functional-testing (line 29): "Integrated with post_tool_use.py hook"
- Scans tool results for mock imports
- BLOCKS execution if mocks detected
- Enforces NO MOCKS Iron Law automatically

**precompact.py** → context-preservation skill:
- Triggers when context near limit
- Forces checkpoint creation (emergency save)
- Referenced in context-preservation (line 48): "When PreCompact hook triggers"
- Prevents context loss automatically

**Key Insight**: Hooks are AUTOMATIC ENFORCERS. Skills document rules; hooks prevent violations.

---

### Pattern 9: Tier-Based MCP Recommendation Algorithm

**Discovery**: mcp-discovery implements quantitative domain → MCP tier mapping

**Tier Structure** (from mcp-discovery lines 59-64):
```
Tier 1 (MANDATORY):
  → Serena MCP (ALWAYS required)
  → Threshold: N/A (unconditional)

Tier 2 (PRIMARY):
  → Domain-specific MCPs
  → Threshold: domain >= 20%
  → Example: Frontend 40% → Puppeteer PRIMARY

Tier 3 (SECONDARY):
  → Supporting domain MCPs + universal tools
  → Threshold: domain >= 10% OR universal (GitHub)
  → Example: Database 15% → PostgreSQL SECONDARY

Tier 4 (OPTIONAL):
  → Keyword-triggered MCPs
  → Threshold: keyword presence (e.g., "research" → Tavily)
```

**Health Check System** (lines 203-220):
```
For each recommended MCP:
1. Provide health check command
2. Expected success/failure states
3. Fallback chain if missing
4. Degradation explanation
```

**Fallback Chains Example** (lines 221-237):
```
Puppeteer unavailable:
  → Playwright (equivalent capability)
  → Chrome DevTools (MCP integration but different API)
  → Manual Testing (no automation)
```

**Key Insight**: MCP recommendations are QUANTITATIVE (domain % thresholds), not subjective.

---

## Questions to Investigate

**Hooks** (PARTIALLY ANSWERED):
- [x] How does SessionStart hook trigger using-shannon skill? → session_start.sh auto-loads it
- [x] What does PreCompact hook do exactly? → Emergency checkpointing (12KB of logic)
- [x] How does post_tool_use.py detect mock violations? → Scans tool results for mock patterns
- [x] Are there other hooks? → YES: user_prompt_submit.py, stop.py (need investigation)

**Commands** (ANSWERED):
- [x] How do /sh_* commands relate to skills? → COMMAND_SKILL_MAP triggers skill auto-loading
- [x] Does /sh_spec invoke spec-analysis skill? → YES + confidence-check + mcp-discovery
- [x] What's the relationship? → Commands trigger skills, skills do work

### Pattern 10: Hook Implementation Details (POST_TOOL_USE.PY Analysis)

**Source**: shannon-plugin/hooks/post_tool_use.py (164 lines read)

**Hook Lifecycle**:
```
1. Tool executed (Write/Edit/MultiEdit)
   ↓
2. Hook fires (PostToolUse event)
   ↓
3. post_tool_use.py receives JSON:
   {
     "tool_name": "Write",
     "tool_input": {"file_path": "...", "content": "..."}
   }
   ↓
4. Hook logic:
   - Skip if not Write/Edit/MultiEdit → exit(0)
   - Skip if not test file → exit(0)
   - Scan content for 13 mock patterns → violations = detect_mocks()
   - If violations: return {"decision": "block", "reason": "..."} → BLOCKS TOOL
   - If clean: exit(0) → ALLOWS TOOL
   ↓
5. Claude Code enforces decision (blocks Write if hook says block)
```

**Mock Detection Patterns** (13 total):
```python
MOCK_PATTERNS = [
  (r'jest\.mock\(', 'jest.mock()'),
  (r'jest\.spyOn', 'jest.spyOn()'),
  (r'unittest\.mock', 'unittest.mock'),
  (r'from\s+unittest\.mock\s+import', 'unittest.mock imports'),
  (r'@[Mm]ock\b', '@Mock annotation'),
  (r'@[Pp]atch\b', '@patch decorator'),
  (r'sinon\.(stub|mock|fake|spy)', 'sinon mocking'),
  (r'mockImplementation', 'mockImplementation'),
  (r'mockReturnValue', 'mockReturnValue'),
  (r'createMock[^a-z]', 'createMock'),
  (r'MockedFunction', 'MockedFunction type'),
  (r'vi\.mock\(', 'vitest mock'),
  (r'TestDouble', 'TestDouble'),
]
```

**Test File Detection**:
```python
test_indicators = [
  '/test/', '/__tests__/', '/tests/',  # Directory patterns
  '.test.', '.spec.',                   # Extension patterns
  '_test.', '_spec.',                   # Name patterns
  'test_', 'spec_'                      # Prefix patterns
]
```

**Violation Response** (if mocks detected):
```json
{
  "decision": "block",
  "reason": "🚨 Shannon NO MOCKS Violation Detected

  **Violations**: jest.mock(), mockReturnValue

  **Required Actions**:
  1. Remove all mock usage
  2. Implement functional test using Puppeteer MCP

  **Quick Start**: Run /sh_check_mcps"
}
```

**Key Insight**: Hooks provide REAL-TIME enforcement. Skills document rules; hooks PREVENT violations DURING execution (not after).

---

### Pattern 11: Hook Configuration System (hooks.json)

**Discovery**: hooks.json orchestrates all hook registrations

**Hook Types**:
```json
{
  "UserPromptSubmit": [
    {
      "description": "Goal injection",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py",
        "timeout": 2000
      }]
    }
  ],

  "PreCompact": [  // Emergency save before context compaction
    "timeout": 15000,
    "continueOnError": false  // MUST NOT FAIL
  ],

  "PostToolUse": [  // Mock detection
    "matcher": "Write|Edit|MultiEdit",  // Only fire for file modifications
    "timeout": 3000
  ],

  "Stop": [  // Wave validation gate
    "timeout": 2000
  ],

  "SessionStart": [  // Meta-skill loading
    "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/session_start.sh",
    "timeout": 5000
  ]
}
```

**Hook Execution Order**:
```
Session Start:
  1. SessionStart hook → loads using-shannon
  2. User interaction begins with Iron Laws active

During Work:
  3. UserPromptSubmit → injects goals into every prompt
  4. PostToolUse → validates every Write/Edit (mock detection)
  5. PreCompact → emergency saves if context limit approached

Session End:
  6. Stop hook → validates wave gates before allowing exit
```

**Error Handling**:
- PreCompact: `continueOnError: false` (MUST succeed)
- Others: Silent failures allowed (logged but don't block)

**Key Insight**: Hooks create "enforcement mesh" around Claude's execution. Can't bypass Iron Laws.

---

### Pattern 12: Multi-Skill Orchestration (shannon-analysis as Example)

**Discovery**: shannon-analysis is FLEXIBLE skill that coordinates sub-skills

**Sub-Skill Architecture** (shannon-analysis lines 33-42):
```yaml
required-sub-skills:
  - mcp-discovery      # Must be available

optional-sub-skills:
  - spec-analysis      # Invoked if specification provided
  - project-indexing   # Invoked for large codebases
  - confidence-check   # Invoked for uncertainty assessment
  - functional-testing # Invoked if testing analysis needed
  - wave-orchestration # Invoked if complexity >=0.50
```

**Orchestration Logic**:
```python
def shannon_analysis(request):
    # 1. Detect analysis type
    analysis_type = detect_type(request)
    # → "architecture", "technical-debt", "complexity", etc.

    # 2. Query Serena for historical context
    history = serena.search_nodes(f"analysis:{project_name}")

    # 3. Select appropriate sub-skills
    if analysis_type == "complexity":
        invoke_skill("spec-analysis")
        invoke_skill("mcp-discovery")  # Uses spec-analysis output
    elif analysis_type == "technical-debt":
        invoke_skill("project-indexing")  # Get file inventory
        grep_for_debt_indicators()
        invoke_skill("confidence-check")  # Assess debt severity

    # 4. Coordinate results
    aggregate_findings()

    # 5. Persist to Serena
    serena.write_memory(f"analysis_{timestamp}", results)
```

**Key Insight**: FLEXIBLE skills orchestrate QUANTITATIVE/RIGID skills. Hierarchy: Orchestrator → Specialists.

---

## Shannon Architecture: Component Hierarchy

Based on discoveries above:

```
┌─────────────────────────────────────────────────┐
│             USER INTERACTION LAYER               │
│  Commands: /sh_spec, /sh_wave, /sh_test        │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│              ENFORCEMENT LAYER                   │
│  Hooks: session_start, post_tool_use,           │
│         precompact, stop, user_prompt_submit    │
│  Iron Laws: NO MOCKS, Mandatory Analysis,       │
│             Checkpoints, Wave Validation         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│            ORCHESTRATION LAYER                   │
│  Meta-Skills: using-shannon, shannon-analysis    │
│  Coordinate: Sub-skill selection, workflow      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           SPECIALIST SKILLS LAYER                │
│  QUANTITATIVE: spec-analysis, wave-orchestration │
│  PROTOCOL: phase-planning, context-preservation  │
│  RIGID: functional-testing                       │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│            INFRASTRUCTURE LAYER                  │
│  MCPs: Serena (memory), Puppeteer (testing),    │
│        Sequential (thinking), Context7 (docs)    │
│  Tools: Read, Write, Grep, Glob, Bash           │
└─────────────────────────────────────────────────┘
```

**Data Flow Example** (User runs /sh_spec):
```
1. USER: "/sh_spec Build todo app"
   ↓
2. COMMAND: /sh_spec triggers spec-analysis via COMMAND_SKILL_MAP
   ↓
3. ENFORCEMENT: session_start hook already loaded using-shannon (Iron Laws active)
   ↓
4. ORCHESTRATION: spec-analysis (specialist skill) executes
   ↓
5. SPECIALIST WORK: Calculate 8D score → domain % → MCP recommendations
   ↓
6. INFRASTRUCTURE: Save to Serena MCP via write_memory()
   ↓
7. ORCHESTRATION: spec-analysis chains to phase-planning
   ↓
8. SPECIALIST WORK: phase-planning generates 5-phase plan
   ↓
9. INFRASTRUCTURE: Save phase plan to Serena
   ↓
10. USER: Receives analysis + phase plan
```

**Enforcement Checkpoints**:
- Hook intercepts at step 8 if phase-planning writes test files with mocks → BLOCKED
- Hook intercepts at step 6 if context limit reached → PreCompact emergency save

---

### Pattern 13: Agent Layer Integration

**Discovery**: 24 Shannon specialist agents discovered in shannon-plugin/agents/

**Agent Categories**:
```
Core Orchestrators (5):
  - WAVE_COORDINATOR: Coordinates parallel wave execution
  - CONTEXT_GUARDIAN: Emergency checkpoint creation (PreCompact)
  - PHASE_ARCHITECT: Phase plan generation
  - ARCHITECT: System design
  - SPEC_ANALYZER: 8D analysis execution

Domain Builders (8):
  - FRONTEND: React/Vue/Angular implementation
  - BACKEND: API/server implementation
  - MOBILE_DEVELOPER: iOS/Android apps
  - DATABASE_ARCHITECT: Schema design
  - DATA_ENGINEER: ETL/pipeline work
  - DEVOPS: Infrastructure/deployment
  - API_DESIGNER: API contract design
  - SECURITY: Security implementation

Quality Specialists (6):
  - TEST_GUARDIAN: Functional testing enforcement
  - QA: Quality assurance
  - CODE_REVIEWER: Code review
  - REFACTORER: Refactoring work
  - PERFORMANCE: Performance optimization
  - ANALYZER: Code analysis

Support (5):
  - SCRIBE: Documentation writing
  - MENTOR: Educational guidance
  - TECHNICAL_WRITER: Technical docs
  - IMPLEMENTATION_WORKER: General implementation
  - PRODUCT_MANAGER: Requirements
```

**Agent-Skill Integration** (from context-restoration checkpoint structure):
```json
{
  "agent_context": {
    "active_agents": ["implementation-worker"],
    "agent_handoff_data": {
      "from_agent": "backend-architect",
      "to_agent": "implementation-worker",
      "context": "Complete auth implementation per plan"
    }
  },
  "serena_memory_keys": [
    "wave_1_complete_taskapp",  // Agents write results here
    "wave_2_results_frontend",  // Agent-specific results
  ]
}
```

**How Agents Use Skills**:
```
WAVE_COORDINATOR agent:
  → Reads wave-orchestration skill for coordination protocol
  → Spawns domain agents (FRONTEND, BACKEND, DATABASE_ARCHITECT)
  → Each domain agent loads context-preservation for checkpoint
  → Each agent writes results to Serena (wave_N_{agent_type}_results)
  → WAVE_COORDINATOR synthesizes via wave-orchestration checkpoint protocol

CONTEXT_GUARDIAN agent:
  → Triggered by PreCompact hook
  → Reads context-preservation skill for checkpoint structure
  → Collects session state
  → Writes to Serena (precompact_checkpoint_{timestamp})
  → Returns checkpoint_id for restoration

TEST_GUARDIAN agent:
  → Reads functional-testing skill for NO MOCKS patterns
  → Scans existing tests for violations
  → Generates Puppeteer/Playwright functional tests
  → Works with post_tool_use.py hook (hook blocks, agent fixes)
```

**Key Insight**: Agents are EXECUTORS of skills. Skills define WHAT to do; agents DO it.

---

## Agents (ANSWERED)

**How Shannon agents differ from general-purpose**:
- [x] Pre-loaded with specific Shannon skills (e.g., WAVE_COORDINATOR has wave-orchestration)
- [x] Mandatory context loading from Serena (every agent reads previous wave results)
- [x] Write results to standardized Serena keys (wave_{N}_{agent_type}_results)
- [x] Follow NO MOCKS philosophy (functional testing only)
- [x] Subject to hook enforcement (post_tool_use blocks mock usage even for agents)

**System Hierarchy** (ANSWERED):
- [x] **Precedence**: Hooks > Skills > Commands > Agents > Tools > MCPs
  - **Hooks**: ENFORCE (cannot be bypassed, real-time blocking)
  - **Skills**: DEFINE workflows (document algorithms and processes)
  - **Commands**: TRIGGER skills (user-facing entry points)
  - **Agents**: EXECUTE skills (specialized sub-agents with pre-loaded skills)
  - **Tools**: IMPLEMENT actions (Read, Write, Grep, etc.)
  - **MCPs**: PROVIDE infrastructure (Serena memory, Puppeteer browser, etc.)
- [x] **Example**: post_tool_use hook blocks even WAVE_COORDINATOR if it tries to Write mocks
- [x] **Iron Law Enforcement**: Skills document → Hooks enforce → Agents comply
  - functional-testing skill documents NO MOCKS
  - post_tool_use.py hook scans and blocks mocks
  - All agents (including TEST_GUARDIAN) subject to hook enforcement

---

## Shannon Framework: Complete Component Inventory

### Commands (48 total)
- **Location**: shannon-plugin/commands/
- **Function**: User-facing entry points for Shannon workflows
- **Examples**: /sh_spec, /sh_wave, /sh_test, /sh_checkpoint, /shannon:prime
- **Integration**: Commands invoke skills via COMMAND_SKILL_MAP

### Skills (16 total - 16,740 lines)
- **Location**: shannon-plugin/skills/
- **Types**:
  - QUANTITATIVE (2): spec-analysis (1544L), wave-orchestration (1581L)
  - PROTOCOL (4): phase-planning (1182L), context-preservation (562L), context-restoration (957L), skill-discovery (565L)
  - RIGID (2): functional-testing (1402L), using-shannon (723L - meta)
  - FLEXIBLE (8): shannon-analysis (1255L), goal-management (847L), mcp-discovery (726L), etc.
- **Enhancements**: 3 with performance benchmarks + execution walkthroughs

### Agents (24 total)
- **Location**: shannon-plugin/agents/
- **Orchestrators**: WAVE_COORDINATOR, CONTEXT_GUARDIAN, PHASE_ARCHITECT, SPEC_ANALYZER, ARCHITECT
- **Domain Builders**: FRONTEND, BACKEND, MOBILE_DEVELOPER, DATABASE_ARCHITECT, DEVOPS, API_DESIGNER, DATA_ENGINEER, SECURITY
- **Quality**: TEST_GUARDIAN, QA, CODE_REVIEWER, REFACTORER, PERFORMANCE, ANALYZER
- **Support**: SCRIBE, MENTOR, TECHNICAL_WRITER, IMPLEMENTATION_WORKER, PRODUCT_MANAGER
- **Configuration**: Each agent has YAML frontmatter with activation thresholds, MCP requirements, dependencies

### Hooks (6 total)
- **Location**: shannon-plugin/hooks/
- **Hooks**: session_start.sh, post_tool_use.py, precompact.py, stop.py, user_prompt_submit.py, hooks.json
- **Function**: Automatic enforcement of Iron Laws
- **Integration**: Intercept tool execution, block violations, trigger emergency saves
- **Documentation Status**: ❌ NO comprehensive documentation (CRITICAL GAP)

### Core Patterns (9 documented)
- **Location**: shannon-plugin/core/
- **Examples**: TESTING_PHILOSOPHY.md, CONTEXT_MANAGEMENT.md, etc.
- **Function**: Define Iron Laws and foundational principles

### MCPs (Tiered System)
- **Tier 1 (MANDATORY)**: Serena MCP (all skills require)
- **Tier 2 (PRIMARY)**: Domain-specific (Puppeteer, PostgreSQL, Magic, Context7)
- **Tier 3 (SECONDARY)**: Supporting (GitHub, AWS, Sequential)
- **Tier 4 (OPTIONAL)**: Conditional (Tavily, monitoring)

---

## Critical Gaps Identified

### GAP 1: Hook System Documentation ❌ CRITICAL
**Status**: 5 hooks exist (6,574 bytes total code) but no comprehensive documentation
**Impact**: Users don't understand enforcement mechanisms
**Priority**: HIGH
**Location for docs**: shannon-plugin/hooks/README.md (doesn't exist)
**Content needed**:
- Hook lifecycle and execution order
- How each hook enforces specific Iron Laws
- Configuration via hooks.json
- Troubleshooting hook failures
- Relationship to skills

### GAP 2: Root README ❌ CRITICAL
**Status**: README.md deleted (shown in git status), backup exists
**Impact**: No entry point explaining Shannon architecture
**Priority**: HIGH
**Content needed**:
- What is Shannon Framework?
- Component hierarchy (Commands → Skills → Agents → Hooks → MCPs)
- Quick start guide
- Installation and configuration
- Integration patterns

### GAP 3: Command Documentation ⚠️ MEDIUM
**Status**: 48 commands exist but no usage guides
**Impact**: Users must reverse-engineer command behavior
**Priority**: MEDIUM
**Content needed**:
- Command reference (all 48 commands)
- Usage examples per command
- Which skills each command invokes
- Parameter documentation

---

## Next Actions (Recommended Pivot)

**COMPLETE**:
- ✅ Batch 1 (3 skills enhanced + tested + committed)
- ✅ System architecture synthesis (13 patterns documented)
- ✅ Agent-Skill-Hook integration mapped

**PIVOT TO HIGH-VALUE WORK**:
1. **Phase 2: Hook Documentation** (Tasks 17-21)
   - Document all 6 hooks comprehensively
   - Explain enforcement mechanisms
   - Show integration with skills

2. **Phase 3: Root README** (Task 22)
   - Restore README.md with architecture overview
   - Explain Shannon's 6-layer hierarchy
   - Quick start and integration guide

3. **Phase 4: Command Guides** (Tasks 23-30)
   - Document 48 commands with examples
   - Command-skill mapping table

**RATIONALE**:
- Remaining 13 skills don't show critical gaps (already comprehensive)
- Hooks/README/Commands are WHERE users get confused
- Synthesis doc captures system integration (can be refined into Root README)

---

**Last Updated**: 2025-11-08T20:45:00Z (after Batch 1 + rapid audit complete)


## Enhancement Insights (From Tasks 1-3)

**What Makes a Good Enhancement**:
1. ✅ **Behavioral Change**: spec-analysis walkthrough → 19% accuracy improvement (0.47→0.38)
2. ⚠️ **Educational Only**: wave-orchestration walkthrough → Same output, more confidence
3. ✅ **Clarifies Ambiguity**: phase-planning walkthrough → Additive vs multiplicative resolved

**Testing Strategy Learned**:
- RED vs GREEN comparison reveals if enhancement changes behavior
- Identical outputs = educational value only (marginal)
- Different outputs = algorithm improvement (high value)

**Focus Going Forward**:
- Target skills with ambiguous algorithms (like spec-analysis had)
- Skip skills already deterministic (like wave-orchestration was)
- Look for integration documentation gaps (how components coordinate)

---

## Next Investigation Areas

1. **Hook System**: How enforcement actually works
2. **Command-Skill Mapping**: /sh_spec → spec-analysis relationship
3. **Agent-Skill Loading**: Do wave agents auto-load skills?
4. **MCP Integration Matrix**: Which skills need which MCPs and why

---

**Last Updated**: 2025-11-08T20:30:00Z (during Batch 1 completion)
