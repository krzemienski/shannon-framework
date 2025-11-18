---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment - applies TDD to process documentation with Shannon quantitative validation by testing with subagents before writing, iterating until bulletproof against rationalization
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle**: If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**Shannon enhancement**: Quantitative validation of skill effectiveness.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are**: Reusable techniques, patterns, tools, reference guides

**Skills are NOT**: Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |

## When to Create a Skill

**Create when**:
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit
- **Shannon**: Complexity >0.4 or used >3 times

**Don't create for**:
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)

## SKILL.md Structure (Shannon Enhanced)

**Frontmatter (YAML)**:
```yaml
---
name: skill-name-with-hyphens
description: Use when [specific triggers and symptoms] - [what it does and how it helps, third person]
---
```

**Max 1024 characters total**
**Name**: Letters, numbers, hyphens only
**Description**: Third-person, starts with "Use when..."

**Body structure**:
```markdown
# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
Bullet list with SYMPTOMS and use cases
When NOT to use

## The Iron Law (if discipline-enforcing skill)
```
NO [THING] WITHOUT [REQUIREMENT] FIRST
```

## [Core Process/Pattern]
Step-by-step or before/after code

## Shannon Enhancement (if applicable)
Quantitative tracking, Serena integration, validation gates

## Known Violations and Counters
Baseline testing captured rationalizations

## Red Flags - STOP
If you catch yourself thinking...

## Common Rationalizations
| Excuse | Reality |
|--------|---------|

## Integration with Other Skills
Required, complementary, Shannon-specific

## The Bottom Line
Summary with Shannon quantitative angle
```

## RED-GREEN-REFACTOR for Skills

### RED Phase: Baseline Testing

**Run pressure scenarios WITHOUT the skill**:

```python
# Create test scenario
scenario = {
    "task": "Implement feature without TDD",
    "pressures": ["time_pressure", "sunk_cost", "exhaustion"],
    "expected_violation": "code_before_test"
}

# Run with sub-agent (no skill loaded)
result = run_subagent_test(scenario, skills=[])

# Document violations
violations = {
    "violated": True,
    "violation_type": "code_before_test",
    "rationalization": "I'll write tests after to verify it works",
    "timestamp": ISO_timestamp
}

serena.write_memory(f"skill_testing/{skill_name}/red_baseline", violations)
```

**Capture**:
- What choices did they make?
- What rationalizations did they use (verbatim)?
- Which pressures triggered violations?

**Shannon tracking**: Quantify violation rate:
```python
baseline_metrics = {
    "scenarios_tested": 5,
    "violations": 5,
    "violation_rate": 1.00,  # 100% violated without skill
    "common_rationalizations": [
        "I'll test after",
        "Too simple to test",
        "Deleting X hours is wasteful"
    ]
}
```

### GREEN Phase: Write Skill & Test

**Write skill addressing baseline violations**:
- Add explicit counters for each rationalization
- Create RED FLAGS list
- Build rationalization table

**Run same scenarios WITH skill**:
```python
# Run with skill loaded
result = run_subagent_test(scenario, skills=[skill_name])

# Verify compliance
compliance = {
    "violated": False,
    "complied": True,
    "skill_effectiveness": 1.00,  # 100% compliance
    "timestamp": ISO_timestamp
}

serena.write_memory(f"skill_testing/{skill_name}/green_compliance", compliance)
```

**Shannon validation**: Quantify improvement:
```python
green_metrics = {
    "scenarios_tested": 5,
    "violations": 0,
    "violation_rate": 0.00,  # 0% violated with skill
    "improvement": 1.00,  # 100% improvement
    "skill_effective": True
}
```

### REFACTOR Phase: Close Loopholes

**Find new rationalizations**:
- Run more pressure scenarios
- Increase pressure combinations
- Document new violations

**Add explicit counters**:
- Update rationalization table
- Add to RED FLAGS
- Re-test until bulletproof

**Shannon tracking**: Measure robustness:
```python
refactor_metrics = {
    "iterations": 3,
    "loopholes_found": 2,
    "loopholes_closed": 2,
    "final_violation_rate": 0.00,
    "pressure_scenarios_passed": 10,
    "robustness_score": 1.00  # Bulletproof
}

serena.write_memory(f"skill_testing/{skill_name}/final", refactor_metrics)
```

## Shannon-Specific Skill Patterns

### Quantitative Tracking in Skills

**Skills should include Serena tracking**:
```python
# Example from systematic-debugging skill
debugging_session = {
    "attempts": 2,
    "success": True,
    "duration_minutes": 30,
    "timestamp": ISO_timestamp
}

serena.write_memory(f"debugging/sessions/{session_id}", debugging_session)
```

### Validation Gates Integration

**Skills should reference Shannon's 3-tier validation**:
```markdown
## Verification

**Shannon 3-Tier Validation**:
- Tier 1 (Flow): Code compiles
- Tier 2 (Artifacts): Tests pass
- Tier 3 (Functional): Real systems verified (NO MOCKS)
```

### MCP Integration Patterns

**Skills should use MCP-discovery**:
```markdown
## Shannon Integration

**MCP Requirements**:
- Sequential: Deep analysis
- Serena: Pattern tracking
- Context7: Framework docs (if applicable)
```

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

**No exceptions**:
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Delete means delete

## Skill Creation Checklist

**RED Phase**:
- [ ] Create 3+ pressure scenarios
- [ ] Run WITHOUT skill
- [ ] Document violations verbatim
- [ ] Identify rationalization patterns
- [ ] **Shannon**: Quantify baseline violation rate

**GREEN Phase**:
- [ ] Write skill addressing violations
- [ ] Include rationalization table
- [ ] Include RED FLAGS
- [ ] Run scenarios WITH skill
- [ ] Verify compliance
- [ ] **Shannon**: Quantify improvement

**REFACTOR Phase**:
- [ ] Find new rationalizations
- [ ] Add explicit counters
- [ ] Re-test until bulletproof
- [ ] **Shannon**: Measure robustness score

**Shannon Validation**:
- [ ] Serena tracking code included
- [ ] Validation gates referenced (if applicable)
- [ ] MCP requirements specified
- [ ] Quantitative metrics defined

**Quality Checks**:
- [ ] Frontmatter: name + description only
- [ ] Description starts with "Use when..."
- [ ] Small flowchart only if decision non-obvious
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling

## Integration with Other Skills

**This is a meta-skill** for creating other skills.

**Required understanding**:
- **test-driven-development** - TDD principles apply to documentation

**Produces**:
- New skills following Shannon patterns
- Quantitatively validated process documentation

**Shannon integration**:
- **Serena MCP** - Track skill effectiveness
- **Sequential MCP** - Deep analysis for complex skills
- Sub-agent testing framework

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Shannon enhancement: Quantify everything.

Not "skill seems robust" - "skill: 0% violation rate across 10 pressure scenarios, robustness score 1.00".

Test with subagents. Measure effectiveness. Close loopholes systematically.

