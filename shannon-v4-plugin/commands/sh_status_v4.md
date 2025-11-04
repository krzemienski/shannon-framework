---
name: sh:status
linked_skills:
  - shannon-status-reporter
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:status
> **Skill-Based**: This command activates the `shannon-status-reporter` skill

## Usage
```bash
/sh:status
```

## What It Does
Generates standardized SITREP (Situation Report) with all 7 required sections:
- Status (Phase, Progress, State)
- Context (Objective, Scope, Dependencies)
- Findings (Key discoveries)
- Issues (Blockers, Risks, Questions)
- Next Steps (Action items)
- Artifacts (Generated files)
- Validation (Tests, Results)

Saves to Serena MCP with unique ID for history tracking.

## Skill Activation
📚 **Full SITREP logic**: `shannon-v4-plugin/skills/shannon-status-reporter/SKILL.md`

**Progressive disclosure**: Full skill content loaded only when activated

---

**Shannon V4** - Status Reporting 📋
