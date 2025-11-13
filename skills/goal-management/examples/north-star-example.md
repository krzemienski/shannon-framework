# North Star Goal Example: E-Commerce MVP Launch

**Date**: 2025-11-03
**Skill**: goal-management
**Scenario**: Multi-session project with goal tracking from specification to completion

---

## Overview

This example demonstrates the complete lifecycle of a North Star goal from initial specification through wave execution to completion. Shows goal parsing, progress tracking, wave integration, and context preservation.

---

## Phase 1: Initial Goal Setting

### User Input

```
User: "I want to build an e-commerce platform. It needs to be good quality
with the essentials - users should be able to browse products, register an
account, and checkout with their credit card. This is the MVP."
```

### Goal Parsing (Automatic)

**Skill Activation**: @goal-management (set mode)

**Parsing Process**:
1. Extract vague term: "good quality" → Interpret as "functional, testable"
2. Extract features: browse products, register account, checkout
3. Generate milestones with weights:
   - User Authentication (35%): Register, login, session management
   - Product Catalog (35%): Display, search, filtering
   - Payment Processing (30%): Stripe integration, checkout flow

**Structured Goal Created**:
```json
{
  "goal_id": "GOAL-20251103T140000",
  "goal_text": "Launch e-commerce MVP with auth, catalog, and payments",
  "priority": "north-star",
  "status": "active",
  "progress": 0,
  "created_at": "2025-11-03T14:00:00.000Z",
  "updated_at": "2025-11-03T14:00:00.000Z",
  "milestones": [
    {
      "name": "User Authentication",
      "description": "Users can register, login, and maintain sessions",
      "weight": 35,
      "status": "pending",
      "completion_criteria": "Auth functional tests pass (NO MOCKS)",
      "completion_date": null
    },
    {
      "name": "Product Catalog",
      "description": "Products displayed with search and filtering",
      "weight": 35,
      "status": "pending",
      "completion_criteria": "Catalog functional tests pass",
      "completion_date": null
    },
    {
      "name": "Payment Processing",
      "description": "Users can checkout with Stripe",
      "weight": 30,
      "status": "pending",
      "completion_criteria": "Stripe integration tests pass (real test mode)",
      "completion_date": null
    }
  ],
  "deadline": null,
  "wave_links": []
}
```

**Stored in Serena**:
- Namespace: `shannon/goals`
- Entity: `goal-20251103T140000`
- Type: `shannon-goal`
- Relations: goal → current-project

**User Notification**:
```
✅ North Star Goal Set: GOAL-20251103T140000

Goal: Launch e-commerce MVP with auth, catalog, and payments
Priority: ⭐ North Star
Progress: 0%

Milestones:
1. User Authentication (35%) - Pending
2. Product Catalog (35%) - Pending
3. Payment Processing (30%) - Pending

Next Action: Run @spec-analysis to determine complexity and wave plan.

Goal persisted to Serena (survives context compaction).
```

---

## Phase 2: Wave Execution with Goal Integration

### Wave 1: User Authentication

**Before Wave Execution**:

**Goal Validation** (Automatic):
```
Validating Wave 1 deliverables against goal...
Goal milestone: User Authentication (35% weight)
Wave 1 deliverables:
  - User registration with email/password
  - Login with JWT tokens
  - Session management
✅ Alignment verified. Wave deliverables match goal milestone.
```

**Wave Execution**:
- 2 agents execute Wave 1 tasks
- Backend: Auth endpoints
- Frontend: Registration/login forms
- Functional tests: NO MOCKS, real database

**After Wave Completion**:

**Goal Update** (Automatic):
```json
{
  "mode": "update",
  "goal_id": "GOAL-20251103T140000",
  "notes": "Wave 1 complete. Auth tests passing (12/12 tests, NO MOCKS)."
}
```

**Processing**:
1. Retrieve goal from Serena
2. Check milestone completion: "Auth tests passing" → Mark milestone complete
3. Calculate progress: 35% (User Authentication complete)
4. Update wave_links: Add Wave 1 deliverables
5. Store updated goal in Serena

**User Notification**:
```
✅ Goal Progress Updated: GOAL-20251103T140000

Progress: 35% (+35%)
Milestone Complete: User Authentication ✅

Remaining Milestones:
- Product Catalog (35%) - In Progress
- Payment Processing (30%) - Pending

Next Action: Execute Wave 2 for Product Catalog.
```

---

## Phase 3: Context Compaction and Goal Restoration

### Scenario: 50 Messages Later, Context Compacted

**User Input**:
```
User: "What was our goal again? How far are we?"
```

**Goal Retrieval** (Automatic):

**Skill Activation**: @goal-management (show mode)

**Process**:
1. Query Serena: `search_nodes("shannon-goal active")`
2. Retrieve: `GOAL-20251103T140000`
3. Parse current state from observations
4. Display goal summary

**User Notification**:
```
⭐ North Star Goal: GOAL-20251103T140000

Goal: Launch e-commerce MVP with auth, catalog, and payments
Priority: North Star
Progress: 35%

Milestones:
✅ User Authentication (35%) - Completed 2025-11-03
🔄 Product Catalog (35%) - In Progress
⏳ Payment Processing (30%) - Pending

Wave History:
- Wave 1: User Authentication (completed)

Next Action: Complete Product Catalog milestone (Wave 2).

Created: 2 hours ago
Last Updated: 30 minutes ago
```

**Key Benefit**: Goal state retrieved from persistent storage despite context compaction. User doesn't need to re-explain goal.

---

## Phase 4: Multiple Goals and Prioritization

### Scenario: User Adds Secondary Goal

**User Input**:
```
User: "Also add social login support (Facebook, Google) as a stretch goal."
```

**Goal Creation** (Automatic):

**Skill Activation**: @goal-management (set mode)

**Process**:
1. Parse goal: Social login support
2. Generate milestones: OAuth integrations
3. Assign priority: "high" (not North Star)
4. Store in Serena with lower priority

**User Notification**:
```
✅ Goal Created: GOAL-20251103T160000

Goal: Add social login (Facebook, Google)
Priority: High (Secondary Goal)
Progress: 0%

⭐ North Star Remains: GOAL-20251103T140000 (E-commerce MVP)

Recommendation: Complete North Star goal (35% → 100%) before starting
secondary goal to maintain focus.
```

**Goal List**:
```
Active Goals:

⭐ North Star:
GOAL-20251103T140000 | E-commerce MVP | 35% | Active

Secondary Goals:
GOAL-20251103T160000 | Social login | 0% | Active | Priority: High
```

---

## Phase 5: Goal Completion

### Scenario: All Milestones Complete

**Wave 3 Complete** (Payment Processing):

**Goal Update** (Automatic):
```json
{
  "mode": "update",
  "goal_id": "GOAL-20251103T140000",
  "notes": "Wave 3 complete. Stripe integration tests passing (real test mode)."
}
```

**Processing**:
1. Mark "Payment Processing" milestone complete
2. Calculate progress: 100% (all milestones complete)
3. Detect completion threshold reached
4. Prompt user for completion confirmation

**User Notification**:
```
🎉 Goal Progress: 100%

All milestones complete for GOAL-20251103T140000!

Milestones:
✅ User Authentication (35%)
✅ Product Catalog (35%)
✅ Payment Processing (30%)

Recommendation: Mark goal complete with /shannon:goal complete GOAL-20251103T140000
```

### User Marks Complete

**User Input**:
```
/shannon:goal complete GOAL-20251103T140000
```

**Skill Activation**: @goal-management (complete mode)

**Process**:
1. Retrieve goal from Serena
2. Update status: "completed"
3. Set completed_at: current timestamp
4. Calculate velocity: created_at to completed_at
5. Archive goal (status="completed", preserve for history)

**User Notification**:
```
🎉 Goal Complete: GOAL-20251103T140000

Goal: Launch e-commerce MVP with auth, catalog, and payments
Duration: 3 days (72 hours)
Milestones: 3/3 complete (100%)
Waves: 3 waves executed

Velocity: 24 hours per milestone
Quality: All functional tests passing (NO MOCKS)

Goal archived to history. Visible with /shannon:goal history.

Next Action: Consider promoting secondary goal (GOAL-20251103T160000)
to North Star, or set new goal.
```

---

## Phase 6: Goal History and Retrospective

### User Reviews History

**User Input**:
```
/shannon:goal history
```

**Skill Activation**: @goal-management (history mode)

**Process**:
1. Query Serena: `search_nodes("shannon-goal completed")`
2. Sort by completed_at (descending)
3. Calculate metrics: velocity, completion rate
4. Display timeline

**User Notification**:
```
Goal History:

Completed Goals:
┌──────────────────┬─────────────────────────────────┬──────────┬──────────┐
│ Goal ID          │ Goal Text                       │ Duration │ Progress │
├──────────────────┼─────────────────────────────────┼──────────┼──────────┤
│ GOAL-20251103... │ E-commerce MVP                  │ 3 days   │ 100%     │
└──────────────────┴─────────────────────────────────┴──────────┴──────────┘

Metrics:
- Goals completed: 1
- Average duration: 3 days
- Average milestones per goal: 3
- Completion rate: 100% (1 completed, 0 abandoned)

Pattern Analysis:
- All goals completed within deadline
- Functional testing approach (NO MOCKS) used consistently
- Wave execution used for all goals

Active Goals:
┌──────────────────┬─────────────────────────────────┬──────────┬──────────┐
│ Goal ID          │ Goal Text                       │ Priority │ Progress │
├──────────────────┼─────────────────────────────────┼──────────┼──────────┤
│ GOAL-20251103... │ Social login                    │ High     │ 0%       │
└──────────────────┴─────────────────────────────────┴──────────┴──────────┘
```

---

## Key Takeaways

### 1. Vague Goals → Structured Goals
- Input: "Build a good platform"
- Output: 3 measurable milestones with weights and criteria
- Benefit: Eliminates scope creep and misalignment

### 2. Progress Tracking
- Automatic progress calculation from milestone status
- User can always ask "How far are we?" and get precise answer
- No manual tracking required

### 3. Context Survival
- Goal stored in Serena, survives compaction
- Retrievable across sessions without user re-explanation
- Persistent state enables multi-day projects

### 4. Wave Integration
- Goals validate wave deliverables (alignment check)
- Wave completion updates goal progress automatically
- Goal-wave linkage prevents drift

### 5. Priority Management
- North Star designation focuses effort
- Secondary goals tracked but don't distract
- Clear recommendation: finish North Star first

### 6. History and Learning
- Completed goals archived for retrospectives
- Velocity metrics enable planning
- Pattern analysis identifies best practices

---

## Anti-Patterns Avoided

This example demonstrates how goal-management skill prevents RED phase violations:

1. ✅ **Vague Goal Parsed**: "Good platform" → 3 measurable milestones
2. ✅ **Goal Survives Compaction**: Retrieved from Serena after 50 messages
3. ✅ **Progress Tracked**: 35% → 100% with milestone-based calculation
4. ✅ **Priorities Managed**: North Star vs secondary goals
5. ✅ **History Maintained**: Completed goal archived with metrics
6. ✅ **Wave Integration**: Goal validates and updates from wave execution

**Without goal-management**: All 6 violations from RED phase would occur.

**With goal-management**: Zero violations, complete goal lifecycle management.

---

**Example Status**: Complete ✅
**Demonstrates**: Full goal lifecycle from vague input to completion
**Duration**: Multi-session project (3 days)
**Outcome**: 100% goal completion with zero context loss
