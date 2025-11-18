---
name: brainstorming
description: Use when creating or developing ideas before writing code or implementation plans - refines rough ideas into fully-formed designs through collaborative questioning with Shannon quantitative validation, alternative exploration, and incremental validation. Don't use during clear mechanical processes
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue with Shannon's quantitative rigor.

**Core principle**: Understand deeply, explore alternatives, validate quantitatively, document systematically.

## The Process

### Understanding the Idea

**Check project context first**:
- Read existing files, docs, recent commits
- **Shannon**: Use project-indexing skill if available
- Load context from Serena if project known

**Ask questions one at a time** to refine the idea:
- Prefer multiple choice when possible
- Open-ended is fine too
- **Only one question per message**
- Break topics into multiple questions

**Focus on understanding**:
- Purpose
- Constraints
- Success criteria
- **Shannon**: Quantitative success metrics

### Exploring Approaches

**Propose 2-3 different approaches** with trade-offs:
- Present conversationally with recommendation
- Lead with recommended option and reasoning
- **Shannon enhancement**: Include complexity estimates

**Example**:
```markdown
I see three approaches:

**Option 1: Microservices** (Recommended)
- Complexity: 0.75/1.00 (COMPLEX)
- Duration: 2-3 weeks
- Pros: Scalability, isolation
- Cons: Higher initial complexity
- **Why recommended**: Aligns with growth plans

**Option 2: Monolith**
- Complexity: 0.45/1.00 (MODERATE)
- Duration: 1 week
- Pros: Simpler, faster to build
- Cons: Scaling limitations

**Option 3: Hybrid**
- Complexity: 0.55/1.00 (MODERATE-COMPLEX)
- Duration: 1.5-2 weeks
- Pros: Balance of both
- Cons: Some compromise on both sides

Which appeals to you?
```

### Presenting the Design

**Once you understand what you're building**:

**Break into sections** of 200-300 words:
- Ask after each section whether it looks right
- Cover: architecture, components, data flow, error handling, testing
- **Shannon**: Include quantitative estimates

**Be ready to go back and clarify** if something doesn't make sense

**Shannon quantitative validation**:
```markdown
## Design Validation

**Complexity Analysis** (Shannon 8D):
- Backend: 60%
- Data: 25%
- Frontend: 10%
- DevOps: 5%
**Overall**: 0.65/1.00 (COMPLEX)

**Estimated Effort**: 80-100 hours

**Risk Assessment**:
- HIGH: Database migrations
- MEDIUM: API integration
- LOW: UI updates

**MCP Requirements**:
- puppeteer (functional testing)
- sequential (complex analysis)
- context7 (framework docs if needed)
```

## After the Design

### Documentation

**Write validated design** to `docs/plans/YYYY-MM-DD-<topic>-design.md`:

```markdown
# [Feature] Design Document

**Date**: YYYY-MM-DD
**Status**: Approved
**Complexity**: 0.65/1.00 (COMPLEX)

## Overview
[2-3 sentences]

## Architecture
[Design sections validated through brainstorming]

## Shannon Analysis

**8D Complexity**: 0.65/1.00
- Backend: 60%
- Data: 25%
- Frontend: 10%
- DevOps: 5%

**Estimated Effort**: 80-100 hours

**Risk Assessment**:
- HIGH: Database migrations
- MEDIUM: API integration
- LOW: UI updates

**Validation Strategy**:
- Tier 1: Flow validation
- Tier 2: Artifact validation
- Tier 3: Functional (NO MOCKS)

**MCP Requirements**:
- puppeteer
- sequential
- context7 (if using React/Next.js)

## Next Steps

- [ ] Create implementation plan (use writing-plans skill)
- [ ] Execute plan (use executing-plans or intelligent-do)
```

**Commit the design document** to git

**Shannon tracking**: Save to Serena:
```python
serena.write_memory(f"designs/{design_id}", {
    "feature": feature_name,
    "complexity": 0.65,
    "domain_distribution": {
        "backend": 0.60,
        "data": 0.25,
        "frontend": 0.10,
        "devops": 0.05
    },
    "estimated_hours": 90,
    "risks": {"HIGH": 1, "MEDIUM": 1, "LOW": 1},
    "approved": True,
    "timestamp": ISO_timestamp
})
```

### Implementation (if continuing)

**Ask**: "Ready to set up for implementation?"

**Two options**:

**Option 1: Write detailed plan** (systematic approach)
- **REQUIRED SUB-SKILL**: Use shannon:writing-plans
- Creates quantitative implementation plan
- Then use shannon:executing-plans for systematic execution

**Option 2: Direct execution** (automatic approach)
- **REQUIRED SUB-SKILL**: Use shannon:intelligent-do
- Automatic wave orchestration
- Faster but less control

## Key Principles

- **One question at a time** - Don't overwhelm
- **Multiple choice preferred** - Easier to answer
- **YAGNI ruthlessly** - Remove unnecessary features
- **Explore alternatives** - Always propose 2-3 approaches
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when needed
- **Shannon quantitative** - Complexity scores, time estimates, risk levels

## Shannon Enhancement: Quantitative Validation

**During brainstorming, track**:

```python
brainstorm_metrics = {
    "questions_asked": 12,
    "alternatives_explored": 3,
    "design_iterations": 2,
    "sections_validated": 5,
    "final_complexity": 0.65,
    "estimated_hours": 90,
    "confidence": 0.85,  # How confident in the design
    "timestamp": ISO_timestamp
}

serena.write_memory(f"brainstorm/{session_id}", brainstorm_metrics)
```

**Learn from patterns**:
```python
# Query historical brainstorms
similar = serena.query_memory("brainstorm/*/complexity~0.6")

# Provide context
avg_duration = average([s["estimated_hours"] for s in similar])
# "Similar designs (complexity ~0.6) took average 85 hours"
```

## Integration with Other Skills

**This skill leads to**:
- **writing-plans** - After design complete, create detailed plan
- **intelligent-do** - Alternative: direct execution

**This skill uses**:
- **spec-analysis** - For complexity scoring (8D analysis)
- **project-indexing** - For understanding existing codebase
- **mcp-discovery** - For identifying MCP requirements

**Shannon integration**:
- **Serena MCP** - Track design decisions, learn patterns
- **Sequential MCP** - Deep analysis for complex design decisions
- **Context7 MCP** - Framework documentation when needed

## The Bottom Line

**Brainstorming is design with Shannon's quantitative validation.**

Not "this design looks good" - "this design: complexity 0.65, 90 hours, 3 HIGH risks mitigated, validated through 5 sections".

Systematic questioning + quantitative validation = reliable designs.

