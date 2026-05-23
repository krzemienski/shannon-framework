# SHANNON-V6-INVENTORY.md — Plugin-by-Plugin Inventory + Migration Matrix

**Status:** LOCKED 2026-05-23
**Source:** /Users/nick/.claude/plugins/installed_plugins.json + /Users/nick/.claude/plugins/cache/* (159 plugins enabled per auditor-3 §1 + ls verification)
**Scope:** Inventory of every consolidation-target plugin + migration matrix to Shannon v6 surface.

---

## §1. Plugins Slated For Replacement (16)

### 1.1 oh-my-claudecode @ omc (v4.13.6)
- Cache path: `~/.claude/plugins/cache/omc/oh-my-claudecode/4.13.6/`
- Commands: 0 standalone .md files; commands are skill-bound (auto-invoke via `/oh-my-claudecode:<skill>`)
- Skills (39): ai-slop-cleaner, ask, autopilot, autoresearch, cancel, ccg, configure-notifications, debug, deep-dive, deep-interview, deepinit, external-context, hud, learner, mcp-setup, omc-doctor, omc-reference, omc-setup, omc-teams, plan, project-session-manager, ralph, ralplan, release, remember, sciomc, self-improve, setup, skill, skillify, team, trace, ultraqa, ultrawork, verify, visual-verdict, wiki, writer-memory + AGENTS.md
- Agents (19): analyst, architect, code-reviewer, code-simplifier, critic, debugger, designer, document-specialist, executor, explore, git-master, planner, qa-tester, scientist, security-reviewer, test-engineer, tracer, verifier, writer
- Hooks: 1 file (hooks.json — wires settings.json-style injection rather than CC hooks.json)
- Replacement: see §3 mapping. ~14 OMC skills absorbed; rest dropped.

### 1.2 validationforge @ validationforge (v1.0.0)
- Cache path: `~/.claude/plugins/cache/validationforge/validationforge/1.0.0/`
- Commands (19): forge-benchmark, forge-execute, forge-install-rules, forge-plan, forge-setup, forge-team, validate, validate-audit, validate-benchmark, validate-ci, validate-consensus, validate-dashboard, validate-fix, validate-plan, validate-sweep, validate-team, validate-team-dashboard, vf-setup, vf-telemetry
- Skills (52): see auditor-3 §1 / ARCHITECTURE.md §1 — full list in cache
- Agents (7): consensus-synthesizer, consensus-validator, evidence-capturer, platform-detector, sweep-controller, validation-lead, verdict-writer
- Hooks (7 scripts + hooks.json): block-test-files.js, completion-claim-validator.js, evidence-gate-reminder.js, evidence-quality-check.js, mock-detection.js, validation-not-compilation.js, validation-state-tracker.js
- Replacement: see §3. 5 hooks absorbed verbatim; 1 renamed; 1 dropped. 6 skills absorbed; 32 dropped (platform-specific folded into `validator` agent dispatch).

### 1.3 crucible @ crucible-local
- Source path: `/Users/nick/Desktop/crucible/crucible-plugin/`
- Commands (19): agent-new, audit, autopilot, command-new, doctor, explain, fix, forge, graph, hook-new, plan-and-execute, remediate, resume, rule-new, skill-new, stack-new, status, trial, validate
- Skills (12): codebase-analysis, completion-gate, disable, documentation-research, enable, evidence-indexing, oracle-review, planning, session-log-audit, setup, skill-enrichment, validation
- Agents (11): codebase-analyst, documentation-researcher, oracle-auditor-1/2/3, planner, reviewer-a/b/c, skill-discoverer, validator
- Hooks: 1 hooks.json
- Replacement: see §3. 6 skills + 6 agent slots absorbed; meta-plugin-development commands (rule-new/hook-new/skill-new/command-new/agent-new/stack-new/graph/trial/explain/fix) DROPPED — out of v6 scope.

### 1.4 claude-hud @ claude-hud (v0.1.0)
- Cache path: `~/.claude/plugins/cache/claude-hud/claude-hud/0.1.0/`
- Commands (2): setup, configure
- Skills: 0
- Agents: 0
- Hooks: 0
- Source: TS compiled to dist/ (vendored as-is in Shannon's `modules/statusline/`)
- Replacement: /shannon:status setup, /shannon:status configure (composite command per SHANNON-V6-COMMANDS.md #23).

### 1.5 prd-generator @ prd-generator
- Source path: `~/.claude/plugins/prd-generator/`
- Commands: present (count unknown without ls; commands/ dir exists)
- Skills: 0
- Replacement: /shannon:prd (single command).

### 1.6 planning-with-files @ planning-with-files (v2.40.1)
- Cache path: `~/.claude/plugins/cache/planning-with-files/planning-with-files/2.40.1/`
- Notable: ships multi-platform variants (.cursor/, .gemini/, .mastracode/, .continue/, .opencode/, .codex/) — the CC variant is mostly empty
- Replacement: /shannon:plan (linear). Most of planning-with-files' content was platform-agnostic doc; not load-bearing for v6.

### 1.7 reflexion @ context-engineering-kit (v3.0.0)
- Cache path: `~/.claude/plugins/cache/context-engineering-kit/reflexion/3.0.0/`
- Commands: 0
- Skills (3): critique, memorize, reflect
- Hooks: 1 hooks dir (with src/ subdir, bun.lockb, package.json — Bun runtime)
- Agents: 0
- Replacement: all 3 skills absorbed (SHANNON-V6-SKILLS-AGENTS.md #15-17). Bun-runtime hooks DROPPED — Shannon hooks are pure node.

### 1.8 sadd @ context-engineering-kit (v3.0.0)
- Cache path: `~/.claude/plugins/cache/context-engineering-kit/sadd/3.0.0/`
- Commands: 0
- Skills (10): do-and-judge, do-competitively, do-in-parallel, do-in-steps, judge, judge-with-debate, launch-sub-agent, multi-agent-patterns, subagent-driven-development, tree-of-thoughts
- Agents: present (dir exists)
- Replacement: 4 skills absorbed (dispatch-parallel, judge, judge-with-debate, tree-of-thoughts); 6 dropped (folded into /shannon:dispatch* commands).

### 1.9 sdd @ context-engineering-kit (v3.0.0)
- Cache path: `~/.claude/plugins/cache/context-engineering-kit/sdd/3.0.0/`
- Commands: 0; Skills: 0 (empty in inventory)
- Replacement: DROPPED entirely; nothing to absorb.

### 1.10 kaizen @ context-engineering-kit (v3.0.0)
- Cache path: `~/.claude/plugins/cache/context-engineering-kit/kaizen/3.0.0/`
- Commands: 0
- Skills (7): analyse, analyse-problem, cause-and-effect, kaizen, plan-do-check-act, root-cause-tracing, why
- Replacement: 2 absorbed (root-cause-tracing absorbs 5 cousins; plan-do-check-act kept distinct). 5 dropped (folded).

### 1.11 anneal-cast @ anneal-umbrella-dev (v0.1.0)
- Cache path: `~/.claude/plugins/cache/anneal-umbrella-dev/anneal-cast/0.1.0/`
- Commands (1): anneal
- Skills (7): atlas, hephaestus, metis, momus, oracle, prometheus-cast, red-team-trinity
- Agents (9): atlas, hephaestus, metis, momus, oracle, prometheus-cast, redteam-assumptions, redteam-scope, redteam-security
- Hooks: 1 hooks dir
- Replacement: /shannon:plan-tournament. Skills/agents folded into `plan-tournament` skill + `red-teamer` agent (single agent with `--lens` arg per UQ-SA-1 recommendation).

### 1.12 anneal-alloy @ anneal-umbrella-dev (v0.1.0)
- Skills: 1 (linear plan variant)
- Replacement: /shannon:plan (default linear).

### 1.13 anneal-temper @ anneal-umbrella-dev (v0.1.0)
- Skills: 1 (convergence variant)
- Replacement: /shannon:plan-converge.

### 1.14 deepest-plan @ deepest-plan-dev
- Cache: present in marketplace cache (per auditor-3 §1 list)
- Skills (15+): cli-validation, baseline-quality-assessment, gate-validation-discipline, deepest-plan, fullstack-validation, condition-based-waiting, preflight, api-validation, ios-validation, parallel-validation, e2e-validate, web-validation, verification-before-completion, responsive-validation, create-validation-plan, error-recovery, accessibility-audit, functional-validation, no-mocking-validation-gates
- Replacement: /shannon:plan-deep. Most skills are duplicates of VF's (vendor-by-vendor); folded into `validator` agent dispatch + existing v6 skills.

### 1.15 start @ the-startup (v3.8.0)
- Skills: validate, implement-incremental, specify-incremental, specify-requirements, test, brainstorm, specify-factory, implement, implement-direct, implement-factory, specify, specify-solution, specify-meta, refactor, analyze, constitution, debug, document, writing-skills, review
- Replacement: specify-* family → /shannon:plan + /shannon:prd. implement-* family → /shannon:cook. validate → /shannon:validate. Most other skills DROPPED (refactor/analyze/constitution/document/writing-skills — out of v6 scope).

### 1.16 autoresearch @ autoresearch (v2.1.2)
- Cache path: `~/.claude/plugins/cache/autoresearch/autoresearch/2.1.2/`
- Commands + Skills + Hooks present
- Replacement: /shannon:research command + `researcher` agent. Skills folded.

---

## §2. Plugins NOT Replaced (Kept Disabled But Available)

Per ARCHITECTURE §1 keep list. Domain-specific or runtime-specific tools:

### Language/IDE LSPs
- swift-lsp, gopls-lsp, pyright-lsp, rust-analyzer-lsp, typescript-lsp — kept as-is (LSP integration)

### Domain helpers
- swift-engineering, expo-app-design, expo-deployment, expo, upgrading-expo, neon-postgres, supabase-pack, cloudflare, vercel-pack, webflow-pack, replit-pack, together-pack, anthropic-pack, cursor-pack — kept

### Content tools
- content-studio (techwolf), technical-content-creator, ai-firstify, all blog-* family, podcast-blog-post-creator, blog-post-writer, youtube-thumbnail-design — kept

### Browser tools
- playwright, playwright-skill, chrome-devtools-mcp, agent-browser, browser-use — kept

### Document tools
- docx, pptx, xlsx, pdf, document-skills — kept

### MCP/protocol tools
- context7, claude-api, mcp-builder, hookify, agent-sdk-dev, plugin-dev — kept

### Marketing/product
- product-management (ccc), product-analysis, marketing-* family, social-automation — kept

### One-offs
- humanizer, statusline-generator (separate from claude-hud), code-review, code-simplifier (claude-plugins-official version — likely overlap with v6 reviewer but kept separate v6.0), feature-dev, ralph-loop, frontend-design, frontend-design-pro, ui-design-system, ui-designer, ui-ux-pro-max — kept

### Personal / Nick's
- orbit, lynx, logblog, distill, dry, claude-mem (cavemem), claude-vault, claude-patterns, claude-performance, claude-telemetry, ghostty-dynamic-themes, social-automation, mermaid-tools — kept (these are user's own infrastructure)

---

## §3. Per-Command Migration Matrix

Format: `Current invocation → Shannon v6 equivalent (or DROPPED)`.

### OMC commands → Shannon
- /oh-my-claudecode:autopilot → /shannon:autopilot
- /oh-my-claudecode:ralph → /shannon:loop
- /oh-my-claudecode:team → /shannon:team
- /oh-my-claudecode:ultrawork → /shannon:loop (no separate ultrawork in v6)
- /oh-my-claudecode:ultraqa → DROPPED (low usage per auditor-3)
- /oh-my-claudecode:plan → /shannon:plan
- /oh-my-claudecode:ralplan → /shannon:plan-deep
- /oh-my-claudecode:trace → /shannon:trace
- /oh-my-claudecode:omc-doctor → /shannon:doctor
- /oh-my-claudecode:omc-setup → /shannon:install
- /oh-my-claudecode:autoresearch → /shannon:research
- /oh-my-claudecode:remember → /shannon:reflect --mode=memorize
- /oh-my-claudecode:self-improve → /shannon:reflect
- /oh-my-claudecode:debug → /shannon:fix
- /oh-my-claudecode:verify → /shannon:validate (or /shannon:audit-completion)
- /oh-my-claudecode:deep-interview → /shannon:prd (interview semantics)
- /oh-my-claudecode:deepinit → DROPPED
- /oh-my-claudecode:deep-dive → DROPPED (low usage)
- /oh-my-claudecode:ccg → DROPPED
- /oh-my-claudecode:sciomc → DROPPED
- /oh-my-claudecode:skillify → DROPPED
- /oh-my-claudecode:hud → /shannon:status
- /oh-my-claudecode:visual-verdict → /shannon:audit --scope screen
- /oh-my-claudecode:cancel → /shannon:install --rollback (covers cancel-modes use case)
- /oh-my-claudecode:writer-memory → /shannon:reflect --mode=memorize
- /oh-my-claudecode:learner → /shannon:reflect --mode=memorize
- /oh-my-claudecode:wiki → DROPPED
- /oh-my-claudecode:project-session-manager → /shannon:trace
- /oh-my-claudecode:external-context → DROPPED
- /oh-my-claudecode:release → DROPPED (use git/gh)
- /oh-my-claudecode:setup → /shannon:install
- /oh-my-claudecode:skill → DROPPED (skills auto-bind)
- /oh-my-claudecode:configure-notifications → DROPPED
- /oh-my-claudecode:mcp-setup → DROPPED (out of v6 scope)
- /oh-my-claudecode:ai-slop-cleaner → /shannon:reflect --mode=critique
- /oh-my-claudecode:omc-teams → /shannon:team
- /oh-my-claudecode:omc-reference → DROPPED (docs only)
- /oh-my-claudecode:ask → /shannon:reflect (ask is reflection)
- /oh-my-claudecode:cook → /shannon:cook

### VF commands → Shannon
- /validationforge:validate → /shannon:validate
- /validationforge:validate-plan → /shannon:validate --plan-only
- /validationforge:validate-audit → /shannon:audit
- /validationforge:validate-fix → /shannon:fix
- /validationforge:validate-ci → /shannon:validate (CI flag inherent)
- /validationforge:validate-consensus → /shannon:forge --mode=consensus
- /validationforge:validate-team → /shannon:team --charter validation-team
- /validationforge:validate-team-dashboard → /shannon:doctor (subset)
- /validationforge:validate-sweep → /shannon:autopilot (sweep = autopilot)
- /validationforge:validate-benchmark → DROPPED (use /shannon:doctor)
- /validationforge:validate-dashboard → DROPPED (use /shannon:doctor)
- /validationforge:vf-setup → /shannon:install
- /validationforge:vf-telemetry → /shannon:trace
- /validationforge:forge-execute → /shannon:forge
- /validationforge:forge-plan → /shannon:plan-deep (+ --with-validation)
- /validationforge:forge-team → /shannon:team --mode=forge
- /validationforge:forge-setup → /shannon:install
- /validationforge:forge-benchmark → DROPPED
- /validationforge:forge-install-rules → DROPPED

### Crucible commands → Shannon
- /crucible:forge → /shannon:forge
- /crucible:autopilot → /shannon:autopilot
- /crucible:plan-and-execute → /shannon:cook
- /crucible:status → /shannon:doctor (composite includes Crucible state)
- /crucible:resume → /shannon:resume
- /crucible:doctor → /shannon:doctor
- /crucible:remediate → (folded into /shannon:autopilot retry loop)
- /crucible:validate → /shannon:validate
- /crucible:audit → /shannon:audit-completion
- /crucible:trial → DROPPED (meta plugin dev)
- /crucible:fix → /shannon:fix
- /crucible:explain → DROPPED
- /crucible:graph → DROPPED
- /crucible:rule-new, :hook-new, :skill-new, :command-new, :agent-new, :stack-new → DROPPED (out of v6 scope; defer to v6.1+)

### Anneal commands → Shannon
- /anneal-cast:anneal → /shannon:plan-tournament
- /anneal-alloy:anneal → /shannon:plan
- /anneal-temper:anneal → /shannon:plan-converge

### deepest-plan commands → Shannon
- /deepest-plan:deepest → /shannon:plan-deep
- /deepest-plan:deepest-plan → /shannon:plan-deep
- /deepest-plan:deepest-validate → /shannon:validate
- /deepest-plan:deepest-validate-fix → /shannon:fix
- /deepest-plan:deepest-validate-plan → /shannon:validate --plan-only
- /deepest-plan:deepest-validate-ci → /shannon:validate
- /deepest-plan:deepest-validate-audit → /shannon:audit
- /deepest-plan:deepest-setup → /shannon:install

### Reflexion commands → Shannon
- /reflexion:reflect → /shannon:reflect
- /reflexion:critique → /shannon:reflect --mode=critique
- /reflexion:memorize → /shannon:reflect --mode=memorize

### SADD commands → Shannon
(SADD has no commands; only skills. Skills are absorbed per SHANNON-V6-SKILLS-AGENTS.md.)
- /sadd:do-in-parallel → /shannon:dispatch-parallel (skill auto-binds to this command)
- /sadd:do-competitively → /shannon:dispatch-competitive
- /sadd:do-in-steps → /shannon:dispatch
- /sadd:judge → folded into dispatch-* command result
- /sadd:judge-with-debate → folded into /shannon:dispatch-competitive
- /sadd:tree-of-thoughts → skill auto-binds to /shannon:tree-of-thoughts (kept as standalone skill)
- /sadd:do-and-judge → /shannon:dispatch (judge inherent)
- /sadd:launch-sub-agent → DROPPED (low-level)
- /sadd:multi-agent-patterns → DROPPED (doc)
- /sadd:subagent-driven-development → DROPPED (doc)

### kaizen commands → Shannon
(kaizen has no commands; only skills.)
- /kaizen:why → /shannon:why
- /kaizen:root-cause-tracing → /shannon:why
- /kaizen:cause-and-effect → /shannon:why
- /kaizen:analyse → /shannon:why
- /kaizen:analyse-problem → /shannon:why
- /kaizen:plan-do-check-act → /shannon:retro
- /kaizen:kaizen → /shannon:retro

### claude-hud commands → Shannon
- /claude-hud:setup → /shannon:status setup
- /claude-hud:configure → /shannon:status configure

### prd-generator commands → Shannon
- (commands undocumented in cache; likely a single create-prd-style command) → /shannon:prd

### planning-with-files commands → Shannon
- (CC variant empty) → /shannon:plan

### start (the-startup) commands → Shannon
- /start:specify, :specify-incremental, :specify-factory, :specify-requirements, :specify-solution, :specify-meta → /shannon:plan or /shannon:prd
- /start:implement, :implement-incremental, :implement-direct, :implement-factory → /shannon:cook
- /start:validate → /shannon:validate
- /start:debug → /shannon:fix
- /start:brainstorm → /shannon:reflect (or external)
- /start:test → /shannon:validate
- /start:refactor → DROPPED (use /shannon:cook)
- /start:analyze → DROPPED
- /start:constitution → DROPPED (CLAUDE.md authored by user)
- /start:document → DROPPED (out of v6 scope)
- /start:writing-skills → DROPPED
- /start:review → /shannon:audit

### autoresearch commands → Shannon
- /autoresearch:* → /shannon:research

---

## §4. Migration Pre-Flight

Before running `scripts/uninstall-others.sh`:

```
Backup checklist (auto by setup.sh):
[ ] settings.json copied to settings.json.pre-shannon-v6.bak
[ ] enabledPlugins state snapshotted to .shannon/uninstall-rollback.json
[ ] extraKnownMarketplaces snapshotted
[ ] List of 16 plugins-to-disable printed for user review
```

Rollback (`scripts/rollback.sh`):
```
[ ] Restore enabledPlugins from .shannon/uninstall-rollback.json
[ ] Re-add removed marketplaces
[ ] Print which plugins were re-enabled
[ ] Tell user: restart CC + DO NOT uninstall Shannon yet (do that manually)
```

---

## §5. Unresolved Questions

- UQ-INV-1: Some plugins (orbit, lynx, distill, dry, claude-mem, kaizen, sadd, reflexion) are user's own. Confirm user wants them subsumed by Shannon — recommendation: KEEP standalone for orbit/lynx/distill/dry (separate domains); ABSORB kaizen/sadd/reflexion (they're enforcement-related and overlap Shannon mission).
- UQ-INV-2: Crucible's meta-plugin-dev commands (rule-new/hook-new/skill-new/command-new/agent-new) — should Shannon ship /shannon:author for the same purpose in v6.1, or keep Crucible as separate dev tool? Recommendation: defer; not v6.0 critical.
- UQ-INV-3: Several "marketplaces" (claude-code-plugins-plus, agent-toolkit, anthropic-agent-skills) bundle dozens of skills. Shannon doesn't disable them, but they may overlap functionally. Recommendation: leave alone in v6.0; address via curated skill catalog in v6.1.
- UQ-INV-4: `validationforge` settings.json plugin entry vs Shannon hooks.json — when both are enabled, VF's block-test-files.js AND Shannon's block-fab-files.js will fire. Recommendation: uninstall-others.sh disables VF entirely; user explicitly chooses parallel mode if they want both.
- UQ-INV-5: Shannon v6 is a single plugin but currently spans multiple "marketplaces" if user pulls from GitHub for distribution. Recommendation: ship shannon-framework as a single repo + single marketplace.json; no cross-marketplace deps.

---

## §6. Summary Counts

- **Plugins to uninstall: 16** (per §1)
- **Plugins to keep: ~140** (per §2 — most enabled plugins are domain helpers, kept)
- **Commands consolidated: 70+ → 26 Shannon commands** (~64% reduction)
- **Skills consolidated: 150+ → 22 Shannon skills** (~85% reduction)
- **Agents consolidated: 60+ → 10 Shannon agents** (~83% reduction)
- **Hooks consolidated: 30+ → 14 Shannon hooks** (~53% reduction)

---

End of SHANNON-V6-INVENTORY.md.
