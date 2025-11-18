---
name: forced-reading-sentinel
description: Automatically enforce full-file reading when prompts/files exceed Shannon thresholds
skill-type: GUARDRAIL
shannon-version: ">=5.4.0"
complexity-triggers: [0.00-1.00]
requires:
  - forced-reading-protocol
---

# Forced Reading Sentinel Skill

## Purpose

Prevent partial comprehension when interacting with large files or prompts. Activated by `user_prompt_submit` hook when:

- Prompt length ≥ **10,000 characters**
- OR prompt line count ≥ **400**
- OR prompt references large ranges (e.g., `lines 1-500`, `L42|`)
- OR the editor attaches files flagged as large (when available)

## Required Actions (when sentinel fires)

1. **Stop and Read Fully**
   - Consume the entire file sequentially.
   - Avoid skimming or jumping to suspected sections.
2. **Verbalize Understanding**
   - Summarize each major block (purpose, data flow, dependencies).
   - Call out implicit invariants and error paths.
3. **Note Context**
   - Record file path, size, and reason sentinel triggered.
   - Capture in response before proposing changes.
4. **Reconfirm Instructions**
   - Check if user wants a summary, refactor, or targeted fix.
   - If instructions ambiguous, ask clarifying questions.

## Response Pattern

When sentinel triggers, prepend:

```
📏 **Forced Reading Sentinel Activated**
- Reason: <character count / line count / range reference>
- Action: Performing full read per FORCED_READING_PROTOCOL.
```

Then walk through reading + summaries before edits.

## Exceptions

- Short prompts referencing large *external* docs still require acknowledgement (explain data unavailable).
- If file cannot be loaded (permissions), state limitation explicitly and request alternative.

## Related Assets

- `core/FORCED_READING_PROTOCOL.md`
- `hooks/user_prompt_submit.py`
- `/shannon:ultrathink`
