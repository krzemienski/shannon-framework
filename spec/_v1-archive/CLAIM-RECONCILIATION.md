# CLAIM-RECONCILIATION.md — Shannon Claim Reconciliation (a.k.a. TRUTH-DOC)

**Date:** 2026-05-23
**Sources reconciled:**
- A1 = withagent-claims.md (post-07 + post-16 + visuals + social copy)
- A2 = shannon-current.md (live shannon-framework v5.6.1 repo state)
- A3 = live-cc-audit.md (what CC actually exposes on Nick's machine, 2026-05-23)
- A4 = prior-art.md (LangChain, DSPy, tapable, Vite, VSCode, OMC, esbuild, ...)

**Status values:**
- SHIPPED-IN-V6 — claim is honored by SHANNON-SPEC.md and will exist in Phase 2-5 deliverables
- DEFERRED-TO-V6.1 — accepted but not in v6.0 ship; recorded in REMAINING-GAPS.md
- REQUIRES-POST-EDIT — claim is wrong about what Shannon ships; blog posts must be updated post-rebuild
- ASPIRATIONAL — promise made in blog with no defensible foundation; will not be honored
- LEGACY-DROPPED — explicitly contradicted by user DECISION 2; v6 uses replacement contract

---

## Section 1. Layer Roster

| WithAgent claim (A1 cite) | Live CC (A3) | Current v5.6.1 (A2) | Required v6 (SPEC §2) | Status |
|---|---|---|---|---|
| "7-layer prompt engineering stack: Global CLAUDE.md, rules/, Hooks, Skills, Agents, MCP, SessionStart" — post-07/post.md:77-89 | CC exposes SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart, Stop, PreCompact events (auditor-3 §3) | v5.6.1 has no executable layers — all prose | 4 enforcement modules (ContextLayer + HookLayer + InvocationLayer + DispatchLayer) + 7-conceptual-layer overlay as docs | SHIPPED-IN-V6 (per user DECISION 1, Path C) |
| "4-layer Enforcement Pyramid: CLAUDE.md, Hooks, Skills, Commands" — post-16/post.md:174-189 | Same CC events | Same prose-only state | 4 enforcement modules per §2.A | SHIPPED-IN-V6 |
| "Defense in depth — if Layer 1 fails, Layer 3 catches it" — post-07/post.md:91 | CC hook chain runs sequentially per event | No real defense; prose-only | Layered modules compose in order 1→4; each emits stderr+exit 2 independently | SHIPPED-IN-V6 |
| "9 rule files: coding-style.md, security.md, ... development-workflow.md" — post-07/post.md:79 | User's actual .claude/rules/ differs (30+ files) | v5.6.1 ships 0 rule files in this layout | v6 ContextLayer loads whatever .claude/rules/*.md exists; does NOT mandate the 9-file taxonomy | REQUIRES-POST-EDIT |
| "Combined 4-layer compliance: 95%+" — post-16/post.md:189 | No telemetry on user's machine to confirm | v5.6.1 reports no such metric | Phase 5 measures post-install via e2e-evidence/end-to-end/ — number may differ | ASPIRATIONAL |
| "23% → 0 violation rate for block-fab-files" — post-07/post.md:164 | No on-machine evidence; auditor-3 found 0 fires in 3 sessions | v5.6.1 has working detector regex | v6 ships same regex (post-16 §4.2 12-pattern canonical); rate measurable only via opt-in telemetry | ASPIRATIONAL |

---

## Section 2. Hook Events

| Claim (A1) | Live CC (A3) | v5.6.1 (A2) | Required v6 | Status |
|---|---|---|---|---|
| PreToolUse, PostToolUse, UserPromptSubmit events exist — post-07/post.md:97-101, post-16/post.md:163-168 | Confirmed: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, SubagentStart, Stop, PreCompact, SessionEnd, TaskCompleted, TeammateIdle, Notification, PermissionRequest, StopFailure (auditor-3 §3) | v5.6.1 uses UserPromptSubmit, PostToolUse, Stop, PreCompact + custom session_start.sh — partial coverage | v6 uses SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart, Stop. PreCompact deferred. | SHIPPED-IN-V6 |
| "PreToolUse fires before tool" — post-16/post.md:165 | Confirmed (auditor-3 §3) | Confirmed | Confirmed | SHIPPED-IN-V6 |
| "PostToolUse fires after tool" — post-16/post.md:166 | Confirmed (auditor-3 §3) | Confirmed | Confirmed | SHIPPED-IN-V6 |
| "UserPromptSubmit fires on every user message" — post-16/post.md:167 | Confirmed; 5+ scripts wired in user's settings.json (auditor-3 §3) | v5.6.1 uses it (user_prompt_submit.py) | v6 uses it (skill-activation-check.js) | SHIPPED-IN-V6 |
| Subagent inheritance hook on Agent tool — post-07/post.md:257 | CC fires PreToolUse on Task/Agent tools; also fires SubagentStart event (auditor-3 §3) | v5.6.1 has no subagent injection | v6 DispatchLayer registers against PreToolUse:Task\|Agent (hook #7 / subagent-governance-inject.js) | SHIPPED-IN-V6 |
| TaskCompleted, TeammateIdle events | Confirmed (auditor-3 §3) | v5.6.1 unused | v6 unused (out of scope) | DEFERRED-TO-V6.1 |
| PreCompact event | Confirmed (auditor-3 §3); v5.6.1 uses it; user's settings.json has empty PreCompact slot | v5.6.1 precompact.py emits prose checkpoint instructions, no actual write (A2 §2) | v6 does NOT register PreCompact (out of scope; v5.6.1 implementation was fake) | DEFERRED-TO-V6.1 |

---

## Section 3. Hook Return Contract

| Claim (A1) | Live CC (A3) | v5.6.1 (A2) | Required v6 | Status |
|---|---|---|---|---|
| return { decision: 'block'\|'allow', message } from default-export function — post-07/post.md:130-152, 168-188 | Live CC convention: stderr+exit 2 to block/inject, exit 0 to allow (auditor-3 §3; ~/.claude/rules/hooks-and-integrations.md). post-07 object-return pattern not supported by current CC. | v5.6.1 hooks/post_tool_use.py returns {decision:block} as JSON to stdout — works on some CC versions, brittle | v6 uses stderr+exit 2 exclusively per CC convention | LEGACY-DROPPED (per user DECISION 2; documented in REMAINING-GAPS.md) |
| process.stderr.write(...); process.exit(2); — post-16/post.md:317-332 | Confirmed = current CC convention (auditor-3 §3; user rule) | v5.6.1 inconsistent (mixes JSON-to-stdout and direct print) | v6 standardizes on this contract | SHIPPED-IN-V6 |
| "exit code 2 injects into agent context" — post-16/post.md:321 | Confirmed for PreToolUse (block) and PostToolUse/UserPromptSubmit (inject) | Partially supported | SHIPPED-IN-V6 |
| "Silent allow — exit 0 with no output" — post-16/post.md:330 | Confirmed (auditor-3 §3) | Confirmed | Confirmed | SHIPPED-IN-V6 |
| "Hook crash = silent allow" — post-16/post.md:169 | Confirmed empirically (auditor-3 §3) | v5.6.1 hooks don't catch consistently | v6 every hook wraps body in handler → process.exit(0) on catch + log to hook-errors.jsonl | SHIPPED-IN-V6 |
| "<100ms, synchronous, no network" — post-16/post.md:346 | CC tolerates slower but penalizes UX | v5.6.1 hooks vary (some read files) | v6 target <100ms; no network calls; sync only | SHIPPED-IN-V6 |
| "Three-response API" — post-16/post.md:317-332 | Confirmed (block / inject / silent) | Partial | SHIPPED-IN-V6 |
| "Matcher pattern Write\|Edit\|MultiEdit as pipe-delimited" — post-16/post.md:342 | Confirmed in live VF hooks.json (auditor-3 §1) | v5.6.1 hooks.json matches | v6 hooks/hooks.json uses pipe-delimited matchers | SHIPPED-IN-V6 |
| stdin JSON payload for hooks (auditor-1 §2.5) — post-16/post.md:285-314 | Confirmed (auditor-3 §3) | v5.6.1 reads stdin per CC convention | Confirmed | SHIPPED-IN-V6 |

---

## Section 4. Plugin Contract

| Claim (A1) | Live CC (A3) | v5.6.1 (A2) | Required v6 | Status |
|---|---|---|---|---|
| "4 plugin extension points: hooks, skills, agents, MCP servers" — post-16/post.md:52 | Confirmed in CC plugin manifest (.claude-plugin/plugin.json supports skills, agents, commands, hooks, mcpServers) | v5.6.1 has plugin.json + marketplace.json but install_local.sh bypasses plugin system | v6 ships via real plugin system (no install_local.sh) | SHIPPED-IN-V6 |
| "Shannon Framework is a reference CC plugin with 5 hooks, 1 skill, 1 agent template" — post-16/post.md:417 | CC supports plugins of this shape | v5.6.1 has 42 skills, 24 agents, 23 commands, 5 hooks — way more sprawl than claim | v6 ships 7 hook scripts + small skill set (TBD Phase 3) + small agent set (TBD Phase 3); aligns toward "5 hooks 1 skill 1 agent" framing | REQUIRES-POST-EDIT |
| Cover-image alt: "5 commands, 5 skills, 5 hooks, 4 agents" — post-16 linkedin-article.md:27 | n/a | v5.6.1 sprawl | v6 ship will differ from BOTH numbers; reconcile post-Phase 3 | REQUIRES-POST-EDIT |
| Install via cp -r hooks/ .claude/hooks/ — post-07/post.md:310-318 | Live CC supports /plugin install (marketplace + cache) — manual cp-r is legacy (auditor-3 §1) | v5.6.1 install_local.sh does manual cp-r | v6 uses /plugin install shannon@shannon-local per VF/OMC pattern | REQUIRES-POST-EDIT |
| "No registration, no manifest parsing, no framework overhead" — post-16/post.md:334 | Live CC DOES require .claude-plugin/plugin.json + hooks/hooks.json for plugin install (auditor-3 §1; VF + OMC patterns) | v5.6.1 has plugin.json but doesn't use the install flow | v6 uses both manifests; post-16 quote is misleading | REQUIRES-POST-EDIT |
| .claude/settings.json hook block — post-16/post.md:128-144 | Confirmed; also hooks/hooks.json inside plugin (auditor-3 §1) | v5.6.1 install_local.sh writes ~/.claude/hooks.json directly | v6 uses plugin-internal hooks.json; no direct settings.json writes by Shannon installer | SHIPPED-IN-V6 |
| Commands surface — /autopilot /ralph /team — post-16 enforcement-pyramid.html:124-128 | These are OMC commands, NOT Shannon (auditor-3 §1) | v5.6.1 has 23 different commands | v6 ships small commands set TBD Phase 3 — does NOT ship /autopilot, /ralph, /team | REQUIRES-POST-EDIT |

---

## Section 5. Code Snippets (per-snippet validation)

| Snippet (A1 cite) | v5.6.1 equivalent (A2) | Required v6 | Status |
|---|---|---|---|
| block-test-files.js post-07 version, 10 patterns, object-return — post-07/post.md:111-152 | v5.6.1 hooks/post_tool_use.py has 13 regex (close cousin) | v6 ships post-16's 12-pattern canonical detector, stderr+exit 2 | LEGACY-DROPPED |
| block-test-files.js post-16 version, 12 patterns, stderr+exit2 — post-16/post.md:202-244 | v5.6.1 PostToolUse equivalent exists (similar regex) | v6 ships verbatim equivalent (under filename block-fab-files.js per §3.4 naming note): 12 patterns, stderr+exit 2, PreToolUse:Write\|Edit\|MultiEdit | SHIPPED-IN-V6 |
| read-before-edit.js — post-07/post.md:168-188; references undeclared readFiles Set | v5.6.1 has no equivalent | v6 ships with explicit const readFiles = new Set() at module top; persists for session lifetime (cleared on SessionEnd) | SHIPPED-IN-V6 |
| validation-not-compilation.js — post-16/post.md:69-123 | v5.6.1 has no equivalent | v6 ships verbatim (BUILD_COMMANDS + SUCCESS_INDICATORS + stderr+exit 2) | SHIPPED-IN-V6 |
| evidence-gate-reminder.js — post-16/post.md:260-275 | v5.6.1 has no equivalent | v6 ships verbatim; registers PreToolUse:TaskUpdate | SHIPPED-IN-V6 |
| skill-activation-check.js — post-07/post.md:204; post-16/post.md:280-283 references; no full impl shown | v5.6.1 hooks/user_prompt_submit.py is closest cousin | v6 implements: regex-match prompt against skill triggers, write hints to stderr, exit 2 if no skill candidates match (no-op silent allow) or exit 2 with skill hints | SHIPPED-IN-V6 |
| Hook 6: validation-skill-tripwire.js — NOT in A1 | n/a — not claimed | v6 adds this hook to address user concern (a); not in original 5-hook loadout | SHIPPED-IN-V6 (new in v6) |
| Hook 7: stop-task-semantics.js — NOT in A1 | n/a — not claimed | v6 adds this hook to address user concern (b); not in original 5-hook loadout | SHIPPED-IN-V6 (new in v6) |
| functional-validation SKILL.md — post-16/post.md:358-374 | v5.6.1 has skills/functional-testing/SKILL.md (cousin) | v6 ships skills/functional-validation/SKILL.md per A1 spec | SHIPPED-IN-V6 |
| Inline SVG diagrams 1-3 post-07 (post-blocks.ts) — 7-layer flow, hook sequence, CLAUDE.md inheritance chain | n/a — diagrams ship in posts only | v6 ships own diagrams as needed; post diagrams unchanged | SHIPPED-IN-V6 |
| Enforcement pyramid Mermaid — post-16 enforcement-pyramid.html | n/a | v6 doc overlay re-renders against the 4-module model (replaces Commands layer with InvocationLayer/DispatchLayer mapping) | REQUIRES-POST-EDIT |

---

## Section 6. Numeric Promises

| Number (A1 cite) | Foundation | Required v6 stance | Status |
|---|---|---|---|
| 23,479 sessions / 42 days / Jan 24 - Mar 6 2026 — post-07/post.md:39, posts/INDEX.md:14 | Blog-series mining data | Out of v6 scope; numbers belong to series-metrics.md not Shannon repo | ASPIRATIONAL |
| 87% violation reduction aggregate — post-07/post.md:265 | Same mining data | Out of v6 scope | ASPIRATIONAL |
| 7ms per tool call overhead — post-07/post.md:265 | Same | v6 targets <100ms; 7ms aspirational without telemetry | DEFERRED-TO-V6.1 |
| 9.6:1 Read-to-Write ratio post-hook — post-07/post.md:267 | Same | Out of v6 scope | ASPIRATIONAL |
| 4.4:1 Read-to-Edit ratio post-hook — post-16/post.md:254 | Same | Out of v6 scope | ASPIRATIONAL |
| 1,370 skill invocations — post-07/post.md:83 | Same | auditor-3 found <1% invocation rate in 3 sessions — contradicts implied lots of invocations framing | REQUIRES-POST-EDIT |
| 327 sequential-thinking MCP invocations — post-07/post.md:87 | Same | Out of v6 scope | ASPIRATIONAL |
| 2,827 Task spawns / 929 Agent calls — post-07/post.md:259 | Same | Out of v6 scope | ASPIRATIONAL |
| 82,552 Bash / 87,152 Read / 19,979 Edit — post-07/post.md:267 | Same | Out of v6 scope | ASPIRATIONAL |
| 68% → 95% subagent compliance with constitution injection — post-07/post.md:255 | Same | Phase 5 will measure post-install — number may differ | DEFERRED-TO-V6.1 |
| 41% → 9% validation-not-compilation violation — post-07/post.md:190 | Same | DEFERRED-TO-V6.1 |
| 31% → 4% read-before-edit violation — post-07/post.md:166 | Same | DEFERRED-TO-V6.1 |
| Task quality +34% — post-07/post.md:202 | Same | DEFERRED-TO-V6.1 |
| 87% / 89% / 95% / 88% rules-compliance numbers — post-07/post.md:235, 249 | Same | DEFERRED-TO-V6.1 |

Rule of thumb: every numeric promise = ASPIRATIONAL or DEFERRED unless Phase 5 measurement reproduces it. v6 spec ships mechanism; rates require post-publication telemetry build-out.

---

## Section 7. Commands Surface

| Command (A1) | Owner per A3 | Required v6 stance | Status |
|---|---|---|---|
| /autopilot | OMC (auditor-3 §1, /oh-my-claudecode:autopilot) | Shannon does NOT ship; remove from enforcement pyramid | REQUIRES-POST-EDIT |
| /ralph | OMC + ralph-loop plugin | Shannon does NOT ship | REQUIRES-POST-EDIT |
| /team | OMC | Shannon does NOT ship | REQUIRES-POST-EDIT |
| Shannon commands TBD Phase 3 (e.g. /shannon:doctor, /shannon:validate) | v6 | v6 ships small command set with shannon: prefix only | SHIPPED-IN-V6 (exact commands set Phase 3) |

---

## Section 8. Layer-Realization Mapping (post-16 enforcement pyramid → v6)

| Post-16 pyramid edge | A1 claim | v6 reality |
|---|---|---|
| L4:Commands → L3:Skills (C1→S1) | /autopilot routes to functional-validation | Shannon command surface TBD Phase 3; current /autopilot is OMC's. Edge invalid as drawn. |
| L3:Skills → L1:Mandates (S1→M1) | functional-validation implements No-fakes mandate | Skill exists in v6 (TBD Phase 3 content); mandate exists in CLAUDE.md (ContextLayer loads). Edge valid. |
| L2:Hooks → L1:Mandates (H1→M1 enforces) | block-fab-files.js enforces No-fakes | Hook ships in v6 (HookLayer); enforces same mandate. Edge valid. |
| L2:Hooks → L1:Mandates (H3→M2, H4→M2) | validation-not-compilation + evidence-gate-reminder enforce Functional-validation mandate | Both ship in v6 (HookLayer). Edges valid. |
| L2:Hooks → L1:Mandates (H2→M3) | read-before-edit.js enforces Read-before-write | Hook ships in v6 (HookLayer). Edge valid. |

**Verdict:** 5 of 6 edges hold under v6. The C1→S1 / C2→S2 / C3→S3 command-to-skill edges break because Shannon does not own /autopilot, /ralph, /team. Diagram needs redraw or commands edge labeled as user-runs-command (any orchestrator, not Shannon-specific).

---

## Section 9. Inconsistency Resolution Log

| Inconsistency (A1 Unresolved) | Resolution |
|---|---|
| 7 layers vs 4 layers | User DECISION 1 = Path C (4 enforcement + 7 doc overlay). LOCKED. |
| Object-return vs stderr+exit2 | User DECISION 2 = stderr+exit2 (CC convention). LOCKED. |
| 10 vs 12 detector patterns | v6 ships 12 (post-16 canonical, A1 §4.2). |
| 5h+1s+1a vs 5c+5s+5h+4a deliverable | v6 targets post-16 prose form (5 hooks, ≥1 skill, ≥1 agent). LinkedIn-article hero alt-text is REQUIRES-POST-EDIT. |
| Commands attribution to Shannon | REQUIRES-POST-EDIT — these are OMC commands. |
| Unnamed subagent inheritance hook | v6 names it subagent-governance-inject.js (DispatchLayer hook #7). |
| readFiles Set undeclared in snippet | v6 declares const readFiles = new Set() at module top. |
| SessionStart injection mechanism | v6 ContextLayer registers against SessionStart event; emits stdout (CC reads as context). |
| MCP tools layer status | v6 does NOT ship MCP servers; DispatchLayer audits MCP tool calls only. MCP layer remains in 7-layer doc overlay as Phase 6+ extension. |
| Numeric provenance | All ASPIRATIONAL or DEFERRED-TO-V6.1 per §6. |

---

End of CLAIM-RECONCILIATION.md (formerly TRUTH-DOC.md per spec naming).
