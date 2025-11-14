# Shannon CLI - Architecture Pivot Point

**Date**: 2025-11-13
**Status**: PAUSED for complete architectural redesign

## Critical Discovery

Shannon CLI was being implemented as a REIMPLEMENTATION of Shannon Framework, when it should be a THIN WRAPPER that LEVERAGES the framework.

## Current (WRONG) Implementation

**What we built in Waves 1-3**:
- SpecAnalyzer with 8D algorithm reimplemented in Python
- WavePlanner reimplementing dependency analysis
- Domain/MCP/Phase components duplicating framework logic
- ~6,740 lines of code reimplementing what already exists

## Correct Architecture (To Be Designed)

**Shannon CLI should be**:
- Thin wrapper over Shannon Framework
- Uses SDK to spawn agents that invoke Shannon skills/commands
- Adds: CLI interface, progress tracking, session persistence, programmatic API
- Does NOT reimplement: 8D analysis, wave orchestration, skill logic

**Integration Pattern**:
```
User: shannon analyze spec.md
  ↓
Shannon CLI (Python wrapper)
  ↓
SDK query() with Shannon plugin loaded
  ↓
Agent executes: /shannon:spec @spec.md
  ↓
Shannon Framework skill: spec-analysis
  ↓
Results streamed to CLI with progress visibility
  ↓
CLI saves to session + displays formatted output
```

## Next Steps

1. Read COMPLETE Shannon Framework structure (18 skills, 15 commands, 9 core docs)
2. Read COMPLETE current TECHNICAL_SPEC.md (4,920 lines)
3. Identify what CLI should ACTUALLY provide vs what framework has
4. Design TRUE architecture (thin wrapper + progress tracking)
5. Write NEW specification

## Code to Review/Potentially Discard

- src/shannon/core/spec_analyzer.py (~800 lines) - Reimplements what spec-analysis skill does
- src/shannon/core/domain_detector.py - Duplicates framework
- src/shannon/core/mcp_recommender.py - Duplicates framework
- src/shannon/core/phase_planner.py - Duplicates framework
- src/shannon/core/wave_planner.py - Duplicates framework
- src/shannon/core/timeline_estimator.py - Duplicates framework

**Total duplicate code**: ~3,000+ lines that shouldn't exist

## Code to Keep

- src/shannon/config.py ✅ - CLI needs configuration
- src/shannon/logger.py ✅ - CLI needs logging
- src/shannon/storage/models.py ✅ - Type safety for results
- src/shannon/core/session_manager.py ✅ - Session persistence

## Analysis Required

Need to understand:
- How Shannon Framework skills work (18 skills)
- How Shannon commands work (15 commands)
- How to invoke them via SDK
- What CLI uniquely provides
- How to stream progress visibly
