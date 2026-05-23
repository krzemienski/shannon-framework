# SHANNON-V6-ARCHITECTURE.md — Single-Plugin Consolidation Architecture

**Status:** LOCKED 2026-05-23 (Phase 1 v2 pivot)
**Supersedes:** spec/_v1-archive/SHANNON-SPEC.md (v1 standalone-plugin design)
**Authority:** This file + COMMANDS + SKILLS-AGENTS + HOOKS + INVENTORY form v6 contract.

---

## §1. Vision

Shannon v6.0.0 is **THE single, fully-functional Claude Code plugin** that replaces 10+ currently installed plugins on this machine. Inspiration is lifted from those plugins (patterns, contracts, hook chains) but consolidated into one self-contained codebase Shannon owns.

**One namespace:** `/shannon:*`. No `/ck:*`, `/omc:*`, `/vf:*`, `/crucible:*`, `/cast:*`, `/alloy:*`, `/temper:*` survive. No co-existence-at-equal-rank.

**Replaces:**
| Plugin | Cache path | Why consolidated |
|---|---|---|
| oh-my-claudecode (OMC) | ~/.claude/plugins/cache/omc/oh-my-claudecode/4.13.6 | Biggest — owns orchestration (autopilot/ralph/team/ultrawork), 39 skills, 19 agents |
| validationforge (VF) | ~/.claude/plugins/cache/validationforge/validationforge/1.0.0 | Owns functional-validation + evidence-gates + no-mocks discipline + consensus engine, 19 cmds, 52 skills, 7 agents, 7 hooks |
| crucible | /Users/nick/Desktop/crucible/crucible-plugin | Evidence-gated completion, 3-reviewer + 3-oracle quorum, refusal discipline, 19 cmds, 12 skills, 11 agents |
| claude-hud | ~/.claude/plugins/cache/claude-hud/claude-hud/0.1.0 | Statusline (TS dist) — Shannon absorbs as statusline module |
| prd-generator | ~/.claude/plugins/prd-generator | PRD authoring — folds into Planning domain |
| planning-with-files | ~/.claude/plugins/cache/planning-with-files/planning-with-files/2.40.1 | Multi-platform planning skill — folds into Planning domain |
| reflexion | ~/.claude/plugins/cache/context-engineering-kit/reflexion/3.0.0 | critique/memorize/reflect — folds into Reflection domain |
| sadd | ~/.claude/plugins/cache/context-engineering-kit/sadd/3.0.0 | 10 subagent skills — folds into Dispatch domain |
| sdd | ~/.claude/plugins/cache/context-engineering-kit/sdd/3.0.0 | Empty placeholder; drop |
| kaizen | ~/.claude/plugins/cache/context-engineering-kit/kaizen/3.0.0 | 7 root-cause skills — folds into Reflection domain |
| anneal-cast | ~/.claude/plugins/cache/anneal-umbrella-dev/anneal-cast/0.1.0 | Tournament planning + 9 agents — folds into Planning domain |
| anneal-alloy | ~/.claude/plugins/cache/anneal-umbrella-dev/anneal-alloy/0.1.0 | Linear planning variant — folds into Planning domain |
| anneal-temper | ~/.claude/plugins/cache/anneal-umbrella-dev/anneal-temper/0.1.0 | Convergence planning variant — folds into Planning domain |
| deepest-plan | ~/.claude/plugins/cache/deepest-plan-dev/deepest-plan | Consensus + gates + synthesis planning — folds into Planning domain |
| start (the-startup) | ~/.claude/plugins/cache/the-startup/start/3.8.0 | specify/implement variants — overlaps Planning + Dispatch; absorbed |
| autoresearch | ~/.claude/plugins/cache/autoresearch/autoresearch/2.1.2 | research workflow — folds into Planning (research phase) |

Plugins NOT consolidated (kept disabled but available):
- IDE / language-specific (swift-engineering, expo-*, neon-postgres, supabase, cloudflare, vercel-pack, webflow-pack, shopify, tanstack)
- Pure content (content-studio, technical-content-creator, blog-* family)
- Browser tools (playwright, chrome-devtools, agent-browser)
- LSP servers (swift-lsp, gopls-lsp, pyright-lsp, rust-analyzer-lsp, typescript-lsp)

Reasoning: Shannon is the **agent governance framework**. Domain-specific helpers stay separate.

---

## §2. Plugin Manifest Layout

```
~/.claude/plugins/shannon-framework/    (or cache/shannon-local/shannon/6.0.0/)
├── .claude-plugin/
│   ├── plugin.json                     # name=shannon, version=6.0.0
│   └── marketplace.json
├── commands/                           # /shannon:* slash commands (see SHANNON-V6-COMMANDS.md)
│   ├── plan.md
│   ├── cook.md
│   ├── validate.md
│   ├── forge.md
│   ├── reflect.md
│   ├── team.md
│   ├── ... (~25 total)
├── skills/                             # Skill authoring units (see SHANNON-V6-SKILLS-AGENTS.md)
│   ├── functional-validation/SKILL.md
│   ├── evidence-gate/SKILL.md
│   ├── consensus-engine/SKILL.md
│   ├── ... (~20 total)
├── agents/                             # Agent profiles
│   ├── planner.md
│   ├── executor.md
│   ├── reviewer.md
│   ├── oracle.md
│   ├── ... (~10 total)
├── hooks/
│   ├── hooks.json                      # CC event → script registration (see SHANNON-V6-HOOKS.md)
│   ├── block-fab-files.js
│   ├── validation-not-compilation.js
│   ├── evidence-gate-reminder.js
│   ├── ... (~14 total)
├── modules/                            # Domain modules (organizing wrapper)
│   ├── orchestration/                  # commands/skills/agents wiring for orchestration domain
│   ├── validation/                     # validation domain
│   ├── completion/                     # evidence-gated completion (crucible-inspired)
│   ├── planning/                       # planning domain (anneal-inspired)
│   ├── reflection/                     # reflection domain (reflexion + kaizen)
│   ├── dispatch/                       # subagent dispatch (sadd-inspired)
│   └── statusline/                     # statusline + observability (hud-inspired)
├── layers/                             # 4 enforcement layer modules (core)
│   ├── context/                        # ContextLayer
│   ├── hook/                           # HookLayer
│   ├── invocation/                     # InvocationLayer
│   └── dispatch/                       # DispatchLayer
├── lib/                                # shared hook-runner, log utils
│   ├── hook-runner.js
│   └── logger.js
├── scripts/
│   ├── setup.sh                        # idempotent marketplace declaration + install
│   ├── uninstall-others.sh             # disable + remove the 10+ consolidated plugins
│   └── validate-all.sh                 # Phase 5 end-to-end gate
└── docs/
    ├── seven-layer-overlay.md          # 7-layer conceptual doc per v1 §2.B
    └── migration-from-omc-vf-crucible.md
```

The `modules/` directory is an **organizational wrapper only** — commands/skills/agents/hooks still register at the top-level `commands/`, `skills/`, etc. paths required by CC's plugin manifest. `modules/<domain>/` exists as documentation (which files belong to which domain) and may host module-private helpers.

---

## §3. Domain Modules

| # | Domain | Replaces | Commands | Skills | Agents | Hooks |
|---|---|---|---|---|---|---|
| 1 | Orchestration | OMC autopilot/ralph/team/ultrawork, start specify/implement | /shannon:cook, /shannon:team, /shannon:loop, /shannon:autopilot | autopilot-runner, team-coordinator, loop-runner | planner, executor, coordinator | skill-activation-check |
| 2 | Validation | VF validate/forge family, lynx audits | /shannon:validate, /shannon:audit, /shannon:fix | functional-validation, evidence-gate, no-mocks-discipline, visual-inspection | validator, evidence-capturer | block-fab-files, validation-not-compilation, evidence-quality-check, mock-detection |
| 3 | Completion | Crucible forge/autopilot/oracle, deepest-plan validation | /shannon:forge, /shannon:audit-completion, /shannon:resume | completion-gate, refusal-discipline, oracle-review, evidence-indexing, codebase-analysis, documentation-research | reviewer-a, reviewer-b, reviewer-c, oracle-1, oracle-2, oracle-3 | evidence-gate-reminder |
| 4 | Planning | anneal-cast/alloy/temper, planning-with-files, prd-generator, deepest-plan, autoresearch | /shannon:plan, /shannon:plan-tournament, /shannon:plan-converge, /shannon:research, /shannon:prd | plan-author, plan-tournament, plan-converge, research-validation, sequential-analysis, create-validation-plan | researcher, plan-author, red-teamer | plan-before-execute |
| 5 | Reflection | reflexion (critique/reflect/memorize), kaizen (analyse/why/root-cause-tracing/plan-do-check-act/cause-and-effect) | /shannon:reflect, /shannon:why, /shannon:retro | critique, reflect, memorize, root-cause-tracing, why, plan-do-check-act | critic, retrospective-analyst | (none — invoke-on-demand) |
| 6 | Dispatch | sadd (10 subagent skills), OMC subagent inheritance | /shannon:dispatch, /shannon:dispatch-parallel, /shannon:dispatch-competitive | dispatch-sequential, dispatch-parallel, dispatch-competitive, judge, judge-with-debate, tree-of-thoughts | dispatch-judge | subagent-governance-inject, stop-task-semantics |
| 7 | Statusline + Observability | claude-hud (TS dist), OMC trace | /shannon:status, /shannon:doctor, /shannon:trace | statusline-config, observability-report | (none — passive instrumentation) | statusline-emit, hooks-fired-log |

Each domain folds into the 4 enforcement layers below.

---

## §4. The 4 Enforcement Layers

(Unchanged from v1 §2.A. Each domain's commands/skills/agents/hooks plug into these layers.)

| Layer | Module owns | Domains contributing |
|---|---|---|
| **1. ContextLayer** | SessionStart inject (global CLAUDE.md + project + rules/*.md), skill-trigger cache | All domains (skills + agents loaded; planner/researcher/critic available from turn one) |
| **2. HookLayer** | Tool-boundary enforcement scripts | Validation (5 hooks), Completion (1 hook), Dispatch (1 hook), Planning (1 hook) |
| **3. InvocationLayer** | Skill hint + tripwire system | Orchestration (skill-activation-check), Validation (validation-skill-tripwire) |
| **4. DispatchLayer** | Subagent governance inject + Stop semantics | Dispatch (subagent-governance-inject, stop-task-semantics), Statusline (hooks-fired-log) |

**Composition rule:** at runtime, an event flows through layers in order 1→4. A SessionStart triggers ContextLayer only; a PostToolUse:Bash triggers HookLayer (validation-not-compilation) then InvocationLayer (validation-skill-tripwire); a Stop triggers DispatchLayer (stop-task-semantics) only.

---

## §5. Install / Uninstall Flow

### Atomic install (Shannon-on)

```
1. User clones repo to /Users/nick/Desktop/shannon-framework (or installs via marketplace)
2. User adds to ~/.claude/settings.json:
     "extraKnownMarketplaces": {
       "shannon-local": { "source": { "path": "/Users/nick/Desktop/shannon-framework", "source": "directory" } }
     }
3. User runs: /plugin install shannon@shannon-local
4. CC clones to ~/.claude/plugins/cache/shannon-local/shannon/6.0.0/
5. CC reads plugin.json + hooks/hooks.json; registers Shannon hooks
6. Next SessionStart → Shannon ContextLayer fires → injects governance
7. Run scripts/setup.sh (idempotent: writes marketplace declaration, prompts user before uninstalling others)
```

### Atomic uninstall others (Shannon-replaces)

`scripts/uninstall-others.sh` performs:

```
1. Print plan: "About to disable: omc, vf, crucible, claude-hud, prd-generator, planning-with-files, reflexion, sadd, sdd, kaizen, anneal-cast, anneal-alloy, anneal-temper, deepest-plan, start, autoresearch"
2. Prompt for confirmation (no -y flag → exit 1 on no)
3. For each plugin slug above:
     - settings.json: set enabledPlugins["<slug>"] = false
     - settings.json: remove extraKnownMarketplaces entry if marketplace is single-purpose
4. Print diff of changed settings.json sections
5. Tell user: restart CC for changes to take effect
```

Plugins NOT touched: any IDE/language tools, content plugins, browser tools, LSP servers (per §1 keep list).

### Rollback

`scripts/rollback.sh`:
- Re-enables all plugins that uninstall-others.sh disabled (reads a backup written before disable).
- Does NOT remove Shannon (user must `/plugin uninstall shannon@shannon-local` manually).

---

## §6. Coexistence-During-Transition Strategy (Optional, Not Default)

Default: full replacement (§5). Optional: parallel mode for users who want to A/B test.

In parallel mode:
- Shannon installs alongside OMC/VF/Crucible.
- Shannon hook scripts use distinct log paths (`~/.claude/logs/shannon/*`) — no collision with VF (`~/.claude/logs/vf/*`) or OMC (`~/.claude/logs/omc/*`).
- Shannon command namespace `/shannon:*` is exclusive — never alias to existing `/ck:*` or `/vf:*`.
- The 12-script OMC Stop chain (auditor-3 §6) gains a 13th: Shannon `stop-task-semantics.js`. Documented as overhead; not a blocker for v6.0 parallel mode.

Recommendation: ship parallel mode in `scripts/setup.sh --parallel`. Default `setup.sh` triggers `uninstall-others.sh`.

---

## §7. Migration Matrix (high-level — full per-command map in SHANNON-V6-INVENTORY.md)

| User invokes today | Shannon v6 equivalent |
|---|---|
| /oh-my-claudecode:autopilot | /shannon:autopilot |
| /oh-my-claudecode:ralph | /shannon:loop |
| /oh-my-claudecode:team | /shannon:team |
| /oh-my-claudecode:ultrawork | /shannon:ultrawork |
| /oh-my-claudecode:plan | /shannon:plan |
| /oh-my-claudecode:trace | /shannon:trace |
| /oh-my-claudecode:omc-doctor | /shannon:doctor |
| /validationforge:validate | /shannon:validate |
| /validationforge:forge-execute | /shannon:forge |
| /validationforge:validate-consensus | /shannon:audit-consensus |
| /validationforge:validate-fix | /shannon:fix |
| /crucible:forge | /shannon:forge (Shannon's forge ABSORBS crucible's evidence quorum) |
| /crucible:autopilot | /shannon:autopilot (Shannon's autopilot ABSORBS crucible's refusal loop) |
| /crucible:resume | /shannon:resume |
| /crucible:status | /shannon:doctor (composite) |
| /anneal-cast:anneal | /shannon:plan-tournament |
| /anneal-alloy:anneal | /shannon:plan |
| /anneal-temper:anneal | /shannon:plan-converge |
| /deepest-plan:deepest | /shannon:plan-deep |
| /reflexion:reflect | /shannon:reflect |
| /reflexion:critique | (folded into /shannon:reflect --mode=critique) |
| /sadd:do-in-parallel | /shannon:dispatch-parallel |
| /sadd:do-competitively | /shannon:dispatch-competitive |
| /claude-hud:setup | /shannon:status setup |
| /claude-hud:configure | /shannon:status configure |
| /prd-generator (slash) | /shannon:prd |
| /planning-with-files:* | /shannon:plan (absorbed) |

---

## §8. Constraints (locked decisions still hold)

- Real loadable plugin via `.claude-plugin/plugin.json` + `hooks/hooks.json` (NOT install_local.sh). [Decision 3]
- Hook contract: stderr+exit 2 (CC convention). [Decision 2]
- 4 enforcement layers + 7-layer conceptual overlay (Path C). [Decision 1]
- KISS: ship only commands users actually invoke per auditor-3 session evidence. Aspirational commands (e.g. /ck:scout never invoked) DROP.

---

## §9. Unresolved Questions (v2-level)

| UQ | Question | Recommendation |
|---|---|---|
| UQ-V2-1 | Does Shannon claim OMC's 307-skill catalog wholesale or curate? | Curate to ~20. The 307-skill catalog is auditor-3 evidence of skill-catalog bloat (invocation rate <1%); don't reproduce the disease. |
| UQ-V2-2 | Should Shannon ship MCP servers (sequential-thinking, stitch, chrome-devtools)? | NO. MCP servers remain external dependencies; Shannon only audits MCP tool calls (DispatchLayer). |
| UQ-V2-3 | Per-domain versioning vs single Shannon version? | Single. v6.0.0 covers all domains. Per-domain feature flags via settings can come in v6.1. |
| UQ-V2-4 | Statusline language: keep claude-hud's TS or rewrite? | Borrow claude-hud's dist/ as a vendored module (cite borrow); don't rewrite in v6.0. Statusline is non-critical-path; reuse is KISS. |
| UQ-V2-5 | Does Shannon ship a TaskCreate/TaskUpdate event listener pair (UQ2 from v1 HANDOFF)? | YES. Lives in DispatchLayer. Maintains `~/.claude/logs/shannon/open-tasks.txt` consumed by stop-task-semantics.js. |
| UQ-V2-6 | UQ6 (numeric promises path) — what's the recommendation? | NOT in v6.0. Numeric promises (87%, 7ms, 9.6:1) remain ASPIRATIONAL; posts must add date-stamped caveat. Telemetry build-out = v6.1+. |
| UQ-V2-7 | Does Shannon ship a /shannon:install command that triggers setup.sh? | YES. Wrap setup.sh + uninstall-others.sh in /shannon:install. Plus /shannon:rollback. |

---

End of SHANNON-V6-ARCHITECTURE.md.
