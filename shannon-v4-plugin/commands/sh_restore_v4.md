---
name: sh:restore
linked_skills:
  - shannon-context-restorer
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:restore
> **Skill-Based**: This command activates the `shannon-context-restorer` skill

## Usage
```bash
/sh:restore
/sh:restore latest
/sh:restore checkpoint_myproject_1730739600000
```

## What It Does
Restores complete project context from checkpoint:
- North Star goal
- Active todos
- Current phase/wave
- Recent decisions
- Generated skills list

Enables:
- Session continuity after restart
- Recovery after auto-compaction
- Time-travel to previous states
- Disaster recovery

Outputs SITREP with:
- Restoration completeness (%)
- What was restored
- Next steps to continue work

## Skill Activation
📚 **Full restoration logic**: `shannon-v4-plugin/skills/shannon-context-restorer/SKILL.md`

**Progressive disclosure**: Full skill content loaded only when activated

---

**Shannon V4** - Session Restoration 🔄
