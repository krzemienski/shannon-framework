---
name: judge
description: LLM-as-judge evaluation of subagent outputs. Debate mode resolves ties via cross-judge argument.
triggers:
  - "judge outputs"
  - "evaluate candidates"
  - "rank subagent results"
  - "judge with debate"
---

# judge

Backs subagent output evaluation across all `/shannon:dispatch*` commands.

## Behavior contract

### Single-output mode (default)
1. Read subagent output + acceptance criteria from spawn context.
2. Score across dimensions:
   - **Completeness** — covers all acceptance criteria
   - **Correctness** — claims are accurate / code compiles / outputs match expected
   - **Quality** — style match, citation density, KISS adherence
   - **Iron rules** — no mocks, no test files, no fabricated evidence
3. Emit verdict: PASS | FAIL | NEEDS_REVISION.

### Debate mode (ties or stakes)
1. N candidate outputs.
2. Spawn 2-3 independent judges via `Task`. Each emits independent score.
3. If judges disagree by >1 severity tier: spawn debate round — each judge argues for its score citing evidence; meta-judge resolves.
4. Final verdict: meta-judge ranking with cited reasoning per candidate.

## When to use

- Every subagent output (default sequential dispatch)
- Competitive mode tie-breaking
- Pre-meta-judge synthesis in parallel mode

## When NOT to use

- Trivial outputs where success is binary (the executor already proved it via gate)

## Iron rules

- Judge does NOT author. Judge reads + emits verdict.
- No "good enough" — PASS or FAIL or NEEDS_REVISION.
- Cited reasoning per dimension. No vague PASSes.
- No self-judging — judge that helped produce an output cannot judge it.
