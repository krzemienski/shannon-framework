# Changelog

All notable changes to Shannon Framework are documented here.

---

## [6.0.0] - 2026-05-24

### ✨ Added

**Project-level opt-in gate** — Shannon hooks are now silent by default and only
fire in projects that explicitly opt in:
- `/shannon:enable` writes `.shannon/active` (hooks fire in this project)
- `/shannon:disable` writes `.shannon/disabled` (sticky off)
- Override matrix: `.shannon/active` present → fire; `.shannon/disabled` present
  → no-op; neither → no-op (default off); `SHANNON_DISABLE=1` → per-shell off;
  `SHANNON_GLOBAL=1` → fire everywhere (testing escape)
- `lib/hook-runner.js` gained `isShannonActive()` + `projectRoot()`; `runHook()`
  short-circuits to exit 0 when the gate fails. Ends cross-project hook pollution.

**Activation benchmark suite** — `benchmarks/run-activation.js`:
- 322-row trigger × innocent-corpus matrix (recall + precision per skill)
- Re-runnable in ~250ms (pure node, no Claude session)

### 🔧 Fixed

**Skill activation precision (F1 0.80 → 1.00 across all 30 skills)**:
- Word-boundary matcher replaces substring `includes()` (killed "iterate"→"reiterate"
  style false positives)
- 4 dangerous single-word triggers removed/specialized:
  `iterate` (reflect), `done` (evidence-gate), `trace`→`session trace`
  (observability), `doctor`→`shannon doctor` (observability)
- Innocent-prompt false positives: 4 → 0

**Plugin manifest** — removed `hooks` dir-path field; Claude Code auto-discovers
`hooks/hooks.json` from convention (fixed duplicate-load error). Flattened symlinks
to real files for CC installer cache compatibility.

**Hook protocol** — UserPromptSubmit hint now exit-0 + stdout (was exit-2 blocking).

### 📊 Validation

Real-system benchmark on the merged release HEAD: 322 rows, recall 100% (282/282),
innocent-clean 100% (40/40), 0 false positives, all skills F1=1.00. Evidence:
`plans/260524-0000-shannon-v6-stabilize-and-release/`.

---

## [5.5.0] - TBD

### ✨ Added

**NEW: Project Onboarding**:
- `/shannon:init` - Complete project onboarding command for existing codebases
  * Deep analysis of every file
  * Tech stack detection (languages, frameworks, versions)
  * Architecture pattern mapping (MVC, Clean, Microservices, etc.)
  * NO MOCKS compliance audit
  * MCP recommendations (tier-based)
  * Generates SHANNON.md and AGENTS.md
  * Configures validation gates (test, build, lint)
  * Shannon Readiness Score (0-100)
  * Flags: `--quick`, `--full`, `--dry-run`

**NEW: Project Onboarding Skill**:
- `project-onboarding` skill for comprehensive codebase scanning
  * Scans every file in project (respects .gitignore)
  * Detects architecture patterns
  * Calculates complexity metrics
  * Audits testing compliance
  * Generates project documentation

**ENHANCED: Existing Commands**:
- `/shannon:do` - Auto-detects Shannon initialization
  * Suggests `/shannon:init` for non-initialized projects
  * 3-5x faster execution for initialized projects
  * New flag: `--skip-init-check`

- `/shannon:spec` - Result caching with intelligent reuse
  * Caches analysis results in Serena MCP
  * 60-120x speedup for repeated analysis
  * Auto-invalidates after 1 week
  * New flags: `--no-cache`, `--cache-only`

- `/shannon:wave` - Progressive execution mode
  * Wave-by-wave review and modification
  * Interactive plan adjustment mid-execution
  * New flag: `--progressive`

- `/shannon:status` - Shannon Readiness Score dashboard
  * Quantitative health score (0-100)
  * Breakdown by category (MCP, Testing, Docs, Gates, Architecture)
  * Actionable recommendations
  * Track improvements over time

**NEW: Generated Project Files** (per project after `/shannon:init`):
- `.shannon/config.json` - Shannon configuration
- `.shannon/project-index.json` - Complete codebase index
- `.shannon/architecture.json` - Architecture map
- `.shannon/baseline-metrics.json` - Initial complexity/debt metrics
- `.shannon/sessions/` - Session checkpoints directory
- `SHANNON.md` - Shannon integration guide
- `AGENTS.md` - Agent onboarding context

### 🚀 Performance

- `/shannon:do` 3-5x faster for initialized projects (context loading vs exploration)
- `/shannon:spec` 60-120x faster for cached results (0.5s vs 30-60s)
- One-time init cost: 5-30 minutes (project size-dependent)
- ROI breakeven: 2-10 sessions

### 📚 Documentation

**New**:
- `commands/init.md` - Complete `/shannon:init` documentation
- `skills/project-onboarding/SKILL.md` - Project onboarding skill guide
- `docs/V5.5_IMPROVEMENTS.md` - Comprehensive improvements breakdown
- `docs/V5.5_RELEASE_NOTES.md` - Complete release notes

**Updated**:
- `README.md` - Version 5.5.0, added `/shannon:init` to Quick Start
- `commands/do.md` - Added init detection section
- `commands/spec.md` - Added caching section
- `commands/wave.md` - Added progressive mode section
- `commands/status.md` - Added readiness score section

### 🔄 Backward Compatibility

**100% backward compatible with V5.0**:
- All V5.0 commands work identically
- All V5.0 flags still supported
- No breaking changes to command syntax
- No breaking changes to output format

**What's New (Additive Only)**:
- New command: `/shannon:init`
- New flags: `--skip-init-check`, `--no-cache`, `--cache-only`, `--progressive`
- Enhanced output: Readiness scores, cached indicators

### 🎯 Migration from V5.0

**Optional (recommended for existing projects)**:
```bash
cd your-project
/shannon:init
```

**No mandatory changes** - all V5.5 features are opt-in

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
