---
name: sh_check_mcps
description: Verify MCP configuration and provide setup guidance
usage: /sh_check_mcps [--install-guide] [--fix]
---

# MCP Server Configuration Checker Command

## Overview

Verifies MCP server availability and provides detailed setup guidance through delegation to the mcp-discovery skill. Uses quantitative domain analysis to recommend appropriate MCPs with tier-based prioritization.

## Prerequisites

None (this command helps establish prerequisites)

## Workflow

### Step 1: Determine Check Type

Parse command arguments:

**Check Types:**
- No arguments → Full MCP verification with recommendations
- `--install-guide` → Show only installation instructions
- `--fix` → Interactive setup assistance
- `--serena-only` → Check only critical Serena MCP

### Step 2: Analyze Project Domains (if available)

If project context exists, estimate domain breakdown:

**Domain Estimation:**
```
IF project files accessible:
  - Count frontend files (React, Vue, etc.) → Frontend %
  - Count backend files (Express, FastAPI, etc.) → Backend %
  - Count database files (migrations, queries) → Database %
ELSE:
  - Use generic recommendations (Serena mandatory, common secondaries)
```

### Step 3: Invoke mcp-discovery Skill

Delegate to `@skill mcp-discovery` for recommendations:

**For Full Check:**
```
@skill mcp-discovery
- Input:
  * mode: "recommend"
  * domain_breakdown: {
      frontend: {frontend_percentage},
      backend: {backend_percentage},
      database: {database_percentage}
    }
  * include_health_checks: true
  * include_setup_guide: true
- Output: mcp_recommendations
```

**For Health Check:**
```
@skill mcp-discovery
- Input:
  * mode: "health_check"
  * recommended_mcps: {mcps from domain analysis}
- Output: health_status
```

**For Fallback Recommendations:**
```
@skill mcp-discovery
- Input:
  * mode: "fallback"
  * unavailable_mcp: "{mcp_name}"
- Output: fallback_chain
```

### Step 4: Present Results

Format skill output for user display:

```markdown
═══════════════════════════════════════════════════════════════
🔍 SHANNON MCP SERVER VERIFICATION
═══════════════════════════════════════════════════════════════

🔴 TIER 1: MANDATORY SERVERS
───────────────────────────────────────────────────────────────

{for each mandatory MCP}
{if operational}
✅ {mcp_name} - CONNECTED
   Version: {version}
   Status: Operational
   Tools Available: {tools_list}
{else}
❌ {mcp_name} - NOT FOUND
   Status: CRITICAL - Shannon cannot function without {mcp_name}
   Purpose: {purpose}

   📦 Installation:
   {installation_command}

   ⚙️  Configuration:
   {configuration_json}

   ✓ Verification:
   {health_check_command}

   📚 Documentation:
   {documentation_url}
{end if}
{end for}

🟡 TIER 2: PRIMARY SERVERS
───────────────────────────────────────────────────────────────

{for each primary MCP}
{if operational}
✅ {mcp_name} - CONNECTED
   Rationale: {domain} {percentage}% >= 20% threshold
   Status: Operational
   Tools Available: {tools_list}
{else}
⚠️  {mcp_name} - NOT FOUND
   Status: Recommended - {purpose}
   Rationale: {domain} {percentage}% >= 20% threshold
   Impact: {impact_description}

   📦 Installation:
   {installation_command}

   ⚙️  Configuration:
   {configuration_json}

   🔄 Fallback Chain:
   {fallback_chain}

   📚 Documentation:
   {documentation_url}
{end if}
{end for}

🟢 TIER 3: SECONDARY SERVERS
───────────────────────────────────────────────────────────────

{for each secondary MCP}
{status and details similar to primary}
{end for}

───────────────────────────────────────────────────────────────
📊 SUMMARY
───────────────────────────────────────────────────────────────

Required:     {mandatory_available}/{mandatory_total} available
Primary:      {primary_available}/{primary_total} available
Secondary:    {secondary_available}/{secondary_total} available

{if any mandatory missing}
🚨 CRITICAL: {missing_mandatory_list} must be configured
{else if any primary missing}
⚠️  FUNCTIONAL: {missing_primary_list} recommended for best experience
{else}
✅ ALL SYSTEMS OPERATIONAL
{end if}

💡 After configuring MCPs, run /sh_status to verify full Shannon functionality

═══════════════════════════════════════════════════════════════
```

### Step 5: Provide Next Steps

Based on health check results:

**If Serena Missing (Critical):**
```markdown
🚨 IMMEDIATE ACTION REQUIRED

Serena MCP is MANDATORY for Shannon Framework.

**Quick Setup**:
1. Install: {installation_command}
2. Configure: Add to Claude Code settings
3. Restart: Claude Code
4. Verify: /sh_check_mcps

Without Serena, Shannon commands will fail.
```

**If Primary MCPs Missing:**
```markdown
⚠️  RECOMMENDED SETUP

Missing Primary MCPs affect core functionality:
{for each missing primary}
- {mcp_name}: {purpose}
  Impact: {impact_description}
{end for}

Setup Order:
1. Install missing Primary MCPs
2. Verify each: {health_check_command}
3. Confirm: /sh_check_mcps
```

## Backward Compatibility

**V3 Compatibility:** ✅ Maintained
- Same command syntax
- Same output format structure
- Enhanced with quantitative domain analysis

**Changes from V3:**
- Internal: Now uses mcp-discovery skill (was hardcoded checks)
- Enhancement: Tier-based recommendations (MANDATORY/PRIMARY/SECONDARY)
- Enhancement: Quantitative domain analysis (Frontend %, Backend %)
- Enhancement: Fallback chain recommendations from domain-mcp-matrix.json
- Enhancement: Health check workflow generation
- No breaking changes to user interface

## Skill Dependencies

- mcp-discovery (REQUIRED)

## MCP Dependencies

None (this command helps establish MCP dependencies)

## Common Issues

**Issue: "Tool not found" errors**
- Cause: Required MCP not configured
- Solution: Run /sh_check_mcps, follow setup instructions

**Issue: "Serena connection failed"**
- Cause: Serena MCP configured but not responding
- Solution: Restart Claude Code, verify SERENA_PROJECT_ROOT

**Issue: "Threshold gaming" (Frontend 19.9%)**
- Detection: User tries to avoid testing by staying below 20%
- Response: Apply threshold margin (±1%), enforce Shannon testing requirements
