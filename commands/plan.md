---
name: plan
description: Linear hierarchical plan author. Drops plans/{date-prefix}-{slug}/{plan.md + phase-NN.md files}. Validation phase included by default.
replaces:
  - /ck:plan
  - /oh-my-claudecode:plan
  - /anneal-alloy:anneal
  - /planning-with-files:planning-with-files
  - /create-validation-plan:create-validation-plan
argument-hint: "<feature-or-task-description> [--phases N] [--with-validation]"
---

# /shannon:plan

Linear plan author. The default plan command — fast, hierarchical, includes a validation phase unless explicitly skipped.

## Inputs

- Positional: feature description or task brief
- `--phases N` — suggest target phase count (default: auto-determined from scope)
- `--with-validation` — explicit: include validation phase (default true; flag is for documentation)

## Behavior

1. Invoke `plan-author` skill against the brief.
2. Output structure:
   ```
   plans/<date-prefix>-<slug>/
     plan.md              # overview, <80 lines, phase list
     phase-01-<name>.md
     phase-02-<name>.md
     ...
     research/            # researcher reports if any
     reports/             # subagent reports as work proceeds
   ```
3. Per phase file (canonical structure):
   - Context links
   - Overview (priority, status, description)
   - Key insights
   - Requirements (functional + non-functional)
   - Architecture
   - Related code files (to modify, create, delete)
   - Implementation steps (numbered)
   - Todo list (checkbox)
   - Success criteria (measurable)
   - Risk assessment
   - Security considerations
   - Next steps (dependencies)
4. Final phase is always validation (unless user-facing change is none).

## Success criteria

- `plan.md` created.
- Phase files numbered zero-padded.
- Every phase has measurable success criteria.
- Validation phase included if any user-facing change.

## Hooks fired

- `plan-before-execute` (PreToolUse:Write reminder if user starts editing `src/` without an open plan)

## Skills invoked

- `plan-author`
- `sequential-analysis` (for complex briefs)

## Examples

```
/shannon:plan "Add SSO with Okta to admin panel"
/shannon:plan "Migrate from SQLite to Postgres" --phases 8
```
