# WithAgent Shannon Claims — Verbatim Extraction

Auditor: auditor-1-withagent (team shannon-rebuild-260523, Workstream A)
Date: 2026-05-23
Mode: Verbatim claim extraction. No interpretation. Every claim cites source path:line.

Sources audited:
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/post.md`
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/visuals/seven-layer-stack.html`
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/post-blocks.ts`
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/frontmatter.json`
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/social/newsletter.md`
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/social/linkedin-article.md`
- `/Users/nick/Desktop/blog-series/posts/post-07-prompt-engineering-stack/social/linkedin.md`
- `/Users/nick/Desktop/blog-series/posts/post-16-claude-code-plugins/post.md`
- `/Users/nick/Desktop/blog-series/posts/post-16-claude-code-plugins/visuals/enforcement-pyramid.html`
- `/Users/nick/Desktop/blog-series/posts/post-16-claude-code-plugins/social/linkedin-article.md`
- `/Users/nick/Desktop/blog-series/posts/post-16-claude-code-plugins/social/linkedin.md`
- `/Users/nick/Desktop/blog-series/site/src/lib/post-bodies/post-07.ts`
- `/Users/nick/Desktop/blog-series/site/src/lib/post-bodies/post-16.ts`
- `/Users/nick/Desktop/blog-series/posts/post-06-parallel-worktrees/post.md` (Post-7 cross-ref only)
- `/Users/nick/Desktop/blog-series/posts/INDEX.md`

Repo name claimed (frontmatter):
- `github_repo: "https://github.com/krzemienski/shannon-framework"` — post-07/post.md:11; post-16/post.md:11
- Index assigns Posts 7 + 16 → `shannon-framework` — posts/INDEX.md:63, posts/INDEX.md:72, posts/INDEX.md:122

---

## Section 1 — Layer Roster (7 entries)

### 1.1 Post-07 canonical 7-layer roster (post.md)

Source: `posts/post-07-prompt-engineering-stack/post.md:77-89`

| # | Layer Name | Path / Locus | Responsibility (verbatim) |
|---|---|---|---|
| 1 | "Global Constitution" | `~/.claude/CLAUDE.md` | "Applies to every project on every machine. This is the constitution. Projects can add laws but can't override it. The non-negotiable mandates live here: functional validation only, no test files, no mocks, evidence-based completion claims." — post.md:77 |
| 2 | "Rules Directory" | `.claude/rules/*.md` | "A 50-line focused file gets more reliable attention than 50 lines buried in a 500-line document. I split governance into nine files: `coding-style.md`, `security.md`, `testing.md`, `git-workflow.md`, `performance.md`, `agents.md`, `patterns.md`, `hooks.md`, `development-workflow.md`. Each file covers one concern." — post.md:79 |
| 3 | "Hooks" | (Code on tool calls) | "Code that runs on every tool call. This is where rules become enforceable. PreToolUse hooks fire before a tool executes and can block the call entirely. PostToolUse hooks fire after and inject corrective reminders. The agent can't ignore a hook that returns `{ \"decision\": \"block\" }`." — post.md:81 |
| 4 | "Skills" | (Workflow files) | "Structured workflows with routing tables and gates. A skill like `functional-validation` is a step-by-step protocol that an agent invokes when it needs to prove something works. Skills carry project-specific context that the agent doesn't have by default. Across all sessions, 1,370 skill invocations kept agents on prescribed workflows instead of improvising." — post.md:83 |
| 5 | "Agents" | (Subagent profiles) | "Specialized roles with scoped instructions. A `code-reviewer` agent has a review checklist baked into its prompt. A `build-fixer` agent knows to check DerivedData and clean caches. Each agent carries domain knowledge that the main agent forgets under context pressure." — post.md:85 |
| 6 | "MCP Tools" | (External tools) | "External capabilities with built-in constraints. The sequential thinking tool (327 invocations across all sessions) forces structured reasoning before implementation. The Stitch MCP enforces design system compliance. These tools add discipline through their interface design, not through written rules." — post.md:87 |
| 7 | "Session Start Hooks" | (SessionStart event) | "Inject the full governance context from turn one. Before the agent has any competing context, it loads the rules, the project constitution, and the enforcement expectations. Sets the behavioral baseline before problem-solving begins." — post.md:89 |

### 1.2 Ordering claims

- Top-down list in prose enumerates Layer 1 → Layer 7 — post-07/post.md:77-89.
- Diagram lists Layer 7 → Layer 1 with arrows L7 → L6 → L5 → L4 → L3 → L2 → L1 — `posts/post-07-prompt-engineering-stack/visuals/seven-layer-stack.html:117-133`.
- Diagram caption: "Layer 1 (CLAUDE.md constitution) sets non-negotiables. Layers 2–3 add focused rule files and mechanical hook enforcement. Layers 4–5 embed rules in structured workflows and specialized agent roles. Layers 6–7 build constraints into tool interfaces and session-start injection — all before competing context accumulates." — visuals/seven-layer-stack.html:104.
- Linkedin article repeats Layer 1→7 prose ordering — `posts/post-07-prompt-engineering-stack/social/linkedin-article.md:75-81`.
- Newsletter bullets list Layer 1→7 — `posts/post-07-prompt-engineering-stack/social/linkedin.md:9-15`.

### 1.3 Defense-in-depth composition rule

"The principle is defense in depth. If the agent forgets the build command (Layer 1 failure), the auto-build hook catches it (Layer 3). If the hook misses it, the evidence gate blocks premature completion claims (Layer 4). No single layer is sufficient. All seven together produce results that no single layer achieves alone." — post-07/post.md:91.

Restated as Shannon principle:
"The 7-layer stack is an error-correcting code for agent behavior. Layer 1 states the rule. Layer 2 provides detail. Layer 3 enforces it mechanically. Layer 4 embeds it in workflows. Layer 5 scopes it to specialized roles. Layer 6 builds it into tool interfaces. Layer 7 loads it before noise accumulates." — post-07/post.md:335.

### 1.4 Post-16 alternate roster (4-layer Shannon Framework "Enforcement Pyramid")

Source: `posts/post-16-claude-code-plugins/post.md:174-189` AND `posts/post-16-claude-code-plugins/visuals/enforcement-pyramid.html:122-155`.

| # | Layer Name (post.md) | Compliance claim | Notes (verbatim) |
|---|---|---|---|
| 1 | "CLAUDE.md" | "Compliance: ~60%" | "tells the agent what to do. Agents forget." — post-16/post.md:184 |
| 2 | "Hooks" | "near 100%" on targeted behaviors | "enforce rules automatically. Can't handle nuanced workflows." — post-16/post.md:185 |
| 3 | "Skills" | (no number) | "provide structured workflows with context the agent lacks. They require invocation, and agents skip them under pressure. The `skill-activation-check.js` hook closes this gap." — post-16/post.md:186 |
| 4 | "Commands" | (no number) | "give users direct control — the final safety net." — post-16/post.md:187 |

Combined claim: "Combined 4-layer compliance: 95%+. The remaining 5% is why you still review the output." — post-16/post.md:189.

Enforcement-pyramid diagram source (Mermaid):
```
subgraph L4["Layer 4 · Commands"]    /autopilot  /ralph  /team
subgraph L3["Layer 3 · Skills"]      functional-validation, gate-validation-discipline, e2e-validate
subgraph L2["Layer 2 · Hooks"]       block-test-files.js, read-before-edit.js, validation-not-compilation.js, evidence-gate-reminder.js
subgraph L1["Layer 1 · CLAUDE.md"]   No mocks mandate, Functional validation protocol, Read-before-write rule
```
Source: `posts/post-16-claude-code-plugins/visuals/enforcement-pyramid.html:122-154`.

Diagram edge labels: C1→S1, C2→S2, C3→S3 (commands→skills); S1→M1, S2→M2, S3→M3 (skills→CLAUDE.md mandates); H1 -.->|enforces| M1, H2 -.->|enforces| M3, H3 -.->|enforces| M2, H4 -.->|enforces| M2 (hooks dotted-enforce CLAUDE.md mandates) — enforcement-pyramid.html:145-154.

LinkedIn-article (post-16) restates 4-layer model — `posts/post-16-claude-code-plugins/social/linkedin-article.md:111-116`.
Site typed body confirms 4-layer wa node graph with sysId `post-16-shannon-stack`, compliance node "95%+" — `site/src/lib/post-bodies/post-16.ts:142-163`.

### 1.5 4-layer Shannon redundancy summary (post-16)

"Redundant encoding means saying the same thing four ways, at four enforcement points:
1. The CLAUDE.md rule says 'no test files.'
2. The `block-test-files.js` hook blocks test file creation at the tool boundary.
3. The `functional-validation` skill provides an alternative workflow.
4. The `/autopilot` command orchestrates the entire flow including validation." — post-16/post.md:400-407.

### 1.6 Roster contradiction note

- Post-07 names **7 layers**; post-16 names **4 layers**, both as "the Shannon Framework." Both posts share the same `github_repo: shannon-framework`. The 4-layer post-16 model = {CLAUDE.md, Hooks, Skills, Commands}. Post-07's full 7-layer set = {CLAUDE.md global, .claude/rules/, Hooks, Skills, Agents, MCP Tools, SessionStart Hooks}. Commands appear ONLY in post-16; Agents, MCP, SessionStart, and rules/ split appear ONLY in post-07.

### 1.7 Inputs / outputs / composition rules

No explicit input/output schema for any layer in either post — claims are prose-level. Closest formal interface = hook stdin/stdout contract (Section 2.5 below).

---

## Section 2 — Hook Claims

### 2.1 Hook event types

Source: post-07/post.md:97-101, post-16/post.md:163-168.

- **PreToolUse**: "fire before the tool executes. They inspect the tool name and inputs, then return `allow`, `block`, or inject a warning message." — post-07/post.md:99.
  - post-16 restates: "fires before the tool executes. It can block (write to stderr, exit code 2), warn (inject context and allow), or silently allow (exit 0 with no output)." — post-16/post.md:165.
- **PostToolUse**: "fire after the tool executes. They inspect the output and inject reminders or corrective context." — post-07/post.md:100.
  - post-16 restates: "fires after execution completes. It can inject reminders based on output by writing to stderr and exiting with code 2. It can't block the action already taken, but it shapes what the agent does next." — post-16/post.md:166.
- **UserPromptSubmit**: "fires on every user message, before the agent starts reasoning. It can inject workflow requirements or force skill evaluation." — post-16/post.md:167.

### 2.2 Hook return contract (post-07 prose)

"The agent can't ignore a hook that returns `{ \"decision\": \"block\" }`." — post-07/post.md:81.

`block-test-files.js` return signatures shown (post-07/post.md:130-152):
- Wrong-tool path: `return { decision: "allow" };` (lines 131-133)
- Exception match: `return { decision: "allow" };` (lines 136-138)
- Block match: `return { decision: "block", message: \`BLOCKED: Cannot create test file: ${filePath}\\nThis project uses functional validation, not unit tests.\` };` (lines 140-148)
- Default: `return { decision: "allow" };` (line 150)

`read-before-edit.js` return signatures (post-07/post.md:168-188):
- Read tracking: tracks `readFiles.add(input.file_path)` — line 171
- Non-edit tool: `return { decision: "allow" };` — lines 173-175
- Unread file: `return { decision: "allow", message: \`WARNING: Editing ${filePath} without reading it first.\` };` — lines 180-184
- Default: `return { decision: "allow" };` — line 186

### 2.3 Hook return contract (post-16 stdin/stdout)

`validation-not-compilation.js` actual implementation (post-16/post.md:85-123):
- Signature: `export default function validationNotCompilation({ tool, input, output })` — line 85
- Tool filter: `if (tool !== "Bash") return;` — line 87
- Reads `input?.command`, `output?.stdout`, `output?.exit_code` — lines 89-91
- Success rule: `exitCode === 0 && SUCCESS_INDICATORS.some(...)` — lines 98-100
- Output mechanism: `process.stderr.write([ "BUILD SUCCESS IS NOT FUNCTIONAL VALIDATION.", ...].join("\n"));` then `process.exit(2);` — lines 106-122

`block-test-files.js` post-16 implementation (post-16/post.md:219-244):
- Signature: `export default function blockTestFiles({ tool, input })` — line 219
- Tool filter: `if (!["Write", "Edit", "MultiEdit"].includes(tool)) return;` — line 220
- Exception loop, then pattern loop — lines 225-243
- Block mechanism: `process.stderr.write([...].join("\n"));` then `process.exit(2);` — lines 231-242

`evidence-gate-reminder.js` post-16 implementation (post-16/post.md:260-275):
- Signature: `export default function evidenceGateReminder({ tool, input })` — line 260
- Tool filter: `if (tool !== "TaskUpdate") return;` — line 261
- Status filter: `if (!["completed", "complete", "done"].includes(status)) return;` — line 263
- Mechanism: `process.stderr.write(...); process.exit(2);` — lines 265-274

Three-response API (post-16/post.md:317-332):
```javascript
// Block — prevent the tool call entirely (PreToolUse only)
// Write reason to stderr, exit code 2
process.stderr.write("Explanation for the agent.");
process.exit(2);

// Inject context — tool proceeds, agent sees the message
// Write to stderr, exit code 2 (PostToolUse and UserPromptSubmit)
process.stderr.write("Reminder or warning text.");
process.exit(2);

// Silent allow — exit with no output, tool proceeds normally
process.exit(0);
```

Contract claim: "That's the entire API. No registration, no manifest parsing, no framework overhead." — post-16/post.md:334.

### 2.4 Contract divergence

- post-07's hook implementations RETURN `{ decision, message }` objects from a default-export function (`{ tool, input }` arg) — post-07/post.md:130-152, 168-188.
- post-16's hook implementations WRITE to `process.stderr` and call `process.exit(2|0)` from a default-export function — post-16/post.md:85-123, 219-244, 260-275, 317-332.
- Both styles claimed for the SAME framework named `shannon-framework`. Both call themselves "the hook contract."

### 2.5 Hook stdin/stdout payload schema (post-16)

"Claude Code spawns the hook script as a child process, writes JSON to its stdin, and reads from its stderr." — post-16/post.md:288.

**PreToolUse hooks receive** (post-16/post.md:291-298):
```json
{
  "tool": "Write",
  "input": {
    "file_path": "/path/to/file.test.ts",
    "content": "..."
  }
}
```

**PostToolUse hooks receive the same, plus output** (post-16/post.md:301-307):
```json
{
  "tool": "Bash",
  "input": { "command": "npm run build" },
  "output": { "stdout": "Build succeeded", "exit_code": 0 }
}
```

**UserPromptSubmit hooks receive** (post-16/post.md:310-314):
```json
{
  "prompt": "Build a login page with email validation"
}
```

### 2.6 Hook integration (settings.json)

Source: post-16/post.md:128-144.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node .claude/hooks/validation-not-compilation.js"
          }
        ]
      }
    ]
  }
}
```

"Drop the file in `.claude/hooks/`, add the entry to `.claude/settings.json`, and the hook fires on every Bash call for every session." — post-16/post.md:146.

### 2.7 The 5 surviving hooks

Both posts converge on the same 5-hook loadout:

| # | Hook | Event | Tool matcher | Violation rate claim | Source |
|---|---|---|---|---|---|
| 1 | `block-test-files.js` | PreToolUse | Write/Edit/MultiEdit | "23% to 0" | post-07/post.md:164; post-16/post.md:199 |
| 2 | `read-before-edit.js` | PreToolUse | Edit (+MultiEdit) | "31% to 4%" (post-07); Read-to-Edit "~2:1 → 4.4:1" (post-16) | post-07/post.md:166; post-16/post.md:251-254 |
| 3 | `validation-not-compilation.js` | PostToolUse | Bash | "41% to 9%" | post-07/post.md:190; post-16/post.md:69-124 |
| 4 | `evidence-gate-reminder.js` | TaskUpdate (post-07 calls this PostToolUse-on-TaskUpdate; post-16 same) | TaskUpdate | "Task completion quality improved 34%" | post-07/post.md:192; post-16/post.md:256-278 |
| 5 | `skill-activation-check.js` | UserPromptSubmit | (every user msg matching implementation intent) | "drives the 1,370 skill invocations" | post-07/post.md:204; post-16/post.md:280-283 |

### 2.8 The 18 dead hooks

Source: post-07/post.md:206-214.

Named dead hooks: `max-file-size`, `no-console-log`, `import-order`, `commit-message-reviewer`, `type-annotation-enforcer`, `function-length`, `single-responsibility`, `dry-violation-detector`, "and ten more" — post-07/post.md:208.

Survivability rule: "if the violation can be objectively detected from the tool input alone, a hook works." — post-07/post.md:210.

Meta-rule: "hooks should enforce safety invariants, not style preferences." — post-07/post.md:214.

### 2.9 Severity model

Source: post-07/post.md:239-249.

- **Block**: "stops the tool call. The agent can't proceed until it takes a different approach. Used for: test file creation, API key commits, writes to reference data files. Zero tolerance." — line 243.
- **Warn**: "injects a warning but allows the tool call to proceed. Used for: editing unread files, large file modifications, missing build verification." — line 245.
- **Remind**: "injects a contextual reminder after the fact. Used for: dev server restarts after config changes, documentation updates after API changes, the 'compilation isn't validation' reminder." — line 247.

Three-level scored "95% compliance". 2-level scored 87%. 5-level scored 88%. — post-07/post.md:249.

### 2.10 Failure-mode catalog (post-16)

Source: post-16/post.md:340-350.

- "Matcher mistakes" — `Write` does not match Edit/MultiEdit; use `Write|Edit|MultiEdit` — line 342.
- "Silent crashes" — unhandled exception = silent allow; wrap in try/catch with `process.exit(0)` fallback — line 344.
- "Performance traps" — <100ms, synchronous, no network — line 346.
- "Hook that cried wolf" — too many warnings = ignored — line 348.
- "State management gotchas" — `read-before-edit.js` uses module-level `Set`, loaded once per session, lost on session restart — line 350.

### 2.11 Subagent inheritance hook (post-07)

"a PreToolUse hook on the Agent tool that automatically injects core rules into every subagent prompt" — post-07/post.md:257. "When the main agent spawns a `code-reviewer`, the hook appends the functional validation mandate, the no-test-files rule, and the evidence-gate checklist to the subagent's instructions." — post-07/post.md:257.

---

## Section 3 — Plugin / Framework Contract Claims

### 3.1 Plugin system extension points (post-16)

"Claude Code's plugin system has four extension points: hooks that fire on tool events, skills that provide domain workflows, agents that define specialist roles, and MCP servers that add tool capabilities." — post-16/post.md:52.

### 3.2 Shannon Framework deliverable count (post-16 closing)

"The [Shannon Framework](https://github.com/krzemienski/shannon-framework) is a reference Claude Code plugin with 5 hooks, 1 skill, and 1 agent template." — post-16/post.md:417.

LinkedIn-article (post-16) restates loadout: "the 5-hook loadout, the 4-layer enforcement pyramid, and the stdin/stdout contract." — `posts/post-16-claude-code-plugins/social/linkedin-article.md:134`.

Cover-image caption (post-16 linkedin-article): "The Shannon plugin loadout: 5 commands, 5 skills, 5 hooks, 4 agents — each row carries a green PASS chip." — `posts/post-16-claude-code-plugins/social/linkedin-article.md:27`. **Note: this number disagrees with the in-body "5 hooks, 1 skill, 1 agent template" — see §6.4.**

### 3.3 Install / install layout (post-07)

```bash
# Copy hooks into your Claude Code project
cp -r hooks/ .claude/hooks/

# Copy skills
cp -r skills/ .claude/skills/

# Copy agents
cp -r agents/ .claude/agents/
```
Source: post-07/post.md:310-318.

Implies repo directory layout: `hooks/`, `skills/`, `agents/` at repo root → mirror into `.claude/{hooks,skills,agents}/`.

### 3.4 Lifecycle phases

No "lifecycle phases" enum is named explicitly. Inferred from hook lifecycle prose (post-16/post.md:156-168) and post-07/post.md:97-101:

| Phase | When | Mechanism |
|---|---|---|
| SessionStart (Layer 7) | "from turn one" | "Inject the full governance context" — post-07/post.md:89 |
| UserPromptSubmit | "on every user message, before the agent starts reasoning" | "inject workflow requirements or force skill evaluation" — post-16/post.md:167 |
| PreToolUse | "before the tool executes" | block / inject warning + allow / silent allow — post-07/post.md:99, post-16/post.md:165 |
| Tool execution | (Claude Code internal) | n/a |
| PostToolUse | "after the tool executes" | inject reminders/corrective context — post-07/post.md:100, post-16/post.md:166 |

### 3.5 Plugin discovery / settings

`.claude/settings.json` `hooks` block with `PostToolUse` array of `{ matcher, hooks: [{ type: "command", command }] }` — post-16/post.md:129-144. No mention of `PreToolUse` example block, no mention of plugin manifest, no mention of plugin marketplace.

### 3.6 No registration claim

"That's the entire API. No registration, no manifest parsing, no framework overhead." — post-16/post.md:334.

### 3.7 Decision framework — hooks vs MCP vs CLAUDE.md vs skills

Source: post-16/post.md:386-392.

- **CLAUDE.md** — "general guidance that doesn't need enforcement. Style preferences, architectural conventions, project context. If 60-70% compliance is enough, CLAUDE.md works." — line 386.
- **Hook** — "when you need to intercept an existing tool call. Block certain Writes, inject warnings after Bash, remind on Edit. Hooks modify existing behavior automatically." — line 388.
- **MCP server** — "when you need to give the agent a capability it doesn't have. Query a database, search an AST, interact with an LSP server, manage persistent state. MCP servers add new tools." — line 390.
- **Skill** — "for structured, multi-step workflows that carry domain context. Validation protocols, review checklists, deployment procedures. Skills are invocable — pair them with a UserPromptSubmit hook to make sure the agent loads them." — line 392.

---

## Section 4 — Code Snippets (Verbatim, Compatibility-Test Class)

These are reproduced verbatim. The actual `shannon-framework` repo MUST contain equivalent files or the posts misrepresent the framework. Lines cite source post location.

### 4.1 `block-test-files.js` (post-07 version)

Source: `posts/post-07-prompt-engineering-stack/post.md:111-152`.

```javascript
const TEST_PATTERNS = [
  /\/__tests__\//,
  /\.test\.[jt]sx?$/,
  /\.spec\.[jt]sx?$/,
  /\.mock\.[jt]sx?$/,
  /test_.*\.py$/,
  /.*_test\.py$/,
  /.*_test\.go$/,
  /Tests?\.swift$/,
  /mock[_-]/i,
  /stub[_-]/i,
];

const ALLOWED_EXCEPTIONS = [
  /playwright/i, // Functional validation, not unit testing
  /e2e/i,
];

export default function blockTestFiles({ tool, input }) {
  if (!["Write", "Edit", "MultiEdit"].includes(tool)) {
    return { decision: "allow" };
  }

  const filePath = input.file_path || input.filePath || "";
  for (const exception of ALLOWED_EXCEPTIONS) {
    if (exception.test(filePath)) return { decision: "allow" };
  }

  for (const pattern of TEST_PATTERNS) {
    if (pattern.test(filePath)) {
      return {
        decision: "block",
        message: `BLOCKED: Cannot create test file: ${filePath}\n` +
          "This project uses functional validation, not unit tests.",
      };
    }
  }

  return { decision: "allow" };
}
```

### 4.2 `block-test-files.js` (post-16 version — 12 patterns, stderr+exit2 contract)

Source: `posts/post-16-claude-code-plugins/post.md:202-244`.

```javascript
const TEST_PATTERNS = [
  /\/__tests__\//,
  /\.test\.[jt]sx?$/,
  /\.spec\.[jt]sx?$/,
  /\.mock\.[jt]sx?$/,
  /test_.*\.py$/,
  /.*_test\.py$/,
  /.*_test\.go$/,
  /Tests?\.swift$/,
  /mock[_-]/i,
  /stub[_-]/i,
  /fake[_-]/i,
  /fixture[_-]/i,
];

const ALLOWED_EXCEPTIONS = [/playwright/i, /e2e/i];

export default function blockTestFiles({ tool, input }) {
  if (!["Write", "Edit", "MultiEdit"].includes(tool)) return;

  const filePath = input.file_path || input.filePath || "";
  if (!filePath) return;

  for (const exception of ALLOWED_EXCEPTIONS) {
    if (exception.test(filePath)) return;
  }

  for (const pattern of TEST_PATTERNS) {
    if (pattern.test(filePath)) {
      process.stderr.write([
        `BLOCKED: Cannot create test file: ${filePath}`,
        "",
        "This project uses functional validation, not unit tests.",
        "Instead of writing tests:",
        "  1. Build the real system",
        "  2. Run it in the simulator/browser/CLI",
        "  3. Exercise the feature through the actual UI",
        "  4. Capture screenshots/logs as evidence",
      ].join("\n"));
      process.exit(2);
    }
  }
}
```

Note: pattern count = **10** in post-07 (4.1), **12** in post-16 (4.2). Post-16 prose claims "12 regex patterns" and "Checks the file path against 12 test patterns" — post-16/post.md:46, 199. Post-07 prose claims "12 test file patterns" — post-07/post.md:164. The post-07 code block lists 10. The post-16 code block lists 12.

### 4.3 `read-before-edit.js` (post-07)

Source: `posts/post-07-prompt-engineering-stack/post.md:168-188`.

```javascript
export default function readBeforeEdit({ tool, input, history }) {
  if (tool === "Read" && input.file_path) {
    readFiles.add(input.file_path);
    return { decision: "allow" };
  }

  if (!["Edit", "MultiEdit"].includes(tool)) {
    return { decision: "allow" };
  }

  const filePath = input.file_path || input.filePath || "";
  if (!readFiles.has(filePath)) {
    return {
      decision: "allow",
      message: `WARNING: Editing ${filePath} without reading it first.`,
    };
  }
  return { decision: "allow" };
}
```

Note: `readFiles` referenced but not declared inside the snippet. Post-16 prose says "tracks state in a module-level Set" — post-16/post.md:350. Means `const readFiles = new Set()` at module top — claim implicit.

### 4.4 `validation-not-compilation.js` (post-16, full implementation)

Source: `posts/post-16-claude-code-plugins/post.md:69-123`.

```javascript
// .claude/hooks/validation-not-compilation.js
// PostToolUse — fires after every Bash command
// Purpose: catch agents declaring victory after a build instead of validating behavior

const BUILD_COMMANDS = [
  /npm run build/, /pnpm build/, /yarn build/,
  /cargo build/, /swift build/, /xcodebuild/,
  /go build/, /\bmake\b/, /gradle build/,
  /mvn (compile|package)/, /\btsc\b/, /vite build/,
];

const SUCCESS_INDICATORS = [
  /build succeeded/i, /compiled successfully/i,
  /build complete/i, /\b0 error/i, /✓|✔|success/i,
];

export default function validationNotCompilation({ tool, input, output }) {
  // Only fire on Bash tool calls
  if (tool !== "Bash") return;

  const command = input?.command ?? "";
  const stdout = output?.stdout ?? "";
  const exitCode = output?.exit_code ?? 1;

  // Check if this was a build command
  const isBuildCommand = BUILD_COMMANDS.some((pattern) => pattern.test(command));
  if (!isBuildCommand) return;

  // Check if the build succeeded
  const buildSucceeded =
    exitCode === 0 &&
    SUCCESS_INDICATORS.some((pattern) => pattern.test(stdout));

  if (!buildSucceeded) return;

  // Build succeeded — inject the reminder
  // Return a message; exit code 2 injects it into the agent's context
  process.stderr.write([
    "",
    "BUILD SUCCESS IS NOT FUNCTIONAL VALIDATION.",
    "",
    "A passing build proves syntax and types. It does not prove behavior.",
    "Before marking this task complete:",
    "",
    "  1. Run the app (simulator, browser, or CLI — whichever applies)",
    "  2. Exercise the specific feature you just built",
    "  3. Confirm the user-facing behavior matches the requirement",
    "  4. Capture a screenshot or log as evidence",
    "",
    "If you cannot run the app right now, note that explicitly.",
    "Do not mark complete based on build output alone.",
    "",
  ].join("\n"));
  process.exit(2);
}
```

### 4.5 `evidence-gate-reminder.js` (post-16)

Source: `posts/post-16-claude-code-plugins/post.md:260-275`.

```javascript
export default function evidenceGateReminder({ tool, input }) {
  if (tool !== "TaskUpdate") return;
  const status = input.status || "";
  if (!["completed", "complete", "done"].includes(status)) return;

  process.stderr.write([
    "EVIDENCE GATE: Task marked complete. Before accepting, verify:",
    "",
    "  [ ] Did I READ the actual evidence file (not just the report)?",
    "  [ ] Did I VIEW the actual screenshot (not just confirm it exists)?",
    "  [ ] Did I EXAMINE the actual command output (not just exit code)?",
    "  [ ] Can I CITE specific evidence for each validation criterion?",
    "  [ ] Would a skeptical reviewer agree this is complete?",
  ].join("\n"));
  process.exit(2);
}
```

### 4.6 Evidence gate checklist (post-07 plain-text form)

Source: `posts/post-07-prompt-engineering-stack/post.md:194-200`.

```text
[ ] Did I READ the actual evidence file (not just the report)?
[ ] Did I VIEW the actual screenshot (not just confirm it exists)?
[ ] Did I EXAMINE the actual command output (not just the exit code)?
[ ] Can I CITE specific evidence for each validation criterion?
[ ] Would a skeptical reviewer agree this is complete?
```

### 4.7 `functional-validation` skill content (post-07 markdown)

Source: `posts/post-07-prompt-engineering-stack/post.md:271-289`.

```markdown
### Step 1: Build the Real System
Build from source. No placeholders, no stubs.

### Step 2: Run It
Start the app, service, or tool in its real environment.

### Step 3: Exercise Through UI
Interact through the actual interface — simulator, browser, CLI.

### Step 4: Capture Evidence
Screenshots, command output, log entries.

### Step 5: Apply Gate Validation
Before claiming complete:
- [ ] Did I READ the actual evidence?
- [ ] Can I CITE specific proof for each criterion?
- [ ] Would a skeptical reviewer agree?
```

### 4.8 `functional-validation` SKILL.md form (post-16)

Source: `posts/post-16-claude-code-plugins/post.md:358-374`.

```text
# functional-validation

> Validates features through real system behavior.

## Trigger Patterns
- "validate this"
- "functional validation"
- "prove it works"

## Execution Steps
1. Build the real system (no placeholders, no stubs)
2. Run it in its real environment
3. Exercise through the actual UI
4. Capture evidence (screenshots, logs, responses)
5. Apply gate validation (5-question checklist)
```

### 4.9 settings.json hook integration

Source: post-16/post.md:128-144 — see §2.6 for full block.

### 4.10 Install commands (post-07)

Source: post-07/post.md:310-318 — see §3.3.

---

## Section 5 — Architecture Diagram References

### 5.1 `posts/post-07-prompt-engineering-stack/visuals/seven-layer-stack.html`

What it shows (Mermaid `graph TB`):
- Subgraph titled "The 7-Layer Prompt Engineering Stack" — line 117.
- 7 nodes L7 → L1 with labels exactly matching Section 1.1 — lines 117-126.
- Directed edges L7→L6→L5→L4→L3→L2→L1 (top-down, Layer-7 to Layer-1 cascade) — lines 128-134.
- Caption emphasises Shannon redundancy principle and 150K-token context window — line 104.

### 5.2 `posts/post-16-claude-code-plugins/visuals/enforcement-pyramid.html`

What it shows (Mermaid `graph TB` with 4 subgraphs):
- L1 · CLAUDE.md → 3 nodes M1/M2/M3 = "No mocks mandate", "Functional validation protocol", "Read-before-write rule" — lines 140-144.
- L2 · Hooks → 4 nodes H1-H4 = `block-test-files.js`, `read-before-edit.js`, `validation-not-compilation.js`, `evidence-gate-reminder.js` — lines 134-139.
- L3 · Skills → 3 nodes S1-S3 = `functional-validation`, `gate-validation-discipline`, `e2e-validate` — lines 129-133.
- L4 · Commands → 3 nodes C1-C3 = `/autopilot`, `/ralph`, `/team` — lines 124-128.
- Edges (lines 145-154):
  - C1 → S1 (commands route to skills)
  - C2 → S2
  - C3 → S3
  - S1 → M1, S2 → M2, S3 → M3 (skills implement mandates)
  - H1 -.->|enforces| M1 (block-test-files enforces No-mocks)
  - H2 -.->|enforces| M3 (read-before-edit enforces Read-before-write)
  - H3 -.->|enforces| M2 (validation-not-compilation enforces Functional-validation)
  - H4 -.->|enforces| M2 (evidence-gate-reminder enforces Functional-validation)
- Caption: "Each catches what the previous one misses; combined compliance hits 95%+." — line 163 in typed body; visual caption at enforcement-pyramid.html:101-105.

### 5.3 post-07 inline diagrams (post.md / post-blocks.ts)

- 3 inline SVGs referenced — `/svg/post-07-1.svg`, `/svg/post-07-2.svg`, `/svg/post-07-3.svg` — post-07/post.md:72, 104, 224.
- post-blocks.ts inlines actual SVG markup for:
  - Diagram 1 (post.md:72): Flow chart of 7 layers — post-07/post-blocks.ts:22.
  - Diagram 2 (post.md:104): Sequence diagram with actors Agent, PreToolUse Hooks, Tool Execution, PostToolUse Hooks, Agent Context. Alt branches: "Block Decision" → "decision block — tool call prevented"; "Warn Decision" → "decision allow + warning message" + "Warning injected into context"; "Allow Decision" → "decision allow". — post-07/post-blocks.ts:35.
  - Diagram 3 (post.md:224): CLAUDE.md Inheritance Chain — Global `~/.claude/CLAUDE.md` → Project `./CLAUDE.md` (label "Inherited by all projects") → 9 leaf nodes for the 9 rules files (label "Extended by"). The 9 leaf labels in order are: `.claude/rules/security.md`, `.claude/rules/coding-style.md`, `.claude/rules/testing.md`, `.claude/rules/git-workflow.md`, `.claude/rules/agents.md`, `.claude/rules/hooks.md`, `.claude/rules/patterns.md`, `.claude/rules/performance.md`, `.claude/rules/development-workflow.md` — post-07/post-blocks.ts:120.

### 5.4 post-16 inline diagrams

- 2 inline SVGs referenced — `/svg/post-16-1.svg`, `/svg/post-16-2.svg` — post-16/post.md:159, 178.
- post-16/post.md:159 = "The Hook Lifecycle" — describes "Three intercept points: before the tool runs, after it finishes, and once per user message" — post-16/post.md:156.
- post-16/post.md:178 = enforcement pyramid (same content as `enforcement-pyramid.html`).
- Typed body adds wa-node graph (sysId `post-16-shannon-stack`) — `site/src/lib/post-bodies/post-16.ts:142-163`.

---

## Section 6 — Behavioral Promises (Shannon framework MUST deliver)

### 6.1 Aggregate violation-rate promise

"Across the measured sessions, the aggregate violation rate dropped from 3.1 per session to 0.4, an 87% reduction." — post-07/post.md:265.
"Hook overhead: 7ms per tool call, undetectable in practice." — post-07/post.md:265.

### 6.2 Per-hook violation-rate promises

(From §2.7 above; restated as promises Shannon must deliver.)

- `block-test-files.js`: 23% → 0% (post-07/post.md:164); non-zero → zero (post-16/post.md:38-39, 199).
- `read-before-edit.js`: 31% → 4% (post-07/post.md:166). Read-to-Edit ratio 2:1 → 4.4:1 (post-16/post.md:254). Read-to-Write ratio 4:1 → 9.6:1 (post-07/post.md:267, post-07/post.md:43).
- `validation-not-compilation.js`: 41% → 9% (post-07/post.md:190). "Across 82,552 Bash calls in 23,479 sessions, the hook fired every time a build succeeded. Every time." — post-16/post.md:150.
- `evidence-gate-reminder.js`: Task completion quality +34% (post-07/post.md:202).
- `skill-activation-check.js`: drives "1,370 skill invocations" (post-07/post.md:204).

### 6.3 Subagent inheritance promise

"68% compliance for subagents without constitution injection versus 95% with it. That's a 27-point drop just because the rules didn't get passed along." — post-07/post.md:255.
"2,827 Task spawns and 929 Agent calls across all 23,479 sessions." — post-07/post.md:259.

### 6.4 Repo deliverable promise

- "The Shannon Framework is a reference Claude Code plugin with 5 hooks, 1 skill, and 1 agent template." — post-16/post.md:417.
- "The [shannon-framework](https://github.com/krzemienski/shannon-framework) repo contains working implementations of all the hooks and skills I've described." — post-07/post.md:307.
- "Drop them into your project: cp -r hooks/ .claude/hooks/ ; cp -r skills/ .claude/skills/ ; cp -r agents/ .claude/agents/" — post-07/post.md:312-318.

Implied directory contract: `shannon-framework/hooks/`, `shannon-framework/skills/`, `shannon-framework/agents/` exist and contain the 5 named hook files + at least 1 skill (`functional-validation`) + at least 1 agent template.

**Inconsistency:** Post-16 linkedin-article hero-cover alt-text says "5 commands, 5 skills, 5 hooks, 4 agents" — post-16/social/linkedin-article.md:27. Post-16 prose says "5 hooks, 1 skill, 1 agent template" — post-16/post.md:417. Both attestations published, materially different deliverable counts.

### 6.5 Three-level severity promise

"Three levels hit 95% compliance." — post-07/post.md:249. Shannon must support Block / Warn / Remind.

### 6.6 Rules-split promise

"A single 800-line CLAUDE.md produced 72% compliance on rules in the bottom half of the file. The same rules split into focused files: 89% compliance." — post-07/post.md:235. Shannon must support `.claude/rules/*.md` split with 9 named files.

### 6.7 Conflict-resolution rule

"When a block hook fires on an instructed action, satisfy the precondition. Don't work around it." — post-07/post.md:303. Layer 3 wins temporarily over Layer 1.

### 6.8 Hook performance budget

"Synchronous. Under 100ms. No network calls." — post-16/post.md:346. "Hook overhead: 7ms per tool call." — post-07/post.md:265.

### 6.9 Hook crash semantics

"a hook that crashes is a silent allow — the tool call proceeds as if no hook existed." — post-16/post.md:169. Shannon hook runner MUST follow that semantics.

### 6.10 Skill invocation effect

"1,370 skill invocations kept agents on prescribed workflows instead of improvising." — post-07/post.md:83. Shannon must instrument skill invocation count.

### 6.11 Tool-call instrumentation promise

Numbers Shannon must be able to measure (claimed measured in production):
- Read: 87,152 — post-07/post.md:267
- Bash: 82,552 — post-07/post.md:267
- Edit: 19,979 — post-07/post.md:267
- Read-to-Write ratio: 9.6:1 (post-hook) — post-07/post.md:267
- Skill: 1,370 — post-07/post.md:62, post-16/post.md:54
- ExitPlanMode: 111 — post-07/post.md:62
- Sequential thinking MCP: 327 — post-07/post.md:87
- Task spawns: 2,827 — post-07/post.md:259
- Agent calls: 929 — post-07/post.md:259
- Sessions surveyed: 23,479 over 42 days — post-07/post.md:39

### 6.12 Cross-post forward promise (post-06 → post-07)

"Post 7 covers the prompt engineering stack that makes isolated agents reliable: how to write specs that produce deterministic outputs, how to structure CLAUDE.md so agents don't drift, and **how the Shannon framework enforces constraints that plain instructions can't.**" — `posts/post-06-parallel-worktrees/post.md:368`. Post-06 is the only OTHER blog post that names Shannon (besides post-07/post-16). It promises Shannon "enforces constraints that plain instructions can't."

---

## Unresolved Questions

1. **Layer count canonical: 7 or 4?** Post-07 specifies 7 layers (CLAUDE.md global, .claude/rules/, Hooks, Skills, Agents, MCP, SessionStart). Post-16 specifies 4 layers (CLAUDE.md, Hooks, Skills, Commands). Both call themselves "Shannon Framework" and both reference the same `github.com/krzemienski/shannon-framework`. Workstream B should determine which the repo actually implements.

2. **Hook return contract: object-return vs stderr+exit?** Post-07 hook code returns `{ decision, message }` objects. Post-16 hook code uses `process.stderr.write(...); process.exit(2);`. These are different contracts. Workstream B/C should determine the live Claude Code-compatible contract.

3. **Test-pattern count: 10 or 12?** Post-07 prose says "12 patterns"; post-07 code shows 10. Post-16 prose says "12 patterns"; post-16 code shows 12. Workstream B should pick canonical.

4. **Deliverable count: 5 hooks + 1 skill + 1 agent OR 5 commands + 5 skills + 5 hooks + 4 agents?** post-16 body says the former; post-16 linkedin-article hero alt-text says the latter. Material conflict.

5. **Commands surface (Layer 4 in post-16 = `/autopilot`, `/ralph`, `/team`)** — neither named slash command appears in post-07. Are commands part of shannon-framework or an external dependency? Workstream B/C should determine.

6. **Sub-agent inheritance hook name** — post-07 prose describes a "PreToolUse hook on the Agent tool" but does not name it. Not in the 5-hook loadout. Either an unnamed 6th hook or part of one of the named hooks. Workstream B should resolve.

7. **`readFiles` Set initialisation** — post-07 code uses `readFiles.add(...)` without declaring the Set in the snippet. Post-16 prose claims module-level. Workstream B verify the actual code.

8. **Session-start injection mechanism (Layer 7)** — post-07 names it but provides no schema, no event name (CC SessionStart hook?), no payload. Workstream C (live Claude Code instrumentation) must resolve.

9. **MCP tools layer (Layer 6)** — post-07 names "sequential thinking" and "Stitch MCP" as examples but does not specify whether Shannon ships MCP servers or just claims credit for third-party MCPs. Workstream B/D must resolve.

10. **Numeric provenance** — post.md frontmatter `date: 2026-05-19` post-dates the claimed measurement window (42 days "Jan 24 – Mar 6, 2026" per posts/INDEX.md:14). Numbers like 87% / 23,479 / 1,370 must reconcile with `scripts/output/series-metrics.md` (referenced in posts/INDEX.md:138). Out of Workstream A scope but flagging.

---

End of extraction. Total claims indexed: ~95. Total source citations: ~110.
