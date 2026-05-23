---
name: reflect
description: Self-refinement pass on prior output. Read last turn, identify gaps, propose specific fixes.
triggers:
  - "reflect on this"
  - "self-refine"
  - "iterate"
  - "self-improve"
  - "what could be better"
---

# reflect

Backs `/shannon:reflect --mode self`. Also used as the inner reflection step of `/shannon:loop`.

## Behavior contract

1. Read the artifact under reflection (last assistant turn, completed file, or named target).
2. Categorize the gaps:
   - **Unaddressed asks** — user requested X, response addressed Y instead.
   - **Vague claims** — "should work" without citation.
   - **Missing evidence** — claimed PASS without cited artifact.
   - **Drive-by edits** — changed lines that don't trace to the user's ask.
   - **Premature completion** — TaskUpdate=completed without gate.
3. For each gap: propose a specific fix (concrete next action, not "try harder").
4. Output `reflect.md` with structure:
   ```markdown
   ## Artifact reflected
   <path>

   ## Gaps
   1. <gap> → fix: <specific action>
   2. ...

   ## Converged?
   YES | NO (if NO, list remaining items)
   ```

## When to use

- End of a `/shannon:loop` iteration
- After completing a phase, before mark-as-done
- User says "reflect on this" / "what could be better"

## When NOT to use

- Trivial change with nothing to reflect on
- Adversarial review (use `/shannon:reflect --mode critique` instead)

## Iron rules

- No vague gaps ("it could be improved"). Specific or skip.
- No fix without an action verb.
- Converged YES means the inspector cannot find another gap.
