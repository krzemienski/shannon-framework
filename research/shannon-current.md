# Shannon-Framework Repo Audit — Current State (v5.6.1)

**Auditor:** auditor-2-shannon
**Date:** 2026-05-23
**Repo:** /Users/nick/Desktop/shannon-framework
**Verdict default:** rebuild needed. Most of repo = markdown prose claiming to be a framework. Real executable surface is small.

---

## 1. Repo Tree Summary

Top-level (19 dirs, 33 files):

```
shannon-framework/
├── .claude-plugin/        2 files — plugin.json (13 lines), marketplace.json (13 lines)
├── agents/                24 .md files — prose agent personas (WAVE_COORDINATOR, ANALYZER, ARCHITECT, BACKEND, ...)
├── commands/              23 .md files — slash command specs (spec, wave, prime, exec, do, ...)
├── core/                  10 .md files — 11,710 lines of behavioral prose
├── dashboard/             Vite+TS+Tailwind app (no purpose proven; not wired to hooks)
├── docs/                  v5.6/, analysis/, plans/, ref/, guides/ — release-note sprawl
├── e2e-evidence/          (empty/unread)
├── hooks/                 5 hook scripts + hooks.json + README + .pyc
├── modes/                 2 .md (SHANNON_INTEGRATION, WAVE_EXECUTION)
├── orchestration/         4 .py files — real code (630 lines)
├── research/              created by this audit
├── scripts/               README.md only (no scripts)
├── server/                websocket.py (364 lines) — websocket server, unclear consumer
├── skills/                42 skill dirs + README — each has SKILL.md (prose)
├── spec/                  empty
├── templates/             SKILL_TEMPLATE.md
└── tests/                 4 real test files (686 lines) + 14 .md verification docs + 6 sdk-examples

Root .md sprawl:
- 24 .md "release/audit" docs (CRITICAL_FIXES.md v2/v3, V5_*, INSTALLATION_VERIFIED_V5.4.md,
  V5.5_RELEASE_NOTES, V5_COMPLETION_CERTIFICATE.md, ...) — recursive self-congratulation
- 4 .sh: install_local.sh (900 lines), install_universal.sh (37KB), test_install.sh, test_universal_install.sh
- 2 .py: validate_shannon_v5.py (markdown-format validator), run_tests.py (pytest wrapper)
```

**Code-to-prose ratio:**
- Real Python code: ~1,400 lines (orchestration/ 630 + server/ 365 + hooks/ ~600 + tests/orchestration/ ~686)
- Prose markdown: 11,710 lines core/ + 24 agents × ~200 lines + 42 skills × ~300 lines + 23 commands × ~200 lines + 50+ root docs
- **Estimate: >95% prose, <5% executable.**

---

## 2. What Actually Executes

### Entry points (real)

**Install:**
- `install_local.sh` (900 lines) — copies files to `~/.claude/skills/shannon/`, `~/.claude/commands/shannon/`, `~/.claude/agents/shannon/`, `~/.claude/core/shannon/`, `~/.claude/modes/shannon/`, `~/.claude/templates/shannon/`, `~/.claude/hooks/shannon/`. Generates `~/.claude/hooks.json` with absolute paths to hook scripts. Embeds `using-shannon` SKILL.md content into a generated `session_start.sh` heredoc.
- `install_universal.sh` (37KB) — same but supports Cursor too.
- Plugin manifest exists (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`) but install_local.sh bypasses the plugin system and writes directly to `~/.claude/` namespaces.

**Hooks (5 real executables):**
- `hooks/user_prompt_submit.py:1` — UserPromptSubmit. Reads `.serena/north_star.txt`, `.serena/active_wave_status.txt`, injects them. Detects "large prompt" (>3000 chars) / "large file ref" (>5000 lines) / spec keywords → prints forced-reading-protocol prose to stdout. **No state, no logic, no enforcement — just print().**
- `hooks/post_tool_use.py:1` — PostToolUse Write/Edit. Regex-matches 13 fake-test patterns in test files. Returns `{"decision":"block"}` JSON if found. **Real enforcement, ~50 LoC pattern matching.**
- `hooks/precompact.py:1` — PreCompact. Generates markdown checkpoint *instructions* with `write_memory("shannon_precompact_checkpoint_{timestamp}", ...)` Serena pseudo-code as a string. **Does not actually write to Serena — emits instructions for Claude to do it.** No verification the checkpoint actually saves.
- `hooks/stop.py:1` — Stop hook. Reads `.serena/wave_validation_pending` and `.serena/critical_todos_incomplete` files. If present, blocks completion with JSON `{"decision":"block"}`. **File-based marker enforcement.**
- `hooks/session_start.sh:1` — bash heredoc. `cat`s `skills/using-shannon/SKILL.md` into stdout wrapped in `<EXTREMELY_IMPORTANT>` tags. **No logic.**

**Orchestration Python (the only meaningful code):**
- `orchestration/orchestrator.py` (306 lines) — `Wave`, `ExecutionState`, `Orchestrator` classes; HALT/RESUME async control via asyncio
- `orchestration/state_manager.py` (131 lines)
- `orchestration/decision_engine.py` (187 lines) — `DecisionEngine`, `DecisionOption`
- `server/websocket.py` (364 lines) — websocket server feeding `dashboard/` Vite app

**Tests:**
- `tests/orchestration/test_halt_resume.py` (119 lines) — pytest-asyncio, imports `from orchestration.orchestrator import Orchestrator, Wave, ExecutionState`. Real unit tests for HALT/RESUME timing.
- `tests/orchestration/test_decision_engine.py` (183 lines)
- `tests/e2e/test_decision_engine_e2e.py` (261 lines)
- `tests/server/test_websocket_decisions.py` (123 lines)
- Rest of `tests/` = .md "verification reports", sdk-examples (loose example scripts), and `validate_skills.py`.

**Validation script:**
- `validate_shannon_v5.py` runs metadata checks on commands/skills .md files. Currently FAILING — 25 issues. Output:
  ```
  ❌ 42 skills validation failed (25 issues)
  - do.md, scaffold.md, discover_skills.md, north_star.md, check_mcps.md,
    execute-plan.md, restore.md, status.md, reflect.md, analyze.md, init.md,
    checkpoint.md, write-plan.md ... (name field doesn't match filename)
  ```
  **The official validator does not pass on master.**

### Entry points (claimed but absent/nonexistent)

- `/shannon:spec`, `/shannon:wave`, `/shannon:prime`, `/shannon:do`, `/shannon:exec`, `/shannon:test`, `/shannon:reflect`, `/shannon:checkpoint`, `/shannon:restore`, `/shannon:north_star`, `/shannon:check_mcps`, `/shannon:status`, `/shannon:analyze`, `/shannon:discover_skills`, `/shannon:health`, `/shannon:ultrathink`, `/shannon:task`, `/shannon:scaffold`, `/shannon:memory`, `/shannon:init`, `/shannon:execute-plan`, `/shannon:write-plan`, `/shannon:generate_instructions` — **all 23 are markdown files**. No code. They describe what to do; Claude must read them and self-execute via prose instructions.
- "8D complexity algorithm" — described in `core/SPEC_ANALYSIS.md` (1,786 lines of prose with pseudo-code). **No Python implementation.** The numbers shown in README examples (`0.72 (VERY COMPLEX)`) cannot be computed by this repo — Claude must do it by reading the prose and inferring.
- "Wave orchestration 3.5x speedup" — `core/WAVE_ORCHESTRATION.md` (1,611 lines). Tied to `orchestration/orchestrator.py` but the orchestrator class is just HALT/RESUME state machinery, not parallel agent dispatch.
- "Serena MCP checkpointing" — checkpoints are written as prose instructions to Claude; success depends on Claude actually invoking `write_memory()`. **No verification.**
- "NO-FAKES hook enforcement" — only the `post_tool_use.py` regex check is real. README claims "4-layer enforcement"; layers 1, 3, 4 are markdown prose.

### Runtime architecture (what actually happens at runtime)

```
Claude Code session start
  ↓
SessionStart hook fires: session_start.sh
  ↓
Prints using-shannon SKILL.md (~300 lines of prose IRON_LAW + rules) into context
  ↓
User submits prompt
  ↓
UserPromptSubmit hook: user_prompt_submit.py
  ↓
Reads .serena/north_star.txt, .serena/active_wave_status.txt → prints into context
Detects large prompts → prints forced-reading-protocol activation prose
  ↓
Claude reads context, sees Shannon rules, decides whether to follow them
  ↓
Claude writes test file
  ↓
PostToolUse hook: post_tool_use.py
  ↓
Regex-scans for fake-test patterns → BLOCKS with JSON if found  ← only real enforcement
  ↓
Claude attempts to Stop
  ↓
Stop hook: stop.py
  ↓
Checks .serena/wave_validation_pending file → BLOCKS if exists  ← real enforcement
  ↓
PreCompact (only if context fills)
  ↓
precompact.py generates Serena checkpoint INSTRUCTIONS as markdown
  ↓
Claude is expected to execute write_memory() to actually save (no verification)
```

**Net: Shannon is ~95% Claude-following-prose, ~5% script-enforced gates.**

---

## 3. Code Worth Salvaging

Default verdict = rebuild. Salvageable pieces with path:line + justification:

### Hooks (real enforcement, mature regex/file-marker patterns)
- `hooks/post_tool_use.py:29-43` — pattern list (13 regex covering Jest, Pytest, Sinon, Vitest fake-test idioms). **Salvage** — concrete pattern coverage worth reusing in any "no-fakes" gate.
- `hooks/post_tool_use.py:63-80` — `is_test_file()` path-suffix detection. **Salvage** — battle-tested test-file heuristic.
- `hooks/stop.py:29-86` — file-marker block pattern (`.serena/wave_validation_pending`). **Salvage** — clean pattern for cross-tool-call state.
- `hooks/user_prompt_submit.py:35-83` — `detect_large_prompt()` + `detect_file_references()` regex. **Salvage** — useful for any prompt-size guard.

### Orchestration Python (the only real engine)
- `orchestration/orchestrator.py:17-25` — `ExecutionState` enum (IDLE/RUNNING/HALTED/COMPLETED/FAILED). **Salvage** — clean state machine.
- `orchestration/orchestrator.py:1-306` — `Wave`, `Orchestrator` HALT/RESUME async control. **Conditional salvage** — only if rebuild keeps an external orchestrator process; the layered prompt-stack engine in plan #6 likely supersedes this.
- `orchestration/decision_engine.py:1-187` — `DecisionEngine`, `DecisionOption`. **Read before discarding** — may inform layered-decision logic.
- `orchestration/state_manager.py:1-131` — small enough to read and decide.

### Server / dashboard
- `server/websocket.py:1-364` — websocket server. **Discard** unless rebuild needs a live UI; not load-bearing for the framework.
- `dashboard/*` — **Discard.** Vite app with no proven consumers.

### Prose-as-spec (NOT code, but reference material)
- `core/SPEC_ANALYSIS.md:1-1786` — 8D complexity scoring algorithm in pseudo-code. **Reference for rebuild** — the algorithm is documented; only needs to be implemented in actual Python.
- `core/WAVE_ORCHESTRATION.md:1-1611` — wave strategy patterns. **Reference only.**
- `core/HOOK_SYSTEM.md:1-1571` — hook architecture documentation. **Reference for hook design** in plan #6.
- `skills/using-shannon/SKILL.md` IRON_LAW block (lines 24-38) — explicit MUST-DOs that map cleanly to enforced rules. **Salvage as rule list** for plan #5 truth doc.
- `skills/functional-testing/SKILL.md` — NO-FAKES doctrine. **Salvage philosophy**, discard implementation pretense.

### Install scaffolding
- `install_local.sh:392-505` — `install_skills()`, `install_commands()`, `install_agents()`, `install_core()`, `install_hooks()` functions. **Salvage shape** — clean `cp -r` install pattern with version-file marker, `~/.claude/{type}/shannon/` namespacing.
- `install_local.sh:519-560` — hooks.json template generation with absolute paths. **Salvage** — reference for plan #6 plugin-loader install routine.

### Discard outright
- All 24 root `V5_*`, `V5.4_*`, `V5.5_*`, `V5.6*`, `CRITICAL_FIXES*`, `INSTALLATION_*`, `SHANNON_V*`, `MASTER_V5_SUMMARY.md` files — release-note sprawl, no value.
- All 24 `agents/*.md` persona files — prose personas, no code, the rebuild's plugin-loader replaces persona-as-markdown with proper agent definitions.
- 38 of 42 `skills/*/SKILL.md` — prose behavioral docs. Keep the doctrinal ones (using-shannon, functional-testing, spec-analysis, wave-orchestration, forced-reading-protocol) as reference; discard the rest.
- All `docs/` v5.6/, analysis/, plans/, ref/, guides/ — release noise.
- `validate_shannon_v5.py` — frontmatter linter for the current broken prose; rebuild's validator will be different.

---

## 4. Mismatches vs WithAgent Post Claims

(Cross-ref to auditor-1 happens in Phase 1 synthesis. This is the unilateral pass — initial flag list.)

Claims likely in withagents.dev/posts/post-07-shannon-framework rendering vs what's actually here:

1. **"4-Layer Enforcement Pyramid"** (README.md:46-72) — Only PostToolUse and Stop hooks enforce. Layers 1, 3, 4 (Core, Skills, Commands) are markdown prose; no enforcement code. Audit verdict: **3 of 4 layers are documentation, not enforcement.**

2. **"8D complexity score 0.00-1.00"** (README.md:188-213) — No Python implementation. `core/SPEC_ANALYSIS.md` describes the algorithm in pseudo-code; Claude must run it manually by reading the doc. Audit verdict: **algorithm is documented, not implemented.**

3. **"Wave orchestration 3.5x speedup"** (README.md:225-246) — `orchestration/orchestrator.py` provides HALT/RESUME state machinery only. Parallel agent dispatch happens via Claude reading `commands/wave.md` prose and self-orchestrating. **Speedup is unmeasured** — no benchmarks in `tests/` matching the claim.

4. **"NO-FAKES hook blocks fake-test usage"** (README.md:248-275) — TRUE for `post_tool_use.py` only. The hook does scan for jest/unittest/sinon/vitest fake-test patterns and return a block decision. Single accurate claim.

5. **"PreCompact hook saves to Serena"** (README.md:283-303) — FALSE as stated. The hook emits markdown *instructions* telling Claude to call `write_memory()`. The hook itself never writes to Serena. Verification step (`read_memory()` confirm) is also prose instruction to Claude. Audit verdict: **"saves" → "instructs Claude to save". Reliability unverified.**

6. **"42 skills, 24 agents, 23 commands"** (README.md:78-82 component inventory says 21/15/15 but actual ls is 42/24/23) — inventory in README is stale. Audit verdict: **README undercount, the actual sprawl is larger.**

7. **"Production-tested"** / **"V5_COMPLETION_CERTIFICATE.md"** / **"INSTALLATION_VERIFIED_V5.4.md"** — `validate_shannon_v5.py` does not pass on master. 25 issues. Audit verdict: **self-certification, not externally verified.**

8. **"61% of skills require Serena MCP"** (README.md:427) — there's no Serena dependency runtime check; install_local.sh does not verify Serena is installed. Audit verdict: **prose declaration, no runtime gate.**

9. **"PreCompact: `continueOnError: false`"** (README.md:441 + hooks.json:30) — TRUE. The hooks.json does set `continueOnError: false`. Whether Claude Code honors it across CC versions is untested in this repo.

10. **"plugin install via marketplace"** (README.md:138-143) — plugin.json + marketplace.json exist (lines 13 each). Installation directories scanned by audit:
    ```
    ls ~/.claude/plugins/  → blocklist.json cache data installed_plugins.json
                            known_marketplaces.json marketplaces oh-my-claudecode
                            plugin-catalog-cache.json prd-generator validationforge
    NO shannon dir present.
    ```
    Audit verdict: **plugin not currently installed on this machine.** Either never installed or removed.

---

## 5. Plugin Install State Delta

**Current state of `~/.claude/plugins/`:**
- ✅ Present: oh-my-claudecode, validationforge, prd-generator, claude-hud
- ❌ Absent: shannon (no `~/.claude/plugins/repos/shannon*`, no installed_plugins.json entry, no shannon dir)
- ❌ Absent: any `~/.claude/skills/shannon/`, `~/.claude/commands/shannon/`, `~/.claude/agents/shannon/`, `~/.claude/hooks/shannon/` (install_local.sh has never been run, or has been uninstalled)
- ❌ Absent: `~/.claude/shannon_version` marker file

**What an install would need to add:**

Per `install_local.sh:140-148` and the marketplace.json, install would create:
```
~/.claude/skills/shannon/         (42 skill dirs, ~12,000 lines of SKILL.md prose)
~/.claude/commands/shannon/       (23 .md command specs)
~/.claude/agents/shannon/         (24 .md agent personas)
~/.claude/core/shannon/           (10 .md files, 11,710 lines behavioral prose)
~/.claude/modes/shannon/          (2 .md)
~/.claude/templates/shannon/      (SKILL_TEMPLATE.md)
~/.claude/hooks/shannon/          (5 hook scripts + auto-generated session_start.sh)
~/.claude/hooks.json              (4 hook configs with absolute paths)
~/.claude/shannon_version         (version marker)
```

**Delta vs rebuild plan:**

Rebuild (per plan tasks #6-#8) will replace this with a real PromptStackEngine + plugin-loader + 7 prompt-stack layer modules. Current install delivers prose to `~/.claude/{type}/shannon/` directories; rebuild needs to deliver real engine code. Install scaffolding from `install_local.sh:392-560` is reusable as the install-routine shape, but the *content* it installs is 95% prose-to-discard.

**Install reliability flags:**
- `install_local.sh` is 900 lines but the actual work is ~150 lines (functions at 392-560); rest is detection / cleanup / status / arg parsing. **Bloated.**
- README recommends `install_universal.sh` (37KB) over plugin install, citing "discovery issues" with the plugin system. **This is a self-admission that the plugin manifest doesn't work reliably.**
- No install integrity check beyond "files exist". No "did the hook actually fire at session start?" gate.

---

## Verdict

**Rebuild. Salvage list is small.**

| Category | Lines | Action |
|---|---|---|
| Hooks (real enforcement) | ~600 LoC | **Salvage patterns** (regex lists, file-marker pattern, decision-block JSON shape) |
| Orchestration Python | ~630 LoC | **Read, then discard** (rebuild's engine supersedes) |
| Server / dashboard | ~700 LoC + Vite app | **Discard** |
| Install scaffolding | ~150 LoC of useful shape (in 900 LoC file) | **Salvage shape, not content** |
| Doctrinal prose (using-shannon, functional-testing, spec-analysis) | ~3,000 lines | **Reference for plan #5 truth doc**, do not deploy |
| All release-note .md sprawl | ~50 files | **Discard** |
| All persona agents/*.md | 24 files | **Discard** (rebuild replaces with agent code) |
| 38 of 42 skill prose files | ~10,000 lines | **Discard** |
| Tests | 686 lines real, 14 .md reports | Keep `tests/orchestration/*`, discard rest |

Net code worth keeping: **<1,000 lines** of patterns + algorithm reference.
Net code to write: a real engine (per tasks #6-#8).

---

## Unresolved Questions

1. **Has the plugin ever actually shipped to a user?** README.md:8 + install_test.log + V5_DEPLOYMENT_COMPLETE.md suggest yes; absence of `~/.claude/plugins/repos/shannon*` here suggests no on this machine. Need: external user telemetry, or git log of install_test.log.
2. **Is "3.5x speedup" claim sourced anywhere?** No benchmark files in `tests/` produce a 3.5x number. Need: original measurement methodology or retract claim in rebuild.
3. **Does `continueOnError: false` actually work?** PreCompact hook depends on it. No test in `tests/` exercises Claude Code's hook-failure path. Need: cross-version CC behavior check (route to auditor-3-live).
4. **Why does install_local.sh exist alongside the plugin manifest?** Self-documented discovery issue (README.md:148). Need: identify the actual plugin-system failure mode for rebuild's plugin-loader to avoid.
5. **Are any of the 42 skills wired to actual code, or are they all prose?** Spot-checked ~6 — all prose. Need: full sweep before plan #5 synthesis to confirm zero hidden Python skill implementations.
6. **`orchestration/orchestrator.py` is real code with passing tests, but is it ever invoked at runtime?** Nothing in `hooks/` or `commands/` calls it. Likely dead — needs grep for `from orchestration` outside `tests/`.

**Status:** DONE
**Summary:** Audited shannon-framework v5.6.1. ~95% prose, ~5% real code (~1,400 LoC Python). Real enforcement = 2 hooks (post_tool_use.py fake-test block, stop.py file-marker block). Everything else = markdown that Claude reads and self-executes. Plugin not currently installed on this machine. Salvage <1,000 LoC of patterns + algorithm reference; rebuild the rest.
**Concerns:** Validator (`validate_shannon_v5.py`) fails on master with 25 issues — repo is publicly claimed "v5.6.1 production-ready" but its own linter doesn't pass.
