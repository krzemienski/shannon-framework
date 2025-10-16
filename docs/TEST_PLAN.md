# Shannon Plugin Test Plan

Complete testing procedure for Shannon Framework plugin installation and functionality.

## Test Environment

**Requirements**:
- Claude Code v1.0.0+ installed
- Fresh Claude Code session (restart before testing)
- Serena MCP configured
- Git access to Shannon repository

## ✅ Automated Validation (Completed)

These tests have already passed:

### Level 1: Structure Valid ✅
- JSON files validate (marketplace.json, plugin.json, hooks.json)
- All required directories present
- File counts correct (34 commands, 19 agents, 8 core, 2 modes)
- All agents have capabilities arrays

### Level 2: Plugin Compliant ✅
- Plugin manifest at correct location
- Commands/agents/hooks at plugin root (not in subdirectories)
- Hook script is executable
- Structure meets Claude Code plugin spec

### Level 3: Commands Valid ✅
- All commands have 'description' in frontmatter
- Frontmatter syntax correct
- Command files properly formatted

### Level 4: Agents Valid ✅
- All agents have 'description' in frontmatter
- All agents have 'capabilities' arrays
- Frontmatter syntax correct

## 📋 Manual Testing Required

### Level 5: Functional Testing

These tests require Claude Code session:

#### Test 5.1: Plugin Loading
```bash
# In terminal
cd /Users/nick/Documents/shannon
claude --debug 2>&1 | grep -i shannon
```

**Expected**: No error messages, plugin loads successfully

**Pass Criteria**:
- No "error" or "failed" messages related to Shannon
- Plugin initialization messages appear
- No JSON parsing errors

#### Test 5.2: Marketplace Addition
```bash
# In Claude Code session
/plugin marketplace add /Users/nick/Documents/shannon
```

**Expected**: "✓ Marketplace shannon-framework added successfully"

**Pass Criteria**:
- Marketplace addition succeeds
- No error messages
- Shannon marketplace appears in `/plugin` list

#### Test 5.3: Plugin Installation
```bash
/plugin install shannon@shannon-framework
```

Select "Install now" when prompted.

**Expected**: Installation completes successfully

**Pass Criteria**:
- Installation progress shows
- Completes without errors
- Shannon appears in installed plugins list

#### Test 5.4: Restart Required
Restart Claude Code to load the plugin.

#### Test 5.5: Command Availability
```bash
/help
```

Scroll or search for Shannon commands.

**Expected**: Shannon commands appear

**Pass Criteria**:
- /sh_spec listed
- /sh_checkpoint listed
- /sh_restore listed
- /sh_status listed
- /sh_check_mcps listed
- /sc_analyze listed
- Other Shannon commands present

#### Test 5.6: Agent Availability
```bash
/agents
```

**Expected**: Shannon agents appear

**Pass Criteria**:
- SPEC_ANALYZER listed with description
- WAVE_COORDINATOR listed
- CONTEXT_GUARDIAN listed
- Other Shannon agents present (19 total)

#### Test 5.7: Status Command
```bash
/sh_status
```

**Expected**: Framework status display

**Pass Criteria**:
- Shows Shannon v3.0.0
- Shows "STATUS: ✅ ACTIVE"
- Lists MCP servers (connected or not found)
- Lists commands and agents
- No errors

#### Test 5.8: MCP Check Command
```bash
/sh_check_mcps
```

**Expected**: MCP server verification with setup instructions

**Pass Criteria**:
- Checks all required/recommended MCPs
- Shows Serena status
- Provides setup instructions if MCPs missing
- No errors in command execution

#### Test 5.9: Specification Analysis (Core Functionality)
```bash
/sh_spec "Build a simple todo application with React frontend, Node.js backend, and PostgreSQL database"
```

**Expected**: Complete 8-dimensional analysis

**Pass Criteria**:
- Produces complexity scores across 8 dimensions
- Identifies domains (frontend, backend, database) with percentages
- Recommends MCP servers (shadcn-ui, sequential, context7, etc.)
- Generates 5-phase implementation plan
- Creates comprehensive todo list (20-50 items)
- Provides timeline estimation
- No errors during execution

### Level 6: Integration Testing

#### Test 6.1: Serena MCP Integration
```bash
# After running /sh_spec
/sh_checkpoint
```

**Expected**: Checkpoint saved to Serena

**Pass Criteria**:
- Checkpoint creation succeeds
- Serena MCP responds
- Checkpoint key returned
- No Serena connection errors

#### Test 6.2: Checkpoint Restore
```bash
/sh_restore
```

**Expected**: Most recent checkpoint restored

**Pass Criteria**:
- Locates checkpoint from Serena
- Restores context successfully
- Reports restored memory count
- Shows continuation instructions

#### Test 6.3: Sequential MCP Integration (if available)
Run specification that triggers complex analysis.

**Expected**: Sequential MCP used for reasoning

**Pass Criteria**:
- Complex analysis completes
- Sequential thinking visible in output
- No Sequential MCP errors

#### Test 6.4: Wave Orchestration (Complex Spec)
```bash
/sh_spec "Build enterprise task management system with React frontend, Node.js backend, PostgreSQL database, mobile apps (iOS and Android), real-time WebSocket sync, admin dashboard, reporting engine, SSO authentication, role-based access control, and third-party integrations (Slack, Google Calendar, Jira)"
```

**Expected**: High complexity triggers wave mode

**Pass Criteria**:
- Complexity score ≥0.7
- Wave mode auto-activates
- Multi-stage execution mentioned
- Todo list has 40+ items
- Multiple domains identified

#### Test 6.5: Hook Execution (PreCompact)
This test is difficult to trigger manually. It requires:
- Long session approaching token limit
- Auto-compact triggered

**Alternative Test**: Check hook is registered
```bash
# Check debug output mentions PreCompact hook
claude --debug 2>&1 | grep -i precompact
```

**Pass Criteria**:
- PreCompact hook registered
- hook/precompact.py path correct
- Hook appears in debug output

### Level 7: Documentation Testing

#### Test 7.1: Installation Guide Accuracy
Follow [docs/PLUGIN_INSTALL.md](PLUGIN_INSTALL.md) exactly with a fresh user.

**Pass Criteria**:
- All steps work as documented
- No missing steps
- Instructions clear and complete

#### Test 7.2: Migration Guide Accuracy
If you have legacy Shannon, follow [docs/MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).

**Pass Criteria**:
- Migration completes successfully
- All legacy functionality preserved
- No data loss

#### Test 7.3: Example Accuracy
Test examples in documentation:

```bash
# From PLUGIN_INSTALL.md
/sh_spec "Build a simple todo application with React frontend and Node.js backend"
```

**Pass Criteria**:
- Example produces expected results
- No errors
- Output matches description

## 🎯 Success Criteria Summary

**Required for Release** (Blockers):
- ✅ Level 1: Structure Valid
- ✅ Level 2: Plugin Compliant
- ✅ Level 3: Commands Valid
- ✅ Level 4: Agents Valid
- ⏳ Level 5: Functional Tests (manual - required before release)

**Should Have** (Not blockers):
- ⏳ Level 6: Integration Tests (manual - recommended)
- ✅ Level 7: Documentation (verified during creation)

## 📝 Test Results Template

Record test results:

```markdown
# Shannon v3.0.0 Plugin Test Results

**Tester**: [Your name]
**Date**: [Test date]
**Environment**: Claude Code v[version], macOS [version]

## Automated Tests
- ✅ Level 1: Structure Valid
- ✅ Level 2: Plugin Compliant
- ✅ Level 3: Commands Valid
- ✅ Level 4: Agents Valid

## Manual Tests
- [ ] Level 5.1: Plugin Loading
- [ ] Level 5.2: Marketplace Addition
- [ ] Level 5.3: Plugin Installation
- [ ] Level 5.5: Command Availability
- [ ] Level 5.6: Agent Availability
- [ ] Level 5.7: Status Command
- [ ] Level 5.8: MCP Check Command
- [ ] Level 5.9: Specification Analysis

## Integration Tests
- [ ] Level 6.1: Serena Integration
- [ ] Level 6.2: Checkpoint Restore
- [ ] Level 6.3: Sequential MCP (if available)
- [ ] Level 6.4: Wave Orchestration
- [ ] Level 6.5: Hook Registration

## Documentation Tests
- [ ] Level 7.1: Installation Guide
- [ ] Level 7.3: Example Accuracy

## Issues Found
[List any issues discovered during testing]

## Overall Result
[ ] PASS - Ready for release
[ ] NEEDS WORK - Issues must be fixed first
```

## 🐛 Troubleshooting Test Failures

### Plugin Won't Load
1. Check `claude --debug` output for specific errors
2. Validate JSON files with `jq`
3. Check file permissions
4. Verify directory structure matches spec

### Commands Not Appearing
1. Verify plugin installed: `/plugin`
2. Check plugin enabled
3. Restart Claude Code
4. Check command frontmatter syntax

### Agents Not Listed
1. Check frontmatter has both description and capabilities
2. Verify capabilities is valid YAML array
3. Check agent files are .md format
4. Restart Claude Code

### Functional Tests Fail
1. Check Serena MCP configured: `/sh_check_mcps`
2. Verify MCP tools available
3. Check Claude Code settings
4. Review error messages for specific issues

## 📊 Test Completion Checklist

Before marking tests complete:

- [ ] All automated tests passed (Levels 1-4)
- [ ] Plugin loads without errors in Claude Code
- [ ] All commands accessible via /help
- [ ] All agents visible in /agents
- [ ] /sh_status command works
- [ ] /sh_spec produces analysis
- [ ] Checkpoint/restore functional (if Serena available)
- [ ] Documentation accurate
- [ ] No critical issues found

**If all checklist items pass**: Ready for Wave 6 (Finalize and Release)

**If any items fail**: Fix issues, retest, then proceed

---

**Next Step After Testing**: Create git tag and release (Wave 6)
