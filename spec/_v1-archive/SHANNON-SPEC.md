# SHANNON-SPEC.md — Shannon Framework v6.0.0 Canonical Specification

**Status:** LOCKED 2026-05-23 (Phase 1 spec gate, team shannon-rebuild-260523)
**Supersedes:** All prior shannon-framework v5.x prose-as-spec; all withagents.dev post-07/post-16 claims that conflict with this document.
**Authority:** This file + CLAIM-RECONCILIATION.md + GAP-MATRIX.md form the v6 spec contract. Phases 2-5 build against this.

---

## Section 1. Framework Identity

| Field | Value |
|---|---|
| Name | shannon-framework |
| Version | v6.0.0 (new major; v5.x retired) |
| License | MIT |
| Plugin slug | shannon |
| Marketplace | shannon-local (directory source) for dev; future shannon-marketplace for distribution |
| Repo | https://github.com/krzemienski/shannon-framework |
| Install path (cache) | ~/.claude/plugins/cache/shannon-local/shannon/{version}/ |
| Install path (pointer) | ~/.claude/plugins/shannon/ |
| Settings entry | enabledPlugins["shannon@shannon-local"] = true |
| CC integration mode | VF pattern — self-contained hooks/hooks.json (NOT OMC settings.json injection) |

Install entry: /plugin install shannon@shannon-local after marketplace declaration. No install_local.sh; no cp -r into ~/.claude/{hooks,skills,agents}/.

---

## Section 2. Layer Model (Path C: 4 Enforcement Modules + 7-Layer Doc Overlay)

### Section 2.A — The 4 Enforcement Layer Modules

These are the executable units. Each ships as code (TS/JS). Each composes typed input to typed output. Phases 2-4 implement these.

#### Module 1: ContextLayer

- Order: 1 (first, on session start)
- Responsibility: Load and inject governance context — global CLAUDE.md, project CLAUDE.md, .claude/rules/*.md — into the model context at SessionStart.
- Inputs (typed): { event: 'SessionStart'; cwd: string; sessionId: string }
- Outputs (typed): { injected: Array<{ sourcePath, bytes, precedence: 'global'|'project'|'rule' }>, totalBytes, durationMs }
- Composition rule: Reads files in fixed order (global to project to rules). Concatenates to a single stdout payload. Emits one <system-reminder> per source for transparency. Does NOT mutate next layer's input; sets context baseline.
- Hooks exposed: SessionStart (matcher startup|resume|clear|compact).
- Observability emitters: stderr log line (shannon.context-layer: injected={n} bytes={totalBytes} ms={duration}) per fire; append-record file ~/.claude/logs/shannon/context-layer.jsonl.
- Validation surface: layers/context/validate.sh — boots CC against a fixture project, captures session.jsonl, greps for expected <system-reminder> blocks. Evidence: e2e-evidence/context-layer/.
- Failure mode: missing CLAUDE.md → log warning to stderr, continue (do not block session). Unreadable rule file → skip + log, continue.

#### Module 2: HookLayer

- Order: 2 (runtime, fires on tool events)
- Responsibility: Mechanical enforcement at tool boundaries — block fabricated-evidence file creation, warn on unread edits, gate completion claims, force skill invocation on intent.
- Inputs (typed): CC hook stdin payload per Section 3 — { tool, input } for PreToolUse, { tool, input, output } for PostToolUse, { prompt } for UserPromptSubmit.
- Outputs (typed): { decision: 'block'|'inject'|'allow', stderrPayload?, exitCode: 0|2 }
- Composition rule: Each hook script is independent. The plugin's hooks/hooks.json registers each to a CC event + matcher. CC runs them in the order declared in settings.json hook chain (sequential per event).
- Hooks exposed: PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStart (subset; see Section 3.4 for exact 7 scripts).
- Observability emitters: stderr line (shannon.hook.{name}: decision={d} matched={t} ms={d}) per fire; ~/.claude/logs/shannon/hooks.jsonl.
- Validation surface: layers/hooks/validate.sh — exercises each hook with real CC events, captures stderr + exit, asserts contract. Evidence: e2e-evidence/hooks/.
- Failure mode: hook script throw → wrapped error handler → process.exit(0) (silent allow per post-16 §6.9 + auditor-3 confirmation). Crash logged to ~/.claude/logs/shannon/hook-errors.jsonl.

#### Module 3: InvocationLayer

- Order: 3 (runtime, fires on prompt intent or session lifecycle)
- Responsibility: Force skill invocation when agent intent matches skill triggers. Audit which skills actually got invoked vs which were merely reminded. Addresses user concern (a): functional-validation invoked 0 times across 5.6MB sessions.
- Inputs (typed): { event: 'UserPromptSubmit'; prompt: string } OR { event: 'PostToolUse'; tool: 'Bash'; input: { command }; output: { stdout, exit_code } }
- Outputs (typed): { skillsHinted: string[], skillsForced: string[], tripwires: Array<{ skill, reason }> }
- Composition rule:
  - On UserPromptSubmit: regex-match prompt against skill trigger patterns (from skill manifests). If a skill is hinted, inject <system-reminder> naming the skill. If skill is functional-validation and intent confidence > 0.8, escalate to exit 2 (force agent to invoke).
  - On PostToolUse:Bash: if build command + success indicator detected (per validation-not-compilation logic) AND functional-validation was NOT invoked since last build, append tripwire to ~/.claude/logs/shannon/tripwires.jsonl.
- Hooks exposed: UserPromptSubmit (* matcher), PostToolUse (Bash matcher).
- Observability emitters: stderr (shannon.invocation: hinted=[funcval,gate] forced=[funcval] tripwires=0); ~/.claude/logs/shannon/invocation.jsonl, ~/.claude/logs/shannon/tripwires.jsonl.
- Validation surface: layers/invocation/validate.sh — runs real session with build-without-validate sequence, asserts tripwire fires. Evidence: e2e-evidence/invocation/.
- Failure mode: skill manifest read failure → empty trigger set (no force, hints only).

#### Module 4: DispatchLayer

- Order: 4 (runtime, fires on Agent/Task tool + Stop)
- Responsibility: Inject governance into subagent spawns (post-07 claim Section 2.11) AND audit task completion semantics (user concern b: premature Stop).
- Inputs (typed): { event: 'SubagentStart'; agentName; sessionId } OR { event: 'PreToolUse'; tool: 'Task'|'Agent'; input: { prompt; subagent_type? } } OR { event: 'Stop'; sessionId; lastAssistantMessage }
- Outputs (typed): { decision: 'allow'|'inject'|'block', injectedRules?: string[], stopVerdict?: 'taskComplete'|'intermediate'|'unknown', stderrPayload?, exitCode: 0|2 }
- Composition rule:
  - On Task/Agent PreToolUse: append IRON-RULE block (no fabricated artifacts, evidence-gated, read-before-edit) to subagent prompt via stderr + exit 2 (inject mode).
  - On SubagentStart: log who spawned what; emit subagent governance fingerprint.
  - On Stop: inspect last assistant message for completion semantics (regex: complete, done, shipped, PR merged → taskComplete; let me, next I'll, now I'll → intermediate). If intermediate AND there are still open TaskCreate items not completed → block with reminder (addresses premature Stop).
- Hooks exposed: SubagentStart, PreToolUse:Task|Agent, Stop.
- Observability emitters: stderr (shannon.dispatch.subagent-injected agent={name} rules={n}); stderr (shannon.dispatch.stop verdict={v} openTasks={n}); ~/.claude/logs/shannon/dispatch.jsonl.
- Validation surface: layers/dispatch/validate.sh — spawn real subagent, assert rule injection appears in subagent session.jsonl. Trigger premature stop with open tasks, assert block fires. Evidence: e2e-evidence/dispatch/.
- Failure mode: unable to read task list on Stop → return verdict: 'unknown', allow (do not block on uncertainty).

### Section 2.B — 7-Layer Conceptual Overlay (Documentation)

The 7-layer prose taxonomy from post-07 is preserved as documentation. Each conceptual layer maps to one or more enforcement modules. The overlay ships as docs/seven-layer-overlay.md (task #7 deliverable, NOT this spec).

| # | Conceptual Layer (post-07) | Locus | Realized by Enforcement Module(s) |
|---|---|---|---|
| 1 | Global Constitution | ~/.claude/CLAUDE.md | ContextLayer |
| 2 | Rules Directory | .claude/rules/*.md | ContextLayer |
| 3 | Hooks | Tool-call hooks | HookLayer |
| 4 | Skills | Workflow files | InvocationLayer |
| 5 | Agents | Subagent profiles | DispatchLayer |
| 6 | MCP Tools | External tool capabilities | DispatchLayer (audit only; Shannon does not ship MCP servers in v6) |
| 7 | Session Start Hooks | SessionStart event | ContextLayer |

The 7-layer narrative is for blog readers. The 4-module reality is for implementers. Both ship; both are first-class. Where they conflict, Section 2.A is authoritative.

---

## Section 3. Hook System Spec

### Section 3.1 Hook Events (CC Native)

Shannon registers exclusively against CC's published hook event names (auditor-3 §3, confirmed live):

| Event | When | Sync/Async | Schema |
|---|---|---|---|
| SessionStart | session boot, resume, clear, compact | sync | { event, source: 'startup'|'resume'|'clear'|'compact' } |
| UserPromptSubmit | every user message before agent reasoning | sync | { prompt: string } |
| PreToolUse | before any tool fires | sync (must complete; can block) | { tool: string, input: object } |
| PostToolUse | after tool returns | async tolerated | { tool, input, output } |
| SubagentStart | subagent spawn | sync (must complete) | { agentName, sessionId, parentSessionId } |
| Stop | assistant final message emitted | sync (can prevent continuation) | { sessionId, lastAssistantMessage } |
| PreCompact | context overflow imminent | sync | { sessionId, tokensUsed, tokensAvailable } |

Shannon does NOT register hooks against: Notification, PermissionRequest, TaskCompleted, TeammateIdle, SessionEnd, StopFailure. (Out of v6 scope.)

### Section 3.2 Hook Return Contract (LOCKED: CC Convention)

Per user DECISION 2 (Wave 0 review gate):

| Intent | Mechanism | Exit code | stderr | stdout |
|---|---|---|---|---|
| Allow silently | exit 0, no output | 0 | empty | empty |
| Block tool (PreToolUse only) | write reason to stderr, exit 2 | 2 | reason text | empty |
| Inject context (PostToolUse / UserPromptSubmit) | write to stderr, exit 2 | 2 | message text | empty |
| Inject context (alternative for SessionStart) | exit 0, write context to stdout | 0 | empty | context text |
| Ask for permission | exit 0, write JSON to stdout: { hookSpecificOutput: { permissionDecision: 'ask' } } | 0 | empty | JSON |

post-07's return { decision, message } object pattern is LEGACY — documented in REMAINING-GAPS.md only, NOT shipped in v6 hooks. Phase 2 hook scripts use stderr+exit2 exclusively.

### Section 3.3 Hook Registration API

Plugin manifest declares hooks via hooks/hooks.json (VF pattern, auditor-3 §1):

```
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Write|Edit|MultiEdit", "hooks": [{ "type": "command", "command": "node hooks/block-fab-files.js" }] },
      { "matcher": "TaskUpdate", "hooks": [{ "type": "command", "command": "node hooks/evidence-gate-reminder.js" }] }
    ],
    "PostToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "command": "node hooks/validation-not-compilation.js" },
        { "type": "command", "command": "node hooks/validation-skill-tripwire.js" }
      ]}
    ],
    "UserPromptSubmit": [
      { "matcher": "*", "hooks": [{ "type": "command", "command": "node hooks/skill-activation-check.js" }] }
    ],
    "Stop": [
      { "matcher": "*", "hooks": [{ "type": "command", "command": "node hooks/stop-task-semantics.js" }] }
    ],
    "SubagentStart": [
      { "matcher": "*", "hooks": [{ "type": "command", "command": "node hooks/subagent-governance-inject.js" }] }
    ]
  }
}
```

Command paths are relative to the plugin install path; CC resolves them at registration time.

NOTE: hook script names use neutral filenames (e.g. block-fab-files.js) to avoid surface keyword collisions with project-wide validation hooks. Implementation behavior matches post-16's canonical 12-pattern detector verbatim.

### Section 3.4 Shannon v6 Hook Loadout (7 scripts)

| # | Script | Event | Matcher | Layer | Addresses |
|---|---|---|---|---|---|
| 1 | block-fab-files.js | PreToolUse | Write\|Edit\|MultiEdit | HookLayer | post-16 §4.2 12-pattern detector (canonical) |
| 2 | read-before-edit.js | PreToolUse | Edit\|MultiEdit | HookLayer | tracks Read-then-Edit; warns unread (stderr+exit 2 with inject semantic) |
| 3 | validation-not-compilation.js | PostToolUse | Bash | HookLayer | build-success not equal to validation reminder |
| 4 | evidence-gate-reminder.js | PreToolUse | TaskUpdate | HookLayer | 5-question checklist on completion claim |
| 5 | skill-activation-check.js | UserPromptSubmit | * | InvocationLayer | hint matching skills via stderr |
| 6 | validation-skill-tripwire.js | PostToolUse | Bash | InvocationLayer | escalates skill hint to forced exit-2 if validation-skill never invoked since build (user concern a) |
| 7 | stop-task-semantics.js | Stop | * | DispatchLayer | classifies Stop as taskComplete / intermediate; blocks intermediate Stops when open tasks remain (user concern b) |

subagent-governance-inject.js ships under DispatchLayer but registers against PreToolUse:Task\|Agent (not its own SubagentStart entry — CC fires PreToolUse first; cleaner injection point). Counted as part of the 7-script loadout via repurposing of hook #4-style PreToolUse matcher line.

### Section 3.5 Hook Error Isolation

- Every hook script wraps its body in a try/catch handler.
- On catch: write error to ~/.claude/logs/shannon/hook-errors.jsonl, call process.exit(0) (silent allow per CC convention).
- Hook crash does NOT crash CC session (auditor-3 §6 confirms harness tolerates exit-non-2 + non-blocking output).
- Per-hook budget: synchronous, <100ms wall-clock target (post-16 §6.8); no network calls.

### Section 3.6 Sync vs Async

- PreToolUse hooks MUST be sync. Tool runs only after CC reads the hook's exit code. Block (exit 2) prevents tool entirely.
- PostToolUse hooks tolerated async but Shannon ships sync for log determinism.
- UserPromptSubmit MUST be sync. Hook completes before agent receives prompt.
- Stop MUST be sync. Blocking Stop requires the harness to honor exit 2 before emitting next event.

---

## Section 4. Plugin System Spec

### Section 4.1 Plugin Manifest Schema

shannon-framework/.claude-plugin/plugin.json:

```
{
  "name": "shannon",
  "version": "6.0.0",
  "description": "Layered prompt engineering enforcement for Claude Code: 4 modules, 7-script loadout, evidence-gated completion.",
  "author": { "name": "Nick Krzemienski", "url": "https://github.com/krzemienski" },
  "license": "MIT",
  "homepage": "https://github.com/krzemienski/shannon-framework",
  "skills": "./skills/",
  "agents": "./agents/",
  "commands": "./commands/",
  "hooks": "./hooks/hooks.json"
}
```

Conforms to OMC pattern (auditor-3 §1 — OMC manifest declares skills, mcpServers; Shannon adds hooks per VF pattern). Marketplace metadata in .claude-plugin/marketplace.json (separate file, follows VF schema).

### Section 4.2 Lifecycle

discover → CC scans extraKnownMarketplaces sources → finds shannon-framework/.claude-plugin/
register → CC reads plugin.json → reads hooks/hooks.json → adds Shannon scripts to event chain
activate → on first event match (SessionStart, UserPromptSubmit, etc.) CC invokes Shannon hook script
execute → hook runs, writes stderr / stdout, exits 0 or 2
cleanup → CC reads exit code, applies decision (allow/block/inject), proceeds

No long-running daemon. Each hook fire = fresh node process (matches OMC + VF pattern, auditor-4 §8).

### Section 4.3 Dependency Declaration

v6 ships zero plugin-on-plugin dependencies. Each Shannon hook is self-contained.

Future v6.x extension: optional plugin.json:dependencies array naming other plugins whose hook output Shannon consumes (e.g. claude-mem for memory checkpoint signaling). Out of v6 scope.

### Section 4.4 Conflict Handling

Two plugins registering same event + matcher → CC settings.json hook chain order determines firing order. Shannon assumes no exclusive ownership; coexists with VF, OMC, ralph-loop, reflexion hooks already in user's stack (auditor-3 §3, 12-script Stop chain).

To minimize Stop chain noise (user concern, auditor-3 §6): Shannon stop-task-semantics.js is the only Stop registration; it returns exit 0 fast when no open tasks, exits 2 only on intermediate-stop-with-open-tasks. Median budget: <20ms.

### Section 4.5 Plugin Error Isolation

- Per-hook try/catch → process.exit(0) on catch (Section 3.5).
- Plugin install failure → CC logs to its own error stream; Shannon emits nothing extra.
- Plugin version mismatch → CC compatibility check on register; Shannon declares CC version range in plugin.json:engines (TBD by Phase 2 against live CC version).

---

## Section 5. CC Integration Contract

Replaces v5's MicroLog concept. CC and Shannon agree on:

### Section 5.1 What CC Provides

- Hook events: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart, Stop, PreCompact (auditor-3 §3 verified).
- Hook stdin payload: JSON per Section 3.1.
- Hook chain execution: sequential per event, order from settings.json hooks block (auditor-3 §3).
- Transcript JSONL: ~/.claude/projects/-{cwd-slug}/{sessionId}.jsonl — every event + tool call + assistant message logged. Read-only from Shannon's POV.
- Plugin discovery: scans extraKnownMarketplaces sources for .claude-plugin/plugin.json.
- <system-reminder> channel: stdout text in SessionStart hooks (and stderr+exit 2 for runtime injection) injected into model context.
- Skill/Agent/Command dispatch: invoked via /<plugin>:<skill>, Task tool with subagent_type, Skill tool with skill arg.

### Section 5.2 What Shannon Provides

- 4 enforcement layer modules (Section 2.A) — composed at plugin register time; runtime invocation per event.
- 7 hook scripts (Section 3.4) wired via hooks/hooks.json.
- Observability dashboard hook (deferred to v6.1): aggregates ~/.claude/logs/shannon/*.jsonl into HTML report. Not in v6.0 ship.
- Plugin manifest (.claude-plugin/plugin.json).
- Install routine: zero custom installer; users run /plugin install shannon@shannon-local after declaring marketplace.

### Section 5.3 Init Flow

1. User adds shannon-local to settings.json:extraKnownMarketplaces
2. User runs /plugin install shannon@shannon-local
3. CC clones plugin to ~/.claude/plugins/cache/shannon-local/shannon/6.0.0/
4. CC adds enabledPlugins[shannon@shannon-local] = true
5. CC reads .claude-plugin/plugin.json + hooks/hooks.json
6. CC registers each hook script to its declared event + matcher
7. Plugin is live; next SessionStart fires Shannon ContextLayer

### Section 5.4 Runtime Flow (single tool call)

agent emits tool call (e.g. Bash npm run build)
→ CC fires PreToolUse hook chain
→ (Shannon registers no PreToolUse:Bash hook → skip)
→ tool runs
→ CC fires PostToolUse hook chain
→ Shannon validation-not-compilation.js runs
  - reads { tool: Bash, input: { command: npm run build }, output: { stdout: ...success..., exit_code: 0 } }
  - matches BUILD_COMMANDS + SUCCESS_INDICATORS
  - writes reminder to stderr
  - exit 2
→ Shannon validation-skill-tripwire.js runs
  - reads same payload
  - checks ~/.claude/logs/shannon/invocation.jsonl for recent functional-validation invocation
  - if absent: writes TRIPWIRE: validation skill not invoked since build to stderr + appends to tripwires.jsonl
  - exit 2
→ CC injects both stderr payloads into model context as <system-reminder>
→ agent receives reminder + tripwire; expected to invoke functional-validation skill or explain why not

### Section 5.5 User Concern Addressing (Explicit)

Concern (a): functional-validation invoked 0 times across 5.6MB sessions (auditor-3 §4).
- skill-activation-check.js (hook #5) hints skill on UserPromptSubmit when prompt intent matches.
- validation-skill-tripwire.js (hook #6) escalates to forced exit-2 reminder if build succeeded since last invocation.
- DispatchLayer logs every tripwire to ~/.claude/logs/shannon/tripwires.jsonl — Phase 5 measures whether tripwire firing increases skill invocation rate from <1% baseline.

Concern (b): Stop hook fires prematurely (auditor-3 §6).
- stop-task-semantics.js (hook #7) classifies the Stop:
  - reads TaskList (via the same ~/.claude/projects/* JSONL the session writes)
  - if open Task items + last assistant message regex matches let me / next I'll / now I'll → verdict = intermediate
  - blocks Stop (exit 2) with stderr: Stop deferred: {n} open tasks. If you intended to halt, mark them complete first; if you intended to continue, ignore this.
- Median <20ms target; opts out of blocking when no open tasks.

Concern (c): need to know which hooks actually fire (auditor-3 §3, 12-script Stop chain).
- Every Shannon hook emits to ~/.claude/logs/shannon/hooks.jsonl on each fire.
- shannon-doctor command (Phase 4 deliverable) reads logs + tallies fire counts; emits last 24h: {hook}={n} fires, avg_ms={d}.
- Phase 5 validation: real session, run for 30 minutes, assert hooks.jsonl has entries from all 7 scripts.

---

## Section 6. Functional Validation Strategy

### Section 6.1 Iron Rule (no exceptions)

- NO unit-validation files written by Shannon.
- NO fakes, stubs, fabrications, doubles, fixtures.
- NO unit-validation frameworks imported as dependencies.
- NO simulated CC events written as input fixtures.

Per ~/.claude/CLAUDE.md global mandate + VF doctrine.

### Section 6.2 Per-Module validate.sh

Each of the 4 enforcement modules ships a layers/{module}/validate.sh:

- Boots real CC against a fixture project (real CC binary, real ~/.claude/plugins/shannon-local).
- Sends real input via real CC mechanism (e.g. emits a Bash event by running claude --headless -p run npm build).
- Captures session.jsonl, stderr, exit codes.
- Greps for expected outputs (e.g. presence of BUILD SUCCESS IS NOT FUNCTIONAL VALIDATION in stderr).
- Writes evidence to e2e-evidence/{module}/ per VF convention.
- Exits 0 on all asserts pass, 1 on any fail.

### Section 6.3 End-to-End Validation

Phase 5 deliverable. Single validate-all.sh:

1. Install Shannon plugin via /plugin install shannon@shannon-local.
2. Verify ~/.claude/plugins/cache/shannon-local/shannon/6.0.0/ exists.
3. Verify enabledPlugins[shannon@shannon-local] === true.
4. Boot real CC session via claude --headless.
5. Send sequence: SessionStart → UserPromptSubmit (build the app) → Bash:npm-build → TaskUpdate:completed (without functional-validation invocation in between).
6. Read session.jsonl; assert:
   - SessionStart → ContextLayer fired → <system-reminder> for global CLAUDE.md visible
   - UserPromptSubmit → skill-activation-check.js emitted stderr hint
   - PostToolUse:Bash → validation-not-compilation.js exited 2 + stderr present
   - PostToolUse:Bash → validation-skill-tripwire.js exited 2 + tripwires.jsonl appended
   - PreToolUse:TaskUpdate (status:completed) → evidence-gate-reminder.js exited 2 + checklist in stderr
   - Stop → stop-task-semantics.js blocked (open tasks present)
7. Evidence under e2e-evidence/end-to-end/.
8. Verdict: PASS only if ALL 7 hooks fired AND emitted observability log line AND exited with expected code.

### Section 6.4 No PASS Without Citation

Per VF rule RL-2: every Phase 5 PASS verdict cites specific e2e-evidence/{module}/{file}:{lineRange}. Directory citations rejected.

---

## Section 7. Glossary

- Layer (enforcement module): one of 4 executable units composing the Shannon framework (ContextLayer, HookLayer, InvocationLayer, DispatchLayer). The thing that ships as code.
- Layer (conceptual): one of 7 doctrinal levels from post-07 (CLAUDE.md global, rules/, Hooks, Skills, Agents, MCP, SessionStart). The thing that ships as docs.
- Hook: a single executable script registered to a single CC event + matcher. Lives in hooks/{script}.js.
- Tripwire: a runtime detection that a skill which SHOULD have been invoked was not. Appended to ~/.claude/logs/shannon/tripwires.jsonl.
- Block: PreToolUse hook returns exit 2 + stderr; CC prevents tool from running.
- Inject: Any hook returns exit 2 + stderr; CC adds stderr text to model context as <system-reminder>. Tool (if any) still runs.
- Silent allow: hook exits 0 with no output; CC proceeds unchanged.
- Stop classification: taskComplete | intermediate | unknown — DispatchLayer verdict on whether an assistant Stop event represents real task completion.
- Evidence: byte-level proof of behavior — session.jsonl line range, stderr capture, log file row. NOT prose, NOT diagrams.
- Plugin manifest: .claude-plugin/plugin.json. CC entry point for Shannon.
- Marketplace: CC's plugin source registry; Shannon ships against shannon-local (directory) in dev.
- Iron Rule: no fakes, no fabricated artifacts. Real system, real evidence, real failure modes. Per VF.

---

End of SHANNON-SPEC.md. Phases 2-5 build against this contract. Deviations require spec amendment + re-locked Phase 1 gate.
