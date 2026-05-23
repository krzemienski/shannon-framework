---
name: prd
description: Structured Product Requirement Document authoring. Interview-driven sections (Why / What / How / Success Metrics / Risks).
replaces:
  - /prd-generator:prd-generator
argument-hint: "<feature-description>"
---

# /shannon:prd

PRD authoring with structured interview. Output: a PRD.md that can feed `/shannon:plan` or `/shannon:plan-deep`.

## Inputs

- Positional: feature description (will be refined through interview)

## Behavior

1. Invoke `plan-author` skill in PRD mode.
2. Interview via `AskUserQuestion` tool:
   - WHY does this matter? (problem statement, business value)
   - WHAT is in scope vs out of scope?
   - WHO is the user? (personas, jobs-to-be-done)
   - WHEN is success? (success metrics, observable behaviors)
   - WHERE does this fit? (system context, dependencies)
   - HOW will we ship? (rollout strategy, risk mitigation)
3. Synthesize PRD.md to `plans/<date>-<slug>/PRD.md`.
4. Explicit user approval gate at end — interview asks "approve to proceed to /shannon:plan?".

## PRD structure

```markdown
# PRD: <feature name>

## Problem statement
## Goals + non-goals
## User personas + jobs-to-be-done
## Success metrics (measurable)
## Functional requirements
## Non-functional requirements (perf, security, accessibility)
## System context + dependencies
## Risks + mitigation
## Rollout strategy
## Open questions
```

## Success criteria

- PRD.md created.
- All sections populated.
- User explicitly approved.

## Hooks fired

- Standard chain (read-mostly)

## Skills invoked

- `plan-author` (PRD subskill)
- `sequential-analysis`

## When to use

- Pre-`/shannon:plan` when feature is large or stakeholder alignment needed.
- When success metrics aren't yet defined.

## When NOT to use

- Small refactor, bug fix, or routine feature (`/shannon:plan` directly).
