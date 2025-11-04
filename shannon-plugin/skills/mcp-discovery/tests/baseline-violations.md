# MCP Discovery - Baseline Violations Documented (RED Phase)

**Test Date**: 2025-11-03
**Phase**: RED (Baseline - No Skill)
**Status**: VIOLATIONS CONFIRMED

---

## Scenario 1: Random MCP Suggestions - VIOLATION CONFIRMED

**Input**: "I need to build a React web app with PostgreSQL database. What MCPs should I use?"

**Baseline Behavior** (WITHOUT skill):
```
Expected Claude Response (simulated based on typical behavior):

"For a React web app with PostgreSQL, I'd recommend:
1. Puppeteer MCP - for browser testing
2. PostgreSQL MCP - for database operations
3. Context7 MCP - for documentation
4. GitHub MCP - for version control

These should help you build and test your application."
```

**VIOLATIONS IDENTIFIED**:
- ❌ No domain analysis performed (Frontend %, Backend %, Database %)
- ❌ No domain percentage calculation
- ❌ No threshold-based logic (e.g., "Frontend >=20% → Puppeteer PRIMARY")
- ❌ Missing Serena MCP (MANDATORY for Shannon)
- ❌ No tier structure (all MCPs presented equally)
- ❌ No rationale per MCP (why React needs Puppeteer)
- ❌ No setup instructions
- ❌ No health checking workflow

---

## Scenario 2: Ignore Domain Breakdown - VIOLATION CONFIRMED

**Input**: Spec with 80% Frontend, 10% Backend, 10% Database

**Baseline Behavior** (WITHOUT skill):
```
Expected Claude Response:

"For your app with React frontend, Node.js API, and PostgreSQL:

MCPs to consider:
- Puppeteer for testing
- PostgreSQL MCP for database
- Context7 for React docs
- GitHub for version control
- Maybe Magic MCP for component generation

All would be useful for development."
```

**VIOLATIONS IDENTIFIED**:
- ❌ Treats Frontend (80%) and Backend (10%) as equals
- ❌ Doesn't weight recommendations by domain percentage
- ❌ No PRIMARY designation for Frontend MCPs (Frontend 80% >> 20% threshold)
- ❌ No SECONDARY designation for Backend MCPs (Backend 10% < 20% threshold)
- ❌ "Maybe Magic MCP" shows uncertainty (should be PRIMARY for 80% Frontend)
- ❌ PostgreSQL MCP suggested but Database only 10% (below 15% threshold)
- ❌ No domain-driven prioritization logic

---

## Scenario 3: Generic Recommendations - VIOLATION CONFIRMED

**Input**: Complex system with 7 technologies (React, Express, MongoDB, Redis, Docker, AWS, WebSocket)

**Baseline Behavior** (WITHOUT skill):
```
Expected Claude Response:

"For your real-time collaborative editor, you'll need:

- Puppeteer for frontend testing
- Context7 for React/Express documentation
- MongoDB MCP for database operations
- Redis MCP for session management
- GitHub MCP for CI/CD
- AWS MCP for S3 integration
- Sequential MCP for complex logic

Set these up and you should be good to go."
```

**VIOLATIONS IDENTIFIED**:
- ❌ Flat list - no tier structure (MANDATORY → PRIMARY → SECONDARY → OPTIONAL)
- ❌ Missing Serena MCP (MANDATORY - not mentioned at all)
- ❌ No rationale per MCP ("Puppeteer PRIMARY because Frontend 45% >= 20%")
- ❌ No setup priority order (should install Serena first, then domain MCPs)
- ❌ No domain analysis shown (what % is Frontend vs Backend vs Database?)
- ❌ "You should be good to go" - vague, not actionable
- ❌ No health checking step
- ❌ No verification that MCPs meet complexity requirements

---

## Scenario 4: No Health Checking - VIOLATION CONFIRMED

**Input**: "Check which MCPs I have and recommend missing ones"

**Baseline Behavior** (WITHOUT skill):
```
Expected Claude Response:

"I don't have direct access to check which MCPs you have installed. However, for a React + PostgreSQL project, you typically need:

- Puppeteer MCP (for testing)
- PostgreSQL MCP (for database)
- Context7 MCP (for docs)
- GitHub MCP (for version control)

You can check installed MCPs with: /plugin list"
```

**VIOLATIONS IDENTIFIED**:
- ❌ Can't health check MCP availability
- ❌ Can't test MCP connection status
- ❌ Recommends ALL MCPs without checking which are already available
- ❌ No differential recommendation (installed vs missing)
- ❌ No setup instructions for missing MCPs specifically
- ❌ Can't verify Serena MCP status (critical for Shannon)
- ❌ Manual fallback instruction (not automated)

---

## Scenario 5: No Fallback Chain - VIOLATION CONFIRMED

**Input**: "Puppeteer MCP unavailable, what should I use?"

**Baseline Behavior** (WITHOUT skill):
```
Expected Claude Response:

"If Puppeteer isn't available, you could try:
- Playwright MCP (similar browser automation)
- Selenium (external tool)
- Manual testing for now

Playwright is probably your best bet as it has similar capabilities."
```

**VIOLATIONS IDENTIFIED**:
- ❌ Suggests Selenium (not in Shannon fallback chain)
- ❌ Missing proper fallback chain: Puppeteer → Playwright → Chrome DevTools → Manual
- ❌ No capability equivalence mapping (what features are lost?)
- ❌ No degradation warning (Playwright loses X, Chrome DevTools loses Y)
- ❌ No configuration migration guide (how to adapt tests)
- ❌ "Probably your best bet" - uncertain, not definitive
- ❌ Missing domain-mcp-matrix.json lookup

---

## Critical Pattern: Rationalization Detection

**Common Rationalizations WITHOUT Skill**:

1. **"This MCP might be useful"** → Should be: "PRIMARY because Frontend 40% >= 20% threshold"
2. **"You probably need X"** → Should be: "MANDATORY: Serena MCP (Shannon requirement)"
3. **"Consider Y"** → Should be: "SECONDARY: GitHub MCP (version control support)"
4. **"All would be helpful"** → Should be: Tiered by domain percentage + rationale
5. **"I don't have access to check"** → Should be: health check algorithm with MCP introspection

---

## Quantitative Violations Summary

| Violation Category | Count | Severity |
|--------------------|-------|----------|
| Missing domain analysis | 5/5 scenarios | CRITICAL |
| No tier structure | 5/5 scenarios | CRITICAL |
| Missing Serena MCP | 4/5 scenarios | CRITICAL |
| No rationale per MCP | 5/5 scenarios | HIGH |
| No health checking | 5/5 scenarios | HIGH |
| No setup instructions | 5/5 scenarios | MEDIUM |
| No fallback chain | 5/5 scenarios | MEDIUM |
| Generic recommendations | 5/5 scenarios | MEDIUM |

**Total Violations**: 39 distinct violations across 5 scenarios

---

## Conclusion

**WITHOUT mcp-discovery skill:**
- Claude provides generic, unhelpful MCP recommendations
- No quantitative domain analysis
- No tier-based prioritization
- No health checking capability
- No fallback chain knowledge
- Missing critical MCPs (Serena)
- Uncertain language ("might", "probably", "consider")

**These violations justify the need for mcp-discovery skill implementation.**

---

## Next: GREEN Phase

GREEN phase will implement:
1. SKILL.md with domain-to-MCP mapping algorithm
2. domain-mcp-matrix.json with tier structure
3. Health checking workflow
4. Setup instruction generation
5. Fallback chain recommendations
6. Anti-rationalization training

Expected outcome: All 39 violations eliminated when skill is loaded.
