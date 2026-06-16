# ANALYZER Agent - Examples

> Loaded on-demand (Tier 3)

## Examples

### Example 1: Performance Analysis

```
Task: Analyze why dashboard loads slowly

Step 1: Evidence Collection
  Glob "**/*dashboard*" → Find dashboard files
  Read dashboard.js → Examine implementation
  Grep "fetch|axios|api" dashboard.js → Find API calls
  write_memory("analysis_dashboard_evidence", {...})

Step 2: Pattern Identification (Sequential MCP)
  Identify: Multiple sequential API calls (not parallel)
  Identify: No caching mechanism
  Identify: Heavy re-renders on every update
  write_memory("analysis_dashboard_patterns", {...})

Step 3: Hypothesis Formation
  H1: Sequential API calls cause delay (HIGH likelihood)
  H2: Missing caching increases load (MEDIUM likelihood)
  H3: Re-render overhead (LOW likelihood)
  write_memory("analysis_dashboard_hypotheses", {...})

Step 4: Verification
  Test H1: Count API calls → 8 sequential calls, 3.2s total
  Test H2: No cache headers in responses
  Test H3: React DevTools shows 20 renders/second
  write_memory("analysis_dashboard_verification", {...})

Step 5: Root Cause & Report
  Primary: Sequential API calls (2.8s of 3.2s delay)
  Secondary: Excessive re-renders (0.4s delay)
  Tertiary: No caching (increases server load)

  Recommendations:
  1. Immediate: Parallelize API calls → 0.8s total (3x faster)
  2. Short-term: Add React.memo to components → reduce renders
  3. Long-term: Implement cache layer → reduce server load

  write_memory("analysis_dashboard_performance_complete", {...})
```