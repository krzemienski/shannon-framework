# VG-7.1 — Live ref grep audit: `shannon-framework`

## Summary

Grep from `blog-series/` root, excluding `.archive/ e2e-evidence/ node_modules/ .next/ plans/ .git/ shannon-framework/`.

- **Total hits:** 10 across 6 files
- **COMPANION_CONCEPT:** 5
- **DOC_INVENTORY:** 4
- **ORPHAN_DEPENDENT:** 0
- **OTHER:** 1 (.gitignore — ignores orphan, does not depend on it)

**ORPHAN_DEPENDENT (BLOCKING) rows:** NONE.

**Verdict: GREEN** — no row requires the local `shannon-framework/` directory to exist. No import path / build script / sync target / sitemap entry depends on it. Deletion is not blocked. Optional doc-inventory edits only.

## Categorized table

| file:line | category | excerpt | suggested action |
|-----------|----------|---------|------------------|
| `.gitignore:131` | OTHER | `shannon-framework/` | none — ignore rule targets the orphan dir; once deleted the rule is harmless stale noise (no dependency). Optional: drop the line. |
| `CLAUDE.md:40` | DOC_INVENTORY | `\| 07 \| `shannon-framework/` \| Claude Code plugin, 4-layer enforcement \|` | none/edit — companion-repo table; truth-preserving as a repo concept. No local-dir dependency. |
| `CLAUDE.md:49` | DOC_INVENTORY | `\| 16 \| `shannon-framework/` \| Plugin hooks + enforcement \|` | none/edit — same table, post 16 row. No local-dir dependency. |
| `TASKS.md:9` | DOC_INVENTORY | `Phase 5: Harden 5 companion repos ... shannon-framework, ...` | none — names the companion repo to git-init, not a local-dir dependency. |
| `posts/INDEX.md:63` | COMPANION_CONCEPT | `\| 7 \| ... \| [shannon-framework](https://github.com/krzemienski/shannon-framework) \|` | none — GitHub URL. |
| `posts/INDEX.md:72` | COMPANION_CONCEPT | `\| 16 \| ... \| [shannon-framework](https://github.com/krzemienski/shannon-framework) \|` | none — GitHub URL. |
| `posts/INDEX.md:122` | DOC_INVENTORY | `shannon-framework                 Posts 7, 16 — prompt stack + plugins` | none/edit — repo-to-post map; concept, not local dir. |
| `posts/post-07-prompt-engineering-stack/frontmatter.json:8` | COMPANION_CONCEPT | `"github_repo": "https://github.com/krzemienski/shannon-framework",` | none — GitHub URL. |
| `posts/post-07-prompt-engineering-stack/post-blocks.ts:36` | COMPANION_CONCEPT | `... from the [shannon-framework](https://github.com/krzemienski/shannon-framework) repo ...` | none — GitHub URL in prose. |
| `posts/post-07-prompt-engineering-stack/post-blocks.ts:141` | COMPANION_CONCEPT | `... in the [shannon-framework](https://github.com/krzemienski/shannon-framework) repo encodes ...` | none — GitHub URL in prose. |

## Rationale

Every reference is either (a) a GitHub URL to the sibling repo `github.com/krzemienski/shannon-framework` (survives orphan deletion — concept, not local path), or (b) an inventory mention in a doc/task list. None resolves to the local `blog-series/shannon-framework/` directory as a build/import/sync/sitemap input.

`.gitignore:131` is the only entry that literally names the local path, but it *ignores* the dir — it has no build-time dependency on the dir's presence. After deletion the rule becomes dead but harmless.
