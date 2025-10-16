# Shannon Plugin - Complete Manual Testing Guide

**Purpose**: Step-by-step instructions for installing and testing Shannon plugin v3.0.1

**Time Required**: 30-45 minutes

**Prerequisites**:
- Claude Code installed
- Terminal access
- This guide open for reference

---

## 🚀 STEP-BY-STEP INSTALLATION TEST

### Step 1: Start Fresh Claude Code Session

```bash
# Open new terminal
cd /Users/nick/Documents/shannon

# Start Claude Code
claude
```

**Expected**: Claude Code starts, shows standard prompt

---

### Step 2: Add Shannon Marketplace

In Claude Code, type:
```bash
/plugin marketplace add /Users/nick/Documents/shannon
```

**Expected Output**:
```
✓ Marketplace added successfully: shannon-framework
```

**If Error**: Check that .claude-plugin/marketplace.json exists and is valid JSON

---

### Step 3: Browse Marketplaces

```bash
/plugin
```

**Expected**:
- Shows shannon-framework in marketplace list
- Shows Shannon plugin available for installation

---

### Step 4: Install Shannon Plugin

```bash
/plugin install shannon@shannon-framework
```

Select "Install now" when prompted.

**Expected**:
```
✓ Shannon plugin installed successfully
Please restart Claude Code to activate the plugin
```

---

### Step 5: Restart Claude Code

Close and restart Claude Code.

**Expected**: On restart, you should see:
```
✓ Shannon Framework v3.0.1 active | Commands: /sh_status | MCP Check: /sh_check_mcps | Docs: /help shannon
```

This is the SessionStart hook notification!

---

## ✅ COMPONENT VERIFICATION TESTS

### Test 6: Verify Commands Available

```bash
/help
```

Scroll or search for "shannon" or look for these commands:

**Shannon Commands (must be present)**:
- [ ] /sh_spec
- [ ] /sh_checkpoint
- [ ] /sh_restore
- [ ] /sh_status
- [ ] /sh_check_mcps
- [ ] /sh_analyze
- [ ] /sh_memory
- [ ] /sh_north_star
- [ ] /sh_wave

**Enhanced SuperClaude Commands (should be present)**:
- [ ] /sc_analyze
- [ ] /sc_implement
- [ ] /sc_build
- [ ] /sc_test
- [ ] (and 20+ more sc_* commands)

**Result**: _____________ commands visible

---

### Test 7: Verify Agents Available

```bash
/agents
```

Look for Shannon agents:

**Shannon Agents (must be present)**:
- [ ] SPEC_ANALYZER
- [ ] PHASE_ARCHITECT
- [ ] WAVE_COORDINATOR
- [ ] CONTEXT_GUARDIAN
- [ ] TEST_GUARDIAN

**Enhanced Agents (should be present)**:
- [ ] ANALYZER
- [ ] ARCHITECT
- [ ] FRONTEND
- [ ] BACKEND
- [ ] (and 10+ more enhanced agents)

**Result**: _____________ agents visible

---

## 🔧 FUNCTIONAL TESTS

### Test 8: Shannon Status Command

```bash
/sh_status
```

**Expected Output**:
```
═══════════════════════════════════════════════════════════════
🌊 SHANNON FRAMEWORK STATUS
═══════════════════════════════════════════════════════════════

VERSION: v3.0.1
STATUS: ✅ ACTIVE | Installation: Plugin System

───────────────────────────────────────────────────────────────
📡 MCP SERVER STATUS
───────────────────────────────────────────────────────────────

REQUIRED:
  [✅ or ❌] Serena MCP       [Connected or Not Found]

RECOMMENDED:
  [Status] Sequential MCP
  [Status] Context7 MCP
  [Status] Puppeteer MCP

... (rest of status output)
```

**Check**:
- [ ] Shows version 3.0.1
- [ ] Shows STATUS: ACTIVE
- [ ] Lists MCP servers
- [ ] Lists commands count
- [ ] Lists agents count
- [ ] No errors

---

### Test 9: MCP Verification Command

```bash
/sh_check_mcps
```

**Expected Output**:
```
═══════════════════════════════════════════════════════════════
🔍 SHANNON MCP SERVER VERIFICATION
═══════════════════════════════════════════════════════════════

🔴 REQUIRED SERVERS
───────────────────────────────────────────────────────────────

[✅ or ❌] Serena MCP - [Status]
   [Setup instructions if missing]

🟡 RECOMMENDED SERVERS
... (recommendations and setup for each)
```

**Check**:
- [ ] Command executes without errors
- [ ] Shows Serena MCP status
- [ ] Shows other MCP statuses
- [ ] Provides setup instructions if any missing

---

### Test 10: Core Specification Analysis

```bash
/sh_spec "Build a task management web application with React frontend, Node.js Express backend, PostgreSQL database, user authentication, real-time updates, and mobile responsive design"
```

**Expected Output** (partial):
```
═══════════════════════════════════════════════════════════════
📊 8-DIMENSIONAL COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════

1. STRUCTURAL COMPLEXITY: [Score 0.0-1.0]
2. COGNITIVE COMPLEXITY: [Score]
3. COORDINATION COMPLEXITY: [Score]
... (8 dimensions)

───────────────────────────────────────────────────────────────
🎯 DOMAIN ANALYSIS
───────────────────────────────────────────────────────────────

Frontend: [X]%
Backend: [Y]%
Database: [Z]%
... (percentages)

───────────────────────────────────────────────────────────────
📡 MCP SERVER RECOMMENDATIONS
... (suggests shadcn-ui, sequential, context7, etc.)

───────────────────────────────────────────────────────────────
📋 5-PHASE IMPLEMENTATION PLAN
... (detailed phases)

───────────────────────────────────────────────────────────────
✅ TODO LIST (20-50 items)
... (comprehensive tasks)
```

**Check**:
- [ ] Produces 8-dimensional scores
- [ ] Shows domain breakdown with percentages
- [ ] Recommends MCP servers
- [ ] Generates 5-phase plan
- [ ] Creates 20+ todo items
- [ ] Provides timeline estimate
- [ ] No errors during execution

---

## 🎯 NORTH STAR TESTING

### Test 11: Set North Star Goal

```bash
# Create North Star file
mkdir -p .serena
echo "Build the most intuitive and powerful task management tool for developers" > .serena/north_star.txt
```

**Expected**: File created successfully

---

### Test 12: Test North Star Injection (UserPromptSubmit Hook)

Now submit ANY prompt (this tests if UserPromptSubmit hook is working):

```bash
# Just type any message to Claude
"What should I implement first?"
```

**Expected**: BEFORE Claude responds, you should see:
```
🎯 **North Star Goal**: Build the most intuitive and powerful task management tool for developers
**Context**: All work must align with this overarching goal.
---
```

**Check**:
- [ ] North Star appears before Claude's response
- [ ] Goal text matches what you wrote
- [ ] UserPromptSubmit hook is working!

If you DON'T see this, the UserPromptSubmit hook isn't firing properly.

---

## 🪝 HOOK TESTING

### Test 13: Test NO MOCKS Detection (PostToolUse Hook)

Try to create a test file with mocks:

```bash
# Ask Claude to create a test with mocks
"Create a test file test.spec.js with jest.mock() in it"
```

**Expected**: Claude should be BLOCKED with message:
```
🚨 Shannon NO MOCKS Violation Detected

File: test.spec.js
Violations: jest.mock()

Shannon Testing Philosophy: Tests must validate REAL system behavior...
[Provides functional test alternative]
```

**Check**:
- [ ] File creation is blocked
- [ ] Clear error message shown
- [ ] Functional test alternative provided
- [ ] PostToolUse hook is working!

If test file IS created with mocks, the hook isn't working.

---

### Test 14: Test Wave Validation (Stop Hook)

This is harder to test. You need to:
1. Create file: `.serena/wave_validation_pending`
2. Put some text in it: "Wave 2 - Backend Implementation"
3. Ask Claude something that would make it stop
4. Check if it's blocked from finishing

**Expected**: Claude is blocked with:
```
⚠️ Shannon Wave Validation Required

Wave 2 - Backend Implementation

Required Actions:
1. Present wave synthesis to user
2. Request explicit approval
...
```

**Check**:
- [ ] Claude blocked from stopping
- [ ] Shows wave validation required
- [ ] Stop hook is working!

---

### Test 15: Check Hook Registration (Debug Mode)

Restart Claude Code with debug flag:

```bash
claude --debug 2>&1 | grep -i "hook\|shannon"
```

**Expected Output** (look for):
```
Loading plugin: shannon
Registering hook: UserPromptSubmit
Registering hook: PreCompact
Registering hook: PostToolUse
Registering hook: Stop
Registering hook: SessionStart
```

**Check**:
- [ ] Plugin loads without errors
- [ ] All 5 hooks register
- [ ] No "hook failed" messages
- [ ] Hook paths use ${CLAUDE_PLUGIN_ROOT} correctly

---

## 🔌 MCP INTEGRATION TESTS

### Test 16: Check Serena MCP Availability

In this Claude Code session, try:

```bash
# This should work if Serena MCP is configured
"List my Serena memories"
```

Claude should be able to call `list_memories()` if Serena is available.

**Or check directly**:
Look at available tools - if you see tools starting with `mcp__serena__`, Serena is available.

**Check**:
- [ ] Serena MCP is configured
- [ ] Can list memories
- [ ] Can write memories
- [ ] Shannon can use Serena for checkpoints

---

### Test 17: Test Checkpoint Creation

```bash
/sh_checkpoint
```

**Expected**:
```
✅ CHECKPOINT SAVED: precompact_checkpoint_20241016_HHMMSS

Checkpoint Details:
- Created: [timestamp]
- Memory Keys: [count] preserved
...
```

**Check**:
- [ ] Checkpoint created successfully
- [ ] Returns checkpoint key
- [ ] Uses Serena MCP
- [ ] No errors

---

### Test 18: Test Checkpoint Restore

```bash
/sh_restore
```

**Expected**:
```
✅ CONTEXT RESTORED: [checkpoint_key]

Restored Context:
- Memories: X loaded
- Project: [name]
...
```

**Check**:
- [ ] Finds most recent checkpoint
- [ ] Restores successfully
- [ ] Shows restored memory count
- [ ] No errors

---

## 📊 COMPREHENSIVE TEST RESULTS

After completing all tests, fill out:

### Installation Tests
- [ ] Marketplace addition: PASS / FAIL
- [ ] Plugin installation: PASS / FAIL
- [ ] Plugin loads on restart: PASS / FAIL

### Component Tests
- [ ] Commands visible (____/34): PASS / FAIL
- [ ] Agents visible (____/19): PASS / FAIL
- [ ] Hooks registered (____/5): PASS / FAIL

### Functional Tests
- [ ] /sh_status works: PASS / FAIL
- [ ] /sh_check_mcps works: PASS / FAIL
- [ ] /sh_spec produces 8D analysis: PASS / FAIL

### Hook Tests
- [ ] SessionStart notification: PASS / FAIL
- [ ] UserPromptSubmit (North Star): PASS / FAIL
- [ ] PostToolUse (NO MOCKS): PASS / FAIL
- [ ] Stop (validation gates): PASS / FAIL
- [ ] PreCompact (checkpoint): PASS / FAIL

### MCP Tests
- [ ] Serena MCP available: YES / NO
- [ ] Sequential MCP available: YES / NO
- [ ] Context7 MCP available: YES / NO
- [ ] Puppeteer MCP available: YES / NO

---

## 🐛 Troubleshooting

### Plugin Won't Install
1. Check JSON valid: `jq . .claude-plugin/marketplace.json`
2. Check path correct: `ls shannon-plugin/.claude-plugin/plugin.json`
3. Try: `claude --debug` and look for error messages

### Commands Don't Appear
1. Verify plugin installed: Look for Shannon in plugin list
2. Check plugin enabled (not disabled)
3. Restart Claude Code
4. Check `claude --debug` for loading errors

### Hooks Don't Fire
1. Check scripts executable: `ls -la shannon-plugin/hooks/*.py`
2. Test scripts manually: `python3 shannon-plugin/hooks/user_prompt_submit.py`
3. Check hook paths in hooks.json use ${CLAUDE_PLUGIN_ROOT}
4. Review debug output for hook execution logs

### MCPs Not Detected
1. Check Claude Code settings for MCP configuration
2. Run: `claude --debug` and look for MCP server startup
3. Verify MCP packages installed: `npm list -g | grep mcp`

---

## 📝 AFTER TESTING - REPORT RESULTS

Create file: `ACTUAL_TEST_RESULTS.md` with your findings:

```markdown
# Shannon v3.0.1 Actual Test Results

**Tester**: [Your name]
**Date**: [Date]
**Environment**: Claude Code v[version]

## Summary
- Installation: [PASS/FAIL]
- Commands: [X/34 working]
- Agents: [X/19 available]
- Hooks: [X/5 working]
- MCP Integration: [Status]

## Issues Found
1. [Any issues]
2. [Problems encountered]

## Recommendations
1. [Fixes needed]
2. [Improvements suggested]
```

---

**This guide ensures systematic testing of every Shannon component!**
