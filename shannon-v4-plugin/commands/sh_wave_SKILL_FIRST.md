---
name: sh:wave
command: /sh:wave
description: "Executes parallel wave orchestration with automated context injection and validation"
category: command
complexity: advanced
triggers: [wave, parallel, orchestration]
mcp_servers: [serena, sequential]
linked_skills:
  - shannon-wave-orchestrator
auto_activate: true
progressive_disclosure:
  tier: 1
  full_content: resources/sh_wave_FULL.md
  estimated_tokens: 100
---

# /sh:wave - Wave Orchestration

> **Skill-Based**: This command activates the `shannon-wave-orchestrator` skill

## Purpose

Executes wave-based parallel task orchestration with:
- TRUE parallelism (2-4× speedup)
- Automated context injection
- Dependency validation
- Result collection

## Usage

```bash
# Execute specific wave
/sh:wave 1
/sh:wave 2

# Execute next wave
/sh:wave next

# Retry failed wave
/sh:wave 1 --retry
```

## Skill Activation

This command activates: **`shannon-wave-orchestrator`**

**The skill provides**:
- Dependency analysis and wave grouping
- Parallel agent spawning (ONE message multi-Task)
- Automated context loading for all agents
- Pre/post wave validation gates
- Serena MCP state management

## Prerequisites

Before running waves:
1. ✅ Run `/sh:spec` to create specification
2. ✅ Run `/sh:plan` to create phase plan
3. ✅ Verify Serena MCP connected

## How It Works

```
/sh:wave 1
  ↓
shannon-wave-orchestrator skill activates
  ↓
PreWave hook: Validates dependencies, injects context
  ↓
ONE message with multiple Task invocations (true parallelism)
  ↓
Wave agents execute in parallel (2-4× faster)
  ↓
PostWave hook: Collects results, validates outputs
  ↓
QualityGate hook: Enforces 5-gate validation
  ↓
Results saved to Serena
  ↓
Next wave or checkpoint
```

## Example

```bash
# Wave 1: Foundation (4 parallel tasks)
/sh:wave 1
# Spawns: database-schema, auth-system, ui-framework, api-design
# Executes: ALL 4 in parallel (ONE message)
# Result: 4 tasks complete in ~1× time (not 4×)

# Wave 2: Implementation (6 parallel tasks)
/sh:wave 2
# Spawns: db-models, auth-impl, ui-components, api-endpoints, tests, docs
# Executes: ALL 6 in parallel (ONE message)
# Result: 6 tasks complete in ~1× time (not 6×)
```

**Total Time**: 2 waves vs 10 sequential tasks = 5× speedup

## Quick Reference

📚 **Full Wave Logic**: See [skills/shannon-wave-orchestrator/SKILL.md](../skills/shannon-wave-orchestrator/SKILL.md)
📚 **Wave Patterns**: See [skills/shannon-wave-orchestrator/resources/WAVE_PATTERNS.md](../skills/shannon-wave-orchestrator/resources/WAVE_PATTERNS.md)
📚 **Command Examples**: See [resources/EXAMPLES.md](./resources/EXAMPLES.md)

## Related Commands

- `/sh:spec` - Create specification (run first)
- `/sh:plan` - Create phase plan (run second)
- `/sh:checkpoint` - Save wave progress
- `/sh:status` - Check wave status

## Error Messages

**"Wave N cannot execute: Wave N-1 not complete"**
→ Complete previous wave first or use `--retry`

**"Context incomplete: spec_analysis not found"**
→ Run `/sh:spec` first

**"Wave validation failed"**
→ Review failed tasks and fix issues

---

**Shannon V4** - Parallel Wave Orchestration 🚀

**Token Count**: ~100 tokens (command metadata only)
**Full Logic**: In `shannon-wave-orchestrator` skill (~2,000 tokens, loaded on-demand)
**Reduction**: 95% vs prose-based approach
