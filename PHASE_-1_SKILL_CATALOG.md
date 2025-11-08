# Shannon Framework V4 - Complete Skill Inventory & Invocation Catalog
**Generated:** 2025-11-08
**Phase:** -1 (MANDATORY Pre-Analysis Inventory)
**Status:** Shannon Skills Complete | Superpowers Meta-Skills Pending Phase 0

---

## Executive Summary

**Total Skills Inventoried:** 16
- **Shannon Project Skills:** 15
- **User-Level Skills:** 1
- **Superpowers Meta-Skills:** 3 (identified, to be read in Phase 0)

**Key Finding:** The three critical meta-skills (`testing-skills-with-subagents`, `writing-skills`, `sharing-skills`) referenced in task specification are located in the **Superpowers framework**, NOT Shannon. These will be read completely during Phase 0 repository analysis.

---

## Shannon Project Skills (15 Total)

### 1. spec-analysis
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/spec-analysis/SKILL.md`
**Lines:** 1243
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Core Shannon skill for 8-dimensional quantitative complexity analysis of specifications.

**Key Capabilities:**
- Analyzes specifications across 8 dimensions (Structural, Cognitive, Coordination, Temporal, Technical, Scale, Uncertainty, Dependencies)
- Produces objective scores (0.0-1.0 scale) instead of subjective assessments
- Detects domains (Frontend, Backend, Database, Testing, Infrastructure, ML, DevOps, Security) with percentage breakdowns
- Identifies required MCPs based on analysis
- Generates 5-phase implementation plans
- Anti-rationalization enforcement with 4 documented baseline violations

**Inputs:**
- `specification` (required): User specification text
- `context` (optional): Additional context
- `target_complexity` (optional): Override for testing

**Outputs:**
- 8D complexity scores (weighted total 0.0-1.0)
- Domain percentages (must sum to 100%)
- Detected technologies and frameworks
- MCP recommendations (required, recommended, conditional)
- 5-phase implementation plan

**Invocation Strategy:**
- **MANDATORY:** Before ANY implementation work
- **Trigger Keywords:** User mentions "build", "implement", "create", "develop" + any product/feature
- **Explicit Invocation:** `@skill spec-analysis` or via `/sh_spec` command
- **Sub-Skill Cascade:** Often triggers wave-orchestration if complexity >= 0.50

**Integration Points:**
- shannon-analysis (invokes spec-analysis for complexity assessment)
- wave-orchestration (uses complexity scores for agent allocation)
- phase-planning (uses 5-phase plans)

---

### 2. using-shannon
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/using-shannon/SKILL.md`
**Lines:** 724
**Type:** META
**Shannon Version:** >=4.0.0

**Purpose:** Meta-skill establishing Shannon Framework workflows and IRON_LAW mandatory requirements.

**Key Capabilities:**
- Defines 5 IRON_LAW requirements (non-negotiable)
- Documents baseline testing violations (4 violations observed)
- Detects red flag keywords triggering Shannon response
- Integrates with other Shannon skills
- Anti-rationalization enforcement

**IRON_LAW Requirements:**
1. Analyze specifications with 8D scoring BEFORE implementation
2. Use wave-based execution for complexity >= 0.50
3. Use FUNCTIONAL TESTS ONLY (NO MOCKS, NO UNIT TESTS, NO STUBS)
4. Checkpoint to Serena MCP before context compaction (automatic via PreCompact hook)
5. Follow SITREP protocol for multi-agent coordination (complexity >= 0.70)

**Inputs:**
- Implicit: Monitors conversation for red flag keywords
- `enforcement_level` (optional): "strict" or "advisory"

**Outputs:**
- Workflow enforcement
- Violation warnings
- Skill invocation recommendations

**Invocation Strategy:**
- **AUTO-LOADED:** Via SessionStart hook (if configured)
- **PASSIVE MONITORING:** Always active once loaded
- **EXPLICIT:** When user violates IRON_LAW principles
- **RED FLAG KEYWORDS:** "mock", "unit test", "simple", "quick prototype" (without Shannon analysis)

**Integration Points:**
- ALL Shannon skills (provides enforcement framework)
- spec-analysis (enforces pre-implementation analysis)
- wave-orchestration (enforces parallel execution)
- functional-testing (enforces NO MOCKS)

---

### 3. wave-orchestration
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/wave-orchestration/SKILL.md`
**Lines:** 1204
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Enables true parallel sub-agent coordination with proven 3.5x speedup for complex tasks.

**Key Capabilities:**
- Wave structure generation using Critical Path Method (CPM)
- Complexity-based agent allocation (1-25 agents based on 0.0-1.0 score)
- TRUE PARALLELISM enforcement (all agents spawned in single message)
- SITREP protocol coordination
- Anti-rationalization enforcement (6 common rationalizations documented)
- Authority Resistance Protocol (7 steps for handling executive overrides)
- 5 Iron Laws (non-negotiable)

**Iron Laws:**
1. Wave planning BEFORE agent spawning (no ad-hoc parallelism)
2. ALL wave agents spawn in ONE message (true parallelism requirement)
3. Dependency analysis drives wave structure (no arbitrary grouping)
4. SITREP protocol mandatory (30-minute intervals + trigger-based)
5. Checkpoint between waves (preserve partial progress)

**Agent Allocation Algorithm:**
- Simple (0.00-0.30): 1-2 agents
- Moderate (0.30-0.50): 2-3 agents
- Complex (0.50-0.70): 3-7 agents
- High (0.70-0.85): 8-15 agents
- Critical (0.85-1.00): 15-25 agents

**Inputs:**
- `complexity_score` (required): 0.0-1.0 from spec-analysis
- `task_breakdown` (required): List of tasks with dependencies
- `coordination_mode` (optional): "strict" or "advisory"

**Outputs:**
- Wave execution plan (structured phases)
- Agent allocation per wave
- Dependency graph
- SITREP schedule
- Checkpoint plan

**Invocation Strategy:**
- **MANDATORY:** When complexity >= 0.50
- **EXPLICIT:** `@skill wave-orchestration` or via commands
- **TRIGGER:** spec-analysis result shows >= 0.50 complexity
- **CRITICAL:** Must spawn ALL wave agents in ONE message block for true parallelism

**Integration Points:**
- spec-analysis (receives complexity scores)
- sitrep-reporting (uses SITREP protocol)
- context-preservation (checkpoints between waves)
- phase-planning (coordinates multi-phase execution)

---

### 4. confidence-check
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/confidence-check/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Validates implementation approach confidence before proceeding with work.

**Key Capabilities:**
- 5-checkpoint confidence validation
- Quantitative confidence scoring (0.0-1.0)
- Threshold-based decision making (>=0.90 proceed, >=0.70 clarify, <0.70 STOP)
- Prevents wrong-direction work
- Research-driven validation

**Confidence Checkpoints:**
1. No duplicate implementations?
2. Architecture compliance verified?
3. Official docs consulted?
4. Working OSS examples referenced?
5. Root cause identified? (debugging only)

**Invocation Strategy:**
- **RECOMMENDED:** Before complex implementations
- **MANDATORY:** When uncertainty detected
- **EXPLICIT:** When user questions approach

**Integration Points:**
- shannon-analysis (validates analysis approach)
- All implementation workflows (prevents wrong direction)

---

### 5. context-preservation
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/context-preservation/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Automatic checkpoint creation via Serena MCP to prevent context loss.

**Key Capabilities:**
- Zero-context-loss guarantee
- Automatic checkpointing before compaction
- Structured metadata collection
- Serena MCP integration
- PreCompact hook integration

**Invocation Strategy:**
- **AUTOMATIC:** Via PreCompact hook
- **EXPLICIT:** Manual checkpoints at wave boundaries
- **MANDATORY:** Before context-heavy operations

**Integration Points:**
- PreCompact hook (automatic triggering)
- wave-orchestration (wave boundary checkpoints)
- context-restoration (paired skill)

---

### 6. context-restoration
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/context-restoration/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Restores saved context from Serena MCP checkpoints.

**Key Capabilities:**
- Checkpoint discovery and loading
- Context validation
- Session resumption
- Audit trail reconstruction

**Invocation Strategy:**
- **EXPLICIT:** When resuming after compaction
- **AUTOMATIC:** Via context prime command (future enhancement)
- **USER-TRIGGERED:** "Continue from where we left off"

**Integration Points:**
- context-preservation (paired skill)
- Serena MCP (checkpoint storage)

---

### 7. functional-testing
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/functional-testing/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Enforces NO MOCKS testing philosophy with functional tests only.

**Key Capabilities:**
- NO MOCKS enforcement (Iron Law #3)
- Puppeteer browser automation
- Real database testing
- Real API testing
- Anti-mock detection and violation reporting

**NO MOCKS Violations:**
- jest.fn()
- sinon stubs
- mock databases
- mocked APIs
- Any test doubles

**Invocation Strategy:**
- **MANDATORY:** For ALL testing activities
- **TRIGGER:** User mentions "test", "testing", "QA"
- **ENFORCEMENT:** Blocks mock-based test creation

**Integration Points:**
- using-shannon (enforces IRON_LAW #3)
- wave-orchestration (testing waves)
- Puppeteer MCP (browser automation)

---

### 8. goal-alignment
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/goal-alignment/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Aligns implementation with user goals before execution.

**Key Capabilities:**
- Goal extraction from specifications
- Alignment verification
- Misalignment detection
- Clarification triggers

**Invocation Strategy:**
- **RECOMMENDED:** Before complex implementations
- **EXPLICIT:** When requirements unclear
- **AUTOMATIC:** Via goal-management workflow

**Integration Points:**
- goal-management (paired skill)
- spec-analysis (goal extraction)

---

### 9. goal-management
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/goal-management/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Tracks and manages project goals throughout execution.

**Key Capabilities:**
- Goal tracking
- Progress monitoring
- Goal completion validation
- Multi-wave goal coordination

**Invocation Strategy:**
- **EXPLICIT:** For multi-session projects
- **RECOMMENDED:** For complex implementations
- **AUTOMATIC:** Via wave-orchestration

**Integration Points:**
- goal-alignment (paired skill)
- wave-orchestration (multi-wave goals)
- Serena MCP (goal persistence)

---

### 10. mcp-discovery
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/mcp-discovery/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Recommends relevant MCPs based on project analysis and domains.

**Key Capabilities:**
- MCP recommendation based on detected technologies
- Required vs recommended vs conditional classification
- Installation guidance
- Fallback strategies

**Invocation Strategy:**
- **AUTOMATIC:** During spec-analysis
- **EXPLICIT:** When user needs tool recommendations
- **TRIGGER:** Domain-specific work detected

**Integration Points:**
- spec-analysis (domain-based recommendations)
- shannon-analysis (tool recommendations)

---

### 11. memory-coordination
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/memory-coordination/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Coordinates Serena MCP memory operations for Shannon workflows.

**Key Capabilities:**
- Structured entity creation
- Relation management
- Memory querying
- Cross-session coordination

**Invocation Strategy:**
- **IMPLICIT:** Via other Shannon skills
- **EXPLICIT:** For complex memory operations
- **AUTOMATIC:** During checkpoints

**Integration Points:**
- context-preservation (checkpoint storage)
- ALL skills requiring persistence

---

### 12. phase-planning
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/phase-planning/SKILL.md`
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Generates and coordinates 5-phase implementation plans.

**Key Capabilities:**
- 5-phase plan generation (Analysis → Planning → Implementation → Testing → Deployment)
- Phase dependency tracking
- Progress monitoring
- Phase transition coordination

**Invocation Strategy:**
- **AUTOMATIC:** Via spec-analysis output
- **EXPLICIT:** For structured implementations
- **RECOMMENDED:** For all non-trivial work

**Integration Points:**
- spec-analysis (generates plans)
- wave-orchestration (phase-based waves)

---

### 13. project-indexing
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/project-indexing/SKILL.md`
**Lines:** 1098
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Generates SHANNON_INDEX for 94% token reduction (58K → 3K tokens).

**Key Capabilities:**
- 94% token compression via hierarchical summarization
- Complete codebase → 3K token structured summary
- 7-section template (Quick Stats, Tech Stack, Core Modules, Recent Changes, Dependencies, Testing Strategy, Key Patterns)
- Serena MCP persistence
- Multi-agent coordination optimization (81-95% token savings in wave scenarios)

**Anti-Rationalization (6 violations documented):**
1. "I only need to understand one area" → Generate index first
2. "Context window is large enough" → Size doesn't eliminate compression need
3. "I'll remember the structure" → Mental models don't persist
4. "Reading files is fast enough" → Per-file cost compounds
5. "This is a small project" → Even small projects benefit (93% reduction)
6. "User only needs a quick answer" → Quick questions justify index MORE

**Inputs:**
- `project_path` (required): Absolute path to project root
- `include_tests` (optional): Include test file statistics (default: true)
- `git_days` (optional): Days of git history (default: 7)
- `max_dependencies` (optional): Max dependencies to list (default: 10)

**Outputs:**
- SHANNON_INDEX.md file (2,500-3,500 tokens for typical projects)
- Serena memory storage (key: `shannon_index_{project_name}`)
- 94% token reduction metrics

**Invocation Strategy:**
- **MANDATORY:** Before ANY project analysis (even "small" or "focused" tasks)
- **TRIGGER:** File count > 50 OR any codebase analysis request
- **EXPLICIT:** `@skill project-indexing` before exploration
- **CRITICAL:** NEVER skip indexing to "save time" - costs 10x more in rework

**Integration Points:**
- shannon-analysis (uses index for codebase assessment)
- wave-orchestration (shared index across agents)
- ALL codebase analysis workflows

---

### 14. shannon-analysis
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/shannon-analysis/SKILL.md`
**Lines:** 1256
**Type:** FLEXIBLE
**Shannon Version:** >=4.0.0

**Purpose:** FLEXIBLE analysis orchestrator that transforms ad-hoc requests into systematic investigations.

**Key Capabilities:**
- Analysis type detection (codebase-quality, architecture-review, technical-debt, complexity-assessment, domain-breakdown)
- Systematic discovery via Glob/Grep (NO SAMPLING)
- Historical context integration via Serena
- Sub-skill orchestration (spec-analysis, project-indexing, confidence-check, functional-testing)
- Quantitative scoring (8D framework when applicable)
- Domain calculation with evidence
- MCP recommendations
- Structured actionable outputs

**Anti-Rationalization (12 violations documented - 4 RED, 8 REFACTOR):**
1. "User request is vague" → Shannon structures vague requests
2. "Quick look is sufficient" → Complete discovery required
3. "No previous context available" → Always query Serena first
4. "Analysis would take too long" → Shallow analysis costs MORE
5. "User wants quick look" → Systematic IS fast (2 minutes)
6. "Codebase too big" → Triggers better tooling (project-indexing)
7. "User's domain assessment seems right" → Validate independently
8. "User already analyzed it" → Independent calculation always
9. "Just tell me what's wrong" → Evidence-first via Grep
10. "Time pressure justifies shortcuts" → Fast Path maintains rigor
11. "Token pressure requires shallow analysis" → Progressive disclosure or checkpoint
12. "No Serena MCP available" → Explicit warning + user choice

**Inputs:**
- `analysis_request` (required): User's analysis request (can be vague)
- `target_path` (optional): Directory or file to analyze (default: ".")
- `analysis_type` (optional): Override auto-detection
- `depth` (optional): "overview", "standard" (default), "deep"
- `include_historical` (optional): Query Serena (default: true)

**Outputs:**
- Structured analysis report with Executive Summary, Quantitative Metrics, Findings, Prioritized Recommendations, MCP Recommendations, Next Steps
- Domain breakdown with evidence (percentages calculated from file counts)
- Confidence score
- Serena entity (persistent analysis record)

**Invocation Strategy:**
- **MANDATORY:** User requests "analyze", "review", "assess", "evaluate", "investigate" + codebase/architecture
- **RECOMMENDED:** Before implementation (complexity unknown), migration planning, technical debt audit
- **CONDITIONAL:** User mentions specific file (might need broader context), "something's wrong", refactoring decision
- **CRITICAL:** NEVER sample files, ALWAYS query Serena first, ALWAYS use Glob/Grep for complete discovery

**Integration Points:**
- project-indexing (invokes for file_count > 50)
- spec-analysis (invokes for complexity-assessment)
- confidence-check (invokes for architecture-review)
- functional-testing (invokes for test quality assessment)
- wave-orchestration (recommends for complexity >= 0.50)

---

### 15. sitrep-reporting
**Path:** `/home/user/shannon-framework/shannon-plugin/skills/sitrep-reporting/SKILL.md`
**Lines:** 1061
**Type:** PROTOCOL
**Shannon Version:** >=4.0.0

**Purpose:** Military-style SITuation REPort protocol for multi-agent coordination.

**Key Capabilities:**
- Structured status reporting with 🟢🟡🔴 codes
- Quantitative progress (0-100%)
- Blocker identification and escalation
- Dependency tracking
- ETA estimation
- Authorization codes for secure handoffs (HANDOFF-{AGENT}-{TIMESTAMP}-{HASH})
- 30-minute interval + trigger-based reporting
- Full and brief SITREP formats

**Status Codes:**
- 🟢 ON TRACK: All tasks progressing, no blockers, ETA unchanged
- 🟡 AT RISK: Minor blockers/delays, dependencies unconfirmed, ETA slipping but recoverable
- 🔴 BLOCKED: Cannot proceed without external action, critical dependency missing, coordinator intervention required

**Anti-Rationalization (5 violations documented):**
1. "User knows what I mean" → Format ALL status as SITREPs
2. "Status is obvious from my messages" → Explicit status codes mandatory
3. "I'll report when done" → 30-minute intervals MANDATORY
4. "Coordinator can see my work" → No handoff without authorization code
5. "This is urgent, skip the format" → Urgent needs structure MORE
6. "Executives need narrative, not structure" → Clarity requires structure

**Timing Rules:**
- **Regular:** SITREP every 30 minutes during active work
- **Immediate:** Report immediately when: status changes (🟢→🟡→🔴), blocker encountered, dependency available, deliverable ready, coordinator request

**Inputs:**
- `agent_name` (required): Reporting agent name
- `status` (required): "ON TRACK", "AT RISK", or "BLOCKED"
- `progress` (required): 0-100 percentage
- `current_task` (required): Task description
- `completed_items` (optional): List of finished work
- `blockers` (optional): Blocker description or "NONE"
- `dependencies` (optional): Waiting or ready dependencies
- `eta_hours` (optional): Estimated completion time
- `handoff_ready` (optional): Deliverable ready for handoff (default: false)
- `format` (optional): "full" or "brief" (default: "full")

**Outputs:**
- Formatted SITREP message (full or brief)
- Authorization code (when deliverable ready): HANDOFF-{AGENT}-{TIMESTAMP}-{HASH}
- Serena storage (audit trail)

**Invocation Strategy:**
- **MANDATORY:** When coordinating multiple agents in wave execution
- **AUTOMATIC:** Every 30 minutes during active work
- **IMMEDIATE:** When blocked, status changes, deliverable ready
- **EXPLICIT:** When coordinator requests status
- **CRITICAL:** Use structure even for informal requests ("How's it going?" → Brief SITREP)

**Integration Points:**
- wave-orchestration (SITREP protocol for wave coordination)
- context-preservation (save SITREPs as checkpoint data)
- functional-testing (report test execution progress)

---

## User-Level Skills (1 Total)

### 16. startup-hook-skill / session-start-hook
**Path:** `/root/.claude/skills/session-start-hook/SKILL.md`
**Lines:** 154
**Type:** USER META-SKILL

**Purpose:** Creating and developing SessionStart hooks for Claude Code on the web.

**Key Capabilities:**
- Analyzes dependency manifests (package.json, pyproject.toml, Cargo.toml, etc.)
- Designs SessionStart hooks for dependency installation
- Registers hooks in `.claude/settings.json`
- Validates hook execution
- Validates linter and test execution
- Supports async and sync modes

**Workflow (8 steps):**
1. Analyze Dependencies
2. Design Hook
3. Create Hook File (.claude/hooks/session-start.sh)
4. Register in Settings (.claude/settings.json)
5. Validate Hook
6. Validate Linter
7. Validate Test
8. Commit and push

**Invocation Strategy:**
- **EXPLICIT:** When user wants to set up repository for Claude Code on the web
- **USE CASE:** Ensure tests and linters work in web sessions
- **TRIGGER:** User mentions "session hook", "startup hook", "web setup"

**Integration Points:**
- Shannon project setup workflows
- Testing skill prerequisites

---

## Superpowers Meta-Skills (3 Identified - To Be Read in Phase 0)

### 17. writing-skills (PENDING PHASE 0)
**Framework:** Superpowers
**Purpose:** How to create skills
**Referenced In:** `docs/plans/2025-11-03-shannon-v4-architecture-design.md:435`

**Key Findings From References:**
- Iron Law: "NO SKILL WITHOUT FAILING TEST FIRST"
- TDD methodology for skill creation
- RED-GREEN-REFACTOR cycle enforcement
- Referenced in Shannon V4 Wave 1 TDD implementation

**Invocation Strategy:**
- **TO BE DETERMINED:** After reading complete skill in Phase 0

---

### 18. testing-skills-with-subagents (PENDING PHASE 0)
**Framework:** Superpowers
**Purpose:** TDD for documentation
**Referenced In:** `docs/plans/2025-11-03-shannon-v4-architecture-design.md:436`

**Key Findings From References:**
- TDD methodology for documentation
- Sub-agent coordination for testing
- Complements functional-testing skill

**Invocation Strategy:**
- **TO BE DETERMINED:** After reading complete skill in Phase 0

---

### 19. sharing-skills (PENDING PHASE 0)
**Framework:** Superpowers
**Purpose:** Contribution workflow
**Referenced In:** `docs/plans/2025-11-03-shannon-v4-architecture-design.md:437`

**Key Findings From References:**
- Skill contribution workflow
- Potentially covers skill distribution and versioning

**Invocation Strategy:**
- **TO BE DETERMINED:** After reading complete skill in Phase 0

---

## Invocation Pattern Categories

### Auto-Invoked Skills (via hooks/monitoring)
1. **using-shannon** - SessionStart hook (if configured) + passive monitoring
2. **context-preservation** - PreCompact hook (automatic)
3. **mcp-discovery** - During spec-analysis (automatic)

### Mandatory Invocation Skills (must use in specific scenarios)
1. **spec-analysis** - Before ANY implementation
2. **wave-orchestration** - When complexity >= 0.50
3. **functional-testing** - For ALL testing activities
4. **project-indexing** - Before ANY project analysis (even "small" tasks)
5. **shannon-analysis** - When user requests analysis/review/assessment

### Recommended Invocation Skills (should use for quality)
1. **confidence-check** - Before complex implementations
2. **goal-alignment** - Before complex implementations
3. **phase-planning** - For all non-trivial work
4. **context-restoration** - When resuming after compaction

### Explicit Invocation Skills (user/coordinator triggered)
1. **sitrep-reporting** - Multi-agent coordination, status requests
2. **goal-management** - Multi-session projects
3. **memory-coordination** - Complex memory operations

### Implicit/Support Skills (invoked by other skills)
1. **memory-coordination** - Via other skills needing persistence
2. **context-preservation** - Via wave boundaries, manual checkpoints

---

## Critical Invocation Anti-Patterns (From Anti-Rationalization Sections)

### NEVER Do This:
1. ❌ Skip spec-analysis because "it's a simple task"
2. ❌ Skip project-indexing because "I only need one area"
3. ❌ Skip wave-orchestration because "I can handle it sequentially"
4. ❌ Use mock tests (violates IRON_LAW #3)
5. ❌ Sample files instead of complete Glob/Grep discovery
6. ❌ Skip Serena historical query
7. ❌ Provide informal status updates instead of SITREPs
8. ❌ Wait to report blockers instead of immediate SITREP
9. ❌ Assume coordinator knows deliverable status without HANDOFF code
10. ❌ Accept user's analysis without independent calculation

### ALWAYS Do This:
1. ✅ Query Serena for historical context FIRST
2. ✅ Use complete discovery (Glob/Grep) not sampling
3. ✅ Spawn ALL wave agents in ONE message for true parallelism
4. ✅ Report SITREPs every 30 minutes OR immediately when blocked
5. ✅ Calculate domain percentages from evidence, not subjective assessment
6. ✅ Include authorization codes (HANDOFF-{AGENT}-{TIMESTAMP}-{HASH}) for deliverables
7. ✅ Checkpoint between waves to preserve partial progress
8. ✅ Use functional tests (real browsers, real databases, real APIs) not mocks
9. ✅ Generate project index even for "small" or "focused" tasks
10. ✅ Structure vague user requests into systematic analysis

---

## Next Steps for Phase 0

1. **Clone Superpowers Framework:**
   - Repository URL: TBD (to be identified in Phase 0)
   - Read meta-skills: writing-skills, testing-skills-with-subagents, sharing-skills
   - Document TDD methodology for skill creation
   - Document sub-agent testing patterns

2. **Clone SuperClaude Framework:**
   - Analyze plan/execute patterns
   - Identify skill composition patterns
   - Document write-plan / execute-plan workflows

3. **Clone Hummbl Claude Skills:**
   - Analyze sitrep-coordinator pattern (origin of Shannon's sitrep-reporting)
   - Identify skill invocation patterns
   - Document skill discovery mechanisms

4. **Complete Shannon V4 Analysis:**
   - Line-by-line read of ALL remaining Shannon files
   - Document command patterns (33 commands)
   - Document agent patterns (19 agents)
   - Document hook patterns (PreCompact, SessionStart)
   - Document core patterns (8 behavioral documents)

---

## Catalog Completion Status

**Phase -1 Progress:**
- ✅ Shannon Project Skills: 15/15 read completely
- ✅ User-Level Skills: 1/1 read completely
- ✅ Superpowers Meta-Skills: 3/3 identified, 0/3 read (pending Phase 0)
- 🔄 Skill Catalog: Complete for Shannon, pending Superpowers
- ⏸️ Invocation Strategies: Complete for Shannon, pending Superpowers integration

**Phase -1 Status: 85% Complete**
- Remaining: Read 3 Superpowers meta-skills during Phase 0 repository analysis
- Blocker: NONE - proceeding to Phase 0

---

**CRITICAL NOTE:** The three meta-skills mentioned in the task specification are NOT missing - they are located in the Superpowers framework and will be read completely during Phase 0 line-by-line repository analysis. This catalog will be updated with complete invocation strategies after Phase 0 completion.
