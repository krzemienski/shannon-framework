---
name: skill-name
description: |
  [160-250 characters describing purpose, when to use, what it provides]
  Use this skill when [trigger condition]. Provides [key capabilities].

skill-type: QUANTITATIVE | RIGID | PROTOCOL | FLEXIBLE
shannon-version: ">=4.0.0"

# MCP INTEGRATION (optional)
mcp-requirements:
  required:
    - name: mcp-name
      purpose: Why this MCP is required
      fallback: What to do if unavailable
  recommended:
    - name: mcp-name
      purpose: Why this MCP enhances capability
      fallback: Degraded behavior
      trigger: When to use (e.g., complexity >= 0.70)
  conditional:
    - name: mcp-name
      purpose: Domain-specific capability
      trigger: When applicable (e.g., frontend domain >= 30%)

# COMPOSITION (optional)
required-sub-skills:
  - skill-name
optional-sub-skills:
  - skill-name

# PERMISSIONS (optional)
allowed-tools: [Read, Write, Grep, Bash, etc.]
model: sonnet | opus | haiku
---

# Skill Name

## Purpose

[2-3 sentences describing what this skill does and its core value]

## When to Use

Use this skill when:
- [Specific trigger condition 1]
- [Specific trigger condition 2]
- [Specific trigger condition 3]

DO NOT use when:
- [Anti-pattern 1]
- [Anti-pattern 2]

## Core Competencies

1. **[Competency Area 1]**: [What skill can do in this area]
2. **[Competency Area 2]**: [What skill can do in this area]
3. **[Competency Area 3]**: [What skill can do in this area]

## Inputs

**Required:**
- `input_name` (type): Description and constraints

**Optional:**
- `option_name` (type): Description, default value

## Workflow

### Phase 1: [Phase Name]

1. **[Step Name]**
   - Action: [What to do]
   - Tool: [Which tool to use]
   - Output: [What this produces]

2. **[Step Name]**
   - Action: [What to do]
   - Validation: [How to verify]
   - Output: [What this produces]

### Phase 2: [Phase Name]

[Continue workflow steps...]

## Agent Activation

[If applicable]

This skill activates the `AGENT_NAME` agent when:
- [Trigger condition]
- [Complexity threshold]

Agent provides:
- System prompt: [Agent role description]
- Tools: [Available tools]
- Context: [What agent receives]

## MCP Integration

[If applicable]

**Required MCPs:**
- **MCP Name**: [Purpose and usage pattern]
  - Fallback: [What to do if unavailable]
  - Error: [Error message to show]

**Recommended MCPs:**
- **MCP Name**: [Enhancement provided]
  - Fallback: [Degraded behavior]
  - Trigger: [When to use]

## Outputs

Structured output object:

```json
{
  "field_name": "value_description",
  "nested_object": {
    "field": "description"
  }
}
```

## Success Criteria

This skill succeeds if:

1. ✅ [Specific measurable criterion]
2. ✅ [Specific measurable criterion]
3. ✅ [Specific measurable criterion]

Validation:
```python
def validate_output(result):
    assert criterion_1
    assert criterion_2
```

## Common Pitfalls

### Pitfall 1: [Pitfall Name]

**Wrong:**
```
[Example of wrong approach]
```

**Right:**
```
[Example of correct approach]
```

**Why:** [Explanation]

### Pitfall 2: [Pitfall Name]

[Continue pattern...]

## Examples

### Example 1: Simple Case

**Input:**
```
[Example input]
```

**Process:**
```
[Key steps]
```

**Output:**
```json
{
  "example": "output"
}
```

### Example 2: Complex Case

[Continue pattern...]

### Example 3: Edge Case

[Continue pattern...]

## Validation

How to verify this skill worked correctly:

1. [Validation step 1]
2. [Validation step 2]
3. [Validation step 3]

## Progressive Disclosure

**In SKILL.md** (this file):
- Core workflow (~400-600 lines)
- Essential examples
- Key success criteria

**In references/** (for deep details):
- `references/DETAILED_ALGORITHM.md`: Complete algorithm specification
- `references/ADVANCED_PATTERNS.md`: Advanced usage patterns

## References

- Core Documentation: `shannon-plugin/core/[RELEVANT_DOC].md`
- Related Skills: `@skill-name`, `@other-skill`
- MCP Setup: See `/shannon:check_mcps` for MCP configuration

---

**Skill Type Classification:**
- **QUANTITATIVE**: Follow algorithm exactly, no subjective adjustments
- **RIGID**: Iron laws, zero exceptions, maximum enforcement
- **PROTOCOL**: Template-driven, follow structure closely, minor adaptations allowed
- **FLEXIBLE**: Principle-based, adapt to context while maintaining core intent
