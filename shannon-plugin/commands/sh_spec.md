---
name: sh:spec
command: /sh:spec
description: "Analyzes user specifications and creates comprehensive implementation roadmaps with 8-dimensional complexity scoring, domain analysis, MCP suggestions, and phase planning"
category: command
complexity: advanced
triggers: [spec, specification, requirements, PRD, multi-paragraph-system-description]
mcp_servers: [serena, sequential, context7]
personas: [system-architect, requirements-analyst]
auto_activate: true
activation_condition: multi_paragraph_spec OR requirements_list OR explicit_command
---

# /sh:spec - Specification Analysis & Planning

> **Shannon V3 Context Framework**: This command activates Shannon's specification analysis engine with 8-dimensional complexity scoring, domain identification, MCP discovery, and structured phase planning.

## Purpose Statement

Transforms unstructured user specifications into comprehensive, actionable project roadmaps through systematic intelligence:

- **8-dimensional complexity scoring** - Quantitative assessment across structural, cognitive, coordination, temporal, technical, scale, uncertainty, and dependency dimensions
- **Domain identification** - Automatic detection and percentage calculation for frontend, backend, database, mobile, devops, and security domains
- **Dynamic MCP discovery** - Intelligent suggestion of appropriate MCP servers based on domain analysis (vs SuperClaude's static 6 servers)
- **5-phase planning** - Structured implementation plan with validation gates, timelines, deliverables, and success criteria
- **Risk assessment** - Identifies potential challenges with mitigation strategies
- **Timeline estimation** - Evidence-based duration estimates correlated to complexity scores
- **Context preservation** - Complete analysis saved to Serena MCP for cross-wave access

**What Makes This Different**: Shannon's specification analysis is automatic, systematic, and quantitative. SuperClaude requires manual specification analysis - developers figure out complexity, domains, and tools themselves. Shannon does this in 30 seconds with reproducible scoring algorithms.

## Usage Patterns

**Basic Usage**:
```
/sh:spec [specification-text]
/sh:spec @path/to/requirements.md
/sh:spec "Build task management web app with React, Express, PostgreSQL"
```

**With Options**:
```
/sh:spec [spec] --depth quick|normal|deep
/sh:spec [spec] --create-phases
/sh:spec [spec] --suggest-mcps
/sh:spec [spec] --save-checkpoint
```

**Auto-Activation** (no explicit command needed):
```
[User provides 3+ paragraph specification]
[User provides 5+ item requirements list]
[User attaches .pdf/.md requirements document]
→ Shannon automatically activates spec analysis
```

**Type in Claude Code conversation window** (not terminal)

## Activation Triggers

Shannon's specification analysis activates automatically when user input contains **ANY** of:

**Multi-Paragraph Specifications**:
- 3+ paragraphs describing a system or project
- Each paragraph > 50 words
- Contains architectural descriptions, feature lists, or technical requirements

**Requirements Lists**:
- 5+ distinct items in list format (numbered or bulleted)
- Example: "Build system with: 1) User auth 2) Dashboard 3) Reports 4) API 5) Admin panel"

**Explicit Keywords**:
- **Primary**: "specification", "spec", "requirements", "PRD", "user stories", "build", "implement", "create", "develop"
- **Secondary**: "needs to", "must have", "should include", "features", "functionality", "users can", "system will"

**File Attachments**:
- User attaches *.pdf, *.md, *.doc, *.docx files
- Files contain specification-like content (detected by scanning first 500 words)

**Explicit Command**:
- User types `/sh:spec` command

**Detection Algorithm** (from SPEC_ANALYSIS.md):
```
IF (paragraph_count >= 3 AND avg_paragraph_length > 50)
   OR (list_item_count >= 5)
   OR (has_primary_keywords AND word_count > 100)
   OR (has_secondary_keywords AND word_count > 200)
   OR (file_attachment AND file_type in [pdf, md, doc, docx])
   OR (explicit_command = "/sh:spec")
THEN activate specification analysis
```

## Execution Flow

When this command activates, Claude Code follows this step-by-step process:

### Step 1: Context Loading (MANDATORY)
```
Execute FIRST before any analysis:
1. list_memories() - Discover all available Serena memories
2. read_memory("spec_analysis_previous") - Check for prior analysis
3. read_memory("project_context") - Load project background if exists
4. read_memory("requirements_draft") - Load partial requirements if exist

Purpose: Avoid duplicate work, build on existing context
```

### Step 2: Specification Parsing
```
Parse user input completely:
- Extract all requirements statements
- Identify technical keywords and frameworks
- Detect architectural patterns
- Count file references, service mentions, module descriptions
- Extract urgency indicators and deadlines
- Identify team coordination needs
- Detect advanced technology mentions
- Extract scale indicators (users, data volume)
- Identify ambiguities and unknowns
- Detect blocking dependencies

Purpose: Raw data extraction for complexity calculation
```

### Step 3: 8-Dimensional Complexity Scoring

**Execute scoring algorithms** (from SPEC_ANALYSIS.md):

**Dimension 1: Structural Complexity (20% weight)**
```
structural_score = weighted_sum(
  file_factor × 0.40,
  service_factor × 0.30,
  module_factor × 0.20,
  component_factor × 0.10
)

Example scores:
- 1 file: 0.04 (trivial)
- 15 files: 0.16 (low)
- 50 files + 3 modules: 0.27 (moderate)
- 200 services: 1.0 (critical)
```

**Dimension 2: Cognitive Complexity (15% weight)**
```
cognitive_score = sum_of_verb_scores(
  analysis_verbs: +0.20 max 0.40
  design_verbs: +0.20 max 0.40
  decision_verbs: +0.10 max 0.30
  learning_verbs: +0.15 max 0.30
  abstract_concepts: +0.15 max 0.30
)

Example: "analyze, architect, research" → 0.75 (high cognitive load)
```

**Dimension 3: Coordination Complexity (15% weight)**
```
coordination_score = (team_count × 0.25) + (integration_keywords × 0.15) + (stakeholders × 0.10)

Example: 5 teams + 3 integration keywords → 1.0 (maximum coordination)
```

**Dimension 4: Temporal Complexity (10% weight)**
```
temporal_score = urgency_multiplier + deadline_factor

Urgency: "urgent" = +0.40, "soon" = +0.30, standard = +0.10
Deadline: 24 hours = +0.50, 3 days = +0.40, 1 week = +0.30
```

**Dimension 5: Technical Complexity (15% weight)**
```
technical_score = advanced_tech_factor + algorithm_factor + integration_factor

Advanced tech (AI/ML, real-time, distributed, low-level, security): +0.20 each
Algorithms: +0.20 each
Integrations: +0.15 each
```

**Dimension 6: Scale Complexity (10% weight)**
```
scale_score = user_factor + data_factor + performance_factor

Users: >1M = +0.40, >100K = +0.30, >10K = +0.20
Data: TB/billions = +0.40, GB/millions = +0.20
Performance: "high performance" = +0.20, "scalable" = +0.15
```

**Dimension 7: Uncertainty Complexity (10% weight)**
```
uncertainty_score = ambiguity_factor + exploratory_factor + research_factor

Ambiguous language ("TBD", "unclear", "maybe"): +0.20 each
Exploratory terms ("explore", "POC", "prototype"): +0.15 each
Research needs: +0.15 each
```

**Dimension 8: Dependencies Complexity (5% weight)**
```
dependency_score = blocking_factor + external_factor

Blocking ("depends on", "requires", "waiting for"): +0.25 each
External dependencies: +0.20 each
```

**Total Complexity Calculation**:
```
total_complexity =
  0.20 × structural_score +
  0.15 × cognitive_score +
  0.15 × coordination_score +
  0.10 × temporal_score +
  0.15 × technical_score +
  0.10 × scale_score +
  0.10 × uncertainty_score +
  0.05 × dependency_score

Result: 0.0 - 1.0 (floating point score)
```

**Interpretation Bands**:
| Score | Label | Sub-Agents | Waves | Timeline |
|-------|-------|------------|-------|----------|
| 0.00-0.30 | Simple | 1-2 | 0-1 | Hours-1 day |
| 0.30-0.50 | Moderate | 2-3 | 1-2 | 1-2 days |
| 0.50-0.70 | Complex | 3-7 | 2-3 | 2-4 days |
| 0.70-0.85 | High | 8-15 | 3-5 | 1-2 weeks |
| 0.85-1.00 | Critical | 15-25 | 5-8 | 2+ weeks |

### Step 4: Domain Identification

**Count keywords for each domain**:

**Frontend Domain** - Keywords: UI, UX, component, React, Vue, Angular, Svelte, responsive, accessibility, CSS, HTML, JavaScript, TypeScript, dashboard, form, button, navigation, modal, chart, animation, etc.

**Backend Domain** - Keywords: API, endpoint, REST, GraphQL, server, microservice, Express, FastAPI, Django, authentication, JWT, OAuth, middleware, business logic, controller, route, etc.

**Database Domain** - Keywords: database, schema, migration, SQL, NoSQL, PostgreSQL, MongoDB, MySQL, ORM, Prisma, transaction, ACID, index, query, data model, etc.

**Mobile/iOS Domain** - Keywords: iOS, iPhone, iPad, Swift, SwiftUI, UIKit, Xcode, App Store, CoreData, HealthKit, mobile app, native, etc.

**DevOps Domain** - Keywords: deploy, CI/CD, Docker, Kubernetes, monitoring, AWS, Azure, GCP, serverless, infrastructure, Terraform, logging, etc.

**Security Domain** - Keywords: security, authentication, authorization, encryption, HTTPS, OAuth, vulnerability, compliance, GDPR, OWASP, etc.

**Calculate percentages**:
```
total_keywords = sum(all_domain_counts)
frontend_percentage = (frontend_count / total_keywords) × 100
[repeat for all domains]

Round to nearest integer
Normalize to sum = 100%
```

**Output format**:
```
Domain Analysis:
- Frontend (34%): React UI, component architecture, responsive design
- Backend (28%): Express API, business logic, authentication
- Database (22%): PostgreSQL, data persistence, schema design
- DevOps (16%): Docker deployment, CI/CD automation
```

### Step 5: MCP Server Suggestion

**Dynamic MCP Discovery Algorithm**:

**Tier 1: MANDATORY (Always Suggest)**
```
Serena MCP (CRITICAL)
- Priority: MANDATORY
- Rationale: Essential for Shannon's zero-context-loss architecture
- Usage: Save spec analysis, phase plans, wave results, checkpoints
- Commands: write_memory("key", data), read_memory("key"), list_memories()
- When: Every Shannon project, every wave, every phase
- Alternative: None (Serena is mandatory)
```

**Tier 2: PRIMARY (Domain-Based, ≥20% threshold)**

If **Frontend ≥ 20%**:
```
1. Magic MCP
   - Rationale: Rapid React/Vue/Angular component generation from 21st.dev
   - Usage: Generate UI components, forms, modals, navigation, dashboards
   - Example: `/ui button --variant primary` generates production-ready button

2. Puppeteer MCP
   - Rationale: Functional browser testing (Shannon's NO MOCKS mandate)
   - Usage: Test real user interactions in actual browser
   - Why: Real browser = real confidence, catches browser-specific issues

3. Context7 MCP
   - Rationale: Official React/Vue/Angular/Svelte documentation
   - Usage: Load framework patterns, hooks docs, best practices
   - Example: Lookup React useEffect patterns, Vue Composition API
```

If **Backend ≥ 20%**:
```
1. Context7 MCP
   - Rationale: Express/FastAPI/Django/Spring framework documentation
   - Usage: Load framework patterns, middleware examples, API design

2. Sequential MCP
   - Rationale: Complex backend logic analysis and multi-step reasoning
   - Usage: Design business logic, analyze architectural trade-offs

3. Database MCP (Specific to DB type)
   - Rationale: Direct database schema operations
   - Usage: Create schemas, run migrations, execute queries
   - Options: PostgreSQL MCP, MongoDB MCP, MySQL MCP, Redis MCP
```

If **Mobile/iOS ≥ 40%**:
```
1. SwiftLens MCP
   - Rationale: Swift code analysis, symbol operations
   - Usage: Analyze Swift codebases, find references, refactor code

2. iOS Simulator Tools
   - Rationale: Functional testing on actual iOS simulator (NO MOCKS)
   - Usage: Run XCUITests on simulator, validate iOS behavior

3. Context7 MCP
   - Rationale: SwiftUI/UIKit/Foundation framework documentation
   - Usage: Load Apple framework patterns, API documentation
```

If **Database ≥ 15%**:
```
PostgreSQL/MongoDB/MySQL MCP (database-specific)
- Rationale: Direct database operations for specified type
- Usage: Schema design, migrations, queries, performance optimization
```

If **DevOps ≥ 15%**:
```
1. GitHub MCP
   - Rationale: CI/CD workflow automation, version control
   - Usage: Create branches, automate commits, GitHub Actions, PRs

2. AWS/Azure/GCP MCP (cloud-specific)
   - Rationale: Cloud infrastructure automation
   - Usage: Deploy services, manage infrastructure, configure cloud resources
```

If **Security ≥ 15%**:
```
1. Context7 MCP
   - Rationale: Security patterns, OAuth libraries, OWASP guidelines
   - Usage: Load security best practices, authentication patterns

2. Sequential MCP
   - Rationale: Systematic threat modeling and security analysis
   - Usage: Analyze attack vectors, assess vulnerabilities
```

**Tier 3: SECONDARY (Supporting)**
```
GitHub MCP (if not already suggested)
- Suggested when: Any project (version control always valuable)
- Priority: Medium

Tavily/Firecrawl MCP
- Suggested when: Keywords like "research", "investigate", "explore"
- Priority: Low-Medium
```

### Step 6: 5-Phase Plan Generation

**Create structured 5-phase implementation plan**:

**Phase 1: Analysis & Planning (15% of total time)**
```
Objectives:
- Complete specification analysis
- Identify all requirements and constraints
- Create detailed task breakdown
- Identify risks and dependencies

Deliverables:
- Detailed specification document
- Task list with estimates
- Risk assessment
- Resource plan

Validation Gate:
✅ Pass Criteria:
- All requirements clearly understood
- No ambiguities remaining
- Complexity score validated
- MCP servers selected and configured

Pass Condition: ALL criteria met
```

**Phase 2: Architecture & Design (20% of total time)**
```
Objectives: [Generated based on domain percentages]
- If Frontend ≥30%: Component hierarchy design, state management strategy
- If Backend ≥30%: API design, database schema, authentication architecture
- If Database ≥25%: Data modeling, normalization, index strategy
- If Mobile ≥40%: iOS app architecture, data flow, navigation design

Deliverables:
- Architecture diagrams
- Technical specifications
- API contracts / component interfaces
- Database schema design

Validation Gate:
✅ Pass Criteria:
- All architectural decisions documented
- Design reviewed and approved
- Technical feasibility validated
- Performance considerations addressed

Pass Condition: ALL criteria met, design approved
```

**Phase 3: Implementation (40% of total time)** [Largest phase]
```
Objectives: [Generated based on domains]
- Implement all features per specification
- Follow established architectural patterns
- Create functional tests alongside code (NO MOCKS)
- Integrate components progressively

Deliverables:
- Working feature implementations
- Functional tests (NO MOCKS)
- Integration code
- Bug fixes

Validation Gate:
✅ Pass Criteria:
- All features implemented per specification
- Code follows established patterns
- Functional tests written (NO MOCKS)
- No known critical bugs

Pass Condition: ALL features complete, tests passing
```

**Phase 4: Integration & Testing (15% of total time)**
```
Objectives:
- Integrate all components
- Functional testing (Shannon: NO MOCKS)
- End-to-end testing
- Performance validation

Deliverables:
- Integrated system
- Test results (functional tests, no mocks)
- Performance metrics
- Bug fixes

Testing Requirements: [Generated based on domains]
- If Frontend: Puppeteer functional tests for user flows (NO MOCKS)
- If Backend: Real HTTP requests, real database (NO MOCKS)
- If iOS: XCUITests on actual simulator (NO MOCKS)

Validation Gate:
✅ Pass Criteria:
- All components integrated successfully
- Functional tests passing (NO MOCKS)
- Performance meets requirements
- No critical or high-priority bugs

Pass Condition: System fully functional, tests passing
```

**Phase 5: Deployment & Documentation (10% of total time)**
```
Objectives:
- Deploy to target environment
- Create comprehensive documentation
- Knowledge transfer
- Post-deployment validation

Deliverables:
- Deployed system
- Technical documentation
- User documentation
- Deployment runbook

Validation Gate:
✅ Pass Criteria:
- System deployed successfully
- All documentation complete
- Deployment validated
- Handoff complete

Pass Condition: System live, documentation complete
```

### Step 7: Timeline Estimation
```
Based on complexity score:

IF complexity < 0.30 (Simple):
  timeline = "4-8 hours"
ELSE IF complexity < 0.50 (Moderate):
  timeline = "1-2 days"
ELSE IF complexity < 0.70 (Complex):
  timeline = "2-4 days"
ELSE IF complexity < 0.85 (High):
  timeline = "1-2 weeks"
ELSE (Critical):
  timeline = "2-4 weeks"
```

### Step 8: Risk Assessment
```
Identify potential challenges:
- Technical risks from advanced technology usage
- Coordination risks from multi-team requirements
- Timeline risks from urgent deadlines
- Uncertainty risks from ambiguous requirements
- Dependency risks from external blockers

For each risk, provide:
- Risk description
- Likelihood (Low/Medium/High)
- Impact (Low/Medium/High)
- Mitigation strategy
```

### Step 9: Save to Serena MCP (CRITICAL)
```
Save complete analysis:

write_memory("spec_analysis_[timestamp]", {
  complexity_score: {total, dimensions},
  domain_analysis: {percentages, descriptions},
  suggested_mcps: {tier1, tier2, tier3},
  phase_plan: {phase1, phase2, phase3, phase4, phase5},
  timeline_estimate: string,
  risk_assessment: [risks],
  metadata: {timestamp, version, framework}
})

Purpose: Enable ALL sub-agents to access this analysis
Context Preservation: Zero information loss across waves
```

### Step 10: Generate Structured Output

**Use output template** (see Output Format section below)

## Sub-Agent Integration

This command activates the **SPEC_ANALYZER sub-agent** when complexity score ≥ 0.5 or user explicitly requests deeper analysis.

**SPEC_ANALYZER Sub-Agent**:
- **File**: Shannon/Agents/spec-analyzer.md
- **Role**: Requirements analysis and project planning expert
- **Activation**: Complexity ≥ 0.5 (moderate to critical) OR explicit invocation
- **Expertise**: 8-dimensional complexity analysis, domain identification, MCP discovery, phase planning
- **MCP Servers**: Serena (mandatory), Sequential (analysis), Context7 (patterns), Tavily (research)
- **Deliverables**: Complete specification analysis report saved to Serena

**Sub-Agent Workflow**:
1. Load context from Serena (list_memories, read previous analyses)
2. Execute 8-dimensional complexity scoring algorithms
3. Identify all domains with percentage calculations
4. Suggest appropriate MCP servers with rationale
5. Generate 5-phase implementation plan with validation gates
6. Create risk assessment with mitigation strategies
7. Save complete analysis to Serena MCP
8. Generate structured output report

**Integration with Wave System**:
- If complexity ≥ 0.7 → Suggest `/sh:create-waves` for parallel execution planning
- Wave coordinator reads `spec_analysis_[timestamp]` from Serena
- All wave workers access domain analysis for specialized work
- Phase plan guides wave sequencing and dependencies

## Output Format

**Complete Analysis Report Template**:

```markdown
# Specification Analysis Complete ✅

*Analyzed by: Shannon V3 Specification Analysis Engine*
*Analysis ID: spec_analysis_[timestamp]*
*Complexity: [score] ([interpretation])*
*Saved to Serena MCP: spec_analysis_[timestamp]*

---

## 📊 Complexity Assessment

**Overall Score**: [score] / 1.0 (**[interpretation]**)

**Dimensional Breakdown**:
| Dimension | Score | Weight | Contribution | Interpretation |
|-----------|-------|--------|--------------|----------------|
| Structural | [score] | 20% | [weighted] | [interpretation] |
| Cognitive | [score] | 15% | [weighted] | [interpretation] |
| Coordination | [score] | 15% | [weighted] | [interpretation] |
| Temporal | [score] | 10% | [weighted] | [interpretation] |
| Technical | [score] | 15% | [weighted] | [interpretation] |
| Scale | [score] | 10% | [weighted] | [interpretation] |
| Uncertainty | [score] | 10% | [weighted] | [interpretation] |
| Dependencies | [score] | 5% | [weighted] | [interpretation] |

**Complexity Interpretation**:
- **Score**: [score]
- **Category**: [Simple|Moderate|Complex|High|Critical]
- **Recommended Sub-Agents**: [count]
- **Recommended Waves**: [count]
- **Estimated Timeline**: [timeline]

---

## 🎯 Domain Analysis

**[Domain Name] ([percentage]%)**:
- [Key characteristic 1]
- [Key characteristic 2]
- [Key characteristic 3]

[Repeat for all domains with percentage > 0]

---

## 🔧 Recommended MCP Servers

### Tier 1: MANDATORY 🔴

**1. Serena MCP** (CRITICAL - Always Required)
   - **Purpose**: Session persistence and zero-context-loss architecture
   - **Usage**: Save all analysis, plans, wave results, enable cross-wave context
   - **When**: Throughout entire project lifecycle
   - **Rationale**: Shannon requires Serena for context preservation across auto-compact

### Tier 2: PRIMARY (Domain-Based)

**[N]. [MCP Name]** ([Domain]: [percentage]%)
   - **Purpose**: [purpose]
   - **Usage**: [usage_description]
   - **When**: [when_to_use]
   - **Rationale**: [why_suggested for this domain]
   - **Example**: [example_usage if applicable]

[Repeat for all primary MCPs]

### Tier 3: SECONDARY (Supporting)

**[N]. [MCP Name]** ([Context])
   - **Purpose**: [purpose]
   - **Usage**: [usage_description]
   - **Priority**: [priority_level]

[Repeat for all secondary MCPs]

### Summary
- **Total Suggested**: [count] MCPs (vs SuperClaude's static 6)
- **Mandatory**: [count]
- **Primary**: [count]
- **Secondary**: [count]
- **Optional**: [count]

**Rationale for Selection**: Domains drive MCP selection - [domain breakdown drives specific MCP recommendations]

---

## 📅 5-Phase Implementation Plan

### Phase 1: Analysis & Planning
**Duration**: [duration]
**Timeline**: [start] - [end]

**Objectives**:
- [objective 1]
- [objective 2]
- [objective 3]

**Deliverables**:
- [deliverable 1]
- [deliverable 2]
- [deliverable 3]

**Validation Gate**:
✅ Pass Criteria:
- [criterion 1]
- [criterion 2]
- [criterion 3]

**Pass Condition**: [pass condition]

---

[Repeat for Phases 2-5]

---

## ⚠️ Risk Assessment

**Risk 1: [Risk Name]**
- **Description**: [risk description]
- **Likelihood**: [Low|Medium|High]
- **Impact**: [Low|Medium|High]
- **Mitigation**: [mitigation strategy]

[Repeat for all identified risks]

---

## ✅ Next Steps

1. **Confirm Analysis**: Review complexity score and domain breakdown for accuracy
2. **Configure MCPs**: Set up recommended MCP servers in Claude Code
3. **Initialize Serena**: Verify this analysis is saved to Serena MCP
4. **Begin Phase 1**: Start with Analysis & Planning phase
5. **Create Waves** (if complexity ≥ 0.7): Run `/sh:create-waves` for parallel execution plan

---

## 🧠 Saved to Serena MCP

This complete analysis has been saved to Serena MCP with key: `spec_analysis_[timestamp]`

**Retrieve with**: `read_memory("spec_analysis_[timestamp]")`

**Context Available For**:
- All wave coordinators
- All implementation workers
- All testing workers
- All sub-agents throughout project lifecycle

**Context Preservation**: Zero information loss across auto-compact events via PreCompact hook

---

*Shannon V3 - From Specification to Production Through Systematic Intelligence*
```

## Examples

### Example 1: Web Application

**Input**:
```
/sh:spec "Build task management web app with React frontend, Express backend, PostgreSQL database, real-time updates via WebSocket, Docker deployment"
```

**Output**:
```
Complexity: 0.68 (Complex)
Domains: Frontend 38%, Backend 28%, Database 18%, DevOps 16%
MCPs: Serena, Magic, Puppeteer, Context7, Sequential, PostgreSQL, GitHub
Timeline: 2-4 days
Sub-Agents: 5-7 recommended
Waves: 3 waves (2a+2b parallel, then 3 sequential)
```

### Example 2: iOS Application

**Input**:
```
/sh:spec "Build SwiftUI meditation app with HealthKit integration, CoreData persistence, StoreKit subscriptions, daily reminders, progress tracking"
```

**Output**:
```
Complexity: 0.71 (High)
Domain: Mobile/iOS 100%
MCPs: Serena, SwiftLens, iOS Simulator, Context7
Timeline: 1-2 weeks
Sub-Agents: 8-12 recommended
Waves: 4 waves (parallel analysis, parallel feature development)
```

### Example 3: Research Project

**Input**:
```
/sh:spec "Research current state of AI code generation tools, analyze 20+ platforms, compare capabilities, synthesize findings into comprehensive report"
```

**Output**:
```
Complexity: 0.55 (Complex)
Domain: Research 100%
MCPs: Serena, Tavily, Firecrawl, Sequential, Context7
Timeline: 2-4 days
Sub-Agents: 3-5 recommended
Waves: 2 waves (parallel research, sequential synthesis)
```

## Integration with Shannon Framework

**Command Chaining**:
```
/sh:spec [specification]              # Step 1: Analyze
  ↓
/sh:create-waves                      # Step 2: Plan waves (if complexity ≥ 0.7)
  ↓
Execute Wave 1: Analysis              # Step 3: Parallel analysis
  ↓
Execute Waves 2a+2b: Implementation   # Step 4: Parallel implementation
  ↓
Execute Wave 3: Integration           # Step 5: Sequential integration
  ↓
/sh:checkpoint "Phase 3 complete"     # Step 6: Manual checkpoint
```

**Context Flow**:
```
/sh:spec saves to Serena → spec_analysis_[timestamp]
  ↓
/sh:create-waves reads spec_analysis_[timestamp]
  ↓
Wave coordinators read spec_analysis_[timestamp]
  ↓
All wave workers read spec_analysis_[timestamp]
  ↓
Testing workers read spec_analysis_[timestamp] for testing strategy
```

**Mode Integration**:
- Activates MODE_SpecAnalysis automatically
- Can combine with --brainstorm for iterative requirement refinement
- Works with --introspect for meta-analysis of specification quality

## Validation & Quality Gates

**Pre-Analysis Validation**:
```
IF word_count(specification) < 50:
  WARNING: "Insufficient detail for analysis (< 50 words)"
  ACTION: Ask user for more detail

IF NOT contains_technical_keywords(specification):
  WARNING: "No technical context detected"
  ACTION: Ask about implementation technology

IF NOT contains_actionable_verbs(specification):
  WARNING: "Specification lacks clear actionable requirements"
  ACTION: Ask "What should the system DO?"
```

**Post-Analysis Validation**:
```
VERIFY:
✅ Complexity score in range [0.0, 1.0]
✅ Domain percentages sum to exactly 100%
✅ Serena MCP in Tier 1 suggestions
✅ At least 1 domain-specific MCP suggested
✅ 5-phase plan generated with validation gates
✅ Testing todos enforce NO MOCKS philosophy
✅ Analysis ID unique and stored in Serena

IF any verification fails:
  ERROR: Report validation failure
  ACTION: Re-run analysis with corrections
```

## Comparison: Shannon vs SuperClaude

| Aspect | SuperClaude | Shannon /sh:spec |
|--------|-------------|------------------|
| **Spec Analysis** | Manual, ad-hoc | Automatic 8-dimensional scoring |
| **Complexity Scoring** | No quantitative assessment | 8-dimensional weighted scoring (0.0-1.0) |
| **Domain Analysis** | Manual identification | Automatic percentage calculation |
| **MCP Suggestions** | Static 6 MCPs | Dynamic discovery (6-15 MCPs with rationale) |
| **Phase Planning** | No structured approach | 5-phase templates with validation gates |
| **Timeline Estimation** | Subjective guess | Evidence-based correlation to complexity |
| **Context Preservation** | Not addressed | Saved to Serena for cross-wave access |
| **Time to Analysis** | 1-3 hours manual | 30 seconds automated |

**Key Innovation**: Shannon transforms specification analysis from manual, time-consuming work into systematic, reproducible, quantitative intelligence that directly informs resource allocation, timeline estimation, and risk assessment.

## Notes

- **Type this command in Claude Code conversation window**, not terminal
- **Auto-activation** works without explicit command for multi-paragraph specs
- **Mandatory Serena MCP**: Shannon requires Serena for zero-context-loss architecture
- **NO MOCKS Philosophy**: All testing suggestions enforce functional testing (real browser, real HTTP, real database)
- **Reproducibility**: Same specification always produces same complexity score
- **Objectivity**: All scores based on measurable indicators, not subjective judgment
- **Context Preservation**: Complete analysis saved to Serena, accessible to ALL sub-agents
- **PreCompact Hook**: Automatic checkpoint creation before Claude Code auto-compacts context

---

*Shannon V3 Framework - Systematic Intelligence for Claude Code*
*Command Reference: /sh:spec - Specification Analysis & Planning*