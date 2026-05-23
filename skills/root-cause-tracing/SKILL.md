---
name: root-cause-tracing
description: Five-whys + cause-and-effect diagram + analysis report. Drives /shannon:why.
triggers:
  - "why is X happening"
  - "root cause"
  - "five whys"
  - "cause and effect"
  - "fishbone analysis"
---

# root-cause-tracing

Backs `/shannon:why`. Five-whys cascade plus Ishikawa categorization.

## Behavior contract

1. Read symptom description.
2. Apply five-whys: each "why" probes one level deeper. Stop when an actionable root cause is reached (not "it's complicated").
3. Build cause-and-effect diagram categorizing across:
   - **Code** — logic error, race condition, type mismatch, edge case
   - **Data** — bad input, schema drift, missing record, stale cache
   - **Config** — wrong env var, misconfigured route, missing secret
   - **Environment** — OS/runtime version, network, hardware constraint
   - **Dependency** — library bug, version mismatch, broken upstream
   - **Human** — incorrect assumption, missed step, undocumented constraint
4. Identify primary category + minimal fix.
5. Write `reports/root-cause-<slug>.md`.

## Per the `instrument-before-theorize.md` rule

If you can't determine root cause in 10 minutes of reading code, **add instrumentation**:
- Print statements at boundary points
- Trace logs at each candidate root cause site
- Live reproduction with the actual data
- THEN re-apply five-whys with empirical evidence

## When to use

- `/shannon:why` invocation
- Phase 2 of `/shannon:fix` (debug step)
- Post-incident analysis

## When NOT to use

- Obvious bugs (null pointer, typo) — fix and move on
- Configuration errors with clear error messages — read and fix

## Iron rules

- Empirical > theoretical. Instrument > reason.
- Five-whys reaches actionable cause, not vague label.
- Cited evidence per "why" answer (log path, file:line).
