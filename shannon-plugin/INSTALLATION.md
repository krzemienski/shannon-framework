# Shannon Framework V4.1 - Installation Guide

**Version**: 4.1.0
**Last Updated**: 2025-11-08

---

## Prerequisites

### Required
- **Claude Code** v1.0.0 or higher
- **Serena MCP Server** - Mandatory for context preservation

### Recommended
- **Sequential MCP** - Enhanced reasoning for complex specifications
- **Context7 MCP** - Framework-specific patterns and documentation
- **Puppeteer MCP** - Real browser automation for functional testing

---

## Installation Methods

### Method 1: Plugin Marketplace (Recommended)

**For Shannon Users** (when published to marketplace):

```bash
# In Claude Code:
/plugin marketplace add shannon-framework/shannon
/plugin install shannon@shannon-framework

# Restart Claude Code
```

### Method 2: Local Plugin Installation

**For Development or Testing**:

```bash
# In Claude Code:
# Add local directory as marketplace
/plugin marketplace add /path/to/shannon-framework

# Install Shannon from local marketplace
/plugin install shannon@shannon

# Restart Claude Code
```

**Example with absolute path**:
```bash
/plugin marketplace add /Users/yourname/projects/shannon-framework
/plugin install shannon@shannon
```

### Method 3: Direct Directory Link (Development)

**For Active Shannon Development**:

```bash
# In Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon@shannon

# After making changes:
/plugin uninstall shannon@shannon
/plugin install shannon@shannon

# Restart Claude Code to load changes
```

---

## Verification

### Step 1: Check Installation

```bash
/sh_status
```

**Expected Output**:
```
🎯 Shannon Framework V4.1.0
Status: ACTIVE
Serena MCP: CONNECTED
Commands: 13 loaded
Skills: 16 loaded
Agents: 19 available
```

### Step 2: Test Core Commands

```bash
# Test specification analysis
/sh_spec "Build a simple web form"

# Test skill discovery (NEW in V4.1)
/sh_discover_skills

# Test session priming (NEW in V4.1)
/shannon:prime --fresh
```

### Step 3: Verify MCP Connections

```bash
/sh_check_mcps
```

**Expected Output**:
```
🔌 MCP Server Status

REQUIRED:
✅ Serena MCP - Connected
   Purpose: Context preservation and checkpointing
   Status: Operational

RECOMMENDED:
✅ Sequential MCP - Connected
   Purpose: Enhanced multi-step reasoning
✅ Context7 MCP - Connected
   Purpose: Framework patterns
⚠️  Puppeteer MCP - Not connected
   Purpose: Browser automation for testing
   Setup: [installation instructions]
```

---

## Configuration

### Serena MCP Setup (Required)

Shannon requires Serena MCP for context preservation. If not configured:

1. **Install Serena MCP**:
   ```bash
   # Follow Serena installation guide
   # Add to Claude Code MCP configuration
   ```

2. **Verify Connection**:
   ```bash
   /sh_check_mcps
   ```

3. **Test Checkpoint**:
   ```bash
   /sh_checkpoint "test"
   /sh_restore "test"
   ```

### Optional MCP Configuration

**Sequential MCP** (Enhanced reasoning):
- Enables deeper analysis for complex specifications
- Required for FORCED_READING_PROTOCOL synthesis steps
- Fallback: Standard Claude reasoning (functional but less thorough)

**Context7 MCP** (Framework patterns):
- Provides framework-specific best practices
- Used by mcp-discovery skill
- Fallback: General recommendations (no framework-specific patterns)

**Puppeteer MCP** (Browser testing):
- Required for NO MOCKS functional browser testing
- Used by functional-testing skill and TEST_GUARDIAN agent
- Fallback: Manual testing guidance (no automated browser tests)

---

## Local Development Setup

### For Shannon Framework Developers

**1. Clone Repository**:
```bash
git clone https://github.com/krzemienski/shannon-framework
cd shannon-framework
```

**2. Install as Local Plugin**:
```bash
# In Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon@shannon
```

**3. Development Workflow**:
```bash
# Edit files in shannon-plugin/
# Examples:
- shannon-plugin/commands/sh_mycommand.md
- shannon-plugin/skills/my-skill/SKILL.md
- shannon-plugin/core/MY_PATTERN.md

# Reinstall to test changes
/plugin uninstall shannon@shannon
/plugin install shannon@shannon

# Restart Claude Code
```

**4. Validation**:
```bash
# Test your changes
/sh_status
/your_new_command

# Verify with Shannon
/sh_discover_skills --refresh  # Should find your new skill
```

---

## Uninstallation

```bash
# In Claude Code:
/plugin uninstall shannon@shannon

# Remove from marketplace (optional):
/plugin marketplace remove shannon
```

---

## Directory Structure After Installation

```
~/.claude/plugins/shannon/     # Installed plugin location
├── .claude-plugin/
│   └── plugin.json
├── commands/                  # 48 slash commands available
├── agents/                    # 26 agents available
├── skills/                    # 16 skills (auto-loaded contextually)
├── core/                      # 9 behavioral patterns (reference)
├── hooks/                     # SessionStart, PreCompact
├── modes/                     # Execution modes
└── templates/                 # Command templates
```

---

## Troubleshooting Installation

### Issue: "Plugin not found"

**Problem**: Marketplace path incorrect

**Solution**:
```bash
# Use absolute path
/plugin marketplace add /Users/yourname/projects/shannon-framework

# Verify marketplace added:
/plugin marketplace list
```

### Issue: "Serena MCP not connected"

**Problem**: Required MCP not configured

**Solution**:
```bash
# Check MCP status
/sh_check_mcps

# Follow Serena installation instructions
# Configure in Claude Code settings
```

### Issue: "Commands not appearing"

**Problem**: Plugin not loaded after installation

**Solution**:
```bash
# Restart Claude Code completely
# Then verify:
/sh_status
```

### Issue: "Changes not reflected"

**Problem**: Plugin cached, needs reinstall

**Solution**:
```bash
/plugin uninstall shannon@shannon
/plugin install shannon@shannon
# Restart Claude Code
```

---

## Next Steps After Installation

1. **Read Plugin README**:
   ```bash
   # Open shannon-plugin/README.md
   ```

2. **Try First Analysis**:
   ```bash
   /sh_spec "Build a REST API with authentication"
   ```

3. **Prime Your Session** (NEW in V4.1):
   ```bash
   /shannon:prime
   ```

4. **Discover Available Skills** (NEW in V4.1):
   ```bash
   /sh_discover_skills
   ```

5. **Set North Star Goal**:
   ```bash
   /sh_north_star "Launch MVP by Q1 2025"
   ```

6. **Read Documentation**:
   - shannon-plugin/README.md - Complete guide
   - shannon-plugin/core/ - Behavioral patterns
   - Root README.md - Quick start

---

## Support

**Issues**: https://github.com/krzemienski/shannon-framework/issues
**Documentation**: shannon-plugin/README.md
**Email**: info@shannon-framework.dev

---

**Shannon Framework V4.1.0** - Installation complete in <2 minutes
