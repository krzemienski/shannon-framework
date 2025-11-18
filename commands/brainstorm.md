---
name: shannon:brainstorm
description: Divergent idea generation + worktree preparation before planning or execution
usage: /shannon:brainstorm "problem or goal statement" [--workspace docs/plans] [--max-ideas 10]
tags: [ideation, discovery, planning, parity]
version: "5.4.0"
delegates_to:
  - brainstorming
  - phase-planning
---

# /shannon:brainstorm – Shannon Divergent Thinking Command

## Overview

`/shannon:brainstorm` mirrors the superpowers brainstorming workflow, but grounds the output in Shannon's 8D complexity heuristics and wave strategy. Use it when you need to explore *multiple* viable approaches, compare trade-offs, and prepare a clean workspace before writing a formal plan.

- Announce: "Running `/shannon:brainstorm` to explore candidate approaches."
- Output: Markdown doc in `docs/plans/brainstorm/YYYY-MM-DD-<slug>.md` with ranked options, risk notes, complexity estimates, and next actions.
- Integration: feeds directly into `/shannon:write_plan` or `/shannon:spec`.

## When to Use

| Situation | Why |
|-----------|-----|
| New feature with fuzzy scope | Need multiple architectures before committing |
| Large refactor | Surface phased approaches w/ risk & blast radius |
| Failing wave | Generate fallback options without disrupting execution queue |
| Prior to `/shannon:write_plan` | Provide raw material for the formal implementation plan |

## Required Inputs

1. **Problem statement** *(one paragraph)*.
2. **Constraints** *(tech stack, performance, compliance, etc.)*.
3. **Known blockers / unknowns**.

If constraints are missing, ask before proceeding.

## Output Template

```markdown
# Brainstorm: <Problem Name> (YYYY-MM-DD)

## Context Snapshot
- Goal:
- Constraints:
- Guardrails: (e.g., NO MOCKS, wave threshold)

## Candidate Approaches

### Option 1 – <Name>
- Summary:
- Pros:
- Cons:
- Estimated 8D Complexity: Scope ?, Tech ?, … Total ? (Simple/Moderate/Complex)
- Testing Strategy:
- Wave Recommendation: Sequential / Wave (N agents)

### Option 2 – …
```

End with **Recommendation** + **Next Commands**:
```
Recommended next steps:
1. /shannon:spec "<selected option>" --context docs/plans/brainstorm/…
2. /shannon:write_plan "<selected option>" --source docs/plans/brainstorm/…
```

## Guardrails

- Always produce **≥3 options** (unless domain truly constrains to fewer; state why).
- Include quick cost / risk comparison table.
- Note dependencies that influence later wave sequencing.
- Never claim decision made—list trade-offs and let operator confirm.

## See Also

- `skills/brainstorming/SKILL.md`
- `/shannon:write_plan`
- `/shannon:spec`
