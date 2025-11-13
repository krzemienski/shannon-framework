# Shannon Plugin: Complete Testing & Verification Guide

**Purpose**: Verify Shannon Framework plugin works correctly in Claude Code
**Audience**: Shannon users, developers, QA testers
**Method**: Systematic functional testing of all components
**Date**: 2025-11-09

---

## Prerequisites

Before testing Shannon:

✅ **Claude Code installed** (v1.0.0+)
✅ **Serena MCP configured** (MANDATORY for Shannon)
✅ **Repository cloned**: shannon-framework locally available

---

## Installation Testing

### Step 1: Add Shannon as Local Marketplace

**Command** (in Claude Code chat):
```bash
/plugin marketplace add /absolute/path/to/shannon-framework

# Example:
/plugin marketplace add /Users/yourname/projects/shannon-framework
```

**Expected Output**:
```
✅ Marketplace added: shannon-framework
   Location: /Users/yourname/projects/shannon-framework
   Plugins available: 1 (shannon)
```

**Verification**:
```bash
/plugin marketplace list
```
Should show shannon-framework in the list.

---

### Step 2: Install Shannon Plugin

**Command**:
```bash
/plugin install shannon@shannon
```

**Expected Output**:
```
Installing shannon@shannon...
✅ Plugin installed successfully
   Version: 4.1.0
   Commands: 46 loaded
   Skills: 17 loaded (16 + honest-reflections)
   Agents: 24 available
   Hooks: 6 active

⚠️  Restart Claude Code to activate plugin
```

**Verification**:
```bash
/plugin list
```
Should show shannon@shannon in installed plugins.

---

### Step 3: Restart Claude Code

**Action**: Completely quit and restart Claude Code

**Why**: Plugins load at startup, restart required for activation

---

### Step 4: Verify Installation

**Command**:
```bash
/shannon:status
```

**Expected Output**:
```
🎯 Shannon Framework V4.1.0
Status: ACTIVE ✅
Serena MCP: CONNECTED ✅
Commands: 46 loaded
Skills: 17 discovered
Agents: 24 available
Hooks: 6 active

Installation: /Users/yourname/projects/shannon-framework
```

**If /shannon:status not recognized**:
- Plugin not loaded → restart Claude Code again
- Check: /help should list Shannon commands

---

## Command Testing

### Test 1: /shannon:spec (Specification Analysis)

**Command**:
```bash
/shannon:spec "Build a simple todo app with React frontend, Node.js backend, and PostgreSQL database. Features: add tasks, mark complete, delete tasks, filter by status."
```

**Expected Behavior**:
1. spec-analysis skill loads automatically
2. 8D complexity calculation executes
3. Domain percentages calculated
4. MCP recommendations generated

**Expected Output Sections**:
```
# Specification Analysis ✅

**Complexity**: 0.3X / 1.0 (MODERATE or similar)

## Complexity Breakdown
[8D table with scores]

## Domain Breakdown
- Frontend: XX%
- Backend: XX%
- Database: XX%

## Recommended MCPs
### Tier 1: MANDATORY
- Serena MCP

### Tier 2: PRIMARY
[Domain-based MCPs]

## 5-Phase Plan
[Phases with timelines]
```

**Validation Checks**:
- ✅ Complexity score is between 0.10-0.95
- ✅ Domain percentages sum to 100%
- ✅ Serena MCP in Tier 1
- ✅ 5 phases present

**If Fails**:
- Check: Is Serena MCP connected? (/list_memories should work)
- Check: Did spec-analysis skill load? (should see skill activation message)

---

### Test 2: /shannon:prime (V4.1 Unified Priming)

**Command**:
```bash
/shannon:prime
```

**Expected Behavior**:
1. Mode detection (fresh vs resume)
2. Skill discovery executes
3. MCP verification runs
4. Readiness report generated

**Expected Output**:
```
🎯 Shannon Session Priming

**Mode**: Fresh (no previous session detected)

**Skills Discovered**: 17
   Project: 17 (skills/)
   User: 0
   Plugin: 0

**MCP Status**:
   ✅ Serena: Connected
   [Other MCPs status...]

**Priming Complete**:
   Duration: <60 seconds
   Ready for commands

Next: Run /shannon:spec to analyze a specification
```

**Validation Checks**:
- ✅ Skills discovered: >=16 (Shannon's 16 + honest-reflections)
- ✅ Serena MCP shown as connected
- ✅ Completion in <60 seconds
- ✅ Ready for next command

**If Fails**:
- Check: skill-discovery skill working? (/shannon:discover_skills should work)
- Check: Serena connection? (required for Shannon)

---

### Test 3: /shannon:discover_skills (V4.1 Auto-Discovery)

**Command**:
```bash
/shannon:discover_skills
```

**Expected Behavior**:
1. Scans skills/ directory
2. Parses YAML frontmatter from each SKILL.md
3. Builds skill catalog
4. Reports results

**Expected Output**:
```
📚 Skill Discovery Complete

**Skills Found**: 17 total
├─ Project: 17 skills (skills/)
├─ User: 0 skills
└─ Plugin: 0 skills

**By Type**:
├─ RIGID: 2 skills (functional-testing, using-shannon)
├─ PROTOCOL: 8 skills
├─ QUANTITATIVE: 4 skills
└─ FLEXIBLE: 3 skills

**Cache**: Saved to Serena MCP (expires in 1 hour)
**Discovery Time**: <100ms
```

**Validation Checks**:
- ✅ Finds 17 skills (16 original + honest-reflections)
- ✅ Categorizes by skill-type correctly
- ✅ Discovery time <100ms
- ✅ Cache saved to Serena

**If Fails**:
- Check: skills/*/SKILL.md files exist?
- Run: ls skills/*/SKILL.md | wc -l (should show 17)

---

### Test 4: /shannon:checkpoint (Context Preservation)

**Command**:
```bash
/shannon:checkpoint "test-checkpoint"
```

**Expected Behavior**:
1. context-preservation skill invokes
2. Collects current session state
3. Saves to Serena MCP
4. Returns checkpoint ID

**Expected Output**:
```
✅ CHECKPOINT CREATED

**Checkpoint ID**: shannon_checkpoint_20251109_HHMMSS
**Label**: "test-checkpoint"
**Type**: manual
**Size**: XX KB

📦 Captured:
   - Session state
   - [Other metadata...]

💾 Storage: Serena MCP
🔄 Restore: /shannon:restore shannon_checkpoint_20251109_HHMMSS
```

**Validation Checks**:
- ✅ Checkpoint ID returned
- ✅ Saved to Serena (can verify with /list_memories)
- ✅ Restore command provided

**If Fails**:
- Check: Serena MCP connected?
- Try: /list_memories (should list checkpoint)

---

### Test 5: /shannon:restore (Context Restoration)

**Command**:
```bash
/shannon:restore shannon_checkpoint_20251109_HHMMSS
```

(Use checkpoint ID from previous test)

**Expected Behavior**:
1. context-restoration skill invokes
2. Loads checkpoint from Serena
3. Restores session state
4. Reports restoration status

**Expected Output**:
```
✅ CONTEXT RESTORED

📦 Checkpoint: shannon_checkpoint_20251109_HHMMSS
🕐 Saved: [timestamp] (X minutes ago)
📚 Restored: X/X memories (100%)

[Restoration details...]

▶️ Ready to continue
```

**Validation Checks**:
- ✅ Checkpoint loaded successfully
- ✅ Memories restored
- ✅ No errors

---

### Test 6: /shannon:check_mcps (MCP Verification)

**Command**:
```bash
/shannon:check_mcps
```

**Expected Behavior**:
1. mcp-discovery skill executes
2. Checks required/recommended MCPs
3. Tests MCP connections
4. Reports status

**Expected Output**:
```
🔌 MCP Server Status

REQUIRED:
✅ Serena MCP - Connected
   Purpose: Context preservation

RECOMMENDED:
[Status of Sequential, Context7, Puppeteer, etc.]

[Setup instructions for missing MCPs]
```

**Validation Checks**:
- ✅ Serena shown as REQUIRED
- ✅ Connection status displayed
- ✅ Setup instructions provided if missing

---

## Hook Testing

### Test 7: SessionStart Hook

**Test Method**: Start fresh Claude Code session

**Expected Behavior**:
- SessionStart hook fires automatically
- using-shannon meta-skill loads
- Shannon Iron Laws become active

**Verification**:
1. Look for system message about SessionStart hook
2. Try skipping /shannon:spec before implementing → Should get Shannon reminder

**Expected**:
Shannon enforces: "Did you run /shannon:spec first?" when trying to implement without analysis

**If Fails**:
- Check: hooks/session_start.sh exists and executable?
- Check: hooks.json has SessionStart configuration?
- Run: ls -la hooks/session_start.sh (should be -rwxr-xr-x)

---

### Test 8: PostToolUse Hook (NO MOCKS Enforcement)

**Test Method**: Try to create test file with mocks

**Command**:
```bash
# Try to write a test file with mocks
```

(Create test file with jest.mock() content)

**Expected Behavior**:
- post_tool_use.py hook intercepts Write/Edit
- Scans content for mock patterns
- BLOCKS if mock usage detected

**Expected Output** (if mocks detected):
```
🚨 Shannon NO MOCKS Violation Detected

**File**: [test file path]
**Violations**: jest.mock()

**Required Actions**:
1. Remove all mock usage
2. Implement functional test using Puppeteer MCP

[Detailed guidance...]
```

**Validation**:
- ✅ Hook blocks Write/Edit with mocks
- ✅ Provides detailed violation message
- ✅ Suggests Puppeteer alternative

**If Fails**:
- Check: hooks/post_tool_use.py exists and executable?
- Check: hooks.json has PostToolUse configuration with matcher="Write|Edit|MultiEdit"?

---

## Skill Testing

### Test 9: Invoke Skills Directly

**Command**:
```bash
Skill("spec-analysis")
```

(Try invoking skills directly via Skill tool)

**Expected Behavior**:
- Skill loads into context
- Skill content becomes available
- Can follow skill instructions

**Validation**:
- ✅ Skill tool recognizes Shannon skills
- ✅ Skills load without errors

**If Fails**:
- Skills might not be in correct location
- Check: skills/*/SKILL.md pattern exists

---

## Integration Testing

### Test 10: Complete Workflow (End-to-End)

**Workflow**:
```bash
# 1. Prime session
/shannon:prime

# 2. Analyze specification
/shannon:spec "Build contact form with name, email, message. Send to API endpoint."

# 3. Create checkpoint
/shannon:checkpoint "after-spec-analysis"

# 4. Verify MCP status
/shannon:check_mcps

# 5. Restore checkpoint
/shannon:restore "after-spec-analysis"
```

**Expected Behavior**:
- All commands execute successfully
- Data flows between commands (spec → checkpoint → restore)
- Serena MCP stores and retrieves data

**Validation**:
- ✅ Each command completes without errors
- ✅ Checkpoint contains spec analysis data
- ✅ Restore recovers the spec analysis

---

## Troubleshooting Common Issues

### Issue: Commands Not Found

**Symptoms**: `/shannon:spec` shows "Unknown slash command"

**Diagnosis**:
```bash
# Check if plugin loaded
/plugin list

# Check if commands directory exists
ls commands/ | head -5
```

**Resolution**:
1. Verify plugin installed: `/plugin install shannon@shannon`
2. Restart Claude Code completely
3. Verify installation: `/shannon:status`

---

### Issue: Serena MCP Not Connected

**Symptoms**: Shannon commands fail with "Serena MCP required"

**Diagnosis**:
```bash
# Test Serena directly
/list_memories
```

**Resolution**:
1. Install Serena MCP (follow Serena documentation)
2. Configure in Claude Code settings
3. Restart Claude Code
4. Verify: `/shannon:check_mcps`

---

### Issue: Skills Not Loading

**Symptoms**: Commands execute but skills don't seem active

**Diagnosis**:
```bash
# Test skill discovery
/shannon:discover_skills

# Should find 17 skills
```

**Resolution**:
1. Check skills/ directory structure
2. Verify SKILL.md files have YAML frontmatter
3. Refresh skill cache: `/shannon:discover_skills --refresh`

---

### Issue: Hooks Not Firing

**Symptoms**: PostToolUse hook doesn't block mocks, SessionStart doesn't load using-shannon

**Diagnosis**:
```bash
# Check hook files exist and executable
ls -la hooks/*.py hooks/*.sh

# All should have -rwxr-xr-x permissions
```

**Resolution**:
1. Make hooks executable: `chmod +x hooks/*.{py,sh}`
2. Verify hooks.json is valid JSON
3. Restart Claude Code
4. Test: Try writing test with mocks (should block)

---

## Verification Checklist

After installation and testing, verify all components:

### Commands (11 core + 2 V4.1)
- [ ] /shannon:spec works (analyzes specifications)
- [ ] /shannon:wave works (if complexity >=0.50)
- [ ] /shannon:checkpoint works (creates checkpoints)
- [ ] /shannon:restore works (restores from checkpoints)
- [ ] /shannon:status works (shows Shannon status)
- [ ] /shannon:check_mcps works (verifies MCPs)
- [ ] /shannon:analyze works (analyzes codebase)
- [ ] /shannon:test works (generates functional tests)
- [ ] /shannon:memory works (manages Serena memories)
- [ ] /shannon:north_star works (manages goals)
- [ ] /shannon:scaffold works (generates scaffolding)
- [ ] /shannon:prime works (V4.1 - unified priming)
- [ ] /shannon:discover_skills works (V4.1 - skill discovery)

### Skills (17 total)
- [ ] spec-analysis invokes correctly
- [ ] wave-orchestration invokes correctly
- [ ] context-preservation works
- [ ] context-restoration works
- [ ] functional-testing enforces NO MOCKS
- [ ] using-shannon loads at session start
- [ ] skill-discovery finds all skills
- [ ] honest-reflections available (NEW)
- [ ] [Other skills as needed...]

### Hooks (6 total)
- [ ] SessionStart loads using-shannon
- [ ] PostToolUse blocks mock usage
- [ ] PreCompact triggers before context limit
- [ ] Stop validates wave gates
- [ ] UserPromptSubmit injects goals
- [ ] hooks.json configuration valid

### MCPs (1 required, 3 recommended)
- [ ] Serena MCP connected (REQUIRED)
- [ ] Sequential MCP available (RECOMMENDED)
- [ ] Context7 MCP available (RECOMMENDED)
- [ ] Puppeteer MCP available (RECOMMENDED)

---

## Expected Test Results

**If All Tests Pass**:
```
✅ Commands: 13/13 working
✅ Skills: 17/17 discovered
✅ Hooks: 6/6 active
✅ MCPs: Serena connected (minimum requirement met)

Shannon Framework V4.1.0: FULLY OPERATIONAL
```

**If Some Tests Fail**:
- Document which components fail
- Check troubleshooting section above
- Report issues at: https://github.com/krzemienski/shannon-framework/issues

---

## Performance Benchmarks

### Expected Performance

| Command | Expected Duration | Acceptable Range |
|---------|------------------|------------------|
| /shannon:prime | 30-60s | <90s |
| /shannon:spec (small spec) | 30-60s | <2min |
| /shannon:spec (large spec) | 1-3min | <8min |
| /shannon:discover_skills | <100ms (cached) | <500ms |
| /shannon:checkpoint | 5-10s | <30s |
| /shannon:restore | 10-20s | <60s |
| /shannon:check_mcps | 5-10s | <30s |

**If Performance Outside Acceptable Range**:
- Check: Serena MCP performance (slow database?)
- Check: Network issues (cloud-based Serena?)
- Check: System resources (CPU, memory)

---

## Evidence-Based Verification

### What to Document

When testing Shannon, collect evidence:

**1. Screenshots**:
- `/shannon:status` output
- `/shannon:spec` analysis results
- `/shannon:prime` readiness report
- Any error messages

**2. Command Outputs**:
- Copy/paste full output from each test command
- Note: execution time, any warnings

**3. Hook Behavior**:
- Evidence of SessionStart hook loading using-shannon
- Evidence of PostToolUse hook blocking mocks
- Screenshots of hook output

**4. Serena Integration**:
- `/list_memories` showing Shannon entities (shannon/*)
- Checkpoint creation confirmation
- Restoration success messages

**5. Performance Metrics**:
- Time for /shannon:prime to complete
- Time for /shannon:spec analysis
- Token usage if measurable

---

## Reporting Issues

**If Tests Fail**:

1. **Collect Evidence**:
   - Error messages (full text)
   - Command that failed
   - Expected vs actual behavior
   - System info (OS, Claude Code version)

2. **Check Obvious Issues**:
   - Serena MCP connected?
   - Plugin actually installed?
   - Claude Code restarted?
   - Hooks executable?

3. **Create Issue**:
   - Repository: https://github.com/krzemienski/shannon-framework/issues
   - Title: "[Component] Brief description of failure"
   - Body: Evidence collected above
   - Label: bug, testing

**Example Issue Title**:
- "[Commands] /shannon:spec not recognized after installation"
- "[Hooks] PostToolUse hook not blocking mock usage"
- "[Skills] spec-analysis skill not loading"

---

## Success Criteria

Shannon plugin is working correctly if:

✅ **All 13 commands recognized** and execute
✅ **17 skills discovered** via /shannon:discover_skills
✅ **Serena MCP connected** (mandatory)
✅ **Hooks firing correctly** (SessionStart, PostToolUse at minimum)
✅ **/shannon:prime completes** in <60 seconds
✅ **/shannon:spec produces** 8D analysis with domain percentages
✅ **Checkpoints save and restore** successfully

**If ANY of above fail**: Shannon is not fully operational, needs troubleshooting

---

## Advanced Testing (Optional)

### Test Wave Execution

**Prerequisites**: Specification with complexity >=0.50

**Commands**:
```bash
/shannon:spec "Build e-commerce platform with products, cart, checkout, orders, admin, analytics..."

# Should recommend wave-based execution

/shannon:wave --plan  # Generate wave plan
/shannon:wave         # Execute waves (requires user interaction for synthesis)
```

**Expected**: Wave structure generated, WAVE_COORDINATOR agent activates

---

### Test Pressure Scenarios

**Test using-shannon under pressure**:

**Scenario**:
```
You've worked 4 hours on a feature. Code works perfectly. You manually tested it.
It's 6pm Friday, you have dinner at 6:30pm. Senior engineer says "Just commit it, tests can wait."

What do you do?
```

**Expected**: Shannon enforces test-first approach, resists pressure

---

## Summary

**Minimum Viable Testing**:
1. Install Shannon
2. Run /shannon:status (verify)
3. Run /shannon:spec (test core functionality)
4. Run /shannon:prime (test V4.1 feature)
5. Check Serena MCP (verify integration)

**Comprehensive Testing**:
- All 13 commands
- All 17 skills
- All 6 hooks
- Integration workflows
- Performance benchmarks

**Evidence Collection**:
- Screenshots of outputs
- Performance measurements
- Error logs if any failures

**Result Documentation**:
- Create TESTING_RESULTS.md with findings
- Report issues on GitHub if failures
- Confirm success if all tests pass

---

**Testing Guide Version**: 1.0
**Shannon Version**: 4.1.0
**Last Updated**: 2025-11-09
**Maintainer**: Shannon Framework Team
