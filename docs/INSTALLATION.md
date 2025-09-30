# Shannon V3 Installation Guide

Complete installation and setup guide for Shannon V3 Context Engineering Framework.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Verification](#verification)
4. [Configuration](#configuration)
5. [Uninstallation](#uninstallation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

Shannon V3 requires the following software to be installed:

#### 1. Claude Code

- **Version**: Latest stable release
- **Installation**: Download from [Anthropic](https://www.anthropic.com)
- **Purpose**: AI assistant that reads Shannon's behavioral instructions

#### 2. Python

- **Version**: Python 3.8 or higher
- **Verification**: Run `python3 --version` or `python --version`
- **Installation**:
  - macOS: `brew install python3`
  - Linux: `sudo apt-get install python3` or `sudo yum install python3`
  - Windows: Download from [python.org](https://www.python.org)

#### 3. pip (Python Package Manager)

- **Version**: Latest (usually included with Python)
- **Verification**: Run `pip --version` or `pip3 --version`
- **Upgrade**: `python3 -m pip install --upgrade pip`

### Recommended MCP Servers

Shannon V3 works best with these MCP servers. While optional, they unlock Shannon's full capabilities:

#### 1. Serena MCP (Required for Full Features)

- **Purpose**: Project memory, session persistence, cross-wave context sharing
- **Installation**: Follow [Serena MCP documentation](https://github.com/serena-mcp/serena)
- **Critical for**: Context preservation, wave orchestration, checkpoint/restore

#### 2. Sequential MCP (Highly Recommended)

- **Purpose**: Complex multi-step reasoning and analysis
- **Installation**: Follow [Sequential MCP documentation](https://github.com/sequential-mcp/sequential)
- **Used for**: Spec analysis, architectural planning, systematic debugging

#### 3. Context7 MCP (Recommended)

- **Purpose**: Official library documentation and framework patterns
- **Installation**: Follow [Context7 documentation](https://context7.ai)
- **Used for**: Technical documentation, best practices, framework integration

#### 4. Additional MCP Servers

- **Magic**: UI component generation from 21st.dev patterns
- **Morphllm**: Pattern-based code transformations
- **Playwright**: Browser automation and E2E testing
- **Tavily**: Web search and research capabilities

### System Requirements

- **Operating System**: macOS, Linux, or Windows
- **Disk Space**: ~50MB for Shannon files
- **Claude Code Configuration Directory**: `~/.claude/` must be writable

---

## Installation

### Step 1: Install Shannon Framework

Install Shannon V3 using pip:

```bash
# Install from PyPI (when published)
pip install Shannon-Framework

# Or install from source
git clone https://github.com/shannon-framework/Shannon-Framework.git
cd Shannon-Framework
pip install -e .
```

### Step 2: Run Shannon Installer

Execute the Shannon installation command:

```bash
Shannon install
```

**What This Does**:
1. Creates `~/.claude/` directory if it doesn't exist
2. Copies 60+ markdown behavioral instruction files to `~/.claude/`
3. Installs PreCompact hook to `~/.claude/hooks/precompact.py`
4. Sets up command patterns, agent definitions, and mode files
5. Configures core behavioral patterns

### Step 3: Expected Output

You should see output similar to:

```
Shannon V3 Installation
=======================

✓ Checking prerequisites...
  ✓ Python 3.9.7 detected
  ✓ Claude Code configuration directory found: ~/.claude/
  ✓ Write permissions verified

✓ Installing Shannon components...
  ✓ Core patterns (11 files)
  ✓ Commands (29 files)
  ✓ Agents (19 files)
  ✓ Modes (9 files)
  ✓ MCP configurations (8 files)
  ✓ PreCompact hook (1 file)

✓ Verifying installation...
  ✓ All files present and readable
  ✓ Hook script executable

Installation complete! 🎉

Next steps:
1. Restart Claude Code to load Shannon framework
2. Run verification: Shannon verify
3. Try your first command: /sh:analyze-spec
```

### Step 4: Restart Claude Code

**Important**: Restart Claude Code to load the Shannon framework.

- **macOS/Linux**: Quit and relaunch Claude Code application
- **Windows**: Exit and restart Claude Code application

---

## Verification

### Automatic Verification

Run Shannon's built-in verification:

```bash
Shannon verify
```

Expected output:

```
Shannon V3 Verification
=======================

✓ Checking installation...
  ✓ ~/.claude/ directory exists
  ✓ Core patterns: 11/11 files present
  ✓ Commands: 29/29 files present
  ✓ Agents: 19/19 files present
  ✓ Modes: 9/9 files present
  ✓ MCP configs: 8/8 files present
  ✓ PreCompact hook: installed and executable

✓ Checking file integrity...
  ✓ All markdown files have valid frontmatter
  ✓ All files are readable by Claude Code
  ✓ No syntax errors detected

✓ Checking MCP servers...
  ✓ Serena MCP: connected
  ⚠ Sequential MCP: not configured (recommended)
  ⚠ Context7 MCP: not configured (optional)

Verification complete!
Status: READY TO USE
```

### Manual Verification

#### 1. Check Directory Structure

```bash
ls -la ~/.claude/
```

Expected structure:

```
~/.claude/
├── commands/           # 29 command files
├── agents/             # 19 agent definition files
├── modes/              # 9 mode files
├── hooks/              # 1 hook script
│   └── precompact.py
├── SPEC_ANALYSIS.md    # Core pattern files
├── PHASE_PLANNING.md
├── WAVE_ORCHESTRATION.md
├── CONTEXT_MANAGEMENT.md
├── TESTING_PHILOSOPHY.md
├── HOOK_SYSTEM.md
├── PROJECT_MEMORY.md
├── MCP_DISCOVERY.md
└── [other core files]
```

#### 2. Verify PreCompact Hook

```bash
# Check hook exists and is executable
ls -la ~/.claude/hooks/precompact.py

# Expected output:
# -rwxr-xr-x  1 user  staff  3456 Jan 15 10:30 precompact.py
```

#### 3. Test in Claude Code

Open Claude Code and try a Shannon command:

```
/sh:help
```

**Expected Behavior**: Claude should respond with Shannon V3 command reference.

If you see a list of Shannon commands, installation is successful!

---

## Configuration

### settings.json Setup

Shannon's PreCompact hook requires registration in Claude Code's settings.json.

#### 1. Locate settings.json

**File Location**:
- **macOS**: `~/Library/Application Support/Claude/settings.json`
- **Linux**: `~/.config/Claude/settings.json`
- **Windows**: `%APPDATA%\Claude\settings.json`

#### 2. Register PreCompact Hook

Add or modify the `hooks` section in settings.json:

```json
{
  "hooks": {
    "preCompact": {
      "command": "python3",
      "args": ["~/.claude/hooks/precompact.py"],
      "enabled": true
    }
  }
}
```

**Important Notes**:
- Use full path to `precompact.py` (expand `~` to actual home directory if needed)
- Ensure `python3` is in your PATH, or use full path (e.g., `/usr/bin/python3`)
- Set `"enabled": true` to activate the hook

#### 3. Verify Hook Registration

Restart Claude Code and check that:
1. No error messages appear on startup
2. Hook executes when context gets full (you'll see preservation messages)

### MCP Server Configuration

Configure recommended MCP servers in Claude Code settings:

```json
{
  "mcpServers": {
    "serena": {
      "url": "http://localhost:PORT",
      "enabled": true
    },
    "sequential": {
      "url": "http://localhost:PORT",
      "enabled": true
    },
    "context7": {
      "url": "http://localhost:PORT",
      "enabled": true
    }
  }
}
```

Replace PORT with actual MCP server ports from their documentation.

---

## Uninstallation

### Complete Removal

To completely remove Shannon V3:

```bash
Shannon uninstall
```

**What This Does**:
1. Removes all Shannon files from `~/.claude/`
2. Removes PreCompact hook from `~/.claude/hooks/`
3. Leaves Claude Code configuration untouched
4. Creates backup at `~/.shannon-backup-[timestamp]/`

### Manual Uninstallation

If the uninstaller fails, remove manually:

```bash
# Remove Shannon files
rm -rf ~/.claude/commands/
rm -rf ~/.claude/agents/
rm -rf ~/.claude/modes/
rm -rf ~/.claude/hooks/precompact.py
rm ~/.claude/SPEC_ANALYSIS.md
rm ~/.claude/PHASE_PLANNING.md
rm ~/.claude/WAVE_ORCHESTRATION.md
rm ~/.claude/CONTEXT_MANAGEMENT.md
rm ~/.claude/TESTING_PHILOSOPHY.md
rm ~/.claude/HOOK_SYSTEM.md
rm ~/.claude/PROJECT_MEMORY.md
rm ~/.claude/MCP_DISCOVERY.md

# Remove Shannon package
pip uninstall Shannon-Framework
```

### Unregister PreCompact Hook

Edit `settings.json` and remove the `preCompact` hook section:

```json
{
  "hooks": {
    // Remove this entire section
  }
}
```

---

## Troubleshooting

### Installation Issues

#### Issue: "Permission Denied" Error

**Symptom**: Cannot write to `~/.claude/` directory

**Solution**:
```bash
# Create directory with proper permissions
mkdir -p ~/.claude/
chmod 755 ~/.claude/

# Re-run installer
Shannon install
```

#### Issue: "Python Not Found" Error

**Symptom**: `python3: command not found`

**Solution**:
```bash
# Check Python installation
which python3

# If not found, install Python
# macOS:
brew install python3

# Linux:
sudo apt-get install python3
```

#### Issue: "pip install" Fails

**Symptom**: Cannot install Shannon-Framework package

**Solution**:
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Try alternative installation
pip install --user Shannon-Framework

# Or install from source
git clone https://github.com/shannon-framework/Shannon-Framework.git
cd Shannon-Framework
pip install -e .
```

### Verification Issues

#### Issue: Shannon Commands Not Working

**Symptom**: `/sh:` commands not recognized in Claude Code

**Checklist**:
1. ✓ Verify installation: `Shannon verify`
2. ✓ Check files exist: `ls ~/.claude/commands/`
3. ✓ Restart Claude Code completely
4. ✓ Try `/sh:help` to test basic functionality

#### Issue: PreCompact Hook Not Working

**Symptom**: Context loss occurs despite hook installation

**Checklist**:
1. ✓ Verify hook exists: `ls -la ~/.claude/hooks/precompact.py`
2. ✓ Check hook is executable: `chmod +x ~/.claude/hooks/precompact.py`
3. ✓ Verify settings.json registration (see Configuration section)
4. ✓ Check Python path in settings.json is correct
5. ✓ Restart Claude Code after settings changes

**Test Hook Manually**:
```bash
# Test hook script
echo '{"trigger":"auto"}' | python3 ~/.claude/hooks/precompact.py

# Expected: JSON output with hookSpecificOutput
```

#### Issue: Serena MCP Not Connected

**Symptom**: Wave orchestration features don't work

**Solution**:
1. Verify Serena MCP is installed and running
2. Check Serena MCP configuration in Claude Code settings
3. Test Serena connection: `Shannon check-mcp serena`
4. Review Serena MCP logs for connection errors

### Runtime Issues

#### Issue: Spec Analysis Doesn't Trigger

**Symptom**: `/sh:analyze-spec` doesn't provide 8-dimensional analysis

**Solution**:
1. Verify SPEC_ANALYSIS.md exists: `cat ~/.claude/SPEC_ANALYSIS.md | head`
2. Check file permissions: `ls -la ~/.claude/SPEC_ANALYSIS.md`
3. Restart Claude Code
4. Try explicit analysis: `/sh:analyze-spec "Build a web app..."`

#### Issue: Sub-Agents Don't Activate

**Symptom**: No parallel sub-agent execution

**Checklist**:
1. ✓ Verify complexity threshold met (≥0.5 for most agents)
2. ✓ Check agent files exist: `ls ~/.claude/agents/`
3. ✓ Ensure Serena MCP connected (required for wave orchestration)
4. ✓ Review spec analysis output for agent suggestions

#### Issue: Context Loss Despite PreCompact Hook

**Symptom**: Losing context even with hook installed

**Diagnosis**:
```bash
# Check hook logs in Claude Code
# Look for: "PreCompact hook executed"

# Verify Serena checkpoints exist
# In Claude Code, run: list_memories()
# Should see: shannon_precompact_checkpoint_*
```

**Solution**:
1. Verify hook registered in settings.json
2. Check Python path is correct in settings.json
3. Test hook manually (see above)
4. Ensure Serena MCP is running and accessible

### Platform-Specific Issues

#### macOS Issues

**Issue**: Permission denied for hook script

**Solution**:
```bash
chmod +x ~/.claude/hooks/precompact.py
xattr -d com.apple.quarantine ~/.claude/hooks/precompact.py
```

#### Linux Issues

**Issue**: Python path incorrect in settings.json

**Solution**:
```bash
# Find Python path
which python3

# Update settings.json with full path
# Example: /usr/bin/python3
```

#### Windows Issues

**Issue**: Backslashes in paths cause errors

**Solution**: Use forward slashes in settings.json paths:
```json
{
  "hooks": {
    "preCompact": {
      "command": "C:/Users/YourName/AppData/Local/Programs/Python/Python39/python.exe",
      "args": ["C:/Users/YourName/.claude/hooks/precompact.py"]
    }
  }
}
```

### Getting Help

If issues persist:

1. **Check Documentation**: Review [User Guide](./USER_GUIDE.md)
2. **GitHub Issues**: Report bugs at [Shannon Framework GitHub](https://github.com/shannon-framework/Shannon-Framework/issues)
3. **Community Discord**: Join Shannon community for support
4. **Debug Mode**: Run `Shannon verify --debug` for detailed diagnostics

---

## Next Steps

After successful installation:

1. **Quick Start**: See [Quick Start Guide](./QUICK_START.md)
2. **First Project**: Try [First Project Tutorial](./FIRST_PROJECT.md)
3. **Command Reference**: Browse [Command Reference](./COMMANDS.md)
4. **User Guide**: Read complete [User Guide](./USER_GUIDE.md)

---

**Installation complete!** 🎉

Shannon V3 is now ready to transform your Claude Code experience.