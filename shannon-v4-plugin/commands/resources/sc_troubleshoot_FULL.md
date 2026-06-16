# /sc:troubleshoot Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:troubleshoot Command

> **Enhanced from SuperClaude's /troubleshoot with Shannon V3 structured debugging framework and evidence-based investigation.**

## Purpose Statement

Transform ad-hoc debugging into systematic, evidence-based root cause analysis. The `/sc:troubleshoot` command activates structured investigation workflows that:

- **Identify Root Causes**: Systematic investigation from symptoms to underlying issues
- **Track Evidence Chains**: Maintain verifiable evidence trails via Serena MCP
- **Apply Debugging Frameworks**: Five Whys, causal chain analysis, hypothesis testing
- **Deliver Actionable Fixes**: Clear remediation steps with validation criteria
- **Preserve Investigation Context**: Store findings for future reference and learning

**Base Capability**: SuperClaude's problem investigation and troubleshooting
**Shannon Enhancement**: Structured debugging methodology, evidence tracking, systematic root cause analysis

## Command Signature

```bash
/sc:troubleshoot [symptoms] [options]

# Basic usage
/sc:troubleshoot "authentication randomly fails"

# With scope specification
/sc:troubleshoot "API slow" --scope backend

# With evidence preservation
/sc:troubleshoot "deployment errors" --save-investigation

# With wave debugging
/sc:troubleshoot "system-wide performance issues" --wave-debug
```

## Shannon V3 Enhancements

### 1. Structured Debugging Framework

**Systematic Investigation Process**:
```yaml
Phase 1: Symptom Documentation (10%)
  → Record observable symptoms
  → Gather initial evidence
  → Define investigation scope

Phase 2: Evidence Collection (25%)
  → Read relevant code
  → Grep for patterns
  → Review logs and configs
  → Check existing tests

Phase 3: Hypothesis Formation (20%)
  → Generate testable hypotheses
  → Prioritize by likelihood
  → Design verification tests

Phase 4: Root Cause Analysis (30%)
  → Execute verification tests
  → Apply Five Whys method
  → Build causal chain
  → Validate root cause

Phase 5: Fix Recommendation (15%)
  → Design remediation
  → Validate fix approach
  → Document implementation steps
  → Define success criteria
```

### 2. Evidence Tracking via Serena MCP

**Memory Structure**:
```javascript
// Investigation Memory Schema
{
  investigation_id: "troubleshoot_[timestamp]_[issue_hash]",
  symptom: "Observable problem description",
  evidence_chain: [
    {
      type: "observation|code|log|test",
      source: "file:line or command",
      finding: "What was discovered",
      timestamp: "when collected"
    }
  ],
  hypotheses: [
    {
      hypothesis: "Testable explanation",
      status: "pending|validated|refuted",
      evidence: "Supporting or refuting evidence",
      verification_method: "How it was tested"
    }
  ],
  root_cause: "Underlying issue identified",
  causal_chain: "Symptom ← Proximate ← Contributing ← Root",
  fix_recommendation: {
    approach: "Remediation strategy",
    steps: ["Implementation steps"],
    validation: ["How to verify fix"],
    risks: ["Potential issues"]
  }
}
```

**Memory Operations**:
```bash
# Start investigation
write_memory("investigation_start", symptom_details)

# Log evidence as collected
write_memory("evidence_auth_code", code_findings)
write_memory("evidence_auth_logs", log_analysis)

# Document hypotheses
write_memory("hypothesis_token_expiry", test_results)

# Store root cause
write_memory("root_cause_analysis", causal_chain)

# Save fix recommendation
write_memory("fix_recommendation", remediation_plan)
```

### 3. Root Cause Analysis Framework

**Five Whys Method** (Sequential MCP assisted):
```
Symptom: Login fails randomly

Why? → Token validation fails intermittently
Evidence: Grep "validateToken" shows try/catch with silent failure

Why? → Token signature verification throws error
Evidence: Read auth.js:45 shows JWT.verify without error handling

Why? → Secret key changes between requests
Evidence: Grep "JWT_SECRET" shows process.env in middleware

Why? → Environment variable reloaded on each request
Evidence: Read middleware/auth.js shows dotenv.config() in function

Why? → Dotenv config called in middleware instead of app initialization
Root Cause: Environment loading in hot path causes race conditions

Causal Chain:
Login fails ← Token invalid ← Signature mismatch ← Secret key changes ← Dotenv in middleware ← [ROOT CAUSE]
```

**Verification Requirements**:
- Each "Why?" must have verifiable evidence
- Evidence must be traceable to source (file:line, log entry, test result)
- Root cause must be actionable
- Causal chain must be logically sound

## Usage Patterns

### Pattern 1: Bug Investigation

```bash
/sc:troubleshoot "form submission fails on production"

# Activates:
# 1. ANALYZER agent for systematic investigation
# 2. Evidence collection via Read, Grep, Glob
# 3. Hypothesis testing with Sequential MCP
# 4. Root cause identification
# 5. Fix recommendation with validation
```

**Investigation Flow**:
1. Document symptom and context
2. Collect evidence from code, logs, configs
3. Form hypotheses about potential causes
4. Test hypotheses systematically
5. Identify root cause via Five Whys
6. Recommend fix with validation criteria
7. Save investigation to Serena

### Pattern 2: Performance Debugging

```bash
/sc:troubleshoot "API response time degraded" --scope backend --save-investigation

# Enhanced with:
# - Performance profiling analysis
# - Bottleneck identification
# - Resource usage examination
# - Optimization recommendations
```

**Specialized Analysis**:
- Database query patterns (N+1, missing indexes)
- Algorithm complexity (O(n²) operations)
- Resource bottlenecks (CPU, memory, I/O)
- Network latency (external APIs, DNS)
- Concurrency issues (race conditions, deadlocks)

### Pattern 3: System-Wide Issues

```bash
/sc:troubleshoot "intermittent 500 errors across services" --wave-debug

# Wave Strategy:
# Wave 1: Review - Survey all services
# Wave 2: Analyze - Investigate error patterns
# Wave 3: Root Cause - Identify common cause
# Wave 4: Fix - Implement remediation
# Wave 5: Validate - Verify resolution
```

### Pattern 4: Deployment Failures

```bash
/sc:troubleshoot "CI/CD pipeline fails on deploy step"

# Investigation areas:
# - Pipeline configuration
# - Environment variables
# - Dependency resolution
# - Build artifacts
# - Deployment scripts
```

## Execution Flow

### Standard Execution

```yaml
Step 1: Initialize Investigation
  → activate_agent: ANALYZER
  → read_memory: Check for previous investigations
  → write_memory: Start new investigation record

Step 2: Symptom Documentation
  → Record observable symptoms
  → Gather reproduction steps
  → Note environmental context
  → Define investigation scope

Step 3: Evidence Collection
  → Read relevant files
  → Grep for patterns and keywords
  → Glob for related files
  → Review logs and error messages
  → Check test coverage
  → write_memory: Log all evidence

Step 4: Hypothesis Formation
  → Generate 3-5 testable hypotheses
  → Prioritize by likelihood and impact
  → Design verification tests
  → write_memory: Document hypotheses

Step 5: Hypothesis Testing
  → Execute verification tests
  → Collect results
  → Validate or refute each hypothesis
  → write_memory: Update hypothesis status

Step 6: Root Cause Analysis
  → Apply Five Whys method (Sequential MCP)
  → Build causal chain
  → Verify root cause is actionable
  → write_memory: Document root cause

Step 7: Fix Recommendation
  → Design remediation strategy
  → Define implementation steps
  → Specify validation criteria
  → Identify potential risks
  → write_memory: Save fix recommendation

Step 8: Report Generation
  → Summarize investigation
  → Present evidence chain
  → Explain root cause
  → Detail fix recommendation
  → Provide validation checklist
```

### Wave Debugging Mode

**Activation**: `--wave-debug` flag or complex system-wide issues

```yaml
Wave 1: Survey & Document
  Goal: Map problem scope
  Activities:
    - Document all symptoms
    - Identify affected systems
    - Collect initial evidence
  Deliverable: Problem scope document

Wave 2: Deep Investigation
  Goal: Gather comprehensive evidence
  Activities:
    - Systematic code review
    - Log analysis
    - Configuration audit
    - Test coverage review
  Deliverable: Evidence repository

Wave 3: Root Cause Analysis
  Goal: Identify underlying issue
  Activities:
    - Hypothesis generation
    - Systematic testing
    - Five Whys analysis
    - Causal chain construction
  Deliverable: Root cause report

Wave 4: Fix Design
  Goal: Design remediation
  Activities:
    - Solution design
    - Risk assessment
    - Implementation planning
    - Validation strategy
  Deliverable: Fix recommendation

Wave 5: Validation
  Goal: Verify resolution approach
  Activities:
    - Test fix feasibility
    - Validate assumptions
    - Review with stakeholders
  Deliverable: Validated fix plan
```

## ANALYZER Agent Integration

### Agent Activation

The `/sc:troubleshoot` command **automatically activates** the ANALYZER agent:

```yaml
Agent: ANALYZER
Role: Lead investigator
Responsibilities:
  - Systematic evidence collection
  - Pattern recognition
  - Hypothesis testing
  - Root cause identification
  - Fix recommendation

Tools Available:
  - Read: Code examination
  - Grep: Pattern searching
  - Glob: File discovery
  - Sequential: Complex analysis
  - Serena: Evidence tracking
  - Bash: Log/system inspection
```

### Investigation Workflow

```
User Command: /sc:troubleshoot "database connection timeout"
    ↓
Activate ANALYZER Agent
    ↓
Phase 1: Symptom Documentation
  ANALYZER: Document symptoms and context
    ↓
Phase 2: Evidence Collection
  ANALYZER → Read: db.js, config.js
  ANALYZER → Grep: "connection|timeout|pool"
  ANALYZER → Bash: Check logs
  ANALYZER → write_memory: evidence_collection
    ↓
Phase 3: Hypothesis Formation
  ANALYZER → Sequential: Analyze patterns
  ANALYZER → write_memory: hypotheses
    ↓
Phase 4: Hypothesis Testing
  ANALYZER: Test each hypothesis
  ANALYZER → write_memory: test_results
    ↓
Phase 5: Root Cause Analysis
  ANALYZER → Sequential: Five Whys
  ANALYZER → write_memory: root_cause
    ↓
Phase 6: Fix Recommendation
  ANALYZER: Design remediation
  ANALYZER → write_memory: fix_plan
    ↓
Generate Investigation Report
```

## Output Format

### Standard Investigation Report

```markdown
# Investigation Report: [Symptom]

## Executive Summary
**Problem**: [Concise problem statement]
**Root Cause**: [Identified underlying issue]
**Recommendation**: [Fix approach]
**Priority**: Critical|High|Medium|Low
**Estimated Effort**: [Time estimate]

## Symptom Documentation
**Observable Symptoms**:
- [Symptom 1]
- [Symptom 2]

**Context**:
- Environment: [Production|Staging|Dev]
- Frequency: [Always|Intermittent|Rare]
- Impact: [Users affected, data at risk]

**Reproduction Steps**:
1. [Step 1]
2. [Step 2]

## Evidence Chain

### Evidence 1: [Type]
**Source**: file.js:45 or log:timestamp
**Finding**: [What was discovered]
**Relevance**: [How it relates to problem]

### Evidence 2: [Type]
**Source**: [Location]
**Finding**: [Discovery]
**Relevance**: [Connection]

## Hypothesis Testing

### Hypothesis 1: [Explanation]
**Status**: ✅ Validated | ❌ Refuted | ⏳ Pending
**Evidence**: [Supporting/refuting evidence]
**Verification Method**: [How tested]

### Hypothesis 2: [Explanation]
**Status**: [Status]
**Evidence**: [Evidence]
**Verification Method**: [Method]

## Root Cause Analysis

### Five Whys
**Symptom**: [Observable problem]

**Why?** → [First level cause]
Evidence: [Verification]

**Why?** → [Second level cause]
Evidence: [Verification]

**Why?** → [Third level cause]
Evidence: [Verification]

**Why?** → [Fourth level cause]
Evidence: [Verification]

**Why?** → [Fifth level cause]
**Root Cause**: [Underlying issue]

### Causal Chain
```
[Symptom] ← [Proximate] ← [Contributing] ← [Underlying] ← [ROOT CAUSE]
```

## Fix Recommendation

### Approach
[High-level fix strategy]

### Implementation Steps
1. [Step 1 with file/code references]
2. [Step 2 with validation criteria]
3. [Step 3 with rollback plan]

### Validation Criteria
- [ ] [Verification step 1]
- [ ] [Verification step 2]
- [ ] [Verification step 3]

### Risks & Mitigation
**Risk**: [Potential issue]
**Mitigation**: [How to handle]

**Risk**: [Potential issue]
**Mitigation**: [How to handle]

### Rollback Plan
[Steps to revert if fix causes issues]

## Investigation Metadata
**Investigation ID**: troubleshoot_[timestamp]_[hash]
**Duration**: [Time taken]
**Files Examined**: [Count and list]
**Tests Run**: [Count]
**Serena Memory**: Saved to investigation_[id]
```

## Examples

### Example 1: Authentication Bug

```bash
/sc:troubleshoot "users randomly logged out"

# Output:
Investigation Report: Random User Logouts

## Executive Summary
Problem: Users randomly logged out mid-session
Root Cause: Session timeout configuration mismatch between frontend and backend
Recommendation: Synchronize session timeout values
Priority: High
Estimated Effort: 2 hours

## Evidence Chain

Evidence 1: Frontend Code
Source: src/auth/session.js:23
Finding: Frontend session timeout = 30 minutes
Relevance: Shorter than backend timeout

Evidence 2: Backend Config
Source: config/session.js:15
Finding: Backend session timeout = 60 minutes
Relevance: Longer than frontend expects

Evidence 3: User Reports
Source: Support tickets #234, #245, #267
Finding: Logouts occur ~30 minutes into session
Relevance: Matches frontend timeout

## Root Cause Analysis

Five Whys:
Symptom: Users logged out unexpectedly

Why? → Session expires prematurely
Evidence: Logout occurs at 30-minute mark

Why? → Frontend invalidates session at 30 minutes
Evidence: session.js:23 shows 30-minute timeout

Why? → Frontend and backend timeouts don't match
Evidence: Backend config shows 60-minute timeout

Why? → Configuration values set independently
Evidence: No shared config source

Root Cause: Session timeout configuration drift between frontend and backend

## Fix Recommendation

Approach: Centralize session timeout configuration

Implementation Steps:
1. Create shared config constant (SESSION_TIMEOUT = 60 minutes)
2. Update frontend to use shared constant
3. Update backend to use shared constant
4. Add validation tests for timeout synchronization

Validation Criteria:
- [✓] Frontend and backend use same timeout value
- [✓] Users remain logged in for full 60 minutes
- [✓] No premature logout reports for 7 days

Investigation Metadata:
Investigation ID: troubleshoot_20240115_auth_logout
Files Examined: 8 (session.js, auth.js, config files)
Serena Memory: investigation_auth_logout
```

### Example 2: Performance Issue

```bash
/sc:troubleshoot "API response time degraded" --scope backend

# Output:
Investigation Report: API Performance Degradation

## Root Cause Analysis

Five Whys:
Symptom: API response time increased from 200ms to 3000ms

Why? → Database queries taking 2.5s average
Evidence: Query logs show 2500ms average response time

Why? → N+1 query pattern on /users endpoint
Evidence: Grep shows 1 query + N relationship queries

Why? → Relationships not eagerly loaded
Evidence: User.findAll() without include statements

Why? → Eager loading removed in recent refactor
Evidence: Git diff shows include removal in commit abc123

Root Cause: Accidental removal of eager loading in refactoring

## Fix Recommendation

Approach: Restore eager loading with proper includes

Implementation Steps:
1. Restore include: [{ model: Role }, { model: Permissions }]
2. Add database query monitoring
3. Add regression test for query count
4. Document eager loading requirement

Validation Criteria:
- [✓] Response time < 300ms
- [✓] Query count = 1 (not N+1)
- [✓] Test prevents future regression
```

## Integration with Shannon V3

### Wave Orchestration Integration

**Wave-Enabled Debugging**:
- Activate with `--wave-debug` flag
- Automatic wave strategy selection based on complexity
- Progressive investigation depth across waves
- Cross-wave evidence accumulation

**Wave Progression**:
```
Wave 1 (Survey) → Evidence collection
Wave 2 (Investigate) → Hypothesis testing
Wave 3 (Analyze) → Root cause identification
Wave 4 (Design) → Fix recommendation
Wave 5 (Validate) → Solution verification
```

### Hook System Integration

**Available Hooks**:
- `troubleshoot:before` - Pre-investigation setup
- `troubleshoot:evidence-collected` - After evidence gathering
- `troubleshoot:hypothesis-tested` - After each hypothesis test
- `troubleshoot:root-cause-found` - Root cause identified
- `troubleshoot:fix-recommended` - Fix designed
- `troubleshoot:after` - Investigation complete

### Project Memory Integration

**Memory Storage**:
```javascript
// Investigation stored in Serena
write_memory("investigation_[issue]", {
  symptom: "Problem description",
  evidence: [...],
  hypotheses: [...],
  root_cause: "...",
  fix: {...}
})

// Retrieve for similar issues
read_memory("investigation_*") // Find related investigations
```

**Learning from History**:
- Similar symptom detection
- Reusable debugging strategies
- Common root cause patterns
- Validated fix approaches

## Best Practices

### Investigation Discipline

✅ **DO**:
- Document symptoms before investigating
- Collect evidence systematically
- Form testable hypotheses
- Verify each step of causal chain
- Save investigation to Serena
- Provide actionable fix recommendations

❌ **DON'T**:
- Jump to conclusions without evidence
- Skip hypothesis testing
- Recommend fixes without root cause
- Ignore contradictory evidence
- Fail to document investigation

### Evidence Quality

**High-Quality Evidence**:
- Traceable to source (file:line, log:timestamp)
- Verifiable by others
- Directly relevant to problem
- Timestamped and contextualized

**Poor Evidence**:
- Assumptions without verification
- Hearsay or speculation
- Irrelevant findings
- Untraceable sources

### Root Cause Validation

**Valid Root Cause Criteria**:
- Actionable (can be fixed)
- Verifiable (supported by evidence)
- Logical (explains all symptoms)
- Fundamental (not just a symptom)

**Root Cause Checklist**:
- [ ] If fixed, would symptoms disappear?
- [ ] Is it the deepest causal level we can act on?
- [ ] Does evidence conclusively support it?
- [ ] Can we verify the fix works?

## Performance Standards

**Investigation Metrics**:
- Time to root cause: < 2 hours for focused issues
- Evidence quality: 100% traceable and verifiable
- Hypothesis accuracy: > 70% validation rate
- Fix success rate: > 90% effective on first implementation

**Quality Gates**:
- All evidence must be logged to Serena
- Root cause must pass validation checklist
- Fix must include validation criteria
- Investigation report must be complete

## Command Success Criteria

An investigation is complete when:
- ✅ Root cause identified and validated
- ✅ Evidence chain documented in Serena
- ✅ Fix recommendation provided with implementation steps
- ✅ Validation criteria defined
- ✅ Investigation report generated
- ✅ Rollback plan documented

## Next Steps

**For Users**:
1. Use `/sc:troubleshoot [symptoms]` for systematic debugging
2. Review investigation reports for root cause and fix
3. Access stored investigations via Serena for learning

**For Integration**:
- Works with `/sc:analyze` for pre-investigation analysis
- Feeds into `/sc:implement` for fix implementation
- Coordinates with TEST_GUARDIAN for validation
- Integrates with wave debugging for complex issues

**Documentation**:
- See ANALYZER.md for detailed agent capabilities
- See WAVE_ORCHESTRATION.md for wave debugging
- See PROJECT_MEMORY.md for Serena integration