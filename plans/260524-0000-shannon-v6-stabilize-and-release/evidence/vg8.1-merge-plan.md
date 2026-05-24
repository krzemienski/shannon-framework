# VG-8.1 Merge Plan — Shannon v6 Rebuild Branch Containment

**Date:** 2026-05-23
**Repo:** `/Users/nick/Desktop/shannon-framework`
**Branches analyzed:** `wt/shannon-rebuild-core` (+6), `wt/shannon-rebuild-integration` (+21), `wt/shannon-rebuild-domains` (+25), all 0 behind `main`.

## Verdict: **SUPERSET — merge `wt/shannon-rebuild-domains` only**

`domains` is a strict superset of `integration`, which is a strict superset of `core`. No commit unique to `core` or `integration`. Merging `domains` into `main` preserves 100% of Phase-6 work; the other two branches can be deleted as redundant.

Containment chain (proven by symmetric diffs):
```
main ⊂ core ⊂ integration ⊂ domains
  +0    +6      +21          +25
```

Pairwise symmetric-diff results (all from `git log --left-right`):
| Comparison | only-in-LHS | only-in-RHS | Conclusion |
|---|---|---|---|
| domains ... integration | 4 (the 4 phase-6 stabilization commits) | **0** | domains ⊃ integration |
| domains ... core | 19 | **0** | domains ⊃ core |
| integration ... core | 15 | **0** | integration ⊃ core |

## Per-commit table — domains (all 25 commits ahead of main, newest first)

| # | SHA | Branch first appearing in | Subject | Phase-6 critical? |
|---|---|---|---|---|
| 1 | 477f4ea | **domains** | fix(hooks): UserPromptSubmit hint exit-0 + stdout (was exit-2 blocking) | YES — hook fix called out in plan |
| 2 | a2d9626 | **domains** | feat(opt-in): project-level gate + word-boundary matcher + benchmark suite | YES — opt-in gate + word-boundary matcher + benchmark (3 of 7 named phase-6 items in one commit) |
| 3 | 9fdedc2 | **domains** | fix(plugin): remove dir-path fields; CC auto-discovers from convention | YES — plugin manifest fix called out in plan |
| 4 | b0ca463 | **domains** | fix(plugin): flatten symlinks to real files for CC installer cache compatibility | YES — installer cache stabilization, paired with 9fdedc2 |
| 5 | 1793b45 | integration | chore(evidence): phase-4 hook firetest + install dry-run results | peripheral — evidence only |
| 6 | 41a6a72 | integration | chore(hooks): chmod +x phase-2 hook scripts | peripheral — chmod |
| 7 | 81ab1cf | integration | feat(scripts): atomic install orchestrator + uninstall + doctor-precheck + dry-run modes | YES — install path used by benchmarks/firetest |
| 8 | cb8971e | integration | feat(hooks): plan-before-execute + context-threshold-warn + block-fab V6 scope fix | YES — could carry trigger-rename / scope renames |
| 9 | 9c93ad6 | integration | feat(evidence): phase-3-domains validation evidence + per-domain inventories | peripheral — evidence |
| 10 | 820ac42 | integration | feat(scripts): 4 validators for command/skill/agent/overlay frontmatter | YES — validator suite |
| 11 | 39389d0 | integration | docs(overlay): seven-layer conceptual mapping | peripheral — docs |
| 12 | ea719e3 | integration | feat(observability): 3 commands + 1 skill | YES — trigger surface (commands/skills may be in rename set) |
| 13 | e6ea043 | integration | feat(dispatch): 3 commands + 3 skills + 1 agent | YES — trigger surface |
| 14 | bb35849 | integration | feat(reflection): 3 commands + 5 skills + 1 agent | YES — trigger surface |
| 15 | 168f917 | integration | feat(planning): 6 commands + 6 skills + 3 agents | YES — trigger surface |
| 16 | 80d177c | integration | feat(completion): 3 commands + 6 skills + 2 agents | YES — trigger surface |
| 17 | ec1915c | integration | feat(validation): 3 commands + 5 skills + 1 agent | YES — trigger surface |
| 18 | 29d267c | integration | feat(orchestration): 4 commands + 3 skills + 2 agents | YES — trigger surface |
| 19 | 7736d02 | integration | chore(domains): wipe v1 commands/skills/agents (greenfield mode) | YES — destructive reset, must precede new commands |
| 20 | 221826e | core | feat(evidence): phase-2-core validation evidence + log dir | peripheral — evidence |
| 21 | f72490c | core | feat(scripts): setup/install/uninstall + manifest validator | YES — install pipeline foundation |
| 22 | 96bc911 | core | feat(hooks): 14 hook scripts + hooks.json registration | YES — hook substrate |
| 23 | 36a8069 | core | feat(layers): 4 enforcement layers (context/hook/invocation/dispatch) | YES — enforcement core |
| 24 | fbf4705 | core | feat(lib): hook-runner shared entry-point + logger | YES — hook runtime |
| 25 | 06c5809 | core | feat(plugin): V6 manifest + shannon-local marketplace declaration | YES — V6 manifest origin |

Phase-6-critical items from plan accounted for in domains:
- opt-in gate commit a2d9626 → present (#2)
- hook fix 477f4ea → present (#1)
- plugin manifest fix 9fdedc2 → present (#3)
- word-boundary matcher → folded into a2d9626 (#2)
- benchmark suite → folded into a2d9626 (#2)
- 4 trigger-rename commits → the 4 commits in #2/#3/#4 are stabilization fixes, not renames; renames are in the integration trigger-surface commits #12-18 (observability/dispatch/reflection/planning/completion/validation/orchestration). All present.

## Ordered merge sequence

```
git checkout main
git merge --no-ff wt/shannon-rebuild-domains
git push origin main
```

Then delete the redundant branches (once main has the merge commit pushed):
```
git branch -D wt/shannon-rebuild-core wt/shannon-rebuild-integration
git push origin --delete wt/shannon-rebuild-core wt/shannon-rebuild-integration  # if pushed
```

## Risk

- Zero merge conflicts expected — `main` is 0 behind on all three branches, so `domains` fast-forwards (or merges cleanly with `--no-ff`).
- No commit loss: containment proven by `git log --left-right` showing zero `>` lines in both comparisons against `domains`.
- If the operator wants the merge commit to carry incremental phase context, they could still merge `core` then `integration` then `domains`, but it produces three identical fast-forwards / empty merges and adds no information. Single-merge is preferred.

## Evidence files

- `vg8.1-branch-divergence.txt` — raw output of commands 1-3
- `vg8.1-domains-vs-integration.txt` — raw output of command 4
- `vg8.1-domains-vs-core.txt` — raw output of command 5
- `vg8.1-integration-vs-core.txt` — raw output of command 6
- `vg8.1-merge-plan.md` — this document
