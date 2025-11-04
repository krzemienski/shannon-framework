# 5-Phase Planning Examples

This document provides three detailed examples of phase planning across different complexity levels: Simple, Complex, and Critical.

---

## Example 1: Simple Project - Todo List CLI (Complexity 0.25)

### Project Overview
- **Name**: Todo List CLI
- **Description**: Simple command-line todo list application
- **Complexity Score**: 0.25
- **Total Timeline**: 8 hours
- **Domain Breakdown**:
  - Backend: 70% (CLI logic, file storage)
  - Frontend: 30% (CLI interface, formatting)

### Phase Plan (3 Phases)

#### Phase 1: Setup & Core Implementation (30% - 2.4 hours)

**Objectives**:
- Set up Node.js project structure
- Implement core todo operations (add, list, complete)
- Create file-based storage system

**Key Activities**:
1. Project scaffolding (20%)
   - Initialize npm project
   - Install dependencies (commander.js, chalk)
   - Set up directory structure

2. Core functionality (60%)
   - Implement add() function
   - Implement list() function
   - Implement complete() function
   - Create JSON file storage

3. CLI interface (20%)
   - Set up commander.js
   - Add command handlers
   - Implement help text

**Deliverables**:
- `package.json` with dependencies
- `src/todo.js` with core functions
- `src/cli.js` with command interface
- `todos.json` storage file

**Validation Gate**:
☐ All three operations (add/list/complete) working
☐ Data persists to JSON file
☐ CLI help text displays correctly
☐ Dependencies installed successfully

**Estimated Duration**: 2.4 hours

---

#### Phase 2: Features & Testing (50% - 4 hours)

**Objectives**:
- Add advanced features (delete, edit, filter)
- Implement comprehensive testing (NO MOCKS)
- Add color formatting and user experience improvements

**Key Activities**:
1. Advanced features (40%)
   - Implement delete() function
   - Implement edit() function
   - Add filtering (by status, date)
   - Add search functionality

2. Testing (40%)
   - Create test fixtures (real JSON files)
   - Write integration tests (real file I/O)
   - Test all CLI commands
   - Test edge cases (empty list, invalid input)

3. UX improvements (20%)
   - Add color formatting (chalk)
   - Improve list display (tables)
   - Add success/error messages
   - Implement input validation

**Deliverables**:
- Enhanced `src/todo.js` with all operations
- `tests/todo.test.js` (100% pass rate)
- Improved CLI output formatting
- Input validation and error handling

**Validation Gate**:
☐ All features implemented and working
☐ All tests passing (NO MOCKS - real file operations)
☐ Input validation catches errors
☐ User experience is polished
☐ Code coverage >= 80%

**Estimated Duration**: 4 hours

---

#### Phase 3: Deployment & Documentation (20% - 1.6 hours)

**Objectives**:
- Package for npm distribution
- Create comprehensive documentation
- Set up installation instructions

**Key Activities**:
1. Packaging (40%)
   - Configure npm bin entry
   - Add shebang to CLI file
   - Test global installation
   - Create .npmignore

2. Documentation (50%)
   - Write README.md with examples
   - Document all commands
   - Add usage screenshots
   - Create CONTRIBUTING.md

3. Final polish (10%)
   - Clean up console.log statements
   - Verify all TODOs removed
   - Test on different platforms
   - Final code review

**Deliverables**:
- npm-ready package structure
- Comprehensive README.md
- Installation guide
- Usage examples

**Validation Gate**:
☐ Package installs globally with npm
☐ All commands work after global install
☐ README is complete and accurate
☐ No console.log or TODO comments remain

**Estimated Duration**: 1.6 hours

---

### Timeline Summary
```
Total: 8 hours
├─ Phase 1: 2.4h (30%)
├─ Phase 2: 4.0h (50%)
└─ Phase 3: 1.6h (20%)

Wave Execution: Sequential (low complexity)
Parallelization: None
```

---

## Example 2: Complex Project - Real-Time Chat App (Complexity 0.65)

### Project Overview
- **Name**: Real-Time Chat Application
- **Description**: WebSocket-based chat with React frontend and Express backend
- **Complexity Score**: 0.65
- **Total Timeline**: 40 hours
- **Domain Breakdown**:
  - Frontend: 45% (React, WebSocket client, UI)
  - Backend: 35% (Express, Socket.io, authentication)
  - Database: 20% (PostgreSQL, chat history)

### Phase Plan (5 Phases)

#### Phase 1: Foundation & Setup (20% - 8 hours)

**Objectives**:
- Design complete system architecture
- Set up development environment
- Define database schema and API contracts
- Install and configure all dependencies

**Key Activities**:
1. System architecture design (35%)
   - Create architecture diagram (components + data flow)
   - Define WebSocket event contracts
   - Plan authentication strategy (JWT)
   - Design database schema

2. Environment setup (30%)
   - Initialize React app (Vite)
   - Initialize Express backend
   - Set up PostgreSQL database
   - Configure development environment

3. API contract definition (25%)
   - Define REST API endpoints
   - Define WebSocket events
   - Create OpenAPI specification
   - Document request/response schemas

4. MCP verification (10%)
   - Install Serena MCP (context preservation)
   - Install Puppeteer MCP (E2E testing)
   - Install PostgreSQL MCP (database testing)
   - Test all MCPs working

**Deliverables**:
- `architecture.md` with system diagram
- `database_schema.sql` with tables and relationships
- `api_contracts.yaml` (OpenAPI spec)
- `websocket_events.md` (event documentation)
- Initialized React and Express projects

**Validation Gate**:
☐ Architecture diagram complete and approved
☐ Database schema designed with all relationships
☐ API contracts documented (REST + WebSocket)
☐ All dependencies installed
☐ All required MCPs verified working
☐ Development environment functional

**Estimated Duration**: 8 hours

---

#### Phase 2: Core Implementation (35% - 14 hours)

**Objectives**:
- Build frontend and backend in parallel waves
- Implement core chat functionality
- Set up WebSocket connections
- Integrate with database

**Wave Structure**:
```
Wave 2a: Frontend (6h) - PARALLEL
Wave 2b: Backend + Database (6h) - PARALLEL
Wave 2c: Integration (2h) - SEQUENTIAL
```

**Wave 2a: Frontend (Parallel)**

Activities:
1. Component development (50%)
   - ChatRoom component
   - MessageList component
   - MessageInput component
   - UserList component
   - LoginForm component

2. State management (25%)
   - Set up Redux Toolkit
   - Create message slice
   - Create auth slice
   - Create user slice

3. WebSocket client (25%)
   - Initialize Socket.io client
   - Implement event listeners
   - Connect to Redux state
   - Handle connection errors

Deliverables:
- Complete React component tree
- Redux store configured
- WebSocket client integrated

**Wave 2b: Backend + Database (Parallel)**

Activities:
1. Database setup (25%)
   - Run schema migrations
   - Create seed data
   - Set up connection pool
   - Test queries

2. API endpoints (40%)
   - POST /auth/register
   - POST /auth/login
   - GET /messages/:roomId
   - GET /users
   - Middleware (auth, validation)

3. WebSocket server (35%)
   - Initialize Socket.io server
   - Implement event handlers (message, join, leave)
   - Broadcast logic
   - Room management
   - Message persistence

Deliverables:
- PostgreSQL database with schema applied
- Express API with all endpoints
- Socket.io server configured
- Authentication system (JWT)

**Wave 2c: Integration (Sequential)**

Activities:
1. Connect frontend to backend (60%)
   - Configure API base URL
   - Test authentication flow
   - Connect WebSocket client to server
   - Verify message flow

2. Integration testing (30%)
   - Test user registration
   - Test user login
   - Test sending messages
   - Test receiving messages
   - Test room functionality

3. Bug fixing (10%)
   - Fix CORS issues
   - Fix WebSocket connection problems
   - Fix authentication bugs
   - Fix message ordering

Deliverables:
- Fully integrated application
- All core features working end-to-end
- Integration bugs fixed

**Validation Gate**:
☐ Frontend components render correctly
☐ Backend API endpoints respond correctly
☐ Database queries execute successfully
☐ WebSocket connection establishes
☐ Messages send and receive in real-time
☐ Authentication flow works (register → login → chat)
☐ All P0 features implemented

**Estimated Duration**: 14 hours
- Wave 2a: 6h (parallel)
- Wave 2b: 6h (parallel)
- Wave 2c: 2h (sequential)
- **Parallelization Gain**: 40% time saved vs sequential (6h saved)

---

#### Phase 3: Integration & Enhancement (25% - 10 hours)

**Objectives**:
- Add advanced features
- Implement typing indicators
- Add file sharing
- Improve user experience

**Key Activities**:
1. Advanced features (50%)
   - Typing indicators (WebSocket events)
   - Online/offline status
   - Read receipts
   - Message reactions (emoji)
   - File upload and sharing

2. UI/UX enhancements (30%)
   - Message timestamps
   - User avatars
   - Notification sounds
   - Unread message counts
   - Responsive design improvements

3. Performance optimization (20%)
   - Message pagination
   - Lazy loading chat history
   - WebSocket reconnection logic
   - Optimize database queries
   - Add indexes for performance

**Deliverables**:
- All advanced features implemented
- Enhanced UI with polish
- Optimized performance
- Better error handling

**Validation Gate**:
☐ Typing indicators working
☐ Online/offline status accurate
☐ File sharing functional
☐ UI is responsive and polished
☐ Performance acceptable (<200ms message latency)
☐ Error handling robust

**Estimated Duration**: 10 hours

---

#### Phase 4: Quality & Polish (15% - 6 hours)

**Objectives**:
- Comprehensive testing (NO MOCKS)
- Performance testing
- Security hardening
- Code quality improvements

**Key Activities**:
1. Testing (50%)
   - Integration tests (real database, real API)
   - E2E tests (Puppeteer MCP - real browser)
   - WebSocket stress testing
   - Multi-user scenario testing
   - Edge case testing

2. Security (25%)
   - SQL injection prevention (parameterized queries)
   - XSS prevention (sanitize input)
   - CSRF protection
   - Rate limiting
   - Security audit

3. Performance (15%)
   - Load testing (100 concurrent users)
   - Database query optimization
   - WebSocket performance tuning
   - Bundle size optimization

4. Code quality (10%)
   - Code review
   - Linting fixes
   - Remove console.logs
   - Documentation improvements

**Deliverables**:
- `tests/` directory with all tests
- 100% test pass rate
- Security audit report
- Performance benchmark results
- Clean, reviewed code

**Validation Gate**:
☐ All tests passing (100%)
☐ NO MOCKS used in any tests
☐ Code coverage >= 80%
☐ Security audit passed
☐ Performance benchmarks met (100 users, <200ms latency)
☐ Code quality checks passed

**Estimated Duration**: 6 hours

---

#### Phase 5: Deployment & Handoff (5% - 2 hours)

**Objectives**:
- Deploy to staging environment
- Create deployment documentation
- Prepare for production

**Key Activities**:
1. Staging deployment (50%)
   - Deploy backend to Heroku/Railway
   - Deploy frontend to Vercel/Netlify
   - Configure PostgreSQL (managed service)
   - Set environment variables
   - Test deployment

2. Documentation (40%)
   - Deployment guide
   - Environment setup instructions
   - Architecture documentation
   - API documentation
   - Troubleshooting guide

3. Final verification (10%)
   - Smoke tests on staging
   - Verify all features working
   - Check monitoring/logging
   - Review security settings

**Deliverables**:
- Staging deployment URL
- Complete deployment guide
- Updated README
- Production-ready checklist

**Validation Gate**:
☐ Application deployed to staging
☐ All smoke tests passing on staging
☐ Environment variables configured
☐ Monitoring/logging operational
☐ Documentation complete
☐ Production-ready

**Estimated Duration**: 2 hours

---

### Timeline Summary
```
Total: 40 hours
├─ Phase 1: 8h (20%)
├─ Phase 2: 14h (35%)
│   ├─ Wave 2a: 6h (Frontend - parallel)
│   ├─ Wave 2b: 6h (Backend - parallel)
│   └─ Wave 2c: 2h (Integration - sequential)
├─ Phase 3: 10h (25%)
├─ Phase 4: 6h (15%)
└─ Phase 5: 2h (5%)

Wave Execution: Parallel (Phase 2)
Parallelization Gain: 40% (6 hours saved)
```

---

## Example 3: Critical Project - E-Commerce Platform (Complexity 0.92)

### Project Overview
- **Name**: E-Commerce Platform
- **Description**: Full-featured e-commerce system with inventory, payments, and admin
- **Complexity Score**: 0.92
- **Total Timeline**: 80 hours
- **Domain Breakdown**:
  - Frontend: 30% (React, cart, checkout)
  - Backend: 40% (Express, payments, inventory)
  - Database: 20% (PostgreSQL, complex queries)
  - Security: 10% (PCI compliance, authentication)

### Phase Plan (6 Phases - 5 Standard + Risk Mitigation)

#### Phase 1: Foundation & Planning (25% - 20 hours)

**Objectives**:
- Extensive requirements analysis
- Comprehensive architecture design
- Security planning (PCI compliance)
- Detailed database schema design

**Key Activities**:
1. Requirements analysis (30%)
   - User stories (50+ stories)
   - Feature prioritization (P0/P1/P2/P3)
   - Non-functional requirements (PCI, GDPR)
   - Constraint documentation
   - Stakeholder interviews

2. Architecture design (35%)
   - System architecture diagram
   - Microservices vs monolith decision
   - Payment gateway integration design
   - Inventory management design
   - Admin panel architecture
   - Scalability planning

3. Security planning (20%)
   - PCI DSS compliance checklist
   - Authentication/authorization design
   - Data encryption strategy
   - Security audit planning
   - Compliance documentation

4. Database design (15%)
   - Complete schema (15+ tables)
   - Relationships and indexes
   - Migration strategy
   - Backup/disaster recovery plan
   - Performance optimization plan

**Deliverables**:
- `requirements.md` (comprehensive)
- `user_stories.md` (50+ stories)
- `architecture.md` with diagrams
- `security_plan.md` (PCI compliance)
- `database_schema.sql` (complete)
- `api_contracts.yaml` (OpenAPI 3.0)

**Validation Gate**:
☐ All requirements documented and approved
☐ Architecture reviewed and signed off
☐ Security plan validated by compliance expert
☐ Database schema reviewed by DBA
☐ All stakeholders aligned
☐ No blocking unknowns remain

**Estimated Duration**: 20 hours

---

#### Phase 2: Core Implementation (25% - 20 hours)

**Objectives**:
- Build all core components in parallel
- Implement payment gateway integration
- Create inventory management system
- Build admin panel

**Wave Structure**:
```
Wave 2a: Frontend (8h) - PARALLEL
Wave 2b: Backend API (8h) - PARALLEL
Wave 2c: Database (4h) - PARALLEL
Wave 2d: Integration (4h) - SEQUENTIAL
```

**Wave 2a: Frontend (Parallel)**

Activities:
1. E-commerce UI (60%)
   - Product catalog page
   - Product detail page
   - Shopping cart
   - Checkout flow (multi-step)
   - User account page
   - Order history

2. Admin panel (30%)
   - Product management
   - Order management
   - Inventory dashboard
   - Analytics dashboard

3. State management (10%)
   - Redux Toolkit setup
   - Cart state
   - Auth state
   - Product catalog state

Deliverables:
- Complete customer frontend
- Complete admin panel
- Redux store configured

**Wave 2b: Backend API (Parallel)**

Activities:
1. Product API (25%)
   - CRUD operations for products
   - Search and filtering
   - Category management
   - Image upload

2. Order API (30%)
   - Order creation
   - Order status management
   - Payment processing integration
   - Email notifications

3. Inventory API (20%)
   - Stock management
   - Low stock alerts
   - Inventory adjustments
   - Supplier management

4. Admin API (15%)
   - User management
   - Role-based access control
   - Analytics endpoints
   - Reporting

5. Authentication (10%)
   - User registration/login
   - Admin authentication
   - JWT token management
   - Session handling

Deliverables:
- Complete REST API
- Payment gateway integrated (Stripe)
- Email service configured

**Wave 2c: Database (Parallel)**

Activities:
1. Schema implementation (40%)
   - Run all migrations
   - Create indexes
   - Set up constraints
   - Configure triggers

2. Seed data (30%)
   - Test products (100+ items)
   - Categories and tags
   - Test users (customers + admins)
   - Sample orders

3. Optimization (30%)
   - Query performance tuning
   - Index optimization
   - Materialized views for analytics
   - Partitioning strategy

Deliverables:
- PostgreSQL database fully configured
- All tables created with data
- Performance optimized

**Wave 2d: Integration (Sequential)**

Activities:
1. API integration (40%)
   - Connect frontend to backend
   - Test all endpoints
   - Fix integration issues
   - Verify data flow

2. Payment testing (30%)
   - Stripe test mode setup
   - Test checkout flow
   - Test refund flow
   - Test error scenarios

3. Integration testing (30%)
   - Test complete user flows
   - Test admin operations
   - Test inventory updates
   - Fix bugs

Deliverables:
- Fully integrated platform
- Payment flow working
- All core features functional

**Validation Gate**:
☐ All frontend pages render correctly
☐ All API endpoints respond correctly
☐ Database performs well under load
☐ Payment gateway integration working
☐ Inventory management functional
☐ Admin panel operational
☐ All P0 features implemented

**Estimated Duration**: 20 hours
- Waves 2a/2b/2c: 8h (parallel)
- Wave 2d: 4h (sequential)
- **Parallelization Gain**: 50% time saved vs sequential (12h saved)

---

#### Phase 3: Integration & Enhancement (20% - 16 hours)

**Objectives**:
- Advanced features (wishlists, reviews, recommendations)
- Third-party integrations (shipping, analytics)
- Mobile responsiveness
- Performance optimization

**Key Activities**:
1. Advanced features (45%)
   - Product reviews and ratings
   - Wishlist functionality
   - Product recommendations (ML-based)
   - Coupon/discount system
   - Gift cards
   - Multiple payment methods

2. Third-party integrations (30%)
   - Shipping provider API (USPS, FedEx)
   - Analytics (Google Analytics)
   - Email marketing (Mailchimp)
   - SMS notifications (Twilio)

3. Mobile responsiveness (15%)
   - Mobile-optimized layouts
   - Touch-friendly UI
   - Progressive Web App (PWA)
   - Mobile checkout optimization

4. Performance (10%)
   - Image optimization (CDN)
   - Code splitting
   - Lazy loading
   - Caching strategies

**Deliverables**:
- All advanced features implemented
- Third-party services integrated
- Mobile-responsive design
- Optimized performance

**Validation Gate**:
☐ Reviews and ratings working
☐ Recommendations accurate
☐ Shipping integration functional
☐ Mobile experience excellent
☐ Performance benchmarks met (<2s page load)
☐ All integrations tested

**Estimated Duration**: 16 hours

---

#### Phase 4: Quality & Testing (20% - 16 hours)

**Objectives**:
- Extensive testing (NO MOCKS)
- Security audit
- Performance testing
- Load testing
- Compliance verification

**Key Activities**:
1. Functional testing (35%)
   - Integration tests (real database, real API, real Stripe)
   - E2E tests (Puppeteer MCP - real browser)
   - Complete user flows (browse → cart → checkout → order)
   - Admin workflow testing
   - Payment scenarios (success, failure, refund)

2. Security testing (25%)
   - PCI DSS compliance audit
   - Penetration testing
   - SQL injection testing
   - XSS prevention verification
   - Authentication/authorization testing
   - Rate limiting verification

3. Performance testing (20%)
   - Load testing (1000 concurrent users)
   - Database performance under load
   - API response times
   - Frontend rendering performance
   - Payment gateway performance

4. Compliance verification (15%)
   - GDPR compliance check
   - PCI DSS self-assessment
   - Accessibility audit (WCAG 2.1)
   - Legal review (terms, privacy policy)

5. Code quality (5%)
   - Code review
   - Security linting
   - Performance profiling
   - Documentation review

**Deliverables**:
- `tests/` directory (200+ tests)
- Security audit report
- Performance benchmark results
- Compliance checklist (completed)
- Code quality report

**Validation Gate**:
☐ All tests passing (100%)
☐ NO MOCKS used in any tests
☐ Code coverage >= 85%
☐ Security audit passed (no critical issues)
☐ PCI DSS compliant
☐ Performance benchmarks met
☐ Compliance verified

**Estimated Duration**: 16 hours

---

#### Phase 5: Risk Mitigation (5% - 4 hours)

**Objectives**:
- Identify and mitigate critical risks
- Disaster recovery testing
- Backup verification
- Monitoring setup
- Incident response planning

**Key Activities**:
1. Risk assessment (25%)
   - Identify critical failure points
   - Analyze security vulnerabilities
   - Review compliance gaps
   - Assess performance bottlenecks

2. Disaster recovery (30%)
   - Test database backups
   - Test restore procedures
   - Verify backup automation
   - Document recovery steps
   - Test failover scenarios

3. Monitoring setup (25%)
   - Application monitoring (New Relic, Datadog)
   - Error tracking (Sentry)
   - Uptime monitoring (Pingdom)
   - Performance monitoring (APM)
   - Alert configuration

4. Incident response (20%)
   - Create incident response plan
   - Define escalation procedures
   - Set up on-call rotation
   - Document runbooks
   - Test incident procedures

**Deliverables**:
- Risk assessment report
- Disaster recovery plan (tested)
- Monitoring dashboards configured
- Incident response plan
- Runbooks for common issues

**Validation Gate**:
☐ All critical risks identified and mitigated
☐ Backup/restore tested successfully
☐ Monitoring operational and alerting
☐ Incident response plan complete
☐ Team trained on procedures

**Estimated Duration**: 4 hours

---

#### Phase 6: Deployment & Handoff (5% - 4 hours)

**Objectives**:
- Production deployment
- Comprehensive documentation
- Team training
- Knowledge transfer

**Key Activities**:
1. Production deployment (40%)
   - Deploy backend (AWS/GCP)
   - Deploy frontend (CDN)
   - Configure database (managed PostgreSQL)
   - Set up Stripe production mode
   - Configure all environment variables
   - Set up SSL certificates
   - Configure DNS

2. Smoke testing (20%)
   - Test production environment
   - Verify payment processing (small test transaction)
   - Check all integrations
   - Verify monitoring/alerts
   - Test backup systems

3. Documentation (25%)
   - Architecture documentation
   - API documentation (Swagger UI)
   - Deployment guide
   - Operations manual
   - Troubleshooting guide
   - Admin user guide

4. Knowledge transfer (15%)
   - Team training sessions
   - Handoff to support team
   - Developer onboarding docs
   - Admin training materials

**Deliverables**:
- Production deployment (live)
- Complete documentation suite
- Training materials
- Handoff checklist (completed)

**Validation Gate**:
☐ Application deployed to production
☐ All smoke tests passing
☐ Payment processing verified (real transaction)
☐ Monitoring and alerts working
☐ Documentation complete and reviewed
☐ Team trained and ready

**Estimated Duration**: 4 hours

---

### Timeline Summary
```
Total: 80 hours
├─ Phase 1: 20h (25%) - Foundation & Planning
├─ Phase 2: 20h (25%) - Core Implementation
│   ├─ Wave 2a: 8h (Frontend - parallel)
│   ├─ Wave 2b: 8h (Backend - parallel)
│   ├─ Wave 2c: 4h (Database - parallel)
│   └─ Wave 2d: 4h (Integration - sequential)
├─ Phase 3: 16h (20%) - Integration & Enhancement
├─ Phase 4: 16h (20%) - Quality & Testing
├─ Phase 5: 4h (5%) - Risk Mitigation
└─ Phase 6: 4h (5%) - Deployment & Handoff

Wave Execution: Parallel (Phase 2)
Parallelization Gain: 50% (12 hours saved)

Risk Mitigation Phase: Required (complexity 0.92)
Security Focus: PCI DSS compliance throughout
```

---

## Summary Comparison

| Aspect | Simple (0.25) | Complex (0.65) | Critical (0.92) |
|--------|---------------|----------------|-----------------|
| **Phase Count** | 3 | 5 | 6 (5 + risk) |
| **Timeline** | 8h | 40h | 80h |
| **Waves** | Sequential | Parallel (Phase 2) | Parallel (Phase 2) |
| **Parallelization Gain** | 0% | 40% | 50% |
| **Planning Phase** | 30% | 20% | 25% |
| **Testing Phase** | 50% | 15% | 20% |
| **Risk Mitigation** | None | None | Dedicated phase |
| **Validation Gates** | 3 | 5 | 6 |
| **Security Focus** | Basic | Moderate | Extensive (PCI) |
| **Testing Rigor** | Basic | Comprehensive | Extensive + Audit |

---

**Key Takeaways**:

1. **Complexity drives structure**: More complex projects need more phases and gates
2. **Parallelization scales**: Higher complexity enables more parallel work
3. **Planning increases**: Critical projects spend proportionally more time planning
4. **Testing rigor varies**: Critical projects require extensive testing and audits
5. **Risk mitigation**: Only critical projects need dedicated risk mitigation phase
6. **Validation gates**: More phases = more checkpoints for quality
