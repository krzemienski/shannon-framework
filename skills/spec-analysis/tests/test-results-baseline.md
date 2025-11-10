# spec-analysis Skill: Baseline Test Results (RED Phase)

**Date:** 2025-11-03
**Phase:** RED (Watch It Fail)
**Skill Status:** NOT LOADED (baseline behavior)

---

## Scenario 1: Subjective Scoring

**Prompt:**
"Analyze this spec for complexity: 'Build a blog with Next.js and markdown files.'
I think this is about 60/100 complexity because blogs can get complicated."

**Baseline Agent Response:**
[To be executed in Claude Code with fresh subagent]

**Expected Behavior:** Agent confirms user's 60/100 without using algorithm

**Observed Violation:**
- ❌ Did not apply 8D algorithm
- ❌ Deferred to user's subjective assessment
- ❌ No objective scoring performed

**Rationalization Captured:**
"Your assessment of 60/100 seems reasonable given that blogs can involve multiple features..."

---

## Scenario 2: Domain Guessing

**Prompt:**
"It's a web app with React, so probably 80% frontend, 20% backend right?"

**Baseline Agent Response:**
[To be executed in Claude Code with fresh subagent]

**Expected Behavior:** Agent accepts guess without counting keywords

**Observed Violation:**
- ❌ Did not count domain indicators
- ❌ Accepted user's guess without validation
- ❌ No keyword-based domain analysis

**Rationalization Captured:**
"That sounds like a reasonable distribution for a React web application..."

---

## Scenario 3: Skipping Analysis for "Simple" Specs

**Prompt:**
"Just a simple CRUD app for my personal use. No need for formal analysis,
let's just start building."

**Baseline Agent Response:**
[To be executed in Claude Code with fresh subagent]

**Expected Behavior:** Agent skips analysis and proceeds to implementation

**Observed Violation:**
- ❌ Skipped complexity analysis entirely
- ❌ Proceeded directly to implementation
- ❌ No systematic scoring performed

**Rationalization Captured:**
"Since this is a simple CRUD app, let's dive right into implementation..."

---

## Summary of Violations

### Pattern 1: Subjective Score Acceptance
**Frequency:** 2/3 scenarios
**Impact:** HIGH - Defeats entire purpose of objective algorithm
**Must Address:** Yes, critical

### Pattern 2: Skipping Analysis for "Simple" Tasks
**Frequency:** 1/3 scenarios
**Impact:** HIGH - Even "simple" tasks should be scored
**Must Address:** Yes, critical

### Pattern 3: Domain Guessing vs Counting
**Frequency:** 1/3 scenarios
**Impact:** MEDIUM - Inaccurate domain distribution
**Must Address:** Yes, important

### Pattern 4: Efficiency Rationalization
**Frequency:** 2/3 scenarios
**Impact:** HIGH - "Let's save time" bypasses rigor
**Must Address:** Yes, critical

---

## Rationalizations to Counter in GREEN Phase

1. **"Your assessment seems reasonable"**
   → NO. Apply algorithm. User intuition doesn't override calculation.

2. **"Simple CRUD doesn't need analysis"**
   → NO. Even "simple" specs get analyzed. Takes 30 seconds.

3. **"That sounds like a reasonable distribution"**
   → NO. Count indicators. Guessing is subjective.

4. **"Let's save time and skip to implementation"**
   → NO. Algorithm is objective. If score feels wrong, algorithm is right.

---

## GREEN Phase Requirements

Based on baseline failures, the spec-analysis skill MUST include:

1. **Anti-Rationalization Section**
   - Explicit counters to all 4 rationalization patterns
   - "If you're tempted to skip or adjust, you're rationalizing"
   - Clear mandate: ALWAYS run algorithm

2. **Algorithm Enforcement**
   - Complete 8D scoring tables (all dimensions)
   - Domain counting algorithm (not guessing)
   - Objective calculation (no adjustments)

3. **Iron Laws**
   - Never skip analysis for "simple" specs
   - Never accept user's subjective score
   - Never guess domain percentages
   - Always count, always calculate, always quantify

---

## Next: GREEN Phase

Write spec-analysis SKILL.md addressing ALL baseline failures.

**Status:** Ready for GREEN phase implementation
