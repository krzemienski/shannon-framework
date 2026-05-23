---
name: reflect
description: Self-refinement pass. Modes: self (read last turn, propose fix), critique (spawn critic agent), memorize (save learned pattern).
replaces:
  - /reflexion:reflect
  - /reflexion:critique
  - /reflexion:remember
  - /oh-my-claudecode:self-improve
argument-hint: "[--mode self|critique|memorize] [--target <session-or-pr>]"
---

# /shannon:reflect

Self-refinement loop. Three modes; pick one per invocation.

## Inputs

- `--mode self|critique|memorize` (default `self`)
- `--target <session-id-or-PR-number>` — for `critique`/`memorize` modes; optional for `self`

## Behavior

### `--mode self`
1. Read the last assistant turn in the current session.
2. Identify gaps (unaddressed asks, vague claims, missing evidence).
3. Propose specific fixes.
4. Output: `reflect.md` at current working location.

### `--mode critique`
1. Spawn `critic` agent in isolated context against target artifact.
2. Critic emits findings (BLOCKING / HIGH / MEDIUM / LOW).
3. Output: `critique.md` with findings + cited file:line.

### `--mode memorize`
1. Extract a learned pattern from the current session OR target artifact.
2. Save to `~/.claude/memory/` (or project-local memory dir) with structured frontmatter.
3. Cross-link via `[[name]]` to related memories.
4. Output: confirmation of memory entry written.

## Success criteria

- Mode-specific output file written.
- For `critique`: every finding cites a path.
- For `memorize`: memory entry has frontmatter, name slug, MEMORY.md index updated.

## Hooks fired

- Standard chain.

## Skills invoked

- `reflect` (self mode)
- `critique` (critique mode)
- `memorize` (memorize mode)

## Examples

```
/shannon:reflect
/shannon:reflect --mode critique --target plans/260523-feature-x/plan.md
/shannon:reflect --mode memorize --target current-session
```
