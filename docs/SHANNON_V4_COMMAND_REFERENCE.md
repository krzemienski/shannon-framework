# Shannon Framework V4 - Command Reference

Complete reference for all Shannon V4 commands.

---

## Table of Contents

1. [Core Commands](#core-commands)
2. [Wave Management](#wave-management)
3. [Context Management](#context-management)
4. [Testing & Analysis](#testing--analysis)
5. [Utility Commands](#utility-commands)
6. [SuperClaude Integration](#superclaude-integration)

---

## Core Commands

### `/sh_spec` - Analyze Specification

**Purpose:** Analyzes project specification using 8D complexity framework

**Syntax:**
```bash
/sh_spec "<specification_text>"
```

**Parameters:**
- `specification_text` (required): Project specification to analyze

**Output:**
```
Shannon Specification Analysis

Specification: "<your specification>"

8D Complexity Analysis:
├─ Technical: 0.75
├─ Temporal: 0.45
├─ Integration: 0.80
├─ Cognitive: 0.60
├─ Environmental: 0.55
├─ Data: 0.70
├─ Scale: 0.65
└─ Unknown: 0.30

Overall Complexity: 0.62 (COMPLEX)

Domains Identified:
- Backend (primary)
- Database (secondary)
- API Design (secondary)
- Security (supporting)

Recommendations:
- Use wave-based approach (3 waves recommended)
- Allocate 14-21 days total
- Consider database architect early
- Plan security review before deployment

Analysis saved to Serena MCP.
```

**Triggers:**
- Activates `spec-analysis` skill
- Invokes SPEC_ANALYZER agent if complexity ≥ 0.50
- Saves analysis to Serena MCP memory
- Creates initial project checkpoint

**Examples:**
```bash
# Simple specification
/sh_spec "Build REST API for user management with CRUD operations"

# Complex specification
/sh_spec "Build e-commerce platform with payment processing, inventory management, real-time order tracking, admin dashboard, and mobile apps for iOS/Android"

# Domain-specific specification
/sh_spec "Implement machine learning pipeline for customer churn prediction using historical data, feature engineering, model training, and deployment to production"
```

**Notes:**
- Complexity < 0.50: Direct implementation recommended
- Complexity ≥ 0.50: Wave-based approach recommended
- Use Sequential MCP for enhanced reasoning (optional)
- Analysis persists across conversations

---

### `/sh_north_star` - Set Project Goal

**Purpose:** Defines overarching project goal for alignment and decision-making

**Syntax:**
```bash
/sh_north_star "<goal_description>"
```

**Parameters:**
- `goal_description` (required): Clear, measurable project goal

**Output:**
```
North Star Goal Set

Goal: "Launch MVP to 100 beta users by end of Q1"

This goal will guide:
- Wave prioritization
- Feature decisions
- Resource allocation
- Timeline planning

Goal saved to Serena MCP.
```

**Triggers:**
- Activates `goal-management` skill
- Saves goal to Serena MCP
- Included in all checkpoints
- Referenced during wave planning

**Examples:**
```bash
# Time-based goal
/sh_north_star "Launch MVP by March 31st"

# User-based goal
/sh_north_star "Reach 1000 active users in first month"

# Quality goal
/sh_north_star "Achieve 99.9% uptime with sub-200ms response times"

# Business goal
/sh_north_star "Generate $10k MRR within 6 months of launch"
```

**Best Practices:**
- Make goals specific and measurable
- Include timeframes
- Align with business objectives
- Keep goals achievable
- Update as project evolves

---

### `/sh_status` - Show Project Status

**Purpose:** Displays current project state and progress

**Syntax:**
```bash
/sh_status
```

**Parameters:**
None

**Output:**
```
Shannon Framework Status

Version: 4.0.0
Status: Active

Project State:
├─ Specification: "Build e-commerce platform..."
├─ Complexity: 0.68 (COMPLEX)
├─ North Star: "Launch to 1000 customers in 6 months"
├─ Current Wave: Wave 2 of 4
└─ Last Checkpoint: wave-1-complete (2 hours ago)

MCP Status:
├─ Serena: ✅ Connected
├─ Sequential: ✅ Connected
├─ Puppeteer: ✅ Connected
└─ Context7: ⚠️  Not available

Checkpoints Available:
- project-start (3 days ago)
- wave-1-complete (2 hours ago)

Next Steps:
- Execute /sh_wave 2
- Review wave plan with /sh_wave 2 --plan
```

**Triggers:**
- Queries Serena MCP for project state
- Checks MCP connections
- Lists available checkpoints

**Use Cases:**
- Check project progress
- Verify MCP connections
- See available checkpoints
- Understand next steps
- Team status updates

---

## Wave Management

### `/sh_wave` - Execute Development Wave

**Purpose:** Orchestrates wave-based development for complex projects

**Syntax:**
```bash
/sh_wave <wave_number> [--plan]
```

**Parameters:**
- `wave_number` (required): Wave number to execute (1, 2, 3, ...)
- `--plan` (optional): Show wave plan without executing

**Planning Output:**
```
Wave 2 Plan

Duration: 5 days
Dependencies: Wave 1 complete

Phases:
1. Foundation (Day 1-2)
   - Set up payment gateway integration
   - Configure security protocols
   - Create database schemas

2. Implementation (Day 2-4)
   - Implement payment processing
   - Build inventory management
   - Create order tracking system

3. Integration (Day 4-5)
   - Integrate all components
   - End-to-end testing
   - Documentation

Deliverables:
- Payment processing API
- Inventory management system
- Order tracking endpoints
- Integration tests
- API documentation

Agents Assigned:
- BACKEND (primary)
- DATABASE_ARCHITECT (supporting)
- SECURITY (review)
- API_DESIGNER (review)

Ready to execute? Run: /sh_wave 2
```

**Execution Output:**
```
Wave 2 Execution

WAVE_COORDINATOR activated

Phase 1: Foundation (Current)
├─ Setting up payment gateway... ✅
├─ Configuring security protocols... ⏳
└─ Creating database schemas... ⏳

Progress: 33% complete
Estimated completion: 4 days

[Work continues with agent coordination...]

Wave 2 Complete! ✅

Deliverables:
✅ Payment processing API
✅ Inventory management system
✅ Order tracking endpoints
✅ Integration tests
✅ API documentation

Checkpoint created: wave-2-complete

Next: /sh_wave 3 --plan
```

**Triggers:**
- Activates `wave-orchestration` skill
- Invokes WAVE_COORDINATOR agent
- Activates domain agents as needed
- Creates automatic checkpoints
- Updates project state in Serena MCP

**Examples:**
```bash
# Plan wave before executing
/sh_wave 1 --plan

# Execute wave
/sh_wave 1

# Continue to next wave
/sh_wave 2
```

**Best Practices:**
- Always review plan first (`--plan`)
- Execute waves sequentially
- Don't skip waves
- Create checkpoints after waves
- Verify completion before continuing

---

## Context Management

### `/sh_checkpoint` - Save Project State

**Purpose:** Creates named checkpoint of complete project state

**Syntax:**
```bash
/sh_checkpoint "<checkpoint_name>"
```

**Parameters:**
- `checkpoint_name` (required): Unique name for checkpoint

**Output:**
```
Checkpoint Created

Name: feature-auth-complete
Created: 2025-01-15 14:30:00
Size: 2.4 KB

Saved Context:
├─ Specification
├─ Complexity analysis
├─ North star goal
├─ Current wave progress
├─ Agent assignments
├─ Memory entries
└─ Project state

Stored in: Serena MCP

Restore with: /sh_restore "feature-auth-complete"
```

**Triggers:**
- Activates `context-preservation` skill
- Invokes CONTEXT_GUARDIAN agent
- Saves all state to Serena MCP
- Creates restoration point

**Examples:**
```bash
# Before major work
/sh_checkpoint "pre-refactor"

# After features
/sh_checkpoint "feature-auth-complete"
/sh_checkpoint "feature-payments-complete"

# Before deployment
/sh_checkpoint "pre-production"

# Version releases
/sh_checkpoint "v1.0.0-release"

# Wave completions
/sh_checkpoint "wave-1-complete"
```

**Naming Conventions:**
```bash
# Features
feature-<name>-start
feature-<name>-complete

# Waves
wave-<number>-start
wave-<number>-complete

# Releases
v<x>.<y>.<z>-release
pre-production
post-deployment

# Experiments
experiment-<name>-baseline
experiment-<name>-results

# Milestones
milestone-<name>
```

---

### `/sh_restore` - Restore Project State

**Purpose:** Restores complete project context from checkpoint

**Syntax:**
```bash
/sh_restore "<checkpoint_name>"
```

**Parameters:**
- `checkpoint_name` (required): Name of checkpoint to restore

**Output:**
```
Checkpoint Restored

Name: feature-auth-complete
Created: 2025-01-15 14:30:00

Restored Context:
├─ Specification: "Build e-commerce platform..."
├─ Complexity: 0.68 (COMPLEX)
├─ North Star: "Launch to 1000 customers..."
├─ Wave Progress: Wave 1 complete, Wave 2 in progress
├─ Agent State: BACKEND, DATABASE_ARCHITECT active
├─ Memory: 12 entries loaded
└─ Project State: Ready

You can now continue where you left off.

Run /sh_status to see current state.
```

**Triggers:**
- Activates `context-restoration` skill
- Loads data from Serena MCP
- Restores all project state
- Reactivates agents if needed

**Examples:**
```bash
# Restore after context loss
/sh_restore "wave-1-complete"

# Restore for comparison
/sh_restore "pre-refactor"

# Restore for rollback
/sh_restore "last-good-state"

# Restore for team coordination
/sh_restore "team-baseline"
```

**Use Cases:**
- New conversation sessions
- Context loss recovery
- Team member onboarding
- Version comparison
- Rollback scenarios
- Experiment comparison

---

### `/sh_memory` - Manage Project Memory

**Purpose:** Interacts with Serena MCP memory system

**Syntax:**
```bash
/sh_memory --list                        # List all memories
/sh_memory --read "<memory_name>"        # Read memory
/sh_memory --write "<name>" "<content>"  # Write memory
/sh_memory --delete "<memory_name>"      # Delete memory
```

**Parameters:**
- `--list`: List all available memories
- `--read`: Read specific memory
- `--write`: Create/update memory
- `--delete`: Remove memory

**List Output:**
```
Project Memories

Available memories (8):
├─ architecture (3 days ago)
├─ coding-standards (3 days ago)
├─ deployment (2 days ago)
├─ api-patterns (2 days ago)
├─ database-schema (1 day ago)
├─ test-strategy (1 day ago)
├─ security-requirements (1 day ago)
└─ performance-targets (1 day ago)

Read with: /sh_memory --read "<name>"
```

**Read Output:**
```
Memory: architecture

Content:
Microservices architecture with event-driven communication
- API Gateway: Kong
- Services: Node.js/Express
- Message Queue: RabbitMQ
- Database: PostgreSQL (per service)
- Cache: Redis
- Deployment: Kubernetes on AWS EKS

Created: 3 days ago
Last updated: 2 days ago
```

**Write Output:**
```
Memory Saved

Name: security-requirements
Size: 0.8 KB

Content saved to Serena MCP.

Access with: /sh_memory --read "security-requirements"
```

**Examples:**
```bash
# List all memories
/sh_memory --list

# Read architecture decisions
/sh_memory --read "architecture"

# Save coding standards
/sh_memory --write "coding-standards" "TypeScript strict mode, ESLint, Prettier, Jest for testing"

# Save deployment info
/sh_memory --write "deployment" "AWS ECS Fargate, RDS PostgreSQL, CloudFront CDN, Route53 DNS"

# Delete outdated memory
/sh_memory --delete "old-architecture"
```

**What to Store:**
- Architecture decisions
- Coding standards
- Deployment procedures
- API patterns
- Testing strategies
- Security requirements
- Performance targets
- Team conventions
- Third-party integrations
- Configuration details

---

## Testing & Analysis

### `/sh_test` - Create Functional Tests

**Purpose:** Generates functional tests following NO MOCKS philosophy

**Syntax:**
```bash
/sh_test [--create] [--platform <platform>] [--feature "<feature>"]
```

**Parameters:**
- `--create`: Generate new test suite
- `--platform`: Target platform (web, api, mobile)
- `--feature`: Feature to test

**Output:**
```
Functional Test Suite Generated

Platform: web
Feature: user login

Generated Files:
├─ tests/functional/login.spec.ts
├─ tests/helpers/browser.ts
└─ tests/fixtures/test-users.json

Test Suite Uses:
✅ Puppeteer MCP (real browser)
✅ Real authentication endpoints
✅ Actual database (test instance)
❌ No mocks

Test Cases:
1. Valid login redirects to dashboard
2. Invalid credentials show error
3. Password reset flow works
4. Session persistence verified
5. Logout clears session

Run tests: npm test -- login.spec.ts

NO MOCKS Philosophy Enforced ✅
```

**Triggers:**
- Activates `functional-testing` skill
- Invokes TEST_GUARDIAN agent
- Uses Puppeteer MCP for web tests
- Enforces NO MOCKS principles

**Examples:**
```bash
# Web application tests
/sh_test --create --platform web --feature "user registration"
/sh_test --create --platform web --feature "checkout flow"
/sh_test --create --platform web --feature "dashboard"

# API tests
/sh_test --create --platform api --feature "task CRUD"
/sh_test --create --platform api --feature "authentication"

# Mobile tests
/sh_test --create --platform mobile --feature "offline sync"
```

**Supported Platforms:**
- `web`: Browser tests using Puppeteer MCP
- `api`: API tests using real HTTP clients
- `mobile`: Mobile app tests using real devices/simulators

**NO MOCKS Enforcement:**
- ✅ Real browsers via Puppeteer MCP
- ✅ Real HTTP requests
- ✅ Real databases (test instances)
- ✅ Real third-party APIs (dev/staging)
- ❌ No jest.mock()
- ❌ No sinon stubs
- ❌ No test doubles

---

### `/sh_analyze` - Deep Project Analysis

**Purpose:** Performs comprehensive project analysis

**Syntax:**
```bash
/sh_analyze [--domains] [--dependencies] [--risks]
```

**Parameters:**
- `--domains`: Analyze domain complexity
- `--dependencies`: Analyze dependencies
- `--risks`: Analyze risks and blockers

**Domain Analysis Output:**
```
Domain Analysis

Identified Domains:
├─ Backend (complexity: 0.75)
│  ├─ Primary concerns: API design, business logic, data flow
│  └─ Recommended agent: BACKEND

├─ Database (complexity: 0.70)
│  ├─ Primary concerns: Schema design, migrations, optimization
│  └─ Recommended agent: DATABASE_ARCHITECT

├─ Frontend (complexity: 0.60)
│  ├─ Primary concerns: UI/UX, state management, performance
│  └─ Recommended agent: FRONTEND

└─ Security (complexity: 0.80)
   ├─ Primary concerns: Authentication, authorization, data protection
   └─ Recommended agent: SECURITY

Recommendations:
- Start with database schema (foundation)
- Backend and frontend can proceed in parallel
- Security review before deployment
```

**Examples:**
```bash
# Analyze all domains
/sh_analyze --domains

# Analyze dependencies
/sh_analyze --dependencies

# Analyze risks
/sh_analyze --risks

# Combined analysis
/sh_analyze --domains --dependencies --risks
```

---

### `/sh_scaffold` - Generate Project Scaffolding

**Purpose:** Creates initial project structure

**Syntax:**
```bash
/sh_scaffold --framework <framework> [--template <template>]
```

**Parameters:**
- `--framework`: Framework choice (react, express, nextjs, etc.)
- `--template`: Optional template variant

**Output:**
```
Project Scaffolding Generated

Framework: react
Template: typescript

Created Structure:
project-root/
├─ src/
│  ├─ components/
│  ├─ pages/
│  ├─ hooks/
│  ├─ utils/
│  └─ App.tsx
├─ public/
├─ tests/
│  └─ functional/
├─ package.json
├─ tsconfig.json
├─ .eslintrc.js
└─ README.md

Next Steps:
1. npm install
2. npm run dev
3. Open http://localhost:3000

Project initialized ✅
```

**Supported Frameworks:**
- `react`: React application
- `express`: Express API
- `nextjs`: Next.js application
- `fastify`: Fastify API
- `vue`: Vue.js application
- `nestjs`: NestJS application

**Examples:**
```bash
# React with TypeScript
/sh_scaffold --framework react --template typescript

# Express API
/sh_scaffold --framework express

# Next.js with App Router
/sh_scaffold --framework nextjs --template app-router
```

---

## Utility Commands

### `/sh_check_mcps` - Check MCP Status

**Purpose:** Shows status of all MCPs and provides installation guidance

**Syntax:**
```bash
/sh_check_mcps
```

**Parameters:**
None

**Output:**
```
MCP Status Report

Required:
├─ Serena MCP: ✅ Connected (v2.1.0)
│  └─ Status: Working correctly

Recommended:
├─ Sequential MCP: ✅ Connected (v1.5.0)
│  └─ Benefit: Enhanced reasoning for complex specs
│
├─ Puppeteer MCP: ⚠️  Not available
│  ├─ Benefit: Browser testing for web applications
│  └─ Install: npm install -g @anthropic/puppeteer-mcp
│
└─ Context7 MCP: ✅ Connected (v3.0.0)
   └─ Benefit: Framework-specific patterns and best practices

Optional:
└─ [Other MCPs...]

Overall Status: Partially Available

Shannon will work with current configuration but some features
will use fallback implementations.

Recommendations:
- Install Puppeteer MCP for web testing
- Current setup sufficient for API/backend projects
```

**Triggers:**
- Activates `mcp-discovery` skill
- Checks MCP connections
- Provides installation guidance
- Shows fallback behavior

---

## SuperClaude Integration

Shannon V4 integrates with SuperClaude (multi-Claude orchestration) through specialized commands:

### `/sc_build` - SuperClaude Build

**Purpose:** Coordinate build tasks across multiple Claude instances

**Syntax:**
```bash
/sc_build --target <target> [--parallel]
```

*See SuperClaude documentation for complete reference*

---

## Command Quick Reference

### Core Workflow
```bash
/sh_spec "<spec>"          # Analyze specification
/sh_north_star "<goal>"    # Set project goal
/sh_wave <N> --plan        # Plan wave
/sh_wave <N>               # Execute wave
/sh_status                 # Check status
```

### Context Management
```bash
/sh_checkpoint "<name>"    # Save state
/sh_restore "<name>"       # Restore state
/sh_memory --list          # List memories
/sh_memory --read "<n>"    # Read memory
```

### Testing & Analysis
```bash
/sh_test --create --platform <p>  # Generate tests
/sh_analyze --domains             # Analyze domains
/sh_scaffold --framework <f>      # Generate scaffolding
```

### Utilities
```bash
/sh_check_mcps            # Check MCP status
```

---

## Command Patterns

### Simple Project Pattern
```bash
/sh_spec "Build simple REST API"
# Follow implementation guidance
/sh_test --create --platform api
```

### Complex Project Pattern
```bash
/sh_spec "Build complex platform..."
/sh_north_star "Launch by Q1"
/sh_checkpoint "baseline"
/sh_wave 1 --plan
/sh_wave 1
/sh_checkpoint "wave-1"
/sh_wave 2 --plan
/sh_wave 2
/sh_checkpoint "wave-2"
```

### Team Coordination Pattern
```bash
# Lead
/sh_spec "Team project..."
/sh_checkpoint "team-baseline"

# Team members
/sh_restore "team-baseline"
/sh_wave <assigned>
/sh_checkpoint "wave-<N>-complete"
```

---

## Version Compatibility

This command reference is for **Shannon Framework V4.0.0**.

Commands maintain backward compatibility with V3:
- All V3 commands work identically
- Same arguments and options
- Same output formats
- Same behavior

New in V4:
- Skill-based architecture (transparent)
- Enhanced agent system (automatic)
- Improved MCP integration
- Better error handling

---

For detailed usage patterns and workflows, see:
- User Guide: `SHANNON_V4_USER_GUIDE.md`
- Skill Reference: `SHANNON_V4_SKILL_REFERENCE.md`
- Migration Guide: `SHANNON_V4_MIGRATION_GUIDE.md`
