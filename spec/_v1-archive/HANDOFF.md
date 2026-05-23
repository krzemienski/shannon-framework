# HANDOFF.md — Phase 1 → Phase 2-5 Handoff Brief

**From:** architect (Phase 1, team shannon-rebuild-260523)
**To:** Phase 2 (core engine), Phase 3 (layer modules + overlay), Phase 4 (CC integration), Phase 5 (validation)
**Date:** 2026-05-23
**Locked spec artifacts:**
- /Users/nick/Desktop/shannon-framework/spec/SHANNON-SPEC.md
- /Users/nick/Desktop/shannon-framework/spec/CLAIM-RECONCILIATION.md  (a.k.a. TRUTH-DOC)
- /Users/nick/Desktop/shannon-framework/spec/GAP-MATRIX.md
- /Users/nick/Desktop/shannon-framework/spec/HANDOFF.md (this file)

---

## TL;DR

Shannon v6.0.0 is a real, loadable Claude Code plugin. It ships **4 enforcement layer modules** + **7 hook scripts** + **plugin manifest** + **per-module validate.sh** scripts. v5.6.1's prose-as-spec model is dead. Phase 5 must prove the plugin actually fires against a real CC session.

## The 4 Enforcement Layer Modules

| Module | Responsibility | CC Events |
|---|---|---|
| ContextLayer | Load + inject CLAUDE.md global, project, .claude/rules/*.md | SessionStart |
| HookLayer | Mechanical tool-boundary enforcement (5 hooks) | PreToolUse, PostToolUse |
| InvocationLayer | Force skill invocation when intent matches; tripwire skipped invocations | UserPromptSubmit, PostToolUse:Bash |
| DispatchLayer | Subagent governance inject + Stop semantics classification | PreToolUse:Task\|Agent, SubagentStart, Stop |

Each module ships at `layers/{module}/` with module.js + validate.sh.

## The 7 Hooks That Ship

| # | Script | CC Event | Matcher | Layer | Behavior |
|---|---|---|---|---|---|
| 1 | block-fab-files.js | PreToolUse | Write\|Edit\|MultiEdit | HookLayer | 12-regex pattern detector; stderr+exit 2 on match (post-16 §4.2 verbatim) |
| 2 | read-before-edit.js | PreToolUse | Edit\|MultiEdit | HookLayer | Tracks Read events; warns on unread Edit |
| 3 | validation-not-compilation.js | PostToolUse | Bash | HookLayer | Reminds: build success ≠ functional validation |
| 4 | evidence-gate-reminder.js | PreToolUse | TaskUpdate | HookLayer | 5-question checklist on completion claim |
| 5 | skill-activation-check.js | UserPromptSubmit | * | InvocationLayer | Hints matching skills via stderr |
| 6 | validation-skill-tripwire.js | PostToolUse | Bash | InvocationLayer | Escalates skill-skip after build success → exit 2 + tripwires.jsonl |
| 7 | stop-task-semantics.js | Stop | * | DispatchLayer | Classifies Stop as taskComplete/intermediate; blocks intermediate with open tasks |

Plus `subagent-governance-inject.js` (DispatchLayer) registers against PreToolUse:Task\|Agent for subagent injection.

## Plugin Install Command

```
# 1. Declare marketplace in ~/.claude/settings.json:
#    "extraKnownMarketplaces": {
#      "shannon-local": {
#        "source": { "path": "/Users/nick/Desktop/shannon-framework", "source": "directory" }
#      }
#    }

# 2. Install
/plugin install shannon@shannon-local
```

NO install_local.sh. NO cp -r into ~/.claude/{hooks,skills,agents}/. Plugin install is the only sanctioned flow.

## Top 3 Functional Validation Gates Phase 5 Must Prove

### Gate G1: Hook Wiring Proof
- Install plugin, boot real CC session via `claude --headless`.
- Send these tool calls in sequence: SessionStart → UserPromptSubmit ("build the app") → Bash(npm run build) → TaskUpdate(status=completed) → Stop.
- Assert: each of the 7 hooks appears at least once in ~/.claude/logs/shannon/hooks.jsonl with correct event, matcher, decision, and ms.
- Evidence: e2e-evidence/end-to-end/hooks-fired.jsonl, e2e-evidence/end-to-end/session.jsonl (lines cited).
- PASS criterion: 7/7 hooks observed with non-zero ms, no exceptions in hook-errors.jsonl.

### Gate G2: User Concern (a) — Validation Skill Tripwire Fires
- In same session, run `npm run build` (success), do NOT invoke `Skill tool with skill=functional-validation`.
- Assert: validation-skill-tripwire.js wrote TRIPWIRE: validation skill not invoked since build to stderr AND appended row to tripwires.jsonl AND exited 2.
- Evidence: e2e-evidence/end-to-end/tripwires.jsonl (line cited).
- PASS criterion: tripwire log entry present, stderr captured in session.jsonl <system-reminder> at correct turn.

### Gate G3: User Concern (b) — Premature Stop Blocked
- In same session, create 2 open TaskCreate items, write assistant message ending with "now I'll continue."
- Allow Stop to fire.
- Assert: stop-task-semantics.js classified as intermediate, exited 2, stderr contains "Stop deferred:" with 2 open tasks count.
- Evidence: e2e-evidence/end-to-end/stop-block.txt (stderr) + session.jsonl line for the Stop event.
- PASS criterion: exit 2 observed, CC honored the block (next assistant turn fired in same session, not new), stderr matches.

User concern (c) — hook observability — is covered by G1 (the logs.jsonl assertion).

## Non-Negotiables

- All hook output contracts = CC convention (stderr write + exit 2). No object-return `{ decision, message }`. (User DECISION 2; legacy pattern in REMAINING-GAPS.md.)
- Real plugin install. No install_local.sh.
- Per-hook try/catch wrap with process.exit(0) on crash + log to hook-errors.jsonl.
- Sync hooks for PreToolUse, UserPromptSubmit, Stop, SubagentStart. PostToolUse may be async but ship sync.
- Per-hook budget: <100ms wall clock; no network.
- Evidence-gated PASS: every validate.sh exits non-zero on any assertion fail. Phase 5 verdict cites file+line ranges, not directories.

## Reading Order for Phase 2

1. SHANNON-SPEC.md §1-2 (identity + layer model)
2. SHANNON-SPEC.md §3 (hook system)
3. SHANNON-SPEC.md §4-5 (plugin + CC integration)
4. GAP-MATRIX.md Priority 1 (BLOCKERS — that's your Phase 2 backlog)
5. CLAIM-RECONCILIATION.md §3, §5 (LEGACY-DROPPED + per-snippet status)

## Reading Order for Phase 3

1. SHANNON-SPEC.md §2.A then §2.B
2. CLAIM-RECONCILIATION.md §8 (layer-realization mapping — which edges hold)
3. GAP-MATRIX.md Priority 2 (HIGH — most layer-module deliverables)
4. Then write docs/seven-layer-overlay.md per §2.B table

## Reading Order for Phase 4

1. SHANNON-SPEC.md §3 (hook spec, including §3.5 error isolation)
2. SHANNON-SPEC.md §4.2 (lifecycle)
3. SHANNON-SPEC.md §5 (CC integration)
4. GAP-MATRIX.md Priority 1 #B1-B12 (every hook impl is a row here)

## Reading Order for Phase 5

1. SHANNON-SPEC.md §6 (validation strategy)
2. GAP-MATRIX.md every row's Validation Method column
3. THIS file Gates G1, G2, G3

---

## Unresolved Questions (escalate before Phase 2)

These were not adjudicated by user DECISIONs 1-4 and surface contradictions that Phase 2 should not invent answers for:

**UQ1 — Skill manifest discovery path for skill-activation-check.js**
Hook needs to read installed-skill trigger patterns. Where does it find them?
- Option A: scan ~/.claude/skills/ glob each fire (slow but accurate)
- Option B: Shannon ships a precomputed registry at logs/shannon/skill-triggers.json updated on SessionStart
- Option C: settings.json plugin-list lookup
Recommendation: B (cache at SessionStart). Confirm with user.

**UQ2 — TaskList readout for stop-task-semantics.js**
Hook needs to know "how many open Task items remain." Where?
- Option A: parse the session JSONL backwards looking for last TaskCreate/TaskUpdate sequence (fragile, slow)
- Option B: Shannon ships its own TaskCreate/TaskUpdate hook pair that maintains a shared file ~/.claude/logs/shannon/open-tasks.txt
- Option C: rely on user-mode subprocess that reads CC task system (does not exist)
Recommendation: B for v6.0 (adds 2 small hooks; not in 7-script loadout). OR for v6.0 MVP: a regex-based heuristic on last 20 lines of session.jsonl. Confirm scope with user.

**UQ3 — Coexistence with OMC's existing Stop chain (12 scripts per A3 §6)**
User has reflexion's persistent-mode.mjs + code-simplifier.mjs already firing on Stop. Adding Shannon's stop-task-semantics.js makes 13. Is this acceptable, or does Shannon need to negotiate priority / replace?
Recommendation: Shannon ships as 13th hook in v6.0; document overhead in REMAINING-GAPS.md. Stop chain minimization → v6.1.

**UQ4 — Marketplace declaration is manual user step (not Shannon's responsibility)**
Spec assumes user adds `extraKnownMarketplaces.shannon-local` manually. Should Shannon ship a one-time install script that adds this line? VF does not; OMC's setup.sh does.
Recommendation: ship `scripts/setup.sh` that adds marketplace entry idempotently. Document; do not auto-run.

**UQ5 — Phase 3 skill / agent counts vs post-16's "5 hooks, 1 skill, 1 agent template"**
Spec says Phase 3 ships small set TBD. Phase 3 lead must decide:
- Honor post-16:417 exactly: 1 skill (functional-validation) + 1 agent template
- Or ship 3-5 skills covering the doctrinal mandates
Recommendation: 1 skill + 1 agent for v6.0; expand v6.1.

**UQ6 — Numeric reproduction telemetry**
GAP-MATRIX Priority 3 M3/M4 defer to "Phase 6+ telemetry build-out." But CLAIM-RECONCILIATION marks all rate promises ASPIRATIONAL. If we never build telemetry, rates stay ASPIRATIONAL forever. Is that acceptable?
Recommendation: yes for v6.0. Add explicit caveat in posts (REQUIRES-POST-EDIT row in CLAIM-RECONCILIATION §6).

---

## Phase 1 Status

Task #5: COMPLETED.

Synthesized artifacts:
- SHANNON-SPEC.md (391 lines)
- CLAIM-RECONCILIATION.md (≈200 lines)
- GAP-MATRIX.md (≈100 lines)
- HANDOFF.md (this file)

All four files at /Users/nick/Desktop/shannon-framework/spec/.

Phase 2 unblocked. Wait on UQ1-UQ6 adjudication or proceed with recommendations.

End of HANDOFF.md.
