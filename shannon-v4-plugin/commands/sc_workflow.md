---
auto_activate: false
base_command: /workflow
category: command
command: /sc:workflow
complexity: advanced
description: Enhanced workflow orchestration with wave-based phase execution, systematic
  validation gates, and PRD-to-production planning
enhancements:
- wave_workflows
- phase_integration
- checkpoint_system
- structured_templates
mcp_servers:
- serena
- sequential
- context7
name: sc:workflow
personas:
- architect
- analyzer
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
triggers:
- workflow
- orchestrate
- coordinate
- plan-execution
- systematic
---

/sc:workflow - Enhanced Workflow Orchestration Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

> **Shannon V3 Enhancement**: SuperClaude's `/workflow` command enhanced with wave-based workflow orchestration, 5-phase integration, systematic validation gates, and structured execution templates.

## Usage Patterns

**Basic Usage**:
```
/sc:workflow [project-name]
/sc:workflow "E-commerce Platform"
/sc:workflow @specs/project-spec.md
```

**With Template Selection**:
```
/sc:workflow [project] --template fullstack
/sc:workflow [project] --template mobile
/sc:workflow [project] --template api-service
/sc:workflow [project] --template custom
```

**With Phase Targeting**:
```
/sc:workflow [project] --start-phase 2
/sc:workflow [project] --phases 1-3
/sc:workflow [project] --skip-discovery
```

**With Wave Control**:
```
/sc:workflow [project] --waves 4
/sc:workflow [project] --sequential (disable parallelization)
/sc:workflow [project] --max-concurrent 3
```

**With Checkpoint Management**:
```
/sc:workflow [project] --auto-checkpoint
/sc:workflow [project] --checkpoint-interval 30m
/sc:workflow [project] --resume-from-checkpoint
```

**Type in Claude Code conversation window** (not terminal)

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
