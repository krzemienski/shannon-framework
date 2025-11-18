---
name: root-cause-analysis
description: Map symptom → immediate cause → deeper cause → root cause with preventative actions
skill-type: PLAYBOOK
shannon-version: ">=5.4.0"
complexity-triggers: [0.30-1.00]
requires:
  - systematic-debugging
  - forced-reading-protocol
---

# Root Cause Analysis Skill

## Intent

Ensure every defect or incident ends with a verifiable causal chain and preventative guardrail. Used by `/shannon:ultrathink` after the systematic-debugging loop confirms a fix.

## Causal Chain Template

```
Symptom: <user-visible issue>
Immediate Cause: <closest technical failure>
Deeper Cause: <design/assumption issue>
Root Cause: <single actionable origin>
Evidence: <logs, line numbers, screenshots>
```

## Required Steps

1. **Evidence Gathering**
   - Preserve failing logs, traces, metrics.
   - Capture git diff hash showing defect location.
2. **Chain Construction**
   - Start with symptom; ask "why" iteratively until reaching immutable fact.
   - Each layer must include proof (line numbers, configs, experiments).
3. **Prevention Plan**
   - Add guardrail (test, monitor, lint rule, process change).
   - Update documentation/plan referencing change.
4. **Communication**
   - Save report under `docs/postmortems/YYYY-MM-DD-<slug>.md` or Serena memory.
   - Share summary with relevant agents (TEST_GUARDIAN, WAVE_COORDINATOR).

## Deliverables

- Markdown report containing:
  - Summary
  - Causal chain table
  - Fix description
  - Tests run
  - Guardrails
  - Follow-up tasks (if any)

## Guardrails

- Never stop at "developer error"—tie to process/tooling gap.
- If multiple root causes exist, list each separately.
- Link to plan/tests/PRs for traceability.

## Related Commands

- `/shannon:ultrathink`
- `/shannon:reflect`
- `/shannon:execute_plan` (append postmortem)
