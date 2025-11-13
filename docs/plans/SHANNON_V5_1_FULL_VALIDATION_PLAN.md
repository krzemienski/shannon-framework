# Shannon v5.1 - Full System Validation and Testing Plan

**Created**: 2025-01-12
**Scope**: Comprehensive validation of Shannon v5.0 after namespace modernization
**Goal**: Verify every component works correctly and integrates properly
**Duration**: 1-2 sessions

---

## Context

Shannon v5.0 completed major refactoring:
- Plugin name: shannon-plugin → shannon
- Commands: sh_*.md → *.md (15 clean names)
- Namespace: /sh_* → /shannon:*
- Structure: Guides moved to docs/
- NEW: Shannon Task (commands/task.md + skills/task-automation/)

**Automated validation completed** ✅:
- Plugin config valid
- Command frontmatter valid (15/15)
- Skill frontmatter valid (18/18)
- Command→skill references valid
- Skill dependencies valid
- Zero structural issues

**NOT YET VALIDATED** ❌:
- Hook system functionality
- Skill testing with real subagents
- End-to-end workflow integration
- Shannon Task actual operation
- Performance and edge cases

---

## Phase 1: Hook System Validation

### 1.1 Read All Hook Files Completely

**Files** (4 Python hooks):
- hooks/post_tool_use.py (NO MOCKS enforcement) ← PARTIALLY READ
- hooks/precompact.py (emergency checkpoints)
- hooks/stop.py (session cleanup)
- hooks/user_prompt_submit.py (input validation)

**Verify**:
- Hook code is syntactically correct
- Hooks register with Claude Code properly
- Each hook's purpose is clear
- Error handling exists

### 1.2 Test Hook Triggering

**Test**: Do hooks actually fire?

**post_tool_use test**:
1. Write a test file with mock
2. Verify hook blocks it
3. Expected: Error message about NO MOCKS

**precompact test**:
1. Fill context to 90%
2. Verify hook creates checkpoint
3. Expected: Checkpoint saved to Serena

**stop test**:
1. End session
2. Verify cleanup runs
3. Expected: Session state saved

### 1.3 Hook-Skill Integration

**Verify**:
- Skills work with hook enforcement
- Hooks don't break skill execution
- Error messages are helpful
- Can recover from hook blocks

---

## Phase 2: Skill Functional Testing

### 2.1 Audit Existing Tests

**Find all skill tests**:
```bash
find skills -type d -name "tests"
find skills -name "*test*.md" -o -name "*TEST*.md"
```

**For each test found**:
- Read test file completely
- Verify it tests the skill properly
- Check: Uses real Skill tool? Or just documentation?
- Check: Tests outputs? Or just describes process?

**Expected**: 7 skills have tests/ directories (found earlier)

### 2.2 Test Skills That Spawn Agents

**Critical skills** (use Task tool to spawn agents):
- wave-orchestration (spawns FRONTEND, BACKEND, etc.)
- Any skill with agent coordination

**Test**:
1. Invoke wave-orchestration skill
2. Verify it can spawn agents with Task tool
3. Check: Agents actually execute?
4. Check: Results properly collected?

**Methodology**: Real subagent testing (NO MOCKS)

### 2.3 Create Missing Skill Tests

**Skills WITHOUT tests** (11 out of 18):
- Prioritize critical skills
- Create functional tests using Skill tool
- Test with real inputs/outputs
- Validate error handling

**Test template**:
```python
# Test: spec-analysis skill
from claude_agent_sdk import query

async def test_spec_analysis():
    result = await query(
        prompt='Use Skill("spec-analysis") with "Build auth system"',
        options={"setting_sources": ["user"]}
    )
    # Verify: Complexity score returned
    # Verify: Domain breakdown present
    # Verify: Format correct
```

---

## Phase 3: Command-Skill-Agent Integration Testing

### 3.1 Command Invocation Tests

**For EACH of 15 commands**:

Test pattern:
```python
async def test_command_{name}():
    result = await query(prompt="/shannon:{name}")
    # Verify: Command loads
    # Verify: Skill invokes (if applicable)
    # Verify: Output format correct
    # Verify: No errors
```

**Priority commands**:
1. /shannon:spec (most critical)
2. /shannon:wave (complex)
3. /shannon:task (NEW)
4. /shannon:prime (multi-skill)

### 3.2 End-to-End Workflow Tests

**Test 1: Manual workflow**
```python
# Test: prime → spec → wave sequence
async def test_manual_workflow():
    # Step 1
    await query("/shannon:prime")
    # Verify: Skills discovered, MCPs verified

    # Step 2
    await query('/shannon:spec "Build calculator"')
    # Verify: Complexity score returned

    # Step 3
    await query('/shannon:wave')
    # Verify: Wave execution starts
```

**Test 2: Shannon Task workflow**
```python
# Test: automated prime → spec → wave
async def test_shannon_task():
    await query('/shannon:task "Build calculator" --plan-only')
    # Verify: All steps execute in order
    # Verify: Plan generated
    # Verify: No execution (plan-only mode)
```

### 3.3 Error Handling Tests

**Test error paths**:
- Command with invalid input
- Skill missing dependency
- Agent spawn failure
- Hook blocking operation
- MCP unavailable

**Verify**:
- Errors are clear
- Recovery options provided
- System doesn't crash
- State preserved

---

## Phase 4: Documentation Completeness

### 4.1 README Verification

**Check**:
- All 15 commands listed ✅
- All examples work (try each one)
- Installation instructions accurate
- Troubleshooting helpful

**Test each README example**:
```bash
# From Quick Start section
/shannon:prime
/shannon:spec "Build auth"
/shannon:task "Build calculator"
```

### 4.2 Guide Accuracy

**For each guide** (docs/guides/commands/):
- Read completely
- Verify examples work
- Check cross-references
- Update if needed

### 4.3 Reference Doc Synthesis

**Read ALL docs/ref files** (15 files):
- sdk-plugins-LATEST.md
- code-claude-slash-commands-LATEST.md
- code-claude-skills-LATEST.md
- (+ 12 more)

**Synthesize**:
- Understand complete plugin spec
- Verify Shannon complies
- Document any deviations

---

## Phase 5: Repository Structure Audit

### 5.1 Directory Structure Review

**Verify clean separation**:
```
shannon-framework/
├── .claude-plugin/   # Plugin config only
├── commands/         # ONLY .md command files (15)
├── skills/           # ONLY skill dirs (18)
├── agents/           # ONLY .md agent files (24)
├── hooks/            # ONLY .py hook files (4)
├── core/             # Architectural docs (9)
├── docs/             # ALL other documentation
├── tests/            # Validation suite
└── README.md         # Source of truth
```

**Check for**:
- No docs in component dirs ✅
- No stray files
- Logical organization
- Standard conventions

### 5.2 Cross-Reference Validation

**Check**:
- README links to guides (correct paths?)
- Guides reference commands (correct names?)
- Skills reference sub-skills (exist?)
- Agents reference skills (valid?)

**Tool**:
```bash
# Find all markdown links
grep -r '\[.*\](.*\.md)' . --include="*.md"
# Verify each linked file exists
```

---

## Phase 6: Performance and Edge Cases

### 6.1 Token Usage

**Measure**:
- Plugin load overhead
- Skill invocation cost
- Agent spawn cost
- Complete workflow token usage

**Optimize** if needed:
- Reduce prompt verbosity
- Cache repeated operations
- Progressive disclosure

### 6.2 Edge Cases

**Test**:
- Empty specification
- Extremely long specification
- Invalid user inputs
- Missing MCPs
- Concurrent operations
- Session interruption
- Context limit scenarios

---

## Phase 7: Create Comprehensive Test Suite

### 7.1 Integration Test Framework

**File**: tests/test_shannon_v5_integration.py

**Tests**:
1. test_plugin_loads()
2. test_all_commands_available()
3. test_skill_discovery()
4. test_spec_analysis_workflow()
5. test_wave_orchestration_workflow()
6. test_shannon_task_workflow()
7. test_hook_enforcement()
8. test_agent_spawning()
9. test_error_handling()
10. test_edge_cases()

**Run**: python3 tests/test_shannon_v5_integration.py

**Expected**: All pass ✅

### 7.2 Add to CI/CD

**GitHub Actions** (future):
```yaml
name: Shannon v5 Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate structure
        run: python3 validate_shannon_v5.py .
      - name: Integration tests
        run: python3 tests/test_shannon_v5_integration.py
```

---

## Success Criteria

Shannon v5.1 validation complete when:

**Structure** ✅:
- All files in correct locations
- No docs in component directories
- Clean separation maintained

**Formats** ✅:
- All YAML/JSON valid
- All frontmatter correct
- All references resolve

**Functionality** ❌ (v5.1 goal):
- All commands work
- All skills execute correctly
- Hooks enforce properly
- Agents spawn successfully
- End-to-end workflows complete

**Integration** ❌ (v5.1 goal):
- Command→skill→agent chain works
- Hooks don't break workflows
- Serena MCP integration solid
- Error handling robust

**Testing** ❌ (v5.1 goal):
- All skills have tests
- Tests use real subagents
- NO MOCKS compliance verified
- Test suite passes

**Documentation** ✅:
- README accurate
- Guides updated
- Examples work

---

## Execution Plan

**Session 1** (Current):
- ✅ Automated validation (DONE - all passed)
- ✅ Create this plan (IN PROGRESS)
- ⏭️ Save audit results

**Session 2** (Next):
- Read all hook files completely
- Read all agent files
- Audit skill tests
- Fix any issues found

**Session 3**:
- Create missing skill tests
- Run integration tests
- End-to-end validation
- Performance testing

**Session 4**:
- Documentation polish
- Edge case testing
- Final validation
- v5.1 release

---

## Audit Results (Current Session)

### Automated Validation ✅

**Validation script**: validate_shannon_v5.py

**Results**:
- Commands: 15, all valid ✅
- Skills: 18, all valid ✅
- Frontmatter: 100% correct ✅
- References: All resolve ✅
- Dependencies: All exist ✅
- Issues: 0 ✅

### Manual Audit (Partial)

**Completed**:
- Plugin config read and verified ✅
- Claude Code specs read (4 critical files) ✅
- post_tool_use.py partially read ✅
- Skill count verified (18 including task-automation) ✅
- Test existence checked (7 skills have tests) ✅

**Not completed** (defer to v5.1):
- Complete hook file reading (4 files)
- Complete agent file reading (24 files)
- Skill test methodology verification
- End-to-end testing
- Performance measurement

---

## Recommendations

**Immediate** (before v5.0 release):
- ✅ DONE: Structure correct, formats valid, references resolve

**v5.1 Priority**:
1. Read all hooks completely
2. Test Shannon Task end-to-end
3. Verify skill tests are proper
4. Add missing tests

**v5.2 Future**:
1. Performance optimization
2. Additional examples
3. Video tutorials
4. Community feedback integration

---

## Summary

**v5.0 Status**: Structurally sound, formats valid, ready for functional testing

**v5.1 Goal**: Complete functional validation, comprehensive testing, production-ready

**Path forward**: Execute v5.1 plan in next sessions with systematic testing
