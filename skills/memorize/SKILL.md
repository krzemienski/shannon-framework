---
name: memorize
description: Extract a learned pattern from session and save to memory. Cross-link with [[name]] to related memories.
triggers:
  - "remember this"
  - "save lesson"
  - "memorize pattern"
  - "save to memory"
  - "add to memory"
---

# memorize

Backs `/shannon:reflect --mode memorize`. Persists session-derived patterns to disk.

## Behavior contract

1. Identify what to memorize (user-pointed pattern, or extract from session).
2. Categorize the memory:
   - **user** — about who the user is, role, preferences
   - **feedback** — corrections + confirmations the user has given
   - **project** — current work-in-progress, decisions, deadlines
   - **reference** — pointers to external systems
3. Write memory file under `~/.claude/projects/<project>/memory/` (or `~/.claude/memory/` for global) with frontmatter:
   ```markdown
   ---
   name: <kebab-case-slug>
   description: <one-line summary>
   metadata:
     type: <user|feedback|project|reference>
   ---

   <body>

   Related: [[other-memory-name]]
   ```
4. Update `MEMORY.md` index with one-line pointer: `- [Title](file.md) — one-line hook`.

## When to use

- User says "remember this"
- Pattern emerges from session that will recur (drift detection, gotcha, preferred approach)
- After a correction the user gave that should not be repeated

## When NOT to use

- Ephemeral session state (use plan / tasks instead)
- Code conventions (those live in CLAUDE.md or `docs/code-standards.md`)
- Already-documented patterns

## Iron rules

- No duplicate memories — check MEMORY.md first; update existing if applicable.
- Frontmatter required. No drift across `name`, `description`, `type`.
- Body explains WHY (per feedback / project type structure).
- MEMORY.md is the index — never write content directly into it.
