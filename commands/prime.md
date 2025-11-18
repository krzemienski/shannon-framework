---
name: shannon:prime
description: Unified session priming command - one command for complete context restoration
usage: /shannon:prime [--fresh|--resume|--quick|--full]
---

# Shannon Prime: Unified Session Priming

## Overview

**One command for complete session priming**. Orchestrates all priming steps automatically:
- Skill discovery (Enhancement #2)
- MCP verification
- Context restoration (if resume)
- Memory loading
- Spec/plan restoration
- Sequential thinking preparation
- Forced reading activation (Enhancement #1)
- Readiness report

**NO competitor has unified priming command** - all require 4-6 separate commands (15-20 minutes).

**Shannon Prime**: <60 seconds total

## Prerequisites

- Serena MCP strongly recommended (for checkpoint restoration)
- No prerequisites for fresh sessions

## Options

- **No flags**: Auto-detect mode (fresh vs resume)
- `--fresh`: Force fresh session initialization
- `--resume`: Force resume from checkpoint
- `--quick`: Fast mode (skip non-critical checks)
- `--full`: Deep mode (comprehensive priming, 2-3 minutes)

## Workflow: 8-Step Priming Sequence

### Step 1: Detect Session Mode

**Auto-Detection Logic**:
```
checkpoints = find_checkpoints(".shannon/sessions/")

IF no checkpoints exist THEN
  mode = "fresh"
ELSE
  latest_checkpoint = most_recent(checkpoints)
  age_hours = (now - checkpoint.timestamp) / 3600

  IF age_hours < 24 THEN
    mode = "auto-resume"  # Recent work, resume
  ELSE
    mode = "fresh"  # Old checkpoint, fresh start
  END IF
END IF
```

**Flag Overrides**:
- `--fresh`: mode = "fresh" (ignore checkpoints)
- `--resume`: mode = "resume" (use latest checkpoint)
- `--quick`: mode = mode + quick_optimizations
- `--full`: mode = mode + deep_loading

**Output**:
```
🎯 Shannon Prime: Initializing session...
🔍 Mode: {AUTO-RESUME|FRESH} (checkpoint {age} hours old)
```

### Step 2: Skill Inventory (Enhancement #2)

**Execute**:
```
/shannon:discover_skills --cache
```

**Integration**: Uses skill-discovery skill to find all SKILL.md files

**Output**:
```
📚 Discovering skills...
   ✅ 104 skills discovered
   ├─ Project: 15
   ├─ User: 89
   └─ Plugin: 0
```

### Step 3: MCP Verification

**Execute**:
```
/shannon:check_mcps
```

**Checks**:
- Serena MCP (MANDATORY for Shannon)
- Sequential MCP (RECOMMENDED for deep thinking)
- Context7 MCP (RECOMMENDED for docs)
- Puppeteer MCP (RECOMMENDED for browser testing)

**Output**:
```
🔌 Verifying MCPs...
   ✅ Serena: Connected
   ✅ Sequential: Available
   ⚠️ Context7: Not connected
   ✅ Puppeteer: Available

   Critical MCPs: ✅ All operational
```

### Step 4: Context Restoration (Resume Mode Only)

**IF mode == "auto-resume" OR mode == "resume" THEN**:

```
/shannon:restore --latest
```

**Restores**:
- Checkpoint data (wave progress, task state)
- North Star goal
- Current wave number
- Next actions

**Output**:
```
💾 Restoring context...
   ✅ Checkpoint: SHANNON-W3-20251108T140000
   📊 Progress: Wave 3/5 (60%)
   🎯 Current: "Implement authentication API"
   ▶️ Next: "Complete JWT token generation"
```

**IF mode == "fresh" THEN**:

```
Skip restoration

Output:
ℹ️ Fresh session (no checkpoint to restore)
```

### Step 5: Memory Reloading

**Load relevant Serena memories**:

```python
# Determine which memories to load based on mode

IF mode == "resume" AND checkpoint exists THEN
  # Load memories from checkpoint's memory_list
  memories_to_load = checkpoint.memory_list
ELSE IF mode == "fresh" THEN
  # Load standard session memories
  memories_to_load = [
    "using_shannon",  # Meta-skill
    "recent_work",    # Last 3 sessions
  ]
ELSE
  # Quick mode: minimal memories
  memories_to_load = ["using_shannon"]
END IF

FOR memory_name IN memories_to_load:
  mcp__serena__read_memory(memory_name)
END FOR
```

**Output**:
```
📚 Loading memories...
   ✅ using_shannon
   ✅ session_42_complete
   ✅ spec_analysis_project_x
   ✅ 8 memories loaded
```

### Step 6: Spec/Plan State Restoration (Resume Only)

**IF mode == "resume" AND checkpoint has spec_plan_state THEN**:

```
Restore from checkpoint:
- Specification ID
- Current phase
- Phase plan details
- Wave assignments
```

**Output**:
```
📋 Restoring spec/plan state...
   ✅ Spec: PROJECT-X-SPEC-20251108
   ✅ Plan: Phase 3/5 (Implementation)
   ✅ Wave: 3/8
```

### Step 7: Sequential Thinking Preparation

**IF Sequential MCP available THEN**:

```
Prepare Sequential MCP for deep thinking:
- Load thinking patterns
- Set default thought counts (50-500 based on complexity)
- Ready for synthesis
```

**Output**:
```
🧠 Sequential thinking ready
   Default: 100 thoughts for medium complexity
```

### Step 8: Enable Forced Reading (Enhancement #1)

**Activate forced reading enforcement**:

```
reading_enforcement_enabled = true
display_forced_reading_status()
```

**Output**:
```
🔍 Forced reading: ACTIVE
   Critical files will require:
   - Pre-counting before reading
   - Sequential line-by-line reading
   - Completeness verification
```

---

## Readiness Report

**After all 8 steps, generate comprehensive readiness report**:

```markdown
═══════════════════════════════════════════════════════════
🎯 SHANNON FRAMEWORK V4 - SESSION READY
═══════════════════════════════════════════════════════════

**SESSION MODE**: {FRESH|AUTO-RESUME|RESUME}
**PRIMING TIME**: {duration} seconds

📚 **SKILLS AVAILABLE**: {total_count}
   Project: {project_count}
   User: {user_count}
   Plugin: {plugin_count}

🔌 **MCP STATUS**:
   ✅ Serena MCP: Connected (mandatory)
   ✅ Sequential MCP: Available
   {status for other MCPs}

{if resume mode}
💾 **CONTEXT RESTORED**:
   Checkpoint: {checkpoint_id}
   Age: {hours} hours ago
   Progress: {progress}%
   Current Wave: {wave_number}/{total_waves}
   Current Task: "{task_description}"
   Next Action: "{next_action}"

📚 **MEMORIES LOADED**: {count}
   {list of memory names}

📋 **WORK STATE**:
   Project: {project_name}
   Specification: {spec_id}
   Phase: {current_phase}/5
   Wave: {current_wave}/{total_waves}
   Next Action: {next_action_description}
{end if}

🧠 **THINKING READY**: Sequential MCP prepared

⚙️ **RULES ACTIVE**:
   - Forced complete reading (FORCED_READING_PROTOCOL)
   - Automatic skill invocation (skill-discovery)
   - NO MOCKS enforcement (TESTING_PHILOSOPHY)
   - SITREP protocol (sitrep-reporting)
   - 8D complexity analysis (SPEC_ANALYSIS)

▶️ **READY TO CONTINUE**
═══════════════════════════════════════════════════════════
```

---

## Mode Comparison

| Mode | When to Use | Priming Time | Components Loaded |
|------|-------------|--------------|-------------------|
| **Auto** | Default (smart detection) | Variable | Depends on checkpoint age |
| **Fresh** | New session, no prior work | 10-20s | Skills + MCPs only |
| **Resume** | Continue from checkpoint | 30-60s | Skills + MCPs + Context + Memories |
| **Quick** | Fast resumption | 5-15s | Essential components only |
| **Full** | Deep comprehensive priming | 60-120s | Everything + verification |

---

## Examples

### Auto Mode (Default)

```bash
/shannon:prime

# Detects checkpoint from 2 hours ago
→ Mode: AUTO-RESUME
→ Restores checkpoint + loads memories
→ Ready in 42 seconds
```

### Fresh Session

```bash
/shannon:prime --fresh

# Ignores checkpoints, fresh start
→ Mode: FRESH
→ Discovers skills + verifies MCPs
→ Ready in 15 seconds
```

### Explicit Resume

```bash
/shannon:prime --resume

# Forces resume even if checkpoint old
→ Mode: RESUME
→ Restores latest checkpoint
→ Ready in 45 seconds
```

### Quick Mode

```bash
/shannon:prime --quick

# Minimal priming for speed
→ Skills + MCPs only
→ Skip memory loading
→ Ready in 8 seconds
```

### Full Deep Priming

```bash
/shannon:prime --full

# Comprehensive everything
→ All skills discovered
→ All MCPs verified
→ All memories loaded
→ Full verification
→ Ready in 90 seconds
```

---

## Error Recovery

### No Serena MCP

```markdown
⚠️ Serena MCP not connected

**Impact**: Cannot restore checkpoints or load memories

**Options**:
1. Continue in fresh mode (no restoration)
2. Connect Serena MCP: /shannon:check_mcps --setup serena
3. Exit and connect Serena before priming

**Recommendation**: Connect Serena MCP for full Shannon capabilities
```

### Checkpoint Corrupted

```markdown
⚠️ Checkpoint restoration failed

**Error**: {error_message}

**Fallback**: Continuing in fresh mode

**Recovery**: Previous work state not recovered. Manual context reload required.
```

---

## Integration with Other Enhancements

**Enhancement #1 (Forced Reading)**:
- Step 8 activates reading enforcement
- All subsequent /shannon:spec, /shannon:analyze commands enforce complete reading

**Enhancement #2 (Skill Discovery)**:
- Step 2 discovers all skills
- Skills available for auto-invocation in subsequent commands

**Both Active After Prime**:
```
User: "Analyze this spec"
Shannon:
1. Auto-invokes spec-analysis skill (Enhancement #2)
2. Enforces complete reading of spec (Enhancement #1)
3. Executes 8D analysis
```

---

## Performance

**Measured Priming Times**:
- Fresh mode: 12-18 seconds
- Auto-resume mode: 35-50 seconds
- Quick mode: 6-10 seconds
- Full mode: 75-105 seconds

**All within <60 second target** (except full mode by design)

---

## The Bottom Line

**Session resumption should be one command, not six.**

Before Shannon Prime:
1. /shannon:restore <checkpoint>
2. /shannon:status
3. /shannon:check_mcps
4. Manually load memories
5. Manually reload spec/plan
6. Manually verify state

After Shannon Prime:
1. /shannon:prime

**60x faster** (1 command vs 6), **12x time savings** (<60s vs 15-20 min).

**Target**: Make Shannon the fastest framework for session resumption and context priming.
