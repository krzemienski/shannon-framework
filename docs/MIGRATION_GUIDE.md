# Shannon Migration Guide: CLAUDE.md → Plugin System

Guide for existing Shannon users migrating from the legacy CLAUDE.md configuration to the new plugin architecture.

## 📊 Migration Overview

**What's Changing**: Installation and distribution method
**What's Staying**: All commands, agents, features, and workflows
**Timeline**: 15-30 minutes for complete migration
**Risk**: Low - straightforward process with rollback option

## 🎯 Why Migrate

### Benefits of Plugin Architecture

1. **Easier Installation**
   - Before: Clone repo, configure CLAUDE.md, manual setup
   - After: Two commands - add marketplace, install plugin

2. **Better Discovery**
   - Plugin marketplace makes Shannon discoverable
   - Integrated with Claude Code help system
   - Version management built-in

3. **Simplified Updates**
   - Before: Git pull + manual merges
   - After: `/plugin update shannon@shannon-framework`

4. **Team Distribution**
   - Repository-level plugin configuration
   - Automatic installation for team members
   - Consistent versions across team

5. **No Per-Project Setup**
   - Plugin is user-level, works for all projects
   - No need to configure CLAUDE.md in each project
   - Global Shannon availability

## 📋 Pre-Migration Checklist

### 1. Backup Current Setup
```bash
# Save current Shannon configuration
cp -r /Users/yourname/projects/your-project/.claude/shannon ~/shannon-backup-$(date +%Y%m%d)

# Save CLAUDE.md if you have Shannon references
cp CLAUDE.md CLAUDE.md.backup
```

### 2. Note Current Version
Check what Shannon version you're using:
```bash
grep "version" Shannon/VERSION 2>/dev/null || echo "Unknown"
```

### 3. Document Active Projects
List any projects currently using Shannon:
```bash
find ~/projects -name "CLAUDE.md" -exec grep -l "Shannon" {} \;
```

### 4. Save Any Custom Modifications
If you've customized Shannon files, save your changes:
```bash
git diff Shannon/ > my-shannon-customizations.patch
```

## 🔄 Migration Steps

### Step 1: Remove Old Shannon References

**If using project-level CLAUDE.md with Shannon:**

Edit your project's `.claude/CLAUDE.md` and remove Shannon @-references:

```markdown
# Remove these lines:
@Shannon/Core/SPEC_ANALYSIS.md
@Shannon/Agents/SPEC_ANALYZER.md
# ... and all other Shannon @ references
```

**If Shannon is in your global ~/.claude/ config:**

Edit `~/.claude/CLAUDE.md` and remove Shannon references.

### Step 2: Install Shannon Plugin

Follow the [Plugin Installation Guide](PLUGIN_INSTALL.md):

```bash
# Add marketplace
/plugin marketplace add shannon-framework/shannon

# Install plugin
/plugin install shannon@shannon-framework

# Restart Claude Code
```

### Step 3: Verify Installation

```bash
# Check Shannon status
/sh_status
```

Expected output:
```
🌊 SHANNON FRAMEWORK STATUS
VERSION: v3.0.0
STATUS: ✅ ACTIVE | Installation: Plugin System
```

### Step 4: Configure Required MCPs

```bash
/sh_check_mcps
```

If Serena MCP missing, configure it:
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

Restart Claude Code after adding Serena.

### Step 5: Test Core Functionality

**Test specification analysis**:
```bash
/sh_spec "Build a simple todo app"
```

Expected: 8-dimensional analysis, domain breakdown, phase plan

**Test checkpoint/restore**:
```bash
/sh_checkpoint
```

Expected: Checkpoint saved to Serena MCP

**Test commands appear in help**:
```bash
/help | grep shannon
```

Expected: Shannon commands listed

### Step 6: Clean Up Legacy Shannon

After verifying plugin works:

**Option A: Archive Legacy Shannon**
```bash
# In project directory
mv Shannon/ Shannon-legacy/
echo "DEPRECATED: This is the legacy CLAUDE.md-based Shannon. The active plugin is installed via Claude Code plugin system." > Shannon-legacy/README.md
```

**Option B: Remove Legacy Shannon Entirely**
```bash
# After thorough testing and confidence plugin works
rm -rf Shannon/
```

**Option C: Keep Both Temporarily**
- Keep Shannon/ directory for reference
- Use plugin version for all new work
- Remove when confident (can wait days/weeks)

## ✅ Verification Checklist

After migration, verify:

- [ ] Shannon plugin shows in `/plugin` list as installed and enabled
- [ ] `/sh_status` shows Shannon v3.0.0 active
- [ ] `/sh_check_mcps` shows Serena MCP connected
- [ ] All Shannon commands appear in `/help`
- [ ] All Shannon agents appear in `/agents`
- [ ] `/sh_spec` with test specification works correctly
- [ ] `/sh_checkpoint` saves context to Serena
- [ ] `/sh_restore` retrieves checkpoint
- [ ] Wave orchestration works for complex specs
- [ ] Context preservation functions across sessions

## 🔀 What Changes

### Installation Method
- **Before**: Clone repo, add @-references to CLAUDE.md
- **After**: `/plugin marketplace add` → `/plugin install`

### Command Availability
- **Before**: Commands available only in projects with Shannon configured
- **After**: Commands available globally in all Claude Code sessions

### Help Integration
- **Before**: Shannon commands documented separately
- **After**: Shannon commands in `/help`, integrated with Claude Code

### Agent Discovery
- **Before**: Agents documented in Shannon files
- **After**: Agents in `/agents`, integrated with Claude Code

### Updates
- **Before**: Git pull + merge conflicts + manual updates
- **After**: `/plugin update shannon@shannon-framework` (when available)

## 🔁 What Stays the Same

### Command Names
All command names unchanged:
- `/sh_spec` works exactly as before
- `/sh_checkpoint`, `/sh_restore` work identically
- `/sc_analyze`, `/sc_implement`, etc. function the same

### Command Behavior
- Specification analysis produces same 8D complexity output
- Wave orchestration works identically
- Context preservation uses same Serena MCP
- NO MOCKS testing philosophy unchanged

### Agent Capabilities
- All 19 agents have same specializations
- Auto-activation triggers unchanged
- Agent behavior and outputs identical

### MCP Requirements
- Still requires Serena MCP (mandatory)
- Still recommends Sequential, Context7, Puppeteer
- Still enforces shadcn-ui for React projects

### Context Preservation
- Uses same Serena MCP for checkpoints
- Checkpoint format unchanged
- `/sh_checkpoint` and `/sh_restore` work identically
- Can restore checkpoints from legacy Shannon sessions

## 🚨 Common Migration Issues

### Issue 1: "Command not found: /sh_spec"

**Cause**: Plugin not installed or not loaded

**Solution**:
1. Verify plugin installed: `/plugin` → check Shannon is listed
2. If not installed: `/plugin install shannon@shannon-framework`
3. Restart Claude Code
4. Try command again

### Issue 2: "Serena MCP required"

**Cause**: Serena MCP not configured

**Solution**:
1. Run `/sh_check_mcps` for detailed diagnosis
2. Follow Serena MCP configuration instructions above
3. Restart Claude Code
4. Verify: `/sh_status` shows Serena connected

### Issue 3: Commands work differently

**Cause**: Unlikely - commands should behave identically

**Solution**:
1. Check you're using correct command name
2. Verify MCP servers are configured
3. Check `/sh_status` for framework status
4. Report issue if behavior genuinely different

### Issue 4: Both plugin and legacy Shannon active

**Cause**: Didn't remove @-references from CLAUDE.md

**Solution**:
1. Edit `.claude/CLAUDE.md` or project CLAUDE.md
2. Remove all Shannon @-references
3. Restart Claude Code
4. Only plugin version should be active now

## 📦 Rollback Procedure

If you need to rollback to legacy Shannon:

**Step 1: Disable Plugin**
```bash
/plugin disable shannon@shannon-framework
```

**Step 2: Restore Legacy Configuration**
```bash
# Restore CLAUDE.md backup
cp CLAUDE.md.backup CLAUDE.md

# Restore Shannon directory
cp -r ~/shannon-backup-YYYYMMDD Shannon/
```

**Step 3: Restart Claude Code**

**Step 4: Verify Legacy Active**
Commands should work via old CLAUDE.md system

**Note**: Rollback is safe because plugin and legacy use same Serena MCP for context, so checkpoints are compatible.

## 🤝 Team Migration

If migrating Shannon for a team:

**Step 1: Coordinate Migration**
- Choose migration date
- Notify all team members
- Ensure everyone has Claude Code updated

**Step 2: Test with One User First**
- One team member migrates following this guide
- Verifies everything works
- Documents any team-specific issues

**Step 3: Team Configuration** (Optional)
- Add repository-level plugin configuration
- See [TEAM_SETUP.md](TEAM_SETUP.md) for details

**Step 4: Roll Out to Team**
- All team members follow migration steps
- Support each other during migration
- Verify everyone's Shannon is working

## 📚 Post-Migration Resources

After successful migration:

1. **Learn New Features**: Check [CHANGELOG.md](../CHANGELOG.md) for v3.0.0 additions
2. **Explore Commands**: Browse [SHANNON_COMMANDS_GUIDE.md](../SHANNON_COMMANDS_GUIDE.md)
3. **Configure Team** (if applicable): See [TEAM_SETUP.md](TEAM_SETUP.md)
4. **Report Issues**: Use GitHub Issues for any migration problems

## 🎉 Migration Complete

Once you verify:
- ✅ Plugin installed and active
- ✅ All commands working
- ✅ Serena MCP connected
- ✅ Test specification analysis successful
- ✅ Checkpoint/restore functional

**You're done!** Shannon now operates as a plugin with all the same power and new distribution benefits.

---

**Need Help?** Run `/sh_check_mcps` for configuration assistance or file an issue at https://github.com/shannon-framework/shannon/issues
