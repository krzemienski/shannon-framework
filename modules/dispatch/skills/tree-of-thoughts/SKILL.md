---
name: tree-of-thoughts
description: Systematic exploration + pruning + expansion via Tree of Thoughts methodology. Branch on candidate sub-thoughts; meta-judge prunes.
triggers:
  - "tree of thoughts"
  - "explore branches"
  - "ToT reasoning"
  - "branch and prune"
---

# tree-of-thoughts

Used inside `/shannon:dispatch-competitive` when candidates need internal branching (sub-options per candidate).

## Behavior contract

1. Root node: task statement.
2. Expand N sub-thoughts (default 3 children per node).
3. For each sub-thought: evaluate via `judge` skill — keep top K, prune the rest.
4. Recursively expand surviving nodes (depth bounded by `--max-depth`, default 3).
5. Leaf nodes are candidate solutions; root-to-leaf path is the reasoning trace.
6. Final selection: best-scoring leaf path; full trace persisted under `reports/tot-<run-id>/`.

## When to use

- Decisions with multiple viable axes (e.g. architectural choices with cascading subdecisions)
- Search problems where pruning bad branches early saves compute
- Within `/shannon:dispatch-competitive` for deeper candidate exploration

## When NOT to use

- Linear task (no branching needed)
- Time-critical decision (ToT trades time for breadth)

## Iron rules

- Every node has a score + evidence.
- Pruned nodes are archived (never deleted) — `pruned/` subdirectory.
- Selected leaf path is a valid reasoning chain from root.
