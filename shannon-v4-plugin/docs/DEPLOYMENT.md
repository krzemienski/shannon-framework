# Shannon Framework v4: Deployment Guide

**Version**: 4.0.0
**Status**: Production Ready
**Deployment Type**: Claude Code Plugin

---

## Deployment Options

### Option 1: Local Development (Recommended for Testing)

```bash
# Clone repository
git clone https://github.com/krzemienski/shannon-framework.git
cd shannon-framework

# Add local marketplace
/plugin marketplace add /absolute/path/to/shannon-framework

# Install Shannon v4
/plugin install shannon-v4@shannon-framework

# Restart Claude Code
```

### Option 2: GitHub Distribution (Recommended for Production)

```bash
# Add GitHub marketplace
/plugin marketplace add https://github.com/krzemienski/shannon-framework

# Install Shannon v4
/plugin install shannon-v4@shannon-framework

# Restart Claude Code
```

### Option 3: NPM Distribution (Future)

```bash
# Not yet implemented - planned for v4.1
npm install -g @shannon-framework/claude-plugin
/plugin install shannon-v4@npm
```

---

## Prerequisites

### Required

1. **Claude Code**: Version 2.0.0 or higher
   ```bash
   claude --version
   ```

2. **Serena MCP** (MANDATORY): Context preservation
   ```bash
   npx @modelcontextprotocol/create-server serena
   ```

### Recommended

3. **Sequential Thinking MCP**: Multi-step reasoning
   ```bash
   npm install -g @modelcontextprotocol/server-sequential
   ```

4. **Puppeteer MCP**: Real browser testing (NO MOCKS)
   ```bash
   npm install -g @modelcontextprotocol/server-puppeteer
   ```

5. **Context7 MCP**: Framework documentation
   ```bash
   npm install -g @modelcontextprotocol/server-context7
   ```

### Project-Specific MCPs (Install as needed)

6. **shadcn-ui MCP**: React component generation (React projects)
7. **Xcode MCP**: iOS build automation (iOS projects)
8. **PostgreSQL/MongoDB/MySQL MCP**: Database operations
9. **AWS/Azure/GCP MCP**: Cloud deployment

---

## Installation Steps

### Step 1: Verify Environment

```bash
# Check Claude Code version
claude --version
# Required: >= 2.0.0

# Check Node.js version (for MCP servers)
node --version
# Required: >= 18.0.0

# Check npm version
npm --version
# Required: >= 9.0.0
```

### Step 2: Install Serena MCP (MANDATORY)

```bash
# Install Serena
npx @modelcontextprotocol/create-server serena

# Configure in Claude Code
# ~/.claude/config.json:
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-serena"]
    }
  }
}

# Test connection
# In Claude Code:
/sh_check_mcps
```

### Step 3: Install Recommended MCPs

```bash
# Sequential Thinking
npm install -g @modelcontextprotocol/server-sequential

# Puppeteer
npm install -g @modelcontextprotocol/server-puppeteer

# Context7
npm install -g @modelcontextprotocol/server-context7

# Configure in ~/.claude/config.json
{
  "mcpServers": {
    "serena": { ... },
    "sequential": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-context7"]
    }
  }
}
```

### Step 4: Install Shannon v4 Plugin

```bash
# Option A: Local development
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon-v4@shannon-framework

# Option B: GitHub
/plugin marketplace add https://github.com/krzemienski/shannon-framework
/plugin install shannon-v4@shannon-framework

# Restart Claude Code (REQUIRED)
```

### Step 5: Verify Installation

```bash
# Check Shannon status
/sh_status

# Expected output:
# ✓ Shannon Framework v4.0.0 active
# ✓ Skills-Based Architecture
# ✓ Progressive Disclosure Enabled
# ✓ Serena MCP: Connected
# ✓ Skills Available: 5+

# Check MCPs
/sh_check_mcps

# Expected output:
# Tier 1 (Mandatory):
#   ✓ Serena MCP - Connected
# Tier 2 (Recommended):
#   ✓ Sequential MCP - Connected
#   ✓ Puppeteer MCP - Connected
#   ✓ Context7 MCP - Connected
```

### Step 6: Quick Start Test

```bash
# Test specification analysis
/sh_spec "Build a simple React todo app with localStorage"

# Expected:
# - 8D complexity analysis
# - Domain detection (Frontend 100%)
# - MCP recommendations (Serena, Puppeteer, Context7)
# - Skill generation (shannon-react-ui)
# - 5-phase plan

# Test checkpoint
/sh_checkpoint "Testing Shannon v4 deployment"

# Expected:
# - State saved to Serena MCP
# - Confirmation message
```

---

## Configuration

### Claude Code Config (~/.claude/config.json)

```json
{
  "plugins": {
    "shannon-v4": {
      "enabled": true,
      "progressive_disclosure": true,
      "skill_auto_generation": true,
      "validation_gates": true
    }
  },
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-serena"],
      "env": {
        "SERENA_STORAGE_PATH": "~/.serena/memories"
      }
    },
    "sequential": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-context7"]
    }
  }
}
```

### Shannon v4 Settings (Optional)

Create `~/.shannon/config.json`:

```json
{
  "version": "4.0.0",
  "features": {
    "progressive_disclosure": true,
    "skill_auto_generation": true,
    "meta_programming": true,
    "validation_gates": true,
    "zero_context_loss": true
  },
  "token_budgets": {
    "session_start": 30000,
    "on_demand_max": 20000
  },
  "skill_generation": {
    "auto": true,
    "tdd_validation": true,
    "framework_specific": true
  },
  "hooks": {
    "prewave": true,
    "postwave": true,
    "quality_gate": true,
    "pre_tool_use": true
  },
  "mcp_tiers": {
    "tier1_mandatory": ["serena"],
    "tier2_recommended": ["sequential", "context7", "puppeteer"],
    "tier3_project_specific": "auto"
  }
}
```

---

## Production Deployment

### Team Environment

```bash
# 1. Install on team CI/CD server
git clone https://github.com/krzemienski/shannon-framework.git
cd shannon-framework

# 2. Install MCPs globally
npm install -g @modelcontextprotocol/server-serena
npm install -g @modelcontextprotocol/server-sequential
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-context7

# 3. Configure shared Serena storage
export SERENA_STORAGE_PATH=/shared/team/serena-memories

# 4. Each developer installs Shannon v4
/plugin marketplace add https://github.com/krzemienski/shannon-framework
/plugin install shannon-v4@shannon-framework
```

### Docker Deployment (Future)

```dockerfile
# Not yet implemented - planned for v4.1
FROM claude-code:latest

# Install MCPs
RUN npm install -g @modelcontextprotocol/server-serena \
                   @modelcontextprotocol/server-sequential \
                   @modelcontextprotocol/server-puppeteer

# Install Shannon v4
RUN /plugin install shannon-v4@shannon-framework

# Configure
COPY config.json ~/.claude/config.json

CMD ["claude-code"]
```

---

## Monitoring & Validation

### Health Checks

```bash
# Shannon status
/sh_status

# MCP connections
/sh_check_mcps

# Skill availability
/sh_list_skills

# Memory status (Serena)
/sh_memory list
```

### Performance Metrics

Track these metrics to validate deployment:

```yaml
Token Efficiency:
  - Session load time: < 5 seconds (v3: ~30 seconds)
  - Session start tokens: ~30K (v3: ~300K)
  - Command activation: < 1 second

Wave Execution:
  - Parallel speedup: 2-4× (same as v3)
  - Context loading: Automated (v3: manual)
  - Validation: Automated (v3: manual)

Skill Generation:
  - Auto-generation time: < 10 seconds
  - Skills per project: 3-8 average
  - Accuracy: 95%+ framework detection
```

### Logs

```bash
# Shannon logs
tail -f ~/.shannon/logs/shannon-v4.log

# Hook execution logs
tail -f ~/.shannon/logs/hooks.log

# MCP connection logs
tail -f ~/.claude/logs/mcp.log
```

---

## Troubleshooting

### Issue: Plugin not loading

**Symptoms**:
- `/sh_status` not recognized
- No Shannon initialization message

**Solution**:
```bash
# Verify plugin installed
/plugin list

# Reinstall
/plugin uninstall shannon-v4@shannon-framework
/plugin install shannon-v4@shannon-framework

# Restart Claude Code (REQUIRED)
```

### Issue: Serena MCP not connected

**Symptoms**:
- `/sh_check_mcps` shows Serena disconnected
- Error: "Serena MCP required"

**Solution**:
```bash
# Test Serena directly
npx @modelcontextprotocol/server-serena

# Check config
cat ~/.claude/config.json

# Verify mcpServers section exists

# Restart Claude Code
```

### Issue: Skills not generating

**Symptoms**:
- `/sh_spec` completes but no skills created
- Skill count = 0

**Solution**:
```bash
# Check spec analysis saved
/sh_memory list
# Look for spec_analysis_* entries

# Manually trigger generation
/sh_generate_skills --from-spec spec_analysis_[timestamp]

# Check logs
tail -f ~/.shannon/logs/skill-generation.log
```

### Issue: Hooks not firing

**Symptoms**:
- PreWave hook not validating
- PostWave hook not collecting results

**Solution**:
```bash
# Check hook permissions
ls -la ~/.claude/plugins/shannon-v4/hooks/*.py
# All should have execute (x) permission

# Make executable
chmod +x ~/.claude/plugins/shannon-v4/hooks/*.py

# Verify hooks.json
cat ~/.claude/plugins/shannon-v4/hooks/hooks.json

# Restart Claude Code
```

---

## Rollback Procedure

If deployment issues occur:

```bash
# 1. Uninstall v4
/plugin uninstall shannon-v4@shannon-framework

# 2. Reinstall v3 (if needed)
/plugin install shannon@shannon-framework

# 3. Restart Claude Code

# 4. Verify v3 working
/sh_status

# Note: Serena memories preserved ✅
```

---

## Upgrade Path

### From v4.0.0 to v4.x.x

```bash
# Update plugin
/plugin update shannon-v4@shannon-framework

# Restart Claude Code

# Verify version
/sh_status
```

### Future Versions

- **v4.1.0**: Priority 2 skills (10 additional skills)
- **v4.2.0**: Enhanced meta-programming
- **v4.3.0**: Advanced validation gates
- **v5.0.0**: Full autonomous mode

---

## Support & Maintenance

### Regular Maintenance

```bash
# Weekly: Update MCPs
npm update -g @modelcontextprotocol/server-serena
npm update -g @modelcontextprotocol/server-sequential

# Monthly: Clean Serena memories
/sh_memory cleanup --older-than 30d

# Quarterly: Review generated skills
/sh_list_skills --usage-stats
```

### Support Channels

- **GitHub Issues**: https://github.com/krzemienski/shannon-framework/issues
- **Documentation**: https://github.com/krzemienski/shannon-framework/docs
- **Community**: Discord (coming soon)

---

## Security Considerations

### MCP Security

```bash
# Serena storage permissions
chmod 700 ~/.serena/memories

# MCP server isolation
# Each MCP runs in separate process

# Network access
# Puppeteer/Playwright: Requires network for real browser testing
# Serena: Local storage only, no network
```

### Hook Security

```bash
# Hooks run with user permissions
# Review hook code before installation:
cat ~/.claude/plugins/shannon-v4/hooks/*.py

# Hooks cannot:
# - Access files outside project directory
# - Make network requests (except via allowed MCPs)
# - Execute arbitrary code
```

---

## Performance Tuning

### Optimize Token Usage

```yaml
# Adjust token budgets in ~/.shannon/config.json
"token_budgets": {
  "session_start": 30000,     # Increase for more upfront loading
  "on_demand_max": 20000      # Increase for larger on-demand chunks
}
```

### Optimize Skill Loading

```yaml
# Disable auto-generation if not needed
"skill_generation": {
  "auto": false,              # Manual skill generation only
  "tdd_validation": true,
  "framework_specific": true
}
```

### Optimize Hook Execution

```yaml
# Disable non-essential hooks
"hooks": {
  "prewave": true,            # Keep (critical)
  "postwave": false,          # Disable if not using wave reports
  "quality_gate": true,       # Keep (critical)
  "pre_tool_use": false       # Disable if not using skill activation hints
}
```

---

## Success Criteria

Deployment is successful when:

✅ `/sh_status` shows Shannon v4.0.0 active
✅ `/sh_check_mcps` shows Serena connected (minimum)
✅ `/sh_spec "test"` completes in < 30 seconds
✅ Skills auto-generate based on spec
✅ Session initialization < 5 seconds
✅ No errors in Shannon logs
✅ Backward compatibility with v3 projects

---

## Deployment Checklist

- [ ] Claude Code >= 2.0.0 installed
- [ ] Node.js >= 18.0.0 installed
- [ ] Serena MCP installed and configured
- [ ] Recommended MCPs installed (Sequential, Puppeteer, Context7)
- [ ] Shannon v4 plugin installed
- [ ] Claude Code restarted
- [ ] `/sh_status` verified
- [ ] `/sh_check_mcps` verified
- [ ] Quick start test completed successfully
- [ ] Team members notified (if team deployment)
- [ ] Documentation distributed

---

**Shannon Framework v4** - Production Ready Deployment 🚀
