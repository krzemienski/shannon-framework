---
name: intelligent-do
description: |
  Context-aware task execution with Serena MCP backend
skill-type: PROTOCOL
shannon-version: ">=5.2.0"
mcp-requirements:
  required:
    - name: serena
      purpose: Context backend
required-sub-skills: [wave-orchestration, memory-coordination]
allowed-tools: [Read, Write, Bash, Serena, SlashCommand]
---

# Intelligent Do

Context-aware execution using Serena MCP.

## Workflow

1. Check Serena: list_memories() → Search shannon_project_{id}
2. First-time: Explore, execute, save context
3. Returning: Load context, execute fast

Serena Keys: shannon_project_{id}, shannon_execution_{ts}
