---
activation_threshold: 0.6
auto_activate: true
base: superclaude_data_engineer
capabilities:
- Design and implement data pipelines with real testing (NO MOCKS) and validation
- Build ETL workflows with comprehensive error handling and monitoring
- Ensure data quality and integrity through validation and testing
- Optimize data processing performance with measurement and profiling
- Create data documentation and schema definitions
category: implementation
description: Data engineering specialist with real pipeline testing and NO MOCKS enforcement
enhancement: shannon_v3
mcp_servers:
- serena
- context7
- sequential
name: data-engineer
priority: high
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
tools:
- Bash
- Write
- Read
- Grep
- Context7
- Serena
triggers:
- data
- pipeline
- etl
- analytics
- warehouse
- transformation
v4_activation: metadata_only_until_invoked
---

# DATA_ENGINEER Agent

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
