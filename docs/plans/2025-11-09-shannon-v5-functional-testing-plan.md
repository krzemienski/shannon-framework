# Shannon Framework v5.0 - Functional Testing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use testing-claude-plugins-with-python-sdk skill for all SDK interactions.

**Goal**: Comprehensive functional testing of Shannon Framework plugin using Claude Agents SDK (Python)

**Approach**: Test Shannon plugin on 4 real specifications via SDK, iterate to improve plugin quality

**Test Specifications**: PRD Creator (18KB), Claude Code Expo (81KB), Repo Nexus (87KB), Shannon CLI (153KB)

**Timeline**: 30-40 hours across 7 phases

---

## Table of Contents

1. [Overview](#overview)
2. [Test Specifications](#test-specifications)
3. [Testing Architecture](#testing-architecture)
4. [Implementation Phases](#implementation-phases)
5. [Validation Strategy](#validation-strategy)
6. [Iteration and Improvement](#iteration-and-improvement)
7. [Success Criteria](#success-criteria)

---

## Overview

### What We're Building

Shannon Framework v5.0 adds **functional testing via Claude Agents SDK (Python)** to validate the plugin works correctly.

**Testing Approach**:
- Load Shannon plugin programmatically via SDK
- Execute Shannon commands (/sh_spec, /sh_wave, /shannon:prime, etc.)
- Validate outputs against expected results
- Test on 4 REAL specifications (not toy examples)
- Monitor long-running operations in real-time
- Iterate: test → find bugs → fix plugin → retest

**NOT**:
- pytest (use executable Python scripts instead)
- Mocking (test real plugin behavior)
- Unit tests (functional/integration tests only)

### Why This Matters

**Current State**: Shannon Framework v4.1 has NO automated testing
- ✅ Plugin works (manually verified)
- ❌ No regression testing (changes could break things)
- ❌ No validation on complex specs
- ❌ No proof 8D algorithm matches documentation

**v5.0 State**: Comprehensive functional test suite
- ✅ Test suite validates all commands
- ✅ Tests run on real, complex specifications
- ✅ Regression prevention (tests catch breaks)
- ✅ Continuous improvement (tests drive bug fixes)

---

## Test Specifications

### Specification 1: PRD Creator (Simplest)

**File**: `docs/ref/prd-creator-spec.md`
**Size**: 18 KB
**Description**: PRD creation web app (React + FastAPI + PostgreSQL)

**Expected Shannon Analysis**:
- Complexity: 0.40-0.50 (MODERATE)
- Domains: Frontend ~35%, Backend ~35%, Database ~20%, DevOps ~10%
- Execution: wave-based (2 waves)
- Timeline: 1-2 days
- MCPs: Context7, PostgreSQL, GitHub

**Test Focus**: Basic 8D algorithm correctness, balanced domain detection

---

### Specification 2: Claude Code Expo (Mobile)

**File**: `docs/ref/claude-code-expo-spec.md`
**Size**: 81 KB
**Description**: Claude Code mobile app (React Native + Express + WebSocket)

**Expected Shannon Analysis**:
- Complexity: 0.65-0.72 (COMPLEX)
- Domains: Mobile ~40%, Frontend ~30%, Backend ~20%, DevOps ~10%
- Execution: wave-based (3-4 waves)
- Timeline: 10-14 days
- MCPs: React Native, Puppeteer, Context7, Sequential

**Test Focus**: Mobile domain detection, WebSocket/real-time tech recognition

---

### Specification 3: Repo Nexus (Full-Stack iOS)

**File**: `docs/ref/repo-nexus-spec.md`
**Size**: 87 KB
**Description**: GitHub topic explorer iOS app (React Native + FastAPI + PostgreSQL + Redis)

**Expected Shannon Analysis**:
- Complexity: 0.68-0.75 (COMPLEX-HIGH)
- Domains: Mobile ~35%, Backend ~30%, Database ~20%, Frontend ~15%
- Execution: wave-based (3-4 waves)
- Timeline: 2 weeks
- MCPs: Context7, PostgreSQL, Redis, GitHub API

**Test Focus**: Multi-technology stack, GitHub API integration detection

---

### Specification 4: Shannon CLI (Meta-Circular)

**File**: `docs/ref/shannon-cli-spec.md`
**Size**: 153 KB
**Description**: Standalone Python CLI tool (Python + Claude SDK + Click + Rich)

**Expected Shannon Analysis**:
- Complexity: 0.72-0.78 (HIGH)
- Domains: Python ~60%, CLI ~20%, Testing ~20%
- Execution: wave-based (6 waves)
- Timeline: 72.5 hours
- MCPs: Context7 (Python SDK), Sequential

**Test Focus**: Meta-circular (Shannon analyzing Shannon), extreme detail handling

---

## Testing Architecture

### Directory Structure

```
shannon-framework/
├── shannon-plugin/                   # Plugin source (v4.1)
│   └── skills/testing-shannon-via-sdk/  # SDK testing skill (reference)
│
├── docs/ref/                         # Test specifications
│   ├── prd-creator-spec.md
│   ├── claude-code-expo-spec.md
│   ├── repo-nexus-spec.md
│   └── shannon-cli-spec.md
│
└── tests/                            # v5: SDK-based functional tests
    ├── README.md                     # How to run tests
    ├── requirements.txt              # claude-agent-sdk
    ├── run_all_tests.py             # Master test runner
    │
    ├── commands/                     # Test Shannon commands
    │   ├── test_sh_spec.py
    │   ├── test_sh_wave.py
    │   ├── test_shannon_prime.py
    │   ├── test_sh_checkpoint.py
    │   └── test_sh_discover_skills.py
    │
    ├── integration/                  # End-to-end workflows
    │   ├── test_full_workflow.py
    │   ├── test_four_specs.py       # All 4 specs tested
    │   └── test_shannon_cli_meta.py # Meta: Shannon builds shannon-cli
    │
    ├── lib/                          # Helper utilities
    │   ├── validators.py             # Validation functions (no pytest)
    │   ├── monitors.py               # Progress monitoring utilities
    │   └── fixtures.py               # Load test specs and expected results
    │
    └── fixtures/                     # Test data
        └── expected/
            ├── prd_creator_expected.json
            ├── claude_code_expo_expected.json
            ├── repo_nexus_expected.json
            └── shannon_cli_expected.json
```

### Test Script Pattern (No Pytest)

Every test is executable Python script:

```python
#!/usr/bin/env python3
"""
Test Shannon command
Run: python tests/commands/test_sh_spec.py
"""

import sys
import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    print("=" * 80)
    print("TEST: Shannon /sh_spec Command")
    print("=" * 80)

    # Load Shannon plugin
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}]
    )

    # Execute command
    spec_text = Path("docs/ref/prd-creator-spec.md").read_text()

    messages = []
    async for msg in query(prompt=f'/sh_spec "{spec_text}"', options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)
            print(".", end="", flush=True)  # Progress

    output = ''.join(messages)
    print()  # Newline

    # Validate (using lib/validators.py)
    from lib.validators import validate_complexity, validate_domains

    checks_passed = 0
    checks_total = 2

    if validate_complexity(output, min_val=0.40, max_val=0.50):
        checks_passed += 1

    if validate_domains(output):
        checks_passed += 1

    # Result
    print(f"\nResult: {checks_passed}/{checks_total} checks passed")

    return 0 if checks_passed == checks_total else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
```

---

## Implementation Phases

### Phase 1: Repository Preparation (Complete ✅)

**Tasks**:
- ✅ Remove shannon-cli artifacts (src/, pyproject.toml, etc.)
- ✅ Create Python SDK testing skill
- ✅ Install skill globally (~/.claude/skills/)
- ✅ Copy skill locally (shannon-plugin/skills/)
- ✅ Verify docs/ref/ has 4 test specs

**Status**: COMPLETE

---

### Phase 2: Test Infrastructure Setup (2-3 hours)

#### Task 2.1: Create Test Directory Structure

**Files to create**:
```
tests/
├── README.md
├── requirements.txt
├── run_all_tests.py
├── commands/
├── integration/
├── lib/
└── fixtures/expected/
```

**Command**:
```bash
mkdir -p tests/{commands,integration,lib,fixtures/expected}
```

#### Task 2.2: Create requirements.txt

**File**: `tests/requirements.txt`

```
claude-agent-sdk>=0.1.0
```

**Install**: `pip install -r tests/requirements.txt`

#### Task 2.3: Create Validation Helper Library

**File**: `tests/lib/validators.py` (~200 lines)

```python
"""
Validation helpers for Shannon testing (no pytest)
"""

import re

def validate_complexity(output: str, min_val: float, max_val: float, name: str = "Complexity") -> bool:
    """
    Extract and validate complexity score

    Args:
        output: Shannon command output
        min_val: Minimum expected complexity
        max_val: Maximum expected complexity
        name: Display name

    Returns:
        True if complexity in range
    """
    # Extract complexity from output
    patterns = [
        r'Complexity:\s*([0-9.]+)',
        r'complexity_score:\s*([0-9.]+)',
        r'([0-9]\.[0-9]{2})\s*/\s*1\.00',
    ]

    complexity = None
    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            complexity = float(match.group(1))
            break

    if complexity is None:
        print(f"  ❌ {name}: Could not extract from output")
        return False

    if min_val <= complexity <= max_val:
        print(f"  ✅ {name}: {complexity:.3f} in [{min_val}, {max_val}]")
        return True
    else:
        print(f"  ❌ {name}: {complexity:.3f} outside [{min_val}, {max_val}]")
        return False

def validate_domains(output: str, expected_sum: int = 100) -> bool:
    """
    Validate domains sum to expected total (default 100%)

    Args:
        output: Shannon output containing domain percentages
        expected_sum: Expected sum (default 100)

    Returns:
        True if domains sum correctly
    """
    # Extract domain percentages
    # Pattern: "Frontend: 35%" or "Frontend  35%"
    domain_pattern = r'(\w+):\s*(\d+)%'
    matches = re.findall(domain_pattern, output)

    if not matches:
        print(f"  ❌ Domains: No domain percentages found in output")
        return False

    domains = {domain: int(pct) for domain, pct in matches}
    total = sum(domains.values())

    if total == expected_sum:
        print(f"  ✅ Domains sum to {expected_sum}%")
        print(f"     {domains}")
        return True
    else:
        print(f"  ❌ Domains sum to {total}% (expected {expected_sum}%)")
        print(f"     {domains}")
        return False

def validate_contains(output: str, patterns: list, name: str = "Output") -> bool:
    """
    Validate output contains all patterns

    Returns: True if all patterns found
    """
    missing = []
    for pattern in patterns:
        if pattern not in output:
            missing.append(pattern)

    if not missing:
        print(f"  ✅ {name}: All {len(patterns)} patterns found")
        return True
    else:
        print(f"  ❌ {name}: Missing {len(missing)} patterns")
        for m in missing:
            print(f"     - '{m}'")
        return False
```

#### Task 2.4: Create Test Fixtures (Expected Results)

**File**: `tests/fixtures/expected/prd_creator_expected.json`

```json
{
  "spec_name": "PRD Creator",
  "spec_file": "docs/ref/prd-creator-spec.md",
  "complexity": {
    "min": 0.40,
    "max": 0.50,
    "interpretation": "moderate"
  },
  "domains": {
    "Frontend": {"min": 30, "max": 40},
    "Backend": {"min": 30, "max": 40}
  },
  "execution_strategy": "wave-based",
  "contains": ["8D", "Domain", "MCP", "Phase"]
}
```

*(Similar files for other 3 specs)*

**Validation Gate**: All infrastructure files created, validators work

---

### Phase 3: Core Command Tests (6-8 hours)

#### Task 3.1: Test /sh_spec Command

**File**: `tests/commands/test_sh_spec.py`

```python
#!/usr/bin/env python3
"""
Test Shannon's /sh_spec command on 4 real specifications
Validates 8D complexity analysis
"""

import sys
import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

# Import validators
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.validators import validate_complexity, validate_domains, validate_contains

# Test specs
TEST_SPECS = [
    {
        'name': 'PRD Creator',
        'file': 'docs/ref/prd-creator-spec.md',
        'complexity_range': (0.40, 0.50),
        'required_patterns': ['8D', 'Domain', 'Frontend', 'Backend']
    },
    {
        'name': 'Claude Code Expo',
        'file': 'docs/ref/claude-code-expo-spec.md',
        'complexity_range': (0.65, 0.72),
        'required_patterns': ['Mobile', 'React Native', 'WebSocket']
    },
    {
        'name': 'Repo Nexus',
        'file': 'docs/ref/repo-nexus-spec.md',
        'complexity_range': (0.68, 0.75),
        'required_patterns': ['Mobile', 'FastAPI', 'PostgreSQL']
    },
    {
        'name': 'Shannon CLI',
        'file': 'docs/ref/shannon-cli-spec.md',
        'complexity_range': (0.72, 0.78),
        'required_patterns': ['Python', 'SDK', 'wave-based']
    }
]

async def test_spec(spec_config: dict) -> bool:
    """Test Shannon on single specification"""

    print(f"\n{'='*80}")
    print(f"Testing: {spec_config['name']}")
    print(f"Spec: {spec_config['file']}")
    print('='*80)

    # Read spec
    spec_text = Path(spec_config['file']).read_text()
    print(f"Spec size: {len(spec_text):,} bytes")

    # Load Shannon plugin
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        model="claude-sonnet-4-5"
    )

    # Execute /sh_spec
    print("Executing /sh_spec...")

    messages = []
    tool_count = 0

    async for msg in query(prompt=f'/sh_spec "{spec_text}"', options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)
            print(".", end="", flush=True)
        elif msg.type == 'tool_call':
            tool_count += 1

    print(f" ({tool_count} tools)")

    output = ''.join(messages)

    # Validate
    print("\nValidation:")

    checks_passed = 0
    checks_total = 3

    # Check 1: Complexity
    min_c, max_c = spec_config['complexity_range']
    if validate_complexity(output, min_c, max_c):
        checks_passed += 1

    # Check 2: Domains sum to 100%
    if validate_domains(output):
        checks_passed += 1

    # Check 3: Required patterns
    if validate_contains(output, spec_config['required_patterns']):
        checks_passed += 1

    # Result
    passed = checks_passed == checks_total
    status = "✅ PASSED" if passed else "❌ FAILED"

    print(f"\n{status}: {checks_passed}/{checks_total} checks")

    return passed

async def main():
    """Test all 4 specifications"""

    print("=" * 80)
    print("SHANNON /sh_spec TEST: 4 Real Specifications")
    print("=" * 80)

    total = len(TEST_SPECS)
    passed_count = 0

    for spec_config in TEST_SPECS:
        if await test_spec(spec_config):
            passed_count += 1

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY: {passed_count}/{total} specs analyzed correctly")
    print('='*80)

    return 0 if passed_count == total else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
```

**Expected Cost**: ~$2.00 (4 specs analyzed)
**Expected Duration**: ~5-10 minutes

**Validation**: Run `python tests/commands/test_sh_spec.py`
- Should analyze all 4 specs
- Complexity scores should be in expected ranges
- Domains should sum to 100% for all

---

#### Task 3.2: Test /shannon:prime Command

**File**: `tests/commands/test_shannon_prime.py`

```python
#!/usr/bin/env python3
"""
Test Shannon's /shannon:prime session priming command
Should complete in <60 seconds
"""

import sys
import asyncio
import time
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    print("=" * 80)
    print("TEST: Shannon /shannon:prime Command")
    print("=" * 80)

    # Load Shannon
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}]
    )

    # Execute /shannon:prime
    print("\nExecuting /shannon:prime...")

    start = time.time()
    messages = []

    async for msg in query(prompt="/shannon:prime", options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)

    elapsed = time.time() - start
    output = ''.join(messages)

    # Validation
    print("\nValidation:")

    checks = []

    # Check 1: Completes in <60 seconds
    checks.append(('Duration', elapsed < 60, f"{elapsed:.1f}s"))

    # Check 2: Skills discovered
    checks.append(('Skills discovered', 'skill' in output.lower(), None))

    # Check 3: Mode detected
    checks.append(('Mode', 'mode' in output.lower() or 'fresh' in output.lower(), None))

    # Check 4: MCPs mentioned
    checks.append(('MCPs', 'mcp' in output.lower() or 'serena' in output.lower(), None))

    # Check 5: Forced reading
    checks.append(('Forced reading', 'forced' in output.lower() or 'reading' in output.lower(), None))

    # Print results
    passed = 0
    for check_name, check_passed, detail in checks:
        status = "✅" if check_passed else "❌"
        detail_str = f" ({detail})" if detail else ""
        print(f"  {status} {check_name}{detail_str}")

        if check_passed:
            passed += 1

    total = len(checks)
    result_status = "✅ PASSED" if passed == total else "❌ FAILED"

    print(f"\n{result_status}: {passed}/{total} checks")

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
```

**Expected Cost**: ~$0.05
**Expected Duration**: ~30 seconds

---

#### Task 3.3: Test /sh_wave Command

**File**: `tests/commands/test_sh_wave.py`

Tests wave planning (NOT execution - too expensive):
- Load spec
- Run /sh_spec then /sh_wave
- Validate wave plan generated
- Check wave count reasonable for complexity

---

#### Task 3.4: Test /sh_discover_skills

**File**: `tests/commands/test_sh_discover_skills.py`

Validates skill discovery works:
- Execute /sh_discover_skills
- Verify ~104 skills found
- Check skill categories (Project, User, Plugin)
- Validate specific Shannon skills mentioned

---

**Phase 2 Validation Gate**:
- All 5 command tests pass
- Can execute each Shannon command via SDK
- Output parsing works reliably

---

### Phase 4: Integration Tests (4-6 hours)

#### Task 4.1: Full Workflow Test

**File**: `tests/integration/test_full_workflow.py`

Complete Shannon workflow:
1. /shannon:prime
2. /sh_spec on PRD Creator
3. /sh_wave (generate plan)
4. Validate complete workflow works

**NOT executing waves** (too expensive for automated test)

---

#### Task 4.2: Four Specs Sequential Test

**File**: `tests/integration/test_four_specs.py`

Test all 4 specs in sequence:
- Analyze PRD Creator → validate
- Analyze Claude Code Expo → validate
- Analyze Repo Nexus → validate
- Analyze Shannon CLI → validate

Verifies Shannon handles variety of:
- Sizes (18KB → 153KB)
- Domains (web, mobile, CLI)
- Complexity (0.40 → 0.78)

---

#### Task 4.3: Meta-Circular Test

**File**: `tests/integration/test_shannon_cli_meta.py`

**Shannon analyzing Shannon**:
- Feed shannon-cli-spec.md to Shannon
- Shannon should recognize it's analyzing itself
- Validate: complexity ~0.72, Python/CLI domains, 6 waves

This is philosophically interesting and proves Shannon can handle meta-specs.

---

### Phase 5: Monitoring and Progress Utilities (2-3 hours)

#### Task 5.1: Progress Monitor

**File**: `tests/lib/monitors.py`

```python
"""
Progress monitoring for long-running Shannon operations
"""

import time
from datetime import datetime

class ProgressMonitor:
    """Monitor Shannon command execution in real-time"""

    def __init__(self, command_name: str):
        self.command = command_name
        self.start = time.time()
        self.tools = 0
        self.messages = 0

    def update(self, message):
        """Update from SDK message"""
        self.messages += 1
        elapsed = time.time() - self.start

        if message.type == 'tool_call':
            self.tools += 1
            print(f"[{elapsed:6.1f}s] Tool: {message.tool_name}")

        elif message.type == 'assistant' and message.content:
            preview = message.content[:60]
            if preview:
                print(f"[{elapsed:6.1f}s] {preview}...")

    def summary(self):
        """Print execution summary"""
        duration = time.time() - self.start

        print("\n" + "-" * 80)
        print(f"Command: {self.command}")
        print(f"Duration: {duration:.1f}s ({duration/60:.1f} min)")
        print(f"Messages: {self.messages}")
        print(f"Tools: {self.tools}")
        print("-" * 80)

# Usage
monitor = ProgressMonitor("/sh_spec")

async for msg in query(prompt="/sh_spec ...", options=options):
    monitor.update(msg)

monitor.summary()
```

#### Task 5.2: Cost Tracker

Track API costs across test runs:
- Budget controller
- Per-test cost tracking
- Total cost reporting

---

### Phase 6: Iterative Testing and Bug Fixing (10-15 hours)

**Process**: Run → Find Bugs → Fix → Retest

#### Iteration Cycle

**Step 1: Run all tests**
```bash
python tests/run_all_tests.py
```

**Step 2: Document failures**
- Which tests failed?
- What was expected vs actual?
- What's the root cause?

**Step 3: Fix Shannon plugin**
- Edit shannon-plugin files (commands, skills, core patterns)
- Example fixes:
  - Add missing domain keywords
  - Fix normalization algorithm
  - Update skill discovery glob patterns
  - Improve output formatting

**Step 4: Retest**
```bash
python tests/run_all_tests.py
```

**Step 5: Verify fix**
- Did test pass?
- Did fix break other tests?
- Document improvement

**Repeat** until all tests pass

#### Expected Bugs to Find

Based on testing, likely bugs:
1. Domain keywords incomplete (missing "FastAPI", "React Native", etc.)
2. Complexity band edge cases (is 0.50 MODERATE or COMPLEX?)
3. MCP recommendation thresholds (19% vs 20%)
4. Skill discovery glob patterns (missing subdirectories)
5. Output formatting inconsistencies

**Track in**: `docs/BUGS_FOUND_V5.md`

---

### Phase 7: Documentation and Release (2-3 hours)

#### Task 7.1: Update README

Add section:

```markdown
## Functional Testing (v5.0)

Shannon Framework v5.0 includes comprehensive functional testing via Claude Agents SDK.

### Running Tests

```bash
cd shannon-framework
pip install -r tests/requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."

# Run all tests
python tests/run_all_tests.py

# Run specific test
python tests/commands/test_sh_spec.py
```

### Test Specifications

Tests validate Shannon on 4 real specifications:
1. **PRD Creator** (18KB) - Web app, moderate complexity
2. **Claude Code Expo** (81KB) - Mobile app, complex
3. **Repo Nexus** (87KB) - Full-stack iOS, complex
4. **Shannon CLI** (153KB) - Meta-circular, high complexity

### Test Coverage

- 8D complexity analysis accuracy
- Domain normalization (sum to 100%)
- Command functionality (/sh_spec, /sh_wave, /shannon:prime)
- Skill discovery
- Wave planning

**Test Suite Cost**: ~$5-10 per complete run
```

#### Task 7.2: Create TESTING.md

**File**: `docs/TESTING.md`

Complete testing guide:
- How to run tests
- Test organization
- Adding new tests
- Interpreting results
- Cost management
- Iteration workflow

#### Task 7.3: Document Bugs and Fixes

**File**: `docs/BUGS_FOUND_V5.md`

Log all bugs found during testing:
- Bug description
- Test that found it
- Fix applied
- Commit hash

**Validation Gate**: Documentation complete, clear, accurate

---

## Validation Strategy

### Test Tiers

**Tier 1: Smoke Tests** (run on every commit, <$0.50, <2 min)
- test_shannon_prime.py (~$0.05, ~30s)
- test_sh_discover_skills.py (~$0.05, ~30s)

**Tier 2: Standard Tests** (run before PR, ~$3, ~10 min)
- test_sh_spec.py (all 4 specs, ~$2.00, ~8 min)
- test_sh_wave.py (wave planning, ~$0.50, ~2 min)
- test_sh_checkpoint.py (~$0.20, ~1 min)

**Tier 3: Integration Tests** (run before release, ~$8, ~30 min)
- test_full_workflow.py (~$2, ~10 min)
- test_four_specs.py (~$3, ~12 min)
- test_shannon_cli_meta.py (~$3, ~10 min)

**Total Suite**: ~$12 for complete run

### Validation Criteria

**Per Test**:
- Exit code 0 (success) or 1 (failure)
- Clear pass/fail reporting
- Specific failure messages

**Per Spec**:
- Complexity in expected range (±0.05 tolerance)
- Domains sum to exactly 100%
- Expected domains detected
- MCP recommendations reasonable

**Overall**:
- 100% pass rate (all tests pass)
- No crashes or exceptions
- Budget stays under limit

---

## Iteration and Improvement

### Bug Tracking

**When test fails**:
1. Capture failure details (expected vs actual)
2. Identify root cause (which plugin file/algorithm)
3. Document in BUGS_FOUND_V5.md
4. Assign priority (Critical/High/Medium/Low)

**Bug Template**:
```markdown
## Bug #N: Domain Keywords Incomplete

**Found by**: test_sh_spec.py (Repo Nexus spec)
**Symptom**: Shannon didn't detect FastAPI (Backend domain)
**Root cause**: "FastAPI" not in Backend domain keywords
**Fix**: Add "fastapi", "fast api" to SPEC_ANALYSIS.md line 487
**Commit**: abc1234
**Verified**: ✅ Repo Nexus now detects Backend correctly
**Status**: FIXED
```

### Iteration Workflow

```
┌─────────────────┐
│ Run test suite  │
└────────┬────────┘
         │
         ▼
    ┌─────────┐      No
    │ Pass?   ├────────┐
    └────┬────┘        │
         │ Yes         │
         │             ▼
         │      ┌──────────────┐
         │      │ Document bug │
         │      └──────┬───────┘
         │             │
         │             ▼
         │      ┌──────────────┐
         │      │ Fix plugin   │
         │      └──────┬───────┘
         │             │
         │             ▼
         │      ┌──────────────┐
         │      │ Commit fix   │
         │      └──────┬───────┘
         │             │
         └─────────────┘

Repeat until 100% pass
```

### Expected Iterations

**Iteration 1** (~10 tests pass): Initial baseline
- Find 5-10 bugs (missing keywords, edge cases)
- Fix obvious issues
- Re-run → 15 tests pass

**Iteration 2** (~15 tests pass): Refinement
- Find 3-5 subtle bugs (normalization, thresholds)
- Fix algorithms
- Re-run → 18 tests pass

**Iteration 3** (~18 tests pass): Edge cases
- Find 1-2 edge case bugs
- Polish algorithms
- Re-run → 20 tests pass (100%)

**Total iterations**: 3-5 expected

---

## Success Criteria

Shannon Framework v5.0 is complete when:

### 1. Test Suite Complete
- [ ] ≥15 Python test scripts (no pytest)
- [ ] Master test runner (run_all_tests.py)
- [ ] Helper library (validators.py, monitors.py)
- [ ] Test fixtures with expected results

### 2. All 4 Specs Pass
- [ ] PRD Creator analyzed correctly (0.40-0.50)
- [ ] Claude Code Expo analyzed correctly (0.65-0.72)
- [ ] Repo Nexus analyzed correctly (0.68-0.75)
- [ ] Shannon CLI analyzed correctly (0.72-0.78)

### 3. Commands Functional
- [ ] /sh_spec works (tested on 4 specs)
- [ ] /shannon:prime works (<60s)
- [ ] /sh_wave works (generates valid plans)
- [ ] /sh_discover_skills works (~104 skills found)
- [ ] /sh_checkpoint works

### 4. Quality Metrics
- [ ] 100% test pass rate
- [ ] Complexity accuracy: ±0.05 from expected
- [ ] Domain sum: 100% always (0 failures)
- [ ] Test cost: ≤$15 total

### 5. Bugs Fixed
- [ ] ≥5 bugs found and documented
- [ ] All critical bugs fixed
- [ ] Fixes verified with retests
- [ ] BUGS_FOUND_V5.md complete

### 6. Documentation
- [ ] README updated with testing section
- [ ] TESTING.md complete (how to run, interpret)
- [ ] BUGS_FOUND_V5.md complete (bugs + fixes)
- [ ] Skill installed (global + local)

### 7. Repository Clean
- [ ] shannon-framework = plugin only (no shannon-cli code)
- [ ] tests/ contains SDK-based tests only
- [ ] docs/ref/ has 4 test specs
- [ ] Git history clean

### 8. SDK Skill Validated
- [ ] Skill provides complete SDK guidance
- [ ] Tested by using it for Shannon testing
- [ ] No gaps found (complete reference)

---

## Task Summary

| Phase | Tasks | Duration | Cost | Validation |
|-------|-------|----------|------|------------|
| 1. Preparation | Repository cleanup, skill creation | Complete ✅ | $0 | Clean repo |
| 2. Infrastructure | Test structure, helpers, fixtures | 2-3h | $0 | Files created |
| 3. Command Tests | 5 command tests | 6-8h | ~$3 | Commands work |
| 4. Integration | 3 workflow tests | 4-6h | ~$8 | Workflows validated |
| 5. Monitoring | Progress utilities | 2-3h | $0 | Utilities work |
| 6. Iteration | Test → fix → retest cycles | 10-15h | ~$4 | 100% pass rate |
| 7. Documentation | README, TESTING.md, bugs | 2-3h | $0 | Docs complete |
| **Total** | **~35 tasks** | **28-38h** | **~$15** | **All criteria met** |

---

## Quick Reference

| Task | Command |
|------|---------|
| **Run all tests** | `python tests/run_all_tests.py` |
| **Run specific test** | `python tests/commands/test_sh_spec.py` |
| **Install dependencies** | `pip install -r tests/requirements.txt` |
| **Check test cost** | Review output cost tracking |
| **View bugs** | `cat docs/BUGS_FOUND_V5.md` |

---

## Next Steps

### After Plan Approval

1. **Execute Phase 2**: Create test infrastructure
2. **Execute Phase 3**: Implement command tests
3. **Run first iteration**: Find initial bugs
4. **Fix and iterate**: Until 100% pass
5. **Document and release**: v5.0 complete

**Estimated**: 28-38 hours, $15 budget

---

**Plan Status**: ✅ COMPLETE
**Ready for**: Implementation via phases
**Dependencies**: Python Agents SDK skill ✅, 4 test specs ✅, Clean repository ✅

