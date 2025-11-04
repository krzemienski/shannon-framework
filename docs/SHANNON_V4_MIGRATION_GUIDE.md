# Shannon Framework V4 - Migration Guide

Guide for migrating from Shannon V3 to V4.

---

## Quick Summary

**Good News:** Shannon V4 maintains 100% backward compatibility with V3.

- ✅ All V3 commands work identically
- ✅ Same arguments and output formats
- ✅ Existing checkpoints remain compatible
- ✅ No breaking changes

**What Changed:**
- Internal architecture (skill-based)
- Enhanced agent system
- Improved MCP integration
- Better error handling

**Migration Time:** < 5 minutes (plugin install)

---

## Migration Steps

### Step 1: Backup (Optional)

```bash
# Export V3 checkpoints (optional precaution)
/sh_memory --list > v3-checkpoints.txt
```

### Step 2: Install V4

```bash
# Uninstall V3 (if installed as plugin)
/plugin uninstall shannon@shannon-framework

# Install V4
/plugin install shannon@shannon-framework

# Restart Claude Code
```

### Step 3: Verify

```bash
# Check version
/sh_status

# Expected output:
# Shannon Framework Status
# Version: 4.0.0
# ...
```

### Step 4: Test Commands

```bash
# Test core commands (should work identically to V3)
/sh_spec "Build test app"
/sh_checkpoint "test"
/sh_restore "test"
/sh_status
```

### Step 5: Check MCPs

```bash
# Verify MCP connections
/sh_check_mcps

# Install any recommended MCPs
```

**Migration Complete!** Your V3 workflows continue to work unchanged.

---

## What's New in V4

### 1. Skill-Based Architecture

**V3:** Monolithic command implementations
**V4:** Modular skills composed by commands

**Impact:** Transparent to users. Commands work identically, but internally use reusable skills.

**Benefits:**
- Better code organization
- Easier maintenance
- Improved testability
- Skill reusability

---

### 2. Enhanced Agent System

**V3:** 5 core agents
**V4:** 19 specialized agents (includes 14 domain agents)

**New Agents:**
- FRONTEND - Frontend development
- BACKEND - Backend services
- DATABASE_ARCHITECT - Database design
- MOBILE_DEVELOPER - Mobile apps
- DEVOPS - Infrastructure
- SECURITY - Security review
- PERFORMANCE - Performance optimization
- QA_ENGINEER - Quality assurance
- DATA_ENGINEER - Data pipelines
- ARCHITECT - System architecture
- PRODUCT_MANAGER - Product strategy
- TECHNICAL_WRITER - Documentation
- API_DESIGNER - API design
- CODE_REVIEWER - Code quality

**Impact:** More specialized expertise, better agent selection

---

### 3. Improved MCP Integration

**V3:** Basic MCP support
**V4:** Enhanced MCP discovery and fallback chains

**New Features:**
- `/sh_check_mcps` command
- Automatic MCP discovery
- Graceful degradation
- Better error messages

**Example:**
```bash
# V4 automatically detects and suggests MCPs
/sh_check_mcps

# Output shows status and installation guidance
Puppeteer MCP: ⚠️  Not available
Install: npm install -g @anthropic/puppeteer-mcp
Benefit: Browser testing for web apps
```

---

### 4. Better Error Handling

**V3:** Generic error messages
**V4:** Specific, actionable error messages with recovery guidance

**Example:**
```bash
# V3 Error:
Error: Checkpoint not found

# V4 Error:
Checkpoint 'my-checkpoint' not found

Available checkpoints:
- wave-1-complete
- feature-auth-complete

Restore with: /sh_restore "<checkpoint-name>"
```

---

## Compatibility Matrix

| Feature | V3 | V4 | Compatible |
|---------|----|----|------------|
| /sh_spec | ✅ | ✅ | ✅ 100% |
| /sh_wave | ✅ | ✅ | ✅ 100% |
| /sh_checkpoint | ✅ | ✅ | ✅ 100% |
| /sh_restore | ✅ | ✅ | ✅ 100% |
| /sh_status | ✅ | ✅ | ✅ 100% |
| /sh_north_star | ✅ | ✅ | ✅ 100% |
| /sh_memory | ✅ | ✅ | ✅ 100% |
| /sh_check_mcps | ❌ | ✅ | N/A (new) |
| /sh_analyze | ❌ | ✅ | N/A (new) |
| /sh_test | ❌ | ✅ | N/A (new) |
| /sh_scaffold | ❌ | ✅ | N/A (new) |
| Checkpoints | ✅ | ✅ | ✅ Cross-version |
| Memory | ✅ | ✅ | ✅ Cross-version |
| Agents | 5 | 19 | ✅ Backward compatible |
| MCP Support | Basic | Enhanced | ✅ Backward compatible |

---

## V3 Workflows in V4

All V3 workflows work unchanged:

### Simple Project (V3 → V4)

```bash
# V3 Workflow
/sh_spec "Build app"
# [implement]

# V4 Workflow (identical)
/sh_spec "Build app"
# [implement]
```

### Complex Project (V3 → V4)

```bash
# V3 Workflow
/sh_spec "Build platform"
/sh_north_star "Launch Q1"
/sh_wave 1
/sh_checkpoint "wave-1"

# V4 Workflow (identical)
/sh_spec "Build platform"
/sh_north_star "Launch Q1"
/sh_wave 1
/sh_checkpoint "wave-1"
```

---

## Using New V4 Features

### MCP Discovery (New in V4)

```bash
# Check MCP status
/sh_check_mcps

# Install recommended MCPs
npm install -g @anthropic/puppeteer-mcp

# Verify
/sh_check_mcps
```

### Functional Testing (New in V4)

```bash
# Generate browser tests
/sh_test --create --platform web --feature "login"

# Generate API tests
/sh_test --create --platform api --feature "users"
```

### Deep Analysis (New in V4)

```bash
# Analyze domains
/sh_analyze --domains

# Analyze dependencies
/sh_analyze --dependencies

# Analyze risks
/sh_analyze --risks
```

### Project Scaffolding (New in V4)

```bash
# Generate React project
/sh_scaffold --framework react

# Generate Express API
/sh_scaffold --framework express
```

---

## Rollback to V3

If you need to rollback (unlikely):

```bash
# Uninstall V4
/plugin uninstall shannon@shannon-framework

# Install V3
/plugin install shannon@shannon-framework --version 3.0.0

# Restart Claude Code

# Verify
/sh_status
# Should show: Version: 3.0.0
```

**Note:** V3 checkpoints work in V4, and V4 checkpoints work in V3.

---

## Common Migration Issues

### Issue: "Command not found"

**Cause:** Plugin not installed correctly

**Solution:**
```bash
/plugin list  # Verify Shannon installed
/plugin install shannon@shannon-framework  # Reinstall if needed
```

---

### Issue: "MCP not connected"

**Cause:** Serena MCP not configured

**Solution:**
```bash
# Check MCP status
/sh_check_mcps

# Follow installation instructions
# Restart Claude Code
```

---

### Issue: "Checkpoint not compatible"

**Cause:** Very unlikely (V4 maintains V3 checkpoint format)

**Solution:**
```bash
# List checkpoints
/sh_memory --list

# Try restore with exact name
/sh_restore "exact-checkpoint-name"

# If still fails, create new checkpoint
/sh_checkpoint "new-baseline"
```

---

### Issue: "Agent not found"

**Cause:** Using V3 agent name not in V4

**Solution:** All V3 agents exist in V4. This shouldn't happen.

---

## Testing Your Migration

### Test Checklist

Run these tests after migration:

```bash
# 1. Version check
/sh_status  # Should show v4.0.0

# 2. Specification analysis
/sh_spec "Build test application with REST API"

# 3. Goal setting
/sh_north_star "Test goal"

# 4. Checkpoint creation
/sh_checkpoint "migration-test"

# 5. Status check
/sh_status

# 6. Restore test
/sh_restore "migration-test"

# 7. MCP check
/sh_check_mcps

# 8. Memory test
/sh_memory --list
```

**All tests should pass without errors.**

---

## FAQ

### Q: Do I need to update my specifications?
**A:** No. V3 specifications work unchanged in V4.

### Q: Will my existing checkpoints work?
**A:** Yes. 100% compatible.

### Q: Can I use V3 and V4 together?
**A:** No. Install one version at a time. But you can switch freely.

### Q: Are there breaking changes?
**A:** No breaking changes. Complete backward compatibility.

### Q: Do I need new MCPs?
**A:** No new MCPs required. But V4 recommends additional MCPs for enhanced features (Puppeteer for testing, Sequential for complex analysis).

### Q: Will my team need training?
**A:** No. If they know V3, they know V4. New commands are optional.

### Q: How long does migration take?
**A:** < 5 minutes (plugin install + verification).

### Q: What's the downtime?
**A:** None. Works immediately after install.

### Q: Can I test V4 without uninstalling V3?
**A:** Yes. Use separate Claude Code instances or test environments.

---

## Migration Support

If you encounter issues:

1. **Check Documentation**
   - User Guide: `SHANNON_V4_USER_GUIDE.md`
   - Command Reference: `SHANNON_V4_COMMAND_REFERENCE.md`
   - Troubleshooting: `SHANNON_V4_TROUBLESHOOTING.md`

2. **Verify Installation**
   ```bash
   /sh_status
   /sh_check_mcps
   ```

3. **Test Core Workflow**
   ```bash
   /sh_spec "Test"
   /sh_checkpoint "test"
   /sh_restore "test"
   ```

4. **Get Help**
   - GitHub Issues: https://github.com/shannon-framework/shannon/issues
   - Documentation: https://shannon-framework.dev/docs
   - Community: https://shannon-framework.dev/community

---

## Next Steps

After successful migration:

1. **Explore New Features**
   - Try `/sh_test` for functional testing
   - Try `/sh_analyze` for deep analysis
   - Try `/sh_scaffold` for project setup

2. **Install Recommended MCPs**
   ```bash
   /sh_check_mcps
   # Follow installation guidance
   ```

3. **Share Feedback**
   - Report any issues
   - Suggest improvements
   - Share success stories

---

**Welcome to Shannon V4!** Enjoy enhanced capabilities with complete backward compatibility.
