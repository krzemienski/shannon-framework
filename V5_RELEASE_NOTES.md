# Shannon Framework V5.0.0 - Release Notes

**Release Date**: November 18, 2025
**Status**: ✅ RELEASED
**Breaking Changes**: YES (Command Namespacing)

---

## 🎯 Executive Summary

Shannon Framework V5.0.0 represents a major evolution in command orchestration, debugging capabilities, and project-specific customization. This release introduces command namespacing for better plugin isolation, a powerful deep debugging command, and auto-generated project-specific instructions that persist across sessions.

---

## 🚨 BREAKING CHANGES

### Command Namespacing

**All commands now require the `shannon:` prefix.**

| Old (V4) | New (V5) |
|----------|----------|
| `/do` | `/shannon:do` |
| `/exec` | `/shannon:exec` |
| `/wave` | `/shannon:wave` |
| `/spec` | `/shannon:spec` |
| `/prime` | `/shannon:prime` |
| `/task` | `/shannon:task` |
| `/analyze` | `/shannon:analyze` |
| `/north_star` | `/shannon:north_star` |
| `/reflect` | `/shannon:reflect` |
| `/checkpoint` | `/shannon:checkpoint` |
| `/restore` | `/shannon:restore` |
| `/discover_skills` | `/shannon:discover_skills` |
| `/check_mcps` | `/shannon:check_mcps` |
| `/memory` | `/shannon:memory` |
| `/scaffold` | `/shannon:scaffold` |
| `/test` | `/shannon:test` |
| `/status` | `/shannon:status` |

**Why this change?**
- Prevents conflicts with other plugins
- Clear namespace ownership
- Industry best practice
- Better plugin isolation

**Migration**: Simply add `shannon:` prefix to all command invocations.

---

## ✨ What's New

### 1. UltraThink Command (Deep Debugging)

```bash
/shannon:ultrathink "Race condition in payment processing" --thoughts 200 --verify
```

**Capabilities**:
- **150+ Sequential Thoughts**: Minimum 150 thoughts (configurable up to 500+)
- **Systematic Debugging Protocol**: Structured approach to finding root causes
- **Forced Complete Reading**: EVERY file read completely before analysis (no shortcuts)
- **Root Cause Tracing**: symptom → immediate cause → deeper cause → ROOT CAUSE
- **Auto-Verification**: `--verify` flag automatically tests the solution

**When to Use**:
- Standard debugging hasn't found the root cause
- Intermittent or hard-to-reproduce bugs
- Complex multi-component issues
- Critical production bugs
- When you need certainty, not speed

**MCP Requirement**: Sequential Thinking MCP (MANDATORY)

**See**: `commands/ultrathink.md` for complete documentation

---

### 2. Project-Specific Custom Instructions

**Problem Solved**: Agents forget project conventions across sessions

**Solution**: Auto-generated instructions that persist and reload at every session

```bash
cd /your/project
/shannon:generate_instructions
```

**What It Detects**:
- CLI argument defaults ("always use `--project-dir . --verbose`")
- Build commands (`npm run build`, `pytest`, etc.)
- Test conventions (framework, patterns, NO MOCKS enforcement)
- Code conventions (style guide, linter, formatter)
- Project-specific rules (from .editorconfig, CONTRIBUTING.md)

**Example Generated Instruction**:
```markdown
## CLI Argument Defaults
**IMPORTANT**: ALWAYS use these arguments unless explicitly overridden:
```bash
shannon-cli --project-dir . --verbose <command>
```
```

**Storage**: `.shannon/custom_instructions.md`

**Auto-Loading**: Loads at every `/shannon:prime` and session start

**Staleness Detection**: Auto-regenerates when project changes significantly

**See**: `core/PROJECT_CUSTOM_INSTRUCTIONS.md` for specification

---

### 3. Command Orchestration Guide

**New Document**: `docs/COMMAND_ORCHESTRATION.md` (900+ lines)

**Answers the question**: "Which Shannon command should I use?"

**Contains**:
- **Command Hierarchy**: Meta → Core → Analysis → Support
- **Decision Trees**: Step-by-step "which command" flowcharts
- **Command → Skill Maps**: See what each command invokes
- **Skill → Command Maps**: See which commands invoke each skill
- **MCP Requirements**: By command
- **Common Workflows**: 5 complete examples
- **Iron Laws**: Shannon's non-negotiable principles
- **Troubleshooting**: Common questions answered

**Quick Decision Tree**:
```
Starting session? → /shannon:prime
Have specification? → /shannon:spec
Want to execute? → /shannon:do (intelligent) OR /shannon:exec (structured)
Complexity >= 0.50? → /shannon:wave
Deep debugging? → /shannon:ultrathink
Validate work? → /shannon:reflect
```

**See**: `docs/COMMAND_ORCHESTRATION.md`

---

## 🔧 Critical Bug Fixes

### Hardcoded Path Issues (CRITICAL)

**Problem**: Plugin was not portable due to hardcoded paths

**Fixed Files**:
1. `hooks/session_start.sh`: `/Users/nick/.claude/skills/...` → `${PLUGIN_DIR}/skills/...`
2. `hooks/hooks.json`: 2 hardcoded paths → `${CLAUDE_PLUGIN_ROOT}`

**Impact**: Plugin now works on ANY installation, not just the original developer's machine

---

## 📚 Documentation Improvements

### New Documents (5 files, ~3,500 lines)

1. **docs/COMMAND_ORCHESTRATION.md** (900+ lines)
   - Complete command usage guide
   - Decision trees and workflows

2. **commands/ultrathink.md** (500+ lines)
   - UltraThink command specification
   - Usage examples and anti-patterns

3. **core/PROJECT_CUSTOM_INSTRUCTIONS.md** (450+ lines)
   - Custom instructions system specification
   - Generation algorithm
   - Loading and staleness detection

4. **docs/V5_IMPLEMENTATION_SUMMARY.md** (900+ lines)
   - Complete implementation status
   - User decision points
   - Timeline and effort estimates

5. **scripts/README.md**
   - Scripts directory documentation
   - Implementation TODO list

### Updated Documents

1. **skills/using-shannon/SKILL.md**
   - Added ALL 19 commands (was missing 11)
   - Command decision tree
   - Complete command reference

2. **skills/intelligent-do/SKILL.md**
   - Added orchestration clarity
   - Explains when to use `/shannon:do` vs alternatives
   - Cross-references to orchestration guide

3. **CHANGELOG.md**
   - V5.0.0 section with breaking changes
   - Migration guide
   - Complete feature list

### Removed Documents (7 obsolete files)

- `AGENT3_SITREP_FINAL.md`
- `AGENT3_VALIDATION_REPORT.md`
- `AGENT6_MISSION_COMPLETE.md`
- `AGENT6_SITREP_COMPLETE.md`
- `COMPLETE_AUDIT_AND_CLEANUP_PLAN.md`
- `COMPLETE_AUDIT_REPORT.md`
- `COMPLETE_FILE_INVENTORY.md`

**Reason**: Superseded by V5 documentation, no longer relevant

---

## 📦 MCP Requirements

### New MANDATORY Requirements

- **Sequential Thinking MCP**: REQUIRED for `/shannon:ultrathink`

### New RECOMMENDED Requirements

- **Sequential Thinking MCP**: RECOMMENDED for complex analysis (complexity >= 0.70)
- **Context7 MCP**: RECOMMENDED for library research
- **Tavily MCP**: RECOMMENDED for best practices research
- **Puppeteer MCP**: RECOMMENDED for functional UI testing

### Existing Requirements (Unchanged)

- **Serena MCP**: MANDATORY for all Shannon functionality (context preservation)

**Check MCP Status**: `/shannon:check_mcps`

---

## 🔢 Statistics

### Commands

- **Total**: 19 commands (was 17)
- **New**: `ultrathink`, `generate_instructions`
- **Updated**: All 17 existing commands renamed with `shannon:` prefix

### Skills

- **Total**: 20 skills (unchanged count)
- **Updated**: `using-shannon`, `intelligent-do` with enhanced documentation

### Documentation

- **Lines Added**: ~3,500 lines of new documentation
- **Files Created**: 5 new documentation files
- **Files Modified**: ~20 files updated
- **Files Removed**: 7 obsolete documents cleaned up

### Code Changes

- **Command Files**: 18 files updated (namespacing)
- **Hook Files**: 2 files updated (portability fixes)
- **Version**: plugin.json updated to 5.0.0

---

## 🔄 Migration Guide

### Step 1: Update Command Syntax

Find and replace in your documentation/workflows:

```bash
# Python/JavaScript example
sed -i 's|/do |/shannon:do |g' **/*.md
sed -i 's|/wave |/shannon:wave |g' **/*.md
sed -i 's|/spec |/shannon:spec |g' **/*.md
# etc. for all commands
```

### Step 2: Install/Update Plugin

```bash
# If not installed
claude plugin marketplace add shannon-framework/shannon
claude plugin install shannon@shannon-framework

# If already installed
claude plugin update shannon@shannon-framework

# Restart Claude Code
```

### Step 3: Verify Installation

```bash
/shannon:status
# Should show: "Shannon Framework v5.0.0 active"
```

### Step 4: Optional - Generate Custom Instructions

```bash
cd /your/project
/shannon:generate_instructions
/shannon:prime  # Reload to apply instructions
```

---

## 💡 Usage Examples

### Example 1: Deep Debugging

```bash
# Intermittent bug that's hard to track down
/shannon:ultrathink "Payment processing fails 1 in 100 times with no error logs" --thoughts 250 --verify

# Result:
# - 250 sequential thoughts analyzing the problem
# - Systematic debugging protocol applied
# - Root cause: Race condition in transaction locking
# - Solution: Add transaction isolation level
# - Auto-verified with concurrent payment test
```

### Example 2: New Project Setup

```bash
# Start new project
/shannon:prime  # Initialize session

# Analyze specification
/shannon:spec "Build task management app with React, Node.js, PostgreSQL"

# Execute (will generate custom instructions automatically)
/shannon:do "implement authentication system"

# Custom instructions now saved to .shannon/custom_instructions.md
# Will auto-load in future sessions
```

### Example 3: Command Orchestration

```bash
# Full automated workflow
/shannon:task "Build REST API with auth and rate limiting" --auto

# Behind the scenes:
# 1. /shannon:prime (session init)
# 2. /shannon:spec (8D analysis)
# 3. /shannon:wave (parallel execution if complex)
# 4. Custom instructions generated if first time
```

---

## 🎯 What's Next (V5.1+)

### Planned Features

1. **Custom Instructions Implementation**: Complete Python implementation of generator
2. **Enhanced UltraThink**: Integration with more systematic debugging patterns
3. **MCP Auto-Setup**: Guided setup for required MCPs
4. **Dashboard Integration**: Real-time command execution visualization

### Community Contributions Welcome

- Custom instruction templates for specific frameworks
- UltraThink debugging patterns
- Workflow examples
- Bug reports and fixes

**See**: `CONTRIBUTING.md`

---

## 🆘 Getting Help

### Documentation

- **Complete Guide**: `docs/COMMAND_ORCHESTRATION.md`
- **Command Reference**: `skills/using-shannon/SKILL.md`
- **Migration Help**: This document (V5_RELEASE_NOTES.md)

### Common Issues

**Q: Commands not found after upgrade**
A: Restart Claude Code and verify with `/shannon:status`

**Q: Hardcoded path errors**
A: V5.0.0 fixes these - ensure you're on latest version

**Q: Which command should I use?**
A: See decision tree in `docs/COMMAND_ORCHESTRATION.md`

**Q: UltraThink not working**
A: Requires Sequential Thinking MCP - check with `/shannon:check_mcps`

### Support

- **GitHub Issues**: https://github.com/krzemienski/shannon-framework/issues
- **Documentation**: README.md and docs/ directory
- **Status Check**: `/shannon:status`

---

## 👥 Credits

**Shannon Framework Team**
- Architecture and design
- Implementation and testing
- Documentation

**Contributors**
- Community feedback and bug reports
- Feature suggestions

---

## 📄 License

MIT License - See LICENSE file

---

## 🔗 Links

- **Repository**: https://github.com/krzemienski/shannon-framework
- **Documentation**: README.md
- **Changelog**: CHANGELOG.md
- **Contributing**: CONTRIBUTING.md

---

**Welcome to Shannon Framework V5.0.0!** 🎉

The most comprehensive AI development framework for Claude, now with better command isolation, deeper debugging, and smarter project awareness.

---

**Release Date**: November 18, 2025
**Version**: 5.0.0
**Breaking Changes**: Yes (Command Namespacing)
**Migration Required**: Yes (Simple find/replace)
**Recommended**: Yes (Critical bug fixes + powerful new features)

