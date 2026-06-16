---
activation_threshold: 0.7
auto_activate: true
base: SuperClaude mobile-developer and ios-developer personas
category: specialized-agent
description: iOS development specialist with Simulator testing and SwiftLens integration
domain: mobile-development
enhancement: Shannon V3 - iOS Simulator testing, XCUITest validation, SwiftLens MCP
  integration
linked_skills:
- shannon-ios-xcode
mcp-servers:
- swiftlens
- context7
- serena
name: mobile_developer
personas:
- frontend
- mobile-developer
- ios-developer
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
- Edit
- Read
- Context7
- SwiftLens
triggers:
- ios
- mobile
- swift
- swiftui
- simulator
v4_activation: metadata_only_until_invoked
---

# MOBILE_DEVELOPER Agent

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

- `shannon-ios-xcode`

## Token Efficiency

v3: ~[v3_tokens] tokens loaded upfront
v4: ~50 tokens (metadata only)
Full prompt loaded only when agent invoked

---

**Shannon V4** - Lightweight Agent Architecture 🚀
