# Shannon Framework v4 - Skill Definition Standard

**Version**: 1.0
**Date**: 2025-11-04
**Status**: APPROVED
**Applies To**: All Shannon v4 skills (13 core skills + future custom skills)

---

## Overview

This document defines the complete standard for Shannon Framework v4 skills, including:
- YAML frontmatter schema
- Markdown body structure (progressive disclosure)
- references/ directory pattern
- Executable code integration (TypeScript/Python)
- Validation rules and automation

**Design Principles** (from Phase 1 research):
1. **Progressive Disclosure** - 3-level loading to minimize token usage
2. **Executable Skills** - Optional TypeScript/Python code for complex logic
3. **Auto-Activation** - Skills can trigger based on context
4. **Composition** - Skills can require other skills (sub-skills)
5. **MCP Integration** - Explicit MCP dependencies declared

---

## Skill Directory Structure

```
shannon-plugin/skills/[skill-name]/
├── SKILL.md                      # Required: Skill definition (frontmatter + body)
├── [skill-name].ts               # Optional: TypeScript executable logic
├── [skill-name].py               # Optional: Python executable logic
├── [skill-name].test.ts          # Optional: Jest tests for TypeScript
├── [skill-name].test.py          # Optional: Pytest tests for Python
└── references/                   # Optional: Detailed documentation
    ├── ALGORITHM.md              # Detailed algorithms
    ├── EXAMPLES.md               # Comprehensive examples
    ├── INTEGRATION.md            # Integration patterns
    └── [OTHER_DOCS].md           # Any other detailed docs
```

**File Naming Rules**:
- Skill directory: lowercase, hyphens only (`spec-analysis`, not `Spec_Analysis`)
- SKILL.md: UPPERCASE (required by Claude Code)
- Executable files: Match skill directory name exactly
- References: UPPERCASE .md files for clarity

---

## Level 1: YAML Frontmatter (Always Loaded)

**Purpose**: Minimal metadata for skill discovery and registration

**Token Budget**: Target 50 tokens, Maximum 100 tokens

**Required Fields**:
```yaml
---
name: skill-name                  # REQUIRED: Lowercase, hyphens, max 64 chars
description: |                    # REQUIRED: What + when to use, max 1024 chars
  Brief description of what this skill does and when to use it.

  Use when:
  - Scenario 1
  - Scenario 2
  - Scenario 3

  Outputs: What this skill produces/returns.
---
```

**Optional Fields (Claude Code Official)**:
```yaml
allowed-tools:                    # OPTIONAL: Restrict tools during execution
  - Read
  - Grep
  - Serena
  - Sequential

license: MIT                      # OPTIONAL: License information

metadata:                         # OPTIONAL: Custom key-value pairs
  author: Shannon Framework Team
  version: 1.0.0
```

**Shannon-Specific Fields** (Custom, not validated by Claude Code):
```yaml
skill-type: QUANTITATIVE          # Shannon skill type classification
shannon-version: ">=4.0.0"        # Minimum Shannon version required

auto_activate: true               # Enable auto-activation
activation_priority: high         # Priority when multiple skills match
activation_threshold: 0.6         # 0.0-1.0 score required to activate
activation_triggers:              # Conditions for auto-activation
  complexity: ">= 0.60"
  keywords:
    - spec
    - specification
    - requirements
  conditions:
    - multi_paragraph_spec
    - requirements_list

required-sub-skills:              # Sub-skills that MUST be invoked
  - name: mcp-discovery
    purpose: "Identify recommended MCPs"
  - name: phase-planning
    purpose: "Generate execution plan"

optional-sub-skills:              # Sub-skills that MAY be invoked
  - name: confidence-check
    purpose: "Validate readiness"

mcp-dependencies:                 # MCP server requirements
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: "Context preservation"
      installation: "npm install -g @modelcontextprotocol/server-serena"
  recommended:
    - name: sequential
      version: ">=1.5.0"
      purpose: "Complex reasoning"
      fallback: "Use simpler reasoning"
  optional:
    - name: context7
      purpose: "Framework docs"
      fallback: "Use cached patterns"
```

**Skill Type Values**:
- `QUANTITATIVE` - Produces numerical scores/metrics (e.g., spec-analysis, confidence-check)
- `RIGID` - Strict workflow, no flexibility (e.g., phase-planning, functional-testing)
- `PROTOCOL` - Follows exact protocol/format (e.g., context-preservation, sitrep-reporting)
- `FLEXIBLE` - Adaptive workflow (e.g., shannon-analysis, project-indexing)

**Activation Priority Values**:
- `critical` - Always activate when triggered (e.g., context-preservation on PreCompact)
- `high` - Strongly recommended (e.g., spec-analysis for specifications)
- `medium` - Suggested (e.g., confidence-check)
- `low` - Optional (e.g., project-indexing for small codebases)

**Validation Rules** (Automated):
```python
# scripts/validate_skills.py

def validate_frontmatter(skill_path):
    """Validate YAML frontmatter for skill."""
    errors = []

    # Required fields
    if not frontmatter.get('name'):
        errors.append("Missing required field: name")
    if not frontmatter.get('description'):
        errors.append("Missing required field: description")

    # Name format
    if not re.match(r'^[a-z0-9-]+$', frontmatter.get('name', '')):
        errors.append("Invalid name format (use lowercase, hyphens only)")
    if len(frontmatter.get('name', '')) > 64:
        errors.append("Name exceeds 64 character limit")

    # Description length
    if len(frontmatter.get('description', '')) > 1024:
        errors.append("Description exceeds 1024 character limit")

    # Skill type validation
    valid_types = ['QUANTITATIVE', 'RIGID', 'PROTOCOL', 'FLEXIBLE']
    if frontmatter.get('skill-type') and frontmatter['skill-type'] not in valid_types:
        errors.append(f"Invalid skill-type (must be one of: {valid_types})")

    # Activation priority validation
    valid_priorities = ['critical', 'high', 'medium', 'low']
    if frontmatter.get('activation_priority') and frontmatter['activation_priority'] not in valid_priorities:
        errors.append(f"Invalid activation_priority (must be one of: {valid_priorities})")

    # Token budget check
    estimated_tokens = estimate_tokens(frontmatter)
    if estimated_tokens > 100:
        errors.append(f"Frontmatter exceeds 100 token budget ({estimated_tokens} tokens)")

    return errors
```

---

## Level 2: SKILL.md Body (Loaded on Invocation)

**Purpose**: High-level workflow and concise step instructions

**Line Budget**: Target 300-500 lines, Maximum 600 lines (HARD LIMIT)

**Structure Template**:

```markdown
# [Skill Name] Skill

## Overview
[2-3 paragraphs explaining purpose, capabilities, and when to use this skill]

## Prerequisites
- [Required context, tools, or setup]
- [If complex, reference: See references/PREREQUISITES.md]

## Workflow (High-Level)

1. [Step 1 Name]
2. [Step 2 Name]
3. [Step 3 Name - REQUIRED SUB-SKILL]
4. [Step 4 Name]
5. [Step 5 Name]
6. [Final Output]

---

## Step Details

### Step 1: [Step Name]

**Purpose**: [What this step accomplishes]

**Instructions**:
[Concise instructions - 5-10 lines maximum]
[Focus on WHAT to do, not detailed HOW]

**References**: See `references/[RELEVANT_DOC].md` for detailed algorithm/implementation

**Output**: [What this step produces]

---

### Step 2: [Step Name]

[Same structure as Step 1]

If executable code:
**Execute**: `@execute [skill-name].ts [functionName]`
```
Input: { ... }
Expected Output: { ... }
```

---

### Step 3: [Step Name] **REQUIRED SUB-SKILL**

**INVOKE**: @skill [sub-skill-name] --param1=value1 --param2=value2

**Purpose**: [Why this sub-skill is required]

**Input Expected**: [What sub-skill needs from previous steps]
**Output Expected**: [What sub-skill returns]

**Wait for sub-skill completion** before proceeding to Step 4.

**References**: See `references/SUB_SKILL_INTEGRATION.md` for integration patterns

---

[Continue for all steps...]

---

## Success Criteria

[Bullet list of measurable outcomes that indicate skill completed successfully]

- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

**Validation**: Run `confidence-check` if uncertain about success (recommended threshold: 90%)

---

## Error Handling

**Common Errors** (concise list):
- [Error 1]: [Quick fix]
- [Error 2]: [Quick fix]
- [Error 3]: [Quick fix]

**Complex Scenarios**: See `references/ERROR_RECOVERY.md` for detailed troubleshooting

---

## Examples

### Example 1: [Simple scenario]
[Brief example - 5-10 lines]

### Example 2: [Common scenario]
[Brief example - 5-10 lines]

**Comprehensive Examples**: See `references/EXAMPLES.md` for 10+ detailed examples

---

## SITREP Output

This skill generates a SITREP in the following format:

```markdown
## SITREP: [Skill Name] - [Task ID]

### Status
...

[Full SITREP template or reference to sitrep-reporting skill]
```

---

## Related Skills

- **[Sub-skill 1]**: [Brief description, when used]
- **[Sub-skill 2]**: [Brief description, when used]
- **[Related skill]**: [How it relates]

---

*Skill Version: 1.0.0 | Last Updated: 2025-11-04*
```

**Size Validation** (Automated):

```python
# scripts/validate_skills.py

def validate_skill_body(skill_path):
    """Validate SKILL.md body size."""
    skill_md = Path(skill_path) / 'SKILL.md'
    lines = skill_md.read_text().splitlines()

    # Remove frontmatter lines
    body_lines = []
    in_frontmatter = False
    frontmatter_count = 0

    for line in lines:
        if line.strip() == '---':
            frontmatter_count += 1
            in_frontmatter = (frontmatter_count == 1)
            continue
        if not in_frontmatter and frontmatter_count >= 2:
            body_lines.append(line)

    line_count = len(body_lines)

    if line_count > 600:
        return [f"SKILL.md body exceeds 600 line limit ({line_count} lines)"]
    elif line_count > 500:
        return [f"WARNING: SKILL.md body exceeds 500 line target ({line_count} lines)"]
    else:
        return []
```

---

## Level 3: references/ Directory (Loaded On-Demand)

**Purpose**: Detailed documentation, algorithms, examples (no size limits)

**Loading Mechanism**: Only loaded when SKILL.md explicitly mentions the file

**Recommended Files**:

```markdown
references/ALGORITHM.md
---
Purpose: Detailed mathematical/logical algorithms
Content:
  - Complete formulas with explanations
  - Pseudocode for complex logic
  - Edge case handling
  - Performance optimization notes
  - Historical context and rationale
Size: Unlimited

references/EXAMPLES.md
---
Purpose: Comprehensive example library
Content:
  - 10+ real-world examples
  - Small, medium, large, complex scenarios
  - Edge cases and corner cases
  - Expected inputs and outputs
  - Explanatory notes
Size: Unlimited

references/INTEGRATION.md
---
Purpose: Integration patterns (MCP, sub-skills, tools)
Content:
  - MCP integration code examples
  - Sub-skill invocation patterns
  - Tool usage patterns
  - Error handling strategies
  - Fallback mechanisms
Size: Unlimited

references/ERROR_RECOVERY.md
---
Purpose: Comprehensive error handling guide
Content:
  - All error scenarios (50+ if applicable)
  - Recovery procedures
  - Troubleshooting decision trees
  - Common pitfalls
  - Debugging techniques
Size: Unlimited

references/TESTING.md
---
Purpose: Testing guidelines and test cases
Content:
  - Functional test scenarios
  - Expected behaviors
  - Edge case testing
  - Performance benchmarks
  - Validation procedures
Size: Unlimited
```

**File Naming**: UPPERCASE .md files for consistency and visibility

**Cross-References**:
```markdown
In SKILL.md:
"See references/ALGORITHM.md for complete 8D scoring formulas"
"See references/EXAMPLES.md for 10+ comprehensive examples"

In references/ALGORITHM.md:
Can reference other references/:
"For integration with MCPs, see INTEGRATION.md"
```

---

## Executable Skills (Optional)

**When to Use Executable Code**:
- Complex mathematical calculations (e.g., 8D complexity scoring)
- Data processing/transformation (e.g., project indexing)
- Structured data generation (e.g., confidence scores)
- Performance-critical logic (e.g., large file processing)
- Reusable algorithms across skills

**When NOT to Use**:
- Simple workflows (markdown sufficient)
- Primarily text generation (Claude excels at this)
- Context-heavy reasoning (let Claude decide)

**TypeScript Executable Template**:

```typescript
// shannon-plugin/skills/[skill-name]/[skill-name].ts

/**
 * [Skill Name] - Executable TypeScript Logic
 *
 * Purpose: [What this executable does]
 * Author: Shannon Framework Team
 * Version: 1.0.0
 */

// Input interface (strict typing)
export interface [SkillName]Input {
  [param1]: string;
  [param2]: number;
  [param3]?: boolean;  // Optional parameter
}

// Output interface (structured data)
export interface [SkillName]Output {
  [result1]: number;
  [result2]: string[];
  [result3]: {
    [nested_field]: any;
  };
  confidence?: number;  // Optional confidence score
  metadata?: {
    execution_time_ms: number;
    version: string;
  };
}

// Main function (async if needed)
export async function [functionName](
  input: [SkillName]Input
): Promise<[SkillName]Output> {
  // Validate input
  validateInput(input);

  // Execute logic
  const result = await executeLogic(input);

  // Return structured data
  return {
    ...result,
    metadata: {
      execution_time_ms: performance.now(),
      version: '1.0.0'
    }
  };
}

// Helper functions (private)
function validateInput(input: [SkillName]Input): void {
  if (!input.[param1]) {
    throw new Error('[param1] is required');
  }
  // Additional validation...
}

async function executeLogic(input: [SkillName]Input): Promise<Partial<[SkillName]Output>> {
  // Core algorithm implementation
  return {
    [result1]: 0.85,
    [result2]: ['item1', 'item2']
  };
}

// Export for testing
export { validateInput, executeLogic };
```

**Python Executable Template**:

```python
# shannon-plugin/skills/[skill-name]/[skill-name].py

"""
[Skill Name] - Executable Python Logic

Purpose: [What this executable does]
Author: Shannon Framework Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time

@dataclass
class [SkillName]Input:
    """Input parameters for [skill-name] skill."""
    param1: str
    param2: float
    param3: Optional[bool] = None

@dataclass
class [SkillName]Output:
    """Output data structure for [skill-name] skill."""
    result1: float
    result2: List[str]
    result3: Dict[str, Any]
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class [SkillName]:
    """[Skill description]."""

    def __init__(self):
        self.version = "1.0.0"

    def execute(self, input_data: [SkillName]Input) -> [SkillName]Output:
        """
        Main execution function.

        Args:
            input_data: Input parameters

        Returns:
            Structured output data

        Raises:
            ValueError: If input validation fails
        """
        # Validate input
        self._validate_input(input_data)

        # Track execution time
        start_time = time.time()

        # Execute logic
        result = self._execute_logic(input_data)

        # Add metadata
        execution_time = (time.time() - start_time) * 1000

        return [SkillName]Output(
            **result,
            metadata={
                'execution_time_ms': execution_time,
                'version': self.version
            }
        )

    def _validate_input(self, input_data: [SkillName]Input) -> None:
        """Validate input parameters."""
        if not input_data.param1:
            raise ValueError("param1 is required")
        # Additional validation...

    def _execute_logic(self, input_data: [SkillName]Input) -> Dict[str, Any]:
        """Core algorithm implementation."""
        return {
            'result1': 0.85,
            'result2': ['item1', 'item2'],
            'result3': {'key': 'value'}
        }

# Convenience function for direct invocation
def [function_name](input_data: [SkillName]Input) -> [SkillName]Output:
    """Execute [skill-name] skill."""
    skill = [SkillName]()
    return skill.execute(input_data)
```

**Invocation from SKILL.md**:

```markdown
### Step 2: Calculate Complexity

**Execute TypeScript**:
@execute spec-analysis.ts analyzeSpecification
```json
Input: {
  "specification": "[user spec text]",
  "project_context": {}
}
```

Expected Output:
```json
{
  "complexity_scores": {
    "structural": 0.75,
    "cognitive": 0.68,
    ...
  },
  "domains": {...},
  "confidence": 0.92,
  "metadata": {...}
}
```

Use the returned `complexity_scores` in the next steps...
```

**Testing Requirements**:

```typescript
// [skill-name].test.ts (Jest)

import { [functionName], validateInput } from './[skill-name]';

describe('[SkillName] Executable', () => {
  describe('Input Validation', () => {
    it('should throw error for missing required params', () => {
      expect(() => validateInput({ param1: '' })).toThrow();
    });

    it('should accept valid input', () => {
      expect(() => validateInput({ param1: 'valid' })).not.toThrow();
    });
  });

  describe('Core Logic', () => {
    it('should return correct output structure', async () => {
      const input = { param1: 'test', param2: 0.5 };
      const output = await [functionName](input);

      expect(output).toHaveProperty('result1');
      expect(output).toHaveProperty('result2');
      expect(output).toHaveProperty('metadata');
    });

    it('should calculate expected values', async () => {
      const input = { param1: 'known input', param2: 1.0 };
      const output = await [functionName](input);

      expect(output.result1).toBeCloseTo(0.85, 2);
      expect(output.result2).toContain('item1');
    });
  });
});
```

```python
# [skill-name].test.py (Pytest)

import pytest
from [skill_name] import [SkillName], [SkillName]Input

class Test[SkillName]:
    def test_input_validation(self):
        """Test input validation."""
        skill = [SkillName]()

        # Missing required parameter
        with pytest.raises(ValueError):
            skill.execute([SkillName]Input(param1=''))

        # Valid input
        skill.execute([SkillName]Input(param1='valid', param2=0.5))

    def test_output_structure(self):
        """Test output contains all required fields."""
        skill = [SkillName]()
        input_data = [SkillName]Input(param1='test', param2=0.5)
        output = skill.execute(input_data)

        assert hasattr(output, 'result1')
        assert hasattr(output, 'result2')
        assert hasattr(output, 'metadata')

    def test_expected_values(self):
        """Test calculation produces expected values."""
        skill = [SkillName]()
        input_data = [SkillName]Input(param1='known input', param2=1.0)
        output = skill.execute(input_data)

        assert output.result1 == pytest.approx(0.85, abs=0.01)
        assert 'item1' in output.result2
```

---

## Complete Example: spec-analysis Skill

**Directory Structure**:
```
shannon-plugin/skills/spec-analysis/
├── SKILL.md                          # 487 lines (within 600 limit)
├── spec-analysis.ts                  # 342 lines
├── spec-analysis.test.ts             # 156 lines
└── references/
    ├── 8D_ALGORITHM.md               # 1,234 lines (detailed formulas)
    ├── EXAMPLES.md                   # 876 lines (15 examples)
    ├── INTEGRATION.md                # 423 lines (MCP patterns)
    └── ERROR_RECOVERY.md             # 267 lines (troubleshooting)
```

**Frontmatter** (spec-analysis/SKILL.md):
```yaml
---
name: spec-analysis
description: |
  Analyzes specifications using 8-dimensional complexity framework.

  Use when:
  - New project specifications provided (any format)
  - Requirement changes need impact assessment
  - Complexity estimation required for planning
  - Domain identification needed for tech stack selection

  Outputs: 8D complexity scores (0-1 scale), domain percentages (6 categories),
  MCP recommendations (mandatory/recommended/optional), 5-phase plan structure,
  comprehensive SITREP.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"
auto_activate: true
activation_priority: high
activation_threshold: 0.6
activation_triggers:
  complexity: ">= 0.60"
  keywords:
    - spec
    - specification
    - requirements
    - PRD
    - "user stories"
  conditions:
    - multi_paragraph_spec
    - requirements_list

required-sub-skills:
  - name: mcp-discovery
    purpose: "Identify recommended MCPs based on detected domains"
  - name: phase-planning
    purpose: "Generate 5-phase execution plan from complexity analysis"

optional-sub-skills:
  - name: confidence-check
    purpose: "Validate specification understanding before analysis"

mcp-dependencies:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: "Context preservation and project memory"
      installation: "npm install -g @modelcontextprotocol/server-serena"
  recommended:
    - name: sequential
      version: ">=1.5.0"
      purpose: "Complex multi-step reasoning for 8D analysis"
      fallback: "Use simpler reasoning (may reduce accuracy)"
    - name: context7
      purpose: "Framework documentation lookup for domain classification"
      fallback: "Use cached patterns and heuristics"

allowed-tools:
  - Read
  - Grep
  - Glob
  - Serena
  - Sequential
  - Context7

metadata:
  author: Shannon Framework Team
  version: 1.0.0
  license: MIT
---
```

**Body Excerpt** (spec-analysis/SKILL.md):
```markdown
# Specification Analysis Skill

## Overview

The Specification Analysis skill performs comprehensive 8-dimensional complexity
assessment of project specifications to enable right-sized effort allocation,
intelligent tech stack recommendations, and structured execution planning.

[... continues for 487 lines total]

## Workflow

1. Parse Specification
2. Calculate 8D Complexity (Executable)
3. Discover MCPs (Required Sub-Skill)
4. Quantify Domains
5. Generate Phase Plan (Required Sub-Skill)
6. Create SITREP

## Step 2: Calculate 8D Complexity

**Execute TypeScript**:
@execute spec-analysis.ts analyzeSpecification

[... detailed instructions]

See `references/8D_ALGORITHM.md` for complete mathematical formulas and calibration data.

## Step 3: Discover MCPs **REQUIRED SUB-SKILL**

**INVOKE**: @skill mcp-discovery --domains=[from Step 2] --complexity=[overall]

[... integration details]
```

**Executable** (spec-analysis/spec-analysis.ts):
```typescript
// 342 lines of 8D calculation logic
export interface SpecAnalysisOutput {
  complexity_scores: {
    structural: number;
    cognitive: number;
    // ... 8 dimensions
  };
  domains: {
    frontend: number;
    backend: number;
    // ... 6 categories
  };
  recommended_mcps: string[];
  confidence: number;
}

export async function analyzeSpecification(
  input: { specification: string }
): Promise<SpecAnalysisOutput> {
  // [342 lines of implementation]
}
```

**References** (spec-analysis/references/8D_ALGORITHM.md):
```markdown
# 8-Dimensional Complexity Scoring Algorithm

## Structural Dimension (Weight: 20%)

Complete mathematical formula:
...

[1,234 lines of detailed algorithm documentation]
```

---

## Validation Automation

**Script**: `scripts/validate_skills.py`

```python
#!/usr/bin/env python3
"""
Shannon v4 Skill Validation

Validates all skills in shannon-plugin/skills/ directory.
Checks:
  - Frontmatter schema compliance
  - SKILL.md size limits
  - Required files present
  - Executable code syntax (if present)
  - Test coverage (if executable)
"""

import sys
from pathlib import Path
import yaml
import subprocess

def validate_all_skills(skills_dir: Path) -> bool:
    """Validate all skills in directory."""
    all_valid = True

    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir():
            continue

        print(f"\nValidating {skill_path.name}...")

        errors = []
        errors.extend(validate_skill_structure(skill_path))
        errors.extend(validate_frontmatter(skill_path))
        errors.extend(validate_skill_body(skill_path))
        errors.extend(validate_executables(skill_path))

        if errors:
            all_valid = False
            for error in errors:
                print(f"  ❌ {error}")
        else:
            print(f"  ✅ Valid")

    return all_valid

if __name__ == '__main__':
    skills_dir = Path(__file__).parent.parent / 'shannon-plugin' / 'skills'
    if validate_all_skills(skills_dir):
        print("\n✅ All skills valid")
        sys.exit(0)
    else:
        print("\n❌ Validation failed")
        sys.exit(1)
```

**CI Integration** (.github/workflows/validate-skills.yml):
```yaml
name: Validate Skills

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: python scripts/validate_skills.py
```

---

## Summary

Shannon v4 Skill Definition Standard ensures:

✅ **Consistent Structure** - All skills follow same format
✅ **Token Efficiency** - Progressive disclosure minimizes context usage
✅ **Executable Integration** - Complex logic in TypeScript/Python
✅ **Auto-Activation** - Skills trigger based on context
✅ **Composition** - Skills can require sub-skills
✅ **MCP Integration** - Explicit dependencies declared
✅ **Automated Validation** - CI ensures compliance

**Status**: APPROVED for Shannon v4 implementation

**Next Steps**:
1. Implement 13 core skills following this standard (Phase 3 Wave 3)
2. Create skill templates for each skill type
3. Build validation automation (Phase 3 Wave 1)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-04
**Next Review**: After first 3 skills implemented
