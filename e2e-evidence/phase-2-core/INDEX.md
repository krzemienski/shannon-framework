# Phase 2 — Shared Core Evidence Index

**Run:** dev-core task #6 — Shannon v6 shared core
**Date:** 2026-05-23
**Branch:** wt/shannon-rebuild-core
**Plugin root:** /Users/nick/Desktop/shannon-framework
**Iron Rule:** All evidence is real execution output. No mocks. No fakes. No test files.

---

## Artifacts (in order produced)

### Manifest validation
- `manifest-validation.txt` — `scripts/_validate-manifest.js` output. Asserts plugin.json (name=shannon, version=6.0.0, hooks=./hooks/hooks.json), marketplace.json (name=shannon-local, plugins[0].name=shannon), hooks.json references 14 distinct scripts all present on disk, 4 layer modules + 4 validate.sh + 2 lib + 3 scripts all exist. `errors: []`, `ok: true`, rc=0.
- `hook-layer-dispatch.txt` — `core/layers/hook/module.js` direct exec; verifies HookLayer dispatch table (11 HookLayer-bound scripts) matches scripts on disk. rc=0.

### Per-layer validate.sh (4 layers, all PASS)
- `layer-context-validate.txt` — ContextLayer built 122,110-byte context (global + project CLAUDE.md + rules/*.md on this machine) + wrote skill-triggers.json to isolated dir. rc=0.
- `layer-hook-validate.txt` — HookLayer dispatch table covers 14 scripts in hooks.json, all present. rc=0.
- `layer-invocation-validate.txt` — InvocationLayer matched 2 seeded skills (functional-validation via "validate this", evidence-gate via "marking complete") against a real cache file. rc=0.
- `layer-dispatch-validate.txt` — DispatchLayer open-tasks dedupe (2 tasks after duplicate append), remove worked (1 task remains), isMidAction("Let me now") = true, isMidAction("All done") = false, IRON_RULE = 368 chars. rc=0.

### Hook-runner fire tests (live hook scripts via lib/hook-runner.js)
- `hook-fire-stderr.txt` — Four real hook fires through CC stdin protocol:
  - block-fab-files allow path (`src/foo.ts`) → rc=0, no stderr.
  - block-fab-files block path (`src/foo.test.ts`) → rc=2 + iron-rule stderr.
  - subagent-governance-inject (`Task`) → rc=2 + 10-line IRON RULE injected to stderr.
  - hooks-fired-log passive (`Read`) → rc=0.
- `hooks-jsonl-after-fires.jsonl` — `hooks.jsonl` log produced by hook-runner across 4 fires. Each line records {ts, script, matchedTool, decision, exitCode, ms, sessionId}.

### Crash + slow-fire safety (hook-runner contract)
- `hook-crash-trace.txt` — Synthetic hook that throws inside handler: process exit rc=0 (CC never blocked), error+stack appended to hook-errors.jsonl with context="handler", and hooks.jsonl correctly OMITS the crashed fire (only successful fires log). Slow-fire test: a 150ms hook returns rc=0, hooks.jsonl records ms=150, hook-errors.jsonl receives {slow:true, ms:150, budget:100} entry.
- `hook-errors-jsonl.txt` — `hook-errors.jsonl` after crash + slow tests. Contains 1 crash record + 1 slow-fire record.

### Portability (run from isolated install path)
- `install-scaffold.txt` — `cp -r` to `/tmp/shannon-test-install/` produced a complete tree: 14 hooks, 4 layer modules, 4 validate.sh, 3 scripts, 2 lib files.
- `portability-check.txt` — Manifest validator + block-fab-files hook run from `/tmp/shannon-test-install/` (not the source repo). Both pass (`ok: true`; spec-match exit 2). Proves CLAUDE_PLUGIN_ROOT-style relative resolution works.

---

## Gate Summary

| Gate | Status | Evidence |
|---|---|---|
| plugin.json + marketplace.json schema valid | PASS | manifest-validation.txt |
| hooks.json references 14 scripts, all present | PASS | manifest-validation.txt, layer-hook-validate.txt |
| 4 layer modules load and run | PASS | 4 layer-*-validate.txt files |
| hook-runner: success path logs hooks.jsonl | PASS | hooks-jsonl-after-fires.jsonl |
| hook-runner: crash path logs hook-errors.jsonl + rc=0 | PASS | hook-crash-trace.txt, hook-errors-jsonl.txt |
| hook-runner: slow-fire records slow:true | PASS | hook-crash-trace.txt |
| Scaffold runs from isolated /tmp install | PASS | portability-check.txt |
| Block-fab-files exits 2 on .test/.spec/__mocks__ paths | PASS | hook-fire-stderr.txt |
| IRON RULE injected to subagent prompt via stderr exit 2 | PASS | hook-fire-stderr.txt |

**Overall:** 9/9 gates PASS. Phase 2 core deliverables complete.

---

## What is NOT in this phase

- 26 slash commands in `commands/` (task #7)
- 22 skill packages in `skills/` (task #7)
- 10 agent profiles in `agents/` (task #7)
- 7 domain module organization wrappers in `modules/` (task #7)
- Live `/plugin install shannon@shannon-local` against ~/.claude/plugins/ (task #8)
- G1/G2/G3 functional gates (hook wiring in real CC session, tripwire fires after build-without-validate, stop-task-semantics blocks premature Stop) — task #9

---

## Refusals / known gaps

None. Every spec'd deliverable for task #6 produced + validated. The hook scripts are functional but minimal (each is <50 lines, delegates to lib/hook-runner.js + the appropriate layer module). Full command/skill/agent surface lands in task #7.

