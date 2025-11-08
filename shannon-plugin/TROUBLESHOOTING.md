# Shannon Framework V4.1 - Troubleshooting Guide

**Version**: 4.1.0
**Last Updated**: 2025-11-08

---

## Common Issues

### Installation Issues

#### Problem: "Plugin not found in marketplace"

**Symptoms**:
```
Error: Plugin 'shannon@shannon-framework' not found
```

**Diagnosis**:
- Marketplace not added or incorrect path
- Plugin name mismatch

**Solution**:
```bash
# For published plugin:
/plugin marketplace add shannon-framework/shannon

# For local development:
/plugin marketplace add /absolute/path/to/shannon-framework

# Verify marketplace:
/plugin marketplace list
```

---

#### Problem: "Serena MCP required but not connected"

**Symptoms**:
```
⚠️  Serena MCP not available
Shannon requires Serena MCP for context preservation
```

**Diagnosis**:
- Serena MCP not installed or configured
- MCP server not running

**Solution**:
```bash
# 1. Check MCP status
/sh_check_mcps

# 2. Install Serena MCP (follow Serena documentation)

# 3. Add to Claude Code MCP configuration:
# - Open Claude Code settings
# - Add Serena to MCP servers list
# - Restart Claude Code

# 4. Verify connection
/sh_check_mcps
```

---

#### Problem: "Commands not available after install"

**Symptoms**:
- `/sh_spec` command not recognized
- `/shannon:prime` command not found

**Diagnosis**:
- Plugin not loaded (needs Claude Code restart)
- Installation incomplete

**Solution**:
```bash
# 1. Verify plugin installed:
/plugin list

# 2. If installed, restart Claude Code completely

# 3. If not installed:
/plugin install shannon@shannon

# 4. After restart, verify:
/sh_status
```

---

### Command Issues

#### Problem: "/sh_spec gives incomplete analysis"

**Symptoms**:
- Missing 8D breakdown
- No domain detection
- No MCP recommendations

**Diagnosis**:
- Specification too short (<20 words)
- spec-analysis skill not loaded

**Solution**:
```bash
# Provide detailed specification (minimum 50-100 words)
/sh_spec "Build a web application with React frontend, Node.js backend, PostgreSQL database, JWT authentication, role-based access control, RESTful API, and user dashboard"

# Verify skill loaded:
/sh_discover_skills --filter spec
```

---

#### Problem: "/shannon:prime fails or takes too long"

**Symptoms**:
```
Error: Checkpoint not found
Error: Memories could not be loaded
Priming takes >5 minutes
```

**Diagnosis**:
- Serena MCP not connected (checkpoints unavailable)
- Old/corrupted checkpoints
- Too many memories

**Solution**:
```bash
# Use fresh mode (skip checkpoint restoration):
/shannon:prime --fresh

# If resume mode needed:
# 1. Check available checkpoints:
/sh_memory --list

# 2. Restore specific checkpoint manually:
/sh_restore checkpoint-name

# 3. Then prime:
/shannon:prime --quick
```

---

#### Problem: "/sh_discover_skills finds no skills"

**Symptoms**:
```
📚 Skills Found: 0
```

**Diagnosis**:
- Skills directory empty (fresh install)
- Scanning wrong directories

**Solution**:
```bash
# Force refresh (ignore cache):
/sh_discover_skills --refresh

# Verify skill directories exist:
ls shannon-plugin/skills/  # Should show 16 skills

# Check user skills:
ls ~/.claude/skills/  # Shows your personal skills
```

---

### Skill Issues

#### Problem: "Skill not auto-invoked when expected"

**Symptoms**:
- spec-analysis skill not loaded for /sh_spec
- functional-testing skill not loaded for testing

**Diagnosis**:
- Skill discovery cache outdated
- Confidence threshold not met (<0.70)
- Skill metadata incorrect

**Solution**:
```bash
# 1. Refresh skill discovery:
/sh_discover_skills --refresh

# 2. Check skill status:
/sh_skill_status  # Shows invocation history

# 3. Manually invoke skill if needed:
Skill("spec-analysis")
```

---

#### Problem: "Forced reading protocol not enforcing"

**Symptoms**:
- Agents skip pre-counting
- Partial reading allowed
- No completeness verification

**Diagnosis**:
- FORCED_READING_PROTOCOL not loaded into context
- Not triggered for file type
- Command not enhanced with protocol

**Solution**:
```bash
# 1. Verify protocol exists:
cat shannon-plugin/core/FORCED_READING_PROTOCOL.md

# 2. For manual enforcement:
# - Count lines first: wc -l file.md
# - Read complete file: Read(file, offset=0)
# - Verify: lines_read == total_lines

# 3. Use enforcing commands:
/sh_spec  # Auto-enforces for specifications
/sh_analyze  # Auto-enforces for analysis targets
/sh_wave  # Auto-enforces for wave plans
```

---

### MCP Issues

#### Problem: "Optional MCPs missing - is Shannon broken?"

**Symptoms**:
```
⚠️  Context7 MCP - Not connected
⚠️  Puppeteer MCP - Not connected
```

**Diagnosis**:
- This is NOT an error
- Optional MCPs enhance but aren't required

**Solution**:
- **Shannon works fine without optional MCPs**
- For enhanced functionality, install optional MCPs:
  - Context7: Framework patterns (nice to have)
  - Sequential: Deep reasoning (recommended for complex specs)
  - Puppeteer: Browser testing (recommended for web projects)

```bash
# Check what's required vs optional:
/sh_check_mcps

# Shannon only REQUIRES Serena MCP
```

---

### Context Issues

#### Problem: "Context lost after long session"

**Symptoms**:
- Specification details forgotten
- Wave progress lost
- North Star goal disappeared

**Diagnosis**:
- Context compaction occurred (automatic after ~1M tokens)
- Checkpoint not created before compaction

**Solution**:
```bash
# Shannon has automatic checkpointing via PreCompact hook
# But you can manually checkpoint anytime:
/sh_checkpoint "milestone-name"

# After context loss, restore:
/sh_restore "milestone-name"

# Or use shannon:prime to restore latest:
/shannon:prime --resume
```

---

#### Problem: "Wave execution lost state mid-wave"

**Symptoms**:
- Wave started but didn't complete
- Task progress lost
- Agent state missing

**Diagnosis**:
- Context compaction during wave
- Checkpoint between waves (not mid-wave)

**Solution**:
```bash
# Check last checkpoint:
/sh_memory --list

# Restore to pre-wave checkpoint:
/sh_restore checkpoint-name

# Resume wave execution:
/sh_wave N --resume
```

---

### Performance Issues

#### Problem: "/sh_spec takes >5 minutes"

**Symptoms**:
- Specification analysis very slow
- High token usage
- Timeout errors

**Diagnosis**:
- Specification too large (>10,000 words)
- Too many domains (10+ domains)
- Sequential MCP not available

**Solution**:
```bash
# 1. Break specification into sections:
/sh_spec "Section 1: Frontend requirements..."
/sh_spec "Section 2: Backend requirements..."

# 2. Check Sequential MCP:
/sh_check_mcps

# 3. Use quick analysis:
/sh_spec "..." --quick  # Skip deep domain analysis
```

---

#### Problem: "Skill discovery slow (>1 minute)"

**Symptoms**:
- /sh_discover_skills takes long time
- Scanning many directories

**Diagnosis**:
- Large user skills directory (>100 skills)
- First run (cold cache)

**Solution**:
```bash
# Use cache (default, 1 hour TTL):
/sh_discover_skills --cache

# Cache makes subsequent calls <10ms

# If cache corrupted:
/sh_discover_skills --refresh  # Rebuild cache
```

---

## Validation Issues

#### Problem: "Validation scenarios not executing"

**Symptoms**:
- testing-skills-with-subagents mentioned but not working

**Diagnosis**:
- Validation scenarios require manual execution
- Not automatic with Shannon installation

**Solution**:
Validation scenarios are documented in SHANNON_V4.1_VALIDATION_PLAN.md but not auto-executed. These are for Shannon development/certification, not user workflows.

**Users don't need to run validation scenarios** - they're for Shannon framework development.

---

## Plugin Integration Issues

#### Problem: "New commands/skills not appearing after update"

**Symptoms**:
- Updated Shannon but /shannon:prime not available
- skill-discovery skill not found

**Diagnosis**:
- Plugin not reinstalled after update
- Old version cached

**Solution**:
```bash
# Full plugin refresh:
/plugin uninstall shannon@shannon
/plugin marketplace remove shannon
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon@shannon

# Restart Claude Code

# Verify version:
/sh_status  # Should show v4.1.0
```

---

## Getting Help

### Check Shannon Status
```bash
/sh_status  # Shows Shannon health, version, loaded components
```

### Check MCP Status
```bash
/sh_check_mcps  # Shows all MCP connections, required vs optional
```

### Check Skill Inventory
```bash
/sh_discover_skills  # Shows all available skills
/sh_skill_status     # Shows skill invocation history (when implemented)
```

### Enable Debug Mode
```bash
# Serena MCP debug (if available):
mcp__serena__get_current_config()

# Shows Serena configuration and connection details
```

---

## Known Limitations

### Current Version (V4.1.0)

**Implemented**:
- ✅ Core behavioral patterns (.md files)
- ✅ Skills and commands (.md files)
- ✅ Plugin manifest (plugin.json)
- ✅ Documentation

**Not Yet Implemented** (future):
- ⚠️ PreRead hook (forced reading enforcement at Read tool level)
- ⚠️ PreCommand hook (auto-skill invocation before commands)
- ⚠️ Agent prompt enhancements (FORCED_READING_PROTOCOL references)
- ⚠️ Validation execution (pressure scenarios with subagents)

**Current Behavior**:
- Commands and skills provide INSTRUCTIONS for forced reading and skill discovery
- Agents follow instructions when loaded
- Automatic enforcement hooks planned for future release

---

## FAQ

**Q: Does Shannon work without Serena MCP?**
A: No. Serena is mandatory for Shannon's context preservation and checkpointing.

**Q: Can I use Shannon with other frameworks?**
A: Shannon enhances SuperClaude commands (sc_*). Fully compatible.

**Q: What's the difference between sh_* and sc_* commands?**
A: sh_* = Shannon-native commands, sc_* = SuperClaude commands enhanced by Shannon

**Q: How do I know which skills are active?**
A: Use `/sh_discover_skills` to see all skills. Skills auto-load contextually based on task.

**Q: Is forced reading automatic?**
A: Currently, commands like /sh_spec, /sh_analyze, /sh_wave INSTRUCT agents to use forced reading protocol. Future versions will have automatic enforcement hooks.

**Q: How long does /shannon:prime take?**
A: Fresh mode: 10-20s, Resume mode: 30-60s, Full mode: 60-120s

**Q: Can I disable forced reading for quick lookups?**
A: Yes (when hooks implemented): `/sh_read_normal <file>` overrides enforcement

---

## Contact & Support

- **Issues**: https://github.com/shannon-framework/shannon/issues
- **Discussions**: https://github.com/shannon-framework/shannon/discussions
- **Email**: info@shannon-framework.dev
- **Documentation**: shannon-plugin/README.md

---

**Shannon Framework V4.1.0** - Troubleshooting Guide
