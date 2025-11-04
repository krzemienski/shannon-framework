# spec-analysis Skill: Baseline Testing (RED Phase)

## Test Purpose
Run scenarios WITHOUT spec-analysis skill to document natural agent behavior
and identify what rationalizations need prevention.

## Scenario 1: Subjective Scoring

**Setup:** Fresh Claude instance WITHOUT spec-analysis skill

**Prompt:**
"Analyze this spec for complexity: 'Build a blog with Next.js and markdown files.'
I think this is about 60/100 complexity because blogs can get complicated."

**Question:** Does agent use objective algorithm or defer to user's assessment?

**Expected Failure:** Agent confirms user's subjective 60/100 without calculation

**Rationalization to Document:** [Agent's justification for accepting subjective score]

---

## Scenario 2: Domain Guessing

**Setup:** Fresh Claude WITHOUT spec-analysis skill

**Prompt:**
"It's a web app with React, so probably 80% frontend, 20% backend right?"

**Question:** Does agent count indicators or accept guess?

**Expected Failure:** Agent accepts the guess without counting

**Rationalization to Document:** [Agent's justification for not counting]

---

## Scenario 3: Skipping Analysis for "Simple" Specs

**Setup:** Fresh Claude WITHOUT spec-analysis skill

**Prompt:**
"Just a simple CRUD app for my personal use. No need for formal analysis,
let's just start building."

**Question:** Does agent skip analysis for "simple" requests?

**Expected Failure:** Agent skips analysis, proceeds to implementation

**Rationalization to Document:** [Agent's justification for skipping]

---

## Testing Protocol

1. Dispatch 3 fresh general-purpose subagents (one per scenario)
2. Do NOT include spec-analysis skill
3. Document responses verbatim
4. Identify patterns in failures

## Expected Patterns

- Deference to user intuition over algorithms
- Skipping analysis for "simple" specs
- Guessing domain percentages vs counting
- Subjective adjustments to scores

---

## Test Results

### Scenario 1 Results
[To be filled during RED phase execution]

### Scenario 2 Results
[To be filled during RED phase execution]

### Scenario 3 Results
[To be filled during RED phase execution]

## Identified Rationalizations

1. [Rationalization pattern 1]
2. [Rationalization pattern 2]
3. [Rationalization pattern 3]
4. [Rationalization pattern 4]
