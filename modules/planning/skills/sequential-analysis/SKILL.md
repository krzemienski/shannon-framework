---
name: sequential-analysis
description: Structured multi-step reasoning with revision capability. For complex problems, root-cause investigation, ambiguous scope.
triggers:
  - "sequential analysis"
  - "step by step reasoning"
  - "complex problem"
  - "ambiguous scope"
  - "revision capability"
---

# sequential-analysis

Wraps `sequential-thinking` MCP (or equivalent). Used for multi-step reasoning where revisions matter.

## Behavior contract

1. Break problem into discrete thought steps (start with estimate of N steps).
2. For each step: state the thought, identify any new ambiguity, note dependencies.
3. Revision support: if a later step exposes that an earlier step was wrong, mark it as revised; re-derive downstream.
4. Branch support: if multiple viable directions exist, branch; track each branch ID; merge winning branch back to main.
5. Hypothesis verification: end-state hypothesis must be verified by tracing the chain of reasoning back to evidence.

## When to use

- Plan author hits a non-obvious decomposition
- Validator finds contradictory evidence
- Refusal-discipline needs to enumerate cascading blockers
- Disagreement protocol in consensus-engine

## When NOT to use

- Simple, linear task with obvious decomposition
- Time-critical iteration (sequential analysis adds latency)

## Output format

```markdown
## Thought 1
<step 1 reasoning>

## Thought 2
<step 2 reasoning>

## Thought 3 (revises Thought 1)
<revised reasoning + why prior thought was wrong>

## Hypothesis
<final claim>

## Verification trace
- Thought 1 → ... → Thought N → Hypothesis (each link cites evidence)
```

## Iron rules

- No invented chain links — every step cites prior step or external evidence.
- Revisions explicit (which earlier step is being revised, why).
- Final hypothesis only emitted after verification trace passes.
