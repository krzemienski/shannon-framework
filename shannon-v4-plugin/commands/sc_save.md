---
aliases:
- save
base_command: SuperClaude /save
category: command
command: /sc:save
complexity: standard
description: SuperClaude-compatible session checkpoint command that maps to Shannon's
  /sh:checkpoint
mcp-servers:
- serena
name: sc:save
personas: []
priority: critical
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
shannon_mapping: /sh:checkpoint
sub-agents:
- CONTEXT_GUARDIAN
triggers:
- save
- checkpoint
- backup
- preserve
- end-session
---

/sc:save - Enhanced Session Checkpoint

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

**Purpose**: SuperClaude-compatible session checkpoint command that maps to Shannon's `/sh:checkpoint` for comprehensive state preservation.

**Shannon V3 Enhancement**: Maintains SuperClaude `/save` compatibility while leveraging Shannon's advanced checkpoint system powered by CONTEXT_GUARDIAN agent.

---

## Usage Patterns

### Basic Usage
```bash
# Auto-generated checkpoint name
/sc:save

# Named checkpoint
/sc:save [checkpoint-name]

# Before ending session
/sc:save end_of_day

# Before risky operation
/sc:save before_experiment
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
