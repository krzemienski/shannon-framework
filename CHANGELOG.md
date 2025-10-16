# Changelog

All notable changes to Shannon Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-10-16

### Added

#### Plugin Architecture
- Complete migration to Claude Code plugin system for better distribution and discoverability
- Plugin manifest (`.claude-plugin/plugin.json`) with comprehensive metadata
- Marketplace configuration for official Shannon marketplace
- Repository-level plugin configuration support for teams

#### New Commands
- `/sh_status` - Framework status, MCP servers, and configuration health check
- `/sh_check_mcps` - Comprehensive MCP server verification with setup guidance
- SessionStart hook notification for user awareness

#### Enhanced Documentation
- `docs/PLUGIN_INSTALL.md` - Complete plugin installation guide
- `docs/MIGRATION_GUIDE.md` - Legacy to plugin migration instructions
- `docs/TEAM_SETUP.md` - Team and enterprise configuration guide
- `shannon-plugin/README.md` - Plugin-specific documentation
- `CHANGELOG.md` - Version history (this file)

#### Agent Capabilities
- Added 'capabilities' arrays to all 19 agents for better discoverability
- Enhanced agent frontmatter with clear capability descriptions
- Improved agent auto-activation through capability-based matching

### Changed

#### Installation Method
- **BREAKING**: Installation now via plugin system instead of CLAUDE.md
- Commands: `/plugin marketplace add shannon-framework/shannon` → `/plugin install shannon@shannon-framework`
- No longer requires project-level CLAUDE.md configuration
- Shannon now available globally across all Claude Code sessions

#### Directory Structure
- Reorganized to match Claude Code plugin requirements
- Commands at `shannon-plugin/commands/` (plugin root)
- Agents at `shannon-plugin/agents/` (plugin root)
- Hooks at `shannon-plugin/hooks/` (plugin root)
- Core patterns at `shannon-plugin/core/` (reference documentation)
- Modes at `shannon-plugin/modes/` (reference documentation)

#### Hook System
- PreCompact hook now uses `${CLAUDE_PLUGIN_ROOT}` for portability
- Added SessionStart hook for user onboarding
- Centralized hook configuration in `hooks/hooks.json`

#### Documentation
- Updated README.md with plugin installation as primary method
- Updated SHANNON_V3_SPECIFICATION.md with plugin architecture section
- Updated SHANNON_COMMANDS_GUIDE.md with plugin references
- Legacy CLAUDE.md-based documentation moved to Shannon-legacy/

### Deprecated

- **CLAUDE.md-based installation**: Still functional but deprecated
- **Shannon/ directory structure**: Renamed to Shannon-legacy/ for reference
- **@-reference system**: Not supported in plugin architecture
- **Project-level Shannon configuration**: Use plugin system instead

### Fixed

- Improved command frontmatter consistency
- Enhanced agent descriptions for better auto-activation
- Clarified MCP server requirements vs recommendations
- Updated all documentation for accuracy

### Removed

- None (all functionality preserved in plugin format)

### BREAKING CHANGES

**Installation Method**:
- Previous installation via CLAUDE.md @-references no longer supported
- Must migrate to plugin system for Shannon v3.0.0+
- See [MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) for upgrade path

**Directory Structure**:
- Shannon/ renamed to Shannon-legacy/
- Active plugin in shannon-plugin/ directory
- Commands and agents in new locations

**Compatibility**:
- Checkpoints from Shannon v2.x are compatible with v3.0.0 (same Serena MCP)
- Command names unchanged - workflows remain compatible
- Agent behavior unchanged - auto-activation works identically

## [2.0.0] - 2024-09-30

### Shannon V2 Features
- 8-dimensional complexity analysis
- Wave orchestration system
- Context preservation via Serena MCP
- NO MOCKS testing philosophy
- 5-phase planning framework
- CLAUDE.md-based distribution

## [1.0.0] - 2024-09-01

### Initial Shannon Release
- Specification analysis capabilities
- Basic phase planning
- Context management
- Testing patterns

---

## Migration Notes

### v2.x → v3.0.0

**Required Actions**:
1. Remove Shannon @-references from CLAUDE.md
2. Install Shannon plugin via marketplace
3. Configure Serena MCP if not already configured
4. Verify installation with `/sh_status`

**No Code Changes**: Your projects and workflows remain unchanged. Only installation method changes.

**Checkpoint Compatibility**: v2.x checkpoints work with v3.0.0 (same Serena MCP format).

### v1.x → v3.0.0

Recommended: Upgrade to v2.0.0 first, then v3.0.0. Or follow v3.0.0 migration guide directly.

---

## Future Roadmap

### Planned for v3.1.0
- Enhanced wave strategies
- Additional specification templates
- Improved MCP discovery algorithms
- Extended team collaboration features

### Planned for v3.2.0
- Visual specification analysis dashboard
- Wave execution monitoring UI
- Checkpoint browser and management tools
- Analytics and usage insights

### Planned for v4.0.0
- Plugin extension API
- Custom complexity dimensions
- Industry-specific analysis frameworks
- Shannon ecosystem marketplace

---

For complete details on any release, see the [GitHub Releases](https://github.com/shannon-framework/shannon/releases) page.

For issues or feature requests, file at [GitHub Issues](https://github.com/shannon-framework/shannon/issues).
