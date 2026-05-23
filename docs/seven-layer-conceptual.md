# Shannon v6 — Seven-Layer Conceptual Overlay

**Status:** Doc overlay describing how post-07's 7 conceptual control surfaces map to Shannon's 4 enforcement layer modules.
**Sources:**
- Post-07 "The Hook Control Plane" — `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/post.md`
- Architecture spec §4 — `spec/SHANNON-V6-ARCHITECTURE.md:122-135`
- Live layer modules — `core/layers/{context,hook,invocation,dispatch}/`

The 4 enforcement layers (`ContextLayer`, `HookLayer`, `InvocationLayer`, `DispatchLayer`) are the RUNTIME realization. The 7 conceptual layers below are the CONTROL SURFACES users (and Shannon authors) think about. This doc is the mapping that keeps both vocabularies consistent.

---

## Mapping Table

| Conceptual layer (post-07) | Concept | Realized by Shannon module | Mechanism | Cite (post:line) |
|---|---|---|---|---|
| 1. Global CLAUDE.md | User-level invariants (e.g. `~/.claude/CLAUDE.md`) loaded at every SessionStart | `core/layers/context/` (ContextLayer) | SessionStart hook reads global CLAUDE.md; injects into system prompt scope | post.md:42-58 |
| 2. Project CLAUDE.md | Repo-specific rules (e.g. `<repo>/CLAUDE.md`) layered on top of global | `core/layers/context/` (ContextLayer) | Same SessionStart pass — reads project CLAUDE.md after global, merges. Order matters for last-win semantics | post.md:60-82 |
| 3. `.claude/rules/*.md` | Modular rule fragments composed at runtime (no monolithic CLAUDE.md) | `core/layers/context/` (ContextLayer) | SessionStart walks `.claude/rules/` glob; concatenates fragments by frontmatter-declared activation conditions | post.md:84-112 |
| 4. Hooks | Tool-boundary enforcement (PreToolUse / PostToolUse / SessionStart / Stop) | `core/layers/hook/` (HookLayer) | `hooks/hooks.json` registers 14 scripts; `lib/hook-runner.js` is shared entry-point; each layer module wires the relevant subset | post.md:114-152 |
| 5. Skills (`.claude/skills/<name>/SKILL.md`) | Composable capability units; user/auto-invoked via slash or activation triggers | `core/layers/invocation/` (InvocationLayer) | InvocationLayer caches `skills/*/SKILL.md` frontmatter; matches `triggers` array against UserPromptSubmit content; surfaces hint to assistant | post.md:154-188 |
| 6. MCP servers | External tool surfaces (sequential-thinking, stitch, chrome-devtools, etc.) | `core/layers/dispatch/` (DispatchLayer) — for governance only | Shannon does NOT ship MCP servers (UQ-V2-2). DispatchLayer audits MCP tool calls via PostToolUse hook chain; emits to `hooks.jsonl`. MCP servers remain external dependencies | post.md:190-218 |
| 7. SessionStart | The boot event — assembles layers 1-6 into the current session | `core/layers/context/` + `lib/hook-runner.js` | SessionStart hook registered in `hooks/hooks.json` matches `startup\|resume\|clear\|compact`. ContextLayer runs first; downstream layers ready by Turn 1 | post.md:220-244 |

---

## How the 4 Enforcement Layers Compose the 7 Conceptual Layers

```
Conceptual                 →  Enforcement (Shannon module)
─────────────────────────────────────────────────────────────
1. Global CLAUDE.md        ┐
2. Project CLAUDE.md       ├→  ContextLayer (core/layers/context/)
3. .claude/rules/*.md      ┘
7. SessionStart            ─→  ContextLayer (boot orchestration)

4. Hooks                   ─→  HookLayer (core/layers/hook/)
                                + lib/hook-runner.js (shared dispatcher)

5. Skills                  ─→  InvocationLayer (core/layers/invocation/)

6. MCP servers             ─→  DispatchLayer (core/layers/dispatch/)
                                — for audit/governance only; Shannon does not ship MCPs
```

`ContextLayer` covers four conceptual layers (1, 2, 3, 7). `HookLayer` covers one (4). `InvocationLayer` covers one (5). `DispatchLayer` covers one (6).

The 4-vs-7 asymmetry is intentional: the 4 enforcement modules are runtime-grouped (what code dispatches what events); the 7 conceptual layers are author-grouped (what users edit to change behavior). Same surface area, different organization principles.

---

## Composition Rule at Runtime

Per `SHANNON-V6-ARCHITECTURE.md:131`:

> A SessionStart triggers ContextLayer only; a PostToolUse:Bash triggers HookLayer (validation-not-compilation) then InvocationLayer (validation-skill-tripwire); a Stop triggers DispatchLayer (stop-task-semantics) only.

Event-driven dispatch sequence at runtime:

```
SessionStart    → ContextLayer
UserPromptSubmit→ InvocationLayer (skill-activation-check)
PreToolUse      → HookLayer (block-fab-files, evidence-gate-reminder, ...)
PostToolUse     → HookLayer (validation-not-compilation, ...) → InvocationLayer (validation-skill-tripwire)
PreToolUse:Task → DispatchLayer (subagent-governance-inject)
Stop            → DispatchLayer (stop-task-semantics)
```

---

## Why This Document Exists

Post-07 popularized the 7-conceptual-layer model among Claude Code users. Shannon's 4-enforcement-layer model is internal-engineering vocabulary. Without this doc, users would read post-07 and not know which Shannon module realizes which conceptual layer.

This overlay is for users and Shannon authors who:
- Read post-07 and want to know where each layer lives in code
- Read Shannon's `core/layers/` and want to know which conceptual layer it covers
- Are debugging a missing behavior and need to know which module owns it

---

## Verification

The mapping above is checked by `scripts/_validate-seven-layer.js` (created in Phase 3 evidence):
- Verifies every conceptual layer (1-7) has a `Realized by` field naming a real module under `core/layers/`.
- Verifies every named module exists on disk.
- Verifies every cite (post:line) points at the actual post file.

Evidence: `e2e-evidence/phase-3-domains/seven-layer-overlay.txt`.

---

End of `docs/seven-layer-conceptual.md`.
