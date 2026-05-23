---
name: refusal-discipline
description: When evidence is missing, write a structured REFUSAL.md and stop. No override, no force-complete. Refusal is a feature.
triggers:
  - "evidence gap"
  - "missing citation"
  - "gate unmet"
  - "refusal needed"
  - "block completion"
---

# refusal-discipline

The refusal pattern, codified. Crucible's contribution to Shannon's iron rules.

## Behavior contract

When invoked (typically by `completion-gate` finding a blocker):

1. Construct REFUSAL.md with structured sections:
   ```markdown
   # REFUSAL — <run-id>
   **Date:** <ISO-8601>
   **Phase:** <phase that produced the refusal>

   ## Cited Blockers

   ### Blocker 1
   - **MSC:** <criterion name>
   - **Why refused:** <one-line reason>
   - **Evidence expected:** <path that should exist>
   - **Evidence actual:** <missing | zero-byte | content-not-matching-claim>
   - **Remediation:** <what would unblock>

   ### Blocker 2
   ...

   ## What was NOT done
   - <phases skipped because of refusal>

   ## How to retry
   - Run /shannon:cook <remediation prompt>
   - Or /shannon:autopilot <task> — refusal-driven retry loop
   ```
2. Write to `plans/reports/REFUSAL-<run-id>.md`.
3. Set TaskUpdate status appropriately (`in_progress` with note, NOT `completed`).
4. Return from the calling skill; HALT the pipeline.

## When to use

- `completion-gate` finds any unmet MSC.
- Validator finds FAIL it cannot reconcile.
- Oracle quorum returns REFUSE.
- Loop hits max-iter without convergence.

## When NOT to use

- Recoverable error (re-try the same step is fine).
- Warning-level finding (LOW severity).

## Iron rules

- **NO `--force-complete` flag.** Refusal is the final word.
- **NO silent downgrade.** A SPLIT consensus does not become a MAJORITY by omission.
- **Cite specific evidence file paths.** No prose-only blockers.
- The REFUSAL.md is the basis for the next `/shannon:autopilot` attempt's remediation prompt.
