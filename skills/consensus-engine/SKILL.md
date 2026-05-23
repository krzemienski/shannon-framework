---
name: consensus-engine
description: Multi-validator agreement gate. N independent validators against same feature; synthesize confidence-scored verdict.
triggers:
  - "consensus validation"
  - "validate with N reviewers"
  - "agreement gate"
  - "high-confidence validation"
  - "consensus gate"
---

# consensus-engine

Execution-time agreement gate. Spawns ≥2 (default 3) independent validators against the same feature; synthesizes confidence-scored verdict.

## Behavior contract

1. **Spawn** N consensus-validator subagents in parallel via `Task` tool. Each owns an isolated evidence subdirectory:
   ```
   e2e-evidence/consensus/<run-id>/
     validator-1/
     validator-2/
     validator-3/
     report.md  (synthesizer-owned)
   ```
2. Each validator runs the full journey list independently. Blind to peer verdicts.
3. **Synthesize** via `consensus-synthesis` (folded into this skill):
   - Per journey: compute (pass_count, fail_count, total).
   - Map to synthesis state:
     | State | Condition | Verdict | Confidence |
     |---|---|---|---|
     | UNANIMOUS_PASS | All PASS | PASS | HIGH |
     | UNANIMOUS_FAIL | All FAIL | FAIL | HIGH |
     | MAJORITY_PASS | ≥⅔ PASS | PASS (after disagreement protocol) | MEDIUM |
     | MAJORITY_FAIL | ≥⅔ FAIL | FAIL (after disagreement protocol) | MEDIUM |
     | SPLIT | Neither side ⅔ | DISAGREEMENT_UNRESOLVED | LOW |
4. **Disagreement protocol** (only on non-unanimous):
   - Identify diverging criteria.
   - Invoke `sequential-analysis` on the divergent evidence.
   - Re-resolve via case (a) re-run missing validator, (b) re-run minority, (c) sharpen criterion (escalate to planner), (d) discard erroring validator.
   - If unresolvable → SPLIT with LOW confidence; escalate.

## File ownership (LOAD-BEARING)

- Coordinator: writes NOTHING
- Validator-N: writes ONLY to `validator-<N>/` subdirectory
- Synthesizer: writes ONLY `report.md`

A validator that writes outside its directory invalidates the run.

## When to use

- High-stakes change (security, payments, production data)
- Pre-major-release validation
- After a near-miss bug to harden the gate
- User explicitly requests `--mode consensus`

## When NOT to use

- Routine refactor with no behavior change
- Exploratory work
- Speed-critical iteration (consensus is 3× the wall time of single-validator)

## Iron rules

- Confidence never upgrades — a late-arriving PASS verdict doesn't turn SPLIT into UNANIMOUS_PASS.
- Evidence quality cannot substitute for agreement.
- SPLIT is a real, reportable outcome. Do NOT silently downgrade to MAJORITY.
