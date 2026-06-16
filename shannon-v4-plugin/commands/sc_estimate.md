---
activation_threshold: 0.6
auto_activate: true
base: SuperClaude /estimate command
category: command
command: /sc:estimate
description: Evidence-based development estimation with 8-dimensional complexity analysis
  and historical learning
mcp_servers:
- serena
- sequential
- context7
name: sc:estimate
output_format: structured_timeline_report
priority: high
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
shannon_enhancements: true
sub_agents:
- spec-analyzer
- phase-architect
tools:
- Read
- Grep
- Glob
- TodoWrite
triggers:
- estimate
- timeline
- effort
- duration
- how long
- time needed
- schedule
---

/sc:estimate - Evidence-Based Development Estimation

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

## Purpose Statement

Enhanced from SuperClaude's `/estimate` command, `/sc:estimate` provides **evidence-based development estimation** using Shannon V3's 8-dimensional complexity scoring, historical project data via Serena MCP, and systematic timeline calculation based on proven project patterns.

**Key Innovation**: Replaces speculative "gut feel" estimation with objective complexity scoring and historical data learning for reproducible, accurate timeline predictions.

## Usage Patterns

### Basic Usage
```
/sc:estimate "Build React e-commerce site with Stripe integration"
/sc:estimate @spec.md
/sc:estimate @PRD.pdf --detailed
```

##

## Skill Integration

**v4 NEW**: This command activates skills:


## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
