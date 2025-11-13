---
category: command
command: /sh:restore
description: Restore project state from Serena MCP checkpoint
mcp_servers:
- serena
name: sh:restore
priority: critical
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
purpose: Restore project state from Serena MCP checkpoint
sub_agents:
- CONTEXT_GUARDIAN
triggers:
- restore
- resume
- recover
- reload
- continue
---

/sh:restore - Project State Restoration Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

## Purpose Statement

The `/sh:restore` command restores complete project state from Serena MCP checkpoints, enabling zero context loss after auto-compact events, session breaks, or context loss scenarios. This command activates the CONTEXT_GUARDIAN sub-agent to perform comprehensive context recovery.

**Core Function**: Load checkpoint → Restore all memories → Rebuild context → Resume work seamlessly

**Zero Context Loss Goal**: Restore 100% of project context within 30 seconds

---

## Usage Patterns

### Pattern 1: Default Restoration (Latest Checkpoint)
```bash
User: /sh:restore
```

**Execution**:
1. Read `latest_checkpoint` pointer from Serena
2. Load most recent checkpoint data
3. Restore all referenced memory keys
4. Validate restoration completeness
5. Present context summary to user
6. Resume from saved state

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
