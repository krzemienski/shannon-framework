---
name: shannon-status-reporter
display_name: "Shannon Status Reporter (SITREP Generator)"
description: "Generates standardized SITREP (Situation Report) in exact specification format for all Shannon v4 components, enabling consistent communication across agents, skills, validation gates, and checkpoints"
category: reporting
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_status command"
  - "/sh_sitrep command"
  - "generate SITREP"
  - "status report requested"
  - "sitrep needed"
mcp_servers:
  required:
    - serena
allowed_tools:
  - Read
  - Glob
  - serena_write_memory
  - serena_read_memory
progressive_disclosure:
  tier: 1
  metadata_tokens: 200
input:
  agent_name:
    type: string
    required: true
    description: "Name of agent/skill generating report"
  task_id:
    type: string
    required: true
    description: "Unique task identifier"
  data:
    type: object
    required: true
    description: "Report data with all SITREP sections"
output:
  sitrep:
    type: string
    description: "Formatted SITREP in markdown"
  sitrep_id:
    type: string
    description: "Unique SITREP ID saved to Serena"
---

# Shannon Status Reporter (SITREP Generator)

> **Communication Protocol**: This skill implements Shannon v4's standardized SITREP (Situation Report) format for all system communication

## Purpose

Systematize the SITREP protocol across all Shannon Framework v4 components by:
- Generating SITREPs in **exact specification template format**
- Ensuring **consistent communication** across agents, skills, gates, checkpoints
- Providing **audit trail** through standardized reporting
- Enabling **context preservation** via SITREP storage in Serena MCP
- Serving as the **communication protocol** for the entire Shannon v4 system

**Key Innovation**: SITREP is not just documentation - it's how ALL Shannon components communicate.

## SITREP Template (from Shannon v4 Specification)

```markdown
## SITREP: [Agent Name] - [Task ID]

### Status
- **Current Phase**: [phase name]
- **Progress**: [percentage or milestone]
- **State**: [running|completed|blocked|failed]

### Context
- **Objective**: [what this agent is accomplishing]
- **Scope**: [boundaries of work]
- **Dependencies**: [other agents or resources needed]

### Findings
- [Key finding 1]
- [Key finding 2]
- [etc.]

### Issues
- **Blockers**: [items preventing progress]
- **Risks**: [potential problems identified]
- **Questions**: [clarifications needed]

### Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]

### Artifacts
- [Link to generated files, reports, etc.]

### Validation
- **Tests Executed**: [functional tests run]
- **Results**: [pass/fail with details]
```

## Capabilities

1. **SITREP Generation**: Create standardized reports from any component
2. **Template Validation**: Ensure all 7 sections present
3. **Markdown Formatting**: Clean, readable output
4. **Serena Integration**: Store SITREPs for audit trail
5. **Context Preservation**: Enable session resumption via SITREP history
6. **Multi-Component Support**: Works for agents, skills, gates, checkpoints

## When to Use

**Mandatory SITREP Generation**:
- After every wave completion (shannon-wave-orchestrator)
- At every validation gate (QualityGate hook)
- After every checkpoint creation (shannon-checkpoint-manager)
- After every phase plan generation (shannon-phase-planner)
- For all research agent reports
- For all sub-agent task completions

**Optional SITREP Generation**:
- User requests status via `/sh:status` or `/sh:sitrep`
- Mid-wave progress updates
- Ad-hoc status checks

## Execution Algorithm

### Step 1: Load Input Data

```javascript
const sitrep_data = {
  agent_name: "shannon-wave-orchestrator",
  task_id: "wave_1_execution",

  // Status section
  current_phase: "Implementation",
  progress: "75% (3/4 tasks complete)",
  state: "running",

  // Context section
  objective: "Execute Wave 1 tasks in parallel",
  scope: "4 independent tasks (database-schema, auth-system, ui-framework, api-design)",
  dependencies: ["spec_analysis", "phase_plan"],

  // Findings section
  findings: [
    "3/4 tasks completed successfully",
    "Task 4 (api-design) in progress",
    "Average execution time: 8 minutes per task"
  ],

  // Issues section
  blockers: [],
  risks: ["Task 4 may require additional 5 minutes"],
  questions: [],

  // Next Steps section
  next_steps: [
    "Complete Task 4 (api-design)",
    "Run Wave 1 validation gate",
    "Generate Wave 1 completion SITREP"
  ],

  // Artifacts section
  artifacts: [
    ".shannon/logs/wave_1_execution.log",
    "database/schema.sql",
    "auth/auth_system.ts",
    "components/ui_framework.tsx"
  ],

  // Validation section
  tests_executed: [
    "Database connection test",
    "Auth system unit test",
    "UI component render test"
  ],
  test_results: "3/3 tests passed"
};
```

### Step 2: Validate Input

```javascript
// Required sections (all must be present)
const REQUIRED_SECTIONS = [
  'agent_name',
  'task_id',
  'current_phase',
  'progress',
  'state',
  'objective',
  'scope',
  'dependencies',
  'findings',
  'blockers',
  'risks',
  'questions',
  'next_steps',
  'artifacts',
  'tests_executed',
  'test_results'
];

// Validate all sections present
for (const section of REQUIRED_SECTIONS) {
  if (sitrep_data[section] === undefined) {
    throw new Error(`SITREP invalid: missing required section '${section}'`);
  }
}

// Validate state is valid
const VALID_STATES = ['running', 'completed', 'blocked', 'failed'];
if (!VALID_STATES.includes(sitrep_data.state)) {
  throw new Error(`SITREP invalid: state must be one of ${VALID_STATES}`);
}
```

### Step 3: Generate SITREP in Exact Template Format

```javascript
const sitrep = `
## SITREP: ${sitrep_data.agent_name} - ${sitrep_data.task_id}

### Status
- **Current Phase**: ${sitrep_data.current_phase}
- **Progress**: ${sitrep_data.progress}
- **State**: ${sitrep_data.state}

### Context
- **Objective**: ${sitrep_data.objective}
- **Scope**: ${sitrep_data.scope}
- **Dependencies**: ${sitrep_data.dependencies.join(', ')}

### Findings
${sitrep_data.findings.map(f => `- ${f}`).join('\n')}

### Issues
- **Blockers**: ${sitrep_data.blockers.length > 0 ? sitrep_data.blockers.join(', ') : 'None'}
- **Risks**: ${sitrep_data.risks.length > 0 ? sitrep_data.risks.join(', ') : 'None'}
- **Questions**: ${sitrep_data.questions.length > 0 ? sitrep_data.questions.join(', ') : 'None'}

### Next Steps
${sitrep_data.next_steps.map(step => `- [ ] ${step}`).join('\n')}

### Artifacts
${sitrep_data.artifacts.map(a => `- ${a}`).join('\n')}

### Validation
- **Tests Executed**: ${sitrep_data.tests_executed.join(', ')}
- **Results**: ${sitrep_data.test_results}
`;

return sitrep.trim();
```

### Step 4: Save to Serena MCP

```javascript
// Generate unique SITREP ID
const timestamp = Date.now();
const sitrep_id = `sitrep_${sitrep_data.agent_name}_${sitrep_data.task_id}_${timestamp}`;

// Save SITREP to Serena
await serena_write_memory(sitrep_id, {
  timestamp: timestamp,
  agent_name: sitrep_data.agent_name,
  task_id: sitrep_data.task_id,
  sitrep_markdown: sitrep,
  sitrep_data: sitrep_data
});

// Update latest SITREP for agent
await serena_write_memory(`latest_sitrep_${sitrep_data.agent_name}`, sitrep_id);

// Append to SITREP history
const sitrep_history = await serena_read_memory("sitrep_history") || [];
sitrep_history.push({
  sitrep_id: sitrep_id,
  agent_name: sitrep_data.agent_name,
  task_id: sitrep_data.task_id,
  timestamp: timestamp,
  state: sitrep_data.state
});
await serena_write_memory("sitrep_history", sitrep_history);
```

### Step 5: Return SITREP

```javascript
return {
  sitrep: sitrep,
  sitrep_id: sitrep_id,
  success: true
};
```

## Usage Examples

### Example 1: Wave Execution SITREP

**Input**:
```javascript
{
  agent_name: "shannon-wave-orchestrator",
  task_id: "wave_1_execution",
  current_phase: "Implementation",
  progress: "100% (4/4 tasks complete)",
  state: "completed",
  objective: "Execute Wave 1 tasks in parallel",
  scope: "4 independent tasks",
  dependencies: ["spec_analysis", "phase_plan"],
  findings: [
    "All 4 tasks completed successfully",
    "Average execution time: 8.5 minutes per task",
    "Total wave duration: 12 minutes (parallel execution)",
    "Speedup: 2.8× vs sequential execution"
  ],
  blockers: [],
  risks: [],
  questions: [],
  next_steps: [
    "Run Wave 1 validation gate",
    "Generate validation SITREP",
    "Begin Wave 2 if validation passes"
  ],
  artifacts: [
    "database/schema.sql",
    "auth/auth_system.ts",
    "components/ui_framework.tsx",
    "api/api_design.ts",
    ".shannon/logs/wave_1_execution.log"
  ],
  tests_executed: [
    "Database connection test",
    "Auth system functionality test",
    "UI component render test",
    "API endpoint availability test"
  ],
  test_results: "4/4 tests passed"
}
```

**Output SITREP**:
```markdown
## SITREP: shannon-wave-orchestrator - wave_1_execution

### Status
- **Current Phase**: Implementation
- **Progress**: 100% (4/4 tasks complete)
- **State**: completed

### Context
- **Objective**: Execute Wave 1 tasks in parallel
- **Scope**: 4 independent tasks
- **Dependencies**: spec_analysis, phase_plan

### Findings
- All 4 tasks completed successfully
- Average execution time: 8.5 minutes per task
- Total wave duration: 12 minutes (parallel execution)
- Speedup: 2.8× vs sequential execution

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- [ ] Run Wave 1 validation gate
- [ ] Generate validation SITREP
- [ ] Begin Wave 2 if validation passes

### Artifacts
- database/schema.sql
- auth/auth_system.ts
- components/ui_framework.tsx
- api/api_design.ts
- .shannon/logs/wave_1_execution.log

### Validation
- **Tests Executed**: Database connection test, Auth system functionality test, UI component render test, API endpoint availability test
- **Results**: 4/4 tests passed
```

### Example 2: Validation Gate SITREP

**Input**:
```javascript
{
  agent_name: "quality-gate",
  task_id: "wave_1_validation",
  current_phase: "Implementation",
  progress: "Validation complete",
  state: "completed",
  objective: "Validate Wave 1 completion criteria",
  scope: "Functional tests for all Wave 1 outputs",
  dependencies: ["wave_1_execution"],
  findings: [
    "All functional tests passed",
    "Database schema valid and deployed",
    "Auth system functional with real authentication",
    "UI components render correctly in real browser",
    "API endpoints respond with expected data"
  ],
  blockers: [],
  risks: [],
  questions: [],
  next_steps: [
    "Generate checkpoint",
    "Proceed to Wave 2",
    "Continue Implementation phase"
  ],
  artifacts: [
    ".shannon/validation/wave_1_gate_results.json",
    ".shannon/logs/functional_tests_wave_1.log",
    "screenshots/ui_components_validated.png"
  ],
  tests_executed: [
    "Database schema validation (functional)",
    "Auth flow end-to-end test (real auth)",
    "UI component render test (real browser)",
    "API endpoint integration test (real HTTP)"
  ],
  test_results: "4/4 functional tests passed (NO MOCKS)"
}
```

**Output SITREP**:
```markdown
## SITREP: quality-gate - wave_1_validation

### Status
- **Current Phase**: Implementation
- **Progress**: Validation complete
- **State**: completed

### Context
- **Objective**: Validate Wave 1 completion criteria
- **Scope**: Functional tests for all Wave 1 outputs
- **Dependencies**: wave_1_execution

### Findings
- All functional tests passed
- Database schema valid and deployed
- Auth system functional with real authentication
- UI components render correctly in real browser
- API endpoints respond with expected data

### Issues
- **Blockers**: None
- **Risks**: None
- **Questions**: None

### Next Steps
- [ ] Generate checkpoint
- [ ] Proceed to Wave 2
- [ ] Continue Implementation phase

### Artifacts
- .shannon/validation/wave_1_gate_results.json
- .shannon/logs/functional_tests_wave_1.log
- screenshots/ui_components_validated.png

### Validation
- **Tests Executed**: Database schema validation (functional), Auth flow end-to-end test (real auth), UI component render test (real browser), API endpoint integration test (real HTTP)
- **Results**: 4/4 functional tests passed (NO MOCKS)
```

### Example 3: Checkpoint SITREP

**Input**:
```javascript
{
  agent_name: "shannon-checkpoint-manager",
  task_id: "checkpoint_wave_1_complete",
  current_phase: "Implementation",
  progress: "Checkpoint created",
  state: "completed",
  objective: "Create checkpoint after Wave 1 completion",
  scope: "Full project state snapshot",
  dependencies: ["wave_1_validation"],
  findings: [
    "Checkpoint created successfully",
    "All 8 required fields captured",
    "State saved to Serena MCP",
    "Knowledge graph entities created"
  ],
  blockers: [],
  risks: [],
  questions: [],
  next_steps: [
    "Continue to Wave 2",
    "Checkpoint available for restoration if needed"
  ],
  artifacts: [
    "checkpoint_myproject_1730832000000 (Serena MCP)"
  ],
  tests_executed: [
    "Checkpoint integrity validation",
    "Serena MCP persistence verification"
  ],
  test_results: "Checkpoint valid and restorable"
}
```

**Output SITREP**: (Similar format with checkpoint-specific details)

### Example 4: Research Agent SITREP

**Input**:
```javascript
{
  agent_name: "research-agent-mcp-servers",
  task_id: "research_mcp_ecosystem",
  current_phase: "Discovery",
  progress: "Research complete",
  state: "completed",
  objective: "Inventory MCP servers on host system",
  scope: "Scan, document capabilities, map to skills",
  dependencies: [],
  findings: [
    "7 MCP servers discovered",
    "Serena MCP: context persistence (required)",
    "Sequential MCP: structured thinking (recommended)",
    "shadcn-ui MCP: React components (recommended)",
    "Puppeteer MCP: browser automation (recommended)",
    "Context7 MCP: framework docs (optional)",
    "xcode MCP: iOS development (conditional)",
    "AWS MCP: deployment (conditional)"
  ],
  blockers: [],
  risks: ["xcode MCP not installed (required for iOS projects)"],
  questions: ["Should we auto-install missing MCP servers?"],
  next_steps: [
    "Map MCP capabilities to skill requirements",
    "Create installation guide for missing servers",
    "Integrate findings into skill definitions"
  ],
  artifacts: [
    "MCP_ECOSYSTEM_INVENTORY.md",
    "mcp_capabilities_matrix.csv"
  ],
  tests_executed: [
    "MCP server connectivity test",
    "Tool function availability verification"
  ],
  test_results: "7/7 servers reachable and functional"
}
```

## Integration with Shannon v4

### Command Integration

**User Command**:
```bash
/sh:status
/sh:sitrep
```

**Skill Activation**:
```
Command received
  ↓
shannon-status-reporter activates
  ↓
Loads current state from Serena
  ↓
Generates SITREP with current progress
  ↓
Returns formatted SITREP to user
```

### Sub-Agent Integration

**Agent Completion Flow**:
```
Agent completes task
  ↓
Agent calls shannon-status-reporter
  ↓
Passes task data
  ↓
SITREP generated in exact format
  ↓
SITREP saved to Serena
  ↓
SITREP returned to orchestrator
```

### Validation Gate Integration

**Gate Execution Flow**:
```
Validation gate executes functional tests
  ↓
Gate calls shannon-status-reporter
  ↓
Passes validation results
  ↓
Validation SITREP generated
  ↓
SITREP saved to audit trail
  ↓
SITREP used for pass/fail decision
```

### Checkpoint Integration

**Checkpoint Creation Flow**:
```
shannon-checkpoint-manager creates checkpoint
  ↓
Calls shannon-status-reporter
  ↓
Checkpoint data formatted as SITREP
  ↓
SITREP stored with checkpoint
  ↓
Session resumption uses SITREP to restore context
```

## SITREP Quality Standards

**Valid SITREP Must Include**:
- ✅ All 7 sections (Status, Context, Findings, Issues, Next Steps, Artifacts, Validation)
- ✅ State is one of: running, completed, blocked, failed
- ✅ Progress is measurable (percentage or milestone)
- ✅ Findings are specific and actionable
- ✅ Next steps are concrete action items
- ✅ Artifacts are linked/listed
- ✅ Validation section includes tests and results

**SITREP Storage**:
- Unique ID: `sitrep_{agent}_{task}_{timestamp}`
- Stored in Serena MCP
- Indexed in sitrep_history
- Latest SITREP for each agent tracked

## Anti-Patterns to Avoid

### ❌ DON'T: Use Free-Form Status Updates

**Wrong**:
```
Status: Everything is going well. Made some progress today.
```

**Why Wrong**: Not structured, not measurable, missing required sections

**Correct**: Use exact SITREP template with all 7 sections

### ❌ DON'T: Skip SITREP Sections

**Wrong**:
```markdown
## SITREP: my-agent - task1

### Status
- Progress: 50%

### Findings
- Did some work
```

**Why Wrong**: Missing 5 sections (Context, Issues, Next Steps, Artifacts, Validation)

**Correct**: Include all 7 sections (use "None" or empty arrays if no content)

### ❌ DON'T: Use Inconsistent Formatting

**Wrong**: Different agents use different formats

**Why Wrong**: Defeats purpose of standardized communication

**Correct**: Always use exact template from specification

### ❌ DON'T: Generate SITREPs Without Saving

**Wrong**:
```javascript
const sitrep = generate_sitrep(data);
return sitrep;  // Not saved to Serena
```

**Why Wrong**: Audit trail lost, session resumption not possible

**Correct**: Always save to Serena with unique ID

## Validation Rules

**SITREP Validation Checklist**:
1. ✅ All 7 sections present
2. ✅ State is valid (running|completed|blocked|failed)
3. ✅ Progress is measurable
4. ✅ Dependencies listed
5. ✅ Next steps are actionable
6. ✅ Artifacts are specified
7. ✅ Validation section includes tests and results
8. ✅ Saved to Serena with unique ID
9. ✅ Markdown formatted correctly

## Success Criteria

A successful SITREP generation satisfies:
- **Completeness**: All 7 sections populated
- **Clarity**: Status, progress, and next steps unambiguous
- **Consistency**: Follows exact template format
- **Persistence**: Saved to Serena for audit trail
- **Actionability**: Next steps are clear and executable
- **Validation**: Includes functional test results

---

**Shannon V4** - Standardized Communication Protocol via SITREP 📋
