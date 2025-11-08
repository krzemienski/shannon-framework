# Forced Complete Reading Protocol

## Overview

This file defines mandatory reading enforcement behaviors for Shannon Framework agents working with critical documents. NO competitor framework implements architectural reading enforcement.

**Purpose**: Prevent skimming and superficial reading that leads to incomplete understanding and incorrect implementations

**Method**: Pre-counting, sequential line-by-line reading, completeness verification, post-reading synthesis

**Output**: Guaranteed complete comprehension of every line in critical documents

**Core Philosophy**: Thoroughness cannot be optional in mission-critical domains (Finance, Healthcare, Legal, Security, Aerospace)

---

## Automatic Activation Triggers

Shannon's forced reading protocol activates automatically for:

### Critical File Types
- **All *.md files** (specifications, plans, documentation)
- **SPEC_* and PLAN_* files** (specification and plan documents)
- **SKILL.md files** (skill definitions MUST be read completely)
- **All files >=3000 lines** (large files most likely to be skimmed)

### Command Contexts
- **/sh_spec** - Specifications MUST be read completely before analysis
- **/sh_analyze** - Analysis targets MUST be read completely
- **/sh_wave** - Wave plans MUST be read completely before execution

### Manual Override Available
- **/sh_read_normal <file>** - Disables enforcement for legitimate quick lookups
- All overrides logged to Serena MCP for audit

---

## Iron Law: The Complete Reading Protocol

<IRON_LAW>

When analyzing critical documents, you MUST follow this exact protocol:

### Step 1: PRE-COUNT (Before reading begins)

**ACTION**: Count total lines in file BEFORE reading ANY content

**Commands**:
```
# Manual counting
/sh_count_lines <file_path>

# Serena MCP method
total_lines = mcp__serena__read_file(file_path).count('\n') + 1
```

**OUTPUT**: "File has {N} lines. Now I will read all {N} lines completely."

**NO EXCEPTIONS**: You cannot read without knowing total line count first.

### Step 2: SEQUENTIAL READING (Line-by-line)

**ACTION**: Read EVERY line sequentially from 1 to N

**NOT ALLOWED**:
- ❌ "Read relevant sections"
- ❌ "Scan for key points"
- ❌ "Quick overview then deep dive"
- ❌ Read offset=0, limit=100 (partial reading)
- ❌ Search for patterns without complete reading

**REQUIRED**:
- ✅ Read line 1
- ✅ Read line 2
- ✅ Read line 3
- ✅ ...continue sequentially...
- ✅ Read line N (last line)

**TRACKING**: Track each line number as you read it

### Step 3: VERIFY COMPLETENESS (Before synthesis)

**ACTION**: Verify lines_read == total_lines

**Formula**:
```
IF lines_read < total_lines THEN
  missing_lines = total_lines - lines_read
  RAISE ERROR: "INCOMPLETE READING: Missing {missing_lines} lines"
  BLOCK: No analysis, no synthesis, no conclusions
  REQUIRED: Return to Step 2, read missing lines
END IF
```

**VERIFICATION OUTPUT**:
```
✅ COMPLETE READING VERIFIED
   Total lines: {N}
   Lines read: {N}
   Completeness: 100%
   Status: READY FOR SYNTHESIS
```

### Step 4: SEQUENTIAL SYNTHESIS (After complete reading only)

**ACTION**: Use Sequential MCP for deep thinking about what was read

**Minimum thinking steps** (based on file size):
- Small (<500 lines): 50+ thoughts minimum
- Medium (500-2000 lines): 100+ thoughts minimum
- Large (2000-5000 lines): 200+ thoughts minimum
- Critical (5000+ lines): 500+ thoughts minimum

**REQUIRED TOOL**: mcp__sequential-thinking__sequentialthinking

**NOT ALLOWED UNTIL COMPLETE**:
- ❌ Analysis during reading
- ❌ Patterns identified during reading
- ❌ Conclusions during reading
- ❌ "I noticed that..." during reading

**ONLY AFTER VERIFICATION**:
- ✅ Synthesis via Sequential MCP
- ✅ Pattern identification
- ✅ Comprehensive analysis
- ✅ Actionable conclusions

</IRON_LAW>

---

## Baseline Testing: Known Violations and Counters

**From RED Phase Testing**: Shannon tested agent behavior WITHOUT this protocol.
All baseline scenarios showed violations. This section documents exact rationalizations and provides explicit counters.

### ❌ VIOLATION 1: "I'll read the relevant sections first"

**Baseline Behavior**: Agent uses Grep/search to find "relevant" sections, skips complete reading

**Rationalization Captured**:
> "Let me search for the key requirements first to understand scope"
> "I'll scan for implementation details in the relevant sections"

**Shannon Counter**:
```
⚠️ STOP. "Relevant sections" = incomplete understanding.

REALITY CHECK:
- You don't know what's relevant until you've read everything
- "Relevant" is determined by your assumptions, not reality
- Critical details are often in "irrelevant" sections

REQUIRED ACTION:
1. Count total lines: /sh_count_lines <file>
2. Read ALL lines sequentially (line 1, 2, 3, ..., N)
3. THEN identify what's relevant (after complete reading)

NO EXCEPTIONS. Search/grep only AFTER complete reading.
```

### ❌ VIOLATION 2: "Read offset=0, limit=200 to get started"

**Baseline Behavior**: Agent reads partial file to "get started", never returns to read rest

**Rationalization Captured**:
> "I'll read the first 200 lines to understand structure, then continue"
> "Starting with an overview of the first few sections"

**Shannon Counter**:
```
⚠️ STOP. Partial reading is incomplete reading.

REALITY CHECK:
- "Get started" reading = never finish reading
- Lines 201-N contain critical details you'll miss
- "Overview" = superficial understanding

REQUIRED ACTION:
1. Count total lines
2. Read ALL lines (not just first 200)
3. Verify lines_read == total_lines
4. NO synthesis until verification passes

NO EXCEPTIONS. No partial reading allowed for critical files.
```

### ❌ VIOLATION 3: "File is too long, I'll skim efficiently"

**Baseline Behavior**: Agent rationalizes skimming for files >2000 lines

**Rationalization Captured**:
> "This 2,500-line specification is quite extensive - I'll skim efficiently for key points"
> "Given the length, I'll focus on the main sections"

**Shannon Counter**:
```
⚠️ STOP. "Too long" is not an exemption.

REALITY CHECK:
- Long files are EXACTLY why this protocol exists
- "Skim efficiently" = miss critical details
- Mission-critical work cannot tolerate "good enough" understanding

REQUIRED ACTION:
1. Yes, read all 2,500 lines
2. Use Sequential MCP for 200+ synthesis thoughts
3. This takes time (30-60 min) - that's acceptable
4. Complete understanding > speed

NO EXCEPTIONS. Long files require COMPLETE reading, not efficient skimming.
```

### ❌ VIOLATION 4: "I remember this file from earlier"

**Baseline Behavior**: Agent skips re-reading based on session memory

**Rationalization Captured**:
> "I already read this file earlier in the session"
> "I recall the key points from when I read it before"

**Shannon Counter**:
```
⚠️ STOP. Memory is not verification.

REALITY CHECK:
- Remembering != having read every line
- Files may have changed
- "Key points" = selective memory, not complete understanding

REQUIRED ACTION:
1. Re-count lines (file may have changed)
2. Read completely again OR verify previous reading was complete:
   - Check lines_read == total_lines from earlier
   - If verification passes, synthesis allowed
   - If no verification exists, re-read completely

NO EXCEPTIONS. Either verify previous complete reading OR re-read completely.
```

---

## Red Flag Keywords

If you catch yourself using these phrases, **STOP IMMEDIATELY** - you're about to violate the protocol:

**Skip-Reading Triggers**:
- "read relevant sections"
- "scan for", "look for", "find the parts about"
- "overview first", "get started with"
- "skim efficiently", "quick pass through"

**Partial-Reading Triggers**:
- "offset=0, limit=100"
- "first few hundred lines"
- "initial sections"
- "start with the beginning"

**Length-Based Rationalization Triggers**:
- "file is too long"
- "quite extensive"
- "very large specification"
- "efficiently review"

**Memory-Based Triggers**:
- "already read this"
- "recall from earlier"
- "familiar with this file"
- "remember the key points"

**ALL OF THESE MEAN**: STOP. Count lines. Read all lines. Verify completeness.

---

## Reading Status Dashboard

Track reading completeness across session:

**Command**: `/sh_reading_status`

**Output Format**:
```markdown
# Reading Completeness Report

| File | Total Lines | Lines Read | Completeness | Status |
|------|-------------|------------|--------------|--------|
| SPEC_ANALYSIS.md | 1786 | 1786 | 100.0% | ✅ COMPLETE |
| PLAN_WAVE_1.md | 450 | 320 | 71.1% | 🟡 PARTIAL |
| requirements.md | 250 | 0 | 0.0% | 🔴 NOT STARTED |
```

**Interpretation**:
- ✅ COMPLETE (100%): Synthesis allowed
- 🟡 PARTIAL (70-99%): Synthesis BLOCKED, read missing lines
- 🔴 INCOMPLETE (<70%): Synthesis BLOCKED, complete reading required

---

## Configuration

### Per-Project Configuration

File: `.shannon/reading-enforcement.json`

```json
{
  "enforcement_enabled": true,
  "critical_file_patterns": [
    "*.md",
    "SPEC_*",
    "PLAN_*",
    "**/skills/**/SKILL.md"
  ],
  "size_threshold": 3000,
  "minimum_synthesis_steps": {
    "small": 50,
    "medium": 100,
    "large": 200,
    "critical": 500
  },
  "override_allowed": true,
  "override_audit": true
}
```

### Disable Enforcement (Legitimate Cases)

**Command**: `/sh_read_normal <file>`

**Use Cases**:
- Quick reference lookups (API docs, syntax guides)
- Repeated reads of same file (already verified complete once)
- User explicitly wants fast skim (user's choice)

**Audit Trail**: All overrides logged to Serena MCP (shannon/reading-enforcement/overrides)

---

## Integration with Shannon Commands

### Enhanced Commands (Enforce Complete Reading)

**/sh_spec** - Specifications:
```markdown
## FORCED READING ENFORCEMENT

Before analyzing specification:
1. Count total lines in specification
2. Read ALL lines sequentially
3. Verify completeness (100%)
4. Use Sequential MCP for 100+ synthesis thoughts
5. THEN present 8D analysis
```

**/sh_analyze** - Analysis Targets:
```markdown
## FORCED READING ENFORCEMENT

Before analyzing codebase/files:
1. For each critical file, count lines
2. Read ALL lines sequentially
3. Verify completeness per file
4. Aggregate: all_files_complete = all(completeness == 100%)
5. THEN synthesize findings
```

**/sh_wave** - Wave Execution:
```markdown
## FORCED READING ENFORCEMENT

Before executing wave:
1. Count lines in wave plan
2. Read ALL tasks sequentially
3. Verify plan completeness (100%)
4. Use Sequential MCP for wave synthesis
5. THEN execute wave tasks
```

---

## Integration with Shannon Skills

### Skills Requiring Complete Reading

**spec-analysis**: MUST read specification completely before 8D scoring
**shannon-analysis**: MUST read codebase files completely before pattern extraction
**confidence-check**: MUST read official docs completely before validation

### Skill Frontmatter Addition

```yaml
---
name: spec-analysis
reading-requirements:
  enforce-complete: true
  minimum-synthesis-steps: 200
  critical-files: ["*.md", "SPEC_*"]
---
```

---

## Integration with Shannon Agents

### Agent Prompts Enhancement

Add to SPEC_ANALYZER, ANALYZER, WAVE_COORDINATOR agent prompts:

```markdown
## FORCED COMPLETE READING PROTOCOL

This agent operates under Shannon's Complete Reading Protocol:

1. ✅ Count total lines BEFORE reading: count_lines(file_path)
2. ✅ Read ALL lines sequentially: line 1, 2, 3, ..., N
3. ✅ Verify completeness: lines_read == total_lines
4. ✅ Sequential synthesis AFTER reading: minimum 100-500 steps
5. ❌ NO analysis until reading complete
6. ❌ NO conclusions during reading
7. ❌ NO skipping or "relevant parts"

**Violation of this protocol will BLOCK task completion.**
```

---

## The Bottom Line

**For mission-critical work, complete understanding is mandatory.**

Same as NO MOCKS for testing: superficial comprehension = unreliable results.

**If you follow "read every line" for code reviews, follow it for specifications.**

This protocol is not optional. It's architectural enforcement of thoroughness.

**Target domains**: Finance, Healthcare, Legal, Security, Aerospace - where AI hallucinations from incomplete reading are unacceptable.
