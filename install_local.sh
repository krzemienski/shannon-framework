#!/bin/bash

# Shannon Framework - Local Installation Script
# Version: 5.5.0
# Purpose: Install Shannon Framework directly to user's Claude configuration
#          instead of using the plugin system (which has discovery issues)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

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

# Logging
LOG_FILE="${HOME}/.claude/shannon_install.log"

# Installation mode
MODE="install"  # install, update, or uninstall

# Function: Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "${LOG_FILE}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "${LOG_FILE}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "${LOG_FILE}"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${LOG_FILE}"
}

print_action() {
    echo -e "${CYAN}[ACTION]${NC} $1" | tee -a "${LOG_FILE}"
}

# Function: Show usage
show_usage() {
    cat << EOF
Shannon Framework v5.0 - Local Installation Script

Usage: $0 [OPTIONS]

OPTIONS:
    --install       Install Shannon Framework (default)
    --update        Update existing installation
    --uninstall     Remove Shannon Framework installation
    --help          Show this help message

EXAMPLES:
    $0                    # Fresh installation
    $0 --install          # Explicit installation
    $0 --update           # Update existing installation
    $0 --uninstall        # Remove installation

INSTALLATION TARGETS:
    ~/.claude/skills/shannon/
    ~/.claude/commands/shannon/
    ~/.claude/agents/shannon/
    ~/.claude/core/shannon/
    ~/.claude/modes/shannon/
    ~/.claude/templates/shannon/
    ~/.claude/hooks/shannon/
    ~/.claude/hooks.json

For detailed documentation, see: INSTALL_LOCAL.md
EOF
}

# Function: Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --install)
                MODE="install"
                shift
                ;;
            --update)
                MODE="update"
                shift
                ;;
            --uninstall)
                MODE="uninstall"
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

# Function: Detect if Shannon plugin is installed
detect_plugin_installation() {
    print_info "Checking for Shannon plugin installation..."

    # Check for plugin directory
    local plugin_dir="${HOME}/.cursor/plugins/shannon@shannon-framework"
    local plugin_dir_alt="${HOME}/.claude/plugins/shannon@shannon-framework"

    if [ -d "${plugin_dir}" ] || [ -d "${plugin_dir_alt}" ]; then
        print_warning "Shannon plugin installation detected"
        return 0
    else
        print_info "No Shannon plugin installation found"
        return 1
    fi
}

# Function: Uninstall Shannon plugin
uninstall_plugin() {
    print_action "Uninstalling Shannon plugin..."

    # Look for plugin directories
    local plugin_dirs=(
        "${HOME}/.cursor/plugins/shannon@shannon-framework"
        "${HOME}/.claude/plugins/shannon@shannon-framework"
    )

    local found=false

    for plugin_dir in "${plugin_dirs[@]}"; do
        if [ -d "${plugin_dir}" ]; then
            print_info "  Removing plugin directory: ${plugin_dir}"
            rm -rf "${plugin_dir}"
            found=true
        fi
    done

    if [ "${found}" = true ]; then
        print_success "Shannon plugin uninstalled"
        print_warning "Please restart Claude Code for changes to take effect"
    else
        print_info "No plugin directories found to remove"
    fi
}

# Function: Uninstall local installation
uninstall_local() {
    print_action "Uninstalling Shannon Framework local installation..."

    local dirs_to_remove=(
        "${SKILLS_DIR}"
        "${COMMANDS_DIR}"
        "${AGENTS_DIR}"
        "${CORE_DIR}"
        "${MODES_DIR}"
        "${TEMPLATES_DIR}"
        "${HOOKS_DIR}"
    )

    local removed_count=0

    for dir in "${dirs_to_remove[@]}"; do
        if [ -d "${dir}" ]; then
            print_info "  Removing: ${dir}"
            rm -rf "${dir}"
            ((removed_count++))
        fi
    done

    # Handle hooks.json
    if [ -f "${HOOKS_CONFIG}" ]; then
        print_info "  Checking hooks.json..."

        # Check if hooks.json contains ONLY Shannon hooks
        if grep -q "shannon" "${HOOKS_CONFIG}"; then
            # Backup first
            local backup="${HOOKS_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "${HOOKS_CONFIG}" "${backup}"
            print_info "  Backed up hooks.json to: ${backup}"

            # Check for the most recent backup
            local latest_backup=$(ls -t "${HOOKS_CONFIG}.backup."* 2>/dev/null | head -1)

            if [ -f "${latest_backup}" ] && [ "${latest_backup}" != "${backup}" ]; then
                print_action "  Restoring hooks.json from backup: ${latest_backup}"
                cp "${latest_backup}" "${HOOKS_CONFIG}"
            else
                print_warning "  No previous backup found. Removing hooks.json."
                print_warning "  You may need to reconfigure hooks manually."
                rm "${HOOKS_CONFIG}"
            fi
        fi
    fi

    if [ ${removed_count} -gt 0 ]; then
        print_success "Uninstalled ${removed_count} Shannon directories"
    else
        print_warning "No Shannon installation found to remove"
    fi

    # Clean up log file
    if [ -f "${LOG_FILE}" ]; then
        print_info "  Archiving log file..."
        mv "${LOG_FILE}" "${LOG_FILE}.$(date +%Y%m%d_%H%M%S).old"
    fi

    print_success "Uninstallation complete"
    echo ""
    print_warning "Please restart Claude Code for changes to take effect"
}

# Function: Check if local installation exists
check_local_installation() {
    if [ -d "${SKILLS_DIR}" ] || [ -d "${COMMANDS_DIR}" ] || [ -d "${AGENTS_DIR}" ]; then
        return 0  # Installation exists
    else
        return 1  # No installation
    fi
}

# Function: Create directory structure
create_directories() {
    print_info "Creating installation directories..."

    mkdir -p "${SKILLS_DIR}"
    mkdir -p "${COMMANDS_DIR}"
    mkdir -p "${AGENTS_DIR}"
    mkdir -p "${CORE_DIR}"
    mkdir -p "${MODES_DIR}"
    mkdir -p "${TEMPLATES_DIR}"
    mkdir -p "${HOOKS_DIR}"

    print_success "Directories created"
}

# Function: Install skills
install_skills() {
    print_info "Installing skills..."

    local skill_count=0

    # Copy each skill directory
    for skill_dir in "${SHANNON_ROOT}/skills"/*; do
        if [ -d "${skill_dir}" ]; then
            local skill_name=$(basename "${skill_dir}")

            # Skip README.md file
            if [ "${skill_name}" = "README.md" ]; then
                continue
            fi

            print_info "  Installing skill: ${skill_name}"

            # Create skill directory
            mkdir -p "${SKILLS_DIR}/${skill_name}"

            # Copy all files from skill directory
            cp -r "${skill_dir}"/* "${SKILLS_DIR}/${skill_name}/"

            ((skill_count++))
        fi
    done

    print_success "Installed ${skill_count} skills"
}

# Function: Install commands
install_commands() {
    print_info "Installing commands..."

    local command_count=0

    # Copy each command file
    for command_file in "${SHANNON_ROOT}/commands"/*.md; do
        if [ -f "${command_file}" ]; then
            local command_name=$(basename "${command_file}")

            print_info "  Installing command: ${command_name}"

            cp "${command_file}" "${COMMANDS_DIR}/"

            ((command_count++))
        fi
    done

    print_success "Installed ${command_count} commands"
}

# Function: Install agents
install_agents() {
    print_info "Installing agents..."

    local agent_count=0

    # Copy each agent file
    for agent_file in "${SHANNON_ROOT}/agents"/*.md; do
        if [ -f "${agent_file}" ]; then
            local agent_name=$(basename "${agent_file}")

            print_info "  Installing agent: ${agent_name}"

            cp "${agent_file}" "${AGENTS_DIR}/"

            ((agent_count++))
        fi
    done

    print_success "Installed ${agent_count} agents"
}

# Function: Install core files
install_core() {
    print_info "Installing core behavioral patterns..."

    local core_count=0

    # Copy each core file
    for core_file in "${SHANNON_ROOT}/core"/*.md; do
        if [ -f "${core_file}" ]; then
            local core_name=$(basename "${core_file}")

            print_info "  Installing core: ${core_name}"

            cp "${core_file}" "${CORE_DIR}/"

            ((core_count++))
        fi
    done

    print_success "Installed ${core_count} core files"
}

# Function: Install modes
install_modes() {
    print_info "Installing modes..."

    local mode_count=0

    # Copy each mode file
    for mode_file in "${SHANNON_ROOT}/modes"/*.md; do
        if [ -f "${mode_file}" ]; then
            local mode_name=$(basename "${mode_file}")

            print_info "  Installing mode: ${mode_name}"

            cp "${mode_file}" "${MODES_DIR}/"

            ((mode_count++))
        fi
    done

    print_success "Installed ${mode_count} modes"
}

# Function: Install templates
install_templates() {
    print_info "Installing templates..."

    local template_count=0

    # Copy each template file
    for template_file in "${SHANNON_ROOT}/templates"/*.md; do
        if [ -f "${template_file}" ]; then
            local template_name=$(basename "${template_file}")

            print_info "  Installing template: ${template_name}"

            cp "${template_file}" "${TEMPLATES_DIR}/"

            ((template_count++))
        fi
    done

    print_success "Installed ${template_count} templates"
}

# Function: Install hooks with using-shannon content embedded
install_hooks() {
    print_info "Installing hooks..."

    # Install hook scripts
    print_info "  Installing hook scripts..."

    # Copy Python hooks
    cp "${SHANNON_ROOT}/hooks/user_prompt_submit.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/precompact.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/post_tool_use.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/stop.py" "${HOOKS_DIR}/"

    # Create session_start.sh with embedded using-shannon content
    print_info "  Creating session_start.sh with embedded using-shannon content..."

    cat > "${HOOKS_DIR}/session_start.sh" << 'HOOK_EOF'
#!/bin/bash
# Shannon Framework V5 - SessionStart Hook
# Loads using-shannon meta-skill to establish Shannon workflows
# Note: using-shannon content is embedded below (not referenced from file)

echo "<EXTREMELY_IMPORTANT>"
echo "You are using Shannon Framework V5."
echo ""
echo "**The content below is the using-shannon skill:**"
echo ""

# Embedded using-shannon skill content
cat << 'SKILL_EOF'
SKILL_EOF

    # Append the actual using-shannon skill content
    cat "${SHANNON_ROOT}/skills/using-shannon/SKILL.md" >> "${HOOKS_DIR}/session_start.sh"

    # Close the heredoc
    cat >> "${HOOKS_DIR}/session_start.sh" << 'HOOK_EOF'
SKILL_EOF

echo ""
echo "</EXTREMELY_IMPORTANT>"
HOOK_EOF

    # Make all hooks executable
    chmod +x "${HOOKS_DIR}/session_start.sh"
    chmod +x "${HOOKS_DIR}/user_prompt_submit.py"
    chmod +x "${HOOKS_DIR}/precompact.py"
    chmod +x "${HOOKS_DIR}/post_tool_use.py"
    chmod +x "${HOOKS_DIR}/stop.py"

    print_success "Hook scripts installed"

    # Update hooks.json
    print_info "  Updating hooks.json..."

    # Backup existing hooks.json if it exists
    if [ -f "${HOOKS_CONFIG}" ]; then
        cp "${HOOKS_CONFIG}" "${HOOKS_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        print_warning "Existing hooks.json backed up"
    fi

    # Create new hooks.json with Shannon hooks
    cat > "${HOOKS_CONFIG}" << 'HOOKS_JSON_EOF'
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "Shannon North Star goal injection for consistent goal alignment",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/user_prompt_submit.py",
            "description": "Injects North Star goal and active wave context into every prompt",
            "timeout": 2000
          }
        ]
      }
    ],

    "PreCompact": [
      {
        "description": "Shannon context preservation - Saves comprehensive checkpoint before auto-compaction to prevent information loss",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/precompact.py",
            "description": "Triggers CONTEXT_GUARDIAN agent to create Serena MCP checkpoint with complete session state",
            "timeout": 15000,
            "continueOnError": false
          }
        ]
      }
    ],

    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "description": "Shannon NO MOCKS testing philosophy enforcement",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/post_tool_use.py",
            "description": "Detects and blocks mock usage in test files to enforce functional testing",
            "timeout": 3000
          }
        ]
      }
    ],

    "Stop": [
      {
        "description": "Shannon wave validation gate enforcement",
        "hooks": [
          {
            "type": "command",
            "command": "${HOME}/.claude/hooks/shannon/stop.py",
            "description": "Blocks completion until wave validation gates are satisfied",
            "timeout": 2000
          }
        ]
      }
    ],

    "SessionStart": [
      {
        "description": "Shannon V5 meta-skill loader - loads using-shannon into every session",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${HOME}/.claude/hooks/shannon/session_start.sh",
            "description": "Loads using-shannon meta-skill to enforce Shannon workflows",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
HOOKS_JSON_EOF

    print_success "hooks.json updated"
}

# Function: Update path references in installed files
update_path_references() {
    print_info "Updating path references in installed files..."

    # Update skill references to core files
    print_info "  Updating skill references to core files..."

    # Find all skill.md files and update references
    find "${SKILLS_DIR}" -name "SKILL.md" -o -name "skill.md" | while read -r skill_file; do
        # Update references to core files
        # Cross-platform sed: create backup, then remove it
        sed -i.bak -e "s|shannon-plugin/core/|${HOME}/.claude/core/shannon/|g" \
                   -e "s|shannon-plugin/skills/|${HOME}/.claude/skills/shannon/|g" \
                   -e "s|shannon-plugin/agents/|${HOME}/.claude/agents/shannon/|g" \
                   -e "s|shannon-plugin/modes/|${HOME}/.claude/modes/shannon/|g" \
                   -e "s|shannon-plugin/templates/|${HOME}/.claude/templates/shannon/|g" \
                   "${skill_file}"

        # Remove backup files
        rm -f "${skill_file}.bak"
    done

    # Update command references
    print_info "  Updating command references..."

    find "${COMMANDS_DIR}" -name "*.md" | while read -r command_file; do
        # Cross-platform sed
        sed -i.bak -e "s|shannon-plugin/core/|${HOME}/.claude/core/shannon/|g" \
                   -e "s|shannon-plugin/skills/|${HOME}/.claude/skills/shannon/|g" \
                   -e "s|shannon-plugin/agents/|${HOME}/.claude/agents/shannon/|g" \
                   "${command_file}"

        rm -f "${command_file}.bak"
    done

    # Update agent references
    print_info "  Updating agent references..."

    find "${AGENTS_DIR}" -name "*.md" | while read -r agent_file; do
        # Cross-platform sed
        sed -i.bak -e "s|shannon-plugin/core/|${HOME}/.claude/core/shannon/|g" \
                   -e "s|shannon-plugin/skills/|${HOME}/.claude/skills/shannon/|g" \
                   "${agent_file}"

        rm -f "${agent_file}.bak"
    done

    # Update core file cross-references
    print_info "  Updating core file cross-references..."

    find "${CORE_DIR}" -name "*.md" | while read -r core_file; do
        # Cross-platform sed
        sed -i.bak -e "s|shannon-plugin/core/|${HOME}/.claude/core/shannon/|g" \
                   -e "s|shannon-plugin/skills/|${HOME}/.claude/skills/shannon/|g" \
                   "${core_file}"

        rm -f "${core_file}.bak"
    done

    print_success "Path references updated"
}

# Function: Verify installation
verify_installation() {
    print_info "Verifying installation..."

    local errors=0

    # Check skills
    if [ ! -d "${SKILLS_DIR}" ] || [ -z "$(ls -A ${SKILLS_DIR})" ]; then
        print_error "Skills directory is empty or missing"
        ((errors++))
    else
        local skill_count=$(find "${SKILLS_DIR}" -mindepth 1 -maxdepth 1 -type d | wc -l)
        print_success "Found ${skill_count} skills"
    fi

    # Check commands
    if [ ! -d "${COMMANDS_DIR}" ] || [ -z "$(ls -A ${COMMANDS_DIR})" ]; then
        print_error "Commands directory is empty or missing"
        ((errors++))
    else
        local command_count=$(find "${COMMANDS_DIR}" -name "*.md" | wc -l)
        print_success "Found ${command_count} commands"
    fi

    # Check agents
    if [ ! -d "${AGENTS_DIR}" ] || [ -z "$(ls -A ${AGENTS_DIR})" ]; then
        print_error "Agents directory is empty or missing"
        ((errors++))
    else
        local agent_count=$(find "${AGENTS_DIR}" -name "*.md" | wc -l)
        print_success "Found ${agent_count} agents"
    fi

    # Check core
    if [ ! -d "${CORE_DIR}" ] || [ -z "$(ls -A ${CORE_DIR})" ]; then
        print_error "Core directory is empty or missing"
        ((errors++))
    else
        local core_count=$(find "${CORE_DIR}" -name "*.md" | wc -l)
        print_success "Found ${core_count} core files"
    fi

    # Check hooks
    if [ ! -d "${HOOKS_DIR}" ] || [ -z "$(ls -A ${HOOKS_DIR})" ]; then
        print_error "Hooks directory is empty or missing"
        ((errors++))
    else
        print_success "Hooks installed"
    fi

    # Check hooks.json
    if [ ! -f "${HOOKS_CONFIG}" ]; then
        print_error "hooks.json missing"
        ((errors++))
    else
        print_success "hooks.json configured"
    fi

    # Check session_start.sh
    if [ ! -f "${HOOKS_DIR}/session_start.sh" ]; then
        print_error "session_start.sh missing"
        ((errors++))
    elif [ ! -x "${HOOKS_DIR}/session_start.sh" ]; then
        print_error "session_start.sh not executable"
        ((errors++))
    else
        print_success "session_start.sh configured"
    fi

    if [ ${errors} -eq 0 ]; then
        print_success "Installation verification passed"
        return 0
    else
        print_error "Installation verification failed with ${errors} errors"
        return 1
    fi
}

# Function: Display post-installation instructions
post_install_instructions() {
    cat << 'INSTRUCTIONS'

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          Shannon Framework v5.0 - Installation Complete        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Installation Summary:
─────────────────────────────────────────────────────────────────
  ✓ Skills installed to:     ~/.claude/skills/shannon/
  ✓ Commands installed to:   ~/.claude/commands/shannon/
  ✓ Agents installed to:     ~/.claude/agents/shannon/
  ✓ Core files installed to: ~/.claude/core/shannon/
  ✓ Modes installed to:      ~/.claude/modes/shannon/
  ✓ Templates installed to:  ~/.claude/templates/shannon/
  ✓ Hooks installed to:      ~/.claude/hooks/shannon/
  ✓ hooks.json configured

Next Steps:
─────────────────────────────────────────────────────────────────
1. RESTART Claude Code (REQUIRED for hooks to activate)

2. Verify Installation:
   Start a new Claude Code session and type:
     /shannon:status

   Expected output:
     "Shannon Framework v5.0 active"

3. Configure MCP Servers:
   Shannon requires Serena MCP (MANDATORY):
     /shannon:check_mcps

   Follow instructions to install any missing MCPs.

4. Start Using Shannon:
   Begin every session with:
     /shannon:prime

   For any project with specifications:
     /shannon:spec "your project description"

   For general tasks:
     /shannon:do "your task description"

Documentation:
─────────────────────────────────────────────────────────────────
  Commands:   ~/.claude/commands/shannon/*.md
  Skills:     ~/.claude/skills/shannon/*/SKILL.md
  Agents:     ~/.claude/agents/shannon/*.md
  Core:       ~/.claude/core/shannon/*.md

Troubleshooting:
─────────────────────────────────────────────────────────────────
  Installation Log:  ~/.claude/shannon_install.log

  If hooks don't fire:
    1. Check hooks.json: cat ~/.claude/hooks.json
    2. Verify hook scripts executable: ls -l ~/.claude/hooks/shannon/
    3. Restart Claude Code completely

  If skills not found:
    1. Check skills directory: ls ~/.claude/skills/shannon/
    2. Restart Claude Code
    3. Try /shannon:discover_skills

Support:
─────────────────────────────────────────────────────────────────
  Repository: https://github.com/shannon-framework/shannon
  Issues:     https://github.com/shannon-framework/shannon/issues

═══════════════════════════════════════════════════════════════════

INSTRUCTIONS
}

# Function: Display post-update instructions
post_update_instructions() {
    cat << 'INSTRUCTIONS'

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           Shannon Framework v5.0 - Update Complete             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Update Summary:
─────────────────────────────────────────────────────────────────
  ✓ All components updated to latest version
  ✓ Path references updated
  ✓ Hooks reconfigured

Next Steps:
─────────────────────────────────────────────────────────────────
1. RESTART Claude Code (REQUIRED for changes to take effect)

2. Verify Update:
   Start a new Claude Code session and type:
     /shannon:status

3. Check for Breaking Changes:
   Review: V5_RELEASE_NOTES.md

═══════════════════════════════════════════════════════════════════

INSTRUCTIONS
}

# Function: Perform installation
perform_install() {
    print_info "Shannon Framework v5.0 - Installation"
    print_info "Installing from: ${SHANNON_ROOT}"
    print_info "Installing to: ${CLAUDE_CONFIG_DIR}"
    echo ""

    # Check for plugin installation and offer to remove it
    if detect_plugin_installation; then
        echo ""
        print_warning "Shannon plugin installation detected!"
        print_warning "The plugin installation may conflict with local installation."
        echo ""
        read -p "Do you want to uninstall the plugin? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            uninstall_plugin
            echo ""
        else
            print_warning "Continuing with plugin still installed (may cause conflicts)"
            echo ""
        fi
    fi

    # Create directories
    create_directories
    echo ""

    # Install components
    install_skills
    echo ""

    install_commands
    echo ""

    install_agents
    echo ""

    install_core
    echo ""

    install_modes
    echo ""

    install_templates
    echo ""

    install_hooks
    echo ""

    # Update path references
    update_path_references
    echo ""

    # Verify installation
    if verify_installation; then
        echo ""
        print_success "Shannon Framework installation completed successfully!"
        echo ""

        # Display post-installation instructions
        post_install_instructions

        return 0
    else
        echo ""
        print_error "Shannon Framework installation completed with errors"
        print_error "Check log file: ${LOG_FILE}"
        return 1
    fi
}

# Function: Perform update
perform_update() {
    print_info "Shannon Framework v5.0 - Update"
    print_info "Updating from: ${SHANNON_ROOT}"
    print_info "Updating in: ${CLAUDE_CONFIG_DIR}"
    echo ""

    # Check if installation exists
    if ! check_local_installation; then
        print_error "No existing Shannon installation found"
        print_info "Use --install to perform fresh installation"
        exit 1
    fi

    print_info "Existing installation found. Proceeding with update..."
    echo ""

    # Backup existing installation
    print_action "Creating backup of existing installation..."
    local backup_dir="${HOME}/.claude/shannon_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "${backup_dir}"

    for dir in "${SKILLS_DIR}" "${COMMANDS_DIR}" "${AGENTS_DIR}" "${CORE_DIR}" "${MODES_DIR}" "${TEMPLATES_DIR}" "${HOOKS_DIR}"; do
        if [ -d "${dir}" ]; then
            local dirname=$(basename "$(dirname "${dir}")")
            local subdirname=$(basename "${dir}")
            cp -r "${dir}" "${backup_dir}/${subdirname}"
        fi
    done

    if [ -f "${HOOKS_CONFIG}" ]; then
        cp "${HOOKS_CONFIG}" "${backup_dir}/hooks.json"
    fi

    print_success "Backup created: ${backup_dir}"
    echo ""

    # Remove old files (but keep directories)
    print_action "Removing old files..."

    find "${SKILLS_DIR}" -mindepth 1 -delete 2>/dev/null || true
    find "${COMMANDS_DIR}" -mindepth 1 -delete 2>/dev/null || true
    find "${AGENTS_DIR}" -mindepth 1 -delete 2>/dev/null || true
    find "${CORE_DIR}" -mindepth 1 -delete 2>/dev/null || true
    find "${MODES_DIR}" -mindepth 1 -delete 2>/dev/null || true
    find "${TEMPLATES_DIR}" -mindepth 1 -delete 2>/dev/null || true
    find "${HOOKS_DIR}" -mindepth 1 -delete 2>/dev/null || true

    print_success "Old files removed"
    echo ""

    # Install updated components
    install_skills
    echo ""

    install_commands
    echo ""

    install_agents
    echo ""

    install_core
    echo ""

    install_modes
    echo ""

    install_templates
    echo ""

    install_hooks
    echo ""

    # Update path references
    update_path_references
    echo ""

    # Verify installation
    if verify_installation; then
        echo ""
        print_success "Shannon Framework update completed successfully!"
        echo ""

        # Display post-update instructions
        post_update_instructions

        print_info "Backup location: ${backup_dir}"
        print_info "If issues occur, restore from backup with: cp -r ${backup_dir}/* ~/.claude/"

        return 0
    else
        echo ""
        print_error "Shannon Framework update completed with errors"
        print_error "Check log file: ${LOG_FILE}"
        print_warning "To restore from backup: cp -r ${backup_dir}/* ~/.claude/"
        return 1
    fi
}

# Function: Perform uninstallation
perform_uninstall() {
    print_info "Shannon Framework v5.0 - Uninstallation"
    echo ""

    # Confirm uninstallation
    print_warning "This will remove all Shannon Framework components from your system."
    echo ""
    read -p "Are you sure you want to uninstall Shannon Framework? (y/N): " -n 1 -r
    echo ""
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi

    # Uninstall local installation
    uninstall_local
    echo ""

    # Check for plugin and offer to remove
    if detect_plugin_installation; then
        echo ""
        print_warning "Shannon plugin installation also detected."
        echo ""
        read -p "Do you want to uninstall the plugin too? (y/N): " -n 1 -r
        echo ""
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            uninstall_plugin
        fi
    fi

    echo ""
    cat << 'UNINSTALL_MSG'
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        Shannon Framework v5.0 - Uninstallation Complete        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Uninstallation Summary:
─────────────────────────────────────────────────────────────────
  ✓ All Shannon directories removed
  ✓ hooks.json backed up and cleaned
  ✓ Installation logs archived

Next Steps:
─────────────────────────────────────────────────────────────────
1. Restart Claude Code for changes to take effect

2. To reinstall Shannon Framework:
   ./install_local.sh --install

═══════════════════════════════════════════════════════════════════

UNINSTALL_MSG
}

# Main execution
main() {
    # Parse command line arguments
    parse_args "$@"

    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "${LOG_FILE}")"

    # Log start
    echo "=== Shannon Framework Installation Script ===" >> "${LOG_FILE}"
    echo "Date: $(date)" >> "${LOG_FILE}"
    echo "Mode: ${MODE}" >> "${LOG_FILE}"
    echo "=============================================" >> "${LOG_FILE}"
    echo "" >> "${LOG_FILE}"

    # Execute based on mode
    case "${MODE}" in
        install)
            perform_install
            exit $?
            ;;
        update)
            perform_update
            exit $?
            ;;
        uninstall)
            perform_uninstall
            exit 0
            ;;
        *)
            print_error "Invalid mode: ${MODE}"
            show_usage
            exit 1
            ;;
    esac
}

# Run main
main "$@"
