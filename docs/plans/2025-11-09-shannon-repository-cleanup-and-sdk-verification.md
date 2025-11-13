# Shannon Repository Complete Cleanup & SDK Verification Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Clean Shannon repository to pure v5.0 state, save all SDK documentation, verify all metadata correct, and establish working SDK testing pattern.

**Architecture:** Systematic cleanup → Documentation verification → SDK pattern establishment → v5 testing foundation

**Tech Stack:** Shannon Framework v5.0 (pure), Claude Agents SDK Python 0.1.6, Serena MCP

---

## Phase 1: Save All SDK Documentation to docs/ref/

### Task 1.1: Fetch and Save Agent SDK Documentation

**Files:**
- Create: `docs/ref/agent-sdk-overview.md`
- Create: `docs/ref/agent-sdk-streaming-vs-single.md`
- Create: `docs/ref/agent-sdk-mcp.md`
- Create: `docs/ref/agent-sdk-subagents.md`
- Create: `docs/ref/agent-sdk-custom-tools.md`
- Create: `docs/ref/agent-sdk-modifying-prompts.md`
- Create: `docs/ref/agent-sdk-sessions.md`
- Create: `docs/ref/agent-sdk-skills.md`
- Create: `docs/ref/agent-sdk-slash-commands.md`

**Step 1: Fetch remaining SDK docs**

Already have:
- ✅ agent-sdk-python-api-reference.md (from python-agent-sdk.md rename)
- ✅ agent-sdk-plugins.md (created)
- ✅ claude-code-cli-plugins.md (created)

Need to fetch and save:
```python
docs_to_fetch = [
    ("https://docs.claude.com/en/docs/agent-sdk/overview", "agent-sdk-overview.md"),
    ("https://docs.claude.com/en/docs/agent-sdk/streaming-vs-single-mode", "agent-sdk-streaming-vs-single.md"),
    ("https://docs.claude.com/en/docs/agent-sdk/mcp", "agent-sdk-mcp.md"),
    ("https://docs.claude.com/en/docs/agent-sdk/subagents", "agent-sdk-subagents.md"),
    ("https://docs.claude.com/en/docs/agent-sdk/custom-tools", "agent-sdk-custom-tools.md"),
    ("https://docs.claude.com/en/docs/agent-sdk/modifying-system-prompts", "agent-sdk-modifying-prompts.md"),
    ("https://docs.claude.com/en/docs/agent-sdk/sessions", "agent-sdk-sessions.md"),
]
```

**Step 2: Save Claude Code CLI docs**

```python
cli_docs_to_fetch = [
    ("https://code.claude.com/docs/en/plugins", "claude-code-plugins.md"),
    ("https://code.claude.com/docs/en/skills", "claude-code-skills.md"),
    ("https://code.claude.com/docs/en/slash-commands", "claude-code-slash-commands.md"),
]
```

**Step 3: Verify all reference docs present**

Run: `ls docs/ref/*.md | wc -l`
Expected: >= 18 files (4 specs + 14+ SDK/CLI docs)

**Step 4: Create reference index**

Create: `docs/ref/README.md`
```markdown
# Shannon Reference Documentation

## Test Specifications (4)
- prd-creator-spec.md
- claude-code-expo-spec.md
- repo-nexus-spec.md
- shannon-cli-spec.md

## Agent SDK Documentation (10+)
- agent-sdk-python-api-reference.md (complete API)
- agent-sdk-plugins.md
- agent-sdk-skills.md
...

## Claude Code CLI Documentation (3)
- claude-code-plugins.md
- claude-code-skills.md
- claude-code-slash-commands.md
```

**Step 5: Commit**

```bash
git add docs/ref/
git commit -m "docs: add complete SDK and CLI reference documentation

Add 10+ SDK and CLI documentation files to docs/ref/ for permanent reference:
- Agent SDK: plugins, skills, sessions, custom-tools, etc.
- Claude Code CLI: plugins, skills, slash-commands

Enables offline reference and prevents re-fetching documentation."
```

---

## Phase 2: Verify Repository Metadata Correctness

### Task 2.1: Verify and Update plugin.json

**Files:**
- Read: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/plugin.json` (if needed)

**Step 1: Check current command/skill/agent counts**

```bash
# Count actual files
ls commands/*.md | wc -l  # Should be 14
ls skills/*/SKILL.md | wc -l  # Should be 17
ls agents/*.md | wc -l  # Should be 24
```

**Step 2: Compare with plugin.json**

Read plugin.json and verify:
- Commands count matches (should update if wrong)
- Skills count matches
- Version is 4.1.0 (correct for v5 base)
- No references to sc_* commands

**Step 3: Update plugin.json if needed**

If counts wrong, update metadata sections.

**Step 4: Commit if changed**

```bash
git add .claude-plugin/plugin.json
git commit -m "fix: update plugin.json metadata after sc_* removal"
```

### Task 2.2: Verify and Update README.md

**Files:**
- Read: `README.md` (complete - 2500+ lines)
- Modify: `README.md`

**Step 1: Search for sc_* references**

```bash
grep -n "sc_\|SuperClaude Enhanced\|48 Commands" README.md
```

**Step 2: Update command counts**

Change:
- "48 Commands" → "14 Commands"
- Remove "SuperClaude Enhanced (35)" sections
- Update component architecture section

**Step 3: Remove SuperClaude sections**

Search for sections titled "SuperClaude Enhanced Commands" and remove completely.

**Step 4: Verify all command lists**

Ensure only sh_* and shannon_prime commands listed.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: update README after sc_* command removal

Update README.md to reflect Shannon v5.0 structure:
- Commands: 48 → 14 (pure Shannon only)
- Remove SuperClaude Enhanced sections
- Update component architecture
- Verify all command references"
```

### Task 2.3: Clean Test Directory

**Files:**
- Review: `tests/` directory
- Delete: Debug/experimental test files

**Step 1: List all test files**

```bash
ls tests/*.py
```

**Step 2: Identify files to keep vs delete**

KEEP:
- tier1_verify_analysis.py (will fix)
- tier2_build_*.py (will fix)
- run_all_verification.py
- requirements.txt
- README.md

DELETE (debug/experimental):
- test_plugin_loads.py
- test_message_attributes.py
- test_sdk_command_debug.py
- test_subprocess_shannon.py
- All other test_*.py files created during debugging

**Step 3: Delete debug files**

```bash
rm tests/test_plugin_*.py
rm tests/test_message_*.py
rm tests/test_sdk_*.py
rm tests/test_subprocess_*.py
rm tests/test_correct_*.py
rm tests/test_with_*.py
rm tests/debug_*.py
```

**Step 4: Verify only essential files remain**

```bash
ls tests/*.py
# Should show: tier1_*, tier2_*, run_all_*
```

**Step 5: Commit**

```bash
git add tests/
git commit -m "chore: remove debug test files, keep only v5 verification scripts"
```

---

## Phase 3: Document Current State Completely

### Task 3.1: Create Current State Inventory

**Files:**
- Create: `docs/CURRENT_STATE.md`

**Step 1: Write complete inventory**

```markdown
# Shannon Framework - Current State (2025-11-09)

## Repository
- Branch: feature/v5.0-functional-testing
- Version: 4.1.0 (base for v5.0)
- Clean: Yes (sc_* removed, session artifacts archived)

## Shannon Plugin Structure

### Commands (14 total)
**Core (11)**:
1. sh_spec.md (159 lines) - 8D complexity analysis
2. sh_wave.md (420 lines) - Wave orchestration
...

**V4.1 NEW (3)**:
12. sh_discover_skills.md (272 lines)
13. sh_reflect.md (105 lines)
14. shannon_prime.md (449 lines)

### Skills (17 total)
1. spec-analysis (1,544 lines) - QUANTITATIVE
2. wave-orchestration (1,581 lines) - QUANTITATIVE
...

### Agents (24 total)
1. WAVE_COORDINATOR - Wave execution
...

### Core Patterns (9 total)
1. SPEC_ANALYSIS.md (1,786 lines)
...

### Hooks (6 total)
...

## What Shannon Does

Shannon Framework is a Claude Code plugin that:
1. Analyzes specifications using 8D complexity framework
2. Executes wave-based parallel development
3. Enforces NO MOCKS functional testing
4. Preserves context via Serena MCP
5. Provides goal management
6. Auto-discovers skills

## How to Use Shannon

### Interactive Claude Code:
```
/plugin install shannon@shannon-framework
/shannon:spec "Build a web app..."
/shannon:wave 1
```

### Via SDK (Python):
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": "./shannon-plugin"}],
    setting_sources=["user", "project"],  # REQUIRED!
    permission_mode="bypassPermissions"
)

async for msg in query("/shannon:spec '...'", options):
    # Process messages
```

## v5.0 Goal

Test Shannon by:
1. Building 4 complete applications via Shannon
2. Verifying they actually work (not string parsing)
3. Three-layer verification: Flow + Artifacts + Functionality
```

**Step 2: Commit**

```bash
git add docs/CURRENT_STATE.md
git commit -m "docs: add complete current state inventory for v5.0"
```

### Task 3.2: Update CLAUDE.md with Current Work

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Read current CLAUDE.md**

Check what it says about current work.

**Step 2: Update status**

```markdown
**Current Work**: Shannon v5.0 Cleanup & SDK Verification
- Branch: feature/v5.0-functional-testing
- Phase: Repository cleanup complete, SDK testing next
- Status: Removed 25 sc_* legacy commands, saving SDK docs, verifying metadata
```

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with current v5.0 status"
```

---

## Phase 4: Fix SDK Testing with Verified Pattern

### Task 4.1: Create SDK Knowledge Document

**Files:**
- Create: `docs/SDK_VERIFIED_PATTERN.md`

**Step 1: Document the verified working pattern**

```markdown
# Claude Agents SDK - Verified Working Pattern for Shannon

## CRITICAL Requirements

1. **setting_sources REQUIRED**:
```python
setting_sources=["user", "project"]  # Plugins/skills won't load without this
```

2. **Message handling - isinstance()** (NOT .type):
```python
if isinstance(message, AssistantMessage):
    for block in message.content:
        if isinstance(block, TextBlock):
            text = block.text
```

3. **API key before import**:
```python
import os
os.environ['ANTHROPIC_API_KEY'] = "..."
from claude_agent_sdk import query  # AFTER setting key
```

## Complete Working Example

[Full working code]
```

**Step 2: Commit**

```bash
git add docs/SDK_VERIFIED_PATTERN.md
git commit -m "docs: add verified SDK usage pattern for Shannon testing"
```

### Task 4.2: Fix tier1_verify_analysis.py

**Files:**
- Modify: `tests/tier1_verify_analysis.py`

**Step 1: Add setting_sources to ClaudeAgentOptions**

Find line ~175:
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": str(plugin_path)}],
    model="claude-sonnet-4-5",
    permission_mode="bypassPermissions"
)
```

Change to:
```python
options = ClaudeAgentOptions(
    plugins=[{"type": "local", "path": str(plugin_path)}],
    setting_sources=["user", "project"],  # REQUIRED for plugins!
    model="claude-sonnet-4-5",
    permission_mode="bypassPermissions",
    allowed_tools=["Skill"]  # Enable Skill tool
)
```

**Step 2: Test the fixed script**

```bash
python tests/tier1_verify_analysis.py
```

Expected: Shannon commands now available, /shannon:spec produces output

**Step 3: Commit if working**

```bash
git add tests/tier1_verify_analysis.py
git commit -m "fix: add setting_sources to enable Shannon plugin loading via SDK"
```

### Task 4.3: Fix all tier2 scripts

**Files:**
- Modify: `tests/tier2_build_prd_creator.py`
- Modify: `tests/tier2_build_mobile_expo.py`
- Modify: `tests/tier2_build_repo_nexus.py`
- Modify: `tests/tier2_build_shannon_cli.py`

**Step 1: Add setting_sources to each**

Same change as tier1: add `setting_sources=["user", "project"]`

**Step 2: Verify all use correct message handling**

Ensure all use isinstance() checks, not .type

**Step 3: Test one to verify pattern**

```bash
python tests/tier2_build_prd_creator.py --dry-run
```

**Step 4: Commit**

```bash
git add tests/tier2_*.py
git commit -m "fix: add setting_sources to all tier2 verification scripts"
```

### Task 4.4: Update SDK Testing Skill

**Files:**
- Modify: `.claude/skills/testing-claude-plugins-with-python-sdk/SKILL.md`

**Step 1: Rewrite skill with CORRECT API**

Based on verified knowledge:
- Use isinstance() not .type
- Iterate message.content blocks
- Add setting_sources requirement
- Add working examples from successful tests

**Step 2: Test skill by reading it**

Verify skill now shows correct patterns.

**Step 3: Commit**

```bash
git add .claude/skills/testing-claude-plugins-with-python-sdk/
git commit -m "fix: update SDK testing skill with verified API patterns

Correct message handling (isinstance not .type)
Add setting_sources requirement
Add working examples from successful tests"
```

---

## Phase 5: Verification & Testing

### Task 5.1: Test Shannon Commands via SDK

**Step 1: Run tier1 verification**

```bash
python tests/tier1_verify_analysis.py
```

Expected: 4/4 specs analyzed successfully

**Step 2: Document results to Serena**

If passing, write success memory.
If failing, document specific failures.

**Step 3: Fix any remaining issues**

Iterate until tier1 passes.

### Task 5.2: Test One Complete Build

**Step 1: Run PRD Creator build**

```bash
python tests/tier2_build_prd_creator.py
```

Expected: Shannon builds complete application

**Step 2: Verify build outputs**

Check:
- Files created
- Servers can start
- Tests exist and pass

**Step 3: Document results**

### Task 5.3: Update v5 Plan

**Files:**
- Modify: `docs/plans/2025-11-09-shannon-v5-functional-testing-plan.md`

**Step 1: Update Phase 1 status**

Mark as ACTUALLY complete (with sc_* removal)

**Step 2: Update Phase 2 approach**

Note: Using SDK with setting_sources, not subprocess

**Step 3: Update verification methodology**

Reference verification skill and three-layer approach

---

## Phase 6: Final Documentation

### Task 6.1: Update Session State in Serena

**Step 1: Write complete synthesis memory**

```python
mcp__serena__write_memory(
    "SHANNON_V5_CLEANUP_COMPLETE_SYNTHESIS",
    content="""
    # Complete
    - Removed 25 sc_* legacy commands
    - Saved 14+ SDK documentation files
    - Fixed plugin.json and README
    - Established working SDK pattern
    - Ready for v5 verification
    """
)
```

### Task 6.2: Create Handoff Document

**Files:**
- Create: `docs/plans/sessions/v5-cleanup-session-handoff.md`

Document what was done, what was learned, current state, next steps.

---

## Success Criteria

- ✅ All SDK docs saved to docs/ref/ (14+ files)
- ✅ sc_* commands removed (25 files deleted)
- ✅ README updated (correct command count)
- ✅ plugin.json verified (correct metadata)
- ✅ Test directory clean (only essential files)
- ✅ SDK pattern verified (tier1 tests pass)
- ✅ Documentation complete (CURRENT_STATE.md, handoff)

---

## Timeline

- Phase 1: 30 minutes (save docs)
- Phase 2: 15 minutes (verify metadata)
- Phase 3: 20 minutes (document state)
- Phase 4: 45 minutes (fix SDK tests)
- Phase 5: 60 minutes (verification)
- Phase 6: 30 minutes (final docs)

**Total**: ~3 hours

---

**Plan saved**: `docs/plans/2025-11-09-shannon-repository-cleanup-and-sdk-verification.md`
