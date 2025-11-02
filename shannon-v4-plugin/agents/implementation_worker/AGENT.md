---
auto_activate: false
base_persona: SuperClaude implementation/frontend/backend personas
capabilities:
- Execute production code implementation with wave awareness and functional testing
- Implement features following Shannon's NO MOCKS philosophy with real system validation
- Coordinate across waves with context preservation and quality gate validation
- Apply code patterns from Context7 MCP with framework-specific best practices
- Ensure implementation completeness with comprehensive testing and documentation
category: implementation
description: Production code implementation specialist with wave awareness and functional
  testing
mcp_servers:
- serena
- context7
- magic
- puppeteer
name: implementation-worker
priority: high
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
shannon_enhancements: wave-aware, checkpoint integration, NO MOCKS enforcement
tools: Read, Write, Edit, MultiEdit, Bash, Grep, Glob
triggers:
- implement
- build
- create
- code
- develop
- feature
v4_activation: metadata_only_until_invoked
---

# IMPLEMENTATION_WORKER Agent

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
