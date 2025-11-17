# Next Session: Build Shannon Framework intelligent-do Skill CORRECTLY

**Current Session**: 2025-11-17, 430K tokens (43%), ~8 hours
**Status**: Shannon CLI alpha ready, Framework skill needs proper building approach

---

## Critical Mistakes This Session

### Mistake 1: Built Without Understanding
- Tried to write intelligent-do skill without invoking teaching skills
- Copied patterns from other skills without full comprehension
- Used wrong Serena MCP tools (mcp__memory__* vs mcp__serena__*)

### Mistake 2: Wrong Serena MCP Tools
- **WRONG**: mcp__memory__create_entities, search_nodes (generic memory MCP)
- **CORRECT**: mcp__serena__write_memory, read_memory, list_memories (Serena MCP)
- Shannon uses simple memory storage, not knowledge graph

### Mistake 3: Didn't Invoke Teaching Skills
- **Should Have**: Invoked skill-writing guidance skill
- **Should Have**: Invoked testing-with-subagents skill
- **Did Instead**: Made up my own patterns

---

## What Actually Needs To Happen

### STEP 1: Understand Serena MCP Correctly

**Tools Available**:
```
mcp__serena__write_memory(key, content)
mcp__serena__read_memory(key)
mcp__serena__list_memories()
```

**NOT** knowledge graph (create_entities, search_nodes, add_observations).

**Example from spec-analysis**:
```javascript
mcp__serena__write_memory(analysis_id, JSON.stringify(analysis))
const verify = mcp__serena__read_memory(analysis_id)
```

**Memory Keys for Shannon**:
- "shannon_project_{project_id}" - Project context
- "shannon_execution_{timestamp}" - Execution results
- "spec_analysis_{id}" - Spec results
- "wave_{id}_results" - Wave results

Simple key-value storage, not graph.

---

### STEP 2: Find and Invoke Teaching Skills

**Check if these exist**:
```bash
cd /Users/nick/Desktop/shannon-framework
ls skills/ | grep -i "skill.*writ\|creat.*skill"
```

**If skill-writing guidance exists**:
- Invoke it to learn correct skill structure
- Follow its instructions exactly
- Don't make up patterns

**Check for testing guidance**:
```bash
ls skills/functional-testing/
# Look for sub-agent testing patterns
```

---

### STEP 3: Study Existing Skills COMPLETELY

**Read ENTIRE skills** (don't skim):
1. **skills/spec-analysis/SKILL.md** (complete) - How to use Serena correctly
2. **skills/wave-orchestration/SKILL.md** (complete) - How to invoke other skills
3. **skills/exec/SKILL.md** (complete) - Complex skill with multiple sub-skills
4. **skills/memory-coordination/SKILL.md** (complete) - Serena patterns

**Extract**:
- Exact Serena tool usage patterns
- How skills are written (plain language instructions)
- How skills invoke other skills (@skill name)
- How to structure workflows
- Anti-rationalization sections
- Testing approach

---

### STEP 4: Build intelligent-do Skill Correctly

**Structure**:
```yaml
---
name: intelligent-do
description: |
  (Clear when-to-use description)
skill-type: PROTOCOL
shannon-version: ">=5.2.0"
mcp-requirements:
  required:
    - name: serena
      purpose: Context backend
required-sub-skills:
  - wave-orchestration
  - memory-coordination
allowed-tools: [Read, Write, Bash, Serena, SlashCommand, TodoWrite]
---

# Intelligent Do

## Purpose
(Clear purpose statement)

## When to Use
(Specific scenarios)

## Anti-Rationalization
(Common mistakes and counters)

## Workflow

### Step 1: Context Detection
1. Check Serena for project memory
   ```
   Use Serena tool:
   const memories = mcp__serena__list_memories()
   const projectKey = `shannon_project_${projectId}`
   const exists = memories.includes(projectKey)
   ```

2. If found → RETURNING
3. If not found → FIRST_TIME

(Continue with clear step-by-step plain language instructions)
```

**Pattern**: Plain language instructions telling Claude what to do, not executable code.

---

### STEP 5: Create /shannon:do Command

**File**: shannon-framework/commands/do.md

**Structure**:
```yaml
---
name: do
description: Intelligent task execution
usage: /shannon:do "task"
delegates_to: intelligent-do
---

# /shannon:do Command

Invokes intelligent-do skill for context-aware task execution.

## Workflow

### Step 1: Invoke Skill
```
@skill intelligent-do
Task: {user_task}
```

(Rest of command definition)
```

---

### STEP 6: Test with functional-testing Patterns

**Use sub-agents properly**:
- Study how functional-testing uses Task tool
- Spawn test agents following Shannon patterns
- Validate with real systems (no mocks)

---

## What's Done in Shannon CLI

**Commits**: 24 total
- ✅ Technical debt cleanup (15 V4 files archived)
- ✅ Bugs fixed (3 critical)
- ✅ Intelligent workflows implemented (10 methods)
- ✅ Basic validation passing (2/4 gates)
- ✅ Architecture documented
- ✅ API key removed from working copy

**Working Now**:
- shannon do command creates files
- First-time workflow auto-onboards
- Returning workflow uses cache
- wave-orchestration skill integration

**Limitations**:
- Complex tasks create stubs only
- No research integration
- No Serena MCP backend (uses local JSON)
- No spec-analysis in workflow

---

## What Needs To Happen

### Shannon Framework Work (Fresh Session):

**Phase 1: Learn Correctly** (1-2 hours)
1. Understand Serena MCP completely (write_memory, read_memory, list_memories)
2. Study 3-4 complete skills (spec-analysis, wave-orchestration, exec, memory-coordination)
3. Invoke any teaching skills that exist
4. Extract exact patterns

**Phase 2: Build Skill** (2-3 hours)
1. Create intelligent-do/SKILL.md following patterns EXACTLY
2. Use mcp__serena__* tools (not mcp__memory__*)
3. Write plain language instructions (not code)
4. Include anti-rationalization sections
5. Structure with proper frontmatter

**Phase 3: Create Command** (30 min)
1. Create commands/do.md
2. Delegates to intelligent-do skill
3. Follow command patterns

**Phase 4: Test** (2-3 hours)
1. Use functional-testing patterns
2. Spawn sub-agents correctly
3. Validate with real execution
4. Collect evidence

**Phase 5: Integrate with CLI** (1 hour)
1. Update Shannon CLI to invoke intelligent-do
2. Test end-to-end
3. Validate complete workflow

**Total**: 7-10 hours with proper approach

---

## Git History Issue

**Security**: API key exposed in commit be86099
- Working copy: FIXED (commit 358c23d)
- Git history: Still contains secret
- Recommendation: Rotate key, use git filter-repo to clean history
- Document: SECURITY_ISSUE_API_KEY.md

---

## Session Metrics

**Duration**: ~8 hours
**Tokens**: 430K / 1M (43% used, 57% remaining)
**Commits**: 24
**Files Created**: 17 documents
**Status**: CLI alpha ready, Framework needs fresh approach

---

## Next Session Quick Start

```bash
# Activate Shannon Framework
cd /Users/nick/Desktop/shannon-framework
mcp__serena__activate_project("shannon-framework")

# Read this handoff
Read("NEXT_SESSION_BUILD_FRAMEWORK_SKILL_CORRECTLY.md")

# Study complete skills
Read("skills/spec-analysis/SKILL.md") # ALL of it
Read("skills/wave-orchestration/SKILL.md") # ALL of it
Read("skills/exec/SKILL.md") # ALL of it
Read("skills/memory-coordination/SKILL.md") # ALL of it

# Understand Serena correctly
# Tools: mcp__serena__write_memory, read_memory, list_memories
# NOT: mcp__memory__create_entities, search_nodes

# THEN build intelligent-do skill correctly
# Following exact patterns from studied skills
# Using correct Serena tools
# Plain language instructions
# Proper testing with sub-agents

# THEN integrate with Shannon CLI
# THEN validate everything
```

---

## What Not To Do

**DON'T**:
- ❌ Rush to build without reading complete skills
- ❌ Use mcp__memory__* tools (use mcp__serena__*)
- ❌ Write executable code in skills (write instructions)
- ❌ Copy patterns without understanding
- ❌ Skip teaching skills that exist
- ❌ Build without testing approach planned

**DO**:
- ✅ Read complete skills thoroughly
- ✅ Use mcp__serena__* tools only
- ✅ Write plain language instructions
- ✅ Invoke teaching skills if they exist
- ✅ Plan testing before building
- ✅ Validate as you build

---

**Session End**: Proper foundation for Framework skill in next session with fresh focus and correct understanding
