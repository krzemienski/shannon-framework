---
name: sc:implement
description: Feature and code implementation with wave orchestration, NO MOCKS testing, context preservation, and intelligent persona activation
category: implementation
complexity: advanced
triggers: [implement, build, create, code, develop, feature]
mcp_servers: [serena, magic, context7, sequential]
personas: [frontend, backend, architect, security]
auto_activate: false
base_command: /implement
enhancements: [wave_orchestration, context_preservation, no_mocks_mandate, serena_integration]
---

# /sc:implement - Enhanced Implementation Command

> **Shannon V3 Enhancement**: SuperClaude's `/implement` command enhanced with wave orchestration for parallel implementation, mandatory NO MOCKS testing philosophy, Serena context preservation, and IMPLEMENTATION_WORKER sub-agent activation.

## Purpose Statement

Feature and code implementation with systematic intelligence and quality guarantees:

- **Wave-Based Parallel Implementation** - Multiple features/components implemented simultaneously by specialized sub-agents
- **NO MOCKS Mandate** - Functional testing only, zero tolerance for fake implementations or stub code
- **Context Preservation** - All implementation decisions and code saved to Serena MCP for cross-wave access
- **Working Code Guarantee** - Every function fully implemented, no placeholders, no TODO comments
- **Intelligent Persona Activation** - Auto-selects domain experts (Frontend, Backend, Security, etc.)
- **MCP Coordination** - Magic for UI, Context7 for patterns, Sequential for complex logic
- **Quality Validation** - Automated testing, lint checks, type validation before completion

**What Makes This Different**: SuperClaude's `/implement` executes sequentially with manual testing. Shannon's `/sc:implement` orchestrates parallel waves of specialized sub-agents, enforces NO MOCKS testing, and preserves complete context for iterative development.

## Shannon V3 Enhancements Over SuperClaude

### 1. Wave Orchestration (NEW)
**SuperClaude**: Sequential implementation, one component at a time
**Shannon**: Parallel waves with IMPLEMENTATION_WORKER and domain specialists

```yaml
wave_1_parallel:
  - frontend-specialist → UI components
  - backend-specialist → API endpoints
  - database-specialist → Schema/migrations

wave_2_parallel:
  - integration-specialist → Connect components
  - test-specialist → Functional tests

wave_3_validation:
  - wave-coordinator → Aggregate & validate
```

### 2. NO MOCKS Testing (MANDATORY)
**SuperClaude**: Testing approach undefined
**Shannon**: Mandatory functional testing with real dependencies

```yaml
testing_mandate:
  - NO mocking libraries (jest.mock, sinon, etc.)
  - NO stub implementations
  - YES functional tests (Playwright for web)
  - YES simulators (Xcode for iOS, Android Studio)
  - YES real backend calls (test databases)
```

### 3. Context Preservation (NEW)
**SuperClaude**: Context lost on auto-compact
**Shannon**: Complete state saved to Serena MCP

```yaml
serena_integration:
  - write_memory("wave_N_implementation", results)
  - read_memory("previous_waves") before starting
  - Cross-wave context access for all agents
  - Implementation decisions preserved
```

### 4. IMPLEMENTATION_WORKER Activation (NEW)
**SuperClaude**: Generic implementation
**Shannon**: Specialized sub-agent with production code focus

```yaml
worker_activation:
  role: "Production code builder"
  mandate: "Complete implementations only"
  validation: "No TODOs, no stubs, no mocks"
```

## Usage Patterns

**Basic Usage**:
```
/sc:implement [feature-description]
/sc:implement "User authentication with JWT"
/sc:implement @specs/auth-feature.md
```

**With Type Specification**:
```
/sc:implement [feature] --type component
/sc:implement [feature] --type api
/sc:implement [feature] --type service
/sc:implement [feature] --type feature
```

**With Framework**:
```
/sc:implement [feature] --framework react
/sc:implement [feature] --framework express
/sc:implement [feature] --framework nextjs
```

**With Wave Control**:
```
/sc:implement [feature] --waves 3
/sc:implement [feature] --parallel-components
/sc:implement [feature] --sequential (disable waves)
```

**Type in Claude Code conversation window** (not terminal)

## Activation Triggers

`/sc:implement` activates when user requests **ANY** of:

**Implementation Keywords**:
- **Primary**: "implement", "build", "create", "develop", "code", "write"
- **Secondary**: "add feature", "create component", "build API", "develop service"

**Feature Descriptions**:
- "Implement user authentication"
- "Build dashboard component"
- "Create REST API endpoints"
- "Develop real-time chat feature"

**File Attachments**:
- Implementation specs: `@feature-spec.md`
- Design files: `@ui-mockups.pdf`
- API contracts: `@api-spec.yaml`

**Type Detection** (auto-selects implementation type):
```yaml
component: "component", "widget", "UI", "interface", "button", "form"
api: "endpoint", "route", "API", "REST", "GraphQL", "controller"
service: "service", "worker", "job", "processor", "handler"
feature: "feature", "capability", "functionality", "system"
```

## Execution Flow with Wave Integration

### Phase 1: Context Loading & Planning (MANDATORY)

**Step 1.1: Load Previous Context**
```
EXECUTE FIRST before any implementation:

1. list_memories() - Discover available project memories
2. read_memory("specification_analysis") - Get spec from /sh:spec
3. read_memory("phase_plan") - Load current phase details
4. read_memory("previous_wave_results") - Check prior implementations
5. think_about_collected_information() - Assess context completeness

IF NO specification_analysis found:
  → Suggest running /sh:spec first
  → Explain value of systematic planning
  → Proceed only if user confirms manual approach
```

**Step 1.2: Implementation Planning**
```
Based on loaded context, create implementation plan:

1. Identify implementation type (component|api|service|feature)
2. Determine domain (frontend|backend|database|mobile)
3. Assess complexity (simple: 1 wave, moderate: 2-3 waves, complex: 4+ waves)
4. Select appropriate MCP servers
5. Activate domain-specific personas
6. Calculate parallel work opportunities

Output: Structured plan with waves, sub-agents, dependencies
```

**Step 1.3: Wave Structure Decision**
```yaml
simple_implementation:
  waves: 1
  pattern: "Single agent, sequential execution"
  example: "Simple React component"

moderate_implementation:
  waves: 2-3
  pattern: "2-3 parallel agents per wave"
  example: "API + UI + database"

complex_implementation:
  waves: 4+
  pattern: "3-5 parallel agents per wave"
  example: "Multi-service feature with real-time"
```

### Phase 2: Wave Execution (Parallel Sub-Agents)

**Wave 1: Core Implementation**
```yaml
parallel_agents:
  agent_1: IMPLEMENTATION_WORKER
    role: "Production code builder"
    focus: "Primary implementation logic"
    tools: [Write, Edit, MultiEdit, Context7]
    output: write_memory("wave_1_core_implementation")

  agent_2: [Domain Specialist - auto-selected]
    examples:
      - frontend-specialist (UI/components)
      - backend-specialist (APIs/services)
      - database-specialist (schema/migrations)
    tools: [Magic (UI), Context7 (patterns), Write, Edit]
    output: write_memory("wave_1_domain_implementation")

  agent_3: [Secondary Specialist - if needed]
    condition: complexity > 0.6
    role: "Supporting implementation"
    output: write_memory("wave_1_secondary_implementation")

dependency_management:
  - All agents read previous wave results
  - No agent proceeds without dependency completion
  - Context shared via Serena memories
```

**Wave 2: Integration & Testing**
```yaml
parallel_agents:
  agent_1: integration-specialist
    role: "Connect wave 1 components"
    input: read_memory("wave_1_*")
    tools: [Edit, MultiEdit, Bash (for validation)]
    output: write_memory("wave_2_integration")

  agent_2: test-specialist
    role: "Functional tests (NO MOCKS)"
    mandate: |
      - Web → Playwright tests
      - iOS → XCTest with simulator
      - Android → Espresso tests
      - API → Real HTTP calls to test DB
    tools: [Write (tests), Bash (test execution), Playwright MCP]
    output: write_memory("wave_2_tests")

validation_gates:
  - All wave 1 code compiles/runs
  - Integration points validated
  - Functional tests passing
```

**Wave 3: Validation & Quality (if needed)**
```yaml
sequential_execution:
  coordinator: wave-coordinator
    role: "Aggregate results, validate completeness"
    input: read_memory("wave_1_*"), read_memory("wave_2_*")
    checks:
      - ✓ No TODO comments in code
      - ✓ No placeholder implementations
      - ✓ All functions fully implemented
      - ✓ Tests use NO mocking libraries
      - ✓ Code passes lint/type checks
      - ✓ Integration tests pass

  output: write_memory("implementation_complete", {
    status: "complete|needs_fixes",
    code_files: ["list of created/modified files"],
    test_files: ["list of test files"],
    validation_results: {checks},
    next_steps: ["if fixes needed"]
  })
```

### Phase 3: Context Preservation & Completion

**Step 3.1: Save Implementation State**
```
write_memory("implementation_[feature-name]", {
  feature: "description",
  type: "component|api|service|feature",
  waves_executed: N,
  files_created: ["array"],
  files_modified: ["array"],
  tests_created: ["array"],
  validation_results: {object},
  dependencies: ["array"],
  next_phase_ready: boolean,
  timestamp: "ISO-8601"
})
```

**Step 3.2: Quality Validation**
```
Execute mandatory quality checks:

1. Bash("npm run lint") OR equivalent linter
2. Bash("npm run typecheck") OR equivalent type checker
3. Bash("npm test") OR equivalent test runner
4. Review output for failures

IF any checks fail:
  → Mark implementation incomplete
  → Create TodoWrite items for fixes
  → DO NOT proceed to completion

IF all checks pass:
  → Mark implementation complete
  → Save final state to Serena
  → Report deliverables to user
```

**Step 3.3: Deliverables Report**
```
Present to user:

## Implementation Complete ✅

**Feature**: [name]
**Type**: [component|api|service|feature]
**Domain**: [frontend|backend|etc.]

### Files Created/Modified:
- path/to/file1.ts (142 lines)
- path/to/file2.tsx (89 lines)
- path/to/file3.test.ts (67 lines)

### Tests:
- ✓ Functional tests (NO MOCKS)
- ✓ Integration tests
- ✓ [Platform-specific: Playwright/XCTest/Espresso]

### Quality Checks:
- ✓ Lint: Passed
- ✓ Type Check: Passed
- ✓ Tests: 15/15 passing

### Context Saved:
- Memory: implementation_[feature-name]
- Available for: Future waves, iterations, debugging

### Next Steps:
[Suggest logical next phase or iteration]
```

## Sub-Agent Integration

### Primary Agent: IMPLEMENTATION_WORKER

**Activation**: Automatic for all `/sc:implement` commands

**Configuration**:
```yaml
name: implementation-worker
category: implementation
mandate: |
  - Every function fully implemented
  - NO TODO comments in production code
  - NO placeholder implementations
  - NO stub methods
  - All logic complete and functional

context_loading:
  - ALWAYS read_memory("specification_analysis")
  - ALWAYS read_memory("phase_plan")
  - ALWAYS read_memory("previous_wave_*")

output:
  - write_memory("wave_N_core_implementation", {
      component: "name",
      files: ["array"],
      implementation_complete: true,
      no_todos: true,
      no_stubs: true
    })
```

### Domain Specialists (Auto-Selected)

**Frontend Specialist**:
```yaml
triggers: [UI, component, React, Vue, interface, design]
mcp_servers: [magic, context7]
tools: [Magic (21st.dev components), Context7 (React patterns)]
focus: ["User interfaces", "Component architecture", "Accessibility"]
```

**Backend Specialist**:
```yaml
triggers: [API, endpoint, service, Express, FastAPI]
mcp_servers: [context7, sequential]
tools: [Context7 (backend patterns), Sequential (API design)]
focus: ["REST/GraphQL APIs", "Business logic", "Data validation"]
```

**Database Specialist**:
```yaml
triggers: [schema, migration, query, PostgreSQL, MongoDB]
mcp_servers: [context7]
focus: ["Schema design", "Migrations", "Query optimization"]
```

**Mobile Specialist**:
```yaml
triggers: [iOS, Android, SwiftUI, Jetpack Compose]
mcp_servers: [context7]
focus: ["Mobile UI", "Platform APIs", "Offline-first"]
```

### Wave Coordinator

**Role**: Orchestrate parallel agents, aggregate results, validate completeness

**Responsibilities**:
```yaml
pre_wave:
  - Assign sub-agents to tasks
  - Ensure dependency order
  - Distribute context via Serena

during_wave:
  - Monitor progress (via memory reads)
  - Detect blockers
  - Coordinate handoffs

post_wave:
  - Aggregate all agent outputs
  - Validate completeness (NO TODOs, NO stubs)
  - Check integration points
  - Decide next wave or completion
```

## NO MOCKS Testing Philosophy (MANDATORY)

### Core Principle

**Shannon Mandate**: NEVER use mocking libraries or fake implementations in tests.

**Rationale**:
- Mocks test mocking code, not real behavior
- Functional tests catch real integration issues
- Tests should validate actual system behavior
- Real dependencies reveal actual problems

### Testing by Platform

**Web Applications**:
```yaml
framework: Playwright (via Playwright MCP)
approach: |
  - Launch real browser (Chrome/Firefox/Safari)
  - Interact with actual rendered UI
  - Validate real API calls
  - Use test database (Docker container)

example:
  - Playwright: browser.navigate(), page.click()
  - NO jest.mock()
  - NO sinon stubs
```

**iOS Applications**:
```yaml
framework: XCTest
approach: |
  - Run tests in Xcode Simulator
  - Use real UIKit/SwiftUI rendering
  - Real network calls to test API

example:
  - XCTestCase with XCUIApplication()
  - Real simulator, real views, real data
```

**Android Applications**:
```yaml
framework: Espresso / Compose Testing
approach: |
  - Run on Android Emulator
  - Real Activity/Fragment rendering
  - Real backend integration

example:
  - Espresso for view interactions
  - Real emulator, real UI, real API
```

**Backend APIs**:
```yaml
approach: |
  - Spin up test database (Docker/in-memory)
  - Make real HTTP requests
  - Validate actual responses

example:
  - Docker PostgreSQL for tests
  - Real HTTP calls via fetch/axios
  - Validate actual DB state
```

### What This Means in Practice

**❌ NEVER Do This**:
```typescript
// BAD: Mocking
jest.mock('./api/userService');
const mockGetUser = jest.fn().mockResolvedValue({id: 1});
```

**✅ ALWAYS Do This**:
```typescript
// GOOD: Functional test with Playwright
test('user can login', async ({page}) => {
  await page.goto('http://localhost:3000/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## Tool Orchestration

### Primary Tools by Phase

**Implementation Phase**:
```yaml
code_creation:
  - Write: New files
  - Edit: Modify existing files
  - MultiEdit: Bulk changes across files

ui_components:
  - Magic MCP: Generate modern UI components

patterns:
  - Context7 MCP: Framework-specific patterns

complex_logic:
  - Sequential MCP: Multi-step reasoning
```

**Testing Phase**:
```yaml
functional_tests:
  - Write: Create test files
  - Playwright MCP: Web UI testing
  - Bash: Run test suites (npm test, pytest, etc.)
```

**Validation Phase**:
```yaml
quality_checks:
  - Bash: npm run lint
  - Bash: npm run typecheck
  - Bash: npm test
  - Read: Review outputs
```

**Context Management**:
```yaml
serena_operations:
  - list_memories(): Discover available context
  - read_memory(): Load previous implementations
  - write_memory(): Save implementation results
  - think_about_collected_information(): Validate context
```

## Output Format

### During Execution

**Wave Start Notification**:
```
🌊 Wave 1: Core Implementation (3 parallel agents)

Agent 1: IMPLEMENTATION_WORKER
  → Focus: Core feature logic
  → Files: src/features/auth/login.ts

Agent 2: frontend-specialist
  → Focus: UI components
  → Files: src/components/LoginForm.tsx

Agent 3: backend-specialist
  → Focus: API endpoints
  → Files: src/api/routes/auth.ts

⏳ Estimated: 5-8 minutes
```

**Wave Progress Updates**:
```
✅ Agent 1 complete: login.ts (89 lines)
✅ Agent 2 complete: LoginForm.tsx (142 lines)
🔄 Agent 3 in progress: auth.ts (67% complete)
```

**Wave Completion**:
```
✅ Wave 1 Complete

Results:
- Files created: 3
- Lines of code: 348
- Tests created: 0 (next wave)
- Context saved: wave_1_core_implementation

Proceeding to Wave 2: Integration & Testing...
```

### Final Deliverables Report

```markdown
# Implementation Complete: [Feature Name] ✅

## Summary
**Type**: [component|api|service|feature]
**Domain**: [frontend|backend|database|mobile]
**Complexity**: [simple|moderate|complex]
**Waves Executed**: N
**Duration**: Xm Ys

## Deliverables

### Code Files
- ✅ src/features/auth/login.ts (89 lines)
  - Complete authentication logic
  - Input validation
  - Error handling

- ✅ src/components/LoginForm.tsx (142 lines)
  - Accessible form component
  - Real-time validation
  - Loading states

- ✅ src/api/routes/auth.ts (67 lines)
  - POST /auth/login endpoint
  - JWT token generation
  - Session management

### Test Files (NO MOCKS ✓)
- ✅ tests/auth/login.spec.ts (48 lines)
  - Playwright functional tests
  - Real browser interactions
  - Actual API calls to test DB

- ✅ tests/api/auth.test.ts (34 lines)
  - Real HTTP requests
  - Docker PostgreSQL test DB
  - Integration validation

## Quality Validation

### Lint Check ✅
```
> npm run lint
✓ No linting errors
```

### Type Check ✅
```
> npm run typecheck
✓ No type errors
```

### Test Suite ✅
```
> npm test
✓ 12/12 tests passing
✓ All functional tests (NO MOCKS)
✓ Integration tests passing
```

## Context Preservation

### Saved to Serena MCP:
- `implementation_user_authentication`
- `wave_1_core_implementation`
- `wave_2_integration_tests`

### Available For:
- Future iterations
- Related features
- Debugging sessions
- Team knowledge sharing

## Architecture Decisions

1. **JWT over sessions**: Stateless auth for API scalability
2. **bcrypt for passwords**: Industry standard, future-proof
3. **Refresh token pattern**: Better UX, security boundary

## Next Steps

### Immediate:
- ✅ Feature ready for staging deployment
- ⏳ Consider rate limiting for /auth/login
- ⏳ Add password reset flow

### Future Enhancements:
- OAuth2 social login (GitHub, Google)
- Multi-factor authentication
- Session management dashboard

## Files Modified
- `src/features/auth/login.ts` (NEW, 89 lines)
- `src/components/LoginForm.tsx` (NEW, 142 lines)
- `src/api/routes/auth.ts` (NEW, 67 lines)
- `tests/auth/login.spec.ts` (NEW, 48 lines)
- `tests/api/auth.test.ts` (NEW, 34 lines)
- `src/api/routes/index.ts` (MODIFIED, +2 lines)

**Total**: 5 new files, 1 modified file, 392 lines of production code
```

## Examples

### Example 1: Simple Component Implementation

**User Input**:
```
/sc:implement "Create a reusable Button component with loading state"
```

**Execution**:
```yaml
wave_1:
  agent: implementation-worker + frontend-specialist
  mcp: magic (for component patterns)
  output:
    - src/components/Button.tsx (78 lines)
    - src/components/Button.test.tsx (42 lines, Playwright)
    - Fully accessible (ARIA labels)
    - Loading spinner animation
    - NO TODOs, complete implementation

validation:
  - ✓ Lint passed
  - ✓ Type check passed
  - ✓ 8/8 Playwright tests passing

context_saved: implementation_button_component
```

### Example 2: API Endpoint Implementation

**User Input**:
```
/sc:implement "Add /api/users/:id endpoint with CRUD operations" --framework express
```

**Execution**:
```yaml
wave_1:
  agent: implementation-worker + backend-specialist
  mcp: context7 (Express patterns)
  output:
    - src/api/routes/users.ts (124 lines)
      - GET /api/users/:id
      - PUT /api/users/:id
      - DELETE /api/users/:id
    - src/api/middleware/validation.ts (45 lines)
    - Full error handling
    - Input validation (Zod)

wave_2:
  agent: test-specialist
  output:
    - tests/api/users.test.ts (89 lines)
      - Real HTTP requests
      - Docker PostgreSQL test DB
      - NO MOCKS
    - ✓ All CRUD operations validated

context_saved: implementation_users_api
```

### Example 3: Complex Feature (Multi-Wave)

**User Input**:
```
/sc:implement @specs/real-time-chat.md --waves 4
```

**Execution**:
```yaml
wave_1_parallel:
  agent_1: frontend-specialist
    output: Chat UI components (React)
  agent_2: backend-specialist
    output: WebSocket server (Socket.io)
  agent_3: database-specialist
    output: Message schema + migrations

wave_2_parallel:
  agent_1: implementation-worker
    output: Message persistence logic
  agent_2: frontend-specialist
    output: Real-time message updates

wave_3_parallel:
  agent_1: integration-specialist
    output: Connect frontend ↔ backend
  agent_2: test-specialist
    output: Functional tests (Playwright)

wave_4_validation:
  coordinator: wave-coordinator
    checks:
      - ✓ Messages persist to DB
      - ✓ Real-time updates work
      - ✓ Multiple users tested
      - ✓ NO TODOs, NO stubs
      - ✓ Functional tests passing

context_saved: implementation_real_time_chat
```

## Integration with Shannon Commands

### Typical Workflow

**Step 1**: Specification Analysis
```
/sh:spec "Build task management app..."
→ Creates comprehensive roadmap with phases
→ Saves to Serena: specification_analysis
```

**Step 2**: Implementation (this command)
```
/sc:implement "Phase 1: Core task CRUD operations"
→ Reads specification_analysis from Serena
→ Implements with wave orchestration
→ Saves to Serena: implementation_task_crud
```

**Step 3**: Checkpoint Progress
```
/sh:checkpoint
→ Saves complete project state
→ Includes all implementations
→ Enables restore on auto-compact
```

**Step 4**: Continue Development
```
/sc:implement "Phase 2: Task assignment system"
→ Reads previous implementations
→ Builds on existing code
→ Maintains consistency
```

### Context Flow

```
/sh:spec
  ↓ writes
Serena: specification_analysis
  ↓ reads
/sc:implement (Wave 1)
  ↓ writes
Serena: wave_1_implementation
  ↓ reads
/sc:implement (Wave 2)
  ↓ writes
Serena: wave_2_implementation
  ↓ reads
/sh:checkpoint
  ↓ writes
Serena: project_checkpoint
```

## Validation & Quality Gates

### Mandatory Pre-Completion Checks

**Code Quality**:
```yaml
- ☐ NO TODO comments in production code
- ☐ NO placeholder implementations
- ☐ NO "Not implemented" errors
- ☐ All functions fully implemented
- ☐ Error handling present
- ☐ Input validation complete
```

**Testing Quality**:
```yaml
- ☐ NO mocking libraries used
- ☐ Functional tests present (Playwright/XCTest/Espresso)
- ☐ Tests validate real behavior
- ☐ Integration tests passing
- ☐ Test coverage reasonable (>70%)
```

**Code Standards**:
```yaml
- ☐ Lint check passes
- ☐ Type check passes (if TypeScript)
- ☐ Build succeeds
- ☐ Follows project conventions
```

**Context Preservation**:
```yaml
- ☐ Implementation saved to Serena
- ☐ Architecture decisions documented
- ☐ Next steps identified
- ☐ Memory keys named consistently
```

### Failure Handling

**If Quality Checks Fail**:
```
1. DO NOT mark implementation complete
2. Create TodoWrite items for specific failures
3. Provide clear fix instructions
4. Maintain wave context for retry
5. Suggest /sc:implement --retry after fixes
```

**If Tests Fail**:
```
1. Review test output in detail
2. Identify root cause (code vs test issue)
3. Fix implementation OR fix test (NOT mock it out)
4. Re-run validation
5. Only mark complete when passing
```

## Best Practices

### For Developers Using This Command

1. **Always run /sh:spec first** for complex features (gets better results)
2. **Let waves run automatically** (don't force sequential unless debugging)
3. **Trust NO MOCKS philosophy** (functional tests catch real issues)
4. **Review context between waves** (use /sh:status to check memories)
5. **Checkpoint after major features** (use /sh:checkpoint regularly)

### For Framework Developers

1. **Enforce NO MOCKS in all agents** (critical for quality)
2. **Validate completeness rigorously** (no TODOs, no stubs)
3. **Save rich context to Serena** (enables iteration)
4. **Test wave coordination carefully** (parallel execution is complex)
5. **Provide clear progress updates** (users should see wave progress)

## Related Commands

- `/sh:spec` - Analyze specifications before implementing (recommended first step)
- `/sh:checkpoint` - Save implementation progress for restoration
- `/sh:status` - View current implementation state and wave progress
- `/sh:restore` - Recover implementation context after auto-compact
- `/sc:test` - Run comprehensive test validation (uses NO MOCKS philosophy)
- `/sc:improve` - Enhance existing implementations with quality focus

---

**Shannon V3 Context Framework** | Implementation Enhancement Module