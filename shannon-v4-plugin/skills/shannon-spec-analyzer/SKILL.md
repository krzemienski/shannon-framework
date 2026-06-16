---
name: shannon-spec-analyzer
display_name: "Shannon Specification Analyzer"
description: "8-dimensional complexity analysis engine for software specifications. Quantifies structural, cognitive, coordination, temporal, technical, scale, uncertainty, and dependency complexity"
category: analysis
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh:spec command"
  - "multi-paragraph specification"
  - "requirements list (5+ items)"
  - "specification keywords detected"
mcp_servers:
  required:
    - serena
  recommended:
    - sequential
    - context7
allowed_tools:
  - Read
  - Glob
  - Grep
  - serena_write_memory
  - serena_read_memory
  - serena_list_memories
  - sequential_thinking
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
  full_content: resources/FULL_SKILL.md
  algorithms: resources/8D_ALGORITHMS.md
input:
  specification:
    type: string
    description: "User specification text (plain text, markdown, or file path)"
    min_length: 50
output:
  complexity_score:
    type: object
    fields:
      total: {type: float, range: [0.0, 1.0]}
      dimensions: {type: object}
  domain_analysis:
    type: object
    description: "Domain percentages and tech stack"
  suggested_mcps:
    type: object
    description: "3-tier MCP recommendations"
  phase_plan:
    type: object
    description: "5-phase implementation plan"
  timeline_estimate:
    type: string
    examples: ["2-4 days", "1-2 weeks"]
  risk_assessment:
    type: array
    description: "Identified risks with mitigation"
---

# Shannon Specification Analyzer

> **8-Dimensional Complexity Analysis**: Quantitative, reproducible project assessment

## Purpose

Transforms unstructured specifications into quantitative complexity assessments:

- **8D Complexity Scoring** (0.0-1.0 scale)
- **Domain Detection** (Frontend, Backend, Database, Mobile, DevOps, Security)
- **MCP Recommendations** (Tier 1/2/3 based on domains)
- **Phase Planning** (5 phases with validation gates)
- **Timeline Estimation** (Evidence-based from complexity)
- **Risk Assessment** (Systematic identification + mitigation)

## Activation

**Automatic**:
- 3+ paragraphs describing a system (each >50 words)
- 5+ requirements in list format
- Keywords: "specification", "requirements", "PRD", "build", "implement"
- `/sh:spec` command

**Manual**:
```bash
Skill("shannon-spec-analyzer")
```

## 8D Complexity Framework

### Dimension 1: Structural (20% weight)
Measures: Files, services, modules, components
```
Score = weighted_sum(
  files × 0.40,
  services × 0.30,
  modules × 0.20,
  components × 0.10
)
```

### Dimension 2: Cognitive (15% weight)
Measures: Analysis, design, decision-making, learning requirements
```
Score = sum(
  analysis_verbs (max 0.40),
  design_verbs (max 0.40),
  decision_verbs (max 0.30),
  learning_verbs (max 0.30)
)
```

### Dimension 3: Coordination (15% weight)
Measures: Teams, integrations, stakeholders
```
Score = (teams × 0.25) + (integrations × 0.15) + (stakeholders × 0.10)
```

### Dimension 4: Temporal (10% weight)
Measures: Urgency, deadlines
```
Score = urgency_multiplier + deadline_factor
```

### Dimension 5: Technical (15% weight)
Measures: Advanced tech (AI/ML, distributed systems), algorithms, integrations
```
Score = advanced_tech + algorithms + integrations
```

### Dimension 6: Scale (10% weight)
Measures: Users, data volume, performance requirements
```
Score = user_factor + data_factor + performance_factor
```

### Dimension 7: Uncertainty (10% weight)
Measures: Ambiguities, exploratory work, research needs
```
Score = ambiguity + exploratory + research
```

### Dimension 8: Dependencies (5% weight)
Measures: Blocking dependencies, external integrations
```
Score = blocking_factor + external_factor
```

### Total Complexity
```
Total = 0.20×structural + 0.15×cognitive + 0.15×coordination +
        0.10×temporal + 0.15×technical + 0.10×scale +
        0.10×uncertainty + 0.05×dependencies
```

**Interpretation**:
| Score | Label | Timeline | Sub-Agents | Waves |
|-------|-------|----------|------------|-------|
| 0.00-0.30 | Simple | Hours-1 day | 1-2 | 0-1 |
| 0.30-0.50 | Moderate | 1-2 days | 2-3 | 1-2 |
| 0.50-0.70 | Complex | 2-4 days | 3-7 | 2-3 |
| 0.70-0.85 | High | 1-2 weeks | 8-15 | 3-5 |
| 0.85-1.00 | Critical | 2+ weeks | 15-25 | 5-8 |

## Domain Detection

**Keyword Counting**:

**Frontend** - Keywords: UI, UX, component, React, Vue, Angular, responsive, CSS, dashboard, form, navigation

**Backend** - Keywords: API, endpoint, REST, GraphQL, server, Express, authentication, JWT, middleware, controller

**Database** - Keywords: database, schema, SQL, PostgreSQL, MongoDB, ORM, Prisma, migration, query, transaction

**Mobile/iOS** - Keywords: iOS, Swift, SwiftUI, Xcode, iPhone, App Store, mobile app, native

**DevOps** - Keywords: deploy, CI/CD, Docker, Kubernetes, AWS, Azure, monitoring, infrastructure

**Security** - Keywords: security, authentication, authorization, encryption, OAuth, vulnerability, compliance

**Calculation**:
```
total_keywords = sum(all_domain_counts)
frontend_percentage = (frontend_count / total_keywords) × 100
[Normalize to sum = 100%]
```

## MCP Recommendations

### Tier 1: MANDATORY
- **Serena MCP** - Always required for context preservation

### Tier 2: PRIMARY (Domain ≥ 20%)
- **Frontend ≥ 20%** → Puppeteer (testing), Context7 (docs)
- **Backend ≥ 20%** → Sequential (reasoning), Context7 (patterns)
- **Mobile ≥ 40%** → Xcode MCP, Context7 (framework docs)
- **Database ≥ 15%** → PostgreSQL/MongoDB/MySQL MCP
- **DevOps ≥ 15%** → GitHub MCP, AWS/Azure/GCP MCP

### Tier 3: PROJECT-SPECIFIC
- **React detected** → shadcn-ui MCP (MANDATORY for React)
- **iOS detected** → Xcode MCP (MANDATORY for iOS)
- **Security ≥ 15%** → Context7 (security patterns)

## 5-Phase Planning

**Phase 1: Analysis & Planning (15%)**
- Requirements gathering
- Constraint identification
- Risk assessment

**Phase 2: Architecture & Design (20%)**
- Design decisions
- Component structure
- API contracts

**Phase 3: Implementation (40%)** [Largest phase]
- Feature development
- Functional testing (NO MOCKS)
- Integration

**Phase 4: Integration & Testing (15%)**
- System integration
- End-to-end testing
- Performance validation

**Phase 5: Deployment & Documentation (10%)**
- Production deployment
- Documentation
- Knowledge transfer

## Execution Flow

### Step 1: Load Context
```javascript
await serena_list_memories()
const previous = await serena_read_memory("spec_analysis_previous")
const project_context = await serena_read_memory("project_context")
```

### Step 2: Parse Specification
Extract:
- Requirements statements
- Technical keywords
- Architectural patterns
- File/service mentions
- Urgency indicators
- Team coordination needs
- Advanced tech mentions
- Scale indicators
- Ambiguities
- Dependencies

### Step 3: Calculate 8D Scores
Run algorithms for each dimension (see resources/8D_ALGORITHMS.md)

### Step 4: Detect Domains
Count keywords, calculate percentages, normalize to 100%

### Step 5: Recommend MCPs
Apply tier rules based on domain percentages

### Step 6: Generate Phase Plan
Create 5-phase plan with validation gates

### Step 7: Estimate Timeline
Correlate complexity score to timeline bands

### Step 8: Assess Risks
Identify risks from dimensions, provide mitigation strategies

### Step 9: Save to Serena (CRITICAL)
```javascript
await serena_write_memory("spec_analysis_[timestamp]", {
  complexity_score: {total, dimensions},
  domain_analysis: {percentages, tech_stack},
  suggested_mcps: {tier1, tier2, tier3},
  phase_plan: {phase1...phase5},
  timeline_estimate,
  risk_assessment,
  metadata: {timestamp, version: "4.0.0", framework: "shannon"}
})
```

### Step 10: Trigger Skill Generation
```javascript
// Auto-activate shannon-skill-generator
Skill("shannon-skill-generator")
```

## Output Format

```markdown
# Specification Analysis Complete ✅

**Complexity**: 0.68 / 1.0 (Complex)
**Timeline**: 2-4 days
**Saved to Serena**: spec_analysis_[timestamp]

## 📊 Complexity Assessment
[8D breakdown table]

## 🎯 Domain Analysis
- Frontend (60%): React 18, Next.js 14 App Router
- Backend (30%): Express 4, Node.js 20
- Database (10%): PostgreSQL 15, Prisma 5

## 🔧 Recommended MCPs
### Tier 1: MANDATORY
- Serena MCP

### Tier 2: PRIMARY
- Puppeteer MCP (Frontend testing)
- Context7 MCP (Framework docs)
- Sequential MCP (Multi-step reasoning)

### Tier 3: PROJECT-SPECIFIC
- shadcn-ui MCP (React component generation)

## 🛠️ Generated Skills
1. shannon-nextjs-14-appdir (Priority 1)
2. shannon-express-prisma-api (Priority 2)
3. shannon-postgres-prisma (Priority 3)

## 📅 5-Phase Plan
[Phase summaries with validation gates]

## ⚠️ Risk Assessment
[Identified risks with mitigation strategies]

## ✅ Next Steps
1. Confirm analysis
2. Install MCPs
3. Verify generated skills
4. Begin Phase 1
5. Run /sh:wave 1 (complexity ≥ 0.7)
```

## Validation

**Pre-Analysis**:
- ✅ Specification ≥ 50 words
- ✅ Contains technical keywords
- ✅ Contains actionable verbs

**Post-Analysis**:
- ✅ Complexity score in [0.0, 1.0]
- ✅ Domain percentages sum to 100%
- ✅ Serena MCP in Tier 1
- ✅ At least 1 domain-specific MCP suggested
- ✅ 5-phase plan generated
- ✅ Analysis saved to Serena

## Innovation

**vs Manual Analysis**:
- Manual: 1-3 hours subjective
- Shannon: 30 seconds reproducible

**vs SuperClaude**:
- SuperClaude: No quantitative assessment
- Shannon: 8-dimensional scoring

**vs v3**:
- v3: Prompt-based instructions
- v4: Skill-based invocation
- Token efficiency: 90% reduction

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
🧮 **8D Algorithms**: [resources/8D_ALGORITHMS.md](./resources/8D_ALGORITHMS.md)
📊 **Examples**: [resources/EXAMPLES.md](./resources/EXAMPLES.md)

---

**Shannon V4** - Quantitative Specification Analysis 🚀
