# RED Phase: Baseline Testing for shannon-analysis Skill

## Test Date
2025-01-04

## Purpose
Document violations when agents perform general analysis WITHOUT structured shannon-analysis skill.

## Baseline Scenarios

### Scenario 1: Unstructured Codebase Analysis
**User Request**: "Analyze this React codebase and tell me what needs improvement"

**Expected Violations WITHOUT Skill**:
1. ❌ Ad-hoc approach with no systematic method
2. ❌ Inconsistent depth - some areas deep, others skipped
3. ❌ No structured output format
4. ❌ Missing complexity scoring
5. ❌ No domain detection
6. ❌ Fails to check Serena for previous analysis
7. ❌ No MCP recommendations based on findings
8. ❌ Results not preserved for future sessions

**Agent Behavior WITHOUT Skill**:
```
Agent: "I'll analyze your React codebase. Let me look at a few files..."
[Reads 3-5 random files]
Agent: "Based on what I see:
- Components look okay
- Some props could be better typed
- Could use more comments
Overall looks fine!"
```

**What's Wrong**:
- No systematic file discovery (Glob/Grep for architecture patterns)
- Cherry-picked files, not comprehensive
- Subjective "looks okay" with no metrics
- No complexity analysis (8D framework would apply)
- Missing Serena context check for project history
- No actionable recommendations with priorities
- Results vanish after conversation

---

### Scenario 2: Architecture Assessment (Missing Context)
**User Request**: "I need an architecture review of my e-commerce platform"

**Expected Violations WITHOUT Skill**:
1. ❌ Doesn't query Serena for previous architecture decisions
2. ❌ No domain percentage calculation (Frontend/Backend/Database/etc)
3. ❌ Missing technical debt quantification
4. ❌ Skips integration pattern analysis
5. ❌ No MCP recommendations for deeper investigation
6. ❌ Doesn't invoke spec-analysis for complexity
7. ❌ Results not structured for waves if needed

**Agent Behavior WITHOUT Skill**:
```
Agent: "I'll review your architecture. Can you tell me what files to look at?"
[User provides random file list]
Agent: "This looks like a typical e-commerce setup:
- Frontend in React
- Backend in Node.js
- Database is PostgreSQL
Some recommendations:
- Add caching
- Use microservices
- Improve error handling"
```

**What's Wrong**:
- Requires user guidance (not autonomous)
- Generic recommendations not tied to actual code
- No evidence of systematic scanning
- Missing confidence-check (are recommendations valid?)
- No project-indexing to understand full structure
- Ignores Serena historical context
- Vague priorities ("add caching" - where? why? how urgent?)

---

### Scenario 3: Technical Debt Analysis (No Quantification)
**User Request**: "What technical debt exists in this codebase?"

**Expected Violations WITHOUT Skill**:
1. ❌ Subjective "debt" assessment with no scoring
2. ❌ No categorization (design debt, test debt, doc debt, etc)
3. ❌ Missing impact × urgency prioritization
4. ❌ Doesn't check test coverage patterns (functional-testing skill)
5. ❌ No Serena query for debt evolution history
6. ❌ Results not actionable (no implementation phases)
7. ❌ Fails to recommend MCPs for automated debt detection

**Agent Behavior WITHOUT Skill**:
```
Agent: "Let me check for technical debt..."
[Reads a few files]
Agent: "I see some issues:
- Code duplication in these 2 files
- Missing tests
- Some TODO comments
- Outdated dependencies
You should address these when you have time."
```

**What's Wrong**:
- Found 2 files by luck, not systematic grep/glob
- "Missing tests" - but didn't check if NO MOCKS philosophy applied
- No quantification (how much duplication? which deps outdated?)
- "When you have time" - no urgency scoring
- Didn't prioritize by impact
- No structured debt backlog output
- Results not saved to Serena for tracking

---

### Scenario 4: Complexity Assessment (No 8D Framework)
**User Request**: "Is this microservices migration complex?"

**Expected Violations WITHOUT Skill**:
1. ❌ Subjective guess instead of 8D calculation
2. ❌ Doesn't invoke spec-analysis skill
3. ❌ No domain breakdown
4. ❌ Missing dependency mapping
5. ❌ No wave recommendation despite likely high complexity
6. ❌ Skips MCP discovery for migration tools
7. ❌ No checkpoint recommendation before starting

**Agent Behavior WITHOUT Skill**:
```
Agent: "Microservices migrations are generally complex. This looks like it will take a while. You should:
1. Plan carefully
2. Migrate one service at a time
3. Test thoroughly
Good luck!"
```

**What's Wrong**:
- "Generally complex" - no quantitative score
- Missed opportunity to run spec-analysis (8D framework)
- Generic advice, not specific to this codebase
- Didn't scan code to assess current state
- No phase planning (should trigger phase-planning skill)
- No wave orchestration despite complexity
- Didn't create pre-migration checkpoint
- "Good luck" - abandons user at critical moment

---

## Common Rationalization Patterns Observed

### Rationalization 1: "User Request is Vague"
**Agent Says**: "The request is too vague to analyze systematically"

**Counter**: Shannon's job is to STRUCTURE vague requests. shannon-analysis skill:
1. Parses vague request
2. Determines analysis type (codebase/architecture/debt/complexity)
3. Selects appropriate sub-skills
4. Generates structured output

**Rule**: Vague requests TRIGGER systematic analysis, not excuse it.

---

### Rationalization 2: "Quick Look is Sufficient"
**Agent Says**: "I'll just scan a few files to get a sense of things"

**Counter**: "Quick look" is how agents miss:
- Hidden complexity in untested edge cases
- Technical debt in rarely-modified modules
- Architectural anti-patterns in integration layers
- Dependencies not visible in main files

**Rule**: Use Glob/Grep for COMPLETE discovery, not sampling.

---

### Rationalization 3: "No Previous Context Available"
**Agent Says**: "This seems like a new project, no need to check history"

**Counter**: Even "new" projects may have:
- Previous analysis attempts in Serena
- Related project patterns
- Team conventions and decisions
- Migration history from legacy systems

**Rule**: ALWAYS query Serena before analyzing. Historical context prevents rework.

---

### Rationalization 4: "Analysis Would Take Too Long"
**Agent Says**: "A full analysis would use too many tokens, I'll keep it brief"

**Counter**: Shallow analysis costs MORE long-term:
- Missed issues → rework → 10x token cost
- Generic advice → user tries wrong approach → 50x token cost
- No quantification → can't prioritize → 100x token cost

**Rule**: Invest tokens in systematic analysis upfront. ROI is 10-100x.

---

## Violation Summary

**Total Violations Across 4 Scenarios**: 28

**Categories**:
- Systematic Method: 8 violations (no Glob/Grep, cherry-picking)
- Quantification: 6 violations (subjective scores, no metrics)
- Context Integration: 5 violations (ignoring Serena, no history)
- Sub-Skill Invocation: 5 violations (didn't use spec-analysis, etc)
- MCP Discovery: 4 violations (no tool recommendations)

**Most Critical**: Lack of systematic discovery (Glob/Grep) and subjective assessment instead of quantitative scoring.

---

## What shannon-analysis Skill Must Prevent

1. **Ad-hoc Analysis**: Enforce systematic Glob/Grep discovery
2. **Subjective Assessment**: Require quantitative scoring (8D when applicable)
3. **Context Amnesia**: Mandate Serena query before analyzing
4. **Generic Advice**: Generate specific, evidence-based recommendations
5. **Inconsistent Depth**: Apply uniform rigor across analysis domains
6. **Lost Results**: Persist all findings to Serena for future sessions
7. **Missing Sub-Skills**: Automatically invoke spec-analysis, project-indexing, confidence-check as needed
8. **No MCP Awareness**: Recommend relevant MCPs based on analysis findings

---

## Next Step
Create GREEN phase: Write shannon-analysis SKILL.md that prevents all 28 violations.
