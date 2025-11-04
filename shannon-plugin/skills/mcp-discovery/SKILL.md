---
name: mcp-discovery
description: |
  Intelligent MCP server recommendation engine based on quantitative domain analysis. Maps project
  domains (Frontend %, Backend %, Database %, etc.) to appropriate MCP servers using tier-based
  priority system (Mandatory > Primary > Secondary > Optional). Performs health checking, generates
  setup instructions, provides fallback chains. Use when: analyzing project needs, configuring MCPs,
  checking MCP health, recommending alternatives.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      purpose: Always mandatory for Shannon Framework
      fallback: none
      degradation: critical

required-by:
  - spec-analysis
  - phase-planning

allowed-tools: Read, Serena
---

# MCP Discovery - Intelligent MCP Recommendation Engine

## Overview

**Purpose**: Provide quantitative, domain-driven MCP server recommendations using tier-based prioritization. Transform domain percentages (from spec-analysis) into actionable MCP setup strategies with health checking, fallback chains, and setup instructions.

**Key Innovation**: Only framework with quantitative domain-to-MCP mapping (not guesswork).

---

## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically rationalize vague MCP recommendations without structured analysis. Below are the 5 most common rationalizations detected in baseline testing, with mandatory counters.

### Rationalization 1: "You might want these MCPs..."

**Example**: User asks for MCPs → Agent responds "You might want Puppeteer, PostgreSQL, GitHub..."

**COUNTER**:
- ❌ **NEVER** suggest MCPs with uncertain language ("might", "probably", "consider")
- ✅ Use quantitative thresholds: "Frontend 40% >= 20% → Puppeteer is PRIMARY"
- ✅ Every MCP has tier designation (MANDATORY, PRIMARY, SECONDARY, OPTIONAL)
- ✅ Every recommendation includes rationale based on domain percentage

**Rule**: No uncertain recommendations. State tier + rationale explicitly.

### Rationalization 2: "All would be helpful"

**Example**: Agent lists 8 MCPs and says "All of these would be helpful for your project"

**COUNTER**:
- ❌ **NEVER** treat all MCPs as equally important
- ✅ Apply tier structure from domain-mcp-matrix.json
- ✅ Serena MCP = MANDATORY (always first)
- ✅ Domain MCPs = PRIMARY (domain >= 20%) or SECONDARY (domain >= 10%)
- ✅ Support MCPs = SECONDARY/OPTIONAL

**Rule**: Tier ALL recommendations. No flat lists.

### Rationalization 3: "I don't have access to check MCPs"

**Example**: User asks "What MCPs am I missing?" → Agent says "I can't check what you have installed"

**COUNTER**:
- ❌ **NEVER** skip health checking workflow
- ✅ Provide health check commands for each MCP
- ✅ Guide user through health check process
- ✅ Generate differential recommendations (installed vs missing)
- ✅ Prioritize missing MANDATORY and PRIMARY MCPs

**Rule**: Always include health check workflow. No helpless responses.

### Rationalization 4: "Try Selenium as alternative"

**Example**: User says "Puppeteer unavailable" → Agent suggests "Try Selenium" (not in fallback chain)

**COUNTER**:
- ❌ **NEVER** suggest random alternatives without consulting fallback chains
- ✅ Use domain-mcp-matrix.json fallback chains
- ✅ Puppeteer fallback: Playwright → Chrome DevTools → Manual Testing (in order)
- ✅ Explain capability degradation for each fallback
- ✅ Provide configuration migration guidance

**Rule**: Fallback chains are defined. Follow them exactly.

### Rationalization 5: "No domain analysis needed"

**Example**: User mentions "React app" → Agent immediately suggests MCPs without calculating domain %

**COUNTER**:
- ❌ **NEVER** skip domain percentage analysis
- ✅ Calculate domain breakdown (Frontend %, Backend %, Database %)
- ✅ Apply thresholds: Primary (>=20%), Secondary (>=10%)
- ✅ Map domains to MCPs using domain-mcp-matrix.json
- ✅ Show quantitative reasoning: "Frontend 45% >= 20% threshold → Puppeteer PRIMARY"

**Rule**: Domain percentages drive ALL recommendations. Always calculate first.

---

## Core Competencies

### 1. Domain-to-MCP Mapping Algorithm

**Input**: Domain percentages from spec-analysis or direct domain counts

**Algorithm**:
```
1. Load domain-mcp-matrix.json
2. FOR EACH domain WITH percentage >= 5%:
   a. IF domain >= 20% → Add domain PRIMARY MCPs
   b. IF domain >= 10% AND domain < 20% → Add domain SECONDARY MCPs
   c. Check keyword conditions (e.g., "React" + Frontend >= 30% → Magic MCP)
3. ALWAYS add MANDATORY MCPs (Serena)
4. Add universal SECONDARY MCPs (GitHub)
5. Check keywords for OPTIONAL MCPs (research → Tavily)
6. Sort by tier priority: MANDATORY → PRIMARY → SECONDARY → OPTIONAL
7. Within each tier, sort by setup_priority
```

**Output**: Tiered MCP list with rationale per MCP

### 2. Health Check System

**Algorithm**:
```
1. FOR EACH recommended MCP:
   a. Look up health_check command from domain-mcp-matrix.json
   b. Generate test instruction: "Test with: /[health_check_command]"
   c. Expected success: "✅ MCP operational"
   d. Expected failure: "❌ MCP not available → Use fallback"
2. Generate health check script:
   - Test MANDATORY MCPs first (critical)
   - Test PRIMARY MCPs second (high priority)
   - Test SECONDARY/OPTIONAL last
3. Report status per MCP: Operational / Missing / Degraded
```

**Output**: Health check workflow + MCP status report

### 3. Fallback Chain Resolution

**Input**: Unavailable MCP name

**Algorithm**:
```
1. Look up MCP in domain-mcp-matrix.json fallback_chains
2. IF fallback chain exists:
   a. Return ordered list: [fallback1, fallback2, ..., manual]
   b. FOR EACH fallback, explain capability differences
   c. Provide migration instructions (e.g., Puppeteer → Playwright code changes)
3. IF no fallback chain:
   a. Return "No direct replacement"
   b. Suggest alternative approach (e.g., manual testing)
```

**Output**: Ordered fallback chain + migration guide

### 4. Setup Instruction Generation

**Algorithm**:
```
1. FOR EACH recommended MCP:
   a. Generate setup command: "Install [MCP] via Claude Code plugin system"
   b. Generate health check: "Verify with: /[health_check_command]"
   c. Generate configuration: "[MCP]-specific settings if needed"
   d. Generate validation: "Test with sample operation"
2. Order by setup_priority (MANDATORY first, then by tier)
3. Generate complete setup script
```

**Output**: Step-by-step setup guide with validation

---

## Workflow

### Mode 1: Recommend MCPs (from domain percentages)

**Input**: Domain percentages (e.g., `{frontend: 40%, backend: 30%, database: 20%}`)

**Steps**:
1. Load domain-mcp-matrix.json
2. Apply domain-to-MCP mapping algorithm
3. Generate tiered recommendations:
   - Tier 1 MANDATORY: Serena MCP (always)
   - Tier 2 PRIMARY: Puppeteer (Frontend 40% >= 20%), Context7 (Backend 30% >= 20%)
   - Tier 3 SECONDARY: PostgreSQL MCP (Database 20% >= 15%), GitHub MCP (universal)
4. Generate rationale per MCP
5. Generate health check workflow
6. Generate setup instructions

**Output**: Tiered MCP list with rationale, health checks, setup guide

### Mode 2: Health Check Existing MCPs

**Input**: User request to check MCP status

**Steps**:
1. List recommended MCPs from domain analysis
2. Generate health check commands per MCP
3. Guide user through testing:
   - "Test Serena: /list_memories → Expected: memory list"
   - "Test Puppeteer: /browser_navigate → Expected: browser launches"
4. Collect results: Operational / Missing / Degraded
5. Report status summary
6. Recommend setup for missing MANDATORY/PRIMARY MCPs

**Output**: MCP health status report + setup guide for missing MCPs

### Mode 3: Fallback Recommendations

**Input**: Unavailable MCP name + reason

**Steps**:
1. Look up fallback chain in domain-mcp-matrix.json
2. Return ordered fallbacks with capability comparison
3. Provide migration guide for code changes
4. Explain degradation per fallback level

**Output**: Fallback chain + migration guide + degradation warnings

---

## Examples

### Example 1: Frontend-Heavy Project (Frontend 60%, Backend 20%, Database 20%)

**Input**:
```
User: "My project is 60% frontend (React), 20% backend (Express), 20% database (PostgreSQL). What MCPs should I use?"
```

**Execution**:
```
Step 1: Load domain-mcp-matrix.json
Step 2: Apply mapping algorithm:
  - Frontend 60% >= 20% → PRIMARY: Puppeteer, Magic (60% >= 30%), Context7
  - Backend 20% >= 20% → PRIMARY: Context7 (already added)
  - Database 20% >= 15% → PRIMARY: PostgreSQL MCP
  - MANDATORY: Serena MCP (always)
  - SECONDARY: GitHub MCP (universal)
Step 3: Sort by tier and priority
```

**Output**:
```markdown
# MCP Recommendations

## Tier 1: MANDATORY
1. **Serena MCP** (Setup Priority: 1)
   - Purpose: Context preservation across waves
   - Rationale: Shannon Framework requirement
   - Setup: Install via /plugin install serena
   - Health Check: /list_memories
   - Fallback: None (critical requirement)

## Tier 2: PRIMARY
2. **Puppeteer MCP** (Frontend 60% >= 20%)
   - Purpose: Functional browser testing (NO MOCKS)
   - Rationale: Frontend 60% >= 20% threshold for Primary tier
   - Setup: Install via /plugin install puppeteer
   - Health Check: /browser_navigate
   - Fallback Chain: Playwright → Chrome DevTools → Manual Testing

3. **Magic MCP** (Frontend 60% >= 30%)
   - Purpose: Component generation for React
   - Rationale: Frontend 60% >= 30% threshold for Magic MCP
   - Setup: Install via /plugin install magic
   - Health Check: /21st_magic_component_builder
   - Fallback Chain: Manual coding

4. **Context7 MCP** (Frontend 60% + Backend 20%)
   - Purpose: Framework documentation (React, Express)
   - Rationale: Multiple domains >= 20% benefit from Context7
   - Setup: Install via /plugin install context7
   - Health Check: /get-library-docs
   - Fallback Chain: Web search → Manual docs

5. **PostgreSQL MCP** (Database 20% >= 15%)
   - Purpose: PostgreSQL database operations
   - Rationale: Database 20% >= 15% threshold for database MCPs
   - Setup: Install via /plugin install postgres
   - Health Check: Database connection test
   - Fallback Chain: Manual psql → Database GUI

## Tier 3: SECONDARY
6. **GitHub MCP** (Universal)
   - Purpose: Version control, CI/CD, project management
   - Rationale: All projects benefit from GitHub integration
   - Setup: Install via /plugin install github
   - Health Check: /list repositories
   - Fallback Chain: Manual git → gh CLI

## Setup Order
1. Install Serena MCP first (MANDATORY)
2. Verify Serena: /list_memories
3. Install Primary MCPs: Puppeteer, Magic, Context7, PostgreSQL
4. Verify each Primary MCP with health check
5. Install Secondary MCPs: GitHub
6. Run full health check workflow

## Health Check Workflow
```bash
# Test MANDATORY
/list_memories
# Expected: ✅ Memory list returned

# Test PRIMARY
/browser_navigate https://example.com
# Expected: ✅ Browser launches

/21st_magic_component_builder
# Expected: ✅ Component generation available

/get-library-docs react
# Expected: ✅ React documentation retrieved

# Test database connection (requires DB setup)
# Expected: ✅ Connection established

# Test SECONDARY
/list repositories
# Expected: ✅ GitHub repositories listed
```

## Next Steps
1. Follow setup order above
2. Run health check workflow
3. If any PRIMARY MCP fails, consult fallback chain
4. Verify all MANDATORY MCPs operational before proceeding
```

### Example 2: Backend-Heavy Project (Backend 70%, Database 25%, Frontend 5%)

**Input**:
```
User: "I'm building a backend API: 70% Express/FastAPI, 25% PostgreSQL, 5% minimal frontend. Recommend MCPs."
```

**Execution**:
```
Step 1: Domain analysis:
  - Backend 70% >= 20% → PRIMARY tier
  - Database 25% >= 15% → PRIMARY tier
  - Frontend 5% < 10% → SKIP (below threshold)
Step 2: Map domains to MCPs:
  - Backend 70% → Context7 PRIMARY
  - Database 25% → PostgreSQL MCP PRIMARY
  - MANDATORY: Serena
Step 3: Frontend 5% → No frontend MCPs (below threshold)
```

**Output**:
```markdown
# MCP Recommendations

## Tier 1: MANDATORY
1. **Serena MCP** - Context preservation (Shannon requirement)

## Tier 2: PRIMARY
2. **Context7 MCP** (Backend 70% >= 20%)
   - Purpose: Express/FastAPI documentation
   - Rationale: Backend-heavy project needs framework references

3. **PostgreSQL MCP** (Database 25% >= 15%)
   - Purpose: PostgreSQL database operations
   - Rationale: Database 25% >= 15% threshold

## Tier 3: SECONDARY
4. **GitHub MCP** (Universal)
   - Purpose: Version control, CI/CD

## Notes
- Frontend 5% < 10% threshold → No frontend MCPs recommended
- Focus on backend tooling (Context7) and database access (PostgreSQL)
- If frontend grows to >= 20%, add Puppeteer for testing
```

### Example 3: Health Check Request

**Input**:
```
User: "Can you check which MCPs I have and tell me what's missing for my React + PostgreSQL project?"
```

**Execution**:
```
Step 1: Calculate expected MCPs:
  - React → Frontend domain (assume 50%)
  - PostgreSQL → Database domain (assume 25%)
  - Remaining → Backend (25%)
Step 2: Expected MCPs:
  - MANDATORY: Serena
  - PRIMARY: Puppeteer (Frontend 50%), Context7, PostgreSQL MCP
  - SECONDARY: GitHub
Step 3: Generate health check workflow
Step 4: Guide user through testing
Step 5: Collect results and recommend missing MCPs
```

**Output**:
```markdown
# MCP Health Check

## Expected MCPs (React + PostgreSQL Project)

### MANDATORY
- Serena MCP ✅ CRITICAL

### PRIMARY
- Puppeteer MCP (Frontend testing)
- Context7 MCP (React documentation)
- PostgreSQL MCP (Database operations)

### SECONDARY
- GitHub MCP (Version control)

## Health Check Workflow

Run these commands and report results:

### 1. Test Serena (MANDATORY)
```bash
/list_memories
```
Expected: ✅ Memory list returned
If fails: ❌ CRITICAL - Install Serena MCP immediately

### 2. Test Puppeteer (PRIMARY)
```bash
/browser_navigate https://example.com
```
Expected: ✅ Browser launches
If fails: ❌ Install Puppeteer OR use fallback (Playwright)

### 3. Test Context7 (PRIMARY)
```bash
/get-library-docs react
```
Expected: ✅ React documentation retrieved
If fails: ⚠️ Use web search fallback

### 4. Test PostgreSQL (PRIMARY)
```bash
# Test database connection (requires DB setup)
```
Expected: ✅ Connection established
If fails: ❌ Install PostgreSQL MCP OR use manual psql

### 5. Test GitHub (SECONDARY)
```bash
/list repositories
```
Expected: ✅ Repositories listed
If fails: ⚠️ Use manual git (low priority)

## Next Steps
1. Run health check workflow above
2. Report which MCPs are operational vs missing
3. I'll generate setup instructions for missing MCPs
4. Prioritize MANDATORY and PRIMARY MCPs first
```

---

## Success Criteria

**Successful when**:
- ✅ All recommendations include tier designation (MANDATORY/PRIMARY/SECONDARY/OPTIONAL)
- ✅ Every MCP has quantitative rationale (e.g., "Frontend 40% >= 20% threshold")
- ✅ Serena MCP always included as MANDATORY (Tier 1)
- ✅ Domain percentages drive PRIMARY tier (domain >= 20%)
- ✅ Health check workflow provided for all recommended MCPs
- ✅ Fallback chains consulted from domain-mcp-matrix.json
- ✅ Setup instructions ordered by priority (MANDATORY first)
- ✅ No uncertain language ("might", "probably", "consider")

**Fails if**:
- ❌ Recommendations without tier structure (flat list)
- ❌ Serena MCP missing from recommendations
- ❌ MCPs suggested without domain percentage justification
- ❌ Uncertain language used ("might want", "could use")
- ❌ Random alternatives suggested (not from fallback chain)
- ❌ No health check workflow provided
- ❌ Domain analysis skipped

---

## Common Pitfalls

### Pitfall 1: Flat MCP Lists

**Problem**: "You need Puppeteer, PostgreSQL, GitHub, Context7, Tavily" (no tiers)

**Why It Fails**: All MCPs treated equally → User doesn't know priorities

**Solution**: ALWAYS tier recommendations:
- Tier 1 MANDATORY: Serena
- Tier 2 PRIMARY: Domain MCPs (domain >= 20%)
- Tier 3 SECONDARY: Support MCPs
- Tier 4 OPTIONAL: Keyword-triggered

### Pitfall 2: Skipping Domain Percentages

**Problem**: User says "React app" → Agent suggests Puppeteer without calculating domain %

**Why It Fails**: No quantitative basis → Can't justify PRIMARY vs SECONDARY tier

**Solution**: ALWAYS calculate or estimate domain percentages:
- "React app" → Estimate Frontend 70%, Backend 20%, Database 10%
- Apply thresholds: Frontend 70% >= 20% → Puppeteer PRIMARY

### Pitfall 3: No Rationale

**Problem**: "Puppeteer MCP - for testing" (no domain percentage shown)

**Why It Fails**: User doesn't understand WHY Puppeteer is recommended

**Solution**: ALWAYS include quantitative rationale:
- "Puppeteer MCP (PRIMARY) - Frontend 40% >= 20% threshold requires functional browser testing"

---

## Validation

**How to verify mcp-discovery executed correctly**:

1. **Check Tier Structure**: All recommendations tiered ✅
2. **Check Serena MCP**: Present in Tier 1 MANDATORY ✅
3. **Check Rationale**: Every MCP has domain % justification ✅
4. **Check Health Checks**: Workflow provided for all MCPs ✅
5. **Check Fallback Chains**: Consulted from domain-mcp-matrix.json ✅
6. **Check Language**: No uncertain terms ("might", "probably") ✅

---

## References

- Domain-MCP mapping: mappings/domain-mcp-matrix.json
- Spec analysis: shannon-plugin/skills/spec-analysis/SKILL.md
- Phase planning: shannon-plugin/skills/phase-planning/SKILL.md
- Testing philosophy: shannon-plugin/core/TESTING_PHILOSOPHY.md

---

## Metadata

**Version**: 4.0.0
**Last Updated**: 2025-11-03
**Author**: Shannon Framework Team
**License**: MIT
**Status**: Core (Quantitative skill, required by spec-analysis)
