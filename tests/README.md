# Shannon Framework v5.0 - Test Suite

Complete functional verification suite for Shannon Framework using Claude Agents SDK (Python).

## Overview

Shannon v5.0 testing validates the entire framework on **4 real specifications**:

1. **PRD Creator** (18KB) - Web app specification
2. **Claude Code Expo** (81KB) - Mobile app specification
3. **Repo Nexus** (87KB) - Full-stack iOS app specification
4. **Shannon CLI** (153KB) - Meta-circular CLI tool specification

Tests execute Shannon commands programmatically via the Claude Agents SDK and verify outputs match expected results.

## Test Architecture

### Two-Tier Strategy

**Tier 1: Analysis Only** (`tier1_verify_analysis.py`)
- Tests `/sh_spec` on all 4 specifications
- Validates 8D complexity analysis
- Checks domain normalization
- **Does NOT build anything** (fast, cheap)
- Cost: ~$2-3 per run
- Duration: 5-10 minutes

**Tier 2: Full Build Verification** (4 separate scripts)
- Builds complete applications
- Uses `shannon-execution-verifier` skill
- Validates build outputs, file structure, functionality
- **Expensive** (builds real applications)
- Cost: ~$20-50 per spec
- Duration: 30-90 minutes per spec

### Test Files

```
tests/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
│
├── tier1_verify_analysis.py          # Tier 1: Analysis only
│
├── tier2_build_prd_creator.py        # Tier 2: Build PRD Creator
├── tier2_build_mobile_expo.py        # Tier 2: Build mobile app
├── tier2_build_repo_nexus.py         # Tier 2: Build Repo Nexus
├── tier2_build_shannon_cli.py        # Tier 2: Build Shannon CLI (meta)
│
└── run_all_verification.py           # Master runner (all tiers)
```

## Setup

### Prerequisites

1. **Python 3.9+** installed
2. **Anthropic API key** with sufficient credits
3. **Shannon Framework plugin** installed in Claude Code

### Installation

```bash
# Navigate to shannon-framework repository
cd /path/to/shannon-framework

# Install dependencies
pip install -r tests/requirements.txt

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Verify Setup

```bash
# Check Python version
python3 --version  # Should be 3.9+

# Check API key
echo $ANTHROPIC_API_KEY  # Should show your key

# Check plugin exists
ls -la shannon-plugin/  # Should show plugin files
```

## Running Tests

### Tier 1: Analysis Only (Recommended First)

Run analysis validation on all 4 specs:

```bash
python tests/tier1_verify_analysis.py
```

**Expected**:
- Duration: 5-10 minutes
- Cost: ~$2-3
- Output: Pass/fail for each spec
- Exit code: 0 (all pass) or 1 (any fail)

**What it validates**:
- Shannon analyzes specs correctly
- Complexity scores in expected ranges
- Domains sum to 100%
- Expected technologies detected
- MCP recommendations appropriate

### Tier 2: Full Build Verification (Expensive)

Build and verify individual applications:

```bash
# Build PRD Creator (simplest, ~30 min, ~$20)
python tests/tier2_build_prd_creator.py

# Build Claude Code Expo mobile app (~60 min, ~$35)
python tests/tier2_build_mobile_expo.py

# Build Repo Nexus full-stack (~60 min, ~$40)
python tests/tier2_build_repo_nexus.py

# Build Shannon CLI meta-circular (~90 min, ~$50)
python tests/tier2_build_shannon_cli.py
```

**What each validates**:
- Shannon executes `/sh_wave` successfully
- Complete application is built
- All files exist in correct structure
- Application runs without errors
- Functional requirements met

**Uses shannon-execution-verifier skill**:
- Loads from `.claude/skills/shannon-execution-verifier/`
- Comprehensive verification checklist
- Reports detailed results

### Run All Tests (Full Suite)

```bash
python tests/run_all_verification.py
```

**Warning**: This runs ALL tiers sequentially:
- Tier 1 (4 specs analysis)
- Tier 2 (4 complete builds)
- Total cost: ~$150-200
- Total duration: 4-6 hours

**Only run when**:
- Making major Shannon changes
- Validating release candidates
- You have budget and time

## Understanding Results

### Success Output

```
================================================================================
SHANNON v5.0 VERIFICATION SUITE
================================================================================

TIER 1: Specification Analysis
--------------------------------------------------------------------------------
✅ PRD Creator:        PASSED (complexity: 0.45, domains: 100%)
✅ Claude Code Expo:   PASSED (complexity: 0.68, domains: 100%)
✅ Repo Nexus:         PASSED (complexity: 0.72, domains: 100%)
✅ Shannon CLI:        PASSED (complexity: 0.75, domains: 100%)

TIER 1 SUMMARY: 4/4 passed

================================================================================
EXIT CODE: 0 (SUCCESS)
```

### Failure Output

```
❌ PRD Creator:        FAILED
   - Complexity: 0.35 (expected 0.40-0.50)
   - Domains: 98% (expected 100%)

EXIT CODE: 1 (FAILURE)
```

### Exit Codes

- `0` = All tests passed
- `1` = One or more tests failed

Scripts exit with proper codes for CI/CD integration.

## Test Specifications

### Spec 1: PRD Creator

- **File**: `docs/ref/prd-creator-spec.md`
- **Size**: 18 KB
- **Type**: Web application (React + FastAPI + PostgreSQL)
- **Complexity**: 0.40-0.50 (MODERATE)
- **Domains**: Frontend ~35%, Backend ~35%, Database ~20%
- **Build Time**: ~30 minutes
- **Test Focus**: Basic 8D algorithm correctness

### Spec 2: Claude Code Expo

- **File**: `docs/ref/claude-code-expo-spec.md`
- **Size**: 81 KB
- **Type**: Mobile app (React Native + Express + WebSocket)
- **Complexity**: 0.65-0.72 (COMPLEX)
- **Domains**: Mobile ~40%, Frontend ~30%, Backend ~20%
- **Build Time**: ~60 minutes
- **Test Focus**: Mobile domain detection, real-time tech

### Spec 3: Repo Nexus

- **File**: `docs/ref/repo-nexus-spec.md`
- **Size**: 87 KB
- **Type**: Full-stack iOS app (React Native + FastAPI + PostgreSQL + Redis)
- **Complexity**: 0.68-0.75 (COMPLEX-HIGH)
- **Domains**: Mobile ~35%, Backend ~30%, Database ~20%
- **Build Time**: ~60 minutes
- **Test Focus**: Multi-technology stack, GitHub API

### Spec 4: Shannon CLI

- **File**: `docs/ref/shannon-cli-spec.md`
- **Size**: 153 KB
- **Type**: Python CLI tool (Python + Claude SDK + Click + Rich)
- **Complexity**: 0.72-0.78 (HIGH)
- **Domains**: Python ~60%, CLI ~20%, Testing ~20%
- **Build Time**: ~90 minutes
- **Test Focus**: Meta-circular, extreme detail handling

## Verification Skill

Tier 2 tests use the `shannon-execution-verifier` skill:

**Location**: `.claude/skills/shannon-execution-verifier/SKILL.md`

**What it checks**:
1. Project structure matches specification
2. All required files exist
3. Dependencies installed correctly
4. Application runs without errors
5. Core functionality works
6. Tests pass (if present)
7. Build artifacts valid

**How it works**:
- Loaded programmatically via SDK
- Invoked after build completes
- Returns detailed verification report
- Exit code indicates pass/fail

## Cost Management

### Estimated Costs (Sonnet 4.5)

| Test | Type | Duration | Cost |
|------|------|----------|------|
| Tier 1 (all 4 specs) | Analysis | 5-10 min | $2-3 |
| PRD Creator build | Full | ~30 min | ~$20 |
| Claude Code Expo build | Full | ~60 min | ~$35 |
| Repo Nexus build | Full | ~60 min | ~$40 |
| Shannon CLI build | Full | ~90 min | ~$50 |
| **Complete suite** | **All** | **4-6 hours** | **~$150** |

### Cost Control Tips

1. **Start with Tier 1**: Run analysis tests first (cheap, fast)
2. **Test individually**: Only run Tier 2 for specs you're debugging
3. **Use dry-run mode**: Some tests support `--dry-run` flag
4. **Monitor API usage**: Check Anthropic console during runs
5. **Budget gates**: Tests abort if cost exceeds threshold

## Debugging Failed Tests

### Step 1: Identify Failure

```bash
python tests/tier1_verify_analysis.py
```

Look for `❌ FAILED` indicators.

### Step 2: Examine Output

Failed tests print:
- Expected values
- Actual values
- Difference/reason

Example:
```
❌ PRD Creator: Complexity FAILED
   Expected: 0.40-0.50
   Actual:   0.35
   Reason:   Score too low (missing domain keywords?)
```

### Step 3: Check Shannon Plugin

Common issues:
- **Missing domain keywords**: Edit `shannon-plugin/skills/spec-analysis/SPEC_ANALYSIS.md`
- **Algorithm bugs**: Check `shannon-plugin/skills/spec-analysis/` logic
- **Output format changes**: Update test validators

### Step 4: Fix and Retest

```bash
# Edit plugin files
vim shannon-plugin/skills/spec-analysis/SPEC_ANALYSIS.md

# Rerun test
python tests/tier1_verify_analysis.py

# If passed, commit fix
git add shannon-plugin/skills/spec-analysis/
git commit -m "fix: add missing domain keywords for X"
```

### Step 5: Document Bug

Add to `docs/BUGS_FOUND_V5.md`:

```markdown
## Bug #N: Missing FastAPI keyword

**Found by**: tier1_verify_analysis.py (Repo Nexus spec)
**Symptom**: Backend domain not detected
**Root cause**: "FastAPI" not in backend keyword list
**Fix**: Added "fastapi", "fast api" to keywords
**Commit**: abc1234
**Verified**: ✅ Test now passes
```

## CI/CD Integration

Tests are designed for CI/CD:

### GitHub Actions Example

```yaml
name: Shannon v5 Tests

on: [push, pull_request]

jobs:
  tier1-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r tests/requirements.txt

      - name: Run Tier 1 tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python tests/tier1_verify_analysis.py

      # Tier 2 tests: only on release branches (expensive)
      - name: Run Tier 2 tests
        if: github.ref == 'refs/heads/release'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python tests/run_all_verification.py --tier2-only
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run fast Tier 1 tests before allowing commit
python tests/tier1_verify_analysis.py

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Fix before committing."
    exit 1
fi

echo "✅ Tests passed."
exit 0
```

## Philosophy: NO MOCKS

Shannon v5 testing follows **NO MOCKS** philosophy:

**We test**:
- ✅ Real Shannon plugin
- ✅ Real Claude API calls
- ✅ Real specifications (18KB-153KB)
- ✅ Real builds (complete applications)

**We do NOT**:
- ❌ Mock Shannon responses
- ❌ Fake API calls
- ❌ Use toy specifications
- ❌ Skip actual builds

**Why**: We want to catch REAL bugs in REAL usage.

## Troubleshooting

### API Key Issues

```bash
# Verify key is set
echo $ANTHROPIC_API_KEY

# Set if missing
export ANTHROPIC_API_KEY="sk-ant-..."

# Add to shell profile for persistence
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r tests/requirements.txt

# Check claude-agent-sdk version
pip show claude-agent-sdk
```

### Plugin Not Found

```bash
# Verify plugin directory exists
ls -la shannon-plugin/

# Check plugin manifest
cat shannon-plugin/claude_plugin.json

# If missing, reinstall Shannon plugin in Claude Code
```

### Tests Hang

- Check internet connection
- Verify API key is valid
- Check Anthropic API status
- Increase timeout in script (default: 10 min)

### Out of Memory

Tier 2 builds use significant memory:
- Close other applications
- Increase system swap space
- Run one Tier 2 test at a time
- Use machine with ≥16GB RAM

## Contributing

### Adding New Tests

1. **Create test file**: `tests/my_new_test.py`
2. **Follow pattern**: Use existing tests as template
3. **Make executable**: `chmod +x tests/my_new_test.py`
4. **Add shebang**: `#!/usr/bin/env python3`
5. **Exit properly**: Return `0` (pass) or `1` (fail)
6. **Document**: Add section to this README

### Test Template

```python
#!/usr/bin/env python3
"""
Test: Description of what this tests

Usage: python tests/my_new_test.py
"""

import sys
import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    """Main test logic"""

    print("="*80)
    print("TEST: My New Test")
    print("="*80)

    # Load Shannon plugin
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./shannon-plugin"}],
        model="claude-sonnet-4-5"
    )

    # Execute test
    messages = []
    async for msg in query(prompt="/sh_spec ...", options=options):
        if msg.type == 'assistant':
            messages.append(msg.content)

    output = ''.join(messages)

    # Validate
    passed = validate_output(output)

    # Report
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"\n{status}")

    return 0 if passed else 1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
```

## Support

**Issues**: Open GitHub issue with:
- Test that failed
- Complete error output
- Environment details (Python version, OS, etc.)

**Questions**: See main Shannon documentation in `shannon-plugin/README.md`

---

**Shannon Framework v5.0**
**Test Suite Version**: 1.0.0
**Last Updated**: 2025-11-09
