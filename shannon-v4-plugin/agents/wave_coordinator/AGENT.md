---
activation_threshold: 0.7
auto_activate: true
capabilities:
- Orchestrate multi-stage command execution with compound intelligence and parallel
  sub-agent coordination
- Auto-detect wave-eligible operations based on complexity (≥0.7), file count (>20),
  and operation diversity (>2)
- Implement progressive, systematic, and adaptive wave strategies based on project
  requirements
- Manage wave checkpoints with rollback capabilities and context preservation across
  wave boundaries
- Optimize execution through intelligent wave sizing and cross-wave learning
category: orchestration
depends_on:
- spec-analyzer
- phase-planner
description: Orchestrates parallel sub-agent execution across multiple waves with
  complete context preservation
linked_skills:
- shannon-context-loader
- shannon-wave-orchestrator
mcp_servers:
- serena
- sequential
name: WAVE_COORDINATOR
priority: critical
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
tools:
- Task
- Read
- TodoWrite
triggers:
- wave
- orchestrate
- parallel
- coordinate
- multi-agent
- create-waves
v4_activation: metadata_only_until_invoked
---

# WAVE_COORDINATOR Agent

> **Shannon V4**: Lightweight frontmatter only. Full prompt loaded on-demand.

## Activation

This agent activates when:
- Explicitly invoked via Task tool
- Auto-activated by matching triggers/keywords
- Referenced by commands or other agents

## Progressive Disclosure

**Tier 1** (Loaded): This metadata (~50 tokens)
**Tier 2** (On-Demand): Full agent prompt → [resources/FULL_PROMPT.md](./resources/FULL_PROMPT.md)
**Tier 3** (On-Demand): Examples → [resources/EXAMPLES.md](./resources/EXAMPLES.md)
**Tier 4** (On-Demand): Patterns → [resources/PATTERNS.md](./resources/PATTERNS.md)

## Linked Skills

- `shannon-context-loader`
- `shannon-wave-orchestrator`

## Token Efficiency

v3: ~[v3_tokens] tokens loaded upfront
v4: ~50 tokens (metadata only)
Full prompt loaded only when agent invoked

---

**Shannon V4** - Lightweight Agent Architecture 🚀
