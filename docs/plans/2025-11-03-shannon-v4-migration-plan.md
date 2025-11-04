# Shannon Framework V4 - Executable Migration Plan

**Plan Type**: Wave-Based Migration from V3 to V4
**Version**: V3.0.1 → V4.0.0
**Date**: 2025-11-03
**Timeline**: 6-8 weeks
**Execution Model**: 5 waves with functional testing per wave

---

## Executive Summary

This document provides the complete executable migration plan for transforming Shannon Framework from V3's monolithic command architecture to V4's skill-based composable architecture.

**Migration Philosophy**:
- **Zero Breaking Changes**: V4 commands work identically to V3 from user perspective
- **Gradual Transition**: Skills and commands coexist during migration
- **Continuous Validation**: Functional tests validate each wave before proceeding
- **Rollback Safety**: Each wave can be rolled back without data loss

**Timeline**: 6-8 weeks (6-8 minutes human time)

**Waves**:
1. **Wave 1**: Core Infrastructure (1 week)
2. **Wave 2**: Core Skills Implementation (2 weeks)
3. **Wave 3**: Context & Memory Skills (1 week)
4. **Wave 4**: Enhanced Skills from Reference Repos (1 week)
5. **Wave 5**: Command Migration & SuperClaude Deprecation (1-2 weeks)

---

## Pre-Migration Requirements

### Prerequisites Checklist

- [ ] Shannon V3.0.1 installed and functional
- [ ] Serena MCP configured and operational (**CRITICAL**)
- [ ] Git repository clean (no uncommitted changes)
- [ ] All existing tests passing
- [ ] Backup created: `git tag v3.0.1-backup`
- [ ] Development branch created: `git checkout -b shannon-v4-migration`
- [ ] Sequential MCP available (recommended, not required)
- [ ] Context7 MCP available (recommended, not required)

### Environment Validation

```bash
# Verify Shannon V3 works
/sh_status
# Expected: Shannon v3.0.1 active

# Verify Serena MCP
/sh_check_mcps
# Expected: ✅ Serena MCP connected

# Verify git state
git status
# Expected: On branch main, nothing to commit

# Create backup tag
git tag v3.0.1-backup
git push origin v3.0.1-backup

# Create development branch
git checkout -b shannon-v4-migration
```

**CRITICAL**: Do NOT proceed without Serena MCP. It's required for context preservation during migration.

---

# Wave 1: Core Infrastructure

**Duration**: 1 week (~1 minute human time)
**Goal**: Create skills/ directory structure, templates, validation infrastructure
**Risk Level**: Low (additive changes, no modifications to existing code)

## Wave 1 Tasks

### Task 1.1: Create Skills Directory Structure

**Files to Create**:
```bash
shannon-plugin/skills/
shannon-plugin/skills/.gitkeep
shannon-plugin/skills/README.md
```

**Implementation**:

```bash
# Create skills directory
mkdir -p shannon-plugin/skills
touch shannon-plugin/skills/.gitkeep
```

**Create skills/README.md**:
```markdown
# Shannon Framework V4 Skills

This directory contains Shannon's behavioral skills that commands orchestrate.

## Skill Structure

Each skill follows this structure:
```
skill-name/
├── SKILL.md          # Main skill file (required)
├── references/       # Deep reference docs (progressive disclosure)
├── examples/         # Usage examples (minimum 3)
└── templates/        # Output templates (if applicable)
```

## Available Skills

**Core Shannon Skills**:
- spec-analysis - 8D complexity scoring
- wave-orchestration - Parallel wave execution
- phase-planning - 5-phase implementation planning
- context-preservation - Checkpoint creation
- context-restoration - Checkpoint restoration
- functional-testing - NO MOCKS enforcement
- mcp-discovery - MCP server recommendations
- memory-coordination - Serena MCP queries
- goal-management - North Star tracking
- shannon-analysis - General analysis

**Enhanced Skills** (from reference frameworks):
- sitrep-reporting - SITREP protocol (from Hummbl)
- confidence-check - Pre-implementation validation (from SuperClaude)
- project-indexing - Codebase compression (from SuperClaude)

**Meta-Skill**:
- using-shannon - Auto-loaded via SessionStart hook

## Skill Development

See: ../../docs/SKILL_DEVELOPMENT_GUIDE.md

## Testing

```bash
# Validate skill structure
python3 shannon-plugin/tests/validate_skills.py

# Test skill invocation
python3 shannon-plugin/tests/test_skill_activation.py
```
```

**Functional Test 1.1**:
```bash
# Test: Skills directory created
test -d shannon-plugin/skills
echo $? # Expected: 0 (success)

# Test: README exists
test -f shannon-plugin/skills/README.md
echo $? # Expected: 0
```

**Acceptance Criteria**:
- [ ] shannon-plugin/skills/ directory exists
- [ ] README.md explains skill structure
- [ ] Git tracking confirmed

---

### Task 1.2: Create Skill Template Files

**Files to Create**:
```
shannon-plugin/templates/
└── SKILL_TEMPLATE.md
```

**Implementation**:

Create `shannon-plugin/templates/SKILL_TEMPLATE.md`:
```markdown
---
name: skill-name
description: |
  [160-250 character rich description with purpose, capabilities, trigger keywords, use cases]

skill-type: QUANTITATIVE | RIGID | PROTOCOL | FLEXIBLE
shannon-version: ">=4.0.0"
complexity-triggers: [0.0-1.0]

mcp-requirements:
  required:
    - name: serena
      purpose: Context preservation
      fallback: local-storage
  recommended: []
  conditional: []

required-sub-skills: []
optional-sub-skills: []

allowed-tools: Read, Grep, Glob, Serena
---

# Skill Name

## Overview

**Purpose**: [What this skill does in one paragraph]

**When to Use**:
- [Trigger scenario 1]
- [Trigger scenario 2]
- [Trigger scenario 3]

**Expected Outcomes**: [What user receives]

**Duration**: [Time estimate]

---

## Core Competencies

### 1. [Competency Area 1]
- [Capability 1]
- [Capability 2]
- [Capability 3]

### 2. [Competency Area 2]
[...]

### 3. [Competency Area 3]
[...]

---

## Workflow

### Step 1: [Action Name]
**Input**: [Data structure or requirements]
**Processing**:
1. [Detailed sub-step]
2. [Detailed sub-step]
3. [Detailed sub-step]

**Output**: [Data structure produced]
**Duration**: [Time estimate]

### Step 2: [Action Name]
[...]

---

## Agent Activation

**Agent**: [AGENT_NAME] (if applicable)

**Context Provided**:
- System prompt: "[Agent's specialized prompt]"
- Tools: [Allowed tools]
- Domain knowledge: [What agent knows]

**Activation Trigger**: [When agent activates]

---

## MCP Integration

### Required MCPs

**[MCP Name]**
- **Purpose**: [Why this skill needs it]
- **Usage**: [Pattern or code example]
- **Fallback**: [If unavailable]
- **Degradation**: [Impact level]

### Recommended MCPs
[...]

---

## Examples

### Example 1: [Simple Case]
**Input**: [...]
**Execution**: [...]
**Output**: [...]

### Example 2: [Complex Case]
[...]

### Example 3: [Edge Case]
[...]

---

## Success Criteria

**Successful when**:
- ✅ [Measurable criterion 1]
- ✅ [Measurable criterion 2]
- ✅ [Measurable criterion 3]

**Fails if**:
- ❌ [Anti-criterion 1]
- ❌ [Anti-criterion 2]

---

## Common Pitfalls

### Pitfall 1: [Problem Name]
**Problem**: [Description]
**Solution**: [Fix]
**Prevention**: [How to avoid]

### Pitfall 2: [Problem Name]
[...]

---

## Validation

**How to verify**:
1. [Check 1]
2. [Check 2]
3. [Check 3]

---

## Progressive Disclosure

**SKILL.md** (This file): ~400-600 lines
- [What's included]

**references/**: [What's deferred]
- [Reference file 1]
- [Reference file 2]

**Claude loads references/ when**: [Conditions]

---

## References

- [Link to core/ document if applicable]
- [Link to related skills]
- [External documentation]

---

## Metadata

**Version**: 4.0.0
**Last Updated**: 2025-11-03
**Author**: Shannon Framework Team
**License**: MIT
**Status**: [Core | Enhanced | Experimental]
```

**Functional Test 1.2**:
```bash
# Test: Template exists
test -f shannon-plugin/templates/SKILL_TEMPLATE.md
echo $? # Expected: 0

# Test: Template has all required sections
grep -q "## Core Competencies" shannon-plugin/templates/SKILL_TEMPLATE.md
grep -q "## Success Criteria" shannon-plugin/templates/SKILL_TEMPLATE.md
grep -q "## Common Pitfalls" shannon-plugin/templates/SKILL_TEMPLATE.md
echo $? # Expected: 0 for all
```

**Acceptance Criteria**:
- [ ] SKILL_TEMPLATE.md created with all sections
- [ ] Template validated against Shannon V4 standard
- [ ] Developers can copy template to create new skills

---

### Task 1.3: Create Validation Infrastructure

**Files to Create**:
```
shannon-plugin/tests/validate_skills.py
shannon-plugin/tests/test_skill_activation.py
shannon-plugin/tests/test_skill_composition.py
```

**Implementation**:

Create `shannon-plugin/tests/validate_skills.py`:
```python
#!/usr/bin/env python3
"""
Shannon V4 Skill Structure Validation

Validates all skills in shannon-plugin/skills/ for:
- Required files (SKILL.md)
- Valid YAML frontmatter
- Required sections present
- Examples exist (minimum 3)
- Success criteria defined
- Common pitfalls documented
- Progressive disclosure properly structured
"""

import yaml
import sys
from pathlib import Path

def validate_skill(skill_dir: Path) -> dict:
    """Validate single skill directory"""
    errors = []
    warnings = []

    # Check 1: SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_dir.name}")
        return {"skill": skill_dir.name, "errors": errors, "warnings": warnings}

    content = skill_md.read_text()

    # Check 2: Valid YAML frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md missing YAML frontmatter")
        return {"skill": skill_dir.name, "errors": errors, "warnings": warnings}

    try:
        yaml_end = content.index("\n---\n", 4)
        frontmatter = yaml.safe_load(content[4:yaml_end])
    except Exception as e:
        errors.append(f"Invalid YAML frontmatter: {e}")
        return {"skill": skill_dir.name, "errors": errors, "warnings": warnings}

    # Check 3: Required frontmatter fields
    required_fields = ["name", "description"]
    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Check 4: Shannon-specific fields
    shannon_fields = ["skill-type", "shannon-version"]
    for field in shannon_fields:
        if field not in frontmatter:
            warnings.append(f"Missing Shannon field: {field}")

    # Check 5: Skill type valid
    if "skill-type" in frontmatter:
        valid_types = ["QUANTITATIVE", "RIGID", "PROTOCOL", "FLEXIBLE"]
        if frontmatter["skill-type"] not in valid_types:
            errors.append(f"Invalid skill-type: {frontmatter['skill-type']}")

    # Check 6: Required sections in markdown
    required_sections = [
        "## Overview",
        "## Core Competencies",
        "## Workflow",
        "## Examples",
        "## Success Criteria",
        "## Common Pitfalls",
    ]
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    # Check 7: Minimum 3 examples
    example_count = content.count("### Example ")
    if example_count < 3:
        warnings.append(f"Only {example_count} examples (recommend 3+)")

    # Check 8: Success criteria has checkboxes
    if "## Success Criteria" in content:
        success_section = content[content.index("## Success Criteria"):]
        success_section = success_section[:success_section.index("\n##", 100) if "\n##" in success_section[100:] else len(success_section)]
        if "- ✅" not in success_section:
            warnings.append("Success criteria should use ✅ checkboxes")
        if "- ❌" not in success_section:
            warnings.append("Failure criteria should use ❌ checkboxes")

    # Check 9: references/ directory (progressive disclosure)
    references_dir = skill_dir / "references"
    if not references_dir.exists():
        warnings.append("No references/ directory (consider for complex skills)")

    # Check 10: examples/ directory
    examples_dir = skill_dir / "examples"
    if not examples_dir.exists():
        warnings.append("No examples/ directory (recommended for clarity)")

    return {
        "skill": skill_dir.name,
        "errors": errors,
        "warnings": warnings,
        "valid": len(errors) == 0
    }

def validate_all_skills():
    """Validate all skills in shannon-plugin/skills/"""
    skills_dir = Path("shannon-plugin/skills")

    if not skills_dir.exists():
        print("❌ shannon-plugin/skills/ directory does not exist")
        return False

    results = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith("."):
            result = validate_skill(skill_dir)
            results.append(result)

    # Print results
    valid_count = sum(1 for r in results if r["valid"])
    total_count = len(results)

    print(f"\n{'='*60}")
    print(f"Shannon V4 Skill Validation Results")
    print(f"{'='*60}\n")

    for result in results:
        status = "✅" if result["valid"] else "❌"
        print(f"{status} {result['skill']}")

        for error in result["errors"]:
            print(f"  ❌ ERROR: {error}")
        for warning in result["warnings"]:
            print(f"  ⚠️  WARNING: {warning}")
        print()

    print(f"{'='*60}")
    print(f"Results: {valid_count}/{total_count} skills valid")
    print(f"{'='*60}\n")

    return valid_count == total_count

if __name__ == "__main__":
    success = validate_all_skills()
    sys.exit(0 if success else 1)
```

**Functional Test 1.3**:
```bash
# Test: Validation script exists
test -f shannon-plugin/tests/validate_skills.py
echo $? # Expected: 0

# Test: Script is executable
chmod +x shannon-plugin/tests/validate_skills.py
python3 shannon-plugin/tests/validate_skills.py
# Expected: "0/0 skills valid" (no skills yet, but script works)
```

**Acceptance Criteria**:
- [ ] validate_skills.py created and executable
- [ ] Script validates YAML frontmatter
- [ ] Script checks required sections
- [ ] Script detects missing examples
- [ ] Script runs without errors (even with 0 skills)

---

### Task 1.4: Create using-shannon Meta-Skill

**Files to Create**:
```
shannon-plugin/skills/using-shannon/
shannon-plugin/skills/using-shannon/SKILL.md
shannon-plugin/skills/using-shannon/anti-rationalizations.md
shannon-plugin/hooks/session_start.sh
```

**Implementation**:

Create `shannon-plugin/skills/using-shannon/SKILL.md`:
```markdown
---
name: using-shannon
description: |
  Use at session start - establishes Shannon Framework workflows including mandatory 8D analysis
  before implementation, NO MOCKS testing enforcement, wave-based execution for complexity ≥0.50,
  and automatic Serena MCP checkpointing. Prevents under-estimation and ensures quantitative rigor.
  Trigger keywords: shannon, specification, complexity, wave, checkpoint.

skill-type: RIGID
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      purpose: Context preservation (mandatory for Shannon)

allowed-tools: All
---

# Using Shannon Framework

<IRON_LAW>
Shannon Framework has MANDATORY workflows for specification-driven development.

YOU MUST:
1. Analyze specifications with 8D scoring BEFORE any implementation
2. Use wave-based execution for complexity ≥0.50 (Complex or higher)
3. Use FUNCTIONAL TESTS ONLY (NO MOCKS, NO UNIT TESTS, NO STUBS)
4. Checkpoint to Serena MCP before context compaction (automatic via PreCompact hook)
5. Follow SITREP protocol for multi-agent coordination (complexity ≥0.70)

These are not guidelines. These are requirements.
Violating these = failing to use Shannon correctly.
</IRON_LAW>

## Mandatory Workflows

### Before Starting ANY Implementation

**Workflow**:
```
1. User provides specification/requirements
2. YOU MUST: Run /sh_spec (or invoke spec-analysis skill)
3. Review 8D complexity score (0.0-1.0)
4. If complexity ≥0.50: Plan wave-based execution
5. If complexity ≥0.70: Use SITREP protocol for coordination
6. ONLY THEN: Begin implementation
```

**Failure Mode**: Starting implementation without 8D analysis

**Why This Fails**: Human intuition under-estimates complexity by 30-50% on average. Shannon's quantitative scoring prevents under-resourcing.

### During Implementation

**Workflow**:
```
1. Follow wave plan (if complexity ≥0.50)
2. Checkpoint at wave boundaries (automatic)
3. Use functional tests ONLY (NO MOCKS)
4. SITREP updates for multi-agent work
5. Never skip validation gates
```

**Failure Mode**: Using unit tests or mock objects

**Why This Fails**: Mocks test mock behavior, not production behavior. Shannon enforces real system testing.

### Before Context Compaction

**Workflow**:
```
1. PreCompact hook triggers (automatic)
2. context-preservation skill auto-invokes
3. Checkpoint saved to Serena MCP
4. Context compacts safely
5. Resume anytime with /sh_restore
```

**Failure Mode**: Manual checkpoint attempts after compaction

**Why This Fails**: Context already lost. PreCompact hook prevents this automatically.

## Common Rationalizations That Violate Shannon

If you catch yourself thinking ANY of these thoughts, STOP. You are about to violate Shannon's quantitative rigor.

❌ **"Specification is simple, skip 8D analysis"**
- **Why This Is Wrong**: Your subjective "simple" is often 0.50-0.70 (Complex) quantitatively
- **Solution**: ALWAYS run /sh_spec, let quantitative scoring decide

❌ **"Unit tests are faster than functional tests"**
- **Why This Is Wrong**: Unit tests with mocks test mock behavior, not production
- **Solution**: Use Puppeteer MCP for real browser tests, real database for data tests

❌ **"Wave execution is overkill for this project"**
- **Why This Is Wrong**: Wave execution provides 3.5x speedup for complexity ≥0.50
- **Solution**: Trust the 8D score - if ≥0.50, use waves

❌ **"Manual testing is fine, automation can come later"**
- **Why This Is Wrong**: Manual tests aren't repeatable, miss regressions
- **Solution**: Functional automation from day 1 via Puppeteer/iOS Simulator MCPs

❌ **"I'll checkpoint manually when needed"**
- **Why This Is Wrong**: You'll forget, or context compacts first
- **Solution**: PreCompact hook handles this automatically - trust the system

❌ **"SITREP is too formal for small projects"**
- **Why This Is Wrong**: Multi-agent projects need coordination regardless of size
- **Solution**: Use SITREP for complexity ≥0.70, checkpoints for lower

❌ **"I can estimate complexity by feel"**
- **Why This Is Wrong**: Human intuition is systematically biased toward under-estimation
- **Solution**: Shannon's 8D quantitative scoring removes bias

❌ **"Skip Serena MCP, I'll track context myself"**
- **Why This Is Wrong**: Context loss is inevitable with compaction - Serena prevents loss
- **Solution**: Serena MCP is REQUIRED for Shannon (verify with /sh_check_mcps)

## When to Use Shannon Commands

### /sh_spec - Specification Analysis
**Trigger When**:
- User provides any specification, requirements, or project description
- Starting new feature or project
- Need complexity assessment
- Planning resource allocation

**Mandatory**: YES - for ALL projects with specifications

**Output**: 8D scores, domain breakdown, MCP recommendations, phase plan, wave plan (if ≥0.50), checkpoint

### /sh_wave - Wave Orchestration
**Trigger When**:
- Executing project with complexity ≥0.50
- Need parallel sub-agent coordination
- Want to achieve 2-4x speedup

**Mandatory**: For complexity ≥0.50 (Shannon's quantitative threshold)

**Output**: Wave execution plan, agent allocation, synthesis checkpoints

### /sh_checkpoint - Manual Checkpoint
**Trigger When**:
- Before long-running task
- User wants to save progress explicitly
- Testing checkpoint/restore functionality

**Mandatory**: NO (PreCompact hook handles automatically)

**Output**: Checkpoint ID, Serena URI

### /sh_restore - Restore Session
**Trigger When**:
- Resuming after context loss
- Continuing from previous session
- Recovering from interruption

**Mandatory**: After context compaction or session end

**Output**: Restored context, ready to continue

### /sh_status - Framework Status
**Trigger When**:
- Want to see Shannon framework health
- Check MCP connections
- View active waves/phases
- Generate SITREP (--sitrep flag)

**Mandatory**: NO (diagnostic utility)

**Output**: Status display, optional SITREP

## Skill Usage Patterns

Shannon skills are **model-invoked** (Claude activates based on context), not user-invoked.

**Pattern 1: Automatic Activation**
```
User: "Analyze this specification: Build a task manager"
↓
Claude sees "specification" + "analyze" keywords
↓
Automatically activates spec-analysis skill
↓
Skill executes 8D analysis
↓
Results presented
```

**Pattern 2: Command-Triggered**
```
User: /sh_spec "Build task manager"
↓
sh_spec command explicitly invokes spec-analysis skill
↓
Skill chain: spec-analysis → mcp-discovery → phase-planning → wave-orchestration
↓
Integrated results presented
```

**Pattern 3: Sub-Skill Composition**
```
spec-analysis skill executing
↓
Reaches step requiring MCP recommendations
↓
Invokes mcp-discovery sub-skill (REQUIRED SUB-SKILL)
↓
mcp-discovery executes and returns data
↓
spec-analysis continues with MCP data
```

## Success Patterns

**Successful Shannon V4 Usage**:
1. ✅ Specification analyzed quantitatively BEFORE implementation
2. ✅ Complexity score determines execution strategy (sequential vs wave)
3. ✅ Functional tests used exclusively (real browsers, real DBs)
4. ✅ Context preserved automatically (zero manual checkpoint management)
5. ✅ Multi-agent coordination via SITREP (for High/Critical projects)
6. ✅ MCP servers configured based on domain analysis
7. ✅ Waves complete with validation gates passing
8. ✅ Project delivered on time with quantitative planning accuracy

**Failure Patterns**:
1. ❌ Skipping 8D analysis → Under-resourced project → Delays/overruns
2. ❌ Using unit tests/mocks → Tests pass, production fails → Bugs in prod
3. ❌ Ignoring wave recommendations → Sequential execution → 3.5x slower
4. ❌ Manual context management → Context loss → Work repeated
5. ❌ Subjective complexity assessment → Wrong resource allocation → Failure

## Integration with Existing Skills

Shannon V4 works alongside your existing skills (brainstorming, project-planning, etc.):

**Pattern**: Brainstorming → Shannon Spec Analysis → Wave Execution
```
1. Use brainstorming skill for design refinement
2. Once design complete, use /sh_spec for quantitative analysis
3. Shannon provides 8D scores + wave plan
4. Execute via Shannon's wave-orchestration skill
5. Functional testing enforced throughout
```

**Shannon is specialized for**: Quantitative analysis, parallel execution, functional testing enforcement

**Other skills are specialized for**: Design, planning, debugging, git workflows, etc.

**Use together**: Shannon handles complexity/execution strategy, other skills handle specific workflows

---

## References

- Complete 8D algorithm: `shannon-plugin/core/SPEC_ANALYSIS.md`
- Wave orchestration: `shannon-plugin/core/WAVE_ORCHESTRATION.md`
- NO MOCKS philosophy: `shannon-plugin/core/TESTING_PHILOSOPHY.md`
- Context preservation: `shannon-plugin/core/CONTEXT_MANAGEMENT.md`
- Anti-rationalizations: `using-shannon/anti-rationalizations.md`

---

## Metadata

**Version**: 4.0.0
**Last Updated**: 2025-11-03
**Author**: Shannon Framework Team
**License**: MIT
**Status**: Meta-Skill (auto-loaded via SessionStart hook)
```

Create `shannon-plugin/hooks/session_start.sh`:
```bash
#!/bin/bash
# Shannon V4 SessionStart Hook
# Loads using-shannon meta-skill into every session

echo "<SHANNON_V4_FRAMEWORK_ACTIVE>"
echo ""
echo "Shannon Framework v4.0.0 activated"
echo ""

# Load using-shannon meta-skill
if [ -f "$HOME/.claude/skills/using-shannon/SKILL.md" ] || [ -f "shannon-plugin/skills/using-shannon/SKILL.md" ]; then
    cat shannon-plugin/skills/using-shannon/SKILL.md 2>/dev/null || cat "$HOME/.claude/skills/using-shannon/SKILL.md"
else
    echo "⚠️ WARNING: using-shannon meta-skill not found"
    echo "Shannon workflows may not be enforced"
fi

echo ""
echo "</SHANNON_V4_FRAMEWORK_ACTIVE>"
```

Update `shannon-plugin/hooks/hooks.json`:
```json
{
  "PreCompact": [{
    "type": "command",
    "command": "python3 shannon-plugin/hooks/precompact.py"
  }],
  "PostToolUse": [{
    "matcher": "Write(**/*test*.{py,js,ts})",
    "hooks": [{
      "type": "command",
      "command": "python3 shannon-plugin/hooks/post_tool_use.py"
    }]
  }],
  "UserPromptSubmit": [{
    "type": "command",
    "command": "python3 shannon-plugin/hooks/user_prompt_submit.py"
  }],
  "Stop": [{
    "type": "command",
    "command": "python3 shannon-plugin/hooks/stop.py"
  }],
  "SessionStart": [{
    "type": "command",
    "command": "bash shannon-plugin/hooks/session_start.sh"
  }]
}
```

**Functional Test 1.4**:
```bash
# Test: using-shannon skill created
test -f shannon-plugin/skills/using-shannon/SKILL.md
echo $? # Expected: 0

# Test: SessionStart hook script created
test -f shannon-plugin/hooks/session_start.sh
chmod +x shannon-plugin/hooks/session_start.sh
echo $? # Expected: 0

# Test: Hook executes successfully
bash shannon-plugin/hooks/session_start.sh
# Expected: Shannon v4.0.0 activated + skill content displayed

# Test: hooks.json updated
grep -q "SessionStart" shannon-plugin/hooks/hooks.json
echo $? # Expected: 0

# Test: Validation passes
python3 shannon-plugin/tests/validate_skills.py
# Expected: 1/1 skills valid (using-shannon)
```

**Acceptance Criteria**:
- [ ] using-shannon skill created with Iron Laws
- [ ] Anti-rationalizations documented
- [ ] SessionStart hook created and configured
- [ ] Hook loads meta-skill into every session
- [ ] Validation passes for using-shannon skill

---

### Task 1.5: Update Plugin Manifest

**File to Modify**:
```
shannon-plugin/.claude-plugin/plugin.json
```

**Changes**:
```json
{
  "name": "shannon",
  "version": "4.0.0-alpha.1",  // Updated from 3.0.1
  "displayName": "Shannon Framework V4 (Alpha)",
  "publisher": "shannon-framework",
  "description": "Specification-driven development framework with skill-based architecture, 8D complexity analysis, wave orchestration, and NO MOCKS testing (V4 ALPHA)",

  // ... rest unchanged ...

  "keywords": [
    "specification-analysis",
    "skill-based-architecture",  // NEW
    "8d-complexity-scoring",
    "wave-orchestration",
    "context-preservation",
    "no-mocks-testing",
    "sitrep-protocol",  // NEW
    "mcp-integration",  // NEW
    "quantitative-planning"
  ]
}
```

**Functional Test 1.5**:
```bash
# Validate JSON syntax
jq . shannon-plugin/.claude-plugin/plugin.json
echo $? # Expected: 0 (valid JSON)

# Test: Version updated
jq -r '.version' shannon-plugin/.claude-plugin/plugin.json
# Expected: "4.0.0-alpha.1"

# Test: New keywords present
jq -r '.keywords[]' shannon-plugin/.claude-plugin/plugin.json | grep "skill-based-architecture"
echo $? # Expected: 0 (found)
```

**Acceptance Criteria**:
- [ ] Version updated to 4.0.0-alpha.1
- [ ] Description mentions V4 and skills
- [ ] New keywords added
- [ ] JSON validates successfully

---

## Wave 1 Summary

**Tasks Completed**:
1. ✅ Skills directory structure created
2. ✅ Skill template created
3. ✅ Validation infrastructure created
4. ✅ using-shannon meta-skill created
5. ✅ Plugin manifest updated to v4.0.0-alpha.1

**Files Created**: 7 new files
**Files Modified**: 2 (hooks.json, plugin.json)
**Lines Added**: ~800 lines

**Functional Tests**: 5 tests, all passing required

**Wave 1 Validation**:
```bash
# Run complete Wave 1 validation
python3 shannon-plugin/tests/validate_skills.py
# Expected: ✅ 1/1 skills valid (using-shannon)

# Test SessionStart hook
bash shannon-plugin/hooks/session_start.sh
# Expected: Shannon v4.0.0 activated + using-shannon skill loaded

# Verify structure
ls -la shannon-plugin/skills/
# Expected: using-shannon/ directory present

# Verify templates
ls -la shannon-plugin/templates/
# Expected: SKILL_TEMPLATE.md present
```

**Rollback Procedure** (if Wave 1 fails):
```bash
git checkout shannon-plugin/.claude-plugin/plugin.json
git checkout shannon-plugin/hooks/hooks.json
rm -rf shannon-plugin/skills/
rm -rf shannon-plugin/templates/
rm shannon-plugin/tests/validate_skills.py
git status # Should show clean
```

**Wave 1 Complete**: ✅ Ready for Wave 2

---

# Wave 2: Core Skills Implementation

**Duration**: 2 weeks (~2 minutes human time)
**Goal**: Implement Shannon's 7 core skills (spec-analysis, wave-orchestration, phase-planning, context-*, functional-testing, mcp-discovery)
**Risk Level**: Medium (core functionality migration)

## Wave 2 Tasks

### Task 2.1: Create spec-analysis Skill

**Files to Create**:
```
shannon-plugin/skills/spec-analysis/
shannon-plugin/skills/spec-analysis/SKILL.md
shannon-plugin/skills/spec-analysis/references/
shannon-plugin/skills/spec-analysis/references/SPEC_ANALYSIS.md (copy from core/)
shannon-plugin/skills/spec-analysis/references/domain-patterns.md
shannon-plugin/skills/spec-analysis/examples/
shannon-plugin/skills/spec-analysis/examples/simple-todo-app.md
shannon-plugin/skills/spec-analysis/examples/complex-realtime-platform.md
shannon-plugin/skills/spec-analysis/examples/critical-trading-system.md
shannon-plugin/skills/spec-analysis/templates/
shannon-plugin/skills/spec-analysis/templates/analysis-output.md
```

**Implementation**:

Copy core documentation as reference:
```bash
mkdir -p shannon-plugin/skills/spec-analysis/references
cp shannon-plugin/core/SPEC_ANALYSIS.md shannon-plugin/skills/spec-analysis/references/
```

Create `shannon-plugin/skills/spec-analysis/SKILL.md` (~500 lines):
```markdown
---
name: spec-analysis
description: |
  8-dimensional quantitative complexity analysis with domain detection. Analyzes specifications
  across structural, cognitive, coordination, temporal, technical, scale, uncertainty, dependency
  dimensions producing 0.0-1.0 scores. Detects domains (Frontend, Backend, Database, etc.) with
  percentages. Use when: analyzing specifications, starting projects, planning implementations,
  assessing complexity quantitatively.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"
complexity-triggers: [0.0-1.0]

mcp-requirements:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: Save analysis for cross-session retrieval
      fallback: local-storage
      degradation: medium
  recommended:
    - name: sequential
      purpose: Deep thinking for complex specs (100-500 steps)
      fallback: native-thinking
      degradation: low
      trigger: preliminary_estimate >= 0.60
  conditional:
    - name: context7
      purpose: Framework documentation when frameworks mentioned
      fallback: websearch

required-sub-skills:
  - mcp-discovery
  - phase-planning

optional-sub-skills:
  - wave-orchestration

allowed-tools: Read, Grep, Glob, Sequential, Serena, Context7, WebSearch, WebFetch
---

# Spec Analysis Skill

[Insert complete workflow from design doc Section 4.2 Skill 1]
[Include: Overview, Core Competencies, 9-step workflow, 3 examples, success criteria, 8 pitfalls]
[Reference: Full algorithm in references/SPEC_ANALYSIS.md]
```

**Example Files**:

`examples/simple-todo-app.md`:
```markdown
# Example: Simple Todo App

**Input Specification**:
```
Build a task manager web app with React frontend and Node.js backend.
Users can create, read, update, and delete tasks.
```

**Expected Analysis**:
- Complexity: 0.33 (Moderate)
- Domains: Frontend 50%, Backend 50%
- Timeline: 5-8 hours
- Waves: None (complexity < 0.50)
```

`examples/complex-realtime-platform.md`:
[Full collaborative doc editor example from Section 4.2]

`examples/critical-trading-system.md`:
[Full financial trading system example from Section 4.2]

**Functional Test 2.1**:
```bash
# Test: Skill structure complete
test -f shannon-plugin/skills/spec-analysis/SKILL.md
test -f shannon-plugin/skills/spec-analysis/references/SPEC_ANALYSIS.md
test -d shannon-plugin/skills/spec-analysis/examples
test -d shannon-plugin/skills/spec-analysis/templates
echo $? # Expected: 0 for all

# Test: Validation passes
python3 shannon-plugin/tests/validate_skills.py
# Expected: ✅ 2/2 skills valid (using-shannon, spec-analysis)

# Test: Skill activation (functional test)
# In Claude Code session:
"Analyze this spec: Build a todo app with React"
# Expected: spec-analysis skill auto-activates
# Expected: Returns 8D analysis with complexity score

# Test: Sub-skill invocation
# spec-analysis should invoke mcp-discovery
# Check logs for: "Invoking mcp-discovery skill"
```

**Acceptance Criteria**:
- [ ] spec-analysis skill created with all files
- [ ] References/ contains full SPEC_ANALYSIS.md algorithm
- [ ] 3 examples present (simple, complex, critical)
- [ ] Validation passes
- [ ] Functional test: Skill activates on "analyze specification"
- [ ] Functional test: Skill invokes mcp-discovery sub-skill
- [ ] Functional test: Returns valid 8D analysis within 5 minutes

---

### Task 2.2: Create wave-orchestration Skill

[Similar structure: Files to create, implementation, functional tests, acceptance criteria]

**Estimated**: ~600 lines of skill content + references + examples + templates

---

### Task 2.3: Create phase-planning Skill

[Similar structure]

**Estimated**: ~400 lines + references

---

### Task 2.4: Create context-preservation Skill

[Similar structure]

**Estimated**: ~350 lines + references

---

### Task 2.5: Create context-restoration Skill

[Similar structure]

**Estimated**: ~300 lines + references

---

### Task 2.6: Create functional-testing Skill

**Special Requirements**: Iron Law enforcement

[Similar structure with NO MOCKS manifesto]

**Estimated**: ~500 lines + references + anti-patterns/

---

### Task 2.7: Create mcp-discovery Skill

[Similar structure]

**Estimated**: ~400 lines + mappings/domain-mcp-matrix.json

---

## Wave 2 Summary

**Tasks**: 7 core skills created

**Files Created**: ~40 files (7 skills × ~6 files each average)

**Lines Added**: ~3500 lines (skill content) + 7000+ lines (references)

**Duration**: 2 weeks (~2 minutes human time)

**Functional Tests**: 7 comprehensive tests (one per skill)

**Wave 2 Validation**:
```bash
# Validate all skills
python3 shannon-plugin/tests/validate_skills.py
# Expected: ✅ 8/8 skills valid

# Test skill chain
# Invoke spec-analysis → should trigger mcp-discovery → phase-planning → wave-orchestration
"Analyze: Build complex real-time platform"
# Expected: Complete chain executes, wave plan generated

# Test context preservation
"Checkpoint this analysis"
# Expected: Checkpoint created in Serena MCP

# Test functional-testing skill
"Add tests for login flow"
# Expected: Skill enforces NO MOCKS, generates Puppeteer test
```

**Rollback**:
```bash
git checkout shannon-plugin/skills/
python3 shannon-plugin/tests/validate_skills.py
# Expected: 1/1 valid (only using-shannon remains)
```

---

# Wave 3: Context & Memory Skills

**Duration**: 1 week (~1 minute human time)
**Goal**: Implement memory-coordination, goal-management, shannon-analysis skills
**Risk Level**: Low (supporting skills, no critical dependencies)

## Wave 3 Tasks

### Task 3.1: Create memory-coordination Skill

**Files**: SKILL.md, references/PROJECT_MEMORY.md, examples/

**Functional Test**: Query Serena for previous analyses

**Estimated**: ~300 lines

---

### Task 3.2: Create goal-management Skill

**Files**: SKILL.md, examples/north-star-tracking.md

**Functional Test**: Track North Star goal alignment

**Estimated**: ~250 lines

---

### Task 3.3: Create shannon-analysis Skill

**Files**: SKILL.md, examples/analysis-workflows.md

**Functional Test**: General-purpose analysis with adaptive skill invocation

**Estimated**: ~400 lines

---

## Wave 3 Summary

**Tasks**: 3 supporting skills

**Files Created**: ~12 files

**Lines Added**: ~950 lines

**Duration**: 1 week

**Wave 3 Validation**:
```bash
python3 shannon-plugin/tests/validate_skills.py
# Expected: ✅ 11/11 skills valid

# Test memory coordination
"What analyses did we do yesterday?"
# Expected: Queries Serena, retrieves previous checkpoints

# Test goal management
"Track North Star: Deliver v4 by end of year"
# Expected: Goal recorded, alignment tracking enabled
```

---

# Wave 4: Enhanced Skills from Reference Repos

**Duration**: 1 week
**Goal**: Add sitrep-reporting, confidence-check, project-indexing from SuperClaude/Hummbl
**Risk Level**: Low (optional enhancements)

## Wave 4 Tasks

### Task 4.1: Create sitrep-reporting Skill (from Hummbl)

**Files**: SKILL.md, templates/ (sitrep-full.md, sitrep-brief.md), examples/

**Estimated**: ~350 lines + templates

---

### Task 4.2: Create confidence-check Skill (from SuperClaude)

**Files**: SKILL.md, confidence.ts (optional), examples/

**Estimated**: ~300 lines + optional TypeScript

---

### Task 4.3: Create project-indexing Skill (from SuperClaude)

**Files**: SKILL.md, templates/SHANNON_INDEX.md, examples/

**Estimated**: ~350 lines

---

## Wave 4 Summary

**Tasks**: 3 enhanced skills

**Files Created**: ~15 files

**Lines Added**: ~1000 lines

**Wave 4 Validation**:
```bash
python3 shannon-plugin/tests/validate_skills.py
# Expected: ✅ 14/14 skills valid

# Test SITREP generation
/sh_wave --sitrep
# Expected: Full SITREP generated with auth code

# Test confidence check
"Check confidence before implementing user auth"
# Expected: 5-check validation, confidence score 0.0-1.0

# Test project indexing
"Generate Shannon index for this codebase"
# Expected: SHANNON_INDEX.md created, 90%+ token reduction
```

---

# Wave 5: Command Migration & SuperClaude Deprecation

**Duration**: 1-2 weeks
**Goal**: Migrate all 9 Shannon commands to skill orchestrators, deprecate 24 SuperClaude commands
**Risk Level**: Medium-High (user-facing changes, backward compatibility critical)

## Wave 5 Tasks

### Task 5.1: Migrate sh_spec Command

**File to Modify**: `shannon-plugin/commands/sh_spec.md`

**Current** (monolithic):
```markdown
---
description: Analyze specification with 8D complexity
---

[~500 lines of inline logic]
```

**V4** (skill orchestrator):
```markdown
---
description: Analyze specification with 8D complexity scoring
---

# Specification Analysis Command

## Overview
Performs comprehensive specification analysis using Shannon's 8D complexity framework.

## Workflow
1. Validate specification input
2. Invoke @spec-analysis skill
   - Returns: 8D scores + domains
3. Skill chain executes:
   - @mcp-discovery (required)
   - @phase-planning (required)
   - @wave-orchestration (if complexity ≥0.50)
   - @context-preservation (required)
4. Present integrated results

## Usage
```
/sh_spec "Your specification text here"
```

## Output
[Standard 8D analysis format - identical to V3]
```

**Functional Test 5.1**:
```bash
# Test: Command still works identically
/sh_spec "Build a task manager with React and Node.js"

# Expected output (IDENTICAL to V3):
# - 📊 8-Dimensional Complexity Analysis
# - Complexity score with label
# - Domain breakdown
# - MCP recommendations
# - Phase plan
# - Wave plan (if applicable)
# - Checkpoint ID

# Validate: Output format unchanged from V3
```

**Acceptance Criteria**:
- [ ] sh_spec migrated to skill orchestrator
- [ ] Backward compatible: V3 users see no difference
- [ ] Skill chain executes correctly
- [ ] All 4 sub-skills invoked in order
- [ ] Output format identical to V3
- [ ] Performance: Complete in 2-5 minutes (same as V3)

---

### Task 5.2-5.9: Migrate Remaining Shannon Commands

**Commands to Migrate**:
- sh_wave (→ wave-orchestration skill)
- sh_checkpoint (→ context-preservation skill)
- sh_restore (→ context-restoration skill)
- sh_analyze (→ shannon-analysis skill)
- sh_memory (→ memory-coordination skill)
- sh_north_star (→ goal-management skill)
- sh_sitrep (NEW → sitrep-reporting skill)
- sh_index (NEW → project-indexing skill)

**Keep Unchanged**:
- sh_status (utility, no skill needed)
- sh_check_mcps (utility, no skill needed)

**Each command migration**:
1. Convert from monolithic to skill orchestrator
2. Add @skill invocation syntax
3. Maintain backward compatibility
4. Functional test: Identical output to V3
5. Performance test: Same or better than V3

---

### Task 5.10: Deprecate SuperClaude Commands

**Files to Modify**: All 24 sc_* command files

**Deprecation Pattern**:
```markdown
---
description: [Original description]
deprecated: true
deprecated-in: 4.0.0
replacement: [Shannon equivalent]
removal-planned: 5.0.0
---

# ⚠️ DEPRECATED: [Command Name]

**This command is deprecated as of Shannon V4.0.0**

**Replacement**: Use `[/sh_equivalent]` instead

**Why Deprecated**: Shannon V4 removes SuperClaude dependencies and provides equivalent functionality through native Shannon commands and skills.

**Migration Guide**:
```
Old: /sc_[name]
New: /sh_[equivalent]
```

**Deprecation Timeline**:
- V4.0-V4.9: This command still works but shows deprecation warning
- V5.0+: This command will be removed

## Original Documentation

[Keep original command documentation for reference during transition]
```

**Example - sc_analyze.md**:
```markdown
---
description: Code and architecture analysis
deprecated: true
deprecated-in: 4.0.0
replacement: /sh_analyze
removal-planned: 5.0.0
---

# ⚠️ DEPRECATED: sc_analyze

**This command is deprecated as of Shannon V4.0.0**

**Replacement**: Use `/sh_analyze` instead

Shannon V4's `/sh_analyze` provides equivalent functionality with:
- Skill-based architecture (more modular)
- Explicit MCP integration
- Better context preservation

**Migration**: Replace `/sc_analyze` with `/sh_analyze` in your workflows.
```

**Functional Test 5.10**:
```bash
# Test: Deprecated commands still work (backward compat)
/sc_analyze
# Expected: Works + shows deprecation warning

# Test: Warning message correct
/sc_analyze 2>&1 | grep "DEPRECATED"
# Expected: Match found

# Test: Replacement suggested
/sc_analyze 2>&1 | grep "/sh_analyze"
# Expected: Match found
```

**Acceptance Criteria**:
- [ ] All 24 sc_* commands marked deprecated
- [ ] Deprecation warnings display when used
- [ ] Shannon equivalents documented
- [ ] Commands still functional (backward compat)
- [ ] Removal timeline clear (v5.0.0)

---

## Wave 5 Summary

**Tasks**: 9 command migrations + 24 deprecations

**Files Modified**: 33 command files

**Lines Modified**: ~2000 lines (command rewrites + deprecation notices)

**Duration**: 1-2 weeks

**Wave 5 Validation**:
```bash
# Test ALL Shannon commands work identically to V3
/sh_spec "Build todo app" # ✓ Works
/sh_wave # ✓ Works
/sh_checkpoint test-checkpoint # ✓ Works
/sh_restore # ✓ Works
/sh_analyze # ✓ Works
/sh_memory # ✓ Works
/sh_north_star "Deliver v4" # ✓ Works
/sh_status # ✓ Works
/sh_check_mcps # ✓ Works

# Test NEW commands
/sh_sitrep # ✓ Works (new SITREP generation)
/sh_index # ✓ Works (new project indexing)

# Test deprecated commands show warnings
/sc_analyze 2>&1 | grep "DEPRECATED"
# Expected: Warning shown, but command executes

# Comprehensive validation
python3 shannon-plugin/tests/test_all_commands.py
# Expected: All commands pass
```

---

# Post-Migration Validation

## Complete System Test

**Test Suite**: `shannon-plugin/tests/test_v4_complete.py`

```python
#!/usr/bin/env python3
"""
Shannon V4 Complete System Validation

Functional tests for entire V4 system:
- All 14 skills operational
- All 11 commands work correctly
- Skill composition chains execute
- MCP integrations functional
- Context preservation works
- Backward compatibility maintained
"""

def test_complete_workflow():
    """Test: Complete /sh_spec → implementation workflow"""

    # Step 1: Specification analysis
    result = run_command('/sh_spec "Build task manager with React + Node.js"')

    assert "8-Dimensional Complexity Analysis" in result
    assert "Complexity:" in result
    assert "Domain Breakdown:" in result
    assert "MCP Recommendations:" in result
    assert "Phase Plan:" in result or "5-Phase" in result
    assert "Checkpoint:" in result

    # Step 2: Verify spec-analysis skill was invoked
    assert_skill_invoked("spec-analysis")

    # Step 3: Verify sub-skills invoked
    assert_skill_invoked("mcp-discovery")
    assert_skill_invoked("phase-planning")
    assert_skill_invoked("context-preservation")

    # Step 4: Verify checkpoint created in Serena
    checkpoint_id = extract_checkpoint_id(result)
    assert checkpoint_exists_in_serena(checkpoint_id)

    # Step 5: Test restoration
    restore_result = run_command(f'/sh_restore {checkpoint_id}')
    assert "Restored from checkpoint" in restore_result

    print("✅ Complete workflow test passed")

def test_wave_execution():
    """Test: Wave execution for complex project"""

    spec = """
    Build a real-time collaborative document editing platform with:
    - React frontend with Yjs CRDT
    - Node.js WebSocket backend
    - PostgreSQL + Redis databases
    - Kubernetes deployment
    """

    result = run_command(f'/sh_spec "{spec}"')

    # Should trigger wave planning (complexity ≥0.50)
    assert "Wave Execution Plan:" in result or "Wave 1:" in result
    assert_skill_invoked("wave-orchestration")

    # Should recommend 3-7 agents
    assert "agents" in result.lower()

    print("✅ Wave execution test passed")

def test_functional_testing_enforcement():
    """Test: NO MOCKS enforcement"""

    # Try to create a test with mocks
    test_code = '''
def test_login():
    mock_auth = Mock()
    assert mock_auth.login("user", "pass")
'''

    # Write test file
    write_file("test_example.py", test_code)

    # Should trigger post_tool_use hook
    # Hook should detect "Mock()" and block or warn

    # Verify hook triggered
    assert_hook_triggered("PostToolUse")

    # Verify warning/error about mock usage
    # (Implementation depends on hook behavior - block vs warn)

    print("✅ NO MOCKS enforcement test passed")

def test_sitrep_generation():
    """Test: SITREP protocol"""

    result = run_command('/sh_sitrep')

    assert "🎖️ SITREP:" in result
    assert "AUTH CODE:" in result
    assert "STATUS:" in result
    assert "## COMPLETED" in result
    assert "## IN PROGRESS" in result
    assert "## BLOCKED" in result

    print("✅ SITREP generation test passed")

def test_project_indexing():
    """Test: Project indexing with 90%+ token reduction"""

    result = run_command('/sh_index')

    assert "Shannon Project Index" in result
    assert "Quick Stats" in result
    assert "Entry Points" in result
    assert "Architecture Pattern" in result

    # Verify token count reduction
    original_tokens = estimate_codebase_tokens()
    index_tokens = estimate_index_tokens(result)
    reduction_percent = ((original_tokens - index_tokens) / original_tokens) * 100

    assert reduction_percent >= 90

    print(f"✅ Project indexing test passed ({reduction_percent:.1f}% reduction)")

def test_backward_compatibility():
    """Test: V3 commands work identically in V4"""

    v3_commands = [
        '/sh_spec "Build todo app"',
        '/sh_wave',
        '/sh_checkpoint test',
        '/sh_status',
    ]

    for cmd in v3_commands:
        result = run_command(cmd)
        assert result is not None
        assert "error" not in result.lower() or "Error" not in result

    print("✅ Backward compatibility test passed")

if __name__ == "__main__":
    test_complete_workflow()
    test_wave_execution()
    test_functional_testing_enforcement()
    test_sitrep_generation()
    test_project_indexing()
    test_backward_compatibility()

    print("\n" + "="*60)
    print("✅ ALL SHANNON V4 SYSTEM TESTS PASSED")
    print("="*60)
```

**Execute Complete Validation**:
```bash
python3 shannon-plugin/tests/test_v4_complete.py
# Expected: All 6 tests pass

# Additional manual testing
# Test in real Claude Code session:
# 1. Install Shannon V4 alpha
# 2. Run through complete workflow
# 3. Verify all commands work
# 4. Verify skills activate correctly
# 5. Verify context preservation works
# 6. Verify SITREP protocol works
```

---

# Migration Timeline

## Week-by-Week Breakdown

### Week 1: Wave 1 - Infrastructure
- Mon-Tue: Create skills/ directory, templates, validation
- Wed-Thu: Create using-shannon meta-skill
- Fri: Wave 1 validation and testing
- **Deliverable**: Infrastructure ready, 1 skill operational

### Week 2: Wave 2 Part 1 - Core Skills (spec-analysis, wave-orchestration, phase-planning)
- Mon-Tue: spec-analysis skill complete
- Wed: wave-orchestration skill complete
- Thu: phase-planning skill complete
- Fri: Test skill chain execution
- **Deliverable**: 3 core skills operational

### Week 3: Wave 2 Part 2 - Core Skills (context, testing, mcp-discovery)
- Mon: context-preservation + context-restoration skills
- Tue: functional-testing skill (Iron Laws)
- Wed: mcp-discovery skill
- Thu-Fri: Wave 2 complete validation
- **Deliverable**: 7 core skills operational

### Week 4: Wave 3 - Context & Memory Skills
- Mon-Tue: memory-coordination skill
- Wed: goal-management skill
- Thu: shannon-analysis skill
- Fri: Wave 3 validation
- **Deliverable**: 10 Shannon skills operational

### Week 5: Wave 4 - Enhanced Skills
- Mon-Tue: sitrep-reporting skill
- Wed: confidence-check skill
- Thu: project-indexing skill
- Fri: Wave 4 validation
- **Deliverable**: 13 skills operational (complete)

### Week 6: Wave 5 Part 1 - Command Migration
- Mon-Tue: Migrate sh_spec, sh_wave, sh_checkpoint
- Wed: Migrate sh_restore, sh_analyze, sh_memory
- Thu: Migrate sh_north_star, add sh_sitrep, sh_index
- Fri: Command migration validation
- **Deliverable**: All commands using skills

### Week 7: Wave 5 Part 2 - SuperClaude Deprecation
- Mon-Tue: Add deprecation notices to all 24 sc_* commands
- Wed: Test backward compatibility
- Thu: Update documentation
- Fri: Wave 5 validation
- **Deliverable**: Clean deprecation path

### Week 8: Final Validation & Release
- Mon-Tue: Complete system testing
- Wed: Documentation finalization
- Thu: Release preparation (changelog, migration guide)
- Fri: V4.0.0 release
- **Deliverable**: Shannon V4.0.0 production release

---

# Functional Testing Strategy

## Testing Philosophy (NO MOCKS)

Shannon V4 maintains Iron Law: **NO MOCK OBJECTS IN TESTS**

All tests must use:
- ✅ Real Claude Code sessions
- ✅ Real Serena MCP
- ✅ Real skill invocations
- ✅ Real checkpoint creation/restoration
- ✅ Real git operations

**No Allowed**:
- ❌ Mock MCP servers
- ❌ Mock skill responses
- ❌ Mock checkpoint storage
- ❌ Unit tests (functional tests only)

## Per-Wave Functional Tests

### Wave 1 Tests
```bash
tests/wave1/
├── test_skills_directory.sh (Directory structure validation)
├── test_template_exists.sh (Template file validation)
├── test_validation_script.sh (validate_skills.py works)
├── test_using_shannon.sh (Meta-skill activation)
└── test_session_start_hook.sh (Hook loads meta-skill)
```

### Wave 2 Tests
```bash
tests/wave2/
├── test_spec_analysis_simple.sh (Simple specification)
├── test_spec_analysis_complex.sh (Complex specification)
├── test_spec_analysis_critical.sh (Critical specification)
├── test_wave_orchestration.sh (Wave planning)
├── test_phase_planning.sh (Phase generation)
├── test_context_preservation.sh (Checkpoint creation)
├── test_context_restoration.sh (Checkpoint retrieval)
├── test_functional_testing.sh (NO MOCKS enforcement)
├── test_mcp_discovery.sh (MCP recommendations)
└── test_skill_composition.sh (Sub-skill chains)
```

### Wave 3 Tests
```bash
tests/wave3/
├── test_memory_coordination.sh (Serena queries)
├── test_goal_management.sh (North Star tracking)
└── test_shannon_analysis.sh (General analysis)
```

### Wave 4 Tests
```bash
tests/wave4/
├── test_sitrep_reporting.sh (SITREP generation)
├── test_confidence_check.sh (5-check validation)
└── test_project_indexing.sh (Token reduction validation)
```

### Wave 5 Tests
```bash
tests/wave5/
├── test_command_migration.sh (All 9 commands work via skills)
├── test_backward_compatibility.sh (V3 behavior preserved)
├── test_sc_deprecation.sh (Deprecation warnings shown)
└── test_complete_workflow.sh (End-to-end validation)
```

## Test Execution

**Per-Wave**:
```bash
# After completing Wave N
cd shannon-plugin
bash tests/wave{N}/test_*.sh

# All tests must pass before proceeding to Wave N+1
```

**Complete Suite**:
```bash
# After Wave 5 complete
python3 shannon-plugin/tests/test_v4_complete.py

# Expected: All tests pass
# Expected: Zero failures
# Expected: Backward compatibility 100%
```

---

# Rollback Procedures

## Wave-Level Rollback

**If Wave N fails validation**:

```bash
# Example: Wave 2 fails
git log --oneline | head -20
# Find last commit before Wave 2

git reset --hard <commit-before-wave-2>
git push origin shannon-v4-migration --force

# Verify rollback
python3 shannon-plugin/tests/validate_skills.py
# Expected: Only Wave 1 skills present

# Resume from failed wave
# Fix issues, restart Wave 2
```

## Complete Migration Rollback

**If entire V4 migration needs to be abandoned**:

```bash
# Return to V3
git checkout main
git branch -D shannon-v4-migration

# Verify V3 operational
/sh_status
# Expected: Shannon v3.0.1 active

# Restore from backup tag
git checkout v3.0.1-backup
```

**Data Loss**: ZERO (Serena MCP preserves all checkpoints regardless of git state)

---

# Success Criteria

## Technical Success

Shannon V4 migration is successful when:

- ✅ All 14 skills implemented with complete specifications
- ✅ All 14 skills pass structural validation (validate_skills.py)
- ✅ All 11 Shannon commands delegate to skills correctly
- ✅ All 9 core commands maintain V3 behavior (backward compatible)
- ✅ 2 new commands operational (sh_sitrep, sh_index)
- ✅ 24 SuperClaude commands deprecated with migration notices
- ✅ All functional tests pass (30+ tests across 5 waves)
- ✅ using-shannon meta-skill auto-loads via SessionStart hook
- ✅ Serena MCP integration operational (checkpoints, restoration)
- ✅ SITREP protocol functional for multi-agent coordination
- ✅ Progressive disclosure working (references/ loaded only when needed)
- ✅ MCP fallback chains validated (graceful degradation)
- ✅ Performance maintained or improved vs V3
- ✅ Documentation complete (architecture doc + migration plan)
- ✅ Plugin manifest updated (v4.0.0)

## User Experience Success

- ✅ V3 users can upgrade without learning new syntax
- ✅ Commands work identically (same inputs, same outputs)
- ✅ New capabilities available for users who want them
- ✅ Migration guide helps users leverage V4 features
- ✅ Deprecation warnings are helpful, not annoying
- ✅ /sh_status shows V4 active with feature overview
- ✅ Installation identical (/plugin install shannon@shannon-framework)
- ✅ Zero complaints about breaking changes

## Quality Success

- ✅ All skills have success criteria defined
- ✅ All skills have common pitfalls documented
- ✅ All skills have minimum 3 examples
- ✅ All skills tested under production conditions
- ✅ Validation automation passes (structure + behavioral + functional)
- ✅ No mock objects in any test (Iron Law maintained)
- ✅ Documentation quality ≥ V3 (target: 9.5/10 vs V3's 9.2/10)

---

# Risk Mitigation

## Identified Risks & Mitigation

### Risk 1: Serena MCP Unavailable
**Probability**: Medium
**Impact**: HIGH (migration blocked without Serena)

**Mitigation**:
- Pre-flight check: Verify Serena operational before starting migration
- Fallback: Implement local-storage fallback for all context preservation
- Degradation: Document cross-session limitations without Serena
- Rollback: Can complete migration with local storage, upgrade to Serena later

### Risk 2: Skill Composition Bugs
**Probability**: Medium
**Impact**: Medium (broken workflows)

**Mitigation**:
- Test each sub-skill independently before composition
- Validate composition chains in isolation
- Comprehensive functional tests for all chains
- Rollback: Fix individual skills without reverting entire wave

### Risk 3: Backward Compatibility Breaks
**Probability**: Low-Medium
**Impact**: HIGH (user disruption)

**Mitigation**:
- Extensive testing of V3 command behavior in V4
- Automated regression tests comparing V3 vs V4 outputs
- Beta testing period (4.0.0-alpha.1 → 4.0.0-beta.1 → 4.0.0)
- Rollback: V3 branch maintained, users can downgrade

### Risk 4: Performance Degradation
**Probability**: Low
**Impact**: Medium (user experience)

**Mitigation**:
- Performance benchmarks: V3 vs V4 execution time
- Token consumption monitoring: Ensure progressive disclosure works
- Load testing: Multiple skill invocations
- Optimization: Skill caching if needed

### Risk 5: Validation Automation Gaps
**Probability**: Medium
**Impact**: Low (quality issues)

**Mitigation**:
- Comprehensive test coverage (30+ functional tests)
- Manual validation checklist for each wave
- Community beta testing before production release
- Continuous monitoring after release

---

# Post-Migration Checklist

After completing all 5 waves:

- [ ] All 14 skills pass validation
- [ ] All 11 commands work correctly
- [ ] All 30+ functional tests pass
- [ ] Backward compatibility confirmed (V3 behavior preserved)
- [ ] Performance validated (same or better than V3)
- [ ] Documentation updated (README, CHANGELOG, migration guide)
- [ ] Plugin manifest updated (version 4.0.0)
- [ ] Git commits clean (good messages, logical structure)
- [ ] Serena MCP checkpoints validated
- [ ] Community beta tested (5+ users)
- [ ] Issues addressed (bug fixes, documentation clarifications)
- [ ] Release notes prepared
- [ ] Changelog updated
- [ ] GitHub release created
- [ ] Plugin marketplace updated
- [ ] Announcement prepared (blog post, Discord, GitHub)

---

# Appendix: Wave Execution Commands

## Execute Wave 1
```bash
cd shannon-framework
git checkout -b wave-1-infrastructure

# Task 1.1
mkdir -p shannon-plugin/skills
# [Create files...]

# Task 1.2
# [Create template...]

# Task 1.3
# [Create validation...]

# Task 1.4
# [Create using-shannon...]

# Task 1.5
# [Update plugin.json...]

# Validate
python3 shannon-plugin/tests/validate_skills.py
# Expected: ✅ 1/1 skills valid

# Commit
git add shannon-plugin/skills/ shannon-plugin/templates/ shannon-plugin/tests/ shannon-plugin/hooks/ shannon-plugin/.claude-plugin/
git commit -m "feat(v4): Wave 1 - Core infrastructure

- Create skills/ directory structure
- Add SKILL_TEMPLATE.md
- Add validation infrastructure (validate_skills.py)
- Create using-shannon meta-skill
- Add SessionStart hook for meta-skill loading
- Update plugin.json to v4.0.0-alpha.1

Wave 1/5 complete ✅"

# Merge to development
git checkout shannon-v4-migration
git merge wave-1-infrastructure
```

## Execute Wave 2
[Similar pattern for each wave]

---

# Appendix: Skill Implementation Order

**Dependency-Ordered Implementation**:

1. **Level 0** (No dependencies): Implement first
   - context-preservation
   - mcp-discovery
   - project-indexing

2. **Level 1** (Depends on Level 0):
   - phase-planning (uses mcp-discovery)
   - functional-testing
   - confidence-check

3. **Level 2** (Depends on Level 0-1):
   - spec-analysis (uses mcp-discovery, phase-planning, context-preservation)
   - wave-orchestration (uses context-preservation)
   - shannon-analysis

4. **Level 3** (Depends on Level 0-2):
   - sitrep-reporting
   - memory-coordination
   - goal-management
   - context-restoration

**Implementation Strategy**: Bottom-up (Level 0 → Level 3) ensures all dependencies available when needed.

---

# Document Complete

**Shannon Framework V4 - Executable Migration Plan**

**Status**: ✅ Complete and Ready for Execution

**Total Waves**: 5
**Total Tasks**: 40+ individual tasks
**Total Functional Tests**: 30+ tests
**Timeline**: 6-8 weeks
**Risk Level**: Medium (mitigated with rollback procedures)

**Next Step**: Begin Wave 1 execution

---

**Document Prepared By**: Shannon Framework Development Team
**Last Updated**: 2025-11-03
**Version**: 4.0.0-migration-plan-v1
**Related Document**: 2025-11-03-shannon-v4-architecture-design.md (architectural specification)

---
