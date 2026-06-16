# Shannon Framework v3 to v4 Migration Guide

**Version**: 4.0.0
**Migration Type**: Non-Breaking (Backward Compatible)
**Recommended Timeline**: Immediate (significant performance gains)

---

## Overview

Shannon v4 introduces **skill-based architecture** and **progressive disclosure**, achieving 90% token reduction while maintaining full backward compatibility with v3 projects.

### Key Changes
- Skill-based orchestration (vs prompt-based)
- Progressive disclosure (metadata-only loading)
- Enhanced hooks (4 new lifecycle hooks)
- Meta-programming (auto-generated skills)
- 3-tier MCP integration system

### Breaking Changes
❌ **None** - v4 is fully backward compatible with v3

### Deprecated
⚠️ Plugin name `shannon` → `shannon-v4` (v3 name still supported via alias)

---

## Migration Steps

### Step 1: Verify v3 Installation

```bash
# Check current Shannon version
/sh_status

# Expected output for v3:
# Shannon Framework v3.x.x active
```

### Step 2: Backup Serena Memories (Optional but Recommended)

```bash
# List all Serena memories
/sh_memory list

# Export critical memories (if Serena supports export)
# - spec_analysis_*
# - phase_plan_*
# - wave_*_complete
# - north_star_goal
```

### Step 3: Install Shannon v4

```bash
# Add marketplace (if local development)
/plugin marketplace add /path/to/shannon-framework

# Uninstall v3 (if installed as plugin)
/plugin uninstall shannon@shannon-framework

# Install v4
/plugin install shannon-v4@shannon-framework

# Restart Claude Code
```

### Step 4: Verify v4 Installation

```bash
# Check Shannon status
/sh_status

# Expected output:
# ✓ Shannon Framework v4.0.0 active
# Skills-Based Architecture
# Progressive Disclosure Enabled
# Skills Available: 5+ (depends on project)
```

### Step 5: Generate Project-Specific Skills (NEW in v4)

```bash
# If you have an existing spec_analysis in Serena:
/sh_spec --from-existing

# Or analyze your project fresh:
/sh_spec "Your project specification here"

# v4 will auto-generate skills based on your tech stack
```

### Step 6: Test Core Functionality

```bash
# Test specification analysis (should work identically)
/sh_spec "Build a simple React app"

# Test checkpoint (should work identically)
/sh_checkpoint "Testing v4 migration"

# Test wave execution (should work identically with better performance)
/sh_wave 1
```

---

## Compatibility Matrix

| Feature | v3 | v4 | Compatible? |
|---------|----|----|-------------|
| **Commands** | `/sh_spec`, `/sh_wave`, etc. | Same | ✅ 100% |
| **8D Analysis** | Full algorithm | Enhanced | ✅ 100% |
| **Wave Orchestration** | Parallel execution | Same + hooks | ✅ 100% |
| **PreCompact Hook** | Zero-context-loss | Enhanced | ✅ 100% |
| **Serena Memories** | All keys | Same keys | ✅ 100% |
| **MCP Integration** | Flat recommendations | 3-tier system | ✅ Backward compatible |
| **Agent Invocation** | Task tool | Same | ✅ 100% |

---

## What's New in v4

### 1. Progressive Disclosure (90% Token Reduction)

**v3 Behavior**:
```
Session start → Load all 300K tokens upfront
```

**v4 Behavior**:
```
Session start → Load 30K tokens (metadata only)
On-demand → Load full content when needed
```

**Impact**: 10× faster session initialization, more context budget available

### 2. Skills System

**v3 Behavior**:
```
Commands execute via prose instructions embedded in command files
```

**v4 Behavior**:
```
Commands → Activate skills → Skills provide specialized guidance
Example: /sh_spec → shannon-spec-analyzer skill
```

**New Commands**:
```bash
/sh_generate_skills  # Manually trigger skill generation
/sh_list_skills      # List available skills
/sh_skill_status     # Show skill activation status
```

### 3. Meta-Programming (Auto-Generated Skills)

**NEW**: `shannon-skill-generator` analyzes your spec and creates project-specific skills:

```yaml
Example:
  Spec: "React + Express + PostgreSQL app"
  Generated Skills:
    - shannon-react-ui (Frontend 60%)
    - shannon-express-api (Backend 30%)
    - shannon-postgres-prisma (Database 10%)
```

**Benefits**:
- Framework-version-specific guidance (e.g., Next.js 14 App Router, not Pages Router)
- Tailored to your exact tech stack
- Auto-updates when spec changes

### 4. Enhanced Hooks (4 New)

**v3 Hooks**:
- SessionStart
- UserPromptSubmit
- PreCompact (zero-context-loss)
- PostToolUse (NO MOCKS enforcement)
- Stop (validation gates)

**v4 New Hooks**:
- **PreWave**: Validates dependencies before wave execution
- **PostWave**: Collects results after wave completion
- **QualityGate**: Enforces 5-gate validation system
- **PreToolUse**: Skill activation and MCP availability checks

**Impact**: Automated validation, reduced manual overhead

### 5. MCP Integration Tiers

**v3 Behavior**:
```
Flat MCP recommendations (6-15 MCPs suggested)
```

**v4 Behavior**:
```
Tier 1 (Mandatory): Serena - Always required
Tier 2 (Recommended): Sequential, Context7, Puppeteer (domain ≥20%)
Tier 3 (Project-Specific): shadcn-ui (React), Xcode (iOS)
```

**Impact**: Clear priority guidance, better MCP selection

---

## Project Migration

### Existing v3 Projects

**Good News**: No changes required! v4 reads the same Serena memories.

**Steps**:
1. Open existing project in Claude Code
2. Install Shannon v4 plugin
3. Restart Claude Code
4. v4 automatically loads existing memories
5. Optionally: Run `/sh_spec --from-existing` to generate skills

**Example**:
```bash
# Your v3 project with Serena memories:
# - spec_analysis_2024_11_01
# - phase_plan_detailed
# - wave_1_complete

# After v4 migration:
# 1. All memories preserved ✅
# 2. Skills auto-generated based on spec_analysis ✅
# 3. Commands work identically ✅
# 4. 90% faster session initialization ✅
```

### New v4 Projects

**Recommended Workflow**:
```bash
# 1. Start with specification
/sh_spec "Build [your project description]"

# 2. Shannon v4 automatically:
#    - Analyzes 8D complexity
#    - Detects domains
#    - Recommends MCPs
#    - Generates project-specific skills
#    - Creates 5-phase plan

# 3. Execute waves (same as v3)
/sh_wave 1

# 4. Checkpoint progress (same as v3)
/sh_checkpoint "Completed authentication"
```

---

## Performance Improvements

### Token Efficiency

| Metric | v3 | v4 | Improvement |
|--------|----|----|-------------|
| **Session Load** | ~300K tokens | ~30K tokens | **10× faster** |
| **Commands** | ~172K tokens | ~14K tokens | **91.7% reduction** |
| **Agents** | ~126K tokens | ~10K tokens | **92.3% reduction** |
| **Overall** | Full upfront | Metadata only | **90% reduction** |

### Wave Execution

| Metric | v3 | v4 | Improvement |
|--------|----|----|-------------|
| **Parallelism** | TRUE (ONE message) | TRUE (preserved) | Same ✅ |
| **Context Loading** | Manual protocol | Auto-injected | **Automated** |
| **Validation** | Manual gates | Auto-validated | **Automated** |
| **Speedup** | 2-4× | 2-4× | Same ✅ |

---

## Troubleshooting

### Issue: "Shannon v4 not found"

**Solution**:
```bash
# Verify marketplace added
/plugin marketplace list

# Add if missing
/plugin marketplace add /path/to/shannon-framework

# Reinstall
/plugin install shannon-v4@shannon-framework
```

### Issue: "Skills not generating"

**Solution**:
```bash
# Verify Serena MCP connected
/sh_check_mcps

# Manually trigger skill generation
/sh_generate_skills --from-spec spec_analysis_[timestamp]

# Check Serena for spec_analysis
/sh_memory list
```

### Issue: "PreCompact hook not firing"

**Solution**:
```bash
# Verify hooks.json loaded
ls ~/.claude/plugins/shannon-v4/hooks/hooks.json

# Check hook permissions
chmod +x ~/.claude/plugins/shannon-v4/hooks/*.py

# Restart Claude Code
```

### Issue: "Commands work differently in v4"

**Answer**: This should not happen! v4 is 100% backward compatible. If you find a command behaving differently, please file an issue.

---

## Rollback to v3

If you need to rollback:

```bash
# Uninstall v4
/plugin uninstall shannon-v4@shannon-framework

# Reinstall v3
/plugin install shannon@shannon-framework

# Restart Claude Code

# Your Serena memories are preserved ✅
```

---

## FAQs

### Q: Will my v3 Serena memories work in v4?
**A**: Yes! 100% compatible. Same keys, same structure.

### Q: Do I need to reinstall MCPs for v4?
**A**: No. v4 uses the same MCPs as v3 (Serena, Sequential, Context7, Puppeteer, etc.)

### Q: Can I use v3 and v4 side-by-side?
**A**: Not recommended. Choose one version. v4 is superior in all aspects while maintaining compatibility.

### Q: Will v4 auto-update my existing specs?
**A**: No. v4 reads existing specs but doesn't modify them. Use `/sh_spec --from-existing` to generate skills.

### Q: What happens to my v3 commands like /sh_spec?
**A**: They work identically in v4 (same input, same output) but with 90% better token efficiency.

### Q: Are v3 agents available in v4?
**A**: Yes! All 19 agents converted to v4 lightweight format. Same capabilities, 92% fewer tokens.

### Q: Does v4 support the NO MOCKS philosophy?
**A**: Yes! Enhanced with `shannon-browser-test` skill and `PostToolUse` hook enforcement.

### Q: How do I know which skills are active?
**A**: Use `/sh_skill_status` or check the session initialization message.

---

## Next Steps After Migration

### 1. Generate Skills for Existing Projects
```bash
/sh_spec --from-existing
```

### 2. Optimize Your Workflow
- Let v4 auto-generate skills instead of manual configuration
- Use new hooks for automated validation
- Leverage 3-tier MCP recommendations

### 3. Explore New Features
- Try meta-programming with `shannon-skill-generator`
- Use `PreWave`/`PostWave` hooks for better wave orchestration
- Test `QualityGate` for automated validation

### 4. Provide Feedback
- Report any compatibility issues
- Suggest Priority 2/3 skills for your domain
- Share performance improvements you observe

---

## Support

**Documentation**:
- [Shannon v4 README](../shannon-v4-plugin/README.md)
- [Skills Catalog](../shannon-v4-plugin/skills/)
- [Command Reference](../shannon-v4-plugin/commands/)

**Issues**:
- GitHub: https://github.com/krzemienski/shannon-framework/issues

---

## Summary

✅ **Migration is simple**: Install v4, restart, continue working
✅ **Backward compatible**: All v3 projects work in v4
✅ **Performance gains**: 90% token reduction, 10× faster initialization
✅ **New capabilities**: Skills, meta-programming, enhanced hooks
✅ **Zero risk**: Easy rollback if needed

**Recommendation**: Migrate to v4 immediately for significant performance improvements with zero downtime.

---

**Shannon v4** - Faster, Smarter, Skill-Based 🚀
