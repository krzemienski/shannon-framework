#!/bin/bash

# Shannon Framework - Installation Test Script
# Purpose: Test installation script logic without actually installing

set -e

SHANNON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Shannon Framework Installation Test ==="
echo ""
echo "Testing from: ${SHANNON_ROOT}"
echo ""

# Test 1: Verify source files exist
echo "Test 1: Verifying source files..."

if [ ! -d "${SHANNON_ROOT}/skills" ]; then
    echo "❌ FAIL: skills directory not found"
    exit 1
fi

if [ ! -d "${SHANNON_ROOT}/commands" ]; then
    echo "❌ FAIL: commands directory not found"
    exit 1
fi

if [ ! -d "${SHANNON_ROOT}/agents" ]; then
    echo "❌ FAIL: agents directory not found"
    exit 1
fi

if [ ! -d "${SHANNON_ROOT}/core" ]; then
    echo "❌ FAIL: core directory not found"
    exit 1
fi

if [ ! -d "${SHANNON_ROOT}/modes" ]; then
    echo "❌ FAIL: modes directory not found"
    exit 1
fi

if [ ! -d "${SHANNON_ROOT}/templates" ]; then
    echo "❌ FAIL: templates directory not found"
    exit 1
fi

if [ ! -d "${SHANNON_ROOT}/hooks" ]; then
    echo "❌ FAIL: hooks directory not found"
    exit 1
fi

echo "✅ PASS: All source directories exist"
echo ""

# Test 2: Count files
echo "Test 2: Counting files..."

skill_count=$(find "${SHANNON_ROOT}/skills" -mindepth 1 -maxdepth 1 -type d ! -name "README.md" | wc -l)
command_count=$(find "${SHANNON_ROOT}/commands" -name "*.md" | wc -l)
agent_count=$(find "${SHANNON_ROOT}/agents" -name "*.md" | wc -l)
core_count=$(find "${SHANNON_ROOT}/core" -name "*.md" | wc -l)
mode_count=$(find "${SHANNON_ROOT}/modes" -name "*.md" | wc -l)
hook_count=$(find "${SHANNON_ROOT}/hooks" -name "*.py" -o -name "*.sh" | wc -l)

echo "  Skills:   ${skill_count}"
echo "  Commands: ${command_count}"
echo "  Agents:   ${agent_count}"
echo "  Core:     ${core_count}"
echo "  Modes:    ${mode_count}"
echo "  Hooks:    ${hook_count}"
echo ""

if [ ${skill_count} -lt 10 ]; then
    echo "⚠️  WARNING: Expected at least 10 skills, found ${skill_count}"
fi

if [ ${command_count} -lt 15 ]; then
    echo "⚠️  WARNING: Expected at least 15 commands, found ${command_count}"
fi

if [ ${agent_count} -lt 20 ]; then
    echo "⚠️  WARNING: Expected at least 20 agents, found ${agent_count}"
fi

echo "✅ PASS: File counts reasonable"
echo ""

# Test 3: Verify critical files exist
echo "Test 3: Verifying critical files..."

critical_files=(
    "skills/using-shannon/SKILL.md"
    "skills/spec-analysis/SKILL.md"
    "skills/wave-orchestration/SKILL.md"
    "skills/functional-testing/SKILL.md"
    "skills/context-preservation/SKILL.md"
    "skills/mcp-discovery/SKILL.md"
    "commands/spec.md"
    "commands/wave.md"
    "commands/do.md"
    "commands/prime.md"
    "hooks/session_start.sh"
    "hooks/user_prompt_submit.py"
    "hooks/precompact.py"
    "hooks/post_tool_use.py"
    "hooks/stop.py"
    "hooks/hooks.json"
    "core/SPEC_ANALYSIS.md"
    "core/WAVE_ORCHESTRATION.md"
    "core/TESTING_PHILOSOPHY.md"
    "core/MCP_DISCOVERY.md"
)

all_found=true

for file in "${critical_files[@]}"; do
    if [ ! -f "${SHANNON_ROOT}/${file}" ]; then
        echo "❌ Missing: ${file}"
        all_found=false
    fi
done

if [ "${all_found}" = true ]; then
    echo "✅ PASS: All critical files exist"
else
    echo "❌ FAIL: Some critical files missing"
    exit 1
fi
echo ""

# Test 4: Verify using-shannon skill has content
echo "Test 4: Verifying using-shannon skill..."

using_shannon_file="${SHANNON_ROOT}/skills/using-shannon/SKILL.md"
using_shannon_size=$(wc -l < "${using_shannon_file}")

echo "  using-shannon skill: ${using_shannon_size} lines"

if [ ${using_shannon_size} -lt 100 ]; then
    echo "❌ FAIL: using-shannon skill seems too short (< 100 lines)"
    exit 1
fi

if ! grep -q "IRON_LAW" "${using_shannon_file}"; then
    echo "❌ FAIL: using-shannon skill missing IRON_LAW section"
    exit 1
fi

echo "✅ PASS: using-shannon skill valid"
echo ""

# Test 5: Verify hooks have proper structure
echo "Test 5: Verifying hook scripts..."

hooks_to_check=(
    "hooks/session_start.sh"
    "hooks/user_prompt_submit.py"
    "hooks/precompact.py"
    "hooks/post_tool_use.py"
    "hooks/stop.py"
)

for hook in "${hooks_to_check[@]}"; do
    hook_file="${SHANNON_ROOT}/${hook}"
    
    # Check shebang exists
    if ! head -n 1 "${hook_file}" | grep -q "^#!"; then
        echo "❌ Missing shebang: ${hook}"
        exit 1
    fi
    
    # Check file is executable
    if [ ! -x "${hook_file}" ]; then
        echo "⚠️  WARNING: ${hook} not executable (will be fixed during install)"
    fi
done

echo "✅ PASS: All hook scripts have proper structure"
echo ""

# Test 6: Verify hooks.json structure
echo "Test 6: Verifying hooks.json..."

hooks_json="${SHANNON_ROOT}/hooks/hooks.json"

if ! cat "${hooks_json}" | python3 -m json.tool > /dev/null 2>&1; then
    echo "❌ FAIL: hooks.json is not valid JSON"
    exit 1
fi

required_hooks=("SessionStart" "UserPromptSubmit" "PreCompact" "PostToolUse" "Stop")

for hook_type in "${required_hooks[@]}"; do
    if ! grep -q "\"${hook_type}\"" "${hooks_json}"; then
        echo "❌ Missing hook type: ${hook_type}"
        exit 1
    fi
done

echo "✅ PASS: hooks.json structure valid"
echo ""

# Test 7: Check for path references that need updating
echo "Test 7: Checking path references..."

# These should exist in source files and will be updated during install
path_patterns=(
    "shannon-plugin/core/"
    "shannon-plugin/skills/"
    "shannon-plugin/agents/"
)

found_references=false

for skill_file in $(find "${SHANNON_ROOT}/skills" -name "SKILL.md" -o -name "skill.md"); do
    for pattern in "${path_patterns[@]}"; do
        if grep -q "${pattern}" "${skill_file}"; then
            found_references=true
            break 2
        fi
    done
done

if [ "${found_references}" = true ]; then
    echo "✅ PASS: Found path references to update (expected)"
else
    echo "⚠️  WARNING: No path references found (may already be updated)"
fi
echo ""

# Test 8: Verify install script exists and is valid
echo "Test 8: Verifying install_local.sh..."

install_script="${SHANNON_ROOT}/install_local.sh"

if [ ! -f "${install_script}" ]; then
    echo "❌ FAIL: install_local.sh not found"
    exit 1
fi

if [ ! -x "${install_script}" ]; then
    echo "❌ FAIL: install_local.sh not executable"
    exit 1
fi

# Check script syntax
if ! bash -n "${install_script}" 2>&1; then
    echo "❌ FAIL: install_local.sh has syntax errors"
    exit 1
fi

echo "✅ PASS: install_local.sh valid"
echo ""

# Summary
echo "=== Test Summary ==="
echo ""
echo "✅ All tests passed!"
echo ""
echo "Installation script is ready to use:"
echo "  ./install_local.sh"
echo ""
echo "This will install Shannon Framework to:"
echo "  ~/.claude/skills/shannon/"
echo "  ~/.claude/commands/shannon/"
echo "  ~/.claude/agents/shannon/"
echo "  ~/.claude/core/shannon/"
echo "  ~/.claude/modes/shannon/"
echo "  ~/.claude/templates/shannon/"
echo "  ~/.claude/hooks/shannon/"
echo "  ~/.claude/hooks.json"
echo ""
echo "After installation, restart Claude Code and run:"
echo "  /shannon:status"
echo ""

