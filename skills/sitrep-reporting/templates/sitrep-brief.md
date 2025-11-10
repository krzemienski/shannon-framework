🎯 **{AGENT}** | {🟢🟡🔴} | {XX}% | ETA: {time}
Blockers: {NONE | description}

---

## Usage Instructions

### When to Use Brief SITREP
- Coordinator scanning multiple agents
- Quick status check
- Wave status summary
- Space-constrained reporting

### Format

```
🎯 **{AGENT}** | {STATUS} | {PROGRESS}% | ETA: {time}
Blockers: {blockers}
```

**Fields**:
- **AGENT**: Agent name (e.g., frontend-dev, backend-dev)
- **STATUS**: One emoji: 🟢 🟡 🔴
- **PROGRESS**: Percentage 0-100%
- **ETA**: Time estimate (e.g., "2h", "30min", "1d")
- **Blockers**: "NONE" or brief description

### Examples

**Single Agent**:
```
🎯 **frontend-dev** | 🟢 | 75% | ETA: 1h
Blockers: NONE
```

**Multiple Agents (Wave Summary)**:
```
🎯 **frontend-dev** | 🟢 | 85% | ETA: 45min
Blockers: NONE

🎯 **backend-dev** | 🟢 | 90% | ETA: 30min
Blockers: NONE

🎯 **database-dev** | 🟡 | 70% | ETA: 1.5h
Blockers: Performance optimization needed

🎯 **test-dev** | 🟢 | 60% | ETA: 2h
Blockers: NONE
```

**With Coordinator Analysis**:
```
🎯 **frontend-dev** | 🟢 | 75% | ETA: 1h
Blockers: NONE

🎯 **backend-dev** | 🟡 | 55% | ETA: 2h
Blockers: API optimization slower than expected

🎯 **database-dev** | 🔴 | 40% | ETA: Unknown
Blockers: Migration script failing

**Wave Status**: 3/3 agents reporting, 1 on track, 1 at risk, 1 blocked
**Coordinator Decision**: Escalate database blocker, continue wave
```

### Status Code Quick Reference

**🟢 ON TRACK**: All progressing, no blockers, ETA unchanged
**🟡 AT RISK**: Minor issues, delays, ETA slipping, recoverable
**🔴 BLOCKED**: Cannot proceed, needs intervention, work stopped

### When to Upgrade to Full SITREP

Use Brief SITREP for quick scans, but provide Full SITREP when:
- Agent is 🔴 BLOCKED (needs detail)
- Deliverable ready for handoff (needs HANDOFF code)
- Coordinator requests detailed status
- Blocker requires explanation

**Example Upgrade**:
```
Initial Brief:
🎯 **database-dev** | 🔴 | 40% | ETA: Unknown
Blockers: Migration failing

Coordinator Response: "Request full SITREP from database-dev"

Full SITREP:
═══════════════════════════════════════════════════════════
🎯 SITREP: database-dev (IMMEDIATE - Blocker Encountered)
═══════════════════════════════════════════════════════════

**STATUS**: 🔴 BLOCKED
**PROGRESS**: 40% complete (PAUSED)
**CURRENT TASK**: Production database migration

**BLOCKERS**: Migration script failing on production schema due to foreign
key constraints not present in staging environment. Need DBA to review
production schema and update migration scripts.

**COORDINATOR ACTION NEEDED**: Escalate to DBA team for immediate review
```

---

## Common Mistakes to Avoid

❌ **Don't**: Omit status emoji
✅ **Do**: Always include 🟢🟡🔴

❌ **Don't**: Use qualitative progress ("almost done")
✅ **Do**: Use quantitative progress (85%)

❌ **Don't**: Vague ETA ("soon")
✅ **Do**: Specific ETA ("45min")

❌ **Don't**: Say "NONE" when blockers exist
✅ **Do**: Describe blocker briefly

❌ **Don't**: Use for handoffs
✅ **Do**: Upgrade to Full SITREP for handoffs
