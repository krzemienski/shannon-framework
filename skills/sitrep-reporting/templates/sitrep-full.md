═══════════════════════════════════════════════════════════
🎯 SITREP: {AGENT_NAME}
═══════════════════════════════════════════════════════════

**STATUS**: {🟢 ON TRACK | 🟡 AT RISK | 🔴 BLOCKED}
**PROGRESS**: {0-100}% complete
**CURRENT TASK**: {task_description}

**COMPLETED**:
- ✅ {completed_item_1}
- ✅ {completed_item_2}
- ✅ {completed_item_3}

**IN PROGRESS**:
- 🔄 {active_task_1} ({percentage}% complete)
- 🔄 {active_task_2} ({percentage}% complete)

**BLOCKERS**: {blocker_description | NONE}

**DEPENDENCIES**:
- ⏸️ Waiting: {dependency} from {agent}
- ✅ Ready: {dependency} available

**ETA TO COMPLETION**: {time_estimate}
**NEXT CHECKPOINT**: {checkpoint_description}
**HANDOFF**: {HANDOFF-AGENT-TIMESTAMP-HASH | N/A}

═══════════════════════════════════════════════════════════

---

## Usage Instructions

### When to Use Full SITREP
- Regular 30-minute interval updates
- Coordinator requests detailed status
- Deliverable ready for handoff
- Complex status requiring detail

### Fields Guide

**STATUS**: Choose ONE:
- 🟢 ON TRACK: All progressing as planned, no blockers, ETA unchanged
- 🟡 AT RISK: Minor blockers, delays present, ETA slipping, recoverable
- 🔴 BLOCKED: Cannot proceed, needs intervention, work stopped

**PROGRESS**: Quantitative 0-100%
- 0%: Not started
- 25%: Design/planning complete
- 50%: Implementation half done
- 75%: Implementation done, testing in progress
- 100%: Complete, tested, documented

**CURRENT TASK**: Specific task being worked on RIGHT NOW

**COMPLETED**: List finished items with ✅
- Be specific: "Login component" not "frontend work"
- Include tests, docs if complete

**IN PROGRESS**: Active tasks with percentage
- Show sub-task progress: "API integration (60% complete)"
- Max 3 concurrent tasks

**BLOCKERS**: Explicit statement
- If NONE: Write "NONE"
- If blocked: Describe what's blocking and why
- 🔴 Status REQUIRES blocker description

**DEPENDENCIES**:
- ⏸️ Waiting: Dependencies not yet available
- ✅ Ready: Dependencies confirmed available
- Include agent name if waiting on agent

**ETA TO COMPLETION**: Time estimate
- Format: "2 hours", "30 minutes", "1 day"
- Update based on actual progress
- If blocked: "Unknown until blocker resolved"

**NEXT CHECKPOINT**: Next major milestone
- Used for wave coordination
- Specific deliverable: "User auth components complete"

**HANDOFF**: Authorization code OR N/A
- Include ONLY when deliverable 100% ready
- Format: HANDOFF-{agent}-{timestamp}-{hash}
- If not ready: Write "N/A"

### Examples

**On Track**:
```
**STATUS**: 🟢 ON TRACK
**PROGRESS**: 70% complete
**BLOCKERS**: NONE
**ETA TO COMPLETION**: 1.5 hours
**HANDOFF**: N/A
```

**At Risk**:
```
**STATUS**: 🟡 AT RISK
**PROGRESS**: 45% complete
**BLOCKERS**: Performance optimization taking longer than expected
**ETA TO COMPLETION**: 3 hours (originally 2 hours)
**HANDOFF**: N/A
```

**Blocked**:
```
**STATUS**: 🔴 BLOCKED
**PROGRESS**: 35% complete (PAUSED)
**BLOCKERS**: Backend API endpoints not available
**DEPENDENCIES**:
- ⏸️ Waiting: API specification from backend-dev agent
**ETA TO COMPLETION**: Unknown until blocker resolved
**HANDOFF**: N/A
```

**Deliverable Ready**:
```
**STATUS**: 🟢 ON TRACK (DELIVERABLE READY)
**PROGRESS**: 100% complete
**BLOCKERS**: NONE
**ETA TO COMPLETION**: COMPLETE
**HANDOFF**: HANDOFF-frontend-dev-1699034567-b8c4f2a9

Deliverable: User authentication components
Location: /src/components/auth/
Status: Tested, documented, ready for integration
```

---

## Common Mistakes to Avoid

❌ **Don't**: "Making good progress"
✅ **Do**: "**PROGRESS**: 65% complete"

❌ **Don't**: "Status seems okay"
✅ **Do**: "**STATUS**: 🟢 ON TRACK"

❌ **Don't**: "Should be done soon"
✅ **Do**: "**ETA TO COMPLETION**: 2 hours"

❌ **Don't**: Skip SITREP for informal updates
✅ **Do**: Use SITREP format EVERY TIME

❌ **Don't**: Wait to report blockers
✅ **Do**: Report 🔴 BLOCKED immediately

❌ **Don't**: Assume coordinator knows work is ready
✅ **Do**: Include HANDOFF authorization code
