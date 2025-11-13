# Claude Code Plugin System: Complete Research

**Purpose**: Understand how Claude Code plugins actually work before testing Shannon
**Method**: Systematic research → understanding → then proper setup
**Date**: 2025-11-08

---

## From Claude Code Documentation

### Plugin Structure (Standard)

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json           # REQUIRED: Plugin manifest
├── commands/                  # OPTIONAL: Custom slash commands
│   └── my-command.md         # Each .md becomes /my-command
├── agents/                    # OPTIONAL: Custom agents
│   └── MY_AGENT.md           # Agent definition
├── skills/                    # OPTIONAL: Model-invoked capabilities
│   └── skill-name/
│       └── SKILL.md          # Skill definition
└── hooks/                     # OPTIONAL: Event handlers
    └── hooks.json            # Hook configuration
```

### plugin.json (REQUIRED Fields)

```json
{
  "name": "plugin-name",        // REQUIRED
  "version": "1.0.0",          // REQUIRED
  "description": "...",        // REQUIRED
  "author": {...},             // REQUIRED
  "displayName": "..."         // OPTIONAL
}
```

---

## How Components Are Discovered

### Commands (commands/)

**Discovery Mechanism**:
- Claude Code scans `commands/` directory
- Each `.md` file becomes a slash command
- Filename determines command name: `sh_spec.md` → `/shannon:spec`
- YAML frontmatter defines: name, description, usage

**Execution**:
- User types `/shannon:spec "specification"`
- Claude Code loads `commands/shannon:spec.md`
- Content is **injected into system prompt**
- Claude **reads the markdown** and **executes the workflow**

**Key Insight**: Commands are **prompt expansions**, not code execution

### Skills (skills/)

**Discovery Mechanism**:
- Claude Code scans `skills/*/SKILL.md` pattern
- Each folder with SKILL.md becomes an available skill
- Folder name = skill name: `skills/spec-analysis/SKILL.md` → "spec-analysis" skill

**Invocation**:
- **Model-invoked**: Claude autonomously loads when relevant to task
- **Explicit**: Via Skill tool: `Skill(skill="spec-analysis")`
- YAML frontmatter describes when to use

**Execution**:
- Skill content loaded into context
- Claude reads instructions
- Claude follows the skill's workflow

**Key Insight**: Skills are **context injections** that guide behavior

### Hooks (hooks/)

**Registration**:
- hooks.json defines hook configuration
- Maps events (SessionStart, PreCompact, PostToolUse, Stop) to scripts

**Execution**:
- Event fires → Claude Code runs specified script
- Script receives JSON input, returns JSON output
- Hook can: allow, block, or modify behavior

**Key Insight**: Hooks are **external scripts** that intercept execution

### Agents (agents/)

**Discovery**:
- Agent .md files in agents/ directory
- Each .md defines specialized sub-agent

**Invocation**:
- Via Task tool with subagent_type parameter
- Agent loads with specific system prompt from .md file

**Key Insight**: Agents are **specialized Claude instances** with preset prompts

---

## Installation Methods

### Method 1: Global (from marketplace)

```bash
/plugin marketplace add org-name/marketplace-name
/plugin install plugin-name@marketplace-name
# Restart Claude Code
```

**Scope**: Available in ALL projects
**Use Case**: Production plugins, widely-used tools

### Method 2: Project-Scoped (local development)

```bash
/plugin marketplace add /absolute/path/to/plugin-directory
/plugin install plugin-name@local-marketplace-name
# Restart Claude Code
```

**Scope**: Available only in this project
**Use Case**: Development, testing, project-specific plugins

### Method 3: .claude/settings.json (team/repo)

```json
{
  "plugins": {
    "enabled": ["plugin-name@marketplace"]
  }
}
```

**Scope**: Auto-loads for team when repo trusted
**Use Case**: Team collaboration, required plugins

---

## For Shannon Testing

### Current Understanding

Shannon structure matches plugin standard:
```
shannon-framework/
├──               # This is the plugin root
│   ├── .claude-plugin/
│   │   └── plugin.json ✓       # Has manifest
│   ├── commands/               # 46 .md files
│   ├── agents/                 # 24 .md files
│   ├── skills/                 # 16 SKILL.md folders
│   └── hooks/
│       └── hooks.json ✓        # Hook configuration
```

### To Test Shannon Locally (Proper Method)

**Step 1**: Add this repo as marketplace
```bash
/plugin marketplace add /Users/nick/Desktop/shannon-framework
```

**Step 2**: Install shannon plugin
```bash
/plugin install shannon@shannon-framework
```

**Step 3**: Restart Claude Code
(Required for plugin to load)

**Step 4**: Verify installation
```bash
/shannon:status  # Should work if Shannon loaded
/help       # Should show Shannon commands
```

**Step 5**: Test components
- Commands: Try /shannon:spec, /shannon:wave, /shannon:checkpoint
- Skills: Use Skill tool to load shannon skills
- Hooks: Should auto-load (SessionStart triggers using-shannon)

---

## Questions Still Unanswered

1. **Command Execution**: When `/shannon:spec` fires, does Claude Code:
   - Load the .md into system prompt?
   - Parse the YAML frontmatter?
   - Execute the "Workflow" section as instructions?
   - How does `@skill spec-analysis` pseudocode actually invoke the skill?

2. **Skill Invocation**: When command says `@skill spec-analysis`, does:
   - Claude Code parse this and load the skill?
   - Or does Claude read it as instruction and use Skill tool itself?
   - Is `@skill` a special syntax or just documentation?

3. **Hook Execution**: When hook fires:
   - Does output go to system prompt or user chat?
   - Can hooks actually block tool execution?
   - How does "decision": "block" work?

4. **Project vs Global**:
   - Where are plugins actually installed?
   - Is there a .claude/plugins/ directory that gets created?
   - How does Claude Code find plugins?

---

## What I Need To Do

1. ✅ Read documentation (done above)
2. **Actually install Shannon locally** (proper /plugin commands in chat)
3. **Test each component** works (commands, skills, hooks, agents)
4. **Trace actual execution paths** (what happens when /shannon:spec fires?)
5. **Document with evidence** (not theory, actual observed behavior)
6. **Use this understanding** to complete remaining enhancements properly

---

## Next Step

Install Shannon locally in THIS Claude Code session and test it works.

Then I'll have actual functional testing capability and can:
- Test the 3 skills I enhanced
- Enhance the remaining 13 skills with ability to test
- Verify hooks actually fire
- Understand command→skill invocation firsthand

**This is what the user meant**: Don't document theories, test the actual system.
