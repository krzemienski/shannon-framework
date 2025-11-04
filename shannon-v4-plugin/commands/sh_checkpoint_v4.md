---
name: sh:checkpoint
linked_skills:
  - shannon-checkpoint-manager
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:checkpoint
> **Skill-Based**: This command activates the `shannon-checkpoint-manager` skill

## Usage
```bash
/sh:checkpoint "Completed authentication system"
/sh:checkpoint "Wave 2 done"
```

## What It Does
Creates comprehensive project checkpoint that preserves:
- Current phase/wave position
- Active and pending todos
- North Star goal
- Recent decisions
- Modified files list
- Generated skills
- Complete project context

Enables zero-context-loss across:
- Session ends
- Auto-compaction events
- Deliberate save points

Outputs SITREP with checkpoint ID and restoration instructions.

## Skill Activation
📚 **Full checkpoint logic**: `shannon-v4-plugin/skills/shannon-checkpoint-manager/SKILL.md`

**Progressive disclosure**: Full skill content loaded only when activated

---

**Shannon V4** - Context Preservation 🛡️
