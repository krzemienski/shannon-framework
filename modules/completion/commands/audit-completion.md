---
name: audit-completion
description: Read evidence tree for a forge run, print MSC table, reviewer consensus, oracle quorum, overall verdict. Read-only.
replaces:
  - /crucible:status
  - /crucible:audit
  - /validationforge:validate-team-dashboard
argument-hint: "[--run-id <id>]"
---

# /shannon:audit-completion

Read-only audit of a completion run. Prints status, reviewer/oracle votes, verdict.

## Inputs

- `--run-id <id>` — completion run identifier (default: latest under `e2e-evidence/`)

## Behavior

1. Resolve run-id (latest, or as provided).
2. Read `e2e-evidence/<run-id>/completion-gate/report.json` for MSC verdict table.
3. Read `e2e-evidence/<run-id>/consensus/report.md` (if exists) for reviewer consensus.
4. Read `e2e-evidence/<run-id>/oracle-quorum/report.md` (if exists) for oracle votes.
5. Print to stdout AND write to `reports/completion-<run-id>.md`:
   - MSC table (per criterion: status + cited evidence path)
   - Reviewer consensus (per reviewer: PASS/FAIL + summary)
   - Oracle quorum (per oracle: APPROVE/REFUSE + cited blocker if any)
   - Overall verdict: COMPLETE | REFUSED | IN_PROGRESS

## Success criteria

- Report saved.
- Every MSC line has a citation.
- Every oracle/reviewer line has a verdict + summary.

## Hooks fired

None — read-only.

## Skills invoked

- `completion-gate` (read-only state inspection)
- `evidence-indexing` (validate INDEX.md files exist)

## Examples

```
/shannon:audit-completion
/shannon:audit-completion --run-id 260523-1334
```
