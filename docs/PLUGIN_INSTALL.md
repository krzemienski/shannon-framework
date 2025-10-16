# Shannon Plugin Installation Guide

Complete guide to installing Shannon Framework as a Claude Code plugin.

## 📋 Prerequisites

### Required
- **Claude Code** v1.0.0 or higher installed
- **Git** for cloning repository (if installing from source)
- **Serena MCP server** configured in Claude Code

### Recommended
- Sequential MCP server (complex analysis)
- Context7 MCP server (framework patterns)
- Puppeteer MCP server (browser testing)

### Conditional
- shadcn-ui MCP server (React/Next.js projects only - Shannon enforces for React UI)

## 🚀 Installation Methods

### Method 1: From GitHub Marketplace (Recommended)

**Step 1: Add Shannon Marketplace**
```bash
/plugin marketplace add shannon-framework/shannon
```

You should see: "✓ Marketplace shannon-framework added successfully"

**Step 2: Install Shannon Plugin**
```bash
/plugin install shannon@shannon-framework
```

Select "Install now" when prompted.

**Step 3: Restart Claude Code**
Required for plugin to load. Close and restart Claude Code.

**Step 4: Verify Installation**
```bash
/sh_status
```

Expected output:
```
🌊 SHANNON FRAMEWORK STATUS
VERSION: v3.0.0
STATUS: ✅ ACTIVE | Installation: Plugin System
...
```

### Method 2: Local Development Installation

For testing or contributing to Shannon:

**Step 1: Clone Repository**
```bash
cd ~/projects
git clone https://github.com/shannon-framework/shannon.git
cd shannon
```

**Step 2: Add Local Marketplace**
```bash
# In Claude Code
/plugin marketplace add /Users/yourname/projects/shannon
```

**Step 3: Install Plugin**
```bash
/plugin install shannon@shannon
```

**Step 4: Restart Claude Code**

**Step 5: Verify**
```bash
/sh_status
```

## 🔧 MCP Server Configuration

Shannon requires specific MCP servers. Run this command to check configuration:

```bash
/sh_check_mcps
```

### Configure Serena MCP (Required)

Serena MCP is MANDATORY for Shannon to function. It provides context preservation and checkpoint/restore capabilities.

**Installation**:
```bash
npm install -g @modelcontextprotocol/server-serena
```

**Configuration** (add to Claude Code settings):
```json
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-serena"],
      "env": {
        "SERENA_PROJECT_ROOT": "${workspaceFolder}"
      }
    }
  }
}
```

**Restart Claude Code** after adding configuration.

**Verify**:
```bash
/sh_status
```

Should show: `✅ Serena MCP - Connected`

### Configure Recommended MCPs

#### Sequential MCP (Recommended)
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

#### Context7 MCP (Recommended)
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

#### Puppeteer MCP (Recommended for Testing)
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

#### shadcn-ui MCP (Required for React/Next.js)
```json
{
  "mcpServers": {
    "shadcn-ui": {
      "command": "npx",
      "args": ["@jpisnice/shadcn-ui-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

See [docs/SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md) for complete shadcn setup.

## ✅ Post-Installation

### 1. Verify All Commands Available
```bash
/help
```

Look for Shannon commands:
- `/sh_spec`, `/sh_checkpoint`, `/sh_restore`, `/sh_status`, `/sh_check_mcps`
- `/sc_analyze`, `/sc_implement`, `/sc_build`, `/sc_test`, etc.

### 2. Verify Agents Available
```bash
/agents
```

Look for Shannon agents:
- SPEC_ANALYZER, PHASE_ARCHITECT, WAVE_COORDINATOR, CONTEXT_GUARDIAN, TEST_GUARDIAN

### 3. Test Core Functionality

**Try specification analysis**:
```bash
/sh_spec "Build a simple todo application with React frontend and Node.js backend"
```

Expected: Complete analysis with complexity scores, domain breakdown, phase plan, and todo list.

**Try checkpoint/restore**:
```bash
/sh_checkpoint
```
Expected: Checkpoint saved to Serena MCP

### 4. Read Documentation
- Browse [SHANNON_COMMANDS_GUIDE.md](../SHANNON_COMMANDS_GUIDE.md) for command details
- Read [SHANNON_V3_SPECIFICATION.md](../SHANNON_V3_SPECIFICATION.md) for architecture
- Check [Team Setup Guide](TEAM_SETUP.md) if configuring for a team

## 🐛 Troubleshooting

### Plugin Not Loading

**Symptom**: `/sh_status` command not found

**Causes**:
- Plugin not installed
- Claude Code not restarted after installation
- Plugin disabled

**Solutions**:
1. Check plugin status: `/plugin`
2. Verify Shannon is listed and enabled
3. If not installed, reinstall: `/plugin install shannon@shannon-framework`
4. Restart Claude Code

### Commands Not Working

**Symptom**: `/sh_spec` returns error: "Serena MCP required"

**Cause**: Required MCP servers not configured

**Solution**:
1. Run `/sh_check_mcps` for detailed diagnosis
2. Configure Serena MCP per instructions above
3. Restart Claude Code
4. Verify: `/sh_status` shows Serena connected

### MCP Configuration Issues

**Symptom**: MCP servers show as "Not Found" in `/sh_status`

**Solutions**:
1. Verify MCP installed: `npm list -g | grep @modelcontextprotocol`
2. Check Claude Code settings file has correct configuration
3. Restart Claude Code after any settings changes
4. Check Claude Code logs for MCP startup errors

### Agent Not Activating

**Symptom**: Agent doesn't auto-activate when expected

**Solution**:
1. Check agent is loaded: `/agents | grep AGENT_NAME`
2. Try manual activation: Use agent in command context
3. Check activation triggers in agent documentation

### Getting Help

- Run `/sh_status` for framework diagnostics
- Run `/sh_check_mcps` for MCP configuration help
- Check [GitHub Issues](https://github.com/shannon-framework/shannon/issues)
- See [Migration Guide](MIGRATION_GUIDE.md) if upgrading from legacy Shannon

## 📚 Next Steps

1. **Learn Commands**: Browse [SHANNON_COMMANDS_GUIDE.md](../SHANNON_COMMANDS_GUIDE.md)
2. **Try First Spec**: Run `/sh_spec` with a project idea
3. **Explore Agents**: Use `/agents` to see all capabilities
4. **Configure Team** (if needed): See [TEAM_SETUP.md](TEAM_SETUP.md)
5. **Read Specification**: Understand architecture in [SHANNON_V3_SPECIFICATION.md](../SHANNON_V3_SPECIFICATION.md)

## 🔗 Resources

- **Repository**: https://github.com/shannon-framework/shannon
- **Documentation**: https://github.com/shannon-framework/shannon#readme
- **Changelog**: https://github.com/shannon-framework/shannon/blob/main/CHANGELOG.md
- **Issues**: https://github.com/shannon-framework/shannon/issues

---

**Shannon Framework v3.0.0** - Transform specifications into reality
