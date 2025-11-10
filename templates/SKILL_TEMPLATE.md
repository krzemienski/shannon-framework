---
name: skill-name
description: |
  [160-250 character rich description with purpose, capabilities, trigger keywords, use cases]

skill-type: QUANTITATIVE | RIGID | PROTOCOL | FLEXIBLE
shannon-version: ">=4.0.0"
complexity-triggers: [0.0-1.0]

mcp-requirements:
  required:
    - name: serena
      purpose: Context preservation
      fallback: local-storage
  recommended: []
  conditional: []

required-sub-skills: []
optional-sub-skills: []

allowed-tools: Read, Grep, Glob, Serena
---

# Skill Name

## Overview

**Purpose**: [What this skill does in one paragraph]

**When to Use**:
- [Trigger scenario 1]
- [Trigger scenario 2]
- [Trigger scenario 3]

**Expected Outcomes**: [What user receives]

**Duration**: [Time estimate]

---

## Core Competencies

### 1. [Competency Area 1]
- [Capability 1]
- [Capability 2]
- [Capability 3]

### 2. [Competency Area 2]
- [Capability 1]
- [Capability 2]

### 3. [Competency Area 3]
- [Capability 1]
- [Capability 2]

---

## Workflow

### Step 1: [Action Name]
**Input**: [Data structure or requirements]

**Processing**:
1. [Detailed sub-step]
2. [Detailed sub-step]
3. [Detailed sub-step]

**Output**: [Data structure produced]

**Duration**: [Time estimate]

### Step 2: [Action Name]
**Input**: [From Step 1]

**Processing**:
1. [Detailed sub-step]
2. [Detailed sub-step]

**Output**: [Data structure produced]

---

## Agent Activation

**Agent**: [AGENT_NAME] (if applicable)

**Context Provided**:
- System prompt: "[Agent's specialized prompt]"
- Tools: [Allowed tools]
- Domain knowledge: [What agent knows]

**Activation Trigger**: [When agent activates]

---

## MCP Integration

### Required MCPs

**[MCP Name]**
- **Purpose**: [Why this skill needs it]
- **Usage**: [Pattern or code example]
- **Fallback**: [If unavailable]
- **Degradation**: [Impact level: high/medium/low]

### Recommended MCPs

**[MCP Name]**
- **Purpose**: [Enhancement it provides]
- **Trigger**: [When to use]
- **Fallback**: [Alternative approach]

---

## Examples

### Example 1: [Simple Case]
**Input**:
```
[Example input]
```

**Execution**:
```
[Step-by-step what happens]
```

**Output**:
```
[Expected result]
```

### Example 2: [Complex Case]
**Input**: [...]

**Execution**: [...]

**Output**: [...]

### Example 3: [Edge Case]
**Input**: [...]

**Execution**: [...]

**Output**: [...]

---

## Success Criteria

**Successful when**:
- ✅ [Measurable criterion 1]
- ✅ [Measurable criterion 2]
- ✅ [Measurable criterion 3]

**Fails if**:
- ❌ [Anti-criterion 1]
- ❌ [Anti-criterion 2]

---

## Common Pitfalls

### Pitfall 1: [Problem Name]
**Problem**: [Description of what goes wrong]

**Solution**: [How to fix it]

**Prevention**: [How to avoid in future]

### Pitfall 2: [Problem Name]
**Problem**: [...]

**Solution**: [...]

**Prevention**: [...]

### Pitfall 3: [Problem Name]
[...]

---

## Validation

**How to verify this skill executed correctly**:
1. [Check 1]
2. [Check 2]
3. [Check 3]

---

## Progressive Disclosure

**SKILL.md** (This file): ~400-600 lines
- [What's included in main file]

**references/**: [What's deferred to references]
- [Reference file 1] - [Purpose]
- [Reference file 2] - [Purpose]

**Claude loads references/ when**: [Conditions that trigger loading deep references]

---

## References

- [Link to core/ document if applicable]
- [Link to related skills]
- [External documentation]

---

## Metadata

**Version**: 4.0.0
**Last Updated**: 2025-11-03
**Author**: Shannon Framework Team
**License**: MIT
**Status**: [Core | Enhanced | Experimental]
