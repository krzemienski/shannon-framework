---
name: critique
description: Adversarial critique of current work. Find holes, name what's missing, identify where assumptions break.
triggers:
  - "critique this"
  - "find holes"
  - "what's wrong"
  - "adversarial review"
  - "tear it apart"
---

# critique

Backs `/shannon:reflect --mode critique`. Spawns `critic` agent in isolated context.

## Behavior contract

1. Identify the artifact under critique (plan, PRD, code diff, evidence package).
2. Spawn `critic` agent via `Task`. Critic owns its output directory.
3. Critic emits findings classified BLOCKING / HIGH / MEDIUM / LOW with cited file:line.
4. Aggregate critic output; surface to user via `critique.md`.

## When to use

- Pre-merge code review (before peer review)
- Pre-execution plan review (lighter than oracle quorum)
- After a near-miss to harden the next iteration

## When NOT to use

- Quick sanity check (use `/shannon:reflect` self-mode)
- Already-reviewed artifact (don't re-critique what oracle has gated)

## Iron rules

- Critique is one-shot. Critic does not iterate with author.
- Findings cite file:line.
- No softening — BLOCKING stays BLOCKING.

## Output

```markdown
# Critique — <artifact>

## BLOCKING
- <finding> [<file>:<line>]
...

## HIGH
- ...

## MEDIUM
- ...

## LOW
- ...
```
