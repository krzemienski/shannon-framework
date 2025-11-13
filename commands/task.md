---
name: task
description: Automated prime → spec → wave workflow for complete task execution
usage: /shannon:task "specification" [--auto] [--plan-only]
---

# Shannon Task: Automated Workflow Command

## Overview

**One-command automation** from specification to ready-to-develop state. Orchestrates Shannon's complete workflow: session priming → specification analysis → wave execution.

**Eliminates**: Manual command chaining (`/shannon:prime` → `/shannon:spec` → `/shannon:wave`)
**Provides**: Intelligent automation with user checkpoints and error handling

## Prerequisites

- Shannon Framework installed and active
- Serena MCP connected (required for checkpoints)
- Valid task specification (minimum 20 words)

## Workflow

### Step 1: Session Preparation

**Invoke**:
```
/shannon:prime
```

**Purpose**:
- Discover all available skills
- Verify MCP connections (Serena, Sequential, Puppeteer)
- Restore any previous session context
- Prepare development environment

**Output**: Session ready in 30-60 seconds

### Step 2: Validate Input

**Check specification provided**:
- If missing: Display usage and exit
- If < 20 words: Warn and request expansion
- If valid: Proceed to analysis

### Step 3: Specification Analysis

**Invoke**:
```
/shannon:spec [user_specification] --save
```

**Capture**:
- Complexity score (0.0-1.0)
- Domain breakdown percentages
- Timeline estimate
- MCP recommendations
- Execution strategy (DIRECT vs WAVE-BASED)

**Output to user**:
```markdown
📊 Specification Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Complexity: {score} ({label})
Strategy: {WAVE-BASED|DIRECT}
Timeline: {estimate}
Waves: {count} recommended
```

### Step 4: User Decision Point (Interactive Mode)

**Present options**:
```markdown
Next Steps:
1. Execute with waves (recommended for complexity >=0.50)
2. Show wave plan only (preview without executing)
3. Skip waves, go to completion (for simple tasks)
4. Abort (exit Shannon Task)

Choice (1/2/3/4):
```

**With --auto flag**: Automatically choose option 1 (execute with waves)

### Step 5: Wave Execution (Conditional)

**IF user chose "Execute" OR --auto flag**:

```
/shannon:wave
```

**Wave Loop**:
1. Execute current wave
2. Show wave results
3. Ask user: "Continue to next wave? (yes/no)"
4. IF yes AND more waves exist: Repeat
5. IF no OR waves complete: Continue to Step 6

**With --auto flag**: Automatically continue all waves

**IF user chose "Show plan only"**:
```
/shannon:wave --plan
```
Display plan and EXIT (don't execute, don't prime)

**IF user chose "Skip waves"**:
Skip directly to Step 6 (complete)

### Step 6: Task Complete

**Summary Output**:
```markdown
✅ Shannon Task Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Executed**:
├─ Session Priming ✅
├─ Specification Analysis ✅
└─ Wave Execution ({wave_count} waves) ✅

**Results**:
- Complexity: {score}
- Time Elapsed: {duration}
- Waves Completed: {count}
- Components Built: {files_created}

**Status**: Ready for development

**Next Actions**:
- Review wave deliverables in project directory
- Run /shannon:status for current state
- Begin implementation or testing
```

## Command Flags

### --auto
Fully automated execution with no user prompts:
```bash
/shannon:task "Build REST API with auth" --auto
```

**Behavior**:
- Automatically executes all waves
- No decision points
- Runs to completion or error
- Use for: Well-defined tasks, automation scripts, CI/CD

### --plan-only
Generate execution plan without running:
```bash
/shannon:task "Build e-commerce platform" --plan-only
```

**Behavior**:
- Runs spec analysis
- Shows wave plan
- Does NOT execute waves
- Does NOT run prime
- Use for: Estimation, planning, review before commitment

## Error Handling

### Specification Analysis Fails

**Error**:
```
❌ Specification analysis failed
Reason: {error_message}
```

**Recovery**:
1. Review specification (may be too vague)
2. Expand specification with more details
3. Retry: `/shannon:task "expanded specification"`

**Common causes**: Spec too short, missing tech stack, ambiguous requirements

### Wave Execution Fails

**Error**:
```
❌ Wave {N} execution failed
Reason: {error_message}
```

**Recovery Options**:
1. **Retry wave**: Fix issue and re-run `/shannon:wave {N}`
2. **Skip wave**: Continue with `/shannon:task --resume-from-prime`
3. **Abort**: Exit and debug manually

**Auto-checkpoint**: Wave state saved before failure (can restore)

### Prime Fails

**Error**:
```
❌ Session priming failed
Reason: {error_message}
```

**Recovery**:
1. Check MCP status: `/shannon:check_mcps`
2. If Serena disconnected: Reconnect and retry
3. Manual prime: `/shannon:prime --fresh`

## Usage Examples

### Example 1: Simple Task (Auto Mode)

```bash
/shannon:task "Build login form with email and password validation" --auto
```

**What happens**:
1. Spec analysis: Complexity 0.35 (SIMPLE)
2. Direct implementation (no waves needed)
3. Prime session
4. Ready in ~2 minutes

### Example 2: Complex Task (Interactive)

```bash
/shannon:task "Build multi-tenant SaaS platform with billing, analytics, and admin dashboard"
```

**What happens**:
1. Spec analysis: Complexity 0.75 (VERY COMPLEX)
2. Shows 3 waves recommended
3. Asks: Execute? → User confirms
4. Wave 1 executes → User reviews → Continues
5. Wave 2 executes → User reviews → Continues
6. Wave 3 executes → User reviews → Continues
7. Prime session
8. Ready in ~8 hours (3 waves)

### Example 3: Planning Mode

```bash
/shannon:task "Build distributed microservices architecture" --plan-only
```

**What happens**:
1. Spec analysis: Complexity 0.82 (VERY COMPLEX)
2. Wave plan generated (4 waves, timeline shown)
3. Stops (no execution)
4. User reviews plan, can adjust specification
5. Re-run without --plan-only when ready

## Integration with Shannon Framework

### Command Chain

**Shannon Task internally executes**:
```
/shannon:spec → /shannon:wave → /shannon:prime
```

**Each command's role**:
- **spec**: Quantitative complexity analysis, domain classification
- **wave**: Parallel multi-agent execution with synthesis checkpoints
- **prime**: Context restoration, skill discovery, MCP verification

### State Management

**Checkpoints created**:
- Pre-wave checkpoint (automatic)
- Post-wave checkpoints (per wave)
- Final checkpoint after prime

**Recovery**: If Shannon Task interrupted, use `/shannon:restore` to recover state

### Skill Dependencies

**Invoked automatically**:
- spec-analysis (via /shannon:spec)
- wave-orchestration (via /shannon:wave)
- context-preservation (via /shannon:prime)
- skill-discovery (via /shannon:prime)

No manual skill invocation needed.

## Performance

**Typical execution times**:
- Simple task (complexity <0.30): 1-3 minutes
- Moderate task (0.30-0.50): 5-15 minutes
- Complex task (0.50-0.70): 1-4 hours
- Very complex (>0.70): 4-12 hours

**Speedup vs manual**:
- Manual: Run 3 commands separately, coordinate manually
- Shannon Task: One command, automated coordination
- Time saved: ~5-10 minutes per task (setup overhead elimination)

## Backward Compatibility

**V4.1 Compatibility**: ✅ NEW command (no breaking changes)

**Alternatives** (still work):
- Manual execution: `/shannon:spec` → `/shannon:wave` → `/shannon:prime`
- Partial automation: Run any command individually

**Migration**: None needed (new feature, not replacement)

## Command Dependencies

**Prerequisites**:
- `/shannon:spec` (REQUIRED)
- `/shannon:wave` (CONDITIONAL - only if complexity >=0.50)
- `/shannon:prime` (REQUIRED)

**Related Commands**:
- `/shannon:status` - Check current state
- `/shannon:checkpoint` - Manual checkpoint creation
- `/shannon:restore` - Recover from interruption

## MCP Dependencies

**Required**:
- Serena MCP (checkpointing, context preservation)

**Recommended**:
- Sequential MCP (complex spec analysis)
- Puppeteer MCP (functional testing in waves)
- Context7 MCP (framework-specific patterns)

## Success Criteria

Shannon Task succeeds when:
- ✅ Specification analyzed (complexity scored)
- ✅ Appropriate execution strategy selected
- ✅ Waves executed if needed (for complexity >=0.50)
- ✅ Session primed (skills discovered, MCPs verified)
- ✅ User ready to continue development
- ✅ All checkpoints created successfully

## Notes

- **Fastest workflow**: `--auto` flag for known-good specifications
- **Safest workflow**: Interactive mode with review at each step
- **Planning workflow**: `--plan-only` for estimation and review
- **Recovery**: Checkpoints enable recovery from any interruption
- **Transparency**: User sees all command outputs, makes decisions

## Related Documentation

- Commands: /shannon:spec, /shannon:wave, /shannon:prime
- Skills: spec-analysis, wave-orchestration, context-preservation
- Guides: commands/guides/ for detailed command documentation
