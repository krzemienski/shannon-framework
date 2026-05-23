# SHANNON-V6-HOOKS.md — Hook Script Surface

**Status:** LOCKED 2026-05-23
**Contract:** All hooks use CC convention (stderr write + exit 2). Per-hook try/catch → `process.exit(0)` on crash + log to `~/.claude/logs/shannon/hook-errors.jsonl`.

---

## Hook Loadout (14 scripts)

### HookLayer (5 hooks — tool-boundary enforcement)

| # | Script | CC Event | Matcher | Replaces | Behavior |
|---|---|---|---|---|---|
| 1 | block-fab-files.js | PreToolUse | `Write\|Edit\|MultiEdit` | VF block-test-files.js, lynx mock-detection (Write phase) | 12-regex pattern detector (post-16 §4.2 canonical); blocks fake/stub/mock/fixture/test files; stderr + exit 2 |
| 2 | read-before-edit.js | PreToolUse | `Edit\|MultiEdit` | (no existing equivalent; post-07 §4.3 pattern) | tracks Read events via module-level Set; on Edit-without-prior-Read → stderr WARNING + exit 2 (inject mode) |
| 3 | validation-not-compilation.js | PostToolUse | `Bash` | VF validation-not-compilation.js (absorbed verbatim) | matches BUILD_COMMANDS + SUCCESS_INDICATORS; reminds build success ≠ functional validation; stderr + exit 2 |
| 4 | evidence-gate-reminder.js | PreToolUse | `TaskUpdate` | VF evidence-gate-reminder.js (absorbed verbatim) | TaskUpdate with status:completed → stderr 5-question checklist + exit 2 |
| 5 | mock-detection.js | PostToolUse | `Edit\|Write\|MultiEdit` | VF mock-detection.js (absorbed) | scans written content for mock-pattern hints; stderr warning + exit 2 |

### InvocationLayer (2 hooks)

| # | Script | CC Event | Matcher | Replaces | Behavior |
|---|---|---|---|---|---|
| 6 | skill-activation-check.js | UserPromptSubmit | `*` | OMC skill-activation-forced-eval.js | reads cached skill triggers (logs/shannon/skill-triggers.json from SessionStart); regex-matches prompt against triggers; emits stderr hints; exit 2 |
| 7 | validation-skill-tripwire.js | PostToolUse | `Bash` | NEW (addresses user concern a) | after Bash build-success: if functional-validation skill NOT invoked since last build → stderr TRIPWIRE + append to logs/shannon/tripwires.jsonl + exit 2 |

### DispatchLayer (3 hooks)

| # | Script | CC Event | Matcher | Replaces | Behavior |
|---|---|---|---|---|---|
| 8 | subagent-governance-inject.js | PreToolUse | `Task\|Agent` | OMC subagent-init.cjs, sdk-auth-subagent-enforcer.js | append IRON-RULE block (no-fakes / evidence-gated / read-before-edit) to subagent prompt via stderr + exit 2 (inject) |
| 9 | stop-task-semantics.js | Stop | `*` | NEW (addresses user concern b — premature Stop); replaces nothing (additive but Shannon-only Stop registration) | reads logs/shannon/open-tasks.txt; if open tasks + last assistant message regex matches "let me / next I'll / now I'll" → exit 2 with stderr "Stop deferred" |
| 10 | task-list-tracker.js | PostToolUse | `TaskCreate\|TaskUpdate` | NEW (supports stop-task-semantics via UQ-V2-5 decision) | maintains logs/shannon/open-tasks.txt — appends on TaskCreate, removes on TaskUpdate status:completed/deleted |

### ContextLayer (1 hook)

| # | Script | CC Event | Matcher | Replaces | Behavior |
|---|---|---|---|---|---|
| 11 | session-context-inject.cjs | SessionStart | `startup\|resume\|clear\|compact` | OMC session-init.cjs, OMC dev-rules-reminder.cjs (partial), Crucible setup | reads global CLAUDE.md + project CLAUDE.md + .claude/rules/*.md; concatenates; writes to stdout (CC reads as <system-reminder>); ALSO writes logs/shannon/skill-triggers.json with cached skill-manifest triggers (consumed by skill-activation-check.js) |

### Observability (3 hooks — passive logging)

| # | Script | CC Event | Matcher | Replaces | Behavior |
|---|---|---|---|---|---|
| 12 | hooks-fired-log.js | PostToolUse | `*` | OMC keyword-detector.mjs (subset), post-tool-use.mjs | append-only log to logs/shannon/hooks.jsonl: {script, decision, matchedTool, ms, sessionId} per fire. Read by /shannon:doctor + /shannon:trace |
| 13 | completion-claim-validator.js | PostToolUse | `Bash` | VF completion-claim-validator.js (absorbed) | catches "build succeeded" claims without subsequent functional validation; stderr remind + exit 2 |
| 14 | evidence-quality-check.js | PostToolUse | `Edit\|Write\|MultiEdit` | VF evidence-quality-check.js (absorbed) | warns on empty (0-byte) evidence files in e2e-evidence/ paths; stderr + exit 2 |

---

## hooks.json Registration

`shannon-framework/hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|resume|clear|compact", "hooks": [
        { "type": "command", "command": "node hooks/session-context-inject.cjs" }
      ]}
    ],
    "UserPromptSubmit": [
      { "matcher": "*", "hooks": [
        { "type": "command", "command": "node hooks/skill-activation-check.js" }
      ]}
    ],
    "PreToolUse": [
      { "matcher": "Write|Edit|MultiEdit", "hooks": [
        { "type": "command", "command": "node hooks/block-fab-files.js" }
      ]},
      { "matcher": "Edit|MultiEdit", "hooks": [
        { "type": "command", "command": "node hooks/read-before-edit.js" }
      ]},
      { "matcher": "TaskUpdate", "hooks": [
        { "type": "command", "command": "node hooks/evidence-gate-reminder.js" }
      ]},
      { "matcher": "Task|Agent", "hooks": [
        { "type": "command", "command": "node hooks/subagent-governance-inject.js" }
      ]}
    ],
    "PostToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "command": "node hooks/validation-not-compilation.js" },
        { "type": "command", "command": "node hooks/validation-skill-tripwire.js" },
        { "type": "command", "command": "node hooks/completion-claim-validator.js" }
      ]},
      { "matcher": "Edit|Write|MultiEdit", "hooks": [
        { "type": "command", "command": "node hooks/mock-detection.js" },
        { "type": "command", "command": "node hooks/evidence-quality-check.js" }
      ]},
      { "matcher": "TaskCreate|TaskUpdate", "hooks": [
        { "type": "command", "command": "node hooks/task-list-tracker.js" }
      ]},
      { "matcher": "*", "hooks": [
        { "type": "command", "command": "node hooks/hooks-fired-log.js" }
      ]}
    ],
    "Stop": [
      { "matcher": "*", "hooks": [
        { "type": "command", "command": "node hooks/stop-task-semantics.js" }
      ]}
    ]
  }
}
```

---

## Common Library (lib/hook-runner.js)

All 14 scripts import a shared runner:

```js
// lib/hook-runner.js
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(process.env.HOME, '.claude/logs/shannon');
const HOOK_ERR = path.join(LOG_DIR, 'hook-errors.jsonl');

function logFire(record) {
  try {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(path.join(LOG_DIR, 'hooks.jsonl'), JSON.stringify(record) + '\n');
  } catch (_) { /* silent — never break parent */ }
}

function logError(scriptName, err) {
  try {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(HOOK_ERR, JSON.stringify({
      ts: new Date().toISOString(),
      script: scriptName,
      error: String(err),
      stack: err && err.stack,
    }) + '\n');
  } catch (_) { /* silent */ }
}

function runHook(scriptName, handler) {
  const start = Date.now();
  let payload = {};
  try {
    const stdinBuf = fs.readFileSync(0, 'utf-8');
    payload = stdinBuf ? JSON.parse(stdinBuf) : {};
  } catch (_) {
    payload = {};
  }

  let result = { decision: 'allow', exitCode: 0 };
  try {
    result = handler(payload) || result;
  } catch (err) {
    logError(scriptName, err);
    process.exit(0);
    return;
  }

  const elapsed = Date.now() - start;
  logFire({
    ts: new Date().toISOString(),
    script: scriptName,
    matchedTool: payload.tool || payload.event || null,
    decision: result.decision || 'allow',
    ms: elapsed,
    sessionId: process.env.CLAUDE_SESSION_ID || null,
  });

  if (result.stderrPayload) {
    process.stderr.write(result.stderrPayload);
  }
  process.exit(result.exitCode || 0);
}

module.exports = { runHook };
```

Every hook script ends with `runHook('script-name', handlerFn)`. Centralized log + error + budget + payload parsing — KISS.

---

## Replaces Map (which existing hook scripts die)

### Killed: OMC settings.json hook chain (8 scripts inherited)
- session-init.cjs → absorbed by session-context-inject.cjs
- dev-rules-reminder.cjs → absorbed by session-context-inject.cjs
- simplify-gate.cjs → DROPPED (was OMC-specific; not a v6 concern)
- usage-context-awareness.cjs → DROPPED
- descriptive-name.cjs → DROPPED
- scout-block.cjs → DROPPED (was Lynx; not v6)
- privacy-block.cjs → DROPPED
- subagent-init.cjs → absorbed by subagent-governance-inject.js

### Killed: VF hooks/hooks.json chain (7 scripts inherited)
- block-test-files.js → renamed block-fab-files.js (same behavior)
- evidence-gate-reminder.js → absorbed verbatim
- validation-not-compilation.js → absorbed verbatim
- completion-claim-validator.js → absorbed verbatim
- validation-state-tracker.js → DROPPED (overlaps hooks-fired-log.js)
- mock-detection.js → absorbed verbatim
- evidence-quality-check.js → absorbed verbatim

### Killed: Crucible hooks/hooks.json
- (Crucible relies on settings.json plus per-skill enforcement — no standalone hooks)
- /Users/nick/Desktop/crucible/crucible-plugin/hooks/hooks.json: 1 file only; behavior absorbed by Shannon's completion-gate skill + evidence-gate-reminder.js

### Killed: Reflexion hooks
- context-guard-stop.mjs → DROPPED (Shannon stop-task-semantics.js owns Stop)
- persistent-mode.mjs → DROPPED (was Reflexion's loop force; Shannon /shannon:loop owns that pattern)
- code-simplifier.mjs → DROPPED

### Killed: HUD hooks (none — HUD has no hooks block, just statusline TS)

### Killed: anneal hooks (3 plugins × hooks/)
- All anneal hook scripts → DROPPED. anneal's intelligence lives in skills + agents; v6 absorbs the skills. Hook layer simplified to Shannon's 14.

### Killed: claude-hud Stop chain participants (12 scripts from auditor-3 §6)
- cavemem stop, iterm2 cc-status, moshi-hook claude-hook, project session-state.cjs, run-hook.cmd emit-event, completion-attempt.sh, ralph-loop on-event.sh, reflexion context-guard-stop.mjs, reflexion persistent-mode.mjs, reflexion code-simplifier.mjs, orbit stop-hook.sh, deep-research bun index.ts Stop
- All → DROPPED if their parent plugin is uninstalled per §1 of ARCHITECTURE. Shannon's stop-task-semantics.js is the ONLY Stop hook in v6.

---

## Hook Performance Budget

- Target: <100ms wall clock per fire (post-16 §6.8 promise).
- Hard cap: 500ms (hook killed if exceeds).
- Total per-event budget: 500ms (sum of all Shannon hooks on that event).
  - PostToolUse:Bash has 4 Shannon hooks (validation-not-compilation, validation-skill-tripwire, completion-claim-validator, hooks-fired-log) — 100ms each = 400ms budget.
- Async tolerated for PostToolUse only; everything else sync.
- No network calls in any hook script.

---

## Validation (Phase 5 per-hook validate.sh)

Each hook ships `layers/<layer-name>/validate.sh` exercising a fresh CC session against fixture input. PASS criteria:
- Hook fires (entry in hooks.jsonl).
- Hook returns correct exit code per fixture.
- stderr payload matches expected pattern.
- No entries in hook-errors.jsonl.

Three required gates (from v1 HANDOFF):
- G1: Hook wiring proof — all 14 hooks appear at least once in hooks.jsonl during real session.
- G2: validation-skill-tripwire fires after build-without-validate.
- G3: stop-task-semantics blocks premature Stop with open tasks.

---

## Unresolved Questions

- UQ-HOOK-1: Should hooks-fired-log.js fire on EVERY PostToolUse `*` matcher (high volume — 230+ fires per session per auditor-3) or be filtered? Recommendation: ship as-is; mitigations possible (size-based rotation of hooks.jsonl, sampling) come v6.1.
- UQ-HOOK-2: Does task-list-tracker.js write file via fs.appendFile (race-prone if hooks parallel) or via lockfile? Recommendation: simple appendFileSync; Shannon hooks are sequential per event, so race risk is negligible.
- UQ-HOOK-3: Should subagent-governance-inject.js inject FULL CLAUDE.md or just IRON-RULE block? Recommendation: IRON-RULE block only (smaller injection; full CLAUDE.md available via subagent's own SessionStart).

---

End of SHANNON-V6-HOOKS.md. 14 hooks shipping; 30+ existing hooks across consolidated plugins are replaced or dropped.
