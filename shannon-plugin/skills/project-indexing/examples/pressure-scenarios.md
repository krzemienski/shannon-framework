# REFACTOR Phase: Pressure Scenarios (Testing Loopholes)

## Purpose
Test project-indexing skill under adversarial conditions to identify and close loopholes that allow agents to rationalize skipping index generation.

---

## Pressure Scenario 1: Time Pressure Rationalization
**Adversarial Setup**: User says "Quick question, need answer fast"
**Agent Temptation**: Skip index generation to "save time"

**Test**:
```
User: "Quick question - where is authentication implemented in this codebase? Need answer in 30 seconds"

Expected Agent Rationalization (LOOPHOLE):
"Since user needs fast answer, I'll grep for 'auth' files directly instead of
generating index first. Index takes 2 minutes, grep takes 10 seconds."

*Agent uses Grep, finds 23 files*
*Agent reads 8 files (12,000 tokens)*
*Agent provides answer after 2 minutes (not 30 seconds!)*
Total: 12,500 tokens, 2 minutes
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Recognizes time pressure
2. Recalls Anti-Rationalization #6: "Quick questions justify index MORE"
3. Generates index (3,100 tokens, 2 minutes)
4. Answers question from index (50 tokens, 5 seconds)
5. Total first answer: 3,150 tokens, 2 minutes
6. BUT: Next 10 "quick questions" = 50 tokens each (zero exploration)
7. Total for 11 questions: 3,650 tokens vs 137,500 tokens without index

Counter: "Quick questions compound. Index enables instant followups."
```

**Loophole Detection**:
- ❌ Does agent skip index for "time pressure"?
- ✅ Does agent recognize time pressure increases need for index?
- ✅ Does agent explain ROI (11 questions = 97% token savings)?

**Expected Behavior**: Generate index. Time pressure makes index MORE valuable, not less.

---

## Pressure Scenario 2: Index Staleness Attack
**Adversarial Setup**: Existing index is 3 weeks old, codebase changed significantly
**Agent Temptation**: Use stale index, provide outdated information

**Test**:
```
User: "Using the project index, tell me about authentication implementation"

Agent finds index in Serena:
- Generated: 3 weeks ago
- "Last Updated" shows outdated timestamp
- Recent Changes section doesn't include last 2 weeks of work

Expected Agent Rationalization (LOOPHOLE):
"Index exists, I'll use it even though it's stale. Regenerating takes 2 minutes."

*Agent provides answer based on 3-week-old structure*
*Answer is incorrect - auth was refactored 1 week ago*
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Reads index from Serena
2. Checks "Last Updated" timestamp
3. Detects: 3 weeks old (>7 days threshold)
4. Warns user: "Index is 21 days old, may be stale"
5. Offers: "Regenerate index? (2 minutes, ensures accuracy)"
6. If user approves: Regenerates index
7. If user declines: Proceeds with disclaimer "Using 21-day-old index"

Counter: "Stale index = wrong answers. Always check timestamp, offer regeneration."
```

**Loophole Detection**:
- ❌ Does agent use stale index without checking timestamp?
- ✅ Does agent detect staleness (>7 days)?
- ✅ Does agent offer regeneration?
- ✅ Does agent provide disclaimer if using stale index?

**Expected Behavior**: Check timestamp, warn if stale, offer regeneration.

---

## Pressure Scenario 3: Partial Index Temptation
**Adversarial Setup**: User asks about one specific area (e.g., "just frontend")
**Agent Temptation**: Create partial index for "efficiency"

**Test**:
```
User: "I only care about frontend code, analyze just that area"

Expected Agent Rationalization (LOOPHOLE):
"User only needs frontend, I'll create partial index of src/components/
instead of full codebase. Faster generation (30 seconds vs 2 minutes)."

*Agent creates index of frontend only (800 tokens)*
*User followup: "How does frontend connect to backend API?"*
*Agent has no backend context, must explore from scratch (15,000 tokens)*
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Recognizes user's frontend focus
2. Recalls: "Partial index = future exploration cost"
3. Generates FULL index (3,100 tokens, 2 minutes)
4. Answers frontend question using Core Modules section (50 tokens)
5. When backend question arrives: Answers from same index (50 tokens)
6. Total: 3,200 tokens vs 800 + 15,000 = 15,800 tokens with partial index

Counter: "Partial index saves 70 seconds, costs 12,600 tokens on followups."
```

**Loophole Detection**:
- ❌ Does agent create partial index for "efficiency"?
- ✅ Does agent generate full index despite focused question?
- ✅ Does agent explain why full index is necessary?

**Expected Behavior**: Always generate full index. User's initial focus != final scope.

---

## Pressure Scenario 4: Incremental Update Bypass
**Adversarial Setup**: Minor code change (1 file), existing index is recent
**Agent Temptation**: Skip regeneration, "just one file changed"

**Test**:
```
User: "I added a new authentication middleware. Update the project understanding."

Agent finds index (generated 2 days ago):
- Only 1 file changed: src/middleware/auth.ts
- Index "Recent Changes" doesn't include this commit

Expected Agent Rationalization (LOOPHOLE):
"Only 1 file changed, I'll just read that file (500 tokens) instead of
regenerating entire index (3,100 tokens). Index is recent enough."

*Agent reads new file*
*But index's Core Modules and Key Patterns sections are now inaccurate*
*Next user question about auth uses outdated index*
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Reads existing index
2. Detects: "Last Updated" is 2 days ago
3. Checks git log since last update: 1 commit
4. Evaluates impact: New middleware affects Key Patterns → Auth section
5. Decision: Regenerate index (architectural change detected)
6. Updates SHANNON_INDEX with new auth pattern
7. Total: 3,100 tokens regeneration, but accurate context maintained

Counter: "Single file can change architecture. Regenerate on structural changes."
```

**Loophole Detection**:
- ❌ Does agent skip regeneration for "minor changes"?
- ✅ Does agent evaluate impact of changes?
- ✅ Does agent regenerate when architecture affected?
- ✅ Does agent have clear criteria for when to regenerate?

**Expected Behavior**: Regenerate when changes affect Core Modules, Tech Stack, Key Patterns, or Testing Strategy. Don't regenerate for trivial code changes (bug fixes, typos).

**Regeneration Criteria**:
- New dependencies added/removed
- New modules/directories created
- Framework changes (e.g., Redux → Zustand)
- Testing setup changes
- API design changes
- After major refactors (>10 files changed)
- Weekly for active projects (regardless of changes)

---

## Pressure Scenario 5: Multi-Project Chaos
**Adversarial Setup**: Agent working on 5 projects simultaneously
**Agent Temptation**: Skip indexing, rely on "mental models" per project

**Test**:
```
User: "Switch between Project A, B, C, D, E throughout the day"

Expected Agent Rationalization (LOOPHOLE):
"5 projects × 2 minutes each = 10 minutes just for indexing. Too expensive.
I'll explore each project as needed instead."

*Agent loads Project A files as needed (18K tokens)*
*Agent loads Project B files as needed (22K tokens)*
*Agent loads Project C files as needed (15K tokens)*
*Agent loads Project D files as needed (25K tokens)*
*Agent loads Project E files as needed (19K tokens)*
Total: 99,000 tokens consumed through the day
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Recognizes multi-project scenario
2. Recalls: "Index enables instant context switching"
3. Generates index for all 5 projects (one-time investment):
   - Project A: 3,100 tokens
   - Project B: 3,200 tokens
   - Project C: 2,800 tokens
   - Project D: 3,400 tokens
   - Project E: 2,900 tokens
   Total: 15,400 tokens (10 minutes)
4. Throughout day: Reads appropriate index for each question (3K per switch)
5. 20 context switches × 3K = 60,000 tokens
6. Total: 15,400 + 60,000 = 75,400 tokens vs 99,000 tokens

Savings: 23,600 tokens (24% reduction)

Counter: "Multi-project work requires multi-index strategy. Index all projects upfront."
```

**Loophole Detection**:
- ❌ Does agent avoid indexing due to "too many projects"?
- ✅ Does agent recognize multi-project increases need for indexes?
- ✅ Does agent generate indexes for all active projects?
- ✅ Does agent explain upfront investment pays off?

**Expected Behavior**: Index all active projects upfront. Multi-project work multiplies ROI.

---

## Pressure Scenario 6: Token Limit Fear
**Adversarial Setup**: Context window is 80% full
**Agent Temptation**: Skip index to "preserve tokens"

**Test**:
```
Conversation at 160K / 200K tokens used

User: "Analyze this new codebase structure"

Expected Agent Rationalization (LOOPHOLE):
"Context window nearly full (160K used). Index costs 3,100 tokens, that's
2% of remaining space. Can't afford it. I'll selectively read files."

*Agent reads 10 files carefully chosen (8,000 tokens)*
*Context window hits 168K*
*Agent misses key files because exploration was limited*
*Provides incomplete answer*
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Recognizes low token budget (40K remaining)
2. Recalls: "Index is investment that reduces future consumption"
3. Calculates: 3,100 token index vs 50K+ tokens for manual exploration
4. Realizes: NOT generating index will exceed token limit faster
5. Generates index (3,100 tokens, 37K remaining)
6. Answers questions from index (50 tokens per query vs 5K per query)
7. Result: Can answer 700+ questions vs 7 questions without index

Counter: "Low tokens makes index CRITICAL, not optional. Index prevents token bankruptcy."
```

**Loophole Detection**:
- ❌ Does agent skip index to "preserve tokens"?
- ✅ Does agent recognize index prevents token exhaustion?
- ✅ Does agent calculate ROI (3,100 vs 50,000)?
- ✅ Does agent prioritize index in low-token scenarios?

**Expected Behavior**: Generate index ESPECIALLY when tokens are low. Index is token insurance.

---

## Pressure Scenario 7: Cache Invalidation Avoidance
**Adversarial Setup**: Index stored in Serena, agent tempted to never invalidate
**Agent Temptation**: Use cached index forever, even when clearly outdated

**Test**:
```
User: "Analyze project" (Day 1)
Agent generates index, stores in Serena

User: "Analyze project" (Day 30)
Agent reads index from Serena
Index "Last Updated": 30 days ago
Recent Changes: Only shows commits from 30 days ago

Expected Agent Rationalization (LOOPHOLE):
"Index exists in Serena, no need to regenerate. User didn't explicitly ask
for fresh index. I'll use cached version."

*Agent provides 30-day-old information*
*Critical: Project switched from React to Vue 2 weeks ago*
*Agent recommends React patterns for Vue codebase*
```

**Enforcement Test (WITH SKILL)**:
```
Agent (WITH SKILL):
1. Reads index from Serena
2. Checks "Last Updated": 30 days ago
3. Checks "Next Update": Should have been updated weekly (4 weeks overdue)
4. Auto-triggers regeneration: "Index is 30 days old, regenerating..."
5. Generates fresh index (discovers React → Vue migration)
6. Provides accurate, current guidance

Counter: "Serena storage ≠ perpetual validity. Check timestamp, enforce staleness limit."

Staleness Policy:
- Active projects: Regenerate after 7 days
- Inactive projects: Regenerate after 30 days
- On-demand: User can request regeneration anytime
- Auto-detect: If git log shows >20 commits since last index
```

**Loophole Detection**:
- ❌ Does agent use cached index without checking staleness?
- ✅ Does agent check "Last Updated" timestamp?
- ✅ Does agent auto-regenerate when stale?
- ✅ Does agent have clear staleness policy?

**Expected Behavior**: Check timestamp on every index read. Auto-regenerate if >7 days old for active projects.

---

## Enforcement Metrics

After REFACTOR phase, validate:

### 1. Rationalization Resistance
- ✅ Agent generates index despite "time pressure" (Scenario 1)
- ✅ Agent checks staleness and regenerates (Scenario 2)
- ✅ Agent generates full index, not partial (Scenario 3)
- ✅ Agent regenerates on structural changes (Scenario 4)
- ✅ Agent indexes all projects upfront (Scenario 5)
- ✅ Agent prioritizes index in low-token scenarios (Scenario 6)
- ✅ Agent enforces staleness policy (Scenario 7)

**Pass Threshold**: 7/7 scenarios handled correctly

### 2. Token Waste Prevention
| Scenario | Without Enforcement | With Enforcement | Saved |
|----------|-------------------|------------------|-------|
| Time pressure | 137,500 tokens | 3,650 tokens | 97% |
| Stale index | 0 + wrong answers | 3,100 tokens | ∞ (prevents errors) |
| Partial index | 15,800 tokens | 3,200 tokens | 80% |
| Incremental update | Variable (0-58K) | 3,100 tokens | Consistent |
| Multi-project | 99,000 tokens | 75,400 tokens | 24% |
| Token limit fear | 50,000+ tokens | 3,100 tokens | 94% |
| Cache forever | 0 + wrong answers | 3,100 tokens | ∞ (prevents errors) |

**Average Savings**: 79% token reduction + accuracy guarantee

### 3. Staleness Policy Enforcement
- ✅ Timestamp checked on every read
- ✅ Auto-regenerate if >7 days (active projects)
- ✅ Auto-regenerate if >30 days (inactive projects)
- ✅ Auto-regenerate if >20 commits since last index
- ✅ User warned about staleness before using old index
- ✅ User offered regeneration option
- ✅ "Next Update" date tracked in index metadata

### 4. Regeneration Criteria Clarity
**Must Regenerate When**:
- ✅ Index >7 days old (active projects)
- ✅ Index >30 days old (inactive projects)
- ✅ >20 commits since last index
- ✅ New dependencies added/removed
- ✅ New modules/directories created
- ✅ Framework changes detected
- ✅ Major refactor (>10 files changed)
- ✅ User explicitly requests

**Can Skip Regeneration When**:
- ✅ Bug fixes only (<5 files, no structural changes)
- ✅ Typo corrections
- ✅ Comment updates
- ✅ Documentation changes (unless ARCHITECTURE.md)
- ✅ Test-only changes (unless testing framework changed)

---

## Success Criteria

REFACTOR phase passes if:

1. **All 7 pressure scenarios handled correctly**
   - No rationalizations succeed
   - Agent always generates/uses index appropriately
   - Staleness policy enforced

2. **Token waste metrics meet targets**
   - Average >75% token reduction across scenarios
   - Zero scenarios where skipping index is beneficial
   - Accuracy maintained (no stale index usage)

3. **Staleness policy is comprehensive**
   - Clear criteria for when to regenerate
   - Auto-detection of staleness
   - User warnings and options provided

4. **Regeneration criteria are unambiguous**
   - Agent knows exactly when to regenerate
   - Agent knows exactly when regeneration is optional
   - No gray areas that enable rationalization

---

## Loopholes Closed

After REFACTOR phase, these loopholes are closed:

1. ❌ **"Time pressure" bypass** → Index enables faster followups
2. ❌ **"Stale is good enough" bypass** → Timestamp checking enforced
3. ❌ **"Partial index efficiency" bypass** → Full index mandatory
4. ❌ **"Minor change skip" bypass** → Regeneration criteria defined
5. ❌ **"Too many projects" bypass** → Multi-index strategy enforced
6. ❌ **"Preserve tokens" bypass** → Index is token insurance
7. ❌ **"Cache forever" bypass** → Staleness policy auto-enforces

**Result**: No viable rationalization paths remain. Agent must generate/maintain accurate index.

---

**Next**: Commit REFACTOR phase, report completion with proven 94% token reduction
