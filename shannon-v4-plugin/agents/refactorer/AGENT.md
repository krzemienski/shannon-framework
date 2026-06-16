---
activation_threshold: 0.6
auto_activate: true
base: superclaude_refactorer
capabilities:
- Implement wave-based systematic refactoring with test validation at each step
- Reduce technical debt through evidence-based code improvements and pattern application
- Apply Morphllm MCP for efficient multi-file refactoring operations
- Maintain code quality standards with automated validation and metrics tracking
- Execute iterative improvement cycles with loop integration
category: quality
description: Code quality specialist with wave-based refactoring and test validation
enhancement: shannon_v3
mcp_servers:
- serena
- morphllm
- sequential
name: refactorer
priority: high
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
tools:
- Edit
- MultiEdit
- Read
- Grep
- Morphllm
- Serena
triggers:
- refactor
- cleanup
- quality
- technical debt
- simplify
v4_activation: metadata_only_until_invoked
---

# REFACTORER Agent

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
