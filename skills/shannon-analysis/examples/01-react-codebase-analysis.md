# Example 1: React Codebase Analysis

## Context
User has React application, unsure about quality and architecture decisions.

## User Request
> "Can you analyze my React app? I want to know if the architecture is solid and what needs improvement."

## Agent Response (WITH shannon-analysis skill)

```
I'll perform a comprehensive analysis of your React application using Shannon's systematic approach.

**Activating shannon-analysis skill...**

---

### Step 1: Analysis Type Detection
- **Detected**: architecture-review + codebase-quality (combined)
- **Keywords**: "analyze", "React", "architecture", "improvement"
- **Target Technology**: React (Frontend framework)
- **Required Sub-Skills**: project-indexing, confidence-check, functional-testing

---

### Step 2: Serena Historical Context
Querying knowledge graph for previous analysis...

**Result**: No previous analysis found (shannon/analysis/react-app)
**Status**: First analysis - applying full rigor

---

### Step 3: Systematic Discovery

**3a. File Inventory (Glob)**
```bash
Glob: **/*.{js,jsx,ts,tsx,json,md}
```

Found 183 files:
- `src/components/`: 67 files
- `src/pages/`: 23 files
- `src/hooks/`: 15 files
- `src/api/`: 31 files
- `src/utils/`: 18 files
- `src/__tests__/`: 22 files
- Config/Build: 7 files

**3b. Pattern Analysis (Grep)**

Dependency patterns:
- `import React`: 145 files (component-based architecture ✓)
- `useState`: 89 occurrences (local state management)
- `useEffect`: 134 occurrences (side effects, possible overuse)
- `fetch|axios`: 45 occurrences (API integration)

Test patterns:
- `jest.fn`: 8 files ❌ (NO MOCKS violation)
- `describe|test|it`: 22 files (12% test coverage)

Technical debt:
- `TODO`: 12 occurrences
- `FIXME`: 3 occurrences
- `console.log`: 67 occurrences (debug statements)

---

### Step 4: Sub-Skill Invocation

**4a. project-indexing** (183 files > 50 threshold)

Generated `SHANNON_INDEX.md`:
- Token reduction: 8,234 tokens → 421 tokens (94.9% reduction)
- Structure: 5 main modules (Components, Pages, Hooks, API, Utils)
- Entry points: App.jsx, index.js, main routing in src/routes.jsx

**4b. confidence-check** (architecture-review mode)

Running 5-check validation...

1. ✅ No duplicate implementations? **90%**
   - Minor: 2 date formatters in different utils files
2. ✅ Architecture compliance? **85%**
   - Follows React component-based patterns mostly
   - Some god components (>500 lines)
3. ⚠️ Official docs verified? **70%**
   - React patterns match docs
   - But custom state management (no Redux/Zustand/etc)
4. ⚠️ Working OSS referenced? **60%**
   - No reference to production React apps
   - Custom patterns without validation
5. N/A Root cause identified? **N/A** (not debugging)

**Overall Confidence: 76%** (CLARIFY threshold)
→ Need user input before recommending major changes

**4c. functional-testing analysis**

Detected: 8 test files using `jest.fn()` (mock functions)

**Violation**: NO MOCKS principle
- Mock tests don't catch integration bugs
- Real browser automation (Puppeteer) needed
- **Severity**: MEDIUM (functional coverage needed)

---

### Step 5: Domain Calculation

File-count-based calculation:

| Domain | Files | Percentage | Evidence |
|--------|-------|-----------|----------|
| Frontend | 133 | 72.7% | components + pages + hooks |
| Backend | 31 | 16.9% | src/api/* (API layer) |
| Testing | 22 | 12.0% | __tests__/* |
| Config | 7 | 3.8% | package.json, tsconfig, etc |

**Dominant Domain**: Frontend (72.7%)
**Diversity Score**: 0.58 (moderately focused)

---

### Step 6: MCP Recommendations

Based on findings:

**Recommended MCPs**:
1. **puppeteer**
   - Reason: 72.7% frontend + 8 mock-based tests need replacement
   - Use: Real browser automation for functional testing
   - Install: Via Claude Code MCP settings

2. **context7**
   - Reason: React framework detected
   - Use: Official pattern validation, best practices
   - Trigger: When implementing new features

---

### Step 7: Structured Analysis Report

---

# React App Architecture Analysis

## Executive Summary
Frontend-focused (72.7%) React application with solid component-based architecture but three key issues: (1) 8 mock-based tests violating NO MOCKS, (2) 134 useEffect hooks suggesting complexity, (3) no global state management despite growing state needs.

## Quantitative Metrics
- **Total Files**: 183
- **Domain Split**: 73% Frontend / 17% Backend / 12% Tests / 4% Config
- **Components**: 67 (good modularity)
- **State Management**: 89 useState, 134 useEffect (high coupling)
- **API Integration**: 45 calls (centralized in src/api)
- **Test Coverage**: 22 files (12% of codebase)

## Architecture Assessment

### ✅ Strengths
1. **Component Structure**: 67 components in organized directories
   - Evidence: `src/components/` well-structured
   - Pattern: Matches React best practices

2. **Custom Hooks**: 15 hooks for reusability
   - Evidence: `src/hooks/` directory
   - Pattern: Good abstraction layer

3. **API Centralization**: 31 API files in dedicated module
   - Evidence: `src/api/*` structure
   - Pattern: Separation of concerns

### ⚠️ Concerns

1. **useEffect Overuse**: 134 instances (7.9 per file avg in pages)
   - Evidence: `grep useEffect` found 134
   - Risk: Dependency tracking complexity, performance issues
   - Recommendation: Consider React Query or SWR for data fetching

2. **No Global State**: Only local useState
   - Evidence: No Redux/Zustand/Jotai imports detected
   - Risk: Prop drilling, state duplication
   - Question for user: Is this by design? Or missing?

3. **God Components**: 3 files >500 lines
   - Evidence: src/pages/Dashboard.jsx (847 lines)
   - Risk: Maintenance burden, hard to test
   - Recommendation: Split into smaller components

### ❌ Violations

**NO MOCKS Violation**: 8 test files with mock functions
- Files: `src/api/__tests__/*.test.js`
- Pattern: Using `jest.fn()` to mock API calls
- Problem: Mock tests don't catch:
  - Network errors
  - CORS issues
  - Response format changes
  - Integration bugs
- **Solution**: Replace with Puppeteer functional tests against real/staging backend

## Technical Debt (Prioritized)

### 🔴 HIGH PRIORITY
1. **Mock-Based Tests** (8 files)
   - Impact: Integration bugs not caught
   - Effort: 3-4 days
   - Action: Migrate to Puppeteer, test against real backend
   - Evidence: `grep 'jest.fn'` found 8 occurrences

### 🟡 MEDIUM PRIORITY
2. **useEffect Complexity** (134 hooks)
   - Impact: Performance, maintainability
   - Effort: 2-3 days
   - Action: Refactor to React Query/SWR for data fetching
   - Evidence: 134 useEffect calls, many for data fetching

3. **Debug Statements** (67 console.log)
   - Impact: Code clutter, minor performance hit
   - Effort: 1 day
   - Action: Remove or replace with proper logging
   - Evidence: `grep 'console.log'` found 67

### 🟢 LOW PRIORITY
4. **TODO Comments** (12 items)
   - Impact: Incomplete features, maintenance notes
   - Effort: Variable
   - Action: Review and resolve each
   - Evidence: `grep TODO` found 12

## Recommendations (Actionable)

### Immediate (This Week)
**1. Replace Mock Tests with Functional Tests**
```bash
# Install Puppeteer MCP
# Then migrate tests:
Before: jest.fn() mocking API responses
After: Puppeteer testing against real staging backend
```

**Effort**: 3-4 days
**ROI**: Catch 80% more integration bugs
**Evidence**: Historical Shannon data on mock vs functional testing

---

### Short-term (Next 2 Weeks)
**2. Introduce Data Fetching Library**

Consider React Query or SWR to reduce useEffect complexity:
```javascript
// Before: Manual useEffect
useEffect(() => {
  fetch('/api/users')
    .then(res => res.json())
    .then(setUsers)
}, [])

// After: React Query
const { data: users } = useQuery('users', fetchUsers)
```

**Effort**: 2-3 days
**Impact**: Simpler code, automatic caching, better UX
**Evidence**: 134 useEffect hooks, many for data fetching

---

### Long-term (Next Month)
**3. Evaluate Global State Management**

**Question for User**: Is lack of global state (Redux/Zustand) intentional?

If not intentional:
- **Recommendation**: Zustand (lightweight) or Jotai (atomic)
- **Effort**: 2-3 days migration
- **Benefit**: Eliminate prop drilling, centralize auth/user state

If intentional:
- Document decision in Serena for future reference
- Monitor prop drilling as app grows

---

## MCP Recommendations

**Install These MCPs**:
1. **puppeteer** (Recommended)
   - Purpose: Replace mock tests with functional browser tests
   - Install: Claude Code MCP settings
   - Usage: Test against real backend, catch integration bugs

2. **context7** (Recommended)
   - Purpose: Validate React patterns against official docs
   - Install: Claude Code MCP settings
   - Usage: During feature implementation

---

## Confidence Assessment

**Overall Confidence: 76%** (CLARIFY threshold)

Before proceeding with recommendations, I need clarification:

1. **State Management**: Is lack of global state intentional or oversight?
2. **Test Priority**: Should mock test replacement be #1 priority?
3. **useEffect Refactor**: Open to introducing React Query/SWR?

Once clarified, I can proceed with HIGH confidence (>90%).

---

## Next Steps

1. **User**: Answer 3 clarification questions above
2. **Shannon**: Based on answers, create wave plan:
   - Wave 1: Test migration (3-4 days)
   - Wave 2: Data fetching refactor (2-3 days)
   - Wave 3: State management (if needed, 2-3 days)
3. **Execute**: With checkpoints between waves

---

**Analysis Complete**
**Duration**: ~2 minutes
**Files Analyzed**: 183 (100% of codebase)
**Method**: Systematic Glob/Grep + Sub-Skills
**Confidence**: 76% (needs clarification)
**Next**: Awaiting user input on 3 questions

---

### Step 8: Persist to Serena
Saving analysis results...

**Entity Created**: `shannon/analysis/react-app-20250104`

**Stored**:
- Analysis type: architecture-review + codebase-quality
- Key metrics: 183 files, 73% frontend, 12% test coverage
- Findings: NO MOCKS violation (8 files), useEffect complexity (134), no global state
- Recommendations: Puppeteer migration, React Query, evaluate Zustand
- Confidence: 76% (clarify state + test priority)

**Relations Created**:
- None (first analysis, no prior context)

**Tags Applied**:
- `analysis-date:2025-01-04`
- `analysis-type:architecture-review`
- `dominant-domain:frontend`
- `confidence:clarify`
- `violations:no-mocks`

Analysis saved for future sessions. ✓

---

**shannon-analysis skill execution complete.**
```

## What Was Different?

**WITHOUT shannon-analysis skill** (from RED baseline):
- Agent would have: "Let me check a few files... Looks good overall!"
- Random sampling, no systematic discovery
- Subjective assessment ("looks solid")
- No historical context check
- Generic advice ("add tests")
- Results vanish after conversation

**WITH shannon-analysis skill**:
- ✅ Complete file inventory (183 files, 100% coverage)
- ✅ Quantitative metrics (73% frontend, 134 useEffect, etc)
- ✅ Serena context check (found it's first analysis)
- ✅ Sub-skill invocation (project-indexing, confidence-check, functional-testing)
- ✅ Evidence-based recommendations (grep results prove claims)
- ✅ Prioritized by impact + effort
- ✅ MCP recommendations (Puppeteer, Context7)
- ✅ Results persisted to Serena for next session
- ✅ Confidence scoring (76% = needs clarification)

## Validation Points

This example demonstrates prevention of:
1. ✅ Rationalization 1: "User request is vague" → Parsed into architecture-review
2. ✅ Rationalization 2: "Quick look sufficient" → Full Glob/Grep discovery
3. ✅ Rationalization 3: "No previous context" → Queried Serena first
4. ✅ Rationalization 4: "Analysis would take too long" → 2 min systematic beats hours rework

All 28 baseline violations prevented. ✓
