# VG-7.0 — Post-16 / shannon-framework Contract Verdict

**Plan:** `plans/260524-0000-shannon-v6-stabilize-and-release/plan.md`
**Gate:** VG-7.0 (Post-16 contract resolution)
**Date:** 2026-05-23
**Investigator:** general-purpose subagent (read-only)
**Trees under test:**
- Canonical: `/Users/nick/Desktop/shannon-framework/` (own .git, GitHub remote `https://github.com/krzemienski/shannon-framework.git`, 35 hooks + 30 skill dirs + 10 agents)
- Orphan: `/Users/nick/Desktop/blog-series/shannon-framework/` (own .git, 3 root files + 4 dirs; only 6 files under hooks+skills+agents)

---

## 1. How post-16 references shannon-framework

Source files inspected (BOTH are live — see `feedback_typed_block_overrides_postmd.md`: the typed `post-16.ts` is what renders on withagents.dev):

- `posts/post-16-claude-code-plugins/post.md` (markdown source, 418 lines)
- `site/src/lib/post-bodies/post-16.ts` (typed Block[] body, 326 lines)

Both files reference the repo **by GitHub URL only** — never by local path:

- Frontmatter `github_repo: "https://github.com/krzemienski/shannon-framework"` (post.md:11)
- Inline link: `[shannon-framework](https://github.com/krzemienski/shannon-framework)` (post.md:62, post.md:417)
- The typed body (`post-16.ts:41`) drops the markdown link and just says "from the shannon-framework" — still no local-path hint.

There is **zero** language anywhere in either source telling the reader to clone, browse, inspect, or otherwise touch `/Users/nick/Desktop/blog-series/shannon-framework/`. The reader contract is `git clone https://github.com/krzemienski/shannon-framework` (or visit the URL on GitHub).

The orphan tree has no separate URL, no documentation pointing readers to it, and no role in the render pipeline.

Evidence: `vg7.0-post16-refs.txt`

---

## 2. File-by-file table — what post-16 expects vs what each tree provides

Six artifacts are *named* or *quoted in full* inside post-16:

| File referenced in post-16 | canonical_has | orphan_has | Notes |
|---|---|---|---|
| `hooks/validation-not-compilation.js` (full source quoted, post.md:69–124) | YES — `/Users/nick/Desktop/shannon-framework/hooks/validation-not-compilation.js` (1.1K) | YES — `/Users/nick/Desktop/blog-series/shannon-framework/hooks/validation-not-compilation.js` | **Implementations diverge.** Orphan = ES-module `export default` (matches post snippet byte-for-byte intent). Canonical = CommonJS `runHook()` wrapper writing `[shannon] validation-not-compilation:` stderr referencing `/shannon:validate`. The post's verbatim source quote no longer matches canonical. |
| `hooks/block-test-files.js` (full source quoted, post.md:202–245) | **NO** — file does not exist; renamed to `hooks/block-fab-files.js` (`find` returned 0 matches for `block-test-files`) | YES — `/Users/nick/Desktop/blog-series/shannon-framework/hooks/block-test-files.js` (1.9K, matches post snippet) | Canonical renamed test→fab and rewrote with `runHook()` wrapper + 12 different FAB_PATTERNS + EXEMPTIONS table. A reader cloning canonical and grepping for `block-test-files.js` finds nothing. |
| `hooks/read-before-edit.js` (named only, post.md:251) | YES (603B) | YES (1.7K) | Both exist; canonical is shorter, orphan keeps post-cited Set-tracking implementation. Behavior is named but not quoted in post — naming-level reference passes. |
| `hooks/evidence-gate-reminder.js` (full source quoted, post.md:260–276) | YES (966B) | YES (1.4K) | Canonical implementation differs in size; not byte-compared, but the file *exists by the cited name* in both. |
| `hooks/skill-activation-check.js` (named only, post.md:281) | YES (1.2K) | YES (1.2K) | Both have it. |
| `skills/functional-validation` (named only, post.md:356, post.md:404) | YES — directory at `/Users/nick/Desktop/shannon-framework/skills/functional-validation/` | YES — directory at `/Users/nick/Desktop/blog-series/shannon-framework/skills/functional-validation/` | Directory present in both. |

Evidence: `vg7.0-canonical-tree.txt`, `vg7.0-orphan-tree.txt`, `e2e-evidence/repo-reference-audit.md` lines 154–161 (audit dated 2026-03-06 verified canonical-pre-rename: "Snippet 1: block-test-files.js -- PASS").

---

## 3. Reader-contract analysis

A new reader of post-16 takes one of two paths:

1. **GitHub path (>99% of readers).** Click `https://github.com/krzemienski/shannon-framework`, land on the canonical repo, clone it, look for the five hooks the post names.
   - They will FIND: `validation-not-compilation.js`, `read-before-edit.js`, `evidence-gate-reminder.js`, `skill-activation-check.js`, `skills/functional-validation/`.
   - They will NOT FIND: `hooks/block-test-files.js` (renamed to `block-fab-files.js`).
   - Of the two files whose **full source is quoted** in the post (`validation-not-compilation.js`, `block-test-files.js`), one no longer exists by that name and the other has been rewritten to a different module shape. The post's `export default function validationNotCompilation(...)` no longer matches canonical's `runHook('validation-not-compilation', (payload) => ...)`.
   - This is a **drift between published post and canonical repo**, but it is not an orphan-tree problem — it is a post-vs-canonical contract problem that exists whether or not the orphan tree is on disk.

2. **Local-orphan path (zero readers).** Nothing in the post, the site, the deploy, or the public docs tells anyone the orphan exists. It is `/Users/nick/Desktop/blog-series/shannon-framework/` — a path only the author can see. Public readers never touch it.

The orphan tree is therefore **not part of the reader contract**. It is an internal post-16 demo snapshot that was checked in alongside the post during initial authoring (audit dated 2026-03-06 confirmed PASS against canonical *at that time*, when canonical still had `block-test-files.js`).

---

## 4. Risk of deleting the orphan

| Risk | Mitigated? |
|---|---|
| Post-16 readers can no longer follow along | NO RISK — post links to GitHub, not to the orphan path. |
| `site/` build references orphan path | UNVERIFIED here, but post-16.ts only embeds source as string literals — no filesystem read at build time. (Recommend `grep -rn 'blog-series/shannon-framework' site/` before deletion.) |
| Orphan contains source code that canonical lost | **PARTIAL RISK** — orphan's `block-test-files.js` (the version quoted verbatim in the published post) does not exist in canonical under that filename. If the canonical's `block-fab-files.js` is considered the successor and the post is later amended to match, the orphan adds nothing. If the post stays as-published, canonical does not literally satisfy the byte-quoted source. |
| Loss of git history in the orphan | Orphan has its own `.git`. If history matters, archive `.git` to `.archive/deprecated-sites/` per `docs/canonical-topology.md` archive zone before deletion. |

---

## 5. FINAL VERDICT

**`RECONCILE_NEEDED_BEFORE_DELETE`**

Rationale:

- The reader contract is GitHub-based, so the orphan does not need to live on disk for readers (`ORPHAN_SAFE_TO_DELETE` would be defensible from a pure reader-contract standpoint).
- BUT the post quotes `block-test-files.js` source verbatim, and that file no longer exists in canonical under that name. Before the orphan is deleted, **one of these must happen first**:
  1. **Amend post-16** to (a) rename the section to `block-fab-files.js`, (b) replace the verbatim source with canonical's current `runHook()`-style implementation, and (c) re-screenshot/re-render. After amendment, the orphan is truly redundant and can be deleted. — OR —
  2. **Confirm via post-author** that the post-as-published is allowed to drift from the canonical repo (i.e., the published code snippets are frozen as historical artifacts, and readers are expected to find the equivalent in canonical under the new name). After explicit author sign-off, delete the orphan and add a note to `e2e-evidence/repo-reference-audit.md` documenting the rename. — OR —
  3. **Restore `block-test-files.js` as a thin alias / legacy export in canonical** pointing to `block-fab-files.js`, so the post's source still resolves. After verification (`ls /Users/nick/Desktop/shannon-framework/hooks/block-test-files.js`), delete the orphan.

The orphan tree's `block-test-files.js` is the *only* on-disk artifact that still matches the published post verbatim. Deleting it before one of the three reconciliation paths above leaves a published post quoting source code that exists nowhere on disk.

A delete-now plan would be defensible only if VG-7.0's success criterion is "no broken links from post to GitHub URL" (true today). It is NOT defensible if the criterion is "post-quoted source must exist somewhere referenceable" (false after orphan deletion).

---

## 6. Recommended next step (out-of-scope for this gate)

Open VG-7.1 = "Decide reconciliation path (amend post / freeze post / restore alias) for `block-test-files.js`" and block orphan deletion on that decision. The orphan stays on disk until VG-7.1 resolves.

---

## Evidence cited

- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/vg7.0-post16-refs.txt`
- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/vg7.0-canonical-tree.txt`
- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/vg7.0-orphan-tree.txt`
- `/Users/nick/Desktop/blog-series/posts/post-16-claude-code-plugins/post.md` (lines 11, 62, 69–124, 202–245, 260–276, 417)
- `/Users/nick/Desktop/blog-series/site/src/lib/post-bodies/post-16.ts` (lines 41, 132, 161, 167, 285)
- `/Users/nick/Desktop/blog-series/e2e-evidence/repo-reference-audit.md` (lines 154–161, 216)
- `/Users/nick/Desktop/shannon-framework/hooks/validation-not-compilation.js`
- `/Users/nick/Desktop/shannon-framework/hooks/block-fab-files.js` (the rename)
- `/Users/nick/Desktop/blog-series/shannon-framework/hooks/block-test-files.js`
- `/Users/nick/Desktop/blog-series/shannon-framework/hooks/validation-not-compilation.js`
