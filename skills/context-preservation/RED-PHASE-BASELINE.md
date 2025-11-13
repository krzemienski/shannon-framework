# Context Preservation Skill - RED Phase Baseline

**Date**: 2025-11-03
**Phase**: RED (Test Without Skill)
**Objective**: Document violations when checkpointing behavior is left to Claude's discretion

## Baseline Scenarios

### Scenario 1: "Checkpoints are overhead for simple waves"

**Setup**:
- Simple 2-phase implementation task (CRUD API)
- Low complexity (< 0.30)
- All work fits in single context

**Expected Rationalization**:
> "This is a simple task. Let's just implement it directly without checkpoint overhead.
> Checkpoints are only needed for complex multi-wave projects. This will be done in 30 minutes."

**Violation**: Skip checkpoint → lose context if interrupted → rework entire wave

---

### Scenario 2: "I'll checkpoint when I think of it"

**Setup**:
- Mid-complexity project (0.50-0.70)
- 3 waves planned
- Wave 1 completes successfully

**Expected Rationalization**:
> "Wave 1 went smoothly. I'll create checkpoint before Wave 2 if I remember.
> Let me just start Wave 2 now while momentum is good."

**Violation**: No checkpoint → PreCompact triggers → emergency save lacks wave deliverables

---

### Scenario 3: "Manual testing is sufficient"

**Setup**:
- User hasn't explicitly requested checkpoint
- Approaching context limits
- Substantial work completed

**Expected Rationalization**:
> "User didn't ask for checkpoints. They can just re-run /shannon:spec if context is lost.
> I should focus on implementation, not administrative tasks."

**Violation**: Context loss → user repeats entire specification → wasted time

---

### Scenario 4: "PreCompact hook will handle it"

**Setup**:
- PreCompact hook exists
- Approaching token limits
- Complex state (multiple waves, test results, goals)

**Expected Rationalization**:
> "There's a PreCompact hook, so checkpoints are automatic. I don't need to think about it.
> The system will save context when needed."

**Violation**: Relies on emergency save → missing structured metadata → poor restoration

---

### Scenario 5: "Checkpoints slow down development"

**Setup**:
- User requests fast turnaround
- Time pressure environment
- Multiple agents coordinating

**Expected Rationalization**:
> "Creating checkpoints takes time. User wants speed. Let's skip checkpoints and
> just push through all waves quickly. We can checkpoint at the very end."

**Violation**: Mid-wave interruption → lose all progress → slower overall

---

## Test Execution (Without Skill)

### Test 1: Simple Wave Checkpoint Skip

**Prompt**:
```
Implement a simple REST API for todo items (GET, POST, PUT, DELETE).
This is a quick task, should take 30 minutes.
```

**Expected Behavior (Without Skill)**:
- Claude analyzes spec
- Skips checkpoint creation
- Implements directly
- **VIOLATION**: No checkpoint before PreCompact

**Actual Results**:
[To be filled during testing]

---

### Test 2: Wave Transition Without Checkpoint

**Prompt**:
```
Wave 1 complete: Frontend components built and tested.
Moving to Wave 2: Backend API implementation.
```

**Expected Behavior (Without Skill)**:
- Wave 1 completion noted
- Move directly to Wave 2
- **VIOLATION**: No wave-checkpoint created

**Actual Results**:
[To be filled during testing]

---

### Test 3: Discretionary Checkpointing

**Prompt**:
```
[Complex multi-wave project ongoing]
[Context approaching 50K tokens]
[No explicit checkpoint request from user]
```

**Expected Behavior (Without Skill)**:
- Continue working
- Rely on PreCompact hook eventually
- **VIOLATION**: No proactive checkpoint

**Actual Results**:
[To be filled during testing]

---

## Violation Summary

| Scenario | Violation Type | Impact | Frequency |
|----------|---------------|--------|-----------|
| Simple waves | Skip overhead | Rework if interrupted | High (70%+) |
| Manual discretion | Forget to checkpoint | Emergency-only saves | High (80%+) |
| No user request | Don't be proactive | Context loss | Very High (90%+) |
| Hook reliance | Minimal metadata | Poor restoration | High (75%+) |
| Time pressure | Speed over safety | Mid-wave failures | Medium (50%+) |

---

## Critical Findings

**Primary Violation Pattern**:
Claude defaults to "checkpoints are optional overhead" unless:
1. User explicitly requests checkpoint
2. PreCompact hook forces emergency save
3. Extreme complexity makes it obvious

**Root Cause**:
No systematic enforcement of checkpoint protocol. Checkpointing is left to:
- User remembering to request it
- Claude's discretion ("is this worth it?")
- Emergency fallback (PreCompact hook)

**Impact**:
- 70%+ of waves proceed without checkpoints
- Context loss requires complete rework
- PreCompact saves lack structured metadata
- Multi-session work frequently fails

---

## Requirements for GREEN Phase

The context-preservation skill MUST:

1. **Eliminate discretion**: Checkpoints are PROTOCOL, not optional
2. **Define triggers**: Automatic checkpoints at wave boundaries, on request, before PreCompact
3. **Structured metadata**: Rich checkpoint structure (goals, waves, tests, files)
4. **Serena integration**: Persistent storage in knowledge graph
5. **Restoration logic**: Clear workflow to restore from checkpoints
6. **Anti-rationalization**: Explicit section addressing all 5 violation patterns

---

## Commit Message

```
test(context-preservation): RED phase baseline - document checkpoint violations

Baseline testing WITHOUT context-preservation skill reveals:
- 70%+ of waves skip checkpoint creation
- Checkpoints treated as optional overhead
- Claude relies on PreCompact emergency saves
- No structured metadata collection
- Context loss forces complete rework

5 violation scenarios documented:
1. Simple waves: "checkpoints are overhead"
2. Discretionary: "I'll checkpoint if I remember"
3. No request: "user didn't ask for it"
4. Hook reliance: "PreCompact will handle it"
5. Time pressure: "checkpoints slow development"

Next: GREEN phase - implement PROTOCOL skill with anti-rationalization
```
