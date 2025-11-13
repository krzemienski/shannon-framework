---
name: SHANNON_INTEGRATION
description: Shannon framework awareness for SuperClaude integration with enhanced patterns
triggers: [shannon commands, shannon project detection, /sh: prefix, serena required]
auto_activate: true
activation_condition: shannon_command OR shannon_project_detected OR serena_context_available
category: integration
priority: high
---

# Shannon Integration Mode

## Purpose

Enable seamless Shannon framework awareness and integration within SuperClaude environments. This mode bridges Shannon's specification analysis, wave orchestration, and context preservation patterns with SuperClaude's existing command system, personas, and MCP server infrastructure.

**Core Value**: Transform SuperClaude into a Shannon-aware system without disrupting existing workflows, providing enhanced specification analysis, parallel wave orchestration, and zero-context-loss session management.

## Mode Architecture

### Integration Layer
```
┌──────────────────────────────────────────┐
│     SuperClaude Base Framework           │
│  (Commands, Personas, MCP, Modes)        │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│     SHANNON_INTEGRATION Mode             │
│  • Pattern awareness                     │
│  • Tool coordination                     │
│  • Context preservation                  │
│  • Wave orchestration                    │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│     Shannon-Enhanced Operations          │
│  • Spec analysis with complexity         │
│  • Phase planning with validation        │
│  • Wave execution with parallelism       │
│  • Context restoration with Serena       │
└──────────────────────────────────────────┘
```

## Activation Triggers

### Automatic Activation

**Shannon Command Detection**:
- Any command starting with `/sh:` prefix
- Commands: analyze-spec, create-phases, create-waves, checkpoint, restore
- Shannon-specific flags: `--shannon`, `--wave`, `--checkpoint`

**Project Context Detection**:
- Serena MCP active with Shannon context keys
- Shannon memory present: "shannon_spec_analysis", "shannon_phase_plan", "shannon_wave_*"
- Shannon project structure detected (phase directories, wave checkpoints)

**Behavioral Indicators**:
- User mentions "Shannon framework", "wave orchestration", "phase planning"
- Request for systematic specification analysis with complexity scoring
- Need for parallel wave execution with context preservation
- Context restoration scenarios across sessions

### Manual Activation
- Flag: `--shannon-mode`, `--shannon-integration`
- Command: `/mode shannon` (if mode switching implemented)
- Explicit request: "Use Shannon patterns", "Enable Shannon mode"

## Behavioral Modifications

### 1. Shannon Pattern Awareness

**Specification Analysis**:
```yaml
when: specification_provided OR requirements_document
behavior:
  - Automatically trigger MODE_SpecAnalysis
  - Apply 8-dimensional complexity framework
  - Calculate domain percentages (must sum to 100%)
  - Generate MCP server recommendations (Tier 1-4)
  - Create structured phase plan (5 phases default)
  - Save analysis to Serena with key "shannon_spec_analysis"

output_format:
  - Quantitative scores (0.0-1.0 scale)
  - Evidence-based claims (cite specification)
  - Structured templates (consistency)
  - Validation gates (quality assurance)
```

**Phase Planning**:
```yaml
when: create_phases_command OR post_spec_analysis
behavior:
  - Reference stored specification analysis
  - Generate 5-phase implementation plan
  - Define validation gates per phase
  - Estimate timeline (hours/days range)
  - Identify dependencies and risks
  - Save plan to Serena with key "shannon_phase_plan"

validation:
  - Each phase has clear deliverables
  - Validation gates are testable
  - Dependencies are explicit
  - Timeline is evidence-based
```

**Wave Orchestration**:
```yaml
when: create_waves_command OR complexity >= 0.7
behavior:
  - Trigger MODE_WaveOrchestration
  - Identify parallel execution opportunities
  - Group independent tasks into waves
  - Spawn wave agents in single message (true parallel)
  - Calculate speedup gains (report to user)
  - Save wave results to Serena per wave

context_management:
  - BEFORE wave: Save previous wave context to Serena
  - DURING wave: All agents load complete context
  - AFTER wave: Synthesize results, save checkpoint
  - Track ALL Serena keys for restoration
```

### 2. Tool Coordination Patterns

**Mandatory Tool Usage**:
```yaml
serena_mcp:
  requirement: MANDATORY for all Shannon operations
  usage:
    - write_memory: Save analysis, plans, wave results
    - read_memory: Restore context across sessions
    - list_memories: Verify Shannon state
    - delete_memory: Clean completed waves

  critical_keys:
    - shannon_spec_analysis: Specification analysis results
    - shannon_phase_plan: Phase implementation plan
    - shannon_wave_1/2/3/N: Wave execution results
    - shannon_checkpoint: Current state snapshot

sequential_mcp:
  requirement: PREFERRED for complex analysis
  usage:
    - Specification analysis (structured reasoning)
    - Complexity scoring (multi-dimensional)
    - Phase planning (systematic approach)
    - Wave synthesis (result integration)

context7_mcp:
  requirement: RECOMMENDED for framework patterns
  usage:
    - Framework best practices lookup
    - Library documentation retrieval
    - Pattern validation
    - Technology research
```

**Tool Selection Matrix**:
```yaml
specification_analysis:
  primary: [Sequential, Read, Grep, Serena]
  secondary: [Context7]
  avoid: [Magic, Playwright]

phase_planning:
  primary: [Sequential, Serena, TodoWrite]
  secondary: [Context7]
  avoid: [Playwright, Puppeteer]

wave_orchestration:
  primary: [Task, Serena, Sequential]
  secondary: [all domain-specific MCPs]
  coordination: parallel_tool_calls

context_preservation:
  primary: [Serena (mandatory)]
  secondary: [Read, Write]
  critical: write_memory BEFORE wave spawn
```

### 3. NO MOCKS Philosophy

**Testing Standards**:
```yaml
implementation_phase:
  testing_requirement: functional_only
  mocking_policy: STRICTLY_FORBIDDEN

  enforcement:
    - Grep verification: "mock|stub|fake|spy" → FAIL
    - Real components only
    - Actual service integration
    - Real database interactions (test DB)
    - Real API calls (test endpoints)

  validation:
    - Tests validate real behavior
    - Integration points are genuine
    - Error handling is authentic
    - Performance is measurable

exceptions:
  none: "NO MOCKS means NO MOCKS"
  alternatives:
    - Test databases (real DB, test data)
    - Test APIs (real endpoints, test env)
    - Local services (real stack, isolated)
```

**Implementation Validation**:
```
BEFORE marking implementation complete:
✓ Run: grep -r "mock\|stub\|fake\|spy" tests/
✓ Verify: Zero matches found
✓ Validate: All tests use real components
✓ Confirm: Tests actually exercise real behavior
✓ Document: Test environment setup (if needed)
```

### 4. Context Preservation Strategy

**Session Lifecycle**:
```yaml
session_start:
  - list_memories() → Identify Shannon state
  - read_memory("shannon_spec_analysis") → Load analysis
  - read_memory("shannon_phase_plan") → Load plan
  - read_memory("shannon_wave_N") → Load wave results
  - read_memory("shannon_checkpoint") → Restore state
  - Reconstruct TodoWrite from checkpoint
  - Display: "Shannon context restored - Wave N of M complete"

during_session:
  - write_memory() after each major milestone
  - Checkpoint: Every 30 minutes OR before risky operations
  - Track: All Serena keys in current session
  - Validate: Context completeness before wave spawn

session_end:
  - write_memory("shannon_checkpoint", full_state)
  - write_memory("shannon_session_summary", outcomes)
  - List all Serena keys for user reference
  - Display: "Shannon state saved - N keys stored"

session_restoration:
  - ZERO CONTEXT LOSS guarantee
  - Perfect session continuity
  - TodoWrite reconstruction from checkpoint
  - Ready to continue from exact point
```

**PreCompact Hook Integration**:
```yaml
hook_purpose: Prevent Serena context loss during compaction
hook_location: Shannon/Hooks/precompact.py
hook_behavior:
  - Detects Serena memory keys before compaction
  - Preserves Shannon state to stable storage
  - Restores after compaction completes
  - Validates no data loss

critical_for:
  - Long sessions (>2 hours)
  - Multi-wave projects
  - Cross-session work
  - Complex specifications
```

## Integration Points

### SuperClaude Command Enhancement

**Enhanced Commands**:
```yaml
/analyze:
  shannon_enhancement:
    - Add --shannon flag for spec analysis
    - Trigger MODE_SpecAnalysis when spec detected
    - Store results in Serena automatically
    - Generate phase plan suggestion

/implement:
  shannon_enhancement:
    - Enforce NO MOCKS in tests
    - Use Serena for context preservation
    - Check for Shannon phase plan first
    - Validate against specification

/improve:
  shannon_enhancement:
    - Load Shannon context if available
    - Reference original specification
    - Maintain phase alignment
    - Update Serena with improvements

/task:
  shannon_enhancement:
    - Coordinate with Shannon waves if active
    - Use Serena for task persistence
    - Align with phase validation gates
    - Enable wave-aware task delegation
```

**New Shannon Commands**:
- `/sh:analyze-spec` → Comprehensive specification analysis
- `/sh:create-phases` → Generate phase implementation plan
- `/sh:create-waves` → Orchestrate parallel wave execution
- `/sh:checkpoint` → Manual state preservation
- `/sh:restore` → Context restoration from checkpoint

### Persona Coordination

**Shannon-Aware Personas**:
```yaml
architect:
  shannon_integration:
    - Reference Shannon specification analysis
    - Align with phase boundaries
    - Consider wave coordination needs
    - Use Serena for architectural decisions

analyzer:
  shannon_integration:
    - Apply 8-dimensional complexity framework
    - Generate Shannon-compatible scores
    - Support specification analysis mode
    - Use Sequential MCP for structure

qa:
  shannon_integration:
    - Enforce NO MOCKS philosophy
    - Validate functional testing only
    - Check phase validation gates
    - Use Serena for test session tracking
```

### MCP Server Preferences

**Shannon Priority Matrix**:
```yaml
tier_1_mandatory:
  - Serena: Context preservation (CRITICAL)
  - Sequential: Structured analysis (HIGH)

tier_2_recommended:
  - Context7: Framework patterns (MEDIUM)
  - Playwright: Functional testing (MEDIUM)

tier_3_domain_specific:
  - Magic: UI implementation
  - Morphllm: Bulk transformations
  - Puppeteer: Browser automation

tier_4_avoided:
  - None: All tools useful in right context
  - Mocking libraries: FORBIDDEN
```

## Examples

### Example 1: Specification Analysis Flow

**User Input**:
```
I need to build a real-time chat application with user authentication,
message persistence, and typing indicators. Should support 1000
concurrent users. Need it done in 2 weeks.
```

**Shannon Integration Behavior**:
```
[Mode: SHANNON_INTEGRATION + MODE_SpecAnalysis activated]

🔍 SHANNON SPECIFICATION ANALYSIS

📊 Complexity Assessment:
- Structural: 0.75 (multiple services, real-time architecture)
- Technical: 0.85 (WebSocket handling, concurrency management)
- Integration: 0.60 (auth system, persistence layer)
- Performance: 0.80 (1000 concurrent users target)
- Security: 0.70 (authentication, authorization)
- Infrastructure: 0.65 (deployment, scaling)
- Testing: 0.65 (functional tests for real-time features)
- Documentation: 0.40 (standard project docs)

🔢 Overall Complexity: 0.68 (High)

🎯 Domain Distribution:
- Backend: 45% (WebSocket server, auth, persistence)
- Frontend: 30% (chat UI, typing indicators)
- Infrastructure: 15% (scaling, deployment)
- Security: 10% (auth implementation)
Total: 100% ✓

🛠️ MCP Server Recommendations:
Tier 1 (Mandatory):
- Serena: Context preservation across waves
- Sequential: Complex analysis and planning

Tier 2 (Recommended):
- Context7: WebSocket, auth patterns
- Playwright: Functional testing (NO MOCKS)

📋 Saved to Serena: Key "shannon_spec_analysis"

🚀 Ready for: /sh:create-phases
```

### Example 2: Wave Orchestration with Context

**User Input**:
```
/sh:create-waves
```

**Shannon Integration Behavior**:
```
[Mode: SHANNON_INTEGRATION + MODE_WaveOrchestration activated]

📖 Loading Shannon Context:
✓ Spec Analysis: shannon_spec_analysis
✓ Phase Plan: shannon_phase_plan
✓ Previous Waves: shannon_wave_1 (complete)

🌊 WAVE 2: Backend + Frontend (Parallel Execution)

Context Preservation:
✓ Wave 1 results saved to Serena
✓ All agents will load complete context
✓ Keys tracked: shannon_spec_analysis, shannon_phase_plan, shannon_wave_1

Spawning parallel wave agents...

[Task call 1: Backend implementation with Serena context]
[Task call 2: Frontend implementation with Serena context]

⏱️ Estimated speedup: 50% (2 parallel vs sequential)

🎯 After completion:
- Results synthesized
- Saved to Serena: shannon_wave_2
- Ready for Wave 3 or next session
```

### Example 3: Cross-Session Restoration

**Session 1 End**:
```
✅ Wave 2 complete
📝 Saving Shannon checkpoint...

Keys stored:
- shannon_spec_analysis: Initial specification analysis
- shannon_phase_plan: 5-phase implementation plan
- shannon_wave_1: Setup and architecture (complete)
- shannon_wave_2: Backend + Frontend (complete)
- shannon_checkpoint: Current state snapshot

🎯 Next session: Continue with Wave 3 (Testing & Integration)
```

**Session 2 Start**:
```
[Mode: SHANNON_INTEGRATION activated]

🔄 Restoring Shannon Context:
✓ shannon_spec_analysis: Loaded
✓ shannon_phase_plan: Loaded
✓ shannon_wave_1: Loaded (complete)
✓ shannon_wave_2: Loaded (complete)
✓ shannon_checkpoint: Loaded

📋 Reconstructing TodoWrite:
✓ Wave 3 tasks loaded
✓ Current status: Ready for Testing & Integration

✨ ZERO CONTEXT LOSS - Ready to continue Wave 3
```

## Quality Standards

### Integration Quality Gates

**Shannon Pattern Compliance**:
- ✓ Serena MCP used for all context operations
- ✓ Sequential MCP preferred for complex analysis
- ✓ NO MOCKS philosophy enforced in tests
- ✓ Context preservation before wave spawning
- ✓ Checkpoint creation at safe intervals

**Output Quality**:
- ✓ Quantitative scores provided (0.0-1.0 scale)
- ✓ Domain percentages sum to 100%
- ✓ Evidence-based claims (cite sources)
- ✓ Structured templates used consistently
- ✓ Validation gates defined and testable

**Session Continuity**:
- ✓ Zero context loss across sessions
- ✓ Perfect TodoWrite reconstruction
- ✓ Complete wave history preserved
- ✓ All Serena keys tracked and validated

### Performance Standards

**Response Time**:
- Specification analysis: < 60 seconds
- Phase planning: < 30 seconds
- Wave orchestration setup: < 20 seconds
- Context restoration: < 10 seconds

**Context Efficiency**:
- Serena key naming: Standardized ("shannon_*")
- Memory storage: Optimized (JSON compression)
- Checkpoint frequency: Adaptive (risk-based)
- Cross-session load time: < 5 seconds

## Compatibility Matrix

### SuperClaude Feature Compatibility

```yaml
commands:
  all_existing: COMPATIBLE (enhanced, not replaced)
  shannon_new: ADDITIVE (new commands coexist)

personas:
  all_existing: COMPATIBLE (Shannon-aware enhancements)
  shannon_agents: ADDITIVE (new sub-agents available)

modes:
  all_existing: COMPATIBLE (modes can combine)
  shannon_modes: ADDITIVE (new modes available)

mcp_servers:
  all_existing: COMPATIBLE (preference ordering added)
  serena: REQUIRED (mandatory for Shannon)

flags:
  all_existing: COMPATIBLE (new flags additive)
  shannon_flags: ADDITIVE (--shannon, --wave, etc.)
```

### Conflict Resolution

**Priority Rules**:
1. Serena context preservation > Speed optimization
2. NO MOCKS philosophy > Convenience
3. Shannon explicit flags > Auto-detection
4. Phase boundaries > Task granularity
5. Wave coordination > Individual completion

**Fallback Behavior**:
- If Serena unavailable → Warn, session-only context
- If Sequential unavailable → Use native reasoning
- If Context7 unavailable → Use web search
- Shannon patterns remain active with degraded capability

## Summary

SHANNON_INTEGRATION mode transforms SuperClaude into a Shannon-aware system that:

1. **Analyzes specifications systematically** with 8-dimensional complexity scoring
2. **Plans in phases** with validation gates and evidence-based timelines
3. **Orchestrates waves** for parallel execution with context preservation
4. **Enforces NO MOCKS** philosophy for authentic functional testing
5. **Preserves context perfectly** across sessions using Serena MCP
6. **Integrates seamlessly** with existing SuperClaude commands, personas, and modes

**Key Innovation**: Bridge Shannon's systematic project management patterns with SuperClaude's rich ecosystem without disruption—additive enhancement, not replacement.

**Critical Dependencies**:
- Serena MCP (mandatory for context preservation)
- Sequential MCP (recommended for structured analysis)
- PreCompact hook (critical for long sessions)

**User Experience**: Shannon patterns activate automatically when needed, provide systematic project analysis, enable zero-context-loss workflows, and deliver measurable execution improvements through parallel wave orchestration.