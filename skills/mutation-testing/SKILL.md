---
name: mutation-testing
description: |
  Verify test quality by injecting mutations into code and measuring catch rate. Calculate mutation score (0.00-1.00) showing test effectiveness. Auto-generate missing tests to improve coverage. Integrate with Serena for continuous mutation tracking. Use when: improving test quality, validating test effectiveness, generating missing test cases, measuring code coverage gaps.

skill-type: ANALYTICAL
shannon-version: ">=5.6.0"

mcp-requirements:
  recommended:
    - name: serena
      purpose: Mutation tracking, historical scoring, correlation analysis
    - name: stryker
      purpose: Mutation testing framework integration
    - name: pitest
      purpose: Java/Kotlin mutation testing
    - name: mutmut
      purpose: Python mutation testing

allowed-tools: All
---

# Mutation Testing - Quantified Test Quality

## Purpose

Measure test effectiveness by injecting mutations (intentional bugs) into code and tracking how many your tests catch. Calculates mutation score (0.00-1.00) to quantify test coverage gaps. Auto-generates additional tests targeting uncaught mutations. Integrates with Serena MCP for continuous tracking and trend analysis.

## When to Use

- Measuring test effectiveness beyond code coverage
- Identifying weak test areas (low mutation scores)
- Auto-generating tests for mutation-resistant code
- Validating test quality gates (require 0.80+ mutation score)
- Tracking mutation improvements over time
- Comparing mutation scores across teams/projects

## Core Metrics

**Mutation Score Calculation:**
```
Score = (Killed Mutations / Total Mutations) × 1.0
Range: 0.00 (no tests catch bugs) to 1.00 (all bugs caught)
```

**Score Interpretation:**
- 0.90+ Excellent test suite, catches most bugs
- 0.80-0.89 Good coverage, minor gaps
- 0.70-0.79 Acceptable but needs improvement
- <0.70 Poor coverage, significant blind spots

## Workflow

### Phase 1: Mutation Generation & Execution
1. **Inject mutations**: Stryker/PIT/mutmut inject bugs
2. **Run tests**: Execute full test suite
3. **Track kills**: Count caught vs escaped mutations
4. **Calculate score**: Derive 0.00-1.00 metric

### Phase 2: Serena Integration
1. **Push metrics**: Send mutation_score, killed_count, escaped_count to Serena
2. **Track history**: Store scores by commit, branch, timestamp
3. **Alert on regression**: Flag if score drops >0.05
4. **Trend analysis**: Show mutation score trajectory

**Serena Push Example:**
```json
{
  "metric_type": "mutation_score",
  "project": "task-app",
  "value": 0.87,
  "components": {
    "auth": 0.92,
    "api": 0.85,
    "ui": 0.79
  },
  "killed": 156,
  "escaped": 23,
  "timestamp": "2025-11-20T10:30:00Z"
}
```

### Phase 3: Gap Analysis & Test Generation
1. **Identify mutations**: List escaped mutations (bugs tests miss)
2. **Pattern detection**: Group by type (boundary, null, operator)
3. **Generate tests**: Auto-create test cases targeting gaps
4. **Validate new tests**: Confirm they catch previously escaped mutations

**Auto-Generated Test Example:**
```python
# Escaped mutation: changed > to >= in boundary check
# Auto-generated test catches this:
def test_score_boundary_at_90():
    """Catches mutations in >= vs > comparisons"""
    assert get_grade(90) == 'A'  # Catches >= → > mutation
    assert get_grade(89) == 'B'  # Catches >= → > at boundary

def test_null_mutations():
    """Catches null/None comparison mutations"""
    assert validate_email(None) == False  # Catches is None → == None
    assert validate_email("") == False    # Catches == "" mutations
```

## Real-World Impact

**E-Commerce Cart System:**
- Initial mutation score: 0.71 (many edge cases uncaught)
- Generated 34 new tests targeting mutations
- Improved score to 0.88 (caught boundary bugs, null handling)
- Prevented 12 production bugs in checkout flow

**Financial API:**
- Mutation score: 0.82 initially
- Serena tracked regression: dropped to 0.79 (new code)
- Auto-generated 8 tests for numeric precision mutations
- Restored to 0.85, prevented rounding errors

## Success Criteria

✅ Mutation score ≥0.80 for critical code
✅ No score regression >0.05 between commits
✅ Auto-generated tests all pass
✅ Serena tracking shows improvement trend
✅ Gap analysis identifies specific weak patterns
