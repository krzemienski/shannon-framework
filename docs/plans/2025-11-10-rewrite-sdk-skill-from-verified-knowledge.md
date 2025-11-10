# Rewrite SDK Testing Skill from Verified Official Documentation

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Completely rewrite testing-claude-plugins-with-python-sdk skill from scratch using verified official documentation, eliminating all incorrect patterns.

**Problem**: Current skill has wrong API (message.type instead of isinstance), outdated patterns, incomplete examples. Must rebuild from official SDK docs.

**Approach**: Deep documentation reading → Complete understanding → Skill reconstruction → Systematic testing → Verified foundation

---

## Phase 1: Complete SDK Documentation Mastery (3-4 hours)

### Task 1.1: Read ALL SDK Docs Line-by-Line

**Files to Read:**
- docs/ref/agent-sdk-python-api-reference.md (1847 lines) - COMPLETE
- docs/ref/agent-sdk-overview.md - COMPLETE
- docs/ref/agent-sdk-plugins.md - COMPLETE
- docs/ref/agent-sdk-skills.md - COMPLETE
- docs/ref/agent-sdk-sessions.md - COMPLETE
- docs/ref/agent-sdk-slash-commands.md - COMPLETE
- docs/ref/agent-sdk-streaming-vs-single.md - COMPLETE
- docs/ref/agent-sdk-mcp.md - COMPLETE
- docs/ref/agent-sdk-subagents.md - COMPLETE
- docs/ref/agent-sdk-custom-tools.md - COMPLETE
- docs/ref/agent-sdk-modifying-prompts.md - COMPLETE
- docs/ref/agent-sdk-todo-tracking.md - COMPLETE

**Step 1: Read python-api-reference.md (1847 lines)**

Read EVERY line, not skimming.
Extract ALL Python examples.
Document message types, content blocks, patterns.

**Step 2: Read each remaining doc completely**

For each file:
- Read every line
- Extract all Python examples
- Note patterns
- Document requirements

**Step 3: Create extraction document**

File: `docs/SDK_PATTERNS_EXTRACTED.md`

Content:
```markdown
# SDK Patterns Extracted from Official Docs

## Message Types (from python-api-reference.md lines 742-800)

```python
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage

@dataclass
class AssistantMessage:
    content: list[ContentBlock]
    model: str

@dataclass
class SystemMessage:
    subtype: str
    data: dict[str, Any]

@dataclass
class ResultMessage:
    session_id: str
    total_cost_usd: float | None
    usage: dict[str, Any] | None
```

## Content Blocks (lines 804-855)

[Complete extraction]

## Plugin Loading (from agent-sdk-plugins.md)

[Complete pattern with setting_sources]

## All Python Examples Extracted

[Every example from all 12 docs]
```

**Step 4: Ultrathink 300 thoughts**

Use Sequential MCP:
```python
mcp__sequential-thinking__sequentialthinking(
    thought="Synthesizing complete SDK knowledge from 12 docs...",
    thoughtNumber=1,
    totalThoughts=300
)
```

Topics:
- How messages actually work
- How plugin loading actually works
- setting_sources requirement
- Message vs content block distinction
- All Python patterns
- Common errors and fixes

**Step 5: Document synthesis to Serena**

```python
mcp__serena__write_memory(
    "CLAUDE_AGENTS_SDK_COMPLETE_MASTERY",
    content="[300-thought synthesis results]"
)
```

### Task 1.2: Test ALL Official Examples

**Files:**
- Create: `tests/sdk-examples/` directory
- Create test file for each example from docs

**Step 1: Extract examples**

From SDK_PATTERNS_EXTRACTED.md, create executable test for each Python example.

**Step 2: Run each example**

```bash
python tests/sdk-examples/example_1_basic_query.py
python tests/sdk-examples/example_2_with_options.py
...
```

Expected: ALL examples work

**Step 3: Document which patterns work**

Create: `tests/sdk-examples/VERIFIED_PATTERNS.md`

List every working pattern with "✅ VERIFIED"

---

## Phase 2: Skill Reconstruction (2-3 hours)

### Task 2.1: Design New Skill Structure

**File:**
- Create: `.claude/skills/testing-claude-plugins-with-python-sdk-v2/design.md`

**Content:**
```markdown
# SDK Testing Skill v2 - Design

## What This Skill Teaches

1. CORRECT message handling (isinstance, not .type)
2. CORRECT plugin loading (setting_sources required)
3. CORRECT content access (iterate blocks)
4. All verified Python examples from official docs
5. Common errors and how to avoid them

## Structure

### Section 1: Installation
- pip install claude-agent-sdk
- Set ANTHROPIC_API_KEY
- Verify installation

### Section 2: Message Handling (CRITICAL)
- Message classes (not .type attribute)
- isinstance() pattern
- Content block iteration
- TextBlock, ToolUseBlock patterns

### Section 3: Plugin Loading
- setting_sources requirement (**CRITICAL**)
- Path specifications
- Verification pattern

### Section 4: Complete Examples
- Basic query
- Plugin loading
- Message processing
- Tool tracking
- Cost tracking

### Section 5: Common Errors
- Missing setting_sources
- Using .type instead of isinstance
- Not iterating content blocks
- API key not set

### Section 6: Testing Patterns
- How to test plugins via SDK
- How to verify plugin loaded
- How to check commands available
- Complete test script template
```

**Step 2: Review design**

Does this cover everything needed?
Based on verified patterns?
No incorrect information?

### Task 2.2: Write Complete New Skill

**File:**
- Create: `.claude/skills/testing-claude-plugins-with-python-sdk-v2/SKILL.md`

**Step 1: Write YAML frontmatter**

```yaml
---
name: testing-claude-plugins-with-python-sdk-v2
description: Complete verified guide for Claude Agents SDK Python based on official documentation. Covers correct message handling (isinstance not .type), plugin loading (setting_sources required), content block iteration, and all verified patterns. Use when testing Claude Code plugins programmatically or building SDK applications.
skill-type: PROTOCOL
version: "2.0.0"
based-on: "Official SDK docs (12 files, 1847 lines read completely)"
verified: true
---
```

**Step 2: Write complete skill content**

Structure:
1. Installation and Setup
2. CRITICAL Requirements (setting_sources, isinstance)
3. Message Handling Patterns (with examples)
4. Plugin Loading Patterns (with examples)
5. Complete Working Examples (verified)
6. Common Errors and Solutions
7. Testing Patterns
8. Quick Reference

Minimum: 1000 lines (comprehensive)
Based entirely on verified official docs
NO guessing, NO outdated patterns

**Step 3: Include ALL working examples from Phase 1**

Every example tested and verified goes in skill.

**Step 4: Add troubleshooting section**

Based on errors encountered:
- "plugins: [] empty" → Missing setting_sources
- "No output from command" → Command not loaded
- etc.

### Task 2.3: Delete Old Skill

**Step 1: Archive old skill**

```bash
mv .claude/skills/testing-claude-plugins-with-python-sdk \
   .claude/skills/testing-claude-plugins-with-python-sdk-OLD-INCORRECT
```

**Step 2: Activate new skill**

```bash
mv .claude/skills/testing-claude-plugins-with-python-sdk-v2 \
   .claude/skills/testing-claude-plugins-with-python-sdk
```

**Step 3: Verify skill loads**

Ask Claude: "What SDK skills are available?"
Should mention the testing skill.

**Step 4: Delete old after verification**

```bash
rm -rf .claude/skills/testing-claude-plugins-with-python-sdk-OLD-INCORRECT
```

---

## Phase 3: Skill Testing and Validation (1-2 hours)

### Task 3.1: Test Skill by Reading It

**Step 1: Load skill in new session**

Start fresh Claude Code session.
Type: "I need help with Claude Agents SDK Python"

**Step 2: Verify skill activates**

Claude should say: "I'm using testing-claude-plugins-with-python-sdk skill..."

**Step 3: Check patterns provided**

Ask: "How do I handle messages from SDK?"
Expected: Correct isinstance() pattern, not .type

**Step 4: Check examples work**

Ask: "Show me example of loading plugin"
Expected: Includes setting_sources

### Task 3.2: Test Skill Patterns in Code

**File:**
- Create: `tests/test_skill_patterns.py`

**Step 1: Write test using skill patterns**

```python
#!/usr/bin/env python3
"""
Test that skill patterns actually work

Based on patterns from testing-claude-plugins-with-python-sdk skill
"""

import os
os.environ['ANTHROPIC_API_KEY'] = "..."

# Import patterns from skill
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def test_basic_pattern():
    """Test basic pattern from skill"""

    # Pattern from skill Section 2
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        setting_sources=["user", "project"],  # From skill
        permission_mode="bypassPermissions"
    )

    # Message handling from skill Section 3
    texts = []
    async for msg in query("hello", options):
        if isinstance(msg, AssistantMessage):  # From skill
            for block in msg.content:  # From skill
                if isinstance(block, TextBlock):  # From skill
                    texts.append(block.text)  # From skill

    assert len(texts) > 0, "Should get response"
    return True

# Test all patterns from skill
asyncio.run(test_basic_pattern())
```

**Step 2: Run test**

```bash
python tests/test_skill_patterns.py
```

Expected: ✅ PASS (all skill patterns work)

**Step 3: If fails**

- Skill has incorrect pattern
- Fix skill
- Retest
- Repeat until passing

### Task 3.3: Validate Against Official Docs

**Step 1: Compare skill to docs**

For each pattern in skill:
- Find corresponding section in official docs
- Verify pattern matches exactly
- Check no deviations or "improvements"

**Step 2: Check completeness**

Does skill cover:
- ✅ Message types?
- ✅ Content blocks?
- ✅ Plugin loading?
- ✅ setting_sources?
- ✅ Common errors?
- ✅ Working examples?

**Step 3: Mark as verified**

Add to skill frontmatter:
```yaml
verified: true
verified-date: "2025-11-10"
based-on: "Official docs v0.1.6"
```

---

## Phase 4: Use Rewritten Skill for v5 Testing (Resume v5)

### Task 4.1: Rewrite Test Scripts Using Skill

**Files:**
- Rewrite: `tests/tier1_verify_analysis.py`
- Rewrite: `tests/tier2_build_*.py`

**Step 1: Open skill**

```python
Skill("testing-claude-plugins-with-python-sdk")
```

**Step 2: Copy patterns EXACTLY from skill**

Don't deviate, don't "improve", don't guess.
Use skill's patterns verbatim.

**Step 3: Test scripts work**

```bash
python tests/tier1_verify_analysis.py
```

Expected: Works because using verified skill patterns

### Task 4.2: Resume v5 Comprehensive Verification

Now that SDK skill is correct and working:

1. Run tier1 (analyze 4 specs)
2. Run tier2 (build applications)
3. Verify builds work
4. Document results
5. Complete v5

---

## Success Criteria

**Phase 1 Complete When:**
- ✅ All 12 SDK docs read completely (every line)
- ✅ All Python examples extracted
- ✅ 300+ sequential thoughts completed
- ✅ Complete synthesis documented
- ✅ All official examples tested and work

**Phase 2 Complete When:**
- ✅ New skill written from scratch (1000+ lines)
- ✅ Based entirely on verified official docs
- ✅ No incorrect patterns
- ✅ Old skill deleted
- ✅ New skill activated

**Phase 3 Complete When:**
- ✅ Skill loads in Claude Code
- ✅ Skill provides correct patterns
- ✅ All skill patterns tested and work
- ✅ Validated against official docs
- ✅ Marked as verified

**Phase 4 Complete When:**
- ✅ Test scripts rewritten using skill
- ✅ tier1 runs successfully
- ✅ Shannon loads via SDK
- ✅ Commands produce output
- ✅ v5 testing can proceed

---

## Timeline

- Phase 1: 3-4 hours (deep learning, no rushing)
- Phase 2: 2-3 hours (complete skill rewrite)
- Phase 3: 1-2 hours (systematic testing)
- Phase 4: Resume v5 execution

**Total**: 6-9 hours (thorough, no shortcuts)

---

## Critical Requirements

1. **Read every line** of every SDK doc (no skimming)
2. **Extract every example** and test it works
3. **Ultrathink 300+ thoughts** to synthesize knowledge
4. **Rewrite skill from scratch** (don't edit old one)
5. **Test every pattern** before declaring complete
6. **No rushing** - thoroughness over speed

---

**Plan Purpose**: Create CORRECT SDK foundation through systematic learning and reconstruction, not quick fixes.
