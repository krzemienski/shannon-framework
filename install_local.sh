#!/bin/bash

# Shannon Framework - Local Installation Script
# Version: 5.6.1
# Purpose: Install Shannon Framework directly to user's Claude configuration
#          ensuring only ONE installation exists (local OR plugin, not both)

set -e  # Exit on error

# =============================================================================
# CONFIGURATION
# =============================================================================

SHANNON_VERSION="5.6.1"
SCRIPT_VERSION="2.0.0"

# Script directory (Shannon Framework root)
SHANNON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# User's Claude configuration directory
CLAUDE_CONFIG_DIR="${HOME}/.claude"

# Installation directories
SKILLS_DIR="${CLAUDE_CONFIG_DIR}/skills/shannon"
COMMANDS_DIR="${CLAUDE_CONFIG_DIR}/commands/shannon"
AGENTS_DIR="${CLAUDE_CONFIG_DIR}/agents/shannon"
CORE_DIR="${CLAUDE_CONFIG_DIR}/core/shannon"
MODES_DIR="${CLAUDE_CONFIG_DIR}/modes/shannon"
TEMPLATES_DIR="${CLAUDE_CONFIG_DIR}/templates/shannon"
HOOKS_DIR="${CLAUDE_CONFIG_DIR}/hooks/shannon"
HOOKS_CONFIG="${CLAUDE_CONFIG_DIR}/hooks.json"

# Version tracking
VERSION_FILE="${CLAUDE_CONFIG_DIR}/shannon_version"

# Logging
LOG_FILE="${CLAUDE_CONFIG_DIR}/shannon_install.log"

# Plugin locations to check
PLUGIN_DIRS=(
    "${HOME}/.claude/plugins/shannon@shannon-framework"
    "${HOME}/.claude/plugins/shannon"
    "${HOME}/.cursor/plugins/shannon@shannon-framework"
    "${HOME}/.cursor/plugins/shannon"
)

MARKETPLACE_FILES=(
    "${HOME}/.claude/plugins/marketplace.json"
    "${HOME}/.cursor/plugins/marketplace.json"
    "${CLAUDE_CONFIG_DIR}/marketplace.json"
)

# Installation mode
MODE="install"
FORCE=false
QUIET=false

# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log_to_file() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}" 2>/dev/null || true
}

print_info() {
    [[ "${QUIET}" == "false" ]] && echo -e "${BLUE}[INFO]${NC} $1"
    log_to_file "INFO: $1"
}

print_success() {
    [[ "${QUIET}" == "false" ]] && echo -e "${GREEN}[SUCCESS]${NC} $1"
    log_to_file "SUCCESS: $1"
}

print_warning() {
    [[ "${QUIET}" == "false" ]] && echo -e "${YELLOW}[WARNING]${NC} $1"
    log_to_file "WARNING: $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    log_to_file "ERROR: $1"
}

print_action() {
    [[ "${QUIET}" == "false" ]] && echo -e "${CYAN}[ACTION]${NC} $1"
    log_to_file "ACTION: $1"
}

print_header() {
    [[ "${QUIET}" == "false" ]] && echo ""
    [[ "${QUIET}" == "false" ]] && echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    [[ "${QUIET}" == "false" ]] && echo -e "${BOLD}  $1${NC}"
    [[ "${QUIET}" == "false" ]] && echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
}

# =============================================================================
# USAGE
# =============================================================================

show_usage() {
    cat << EOF
${BOLD}Shannon Framework v${SHANNON_VERSION} - Local Installation Script${NC}

${BOLD}USAGE:${NC}
    $0 [OPTIONS]

${BOLD}OPTIONS:${NC}
    --install       Install or reinstall Shannon Framework (default)
    --update        Alias for --install (same behavior)
    --uninstall     Remove Shannon Framework completely
    --status        Show current installation status
    --force, -f     Non-interactive mode (auto-yes to prompts)
    --quiet, -q     Minimal output
    --help, -h      Show this help message

${BOLD}EXAMPLES:${NC}
    $0                    # Interactive installation
    $0 --install          # Same as above
    $0 --install --force  # Non-interactive installation
    $0 --status           # Check what's installed
    $0 --uninstall        # Remove everything

${BOLD}WHAT THIS SCRIPT DOES:${NC}
    1. Detects and removes ANY existing Shannon plugin installations
    2. Detects and removes ANY existing Shannon local installations
    3. Installs fresh Shannon v${SHANNON_VERSION} to ~/.claude/
    4. Ensures only ONE installation exists

${BOLD}INSTALLATION LOCATIONS:${NC}
    ~/.claude/skills/shannon/
    ~/.claude/commands/shannon/
    ~/.claude/agents/shannon/
    ~/.claude/core/shannon/
    ~/.claude/modes/shannon/
    ~/.claude/templates/shannon/
    ~/.claude/hooks/shannon/
    ~/.claude/hooks.json
    ~/.claude/shannon_version

${BOLD}DOCUMENTATION:${NC}
    See: INSTALL_LOCAL.md
EOF
}

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install)
                MODE="install"
                shift
                ;;
            --update)
                MODE="install"  # Update is now same as install
                shift
                ;;
            --uninstall)
                MODE="uninstall"
                shift
                ;;
            --status)
                MODE="status"
                shift
                ;;
            --force|-f)
                FORCE=true
                shift
                ;;
            --quiet|-q)
                QUIET=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# =============================================================================
# DETECTION FUNCTIONS
# =============================================================================

# Get installed version (if any)
get_installed_version() {
    if [[ -f "${VERSION_FILE}" ]]; then
        head -n 1 "${VERSION_FILE}" 2>/dev/null
    else
        echo ""
    fi
}

# Check if local installation exists
check_local_installation() {
    [[ -d "${SKILLS_DIR}" ]] || [[ -d "${COMMANDS_DIR}" ]] || [[ -d "${AGENTS_DIR}" ]] || [[ -f "${VERSION_FILE}" ]]
}

# Check for plugin directories
detect_plugin_directories() {
    local found=false
    for plugin_dir in "${PLUGIN_DIRS[@]}"; do
        if [[ -d "${plugin_dir}" ]]; then
            print_warning "Found plugin directory: ${plugin_dir}"
            found=true
        fi
    done
    [[ "${found}" == "true" ]]
}

# Check for marketplace.json entries
detect_marketplace_entries() {
    local found=false
    for marketplace_file in "${MARKETPLACE_FILES[@]}"; do
        if [[ -f "${marketplace_file}" ]]; then
            if grep -qi "shannon" "${marketplace_file}" 2>/dev/null; then
                print_warning "Found Shannon entry in: ${marketplace_file}"
                found=true
            fi
        fi
    done
    [[ "${found}" == "true" ]]
}

# Comprehensive plugin detection
detect_any_plugin_installation() {
    local found=false

    # Check directories
    for plugin_dir in "${PLUGIN_DIRS[@]}"; do
        if [[ -d "${plugin_dir}" ]]; then
            found=true
            break
        fi
    done

    # Check marketplace files
    if [[ "${found}" == "false" ]]; then
        for marketplace_file in "${MARKETPLACE_FILES[@]}"; do
            if [[ -f "${marketplace_file}" ]] && grep -qi "shannon" "${marketplace_file}" 2>/dev/null; then
                found=true
                break
            fi
        done
    fi

    [[ "${found}" == "true" ]]
}

# =============================================================================
# CLEANUP FUNCTIONS
# =============================================================================

# Remove plugin directories
remove_plugin_directories() {
    print_action "Removing plugin directories..."
    local removed=0

    for plugin_dir in "${PLUGIN_DIRS[@]}"; do
        if [[ -d "${plugin_dir}" ]]; then
            print_info "  Removing: ${plugin_dir}"
            rm -rf "${plugin_dir}"
            ((removed++))
        fi
    done

    if [[ ${removed} -gt 0 ]]; then
        print_success "Removed ${removed} plugin director(y/ies)"
    fi
}

# Remove Shannon from marketplace.json files
clean_marketplace_entries() {
    print_action "Cleaning marketplace entries..."

    for marketplace_file in "${MARKETPLACE_FILES[@]}"; do
        if [[ -f "${marketplace_file}" ]] && grep -qi "shannon" "${marketplace_file}" 2>/dev/null; then
            print_info "  Cleaning: ${marketplace_file}"

            # Backup
            cp "${marketplace_file}" "${marketplace_file}.backup.$(date +%Y%m%d_%H%M%S)"

            # Remove shannon entries (this is a simplified approach)
            # For proper JSON manipulation, we'd use jq, but keeping it simple
            if command -v jq &> /dev/null; then
                # Use jq if available
                jq 'del(.plugins[] | select(.name | test("shannon"; "i")))' "${marketplace_file}" > "${marketplace_file}.tmp" 2>/dev/null && \
                mv "${marketplace_file}.tmp" "${marketplace_file}" || \
                print_warning "    Could not clean with jq, manual cleanup may be needed"
            else
                print_warning "    jq not available, manual cleanup of ${marketplace_file} may be needed"
            fi
        fi
    done
}

# Remove local installation
remove_local_installation() {
    print_action "Removing local installation..."
    local removed=0

    local dirs_to_remove=(
        "${SKILLS_DIR}"
        "${COMMANDS_DIR}"
        "${AGENTS_DIR}"
        "${CORE_DIR}"
        "${MODES_DIR}"
        "${TEMPLATES_DIR}"
        "${HOOKS_DIR}"
    )

    for dir in "${dirs_to_remove[@]}"; do
        if [[ -d "${dir}" ]]; then
            print_info "  Removing: ${dir}"
            rm -rf "${dir}"
            ((removed++))
        fi
    done

    # Remove version file
    if [[ -f "${VERSION_FILE}" ]]; then
        rm -f "${VERSION_FILE}"
        print_info "  Removed version file"
    fi

    # Handle hooks.json - backup and remove Shannon hooks
    if [[ -f "${HOOKS_CONFIG}" ]]; then
        if grep -q "shannon" "${HOOKS_CONFIG}" 2>/dev/null; then
            local backup="${HOOKS_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "${HOOKS_CONFIG}" "${backup}"
            print_info "  Backed up hooks.json to: ${backup}"
            rm -f "${HOOKS_CONFIG}"
            print_info "  Removed hooks.json (Shannon-managed)"
        fi
    fi

    if [[ ${removed} -gt 0 ]]; then
        print_success "Removed ${removed} Shannon director(y/ies)"
    fi
}

# Complete cleanup of all Shannon installations
remove_all_shannon() {
    print_header "Removing All Shannon Installations"

    # Remove plugins first
    remove_plugin_directories
    clean_marketplace_entries

    # Remove local installation
    remove_local_installation

    print_success "All Shannon installations removed"
}

# =============================================================================
# INSTALLATION FUNCTIONS
# =============================================================================

create_directories() {
    print_action "Creating installation directories..."

    mkdir -p "${SKILLS_DIR}"
    mkdir -p "${COMMANDS_DIR}"
    mkdir -p "${AGENTS_DIR}"
    mkdir -p "${CORE_DIR}"
    mkdir -p "${MODES_DIR}"
    mkdir -p "${TEMPLATES_DIR}"
    mkdir -p "${HOOKS_DIR}"

    print_success "Directories created"
}

install_skills() {
    print_action "Installing skills..."
    local count=0

    for skill_dir in "${SHANNON_ROOT}/skills"/*; do
        if [[ -d "${skill_dir}" ]]; then
            local skill_name=$(basename "${skill_dir}")
            mkdir -p "${SKILLS_DIR}/${skill_name}"
            cp -r "${skill_dir}"/* "${SKILLS_DIR}/${skill_name}/"
            ((count++))
        fi
    done

    print_success "Installed ${count} skills"
}

install_commands() {
    print_action "Installing commands..."
    local count=0

    for command_file in "${SHANNON_ROOT}/commands"/*.md; do
        if [[ -f "${command_file}" ]]; then
            cp "${command_file}" "${COMMANDS_DIR}/"
            ((count++))
        fi
    done

    print_success "Installed ${count} commands"
}

install_agents() {
    print_action "Installing agents..."
    local count=0

    for agent_file in "${SHANNON_ROOT}/agents"/*.md; do
        if [[ -f "${agent_file}" ]]; then
            cp "${agent_file}" "${AGENTS_DIR}/"
            ((count++))
        fi
    done

    print_success "Installed ${count} agents"
}

install_core() {
    print_action "Installing core files..."
    local count=0

    for core_file in "${SHANNON_ROOT}/core"/*.md; do
        if [[ -f "${core_file}" ]]; then
            cp "${core_file}" "${CORE_DIR}/"
            ((count++))
        fi
    done

    print_success "Installed ${count} core files"
}

install_modes() {
    print_action "Installing modes..."
    local count=0

    for mode_file in "${SHANNON_ROOT}/modes"/*.md; do
        if [[ -f "${mode_file}" ]]; then
            cp "${mode_file}" "${MODES_DIR}/"
            ((count++))
        fi
    done

    print_success "Installed ${count} modes"
}

install_templates() {
    print_action "Installing templates..."
    local count=0

    for template_file in "${SHANNON_ROOT}/templates"/*.md; do
        if [[ -f "${template_file}" ]]; then
            cp "${template_file}" "${TEMPLATES_DIR}/"
            ((count++))
        fi
    done

    print_success "Installed ${count} templates"
}

install_hooks() {
    print_action "Installing hooks..."

    # Copy Python hooks
    cp "${SHANNON_ROOT}/hooks/user_prompt_submit.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/precompact.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/post_tool_use.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/stop.py" "${HOOKS_DIR}/"

    # Create session_start.sh with embedded using-shannon content
    cat > "${HOOKS_DIR}/session_start.sh" << 'HOOK_HEADER'
#!/bin/bash
# Shannon Framework V5.6 - SessionStart Hook
# Loads using-shannon meta-skill to establish Shannon workflows

echo "<EXTREMELY_IMPORTANT>"
echo "You are using Shannon Framework V5.6."
echo ""
echo "**The content below is the using-shannon skill:**"
echo ""
cat << 'SKILL_CONTENT'
HOOK_HEADER

    # Embed using-shannon content
    cat "${SHANNON_ROOT}/skills/using-shannon/SKILL.md" >> "${HOOKS_DIR}/session_start.sh"

    cat >> "${HOOKS_DIR}/session_start.sh" << 'HOOK_FOOTER'
SKILL_CONTENT
echo ""
echo "</EXTREMELY_IMPORTANT>"
HOOK_FOOTER

    # Make hooks executable
    chmod +x "${HOOKS_DIR}"/*.py "${HOOKS_DIR}"/*.sh 2>/dev/null || true

    # Create hooks.json
    cat > "${HOOKS_CONFIG}" << HOOKS_JSON
{
  "\$schema": "https://claude.ai/hooks-schema.json",
  "\$comment": "Shannon Framework v${SHANNON_VERSION} - Local Installation",
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "Shannon v${SHANNON_VERSION} - Context injection and forced reading",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/user_prompt_submit.py",
            "timeout": 3000
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "description": "Shannon v${SHANNON_VERSION} - Context preservation checkpoint",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/precompact.py",
            "timeout": 15000,
            "continueOnError": false
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "description": "Shannon v${SHANNON_VERSION} - NO MOCKS enforcement",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/post_tool_use.py",
            "timeout": 3000
          }
        ]
      }
    ],
    "Stop": [
      {
        "description": "Shannon v${SHANNON_VERSION} - Wave validation gates",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/stop.py",
            "timeout": 2000
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "description": "Shannon v${SHANNON_VERSION} - Meta-skill loader",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${HOME}/.claude/hooks/shannon/session_start.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
HOOKS_JSON

    print_success "Hooks installed and configured"
}

update_path_references() {
    print_action "Updating path references..."

    # Expand HOME now to avoid issues with special characters in paths
    local home_path="${HOME}"

    # Process all md files - apply each sed pattern separately for safety
    find "${CLAUDE_CONFIG_DIR}" -path "*/shannon/*.md" -type f 2>/dev/null | while read -r file; do
        # Apply each substitution separately - no eval needed
        sed -i.bak \
            -e "s|shannon-plugin/core/|${home_path}/.claude/core/shannon/|g" \
            -e "s|shannon-plugin/skills/|${home_path}/.claude/skills/shannon/|g" \
            -e "s|shannon-plugin/agents/|${home_path}/.claude/agents/shannon/|g" \
            -e "s|shannon-plugin/modes/|${home_path}/.claude/modes/shannon/|g" \
            -e "s|shannon-plugin/templates/|${home_path}/.claude/templates/shannon/|g" \
            -e "s|shannon-plugin/hooks/|${home_path}/.claude/hooks/shannon/|g" \
            "$file" 2>/dev/null || true
        rm -f "${file}.bak" 2>/dev/null || true
    done

    print_success "Path references updated"
}

write_version_file() {
    print_action "Writing version file..."

    cat > "${VERSION_FILE}" << VERSION_INFO
${SHANNON_VERSION}
# Shannon Framework Version File
# Installed: $(date -Iseconds)
# Source: ${SHANNON_ROOT}
# Script: v${SCRIPT_VERSION}
VERSION_INFO

    print_success "Version ${SHANNON_VERSION} recorded"
}

verify_installation() {
    print_action "Verifying installation..."
    local errors=0

    # Check directories
    [[ -d "${SKILLS_DIR}" ]] || { print_error "Skills directory missing"; ((errors++)); }
    [[ -d "${COMMANDS_DIR}" ]] || { print_error "Commands directory missing"; ((errors++)); }
    [[ -d "${AGENTS_DIR}" ]] || { print_error "Agents directory missing"; ((errors++)); }
    [[ -d "${CORE_DIR}" ]] || { print_error "Core directory missing"; ((errors++)); }
    [[ -d "${HOOKS_DIR}" ]] || { print_error "Hooks directory missing"; ((errors++)); }

    # Check key files
    [[ -f "${HOOKS_CONFIG}" ]] || { print_error "hooks.json missing"; ((errors++)); }
    [[ -f "${VERSION_FILE}" ]] || { print_error "Version file missing"; ((errors++)); }
    [[ -x "${HOOKS_DIR}/session_start.sh" ]] || { print_error "session_start.sh not executable"; ((errors++)); }

    # Count installed items
    local skill_count=$(find "${SKILLS_DIR}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    local command_count=$(find "${COMMANDS_DIR}" -name "*.md" 2>/dev/null | wc -l)
    local agent_count=$(find "${AGENTS_DIR}" -name "*.md" 2>/dev/null | wc -l)

    print_info "  Skills: ${skill_count}"
    print_info "  Commands: ${command_count}"
    print_info "  Agents: ${agent_count}"

    if [[ ${errors} -eq 0 ]]; then
        print_success "Installation verified successfully"
        return 0
    else
        print_error "Installation verification failed with ${errors} error(s)"
        return 1
    fi
}

# =============================================================================
# MAIN OPERATIONS
# =============================================================================

show_status() {
    print_header "Shannon Framework Installation Status"

    # Check local installation
    if check_local_installation; then
        local version=$(get_installed_version)
        if [[ -n "${version}" ]]; then
            print_success "Local installation: v${version}"
        else
            print_warning "Local installation: Yes (version unknown)"
        fi

        local skill_count=$(find "${SKILLS_DIR}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
        local command_count=$(find "${COMMANDS_DIR}" -name "*.md" 2>/dev/null | wc -l)
        local agent_count=$(find "${AGENTS_DIR}" -name "*.md" 2>/dev/null | wc -l)

        print_info "  Skills: ${skill_count}"
        print_info "  Commands: ${command_count}"
        print_info "  Agents: ${agent_count}"
        print_info "  Location: ${CLAUDE_CONFIG_DIR}"
    else
        print_info "Local installation: Not installed"
    fi

    echo ""

    # Check for plugins
    print_info "Checking for plugin installations..."
    if detect_any_plugin_installation; then
        print_warning "Plugin installation detected (should be removed)"
        detect_plugin_directories
        detect_marketplace_entries
    else
        print_success "No plugin installations found"
    fi

    echo ""

    # Recommendation
    if check_local_installation && ! detect_any_plugin_installation; then
        print_success "✅ Installation is clean (local only)"
    elif ! check_local_installation && ! detect_any_plugin_installation; then
        print_info "Shannon is not installed. Run: $0 --install"
    else
        print_warning "⚠️  Multiple installations detected. Run: $0 --install --force"
    fi
}

perform_install() {
    print_header "Shannon Framework v${SHANNON_VERSION} Installation"

    print_info "Source: ${SHANNON_ROOT}"
    print_info "Target: ${CLAUDE_CONFIG_DIR}"
    echo ""

    # Step 1: Check for existing installations
    local has_local=false
    local has_plugin=false
    local installed_version=""

    if check_local_installation; then
        has_local=true
        installed_version=$(get_installed_version)
    fi

    if detect_any_plugin_installation; then
        has_plugin=true
    fi

    # Step 2: Handle existing installations
    if [[ "${has_plugin}" == "true" ]]; then
        print_warning "Plugin installation detected!"
        echo ""

        if [[ "${FORCE}" == "true" ]]; then
            print_info "Force mode: Removing plugin installation automatically"
        else
            echo -e "${YELLOW}The plugin installation will conflict with local installation.${NC}"
            read -p "Remove plugin installation? (Y/n): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                : # Continue
            else
                print_error "Cannot proceed with plugin installed"
                exit 1
            fi
        fi

        remove_plugin_directories
        clean_marketplace_entries
        echo ""
    fi

    if [[ "${has_local}" == "true" ]]; then
        if [[ -n "${installed_version}" ]]; then
            print_info "Existing installation: v${installed_version}"

            if [[ "${installed_version}" == "${SHANNON_VERSION}" ]]; then
                if [[ "${FORCE}" == "true" ]]; then
                    print_info "Force mode: Reinstalling same version"
                else
                    echo -e "${YELLOW}Same version already installed.${NC}"
                    read -p "Reinstall? (y/N): " -n 1 -r
                    echo ""
                    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                        print_info "Installation cancelled"
                        exit 0
                    fi
                fi
            else
                print_info "Upgrading from v${installed_version} to v${SHANNON_VERSION}"
            fi
        else
            print_info "Existing installation found (version unknown)"
        fi

        print_action "Removing existing local installation..."
        remove_local_installation
        echo ""
    fi

    # Step 3: Fresh installation
    print_header "Installing Shannon v${SHANNON_VERSION}"

    create_directories
    install_skills
    install_commands
    install_agents
    install_core
    install_modes
    install_templates
    install_hooks
    update_path_references
    write_version_file

    echo ""

    # Step 4: Verify
    if verify_installation; then
        echo ""
        print_header "Installation Complete!"

        cat << COMPLETE

  ✅ Shannon Framework v${SHANNON_VERSION} installed successfully

  ${BOLD}IMPORTANT: Restart Claude Code for hooks to activate${NC}

  ${BOLD}Quick Start:${NC}
  1. Restart Claude Code
  2. Run: /shannon:status
  3. Run: /shannon:prime

  ${BOLD}Documentation:${NC}
  - Commands: ~/.claude/commands/shannon/
  - Skills:   ~/.claude/skills/shannon/
  - Core:     ~/.claude/core/shannon/

COMPLETE
        return 0
    else
        print_error "Installation failed - check log: ${LOG_FILE}"
        return 1
    fi
}

perform_uninstall() {
    print_header "Shannon Framework Uninstallation"

    if [[ "${FORCE}" == "false" ]]; then
        print_warning "This will remove ALL Shannon installations from your system."
        echo ""
        read -p "Are you sure? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Uninstallation cancelled"
            exit 0
        fi
    fi

    remove_all_shannon

    # Archive log
    if [[ -f "${LOG_FILE}" ]]; then
        mv "${LOG_FILE}" "${LOG_FILE}.$(date +%Y%m%d_%H%M%S).old" 2>/dev/null || true
    fi

    echo ""
    print_header "Uninstallation Complete"

    cat << UNINSTALL_DONE

  ✅ Shannon Framework has been removed

  ${BOLD}IMPORTANT: Restart Claude Code for changes to take effect${NC}

  To reinstall:
    $0 --install

UNINSTALL_DONE
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    parse_args "$@"

    # Ensure log directory exists
    mkdir -p "$(dirname "${LOG_FILE}")" 2>/dev/null || true

    log_to_file "=========================================="
    log_to_file "Shannon Installation Script v${SCRIPT_VERSION}"
    log_to_file "Mode: ${MODE}, Force: ${FORCE}"
    log_to_file "=========================================="

    case "${MODE}" in
        install)
            perform_install
            exit $?
            ;;
        uninstall)
            perform_uninstall
            exit 0
            ;;
        status)
            show_status
            exit 0
            ;;
        *)
            print_error "Invalid mode: ${MODE}"
            exit 1
            ;;
    esac
}

main "$@"
