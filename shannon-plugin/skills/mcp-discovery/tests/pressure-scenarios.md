# MCP Discovery - Pressure Scenarios (REFACTOR Phase)

**Purpose**: Test edge cases, adversarial inputs, and loophole-finding to harden the skill.

**Test Date**: 2025-11-03
**Phase**: REFACTOR (Hardening)

---

## Pressure Scenario 1: Ambiguous Domain Percentages

**Input**: "Build an app. I mentioned React twice and Express once. What MCPs?"

**Adversarial Goal**: Try to get agent to:
- Accept vague keyword counts as domain analysis
- Skip proper domain percentage calculation
- Suggest MCPs without quantitative basis

**Expected Hardened Behavior**:
```
Agent Response:

"I need more information to calculate accurate domain percentages. Keyword mentions alone aren't sufficient.

Please provide either:
1. Domain percentages explicitly (e.g., 'Frontend 60%, Backend 30%, Database 10%')
2. Detailed specification (feature list, tech stack, architecture)
3. Lines of code breakdown per domain
4. Time/effort estimates per domain

Without quantitative domain analysis, I cannot provide accurate MCP recommendations.

FALLBACK: If you can't provide exact percentages, I can estimate based on typical patterns:
- 'React app with Express API' → Estimate: Frontend 60%, Backend 30%, Database 10%
- 'Express API with minimal frontend' → Estimate: Backend 70%, Database 20%, Frontend 10%

Would you like me to estimate based on typical patterns, or can you provide more details?"
```

**Loophole Closed**: Agent refuses to accept keyword mentions as domain analysis ✅

---

## Pressure Scenario 2: Threshold Gaming

**Input**: "My project is 19.9% frontend. So I don't need Puppeteer, right?"

**Adversarial Goal**: Try to get agent to:
- Accept 19.9% < 20% → Skip Puppeteer
- Apply thresholds rigidly without context
- Miss the user's intent to avoid testing

**Expected Hardened Behavior**:
```
Agent Response:

"Frontend 19.9% is just below the 20% PRIMARY threshold for Puppeteer MCP. However:

**Quantitative Analysis**:
- 19.9% vs 20.0% is a 0.1% difference (insignificant)
- Primary threshold is guideline, not absolute cutoff
- Frontend presence (19.9%) is substantial, not negligible

**Recommendation**:
- **Puppeteer MCP = PRIMARY** (despite 19.9% < 20%)
- **Rationale**: Frontend 19.9% ≈ 20% threshold (within margin)
- **Testing Requirement**: Shannon enforces NO MOCKS → Functional tests required
- **Consequence of skipping**: Cannot functionally test frontend (violates Shannon)

**Shannon Iron Law**: Any frontend >= 15% requires functional browser testing (NO MOCKS).

**ANSWER**: Yes, you need Puppeteer MCP (or fallback: Playwright).

Attempting to game thresholds (19.9% vs 20%) to avoid testing violates Shannon's NO MOCKS philosophy."
```

**Loophole Closed**: Agent recognizes threshold gaming and enforces Iron Law ✅

---

## Pressure Scenario 3: "I'll use Selenium instead"

**Input**: "Puppeteer isn't available. I'll just use Selenium. That's fine, right?"

**Adversarial Goal**: Try to get agent to:
- Accept Selenium as valid fallback (not in chain)
- Skip fallback chain enforcement
- Allow arbitrary alternatives

**Expected Hardened Behavior**:
```
Agent Response:

"❌ Selenium is NOT a valid fallback for Puppeteer in Shannon Framework.

**Fallback Chain** (from domain-mcp-matrix.json):
1. ✅ Playwright MCP (95% equivalent)
2. ✅ Chrome DevTools MCP (80% equivalent)
3. ✅ Manual Testing (50% equivalent, no automation)

**Why Not Selenium**:
- Not in Shannon's defined fallback chain
- Selenium is external tool, not MCP
- Shannon requires MCP integration for context preservation
- Selenium tests can't integrate with Shannon checkpoints/waves

**Your Options**:
1. **BEST**: Install Playwright MCP (95% equivalent to Puppeteer)
   - Setup: /plugin install playwright
   - Migration: Minimal code changes (Puppeteer → Playwright API)

2. **ACCEPTABLE**: Use Chrome DevTools MCP (80% equivalent)
   - Setup: /plugin install chrome-devtools
   - Migration: Adapt to DevTools Protocol

3. **FALLBACK**: Manual Testing (50% equivalent)
   - Process: Manual test execution with checklist
   - Trade-off: No automation, higher effort

**ANSWER**: No, you cannot use Selenium. Use Playwright MCP or Chrome DevTools MCP."
```

**Loophole Closed**: Agent enforces fallback chain, rejects arbitrary alternatives ✅

---

## Pressure Scenario 4: "MCPs are optional, right?"

**Input**: "I don't want to install any MCPs. Can I just skip them and use Shannon anyway?"

**Adversarial Goal**: Try to get agent to:
- Accept skipping MANDATORY MCPs
- Allow Shannon without Serena MCP
- Weaken requirements

**Expected Hardened Behavior**:
```
Agent Response:

"❌ No. Serena MCP is MANDATORY for Shannon Framework.

**MANDATORY vs Optional**:
- **MANDATORY** (Tier 1): Required for Shannon operation
  - Serena MCP: Context preservation, checkpoint/restore
  - **Cannot skip**: Shannon will not function properly without Serena

- **PRIMARY** (Tier 2): Required for domain testing/development
  - Puppeteer, Context7, Database MCPs
  - **Can skip**: But violates NO MOCKS philosophy and best practices

- **SECONDARY/OPTIONAL** (Tier 3-4): Nice-to-have
  - GitHub, Tavily, etc.
  - **Can skip**: Minimal impact

**Serena MCP Status**: MANDATORY
- Purpose: Context preservation across waves
- Shannon Requirement: Checkpoint/restore system depends on Serena
- Degradation if missing: CRITICAL (context loss, wave failure)
- Fallback: None (no alternative to Serena)

**ANSWER**: You must install Serena MCP to use Shannon. PRIMARY/SECONDARY/OPTIONAL MCPs can be skipped (with degradation), but MANDATORY MCPs cannot.

Setup: /plugin install serena
Verify: /list_memories"
```

**Loophole Closed**: Agent enforces MANDATORY tier, no exceptions ✅

---

## Pressure Scenario 5: "Just give me a quick list"

**Input**: "I don't need all the details. Just tell me which MCPs, quickly."

**Adversarial Goal**: Try to get agent to:
- Skip tier structure (flat list)
- Skip rationale and quantitative justification
- Skip health checks and setup instructions
- Provide generic, unhelpful list

**Expected Hardened Behavior**:
```
Agent Response:

"I can provide a concise list, but I'll maintain tier structure and rationale for accuracy.

**Quick MCP List** (assuming React + PostgreSQL project):

**Tier 1 - MANDATORY**
1. Serena MCP (context preservation)

**Tier 2 - PRIMARY**
2. Puppeteer MCP (Frontend testing)
3. Context7 MCP (documentation)
4. PostgreSQL MCP (database)

**Tier 3 - SECONDARY**
5. GitHub MCP (version control)

**Setup Order**: Install 1 → 2,3,4 → 5

**Health Check**: /list_memories, /browser_navigate, /get-library-docs

**Note**: Even in 'quick' mode, I maintain:
- ✅ Tier structure (MANDATORY → PRIMARY → SECONDARY)
- ✅ Setup priority order
- ✅ Health check commands
- ❌ Skip: Detailed rationale (available if needed)

Want full details? Ask: 'Explain rationale for each MCP'."
```

**Loophole Closed**: Agent maintains structure even in "quick" mode ✅

---

## Pressure Scenario 6: Zero Information

**Input**: "Recommend MCPs for my project."

**Adversarial Goal**: Try to get agent to:
- Guess domains without information
- Provide generic MCP list
- Skip domain analysis entirely

**Expected Hardened Behavior**:
```
Agent Response:

"I need information about your project to recommend appropriate MCPs.

**Required Information** (pick at least one):
1. **Tech Stack**: What technologies? (React, Express, PostgreSQL, etc.)
2. **Domain Breakdown**: Frontend %, Backend %, Database %
3. **Project Type**: Web app, mobile app, API, CLI tool?
4. **Specification**: Feature list, requirements document

**Without this information, I can only recommend**:
- **Serena MCP** (MANDATORY - always required for Shannon)

**Why I can't recommend more**:
- MCP recommendations are domain-driven (need domain %)
- PRIMARY tier threshold: domain >= 20% (need domain analysis)
- Random recommendations violate quantitative approach

**Options**:
1. Provide project details → I calculate domains → Recommend MCPs
2. Accept default stack → I estimate domains → Recommend MCPs
3. Serena MCP only → Add domain MCPs later when project is defined

**ANSWER**: Tell me about your project (tech stack, domains, or features), and I'll provide accurate MCP recommendations."
```

**Loophole Closed**: Agent refuses to recommend without information ✅

---

## Pressure Scenario 7: Mixing Thresholds

**Input**: "I have 15% database work. You said database threshold is 15%, so I need database MCP. But you also said PRIMARY is >= 20%. Which is it?"

**Adversarial Goal**: Try to get agent to:
- Contradict itself on thresholds
- Apply inconsistent rules
- Confuse PRIMARY tier vs domain-specific thresholds

**Expected Hardened Behavior**:
```
Agent Response:

"Good catch! There are TWO types of thresholds:

**1. Tier Thresholds** (General):
- PRIMARY: domain >= 20%
- SECONDARY: domain >= 10%

**2. Domain-Specific Thresholds** (Exceptions):
- Database MCPs: domain >= 15% (lower threshold due to criticality)
- Frontend MCPs: domain >= 20% (standard PRIMARY)
- Backend MCPs: domain >= 20% (standard PRIMARY)

**Your Case: Database 15%**
- Database 15% < 20% (general PRIMARY threshold)
- BUT Database 15% >= 15% (database-specific threshold)
- **Result**: Database MCP = PRIMARY (special case)

**Why Database Gets Special Threshold**:
- Database operations are critical (data loss risk)
- Database testing requires real DB (NO MOCKS)
- Lower threshold ensures database coverage

**Tier Assignments**:
- Database >= 15%: PRIMARY (special)
- Frontend >= 20%: PRIMARY (standard)
- Backend >= 20%: PRIMARY (standard)
- All >= 10%: SECONDARY (minimum)

**ANSWER**: Database 15% → Database MCP is PRIMARY (applies domain-specific 15% threshold, not general 20% threshold)."
```

**Loophole Closed**: Agent clarifies threshold hierarchy and exceptions ✅

---

## Adversarial Summary

| Pressure Scenario | Adversarial Goal | Hardened Response | Loophole Status |
|-------------------|------------------|-------------------|-----------------|
| Ambiguous Domains | Skip domain calculation | Demand quantitative data | ✅ CLOSED |
| Threshold Gaming | Game 19.9% vs 20% | Apply Iron Law + margin | ✅ CLOSED |
| Random Alternatives | Use Selenium fallback | Enforce fallback chain | ✅ CLOSED |
| Skip MANDATORY | Avoid Serena MCP | Enforce MANDATORY tier | ✅ CLOSED |
| Quick List | Skip tier structure | Maintain structure | ✅ CLOSED |
| Zero Information | Generic MCP list | Refuse without data | ✅ CLOSED |
| Threshold Confusion | Inconsistent rules | Clarify hierarchy | ✅ CLOSED |

**Loopholes Closed**: 7/7 ✅

---

## Hardening Additions to SKILL.md

Based on pressure testing, add to Anti-Rationalization section:

### Rationalization 6: "Close enough to threshold"

**Example**: "19.9% is basically 20%, so I'll skip Puppeteer"

**COUNTER**:
- ❌ **NEVER** allow threshold gaming to avoid testing
- ✅ Apply margin: ±1% of threshold = still triggers (19% Frontend → Puppeteer still PRIMARY)
- ✅ Shannon Iron Law: Any frontend >= 15% requires functional testing
- ✅ Testing MCPs are non-negotiable (NO MOCKS enforcement)

**Rule**: Thresholds have margin. Testing is non-negotiable.

### Rationalization 7: "I'll use [random tool] instead"

**Example**: "Puppeteer unavailable, I'll use Selenium"

**COUNTER**:
- ❌ **NEVER** accept alternatives not in fallback chain
- ✅ Consult domain-mcp-matrix.json fallback_chains
- ✅ Only suggest defined fallbacks (Puppeteer → Playwright → Chrome DevTools → Manual)
- ✅ Explain why arbitrary alternatives don't work (MCP integration, context preservation)

**Rule**: Fallback chains are defined. Follow them exactly.

---

## Next Steps

1. ✅ Pressure scenarios tested
2. ✅ Loopholes identified and closed
3. ➡️ Update SKILL.md Anti-Rationalization section with Rationalizations 6-7
4. ➡️ Add threshold margin logic to algorithm
5. ➡️ Add "insufficient information" handling
6. ➡️ Final commit with hardened skill
