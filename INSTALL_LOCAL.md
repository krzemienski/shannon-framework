# Shannon Framework - Local Installation Guide

## Overview

This guide explains how to install Shannon Framework **directly** to your user-level Claude configuration instead of using the plugin system.

### Why Local Installation?

The Claude plugin system doesn't always properly discover plugin components (skills, commands, agents, etc.). Local installation ensures Shannon Framework is **always** accessible by installing directly to `~/.claude/`.

### What Gets Installed

The local installation script (`install_local.sh`) installs Shannon Framework components to:

```
~/.claude/
├── skills/shannon/          # 17 skills
├── commands/shannon/        # 19 commands  
├── agents/shannon/          # 24 agents
├── core/shannon/            # 9 behavioral patterns
├── modes/shannon/           # 2 execution modes
├── templates/shannon/       # Templates
├── hooks/shannon/           # 5 hook scripts
└── hooks.json               # Hook configuration
```

## Installation

### Prerequisites

1. **Claude Code** installed
2. **Bash shell** (macOS/Linux)
3. **Serena MCP** configured (MANDATORY for Shannon)

### Installation Options

The installation script supports three modes:

```bash
./install_local.sh             # Fresh installation (default)
./install_local.sh --install   # Explicit installation
./install_local.sh --update    # Update existing installation
./install_local.sh --uninstall # Remove installation
./install_local.sh --help      # Show usage
```

### Step 1: Run Installation Script

From the Shannon Framework repository root:

```bash
./install_local.sh
```

**Automatic Plugin Detection:**
- If you have Shannon plugin installed, the script will detect it
- You'll be prompted to uninstall the plugin (recommended to avoid conflicts)
- The script will automatically remove the plugin if you agree

The script will:
- ✅ Create installation directories in `~/.claude/`
- ✅ Copy all skills, commands, agents, core files, modes, templates
- ✅ Install hook scripts with proper permissions
- ✅ Update `hooks.json` with Shannon hooks
- ✅ Embed `using-shannon` skill content into `session_start.sh` hook
- ✅ Update all path references to point to installed locations
- ✅ Verify installation integrity

### Step 2: Restart Claude Code

**CRITICAL**: You must completely restart Claude Code for hooks to activate.

1. Quit Claude Code
2. Restart Claude Code
3. Open any project

### Step 3: Verify Installation

In Claude Code, start a new session and run:

```
/shannon:status
```

**Expected output:**
```
Shannon Framework v5.4 active
```

### Step 4: Configure MCP Servers

Shannon requires Serena MCP (mandatory) and recommends other MCPs based on your project domains.

Check MCP status:
```
/shannon:check_mcps
```

Follow the instructions to install any missing MCPs.

## Usage

### Starting a Session

Begin every Shannon session with:

```
/shannon:prime
```

This command:
- Discovers all available skills
- Verifies MCP connections  
- Restores context if returning to a project
- Loads memories
- Activates forced reading protocol

### Analyzing a Specification

Before implementing any project, run:

```
/shannon:spec "Build a task management app with React and PostgreSQL"
```

This provides:
- 8-dimensional complexity score (0.0-1.0)
- Domain breakdown (Frontend %, Backend %, Database %)
- Execution strategy (sequential vs wave-based)
- MCP recommendations
- Phase plan

### Executing Tasks

For general task execution:

```
/shannon:do "add authentication with Auth0"
```

For structured execution with validation:

```
/shannon:exec "add authentication to React app"
```

For complex projects (complexity >= 0.50):

```
/shannon:wave Build authentication system
```

## Directory Structure

### Skills (`~/.claude/skills/shannon/`)

17 skills organized by function:

- `spec-analysis/` - 8D complexity analysis
- `wave-orchestration/` - Parallel wave execution
- `functional-testing/` - NO MOCKS enforcement
- `context-preservation/` - Automatic checkpointing
- `mcp-discovery/` - MCP recommendations
- `using-shannon/` - Meta-skill (loaded via SessionStart hook)
- And 11 more...

Each skill contains:
- `SKILL.md` - Main skill definition
- `examples/` - Usage examples
- `references/` - Related core files
- `tests/` - Validation tests

### Commands (`~/.claude/commands/shannon/`)

19 commands for Shannon workflows:

**Execution:**
- `do.md` - Intelligent task execution
- `exec.md` - Autonomous execution with validation
- `task.md` - Full workflow automation
- `wave.md` - Wave-based parallel execution

**Analysis:**
- `spec.md` - 8D complexity analysis
- `analyze.md` - Project analysis

**Session Management:**
- `prime.md` - Session initialization
- `status.md` - Framework health check

**And 11 more...**

### Agents (`~/.claude/agents/shannon/`)

24 specialized agents:

- `SPEC_ANALYZER.md` - Specification analysis
- `WAVE_COORDINATOR.md` - Wave orchestration
- `CONTEXT_GUARDIAN.md` - Context preservation
- `TEST_GUARDIAN.md` - Testing enforcement
- And 20 more...

### Core Files (`~/.claude/core/shannon/`)

9 behavioral patterns that define Shannon's workflows:

- `SPEC_ANALYSIS.md` - 8D complexity algorithm
- `WAVE_ORCHESTRATION.md` - Parallel execution patterns
- `TESTING_PHILOSOPHY.md` - NO MOCKS philosophy
- `CONTEXT_MANAGEMENT.md` - Checkpointing system
- `MCP_DISCOVERY.md` - MCP recommendation engine
- And 4 more...

### Hooks (`~/.claude/hooks/shannon/`)

5 hook scripts that enforce Shannon workflows:

**session_start.sh** - Loads `using-shannon` meta-skill at session start
- Establishes Shannon workflows
- **Note:** using-shannon content is **embedded** in this hook (not referenced)

**user_prompt_submit.py** - Injects North Star goal into every prompt
- Ensures goal alignment throughout session

**precompact.py** - Saves checkpoint before auto-compaction
- Prevents context loss during Claude Code compaction
- Triggers CONTEXT_GUARDIAN agent

**post_tool_use.py** - Blocks mock usage in test files
- Enforces NO MOCKS philosophy
- Detects jest.mock, unittest.mock, etc.

**stop.py** - Blocks completion until validation gates pass
- Ensures wave validation approval

## Key Differences from Plugin Installation

### Path Resolution

**Plugin installation:**
```markdown
References: shannon-plugin/skills/spec-analysis/SKILL.md
Variable: ${CLAUDE_PLUGIN_ROOT}/skills/spec-analysis/SKILL.md
```

**Local installation:**
```markdown
References: ~/.claude/skills/shannon/spec-analysis/SKILL.md
Direct path: /Users/username/.claude/skills/shannon/spec-analysis/SKILL.md
```

All path references are updated during installation.

### using-shannon Skill Loading

**Plugin installation:**
```bash
# session_start.sh references file
cat "${PLUGIN_DIR}/skills/using-shannon/SKILL.md"
```

**Local installation:**
```bash
# session_start.sh has content embedded
cat << 'SKILL_EOF'
[full using-shannon skill content here]
SKILL_EOF
```

This eliminates dependency on external files and ensures the skill is **always** loaded.

### Hook Configuration

**Plugin installation:**
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py"
}
```

**Local installation:**
```json
{
  "command": "${HOME}/.claude/hooks/shannon/user_prompt_submit.py"
}
```

Hooks use absolute paths to user's home directory.

## Verification

### Check Installation Integrity

```bash
# Verify skills installed
ls ~/.claude/skills/shannon/

# Verify commands installed  
ls ~/.claude/commands/shannon/

# Verify agents installed
ls ~/.claude/agents/shannon/

# Verify core files installed
ls ~/.claude/core/shannon/

# Verify hooks installed
ls ~/.claude/hooks/shannon/

# Verify hooks.json configured
cat ~/.claude/hooks.json
```

### Check Hook Scripts Executable

```bash
ls -l ~/.claude/hooks/shannon/

# Expected output:
# -rwxr-xr-x  session_start.sh
# -rwxr-xr-x  user_prompt_submit.py
# -rwxr-xr-x  precompact.py
# -rwxr-xr-x  post_tool_use.py
# -rwxr-xr-x  stop.py
```

### Test SessionStart Hook

Create a new Claude Code session and check for the using-shannon skill message:

```
<EXTREMELY_IMPORTANT>
You are using Shannon Framework V5.
...
</EXTREMELY_IMPORTANT>
```

If this appears at session start, the SessionStart hook is working.

### Test UserPromptSubmit Hook

Set a North Star goal:

```
/shannon:north_star "Build production-ready SaaS platform"
```

Then submit any prompt. You should see:

```
🎯 **North Star Goal**: Build production-ready SaaS platform
**Context**: All work must align with this overarching goal.
---
```

If this appears before your prompt, the UserPromptSubmit hook is working.

### Test PostToolUse Hook

Try to create a test file with mocks:

```
Create a test file test/example.test.js with:
  jest.mock('./module');
```

You should see:

```
🚨 **Shannon NO MOCKS Violation Detected**
...
```

If blocked, the PostToolUse hook is working.

## Troubleshooting

### Hooks Not Firing

**Problem:** Hooks don't execute when expected

**Solutions:**
1. Verify hooks.json exists: `cat ~/.claude/hooks.json`
2. Check hook scripts are executable: `ls -l ~/.claude/hooks/shannon/`
3. Completely restart Claude Code (quit and reopen)
4. Check installation log: `cat ~/.claude/shannon_install.log`

### Skills Not Found

**Problem:** `/shannon:spec` or other commands return "command not found"

**Solutions:**
1. Verify skills installed: `ls ~/.claude/skills/shannon/`
2. Verify commands installed: `ls ~/.claude/commands/shannon/`
3. Restart Claude Code
4. Try skill discovery: `/shannon:discover_skills`

### Path References Broken

**Problem:** Skills reference files that don't exist

**Solutions:**
1. Re-run installation script: `./install_local.sh`
2. Check path updates: `grep "shannon-plugin" ~/.claude/skills/shannon/*/SKILL.md`
   - Should return no results (all references updated)

### session_start.sh Not Loading

**Problem:** using-shannon skill not loaded at session start

**Solutions:**
1. Verify session_start.sh executable: `ls -l ~/.claude/hooks/shannon/session_start.sh`
2. Test hook manually: `bash ~/.claude/hooks/shannon/session_start.sh`
3. Check hooks.json SessionStart configuration: `cat ~/.claude/hooks.json | grep -A 10 SessionStart`

## Uninstallation

To remove Shannon Framework local installation:

```bash
./install_local.sh --uninstall
```

**What --uninstall does:**
- ✅ Removes all Shannon directories
- ✅ Backs up hooks.json before cleaning
- ✅ Restores previous hooks.json (if backup exists)
- ✅ Optionally uninstalls Shannon plugin (if detected)
- ✅ Archives installation logs

**Interactive prompts:**
1. Confirmation: "Are you sure you want to uninstall?"
2. Plugin detection: "Do you want to uninstall the plugin too?" (if found)

After uninstallation, restart Claude Code for changes to take effect.

**Manual Uninstallation** (if script fails):

```bash
# Remove installed components
rm -rf ~/.claude/skills/shannon
rm -rf ~/.claude/commands/shannon
rm -rf ~/.claude/agents/shannon
rm -rf ~/.claude/core/shannon
rm -rf ~/.claude/modes/shannon
rm -rf ~/.claude/templates/shannon
rm -rf ~/.claude/hooks/shannon

# Restore original hooks.json (if backup exists)
mv ~/.claude/hooks.json.backup.YYYYMMDD_HHMMSS ~/.claude/hooks.json
```

Then restart Claude Code.

## Updating

To update to a newer version of Shannon Framework:

1. Pull latest changes from repository:
   ```bash
   cd /path/to/shannon-framework
   git pull
   ```

2. Run update command:
   ```bash
   ./install_local.sh --update
   ```

3. Restart Claude Code

**What --update does:**
- ✅ Creates backup of existing installation
- ✅ Removes old files
- ✅ Installs updated components
- ✅ Updates path references
- ✅ Reconfigures hooks
- ✅ Verifies installation

**Backup location:** `~/.claude/shannon_backup_YYYYMMDD_HHMMSS/`

If issues occur after update, restore from backup:
```bash
cp -r ~/.claude/shannon_backup_YYYYMMDD_HHMMSS/* ~/.claude/
```

## Migration from Plugin Installation

If you previously installed Shannon as a Claude plugin:

### Option 1: Automatic Migration (Recommended)

```bash
./install_local.sh --install
```

The script will:
1. Detect existing plugin installation
2. Prompt you to uninstall the plugin
3. Automatically remove the plugin if you agree
4. Install local version
5. Restart required

### Option 2: Manual Migration

1. Uninstall the plugin manually:
   ```
   /plugin uninstall shannon@shannon-framework
   ```

2. Run local installation:
   ```bash
   ./install_local.sh --install
   ```

3. Restart Claude Code

4. Verify with:
   ```
   /shannon:status
   ```

**Note:** The automatic migration (Option 1) is recommended as it detects and removes potential conflicts.

## Support

**Installation Issues:**
- Check log file: `~/.claude/shannon_install.log`
- Review this guide's Troubleshooting section
- Open issue: https://github.com/shannon-framework/shannon/issues

**Usage Questions:**
- Read command docs: `~/.claude/commands/shannon/*.md`
- Read skill docs: `~/.claude/skills/shannon/*/SKILL.md`
- Consult core files: `~/.claude/core/shannon/*.md`

## License

MIT License - See LICENSE file in repository root.

---

**Shannon Framework v5.4** - Quantitative, Enforced, Production-Ready Development

