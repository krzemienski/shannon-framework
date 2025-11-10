# Agent Skills in Claude Code

Agent Skills package expertise into discoverable capabilities.

## What are Skills?

Each Skill = `SKILL.md` file with instructions + optional supporting files.

**Model-invoked**: Claude autonomously decides when to use based on description.

## Creating Skills

### Personal Skills
Location: `~/.claude/skills/my-skill-name/`

### Project Skills
Location: `.claude/skills/my-skill-name/`

## SKILL.md Structure

```yaml
---
name: your-skill-name
description: What this does and when to use it
---

# Your Skill Name

## Instructions
Step-by-step guidance.
```

**Field requirements:**
- `name`: lowercase, numbers, hyphens only (max 64 chars)
- `description`: Brief description (max 1024 chars)

## Directory Structure

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional)
├── scripts/ (optional)
└── templates/ (optional)
```

## Restrict Tools

```yaml
---
name: safe-reader
description: Read-only file access
allowed-tools: Read, Grep, Glob
---
```

## Testing

Ask questions matching the description:

```
Can you help me extract text from this PDF?
```

Claude automatically uses the Skill if it matches.
