---
auto_activate: false
base: SuperClaude /spawn command
category: command
command: /sc:spawn
deliverables:
- spawned_agents
- coordination_plans
- execution_results
description: Enhanced meta-orchestration command with wave coordination awareness
  and Serena context sharing
enhancements:
- wave_orchestration
- serena_context_sharing
- parallel_coordination
mcp_servers:
- serena
- sequential
name: sc:spawn
priority: high
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
sub_agents:
- WAVE_COORDINATOR
- PHASE_ARCHITECT
- domain_specialists
tools:
- Task
- TodoWrite
- Read
- Grep
triggers:
- spawn
- orchestrate
- coordinate
- multi-agent
- parallel-execution
---

/sc:spawn - Enhanced Task Orchestration Command

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

## Purpose Statement

**Base Capability** (SuperClaude): Meta-system task orchestration with intelligent breakdown and delegation for complex multi-domain operations.

**Shannon V3 Enhancements**: Wave orchestration awareness, Serena-based context sharing, WAVE_COORDINATOR integration, and parallel sub-agent coordination with complete context preservation.

## Usage Examples

### Example 1: Simple Multi-Agent Analysis

```bash
User: /sc:spawn analyze codebase --focus security,performance

Claude:
## 🚀 Spawning Sub-Agents: Codebase Analysis

**Operation Details**:
- Operation: Comprehensive codebase analysis
- Complexity: 0.6 / 1.0 (medium)
- Agent Count: 2 agents
- Execution Pattern: Parallel
- Checkpoint: Not required

**Context Setup**:
Loaded from Serena:
✓ spec_analysis (project requirements)
✓ architecture_complete (system design)

**Agent Assignments**:
1. **security-specialist** - Security vulnerability scan and threat modeling
2. **performance-analyst** - Performance bottleneck identification and optimization

**Spawning 2 Agents in PARALLEL**:

[Both agents execute simultaneously with context loading]

---

##

## Skill Integration

**v4 NEW**: This command activates skills:


## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
