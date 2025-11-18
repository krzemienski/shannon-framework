---
name: brainstorming
description: Divergent idea exploration + wave-aware option scoring before formal planning
skill-type: PLAYBOOK
shannon-version: ">=5.4.0"
complexity-triggers: [0.00-1.00]
requires:
  - phase-planning
  - spec-analysis
---

# Brainstorming Skill

## Intent

Produce multiple viable solution approaches before committing to a plan. Every option must include:

- Architecture summary (2-3 sentences)
- Initial 8D complexity estimates
- Testing + observability strategy
- Wave recommendation (Sequential vs Wave, agent count)
- Risk / blast radius assessment

## Required Workflow

1. **Set Stage**
   - Announce use of brainstorming skill.
   - Confirm specification / goal / constraints.
   - If missing, request `/shannon:spec` first.

2. **Generate Options (≥3)**
   - Use divergent thinking (tech stack permutations, scope splits, feature flags).
   - For each option include:
     ```
     Option N – <Name>
     Summary:
     Pros / Cons:
     Complexity: Scope ?, Tech ?, … Total ? (Simple/Moderate/Complex)
     Testing: <how NO MOCKS applies>
     Wave Strategy: Sequential or Wave (N agents)
     ```

3. **Compare**
   - Build table: Option × {Complexity, Risk, Time, Dependencies}.
   - Highlight blockers + unknowns per option.

4. **Recommend + Handoff**
   - State recommended option + rationale.
   - Provide next commands:
     - `/shannon:spec "<option>" --context <doc>`
     - `/shannon:write_plan "<option>" --source <doc>`

5. **Persist**
   - Save to `docs/plans/brainstorm/YYYY-MM-DD-<slug>.md`.
   - Record metadata (goal, constraints, participants).

## Guardrails

- Include at least one conservative + one ambitious option.
- If only one viable path exists, document why others fail.
- Never skip testing strategy—even for exploratory options.
- Always mention Serena checkpointing strategy.

## Related Commands

- `/shannon:brainstorm`
- `/shannon:write_plan`
- `/shannon:spec`
