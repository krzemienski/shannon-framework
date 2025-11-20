---
activation_condition: multi_paragraph_spec OR requirements_list OR explicit_command
auto_activate: true
category: command
command: /sh:spec
complexity: advanced
description: Analyzes user specifications and creates comprehensive implementation
  roadmaps with 8-dimensional complexity scoring, domain analysis, MCP suggestions,
  and phase planning
linked_skills:
- shannon-skill-generator
- shannon-spec-analyzer
mcp_servers:
- serena
- sequential
- context7
name: sh:spec
personas:
- system-architect
- requirements-analyst
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
triggers:
- spec
- specification
- requirements
- PRD
- multi-paragraph-system-description
---

/sh:spec - Specification Analysis & Planning

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

> **Shannon V3 Context Framework**: This command activates Shannon's specification analysis engine with 8-dimensional complexity scoring, domain identification, MCP discovery, and structured phase planning.

## Usage Patterns

**Basic Usage**:
```
/sh:spec [specification-text]
/sh:spec @path/to/requirements.md
/sh:spec "Build task management web app with React, Express, PostgreSQL"
```

**With Options**:
```
/sh:spec [spec] --depth quick|normal|deep
/sh:spec [spec] --create-phases
/sh:spec [spec] --suggest-mcps
/sh:spec [spec] --save-checkpoint
```

**Auto-Activation** (no explicit command needed):
```
[User provides 3+ paragraph specification]
[User provides 5+ item requirements list]
[User attaches .pdf/.md requirements document]
→ Shannon automatically activates spec analysis
```

**Type in Claude Code conversation window** (not terminal)

##

## Skill Integration

**v4 NEW**: This command activates skills:

- `shannon-skill-generator`
- `shannon-spec-analyzer`

## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
