---
name: sc:design
category: shannon-command
base_command: /design (SuperClaude)
shannon_version: 3.0.0
enhanced: true
wave_enabled: true
description: Enhanced design orchestration with Phase 2 validation gates and architecture decision tracking
---

# /sc:design - Shannon V3 Enhanced Design Command

## Purpose Statement

**Base Function** (SuperClaude): Orchestrate system architecture design, component specifications, and technical planning.

**Shannon V3 Enhancements**:
- **Phase 2 Integration**: Automatic alignment with Phase Planning validation gates
- **Architecture Decision Records**: Persistent tracking via Serena MCP
- **Cross-Wave Context**: Design decisions accessible to all subsequent waves
- **Template Library**: Pre-structured design document templates
- **Validation Automation**: Checklist-driven approval gates
- **MCP Coordination**: Context7 for patterns, Sequential for analysis, Serena for persistence

## Command Metadata

```yaml
command: /sc:design
category: development
complexity: high
wave_enabled: true
phase_alignment: Phase 2 (Architecture)
primary_personas: [architect, system-architect, frontend-architect, backend-architect]
primary_mcps: [sequential, context7, serena]
secondary_mcps: [magic, playwright]
output_artifacts: [architecture.md, schemas.md, api_contracts.md, adr/*.md]
validation_required: true
```

## Usage Patterns

### Basic Usage
```bash
/sc:design [domain] [scope] [flags]
```

**Domains**:
- `system` - Full system architecture (microservices, data flow, component interaction)
- `api` - API contracts and endpoint specifications (REST, GraphQL, WebSocket)
- `database` - Schema design and data modeling (tables, relationships, indexes)
- `frontend` - UI component hierarchy and state management
- `backend` - Service architecture and business logic organization
- `infrastructure` - Deployment, scaling, and operational design

**Scopes**:
- `high-level` - Architecture overview and major component relationships
- `detailed` - Complete specifications with implementation guidance
- `component` - Single component or subsystem design

### Shannon-Specific Flags

```bash
--phase-aware         # Auto-align with Phase 2 validation gates (default: true)
--adr                 # Generate Architecture Decision Records
--template <name>     # Use specific design template
--validation-checklist # Generate Phase 2 validation checklist
--cross-wave-context  # Store for access by all subsequent waves (via Serena)
--interactive         # Step-by-step design with user confirmation
```

### Combined Flags (SuperClaude + Shannon)

```bash
/sc:design system detailed --adr --seq --c7 --validation-checklist
# Full system design with ADRs, Sequential analysis, Context7 patterns, validation

/sc:design api --template rest-api --phase-aware --interactive
# Interactive API design using REST template, aligned with Phase 2 gates

/sc:design database --adr --cross-wave-context --postgres
# Database design with ADRs, stored for wave access, PostgreSQL-specific
```

## Shannon V3 Enhancements

### 1. Phase 2 Validation Gate Integration

**Automatic Alignment**: When `/sc:design` is invoked during Phase 2, Shannon automatically:

1. **Loads Phase 1 Context**:
   ```
   read_memory("spec_analysis_complete")
   read_memory("requirements_complete")
   read_memory("phase_1_complete")
   ```

2. **Creates Phase 2 Validation Checklist**:
   ```markdown
   ## Phase 2 Validation Gate

   ☐ System architecture diagram created
   ☐ Database schema complete (all tables, relationships)
   ☐ API contracts documented (OpenAPI spec)
   ☐ Component hierarchy designed
   ☐ Testing strategy approved (user confirms NO MOCKS approach)
   ☐ Parallelization opportunities identified

   User must approve: "Architecture approved, begin implementation"
   ```

3. **Generates Design Artifacts** aligned with validation requirements

4. **Stores Completion State**:
   ```
   write_memory("architecture_complete", {
     system_architecture: {...},
     database_schema: {...},
     api_contracts: {...},
     validation_checklist: {...},
     approved: false  // awaiting user confirmation
   })
   ```

### 2. Architecture Decision Records (ADR)

**Purpose**: Persistent tracking of design decisions for future reference and wave access.

**Format** (based on Michael Nygard's ADR template):
```markdown
# ADR-001: Use React with TypeScript for Frontend

**Date**: 2025-09-30
**Status**: Accepted
**Context**: Need modern, maintainable frontend framework with strong typing
**Decision**: React 18+ with TypeScript, Vite build system
**Consequences**:
  - Positive: Type safety, component reusability, large ecosystem
  - Negative: Build complexity, TypeScript learning curve
  - Neutral: Need state management solution (TBD in next ADR)
**Alternatives Considered**:
  - Vue 3: Good, but team more familiar with React
  - Angular: Too heavyweight for project scope
**References**: [Context7: React patterns], [spec_analysis: frontend 45%]
```

**Storage Strategy**:
```
Project Root:
├── docs/
│   └── architecture/
│       ├── adr/
│       │   ├── 001-frontend-framework.md
│       │   ├── 002-state-management.md
│       │   ├── 003-database-choice.md
│       │   └── INDEX.md (auto-generated)
│       ├── architecture.md
│       ├── schemas.md
│       └── api_contracts.md
```

**Serena Integration**:
```
write_memory("adr_001_frontend_framework", {
  decision: "React + TypeScript",
  rationale: "...",
  status: "accepted",
  date: "2025-09-30"
})
```

### 3. Cross-Wave Context Preservation

**Problem**: Wave 2+ sub-agents need Phase 2 architecture decisions.

**Solution**: Serena MCP storage with structured access patterns.

```yaml
Phase 2 Output Stored:
  architecture_complete:
    system_design: "Microservices architecture with API gateway..."
    components:
      frontend: "React SPA with Redux state management"
      backend: "Express.js REST API, Node 20 LTS"
      database: "PostgreSQL 15 with Prisma ORM"
    decisions:
      - adr_001: "React + TypeScript"
      - adr_002: "Redux for state management"
      - adr_003: "PostgreSQL over MongoDB"
    validation:
      status: "approved"
      approved_by: "user"
      approved_at: "2025-09-30T14:30:00Z"

Wave 2+ Access Pattern:
  frontend_wave:
    read_memory("architecture_complete")
    → Use components.frontend specification
    → Reference adr_001 and adr_002 for implementation guidance

  backend_wave:
    read_memory("architecture_complete")
    → Use components.backend specification
    → Reference adr_003 for database interaction patterns
```

### 4. Template Library

Shannon provides pre-structured templates for common design patterns:

**System Architecture Template**:
```markdown
# System Architecture: [Project Name]

## Executive Summary
[2-3 sentence overview]

## System Context Diagram
```
[User] → [API Gateway] → [Services]
                        ↓
                    [Database]
```

## Component Breakdown

### Frontend
- Framework: [React/Vue/Angular]
- State Management: [Redux/MobX/Zustand]
- Key Libraries: [list]
- Build System: [Vite/Webpack]

### Backend
- Runtime: [Node/Python/Go]
- Framework: [Express/FastAPI/Gin]
- Architecture Style: [REST/GraphQL/gRPC]
- Authentication: [JWT/OAuth/Session]

### Database
- Type: [PostgreSQL/MongoDB/MySQL]
- ORM/ODM: [Prisma/TypeORM/Mongoose]
- Key Entities: [list]
- Migration Strategy: [approach]

### Infrastructure
- Hosting: [AWS/GCP/Azure/Vercel]
- Containerization: [Docker/Kubernetes]
- CI/CD: [GitHub Actions/GitLab CI]
- Monitoring: [Sentry/DataDog/Prometheus]

## Data Flow

1. User Action → Frontend
2. Frontend → API Gateway (with auth token)
3. API Gateway → Service Layer
4. Service Layer → Database
5. Response propagation back to user

## Security Considerations

- Authentication: [approach]
- Authorization: [RBAC/ABAC]
- Data encryption: [at rest/in transit]
- Input validation: [strategy]

## Performance Strategy

- Caching: [Redis/Memcached]
- Load balancing: [approach]
- Database optimization: [indexes/partitioning]
- CDN usage: [Cloudflare/CloudFront]

## Testing Strategy (NO MOCKS)

- Unit tests: [framework]
- Integration tests: [approach]
- E2E tests: Puppeteer (mandatory functional testing)
- Performance tests: [k6/Artillery]

## Deployment Architecture

[Production environment diagram]

## Wave Parallelization Opportunities

Based on spec analysis:
- Wave 2a: Frontend components (45% complexity)
- Wave 2b: Backend API endpoints (36% complexity)
- Wave 2c: Database setup and integration (14% complexity)

Dependencies:
- All waves depend on Phase 2 architecture approval
- Wave 2c integration requires 2a and 2b completion
```

**API Contract Template** (OpenAPI):
```yaml
openapi: 3.0.0
info:
  title: [API Name]
  version: 1.0.0
  description: [Purpose]

servers:
  - url: http://localhost:3000/api/v1
    description: Development

paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: Created

components:
  schemas:
    User:
      type: object
      properties:
        id: {type: integer}
        email: {type: string}
        created_at: {type: string, format: date-time}
```

**Database Schema Template**:
```sql
-- Database: project_name
-- DBMS: PostgreSQL 15
-- Generated: 2025-09-30

-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);

-- Relationships
-- (Define foreign keys, constraints)

-- Migration strategy: Prisma migrations
-- Seed data: seeds/users.ts
```

## Execution Flow with Validation Gates

### Standard Flow (Non-Phase-Aware)

```mermaid
User: /sc:design system detailed --adr

1. Domain Detection: "system" → system-architect persona
2. Scope Analysis: "detailed" → comprehensive specifications
3. MCP Activation: Sequential (analysis), Context7 (patterns)
4. Template Selection: system_architecture.md
5. Design Generation:
   - System context diagram
   - Component breakdown
   - Data flow
   - Security & performance strategy
6. ADR Generation (--adr flag):
   - Identify major decisions
   - Create ADR files
   - Store in docs/architecture/adr/
7. Serena Storage:
   - write_memory("system_architecture", results)
8. Output Delivery:
   - Present architecture.md
   - Present ADR files
   - Provide implementation guidance
```

### Phase 2 Flow (Phase-Aware)

```mermaid
User: /sc:design system detailed --phase-aware --validation-checklist

Phase 2 Context Loading:
├─ read_memory("spec_analysis_complete")
├─ read_memory("requirements_complete")
├─ read_memory("phase_1_complete")
└─ Load Phase 2 timeline: 4.5 hours, 10-12 todos

Design Generation:
├─ System architecture (aligned with spec analysis domains)
├─ Database schema (based on requirements entities)
├─ API contracts (derived from user stories)
└─ Component hierarchy

Validation Checklist Creation:
☐ System architecture diagram created
☐ Database schema complete
☐ API contracts documented
☐ Component hierarchy designed
☐ Testing strategy approved (NO MOCKS)
☐ Parallelization opportunities identified

User Approval Gate:
  Present all artifacts
  Wait for user confirmation: "Architecture approved, begin implementation"

Post-Approval:
├─ write_memory("architecture_complete", full_design)
├─ write_memory("phase_2_complete", true)
├─ Generate Phase 3 preparation checklist
└─ Output: "Phase 2 validated. Ready for implementation waves."
```

## Sub-Agent Integration

### Primary Sub-Agents

**ARCHITECT** (system-architect):
- **Purpose**: High-level system design and component relationships
- **Activation**: `/sc:design system`
- **Context Access**:
  ```
  read_memory("spec_analysis_complete")
  read_memory("requirements_complete")
  ```
- **Output**: System architecture diagram, component specifications
- **MCP Usage**: Sequential (analysis), Context7 (patterns)

**FRONTEND_ARCHITECT** (frontend-architect):
- **Purpose**: UI component hierarchy and state management design
- **Activation**: `/sc:design frontend`
- **Context Access**:
  ```
  read_memory("architecture_complete")  # if system design exists
  ```
- **Output**: Component tree, state flow, routing structure
- **MCP Usage**: Magic (UI patterns), Context7 (React/Vue patterns)

**BACKEND_ARCHITECT** (backend-architect):
- **Purpose**: API design, service layer, business logic organization
- **Activation**: `/sc:design backend` or `/sc:design api`
- **Context Access**:
  ```
  read_memory("architecture_complete")
  read_memory("database_schema")  # if exists
  ```
- **Output**: API contracts, service specifications, authentication flow
- **MCP Usage**: Context7 (framework patterns), Sequential (security analysis)

**DATABASE_ARCHITECT** (specialized architect):
- **Purpose**: Schema design, relationship modeling, optimization strategy
- **Activation**: `/sc:design database`
- **Context Access**:
  ```
  read_memory("requirements_complete")  # entities from requirements
  read_memory("architecture_complete")  # if exists
  ```
- **Output**: DDL scripts, ER diagrams, index strategy, migration plan
- **MCP Usage**: PostgreSQL MCP (if available), Context7 (ORM patterns)

### Sub-Agent Coordination Patterns

**Sequential Design Flow**:
```
/sc:design system
  → ARCHITECT creates system overview
  → Store: write_memory("architecture_complete")

/sc:design database
  → DATABASE_ARCHITECT reads architecture_complete
  → Creates schema aligned with system design
  → Store: write_memory("database_schema_complete")

/sc:design api
  → BACKEND_ARCHITECT reads architecture_complete + database_schema
  → Creates API contracts aligned with both
  → Store: write_memory("api_contracts_complete")
```

**Parallel Design Flow** (Wave-Enabled):
```
Wave 1 (Design Phase):
  Parallel Sub-Agents:
  ├─ FRONTEND_ARCHITECT → UI specifications
  ├─ BACKEND_ARCHITECT → API specifications
  └─ DATABASE_ARCHITECT → Schema specifications

  Each reads: spec_analysis_complete, requirements_complete
  Each stores: component-specific design

  Synthesis:
  └─ ARCHITECT reviews all designs
     → Identifies integration points
     → Creates unified architecture_complete
```

## Output Format

### Standard Output

```markdown
# Architecture Design: [Project Name]

**Date**: 2025-09-30
**Phase**: 2 (Architecture)
**Designer**: system-architect (Shannon V3)
**Status**: Awaiting Approval

---

## Executive Summary

[2-3 sentence project overview with key architectural choices]

---

## System Architecture

[Detailed system design following template]

---

## Architecture Decision Records

- [ADR-001: Frontend Framework Choice](docs/architecture/adr/001-frontend-framework.md)
- [ADR-002: Database Selection](docs/architecture/adr/002-database-selection.md)
- [ADR-003: API Style](docs/architecture/adr/003-api-style.md)

---

## Wave Parallelization Strategy

Based on spec analysis (complexity: 0.68, domains: Frontend 45%, Backend 36%, Database 14%):

**Wave 2a** (Frontend):
- Build React components
- Implement Redux state management
- Create routing structure
- **Depends on**: Phase 2 approval only

**Wave 2b** (Backend):
- Build Express API endpoints
- Implement authentication middleware
- Create business logic services
- **Depends on**: Phase 2 approval only

**Wave 2c** (Database & Integration):
- Set up PostgreSQL with Prisma
- Run migrations
- Integrate frontend + backend
- **Depends on**: Wave 2a + 2b completion

---

## Phase 2 Validation Checklist

☐ System architecture diagram created
☐ Database schema complete (all tables, relationships)
☐ API contracts documented (OpenAPI spec)
☐ Component hierarchy designed
☐ Testing strategy approved (user confirms NO MOCKS approach)
☐ Parallelization opportunities identified

**Action Required**: Please review all artifacts and confirm:
"Architecture approved, begin implementation"

---

## Next Steps

1. User reviews and approves architecture
2. Shannon stores approval: write_memory("phase_2_complete", true)
3. Wave orchestration begins with Phase 3 implementation
4. All waves access architecture via: read_memory("architecture_complete")
```

## Examples

### Example 1: Full System Design (Phase 2)

```bash
/sc:design system detailed --phase-aware --adr --validation-checklist
```

**Context**: Running during Phase 2 of Shannon workflow.

**Process**:
1. Loads Phase 1 context (spec analysis, requirements)
2. Activates system-architect persona
3. Uses Sequential for architectural analysis
4. Uses Context7 for pattern research (React, Express, PostgreSQL)
5. Generates complete system architecture
6. Creates 3 ADRs (frontend, backend, database choices)
7. Generates Phase 2 validation checklist
8. Stores everything via Serena for wave access
9. Awaits user approval

**Output Files**:
- `docs/architecture/architecture.md` (full system design)
- `docs/architecture/adr/001-frontend-framework.md`
- `docs/architecture/adr/002-backend-framework.md`
- `docs/architecture/adr/003-database-choice.md`
- Serena memory: `architecture_complete`

### Example 2: API Design with Interactive Mode

```bash
/sc:design api --template rest-api --interactive --adr
```

**Process**:
1. Loads REST API template
2. Interactive prompts:
   - "Which entities need CRUD operations?" → User responds
   - "Authentication method?" → User chooses JWT
   - "Rate limiting required?" → User confirms yes
3. Generates OpenAPI specification
4. Creates ADR for authentication choice
5. Provides implementation guidance

**Output**:
- `docs/architecture/api_contracts.yaml` (OpenAPI spec)
- `docs/architecture/adr/004-jwt-authentication.md`

### Example 3: Database Schema Design

```bash
/sc:design database --postgres --adr --cross-wave-context
```

**Process**:
1. Reads requirements_complete for entities
2. Reads architecture_complete if exists
3. Activates DATABASE_ARCHITECT
4. Designs PostgreSQL schema with:
   - Tables for all entities
   - Relationships and foreign keys
   - Indexes for performance
   - Prisma migration strategy
5. Creates ADR for schema decisions
6. Stores via Serena for Wave 2c access

**Output**:
- `docs/architecture/schemas.sql`
- `prisma/schema.prisma` (Prisma schema file)
- `docs/architecture/adr/005-schema-design.md`
- Serena memory: `database_schema_complete`

## Integration with Shannon Workflow

### Pre-Design: Phase 1 Complete

```
Phase 1 Output (from /sc:plan-phases):
├─ spec_analysis_complete
├─ requirements_complete
├─ user_stories_complete (25 stories)
├─ tech_stack_selected (React, Express, PostgreSQL)
└─ phase_1_approved

User confirms: "Phase 1 complete, proceed to architecture"
```

### Design Execution: Phase 2

```
/sc:design system detailed --phase-aware --adr --validation-checklist

Shannon Process:
1. Loads Phase 1 context
2. Generates architecture aligned with tech stack
3. Creates ADRs for major decisions
4. Produces validation checklist
5. Awaits user approval
```

### Post-Design: Phase 3 Preparation

```
User approves: "Architecture approved, begin implementation"

Shannon Process:
1. write_memory("phase_2_complete", true)
2. write_memory("architecture_complete", full_design)
3. Prepare Wave 2 coordination
4. Output: "Ready for /sc:implement with wave orchestration"
```

### Cross-Wave Access Example

```
Wave 2a (Frontend Implementation):
  Sub-Agent: ui-component-builder
  Context Loading:
    read_memory("architecture_complete")
    → components.frontend: "React SPA with Redux"
    → adr_001: "Use functional components with hooks"

  Implementation:
    Follow architecture specifications
    Reference ADRs for decision rationale
    Build components aligned with design

Wave 2b (Backend Implementation):
  Sub-Agent: api-endpoint-builder
  Context Loading:
    read_memory("architecture_complete")
    → components.backend: "Express.js REST API"
    → api_contracts: OpenAPI specification

  Implementation:
    Build endpoints matching OpenAPI spec
    Implement authentication per ADR-004
    Follow architecture patterns
```

## Quality Standards

### Shannon V3 Requirements

✅ **Phase Alignment**: Design must align with Phase 2 validation gates
✅ **Context Preservation**: All designs stored via Serena for wave access
✅ **Decision Tracking**: Major decisions documented in ADRs
✅ **Template Compliance**: Designs follow structured templates
✅ **User Validation**: Explicit approval required before Phase 3
✅ **Wave Awareness**: Parallelization opportunities identified
✅ **NO MOCKS Philosophy**: Testing strategy explicitly defines functional testing

### Design Quality Checklist

- [ ] System context clearly defined
- [ ] All major components identified
- [ ] Data flow documented
- [ ] Security considerations addressed
- [ ] Performance strategy defined
- [ ] Testing approach specified (NO MOCKS)
- [ ] Deployment architecture outlined
- [ ] ADRs created for major decisions
- [ ] Wave parallelization opportunities identified
- [ ] Integration points clearly defined

## Troubleshooting

### Issue: Design Not Aligned with Phase 1

**Symptom**: Architecture doesn't match requirements or tech stack.

**Solution**:
```bash
# Force reload Phase 1 context
read_memory("spec_analysis_complete")
read_memory("requirements_complete")
read_memory("tech_stack_selected")

# Regenerate design
/sc:design system detailed --phase-aware
```

### Issue: Validation Gate Checklist Missing

**Symptom**: No validation checklist generated.

**Solution**:
```bash
# Explicitly request checklist
/sc:design [domain] --validation-checklist --phase-aware
```

### Issue: ADRs Not Created

**Symptom**: No Architecture Decision Records despite `--adr` flag.

**Solution**:
```bash
# Verify ADR directory exists
mkdir -p docs/architecture/adr

# Regenerate with ADRs
/sc:design [domain] --adr

# Or generate ADRs separately
"Create ADR for [decision] in docs/architecture/adr/00X-[name].md"
```

### Issue: Sub-Agents Lack Context

**Symptom**: Wave 2+ sub-agents don't have architecture context.

**Solution**:
```bash
# Verify Serena storage
list_memories()

# Should show: architecture_complete, database_schema_complete, etc.

# If missing, regenerate and store
/sc:design [domain] --cross-wave-context
```

---

**Shannon Framework V3** - Enhanced SuperClaude with Phase Planning, Wave Orchestration, and Context Preservation