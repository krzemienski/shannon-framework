# SHANNON-V6-COMMANDS.md — Slash Command Surface

**Status:** LOCKED 2026-05-23
**Namespace:** All commands invoked as `/shannon:<name>`.
**Replaces:** /oh-my-claudecode:*, /validationforge:*, /crucible:*, /anneal-*:*, /deepest-plan:*, /reflexion:*, /sadd:*, /claude-hud:*, /prd-generator:*, /planning-with-files:*, /start:*, /autoresearch:*.

Each command lives at `shannon-framework/commands/<name>.md` as a slash-command spec markdown file.

---

## Command List (26 total)

### Domain: Orchestration (4 commands)

#### 1. /shannon:cook
- **Replaces:** /ck:cook, /oh-my-claudecode:cook, /validationforge:validate-fix, /crucible:plan-and-execute
- **Inputs:** `[plan-path | task-description]`, optional `--fast`, optional `--no-validate`
- **Behavior step-by-step:**
  1. If arg looks like a path → read plan; else treat as task brief.
  2. Invoke `plan-author` skill IF no plan provided (yields plans/{date}-{slug}/).
  3. Invoke `executor` agent with plan + IRON-RULE injection (no fakes).
  4. After executor returns: invoke `functional-validation` skill (unless --no-validate).
  5. Invoke `evidence-gate` skill before marking complete.
- **Success criteria:** all phases executed, evidence under e2e-evidence/, no FAIL verdicts open.
- **Hooks fired:** evidence-gate-reminder (on TaskUpdate completed), validation-not-compilation (after Bash builds), validation-skill-tripwire (if build+no validate).
- **Skills invoked:** plan-author (optional), functional-validation, evidence-gate.

#### 2. /shannon:team
- **Replaces:** /oh-my-claudecode:team, /validationforge:validate-team, /oh-my-claudecode:omc-teams
- **Inputs:** `<team-name>` + `--charter <file>` + optional `--size N`
- **Behavior:** spawn N teammates via Task tool; each gets subagent-governance-inject IRON-RULE; team-coordinator agent orchestrates; TaskList shared.
- **Success criteria:** all teammate tasks completed, no orphan in_progress, lead verdict written.
- **Hooks fired:** subagent-governance-inject (PreToolUse:Task per spawn), stop-task-semantics (Stop, blocks if any teammate task still in_progress).
- **Skills invoked:** team-coordinator (custom skill); per teammate: whatever charter says.

#### 3. /shannon:loop
- **Replaces:** /oh-my-claudecode:ralph, /ralph-loop:*, /ralph-planner:*, /ralph-specum:*, /ralphex:*, /ralph-wiggum-marketer:* (all ralph variants ABSORBED)
- **Inputs:** `<goal>`, optional `--max-iter N` (default 5), optional `--verify-with <skill>`
- **Behavior:** loop {do, verify, reflect} until verify-with skill passes OR max-iter hit.
- **Success criteria:** verify skill returns PASS; reflexion skill confirms convergence.
- **Hooks fired:** standard chain.
- **Skills invoked:** loop-runner, reflect, the user-specified verify-with skill.

#### 4. /shannon:autopilot
- **Replaces:** /oh-my-claudecode:autopilot, /crucible:autopilot, /deepest-plan:deepest-validate
- **Inputs:** `<task>` + optional `--max-attempts N` (default 3)
- **Behavior:** /shannon:cook in refusal-driven retry loop. Crucible's REFUSAL.md pattern preserved.
- **Success criteria:** completion-gate verdict = COMPLETE OR max-attempts exceeded → emit REFUSAL.md.
- **Hooks fired:** full chain; evidence-gate-reminder critical.
- **Skills invoked:** /shannon:cook + completion-gate + refusal-discipline.

### Domain: Validation (3 commands)

#### 5. /shannon:validate
- **Replaces:** /validationforge:validate, /validationforge:validate-plan, /validationforge:validate-ci, /validationforge:validate-sweep, /deepest-plan:deepest-validate, /lynx:audit
- **Inputs:** optional `--mode quick|standard|consensus`, optional `--platform ios|web|api|cli|fullstack`
- **Behavior:** detect platform (or use --platform), run create-validation-plan skill, execute against real system, capture evidence to e2e-evidence/, write verdict report.
- **Success criteria:** every journey has cited PASS/FAIL evidence; no INCONCLUSIVE.
- **Hooks fired:** block-fab-files (PreToolUse Write), evidence-quality-check (PostToolUse Edit), validation-not-compilation.
- **Skills invoked:** create-validation-plan, functional-validation, platform-specific (ios-validation, web-validation, api-validation, cli-validation, fullstack-validation), evidence-gate.

#### 6. /shannon:audit
- **Replaces:** /validationforge:validate-audit, /lynx:audit-screen, /lynx:full-ui-experience-audit, /seven-day-drift-audit:*, /session-retrospective-audit:*
- **Inputs:** `--scope screen|app|session|drift`, optional `--days N` (for drift)
- **Behavior:** read-only audit; classifies findings by severity (BLOCKING / HIGH / MEDIUM / LOW). For drift: searches sessions per ~/.claude/rules pattern, compares plan claims vs evidence.
- **Success criteria:** audit report at reports/audit-{slug}.md cites every finding.
- **Hooks fired:** none (read-only).
- **Skills invoked:** visual-inspection, full-functional-audit, baseline-quality-assessment, session-log-audit.

#### 7. /shannon:fix
- **Replaces:** /ck:fix, /validationforge:validate-fix, /oh-my-claudecode:fix
- **Inputs:** `[bug-description | error-log-path]`, optional `--auto`
- **Behavior:** scout-then-debug-then-implement-then-revalidate. 3-strike cap per VF forge convention. Each attempt = fresh e2e-evidence/forge-attempt-N/ dir.
- **Success criteria:** re-validation PASS within 3 attempts OR mark UNFIXABLE.
- **Hooks fired:** standard chain.
- **Skills invoked:** scout, debug, error-recovery, functional-validation.

### Domain: Completion (3 commands)

#### 8. /shannon:forge
- **Replaces:** /crucible:forge, /validationforge:forge-execute, /validationforge:forge-team
- **Inputs:** `<task>`, optional `--mode consensus` (engages 3-reviewer + 3-oracle quorum)
- **Behavior:** Crucible's full pipeline absorbed — codebase-analysis → docs-research → planning → oracle-plan-review → execute → validation → evidence-indexing → 3-reviewer consensus → 3-oracle quorum → completion-gate. Refuses on cited blocker.
- **Success criteria:** completion-gate verdict = COMPLETE; quorum ≥2/3 APPROVE.
- **Hooks fired:** entire chain; evidence-gate-reminder critical.
- **Skills invoked:** codebase-analysis, documentation-research, plan-author, oracle-review, evidence-indexing, completion-gate, refusal-discipline.

#### 9. /shannon:audit-completion
- **Replaces:** /crucible:status, /crucible:audit, /validationforge:validate-team-dashboard
- **Inputs:** optional `--run-id <id>`
- **Behavior:** read evidence/ tree for given run; print MSC table + reviewer consensus + oracle quorum + overall verdict.
- **Success criteria:** report saved to reports/completion-{run-id}.md.
- **Hooks fired:** none.
- **Skills invoked:** completion-gate (read-only).

#### 10. /shannon:resume
- **Replaces:** /crucible:resume, /campaign-state:resume
- **Inputs:** optional `--run-id <id>` (else latest run)
- **Behavior:** inspect evidence/ tree; identify last completed phase; resume from next missing phase artifact.
- **Success criteria:** session continues from precise resume point.
- **Hooks fired:** standard chain.
- **Skills invoked:** completion-gate (state reader).

### Domain: Planning (5 commands)

#### 11. /shannon:plan
- **Replaces:** /ck:plan, /oh-my-claudecode:plan, /anneal-alloy:anneal (linear variant), /planning-with-files:*, /create-validation-plan:*
- **Inputs:** `<feature-or-task-description>`, optional `--phases N`, optional `--with-validation`
- **Behavior:** linear plan author. Drops plans/{date-prefix}-{slug}/{plan.md + phase-NN.md files}. Includes validation phase if --with-validation OR if task implies user-facing change.
- **Success criteria:** plan.md created; phase files numbered; success criteria cited per phase.
- **Hooks fired:** plan-before-execute (PreToolUse:Write reminder if user starts editing src/ without plan).
- **Skills invoked:** plan-author, sequential-analysis.

#### 12. /shannon:plan-tournament
- **Replaces:** /anneal-cast:anneal (tournament variant)
- **Inputs:** `<problem>`, optional `--candidates N` (default 3)
- **Behavior:** spawn N parallel `plan-author` agents with distinct perspectives (e.g. security-first, perf-first, simplicity-first); spawn `red-teamer` agent against each; tournament-judge selects winner.
- **Success criteria:** winning plan saved; loser plans archived to plans/{slug}/_rejected/.
- **Hooks fired:** standard chain.
- **Skills invoked:** plan-tournament, plan-author (×N), red-teamer.

#### 13. /shannon:plan-converge
- **Replaces:** /anneal-temper:anneal (convergence variant)
- **Inputs:** `<problem>`, optional `--rounds N` (default 3)
- **Behavior:** N rounds of plan-author refine → red-teamer critique → plan-author revise. Each round writes a checkpoint; convergence detected when red-teamer returns ≤1 BLOCKING finding.
- **Success criteria:** convergence reached within N rounds OR explicit non-convergence noted.
- **Skills invoked:** plan-converge, plan-author, red-teamer.

#### 14. /shannon:plan-deep
- **Replaces:** /deepest-plan:deepest, /deepest-plan:deepest-plan
- **Inputs:** `<problem>`, optional `--synthesis N`, optional `--debate`
- **Behavior:** consensus + gates + synthesis. Wraps /shannon:plan-tournament + /shannon:plan-converge + gate injection. Deepest-plan's 6-stage pipeline preserved.
- **Skills invoked:** plan-tournament, plan-converge, plan-author, red-teamer, create-validation-plan (gate injection).

#### 15. /shannon:research
- **Replaces:** /autoresearch:*, /oh-my-claudecode:autoresearch, /ck:research, /deep-research:*
- **Inputs:** `<topic>`, optional `--sources N`, optional `--depth shallow|standard|deep`
- **Behavior:** spawn N parallel `researcher` agents; each takes a sub-topic; aggregator writes research/{slug}.md with citations.
- **Success criteria:** research file has ≥N citations; aggregator agent emits SUMMARY.md.
- **Skills invoked:** research-validation, sequential-analysis.

#### 16. /shannon:prd
- **Replaces:** /prd-generator:* (entire plugin)
- **Inputs:** `<feature-description>` + interactive interview
- **Behavior:** structured PRD authoring with sections (Why / What / How / Success Metrics / Risks). Asks clarifying questions via AskUserQuestion.
- **Success criteria:** PRD.md saved; user explicitly approves before exit.
- **Skills invoked:** plan-author (PRD subskill), sequential-analysis.

### Domain: Reflection (3 commands)

#### 17. /shannon:reflect
- **Replaces:** /reflexion:reflect, /reflexion:critique, /oh-my-claudecode:self-improve
- **Inputs:** optional `--mode self|critique|memorize`, optional `--target <session-or-pr>`
- **Behavior:** self-refinement pass. Mode `self`: read last assistant turn, identify gaps, propose fix. Mode `critique`: spawn `critic` agent against current work. Mode `memorize`: extract learned pattern → save to ~/.claude/memory/.
- **Success criteria:** reflect.md or critique.md or memory entry written.
- **Skills invoked:** reflect, critique, memorize.

#### 18. /shannon:why
- **Replaces:** /kaizen:why, /kaizen:root-cause-tracing, /kaizen:cause-and-effect, /kaizen:analyse, /kaizen:analyse-problem
- **Inputs:** `<symptom-or-bug-description>`
- **Behavior:** five-whys + root-cause-tracing + cause-and-effect diagram. Output: root-cause-{slug}.md.
- **Skills invoked:** root-cause-tracing, why, cause-and-effect.

#### 19. /shannon:retro
- **Replaces:** /ck:retro, /retrospective-analyzer:*, /retro:*, /kaizen:plan-do-check-act
- **Inputs:** optional `--days N` (default 7), optional `--scope project|session`
- **Behavior:** mine session JSONLs over N days; aggregate decisions, lessons, gotchas; write retrospective-{date}.md.
- **Skills invoked:** retrospective-validation, plan-do-check-act, session-log-audit.

### Domain: Dispatch (3 commands)

#### 20. /shannon:dispatch
- **Replaces:** /sadd:do-in-steps, /sadd:launch-sub-agent, /oh-my-claudecode:dispatching-parallel-agents (sequential mode)
- **Inputs:** `<task-list-path | inline-tasks>`, optional `--model opus|sonnet|haiku`
- **Behavior:** sequential subagent chain. Each subagent gets IRON-RULE inject. judge-mode confirms each output before next dispatches.
- **Skills invoked:** dispatch-sequential, judge.

#### 21. /shannon:dispatch-parallel
- **Replaces:** /sadd:do-in-parallel, /superpowers:dispatching-parallel-agents (parallel mode)
- **Inputs:** `<task-list>`, max parallelism N (default 5)
- **Behavior:** parallel subagents; meta-judge + LLM-as-judge verification per sadd's pattern.
- **Skills invoked:** dispatch-parallel, judge.

#### 22. /shannon:dispatch-competitive
- **Replaces:** /sadd:do-competitively, /sadd:do-and-judge
- **Inputs:** `<task>` + `--candidates N`
- **Behavior:** N parallel subagents on same task; multi-judge evaluation; evidence-based synthesis.
- **Skills invoked:** dispatch-competitive, judge-with-debate, tree-of-thoughts (optional).

### Domain: Statusline + Observability (4 commands)

#### 23. /shannon:status
- **Replaces:** /claude-hud:setup, /claude-hud:configure
- **Inputs:** `[setup | configure | show]`, statusline-config options
- **Behavior:** statusline install / config (borrows claude-hud's dist/ unchanged, cited as vendored). `show` prints current statusline state.
- **Skills invoked:** statusline-config.

#### 24. /shannon:doctor
- **Replaces:** /oh-my-claudecode:omc-doctor, /crucible:doctor, /crucible:status, /vf-setup verify
- **Inputs:** none
- **Behavior:** health check: plugin manifest, hooks/hooks.json registered, settings.json valid, log dirs writable, marketplace declarations sane. Reports drift.
- **Skills invoked:** observability-report.

#### 25. /shannon:trace
- **Replaces:** /oh-my-claudecode:trace
- **Inputs:** optional `--session <id>`, optional `--last-N <num>`
- **Behavior:** read session JSONL; emit timeline of hooks fired, skills invoked, tools called. Helps prove which Shannon hooks are actually working in real sessions.
- **Skills invoked:** observability-report, session-log-audit.

#### 26. /shannon:install
- **Replaces:** /oh-my-claudecode:omc-setup, /validationforge:vf-setup, /crucible:setup
- **Inputs:** optional `--parallel` (coexist with other plugins) or `--replace` (default; runs uninstall-others.sh)
- **Behavior:** idempotent setup. Writes marketplace declaration if missing. Runs uninstall-others.sh (after y/N prompt) unless --parallel. Verifies install via doctor at end.
- **Skills invoked:** observability-report.

---

## Commands Dropped (NOT shipping in v6)

Per auditor-3 evidence + KISS:

- /oh-my-claudecode:ccg, :sciomc, :skillify, :writer-memory, :deep-dive, :deep-interview, :ultraqa, :ultrawork, :setup (replaced by /shannon:install) — never widely invoked in 3 audited sessions
- /validationforge:validate-consensus, :validate-team-dashboard, :validate-benchmark, :forge-team, :forge-benchmark, :forge-install-rules — overlapping responsibilities; consolidated to /shannon:forge + /shannon:doctor
- /crucible:forge subcommands (rule-new, hook-new, skill-new, command-new, agent-new, stack-new, graph, explain, trial, fix) — meta-plugin-development; out of v6 scope (added v6.1 if needed)
- /anneal-cast:atlas, :hephaestus, :metis, :momus, :oracle, :prometheus-cast, :red-team-trinity — these are SKILLS not commands in anneal; preserved as Shannon skills (see SHANNON-V6-SKILLS-AGENTS.md)
- /reflexion:remember (folded into /shannon:reflect --mode=memorize)
- /sadd:tree-of-thoughts, :multi-agent-patterns, :do-and-judge — kept as skills; not as standalone commands

---

## Unresolved Questions

- UQ-CMD-1: Should /shannon:cook accept `--auto` to skip plan-author and go straight to executor? Recommendation: yes, gated on small task size.
- UQ-CMD-2: Should /shannon:research be subcommand of /shannon:plan? Recommendation: keep separate; research often happens without planning a build.
- UQ-CMD-3: Does /shannon:install support remote marketplace (not just local directory)? Recommendation: v6.0 ships local only; v6.1 adds GitHub-based marketplace.

---

End of SHANNON-V6-COMMANDS.md. 26 commands, replaces 70+ commands across 16 plugins.
