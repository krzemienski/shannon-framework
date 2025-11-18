---
name: shannon:write-plan
description: |
  Create detailed implementation plan with Shannon quantitative analysis. Generates comprehensive
  plans with complexity scoring, validation gates, MCP requirements, and bite-sized tasks.
  Plans saved to docs/plans/ with full quantitative metadata for systematic execution.

usage: |
  /shannon:write-plan
  /shannon:write-plan --feature "feature name"

examples:
  - /shannon:write-plan
  - /shannon:write-plan --feature "user authentication system"

delegates_to:
  - writing-plans

version: "5.4.0"
---

# /shannon:write-plan - Create Implementation Plan

## Purpose

Create comprehensive implementation plans with Shannon's quantitative methodology:
- ✅ Complexity scoring (8D analysis)
- ✅ Validation gates per task
- ✅ MCP requirements detection
- ✅ Bite-sized tasks (2-5 min each)
- ✅ Complete code examples
- ✅ Exact file paths
- ✅ Serena persistence

**Philosophy**: Plans are contracts. Be specific. Be quantitative. Assume nothing.

---

## Workflow

### Step 1: Invoke writing-plans Skill

The command delegates all planning logic to the writing-plans skill:

```
Invoke sub-skill:
@skill writing-plans

Feature: {user_provided_feature_description}
```

The skill handles:
- Complexity analysis (8D scoring)
- Domain distribution calculation
- Task breakdown
- Validation gate specification
- MCP requirements detection
- Quantitative estimation
- Plan document generation

### Step 2: Report Results

After skill completes, display summary:

```markdown
✅ Implementation Plan Created

**Plan**: docs/plans/YYYY-MM-DD-{feature}.md

**Shannon Analysis**:
- Complexity: 0.62/1.00 (COMPLEX)
- Domains: Backend 70%, Data 20%, Security 10%
- Tasks: 18 tasks
- Estimated Duration: 8-10 hours

**Validation Strategy**:
- Tier 1: Flow validation (tsc, linter)
- Tier 2: Artifacts (tests, build)
- Tier 3: Functional (NO MOCKS - Puppeteer, real DB)

**MCP Requirements**:
- puppeteer (E2E testing)
- sequential (security analysis)
- context7 (if framework docs needed)

**Execution Options**:
1. Systematic: /shannon:execute-plan (batch execution with review)
2. Automatic: /shannon:do --with-plan (wave orchestration)
3. Manual: Follow plan yourself

**Saved to Serena**: plans/{plan_id}/metadata
```

---

## Parameters

**--feature**: Feature name/description (optional, will prompt if not provided)  
**--auto**: Skip confirmations  
**--complexity**: Force complexity level (0.0-1.0)

---

## Integration with Shannon CLI

Shannon CLI can invoke this command via Agent SDK:

```python
# Shannon CLI code
async for message in sdk_client.query(
    prompt="/shannon:write-plan --feature 'user auth'",
    options=ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "{shannon_framework_path}"}],
        setting_sources=["user", "project"]
    )
):
    # Command executes writing-plans skill
    # Returns plan with quantitative analysis
```

Or invoke skill directly:

```python
async for message in sdk_client.invoke_skill(
    skill_name='writing-plans',
    prompt_content=f"Feature: {feature}"
):
    # Same result
```

---

## Examples

### Simple Feature

```bash
/shannon:write-plan --feature "add password reset endpoint"

# Output:
# ✅ Plan: docs/plans/2025-11-18-password-reset.md
# Complexity: 0.35/1.00 (SIMPLE)
# Tasks: 6
# Duration: 2-3 hours
# Tier 3: Real HTTP tests required
```

### Complex Feature

```bash
/shannon:write-plan --feature "implement e-commerce checkout with Stripe"

# Output:
# ✅ Plan: docs/plans/2025-11-18-ecommerce-checkout.md
# Complexity: 0.68/1.00 (COMPLEX)
# Tasks: 24
# Duration: 12-15 hours
# MCP: puppeteer, sequential, tavily (Stripe best practices)
# High Risk: Payment processing (security critical)
```

---

## Integration with Other Commands

**Leads to**:
- **/shannon:execute-plan** - Systematic batch execution of created plan
- **/shannon:do --with-plan** - Automatic execution with wave orchestration

**Works with**:
- **/shannon:spec** - Can create plan from specification analysis
- **/shannon:brainstorm** - Design first, then create plan

---

**Status**: Command complete, delegates to writing-plans skill

