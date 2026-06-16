# Shannon Framework v4: Skill-First Architecture Enhancement

**Enhancement Type**: Architectural Refinement
**Focus**: Commands as Skill Activators (Not Prose Containers)
**Status**: In Progress

---

## Problem Statement

Current v4 implementation has **mixed approach**:
- ✅ Created 5 Priority 1 skills
- ❌ Commands still contain prose instructions (not fully skill-based)
- ❌ Missing skills for core Shannon functionality
- ❌ Commands don't primarily activate skills

**Example Current State**:
```markdown
# /sh_wave command (CURRENT - WRONG)
---
frontmatter
---

## Execution Flow

### Step 1: Load Context
[500 lines of prose instructions]

### Step 2: Validate Dependencies
[300 lines of prose]

### Step 3: Execute Wave
[400 lines of prose]
```

**Desired State**:
```markdown
# /sh_wave command (DESIRED - SKILL-FIRST)
---
frontmatter
linked_skills:
  - shannon-wave-orchestrator
---

## Purpose
Executes wave-based parallel task orchestration.

## Activation
This command activates the `shannon-wave-orchestrator` skill.

📚 See: skills/shannon-wave-orchestrator/SKILL.md for full execution logic
```

---

## Command-to-Skill Mapping

### Core Shannon Commands (13 total)

| Command | Current Skill | Status | New Skill Needed |
|---------|--------------|--------|------------------|
| **/sh_spec** | shannon-spec-analyzer | ✅ Created | None |
| **/sh_plan** | None | ❌ Prose-based | shannon-phase-planner |
| **/sh_wave** | None | ❌ Prose-based | shannon-wave-orchestrator |
| **/sh_checkpoint** | None | ❌ Prose-based | shannon-checkpoint-manager |
| **/sh_restore** | None | ❌ Prose-based | shannon-context-restorer |
| **/sh_memory** | None | ❌ Prose-based | shannon-serena-manager |
| **/sh_north_star** | None | ❌ Prose-based | shannon-goal-tracker |
| **/sh_status** | None | ❌ Prose-based | shannon-status-reporter |
| **/sh_check_mcps** | None | ❌ Prose-based | shannon-mcp-validator |
| **/sh_analyze** | None | ❌ Prose-based | shannon-code-analyzer |
| **/sh_quickstart** | None | ❌ Prose-based | shannon-quickstart-guide |
| **/sh_help** | None | ❌ Prose-based | shannon-help-system |
| **/sh_workflow** | None | ❌ Prose-based | shannon-workflow-manager |

**Summary**:
- ✅ 1/13 commands skill-based (8%)
- ❌ 12/13 commands prose-based (92%)
- **Need**: 12 additional skills

---

## Priority Skills to Create

### Priority 1A (Core Shannon - URGENT)

#### 1. shannon-wave-orchestrator
**Purpose**: Parallel wave execution with dependency management
**Capabilities**:
- Dependency analysis and wave grouping
- Parallel agent spawning (ONE message multi-Task)
- Context injection automation
- Wave validation and result collection
- Serena state management

**Replaces**: 1,612 lines of prose in WAVE_ORCHESTRATION.md

#### 2. shannon-checkpoint-manager
**Purpose**: Context preservation and checkpoint creation
**Capabilities**:
- State extraction (todos, wave, decisions, files)
- Serena MCP persistence
- Checkpoint labeling and metadata
- Restore point creation

**Replaces**: 300+ lines of prose in /sh_checkpoint

#### 3. shannon-phase-planner
**Purpose**: 5-phase implementation planning
**Capabilities**:
- Effort distribution (20-15-45-15-5%)
- Phase dependency mapping
- Validation gate creation
- Timeline estimation
- Deliverable specification

**Replaces**: 400+ lines of prose in /sh_plan

#### 4. shannon-serena-manager
**Purpose**: Serena MCP memory management
**Capabilities**:
- Memory CRUD operations
- Memory listing and search
- Knowledge graph navigation
- Context queries

**Replaces**: 200+ lines of prose in /sh_memory

### Priority 1B (Supporting)

#### 5. shannon-context-restorer
**Purpose**: Session context restoration
**Capabilities**:
- Checkpoint loading from Serena
- State reconstruction
- Session re-initialization
- Context validation

**Replaces**: 200+ lines of prose in /sh_restore

#### 6. shannon-goal-tracker
**Purpose**: North Star goal management
**Capabilities**:
- Goal setting and persistence
- Goal alignment checking
- Progress tracking
- Goal reminder injection

**Replaces**: 150+ lines of prose in /sh_north_star

#### 7. shannon-mcp-validator
**Purpose**: MCP server availability checking
**Capabilities**:
- MCP connection testing
- Tier validation (Tier 1/2/3)
- Graceful degradation suggestions
- MCP installation guidance

**Replaces**: 100+ lines of prose in /sh_check_mcps

---

## Skill-First Architecture

### Command Structure (NEW)

```markdown
---
name: command-name
command: /command-name
description: "Brief description"
category: command
linked_skills:
  - primary-skill-name
  - optional-secondary-skill
mcp_servers: [required-mcps]
auto_activate: true
progressive_disclosure:
  tier: 1
  full_content: resources/FULL.md
  estimated_tokens: 100  # Much smaller!
---

# /command-name

> **Skill-Based**: This command activates the `primary-skill-name` skill

## Purpose
[1-2 sentences]

## Usage
```bash
/command-name [args]
```

## Skill Activation
This command activates: `primary-skill-name`

**Skill provides**:
- [Capability 1]
- [Capability 2]
- [Capability 3]

## Quick Reference
📚 **Full Logic**: See [skills/primary-skill-name/SKILL.md](../skills/primary-skill-name/SKILL.md)
📚 **Examples**: See [resources/EXAMPLES.md](./resources/EXAMPLES.md)

---
**Shannon V4** - Skill-First Architecture 🚀
```

**Token Count**: ~100 tokens (vs 500-1000+ in current prose-based)

### Skill Structure (Detailed)

```markdown
---
name: skill-name
display_name: "Skill Display Name"
description: "What this skill does"
category: core|analysis|orchestration|management
version: "4.0.0"
priority: 1
auto_activate: true
activation_triggers:
  - command-name
  - context-condition
mcp_servers:
  required: [serena]
  recommended: [sequential, context7]
allowed_tools: [Tool1, Tool2, serena_write_memory]
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
  full_content: resources/FULL_SKILL.md
input:
  param1: {type, description}
output:
  result1: {type, description}
---

# Skill Name

> **Core Shannon Skill**: [What it does]

## Purpose
[Detailed purpose]

## Capabilities
- [Capability 1 with details]
- [Capability 2 with details]
- [Capability 3 with details]

## Activation
[When this skill activates]

## Execution Algorithm

### Step 1: [Action]
```javascript
// Pseudo-code for algorithm
const result = performAction();
```

### Step 2: [Action]
[Detailed steps]

### Step 3: [Action]
[Detailed steps]

## Integration
[How this skill works with other skills]

## Examples
[Real-world examples]

## Patterns
[Common patterns and best practices]

---
**Shannon V4** - [Skill Name] 🚀
```

---

## Skill Composition Patterns

### Pattern 1: Command → Single Skill

```
/sh_checkpoint
  ↓
shannon-checkpoint-manager
  ↓
Creates checkpoint in Serena
```

**Simple 1:1 mapping**

### Pattern 2: Command → Skill Chain

```
/sh_spec
  ↓
shannon-spec-analyzer
  ↓ (triggers)
shannon-skill-generator
  ↓ (generates)
shannon-[project-specific-skills]
```

**Skill activates other skills**

### Pattern 3: Command → Multiple Skills (Parallel)

```
/sh_wave 1
  ↓
shannon-wave-orchestrator
  ├→ shannon-context-loader (parallel)
  ├→ shannon-dependency-validator (parallel)
  └→ shannon-agent-spawner (parallel)
```

**Skill orchestrates multiple skills**

### Pattern 4: Skill → Agent → Skill

```
/sh_plan
  ↓
shannon-phase-planner
  ↓ (may spawn)
PHASE_ARCHITECT agent
  ↓ (uses)
shannon-spec-analyzer (for context)
```

**Skills and agents compose**

---

## Token Efficiency Gains

### Current v4 (Prose in Commands)

```
Command file: /sh_wave.md
  Frontmatter: ~50 tokens
  Purpose: ~50 tokens
  Execution steps: ~800 tokens  ⬅️ PROBLEM
  Examples: ~200 tokens
  Total: ~1,100 tokens

LOADED UPFRONT (even if never used)
```

### Enhanced v4 (Skill-First)

```
Command file: /sh_wave.md
  Frontmatter: ~50 tokens
  Purpose: ~30 tokens
  Skill reference: ~20 tokens  ⬅️ SOLUTION
  Total: ~100 tokens

Skill file: shannon-wave-orchestrator/SKILL.md
  Metadata: ~150 tokens (loaded)
  Full algorithm: ~800 tokens (resources/FULL_SKILL.md)

LOADED ONLY WHEN SKILL ACTIVATES
```

**Additional Savings**:
- Command: 1,100 → 100 tokens (91% reduction)
- Skill metadata: Loaded on-demand
- **Total for 13 commands**: ~13,000 → ~1,300 tokens (90% additional reduction)

---

## Implementation Plan

### Phase 1: Create Core Skills (Priority 1A)
1. shannon-wave-orchestrator ⬅️ START HERE
2. shannon-checkpoint-manager
3. shannon-phase-planner
4. shannon-serena-manager

### Phase 2: Create Supporting Skills (Priority 1B)
5. shannon-context-restorer
6. shannon-goal-tracker
7. shannon-mcp-validator

### Phase 3: Refactor Commands
- Update all 13 Shannon commands to skill-first format
- Move prose to skill resources
- Add linked_skills frontmatter
- Reduce command files to ~100 tokens each

### Phase 4: Update Documentation
- Skill composition patterns guide
- Command → Skill mapping reference
- Skill development guide
- Examples and use cases

---

## Success Criteria

### Token Efficiency
- [x] Commands reduced to ~100 tokens each
- [ ] Additional 90% reduction in command overhead
- [ ] Total v4 base: ~5K tokens (from current ~24K)

### Architecture
- [ ] All commands link to skills
- [ ] Skills contain all logic (not commands)
- [ ] Skills can be composed and orchestrated
- [ ] Clear skill activation patterns

### Developer Experience
- [ ] Commands are simple and obvious
- [ ] Skills are discoverable
- [ ] Skill reuse across commands
- [ ] Clear separation of concerns

---

## Next Steps

1. **Create shannon-wave-orchestrator** (highest priority)
2. Create remaining Priority 1A skills
3. Refactor /sh_wave to skill-first format
4. Test skill activation
5. Apply pattern to all 13 commands
6. Update documentation

---

**Shannon V4 Enhancement** - Skill-First Architecture 🎯
