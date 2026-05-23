---
name: validate
description: Detect platform, run validation journeys against the real system, capture evidence, emit cited PASS/FAIL verdicts. Replaces VF validate family and deepest-plan validate.
replaces:
  - /validationforge:validate
  - /validationforge:validate-plan
  - /validationforge:validate-ci
  - /validationforge:validate-sweep
  - /deepest-plan:deepest-validate
  - /lynx:audit
argument-hint: "[--mode quick|standard|consensus] [--platform ios|web|api|cli|fullstack]"
---

# /shannon:validate

End-to-end functional validation. Real system in, cited PASS/FAIL verdict out.

## Inputs

- `--mode quick|standard|consensus` (default `standard`)
  - `quick` — critical journeys only
  - `standard` — full discovery + journey execution
  - `consensus` — engages `consensus-engine` skill with N=3 independent validators
- `--platform ios|web|api|cli|fullstack` — override autodetect

## Behavior

1. Platform detection: read project markers (Xcode project files, `package.json`, `manage.py`, `Cargo.toml`, OpenAPI specs). Override with `--platform`.
2. Invoke `create-validation-plan` skill (planning domain). Output: `e2e-evidence/<run-id>/validation-plan.md` listing journeys with PASS criteria per step.
3. Dispatch to platform-specific execution under the `validator` agent. Agent routes by platform.
4. Per journey: capture evidence to `e2e-evidence/<run-id>/<journey-slug>/step-NN-<action>-<result>.<ext>`. Every evidence file must be non-empty.
5. `evidence-quality-check` hook fires after each Write — refuses zero-byte evidence.
6. After all journeys: `validator` agent writes per-journey verdict. Synthesis: lead writes `e2e-evidence/<run-id>/report.md`.
7. `--mode consensus`: invoke `consensus-engine` skill — spawns 3 isolated validators, synthesizes confidence-scored verdict.

## Success criteria

- Every journey has a PASS or FAIL verdict with cited evidence files.
- No INCONCLUSIVE outcomes — missing evidence = FAIL.
- Evidence inventory file lists every artifact with byte count.

## Hooks fired

- `block-fab-files` (PreToolUse:Write) — refuses `*.test.*` etc.
- `evidence-quality-check` (PostToolUse:Edit|Write) — flags empty evidence.
- `validation-not-compilation` (PostToolUse:Bash) — reminds that build success ≠ functional pass.
- `validation-skill-tripwire` (InvocationLayer) — fires if user invokes build without follow-up validate.

## Skills invoked

- `create-validation-plan` (planning)
- `functional-validation` (this domain)
- `evidence-gate`
- `consensus-engine` (only if `--mode consensus`)

## Examples

```
/shannon:validate
/shannon:validate --mode consensus
/shannon:validate --platform ios --mode standard
```
