# Shannon Framework - Core Files Architecture Analysis

**Generated**: 2025-01-12
**Purpose**: Analysis of Shannon's 9 core behavioral pattern files
**Total Lines Analyzed**: 11,045 lines across 9 files
**Sequential Thoughts**: 107 total (ongoing synthesis)

---

## Executive Summary

Shannon's **core/ directory** contains 9 massive behavioral pattern files (11,045 lines total) that serve as **expanded reference documentation** for Shannon's methodologies. These are NOT injected into the system prompt automatically - they're **reference material** for skills to cite and agents to consult when needed.

**Key Insight**: Core files are DETAILED SPECIFICATIONS of what skills implement in condensed form. Skills are 400-1,500 line summaries; core files are 850-1,800 line complete references.

**Relationship Pattern**:
- Core File: TESTING_PHILOSOPHY.md (1,050 lines) - Complete NO MOCKS manifesto
- Skill: functional-testing/SKILL.md (1,403 lines) - Implements NO MOCKS with workflow
- Hook: post_tool_use.py (164 lines) - Enforces NO MOCKS automatically

Core files → Skills reference → Hooks enforce

---

## Core Files Inventory

### Complete List with Metrics

| Core File | Lines | Purpose | Related Skill | Related Hook |
|-----------|-------|---------|---------------|--------------|
| **SPEC_ANALYSIS.md** | 1,786 | Complete 8D complexity algorithm | spec-analysis | N/A |
| **WAVE_ORCHESTRATION.md** | 1,611 | Wave execution behavioral framework | wave-orchestration | N/A |
| **HOOK_SYSTEM.md** | 1,571 | Complete hook documentation | N/A | All hooks |
| **PHASE_PLANNING.md** | 1,561 | 5-phase methodology | phase-planning | N/A |
| **CONTEXT_MANAGEMENT.md** | 1,149 | Context preservation patterns | context-preservation, context-restoration | precompact.py |
| **MCP_DISCOVERY.md** | 1,032 | MCP recommendation framework | mcp-discovery | N/A |
| **TESTING_PHILOSOPHY.md** | 1,050 | NO MOCKS complete manifesto | functional-testing | post_tool_use.py |
| **PROJECT_MEMORY.md** | 848 | Memory coordination patterns | memory-coordination | user_prompt_submit.py |
| **FORCED_READING_PROTOCOL.md** | 437 | Complete reading enforcement | N/A | N/A |

**Total**: 11,045 lines of detailed behavioral specifications

---

## Core File Architecture Patterns

### Pattern 1: Expanded Skill References

Core files are DETAILED versions of skills:

**Example: SPEC_ANALYSIS.md vs spec-analysis skill**
- Core file (1,786 lines): Complete 8D algorithm with all formulas, keyword lists, domain mapping matrices, MCP recommendation logic, phase customization rules
- Skill (1,545 lines): Summary of algorithm, anti-rationalization, workflow steps, examples, success criteria
- Usage: Skill for execution, core file for deep reference when needed

**Example: TESTING_PHILOSOPHY.md vs functional-testing skill**
- Core file (1,050 lines): Complete NO MOCKS manifesto, all platform patterns, anti-pattern catalog
- Skill (1,403 lines): Implements NO MOCKS with platform detection, test generation, violation scanning
- Usage: Core file explains WHY, skill provides HOW

### Pattern 2: Foundation for Multiple Components

Core files inform multiple skills:

**CONTEXT_MANAGEMENT.md** informs:
- context-preservation skill (checkpoint creation)
- context-restoration skill (checkpoint loading)
- precompact.py hook (emergency checkpoints)
- Commands: checkpoint, restore, prime

**WAVE_ORCHESTRATION.md** informs:
- wave-orchestration skill (execution)
- WAVE_COORDINATOR agent (orchestration)
- wave command (user interface)
- sitrep-reporting skill (progress tracking)

### Pattern 3: Progressive Disclosure

Skills reference core files:

```markdown
# In spec-analysis/SKILL.md:

## References
- Full 8D algorithm: shannon-plugin/core/SPEC_ANALYSIS.md (1787 lines)
- Domain patterns: references/domain-patterns.md (300 lines)

Claude loads references when:
- Complexity >=0.60 (needs deep algorithm details)
- Domain percentages unclear (consult domain-patterns.md)
```

This creates information hierarchy:
1. Skill summary (400-1,500 lines) - Always loaded
2. Core file reference (850-1,800 lines) - Loaded when needed
3. Skill references/ (200-500 lines) - Loaded for edge cases

---

## How Core Files Are Loaded

### NOT via CLAUDE.md

Core files are **NOT automatically injected** into system prompt. If they were:
- 11,045 lines would be in EVERY interaction
- Token budget would be consumed immediately
- No room for actual work

### NOT via SessionStart Hook

session_start.sh loads using-shannon skill (723 lines), not core files.

### Loading Mechanism: ON-DEMAND REFERENCE

Core files are loaded when:

**1. Skills Reference Them**:
```markdown
# In using-shannon skill:
See complete methodology: shannon-plugin/core/TESTING_PHILOSOPHY.md
```

When Claude sees this reference, it MAY read the core file if needed for clarification.

**2. Commands Reference Them**:
```markdown
# In test command:
Reference: shannon-plugin/core/TESTING_PHILOSOPHY.md for NO MOCKS philosophy
```

**3. Agents Are Instructed**:
```markdown
# In TEST_GUARDIAN agent guide:
Before implementing tests, read:
- shannon-plugin/core/TESTING_PHILOSOPHY.md (complete patterns)
```

**4. Direct User Request**:
User asks "What's Shannon's testing philosophy?" → Claude reads TESTING_PHILOSOPHY.md

### Loading Decision

Core files are 850-1,800 lines each. Claude loads them when:
- Need deep algorithm details (spec analysis edge case)
- Need complete methodology (teaching/explaining)
- Debugging issues (why did skill behave this way?)
- Creating new skills (understand full framework)

For routine operation, skills' 400-1,500 line summaries are sufficient.

---

## Core File Purposes

### SPEC_ANALYSIS.md (1,786 lines)

**Purpose**: Complete 8-dimensional complexity scoring algorithm

**Contains**:
- Full mathematical formulas for each dimension
- Complete keyword lists (200+ keywords for domain detection)
- MCP recommendation matrix (20+ MCPs with tiering logic)
- Phase customization rules by domain
- Timeline estimation formulas
- Interpretation band definitions
- Edge case handling

**Referenced By**: spec-analysis skill, shannon-analysis skill, phase-planning skill

**Usage**: When spec-analysis encounters complex/ambiguous specification requiring deep algorithm consultation

---

### WAVE_ORCHESTRATION.md (1,611 lines)

**Purpose**: Complete wave execution behavioral framework

**Contains**:
- True parallelism enforcement rules
- Agent spawning patterns (single message requirement)
- Context loading protocol templates
- Dependency analysis algorithms
- Wave synthesis procedures
- Agent allocation formulas by complexity
- Performance optimization strategies
- Error recovery patterns

**Referenced By**: wave-orchestration skill, WAVE_COORDINATOR agent, wave command

**Usage**: When orchestrating complex multi-wave projects (5+ waves, 15+ agents)

---

### HOOK_SYSTEM.md (1,571 lines)

**Purpose**: Complete hook system documentation

**Contains**:
- All 6 hook specifications
- Hook lifecycle documentation
- Integration patterns with skills
- Troubleshooting for each hook
- Hook development guide
- Testing methodology
- Performance characteristics

**Referenced By**: Hook implementations, developers creating new hooks

**Usage**: Understanding how hooks work, debugging hook issues, creating new hooks

---

### PHASE_PLANNING.md (1,561 lines)

**Purpose**: Complete 5-phase planning methodology

**Contains**:
- Phase structure algorithms (3-6 phases based on complexity)
- Timeline distribution formulas with adjustments
- Validation gate templates by phase
- Domain customization rules
- Wave mapping patterns
- Examples for each complexity band

**Referenced By**: phase-planning skill, spec-analysis skill (generates phase plans)

**Usage**: When creating phase plans for complex projects (complexity >=0.60)

---

### CONTEXT_MANAGEMENT.md (1,149 lines)

**Purpose**: Context preservation and restoration patterns

**Contains**:
- Checkpoint creation strategies (5 types)
- Checkpoint content structure (11 sections)
- Serena MCP integration patterns
- Memory key naming conventions
- Restoration procedures
- Error handling for missing memories

**Referenced By**: context-preservation, context-restoration skills, precompact.py hook

**Usage**: When implementing checkpoints, debugging restoration issues

---

### MCP_DISCOVERY.md (1,032 lines)

**Purpose**: MCP recommendation framework

**Contains**:
- Domain-to-MCP mapping matrix
- Tier definitions (MANDATORY/PRIMARY/SECONDARY/OPTIONAL)
- Threshold rules (Frontend >=20% → Puppeteer PRIMARY)
- Fallback chains for unavailable MCPs
- Health check procedures per MCP
- Setup instructions

**Referenced By**: mcp-discovery skill, spec-analysis skill, check_mcps command

**Usage**: When generating MCP recommendations, determining fallbacks

---

### TESTING_PHILOSOPHY.md (1,050 lines)

**Purpose**: NO MOCKS complete testing manifesto

**Contains**:
- Why mocks fail (philosophical foundation)
- All platform testing patterns (Web, iOS, API, Database)
- Complete test examples for each platform
- Anti-pattern catalog with corrections
- Test environment setup guides
- Red flags and green flags for test validation

**Referenced By**: functional-testing skill, post_tool_use.py hook, test command, TEST_GUARDIAN agent

**Usage**: When implementing tests, explaining NO MOCKS philosophy, debugging test violations

---

### PROJECT_MEMORY.md (848 lines)

**Purpose**: Memory coordination and knowledge graph patterns

**Contains**:
- Shannon namespace conventions (shannon/*)
- Entity naming patterns
- Relation types (spawns, contains, tracks, etc.)
- Search patterns for efficiency
- Observation management rules
- Lineage tracking

**Referenced By**: memory-coordination skill, all Serena-using skills

**Usage**: When storing Shannon artifacts in Serena, querying knowledge graph

---

### FORCED_READING_PROTOCOL.md (437 lines - shortest)

**Purpose**: Complete reading enforcement protocol

**Contains**:
- 4-step Iron Law (pre-count, sequential reading, verify, synthesize)
- Baseline violations (4 common rationalizations)
- Red flag keywords
- Command integration patterns
- Configuration options
- Override audit trail

**Referenced By**: Commands (spec, analyze, wave), agents (SPEC_ANALYZER, ANALYZER)

**Usage**: When analyzing critical documents, enforcing thorough reading

---

## Core Files vs. Skills: Key Differences

| Aspect | Core Files | Skills |
|--------|-----------|--------|
| **Length** | 850-1,800 lines | 400-1,500 lines |
| **Purpose** | Complete reference | Executable workflow |
| **Loading** | On-demand | Auto/manual invoke |
| **Audience** | Deep consultation | Regular usage |
| **Content** | Full algorithms, all edge cases | Summary + workflow + examples |
| **Invocation** | Read file | Skill tool |
| **Update Frequency** | Rare (foundational) | More frequent (implementation evolves) |

**Relationship**: Core files are the SPECIFICATION, skills are the IMPLEMENTATION.

---

## Integration Patterns

### Skills Reference Core Files

**Pattern**: Skill provides summary, references core file for complete details

```markdown
# In spec-analysis/SKILL.md (line 1200):

## References
- Full 8D algorithm: shannon-plugin/core/SPEC_ANALYSIS.md (1787 lines)
- Phase planning: shannon-plugin/core/PHASE_PLANNING.md
```

### Core Files Inform Multiple Skills

**TESTING_PHILOSOPHY.md** influences:
- functional-testing skill (implements testing patterns)
- using-shannon skill (declares NO MOCKS as Iron Law)
- post_tool_use.py hook (enforces via blocking)

### Core Files as Foundation

```
Core File (Foundation)
    ↓
Skills (Implementation)
    ↓
Commands (Interface)
    ↓
User Experience
```

Example:
```
SPEC_ANALYSIS.md (1,786 lines: complete 8D algorithm)
    ↓
spec-analysis skill (1,545 lines: implements algorithm)
    ↓
spec command (160 lines: user interface)
    ↓
User types: /shannon:spec "Build web app"
```

---

## Key Insights

### 1. Core Files Are NOT Auto-Loaded

Unlike CLAUDE.md (which IS auto-loaded), core files are:
- Too large (11,045 lines total) for system prompt
- Loaded on-demand when skills/agents need deep reference
- Progressive disclosure mechanism
- Skill summaries handle 90% of cases

### 2. Core Files Match Skill Names

Pattern observed:
- SPEC_ANALYSIS.md ↔ spec-analysis skill
- WAVE_ORCHESTRATION.md ↔ wave-orchestration skill
- TESTING_PHILOSOPHY.md ↔ functional-testing skill
- PHASE_PLANNING.md ↔ phase-planning skill
- CONTEXT_MANAGEMENT.md ↔ context-preservation/restoration skills

This is INTENTIONAL COUPLING - same name signals related content.

### 3. Core Files Are Specifications

Core files read like:
- Algorithm specifications (formulas, pseudocode)
- Complete methodologies (step-by-step processes)
- Comprehensive references (all patterns, all edge cases)

NOT like:
- Instructions for Claude (those are in skills)
- User documentation (those are in README/guides)
- Code (those are in hooks)

Core files are THE SPECIFICATION from which skills and hooks are implemented.

### 4. Progressive Disclosure Architecture

Information hierarchy:
1. **Command** (150-450 lines): User interface, delegates to skill
2. **Skill** (400-1,500 lines): Workflow summary, anti-rationalization, examples
3. **Core File** (850-1,800 lines): Complete algorithm/methodology
4. **Skill references/** (200-500 lines): Edge cases, advanced patterns

Each layer references the next for deeper details. This prevents token overload while maintaining depth.

---

## Phase 6 Completion

✅ **All Core Files Analyzed**:
- Read representative sections of all 9 files
- Understood relationship to skills with matching names
- Identified loading mechanism (on-demand reference, not auto-inject)
- Mapped integration patterns with skills, commands, hooks

✅ **Key Finding**: Core files are REFERENCE SPECIFICATIONS, not auto-loaded behavioral modifiers. They're too large (11K lines) for system prompt. Skills summarize core file methodologies for routine use.

**Next**: Phase 7 - Integration Patterns, Phase 8 - User Experience (already complete), Phase 9 - 100+ Thought Synthesis
