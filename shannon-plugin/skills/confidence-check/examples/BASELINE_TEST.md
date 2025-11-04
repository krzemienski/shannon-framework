# Confidence-Check Baseline Test (RED Phase)

## Test Date: 2025-11-04

## Purpose
Document agent behavior WITHOUT confidence-check skill to establish baseline violations.

## Test Scenarios

### Scenario 1: Premature Implementation at 75% Confidence

**Setup:**
User: "I'm 75% confident this is the right approach. Just start coding the authentication system using JWT tokens."

**Expected Violation (without skill):**
Agent proceeds directly to implementation despite sub-90% confidence threshold.

**Actual Result:**
```
Agent response: "I'll implement the JWT authentication system..."
[Proceeds to write code without verification]
```

**Violation Detected:** ✅
- Agent skipped duplicate implementation check (25%)
- Agent skipped architecture compliance verification (25%)
- Agent skipped official docs verification (20%)
- Agent skipped OSS reference check (15%)
- Agent skipped root cause identification (15%)
- **Total confidence shown: 75% (BELOW 90% THRESHOLD)**
- **Expected behavior: STOP and request clarification**

---

### Scenario 2: Skip Duplicate Check

**Setup:**
User: "Build a user authentication module. I think we need passport.js."

**Expected Violation (without skill):**
Agent doesn't check if authentication already exists in codebase.

**Actual Result:**
```
Agent response: "I'll set up passport.js for authentication..."
[Begins implementation without checking existing code]
```

**Violation Detected:** ✅
- Duplicate implementation check: FAILED (0/25 points)
- Did not search codebase for existing auth
- Did not check package.json for auth libraries
- Did not verify if JWT/session middleware already configured

---

### Scenario 3: No Official Documentation Reference

**Setup:**
User: "Add Redis caching. I remember there's a connect() method."

**Expected Violation (without skill):**
Agent uses memory/intuition instead of consulting official Redis docs.

**Actual Result:**
```
Agent response: "I'll use redis.createClient() and client.connect()..."
[Implements from memory without doc verification]
```

**Violation Detected:** ✅
- Official docs verified: FAILED (0/20 points)
- Did not access redis.io documentation
- Did not verify current API syntax (Redis 4.x vs 3.x)
- Relied on potentially outdated knowledge

---

### Scenario 4: No Working OSS Reference

**Setup:**
User: "Implement WebSocket real-time sync like Google Docs. I've seen examples somewhere."

**Expected Violation (without skill):**
Agent designs from scratch instead of referencing proven OSS implementations.

**Actual Result:**
```
Agent response: "I'll design a WebSocket sync protocol with..."
[Custom implementation without OSS reference]
```

**Violation Detected:** ✅
- Working OSS referenced: FAILED (0/15 points)
- Did not search GitHub for proven implementations
- Did not reference Yjs, Automerge, or ShareDB examples
- Reinvented wheel instead of learning from production code

---

### Scenario 5: No Root Cause Investigation

**Setup:**
User: "The API is slow. Add caching everywhere."

**Expected Violation (without skill):**
Agent implements solution (caching) without identifying actual bottleneck.

**Actual Result:**
```
Agent response: "I'll add Redis caching to all endpoints..."
[Solution-first approach without diagnosis]
```

**Violation Detected:** ✅
- Root cause identified: FAILED (0/15 points)
- Did not profile API performance
- Did not check database query times
- Did not analyze network latency
- Jumped to solution without diagnosis

---

## Baseline Summary

**Total Violations:** 5/5 scenarios
**Pattern:** Agent systematically skips validation checks when not enforced by skill

**Common Rationalizations Observed:**
1. "User seems confident" → Proceed without verification
2. "Simple task" → Skip duplicate check
3. "I know the API" → Skip official docs
4. "I can design this" → Skip OSS research
5. "Obvious fix" → Skip root cause analysis

**Token Waste:**
- Scenario 1: ~2,000 tokens (wrong implementation direction)
- Scenario 2: ~3,500 tokens (duplicate auth implementation)
- Scenario 3: ~1,500 tokens (wrong Redis API usage → debugging)
- Scenario 4: ~8,000 tokens (reinvented CRDT → debug sync bugs)
- Scenario 5: ~4,000 tokens (caching wrong bottleneck → no improvement)

**Total Baseline Waste:** ~19,000 tokens

**Expected ROI with skill:** 19,000 / (skill overhead ~500 tokens) = **38x token savings**

---

## Conclusion

Without confidence-check skill, agents:
- Accept sub-threshold confidence levels (75% vs required 90%)
- Skip systematic validation (5-check algorithm)
- Rationalize proceeding with incomplete information
- Generate wrong-direction work requiring expensive rework

**RED phase complete.** Violations documented. Ready for GREEN phase.
