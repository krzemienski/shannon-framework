---
auto_persona:
- architect
- analyzer
base: SuperClaude /task command
category: command
command: /sc:task
complexity_threshold: 0.6
description: Long-term project management with wave orchestration, phase tracking,
  and cross-session persistence
mcp_servers:
- serena
- sequential
name: sc:task
progressive_disclosure:
  estimated_tokens: 200
  full_content: resources/FULL.md
  tier: 1
shannon_enhancement: true
sub_agents:
- WAVE_COORDINATOR
- PHASE_ARCHITECT
tools:
- Task
- TodoWrite
- Read
- Write
wave_enabled: true
---

/sc:task - Project Task Management with Wave Orchestration

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

> **Shannon V3 Enhancement**: SuperClaude's `/task` command enhanced with wave orchestration, PHASE_ARCHITECT integration, Serena-based progress tracking, and multi-session project continuity.

## Usage Patterns

### Pattern 1: Create New Project

```bash
# Create project with automatic wave orchestration
/sc:task create e-commerce "Build e-commerce web app with React, Express, PostgreSQL"

# System Response:
Creating project: e-commerce
- Analyzing specification via SPEC_ANALYZER
- Generating phase plan via PHASE_ARCHITECT
- Calculating wave structure via WAVE_COORDINATOR
- Saving project state to Serena

PROJECT CREATED: e-commerce
Complexity: 0.78 (high)
Timeline: 40 hours across 5 phases
Wave orchestration: ENABLED (9 waves planned)
Validation gates: 5 defined

Ready to execute Phase 1 Discovery
Run: /sc:task execute e-commerce
```

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
