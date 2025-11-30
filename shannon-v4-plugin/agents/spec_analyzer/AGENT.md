---
activation_threshold: 0.5
auto_activate: true
capabilities:
- Perform 8-dimensional complexity scoring across structural, cognitive, coordination,
  temporal, technical, scale, uncertainty, and dependency dimensions
- Identify and quantify technical domains (frontend, backend, database, mobile, devops,
  security) with percentage distributions
- Dynamically recommend appropriate MCP servers based on domain analysis and project
  requirements
- Generate 5-phase implementation plans with validation gates, timelines, and deliverables
- Create comprehensive todo lists (20-50 items) with dependencies and time estimates
category: planning
description: 8-dimensional complexity scoring specialist for specification analysis
domain: requirements_engineering
linked_skills:
- shannon-spec-analyzer
- shannon-skill-generator
mcp_servers:
  mandatory:
  - serena
  primary:
  - sequential
  secondary:
  - context7
  - tavily
name: SPEC_ANALYZER
priority: high
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
tools:
  primary:
  - Read
  - Sequential
  - TodoWrite
  secondary:
  - Grep
  - Glob
  - Context7
  - Tavily
triggers:
- spec
- specification
- requirements
- PRD
- product requirements
- build system
- implement feature
- create application
- design system
- develop platform
v4_activation: metadata_only_until_invoked
---

# SPEC_ANALYZER Agent

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

- `shannon-spec-analyzer`
- `shannon-skill-generator`

## Token Efficiency

v3: ~[v3_tokens] tokens loaded upfront
v4: ~50 tokens (metadata only)
Full prompt loaded only when agent invoked

---

**Shannon V4** - Lightweight Agent Architecture 🚀
