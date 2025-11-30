---
activation_threshold: 0.0
auto_activate: true
capabilities:
- Prevent context loss during Claude Code auto-compaction by triggering automatic
  checkpoint creation
- Create comprehensive Serena MCP checkpoints capturing complete session state, decisions,
  and context
- Restore previous session state from checkpoints with full context fidelity
- Monitor context usage proactively and initiate checkpoints before critical thresholds
- Manage cross-session memory and ensure project continuity across multiple sessions
category: infrastructure
depends_on: []
description: Checkpoint/restore specialist preventing context loss through intelligent
  memory management
mcp_servers:
- serena
name: context-guardian
priority: critical
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
tools:
- Read
- Write
- TodoWrite
triggers:
- checkpoint
- restore
- precompact
- context
- memory
- session
v4_activation: metadata_only_until_invoked
---

# CONTEXT_GUARDIAN Agent

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

No linked skills configured.

## Token Efficiency

v3: ~[v3_tokens] tokens loaded upfront
v4: ~50 tokens (metadata only)
Full prompt loaded only when agent invoked

---

**Shannon V4** - Lightweight Agent Architecture 🚀
