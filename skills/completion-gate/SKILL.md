---
name: completion-gate
description: Evaluate the completion gate. Refuses on any missing MSC. Reads evidence tree; emits machine-readable report.json. No override flag.
triggers:
  - "completion gate"
  - "ship gate"
  - "evaluate completion"
  - "final completion gate"
---

# completion-gate

Final-gate evaluator. Reads the entire evidence tree, evaluates every Mandatory Success Criterion against cited evidence, requires three-reviewer consensus PASS plus Oracle quorum APPROVED.

## Behavior contract

1. Read `e2e-evidence/<run-id>/` tree.
2. For each MSC (Mandatory Success Criterion) declared in the plan:
   - Locate cited evidence file(s).
   - Verify file exists, non-empty, content supports the claim.
   - Mark MSC: PASS / FAIL / MISSING.
3. Read consensus report (if applicable) — require ≥2/3 reviewer PASS.
4. Read oracle quorum report — require ≥2/3 oracle APPROVE + 0 unresolved critical blockers.
5. Emit `e2e-evidence/<run-id>/completion-gate/report.json`:
   ```json
   {
     "run_id": "...",
     "msc_count": N,
     "msc_pass": M,
     "msc_fail_or_missing": K,
     "reviewer_consensus": "PASS" | "FAIL" | "N/A",
     "oracle_quorum": "APPROVED" | "REFUSED" | "N/A",
     "verdict": "COMPLETE" | "REFUSED",
     "cited_blockers": [ { "msc": "...", "reason": "...", "evidence_path": "..." } ]
   }
   ```
6. If any MSC FAILED, MISSING, or quorum REFUSED → verdict REFUSED. Write `REFUSAL.md` alongside report.json.

## When to use

- Phase 10 of `/shannon:forge`
- Final gate of `/shannon:autopilot` retry loop
- Audit checkpoint via `/shannon:audit-completion`

## When NOT to use

- Mid-iteration (gate only fires at outer boundary)
- Exploratory work without declared MSCs

## Iron rules

- **NO override flag.** No `--force-complete`. No `--accept-blockers`.
- **NO inferred MSCs** — only those declared in the plan count.
- **Missing evidence = FAIL, not INCONCLUSIVE.**
- Self-review forbidden — gate is mechanical, not advisory.
