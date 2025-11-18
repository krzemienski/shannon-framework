---
name: systematic-debugging
description: Checklist-driven debugging protocol combining sequential thinking, forced reading, and instrumentation
skill-type: PLAYBOOK
shannon-version: ">=5.4.0"
complexity-triggers: [0.30-1.00]
requires:
  - forced-reading-protocol
  - functional-testing
---

# Systematic Debugging Skill

## Intent

Provide a battle-tested sequence for isolating and fixing defects. Activated automatically by `/shannon:ultrathink`, but can be referenced manually during `/shannon:do` or `/shannon:exec`.

## Protocol

1. **Frame the Problem**
   - Restate symptom, impact, repro frequency.
   - Note environment (prod/staging/local) and measurement sources.
2. **Forced Reading**
   - Read ALL relevant files fully (no skipping). Use forced-reading-sentinel.
   - Summarize each section to prove comprehension.
3. **Establish Baseline**
   - Create failing test that reproduces issue.
   - Capture exact logs/metrics before making changes.
4. **Binary Search / Isolation**
   - Toggle feature flags, bisect commits, isolate components.
   - Instrument code paths with high-signal logging.
5. **Hypothesis Table**
   - List potential causes; score vs evidence.
   - Disprove quickly—document why eliminated.
6. **Root Cause Confirmation**
   - Once narrowed, trace call stack + state transitions.
   - Capture final proof (line numbers, data snapshots).
7. **Fix + Verification**
   - Apply minimal patch.
   - Run failing test (should now pass) + regression suite.
8. **Postmortem Notes**
   - Document cause, blast radius, preventative guardrails.
   - Update plan/issues with learnings.

## Outputs

- Markdown report or Serena memory entry containing:
  - Problem statement
  - Reproduction steps
  - Hypothesis log
  - Root cause chain
  - Fix summary
  - Tests run
  - Prevention actions

## Guardrails

- Never skip forced-reading step.
- No speculative fixes without reproduction proof.
- Log everything—future subagents rely on traceability.

## Related Commands

- `/shannon:ultrathink`
- `/shannon:do --debug`
- `/shannon:test`
