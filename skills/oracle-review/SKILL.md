---
name: oracle-review
description: Pre-execution plan-review AND post-execution evidence-audit. Quorum-gated. Spawns ≥3 isolated oracle agents; ≥2 APPROVE required.
triggers:
  - "oracle review"
  - "plan review"
  - "evidence audit"
  - "quorum review"
  - "final gate audit"
---

# oracle-review

Quorum gate. Invoked at two points: BEFORE execution (plan review) AND AFTER execution (evidence audit).

## Behavior contract

### Pre-execution (plan-review)

1. Spawn 3 `oracle` agents in parallel, isolated contexts. Each receives the plan + codebase-analysis + documentation-research artifacts.
2. Each oracle independently emits:
   ```
   verdict: APPROVE | REFUSE
   cited_blocker: <if REFUSE, file:line evidence>
   summary: <one paragraph>
   ```
3. Aggregate: ≥2 APPROVE AND 0 unresolved critical blockers → PASS; pipeline proceeds.
4. Otherwise: REFUSE → invoke `refusal-discipline`; halt.

### Post-execution (evidence-audit)

1. Spawn 3 `oracle` agents in parallel, isolated contexts. Each receives full evidence tree.
2. Each oracle reads cited evidence per MSC, votes APPROVE / REFUSE.
3. Aggregate via same quorum rule.

## File ownership

- Coordinator: writes nothing.
- Oracle-N: writes ONLY `e2e-evidence/<run-id>/oracle-quorum/oracle-<N>/verdict.md`.
- Synthesizer: writes ONLY `e2e-evidence/<run-id>/oracle-quorum/report.md`.

## When to use

- Phase 4 of `/shannon:forge` (pre-execution plan review).
- Phase 9 of `/shannon:forge` (post-execution evidence audit).
- Standalone audit via `/shannon:audit-completion`.

## When NOT to use

- Routine `/shannon:cook` runs (lightweight) — only forge invokes oracle quorum.

## Iron rules

- **Distinct from reviewer.** Oracle = pre-execution gate OR final evidence audit. Reviewer = post-implementation code/security/perf review. Both can exist for the same run.
- **No self-review.** Oracle that produced an artifact may not also review it.
- **Quorum is hard.** 2/3 APPROVE OR refusal.
- **Citations specific.** Directory references do not count; file path + line range where relevant.
