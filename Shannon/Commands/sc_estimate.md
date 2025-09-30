---
name: sc:estimate
description: Evidence-based development estimation with 8-dimensional complexity analysis and historical learning
category: Planning
priority: high
base: SuperClaude /estimate command
shannon_enhancements: true
triggers: [estimate, timeline, effort, duration, how long, time needed, schedule]
auto_activate: true
activation_threshold: 0.6
tools: [Read, Grep, Glob, TodoWrite]
mcp_servers: [serena, sequential, context7]
sub_agents: [spec-analyzer, phase-architect]
output_format: structured_timeline_report
---

# /sc:estimate - Evidence-Based Development Estimation

## Purpose Statement

Enhanced from SuperClaude's `/estimate` command, `/sc:estimate` provides **evidence-based development estimation** using Shannon V3's 8-dimensional complexity scoring, historical project data via Serena MCP, and systematic timeline calculation based on proven project patterns.

**Key Innovation**: Replaces speculative "gut feel" estimation with objective complexity scoring and historical data learning for reproducible, accurate timeline predictions.

## Shannon V3 Enhancements Over SuperClaude

### Enhancement Matrix

| Capability | SuperClaude /estimate | Shannon /sc:estimate | Impact |
|------------|----------------------|---------------------|---------|
| **Complexity Analysis** | Manual, subjective | 8-dimensional scoring (0.0-1.0) | Objective, reproducible |
| **Historical Data** | No learning | Serena MCP stores actual durations | Improves accuracy over time |
| **Sub-Agent Integration** | Single-agent analysis | SPEC_ANALYZER + PHASE_ARCHITECT collaboration | Comprehensive estimation |
| **Confidence Intervals** | Single estimate | Min-Expected-Max ranges with confidence % | Risk-aware planning |
| **Phase Breakdown** | Ad-hoc | 5-phase template with validation gates | Structured timelines |
| **MCP Coordination** | Static usage | Dynamic Sequential + Context7 + Serena | Better intelligence |
| **Estimation Units** | Hours/days only | Hours, days, weeks with developer count | Flexible planning |

### Core Innovation: 8-Dimensional Complexity Scoring

Shannon replaces subjective complexity guessing with **objective, measurable complexity scoring** across 8 dimensions:

1. **Structural Complexity** (0.0-1.0): File count, services, modules, architecture layers
2. **Cognitive Complexity** (0.0-1.0): Design patterns, decision points, algorithmic difficulty
3. **Coordination Complexity** (0.0-1.0): Team dependencies, integration points, communication needs
4. **Temporal Complexity** (0.0-1.0): Deadlines, urgency, time constraints
5. **Technical Complexity** (0.0-1.0): Advanced technologies, algorithms, performance requirements
6. **Scale Complexity** (0.0-1.0): Data volume, user load, concurrent operations
7. **Uncertainty Complexity** (0.0-1.0): Ambiguities, unknowns, research requirements
8. **Dependency Complexity** (0.0-1.0): External dependencies, blockers, third-party integrations

**Overall Complexity** = Weighted average of all 8 dimensions

**Estimation Formula**:
```
Base Effort (hours) = f(Overall_Complexity, Domain_Mix, Historical_Data)

Where:
- Overall_Complexity: 0.0-1.0 score from 8 dimensions
- Domain_Mix: Percentage breakdown (frontend, backend, database, mobile, devops, security)
- Historical_Data: Actual durations from Serena MCP for similar projects
```

### Enhancement 2: Historical Learning via Serena

Every project completion stores actual effort data to Serena MCP:

```yaml
# Stored after project completion
serena_key: "project_actuals_[timestamp]"
data:
  complexity_score: 0.72
  estimated_hours: 80
  actual_hours: 95
  variance: +18.75%
  domains: {frontend: 40%, backend: 50%, database: 10%}
  lessons_learned: "Underestimated database migration complexity"
```

**Learning Loop**:
1. First project: Use base complexity formula
2. Store actual vs estimated data to Serena
3. Next project: Query Serena for similar complexity/domain projects
4. Adjust estimation using historical variance patterns
5. Continuously improve accuracy

**Result**: Estimation accuracy improves from ~60% → 85%+ over time.

## Usage Patterns

### Basic Usage
```
/sc:estimate "Build React e-commerce site with Stripe integration"
/sc:estimate @spec.md
/sc:estimate @PRD.pdf --detailed
```

### Advanced Usage
```
# With specific scope
/sc:estimate "Implement user authentication" --scope module

# With team size context
/sc:estimate @spec.md --team-size 3 --availability 0.7

# With historical comparison
/sc:estimate "Mobile app" --compare-historical

# Fast estimation (skip detailed analysis)
/sc:estimate "Add search feature" --quick
```

### Flags

| Flag | Effect | Use When |
|------|--------|----------|
| `--detailed` | Full 8-dimensional breakdown | Important decisions, presentations |
| `--quick` | Fast estimation (skip analysis) | Small features, rough estimates |
| `--scope [file\|module\|project]` | Define estimation boundary | Clear scope exists |
| `--team-size N` | Adjust for N developers | Team planning |
| `--availability N` | Account for partial availability (0.0-1.0) | Part-time teams |
| `--compare-historical` | Show similar past projects | Learn from history |
| `--confidence-interval` | Show min-expected-max ranges | Risk planning |
| `--phase-breakdown` | Show 5-phase timeline detail | Structured planning |

## Execution Flow

### Phase 1: Context Discovery (Serena MCP)
```
Step 1: Load Previous Estimations
Execute: list_memories()
Identify: estimation_*, project_actuals_*, complexity_patterns_*

Step 2: Load Historical Data
Execute: read_memory("project_actuals_[recent]")
Purpose: Learn from past estimation accuracy

Step 3: Load Existing Analysis
Execute: read_memory("spec_analysis")
Purpose: Reuse complexity scoring if already analyzed
```

### Phase 2: Specification Analysis (SPEC_ANALYZER Sub-Agent)

If spec analysis doesn't exist in Serena, spawn SPEC_ANALYZER:

```
Activation: @spec-analyzer sub-agent
Task: Complete 8-dimensional complexity analysis
Input: User specification or requirements
Output: write_memory("spec_analysis_[timestamp]", {
  complexity_scores: {8 dimensions},
  overall_complexity: 0.72,
  domains: {breakdown},
  file_count_estimate: 35,
  service_count: 4,
  integration_points: 7
})
```

**SPEC_ANALYZER Responsibilities**:
- Parse specification completely
- Calculate all 8 complexity dimensions with evidence
- Identify domains and percentages
- Count estimated artifacts (files, services, APIs)
- Save results to Serena for reuse

### Phase 3: Phase Planning (PHASE_ARCHITECT Sub-Agent)

Spawn PHASE_ARCHITECT to create structured timeline:

```
Activation: @phase-architect sub-agent
Task: Create 5-phase plan with time allocations
Input: spec_analysis from Serena
Output: write_memory("phase_plan", {
  phases: [
    {name: "Discovery", duration_pct: 20%, hours: 16},
    {name: "Architecture", duration_pct: 15%, hours: 12},
    {name: "Implementation", duration_pct: 45%, hours: 36},
    {name: "Testing", duration_pct: 15%, hours: 12},
    {name: "Deployment", duration_pct: 5%, hours: 4}
  ],
  total_hours: 80,
  validation_gates: 5
})
```

**PHASE_ARCHITECT Responsibilities**:
- Apply 5-phase template (Discovery 20%, Architecture 15%, Implementation 45%, Testing 15%, Deployment 5%)
- Adjust percentages based on domain mix (e.g., more testing for security domains)
- Define validation gates
- Calculate phase durations
- Account for rework probability (complexity-based)

### Phase 4: Timeline Calculation (Sequential MCP)

Use Sequential MCP for complex timeline logic:

```
Activation: Sequential MCP reasoning
Task: Calculate timeline with confidence intervals
Input: spec_analysis + phase_plan + historical_data
Logic:
  1. Base effort = f(complexity, domains, artifact_count)
  2. Historical adjustment = avg(similar_projects.variance)
  3. Team adjustment = base_effort / (team_size × availability)
  4. Rework buffer = complexity × 0.15 (high complexity = more rework)
  5. Confidence intervals:
     - Optimistic (10th percentile): base × 0.85
     - Expected (50th percentile): base × 1.0
     - Pessimistic (90th percentile): base × 1.35
```

### Phase 5: Synthesis & Output

Generate structured estimation report:

```markdown
# Estimation Report: [Project Name]

## Executive Summary
- **Overall Complexity**: 0.72 (High)
- **Estimated Effort**: 80 hours (Expected)
- **Confidence Interval**: 68-108 hours (80% confidence)
- **Timeline**: 10 business days (1 developer @ 8hr/day)
- **Team Adjusted**: 4 days (2 developers @ 70% availability)

## 8-Dimensional Complexity Analysis

### Structural Complexity: 0.68
- Estimated 35 files across 4 services
- 3-tier architecture (frontend, API, database)
- Evidence: React SPA + Node.js API + PostgreSQL

### Cognitive Complexity: 0.75
- Advanced state management patterns required
- Complex business logic (payment processing, inventory)
- Evidence: Stripe integration, real-time inventory sync

### [Continue for all 8 dimensions...]

## Domain Breakdown

| Domain | Percentage | Hours | Key Activities |
|--------|-----------|-------|----------------|
| Frontend | 40% | 32 | React components, state management, UI |
| Backend | 50% | 40 | API endpoints, business logic, integrations |
| Database | 10% | 8 | Schema design, migrations |

## Phase Timeline

### Phase 1: Discovery (20%, 16 hours, 2 days)
- Requirements finalization
- Technical research (Stripe API, React patterns)
- Architecture decisions
- **Validation Gate**: Requirements approved by stakeholders

### Phase 2: Architecture (15%, 12 hours, 1.5 days)
- System design
- Database schema
- API contract definition
- **Validation Gate**: Architecture review complete

### Phase 3: Implementation (45%, 36 hours, 4.5 days)
- Wave 1: Backend API (18 hours)
- Wave 2: Frontend UI (18 hours)
- Parallel execution opportunity
- **Validation Gate**: Feature complete, integration tests pass

### Phase 4: Testing (15%, 12 hours, 1.5 days)
- Functional testing (Puppeteer)
- Stripe integration testing
- Performance validation
- **Validation Gate**: All tests passing

### Phase 5: Deployment (5%, 4 hours, 0.5 days)
- Production deployment
- Monitoring setup
- Documentation
- **Validation Gate**: Production verification complete

## Historical Comparison

Similar projects (via Serena MCP):
- **Project A** (complexity: 0.70): Estimated 75h, Actual 88h (+17%)
- **Project B** (complexity: 0.74): Estimated 85h, Actual 82h (-4%)
- **Average Variance**: +6.5%

**Recommendation**: Add 10% buffer for unknowns → 88 hours total

## Risk Factors

### High Impact Risks
- **Stripe API complexity**: +8 hours (mitigated by early spike)
- **Real-time inventory sync**: +6 hours (complex state management)

### Medium Impact Risks
- **Third-party API rate limits**: +4 hours (implement caching)

## Confidence Analysis

| Scenario | Effort | Timeline | Probability |
|----------|--------|----------|-------------|
| Optimistic | 68 hours | 8.5 days | 10% |
| Expected | 80 hours | 10 days | 50% |
| Pessimistic | 108 hours | 13.5 days | 90% |

**Recommendation**: Plan for Expected (80h), communicate Pessimistic (108h) to stakeholders

## Team Sizing Recommendations

| Team Size | Availability | Duration | Notes |
|-----------|-------------|----------|-------|
| 1 developer | 100% | 10 days | Sequential work, long timeline |
| 2 developers | 70% | 7 days | Parallel frontend/backend, realistic |
| 3 developers | 100% | 4 days | Maximum parallelization, coordination overhead |

**Optimal**: 2 developers @ 70% availability = 7 business days
```

## Sub-Agent Integration Details

### SPEC_ANALYZER Activation

**When**: No spec_analysis exists in Serena OR --reanalyze flag used

**Spawning**:
```markdown
Use @spec-analyzer sub-agent to perform 8-dimensional complexity analysis.

Input: [user specification]
Expected Output: Serena memory key "spec_analysis_[timestamp]"
Required: Complete all 8 dimensions with evidence
```

**SPEC_ANALYZER delivers**:
- 8-dimensional complexity scores with evidence for each
- Overall complexity score (weighted average)
- Domain identification and percentages
- Artifact count estimates (files, services, APIs, database tables)
- Risk factors and uncertainties
- MCP server recommendations

### PHASE_ARCHITECT Activation

**When**: Always (required for structured timeline)

**Spawning**:
```markdown
Use @phase-architect sub-agent to create 5-phase implementation plan.

Input: spec_analysis from Serena
Expected Output: Serena memory key "phase_plan"
Required: 5 phases with hours, validation gates, dependencies
```

**PHASE_ARCHITECT delivers**:
- 5-phase breakdown (Discovery, Architecture, Implementation, Testing, Deployment)
- Phase percentages adjusted for domain mix
- Hour allocations per phase
- Validation gate definitions
- Phase dependencies and parallel opportunities
- Wave recommendations for Implementation phase

## MCP Server Coordination

### Serena MCP (Primary - Context & Learning)

**Usage**:
```
1. list_memories() - discover available context
2. read_memory("spec_analysis") - load complexity analysis
3. read_memory("project_actuals_*") - historical learning
4. write_memory("estimation_[timestamp]", results) - save for future
```

**Learning Pattern**:
- Store estimation_* for in-progress projects
- Convert to project_actuals_* on completion
- Query similar projects for variance patterns
- Improve accuracy with each project

### Sequential MCP (Timeline Logic)

**Usage**: Complex timeline calculations with confidence intervals

**Reasoning Tasks**:
- Effort calculation from complexity + domains + artifacts
- Confidence interval computation (10th/50th/90th percentiles)
- Team size and availability adjustments
- Rework buffer calculations based on uncertainty
- Risk impact quantification

### Context7 MCP (Framework Research)

**Usage**: When domains involve specific frameworks

**Queries**:
- "React development time patterns" → inform frontend estimates
- "Node.js API complexity" → inform backend estimates
- "PostgreSQL migration best practices" → inform database estimates
- Framework-specific gotchas that impact timelines

## Output Format Specifications

### Executive Summary (Always)
- Overall complexity score (0.0-1.0)
- Expected effort (hours)
- Confidence interval (min-max range)
- Timeline in business days
- Team size recommendations

### Detailed Analysis (--detailed flag)
- Full 8-dimensional breakdown with evidence
- Domain percentage breakdown with activities
- Historical comparison (if similar projects exist)
- Risk factors with quantified impact
- Confidence analysis with scenarios

### Quick Format (--quick flag)
- Complexity score
- Estimated hours (single number)
- Suggested timeline
- Major risks only

### Phase Breakdown (--phase-breakdown flag)
- All 5 phases with durations
- Validation gates
- Dependencies
- Parallel opportunities
- Wave structure for Implementation phase

## Integration with Other Commands

### Before /sc:estimate
- `/sh:analyze-spec` - Creates spec_analysis in Serena (reused by estimate)
- `/sc:plan-phases` - Creates phase_plan in Serena (reused by estimate)

### After /sc:estimate
- `/sc:execute-waves` - Uses estimation to plan wave execution
- `/implement` - References timeline for realistic expectations
- `/git` - Uses phase timeline for commit planning

### Chaining Example
```
User: /sh:analyze-spec @spec.md
→ Creates spec_analysis in Serena

User: /sc:estimate @spec.md
→ Reads spec_analysis from Serena (no reanalysis needed)
→ Spawns phase-architect
→ Generates timeline with confidence intervals

User: /sc:execute-waves
→ Reads spec_analysis + estimation from Serena
→ Plans wave execution based on timeline
```

## Examples

### Example 1: Simple Feature Estimation
```
User: /sc:estimate "Add user profile edit functionality"

Output:
# Estimation Report: User Profile Edit Feature

## Executive Summary
- **Overall Complexity**: 0.35 (Low-Medium)
- **Estimated Effort**: 12 hours
- **Timeline**: 1.5 business days (1 developer)

## Quick Analysis
- Frontend: React form component (6 hours)
- Backend: PUT /api/user/:id endpoint (4 hours)
- Testing: Functional tests (2 hours)

## Recommendation
Single developer can complete in 2 days with buffer.
```

### Example 2: Full Application Estimation
```
User: /sc:estimate @ecommerce_spec.md --detailed --team-size 2

Output:
# Estimation Report: E-Commerce Platform

## Executive Summary
- **Overall Complexity**: 0.72 (High)
- **Estimated Effort**: 160 hours (Expected)
- **Confidence Interval**: 136-216 hours (80% confidence)
- **Timeline**: 20 days (1 dev) → 12 days (2 devs @ 70%)

## 8-Dimensional Complexity Analysis
[Full breakdown of all 8 dimensions with evidence]

## Domain Breakdown
- Frontend (40%): 64 hours
- Backend (45%): 72 hours
- Database (10%): 16 hours
- DevOps (5%): 8 hours

## Phase Timeline
[Complete 5-phase breakdown with hours and gates]

## Historical Comparison
- Similar project A: +15% variance
- Similar project B: +8% variance
- Recommendation: Plan for 180 hours (Expected + 12.5% buffer)

## Team Recommendations
**Optimal Configuration**: 2 developers @ 70% availability = 12 business days
- Developer A: Frontend + UI/UX
- Developer B: Backend + Database
- Parallel work reduces total timeline by 40%
```

### Example 3: Historical Learning
```
User: /sc:estimate "Mobile shopping app" --compare-historical

Output:
# Estimation Report: Mobile Shopping App

## Current Estimation
- **Complexity**: 0.68
- **Estimated**: 120 hours

## Historical Comparison (via Serena MCP)

### Similar Project: "Retail Mobile App" (6 months ago)
- Complexity: 0.65
- Estimated: 110 hours
- Actual: 135 hours
- Variance: +22.7%
- Lesson: "Underestimated iOS simulator setup and native module integration"

### Similar Project: "Food Delivery App" (3 months ago)
- Complexity: 0.71
- Estimated: 130 hours
- Actual: 140 hours
- Variance: +7.7%
- Lesson: "Better MCP coordination improved accuracy"

### Recommendation
Based on historical mobile app variance (+15% average):
- **Adjusted Estimate**: 138 hours
- **With 10% safety buffer**: 152 hours
- **Communicate to stakeholders**: 150-160 hours
```

## Quality Standards

### Estimation Accuracy Targets
- **First project**: ±40% variance acceptable (no historical data)
- **After 5 projects**: ±20% variance target
- **After 10 projects**: ±15% variance target (excellent)

### Confidence Interval Requirements
- **Optimistic (10th percentile)**: 85% of base estimate
- **Expected (50th percentile)**: 100% of base estimate
- **Pessimistic (90th percentile)**: 135% of base estimate

### Evidence Requirements
- Every complexity score MUST have supporting evidence
- Domain percentages MUST reference specific features
- Historical comparisons MUST cite specific Serena memory keys
- Risk factors MUST have quantified hour impacts

### Serena MCP Storage
- ALWAYS save estimation results: write_memory("estimation_[timestamp]", full_report)
- On project completion: update with actuals, rename to project_actuals_[timestamp]
- Store lessons learned for future pattern matching

## Best Practices

### Do's
✅ Load historical data from Serena before estimating
✅ Use objective 8-dimensional scoring, not gut feel
✅ Provide confidence intervals, not single numbers
✅ Account for team size and availability realistically
✅ Include validation gates in timeline
✅ Store results to Serena for learning
✅ Compare to similar historical projects
✅ Quantify risk impacts in hours

### Don'ts
❌ Never estimate without complexity analysis
❌ Don't ignore historical variance patterns
❌ Don't provide false precision (avoid "exactly 73.5 hours")
❌ Don't forget coordination overhead for multi-developer teams
❌ Don't skip rework buffers for high complexity
❌ Don't lose estimation data (always save to Serena)
❌ Don't use round numbers without justification ("100 hours" suspicious)

## Performance Optimization

### Fast Path (--quick flag)
- Skip detailed 8-dimensional analysis
- Use simplified complexity heuristic
- Skip historical comparison
- Provide single estimate, no confidence interval
- **Use for**: Small features, rough planning, quick feedback

### Standard Path (default)
- Complete 8-dimensional analysis (if not cached)
- Historical comparison (if similar projects exist)
- Confidence intervals
- Phase breakdown
- **Use for**: Normal project planning

### Deep Path (--detailed flag)
- Full analysis with evidence for every dimension
- Multiple historical project comparisons
- Risk quantification
- Team sizing analysis
- Wave structure recommendations
- **Use for**: Important decisions, presentations, complex projects

## Success Metrics

Shannon's /sc:estimate is successful when:

### Functional Metrics
- ✅ Generates objective complexity scores (0.0-1.0) with evidence
- ✅ Provides confidence intervals (min-expected-max)
- ✅ Improves accuracy using historical Serena data
- ✅ Accounts for team size and availability
- ✅ Breaks down timeline into 5 phases with gates

### Quality Metrics
- ✅ Estimation variance ≤20% after 5 projects (with historical learning)
- ✅ 90% of projects complete within pessimistic estimate
- ✅ Historical patterns successfully match similar projects
- ✅ Team sizing recommendations validated by actual execution

### Integration Metrics
- ✅ Reuses spec_analysis from /sh:analyze-spec (no duplicate work)
- ✅ Successfully spawns SPEC_ANALYZER and PHASE_ARCHITECT sub-agents
- ✅ Stores all estimates to Serena for future learning
- ✅ Feeds timelines to /sc:execute-waves for wave planning

## Command Evolution

**Version History**:
- **SuperClaude /estimate**: Manual analysis, single estimate, no learning
- **Shannon V1 /sc:estimate**: Added 8-dimensional complexity (this version)
- **Future Shannon V2**: ML-based effort prediction, automated variance analysis

**Roadmap**:
- Historical pattern matching improvements
- Automated complexity scoring from code analysis
- Integration with time tracking tools for actual vs estimated comparison
- Team velocity tracking per developer
- Automatic re-estimation triggers on scope changes