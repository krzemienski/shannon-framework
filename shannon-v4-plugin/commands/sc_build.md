---
base_command: /build
category: command
command: /sc:build
description: Build command with wave orchestration, parallel builds, and NO MOCKS
  testing
linked_skills:
- shannon-browser-test
mcp_servers:
- serena
- shadcn
- puppeteer
- context7
name: sc:build
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
shannon_version: 3.0.0
sub_agents:
- IMPLEMENTATION_WORKER
- FRONTEND
- BACKEND
type: enhanced_superclaude
wave_enabled: true
---

/sc:build - Enhanced Build Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

## Purpose Statement

**Base Functionality** (SuperClaude): Project builder with automatic framework detection, intelligent persona activation, and MCP integration for builds and UI generation.

**Shannon V3 Enhancements**: Wave-based parallel builds, mandatory NO MOCKS functional testing, Serena checkpoint integration, and cross-wave context sharing for zero-context-loss build workflows.

**Primary Use Case**: Build features, components, or complete applications with parallel sub-agent execution and real-world validation testing.

---

## Usage Patterns

### Pattern 1: Component Build (Single Wave)
```bash
/sc:build LoginForm @src/components/
```
**Execution**:
- Wave 1: FRONTEND agent builds component + functional test
- Output: LoginForm.tsx + LoginForm.test.js (Puppeteer)

##

## Skill Integration

**v4 NEW**: This command activates skills:

- `shannon-browser-test`

## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
