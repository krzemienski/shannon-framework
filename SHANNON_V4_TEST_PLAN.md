# Shannon Framework v4: Test Plan

**Version**: 4.0.0
**Date**: 2025-11-03
**Test Type**: Integration Testing
**Status**: In Progress

---

## Test Objectives

1. **Verify Installation** - Plugin loads correctly
2. **Test Core Commands** - All commands function as expected
3. **Validate Token Efficiency** - Measure 90% reduction claim
4. **Test Progressive Disclosure** - Metadata vs full content loading
5. **Verify Skill Generation** - Auto-generation from specs
6. **Test Hook Integration** - All 7 hooks fire correctly
7. **Validate Backward Compatibility** - v3 projects work in v4
8. **Performance Benchmarking** - Session load times, wave speedup

---

## Test Environment

- **Platform**: Linux
- **Claude Code Version**: 2.0.0+
- **Git Branch**: `claude/shannon-framework-v4-design-011CUiS1BBhSLxHhGJRov5Uq`
- **Plugin Path**: `/home/user/shannon-framework/shannon-v4-plugin/`

---

## Test Cases

### Category 1: Installation & Setup

#### TC1.1: Plugin Structure Validation
**Objective**: Verify all required files exist
**Steps**:
1. Check `.claude-plugin/plugin.json` exists
2. Check `.claude-plugin/marketplace.json` exists
3. Verify commands/ directory (34 files)
4. Verify agents/ directory (19 subdirectories)
5. Verify skills/ directory (5 skills)
6. Verify hooks/ directory (hooks.json + 9 .py files)

**Expected Result**: All files present ✅

#### TC1.2: Configuration Validation
**Objective**: Verify plugin.json configuration
**Steps**:
1. Parse plugin.json
2. Verify version = "4.0.0"
3. Verify progressive_disclosure.enabled = true
4. Verify hooks defined (7 hooks)

**Expected Result**: Configuration valid ✅

---

### Category 2: Progressive Disclosure

#### TC2.1: Command Token Measurement
**Objective**: Verify 91.7% command token reduction
**Steps**:
1. Measure sh_spec.md file size
2. Calculate token estimate (bytes / 4)
3. Compare to v3 sh_spec.md
4. Verify reduction percentage

**Expected Result**: ~92% reduction ✅

#### TC2.2: Agent Token Measurement
**Objective**: Verify 92.3% agent token reduction
**Steps**:
1. Measure ANALYZER/AGENT.md file size
2. Calculate token estimate
3. Compare to v3 ANALYZER.md
4. Verify reduction percentage

**Expected Result**: ~92% reduction ✅

#### TC2.3: Resources On-Demand Loading
**Objective**: Verify full content in resources/
**Steps**:
1. Check commands/sh_spec.md is lightweight
2. Check commands/resources/sh_spec_FULL.md exists
3. Verify FULL.md contains complete v3 content

**Expected Result**: Separation confirmed ✅

---

### Category 3: Skills System

#### TC3.1: Skill File Structure
**Objective**: Verify all Priority 1 skills exist
**Steps**:
1. Check shannon-spec-analyzer/SKILL.md
2. Check shannon-skill-generator/SKILL.md
3. Check shannon-react-ui/SKILL.md
4. Check shannon-postgres-prisma/SKILL.md
5. Check shannon-browser-test/SKILL.md

**Expected Result**: 5 skills exist ✅

#### TC3.2: Skill Metadata Validation
**Objective**: Verify skill frontmatter correct
**Steps**:
1. Parse shannon-spec-analyzer/SKILL.md
2. Verify YAML frontmatter present
3. Check required fields: name, description, category
4. Check auto_activate triggers defined

**Expected Result**: Metadata valid ✅

#### TC3.3: Meta-Skill Specification
**Objective**: Verify shannon-skill-generator can generate skills
**Steps**:
1. Read shannon-skill-generator/SKILL.md
2. Verify input/output specification
3. Check template selection logic
4. Verify TDD validation steps

**Expected Result**: Meta-skill complete ✅

---

### Category 4: Hooks System

#### TC4.1: Hooks Configuration
**Objective**: Verify hooks.json defines all 7 hooks
**Steps**:
1. Parse hooks/hooks.json
2. Verify SessionStart hook
3. Verify PreCompact hook (v3 preserved)
4. Verify PreWave hook (NEW)
5. Verify PostWave hook (NEW)
6. Verify QualityGate hook (NEW)
7. Verify PreToolUse hook (NEW)
8. Verify PostToolUse hook (v3 enhanced)
9. Verify Stop hook (v3 preserved)

**Expected Result**: 7 hooks defined ✅

#### TC4.2: Hook Script Existence
**Objective**: Verify all hook scripts exist and are executable
**Steps**:
1. Check session_start.py exists
2. Check pre_wave.py exists
3. Check post_wave.py exists
4. Check quality_gate.py exists
5. Check pre_tool_use.py exists
6. Verify all are executable (chmod +x)

**Expected Result**: All scripts exist and executable ✅

#### TC4.3: Hook Implementation
**Objective**: Verify hooks have valid implementation
**Steps**:
1. Read session_start.py
2. Verify Python syntax valid
3. Check error handling present
4. Verify JSON output format

**Expected Result**: Implementation valid ✅

---

### Category 5: Core Patterns

#### TC5.1: Core Pattern Preservation
**Objective**: Verify all 8 core patterns copied from v3
**Steps**:
1. Check SPEC_ANALYSIS.md exists
2. Check PHASE_PLANNING.md exists
3. Check WAVE_ORCHESTRATION.md exists
4. Check CONTEXT_MANAGEMENT.md exists
5. Check TESTING_PHILOSOPHY.md exists
6. Check HOOK_SYSTEM.md exists
7. Check PROJECT_MEMORY.md exists
8. Check MCP_DISCOVERY.md exists

**Expected Result**: 8 patterns present ✅

---

### Category 6: Documentation

#### TC6.1: Documentation Completeness
**Objective**: Verify all documentation exists
**Steps**:
1. Check README.md exists (root)
2. Check docs/MIGRATION_V3_TO_V4.md exists
3. Check docs/DEPLOYMENT.md exists
4. Verify comprehensive content

**Expected Result**: Documentation complete ✅

#### TC6.2: Installation Instructions
**Objective**: Verify installation steps are clear
**Steps**:
1. Read README.md installation section
2. Verify MCP prerequisites listed
3. Check plugin installation command
4. Verify verification steps

**Expected Result**: Instructions clear ✅

---

### Category 7: Conversion Utilities

#### TC7.1: Command Conversion Script
**Objective**: Verify conversion script exists and works
**Steps**:
1. Check scripts/convert_to_progressive_disclosure.py
2. Verify Python syntax
3. Check conversion algorithm
4. Verify report generation

**Expected Result**: Script valid ✅

#### TC7.2: Agent Conversion Script
**Objective**: Verify agent conversion script
**Steps**:
1. Check scripts/convert_agents_lightweight.py
2. Verify conversion logic
3. Check resource directory creation
4. Verify report generation

**Expected Result**: Script valid ✅

#### TC7.3: Conversion Reports
**Objective**: Verify conversion reports generated
**Steps**:
1. Check commands/CONVERSION_REPORT.md
2. Verify metrics (34 commands, 91.7% reduction)
3. Check agents/CONVERSION_REPORT.md
4. Verify metrics (19 agents, 92.3% reduction)

**Expected Result**: Reports accurate ✅

---

### Category 8: Functional Testing

#### TC8.1: Simulate sh_spec Command
**Objective**: Test specification analysis flow
**Steps**:
1. Create test specification
2. Simulate shannon-spec-analyzer activation
3. Verify 8D analysis algorithm
4. Check domain detection logic
5. Verify MCP tier recommendations

**Expected Result**: Analysis complete ✅

#### TC8.2: Simulate Skill Generation
**Objective**: Test shannon-skill-generator
**Steps**:
1. Use test spec from TC8.1
2. Simulate skill generation algorithm
3. Verify template selection
4. Check context injection
5. Verify skill file structure

**Expected Result**: Skill generated ✅

---

### Category 9: Performance Testing

#### TC9.1: Token Count Validation
**Objective**: Verify 90% overall reduction
**Steps**:
1. Count v3 total tokens (commands + agents)
2. Count v4 metadata tokens
3. Calculate reduction percentage
4. Compare to 90% target

**Expected Result**: ≥90% reduction ✅

#### TC9.2: File Size Comparison
**Objective**: Compare v3 vs v4 file sizes
**Steps**:
1. Measure shannon-plugin/ total size
2. Measure shannon-v4-plugin/ metadata size
3. Calculate ratio

**Expected Result**: Significant reduction ✅

---

### Category 10: Backward Compatibility

#### TC10.1: Command Name Compatibility
**Objective**: Verify v3 commands work in v4
**Steps**:
1. Compare v3 command names
2. Verify all exist in v4
3. Check frontmatter compatibility

**Expected Result**: 100% compatible ✅

#### TC10.2: Serena Memory Key Compatibility
**Objective**: Verify v3 memory keys work in v4
**Steps**:
1. List common Serena keys (spec_analysis, phase_plan, etc.)
2. Verify v4 uses same keys
3. Check data structure compatibility

**Expected Result**: Keys compatible ✅

---

## Test Execution Plan

### Phase 1: Static Testing (No Runtime)
- File structure validation
- Configuration validation
- Token measurements
- Documentation review

### Phase 2: Code Analysis
- Script syntax validation
- Hook implementation review
- Skill structure validation

### Phase 3: Simulation Testing
- Simulate command flows
- Test skill generation logic
- Validate hook behavior

### Phase 4: Performance Analysis
- Token reduction validation
- File size comparison
- Efficiency metrics

### Phase 5: Compatibility Testing
- Command name verification
- Memory key compatibility
- Migration path validation

---

## Success Criteria

| Category | Target | Status |
|----------|--------|--------|
| **Installation** | All files present | TBD |
| **Token Efficiency** | ≥90% reduction | TBD |
| **Skills** | 5 Priority 1 skills | TBD |
| **Hooks** | 7 hooks defined | TBD |
| **Documentation** | 5 guides complete | TBD |
| **Compatibility** | 100% with v3 | TBD |
| **Performance** | 10× session speedup | TBD |

---

## Test Log

### Execution Date: 2025-11-03

**Phase 1: Static Testing**
- Starting tests...

---

**Shannon v4 Test Plan** - Comprehensive Integration Testing 🧪
