# Specification Analysis Behavioral Patterns

## Overview

This file defines behavioral patterns for Claude Code to automatically analyze user specifications and extract structured intelligence for project planning through Shannon Framework.

**Purpose**: Transform unstructured specifications into actionable project plans with quantitative metrics

**Method**: Pattern recognition, keyword analysis, 8-dimensional complexity scoring, domain mapping, MCP suggestion

**Output**: Structured analysis with complexity metrics, domain breakdown, MCP recommendations, phase plans, actionable todos

**Core Philosophy**: Objective, reproducible, systematic analysis that directly informs resource allocation, timeline estimation, and risk assessment.

---

## Automatic Detection Triggers

Shannon's specification analysis activates automatically when user input contains ANY of:

### Multi-Paragraph Specifications
- **Trigger**: 3+ paragraphs describing a system or project
- **Condition**: Each paragraph > 50 words
- **Pattern**: Contains architectural descriptions, feature lists, or technical requirements

### Requirements Lists
- **Trigger**: 5+ distinct items in list format
- **Pattern**: Numbered lists, bullet points, feature enumerations
- **Example**: "Build system with: 1) User auth 2) Dashboard 3) Reports 4) API 5) Admin panel"

### Explicit Keywords
**Primary Keywords** (high confidence):
- "specification", "spec", "requirements", "PRD", "user stories"
- "build", "implement", "create", "develop" (with multi-sentence context)
- "system design", "architecture", "technical design"

**Secondary Keywords** (moderate confidence):
- "needs to", "must have", "should include"
- "features", "functionality", "capabilities"
- "users can", "system will", "application should"

### File Attachments
- **Trigger**: User attaches *.pdf, *.md, *.doc, *.docx files
- **Pattern**: Files containing specification-like content
- **Detection**: Scan first 500 words for requirement patterns

### Detection Algorithm
```
FUNCTION should_activate_spec_analysis(user_input):
  paragraph_count = count_paragraphs(user_input)
  avg_paragraph_length = average_words_per_paragraph(user_input)
  list_item_count = count_list_items(user_input)

  has_primary_keywords = contains_any(user_input, primary_keywords)
  has_secondary_keywords = contains_any(user_input, secondary_keywords)
  word_count = total_words(user_input)

  IF (paragraph_count >= 3 AND avg_paragraph_length > 50)
     OR (list_item_count >= 5)
     OR (has_primary_keywords AND word_count > 100)
     OR (has_secondary_keywords AND word_count > 200)
     OR (file_attachment AND file_type in [pdf, md, doc, docx])
  THEN
    RETURN true (activate spec analysis)
  ELSE
    RETURN false (standard conversation mode)
  END IF
END FUNCTION
```

---

## 8-Dimensional Complexity Framework

### Framework Purpose

Provide objective, reproducible complexity scoring to guide:
- **Sub-agent allocation**: How many agents to spawn (3-25 based on score)
- **Wave structure**: How many waves needed (1-8 based on complexity)
- **Timeline estimation**: Project duration (hours to weeks)
- **Resource planning**: MCP servers, tools, infrastructure needs
- **Risk assessment**: Potential challenges and mitigation strategies

### Scoring Philosophy

- **Objective**: Based on measurable indicators, not subjective judgment
- **Reproducible**: Same specification always produces same score
- **Granular**: 8 dimensions provide nuanced understanding of complexity types
- **Actionable**: Score directly informs planning decisions and resource allocation
- **Weighted**: Dimensions weighted by impact on project complexity

### Dimension 1: Structural Complexity (Weight: 20%)

**Definition**: Measures project scope through file count, service count, module organization, and system breadth.

**Why 20% weight**: Structural scope is the PRIMARY driver of project complexity - more components directly = more work.

**Scoring Algorithm**:
```
structural_score = min(1.0, weighted_sum of:
  - file_factor × 0.40
  - service_factor × 0.30
  - module_factor × 0.20
  - component_factor × 0.10
)

WHERE:

file_factor = log10(file_count + 1) / 3
  Examples:
    1 file: log10(2) / 3 = 0.10
    10 files: log10(11) / 3 = 0.35
    50 files: log10(51) / 3 = 0.57
    100 files: log10(101) / 3 = 0.67
    1000 files: log10(1001) / 3 = 1.0

service_factor = min(1.0, service_count / 20)
  Examples:
    1 service (monolith): 1 / 20 = 0.05
    5 services (microservices): 5 / 20 = 0.25
    10 services: 10 / 20 = 0.50
    20+ services: 1.0

module_factor = min(1.0, module_count / 15)
  Examples:
    1 module: 0.07
    5 modules: 0.33
    15+ modules: 1.0

component_factor = min(1.0, component_count / 10)
  Examples:
    3 components: 0.30
    10+ components: 1.0
```

**Detection Patterns** (regex):
```regex
File count:
  \b(\d+)\s+(files?|components?)\b
  "(entire|all|complete)\s+(\w+)\s+system" → multiply by 1.5

Service count:
  \b(\d+)\s+(services?|microservices?|APIs?)\b
  "monolith" → service_count = 1

Module references:
  \b(\d+)\s+(modules?|packages?|libraries?)\b

Qualifier multipliers:
  "entire" → ×1.5
  "all" → ×1.3
  "comprehensive" → ×1.2
  "complete" → ×1.2
  "full" → ×1.1
```

**Scoring Examples**:

| Specification Text | Detection | Calculation | Score | Interpretation |
|--------------------|-----------|-------------|-------|----------------|
| "Update login function in auth.ts" | 1 file | log10(2)/3 × 0.4 = 0.04 | 0.04 | Trivial |
| "Refactor authentication module (15 files)" | 15 files | log10(16)/3 × 0.4 = 0.16 | 0.16 | Low |
| "Redesign user management (50 files, 3 modules)" | 50 files, 3 modules | (0.57×0.4) + (0.2×0.2) = 0.27 | 0.27 | Moderate |
| "Redesign ENTIRE user system across 50 files" | 50 files, "entire" × 1.5 | 0.27 × 1.5 = 0.41 | 0.41 | Moderate-High |
| "Build e-commerce with 5 microservices, 80 files" | 80 files, 5 services | (0.63×0.4) + (0.25×0.3) = 0.33 | 0.33 | Moderate |
| "Migrate ALL 200 services to new architecture" | 200 services, "all" × 1.3 | 1.0 × 1.3 = 1.0 (capped) | 1.0 | Critical |

### Dimension 2: Cognitive Complexity (Weight: 15%)

**Definition**: Measures mental effort required - analysis depth, design sophistication, decision-making complexity, learning needs.

**Why 15% weight**: Cognitive load significantly impacts timeline and quality, but less than raw structural scope.

**Scoring Algorithm**:
```
cognitive_score = min(1.0, sum_of_verb_scores)

Verb Categories (cumulative scoring):

analysis_verbs = ["analyze", "understand", "comprehend", "study", "examine", "investigate", "research"]
  Score per occurrence: +0.20 (max 0.40 for 2+ occurrences)

design_verbs = ["design", "architect", "plan", "structure", "model", "blueprint", "conceptualize"]
  Score per occurrence: +0.20 (max 0.40)

decision_verbs = ["choose", "select", "evaluate", "compare", "assess", "decide", "determine"]
  Score per occurrence: +0.10 (max 0.30)

learning_verbs = ["learn", "explore", "discover", "experiment"]
  Score per occurrence: +0.15 (max 0.30)

abstract_concepts = ["architecture", "pattern", "strategy", "methodology", "framework", "paradigm"]
  Score per occurrence: +0.15 (max 0.30)
```

**Scoring Examples**:

| Specification | Verbs Detected | Calculation | Score | Interpretation |
|---------------|----------------|-------------|-------|----------------|
| "Fix the login bug" | None | Base: 0.0 | 0.10 | Minimal cognitive load |
| "Design authentication architecture" | design(0.20) + architecture(0.15) | 0.35 | 0.35 | Moderate cognitive load |
| "Analyze, architect, and research ML inference system" | analyze(0.20) + architect(0.20) + research(0.20, capped at 0.40 for analysis_verbs) + architecture(0.15) | 0.75 | 0.75 | High cognitive load |
| "Study distributed systems patterns, design microservices, evaluate trade-offs" | study(0.20) + patterns(0.15) + design(0.20) + evaluate(0.10) | 0.65 | 0.65 | High cognitive load |

### Dimension 3: Coordination Complexity (Weight: 15%)

**Definition**: Measures team coordination, component integration, and cross-functional collaboration needs.

**Why 15% weight**: Coordination overhead is major complexity driver, especially in larger projects.

**Scoring Algorithm**:
```
coordination_score = min(1.0,
  (team_count × 0.25) +
  (integration_keyword_count × 0.15) +
  (stakeholder_count × 0.10)
)

WHERE:

team_count = count_unique_teams_mentioned:
  Teams detected by keywords:
    - "frontend team" | "frontend" | "UI team" | "client team" → frontend_team
    - "backend team" | "backend" | "API team" | "server team" → backend_team
    - "database team" | "data team" | "DBA" → database_team
    - "DevOps team" | "infrastructure team" | "platform team" → devops_team
    - "security team" | "infosec" | "security" → security_team
    - "QA team" | "testing team" | "quality" → qa_team
    - "mobile team" | "iOS team" | "Android team" → mobile_team

integration_keyword_count = count_occurrences_of:
  ["coordinate", "integrate", "sync", "align", "collaborate", "communicate",
   "interface", "handoff", "dependency", "cross-team"]

stakeholder_count = count_mentions_of:
  ["teams", "departments", "groups", "stakeholders", "organizations"]
```

**Scoring Examples**:

| Specification | Detection | Calculation | Score |
|---------------|-----------|-------------|-------|
| "Build API endpoint" | 0 teams, 0 integration keywords | 0.0 | 0.0 |
| "Coordinate frontend and backend teams on API design" | 2 teams, 1 integration keyword | (2 × 0.25) + (1 × 0.15) = 0.65 | 0.65 |
| "Align across frontend, backend, DevOps, security, and QA teams with multiple integration points" | 5 teams, 3 integration keywords | (5 × 0.25 = 1.0, capped) + (3 × 0.15 = 0.45) = 1.0 (capped) | 1.0 |

### Dimension 4: Temporal Complexity (Weight: 10%)

**Definition**: Measures time pressure, deadline constraints, and urgency factors.

**Why 10% weight**: Deadlines impact planning but don't fundamentally change technical complexity.

**Scoring Algorithm**:
```
temporal_score = min(1.0,
  urgency_multiplier + deadline_factor
)

WHERE:

urgency_multiplier (from keywords):
  "urgent" | "emergency" | "critical" | "ASAP" | "immediately" → +0.40
  "soon" | "quickly" | "fast" | "rapid" → +0.30
  "standard timeline" | "normal priority" → +0.10

deadline_factor (from time mentions):
  deadline_mentioned = TRUE if contains:
    - "\d+ (hours?|days?|weeks?)"
    - "by (tomorrow|next week|end of month)"
    - "deadline:", "due date:"

  IF deadline_mentioned:
    Extract time_value and time_unit
    IF time_unit = "hours": +0.50
    IF time_unit = "days" AND time_value < 3: +0.40
    IF time_unit = "days" AND time_value < 7: +0.30
    IF time_unit = "weeks" AND time_value < 2: +0.20
    ELSE: +0.10
  ELSE:
    deadline_factor = 0.0
```

**Scoring Examples**:

| Specification | Detection | Score |
|---------------|-----------|-------|
| "Build user dashboard" | No urgency, no deadline | 0.10 |
| "Build dashboard, need it soon" | "soon" keyword | 0.30 |
| "URGENT: Fix login bug within 24 hours" | "urgent" + 24 hours deadline | 0.90 |
| "Complete feature by next week" | 1 week deadline | 0.30 |

### Dimension 5: Technical Complexity (Weight: 15%)

**Definition**: Measures sophistication of technologies, algorithms, and advanced technical requirements.

**Why 15% weight**: Technical difficulty significantly impacts implementation time and expertise needs.

**Scoring Algorithm**:
```
technical_score = min(1.0,
  advanced_tech_factor +
  algorithm_factor +
  integration_factor
)

WHERE:

advanced_tech_factor = count_matches × 0.20 (max 0.60)
  Advanced technologies:
    - AI/ML: "machine learning", "neural network", "LLM", "GPT", "model training", "inference"
    - Real-time: "WebSocket", "real-time", "streaming", "pub/sub", "message queue"
    - Distributed: "microservices", "distributed system", "consensus", "CAP theorem"
    - Low-level: "memory management", "concurrency", "thread pool", "async/await"
    - Security: "encryption", "cryptography", "zero-trust", "OAuth", "JWT"

algorithm_factor = count_matches × 0.20 (max 0.40)
  Complex algorithms:
    - "algorithm", "optimization", "O(n log n)", "dynamic programming"
    - "graph", "tree traversal", "search algorithm", "sorting"
    - "pathfinding", "recommendation engine", "ranking algorithm"

integration_factor = count_matches × 0.15 (max 0.30)
  Third-party integrations:
    - "API integration", "third-party", "webhook", "OAuth provider"
    - "payment gateway", "Stripe", "PayPal"
    - Specific services: "AWS S3", "SendGrid", "Twilio"
```

**Scoring Examples**:

| Specification | Detection | Score |
|---------------|-----------|-------|
| "CRUD app with basic forms" | No advanced tech | 0.10 |
| "Real-time chat with WebSocket" | 1 real-time tech | 0.30 |
| "ML recommendation engine with real-time updates and Stripe integration" | 3 matches (ML + real-time + integration) | 0.55 |
| "Distributed microservices with event-driven architecture, ML inference, and complex graph algorithms" | Multiple advanced (0.60) + algorithms (0.40) | 1.0 |

### Dimension 6: Scale Complexity (Weight: 10%)

**Definition**: Measures data volume, user load, and performance requirements.

**Why 10% weight**: Scale impacts architecture but is less fundamental than core complexity.

**Scoring Algorithm**:
```
scale_score = min(1.0,
  user_factor +
  data_factor +
  performance_factor
)

WHERE:

user_factor (from mentions):
  IF contains "\d+\s*(users?|concurrent)"
    Extract user_count
    IF user_count > 1_000_000: +0.40
    IF user_count > 100_000: +0.30
    IF user_count > 10_000: +0.20
    IF user_count > 1_000: +0.10
    ELSE: +0.05

data_factor (from mentions):
  IF contains "\d+\s*(GB|TB|PB|million|billion)\s+(records?|rows?|documents?)"
    Extract data_size
    IF data_size in TB or billions: +0.40
    IF data_size in GB or millions: +0.20
    ELSE: +0.10

performance_factor (from requirements):
  "high performance" | "low latency" | "< \d+ms" → +0.20
  "scalable" | "scale to" → +0.15
  "caching" | "CDN" | "load balancing" → +0.10
```

**Scoring Examples**:

| Specification | Detection | Score |
|---------------|-----------|-------|
| "Small app for internal team" | No scale mentions | 0.10 |
| "App for 50,000 users with 10GB data" | 50K users + 10GB | 0.40 |
| "High-performance system for 5M concurrent users, TB-scale data" | 5M users + TB + high-perf | 1.0 |

### Dimension 7: Uncertainty Complexity (Weight: 10%)

**Definition**: Measures ambiguities, unknowns, and exploratory requirements.

**Why 10% weight**: Uncertainty adds planning overhead but doesn't change fundamental complexity.

**Scoring Algorithm**:
```
uncertainty_score = min(1.0,
  ambiguity_factor +
  exploratory_factor +
  research_factor
)

WHERE:

ambiguity_factor = count_matches × 0.20 (max 0.40)
  Ambiguous language:
    - "TBD", "to be determined", "unclear", "not sure", "possibly"
    - "maybe", "might", "could be", "approximately"
    - Question marks in requirements

exploratory_factor = count_matches × 0.15 (max 0.30)
  Exploratory terms:
    - "explore", "investigate", "proof of concept", "POC", "prototype"
    - "experiment with", "try different approaches"

research_factor = count_matches × 0.15 (max 0.30)
  Research needs:
    - "research", "evaluate options", "compare solutions"
    - "not decided yet", "need to investigate"
```

**Scoring Examples**:

| Specification | Detection | Score |
|---------------|-----------|-------|
| "Build login with email/password" | Clear requirements | 0.10 |
| "Build dashboard, layout TBD, explore different chart libraries" | 2 ambiguous terms | 0.40 |
| "Prototype recommendation system, research ML approaches, evaluate trade-offs (details unclear)" | Multiple uncertainty markers | 0.75 |

### Dimension 8: Dependencies Complexity (Weight: 5%)

**Definition**: Measures blocking dependencies and prerequisite requirements.

**Why 5% weight**: Dependencies cause delays but are often manageable with planning.

**Scoring Algorithm**:
```
dependency_score = min(1.0,
  blocking_factor +
  external_factor
)

WHERE:

blocking_factor = count_matches × 0.25 (max 0.50)
  Blocking language:
    - "blocked by", "depends on", "requires", "prerequisite"
    - "waiting for", "needs approval", "gated by"

external_factor = count_matches × 0.20 (max 0.50)
  External dependencies:
    - "third-party approval", "vendor", "partner team"
    - "external API", "waiting on other team"
```

**Scoring Examples**:

| Specification | Detection | Score |
|---------------|-----------|-------|
| "Build feature (all resources available)" | No dependencies | 0.10 |
| "Implement after auth system complete" | 1 blocker | 0.35 |
| "Blocked by vendor API approval, requires partner team integration, waiting on security review" | 3 blockers | 0.75 |

---

### Total Complexity Calculation

**Weighted Sum Formula**:
```
total_complexity_score =
  0.20 × structural_score +
  0.15 × cognitive_score +
  0.15 × coordination_score +
  0.10 × temporal_score +
  0.15 × technical_score +
  0.10 × scale_score +
  0.10 × uncertainty_score +
  0.05 × dependency_score

Result: 0.0 - 1.0 (floating point)
```

**Interpretation Bands**:

| Score Range | Label | Sub-Agents | Waves | Timeline | Characteristics |
|-------------|-------|------------|-------|----------|-----------------|
| 0.00-0.30 | Simple | 1-2 | 0-1 | Hours-1 day | Single file/function, clear requirements, minimal coordination |
| 0.30-0.50 | Moderate | 2-3 | 1-2 | 1-2 days | Multi-file, some design needed, limited dependencies |
| 0.50-0.70 | Complex | 3-7 | 2-3 | 2-4 days | Cross-module, significant design, some unknowns |
| 0.70-0.85 | High | 8-15 | 3-5 | 1-2 weeks | System-wide, advanced tech, multiple teams |
| 0.85-1.00 | Critical | 15-25 | 5-8 | 2+ weeks | Enterprise-scale, cutting-edge tech, high uncertainty |

**Example Calculation**:

Specification: "Build e-commerce web app with React frontend (20 components), Express backend (5 microservices), PostgreSQL database, real-time inventory updates via WebSocket, integrate Stripe payment gateway, support 100K users, ML-based product recommendations, requires design phase"

**Dimension Scores**:
- Structural: 20 components → 0.40
- Cognitive: "design" + "recommendations" → 0.35
- Coordination: frontend + backend + database (3 teams) → 0.75
- Temporal: Standard (no urgency) → 0.10
- Technical: Real-time + ML + integration → 0.55
- Scale: 100K users → 0.30
- Uncertainty: Clear requirements → 0.10
- Dependencies: No blockers → 0.10

**Weighted Calculation**:
```
total = (0.20 × 0.40) + (0.15 × 0.35) + (0.15 × 0.75) + (0.10 × 0.10) +
        (0.15 × 0.55) + (0.10 × 0.30) + (0.10 × 0.10) + (0.05 × 0.10)
      = 0.08 + 0.0525 + 0.1125 + 0.01 + 0.0825 + 0.03 + 0.01 + 0.005
      = 0.3825 ≈ 0.38

Interpretation: MODERATE complexity
Recommendation: 2-3 sub-agents, 1-2 waves, 1-2 days
```

---

## Domain Identification Logic

### Purpose

Identify all technical domains involved in specification to:
- Suggest appropriate MCP servers for each domain
- Allocate specialized sub-agents (frontend-architect, backend-architect, etc.)
- Plan parallel wave execution by domain
- Estimate resource needs and expertise requirements

### 6 Primary Domains

#### Domain 1: Frontend

**Keywords** (case-insensitive matching):
```
UI, UX, component, React, Vue, Angular, Svelte, Next.js, Nuxt, Gatsby,
interface, design, responsive, mobile-first, web app, dashboard, form,
button, navigation, navbar, sidebar, modal, dialog, card, table, list,
grid, chart, graph, visualization, layout, CSS, SCSS, Sass, Tailwind,
styled-components, HTML, JavaScript, TypeScript, JSX, TSX, animation,
transition, accessibility, ARIA, semantic HTML, DOM, browser, client-side,
SPA, PWA, service worker, webpack, Vite, Rollup
```

**File Pattern Matching**:
```regex
Filenames suggesting frontend:
  - *.jsx, *.tsx, *.vue, *.svelte
  - *Component.*, *View.*, *Page.*
  - *.css, *.scss, *.sass, *.less
  - components/*, views/*, pages/*, layouts/*
```

**Percentage Calculation**:
```
frontend_keyword_count = count_occurrences(frontend_keywords, spec_text)
total_domain_keywords = sum(all_domain_keyword_counts)
frontend_percentage = (frontend_keyword_count / total_domain_keywords) × 100

Round to nearest integer
```

**MCP Suggestions** (if frontend ≥ 20%):
- **Magic MCP** (Primary) - React/Vue/Angular component generation from 21st.dev
- **Puppeteer MCP** (Primary) - Functional browser testing (Shannon's NO MOCKS mandate)
- **Context7 MCP** (Secondary) - Official React/Vue/Angular documentation
- **Playwright MCP** (Alternative) - Cross-browser E2E testing

**Testing Approach**: Puppeteer functional tests with real browser (NO MOCKS)

**Example**:
```
Spec: "Build React dashboard with charts, tables, forms, responsive design"
Frontend keywords detected: React(1), dashboard(1), charts(1), tables(1), forms(1), responsive(1), design(1) = 7 matches
Total keywords: 7 (100% frontend)
Domain: Frontend 100%
Suggests: Magic MCP, Puppeteer MCP, Context7 MCP
```

#### Domain 2: Backend

**Keywords**:
```
API, endpoint, REST, RESTful, GraphQL, gRPC, server, service, microservice,
backend, Express, Koa, Fastify, NestJS, FastAPI, Django, Flask, Spring Boot,
Go, Rust, authentication, authorization, auth, JWT, OAuth, session, cookie,
business logic, controller, route, handler, middleware, model, ORM, Prisma,
TypeORM, Sequelize, Drizzle, validation, error handling, logging, monitoring,
rate limiting, caching, Redis, message queue, Kafka, RabbitMQ, pub/sub,
serverless, Lambda, Cloud Functions, backend integration
```

**File Patterns**:
```regex
*Controller.*, *Service.*, *Handler.*, *Route.*, *Middleware.*
controllers/*, services/*, api/*, routes/*, handlers/*
```

**MCP Suggestions** (if backend ≥ 20%):
- **Context7 MCP** (Primary) - Express/FastAPI/Django/Spring documentation
- **Sequential MCP** (Primary) - Complex backend logic analysis
- **Database MCP** (Primary) - Based on database mentioned (Postgres, Mongo, MySQL)
- **Serena MCP** (Mandatory) - Session persistence

**Testing**: Real HTTP requests, real database operations on test instance (NO MOCKS)

#### Domain 3: Database

**Keywords**:
```
database, DB, schema, migration, query, SQL, NoSQL, relational, document,
PostgreSQL, Postgres, MySQL, MariaDB, SQLite, MongoDB, DynamoDB, Cassandra,
Redis, Memcached, Elasticsearch, data model, table, collection, document,
ORM, Prisma, TypeORM, Sequelize, Mongoose, SQLAlchemy, Hibernate, GORM,
transaction, ACID, index, foreign key, join, aggregation, normalization,
data persistence, data layer, repository pattern
```

**MCP Suggestions** (if database ≥ 15%):
- **PostgreSQL MCP** (if Postgres mentioned)
- **MongoDB MCP** (if MongoDB mentioned)
- **MySQL MCP** (if MySQL mentioned)
- **Redis MCP** (if Redis/cache mentioned)
- **Context7 MCP** (for ORM documentation)

**Testing**: Real database operations on test instance (NO MOCKS)

#### Domain 4: Mobile/iOS

**Keywords**:
```
iOS, iPhone, iPad, mobile app, native app, Swift, SwiftUI, UIKit, Objective-C,
Xcode, App Store, TestFlight, CoreData, HealthKit, StoreKit, ARKit, CoreML,
Push notifications, APNS, CocoaPods, Swift Package Manager, watchOS, tvOS,
iOS simulator, device testing, mobile-first, responsive, touch gestures
```

**MCP Suggestions** (if mobile ≥ 40%):
- **SwiftLens MCP** (Primary) - Swift code analysis, symbol operations
- **iOS Simulator Tools** (Primary) - XCUITest functional testing on simulator
- **Context7 MCP** (Secondary) - SwiftUI/UIKit/Foundation documentation

**Testing**: XCUITest on actual iOS simulator (NO MOCKS)

#### Domain 5: DevOps

**Keywords**:
```
deploy, deployment, CI/CD, pipeline, Docker, Dockerfile, container,
Kubernetes, K8s, orchestration, infrastructure, IaC, Terraform, CloudFormation,
monitoring, observability, logging, Prometheus, Grafana, ELK, Datadog, Sentry,
AWS, Azure, GCP, cloud, serverless, EC2, S3, Lambda, RDS, CloudFront, CDN,
load balancing, auto-scaling, health check, blue-green deployment, canary,
rollback, backup, disaster recovery, high availability
```

**MCP Suggestions** (if devops ≥ 15%):
- **GitHub MCP** - CI/CD workflow automation
- **AWS MCP** (if AWS mentioned)
- **Azure MCP** (if Azure mentioned)
- **Kubernetes MCP** (if K8s mentioned)

#### Domain 6: Security

**Keywords**:
```
security, authentication, authorization, encryption, HTTPS, SSL, TLS,
certificate, OAuth, OpenID Connect, SAML, JWT, token, session security,
RBAC, role-based access, permission, access control, firewall, WAF,
vulnerability, penetration testing, security audit, OWASP, XSS, CSRF,
SQL injection, input validation, sanitization, hashing, bcrypt, Argon2,
compliance, GDPR, HIPAA, SOC2, PCI-DSS, security headers, CSP, CORS
```

**MCP Suggestions** (if security ≥ 15%):
- **Context7 MCP** - Security patterns, OAuth libraries, OWASP guidelines
- **Sequential MCP** - Threat modeling, security architecture analysis

---

### Domain Percentage Distribution Algorithm

**Step-by-Step Process**:

1. **Count Keywords for Each Domain**:
```
FUNCTION count_domain_keywords(spec_text, domain_keywords):
  count = 0
  FOR EACH keyword IN domain_keywords:
    occurrences = case_insensitive_count(keyword, spec_text)
    count += occurrences
  END FOR
  RETURN count
END FUNCTION

frontend_count = count_domain_keywords(spec, frontend_keywords)
backend_count = count_domain_keywords(spec, backend_keywords)
database_count = count_domain_keywords(spec, database_keywords)
mobile_count = count_domain_keywords(spec, mobile_keywords)
devops_count = count_domain_keywords(spec, devops_keywords)
security_count = count_domain_keywords(spec, security_keywords)
```

2. **Calculate Raw Percentages**:
```
total_count = frontend_count + backend_count + database_count +
              mobile_count + devops_count + security_count

frontend_raw = (frontend_count / total_count) × 100
backend_raw = (backend_count / total_count) × 100
database_raw = (database_count / total_count) × 100
mobile_raw = (mobile_count / total_count) × 100
devops_raw = (devops_count / total_count) × 100
security_raw = (security_count / total_count) × 100
```

3. **Round and Normalize**:
```
Round each percentage to nearest integer

Calculate sum of rounded percentages
IF sum ≠ 100:
  difference = 100 - sum
  Distribute difference to largest domain(s)
END IF

VERIFICATION: sum of all percentages MUST equal 100%
```

**Example Calculation**:

Spec: "Build task management web app with React frontend, Express backend, PostgreSQL database, Docker deployment"

```
Keyword Counts:
  Frontend: React(1), web app(1), frontend(1) = 3
  Backend: Express(1), backend(1) = 2
  Database: PostgreSQL(1), database(1) = 2
  DevOps: Docker(1), deployment(1) = 2
  Mobile: 0
  Security: 0
  Total: 9

Raw Percentages:
  Frontend: 3/9 × 100 = 33.33%
  Backend: 2/9 × 100 = 22.22%
  Database: 2/9 × 100 = 22.22%
  DevOps: 2/9 × 100 = 22.22%

Rounded:
  Frontend: 33%
  Backend: 22%
  Database: 22%
  DevOps: 22%
  Sum: 99% (need to add 1%)

Distribute difference to largest (Frontend):
  Frontend: 34%
  Backend: 22%
  Database: 22%
  DevOps: 22%
  Sum: 100% ✓
```

**Output Format**:
```markdown
## Domain Analysis

**Frontend (34%)**:
- React UI framework
- Component-based architecture
- Web application interface

**Backend (22%)**:
- Express REST API server
- Business logic layer
- API endpoint handling

**Database (22%)**:
- PostgreSQL relational database
- Data persistence layer
- Schema design and migrations

**DevOps (22%)**:
- Docker containerization
- Deployment infrastructure
- Environment configuration
```

---

## MCP Server Suggestion Engine

### Purpose

Based on domain analysis, automatically suggest appropriate MCP servers with clear rationale, priority, and usage guidance.

### Suggestion Algorithm

```
FUNCTION suggest_mcp_servers(domain_percentages, spec_text):
  suggested_mcps = []

  // Step 1: MANDATORY MCPs (always suggest)
  suggested_mcps.add({
    name: "Serena MCP",
    tier: 1,
    priority: "MANDATORY",
    rationale: "Essential for session persistence and context preservation across waves",
    usage: "Save spec analysis, phase plans, wave results, enable context restoration"
  })

  // Step 2: Domain-based PRIMARY MCPs (≥20% threshold)
  FOR EACH domain IN domain_percentages:
    IF domain.percentage >= 20%:
      domain_mcps = get_mcps_for_domain(domain.name)
      FOR EACH mcp IN domain_mcps:
        suggested_mcps.add({
          name: mcp.name,
          tier: 2,
          priority: "PRIMARY",
          rationale: mcp.rationale + " (Domain: " + domain.name + " " + domain.percentage + "%)",
          usage: mcp.usage
        })
      END FOR
    END IF
  END FOR

  // Step 3: Keyword-based SECONDARY MCPs
  IF contains_keywords(spec_text, ["research", "investigate", "explore"]):
    suggested_mcps.add({name: "Tavily MCP", tier: 3, priority: "SECONDARY"})
  END IF

  IF contains_keywords(spec_text, ["version control", "git", "repository"]):
    suggested_mcps.add({name: "GitHub MCP", tier: 3, priority: "SECONDARY"})
  END IF

  // Step 4: Remove duplicates, sort by tier and priority
  RETURN deduplicate_and_sort(suggested_mcps)
END FUNCTION
```

### MCP Priority Matrix

#### Tier 1: MANDATORY (Always Suggested)

**Serena MCP** 🔴
- **Priority**: CRITICAL
- **Rationale**: Essential for Shannon's zero-context-loss architecture
- **Usage**:
  - Save complete specification analysis to memory
  - Store phase plans and wave results
  - Enable context restoration after auto-compact
  - Share context across ALL sub-agents
- **Commands**: `write_memory("key", data)`, `read_memory("key")`, `list_memories()`
- **When**: Every Shannon project, every wave, every phase
- **Alternative**: None (Serena is mandatory for Shannon operation)

#### Tier 2: PRIMARY (Domain-Based, ≥20% threshold)

**Frontend Domain (≥20%)**:

1. **Magic MCP**
   - **Rationale**: Rapid UI component generation from 21st.dev component library with modern patterns
   - **Usage**: Generate React/Vue/Angular components, forms, modals, navigation, dashboards
   - **When**: Building UI, implementing design systems, creating responsive layouts
   - **Alternative**: Manual component coding (slower, less consistent)
   - **Example**: `/ui button --variant primary --size large` generates production-ready button component

2. **Puppeteer MCP**
   - **Rationale**: Functional browser testing (Shannon's NO MOCKS mandate)
   - **Usage**: Test real user interactions in actual browser, validate UI behavior functionally
   - **When**: Phase 4 (Integration Testing), validation gates, E2E testing
   - **Alternative**: Playwright MCP (similar), manual testing (slower)
   - **Why NO MOCKS**: Real browser = real confidence, catches browser-specific issues

3. **Context7 MCP**
   - **Rationale**: Official React/Vue/Angular/Svelte documentation lookup
   - **Usage**: Load framework patterns, hooks documentation, best practices
   - **When**: Implementing features, learning APIs, following official patterns
   - **Alternative**: Web search (less curated), manual documentation (slower)
   - **Example**: Lookup React useEffect patterns, Vue composition API

**Backend Domain (≥20%)**:

1. **Context7 MCP**
   - **Rationale**: Express/FastAPI/Django/Spring framework documentation
   - **Usage**: Load framework patterns, middleware examples, API design best practices
   - **When**: Implementing API endpoints, setting up backend architecture
   - **Alternative**: Web search, Stack Overflow (less reliable)

2. **Sequential MCP**
   - **Rationale**: Complex backend logic analysis and multi-step reasoning
   - **Usage**: Design complex business logic, analyze architectural trade-offs, systematic debugging
   - **When**: Architecture design, complex implementation decisions, system analysis
   - **Alternative**: Native Claude reasoning (less structured, no hypothesis tracking)

3. **Database MCP** (Specific to DB type)
   - **Rationale**: Direct database schema operations and query optimization
   - **Usage**: Create schemas, run migrations, execute queries, analyze performance
   - **When**: Database design, schema changes, data operations
   - **Alternative**: Manual SQL writing, ORM code (more verbose)
   - **Options**: PostgreSQL MCP, MongoDB MCP, MySQL MCP, Redis MCP

**Mobile/iOS Domain (≥40%)**:

1. **SwiftLens MCP**
   - **Rationale**: Swift code analysis, symbol operations, semantic understanding
   - **Usage**: Analyze Swift codebases, find symbol references, refactor code
   - **When**: Working with existing Swift projects, large-scale refactoring
   - **Alternative**: Manual code analysis (slow, error-prone)

2. **iOS Simulator Tools**
   - **Rationale**: Functional testing on actual iOS simulator (NO MOCKS)
   - **Usage**: Run XCUITests on simulator, validate app behavior in real iOS environment
   - **When**: Testing iOS apps, validation gates, E2E testing
   - **Alternative**: Manual testing on device (slower, less automated)

3. **Context7 MCP**
   - **Rationale**: SwiftUI/UIKit/Foundation framework documentation
   - **Usage**: Load Apple framework patterns, API documentation
   - **When**: Implementing iOS features, learning iOS APIs
   - **Alternative**: Apple developer docs website (less integrated)

**Database Domain (≥15%)**:

1. **PostgreSQL/MongoDB/MySQL MCP** (database-specific)
   - **Rationale**: Direct database operations for specified database type
   - **Usage**: Schema design, migrations, queries, performance optimization
   - **When**: Database-heavy applications, data modeling, schema changes
   - **Alternative**: ORM abstractions (less control), manual SQL (verbose)

**DevOps Domain (≥15%)**:

1. **GitHub MCP**
   - **Rationale**: CI/CD workflow automation, version control operations
   - **Usage**: Create branches, automate commits, set up GitHub Actions, manage PRs
   - **When**: Setting up deployment pipelines, version control automation
   - **Alternative**: Manual git commands (tedious, error-prone)

2. **AWS/Azure/GCP MCP** (cloud-specific)
   - **Rationale**: Cloud infrastructure automation
   - **Usage**: Deploy services, manage infrastructure, configure cloud resources
   - **When**: Cloud deployments, infrastructure setup
   - **Alternative**: Manual cloud console operations (slow, not reproducible)

**Security Domain (≥15%)**:

1. **Context7 MCP**
   - **Rationale**: Security patterns, OAuth libraries, OWASP guidelines
   - **Usage**: Load security best practices, authentication patterns
   - **When**: Implementing authentication, security features
   - **Alternative**: Web search (less trustworthy for security)

2. **Sequential MCP**
   - **Rationale**: Systematic threat modeling and security analysis
   - **Usage**: Analyze attack vectors, assess vulnerabilities, design security architecture
   - **When**: Security architecture design, threat modeling sessions
   - **Alternative**: Ad-hoc security analysis (less systematic)

#### Tier 3: SECONDARY (Supporting, Optional)

**GitHub MCP** (if not already suggested):
- **Suggested when**: Any project (version control always valuable)
- **Usage**: Automate git workflows, PR creation, issue management
- **Priority**: Medium
- **Alternative**: Manual git commands

**Tavily/Firecrawl MCP**:
- **Suggested when**: Keywords like "research", "investigate", "explore current"
- **Usage**: Web search, content extraction, current information gathering
- **Priority**: Low-Medium
- **Alternative**: Manual web search, Claude knowledge

#### Tier 4: OPTIONAL (Keyword-Specific)

**Monitoring MCPs** (Sentry, DataDog, etc.):
- **Suggested when**: "monitoring", "observability", "error tracking" mentioned
- **Usage**: Error tracking, performance monitoring, alerting
- **Priority**: Low

**Jira/Linear MCP**:
- **Suggested when**: "project management", "issue tracking" mentioned
- **Usage**: Task management, issue tracking integration
- **Priority**: Low

---

### Example MCP Suggestion Output

**Input Specification**: "Build task management web app with React frontend (dashboard, forms, charts), Express REST API backend, PostgreSQL database, real-time updates via WebSocket, Docker deployment, integrate Stripe for payments"

**Domain Analysis**:
- Frontend: 38% (React, dashboard, forms, charts, UI)
- Backend: 28% (Express, API, real-time, WebSocket)
- Database: 18% (PostgreSQL, persistence)
- DevOps: 11% (Docker, deployment)
- Security: 5% (implied by payments, Stripe)

**Generated MCP Suggestions**:

```markdown
## Recommended MCP Servers

### Tier 1: MANDATORY 🔴

**1. Serena MCP** (CRITICAL - Always Required)
   - **Purpose**: Session persistence and zero-context-loss architecture
   - **Usage**: Save all analysis, plans, wave results, enable cross-wave context sharing
   - **When**: Throughout entire project lifecycle
   - **Commands**: write_memory, read_memory, list_memories
   - **Rationale**: Shannon requires Serena for context preservation across auto-compact events

---

### Tier 2: PRIMARY (Based on Domain Analysis)

**2. Magic MCP** (Frontend: 38%)
   - **Purpose**: React component generation from 21st.dev component library
   - **Usage**: Generate dashboard layout, form components, chart wrappers, task cards
   - **When**: Building UI components (Phase 3)
   - **Rationale**: Frontend is 38% of project, Magic accelerates React development with modern patterns
   - **Example**: Generate dashboard layout, task card component, form inputs

**3. Puppeteer MCP** (Frontend Testing)
   - **Purpose**: Functional browser testing (Shannon's NO MOCKS mandate)
   - **Usage**: Test task creation, editing, deletion, real-time updates in actual browser
   - **When**: Phase 4 (Integration Testing), validation gates
   - **Rationale**: Must test real user interactions, Shannon prohibits mocked browser tests
   - **Tests**: Create task flow, edit task flow, real-time sync between tabs

**4. Context7 MCP** (All Domains: React, Express, PostgreSQL)
   - **Purpose**: Official documentation for React, Express, PostgreSQL
   - **Usage**:
     - React: Load /facebook/react patterns for hooks, components
     - Express: Load /expressjs/express for middleware, routing
     - PostgreSQL: Load /postgres/postgres for schema design
   - **When**: Throughout implementation for framework best practices
   - **Rationale**: Ensure adherence to official patterns from authoritative sources

**5. Sequential MCP** (Backend: 28%, Complex Logic)
   - **Purpose**: Multi-step reasoning for complex backend architecture
   - **Usage**:
     - Design real-time WebSocket architecture
     - Analyze Express + WebSocket integration patterns
     - Systematic API design decisions
   - **When**: Phase 2 (Architecture Design), complex implementation decisions
   - **Rationale**: Real-time systems require systematic analysis of trade-offs

**6. PostgreSQL MCP** (Database: 18%)
   - **Purpose**: PostgreSQL schema design and operations
   - **Usage**:
     - Create tables for tasks, users, projects
     - Design indexes for query optimization
     - Implement migrations
   - **When**: Phase 2 (Schema Design), Phase 3 (Implementation)
   - **Rationale**: Direct database operations more efficient than manual SQL

---

### Tier 3: SECONDARY (Supporting Features)

**7. GitHub MCP** (Version Control - Recommended)
   - **Purpose**: Automate git workflows and version control
   - **Usage**: Create feature branches, automated commits, PR creation
   - **When**: Throughout project for version control automation
   - **Rationale**: Streamlines development workflow and reduces manual git operations

**8. Stripe MCP** (Payment Integration - Optional)
   - **Purpose**: Stripe payment gateway integration
   - **Usage**: Payment processing, subscription management
   - **When**: If payment features are implemented
   - **Rationale**: Mentioned "integrate Stripe" in specification

---

### Tier 4: OPTIONAL (If Needed Later)

**9. Tavily MCP** (External Research - If Unknown Technologies)
   - **Purpose**: Web search for current information
   - **Usage**: Research WebSocket libraries, best practices
   - **When**: If encountering unfamiliar technologies during implementation
   - **Priority**: LOW

---

## Summary
- **Total Suggested**: 7-9 MCPs (vs SuperClaude's static 6)
- **Mandatory**: 1 (Serena)
- **Primary**: 5 (Magic, Puppeteer, Context7, Sequential, PostgreSQL)
- **Secondary**: 2 (GitHub, Stripe)
- **Optional**: 1-2 (Tavily, others as needed)

## Rationale for Selection
Domains drive MCP selection: Frontend (38%) → Magic + Puppeteer, Backend (28%) → Sequential + Context7, Database (18%) → PostgreSQL MCP. Shannon's NO MOCKS principle mandates Puppeteer for real browser testing. Serena required for context preservation.
```

---

## 5-Phase Plan Generation

### Purpose

After complexity scoring and domain analysis, automatically generate structured 5-phase implementation plan with validation gates, timeline estimates, and clear deliverables.

### Phase Structure Template

Shannon uses **5 standard phases** for all projects:

1. **Analysis & Planning** - Understand requirements, create detailed plan
2. **Architecture & Design** - System design, technical specifications
3. **Implementation** - Core development work
4. **Integration & Testing** - Combine components, test functionality (NO MOCKS)
5. **Deployment & Documentation** - Deploy, document, handoff

### Phase Planning Algorithm

```
FUNCTION generate_phase_plan(complexity_score, domain_percentages, spec_text):
  phases = []

  // Adjust timeline based on complexity
  base_timeline = estimate_timeline(complexity_score)

  // Phase 1: Analysis & Planning
  phases.add({
    number: 1,
    name: "Analysis & Planning",
    duration: base_timeline × 0.15,  // 15% of total time
    objectives: [
      "Complete specification analysis",
      "Identify all requirements and constraints",
      "Create detailed task breakdown",
      "Identify risks and dependencies"
    ],
    deliverables: [
      "Detailed specification document",
      "Task list with estimates",
      "Risk assessment",
      "Resource plan"
    ],
    validation_gate: {
      criteria: [
        "All requirements clearly understood",
        "No ambiguities remaining",
        "Complexity score validated",
        "MCP servers selected and configured"
      ],
      pass_condition: "ALL criteria met"
    }
  })

  // Phase 2: Architecture & Design
  phases.add({
    number: 2,
    name: "Architecture & Design",
    duration: base_timeline × 0.20,  // 20% of total time
    objectives: generate_architecture_objectives(domain_percentages),
    deliverables: generate_architecture_deliverables(domain_percentages),
    validation_gate: {
      criteria: generate_architecture_criteria(domain_percentages),
      pass_condition: "ALL criteria met, design approved"
    }
  })

  // Phase 3: Implementation
  phases.add({
    number: 3,
    name: "Implementation",
    duration: base_timeline × 0.40,  // 40% of total time (largest phase)
    objectives: generate_implementation_objectives(domain_percentages),
    deliverables: generate_implementation_deliverables(domain_percentages),
    validation_gate: {
      criteria: [
        "All features implemented per specification",
        "Code follows established patterns",
        "Unit tests written (functional, NO MOCKS)",
        "No known critical bugs"
      ],
      pass_condition: "ALL features complete, tests passing"
    }
  })

  // Phase 4: Integration & Testing
  phases.add({
    number: 4,
    name: "Integration & Testing",
    duration: base_timeline × 0.15,  // 15% of total time
    objectives: [
      "Integrate all components",
      "Functional testing (Shannon: NO MOCKS)",
      "End-to-end testing",
      "Performance validation"
    ],
    deliverables: [
      "Integrated system",
      "Test results (functional tests, no mocks)",
      "Performance metrics",
      "Bug fixes"
    ],
    validation_gate: {
      criteria: [
        "All components integrated successfully",
        "Functional tests passing (NO MOCKS)",
        "Performance meets requirements",
        "No critical or high-priority bugs"
      ],
      pass_condition: "System fully functional, tests passing"
    },
    testing_requirements: generate_testing_requirements(domain_percentages)
  })

  // Phase 5: Deployment & Documentation
  phases.add({
    number: 5,
    name: "Deployment & Documentation",
    duration: base_timeline × 0.10,  // 10% of total time
    objectives: [
      "Deploy to target environment",
      "Create comprehensive documentation",
      "Knowledge transfer",
      "Post-deployment validation"
    ],
    deliverables: [
      "Deployed system",
      "Technical documentation",
      "User documentation",
      "Deployment runbook"
    ],
    validation_gate: {
      criteria: [
        "System deployed successfully",
        "All documentation complete",
        "Deployment validated",
        "Handoff complete"
      ],
      pass_condition: "System live, documentation complete"
    }
  })

  RETURN phases
END FUNCTION
```

### Timeline Estimation Based on Complexity

```
FUNCTION estimate_timeline(complexity_score):
  IF complexity_score < 0.30:  // Simple
    RETURN "4-8 hours"
  ELSE IF complexity_score < 0.50:  // Moderate
    RETURN "1-2 days"
  ELSE IF complexity_score < 0.70:  // Complex
    RETURN "2-4 days"
  ELSE IF complexity_score < 0.85:  // High
    RETURN "1-2 weeks"
  ELSE:  // Critical
    RETURN "2-4 weeks"
  END IF
END FUNCTION
```

### Domain-Specific Phase Customization

**Frontend-Heavy Projects** (Frontend ≥ 40%):
```
Phase 2 Architecture Additions:
  - Component hierarchy design
  - State management strategy
  - Routing architecture
  - UI/UX design system

Phase 3 Implementation Additions:
  - UI component development
  - Responsive design implementation
  - Accessibility features

Phase 4 Testing Additions:
  - Puppeteer browser testing (NO MOCKS)
  - Visual regression testing
  - Accessibility testing (WCAG compliance)
```

**Backend-Heavy Projects** (Backend ≥ 40%):
```
Phase 2 Architecture Additions:
  - API design (REST/GraphQL)
  - Database schema design
  - Authentication/authorization architecture
  - Scalability considerations

Phase 3 Implementation Additions:
  - API endpoint implementation
  - Business logic development
  - Middleware and error handling

Phase 4 Testing Additions:
  - API functional testing (real HTTP requests, NO MOCKS)
  - Database integration testing (test database, NO MOCKS)
  - Load testing
```

**Database-Heavy Projects** (Database ≥ 25%):
```
Phase 2 Architecture Additions:
  - Data modeling and normalization
  - Index strategy
  - Migration strategy
  - Backup and recovery plan

Phase 3 Implementation Additions:
  - Schema creation
  - Migration scripts
  - Query optimization

Phase 4 Testing Additions:
  - Data integrity tests (real database, NO MOCKS)
  - Query performance tests
  - Migration rollback tests
```

---

## Todo List Creation

### Purpose

Generate comprehensive, actionable todo items from specification analysis for Claude Code's TodoWrite tool integration.

### Todo Generation Algorithm

```
FUNCTION generate_todos(spec_analysis, phase_plan):
  todos = []

  // Phase 1: Analysis todos
  todos.add({
    phase: 1,
    content: "Review complete specification and identify all requirements",
    activeForm: "Reviewing specification",
    status: "pending",
    dependencies: []
  })

  todos.add({
    phase: 1,
    content: "Validate complexity score and domain analysis accuracy",
    activeForm: "Validating analysis",
    status: "pending",
    dependencies: ["Review complete specification"]
  })

  todos.add({
    phase: 1,
    content: "Configure recommended MCP servers: " + join(mcp_names, ", "),
    activeForm: "Configuring MCP servers",
    status: "pending",
    dependencies: ["Validate complexity score"]
  })

  // Generate todos for each domain
  FOR EACH domain IN domains WHERE domain.percentage >= 15%:
    domain_todos = generate_domain_todos(domain, phase_plan)
    todos.add_all(domain_todos)
  END FOR

  // Phase 4: Testing todos (Shannon mandates NO MOCKS)
  testing_todos = generate_testing_todos(domains)
  todos.add_all(testing_todos)

  // Phase 5: Deployment todos
  deployment_todos = generate_deployment_todos(spec_analysis)
  todos.add_all(deployment_todos)

  RETURN todos
END FUNCTION
```

### Domain-Specific Todo Templates

**Frontend Todos** (if Frontend ≥ 20%):
```
Phase 2:
  - "Design component hierarchy and structure"
  - "Create wireframes/mockups for key UI screens"
  - "Define state management approach (Context API, Redux, Zustand)"

Phase 3:
  - "Implement core UI components using Magic MCP where appropriate"
  - "Build responsive layouts with mobile-first approach"
  - "Implement accessibility features (ARIA labels, keyboard navigation)"
  - "Set up routing and navigation"

Phase 4:
  - "Write Puppeteer functional tests for user flows (NO MOCKS)"
  - "Test responsive design on multiple screen sizes"
  - "Validate accessibility with automated tools"
```

**Backend Todos** (if Backend ≥ 20%):
```
Phase 2:
  - "Design API endpoints and request/response contracts"
  - "Plan authentication and authorization flow"
  - "Design database integration layer"

Phase 3:
  - "Implement API routes and handlers"
  - "Set up middleware (auth, error handling, logging)"
  - "Implement business logic layer"
  - "Configure CORS and security headers"

Phase 4:
  - "Write functional API tests with real HTTP requests (NO MOCKS)"
  - "Test authentication and authorization flows"
  - "Validate error handling and edge cases"
```

**Database Todos** (if Database ≥ 15%):
```
Phase 2:
  - "Design normalized database schema"
  - "Plan index strategy for query optimization"
  - "Create migration strategy"

Phase 3:
  - "Implement schema using {DATABASE_TYPE} MCP"
  - "Write migration scripts"
  - "Set up database connection and pooling"

Phase 4:
  - "Write database integration tests on test instance (NO MOCKS)"
  - "Validate data integrity constraints"
  - "Test migration rollback procedures"
```

### Testing Todos (Shannon's NO MOCKS Philosophy)

```
FUNCTION generate_testing_todos(domains):
  testing_todos = []

  IF frontend_domain_exists:
    testing_todos.add({
      content: "Implement Puppeteer functional tests for core user flows (NO MOCKS)",
      activeForm: "Writing Puppeteer tests",
      phase: 4,
      rationale: "Shannon mandates functional testing with real browser, no mocked DOM"
    })
  END IF

  IF backend_domain_exists:
    testing_todos.add({
      content: "Write API functional tests with real HTTP requests (NO MOCKS)",
      activeForm: "Writing API functional tests",
      phase: 4,
      rationale: "Shannon mandates real HTTP requests, no request mocking"
    })
  END IF

  IF database_domain_exists:
    testing_todos.add({
      content: "Write database tests on test instance (NO MOCKS)",
      activeForm: "Writing database tests",
      phase: 4,
      rationale: "Shannon mandates real database operations on test instance"
    })
  END IF

  RETURN testing_todos
END FUNCTION
```

---

## Validation Gates

### Purpose

Define pre-execution validation checks that Claude should perform before activating specification analysis mode to ensure quality and appropriateness.

### Pre-Analysis Validation

```
FUNCTION validate_before_analysis(user_input):
  validation_results = {
    should_proceed: false,
    issues: [],
    warnings: []
  }

  // Check 1: Sufficient detail
  IF word_count(user_input) < 50:
    validation_results.issues.add("Insufficient detail for specification analysis (< 50 words)")
    validation_results.warnings.add("Consider asking user for more detail before analyzing")
  END IF

  // Check 2: Clear technical context
  IF NOT contains_technical_keywords(user_input):
    validation_results.warnings.add("No clear technical context detected")
    validation_results.warnings.add("May need clarification on implementation technology")
  END IF

  // Check 3: Actionable requirements
  IF NOT contains_actionable_verbs(user_input):
    validation_results.warnings.add("Specification lacks clear actionable requirements")
    validation_results.warnings.add("Consider asking: 'What should the system DO?'")
  END IF

  // Check 4: Shannon commands present
  IF contains_shannon_commands(user_input):
    validation_results.should_proceed = true  // Explicit Shannon command
  END IF

  // Decision logic
  IF validation_results.issues.length == 0:
    validation_results.should_proceed = true
  END IF

  RETURN validation_results
END FUNCTION
```

### Post-Analysis Validation

```
FUNCTION validate_analysis_output(analysis_results):
  validation = {
    complete: false,
    errors: [],
    quality_score: 0.0
  }

  // Validate complexity score
  IF analysis_results.complexity_score NOT IN [0.0, 1.0]:
    validation.quality_score += 0.20
  ELSE:
    validation.errors.add("Complexity score is 0.0 or 1.0, likely calculation error")
  END IF

  // Validate domain percentages sum to 100%
  domain_sum = sum(analysis_results.domain_percentages)
  IF domain_sum == 100:
    validation.quality_score += 0.20
  ELSE:
    validation.errors.add("Domain percentages sum to " + domain_sum + "%, not 100%")
  END IF

  // Validate at least 1 MCP suggested
  IF length(analysis_results.suggested_mcps) >= 1:
    validation.quality_score += 0.20
  ELSE:
    validation.errors.add("No MCP servers suggested, analysis incomplete")
  END IF

  // Validate Serena MCP present
  IF "Serena MCP" IN analysis_results.suggested_mcps:
    validation.quality_score += 0.20
  ELSE:
    validation.errors.add("Serena MCP not suggested (mandatory for Shannon)")
  END IF

  // Validate phase plan completeness
  IF length(analysis_results.phase_plan) == 5:
    validation.quality_score += 0.20
  ELSE:
    validation.errors.add("Phase plan incomplete, expected 5 phases")
  END IF

  // Set complete flag
  IF validation.errors.length == 0 AND validation.quality_score >= 0.80:
    validation.complete = true
  END IF

  RETURN validation
END FUNCTION
```

---

## Output Templates

### Complete Analysis Output Template

```markdown
# Specification Analysis Complete ✅

*Analyzed by: Shannon V3 Specification Analysis Engine*
*Analysis ID: spec_analysis_{timestamp}*
*Complexity: {score} ({interpretation})*
*Saved to Serena MCP: spec_analysis_{timestamp}*

---

## 📊 Complexity Assessment

**Overall Score**: {score} / 1.0 (**{interpretation}**)

**Dimensional Breakdown**:
| Dimension | Score | Weight | Contribution | Interpretation |
|-----------|-------|--------|--------------|----------------|
| Structural | {score} | 20% | {weighted} | {interpretation} |
| Cognitive | {score} | 15% | {weighted} | {interpretation} |
| Coordination | {score} | 15% | {weighted} | {interpretation} |
| Temporal | {score} | 10% | {weighted} | {interpretation} |
| Technical | {score} | 15% | {weighted} | {interpretation} |
| Scale | {score} | 10% | {weighted} | {interpretation} |
| Uncertainty | {score} | 10% | {weighted} | {interpretation} |
| Dependencies | {score} | 5% | {weighted} | {interpretation} |

**Complexity Interpretation**:
- **Score**: {score}
- **Category**: {Simple|Moderate|Complex|High|Critical}
- **Recommended Sub-Agents**: {count}
- **Recommended Waves**: {count}
- **Estimated Timeline**: {timeline}

---

## 🎯 Domain Analysis

{FOR EACH domain WHERE percentage > 0}
**{Domain Name} ({percentage}%)**:
- {Key characteristic 1}
- {Key characteristic 2}
- {Key characteristic 3}
{END FOR}

---

## 🔧 Recommended MCP Servers

### Tier 1: MANDATORY 🔴

**{N}. {MCP Name}** ({Priority})
   - **Purpose**: {purpose}
   - **Usage**: {usage_description}
   - **When**: {when_to_use}
   - **Rationale**: {why_suggested}
   {IF alternatives exist}
   - **Alternative**: {alternatives}
   {END IF}

### Tier 2: PRIMARY (Domain-Based)

{FOR EACH primary_mcp}
**{N}. {MCP Name}** ({Domain}: {percentage}%)
   - **Purpose**: {purpose}
   - **Usage**: {usage_description}
   - **When**: {when_to_use}
   - **Rationale**: {why_suggested}
   {IF examples exist}
   - **Example**: {example_usage}
   {END IF}
{END FOR}

### Tier 3: SECONDARY (Supporting)

{FOR EACH secondary_mcp}
**{N}. {MCP Name}** ({Context})
   - **Purpose**: {purpose}
   - **Usage**: {usage_description}
   - **Priority**: {priority_level}
{END FOR}

### Summary
- **Total Suggested**: {count} MCPs
- **Mandatory**: {count}
- **Primary**: {count}
- **Secondary**: {count}
- **Optional**: {count}

---

## 📅 5-Phase Implementation Plan

{FOR EACH phase IN phases}
### Phase {number}: {name}
**Duration**: {duration}
**Timeline**: {start_date} - {end_date}

**Objectives**:
{FOR EACH objective}
- {objective}
{END FOR}

**Deliverables**:
{FOR EACH deliverable}
- {deliverable}
{END FOR}

**Validation Gate**:
✅ Pass Criteria:
{FOR EACH criterion}
- {criterion}
{END FOR}

**Pass Condition**: {pass_condition}

---
{END FOR}

## ✅ Next Steps

1. **Confirm Analysis**: Review complexity score and domain breakdown for accuracy
2. **Configure MCPs**: Set up recommended MCP servers in Claude Code
3. **Initialize Serena**: Save this analysis to Serena MCP for context preservation
4. **Begin Phase 1**: Start with Analysis & Planning phase
5. **Create Waves**: Plan wave structure based on complexity and domains

---

## 🧠 Saved to Serena MCP

This complete analysis has been saved to Serena MCP with key: `spec_analysis_{timestamp}`

**Retrieve with**: `read_memory("spec_analysis_{timestamp}")`

**Context Available For**:
- All wave coordinators
- All implementation workers
- All testing workers
- All sub-agents throughout project lifecycle

---

*Shannon V3 - From Specification to Production Through Systematic Intelligence*
```

---

## Integration with Shannon Commands

### Command Activation Flow

When user types `/sh:analyze-spec {specification}`:

1. **Load SPEC_ANALYSIS.md**: Claude Code reads this file as behavioral instructions
2. **Activate Patterns**: All algorithms and decision trees become active behavior
3. **Execute Analysis**: Follow 8-dimensional scoring, domain identification, MCP suggestion
4. **Generate Output**: Use output templates for structured presentation
5. **Save to Serena**: Store complete analysis for cross-wave context sharing

### Integration with Other Shannon Components

**PHASE_PLANNING.md**:
- Spec analysis provides complexity score → Phase planning adjusts timeline
- Domain percentages → Phase planning adds domain-specific objectives
- MCP suggestions → Phase planning integrates MCP usage into phase gates

**WAVE_ORCHESTRATION.md**:
- Complexity score → Determines wave count (1-8 waves)
- Domain analysis → Determines wave specialization (frontend wave, backend wave)
- Sub-agent count → Based on complexity score interpretation

**MCP_DISCOVERY.md**:
- Domain analysis → Triggers MCP discovery for appropriate servers
- MCP suggestions → Detailed rationale for each server recommendation
- Tier system → Prioritizes MCP setup order

**TESTING_PHILOSOPHY.md**:
- Domain analysis → Determines testing approach per domain
- NO MOCKS mandate → Applied to all functional testing todos
- Testing todos → Generated based on domains with ≥15% presence

---

## Quality Standards

### Analysis Quality Criteria

- **Objectivity**: All scores based on measurable indicators, not subjective judgment
- **Reproducibility**: Same specification produces same scores consistently
- **Comprehensiveness**: All 8 dimensions analyzed, no dimension skipped
- **Domain Coverage**: All domains with ≥5% representation identified
- **MCP Appropriateness**: Suggested MCPs match domain needs and project scale
- **Timeline Realism**: Timeline estimates align with complexity scores
- **Context Preservation**: Complete analysis saved to Serena MCP

### Success Indicators

- ✅ Complexity score in valid range (0.0-1.0)
- ✅ Domain percentages sum to exactly 100%
- ✅ Serena MCP always in Tier 1 suggestions
- ✅ At least 1 domain-specific MCP suggested
- ✅ 5-phase plan generated with validation gates
- ✅ Testing todos enforce NO MOCKS philosophy
- ✅ Analysis ID unique and stored in Serena

---

*End of SPEC_ANALYSIS.md - Specification Analysis Behavioral Patterns*