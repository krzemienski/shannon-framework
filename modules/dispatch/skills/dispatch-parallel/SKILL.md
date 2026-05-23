---
name: dispatch-parallel
description: Launch N parallel sub-agents with model selection, quality-focused prompting, meta-judge verification. Used in parallel, sequential, and competitive modes.
triggers:
  - "do in parallel"
  - "parallel subagents"
  - "fan out tasks"
  - "competitive dispatch"
---

# dispatch-parallel

Backs all three `/shannon:dispatch*` commands. Mode determined by invocation.

## Behavior contract

### Sequential mode (`/shannon:dispatch`)
1. Task list → ordered sequence.
2. Per task: spawn one subagent; wait; judge; proceed.

### Parallel mode (`/shannon:dispatch-parallel`)
1. Task list → batches of `--max-parallel`.
2. Per batch: spawn all subagents in same response (multiple tool calls in one assistant turn).
3. Wait for all; judge each; meta-judge cross-checks.

### Competitive mode (`/shannon:dispatch-competitive`)
1. Same task → N identical spawns in parallel.
2. Each owns isolated output directory.
3. Judge ranks; debate mode resolves ties.

## File ownership (LOAD-BEARING for parallel and competitive)

Each subagent owns its evidence/output directory exclusively. Cross-write = invalid run.

## Prompt construction

Each subagent receives:
- Task statement
- IRON RULE inject (via `subagent-governance-inject` hook on PreToolUse:Task)
- Output directory (exclusive write zone)
- Acceptance criteria
- Model selection (default opus per project rule)

## When to use

- Multi-step task with clear sequencing → sequential
- Independent tasks across files → parallel
- Single-output decision needing multiple perspectives → competitive

## When NOT to use

- Single short task → just do it inline, no dispatch needed
- Cross-task state required → sequential, never parallel/competitive

## Iron rules

- No shared mutable state across parallel/competitive subagents.
- File ownership enforced at spawn-prompt level.
- Model defaults to opus; opt-out only with explicit `--model` flag.
