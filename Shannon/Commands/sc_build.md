---
name: sc_build
category: command
type: enhanced_superclaude
base_command: /build
shannon_version: 3.0.0
wave_enabled: true
description: Build command with wave orchestration, parallel builds, and NO MOCKS testing
---

# /sc:build - Enhanced Build Command

## Purpose Statement

**Base Functionality** (SuperClaude): Project builder with automatic framework detection, intelligent persona activation, and MCP integration for builds and UI generation.

**Shannon V3 Enhancements**: Wave-based parallel builds, mandatory NO MOCKS functional testing, Serena checkpoint integration, and cross-wave context sharing for zero-context-loss build workflows.

**Primary Use Case**: Build features, components, or complete applications with parallel sub-agent execution and real-world validation testing.

---

## Shannon V3 Enhancements

### What's New in Shannon

1. **Wave Orchestration for Parallel Builds**
   - Split build tasks across multiple waves
   - Sub-agents (IMPLEMENTATION_WORKER, FRONTEND, BACKEND) execute in parallel
   - Each wave completes before next wave starts
   - Cross-wave context via Serena MCP

2. **Mandatory NO MOCKS Testing**
   - All builds include functional tests
   - Web: Puppeteer MCP for real browser testing
   - iOS: XCUITests on actual simulator
   - Backend: Real HTTP requests with test database
   - NEVER use unittest.mock, jest.mock, or any mocking libraries

3. **Serena Checkpoint Integration**
   - Automatic checkpoints before each wave
   - PreCompact hook integration
   - Complete build state preserved
   - Restoration capability if context lost

4. **Intelligent Sub-Agent Activation**
   - IMPLEMENTATION_WORKER: Core build logic
   - FRONTEND: UI components (with Magic MCP)
   - BACKEND: APIs and services
   - TESTING_WORKER: Functional test creation
   - Platform-specific agents (iOS, Web) as needed

5. **Enhanced Output Format**
   - Wave-by-wave progress reporting
   - Real-time build status updates
   - Functional test results (NO MOCKS)
   - Deployment-ready artifacts

---

## Command Usage

### Basic Syntax
```bash
/sc:build [target] [@path] [--flags]
```

### Parameters

**target** (optional): What to build
- Component name: `LoginForm`, `Dashboard`, `UserProfile`
- Feature name: `authentication`, `payment-flow`, `admin-panel`
- Application scope: `entire-app`, `frontend`, `backend`

**@path** (optional): Target directory or file
- `@src/components/` - Build in components directory
- `@src/features/auth/` - Build authentication feature
- `@frontend/` - Build frontend application

**Flags**:
- `--type [component|api|service|feature]` - Specify build type
- `--framework <name>` - Specify framework (React, Vue, Angular, Express, etc.)
- `--no-tests` - Skip functional test creation (NOT RECOMMENDED)
- `--wave-count <n>` - Manual wave count (default: auto-calculated)
- `--single-wave` - Disable wave orchestration (sequential build)
- `--checkpoint-frequency <n>` - Checkpoint every N minutes (default: 15)

---

## Usage Patterns

### Pattern 1: Component Build (Single Wave)
```bash
/sc:build LoginForm @src/components/
```
**Execution**:
- Wave 1: FRONTEND agent builds component + functional test
- Output: LoginForm.tsx + LoginForm.test.js (Puppeteer)

### Pattern 2: Feature Build (Multi-Wave)
```bash
/sc:build authentication @src/features/auth/
```
**Execution**:
- Wave 1: IMPLEMENTATION_WORKER analyzes requirements
- Wave 2: FRONTEND builds UI components + BACKEND builds API endpoints
- Wave 3: TESTING_WORKER creates functional tests (browser + API tests)
- Wave 4: Integration validation

### Pattern 3: Full Application Build (Complex Multi-Wave)
```bash
/sc:build entire-app --framework React --type feature
```
**Execution**:
- Wave 1: Architecture planning (IMPLEMENTATION_WORKER)
- Wave 2: Frontend components (FRONTEND) + Backend APIs (BACKEND) in parallel
- Wave 3: Database schema + State management
- Wave 4: Functional test suite (TESTING_WORKER with Puppeteer MCP)
- Wave 5: Integration + deployment preparation

### Pattern 4: iOS Build
```bash
/sc:build UserProfileView @MyApp/Views/ --framework SwiftUI
```
**Execution**:
- Wave 1: IOS_SPECIALIST builds SwiftUI view
- Wave 2: TESTING_WORKER creates XCUITest on simulator (NO MOCKS)
- Output: UserProfileView.swift + UserProfileViewTests.swift

### Pattern 5: Backend API Build
```bash
/sc:build payment-api @src/routes/ --type api
```
**Execution**:
- Wave 1: BACKEND_SPECIALIST builds Express/FastAPI routes
- Wave 2: TESTING_WORKER creates functional HTTP tests (real database)
- Output: payment.routes.js + payment.routes.test.js (real HTTP, NO MOCKS)

---

## Execution Flow with Wave Integration

### Pre-Execution (Setup Phase)

**Step 1: Context Analysis**
- Load SuperClaude /build command base behavior
- Parse target and flags
- Determine build scope and complexity

**Step 2: Framework Detection**
- Scan package.json, pubspec.yaml, Podfile, etc.
- Identify primary framework (React, Vue, Flutter, SwiftUI, etc.)
- Load framework-specific patterns from Context7 MCP

**Step 3: Complexity Assessment**
- Calculate wave count based on scope
- Identify required sub-agents
- Generate wave execution plan

**Step 4: Serena Checkpoint Creation**
```javascript
// Automatic checkpoint before build starts
write_memory("build_checkpoint_initial", {
  target: "LoginForm",
  timestamp: "2025-09-30T10:30:00Z",
  framework: "React",
  wave_plan: ["Wave 1: Component build", "Wave 2: Functional test"]
});
```

---

### Wave Execution Pattern

**Wave Structure**:
```
Wave N:
  ├─ Pre-Wave Checkpoint (Serena MCP)
  ├─ Sub-Agent Activation (parallel)
  │   ├─ IMPLEMENTATION_WORKER: Core logic
  │   ├─ FRONTEND: UI components (if needed)
  │   └─ BACKEND: API routes (if needed)
  ├─ Context Sharing (Serena MCP)
  ├─ Output Validation
  └─ Post-Wave Checkpoint (Serena MCP)
```

**Example: Two-Wave Build**

**Wave 1: Component Implementation**
```yaml
Objective: Build LoginForm component
Sub-Agents: FRONTEND (primary)
MCP Tools: Magic MCP (UI generation), Context7 (React patterns)
Deliverables:
  - LoginForm.tsx (functional component)
  - LoginForm.module.css (styles)
Checkpoint: "build_wave1_complete"
```

**Wave 2: Functional Testing (NO MOCKS)**
```yaml
Objective: Create functional tests for LoginForm
Sub-Agents: TESTING_WORKER (primary)
MCP Tools: Puppeteer MCP (browser automation)
Deliverables:
  - LoginForm.test.js (Puppeteer functional test)
  - Test validates real form submission
  - Test validates real API calls (NO MOCKS)
Checkpoint: "build_wave2_complete"
```

---

### Cross-Wave Context Sharing (Serena MCP)

**Context Written in Wave 1** (by FRONTEND agent):
```javascript
write_memory("build_wave1_output", {
  component_name: "LoginForm",
  file_path: "src/components/LoginForm.tsx",
  props: ["onSubmit", "isLoading"],
  api_endpoint: "/api/auth/login",
  form_fields: ["email", "password"]
});
```

**Context Read in Wave 2** (by TESTING_WORKER agent):
```javascript
const wave1Output = read_memory("build_wave1_output");

// TESTING_WORKER now knows:
// - Component accepts onSubmit prop
// - Component calls /api/auth/login endpoint
// - Component has email and password fields
//
// Creates functional test WITHOUT MOCKS:
// - Real browser interaction (Puppeteer)
// - Real form typing
// - Real API call to /api/auth/login
```

**Result**: TESTING_WORKER creates accurate functional tests without needing to re-analyze component code.

---

### Post-Execution (Validation Phase)

**Step 1: Build Validation**
- Verify all deliverables created
- Run linters and type checkers
- Validate framework conventions

**Step 2: Functional Test Execution**
```bash
# Web builds
npm test -- LoginForm.test.js  # Puppeteer test

# iOS builds
xcodebuild test -scheme MyApp  # XCUITest on simulator

# Backend builds
npm test -- payment.routes.test.js  # Real HTTP test
```

**Step 3: Final Checkpoint**
```javascript
write_memory("build_complete", {
  status: "success",
  deliverables: ["LoginForm.tsx", "LoginForm.test.js"],
  tests_passing: true,
  functional_tests: true,  // NO MOCKS
  timestamp: "2025-09-30T10:45:00Z"
});
```

---

## Sub-Agent Integration

### Primary Sub-Agents for /sc:build

**IMPLEMENTATION_WORKER** (Wave Coordinator)
- **Role**: Build orchestration, core logic implementation
- **Activation**: All builds
- **Responsibilities**:
  - Wave planning
  - Dependency resolution
  - Cross-wave coordination
  - Architecture decisions

**FRONTEND** (UI Builder)
- **Role**: User interface implementation
- **Activation**: Web/iOS UI builds
- **Responsibilities**:
  - Component creation (with Magic MCP)
  - Styling implementation
  - State management
  - Accessibility compliance
- **MCP Tools**: Magic MCP (21st.dev components), Context7 (framework patterns)

**BACKEND_SPECIALIST** (API Builder)
- **Role**: Server-side implementation
- **Activation**: API/service builds
- **Responsibilities**:
  - Route implementation
  - Business logic
  - Database integration
  - API documentation
- **MCP Tools**: Context7 (Express/FastAPI patterns), Serena (API memory)

**TESTING_WORKER** (Functional Test Creator)
- **Role**: Functional test creation (NO MOCKS)
- **Activation**: All builds (unless --no-tests)
- **Responsibilities**:
  - Puppeteer test creation (web)
  - XCUITest creation (iOS)
  - API test creation (backend)
  - Test execution validation
- **MCP Tools**: Puppeteer MCP (web), Context7 (testing patterns)
- **Critical Rule**: NEVER use mocks, always test real functionality

**IOS_SPECIALIST** (iOS-Specific)
- **Role**: SwiftUI/UIKit implementation
- **Activation**: iOS builds
- **Responsibilities**:
  - Swift code generation
  - SwiftUI view implementation
  - Xcode project integration
  - Simulator testing
- **MCP Tools**: SwiftLens MCP (Swift analysis), Context7 (SwiftUI patterns)

**WEB_SPECIALIST** (Web-Specific)
- **Role**: Modern web stack implementation
- **Activation**: React/Vue/Angular builds
- **Responsibilities**:
  - Framework-specific patterns
  - Build tool configuration
  - Performance optimization
  - Browser compatibility
- **MCP Tools**: Magic MCP (components), Context7 (framework docs)

---

### Sub-Agent Coordination Example

**Scenario**: Build authentication feature

**Wave 1: Planning**
```yaml
Agent: IMPLEMENTATION_WORKER
Tasks:
  - Analyze authentication requirements
  - Identify components needed (LoginForm, AuthContext, API routes)
  - Create wave plan for parallel execution
Output:
  - write_memory("auth_plan", wave_plan)
```

**Wave 2: Parallel Implementation**
```yaml
Agent 1: FRONTEND (parallel)
Tasks:
  - Build LoginForm component
  - Build AuthContext provider
Output:
  - LoginForm.tsx, AuthContext.tsx
  - write_memory("frontend_output", component_details)

Agent 2: BACKEND_SPECIALIST (parallel)
Tasks:
  - Build /api/auth/login endpoint
  - Build /api/auth/logout endpoint
Output:
  - auth.routes.js, auth.controller.js
  - write_memory("backend_output", api_details)
```

**Wave 3: Functional Testing (NO MOCKS)**
```yaml
Agent: TESTING_WORKER
Tasks:
  - Read frontend_output and backend_output memories
  - Create Puppeteer test (real browser)
  - Test real login flow (no mocked API)
Output:
  - auth.e2e.test.js (Puppeteer functional test)
  - write_memory("test_results", test_status)
```

---

## NO MOCKS Testing Philosophy

### Critical Rules (Enforced by TESTING_WORKER)

**Rule 1**: NEVER use unittest.mock, jest.mock, sinon, etc.
**Rule 2**: ALWAYS test real user interactions
**Rule 3**: ALWAYS use real HTTP requests (no mock servers)
**Rule 4**: ALWAYS use real databases (test database with real schema)

### Testing by Platform

**Web Applications**:
```javascript
// ✅ CORRECT: Functional test with Puppeteer (NO MOCKS)
test('user can login', async () => {
  await page.goto('http://localhost:3000/login');
  await page.type('#email', 'user@example.com');
  await page.type('#password', 'password123');
  await page.click('button[type="submit"]');

  // Real browser, real typing, real HTTP request, real API response
  await page.waitForSelector('.dashboard');
  expect(await page.url()).toContain('/dashboard');
});

// ❌ WRONG: Mock-based test (FORBIDDEN)
test('user can login', async () => {
  const mockLogin = jest.fn().mockResolvedValue({success: true});
  // This doesn't test real behavior - NEVER DO THIS
});
```

**iOS Applications**:
```swift
// ✅ CORRECT: XCUITest on real simulator (NO MOCKS)
func testUserCanLogin() {
    let app = XCUIApplication()
    app.launch()

    app.textFields["Email"].tap()
    app.textFields["Email"].typeText("user@example.com")
    app.secureTextFields["Password"].typeText("password123")
    app.buttons["Login"].tap()

    // Real simulator, real UI, real API call, real navigation
    XCTAssert(app.otherElements["Dashboard"].waitForExistence(timeout: 5))
}

// ❌ WRONG: Mock API responses (FORBIDDEN)
// Never mock URLSession or API responses
```

**Backend APIs**:
```javascript
// ✅ CORRECT: Real HTTP test with real database (NO MOCKS)
test('POST /api/tasks creates task', async () => {
  const response = await fetch('http://localhost:3000/api/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title: 'Test Task'})
  });

  // Real HTTP, real database write, real response
  expect(response.status).toBe(201);

  const task = await response.json();
  expect(task.title).toBe('Test Task');

  // Verify in real database
  const dbTask = await db.tasks.findById(task.id);
  expect(dbTask.title).toBe('Test Task');
});

// ❌ WRONG: Mocked database (FORBIDDEN)
jest.mock('./database');  // NEVER DO THIS
```

---

## Output Format

### Wave Progress Report

```
🌊 WAVE 1: Component Implementation
═══════════════════════════════════════════════════════════════

📍 Checkpoint: build_wave1_start (saved to Serena)
⏱️  Started: 2025-09-30 10:30:00

🤖 Active Sub-Agents:
  ├─ FRONTEND (primary)
  └─ IMPLEMENTATION_WORKER (coordinator)

🛠️  MCP Tools:
  ├─ Magic MCP: UI component generation
  └─ Context7 MCP: React patterns

📦 Deliverables:
  ✅ src/components/LoginForm.tsx (created)
  ✅ src/components/LoginForm.module.css (created)

💾 Context Saved:
  └─ build_wave1_output (Serena memory)

✅ Wave 1 Complete
⏱️  Duration: 2m 15s
```

```
🌊 WAVE 2: Functional Testing (NO MOCKS)
═══════════════════════════════════════════════════════════════

📍 Checkpoint: build_wave2_start (saved to Serena)
⏱️  Started: 2025-09-30 10:32:15

🤖 Active Sub-Agents:
  ├─ TESTING_WORKER (primary)
  └─ IMPLEMENTATION_WORKER (coordinator)

🛠️  MCP Tools:
  └─ Puppeteer MCP: Browser automation

📖 Context Loaded:
  └─ build_wave1_output (from Wave 1)

📦 Deliverables:
  ✅ src/components/LoginForm.test.js (created)
  ✅ Functional test: user can submit login form
  ✅ Functional test: form validates email format
  ✅ Functional test: form shows loading state

🧪 Test Execution:
  ✅ All functional tests passing (3/3)
  ✅ Real browser testing with Puppeteer
  ✅ Real API calls (NO MOCKS)

💾 Context Saved:
  └─ build_wave2_output (Serena memory)

✅ Wave 2 Complete
⏱️  Duration: 3m 45s
```

### Final Build Summary

```
═══════════════════════════════════════════════════════════════
  BUILD COMPLETE: LoginForm
═══════════════════════════════════════════════════════════════

📊 Summary:
  ├─ Total Waves: 2
  ├─ Total Duration: 6m 0s
  ├─ Sub-Agents Used: 2
  └─ MCP Tools: Magic, Context7, Puppeteer

📂 Files Created:
  ├─ src/components/LoginForm.tsx (182 lines)
  ├─ src/components/LoginForm.module.css (45 lines)
  └─ src/components/LoginForm.test.js (78 lines)

🧪 Testing:
  ├─ Test Type: Functional (NO MOCKS)
  ├─ Test Tool: Puppeteer MCP
  ├─ Tests Created: 3
  └─ Tests Passing: 3/3 ✅

💾 Serena Checkpoints:
  ├─ build_checkpoint_initial
  ├─ build_wave1_output
  ├─ build_wave2_output
  └─ build_complete

🚀 Next Steps:
  1. Run: npm test LoginForm.test.js
  2. Integrate: Import LoginForm in parent component
  3. Deploy: Component ready for production
```

---

## Examples

### Example 1: Simple Component Build

**Command**:
```bash
/sc:build Button @src/components/ --framework React
```

**Execution**:
- Single wave (low complexity)
- FRONTEND agent builds component
- TESTING_WORKER creates Puppeteer test
- Output: Button.tsx + Button.test.js

### Example 2: Feature Build with Backend

**Command**:
```bash
/sc:build task-management @src/features/tasks/
```

**Execution**:
- Wave 1: IMPLEMENTATION_WORKER plans architecture
- Wave 2: FRONTEND builds TaskList/TaskForm + BACKEND builds /api/tasks routes
- Wave 3: TESTING_WORKER creates E2E tests (Puppeteer + real HTTP)
- Output: 8 files (components, routes, tests)

### Example 3: iOS View Build

**Command**:
```bash
/sc:build SettingsView @MyApp/Views/ --framework SwiftUI
```

**Execution**:
- Wave 1: IOS_SPECIALIST builds SwiftUI view
- Wave 2: TESTING_WORKER creates XCUITest
- Output: SettingsView.swift + SettingsViewTests.swift

### Example 4: Full-Stack Feature

**Command**:
```bash
/sc:build authentication --type feature
```

**Execution**:
- Wave 1: Architecture planning
- Wave 2: Frontend components + Backend API routes (parallel)
- Wave 3: Database schema + JWT middleware
- Wave 4: Functional test suite (browser + API tests, NO MOCKS)
- Output: 15+ files (complete authentication system)

---

## Integration with SuperClaude

### Base Functionality Preserved

**From SuperClaude /build**:
- ✅ Automatic framework detection
- ✅ Intelligent persona activation (Frontend/Backend/Architect)
- ✅ MCP integration (Magic for UI, Context7 for patterns)
- ✅ Tool orchestration (Read, Edit, MultiEdit, Bash)

**Shannon Additions**:
- ✅ Wave-based parallel execution
- ✅ Mandatory NO MOCKS testing
- ✅ Serena checkpoint integration
- ✅ Cross-wave context sharing
- ✅ Platform-specific sub-agents (iOS, Web, Backend)

### Persona Coordination

**SuperClaude Personas** (still active):
- Frontend persona → Enhanced by FRONTEND sub-agent
- Backend persona → Enhanced by BACKEND_SPECIALIST sub-agent
- Architect persona → Enhanced by IMPLEMENTATION_WORKER sub-agent

**Shannon Sub-Agents** (work alongside personas):
- Sub-agents handle wave orchestration
- Personas provide domain expertise
- Both access same Serena context

---

## Notes

- **Type this command in Claude Code conversation window**, not terminal
- **Serena MCP required**: Shannon's zero-context-loss architecture depends on Serena
- **NO MOCKS mandatory**: All tests must be functional (real browser, real HTTP, real database)
- **Wave count auto-calculated**: Based on build complexity, override with --wave-count if needed
- **Checkpoint frequency**: Default 15 minutes, critical builds use 5-10 minutes
- **PreCompact integration**: Automatic checkpoint before Claude Code auto-compacts context
- **Context preservation**: All wave outputs saved to Serena, accessible to all sub-agents
- **Platform detection**: Automatically activates iOS_SPECIALIST (iOS), WEB_SPECIALIST (web), etc.
- **Framework patterns**: Context7 MCP provides official framework best practices
- **Parallel execution**: Multiple sub-agents work simultaneously when no dependencies exist

---

## Quality Standards

### Build Quality
- ✅ Code follows framework conventions
- ✅ Components are production-ready
- ✅ No TODO comments for core functionality
- ✅ Proper error handling implemented
- ✅ Accessibility requirements met (web/iOS)

### Testing Quality (NO MOCKS)
- ✅ Functional tests validate real behavior
- ✅ Tests use real browser (Puppeteer) or simulator (XCUITest)
- ✅ Tests make real HTTP requests (no mock servers)
- ✅ Tests use real database (test schema)
- ✅ NO usage of unittest.mock, jest.mock, sinon, or any mocking library

### Context Preservation
- ✅ Checkpoint created before each wave
- ✅ All wave outputs saved to Serena
- ✅ Complete state restorable if context lost
- ✅ PreCompact hook prevents data loss

---

## Related Commands

- `/sc:spec` - Analyze specification before building
- `/sc:plan` - Generate 5-phase plan before building
- `/sc:test` - Create additional functional tests
- `/sc:implement` - Implementation with different workflow
- `/analyze` - Analyze existing build quality