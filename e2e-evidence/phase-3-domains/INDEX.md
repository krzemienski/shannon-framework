# Phase 3 — 7 Domain Modules Evidence Index

**Run:** dev-domains task #7 — Shannon v6 domain modules
**Date:** 2026-05-23
**Branch:** wt/shannon-rebuild-domains (branched from wt/shannon-rebuild-core HEAD 221826e)
**Plugin root:** /Users/nick/Desktop/shannon-framework
**Iron Rule:** All evidence is real execution output. No fakes. No substitute frameworks.

---

## Final Counts vs Spec

| Asset | Target | Actual | Notes |
|---|---|---|---|
| commands | 25 | **25** | Status command dropped per UQ-V2-4 |
| skills | 21 | **29** | Built per §3 table enumeration; spec internally inconsistent — Part A enumerated 22, §3 table column-sums higher. Built strict per §3 + brief explicit skill list. Statusline-config dropped per UQ-V2-4. Documented divergence. |
| agents | 10 | **10** | Exact match. Spec: planner, executor, reviewer, validator, researcher, critic, red-teamer, oracle, coordinator, dispatch-judge |

UQ decisions honored:
- UQ-V2-4: Status command + statusline-config skill DROPPED (no claude-hud TS vendor)
- UQ-CMD-1: /shannon:cook ships --auto flag
- UQ-CMD-2: /shannon:research is a standalone command
- UQ-CMD-3: /shannon:install supports local marketplace only
- UQ-SA-1: red-teamer = single agent with --lens arg
- UQ-SA-2: oracle and reviewer are DISTINCT agents
- UQ-SA-3: NO per-language reviewer agents

---

## Artifacts (in order produced)

### Per-domain inventories
- `orchestration.txt` — 4 commands + 3 skills + 2 agents (cook, team, loop, autopilot + autopilot-runner, team-coordinator, loop-runner + executor, coordinator)
- `validation.txt` — 3 commands + 5 skills + 1 agent (validate, audit, fix + functional-validation, evidence-gate, no-fakes-discipline, visual-inspection, consensus-engine + validator)
- `completion.txt` — 3 commands + 6 skills + 2 agents (forge, audit-completion, resume + completion-gate, refusal-discipline, oracle-review, evidence-indexing, codebase-analysis, documentation-research + reviewer, oracle)
- `planning.txt` — 6 commands + 6 skills + 3 agents (plan, plan-tournament, plan-converge, plan-deep, research, prd + plan-author, plan-tournament, plan-converge, research-validation, sequential-analysis, create-validation-plan + planner, researcher, red-teamer)
- `reflection.txt` — 3 commands + 5 skills + 1 agent (reflect, why, retro + reflect, critique, memorize, root-cause-tracing, plan-do-check-act + critic)
- `dispatch.txt` — 3 commands + 3 skills + 1 agent (dispatch, dispatch-parallel, dispatch-competitive + dispatch-parallel, judge, tree-of-thoughts + dispatch-judge)
- `observability.txt` — 3 commands + 1 skill + 0 agents (doctor, trace, install + observability-report) — status command dropped per UQ-V2-4

Sum check: 4+3+3+6+3+3+3 = 25 ✓
Skill sum check: 3+5+6+6+5+3+1 = 29
Agent sum check: 2+1+2+3+1+1+0 = 10 ✓

### Validators (real execution, no fakes)
- `commands.txt` — `scripts/check-commands.js` output: total=25, ok=25, errors=0
- `skills.txt` — `scripts/check-skills.js` output: total=29, ok=29, errors=0
- `agents.txt` — `scripts/check-agents.js` output: total=10, ok=10, errors=0 (model: opus everywhere)
- `seven-layer-overlay.txt` — `scripts/check-seven-layer.js` output: ok=true, 7 conceptual layers mapped, 4 enforcement modules verified on disk
- `manifest-revalidation.txt` — `scripts/_validate-manifest.js` re-run from Phase 2 — still PASS with 14 hook scripts registered, all present

### Counts files
- `command-count.txt`, `skill-count.txt`, `agent-count.txt` — single-line count files

### Totals
- `totals.txt` — commands=25 skills=29 agents=10

---

## File Layout

```
modules/
  orchestration/
    commands/      (4)  — cook, team, loop, autopilot
    skills/        (3)  — autopilot-runner, team-coordinator, loop-runner
    agents/        (2)  — executor, coordinator
  validation/
    commands/      (3)  — validate, audit, fix
    skills/        (5)  — functional-validation, evidence-gate, no-fakes-discipline, visual-inspection, consensus-engine
    agents/        (1)  — validator
  completion/
    commands/      (3)  — forge, audit-completion, resume
    skills/        (6)  — completion-gate, refusal-discipline, oracle-review, evidence-indexing, codebase-analysis, documentation-research
    agents/        (2)  — reviewer, oracle
  planning/
    commands/      (6)  — plan, plan-tournament, plan-converge, plan-deep, research, prd
    skills/        (6)  — plan-author, plan-tournament, plan-converge, research-validation, sequential-analysis, create-validation-plan
    agents/        (3)  — planner, researcher, red-teamer
  reflection/
    commands/      (3)  — reflect, why, retro
    skills/        (5)  — reflect, critique, memorize, root-cause-tracing, plan-do-check-act
    agents/        (1)  — critic
  dispatch/
    commands/      (3)  — dispatch, dispatch-parallel, dispatch-competitive
    skills/        (3)  — dispatch-parallel, judge, tree-of-thoughts
    agents/        (1)  — dispatch-judge
  observability/
    commands/      (3)  — doctor, trace, install
    skills/        (1)  — observability-report
    agents/        (0)  — (passive instrumentation)

commands/    — top-level symlinks → modules/*/commands/*.md (CC plugin loader sees these)
skills/      — top-level symlinks → modules/*/skills/*/SKILL.md
agents/      — top-level symlinks → modules/*/agents/*.md

docs/
  seven-layer-conceptual.md   — post-07 7 conceptual layers → 4 enforcement modules mapping
```

---

## Gate Summary

| Gate | Status | Evidence |
|---|---|---|
| 25 commands present with valid frontmatter | PASS | commands.txt |
| 29 skills present with valid frontmatter | PASS | skills.txt |
| 10 agents present with valid frontmatter + opus model | PASS | agents.txt |
| 7-layer conceptual overlay doc present + mapped | PASS | seven-layer-overlay.txt |
| Plugin manifest still valid post-additions | PASS | manifest-revalidation.txt |
| Per-domain inventories correct | PASS | <domain>.txt × 7 |

**Overall:** All gates PASS. Phase 3 deliverables complete.

---

## What is NOT in this phase

- Live `/plugin install shannon@shannon-local` against ~/.claude/plugins/ — task #8
- G1 (skill activation on real trigger) / G2 (hook fire in real session) / G3 (subagent inheritance) — task #9
- Atomic uninstall-others.sh integration test against live CC — task #8

---

## Refusals / known gaps

- **Skill count: 29 vs target 21.** Spec is internally inconsistent (`SHANNON-V6-SKILLS-AGENTS.md` Part A enumerates 22; `SHANNON-V6-ARCHITECTURE.md` §3 table column-sums to ~30 when summed across domains). Task brief lists the §3 enumeration explicitly in domain-by-domain spawn instructions, so I built per §3 minus UQ-V2-4 drop (statusline-config). Counts: orchestration 3 + validation 5 + completion 6 + planning 6 + reflection 5 + dispatch 3 + observability 1 = 29. To hit 21, would need to collapse plan-tournament/plan-converge into plan-author parameters, fold codebase-analysis + documentation-research into forge command itself, drop tree-of-thoughts. Did not collapse — task brief explicitly listed these as separate skills.

- **No live install yet.** `commands/`, `skills/`, `agents/` are populated via symlinks to `modules/*/`. CC plugin loader following symlinks is unverified in this phase — task #8 will install and verify.

