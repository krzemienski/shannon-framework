#!/usr/bin/env bash
#
# Shannon V3 Verification Script
# Comprehensive validation of structure, installation, and functionality
#

set -uo pipefail

# Colors and formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Script configuration
VERBOSE=false
QUICK=false
fail_count=0
pass_count=0
warn_count=0

# Shannon paths
SHANNON_ROOT="${SHANNON_ROOT:-$HOME/.claude}"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --quick|-q)
      QUICK=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --verbose, -v    Show detailed output"
      echo "  --quick, -q      Run only fast checks"
      echo "  --help, -h       Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Helper functions
log_section() {
  echo ""
  echo -e "${BLUE}${BOLD}=== $1 ===${NC}"
}

log_verbose() {
  if [ "$VERBOSE" = true ]; then
    echo "  $1"
  fi
}

check() {
  local test_name=$1
  shift

  log_verbose "Checking: $test_name"

  if "$@" &>/dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: $test_name"
    ((pass_count++))
    return 0
  else
    echo -e "${RED}❌ FAIL${NC}: $test_name"
    ((fail_count++))
    return 1
  fi
}

warn() {
  echo -e "${YELLOW}⚠️  WARN${NC}: $1"
  ((warn_count++))
}

# Verification functions
check_file_exists() {
  [ -f "$1" ]
}

check_dir_exists() {
  [ -d "$1" ]
}

check_file_count() {
  local dir=$1
  local pattern=$2
  local expected=$3
  local actual=$(find "$dir" -name "$pattern" | wc -l | tr -d ' ')
  [ "$actual" -eq "$expected" ]
}

check_min_size() {
  local file=$1
  local min_bytes=$2
  [ -f "$file" ] && [ $(wc -c < "$file") -ge "$min_bytes" ]
}

check_yaml_frontmatter() {
  local file=$1
  head -n 1 "$file" | grep -q "^---$"
}

check_content_field() {
  local file=$1
  local field=$2
  grep -q "^$field:" "$file"
}

check_executable() {
  [ -x "$1" ]
}

# 1. Structural Integrity Checks
verify_structure() {
  log_section "Structural Integrity"

  # Core framework files
  check "Core directory exists" check_dir_exists "$PROJECT_ROOT/Shannon/Core"
  check "Core has 8 files" check_file_count "$PROJECT_ROOT/Shannon/Core" "*.md" 8

  check "CONTEXT_MANAGEMENT.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/CONTEXT_MANAGEMENT.md"
  check "HOOK_SYSTEM.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/HOOK_SYSTEM.md"
  check "MCP_DISCOVERY.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/MCP_DISCOVERY.md"
  check "PHASE_PLANNING.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/PHASE_PLANNING.md"
  check "PROJECT_MEMORY.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/PROJECT_MEMORY.md"
  check "SPEC_ANALYSIS.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/SPEC_ANALYSIS.md"
  check "TESTING_PHILOSOPHY.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/TESTING_PHILOSOPHY.md"
  check "WAVE_ORCHESTRATION.md exists" check_file_exists "$PROJECT_ROOT/Shannon/Core/WAVE_ORCHESTRATION.md"

  # Agents directory
  check "Agents directory exists" check_dir_exists "$PROJECT_ROOT/Shannon/Agents"
  check "Agents has 19 files" check_file_count "$PROJECT_ROOT/Shannon/Agents" "*.md" 19

  # Essential agents
  check "SPEC_ANALYZER agent exists" check_file_exists "$PROJECT_ROOT/Shannon/Agents/SPEC_ANALYZER.md"
  check "PHASE_ARCHITECT agent exists" check_file_exists "$PROJECT_ROOT/Shannon/Agents/PHASE_ARCHITECT.md"
  check "WAVE_COORDINATOR agent exists" check_file_exists "$PROJECT_ROOT/Shannon/Agents/WAVE_COORDINATOR.md"
  check "TEST_GUARDIAN agent exists" check_file_exists "$PROJECT_ROOT/Shannon/Agents/TEST_GUARDIAN.md"
  check "CONTEXT_GUARDIAN agent exists" check_file_exists "$PROJECT_ROOT/Shannon/Agents/CONTEXT_GUARDIAN.md"

  # Commands directory
  check "Commands directory exists" check_dir_exists "$PROJECT_ROOT/Shannon/Commands"
  check "Commands has 29 files" check_file_count "$PROJECT_ROOT/Shannon/Commands" "*.md" 29

  # Key commands
  check "sc_analyze command exists" check_file_exists "$PROJECT_ROOT/Shannon/Commands/sc_analyze.md"
  check "sc_implement command exists" check_file_exists "$PROJECT_ROOT/Shannon/Commands/sc_implement.md"
  check "sh_spec command exists" check_file_exists "$PROJECT_ROOT/Shannon/Commands/sh_spec.md"
  check "sh_checkpoint command exists" check_file_exists "$PROJECT_ROOT/Shannon/Commands/sh_checkpoint.md"

  # Modes directory
  check "Modes directory exists" check_dir_exists "$PROJECT_ROOT/Shannon/Modes"
  check "Modes has 2 files" check_file_count "$PROJECT_ROOT/Shannon/Modes" "*.md" 2

  # Scripts
  check "Scripts directory exists" check_dir_exists "$PROJECT_ROOT/scripts"

  # Optional installation scripts (not required for core functionality)
  if [ -f "$PROJECT_ROOT/scripts/install.sh" ]; then
    check "install.sh exists" check_file_exists "$PROJECT_ROOT/scripts/install.sh"
    check "install.sh executable" check_executable "$PROJECT_ROOT/scripts/install.sh"
  else
    warn "install.sh not yet created (optional)"
  fi

  if [ -f "$PROJECT_ROOT/scripts/uninstall.sh" ]; then
    check "uninstall.sh exists" check_file_exists "$PROJECT_ROOT/scripts/uninstall.sh"
    check "uninstall.sh executable" check_executable "$PROJECT_ROOT/scripts/uninstall.sh"
  else
    warn "uninstall.sh not yet created (optional)"
  fi

  # Tests
  check "Tests directory exists" check_dir_exists "$PROJECT_ROOT/tests"
  check "pytest config exists" check_file_exists "$PROJECT_ROOT/tests/pytest.ini"
  check "Hooks test exists" check_file_exists "$PROJECT_ROOT/tests/test_hooks.py"
  check "Structure test exists" check_file_exists "$PROJECT_ROOT/tests/test_structure.py"
}

# 2. Content Validation
verify_content() {
  log_section "Content Validation"

  # Check YAML frontmatter in agents
  local agents_with_frontmatter=0
  for agent in "$PROJECT_ROOT/Shannon/Agents"/*.md; do
    if check_yaml_frontmatter "$agent"; then
      ((agents_with_frontmatter++))
    fi
  done
  check "All agents have YAML frontmatter" [ "$agents_with_frontmatter" -eq 19 ]

  # Check YAML frontmatter in commands
  local commands_with_frontmatter=0
  for command in "$PROJECT_ROOT/Shannon/Commands"/*.md; do
    if check_yaml_frontmatter "$command"; then
      ((commands_with_frontmatter++))
    fi
  done
  check "All commands have YAML frontmatter" [ "$commands_with_frontmatter" -eq 29 ]

  # Check required fields in core files
  check "SPEC_ANALYSIS has content" grep -q "Specification Analysis" "$PROJECT_ROOT/Shannon/Core/SPEC_ANALYSIS.md"
  check "WAVE_ORCHESTRATION has content" grep -q "Wave Orchestration" "$PROJECT_ROOT/Shannon/Core/WAVE_ORCHESTRATION.md"
  check "PHASE_PLANNING has content" grep -q "Phase Planning" "$PROJECT_ROOT/Shannon/Core/PHASE_PLANNING.md"

  # Check minimum file sizes (should have substantial content)
  check "SPEC_ANALYSIS min size" check_min_size "$PROJECT_ROOT/Shannon/Core/SPEC_ANALYSIS.md" 20000
  check "WAVE_ORCHESTRATION min size" check_min_size "$PROJECT_ROOT/Shannon/Core/WAVE_ORCHESTRATION.md" 20000
  check "HOOK_SYSTEM min size" check_min_size "$PROJECT_ROOT/Shannon/Core/HOOK_SYSTEM.md" 20000

  # Check agent metadata
  check "SPEC_ANALYZER has name" check_content_field "$PROJECT_ROOT/Shannon/Agents/SPEC_ANALYZER.md" "name"
  check "WAVE_COORDINATOR has category" check_content_field "$PROJECT_ROOT/Shannon/Agents/WAVE_COORDINATOR.md" "category"
  check "TEST_GUARDIAN has description" check_content_field "$PROJECT_ROOT/Shannon/Agents/TEST_GUARDIAN.md" "description"
}

# 3. Installation Verification
verify_installation() {
  log_section "Installation Verification"

  if [ ! -d "$SHANNON_ROOT" ]; then
    warn "Shannon not installed in $SHANNON_ROOT (run scripts/install.sh)"
    return
  fi

  # Check installed structure
  check "Installed core files" check_dir_exists "$SHANNON_ROOT"

  local core_files=(COMMANDS.md FLAGS.md MCP.md MODES.md ORCHESTRATOR.md PERSONAS.md PRINCIPLES.md RULES.md)
  for file in "${core_files[@]}"; do
    check "Installed $file" check_file_exists "$SHANNON_ROOT/$file"
  done

  # Check Claude Code hooks
  if [ -d "$HOME/.config/claude" ]; then
    check "Claude Code hooks dir exists" check_dir_exists "$HOME/.config/claude/hooks"
    check "precompact.py exists" check_file_exists "$HOME/.config/claude/hooks/precompact.py"
    check "precompact.py executable" check_executable "$HOME/.config/claude/hooks/precompact.py"
  else
    warn "Claude Code config not found (hooks not installed)"
  fi
}

# 4. Hook Functionality
verify_hooks() {
  if [ "$QUICK" = true ]; then
    return
  fi

  log_section "Hook Functionality"

  local hook_path="$HOME/.config/claude/hooks/precompact.py"

  if [ ! -f "$hook_path" ]; then
    warn "precompact.py not installed, skipping hook tests"
    return
  fi

  # Test hook execution
  check "Hook is Python script" head -n 1 "$hook_path" | grep -q "python"

  # Test with dummy context
  local test_context='{"request": {"prompt": "test"}, "projectRoot": "/tmp"}'
  if echo "$test_context" | python3 "$hook_path" &>/dev/null; then
    check "Hook executes without errors" true
  else
    check "Hook executes without errors" false
  fi
}

# 5. Test Suite
verify_tests() {
  if [ "$QUICK" = true ]; then
    return
  fi

  log_section "Test Suite"

  cd "$PROJECT_ROOT"

  # Check if pytest is available
  if ! command -v pytest &>/dev/null; then
    warn "pytest not installed, skipping test suite"
    return
  fi

  # Run tests
  if pytest tests/ -v &>/dev/null; then
    check "Test suite passes" true
  else
    check "Test suite passes" false
    if [ "$VERBOSE" = true ]; then
      echo "  Run 'pytest tests/ -v' for details"
    fi
  fi
}

# 6. Artifact Creation
verify_artifacts() {
  if [ "$QUICK" = true ]; then
    return
  fi

  log_section "Artifact Creation"

  # Check artifacts directory
  if [ -d "$PROJECT_ROOT/artifacts" ]; then
    check "Artifacts directory exists" true

    local artifact_count=$(ls -1 "$PROJECT_ROOT/artifacts" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$artifact_count" -gt 0 ]; then
      check "Artifacts created" true
      log_verbose "Found $artifact_count artifacts"
    else
      warn "No artifacts found (none generated yet)"
    fi
  else
    warn "Artifacts directory does not exist"
  fi
}

# 7. Git Status
verify_git() {
  if [ "$QUICK" = true ]; then
    return
  fi

  log_section "Git Status"

  cd "$PROJECT_ROOT"

  if ! git rev-parse --git-dir &>/dev/null; then
    warn "Not a git repository"
    return
  fi

  # Check for uncommitted changes
  if [ -z "$(git status --porcelain)" ]; then
    check "No uncommitted changes" true
  else
    warn "Uncommitted changes detected"
    if [ "$VERBOSE" = true ]; then
      git status --short | head -10
    fi
  fi

  # Check current branch
  local branch=$(git branch --show-current)
  log_verbose "Current branch: $branch"
}

# 8. Integration Checks
verify_integration() {
  log_section "Integration Verification"

  # Check cross-references in core
  check "WAVE_ORCHESTRATION references phases" grep -qi "phase" "$PROJECT_ROOT/Shannon/Core/WAVE_ORCHESTRATION.md"
  check "SPEC_ANALYSIS references testing" grep -qi "test" "$PROJECT_ROOT/Shannon/Core/SPEC_ANALYSIS.md"
  check "HOOK_SYSTEM references context" grep -qi "context" "$PROJECT_ROOT/Shannon/Core/HOOK_SYSTEM.md"

  # Check agent coordination
  check "WAVE_COORDINATOR references wave strategy" grep -qi "wave" "$PROJECT_ROOT/Shannon/Agents/WAVE_COORDINATOR.md"
  check "PHASE_ARCHITECT references planning" grep -qi "plan" "$PROJECT_ROOT/Shannon/Agents/PHASE_ARCHITECT.md"
  check "TEST_GUARDIAN references testing" grep -qi "test" "$PROJECT_ROOT/Shannon/Agents/TEST_GUARDIAN.md"
  check "SPEC_ANALYZER references specification" grep -qi "spec" "$PROJECT_ROOT/Shannon/Agents/SPEC_ANALYZER.md"

  # Check command integration
  check "sh_spec command exists" grep -qi "specification" "$PROJECT_ROOT/Shannon/Commands/sh_spec.md"
  check "sh_checkpoint references saving" grep -qi "save\|checkpoint" "$PROJECT_ROOT/Shannon/Commands/sh_checkpoint.md"
}

# Summary
print_summary() {
  echo ""
  echo -e "${BLUE}${BOLD}=== VERIFICATION SUMMARY ===${NC}"
  echo ""
  echo -e "${GREEN}Passed:${NC}  $pass_count"
  echo -e "${RED}Failed:${NC}  $fail_count"
  echo -e "${YELLOW}Warnings:${NC} $warn_count"
  echo ""

  if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✅ Shannon V3 verification PASSED${NC}"
    echo ""
    echo "System is ready for use."
    if [ $warn_count -gt 0 ]; then
      echo -e "${YELLOW}Note: $warn_count warnings detected (non-critical)${NC}"
    fi
  else
    echo -e "${RED}${BOLD}❌ Shannon V3 verification FAILED${NC}"
    echo ""
    echo "Please address the $fail_count failed checks above."
    if [ "$VERBOSE" = false ]; then
      echo "Run with --verbose for detailed output."
    fi
  fi
  echo ""
}

# Main execution
main() {
  echo -e "${BLUE}${BOLD}Shannon V3 Verification Script${NC}"
  echo "Project: $PROJECT_ROOT"
  echo "Install: $SHANNON_ROOT"

  if [ "$QUICK" = true ]; then
    echo -e "${YELLOW}Quick mode: Running fast checks only${NC}"
  fi

  verify_structure
  verify_content
  verify_installation
  verify_hooks
  verify_tests
  verify_artifacts
  verify_git
  verify_integration

  print_summary

  exit $fail_count
}

main