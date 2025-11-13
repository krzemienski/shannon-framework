# Shannon Framework: Hook System Documentation

**Purpose**: Comprehensive guide to Shannon's automatic enforcement system
**Audience**: Shannon developers and advanced users
**Status**: V4.1 Complete Documentation
**Date**: 2025-11-08

---

## Overview

Shannon's hook system provides **automatic enforcement** of Iron Laws through real-time interception of Claude Code execution. Hooks create an "enforcement mesh" that prevents violations BEFORE they occur, not after.

**Core Principle**: Skills DOCUMENT rules → Hooks ENFORCE rules → Agents COMPLY with rules

**Value Proposition**: Impossible to bypass Iron Laws (NO MOCKS, mandatory checkpoints, etc.) even under time pressure or authority demands.

---

## The 6 Shannon Hooks

### Quick Reference Table

| Hook | Event | Purpose | Timeout | Can Fail? | Enforcement Level |
|------|-------|---------|---------|-----------|-------------------|
| **session_start.sh** | SessionStart | Load using-shannon meta-skill | 5s | No | CRITICAL |
| **user_prompt_submit.py** | UserPromptSubmit | Inject North Star goals into prompts | 2s | Yes | HIGH |
| **post_tool_use.py** | PostToolUse (Write/Edit) | Block mock usage in test files | 3s | Yes | CRITICAL |
| **precompact.py** | PreCompact | Emergency checkpoint before auto-compact | 15s | **NO** | CRITICAL |
| **stop.py** | Stop | Validate wave gates before session end | 2s | Yes | MEDIUM |
| **hooks.json** | N/A (config) | Register and configure all hooks | N/A | N/A | N/A |

---

## Hook Lifecycle & Execution Order

### Session Start Sequence

```
1. User opens Claude Code or starts new conversation
   ↓
2. SessionStart event fires
   ↓
3. session_start.sh hook executes (timeout: 5s)
   ↓
4. Hook loads using-shannon meta-skill
   ↓
5. using-shannon establishes Iron Laws:
   - Mandatory 8D analysis before implementation
   - NO MOCKS testing philosophy
   - Wave-based execution for complexity >=0.50
   - Automatic checkpoint protocol
   ↓
6. User sees: <system-reminder>SessionStart hook success</system-reminder>
   ↓
7. Session begins with Iron Laws ACTIVE
```

**Integration Point**: using-shannon skill defines behavioral rules; session_start ensures they're loaded.

---

### During Execution

```
User types message
   ↓
UserPromptSubmit event fires
   ↓
user_prompt_submit.py injects context (timeout: 2s)
   ↓
   Injected content:
   - North Star goal (if set via goal-management)
   - Active wave context (if in wave execution)
   - Shannon framework reminders
   ↓
Claude receives enhanced prompt
   ↓
Claude executes tools (Write/Edit/Read/etc.)
   ↓
PostToolUse event fires (after Write/Edit/MultiEdit)
   ↓
post_tool_use.py scans content (timeout: 3s)
   ↓
   IF test file AND mocks detected:
      → return {"decision": "block", "reason": "..."}
      → Write/Edit BLOCKED
      → User sees violation message
   ELSE:
      → Tool allowed
      → Execution continues
```

**Integration Points**:
- user_prompt_submit.py ↔ goal-management skill (reads North Star goal)
- post_tool_use.py ↔ functional-testing skill (enforces NO MOCKS)

---

### Emergency Checkpoint (PreCompact)

```
Context approaches token limit (e.g., 95% usage)
   ↓
PreCompact event fires (CRITICAL - cannot fail)
   ↓
precompact.py executes (timeout: 15s, continueOnError: false)
   ↓
   Hook generates checkpoint INSTRUCTIONS:
   - "CONTEXT_GUARDIAN: Execute checkpoint sequence"
   - "write_memory('shannon_precompact_checkpoint_[timestamp]', {...})"
   - Template with 11 sections (wave state, todos, decisions, etc.)
   ↓
Instructions injected into system prompt
   ↓
Claude reads instructions and executes:
   1. list_memories() → discover existing memories
   2. write_memory(checkpoint_key, comprehensive_checkpoint_json)
   3. Returns: checkpoint_id for restoration
   ↓
Hook receives confirmation
   ↓
Auto-compaction proceeds (context preserved)
```

**Integration Point**: precompact.py ↔ context-preservation skill (skill defines checkpoint structure, hook triggers it)

**Critical Detail**: Hook generates INSTRUCTIONS, not actual checkpoint. Claude/CONTEXT_GUARDIAN performs the save.

---

### Session End

```
User stops conversation or closes Claude Code
   ↓
Stop event fires
   ↓
stop.py executes (timeout: 2s)
   ↓
   Hook validates:
   - Are we mid-wave? (check for active wave context)
   - Are validation gates satisfied?
   - Any pending critical work?
   ↓
   IF mid-wave without synthesis:
      → Warning: "Wave [N] incomplete - recommend /shannon:checkpoint before exiting"
      → Allow exit (warning only)
   ELSE:
      → Clean exit allowed
```

**Integration Point**: stop.py ↔ wave-orchestration skill (validates wave synthesis protocol)

---

## Detailed Hook Documentation

### 1. session_start.sh

**File**: shannon-plugin/hooks/session_start.sh (425 bytes)
**Event**: SessionStart
**Timeout**: 5000ms (5 seconds)
**Can Fail**: No (critical for Shannon functionality)

**Purpose**: Automatically load using-shannon meta-skill at session start to establish Iron Laws.

**Implementation**:
```bash
#!/bin/bash
# Session start hook - loads using-shannon meta-skill

# Load using-shannon skill into session
echo "Loading Shannon Framework meta-skill..."

# Meta-skill establishes:
# - Mandatory 8D analysis before implementation
# - NO MOCKS testing enforcement
# - Wave execution for complexity >=0.50
# - Checkpoint protocol
# - SITREP for coordination

# Hook output format:
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Shannon Framework initialized. Iron Laws active.",
    "metadata": {
      "skills_loaded": ["using-shannon"],
      "iron_laws_active": true
    }
  }
}
EOF
```

**What Gets Loaded**: using-shannon skill (723 lines)
- 4 baseline violations with counters
- Red flag keyword detection
- Mandatory workflows (analysis → implementation, NO MOCKS, checkpoints)

**User Impact**: Users see `<system-reminder>SessionStart hook success</system-reminder>` confirming Iron Laws are active.

**Failure Mode**: If this hook fails, Shannon Framework doesn't load → No Iron Law enforcement → Users get vanilla Claude behavior.

**Troubleshooting**:
- Check: `echo $CLAUDE_PLUGIN_ROOT` → Should point to shannon-plugin directory
- Check: shannon-plugin/skills/using-shannon/SKILL.md exists
- Verify: Hook timeout (5s) is sufficient for skill loading

---

### 2. post_tool_use.py

**File**: shannon-plugin/hooks/post_tool_use.py (164 lines)
**Event**: PostToolUse (fires after Write, Edit, MultiEdit)
**Matcher**: `Write|Edit|MultiEdit` (only these tools)
**Timeout**: 3000ms (3 seconds)
**Can Fail**: Yes (logs warning, allows tool on error)

**Purpose**: Real-time detection and blocking of mock usage in test files to enforce NO MOCKS Iron Law.

**Algorithm**:
```python
def execute(tool_name, tool_input):
    # 1. Filter tools
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return ALLOW  # Only care about file modifications

    # 2. Extract file path
    file_path = tool_input.get('file_path')
    if not is_test_file(file_path):  # Check for /test/, .test., _test., etc.
        return ALLOW  # Only scan test files

    # 3. Get content
    content = tool_input.get('content') or tool_input.get('new_string')

    # 4. Scan for 13 mock patterns
    violations = detect_mocks(content)
    # Patterns: jest.mock, unittest.mock, @patch, sinon.stub, etc.

    # 5. Block if violations found
    if violations:
        return BLOCK with detailed guidance:
          - What was detected
          - Why mocks are forbidden
          - How to write functional tests instead
          - Puppeteer MCP setup instructions

    return ALLOW  # No violations, proceed
```

**Mock Patterns Detected** (13 total):
```python
- jest.mock()
- jest.spyOn()
- unittest.mock
- @Mock / @Patch decorators
- sinon.stub/mock/fake/spy()
- mockImplementation / mockReturnValue
- vi.mock() (vitest)
- TestDouble
```

**Test File Detection**:
```python
test_indicators = [
    '/test/', '/__tests__/', '/tests/',  # Directory patterns
    '.test.', '.spec.',                   # Extension patterns
    '_test.', '_spec.',                   # Name patterns
    'test_', 'spec_'                      # Prefix patterns
]
```

**Block Response Example**:
```
🚨 Shannon NO MOCKS Violation Detected

**File**: src/__tests__/auth.test.ts
**Violations**: jest.mock(), mockReturnValue

**Shannon Testing Philosophy**: Tests must validate REAL system behavior.

**Required Actions**:
1. Remove all mock usage
2. Implement functional test using Puppeteer MCP (real browser)

**Quick Start**: Run /shannon:check_mcps to verify Puppeteer configured
```

**Integration**:
- Enforces: functional-testing skill's NO MOCKS philosophy
- Works with: TEST_GUARDIAN agent (agent generates compliant tests)
- Blocks: Even WAVE_COORDINATOR agents if they try to write mocks

**Performance**: Regex scanning on every Write/Edit to test files (~10-50ms overhead)

**Troubleshooting**:
- **False positives**: If mock is in comment/string, still detected (intentional - prevents workarounds)
- **Bypass attempts**: Cannot bypass - hook runs BEFORE tool executes
- **Disable**: Remove from hooks.json PostToolUse section (NOT recommended)

---

### 3. precompact.py

**File**: shannon-plugin/hooks/precompact.py (12,583 bytes - largest hook)
**Event**: PreCompact (fires when Claude Code detects context limit approaching)
**Timeout**: 15000ms (15 seconds - longest timeout)
**Can Fail**: **NO** (`continueOnError: false` - MUST succeed)

**Purpose**: Generate checkpoint instructions for CONTEXT_GUARDIAN to preserve ALL session state before auto-compaction.

**Critical Design**: Hook doesn't save directly - it generates INSTRUCTIONS for Claude to execute.

**Why Instructions vs Direct Save**:
- Hook runs in Python subprocess (no direct Serena MCP access)
- Claude has full context + Serena access
- Instructions ensure Claude uses context-preservation skill properly
- Allows skill to evolve without changing hook

**Generated Instructions** (11 sections):
```markdown
# CRITICAL: PreCompact Auto-Checkpoint Required

## CONTEXT_GUARDIAN: Execute Checkpoint Sequence

Step 1: list_memories() → Discover existing memories

Step 2: write_memory("shannon_precompact_checkpoint_{timestamp}", {
    checkpoint_type: "auto_precompact",
    timestamp: "2025-11-08T20:50:00Z",
    serena_memory_keys: [...],          // All existing memories
    active_wave_state: {...},           // Current wave number, phase, progress
    phase_state: {...},                 // Phase 1-5, progress
    project_context: {...},             // North Star goal, focus
    todo_state: {...},                  // TodoWrite state
    decisions_made: [...],              // Architectural decisions
    integration_status: {...},          // Components built
    next_steps: [...],                  // Resume actions
    performance_metrics: {...},         // Execution stats
    conversation_summary: "...",        // 200-500 char summary
})

Step 3: Verify checkpoint saved:
  verify = read_memory("shannon_precompact_checkpoint_{timestamp}")
  if (!verify) ERROR

Step 4: Return checkpoint_id for restoration
```

**Checkpoint Structure** (from lines 141-198):
- 11 comprehensive sections
- Captures wave state, phase progress, todos, decisions
- Enables zero-context-loss restoration

**Integration Flow**:
```
PreCompact event
  ↓
precompact.py generates instructions
  ↓
Instructions injected into system prompt
  ↓
Claude invokes context-preservation skill
  ↓
context-preservation collects all 11 sections
  ↓
Serena MCP write_memory() saves checkpoint
  ↓
Checkpoint verified with read-back test
  ↓
Auto-compaction proceeds safely
```

**Failure Handling**:
- **If Serena MCP unavailable**: Warning logged, instructions still generated (Claude handles gracefully)
- **If hook times out (>15s)**: Compaction aborted, user prompted to resolve
- **If checkpoint save fails**: Claude retries or prompts user

**Troubleshooting**:
- **Logs**: ~/.claude/shannon-logs/precompact/
- **Check Serena**: Verify .serena/ directory exists in project
- **Test**: Manually trigger with /shannon:checkpoint to verify Serena working

**Performance**: Generates instructions in <100ms (checkpoint save by Claude takes 10-30s for comprehensive state)

---

### 4. user_prompt_submit.py

**File**: shannon-plugin/hooks/user_prompt_submit.py (2,182 bytes)
**Event**: UserPromptSubmit (fires before EVERY user message processed)
**Timeout**: 2000ms (2 seconds)
**Can Fail**: Yes (warning logged, prompt proceeds)

**Purpose**: Inject North Star goal and active wave context into every prompt to maintain alignment.

**Injection Strategy**:
```python
def execute(user_prompt):
    # 1. Check if North Star goal exists
    goal = read_serena_goal()  # From goal-management

    # 2. Check if in wave execution
    wave_context = read_active_wave()  # From wave-orchestration

    # 3. Build injection text
    injection = ""

    if goal:
        injection += f"\n**North Star Goal**: {goal['goal_text']}"
        injection += f"\n**Progress**: {goal['progress']}%"

    if wave_context:
        injection += f"\n**Active Wave**: Wave {wave_context['wave_number']}"
        injection += f"\n**Wave Phase**: {wave_context['phase']}"
        injection += f"\n**Wave Objectives**: {wave_context['objectives']}"

    # 4. Inject into user prompt
    enhanced_prompt = f"{injection}\n\n{user_prompt}"

    return enhanced_prompt
```

**What Gets Injected**:
- North Star goal (from goal-management skill)
- Goal progress percentage
- Active wave number and phase
- Wave objectives
- Shannon Framework reminders

**User Impact**: Transparent (users don't see injection, but Claude maintains alignment)

**Integration**:
- goal-management skill → user_prompt_submit.py (reads goal from Serena)
- wave-orchestration skill → user_prompt_submit.py (reads wave state)

**Failure Mode**: If Serena unavailable, hook proceeds without injection (degraded - no alignment enforcement)

**Troubleshooting**:
- Check: Serena MCP connected (`/list_memories` should work)
- Check: Goal exists in Serena (`search_nodes("shannon/goals")`)
- Verify: Injection visible in Claude's understanding of context

---

### 5. stop.py

**File**: shannon-plugin/hooks/stop.py (2,734 bytes)
**Event**: Stop (fires when user ends conversation or closes Claude Code)
**Timeout**: 2000ms (2 seconds)
**Can Fail**: Yes (warning only, exit proceeds)

**Purpose**: Validate wave execution gates and warn if exiting mid-wave without synthesis.

**Validation Logic**:
```python
def execute():
    # 1. Check for active wave
    active_wave = read_serena("active_wave_state")

    if not active_wave:
        return ALLOW  # Not in wave execution, clean exit

    # 2. Check wave phase
    wave_phase = active_wave.get("phase")  # planning|execution|synthesis|complete

    # 3. Validate synthesis complete
    if wave_phase in ["execution", "synthesis"]:
        # Mid-wave or awaiting synthesis - potentially problematic exit
        synthesis_complete = check_serena(f"wave_{wave_number}_complete")

        if not synthesis_complete:
            return WARNING:
                "⚠️  Exiting mid-Wave {wave_number} without synthesis checkpoint

                **Status**: Wave {wave_number} {wave_phase}
                **Risk**: Progress may be lost without wave synthesis

                **Recommended**:
                1. Complete wave synthesis: /shannon:wave_synthesis
                2. OR create manual checkpoint: /shannon:checkpoint
                3. Then exit safely

                **Allow exit anyway?** (Progress may be incomplete)"

    return ALLOW  # Clean exit
```

**Integration**:
- wave-orchestration skill → stop.py (enforces synthesis checkpoint protocol)
- context-preservation skill → stop.py (recommends /shannon:checkpoint)

**User Impact**: Warns before data loss, but doesn't BLOCK exit (user choice)

**Troubleshooting**:
- If false warnings: Check wave state in Serena (may be stale)
- Clear state: Remove active_wave_state from Serena if corrupted

---

### 6. hooks.json

**File**: shannon-plugin/hooks/hooks.json (76 lines)
**Purpose**: Register and configure all 5 executable hooks

**Structure**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "description": "Shannon V4 meta-skill loader",
        "hooks": [{
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/session_start.sh",
          "timeout": 5000
        }]
      }
    ],

    "UserPromptSubmit": [
      {
        "description": "North Star goal injection",
        "hooks": [{
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py",
          "timeout": 2000
        }]
      }
    ],

    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",  // Only fire for these tools
        "description": "NO MOCKS enforcement",
        "hooks": [{
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/post_tool_use.py",
          "timeout": 3000
        }]
      }
    ],

    "PreCompact": [
      {
        "description": "Emergency checkpoint generation",
        "hooks": [{
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/precompact.py",
          "timeout": 15000,
          "continueOnError": false  // MUST succeed
        }]
      }
    ],

    "Stop": [
      {
        "description": "Wave validation gate",
        "hooks": [{
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/stop.py",
          "timeout": 2000
        }]
      }
    ]
  }
}
```

**Configuration Parameters**:
- **type**: "command" (execute shell command)
- **command**: Path to hook script (uses ${CLAUDE_PLUGIN_ROOT} variable)
- **timeout**: Max execution time in milliseconds
- **matcher**: Tool name regex (PostToolUse only)
- **continueOnError**: true (allow failure) or false (MUST succeed)
- **description**: Human-readable purpose

**Adding New Hooks**:
1. Create hook script in shannon-plugin/hooks/
2. Make executable: `chmod +x hooks/my_hook.py`
3. Add entry to hooks.json
4. Test with event trigger
5. Deploy with plugin

**Removing Hooks**:
1. Remove entry from hooks.json
2. Optional: Delete hook script file
3. Restart Claude Code

---

## Hook-Skill Integration Patterns

### Pattern 1: Enforcement Hooks (post_tool_use.py)

**Workflow**:
```
Skill (functional-testing) documents rule:
  → "NO MOCKS: Use real browsers, real databases, real APIs"

Hook (post_tool_use.py) enforces rule:
  → Scans every Write/Edit to test files
  → Blocks if mocks detected
  → Provides remediation guidance

Agent (TEST_GUARDIAN) complies:
  → Generates Puppeteer tests (real browser)
  → Hook allows (no mocks detected)
  → Tests execute successfully
```

**Key**: Skill defines WHAT, Hook prevents VIOLATION, Agent does CORRECT implementation.

---

### Pattern 2: Instruction Hooks (precompact.py)

**Workflow**:
```
Skill (context-preservation) defines checkpoint structure:
  → 11-section comprehensive checkpoint JSON
  → Save to Serena with write_memory()

Hook (precompact.py) triggers skill:
  → Generates instructions referencing skill
  → "Execute context-preservation checkpoint sequence"
  → Provides checkpoint template

Claude executes skill:
  → Reads context-preservation skill
  → Follows checkpoint protocol
  → Saves to Serena
```

**Key**: Hook ORCHESTRATES skill execution (doesn't implement directly).

---

### Pattern 3: Meta-Skill Hooks (session_start.sh)

**Workflow**:
```
Meta-Skill (using-shannon) defines framework rules:
  → Mandatory 8D analysis
  → NO MOCKS philosophy
  → Wave execution thresholds
  → Checkpoint requirements

Hook (session_start.sh) loads meta-skill:
  → Executes at SessionStart
  → Meta-skill establishes behavioral baseline
  → All subsequent interactions subject to rules

Other skills reference meta-skill rules:
  → spec-analysis enforces 8D (references using-shannon)
  → functional-testing enforces NO MOCKS (references using-shannon)
```

**Key**: Meta-skill hook creates behavioral foundation for entire session.

---

## Troubleshooting Guide

### Issue 1: "SessionStart hook didn't load using-shannon"

**Symptoms**:
- No Iron Law enforcement
- Mocks allowed in tests
- No mandatory 8D analysis

**Diagnosis**:
```bash
# Check hook file exists
ls shannon-plugin/hooks/session_start.sh
# Should show: -rwxr-xr-x ... session_start.sh

# Check executable permission
chmod +x shannon-plugin/hooks/session_start.sh

# Check hooks.json registration
grep -A 10 "SessionStart" shannon-plugin/hooks/hooks.json
# Should show session_start.sh command

# Check using-shannon skill exists
ls shannon-plugin/skills/using-shannon/SKILL.md
```

**Resolution**:
1. Verify shannon-plugin installed correctly
2. Check $CLAUDE_PLUGIN_ROOT environment variable
3. Restart Claude Code
4. Manually load: Invoke using-shannon skill

---

### Issue 2: "post_tool_use hook blocking legitimate test code"

**Symptoms**:
- Cannot write test files
- "Mock violation" error but no mocks used
- Words like "mock" in comments triggering false positives

**Diagnosis**:
```bash
# Check what was detected
# Hook shows exact pattern matched (e.g., "jest.mock()")

# Common false positives:
# - "mock" in comments: "// This test doesn't mock..." ← Still detected
# - Variable named "mock": const mock = {...} ← Detected
```

**Resolution**:
```
TRUE VIOLATION (intended block):
  → Remove mock usage, write functional test with Puppeteer

FALSE POSITIVE (legitimate code):
  → Rename variable: mock → testData
  → Rephrase comment: "This test doesn't use test doubles"
  → Move mock-related docs outside test files
```

**Note**: Shannon intentionally has aggressive detection. Better false positive than missed mock.

---

### Issue 3: "PreCompact hook timeout (>15s)"

**Symptoms**:
- Compaction fails with timeout error
- Large checkpoint generation taking too long
- Memory write operations slow

**Diagnosis**:
```bash
# Check Serena MCP performance
time /list_memories
# Should complete <1 second

# Check checkpoint size
# Large projects (100+ waves) may have megabyte checkpoints

# Check Serena backend
# SQLite database may be slow on network drives
```

**Resolution**:
```
SLOW SERENA:
  → Check .serena/ location (should be on fast local disk)
  → Optimize: Move .serena/ to SSD if on network drive

LARGE CHECKPOINT:
  → Expected for complex projects (15s is allocated for this)
  → Consider: Split checkpoints across multiple memories
  → Verify: hook.json timeout = 15000 (not 5000)

TIMEOUT STILL OCCURS:
  → Increase timeout in hooks.json: "timeout": 25000
  → Trade-off: Longer checkpoint time vs guaranteed save
```

---

### Issue 4: "Hooks not firing at all"

**Symptoms**:
- No SessionStart message
- post_tool_use allows mocks
- PreCompact doesn't save checkpoints

**Diagnosis**:
```bash
# Check Claude Code version (hooks require recent version)
# Check plugin installation
ls ~/.claude/plugins/shannon/  # or equivalent

# Check hooks.json parsed correctly
python3 -m json.tool shannon-plugin/hooks/hooks.json
# Should output valid JSON (no errors)

# Check hook scripts executable
ls -l shannon-plugin/hooks/*.py shannon-plugin/hooks/*.sh
# All should have x permission
```

**Resolution**:
1. Reinstall Shannon plugin
2. Verify hooks.json valid JSON
3. Make all hooks executable: `chmod +x shannon-plugin/hooks/*`
4. Restart Claude Code (hooks loaded at startup)

---

## Hook Development Guide

### Creating a New Hook

**Example**: Create `pre_wave_validation.py` hook

**Step 1: Write Hook Script**

```python
#!/usr/bin/env -S python3
"""
Shannon PreWaveValidation Hook - Validate wave readiness

Purpose: Ensure all prerequisites satisfied before wave execution begins
"""

import json
import sys

def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract context
    # (hook-specific logic here)

    # Validation logic
    ready = validate_wave_prerequisites()

    if not ready:
        # Block wave execution
        output = {
            "decision": "block",
            "reason": "Prerequisites not satisfied..."
        }
        print(json.dumps(output))
        sys.exit(0)

    # Allow if ready
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Step 2: Make Executable**

```bash
chmod +x shannon-plugin/hooks/pre_wave_validation.py
```

**Step 3: Register in hooks.json**

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "Wave prerequisite validation",
        "hooks": [{
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/pre_wave_validation.py",
          "timeout": 2000
        }]
      }
    ]
  }
}
```

**Step 4: Test Hook**

```bash
# Create test input
echo '{"user_prompt": "Execute wave 2"}' | python3 hooks/pre_wave_validation.py

# Expected output:
{"decision": "allow"} OR {"decision": "block", "reason": "..."}
```

**Step 5: Document in This README**

Add section under "Detailed Hook Documentation" with:
- Purpose
- Algorithm
- Integration points
- Troubleshooting

---

## Best Practices

### Hook Design Principles

1. **Fail Fast**: Validate early, block before damage occurs
2. **Clear Feedback**: Explain WHY blocked + HOW to fix
3. **Graceful Degradation**: Log errors, don't crash Claude
4. **Performance**: Keep hooks <100ms (exception: PreCompact = 15s allowed)
5. **Single Responsibility**: One hook = one enforcement rule
6. **Integration-Aware**: Reference skills for remediation guidance

### Hook Anti-Patterns

❌ **Silent Failures**: Always log + provide user feedback
❌ **Blocking Critical Hooks**: Only PreCompact should have continueOnError=false
❌ **Complex Logic**: Keep hooks simple - delegate to skills for complex workflows
❌ **Direct Implementation**: Hooks should trigger skills, not reimplement them
❌ **Ignoring Serena Availability**: Check and degrade gracefully if unavailable

### Testing Hooks

**Unit Test**:
```bash
# Test mock detection
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.spec.ts", "content": "jest.mock()"}}' \
  | python3 hooks/post_tool_use.py

# Expected: {"decision": "block", "reason": "..."}
```

**Integration Test**:
1. Install Shannon plugin
2. Create test file with mocks
3. Attempt Write → Should block
4. Remove mocks, retry → Should allow

**End-to-End Test**:
1. Start Claude Code session
2. Verify SessionStart hook loaded using-shannon
3. Write test with mocks → Blocked by post_tool_use
4. Approach context limit → PreCompact fires
5. Exit mid-wave → Stop hook warns

---

## Integration with Shannon Components

### Hooks ↔ Skills

**Bidirectional Relationship**:
```
Skills INFORM hooks:
  → functional-testing documents 13 mock patterns
  → post_tool_use.py implements detection for those patterns

Hooks ENFORCE skills:
  → context-preservation defines checkpoint structure
  → precompact.py ensures checkpoint happens

Hooks TRIGGER skills:
  → session_start.sh loads using-shannon
  → precompact.py generates instructions for context-preservation
```

### Hooks ↔ Agents

**Hooks apply to ALL agents**:
```
WAVE_COORDINATOR spawns TEST_GUARDIAN
  ↓
TEST_GUARDIAN generates test with jest.mock()
  ↓
TEST_GUARDIAN tries Write(test_file, content_with_mocks)
  ↓
post_tool_use.py hook intercepts
  ↓
Hook scans content → Detects jest.mock()
  ↓
Hook BLOCKS Write → TEST_GUARDIAN receives error
  ↓
TEST_GUARDIAN revises → Generates Puppeteer test
  ↓
Retry Write → Hook allows (no mocks) → Success
```

**Key**: Even Shannon specialist agents subject to hook enforcement.

### Hooks ↔ Commands

**Commands don't bypass hooks**:
```
User: /shannon:test
  ↓
Command invokes functional-testing skill
  ↓
Skill generates test code
  ↓
Skill uses Write tool
  ↓
post_tool_use.py hook still fires (same as manual Write)
  ↓
If mocks present → BLOCKED (even from command)
```

**Key**: Hooks operate at TOOL level (below commands/skills).

---

## Performance Impact

| Hook | Overhead | When It Fires | User Impact |
|------|----------|---------------|-------------|
| session_start | ~500ms | Once per session | Negligible (one-time) |
| user_prompt_submit | ~50ms | Every prompt | Transparent (<0.1s) |
| post_tool_use | ~10-50ms | Every Write/Edit to test files | Minimal (regex scan) |
| precompact | ~100ms hook + 10-30s checkpoint | Rare (context limit) | Noticeable but necessary |
| stop | ~100ms | Once per session end | Negligible |

**Total Overhead**: <1 second per session (except PreCompact saves)

**Value**: Prevents hours of rework from mock-based false confidence, context loss, goal drift.

---

## Reference

**Related Skills**:
- using-shannon: Meta-skill loaded by session_start.sh
- functional-testing: NO MOCKS rules enforced by post_tool_use.py
- context-preservation: Checkpoint structure used by precompact.py
- wave-orchestration: Validation gates enforced by stop.py
- goal-management: Goals injected by user_prompt_submit.py

**Hook Logs**:
- Location: ~/.claude/shannon-logs/
- Subdirectories: precompact/, post_tool_use/, session_start/
- Format: JSON logs per execution

**Claude Code Hook Documentation**:
- Official docs: https://docs.claude.com/claude-code/hooks
- Hook events: SessionStart, PreCompact, PostToolUse, Stop, UserPromptSubmit
- Hook API: JSON input/output format

---

## Appendix: Hook Event Reference

### SessionStart
- **When**: New session begins or conversation reset
- **Input**: None
- **Output**: additionalContext (injected into system prompt)
- **Cannot block**: N/A (pre-execution)

### UserPromptSubmit
- **When**: Before EVERY user message processed
- **Input**: `{"user_prompt": "..."}`
- **Output**: Modified prompt OR additional context
- **Cannot block**: Cannot prevent prompt (but can augment)

### PostToolUse
- **When**: After ANY tool execution
- **Input**: `{"tool_name": "...", "tool_input": {...}, "tool_output": {...}}`
- **Output**: `{"decision": "allow"|"block", "reason": "..."}`
- **Can block**: YES (return decision="block")

### PreCompact
- **When**: Claude Code about to auto-compact conversation
- **Input**: `{"trigger": "auto"|"manual", "context_size": ...}`
- **Output**: additionalContext (checkpoint instructions)
- **Cannot block**: Cannot prevent compaction (but can inject instructions)
- **Critical**: continueOnError=false (MUST succeed)

### Stop
- **When**: User ends conversation or closes Claude Code
- **Input**: `{"reason": "user_stop"|"timeout"|"error"}`
- **Output**: Warning message if needed
- **Can block**: Cannot prevent exit (but can warn)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-08
**Shannon Version**: 4.1.0
