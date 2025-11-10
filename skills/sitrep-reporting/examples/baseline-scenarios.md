# RED Phase: Baseline Scenarios (Without SITREP Skill)

## Purpose
Test agent behavior WITHOUT sitrep-reporting skill to document violations that the skill must prevent.

## Scenario 1: Vague Status Updates
**Setup**: Ask agent to report progress on multi-step task
**Expected Violation**: Agent provides unstructured narrative without status codes, progress percentage, or ETA

**Test**:
```
User: "Give me a status update on your progress implementing the user authentication system"

Expected Agent Response (WITHOUT SKILL):
"I'm working on the authentication system. Made some good progress on the login form.
Still need to handle the backend API. Should be done soon."
```

**Violations to Document**:
- ❌ No status code (🟢🟡🔴)
- ❌ No quantitative progress (0-100%)
- ❌ "Soon" is not an ETA
- ❌ No blockers identified
- ❌ No dependencies tracked
- ❌ No current task specified
- ❌ No completed items listed

---

## Scenario 2: No Structure or Format
**Setup**: Agent working on Wave 2 of implementation, request SITREP
**Expected Violation**: Free-form response without military SITREP structure

**Test**:
```
User: "WAVE_COORDINATOR requesting SITREP from frontend-dev agent"

Expected Agent Response (WITHOUT SKILL):
"Hey, I'm doing okay. Got the components built but having some trouble with the API
integration. The backend team hasn't given me the endpoints yet so I'm kind of stuck.
Probably need another day or two."
```

**Violations to Document**:
- ❌ No SITREP header/footer structure
- ❌ No authorization code for handoff
- ❌ Informal tone ("Hey", "okay", "kind of")
- ❌ No explicit blocker status (🔴 BLOCKED)
- ❌ No dependency tracking format
- ❌ "Probably another day or two" is not precise ETA
- ❌ No checkpoint identification

---

## Scenario 3: Missing Progress Metrics
**Setup**: Agent completing complex multi-phase task, request progress update
**Expected Violation**: Qualitative descriptions without quantitative metrics

**Test**:
```
User: "Provide progress update on database migration"

Expected Agent Response (WITHOUT SKILL):
"The database migration is going well. I've finished the schema design and started
working on the data transformation scripts. Still have the validation and rollback
procedures to implement."
```

**Violations to Document**:
- ❌ "going well" is not a status code
- ❌ No percentage complete
- ❌ Cannot track velocity without metrics
- ❌ No time estimate for remaining work
- ❌ No risk assessment (on track vs at risk)
- ❌ No next checkpoint defined

---

## Scenario 4: Lost Context in Handoffs
**Setup**: Two agents collaborating, frontend needs backend deliverable
**Expected Violation**: No authorization code, unclear if work is actually ready

**Test**:
```
Frontend Agent: "Is the API ready for integration?"
Backend Agent: "Yeah, I think it's ready. You can start using it."
```

**Violations to Document**:
- ❌ No HANDOFF authorization code
- ❌ "I think" indicates uncertainty
- ❌ No formal deliverable confirmation
- ❌ No audit trail for handoff
- ❌ Cannot verify work was actually completed
- ❌ No checkpoint reference

---

## Scenario 5: Missed Coordination Window
**Setup**: Wave coordinator checking on 3 sub-agents, one is blocked but doesn't report
**Expected Violation**: Agent waits too long to report blocker, delays entire wave

**Test**:
```
Coordinator: "Request status from all sub-agents"
Database Agent: "Still working on the schema validation"
[45 minutes pass]
Database Agent: "Actually I'm blocked - the ORM library has a bug"
```

**Violations to Document**:
- ❌ No 30-minute SITREP interval
- ❌ Blocker identified too late
- ❌ No 🔴 BLOCKED status when blocker occurred
- ❌ No trigger-based SITREP (should report immediately when blocked)
- ❌ Entire wave delayed by communication failure

---

## Documentation Checklist

After running these scenarios, document:

1. **Rationalization Patterns**:
   - "User knows what I mean" → No, need formal structure
   - "Status is obvious from my messages" → No, need explicit codes
   - "I'll report when done" → No, need regular intervals
   - "Coordinator can see my work" → No, need authorization codes

2. **Communication Failures**:
   - Lost context between agents
   - Unclear handoff readiness
   - Delayed blocker reporting
   - No audit trail

3. **Metrics Gaps**:
   - Cannot calculate velocity
   - Cannot predict completion
   - Cannot identify at-risk tasks
   - Cannot coordinate dependencies

4. **Timing Issues**:
   - No regular reporting interval
   - No trigger-based reporting
   - Blockers reported too late

---

## Expected Outcome

After RED phase testing:
- 15-20 documented violations
- 4-5 rationalization patterns identified
- Clear need for structured SITREP protocol
- Baseline for GREEN phase compliance testing

---

**Next**: GREEN phase - Create SKILL.md that prevents ALL documented violations
