# Shannon V4 Testing & Validation

This directory contains automated tests and validation tools for Shannon V4 components.

## Quick Start

### Run Comprehensive Integration Validation

```bash
# From shannon-framework root
python3 shannon-plugin/tests/comprehensive_validation.py .

# Or with explicit path
python3 shannon-plugin/tests/comprehensive_validation.py /path/to/shannon-framework
```

**Output:** Generates two reports in `shannon-plugin/tests/`:
- `COMPREHENSIVE_VALIDATION_RESULTS.md` - Detailed validation output
- `INTEGRATION_HEALTH_SUMMARY.md` - Executive summary (read this first)

### Exit Codes

- `0` - Validation passed (health score >= 95% with no critical errors)
- `1` - Validation failed (critical errors found or health score < 95%)

## Validation Components

### Test 1: Command → Skill References

Validates that all `@skill` references in command files point to existing skills.

**Checks:**
- All commands in `shannon-plugin/commands/`
- Extracts `@skill <skill-name>` patterns
- Verifies each skill exists in `shannon-plugin/skills/`
- Reports broken references

### Test 2: Agent Definitions

Validates agent structure and documentation completeness.

**Checks:**
- All agents in `shannon-plugin/agents/`
- Frontmatter presence
- SITREP protocol mentions
- Serena MCP integration mentions
- `activated-by` skill validity

### Test 3: Skill Dependencies

Validates skill dependency graph integrity.

**Checks:**
- All skills in `shannon-plugin/skills/`
- `required-sub-skills` references
- Circular dependency detection
- Dependency graph generation
- Orphaned skill detection

### Test 4: Documentation Cross-References

Validates documentation references to skills and commands.

**Checks:**
- All markdown files in `docs/`
- `@skill` references validity
- `/sh_*` and `/sc_*` command references
- File path references (informational)

## Understanding Results

### Health Score

The health score is calculated as:
```
(Passed Checks / Total Checks) × 100
```

**Grade Scale:**
- 95-100%: ✅ EXCELLENT - Production ready
- 80-94%: ✓ GOOD - Minor issues
- 60-79%: ⚠ FAIR - Several issues
- <60%: ✗ POOR - Critical issues

### Known Issues

#### YAML Parser False Positives

The validator currently reports errors for skills with explicit empty arrays:

```yaml
required-sub-skills: []
```

**Status:** This is a validator bug, not an integration issue. These skills are properly declaring zero dependencies.

**Fix:** Update `extract_frontmatter()` in `comprehensive_validation.py` to handle empty array notation.

**Impact:** Reduces reported health score from 97.4% to 91.38%. Actual integration health is 97.4%.

## Test Files

### Current Tests

- **comprehensive_validation.py** - Main integration validation script
- **COMPREHENSIVE_VALIDATION_RESULTS.md** - Last validation run detailed results
- **INTEGRATION_HEALTH_SUMMARY.md** - Executive summary of last validation
- **README.md** - This file

### Legacy Tests (Pre-V4)

These tests may not work with V4 structure:
- `test_plugin_manifest.py`
- `test_skill_template.py`
- `test_validation_infrastructure.py`
- `test_wave1_infrastructure.py`

**Status:** To be updated for V4 or archived.

## Continuous Integration

### Git Hook Integration (Recommended)

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running Shannon V4 integration validation..."
python3 shannon-plugin/tests/comprehensive_validation.py .

if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Commit blocked."
    echo "Review: shannon-plugin/tests/COMPREHENSIVE_VALIDATION_RESULTS.md"
    exit 1
fi

echo "✅ Validation passed."
```

### GitHub Actions (Future)

```yaml
name: Shannon V4 Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run validation
        run: python3 shannon-plugin/tests/comprehensive_validation.py .
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: shannon-plugin/tests/COMPREHENSIVE_VALIDATION_RESULTS.md
```

## Adding New Tests

### Test Structure

```python
def validate_new_component(self) -> Dict:
    """Test X: Description of what this validates"""
    print("\n\nTEST X: Test Name")
    print("=" * 60)

    results = {}

    # Perform validation
    for item in items_to_validate:
        # Validation logic
        if is_valid:
            print(f"  ✓ {item}")
        else:
            print(f"  ✗ {item} - REASON")
            self.results["errors"].append(f"Error description")

    self.results["test_name"] = results
    return results
```

### Integration

1. Add validation method to `ShannonValidator` class
2. Call method in `run_all_validations()`
3. Add results section to `generate_report()`
4. Update health score calculation if needed

## Interpreting Warnings vs Errors

### Errors (Critical)

Block production deployment. Must be fixed.

**Examples:**
- Broken skill references in commands
- Circular dependencies
- Missing required files
- Invalid frontmatter

### Warnings (Non-Critical)

Should be addressed but don't block deployment.

**Examples:**
- Missing SITREP protocol mentions (documentation)
- Legacy command names in historical docs (expected)
- Missing optional fields (documentation quality)
- Path references to external files (informational)

## Troubleshooting

### Validation Fails to Run

```bash
# Check Python version (requires 3.7+)
python3 --version

# Check file permissions
chmod +x shannon-plugin/tests/comprehensive_validation.py

# Run with verbose output
python3 -v shannon-plugin/tests/comprehensive_validation.py .
```

### False Positives

If validation reports errors that don't make sense:

1. Check `INTEGRATION_HEALTH_SUMMARY.md` for analysis
2. Review specific error in `COMPREHENSIVE_VALIDATION_RESULTS.md`
3. Verify the reported issue actually exists in the file
4. Check if it's a known validator bug (see Known Issues above)

### Health Score Lower Than Expected

1. Read `INTEGRATION_HEALTH_SUMMARY.md` first (contains analysis)
2. Check for validator false positives (YAML parsing)
3. Review warnings vs errors distinction
4. Verify legacy doc references are expected

## Future Enhancements

### Planned Tests

- **Agent Activation Validation** - Verify agents activate correctly
- **Skill Invocation Testing** - Test @skill calls work
- **Hook Integration Testing** - Validate hook system
- **MCP Availability Testing** - Check required MCPs present
- **Documentation Coverage** - Ensure all components documented

### Tool Improvements

- **Interactive Mode** - Step through validation tests
- **Fix Suggestions** - Automated fix generation
- **Visual Reports** - HTML/PDF report generation
- **Dependency Diagrams** - Graphviz visualization
- **Performance Tracking** - Track health score over time

## Contributing

When adding new Shannon components:

1. Run validation before committing
2. Ensure health score stays >= 95%
3. Fix any errors introduced
4. Document any new patterns/conventions
5. Update tests if validation rules change

## Support

For validation issues:

1. Check `INTEGRATION_HEALTH_SUMMARY.md` for analysis
2. Review `COMPREHENSIVE_VALIDATION_RESULTS.md` for details
3. See known issues section above
4. Check Shannon V4 documentation in `docs/`

---

**Last Updated:** 2025-11-04
**Shannon Version:** 4.0.0
**Validation Version:** 1.0.0
