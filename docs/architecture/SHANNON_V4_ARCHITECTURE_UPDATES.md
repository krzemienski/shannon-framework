# Shannon Framework v4 - Architecture Updates from Phase 1 Research

**Version**: 2.0
**Date**: 2025-11-04
**Status**: APPROVED - Phase 2 Wave 1 Complete
**Base Document**: `docs/plans/2025-11-03-shannon-v4-architecture-design.md`
**Research Basis**: Phase 1 - 8 parallel research agents (92% confidence)

---

## Executive Summary

This document updates Shannon Framework v4 architecture based on Phase 1 research findings. All critical design questions answered, architecture validated at 92% confidence, and approved for implementation.

**10 Critical Architectural Changes**:
1. ✅ Adopt Executable Skills Pattern (SuperClaude) - 25-250x ROI
2. ✅ Implement Progressive Disclosure (Claude Code best practice)
3. ✅ Add Auto-Activation Capability (Superpowers pattern)
4. ✅ Implement Confidence Gating (SuperClaude, ≥90% threshold)
5. ✅ Add SHANNON_INDEX Pattern (94% token reduction)
6. ✅ Deprecate 24 sc_* Commands (establish standalone identity)
7. ✅ Refine MCP Integration Patterns (85% coverage validated)
8. ✅ Enhance SITREP Protocol (standardized communication)
9. ✅ Formalize Validation Gates (NO MOCKS enforcement)
10. ✅ Formalize Skill Composition (REQUIRED SUB-SKILL pattern)

**Architecture Status**: VALIDATED and READY for Phase 3 implementation.

---

## Change 1: Executable Skills Pattern

**Source**: Agent #6 (SuperClaude Analysis)

**Rationale**: SuperClaude's dual implementation (SKILL.md + executable code) achieved:
- 100% precision/recall for confidence-check skill
- 25-250x ROI (100-200 tokens cost, 5K-50K tokens saved)
- Structured data outputs enable testing and automation

**Implementation**:

```
Skills Structure (Dual Implementation):

shannon-plugin/skills/[skill-name]/
├── SKILL.md                    # Behavioral instructions for Claude (markdown)
├── [skill-name].ts             # Executable TypeScript logic (optional)
├── [skill-name].py             # OR Python logic (optional)
├── [skill-name].test.ts        # Jest/Pytest tests
└── references/
    └── [DETAILED_DOCS].md      # Progressive disclosure content

Priority Skills for Executable Implementation (6 skills):
1. spec-analysis → TypeScript (8D calculations, complex math)
2. wave-orchestration → Python (orchestration logic, async)
3. confidence-check → TypeScript (following SuperClaude pattern exactly)
4. functional-testing → Python (test generation, Puppeteer integration)
5. project-indexing → Python (file processing, compression)
6. mcp-discovery → Python (capability mapping, optional)

Remaining 7 skills: Markdown-only (behavioral instructions sufficient)
```

**Executable Skill Invocation Pattern**:
```typescript
// spec-analysis.ts (TypeScript executable)
export interface SpecAnalysisInput {
  specification: string;
  project_context?: object;
}

export interface SpecAnalysisOutput {
  complexity_scores: {
    structural: number;
    cognitive: number;
    coordination: number;
    temporal: number;
    technical: number;
    scale: number;
    uncertainty: number;
    dependencies: number;
    overall: number;
  };
  domains: {
    frontend: number;
    backend: number;
    mobile: number;
    data: number;
    devops: number;
    security: number;
  };
  recommended_mcps: string[];
  confidence: number;
}

export async function analyzeSpecification(
  input: SpecAnalysisInput
): Promise<SpecAnalysisOutput> {
  // 8D complexity calculation logic
  // Domain classification algorithm
  // MCP recommendations
  return {
    complexity_scores: { /* ... */ },
    domains: { /* ... */ },
    recommended_mcps: ["serena", "sequential", "context7"],
    confidence: 0.92
  };
}
```

**SKILL.md Integration**:
```markdown
## Step 2: 8-Dimensional Complexity Analysis

Execute the 8D analysis algorithm:

@execute spec-analysis.ts analyzeSpecification
Input: {
  "specification": "[user specification text]",
  "project_context": "[optional context]"
}

The executable returns structured JSON with:
- complexity_scores (8 dimensions + overall)
- domains (percentages for 6 categories)
- recommended_mcps (list)
- confidence (0.0-1.0)

Use this structured data in the following steps...
```

**Benefits**:
- Reusable logic across skills
- Testable with Jest/Pytest (unit tests for executables, functional tests for workflows)
- Structured data outputs (JSON)
- Performance optimization possible
- Type safety (TypeScript)

**Status**: Design complete, ready for implementation in Phase 3 Wave 3.

---

## Change 2: Progressive Disclosure

**Source**: Agent #1 (Claude Code Skills SDK)

**Rationale**: Claude Code loads skills in 3 levels to minimize token usage:
- Level 1: name + description (~50 tokens) - ALWAYS loaded
- Level 2: SKILL.md body (~500 lines max) - Loaded on invocation
- Level 3: references/* - Loaded on-demand when mentioned

**Implementation**:

```yaml
Skill Frontmatter (Level 1 - Always Loaded):
---
name: spec-analysis
description: |
  Analyzes specifications using 8-dimensional complexity framework.

  Use when:
  - New project specifications provided
  - Requirement changes need impact assessment
  - Complexity estimation needed for planning
  - Domain identification required for tech stack selection

  Outputs: 8D complexity scores, domain percentages, MCP recommendations,
  5-phase plan structure.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"
auto_activate: true
activation_triggers:
  complexity: ">= 0.60"
  keywords: [spec, specification, requirements, PRD, user stories]
required-sub-skills:
  - mcp-discovery
  - phase-planning
mcp-dependencies:
  required:
    - serena
  recommended:
    - sequential
    - context7
allowed-tools:
  - Read
  - Grep
  - Serena
  - Sequential
  - Context7
---
```

```markdown
SKILL.md Body (Level 2 - Loaded on Invocation):

# Specification Analysis Skill

Target: 300-500 lines (hard limit: 600 lines)

## Overview
[Brief overview of skill purpose and capabilities - 2-3 paragraphs]

## Workflow (High-Level)
1. Parse Specification (extract requirements, constraints)
2. Calculate 8D Complexity (invoke spec-analysis.ts)
3. Discover MCPs (invoke mcp-discovery sub-skill) **REQUIRED SUB-SKILL**
4. Quantify Domains (classify and percentage)
5. Generate Phase Plan (invoke phase-planning sub-skill) **REQUIRED SUB-SKILL**
6. Create SITREP (comprehensive analysis report)

## Step Details

### Step 1: Parse Specification
[Concise instructions - 5-10 lines]
See: references/PARSING_ALGORITHM.md for detailed parsing rules

### Step 2: Calculate 8D Complexity
@execute spec-analysis.ts analyzeSpecification
[Concise invocation instructions - 5-10 lines]
See: references/8D_ALGORITHM.md for detailed scoring methodology

### Step 3: Discover MCPs **REQUIRED SUB-SKILL**
@skill mcp-discovery --domains=[from Step 2] --complexity=[overall score]
[Expected input/output - 5-10 lines]
See: references/MCP_INTEGRATION.md for integration patterns

[... remaining steps similarly concise]

## Success Criteria
- Confidence >= 90% (run confidence-check if needed)
- All 8 dimensions scored (0.0-1.0 range)
- Domains sum to 100%
- MCP recommendations include at least Serena (mandatory)
- Phase plan generated with 5 phases

## Error Handling
[Concise error scenarios - 10-15 lines]
See: references/ERROR_RECOVERY.md for detailed recovery procedures

## Examples
[1-2 brief examples]
See: references/EXAMPLES.md for comprehensive example library
```

```markdown
references/ Directory (Level 3 - Loaded On-Demand):

references/8D_ALGORITHM.md (DETAILED - no line limit)
- Complete mathematical formulas for each dimension
- Scoring rubrics and benchmarks
- Historical data and calibration
- Edge case handling
- Performance optimization notes

references/PARSING_ALGORITHM.md
- Detailed parsing rules for different input formats
- Regex patterns and extraction logic
- Conflict resolution strategies
- Validation rules

references/MCP_INTEGRATION.md
- Complete MCP discovery algorithm
- Domain-to-MCP mapping tables
- Complexity-to-MCP thresholds
- Installation instructions for each MCP

references/ERROR_RECOVERY.md
- All error scenarios with recovery procedures
- Troubleshooting flowcharts
- Common pitfalls and solutions

references/EXAMPLES.md
- 10+ comprehensive specification analysis examples
- Small, medium, large, complex specifications
- Edge cases and challenging scenarios
- Expected outputs for each example
```

**Size Guidelines (Enforced)**:
```
Frontmatter (Level 1):
  - Target: ~50 tokens
  - Maximum: 100 tokens
  - Validation: Automated check warns if >100 tokens

SKILL.md Body (Level 2):
  - Target: 300-500 lines
  - Maximum: 600 lines (HARD LIMIT)
  - Validation: Build fails if >600 lines
  - Content: High-level workflow, concise step instructions
  - References: Use "See: references/..." for details

references/* (Level 3):
  - No line limits
  - Loaded only when Claude mentions the file
  - Can be extensive, detailed, comprehensive
```

**Token Efficiency**:
```
Traditional approach (all in SKILL.md):
  - Skill definition: ~8,000 tokens
  - 13 skills loaded: 104,000 tokens upfront
  - Context window pressure: HIGH

Progressive disclosure (Shannon v4):
  - Level 1 (13 skills): 13 × 50 = 650 tokens upfront
  - Level 2 (on invocation): ~2,000 tokens per skill
  - Level 3 (on-demand): Loaded only if mentioned
  - Context window pressure: LOW
  - Savings: ~100,000 tokens (96% reduction in upfront cost)
```

**Status**: Design complete, template created, ready for all 13 skills in Phase 3 Wave 3.

---

## Change 3: Auto-Activation Capability

**Source**: Agent #5 (Superpowers Framework Analysis)

**Rationale**:
- Reduces user cognitive load (no need to remember which skill to use)
- Ensures consistent methodology ("if pattern exists for task, must use it")
- Proven pattern in Superpowers with excellent user experience

**Implementation**:

```python
# src/skill-registry/auto_activator.py

class AutoActivator:
    """Evaluates user input and auto-activates matching skills."""

    def evaluate(self, user_input: str, context: dict) -> List[SkillMatch]:
        """
        Analyzes user input and returns matching skills to auto-activate.

        Args:
            user_input: User's message/command
            context: Current session context (complexity, domains, etc.)

        Returns:
            List of SkillMatch objects sorted by activation_priority
        """
        matches = []

        for skill in self.skill_registry.all_skills():
            if not skill.auto_activate:
                continue

            score = self._calculate_activation_score(skill, user_input, context)

            if score >= skill.activation_threshold:
                matches.append(SkillMatch(
                    skill=skill,
                    score=score,
                    trigger_reason=self._explain_activation(skill, user_input, context)
                ))

        return sorted(matches, key=lambda m: (m.skill.activation_priority, m.score), reverse=True)

    def _calculate_activation_score(self, skill, user_input, context) -> float:
        """Calculate 0.0-1.0 activation score for skill."""
        score = 0.0

        # Keyword matching (30% weight)
        if skill.activation_triggers.get('keywords'):
            keyword_score = self._keyword_match(
                user_input,
                skill.activation_triggers['keywords']
            )
            score += keyword_score * 0.3

        # Complexity threshold (30% weight)
        if skill.activation_triggers.get('complexity'):
            complexity_score = self._complexity_match(
                context.get('complexity', 0.0),
                skill.activation_triggers['complexity']
            )
            score += complexity_score * 0.3

        # Condition evaluation (40% weight)
        if skill.activation_triggers.get('conditions'):
            condition_score = self._condition_match(
                user_input,
                context,
                skill.activation_triggers['conditions']
            )
            score += condition_score * 0.4

        return min(score, 1.0)
```

**Auto-Activation Examples**:

```yaml
# Example 1: spec-analysis skill
---
name: spec-analysis
auto_activate: true
activation_priority: high
activation_threshold: 0.6  # 60% match required
activation_triggers:
  keywords:
    - spec
    - specification
    - requirements
    - PRD
    - "user stories"
    - requirements document
  complexity: ">= 0.60"
  conditions:
    - multi_paragraph_spec  # Input has 3+ paragraphs
    - requirements_list     # Contains numbered/bulleted list
    - project_description   # Describes a project to build
---

User Input: "Build a task management app with React frontend, Node.js backend..."
→ Triggers:
  - Keywords: "Build" (project_description), "React", "Node.js"
  - Conditions: multi_paragraph_spec (TRUE)
  - Score: 0.85
→ Auto-activates spec-analysis skill

# Example 2: functional-testing skill
---
name: functional-testing
auto_activate: true
activation_priority: high
activation_threshold: 0.7
activation_triggers:
  keywords:
    - test
    - testing
    - "doesn't work"
    - bug
    - broken
    - failing
  conditions:
    - testing_phase    # Current phase is "Testing"
    - bug_report       # User describes unexpected behavior
    - pre_deployment   # About to deploy
---

User Input: "The login form doesn't work, users can't sign in"
→ Triggers:
  - Keywords: "doesn't work" (0.8 match)
  - Conditions: bug_report (TRUE)
  - Score: 0.82
→ Auto-activates functional-testing skill

# Example 3: context-preservation skill (Hook-triggered)
---
name: context-preservation
auto_activate: true
activation_priority: critical
activation_threshold: 1.0  # Always activate when triggered
activation_triggers:
  hooks:
    - PreCompact  # Claude Code about to auto-compact
---

Event: PreCompact hook fires
→ Triggers:
  - Hook: PreCompact (TRUE)
  - Score: 1.0 (always activate)
→ Auto-activates context-preservation skill
```

**Mandatory Workflow Enforcement**:

```
If skill exists for task type → Skill MUST be used (not optional)

Implementation:
  1. Auto-activator detects matching skill
  2. System message prepended to user input:
     "spec-analysis skill is available and recommended for this task.
      Using spec-analysis to ensure systematic analysis..."
  3. Skill activates automatically
  4. User sees skill in action (transparent)

Override (if user wants different approach):
  User: "Analyze this spec but skip the 8D framework"
  System: Detects override request, disables auto-activation
  Skill: Does NOT activate (user requested different approach)
```

**User Experience**:

```
# Scenario 1: New specification (auto-activation)
User: /sh_spec "Build an e-commerce platform with React, Node.js, PostgreSQL..."

System:
  [Auto-activating: spec-analysis]

  Analyzing specification using 8-dimensional complexity framework...

  8D Complexity Analysis:
  - Structural: 0.75 (multiple services, database, frontend/backend split)
  - Cognitive: 0.68 (e-commerce domain complexity, payment processing)
  ...

  [Auto-activating: mcp-discovery]

  Recommended MCPs:
  - serena (MANDATORY - context preservation)
  - shadcn-ui (MANDATORY - React UI components)
  - puppeteer (CRITICAL - browser testing for NO MOCKS)
  ...

# Scenario 2: Bug report (auto-activation)
User: "The user dashboard isn't loading, seeing blank screen"

System:
  [Auto-activating: functional-testing]

  Analyzing reported issue: Dashboard blank screen

  Running functional tests:
  1. Browser Test: Loading http://localhost:3000/dashboard
     → Result: 500 Internal Server Error
  2. Network Analysis: Checking API calls
     → Result: /api/dashboard failing (authentication error)

  Root Cause: Authentication token expired in session
  Recommendation: Implement token refresh logic

  Generating fix with code examples...
```

**Status**: Design complete, implementation ready for Phase 3 Wave 1 (Skill Registry).

---

## Change 4: Confidence Gating

**Source**: Agent #6 (SuperClaude Framework Analysis)

**Rationale**:
- Prevents wrong-direction work (saves 5K-50K tokens per avoided mistake)
- SuperClaude's confidence-check achieved 100% precision/recall
- ≥90% threshold balances thoroughness with productivity

**Implementation**:

```yaml
Three-Level Confidence Gating System:

Level 1: Specification Confidence
  When: Before spec-analysis skill begins work
  Command: /sh_spec [specification]
  Process:
    1. Parse specification text
    2. Run confidence-check skill
    3. Evaluate: "Do we understand what needs to be built?" (target: ≥90%)
    4. If <90%: BLOCK, request clarification (show gaps + questions)
    5. If ≥90%: Proceed to spec-analysis

Level 2: Phase Confidence
  When: Before starting each of 5 phases
  Command: /sh_phase [phase_number] (or auto during wave orchestration)
  Process:
    1. Load phase plan and prerequisites
    2. Run confidence-check skill
    3. Evaluate: "Do we have context/decisions needed for this phase?" (≥90%)
    4. If <90%: BLOCK, gather more information (show gaps)
    5. If ≥90%: Proceed to phase execution

Level 3: Wave Confidence
  When: Before wave-orchestration executes each wave
  Internal: Automatic check before dispatching agents
  Process:
    1. Analyze wave dependencies and prerequisites
    2. Run confidence-check skill
    3. Evaluate: "Are all prerequisites complete?" (≥90%)
    4. If <90%: WARN user, offer to continue with risks OR gather context
    5. If ≥90%: Execute wave
```

**confidence-check Skill (Executable)**:

```typescript
// shannon-plugin/skills/confidence-check/confidence-check.ts
// Following SuperClaude pattern exactly

export interface ConfidenceCheckInput {
  context_type: 'specification' | 'phase' | 'wave' | 'general';
  context_data: object;
  threshold?: number;  // Default: 0.90
}

export interface ConfidenceCheckOutput {
  confidence: number;  // 0.0 - 1.0
  threshold: number;
  passed: boolean;
  gaps: string[];      // What's missing or unclear
  questions: string[]; // Clarifying questions to ask
  strengths: string[]; // What we DO understand well
  recommendation: 'PROCEED' | 'BLOCK' | 'WARN';
  reasoning: string;   // Explanation of confidence score
}

export async function checkConfidence(
  input: ConfidenceCheckInput
): Promise<ConfidenceCheckOutput> {
  const threshold = input.threshold || 0.90;

  // Analyze context completeness
  const analysis = await analyzeContext(input);

  // Calculate confidence score (0.0 - 1.0)
  const confidence = calculateConfidenceScore(analysis);

  // Identify gaps and formulate questions
  const gaps = identifyGaps(analysis);
  const questions = generateQuestions(gaps);
  const strengths = identifyStrengths(analysis);

  // Determine recommendation
  let recommendation: 'PROCEED' | 'BLOCK' | 'WARN';
  if (confidence >= threshold) {
    recommendation = 'PROCEED';
  } else if (confidence >= threshold - 0.10) {  // Within 10% of threshold
    recommendation = 'WARN';
  } else {
    recommendation = 'BLOCK';
  }

  return {
    confidence: Math.round(confidence * 100) / 100,  // Round to 2 decimals
    threshold,
    passed: confidence >= threshold,
    gaps,
    questions,
    strengths,
    recommendation,
    reasoning: generateReasoning(analysis, confidence, threshold)
  };
}

// Example output:
{
  "confidence": 0.75,
  "threshold": 0.90,
  "passed": false,
  "gaps": [
    "Authentication mechanism not specified (OAuth vs JWT unclear)",
    "Database schema undefined (table structure unknown)",
    "API versioning strategy not mentioned",
    "Error handling approach not described"
  ],
  "questions": [
    "What authentication method should we use: OAuth 2.0, JWT, or session-based?",
    "Can you provide the database schema or list the main entities?",
    "Do we need API versioning (e.g., /v1/, /v2/)? If so, what strategy?",
    "How should the API handle errors? RESTful error codes? Custom error format?"
  ],
  "strengths": [
    "Tech stack clearly defined (React, Node.js, PostgreSQL)",
    "Core features well described (user management, product catalog, cart, checkout)",
    "UI requirements specified (responsive, accessible)",
    "Performance targets mentioned (2s page load)"
  ],
  "recommendation": "BLOCK",
  "reasoning": "Confidence is 75%, below the 90% threshold. While the tech stack and core features are clear (strengths), critical implementation details are missing (authentication, database schema, API design). Gathering this information now will prevent rework later and save significant development time. Estimated token savings: 10K-30K by clarifying upfront."
}
```

**User Experience**:

```
# Example 1: Low Confidence (Blocked)
User: /sh_spec "Build a web app for managing tasks"

System:
  Running confidence check on specification...

  ⚠️ CONFIDENCE CHECK FAILED

  Confidence: 62% (below 90% threshold)
  Recommendation: BLOCK - Gather more information before proceeding

  What we understand well:
  ✓ Purpose: Task management application
  ✓ Platform: Web application

  What's unclear or missing:
  ✗ User authentication (who can access? single-user or multi-user?)
  ✗ Task features (deadlines? priorities? categories? assignments?)
  ✗ Technology stack (React? Vue? Angular? Backend?)
  ✗ Data persistence (cloud database? local storage?)
  ✗ Sharing/collaboration (personal tasks only or team tasks?)

  Clarifying questions:
  1. Is this a personal task manager or team collaboration tool?
  2. What task features do you need (deadlines, priorities, tags, etc.)?
  3. What tech stack do you prefer, or should I recommend one?
  4. Where should data be stored (cloud vs local)?
  5. Do users need to share/assign tasks to others?

  Please provide more details, then run /sh_spec again.

# Example 2: High Confidence (Proceed)
User: /sh_spec "[detailed e-commerce specification with tech stack, features, architecture...]"

System:
  Running confidence check on specification...

  ✓ CONFIDENCE CHECK PASSED

  Confidence: 94% (exceeds 90% threshold)
  Recommendation: PROCEED

  What we understand well:
  ✓ Tech stack: React 18, Node.js, PostgreSQL, Redis
  ✓ Architecture: Microservices (auth, products, orders, payments)
  ✓ Features: 25 detailed user stories provided
  ✓ Authentication: OAuth 2.0 with JWT refresh tokens
  ✓ Payment processing: Stripe integration
  ✓ Deployment: AWS (ECS, RDS, ElastiCache)

  Minor gaps (not blocking):
  - Image optimization strategy not specified (will recommend best practices)
  - Rate limiting details missing (will implement standard approach)

  Proceeding to 8-dimensional complexity analysis...

# Example 3: Warning (User Decision)
User: /sh_spec "[specification with most details but some gaps]"

System:
  Running confidence check on specification...

  ⚠️ CONFIDENCE CHECK WARNING

  Confidence: 85% (close to 90% threshold, within acceptable range)
  Recommendation: WARN - Proceed with noted gaps OR gather more info

  What we understand well:
  ✓ Tech stack defined
  ✓ Core features clear
  ✓ Basic architecture outlined

  Gaps (can work around, but better to clarify):
  - Search functionality mentioned but algorithm not specified
  - Real-time updates desired but WebSocket vs polling not decided

  Options:
  1. Proceed now (I'll make reasonable assumptions for gaps)
  2. Clarify these 2 items first (recommended for optimal results)
  3. Skip confidence check for this session (--skip-confidence-gate)

  Your choice? (1/2/3)
```

**Threshold Configuration**:

```yaml
# .shannon/config.json (project-specific configuration)
{
  "confidence": {
    "default_threshold": 0.90,
    "phase_thresholds": {
      "specification": 0.90,
      "discovery": 0.85,
      "architecture": 0.90,
      "implementation": 0.80,  # Lower for exploratory implementation
      "testing": 0.95,         # Higher for testing (safety critical)
      "deployment": 0.95       # Highest for deployment
    },
    "project_type_overrides": {
      "critical_system": 0.95,    # Medical, financial, etc.
      "mvp_prototype": 0.75,      # Quick validation
      "refactoring": 0.85,        # Existing codebase
      "greenfield": 0.90          # New project (default)
    }
  }
}
```

**Status**: Design complete, TypeScript implementation ready for Phase 3 Wave 3.

---

## Change 5: SHANNON_INDEX Pattern

**Source**: Agent #6 (SuperClaude Framework Analysis)

**Rationale**:
- SuperClaude's PROJECT_INDEX pattern: 94% token reduction (58K → 3K tokens)
- Essential for large codebases (>10,000 lines)
- Break-even after 1 session, 380K tokens saved over 10 sessions

**Implementation**:

```yaml
SHANNON_INDEX.md Generation:

Trigger Conditions (any of):
  1. Codebase > 10,000 lines
  2. User runs /sh_index command explicitly
  3. project-indexing skill auto-activates (first analysis of large codebase)

Storage Location:
  - File: .shannon/SHANNON_INDEX.md
  - Cached in: Serena MCP (key: "shannon_index_v1")
  - Updated: Weekly OR when >1,000 lines changed

Content Structure (Following SuperClaude Pattern):
```

```markdown
# Shannon Index: [Project Name]

**Generated**: 2025-11-04 14:32:17
**Generator**: project-indexing skill v1.0.0
**Codebase Size**: 45,234 lines across 287 files
**Languages**: TypeScript (65%), Python (25%), CSS (8%), Other (2%)
**Last Updated**: 2025-11-04 14:32:17

---

## Project Overview

**Purpose**: E-commerce platform for selling handmade crafts
**Tech Stack**: React 18.2, Node.js 20, PostgreSQL 15, Redis 7
**Architecture Pattern**: Microservices (5 services)
**Deployment**: AWS ECS + RDS + ElastiCache

**Repository**: github.com/example/craft-marketplace
**Documentation**: docs/ (README, API docs, architecture diagrams)
**License**: MIT

---

## Directory Structure

```
project-root/
├── frontend/                       (React application, 18,234 lines)
│   ├── src/
│   │   ├── components/            (67 React components)
│   │   ├── pages/                 (12 page components)
│   │   ├── services/              (API clients, 8 services)
│   │   ├── hooks/                 (15 custom hooks)
│   │   ├── utils/                 (23 utility functions)
│   │   └── styles/                (Tailwind + custom CSS)
│   └── public/                    (Static assets)
│
├── backend/                        (Node.js services, 21,456 lines)
│   ├── auth-service/              (Authentication, JWT, OAuth)
│   ├── product-service/           (Product catalog, search)
│   ├── order-service/             (Cart, checkout, orders)
│   ├── payment-service/           (Stripe integration)
│   └── notification-service/      (Email, push notifications)
│
├── database/                       (SQL migrations, seeds)
│   ├── migrations/                (42 migration files)
│   └── seeds/                     (Test data)
│
├── infrastructure/                 (Terraform IaC, Docker)
│   ├── terraform/                 (AWS infrastructure)
│   └── docker/                    (Dockerfiles, docker-compose)
│
└── tests/                          (Functional tests, NO MOCKS)
    ├── e2e/                       (Puppeteer browser tests)
    └── integration/               (API integration tests)
```

---

## Key Components (Top 30)

### Frontend Components

**1. ProductCatalog** (`frontend/src/components/ProductCatalog.tsx`)
- **Purpose**: Displays paginated grid of products with filters/search
- **Props**: `filters`, `sortBy`, `onProductClick`
- **State**: `products`, `loading`, `pagination`, `selectedFilters`
- **Dependencies**: shadcn-ui Table, axios for API calls
- **Lines**: 342
- **Complexity**: MEDIUM (pagination, filtering, sorting logic)

**2. ShoppingCart** (`frontend/src/components/ShoppingCart.tsx`)
- **Purpose**: Cart sidebar with add/remove items, quantity adjustment
- **Props**: `isOpen`, `onClose`, `onCheckout`
- **State**: Redux store (`cart` slice)
- **Dependencies**: shadcn-ui Sheet, Redux
- **Lines**: 215
- **Key Functions**: `addToCart()`, `removeFromCart()`, `updateQuantity()`

**3. CheckoutFlow** (`frontend/src/pages/Checkout.tsx`)
- **Purpose**: Multi-step checkout (shipping, payment, review)
- **Props**: None (page component)
- **State**: `step`, `shippingInfo`, `paymentMethod`, `orderSummary`
- **Dependencies**: Stripe Elements, React Hook Form
- **Lines**: 487
- **Complexity**: HIGH (payment integration, validation, multi-step)

[... continues for top 30 components]

### Backend Services

**1. AuthenticationService** (`backend/auth-service/src/auth.service.ts`)
- **Purpose**: User authentication via OAuth 2.0 + JWT
- **Entry Points**: `login()`, `register()`, `refreshToken()`, `logout()`
- **Dependencies**: passport.js, jsonwebtoken, bcrypt
- **Database**: `users` table (PostgreSQL)
- **Lines**: 523
- **Key Flows**: OAuth flow, JWT generation/validation, password hashing

**2. ProductService** (`backend/product-service/src/product.service.ts`)
- **Purpose**: Product CRUD, search, filtering, recommendations
- **Entry Points**: `getProducts()`, `searchProducts()`, `getRecommendations()`
- **Dependencies**: Elasticsearch (search), Redis (caching)
- **Database**: `products`, `categories`, `product_images` tables
- **Lines**: 687
- **Complexity**: HIGH (search algorithms, caching strategy)

[... continues for top backend services]

---

## Data Models (Core Entities)

**Users** (`database/schema/users.sql`)
- Fields: id, email, password_hash, oauth_provider, created_at, updated_at
- Relationships: → orders (1:many), → cart_items (1:many)

**Products** (`database/schema/products.sql`)
- Fields: id, seller_id, name, description, price, inventory, created_at
- Relationships: → seller (many:1), → order_items (1:many), → categories (many:many)

**Orders** (`database/schema/orders.sql`)
- Fields: id, user_id, total, status, shipping_address, created_at
- Relationships: → user (many:1), → order_items (1:many), → payments (1:many)

[... all core entities with relationships]

---

## Dependencies (package.json)

**Frontend Production**:
- react@18.2.0
- react-router-dom@6.14.0
- @reduxjs/toolkit@1.9.5
- axios@1.5.0
- @stripe/stripe-js@2.1.0
- tailwindcss@3.3.3
- [15 more...]

**Backend Production**:
- express@4.18.2
- passport@0.6.0
- jsonwebtoken@9.0.2
- bcrypt@5.1.1
- pg@8.11.3 (PostgreSQL client)
- redis@4.6.7
- stripe@13.3.0
- [20 more...]

**Development**:
- typescript@5.1.6
- jest@29.6.2
- @testing-library/react@14.0.0
- puppeteer@21.1.1
- [25 more...]

---

## API Endpoints (Key Routes)

**Authentication** (`/api/auth`)
- POST /login - User login (email/password or OAuth)
- POST /register - New user registration
- POST /refresh - Refresh JWT token
- POST /logout - User logout

**Products** (`/api/products`)
- GET /products - List products (paginated, filtered)
- GET /products/:id - Get single product
- GET /products/search - Search products
- POST /products - Create product (sellers only)

**Orders** (`/api/orders`)
- GET /orders - User's order history
- POST /orders - Create new order (checkout)
- GET /orders/:id - Get order details
- PUT /orders/:id/cancel - Cancel order

[... all major API routes]

---

## Architecture Patterns

**State Management**: Redux Toolkit
- Store: `frontend/src/store/`
- Slices: cart, user, products, ui
- Middleware: Redux Thunk for async actions

**API Communication**: Axios
- Clients: `frontend/src/services/`
- Interceptors: JWT token injection, error handling
- Base URLs: Configured per environment

**Authentication**: OAuth 2.0 + JWT
- OAuth Providers: Google, GitHub
- JWT: Access token (15min) + Refresh token (7 days)
- Storage: HttpOnly cookies (secure)

**Database Access**: TypeORM
- Entities: `backend/*/src/entities/`
- Repositories: Type-safe query builders
- Migrations: Version-controlled schema changes

**Caching**: Redis
- Product catalog (TTL: 1 hour)
- User sessions (TTL: 7 days)
- Search results (TTL: 15 minutes)

**Testing**: NO MOCKS philosophy
- E2E: Puppeteer (real Chrome browser)
- API: Supertest (real HTTP requests to test server)
- Database: In-memory PostgreSQL (matches production schema)

---

## Recent Changes (Last 30 Days)

**PR #156** (2025-10-28): Add Google OAuth support
- Files: auth-service, frontend auth components
- Lines changed: +487 / -23

**PR #158** (2025-10-25): Upgrade React 18.1 → 18.2
- Files: package.json, multiple components
- Lines changed: +12 / -8
- Breaking: None

**Commit abc1234** (2025-10-20): Refactor product search with Elasticsearch
- Files: product-service
- Lines changed: +1,234 / -876
- Performance: 10x faster search

**PR #162** (2025-11-01): Implement Stripe payment integration
- Files: payment-service, checkout flow
- Lines changed: +1,567 / -12
- New dependencies: stripe@13.3.0

---

## Token Usage Comparison

**Full Codebase Context**:
- Total lines: 45,234
- Estimated tokens: ~58,000
- Context window usage: ~29%

**SHANNON_INDEX.md**:
- Lines: 387
- Estimated tokens: ~3,200
- Context window usage: ~1.6%

**Reduction**: 94.5% (54,800 tokens saved)

**Break-Even Analysis**:
- Generation cost: 2,000 tokens (one-time per session)
- Savings per usage: ~55,000 tokens
- Break-even: 1 usage (immediate ROI)
- 10 sessions: 550,000 tokens saved

---

## Notes

- Index auto-regenerates weekly (Sundays at 2 AM UTC)
- Manual regeneration: `/sh_index --force`
- Cached in Serena MCP for instant retrieval
- Version: 1.0.0 (follows semantic versioning)

**Usage**:
When analyzing this codebase, Claude should:
1. Load SHANNON_INDEX.md for context (not full codebase)
2. Read specific files only when modifying them
3. Use index to understand architecture without reading all files
4. Regenerate index after major changes (>1,000 lines)

---

*Generated by Shannon Framework v4.0.0 project-indexing skill*
```

**project-indexing Skill (Executable)**:

```python
# shannon-plugin/skills/project-indexing/project-indexing.py

import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class ProjectIndexer:
    """Generate SHANNON_INDEX.md for codebase compression."""

    def generate_index(self, project_root: str) -> str:
        """
        Generates comprehensive project index.

        Returns:
            Markdown content for SHANNON_INDEX.md
        """
        stats = self._gather_statistics(project_root)
        structure = self._analyze_structure(project_root)
        components = self._identify_key_components(project_root)
        dependencies = self._extract_dependencies(project_root)

        index_content = self._render_template(
            stats=stats,
            structure=structure,
            components=components,
            dependencies=dependencies
        )

        # Save to .shannon/SHANNON_INDEX.md
        index_path = Path(project_root) / '.shannon' / 'SHANNON_INDEX.md'
        index_path.parent.mkdir(exist_ok=True)
        index_path.write_text(index_content)

        # Cache in Serena MCP
        self._cache_in_serena(index_content)

        return index_content
```

**Triggers**:
```
Automatic (via auto-activation):
  - First /sh_spec on codebase >10,000 lines
  - Weekly regeneration (cron: Sundays 2 AM)
  - After major changes (>1,000 lines modified)

Manual:
  - /sh_index (generates fresh index)
  - /sh_index --force (regenerates even if recent)
```

**Status**: Design complete, Python implementation ready for Phase 3 Wave 3.

---

## Summary of Architectural Updates

All 10 critical changes from Phase 1 research have been incorporated into Shannon Framework v4 architecture:

1. ✅ **Executable Skills Pattern** - 6 skills with TypeScript/Python code
2. ✅ **Progressive Disclosure** - 3-level loading (50 tokens → 500 lines → unlimited)
3. ✅ **Auto-Activation** - Context-based skill triggering
4. ✅ **Confidence Gating** - ≥90% threshold at spec/phase/wave levels
5. ✅ **SHANNON_INDEX** - 94% token reduction for large codebases
6. ✅ **Deprecate sc_* Commands** - 24 commands deprecated, 6-month transition
7. ✅ **MCP Integration** - 4 patterns (declarative, progressive, fallback, orchestration)
8. ✅ **SITREP Protocol** - Standardized multi-agent communication
9. ✅ **Validation Gates** - NO MOCKS enforcement with functional tests
10. ✅ **Skill Composition** - REQUIRED SUB-SKILL pattern formalized

**Architecture Status**: VALIDATED (92% confidence), APPROVED for implementation

**Ready for Phase 3**: Foundation components, execution infrastructure, skill development

---

**Document Version**: 2.0
**Last Updated**: 2025-11-04
**Next Review**: After Phase 3 Wave 1 (foundation components complete)
