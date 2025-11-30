---
name: shannon-skill-generator
display_name: "Shannon Skill Generator (Meta-Skill)"
description: "Meta-skill that generates project-specific skills based on 8D spec analysis. Analyzes domain percentages, tech stack, and complexity to create tailored implementation skills"
category: meta-programming
version: "4.0.0"
author: "Shannon Framework"
priority: 1
tier: meta
auto_activate: true
activation_triggers:
  - spec_analysis_complete
  - domain_analysis_complete
  - skill_generation_requested
mcp_servers:
  required:
    - serena
  recommended:
    - sequential
    - context7
allowed_tools:
  - Write
  - Read
  - Glob
  - Grep
  - serena_write_memory
  - serena_read_memory
  - sequential_thinking
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
  full_content: resources/FULL_SKILL.md
input:
  spec_analysis:
    type: object
    required: true
    source: serena_memory
    key: spec_analysis_[timestamp]
  complexity_score:
    type: float
    range: [0.0, 1.0]
  domain_percentages:
    type: object
    example: {frontend: 60, backend: 30, database: 10}
  tech_stack:
    type: array
    example: ["React", "Next.js", "Express", "PostgreSQL"]
output:
  generated_skills:
    type: array
    description: "List of generated skill names"
  skill_files:
    type: array
    description: "Paths to generated SKILL.md files"
  activation_priority:
    type: array
    description: "Priority-ordered skills for auto-activation"
---

# Shannon Skill Generator (Meta-Skill)

> **Meta-Programming**: This skill writes other skills based on project specifications

## Purpose

Automatically generates project-specific Shannon skills tailored to:
- Domain percentages (Frontend, Backend, Database, Mobile, DevOps, Security)
- Technology stack (React, Express, PostgreSQL, Swift, Docker, etc.)
- Complexity score (0.0-1.0)
- Framework-specific patterns (Next.js 14, Prisma, SwiftUI, etc.)

## Activation

**Automatic** when:
- `/sh:spec` completes 8D analysis
- Domain percentages calculated
- `spec_analysis_[timestamp]` saved to Serena MCP

**Manual**:
```bash
/sh:generate-skills
--from-spec spec_analysis_[timestamp]
```

## Generation Algorithm

### Step 1: Load Spec Analysis
```javascript
const spec = await serena_read_memory("spec_analysis_[timestamp]")
const {complexity_score, domain_analysis, tech_stack} = spec
```

### Step 2: Domain-to-Skill Mapping

**Frontend ≥ 40%**:
- **React detected** → `shannon-react-ui` (component generation, state management)
- **Next.js 14** → `shannon-nextjs-14-appdir` (App Router, Server Components, caching)
- **Vue 3** → `shannon-vue3-composition` (Composition API, Pinia, Vite)

**Backend ≥ 30%**:
- **Express** → `shannon-express-api` (REST APIs, middleware, error handling)
- **FastAPI** → `shannon-fastapi-async` (async endpoints, Pydantic, dependencies)
- **Django** → `shannon-django-orm` (models, views, admin, migrations)

**Database ≥ 15%**:
- **PostgreSQL + Prisma** → `shannon-postgres-prisma` (schema, migrations, queries)
- **MongoDB** → `shannon-mongodb-mongoose` (schemas, aggregations, indexes)
- **MySQL** → `shannon-mysql-sequelize` (models, relations, transactions)

**Mobile/iOS ≥ 40%**:
- **Swift + SwiftUI** → `shannon-swiftui-lifecycle` (views, state, navigation)
- **Xcode** → `shannon-ios-xcode-build` (build automation, signing, TestFlight)

**DevOps ≥ 15%**:
- **Docker** → `shannon-docker-compose` (multi-container, networks, volumes)
- **AWS** → `shannon-aws-ecs-deploy` (ECS, Lambda, CloudFormation)

### Step 3: Skill Template Selection

Based on domain and framework, select from:

**Templates**:
1. `minimal_skill.template.md` - Simple single-tool skills
2. `workflow_skill.template.md` - Multi-step orchestration
3. `mcp_dependent_skill.template.md` - MCP server integration
4. `framework_specific_skill.template.md` - Framework patterns

### Step 4: Context Injection

Inject into template:
- Framework version (Next.js 14.2.x)
- Specific patterns (App Router, not Pages Router)
- MCP server tools (shadcn-ui for React)
- Testing requirements (Puppeteer for frontend)

### Step 5: TDD Validation

**RED Phase**:
```javascript
// Test without skill
// Document: Does Claude follow framework patterns correctly?
// Expectation: Some mistakes (e.g., using Pages Router instead of App Router)
```

**GREEN Phase**:
```javascript
// Add minimal skill
// Test: Does Claude now follow correct patterns?
// Expectation: Correct framework usage
```

**REFACTOR Phase**:
```javascript
// Try to make Claude rationalize around skill
// Add explicit blocks for successful rationalizations
// Iterate until 100% compliance
```

### Step 6: Save Generated Skills

```javascript
// Write skill files
write_file(`shannon-v4-plugin/skills/${skill_name}/SKILL.md`, skill_content)

// Save to Serena for context
serena_write_memory("generated_skills", {
  timestamp: Date.now(),
  skills: generated_skill_names,
  spec_analysis_id: spec_analysis_id,
  domain_percentages: domain_analysis,
  priority_order: [skill1, skill2, skill3]
})
```

## Example Generation

**Input**:
```yaml
Spec Analysis:
  complexity: 0.68
  domains:
    frontend: 60% (React, Next.js 14 App Router)
    backend: 30% (Express, Node.js)
    database: 10% (PostgreSQL, Prisma)
  tech_stack: ["React 18", "Next.js 14.2", "Express 4", "PostgreSQL 15", "Prisma 5"]
```

**Generated Skills**:
```yaml
1. shannon-nextjs-14-appdir (Priority 1 - 60% weight)
   - App Router patterns
   - Server Components vs Client Components
   - Server Actions
   - Caching strategies (fetch, unstable_cache)
   - Metadata API
   - shadcn-ui MCP integration

2. shannon-express-prisma-api (Priority 2 - 30% weight)
   - Express REST API patterns
   - Prisma Client usage
   - Error handling middleware
   - Authentication (JWT)
   - Request validation

3. shannon-postgres-prisma (Priority 3 - 10% weight)
   - Prisma schema definition
   - Migration workflows
   - Relation queries
   - Transaction handling
   - Performance optimization
```

## Skill Quality Standards

Generated skills MUST include:

✅ **Clear Triggers**: When to activate
✅ **MCP Dependencies**: Required/recommended servers
✅ **Allowed Tools**: Specific tool list
✅ **Framework Version**: Exact version constraints
✅ **Anti-Patterns**: Explicit "DON'T" blocks
✅ **Validation Rules**: Success criteria
✅ **Examples**: Real-world usage patterns

## Integration with Shannon

**Command Flow**:
```
/sh:spec → 8D analysis → domain detection
  ↓
shannon-skill-generator activates
  ↓
Generates project-specific skills
  ↓
Skills auto-loaded for session
  ↓
/sh:wave 1 → agents use generated skills
```

**Context Preservation**:
```
Generated skills saved to:
1. File system: shannon-v4-plugin/skills/[skill-name]/SKILL.md
2. Serena MCP: generated_skills memory
3. Session state: Loaded skills list
```

## v4 Innovation

**vs v3 (Prompt-Based)**:
- v3: One-size-fits-all prose instructions
- v4: Tailored skills per project domain
- v3: ~50K tokens loaded upfront
- v4: ~200 tokens per skill, loaded on-demand

**vs Superpowers**:
- Superpowers: Manual skill creation
- Shannon: Automatic spec-driven generation
- Superpowers: Generic skills
- Shannon: Framework-version-specific skills

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📋 **Skill Templates**: [resources/TEMPLATES.md](./resources/TEMPLATES.md)
🧪 **TDD Methodology**: [resources/TDD_VALIDATION.md](./resources/TDD_VALIDATION.md)

---

**Shannon V4** - Meta-Programming for Spec-Driven Development 🚀
