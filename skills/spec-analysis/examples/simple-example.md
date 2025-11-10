# spec-analysis Example: Simple Todo App

**Complexity Band:** SIMPLE (0.28-0.35)
**Expected Outcome:** Sequential execution, 1-2 agents, 4-6 hours
**Purpose:** Demonstrates spec-analysis workflow for straightforward single-domain project

---

## Input Specification

```
Build a simple todo app with React. Users can:
- Add new tasks with title and description
- Mark tasks as complete
- Delete tasks
- Filter by complete/incomplete

Store data in localStorage. Responsive design for mobile.
```

---

## Step-by-Step Analysis

### Step 1: Activation Detection
**Triggers Met:**
- ✅ 5 distinct feature items (bullet list)
- ✅ Primary keyword: "Build"
- ✅ Secondary keywords: "Users can" (repeated)
- ✅ >50 words

**Decision:** Activate spec-analysis mode

---

### Step 2: 8-Dimensional Scoring

#### Structural Complexity (Weight: 20%)
**Keywords Found:** "1 file" (implied single-page app)
**Calculation:**
- File count: 1 (React app)
- File factor: `log10(1 + 1) / 3 = 0.10`
- Service count: 0 (no backend)
- Module complexity: Low (single component)

**Score:** 0.10

#### Cognitive Complexity (Weight: 15%)
**Keywords Found:** "design" (responsive design)
**Calculation:**
- Analysis verbs: 0
- Design verbs: 1 ("design") → +0.20
- Decision verbs: 0
- Abstract concepts: 0

**Score:** 0.20

#### Coordination Complexity (Weight: 15%)
**Keywords Found:** None (solo project implied)
**Calculation:**
- Team count: 0
- Integration keywords: 0
- Stakeholders: 0

**Score:** 0.10 (minimum baseline)

#### Temporal Complexity (Weight: 10%)
**Keywords Found:** None (no deadline)
**Calculation:**
- Urgency: None → +0.00
- Deadline: None → +0.00

**Score:** 0.10 (minimum baseline)

#### Technical Complexity (Weight: 15%)
**Keywords Found:** "React", "localStorage", "responsive"
**Calculation:**
- Advanced tech: 0 (React is standard)
- Complex algorithms: 0
- Integrations: 0 (localStorage is built-in)
- Responsive design: Standard practice → +0.10

**Score:** 0.20

#### Scale Complexity (Weight: 10%)
**Keywords Found:** "localStorage" (implies small scale)
**Calculation:**
- Users: Not mentioned → assume personal use (<100 users) → +0.05
- Data: localStorage (KB-scale) → +0.05
- Performance: Not mentioned → +0.00

**Score:** 0.10

#### Uncertainty Complexity (Weight: 10%)
**Keywords Found:** None (requirements are clear)
**Calculation:**
- Ambiguity keywords: 0
- Exploratory terms: 0
- Research needs: 0

**Score:** 0.10 (minimum baseline)

#### Dependencies Complexity (Weight: 5%)
**Keywords Found:** None (no blocking dependencies)
**Calculation:**
- Blocking language: 0
- External dependencies: 0

**Score:** 0.10 (minimum baseline)

---

### Weighted Total Calculation

```
total = (0.20 × 0.10) + (0.15 × 0.20) + (0.15 × 0.10) +
        (0.10 × 0.10) + (0.15 × 0.20) + (0.10 × 0.10) +
        (0.10 × 0.10) + (0.05 × 0.10)

     = 0.02 + 0.03 + 0.015 + 0.01 + 0.03 + 0.01 + 0.01 + 0.005
     = 0.13
```

**Apply minimum floor (0.10):** Final score = **0.13**

**Interpretation Band:** SIMPLE (0.00-0.30)

---

### Step 3: Domain Detection

#### Keyword Counting
- **Frontend:** React (1), design (1), responsive (1), mobile (1) = **4 keywords**
- **Backend:** 0
- **Database:** localStorage (1) = **1 keyword** (counts as Database/Storage)
- **Mobile:** mobile (1) = **1 keyword** (overlaps with Frontend)
- **DevOps:** 0
- **Security:** 0

**Total unique domain keywords:** 5 (React, design, responsive, mobile, localStorage)

#### Raw Percentages
```
Frontend: (4 / 5) × 100 = 80%
Database: (1 / 5) × 100 = 20%
```

#### Normalization
Sum = 80% + 20% = 100% ✅ (already normalized)

**Final Domain Distribution:**
- Frontend: **80%**
- Database: **20%**

---

### Step 4: MCP Recommendations

#### Tier 1: MANDATORY
1. **Serena MCP** - Context preservation (required for all Shannon workflows)

#### Tier 2: PRIMARY (>=20% domain threshold)
2. **Magic MCP** - Frontend 80% (React component generation)
   - Purpose: Generate React components with /ui command
   - Usage: When building UI components (buttons, forms, todo items)
   - Fallback: Manual component creation

3. **Puppeteer MCP** - Frontend testing (functional tests, NO MOCKS)
   - Purpose: Real browser testing for user interactions
   - Usage: Test "add task", "mark complete", "delete" flows
   - Fallback: Manual testing

#### Tier 3: SECONDARY
4. **GitHub MCP** - Version control and deployment
   - Purpose: Commit management, GitHub Actions for deployment
   - Usage: Push code, create repo, deploy to GitHub Pages
   - Fallback: Manual git operations

**Total MCPs:** 4 (appropriate for SIMPLE project)

---

### Step 5: 5-Phase Plan Generation

**Timeline Estimate:** 4-6 hours (SIMPLE band)

#### Phase 1: Analysis & Planning (15% = 36 minutes)
**Objectives:**
- Complete spec analysis (already done)
- Create task breakdown (5 tasks identified)
- Risk assessment (minimal risks: localStorage browser compatibility)

**Deliverables:**
- ✅ Spec analysis complete (this document)
- Task list: [Setup React, Create TodoList component, Add localStorage, Style responsive, Write Puppeteer tests]
- Risk doc: localStorage browser support (mitigation: add fallback message)

**Validation Gate:** All requirements clear, no ambiguities, MCPs configured

**Duration:** 36 minutes

---

#### Phase 2: Architecture & Design (20% = 48 minutes)
**Objectives:**
- Component hierarchy design (TodoApp → TodoList → TodoItem)
- State management strategy (useState for simple state)
- Data model (Task: {id, title, description, completed})
- Responsive layout (mobile-first CSS)

**Deliverables:**
- Component tree diagram
- State flow diagram
- Task data model
- Mobile/desktop layout wireframes

**Validation Gate:** Component structure approved, data model validated

**Duration:** 48 minutes

---

#### Phase 3: Implementation (40% = 2.4 hours)
**Objectives:**
- Create React app structure
- Implement TodoList component with add/delete/complete
- Implement TodoFilter component (show all/active/completed)
- Add localStorage persistence (save on change, load on mount)
- Responsive CSS (mobile-first, flexbox)

**Deliverables:**
- Working React app
- localStorage integration functional
- Responsive design implemented
- All 5 features complete

**Validation Gate:** All features working per spec, manual testing passed

**Duration:** 2 hours 24 minutes

---

#### Phase 4: Integration & Testing (15% = 36 minutes)
**Objectives:**
- Puppeteer functional tests (NO MOCKS)
  - Test: Add new task → verify appears in list
  - Test: Mark task complete → verify checkbox + strikethrough
  - Test: Delete task → verify removed from list
  - Test: Filter tasks → verify correct tasks shown
  - Test: Reload page → verify localStorage persistence

**Deliverables:**
- 5 Puppeteer test scenarios passing
- Real browser testing (Chrome/Firefox)
- All user flows validated

**Validation Gate:** All Puppeteer tests passing, localStorage persistence verified

**Duration:** 36 minutes

---

#### Phase 5: Deployment & Documentation (10% = 24 minutes)
**Objectives:**
- Deploy to GitHub Pages (or Vercel/Netlify)
- Create README.md (installation, usage, features)
- Document localStorage behavior (browser requirements)

**Deliverables:**
- Live URL (deployed app)
- README.md complete
- Browser compatibility notes

**Validation Gate:** App deployed and accessible, docs complete

**Duration:** 24 minutes

---

### Step 6: Save to Serena MCP

**Analysis ID:** `spec_analysis_todo_app_20250103_143022`

**Saved Data:**
```json
{
  "analysis_id": "spec_analysis_todo_app_20250103_143022",
  "complexity_score": 0.13,
  "interpretation": "SIMPLE",
  "dimension_scores": {
    "structural": 0.10,
    "cognitive": 0.20,
    "coordination": 0.10,
    "temporal": 0.10,
    "technical": 0.20,
    "scale": 0.10,
    "uncertainty": 0.10,
    "dependencies": 0.10
  },
  "domain_percentages": {
    "frontend": 80,
    "database": 20
  },
  "mcp_recommendations": [
    {"name": "Serena MCP", "tier": 1},
    {"name": "Magic MCP", "tier": 2},
    {"name": "Puppeteer MCP", "tier": 2},
    {"name": "GitHub MCP", "tier": 3}
  ],
  "phase_plan": {
    "phase_1": "Analysis & Planning (36 min)",
    "phase_2": "Architecture & Design (48 min)",
    "phase_3": "Implementation (2.4 hrs)",
    "phase_4": "Integration & Testing (36 min)",
    "phase_5": "Deployment & Documentation (24 min)"
  },
  "execution_strategy": "sequential",
  "timeline": "4-6 hours"
}
```

**Verification:** `read_memory("spec_analysis_todo_app_20250103_143022")` → ✅ Success

---

## Output Report

```markdown
# Specification Analysis ✅

**Complexity**: 0.13 / 1.0 (SIMPLE)
**Execution Strategy**: Sequential (no waves needed)
**Timeline**: 4-6 hours
**Analysis ID**: spec_analysis_todo_app_20250103_143022

## Domain Breakdown
- Frontend (80%): React UI, component-based architecture, responsive design
- Database (20%): localStorage persistence

## Recommended MCPs (4 total)
1. **Serena MCP** (Tier 1 - MANDATORY) - Context preservation
2. **Magic MCP** (Tier 2 - PRIMARY) - React component generation (Frontend 80%)
3. **Puppeteer MCP** (Tier 2 - PRIMARY) - Functional testing (NO MOCKS)
4. **GitHub MCP** (Tier 3 - SECONDARY) - Version control

## 5-Phase Plan (4-6 hours)
- **Phase 1:** Analysis & Planning (36 min)
- **Phase 2:** Architecture & Design (48 min)
- **Phase 3:** Implementation (2.4 hrs) ← Largest phase
- **Phase 4:** Integration & Testing (36 min) - Puppeteer tests
- **Phase 5:** Deployment & Documentation (24 min)

## Next Steps
1. ✅ Complexity confirmed: SIMPLE (sequential execution appropriate)
2. Configure MCPs: Install Magic, Puppeteer, ensure Serena connected
3. Begin Phase 1: Already complete (this analysis)
4. Proceed to Phase 2: Design component hierarchy
```

---

## Anti-Rationalization Applied

### Temptation 1: "This is simple, skip analysis"
**Resisted:** ✅ Ran full algorithm despite "simple" label
**Result:** Score of 0.13 confirms SIMPLE, but analysis revealed:
- 5 distinct features to track
- localStorage complexity (browser compatibility)
- Responsive design requirements
- Testing strategy needed (Puppeteer)

**Value:** 30-second analysis prevented missed requirements

### Temptation 2: "Obviously 100% frontend, skip domain counting"
**Resisted:** ✅ Counted keywords objectively
**Result:** Discovered 20% Database domain (localStorage)
**Impact:** Remembered to test persistence behavior, handle localStorage errors

### Validation
- Complexity score: 0.13 (valid, in [0.10, 0.95] range) ✅
- Domain percentages: 80% + 20% = 100% ✅
- Serena MCP in Tier 1 ✅
- Domain-specific MCPs: Magic (Frontend 80%) ✅
- 5 phases with validation gates ✅
- Testing enforces NO MOCKS (Puppeteer) ✅

**Quality Score:** 1.0 (all checks passed)

---

## Key Takeaways

1. **"Simple" Still Gets Analyzed:** Even 0.13 complexity benefits from systematic analysis
2. **Objective Scoring Works:** Algorithm revealed 20% Database domain not obvious from casual reading
3. **Phase Planning Valuable:** 5-phase structure with timelines guides execution
4. **MCP Right-sizing:** 4 MCPs appropriate (not overwhelming for SIMPLE project)
5. **Testing Philosophy:** Puppeteer for functional tests enforces NO MOCKS even for simple apps
