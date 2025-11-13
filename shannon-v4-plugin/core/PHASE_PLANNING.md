---
name: PHASE_PLANNING
description: Behavioral instructions for 5-phase planning with validation gates and systematic project execution
category: core
version: 3.0.0
---

# Phase Planning System

## Purpose Statement

This document defines the behavioral patterns Claude follows when planning multi-phase implementations in Shannon V3. It provides structured templates for decomposing projects into 5 distinct phases with clear validation gates, effort distribution guidelines, and transition logic.

**Core Philosophy**: Systematic execution through structured phases reduces rework, prevents scope creep, and ensures quality through validation gates.

**When to Use**: Apply 5-phase planning for any project with complexity score ≥0.3 or requiring >8 hours of work.

---

## 5-Phase Structure Overview

Shannon V3 uses a standardized 5-phase approach with fixed effort distribution:

```
Phase 1: DISCOVERY     (20% effort) - Requirements finalization
Phase 2: ARCHITECTURE  (15% effort) - System design
Phase 3: IMPLEMENTATION(45% effort) - Parallel wave execution
Phase 4: TESTING       (15% effort) - Functional validation
Phase 5: DEPLOYMENT    (5% effort)  - Production release
```

**Validation Gates**: Each phase ends with a mandatory gate requiring user approval before proceeding.

**Progressive Refinement**: Early phases focus on clarity, later phases on execution.

---

## Phase 1: Discovery (20% Effort)

### Objectives
- Finalize all project requirements
- Resolve ambiguities and unknowns
- Create comprehensive user stories
- Confirm technical approach
- Verify all required tools/MCPs available

### Activities

**Requirements Documentation** (30% of phase)
```
Sub-Agent: requirements-analyst
Tools: Write, Read
MCPs: None required

Activities:
1. Extract all features from specification
2. Prioritize features (P0/P1/P2/P3)
3. Identify functional vs non-functional requirements
4. Document constraints (time, resources, technical)
5. List assumptions explicitly

Deliverable: requirements.md
Template:
  # Project Requirements
  ## Functional Requirements
  - [P0] Feature description with acceptance criteria
  - [P1] Feature description with acceptance criteria

  ## Non-Functional Requirements
  - Performance: Response time <200ms
  - Security: Authentication + authorization

  ## Constraints
  - Timeline: Must complete in X days
  - Resources: Solo developer

  ## Assumptions
  - User has Node.js installed
  - Database can be PostgreSQL
```

**Technical Research** (25% of phase)
```
Sub-Agent: system-architect
Tools: Read, WebSearch, Glob
MCPs: Context7 (framework documentation)

Activities:
1. Research suggested technology stack
2. Validate framework versions are compatible
3. Find official documentation for major libraries
4. Identify potential technical risks
5. Confirm all technologies can integrate

Deliverable: tech_stack_analysis.md
Template:
  # Technology Stack Analysis

  ## Selected Technologies
  - Frontend: React 18.2 (rationale)
  - Backend: Express 4.18 (rationale)
  - Database: PostgreSQL 15 (rationale)

  ## Compatibility Matrix
  [Table showing version compatibility]

  ## Technical Risks
  - Risk 1: Description + mitigation
  - Risk 2: Description + mitigation

  ## Documentation Sources
  - React: https://react.dev (Context7 available)
  - Express: https://expressjs.com (Context7 available)
```

**User Story Creation** (20% of phase)
```
Sub-Agent: requirements-analyst
Tools: Write
MCPs: None required

Activities:
1. Convert features into user stories
2. Write acceptance criteria for each story
3. Add story points (Fibonacci: 1,2,3,5,8,13)
4. Group stories into epics
5. Prioritize stories within epics

Deliverable: user_stories.md
Template:
  # User Stories

  ## Epic 1: User Authentication

  ### Story 1.1: User Registration
  **As a** new user
  **I want** to create an account with email/password
  **So that** I can access the application

  **Acceptance Criteria**:
  - Email validation (proper format)
  - Password strength requirements (8+ chars, special char)
  - Duplicate email rejection
  - Success confirmation email sent

  **Story Points**: 5
  **Priority**: P0
```

**MCP Verification** (15% of phase)
```
Sub-Agent: None (direct action)
Tools: Bash
MCPs: All suggested from spec analysis

Activities:
1. List currently installed MCPs (claude mcp list)
2. Identify missing MCPs from spec analysis suggestions
3. Install missing MCPs (claude mcp add [server])
4. Test each MCP with simple operation
5. Document MCP readiness

Deliverable: mcp_ready.md
Template:
  # MCP Server Status

  ## Installed and Tested
  ✅ Serena MCP - Tested: list_memories()
  ✅ Magic MCP - Tested: simple component
  ✅ Puppeteer MCP - Tested: navigate to example.com

  ## Installation Required
  ⚠️ PostgreSQL MCP - Run: claude mcp add postgresql

  ## Not Available
  ❌ CustomMCP - Alternative: Use native approach
```

**Discovery Review** (10% of phase)
```
Activities:
1. Review all deliverables for completeness
2. Verify all ambiguities resolved
3. Confirm user stories have acceptance criteria
4. Check technical stack is feasible
5. Prepare validation gate presentation

Output: Summary document for user review
```

### Phase 1 Validation Gate

**Gate Criteria** (ALL must be satisfied):
```
☐ requirements.md complete with all features listed
☐ All ambiguities from spec analysis resolved
☐ User stories written (minimum 15 stories)
☐ Every story has clear acceptance criteria
☐ Technical stack selected with rationale
☐ All required MCP servers confirmed available
☐ No blocking unknowns remain
```

**User Approval Required**:
```
Present to user:
- requirements.md
- user_stories.md
- tech_stack_analysis.md
- mcp_ready.md

Request explicit approval:
"Phase 1 (Discovery) complete. All requirements documented, technical
approach confirmed, and tools ready. Proceed to Phase 2 (Architecture)?"

If approved → Proceed to Phase 2
If not approved → Iterate on Phase 1 based on feedback
```

**Save Phase Completion**:
```
write_memory("phase_1_complete", {
  timestamp: [ISO timestamp],
  duration: "6.4 hours actual vs 6.4 hours planned",
  deliverables: ["requirements.md", "user_stories.md", "tech_stack_analysis.md", "mcp_ready.md"],
  validation_gate_status: "APPROVED",
  user_feedback: "[any notes from user]",
  next_phase: "Phase 2: Architecture"
})
```

---

## Phase 2: Architecture (15% Effort)

### Objectives
- Design complete system architecture
- Create database schema with relationships
- Define all API contracts (OpenAPI spec)
- Plan component hierarchy (frontend)
- Design testing strategy (NO MOCKS)
- Identify parallelization opportunities

### Activities

**System Architecture Design** (35% of phase)
```
Sub-Agent: system-architect
Tools: Write, Read
MCPs: Sequential (structured analysis), Context7 (architectural patterns)

Activities:
1. Create high-level system diagram (components + connections)
2. Define service boundaries (if microservices)
3. Document data flow between components
4. Specify external integrations (APIs, services)
5. Plan authentication/authorization flow
6. Design error handling strategy

Deliverable: architecture.md + system_diagram.png
Template:
  # System Architecture

  ## High-Level Overview
  [ASCII diagram showing components]

  ## Components
  ### Frontend (React SPA)
  - Responsibilities: UI rendering, user input, API calls
  - Technology: React 18, React Router, Redux Toolkit
  - Entry point: src/App.tsx

  ### Backend (Express API)
  - Responsibilities: Business logic, data validation, DB access
  - Technology: Express 4, TypeScript, JWT auth
  - Entry point: src/server.ts

  ## Data Flow
  1. User action → React component
  2. Component dispatches Redux action
  3. Action makes API call to Express
  4. Express validates + queries PostgreSQL
  5. Response → Redux store → Component re-renders

  ## Security Architecture
  - JWT tokens (15min expiry, refresh tokens)
  - Password hashing: bcrypt (10 rounds)
  - HTTPS required in production
  - CORS: Whitelist specific origins
```

**Database Schema Design** (25% of phase)
```
Sub-Agent: system-architect
Tools: Write, Read
MCPs: PostgreSQL (if available), Context7 (database patterns)

Activities:
1. Identify all entities from requirements
2. Define tables with columns (types, constraints)
3. Establish relationships (1:1, 1:N, M:N)
4. Add indexes for performance
5. Plan migrations strategy
6. Document sample queries

Deliverable: database_schema.sql + schema_diagram.png
Template:
  -- Database Schema

  -- Users table
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX idx_users_email ON users(email);

  -- Sessions table (1:N relationship with users)
  CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX idx_sessions_user_id ON sessions(user_id);
  CREATE INDEX idx_sessions_token ON sessions(token);
```

**API Contract Design** (25% of phase)
```
Sub-Agent: system-architect
Tools: Write, Read
MCPs: Context7 (REST/GraphQL patterns)

Activities:
1. List all required endpoints
2. Define request/response schemas for each
3. Specify HTTP methods and status codes
4. Document authentication requirements
5. Add example requests/responses
6. Create OpenAPI/Swagger spec

Deliverable: api_contracts.yaml (OpenAPI 3.0)
Template:
  openapi: 3.0.0
  info:
    title: Project API
    version: 1.0.0

  paths:
    /api/auth/register:
      post:
        summary: Register new user
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                    format: email
                  password:
                    type: string
                    minLength: 8
        responses:
          201:
            description: User created
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    userId:
                      type: integer
                    message:
                      type: string
          400:
            description: Invalid input
          409:
            description: Email already exists
```

**Component Hierarchy Design** (Frontend, 10% of phase)
```
Sub-Agent: frontend-specialist
Tools: Write, Read
MCPs: Magic (UI patterns), Context7 (React patterns)

Activities:
1. Design component tree structure
2. Identify reusable components
3. Plan state management approach (props vs global)
4. Define component interfaces (TypeScript)
5. List required third-party components

Deliverable: component_hierarchy.md
Template:
  # Component Hierarchy

  ## Top-Level Structure
  App
  ├── AuthProvider (context)
  ├── Router
  │   ├── PublicRoute
  │   │   ├── LoginPage
  │   │   └── RegisterPage
  │   └── PrivateRoute
  │       ├── DashboardPage
  │       │   ├── Header
  │       │   ├── Sidebar
  │       │   └── MainContent
  │       └── ProfilePage

  ## Reusable Components
  - Button (variants: primary, secondary, danger)
  - Input (types: text, email, password, with validation)
  - Modal (generic modal wrapper)
  - Card (content container)

  ## State Management
  - Global: Redux Toolkit (auth state, user profile)
  - Local: useState (form inputs, UI toggles)
```

**Testing Strategy Design** (5% of phase)
```
Sub-Agent: qa-specialist
Tools: Write, Read
MCPs: Puppeteer (browser testing), Context7 (testing patterns)

Activities:
1. Define testing layers (unit, integration, e2e)
2. Specify NO MOCKS mandate compliance
3. Plan functional test scenarios
4. List required test utilities
5. Design test data management

Deliverable: testing_strategy.md
Template:
  # Testing Strategy

  ## Testing Philosophy
  **NO MOCKS**: All tests use real implementations
  - Database: Test database (isolated, cleared between tests)
  - API: Real Express server running in test mode
  - Browser: Real browser via Puppeteer MCP

  ## Testing Layers
  ### Unit Tests (30%)
  - Pure functions (utils, helpers)
  - NO mocking of dependencies
  - Example: Password validation function

  ### Integration Tests (40%)
  - API endpoints with real database
  - Example: POST /api/auth/register actually creates user

  ### End-to-End Tests (30%)
  - Full user flows in real browser
  - Example: Complete registration → login → dashboard flow
  - Tool: Puppeteer MCP

  ## Test Data Management
  - Factory functions for test data creation
  - Database seeding scripts
  - Cleanup after each test (TRUNCATE tables)
```

### Phase 2 Validation Gate

**Gate Criteria** (ALL must be satisfied):
```
☐ System architecture diagram complete with all components
☐ Database schema designed (all tables, relationships, indexes)
☐ API contracts documented (OpenAPI spec with examples)
☐ Component hierarchy designed (frontend structure)
☐ Testing strategy documented (NO MOCKS confirmed)
☐ Parallelization opportunities identified
☐ All design decisions have rationale
```

**User Approval Required**:
```
Present to user:
- architecture.md with system diagram
- database_schema.sql with schema diagram
- api_contracts.yaml (OpenAPI spec)
- component_hierarchy.md
- testing_strategy.md

Request explicit approval:
"Phase 2 (Architecture) complete. System design finalized with database
schema, API contracts, and testing strategy. Proceed to Phase 3 (Implementation)?"

If approved → Proceed to Phase 3
If not approved → Iterate on Phase 2 based on feedback
```

**Save Phase Completion**:
```
write_memory("phase_2_complete", {
  timestamp: [ISO timestamp],
  duration: "4.8 hours actual vs 4.8 hours planned",
  deliverables: ["architecture.md", "database_schema.sql", "api_contracts.yaml", "component_hierarchy.md", "testing_strategy.md"],
  validation_gate_status: "APPROVED",
  design_decisions: ["JWT auth chosen over sessions", "PostgreSQL over MongoDB"],
  parallelization_plan: "Frontend and backend can develop in parallel (Wave 2a and 2b)",
  next_phase: "Phase 3: Implementation"
})
```

---

## Phase 3: Implementation (45% Effort)

### Objectives
- Execute all development work
- Build frontend + backend + database in parallel waves
- Integrate components systematically
- Implement all features from user stories
- Follow architecture and API contracts

### Wave Structure Planning

**Wave Determination Logic**:
```
Load from spec_analysis:
- Domain percentages
- Complexity score

Rules:
1. If domain >= 30% → Gets dedicated wave
2. If domain < 30% → Merge with related domain
3. Independent domains → Parallel waves
4. Dependent domains → Sequential waves

Example (Chat Application):
  Frontend: 45% → Wave 3a (parallel)
  Backend: 36% → Wave 3b (parallel)
  Database: 14% → Included in Wave 3b
  Integration: N/A → Wave 3c (sequential, after 3a+3b)
```

**Wave Execution Patterns**:
```
Pattern 1: Two Parallel Waves + Integration
Wave 3a: Frontend (parallel)
Wave 3b: Backend + Database (parallel)
Wave 3c: Integration (sequential)

Pattern 2: Three Parallel Waves + Integration
Wave 3a: Frontend (parallel)
Wave 3b: Backend (parallel)
Wave 3c: Database (parallel)
Wave 3d: Integration (sequential)

Pattern 3: Sequential (Low Complexity)
Wave 3a: All implementation (sequential)
```

### Wave 3a: Frontend Implementation (Example)

**Assigned Sub-Agents**:
```
- frontend-specialist (primary)
- ui-component-builder (Magic MCP)
- state-manager (Redux setup)
```

**Context Loading** (MANDATORY):
```
EVERY sub-agent MUST load:
1. list_memories()
2. read_memory("spec_analysis")
3. read_memory("phase_1_complete")
4. read_memory("phase_2_complete")
5. read_memory("component_hierarchy")
6. read_memory("api_contracts")
```

**Implementation Tasks**:
```
1. Project Setup (10%)
   - Create React app structure
   - Configure TypeScript
   - Set up Redux Toolkit
   - Install dependencies

2. Component Development (60%)
   - Build reusable components (Button, Input, Modal)
   - Create page components (Login, Register, Dashboard)
   - Implement state management (Redux slices)
   - Add routing (React Router)
   - Use Magic MCP for complex UI components

3. API Integration (20%)
   - Create API client (axios/fetch wrapper)
   - Implement API calls matching contracts
   - Add error handling
   - Connect Redux actions to API

4. Styling (10%)
   - Apply CSS/Tailwind/Material-UI
   - Ensure responsive design
   - Add loading states
   - Implement accessibility (ARIA labels)
```

**Deliverables**:
```
- Complete React application (src/ directory)
- All components functional
- API integration layer working
- README with setup instructions
```

### Wave 3b: Backend + Database Implementation (Example)

**Assigned Sub-Agents**:
```
- backend-specialist (primary)
- database-architect (PostgreSQL MCP)
- api-builder (Express setup)
```

**Context Loading** (MANDATORY):
```
Same as Wave 3a - MUST load all previous phase context
```

**Implementation Tasks**:
```
1. Project Setup (10%)
   - Create Express app structure
   - Configure TypeScript
   - Set up PostgreSQL connection
   - Install dependencies

2. Database Setup (15%)
   - Run schema migrations
   - Create seed data for development
   - Set up database client (pg/Sequelize/Prisma)
   - Test database connection

3. API Development (60%)
   - Implement all endpoints from api_contracts.yaml
   - Add request validation (Zod/Joi)
   - Implement authentication (JWT)
   - Add authorization middleware
   - Implement business logic
   - Connect to database (queries)

4. Error Handling (10%)
   - Global error handler
   - Validation error responses
   - Database error handling
   - Logging setup

5. Security (5%)
   - CORS configuration
   - Rate limiting
   - Input sanitization
   - Security headers (Helmet)
```

**Deliverables**:
```
- Complete Express application (server/ directory)
- All API endpoints functional
- Database schema applied
- README with setup instructions
```

### Wave 3c: Integration (Sequential after 3a+3b)

**Timing**: Executes AFTER Wave 3a AND Wave 3b complete

**Assigned Sub-Agents**:
```
- integration-specialist (primary)
- qa-specialist (testing)
```

**Context Loading** (MANDATORY):
```
MUST load:
1. All Phase 1 and Phase 2 context
2. read_memory("wave_3a_complete") - Frontend results
3. read_memory("wave_3b_complete") - Backend results
```

**Integration Tasks**:
```
1. Environment Setup (10%)
   - Configure environment variables
   - Set up database for testing
   - Configure API base URL in frontend

2. Integration Testing (40%)
   - Start backend server
   - Start frontend dev server
   - Test API calls from frontend
   - Verify authentication flow works
   - Test all major user flows
   - Fix integration issues

3. Documentation (20%)
   - Update README with full setup instructions
   - Document API endpoints
   - Create deployment guide
   - Add troubleshooting section

4. Code Review (20%)
   - Review frontend code quality
   - Review backend code quality
   - Check code style consistency
   - Verify all TODOs removed

5. Final Polish (10%)
   - Fix any remaining bugs
   - Optimize performance
   - Clean up console logs
   - Verify all features working
```

**Deliverables**:
```
- Fully integrated application
- All features working end-to-end
- Complete documentation
- Ready for testing phase
```

### Phase 3 Validation Gate

**Gate Criteria** (ALL must be satisfied):
```
☐ All frontend components built and functional
☐ All backend API endpoints implemented
☐ Database schema applied successfully
☐ Frontend and backend integrated (API calls working)
☐ Authentication/authorization working
☐ All P0 user stories implemented
☐ No critical bugs or errors
☐ Code quality meets standards (linting passes)
```

**Integration Verification**:
```
Run integration checklist:
1. Start backend server → No errors
2. Start frontend dev server → No errors
3. Open browser → Application loads
4. Test registration flow → User created in DB
5. Test login flow → JWT token received
6. Test authenticated endpoint → Data retrieved
7. Test logout → Token invalidated

All steps must pass.
```

**User Approval Required**:
```
Present to user:
- Demo of working application (video/screenshots)
- List of implemented features
- Integration test results
- Any known issues or limitations

Request explicit approval:
"Phase 3 (Implementation) complete. All features implemented and
integrated. Application functional. Proceed to Phase 4 (Testing)?"

If approved → Proceed to Phase 4
If not approved → Fix issues, re-integrate
```

**Save Phase Completion**:
```
write_memory("phase_3_complete", {
  timestamp: [ISO timestamp],
  duration: "14.4 hours actual vs 14.4 hours planned",
  waves_executed: ["wave_3a_frontend", "wave_3b_backend", "wave_3c_integration"],
  parallelization_gain: "40% time saved vs sequential",
  deliverables: ["frontend/", "backend/", "integration_docs.md"],
  validation_gate_status: "APPROVED",
  features_completed: 25,
  known_issues: [],
  next_phase: "Phase 4: Testing"
})
```

---

## Phase 4: Testing (15% Effort)

### Objectives
- Execute comprehensive functional testing (NO MOCKS)
- Validate all user stories with acceptance criteria
- Perform end-to-end testing in real browser
- Test edge cases and error scenarios
- Ensure application meets quality standards

### Activities

**Functional Test Development** (40% of phase)
```
Sub-Agent: qa-specialist
Tools: Write, Read, Bash
MCPs: Puppeteer (browser testing), PostgreSQL (database setup)

Activities:
1. Set up test environment (test database, test server)
2. Create test data factories (no mocks, real data)
3. Write integration tests for all API endpoints
4. Write end-to-end tests for user flows
5. Test authentication and authorization
6. Test error handling and edge cases

Deliverable: tests/ directory with comprehensive test suite
Structure:
  tests/
  ├── integration/
  │   ├── auth.test.ts (real API, real DB)
  │   ├── users.test.ts
  │   └── sessions.test.ts
  ├── e2e/
  │   ├── registration.test.ts (Puppeteer)
  │   ├── login.test.ts (Puppeteer)
  │   └── dashboard.test.ts (Puppeteer)
  └── helpers/
      ├── testDatabase.ts (DB setup/teardown)
      ├── testServer.ts (Express setup)
      └── factories.ts (test data creation)
```

**Test Execution** (30% of phase)
```
Sub-Agent: qa-specialist
Tools: Bash, Read
MCPs: Puppeteer (E2E tests)

Activities:
1. Run all integration tests
2. Run all E2E tests in real browser
3. Document test results
4. Identify failing tests
5. Create bug reports for failures

Process:
$ npm run test:integration
$ npm run test:e2e

Track results:
✅ 45/50 tests passing (90%)
❌ 5 tests failing:
  - auth.test.ts: "Should reject weak passwords"
  - login.test.ts: "Should handle network errors"
  - dashboard.test.ts: "Should load user data on mount"
```

**Bug Fixing** (25% of phase)
```
Sub-Agent: implementation-specialist
Tools: Edit, Read, Bash
MCPs: None (fixing existing code)

Activities:
1. Investigate each failing test
2. Fix identified bugs
3. Re-run tests to verify fixes
4. Ensure no regressions introduced

Bug Fix Process:
1. Read failing test
2. Understand expected behavior
3. Debug actual behavior
4. Fix code
5. Run single test: npm test -- auth.test.ts
6. Run full suite: npm run test:integration
7. Verify 100% pass rate
```

**Test Documentation** (5% of phase)
```
Activities:
1. Document test coverage
2. List all tested scenarios
3. Note any untested edge cases
4. Create test maintenance guide

Deliverable: test_results.md
Template:
  # Test Results

  ## Test Coverage
  - Integration Tests: 25 tests, 100% pass rate
  - E2E Tests: 15 tests, 100% pass rate
  - Total: 40 tests, 100% pass rate

  ## Tested Scenarios
  ✅ User registration with valid data
  ✅ User registration with duplicate email
  ✅ User login with correct credentials
  ✅ User login with incorrect credentials
  ✅ Protected route access without token
  ✅ Protected route access with valid token
  [... all scenarios ...]

  ## Known Limitations
  - Performance testing not included
  - Security penetration testing not included
  - Load testing not included

  ## Test Maintenance
  - Run before each commit: npm run test
  - Run before each deploy: npm run test:full
  - Update tests when API changes
```

### Phase 4 Validation Gate

**Gate Criteria** (ALL must be satisfied):
```
☐ All integration tests passing (100%)
☐ All E2E tests passing (100%)
☐ All user stories validated against acceptance criteria
☐ NO MOCKS used in any tests
☐ Edge cases tested
☐ Error handling validated
☐ Authentication/authorization tested
☐ Test documentation complete
```

**Quality Verification**:
```
Run quality checklist:
1. Code coverage >= 80% → Check coverage report
2. All tests use real implementations → Manual verification
3. No console.error in test runs → Check test output
4. All user stories have tests → Cross-reference stories
5. Test suite runs in < 5 minutes → Time execution

All criteria must pass.
```

**User Approval Required**:
```
Present to user:
- test_results.md (all tests passing)
- Test coverage report
- Demo of E2E tests running in browser (video)
- List of validated user stories

Request explicit approval:
"Phase 4 (Testing) complete. All tests passing, all user stories
validated. Application quality verified. Proceed to Phase 5 (Deployment)?"

If approved → Proceed to Phase 5
If not approved → Add more tests, fix issues
```

**Save Phase Completion**:
```
write_memory("phase_4_complete", {
  timestamp: [ISO timestamp],
  duration: "4.8 hours actual vs 4.8 hours planned",
  deliverables: ["tests/", "test_results.md", "coverage_report.html"],
  validation_gate_status: "APPROVED",
  test_stats: {
    total_tests: 40,
    passing: 40,
    failing: 0,
    coverage: "85%"
  },
  no_mocks_verified: true,
  next_phase: "Phase 5: Deployment"
})
```

---

## Phase 5: Deployment (5% Effort)

### Objectives
- Deploy application to staging environment
- Verify deployment successful
- Create deployment documentation
- Prepare for production release

### Activities

**Deployment Preparation** (30% of phase)
```
Sub-Agent: devops-specialist
Tools: Write, Read, Bash
MCPs: None (deployment scripts)

Activities:
1. Create deployment scripts
2. Configure environment variables
3. Set up hosting platform (Vercel, Heroku, AWS)
4. Configure database (production instance)
5. Set up CI/CD (if required)

Deliverable: deployment_guide.md
Template:
  # Deployment Guide

  ## Prerequisites
  - Node.js 18+
  - PostgreSQL 15+
  - Environment variables configured

  ## Staging Deployment
  1. Set environment variables:
     - DATABASE_URL=postgresql://...
     - JWT_SECRET=...
     - FRONTEND_URL=...

  2. Deploy backend:
     $ cd backend
     $ npm run build
     $ npm start

  3. Deploy frontend:
     $ cd frontend
     $ npm run build
     $ npm run preview

  ## Production Deployment
  [Production-specific steps]
```

**Staging Deployment** (50% of phase)
```
Sub-Agent: devops-specialist
Tools: Bash, Read
MCPs: None

Activities:
1. Run deployment scripts
2. Deploy backend to staging
3. Deploy frontend to staging
4. Apply database migrations
5. Verify deployment health

Deployment Process:
$ ./scripts/deploy-staging.sh

Verify:
- Backend health check: curl https://api-staging.example.com/health
- Frontend loads: https://staging.example.com
- Database connected: Check backend logs
- API functional: Test registration endpoint
```

**Deployment Verification** (15% of phase)
```
Sub-Agent: qa-specialist
Tools: Bash, Read
MCPs: Puppeteer (smoke testing)

Activities:
1. Run smoke tests on staging
2. Test critical user flows
3. Verify environment variables correct
4. Check logging/monitoring working
5. Document any deployment issues

Smoke Test Checklist:
✅ Homepage loads
✅ Registration works
✅ Login works
✅ Dashboard accessible
✅ API endpoints responding
✅ Database queries working
```

**Documentation Update** (5% of phase)
```
Activities:
1. Update README with deployment info
2. Document environment variables
3. Add troubleshooting section
4. Create runbook for operations

Deliverable: Updated README.md and RUNBOOK.md
```

### Phase 5 Validation Gate

**Gate Criteria** (ALL must be satisfied):
```
☐ Application deployed to staging successfully
☐ All smoke tests passing on staging
☐ Environment variables configured correctly
☐ Database migrations applied successfully
☐ Logging/monitoring operational
☐ Deployment documentation complete
☐ Rollback procedure documented
```

**Production Readiness Checklist**:
```
☐ Security review completed
☐ Performance acceptable (<2s page load)
☐ Error tracking configured (Sentry/Rollbar)
☐ Database backups configured
☐ SSL/TLS certificates valid
☐ CORS configured correctly
☐ Rate limiting in place
☐ Health check endpoints working
```

**User Approval Required**:
```
Present to user:
- Staging URL for testing
- deployment_guide.md
- Smoke test results
- Production readiness checklist

Request explicit approval:
"Phase 5 (Deployment) complete. Application deployed to staging and
verified. Ready for production release?"

If approved → Project complete!
If not approved → Address deployment issues
```

**Save Phase Completion**:
```
write_memory("phase_5_complete", {
  timestamp: [ISO timestamp],
  duration: "1.6 hours actual vs 1.6 hours planned",
  deliverables: ["deployment_guide.md", "RUNBOOK.md"],
  validation_gate_status: "APPROVED",
  staging_url: "https://staging.example.com",
  production_ready: true,
  deployment_issues: [],
  next_steps: "Production deployment (outside Shannon scope)"
})
```

---

## Effort Distribution Guidelines

### Baseline Distribution (Standard Project)

```
Total Project Time: T hours

Phase 1 (Discovery):     20% = 0.20 * T
Phase 2 (Architecture):  15% = 0.15 * T
Phase 3 (Implementation): 45% = 0.45 * T
Phase 4 (Testing):       15% = 0.15 * T
Phase 5 (Deployment):     5% = 0.05 * T
```

### Adjustment Factors

**Complexity-Based Adjustments**:
```
Simple (0.0-0.3):
- Discovery:     15% (less unknowns)
- Architecture:  10% (simpler design)
- Implementation: 55% (more straightforward coding)
- Testing:       15% (fewer edge cases)
- Deployment:     5%

Complex (0.7-0.85):
- Discovery:     25% (more unknowns)
- Architecture:  20% (complex design)
- Implementation: 35% (parallel waves offset complexity)
- Testing:       15% (same rigor)
- Deployment:     5%

Critical (0.85-1.0):
- Discovery:     30% (extensive research)
- Architecture:  25% (very complex design)
- Implementation: 25% (high coordination overhead)
- Testing:       15% (rigorous validation)
- Deployment:     5%
```

**Domain-Based Adjustments**:
```
If Database-Heavy (Database >= 30%):
- Architecture: +5% (schema design critical)
- Implementation: -5% (offset from architecture)

If Frontend-Heavy (Frontend >= 50%):
- Implementation: +5% (UI work time-consuming)
- Testing: +5% (E2E tests take time)
- Architecture: -5% (simpler backend)
- Deployment: -5% (static hosting simpler)

If Backend-Heavy (Backend >= 50%):
- Architecture: +5% (API design critical)
- Testing: +5% (integration tests complex)
- Implementation: -10% (offset increases)
```

**Uncertainty-Based Adjustments**:
```
If High Uncertainty (>5 unknowns in spec):
- Discovery: +10% (more research needed)
- Architecture: +5% (more design iterations)
- Implementation: -10% (offset)
- Testing: -5% (offset)
```

### Calculation Example

**Scenario**: Chat application, 32 hours total, complexity 0.68, uncertainty moderate

```
Base Distribution:
Discovery:     20% = 6.4 hours
Architecture:  15% = 4.8 hours
Implementation: 45% = 14.4 hours
Testing:       15% = 4.8 hours
Deployment:     5% = 1.6 hours

Adjustments (Complexity 0.68 = "Complex"):
Discovery:     +5% = +1.6 hours → 8.0 hours
Architecture:  +5% = +1.6 hours → 6.4 hours
Implementation: -10% = -3.2 hours → 11.2 hours
Testing:       No change → 4.8 hours
Deployment:    No change → 1.6 hours

Final Distribution:
Phase 1: 8.0 hours (25%)
Phase 2: 6.4 hours (20%)
Phase 3: 11.2 hours (35%)
Phase 4: 4.8 hours (15%)
Phase 5: 1.6 hours (5%)
Total: 32 hours
```

---

## Phase Transition Logic

### When to Move Between Phases

**Transition Requirements**:
```
Phase 1 → Phase 2:
✓ All validation gate criteria met
✓ User explicitly approves
✓ No blocking unknowns remain
✓ write_memory("phase_1_complete", ...) executed

Phase 2 → Phase 3:
✓ All validation gate criteria met
✓ User explicitly approves
✓ Architecture diagrams complete
✓ write_memory("phase_2_complete", ...) executed
✓ Wave execution plan created (if parallel)

Phase 3 → Phase 4:
✓ All validation gate criteria met
✓ User explicitly approves
✓ Integration successful
✓ All P0 features implemented
✓ write_memory("phase_3_complete", ...) executed

Phase 4 → Phase 5:
✓ All validation gate criteria met
✓ User explicitly approves
✓ All tests passing (100%)
✓ write_memory("phase_4_complete", ...) executed

Phase 5 → Complete:
✓ All validation gate criteria met
✓ User explicitly approves
✓ Staging deployment successful
✓ write_memory("phase_5_complete", ...) executed
✓ write_memory("project_complete", ...) executed
```

### Backward Transitions (Phase Rollback)

**When to Rollback**:
```
If validation gate fails:
1. User identifies issues during review
2. Critical requirements missed
3. Design flaws discovered
4. Implementation cannot proceed

Rollback Process:
1. Document issues in current phase memory
2. Mark validation_gate_status: "REJECTED"
3. Create todo list of required changes
4. Iterate on same phase
5. Re-submit for validation when ready
6. Do NOT proceed to next phase until approved
```

**Example Rollback**:
```
Scenario: User rejects Phase 2 (Architecture)

Action:
write_memory("phase_2_iteration", {
  timestamp: [ISO timestamp],
  validation_gate_status: "REJECTED",
  user_feedback: "Database schema missing indexes, API contracts lack error responses",
  required_changes: [
    "Add indexes to users and sessions tables",
    "Add 400/401/500 error responses to all API endpoints",
    "Revise testing strategy to include performance tests"
  ],
  next_action: "Address feedback, resubmit Phase 2 for approval"
})

Iterate on Phase 2 → Fix issues → Resubmit → Get approval → Proceed to Phase 3
```

---

## Parallel vs Sequential Decision Framework

### Parallelization Criteria

**When to Use Parallel Waves**:
```
1. Complexity >= 0.5
2. Multiple domains with >= 30% each
3. Domains are independent (no blocking dependencies)
4. Development time > 3 days

Example: Frontend 45%, Backend 36% → Parallel (Wave 3a and 3b)
```

**When to Use Sequential**:
```
1. Complexity < 0.5
2. Single dominant domain (>70%)
3. Strong dependencies between domains
4. Development time < 2 days

Example: Simple API-only project, Backend 85% → Sequential
```

### Dependency Analysis

**Independence Check**:
```
Frontend independent of Backend?
✓ Frontend can develop using mocked API responses
✓ Backend can develop using Postman for testing
→ PARALLEL CAPABLE

Frontend depends on Backend?
✗ Frontend requires real API endpoints immediately
→ SEQUENTIAL REQUIRED (Backend first, then Frontend)

Backend depends on Frontend?
✗ Backend needs frontend data structures
→ SEQUENTIAL REQUIRED (Frontend first, then Backend)
```

**Example Dependency Matrix**:
```
          | Frontend | Backend | Database | Mobile
----------|----------|---------|----------|--------
Frontend  |    -     |   ✗     |    ✗     |   ✗
Backend   |    ✗     |    -    |    ✓     |   ✗
Database  |    ✗     |    ✓    |    -     |   ✗
Mobile    |    ✗     |   ✗     |    ✗     |   -

✓ = Depends on (must wait for)
✗ = Independent (can work in parallel)

Analysis:
- Backend depends on Database → Database must complete first
- Frontend and Mobile independent of each other → Can parallelize
- Backend and Frontend independent → Can parallelize

Wave Structure:
  Wave 3a: Database setup (sequential first)
  Wave 3b: Backend (after 3a)
  Wave 3c: Frontend (parallel with 3b)
  Wave 3d: Mobile (parallel with 3b and 3c)
  Wave 3e: Integration (sequential after all)
```

---

## Phase Documentation Requirements

### Memory Storage Schema

**Phase 1 Complete**:
```typescript
write_memory("phase_1_complete", {
  phase_number: 1,
  phase_name: "Discovery",
  timestamp: string,           // ISO 8601
  duration_actual: string,     // "6.4 hours"
  duration_planned: string,    // "6.4 hours"
  variance: string,            // "+0.0 hours (0%)"
  deliverables: string[],      // ["requirements.md", "user_stories.md", ...]
  validation_gate_status: "APPROVED" | "REJECTED",
  gate_criteria_met: boolean[], // [true, true, true, ...]
  user_feedback: string,
  issues_identified: string[],
  next_phase: "Phase 2: Architecture"
})
```

**Phase 2 Complete**:
```typescript
write_memory("phase_2_complete", {
  phase_number: 2,
  phase_name: "Architecture",
  timestamp: string,
  duration_actual: string,
  duration_planned: string,
  variance: string,
  deliverables: string[],
  validation_gate_status: "APPROVED" | "REJECTED",
  design_decisions: string[],       // ["JWT over sessions", ...]
  architectural_patterns: string[], // ["MVC", "REST", ...]
  parallelization_plan: string,     // "Frontend and Backend parallel"
  next_phase: "Phase 3: Implementation"
})
```

**Phase 3 Complete**:
```typescript
write_memory("phase_3_complete", {
  phase_number: 3,
  phase_name: "Implementation",
  timestamp: string,
  duration_actual: string,
  duration_planned: string,
  variance: string,
  waves_executed: string[],         // ["wave_3a_frontend", "wave_3b_backend", ...]
  parallelization_gain: string,     // "40% time saved vs sequential"
  deliverables: string[],
  validation_gate_status: "APPROVED" | "REJECTED",
  features_completed: number,
  known_issues: string[],
  code_quality_metrics: {
    linting_passed: boolean,
    type_errors: number,
    todos_remaining: number
  },
  next_phase: "Phase 4: Testing"
})
```

**Phase 4 Complete**:
```typescript
write_memory("phase_4_complete", {
  phase_number: 4,
  phase_name: "Testing",
  timestamp: string,
  duration_actual: string,
  duration_planned: string,
  variance: string,
  deliverables: string[],
  validation_gate_status: "APPROVED" | "REJECTED",
  test_stats: {
    total_tests: number,
    passing: number,
    failing: number,
    coverage_percentage: string
  },
  no_mocks_verified: boolean,       // MUST be true
  user_stories_validated: number,
  next_phase: "Phase 5: Deployment"
})
```

**Phase 5 Complete**:
```typescript
write_memory("phase_5_complete", {
  phase_number: 5,
  phase_name: "Deployment",
  timestamp: string,
  duration_actual: string,
  duration_planned: string,
  variance: string,
  deliverables: string[],
  validation_gate_status: "APPROVED" | "REJECTED",
  staging_url: string,
  production_ready: boolean,
  deployment_issues: string[],
  next_steps: string                // "Production deployment"
})
```

### Project Completion Record

```typescript
write_memory("project_complete", {
  project_name: string,
  spec_file: string,
  start_timestamp: string,
  end_timestamp: string,
  total_duration_actual: string,
  total_duration_planned: string,
  variance: string,
  phases_completed: 5,
  all_validation_gates_passed: boolean,
  final_deliverables: string[],
  total_features_implemented: number,
  test_coverage: string,
  deployment_status: "staging" | "production",
  lessons_learned: string[],
  success_metrics: {
    on_time: boolean,
    on_scope: boolean,
    quality_maintained: boolean,
    no_mocks_philosophy_followed: boolean
  }
})
```

---

## Summary: 5-Phase Planning Principles

### Core Tenets
1. **Structured Progression**: Every project follows the same 5 phases
2. **Validation Gates**: No phase skipping without explicit approval
3. **Effort Distribution**: Standard percentages with complexity adjustments
4. **Parallel Execution**: Wave-based parallelization in Phase 3 when feasible
5. **Complete Documentation**: Every phase fully documented in Serena memory

### Success Criteria
- ✅ All phases complete with validation gates passed
- ✅ User explicitly approves each phase transition
- ✅ Effort distribution matches planning (variance < 20%)
- ✅ All deliverables produced as specified
- ✅ No phase skipped or rushed

### Anti-Patterns to Avoid
- ❌ Skipping validation gates
- ❌ Proceeding without user approval
- ❌ Merging phases together
- ❌ Starting implementation before architecture approved
- ❌ Testing without complete implementation
- ❌ Deploying without passing tests

---

**END OF PHASE_PLANNING.MD**