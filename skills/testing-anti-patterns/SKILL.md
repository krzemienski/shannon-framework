---
name: testing-anti-patterns
description: Use when writing or changing tests, adding mocks, or tempted to add test-only methods to production code - prevents testing mock behavior, production pollution with test-only methods, and mocking without understanding dependencies, with quantitative anti-pattern detection scoring
---

# Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle**: Test what the code does, not what the mocks do.

**Shannon enhancement**: Automatically detect and score anti-patterns quantitatively.

**Following strict TDD prevents these anti-patterns.**

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
4. NEVER use partial/incomplete mocks
5. SHANNON: Track anti-pattern violations quantitatively
```

## Anti-Pattern 1: Testing Mock Behavior

**Severity**: 0.95/1.00 (CRITICAL)

**The violation**:
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**Why this is wrong**:
- You're verifying the mock works, not that the component works
- Test passes when mock is present, fails when it's not
- Tells you nothing about real behavior

**Shannon detection**:
```python
# Automatically detect mock behavior testing
def detect_mock_testing(test_code: str) -> float:
    """Returns anti-pattern score 0.00-1.00"""
    score = 0.0

    # Check for mock-specific test IDs
    if re.search(r'getByTestId.*-mock', test_code):
        score += 0.50

    # Check for assertions on mock existence only
    if 'expect(.*mock.*).toBe' in test_code and 'real assertion' not in test_code:
        score += 0.45

    return min(score, 1.0)

# Track in Serena
anti_pattern_detected = {
    "type": "testing_mock_behavior",
    "severity": 0.95,
    "test_file": test_file,
    "line": line_number,
    "recommendation": "Test real component behavior, not mock existence"
}
```

**The fix**:
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

## Anti-Pattern 2: Test-Only Methods in Production

**Severity**: 0.85/1.00 (HIGH)

**The violation**:
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
  }
}
```

**Shannon detection**:
```python
# Detect test-only methods in production classes
def detect_test_only_methods(production_code: str, test_code: str) -> dict:
    """Scans for methods only called in tests"""

    production_methods = extract_public_methods(production_code)
    test_usage = extract_method_calls(test_code)
    production_usage = extract_method_calls(production_code)

    test_only = []
    for method in production_methods:
        if method in test_usage and method not in production_usage:
            test_only.append({
                "method": method,
                "severity": 0.85,
                "recommendation": "Move to test utilities"
            })

    return test_only
```

**The fix**:
```typescript
// ✅ GOOD: Test utilities handle test cleanup
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}
```

## Anti-Pattern 3: Mocking Without Understanding

**Severity**: 0.75/1.00 (HIGH)

**The violation**:
```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate server', () => {
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**Shannon detection**:
```python
# Detect mocking that breaks test dependencies
def detect_over_mocking(test_code: str) -> dict:
    """Identifies mocks that may break test logic"""

    mocked_methods = extract_mocked_methods(test_code)
    test_expectations = extract_expectations(test_code)

    suspicious_mocks = []
    for mock in mocked_methods:
        # Check if mock returns undefined/null for methods that have side effects
        if 'mockResolvedValue(undefined)' in mock['implementation']:
            suspicious_mocks.append({
                "mock": mock['name'],
                "severity": 0.75,
                "reason": "Mocking method to undefined may break test dependencies"
            })

    return suspicious_mocks
```

**The fix**:
```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate server', () => {
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

## Anti-Pattern 4: Incomplete Mocks

**Severity**: 0.80/1.00 (HIGH)

**The violation**:
```typescript
// ❌ BAD: Partial mock
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};
```

**Shannon detection**:
```python
# Detect incomplete mocks by comparing to real API schema
def detect_incomplete_mocks(mock_data: dict, real_schema: dict) -> dict:
    """Compares mock to real API schema"""

    missing_fields = []
    mock_keys = set(mock_data.keys())
    schema_keys = set(real_schema.keys())

    missing = schema_keys - mock_keys
    completeness = len(mock_keys) / len(schema_keys) if schema_keys else 1.0

    return {
        "severity": 1.0 - completeness,  # More missing = higher severity
        "missing_fields": list(missing),
        "completeness": completeness,
        "recommendation": f"Add missing fields: {', '.join(missing)}"
    }
```

**The fix**:
```typescript
// ✅ GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
};
```

## Shannon Enhancement: Automated Anti-Pattern Scanning

**Pre-commit hook integration**:
```bash
#!/bin/bash
# hooks/pre-commit-test-quality.sh

# Scan all test files for anti-patterns
TEST_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.test\.')

for test_file in $TEST_FILES; do
  # Run Shannon anti-pattern detection
  ANTI_PATTERNS=$(shannon_detect_anti_patterns "$test_file")

  if [ -n "$ANTI_PATTERNS" ]; then
    echo "⚠️  ANTI-PATTERNS DETECTED in $test_file:"
    echo "$ANTI_PATTERNS" | jq -r '.[] | "  - \(.type): \(.severity) severity - \(.recommendation)"'

    HIGH_SEVERITY=$(echo "$ANTI_PATTERNS" | jq '[.[] | select(.severity > 0.70)] | length')

    if [ "$HIGH_SEVERITY" -gt 0 ]; then
      echo ""
      echo "❌ BLOCKING COMMIT: $HIGH_SEVERITY high-severity anti-patterns detected"
      echo "See: /shannon:skill testing-anti-patterns"
      exit 1
    fi
  fi
done
```

**Continuous monitoring**:
```python
# Track anti-pattern metrics over time
anti_pattern_metrics = {
    "project": project_name,
    "scan_date": ISO_timestamp,
    "total_tests": 234,
    "anti_patterns_found": 12,
    "by_severity": {
        "critical": 2,  # 0.90-1.00
        "high": 5,      # 0.70-0.89
        "medium": 3,    # 0.40-0.69
        "low": 2        # 0.00-0.39
    },
    "by_type": {
        "testing_mock_behavior": 4,
        "test_only_methods": 3,
        "over_mocking": 2,
        "incomplete_mocks": 3
    },
    "avg_severity": 0.63,
    "trend": "improving"  # vs last scan
}

serena.write_memory(f"test_quality/anti_patterns/{scan_id}", anti_pattern_metrics)
```

## Shannon Enhancement: Quantitative Test Quality Score

**Formula**:
```python
def calculate_test_quality_score(test_suite: dict) -> float:
    """
    Comprehensive test quality scoring
    Returns: 0.00 (poor) to 1.00 (excellent)
    """

    # Factors
    anti_pattern_penalty = sum([ap["severity"] for ap in test_suite["anti_patterns"]])
    mock_ratio = test_suite["mocked_tests"] / test_suite["total_tests"]
    integration_ratio = test_suite["integration_tests"] / test_suite["total_tests"]
    flakiness = test_suite["avg_flakiness_score"]

    # Score calculation
    base_score = 1.0
    base_score -= (anti_pattern_penalty / test_suite["total_tests"])  # Penalize anti-patterns
    base_score -= (mock_ratio * 0.2)      # Penalize excessive mocking
    base_score += (integration_ratio * 0.1)  # Reward integration tests
    base_score -= (flakiness * 0.3)       # Penalize flakiness

    return max(0.0, min(1.0, base_score))

# Example output
test_quality = {
    "overall_score": 0.78,  # GOOD (0.70-0.85)
    "grade": "B+",
    "total_tests": 234,
    "anti_patterns": 12,
    "mock_ratio": 0.35,
    "integration_ratio": 0.25,
    "avg_flakiness": 0.04,
    "recommendations": [
        "Reduce mock usage from 35% to <25%",
        "Fix 2 critical anti-patterns in auth tests",
        "Add 20 more integration tests for 30% coverage"
    ]
}
```

## TDD Prevents These Anti-Patterns

**Why TDD helps**:
1. **Write test first** → Forces you to think about what you're actually testing
2. **Watch it fail** → Confirms test tests real behavior, not mocks
3. **Minimal implementation** → No test-only methods creep in
4. **Real dependencies** → You see what the test actually needs before mocking

**If you're testing mock behavior, you violated TDD**.

## Quick Reference

| Anti-Pattern | Severity | Fix |
|--------------|----------|-----|
| Testing mock behavior | 0.95 | Test real component or unmock it |
| Test-only methods | 0.85 | Move to test utilities |
| Mocking without understanding | 0.75 | Understand dependencies, mock minimally |
| Incomplete mocks | 0.80 | Mirror real API completely |
| Tests as afterthought | 0.90 | TDD - tests first |

## Integration with Other Skills

**This skill works with**:
- **test-driven-development** - TDD prevents anti-patterns
- **condition-based-waiting** - Replaces timeout anti-patterns
- **verification-before-completion** - Verify test quality before commit

**Shannon integration**:
- **Serena MCP** - Track anti-pattern metrics over time
- **Sequential MCP** - Deep analysis of complex anti-patterns
- **Automated scanning** - Pre-commit hooks + CI integration

## The Bottom Line

**Mocks are tools to isolate, not things to test.**

Shannon's quantitative detection turns test quality from subjective to measurable.

Scan automatically. Score objectively. Fix systematically.
