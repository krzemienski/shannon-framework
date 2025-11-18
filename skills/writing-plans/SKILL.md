---
name: writing-plans
description: Use when design is complete and you need detailed implementation tasks for engineers with zero codebase context - creates comprehensive implementation plans with Shannon quantitative analysis, exact file paths, complete code examples, validation gates, and MCP requirements assuming engineer has minimal domain knowledge
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know with Shannon's quantitative rigor.

**Core principle**: Plans must be self-contained, quantitatively validated, and assume zero prior knowledge.

**Announce at start**: "I'm using the writing-plans skill to create the implementation plan."

**Shannon enhancement**: All plans include complexity scoring, validation gates, and MCP requirements.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes)**:
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this Shannon-enhanced header**:

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use shannon:executing-plans to implement this plan task-by-task.

**Goal**: [One sentence describing what this builds]

**Architecture**: [2-3 sentences about approach]

**Tech Stack**: [Key technologies/libraries]

---

## Shannon Quantitative Analysis

**Complexity Score**: 0.45/1.00 (MODERATE)

**8D Domain Distribution**:
- Backend: 60%
- Data: 25%
- Frontend: 10%
- DevOps: 5%

**Estimated Tasks**: 12 (formula: complexity × scope × domains)

**Estimated Duration**: 4-6 hours (based on complexity + task count)

**Risk Assessment**:
- High Risk: Database migrations (data layer)
- Medium Risk: API integration
- Low Risk: UI updates

---

## Validation Strategy

**Shannon 3-Tier Validation**:

**Tier 1 (Flow)**: 
- TypeScript: `tsc --noEmit`
- Linter: `ruff check .`

**Tier 2 (Artifacts)**:
- Tests: `npm test` (expect X/X pass)
- Build: `npm run build`

**Tier 3 (Functional - NO MOCKS)**:
- E2E: `npm run test:e2e` (Puppeteer required)
- Real database tests
- Real HTTP integration tests

---

## MCP Requirements

**Required MCPs**:
- puppeteer: Web testing (Tier 3 validation)
- sequential: Deep analysis for complex tasks

**Recommended MCPs**:
- context7: Framework documentation (if using React/etc)
- tavily: Best practices research (if new libraries)

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Shannon Metadata**:
- Complexity: 0.3/1.00 (SIMPLE)
- Estimated Time: 20 minutes
- Risk Level: LOW
- Validation Tier: 2 (Artifacts)

**Files**:
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**MCP Tools Needed**:
- None (standard tools sufficient)

**Step 1: Write the failing test (TDD RED phase)**

**Shannon Requirement**: Test must use REAL systems (NO MOCKS)

```python
# tests/path/test_feature.py
def test_specific_behavior():
    # ✅ GOOD: Real database
    db = connect_real_test_database()
    
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Shannon Verification**: 
- Exit code: 1 (failure)
- Reason: Feature missing (not typo)
- NO MOCKS: Verified (test uses real DB)

**Step 3: Write minimal implementation (TDD GREEN phase)**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Shannon Verification**:
- Exit code: 0 (success)
- Tests: 1/1 pass
- NO MOCKS: Still verified

**Step 5: Run validation gates**

```bash
# Tier 1: Flow
ruff check .  # Expect: 0 errors

# Tier 2: Artifacts  
pytest  # Expect: All tests pass
```

**Step 6: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature

Shannon validation: 2/3 tiers PASS (Tier 3 N/A for this task)"
```

**Shannon Tracking**: Save to Serena:
```python
serena.write_memory(f"plan_execution/task_{N}", {
    "task_id": N,
    "complexity": 0.3,
    "duration_actual": "18 minutes",
    "validation_tiers": [1, 2],
    "success": True
})
```
```

## Remember

- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Shannon quantitative metrics (complexity, time, validation tiers)
- MCP requirements explicitly stated
- NO MOCKS requirement enforced
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Shannon quantitative analysis complete.**

**Complexity**: 0.45/1.00 (MODERATE)  
**Tasks**: 12  
**Estimated Duration**: 4-6 hours  
**Validation Strategy**: 3-tier with NO MOCKS

**Three execution options:**

**1. Intelligent Execution (shannon:do)** - Automatic wave orchestration, fast iteration

**2. Systematic Execution (shannon:executing-plans)** - Batch execution with review checkpoints, full control

**3. Manual Execution** - You execute tasks yourself using plan as guide

**Which approach?"**

**If Systematic chosen**:
- **REQUIRED SUB-SKILL**: Use shannon:executing-plans
- Batch execution (complexity-based sizing)
- Review between batches
- Quantitative progress tracking

**If Intelligent chosen**:
- **REQUIRED SUB-SKILL**: Use shannon:wave-orchestration
- Automatic parallelization
- Shannon validation gates
- Faster but less control

## Shannon-Specific Enhancements

### Complexity Scoring Per Task

**Formula**: 
```python
task_complexity = calculate_8d_complexity({
    "backend": lines_of_code / 100,
    "data": database_operations / 10,
    "frontend": components / 5,
    # ... other dimensions
})

# Result: 0.00-1.00 scale
```

**Use this to**:
- Estimate task duration
- Determine validation requirements
- Size batches for execution
- Assess risk

### MCP Discovery Integration

**Auto-detect MCP requirements**:

```python
# Scan task for keywords
if "web" in task or "browser" in task:
    mcps.append("puppeteer")

if "analyze" in task or "complex" in task:
    mcps.append("sequential")

if framework in ["React", "Next.js", "Vue"]:
    mcps.append("context7")

if "research" in task or "best practices" in task:
    mcps.append("tavily")
```

### Validation Gates Per Task

**Determine which tiers apply**:

| Task Type | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|
| Backend logic | ✅ | ✅ | ✅ (real DB) |
| Frontend component | ✅ | ✅ | ✅ (Puppeteer) |
| Configuration | ✅ | ❌ | ❌ |
| Documentation | ✅ (linter) | ❌ | ❌ |

### Serena Persistence

**Save plan metadata**:

```python
plan_metadata = {
    "plan_id": plan_id,
    "feature_name": feature_name,
    "complexity": 0.45,
    "domain_distribution": {
        "backend": 0.60,
        "data": 0.25,
        "frontend": 0.10,
        "devops": 0.05
    },
    "total_tasks": 12,
    "estimated_duration_hours": 5.0,
    "validation_tiers": [1, 2, 3],
    "mcp_requirements": ["puppeteer", "sequential"],
    "created": ISO_timestamp
}

serena.write_memory(f"plans/{plan_id}/metadata", plan_metadata)
```

**Track execution later**:
```python
# When executing, reference the plan
execution = serena.read_memory(f"plans/{plan_id}/metadata")
```

## Integration with Other Skills

**This skill requires**:
- **forced-reading-protocol** - If analyzing existing requirements
- **spec-analysis** - For complexity scoring (8D analysis)

**This skill produces plans for**:
- **executing-plans** - Systematic batch execution
- **wave-orchestration** - Intelligent parallel execution

**Complementary skills**:
- **brainstorming** - Use before writing-plans (design first)
- **verification-before-completion** - Use during execution

## Example Plan Header

```markdown
# User Authentication System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use shannon:executing-plans

**Goal**: Implement secure user authentication with email/password and session management

**Architecture**: JWT-based authentication with bcrypt password hashing, session stored in Redis, protected routes via middleware

**Tech Stack**: Express.js, PostgreSQL, Redis, bcrypt, jsonwebtoken

---

## Shannon Quantitative Analysis

**Complexity Score**: 0.62/1.00 (COMPLEX)

**8D Domain Distribution**:
- Backend: 70% (auth logic, middleware)
- Data: 20% (user storage, sessions)
- Security: 10% (password hashing, JWT)

**Estimated Tasks**: 18
**Estimated Duration**: 8-10 hours

**Risk Assessment**:
- HIGH: Security (password storage, JWT secrets)
- MEDIUM: Session management (Redis integration)
- LOW: Route protection (standard middleware)

---

## Validation Strategy

**Tier 1 (Flow)**:
- `tsc --noEmit` (0 errors)
- `eslint .` (0 errors)

**Tier 2 (Artifacts)**:
- `npm test` (expect 45/45 pass)
- `npm run build` (exit 0)

**Tier 3 (Functional - NO MOCKS)**:
- `npm run test:e2e:auth` (Puppeteer)
- Real PostgreSQL database tests
- Real Redis session tests
- NO mocking of bcrypt, JWT, or database

---

## MCP Requirements

**Required**:
- puppeteer: Browser-based auth flow testing
- sequential: Security analysis for auth patterns

**Recommended**:
- context7: Express.js middleware patterns
- tavily: JWT best practices research

---
```

## The Bottom Line

**Plans are contracts. Be specific. Be quantitative. Assume nothing.**

Shannon's enhancements transform vague plans into quantitatively validated roadmaps.

Not "implement auth" - "implement auth (complexity 0.62, 18 tasks, 8-10 hours, 3-tier validation with NO MOCKS)".

