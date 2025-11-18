---
name: shannon:discover_skills
description: Discover and catalog all available skills on system
usage: /shannon:discover_skills [--cache|--refresh|--filter <pattern>]
---

# Skill Discovery Command

## Overview

Automatically discovers ALL skills across project, user, and plugin directories. Builds comprehensive catalog with metadata for intelligent skill selection and auto-invocation.

## Prerequisites

- No prerequisites (works standalone)
- Serena MCP recommended (for caching catalog)

## Options

- `--cache`: Use cached results if available (default, fast)
- `--refresh`: Force fresh discovery (ignore cache, scan all directories)
- `--filter <pattern>`: Filter results by skill name or description pattern

## Workflow

### Step 1: Determine Cache Strategy

```
IF --refresh flag present THEN
  force_refresh = true
  skip_cache = true
ELSE IF --cache flag present OR no flags THEN
  force_refresh = false
  check_cache = true
ELSE
  force_refresh = false
  check_cache = true
END IF
```

### Step 2: Check Cache (if applicable)

```
IF check_cache THEN
  # Try to load from Serena MCP
  cached_catalog = mcp__serena__read_memory("skill_catalog_current_session")

  IF cached_catalog exists AND age < 1 hour THEN
    RETURN cached_catalog
  END IF
END IF

# If no cache or expired, proceed to discovery
```

### Step 3: Execute Discovery

**Invoke skill-discovery skill**:

```markdown
@skill skill-discovery

Execute complete skill discovery protocol:
1. Scan project skills (./skills/*/SKILL.md)
2. Scan user skills (~/.claude/skills/*/SKILL.md)
3. Scan plugin skills (installed plugins)
4. Parse YAML frontmatter for each skill
5. Extract metadata (name, description, type, MCPs, triggers)
6. Build complete catalog
```

The skill-discovery skill will handle all scanning, parsing, and catalog building.

### Step 4: Apply Filter (if specified)

```
IF --filter <pattern> present THEN
  filtered_skills = {
    name: metadata
    for name, metadata in all_skills.items()
    if pattern.lower() in name.lower()
       OR pattern.lower() in metadata.description.lower()
  }

  DISPLAY: Filtered results
  COUNT: Show "X skills matching '{pattern}' (Y total)"
ELSE
  DISPLAY: All skills
END IF
```

### Step 5: Cache Results

```
IF Serena MCP available THEN
  mcp__serena__write_memory(
    "skill_catalog_current_session",
    content=json.dumps(skill_catalog)
  )

  DISPLAY: "✅ Cached to Serena MCP (expires in 1 hour)"
ELSE
  DISPLAY: "⚠️ Cache unavailable (Serena MCP not connected)"
END IF
```

### Step 6: Present Results

**Output Format**:

```markdown
═══════════════════════════════════════════════════════════
📚 SKILL DISCOVERY RESULTS
═══════════════════════════════════════════════════════════

**Skills Found**: {total_count}
├─ Project: {project_count} skills
├─ User: {user_count} skills
└─ Plugin: {plugin_count} skills

**By Type**:
├─ RIGID: {rigid_count}
├─ PROTOCOL: {protocol_count}
├─ QUANTITATIVE: {quant_count}
└─ FLEXIBLE: {flexible_count}

**Discovery Time**: {duration}ms
**Cache Status**: {cached|not_cached}

{if --filter present}
**Filter**: "{pattern}" ({filtered_count}/{total_count} matching)
{end if}

═══════════════════════════════════════════════════════════

{if verbose OR skill_count < 20}
**Skill Catalog**:

{for each namespace (project, user, plugin)}
### {Namespace} Skills ({count})

{for each skill in namespace}
- **{skill.name}** ({skill.skill_type})
  {skill.description}
  MCPs: {skill.mcp_requirements}
  {if skill.required_sub_skills}Sub-skills: {skill.required_sub_skills}{end}
{end}
{end}
{else}
Use /sh_skill_status to see invocation history
Use --filter to search skills
{end if}

═══════════════════════════════════════════════════════════
```

## Error Handling

### No Skills Found

```markdown
⚠️ No skills discovered

**Checked Locations**:
- ./skills/ (not found or empty)
- ~/.claude/skills/ (not found or empty)
- Installed plugins (none with skills)

**Suggestions**:
1. Create skills in ./skills/ directory
2. Install user skills to ~/.claude/skills/
3. Install Shannon plugin skills
4. Run /sh_help for skill creation guidance
```

### Cache Errors

```markdown
⚠️ Cache operation failed

**Error**: {error_message}

**Fallback**: Using in-memory catalog (will not persist across context loss)

**Recovery**: Check Serena MCP connection with /shannon:check_mcps
```

---

## Integration with Auto-Invocation

**This command is part of the auto-invocation system**:

1. **SessionStart hook**: Runs `/shannon:discover_skills --cache` automatically
2. **Skills discovered**: Made available for selection
3. **PreCommand hook**: Selects applicable skills before command execution
4. **Skills invoked**: Auto-loaded into agent context

**User sees**:
```
🎯 Auto-Invoked Skills (2 applicable):
   - spec-analysis (confidence: 0.85)
   - confidence-check (confidence: 0.72)
```

---

## Examples

### Basic Discovery

```bash
/shannon:discover_skills

→ Discovers all skills, uses cache if available
→ Displays count and summary
```

### Force Fresh Discovery

```bash
/shannon:discover_skills --refresh

→ Ignores cache, scans all directories
→ Useful after installing new skills
```

### Search for Specific Skills

```bash
/shannon:discover_skills --filter testing

→ Shows only skills matching "testing"
→ Example: functional-testing, testing-anti-patterns
```

### Discovery + Detailed List

```bash
/shannon:discover_skills --refresh --verbose

→ Fresh scan with complete skill catalog displayed
→ Shows all metadata for each skill
```

---

## Performance

**Cold Discovery** (first run, no cache):
- Scan directories: ~20ms
- Parse YAML: ~30ms (100 skills)
- Build catalog: ~10ms
- **Total**: ~60ms

**Warm Cache** (cached results):
- Retrieve from Serena: ~5ms
- **Total**: ~5ms

**Improvement**: 12x faster with cache

---

## The Bottom Line

**Skill discovery should happen automatically at session start, not manually when you remember.**

Same as import discovery in IDEs: tools find imports, you don't list them manually.

**This command makes Shannon the only framework with intelligent, automatic skill system.**

Use `--cache` for speed, `--refresh` after skill changes, `--filter` to search.
