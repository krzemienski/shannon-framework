# Shannon Prior-Art Survey — Workstream D

**Auditor:** auditor-4-prior-art
**Team:** shannon-rebuild-260523
**Date:** 2026-05-23
**Default verdict:** Build Shannon from scratch. Use survey to validate design choices only.

## Method

Survey 9 systems across three classes:
1. **LLM-prompt composition** (LangChain, LlamaIndex, Haystack, DSPy)
2. **Build-system hooks** (Webpack tapable, Vite, esbuild)
3. **Plugin lifecycle / activation** (VSCode, oh-my-claudecode)

Per-system: what it does, transferable patterns, explicit reject reason.

---

## 1. LangChain (LCEL + CallbackHandler)

**What:** Python/JS framework for chaining LLM calls. LCEL composes Runnables with pipe operator (`prompt | llm | parser`). CallbackHandler exposes lifecycle events (on_llm_start, on_llm_new_token, on_llm_end, on_chain_start, on_chain_end, on_tool_start, on_agent_action).

**Transferable:**
- **Runnable interface uniformity** — every node implements `invoke`/`stream`/`batch`. Shannon prompt-stack layers should share one interface so layers compose orthogonally.
- **Callback event taxonomy** — pre/post pairs per node type. Maps cleanly to Shannon hook lanes (PreLayer, PostLayer, PreCompose, PostCompose).

**Reject reuse:**
- Wrong language (Python heavy; Shannon = TS/JS-first for CC integration).
- Wrong scope — LangChain owns LLM invocation; Shannon owns the *prompt assembly stack* before invocation.
- Heavy abstraction (LangSmith, LangGraph deps) violates KISS.
- WithAgent claims Shannon's value is layered *prompt assembly*, not chain orchestration.

Source: https://docs.langchain.com/oss/python/langchain/overview, https://python.langchain.com/api_reference/core/callbacks.html

---

## 2. LlamaIndex (IngestionPipeline + TransformComponent)

**What:** Pipeline chains `Transformation` nodes sequentially. Each transformation processes prior output. Built-in caching via (node, transform)-pair hash. Sync `run()` + async `arun()` + parallel `num_workers`.

**Transferable:**
- **Hash-based caching of (input, layer) pairs** — Shannon prompt-stack should cache by `(layer_id, input_hash)` so unchanged layers skip recompute. Big win for stable system-prompt layers.
- **Sequential transformation as composition default** — KISS-aligned; defer parallel/branched to v2.

**Reject reuse:**
- Wrong domain — ingestion pipeline for document indexing, not prompt assembly.
- Vector-store coupling is dead weight.
- Python.

Source: https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/

---

## 3. Haystack 2.x (Component + Pipeline)

**What:** `@component` decorator declares typed inputs/outputs. `Pipeline.add_component()` + `Pipeline.connect("producer.out", "consumer.in")` wires nodes. Type validation at connection time, not runtime. Supports branches, loops, async.

**Transferable:**
- **Explicit connection wiring** vs implicit pipe operator — Shannon could let layer authors declare typed `requires` / `provides` so the engine validates the stack at boot, not at first request.
- **Static validation at compose time** — fail-fast philosophy aligns with Shannon's evidence-gated ethos.

**Reject reuse:**
- Python.
- YAML serialization overkill for our use.
- Component model assumes data-flow DAG; Shannon is closer to a linear layered stack (intentionally simpler).

Source: https://docs.haystack.deepset.ai/docs/pipelines

---

## 4. DSPy (Signatures + Modules + Optimizers)

**What:** Decouples task spec (Signature) from reasoning strategy (Module: Predict / ChainOfThought / ReAct) from prompt-tuning (Optimizer). "Writing code instead of strings."

**Transferable:**
- **Signature/Module separation** is the strongest prior-art match for Shannon's WithAgent claim. A Shannon prompt-stack layer should declare a Signature (what it adds to the prompt: system rules / persona / examples / tool list) independent of strategy (static text / templated / fetched-from-skill).
- **Optimizer concept** — defer to v2, but Shannon should leave a seam for per-layer prompt tuning (A/B variants, eval-driven selection).

**Reject reuse:**
- Python.
- Optimizer requires training data / metrics infra Shannon doesn't have.
- DSPy is invocation-oriented (it owns the LM call); Shannon stops at prompt assembly.

Source: https://dspy.ai/learn/programming/overview/

---

## 5. Webpack tapable (Hook taxonomy)

**What:** Pure hook library. 5 core types: `SyncHook` (fire-and-forget), `SyncBailHook` (early-exit on first non-undefined), `SyncWaterfallHook` (value threaded through), `AsyncSeriesHook` (sequential await), `AsyncParallelHook` (concurrent).

**Transferable:**
- **Hook-type taxonomy** is gold. Shannon hook system should adopt all 5 semantics. Examples:
  - `PreCompose` = SyncHook (notify)
  - `LayerVeto` = SyncBailHook (any layer returns "skip" → stop)
  - `TransformPrompt` = SyncWaterfallHook (each layer mutates accumulated prompt)
  - `AsyncFetch` = AsyncSeriesHook (fetch external context in order)
  - `AsyncParallelFetch` = AsyncParallelHook (independent context fetches)
- **Tap registration model** (`hook.tap(name, fn)`) — Shannon plugins register against named hooks; engine doesn't know plugin internals.

**Reject reuse:**
- Tapable itself? Could literally `npm install tapable`. Worth considering. But:
  - 4MB dep + Webpack DNA pulls reviewer attention to "Shannon = Webpack-y" framing, undermining "own framework" WithAgent narrative.
  - Tapable's API is stable but verbose; Shannon can ship 200 LOC of equivalent in TS with cleaner ergonomics matching CC hook events.
- **DECISION: borrow the 5-type taxonomy + tap semantics, reimplement in ~200 LOC TS.**

Source: https://github.com/webpack/tapable

---

## 6. Vite Plugin API (Rollup-compat + Vite-specific hooks)

**What:** Plugin = object with named hook functions. Two tiers:
- **Universal (Rollup-compat):** `resolveId`, `load`, `transform`, `buildStart`, `buildEnd`, `closeBundle`
- **Vite-specific:** `config` (mutate before resolve), `configResolved` (read after resolve), `configureServer`, `transformIndexHtml`, `handleHotUpdate`

Hook order is fixed: `config` → `configResolved` → universal hooks.

**Transferable:**
- **Two-phase lifecycle** — config-mutation phase vs runtime phase. Shannon should split:
  - **Boot phase:** layers declare/modify stack composition (analog: `config`)
  - **Compose phase:** layers contribute prompt content (analog: `transform`)
  - **Finalize phase:** read-only post-compose hook for logging / instrumentation (analog: `closeBundle`)
- **Plugin-as-object** (vs Plugin-as-class) — lower ceremony, easier authoring.

**Reject reuse:**
- Vite's hooks are bundler-shaped (resolveId, load); semantics don't map to prompt assembly.
- Rollup-compat baggage irrelevant to Shannon.

Source: https://vite.dev/guide/api-plugin.html

---

## 7. VSCode Extension API (Activation Events + Contributes)

**What:** Extensions lazy-load on declared activation events (`onLanguage:python`, `onCommand:myCmd`, `onView:viewId`, `workspaceContains:**/.file`, `onStartupFinished`, `*`). Extension exports `activate()` / `deactivate()`. Contributes points declare static UI/feature attachments (commands, menus, keybindings) without code execution.

**Transferable:**
- **Activation-event lazy loading** — Shannon plugins should not all initialize on startup. Declare activation conditions: `onPostType:tutorial`, `onSkillInvoked:planning`, `onProjectHasFile:.shannon`. Reduces cold-start cost.
- **Contributes vs activate split** — static manifest declares what plugin can do (visible to engine without running plugin code); runtime `activate()` only runs when needed. Shannon plugin manifest should similarly declare layers/hooks statically, defer code load until activated.
- **`onStartupFinished` deferred init** — Shannon should support a "warm-up-after-first-request" tier.

**Reject reuse:**
- VSCode's contribution points are UI-shaped (menus, themes, languages); irrelevant.
- Activation-event syntax is fine but full VSCode extension manifest is overkill — Shannon needs ~10 fields, not 100.

Source: https://code.visualstudio.com/api/references/activation-events

---

## 8. oh-my-claudecode (OMC) — on-machine

**What:** Claude Code plugin layer at `~/.claude/`. Three primitives:
- **Hooks** (`~/.claude/hooks/*.js|cjs|mjs`) — fire on CC lifecycle events (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart, SubagentStop, Stop, TeammateIdle, TaskCompleted). Inject `<system-reminder>` tags, block tools (exit 2 + stderr), or no-op (exit 0).
- **Skills** (`~/.claude/skills/<id>/SKILL.md`) — markdown-frontmatter capability modules. Invoked via `/oh-my-claudecode:<id>` or auto-activated by keyword. Compose with native tools.
- **Agents** — sub-task delegation with isolated context (`SendMessage`, `TaskUpdate`).

**Transferable:**
- **Hook lifecycle event taxonomy is the most relevant prior art on this entire machine.** Shannon must integrate at exactly these event boundaries — UserPromptSubmit, PreToolUse, SubagentStart. Don't invent new event names; align with CC's published hook protocol (`stderr+exit2` to block, `stdout+exit0` to inject context, JSON `hookSpecificOutput.permissionDecision` for ask).
- **Single-process plugin model** — OMC hooks are short-lived processes, no daemon. Shannon should match: no long-running daemon, hooks/plugins are pure functions invoked per event.
- **Skill manifest + body separation** — SKILL.md frontmatter (id, description, triggers) is the contributes manifest; body is the activate() payload. Shannon layer authoring should mirror.
- **`<system-reminder>` channel** for engine→model context injection — Shannon should use this same channel; don't invent a parallel one.

**Reject reuse (as Shannon's foundation):**
- OMC is a *user* of CC, not a *layer-author framework*. Shannon plugins will likely *ship as* OMC-compatible skills+hooks, but Shannon's layer engine is upstream of OMC's lifecycle.
- OMC ships ~50 skills + ~25 hooks; that scope conflates "framework" and "content." Shannon = framework only.
- OMC's hook scripts are loose `.js`/`.cjs` files; Shannon needs typed authoring API.

Source: on-machine inspection — `~/.claude/hooks/`, `~/.claude/skills/`, project CLAUDE.md OMC section.

---

## 9. esbuild Plugin API (onResolve / onLoad + filter + namespace)

**What:** Plugin = `{name, setup}`. Setup gets `build` object with `onResolve`, `onLoad`, `onStart`, `onEnd` registrars. Every callback **requires a regex filter** (perf: skip JS-call entirely on non-match). Namespace mechanism enables virtual modules. `pluginData` flows from onResolve → onLoad → next onResolve (cooperation without coordination).

**Transferable:**
- **Regex-filter-on-registration** — single biggest perf insight. Shannon hook taps must declare a fast pre-filter (`layerType: "persona"`, `postSlug: /^post-2[0-9]$/`) so the engine skips inactive taps without invoking them. Avoids 1000-tap iteration cost.
- **pluginData side-channel** — layers can pass opaque data to later layers without baking it into the prompt stream. Useful for telemetry, A/B tags, layer-specific metadata.
- **`build.resolve()` re-entry** — plugins can delegate back to the engine. Shannon should expose `engine.compose(subset)` to layers that want to assemble a sub-stack.

**Reject reuse:**
- esbuild is Go-runtime + RPC bridge; tied to bundling.
- Filter regex is the only borrow; reimplement in 5 LOC.

Source: https://esbuild.github.io/plugins/

---

## Synthesis Matrix

| System | Hook taxonomy | Composition model | Lazy activation | Caching | Manifest split |
|--------|---------------|-------------------|-----------------|---------|----------------|
| LangChain | Callback events | Pipe / Runnable | No | No | No |
| LlamaIndex | Sequential | Transformation chain | No | **(hash) ✓** | No |
| Haystack | Connection-typed | Explicit DAG | No | No | Partial |
| DSPy | Module signatures | Module chain | No | No | **(Signature) ✓** |
| Tapable | **5-type ✓** | Tap registration | No | No | No |
| Vite | Two-phase | Object hooks | Partial | No | Yes |
| VSCode | Activation events | Contributes manifest | **✓✓** | No | **✓✓** |
| OMC/CC | **CC native ✓✓** | Skill+Hook+Agent | Partial | No | **(frontmatter) ✓** |
| esbuild | Filter-gated | Namespace + pluginData | No (filter) | No | Partial |

---

## Recommendation

**Build Shannon from scratch.** Borrow patterns, reuse zero implementations.

### Borrow patterns

1. **Tapable's 5-type hook taxonomy** (SyncHook / SyncBailHook / SyncWaterfallHook / AsyncSeriesHook / AsyncParallelHook) — reimplement in ~200 LOC TS.
2. **esbuild's regex pre-filter on tap registration** — perf-critical for >50 plugins.
3. **VSCode's activation events + contributes/activate split** — lazy plugin load + static manifest declares capability without running code.
4. **OMC/CC's hook lifecycle event names** — align with `UserPromptSubmit`, `PreToolUse`, `SubagentStart`, `SubagentStop`, `Stop`. Don't reinvent.
5. **OMC's `<system-reminder>` injection channel** — single context-injection protocol; don't duplicate.
6. **DSPy's Signature concept** — Shannon layer declares typed `provides` (system / persona / examples / tools / rules / instructions / metadata) so the engine can validate the 7-layer stack composition at boot.
7. **Vite's two-phase lifecycle** — `boot` (mutate stack composition) vs `compose` (contribute prompt content) vs `finalize` (read-only post-compose telemetry).
8. **LlamaIndex's `(layer_id, input_hash)` cache key** — skip recompute for stable layers (system prompt rarely changes per-request).
9. **Haystack's static typed connection validation** — fail-fast at boot if a layer's `requires` is not produced by an upstream layer.

### Reject reuse of

- **LangChain / LangGraph / LangSmith** — wrong language, wrong scope, abstraction tax kills KISS.
- **LlamaIndex full pipeline** — vector-store coupling, ingestion-shaped.
- **Haystack core** — Python, YAML serialization, DAG model heavier than Shannon needs.
- **DSPy runtime** — Python, optimizer requires training infra Shannon lacks.
- **tapable npm dep** — borrow taxonomy, reimplement; avoid Webpack-DNA framing.
- **Vite plugin API** — bundler-shaped hooks (resolveId, load) don't map.
- **VSCode extension manifest** — 100+ fields when Shannon needs ~10.
- **OMC as framework** — OMC is a *user* of CC; Shannon sits upstream as the prompt-assembly engine that ships *as* OMC skills/hooks.
- **esbuild plugin runtime** — Go + RPC; only the regex-filter idea is transferable.

### Validation of WithAgent claims

Per Workstream A's mandate to validate post claims against design choices, the prior art **supports** the WithAgent positioning that Shannon is a layered prompt-stack engine distinct from chain frameworks (LangChain/LlamaIndex). No prior system surveyed unifies:
- 7-layer typed prompt stack (closest: DSPy Signatures, but DSPy owns LM invocation)
- CC-native hook lifecycle alignment (closest: OMC, but OMC is content not framework)
- Plugin manifest + activation events for prompt-layer contribution (closest: VSCode, but UI-shaped)

The gap is real. Build it.

---

## Unresolved Questions

1. **Should Shannon ship as an OMC plugin or as a standalone CC plugin?** Standalone preserves "own framework" framing per WithAgent claims; OMC-bundling reduces install friction. Needs Workstream A/B verdict on positioning vs reach.
2. **Adopt `tapable` npm dep, or reimplement 200 LOC?** Reimplement recommended above, but if Phase 6 timeline tight, npm dep is 1-day savings vs ~1 week reimpl. Defer to Phase 6 lead.
3. **Caching layer scope — in-memory only, or persistent to disk?** LlamaIndex offers both. Shannon v1: in-memory only (KISS); persistent cache deferred to v2.
4. **DSPy-style Signatures: enforce typed `provides`/`requires` strictly, or advisory?** Strict = Haystack-style fail-fast; advisory = lower author friction. Recommend strict in v1 (matches Shannon evidence-gated ethos).
5. **VSCode-style activation events — do we need >5 trigger types?** Survey suggests `onAlways`, `onPostType:X`, `onSkillInvoked:X`, `onProjectHasFile:X`, `onUserPromptMatches:/regex/` covers Shannon needs. Confirm in Workstream B (current repo audit).
