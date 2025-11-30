---
name: sh:memory
linked_skills:
  - shannon-serena-manager
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:memory
> **Skill-Based**: This command activates the `shannon-serena-manager` skill

## Usage
```bash
/sh:memory list
/sh:memory list checkpoint_*
/sh:memory read north_star_goal
/sh:memory search "react dashboard"
/sh:memory write my_key '{"data": "value"}'
```

## What It Does
High-level Serena MCP operations:
- **list** - List all memories (with optional pattern filter)
- **read** - Load memory by key (with similarity suggestions if not found)
- **write** - Save memory with automatic versioning and backup
- **search** - Full-text search across all memories
- **delete** - Safe deletion with backup

All operations output standardized SITREP.

## Skill Activation
📚 **Full memory logic**: `shannon-v4-plugin/skills/shannon-serena-manager/SKILL.md`

**Progressive disclosure**: Full skill content loaded only when activated

---

**Shannon V4** - Memory Management 💾
