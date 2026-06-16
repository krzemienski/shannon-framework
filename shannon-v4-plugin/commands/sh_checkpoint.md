---
category: command
command: /sh:checkpoint
description: Create, load, or manage execution checkpoints for rollback and recovery
linked_skills:
- shannon-serena-manager
mcp_servers:
- serena
name: sh:checkpoint
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
sub_agents:
- CHECKPOINT_GUARDIAN
version: 3.0
---

/sh:checkpoint - Checkpoint Management

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

## Purpose

Create, load, and manage execution checkpoints that capture complete system state for rollback, recovery, and session continuity across context compactions.

**Core Objective**: Enable time-travel debugging and recovery by preserving complete state snapshots at critical execution boundaries.

---

## Usage Patterns

### Basic Usage
```bash
# Create checkpoint at current state
/sh:checkpoint

# Create named checkpoint
/sh:checkpoint create important_milestone

# Load specific checkpoint
/sh:checkpoint load cp_abc123

# List recent checkpoints
/sh:checkpoint list

# Compare checkpoints
/sh:checkpoint compare cp_abc123 cp_def456

# Rollback to checkpoint
/sh:checkpoint rollback cp_abc123
```

##

## Skill Integration

**v4 NEW**: This command activates skills:

- `shannon-serena-manager`

## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
