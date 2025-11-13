# Shannon Framework - Integration & Interaction Patterns

**Generated**: 2025-01-12
**Purpose**: Document how commands, skills, hooks, and core files work together
**Based On**: Complete analysis of all Shannon components
**Sequential Thoughts**: 107 total (ongoing)

---

## Executive Summary

Shannon Framework's power comes from **multi-layer integration** across 4 component types working in concert. Each component has distinct responsibilities, but they form a cohesive system through well-defined integration patterns.

**Key Architecture**: Defense-in-depth enforcement through layered components
- **Core Files** (11K lines): Foundational specifications
- **Hooks** (5 scripts): Automatic enforcement mesh
- **Skills** (18 × ~800 lines): Workflow implementations
- **Commands** (15 × ~300 lines): User-facing interface

Together: ~30,000+ lines of coordinated methodology

---

## Complete Workflow Example: `/shannon:spec "Build web app"`

### Layer-by-Layer Execution

```
USER types: /shannon:spec "Build a task management web app with React and PostgreSQL"
    ↓
─────────────────────────────────────────────────────────────
COMMAND LAYER (spec.md)
─────────────────────────────────────────────────────────────
1. SlashCommand tool receives "shannon:spec"
2. commands/spec.md content loads and expands into prompt
3. Command content says: "Invoke spec-analysis skill"
4. Parsed arguments: spec_text = "Build a task..."
    ↓
─────────────────────────────────────────────────────────────
HOOK LAYER (user_prompt_submit.py)
─────────────────────────────────────────────────────────────
5. UserPromptSubmit hook fires BEFORE processing
6. Hook reads: .serena/north_star.txt (if exists)
7. Hook injects: "🎯 North Star Goal: [goal]"
8. Enhanced prompt now includes alignment context
    ↓
─────────────────────────────────────────────────────────────
SKILL LAYER (spec-analysis)
─────────────────────────────────────────────────────────────
9. Claude invokes: Skill tool with "spec-analysis"
10. skills/spec-analysis/SKILL.md loads (1,545 lines)
11. Skill instructs: Run 8D complexity algorithm
12. Skill references: core/SPEC_ANALYSIS.md (for complete algorithm)
13. Skill invokes sub-skills: mcp-discovery, phase-planning
14. Workflow executes:
    - Step 1: Parse specification
    - Step 2: Calculate 8D scores
    - Step 3: Detect domains
    - Step 4: Recommend MCPs
    - Step 5: Generate 5-phase plan
    - Step 6: Save to Serena
    - Step 7: Format output
15. Results ready: complexity=0.55, domains={Frontend:45%, Backend:30%, Database:25%}
    ↓
─────────────────────────────────────────────────────────────
MCP LAYER (Serena)
─────────────────────────────────────────────────────────────
16. Skill calls: mcp__serena__write_memory()
17. Serena stores: spec_analysis_20250112_100000
18. Memory includes: complexity scores, domain breakdown, MCP recommendations, phase plan
19. Future waves/agents can read this via: read_memory("spec_analysis_20250112_100000")
    ↓
─────────────────────────────────────────────────────────────
OUTPUT LAYER (Command Formatting)
─────────────────────────────────────────────────────────────
20. Command spec.md defines output format:
    ```
    📊 Shannon Specification Analysis
    **Complexity**: {score}/100 ({label})
    8D Breakdown: [table]
    Domain Breakdown: [percentages]
    MCP Recommendations: [tiered list]
    ```
21. Claude formats results per specification
22. Professional output with box drawing, emoji, structure
    ↓
─────────────────────────────────────────────────────────────
USER SEES
─────────────────────────────────────────────────────────────
23. Formatted analysis report
24. Complexity: 55/100 (COMPLEX)
25. Recommendation: Use wave-based execution
26. Next step: /shannon:wave to execute
```

### What Happened at Each Layer

- **Core**: Provided complete algorithm specification (referenced by skill)
- **Command**: Provided user interface and output formatting
- **Hook**: Injected North Star context for alignment
- **Skill**: Executed algorithm, orchestrated sub-skills, saved to Serena
- **MCP**: Persisted results for future use

---

## Defense-in-Depth: NO MOCKS Enforcement

Shannon enforces NO MOCKS at **4 layers simultaneously**:

### Layer 1: Core File (Foundation)
**File**: TESTING_PHILOSOPHY.md (1,050 lines)
- **What**: Complete philosophical foundation
- **Content**: Why mocks fail, real system benefits, all platform patterns
- **Enforcement**: Educational (explains the principle)

### Layer 2: Meta-Skill (Behavioral Requirement)
**Skill**: using-shannon (723 lines)
- **What**: Declares NO MOCKS as Iron Law
- **Content**: Baseline violations, rationalization counters, mandatory workflows
- **Enforcement**: Strong prompt (ALL CAPS, MUST, REQUIRED)
- **Loading**: Automatic via session_start.sh hook

### Layer 3: Implementation Skill (Workflow Guidance)
**Skill**: functional-testing (1,403 lines)
- **What**: Implements NO MOCKS with practical patterns
- **Content**: Platform-specific testing (Puppeteer, iOS Simulator, Real HTTP)
- **Enforcement**: Workflow instructions, test generation, violation scanning
- **Invocation**: Via test command or auto-discovery

### Layer 4: Hook (Automatic Blocking)
**Hook**: post_tool_use.py (164 lines)
- **What**: Automatically blocks mock usage in real-time
- **Content**: 13 regex patterns, test file detection, blocking logic
- **Enforcement**: ABSOLUTE - cannot be overridden
- **Execution**: Automatic on every Write/Edit to test files

### Enforcement Cascade

```
User tries to write: jest.mock()
    ↓
1. Core File: "Mocks create false confidence" (if read)
2. Meta-Skill: "YOU MUST use functional tests ONLY"
3. Skill: "Use Puppeteer MCP for real browser testing"
4. Hook: BLOCKS write, returns error
    ↓
Result: Mock code NEVER WRITTEN

Even if user ignores skills (1-3), hook (4) blocks automatically.
```

This is **defense-in-depth**: Multiple layers enforce same principle, so violating requires circumventing ALL layers (effectively impossible).

---

## Data Flow: Serena MCP as Central State

```
                    ┌──────────────────┐
                    │   SERENA MCP     │
                    │  (Central State) │
                    └────────┬─────────┘
                             │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐      ┌──────▼─────┐     ┌────▼────┐
    │ Commands│      │   Skills   │     │  Hooks  │
    │  write  │      │ read/write │     │  read   │
    └────┬────┘      └──────┬─────┘     └────┬────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                    ┌───────▼────────┐
                    │  User Session  │
                    └────────────────┘

Flow Pattern:
1. Commands invoke skills
2. Skills save results to Serena (spec analysis, wave results, goals)
3. Other skills read from Serena (wave-orchestration reads spec_analysis)
4. Hooks read signals from Serena (user_prompt_submit reads North Star)
5. Context preserved across sessions via Serena
6. Waves coordinate through shared Serena state
```

**Serena is Shannon's BACKBONE** - persistent state layer everything depends on.

---

## Component Interaction Matrix

| From ↓ / To → | Commands | Skills | Hooks | Core Files | Serena |
|---------------|----------|--------|-------|------------|--------|
| **Commands** | Chain (task→prime) | Invoke ✅ | Wrapped by hooks | Reference 📖 | Via skills |
| **Skills** | N/A | Invoke sub-skills ✅ | Enforced by hooks | Reference ✅ | Read/Write ✅ |
| **Hooks** | Wrap execution ✅ | Trigger ✅ | N/A | N/A | Read ✅ |
| **Core Files** | Inform 📖 | Inform ✅ | Document 📖 | N/A | Via skills |
| **Serena** | Via skills | Direct ✅ | Filesystem IPC | Via skills | N/A |

**Legend**: ✅ Direct integration, 📖 Reference/documentation relationship

---

## Key Integration Patterns

### Pattern 1: Command → Skill Delegation
Commands are thin wrappers that delegate to skills for actual work.

### Pattern 2: Skill Composition
Skills invoke sub-skills to build complex workflows from simple components.

### Pattern 3: Hook Enforcement
Hooks enforce what skills describe through automatic blocking/injection.

### Pattern 4: Serena State Sharing
All components share state through Serena MCP (specs, waves, goals, checkpoints).

### Pattern 5: Core File Reference
Skills and commands reference core files for complete methodologies.

### Pattern 6: Progressive Disclosure
Information flows: Command summary → Skill workflow → Core file complete algorithm

---

## Phase 7 Completion

✅ **All Integration Patterns Documented**:
- Complete workflow example traced through all layers
- Defense-in-depth pattern explained (NO MOCKS 4-layer enforcement)
- Data flow via Serena MCP
- Component interaction matrix
- 6 key integration patterns identified

**Next**: Phase 9 - Architecture Synthesis (100+ Thoughts Required)
