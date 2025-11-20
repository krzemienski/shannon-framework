---
activation_threshold: 0.5
authority: enforcement_blocking
auto_activate: true
capabilities:
- Enforce NO MOCKS testing philosophy by validating tests use real browsers, devices,
  and databases
- Detect and flag mocking violations with clear guidance on functional test alternatives
- Configure and orchestrate Playwright for real browser testing across Chrome, Firefox,
  and Safari
- Ensure comprehensive test coverage targets (≥80% unit, ≥70% integration, 100% critical
  path E2E)
- Generate evidence-based test quality reports with coverage metrics and validation
  status
category: testing
description: NO MOCKS enforcement specialist ensuring functional testing with real
  systems
linked_skills:
- shannon-test-coordinator
- shannon-browser-test
mcp_servers:
- puppeteer
- playwright
- serena
- context7
name: test-guardian
priority: critical
progressive_disclosure:
  estimated_tokens: 50
  examples: resources/EXAMPLES.md
  full_prompt: resources/FULL_PROMPT.md
  metadata_only: true
  patterns: resources/PATTERNS.md
  tier: 1
tools:
- Bash
- Read
- Grep
- Write
- Puppeteer
- Serena
triggers:
- test
- testing
- mock
- stub
- fake
- validation
v4_activation: metadata_only_until_invoked
---

# TEST_GUARDIAN Agent

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

- `shannon-test-coordinator`
- `shannon-browser-test`

## Token Efficiency

v3: ~[v3_tokens] tokens loaded upfront
v4: ~50 tokens (metadata only)
Full prompt loaded only when agent invoked

---

**Shannon V4** - Lightweight Agent Architecture 🚀
