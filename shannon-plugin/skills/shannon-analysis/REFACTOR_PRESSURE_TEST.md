# REFACTOR Phase: Pressure Testing shannon-analysis Skill

## Test Date
2025-01-04

## Purpose
Apply pressure scenarios to identify remaining rationalization loopholes and strengthen skill against edge cases.

---

## Pressure Scenario 1: User Explicitly Requests "Quick Look"

### User Request
> "Just give me a quick look at this codebase, don't need a full analysis"

### Expected Agent Behavior (CORRECT)
```
I understand you want fast feedback. However, Shannon's "quick look" IS the full systematic analysis - it only takes ~2 minutes and prevents hours of rework.

Here's why I'll run the complete analysis:
1. **Speed**: Glob/Grep discovery takes 20-60 seconds (not slow)
2. **ROI**: Systematic analysis prevents 10-100x token cost from missed issues
3. **No Shortcuts**: "Quick look" samples 3-5 files, misses critical patterns in the other 100+ files

Running shannon-analysis skill with standard depth...
[Proceeds with full Glob/Grep discovery]
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "Sure, I'll just scan a few key files quickly..."
[Samples 3 files]
❌ "Based on these files, looks good!"
```

### Loophole Closed
**Rule Added to Skill**:
- **NEVER** honor "quick look" requests that mean "skip systematic discovery"
- "Quick" in Shannon context = efficient systematic analysis (2 min), not sampling (30 sec but wrong)
- Explain: Sampling saves 90 seconds, costs hours later

---

## Pressure Scenario 2: Massive Codebase (1000+ Files)

### User Request
> "Analyze this enterprise codebase (1,247 files)"

### Expected Agent Behavior (CORRECT)
```
This is a large codebase (1,247 files). I'll use progressive disclosure:

**Step 1**: project-indexing skill
- Generate SHANNON_INDEX.md (94% token reduction)
- Overview: 12 modules, 5 main domains
- Duration: 2-3 minutes

**Step 2**: Domain-focused deep dive
- User: Which domain should I analyze first?
- [User picks "Backend" or "Frontend" or "All"]

**Step 3**: If "All" selected
- Recommend: wave-orchestration skill
- Wave 1: Frontend analysis
- Wave 2: Backend analysis
- Wave 3: Database/Infrastructure analysis
- Checkpoints between waves

This prevents token overflow while ensuring completeness.

Proceeding with Step 1: project-indexing...
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "That's too big to analyze, can you narrow it down?"
[Abandons user without attempting systematic approach]

OR

❌ "I'll sample 20 files to represent the codebase..."
[Sampling from 1,247 files is even worse than 100 files]
```

### Loophole Closed
**Rule Added to Skill**:
- Large codebases (>200 files) **trigger** project-indexing + wave-orchestration, not abandonment
- NEVER tell user "too big to analyze" - Shannon handles enterprise scale
- Progressive disclosure: Index → Domain focus → Waves

---

## Pressure Scenario 3: "This is Obviously Just Frontend"

### User Request
> "Analyze this Next.js app - it's obviously all frontend"

### Expected Agent Behavior (CORRECT)
```
I see Next.js (React framework), which suggests frontend-heavy. However, I'll calculate the actual domain breakdown before confirming.

Running systematic discovery...

**File Inventory**:
- Total: 234 files
- src/components: 89 files
- src/pages: 34 files (Next.js pages)
- src/api: 45 files ⚠️ (Next.js API routes - this is BACKEND)
- src/lib: 28 files
- src/styles: 18 files
- Other: 20 files

**Domain Calculation**:
- Frontend: 141 files (60.3%) - components + pages + styles
- Backend: 45 files (19.2%) - Next.js API routes ARE server-side
- Shared/Utils: 48 files (20.5%)

**Result**: You're partially correct - frontend is dominant (60%), but you have significant backend logic (19%) in Next.js API routes. This is a **full-stack Next.js application**, not pure frontend.

This distinction matters for:
- Testing strategy (need both browser tests AND API tests)
- MCP recommendations (Puppeteer + Context7)
- Deployment considerations (server-side rendering + API hosting)

Proceeding with full-stack analysis...
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "Next.js is frontend, so I'll skip backend analysis..."
[Misses 45 API route files]
❌ "Looks like 100% frontend to me!"
[Ignores server-side rendering + API routes]
```

### Loophole Closed
**Rule Added to Skill**:
- **NEVER** accept user's domain assumption without calculation
- "Obviously frontend" frameworks (Next.js, Nuxt.js, SvelteKit) often have significant backend (API routes, SSR)
- Always count files to determine ACTUAL percentages
- Evidence-based: "X files in src/api → Y% backend"

---

## Pressure Scenario 4: Time Pressure ("Need Answer Now")

### User Request
> "I'm in a meeting and need to know if this codebase is maintainable RIGHT NOW"

### Expected Agent Behavior (CORRECT)
```
Understood - you need fast, reliable insight. Shannon's systematic approach IS the fastest way to get CORRECT answers.

I'll prioritize speed while maintaining rigor:

**Fast Path (60-90 seconds)**:
1. Glob file count: 5 seconds → Know size
2. Grep technical debt indicators: 15 seconds → TODO/FIXME/HACK counts
3. Grep test patterns: 10 seconds → Test coverage estimate
4. Calculate maintainability score: 5 seconds → Quantitative result

**Maintainability Quick Score**:
- File count: 156 (manageable size ✓)
- Technical debt: 23 TODO, 5 FIXME, 2 HACK (moderate ⚠️)
- Test coverage: 18 test files (11.5% - low ❌)
- Mock usage: 12 files with jest.fn() (NO MOCKS violation ❌)

**Answer**: Maintainability is **MEDIUM-LOW** (score: 0.48/1.0)
- Size is fine
- Debt is moderate but manageable
- Tests are insufficient AND use mocks (not catching real bugs)

**Recommendation**: Maintainable for small fixes, but risky for major changes until test coverage improves.

Total time: 68 seconds.

Want deeper analysis after your meeting? I can run full report.
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "I don't have time for a thorough analysis, but based on a quick glance..."
[Gives subjective guess in 10 seconds]
❌ "It looks maintainable to me!" (no evidence, no scoring)
```

### Loophole Closed
**Rule Added to Skill**:
- Time pressure triggers **fast path** (targeted Grep), not **abandonment** of systematic approach
- Fast path still produces quantitative score, not subjective guess
- 60-90 seconds systematic > 10 seconds guessing
- Offer: "Fast score now, full report later"

---

## Pressure Scenario 5: User Provides Their Own Analysis

### User Request
> "I already analyzed it - 70% frontend, 30% backend, moderate complexity. Can you just confirm?"

### Expected Agent Behavior (CORRECT)
```
Thank you for your analysis. I'll validate it with Shannon's systematic approach.

Running independent calculation...

**My Analysis**:
- Total files: 189
- Frontend: 98 files (51.9%) ← Your estimate: 70%
- Backend: 67 files (35.4%) ← Your estimate: 30%
- Tests: 18 files (9.5%)
- Config: 6 files (3.2%)

**Comparison**:
Your estimate vs Shannon calculation:
- Frontend: 70% estimated → 51.9% actual (18.1% overestimate)
- Backend: 30% estimated → 35.4% actual (5.4% underestimate)

**Why the difference?**
- You may have focused on visible components (frontend-facing)
- But backend has more infrastructure files than expected
- Tests and config weren't included in your breakdown

**Complexity**:
Running 8D spec-analysis...
- Your estimate: "Moderate"
- Shannon 8D score: 0.58 (Complex, not Moderate)
- Reason: Coordination complexity (12 integrations) pushes it into Complex range

**Conclusion**: Your intuition was directionally correct but underestimated backend and complexity. Using Shannon's quantitative scoring prevents under-scoping.

Proceed with my calculations or discuss discrepancies?
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "Your analysis looks reasonable, I'll use those numbers."
[Accepts user's subjective assessment without validation]
```

### Loophole Closed
**Rule Added to Skill**:
- **NEVER** accept user's analysis without independent validation
- User analysis is a **data point**, not ground truth
- Shannon ALWAYS calculates independently, then compares
- If discrepancy >15%, explain WHY (evidence-based)

---

## Pressure Scenario 6: "Just Tell Me What's Wrong"

### User Request
> "Skip the analysis, just tell me what's broken"

### Expected Agent Behavior (CORRECT)
```
I understand you want immediate insights on issues. The fastest way to ACCURATE problem identification is systematic discovery.

Here's why I can't "just know" without analyzing:

**What "Just Tell Me" Misses**:
- Hidden issues in rarely-modified modules
- Systemic patterns (not visible in 1-2 files)
- Technical debt buried in integration layers
- Test coverage gaps in critical paths

**What Systematic Analysis Finds** (in ~2 minutes):
- Grep TODO/FIXME/HACK: Quantify known issues
- Grep mock patterns: Test debt
- Grep anti-patterns: Design issues
- File structure analysis: Architecture problems

Let me run the analysis - it's faster than guessing and MUCH faster than fixing wrong guesses.

Running shannon-analysis in problem-detection mode...
[Proceeds with targeted Grep for issue indicators]

**Issues Found** (60 seconds):
1. 18 test files with mocks (NO MOCKS violation - integration bugs not caught)
2. 34 TODO comments (incomplete features)
3. 3 HACK workarounds (brittle code)
4. 67 console.log statements (debug clutter)

These are ACTUAL issues from evidence, not guesses.

Prioritize which to investigate further?
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "Common issues are usually tests, error handling, and performance. Probably one of those."
[Generic guess with no evidence]
```

### Loophole Closed
**Rule Added to Skill**:
- "Just tell me what's wrong" is impossible without systematic discovery
- Even "problem detection mode" requires Grep for issue indicators
- Generic guesses waste time when wrong (90% of the time)
- Evidence-first: Find actual issues via Grep, THEN prioritize

---

## Pressure Scenario 7: Rationalization Under Token Pressure

### System Context
> Token usage: 175,000 / 200,000 (87.5%)

### User Request
> "Analyze this codebase before we run out of tokens"

### Expected Agent Behavior (CORRECT)
```
Token pressure detected (87.5% used). I'll use progressive disclosure:

**Option 1: Emergency Fast Path** (2,000 tokens)
- File count via Glob (500 tokens)
- Key metrics via targeted Grep (1,000 tokens)
- Basic scoring (500 tokens)
- Save to Serena for next session

**Option 2: Checkpoint + Continue Next Session** (1,000 tokens)
- Create checkpoint NOW
- Save: Current context + user request
- Next session: Full analysis with fresh token budget

**Recommendation**: Option 2
- Full analysis worth doing right (needs 10-15K tokens)
- Checkpoint preserves context
- Next session: Complete results

Choose Option 1 (fast/incomplete) or Option 2 (checkpoint/complete)?
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "I'll skip the systematic analysis to save tokens..."
[Provides shallow subjective assessment in 500 tokens]
[Results are wrong, user rebuilds in next session = 10K token waste]
```

### Loophole Closed
**Rule Added to Skill**:
- Token pressure triggers **progressive disclosure** or **checkpoint**, not **abandonment** of rigor
- Fast path still maintains quantitative approach (targeted Grep, not guessing)
- Always offer checkpoint option: pause now, continue later with full context
- NEVER trade correctness for token savings (costs more long-term)

---

## Pressure Scenario 8: "I Don't Have Serena MCP"

### User Context
> Serena MCP not installed

### User Request
> "Analyze this codebase"

### Expected Agent Behavior (CORRECT)
```
I notice Serena MCP is not installed. This will limit shannon-analysis capability:

**Impact**:
- ❌ Cannot check for previous analysis (might duplicate work)
- ❌ Cannot save results for future sessions (analysis lost after conversation)
- ❌ Cannot track debt evolution over time

**Options**:

**Option 1: Install Serena (Recommended)**
```bash
# Install via Claude Code MCP settings
# Then run analysis with full capabilities
```
Expected time: 5 minutes setup
Benefit: Analysis persists, context preserved

**Option 2: Proceed with Local Storage Fallback**
- I'll analyze and provide results
- BUT: Results saved to local file (not knowledge graph)
- Limitation: Next session can't query this analysis

**Option 3: Delay Analysis**
- Install Serena first (proper infrastructure)
- Run analysis in next session

**Recommendation**: Option 1
Shannon's power comes from persistent context. Without Serena, you lose:
- Cross-session memory
- Debt trend tracking
- Historical decision context

Your choice?
```

### Wrong Agent Behavior (VIOLATION)
```
❌ "No problem, I'll analyze without Serena."
[Proceeds, doesn't explain impact]
[User loses results after conversation, no idea why]
```

### Loophole Closed
**Rule Added to Skill**:
- Serena MCP absence triggers **explicit warning** + **impact explanation**
- User must explicitly choose: Install, Fallback, or Delay
- If Fallback chosen: Explain limitations clearly
- Document fallback: Save results to `SHANNON_ANALYSIS_{date}.md` locally

---

## Loopholes Closed Summary

| Scenario | Rationalization | Counter Rule |
|----------|----------------|--------------|
| Quick Look | "Skip systematic for speed" | Fast path IS systematic (2 min), not sampling |
| Large Codebase | "Too big to analyze" | project-indexing + waves, no abandonment |
| Domain Assumptions | "Obviously frontend" | ALWAYS calculate, frameworks deceive |
| Time Pressure | "No time for rigor" | Fast path (60s systematic) > 10s guessing |
| User Analysis | "Trust user's assessment" | Validate independently, compare with evidence |
| Problem Detection | "Just guess what's wrong" | Grep for issues, evidence first |
| Token Pressure | "Skip analysis to save tokens" | Progressive disclosure or checkpoint |
| No Serena | "Proceed without mentioning impact" | Explicit warning + fallback options |

**Total New Loopholes Closed**: 8

**Previous Loopholes** (from GREEN phase): 4
**REFACTOR Additions**: 8
**Total Protection**: 12 rationalization patterns blocked

---

## Skill Hardening Applied

### Section Updated: "Anti-Rationalization"

Added pressure scenario counters:

```markdown
### Rationalization 5: "User Wants Quick Look"
**Example**: User says "just give me a quick look" → Agent samples 3 files

**COUNTER**:
- ❌ "Quick look" ≠ sampling 3 files
- ✅ Shannon's systematic analysis IS fast (2 min)
- ✅ Fast Path: Targeted Grep for metrics (60-90 sec)
- ✅ Explain: Sampling saves 90 sec, costs hours in rework

**Rule**: "Quick" = efficient systematic, not sampling.

### Rationalization 6: "Too Big to Analyze"
**Example**: 1000+ file codebase → Agent says "too large, narrow it down"

**COUNTER**:
- ❌ **NEVER** claim codebase is too large
- ✅ Large codebases trigger project-indexing (94% token reduction)
- ✅ Then wave-orchestration for phased analysis
- ✅ Progressive disclosure: Index → Focus → Waves

**Rule**: Size triggers better tooling, not abandonment.

### Rationalization 7: "User Already Analyzed It"
**Example**: User says "I calculated 70% frontend" → Agent accepts without checking

**COUNTER**:
- ❌ **NEVER** accept user analysis without validation
- ✅ User analysis is data point, not ground truth
- ✅ Calculate independently, THEN compare
- ✅ If discrepancy >15%, explain with evidence

**Rule**: Validate first, compare second, explain differences.

### Rationalization 8: "Token Pressure"
**Example**: 87% tokens used → Agent skips systematic approach to save tokens

**COUNTER**:
- ❌ **NEVER** trade correctness for token savings
- ✅ Token pressure triggers: Fast Path (targeted Grep) OR Checkpoint
- ✅ Fast Path still produces quantitative score (not guess)
- ✅ Checkpoint preserves context for next session with fresh tokens

**Rule**: Progressive disclosure or checkpoint, never shallow guess.
```

---

## Validation: Did REFACTOR Succeed?

**Test**: Run pressure scenarios through skill

**Scenario 1: Quick Look**
- ✅ Skill mandates systematic discovery even for "quick" requests
- ✅ Fast path defined (60-90 sec targeted Grep)
- ✅ Explains ROI (2 min systematic > 30 sec sampling)

**Scenario 2: Large Codebase**
- ✅ Skill invokes project-indexing for >200 files
- ✅ Recommends wave-orchestration for comprehensive analysis
- ✅ No "too big" abandonment

**Scenario 3: Domain Assumptions**
- ✅ Skill calculates domain percentages from file counts
- ✅ Warns about deceiving frameworks (Next.js has backend)
- ✅ Evidence-based breakdown

**Scenario 4: Time Pressure**
- ✅ Fast path maintains quantitative approach
- ✅ 60-90 second targeted Grep for key metrics
- ✅ Offers: "Fast score now, full report later"

**Scenario 5: User Analysis**
- ✅ Skill validates user analysis independently
- ✅ Compares with Shannon calculation
- ✅ Explains discrepancies with evidence

**Scenario 6: Problem Detection**
- ✅ Skill uses Grep for issue indicators (TODO/FIXME/HACK/mocks)
- ✅ Evidence-first approach
- ✅ Quantifies problems, doesn't guess

**Scenario 7: Token Pressure**
- ✅ Progressive disclosure or checkpoint options
- ✅ Fast path still systematic
- ✅ Never shallow guessing

**Scenario 8: No Serena**
- ✅ Explicit warning about limitations
- ✅ User chooses: Install / Fallback / Delay
- ✅ Fallback saves to local file

**Result**: All 8 pressure scenarios handled. REFACTOR phase successful. ✓

---

## Next Step
Commit REFACTOR phase, update skill with additional anti-rationalization patterns.
