# Shannon CLI - Critical Lessons Learned

## Mistake: Reimplementing Instead of Delegating

**What happened**: Spent Waves 1-3 reimplementing 8D algorithm, wave orchestration, domain detection - 5,000+ lines duplicating Shannon Framework.

**Why it was wrong**: Shannon Framework ALREADY has all this in spec-analysis and wave-orchestration skills (11,000 lines of tested behavioral patterns).

**Cost**: ~20 hours wasted + 5,000 lines of duplicate code

**Root cause**: Didn't read Shannon Framework structure first. Assumed CLI meant "reimplement in Python".

## Mistake: Creating Pytest Tests

**What happened**: Agents created test_*.py files with pytest.

**Why it was wrong**: TECHNICAL_SPEC.md explicitly says "NO pytest - shell scripts ONLY" (Section 2.2, line 149).

**Cost**: Violated core spec requirement, had to delete tests and respawn agents.

**Root cause**: Didn't enforce NO PYTEST in agent prompts clearly enough.

## Mistake: Wrong SDK API Assumptions

**What happened**: Implemented AgentFactory assuming SDK had certain classes/methods without reading SDK docs.

**Why it was wrong**: Made assumptions instead of reading anthropics/claude-agent-sdk-python README and types.py.

**Cost**: Had to redesign SDK integration after functional testing revealed errors.

**Root cause**: Skipped "read the documentation" step.

## Correct Approach (V2.0)

1. ✅ Read Shannon Framework README FIRST
2. ✅ Read Claude Agent SDK documentation FIRST
3. ✅ Understand what exists before building
4. ✅ Delegate to framework instead of reimplementing
5. ✅ Test functionally with REAL SDK calls
6. ✅ NO PYTEST - shell scripts only

## Architecture Insight

Shannon CLI should be ~3,000-5,000 lines:
- SDK client wrapper
- Progress tracking UI
- Session persistence
- CLI commands
- Configuration

NOT 15,000+ lines reimplementing what framework already has.

**Thin wrapper > Reimplementation**

## Key Takeaway

**ALWAYS**: Read existing system documentation completely before designing.
**NEVER**: Assume you need to reimplement - check what exists first.
**VERIFY**: Test with real integrations early, not after building everything.
