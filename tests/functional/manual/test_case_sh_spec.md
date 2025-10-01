# Test Case: /sh:spec Command Validation

**Test ID**: TC-001
**Priority**: Critical
**Category**: Behavioral/Analysis
**Estimated Time**: 10 minutes

## Objective

Validate that /sh:spec command produces 8-dimensional complexity analysis with correct Shannon behavioral patterns, artifact generation, and MCP recommendations.

## Prerequisites

- [ ] Shannon project loaded in Claude Code
- [ ] Serena MCP configured and functional
- [ ] .shannon/ directory cleared (fresh start)
- [ ] Test environment: /Users/nick/Documents/shannon

## Test Steps

### Step 1: Environment Setup

```bash
# Clear previous test artifacts
cd /Users/nick/Documents/shannon
rm -rf .shannon/analysis/spec_*.md
mkdir -p .shannon/analysis
mkdir -p test-results/TC-001/{artifacts,screenshots,logs}
```

**Expected**: Directories created without errors

### Step 2: Execute /sh:spec Command

**Command**:
```
/sh:spec "Build a todo application with user authentication, task management, and real-time notifications"
```

**Expected Behavior**:
- SPEC_ANALYZER agent should activate
- 8-dimensional complexity analysis initiates
- Sequential MCP may be used for complex reasoning
- Output appears in structured Shannon format
- NO generic Claude Code responses

### Step 3: Validate Output Structure

**Output Format Checklist**:
- [ ] Title: "# Specification Analysis: [description]"
- [ ] Section 1: "## 8-Dimensional Complexity Analysis"
- [ ] Overall complexity score displayed (0.0-1.0)
- [ ] Complexity classification (Simple/Moderate/Moderate-High/Complex/Very Complex)
- [ ] All 8 dimensions listed with individual scores
- [ ] Each dimension shows weight percentage
- [ ] Section 2: "## Domain Analysis"
- [ ] Domain breakdown with percentages
- [ ] Percentages sum to 100%
- [ ] Section 3: "## MCP Server Recommendations"
- [ ] Tier 1-4 structure present
- [ ] Serena MCP in Tier 1 (always)
- [ ] Context-appropriate MCP servers recommended
- [ ] Section 4: "## 5-Phase Implementation Plan"
- [ ] Phase 1: Discovery & Analysis
- [ ] Phase 2: Design & Architecture
- [ ] Phase 3: Implementation
- [ ] Phase 4: Integration & Testing
- [ ] Phase 5: Deployment & Monitoring
- [ ] Each phase has validation gates
- [ ] Section 5: "## Timeline Estimation"
- [ ] Total duration estimate
- [ ] Phase-by-phase breakdown
- [ ] Section 6: "## Risk Assessment"
- [ ] Risk categories identified
- [ ] Mitigation strategies provided
- [ ] Section 7: "## Wave Orchestration Strategy"
- [ ] Wave count recommendation
- [ ] Wave boundaries defined
- [ ] Rationale provided

### Step 4: Validate Complexity Analysis Details

**8-Dimension Validation Checklist**:

1. **Structural Complexity (20%)**:
   - [ ] Score present (0.0-1.0)
   - [ ] Factors: components, modules, dependencies
   - [ ] Justification provided

2. **Cognitive Complexity (15%)**:
   - [ ] Score present
   - [ ] Factors: business logic, edge cases, state management
   - [ ] Justification provided

3. **Integration Complexity (15%)**:
   - [ ] Score present
   - [ ] Factors: external APIs, services, data sources
   - [ ] Justification provided

4. **Data Complexity (10%)**:
   - [ ] Score present
   - [ ] Factors: data models, relationships, transformations
   - [ ] Justification provided

5. **Concurrency Complexity (10%)**:
   - [ ] Score present
   - [ ] Factors: real-time features, async operations
   - [ ] Justification provided

6. **Testing Complexity (10%)**:
   - [ ] Score present
   - [ ] Factors: test coverage, test types required
   - [ ] Justification provided

7. **Security Complexity (10%)**:
   - [ ] Score present
   - [ ] Factors: authentication, authorization, data protection
   - [ ] Justification provided

8. **Deployment Complexity (10%)**:
   - [ ] Score present
   - [ ] Factors: infrastructure, CI/CD, monitoring
   - [ ] Justification provided

### Step 5: Validate Domain Analysis

**Domain Analysis Checklist**:
- [ ] Frontend percentage (if UI present)
- [ ] Backend percentage (if server-side logic present)
- [ ] Database percentage (if data persistence present)
- [ ] DevOps percentage (if deployment mentioned)
- [ ] Security percentage (if auth/security present)
- [ ] All percentages are integers
- [ ] Total equals 100%
- [ ] Dominant domain correctly identified

### Step 6: Validate MCP Recommendations

**MCP Tier Validation**:

**Tier 1 - Essential** (Always Present):
- [ ] Serena MCP listed
- [ ] Rationale: "Project memory, semantic search, symbol operations"

**Tier 2 - Highly Recommended** (Context-Dependent):
- [ ] If frontend >20%: shadcn MCP present
- [ ] If complexity >0.7: Sequential MCP present
- [ ] If API integration: Context7 MCP present
- [ ] Appropriate rationale for each

**Tier 3 - Beneficial** (Nice-to-Have):
- [ ] Complementary MCP servers suggested
- [ ] Clear use cases provided

**Tier 4 - Optional** (Enhancement):
- [ ] Optional MCP servers listed
- [ ] Rationale explains optional nature

### Step 7: Validate Implementation Plan

**5-Phase Plan Validation**:

**Phase 1 - Discovery & Analysis**:
- [ ] Scope definition task
- [ ] Requirements gathering task
- [ ] Architecture planning task
- [ ] Validation gate defined

**Phase 2 - Design & Architecture**:
- [ ] Design tasks specified
- [ ] Architecture decisions documented
- [ ] Validation gate defined

**Phase 3 - Implementation**:
- [ ] Core feature implementation tasks
- [ ] Component/module tasks
- [ ] Validation gate defined

**Phase 4 - Integration & Testing**:
- [ ] Integration tasks
- [ ] Testing tasks (unit, integration, E2E)
- [ ] Validation gate defined

**Phase 5 - Deployment & Monitoring**:
- [ ] Deployment tasks
- [ ] Monitoring setup
- [ ] Validation gate defined

### Step 8: Validate Artifact Generation

**Artifact Checklist**:
- [ ] .shannon/analysis/ directory exists
- [ ] spec_YYYYMMDD_HHMMSS.md file created
- [ ] File timestamp matches execution time (±1 minute)
- [ ] File size >5KB (substantial content)
- [ ] File readable and well-formatted
- [ ] YAML frontmatter present (optional but preferred)

**Artifact Content Validation**:
```bash
# Check artifact exists and has content
ls -lh .shannon/analysis/spec_*.md
wc -l .shannon/analysis/spec_*.md
```
- [ ] File size >5KB
- [ ] Line count >200

### Step 9: Validate Behavioral Patterns

**Shannon-Specific Behaviors**:
- [ ] NO generic "I'll help you build..." responses
- [ ] SPEC_ANALYZER agent explicitly mentioned or implied
- [ ] Complexity score calculation shown
- [ ] Domain analysis performed (not just description)
- [ ] MCP recommendations context-aware (not generic list)
- [ ] Wave count justified by complexity (not arbitrary)
- [ ] Implementation plan tailored to specification
- [ ] Risk assessment addresses actual project risks
- [ ] Timeline estimation reasonable for complexity

**Anti-Patterns (Should NOT Appear)**:
- [ ] Generic feature descriptions without analysis
- [ ] Missing complexity scores
- [ ] All MCP servers recommended regardless of need
- [ ] Copy-paste 5-phase plan without customization
- [ ] Arbitrary wave count without justification

## Expected Results

**Output Structure Example**:
```markdown
# Specification Analysis: Build todo app with authentication

## 8-Dimensional Complexity Analysis

**Overall Complexity Score**: 0.68 (Moderate-High)

### Dimension Scores:
1. Structural Complexity (20%): 0.65
   - Multiple frontend components (TodoList, TodoItem, AuthForm)
   - Backend API with authentication layer
   - Database schema with relationships

2. Cognitive Complexity (15%): 0.75
   - User authentication flows (signup, login, logout)
   - Authorization logic (user-specific todos)
   - Real-time notification system
   - Task state management (create, update, delete, complete)

3. Integration Complexity (15%): 0.70
   - WebSocket for real-time notifications
   - REST API for CRUD operations
   - Possible third-party auth providers

4. Data Complexity (10%): 0.60
   - User model (id, email, password_hash)
   - Todo model (id, user_id, title, description, completed)
   - Notification model (id, user_id, message, read)

5. Concurrency Complexity (10%): 0.80
   - Real-time WebSocket connections
   - Concurrent user sessions
   - Race conditions in todo updates

6. Testing Complexity (10%): 0.65
   - Unit tests for business logic
   - Integration tests for API endpoints
   - E2E tests for authentication flows

7. Security Complexity (10%): 0.75
   - Password hashing and storage
   - JWT token management
   - Session handling
   - CSRF protection
   - Input validation

8. Deployment Complexity (10%): 0.55
   - Standard web app deployment
   - Database migration management
   - Environment configuration

## Domain Analysis

**Domain Breakdown**:
- Frontend: 30%
- Backend: 35%
- Database: 15%
- DevOps: 10%
- Security: 10%

**Dominant Domain**: Backend (35%)

## MCP Server Recommendations

### Tier 1 - Essential
- **Serena**: Project memory, semantic code search, symbol operations

### Tier 2 - Highly Recommended
- **shadcn**: Frontend is 30% - use shadcn for React UI components
- **Sequential**: Complexity 0.68 requires structured reasoning
- **Context7**: Authentication patterns and best practices

### Tier 3 - Beneficial
- **Playwright**: E2E testing for authentication flows

### Tier 4 - Optional
- None for this specification

## 5-Phase Implementation Plan

### Phase 1: Discovery & Analysis
**Tasks**:
1. Define todo data model and relationships
2. Document authentication requirements (JWT vs session)
3. Identify notification delivery mechanisms
**Validation Gate**: Requirements documented, architecture approved

[... continues for all 5 phases ...]

## Timeline Estimation

**Total Duration**: 3-4 weeks

**Phase Breakdown**:
- Phase 1: 3-4 days
- Phase 2: 4-5 days
- Phase 3: 8-10 days
- Phase 4: 4-5 days
- Phase 5: 2-3 days

## Risk Assessment

**High Priority Risks**:
1. **Authentication Security**: Mitigation - use established libraries, security audit
2. **Real-time Performance**: Mitigation - load testing, connection pooling
3. **Data Integrity**: Mitigation - transaction handling, validation

## Wave Orchestration Strategy

**Recommended Wave Count**: 4 waves

**Wave Boundaries**:
1. Wave 1: Authentication system
2. Wave 2: Todo CRUD operations
3. Wave 3: Real-time notifications
4. Wave 4: Integration and polish

**Rationale**: Complexity 0.68 justifies 4 waves for systematic development
```

**Artifact Created**: .shannon/analysis/spec_20250930_143022.md

## Validation Criteria

**Pass Criteria**:
- ✅ All critical checkboxes checked (Sections 3-9)
- ✅ Artifact created with correct naming
- ✅ Output contains all 7 required sections
- ✅ Complexity scores present for all 8 dimensions
- ✅ Domain percentages sum to 100%
- ✅ Serena MCP in Tier 1
- ✅ Wave count justified by complexity

**Fail Criteria**:
- ❌ Any critical section missing from output
- ❌ Complexity scores missing or invalid
- ❌ Domain analysis incorrect or missing
- ❌ Artifact not created
- ❌ Generic Claude responses instead of Shannon patterns

## Debug Information

**Logs to Collect**:
- [ ] Copy full command output to: test-results/TC-001/output.md
- [ ] Copy artifact to: test-results/TC-001/artifacts/
- [ ] Screenshot of execution: test-results/TC-001/screenshots/
- [ ] Claude Code console logs: test-results/TC-001/logs/

**Debug Commands**:
```bash
# Verify artifact
cat .shannon/analysis/spec_*.md | head -50

# Check file size
ls -lh .shannon/analysis/spec_*.md

# Count sections
grep -c "^## " .shannon/analysis/spec_*.md

# Verify Serena MCP mentioned
grep -i "serena" .shannon/analysis/spec_*.md
```

## Notes

**Record Observations**:
- Execution time: _____ seconds
- Artifact file size: _____ KB
- Wave count recommended: _____
- Complexity score: _____
- Any errors or warnings: _____
- Unexpected behavior: _____
- Shannon behavioral patterns observed: _____

**Known Issues**:
- None at test creation time

**Variations to Test**:
1. Simple spec (complexity <0.4)
2. Complex spec (complexity >0.8)
3. Frontend-heavy spec (>60% frontend)
4. Backend-heavy spec (>60% backend)
5. Security-focused spec (auth, encryption, compliance)
