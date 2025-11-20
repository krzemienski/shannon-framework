---
name: dispatching-parallel-agents
description: Use for 3+ independent failures - dispatches parallel subagents with Shannon wave coordination, success scoring (0.00-1.00) per domain, and MCP result aggregation
---

# Dispatching Parallel Agents (Shannon-Enhanced)

## Overview

**Parallel investigation of independent failures with quantitative success tracking.**

Dispatch one agent per independent problem domain. Shannon enhancement adds wave-based coordination, numerical success scoring, and MCP result aggregation.

**Success Scoring (0.00-1.00):**
- Per-domain: agent_success_score = (problems_fixed / problems_identified)
- Overall: parallel_efficiency = (domains_completed_concurrently / sequential_cost)

## When to Use

```
3+ independent failures?
├─ Yes, independent domains?
│  ├─ Yes → Parallel dispatch (optimal)
│  └─ No → Sequential investigation
└─ No → Single agent focus
```

**Dispatch when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem understood without context from others
- No shared state between investigations

**Don't dispatch:**
- Failures are related (fix one might fix others)
- Agents need full system state understanding
- Would interfere with each other's work

## The Pattern

### 1. Identify Independent Domains

Group failures by subsystem:
```
Domain A: Tool approval flow (file_a_test)
Domain B: Batch completion (file_b_test)
Domain C: Abort functionality (file_c_test)
```

**Independence check:** Fixing Domain A doesn't touch Domain B/C code paths.

### 2. Assign Success Metrics

```bash
# Per-domain scoring (Serena)
per_domain_metrics = {
  domain: "Tool approval",
  problems_identified: 3,
  initial_root_cause_clarity: 0.6,  # 0-1.0
  estimated_complexity: 0.7,        # 0-1.0
}
```

### 3. Dispatch with Shannon Wave Coordination

```bash
# Launch agents concurrently with wave tracking
Task("Fix Domain A", wave_id="w1", timeout=30min)
Task("Fix Domain B", wave_id="w1", timeout=30min)
Task("Fix Domain C", wave_id="w1", timeout=30min)

# Shannon wave monitors parallel execution
# MCP tracks: start_time, end_time, status per agent
```

### 4. Aggregate Results via MCP

**Result structure (Serena):**
```yaml
parallel_dispatch:
  wave_id: "w1"
  domains_completed: 3
  time_sequential_equivalent: 90min
  time_actual_parallel: 35min
  efficiency_score: (90/35) = 2.57x faster

  per_domain:
    - domain: "Tool approval"
      agent_success_score: 0.95  # 2/3 fixed, 1 minor issue
      root_causes_found: 2
      files_modified: 3

    - domain: "Batch completion"
      agent_success_score: 1.00  # 2/2 fixed perfectly
      root_causes_found: 1
      files_modified: 2

    - domain: "Abort functionality"
      agent_success_score: 0.85  # 1/3 fixed, 1 partial
      root_causes_found: 1
      files_modified: 4
```

### 5. Review & Integrate

After agents return:
- [ ] Read each domain summary
- [ ] Verify agent_success_score > 0.80 per domain
- [ ] Check for code conflicts (MCP tracks file modifications)
- [ ] Run full test suite on integrated changes
- [ ] Calculate overall efficiency_score

## Agent Prompt Structure

```markdown
**Domain:** Fix agent-tool-abort.test.ts failures
**Scope:** Only this file and its immediate dependencies
**Success Metric:** Fix all 3 failing tests

Failing tests:
1. "should abort tool with partial output" → expects 'interrupted'
2. "should handle mixed completed/aborted" → timing issue
3. "should properly track pendingToolCount" → gets 0, expects 3

Your task:
1. Identify root causes
2. Fix with minimal code changes
3. Verify all 3 tests pass

Return: Summary of root causes, changes made, final test results
```

## Success Scoring Methodology

**Per-domain score:**
```
agent_success_score = (
  (problems_fixed / problems_identified) * 0.6 +
  (test_pass_rate) * 0.3 +
  (1.0 if no_conflicts else 0.0) * 0.1
)
Range: 0.00-1.00
```

**Overall parallel efficiency:**
```
efficiency_score = sequential_time_cost / actual_parallel_time
Range: 1.0x (no benefit) to Nx (benefit)
```

## Verification Checklist

- [ ] Identified 3+ independent domains
- [ ] Dispatched agents concurrently (wave_id tracked)
- [ ] All per_domain agent_success_score > 0.80
- [ ] MCP detected no file conflicts
- [ ] Full test suite green
- [ ] efficiency_score > 1.5x (time benefit)
- [ ] Integrated all changes

## Common Mistakes

❌ Too broad scope (fix everything)
✅ Specific scope (one test file)

❌ No domain metrics
✅ Track agent_success_score per domain

❌ Skip conflict detection
✅ MCP checks file modifications across agents

❌ Sequential dispatch (defeats purpose)
✅ Launch all agents concurrently with wave_id

## Pattern Learning (Serena)

Track across sessions:
- Domain types that parallelize well
- Average efficiency_score per domain type
- Typical agent_success_score distributions
- Common conflict patterns

Use historical data to:
- Predict which domains need more time
- Pre-estimate efficiency gains
- Alert if efficiency_score < 1.5x (may need sequential instead)

## Integration

**With:** testing-skills-with-subagents (each agent tests independently)
**MCP:** Tracks file modifications, test results, timing
**Serena:** Metrics for pattern learning

## Real-World Impact

From debugging session (2025):
- 6 failures across 3 domains
- Parallel dispatch: 3 agents concurrent
- efficiency_score: 2.1x (30min parallel vs 60min sequential)
- Overall per_domain agent_success_score: 0.93
