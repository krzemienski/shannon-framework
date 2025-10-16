---
name: sc:index
description: Enhanced command catalog browsing with Shannon command integration
category: command
base: SuperClaude /index command
enhancement: Shannon V3 command catalog + wave command patterns
complexity: low
wave-enabled: false
activates: [ANALYZER, MENTOR]
mcp-servers: [serena]
tools: [Read, Serena]
---

# /sc:index - Enhanced Command Catalog Browser

> **Enhanced from SuperClaude's `/index` command with Shannon V3 command catalog integration, wave command browsing, and intelligent command discovery.**

## Command Identity

**Name**: /sc:index
**Base Command**: SuperClaude's `/index`
**Shannon Enhancement**: Includes Shannon /sh: commands, wave patterns, MCP integration matrix
**Primary Domain**: Command discovery, usage patterns, workflow guidance
**Complexity Level**: Low (information retrieval and presentation)

---

## Purpose Statement

The `/sc:index` command transforms command discovery from static documentation into an intelligent catalog browser. It provides:

- **Unified Command Catalog**: Both SuperClaude /sc: and Shannon /sh: commands in one interface
- **Smart Search**: Find commands by keyword, domain, capability, or use case
- **Usage Patterns**: Real examples showing command combinations and workflows
- **Wave Integration**: Understand which commands support wave orchestration
- **MCP Mapping**: See which MCP servers each command utilizes
- **Context-Aware**: Suggests relevant commands based on project state

**SuperClaude Foundation**: Built on SuperClaude's command indexing with intelligent routing

**Shannon V3 Enhancements**:
- Integrated catalog of Shannon /sh: commands (4 new commands)
- Wave-enabled command identification and patterns
- MCP server integration matrix per command
- Sub-agent activation patterns for each command
- Workflow templates and command chaining examples
- Project context-aware command suggestions

---

## Shannon V3 Enhancements

### 1. Unified Command Catalog

**Complete Command Set** (29 total commands):

**SuperClaude Commands** (25):
```yaml
development:
  - /sc:build - Project builder with framework detection
  - /sc:implement - Feature and code implementation
  - /sc:design - Design orchestration

analysis:
  - /sc:analyze - Multi-dimensional code analysis
  - /sc:troubleshoot - Problem investigation
  - /sc:explain - Educational explanations

quality:
  - /sc:improve - Evidence-based enhancement
  - /sc:cleanup - Technical debt reduction

testing:
  - /sc:test - Testing workflows

documentation:
  - /sc:document - Documentation generation

planning:
  - /sc:estimate - Evidence-based estimation
  - /sc:task - Long-term project management

version_control:
  - /sc:git - Git workflow assistant

meta:
  - /sc:index - Command catalog browsing (this command)
  - /sc:load - Project context loading
  - /sc:spawn - Task orchestration
```

**Shannon Commands** (4):
```yaml
specification:
  - /sh:analyze-spec - Automatic 8-dimensional spec analysis

execution:
  - /sh:plan-phase - Structured 5-phase planning
  - /sh:execute-wave - Wave-based parallel orchestration

context:
  - /sh:checkpoint - Session state preservation
  - /sh:restore - Context restoration from checkpoint
  - /sh:status - Wave and session state monitoring
```

### 2. Wave-Enabled Command Matrix

**Commands Supporting Wave Orchestration** (7 commands):

| Command | Wave Support | Parallelization | Sub-Agents | Typical Waves |
|---------|--------------|-----------------|------------|---------------|
| /sc:analyze | Yes | Full | Domain specialists | 2-3 waves |
| /sc:build | Yes | Conditional | Build specialists | 1-3 waves |
| /sc:design | Yes | Full | Design specialists | 2-4 waves |
| /sc:implement | Yes | Full | Domain workers | 2-5 waves |
| /sc:improve | Yes | Full | Quality specialists | 2-4 waves |
| /sc:task | Yes | Full | Task specialists | Variable |
| /sh:execute-wave | Yes | Native | Any sub-agents | Variable |

**Wave Patterns**:
```yaml
analysis_wave:
  command: /sc:analyze
  pattern: "Scope → Parallel Analysis → Synthesis"
  waves: 3
  agents: [ANALYZER, ARCHITECT, PERFORMANCE, SECURITY, QA]

implementation_wave:
  command: /sc:implement
  pattern: "Design → Parallel Build → Integration → Testing"
  waves: 4
  agents: [domain-specific workers]

improvement_wave:
  command: /sc:improve
  pattern: "Assessment → Parallel Enhancement → Validation"
  waves: 3
  agents: [REFACTORER, PERFORMANCE, QA]
```

### 3. MCP Integration Matrix

**MCP Server Usage by Command**:

```yaml
serena_required:
  commands: [ALL Shannon commands, /sc:load, /sc:task]
  reason: "Context preservation and project memory"

sequential_primary:
  commands: [/sc:analyze, /sc:troubleshoot, /sc:explain]
  reason: "Complex reasoning and analysis"

context7_integration:
  commands: [/sc:build, /sc:implement, /sc:document, /sc:explain]
  reason: "Official documentation and patterns"

magic_ui:
  commands: [/sc:build, /sc:implement, /sc:design]
  reason: "UI component generation"

playwright_testing:
  commands: [/sc:test, /sc:build]
  reason: "Functional testing and validation"

tavily_research:
  commands: [/sh:analyze-spec]
  reason: "Market research and competitive analysis"
```

### 4. Sub-Agent Activation Patterns

**Agent Activation by Command**:

```yaml
primary_coordinators:
  ANALYZER: [/sc:analyze, /sc:troubleshoot, /sc:explain]
  ARCHITECT: [/sc:design, /sc:analyze]
  MENTOR: [/sc:explain, /sc:document]
  SCRIBE: [/sc:document, /sc:git]

domain_specialists:
  FRONTEND: [/sc:build, /sc:implement, /sc:improve]
  BACKEND: [/sc:build, /sc:implement, /sc:improve]
  DATA_ENGINEER: [/sc:build, /sc:implement]
  IOS_ENGINEER: [/sc:build, /sc:implement]
  MOBILE_ENGINEER: [/sc:build, /sc:implement]

quality_specialists:
  QA: [/sc:test, /sc:analyze]
  PERFORMANCE: [/sc:improve, /sc:analyze]
  SECURITY: [/sc:analyze, /sc:improve]
  REFACTORER: [/sc:cleanup, /sc:improve]

operations:
  DEVOPS: [/sc:git, /sc:build]
```

### 5. Context-Aware Command Suggestions

**Based on Project State**:

```yaml
no_spec_analysis:
  suggestion: "/sh:analyze-spec @requirements.md"
  reason: "Start with specification analysis"

spec_exists_no_implementation:
  suggestion: "/sh:plan-phase → /sh:execute-wave"
  reason: "Move from planning to execution"

code_exists_no_analysis:
  suggestion: "/sc:analyze . --comprehensive"
  reason: "Understand current codebase state"

quality_issues_detected:
  suggestion: "/sc:improve [target] --quality"
  reason: "Address quality findings"

testing_gaps:
  suggestion: "/sc:test --generate-functional"
  reason: "Create functional tests"
```

---

## Usage Patterns

### Basic Usage

```bash
/sc:index [query] [options]
```

**Parameters**:
- `[query]`: Search term, domain, or command name (optional)
- `[options]`: Search modifiers and filters (optional)

### Usage Examples

**Browse All Commands**:
```bash
/sc:index
# Lists all 29 commands (SuperClaude + Shannon) with brief descriptions
```

**Search by Keyword**:
```bash
/sc:index analyze
# Returns: /sc:analyze, /sh:analyze-spec, /sc:troubleshoot
# Shows usage patterns and examples for analysis commands
```

**Filter by Domain**:
```bash
/sc:index --domain testing
# Returns: /sc:test, wave patterns for testing
# Shows functional testing philosophy and examples
```

**Find Wave Commands**:
```bash
/sc:index --wave-enabled
# Returns: All 7 wave-enabled commands
# Shows parallelization patterns and sub-agent usage
```

**MCP Integration Lookup**:
```bash
/sc:index --mcp sequential
# Returns: All commands using Sequential MCP
# Shows integration patterns and use cases
```

**Command Comparison**:
```bash
/sc:index /sc:analyze vs /sh:analyze-spec
# Shows differences, when to use each, workflow integration
```

**Workflow Discovery**:
```bash
/sc:index workflow web-app
# Returns: Command sequence for web app development
# Example: /sh:analyze-spec → /sh:plan-phase → /sh:execute-wave → /sc:test
```

---

## Execution Flow

### Phase 1: Query Parsing

```
1. Parse User Query
   - Extract search terms
   - Identify filters (--domain, --wave-enabled, --mcp, etc.)
   - Detect comparison requests (vs, versus, compare)
   - Recognize workflow queries (workflow, sequence, chain)

2. Determine Query Type
   - No query → Full catalog listing
   - Keyword → Fuzzy search across commands
   - Domain filter → Category-based filtering
   - Wave filter → Wave-enabled commands only
   - MCP filter → Commands using specific MCP
   - Comparison → Side-by-side command comparison
   - Workflow → Template workflow suggestions
```

### Phase 2: Context Loading

```
1. Load Project Context (if available)
   - read_memory("spec_analysis") → Project domain and complexity
   - read_memory("current_phase") → Development phase
   - read_memory("quality_findings") → Known issues
   - list_memories() → Available project state

2. Analyze Project State
   - Has specification analysis been performed?
   - What phase is project in? (discovery, implementation, testing)
   - Are there known quality issues?
   - What commands have been used recently?

3. Prepare Context-Aware Suggestions
   - Based on project state, suggest next logical commands
   - Highlight relevant workflows
   - Warn about missing prerequisites
```

### Phase 3: Search Execution

```
For Catalog Listing:
1. Group commands by category (SuperClaude vs Shannon)
2. Sort by frequency of use or alphabetically
3. Show brief description for each
4. Indicate wave support and primary MCP servers

For Keyword Search:
1. Fuzzy match against command names and descriptions
2. Rank by relevance (name match > description match)
3. Include related commands (similar domain/capability)
4. Show usage examples for top matches

For Filtered Search:
1. Apply filters (domain, wave, MCP, agent)
2. Return matching commands with context
3. Show integration patterns for filtered results
4. Suggest complementary commands

For Comparison:
1. Extract command details for both commands
2. Show side-by-side comparison table
3. Highlight key differences
4. Provide guidance on when to use each
5. Show example workflows using both

For Workflow Query:
1. Identify use case (web app, iOS app, API, etc.)
2. Load relevant workflow template
3. Show command sequence with explanations
4. Include validation gates and checkpoints
5. Suggest MCP servers and sub-agents
```

### Phase 4: Result Presentation

```
1. Format Results
   - Use structured tables for command listings
   - Include usage examples for each command
   - Show MCP integration and sub-agent activation
   - Highlight wave support and parallelization

2. Add Context-Aware Suggestions
   - Based on project state, suggest relevant commands
   - Show workflow paths from current state
   - Warn about prerequisites not met

3. Provide Quick Reference
   - Common flag combinations
   - Integration patterns with other commands
   - Best practices and tips
```

---

## Output Format

### Full Catalog Listing

```markdown
# Shannon Framework Command Catalog

**Total Commands**: 29 (25 SuperClaude + 4 Shannon)
**Wave-Enabled**: 7 commands
**MCP Servers**: Serena, Sequential, Context7, Magic, Playwright, Tavily

---

## SuperClaude Commands (25)

### Development Commands

**`/sc:build [target]`**
- **Purpose**: Project builder with framework detection
- **Wave Support**: Yes (conditional)
- **MCP Servers**: Magic, Context7, Serena
- **Sub-Agents**: FRONTEND, BACKEND, domain specialists
- **Example**: `/sc:build web-app --framework react`

**`/sc:implement [feature]`**
- **Purpose**: Feature and code implementation with intelligent persona activation
- **Wave Support**: Yes (full)
- **MCP Servers**: Magic, Context7, Sequential, Serena
- **Sub-Agents**: Domain-specific workers based on feature type
- **Example**: `/sc:implement authentication --type backend`

**`/sc:design [domain]`**
- **Purpose**: Design orchestration and system architecture
- **Wave Support**: Yes (full)
- **MCP Servers**: Magic, Sequential, Context7, Serena
- **Sub-Agents**: ARCHITECT, domain designers
- **Example**: `/sc:design database-schema`

### Analysis Commands

**`/sc:analyze [target]`**
- **Purpose**: Multi-dimensional code and system analysis
- **Wave Support**: Yes (full)
- **MCP Servers**: Serena, Sequential, Context7
- **Sub-Agents**: ANALYZER, ARCHITECT, PERFORMANCE, SECURITY, QA
- **Example**: `/sc:analyze src/ --comprehensive --wave-mode`

**`/sc:troubleshoot [symptoms]`**
- **Purpose**: Problem investigation and debugging
- **Wave Support**: No
- **MCP Servers**: Sequential, Playwright, Serena
- **Sub-Agents**: ANALYZER, QA
- **Example**: `/sc:troubleshoot "API timeouts on production"`

**`/sc:explain [topic]`**
- **Purpose**: Educational explanations with clarity focus
- **Wave Support**: No
- **MCP Servers**: Context7, Sequential, Serena
- **Sub-Agents**: MENTOR, SCRIBE
- **Example**: `/sc:explain react-hooks --beginner-friendly`

### Quality Commands

**`/sc:improve [target]`**
- **Purpose**: Evidence-based code enhancement
- **Wave Support**: Yes (full)
- **MCP Servers**: Sequential, Context7, Magic, Serena
- **Sub-Agents**: REFACTORER, PERFORMANCE, ARCHITECT, QA
- **Example**: `/sc:improve src/ --focus performance --wave-mode`

**`/sc:cleanup [target]`**
- **Purpose**: Project cleanup and technical debt reduction
- **Wave Support**: No
- **MCP Servers**: Sequential, Serena
- **Sub-Agents**: REFACTORER
- **Example**: `/sc:cleanup src/ --remove-dead-code`

### Testing Commands

**`/sc:test [type]`**
- **Purpose**: Testing workflows with functional-first approach
- **Wave Support**: No
- **MCP Servers**: Playwright, Sequential, Serena
- **Sub-Agents**: QA
- **Example**: `/sc:test --functional --generate-e2e`

### Documentation Commands

**`/sc:document [target]`**
- **Purpose**: Documentation generation
- **Wave Support**: No
- **MCP Servers**: Context7, Sequential, Serena
- **Sub-Agents**: SCRIBE, MENTOR
- **Example**: `/sc:document api/ --format markdown`

### Planning Commands

**`/sc:estimate [target]`**
- **Purpose**: Evidence-based estimation
- **Wave Support**: No
- **MCP Servers**: Sequential, Context7, Serena
- **Sub-Agents**: ANALYZER, ARCHITECT
- **Example**: `/sc:estimate feature-authentication`

**`/sc:task [operation]`**
- **Purpose**: Long-term project management
- **Wave Support**: Yes (variable)
- **MCP Servers**: Sequential, Serena
- **Sub-Agents**: ANALYZER, ARCHITECT, domain specialists
- **Example**: `/sc:task create epic/user-authentication`

### Version Control Commands

**`/sc:git [operation]`**
- **Purpose**: Git workflow assistant
- **Wave Support**: No
- **MCP Servers**: Sequential, Serena
- **Sub-Agents**: DEVOPS, SCRIBE, QA
- **Example**: `/sc:git commit --message "feat: add authentication"`

### Meta Commands

**`/sc:index [query]`**
- **Purpose**: Command catalog browsing (this command)
- **Wave Support**: No
- **MCP Servers**: Serena
- **Sub-Agents**: ANALYZER, MENTOR
- **Example**: `/sc:index workflow web-app`

**`/sc:load [path]`**
- **Purpose**: Project context loading
- **Wave Support**: No
- **MCP Servers**: Serena, all available
- **Sub-Agents**: ANALYZER, ARCHITECT, SCRIBE
- **Example**: `/sc:load @project-root`

**`/sc:spawn [mode]`**
- **Purpose**: Task orchestration and delegation
- **Wave Support**: Yes (native)
- **MCP Servers**: All servers, Serena
- **Sub-Agents**: Any, based on task decomposition
- **Example**: `/sc:spawn --parallel --sub-agents 5`

---

## Shannon Commands (4)

**`/sh:analyze-spec [specification]`**
- **Purpose**: Automatic 8-dimensional specification analysis
- **Wave Support**: No
- **MCP Servers**: Serena, Sequential, Tavily, Context7
- **Sub-Agents**: ANALYZER, ARCHITECT
- **Output**: Complexity score, domain breakdown, MCP suggestions, 5-phase plan
- **Example**: `/sh:analyze-spec @requirements.md`

**`/sh:plan-phase [phase_number]`**
- **Purpose**: Structured 5-phase planning with validation gates
- **Wave Support**: No (prepares for wave execution)
- **MCP Servers**: Serena, Sequential
- **Sub-Agents**: ARCHITECT, domain planners
- **Output**: Phase objectives, todo list, sub-agent allocation, validation criteria
- **Example**: `/sh:plan-phase 3`

**`/sh:execute-wave [wave_definition]`**
- **Purpose**: Wave-based parallel orchestration
- **Wave Support**: Yes (native)
- **MCP Servers**: Serena, all relevant to wave tasks
- **Sub-Agents**: Variable, based on wave definition
- **Output**: Wave results from all parallel sub-agents
- **Example**: `/sh:execute-wave wave_2_implementation`

**`/sh:checkpoint`**
- **Purpose**: Session state preservation
- **Wave Support**: No
- **MCP Servers**: Serena (critical)
- **Sub-Agents**: None (utility command)
- **Output**: Checkpoint confirmation with timestamp
- **Example**: `/sh:checkpoint --before-risky-operation`

**`/sh:restore [checkpoint_id]`**
- **Purpose**: Context restoration from checkpoint
- **Wave Support**: No
- **MCP Servers**: Serena (critical)
- **Sub-Agents**: None (utility command)
- **Output**: Restored context confirmation
- **Example**: `/sh:restore checkpoint_20250929_143022`

**`/sh:status`**
- **Purpose**: Wave and session state monitoring
- **Wave Support**: No
- **MCP Servers**: Serena
- **Sub-Agents**: None (monitoring command)
- **Output**: Current wave, phase, progress, active sub-agents
- **Example**: `/sh:status --verbose`

---

## Wave Command Patterns

**Wave 1: Analysis**
```
/sh:analyze-spec → /sc:analyze → /sh:plan-phase 1
```

**Wave 2-4: Implementation**
```
/sh:execute-wave wave_2_frontend
/sh:execute-wave wave_3_backend
/sh:execute-wave wave_4_integration
```

**Wave 5: Validation**
```
/sc:test --functional → /sc:analyze --post-implementation
```

---

## Context-Aware Suggestions

Based on your project state: {project_state}

**Recommended Next Commands**:
1. {suggestion_1}
2. {suggestion_2}
3. {suggestion_3}
```

### Keyword Search Results

```markdown
# Search Results: "{query}"

**Matching Commands** (3):

## /sc:analyze - Multi-dimensional code analysis
**Relevance**: Primary match (command name)
**Wave Support**: Yes (full parallelization)
**MCP Servers**: Serena, Sequential, Context7
**Sub-Agents**: ANALYZER, ARCHITECT, PERFORMANCE, SECURITY, QA

**Usage**:
```bash
/sc:analyze src/ --comprehensive --wave-mode
```

**Common Patterns**:
- Quality assessment: `/sc:analyze src/ --focus quality`
- Security audit: `/sc:analyze . --focus security --deep`
- Performance profiling: `/sc:analyze api/ --focus performance`

**Integration**:
- After: `/sc:improve`, `/sc:cleanup`, `/sc:document`
- Before: Implementation planning, refactoring decisions

---

## /sh:analyze-spec - Specification analysis
**Relevance**: Secondary match (similar domain)
**Wave Support**: No
**MCP Servers**: Serena, Sequential, Tavily, Context7
**Sub-Agents**: ANALYZER, ARCHITECT

**Usage**:
```bash
/sh:analyze-spec @requirements.md
```

**Difference from /sc:analyze**:
- `/sh:analyze-spec`: Analyzes requirements documents, creates execution plan
- `/sc:analyze`: Analyzes existing code, identifies quality issues

**Workflow**:
```
/sh:analyze-spec (requirements) → /sh:plan-phase → /sh:execute-wave → /sc:analyze (code)
```

---

## Related Commands

**For deeper analysis**: `/sc:troubleshoot`, `/sc:explain`
**For improvements**: `/sc:improve`, `/sc:cleanup`
**For validation**: `/sc:test`
```

### Command Comparison

```markdown
# Command Comparison: /sc:analyze vs /sh:analyze-spec

## Side-by-Side Comparison

| Aspect | /sc:analyze | /sh:analyze-spec |
|--------|-------------|------------------|
| **Target** | Existing code | Requirements documents |
| **Purpose** | Code quality assessment | Project planning |
| **Output** | Quality findings, recommendations | Complexity score, execution plan |
| **Wave Support** | Yes (parallel domain analysis) | No (preparation for waves) |
| **MCP Servers** | Serena, Sequential, Context7 | Serena, Sequential, Tavily, Context7 |
| **Sub-Agents** | Domain specialists (5-7) | Planning agents (2-3) |
| **Typical Use** | Mid/late project | Project start |
| **Duration** | 5-30 minutes | 2-10 minutes |

## When to Use Each

**Use /sh:analyze-spec when**:
- Starting a new project
- Have requirements document
- Need complexity assessment
- Want structured execution plan
- Determining MCP servers needed

**Use /sc:analyze when**:
- Have existing codebase
- Need quality assessment
- Looking for improvements
- Debugging issues
- Preparing for refactoring

## Workflow Integration

**Typical Sequence**:
```
1. /sh:analyze-spec @requirements.md
   → Get complexity, domains, plan

2. /sh:plan-phase 1-5
   → Create detailed phase plans

3. /sh:execute-wave wave_X
   → Implement features

4. /sc:analyze src/
   → Assess implementation quality

5. /sc:improve src/ --based-on-analysis
   → Address findings
```

## Best Practices

- **Always start with /sh:analyze-spec** for new projects
- **Use /sc:analyze regularly** during development
- **Combine both** for comprehensive project understanding
- **Save results to Serena** for project memory
```

### Workflow Template

```markdown
# Workflow: Web Application Development

## Overview
**Use Case**: Building a full-stack web application
**Duration**: 4-8 weeks
**Waves**: 5-7 waves
**Commands Used**: 12 commands

---

## Phase 1: Discovery (Week 1)

**Commands**:
```bash
1. /sh:analyze-spec @project-requirements.md
   # Output: Complexity score, domain breakdown, MCP suggestions

2. /sc:load @project-root
   # Load any existing codebase or assets

3. /sh:plan-phase 1
   # Create detailed discovery phase plan
```

**Validation Gate**: Requirements signed off by stakeholders

---

## Phase 2: Architecture (Week 1-2)

**Commands**:
```bash
4. /sc:design system-architecture
   # Design overall system structure

5. /sc:design database-schema
   # Design data model

6. /sh:plan-phase 2
   # Create architecture phase plan
```

**Validation Gate**: Architecture review approved

---

## Phase 3: Implementation (Week 2-6)

**Wave 1: Foundation**
```bash
7. /sh:execute-wave wave_1_foundation
   # Setup: Database, authentication, core services
   # Sub-Agents: BACKEND (2), DATA_ENGINEER (1)
```

**Wave 2: Frontend**
```bash
8. /sh:execute-wave wave_2_frontend
   # Components: UI components, pages, state management
   # Sub-Agents: FRONTEND (3)
```

**Wave 3: Backend**
```bash
9. /sh:execute-wave wave_3_backend
   # APIs: REST endpoints, business logic, integrations
   # Sub-Agents: BACKEND (3)
```

**Wave 4: Integration**
```bash
10. /sh:execute-wave wave_4_integration
    # Connect frontend + backend, end-to-end flows
    # Sub-Agents: FRONTEND (1), BACKEND (1)
```

**Validation Gate**: All features implemented, integration complete

---

## Phase 4: Testing (Week 6-7)

**Commands**:
```bash
11. /sc:test --functional --comprehensive
    # Functional tests with Puppeteer (NO MOCKS)

12. /sc:analyze . --comprehensive --wave-mode
    # Quality assessment across all dimensions
```

**Validation Gate**: All tests pass, quality standards met

---

## Phase 5: Deployment (Week 7-8)

**Commands**:
```bash
13. /sc:git commit --all-changes
    # Commit final changes

14. /sc:document . --deployment-guide
    # Create deployment documentation

15. /sc:build --production --optimize
    # Production build
```

**Validation Gate**: Successful production deployment

---

## MCP Servers Used
- **Serena**: Context preservation (all phases)
- **Sequential**: Analysis and planning (phases 1-2, 4)
- **Context7**: Framework documentation (phases 2-3)
- **Magic**: UI component generation (phase 3)
- **Playwright**: Functional testing (phase 4)

## Sub-Agents Deployed
- **ANALYZER**: 2 times (spec analysis, quality analysis)
- **ARCHITECT**: 3 times (system design, architecture review)
- **FRONTEND**: 4 times (UI implementation, testing)
- **BACKEND**: 5 times (API implementation, services)
- **DATA_ENGINEER**: 2 times (database design, optimization)
- **QA**: 2 times (testing, quality validation)

## Success Metrics
- All 5 phases completed with gates passed
- 100% functional test coverage (NO MOCKS)
- Quality score >80/100 across all dimensions
- Zero critical security vulnerabilities
- Production deployment successful
```

---

## Examples

### Example 1: Find Testing Commands

**Command**:
```bash
/sc:index --domain testing
```

**Output**:
```markdown
# Commands for Domain: Testing

## Primary Testing Command

**`/sc:test [type]`**
- **Purpose**: Testing workflows with functional-first approach (NO MOCKS)
- **MCP Servers**: Playwright, Sequential, Serena
- **Sub-Agents**: QA
- **Examples**:
  - `/sc:test --functional` - Generate functional tests with Puppeteer
  - `/sc:test --e2e` - End-to-end user journey tests
  - `/sc:test --coverage` - Run tests with coverage analysis

## Related Commands for Testing

**`/sc:analyze [target] --focus testing`**
- Analyze test coverage and quality
- Identify testing gaps
- Recommend test improvements

**`/sc:implement test-suite --type functional`**
- Implement new functional test suite
- Follow NO MOCKS philosophy

## Shannon Testing Philosophy

**Functional Testing First - NO MOCKS**
- Web: Use Puppeteer MCP or Playwright MCP
- iOS: Use iOS Simulator with XCUITests
- Backend: Real HTTP requests, real databases

**Key Principle**: Test real behavior, not mocked approximations

## Workflow Example
```bash
/sc:analyze src/ --focus testing  # Identify gaps
/sc:test --generate-functional    # Create functional tests
/sc:test --run-all               # Execute test suite
```
```

### Example 2: Wave Command Discovery

**Command**:
```bash
/sc:index --wave-enabled
```

**Output**:
```markdown
# Wave-Enabled Commands (7)

Commands supporting parallel wave orchestration for faster execution.

## SuperClaude Wave Commands

1. **`/sc:analyze`** - Multi-dimensional analysis with parallel domain specialists
2. **`/sc:build`** - Build with conditional parallelization for multi-platform
3. **`/sc:design`** - Design with parallel domain designers
4. **`/sc:implement`** - Implementation with parallel domain workers
5. **`/sc:improve`** - Improvement with parallel quality specialists
6. **`/sc:task`** - Task management with variable wave support

## Shannon Wave Commands

7. **`/sh:execute-wave`** - Native wave orchestration command

## Wave Benefits

**Performance Gains**: 3-5x faster execution through true parallelism
**Pattern**: Independent sub-agents spawn in SINGLE message → parallel execution
**Coordination**: Serena MCP enables cross-wave context sharing

## Example Wave Pattern

```bash
# Wave 1: Analysis (parallel)
/sc:analyze src/ --wave-mode
# Spawns: ANALYZER, ARCHITECT, PERFORMANCE, SECURITY, QA (all parallel)

# Wave 2: Implementation (parallel)
/sh:execute-wave wave_2_frontend_backend
# Spawns: FRONTEND(3), BACKEND(3) (all parallel, 6 agents total)

# Wave 3: Integration (sequential, depends on Wave 2)
/sh:execute-wave wave_3_integration
# Spawns: Integration agents after Wave 2 completes
```

## When to Use Waves

✅ **Use waves when**:
- Multiple independent tasks
- Large codebase (>50 files)
- Multi-domain project
- Time-sensitive delivery

❌ **Don't use waves when**:
- Single file/small scope
- Sequential dependencies
- Simple operations
- Learning/exploration
```

### Example 3: Command Workflow for New Project

**Command**:
```bash
/sc:index workflow new-project
```

**Output**:
```markdown
# Workflow: Starting a New Project

## Prerequisites
- Requirements document or specification
- Project repository (empty or existing)
- Claude Code with Shannon Framework installed

## Step-by-Step Workflow

### Step 1: Specification Analysis
```bash
/sh:analyze-spec @requirements.md
```
**Output**:
- 8-dimensional complexity score
- Domain breakdown (frontend, backend, mobile, etc.)
- MCP server suggestions
- 5-phase execution plan
- Initial todo list (20-50 items)

**Next**: Review analysis, confirm understanding with stakeholders

---

### Step 2: Load Project Context
```bash
/sc:load @project-root
```
**Output**:
- Existing codebase analysis (if any)
- Framework detection
- Project structure understanding

**Next**: Validate project setup, create missing directories

---

### Step 3: Phase Planning
```bash
/sh:plan-phase 1  # Discovery
/sh:plan-phase 2  # Architecture
/sh:plan-phase 3  # Implementation
/sh:plan-phase 4  # Testing
/sh:plan-phase 5  # Deployment
```
**Output**: Detailed plans for each phase with:
- Objectives and activities
- Validation gates
- Sub-agent allocation
- MCP server usage
- Timeline estimates

**Next**: Review plans, adjust based on constraints

---

### Step 4: Discovery Phase Execution
```bash
/sc:design system-architecture
/sc:design database-schema
/sc:document architecture --diagrams
```
**Validation Gate**: Architecture approved? → Proceed
**Checkpoint**: `/sh:checkpoint --phase-1-complete`

---

### Step 5: Implementation Phase Execution
```bash
/sh:execute-wave wave_1_foundation
/sh:execute-wave wave_2_frontend
/sh:execute-wave wave_3_backend
/sh:execute-wave wave_4_integration
```
**Wave Pattern**: Parallel execution where independent
**Context Sharing**: All sub-agents read previous wave results via Serena
**Checkpoint**: `/sh:checkpoint --after-each-wave`

---

### Step 6: Testing Phase Execution
```bash
/sc:test --functional --generate-e2e
/sc:analyze . --comprehensive
```
**Testing Philosophy**: Functional tests only (NO MOCKS)
**Quality Validation**: Ensure all dimensions meet standards
**Checkpoint**: `/sh:checkpoint --testing-complete`

---

### Step 7: Deployment Phase
```bash
/sc:build --production
/sc:document --deployment-guide
/sc:git commit --final-release
```
**Final Validation**: All gates passed, production ready

---

## Timeline Estimate
- **Simple Project** (complexity <0.4): 1-2 weeks
- **Moderate Project** (complexity 0.4-0.7): 3-6 weeks
- **Complex Project** (complexity >0.7): 8-16 weeks

## MCP Servers Typically Needed
- **Serena** (mandatory): Context preservation
- **Sequential**: Analysis and planning
- **Context7**: Framework documentation
- **Magic**: UI generation (if web/mobile)
- **Playwright**: Functional testing (if web)
- **Tavily**: Research (if needed)

## Success Checklist
- [ ] Specification analyzed and understood
- [ ] All 5 phases planned with validation gates
- [ ] Architecture designed and approved
- [ ] Implementation complete with wave orchestration
- [ ] Functional tests passing (NO MOCKS)
- [ ] Quality analysis shows >80/100 score
- [ ] Documentation complete
- [ ] Production deployment successful
```

---

## Integration Points

### With SuperClaude Framework
- Inherits all SuperClaude commands
- Uses SuperClaude personas and MCP coordination
- Extends with Shannon /sh: commands
- Maintains backward compatibility

### With Shannon V3 System
- Lists Shannon-specific commands
- Shows wave orchestration patterns
- Integrates with checkpoint/restore system
- References Serena MCP requirements

### With MCP Servers
- Shows MCP usage per command
- Provides integration patterns
- Explains MCP fallback chains
- Helps discover appropriate MCPs

---

## Best Practices

### Using /sc:index Effectively

1. **Start with /sc:index** when unsure which command to use
2. **Search by domain** to find relevant commands quickly
3. **Check wave support** for large-scale operations
4. **Review workflows** for comprehensive project guidance
5. **Use comparisons** to understand command differences

### Command Discovery Strategy

```yaml
1. High-level question:
   /sc:index [keyword] → Find relevant commands

2. Understand capabilities:
   /sc:index [command] → Detailed command info

3. Compare alternatives:
   /sc:index [cmd1] vs [cmd2] → Side-by-side comparison

4. Find workflow:
   /sc:index workflow [use-case] → End-to-end guidance

5. Context-aware help:
   /sc:index → See suggestions based on project state
```

---

## Summary

The `/sc:index` command provides intelligent command discovery for the Shannon Framework:

✅ **Unified catalog** of 29 commands (SuperClaude + Shannon)
✅ **Wave-enabled identification** for parallel execution
✅ **MCP integration matrix** showing server usage
✅ **Sub-agent activation** patterns per command
✅ **Workflow templates** for common use cases
✅ **Context-aware suggestions** based on project state
✅ **Comparison tools** for understanding differences
✅ **Best practice guidance** for effective command usage

**Result**: Transform command discovery from documentation search into intelligent navigation, helping users find the right tools for their specific needs with Shannon Framework.