# /shannon:spec Command - Complete Usage Guide

**Command**: `/shannon:spec`
**Purpose**: Analyze specifications using Shannon's 8-dimensional complexity framework
**Skill**: Invokes spec-analysis skill (1544 lines)
**Output**: Quantitative complexity score, domain breakdown, MCP recommendations, 5-phase plan

---

## Overview

The `/shannon:spec` command is Shannon's **entry point** for specification-driven development. It transforms subjective assessments ("this looks simple") into objective quantitative analysis using an 8-dimensional scoring framework.

**Core Value**: Prevents the #1 cause of project failures - under-estimating complexity.

**Usage**:
```bash
/shannon:spec "specification text"
/shannon:spec "specification text" --mcps
/shannon:spec "specification text" --save
/shannon:spec "specification text" --deep
```

**Flags**:
- `--mcps`: Include detailed MCP recommendations (default: true)
- `--save`: Save analysis to Serena MCP (default: true)
- `--deep`: Use Sequential MCP for deep analysis (for complexity >=0.60)

---

## The 15 Usage Examples

### Example 1: Minimal Valid Specification

**Input**:
```bash
/shannon:spec "Build a simple todo list app. Users can add tasks, mark them complete, and delete them. Store in localStorage."
```

**Output**:
```
# Specification Analysis ✅

**Complexity**: 0.22 / 1.0 (SIMPLE)
**Execution Strategy**: Sequential
**Timeline**: 4-6 hours
**Analysis ID**: spec_analysis_20251108_210001

## Complexity Breakdown
| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Structural | 0.15 | 20% | 0.030 |
| Cognitive | 0.10 | 15% | 0.015 |
| Coordination | 0.10 | 15% | 0.015 |
| Temporal | 0.10 | 10% | 0.010 |
| Technical | 0.20 | 15% | 0.030 |
| Scale | 0.10 | 10% | 0.010 |
| Uncertainty | 0.10 | 10% | 0.010 |
| Dependencies | 0.10 | 5% | 0.005 |
| **TOTAL** | **0.22** | | **SIMPLE** |

## Domain Breakdown
- Frontend (75%): Todo UI, task display, localStorage interaction
- Database (25%): localStorage persistence

## Recommended MCPs (3 total)
### Tier 1: MANDATORY
1. Serena MCP - Context preservation

### Tier 2: PRIMARY
2. Magic MCP - React component generation (Frontend 75%)

### Tier 3: SECONDARY
3. GitHub MCP - Version control

## Next Steps
1. Sequential execution (no waves needed)
2. Configure 3 MCPs
3. Begin implementation (4-6 hours)
```

**Key Learning**: Even "simple" todos get analyzed - baseline complexity is 0.22, not 0.

---

### Example 2: Simple Project (Score 0.25-0.40)

**Input**:
```bash
/shannon:spec "Build a weather dashboard that fetches data from OpenWeather API and displays current conditions, 5-day forecast, and weather alerts. React frontend with chart visualization. Deploy to Netlify."
```

**Output**:
```
**Complexity**: 0.35 / 1.0 (MODERATE)
**Timeline**: 8-12 hours (1-2 days)
**Execution Strategy**: Sequential

## Dimension Analysis
- Structural: 0.30 (multiple components: dashboard, forecast, alerts, charts)
- Technical: 0.45 (API integration, chart library, real-time updates)
- Scale: 0.15 (API rate limits consideration)

## Domain Breakdown
- Frontend (80%): React dashboard, chart.js, responsive design
- Backend (15%): API integration, data transformation
- DevOps (5%): Netlify deployment

## MCP Recommendations (5 total)
- Serena MCP (Tier 1)
- Magic MCP + Puppeteer MCP (Tier 2 - Frontend 80%)
- Context7 MCP (Tier 2 - React/Chart.js docs)
- GitHub MCP + Netlify MCP (Tier 3)

## 5-Phase Plan
Phase 1: Setup (15% - 1.5h)
Phase 2: Core Dashboard (40% - 4h)
Phase 3: Charts & Alerts (25% - 2.5h)
Phase 4: Testing (15% - 1.5h) - Puppeteer tests
Phase 5: Deploy (5% - 30min) - Netlify
```

**Key Learning**: API integration + visualization elevates complexity from 0.22 → 0.35.

---

### Example 3: Moderate Project (Score 0.40-0.60)

**Input**:
```bash
/shannon:spec "Build an inventory management system for retail stores.

Features:
- Product catalog with search and barcode scanning
- Stock level tracking with low-stock alerts
- Multi-user access (owner, manager, staff roles)
- Sales reporting dashboard with charts
- Receipt printer integration
- SQLite database for offline capability
- Sync to cloud when online
- Mobile-responsive web interface

Timeline: Deploy in 2 weeks for pilot store"
```

**Output**:
```
**Complexity**: 0.48 / 1.0 (MODERATE)
**Timeline**: 16-20 hours (2-3 days, achievable in 2 weeks)
**Execution Strategy**: Sequential (but close to wave threshold 0.50)

## Dimension Analysis
- Structural: 0.45 (9 features, ~12-15 files estimated)
- Coordination: 0.70 (multi-role system, hardware integration)
- Technical: 0.55 (offline-sync, barcode/printer hardware)
- Temporal: 0.30 (2-week deadline)

## Domain Breakdown
- Backend (30%): Offline-sync, role-based access, cloud sync
- Frontend (28%): Product catalog, dashboard, responsive UI
- Database (22%): SQLite schema, offline-first
- Hardware (15%): Barcode scanner, receipt printer
- Security (5%): Multi-user roles

## MCP Recommendations (8 total)
### Tier 1
- Serena MCP

### Tier 2
- Context7 MCP (Backend 30%, Frontend 28%)
- Magic MCP (Frontend components)
- Puppeteer MCP (Functional testing)
- SQLite MCP (Database 22%)

### Tier 3
- GitHub MCP, Sequential MCP (optional for offline-sync logic)

### Tier 4
- Tavily MCP (Research barcode scanner SDKs)

## 5-Phase Plan (2-3 days)
Phase 1: Foundation (20% - 3.5h) - SQLite schema, hardware SDK research
Phase 2: Implementation (45% - 9h) - Catalog, tracking, dashboard
Phase 3: Testing (25% - 5h) - Puppeteer tests, hardware integration tests
Phase 4: Deployment (10% - 2h) - Pilot store deployment

**Risk Assessment**:
⚠️ Hardware integration (barcode, printer) adds uncertainty
⚠️ Offline-sync complexity may require Sequential MCP analysis
```

**Key Learning**: Hardware integration + offline-sync push complexity higher than pure web apps.

---

### Example 4: Complex Project (Score 0.60-0.75)

**Input**:
```bash
/shannon:spec "Build a real-time collaborative document editor (Google Docs clone).

Frontend:
- React with TypeScript
- Rich text editing (Slate.js)
- Real-time cursor tracking
- Presence indicators
- Commenting system
- Version history viewer

Backend:
- Node.js with Express
- WebSocket server for real-time sync
- Yjs CRDT for conflict-free editing
- JWT authentication
- Document API (CRUD)

Database:
- PostgreSQL for documents, users, permissions
- Redis for session/presence
- S3 for document snapshots

Infrastructure:
- Docker containers
- Kubernetes deployment
- CI/CD with GitHub Actions

Timeline: 2 weeks"
```

**Output**:
```
**Complexity**: 0.68 / 1.0 (COMPLEX)
**Execution Strategy**: WAVE-BASED (MANDATORY)
**Expected Waves**: 3-5 waves
**Timeline**: 8-10 days (aggressive for 2 weeks)
**Analysis ID**: spec_analysis_20251108_210002

## Dimension Analysis
- Structural: 0.55 (multiple services, microservice architecture)
- Cognitive: 0.65 (CRDT algorithms, real-time architecture)
- Coordination: 0.75 (frontend, backend, devops teams)
- Temporal: 0.40 (2-week deadline)
- Technical: 0.80 (WebSocket, CRDT, real-time sync)
- Scale: 0.50 (<100ms latency requirement)
- Uncertainty: 0.15 (well-defined requirements)
- Dependencies: 0.30 (multiple integrations)

## Domain Breakdown
- Frontend (34%): React/TypeScript, Slate.js, real-time UI, cursors, presence
- Backend (30%): Express API, WebSocket, Yjs CRDT, authentication
- Database (21%): PostgreSQL, Redis, S3 snapshots
- DevOps (15%): Docker, Kubernetes, CI/CD

## Recommended MCPs (9 total)
### Tier 1: MANDATORY
1. Serena MCP

### Tier 2: PRIMARY
2. Magic MCP (Frontend 34%)
3. Puppeteer MCP (Real browser testing)
4. Context7 MCP (React/Express/PostgreSQL docs)
5. Sequential MCP (CRDT architecture - complex algorithms)
6. PostgreSQL MCP (Database 21%)
7. Redis MCP (Session management)

### Tier 3: SECONDARY
8. GitHub MCP (CI/CD)
9. AWS MCP (S3 integration)

### Tier 4: OPTIONAL
10. Tavily MCP (Research Yjs CRDT best practices)

## ⚠️ CRITICAL: Wave-Based Execution Required

**Why**: Complexity 0.68 >= 0.50 threshold MANDATES parallel execution

**Wave Structure Recommendation**:
```
Wave 1: Foundation (2h)
  - 1 agent: Architecture design, CRDT research

Wave 2: Core Implementation (6h - PARALLEL)
  - 3 agents parallel:
    * Frontend UI (React/Slate setup)
    * Backend API + WebSocket
    * Database schema (PostgreSQL + Redis)

Wave 3: Integration (4h - PARALLEL)
  - 2 agents:
    * Real-time sync integration
    * Authentication & permissions

Wave 4: Testing (3h)
  - 1 agent: Puppeteer collaborative editing tests

Total: 15h parallel vs 28h sequential = 1.9x speedup
```

## Next Steps
1. ⚠️ RUN /shannon:spec to generate detailed wave plan
2. Configure 9 recommended MCPs (prioritize Tier 1-2)
3. Use Sequential MCP for CRDT architecture decisions
4. MANDATORY: Puppeteer tests for real-time sync (NO MOCKS)
```

**Key Learning**: Real-time systems with CRDTs score 0.65-0.75 (Complex-High). Wave execution saves 13 hours.

---

### Example 5: Critical Project (Score 0.75-1.00)

**Input**:
```bash
/shannon:spec "URGENT: Build high-frequency trading system.

Requirements:
- Sub-millisecond order matching (<500μs p99)
- 1M orders/second peak load
- 99.999% uptime (5 nines)
- Real-time risk management engine
- ML price prediction (LSTM model)
- Multi-exchange aggregation (Binance, Coinbase, Kraken)
- Regulatory compliance (SEC, FINRA)
- Distributed across 5+ data centers

Technical:
- Rust backend for performance
- C++ matching engine
- Kafka event streaming (millions/sec)
- TimescaleDB time-series (billions of records)
- Redis cluster for order book
- Kubernetes with custom scheduler

Timeline: Production in 4 weeks (CRITICAL)

Unknowns:
- Market data feed integration TBD
- ML model architecture unclear
- Disaster recovery undefined
- Security audit pending legal"
```

**Output**:
```
🚨 **CRITICAL COMPLEXITY DETECTED** 🚨

**Complexity**: 0.92 / 1.0 (CRITICAL)
**Execution Strategy**: WAVE-BASED (15-25 agents REQUIRED)
**Expected Waves**: 5-8 waves
**Timeline**: 20-25 days (EXTREMELY AGGRESSIVE - 60% risk of delay)
**Analysis ID**: spec_analysis_20251108_210003

## Complexity Breakdown
| Dimension | Score | Risk Level |
|-----------|-------|------------|
| Structural | 0.90 | 🔴 CRITICAL |
| Cognitive | 0.85 | 🔴 HIGH |
| Coordination | 1.00 | 🔴 CRITICAL (5+ teams) |
| Temporal | 0.90 | 🔴 HIGH (4-week critical deadline) |
| Technical | 1.00 | 🔴 CRITICAL (HFT, sub-ms latency) |
| Scale | 1.00 | 🔴 CRITICAL (1M orders/sec, 99.999% uptime) |
| Uncertainty | 0.80 | 🔴 HIGH (multiple TBDs) |
| Dependencies | 0.75 | 🔴 HIGH (vendor approvals, audits) |

## Domain Breakdown
- Backend (38%): Rust/C++ HFT engine, Kafka streaming
- Database (21%): TimescaleDB billions, Redis cluster
- DevOps (17%): 5+ data centers, Kubernetes
- ML (13%): LSTM models, price prediction
- Security (11%): SEC/FINRA compliance, auditing

## Recommended MCPs (13 total)
### Tier 1: MANDATORY
1. Serena MCP - CRITICAL for 5-8 wave context preservation

### Tier 2: PRIMARY (8 MCPs)
2. Context7 MCP (Rust/Kafka/TimescaleDB docs)
3. Sequential MCP (200-500 step HFT architecture analysis - CRITICAL)
4. PostgreSQL MCP (TimescaleDB operations)
5. Redis MCP (Cluster management)
6. Kubernetes MCP (Custom scheduler optimization)
7. AWS/GCP MCP (Multi-region deployment)
8. GitHub MCP (CI/CD high-velocity)
9. ML Framework MCP (LSTM development)

### Tier 3: SECONDARY (4 MCPs)
10. Tavily MCP (Research HFT patterns, ML architectures)
11-13. Exchange API MCPs (Binance, Coinbase, Kraken)

## 🚨 RISK ASSESSMENT 🚨

**CRITICAL RISKS**:
1. **Timeline Risk**: 0.92 complexity + 4-week deadline = 60% probability of delay
   - Recommendation: Extend to 6-8 weeks (50% buffer)

2. **Dependency Risk**: Blocked by vendor approvals (1 week) + security audit (2 weeks)
   - Action: Start vendor approvals IMMEDIATELY (parallel to development)

3. **Uncertainty Risk**: ML model TBD, disaster recovery undefined
   - Action: Dedicate 1-2 agents to research in Phase 1

4. **Technical Risk**: Sub-millisecond latency with distributed system
   - Mitigation: Use Sequential MCP for ALL critical architecture decisions

5. **Coordination Risk**: 5+ teams (Backend, ML, DevOps, Security, Legal)
   - Protocol: Daily SITREP coordination meetings MANDATORY

## Wave Execution Plan (MANDATORY)
```
Wave 1: Deep Analysis & Risk Assessment (3 days)
  - 3 agents: HFT architect, ML researcher, Security planner

Wave 2: Foundation Implementation (4 days - PARALLEL)
  - 5 agents: C++ matching engine, Rust backend, TimescaleDB setup, Redis cluster, ML pipeline

Wave 3: Integration Layer (3 days - PARALLEL)
  - 4 agents: Kafka streaming, Exchange APIs, Risk engine, Monitoring

Wave 4: Testing & Optimization (3 days - PARALLEL)
  - 3 agents: Load testing (1M orders/sec), Latency optimization (<500μs), Security testing

Wave 5: Deployment & Compliance (2 days)
  - 2 agents: Multi-region deployment, Compliance documentation

Total: 15 days minimum (vs 4 weeks requested)
Speedup: 3.5x vs sequential (15 days vs 52 days)
Risk: Still aggressive - recommend 20-25 day timeline
```

## IMMEDIATE ACTIONS REQUIRED
1. 🚨 Escalate timeline risk to stakeholders
2. Configure ALL 13 MCPs (no optional - all needed for CRITICAL)
3. Begin vendor approvals NOW (don't wait for development)
4. Use Sequential MCP for Phase 1 analysis (200-500 reasoning steps)
5. Establish daily SITREP protocol
```

**Key Learning**: CRITICAL projects (0.85-1.00) require:
- 15-25 agents
- 5-8 waves
- Sequential MCP for architecture decisions
- Daily SITREP coordination
- Realistic timeline assessment (4 weeks insufficient for 0.92)

---

### Example 6: Frontend-Heavy Specification

**Input**:
```bash
/shannon:spec "Build a social media dashboard for influencers.

Features:
- Multi-account management (Instagram, Twitter, TikTok, YouTube)
- Unified content calendar with drag-and-drop scheduling
- Analytics dashboard with engagement metrics
- Post composer with media upload and preview
- Comment/DM inbox aggregation
- Hashtag trend analyzer
- Follower growth charts
- Automated posting schedules
- Mobile-responsive design
- Dark mode support

Tech: React/Next.js, Tailwind CSS
Backend: Minimal - mostly API integrations
Storage: Firebase for user data"
```

**Output**:
```
**Complexity**: 0.52 / 1.0 (COMPLEX)
**Timeline**: 3-4 days
**Execution Strategy**: WAVE-BASED (Frontend-heavy triggers threshold)

## Domain Breakdown
- Frontend (70%): React/Next.js, drag-drop, calendar, charts, 4 social integrations
- Backend (20%): API integrations, Firebase, scheduled posts
- Database (10%): Firebase schema

## Dimension Analysis
- Structural: 0.50 (10 features, complex UI)
- Coordination: 0.60 (social API integration coordination)
- Technical: 0.60 (4 social APIs, automated scheduling, real-time updates)

## MCP Recommendations
### Tier 2: PRIMARY (Frontend >=20%)
- Magic MCP - Component generation (70% Frontend)
- Puppeteer MCP - Real browser testing (MANDATORY for 70%)
- Context7 MCP - React/Next.js/Tailwind docs

### Tier 3
- GitHub MCP, Firebase MCP

### Tier 4
- Tavily MCP (Research social API limitations)

## Phase Plan with Frontend Emphasis
Phase 1: Setup & API Research (15% - 3h)
Phase 2: Core UI Components (45% - 9h) ← Frontend emphasis
Phase 3: Integrations (20% - 4h)
Phase 4: Testing (15% - 3h) ← Puppeteer heavy
Phase 5: Deploy (5% - 1h)

## Frontend-Specific Recommendations
1. Use Magic MCP for rapid component scaffolding
2. Puppeteer tests CRITICAL (70% Frontend requires extensive E2E)
3. Test all 4 social integrations with REAL APIs (no mocks)
4. Mobile-responsive testing (Puppeteer viewport simulation)
```

**Key Learning**: Frontend-heavy (>50%) adjusts:
- Phase 2 gets +5% (UI work time-consuming)
- Phase 4 gets +5% (E2E tests critical)
- Phase 5 gets -10% (static hosting simpler)

---

### Example 7: Backend-Heavy Specification

**Input**:
```bash
/shannon:spec "Build a multi-tenant SaaS billing platform.

Backend:
- Stripe subscription management
- Invoice generation and PDF export
- Usage metering and tiered pricing
- Tax calculation (TaxJar API)
- Dunning management (failed payments)
- Webhook handling for Stripe events
- Admin API with complex permissions
- Audit logging for compliance
- Data export (GDPR compliance)

Frontend:
- Simple billing portal (view invoices, update payment method)
- Admin dashboard (minimal - mostly reports)

Database:
- PostgreSQL for subscriptions, invoices, usage data
- Complex schema with multi-tenancy isolation
- Time-series usage metrics

Architecture:
- Multi-tenant with row-level security
- Scalable to 10K customers
- Event-driven via webhooks"
```

**Output**:
```
**Complexity**: 0.72 / 1.0 (HIGH)
**Timeline**: 6-8 days
**Execution Strategy**: WAVE-BASED (3-5 waves, 8-12 agents)

## Domain Breakdown
- Backend (55%): Stripe, billing logic, webhooks, permissions, APIs
- Database (25%): PostgreSQL, multi-tenancy, time-series
- Frontend (15%): Billing portal, admin dashboard
- Security (5%): GDPR, audit logging

## Dimension Analysis
- Technical: 0.85 (Stripe webhooks, tax calculation, multi-tenancy, GDPR)
- Coordination: 0.80 (backend team, compliance team, payment integration)
- Scale: 0.60 (10K customers, complex pricing)
- Dependencies: 0.40 (Stripe, TaxJar external dependencies)

## MCP Recommendations (10 total)
### Tier 1
- Serena MCP

### Tier 2: PRIMARY
- Context7 MCP (Express/Node.js/PostgreSQL docs)
- Sequential MCP (Multi-tenancy architecture CRITICAL)
- PostgreSQL MCP (Database 25%, multi-tenant schema)
- Stripe MCP (Primary integration)
- Puppeteer MCP (Testing billing flows)

### Tier 3
- GitHub MCP, AWS MCP, TaxJar API integration

## Backend-Specific Phase Plan
Phase 1: Foundation (25% - 12h) ← Backend emphasis
  - Multi-tenant architecture design
  - Database schema with RLS
  - Stripe webhook infrastructure

Phase 2: Core Implementation (30% - 14h)
  - Subscription management
  - Invoice generation
  - Usage metering

Phase 3: Integration (20% - 10h)
  - Stripe event handling
  - Tax calculation
  - Dunning logic

Phase 4: Testing (20% - 10h) ← API testing heavy
  - Real Stripe test mode (NO MOCKS)
  - Multi-tenant isolation tests
  - GDPR compliance validation

Phase 5: Deployment (5% - 2h)

## Critical Recommendations
1. ⚠️ USE SEQUENTIAL MCP for multi-tenant architecture (high risk of errors)
2. ⚠️ Test with REAL Stripe test mode (Stripe provides test API)
3. ⚠️ Multi-tenancy testing CRITICAL (data isolation bugs catastrophic)
4. ⚠️ GDPR compliance review BEFORE production
```

**Key Learning**: Backend-heavy (>50%) adjusts Phase 1 up, requires Sequential MCP for complex architecture.

---

### Example 8: Full-Stack Balanced

**Input**:
```bash
/shannon:spec "Build a customer support ticketing system.

Frontend:
- React dashboard for support agents
- Ticket list with filtering (status, priority, assignee)
- Ticket detail view with rich text editor for responses
- Real-time updates when tickets change

Backend:
- Express API with TypeScript
- Authentication for agents and admins
- REST endpoints for tickets (CRUD)
- WebSocket for real-time updates
- Email integration (SendGrid)

Database:
- PostgreSQL for tickets, users, responses
- Full-text search on ticket content

Deploy: Docker to AWS
Timeline: 1 week"
```

**Output**:
```
**Complexity**: 0.58 / 1.0 (COMPLEX)
**Timeline**: 2-3 days (achievable in 1 week)
**Execution Strategy**: WAVE-BASED (balanced domains trigger waves)

## Domain Breakdown (Balanced)
- Backend (41%): Express API, auth, WebSocket, SendGrid
- Frontend (33%): React dashboard, filtering, rich text editor
- Database (26%): PostgreSQL schema, full-text search

**Observation**: Near-equal distribution indicates full-stack project

## MCP Recommendations (8 total)
- Context7 MCP (Backend 41%, Frontend 33%, Database 26% - all PRIMARY)
- Magic MCP (Frontend 33%)
- Puppeteer MCP (Frontend testing)
- PostgreSQL MCP (Database 26%)

## Balanced Wave Structure
Wave 1: Architecture (2h)
Wave 2: Database + Frontend (parallel - 3h)
Wave 3: Backend API (depends on DB - 4h)
Wave 4: Integration Testing (2h)

Total: 11h (vs 16h sequential = 1.45x speedup)
```

**Key Learning**: Balanced domains (no single domain >50%) still benefit from waves if complexity >=0.50.

---

### Example 9: Mobile App Specification

**Input**:
```bash
/shannon:spec "Build a fitness tracking mobile app.

Features:
- Native iOS and Android apps
- Workout logging with exercise library
- GPS route tracking for runs/cycles
- Integration with Apple Health and Google Fit
- Social features (share workouts, follow friends)
- Progress charts and statistics
- Push notifications for reminders
- Offline mode with cloud sync

Backend:
- Node.js API for workout data
- User authentication
- Social features backend
- Cloud sync service

Database:
- PostgreSQL for users, workouts, social data
- S3 for GPS route data (JSON)

Timeline: 6 weeks for MVP"
```

**Output**:
```
**Complexity**: 0.65 / 1.0 (COMPLEX)
**Timeline**: 4-5 days (achievable in 6 weeks)
**Execution Strategy**: WAVE-BASED

## Domain Breakdown
- Mobile (45%): iOS app, Android app, Health/Fit integrations, GPS tracking
- Backend (30%): Node.js API, auth, social backend, sync
- Database (20%): PostgreSQL, S3 for GPS data
- Frontend (5%): Minimal web portal

## MCP Recommendations (9 total)
### Tier 2: PRIMARY
- iOS Simulator MCP (Mobile 45% - CRITICAL)
- Context7 MCP (Swift/React Native/Node.js docs)
- Puppeteer MCP (Web portal testing)
- PostgreSQL MCP (Database 20%)

### Tier 3
- GitHub MCP, AWS MCP (S3)

### Tier 4
- Tavily MCP (Research Apple Health / Google Fit APIs)

## Mobile-Specific Considerations
⚠️ **Mobile Development Requires**:
1. iOS Simulator MCP for automated testing (NO MOCKS)
2. Separate builds for iOS and Android (2x implementation time)
3. App store submission process (Phase 5 extended)
4. Health/Fit API integration testing with REAL devices

## Wave Structure for Mobile
Wave 1: Backend + Database (parallel - 3h)
Wave 2: iOS Implementation (4h) - Can start if API contracts defined
Wave 3: Android Implementation (4h) - Parallel to Wave 2 if resources allow
Wave 4: Health/Fit Integration (2h)
Wave 5: Testing (3h) - iOS Simulator + Android emulator

Total: 16h (vs 24h sequential = 1.5x speedup)
```

**Key Learning**: Mobile apps (>=40%) trigger iOS Simulator MCP recommendations, require platform-specific testing.

---

### Example 10: With Attached Specification File

**Input**:
```bash
/shannon:spec "See attached specification document for requirements" @project_spec.pdf
```

**Output**:
```
🚨 **PDF Processing Required**

**Action**: Reading specification from project_spec.pdf...

**Document Analysis**:
- Pages: 15
- Word count: ~4,200 words
- Sections: Requirements (5 pages), Architecture (3 pages), Timeline (2 pages)
- Detected features: 28 distinct features
- Complexity indicators: Multiple "critical", "must", "regulatory" keywords

**Parsing** (using deep mode for large spec):
[Spec-analysis processes PDF content...]

**Complexity**: 0.78 / 1.0 (HIGH)
**Reason**: Large specification (4200 words) + regulatory keywords + 28 features

[Full analysis output...]

**Special Handling**:
- Large spec (>2000 words) → Auto-enabled --deep flag
- PDF parsing may take 30-60s (extracting text, analyzing structure)
- Sequential MCP recommended for 0.78 complexity
```

**Key Learning**: Attached files auto-processed, large specs (>2000 words) trigger deep analysis mode.

---

### Example 11: --mcps Flag Usage

**Input**:
```bash
/shannon:spec "Build REST API for blog platform with Express and MongoDB" --mcps
```

**Output**:
```
**Complexity**: 0.42 / 1.0 (MODERATE)

[Standard analysis output...]

## DETAILED MCP RECOMMENDATIONS (--mcps flag active)

### Tier 1: MANDATORY
**Serena MCP**
- **Purpose**: Context preservation across sessions, wave coordination
- **Setup**:
  ```bash
  # Install Serena MCP
  npm install -g @serena/mcp-server
  # Configure in Claude Code settings
  ```
- **Health Check**: `/list_memories` → Should return memory list
- **Fallback**: NONE (Serena is mandatory for Shannon)
- **Degradation if missing**: CRITICAL - Cannot save analysis, cannot coordinate waves

### Tier 2: PRIMARY
**Context7 MCP** (Backend 60%)
- **Purpose**: Express framework documentation, MongoDB patterns
- **Triggers**: Backend domain >=20% (currently 60%)
- **Usage**: Auto-loaded when Express/MongoDB detected in code
- **Setup**:
  ```bash
  # Context7 MCP installation
  /plugin install context7
  ```
- **Health Check**: Query Express docs to verify
- **Fallback**: Manual documentation lookup (slower)
- **Degradation**: MEDIUM - Can continue but slower lookup

**MongoDB MCP** (Database 30%)
- **Purpose**: Schema operations, query optimization
- **Triggers**: MongoDB mentioned + Database >=15%
- **Setup**: Configure MongoDB connection string
- **Health Check**: Test connection with sample query
- **Fallback**: Manual MongoDB CLI
- **Degradation**: LOW - MongoDB CLI adequate

**Puppeteer MCP** (Testing requirement)
- **Purpose**: Functional API testing with real HTTP
- **Why needed**: Shannon NO MOCKS philosophy
- **Setup**: Puppeteer auto-installed with MCP
- **Health Check**: `/browser_navigate` → Browser should launch
- **Fallback**: Manual Postman testing
- **Degradation**: HIGH - Manual testing error-prone and slow

### Tier 3: SECONDARY
**GitHub MCP**
- **Purpose**: CI/CD automation, version control
- **Setup**: Connect GitHub account
- **Health Check**: `/github_get_repo` → Repo info returned
- **Fallback**: Manual git commands
- **Degradation**: LOW - Git CLI adequate

## MCP Installation Priority
1. Serena (MANDATORY - install FIRST)
2. Context7 (HIGH - significant productivity boost)
3. Puppeteer (HIGH - required for NO MOCKS compliance)
4. MongoDB (MEDIUM - nice to have)
5. GitHub (LOW - manual git works)

## Setup Verification Script
```bash
# Run all health checks
/shannon:check_mcps

# Expected output:
# ✅ Serena MCP: Connected
# ✅ Context7 MCP: Available
# ✅ Puppeteer MCP: Configured
# ⚠️ MongoDB MCP: Not configured (optional)
# ✅ GitHub MCP: Connected
```
```

**Key Learning**: --mcps flag provides extensive setup guidance, health checks, fallback chains, degradation analysis.

---

### Example 12: --save Flag Usage

**Input**:
```bash
/shannon:spec "Build inventory system" --save
```

**Process**:
```
1. Run 8D analysis
   → Complexity: 0.48

2. Calculate domain percentages
   → Backend 35%, Frontend 30%, Database 25%, Hardware 10%

3. Generate MCP recommendations
   → 6 MCPs recommended

4. Create 5-phase plan
   → 16 hours total

5. **SAVE TO SERENA** (--save flag active):
   write_memory("spec_analysis_inventory_20251108", {
     complexity_score: 0.48,
     domains: {...},
     mcps: [...],
     phase_plan: {...},
     created_at: "2025-11-08T21:15:00Z"
   })

6. **VERIFY SAVE**:
   verify = read_memory("spec_analysis_inventory_20251108")
   if (!verify) ERROR: "Serena save failed"

7. **CONFIRM TO USER**:
   "✅ Analysis saved to Serena MCP
    Restore with: /shannon:restore spec_analysis_inventory_20251108
    OR: Auto-restored via /shannon:prime in future sessions"
```

**Output Includes**:
```
## Analysis Saved ✅

**Serena Key**: spec_analysis_inventory_20251108
**Restore Command**: `/shannon:restore spec_analysis_inventory_20251108`
**Auto-Restore**: /shannon:prime (future sessions)

**Saved Data**:
- Complexity score: 0.48
- Domain breakdown
- MCP recommendations
- Complete 5-phase plan
- Timeline: 16 hours
```

**Key Learning**: --save ensures analysis persists across sessions (default true, explicit for clarity).

---

### Example 13: --deep Flag (Complex Analysis)

**Input**:
```bash
/shannon:spec "Build distributed microservices platform with service mesh, observability, and multi-cloud deployment" --deep
```

**Process**:
```
1. Detect complexity indicators: "distributed", "microservices", "service mesh", "multi-cloud"
   → Preliminary estimate: 0.75-0.85 (HIGH)

2. --deep flag triggers EXTENDED ANALYSIS:
   → Load Sequential MCP for deep reasoning
   → 200-500 reasoning steps for architecture analysis
   → Time: 5-10 minutes (vs 2-3 minutes standard)

3. Sequential MCP analyzes:
   thought #1: "Distributed systems have hidden coordination complexity..."
   thought #50: "Service mesh adds operational overhead..."
   thought #150: "Multi-cloud increases deployment complexity..."
   thought #287: "Final complexity assessment considering all factors..."

4. Deep analysis complete:
   → Complexity: 0.82 / 1.0 (HIGH)
   → 8D scores refined through systematic reasoning
   → Architecture recommendations included
```

**Output**:
```
**Complexity**: 0.82 / 1.0 (HIGH - Deep Analysis)
**Analysis Mode**: DEEP (Sequential MCP - 287 reasoning steps)
**Timeline**: 10-15 days

## Deep Analysis Insights

**Structural Complexity** (0.85):
- Not just file count, but service interdependencies
- Service mesh adds N² complexity (every service can call every other)
- Multi-cloud deployment triples infrastructure complexity

**Technical Complexity** (0.95):
- Service mesh (Istio/Linkerd) is advanced technology
- Observability stack (Prometheus, Grafana, Jaeger) adds operational burden
- Multi-cloud (AWS + Azure + GCP) requires provider-specific expertise

**Coordination Complexity** (0.90):
- Microservices = multiple teams (frontend services, backend services, platform team)
- Service mesh = dedicated SRE team needed
- Multi-cloud = cloud architecture team required

[Full analysis with Sequential MCP insights...]

## Wave Execution (8-15 agents, 5-7 waves)

Wave 1: Architecture & Service Mesh Design (2 days, Sequential MCP CRITICAL)
Wave 2: Core Services Implementation (3 days, 5 agents parallel)
Wave 3: Service Mesh Integration (2 days, 3 agents)
Wave 4: Observability Stack (2 days, 2 agents)
Wave 5: Multi-Cloud Deployment (2 days, 3 agents)

Total: 11 days parallel vs 35 days sequential = 3.2x speedup
```

**Key Learning**: --deep flag uses Sequential MCP for 200-500 step analysis, reveals hidden complexity in distributed systems.

---

### Example 14: Minimal Specification (Edge Case)

**Input**:
```bash
/shannon:spec "Change button color to blue"
```

**Output**:
```
⚠️ **SPECIFICATION TOO SMALL**

**Reason**: Specification has only 5 words (minimum 20 words for reliable analysis)

**Detected Intent**: UI modification (not full project specification)

**Recommendation**:
This appears to be a task, not a specification. For tasks:
- Just implement directly (no /shannon:spec needed)
- Use: "Change button color to blue in src/components/Button.tsx"

**When to Use /shannon:spec**:
- Projects with 5+ features
- Specifications with 3+ paragraphs
- Multi-component systems
- Anything requiring >4 hours of work

**If this IS a full spec**:
- Expand with details: "Change button color to blue [WHERE? WHICH button? What shade of blue? Any accessibility requirements?]"
- Minimum 50 words recommended for accurate 8D analysis
```

**Key Learning**: /shannon:spec validates input, rejects specs <20 words, guides users to proper command.

---

### Example 15: Conflicting Timeline Constraint

**Input**:
```bash
/shannon:spec "Build enterprise resource planning (ERP) system with:
- Inventory management
- Order processing
- Customer relationship management
- Financial accounting
- HR management
- Supply chain tracking
- Reporting and analytics
- Multi-tenancy for 100+ companies
- Mobile apps for field workers
- Integration with 10+ third-party systems

Timeline: Launch complete system in 3 weeks"
```

**Output**:
```
🚨 **CRITICAL TIMELINE CONFLICT DETECTED** 🚨

**Complexity**: 0.89 / 1.0 (CRITICAL)
**Calculated Timeline**: 25-30 days (4-6 weeks MINIMUM)
**User Requested**: 3 weeks (21 days)

## Timeline Feasibility Assessment

**Calculated Effort**:
- 15-20 agents required
- 6-8 waves
- 25-30 days minimum (3.5x speedup already applied)

**User Constraint**: 3 weeks = 21 days

**GAP**: 4-9 days SHORT (16-30% timeline deficiency)

## 🚨 RECOMMENDATIONS 🚨

**Option 1: Extend Timeline** (RECOMMENDED)
- Request: 6-week timeline (42 days)
- Provides: 12-17 day buffer (acceptable for CRITICAL)
- Risk: MEDIUM (manageable with buffer)

**Option 2: Reduce Scope**
- Phase 1 MVP: Core 4 modules (Inventory, Orders, CRM, Finance)
- Phase 2: Remaining (HR, Supply Chain, Mobile, Analytics)
- Timeline: 3 weeks for MVP, 3 weeks for Phase 2
- Risk: MEDIUM (two-phase delivery)

**Option 3: Accept HIGH RISK** (NOT RECOMMENDED)
- Proceed with 3-week timeline
- Risk: 70% probability of missing deadline
- Mitigation: Daily SITREP, 20+ agents, aggressive parallelization
- Consequences: Quality compromises likely, technical debt accumulation

## Detailed Rationale

**Why 3 weeks insufficient**:
```
Dimension Analysis:
- Structural: 0.90 (10 major modules, 100+ files estimated)
- Coordination: 1.00 (ERP requires Finance, HR, Supply Chain, IT teams)
- Technical: 0.95 (Multi-tenancy, 10+ integrations, mobile)
- Scale: 0.85 (100+ company tenants, enterprise performance)
- Uncertainty: 0.80 (10+ third-party API integrations undefined)

Timeline Formula:
  Base = 0.89 * 35 days = 31 days
  Speedup = 3.5x parallel execution = 31 / 3.5 = 9 days saved
  Minimum = 31 - 9 = 22 days (optimistic)
  Realistic = 25-30 days (with buffer)
```

**User Choice Required**:
- [ ] Option 1: Extend timeline to 6 weeks
- [ ] Option 2: Deliver MVP in 3 weeks, full system in 6 weeks
- [ ] Option 3: Accept 70% delay risk, proceed with 3 weeks

**Shannon will not proceed until timeline conflict resolved.**
```

**Key Learning**: /shannon:spec detects timeline conflicts, forces explicit risk acknowledgment before proceeding.

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Specification Too Vague

**Symptom**:
```bash
/shannon:spec "Build a good app"
```

**Why It Fails**:
- "good" is subjective (unmeasurable)
- No features specified (cannot calculate structural complexity)
- No technical details (cannot assess technical dimension)
- No timeline (cannot assess temporal dimension)

**Shannon Response**:
```
⚠️ **SPECIFICATION TOO VAGUE**

**Missing Information**:
- Features: What does the app DO?
- Technologies: What stack? (React, Vue, Python, etc.)
- Users: Who uses it? How many?
- Timeline: When needed?
- Scale: Expected load?

**Minimum Viable Specification**:
- 3+ distinct features
- 50+ words
- Mention of tech stack OR platform
- Basic timeline indicator

**Example Improvement**:
/shannon:spec "Build a task management app (React frontend, Node.js backend, PostgreSQL database) with:
- User authentication
- Task creation and editing
- Task assignment to team members
- Due date tracking
- Priority levels
Timeline: 2 weeks"
```

**Recommendation**: Add features, tech stack, timeline → Re-run /shannon:spec

---

### ❌ Anti-Pattern 2: Too Short (<50 words)

**Symptom**:
```bash
/shannon:spec "React app with login"
```

**Why It Fails**:
- Insufficient context for domain detection (Frontend? Backend? Database?)
- Cannot assess coordination complexity (1 feature)
- Uncertainty high (90% of requirements missing)

**Shannon Response**:
```
⚠️ **SPECIFICATION TOO SHORT** (4 words, minimum 50 recommended)

**What's Missing**:
- What happens after login? (Dashboard, profile, content?)
- Backend? (How is auth handled? JWT, sessions?)
- Database? (Where are users stored?)
- Complete user workflows

**Expand Specification**:
- Describe 5-10 features (not just login)
- Include backend/database requirements
- Mention deployment and timeline

**Current Analysis** (LIMITED ACCURACY):
Complexity: ~0.30 (guess based on minimal info)
Note: This score has LOW CONFIDENCE due to vague specification
```

**Recommendation**: Expand to 100+ words with complete feature list → Re-run /shannon:spec

---

### ❌ Anti-Pattern 3: Accepting User's Subjective Score

**Symptom**:
```bash
User: "I think this is 40/100 complexity"
Agent: "Your 40/100 assessment seems reasonable..."
```

**Why It Fails**:
- User intuition biased 30-50% low
- No systematic 8-dimensional analysis
- Anchoring bias (agent accepts user number)

**Shannon Counter** (from using-shannon skill):
```
⚠️ STOP. User provided estimate - this triggers MANDATORY algorithm.

**User's Assessment**: 40/100 (subjective)
**Action**: Running objective 8D analysis...

[Runs /shannon:spec...]

**Algorithm Result**: 0.58 / 1.0 = 58/100 (quantitative)

**Comparison**:
- User estimated: 40/100 (18-point underestimation)
- Algorithm calculated: 58/100
- Difference: 45% underestimation

**Why Different**:
- User missed: Coordination complexity (3 teams)
- User missed: Technical complexity (real-time sync)
- User missed: Integration complexity (4 third-party APIs)

**Proceeding with**: 0.58 (algorithm's objective score)
```

**Recommendation**: ALWAYS run /shannon:spec when user provides estimate. Compare results, explain differences.

---

### ❌ Anti-Pattern 4: Skipping Analysis for "Simple" Projects

**Symptom**:
```bash
User: "This is straightforward CRUD, no need for analysis"
Agent: "You're right, let's start implementing..."
```

**Why It Fails**:
- "Straightforward CRUD" often scores 0.40-0.55 (Moderate-Complex)
- Missing: Auth (0.15 complexity), deployment (0.10), testing (0.10), error handling (0.10)
- Real complexity: 0.40-0.55, not 0.15-0.25

**Shannon Counter** (using-shannon anti-rationalization):
```
⚠️ STOP. "Straightforward" is subjective, not quantitative.

**Required Action**:
1. Run /shannon:spec anyway (takes 30 seconds)
2. Let algorithm decide if actually simple

**Running Analysis...**

**Result**: 0.52 / 1.0 (COMPLEX)

**Surprise**:
- User thought: "Straightforward" → 0.20
- Algorithm found: COMPLEX → 0.52
- Difference: 2.6x underestimation

**Hidden Complexity**:
- CRUD = Create (form validation), Read (search, filtering), Update (versioning?), Delete (soft delete?)
- Auth adds 0.15
- Testing adds 0.10
- Deployment adds 0.10
- Error handling adds 0.10

**Correct Approach**:
- Use wave-based execution (complexity 0.52 >= 0.50)
- 3-5 agents
- 2-3 days (not "few hours")
```

**Recommendation**: using-shannon skill blocks "straightforward" rationalization. Run /shannon:spec regardless of subjective assessment.

---

### ❌ Anti-Pattern 5: Missing Domain Information

**Symptom**:
```bash
/shannon:spec "Build a platform for X" [no mention of tech stack, frontend, backend, database]
```

**Why It Fails**:
- Cannot calculate domain percentages without tech indicators
- MCP recommendations will be generic
- Phase plan won't be domain-customized

**Shannon Response**:
```
⚠️ **DOMAIN INFORMATION MISSING**

**Current Specification**: "Build a platform for X"

**Missing**:
- Frontend technology? (React, Vue, Angular, mobile?)
- Backend technology? (Node.js, Python, Java?)
- Database? (PostgreSQL, MongoDB, MySQL?)
- Infrastructure? (AWS, Azure, Docker, Kubernetes?)

**Impact of Missing Info**:
- Domain detection will be UNCERTAIN
- MCP recommendations will be GENERIC (cannot suggest React vs Vue MCPs)
- Phase plan will lack domain-specific guidance

**Better Specification**:
/shannon:spec "Build a platform for X with:
- React frontend with TypeScript
- Express backend with Node.js
- PostgreSQL database
- Docker deployment to AWS
[...features...]"

**Proceeding Anyway** (with LOW CONFIDENCE warning):
```

**Recommendation**: Include tech stack in specification for accurate domain detection.

---

## Integration with Other Commands

### /shannon:spec → /shannon:spec Integration

**Workflow**:
```bash
# Step 1: Analyze specification
/shannon:spec "Build e-commerce platform..."

# Output includes:
# Complexity: 0.68 (COMPLEX)
# Execution Strategy: WAVE-BASED

# Step 2: Generate wave structure
/shannon:spec

# This reads spec_analysis from Serena
# Generates wave structure based on complexity 0.68
```

**Data Flow**:
```
/shannon:spec
  ↓
spec-analysis skill calculates complexity
  ↓
Saves to Serena: write_memory("spec_analysis_ID", {...})
  ↓
/shannon:spec
  ↓
wave-orchestration skill reads: read_memory("spec_analysis_ID")
  ↓
Uses complexity score to allocate agents (0.68 → 8-12 agents)
```

**Key**: /shannon:spec must run BEFORE /shannon:spec (waves need complexity score).

---

### /shannon:spec → /shannon:check_mcps Integration

**Workflow**:
```bash
# Step 1: Get MCP recommendations
/shannon:spec "Build React + Express app..."

# Output includes:
# Recommended MCPs:
# - Serena (Tier 1)
# - Magic, Puppeteer, Context7 (Tier 2)

# Step 2: Verify MCPs configured
/shannon:check_mcps

# This cross-references recommendations with installed MCPs
# Shows: Installed vs Missing
```

**Data Flow**:
```
/shannon:spec → MCP recommendations generated
  ↓
/shannon:check_mcps reads spec_analysis
  ↓
Compares recommended vs installed
  ↓
Generates setup guide for missing PRIMARY/MANDATORY MCPs
```

---

### /shannon:spec → /shannon:spec Integration

**Workflow**:
```bash
# Scenario: User has existing codebase, wants complexity assessment

# Step 1: Analyze codebase (not specification)
/shannon:spec

# shannon-analysis skill:
# - Scans codebase (file counts, domain detection from file types)
# - Generates complexity estimate

# Step 2: User provides specification for comparison
/shannon:spec "Original specification was..."

# Step 3: Compare
# Codebase analysis: 0.55 (what was built)
# Spec analysis: 0.42 (what was planned)
# Difference: Scope creep of +0.13 (31% complexity increase)
```

**Use Case**: Detect scope creep by comparing codebase complexity vs original spec complexity.

---

## Recommended Workflows

### Workflow 1: New Project

```bash
# Step 1: Prime session
/shannon:prime

# Step 2: Analyze specification
/shannon:spec "[your specification]"

# Step 3: Review output, install MCPs
# Based on recommendations

# Step 4: Execute
If complexity < 0.50:
  → Just start implementing (sequential)
Else:
  → /shannon:spec (parallel execution)

# Step 5: Checkpoint progress
/shannon:spec "Phase 2 complete"
```

---

### Workflow 2: Resume Existing Project

```bash
# Step 1: Restore context
/shannon:prime --resume

# Step 2: Check if spec analysis exists
/shannon:spec

# If spec analysis NOT in memory:
/shannon:spec "[reconstruct specification from memory/docs]"

# If spec analysis EXISTS:
# Continue from where you left off
```

---

### Workflow 3: Specification Refinement

```bash
# Initial vague spec
/shannon:spec "Build marketplace app"

# Output:
# ⚠️ SPECIFICATION TOO VAGUE
# Complexity: ~0.50 (LOW CONFIDENCE)

# Refine based on feedback
/shannon:spec "Build two-sided marketplace connecting freelancers with clients.

Freelancer side:
- Profile creation with portfolio
- Service listings
- Availability calendar
- Pricing configuration

Client side:
- Browse freelancer profiles
- Search by skill, rate, availability
- Booking system
- Messaging

Shared:
- Payment processing (Stripe)
- Review and rating system
- Dispute resolution

Backend: Node.js, PostgreSQL
Frontend: Next.js, Tailwind
Timeline: 4 weeks"

# Output:
# Complexity: 0.61 (COMPLEX - HIGH CONFIDENCE)
# Now has concrete domain percentages, MCP recommendations
```

---

## Troubleshooting

### Issue: "Analysis score seems wrong"

**Symptom**: Complexity score doesn't match intuition

**Examples**:
- "Simple todo app" → 0.42 (expected 0.15)
- "Complex trading system" → 0.68 (expected 0.90)

**Diagnosis**:
```
⚠️ **TRUST THE ALGORITHM**

**Why scores feel wrong**:
1. Human intuition systematically biased (30-50% underestimation)
2. Algorithm considers 8 dimensions (humans typically consider 2-3)
3. Hidden complexity revealed (auth, testing, deployment, error handling)

**Validate Algorithm**:
- Check dimension breakdown (which dimensions scored high?)
- Review domain percentages (do they match specification?)
- Verify MCP recommendations align with domains
- Confirm 5-phase plan makes sense

**If STILL seems wrong**:
- Run with --deep flag for 200-500 step Sequential analysis
- Review calculation in spec-analysis skill walkthrough (lines 1264-1534)
- File issue if mathematical error found
```

**Resolution**: Algorithm is objective. If score feels wrong, algorithm is right. Review dimensions to understand WHY.

---

### Issue: "No MCP recommendations generated"

**Symptom**: Tier 1 has only Serena, no Tier 2 MCPs

**Cause**: Domain detection failed (no tech stack mentioned)

**Example**:
```bash
/shannon:spec "Build a system to manage inventory"
# No React, Express, PostgreSQL mentioned
# Result: Generic domain percentages, no specific MCP recommendations
```

**Resolution**:
```bash
# Add tech stack details
/shannon:spec "Build inventory management system with React frontend, Express backend, PostgreSQL database..."

# Now domain detection works:
# Frontend 35% (React mentioned) → Magic MCP, Puppeteer MCP
# Backend 40% (Express mentioned) → Context7 MCP
# Database 25% (PostgreSQL mentioned) → PostgreSQL MCP
```

---

### Issue: "Timeline estimate too long/short"

**Symptom**: Shannon estimates 5 days but you think 2 days sufficient

**Cause**: Algorithm includes hidden complexity (testing, deployment, docs, error handling)

**Resolution**:
```
⚠️ Shannon timeline includes:
- Implementation (40% of time)
- Testing with NO MOCKS (15% - functional tests take longer than mocks)
- Deployment (10% - infrastructure setup, CI/CD)
- Documentation (5% - technical docs, API docs)
- Planning (15% - spec analysis, architecture)
- Integration (15% - connecting components, debugging)

**User estimate**: Usually only counts implementation (40%)

**Shannon estimate**: Counts COMPLETE delivery (100%)

**If you want faster**:
- Remove deployment → Save 10%
- Skip documentation → Save 5%
- Use mocks → ❌ BLOCKED by Shannon (NO MOCKS iron law)

**Actual timeline**: Shannon's estimate is realistic for production-ready delivery
```

---

## Advanced Usage

### Using with Serena MCP Query

**Scenario**: Retrieve and compare previous analyses

```bash
# Analyze new version of spec
/shannon:spec "Build auth system v2..."

# Query Serena for previous analysis
/list_memories
# Shows: spec_analysis_auth_v1_20251101

# Read previous analysis
/read_memory spec_analysis_auth_v1_20251101

# Compare:
# V1: Complexity 0.45, Timeline 2 days
# V2: Complexity 0.58, Timeline 3 days
# Difference: +0.13 complexity (added OAuth, 2FA, audit logging)
```

**Value**: Track specification evolution and scope creep quantitatively.

---

### Combining with --deep for Ambiguous Specs

**Scenario**: Specification has high uncertainty

```bash
/shannon:spec "Build ML-powered recommendation system.

- Collaborative filtering OR content-based filtering (TBD)
- Real-time OR batch processing (TBD)
- 100K users OR 1M users (unclear)
- AWS OR GCP (undecided)"

--deep
```

**Process**:
```
Sequential MCP analyzes uncertainties:
  thought #15: "Collaborative filtering adds 0.20 complexity"
  thought #45: "Real-time processing adds 0.25 complexity"
  thought #103: "1M users requires different architecture (+0.30 scale)"
  thought #178: "Need to score BOTH scenarios..."

**Analysis generates TWO scores**:
- Conservative: 0.55 (content-based, batch, 100K, AWS)
- Aggressive: 0.78 (collaborative, real-time, 1M, multi-cloud)

**Recommendation**: Plan for AGGRESSIVE (0.78) to avoid under-resourcing
```

**Value**: --deep flag handles ambiguous specs with scenario analysis.

---

## Performance Expectations

| Specification Size | Analysis Time | Mode | Quality Score |
|--------------------|---------------|------|---------------|
| <500 words | 30-60s | standard | 0.95+ |
| 500-2000 words | 1-3 min | standard | 0.90+ |
| 2000-5000 words | 3-8 min | deep | 0.85+ |
| >5000 words (PDF) | 8-15 min | deep | 0.80+ |

**If analysis takes longer**:
- Check: Is specification very large (>3000 words)?
- Check: Is uncertainty score >0.60 (many TBDs)?
- Check: Is Sequential MCP active (deep analysis mode)?

All are expected - large/ambiguous specs take longer for thorough analysis.

---

## Command Output Reference

### Standard Output Sections

1. **Executive Summary**
   - Complexity score (0.0-1.0)
   - Interpretation band (Simple/Moderate/Complex/High/Critical)
   - Execution strategy (Sequential vs Wave-based)
   - Timeline estimate
   - Analysis ID (for Serena retrieval)

2. **Complexity Breakdown Table**
   - 8 dimensions with individual scores
   - Weights (20%, 15%, etc.)
   - Weighted contributions
   - Dimension-specific rationale

3. **Domain Analysis**
   - Domain percentages (Frontend %, Backend %, Database %, etc.)
   - Percentages sum to exactly 100%
   - Domain characteristics (2-3 bullets per domain)

4. **Recommended MCPs**
   - Tiered list (Tier 1 → Tier 2 → Tier 3 → Tier 4)
   - Each MCP with rationale, purpose, usage patterns
   - Health check commands
   - Fallback chains

5. **5-Phase Implementation Plan**
   - Phases with percentages (sum to 100%)
   - Phase objectives (domain-customized)
   - Phase deliverables
   - Validation gates (success criteria)
   - Timeline per phase

6. **Next Steps**
   - Immediate actions (configure MCPs, begin Phase 1)
   - Execution strategy (sequential vs wave)
   - Risk mitigations (if applicable)

### Extended Output (for High/Critical)

7. **Risk Assessment** (complexity >=0.70)
   - Timeline risks
   - Technical risks
   - Coordination risks
   - Dependency risks
   - Mitigation strategies

8. **Wave Execution Preview** (complexity >=0.50)
   - Expected wave count
   - Agent allocation
   - Parallel opportunities
   - Estimated speedup

---

## FAQ

**Q: How long should my specification be?**
A: Minimum 50 words, recommended 100-500 words. Include:
   - 5-10 features
   - Tech stack
   - Timeline constraint
   - Scale/user estimates

**Q: Can I analyze an existing codebase instead?**
A: Use /shannon:spec for codebase analysis. /shannon:spec is for specifications (requirements, not code).

**Q: What if I don't have a written spec?**
A: Describe verbally what you want to build (50+ words). Shannon will structure it.

**Q: Does higher complexity mean worse project?**
A: No. Just means appropriate rigor needed. 0.85 project with proper planning succeeds; 0.45 project without planning fails.

**Q: Can I override the complexity score?**
A: No. Algorithm is objective. If you think it's wrong, check your specification for hidden complexity.

**Q: What if timeline constraint conflicts with calculated timeline?**
A: Shannon will warn and present options (extend timeline, reduce scope, accept risk).

---

**Command**: /shannon:spec
**Skill**: spec-analysis (skills/spec-analysis/SKILL.md)
**Examples**: 15 comprehensive scenarios
**Anti-Patterns**: 5 common mistakes + corrections
**Integration**: Links to /shannon:spec, /shannon:check_mcps, /shannon:spec
