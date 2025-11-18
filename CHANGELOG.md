# Changelog

All notable changes to Shannon Framework are documented here.

---

## [5.4.0] - 2025-11-18

### ✨ Added
- **Planning parity**: `/shannon:brainstorm`, `/shannon:write_plan`, `/shannon:execute_plan` with new skills.
- **Debugging skills**: `systematic-debugging`, `root-cause-analysis`, and `forced-reading-sentinel`.
- **Forced Reading Sentinel**: Hook guardrail automatically warns for prompts/files ≥10k characters or ≥400 lines.
- **Documentation**: README, COMMAND_ORCHESTRATION, using-shannon updated for 22 commands / 26 skills.

### 🔧 Improved
- `/shannon:ultrathink` explicitly delegates to the new debugging skills.
- `hooks/user_prompt_submit.py` now emits sentinel banners plus North Star context.
- Added `tests/hooks/test_user_prompt_submit.py` to verify sentinel behavior.
- Installers & quick-start scripts updated to version 5.4.0.

### ✅ Validation
- `python3 -m pytest tests/hooks/test_user_prompt_submit.py`
- `./test_install.sh`
- `./test_universal_install.sh`

---

## [5.0.0] - 2025-11-18

### 🚨 BREAKING CHANGES

**Command Namespacing**: All commands now require `shannon:` prefix
- Old: `/do`, `/wave`, `/spec`
- New: `/shannon:do`, `/shannon:wave`, `/shannon:spec`
- **Migration**: Replace all command invocations with namespaced versions
- **Benefit**: Namespace isolation, no conflicts with other plugins

### ✨ Added

**New Commands**:
- `/shannon:ultrathink` - Deep debugging with 150+ sequential thoughts
- `/shannon:generate_instructions` - Auto-generate project-specific custom instructions

**New Features**:
- **Command Orchestration Guide**: `docs/COMMAND_ORCHESTRATION.md` (900+ lines)
- **Project-Specific Custom Instructions**: Auto-generated, persistent across sessions
- **Enhanced Documentation**: All 18 commands in `using-shannon` skill

### 🔧 Fixed

**Critical Portability Bugs**:
- Fixed hardcoded paths in `hooks/session_start.sh`
- Fixed hardcoded paths in `hooks/hooks.json` (2 instances)
- All hooks now use `${CLAUDE_PLUGIN_ROOT}`

### 📚 Documentation

**New**: `docs/COMMAND_ORCHESTRATION.md`, `commands/ultrathink.md`, `core/PROJECT_CUSTOM_INSTRUCTIONS.md`
**Updated**: `skills/using-shannon/SKILL.md`, `skills/intelligent-do/SKILL.md`

### 📦 MCP Requirements

- Sequential Thinking MCP (MANDATORY for `/shannon:ultrathink`)

### 🔄 Migration from V4

```bash
# Update all command calls
/do → /shannon:do
/wave → /shannon:wave
/spec → /shannon:spec
# (etc. for all 19 commands)
```

---

## [5.1.0] - 2025-11-15

### Added
- **/shannon:exec** - Autonomous task execution with library discovery and validation
- **exec skill** - Complete 6-phase orchestration workflow
- **3 Protocol References**:
  - LIBRARY_DISCOVERY_PROTOCOL.md (606 lines)
  - FUNCTIONAL_VALIDATION_PROTOCOL.md (888 lines)
  - GIT_WORKFLOW_PROTOCOL.md (905 lines)
- Integration with Shannon CLI V3.5.0 executor modules
- Multi-registry library discovery (npm, PyPI, CocoaPods, Maven, crates.io)
- 3-tier validation (static, tests, functional)
- Atomic git commits with validation messages
- Retry logic with rollback (max 3 attempts)

### Documentation
- Complete protocol documentation (2,399 lines)
- Exec skill guide (526 lines)
- Integration examples
- Platform-specific validation guides

### Requirements
- Shannon CLI V3.5.0+ (provides executor modules)
- Serena MCP (required for caching)

### Commands
- Total commands: 16 (was 15)
- Total skills: 19 (was 18)

See `skills/exec/SKILL.md` and `commands/exec.md` for complete documentation.

---

## [5.0.0] - 2025-01-12

### Changed
- Plugin name: shannon-plugin → shannon
- Namespace: /sh_* → /shannon:*
- Command files: All 14 renamed
- Structure: Guides moved to docs/guides/

### Added
- /shannon:task command (automated workflow)
- task-automation skill

### Fixed
- 415 shannon-plugin/ references updated
- All path references now relative

---

**For older changelog entries, see git history**
