# /sc:cleanup - Enhanced Cleanup Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:cleanup - Enhanced Cleanup Command

> **Enhanced from SuperClaude's `/cleanup` command with Shannon V3 systematic cleanup patterns, mandatory test validation, and Serena context preservation for project memory.**

## Command Identity

**Name**: /sc:cleanup
**Base Command**: SuperClaude's `/cleanup`
**Shannon Enhancement**: Systematic cleanup patterns, test validation enforcement, context preservation
**Primary Domain**: Code quality, technical debt reduction, refactoring, maintainability improvement
**Complexity Level**: Moderate (systematic multi-file cleanup with validation)

---

## Purpose Statement

The `/sc:cleanup` command transforms ad-hoc code cleanup into systematic, validated technical debt reduction. It provides:

- **Pattern-Based Cleanup**: Systematic application of cleanup patterns across codebase
- **Test Validation**: Mandatory test execution before and after cleanup changes
- **Context Preservation**: All cleanup operations tracked in Serena for project memory
- **Safe Refactoring**: Incremental changes with validation gates to prevent breakage
- **Quality Metrics**: Measurable improvements in code quality and maintainability

**SuperClaude Foundation**: Built on SuperClaude's refactorer persona with quality focus and systematic approach

**Shannon V3 Enhancements**:
- Structured cleanup pattern catalog with application guidelines
- Mandatory test validation before/after all cleanup operations
- Serena integration for cleanup history and context preservation
- Safe multi-file cleanup with rollback capability
- Automated detection of cleanup opportunities via pattern matching

---

## Shannon V3 Enhancements

### 1. Systematic Cleanup Patterns

**Pattern Catalog** (12 standard cleanup patterns):
```yaml
dead_code_elimination:
  description: "Remove unused functions, variables, imports, and files"
  detection: Grep for definitions + reference analysis
  risk: Low
  validation: Test suite must pass

duplicate_code_reduction:
  description: "Extract common code into reusable functions/modules"
  detection: Pattern matching for similar code blocks
  risk: Medium
  validation: Test suite + manual review

naming_consistency:
  description: "Standardize naming conventions across codebase"
  detection: Convention violations via pattern analysis
  risk: Low
  validation: Test suite + type checking

import_optimization:
  description: "Remove unused imports, organize import statements"
  detection: Import analysis + usage tracking
  risk: Very Low
  validation: Compilation/import checks

comment_cleanup:
  description: "Remove outdated comments, improve documentation"
  detection: TODO/FIXME/deprecated comment patterns
  risk: Very Low
  validation: Manual review

complexity_reduction:
  description: "Simplify complex functions, reduce nesting"
  detection: Cyclomatic complexity analysis
  risk: Medium
  validation: Test suite + behavior verification

dependency_cleanup:
  description: "Remove unused dependencies, update outdated packages"
  detection: Dependency analysis + usage tracking
  risk: Medium
  validation: Test suite + dependency resolution

formatting_standardization:
  description: "Apply consistent formatting via linters/formatters"
  detection: Linter violations
  risk: Very Low
  validation: Linter pass + test suite

error_handling_improvement:
  description: "Add missing error handling, improve exception patterns"
  detection: Error pattern analysis + uncaught exceptions
  risk: Low
  validation: Test suite + error scenario testing

type_annotation_addition:
  description: "Add missing type hints/annotations"
  detection: Type coverage analysis
  risk: Low
  validation: Type checker + test suite

console_log_removal:
  description: "Remove debugging console.log/print statements"
  detection: Pattern matching for debug statements
  risk: Very Low
  validation: Test suite pass

file_organization:
  description: "Reorganize files into logical directory structure"
  detection: Manual analysis + architectural patterns
  risk: Medium
  validation: Test suite + import resolution
```

### 2. Test Validation Framework

**Mandatory Testing Workflow**:
```
1. Pre-Cleanup Baseline
   ├─ Run test suite → Record baseline status
   ├─ Capture test output → Store in Serena
   └─ Calculate coverage → Baseline coverage metrics

2. Cleanup Execution
   ├─ Apply cleanup pattern → Incremental changes
   ├─ Track modifications → File-by-file change log
   └─ Create checkpoint → Rollback point if needed

3. Post-Cleanup Validation
   ├─ Run test suite → Compare against baseline
   ├─ Verify all tests pass → No regressions introduced
   ├─ Check coverage maintained → Coverage should not decrease
   └─ Generate validation report → Success/failure with evidence

4. Quality Gates
   ├─ All tests must pass → Blocking requirement
   ├─ No new warnings/errors → Quality regression check
   ├─ Coverage maintained → Baseline or improved
   └─ Manual review for medium+ risk → Human validation gate
```

**Test Validation Enforcement**:
- **Blocking**: Cleanup fails if tests don't pass post-cleanup
- **Evidence-Based**: All test results captured and stored
- **Rollback**: Automatic rollback if validation fails
- **Reporting**: Clear success/failure reporting with test evidence

### 3. Context Preservation via Serena

**Cleanup Memory Structure**:
```yaml
cleanup_session:
  session_id: "cleanup_[timestamp]_[scope_hash]"
  scope: "target files/directories"
  patterns_applied: ["pattern1", "pattern2"]

  pre_cleanup_state:
    files_modified: []
    test_status: "passing|failing"
    test_output: "baseline test results"
    coverage: "baseline coverage %"

  cleanup_operations:
    - pattern: "pattern_name"
      files: ["file1", "file2"]
      changes: "description of changes"
      risk_level: "low|medium|high"

  post_cleanup_state:
    test_status: "passing|failing"
    test_output: "validation test results"
    coverage: "post-cleanup coverage %"
    validation: "success|failure"

  quality_metrics:
    files_touched: 15
    lines_removed: 247
    complexity_reduced: "12%"
    warnings_eliminated: 8

  lessons_learned:
    what_worked: []
    challenges: []
    recommendations: []
```

**Serena Integration**:
- Store cleanup session history for future reference
- Track successful patterns for reuse
- Preserve rollback points for recovery
- Enable cross-session cleanup learning

### 4. Safe Multi-File Cleanup

**Incremental Change Strategy**:
```yaml
batch_processing:
  strategy: "process files in small batches"
  batch_size: 5-10 files per iteration
  validation: "run tests after each batch"
  rollback: "revert batch if validation fails"

risk_based_ordering:
  low_risk_first: "formatting, imports, comments"
  medium_risk_second: "naming, simple refactoring"
  high_risk_last: "structural changes, complexity reduction"

checkpoint_strategy:
  frequency: "after each batch"
  storage: "Serena memory + git commits"
  rollback: "automated on validation failure"
```

---

## Usage Patterns

### Basic Usage

```bash
# Clean up specific file
/sc:cleanup @src/utils/helpers.ts

# Clean up directory
/sc:cleanup @src/components/

# Clean up entire project with specific patterns
/sc:cleanup --patterns "dead_code,imports,formatting"

# Clean up with specific risk tolerance
/sc:cleanup @src/ --max-risk medium
```

### Advanced Usage

```bash
# Cleanup with explicit test command
/sc:cleanup @src/ --test-command "npm test"

# Cleanup with coverage threshold
/sc:cleanup @src/ --maintain-coverage 80

# Cleanup with dry-run mode
/sc:cleanup @src/ --dry-run

# Cleanup with auto-commit on success
/sc:cleanup @src/ --auto-commit "chore: cleanup src directory"

# Cleanup specific patterns only
/sc:cleanup @src/ --patterns "console_logs,dead_code" --exclude-patterns "complexity"
```

### Wave Integration

```bash
# Although cleanup is not wave-enabled, it can be part of wave workflows
# Example: cleanup phase in improvement wave
/sc:improve @src/ --wave-mode
# Wave 2: Cleanup dead code (automatic /sc:cleanup invocation)
```

---

## Execution Flow

### Phase 1: Discovery and Planning

**1.1 Target Identification**
```
Input: File path or directory scope
↓
Scan target scope:
├─ Identify all files in scope
├─ Determine file types (JS/TS/PY/etc)
├─ Calculate scope size (file count, LOC)
└─ Assess complexity level
```

**1.2 Pattern Detection**
```
For each cleanup pattern:
├─ Run pattern detection (Grep, Sequential)
├─ Identify opportunities (count, locations)
├─ Assess risk level (low/medium/high)
└─ Estimate impact (lines affected, files touched)

Output: Cleanup opportunity report
```

**1.3 Test Discovery**
```
Identify test suite:
├─ Detect test framework (Jest, pytest, etc)
├─ Find test command (package.json, Makefile)
├─ Locate test files (convention-based search)
└─ Verify test environment
```

**1.4 Cleanup Plan Generation**
```
Create cleanup plan:
├─ Selected patterns (auto or manual)
├─ File batches (grouped by risk/dependency)
├─ Validation gates (test checkpoints)
├─ Rollback strategy (checkpoint creation)
└─ Estimated time (based on scope + testing)

Present plan to user for confirmation
```

### Phase 2: Pre-Cleanup Baseline

**2.1 Baseline Test Execution**
```
Run test suite:
├─ Execute test command
├─ Capture output (stdout, stderr)
├─ Parse test results (pass/fail counts)
└─ Record baseline status

Store in Serena: pre_cleanup_test_baseline
```

**2.2 Baseline Quality Metrics**
```
Collect metrics:
├─ Test coverage % (if available)
├─ Linter warnings/errors count
├─ Type checking errors (if applicable)
├─ Code complexity metrics
└─ File/line counts

Store in Serena: pre_cleanup_quality_metrics
```

**2.3 Checkpoint Creation**
```
Create rollback point:
├─ Git commit current state (if in repo)
├─ Serena snapshot of file contents
└─ Record checkpoint ID for recovery
```

### Phase 3: Cleanup Execution

**3.1 Pattern Application Loop**
```
For each cleanup pattern in plan:
  ├─ Load pattern definition
  ├─ Identify target files for this pattern
  ├─ Group files into batches (5-10 files)
  │
  └─ For each batch:
      ├─ Apply cleanup changes (Edit/MultiEdit)
      ├─ Run quick validation (syntax check)
      ├─ Run test suite (if checkpoint reached)
      ├─ Validate results (tests pass?)
      │   ├─ Success: Continue to next batch
      │   └─ Failure: Rollback batch + report error
      └─ Create checkpoint (after successful validation)
```

**3.2 Change Tracking**
```
For each modification:
├─ Record file path
├─ Record line changes (added/removed)
├─ Record pattern applied
├─ Track cumulative impact
└─ Store in Serena memory
```

**3.3 Risk Management**
```
Risk-based execution order:
1. Very Low Risk (imports, formatting, comments)
   └─ Test validation: Every 10 files

2. Low Risk (console logs, dead code detection)
   └─ Test validation: Every 5 files

3. Medium Risk (naming, simple refactoring)
   └─ Test validation: Every 3 files

4. High Risk (complexity reduction, structural)
   └─ Test validation: After each file
```

### Phase 4: Post-Cleanup Validation

**4.1 Full Test Suite Execution**
```
Run complete test suite:
├─ Execute same test command as baseline
├─ Capture output (stdout, stderr)
├─ Parse test results (pass/fail counts)
└─ Compare against baseline

Validation Rule: All tests that passed before must still pass
```

**4.2 Quality Metrics Comparison**
```
Compare against baseline:
├─ Test coverage (must maintain or improve)
├─ Linter warnings (should decrease)
├─ Type errors (should maintain or improve)
├─ Complexity metrics (should improve)
└─ Generate comparison report
```

**4.3 Validation Decision**
```
Success Criteria:
✓ All baseline tests still pass
✓ No new test failures introduced
✓ Coverage maintained or improved
✓ No new linter errors
✓ No new type errors

Failure: Rollback to checkpoint + report issues
Success: Proceed to finalization
```

### Phase 5: Finalization and Reporting

**5.1 Serena Memory Update**
```
Store cleanup session:
├─ Session metadata (timestamp, scope, patterns)
├─ Pre/post test results
├─ Quality metric improvements
├─ Files modified + change details
├─ Lessons learned
└─ Recommendations for future cleanups
```

**5.2 Report Generation**
```markdown
# Cleanup Report: [Scope]

## Summary
- Patterns Applied: [list]
- Files Modified: [count]
- Lines Removed: [count]
- Test Status: [PASS/FAIL]
- Coverage: [baseline → post-cleanup]

## Changes by Pattern
[pattern_name]:
  - Files: [list]
  - Changes: [description]
  - Impact: [metrics]

## Validation Results
✓ All tests passing
✓ Coverage maintained: 85% → 87%
✓ Linter warnings: 24 → 12
✓ Complexity reduced: 15% average

## Quality Improvements
- [improvement 1]
- [improvement 2]

## Recommendations
- [future cleanup opportunity 1]
- [future cleanup opportunity 2]
```

**5.3 Git Integration (Optional)**
```
If --auto-commit flag:
├─ Stage all modified files
├─ Create commit with cleanup details
├─ Include cleanup report in commit message
└─ Push if --auto-push specified
```

---

## Sub-Agent Integration

### REFACTORING_EXPERT Agent

**Role**: Lead cleanup pattern application and code quality improvement

**Responsibilities**:
- Pattern detection and opportunity identification
- Safe refactoring strategy development
- Multi-file change orchestration
- Code quality assessment and improvement

**Tools**: Read, Edit, MultiEdit, Grep, Sequential

**Activation**: Primary agent for all cleanup operations

### QUALITY_ENGINEER Agent

**Role**: Test validation and quality gate enforcement

**Responsibilities**:
- Test suite execution and validation
- Coverage analysis and reporting
- Quality metric tracking and comparison
- Validation gate enforcement

**Tools**: Bash, Read, Grep, Serena

**Activation**: Validation phases and quality checks

---

## Output Format

### Cleanup Plan (User Confirmation)

```markdown
# Cleanup Plan: [scope]

## Detected Opportunities

**dead_code_elimination**: 15 occurrences
- Unused functions: 8
- Unused variables: 12
- Unused imports: 23
- Risk: Low | Impact: ~150 lines removed

**import_optimization**: 45 files
- Unorganized imports: 32 files
- Unused imports: 23 files
- Risk: Very Low | Impact: ~80 lines removed

**console_log_removal**: 18 occurrences
- Debug logs: 18
- Risk: Very Low | Impact: 18 lines removed

## Execution Strategy

**Batch 1** (Very Low Risk): Import optimization
- Files: 32 files in 4 batches
- Test checkpoint: After each batch

**Batch 2** (Low Risk): Dead code elimination
- Files: 15 files in 3 batches
- Test checkpoint: After each batch

**Batch 3** (Very Low Risk): Console log removal
- Files: 12 files in 2 batches
- Test checkpoint: After final batch

## Test Validation
- Test command: `npm test`
- Baseline: Will be established before cleanup
- Validation: After each batch completion

## Estimated Impact
- Total files modified: ~45 files
- Total lines removed: ~248 lines
- Estimated time: 8-12 minutes
- Risk level: Low

Proceed with cleanup? [Y/n]
```

### Cleanup Report (Final Output)

```markdown
# Cleanup Report: src/components/

## Session Summary
- Session ID: cleanup_20240930_143025_comp_hash
- Duration: 11 minutes 34 seconds
- Status: ✓ SUCCESS

## Patterns Applied

### 1. import_optimization
- Files modified: 32 files
- Imports removed: 23 unused
- Imports organized: 32 files
- Lines removed: 81 lines
- Test validation: ✓ PASSED

### 2. dead_code_elimination
- Files modified: 15 files
- Functions removed: 8 unused
- Variables removed: 12 unused
- Lines removed: 152 lines
- Test validation: ✓ PASSED

### 3. console_log_removal
- Files modified: 12 files
- Debug statements removed: 18
- Lines removed: 18 lines
- Test validation: ✓ PASSED

## Validation Results

**Test Suite**:
✓ All 247 tests passing (baseline: 247 passing)
✓ No new failures introduced
✓ Test execution time: 23.4s (baseline: 24.1s)

**Code Coverage**:
✓ Coverage maintained: 85.2% → 85.8% (+0.6%)
✓ No coverage regressions

**Quality Metrics**:
✓ Linter warnings: 24 → 12 (-50%)
✓ Complexity score: Avg 8.2 → 7.8 (-5%)
✓ Maintainability index: 68 → 72 (+6%)

## Impact Summary

**Files Modified**: 45 files
**Lines Removed**: 251 lines
**Code Quality**: Improved across all metrics
**Test Coverage**: Maintained with slight improvement
**Build Status**: ✓ Passing

## Quality Improvements

✓ Removed all unused imports and dead code
✓ Eliminated debug console.log statements
✓ Reduced codebase size by 251 lines
✓ Improved code maintainability by 6%
✓ Reduced linter warnings by 50%

## Context Preservation

✓ Cleanup session stored in Serena memory
✓ Rollback points created and preserved
✓ Quality metrics tracked for comparison
✓ Lessons learned captured for future cleanups

## Recommendations for Future Cleanup

1. **Complexity Reduction**: 8 functions with complexity >10 identified
   - Target: `handleUserSubmit()`, `processData()`, `validateInput()`
   - Recommended: Extract sub-functions, reduce nesting

2. **Type Annotation**: 15 functions missing type annotations
   - Target: `src/utils/` directory
   - Recommended: Add TypeScript type hints

3. **Error Handling**: 12 functions with incomplete error handling
   - Target: API interaction functions
   - Recommended: Add try-catch blocks, improve error messages

## Git Commit

✓ Changes committed: `chore: cleanup src/components directory`
```

---

## Examples

### Example 1: Basic File Cleanup

```bash
/sc:cleanup @src/utils/helpers.ts
```

**Output**:
```
🔍 Analyzing src/utils/helpers.ts...

Detected Opportunities:
✓ dead_code_elimination: 2 unused functions
✓ import_optimization: 4 unused imports
✓ console_log_removal: 3 debug statements

📋 Cleanup Plan:
- Remove 2 unused functions (28 lines)
- Remove 4 unused imports (4 lines)
- Remove 3 console.log statements (3 lines)
- Total impact: 35 lines removed

🧪 Running baseline tests...
✓ Tests passing: 247/247

🔧 Applying cleanup patterns...
✓ Removed unused imports (4 lines)
✓ Removed unused functions (28 lines)
✓ Removed console.log statements (3 lines)

🧪 Running validation tests...
✓ Tests passing: 247/247
✓ Coverage maintained: 85%

✅ Cleanup completed successfully!
- Lines removed: 35
- Quality improved: +4% maintainability
```

### Example 2: Directory Cleanup with Pattern Selection

```bash
/sc:cleanup @src/components/ --patterns "dead_code,imports"
```

**Output**:
```
🔍 Analyzing src/components/ (28 files)...

Selected Patterns:
✓ dead_code_elimination
✓ import_optimization

Detected Opportunities:
- Unused functions: 12 across 8 files
- Unused variables: 18 across 12 files
- Unused imports: 34 across 24 files

📋 Cleanup Plan:
Batch 1: Import optimization (24 files, 4 batches)
Batch 2: Dead code elimination (15 files, 3 batches)

Estimated time: 8-10 minutes
Proceed? [Y/n] Y

🧪 Establishing baseline...
✓ Tests: 247/247 passing
✓ Coverage: 85.2%

🔧 Executing cleanup...

Batch 1.1: Optimizing imports (6 files)...
✓ Modified 6 files, removed 8 unused imports
✓ Tests: 247/247 passing

Batch 1.2: Optimizing imports (6 files)...
✓ Modified 6 files, removed 9 unused imports
✓ Tests: 247/247 passing

[... continuing through all batches ...]

✅ Cleanup completed successfully!
📊 Full report generated
💾 Session saved to Serena memory
```

### Example 3: Cleanup with Dry Run

```bash
/sc:cleanup @src/ --dry-run
```

**Output**:
```
🔍 DRY RUN MODE - No changes will be made

Analyzing src/ (142 files)...

Detected Opportunities:
✓ dead_code_elimination: 45 occurrences (estimated 320 lines)
✓ import_optimization: 89 files (estimated 150 lines)
✓ console_log_removal: 34 occurrences (34 lines)
✓ naming_consistency: 23 violations (0 lines, refactoring)
✓ formatting_standardization: 67 files (auto-fix available)

Total Impact:
- Files to modify: ~95 files
- Lines to remove: ~504 lines
- Refactoring operations: 23
- Estimated time: 25-30 minutes
- Risk level: Low-Medium

Recommended Approach:
1. Start with very low risk patterns (imports, formatting)
2. Proceed to low risk (dead code, console logs)
3. Consider medium risk separately (naming consistency)

To execute: /sc:cleanup @src/ --patterns "imports,dead_code,console_logs"
```

---

## Integration Points

### SuperClaude Framework

**Persona Activation**:
- Primary: `refactorer` (code quality specialist)
- Secondary: `qa` (test validation)
- Support: `analyzer` (pattern detection)

**MCP Coordination**:
- Serena: Context preservation and cleanup history
- Sequential: Complex pattern detection and analysis
- Context7: Cleanup best practices and patterns

**Rules Compliance**:
- File Organization: Proper cleanup of temporary files
- Quality Standards: Enforce quality improvements
- Evidence-Based: All cleanup justified by metrics
- Validation Required: Mandatory test execution

### Wave System

**Not Wave-Enabled**: Cleanup is typically focused, scoped operation
**Wave Integration**: Can be invoked as part of larger wave workflows
**Example**: Improvement wave may include cleanup phase

### Shannon V3 Workflows

**Typical Usage Sequences**:
```
1. /sc:analyze → identify cleanup opportunities
2. /sc:cleanup → systematic cleanup execution
3. /sc:test → comprehensive validation

Or as part of improvement cycle:
1. /sc:improve --wave-mode
   → Wave 2: Cleanup (automatic /sc:cleanup)
```

---

## Quality Standards

### Test Validation Requirements

**Mandatory**:
- ✓ All baseline tests must pass post-cleanup
- ✓ No new test failures introduced
- ✓ Coverage must be maintained or improved
- ✓ Test execution within 10% of baseline time

**Recommended**:
- Test suite execution < 5 minutes (for rapid iteration)
- Coverage improvement goal: +2-5%
- Flaky test detection and reporting

### Risk Tolerance

**Very Low Risk**: No test validation between files (batch of 10)
**Low Risk**: Test validation every 5 files
**Medium Risk**: Test validation every 3 files
**High Risk**: Test validation after each file

### Quality Metrics

**Success Criteria**:
- Lines removed > 0
- Maintainability index improved
- Linter warnings decreased
- Test coverage maintained
- No new bugs introduced

---

## Error Handling

### Common Failure Scenarios

**Test Failures Post-Cleanup**:
```
Action: Automatic rollback to last checkpoint
Report: Failed cleanup batch + test output
User Action: Review test failures, adjust cleanup scope
```

**Coverage Regression**:
```
Action: Warn user, request manual review
Options: Proceed with warning OR rollback
User Action: Investigate coverage loss, add tests if needed
```

**Linter Errors Introduced**:
```
Action: Automatic rollback to last checkpoint
Report: Linter errors + affected files
User Action: Review cleanup pattern, adjust application
```

**Git Conflict on Commit**:
```
Action: Leave changes uncommitted
Report: Conflict details + resolution steps
User Action: Resolve conflicts manually, commit when ready
```

### Recovery Mechanisms

**Checkpoint Rollback**:
- Serena memory restoration
- Git reset to checkpoint commit (if applicable)
- File content restoration from snapshot

**Partial Success Handling**:
- Complete successful batches remain applied
- Failed batch rolled back
- Report indicates partial completion + next steps

---

## Performance Considerations

**Execution Time Estimation**:
```
Small cleanup (1-5 files): 2-4 minutes
Medium cleanup (5-20 files): 5-12 minutes
Large cleanup (20-50 files): 15-30 minutes
Very large cleanup (50+ files): 30+ minutes
```

**Optimization Strategies**:
- Batch processing reduces test execution overhead
- Risk-based ordering frontloads quick wins
- Incremental validation enables early failure detection
- Parallel pattern detection (multiple Grep calls)

**Resource Usage**:
- Test execution typically dominates execution time
- Serena memory storage: ~1-5MB per cleanup session
- Git checkpoint storage: Minimal (delta compression)

---

## Best Practices

### When to Use /sc:cleanup

**Good Candidates**:
- After major feature completion (cleanup technical debt)
- Before code reviews (improve code quality)
- Regular maintenance (quarterly cleanup cycles)
- After dependency updates (cleanup deprecated patterns)
- When linter warnings accumulate
- When test suite slows down (remove dead test code)

**Poor Candidates**:
- During active feature development (wait for stability)
- Without test suite (too risky without validation)
- On unfamiliar codebase (understand first)
- Under time pressure (cleanup requires validation time)

### Preparation Checklist

✓ Test suite exists and passes
✓ Baseline coverage known
✓ Git repository clean (or willing to checkpoint)
✓ Time allocated for validation (plan for 2x estimated time)
✓ Scope clearly defined (file/directory boundaries)
✓ Risk tolerance assessed (what patterns are safe?)

### Post-Cleanup Actions

✓ Review cleanup report for completeness
✓ Commit changes with detailed message
✓ Update documentation if structure changed
✓ Share improvements with team (knowledge transfer)
✓ Schedule next cleanup cycle (proactive maintenance)

---

## Version History

**Shannon V3 Initial Release**: Enhanced from SuperClaude `/cleanup`
- Added: Systematic cleanup pattern catalog
- Added: Mandatory test validation framework
- Added: Serena context preservation
- Added: Risk-based batch processing
- Added: Comprehensive reporting and metrics

**Future Enhancements**:
- AI-powered pattern detection (ML-based code smell detection)
- Automated pattern application confidence scoring
- Cross-project cleanup pattern learning
- Integration with CI/CD for continuous cleanup
- Performance profiling for cleanup impact measurement