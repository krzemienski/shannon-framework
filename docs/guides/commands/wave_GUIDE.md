# /shannon:wave Command - Complete Usage Guide

**Command**: `/shannon:wave`
**Purpose**: Orchestrate parallel multi-agent execution using wave-based coordination
**Skill**: Invokes wave-orchestration skill (1581 lines)
**Agent**: Activates WAVE_COORDINATOR for parallel execution
**Output**: Wave execution plan, parallel speedup metrics, synthesis checkpoints

---

## Overview

The `/shannon:wave` command implements Shannon's **signature parallel execution system** achieving 3.5x average speedup through true multi-agent parallelism. It analyzes dependencies, groups independent work into waves, spawns agents in parallel, and manages synthesis checkpoints.

**Core Value**: Transforms 16-hour sequential work into 5-hour parallel execution.

**When to Use**:
- Complexity >=0.50 (Complex or higher) - MANDATORY
- Multiple independent components (frontend + backend + database)
- Clear dependency boundaries
- 3+ agents needed

**Usage**:
```bash
/shannon:wave                           # Execute waves (uses existing plan or creates new)
/shannon:wave [request]                 # Execute specific wave request
/shannon:wave --plan                    # Generate plan only (don't execute)
/shannon:wave --dry-run                 # Detailed planning with risk analysis
```

---

## The 15 Usage Examples

### Example 1: Basic Wave Execution (Post /shannon:wave)

**Context**: Already ran `/shannon:wave`, complexity = 0.58

**Input**:
```bash
/shannon:wave
```

**Process**:
```
1. Load spec_analysis from Serena (complexity: 0.58)
2. Load phase_plan from Serena
3. wave-orchestration generates wave structure:

   Wave 1: Foundation (1 agent, 2h)
     - Architecture design

   Wave 2: Implementation (3 agents PARALLEL, 4h)
     - Frontend builder
     - Backend builder
     - Database builder

   Wave 3: Integration (1 agent, 2h)
     - Integration testing

4. WAVE_COORDINATOR executes:
   - Spawns Wave 1 (1 agent) → waits
   - Synthesizes Wave 1 → user approves
   - Spawns Wave 2 (3 agents IN ONE MESSAGE) → true parallel
   - Synthesizes Wave 2 → user approves
   - Spawns Wave 3 (1 agent) → waits
   - Final synthesis

Total: 8h parallel vs 14h sequential = 1.75x speedup
```

**Output**:
```
🌊 Wave Execution Complete

**Strategy**: Parallel with Integration
**Total Waves**: 3
**Agents Deployed**: 5
**Execution Time**: 8 hours
**Speedup**: 1.75x vs sequential (saved 6 hours)

**Waves Executed**:
├─ Wave 1: Foundation (2h)
│  └─ Deliverables: Architecture diagram, API contracts, DB schema
├─ Wave 2: Implementation (4h - PARALLEL)
│  ├─ Frontend: React components, state management
│  ├─ Backend: Express API, authentication
│  └─ Database: PostgreSQL schema, migrations
└─ Wave 3: Integration (2h)
   └─ Deliverables: 12 Puppeteer tests (NO MOCKS), integration validated

**Goal Alignment**: 0.85 / 1.0 ✅

**Checkpoints Created**:
✓ Pre-wave: shannon_prewave_20251108_210500
✓ Wave 1: wave_1_complete
✓ Wave 2: wave_2_complete
✓ Wave 3: wave_3_complete
```

**Key Learning**: No request text needed if spec_analysis exists - uses existing context.

---

### Example 2: Wave Planning Mode (--plan)

**Input**:
```bash
/shannon:wave Build multi-tenant SaaS platform --plan
```

**Output**:
```
📋 Wave Execution Plan Generated

**Complexity**: 0.72 (from spec or calculated)
**Execution Strategy**: Wave-Based Parallel
**Total Waves**: 4
**Total Agents**: 9
**Estimated Time**: 12h parallel (vs 28h sequential = 2.3x speedup)

## Wave Structure

### Wave 1: Architecture & Design
**Dependencies**: None
**Agents**: 2
**Execution**: Sequential (planning phase)
**Duration**: 3h
**Tasks**:
- Multi-tenant architecture design (database isolation, row-level security)
- API contract definition
**Agent Types**: ARCHITECT, DATABASE_ARCHITECT

### Wave 2: Foundation Implementation
**Dependencies**: Wave 1 complete
**Agents**: 3
**Execution**: PARALLEL
**Duration**: 5h
**Tasks**:
- Database schema with multi-tenancy (PostgreSQL)
- Authentication service (JWT with tenant context)
- Frontend scaffolding (React with tenant selector)
**Agent Types**: DATABASE_ARCHITECT, BACKEND, FRONTEND

### Wave 3: Feature Implementation
**Dependencies**: Wave 2 complete
**Agents**: 3
**Execution**: PARALLEL
**Duration**: 4h
**Tasks**:
- Tenant management UI
- User management with roles
- Billing integration (Stripe with tenant isolation)
**Agent Types**: FRONTEND, BACKEND, IMPLEMENTATION_WORKER

### Wave 4: Testing & Validation
**Dependencies**: Wave 3 complete
**Agents**: 1
**Execution**: Sequential
**Duration**: 2h
**Tasks**:
- Multi-tenant isolation tests (ensure no data leakage)
- Puppeteer E2E tests (real browser, NO MOCKS)
- Performance testing (tenant query optimization)
**Agent Types**: TEST_GUARDIAN

## Parallelization Analysis

**Sequential Execution** (if done one by one):
Wave 1: 3h
Wave 2: 5h + 5h + 5h = 15h (3 agents sequential)
Wave 3: 4h + 4h + 4h = 12h (3 agents sequential)
Wave 4: 2h
Total: 32h

**Parallel Execution** (as planned):
Wave 1: 3h
Wave 2: max(5h, 5h, 5h) = 5h (3 agents parallel)
Wave 3: max(4h, 4h, 4h) = 4h (3 agents parallel)
Wave 4: 2h
Total: 14h

**Speedup**: 32h → 14h = 2.3x faster
**Time Saved**: 18 hours

## Next Actions

**To Execute This Plan**:
```bash
/shannon:wave   # Run without --plan flag
```

**To Modify Plan**:
- Adjust agent allocation (if resource constraints)
- Change wave grouping (if different dependencies)
- Update and re-run /shannon:wave --plan

**Plan Saved**:
✓ Serena MCP: wave_execution_plan_20251108
✓ Retrieve: read_memory("wave_execution_plan_20251108")
```

**Key Learning**: --plan shows structure without executing, enables review before commitment.

---

### Example 3: Dry Run with Risk Analysis (--dry-run)

**Input**:
```bash
/shannon:wave Build real-time collaboration platform --dry-run
```

**Output**:
```
🔍 Wave Execution Dry Run - Comprehensive Analysis

[Wave structure as in Example 2...]

## Risk Analysis

### Wave 1 Risks
⚠️ **Architecture Risk**: CRDT selection critical
- Impact: Wrong choice = Wave 2-3 rework (8h wasted)
- Mitigation: Use Sequential MCP for 100-step analysis
- Decision Gate: Architecture review before Wave 2

### Wave 2 Risks
⚠️ **Integration Risk**: WebSocket + CRDT integration complex
- Impact: May block Wave 3 if not working
- Mitigation: Dedicated integration testing in Wave 2
- Fallback: Extend Wave 2 by 2h if issues found

### Wave 3 Risks
⚠️ **Performance Risk**: Real-time sync may not meet <100ms target
- Impact: May require Wave 3b for optimization
- Mitigation: Performance testing early in Wave 3
- Contingency: Add optimization wave if needed

## Token Usage Estimates

Wave 1: 15K tokens (architecture discussion)
Wave 2: 45K tokens (3 agents × 15K each)
Wave 3: 30K tokens (2 agents × 15K each)
Wave 4: 12K tokens (testing synthesis)
Synthesis Overhead: 20K tokens (checkpoints, validation)
**Total**: ~122K tokens

**Budget Check**:
Available: 200K tokens
Required: 122K tokens
Remaining: 78K tokens (safe - 39% buffer)

## Checkpoint Strategy

**Recommended Checkpoints** (beyond mandatory wave synthesis):
1. After Wave 1 (architecture locked in)
2. After Wave 2 (foundation complete - major milestone)
3. Before Wave 4 (testing phase - validate implementation first)

**Rationale**: High-risk waves (1, 2) need extra checkpoints for rollback capability.

## Execution Timeline

**If starting now** (2025-11-08 21:30):
- Wave 1: 21:30 - 00:30 (3h)
- Synthesis 1: 00:30 - 00:45 (15min)
- Wave 2: 00:45 - 05:45 (5h PARALLEL)
- Synthesis 2: 05:45 - 06:00 (15min)
- Wave 3: 06:00 - 10:00 (4h PARALLEL)
- Synthesis 3: 10:00 - 10:15 (15min)
- Wave 4: 10:15 - 12:15 (2h)
- Final Synthesis: 12:15 - 12:30 (15min)

**Completion**: 2025-11-09 12:30 (15 hours total)

## Proceed with Execution?

**Dry run complete - no execution performed.**

To execute:
```bash
/shannon:wave  # Run without --dry-run flag
```

To revise plan:
- Modify wave structure
- Adjust risk mitigations
- Re-run --dry-run
```

**Key Learning**: --dry-run provides comprehensive pre-execution analysis (risks, tokens, timeline, checkpoints).

---

### Example 4: 2-Wave Simple Parallel

**Input**:
```bash
/shannon:wave Implement user dashboard and admin panel
```

**Context**: Complexity 0.52 (Complex), two independent components

**Execution**:
```
Wave Structure Generated:

Wave 1: Parallel Implementation (6h)
  - 2 agents in ONE message:
    * FRONTEND agent: User dashboard (React components, routing, state)
    * FRONTEND agent: Admin panel (admin UI, user management, analytics)

No Wave 2 needed - no dependencies

WAVE_COORDINATOR spawns both agents:
<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">frontend-developer</parameter>
    <parameter name="description">User dashboard implementation</parameter>
    <parameter name="prompt">
      ## CONTEXT LOADING
      1. read_memory("spec_analysis")
      2. read_memory("phase_plan")

      ## YOUR TASK
      Implement user dashboard with [...details...]
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">frontend-developer</parameter>
    <parameter name="description">Admin panel implementation</parameter>
    <parameter name="prompt">
      ## CONTEXT LOADING
      1. read_memory("spec_analysis")
      2. read_memory("phase_plan")

      ## YOUR TASK
      Implement admin panel with [...details...]
    </parameter>
  </invoke>
</function_calls>

Both agents execute SIMULTANEOUSLY.
Result: 6h parallel vs 12h sequential = 2x speedup
```

**Output**:
```
🌊 Wave 1 Complete

**Agents**: 2 (parallel execution)
**Duration**: 6h
**Speedup**: 2.0x

**Deliverables**:
├─ User Dashboard (FRONTEND agent #1)
│  ├─ Components: Profile, Settings, Dashboard, Activity
│  ├─ Files: 12 components, 3 pages
│  └─ Tests: 8 Puppeteer tests
└─ Admin Panel (FRONTEND agent #2)
   ├─ Components: UserManagement, Analytics, SystemSettings
   ├─ Files: 10 components, 2 pages
   └─ Tests: 6 Puppeteer tests

**Synthesis**:
✅ Zero duplicate work
✅ No integration conflicts
✅ All tests passing (NO MOCKS)
✅ Goal alignment: 0.92

**Checkpoint**: wave_1_complete_dashboard
```

**Key Learning**: Independent components execute in true parallel (2 agents in one message = 2x speedup).

---

### Example 5: 5-Wave Complex Project

**Input**:
```bash
/shannon:wave Build complete e-commerce platform
```

**Context**: Complexity 0.76 (HIGH), multiple domains, complex dependencies

**Wave Structure**:
```
Wave 1: Architecture (1 agent, 3h)
  ├─ System design
  ├─ Database schema design
  ├─ API contracts
  └─ Dependencies: None

Wave 2: Foundation (4 agents PARALLEL, 5h)
  ├─ Database setup (PostgreSQL + migrations)
  ├─ Backend API scaffold (Express + auth)
  ├─ Frontend scaffold (Next.js + routing)
  └─ Payment gateway setup (Stripe integration)
  └─ Dependencies: Wave 1

Wave 3: Core Features (5 agents PARALLEL, 6h)
  ├─ Product catalog (frontend)
  ├─ Shopping cart (frontend + backend)
  ├─ User accounts (backend + database)
  ├─ Order processing (backend + database)
  └─ Admin dashboard (frontend)
  └─ Dependencies: Wave 2

Wave 4: Advanced Features (3 agents PARALLEL, 4h)
  ├─ Search (Elasticsearch integration)
  ├─ Reviews & ratings
  └─ Email notifications (SendGrid)
  └─ Dependencies: Wave 3

Wave 5: Testing & Deployment (2 agents, 3h)
  ├─ Puppeteer E2E tests (complete user journeys)
  └─ Deployment (Docker + Kubernetes)
  └─ Dependencies: Wave 4

Total: 21h parallel vs 65h sequential = 3.1x speedup
```

**Execution**:
```
WAVE_COORDINATOR orchestrates all 5 waves:

For each wave:
  1. Load all previous wave results from Serena
  2. Spawn agents (parallel if >1 agent, ONE message)
  3. Wait for all agents to complete
  4. Synthesize results
  5. Validate (no conflicts, no missing work, tests pass)
  6. Save wave_N_complete to Serena
  7. Present to user for approval
  8. Get explicit approval before next wave

Iron Law: Cannot skip synthesis checkpoints
```

**Key Learning**: Large projects (complexity 0.70-0.85) need 5-7 waves, 8-15 agents, achieve 3-4x speedup.

---

### Example 6: Dependency Chain (Sequential Waves)

**Input**:
```bash
/shannon:wave Implement authentication system
```

**Context**: Auth has strict dependencies (each step depends on previous)

**Wave Structure**:
```
Wave 1: Database Schema (1 agent, 2h)
  - Users table
  - Sessions table
  - Refresh tokens table
  Dependencies: None

Wave 2: Backend Auth Service (1 agent, 4h)
  - JWT generation
  - Password hashing
  - Session management
  Dependencies: Wave 1 (needs user schema)

Wave 3: Auth Endpoints (1 agent, 3h)
  - /register endpoint
  - /login endpoint
  - /logout endpoint
  - /refresh-token endpoint
  Dependencies: Wave 2 (needs auth service)

Wave 4: Frontend Auth UI (1 agent, 3h)
  - Login form
  - Registration form
  - Protected routes
  Dependencies: Wave 3 (needs endpoints)

Wave 5: Testing (1 agent, 2h)
  - Puppeteer login flow test
  - Token refresh test
  - Protected route access test
  Dependencies: Wave 4 (needs complete system)

Total: 14h (NO speedup vs sequential due to dependencies)
```

**Output**:
```
🌊 Wave Execution Complete

**Strategy**: Sequential (dependency chain)
**Total Waves**: 5
**Agents Deployed**: 5
**Execution Time**: 14h
**Speedup**: 1.0x (no parallelism possible)
**Reason**: Each wave depends on previous (strict dependency chain)

**Observation**: Not all projects benefit from waves.
Shannon detected dependencies and created optimal structure.
```

**Key Learning**: Wave orchestration doesn't FORCE parallelism - it finds optimal structure. Some projects are inherently sequential.

---

### Example 7: Partial Parallelism (Mixed Dependencies)

**Input**:
```bash
/shannon:wave Build blog platform with CMS
```

**Wave Structure**:
```
Wave 1: Foundation (1 agent, 2h)
  - Database schema (posts, users, comments, categories)

Wave 2: Backend + Frontend Start (2 agents PARALLEL, 4h)
  - Backend API (Express endpoints for posts/users) [depends: Wave 1]
  - Frontend structure (Next.js routing, layouts) [depends: Wave 1]

Wave 3: Features (3 agents PARALLEL, 5h)
  - Rich text editor (frontend) [depends: Wave 2 frontend]
  - Comment system (backend + frontend) [depends: Wave 2 both]
  - Admin CMS (frontend + backend) [depends: Wave 2 both]

Wave 4: Testing (1 agent, 2h)
  - Puppeteer full user journey tests

Total: 13h parallel vs 21h sequential = 1.6x speedup
```

**Parallelization Pattern**:
```
Sequential Execution:
Wave 1: 2h
Wave 2: 4h + 4h = 8h (no parallelism)
Wave 3: 5h + 5h + 5h = 15h (no parallelism)
Wave 4: 2h
Total: 27h

Parallel Execution:
Wave 1: 2h
Wave 2: max(4h, 4h) = 4h (2 parallel)
Wave 3: max(5h, 5h, 5h) = 5h (3 parallel)
Wave 4: 2h
Total: 13h

Savings: 27h - 13h = 14 hours (52% time reduction)
```

**Key Learning**: Partial parallelism still provides significant speedup (1.6-2.0x common).

---

### Example 8: Maximum Parallelism (Independent Microservices)

**Input**:
```bash
/shannon:wave Build microservices for user service, product service, order service, notification service
```

**Context**: 4 independent microservices (maximum parallelism opportunity)

**Wave Structure**:
```
Wave 1: Shared Architecture (1 agent, 2h)
  - API gateway design
  - Service mesh setup
  - Shared database conventions

Wave 2: Microservices Implementation (4 agents PARALLEL, 6h)
  - User service (auth, profiles) [BACKEND agent]
  - Product service (catalog, inventory) [BACKEND agent]
  - Order service (cart, checkout) [BACKEND agent]
  - Notification service (email, SMS) [BACKEND agent]

Wave 3: Integration (1 agent, 3h)
  - API gateway configuration
  - Service-to-service communication
  - Integration tests

Total: 11h parallel vs 26h sequential = 2.4x speedup
```

**Agent Spawning** (Wave 2 - TRUE PARALLELISM):
```
<function_calls>
  <invoke name="Task">Backend - User Service</invoke>
  <invoke name="Task">Backend - Product Service</invoke>
  <invoke name="Task">Backend - Order Service</invoke>
  <invoke name="Task">Backend - Notification Service</invoke>
</function_calls>

All 4 agents execute SIMULTANEOUSLY
Duration: max(6h, 6h, 6h, 6h) = 6h
NOT: 6+6+6+6 = 24h
```

**Key Learning**: Independent components = maximum parallelism = highest speedup potential.

---

### Example 9: Token-Constrained Wave (Split Large Wave)

**Input**:
```bash
/shannon:wave Implement 12 dashboard widgets
```

**Context**: 12 independent widgets, but token budget limits agents/wave

**Wave Structure** (with token constraints):
```
Token Budget Analysis:
- Available: 150K tokens
- Safety buffer: 20K
- Usable: 130K
- Per agent: ~3K average
- Max agents: 130K / 3K = 43 agents (token-wise)
- Synthesis limit: 10 agents/wave (manageable synthesis)

Result: Split into waves

Wave 3a: Widgets 1-5 (5 agents PARALLEL, 4h)
Wave 3b: Widgets 6-10 (5 agents PARALLEL, 4h)
Wave 3c: Widgets 11-12 (2 agents PARALLEL, 4h)

Total: 12h vs 48h sequential = 4x speedup
```

**Key Learning**: Token budget limits wave size. wave-orchestration automatically splits large parallel work.

---

### Example 10: Mid-Wave Failure Recovery

**Input**:
```bash
/shannon:wave Continue Wave 2
```

**Context**: Wave 2 had partial failure (2 agents succeeded, 1 failed)

**Recovery Process**:
```
1. WAVE_COORDINATOR detects Wave 2 incomplete:
   - Read wave_2_results from Serena
   - Status: 2/3 agents succeeded, 1 failed

2. Analyze failure:
   - Failed agent: DATABASE_ARCHITECT
   - Reason: PostgreSQL connection error
   - Impact: Blocks frontend/backend agents (need schema)

3. Respawn failed agent with fixes:
   - Load previous context
   - Apply fix (correct connection string)
   - Re-execute

4. Synthesize complete Wave 2:
   - All 3 agents now complete
   - Save wave_2_complete
   - Proceed to Wave 3
```

**Output**:
```
🔧 Wave 2 Recovery Complete

**Original Status**: 2/3 agents succeeded
**Failed Agent**: DATABASE_ARCHITECT (PostgreSQL connection error)
**Recovery Action**: Respawned with corrected connection string
**New Status**: 3/3 agents succeeded ✅

**Wave 2 Complete**:
All deliverables now present, proceeding to Wave 3
```

**Key Learning**: wave-orchestration includes error recovery - partial failures don't require full wave restart.

---

### Example 11: Dynamic Wave Adjustment

**Input**:
```bash
/shannon:wave Build payment processing system
```

**Initial Plan**: 3 waves
**Execution**: Discovers complexity during Wave 1, adjusts

**Process**:
```
Wave 1: Architecture (discovers PCI compliance needed)
  ↓
Synthesis 1: "PCI compliance adds significant complexity"
  ↓
WAVE_COORDINATOR recalculates:
  - Original: 3 waves
  - Adjusted: 4 waves (added Wave 3b for compliance)
  ↓
Presents adjusted plan to user
  ↓
User approves
  ↓
Continues with 4-wave structure
```

**Output**:
```
⚠️ **Wave Structure Adjusted**

**Original Plan**: 3 waves
**Discovered**: PCI compliance requirement (Wave 1 revealed)
**Adjusted Plan**: 4 waves

**New Wave Inserted**:
Wave 3b: PCI Compliance (2 agents, 4h)
  - Security review
  - Compliance implementation

**Impact**:
- Timeline: +4h (necessary for PCI)
- Agents: +2
- User approval required

**Approve adjusted structure?**
```

**Key Learning**: wave-orchestration adapts to discovered complexity mid-execution.

---

### Example 12: Wave with Existing Plan

**Input**:
```bash
# Context: Previously ran /shannon:wave --plan

/shannon:wave
```

**Process**:
```
1. Check Serena for existing plan:
   plan = read_memory("wave_execution_plan")

2. Found existing plan ✅

3. Present plan summary:
   "Found existing wave plan (4 waves, 9 agents, 12h estimated)"

4. Ask user:
   "Execute existing plan OR generate new plan?"

5. User choice: Execute existing

6. WAVE_COORDINATOR loads plan and executes
```

**Output**:
```
📋 Existing Wave Plan Found

**Plan**: wave_execution_plan_20251108
**Created**: 2025-11-08T20:00:00Z
**Waves**: 4
**Agents**: 9
**Estimated**: 12h

**Execute this plan?**
- [YES] - Execute with existing structure
- [NO] - Generate new plan (--plan flag recommended first)
- [MODIFY] - Load plan for editing (advanced)

[User selects YES]

Executing existing plan...
[Normal wave execution proceeds]
```

**Key Learning**: --plan creates reusable plan stored in Serena. Can execute multiple times if needed (e.g., retry after fixing issues).

---

### Example 13: SITREP Protocol (High Complexity >=0.70)

**Input**:
```bash
/shannon:wave Build enterprise resource planning system
```

**Context**: Complexity 0.82 (HIGH), requires SITREP coordination protocol

**SITREP Integration**:
```
Complexity 0.82 triggers SITREP (>=0.70 threshold)

After EACH wave synthesis:
1. WAVE_COORDINATOR generates SITREP:

   **SITUATION**:
   - Wave 2 of 6 complete
   - 5 agents deployed (3 succeeded, 2 in progress)

   **OBJECTIVES**:
   - Complete foundation modules (ERP core)
   - Next: Implement inventory management

   **PROGRESS**:
   - Overall: 35% complete (Wave 2/6)
   - Timeline: On track (12h spent / 35h estimated)

   **BLOCKERS**:
   - Financial module awaiting API key (vendor delay)
   - Workaround: Using test API for now

   **NEXT ACTIONS**:
   - Resolve API key issue
   - Begin Wave 3 (inventory management)
   - Expected completion: Wave 3 by EOD tomorrow

2. User reviews SITREP

3. User provides feedback/approvals

4. Next wave begins
```

**Output**:
```
🌊 Wave 2 Complete - SITREP

## SITUATION
- Wave: 2 of 6
- Agents: 5 deployed (all succeeded ✅)
- Phase: Foundation complete

## OBJECTIVES
- Completed: ERP core modules, database schema
- Next: Inventory + Supply Chain (Wave 3)

## PROGRESS
- Overall: 35% (on track)
- Timeline: 12h spent / 35h estimated
- Speedup: 2.8x (actual vs sequential)

## BLOCKERS
- ⚠️ Financial module API key pending (vendor approval)
- Mitigation: Using sandbox API, will switch when live key available

## NEXT ACTIONS
1. Begin Wave 3: Inventory Management (6 agents, 7h)
2. Parallel-track: API key approval
3. Expected: Wave 3 complete by 2025-11-09 18:00

**User Approval Required to Proceed**:
- [ ] Approve Wave 3 execution
- [ ] Address blockers first
- [ ] Modify plan
```

**Key Learning**: High complexity (>=0.70) requires SITREP protocol for coordination visibility.

---

### Example 14: Wave Abort & Restart

**Input**:
```bash
# Mid-wave discovery: Wrong approach
User: "Stop Wave 2, the architecture is wrong"

/shannon:wave --abort
```

**Process**:
```
1. Detect active wave: Wave 2 in progress

2. Abort protocol:
   - Gracefully stop running agents
   - Save partial wave results: wave_2_partial
   - DO NOT synthesize incomplete wave
   - Restore from pre-wave checkpoint

3. User addresses architecture issue

4. Restart with corrected approach:
   /shannon:wave --restart-from wave-1

5. Re-execute from Wave 1 with new architecture
```

**Output**:
```
⚠️ Wave 2 Aborted

**Status**: Wave 2 terminated (2/3 agents incomplete)
**Reason**: User-requested abort (architecture revision needed)

**Saved**:
✓ Partial results: wave_2_partial_20251108
✓ Wave 1 intact: wave_1_complete

**Restored**:
✓ Checkpoint: pre_wave_2_checkpoint
✓ State: As of Wave 1 synthesis

**Next Steps**:
1. Address architectural issues
2. Update architecture in Serena
3. Restart: /shannon:wave --restart-from wave-1

**Time Lost**: 3h (Wave 2 partial work)
**Time Saved by Early Abort**: 18h (vs discovering issue in Wave 5)
```

**Key Learning**: Wave checkpoints enable early abort with minimal waste. Better to lose 3h than discover issue after 20h.

---

### Example 15: Single-Wave Execution (Complexity Just Above Threshold)

**Input**:
```bash
/shannon:wave Add analytics dashboard
```

**Context**: Complexity 0.51 (just above 0.50 threshold)

**Wave Structure** (minimal overhead):
```
Wave 1: Analytics Implementation (3 agents PARALLEL, 5h)
  - Chart components (frontend)
  - Analytics API (backend)
  - Data aggregation (database queries)

Only 1 wave needed (all work independent)

Sequential: 5h + 5h + 5h = 15h
Parallel: max(5h, 5h, 5h) = 5h
Speedup: 3.0x
```

**Output**:
```
🌊 Wave 1 Complete

**Strategy**: Single-Wave Parallel
**Agents**: 3 (all in Wave 1)
**Duration**: 5h
**Speedup**: 3.0x (vs 15h sequential)

**Deliverables**:
├─ Chart Components: 8 React components
├─ Analytics API: 6 endpoints
└─ Data Aggregation: 4 optimized queries

**Tests**: 10 Puppeteer tests (dashboard user flows)

**Observation**: Simple projects (complexity ~0.50) often need only 1 parallel wave.
```

**Key Learning**: Complexity 0.50-0.55 often results in single-wave execution (still benefits from parallelism).

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Running Waves Without /shannon:wave First

**Symptom**:
```bash
/shannon:wave Build app  # No /shannon:wave run first
```

**Why It Fails**:
- wave-orchestration needs complexity score to allocate agents
- No spec_analysis in Serena
- Cannot determine execution strategy

**Shannon Response**:
```
❌ **PREREQUISITE MISSING**

**Required**: Specification analysis must run BEFORE wave execution

**Missing**: spec_analysis not found in Serena

**Action Required**:
1. Run /shannon:wave first:
   /shannon:wave "Build app with [features]"

2. Then run /shannon:wave:
   /shannon:wave

**Why**: Wave structure depends on:
- Complexity score (determines agent count)
- Domain percentages (determines agent types)
- Phase plan (determines wave grouping)

**Cannot proceed without spec analysis.**
```

**Recommendation**: ALWAYS run /shannon:wave before /shannon:wave. Exception: Resuming existing waves.

---

### ❌ Anti-Pattern 2: Expecting Speedup for Sequential Work

**Symptom**:
```bash
User: "Why only 1.1x speedup? I expected 3x!"
```

**Why**:
- Project has strict dependency chain
- Each phase must complete before next begins
- No parallelization opportunities

**Shannon Response**:
```
**Your Project Dependencies**:
```
Phase A (Database)
  ↓ (B depends on A)
Phase B (Backend API)
  ↓ (C depends on B)
Phase C (Frontend)
  ↓ (D depends on C)
Phase D (Testing)
```

**Parallelization Opportunities**: NONE (strict chain)

**Result**:
Wave 1: Phase A (3h)
Wave 2: Phase B (4h)
Wave 3: Phase C (5h)
Wave 4: Phase D (2h)
Total: 14h

**Sequential**: 3+4+5+2 = 14h (same)
**Speedup**: 1.0x (no parallelism possible)

**Why Shannon Still Used Waves**:
- Synthesis checkpoints between phases
- Context preservation at boundaries
- Clean validation gates
- Recovery capability if issues arise

**Value**: Not speedup, but STRUCTURE and SAFETY
```

**Recommendation**: Don't expect speedup for inherently sequential work. Wave benefits = checkpoints + gates.

---

### ❌ Anti-Pattern 3: Skipping Synthesis Checkpoints "To Save Time"

**Symptom**:
```bash
User: "Run all waves back-to-back, skip checkpoints, we're behind schedule"
```

**Shannon Counter** (Iron Law #1):
```
❌ **CANNOT SKIP SYNTHESIS CHECKPOINTS**

**This is Iron Law #1** (non-negotiable even under):
- CEO authority
- Critical deadlines
- "We're behind schedule"

**Why Checkpoints Are Mandatory**:
- Synthesis takes 15 min per wave
- Skipping risks HOURS of rework from cascading failures
- "Behind schedule" means checkpoints are MORE critical (catch issues early)

**What Happens if You Skip**:
Wave 1: 3h → Integrates to Wave 2 (no validation)
Wave 2: 5h → Integrates to Wave 3 (no validation)
Wave 3: 4h → FAILS (integration conflict from Wave 1)
Recovery: Re-do Waves 2-3 = 9h wasted

**With Checkpoints**:
Wave 1: 3h → Synthesis (15min) → Issue caught → Fixed (30min)
Wave 2: 5h → Synthesis (15min) → Clean ✅
Wave 3: 4h → Success
Total: 12h 30min vs 21h (catching late) = 8.5h saved

**Shannon Will Not Proceed Without Checkpoints**
```

**Recommendation**: Trust the Iron Laws. Checkpoints save time, don't waste it.

---

### ❌ Anti-Pattern 4: Sequential Agent Spawning

**Symptom**:
```bash
# Agent spawns Wave 2 agents one by one
Message 1: <invoke>Agent 1</invoke>
[waits for completion]
Message 2: <invoke>Agent 2</invoke>
[waits for completion]
Message 3: <invoke>Agent 3</invoke>
```

**Why It Fails**:
- Sequential spawning = NO parallelism
- Duration: Agent1 + Agent2 + Agent3 (sum)
- NOT: max(Agent1, Agent2, Agent3)

**Shannon Enforcement** (Iron Law #5):
```
⚠️ **PARALLELISM VIOLATION DETECTED**

**Issue**: Agents spawned sequentially (3 separate messages)

**Result**: NO SPEEDUP
- Agent 1: 12 min
- Agent 2: 12 min
- Agent 3: 12 min
- Total: 36 minutes

**Required**: All wave agents in ONE message
```
<function_calls>
  <invoke>Agent 1</invoke>
  <invoke>Agent 2</invoke>
  <invoke>Agent 3</invoke>
</function_calls>
```

**Result**: PARALLELISM
- All 3: max(12, 12, 12) = 12 minutes
- Speedup: 3x faster

**Correction**: wave-orchestration skill enforces parallel spawning
```

**Recommendation**: WAVE_COORDINATOR ensures correct parallel spawning. Don't manual-spawn.

---

### ❌ Anti-Pattern 5: Under-Allocating Agents Based on "Feels Like Too Many"

**Symptom**:
```bash
Algorithm: "Complexity 0.72 → 8-12 agents recommended"
User: "8 agents feels like overkill, let's use 3"
```

**Shannon Counter** (Iron Law #3):
```
❌ **CANNOT OVERRIDE COMPLEXITY-BASED ALLOCATION**

**Algorithm Calculation**:
- Complexity: 0.72 (HIGH band: 0.70-0.85)
- Agent allocation: 8-15 agents
- Recommendation: 10 agents

**Your Suggestion**: 3 agents

**Impact of Under-Allocation**:
```
With 10 agents (algorithm):
  - Timeline: 18h parallel
  - Speedup: 3.2x

With 3 agents (user suggestion):
  - Timeline: 42h (can't parallelize enough)
  - Speedup: 1.4x
  - LOST: 24 hours (vs optimal)
```

**Why Algorithm is Correct**:
- 8D complexity framework accounts for:
  * Structural complexity (file count)
  * Coordination needs (team size)
  * Technical complexity (advanced features)
- User intuition under-estimates by 50-70%

**Proceeding with**: 10 agents (algorithm recommendation)

**If resource constrained**:
- Option: Extend timeline (42h vs 18h)
- Option: Reduce scope (fewer features → lower complexity)
- NOT: Under-allocate and expect same timeline
```

**Recommendation**: Trust complexity-based allocation. Algorithm is objective, "feels like" is subjective.

---

## Integration with Other Commands

### Workflow: /shannon:wave → /shannon:wave

**Complete Flow**:
```bash
# Step 1: Analyze specification
/shannon:wave "Build marketplace platform..."

# Output:
# Complexity: 0.68 (COMPLEX)
# Execution Strategy: WAVE-BASED ← Triggers /shannon:wave

# Step 2: Execute waves
/shannon:wave

# This reads spec_analysis and generates waves
```

**Data Flow**:
```
/shannon:wave
  ↓
spec-analysis calculates complexity: 0.68
  ↓
Saves: write_memory("spec_analysis_ID", {complexity: 0.68, domains: {...}})
  ↓
/shannon:wave
  ↓
wave-orchestration reads: read_memory("spec_analysis_ID")
  ↓
Uses complexity 0.68 to allocate: 8-12 agents across 3-5 waves
```

---

### Workflow: /shannon:wave → /shannon:wave --resume

**Recovery Scenario**:
```bash
# Working on Wave 2, context loss occurs

# Step 1: Context lost (auto-compact or session break)

# Step 2: Restore
/shannon:wave  # Or /shannon:prime

# Step 3: Resume wave execution
/shannon:wave --resume

# This detects incomplete wave, continues from last checkpoint
```

---

## Troubleshooting

### Issue: "Wave execution not starting"

**Diagnosis**:
```bash
# Check prerequisites
/list_memories | grep spec_analysis
# Should show: spec_analysis_[id]

# If missing:
❌ Run /shannon:wave first

# Check Serena MCP
/list_memories
# Should work without error

# If error:
❌ Serena MCP not configured
```

---

### Issue: "No parallelism detected, all waves sequential"

**Cause**: Project has sequential dependencies

**Example**:
```
Your project:
  Database schema → Backend API → Frontend UI → Testing
  (each depends on previous)

Result: 4 sequential waves (no parallelism)
```

**This is CORRECT BEHAVIOR** - wave-orchestration detects dependencies and creates optimal structure.

**If you think parallelism IS possible**:
- Review dependency graph (are dependencies real?)
- Consider: Can frontend start with mocked API? (❌ NO MOCKS - so no)
- Redesign: Remove dependencies (API contracts allow parallel work)

---

### Issue: "Synthesis checkpoint taking too long (>30 min)"

**Cause**: Large wave with many agents (>7 agents)

**Diagnosis**:
```
Wave 5: 10 agents deployed
Synthesis needs to:
- Collect 10 agent results
- Cross-validate for conflicts
- Aggregate deliverables
- Create synthesis document

Estimated: 20-30 minutes for 10 agents
```

**This is EXPECTED** for large waves.

**Optimization**:
- Split wave into 2 smaller waves (5 agents each)
- Synthesis time: 15 min × 2 = 30 min total (but checkpoints earlier)
- Trade-off: More waves vs faster synthesis

---

## Performance Expectations

| Wave Size | Synthesis Time | Speedup | Efficiency |
|-----------|----------------|---------|------------|
| 2 agents | 10-15 min | 1.5-1.8x | 75-90% |
| 3 agents | 15-20 min | 2.0-2.5x | 65-85% |
| 5 agents | 20-25 min | 3.0-4.0x | 60-80% |
| 7 agents | 25-30 min | 3.5-5.0x | 50-70% |
| 10 agents | 30-40 min | 4.0-6.0x | 40-60% |

**Synthesis overhead is WORTH IT** - prevents integration failures that cost hours.

---

## Advanced Usage

### Custom Wave Request (Override Default Plan)

**Input**:
```bash
/shannon:wave Build frontend in 2 parallel tracks: components in Wave 1, pages in Wave 2
```

**Process**:
```
wave-orchestration interprets custom request:
- User wants 2 waves (not default dependency-based structure)
- Wave 1: Components
- Wave 2: Pages (depends on Wave 1)

Generates custom structure matching user request
(overrides default phase plan structure)
```

**Value**: Allows experienced users to specify wave structure explicitly.

---

### Wave Metrics Review

**Input**:
```bash
# After waves complete
/shannon:wave pattern wave-execution
```

**Output**:
```
📊 Wave Execution Pattern Analysis

**Historical Waves** (last 5 projects):
1. Project A: 3 waves, 2.4x speedup
2. Project B: 5 waves, 3.1x speedup
3. Project C: 2 waves, 1.8x speedup
4. Project D: 4 waves, 2.9x speedup
5. Project E: 6 waves, 3.5x speedup

**Average Speedup**: 2.7x

**Efficiency Trends**:
- Waves with 3-5 agents: 75% avg efficiency
- Waves with 7+ agents: 55% avg efficiency
- Optimal: 3-5 agents per wave for balance

**Recommendations**:
- Your projects average 3.5 waves
- Optimal agent count: 4-5 per wave
- Synthesis time: ~20 min per wave (consistent)
```

**Value**: Learn from historical wave patterns to optimize future executions.

---

## Command Output Reference

### Planning Mode Output (--plan)

```
📋 Wave Execution Plan

1. Wave Structure (N waves)
2. Agent Allocation (per wave)
3. Dependency Graph
4. Estimated Timeline
5. Parallelization Opportunities
6. Speedup Calculation
7. Risk Assessment (for --dry-run)
8. Token Budget (for --dry-run)

Saved to: wave_execution_plan_{timestamp}
```

### Execution Mode Output

```
🌊 Wave N of M Complete

1. Execution Summary (wave details)
2. Agent Results (per agent deliverables)
3. Synthesis (cross-validation)
4. Goal Alignment (if North Star exists)
5. Tests (functional test results)
6. Next Wave Preview (if not final wave)
7. Checkpoint Confirmation

After ALL waves:
🎉 All Waves Complete
- Final metrics (total time, speedup, efficiency)
- Complete deliverables list
- Goal achievement (0.0-1.0)
- Next steps (deployment, documentation)
```

---

## FAQ

**Q: When should I use /shannon:wave vs just implementing?**
A: Use /shannon:wave when:
   - Complexity >=0.50 (from /shannon:wave)
   - Multiple independent components
   - Want 2-4x speedup

   Skip /shannon:wave when:
   - Complexity <0.50 (sequential is fine)
   - Single linear task
   - Strict dependency chain (no parallelism possible)

**Q: Can I modify wave structure after generation?**
A: Yes, use --plan to review, then manually adjust in Serena before executing.

**Q: What if a wave fails mid-execution?**
A: wave-orchestration includes error recovery:
   - Failed agents respawn with fixes
   - Partial wave saved
   - Continue from last successful wave

**Q: How long does synthesis take?**
A: 10-30 minutes per wave depending on agent count. This is NECESSARY for validation.

**Q: Can I skip waves 2-3 and jump to wave 4?**
A: No. Dependencies must be satisfied. Cannot skip waves.

---

**Command**: /shannon:wave
**Skill**: wave-orchestration (shannon-plugin/skills/wave-orchestration/SKILL.md)
**Agent**: WAVE_COORDINATOR (shannon-plugin/agents/WAVE_COORDINATOR.md)
**Examples**: 15 comprehensive scenarios
**Anti-Patterns**: 5 common mistakes + corrections
**Integration**: Links to /shannon:wave (prerequisite), /shannon:wave (recovery)
