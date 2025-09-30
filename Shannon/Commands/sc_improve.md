---
name: sc:improve
command: /sc:improve
description: "Evidence-based code enhancement with wave-based iterative improvement, test validation, quality metrics tracking, and systematic refinement"
category: command
complexity: advanced
triggers: [improve, refine, enhance, polish, optimize, cleanup]
mcp_servers: [serena, sequential, context7, morphllm]
personas: [refactorer, qa, performance, architect]
auto_activate: false
base_command: /improve
enhancements: [wave_iteration, test_validation, quality_metrics, evidence_tracking]
---

# /sc:improve - Enhanced Code Improvement Command

> **Shannon V3 Enhancement**: SuperClaude's `/improve` command enhanced with wave-based iterative improvement, mandatory test validation after each wave, quality metrics tracking, and REFACTORER + QA sub-agent coordination.

## Purpose Statement

Evidence-based code enhancement with systematic refinement and quality validation:

- **Wave-Based Iterative Improvement** - Multiple improvement passes with validation gates between waves
- **Test Validation Mandate** - All improvements verified with functional tests before proceeding
- **Quality Metrics Tracking** - Measurable improvement across complexity, maintainability, performance
- **Context Preservation** - All improvement decisions and rationale saved to Serena MCP
- **Evidence-Based Refinement** - Every change justified with measurements and validation
- **Intelligent Persona Activation** - Auto-selects REFACTORER (primary), QA (validation), domain specialists
- **MCP Coordination** - Sequential for analysis, Morphllm for pattern edits, Context7 for best practices
- **Iterative Excellence** - Continue improving until quality thresholds met or diminishing returns

**What Makes This Different**: SuperClaude's `/improve` makes single-pass improvements. Shannon's `/sc:improve` orchestrates multiple waves of systematic refinement with test validation between each wave, quality metric tracking, and evidence-based decision making.

## Shannon V3 Enhancements Over SuperClaude

### 1. Wave-Based Iterative Improvement (NEW)
**SuperClaude**: Single improvement pass, manual iteration
**Shannon**: Automated multi-wave refinement with validation gates

```yaml
improvement_waves:
  wave_1_analysis:
    - REFACTORER → Identify improvement opportunities
    - Sequential → Complexity and quality analysis
    - QA → Test coverage assessment
    - write_memory("improvement_baseline", metrics)

  wave_2_implementation:
    - REFACTORER → Apply improvements (complexity, readability)
    - Edit/MultiEdit → Code modifications
    - write_memory("wave_2_changes", diff)

  wave_3_validation:
    - QA → Execute functional tests
    - Performance → Benchmark validation
    - write_memory("wave_2_results", test_results)

  wave_4_iteration:
    - IF metrics_improved AND tests_pass → Continue to wave_5
    - IF diminishing_returns → Conclude with report
    - IF tests_fail → Rollback and adjust approach
```

### 2. Test Validation Mandate (NEW)
**SuperClaude**: Testing approach undefined
**Shannon**: Mandatory functional testing after every improvement wave

```yaml
validation_requirements:
  after_each_wave:
    - Execute ALL existing tests
    - Verify no regressions introduced
    - Validate performance metrics stable or improved
    - Block next wave if ANY test fails

  test_types:
    - Functional tests (Playwright for web)
    - Integration tests (real dependencies)
    - Performance benchmarks (before/after)
    - NO mock-based tests accepted

  failure_handling:
    - Rollback changes immediately
    - Analyze root cause
    - Adjust improvement strategy
    - Re-attempt with refined approach
```

### 3. Quality Metrics Tracking (NEW)
**SuperClaude**: Qualitative improvement assessment
**Shannon**: Quantitative metrics with evidence-based validation

```yaml
tracked_metrics:
  complexity:
    - Cyclomatic complexity (before/after)
    - Cognitive complexity (before/after)
    - Nesting depth reduction
    - Target: 20% complexity reduction

  maintainability:
    - Code duplication percentage
    - Function length distribution
    - Naming consistency score
    - Target: Maintainability index >70

  performance:
    - Execution time (microseconds)
    - Memory allocation (bytes)
    - API response times (ms)
    - Target: No performance regression

  test_coverage:
    - Line coverage percentage
    - Branch coverage percentage
    - Critical path coverage
    - Target: Maintain or improve coverage

  evidence_storage:
    - write_memory("metrics_baseline", initial_state)
    - write_memory("metrics_wave_N", current_state)
    - write_memory("metrics_final", end_state)
```

### 4. REFACTORER + QA Coordination (NEW)
**SuperClaude**: Generic improvement
**Shannon**: Specialized sub-agents with complementary expertise

```yaml
agent_coordination:
  refactorer_role:
    - Primary improvement driver
    - Code quality expert
    - Pattern recognition specialist
    - Simplicity advocate

  qa_role:
    - Validation gatekeeper
    - Test execution specialist
    - Quality assurance advocate
    - Regression prevention

  coordination_pattern:
    - REFACTORER proposes improvements
    - QA validates with tests
    - Iterate until quality thresholds met
    - Both agents write_memory() for context
```

## Usage Patterns

**Basic Usage**:
```
/sc:improve [target]
/sc:improve src/auth/login.js
/sc:improve @components/UserProfile.tsx
/sc:improve "authentication module"
```

**With Focus Area**:
```
/sc:improve [target] --focus performance
/sc:improve [target] --focus security
/sc:improve [target] --focus maintainability
/sc:improve [target] --focus readability
```

**With Iteration Control**:
```
/sc:improve [target] --iterations 3
/sc:improve [target] --until-threshold
/sc:improve [target] --max-waves 5
```

**With Scope Control**:
```
/sc:improve [target] --scope file
/sc:improve [target] --scope module
/sc:improve [target] --scope system
```

**With Quality Thresholds**:
```
/sc:improve [target] --complexity-max 10
/sc:improve [target] --coverage-min 80
/sc:improve [target] --performance-budget 100ms
```

## Execution Flow with Iterative Waves

### Phase 1: Baseline Analysis
**Objective**: Establish current state and improvement opportunities

```yaml
step_1_context_loading:
  action: read_memory("project_context")
  purpose: "Understand project patterns and history"

step_2_target_analysis:
  tools: [Read, Grep, Serena]
  actions:
    - Read target files completely
    - find_symbol() for code structure
    - search_for_pattern() for anti-patterns
  output: "Target code understanding"

step_3_metrics_baseline:
  measurements:
    - Cyclomatic complexity per function
    - Code duplication percentage
    - Function length distribution
    - Nesting depth analysis
    - Performance benchmarks
  tools: [Sequential, Bash]
  storage: write_memory("improvement_baseline", metrics)

step_4_opportunity_identification:
  agent: REFACTORER
  analysis:
    - Complexity hotspots
    - Duplication candidates
    - Naming inconsistencies
    - Pattern violations
    - Performance bottlenecks
  output: "Prioritized improvement list"
  storage: write_memory("improvement_opportunities", list)

step_5_strategy_planning:
  agent: REFACTORER + QA
  planning:
    - Estimate improvement waves needed
    - Identify dependencies between improvements
    - Plan validation approach for each wave
    - Set quality thresholds
  output: "Wave execution plan"
  storage: write_memory("improvement_plan", plan)
```

### Phase 2: Wave Execution Loop
**Objective**: Apply improvements iteratively with validation gates

```yaml
wave_loop:
  for each wave in plan:

    step_1_wave_preparation:
      action: read_memory("metrics_wave_N-1")
      purpose: "Understand previous wave results"
      agent: REFACTORER

    step_2_improvement_application:
      agent: REFACTORER
      tools: [Edit, MultiEdit, Morphllm]
      actions:
        - Apply targeted improvements from wave plan
        - Maintain code style consistency
        - Preserve functionality
        - Document changes
      validation: "No syntax errors introduced"
      storage: write_memory("wave_N_changes", diff)

    step_3_immediate_validation:
      agent: QA
      tools: [Bash, Sequential]
      actions:
        - Lint checks (eslint, pylint, etc.)
        - Type validation (tsc, mypy, etc.)
        - Syntax validation
      gate: "MUST pass before testing"

    step_4_test_execution:
      agent: QA
      tools: [Bash, Playwright]
      actions:
        - Execute ALL existing tests
        - Run performance benchmarks
        - Measure coverage
        - Check for regressions
      validation: "100% pass rate required"
      storage: write_memory("wave_N_test_results", results)

    step_5_metrics_measurement:
      agent: REFACTORER + QA
      tools: [Sequential, Bash]
      measurements:
        - Complexity delta from baseline
        - Performance delta from baseline
        - Coverage delta from baseline
        - Maintainability improvement
      storage: write_memory("wave_N_metrics", metrics)

    step_6_wave_decision:
      decision_logic: |
        IF all_tests_pass AND metrics_improved:
          - Continue to next wave
          - Update baseline with current metrics
        ELIF all_tests_pass AND metrics_neutral:
          - Assess diminishing returns
          - Continue if more opportunities exist
        ELIF tests_fail:
          - ROLLBACK all wave changes immediately
          - Analyze failure root cause
          - Adjust strategy
          - Retry wave with refined approach
        ELIF metrics_degraded:
          - ROLLBACK changes
          - Re-evaluate improvement strategy

      storage: write_memory("wave_N_decision", decision)
```

### Phase 3: Convergence & Reporting
**Objective**: Conclude improvements and document results

```yaml
step_1_convergence_check:
  conditions:
    - quality_thresholds_met: true
    - diminishing_returns: true
    - max_waves_reached: true
  decision: "Conclude improvement session"

step_2_final_validation:
  agent: QA
  actions:
    - Complete test suite execution
    - Full coverage report
    - Performance regression check
    - Security scan
  requirement: "ALL validations MUST pass"

step_3_metrics_comparison:
  agent: REFACTORER
  tools: [Sequential]
  comparison:
    baseline: read_memory("improvement_baseline")
    final: current_metrics
    delta: calculate_improvement()
  output: "Evidence-based improvement report"

step_4_documentation:
  agent: REFACTORER
  outputs:
    - Improvement summary with metrics
    - Changes made per wave
    - Test validation evidence
    - Recommendations for future
  storage: write_memory("improvement_complete", report)

step_5_context_preservation:
  actions:
    - write_memory("final_state", code_snapshot)
    - write_memory("lessons_learned", insights)
    - write_memory("quality_evolution", metric_timeline)
  purpose: "Enable future improvements to build on this work"
```

## Sub-Agent Integration

### REFACTORER (Primary Driver)
**Activation**: Automatic when /sc:improve invoked

**Responsibilities**:
- Identify improvement opportunities through code analysis
- Prioritize improvements by impact and risk
- Apply code transformations systematically
- Maintain simplicity and readability focus
- Document improvement rationale

**Expertise**:
- Complexity reduction patterns
- Code duplication elimination
- Naming consistency enforcement
- Pattern recognition and application
- Technical debt assessment

**Tools Used**:
- Sequential MCP (complexity analysis)
- Context7 MCP (best practice patterns)
- Morphllm MCP (bulk pattern edits)
- Edit/MultiEdit (targeted improvements)
- Serena MCP (context preservation)

**Output Format**:
```yaml
wave_N_improvements:
  complexity_reductions:
    - "Extracted nested conditionals to guard clauses"
    - "Simplified cyclomatic complexity from 15 to 8"

  duplication_removal:
    - "Extracted common validation logic to shared utility"
    - "Reduced code duplication from 35% to 12%"

  naming_improvements:
    - "Renamed ambiguous variables for clarity"
    - "Applied consistent naming conventions"

  pattern_applications:
    - "Applied Strategy pattern to replace switch statements"
    - "Implemented Guard Clauses for early returns"
```

### QA (Validation Gatekeeper)
**Activation**: Automatic after each improvement wave

**Responsibilities**:
- Execute comprehensive test suites
- Validate no regressions introduced
- Measure quality metrics evolution
- Block progression if validation fails
- Provide evidence for improvement claims

**Expertise**:
- Functional testing with real dependencies
- Performance benchmarking
- Test coverage analysis
- Regression detection
- Quality gate enforcement

**Tools Used**:
- Bash (test execution)
- Playwright MCP (web functional tests)
- Sequential MCP (test analysis)
- Serena MCP (result storage)

**Output Format**:
```yaml
wave_N_validation:
  test_execution:
    total_tests: 247
    passed: 247
    failed: 0
    duration: "12.4s"
    status: "✅ ALL PASS"

  performance_benchmarks:
    api_response_time:
      baseline: "145ms"
      current: "142ms"
      delta: "-3ms (2% improvement)"

    memory_usage:
      baseline: "84MB"
      current: "82MB"
      delta: "-2MB (2.4% improvement)"

  coverage_report:
    line_coverage: "87.3% (unchanged)"
    branch_coverage: "79.1% (+1.2%)"
    status: "✅ MAINTAINED"

  gate_status: "✅ PASS - Proceed to next wave"
```

### Performance Specialist (Conditional)
**Activation**: When `--focus performance` specified

**Responsibilities**:
- Identify performance bottlenecks
- Propose optimization strategies
- Validate performance improvements
- Ensure no regressions

**Expertise**:
- Algorithm complexity analysis
- Memory optimization
- Caching strategies
- Database query optimization

### Security Specialist (Conditional)
**Activation**: When security issues detected

**Responsibilities**:
- Identify security vulnerabilities
- Propose secure alternatives
- Validate security improvements
- Ensure compliance with security standards

**Expertise**:
- OWASP Top 10
- Input validation patterns
- Authentication/authorization best practices
- Secure coding standards

## Output Format

### Improvement Summary Report
```markdown
# Code Improvement Report

## 📊 Executive Summary
**Target**: [file/module path]
**Waves Executed**: [N waves]
**Total Duration**: [time]
**Overall Status**: ✅ Success / ⚠️ Partial / ❌ Failed

## 📈 Quality Metrics Evolution

### Complexity Reduction
- **Baseline**: Cyclomatic complexity avg 12.4
- **Final**: Cyclomatic complexity avg 8.1
- **Improvement**: -34.7% complexity reduction
- **Evidence**: [link to metrics file]

### Code Duplication
- **Baseline**: 28% duplication
- **Final**: 9% duplication
- **Improvement**: -68% duplication reduction
- **Evidence**: [detailed duplication report]

### Maintainability Index
- **Baseline**: 62 (moderate)
- **Final**: 78 (good)
- **Improvement**: +25.8% maintainability increase
- **Evidence**: [maintainability calculation]

### Performance Benchmarks
- **API Response Time**: 145ms → 142ms (-2.1%)
- **Memory Usage**: 84MB → 82MB (-2.4%)
- **CPU Utilization**: 23% → 21% (-8.7%)
- **Evidence**: [benchmark results]

## 🔄 Wave-by-Wave Summary

### Wave 1: Complexity Reduction
**Changes Applied**:
- Extracted nested conditionals to guard clauses (auth.js:45-67)
- Simplified branching logic with early returns (validation.js:23-41)
- Reduced function cyclomatic complexity from 15 to 8

**Validation Results**:
- Tests: ✅ 247/247 passed
- Performance: ✅ No regression
- Coverage: ✅ 87.3% maintained

**Metrics Impact**:
- Complexity: -40% in modified functions
- Readability: Significant improvement

### Wave 2: Duplication Elimination
**Changes Applied**:
- Extracted common validation logic to utils/validators.js
- Consolidated error handling patterns
- Created shared authentication utilities

**Validation Results**:
- Tests: ✅ 247/247 passed
- Performance: ✅ 2% improvement
- Coverage: ✅ 88.1% (+0.8%)

**Metrics Impact**:
- Duplication: -68% project-wide
- Maintainability: +15 index points

### Wave 3: Pattern Refinement
**Changes Applied**:
- Applied Strategy pattern to replace switch statements
- Implemented consistent naming conventions
- Standardized error handling approach

**Validation Results**:
- Tests: ✅ 247/247 passed
- Performance: ✅ Stable
- Coverage: ✅ 88.1% maintained

**Metrics Impact**:
- Consistency: 95% naming adherence
- Pattern compliance: 100%

## 🧪 Testing Evidence

### Functional Tests
```bash
$ npm test
✅ 247 tests passed (0 failed)
⏱️  Duration: 12.4s
📊 Coverage: 88.1% lines, 79.1% branches
```

### Performance Benchmarks
```bash
$ npm run benchmark
API Response Time: 142ms (baseline: 145ms) ✅
Memory Usage: 82MB (baseline: 84MB) ✅
Throughput: 1,240 req/s (baseline: 1,205 req/s) ✅
```

## 📋 Files Modified
- ✏️ `src/auth/authentication.js` (complexity reduction)
- ✏️ `src/auth/validation.js` (guard clauses)
- ✏️ `src/utils/validators.js` (duplication elimination)
- ✏️ `src/middleware/error-handler.js` (pattern application)
- ✏️ `src/config/security.js` (naming consistency)

## 🎯 Recommendations

### Future Improvements
1. Consider extracting authentication logic to separate service layer
2. Opportunity for caching optimization in user lookup
3. Database query optimization potential in audit logging

### Maintenance Notes
- Maintain current naming conventions in new code
- Continue using guard clause pattern for early returns
- Leverage shared validators for all input validation

## 💾 Context Preserved
All improvement decisions, metrics, and rationale stored in Serena MCP:
- `memory://improvement_baseline` - Initial state
- `memory://wave_1_results` - First wave outcomes
- `memory://wave_2_results` - Second wave outcomes
- `memory://wave_3_results` - Third wave outcomes
- `memory://improvement_complete` - Final summary
```

## Examples

### Example 1: Basic Code Improvement
```
User: /sc:improve src/auth/login.js

Shannon:
1. Analyzing login.js baseline metrics...
   ✅ Complexity: avg 14.2 (high)
   ⚠️ Duplication: 3 similar patterns
   ✅ Tests: 45/45 passing

2. Wave 1: Complexity reduction
   - Extracted nested conditionals
   - Applied guard clauses
   - Validation: ✅ 45/45 tests pass
   - Metrics: Complexity 14.2 → 8.1 (-43%)

3. Wave 2: Duplication elimination
   - Extracted validation helper
   - Consolidated error handling
   - Validation: ✅ 45/45 tests pass
   - Metrics: Duplication 3 → 0 instances

4. Final validation
   ✅ All tests passing
   ✅ Performance stable
   ✅ Coverage maintained at 92%

Result: 43% complexity reduction, zero duplication, 100% test pass rate
```

### Example 2: Performance-Focused Improvement
```
User: /sc:improve src/api/users.js --focus performance

Shannon:
1. Baseline performance benchmarks...
   ⚠️ GET /users: 340ms (target <200ms)
   ⚠️ Database query: N+1 pattern detected
   ✅ Memory: 145MB (acceptable)

2. Wave 1: Query optimization
   - Replaced N+1 with JOIN query
   - Added database indexes
   - Validation: ✅ 67/67 tests pass
   - Performance: 340ms → 145ms (-57%)

3. Wave 2: Response caching
   - Implemented Redis cache layer
   - Cache invalidation strategy
   - Validation: ✅ 67/67 tests pass
   - Performance: 145ms → 42ms (-71% total)

4. Final validation
   ✅ All tests passing
   ✅ Target <200ms achieved (42ms)
   ✅ Memory usage stable

Result: 87% response time improvement, maintained test coverage
```

### Example 3: Multi-Wave Quality Enhancement
```
User: /sc:improve src/components/ --iterations 5 --focus maintainability

Shannon:
1. Analyzing 12 component files...
   ⚠️ Avg complexity: 16.8
   ⚠️ Duplication: 42%
   ⚠️ Maintainability index: 54 (poor)
   ✅ Tests: 156/156 passing

2. Wave 1: Component structure
   - Extracted custom hooks
   - Separated concerns
   - Validation: ✅ 156/156 tests pass
   - Metrics: Complexity 16.8 → 12.3

3. Wave 2: Duplication removal
   - Created shared UI utilities
   - Consolidated styling logic
   - Validation: ✅ 156/156 tests pass
   - Metrics: Duplication 42% → 18%

4. Wave 3: Pattern consistency
   - Applied consistent prop patterns
   - Standardized state management
   - Validation: ✅ 156/156 tests pass
   - Metrics: Maintainability 54 → 68

5. Wave 4: Performance optimization
   - Memoization where appropriate
   - Lazy loading implementation
   - Validation: ✅ 156/156 tests pass
   - Metrics: Render time -35%

6. Wave 5: Documentation
   - Added JSDoc comments
   - PropTypes definitions
   - Validation: ✅ 156/156 tests pass
   - Metrics: Maintainability 68 → 79

Final: 53% complexity reduction, 75% less duplication, maintainability "good"
```

### Example 4: Security-Focused Improvement
```
User: /sc:improve src/auth/ --focus security

Shannon:
1. Security audit of auth module...
   🚨 Input validation gaps
   🚨 SQL injection risk in login
   ⚠️ Weak password requirements
   ✅ HTTPS enforcement present

2. Wave 1: Input validation
   - Implemented strict validation
   - Added sanitization layer
   - Validation: ✅ 89/89 tests pass
   - Security: Input validation 100% coverage

3. Wave 2: SQL injection prevention
   - Converted to parameterized queries
   - Added ORM safety checks
   - Validation: ✅ 89/89 tests pass
   - Security: SQL injection risk eliminated

4. Wave 3: Password policy
   - Enhanced password requirements
   - Implemented rate limiting
   - Validation: ✅ 95/95 tests pass (6 new tests)
   - Security: OWASP compliance achieved

5. Final security scan
   ✅ No critical vulnerabilities
   ✅ OWASP Top 10 compliance
   ✅ All tests passing

Result: Security vulnerabilities eliminated, compliance achieved
```

## Integration with Other Commands

### Pre-Improvement Analysis
```bash
# Analyze before improving
/sc:analyze src/auth/ --focus quality
# Review findings, then improve
/sc:improve src/auth/ --based-on-analysis
```

### Post-Implementation Improvement
```bash
# Implement feature first
/sc:implement "user authentication"
# Then improve implementation
/sc:improve src/auth/ --newly-implemented
```

### Iterative Development Cycle
```bash
# Implement → Test → Improve → Repeat
/sc:implement "payment processing"
/sc:test src/payments/ --functional
/sc:improve src/payments/ --based-on-test-results
```

## Quality Gates & Thresholds

### Mandatory Gates (Block Progression)
- ✅ ALL tests must pass after each wave
- ✅ NO new lint errors introduced
- ✅ NO syntax errors present
- ✅ NO type errors (TypeScript/typed languages)

### Quality Thresholds (Target Goals)
- 🎯 Complexity: <10 per function (recommended)
- 🎯 Duplication: <10% (recommended)
- 🎯 Maintainability Index: >70 (good)
- 🎯 Test Coverage: Maintain or improve
- 🎯 Performance: No regression >5%

### Convergence Criteria (Stop Conditions)
- ✅ All quality thresholds met
- ✅ Diminishing returns (<5% improvement per wave)
- ✅ Maximum waves reached (default: 5)
- ✅ Manual user stop requested

## Integration with SuperClaude

Shannon's `/sc:improve` builds on SuperClaude's foundation:
- **Inherits**: SuperClaude's persona system, MCP integration, tool orchestration
- **Enhances**: Adds wave-based iteration, test validation, metrics tracking
- **Preserves**: All SuperClaude improvement capabilities remain available
- **Extends**: Systematic approach with evidence-based validation

**Migration Path**: Existing SuperClaude users can use `/sc:improve` as drop-in replacement with enhanced capabilities. All SuperClaude flags and patterns work with Shannon enhancements automatically applied.

## Success Criteria

An improvement session is successful when:
- ✅ All quality thresholds met or improved
- ✅ 100% test pass rate maintained
- ✅ No performance regressions introduced
- ✅ Evidence-based improvement metrics documented
- ✅ Context preserved in Serena for future sessions
- ✅ Code maintainability demonstrably improved