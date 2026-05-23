# Phase 4 — Hooks + Install Scripts Integration Evidence

**Date:** 2026-05-23
**Worktree:** wt/shannon-rebuild-integration
**Branched from:** wt/shannon-rebuild-domains @ 9c93ad6
**Scope:** Phase 4 of shannon-rebuild plan. Wire 14+ hook scripts on top of Phase 2/3 scaffolding, add `plan-before-execute` + `context-threshold-warn` (the two missing per spec), apply `block-fab-files` scope/exemption fix from V6 update, build atomic install/uninstall + doctor-precheck, dry-run validate everything against `/tmp/shannon-test-v6` scaffold.

**Iron rule reminder:** NO live install was triggered. NO real CC `/plugin install`. All artifacts come from running real scripts against synthetic-but-real CC payload shapes piped via stdin — no mocks, no test files, no test frameworks.

---

## Hook inventory after Phase 4

`scripts/_validate-manifest.js` reports `hookScriptCount: 16` (14 spec'd + 2 Phase 2 bonus enforcers).

| # | Script | Event | Matcher | Origin |
|---|---|---|---|---|
| 1 | `session-context-inject.cjs` | SessionStart | startup\|resume\|clear\|compact | Phase 2 (covers spec's context-injector + skill-registry-cache merged) |
| 2 | `skill-activation-check.js` | UserPromptSubmit | * | Phase 2 |
| 3 | `block-fab-files.js` | PreToolUse | Write\|Edit\|MultiEdit | Phase 2 — **V6 SCOPING FIX applied this phase** |
| 4 | `read-before-edit.js` | PreToolUse | Edit\|MultiEdit | Phase 2 |
| 5 | `plan-before-execute.js` | PreToolUse | Write\|Edit\|MultiEdit | **NEW this phase — spec gap filled** |
| 6 | `evidence-gate-reminder.js` | PreToolUse | TaskUpdate | Phase 2 |
| 7 | `subagent-governance-inject.js` | PreToolUse | Task\|Agent | Phase 2 |
| 8 | `validation-not-compilation.js` | PostToolUse | Bash | Phase 2 |
| 9 | `validation-skill-tripwire.js` | PostToolUse | Bash | Phase 2 |
| 10 | `completion-claim-validator.js` | PostToolUse | Bash | Phase 2 bonus |
| 11 | `fab-pattern-detection.js` | PostToolUse | Edit\|Write\|MultiEdit | Phase 2 bonus |
| 12 | `evidence-quality-check.js` | PostToolUse | Edit\|Write\|MultiEdit | Phase 2 bonus |
| 13 | `task-list-tracker.js` | PostToolUse | TaskCreate\|TaskUpdate | Phase 2 |
| 14 | `hooks-fired-log.js` | PostToolUse | * | Phase 2 |
| 15 | `context-threshold-warn.js` | PostToolUse | * | **NEW this phase — spec gap filled** |
| 16 | `stop-task-semantics.js` | Stop | * | Phase 2 |

---

## V6 scope fix applied — block-fab-files

Before: matched any path containing `/tests/`, `*.test.*`, `*.spec.*`, etc. — false-positive blocked `scripts/validate.sh`, `modules/foo/scripts/run-tests.sh`, `docs/test-strategy.md`.

After: enforcement scoped to `src/`, `lib/`, `app/` subtrees. EXEMPTIONS for `scripts/`, `tools/`, `tests/` (top-level), `modules/*/scripts/`, `docs/`, `research/`, SKILL.md / AGENT.md / command .md / agent .md, and `e2e-evidence/`.

See `per-hook-firetest/block-fab--*` for 6 evidence scenarios proving the fix.

---

## Install / uninstall surface

| Script | New / Changed | Modes |
|---|---|---|
| `scripts/install.sh` | Extended this phase | `(default)`, `--dry-run`, `--auto`, `--resume-after-cc-install` |
| `scripts/setup.sh` | Phase 2 (unchanged) | idempotent marketplace declare |
| `scripts/uninstall.sh` | **NEW this phase** | `(default)`, `--dry-run`, `--purge-logs` |
| `scripts/uninstall-others.sh` | Extended this phase | `(default)`, `--dry-run` |
| `scripts/doctor-precheck.sh` | **NEW this phase** | `--target <path>`, `-v`, `--help` |

---

## Evidence catalog

### `per-hook-firetest/` — 29 scenarios, 1 dir per scenario, each containing `{stdout, stderr, exit}`

`firetest.sh` (copied to evidence root) pipes synthetic CC payloads to each hook. Asserted behavior:

**block-fab-files** (6 scenarios)
- `block-fab--app-test-file-blocks` — exit 2 ✓ (V6 scope: matches `*.test.*` in active scope)
- `block-fab--scripts-allowed` — exit 0 ✓ (V6 fix: scripts/ exempted)
- `block-fab--app-src-clean-allowed` — exit 0 ✓
- `block-fab--src-spec-blocks` — exit 2 ✓
- `block-fab--docs-allowed` — exit 0 ✓ (V6 fix: docs/ exempted)
- `block-fab--module-scripts-allowed` — exit 0 ✓ (V6 fix: modules/*/scripts/ exempted)

**read-before-edit** — exit 0 + stderr advisory ✓

**plan-before-execute** (NEW)
- `plan-before-execute--no-fresh-plan-warns` — exit 2 + stderr ✓
- `plan-before-execute--outside-scope-silent` — exit 0 (docs/ outside scope) ✓

**evidence-gate-reminder**
- `evidence-gate--task-completed-emits-checklist` — exit 2 + 5-question checklist ✓
- `evidence-gate--task-in-progress-silent` — exit 0 ✓

**validation-not-compilation**
- `validation-not-compilation--build-success-warns` — exit 2 ✓
- `validation-not-compilation--unrelated-bash-silent` — exit 0 ✓

**validation-skill-tripwire**
- `validation-skill-tripwire--build-without-validation-fires` — exit 2 + tripwires.jsonl appended ✓ (see `firetest-tripwires.jsonl`)

**completion-claim-validator**
- `completion-claim--it-works-warns` — exit 2 ✓
- `completion-claim--neutral-output-silent` — exit 0 ✓

**task-list-tracker**
- `task-tracker--create-appends` — exit 0 ✓ (open-tasks.txt appended)
- `task-tracker--completed-removes` — exit 0 ✓ (open-tasks.txt removed)

**subagent-governance-inject** — always exit 2 + IRON RULE in stderr ✓

**hooks-fired-log** — passive exit 0 ✓ (appends to hooks.jsonl, see `firetest-hooks.jsonl`)

**context-threshold-warn** (NEW)
- `context-threshold--no-session-silent` — exit 0 ✓ (no CLAUDE_SESSION_ID env)

**skill-activation-check**
- `skill-activation--prompt-no-match-silent` — exit 0 ✓

**stop-task-semantics**
- `stop-semantics--mid-action-blocks` — exit 2 (pre-seeded open-tasks.txt + "let me also" phrasing) ✓
- `stop-semantics--neutral-text-allows` — exit 0 ✓

**fab-pattern-detection**
- `fab-pattern--jest-fn-warns` — exit 2 ✓
- `fab-pattern--clean-allows` — exit 0 ✓

**evidence-quality-check**
- `evidence-quality--empty-warns` — exit 2 ✓
- `evidence-quality--nonempty-allows` — exit 0 ✓

**session-context-inject.cjs**
- `session-context-inject--runs` — exit 0 ✓

### `crash-tests/` — 16 hooks × 3 malformed payloads = 48 scenarios

Per-hook subdir with `{empty, invalid, null-input}.{stdout, stderr, exit}`.

Result: every hook except `subagent-governance-inject.js` (which always exits 2 by design — injects IRON RULE) exits 0 on malformed input. `hook-errors.jsonl` empty (no handler crashes) — `lib/hook-runner.js` try/catch swallows every error and exits 0, never breaking the CC tool flow.

### `install-tests/`

- `install-dry-run.{stdout,stderr}` — `scripts/install.sh --dry-run` Phase 1 → exit 0, no mutations
- `install-dry-run-resume.{stdout,stderr}` — `--dry-run --resume-after-cc-install` → exit 0, would call doctor-precheck (and skip)
- `uninstall-others-dry-run.{stdout,stderr}` — lists all 16 plugins; exit 0
- `uninstall-dry-run.{stdout,stderr}` — Shannon self-uninstall plan; exit 0

### `doctor-tests/`

- `doctor-precheck-tmp.{stdout,stderr}` — `--target /tmp/shannon-test-v6 -v`
- Result: **PASS 11 / FAIL 1**. Only fail = `marketplace-declared` (extraKnownMarketplaces.shannon-local missing in live settings.json) — expected because live setup.sh was NOT run per spec instruction. Plugin layout, JSON validity, hook script presence + executability, log dir writability all PASS.

### Top-level

- `manifest-validation.json` — `_validate-manifest.js` output: 16 hookScripts, 0 errors, ok=true
- `firetest.sh` — harness script (copy of `/tmp/shannon-test-v6/scripts/firetest.sh`)
- `crash-test.sh` — crash-test harness
- `firetest-hooks.jsonl` — full hooks.jsonl trace from firetest run (~29 fire events, all <50ms)
- `firetest-tripwires.jsonl` — 1 tripwire: `build-success-without-validation` correctly fired

---

## Validation summary

| Gate | Result | Citation |
|---|---|---|
| All hook scripts declared in hooks.json exist | PASS | `manifest-validation.json` |
| All 16 hooks accept synthetic payload | PASS | `per-hook-firetest/*/exit` |
| `block-fab-files` V6 scope fix correct | PASS | 6 firetest scenarios |
| New `plan-before-execute` works in scope | PASS | `per-hook-firetest/plan-before-execute--*` |
| New `context-threshold-warn` passive-allow | PASS | `per-hook-firetest/context-threshold--*` |
| Hooks never crash CC tool flow on malformed input | PASS | `crash-tests/*/*.exit` (16 × 3 = 48) |
| Tripwires log appended on build-without-validation | PASS | `firetest-tripwires.jsonl` |
| Task tracker maintains open-tasks.txt | PASS | task-tracker--create-appends + task-tracker--completed-removes |
| `install.sh --dry-run` exits 0 mutating nothing | PASS | `install-tests/install-dry-run.*` |
| `uninstall-others.sh --dry-run` exits 0 listing 16 plugins | PASS | `install-tests/uninstall-others-dry-run.stdout` |
| `uninstall.sh --dry-run` exits 0 | PASS | `install-tests/uninstall-dry-run.*` |
| `doctor-precheck.sh` correctly finds + flags state | PASS | `doctor-tests/doctor-precheck-tmp.stdout` (11/12) |

---

## What was NOT done (intentionally — spec instruction)

- **NO live install.** `scripts/install.sh` was NOT executed without `--dry-run`.
- **NO `/plugin install shannon@shannon-local`** triggered in live CC.
- **NO live `uninstall-others.sh`** that would disable OMC / VF / Crucible.
- **NO commits or pushes** to the worktree branch beyond Phase 4 changes (next: lead reviews evidence + runs the install scripts from terminal).

This is by design per the task spec: "Phase 4 = ready the gun, NOT pull the trigger."

---

## Files changed this phase

```
hooks/block-fab-files.js                       — V6 scoping + exemptions
hooks/plan-before-execute.js                   — NEW
hooks/context-threshold-warn.js                — NEW
hooks/hooks.json                               — register 2 new hooks
scripts/install.sh                             — atomic 2-phase + --dry-run + --auto
scripts/uninstall.sh                           — NEW (Shannon self-remove + --dry-run)
scripts/uninstall-others.sh                    — added --dry-run
scripts/doctor-precheck.sh                     — NEW
```

## Status

**READY FOR LIVE TRIGGER.** Lead may now run `scripts/install.sh` from terminal to execute the actual `/plugin install` + `uninstall-others.sh` sequence after reviewing this evidence.
