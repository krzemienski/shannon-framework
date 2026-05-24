# G7-AMEND — Post-16 reconciled to canonical shannon-framework v6

**Gate:** G7-AMEND (follow-up to VG-7.0 verdict `RECONCILE_NEEDED_BEFORE_DELETE`)
**Plan:** `plans/260524-0000-shannon-v6-stabilize-and-release/plan.md`
**Date:** 2026-05-23
**Executor:** general-purpose subagent
**Reconciliation path chosen:** Option 1 from VG-7.0 §5 — amend post-16 to canonical.

---

## 1. Files edited (exactly 2 — scope respected)

| File | Repo | Diff size | Path |
|---|---|---|---|
| `posts/post-16-claude-code-plugins/post.md` | blog-series (top-level) | 241 lines | `evidence/g7-amend-post-md.diff` |
| `site/src/lib/post-bodies/post-16.ts` | site/ submodule | 235 lines | `evidence/g7-amend-post16-ts.diff` |

**No frontmatter touched.** Title, subtitle, date, series_number, series_total, github_repo, tags, slug, canonicalUrl, all metadata unchanged.

**No other files touched.** Did NOT run build, lint, dev, or git mutations beyond `git diff`.

---

## 2. Canonical source quoted (byte-equivalent to shannon-framework HEAD)

Source files read verbatim from canonical:
- `/Users/nick/Desktop/shannon-framework/hooks/validation-not-compilation.js` (21 lines)
- `/Users/nick/Desktop/shannon-framework/hooks/block-fab-files.js` (82 lines)

Both files were replaced into post.md and post-16.ts as the literal canonical source. The TypeScript template literal in post-16.ts escapes backslashes per the existing pattern (`\\b` for `\b`, `\\/` for `/`, `\\n` for `\n`).

---

## 3. Changes made (per file, per section)

### post.md
1. **Lines 68–124 (old) → new validation-not-compilation source block** — replaced 56-line legacy ES-module quote with 20-line canonical CommonJS `runHook()` wrapper. Added 1-sentence Shannon-v6 explanatory note immediately after the code fence.
2. **Line 197 → header rename** — `### block-test-files.js — The Hard Stop` → `### block-fab-files.js — The Hard Stop`. Lead-in paragraph rewritten to describe fabricated-artifact patterns + scope/exemption tables.
3. **Lines 202–245 (old) → new block-fab-files source block** — replaced 44-line legacy quote with 82-line canonical implementation (FAB_PATTERNS, EXEMPTIONS, ACTIVE_SCOPE, `runHook('block-fab-files', …)`).
4. **Closing paragraph for the section** — rewritten to call out the Shannon-v6 rename + scope/exemption rationale.
5. **Line 378 (Skills reinforcement)** — `block-test-files.js` → `block-fab-files.js`.
6. **Line 403 (Shannon Insight enumerated list, item 2)** — `block-test-files.js` → `block-fab-files.js`.

### site/src/lib/post-bodies/post-16.ts
1. **Block at code{lang:javascript, caption: ".claude/hooks/validation-not-compilation.js"}** — caption changed to `hooks/validation-not-compilation.js`; body replaced with canonical CommonJS source (backslash-escaped). Added a new `{type:"p"}` block explaining the v6 refactor.
2. **Lead-in paragraph for the second hook (`block-test-files.js — The Hard Stop`)** — rewritten to `block-fab-files.js — The Hard Stop` with the new scope/exemption description.
3. **Code block** — caption `block-test-files.js · pattern matcher` → `hooks/block-fab-files.js`; body replaced with canonical source (backslash-escaped).
4. **Trailing paragraph** — rewritten to document the rename.
5. **Skills-reinforcement paragraph (line ~307)** — `block-test-files.js` → `block-fab-files.js`.
6. **Shannon Insight list (line ~321)** — `block-test-files.js` → `block-fab-files.js`.

Preserved: lead, pull-quote, tldr, all charts, all `wa` diagram blocks, all JSON snippets, all stdin/stdout-contract code blocks, "Other Four Hooks" header, evidence-gate-reminder code block, all narrative paragraphs unrelated to these two hooks.

---

## 4. Verification grep output (Step 6)

### A. `block-test-files` — expect 0 bare/code references, 2 prose hits documenting the rename

```
posts/post-16-claude-code-plugins/post.md:252: Twelve patterns cover test files, mocks, stubs, fakes, and fixtures across language conventions. Shannon v6 renamed the hook from `block-test-files.js` to `block-fab-files.js` (fabricated artifacts) and added scope + exemption tables so the matcher no longer false-positives on legitimate `scripts/`, `tools/`, or skill markdown. Every block message includes the path, the matched pattern, and the IRON RULE that explains why.

site/src/lib/post-bodies/post-16.ts:217: { type: "p", text: "Twelve patterns cover test files, mocks, stubs, fakes, and fixtures across language conventions. Shannon v6 renamed the hook from block-test-files.js to block-fab-files.js (fabricated artifacts) and added scope + exemption tables so the matcher no longer false-positives on legitimate scripts/, tools/, or skill markdown. Every block message includes the path, the matched pattern, and the IRON RULE that explains why." },
```

Both remaining hits are **intentional rename-prose** (one sentence per file documenting the v6 rename). No code-block, no header, no inline-tick reference to the old name remains.

### B. `block-fab-files` — expect ≥1 per file (got many — header, code, prose, refs)

```
post.md:164: ### block-fab-files.js — The Hard Stop
post.md:226: runHook('block-fab-files', (payload) => {
post.md:247: stderrPayload: `[shannon] block-fab-files: …`
post.md:252: rename-prose (above)
post.md:383: The `block-fab-files.js` hook prevents shortcuts
post.md:408: The `block-fab-files.js` hook blocks test file creation

post-16.ts:134: block-fab-files.js — The Hard Stop. PreToolUse on Write, Edit, MultiEdit…
post-16.ts:135: caption: "hooks/block-fab-files.js"
post-16.ts:193: runHook('block-fab-files', (payload) => {
post-16.ts:214: stderrPayload: …block-fab-files: …
post-16.ts:217: rename-prose
post-16.ts:307: The block-fab-files.js hook prevents shortcuts
post-16.ts:321: "The block-fab-files.js hook blocks test file creation at the tool boundary."
```

### C. `validationNotCompilation` / `validation-not-compilation` — expect present (canonical retained)

Distinguishing canonical lines (post.md):
- L76: `runHook('validation-not-compilation', (payload) => {`
- (canonical wraps via `runHook` from `lib/hook-runner` — old `export default function validationNotCompilation` removed)

Distinguishing canonical lines (post-16.ts):
- `runHook('validation-not-compilation', …)` present in code block
- `const { runHook } = require('../lib/hook-runner');` present
- `Invoke /shannon:validate to verify through real interfaces.` present
- Old `BUILD_COMMANDS` regex array (12 entries) gone; replaced with single regex `BUILD_CMDS`.

Spot-check distinguishing lines (canonical-only, did not exist in published post pre-G7):
- `const { runHook } = require('../lib/hook-runner');`
- `BUILD_CMDS = /\b(npm run build|pnpm build|…)\b/i`
- `[shannon] validation-not-compilation: build succeeded, but compilation is NOT functional validation. Invoke /shannon:validate …`
- `runHook('block-fab-files', (payload) => { … return { decision: 'block', exitCode: 2, stderrPayload: \`[shannon] block-fab-files: "${filePath}" matches fabricated-artifact pattern …\` }; });`

All four match canonical at byte level.

---

## 5. Before/after excerpts

### validation-not-compilation.js (post.md, lead lines)

Before:
```
// .claude/hooks/validation-not-compilation.js
// PostToolUse — fires after every Bash command
const BUILD_COMMANDS = [
  /npm run build/, /pnpm build/, /yarn build/,
  …  (12 entries)
];
export default function validationNotCompilation({ tool, input, output }) { … }
```

After (matches canonical byte-for-byte):
```
#!/usr/bin/env node
// PostToolUse Bash — reminder when build commands succeed.
const { runHook } = require('../lib/hook-runner');
const BUILD_CMDS = /\b(npm run build|pnpm build|yarn build|cargo build|go build|make build|xcodebuild|gradle build|mvn package|tsc)\b/i;
…
runHook('validation-not-compilation', (payload) => { …
  stderrPayload: '[shannon] validation-not-compilation: build succeeded, but compilation is NOT functional validation. Invoke /shannon:validate to verify through real interfaces.\n',
});
```

### block-test-files.js → block-fab-files.js (post.md)

Before:
```
### block-test-files.js — The Hard Stop
const TEST_PATTERNS = [ /\/__tests__\//, /\.test\.[jt]sx?$/, … ];
const ALLOWED_EXCEPTIONS = [/playwright/i, /e2e/i];
export default function blockTestFiles({ tool, input }) { … }
```

After (matches canonical byte-for-byte):
```
### block-fab-files.js — The Hard Stop
#!/usr/bin/env node
// PreToolUse Write|Edit|MultiEdit — block fabricated-artifact filenames.
const { runHook } = require('../lib/hook-runner');
const FAB_PATTERNS = [ /\.test\.[a-z]+$/i, /\.spec\.[a-z]+$/i, /__mocks__\//, … ];
const EXEMPTIONS = [ /\/e2e-evidence\//, /\/evidence\//, /\.claude-plugin\//, /\/scripts\//, /\/tools\//, /\bSKILL\.md$/, … ];
const ACTIVE_SCOPE = [ /\/src\//, /\/lib\//, /\/app\//, /^src\//, /^lib\//, /^app\// ];
runHook('block-fab-files', (payload) => { … });
```

---

## 6. Evidence files (cited)

- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/g7-amend-post-md.diff` (241 lines)
- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/g7-amend-post16-ts.diff` (235 lines)
- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/g7-amend-summary.md` (this file)

Cross-references:
- `/Users/nick/Desktop/blog-series/plans/260524-0000-shannon-v6-stabilize-and-release/evidence/vg7.0-contract-verdict.md` (the verdict that motivated this gate)
- `/Users/nick/Desktop/shannon-framework/hooks/validation-not-compilation.js` (canonical source of truth)
- `/Users/nick/Desktop/shannon-framework/hooks/block-fab-files.js` (canonical source of truth)

---

## 7. Risks / notes

1. **Submodule diff:** `site/src/lib/post-bodies/post-16.ts` is inside the `site/` git submodule. `git diff` from the top-level repo returns nothing for that path — the diff was captured via `git -C site diff src/lib/post-bodies/post-16.ts`. The submodule path will need to be committed inside the submodule, then the parent's submodule pointer bumped, in a separate gate (NOT this gate's scope per the protocol: "DO NOT commit, push, or invoke git mutations beyond `git diff`").
2. **Typed body precedence:** Project memory `feedback_typed_block_overrides_postmd.md` confirms `post-16.ts` is what actually renders on `withagents.dev/posts/post-16-claude-code-plugins`. Both files were updated — the live render will reflect the canonical source the moment the submodule pointer + build ship.
3. **Visual / build / lint:** Not run (per protocol — next gate's responsibility). However, the `\\` escaping inside the TypeScript template literal follows the exact pattern used by the surrounding code blocks in post-16.ts, so the file should remain TS-valid.
4. **Orphan tree:** `/Users/nick/Desktop/blog-series/shannon-framework/` (the orphan VG-7.0 flagged) is now safe to delete — its `block-test-files.js` is no longer the sole on-disk satisfier of the published post. A follow-up gate can archive `.git` per the canonical-topology archive zone and remove the orphan tree.
5. **Frontmatter integrity:** Lines 1–33 of post.md unchanged. `series_total: '33'` preserved. `github_repo`, `slug`, `date`, `published`, `scheduled_for` all unchanged. ✓

---

## Status

**DONE** — post-16 markdown source and typed body now mirror canonical shannon-framework v6. Two `block-test-files` strings remain in the post (one per file), both in deliberate rename-explanation prose. All code blocks and all functional references resolve to `block-fab-files.js` and the `runHook()`-style `validation-not-compilation.js` in the canonical repo at `https://github.com/krzemienski/shannon-framework`.
