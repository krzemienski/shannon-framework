# Shannon CLI Specification V2.0 - Complete Architectural Redesign

**Date**: 2025-11-13
**Status**: New specification complete
**Approach**: Thin wrapper over Shannon Framework (NOT reimplementation)

## Key Changes from V1.0

### V1.0 (WRONG Approach)
- Reimplemented 8D algorithm in Python (~800 lines)
- Reimplemented wave orchestration (~400 lines)
- Reimplemented domain detection (~424 lines)
- Reimplemented MCP engine (~363 lines)
- Reimplemented phase planning (~510 lines)
- Reimplemented timeline estimation (~245 lines)
- **Total**: 6,918 lines of duplicated logic

### V2.0 (CORRECT Approach)
- Delegates to spec-analysis skill (0 lines of algorithm code)
- Delegates to wave-orchestration skill (0 lines)
- Delegates to ALL Shannon Framework skills
- **Total**: ~3,000 lines (CLI wrapper only)

**Code Reduction**: 57% smaller
**Algorithm Duplication**: 0%
**Maintenance**: Framework updates propagate automatically

## Core Architecture

Shannon CLI is a **thin wrapper** that:
1. Loads Shannon Framework plugin via SDK
2. Invokes skills/commands
3. Streams progress with Rich UI
4. Saves results to local sessions
5. Provides JSON output for automation

## Components

**Layer 1: CLI Interface** (~500 lines)
- Click commands: analyze, wave, status, resume
- Argument parsing and validation
- Exit code handling

**Layer 2: SDK Orchestration** (~800 lines)
- ShannonSDKClient: Plugin loading + skill invocation
- MessageParser: Extract results from SDK messages
- ProgressUI: Rich spinners/tables
- OutputFormatter: JSON/Markdown/Tables

**Layer 3: Session Storage** (~700 lines - reuse Wave 1)
- SessionManager: Local file persistence
- Config: CLI configuration
- Logger: Extreme logging
- Models: Pydantic type safety

**Layer 4: Shannon Framework** (delegated)
- 18 skills (11,045 behavioral lines)
- 15 commands
- 9 core files
- Loaded via SDK plugins

## Implementation Plan

**Wave 1**: ✅ Complete (Config, Logger, SessionManager, Models)
**Wave 2**: SDK Integration (6 hours) - ShannonSDKClient + MessageParser
**Wave 3**: CLI Commands (8 hours) - Click commands as wrappers
**Wave 4**: Progress UI (6 hours) - Rich spinners/tables
**Wave 5**: Output Formatting (4 hours) - JSON/Markdown formatters
**Wave 6**: Functional Testing (6 hours) - Shell script validation

**Total**: 30 hours (59% faster than V1.0's 72.5 hours)

## Files to Delete

~5,118 lines of reimplemented algorithms:
- src/shannon/core/spec_analyzer.py
- src/shannon/core/domain_detector.py
- src/shannon/core/mcp_recommender.py
- src/shannon/core/phase_planner.py
- src/shannon/core/timeline_estimator.py
- src/shannon/core/wave_planner.py
- src/shannon/core/wave_coordinator.py
- src/shannon/core/progress_tracker.py
- src/shannon/sdk/agent_factory.py (old version)
- src/shannon/sdk/prompt_builder.py (old version)
- src/shannon/sdk/templates/*

## Success Criteria

✅ Invokes Shannon Framework skills via SDK
✅ Shows real-time progress with Rich UI
✅ Outputs JSON for automation
✅ Saves sessions locally
✅ Zero algorithm duplication
✅ Code ≤ 3,000 lines
✅ Shell script testing only (NO pytest)
✅ Works standalone (no Claude Code UI)

Complete specification in: TECHNICAL_SPEC_V2.md
