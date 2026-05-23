# GAP-MATRIX.md — Shannon v6 Implementation Gap Matrix

**Date:** 2026-05-23
**Purpose:** Row-per-implementable-item to drive Phase 2-5 work. Sorted by priority (blockers first).

**Columns:**
- Claim — what was promised or required
- Source — A1/A2/A3/A4 + cite
- Expected Behavior — observable outcome
- Current Support — what v5.6.1 already provides (A2 evidence)
- Required Implementation — what Phase 2-5 must build
- Validation Method — how Phase 5 will prove it works
- Status — BLOCKER / HIGH / MEDIUM / LOW / NICE-TO-HAVE

---

## Priority 1: BLOCKERS (must ship in v6.0)

| # | Claim | Source | Expected Behavior | Current Support | Required Implementation | Validation Method | Status |
|---|---|---|---|---|---|---|---|
| B1 | Shannon plugin installable via /plugin install | A1 §3.5; A3 §7 | After install, ~/.claude/plugins/cache/shannon-local/shannon/6.0.0/ exists; enabledPlugins[shannon@shannon-local]=true | NONE — repo has 5.6.1 install_local.sh (manual cp -r) | Create .claude-plugin/plugin.json + .claude-plugin/marketplace.json conforming to CC schema (see A3 §7 11-item delta). Delete install_local.sh. | Run /plugin install shannon@shannon-local; assert path exists + settings.json updated | BLOCKER |
| B2 | hooks/hooks.json registers 7 scripts | A1 §2.6; A3 §1 (VF pattern) | CC reads hooks.json at plugin register; chains Shannon hooks per declared event+matcher | NONE — v5.6.1 install_local.sh writes ~/.claude/hooks.json directly (bypasses plugin) | Author hooks/hooks.json per SPEC §3.3; declare all 7 hooks with correct matchers | After install, session.jsonl shows Shannon hooks in chain at each event | BLOCKER |
| B3 | block-fab-files.js executes 12-pattern detector + stderr+exit 2 | A1 §4.2 (post-16 verbatim) | PreToolUse:Write on path matching pattern → exit 2 + stderr explanation; tool blocked | v5.6.1 hooks/post_tool_use.py has 13-regex cousin (PostToolUse, not PreToolUse) | Write hooks/block-fab-files.js per post-16:202-244 verbatim (TS→JS). Change registration to PreToolUse | layers/hooks/validate.sh fires real Write with matching filename; assert exit 2 + stderr present | BLOCKER |
| B4 | validation-not-compilation.js fires on PostToolUse:Bash | A1 §4.4 (post-16:69-123) | After Bash build command with success indicator → stderr reminder + exit 2 | NONE | Write hooks/validation-not-compilation.js verbatim from post-16:69-123 | Run real npm build; assert stderr contains BUILD SUCCESS IS NOT FUNCTIONAL VALIDATION | BLOCKER |
| B5 | evidence-gate-reminder.js fires on PreToolUse:TaskUpdate with status:completed | A1 §4.5 (post-16:260-275) | TaskUpdate with status completed → stderr 5-question checklist + exit 2 | NONE | Write hooks/evidence-gate-reminder.js verbatim from post-16:260-275 | Run real TaskUpdate completed; assert stderr contains checklist | BLOCKER |
| B6 | read-before-edit.js tracks reads then warns on unread edits | A1 §4.3 (post-07:168-188) | After Edit on file not previously Read → stderr warning + exit 2 (inject mode, not block) | NONE | Write hooks/read-before-edit.js with explicit const readFiles = new Set() module-top + try/catch + process.exit(0) on crash | Real session: Edit unread file; assert stderr WARNING + exit 2 | BLOCKER |
| B7 | skill-activation-check.js hints on UserPromptSubmit | A1 §2.7 (post-07:204, post-16:280-283) | Prompt matching skill trigger pattern → stderr hint listing matched skills + exit 2 | v5.6.1 user_prompt_submit.py is cousin (different logic) | Write hooks/skill-activation-check.js: read prompt, regex-match against skill manifest triggers, emit stderr hint | Submit prompt "build the app"; assert stderr lists functional-validation, gate-validation-discipline | BLOCKER |
| B8 | validation-skill-tripwire.js detects skip | A1: NEW per user concern (a); A3 §4 (0 invocations) | After Bash build success + no functional-validation Skill invocation since last build → stderr TRIPWIRE + exit 2 + append to tripwires.jsonl | NONE (new) | Write hooks/validation-skill-tripwire.js: read ~/.claude/logs/shannon/invocation.jsonl, check timestamps, fire tripwire | layers/invocation/validate.sh: run npm build, do NOT invoke skill, assert TRIPWIRE stderr | BLOCKER |
| B9 | stop-task-semantics.js classifies Stop | A1: NEW per user concern (b); A3 §6 | Stop event + open TaskCreate items + last assistant message regex (let me / next I'll) → exit 2 + stderr defer message | NONE (new) | Write hooks/stop-task-semantics.js: read TaskList JSON via shared file or settings inject, regex last assistant msg | Real session with open tasks + intermediate Stop; assert exit 2 + stderr | BLOCKER |
| B10 | subagent-governance-inject.js appends IRON-RULE on Task/Agent | A1 §2.11 (post-07:257) | PreToolUse:Task → append no-fakes / evidence-gated / read-before-edit to prompt via stderr+exit 2 | NONE | Write hooks/subagent-governance-inject.js per post-07:257 prose | Spawn subagent; read subagent session.jsonl; assert IRON-RULE text in first message | BLOCKER |
| B11 | Per-hook try/catch wrapping with exit 0 fallback | A1 §6.9 (post-16:169); A3 §3 | Hook script throw → process.exit(0) + log to hook-errors.jsonl; CC proceeds | v5.6.1 hooks inconsistent | All 7 hook scripts share a try/catch wrapper module: lib/hook-runner.js exposing runHook(handler) | layers/hooks/validate.sh: inject throw in one hook; assert exit 0 + log entry | BLOCKER |
| B12 | Hook log file per fire | A1: NEW per user concern (c); A3 §3 | Every hook fire appends one JSON record to ~/.claude/logs/shannon/hooks.jsonl | NONE | Hook runner writes log line on every fire (script, decision, matched, ms, sessionId) | After session: grep hooks.jsonl, assert >=7 entries (one per hook) | BLOCKER |

---

## Priority 2: HIGH (v6.0 if time; v6.1 acceptable)

| # | Claim | Source | Expected Behavior | Current Support | Required Implementation | Validation Method | Status |
|---|---|---|---|---|---|---|---|
| H1 | ContextLayer SessionStart injection | A1 §1.1 Layer 7 (post-07:89); A3 §3 | SessionStart fires → CLAUDE.md global + project + .claude/rules/*.md concatenated to stdout, CC reads as context | v5.6.1 session_start.sh heredoc's a single skill file | Write layers/context/context-layer.js that reads all 3 sources, writes to stdout, exits 0 | Boot session; assert <system-reminder> for each rule file in transcript | HIGH |
| H2 | functional-validation SKILL.md content | A1 §4.8 (post-16:358-374) | /shannon:functional-validation invocable; SKILL.md per post-16 schema (Trigger Patterns + Execution Steps) | v5.6.1 has skills/functional-testing/SKILL.md (cousin) | Author skills/functional-validation/SKILL.md per post-16:358-374 verbatim | Invoke Skill tool with skill=functional-validation; assert frontmatter loaded | HIGH |
| H3 | shannon-doctor command emits fire counts | User concern (c) extension | /shannon:doctor reads logs/shannon/*.jsonl, prints last-24h hook fire counts + avg ms | NONE | Author commands/doctor.md (skill-style) that runs a bash one-liner over logs | Run /shannon:doctor after 30min session; assert output table shows 7 hooks | HIGH |
| H4 | Three-level severity: Block / Warn / Remind | A1 §2.9 (post-07:239-249) | Each hook returns one of Block (PreToolUse exit 2 = tool prevented), Warn (PostToolUse exit 2 = inject), Remind (PostToolUse exit 2 = inject, lower-stakes wording) | v5.6.1 has only 2 effective modes | Hook implementations differentiate via stderr wording + which event they register; document in hook header comment | Visual inspection of each hook's stderr text against severity taxonomy | HIGH |
| H5 | Rules-split — load N rule files | A1 §6.6 (post-07:235) | .claude/rules/*.md files all loaded by ContextLayer at SessionStart | v5.6.1 hardcodes single skill file | ContextLayer iterates .claude/rules/ glob, concatenates | Boot session in project with 9 rule files; assert all 9 sources cited in transcript | HIGH |

---

## Priority 3: MEDIUM (v6.1 default)

| # | Claim | Source | Expected Behavior | Current Support | Required Implementation | Validation Method | Status |
|---|---|---|---|---|---|---|---|
| M1 | Observability dashboard | User concern (c) extension | HTML dashboard summarizing logs/shannon/*.jsonl | NONE | Phase 6+: author dashboard skill that renders HTML from logs | Open dashboard.html; manually verify | MEDIUM (DEFERRED-TO-V6.1) |
| M2 | Hook performance budget enforcement | A1 §6.8 (post-16:346) | Hook wall-clock > 100ms → log warning to hook-errors.jsonl | NONE | Hook runner wraps handler with Date.now timing; warns if elapsed > 100 | Inject slow handler; assert warning logged | MEDIUM |
| M3 | Subagent inheritance compliance number | A1 §6.3 (post-07:255: 68% → 95%) | Telemetry can compute compliance rate | NONE | Phase 6+: opt-in telemetry script analyzing subagent session.jsonl files | Run for 7 days, compute rate | MEDIUM (DEFERRED-TO-V6.1) |
| M4 | Numeric promises measurable | A1 §6.11 (all rates 87%, 7ms, 9.6:1) | Phase 5 measurement reproduces published rates | NONE | Phase 6+: full telemetry build-out | Aggregate over real sessions | MEDIUM (DEFERRED-TO-V6.1) |
| M5 | Hook crash error log | A1 §6.9 derived | hook-errors.jsonl exists, each entry has timestamp + script + error message | NONE | Hook runner writes catch-block log | Inject throw; assert entry | MEDIUM |
| M6 | TaskList read in stop-task-semantics | B9 derivation | Read open task count without parsing fragile JSONL | NONE | Use shared file at ~/.claude/logs/shannon/open-tasks.txt updated by Shannon TaskCreate/TaskUpdate hooks (post-MVP) | Inject TaskCreate; assert open-tasks.txt count++ | MEDIUM (could simplify to grep on JSONL for v6.0) |

---

## Priority 4: LOW (v6.2 or later)

| # | Claim | Source | Expected Behavior | Status |
|---|---|---|---|---|
| L1 | PreCompact event registration | A2 §2 (v5.6.1 has fake impl) | Real PreCompact handler that writes memory checkpoint | LOW (DEFERRED-TO-V6.1; v5.6.1 impl was fake per A2 §2) |
| L2 | MCP servers shipped by Shannon | A1 §1.1 Layer 6 | Shannon ships sequential-thinking-MCP or design-system-MCP | LOW (DEFERRED; v6 audits MCP only) |
| L3 | TaskCompleted / TeammateIdle handlers | A3 §3 events | Shannon listens to these for telemetry | LOW |
| L4 | shannon-framework as OMC plugin | A4 §1 unresolved | Shannon bundled inside OMC instead of standalone | LOW (rejected — keep standalone) |

---

## Priority 5: REJECT (not shipping)

| # | Claim | Source | Reason for rejection |
|---|---|---|---|
| R1 | `/autopilot` `/ralph` `/team` commands as Shannon's | A1 §1.4 enforcement-pyramid.html:124-128 | These are OMC commands (A3 §1). Shannon does NOT own these. Diagram is wrong; post must update. |
| R2 | "5 commands, 5 skills, 5 hooks, 4 agents" cover-image deliverable | post-16/social/linkedin-article.md:27 | Conflicts with post-16:417 prose count. v6 ships post-16 prose (5h/1s/1a). Cover-image needs reshoot. |
| R3 | Object-return hook contract `return { decision, message }` | A1 §2.4 (post-07 style) | User DECISION 2: stderr+exit 2 only. Object-return is LEGACY-DROPPED. |
| R4 | install_local.sh manual cp -r install | A1 §3.3 (post-07:310-318); A2 §2 (v5.6.1 ships it) | v6 uses /plugin install. install_local.sh DELETED. Post must update install snippet. |
| R5 | "No registration, no manifest parsing, no framework overhead" claim | post-16/post.md:334 | False under v6 plugin-install flow. Plugin manifest + hooks.json ARE the registration. Post must update. |
| R6 | v5.6.1 8D complexity algorithm Python impl | A2 §3 | Not in v6 scope. Belongs to a future v7+ planning surface. |
| R7 | Wave orchestration 3.5x speedup | A2 §3 | Not in v6 scope. v5.6.1 orchestrator.py is HALT/RESUME only; speedup unmeasured. |

---

## Phase 2-5 Work Drivers

Phase 2 (core engine) consumes: B1, B2, B11, B12.
Phase 3 (layer modules + overlay) consumes: H1, H2, H3, H5, plus the 7-layer doc overlay (post-07 conceptual restated against §2.B).
Phase 4 (CC integration) consumes: B3-B10 hook implementations + activation cycles.
Phase 5 (post-truth validation gates) consumes: all validate.sh per module + validate-all.sh per SPEC §6.3.

---

End of GAP-MATRIX.md.
