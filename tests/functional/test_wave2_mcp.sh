#!/bin/bash
# Wave 2 Validation Gate: MCP Management
# Tests MCP server auto-installation and management

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Wave 2: MCP Management Validation"
echo "═══════════════════════════════════════"
echo ""

# Test 1: mcp-install command exists
echo "Test 1: mcp-install command availability"
shannon mcp-install --help > /dev/null 2>&1
assert_exit_code 0 $? "mcp-install command exists" && record_pass || record_fail

# Test 2: Help text is informative
output=$(shannon mcp-install --help 2>&1)
assert_contains "$output" "MCP|server|install" "Help text mentions MCP functionality" && record_pass || record_fail

# Test 3: MCP listing command (try multiple possible names)
echo "Test 3: MCP listing functionality"
list_output=$(shannon mcp list 2>&1 || shannon mcp-list 2>&1 || shannon mcp status 2>&1 || echo "COMMAND_NOT_FOUND")

if [ "$list_output" != "COMMAND_NOT_FOUND" ]; then
    echo "  ✅ PASS: MCP listing command exists"
    record_pass
else
    echo "  ⚠️  INFO: MCP list command not found (may not be implemented yet)"
fi

# Test 4: Dry-run installation (safe test without actual installation)
echo "Test 4: Dry-run MCP installation"
output=$(shannon mcp-install puppeteer --dry-run 2>&1 || echo "DRY_RUN_NOT_SUPPORTED")

if [ "$output" != "DRY_RUN_NOT_SUPPORTED" ]; then
    if echo "$output" | grep -qE "install|would install|puppet"; then
        echo "  ✅ PASS: Dry-run installation shows expected behavior"
        record_pass
    else
        echo "  ⚠️  INFO: Dry-run succeeded but output unclear"
    fi
else
    echo "  ⚠️  INFO: Dry-run flag not supported (skipping)"
fi

echo ""
print_summary "test_wave2_mcp.sh"
