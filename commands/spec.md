---
name: shannon:spec
description: Analyze specification using Shannon 8D complexity framework
usage: /shannon:spec "specification text" [--mcps] [--save]
---

# Specification Analysis Command

## Overview

Performs comprehensive specification analysis using Shannon's 8-dimensional complexity framework. Invokes the spec-analysis skill to generate objective complexity scores, domain breakdowns, and MCP recommendations.

## Prerequisites

- Specification text provided (minimum 20 words)
- Serena MCP available for saving results (check with `/shannon:check_mcps`)

## Workflow

### Step 1: Validate Input

Check specification provided:
- If missing: Display usage and request specification
- If < 20 words: Warn that analysis may be inaccurate

### Step 2: Invoke spec-analysis Skill

Use the `@skill spec-analysis` skill to perform analysis:

**Invocation:**
```
@skill spec-analysis
- Input: User's specification text
- Options:
  * include_mcps: true (if --mcps flag present, default: true)
  * save_to_serena: true (if --save flag present, default: true)
  * depth: "standard"
- Output: analysis_result
```

The spec-analysis skill will:
1. Parse specification
2. Apply 8D complexity algorithm
3. Classify domains
4. Generate MCP recommendations
5. Save to Serena MCP

### Step 3: Present Results

Format and display analysis results:

```markdown
📊 Shannon Specification Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Complexity: {complexity_score}/100 ({complexity_label})**

8D Breakdown:
├─ Structural:    {structural}/10
├─ Cognitive:     {cognitive}/15
├─ Coordination:  {coordination}/10
├─ Temporal:      {temporal}/10
├─ Technical:     {technical}/15
├─ Scale:         {scale}/15
├─ Uncertainty:   {uncertainty}/15
└─ Dependencies:  {dependencies}/10

Domain Breakdown:
{for each domain}
├─ {Domain}: {percentage}%

Risk Assessment: {risk_level}
Timeline Estimate: {estimated_timeline}
Team Size: {team_size_recommendation}

{if --mcps flag}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MCP Recommendations:

Required:
{for each required MCP}
  ✅ {mcp_name}
     Purpose: {purpose}
     Setup: /shannon:check_mcps --setup {mcp_name}

Recommended:
{for each recommended MCP}
  📦 {mcp_name}
     Purpose: {purpose}
     Setup: /shannon:check_mcps --setup {mcp_name}

Conditional:
{for each conditional MCP}
  ⚙️  {mcp_name}
     Trigger: {trigger_condition}
     Setup: /shannon:check_mcps --setup {mcp_name}
{end if}

{if saved_to_serena}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Analysis saved to Serena MCP
Key: {serena_key}
Restore: /shannon:restore {timestamp}
{else}
⚠️  Analysis not saved (Serena MCP unavailable)
Run: /shannon:check_mcps for setup instructions
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
{if complexity < 30}
- Proceed with direct implementation
- Run /shannon:test to create functional tests

{else if complexity < 50}
- Generate implementation plan: @skill phase-planning
- Consider wave execution for parallelization

{else}
- Generate phase plan: @skill phase-planning
- Generate wave plan: @skill wave-orchestration
- Multi-agent execution recommended
- Create checkpoint: /shannon:checkpoint before-implementation
{end if}
```

### Step 4: Update Command Documentation

Keep backward compatibility notes in command file:

```markdown
## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same required arguments
- Compatible output format
- Enhanced with --mcps flag (opt-in)

**Changes from V3:**
- Internal: Now uses spec-analysis skill (was monolithic)
- Enhancement: Better MCP recommendations
- Enhancement: Improved Serena MCP integration
- No breaking changes
```

## Output Format

[Output format section above]

## Skill Dependencies

- spec-analysis (REQUIRED)

## MCP Dependencies

- Serena MCP (required for --save, recommended always)
- Sequential MCP (recommended for complex specs)
