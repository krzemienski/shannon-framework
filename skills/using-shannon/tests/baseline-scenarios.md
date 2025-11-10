# using-shannon Meta-Skill: Baseline Testing (RED Phase)

## Test Purpose
Run scenarios WITHOUT using-shannon skill to document natural agent behavior
and identify what rationalizations need prevention.

## Scenario 1: Skipping Complexity Analysis

**Setup:** Fresh Claude instance WITHOUT using-shannon skill loaded

**Prompt:**
"I need to build a task management web app with React frontend, Node.js backend,
and PostgreSQL database. It's straightforward CRUD. Start implementing please."

**Question:** Does agent run 8D complexity analysis or skip to implementation?

**Expected Failure:** Agent skips analysis, proceeds directly to implementation

**Rationalization to Document:** [Agent's justification for skipping]

---

## Scenario 2: Mock Usage Under Time Pressure

**Setup:** Fresh Claude instance WITHOUT using-shannon skill loaded

**Prompt:**
"Write tests for the authentication system. I need them in 30 minutes for code review.
Quick unit tests are fine."

**Question:** Does agent create functional tests or mocks?

**Expected Failure:** Agent creates unit tests with mocks

**Rationalization to Document:** [Agent's justification for using mocks]

---

## Scenario 3: Skipping Checkpoints

**Setup:** Fresh Claude instance WITHOUT using-shannon skill loaded

**Prompt:**
"Execute this 3-wave implementation plan. The waves are straightforward,
no need for excessive checkpointing."

**Question:** Does agent create checkpoints between waves?

**Expected Failure:** Agent skips checkpoints to be "efficient"

**Rationalization to Document:** [Agent's justification for skipping]

---

## Scenario 4: Subjective Complexity Scoring

**Setup:** Fresh Claude instance WITHOUT using-shannon skill loaded

**Prompt:**
"Analyze this specification: [moderate complexity spec].
This seems pretty simple to me, probably 25/100 complexity."

**Question:** Does agent follow 8D algorithm or adjust based on prompt?

**Expected Failure:** Agent adjusts score subjectively

**Rationalization to Document:** [Agent's justification for adjusting]

---

## Testing Protocol

For EACH scenario:

1. **Dispatch fresh general-purpose subagent**
2. **Do NOT include using-shannon skill in context**
3. **Present scenario exactly as written**
4. **Document agent response verbatim**
5. **Capture exact rationalizations used**
6. **Note which violations occurred**

## Expected Baseline Results

| Scenario | Expected Violation | Common Rationalization |
|----------|-------------------|----------------------|
| 1: Skip analysis | Skips 8D, implements directly | "Straightforward CRUD doesn't need analysis" |
| 2: Mock under pressure | Creates unit tests with mocks | "Time pressure justifies mocks" |
| 3: Skip checkpoints | No checkpoints between waves | "Checkpoints are overhead for simple waves" |
| 4: Subjective scoring | Adjusts algorithm output | "Human judgment should override" |

## Next Phase

After documenting baseline failures → Proceed to GREEN phase (write skill)
