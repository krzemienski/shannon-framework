---
name: resume
description: Inspect evidence tree, identify last completed phase, resume from the next missing phase artifact. Evidence-tree-as-state.
replaces:
  - /crucible:resume
  - /campaign-state:resume
argument-hint: "[--run-id <id>]"
---

# /shannon:resume

Resume a halted `/shannon:forge` or `/shannon:autopilot` run. No separate state file — the evidence tree IS the state.

## Inputs

- `--run-id <id>` — run identifier (default: latest under `e2e-evidence/`)

## Behavior

1. Resolve run-id (latest, or as provided).
2. Walk `e2e-evidence/<run-id>/` directories in canonical phase order:
   - `codebase-analysis/`
   - `documentation-research/`
   - `plan/`
   - `oracle-plan-reviews/`
   - `execution/`
   - `validation/`
   - `consensus/` (if consensus mode)
   - `oracle-quorum/`
   - `completion-gate/`
3. Find first directory missing its `INDEX.md` or expected terminal artifact (`verdict.md`, `report.json`).
4. Restart pipeline from that phase. Prior phases trusted as complete.

## Success criteria

- Pipeline continues from precise resume point.
- No re-work of completed phases (which can contaminate fresh-evidence invariant).
- Final state matches if run had not been halted.

## Hooks fired

- Standard chain from resume point forward.

## Skills invoked

- `completion-gate` (state reader)
- Whichever phase skill is resumed

## Iron rules

- Never restart a completed phase on resume — contamination risk.
- Never invent state — the evidence tree is the truth.

## Examples

```
/shannon:resume
/shannon:resume --run-id 260523-1334
```
