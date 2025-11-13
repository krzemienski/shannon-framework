# Claude Code Plugin Architecture - Official Reference

**Generated**: 2025-01-12
**Purpose**: Authoritative understanding of Claude Code plugin capabilities from official Anthropic documentation
**Sources**: docs/ref/ directory (17 official documentation files)
**Sequential Thoughts**: 30 thoughts completed

---

## Executive Summary

Claude Code plugins extend Claude's capabilities through a well-defined component system. Plugins can include **slash commands**, **skills**, **hooks**, **subagents**, **MCP servers**, and **system prompt modifications** (CLAUDE.md). Each component type serves a specific purpose and has different invocation patterns and enforcement capabilities.

**Key Insight**: Plugins work through **prompt engineering**, not code execution. Most components are markdown files that inject instructions into Claude's context.

---

## Official Plugin Components

### 1. Slash Commands

**Purpose**: User-invoked entry points for workflows

**File Structure**:
- Location: `.claude/commands/`
- Format: `{command-name}.md`
- Invocation: `/command-name` (or `/plugin-name:command-name` when from plugin)

**Basic Example** (commands/optimize.md):
```markdown
Analyze this code for performance issues and suggest optimizations.
```

**With Frontmatter** (commands/fix-issue.md):
```markdown
---
description: Fix GitHub issue
argument-hint: [issue-number] [priority]
allowed-tools: Read, Write, Bash
---

Fix issue #$1 with priority $2.
Check issue description and implement changes.
```

**Features**:
- **Arguments**: `$ARGUMENTS` (all), `$1`, `$2`, etc. (individual)
- **Bash execution**: `!`git status`` (inline command execution)
- **File references**: `@src/utils/helpers.js` (include file content)
- **Tool restrictions**: `allowed-tools` limits available tools
- **Namespacing**: Auto-namespaced to prevent conflicts (plugin-name:command)

**Invocation Method**: Manual by user via SlashCommand tool

**Enforcement**: Medium - User chooses when to invoke, but command content is explicit instruction

---

### 2. Skills

**Purpose**: Model-invoked workflows that activate based on context

**File Structure**:
- Location: `.claude/skills/{skill-name}/`
- Required: `SKILL.md`
- Optional: `reference.md`, `scripts/`, `templates/`, `examples/`, `tests/`

**SKILL.md Structure**:
```yaml
---
name: your-skill-name
description: What this does and when to use it
allowed-tools: Read, Grep, Glob  # Optional: restrict tools
---

# Your Skill Name

## Instructions
Step-by-step guidance for Claude to follow.
```

**Frontmatter Requirements**:
- `name`: lowercase, numbers, hyphens only (max 64 chars)
- `description`: Max 1024 chars - **CRITICAL for model to know when to invoke**
- `allowed-tools`: Optional tool restrictions

**Invocation Methods**:
1. **Automatic**: Claude reads descriptions at startup, invokes when context matches
2. **Manual**: Via Skill tool directly
3. **Command-triggered**: Command expansion instructs "use {skill-name} skill"

**Enforcement**: Strong (via description matching) to Very Strong (via explicit language in skill content)

**SDK Requirement**:
```python
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # REQUIRED!
    allowed_tools=["Skill"]
)
```

Without `setting_sources`, skills don't load from filesystem!

---

### 3. Hooks

**Purpose**: Event-driven automation that executes automatically on lifecycle events

**File Structure**:
- Location: `hooks/`
- Configuration: `hooks.json`
- Scripts: `.sh`, `.py` files

**hooks.json Structure**:
```json
{
  "hooks": {
    "EventName": [
      {
        "description": "...",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/script.py",
            "description": "...",
            "timeout": 5000,
            "continueOnError": false
          }
        ]
      }
    ]
  }
}
```

**Available Events**:
- `SessionStart`: When session begins
- `UserPromptSubmit`: Before each user prompt (every interaction!)
- `PostToolUse`: After tool usage (can use matcher to filter specific tools)
- `PreCompact`: Before context compression
- `Stop`: When session ends

**Hook Features**:
- `matcher`: Regex pattern to filter tool names (e.g., `"Write|Edit|MultiEdit"`)
- `timeout`: Maximum execution time in milliseconds
- `continueOnError`: Whether to proceed if hook fails (false = blocks session)
- `type`: Usually "command" (execute shell/Python script)

**Invocation**: Automatic on lifecycle events (cannot be skipped by user)

**Enforcement**: Strongest - Automatic execution, can block actions, can inject context

---

### 4. Subagents (Agents)

**Purpose**: Specialized AIs for specific tasks with separate context

**Two Definition Approaches**:

**A. Filesystem** (agents/*.md):
```markdown
---
description: When to use this agent
---

# Agent System Prompt

You are a specialized agent for...
```

**B. Programmatic** (SDK only):
```python
options = ClaudeAgentOptions(
    agents={
        'code-reviewer': {
            'description': 'Expert code review specialist',
            'prompt': 'You are a code reviewer...',
            'tools': ['Read', 'Grep', 'Glob'],
            'model': 'sonnet'
        }
    }
)
```

**Benefits**:
- Separate context from main agent
- Specialized instructions
- Tool restrictions
- Can run in parallel

**Invocation**: Via Task tool with subagent_type parameter

**Note**: Claude Code has many built-in agents. Plugins can define custom agents OR provide guides for using built-in agents.

---

### 5. MCP Servers (Custom Tools)

**Purpose**: Extend Claude with custom tools via Model Context Protocol

**Creation** (SDK):
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("get_weather", "Get temperature for location", {"lat": float, "lon": float})
async def get_weather(args: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": "Temperature: 72°F"}]}

server = create_sdk_mcp_server(name="weather", version="1.0.0", tools=[get_weather])
```

**Usage**:
```python
options = ClaudeAgentOptions(
    mcp_servers={"weather": server},
    allowed_tools=["mcp__weather__get_weather"]
)
```

**Tool Name Format**: `mcp__{server_name}__{tool_name}`

**Invocation**: Claude calls tools as needed (if in allowed_tools)

---

### 6. System Prompt Modification (CLAUDE.md)

**Purpose**: Modify Claude's base behavior for all interactions in a project

**File**: `CLAUDE.md` or `.claude/CLAUDE.md` at project root

**Loading**:
```python
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},
    setting_sources=["project"]  # REQUIRED to load CLAUDE.md!
)
```

**Characteristics**:
- Persists across sessions (file-based)
- Always loaded when present (if setting_sources configured)
- Modifies base behavior before any other instructions
- Cannot be disabled without removing file or changing setting_sources

**Enforcement**: Very Strong - Always active, modifies foundation

---

## Plugin Manifest (plugin.json)

**Location**: `.claude-plugin/plugin.json`

**Required Fields**:
```json
{
  "name": "plugin-name",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  }
}
```

**Optional Fields**:
- `homepage`: Plugin website
- `repository`: Source code URL
- `license`: License type (e.g., "MIT")
- `keywords`: Searchable keywords for marketplace

**Purpose**: Identifies plugin to Claude Code, enables marketplace distribution

---

## Plugin Loading and Discovery

### CLI Installation

```bash
# Add marketplace
/plugin marketplace add owner/repo

# Install plugin
/plugin install plugin-name@marketplace-name

# Plugin installed to:
~/.claude/plugins/plugin-name@marketplace-name/
```

**At Startup**:
1. plugin.json read → Metadata registered
2. CLAUDE.md loaded → System prompt modified
3. Commands discovered → Registered as /plugin-name:command
4. Skills discovered → Metadata added to available skills
5. Hooks registered → Bound to lifecycle events
6. Agent definitions loaded → Available for Task tool

### SDK Loading

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # CRITICAL!
    plugins=[{"type": "local", "path": "./my-plugin"}],
    allowed_tools=["Skill", "SlashCommand", "TodoWrite"]
)

async for message in query(prompt="/my-plugin:command", options=options):
    print(message)
```

**Critical Requirements**:
- `setting_sources=["user", "project"]` - Without this, skills and commands don't load!
- `plugins` list with paths - Specifies which plugins to load
- `allowed_tools` - Must include "Skill" for skills, "SlashCommand" for commands

---

## Component Comparison Matrix

| Feature | Commands | Skills | Hooks | CLAUDE.md | Agents |
|---------|----------|--------|-------|-----------|--------|
| **Invocation** | User manual | Model automatic | Event automatic | Always loaded | Task tool |
| **Structure** | Single .md | Directory | Scripts + JSON | Single file | .md or programmatic |
| **Complexity** | Simple prompts | Complex workflows | Event handlers | Instructions | Specialized prompts |
| **Files** | One file | Multiple files | Multiple files | One file | One file or config |
| **Enforcement** | Medium | Strong | Strongest | Very Strong | Medium |
| **User Control** | Full | Partial | None | None | Full |
| **Tool Restriction** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Arguments** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Context** | Shared | Shared | Shared | Shared | Separate |

---

## Enforcement Capabilities

### What Plugins CAN Enforce

✅ **Via Hooks** (Strongest):
- Inject content into every prompt (UserPromptSubmit)
- Block specific tool usage (PostToolUse with matcher)
- Require validation before completion (Stop with continueOnError: false)
- Create checkpoints before compression (PreCompact)
- Execute setup scripts (SessionStart)

✅ **Via CLAUDE.md** (Very Strong):
- Define base behavioral patterns (always loaded)
- Set project-specific rules and constraints
- Establish coding standards and practices

✅ **Via Skills** (Strong):
- Enforce workflows through detailed instructions
- Use strong language (CRITICAL, MUST, REQUIRED)
- Require TodoWrite for checklist items
- Guide step-by-step processes

✅ **Via Commands** (Medium):
- Provide clear entry points for workflows
- Expand to explicit instructions
- Invoke skills programmatically

### What Plugins CANNOT Enforce

❌ **Cannot Force**:
- Model to read content completely (can skim despite instructions)
- Model to use specific tools (can choose alternatives)
- User to invoke commands (user has full control)
- Model to follow suggestions (vs. requirements)

❌ **Cannot Prevent**:
- User from overriding workflows in chat
- Context loss (except via checkpoints)
- Model from making autonomous decisions
- Skill discovery failures (if description doesn't match)

❌ **Cannot Guarantee**:
- 100% compliance with any instruction (model is autonomous)
- Perfect execution of complex workflows
- That skills will be discovered and used automatically

### Mitigation Strategies

**To Maximize Enforcement**:
1. **Layer mechanisms**: Use hooks + skills + commands for same principle
2. **Strong language**: ALL CAPS, bold, "CRITICAL", "MUST"
3. **Explicit checklists**: → TodoWrite for visibility and tracking
4. **Validation gates**: Hooks that block until conditions met
5. **Examples**: Show correct vs. incorrect patterns
6. **Repetition**: State requirements multiple times in different components

**Defense in Depth**: Shannon uses ALL these strategies

---

## Plugin Lifecycle Flow

### Installation to Execution

```
User Action: /plugin install shannon@shannon-framework
    ↓
Installation:
    - Plugin copied to ~/.claude/plugins/shannon@shannon-framework/
    - Metadata registered in Claude Code
    ↓
Next Claude Code Startup:
    - plugin.json read → "shannon" registered
    - CLAUDE.md loaded → Base system prompt modified
    - Commands discovered → /shannon:spec, /shannon:prime, etc. registered
    - Skills discovered → Metadata for 18 skills added
    - Hooks registered → 5 event types bound to scripts
    ↓
SessionStart Event:
    - Hooks fire → session_start.sh executes
    - using-shannon meta-skill loaded
    - Shannon framework now active
    ↓
User Types: /shannon:spec "Build a web app"
    ↓
Command Expansion:
    - commands/spec.md content loaded
    - Content becomes prompt: "Use spec-analysis skill to..."
    ↓
Skill Invocation:
    - Skill tool called with "spec-analysis"
    - skills/spec-analysis/SKILL.md loaded
    - Skill content guides behavior
    ↓
UserPromptSubmit Hook:
    - Fires before processing
    - Injects North Star goal context
    - Adds active wave information
    ↓
Execution:
    - Claude follows skill workflow
    - 8D complexity analysis performed
    - If writing code → PostToolUse hook checks for mocks
    ↓
Completion:
    - Stop hook fires
    - Validates wave gates
    - Blocks if validation fails
    ↓
PreCompact (if needed):
    - Context growing large
    - PreCompact hook fires
    - Checkpoint created before compression
```

---

## Component Invocation Patterns

### Commands

**Pattern 1: Direct Invocation**
```
User types: /shannon:spec "specification text"
↓
SlashCommand tool receives "shannon:spec"
↓
commands/spec.md content expands into prompt
↓
Claude processes expanded prompt
```

**Pattern 2: With Arguments**
```
User types: /shannon:task "feature description" high
↓
Command receives: $1="feature description", $2="high", $ARGUMENTS="feature description high"
↓
Command template: "Create task for $1 with priority $2"
↓
Expands to: "Create task for feature description with priority high"
```

**Pattern 3: With Bash Execution**
```
Command content: "Current status: !`git status`"
↓
Bash command executes: git status
↓
Output inserted: "Current status: On branch main, nothing to commit"
```

### Skills

**Pattern 1: Automatic (Model-Invoked)**
```
User request: "I need to test this authentication module"
↓
Claude reads skill descriptions
↓
Matches: functional-testing skill ("NO MOCKS testing enforcement")
↓
Claude invokes: Skill tool with "functional-testing"
↓
skills/functional-testing/SKILL.md loaded and followed
```

**Pattern 2: Command-Triggered**
```
User types: /shannon:test
↓
commands/test.md expands: "Use functional-testing skill"
↓
Claude sees explicit instruction
↓
Invokes Skill tool with "functional-testing"
```

**Pattern 3: Skill-Referenced**
```
spec-analysis skill content: "If errors occur, use systematic-debugging skill"
↓
Claude encounters error during spec analysis
↓
Invokes Skill tool with "systematic-debugging"
↓
Nested skill workflow activated
```

### Hooks

**Pattern 1: Context Injection (UserPromptSubmit)**
```
User types any prompt
↓
UserPromptSubmit hook fires BEFORE processing
↓
user_prompt_submit.py executes
↓
Reads North Star goal + active wave
↓
Injects context into prompt: "Remember: North Star goal is X. Active wave: Y."
↓
Enhanced prompt processed by Claude
```

**Pattern 2: Action Blocking (PostToolUse)**
```
Claude uses Write tool to create test file
↓
PostToolUse hook fires with matcher="Write|Edit|MultiEdit"
↓
post_tool_use.py executes
↓
Scans written content for mock patterns
↓
If mocks detected: Returns error, blocks write
If no mocks: Allows write to proceed
```

**Pattern 3: Validation Gates (Stop)**
```
User ends session or Claude completes task
↓
Stop hook fires
↓
stop.py validates wave completion gates
↓
If gates satisfied: Session ends normally
If gates not satisfied: Blocks with error message
```

**Pattern 4: State Preservation (PreCompact)**
```
Context size approaches limit
↓
Claude Code prepares to compact (compress context)
↓
PreCompact hook fires BEFORE compaction
↓
precompact.py creates checkpoint (15s timeout allowed)
↓
Checkpoint saved
↓
Compaction proceeds
```

---

## Enforcement Strength Analysis

### Enforcement Hierarchy (Strongest to Weakest)

**1. Hooks with continueOnError: false** (ABSOLUTE)
- Session cannot proceed if hook fails
- No user override possible
- Example: Shannon's PreCompact hook

**2. Hooks with Automatic Firing** (VERY STRONG)
- Execute on events without user action
- Can inject context, block actions
- Example: UserPromptSubmit (fires on every prompt)

**3. CLAUDE.md Always-Loaded** (VERY STRONG)
- Loaded at every session start
- No way to disable (except uninstall plugin)
- Modifies base behavior foundation

**4. Skills with CRITICAL/MUST Language** (STRONG)
- Strong prompt engineering
- Model highly likely to follow
- Example: "YOU MUST create TodoWrite todos"

**5. Command Explicit Instructions** (MEDIUM-STRONG)
- User chose to invoke
- Instruction is clear and direct
- Example: "Use spec-analysis skill to analyze this specification"

**6. Skills with Automatic Discovery** (MEDIUM)
- Model chooses when to invoke
- Based on description matching
- Can fail to discover if description doesn't match context

**7. Skills with SHOULD/RECOMMENDED** (MODERATE)
- Softer language
- Model may skip if conditions warrant
- Example: "You SHOULD consider using..."

**8. Documentation and Examples** (WEAK)
- Informative but not enforced
- Model may ignore if focused on task
- Example: README files, usage guides

---

## Shannon Framework's Usage of Official Capabilities

### Standard Components (Used by Shannon)

✅ **Slash Commands**: 15 commands in commands/
- analyze, spec, prime, test, wave, etc.
- Follow official structure exactly
- Use frontmatter for descriptions and arguments

✅ **Skills**: 18 skills in skills/
- Each has SKILL.md with required frontmatter
- Descriptions optimized for auto-discovery
- Many include examples/, tests/, references/

✅ **Hooks**: 5 active hooks in hooks.json
- SessionStart, UserPromptSubmit, PostToolUse, PreCompact, Stop
- Mix of shell (.sh) and Python (.py) scripts
- Strategic use of continueOnError and matchers

✅ **Plugin Manifest**: .claude-plugin/plugin.json
- All required fields present
- Version 5.0.0, proper metadata
- Marketplace-ready

✅ **CLAUDE.md**: Root level file
- Installation and usage instructions
- Version information
- Developer vs. user guidance

✅ **Agent Guides**: 25 agent guide files
- NOT custom agents (filesystem approach)
- GUIDES for using Claude Code's built-in agents
- This is clever reuse of agents/ directory for documentation

### Custom/Non-Standard Components (Shannon Extensions)

❓ **core/ Directory**: 9 behavioral pattern files
- NOT mentioned in official plugin documentation
- Appear to be additional system prompt modifications
- Mechanism unclear - investigate in Phase 6

❓ **modes/ Directory**: 2 mode definition files
- NOT mentioned in official plugin documentation
- Purpose unclear - investigate in Phase 6

✅ **Extensive Documentation**: docs/, tests/, examples/
- Standard practice, well-organized
- Reference documentation maintained
- Comprehensive testing framework

---

## Key Insights from Official Documentation

### 1. Plugins Are Prompt-Engineering Frameworks
Components are primarily **markdown files** that inject instructions. The plugin system provides:
- Structured way to organize prompts (commands, skills, core)
- Lifecycle hooks to inject at right moments
- Discovery mechanisms to activate when needed

### 2. setting_sources Is Critical for SDK
```python
# WITHOUT setting_sources - Plugin won't work!
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./plugin"}]
)
# Skills won't load, commands won't load, CLAUDE.md won't load

# WITH setting_sources - Plugin fully functional
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # THE KEY!
    plugins=[{"type": "local", "path": "./plugin"}]
)
```

### 3. Namespacing Prevents Conflicts
All plugin commands are automatically namespaced:
- Internal: `commands/spec.md`
- External: `/shannon:spec`

Users know which plugin provides which command, multiple plugins can coexist.

### 4. Model Invocation vs. User Invocation
**Model-invoked** (Skills):
- Pro: Automatic, discovers when needed
- Con: May not discover if description doesn't match

**User-invoked** (Commands):
- Pro: Explicit, reliable activation
- Con: Requires user knowledge of when to invoke

**Best Practice**: Provide BOTH (Shannon does this)
- Commands for explicit invocation
- Skills for automatic discovery
- Commands can invoke skills (gets both benefits)

### 5. Hooks Enable True Enforcement
Only hooks can:
- Execute WITHOUT user action
- Block actions (continueOnError: false)
- Inject into EVERY interaction (UserPromptSubmit)
- Intercept specific tools (PostToolUse with matcher)

This makes hooks the most powerful enforcement mechanism.

---

## Official Capabilities Shannon Doesn't Use

Based on documentation review:

❌ **Custom MCP Servers** (In-Plugin):
- Shannon teaches MCP discovery/usage
- But doesn't bundle MCP servers
- Makes sense: MCP servers are external integrations

❌ **Programmatic Agents** (SDK):
- Shannon uses filesystem approach (agents/*.md)
- Actually uses for documentation, not custom agents
- Relies on Claude Code's built-in agents

❓ **Tool Restrictions in Commands**:
- Official docs show allowed-tools in command frontmatter
- Need to verify if Shannon's commands use this

❓ **Bash Execution in Commands**:
- Official docs show !`command` syntax
- Need to verify if Shannon's commands use this

---

## Questions for Next Phases

### Phase 3 (Commands Analysis)
- Do Shannon's commands use allowed-tools restrictions?
- Do any commands use bash execution (!`command`)?
- Which commands invoke which skills?
- Are commands named with sh_* prefix in some contexts?

### Phase 4 (Skills Analysis)
- Which skills have allowed-tools restrictions?
- Which skills reference other skills?
- What makes using-shannon a "meta-skill"?
- How strong is the enforcement language in each skill?

### Phase 5 (Hooks Analysis)
- How does post_tool_use.py detect mocks?
- What are "wave validation gates" in stop.py?
- What does user_prompt_submit.py inject exactly?
- Why shell for session_start but Python for others?

### Phase 6 (Core Files Analysis)
- How are core/ files loaded? (Not in official docs!)
- Are they referenced in CLAUDE.md?
- Loaded by SessionStart hook?
- What's their relationship to skills with similar names?

---

## Authoritative Conclusions

Based on 30 sequential thoughts analyzing official Claude Code documentation:

1. **Plugin Architecture is Well-Defined**: Commands, skills, hooks, agents, MCP servers, CLAUDE.md
2. **Enforcement Varies by Component**: Hooks strongest, documentation weakest
3. **Prompt Engineering is Primary Mechanism**: Markdown files inject instructions
4. **setting_sources is Critical for SDK**: Required for plugin loading
5. **Namespacing Enables Coexistence**: Multiple plugins work together
6. **Shannon Uses Standard Capabilities**: Follows official patterns closely
7. **Shannon Adds Custom Extensions**: core/ and modes/ directories non-standard
8. **Shannon Maximizes Available Enforcement**: Uses strongest mechanisms for critical behaviors

**Ready for Phase 3**: Commands Architecture Analysis with authoritative framework for evaluation

---

## Reference Documentation Inventory

### Core Plugin Docs (Read Completely)
- ✅ code-claude-skills-LATEST.md (65 lines)
- ✅ code-claude-slash-commands-LATEST.md (74 lines)
- ✅ plugin-marketplaces-LATEST.md (137 lines)

### SDK Docs (Read Completely)
- ✅ sdk-plugins-LATEST.md (103 lines)
- ✅ sdk-skills-LATEST.md (53 lines)
- ✅ sdk-subagents-LATEST.md (46 lines)
- ✅ sdk-custom-tools-LATEST.md (52 lines)
- ✅ sdk-modifying-prompts-LATEST.md (55 lines)
- ✅ sdk-sessions-LATEST.md (56 lines)
- ✅ sdk-todo-tracking-LATEST.md (35 lines)

### Directory Documentation
- ✅ claude-code-llms.txt (48 lines) - Documentation directory
- 🔍 claude-code-llms-full.txt (13,628 lines) - Full docs (sampled, not read completely)

### Specification Files (For Context)
- 📋 prd-creator-spec.md (232 lines) - Test application spec
- 📋 claude-code-expo-spec.md (2,884 lines) - Test application spec
- 📋 repo-nexus-spec.md (2,924 lines) - Test application spec
- 📋 shannon-cli-spec.md (4,920 lines) - Test application spec

**Total Read**: ~800 lines of official plugin architecture documentation
**Purpose**: Authoritative framework for analyzing Shannon's implementation
