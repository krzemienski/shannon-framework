# Shannon Team Setup Guide

Configure Shannon Framework for team and enterprise environments with automatic installation and consistent configuration.

## 📊 Overview

Shannon supports team-wide deployment through Claude Code's repository-level plugin configuration. When configured properly, Shannon automatically installs for all team members who trust the repository.

## 🎯 Benefits

### For Teams
- **Consistent Tooling**: Everyone has same Shannon version
- **Automatic Installation**: No manual setup for each team member
- **Centralized Updates**: Update Shannon once for whole team
- **Reduced Onboarding**: New members get Shannon automatically

### For Enterprises
- **Standardized Workflows**: Company-wide specification-driven development
- **Quality Enforcement**: NO MOCKS philosophy across all projects
- **Context Preservation**: Serena checkpoints prevent knowledge loss
- **Audit Trail**: Wave orchestration provides clear execution records

## 🛠️ Repository-Level Configuration

### Configure Shannon for a Project

Add Shannon to your project's `.claude/settings.json`:

```json
{
  "pluginMarketplaces": [
    "shannon-framework/shannon"
  ],
  "plugins": {
    "shannon@shannon-framework": {
      "enabled": true,
      "autoInstall": true
    }
  }
}
```

**What This Does**:
1. Adds Shannon marketplace to plugin sources
2. Enables Shannon plugin for this project
3. Auto-installs Shannon when team members trust the repository

### Commit Configuration

```bash
# Add settings to repository
git add .claude/settings.json
git commit -m "chore: configure Shannon Framework for team"
git push
```

## 👥 Team Member Setup

### For Each Team Member

**Step 1: Pull Latest Changes**
```bash
git pull origin main
```

**Step 2: Trust Repository** (if not already trusted)
Claude Code will prompt to trust the repository's `.claude/` configuration.

**Step 3: Restart Claude Code**
Shannon plugin auto-installs based on repository configuration.

**Step 4: Verify Installation**
```bash
/sh_status
```

Should show Shannon v3.0.0 active.

### Configure Required MCPs

Each team member must configure MCP servers in their Claude Code settings (this is user-level, not repository-level):

**Serena MCP** (Required):
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

**Recommended MCPs**:
- Sequential MCP (complex analysis)
- Context7 MCP (framework patterns)
- Puppeteer MCP (browser testing)
- shadcn-ui MCP (if building React/Next.js apps)

Run `/sh_check_mcps` for complete configuration guidance.

## 🏢 Enterprise Deployment

### Option 1: Public GitHub Repository

**Setup**:
1. Fork Shannon repository to company GitHub org
2. Customize as needed for company workflows
3. Configure repository plugin settings
4. Team members add: `/plugin marketplace add company-org/shannon`

### Option 2: Private Marketplace

**Setup**:
1. Create private plugin marketplace repository
2. Include Shannon as a plugin
3. Configure company-specific settings
4. Team members add private marketplace

**Structure**:
```
company-plugins/
├── .claude-plugin/
│   └── marketplace.json
└── shannon/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── commands/
    ├── agents/
    └── ...
```

**marketplace.json**:
```json
{
  "name": "company-dev-tools",
  "owner": {
    "name": "Company Engineering",
    "url": "https://github.com/company"
  },
  "plugins": [
    {
      "name": "shannon",
      "source": "./shannon",
      "description": "Company-customized Shannon Framework"
    }
  ]
}
```

### Option 3: Internal NPM Package

For maximum control:
1. Package Shannon as internal NPM module
2. Publish to private npm registry
3. Reference in MCP configuration
4. Centralized version management

## 🔧 Configuration Best Practices

### Version Pinning

Pin Shannon to specific version for stability:

```json
{
  "plugins": {
    "shannon@shannon-framework": {
      "enabled": true,
      "autoInstall": true,
      "version": "3.0.0"
    }
  }
}
```

### Selective Command Enablement

Enable only specific Shannon commands if desired:

```json
{
  "plugins": {
    "shannon@shannon-framework": {
      "enabled": true,
      "disabledCommands": [
        "sh_wave",
        "sh_north_star"
      ]
    }
  }
}
```

### Team MCP Configuration Template

Create a shared MCP configuration template for team:

**File**: `docs/MCP_SETUP_TEMPLATE.md`
```markdown
# Team MCP Server Configuration

Copy this configuration to your Claude Code settings.

## Required for Shannon

### Serena MCP
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

## Recommended for Full Functionality

[Include Sequential, Context7, Puppeteer configurations]
```

## 📊 Rollout Strategy

### Phased Rollout (Recommended for Large Teams)

**Phase 1: Pilot (Week 1)**
- 2-3 team members install Shannon plugin
- Test all workflows
- Document team-specific setup needs
- Create internal FAQ

**Phase 2: Early Adopters (Week 2)**
- 25% of team installs Shannon
- Provide peer support
- Refine configuration based on feedback
- Update team documentation

**Phase 3: General Availability (Week 3+)**
- All remaining team members install
- Repository-level configuration active
- Full team using Shannon
- Monitor for issues

### Big Bang Rollout (For Small Teams)

**Preparation Week**:
- Set up repository configuration
- Test thoroughly with one user
- Schedule migration day
- Send pre-migration instructions

**Migration Day**:
- Morning: Team meeting explaining changes
- Midday: All team members migrate together
- Afternoon: Support session for issues
- End of day: Verify all team members operational

## 🎓 Team Training

### Training Resources to Provide

1. **Quick Start Video** (Record internal demo)
   - Installing Shannon plugin
   - Running first /sh_spec command
   - Understanding 8D complexity output
   - Using wave orchestration

2. **Command Cheat Sheet**
   - Essential commands: /sh_spec, /sh_checkpoint, /sh_status
   - When to use each command
   - Common workflows

3. **Troubleshooting Guide**
   - Common setup issues
   - MCP configuration problems
   - Internal support contacts

### Training Sessions

**Session 1: Shannon Basics (30 min)**
- What is Shannon
- Installation process
- First specification analysis
- Understanding complexity scores

**Session 2: Advanced Features (45 min)**
- Wave orchestration for complex projects
- Context preservation and checkpoints
- NO MOCKS testing philosophy
- Integration with existing workflows

**Session 3: Q&A and Support (30 min)**
- Answer team questions
- Troubleshoot individual setups
- Share best practices

## 📈 Monitoring and Success Metrics

### Track Team Adoption

**Metrics to Monitor**:
- % of team with Shannon installed
- Avg specifications analyzed per week
- Checkpoints created (context preservation usage)
- Wave orchestrations executed
- NO MOCKS test compliance

**Tools**:
- Survey team members
- Check Serena MCP usage patterns
- Review project documentation
- Track specification documents created

### Success Criteria

**Week 1**:
- [ ] 100% of pilot group operational
- [ ] No blocker issues encountered
- [ ] Positive pilot group feedback

**Week 4**:
- [ ] 75%+ of team using Shannon actively
- [ ] MCP configuration issues resolved
- [ ] Team comfortable with core commands

**Week 12**:
- [ ] 90%+ of projects use Shannon for specifications
- [ ] Wave orchestration in regular use
- [ ] Context preservation preventing rework
- [ ] Team satisfaction with Shannon workflows

## 🐛 Team-Level Troubleshooting

### Issue: Inconsistent Shannon Versions

**Symptom**: Team members have different Shannon versions

**Solution**:
1. Pin version in repository settings.json
2. All team members: `/plugin update shannon@shannon-framework`
3. Verify consistent versions: `/sh_status`

### Issue: MCP Configuration Differences

**Symptom**: Shannon works for some team members, not others

**Solution**:
1. Create MCP configuration template (see above)
2. All team members apply same configuration
3. Verify: `/sh_check_mcps` on each machine
4. Document company-specific MCP requirements

### Issue: Repository Trust Required

**Symptom**: Plugin doesn't auto-install for new team members

**Solution**:
1. Ensure `.claude/settings.json` in repository
2. Team member must "trust" repository in Claude Code
3. Restart Claude Code after trusting
4. Plugin should auto-install

## 📞 Support Resources

### Internal Support

**Designate Shannon Champions**:
- 1-2 team members become Shannon experts
- Provide first-line support to team
- Escalate issues to Shannon GitHub if needed

**Create Internal Slack/Chat Channel**:
- #shannon-support or similar
- Quick help for team members
- Share tips and best practices

### External Support

- **GitHub Issues**: https://github.com/shannon-framework/shannon/issues
- **Documentation**: https://github.com/shannon-framework/shannon#readme
- **Community**: (if applicable)

## 🎉 Successful Team Deployment

**Signs of Success**:
- All team members can run `/sh_spec` successfully
- Specification-driven development becomes standard practice
- Context preservation prevents duplicate work
- NO MOCKS testing improves code quality
- Wave orchestration speeds up complex projects
- Team consistently uses Shannon for planning

**Team Benefits Realized**:
- Faster project planning (8D analysis automates estimation)
- Better context continuity (checkpoints prevent knowledge loss)
- Higher quality (NO MOCKS catches integration bugs)
- More efficient execution (wave parallelization)
- Consistent workflows across projects

---

**Questions?** Contact your Shannon team champions or file an issue at GitHub.

**Ready to Roll Out?** Start with pilot group and expand systematically.
