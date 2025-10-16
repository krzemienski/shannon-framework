---
name: sc:brainstorm
command: /sc:brainstorm
description: Collaborative discovery with structured requirement exploration and Serena idea tracking
category: command
base: SuperClaude /brainstorm command
shannon_enhancements: true
version: 3.0.0
---

# /sc:brainstorm - Enhanced Collaborative Discovery

> **Shannon V3 Enhancement**: Structured requirement discovery with persistent idea tracking via Serena MCP, multi-phase exploration framework, and systematic validation gates.

## Purpose

Transform vague concepts into actionable requirements through **Socratic dialogue**, **systematic exploration**, and **structured documentation**. Shannon V3 enhances SuperClaude's brainstorming with formal discovery frameworks, persistent memory, and quality validation.

**SuperClaude Foundation**: Collaborative discovery mindset for interactive requirements exploration
**Shannon Enhancement**: 8-phase structured discovery, Serena-powered idea tracking, validation gates, and cross-session continuity

---

## Command Structure

```bash
/sc:brainstorm [topic] [flags]
```

### Arguments

**`[topic]`** (optional)
- Initial concept or problem statement
- Examples: "web app", "authentication system", "user dashboard"
- Can be vague - brainstorming clarifies scope

### Flags

**Discovery Control**:
- `--quick` - Fast 3-phase discovery (60% time)
- `--standard` - Full 8-phase discovery (default)
- `--deep` - Extended exploration with validation (150% time)

**Memory Management**:
- `--continue` - Resume previous brainstorming session
- `--new` - Start fresh (clear previous session)
- `--save-ideas` - Store all generated ideas in Serena

**Integration**:
- `--spec` - Generate `/sh:spec` compatible specification after discovery
- `--estimate` - Include effort estimation in requirements
- `--phase-plan` - Create phase-based implementation plan

**Output**:
- `--brief` - Concise requirement summary only
- `--detailed` - Full discovery documentation (default)
- `--interactive` - Step-by-step confirmation mode

---

## Shannon V3 Enhancements

### 1. Structured Discovery Framework

**8-Phase Discovery Process**:

```yaml
phase_1_context:
  name: "Problem Understanding"
  duration: 10%
  objective: "Define problem space and success criteria"

phase_2_stakeholders:
  name: "Stakeholder Analysis"
  duration: 10%
  objective: "Identify users, needs, constraints"

phase_3_requirements:
  name: "Requirement Elicitation"
  duration: 20%
  objective: "Extract functional and non-functional requirements"

phase_4_constraints:
  name: "Constraint Mapping"
  duration: 10%
  objective: "Technical, business, resource constraints"

phase_5_validation:
  name: "Requirement Validation"
  duration: 15%
  objective: "Verify completeness and feasibility"

phase_6_prioritization:
  name: "Priority Assignment"
  duration: 15%
  objective: "Must-have vs nice-to-have classification"

phase_7_documentation:
  name: "Formal Documentation"
  duration: 15%
  objective: "Create structured requirements brief"

phase_8_handoff:
  name: "Implementation Planning"
  duration: 5%
  objective: "Prepare for /sh:spec or /sc:implement"
```

### 2. Serena MCP Integration

**Persistent Idea Tracking**:

```yaml
memory_structure:
  session_context: "brainstorm_[timestamp]_[topic]"

  idea_storage:
    - brainstorm_ideas_[topic]: "All generated ideas"
    - brainstorm_requirements_[topic]: "Validated requirements"
    - brainstorm_constraints_[topic]: "Identified limitations"
    - brainstorm_questions_[topic]: "Unanswered questions"

  cross_session:
    - Resume previous brainstorming sessions
    - Track idea evolution over time
    - Build project knowledge base
```

**Memory Operations**:
- `write_memory()`: Store discoveries after each phase
- `read_memory()`: Resume previous sessions with `--continue`
- `list_memories()`: View all brainstorming sessions for project
- `search_nodes()`: Find related ideas across sessions

### 3. Validation Gates

**Quality Checkpoints**:

```yaml
gate_1_clarity:
  checkpoint: "Phase 1 Complete"
  validates: "Problem statement is clear and actionable"

gate_2_completeness:
  checkpoint: "Phase 3 Complete"
  validates: "All requirement categories addressed"

gate_3_feasibility:
  checkpoint: "Phase 5 Complete"
  validates: "Requirements are achievable within constraints"

gate_4_priority:
  checkpoint: "Phase 6 Complete"
  validates: "Clear MVP scope and roadmap"
```

### 4. Sub-Agent Coordination

**MENTOR Agent**: Primary facilitator for discovery dialogue
**SPEC_ANALYZER Agent**: Technical feasibility assessment
**PHASE_ARCHITECT Agent**: Implementation planning (Phase 8)

---

## Execution Flow

### Standard Discovery Flow

```
1. Session Initialization
   ├─ Check for existing brainstorming sessions (--continue)
   ├─ Load previous context from Serena MCP
   └─ Create new session memory structure

2. Phase 1: Problem Understanding (MENTOR Agent)
   ├─ Ask: "What problem are you solving?"
   ├─ Ask: "Who experiences this problem?"
   ├─ Ask: "What does success look like?"
   ├─ Document problem statement
   └─ GATE 1: Clarity validation

3. Phase 2: Stakeholder Analysis (MENTOR Agent)
   ├─ Identify primary users
   ├─ Identify secondary stakeholders
   ├─ Map user needs and pain points
   └─ Store stakeholder profiles in Serena

4. Phase 3: Requirement Elicitation (MENTOR + SPEC_ANALYZER)
   ├─ Functional requirements discovery
   ├─ Non-functional requirements (performance, security, etc.)
   ├─ Integration requirements
   ├─ Data requirements
   └─ GATE 2: Completeness validation

5. Phase 4: Constraint Mapping (SPEC_ANALYZER Agent)
   ├─ Technical constraints (stack, infrastructure)
   ├─ Business constraints (budget, timeline)
   ├─ Resource constraints (team, skills)
   └─ Regulatory/compliance constraints

6. Phase 5: Requirement Validation (MENTOR + SPEC_ANALYZER)
   ├─ Feasibility assessment
   ├─ Identify conflicts and dependencies
   ├─ Resolve ambiguities
   └─ GATE 3: Feasibility validation

7. Phase 6: Priority Assignment (MENTOR Agent)
   ├─ Must-have (MVP scope)
   ├─ Should-have (Phase 2)
   ├─ Nice-to-have (Future)
   └─ GATE 4: Priority validation

8. Phase 7: Formal Documentation (SCRIBE Agent)
   ├─ Create requirements brief
   ├─ Generate user stories (optional)
   ├─ Document assumptions and risks
   └─ Store final requirements in Serena

9. Phase 8: Implementation Planning (PHASE_ARCHITECT Agent)
   ├─ Suggest implementation approach
   ├─ Estimate complexity (high-level)
   ├─ Recommend next command (/sh:spec or /sc:implement)
   └─ Store handoff context in Serena
```

### Quick Discovery Flow (--quick)

```
Compressed 3-phase approach for rapid exploration:

Phase 1: Problem + Stakeholders (20% time)
Phase 2: Requirements + Constraints (50% time)
Phase 3: Documentation + Handoff (30% time)

Validation gates reduced to 2 checkpoints
Memory storage still active for continuity
```

### Deep Discovery Flow (--deep)

```
Extended exploration with additional validation:

+ Phase 0: Pre-Discovery (research existing solutions)
+ Additional validation checkpoints after each phase
+ Competitive analysis and market research
+ Risk assessment and mitigation planning
+ Multiple iteration cycles with user feedback
```

---

## Output Format

### Standard Output (--detailed)

```markdown
# Brainstorming Session: [Topic]
**Session ID**: brainstorm_[timestamp]_[topic]
**Mode**: Standard Discovery (8 phases)
**Duration**: [Estimated time]

---

## 🎯 Problem Statement
[Clear articulation of problem being solved]

**Success Criteria**:
- [Measurable outcome 1]
- [Measurable outcome 2]

**Validation**: Gate 1 PASSED ✓

---

## 👥 Stakeholders
**Primary Users**: [User personas]
**Secondary Stakeholders**: [Additional stakeholders]

**Key Needs**:
- [Need 1]
- [Need 2]

---

## 📋 Requirements

### Functional Requirements
**FR-1**: [Requirement description]
- Priority: Must-have
- Complexity: Medium
- Dependencies: None

**FR-2**: [Requirement description]
- Priority: Should-have
- Complexity: High
- Dependencies: FR-1

### Non-Functional Requirements
**NFR-1**: [Performance requirement]
**NFR-2**: [Security requirement]

**Validation**: Gate 2 PASSED ✓

---

## ⚠️ Constraints

**Technical**:
- Stack: [Technologies]
- Infrastructure: [Constraints]

**Business**:
- Budget: [Limitation]
- Timeline: [Deadline]

**Resource**:
- Team size: [Number]
- Skills: [Expertise gaps]

---

## ✅ Validated Requirements
[List of requirements that passed feasibility assessment]

**Validation**: Gate 3 PASSED ✓

---

## 🎯 Priority Breakdown

**Must-Have (MVP Scope)**:
- [Requirement 1]
- [Requirement 2]

**Should-Have (Phase 2)**:
- [Requirement 3]

**Nice-to-Have (Future)**:
- [Requirement 4]

**Validation**: Gate 4 PASSED ✓

---

## 📝 Requirements Brief

[Formal structured documentation suitable for handoff]

**Assumptions**:
- [Assumption 1]

**Risks**:
- [Risk 1] (Mitigation: [Strategy])

**Open Questions**:
- [Question 1]

---

## 🚀 Next Steps

**Recommended Command**: `/sh:spec @requirements_brief.md`

**Implementation Approach**: [High-level strategy]

**Estimated Complexity**:
- Time: [Range]
- Risk: [Level]

**Serena Memory**:
- ✓ Requirements stored: `brainstorm_requirements_[topic]`
- ✓ Ideas stored: `brainstorm_ideas_[topic]`
- ✓ Session context saved for resumption
```

### Brief Output (--brief)

```markdown
# Requirements Brief: [Topic]

## Problem
[One paragraph problem statement]

## Requirements (MVP)
1. [Must-have requirement 1]
2. [Must-have requirement 2]

## Constraints
- [Key constraint 1]
- [Key constraint 2]

## Next Action
`/sh:spec @requirements_brief.md`
```

---

## Integration Patterns

### Pattern 1: Brainstorm → Spec → Task

```bash
# Step 1: Discover requirements
/sc:brainstorm "user authentication system" --spec

# Step 2: Generate detailed specification
/sh:spec @brainstorm_requirements.md

# Step 3: Create implementation plan
/sc:task create @specification.md
```

### Pattern 2: Iterative Refinement

```bash
# Session 1: Initial discovery
/sc:brainstorm "e-commerce platform" --save-ideas

# Session 2: Continue refinement (later)
/sc:brainstorm --continue --deep

# Session 3: Finalize and handoff
/sc:brainstorm --continue --spec
```

### Pattern 3: Multi-Stakeholder Discovery

```bash
# Round 1: Technical stakeholders
/sc:brainstorm "API integration" --focus technical

# Round 2: Business stakeholders
/sc:brainstorm --continue --focus business

# Round 3: Synthesis
/sc:brainstorm --continue --detailed
```

---

## Examples

### Example 1: Vague Concept → Clear Requirements

**Input**:
```bash
/sc:brainstorm "I want to build something for my team"
```

**Discovery Process**:
```
MENTOR: 🤔 Let's explore this together!

Phase 1: Problem Understanding
Q: What specific problem is your team facing?
→ "Communication is scattered across multiple tools"

Q: What does success look like for your team?
→ "All communication in one place, easy to search"

Q: Who on the team would use this most?
→ "Developers and project managers"

✓ Problem Statement: Build unified communication platform for development teams

Phase 2: Stakeholder Analysis
...
[continues through all phases]
```

**Output**: Detailed requirements brief with:
- Problem: Unified team communication platform
- 12 functional requirements (MVP: 5)
- 4 technical constraints
- Priority roadmap
- Next action: `/sh:spec @team_communication_requirements.md`

### Example 2: Quick Discovery

**Input**:
```bash
/sc:brainstorm "blog with comments" --quick --brief
```

**Output** (compressed):
```markdown
# Requirements Brief: Blog with Comments

## Problem
Create blog platform supporting articles and reader comments

## Requirements (MVP)
1. Article CRUD operations
2. Comment submission on articles
3. User authentication (authors only)
4. Basic content moderation

## Constraints
- Timeline: 2 weeks
- Single developer
- Must use existing React stack

## Next Action
`/sc:implement "blog with comment system" @requirements_brief.md`
```

### Example 3: Continuation Session

**Session 1**:
```bash
/sc:brainstorm "inventory management" --save-ideas
# [Initial discovery, stored in Serena]
```

**Session 2 (next day)**:
```bash
/sc:brainstorm --continue

# Shannon automatically:
# 1. Loads previous session from Serena
# 2. Presents summary of progress
# 3. Asks where to continue
```

**Output**:
```
✓ Loaded session: brainstorm_20250929_inventory
✓ Progress: Phases 1-4 complete (50%)
✓ Next: Phase 5 - Requirement Validation

Continue from Phase 5? [yes/no]
```

---

## Tool Orchestration

### Primary Tools

**Sequential MCP** (Reasoning Engine)
- Multi-step discovery logic
- Question generation and sequencing
- Validation gate assessment

**Serena MCP** (Memory Management)
- `write_memory()` - Store discoveries after each phase
- `read_memory()` - Load previous sessions
- `list_memories()` - Show all brainstorming sessions
- `search_nodes()` - Find related ideas

**Write Tool** (Documentation)
- Create requirements briefs
- Generate user stories
- Document assumptions and risks

### Tool Coordination Pattern

```yaml
phase_1_3_discovery:
  primary: Sequential MCP (socratic questioning)
  secondary: Write (document responses)
  memory: Serena (store discoveries)

phase_4_5_validation:
  primary: Sequential MCP (feasibility analysis)
  secondary: Serena (retrieve constraints)
  coordination: SPEC_ANALYZER agent

phase_6_8_planning:
  primary: Serena (store final requirements)
  secondary: Write (create formal documentation)
  coordination: PHASE_ARCHITECT agent
```

---

## Quality Standards

### Discovery Completeness

**Must Address**:
- Problem statement (clear, measurable)
- Stakeholder needs (primary + secondary)
- Functional requirements (categorized)
- Non-functional requirements (explicit)
- Technical constraints (realistic)
- Business constraints (acknowledged)
- Priority classification (MVP identified)

### Validation Gates

**Gate 1: Clarity** (Phase 1)
- ✓ Problem is specific and actionable
- ✓ Success criteria are measurable
- ✓ Stakeholders are identified

**Gate 2: Completeness** (Phase 3)
- ✓ All requirement categories covered
- ✓ No obvious gaps in functionality
- ✓ Non-functional requirements explicit

**Gate 3: Feasibility** (Phase 5)
- ✓ Requirements achievable within constraints
- ✓ No insurmountable technical barriers
- ✓ Conflicts and dependencies resolved

**Gate 4: Priority** (Phase 6)
- ✓ Clear MVP scope definition
- ✓ Realistic prioritization rationale
- ✓ Future roadmap outlined

### Documentation Quality

**Requirements Brief Must Include**:
- Problem statement (1-2 paragraphs)
- Stakeholder analysis (users, needs)
- Prioritized requirements list
- Constraint documentation
- Assumptions and risks
- Next action recommendation

---

## Performance Characteristics

### Standard Discovery
- **Duration**: 30-60 minutes (depends on complexity)
- **Phases**: 8 structured phases
- **Validation Gates**: 4 checkpoints
- **Memory Operations**: 8-12 writes to Serena
- **Output**: 500-1000 line requirements brief

### Quick Discovery (--quick)
- **Duration**: 15-30 minutes (60% reduction)
- **Phases**: 3 compressed phases
- **Validation Gates**: 2 checkpoints
- **Memory Operations**: 4-6 writes
- **Output**: 200-400 line brief

### Deep Discovery (--deep)
- **Duration**: 60-120 minutes (150% extension)
- **Phases**: 9-10 phases (with pre-discovery)
- **Validation Gates**: 8+ checkpoints
- **Memory Operations**: 15-20 writes
- **Output**: 1000-2000 line detailed specification

---

## Best Practices

### 1. Start Vague, Iterate to Clarity
```bash
# Good: Let brainstorming refine vague concepts
/sc:brainstorm "some kind of dashboard"

# Avoid: Over-constraining initial input
/sc:brainstorm "React dashboard with Redux, Material-UI, real-time WebSocket updates..."
```

### 2. Use Memory for Continuity
```bash
# Good: Resume and build on previous sessions
/sc:brainstorm --continue

# Avoid: Starting fresh each time
/sc:brainstorm "same topic" --new  # loses context
```

### 3. Validate Before Proceeding
```bash
# Good: Let gates ensure quality
/sc:brainstorm "project" --standard  # includes validation

# Avoid: Rushing to implementation
/sc:brainstorm "project" --quick --skip-validation  # risky
```

### 4. Choose Appropriate Depth
```bash
# Prototype/MVP: Quick discovery
/sc:brainstorm "prototype feature" --quick

# Production system: Standard discovery
/sc:brainstorm "production feature" --standard

# Critical/complex: Deep discovery
/sc:brainstorm "payment system" --deep
```

### 5. Integrate with Workflow
```bash
# Complete workflow chain
/sc:brainstorm "feature" --spec → /sh:spec → /sc:task create
```

---

## Comparison with SuperClaude

| Aspect | SuperClaude | Shannon V3 |
|--------|-------------|------------|
| **Discovery Structure** | Informal Socratic dialogue | Formal 8-phase framework |
| **Memory** | Session-only | Persistent via Serena MCP |
| **Validation** | Implicit | 4 explicit validation gates |
| **Continuity** | Limited | Full cross-session support |
| **Output** | Informal notes | Structured requirements brief |
| **Integration** | Manual handoff | Direct `/sh:spec` integration |
| **Sub-Agents** | MENTOR only | MENTOR + SPEC_ANALYZER + PHASE_ARCHITECT |
| **Depth Control** | Fixed | 3 modes (quick/standard/deep) |

---

## Related Commands

**Upstream**:
- None (brainstorming is typically entry point)

**Downstream**:
- `/sh:spec` - Generate detailed specification from requirements
- `/sc:implement` - Direct implementation from requirements
- `/sc:task` - Create task breakdown from requirements
- `/sc:estimate` - Estimate effort from requirements

**Complementary**:
- `/sc:analyze` - Analyze existing systems before brainstorming
- `/sc:explain` - Understand concepts during discovery
- `/sc:research` - Research technologies/approaches during constraints phase

---

## Troubleshooting

### Issue: Discovery feels too slow
**Solution**: Use `--quick` flag for rapid exploration
```bash
/sc:brainstorm "topic" --quick
```

### Issue: Lost context between sessions
**Solution**: Always use `--continue` to resume
```bash
/sc:brainstorm --continue
```

### Issue: Requirements too vague after brainstorming
**Solution**: Use `--deep` mode for thorough exploration
```bash
/sc:brainstorm "topic" --deep
```

### Issue: Can't find previous brainstorming sessions
**Solution**: List all sessions stored in Serena
```bash
# Use Serena MCP directly
list_memories()  # Shows all brainstorm_* memories
```

---

**Shannon V3 Philosophy**: Transform uncertainty into clarity through structured discovery, persistent memory, and systematic validation. Every project begins with understanding—brainstorming ensures we understand correctly before we build.