---
name: functional-validation
description: End-to-end no-mocks validation through real system execution. Build, run, exercise UI, capture evidence, apply gate validation.
triggers:
  - "validate this"
  - "prove it works"
  - "functional validation"
  - "no mocks"
  - "ensure feature works"
  - "validate the feature"
---

# functional-validation

Iron-rule no-mocks validation. Real system in, evidence-cited verdict out.

## Behavior contract

Five steps, in order:

1. **Build the real system.** No stubs. No fakes. No mocked dependencies. If the build doesn't succeed, validation is BLOCKED — fix the build first.
2. **Run it.** Start the actual server / app / CLI / simulator. Real ports. Real processes.
3. **Exercise through UI / real interface.** Real clicks (agent-browser), real cURL requests, real CLI invocations, real iOS simulator taps.
4. **Capture evidence.** Screenshots, API response bodies (with headers), CLI stdout, logs with timestamps. All artifacts land under `e2e-evidence/<run-id>/<journey>/step-NN-<desc>.<ext>`.
5. **Apply gate validation.** Invoke `evidence-gate` skill — 5-question checklist. Any "no" → REFUSE.

## When to use

- Marking a feature complete
- Pre-merge / pre-deploy / pre-ship
- Verifying a bug fix worked
- Validating a UI redesign
- Any time the assistant claimed "done"

## When NOT to use

- Pure type-system change with no runtime behavior shift (typecheck is enough)
- Documentation-only commit
- File rename with no semantic change

## Iron rules (absolute)

- **NO mocks, stubs, test doubles, fixtures.**
- **NO test files** (`*.test.*`, `*.spec.*`, `tests/`, `__tests__/`). The `block-fab-files` hook enforces this; do not try to bypass.
- **NO fabricated evidence.** Quote real CLI stdout. Real screenshot pixels. Real HTTP response bodies.
- **NO zero-byte evidence files.** `evidence-quality-check` hook refuses empty artifacts.
- **NO compilation-success as proof of function.** Build pass ≠ feature works. Always exercise the running system.
- Citations specific: `e2e-evidence/<run-id>/<journey>/step-03-login-success.png:` (file, not directory). Line ranges where relevant.

## Examples

```
Feature: "Add password reset link to login page"
1. pnpm build → exit 0
2. pnpm dev → server up on :3000
3. agent-browser navigate /login → screenshot step-01-login-loaded.png
4. agent-browser click "Forgot password" → screenshot step-02-reset-modal.png
5. agent-browser fill email → submit → screenshot step-03-email-sent-toast.png
6. evidence-gate → PASS (citations: step-01, step-02, step-03)
```
