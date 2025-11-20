---
name: sh:plan
linked_skills:
  - shannon-phase-planner
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:plan
> **Skill-Based**: This command activates the `shannon-phase-planner` skill

## Description

Creates a comprehensive 5-phase implementation plan with wave-based task grouping following Shannon's methodology:
- **Discovery (20%)**: Requirements, research, context gathering
- **Architecture (15%)**: System design, technology decisions
- **Implementation (45%)**: Core development work
- **Testing (15%)**: Functional validation (NO MOCKS)
- **Deployment (5%)**: Release and monitoring

## Usage

```bash
# Create phase plan from existing spec analysis
/sh:plan

# Create phase plan with specific spec
/sh:plan --from-spec spec_analysis_20251104

# Create phase plan with constraints
/sh:plan --timeline "8 weeks" --team-size 3
```

## Prerequisites

- Spec analysis must exist (run `/sh:spec` first)
- North Star goal must be set (run `/sh:north_star` first)
- Serena MCP must be available

## Skill Activation

This command activates: **`shannon-phase-planner`**

📚 **Full planning logic**: `skills/shannon-phase-planner/SKILL.md`

The skill will:
1. Load spec analysis from Serena MCP
2. Load North Star goal
3. Analyze complexity for phase planning
4. Create 5-phase structure with validation gates
5. Group tasks into dependency waves
6. Estimate effort distribution (20-15-45-15-5%)
7. Identify risks and blockers
8. Save phase plan to Serena MCP
9. Generate planning report

## Output

The skill generates:
- Complete 5-phase plan with objectives
- Wave structure for each phase
- Validation gates with clear criteria
- Effort distribution breakdown
- Risk assessment
- Estimated timeline
- Critical path analysis

## Integration

**Command Flow**:
```
/sh:spec → shannon-spec-analyzer → Saves spec analysis
  ↓
/sh:plan → shannon-phase-planner → Loads spec, creates plan
  ↓
Phase plan saved to Serena MCP
  ↓
/sh:wave 1 → shannon-wave-orchestrator → Executes first wave
```

## Examples

### Example 1: Simple React Dashboard
```bash
$ /sh:spec "Build React dashboard with charts"
✅ Spec analysis complete (complexity: 0.35)

$ /sh:plan
✅ Phase plan created (8 waves, ~3 weeks)

Phase 1: Discovery (15% - adjusted for low complexity)
Phase 2: Architecture (10%)
Phase 3: Implementation (55%)
Phase 4: Testing (15%)
Phase 5: Deployment (5%)
```

### Example 2: Complex Full-Stack SaaS
```bash
$ /sh:spec "Build SaaS with Next.js, Express, PostgreSQL, AWS"
✅ Spec analysis complete (complexity: 0.78)

$ /sh:plan
✅ Phase plan created (18 waves, ~12 weeks)

Phase 1: Discovery (25% - adjusted for high complexity)
Phase 2: Architecture (20%)
Phase 3: Implementation (40%)
Phase 4: Testing (10%)
Phase 5: Deployment (5%)
```

### Example 3: With Constraints
```bash
$ /sh:plan --timeline "4 weeks" --team-size 2
⚠️  Timeline aggressive for complexity 0.68
✅ Phase plan adjusted for constraints
```

## Validation Gates

Each phase has mandatory validation gates:

**Phase 1 → 2**: Requirements documented, feasibility confirmed
**Phase 2 → 3**: Architecture approved, contracts defined
**Phase 3 → 4**: All features implemented, spec adherence verified
**Phase 4 → 5**: All tests pass, quality standards met
**Phase 5 → Complete**: Production operational, monitoring active

Use `/sh:status` to check current validation gate status.

---

**Shannon V4** - Skill-First Command Architecture 🎯
