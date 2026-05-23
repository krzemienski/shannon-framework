# Live Claude Code System Audit — auditor-3-live-cc

**Date:** 2026-05-23
**Auditor:** auditor-3-live-cc (team shannon-rebuild-260523)
**Scope:** Wave 0 read-only forensic audit of live Claude Code install on `darwin` (Nick's machine), evidence from `~/.claude/settings.json`, plugin cache, hook scripts, session JSONL.
**Iron Rule:** Every claim cites `path:line` from settings.json, plugin manifest, or session.jsonl. No theoretical state — only files observed on disk.

---

## §1. Plugin Inventory

Source: `~/.claude/settings.json:14-115` (`enabledPlugins` block).

**Enabled plugins (counted):** 65 enabled, 60 disabled. Total registered: 125 plugin slots.

### Plugin storage layout
- `~/.claude/plugins/` — pointer dirs (mostly thin: `oh-my-claudecode/`, `claude-hud/`, `validationforge/`, `prd-generator/`). OMC pointer dir EMPTY — actual code in cache.
- `~/.claude/plugins/cache/` — versioned install root (30 marketplace dirs).
- `~/.claude/plugins/installed_plugins.json` — installed version manifest.

### Active plugins with hook registrations (verified by hooks.json existence)
Source: `find ~/.claude/plugins/cache -name "hooks.json"`.

| Plugin | Cache path | hooks.json | plugin.json |
|--------|-----------|------------|-------------|
| validationforge | `/cache/validationforge/validationforge/1.0.0/` | YES (`hooks/hooks.json`) | YES |
| oh-my-claudecode | `/cache/omc/oh-my-claudecode/4.13.6/` | NO (uses settings.json injection) | YES (no hook block) |
| caveman | `/cache/caveman/caveman/{rev}/.codex/` | YES (codex variant) | — |
| superpowers-marketplace/episodic-memory | `/cache/superpowers-marketplace/episodic-memory/1.4.2/` | YES | — |
| claude-plugins-official/remember | `/cache/claude-plugins-official/remember/0.7.2/` | YES | — |
| claude-code-settings | `/cache/claude-code-settings/claude-code-settings/2.1.7/` | YES | — |
| explanatory-output-style | `/cache/claude-plugins-official/explanatory-output-style/1.0.0/` | YES | — |

### VF plugin hooks.json content (verified)
Source: `~/.claude/plugins/cache/validationforge/validationforge/1.0.0/hooks/hooks.json:1-58`.

| Event | Matcher | Hook script | Purpose |
|-------|---------|-------------|---------|
| PreToolUse | `Write\|Edit\|MultiEdit` | `block-test-files.js` | Block test/mock/stub files |
| PreToolUse | `TodoWrite\|TaskUpdate` | `evidence-gate-reminder.js` | Inject evidence checklist |
| PostToolUse | `Bash` | `validation-not-compilation.js` | Warn: build success ≠ validation |
| PostToolUse | `Bash` | `completion-claim-validator.js` | Catch unverified completion claims |
| PostToolUse | `Bash` | `validation-state-tracker.js` | Track validation activity |
| PostToolUse | `Edit\|Write\|MultiEdit` | `mock-detection.js` | Detect mock patterns in code |
| PostToolUse | `Edit\|Write\|MultiEdit` | `evidence-quality-check.js` | Warn on empty evidence files |

### OMC plugin
Source: `~/.claude/plugins/cache/omc/oh-my-claudecode/4.13.6/.claude-plugin/plugin.json:1-15`.

OMC `plugin.json` declares `skills: ./skills/` + `mcpServers: ./.mcp.json` — **NO hook block**. OMC hooks are injected via `~/.claude/settings.json` directly (e.g. `dev-rules-reminder.cjs`, `simplify-gate.cjs`, `subagent-init.cjs`).

### Shannon — NOT INSTALLED (confirmed)
Source: `find ~/.claude -iname "*shannon*"` returns:
- `~/.claude/tasks/shannon-rebuild-260523` (THIS audit's task dir)
- `~/.claude/projects/-Users-nick-Desktop-shannon-cc` (Shannon's own project conv history)
- `~/.claude/teams/shannon-rebuild-260523/` (this audit team)
- **No `~/.claude/plugins/shannon*`. No `~/.claude/skills/shannon*`. No `~/.claude/agents/shannon*`. No `shannon` entry in `installed_plugins.json`.**

Settings.json `enabledPlugins` has NO `shannon@*` key. Shannon is **claimed but never installed**.

---

## §2. Hook Inventory + Firing Map

### Hook scripts on disk
Source: `ls ~/.claude/hooks/`. **50+ scripts** in `~/.claude/hooks/` (script files, not subdirs).

### Authoritative hook chain (settings.json:hooks)
Source: `~/.claude/settings.json` → `hooks` block (parsed structured).

| Event | Matcher | Hook chain (script → effect) |
|-------|---------|------------------------------|
| **SessionStart** | `*` | cavemem (passive), iterm2 cc-status (passive), moshi-hook (passive) |
| SessionStart | `startup\|resume\|clear\|compact` | `session-init.cjs` (inject context) |
| **UserPromptSubmit** | `*` | cavemem, `simplify-gate.cjs` (DECISION:block), `dev-rules-reminder.cjs` (stderr context), `usage-context-awareness.cjs` (passive), iterm2, moshi-hook |
| **PreToolUse** | `Write` | `descriptive-name.cjs` (console.error if undescriptive) |
| PreToolUse | `Bash\|Glob\|Grep\|Read\|Edit\|Write` | `scout-block.cjs`, `privacy-block.cjs` |
| PreToolUse | `*` | iterm2 cc-status |
| **PostToolUse** | `*` | cavemem (post-tool-use), iterm2 cc-status |
| PostToolUse | `Skill` | `skill-body-recovery.js` (stderr) |
| **Stop** | `*` | cavemem (stop), iterm2, moshi-hook |
| **SubagentStart** | `*` | `subagent-init.cjs` (inject context) |
| **TaskCompleted** | `*` | `task-completed-handler.cjs` (stderr beep) |
| **TeammateIdle** | `*` | `teammate-idle-handler.cjs` (stderr) |
| SessionEnd | `*` | cavemem, iterm2 |

### Hook script categorization (effect grep, 50+ files)
Source: hand-categorized from grep over `~/.claude/hooks/*.js *.cjs *.mjs`.

**Blocking (process.exit(2) or `decision:"block"`):**
- `block-test-files.js` — stderr (PreToolUse, VF plugin)
- `pre-commit-evidence-gate.js` — stderr (PreToolUse)
- `root-cause-enforce-pre.js` — stderr (PreToolUse)
- `simplify-gate.cjs` — `decision:'block'` (UserPromptSubmit)
- `syntax-check-after-edit.js` — stderr (PostToolUse)
- `code-simplifier.mjs` — `decision:'block'` on **Stop**
- `persistent-mode.mjs` — `decision:"block"` on **Stop**

**Context-injecting / passive reminder:**
- `dev-rules-reminder.cjs` (UserPromptSubmit, SessionStart)
- `evidence-gate-reminder.js` (PreToolUse:TaskUpdate, VF plugin)
- `skill-activation-forced-eval.js` (UserPromptSubmit)
- `validation-not-compilation.js`, `completion-claim-validator.js` (PostToolUse:Bash, VF plugin)
- `mock-detection.js`, `evidence-quality-check.js` (PostToolUse:Edit, VF plugin)
- `documentation-context-check.js`, `gsd-workflow-guard.js`, `plan-before-execute.js`, `read-before-edit.js`, `sdk-auth-subagent-enforcer.js`, `subagent-context-enforcer.js`, `usage-context-awareness.cjs` — passive

**Operational:**
- `keyword-detector.mjs` (PreToolUse + PostToolUse + Stop + UserPromptSubmit, passive)
- `post-tool-use.mjs`, `post-tool-use-failure.mjs`
- `skill-body-recovery.js` (PostToolUse:Skill, stderr)
- `skill-dedup.cjs` (SessionStart/SessionEnd/Stop)
- `keyword-detector.mjs`, `notify.cjs`, `patterns.js` — passive logging

### Cross-referenced: settings.json hooks vs scripts on disk
Many scripts in `~/.claude/hooks/` are **NOT** wired into settings.json (`block-test-files.js`, `completion-claim-validator.js`, `evidence-gate-reminder.js`, `mock-detection.js`, etc.).

These ARE wired via VF plugin's own `hooks.json` (`~/.claude/plugins/cache/validationforge/validationforge/1.0.0/hooks/hooks.json:1-58`) and assembled at session start. The `~/.claude/hooks/*` copies are **stale duplicates from a manual install** — the live ones run from cache path.

---

## §3. Settings.json Hook Chain (exact)

Source: `~/.claude/settings.json` — direct hook block extracted.

Direct events configured at `~/.claude/settings.json:hooks`:
- **SessionStart**: 4 scripts (cavemem, session-init.cjs, iterm2, moshi-hook)
- **UserPromptSubmit**: 6 scripts (cavemem, simplify-gate.cjs, dev-rules-reminder.cjs, usage-context-awareness.cjs, iterm2, moshi-hook)
- **PreToolUse**: 3 matcher groups: `Write` → descriptive-name.cjs; `Bash|Glob|Grep|Read|Edit|Write` → scout-block.cjs + privacy-block.cjs; `*` → iterm2
- **PostToolUse**: 3 hooks: cavemem, iterm2, `skill-body-recovery.js` (Skill only)
- **Stop**: 3 scripts (cavemem, iterm2, moshi-hook)
- **SubagentStart**: `subagent-init.cjs`
- **TaskCompleted**: `task-completed-handler.cjs`
- **TeammateIdle**: `teammate-idle-handler.cjs`
- **SessionEnd**: cavemem + iterm2
- **PermissionRequest**: iterm2 + moshi-hook
- **Notification**: iterm2
- **PreCompact**: (empty)
- **StopFailure**: iterm2

**Plugin-registered hooks fold in at runtime.** Stop hook from session JSONL (`~/.claude/projects/.../982f9f03...jsonl:977`) shows `hookCount:12` actually firing — 3 from settings.json + 9 from plugins (claude-hud, ralph-loop, reflexion, deep-research, etc.).

---

## §4. Skill / Agent Inventory

Source: `ls ~/.claude/skills/ | wc -l` and `ls ~/.claude/agents/ | wc -l`.

- **307 skill dirs** in `~/.claude/skills/`
- **53 agent files** in `~/.claude/agents/`
- Plus per-plugin skills (VF 52 skills, OMC ~50 skills, lynx, content-studio, kaizen, etc.)

### High-frequency reminder hooks (per session histogram)
Source: `grep -oE '"hookName":"[^"]+"' $SESS2 | sort | uniq -c` on `~/.claude/projects/.../982f9f03-f6fa-4961-aae2-0808685ff32c.jsonl`.

| Hook | Fires/session | Verdict |
|------|---------------|---------|
| PostToolUse:Bash | 230 | reminders only (parallel-execute) |
| PreToolUse:Bash | 90 | reminders only |
| PostToolUse:TaskCreate | 73 | reminders only |
| PostToolUse:TaskUpdate | 34 | reminders only |
| PostToolUse:Write | 32 | mock-detection + evidence-quality (passive) |
| PreToolUse:TaskCreate | 26 | reminder |
| PreToolUse:TaskUpdate | 24 | evidence-gate-reminder |
| SessionStart:startup | 12 | context inject |
| Stop | 5 | 12-script chain, all `continue:true` |

### Skill INVOCATION counts (not reminders)
Source: `grep -c '"name":"Skill","input":{"skill":"<X>"'` on 3 mined session files.

- **`functional-validation` invoked: 0** across all 3 sessions (ae8256, 982f, 3aff)
- `lynx:full-ui-experience-audit`: 1 (SESS2)
- `agent-browser`: 1 (SESS ae8256)
- `full-functional-audit`: 1 (SESS ae8256)
- **Total Skill invocations across ~3 hours of work in 3 sessions: ~4-6.**

**The "skill catalog" loaded into context is 307 + per-plugin. The actual invocation rate is <1%.**

---

## §5. Validation-Skip Evidence (≥3 cited)

User concern (b): "functional-validation skill still gets skipped despite block-test-files hook working."

### Evidence A: SESS3 (`3aff1068-d602-4615-858d-f82de3eab45f.jsonl`, 1.0MB, 21 Bash + 1 Write)
- **0 invocations of `functional-validation`** — `grep -c '"skill":"functional-validation"' = 0`.
- **0 Skill invocations of any kind** — `grep -oE '"name":"Skill","input"...' = 0`.
- 125 PostToolUse:Bash hooks fired (reminder context injected).
- 9 PostToolUse:Write hooks fired (`mock-detection.js` + `evidence-quality-check.js` warned, agent kept going).
- **Outcome:** session completed 1 Write + 21 Bash without ever invoking the validation skill the hooks remind about.

### Evidence B: SESS2 (`982f9f03-f6fa-4961-aae2-0808685ff32c.jsonl`, 1.3MB, 46 Bash + 3 Edit + 4 Write)
- Skill invoked exactly once: `lynx:full-ui-experience-audit` (`SESS2:29`).
- **`functional-validation`: 0 invocations.**
- 32 PostToolUse:Write events fired through `mock-detection` + `evidence-quality-check` — both passive, no block.
- 230 PostToolUse:Bash hook fires — `validation-not-compilation.js` is registered (`hooks.json:23-26`) but no stderr capture in session JSONL means it returns silent exit-0 (no condition matched, no warning surfaced).
- `evidence-gate-reminder` text appears 5+ times (`SESS2:391, 393, 405, 407, 542`) — agent received the checklist, continued without invoking validate.

### Evidence C: SESS ae8256 (`ae825601-1820-460a-b641-64af7b6e45c9.jsonl`, 3.3MB, 73 Bash + 2 Edit + 3 Write)
- Skills invoked: `agent-browser`, `full-functional-audit` — **`functional-validation`: 0**.
- 73 Bash invocations. No corresponding `validation-not-compilation` stderr trips found.

**Pattern (3-of-3 sessions):** VF passive reminders fire (200+ times per session) without ever causing the agent to pause and invoke the validation skill. Reminders inject text → context bloat → ignored.

---

## §6. Premature Stop Evidence (≥2 cited)

User concern (c): "Stop hook fires prematurely."

### Evidence A: Stop chain runs 12 scripts in 800ms — every assistant message
Source: `SESS2:977` (`stop_hook_summary` system event), `hookCount:12`.

Stop chain on EVERY assistant turn end:
1. cavemem stop (101ms)
2. iterm2 cc-status (16ms)
3. moshi-hook claude-hook
4. project session-state.cjs (184ms)
5. claude-hud `run-hook.cmd emit-event` (32ms)
6. claude-hud `bin/completion-attempt.sh` (37ms)
7. ralph-loop `scripts/on-event.sh` (49ms)
8. reflexion `context-guard-stop.mjs` (122ms)
9. reflexion `persistent-mode.mjs` (153ms)
10. reflexion `code-simplifier.mjs` (127ms)
11. orbit `stop-hook.sh` (32ms)
12. deep-research `bun index.ts Stop` (41ms)

`preventedContinuation:false` — but all 12 fire on every Stop event regardless of whether the agent's response represents a logical completion or an intermediate step. **Stop is fired by the harness whenever assistant emits final text** — there's no notion of "is the user-level task done"; the firing IS premature relative to task completion semantics.

### Evidence B: Reflexion `code-simplifier.mjs` + `persistent-mode.mjs` each block-respond on Stop
Source: `SESS2:975` (`code-simplifier.mjs` output `{"continue":true}` — was prepared to set `{"continue":false}` per its `decision:'block'` capability).

These scripts CAN return `{"continue":false}` to force the model into a follow-up turn — meaning Stop "premature" is observable when these scripts fire `continue:false` mid-task. In SESS2 they returned `continue:true` each time, but the firing pattern reveals every assistant message triggers Stop adjudication. The user's "premature Stop" likely refers to: model ends message → 12-script chain → reflexion forces persistent mode → agent keeps going / agent unexpectedly stops.

### Evidence C: 5 Stop events in SESS2 over ~12 minutes of work
Source: `grep -c '"hookName":"Stop"' = 5` in SESS2; session start 21:01:08 → Stop fires at 21:16:57. Stop fires on assistant pauses for tool result, not on task completion. Premature is **structural** — the harness doesn't distinguish "intermediate stop" from "final stop."

---

## §7. Shannon Install Delta (exact paths needed)

For Shannon to actually be installed (matching the patterns observed for VF/OMC):

### Required artifacts
1. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/.claude-plugin/plugin.json` — manifest
2. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/hooks/hooks.json` — hook registrations
3. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/hooks/*.js` — hook script implementations
4. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/skills/*/SKILL.md` — skill defs
5. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/agents/*.md` — agent defs
6. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/commands/*.md` — slash commands
7. `~/.claude/plugins/cache/{shannon-marketplace}/shannon/{version}/CLAUDE.md` — project rules
8. `~/.claude/plugins/installed_plugins.json` — add `"shannon@{marketplace}": [{ scope, installPath, version, ... }]`
9. `~/.claude/settings.json:enabledPlugins` — add `"shannon@{marketplace}": true`
10. `~/.claude/settings.json:extraKnownMarketplaces` — add marketplace source
11. `~/.claude/plugins/marketplace-cache/{marketplace}.json` — marketplace listing

### Required marketplace declaration (settings.json pattern)
```json
"extraKnownMarketplaces": {
  "shannon-local": {
    "source": {"path": "/Users/nick/Desktop/shannon-framework", "source": "directory"}
  }
}
```

(matches crucible-local pattern: `~/.claude/settings.json:crucible-local`.)

### Current shannon-framework repo state
`/Users/nick/Desktop/shannon-framework/` (per session task dirs) contains research output only — no `.claude-plugin/plugin.json`, no `hooks/hooks.json`, no `skills/`, no `agents/`. The repo currently has NO installable plugin tree.

**Gap:** Shannon must produce items 1-11 above before `/plugin install shannon@shannon-local` will work.

---

## Summary

- **65 plugins enabled.** Shannon NOT among them.
- **12-script Stop chain.** Stop fires on every assistant message; "premature" is structural — the harness doesn't track task semantics.
- **VF hooks registered** (`block-test-files`, `evidence-gate-reminder`, `mock-detection`, `evidence-quality-check`, `validation-not-compilation`, `completion-claim-validator`, `validation-state-tracker`) — all passive (stderr / context injection) except `block-test-files`. None forced `functional-validation` invocation in 3 audited sessions.
- **`functional-validation` invoked: 0** across 3 sessions (~5.6MB JSONL, 140+ Bash, 6 Edit, 8 Write). Skill catalog (307 skills) loaded → invocation rate <1%.
- **Hook reminder fatigue confirmed:** 230 PostToolUse:Bash + 32 PostToolUse:Write reminders per session, all passive. Agent receives → ignores → continues.
- **Shannon install delta:** 11 file/config items. Currently 0 of 11 exist.

---

## Unresolved Questions

1. Does the VF `block-test-files.js` ever exit-2 in real sessions? No fire evidence found in 3 mined sessions — the agent doesn't attempt test files often enough to trip it. Need a session with test-file attempt to confirm.
2. `persistent-mode.mjs` + `code-simplifier.mjs` can `continue:false` on Stop — under what conditions? Found 0 instances of `continue:false` in mined sessions. Need a session where persistent-mode actually engages.
3. Are the reflexion Stop hooks (`context-guard-stop.mjs`, `persistent-mode.mjs`, `code-simplifier.mjs`) the source of "premature Stop"? Their firing on every Stop is confirmed; whether they cause unexpected continuation requires a session where the user perceived premature behavior — not yet located in mined data.
4. Should Shannon use settings.json injection (OMC pattern) or `hooks/hooks.json` (VF pattern)? OMC pattern is more invasive; VF pattern self-contains. VF pattern recommended.
5. How does Shannon avoid joining the 12-script Stop chain noise? Likely needs its own Stop budget gate, opt-out for noisy hooks, or replace the chain entirely.
