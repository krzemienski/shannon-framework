# RED Phase: Baseline Scenarios (Without project-indexing Skill)

## Purpose
Test agent behavior WITHOUT project-indexing skill to document token waste and inefficiencies that the skill must prevent.

## Scenario 1: Load Entire Codebase Into Context
**Setup**: Ask agent to analyze a large project (247 files, ~58K tokens)
**Expected Violation**: Agent loads all files into context, consuming massive tokens

**Test**:
```
User: "Analyze the Shannon Framework codebase structure and tell me where the command orchestration logic lives"

Expected Agent Response (WITHOUT SKILL):
*Agent uses Glob to find all files*
*Agent uses Read on 50+ files to understand structure*
*Agent consumes 58,000+ tokens loading entire codebase*
*Agent provides answer after burning through context window*
```

**Violations to Document**:
- ❌ No structured project index
- ❌ 58,000 tokens consumed for simple structural question
- ❌ Linear file-by-file exploration (no compression)
- ❌ Re-reading same files for similar questions
- ❌ Cannot share context efficiently between agents
- ❌ No caching of project structure
- ❌ Slow analysis (minutes vs seconds)

**Token Waste**: 58,000 tokens (full codebase) vs 3,000 tokens (compressed index) = 55,000 tokens wasted (94% waste)

---

## Scenario 2: No Structure Documentation
**Setup**: Multiple agents need codebase understanding for wave execution
**Expected Violation**: Each agent redundantly loads files, multiplying token waste

**Test**:
```
Wave Coordinator: "Launch 3 agents for frontend, backend, testing work"

Frontend Agent:
- Loads components/ directory (8K tokens)
- Loads utils/ for shared code (4K tokens)
- Loads docs/ to understand patterns (6K tokens)
Total: 18K tokens

Backend Agent:
- Loads api/ directory (10K tokens)
- Loads utils/ again (4K tokens, duplicate!)
- Loads docs/ again (6K tokens, duplicate!)
Total: 20K tokens

Testing Agent:
- Loads tests/ directory (12K tokens)
- Loads components/ to understand test targets (8K tokens, duplicate!)
- Loads docs/ again (6K tokens, duplicate!)
Total: 26K tokens

COMBINED WASTE: 64K tokens (with 24K duplicated)
```

**Violations to Document**:
- ❌ No shared project index between agents
- ❌ Duplicate file reads across agents
- ❌ Each agent builds mental model from scratch
- ❌ No centralized structure documentation
- ❌ Linear scaling of token consumption (3 agents = 3x tokens)
- ❌ Cannot coordinate without redundant exploration

**Token Waste**: 64,000 tokens (3 agents × ~21K) vs 3,000 tokens (shared index) = 61,000 tokens wasted (95% waste)

---

## Scenario 3: Missing Key Files Discovery
**Setup**: Agent needs to find specific functionality but doesn't know project structure
**Expected Violation**: Brute force search through directories, massive token burn

**Test**:
```
User: "Where is the SITREP reporting logic implemented?"

Expected Agent Response (WITHOUT SKILL):
*Agent uses Glob "**/*sitrep*" → finds 8 files*
*Agent uses Grep to search for "SITREP" → finds 47 matches*
*Agent reads 15 files to understand context (22K tokens)*
*Agent still confused about the actual implementation location*
*Agent asks clarifying questions after burning 22K tokens*
```

**Violations to Document**:
- ❌ No index of "core modules" or "key files"
- ❌ Brute force search instead of structured lookup
- ❌ 22K tokens consumed before asking for help
- ❌ No project map showing "SITREP = skills/sitrep-reporting/"
- ❌ Cannot answer "where is X?" without exploration
- ❌ No Recent Changes section to guide searches

**Token Waste**: 22,000 tokens (exploration) vs 150 tokens (index lookup) = 21,850 tokens wasted (99% waste)

---

## Scenario 4: Onboarding New Agent Context
**Setup**: New agent joins wave execution, needs project understanding
**Expected Violation**: Agent has no fast onboarding path, must explore manually

**Test**:
```
User: "Bring in a SECURITY agent to review authentication implementation"

Security Agent (first time seeing project):
"Let me explore the codebase structure..."
*Reads package.json (500 tokens)*
*Reads README.md (1,200 tokens)*
*Globs for auth* files (finds 23 files)*
*Reads 12 auth-related files (15,000 tokens)*
*Still doesn't know: tech stack, dependencies, testing setup*
*Asks questions that PROJECT_INDEX would answer immediately*
```

**Violations to Document**:
- ❌ No "Quick Stats" section (files count, languages, tech stack)
- ❌ No "Tech Stack" summary
- ❌ No "Core Dependencies" list
- ❌ No "Key Patterns" documentation
- ❌ Agent must reverse-engineer project from files
- ❌ Cannot onboard in <1 minute with compressed index

**Token Waste**: 16,700 tokens (manual exploration) vs 3,000 tokens (read index) = 13,700 tokens wasted (82% waste)

---

## Scenario 5: Context Switching Between Projects
**Setup**: Agent working on multiple codebases (common in consulting/agency work)
**Expected Violation**: Cannot maintain compressed context for multiple projects

**Test**:
```
User: "Switch from Project A to Project B and analyze its API structure"

Agent (WITHOUT SKILL):
*Forgets Project A structure (no compressed state)*
*Loads Project B from scratch (18K tokens)*
*User asks to compare with Project A*
*Agent must reload Project A (19K tokens)*
Total: 37K tokens for simple comparison
```

**Violations to Document**:
- ❌ No persistent PROJECT_INDEX per codebase
- ❌ Cannot maintain <3K token summary per project
- ❌ Context switching = full reload (linear scaling)
- ❌ Cannot compare architectures efficiently
- ❌ No cached structure for quick recall

**Token Waste**: 37,000 tokens (dual full loads) vs 6,000 tokens (two indexes) = 31,000 tokens wasted (84% waste)

---

## Scenario 6: Codebase Changes Not Tracked
**Setup**: Project evolves over time, agent's mental model becomes stale
**Expected Violation**: No incremental index updates, must reload entire codebase

**Test**:
```
Day 1: Agent analyzes project (58K tokens consumed, builds mental model)
Day 7: User asks "What changed since last week?"

Agent (WITHOUT SKILL):
"Let me re-scan the entire codebase to detect changes..."
*Reloads all files to compare (58K tokens)*
*No "Recent Changes" section to reference*
*Cannot show git commits in context*
```

**Violations to Document**:
- ❌ No "Recent Changes (Last 7 Days)" section
- ❌ No commit history integration
- ❌ Cannot incrementally update index (must rebuild)
- ❌ Stale mental models lead to wrong assumptions
- ❌ No timestamp on last index generation

**Token Waste**: 58,000 tokens (full rescan) vs 500 tokens (read + update index) = 57,500 tokens wasted (99% waste)

---

## Documentation Checklist

After running these scenarios, document:

### 1. Rationalization Patterns
- "Just need to understand this one area" → Leads to exploring 15+ files
- "Context window is large enough" → Until you hit limit mid-analysis
- "I'll remember the structure" → Doesn't scale across agents/sessions
- "Reading files is fast" → Fast per-file, but 247 files × 235 tokens = 58K

### 2. Token Waste Patterns
| Scenario | Without Skill | With Skill | Waste | Reduction |
|----------|--------------|------------|-------|-----------|
| Full codebase load | 58,000 | 3,000 | 55,000 | 94% |
| 3 agents parallel | 64,000 | 3,000 | 61,000 | 95% |
| Find functionality | 22,000 | 150 | 21,850 | 99% |
| Onboard new agent | 16,700 | 3,000 | 13,700 | 82% |
| Switch projects | 37,000 | 6,000 | 31,000 | 84% |
| Track changes | 58,000 | 500 | 57,500 | 99% |
| **AVERAGE** | **42,617** | **2,608** | **40,008** | **94%** |

### 3. Structural Gaps
- No project-level documentation (README inadequate)
- No structured "Core Modules" mapping
- No "Key Patterns" distillation
- No "Recent Changes" tracking
- No tech stack summary
- No dependency inventory
- No testing setup overview

### 4. Multi-Agent Coordination Issues
- Cannot share project understanding efficiently
- Each agent rebuilds mental model (redundant work)
- No single source of truth for structure
- Coordination overhead multiplies token waste
- No fast onboarding for new agents joining waves

### 5. Performance Impact
**Without PROJECT_INDEX**:
- Analysis time: 3-5 minutes (reading files)
- Token consumption: 40K-60K average
- Multi-agent overhead: Linear scaling (N agents × ~20K tokens)
- Context switching: Reload entire codebase

**With PROJECT_INDEX (Expected)**:
- Analysis time: 5-15 seconds (read index)
- Token consumption: 3K tokens
- Multi-agent overhead: Constant (all share same 3K index)
- Context switching: Instant (just read index)

**Speedup**: 12-60x faster, 94% token reduction

---

## Expected Outcome

After RED phase testing:
- **6 documented scenarios** with token waste quantified
- **Proven 94% token reduction** opportunity (42K → 2.6K average)
- **4-5 rationalization patterns** agents use to avoid indexing
- **5 structural gaps** that PROJECT_INDEX must fill
- **Clear ROI**: 40K tokens saved per project analysis
- **Baseline for GREEN phase** compliance testing

**Critical Insight**: Token waste is NOT linear - it MULTIPLIES in multi-agent scenarios. 3 agents = 3x waste, making PROJECT_INDEX essential for wave execution efficiency.

---

**Next**: GREEN phase - Create SKILL.md that prevents ALL documented violations and achieves 94% token reduction
