---
name: shannon:do
description: |
  Intelligent task execution with auto-context and research. One catch-all command:
  First time explores and caches, returning uses cache for speed, auto-detects when
  to research and when to spec. Handles any scenario intelligently.

usage: |
  /shannon:do "task description"
  /shannon:do "task" --auto

examples:
  - /shannon:do "create authentication system"
  - /shannon:do "add Stripe billing integration"
  - /shannon:do "refactor user module for better performance"

delegates_to:
  - intelligent-do

version: "5.2.0"
---

# /shannon:do - Intelligent Task Execution

## Purpose

One-stop intelligent task execution command that handles everything automatically:
- ✅ New projects (auto spec + research + waves)
- ✅ Existing projects (explore + cache + execute)
- ✅ Research integration (auto-detect libraries)
- ✅ Context caching (fast return visits via Serena MCP)
- ✅ Validation gates (auto-detect or ask)

**Philosophy**: "Just do it intelligently" - minimal user input, maximum automation.

---

## Workflow

### Step 1: Invoke intelligent-do Skill

The command delegates all intelligence to the intelligent-do skill:

```
Invoke sub-skill:
@skill intelligent-do

Task: {user_provided_task_description}
```

The skill handles:
- Context detection (Serena MCP check)
- Project exploration (if first time)
- Research (if external libraries detected)
- Spec analysis (if complex task)
- Wave execution (with full context)
- Serena storage (for next time)

### Step 2: Report Results

After skill completes, display summary:

```markdown
✅ Task Complete

Context: {first-time|cached}
Research: {libraries_researched if any}
Spec: {complexity_score if analyzed}
Files Created: {count}
  - {file1}
  - {file2}
  ...

Validation Gates: {if configured}
  - Test: {test_command}
  - Build: {build_command}
  - Lint: {lint_command}

Time: {duration}
Saved to Serena: shannon_execution_{timestamp}
```

---

## Parameters

**--auto**: Autonomous mode (no user questions)
**--interactive**: Ask for confirmations (default)
**--no-research**: Skip research even if detected
**--force-spec**: Always run spec analysis

---

## Integration with Shannon CLI

Shannon CLI can invoke this command via Agent SDK:

```python
# Shannon CLI code
async for message in sdk_client.query(
    prompt="/shannon:do {task}",
    options=ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "{shannon_framework_path}"}],
        setting_sources=["user", "project"]
    )
):
    # Command executes intelligent-do skill
    # Returns results
```

Or invoke skill directly:

```python
async for message in sdk_client.invoke_skill(
    skill_name='intelligent-do',
    prompt_content=f"Task: {task}"
):
    # Same result
```

**CLI Value-Add**:
- Cost optimization (model selection)
- Analytics (session tracking)
- Dashboard streaming (WebSocket events)
- Local platform features

---

## Examples

### Simple Task

```bash
/shannon:do "create utils.py with string formatting helpers"

# Fast path:
# - Check Serena (< 1s)
# - Skip spec (simple task)
# - Execute wave
# - Save to Serena
# Time: 2-3 minutes
```

### Complex New Project

```bash
/shannon:do "create e-commerce platform with inventory, payments, user accounts, and admin dashboard"

# Full workflow:
# - No Serena context → First time
# - Empty directory → New project
# - Complex (4 requirements) → Run spec-analysis
# - "payments" detected → Research Stripe integration
# - Execute waves with spec + research
# - Save everything to Serena
# Time: 8-12 minutes
```

### Returning to Project

```bash
cd /projects/existing-app
/shannon:do "add password reset feature"

# Cached workflow:
# - Found in Serena → Load context
# - Fresh (2 hours old) → Use cache
# - No changes (file count same)
# - Display: "Using cached context"
# - Execute with cached gates and tech stack
# - Save execution
# Time: 2-3 minutes (vs 5 first time)
```

---

**Status**: Command definition complete, delegates to intelligent-do skill
