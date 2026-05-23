---
name: why
description: Five-whys + root-cause-tracing + cause-and-effect diagram. Output root-cause analysis report.
replaces:
  - /kaizen:why
  - /kaizen:root-cause-tracing
  - /kaizen:cause-and-effect
  - /kaizen:analyse
  - /kaizen:analyse-problem
argument-hint: "<symptom-or-bug-description>"
---

# /shannon:why

Root-cause analysis. Five-whys cascade plus cause-and-effect mapping.

## Inputs

- Positional: symptom or bug description

## Behavior

1. Invoke `root-cause-tracing` skill.
2. Apply five-whys:
   - Q1: Why does the symptom occur? → A1
   - Q2: Why does A1 happen? → A2
   - ...continue until reaching a root cause that is actionable.
3. Build cause-and-effect diagram (Ishikawa / fishbone style; categories: code, data, config, environment, dependency, human).
4. Identify the smallest fix that addresses the root cause.
5. Output: `reports/root-cause-<slug>.md` with whys chain + diagram + proposed fix.

## Success criteria

- Five-whys chain reaches an actionable root cause (not a vague "it's complicated").
- Diagram identifies primary category.
- Proposed fix is specific (file path + change description).

## Hooks fired

- Standard chain (read-mostly).

## Skills invoked

- `root-cause-tracing`
- `sequential-analysis` (for deep chains)

## Iron rules

- No "the system is buggy" — go deeper.
- No "more testing" — fix the cause, do not pad coverage.
- Per `instrument-before-theorize.md`: if you can't determine root cause in 10 min of reading, ADD INSTRUMENTATION before continuing.

## Examples

```
/shannon:why "Login button does nothing on Safari mobile"
/shannon:why "Deploy preview returns 502 on Vercel since yesterday"
```
