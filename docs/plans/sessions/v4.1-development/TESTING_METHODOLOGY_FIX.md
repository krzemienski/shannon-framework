# Critical Issue: Sub-Agent Testing Methodology Flaw

## Problem Discovered

**All sub-agent tests failing with**: "Unknown skill: spec-analysis"

**Root Cause**: Sub-agents spawned via Task() don't have access to Shannon skills
- Skills live in shannon-plugin/skills/
- Sub-agents spawn in clean environment  
- Skill() tool requires skills to be in discovery system
- Shannon plugin not active in sub-agent context

## Tests Invalidated

❌ spec-analysis RED/GREEN test (claimed 19% improvement) - BOTH tests failed to access skill
❌ wave-orchestration RED/GREEN test - Tests failed  
❌ phase-planning RED/GREEN test - Tests failed
❌ honest-reflections validation test - Test failed

**All validation claims based on failed tests are INVALID**

## Correct Testing Methodology

### Option 1: Direct Execution (Not Sub-Agents)

Test by **reading skill instructions and executing directly**:

```
1. Read spec-analysis/SKILL.md completely
2. Follow instructions manually (calculate 8D scores myself)
3. Compare WITH walkthrough vs WITHOUT walkthrough
4. See if results differ
```

No sub-agents needed - just execute the algorithm.

### Option 2: Inline Skill Content

Provide complete skill content in sub-agent prompt:

```python
Task(
  prompt=f"""
  You have this skill available:
  
  {read_file('shannon-plugin/skills/spec-analysis/SKILL.md')}
  
  Now use it to analyze: [specification]
  """
)
```

This makes skill content available without requiring Skill() tool.

### Option 3: Test Real Commands Instead

Instead of testing skills in isolation, test actual Shannon commands:
- Commands ARE available (they're .md files that Claude reads)
- Test: Does /sh_spec produce 8D analysis?
- Test: Does /sh_wave coordinate agents?
- Test: Does /sh_checkpoint save to Serena?

## What Must Be Re-Done

1. **Re-validate spec-analysis enhancement**: Use Option 1 or 2 with working tests
2. **Re-validate wave-orchestration**: Test actual mechanism
3. **Re-validate phase-planning**: Test with inline skill content
4. **Test honest-reflections**: Include full skill content in prompt

## Next Steps

1. Fix testing methodology immediately
2. Re-run all validations with correct approach
3. Retract invalid claims
4. Document what actually works vs assumptions

