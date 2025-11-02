# /sh_check_mcps - MCP Server Configuration Checker - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sh_check_mcps - MCP Server Configuration Checker

Comprehensive MCP server verification with step-by-step setup instructions for missing or misconfigured servers.

## Purpose

Shannon Framework requires specific MCP servers to function. This command:
- Checks for required and recommended MCP servers
- Verifies server connectivity and tool availability
- Provides detailed setup instructions for missing servers
- Guides users through MCP configuration process
- Troubleshoots common MCP issues

## Usage

```bash
/sh_check_mcps                  # Complete MCP check with setup guidance
/sh_check_mcps --install-guide  # Show only installation instructions
/sh_check_mcps --serena-only    # Check only critical Serena MCP
/sh_check_mcps --fix            # Interactive setup assistance
```

## MCP Requirements

### Required MCPs (Critical)

**Serena MCP** - MANDATORY
- **Purpose**: Context preservation, checkpoint/restore, project memory
- **Why Critical**: Shannon cannot function without context preservation
- **Impact if Missing**: Shannon commands will fail with errors
- **Tools Used**: list_memories, write_memory, read_memory, create_entities, search_nodes

### Recommended MCPs (Strongly Advised)

**Sequential MCP**
- **Purpose**: Complex multi-step reasoning and analysis
- **Impact**: Reduced analysis quality, no deep reasoning support
- **Tools Used**: sequentialthinking

**Context7 MCP**
- **Purpose**: Official framework patterns and documentation
- **Impact**: Less guidance on framework-specific implementations
- **Tools Used**: resolve-library-id, get-library-docs

**Puppeteer MCP**
- **Purpose**: Real browser testing for NO MOCKS philosophy
- **Impact**: Cannot perform browser automation and E2E testing
- **Tools Used**: puppeteer_navigate, puppeteer_screenshot, puppeteer_click, puppeteer_fill

### Conditional MCPs

**shadcn-ui MCP**
- **Purpose**: React/Next.js UI components from shadcn/ui library
- **Required For**: React/Next.js projects only
- **Shannon Enforcement**: Shannon REQUIRES shadcn for all React UI work
- **Tools Used**: get_component, list_components, get_block, list_blocks
- **Package**: @jpisnice/shadcn-ui-mcp-server

## Example Output

```
═══════════════════════════════════════════════════════════════
🔍 SHANNON MCP SERVER VERIFICATION
═══════════════════════════════════════════════════════════════

🔴 REQUIRED SERVERS
───────────────────────────────────────────────────────────────

❌ Serena MCP - NOT FOUND
   Status: CRITICAL - Shannon cannot function without Serena
   Purpose: Context preservation, checkpoint/restore, project memory
   Tools Missing: list_memories, write_memory, read_memory

   📦 Installation:
   npm install -g @modelcontextprotocol/server-serena

   ⚙️  Configuration (add to Claude Code settings):
   {
     "mcpServers": {
       "serena": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-serena"],
         "env": {
           "SERENA_PROJECT_ROOT": "${workspaceFolder}"
         }
       }
     }
   }

   ✓ Verification:
   After adding configuration and restarting Claude Code:
   1. Run /sh_status
   2. Confirm Serena shows ✅ Connected
   3. Test with: Check if you have access to list_memories tool

   📚 Documentation:
   https://github.com/modelcontextprotocol/servers/tree/main/serena

🟡 RECOMMENDED SERVERS
───────────────────────────────────────────────────────────────

✅ Sequential MCP - CONNECTED
   Version: Detected
   Status: Operational
   Tools Available: sequentialthinking ✓

⚠️  Context7 MCP - NOT FOUND
   Status: Recommended - Provides framework patterns
   Purpose: Official documentation and code patterns
   Impact: Less guidance on React, Next.js, and framework specifics

   📦 Installation:
   npm install -g @context7/mcp-server

   ⚙️  Configuration:
   {
     "mcpServers": {
       "context7": {
         "command": "npx",
         "args": ["-y", "@context7/mcp-server"]
       }
     }
   }

   📚 Documentation:
   https://context7.dev/docs

✅ Puppeteer MCP - CONNECTED
   Version: Detected
   Status: Operational
   Tools Available: puppeteer_navigate, puppeteer_screenshot ✓

🟢 CONDITIONAL SERVERS
───────────────────────────────────────────────────────────────

✅ shadcn-ui MCP - CONNECTED
   Status: Required for React/Next.js projects
   Purpose: Shannon enforces shadcn for all React UI work
   Tools Available: get_component, list_components ✓

   ⚠️  Note: If building React/Next.js apps, this MCP is mandatory
   Shannon will error without it for React UI operations

───────────────────────────────────────────────────────────────
📊 SUMMARY
───────────────────────────────────────────────────────────────

Required:     0/1 available ❌ CRITICAL - Serena MCP must be configured
Recommended:  2/3 available ⚠️  FUNCTIONAL - Context7 recommended for best experience
Conditional:  1/1 available ✅ READY for React/Next.js projects

🚨 CRITICAL: Serena MCP must be configured for Shannon to function
   Run this command with --install-guide for detailed setup walkthrough

💡 After configuring MCPs, run /sh_status to verify full Shannon functionality

═══════════════════════════════════════════════════════════════
```

## MCP Detection Logic

This command checks MCP availability by attempting to detect their tools:

```
FOR each MCP server:
  CHECK if characteristic tools exist in available tool list
  IF tools found:
    STATUS = Connected ✅
    VERIFY by listing tool names
  ELSE:
    STATUS = Not Found ❌
    PROVIDE installation instructions
    PROVIDE configuration example
    PROVIDE verification steps
```

## Setup Guidance

### For Each Missing MCP

The command provides:
1. **Clear status**: Why this MCP is needed
2. **Installation command**: Copy-paste ready npm install
3. **Configuration example**: Complete Claude Code settings JSON
4. **Verification steps**: How to confirm it's working
5. **Documentation link**: Official docs for troubleshooting

### Interactive Mode (--fix)

With `--fix` flag, this command can guide users through:
1. Detecting Claude Code settings file location
2. Showing current MCP configuration
3. Providing exact edits needed
4. Confirming each MCP after configuration

## Common Issues

**Issue: "Tool not found" errors**
- Cause: Required MCP not configured
- Solution: Run /sh_check_mcps, follow setup instructions

**Issue: "Serena connection failed"**
- Cause: Serena MCP configured but not responding
- Solution: Restart Claude Code, check Serena logs, verify SERENA_PROJECT_ROOT

**Issue: "shadcn-ui not available"**
- Cause: Working on React project without shadcn MCP
- Solution: Install shadcn-ui MCP per instructions

## Related Commands

- `/sh_status` - Overall framework status
- `/help` - All available commands
- Claude Code settings for MCP configuration

## Implementation Notes

This command is essential for user success. It dramatically reduces setup friction and support burden by providing actionable, specific guidance for MCP configuration.

New users should run this immediately after installing Shannon to ensure all dependencies are met.
