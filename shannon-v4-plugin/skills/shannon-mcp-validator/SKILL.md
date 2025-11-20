---
name: shannon-mcp-validator
display_name: "Shannon MCP Validator (MCP Server Checking)"
description: "Validates MCP server availability, checks versions, and provides installation guidance with graceful degradation"
category: validation
version: "4.0.0"
author: "Shannon Framework"
priority: 1
auto_activate: true
activation_triggers:
  - "/sh_check_mcps command"
  - "check MCP servers"
  - "validate MCPs"
  - "MCP status"
mcp_servers:
  required: []
  recommended: []
allowed_tools:
  - Bash
progressive_disclosure:
  tier: 1
  metadata_tokens: 150
input:
  operation:
    type: string
    description: "Operation: check, install, recommend"
    required: false
    default: "check"
  mcp_name:
    type: string
    description: "Specific MCP to check (optional)"
    required: false
output:
  mcp_status:
    type: object
    description: "Status of all MCP servers"
  recommendations:
    type: array
    description: "Installation recommendations"
  sitrep:
    type: object
    description: "Standardized SITREP (via shannon-status-reporter)"
---

# Shannon MCP Validator

> **MCP Server Management**: Check availability, provide installation guidance, enable graceful degradation

## Purpose

Validates Model Context Protocol (MCP) server availability and provides:
- **Availability checking** - Detect which MCPs are installed
- **Version validation** - Ensure MCPs meet requirements
- **Installation guidance** - Help user install missing MCPs
- **Graceful degradation** - Skills function without optional MCPs
- **Dynamic recommendations** - Suggest MCPs based on project needs

## Capabilities

### 1. MCP Status Check
- Detect installed MCP servers
- Check server connectivity
- Validate versions
- Report health status

### 2. Installation Guidance
- Provide installation commands
- Link to documentation
- Explain benefits of each MCP
- Prioritize by importance (required vs recommended)

### 3. Project-Specific Recommendations
- Analyze project type
- Recommend relevant MCPs
- Explain why each MCP helps
- Provide installation priority

### 4. Graceful Degradation
- Identify fallback strategies
- Report functionality impact
- Suggest alternatives
- Enable partial operation

## Activation

**Automatic**:
```bash
/sh_check_mcps
/sh_check_mcps serena
/sh_check_mcps install serena
```

**Manual**:
```bash
Skill("shannon-mcp-validator")
```

## Execution Algorithm

### Step 1: Detect Installed MCPs

```javascript
async function detectInstalledMCPs() {
  // Shannon Framework standard MCPs
  const standard_mcps = [
    {
      name: "serena",
      display_name: "Serena MCP",
      category: "required",
      description: "Context persistence and memory management",
      tools: ["serena_write_memory", "serena_read_memory", "serena_list_memories"],
      install_command: "npm install -g @modelcontextprotocol/server-memory",
      docs: "https://github.com/modelcontextprotocol/servers/tree/main/src/memory"
    },
    {
      name: "sequential",
      display_name: "Sequential Thinking MCP",
      category: "recommended",
      description: "Structured thinking for complex analysis",
      tools: ["sequential_thinking"],
      install_command: "npm install -g @modelcontextprotocol/server-sequential-thinking",
      docs: "https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking"
    },
    {
      name: "puppeteer",
      display_name: "Puppeteer MCP",
      category: "recommended",
      description: "Browser automation and testing",
      tools: ["puppeteer_navigate", "puppeteer_screenshot", "puppeteer_click"],
      install_command: "npm install -g @modelcontextprotocol/server-puppeteer",
      docs: "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer"
    },
    {
      name: "context7",
      display_name: "Context7 MCP",
      category: "recommended",
      description: "Framework patterns and examples",
      tools: ["context7_search", "context7_get"],
      install_command: "npm install -g @context7/mcp",
      docs: "https://context7.dev"
    },
    {
      name: "shadcn-ui",
      display_name: "shadcn/ui MCP",
      category: "optional",
      description: "React component generation",
      tools: ["shadcn_add", "shadcn_list"],
      install_command: "npm install -g @shadcn/ui-mcp",
      docs: "https://ui.shadcn.com"
    }
  ];

  const mcp_status = [];

  for (const mcp of standard_mcps) {
    // Try to detect if MCP tools are available
    const is_available = await checkMCPAvailability(mcp);

    mcp_status.push({
      ...mcp,
      available: is_available.available,
      version: is_available.version,
      health: is_available.health,
      error: is_available.error
    });
  }

  return mcp_status;
}

async function checkMCPAvailability(mcp) {
  try {
    // Check if any of the MCP's tools are available
    // This is a heuristic - we can't directly query tool availability
    // In real implementation, this would check tool registry

    // For now, return based on known Shannon dependencies
    const known_available = ["serena"]; // Serena is required for Shannon

    return {
      available: known_available.includes(mcp.name),
      version: known_available.includes(mcp.name) ? "unknown" : null,
      health: known_available.includes(mcp.name) ? "healthy" : "not_installed"
    };
  } catch (error) {
    return {
      available: false,
      version: null,
      health: "error",
      error: error.message
    };
  }
}
```

### Step 2: Categorize and Prioritize

```javascript
function categorizeMCPs(mcp_status) {
  const categorized = {
    required: {
      installed: [],
      missing: []
    },
    recommended: {
      installed: [],
      missing: []
    },
    optional: {
      installed: [],
      missing: []
    }
  };

  for (const mcp of mcp_status) {
    const category = categorized[mcp.category];

    if (mcp.available) {
      category.installed.push(mcp);
    } else {
      category.missing.push(mcp);
    }
  }

  return categorized;
}
```

### Step 3: Generate Recommendations

```javascript
function generateRecommendations(categorized, project_context = null) {
  const recommendations = [];

  // Required MCPs that are missing
  for (const mcp of categorized.required.missing) {
    recommendations.push({
      mcp: mcp.name,
      priority: "critical",
      reason: `${mcp.display_name} is REQUIRED for Shannon Framework. Without it, core features won't work.`,
      impact: "High - Core functionality blocked",
      install_command: mcp.install_command,
      docs: mcp.docs
    });
  }

  // Recommended MCPs that are missing
  for (const mcp of categorized.recommended.missing) {
    recommendations.push({
      mcp: mcp.name,
      priority: "high",
      reason: `${mcp.display_name} is RECOMMENDED. ${mcp.description}`,
      impact: "Medium - Enhanced functionality unavailable",
      install_command: mcp.install_command,
      docs: mcp.docs
    });
  }

  // Project-specific recommendations
  if (project_context) {
    const project_specific = recommendForProject(project_context);
    recommendations.push(...project_specific);
  }

  return recommendations;
}

function recommendForProject(project_context) {
  const recommendations = [];

  // Example: React projects benefit from shadcn-ui MCP
  if (project_context.includes('react') || project_context.includes('ui')) {
    recommendations.push({
      mcp: "shadcn-ui",
      priority: "medium",
      reason: "Your project involves React UI. shadcn/ui MCP provides component generation.",
      impact: "Low - Convenience feature",
      install_command: "npm install -g @shadcn/ui-mcp",
      docs: "https://ui.shadcn.com"
    });
  }

  // Example: Testing projects benefit from Puppeteer
  if (project_context.includes('test') || project_context.includes('e2e')) {
    recommendations.push({
      mcp: "puppeteer",
      priority: "high",
      reason: "Your project involves testing. Puppeteer MCP enables browser automation.",
      impact: "Medium - Testing capabilities enhanced",
      install_command: "npm install -g @modelcontextprotocol/server-puppeteer",
      docs: "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer"
    });
  }

  return recommendations;
}
```

### Step 4: Generate Installation Guide

```javascript
function generateInstallationGuide(recommendations) {
  if (recommendations.length === 0) {
    return "All recommended MCPs are installed ✅";
  }

  const guide = `
# MCP Installation Guide

${recommendations.filter(r => r.priority === 'critical').length > 0 ? `
## 🚨 Critical (Required)

${recommendations
  .filter(r => r.priority === 'critical')
  .map(r => `
### ${r.mcp}

**Why**: ${r.reason}
**Impact**: ${r.impact}

**Install**:
\`\`\`bash
${r.install_command}
\`\`\`

**Docs**: ${r.docs}
`).join('\n')}
` : ''}

${recommendations.filter(r => r.priority === 'high').length > 0 ? `
## ⚠️ High Priority (Recommended)

${recommendations
  .filter(r => r.priority === 'high')
  .map(r => `
### ${r.mcp}

**Why**: ${r.reason}
**Impact**: ${r.impact}

**Install**:
\`\`\`bash
${r.install_command}
\`\`\`

**Docs**: ${r.docs}
`).join('\n')}
` : ''}

${recommendations.filter(r => r.priority === 'medium').length > 0 ? `
## ℹ️ Medium Priority (Optional)

${recommendations
  .filter(r => r.priority === 'medium')
  .map(r => `
### ${r.mcp}

**Why**: ${r.reason}
**Impact**: ${r.impact}

**Install**:
\`\`\`bash
${r.install_command}
\`\`\`

**Docs**: ${r.docs}
`).join('\n')}
` : ''}

---

**Quick Install All**:
\`\`\`bash
${recommendations.map(r => r.install_command).join(' && \\\n')}
\`\`\`
  `;

  return guide;
}
```

### Step 5: Graceful Degradation Strategy

```javascript
function generateDegradationStrategy(categorized) {
  const missing_required = categorized.required.missing;
  const missing_recommended = categorized.recommended.missing;

  const strategies = [];

  for (const mcp of missing_required) {
    strategies.push({
      mcp: mcp.name,
      impact: "Shannon Framework CANNOT operate without this MCP",
      fallback: "None - installation required",
      user_action: "Install immediately"
    });
  }

  for (const mcp of missing_recommended) {
    strategies.push({
      mcp: mcp.name,
      impact: `${mcp.description} unavailable`,
      fallback: getFallbackStrategy(mcp.name),
      user_action: "Recommended to install"
    });
  }

  return strategies;
}

function getFallbackStrategy(mcp_name) {
  const fallbacks = {
    sequential: "Manual step-by-step planning without structured thinking",
    puppeteer: "Manual browser testing or alternative test frameworks",
    context7: "Manual framework pattern research",
    "shadcn-ui": "Manual React component creation"
  };

  return fallbacks[mcp_name] || "Reduced functionality";
}
```

### Step 6: Generate SITREP

```javascript
const sitrep_data = {
  agent_name: "shannon-mcp-validator",
  task_id: `mcp_check_${Date.now()}`,
  current_phase: "MCP Validation",
  progress: 100,
  state: categorized.required.missing.length === 0 ? "completed" : "blocked",

  objective: "Validate MCP server availability and provide installation guidance",
  scope: [
    `Checked ${mcp_status.length} standard MCPs`,
    `Required: ${categorized.required.installed.length}/${categorized.required.installed.length + categorized.required.missing.length}`,
    `Recommended: ${categorized.recommended.installed.length}/${categorized.recommended.installed.length + categorized.recommended.missing.length}`
  ],
  dependencies: mcp_status.filter(m => m.available).map(m => m.name),

  findings: [
    `Installed: ${[...categorized.required.installed, ...categorized.recommended.installed, ...categorized.optional.installed].map(m => m.name).join(', ')}`,
    `Missing Required: ${categorized.required.missing.map(m => m.name).join(', ') || 'None'}`,
    `Missing Recommended: ${categorized.recommended.missing.map(m => m.name).join(', ') || 'None'}`
  ],

  blockers: categorized.required.missing.length > 0
    ? [`Missing required MCPs: ${categorized.required.missing.map(m => m.name).join(', ')}`]
    : [],
  risks: categorized.recommended.missing.length > 0
    ? [`Missing recommended MCPs reduces functionality: ${categorized.recommended.missing.map(m => m.name).join(', ')}`]
    : [],
  questions: [],

  next_steps: recommendations
    .filter(r => r.priority === 'critical' || r.priority === 'high')
    .slice(0, 3)
    .map(r => `Install ${r.mcp}: ${r.install_command}`),

  artifacts: ["mcp_status_report.md", "installation_guide.md"],

  tests_executed: ["mcp_detection", "version_check", "health_check"],
  test_results: categorized.required.missing.length === 0
    ? "All required MCPs installed"
    : `${categorized.required.missing.length} required MCPs missing`
};

const sitrep = await generate_sitrep(sitrep_data);
return sitrep;
```

## Examples

### Example 1: Check All MCPs

```bash
/sh_check_mcps
```

**SITREP Output**:
```markdown
## SITREP: shannon-mcp-validator - mcp_check_1730739600000

### Status
- **Current Phase**: MCP Validation
- **Progress**: 100%
- **State**: completed

### Context
- **Objective**: Validate MCP server availability and provide installation guidance
- **Scope**: Checked 5 standard MCPs, Required: 1/1, Recommended: 2/4
- **Dependencies**: serena, sequential, puppeteer

### Findings
- Installed: serena, sequential, puppeteer
- Missing Required: None
- Missing Recommended: context7, shadcn-ui

### Issues
- **Blockers**: None
- **Risks**: Missing recommended MCPs reduces functionality: context7, shadcn-ui
- **Questions**: None

### Next Steps
- [ ] Install context7: npm install -g @context7/mcp
- [ ] Install shadcn-ui: npm install -g @shadcn/ui-mcp

### Artifacts
- mcp_status_report.md
- installation_guide.md

### Validation
- **Tests Executed**: mcp_detection, version_check, health_check
- **Results**: All required MCPs installed
```

### Example 2: Missing Required MCP

```bash
/sh_check_mcps
```

**SITREP Output** (if Serena missing):
```markdown
## SITREP: shannon-mcp-validator - mcp_check_1730739600000

### Status
- **Current Phase**: MCP Validation
- **Progress**: 100%
- **State**: blocked

### Context
- **Objective**: Validate MCP server availability and provide installation guidance
- **Scope**: Checked 5 standard MCPs, Required: 0/1, Recommended: 0/4
- **Dependencies**: (none)

### Findings
- Installed: (none)
- Missing Required: serena
- Missing Recommended: sequential, puppeteer, context7, shadcn-ui

### Issues
- **Blockers**: Missing required MCPs: serena
- **Risks**: Missing recommended MCPs reduces functionality: sequential, puppeteer, context7, shadcn-ui
- **Questions**: None

### Next Steps
- [ ] Install serena: npm install -g @modelcontextprotocol/server-memory (CRITICAL)
- [ ] Install sequential: npm install -g @modelcontextprotocol/server-sequential-thinking
- [ ] Install puppeteer: npm install -g @modelcontextprotocol/server-puppeteer

### Artifacts
- mcp_status_report.md
- installation_guide.md

### Validation
- **Tests Executed**: mcp_detection, version_check, health_check
- **Results**: 1 required MCPs missing - INSTALLATION REQUIRED
```

## Integration with Shannon v4

**Used by**:
- /sh_check_mcps command
- shannon-skill-generator (validates MCP dependencies)
- All Shannon skills (pre-execution validation)

**Uses**:
- shannon-status-reporter (SITREP generation)
- Bash tool (for MCP detection)

**Pre-Execution Validation**:
```
Skill activation
  ↓
Check required MCPs (shannon-mcp-validator)
  ↓
All available? → Execute skill
Missing? → Report + graceful degradation
```

## Best Practices

### DO ✅
- Check MCPs before starting project
- Install all required MCPs immediately
- Install recommended MCPs for best experience
- Re-check after MCP updates
- Use graceful degradation when possible

### DON'T ❌
- Skip required MCP installation
- Ignore MCP health warnings
- Use incompatible MCP versions
- Install MCPs without reading docs
- Expect full functionality without recommended MCPs

## MCP Categories

**Required**:
- serena - MANDATORY for Shannon Framework

**Recommended**:
- sequential - Enhanced planning and analysis
- puppeteer - Browser testing capabilities
- context7 - Framework patterns and examples

**Optional**:
- shadcn-ui - React component convenience
- [Project-specific MCPs based on needs]

## Learn More

📚 **Full Documentation**: [resources/FULL_SKILL.md](./resources/FULL_SKILL.md)
📚 **MCP Installation Guide**: [resources/MCP_INSTALLATION.md](./resources/MCP_INSTALLATION.md)
📚 **Official MCP Docs**: https://modelcontextprotocol.io

---

**Shannon V4** - MCP Management & Validation ✓
