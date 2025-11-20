---
name: sh:wave
linked_skills:
  - shannon-wave-orchestrator
progressive_disclosure:
  tier: 1
  estimated_tokens: 100
---

# /sh:wave
> **Skill-Based**: This command activates the `shannon-wave-orchestrator` skill

## Usage
```bash
/sh:wave 1
/sh:wave next
```

## What It Does
Executes parallel wave of independent tasks with:
- **TRUE Parallelism** - ONE message with multiple Task invocations (2-4× speedup)
- **Automated context injection** - All agents receive north_star, spec_analysis, phase_plan
- **Dependency management** - Tasks grouped by dependencies
- **Validation gates** - Pre/post wave validation
- **State persistence** - Results saved to Serena

Wave completes when all tasks succeed and validation passes.

Outputs SITREP with:
- Wave results (tasks succeeded/failed)
- Next wave number or phase completion
- Validation status

## Skill Activation
📚 **Full orchestration logic**: `shannon-v4-plugin/skills/shannon-wave-orchestrator/SKILL.md`

**Progressive disclosure**: Full skill content loaded only when activated

---

**Shannon V4** - Parallel Wave Execution 🚀
