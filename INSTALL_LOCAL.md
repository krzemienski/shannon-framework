# Shannon Framework - Local Installation Guide

## Overview

This guide explains how to install Shannon Framework **directly** to your user-level Claude configuration instead of using the plugin system.

### Why Local Installation?

The Claude plugin system doesn't always properly discover plugin components (skills, commands, agents, etc.). Local installation ensures Shannon Framework is **always** accessible by installing directly to `~/.claude/`.

### Key Benefits

1. **Single Installation**: Script ensures only ONE installation exists (removes plugins automatically)
2. **Version Tracking**: Tracks installed version for smart updates
3. **Idempotent**: Safe to run multiple times
4. **Clean Updates**: Automatically handles upgrades from any previous version
5. **Complete Cleanup**: Removes ALL Shannon artifacts when uninstalling

### What Gets Installed

```
~/.claude/
├── skills/shannon/          # 42 skills
├── commands/shannon/        # 23 commands
├── agents/shannon/          # 24 agents
├── core/shannon/            # 10 behavioral patterns
├── modes/shannon/           # 2 execution modes
├── templates/shannon/       # Templates
├── hooks/shannon/           # 5 hook scripts
├── hooks.json               # Hook configuration
└── shannon_version          # Version tracking file
```

## Quick Start

```bash
# Install (or reinstall)
./install_local.sh

# Check status
./install_local.sh --status

# Uninstall everything
./install_local.sh --uninstall
```

## Installation

### Prerequisites

1. **Claude Code** installed
2. **Bash shell** (macOS/Linux)
3. **Serena MCP** configured (MANDATORY for Shannon)

### Installation Options

```bash
./install_local.sh                # Interactive installation (default)
./install_local.sh --install      # Same as above
./install_local.sh --update       # Same as install (unified behavior)
./install_local.sh --status       # Show installation status
./install_local.sh --uninstall    # Remove everything
./install_local.sh --force        # Non-interactive (auto-yes)
./install_local.sh --quiet        # Minimal output
./install_local.sh --help         # Show usage
```

### Step 1: Run Installation Script

From the Shannon Framework repository root:

```bash
./install_local.sh
```

**What the script does:**

1. **Detects existing installations:**
   - Checks for plugin directories
   - Checks marketplace.json entries
   - Checks for local installation

2. **Removes conflicts automatically:**
   - Removes plugin directories (`~/.claude/plugins/shannon*`, `~/.cursor/plugins/shannon*`)
   - Cleans marketplace.json entries
   - Removes old local installation

3. **Installs fresh:**
   - Creates all directories
   - Copies skills, commands, agents, core, modes, templates
   - Installs hooks with proper permissions
   - Creates hooks.json with absolute paths
   - Embeds using-shannon content in session_start.sh
   - Updates all path references
   - Writes version file

4. **Verifies:**
   - Checks all directories exist
   - Validates hook executables
   - Counts installed components

### Step 2: Restart Claude Code

**CRITICAL**: You must completely restart Claude Code for hooks to activate.

1. Quit Claude Code completely
2. Restart Claude Code
3. Open any project

### Step 3: Verify Installation

Check installation status:

```bash
./install_local.sh --status
```

Expected output:
```
═══════════════════════════════════════════════════════════════
  Shannon Framework Installation Status
═══════════════════════════════════════════════════════════════
[SUCCESS] Local installation: v5.6.1
[INFO]   Skills: 42
[INFO]   Commands: 23
[INFO]   Agents: 24
[INFO]   Location: /Users/you/.claude

[INFO] Checking for plugin installations...
[SUCCESS] No plugin installations found

[SUCCESS] ✅ Installation is clean (local only)
```

In Claude Code, run:
```
/shannon:status
```

Expected output:
```
Shannon Framework v5.6.1 active
```

### Step 4: Configure MCP Servers

Shannon requires Serena MCP (mandatory):

```
/shannon:check_mcps
```

Follow instructions to install any missing MCPs.

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

```
/shannon:spec "Build a task management app with React and PostgreSQL"
```

### Executing Tasks

```
/shannon:do "add authentication with Auth0"
```

For complex projects (complexity >= 0.50):

```
/shannon:wave start
```

## Version Management

### Checking Installed Version

```bash
./install_local.sh --status

# Or directly:
cat ~/.claude/shannon_version
```

### Updating to New Version

Simply run install again:

```bash
cd /path/to/shannon-framework
git pull
./install_local.sh
```

The script:
1. Detects existing installation and version
2. Prompts if same version (use `--force` to skip)
3. Removes old installation cleanly
4. Installs new version
5. Updates version file

### Non-Interactive Update

For CI/CD or automation:

```bash
./install_local.sh --install --force
```

## Directory Structure

### Skills (`~/.claude/skills/shannon/`)

42 skills organized by function:

- `spec-analysis/` - 8D complexity analysis
- `wave-orchestration/` - Parallel wave execution
- `functional-testing/` - NO MOCKS enforcement
- `context-preservation/` - Automatic checkpointing
- `mutation-testing/` - Test quality verification
- `security-pattern-detection/` - OWASP scanning
- And 36 more...

### Commands (`~/.claude/commands/shannon/`)

23 commands for Shannon workflows:

- `do.md` - Intelligent task execution
- `spec.md` - 8D complexity analysis
- `wave.md` - Wave-based parallel execution
- `health.md` - Health dashboard (v5.6 NEW)
- And 19 more...

### Agents (`~/.claude/agents/shannon/`)

24 specialized agents with mandatory protocols:

- SITREP reporting
- Context loading from Serena
- NO MOCKS enforcement

### Hooks (`~/.claude/hooks/shannon/`)

5 hook scripts:

| Hook | Purpose |
|------|---------|
| `session_start.sh` | Loads using-shannon meta-skill |
| `user_prompt_submit.py` | Injects North Star goal, auto forced reading |
| `precompact.py` | Saves checkpoint before compaction |
| `post_tool_use.py` | Blocks mock usage in tests |
| `stop.py` | Enforces wave validation gates |

## Troubleshooting

### Check Status First

Always start with:
```bash
./install_local.sh --status
```

### Common Issues

#### Hooks Not Firing

1. Verify hooks.json exists: `cat ~/.claude/hooks.json`
2. Check hook scripts are executable: `ls -l ~/.claude/hooks/shannon/`
3. **Completely restart Claude Code** (quit and reopen)
4. Check installation log: `cat ~/.claude/shannon_install.log`

#### Plugin Still Detected

Run with force to clean everything:
```bash
./install_local.sh --install --force
```

#### Skills Not Found

1. Verify skills installed: `ls ~/.claude/skills/shannon/ | wc -l` (should be 42)
2. Restart Claude Code
3. Try: `/shannon:discover_skills`

#### Version File Missing

Re-run installation:
```bash
./install_local.sh --install --force
```

### Manual Verification

```bash
# Check directories
ls ~/.claude/skills/shannon/
ls ~/.claude/commands/shannon/
ls ~/.claude/agents/shannon/

# Check hooks executable
ls -l ~/.claude/hooks/shannon/

# Check hooks.json
cat ~/.claude/hooks.json | head -20

# Check version
cat ~/.claude/shannon_version
```

## Uninstallation

```bash
./install_local.sh --uninstall
```

**What --uninstall does:**
- ✅ Removes ALL plugin directories
- ✅ Cleans marketplace.json entries
- ✅ Removes ALL local Shannon directories
- ✅ Backs up and removes hooks.json
- ✅ Removes version file
- ✅ Archives installation logs

**Non-interactive:**
```bash
./install_local.sh --uninstall --force
```

**Manual Uninstallation** (if script fails):

```bash
rm -rf ~/.claude/skills/shannon
rm -rf ~/.claude/commands/shannon
rm -rf ~/.claude/agents/shannon
rm -rf ~/.claude/core/shannon
rm -rf ~/.claude/modes/shannon
rm -rf ~/.claude/templates/shannon
rm -rf ~/.claude/hooks/shannon
rm -f ~/.claude/hooks.json
rm -f ~/.claude/shannon_version
```

Then restart Claude Code.

## Migration from Plugin Installation

If you previously installed Shannon as a Claude plugin, the install script handles it automatically:

```bash
./install_local.sh
```

The script will:
1. Detect existing plugin installation
2. Remove plugin directories
3. Clean marketplace.json entries
4. Install local version
5. Display restart instructions

No manual steps needed - the script handles everything.

## Script Details

### Version Tracking

The script maintains `~/.claude/shannon_version`:

```
5.6.1
# Shannon Framework Version File
# Installed: 2025-11-29T10:30:00-08:00
# Source: /Users/nick/Desktop/shannon-framework
# Script: v2.0.0
```

### Locations Checked for Plugins

```
~/.claude/plugins/shannon@shannon-framework
~/.claude/plugins/shannon
~/.cursor/plugins/shannon@shannon-framework
~/.cursor/plugins/shannon
~/.claude/plugins/marketplace.json
~/.cursor/plugins/marketplace.json
```

### Log File

All operations logged to: `~/.claude/shannon_install.log`

## Support

**Installation Issues:**
- Check log file: `~/.claude/shannon_install.log`
- Run status: `./install_local.sh --status`
- Open issue: https://github.com/shannon-framework/shannon/issues

**Usage Questions:**
- Commands: `~/.claude/commands/shannon/*.md`
- Skills: `~/.claude/skills/shannon/*/SKILL.md`
- Core: `~/.claude/core/shannon/*.md`

---

**Shannon Framework v5.6.1** - Quantitative, Enforced, Production-Ready Development
