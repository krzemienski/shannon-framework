# Changelog

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
