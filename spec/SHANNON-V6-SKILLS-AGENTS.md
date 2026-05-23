# SHANNON-V6-SKILLS-AGENTS.md — Skill + Agent Surface

**Status:** LOCKED 2026-05-23
**Namespace:** Skills auto-bind to `/shannon:<skill>`. Agents invoked via `Task` tool with `subagent_type=<agent-name>`.

---

## Part A: Skills (22 total)

Each skill lives at `shannon-framework/skills/<slug>/SKILL.md` with frontmatter `{ name, description, triggers }`.

### Validation Skills (5)

#### 1. functional-validation
- **Replaces:** /validationforge:functional-validation, /ck:gate-validation-discipline (folded)
- **Description:** End-to-end no-mocks validation through real system execution.
- **Triggers:** "validate this", "prove it works", "functional validation", "no mocks", "ensure feature works"
- **Behavior contract:** 5 steps: (1) build real system, (2) run it, (3) exercise through UI, (4) capture evidence, (5) apply gate validation. Outputs go to e2e-evidence/<slug>/. Refuses to PASS without cited evidence.

#### 2. evidence-gate
- **Replaces:** /validationforge:gate-validation-discipline, /crucible:completion-gate (partial), /verification-before-completion
- **Description:** 5-question checklist applied before any completion claim.
- **Triggers:** "marking complete", "task complete", "ready to ship", "PR ready"
- **Behavior contract:** Asks: READ evidence? VIEW screenshot? EXAMINE output? CITE proof? Skeptic agree? Any "no" → REFUSE completion.

#### 3. no-fakes-discipline
- **Replaces:** /validationforge:no-mocking-validation-gates
- **Description:** Prevents circumventing validation via fakes/stubs/mocks/fixtures.
- **Triggers:** about to write test file, about to add fallback mode, about to mock an API
- **Behavior contract:** detect intent (Write tool path matches detector), inject refusal stderr.

#### 4. visual-inspection
- **Replaces:** /validationforge:visual-inspection, /lynx:ui-experience-audit (partial)
- **Description:** Systematic visual QA for UI screenshots (iOS HIG / web WCAG / cross-platform).
- **Triggers:** "visual audit", "screenshot review", "HIG check"
- **Behavior contract:** evaluate layout, typography, contrast, touch targets, dark mode, overflow, spacing, accessibility per platform standards.

#### 5. consensus-engine
- **Replaces:** /validationforge:consensus-engine, /validationforge:consensus-synthesis, /validationforge:consensus-disagreement-analysis
- **Description:** Multi-validator agreement gate. N independent validators against same feature; synthesize confidence-scored verdict.
- **Triggers:** "consensus validation", "validate with N reviewers", "agreement gate"
- **Behavior contract:** spawn N (default 3) consensus-validator subagents in parallel isolated directories; synthesizer reads all verdicts; emits HIGH/MEDIUM/LOW confidence; disagreement protocol on SPLIT.

### Completion Skills (4)

#### 6. completion-gate
- **Replaces:** /crucible:completion-gate
- **Description:** Reads evidence/ tree, evaluates every MSC against cited evidence, requires three-reviewer consensus + Oracle quorum.
- **Triggers:** "completion gate", "final gate", "ship gate"
- **Behavior contract:** read evidence/completion-gate/report.json; emit COMPLETE / REFUSED with cited blockers.

#### 7. refusal-discipline
- **Replaces:** /crucible refusal pattern (codified)
- **Description:** When evidence is missing, write REFUSAL.md and stop.
- **Triggers:** evidence gap, missing citation, gate unmet
- **Behavior contract:** structured REFUSAL.md with cited blockers, no override flag, no force-complete.

#### 8. oracle-review
- **Replaces:** /crucible:oracle-review
- **Description:** Plan-time and post-execution Oracle quorum review.
- **Triggers:** before /shannon:cook execute; before /shannon:forge completes
- **Behavior contract:** spawn 3+ oracle-* agents in isolated contexts; quorum = ≥2 APPROVE + 0 unresolved critical blockers.

#### 9. evidence-indexing
- **Replaces:** /crucible:evidence-indexing
- **Description:** Maintain README.md + INDEX.md in every evidence/ subdirectory.
- **Triggers:** after any phase artifact lands in evidence/
- **Behavior contract:** refuse to leave any evidence dir un-indexed at gate-completion.

### Planning Skills (5)

#### 10. plan-author
- **Replaces:** /ck:plan, /oh-my-claudecode:plan, /anneal-alloy:anneal, /planning-with-files:*, /crucible:planning, /create-validation-plan
- **Description:** Linear hierarchical plan author. plan.md + phase-NN.md files; success criteria + validation gates per phase.
- **Triggers:** "plan this", "create plan", "implementation plan"
- **Behavior contract:** plans/{date-prefix}-{slug}/ directory; validation phase included by default.

#### 11. plan-tournament
- **Replaces:** /anneal-cast tournament pattern
- **Description:** N parallel plan-author candidates with distinct perspectives; red-teamer per candidate; tournament-judge selects.
- **Triggers:** "plan tournament", "compare plans", "anneal cast"

#### 12. plan-converge
- **Replaces:** /anneal-temper convergence pattern
- **Description:** Iterative plan refine → critique → revise; converges when red-teamer ≤1 BLOCKING.
- **Triggers:** "plan converge", "iteratively refine plan", "anneal temper"

#### 13. research-validation
- **Replaces:** /validationforge:research-validation, /autoresearch:*
- **Description:** Gather standards, best practices, applicable criteria before validation planning.
- **Triggers:** "research validation standards", "applicable criteria"
- **Behavior contract:** map standards (WCAG, HIG, security) to v6 skills; output research/{slug}.md.

#### 14. sequential-analysis
- **Replaces:** /validationforge:sequential-analysis, sequential-thinking MCP wrap
- **Description:** Structured multi-step reasoning with revision capability.
- **Triggers:** complex problem, root-cause investigation, ambiguous scope.

### Reflection Skills (5)

#### 15. reflect
- **Replaces:** /reflexion:reflect
- **Description:** Self-refinement pass on prior output.
- **Triggers:** "reflect on this", "self-refine", "iterate"

#### 16. critique
- **Replaces:** /reflexion:critique
- **Description:** Adversarial critique of current work.
- **Triggers:** "critique this", "find holes", "what's wrong"

#### 17. memorize
- **Replaces:** /reflexion:memorize, /oh-my-claudecode:remember, /claude-vault:* (overlap)
- **Description:** Extract learned pattern from session; save to ~/.claude/memory/.
- **Triggers:** "remember this", "save lesson", "memorize pattern"

#### 18. root-cause-tracing
- **Replaces:** /kaizen:why, /kaizen:root-cause-tracing, /kaizen:cause-and-effect, /kaizen:analyse, /kaizen:analyse-problem
- **Description:** Five-whys + cause-and-effect diagram + analysis report.
- **Triggers:** "why is X happening", "root cause", "five whys"

#### 19. plan-do-check-act
- **Replaces:** /kaizen:plan-do-check-act, /kaizen:kaizen
- **Description:** Iterative PDCA cycle for systematic experimentation.
- **Triggers:** "iterate experiment", "PDCA", "continuous improvement"

### Dispatch Skills (3)

#### 20. dispatch-parallel
- **Replaces:** /sadd:do-in-parallel, /superpowers:dispatching-parallel-agents
- **Description:** Launch N parallel sub-agents with model selection, quality-focused prompting, meta-judge verification.
- **Triggers:** "do in parallel", "parallel subagents"

#### 21. judge
- **Replaces:** /sadd:judge, /sadd:judge-with-debate
- **Description:** LLM-as-judge evaluation of subagent outputs; debate mode for tie-breaking.
- **Triggers:** "judge outputs", "evaluate candidates"

#### 22. tree-of-thoughts
- **Replaces:** /sadd:tree-of-thoughts
- **Description:** Systematic exploration + pruning + expansion via Tree of Thoughts methodology.
- **Triggers:** "tree of thoughts", "explore branches"

### Observability Skills (Statusline + Trace; folded into 1)

These are part of Statusline domain — borrowed from claude-hud TS dist:

- statusline-config — wrap claude-hud's `setup` / `configure` (vendored)
- observability-report — Shannon-specific log reader for trace/doctor

(Counted as part of the 22.)

---

## Part B: Agents (10 total)

Each agent lives at `shannon-framework/agents/<name>.md` with frontmatter `{ name, description, model }`.

### Core Agents (4)

#### 1. planner
- **Replaces:** OMC planner, Crucible planner, anneal plan-author personas
- **Description:** Authors implementation plans. Reads codebase, identifies phases, writes success criteria. NEVER edits source.
- **Model:** opus (high-stakes reasoning)
- **Triggers:** /shannon:plan, /shannon:plan-tournament, /shannon:plan-deep

#### 2. executor
- **Replaces:** OMC executor, OMC fullstack-developer, start implement-incremental
- **Description:** Executes a phase plan against the codebase. Reads phase-NN.md, makes edits, runs validation per phase gates.
- **Model:** opus (when phase complex) or sonnet (when phase mechanical)
- **Triggers:** /shannon:cook (post-plan), /shannon:autopilot

#### 3. reviewer
- **Replaces:** OMC code-reviewer, OMC security-reviewer, VF verdict-writer, Crucible reviewer-a/b/c
- **Description:** Post-implementation review: correctness, security, performance, style. Cites evidence per finding.
- **Model:** opus (final-gate review) or sonnet (intermediate)
- **Triggers:** /shannon:cook (post-execution), /shannon:forge (consensus mode)

#### 4. validator
- **Replaces:** VF validation-lead, VF platform-detector, VF evidence-capturer, Crucible validator
- **Description:** Runs validation suite per platform. Detects platform, executes journeys, captures evidence, emits per-journey verdict.
- **Model:** sonnet (standard) or opus (consensus mode)
- **Triggers:** /shannon:validate, /shannon:forge

### Specialist Agents (4)

#### 5. researcher
- **Replaces:** OMC researcher, autoresearch implementations, deep-research:*
- **Description:** Researches a sub-topic; outputs cited summary. Used by /shannon:research and /shannon:plan-deep.
- **Model:** sonnet (most cases); opus when topic dense.

#### 6. critic
- **Replaces:** OMC critic, reflexion critique pattern
- **Description:** Adversarial critique of work artifact. Surfaces what's missing, what's wrong, where assumptions break.
- **Model:** opus (always — content-quality-critical)

#### 7. red-teamer
- **Replaces:** anneal red-team-trinity, /red-team:*, /harden-plan:*
- **Description:** Dispatch hostile reviewers (security, scope-creep, evidence-rigor, failure-modes) against a plan/PRD.
- **Model:** opus.
- **Triggers:** /shannon:plan-tournament (per candidate), /shannon:plan-converge (each round)

#### 8. oracle
- **Replaces:** Crucible oracle-auditor-1/2/3, Crucible reviewer-a/b/c (when functioning as oracle)
- **Description:** Final-gate Oracle. Reviews plan OR completed evidence in isolated context. Emits APPROVE / REFUSE with cited blocker.
- **Model:** opus.
- **Triggers:** /shannon:forge (consensus), /shannon:audit-completion

### Coordination Agents (2)

#### 9. coordinator
- **Replaces:** OMC team-lead pattern, VF validation-lead orchestration
- **Description:** Multi-teammate coordinator. Maintains TaskList; assigns tasks; synthesizes findings; resolves conflicts.
- **Model:** opus.
- **Triggers:** /shannon:team

#### 10. dispatch-judge
- **Replaces:** /sadd:judge consumed as agent (vs skill)
- **Description:** Meta-judge for /shannon:dispatch-* commands. Evaluates parallel subagent outputs, scores, emits winner.
- **Model:** opus.
- **Triggers:** /shannon:dispatch-parallel, /shannon:dispatch-competitive

---

## Skills/Agents DROPPED (from consolidated plugins)

### From OMC (39 skills, 19 agents) — DROPPED 25 skills, 10 agents
- OMC owns many one-off helpers (configure-notifications, deepinit, mcp-setup, project-session-manager, skillify, sciomc, ultraqa, ultrawork-runner, visual-verdict, wiki, writer-memory, learner, external-context, ai-slop-cleaner, omc-doctor) — most replaced by /shannon:doctor + /shannon:reflect + /shannon:trace
- OMC agents not absorbed: analyst, designer, document-specialist, explore, git-master, qa-tester, scientist, test-engineer, tracer, writer — Shannon's 10 agents are intentionally lean. These can be added v6.1 if needed.

### From VF (52 skills, 7 agents) — DROPPED 32 skills, 3 agents
- Platform-specific validation skills (ios-validation, web-validation, api-validation, cli-validation, fullstack-validation, react-native-validation, flutter-validation, django-validation, rust-cli-validation) folded into `validator` agent per-platform dispatch — not separate skills.
- Specialized: ios-simulator-control, chrome-devtools, playwright-validation, web-testing — these are MCP-server-or-tool wrappers; Shannon delegates to existing MCPs, doesn't reimplement.
- VF accessibility-audit, responsive-validation, design-token-audit, design-validation, stitch-integration → Shannon /shannon:audit covers via visual-inspection.

### From Crucible (12 skills, 11 agents) — KEPT 6 skills, 3 agent slots
- Kept: completion-gate, refusal-discipline, oracle-review, evidence-indexing, codebase-analysis, documentation-research
- Kept: oracle (slot for 3 instances), reviewer (slot for 3 instances)
- Dropped: setup, enable, disable, session-log-audit (folded into /shannon:audit), skill-enrichment (folded into ContextLayer cache)
- Dropped agents: codebase-analyst, documentation-researcher, skill-discoverer (folded into researcher agent)

### From SADD (10 skills) — KEPT 4
- Kept: dispatch-parallel (=do-in-parallel), judge, tree-of-thoughts, judge-with-debate
- Dropped: do-in-steps (folded into dispatch-sequential which is the default dispatch behavior), do-competitively (folded into /shannon:dispatch-competitive command), do-and-judge (folded into dispatch-* pattern), multi-agent-patterns (doc only), launch-sub-agent (low-level; not a user-facing skill), subagent-driven-development (doc only)

### From anneal (3 plugins, 21 skills total) — KEPT 3 (one per variant: tournament, linear, converge)
- Dropped agent personas: atlas, hephaestus, metis, momus, prometheus-cast — folded into red-teamer agent's instructions
- Dropped: red-team-trinity, redteam-assumptions, redteam-scope, redteam-security — folded into red-teamer agent
- Kept (as skills): plan-tournament, plan-converge (the linear variant is the default plan-author)

### From start (the-startup) — DROPPED all
- specify, specify-incremental, specify-factory, specify-requirements, specify-solution, specify-meta — folded into /shannon:plan and /shannon:prd
- implement, implement-direct, implement-incremental, implement-factory — folded into /shannon:cook
- validate (in start) — folded into /shannon:validate

### From kaizen (7 skills) — KEPT 2 (consolidated)
- Kept: root-cause-tracing, plan-do-check-act
- Dropped: analyse, analyse-problem, cause-and-effect, why, kaizen — folded into root-cause-tracing

### From reflexion (3 skills) — KEPT all 3 (renamed for consistency)
- reflect, critique, memorize — kept verbatim semantics

### From planning-with-files (mostly empty in CC variant) — DROPPED
- The Claude variant is empty per inventory (other ecosystem variants exist: cursor, gemini, mastracode, etc.); folded into /shannon:plan

### From prd-generator — KEPT 1
- Folded into /shannon:prd command + plan-author skill (PRD subskill)

### From claude-hud — KEPT 2 (vendored as observability)
- statusline-config (wraps claude-hud setup/configure)
- observability-report (Shannon-specific log reader; new)

### From deepest-plan (15+ skills) — DROPPED most, folded into existing
- Kept as folded: /shannon:plan-deep ABSORBS deepest semantics
- Platform validators (api-validation, cli-validation, fullstack-validation, ios-validation, web-validation) all DROPPED (duplicate of VF; both vendor-owned by `validator` agent)
- accessibility-audit, responsive-validation, condition-based-waiting, error-recovery, parallel-validation — DROPPED (low-value duplicates)

---

## Final Counts

- **Skills: 22** (target was 15-25 — landed mid-range)
- **Agents: 10** (target was 8-12 — landed mid-range)
- **Commands: 26** (per SHANNON-V6-COMMANDS.md)
- **Hooks: 14** (per SHANNON-V6-HOOKS.md)

---

## Unresolved Questions

- UQ-SA-1: Should `red-teamer` be a single agent with `--lens` arg, or 4 separate agents (security/scope/evidence/failure-modes)? Recommendation: single agent + lens arg per anneal pattern.
- UQ-SA-2: Should `oracle` and `reviewer` be the same agent at different gate positions, or distinct? Recommendation: distinct — oracle does pre-execution plan review; reviewer does post-execution evidence review. Crucible distinguishes them.
- UQ-SA-3: Does Shannon ship per-language reviewer agents (python-reviewer, go-reviewer, swift-reviewer)? Recommendation: NO. `reviewer` is language-agnostic; user adds per-language CLAUDE.md rules to bias review.

---

End of SHANNON-V6-SKILLS-AGENTS.md.
