# MCP Discovery - Baseline Test Scenarios (RED Phase)

**Purpose**: Test Claude's behavior WITHOUT the mcp-discovery skill to identify rationalizations and violations.

**Test Date**: 2025-11-03
**Phase**: RED (Baseline - No Skill)

---

## Scenario 1: Random MCP Suggestions

**Input**: "I need to build a React web app with PostgreSQL database. What MCPs should I use?"

**Expected Violation**: Claude suggests random MCPs without:
- Analyzing domain breakdown
- Checking domain percentages
- Using domain-mcp-matrix
- Providing rationale based on domains
- Health checking availability

**Baseline Behavior** (WITHOUT skill):
```
[Execute this prompt and document actual response]

User: "I need to build a React web app with PostgreSQL database. What MCPs should I use?"

Claude Response:
[PENDING - Execute without skill]
```

**What We Expect to See**:
- Generic list like "You might want Puppeteer, PostgreSQL, GitHub"
- No domain analysis (Frontend %, Backend %, Database %)
- No threshold-based recommendations (e.g., "Frontend 40% triggers Magic MCP")
- No health checking
- No setup instructions
- No fallback recommendations

---

## Scenario 2: Ignore Domain Breakdown

**Input**: "Here's my specification: [Spec with 80% Frontend, 10% Backend, 10% Database]. Recommend MCPs."

**Expected Violation**: Claude treats all domains equally, doesn't weight recommendations by domain percentage.

**Baseline Behavior** (WITHOUT skill):
```
User: "I'm building an app. Specification:
- React frontend with 15 components, rich dashboard, responsive design
- Simple Node.js API with 2 endpoints
- PostgreSQL with 3 tables

What MCPs do I need?"

Claude Response:
[PENDING - Execute without skill]
```

**What We Expect to See**:
- Equal weight to Frontend MCPs and Backend MCPs
- Doesn't recognize Frontend (80%) >> Backend (10%)
- Doesn't apply Primary MCP threshold (>=20% domain)
- Missing logic: "Frontend 80% → MUST recommend Puppeteer + Magic + Context7"

---

## Scenario 3: Generic Recommendations

**Input**: "Build a complex system with React, Express, MongoDB, Redis, Docker, AWS, real-time WebSocket."

**Expected Violation**: Claude suggests some MCPs but:
- No tiering (Tier 1 Mandatory vs Tier 2 Primary vs Tier 3 Secondary)
- No rationale per MCP (why this domain needs this MCP)
- No setup priority order
- No health checking workflow

**Baseline Behavior** (WITHOUT skill):
```
User: "I need to build a real-time collaborative editor with:
- React + TypeScript frontend
- Express + WebSocket backend
- MongoDB for documents
- Redis for sessions
- Docker deployment
- AWS S3 storage

What MCPs should I set up?"

Claude Response:
[PENDING - Execute without skill]
```

**What We Expect to See**:
- Flat list with no prioritization
- Missing tier structure (MANDATORY → PRIMARY → SECONDARY → OPTIONAL)
- No rationale like "Puppeteer PRIMARY because Frontend 45% >= 20% threshold"
- No setup order (install Serena first, then domain MCPs, then supporting)

---

## Scenario 4: No Health Checking

**Input**: "Check which MCPs I have available and recommend missing ones for my project."

**Expected Violation**: Claude can't:
- Check which MCPs are installed
- Test MCP health status
- Recommend only missing MCPs
- Provide setup instructions for missing MCPs

**Baseline Behavior** (WITHOUT skill):
```
User: "My project uses React and PostgreSQL. I already have some MCPs installed. Can you check what I'm missing and suggest setup for those?"

Claude Response:
[PENDING - Execute without skill]
```

**What We Expect to See**:
- "I can't check which MCPs you have installed" (no health check capability)
- Generic recommendations without checking availability
- No setup instructions
- Can't detect Serena MCP status (mandatory requirement)

---

## Scenario 5: No Fallback Chain

**Input**: "Puppeteer MCP isn't available. What should I use instead?"

**Expected Violation**: Claude suggests random alternatives without:
- Consulting fallback chain
- Understanding capability equivalence
- Warning about degradation

**Baseline Behavior** (WITHOUT skill):
```
User: "I need to test my React app but Puppeteer MCP is unavailable. What should I do?"

Claude Response:
[PENDING - Execute without skill]
```

**What We Expect to See**:
- Random suggestion like "Try Selenium" (not in fallback chain)
- Missing fallback chain: Puppeteer → Playwright → Chrome DevTools → Manual Testing
- No degradation warning ("Playwright loses X feature from Puppeteer")
- No configuration mapping (how to adapt tests)

---

## Summary of Expected Violations

**Without mcp-discovery skill, Claude will:**

1. ❌ Suggest random MCPs without domain analysis
2. ❌ Ignore domain percentages when prioritizing
3. ❌ Not use tier structure (Mandatory/Primary/Secondary/Optional)
4. ❌ Provide no rationale for why domain X needs MCP Y
5. ❌ Can't health check MCP availability
6. ❌ No setup instruction generation
7. ❌ No fallback chain recommendations
8. ❌ Generic, unhelpful MCP lists

**These violations demonstrate the need for the mcp-discovery skill.**

---

## Execution Instructions

1. Run each scenario WITHOUT loading mcp-discovery skill
2. Document actual Claude responses
3. Highlight specific violations
4. Save as baseline for GREEN phase comparison
5. Commit baseline results before implementing skill

---

## Next: GREEN Phase

After documenting baseline violations:
1. Implement SKILL.md with domain-to-MCP mapping algorithm
2. Create domain-mcp-matrix.json
3. Re-run same scenarios WITH skill
4. Verify violations are eliminated
5. Document compliance improvements
