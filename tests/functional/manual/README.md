# Shannon Manual Test Cases

Comprehensive manual test case templates for validating Shannon framework behavioral patterns and command implementations.

## Overview

This directory contains 6 detailed manual test case templates with step-by-step validation checklists for critical Shannon functionality.

## Test Cases

### TC-001: /sh:spec Command Validation
**File**: `test_case_sh_spec.md`
**Priority**: Critical
**Time**: 10 minutes
**Focus**: 8-dimensional complexity analysis, artifact generation, MCP recommendations

**Validates**:
- SPEC_ANALYZER agent activation
- 8-dimensional complexity scoring
- Domain analysis accuracy
- MCP server recommendations
- 5-phase implementation plan
- Wave count justification
- Artifact creation (.shannon/analysis/spec_*.md)

### TC-002: Checkpoint and Restore Cycle
**File**: `test_case_sh_checkpoint.md`
**Priority**: Critical
**Time**: 15 minutes
**Focus**: Session state persistence and restoration

**Validates**:
- Checkpoint creation (/sh:checkpoint)
- JSON artifact structure
- State restoration (/sh:restore)
- Context preservation
- Memory entry persistence
- Todo list state management
- Cross-session persistence

### TC-003: /sc:implement with React + shadcn
**File**: `test_case_sc_implement_react.md`
**Priority**: High
**Time**: 20 minutes
**Focus**: MCP integration, React component generation, NO MOCKS enforcement

**Validates**:
- IMPLEMENTER agent activation
- shadcn MCP usage for UI components
- Serena MCP for project context
- TypeScript type correctness
- React hooks and modern patterns
- Complete validation logic (no mocks)
- Accessibility attributes
- Component integration

### TC-004: Wave Orchestration with Parallel Execution
**File**: `test_case_wave_orchestration.md`
**Priority**: Critical
**Time**: 25 minutes
**Focus**: Multi-wave coordination, parallel operations, wave boundaries

**Validates**:
- WAVE_ORCHESTRATOR agent activation
- Wave planning and boundary definition
- Parallel execution within waves
- Sequential wave progression
- Module assignment to waves
- Wave coordination and file conflict prevention
- Performance gains (30-40% faster)
- Wave artifact generation

### TC-005: PreCompact Hook Memory Optimization
**File**: `test_case_precompact_hook.md`
**Priority**: High
**Time**: 15 minutes
**Focus**: Context optimization, token efficiency, quality preservation

**Validates**:
- Automatic PreCompact activation
- Token reduction (30-50%)
- Symbol-enhanced communication (--uc mode)
- Selective context retention
- MCP query optimization
- Quality preservation (>90%)
- Adaptive threshold behavior
- Metrics artifact generation

### TC-006: NO MOCKS Rule Enforcement
**File**: `test_case_no_mocks_enforcement.md`
**Priority**: Critical
**Time**: 20 minutes
**Focus**: Zero tolerance for placeholder implementations

**Validates**:
- NO TODO/FIXME comments
- NO mock implementations
- NO placeholder code patterns
- Complete feature implementations
- Real validation logic
- Real error handling
- Real async implementations
- Automated mock detection

## Test Execution Guidelines

### Prerequisites
- Shannon project loaded in Claude Code
- Serena MCP configured and functional
- Other MCP servers as needed per test case
- Test environment: `/Users/nick/Documents/shannon`

### Test Structure
Each test case includes:
1. **Objective**: Clear validation goal
2. **Prerequisites**: Required setup and dependencies
3. **Test Steps**: Detailed step-by-step instructions
4. **Validation Checklists**: Comprehensive verification points
5. **Expected Results**: Sample outputs and artifacts
6. **Pass/Fail Criteria**: Clear success conditions
7. **Debug Information**: Logs and artifacts to collect

### Execution Order
Recommended order for comprehensive validation:

1. **TC-001** (sh:spec) - Foundation
2. **TC-006** (NO MOCKS) - Quality baseline
3. **TC-003** (sc:implement React) - Integration
4. **TC-004** (Wave Orchestration) - Advanced coordination
5. **TC-005** (PreCompact Hook) - Performance
6. **TC-002** (Checkpoint/Restore) - Session management

### Results Collection

Each test case generates artifacts in:
```
test-results/TC-XXX/
├── artifacts/      # Generated code, specs, checkpoints
├── logs/          # Execution logs and errors
├── screenshots/   # Visual validation captures
└── metrics/       # Performance and quality metrics
```

## Quality Standards

### Pass Criteria
- All validation checkboxes checked
- Artifacts generated correctly
- Shannon behavioral patterns evident
- NO generic Claude Code responses
- Professional code quality maintained

### Fail Criteria
- Mock implementations detected
- Incomplete features (TODOs, placeholders)
- Artifacts missing or malformed
- Generic responses instead of Shannon patterns
- Quality degradation

## Validation Metrics

### Per Test Case
- Execution time (actual vs estimated)
- Artifact completeness percentage
- Validation checkpoint pass rate
- Quality score (1-10)
- Shannon pattern adherence

### Overall Framework
- Total violations detected: 0 (required)
- Implementation completeness: 100%
- Test pass rate: 100%
- Professional quality maintained
- Shannon behaviors consistent

## Test Maintenance

### Updating Test Cases
When Shannon framework changes:
1. Review affected test cases
2. Update validation checklists
3. Modify expected outputs
4. Adjust pass/fail criteria
5. Test against new implementation

### Adding New Test Cases
Follow template structure:
- Test ID: TC-XXX
- Priority: Critical/High/Medium
- Category: Behavioral/Integration/E2E
- Estimated Time
- Detailed steps with validation checklists

## Automation Potential

While these are manual test cases, components can be automated:
- Mock detection scripts (TC-006 has example)
- Artifact structure validation
- File content pattern matching
- Metrics collection and reporting

## Support

For issues or questions about test cases:
1. Review test case objectives and validation criteria
2. Check debug commands for troubleshooting
3. Collect logs and artifacts for analysis
4. Compare against expected results

## Document Information

**Created**: 2025-10-01
**Format**: Markdown with bash/python code blocks
**Total Lines**: 3,387 lines across 6 test cases
**Average**: 565 lines per test case

**Maintenance**: Update test cases when Shannon framework adds new features or modifies existing behavioral patterns.
